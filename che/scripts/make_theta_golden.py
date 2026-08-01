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

DEFAULT_OUT = Path("che/tests/golden/theta_golden_v1.json")

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


def _feed_state(h, state) -> None:
    for field in sorted(f.name for f in dataclasses.fields(state)):
        _feed(h, f"state.{field}", getattr(state, field))


def _feed_mapping(h, prefix: str, mapping: dict) -> None:
    for k in sorted(mapping):
        _feed(h, f"{prefix}.{k}", mapping[k])


def _actions(key: jax.Array, n_agents: int) -> jax.Array:
    return jax.random.randint(key, (n_agents,), 0, N_ACTIONS, dtype=jnp.int32)


def run_case(cfg_env, seed: int, n_steps: int, track: str) -> dict:
    """Roll one case and return its digests plus human-readable probes.

    TWO DIGESTS, and the split is a measured necessity rather than tidiness.

    `core`  — actions, EnvState, obs, reward, done: everything that *is* the
              trajectory and everything a later step can read back.
    `info`  — the diagnostic channels, which are Def.-2-compliant metrics no
              kernel ever reads.

    Generating this artifact surfaced a pre-existing jit/nojit divergence on
    severity_high: `info.survival_rate` differs by exactly one float32 ULP
    (5.96e-08) from t = 29 on, because `alive.mean()` reassociates differently
    once the first agent dies and the mean stops being exactly 1.0. No state,
    obs, reward or done field diverges. Splitting the digest lets acceptance
    2a demand bitwise equality on the trajectory in BOTH modes while grading
    float-reduction metrics separately, instead of being weakened wholesale
    by a rounding difference that predates the refactor and cannot feed back
    into any kernel.

    The probes are not the test — the digests are. They exist so a failing
    comparison can be diagnosed without re-deriving the trajectory by hand.
    """
    core = hashlib.sha256()
    meta = hashlib.sha256()
    key = jax.random.PRNGKey(seed)
    key, k_reset = jax.random.split(key)

    transition = step if track == "kernel" else step_autoreset
    obs, state = reset(k_reset, cfg_env)
    _feed_mapping(core, "obs0", obs)
    _feed_state(core, state)

    reward_sum = 0.0
    done_count = 0
    for t in range(n_steps):
        key, k_act, k_step = jax.random.split(key, 3)
        actions = _actions(k_act, cfg_env.n_agents)
        _feed(core, f"actions.{t}", actions)
        obs, state, reward, done, info = transition(k_step, state, actions, cfg_env)
        _feed_mapping(core, f"obs.{t}", obs)
        _feed_state(core, state)
        _feed(core, f"reward.{t}", reward)
        _feed(core, f"done.{t}", done)
        _feed_mapping(meta, f"info.{t}", info)
        reward_sum += float(reward)
        done_count += int(np.asarray(done))

    return {
        "digest_core": core.hexdigest(),
        "digest_info": meta.hexdigest(),
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


def _mode_agreement(entries: list[dict]) -> dict:
    """Do jit and nojit already produce identical digests ON MAIN?

    This bounds what 'bitwise' can mean as an acceptance criterion, so it is
    measured and recorded rather than assumed in either direction. Reported
    per digest: `core` is the trajectory, `info` the diagnostic channels.
    """
    out: dict = {}
    for which in ("core", "info"):
        by_case: dict[tuple, dict[str, str]] = {}
        for e in entries:
            key = (e["config"], e["track"], e["seed"])
            by_case.setdefault(key, {})[e["mode"]] = e[f"digest_{which}"]
        disagree = [k for k, v in by_case.items() if v.get("jit") != v.get("nojit")]
        out[which] = {
            "n_cases": len(by_case),
            "n_agree": len(by_case) - len(disagree),
            "n_disagree": len(disagree),
            "disagreeing": [list(k) for k in disagree],
        }
    return out


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
    for which, ma in built["mode_agreement"].items():
        print(
            f"{which:5s}: cases {ma['n_cases']}   jit==nojit {ma['n_agree']}"
            f"   differ {ma['n_disagree']}"
        )
        for row in ma["disagreeing"]:
            print(f"    MODE DIVERGENCE: {row}")

    if args.check:
        stored = json.loads(out.read_text())
        bad = []
        for which in ("core", "info"):
            old = {
                (e["config"], e["track"], e["seed"], e["mode"]): e[f"digest_{which}"]
                for e in stored["entries"]
            }
            new = {
                (e["config"], e["track"], e["seed"], e["mode"]): e[f"digest_{which}"]
                for e in built["entries"]
            }
            bad += [(which, k) for k in sorted(old) if old.get(k) != new.get(k)]
        n_digests = 2 * len(stored["entries"])
        print(f"\ncompared {n_digests} digests; mismatches: {len(bad)}")
        for which, k in bad:
            print(f"  {which} {k}")
        raise SystemExit(1 if bad else 0)

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(built, indent=1) + "\n")
    print(f"\nwrote {out}  ({len(built['entries'])} entries)")


if __name__ == "__main__":
    main()
