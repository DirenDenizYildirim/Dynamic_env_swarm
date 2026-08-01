"""E2C-2 — the courier variant: Remark-2 VoC validation (theory §5, M5.2).

Remark 2 as originally written was wrong about the denied baseline, and
the correction ran through three drafts in one day (2′, 2″, 2‴). What
survived is narrower and sharper: **communication is load-bearing exactly
when perception fails *and redundancy is unavailable*.** This module
measures that claim rather than restating it.

The environment extends E2C (`che/env/e2c.py`, Thm. 1) with a second
agent, keeping the locked Option-A geometry so every constant is shared
with the Theorem-1 handshake:

    courier (agent 0)  the only agent that can score. Walks the d-step
                       approach to the branch b, commits to a corridor,
                       walks ell. Reward 1 iff it reaches the goal by T.
    scout   (agent 1)  cannot score. Probes corridor L to the fire depth
                       and certifies it, or dies trying.

**Fire-anchored scouting fixes the horizon.** The scout's report is only
worth anything once it has walked *past* the depth at which the fire
sits: surviving one step into L certifies nothing when the fire is at
depth l_f = 2. So the verdict lands at step d + l_f, the courier waits
for it, and then needs ell steps to reach the goal:

    T = d + l_f + ell                       (Q2 ruling, 2026-07-28)

which is Remark 2's original T = d + ell + 1 at l_f = 1. The horizon is
*derived* here (`horizon()`) from the lethality geometry rather than
written down, and `test_e2c.py::test_scout_dies_at_the_fire_anchored_step`
pins the step the derivation rests on.

**Only the message channel carries the scout's fate** (Q1/Q6 rulings).
The courier's scripted policies read the Coupling-B content planes
(burning, smoke) and never plane 6, the alive-occupancy plane — otherwise
it could watch the scout vanish and the "comms" result would be a
perception result wearing a comms hat. `test_e2c2.py` asserts the
blinding by poisoning plane 6.

Delivery goes through the **production comms kernel** (`comms.
in_range_mask` + `comms.sample_links`, Def. 7), not a bespoke coin: the
same reason E2C routes perception through the production `observe`. If
the link kernel's range test or its delta convention were wrong, the free
arm would stop hitting 1 and this milestone would fail loudly.

The four scripted arms
----------------------
- **free** (delta = 0): act on the delivered bit; silence means the scout
  died, which identifies Z. J = 1 at every kappa_B — messages are not
  attenuated by smoke (Def. 7: T_K does not depend on h).
- **denied, pinned** (ignores messages, commits at b on step d): M4.2's
  commit schedule exactly, so J = 1/2 + q(kappa_B)/2 with the *same* q
  the Theorem-1 handshake predicts. **This is the acceptance gate** — it
  is the arm that is exactly predictable.
- **denied + dawdle** (ignores messages, spends the l_f slack steps
  idling, commits at d + l_f): J = 1/2 + q~/2, q~ >= q. Remark 2″'s
  residual, measured instead of reasoned around.
- **coverage** (team-any reward, no messages): the two agents split the
  corridors, so one of them always survives and J = 1 under total denial.
  Remark 2′(i) as a picture: with interchangeable expendable agents at
  least as numerous as the hypotheses, VoC collapses to zero. It is a
  *different reward* and never enters VoC.

VoC is reported twice, per the round-2 ruling:

    VoC_gated = 1/2 (1 - q)     protocol-matched, exactly predictable
    VoC_true  = 1/2 (1 - q~)    measured against the true denied optimum

Why the dawdle maximum is the denied *optimum* and not a lower bound
--------------------------------------------------------------------
Two lines, as ruled. (1) While uninformed, the courier's information
state is exactly the step index t: every observation so far returned "no
evidence", which is a deterministic function of t, so there is nothing
else to condition on. (2) Once informed it commits immediately — further
observation cannot change a decision that is already correct, and the
horizon is tight. So an optimal denied policy is a *choice of where to
spend the l_f idle steps*, i.e. open-loop, and `idle_schedules()`
enumerates that family exhaustively (C(d + l_f, l_f) = 6 members). The
maximum over the family is therefore the optimum, and 1/2 + q~/2 is an
equality.
"""

import dataclasses
import functools
import itertools

import chex
import jax
import jax.numpy as jnp
import numpy as np

