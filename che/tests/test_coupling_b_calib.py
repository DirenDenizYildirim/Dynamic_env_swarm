"""M4.3 tests: the Coupling-B calibration engine measures what it claims.

The M4.3 lock rests on three measured numbers, so each estimator is
pinned here:

1. `masked_frac` is computed as an expectation (mean of 1 - tau over
   crop cells) rather than by drawing reveals. That is only legitimate
   if it equals the expectation of the env's own `masked_frac` info
   channel — asserted against a paired reference rollout.
2. The detection ring must sit inside the quadrature-sampled regime
   (M4.2 Finding 1 / ruling item 2): if a single-cell source on the ring
   were unoccludable, detection would read ~1 at every kappa_B and the
   band would be meaningless.
3. The ring is the Euclidean distance-3 shell, not a Chebyshev square.
"""

import dataclasses

import jax
import jax.numpy as jnp
import numpy as np

from che.calibration.coupling_b import (
    DETECTION_DIST,
    DETECTION_HALFWIDTH,
    endpoint_sampled_fraction,
    episode_observables,
    ring_mask,
)
from che.env.config import EnvConfig, ThetaConfig
from che.env.env import N_ACTIONS, reset, step
from che.env.types import BURNING

KB = 1.0
CFG = EnvConfig(
    grid_size=32,
    n_agents=6,
    horizon=64,
    obs_window=9,
    obs_version=3,
    n_food=8,
    theta=ThetaConfig(beta=0.49, kappa_B=KB, sigma_s=1.0, eta=0.5),
)


def _reference_masked_frac(key: jax.Array, cfg: EnvConfig) -> tuple[float, float]:
    """Fire-active-step sum and count of the env's own masked_frac
    channel, over the *same* states `episode_observables` visits (same
    key structure, obs-blind random actions)."""
    k_reset, k_run = jax.random.split(key)
    _, state = reset(k_reset, cfg)

    @jax.jit
    def one(state, key_t):
        k_act, k_step = jax.random.split(key_t)
        actions = jax.random.randint(
            k_act, (cfg.n_agents,), 0, N_ACTIONS, dtype=jnp.int32
        )
        _, state_new, _, _, info = step(k_step, state, actions, cfg)
        fire = (state_new.hazard == BURNING).any()
        return state_new, jnp.where(fire, info["masked_frac"], 0.0), fire

    total, n_steps = 0.0, 0.0
    for key_t in jax.random.split(k_run, cfg.horizon):
        state, contrib, fire = one(state, key_t)
        total += float(contrib)
        n_steps += float(fire)
    return total, n_steps


def test_masked_frac_estimator_matches_env_channel():
    """Estimator vs the realized channel on identical states. The
    calibration integrates out the reveal draw, so it should agree to
    the channel's own Bernoulli noise — not exactly, but tightly."""
    keys = jax.random.split(jax.random.PRNGKey(0), 12)
    kap = jnp.asarray([KB], jnp.float32)
    est_num, est_den, ref_num, ref_den = 0.0, 0.0, 0.0, 0.0
    for k in keys:
        out = episode_observables(k, CFG, kap)
        est_num += float(out["masked_sum"][0])
        est_den += float(out["fire_steps"])
        num, den = _reference_masked_frac(k, CFG)
        ref_num += num
        ref_den += den
    assert est_den == ref_den > 0  # identical fire-active step counts
    est, ref = est_num / est_den, ref_num / ref_den
    # Per-step channel noise is a mean over n_agents * k^2 = 486 reveal
    # draws; pooled over these steps the agreement is far tighter than 5%.
    assert abs(est - ref) < 0.05 * max(ref, 1e-6), (est, ref)


def test_detection_ring_is_in_the_quadrature_sampled_regime():
    """M4.2 ruling item 2, made explicit rather than implicit: every
    distance-3 ring cell is occludable by a single-cell source at that
    cell. (At distance >= 5 this drops below 1 — Finding 1.)"""
    assert endpoint_sampled_fraction(9) == 1.0
    assert endpoint_sampled_fraction(17) == 1.0  # ring is k-independent


def test_ring_mask_is_the_euclidean_distance_3_shell():
    ring = np.asarray(ring_mask(9))
    r = 4
    for i in range(9):
        for j in range(9):
            d = float(np.hypot(i - r, j - r))
            assert bool(ring[i, j]) == (abs(d - DETECTION_DIST) < DETECTION_HALFWIDTH)
    assert ring[r + 3, r] == 1.0  # (3, 0): d = 3
    assert ring[r + 2, r + 2] == 1.0  # (2, 2): d = 2.83
    assert ring[r + 3, r + 2] == 0.0  # (3, 2): d = 3.61
    assert ring.sum() > 0


def test_masked_frac_ceiling_bounds_the_observable():
    """The ceiling is the sup over kappa_B: masked_frac at a huge kappa_B
    must approach it from below and never exceed it."""
    kap = jnp.asarray([0.5, 1000.0], jnp.float32)
    masked_sum, ceiling_sum, steps = np.zeros(2), 0.0, 0.0
    for k in jax.random.split(jax.random.PRNGKey(3), 8):
        out = episode_observables(k, CFG, kap)
        masked_sum += np.asarray(out["masked_sum"], np.float64)
        ceiling_sum += float(out["ceiling_sum"])
        steps += float(out["fire_steps"])
    assert steps > 0
    masked, ceiling = masked_sum / steps, ceiling_sum / steps
    assert ceiling > 0, "no agent ever had smoke in crop — vacuous test"
    assert masked[0] < masked[1] <= ceiling + 1e-6, (masked, ceiling)


def test_kappa_b_zero_masks_nothing():
    cfg0 = dataclasses.replace(
        CFG, theta=dataclasses.replace(CFG.theta, kappa_B=0.0)
    )
    out = episode_observables(
        jax.random.PRNGKey(1), cfg0, jnp.asarray([0.0], jnp.float32)
    )
    assert float(out["masked_sum"][0]) == 0.0
    assert float(out["det_num"][0]) == float(out["det_den"])  # tau == 1
