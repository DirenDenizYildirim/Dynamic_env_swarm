"""Composed CHE environment: reset/step in the Prop.-1 kernel order.

Step order (CLAUDE.md invariant #2, Prop. 1):
    1. c'   ~ T_C(c, x)            structure_step (reads pre-step occupancy)
    2. h'   ~ T_H(h, c, c')        CA spread, then Coupling A seeds from c'-c
    3. rho' =  e^{-eta} rho + ...  smoke_step (reads h')
    4. x'   ~ T_X(x, a, h', c')    kills/blocking vs h', c' + task collection
    5. k'   ~ T_K(x')              comms — Phase 5 (not built in Phase 0)
Observations are drawn from the post-step state O(. | x', h', rho', c', k').

Phase-1 (M1.1) semantics — T_X finally reads the hazard and structure. Per
the Prop.-1 sequential composition, h' and c' are already-sampled components
of s' when T_X runs, so lethality/blocking are evaluated against the
*post-update* fields (a cell igniting under a stationary agent kills it).
Death logic is deterministic given the sampled fields: it consumes no PRNG,
so it cannot perturb any other subsystem's stream (invariant #3).

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
from che.env.structure import (
    coupling_a_seed_mask,
    dilate,
    generate_weak_mask,
    structure_step,
)
from che.env.tasks import occupancy_grid, spawn_food, task_step
from che.env.types import BURNING, COLLAPSED, FUEL, INTACT, EnvState

# Action set: 5 discrete actions (stay + 4 von-Neumann moves).
N_ACTIONS = 5

# M3.1: fold_in tag for the weak-terrain reset stream (any fixed constant).
_WEAK_STREAM = 31
_ACTION_OFFSETS = jnp.array([[0, 0], [-1, 0], [1, 0], [0, -1], [0, 1]], dtype=jnp.int32)


def agent_step(
    agent_pos: jax.Array,
    agent_alive: jax.Array,
    actions: jax.Array,
    hazard_new: jax.Array,
    structure_new: jax.Array,
    collapse_increment: jax.Array,
    grid_size: int,
) -> tuple[jax.Array, jax.Array, jax.Array, jax.Array]:
    """T_X (Def. 1) with M1.1 lethality and blocking, in this order:

    1. **Collapse-kill (pre-move x).** An alive agent standing on a cell of
       the collapse increment (c' - c) falls and is disabled. DECISION
       (human-locked): no escape — the floor gives way before the agent
       acts; consistent with c' being sampled before x' (Prop. 1).
    2. **Movement.** Survivors propose clip-to-grid von-Neumann moves; a
       move into a cell Collapsed in c' is cancelled (agent stays). Burnt
       cells are passable (ash). Dead agents hold still.
    3. **Fire-kill (post-move x').** alive' = alive AND NOT(cell(x') is
       Burning in h') — evaluated against the post-update hazard, so a cell
       igniting under a stationary agent kills it. Burning cells are
       enterable (and lethal): avoidance must be learned, not enforced.

    Deterministic given its inputs — consumes no PRNG (invariant #3).
    Returns (pos', alive', deaths_fire, deaths_collapse, blocked_moves)
    with int32 counts; blocked_moves counts alive agents whose proposed
    move was cancelled by a Collapsed cell (M3.4-lock addendum: the
    non-ignition structural channel, reported at M3.5).
    """
    chex.assert_shape(agent_pos, (None, 2))
    chex.assert_type(hazard_new, jnp.uint8)
    chex.assert_type(structure_new, jnp.uint8)
    chex.assert_type(collapse_increment, jnp.bool_)
    fell = agent_alive & collapse_increment[agent_pos[:, 0], agent_pos[:, 1]]
    alive_mid = agent_alive & ~fell
    proposed = jnp.clip(agent_pos + _ACTION_OFFSETS[actions], 0, grid_size - 1)
    blocked = structure_new[proposed[:, 0], proposed[:, 1]] == COLLAPSED
    can_move = alive_mid & ~blocked
    pos_new = jnp.where(can_move[:, None], proposed, agent_pos).astype(jnp.int32)
    burned = alive_mid & (hazard_new[pos_new[:, 0], pos_new[:, 1]] == BURNING)
    alive_new = alive_mid & ~burned
    return (
        pos_new,
        alive_new,
        burned.sum().astype(jnp.int32),
        fell.sum().astype(jnp.int32),
        (alive_mid & blocked).sum().astype(jnp.int32),
    )


def reset(key: jax.Array, cfg: EnvConfig) -> tuple[dict[str, jax.Array], EnvState]:
    """Initial state: food on distinct cells, agents uniform (overlap OK —
    DECISION), all-Fuel hazard with one random ignition (DECISION: gives the
    gate and the obs planes real fire/smoke dynamics; cost is state-
    independent), intact structure, zero smoke.

    M1.3 frozen mode: the CA is burned in for t_gen steps (default
    horizon / 2) from the single ignition, then h is frozen for the whole
    episode. Rationale (preserve): with t_gen = horizon / 2 the frozen map
    is a draw from the *same marginal* the dynamic env passes through
    mid-episode — the control differs in evolution, not in hazard mass
    (the system-scale analogue of Thm. 1's fixed-map policy). Smoke is NOT
    pre-accumulated: it starts at 0 and evolves during the episode from the
    frozen Burning set (still lethal, still smoke-emitting).
    """
    ll = cfg.grid_size
    th = cfg.theta
    # Unconditional 4-way split (invariant #3): dynamic mode discards
    # k_burnin, so dynamic<->frozen resets with the same key place identical
    # food/agents/ignition and differ only through the freeze.
    k_food, k_agents, k_fire, k_burnin = jax.random.split(key, 4)
    # M3.1: weak-cell terrain from a dedicated stream. DECISION: derived via
    # fold_in rather than widening the 4-way split above, so the four
    # Phase-2 reset streams are provably untouched (invariant #3 — bitwise
    # recovery of Phase-2 trajectories when the structural element is off).
    weak = generate_weak_mask(
        jax.random.fold_in(key, _WEAK_STREAM),
        ll,
        f_weak=th.f_weak,
        n_smooth=th.weak_smooth,
    )
    food = spawn_food(k_food, ll, cfg.n_food)
    agent_pos = jax.random.randint(
        k_agents, (cfg.n_agents, 2), minval=0, maxval=ll, dtype=jnp.int32
    )
    fire_cell = jax.random.randint(k_fire, (2,), minval=0, maxval=ll)
    hazard = jnp.full((ll, ll), FUEL, dtype=jnp.uint8)
    hazard = hazard.at[fire_cell[0], fire_cell[1]].set(BURNING)
    if cfg.hazard_mode == "frozen":  # static branch: cfg is a static arg

        def burn(h: jax.Array, k: jax.Array):
            return hazard_step(k, h, beta=th.beta, iota=th.iota), None

        hazard, _ = jax.lax.scan(
            burn, hazard, jax.random.split(k_burnin, cfg.t_gen_resolved)
        )
    state = EnvState(
        agent_pos=agent_pos,
        agent_alive=jnp.ones((cfg.n_agents,), dtype=jnp.bool_),
        food=food,
        hazard=hazard,
        smoke=jnp.zeros((ll, ll), dtype=jnp.float32),
        structure=jnp.full((ll, ll), INTACT, dtype=jnp.uint8),
        weak=weak,
        t=jnp.zeros((), dtype=jnp.int32),
        key=key,
        ep_deaths_fire=jnp.zeros((), dtype=jnp.int32),
        ep_deaths_collapse=jnp.zeros((), dtype=jnp.int32),
        ep_smoke_sum=jnp.zeros((), dtype=jnp.float32),
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
        state.weak,
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
    if cfg.hazard_mode == "frozen":
        # M1.3: h is frozen — the CA/seed draws above still happen and are
        # discarded, so dynamic<->frozen with the same key share every
        # other stream bitwise (invariant #3). Frozen Burning cells stay
        # Burning: lethal and smoke-emitting, but never spread or burn out.
        hazard_new = state.hazard
        seeded_ignitions = jnp.zeros_like(seed_mask)
    else:
        hazard_new = seed_ignitions(hazard_ca, seed_mask)
        seeded_ignitions = hazard_ca != hazard_new  # Fuel cells Coupling A lit

    # 3. rho' from h' (Def. 6; smoke outlives flame).
    smoke_new = smoke_step(state.smoke, hazard_new, sigma_s=th.sigma_s, eta=th.eta)

    # 4. x' ~ T_X + task dynamics. M1.1: lethality/blocking against h'/c'.
    # DECISION: an agent disabled this step does not collect food this step
    # (it died before/on arrival) — occupancy filters on the post-death
    # alive vector, keeping "dead agents never collect" exact.
    pos_new, alive_new, deaths_fire, deaths_collapse, blocked_moves = agent_step(
        state.agent_pos,
        state.agent_alive,
        actions,
        hazard_new,
        structure_new,
        collapse_increment,
        cfg.grid_size,
    )
    occ_post = occupancy_grid(pos_new, alive_new, cfg.grid_size)
    food_new, task_reward = task_step(state.food, occ_post)
    # Def.-2-compliant death penalty: reads only the alpha transition (an X
    # variable) — never hazard/smoke/structure directly.
    reward = task_reward - th.death_penalty * (deaths_fire + deaths_collapse).astype(
        jnp.float32
    )

    # 5. k' ~ T_K(x'): comms channel — Phase 5.

    t_new = state.t + 1
    done = t_new >= cfg.horizon
    ep_deaths_fire = state.ep_deaths_fire + deaths_fire
    ep_deaths_collapse = state.ep_deaths_collapse + deaths_collapse
    # Smoke exposure (Phase-2 metric, human-approved 2026-07-19): per-step
    # exposure = mean over *alive survivors* of rho'(x'_i), post-step fields
    # per Prop. 1; 0 when no one survives. DECISION: agents that die this
    # step contribute nothing — exposure tracks the operating swarm, and
    # death is already counted by its own metrics. Deterministic given the
    # sampled fields (consumes no PRNG, invariant #3) and info-only: the
    # reward never reads it (Def. 2).
    smoke_at_agents = smoke_new[pos_new[:, 0], pos_new[:, 1]]
    step_exposure = jnp.where(alive_new, smoke_at_agents, 0.0).sum() / jnp.maximum(
        alive_new.sum(dtype=jnp.float32), 1.0
    )
    ep_smoke_sum = state.ep_smoke_sum + step_exposure
    state_new = EnvState(
        agent_pos=pos_new,
        agent_alive=alive_new,
        food=food_new,
        hazard=hazard_new,
        smoke=smoke_new,
        structure=structure_new,
        weak=state.weak,  # fixed per episode (M3.1 terrain)
        t=t_new,
        key=key,
        ep_deaths_fire=ep_deaths_fire,
        ep_deaths_collapse=ep_deaths_collapse,
        ep_smoke_sum=ep_smoke_sum,
    )
    obs = observe(state_new, cfg)  # post-step state, per Prop. 1

    # Invariant #5: coupling-co-active counter — collapse-seeded ignitions
    # within perception range (DECISION: Chebyshev radius obs_window // 2,
    # matching the crop; revisit when Coupling B fixes attenuation range)
    # of an alive agent, evaluated at post-step positions x'.
    near_agents = dilate(occ_post, cfg.obs_window // 2)
    co_active = (seeded_ignitions & near_agents).sum().astype(jnp.int32)
    # M3.4-lock addendum channels (info-only, deterministic, no PRNG):
    # collapse events this step, blocked-move encounters (non-ignition
    # structural channel), and the share of alive survivors standing on
    # weak cells (load-avoidance observable for the M3.5 report).
    weak_occupancy = jnp.where(
        alive_new,
        state.weak[pos_new[:, 0], pos_new[:, 1]],
        False,
    ).sum(dtype=jnp.float32) / jnp.maximum(alive_new.sum(dtype=jnp.float32), 1.0)
    info = {
        "coupling_co_active": co_active,
        # M3.2: Coupling A output channel — count of Fuel cells ignited by
        # this step's collapse increment (0 whenever kappa_A = 0 or frozen).
        "seeded_ignitions": seeded_ignitions.sum().astype(jnp.int32),
        "collapse_events": collapse_increment.sum(dtype=jnp.int32),
        "blocked_moves": blocked_moves,
        "weak_occupancy": weak_occupancy.astype(jnp.float32),
        "food_remaining": food_new.sum().astype(jnp.int32),
        "deaths_fire": deaths_fire,
        "deaths_collapse": deaths_collapse,
        # M1.4 episode metrics — emitted every step, *valid at done* (with
        # autoreset they describe the ending episode; consumers mask by
        # done and aggregate NaN-safely).
        "survival_rate": alive_new.mean(dtype=jnp.float32),
        "completion": 1.0 - food_new.sum(dtype=jnp.float32) / jnp.float32(cfg.n_food),
        "ep_deaths_fire": ep_deaths_fire,
        "ep_deaths_collapse": ep_deaths_collapse,
        # Time-average of per-step exposure; t_new >= 1 so no zero division.
        "mean_smoke_exposure": ep_smoke_sum / t_new.astype(jnp.float32),
    }
    return obs, state_new, reward, done, info
