"""M3.4 Coupling-A parameter calibration engine (phase3_prompt.md).

Random-policy rollouts of the *full* environment (env.reset/env.step —
the training substrate itself, primary reset ignition included) at each
locked severity, measuring the M3.4 target observables per episode:

- ``n_collapses``: collapsed cells at the horizon (collapse is absorbing
  and episodes start fully intact, so the final stock equals the event
  count);
- ``n_seeded``: realized Coupling-A ignitions (sum of the
  info["seeded_ignitions"] channel);
- ``deaths_collapse`` / ``deaths_fire``: episode totals;
- ``burnt_cells``: non-Fuel count at the horizon;
- ``survival_rate`` at the horizon.

The Low-severity seeded-burnt share (target >= 50%) is measured by
**paired runs** kappa_A ∈ {0, kappa*} on identical episode keys — the
nesting invariant (unconditional PRNG consumption) makes the kappa_A = 0
member the exactly-nested model, so the pair is a clean common-random-
numbers estimate:  share = 1 - E[B(0)] / E[B(kappa*)].

Candidate design (expectations that motivate the grid; measured values
decide): E[collapses] ~ lambda_0 * f_weak * L^2 * T; E[seeded] ~
E[collapses] * 9 * kappa_A * P(Fuel); E[deaths_collapse] ~ lambda_load *
(alive-agent steps on weak cells) ~ lambda_load * n_agents * T * f_weak
for a random policy. r_seed stays at the config default 1 (3x3 ball,
Def. 5) — not swept.

CLI (writes che/bench/results/phase3/m34/coupling_a_calibration.json):

    nice -n 19 uv run python -m che.calibration.coupling_a
"""

import argparse
import json
import subprocess
import time
from pathlib import Path

import jax
import jax.numpy as jnp
import numpy as np

from che.env.config import EnvConfig, ThetaConfig
from che.env.env import reset, step
from che.env.types import COLLAPSED, FUEL

SEVERITIES = {"low": 0.43, "medium": 0.49, "high": 0.70}  # severity_lock.md
N_ACTIONS = 5  # stay + von Neumann (env._ACTION_OFFSETS)

# Candidate design (DECISION): factored along causal axes around a
# center candidate rather than fully crossed — each observable is driven
# by one axis (collapses by lambda_0 * f_weak; seeded and the Low share
# by kappa_A; deaths_collapse by lambda_load), so a cross would multiply
# compiles (one per frozen cfg) without adding information. The center
# candidate is measured in full; the proposal composes per-axis choices.
_BASE = {"f_weak": 0.15, "lambda_0": 5e-5, "kappa_A": 0.06, "lambda_load": 4e-4}
CANDIDATES: tuple[dict, ...] = (
    # Collapse axis: (f_weak, lambda_0), incl. one f_weak sensitivity pair.
    {**_BASE, "lambda_0": 3e-5},
    _BASE,
    {**_BASE, "lambda_0": 8e-5},
    {**_BASE, "f_weak": 0.25, "lambda_0": 3e-5},
    # Seeding axis: kappa_A at the base collapse rate.
    {**_BASE, "kappa_A": 0.03},
    {**_BASE, "kappa_A": 0.1},
    # Load axis: lambda_load at the base collapse rate.
    {**_BASE, "lambda_load": 1e-4},
    {**_BASE, "lambda_load": 1e-3},
)


def make_config(beta: float, cand: dict, *, kappa_A_override=None) -> EnvConfig:
    """Reference-scale env (64^2, 12 agents, horizon 256, obs v2) with the
    candidate's structure/coupling parameters."""
    return EnvConfig(
        grid_size=64,
        n_agents=12,
        horizon=256,
        obs_window=9,
        n_food=32,
        theta=ThetaConfig(
            beta=beta,
            kappa_A=(cand["kappa_A"] if kappa_A_override is None else kappa_A_override),
            lambda_0=cand["lambda_0"],
            lambda_load=cand["lambda_load"],
            f_weak=cand["f_weak"],
        ),
    )


