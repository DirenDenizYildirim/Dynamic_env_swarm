"""M3.3 Prop.-3 quantitative test engine (theory §10 hook).

Hazard+structure-only rollouts in the "collapse is the only birth channel"
regime of Prop. 3: subcritical Low severity beta = 0.43, iota = 0, **no
primary ignition** — every Burning cell descends from a Coupling A seed.
No agents exist, so lambda_load is inert and T_C reads a zero load grid.

Alignment with Prop. 3's hypotheses (each a DECISION, mirrored in the test):

- *"each collapse seeding one ignition"*: kappa_A is fixed small (default
  0.02, ~0.18 expected seeds per collapse over the 3x3 ball), so a collapse
  that seeds at all almost always seeds exactly once; the slope is measured
  against the *realized* E[N_seeds], which absorbs kappa_A exactly.
- *"uniformly located"*: weak_smooth = 0 — an iid (unclustered) weak mask,
  so collapse sites (hence seeds) are uniform over the arena. The clustered
  masks of training configs would correlate seed locations and inflate
  overlap beyond the proposition's regime.
- *"seeded clusters pairwise disjoint (sparse regime)"*: lambda_0 sweeps
  sparse -> moderate; the per-value overlap diagnostic below reports how
  far each point sits from disjointness. Overlap only merges clusters
  (removes double counting), so it biases the slope *down*, never up.

Per (lambda_0, seed) run measurements:

- ``b_t``: total non-Fuel cell count at the horizon (counts Burning like
  the chi-hat DECISION in calibration/percolation.py; with the subcritical
  beta and T = 256 >> extinction time, the counts coincide in practice).
- ``n_seeds``: realized Coupling-A ignition count (Fuel -> Burning flips
  from seeding, summed over the run) — the x-axis of Prop. 3.
- ``n_collapses``: realized collapse-increment total (reservoir depletion
  diagnostic; the weak-cell reservoir is finite and absorbing).
- ``n_overlap_seeds``: seeds born within Chebyshev distance 1 of an
  already-ignited cell or of another same-step seed — a *birth-adjacency*
  proxy for cluster overlap (an underestimate: clusters can also grow into
  each other later; reported per lambda_0, never a test criterion).

The kernels are the env's own (structure_step, coupling_a_seed_mask,
hazard_step, seed_ignitions), sampled in the Prop.-1 order exactly as
env.step composes them.

CLI (full-scale GPU sweep; the @slow CPU test imports run_prop3_ensemble):

    uv run python -m che.calibration.prop3            # L=64 defaults
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

from che.env.hazard import hazard_step, seed_ignitions
from che.env.structure import (
    coupling_a_seed_mask,
    dilate,
    generate_weak_mask,
    structure_step,
)
from che.env.types import COLLAPSED, FUEL, INTACT

BETA_LOW = 0.43  # Phase-2 locked Low severity (severity_lock.md)
KAPPA_A = 0.02  # DECISION: ~one seed per seeding collapse (module docstring)
R_SEED = 1  # config default N_A radius (3x3 ball)
F_WEAK = 0.4  # reservoir size; iid mask (weak_smooth = 0)
HORIZON = 256  # matches the training episode horizon (phase prompt)

# Default lambda_0 sweeps, sparse -> moderate: chosen so realized
# E[N_seeds] spans ~0.4..5 (L=32) / ~0.5..11 (L=64) and E[B_T] stays well
# below the arena (mean seeded-cluster mass << m, Prop. 3's regime).
LAMBDAS_L32 = (2e-5, 6e-5, 1.2e-4, 1.8e-4, 2.5e-4)
LAMBDAS_L64 = (1e-5, 3e-5, 6e-5, 1e-4, 1.5e-4)


def prop3_run(
    key: jax.Array,
    lambda_0: jax.Array,
    *,
    grid_size: int,
    horizon: int = HORIZON,
    beta: float = BETA_LOW,
    kappa_A: float = KAPPA_A,
    r_seed: int = R_SEED,
    f_weak: float = F_WEAK,
) -> dict[str, jax.Array]:
    """One no-agents run: all-Fuel hazard, no primary ignition, iid weak
    mask; per-step sampling mirrors env.step's Prop.-1 order (structure ->
    seed mask from the increment -> CA spread -> apply seeds). lambda_0 may
    be traced (vmapped); the rest is static."""
    k_weak, k_run = jax.random.split(key)
    weak = generate_weak_mask(k_weak, grid_size, f_weak=f_weak, n_smooth=0)
    hazard0 = jnp.full((grid_size, grid_size), FUEL, dtype=jnp.uint8)
    structure0 = jnp.full((grid_size, grid_size), INTACT, dtype=jnp.uint8)
    zero_load = jnp.zeros((grid_size, grid_size), dtype=jnp.float32)

    def neighbor_count(mask: jax.Array) -> jax.Array:
        """Number of True cells in each cell's 3x3 ball, excluding itself."""
        p = jnp.pad(mask.astype(jnp.int32), 1)
        total = sum(
            p[i : i + grid_size, j : j + grid_size]
            for i in (0, 1, 2)
            for j in (0, 1, 2)
        )
        return total - mask.astype(jnp.int32)

    def body(carry, key_t):
        hazard, structure, n_seeds, n_collapses, n_overlap = carry
        k_struct, k_seed, k_fire = jax.random.split(key_t, 3)
        structure_new = structure_step(
            k_struct, structure, weak, zero_load,
            lambda_0=lambda_0, lambda_load=0.0,
        )
        inc = (structure_new == COLLAPSED) & (structure == INTACT)
        mask = coupling_a_seed_mask(k_seed, inc, kappa_A=kappa_A, r_seed=r_seed)
        hazard_ca = hazard_step(k_fire, hazard, beta=beta, iota=0.0)
        hazard_new = seed_ignitions(hazard_ca, mask)
        seeded = hazard_ca != hazard_new  # realized Fuel -> Burning seeds
        # Birth-adjacency overlap proxy: seed touches pre-seed non-Fuel or
        # another seed placed this step (Chebyshev 1).
        near_ignited = dilate(hazard_ca != FUEL, 1)
        overlap = seeded & (near_ignited | (neighbor_count(seeded) > 0))
        return (
            hazard_new,
            structure_new,
            n_seeds + seeded.sum(dtype=jnp.int32),
            n_collapses + inc.sum(dtype=jnp.int32),
            n_overlap + overlap.sum(dtype=jnp.int32),
        ), None

    (hazard_f, _, n_seeds, n_collapses, n_overlap), _ = jax.lax.scan(
        body,
        (hazard0, structure0, jnp.int32(0), jnp.int32(0), jnp.int32(0)),
        jax.random.split(k_run, horizon),
    )
    return {
        "b_t": (hazard_f != FUEL).sum(dtype=jnp.int32),
        "n_seeds": n_seeds,
        "n_collapses": n_collapses,
        "n_overlap_seeds": n_overlap,
    }


