"""Invariant #1 (Def. 2): reward reads task variables only.

Two states differing ONLY in hazard/smoke/structure must yield bitwise
identical rewards under the same key and actions. Do not weaken this test.
(Phase-1 note: when hazard begins disabling agents, kernel-mediated reward
differences become legitimate per Def. 2; this test must then pin x' equal
across variants rather than be loosened — consult the human first.)
"""

import dataclasses

import jax
import jax.numpy as jnp

from che.env.config import EnvConfig, ThetaConfig
from che.env.env import reset, step
from che.env.types import BURNING, BURNT, COLLAPSED

# A deliberately "hot" theta: active fire, spontaneous ignition, collapses,
# and Coupling A all on — reward must be blind to every one of them.
HOT_THETA = ThetaConfig(
    beta=0.6, kappa_A=0.5, iota=0.02, lambda_0=0.05, lambda_load=0.1
)
CFG = EnvConfig(grid_size=16, n_agents=4, horizon=64, theta=HOT_THETA)


def hazard_variants(state):
    """The base state plus copies differing only in h, rho, or c."""
    ll = CFG.grid_size
    checker = (jnp.indices((ll, ll)).sum(0) % 2).astype(jnp.uint8)
    yield state
    yield dataclasses.replace(state, hazard=checker * BURNING)
    yield dataclasses.replace(state, hazard=jnp.full_like(state.hazard, BURNT))
    yield dataclasses.replace(state, smoke=jnp.ones_like(state.smoke) * 3.5)
    yield dataclasses.replace(state, structure=checker * COLLAPSED)
    yield dataclasses.replace(
        state,
        hazard=(1 - checker) * BURNING,
        smoke=jnp.ones_like(state.smoke) * 0.7,
        structure=checker * COLLAPSED,
    )


def test_reward_identical_across_hazard_smoke_structure():
    step_j = jax.jit(step, static_argnames="cfg")
    for seed in range(3):
        key = jax.random.PRNGKey(seed)
        _, base = reset(key, CFG)
        k_step, k_act = jax.random.split(jax.random.PRNGKey(100 + seed))
        actions = jax.random.randint(k_act, (CFG.n_agents,), 0, 5)
        results = [
            step_j(k_step, s, actions, CFG) for s in hazard_variants(base)
        ]
        rewards = [float(r[2]) for r in results]
        assert all(r == rewards[0] for r in rewards), rewards
        # The task state must evolve identically too.
        foods = [r[1].food for r in results]
        assert all((f == foods[0]).all() for f in foods)
