"""M6.0a — generate the pre-refactor golden trajectory artifact.

THIS SCRIPT MUST BE RUN ON CURRENT MAIN, BEFORE ANY PART OF THE TRACED-THETA
REFACTOR LANDS. Acceptance 2a of the M6.0 spike (decision_log.md, human
2026-08-01) is a *cross-tree* bitwise regression: traced-theta must reproduce
current-main trajectories bitwise under matched keys. The baseline it
compares against ceases to exist the moment the tree changes, so the golden
is the spike's first commit and its ordering is the one irreversible
constraint in the plan.

WHAT IS HASHED. Per step: every EnvState field, every observation array,
the reward, the done flag, and every `info` channel — i.e. the full
observable surface of one env transition. A refactor that perturbs any
kernel stream, any dtype, or any info channel moves the digest.

TWO TRACKS.
  kernel    — reset + step, driven by a fixed pseudo-random action sequence
              (no policy, no network parameters in the loop).
  autoreset — rollout.step_autoreset on a SHORT horizon so `done` actually
              fires several times. This is the path where the mixture will
              resample theta per episode, so it must be pinned before the
              refactor, not after.

TWO MODES. Entries are produced for both `jit` and `nojit` (via
jax.disable_jit). Whether those two already agree ON MAIN is itself a
finding the spike needs: it bounds what "bitwise" can mean as an acceptance
criterion. Recorded in the artifact rather than assumed either way.

Usage (CPU, from the repo root):
    uv run python -m che.scripts.make_theta_golden
    uv run python -m che.scripts.make_theta_golden --out <path> --check
"""

from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import subprocess
from pathlib import Path

import jax
import jax.numpy as jnp
import numpy as np

from che.env.config import load_config
from che.env.env import N_ACTIONS, reset, step
from che.train.rollout import step_autoreset

DEFAULT_OUT = Path("che/tests/golden/theta_golden.json")

# (config, n_steps). Kept small enough that the CPU suite stays fast in both
# modes; large enough that fire spreads, structures collapse, and Coupling A
# actually seeds on the configs where it is active.
CASES: tuple[tuple[str, int], ...] = (
    ("che/configs/debug.yaml", 64),
    ("che/configs/severity_low.yaml", 32),
    ("che/configs/severity_medium.yaml", 32),
    ("che/configs/severity_high.yaml", 32),
    ("che/configs/joint_medium.yaml", 32),
)
SEEDS: tuple[int, ...] = (0, 1)
# Autoreset track: short horizon so `done` fires repeatedly inside n_steps.
AUTORESET_HORIZON = 8


def _to_numpy(x) -> np.ndarray:
    """Device array -> numpy, unwrapping typed PRNG keys to their raw data."""
    try:
        if jnp.issubdtype(jnp.asarray(x).dtype, jax.dtypes.prng_key):
            x = jax.random.key_data(x)
    except (TypeError, AttributeError):
        pass
    return np.asarray(x)


def _feed(h, name: str, value) -> None:
    """Absorb one named array canonically: name, dtype, shape, then bytes."""
    a = _to_numpy(value)
    h.update(name.encode())
    h.update(str(a.dtype).encode())
    h.update(str(a.shape).encode())
    h.update(np.ascontiguousarray(a).tobytes())


def _actions(key: jax.Array, n_agents: int) -> jax.Array:
    return jax.random.randint(key, (n_agents,), 0, N_ACTIONS, dtype=jnp.int32)


