"""M1.3 tests: static-hazard control variant (the memorization control).

Frozen h is constant over the episode (Burning cells stay Burning — lethal,
smoke-emitting, never spreading); smoke still evolves to its steady state;
the burn-in is reproducible per key.
"""

import dataclasses

import jax
import jax.numpy as jnp

from che.env.config import EnvConfig, ThetaConfig
from che.env.env import reset, step
from che.env.types import BURNING

THETA = ThetaConfig(beta=0.6, sigma_s=1.0, eta=0.5)
# t_gen pinned to 8: at the horizon/2 default (32) a 16-cell arena has
# usually burned out entirely (front hits the boundary and dies), leaving
# nothing Burning to freeze — fine for the control protocol at 64², but
# these tests need live frozen fire. The default itself is asserted in
# test_default_t_gen_is_half_horizon.
CFG = EnvConfig(
    grid_size=16,
    n_agents=4,
    horizon=64,
    hazard_mode="frozen",
    t_gen=8,
    theta=THETA,
)
SEED = 0  # chosen so the burn-in leaves live Burning cells (asserted below)


def _rollout(cfg, seed, n_steps):
    key = jax.random.PRNGKey(seed)
    key, k_reset = jax.random.split(key)
    _, state0 = reset(k_reset, cfg)

    def body(carry, _):
        key, state = carry
        key, k_act, k_step = jax.random.split(key, 3)
        actions = jax.random.randint(k_act, (cfg.n_agents,), 0, 5, jnp.int32)
        _, state, _, _, _ = step(k_step, state, actions, cfg)
        return (key, state), (state.hazard, state.smoke)

    _, (hazards, smokes) = jax.lax.scan(body, (key, state0), None, length=n_steps)
    return state0, hazards, smokes


def test_frozen_hazard_constant_over_episode():
    state0, hazards, _ = _rollout(CFG, SEED, 40)
    assert bool((state0.hazard == BURNING).any())  # burn-in left live fire
    assert (hazards == state0.hazard[None]).all()  # h never changes


def test_default_t_gen_is_half_horizon():
    assert dataclasses.replace(CFG, t_gen=None).t_gen_resolved == CFG.horizon // 2
    assert CFG.t_gen_resolved == 8


def test_smoke_still_evolves_to_steady_state():
    # rho on a frozen Burning cell: rho_T = sigma_s (1 - e^{-eta T}) /
    # (1 - e^{-eta}) -> sigma_s / (1 - e^{-eta}); 0 elsewhere (no emission).
    th = CFG.theta
    state0, _, smokes = _rollout(CFG, SEED, 40)
    burning = state0.hazard == BURNING
    steady = th.sigma_s / (1.0 - jnp.exp(-th.eta))
    final = smokes[-1]
    assert jnp.abs(final[burning] - steady).max() < 1e-4
    assert (final[~burning] == 0.0).all()
    # And it *evolves*: early smoke is strictly below the steady state.
    assert smokes[0][burning].max() < steady - 1e-3


def test_burnin_reproducible_per_key():
    k = jax.random.PRNGKey(11)
    _, a = reset(k, CFG)
    _, b = reset(k, CFG)
    assert (a.hazard == b.hazard).all()
    _, c = reset(jax.random.PRNGKey(12), CFG)
    assert (a.hazard != c.hazard).any()


def test_dynamic_mode_unaffected_by_t_gen():
    # t_gen is a frozen-mode knob: dynamic resets ignore it entirely.
    dyn = EnvConfig(grid_size=16, n_agents=4, horizon=64, theta=THETA)
    dyn_t = dataclasses.replace(dyn, t_gen=13)
    k = jax.random.PRNGKey(2)
    _, a = reset(k, dyn)
    _, b = reset(k, dyn_t)
    for f in ("hazard", "food", "agent_pos", "structure", "smoke"):
        assert (getattr(a, f) == getattr(b, f)).all()
