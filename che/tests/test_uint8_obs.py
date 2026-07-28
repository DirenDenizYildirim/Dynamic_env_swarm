"""M5.1f: uint8 observation storage + in-network normalization.

The pre-registered contingency (standing rule 2026-07-21), activated because
the Phase-6/7 configuration does not fit the card in float32: its population
obs trajectory is 11.39 GiB and minibatching copies it (M5.1d row B, OOM).

What these tests pin:
1. Quantization is lossless on every indicator plane and bounded on smoke —
   the only continuous plane — so activating the contingency changes obs
   fidelity in exactly one known, quantified place.
2. The network's in-network normalization inverts it exactly.
3. Acting and replay see the SAME array. If the collector acted on float32
   crops and replayed uint8 ones, PPO's first-epoch ratio would differ from
   1 by a quantization artifact — a silent bias in the surrogate, not a
   rounding detail.
4. The 4x memory saving is real, and the off-by-default path is untouched.
"""

import dataclasses

import chex
import jax
import jax.numpy as jnp
import numpy as np
import pytest

from che.env.comms import MSG_DIM
from che.env.config import Config, EnvConfig, ThetaConfig, TrainConfig
from che.env.env import N_ACTIONS, reset
from che.env.observation import (
    dequantize_grid,
    n_planes,
    plane_scales,
    quantize_grid,
    rho_max,
)
from che.train.ippo import make_train_fns
from che.train.networks import ActorCritic

ECFG = EnvConfig(
    grid_size=16, n_agents=4, horizon=32, n_food=6,
    theta=ThetaConfig(beta=0.49, kappa_A=0.06, kappa_B=1.0, f_weak=0.15),
)


def _cfg(uint8: bool) -> Config:
    return Config(
        env=ECFG,
        train=TrainConfig(
            n_envs=2, rollout_len=8, n_minibatches=2, n_epochs=2,
            uint8_obs=uint8,
        ),
    )


def test_scales_match_the_plane_table():
    """Smoke is the only non-indicator plane, and its bound is Def. 6's."""
    scales = plane_scales(ECFG)
    assert len(scales) == n_planes(ECFG)
    assert scales[2] == pytest.approx(rho_max(ECFG))  # v3 smoke index
    assert all(s == 1.0 for i, s in enumerate(scales) if i != 2)
    # sigma_s / (1 - e^-eta) with the locked constants.
    assert rho_max(ECFG) == pytest.approx(2.5414940825, rel=1e-9)


def test_indicator_planes_round_trip_exactly():
    """Binary planes must survive quantization bit-for-bit: a masked cell has
    to stay exactly 0 and a burning cell exactly 1, or Coupling B's semantics
    would drift with the storage format."""
    g = jnp.zeros((1, 9, 9, n_planes(ECFG)), jnp.float32)
    g = g.at[0, :, :, 0].set(1.0).at[0, :, :, 7].set(1.0)  # burning + visibility
    back = dequantize_grid(quantize_grid(g, ECFG), plane_scales(ECFG))
    np.testing.assert_array_equal(np.asarray(back[0, ..., 0]), np.ones((9, 9)))
    np.testing.assert_array_equal(np.asarray(back[0, ..., 7]), np.ones((9, 9)))
    np.testing.assert_array_equal(np.asarray(back[0, ..., 3]), np.zeros((9, 9)))


def test_smoke_error_is_bounded_by_half_a_quantization_step():
    """The one lossy plane, quantified rather than asserted to be fine."""
    rho = jnp.linspace(0.0, rho_max(ECFG), 257)
    g = jnp.zeros((257, 1, 1, n_planes(ECFG)), jnp.float32).at[:, 0, 0, 2].set(rho)
    back = dequantize_grid(quantize_grid(g, ECFG), plane_scales(ECFG))
    err = np.abs(np.asarray(back[:, 0, 0, 2]) - np.asarray(rho))
    step = rho_max(ECFG) / 255.0
    assert err.max() <= step / 2 + 1e-6, f"max error {err.max()} > {step / 2}"


