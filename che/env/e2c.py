"""E2C micro-environment — the Theorem-1 handshake (theory §5, §10 hook).

Thm. 1's two-corridor environment: start s0, a path of d steps to the
branch b, two disjoint corridors L/R of length ell leading to the goal,
horizon T = d + ell (zero slack), and a fire at depth l_f in corridor
Z ~ U{L, R} that disables any agent entering it. Reward 1 for reaching
the goal by T. Predicted optimal value J*(kappa_B) = 1/2 + q(kappa_B)/2
with q = P(the burning corridor is revealed in the crop at some
pre-commitment step); the memorizing (signal-blind) policy sits at 1/2
for every kappa_B, so the memorization gap is exactly q/2.

**The agent's only information channel is the production Coupling-B code
path.** The smoke field evolves by `hazard.smoke_step` and observations
come from `observation.observe` at obs v3 — the same crop, the same
shared `transmittance`, the same per-cell reveal draw, the same
`env._OBS_STREAM` fold_in the swarm env uses. No bespoke signal channel
exists here; if the crop offsets, the plane order or the reveal plumbing
were wrong, the hand-coded policy would stop seeing the fire and J*
would collapse onto the 1/2 floor.

Geometry (Option A, human ruling 2026-07-27 — `docs/decision_log.md`):
d = 2, l_f = 2, ell = 4, k = 9, which respects the phase-prompt rule
k >= 2(d + l_f) + 1. The prompt's *illustrative* d = 6 / k = 17 was
measured to be unusable: with a single-cell smoke source the n_quad = 4
midpoint quadrature never samples the ray's endpoint beyond axis
distance ~4, so tau == 1 *exactly* at the first two steps and hence
q == 1 for every kappa_B — a flat J* = 1 curve, with the acceptance
criterion `J*(large) - 1/2 <= 0.02` unreachable. Shrinking the geometry
puts every pre-commitment distance (2.83, 2.24, 2.00) inside the
well-sampled regime. This is recorded as a documented kernel property,
not a bug (see `observation.transmittance`); an endpoint-inclusive
quadrature (Option C) was considered and rejected — it would re-open
locked M4.1, invalidate the fresh bench row, and change obs-v3 semantics
to serve a regime production rarely enters.

Residual side channel (M4.2 Finding 2, quantified in `phase4_report.md`):
smoke is co-located with the fire, so the ray to the *mirror* corridor
cell crosses no smoke and that cell is always revealed. "Exactly one
candidate masked" therefore identifies Z from the visibility plane
alone, without ever seeing fire content. Thm. 1 idealizes that away, so
the policies scored against the theorem read **content planes only**
(burning, smoke); the plane-7 oracle is measured separately and reported
as the size of the side channel, never as J*.

DECISION (scripted hazard): the fire cell is held Burning for the whole
episode rather than run through the CA. Thm. 1 defines E2C structurally
("corridor Z burns at depth l_f", lethal throughout) and the CA kernel
is validated elsewhere (Prop. 2 percolation, Prop. 3 Coupling A); what
this milestone must validate is the *observation* path. Def. 3's
one-step burn-out would make corridor Z safe from t = 1 and delete the
theorem's hypothesis.

DECISION (one smoke step before the first observation): the fire has
been burning since t = 0, so the first observation already sees one
emission. Without it rho_0 == 0 => tau_0 == 1 => q == 1 trivially, for
every kappa_B. The prediction MC mirrors this protocol exactly (M3.3
lesson: predicted and empirical must share every constant).

DECISION (one goal cell per corridor): Thm. 1's single goal reachable by
two disjoint corridors is realized as the far end of each corridor
(mirror-symmetric). With zero slack the agent commits once and walks, so
the two formulations are behaviourally identical.
"""

import dataclasses
import functools

import chex
import jax
import jax.numpy as jnp
import numpy as np

from che.env.config import EnvConfig, ThetaConfig
from che.env.env import _OBS_STREAM
from che.env.hazard import smoke_step
from che.env.observation import observe, transmittance
from che.env.types import BURNING, FUEL, zeros_state

# --- Geometry (Option A; every pre-commitment distance <= 4) -------------
D_PATH = 2  # d: steps from s0 to the branch b
L_F = 2  # l_f: fire depth into corridor Z
CORRIDOR_LEN = 4  # ell: corridor length; the goal is its far end
K_OBS = 9  # k: >= 2 * (d + l_f) + 1 = 9 (phase-prompt rule)
GRID = 13  # arena side; keeps the whole pre-commitment crop in-grid
HORIZON = D_PATH + CORRIDOR_LEN  # T: zero slack
B_ROW = GRID // 2  # branch cell (row, col); the approach runs down the
B_COL = GRID // 2  # column, the corridors along the row

