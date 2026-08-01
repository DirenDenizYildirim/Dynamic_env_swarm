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

from che.env.comms import in_range_mask, sample_links
from che.env.config import EnvConfig, MixtureComponent
from che.env.hazard import hazard_step, seed_ignitions, smoke_step
from che.env.observation import masked_fraction, observe, per_agent_masked
from che.env.structure import (
    coupling_a_seed_mask,
    dilate,
    generate_weak_mask,
    structure_step,
)
from che.env.tasks import occupancy_grid, spawn_food, task_step
from che.env.types import (
    BURNING,
    COLLAPSED,
    FUEL,
    INTACT,
    EnvState,
    ThetaLive,
)

# Action set: 5 discrete actions (stay + 4 von-Neumann moves).
N_ACTIONS = 5

# M3.1: fold_in tag for the weak-terrain reset stream (any fixed constant).
_WEAK_STREAM = 31
# M4.1: fold_in tag for the obs v3 reveal draw (Coupling B). DECISION:
# derived via fold_in from the reset/step key — like _WEAK_STREAM — so the
# pre-existing kernel streams (split(key, 3/4)) are provably untouched and
# obs v3 with kappa_B = 0 bitwise-recovers the obs v2 trajectories
# (invariant #3). fold_in is pure: computing it never advances `key`.
_OBS_STREAM = 47
# M5.0: fold_in tag for the comms link draw (T_K, Def. 7). Same DECISION as
# _WEAK_STREAM/_OBS_STREAM: a dedicated derived stream, so the split(key, 3)
# kernel streams are provably untouched and delta = 0 bitwise-recovers the
# pre-comms trajectories (invariant #3).
_COMMS_STREAM = 53
# M6.0: fold_in tag for the mixture-component draw. Same DECISION as the
# three streams above — a dedicated derived stream, so the split(key, 3/4)
# kernel streams are provably untouched and a single-component (degenerate)
# mixture bitwise-recovers the pre-M6.0 trajectories (invariant #3).
_MIXTURE_STREAM = 59
_ACTION_OFFSETS = jnp.array([[0, 0], [-1, 0], [1, 0], [0, -1], [0, 1]], dtype=jnp.int32)


def _mixture_table(cfg: EnvConfig) -> tuple[jax.Array, dict[str, jax.Array]]:
    """Static -> arrays: (log-weights, {field: per-component values}).

    A component is a patch on the base theta, so an unset field inherits
    `cfg.theta`. Built from Python floats at trace time; the only traced
    thing is the index that selects a row.
    """
    comps = cfg.mixture.components or (
        # The degenerate case, synthesized rather than branched: one
        # component that IS the config's theta. This is what keeps the
        # traced path the only path (invariant #3 — the draw always happens
        # and always consumes its stream, even when it cannot change).
        MixtureComponent(name="_config", weight=1.0),
    )
    total = sum(c.weight for c in comps)
    logits = jnp.log(
        jnp.asarray([c.weight / total for c in comps], dtype=jnp.float32)
    )
    base = cfg.theta
    table = {
        field: jnp.asarray(
            [
                getattr(base, field) if getattr(c, field) is None
                else getattr(c, field)
                for c in comps
            ],
            dtype=jnp.float32,
        )
        for field in ("beta", "kappa_A", "kappa_B", "delta")
    }
    return logits, table


def sample_theta_live(
    key: jax.Array, cfg: EnvConfig
) -> tuple[ThetaLive, jax.Array]:
    """Draw this episode's traced theta (M6.0), returning (theta_live, index).

    Called once per reset/autoreset. `key` must already be the dedicated
    mixture stream (see `_MIXTURE_STREAM`), so the draw can never perturb the
    reset splits and a single-component mixture bitwise-recovers pre-M6.0
    trajectories.

    The draw is UNCONDITIONAL (invariant #3): a one-component mixture still
    samples a categorical whose outcome is forced, exactly as the zeroed
    stressor branches still sample uniforms they compare against 0. Nothing
    here branches on a config value in a way that changes key consumption.
    """
    logits, table = _mixture_table(cfg)
    idx = jax.random.categorical(key, logits)
    return (
        ThetaLive(**{field: values[idx] for field, values in table.items()}),
        idx.astype(jnp.int32),
    )


def _comms_obs(
    key: jax.Array,
    agent_pos: jax.Array,
    agent_alive: jax.Array,
    cfg: EnvConfig,
    delta: jax.Array,
) -> tuple[jax.Array, jax.Array]:
    """T_K (Def. 7) at Prop.-1 position 5: (links, in_range) from x' only.

    Returns the realized directed link graph and the eligibility mask it was
    thinned from — the mask is the delivery-rate denominator, kept so the
    eval harness can pool exact ratios instead of averaging per-step ones
    (the M4.4 numerator/denominator lesson).

    M6.0: `delta` is traced (per-episode, from the state) while `r_comm`
    stays static on the config — the range is locked geometry that no
    mixture varies, and it is also the one comms parameter that would change
    nothing if traced (the [n, n] mask is built at full shape regardless).
    """
    in_range = in_range_mask(agent_pos, agent_alive, cfg.theta.r_comm)
    return sample_links(key, in_range, delta), in_range


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
    # M6.0: this episode's traced theta, drawn before anything that reads it
    # (the frozen burn-in below uses beta). Its stream is derived by fold_in,
    # so the four reset splits are untouched.
    theta_live, mixture_component = sample_theta_live(
        jax.random.fold_in(key, _MIXTURE_STREAM), cfg
    )
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
            return hazard_step(k, h, beta=theta_live.beta, iota=th.iota), None

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
        theta_live=theta_live,
        mixture_component=mixture_component,
    )
    obs = observe(state, cfg, jax.random.fold_in(key, _OBS_STREAM))
    # M5.0: the reset obs carries a link graph too, so the obs schema is the
    # same object at t = 0 and after every step (autoreset tree_maps over
    # both branches). No message has been emitted yet, so the aggregate the
    # policy builds from it is the zero vector either way.
    links, _ = _comms_obs(
        jax.random.fold_in(key, _COMMS_STREAM),
        agent_pos,
        state.agent_alive,
        cfg,
        theta_live.delta,
    )
    return {**obs, "links": links}, state


