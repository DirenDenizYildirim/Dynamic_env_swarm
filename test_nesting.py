"""CLAUDE.md invariant #3: bitwise ablation nesting.

Switching one subsystem's parameters may not perturb any *other*
subsystem's trajectory, because every stochastic branch consumes its PRNG
stream unconditionally. These tests pin the cross-subsystem consequences:

1. With kappa_A = 0, structure activity (lambda_0 > 0 vs = 0) must leave the
   hazard, smoke, food, and agent trajectories bitwise identical — the
   "no Coupling A" ablation is the nested model exactly.
2. With no collapses possible (lambda_0 = lambda_load = 0), kappa_A's value
   is immaterial bitwise.
3. Hazard transmissibility beta must not perturb the structure trajectory.
"""

import dataclasses

import jax
import jax.numpy as jnp

from che.env.config import EnvConfig, ThetaConfig
from che.env.env import reset, step

N_STEPS = 25


def _traj(theta: ThetaConfig, seed: int = 3):
    cfg = EnvConfig(grid_size=16, n_agents=4, horizon=64, theta=theta)
    key = jax.random.PRNGKey(seed)
    key, k_reset = jax.random.split(key)
    _, state = reset(k_reset, cfg)

    def body(carry, _):
        key, state = carry
        key, k_act, k_step = jax.random.split(key, 3)
        actions = jax.random.randint(k_act, (cfg.n_agents,), 0, 5, jnp.int32)
        _, state, _, _, _ = step(k_step, state, actions, cfg)
        return (key, state), (
            state.hazard,
            state.smoke,
            state.structure,
            state.food,
            state.agent_pos,
        )

    _, out = jax.lax.scan(body, (key, state), None, length=N_STEPS)
    return dict(zip(("hazard", "smoke", "structure", "food", "pos"), out))


def _assert_bitwise_equal(a, b, fields):
    for f in fields:
        assert (a[f] == b[f]).all(), f"{f} trajectory perturbed — invariant #3"


def test_structure_activity_cannot_perturb_other_subsystems():
    base = ThetaConfig(beta=0.5, kappa_A=0.0, lambda_0=0.0)
    active = dataclasses.replace(base, lambda_0=0.05, lambda_load=0.1)
    a, b = _traj(base), _traj(active)
    # Structure itself differs (sanity that the knob is live)...
    assert (a["structure"] != b["structure"]).any()
    # ...but with kappa_A = 0 nothing else may move by a single bit.
    _assert_bitwise_equal(a, b, ("hazard", "smoke", "food", "pos"))


def test_kappa_a_immaterial_without_collapses():
    base = ThetaConfig(beta=0.5, kappa_A=0.0, lambda_0=0.0, lambda_load=0.0)
    hot = dataclasses.replace(base, kappa_A=0.9)
    a, b = _traj(base), _traj(hot)
    _assert_bitwise_equal(a, b, ("hazard", "smoke", "structure", "food", "pos"))


def test_beta_cannot_perturb_structure():
    lo = ThetaConfig(beta=0.1, lambda_0=0.05, lambda_load=0.1)
    hi = dataclasses.replace(lo, beta=0.9)
    a, b = _traj(lo), _traj(hi)
    assert (a["hazard"] != b["hazard"]).any()  # knob is live
    _assert_bitwise_equal(a, b, ("structure", "food", "pos"))