# Corridor sides as signed column directions: -1 = L, +1 = R.
SIDE_L = -1
SIDE_R = 1

# (sigma_s, eta) are the env family's long-standing values and are read
# from the shared defaults rather than restated — the phase-4 prompt's
# note applies: optical depth is the product kappa_B * rho, so sweeping
# kappa_B alone is fully general and the smoke constants must not drift
# between the micro-env and the swarm env.
_THETA_DEFAULTS = ThetaConfig()
SIGMA_S = _THETA_DEFAULTS.sigma_s
ETA = _THETA_DEFAULTS.eta


def e2c_config(kappa_B: float) -> EnvConfig:
    """The micro-env's own EnvConfig — obs v3, one agent, its own k."""
    return EnvConfig(
        grid_size=GRID,
        n_agents=1,
        horizon=HORIZON,
        obs_window=K_OBS,
        obs_version=3,
        theta=ThetaConfig(kappa_B=kappa_B),
    )


def fire_cell(z: jax.Array | int) -> tuple[jax.Array, jax.Array]:
    """(row, col) of the sustained fire: depth L_F into corridor `z`."""
    return jnp.int32(B_ROW), jnp.int32(B_COL) + jnp.int32(z) * L_F


def _hazard_field(z: jax.Array | int) -> jax.Array:
    """All-Fuel arena with the corridor-Z fire cell held Burning."""
    row, col = fire_cell(z)
    return jnp.full((GRID, GRID), FUEL, jnp.uint8).at[row, col].set(BURNING)


def _agent_pos(t: jax.Array | int) -> jax.Array:
    """Approach position at pre-commitment step t: d - t cells above b."""
    return jnp.stack(
        [jnp.int32(B_ROW) - D_PATH + jnp.int32(t), jnp.int32(B_COL)]
    )[None, :]


def _candidate_index(
    t: jax.Array | int, side: jax.Array | int
) -> tuple[jax.Array, jax.Array]:
    """Crop index of a candidate fire cell (depth L_F into `side`) as seen
    from the approach position at step t. The crop is centered on the
    agent, so the offset (d - t, side * l_f) lands at r + offset."""
    r = K_OBS // 2
    return (
        jnp.int32(r + D_PATH) - jnp.int32(t),
        jnp.int32(r) + jnp.int32(side) * L_F,
    )


def _content_signal(grid: jax.Array, row: jax.Array, col: jax.Array) -> jax.Array:
    """Coupling-B content channel at one crop cell: burning (plane 0) or
    smoke (plane 2) revealed. Both are gated by the same per-cell reveal
    draw, so they coincide; reading both is the honest "the agent looks
    at the hazard planes" statement. **Plane 7 is deliberately not read**
    — see the module docstring's Finding-2 note."""
    return (grid[row, col, 0] > 0) | (grid[row, col, 2] > 0)


def _visibility(grid: jax.Array, row: jax.Array, col: jax.Array) -> jax.Array:
    """Plane 7 (realized reveal mask) at one crop cell — the side-channel
    oracle's *only* input."""
    return grid[row, col, 7] > 0


