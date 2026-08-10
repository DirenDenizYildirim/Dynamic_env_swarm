"""M6.0a — the cross-tree bitwise regression (spike acceptance 2a).

`che/tests/golden/theta_golden.json` was generated on main BEFORE any part of
the traced-theta refactor landed (M6.0 ruling, decision_log.md 2026-08-01:
"the golden artifact is the first commit; nothing lands on the refactor path
before its hash exists"). These tests re-roll the same trajectories in the
current tree and demand every pre-existing field still hash identically.

This is the safety proof of the whole refactor. Once theta becomes a per-env
traced field, XLA can no longer constant-fold it, and a silent change in any
kernel stream, dtype, or info channel would otherwise stay invisible until it
surfaced as an unexplained shift in a Phase-6 result.

PER-FIELD, NOT PER-TRAJECTORY. A lumped digest cannot distinguish "a value
changed" from "a field was added", and adding fields to EnvState is exactly
what this refactor does. Hashing per field keeps the criterion strict —
every pre-existing field must match byte-for-byte — while letting genuinely
additive schema growth be acknowledged deliberately, in ALLOWED_NEW_FIELDS
below, rather than by weakening the test.

KNOWN, DIAGNOSED, AND PINNED: generating the golden measured a PRE-EXISTING
jit/nojit divergence in `info.survival_rate` on severity_high — exactly one
float32 ULP (5.96e-08) from t = 29, where `alive.mean()` reassociates once
the first agent dies and the mean stops being exactly 1.0. It is confined to
that one diagnostic channel; no trajectory field diverges.
"""

from __future__ import annotations

import dataclasses
import json
from pathlib import Path

import jax
import pytest

from che.env.config import load_config
from che.scripts.make_theta_golden import AUTORESET_HORIZON, is_info, run_case

GOLDEN = Path(__file__).resolve().parent / "golden" / "theta_golden.json"

# Fields the tree is allowed to ADD relative to the golden. Every entry is a
# deliberate schema change from a transcribed ruling — adding a name here is
# the acknowledgement, and anything not listed fails the suite.
#
# M6.0b (traced theta): the per-episode theta slice moves into EnvState, so
# each traced scalar and the drawn component index become state fields.
# M6.0c (mixture): the component index is also surfaced in `info` so a
# training run can be audited against its intended mixture weights (2d).
ALLOWED_NEW_FIELDS: frozenset[str] = frozenset(
    {
        "state.theta_live.beta",
        "state.theta_live.kappa_A",
        "state.theta_live.kappa_B",
        "state.theta_live.delta",
        "state.mixture_component",
        "info.mixture_component",
        # M6.1: fixed-width per-component realized-weight channels. Fixed
        # width is the point — the observable surface must not change with
        # the mixture, or every config would need its own golden.
        *(f"info.mixture_count_{i}" for i in range(8)),
        # Render-gate diagnostic (registrar 2026-08-10): positional drift.
        # Info-only, deterministic, no PRNG. That this entry is the ONLY
        # change the golden needed is the acceptance: every trajectory field
        # and every pre-existing info digest reproduced bitwise across all
        # four configs, both tracks and both modes, so the channels observe
        # the env without perturbing it.
        "info.center_dist_sum",
        "info.boundary_agents",
    }
)

# The one measured, localized mode divergence (see the module docstring).
KNOWN_MODE_DIVERGENCE: frozenset[str] = frozenset({"info.survival_rate"})


def _load() -> dict:
    with open(GOLDEN) as f:
        return json.load(f)


ARTIFACT = _load()


def _mode() -> str:
    return "nojit" if jax.config.jax_disable_jit else "jit"


def _entries_for_mode() -> list[dict]:
    return [e for e in ARTIFACT["entries"] if e["mode"] == _mode()]


def _ident(e: dict) -> str:
    return f"{Path(e['config']).stem}-{e['track']}-s{e['seed']}"