from che.env.comms import in_range_mask, sample_links
from che.env.config import EnvConfig, ThetaConfig
from che.env.e2c import (
    B_COL,
    B_ROW,
    CORRIDOR_LEN,
    D_PATH,
    ETA,
    GRID,
    K_OBS,
    L_F,
    SIDE_L,
    SIDE_R,
    SIGMA_S,
    _content_signal,
    _hazard_field,
    _walk_alive,
)
from che.env.env import _OBS_STREAM
from che.env.hazard import smoke_step
from che.env.observation import observe, transmittance
from che.env.types import theta_live_from, zeros_state

# The private helpers above are imported deliberately rather than copied.
# M3.3's lesson is that predicted and empirical must share every constant;
# E2C-2 and E2C must share the arena, the fire placement, the content
# channel and the walk, or a divergence between them would be
# uninterpretable.

# --- Derived horizon (Q2 ruling) ----------------------------------------


def scout_verdict_step() -> int:
    """Step at which the scout's fate is determinate.

    The scout reaches the branch at d and then walks into corridor L. Its
    survival is informative only once it has stepped *onto* the depth
    where a fire would be, which is l_f steps in. Deriving this — rather
    than asserting a slack of 1 — is what makes the horizon fire-anchored.
    """
    return D_PATH + L_F


def horizon() -> int:
    """T = d + l_f + ell: wait for the verdict, then walk the corridor."""
    return scout_verdict_step() + CORRIDOR_LEN


E2C2_HORIZON = horizon()

# The courier's commit schedules, as sequences of distance-from-branch.
# Pinned reproduces M4.2 exactly: approach, commit on arrival at b.
PINNED_SCHEDULE: tuple[int, ...] = tuple(range(D_PATH, -1, -1))


def idle_schedules() -> tuple[tuple[int, ...], ...]:
    """The full open-loop idle-placement family (round-2 ruling item 2).

    Every way of spending the l_f slack steps during the approach: choose
    which d of the d + l_f steps are moves, the rest are idles. Returns
    distance-from-branch sequences of length d + l_f + 1, each starting at
    d and ending at 0. C(d + l_f, l_f) = 6 members at the locked geometry.

    Idling early observes from farther away but through thinner smoke;
    idling late is closer but later, and the smoke has been accumulating.
    Which wins is a measurement, not an intuition — that is the point.
    """
    out = []
    for moves in itertools.combinations(range(D_PATH + L_F), D_PATH):
        dist, seq = D_PATH, [D_PATH]
        for s in range(D_PATH + L_F):
            dist -= 1 if s in moves else 0
            seq.append(dist)
        out.append(tuple(seq))
    return tuple(out)


IDLE_SCHEDULES = idle_schedules()


def e2c2_config(kappa_B: float, delta: float) -> EnvConfig:
    """The micro-env's EnvConfig: obs v3, two agents, its own k and T."""
    return EnvConfig(
        grid_size=GRID,
        n_agents=2,
        horizon=E2C2_HORIZON,
        obs_window=K_OBS,
        obs_version=3,
        theta=ThetaConfig(kappa_B=kappa_B, delta=delta),
    )


# --- Kinematics ---------------------------------------------------------


def scout_alive(t: jax.Array | int, z: jax.Array | int) -> jax.Array:
    """The scout probes corridor L; it dies iff Z = L, at step d + l_f.

    Corridors are exchangeable (`test_corridors_are_exchangeable`), so
    fixing the probed side to L costs no generality.
    """
    doomed = jnp.asarray(z) == SIDE_L
    return ~(doomed & (jnp.asarray(t) >= scout_verdict_step()))


def _scout_col(t: jax.Array | int) -> jax.Array:
    """Scout column: with the courier until b, then l_f steps into L."""
    into = jnp.maximum(jnp.asarray(t, jnp.int32) - D_PATH, 0)
    return jnp.int32(B_COL) + jnp.int32(SIDE_L) * jnp.minimum(into, L_F)


def _positions(
    t: jax.Array | int, dist: jax.Array | int, z: jax.Array | int
) -> jax.Array:
    """(2, 2) agent positions: courier `dist` cells above b, scout probing."""
    del z  # the scout's path does not depend on Z; only its survival does
    courier = jnp.stack(
        [jnp.int32(B_ROW) - jnp.asarray(dist, jnp.int32), jnp.int32(B_COL)]
    )
    scout_row = jnp.int32(B_ROW) - jnp.maximum(
        jnp.int32(D_PATH) - jnp.asarray(t, jnp.int32), 0
    )
    scout = jnp.stack([scout_row, _scout_col(t)])
    return jnp.stack([courier, scout])