def _observation_phase(key: jax.Array, z: jax.Array, cfg: EnvConfig) -> dict:
    """Pre-commitment steps t = 0..d: smoke_step -> observe -> read crop.

    Returns the content-channel belief (`informed`, `seen_side`) and the
    plane-7 oracle's belief (`oracle_evidence`, `oracle_side`).
    """
    hazard = _hazard_field(z)
    template = zeros_state(GRID, 1, key)

    def body(carry, xs):
        smoke, informed_l, informed_r, o_side, o_evid = carry
        t, k = xs
        # Def. 6 / D3 smoke update, then observations from the post-update
        # field — the Prop.-1 order the swarm env uses.
        smoke = smoke_step(smoke, hazard, sigma_s=SIGMA_S, eta=ETA)
        state = dataclasses.replace(
            template, hazard=hazard, smoke=smoke, agent_pos=_agent_pos(t), t=t
        )
        obs = observe(state, cfg, jax.random.fold_in(k, _OBS_STREAM))
        grid = obs["grid"][0]
        row_l, col_l = _candidate_index(t, SIDE_L)
        row_r, col_r = _candidate_index(t, SIDE_R)
        informed_l = informed_l | _content_signal(grid, row_l, col_l)
        informed_r = informed_r | _content_signal(grid, row_r, col_r)
        # Side channel: exactly one candidate masked identifies the smoky
        # side. First evidence wins (all evidence agrees — only the
        # corridor-Z ray carries smoke).
        masked_l = ~_visibility(grid, row_l, col_l)
        masked_r = ~_visibility(grid, row_r, col_r)
        evidence = masked_l ^ masked_r
        side = jnp.where(masked_r, SIDE_R, SIDE_L).astype(jnp.int32)
        o_side = jnp.where(evidence & ~o_evid, side, o_side)
        o_evid = o_evid | evidence
        return (smoke, informed_l, informed_r, o_side, o_evid), None

    init = (
        jnp.zeros((GRID, GRID), jnp.float32),
        jnp.bool_(False),
        jnp.bool_(False),
        jnp.int32(SIDE_L),
        jnp.bool_(False),
    )
    steps = jnp.arange(D_PATH + 1, dtype=jnp.int32)
    (_, informed_l, informed_r, o_side, o_evid), _ = jax.lax.scan(
        body, init, (steps, jax.random.split(key, D_PATH + 1))
    )
    return {
        "informed": informed_l | informed_r,
        # Meaningful only when informed; only the Z side can carry content.
        "seen_side": jnp.where(informed_r, SIDE_R, SIDE_L).astype(jnp.int32),
        "oracle_evidence": o_evid,
        "oracle_side": o_side,
    }


def _walk_alive(direction: jax.Array, z: jax.Array) -> jax.Array:
    """Post-commitment walk: ell steps from b along `direction`. Stepping
    on the burning cell (depth L_F into corridor Z) disables the agent;
    zero slack means the goal is reached exactly at the horizon, so
    success == alive after ell steps."""
    _, fire_col = fire_cell(z)

    def body(carry, _):
        alive, col = carry
        col = col + direction
        return (alive & (col != fire_col), col), None

    (alive, _), _ = jax.lax.scan(
        body,
        (jnp.bool_(True), jnp.int32(B_COL)),
        None,
        length=CORRIDOR_LEN,
    )
    return alive


def episode(key: jax.Array, cfg: EnvConfig) -> dict:
    """One E2C episode under all three policies (common random numbers).

    - **optimal** (Thm. 1): walk to b reading the content channel; if
      informed take the corridor != Z, else tie-break to L.
    - **memorizing**: always L — the signal-blind policy that is optimal
      on the fixed-map variant. Value 1/2 for every kappa_B.
    - **oracle**: guesses Z from the plane-7 mask pattern alone; scored
      only to quantify the side channel.

    The three share the approach (identical positions and observations
    until the commitment) and differ only in the corridor they take.
    """
    k_z, k_obs = jax.random.split(key)
    z = jnp.where(jax.random.bernoulli(k_z), SIDE_R, SIDE_L).astype(jnp.int32)
    belief = _observation_phase(k_obs, z, cfg)
    dir_optimal = jnp.where(belief["informed"], -belief["seen_side"], SIDE_L)
    oracle_guess = jnp.where(
        belief["oracle_evidence"], belief["oracle_side"], SIDE_L
    ).astype(jnp.int32)
    return {
        "success_optimal": _walk_alive(dir_optimal, z),
        "success_memorizing": _walk_alive(jnp.int32(SIDE_L), z),
        "success_oracle": _walk_alive(-oracle_guess, z),
        "oracle_correct": oracle_guess == z,
        "informed": belief["informed"],
        "z_is_right": z == SIDE_R,
    }


def run_episodes(key: jax.Array, cfg: EnvConfig, n_episodes: int) -> dict:
    """`n_episodes` independent E2C episodes, vmapped."""
    batch = jax.jit(jax.vmap(functools.partial(episode, cfg=cfg)))
    return batch(jax.random.split(key, n_episodes))


def tau_profile(cfg: EnvConfig, z: jax.Array | int) -> jax.Array:
    """tau at the fire cell for each pre-commitment step t = 0..d, from
    the shared `transmittance` against the same smoke trajectory the
    rollout sees (same smoke_step protocol, same k, same kappa_B).

    Deterministic: E2C's only randomness is Z and the reveal draws.
    """
    hazard = _hazard_field(z)

    def body(smoke, t):
        smoke = smoke_step(smoke, hazard, sigma_s=SIGMA_S, eta=ETA)
        tau = transmittance(
            smoke, _agent_pos(t), kappa_B=cfg.theta.kappa_B, k=K_OBS
        )
        row, col = _candidate_index(t, z)
        return smoke, tau[0, row, col]

    _, taus = jax.lax.scan(
        body, jnp.zeros((GRID, GRID), jnp.float32), jnp.arange(D_PATH + 1)
    )
    chex.assert_shape(taus, (D_PATH + 1,))
    return taus


