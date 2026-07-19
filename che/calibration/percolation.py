"""M2.1 hazard-only calibration engine (theory §3 made executable).

Pure-hazard percolation rollouts: no agents, no task, no smoke — the fire CA
kernel `hazard_step` (Def. 3) is reused *unchanged*. Protocol per (L, beta,
seed): all-Fuel L x L grid, single center ignition, scan T_max = 4L fixed
steps (absorption is cheap under jit; no early exit).

Measured per run:

- ``spanned``: any non-Fuel (Burning/Burnt) cell touches the grid boundary
  at T_max. Ever-ignited is absorbing, so the final-state check equals
  "ever touched the boundary".
- ``burnt_fraction``: non-Fuel fraction at T_max. DECISION: counts Burning
  as well as Burnt — chi-hat (M2.2, reused by Phase 3's Prop.-3 test) needs
  the total ignited cluster mass, and on the subcritical side the fire is
  long extinct at T_max = 4L so the two counts coincide there anyway.
- ``extinction_time``: first step t (1-based) with no Burning cell after
  the update, else T_max. With iota = 0 extinction is absorbing, so "first"
  is well defined.
- ``front_radius[t]``: running max over time of the Chebyshev radius (from
  the center ignition) of the non-Fuel set — the supercritical front-speed
  observable v-hat (M2.2).

Batching: `hazard_step` compares uniforms against a traced beta, so the run
is vmapped over seeds (inner) and betas (outer). Seed keys are shared across
betas — common random numbers realize Prop. 2's monotone coupling exactly,
which sharpens the finite-size curve crossings and the M2.3 isotonicity
test. Per-L key streams are separated via `fold_in(key, L)`.

Amendment 2026-07-19 (spec correction): the center-seed `spanned`
observable has one-sided finite-size bias (a smaller grid is easier to
span at every beta), so its finite-size curves never cross and estimator
(a) needs the canonical observable instead. `--mode crossing` ignites the
**full left column** at t=0 and records ``crossed`` = any non-Fuel cell in
the right column at T_max (ever-ignited is absorbing, so this equals
"fire ever reached the right column") — the left-right crossing
probability R_L(beta), whose finite-size curves do cross at beta_c.
Refined beta grid only; separate key stream (fold_in offset) from the
span mode.

CLI (writes che/bench/results/phase2/calibration.npz + provenance JSON):

    uv run python -m che.calibration.percolation                  # span mode
    uv run python -m che.calibration.percolation --mode crossing  # R_L mode
"""

import argparse
import functools
import json
import subprocess
import time
from pathlib import Path

import chex
import jax
import jax.numpy as jnp
import numpy as np

from che.env.hazard import hazard_step
from che.env.types import BURNING, FUEL

# Beta grid (M2.1): 0.05..0.95 step 0.05 coarse, refined 0.40..0.60 step
# 0.01. Built in integer hundredths so the union dedupes exactly.
_COARSE_HUNDREDTHS = range(5, 100, 5)
_FINE_HUNDREDTHS = range(40, 61, 1)

DEFAULT_SIZES = (32, 48, 64)
DEFAULT_N_SEEDS = 512


def beta_grid() -> jax.Array:
    """The deduplicated coarse + refined beta grid, float32, sorted."""
    hundredths = sorted(set(_COARSE_HUNDREDTHS) | set(_FINE_HUNDREDTHS))
    return jnp.asarray([b / 100.0 for b in hundredths], dtype=jnp.float32)


def fine_beta_grid() -> jax.Array:
    """The refined 0.40..0.60 step 0.01 grid only (crossing mode)."""
    return jnp.asarray(
        [b / 100.0 for b in _FINE_HUNDREDTHS], dtype=jnp.float32
    )


def percolation_run(
    key: jax.Array, beta: jax.Array, *, grid_size: int, t_max: int
) -> dict[str, jax.Array]:
    """One pure-hazard run: center ignition, T_max fixed CA steps.

    Returns per-run measurements (see module docstring). beta may be traced;
    grid_size and t_max are static.
    """
    center = grid_size // 2
    hazard0 = (
        jnp.full((grid_size, grid_size), FUEL, dtype=jnp.uint8)
        .at[center, center]
        .set(BURNING)
    )
    rows = jnp.arange(grid_size, dtype=jnp.int32)
    cheb = jnp.maximum(
        jnp.abs(rows - center)[:, None], jnp.abs(rows - center)[None, :]
    )

    def body(carry, xs):
        hazard, ext_time, front = carry
        key_t, t = xs
        hazard = hazard_step(key_t, hazard, beta=beta, iota=0.0)
        no_burning = ~(hazard == BURNING).any()
        ext_time = jnp.where(
            (ext_time == t_max) & no_burning, t, ext_time
        )
        front = jnp.maximum(
            front, jnp.max(jnp.where(hazard != FUEL, cheb, 0))
        )
        return (hazard, ext_time, front), front

    keys = jax.random.split(key, t_max)
    steps = jnp.arange(1, t_max + 1, dtype=jnp.int32)
    (hazard_final, ext_time, _), front_radius = jax.lax.scan(
        body,
        (hazard0, jnp.int32(t_max), jnp.int32(0)),
        (keys, steps),
    )

    non_fuel = hazard_final != FUEL
    spanned = (
        non_fuel[0].any()
        | non_fuel[-1].any()
        | non_fuel[:, 0].any()
        | non_fuel[:, -1].any()
    )
    return {
        "spanned": spanned,
        "burnt_fraction": non_fuel.mean(dtype=jnp.float32),
        "extinction_time": ext_time,
        "front_radius": front_radius,
    }