def run_case(cfg_env, seed: int, n_steps: int, track: str) -> dict:
    """Roll one case and return a PER-FIELD digest map plus probes.

    ONE DIGEST PER FIELD, not one per trajectory — and the reason is the
    whole point of the artifact.

    A lumped digest can express "something changed" but not "a field was
    ADDED", and adding fields to `EnvState` is exactly what the traced-theta
    refactor does (`theta_live`, `mixture_component`). Under a lumped hash,
    acceptance 2a would fail on the very refactor it exists to certify, for a
    reason that is not a regression — and the temptation would then be to
    relax the criterion, which is how a safety proof quietly stops proving
    anything. Per field, the criterion stays strict: every field that existed
    before must hold identical bytes, while genuinely new fields surface as
    additive and must be acknowledged in the test's explicit allow-list.

    Fields are classified by prefix. `info.*` are the Def.-2-compliant
    diagnostic channels no kernel ever reads; everything else — `actions`,
    `state.*`, `obs.*`, `reward`, `done` — is the trajectory itself and
    everything a later step can read back. Nested dataclass state fields
    (e.g. `theta_live`) are flattened one level, so each traced scalar gets
    its own digest.

    Generating the first version of this artifact surfaced a PRE-EXISTING
    jit/nojit divergence on severity_high: `info.survival_rate` differs by
    exactly one float32 ULP (5.96e-08) from t = 29 on, because
    `alive.mean()` reassociates once the first agent dies and the mean stops
    being exactly 1.0. Per-field digests localize that to the single channel
    instead of tainting the trajectory verdict.

    The probes are not the test — the digests are. They exist so a failing
    comparison can be diagnosed without re-deriving the trajectory by hand.
    """
    hashes: dict = {}

    def feed(name: str, value) -> None:
        _feed(hashes.setdefault(name, hashlib.sha256()), name, value)

    def feed_state(s) -> None:
        for f in sorted(x.name for x in dataclasses.fields(s)):
            value = getattr(s, f)
            if dataclasses.is_dataclass(value):  # nested, e.g. theta_live
                for g in sorted(x.name for x in dataclasses.fields(value)):
                    feed(f"state.{f}.{g}", getattr(value, g))
            else:
                feed(f"state.{f}", value)

    def feed_mapping(prefix: str, mapping: dict) -> None:
        for k in sorted(mapping):
            feed(f"{prefix}.{k}", mapping[k])

    key = jax.random.PRNGKey(seed)
    key, k_reset = jax.random.split(key)

    transition = step if track == "kernel" else step_autoreset
    obs, state = reset(k_reset, cfg_env)
    feed_mapping("obs", obs)
    feed_state(state)

    reward_sum = 0.0
    done_count = 0
    for _ in range(n_steps):
        key, k_act, k_step = jax.random.split(key, 3)
        actions = _actions(k_act, cfg_env.n_agents)
        feed("actions", actions)
        obs, state, reward, done, info = transition(k_step, state, actions, cfg_env)
        feed_mapping("obs", obs)
        feed_state(state)
        feed("reward", reward)
        feed("done", done)
        feed_mapping("info", info)
        reward_sum += float(reward)
        done_count += int(np.asarray(done))

    return {
        "fields": {k: h.hexdigest() for k, h in sorted(hashes.items())},
        "probe": {
            "reward_sum": round(reward_sum, 6),
            "done_count": done_count,
            "final_t": int(np.asarray(state.t)),
            "final_alive": int(np.asarray(state.agent_alive).sum()),
            "final_burnt_cells": int((np.asarray(state.hazard) != 0).sum()),
            "ep_deaths_fire": int(np.asarray(state.ep_deaths_fire)),
            "ep_deaths_collapse": int(np.asarray(state.ep_deaths_collapse)),
        },
    }


def build(cases=CASES, seeds=SEEDS) -> dict:
    entries: list[dict] = []
    for cfg_path, n_steps in cases:
        base = load_config(cfg_path).env
        for track in ("kernel", "autoreset"):
            cfg_env = (
                base
                if track == "kernel"
                else dataclasses.replace(base, horizon=AUTORESET_HORIZON)
            )
            for seed in seeds:
                for mode in ("jit", "nojit"):
                    ctx = jax.disable_jit() if mode == "nojit" else _null_ctx()
                    with ctx:
                        result = run_case(cfg_env, seed, n_steps, track)
                    entries.append(
                        {
                            "config": cfg_path,
                            "track": track,
                            "seed": seed,
                            "mode": mode,
                            "n_steps": n_steps,
                            "horizon": int(cfg_env.horizon),
                            **result,
                        }
                    )
    return {
        "format": 2,
        "artifact": "M6.0a pre-refactor golden (theta as a compile-time constant)",
        "purpose": (
            "Cross-tree bitwise regression baseline for the traced-theta "
            "refactor. Acceptance 2a of the M6.0 spike."
        ),
        "provenance": _provenance(),
        "spec": {
            "seeds": list(seeds),
            "autoreset_horizon": AUTORESET_HORIZON,
            "hashed": (
                "per step: every EnvState field, every obs array, reward, done, "
                "and every info channel; plus the driving action sequence"
            ),
        },
        "mode_agreement": _mode_agreement(entries),
        "entries": entries,
    }


