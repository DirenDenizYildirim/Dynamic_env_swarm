"""M3.3 diagnostic: decompose the sweep-slope vs chi-hat gap (Prop. 3).

The L = 64 GPU sweep (prop3_L64.json) measured slope/chi-hat = 0.686 —
below the L = 32 band but on the side Prop. 3 allows (E[B_T] <= lambda T
chi in general; every finite-size/finite-time correction is downward).
This script quantifies the three downward corrections separately, using
single-ignition hazard-only runs that record the cluster-mass *trajectory*
m(u) = E[non-Fuel cells at age u]:

1. **Conditioning** (chi-hat side): the Phase-2 estimator conditions on
   non-spanning, discarding the largest clusters, so chi-hat < the
   unconditional center-seed mass. Large at L = 32 (~18% span), small at
   L = 64 (~2%).
2. **Spatial truncation** (sweep side): sweep seeds are uniformly located,
   so clusters near the boundary are clipped; chi-hat ignites the center.
   Ratio m_unif(4L) / m_center(4L), unconditional.
3. **Temporal truncation** (sweep side): a seed born at step s grows for
   T - s steps; birth times are uniform, so the predicted sweep slope is
   the age-average (1/T) sum_{u=0}^{T-1} m_unif(u), with m_unif(0) = 1.
   Measured outcome: *minor* (~7% at both L) — cluster mass at beta =
   0.43 saturates by age ~64 steps, so the horizon-256 window is
   generous, refuting the pre-run hypothesis that 4L-exact starved
   late-born seeds at L = 64.

Residual after 1-3 = same-collapse multi-seeds (P(>=2 | >=1) = 7.9% at
kappa_A = 0.02 over the 3x3 ball — siblings share one cluster and
inflate the x-axis) + cross-cluster overlap (birth-adjacency proxy
0.08-0.13 in the sweep). Validation: the chain reproduces the L = 32
slow-test slope (residual factor 0.843 at L = 32 vs 0.836 at L = 64 —
L-independent, as it must be). Full accounting: phase3_report.md M3.3.

Writes che/bench/results/phase3/m33/deficit_decomposition.json.

    nice -n 19 uv run python -m che.scripts.prop3_deficit
"""

import json
import time
from pathlib import Path

import jax
import jax.numpy as jnp
import numpy as np

from che.calibration.prop3 import BETA_LOW, HORIZON
from che.env.hazard import hazard_step
from che.env.types import BURNING, FUEL

MC = {32: 8192, 64: 4096}  # runs per (L, location mode)


def mass_trajectory_run(
    key: jax.Array, *, grid_size: int, t_max: int, uniform_loc: bool
) -> dict[str, jax.Array]:
    """One single-ignition run recording m(u) for u = 1..t_max plus the
    final spanning flag (percolation_run protocol, trajectory added)."""
    k_loc, k_run = jax.random.split(key)
    if uniform_loc:
        flat = jax.random.randint(k_loc, (), 0, grid_size * grid_size)
        row, col = flat // grid_size, flat % grid_size
    else:
        row = col = grid_size // 2
    hazard0 = (
        jnp.full((grid_size, grid_size), FUEL, dtype=jnp.uint8)
        .at[row, col]
        .set(BURNING)
    )

    def body(hazard, key_t):
        hazard = hazard_step(key_t, hazard, beta=BETA_LOW, iota=0.0)
        return hazard, (hazard != FUEL).sum(dtype=jnp.int32)

    hazard_f, mass = jax.lax.scan(body, hazard0, jax.random.split(k_run, t_max))
    non_fuel = hazard_f != FUEL
    spanned = (
        non_fuel[0].any()
        | non_fuel[-1].any()
        | non_fuel[:, 0].any()
        | non_fuel[:, -1].any()
    )
    return {"mass": mass, "spanned": spanned}


def ensemble(
    key: jax.Array, *, grid_size: int, n_runs: int, uniform_loc: bool
) -> dict[str, np.ndarray]:
    run = jax.jit(
        jax.vmap(
            lambda k: mass_trajectory_run(
                k,
                grid_size=grid_size,
                t_max=HORIZON,
                uniform_loc=uniform_loc,
            )
        )
    )
    out = run(jax.random.split(key, n_runs))
    return {k: np.asarray(v) for k, v in out.items()}


def decompose(grid_size: int, key: jax.Array) -> dict:
    n = MC[grid_size]
    k_center, k_unif = jax.random.split(key)
    center = ensemble(k_center, grid_size=grid_size, n_runs=n, uniform_loc=False)
    unif = ensemble(k_unif, grid_size=grid_size, n_runs=n, uniform_loc=True)

    four_l = 4 * grid_size  # chi-hat protocol horizon (index four_l - 1)
    m_center = center["mass"].mean(axis=0)  # m(u), u = 1..HORIZON
    m_unif = unif["mass"].mean(axis=0)
    ns = ~center["spanned"]
    chi_cond = float(center["mass"][ns, four_l - 1].mean())
    # Age-average with m(0) = 1: ages are uniform over {0..HORIZON-1}.
    pred_slope = float((1.0 + m_unif[: HORIZON - 1].sum()) / HORIZON)
    return {
        "grid_size": grid_size,
        "n_runs": n,
        "horizon": HORIZON,
        "chi_protocol_t": four_l,
        "n_nonspanning_center": int(ns.sum()),
        "chi_cond_center_4L": chi_cond,
        "m_center_uncond_4L": float(m_center[four_l - 1]),
        "m_unif_uncond_4L": float(m_unif[four_l - 1]),
        "m_unif_uncond_final": float(m_unif[-1]),
        "predicted_sweep_slope": pred_slope,
        "m_unif_trajectory_sample": {
            str(u): float(m_unif[u - 1])
            for u in (16, 32, 64, 128, 192, 256)
            if u <= HORIZON
        },
    }


def main() -> None:
    out_dir = Path("che/bench/results/phase3/m33")
    out_dir.mkdir(parents=True, exist_ok=True)
    key = jax.random.PRNGKey(11)
    t0 = time.perf_counter()
    result = {
        "beta": BETA_LOW,
        "blocks": [decompose(gs, jax.random.fold_in(key, gs)) for gs in (32, 64)],
        "jax_version": jax.__version__,
        "backend": jax.default_backend(),
        "wall_seconds": None,
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    result["wall_seconds"] = time.perf_counter() - t0
    path = out_dir / "deficit_decomposition.json"
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
