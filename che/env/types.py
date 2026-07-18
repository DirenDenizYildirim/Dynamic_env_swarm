"""State containers for the CHE environment (Def. 1: S = X x H x C x K).

Dtype decisions (per CLAUDE.md conventions, documented here):
- ``hazard``: uint8 with the Sigma_H coding FUEL=0, BURNING=1, BURNT=2
  (Def. 3). uint8 keeps the grid cheap to move and compare; kernels cast to
  float32 locally for convolutions.
- ``structure``: uint8, INTACT=0, COLLAPSED=1 (Def. 5; collapsed absorbing).
- ``food``: uint8 presence grid, the Phase-0 foraging task state. It is a
  *task variable* in the sense of Def. 2 (reward may read it; reward may
  never read hazard/smoke/structure).
- ``smoke``: float32 density field rho (Def. 6; smoke outlives flame, D3).
- ``agent_pos``: int32 [n, 2] grid coordinates (row, col); int32 is safe for
  any realistic L and matches JAX's default integer width on GPU.
- ``agent_alive``: bool [n] (alpha_i in Def. 1).
- ``t``: int32 scalar timestep.
- ``key``: the environment's own PRNG key, threaded through step (invariant:
  split at call boundaries, never reuse, consume unconditionally).
"""

import jax
import jax.numpy as jnp
from chex import dataclass

# Sigma_H per-cell hazard states (Def. 3).
FUEL: int = 0
BURNING: int = 1
BURNT: int = 2

# Structural states (Def. 5).
INTACT: int = 0
COLLAPSED: int = 1


@dataclass
class EnvState:
    """Full environment state s = (x, h, rho, c, t) plus PRNG key.

    The comms-channel state k (Def. 7) is sampled fresh each step from x'
    (Prop. 1 order) and consumed within the step, so it is not carried here;
    it becomes a state component only if delayed/buffered messaging is added
    (Phase 5 decision).
    """

    # --- X: joint agent state ---
    agent_pos: jax.Array  # int32 [n_agents, 2], (row, col) on the grid
    agent_alive: jax.Array  # bool [n_agents]
    # --- task state (Phase-0 foraging stub; Def. 2 "task variables") ---
    food: jax.Array  # uint8 [L, L], 1 where an uncollected food item sits
    # --- H: hazard field and smoke density ---
    hazard: jax.Array  # uint8 [L, L], values in {FUEL, BURNING, BURNT}
    smoke: jax.Array  # float32 [L, L], rho >= 0
    # --- C: structural state ---
    structure: jax.Array  # uint8 [L, L], values in {INTACT, COLLAPSED}
    # --- bookkeeping ---
    t: jax.Array  # int32 scalar
    key: jax.Array  # PRNG key


def zeros_state(grid_size: int, n_agents: int, key: jax.Array) -> EnvState:
    """An all-clear state at t=0: all Fuel, no smoke, intact, agents at origin.

    Used by tests and as the template `reset` (M0.3) fills in.
    """
    ll = grid_size
    return EnvState(
        agent_pos=jnp.zeros((n_agents, 2), dtype=jnp.int32),
        agent_alive=jnp.ones((n_agents,), dtype=jnp.bool_),
        food=jnp.zeros((ll, ll), dtype=jnp.uint8),
        hazard=jnp.full((ll, ll), FUEL, dtype=jnp.uint8),
        smoke=jnp.zeros((ll, ll), dtype=jnp.float32),
        structure=jnp.full((ll, ll), INTACT, dtype=jnp.uint8),
        t=jnp.zeros((), dtype=jnp.int32),
        key=key,
    )