def predict_q(key: jax.Array, cfg: EnvConfig, n_mc: int) -> dict:
    """Numeric q(kappa_B) by Monte Carlo over the reveal randomness.

    Mirrors the rollout protocol exactly (same Z draw, same smoke
    trajectory, same shared `transmittance`, same `u < tau` reveal
    convention) but does **not** go through `observe`, and is driven by
    an independent PRNG stream. Both properties are load-bearing: with
    shared keys and a shared code path the acceptance test would reduce
    to the arithmetic identity J = q + (1 - q)/2 (M4.2 ruling, item 3).
    """

    def one(k):
        k_z, k_reveal = jax.random.split(k)
        z = jnp.where(jax.random.bernoulli(k_z), SIDE_R, SIDE_L).astype(jnp.int32)
        taus = tau_profile(cfg, z)
        return (jax.random.uniform(k_reveal, taus.shape) < taus).any()

    informed = jax.jit(jax.vmap(one))(jax.random.split(key, n_mc))
    return {"informed": informed}


def _rate_se(x: jax.Array) -> tuple[float, float]:
    """Bernoulli mean and its standard error."""
    a = np.asarray(x, dtype=np.float64)
    p = float(a.mean())
    return p, float(np.sqrt(max(p * (1.0 - p), 0.0) / a.size))


def sweep_point(
    key: jax.Array, kappa_B: float, n_episodes: int, n_mc: int
) -> dict:
    """One kappa_B point: empirical curve, numeric prediction, oracle."""
    cfg = e2c_config(kappa_B)
    # Independent streams for the empirical rollouts and the prediction MC.
    k_emp, k_pred = jax.random.split(key)
    emp = run_episodes(k_emp, cfg, n_episodes)
    pred = predict_q(k_pred, cfg, n_mc)

    j_opt, se_opt = _rate_se(emp["success_optimal"])
    j_mem, se_mem = _rate_se(emp["success_memorizing"])
    q_mc, se_q = _rate_se(pred["informed"])
    q_emp, se_q_emp = _rate_se(emp["informed"])
    oracle_acc, se_oracle = _rate_se(emp["oracle_correct"])
    taus = np.asarray(tau_profile(cfg, SIDE_R), dtype=np.float64)
    j_pred = 0.5 + q_mc / 2.0
    se_j_pred = se_q / 2.0
    return {
        "kappa_B": float(kappa_B),
        "n_episodes": int(n_episodes),
        "n_mc": int(n_mc),
        "j_optimal": j_opt,
        "se_j_optimal": se_opt,
        "j_memorizing": j_mem,
        "se_j_memorizing": se_mem,
        "q_mc": q_mc,
        "se_q_mc": se_q,
        # Zero-MC-error cross-check of the MC estimator.
        "q_analytic": float(1.0 - np.prod(1.0 - taus)),
        # q as measured through the full observe() pipeline — a check of
        # the composition (crop offsets, plane order, reveal plumbing),
        # never the predictor (that would be the tautology above).
        "q_empirical": q_emp,
        "se_q_empirical": se_q_emp,
        "j_predicted": j_pred,
        "se_j_predicted": se_j_pred,
        "delta": j_opt - j_pred,
        "se_delta": float(np.hypot(se_opt, se_j_pred)),
        "oracle_accuracy": oracle_acc,
        "se_oracle_accuracy": se_oracle,
        "tau_profile": taus.tolist(),
    }


# Sweep grid: spans q ~ 1 -> q ~ 0, includes kappa_B = 0 and a large point
# (phase-4 prompt M4.2).
KAPPA_GRID = (0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 5.0, 8.0)


def run_sweep(
    key: jax.Array,
    kappas: tuple[float, ...] = KAPPA_GRID,
    n_episodes: int = 8192,
    n_mc: int = 8192,
) -> list[dict]:
    """The M4.2 sweep: one `sweep_point` per kappa_B, independent keys."""
    keys = jax.random.split(key, len(kappas))
    return [
        sweep_point(k, kb, n_episodes, n_mc)
        for k, kb in zip(keys, kappas, strict=True)
    ]
