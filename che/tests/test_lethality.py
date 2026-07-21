"""M1.1 tests: exact death semantics, blocking, collapse-kill, dead-agent
inertness. Unit tests hand-construct h'/c' around an agent and call the pure
`agent_step` (the phase prompt's construction); integration tests force the
same outcomes through the composed `step` with deterministic parameters
(beta = 1)."""

import dataclasses

import jax
import jax.numpy as jnp

from che.env.config import EnvConfig, ThetaConfig
from che.env.env import agent_step, reset, step
from che.env.types import (
    BURNING,
    BURNT,
    COLLAPSED,
    FUEL,
    INTACT,
    zeros_state,
)

L = 8


def _fields(hazard=None, structure=None, increment=None):
    """All-clear h'/c'/increment fields with optional hand-set cells."""
    hz = jnp.full((L, L), FUEL, jnp.uint8)
    st = jnp.full((L, L), INTACT, jnp.uint8)
    inc = jnp.zeros((L, L), jnp.bool_)
    for cell, val in hazard or []:
        hz = hz.at[cell].set(val)
    for cell in structure or []:
        st = st.at[cell].set(COLLAPSED)
    for cell in increment or []:
        inc = inc.at[cell].set(True)
    return hz, st, inc


STAY, UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3, 4


def _one(action, hazard=None, structure=None, increment=None, alive=True):
    """Run agent_step for a single agent at (2, 2)."""
    hz, st, inc = _fields(hazard, structure, increment)
    pos = jnp.array([[2, 2]], jnp.int32)
    return agent_step(
        pos,
        jnp.array([alive]),
        jnp.array([action], jnp.int32),
        hz,
        st,
        inc,
        L,
    )


def test_burning_kills_stationary_agent():
    # A cell igniting under a stationary agent kills it (h' evaluated).
    pos, alive, d_fire, d_coll, _ = _one(STAY, hazard=[((2, 2), BURNING)])
    assert not bool(alive[0])
    assert (int(d_fire), int(d_coll)) == (1, 0)
    assert (pos[0] == jnp.array([2, 2])).all()


def test_moving_into_burning_cell_kills():
    pos, alive, d_fire, _, _ = _one(RIGHT, hazard=[((2, 3), BURNING)])
    assert not bool(alive[0])
    assert int(d_fire) == 1
    assert (pos[0] == jnp.array([2, 3])).all()  # died on arrival at x'


def test_burnt_is_passable_and_harmless():
    pos, alive, d_fire, d_coll, _ = _one(RIGHT, hazard=[((2, 3), BURNT)])
    assert bool(alive[0])
    assert (pos[0] == jnp.array([2, 3])).all()
    assert int(d_fire) + int(d_coll) == 0


def test_collapsed_blocks_movement():
    pos, alive, _, _, n_blocked = _one(RIGHT, structure=[(2, 3)])
    assert bool(alive[0])
    assert (pos[0] == jnp.array([2, 2])).all()  # move cancelled, stays
    assert int(n_blocked) == 1  # counted as a blocking encounter (M3.4)


def test_collapse_under_agent_kills_no_escape():
    # DECISION (human-locked): the floor gives way before the agent acts —
    # moving away the same step does not save it.
    pos, alive, d_fire, d_coll, _ = _one(RIGHT, structure=[(2, 2)], increment=[(2, 2)])
    assert not bool(alive[0])
    assert (int(d_fire), int(d_coll)) == (0, 1)
    assert (pos[0] == jnp.array([2, 2])).all()  # fell: never moved


def test_dead_agents_are_inert_and_not_recounted():
    # Fire and collapse both under an already-dead agent: no motion, no
    # double-counted death.
    pos, alive, d_fire, d_coll, _ = _one(
        RIGHT,
        hazard=[((2, 2), BURNING)],
        increment=[(2, 2)],
        structure=[(2, 2)],
        alive=False,
    )
    assert not bool(alive[0])
    assert int(d_fire) + int(d_coll) == 0
    assert (pos[0] == jnp.array([2, 2])).all()


def _state_with(cfg, agent_pos, hazard_cells=(), food_cells=()):
    s = zeros_state(cfg.grid_size, len(agent_pos), jax.random.PRNGKey(0))
    hz = s.hazard
    for cell, val in hazard_cells:
        hz = hz.at[cell].set(val)
    food = s.food
    for cell in food_cells:
        food = food.at[cell].set(1)
    return dataclasses.replace(
        s, agent_pos=jnp.array(agent_pos, jnp.int32), hazard=hz, food=food
    )


def test_step_ignition_under_stationary_agent_kills_and_penalizes():
    # beta = 1: the Burning neighbor ignites the agent's Fuel cell in h'.
    theta = ThetaConfig(beta=1.0, death_penalty=0.5)
    cfg = EnvConfig(grid_size=L, n_agents=1, horizon=32, n_food=1, theta=theta)
    s = _state_with(cfg, [[2, 2]], hazard_cells=[((2, 3), BURNING)])
    actions = jnp.array([STAY], jnp.int32)
    _, s_new, reward, _, info = step(jax.random.PRNGKey(7), s, actions, cfg)
    assert not bool(s_new.agent_alive[0])
    assert int(info["deaths_fire"]) == 1
    assert int(info["deaths_collapse"]) == 0
    assert float(reward) == -0.5  # no food collected, one death at c = 0.5


def test_newly_dead_agent_does_not_collect():
    # Food sits on a cell that ignites this step; the agent moves onto it,
    # dies on arrival, and the item stays (DECISION in env.step).
    theta = ThetaConfig(beta=1.0, death_penalty=0.0)
    cfg = EnvConfig(grid_size=L, n_agents=1, horizon=32, n_food=1, theta=theta)
    s = _state_with(
        cfg,
        [[2, 2]],
        hazard_cells=[((2, 4), BURNING)],  # ignites (2, 3) in h'
        food_cells=[(2, 3)],
    )
    actions = jnp.array([RIGHT], jnp.int32)
    _, s_new, reward, _, info = step(jax.random.PRNGKey(7), s, actions, cfg)
    assert not bool(s_new.agent_alive[0])
    assert int(info["deaths_fire"]) == 1
    assert float(reward) == 0.0
    assert int(s_new.food[2, 3]) == 1  # not collected


def test_dead_agents_inert_over_rollout():
    # Supercritical fire + spontaneous ignition: deaths are certain. Once
    # dead: alive stays False, position frozen forever.
    theta = ThetaConfig(beta=0.9, iota=0.05)
    cfg = EnvConfig(grid_size=16, n_agents=4, horizon=64, n_food=8, theta=theta)
    key = jax.random.PRNGKey(1)
    key, k_reset = jax.random.split(key)
    _, state = reset(k_reset, cfg)

    def body(carry, _):
        key, state = carry
        key, k_act, k_step = jax.random.split(key, 3)
        actions = jax.random.randint(k_act, (cfg.n_agents,), 0, 5, jnp.int32)
        _, state, _, _, _ = step(k_step, state, actions, cfg)
        return (key, state), (state.agent_alive, state.agent_pos)

    _, (alive, pos) = jax.lax.scan(body, (key, state), None, length=40)
    assert not alive[-1].all()  # the hazard actually killed someone
    # Alive is monotone non-increasing (no resurrection).
    assert (alive[1:] <= alive[:-1]).all()
    # Positions frozen from the step an agent is dead onward.
    dead = ~alive[:-1]
    moved = (pos[1:] != pos[:-1]).any(axis=-1)
    assert not (dead & moved).any()