def _candidate_index(
    dist: jax.Array | int, side: jax.Array | int
) -> tuple[jax.Array, jax.Array]:
    """Crop index of the candidate fire cell on `side`, from distance `dist`.

    The crop is centered on the courier, which sits `dist` cells above b,
    so b is at row r + dist and the candidate at column r + side * l_f.
    """
    r = K_OBS // 2
    return (
        jnp.int32(r) + jnp.asarray(dist, jnp.int32),
        jnp.int32(r) + jnp.asarray(side, jnp.int32) * L_F,
    )


# --- Perception and delivery -------------------------------------------


def _observation_phase(
    key: jax.Array, z: jax.Array, cfg: EnvConfig, schedule: tuple[int, ...]
) -> dict:
    """Walk `schedule`, stepping smoke then observing, exactly as E2C does.

    Reads the content planes only (burning, smoke) — never plane 6, and
    never plane 7 (the M4.2 Finding-2 side channel).
    """
    hazard = _hazard_field(z)
    template = zeros_state(GRID, 2, key, theta_live_from(cfg.theta))
    sched = jnp.asarray(schedule, jnp.int32)

    def body(carry, xs):
        smoke, inf_l, inf_r = carry
        t, dist, k = xs
        # Def. 6 / D3 smoke update, then observe the post-update field —
        # the Prop.-1 order.
        smoke = smoke_step(smoke, hazard, sigma_s=SIGMA_S, eta=ETA)
        state = dataclasses.replace(
            template,
            hazard=hazard,
            smoke=smoke,
            agent_pos=_positions(t, dist, z),
            agent_alive=jnp.stack([jnp.bool_(True), scout_alive(t, z)]),
            t=t,
        )
        obs = observe(state, cfg, jax.random.fold_in(k, _OBS_STREAM))
        grid = obs["grid"][0]  # the courier's crop
        row_l, col_l = _candidate_index(dist, SIDE_L)
        row_r, col_r = _candidate_index(dist, SIDE_R)
        inf_l = inf_l | _content_signal(grid, row_l, col_l)
        inf_r = inf_r | _content_signal(grid, row_r, col_r)
        return (smoke, inf_l, inf_r), None

    n = len(schedule)
    init = (jnp.zeros((GRID, GRID), jnp.float32), jnp.bool_(False), jnp.bool_(False))
    (_, inf_l, inf_r), _ = jax.lax.scan(
        body,
        init,
        (jnp.arange(n, dtype=jnp.int32), sched, jax.random.split(key, n)),
    )
    return {
        "informed": inf_l | inf_r,
        # Meaningful only when informed; only the Z side can carry content.
        "seen_side": jnp.where(inf_r, SIDE_R, SIDE_L).astype(jnp.int32),
    }


def _message_delivered(key: jax.Array, z: jax.Array, cfg: EnvConfig) -> jax.Array:
    """Did the scout's certification reach the courier at the verdict step?

    Through the production Def.-7 kernel. A dead scout is dropped by
    `in_range_mask`'s alive test, so "silence" covers both causes — death
    and link loss — and only delta = 0 makes silence unambiguous. That is
    exactly the courier's epistemic situation and is not smoothed over.
    """
    t = scout_verdict_step()
    alive = jnp.stack([jnp.bool_(True), scout_alive(t, z)])
    pos = _positions(t, jnp.int32(0), z)  # the courier is waiting at b
    links = sample_links(
        key, in_range_mask(pos, alive, cfg.theta.r_comm), cfg.theta.delta
    )
    return links[1, 0]  # scout -> courier


# --- Episode ------------------------------------------------------------


