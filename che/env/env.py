"""Composed CHE environment: reset/step in the Prop.-1 kernel order.

Step order (CLAUDE.md invariant #2, Prop. 1):
    1. c'   ~ T_C(c, x)            structure_step (reads pre-step occupancy)
    2. h'   ~ T_H(h, c, c')        CA spread, then Coupling A seeds from c'-c
    3. rho' =  e^{-eta} rho + ...  smoke_step (reads h')
    4. x'   ~ T_X(x, a, h, c)      moves + task collection
    5. k'   ~ T_K(x')              comms — Phase 5 (not built in Phase 0)
Observations are drawn from the post-step state O(. | x', h', rho', c', k').

Phase-0 restriction: hazard/smoke/structure run every step (the M0.4 gate
must measure their real cost) but do NOT affect agents — T_X ignores h and c
until Phase 1. Deaths, blocking, and Coupling B enter later phases.

Invariant #5: the coupling-co-active counter (collapse-seeded ignitions
within perception range of an alive agent) is computed and logged in `info`
from day one, even though it is identically 0 while kappa_A = 0.
"""

import chex
import jax
import jax.numpy as jnp

from che.env.config import EnvConfig
from che.env.hazard import hazard_step, seed_ignitions, smoke_step
from che.env.observation import observe
from che.env.structure import coupling_a_seed_mask, dilate, structure_step
from che.env.tasks import occupancy_grid, spawn_food, task_step
from che.env.types import BURNING, COLLAPSED, FUEL, INTACT, EnvState

# Action set: 5 discrete actions (stay + 4 von-Neumann moves).
N_ACTIONS = 5
_ACTION_OFFSETS = jnp.array(
    [[0, 0], [-1, 0], [1, 0], [0, -1], [0, 1]], dtype=jnp.int32
)


def move_agents(
    agent_pos: jax.Array, actions: jax.Array, agent_alive: jax.Array, grid_size: int
) -> jax.Array:
    """T_X movement: clip-to-grid von-Neumann moves; dead agents hold still.

    Signature note: T_X(x' | x, a, h, c) may read h and c (Def. 1); in
    Phase 0 movement ignores them by design (hazard is inert to agents).
    """
    chex.assert_shape(agent_pos, (None, 2))
    proposed = agent_pos + _ACTION_OFFSETS[actions]
    proposed = jnp.clip(proposed, 0, grid_size - 1)
    return jnp.where(agent_alive[:, None], proposed, agent_pos).astype(jnp.int32)


def reset(key: jax.Array, cfg: EnvConfig) -> tuple[dict[str, jax.Array], EnvState]:
    """Initial state: food on distinct cells, agents uniform (overlap OK —
    DECISION), all-Fuel hazard with one random ignition (DECISION: gives the
    gate and the obs planes real fire/smoke dynamics; cost is state-
    independent), intact structure, zero smoke.
    """
    ll = cfg.grid_size
    k_food, k_agents, k_fire = jax.random.split(key, 3)
    food = spawn_food(k_food, ll, cfg.n_food)
    agent_pos = jax.random.randint(
        k_agents, (cfg.n_agents, 2), minval=0, maxval=ll, dtype=jnp.int32
    )
    fire_cell = jax.random.randint(k_fire, (2,), minval=0, maxval=ll)
    hazard = jnp.full((ll, ll), FUEL, dtype=jnp.uint8)
    hazard = hazard.at[fire_cell[0], fire_cell[1]].set(BURNING)
    state = EnvState(
        agent_pos=agent_pos,
        agent_alive=jnp.ones((cfg.n_agents,), dtype=jnp.bool_),
        food=food,
        hazard=hazard,
        smoke=jnp.zeros((ll, ll), dtype=jnp.float32),
        structure=jnp.full((ll, ll), INTACT, dtype=jnp.uint8),
        t=jnp.zeros((), dtype=jnp.int32),
        key=key,
    )
    return observe(state, cfg), state


def step(
    key: jax.Array, state: EnvState, actions: jax.Array, cfg: EnvConfig
) -> tuple[dict[str, jax.Array], EnvState, jax.Array, jax.Array, dict[str, jax.Array]]:
    """One environment transition in the Prop.-1 order.

    Returns (obs, state', team_reward, done, info). `state.key` records the
    key used to produce the state (bookkeeping only; all sampling uses the
    explicit `key` argument, split once per stochastic kernel).
    """
    th = cfg.theta
    k_struct, k_seed, k_fire = jax.random.split(key, 3)

    # 1. c' ~ T_C(c, x): reads *pre-step* occupancy.
    occ_pre = occupancy_grid(state.agent_pos, state.agent_alive, cfg.grid_size)
    structure_new = structure_step(
        k_struct,
        state.structure,
        occ_pre.astype(jnp.float32),
        lambda_0=th.lambda_0,
        lambda_load=th.lambda_load,
    )
    collapse_increment = (structure_new == COLLAPSED) & (state.structure == INTACT)

    # 2. h' ~ T_H(h, c, c'): CA spread, then the Coupling A impulse from the
    # collapse increment (seeded cells are Burning in h', spread next step).
    seed_mask = coupling_a_seed_mask(
        k_seed, collapse_increment, kappa_A=th.kappa_A, r_seed=th.r_seed
    )
    hazard_ca = hazard_step(k_fire, state.hazard, beta=th.beta, iota=th.iota)
    hazard_new = seed_ignitions(hazard_ca, seed_mask)
    seeded_ignitions = hazard_ca != hazard_new  # Fuel cells Coupling A lit

    # 3. rho' from h' (Def. 6; smoke outlives flame).
    smoke_new = smoke_step(state.smoke, hazard_new, sigma_s=th.sigma_s, eta=th.eta)

    # 4. x' ~ T_X(x, a, h, c) + task dynamics (collection on post-move cells).
    pos_new = move_agents(state.agent_pos, actions, state.agent_alive, cfg.grid_size)
    occ_post = occupancy_grid(pos_new, state.agent_alive, cfg.grid_size)
    food_new, reward = task_step(state.food, occ_post)

    # 5. k' ~ T_K(x'): comms channel — Phase 5.

    t_new = state.t + 1
    done = t_new >= cfg.horizon
    state_new = EnvState(
        agent_pos=pos_new,
        agent_alive=state.agent_alive,
        food=food_new,
        hazard=hazard_new,
        smoke=smoke_new,
        structure=structure_new,
        t=t_new,
        key=key,
    )
    obs = observe(state_new, cfg)  # post-step state, per Prop. 1

    # Invariant #5: coupling-co-active counter — collapse-seeded ignitions
    # within perception range (DECISION: Chebyshev radius obs_window // 2,
    # matching the crop; revisit when Coupling B fixes attenuation range)
    # of an alive agent, evaluated at post-step positions x'.
    near_agents = dilate(occ_post, cfg.obs_window // 2)
    co_active = (seeded_ignitions & near_agents).sum().astype(jnp.int32)
    info = {
        "coupling_co_active": co_active,
        "food_remaining": food_new.sum().astype(jnp.int32),
    }
    return obs, state_new, reward, done, info
