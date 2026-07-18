"""Invariant #1 (Def. 2): reward reads task variables only.

Two states differing ONLY in hazard/smoke/structure must yield bitwise
identical rewards under the same key and actions. Do not weaken this test.

Phase-1 form (per this file's original Phase-1 note and the pre-approved
M1.1 plan): the hazard now disables agents, so kernel-mediated reward
differences are legitimate per Def. 2. The test therefore *pins the alpha
transition equal* instead of loosening anything: all hazard/structure
differences are confined to cells Chebyshev-far (>= 6) from every agent, so
x'/alive' evolve identically across variants and any reward difference
would be a Def.-2 violation (reward reading h/rho/c directly). Smoke may
still differ everywhere — it cannot touch agents until Coupling B. Also
covers death_penalty > 0 (M1.1): identical alpha transitions must still
yield identical rewards.
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

# All agents live in the low-index corner; differences live in the far
# corner. Chebyshev margin >= 6 > 1 (move) + 1 (CA spread) + r_seed keeps
# the alpha transition provably identical across variants for one step.
AGENT_POS = jnp.array([[2, 2], [3, 2], [2, 3], [4, 4]], dtype=jnp.int32)


def _far(ll: int) -> jax.Array:
    """Mask of the far corner: rows and cols >= 10 (distance >= 6)."""
    rows, cols = jnp.indices((ll, ll))
    return (rows >= 10) & (cols >= 10)


def hazard_variants(state):
    """The base state plus copies differing only in h, rho, or c — far away."""
    ll = CFG.grid_size
    far = _far(ll)
    checker = (jnp.indices((ll, ll)).sum(0) % 2).astype(jnp.uint8)
    far_checker_burning = jnp.where(
        far, checker * BURNING, state.hazard
    ).astype(jnp.uint8)
    far_burnt = jnp.where(far, BURNT, state.hazard).astype(jnp.uint8)
    far_collapsed = jnp.where(
        far, checker * COLLAPSED, state.structure
    ).astype(jnp.uint8)
    yield state
    yield dataclasses.replace(state, hazard=far_checker_burning)
    yield dataclasses.replace(state, hazard=far_burnt)
    yield dataclasses.replace(state, smoke=jnp.ones_like(state.smoke) * 3.5)
    yield dataclasses.replace(state, structure=far_collapsed)
    yield dataclasses.replace(
        state,
        hazard=far_burnt,
        smoke=jnp.ones_like(state.smoke) * 0.7,
        structure=far_collapsed,
    )


def _run(theta: ThetaConfig):
    cfg = dataclasses.replace(CFG, theta=theta)
    step_j = jax.jit(step, static_argnames="cfg")
    for seed in range(3):
        key = jax.random.PRNGKey(seed)
        _, base = reset(key, cfg)
        base = dataclasses.replace(base, agent_pos=AGENT_POS)
        k_step, k_act = jax.random.split(jax.random.PRNGKey(100 + seed))
        actions = jax.random.randint(k_act, (cfg.n_agents,), 0, 5)
        results = [
            step_j(k_step, s, actions, cfg) for s in hazard_variants(base)
        ]
        rewards = [float(r[2]) for r in results]
        assert all(r == rewards[0] for r in rewards), rewards
        # The alpha transition and task state must evolve identically too
        # (this is what makes the reward comparison meaningful post-M1.1).
        states = [r[1] for r in results]
        for s in states[1:]:
            assert (s.agent_pos == states[0].agent_pos).all()
            assert (s.agent_alive == states[0].agent_alive).all()
            assert (s.food == states[0].food).all()


def test_reward_identical_across_hazard_smoke_structure():
    _run(HOT_THETA)


def test_reward_identical_with_death_penalty():
    """M1.1: death_penalty reads only the alpha transition — with identical
    alive vectors (pinned by the far-field construction), states differing
    only in hazard/smoke/structure must still yield identical reward."""
    _run(dataclasses.replace(HOT_THETA, death_penalty=0.5))