def run_prop3_ensemble(
    key: jax.Array,
    lambdas: jax.Array,
    *,
    grid_size: int,
    n_seeds_mc: int,
    **run_kwargs,
) -> dict[str, jax.Array]:
    """vmap over (lambda_0, MC seed): leading shape [n_lambda, n_seeds_mc].

    The same MC keys are shared across lambda values (common random
    numbers, as in calibration/percolation.py)."""
    chex.assert_rank(lambdas, 1)
    mc_keys = jax.random.split(key, n_seeds_mc)
    run = functools.partial(prop3_run, grid_size=grid_size, **run_kwargs)
    batched = jax.vmap(jax.vmap(run, in_axes=(0, None)), in_axes=(None, 0))
    return jax.jit(batched)(mc_keys, lambdas)


def fit_slope_through_origin(
    e_seeds: np.ndarray, e_bt: np.ndarray
) -> tuple[float, float]:
    """(slope, R^2) of E[B_T] = slope * E[N_seeds] through the origin.

    DECISION: through-origin is the proposition's form — with iota = 0 and
    no primary ignition, zero seeds implies zero burnt area exactly. R^2 is
    computed against the mean of E[B_T] (the usual definition), so it still
    penalizes non-linearity across the sweep points.
    """
    x = np.asarray(e_seeds, np.float64)
    y = np.asarray(e_bt, np.float64)
    slope = float((x * y).sum() / (x * x).sum())
    ss_res = ((y - slope * x) ** 2).sum()
    ss_tot = ((y - y.mean()) ** 2).sum()
    return slope, float(1.0 - ss_res / ss_tot)


def summarize(
    out: dict[str, jax.Array], lambdas: np.ndarray
) -> dict:
    """Per-lambda means + the origin fit, as plain-python JSON-ables."""
    e_bt = np.asarray(out["b_t"]).mean(axis=1)
    e_seeds = np.asarray(out["n_seeds"]).mean(axis=1)
    se_bt = np.asarray(out["b_t"]).std(axis=1) / np.sqrt(
        out["b_t"].shape[1]
    )
    total_seeds = np.asarray(out["n_seeds"]).sum(axis=1)
    overlap_frac = np.where(
        total_seeds > 0,
        np.asarray(out["n_overlap_seeds"]).sum(axis=1)
        / np.maximum(total_seeds, 1),
        0.0,
    )
    slope, r2 = fit_slope_through_origin(e_seeds, e_bt)
    free = np.polyfit(e_seeds, e_bt, 1)  # sensitivity: free intercept
    return {
        "lambdas": [float(v) for v in lambdas],
        "e_n_seeds": e_seeds.tolist(),
        "e_b_t": e_bt.tolist(),
        "se_b_t": se_bt.tolist(),
        "e_n_collapses": np.asarray(out["n_collapses"])
        .mean(axis=1)
        .tolist(),
        "overlap_seed_fraction": overlap_frac.tolist(),
        "slope_through_origin": slope,
        "r2_through_origin": r2,
        "slope_free_intercept": float(free[0]),
        "intercept_free": float(free[1]),
    }