def _cfg_for(entry: dict):
    base = load_config(entry["config"]).env
    if entry["track"] == "autoreset":
        return dataclasses.replace(base, horizon=AUTORESET_HORIZON)
    return base


# ------------------------------------------------------------------ artifact


def test_golden_artifact_is_intact():
    assert ARTIFACT["format"] == 2
    assert ARTIFACT["provenance"]["git_commit"] != "unknown"
    assert ARTIFACT["entries"], "golden artifact carries no entries"
    for e in ARTIFACT["entries"]:
        assert e["fields"], f"{_ident(e)} has no field digests"
        assert all(len(d) == 64 for d in e["fields"].values())


def test_trajectory_is_mode_independent_on_main():
    """The property acceptance 2a leans on: whether JIT is enabled must not
    change the trajectory. If it ever does, that is a bug in its own right
    AND it silently redefines what the bitwise criterion means."""
    diverging = set(ARTIFACT["mode_agreement"]["diverging_fields"])
    trajectory = {f for f in diverging if not is_info(f)}
    assert not trajectory, (
        f"trajectory fields became mode-dependent: {sorted(trajectory)}"
    )


def test_known_info_divergence_is_still_the_only_one():
    """Guards the localization, so a NEW float-reduction divergence cannot
    hide behind the one already diagnosed."""
    diverging = set(ARTIFACT["mode_agreement"]["diverging_fields"])
    assert diverging == KNOWN_MODE_DIVERGENCE, (
        f"info-channel mode divergence changed: {diverging ^ KNOWN_MODE_DIVERGENCE}. "
        "The known case is survival_rate on severity_high (alive.mean() "
        "reassociation, 1 ULP). A new one needs its own localization first."
    )


# ------------------------------------------------------- the regression itself


@pytest.mark.parametrize("entry", _entries_for_mode(), ids=_ident)
def test_trajectory_matches_golden(entry):
    """Re-roll and compare every field. A failure means the current tree no
    longer reproduces pre-refactor behaviour bitwise."""
    result = run_case(_cfg_for(entry), entry["seed"], entry["n_steps"], entry["track"])
    now, golden = result["fields"], entry["fields"]

    missing = sorted(set(golden) - set(now))
    assert not missing, (
        f"FIELDS DISAPPEARED for {_ident(entry)}: {missing}. A field the golden "
        "recorded no longer exists — the observable surface shrank, which the "
        "additive allow-list does not cover."
    )

    changed = sorted(f for f in golden if now[f] != golden[f])
    traj = [f for f in changed if not is_info(f)]
    diag = [f for f in changed if is_info(f)]
    assert not traj, (
        f"TRAJECTORY CHANGED for {_ident(entry)} in {_mode()} mode: {traj}\n"
        f"  golden probe:  {entry['probe']}\n"
        f"  current probe: {result['probe']}\n"
        "This is M6.0 acceptance 2a. Traced theta must reproduce main bitwise "
        "at fixed locked theta; if this fails, the refactor changed environment "
        "behaviour and the ladder in decision_log.md applies (stop and report)."
    )
    assert not diag, (
        f"INFO CHANNELS CHANGED for {_ident(entry)} in {_mode()} mode: {diag}\n"
        f"  golden probe:  {entry['probe']}\n"
        f"  current probe: {result['probe']}\n"
        "The trajectory itself is intact. Diagnostic channels are Def.-2 "
        "metrics no kernel reads, so this cannot alter a trajectory — but it "
        "does alter every logged metric, and needs localizing to a specific "
        "channel before acceptance."
    )

    unexpected = sorted(set(now) - set(golden) - ALLOWED_NEW_FIELDS)
    assert not unexpected, (
        f"UNDECLARED NEW FIELDS for {_ident(entry)}: {unexpected}. Schema growth "
        "is allowed but must be deliberate: add the field to ALLOWED_NEW_FIELDS "
        "with the ruling that introduced it."
    )