def crossing_run(
    key: jax.Array, beta: jax.Array, *, grid_size: int, t_max: int
) -> dict[str, jax.Array]:
    """One R_L run (2026-07-19 amendment): full left column ignited at t=0,
    T_max fixed CA steps; ``crossed`` = any non-Fuel cell in the right
    column at T_max (== "ever reached", since ever-ignited is absorbing).
    """
    hazard0 = (
        jnp.full((grid_size, grid_size), FUEL, dtype=jnp.uint8)
        .at[:, 0]
        .set(BURNING)
    )

    def body(hazard, key_t):
        return hazard_step(key_t, hazard, beta=beta, iota=0.0), None

    hazard_final, _ = jax.lax.scan(
        body, hazard0, jax.random.split(key, t_max)
    )
    return {"crossed": (hazard_final[:, -1] != FUEL).any()}


def run_ensemble(
    key: jax.Array,
    betas: jax.Array,
    *,
    grid_size: int,
    n_seeds: int,
    t_max: int,
    mode: str = "span",
) -> dict[str, jax.Array]:
    """vmap over (beta, seed): outputs have leading shape [n_beta, n_seeds].

    The same n_seeds keys are reused across betas (common random numbers;
    see module docstring). mode selects the per-run protocol: "span"
    (center seed, percolation_run) or "crossing" (left column, R_L).
    """
    chex.assert_rank(betas, 1)
    seed_keys = jax.random.split(key, n_seeds)
    run_fn = {"span": percolation_run, "crossing": crossing_run}[mode]
    run = functools.partial(run_fn, grid_size=grid_size, t_max=t_max)
    batched = jax.vmap(jax.vmap(run, in_axes=(0, None)), in_axes=(None, 0))
    return jax.jit(batched)(seed_keys, betas)


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
    p.add_argument("--n-seeds", type=int, default=DEFAULT_N_SEEDS)
    p.add_argument(
        "--sizes", type=int, nargs="+", default=list(DEFAULT_SIZES)
    )
    p.add_argument(
        "--mode", choices=("span", "crossing"), default="span"
    )
    p.add_argument(
        "--out-dir",
        type=Path,
        default=Path("che/bench/results/phase2"),
    )
    args = p.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    betas = beta_grid() if args.mode == "span" else fine_beta_grid()
    key = jax.random.PRNGKey(args.seed)
    # Crossing mode uses a disjoint fold_in offset so its draws never
    # collide with the span sweep's per-L streams.
    key_offset = 0 if args.mode == "span" else 1_000_000
    arrays: dict[str, np.ndarray] = {
        "betas": np.asarray(betas),
        "sizes": np.asarray(args.sizes, dtype=np.int32),
    }
    timings: dict[str, float] = {}
    for grid_size in args.sizes:
        t_max = 4 * grid_size
        t0 = time.perf_counter()
        out = run_ensemble(
            jax.random.fold_in(key, key_offset + grid_size),
            betas,
            grid_size=grid_size,
            n_seeds=args.n_seeds,
            t_max=t_max,
            mode=args.mode,
        )
        jax.block_until_ready(out)
        dt = time.perf_counter() - t0
        timings[f"L{grid_size}"] = dt
        for name, val in out.items():
            arrays[f"{name}_L{grid_size}"] = np.asarray(val)
        print(
            f"L={grid_size}: {betas.shape[0]} betas x {args.n_seeds} seeds"
            f" x {t_max} steps in {dt:.1f}s"
        )

    stem = (
        "calibration" if args.mode == "span" else "calibration_crossing"
    )
    npz_path = args.out_dir / f"{stem}.npz"
    np.savez_compressed(npz_path, **arrays)
    provenance = {
        "mode": args.mode,
        "jax_version": jax.__version__,
        "backend": jax.default_backend(),
        "device": str(jax.devices()[0]),
        "git_commit": _git_commit(),
        "seed": args.seed,
        "n_seeds": args.n_seeds,
        "sizes": args.sizes,
        "t_max": {f"L{s}": 4 * s for s in args.sizes},
        "n_betas": int(betas.shape[0]),
        "beta_grid": (
            "0.05:0.95:0.05 union 0.40:0.60:0.01"
            if args.mode == "span"
            else "0.40:0.60:0.01"
        ),
        "wall_seconds": timings,
        "timestamp_utc": time.strftime(
            "%Y-%m-%dT%H:%M:%SZ", time.gmtime()
        ),
    }
    prov_path = args.out_dir / f"{stem}_provenance.json"
    prov_path.write_text(json.dumps(provenance, indent=2) + "\n")
    print(f"wrote {npz_path} and {prov_path}")


if __name__ == "__main__":
    main()