class _null_ctx:
    def __enter__(self):
        return None

    def __exit__(self, *a):
        return False


def _provenance() -> dict:
    def _git(*args: str) -> str:
        try:
            return subprocess.check_output(
                ["git", *args], text=True, stderr=subprocess.DEVNULL
            ).strip()
        except Exception:  # noqa: BLE001 - provenance is best-effort
            return "unknown"

    return {
        "git_commit": _git("rev-parse", "HEAD"),
        "git_dirty_files": len(_git("status", "--porcelain").splitlines()),
        "jax_version": jax.__version__,
        "platform": jax.default_backend(),
        "devices": [str(d) for d in jax.devices()],
        "x64_enabled": bool(jax.config.jax_enable_x64),
    }


def is_info(field: str) -> bool:
    """Diagnostic channels (Def.-2 metrics no kernel reads) vs the trajectory."""
    return field.startswith("info.")


def _mode_agreement(entries: list[dict]) -> dict:
    """Do jit and nojit already produce identical digests ON MAIN?

    This bounds what 'bitwise' can mean as an acceptance criterion, so it is
    measured and recorded rather than assumed in either direction. Reported
    per field so a divergence names the channel it lives in — the difference
    between "High diverges" and "survival_rate diverges".
    """
    by_case: dict[tuple, dict[str, dict]] = {}
    for e in entries:
        key = (e["config"], e["track"], e["seed"])
        by_case.setdefault(key, {})[e["mode"]] = e["fields"]

    diverging: list[dict] = []
    for case, modes in sorted(by_case.items()):
        a, b = modes.get("jit", {}), modes.get("nojit", {})
        bad = sorted(f for f in set(a) | set(b) if a.get(f) != b.get(f))
        if bad:
            diverging.append({"case": list(case), "fields": bad})

    all_fields = sorted({f for e in entries for f in e["fields"]})
    return {
        "n_cases": len(by_case),
        "n_cases_diverging": len(diverging),
        "diverging_fields": sorted({f for d in diverging for f in d["fields"]}),
        "detail": diverging,
        "n_fields_tracked": len(all_fields),
        "n_trajectory_fields": sum(1 for f in all_fields if not is_info(f)),
        "n_info_fields": sum(1 for f in all_fields if is_info(f)),
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    ap.add_argument(
        "--check",
        action="store_true",
        help="regenerate and compare against the artifact instead of writing it",
    )
    args = ap.parse_args()
    out = Path(args.out)

    built = build()
    ma = built["mode_agreement"]
    print(
        f"cases {ma['n_cases']}   fields/case {ma['n_fields_tracked']} "
        f"({ma['n_trajectory_fields']} trajectory + {ma['n_info_fields']} info)"
    )
    print(f"jit vs nojit: {ma['n_cases_diverging']} case(s) diverge")
    for row in ma["detail"]:
        print(f"    MODE DIVERGENCE {row['case']}: {row['fields']}")

    if args.check:
        stored = json.loads(out.read_text())
        old = {
            (e["config"], e["track"], e["seed"], e["mode"]): e["fields"]
            for e in stored["entries"]
        }
        new = {
            (e["config"], e["track"], e["seed"], e["mode"]): e["fields"]
            for e in built["entries"]
        }
        changed, added, missing, n = [], set(), set(), 0
        for case, fields in sorted(old.items()):
            cur = new.get(case, {})
            for f, d in sorted(fields.items()):
                n += 1
                if f not in cur:
                    missing.add(f)
                elif cur[f] != d:
                    changed.append((case, f))
            added |= set(cur) - set(fields)
        print(f"\ncompared {n} field digests")
        print(
            f"  changed: {len(changed)}   missing: {len(missing)}"
            f"   added: {len(added)}"
        )
        for case, f in changed[:20]:
            print(f"    CHANGED {f}  {case}")
        for f in sorted(missing):
            print(f"    MISSING {f}")
        for f in sorted(added):
            print(f"    ADDED   {f}  (additive — acknowledge in the test allow-list)")
        raise SystemExit(1 if (changed or missing) else 0)

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(built, indent=1) + "\n")
    print(f"\nwrote {out}  ({len(built['entries'])} entries)")


if __name__ == "__main__":
    main()
