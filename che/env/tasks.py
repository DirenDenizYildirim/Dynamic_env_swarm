"""Phase-0 foraging stub: task dynamics + reward (Def. 2 compliant).

The reward function reads *task variables only* (food grid + agent
occupancy). It must never take hazard, smoke, or structural state as
arguments — that is the paper's Definition 2 and is enforced by
tests/test_reward_independence.py. If a future task seems to need
hazard-aware reward: stop and ask (CLAUDE.md invariant #1).
"""

import chex
import jax
import jax.numpy as jnp


def occupancy_grid(
    agent_pos: jax.Array, agent_alive: jax.Array, grid_size: int
) -> jax.Array:
    """Boolean [L, L] grid, True where at least one alive agent stands."""
    chex.assert_shape(agent_pos, (None, 2))
    occ = jnp.zeros((grid_size, grid_size), dtype=jnp.bool_)
    return occ.at[agent_pos[:, 0], agent_pos[:, 1]].max(agent_alive)


def spawn_food(key: jax.Array, grid_size: int, n_food: int) -> jax.Array:
    """Scatter n_food items on distinct cells, uniformly at random."""
    idx = jax.random.choice(key, grid_size * grid_size, (n_food,), replace=False)
    flat = jnp.zeros((grid_size * grid_size,), dtype=jnp.uint8).at[idx].set(1)
    return flat.reshape(grid_size, grid_size)


def task_step(food: jax.Array, occupancy: jax.Array) -> tuple[jax.Array, jax.Array]:
    """Collection: an occupied food cell yields +1 team reward and empties.

    Multiple agents on one food cell still collect a single item (+1).
    Returns (food', team_reward). Reads task variables and agent occupancy
    only — no hazard/smoke/structure arguments, by design (Def. 2).
    """
    chex.assert_type(food, jnp.uint8)
    chex.assert_equal_shape([food, occupancy])
    collected = (food == 1) & occupancy
    reward = collected.sum().astype(jnp.float32)
    food_new = jnp.where(collected, jnp.uint8(0), food).astype(jnp.uint8)
    return food_new, reward