def step(
    key: jax.Array, state: EnvState, actions: jax.Array, cfg: EnvConfig
) -> tuple[dict[str, jax.Array], EnvState, jax.Array, jax.Array, dict[str, jax.Array]]:
    """One environment transition in the Prop.-1 order.

    Returns (obs, state', team_reward, done, info). `state.key` records the
    key used to produce the state (bookkeeping only; all sampling uses the
    explicit `key` argument, split once per stochastic kernel).
    """
    th = cfg.theta
    # M6.0: beta/kappa_A/kappa_B/delta come from the state (traced, resampled
    # per episode by the mixture); everything else stays static on the config.
    # theta_live is constant for the episode's duration, so every kernel in
    # the Prop.-1 order below reads one consistent theta.
    tl = state.theta_live
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
        k_seed, collapse_increment, kappa_A=tl.kappa_A, r_seed=th.r_seed
    )
    hazard_ca = hazard_step(k_fire, state.hazard, beta=tl.beta, iota=th.iota)
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

    # 5. k' ~ T_K(x'): comms channel (Def. 7, M5.0). Reads post-step
    # positions/aliveness only — never h', rho' or c' — and draws from its
    # own fold_in stream, so delta cannot perturb any kernel above.
    links, links_in_range = _comms_obs(
        jax.random.fold_in(key, _COMMS_STREAM), pos_new, alive_new, cfg, tl.delta
    )

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
        # theta_live is fixed for the episode: the mixture draws it at
        # reset/autoreset, never mid-episode.
        theta_live=tl,
        mixture_component=state.mixture_component,
    )
    # Post-step state, per Prop. 1; the reveal draw (obs v3, Coupling B)
    # uses its own fold_in stream so the kernel streams above are untouched.
    obs = observe(state_new, cfg, jax.random.fold_in(key, _OBS_STREAM))
    obs = {**obs, "links": links}

    # Invariant #5: coupling-co-active counter — collapse-seeded ignitions
    # within perception range (DECISION: Chebyshev radius obs_window // 2,
    # matching the crop; revisit when Coupling B fixes attenuation range)
    # of an alive agent, evaluated at post-step positions x'.
    near_agents = dilate(occ_post, cfg.obs_window // 2)
    co_active = (seeded_ignitions & near_agents).sum().astype(jnp.int32)
    # M4.4 addendum (a): agents in a "danger moment" — a Burning cell
    # inside the crop (same Chebyshev radius as the co-active test).
    burning_near = dilate(hazard_new == BURNING, cfg.obs_window // 2)
    danger = alive_new & burning_near[pos_new[:, 0], pos_new[:, 1]]
    agent_masked = per_agent_masked(obs["grid"], cfg)
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
        # M4.0 harness addendum (Phase-4 carry-overs; info-only, no PRNG):
        # burnt_fraction = non-Fuel share of the arena — matches the
        # Phase-2/3 burnt-cells observable (calibration counts non-Fuel at
        # the horizon); nondecreasing, final value at done is the episode
        # metric. masked_frac = mean over alive agents of the masked
        # crop-cell share (identically 0 until M4.1's obs v3 mask).
        "burnt_fraction": (hazard_new != FUEL).mean(dtype=jnp.float32),
        "masked_frac": masked_fraction(obs["grid"], alive_new, cfg),
        # M4.4 addendum (a), human-locked 2026-07-27: *danger-moment*
        # masking — the masked share restricted to alive agents with a
        # Burning cell inside their crop. Reported as a diagnostic, never
        # as a calibration band (the M4.3 lock retired the unconditional
        # masked_frac band because it is policy-suppressible). Emitted as
        # numerator/denominator counts, not as a per-step ratio, so the
        # eval harness can pool them exactly over steps and episodes
        # instead of averaging conditional means over steps where the
        # condition never fired. "In crop" is the Chebyshev radius
        # obs_window // 2 — the crop's own metric, matching invariant
        # #5's co-active test. Deterministic, no PRNG (invariant #3).
        "masked_danger_sum": jnp.where(danger, agent_masked, 0.0).sum(),
        "danger_agents": danger.sum(dtype=jnp.float32),
        "alive_agents": alive_new.sum(dtype=jnp.float32),
        # M5.0 comms channels (Def. 7), emitted as poolable numerator /
        # denominator counts rather than per-step ratios — same reason as
        # the M4.4 danger-moment pair: pooling over steps and episodes must
        # weight each ordered pair equally, not each step. Delivery rate =
        # links_alive / links_in_range (isolates delta from geometry);
        # mean alive out-degree = links_alive / alive_agents (geometry x
        # knob, the M5.4 band observable). Deterministic given the sampled
        # graph; the reward never reads them (Def. 2).
        "links_alive": links.sum(dtype=jnp.float32),
        "links_in_range": links_in_range.sum(dtype=jnp.float32),
        # M6.0c: which mixture component this episode was drawn from, so a
        # training run can be audited against its intended weights (spike
        # acceptance 2d). Reports the STEPPING episode's component: under
        # autoreset, `state` is the ending episode while the returned state
        # may already be a fresh draw, and `info` describes the former.
        # Deterministic, info-only, consumes no PRNG (invariants #3, Def. 2).
        "mixture_component": state.mixture_component,
    }
    return obs, state_new, reward, done, info
