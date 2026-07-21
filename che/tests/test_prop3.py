"""M3.3 ★ Prop.-3 quantitative test ★ v2 (theory §10 hook), CPU scale.

v2 per the human M3.3 ruling (2026-07-21; decision_log.md): test v1
compared protocol-mismatched quantities — the sweep slope (uniform seed
locations, uniform birth times, unconditional mass) against the Phase-2
chi-hat estimator (center seed, non-spanning-conditioned) — and passed at
L = 32 only through a cancellation of the two protocols' opposite biases
(RA spec error, logged; full accounting in phase3_report.md M3.3).

v2 computes its reference *matched to the sweep's protocol* internally
(`matched_reference`: single-seed rollouts at this test's own L, uniform
seed locations, uniform birth times via age-averaging, unconditional
mass) and runs the sweep in a purified sparse regime:

- kappa_A = KAPPA_A_PURE = 0.003: P(>=2 seeds | >=1 seed) = 1.3% <= 2%
  (ruling criterion 1);
- LAMBDAS_L32_PURE: top burnt density ~2.2%, so the birth-adjacency
  overlap proxy stays <= 3% (ruling criterion 2; asserted below as a
  regime check, not an acceptance criterion).

Acceptance (human-locked): slope/matched_ref ∈ [0.90, 1.02], R² >= 0.99.

Known residual biases inside the band (measured in the M3.3 pilot):
sibling seeds ~-1.2%, cross-cluster overlap ~-1%, and a +~2% seed-
location edge effect (the 3x3 dilation underweights border cells, whose
clusters are clipped, relative to the exactly-uniform reference) — net
ratio ~1.00. MC sizes below put the combined MC error at ~2.4%
(through-origin slope ~2.2% at SWEEP_MC = 8192, reference ~1.1% at
MATCHED_MC = 16384); with the pinned PRNG keys the outcome is
deterministic. Wall time ~15-20 min on CPU (niced) — this is the
quantitative theory<->implementation handshake, priced accordingly.
"""

import jax
import jax.numpy as jnp
import numpy as np
import pytest

from che.calibration.prop3 import (
    KAPPA_A_PURE,
    LAMBDAS_L32_PURE,
    fit_slope_through_origin,
    matched_reference,
    run_prop3_ensemble,
    summarize,
)

pytestmark = pytest.mark.slow

L = 32
SWEEP_MC = 8192  # runs per lambda value (>= the 512 phase-prompt floor)
MATCHED_MC = 16384  # single-seed runs for the matched reference


@pytest.fixture(scope="module")
def sweep() -> dict:
    out = run_prop3_ensemble(
        jax.random.PRNGKey(0),
        jnp.asarray(LAMBDAS_L32_PURE, dtype=jnp.float32),
        grid_size=L,
        n_seeds_mc=SWEEP_MC,
        kappa_A=KAPPA_A_PURE,
    )
    return {k: np.asarray(v) for k, v in out.items()}


@pytest.fixture(scope="module")
def matched() -> dict:
    """The sweep-matched per-seed mass reference at this test's own L:
    uniform location, uniform birth time (age-average), unconditional."""
    return matched_reference(jax.random.PRNGKey(7), grid_size=L, n_runs=MATCHED_MC)


def test_collapse_is_the_only_birth_channel(sweep):
    """iota = 0 and no primary ignition: a run with zero realized seeds
    must end with zero burnt area, at every lambda_0."""
    no_seeds = sweep["n_seeds"] == 0
    assert no_seeds.any()  # the sparse regime produces such runs
    assert (sweep["b_t"][no_seeds] == 0).all()
    # And fire happens at all (the sweep is not vacuous).
    assert (sweep["b_t"] > 0).any()


def test_seeding_scales_with_lambda(sweep):
    """E[N_collapses] and E[N_seeds] increase along the sweep (the weak
    reservoir depletes ~5% at the top lambda, so growth stays monotone)."""
    e_coll = sweep["n_collapses"].mean(axis=1)
    e_seeds = sweep["n_seeds"].mean(axis=1)
    assert (np.diff(e_coll) > 0).all()
    assert (np.diff(e_seeds) > 0).all()


def test_purified_regime(sweep):
    """Regime check (ruling): birth-adjacency overlap proxy <= 3% at
    every lambda. A violation invalidates the sweep, it does not fail
    Prop. 3 — hence a separate test from the acceptance ratio."""
    s = summarize(sweep, np.asarray(LAMBDAS_L32_PURE))
    assert max(s["overlap_seed_fraction"]) <= 0.03, s["overlap_seed_fraction"]


def test_prop3_slope_matches_matched_reference(sweep, matched):
    """The theory<->implementation handshake, v2: through-origin slope
    of E[B_T] vs E[N_seeds] within [0.90, 1.02] of the protocol-matched
    reference (human-locked band), R² >= 0.99."""
    s = summarize(sweep, np.asarray(LAMBDAS_L32_PURE))
    slope, r2 = fit_slope_through_origin(
        np.asarray(s["e_n_seeds"]), np.asarray(s["e_b_t"])
    )
    ref = matched["matched_ref"]
    ratio = slope / ref
    print(
        f"\nProp.-3 v2 L={L}: slope={slope:.2f}, "
        f"matched_ref={ref:.2f} (SE {matched['se']:.2f}), "
        f"ratio={ratio:.3f}, R2={r2:.4f}, "
        f"overlap_frac={[round(v, 3) for v in s['overlap_seed_fraction']]}"
    )
    assert 0.90 <= ratio <= 1.02, (slope, ref, ratio)
    assert r2 >= 0.99, r2