def _git_commit() -> str:
    try:
        return subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--grid-size", type=int, default=64)
    p.add_argument("--n-seeds", type=int, default=512, help="MC runs per lambda")
    p.add_argument(
        "--lambdas", type=float, nargs="+", default=None,
        help="lambda_0 sweep values (default: per-grid-size presets)",
    )
    p.add_argument(
        "--out-dir", type=Path,
        default=Path("che/bench/results/phase3/m33"),
    )
    args = p.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    lambdas = args.lambdas or list(
        {32: LAMBDAS_L32, 64: LAMBDAS_L64}.get(args.grid_size, LAMBDAS_L64)
    )
    lam = jnp.asarray(lambdas, dtype=jnp.float32)
    t0 = time.perf_counter()
    out = run_prop3_ensemble(
        jax.random.PRNGKey(args.seed), lam,
        grid_size=args.grid_size, n_seeds_mc=args.n_seeds,
    )
    jax.block_until_ready(out)
    wall = time.perf_counter() - t0
    summary = summarize(out, np.asarray(lambdas))

    # chi-hat reference from the Phase-2 estimates at this grid size.
    est_path = Path("che/bench/results/phase2/estimates.npz")
    chi_ref = None
    if est_path.exists():
        est = np.load(est_path)
        chi_key = f"chi_hat_L{args.grid_size}"
        if chi_key in est:
            i = int(np.argmin(np.abs(est["betas"] - BETA_LOW)))
            chi_ref = float(est[chi_key][i])
    summary.update({
        "grid_size": args.grid_size,
        "n_seeds_mc": args.n_seeds,
        "beta": BETA_LOW,
        "kappa_A": KAPPA_A,
        "r_seed": R_SEED,
        "f_weak": F_WEAK,
        "horizon": HORIZON,
        "chi_hat_ref": chi_ref,
        "slope_over_chi_hat": (
            summary["slope_through_origin"] / chi_ref if chi_ref else None
        ),
        "jax_version": jax.__version__,
        "backend": jax.default_backend(),
        "device": str(jax.devices()[0]),
        "git_commit": _git_commit(),
        "seed": args.seed,
        "wall_seconds": wall,
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    })

    np.savez_compressed(
        args.out_dir / f"prop3_L{args.grid_size}.npz",
        lambdas=np.asarray(lambdas, np.float64),
        **{k: np.asarray(v) for k, v in out.items()},
    )
    (args.out_dir / f"prop3_L{args.grid_size}.json").write_text(
        json.dumps(summary, indent=2) + "\n"
    )
    print(json.dumps(summary, indent=2))

    # Figure: E[B_T] vs E[N_seeds], origin fit vs the chi-hat line.
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(5.2, 4.0), constrained_layout=True)
    x = np.asarray(summary["e_n_seeds"])
    y = np.asarray(summary["e_b_t"])
    yerr = np.asarray(summary["se_b_t"])
    ax.errorbar(x, y, yerr=yerr, fmt="o", ms=5, capsize=3, label="sweep")
    xs = np.linspace(0.0, x.max() * 1.05, 50)
    ax.plot(
        xs, summary["slope_through_origin"] * xs, "-",
        label=f"fit slope {summary['slope_through_origin']:.1f} "
        f"(R²={summary['r2_through_origin']:.4f})",
    )
    if chi_ref:
        ax.plot(
            xs, chi_ref * xs, "--",
            label=f"χ̂({BETA_LOW}) = {chi_ref:.1f}",
        )
    ax.set_xlabel("E[N_seeds]")
    ax.set_ylabel("E[B_T] (cells)")
    ax.set_title(
        f"Prop. 3 linear scaling, L={args.grid_size}, "
        f"β={BETA_LOW}, {args.n_seeds} runs/point"
    )
    ax.legend(fontsize=8)
    fig.savefig(args.out_dir / f"prop3_L{args.grid_size}.png", dpi=150)
    print(f"wrote sweep npz/json/png to {args.out_dir}")


if __name__ == "__main__":
    main()
