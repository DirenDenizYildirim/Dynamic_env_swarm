"""M6.0a — the cross-tree bitwise regression (spike acceptance 2a).

`che/tests/golden/theta_golden_v1.json` was generated on main BEFORE any part
of the traced-theta refactor landed (M6.0 ruling, decision_log.md 2026-08-01:
"the golden artifact is the first commit; nothing lands on the refactor path
before its hash exists"). These tests re-roll the same trajectories in the
current tree and demand the digests still match.

This is the safety proof of the whole refactor. Once theta becomes a per-env
traced field, XLA can no longer constant-fold it, and a silent change in any
kernel stream, dtype, or info channel would otherwise be invisible until it
showed up as an unexplained shift in a Phase-6 result.

DIGEST SPLIT, and why it is not a weakening. `core` covers actions, EnvState,
obs, reward and done — the trajectory itself, and everything a later step can
read back. `info` covers the Def.-2-compliant diagnostic channels, which no
kernel ever reads. Generating the golden measured a PRE-EXISTING jit/nojit
divergence on severity_high: `info.survival_rate` differs by exactly one
float32 ULP (5.96e-08) from t = 29, because `alive.mean()` reassociates once
the first agent dies and the mean stops being exactly 1.0. `core` agreed in
20/20 cases. Both digests are stored PER MODE, so both are compared strictly
here — the split localizes the known rounding difference instead of excusing
it.
"""

from __future__ import annotations

import dataclasses
import json
from pathlib import Path

import jax
import pytest

from che.env.config import load_config
from che.scripts.make_theta_golden import AUTORESET_HORIZON, run_case

GOLDEN = Path(__file__).resolve().parent / "golden" / "theta_golden_v1.json"


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
    assert ARTIFACT["provenance"]["git_commit"] != "unknown"
    assert ARTIFACT["entries"], "golden artifact carries no entries"
    for e in ARTIFACT["entries"]:
        assert len(e["digest_core"]) == 64
        assert len(e["digest_info"]) == 64


def test_core_trajectory_is_mode_independent_on_main():
    """The recorded property acceptance 2a leans on.

    If a future change makes the *trajectory* depend on whether JIT is on,
    that is a bug in its own right — and it would also silently redefine what
    the bitwise criterion means.
    """
    core = ARTIFACT["mode_agreement"]["core"]
    assert core["n_disagree"] == 0, (
        f"core digests became mode-dependent: {core['disagreeing']}. The "
        "bitwise acceptance criterion assumes the trajectory does not depend "
        "on the JIT setting."
    )


def test_known_info_divergence_is_still_the_only_one():
    """Guards the localization, so a NEW float-reduction divergence cannot
    hide behind the one already diagnosed (survival_rate, 1 ULP, High)."""
    info = ARTIFACT["mode_agreement"]["info"]
    known = {("che/configs/severity_high.yaml", "kernel", 0),
             ("che/configs/severity_high.yaml", "kernel", 1)}
    got = {tuple(x) for x in info["disagreeing"]}
    assert got == known, (
        f"info-channel mode divergence changed: {got ^ known}. The known case "
        "is survival_rate on severity_high (alive.mean() reassociation, 1 ULP). "
        "A new one needs its own localization before it is accepted."
    )


# ------------------------------------------------------- the regression itself


@pytest.mark.parametrize("entry", _entries_for_mode(), ids=_ident)
def test_trajectory_matches_golden(entry):
    """Re-roll and compare. A failure here means the current tree no longer
    reproduces pre-refactor behaviour bitwise."""
    result = run_case(
        _cfg_for(entry), entry["seed"], entry["n_steps"], entry["track"]
    )
    assert result["digest_core"] == entry["digest_core"], (
        f"CORE TRAJECTORY CHANGED for {_ident(entry)} in {_mode()} mode.\n"
        f"  golden probe:  {entry['probe']}\n"
        f"  current probe: {result['probe']}\n"
        "This is M6.0 acceptance 2a. The traced-theta refactor must reproduce "
        "main bitwise at fixed locked theta; if this fails, the refactor "
        "changed environment behaviour and the ladder in decision_log.md "
        "applies (stop and report)."
    )
    assert result["digest_info"] == entry["digest_info"], (
        f"INFO CHANNELS CHANGED for {_ident(entry)} in {_mode()} mode "
        "(trajectory itself is intact).\n"
        f"  golden probe:  {entry['probe']}\n"
        f"  current probe: {result['probe']}\n"
        "Diagnostic channels are Def.-2-compliant metrics no kernel reads, so "
        "this cannot alter a trajectory — but it does alter every logged "
        "metric, and needs localizing to a specific channel before acceptance."
    )