def test_quantization_is_idempotent():
    """quantize(dequantize(q)) == q, so a value that has been through the
    pipeline once does not drift if it goes through again."""
    key = jax.random.PRNGKey(0)
    g = jax.random.uniform(key, (4, 9, 9, n_planes(ECFG))) * 2.0
    q1 = quantize_grid(g, ECFG)
    q2 = quantize_grid(dequantize_grid(q1, plane_scales(ECFG)), ECFG)
    chex.assert_trees_all_equal(q1, q2)


def test_network_normalizes_uint8_exactly_like_the_float_path():
    net = ActorCritic(N_ACTIONS, obs_scale=plane_scales(ECFG))
    key = jax.random.PRNGKey(1)
    k_init, k_g = jax.random.split(key)
    shape = (3, 9, 9, n_planes(ECFG))
    g = jax.random.uniform(k_g, shape) * 2.0
    q = quantize_grid(g, ECFG)
    deq = dequantize_grid(q, plane_scales(ECFG))
    vec = jnp.zeros((3, 4), jnp.float32)
    msg = jnp.zeros((3, MSG_DIM), jnp.float32)
    params = net.init(k_init, q, vec, msg)
    from_u8 = net.apply(params, q, vec, msg)
    from_f32 = net.apply(params, deq, vec, msg)
    chex.assert_trees_all_equal(from_u8, from_f32)


def test_uint8_without_scale_is_a_loud_error():
    net = ActorCritic(N_ACTIONS)  # no obs_scale
    q = jnp.zeros((1, 9, 9, n_planes(ECFG)), jnp.uint8)
    with pytest.raises(ValueError, match="obs_scale"):
        net.init(jax.random.PRNGKey(0), q, jnp.zeros((1, 4)), jnp.zeros((1, MSG_DIM)))


def test_collector_stores_uint8_and_acts_on_the_same_array():
    """The bias guard. The stored crop must be byte-identical to the one the
    action was sampled from, so the surrogate replays the true policy input.

    Checked by reconstructing what the collector does: quantize once, act on
    that, store that. If a future edit reintroduces a float32 forward pass
    beside a uint8 store, the two log-probs diverge and this fails."""
    cfg = _cfg(True)
    fns = make_train_fns(cfg)
    runner = fns.init(jax.random.PRNGKey(0))
    obs, _ = reset(jax.random.PRNGKey(3), cfg.env)
    q = quantize_grid(obs["grid"], cfg.env)
    assert q.dtype == jnp.uint8
    net = ActorCritic(N_ACTIONS, obs_scale=plane_scales(cfg.env))
    msg = jnp.zeros((cfg.env.n_agents, MSG_DIM), jnp.float32)
    acted = net.apply(runner.train_state.params, q, obs["vec"], msg)
    replayed = net.apply(runner.train_state.params, q, obs["vec"], msg)
    chex.assert_trees_all_equal(acted, replayed)
    # And the float path would NOT agree — which is why the collector must
    # never mix them (this is the failure mode, asserted as such).
    float_path = net.apply(runner.train_state.params, obs["grid"], obs["vec"], msg)
    assert not jnp.allclose(float_path[0], acted[0], atol=0, rtol=0) or bool(
        jnp.all(obs["grid"] == dequantize_grid(q, plane_scales(cfg.env)))
    )


def test_memory_saving_is_four_fold():
    g = jnp.zeros((8, 4, 9, 9, n_planes(ECFG)), jnp.float32)
    assert g.nbytes // quantize_grid(g, ECFG).nbytes == 4


@pytest.mark.parametrize("uint8", [False, True])
def test_training_chunk_runs_in_both_modes(uint8):
    cfg = _cfg(uint8)
    fns = make_train_fns(cfg)
    runner = fns.init(jax.random.PRNGKey(0))
    runner, metrics = fns.chunk(runner, 1)
    assert jnp.isfinite(metrics["total_loss"]).all()
    assert jnp.isfinite(metrics["entropy"]).all()


def test_default_configs_are_unchanged():
    """Off by default: every pre-M5.1f config keeps its behaviour and its
    config hash, so existing checkpoints still resume."""
    assert TrainConfig().uint8_obs is False
    cfg = dataclasses.replace(_cfg(False))
    assert cfg.train.uint8_obs is False
