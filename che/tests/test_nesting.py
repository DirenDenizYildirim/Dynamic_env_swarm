"""CLAUDE.md invariant #3: bitwise ablation nesting.

Switching one subsystem's parameters may not perturb any *other*
subsystem's PRNG stream, because every stochastic branch consumes its
stream unconditionally. Phase-1 note (M1.1): T_X now legitimately reads h'
and c' (lethality/blocking), so structure activity *may* change agent and
food trajectories through the kernel, and fire deaths *may* change
structure through the load term — those are Def.-1 dependencies, not
stream perturbations. The bitwise assertions below pin exactly the
channels that must remain closed:

1. With kappa_A = 0, structure activity must leave the hazard and smoke
   trajectories bitwise identical (structure -> hazard only via Coupling A).
2. With no collapses possible (lambda_0 = lambda_load = 0), kappa_A's value
   is immaterial bitwise, on every field.
3. With lambda_load = 0 (the only x -> c channel closed), beta must not
   perturb the structure trajectory, even as fire kills agents.
4. death_penalty is reward-only: it may not perturb any state trajectory.
5. Death logic consumes no PRNG: a hand-built field-only replay of the same
   key schedule reproduces hazard/smoke/structure bitwise while agents die.
"""

import dataclasses

import jax
import jax.numpy as jnp

from che.env.config import EnvConfig, ThetaConfig
from che.env.env import reset, step
from che.env.hazard import hazard_step, seed_ignitions, smoke_step
from che.env.structure import coupling_a_seed_mask, structure_step
from che.env.types import COLLAPSED, INTACT

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
        _, state, reward, _, _ = step(k_step, state, actions, cfg)
        return (key, state), (
            state.hazard,
            state.smoke,
            state.structure,
            state.food,
            state.agent_pos,
            state.agent_alive,
            reward,
        )

    _, out = jax.lax.scan(body, (key, state), None, length=N_STEPS)
    names = ("hazard", "smoke", "structure", "food", "pos", "alive", "reward")
    return dict(zip(names, out, strict=True))


def _assert_bitwise_equal(a, b, fields):
    for f in fields:
        assert (a[f] == b[f]).all(), f"{f} trajectory perturbed — invariant #3"


def test_structure_activity_cannot_perturb_hazard_stream():
    base = ThetaConfig(beta=0.5, kappa_A=0.0, lambda_0=0.0)
    active = dataclasses.replace(base, lambda_0=0.05, lambda_load=0.1)
    a, b = _traj(base), _traj(active)
    # Structure itself differs (sanity that the knob is live)...
    assert (a["structure"] != b["structure"]).any()
    # ...but with kappa_A = 0 the hazard/smoke streams may not move a bit.
    # (pos/food/alive legitimately differ: T_X reads c' since M1.1.)
    _assert_bitwise_equal(a, b, ("hazard", "smoke"))


def test_kappa_a_immaterial_without_collapses():
    base = ThetaConfig(beta=0.5, kappa_A=0.0, lambda_0=0.0, lambda_load=0.0)
    hot = dataclasses.replace(base, kappa_A=0.9)
    a, b = _traj(base), _traj(hot)
    _assert_bitwise_equal(
        a, b, ("hazard", "smoke", "structure", "food", "pos", "alive")
    )


def test_beta_cannot_perturb_structure_without_load_channel():
    # lambda_load = 0 closes the legitimate fire -> deaths -> load -> c
    # path; what remains must be bitwise invariant to beta.
    lo = ThetaConfig(beta=0.1, lambda_0=0.05, lambda_load=0.0)
    hi = dataclasses.replace(lo, beta=0.9)
    a, b = _traj(lo), _traj(hi)
    assert (a["hazard"] != b["hazard"]).any()  # knob is live
    _assert_bitwise_equal(a, b, ("structure",))


def test_death_penalty_is_reward_only():
    base = ThetaConfig(beta=0.8, iota=0.02, death_penalty=0.0)
    pen = dataclasses.replace(base, death_penalty=0.7)
    a, b = _traj(base), _traj(pen)
    _assert_bitwise_equal(
        a, b, ("hazard", "smoke", "structure", "food", "pos", "alive")
    )
    assert not a["alive"][-1].all()  # deaths actually occurred...
    assert (a["reward"] != b["reward"]).any()  # ...and only rewards moved.


def test_death_logic_consumes_no_prng():
    """M1.1 nesting extension: same-key field-only replay.

    Re-run the (structure, hazard, smoke) kernels outside the env with the
    exact key schedule `step` uses; the env's field trajectories must match
    bitwise even though agents are dying inside the env. lambda_load = 0
    keeps T_C independent of occupancy, so the replay needs no agents.
    """
    theta = ThetaConfig(
        beta=0.7, iota=0.02, kappa_A=0.5, lambda_0=0.03, lambda_load=0.0
    )
    cfg = EnvConfig(grid_size=16, n_agents=4, horizon=64, theta=theta)
    seed = 3
    env = _traj(theta, seed=seed)

    key = jax.random.PRNGKey(seed)
    key, k_reset = jax.random.split(key)
    _, state0 = reset(k_reset, cfg)
    zero_load = jnp.zeros((cfg.grid_size, cfg.grid_size), jnp.float32)

    def body(carry, _):
        key, hazard, smoke, structure = carry
        key, _k_act, k_step = jax.random.split(key, 3)  # k_act discarded
        k_struct, k_seed, k_fire = jax.random.split(k_step, 3)
        structure_new = structure_step(
            k_struct,
            structure,
            zero_load,
            lambda_0=theta.lambda_0,
            lambda_load=theta.lambda_load,
        )
        inc = (structure_new == COLLAPSED) & (structure == INTACT)
        mask = coupling_a_seed_mask(
            k_seed, inc, kappa_A=theta.kappa_A, r_seed=theta.r_seed
        )
        hazard_new = seed_ignitions(
            hazard_step(k_fire, hazard, beta=theta.beta, iota=theta.iota), mask
        )
        smoke_new = smoke_step(
            smoke, hazard_new, sigma_s=theta.sigma_s, eta=theta.eta
        )
        return (key, hazard_new, smoke_new, structure_new), (
            hazard_new,
            smoke_new,
            structure_new,
        )

    _, (hz, sm, st) = jax.lax.scan(
        body,
        (key, state0.hazard, state0.smoke, state0.structure),
        None,
        length=N_STEPS,
    )
    assert not env["alive"][-1].all()  # the env run had real deaths
    assert (env["hazard"] == hz).all()
    assert (env["smoke"] == sm).all()
    assert (env["structure"] == st).all()