def episode(key: jax.Array, cfg: EnvConfig, schedule: tuple[int, ...]) -> dict:
    """One E2C-2 episode under all four arms, common random numbers.

    The arms share Z and the link draw; the two denied observation windows
    get independent streams because they are different protocols observing
    at different places and times.
    """
    k_z, k_pin, k_dawdle, k_link = jax.random.split(key, 4)
    z = jnp.where(jax.random.bernoulli(k_z), SIDE_R, SIDE_L).astype(jnp.int32)

    pinned = _observation_phase(k_pin, z, cfg, PINNED_SCHEDULE)
    dawdled = _observation_phase(k_dawdle, z, cfg, schedule)
    delivered = _message_delivered(k_link, z, cfg)

    # Content-channel commitment (M4.2's rule): avoid the side seen to
    # carry hazard; tie-break L when uninformed.
    dir_pinned = jnp.where(pinned["informed"], -pinned["seen_side"], SIDE_L)
    dir_dawdle = jnp.where(dawdled["informed"], -dawdled["seen_side"], SIDE_L)

    # Free arm: a delivered certification says "L is safe"; silence at
    # delta = 0 says the scout died in L, so Z = L and R is safe.
    dir_free = jnp.where(delivered, jnp.int32(SIDE_L), jnp.int32(SIDE_R))
    # If a message could have been lost rather than never sent, the courier
    # is no better off than the pinned policy; at delta = 0 this branch is
    # unreachable and `test_free_arm_collapses_onto_pinned_under_denial`
    # pins the delta = 1 end.
    dir_free = jnp.where(
        (cfg.theta.delta > 0.0) & ~delivered, dir_pinned, dir_free
    )

    return {
        "success_free": _walk_alive(dir_free, z),
        "success_pinned": _walk_alive(dir_pinned, z),
        "success_dawdle": _walk_alive(dir_dawdle, z),
        # Team-any coverage: the agents split the corridors, so exactly one
        # of them survives — under any delta, without a single message.
        "success_coverage": _walk_alive(jnp.int32(SIDE_L), z)
        | _walk_alive(jnp.int32(SIDE_R), z),
        "delivered": delivered,
        "informed_pinned": pinned["informed"],
        "informed_dawdle": dawdled["informed"],
        "z_is_right": z == SIDE_R,
    }


def run_episodes(
    key: jax.Array, cfg: EnvConfig, n_episodes: int, schedule: tuple[int, ...]
) -> dict:
    """`n_episodes` independent E2C-2 episodes, vmapped."""
    batch = jax.jit(jax.vmap(functools.partial(episode, cfg=cfg, schedule=schedule)))
    return batch(jax.random.split(key, n_episodes))


# --- Prediction ---------------------------------------------------------


def tau_profile(
    cfg: EnvConfig, z: jax.Array | int, schedule: tuple[int, ...]
) -> jax.Array:
    """tau at the fire cell for each step of `schedule`, from the shared
    `transmittance` against the same smoke trajectory the rollout sees."""
    hazard = _hazard_field(z)
    sched = jnp.asarray(schedule, jnp.int32)

    def body(smoke, xs):
        t, dist = xs
        smoke = smoke_step(smoke, hazard, sigma_s=SIGMA_S, eta=ETA)
        pos = _positions(t, dist, z)[:1]  # the courier only
        tau = transmittance(smoke, pos, kappa_B=cfg.theta.kappa_B, k=K_OBS)
        row, col = _candidate_index(dist, z)
        return smoke, tau[0, row, col]

    n = len(schedule)
    _, taus = jax.lax.scan(
        body,
        jnp.zeros((GRID, GRID), jnp.float32),
        (jnp.arange(n, dtype=jnp.int32), sched),
    )
    chex.assert_shape(taus, (n,))
    return taus


def predict_q(
    key: jax.Array, cfg: EnvConfig, n_mc: int, schedule: tuple[int, ...]
) -> jax.Array:
    """Numeric q for a schedule by MC over the reveal randomness.

    Mirrors the rollout protocol exactly but does not go through
    `observe`, and runs on an independent stream — both load-bearing, or
    the acceptance test would collapse to the identity J = q + (1-q)/2
    (M4.2 ruling, item 3).
    """

    def one(k):
        k_z, k_reveal = jax.random.split(k)
        z = jnp.where(jax.random.bernoulli(k_z), SIDE_R, SIDE_L).astype(jnp.int32)
        taus = tau_profile(cfg, z, schedule)
        return (jax.random.uniform(k_reveal, taus.shape) < taus).any()

    return jax.jit(jax.vmap(one))(jax.random.split(key, n_mc))


def _rate_se(x) -> tuple[float, float]:
    """Bernoulli mean and its standard error."""
    a = np.asarray(x, dtype=np.float64)
    p = float(a.mean())
    return p, float(np.sqrt(max(p * (1.0 - p), 0.0) / a.size))


