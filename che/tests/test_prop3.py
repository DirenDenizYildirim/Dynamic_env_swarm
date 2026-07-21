"""M3.3 ★ Prop.-3 quantitative test ★ (theory §10 hook), CPU scale.

E[B_T] = chi(beta) * E[N_seeds] in the sparse-seeding regime (Prop. 3):
sweep lambda_0 at L = 32, beta = 0.43 (Low), iota = 0, no primary ignition
— collapse is the only birth channel — and compare the through-origin
least-squares slope of E[B_T] vs E[N_seeds] against chi-hat(0.43)
**recomputed at L = 32 inside this test** with the Phase-2 estimator
(never compare chi-hat across grid sizes; the phase-2 reference for the
full-scale GPU sweep is the size-matched L = 64 value).

Acceptance (pre-agreed, phase prompt): slope ∈ [0.75, 1.05] * chi_hat and
through-origin R² >= 0.99. The band is asymmetric-aware: cluster overlap
and boundary truncation only *reduce* the slope; the upside allowance
covers MC error and the chi-hat estimator's non-spanning conditioning
(at L = 32, beta = 0.43 about 18% of single-seed runs span and are
excluded from chi-hat, so the sweep — which keeps every run — can sit
slightly above it).
"""

import jax
import jax.numpy as jnp
import numpy as np
import pytest

from che.calibration.estimates import chi_hat
from che.calibration.percolation import run_ensemble
from che.calibration.prop3 import (
    BETA_LOW,
    LAMBDAS_L32,
    fit_slope_through_origin,
    run_prop3_ensemble,
    summarize,
)

pytestmark = pytest.mark.slow

L = 32
# MC sizes: the phase prompt sets a >= 512 floor per lambda; these are
# raised above it because at N = 512 the chi-hat reference alone moves by
# ~±10% between key seeds (measured: 32.8 / 38.2 around a converged ~34.9)
# — noise larger than the acceptance band. Precision increase, not a
# tolerance change: the [0.75, 1.05] band is untouched.
SWEEP_MC = 1024  # runs per lambda value
CHI_MC = 8192  # single-seed runs for the chi-hat reference (cheap: T=4L)


@pytest.fixture(scope="module")
def sweep() -> dict:
    out = run_prop3_ensemble(
        jax.random.PRNGKey(0),
        jnp.asarray(LAMBDAS_L32, dtype=jnp.float32),
        grid_size=L,
        n_seeds_mc=SWEEP_MC,
    )
    return {k: np.asarray(v) for k, v in out.items()}


@pytest.fixture(scope="module")
def chi_ref() -> float:
    """chi-hat(0.43) at L = 32, Phase-2 estimator on fresh single-center-
    ignition runs (percolation_run protocol, T_max = 4L), CPU scale."""
    out = run_ensemble(
        jax.random.PRNGKey(7),
        jnp.asarray([BETA_LOW], dtype=jnp.float32),
        grid_size=L,
        n_seeds=CHI_MC,
        t_max=4 * L,
    )
    chi, n_ns = chi_hat(
        np.asarray(out["burnt_fraction"]), np.asarray(out["spanned"]), L
    )
    assert n_ns[0] > 0.5 * CHI_MC  # subcritical sanity: most runs don't span
    return float(chi[0])


def test_collapse_is_the_only_birth_channel(sweep):
    """iota = 0 and no primary ignition: a run with zero realized seeds
    must end with zero burnt area, at every lambda_0."""
    no_seeds = sweep["n_seeds"] == 0
    assert no_seeds.any()  # the sparsest lambda produces such runs
    assert (sweep["b_t"][no_seeds] == 0).all()
    # And fire happens at all (the sweep is not vacuous).
    assert (sweep["b_t"] > 0).any()


def test_seeding_scales_with_lambda(sweep):
    """E[N_collapses] and E[N_seeds] increase along the sweep (reservoir
    barely depletes at these lambdas, so the growth is near-linear)."""
    e_coll = sweep["n_collapses"].mean(axis=1)
    e_seeds = sweep["n_seeds"].mean(axis=1)
    assert (np.diff(e_coll) > 0).all()
    assert (np.diff(e_seeds) > 0).all()


def test_prop3_slope_matches_chi_hat(sweep, chi_ref):
    """The theory<->implementation handshake: through-origin slope of
    E[B_T] vs E[N_seeds] within [0.75, 1.05] * chi_hat, R² >= 0.99."""
    s = summarize(sweep, np.asarray(LAMBDAS_L32))
    slope, r2 = fit_slope_through_origin(
        np.asarray(s["e_n_seeds"]), np.asarray(s["e_b_t"])
    )
    ratio = slope / chi_ref
    # Disjointness diagnostic (reported, never a criterion).
    print(
        f"\nProp.-3 L={L}: slope={slope:.2f}, chi_hat={chi_ref:.2f}, "
        f"ratio={ratio:.3f}, R2={r2:.4f}, "
        f"overlap_frac={[round(v, 3) for v in s['overlap_seed_fraction']]}"
    )
    assert 0.75 <= ratio <= 1.05, (slope, chi_ref, ratio)
    assert r2 >= 0.99, r2
