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
class ThetaLive:
    """The per-env TRACED slice of theta (M6.0 spike, decision_log 2026-08-01).

    These four are the composable stressor elements plus the severity axis —
    the only theta fields a training mixture varies. They live in `EnvState`
    rather than in `EnvConfig` because a mixture resamples them per episode
    at reset/autoreset, which makes them data, not configuration.

    WHY EXACTLY THESE FOUR. Each is a probability-like scalar consumed by a
    comparison against uniforms or by a multiply, so tracing costs one
    broadcast and changes no array shape:
      beta     -> hazard_step, compared against per-cell uniforms (Def. 3)
      kappa_A  -> coupling_a_seed_mask, a Bernoulli probability (Def. 5)
      kappa_B  -> transmittance, a multiply inside exp (Def. 6)
      delta    -> sample_links, compared against uniforms (Def. 7)

    WHAT IS DELIBERATELY NOT HERE (M6.0 scope fence):
      r_seed, obs_window, grid_size — shape/loop parameters; tracing them
        would change array shapes, not just values.
      sigma_s, eta — HARD exclusion. They feed observation.rho_max ->
        plane_scales, i.e. the uint8 quantization scales, whose reciprocal is
        folded on the HOST precisely because fp32 division is not correctly
        rounded on the GPU backend (M5.1h). Tracing them would dismantle that
        fix. Verified: plane_scales does not depend on kappa_B, so the uint8
        path is untouched by the mixture as scoped.
      death_penalty, r_comm — locked training-protocol/geometry constants
        that no mixture varies (docs/locks.yaml).

    float32 scalars, matching the dtype the kernels compare against.
    """

    beta: jax.Array
    kappa_A: jax.Array
    kappa_B: jax.Array
    delta: jax.Array


def theta_live_from(theta) -> ThetaLive:
    """Build the traced slice from a static `ThetaConfig`.

    This is the degenerate, single-component case: a run with no mixture is a
    run whose mixture has one component, so the traced path is the ONLY path
    and there is no `if mixture is None` branch anywhere in the kernels.
    Bitwise identity with the pre-refactor tree depends on these scalars
    holding exactly the float32 values the Python constants held.
    """
    return ThetaLive(
        beta=jnp.asarray(theta.beta, dtype=jnp.float32),
        kappa_A=jnp.asarray(theta.kappa_A, dtype=jnp.float32),
        kappa_B=jnp.asarray(theta.kappa_B, dtype=jnp.float32),
        delta=jnp.asarray(theta.delta, dtype=jnp.float32),
    )


@dataclass
class EnvState:
    """Full environment state s = (x, h, rho, c, t) plus PRNG key.

    The comms-channel state k (Def. 7) is sampled fresh each step from x'
    (Prop. 1 order) and consumed within the step, so it is not carried here.

    M5.0 resolution of the deferred "Phase 5 decision": still not carried.
    The message path does have one-step latency, but the latency lives in
    the *message tensors* (training/rollout carry, see comms.py), not in the
    graph: links sampled during step t ride out in obs_{t+1} and are
    consumed by the policy that acts at t+1, before step t+1 samples the
    next graph. Nothing in any kernel ever reads k back, which is also why
    delta cannot perturb a kernel stream (tests/test_comms.py).
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
    # M3.1 weak-cell terrain mask (Def. 5 substrate): bool [L, L], fixed per
    # episode at reset; only weak cells can collapse. Observable through the
    # structure obs plane (weak-intact = 0.5) per the M3.1 DECISION.
    weak: jax.Array
    # --- bookkeeping ---
    t: jax.Array  # int32 scalar
    key: jax.Array  # PRNG key
    # --- M1.4 episode accumulators (int32 scalars, reset to 0) ---
    # Death totals by cause since episode start; surfaced in `info` and
    # valid as episode metrics at done. Kept in state because per-step
    # info is not otherwise aggregable inside jitted collectors.
    ep_deaths_fire: jax.Array
    ep_deaths_collapse: jax.Array
    # --- M6.0: the traced theta slice for THIS episode ---
    # Sampled at reset/autoreset from the mixture spec on a dedicated stream
    # and held constant for the episode's duration, so every kernel in the
    # Prop.-1 order reads one consistent theta. `mixture_component` is the
    # index that was drawn; it is surfaced in `info` so a training run can be
    # audited against its intended mixture weights (spike acceptance 2d).
    theta_live: ThetaLive
    mixture_component: jax.Array  # int32 scalar
    # Running sum over steps of the mean smoke density rho'(x'_i) over alive
    # agents (float32 scalar; 0 contribution on steps with no survivors).
    # Surfaced as `mean_smoke_exposure` (divided by t) in `info` — an
    # H-derived *metric* only; never read by the reward (Def. 2).
    ep_smoke_sum: jax.Array


def zeros_state(
    grid_size: int, n_agents: int, key: jax.Array, theta_live: ThetaLive
) -> EnvState:
    """An all-clear state at t=0: all Fuel, no smoke, intact, agents at origin.

    Used by tests and as the template `reset` (M0.3) fills in.

    `theta_live` is REQUIRED, deliberately (M6.0). Since the kernels now read
    theta from the state, a default here would silently substitute some other
    theta for the caller's config — a wrong answer instead of an error. Build
    it with `theta_live_from(cfg.theta)`.
    """
    ll = grid_size
    return EnvState(
        theta_live=theta_live,
        mixture_component=jnp.zeros((), dtype=jnp.int32),
        agent_pos=jnp.zeros((n_agents, 2), dtype=jnp.int32),
        agent_alive=jnp.ones((n_agents,), dtype=jnp.bool_),
        food=jnp.zeros((ll, ll), dtype=jnp.uint8),
        hazard=jnp.full((ll, ll), FUEL, dtype=jnp.uint8),
        smoke=jnp.zeros((ll, ll), dtype=jnp.float32),
        structure=jnp.full((ll, ll), INTACT, dtype=jnp.uint8),
        weak=jnp.zeros((ll, ll), dtype=jnp.bool_),
        t=jnp.zeros((), dtype=jnp.int32),
        key=key,
        ep_deaths_fire=jnp.zeros((), dtype=jnp.int32),
        ep_deaths_collapse=jnp.zeros((), dtype=jnp.int32),
        ep_smoke_sum=jnp.zeros((), dtype=jnp.float32),
    )