def sweep_point(
    key: jax.Array, kappa_B: float, n_episodes: int, n_mc: int
) -> dict:
    """One kappa_B point: all four arms, both delta ends, the idle family.

    The denied arms never read a message, so they are delta-independent by
    construction and are measured once. The free arm is measured at both
    delta = 0 (where it should sit at 1) and delta = 1 (where it must
    collapse exactly onto pinned).
    """
    cfg0 = e2c2_config(kappa_B, delta=0.0)
    cfg1 = e2c2_config(kappa_B, delta=1.0)
    k_free, k_den, k_pred, k_fam = jax.random.split(key, 4)

    # delta = 0 and delta = 1 share the episode key, so the arms differ
    # only through the link draw — the cleanest possible contrast.
    free0 = run_episodes(k_free, cfg0, n_episodes, PINNED_SCHEDULE)
    free1 = run_episodes(k_free, cfg1, n_episodes, PINNED_SCHEDULE)
    den = run_episodes(k_den, cfg1, n_episodes, PINNED_SCHEDULE)

    j_free, se_free = _rate_se(free0["success_free"])
    j_free_denied, _ = _rate_se(free1["success_free"])
    j_pinned, se_pinned = _rate_se(den["success_pinned"])
    j_cov, se_cov = _rate_se(den["success_coverage"])
    q_emp, se_q_emp = _rate_se(den["informed_pinned"])

    q_mc, se_q = _rate_se(predict_q(k_pred, cfg1, n_mc, PINNED_SCHEDULE))
    taus_pin = np.asarray(tau_profile(cfg1, SIDE_R, PINNED_SCHEDULE), np.float64)

    # The open-loop idle family, each member measured and predicted.
    fam_keys = jax.random.split(k_fam, len(IDLE_SCHEDULES))
    family = []
    for sched, k in zip(IDLE_SCHEDULES, fam_keys, strict=True):
        k_emp, k_mc = jax.random.split(k)
        ep = run_episodes(k_emp, cfg1, n_episodes, sched)
        j_d, se_d = _rate_se(ep["success_dawdle"])
        qt_mc, se_qt = _rate_se(predict_q(k_mc, cfg1, n_mc, sched))
        taus = np.asarray(tau_profile(cfg1, SIDE_R, sched), np.float64)
        family.append(
            {
                "schedule": list(sched),
                "j_dawdle": j_d,
                "se_j_dawdle": se_d,
                "q_tilde_mc": qt_mc,
                "se_q_tilde_mc": se_qt,
                "q_tilde_analytic": float(1.0 - np.prod(1.0 - taus)),
            }
        )
    best = max(family, key=lambda r: r["q_tilde_analytic"])

    j_pred = 0.5 + q_mc / 2.0
    return {
        "kappa_B": float(kappa_B),
        "n_episodes": int(n_episodes),
        "n_mc": int(n_mc),
        # Arms.
        "j_free": j_free,
        "se_j_free": se_free,
        "j_free_denied": j_free_denied,
        "j_pinned": j_pinned,
        "se_j_pinned": se_pinned,
        "j_coverage": j_cov,
        "se_j_coverage": se_cov,
        # The gate: pinned vs the M4.2 prediction.
        "q_mc": q_mc,
        "se_q_mc": se_q,
        "q_analytic": float(1.0 - np.prod(1.0 - taus_pin)),
        "q_empirical": q_emp,
        "se_q_empirical": se_q_emp,
        "j_predicted": j_pred,
        "se_j_predicted": se_q / 2.0,
        "delta_gate": j_pinned - j_pred,
        "se_delta_gate": float(np.hypot(se_pinned, se_q / 2.0)),
        # The dawdle family and its maximum.
        "family": family,
        "q_tilde": best["q_tilde_mc"],
        "q_tilde_analytic": best["q_tilde_analytic"],
        "j_dawdle_best": best["j_dawdle"],
        "best_schedule": best["schedule"],
        # VoC, both ways (round-2 ruling item 1).
        "voc_gated": 0.5 * (1.0 - q_mc),
        "voc_true": 0.5 * (1.0 - best["q_tilde_mc"]),
        "voc_measured": j_free - j_pinned,
        "tau_profile": taus_pin.tolist(),
    }


# Same grid as the Theorem-1 sweep: spans q ~ 1 -> q ~ 0, includes
# kappa_B = 0 and a large point, so the two figures are comparable.
KAPPA_GRID = (0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 5.0, 8.0)


def run_sweep(
    key: jax.Array,
    kappas: tuple[float, ...] = KAPPA_GRID,
    n_episodes: int = 4096,
    n_mc: int = 8192,
) -> list[dict]:
    """The M5.2 sweep: one `sweep_point` per kappa_B, independent keys."""
    keys = jax.random.split(key, len(kappas))
    return [
        sweep_point(k, kb, n_episodes, n_mc)
        for k, kb in zip(keys, kappas, strict=True)
    ]