def episode(key: jax.Array, cfg: EnvConfig) -> dict[str, jax.Array]:
    """One random-policy episode; returns the M3.4 observables."""
    k_reset, k_run = jax.random.split(key)
    _, state = reset(k_reset, cfg)

    def body(carry, key_t):
        state, n_seeded = carry
        k_act, k_step = jax.random.split(key_t)
        actions = jax.random.randint(
            k_act, (cfg.n_agents,), 0, N_ACTIONS, dtype=jnp.int32
        )
        _, state_new, _, _, info = step(k_step, state, actions, cfg)
        return (state_new, n_seeded + info["seeded_ignitions"]), None

    (state_f, n_seeded), _ = jax.lax.scan(
        body,
        (state, jnp.int32(0)),
        jax.random.split(k_run, cfg.horizon),
    )
    return {
        "n_collapses": (state_f.structure == COLLAPSED).sum(dtype=jnp.int32),
        "n_seeded": n_seeded,
        "deaths_collapse": state_f.ep_deaths_collapse,
        "deaths_fire": state_f.ep_deaths_fire,
        "burnt_cells": (state_f.hazard != FUEL).sum(dtype=jnp.int32),
        "survival_rate": state_f.agent_alive.mean(dtype=jnp.float32),
    }


def run_cell(key: jax.Array, cfg: EnvConfig, n_eps: int) -> dict[str, np.ndarray]:
    """n_eps random-policy episodes, vmapped; one compile per cfg."""
    out = jax.jit(jax.vmap(episode, in_axes=(0, None)), static_argnums=1)(
        jax.random.split(key, n_eps), cfg
    )
    return {k: np.asarray(v) for k, v in out.items()}


def summarize_cell(out: dict[str, np.ndarray]) -> dict:
    n = out["n_collapses"].shape[0]
    return {
        "n_eps": int(n),
        **{k: float(v.mean()) for k, v in out.items()},
        "se_deaths_collapse": float(out["deaths_collapse"].std() / np.sqrt(n)),
    }


def _git_commit() -> str:
    try:
        return subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--n-eps", type=int, default=128)
    p.add_argument(
        "--out-dir",
        type=Path,
        default=Path("che/bench/results/phase3/m34"),
    )
    args = p.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    key = jax.random.PRNGKey(args.seed)

    results = []
    t0 = time.perf_counter()
    for ci, cand in enumerate(CANDIDATES):
        row: dict = {"candidate": cand}
        # Same episode-key block for every severity and for the paired
        # kappa_A = 0 member (CRN throughout the row).
        k_cell = jax.random.fold_in(key, ci)
        for name, beta in SEVERITIES.items():
            cfg = make_config(beta, cand)
            row[name] = summarize_cell(run_cell(k_cell, cfg, args.n_eps))
        # Low-severity seeded-share via the paired nested run.
        cfg0 = make_config(SEVERITIES["low"], cand, kappa_A_override=0.0)
        out0 = run_cell(k_cell, cfg0, args.n_eps)
        b_low = row["low"]["burnt_cells"]
        b0 = float(out0["burnt_cells"].mean())
        row["low_seeded_share"] = 1.0 - b0 / b_low if b_low else 0.0
        row["low_burnt_kappa0"] = b0
        results.append(row)
        print(
            f"[{ci + 1}/{len(CANDIDATES)}] {cand} -> "
            f"low: coll {row['low']['n_collapses']:.1f}, "
            f"seeded {row['low']['n_seeded']:.2f}, "
            f"dc {row['low']['deaths_collapse']:.3f}, "
            f"share {row['low_seeded_share']:.2f}",
            flush=True,
        )

    payload = {
        "candidates": results,
        "n_eps": args.n_eps,
        "severities": SEVERITIES,
        "r_seed": 1,
        "targets": {
            "collapses_per_ep": [3, 10],
            "seeded_per_ep": [1, 5],
            "low_seeded_share_min": 0.5,
            "deaths_collapse_per_ep": [0.05, 0.5],
        },
        "jax_version": jax.__version__,
        "backend": jax.default_backend(),
        "git_commit": _git_commit(),
        "seed": args.seed,
        "wall_seconds": time.perf_counter() - t0,
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    path = args.out_dir / "coupling_a_calibration.json"
    path.write_text(json.dumps(payload, indent=2) + "\n")
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
