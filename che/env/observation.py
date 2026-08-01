"""Egocentric observations — obs v3 (M4.1, Coupling B live); v2/v1 archival.

obs v3 = the v2 content planes (below) gated per cell by Beer-Lambert
transmittance through the smoke field (Def. 6), plus an appended
visibility plane:

    7. visibility — the *realized* per-cell reveal mask (1 = seen).
       Agents must be able to distinguish "unseen" from "absent"; zero-
       fill without a mask would conflate them and confound ISO/JOINT
       with an artificial memory burden (M4.1 locked design).

Per-cell stochastic masking: for each cell y in agent i's crop, optical
depth D(i, y) = kappa_B * dist(x_i, y) * mean_rho(ray), with mean_rho an
S=4-point quadrature along the ray through the *current* (post-step)
smoke field; tau = exp(-D); the cell's 7 content planes are revealed
with probability tau, else zeroed. Own cell: dist 0 => tau = 1, always
visible. Own-state vec unaffected. The reveal uniforms are drawn
unconditionally, so kappa_B = 0 => tau == 1 => bitwise-identical
trajectories to the pre-masking env under the same keys (invariant #3).
Schema frozen after M4.1 (Phase 5 adds message inputs, not grid planes).

obs v2 content planes, in order (float32, k x k crops centered on the
agent; all indicators {0, 1} except smoke, which stays continuous):
    0. burning         — 1[hazard == Burning]  (the lethal set)
    1. burnt           — 1[hazard == Burnt]    (cold ash: safe, passable)
    2. smoke           — raw rho (bounded by sigma_s / (1 - e^-eta))
    3. food            — 1[food]
    4. weak            — 1[weak terrain] (M3.1 mask; static per episode.
       DECISION: the raw mask — a collapsed weak cell stays 1 here AND
       sets plane 5; two indicators carry strictly more information than
       v1's collapse-wins tri-level plane)
    5. collapsed       — 1[structure == Collapsed]
    6. alive occupancy — 1 where an alive agent stands (DECISION,
       human-locked: includes the observer itself; the own-state vector
       disambiguates self). Dead agents disappear from this plane —
       they are attrition, not obstacles (M1.1).

Why v2 (D5, 2026-07-20, M3.0b evidence): v1 plane 0 encoded hazard
state / 2, so Burnt (1.0) read *higher* than Burning (0.5) — ash looked
maximally dangerous, and Medium-trained policies abandoned burnt regions
(audit 1) with the matching completion signature in the 3x3 cross matrix
(audit 2). Indicator planes carry no spurious ordinal structure.

obs v1 (M1.2, archival only — no cross-version comparisons, ever):
    0. hazard / 2      — {0, .5, 1} for {Fuel, Burning, Burnt}
    1. smoke           — raw rho
    2. food            — {0, 1}
    3. structure       — {0, .5, 1} for {sound, weak-intact, collapsed}
    4. alive occupancy — as v2 plane 6

Out-of-bounds cells pad 0 on the content planes. The visibility plane is
computed for every crop cell (rays sample out-of-grid smoke as 0), so an
out-of-bounds cell can read "seen and empty" — same conflation v2 already
had, and the own-position vec disambiguates the arena edge.

Own-state vector unchanged: (row/L, col/L, alive, t/horizon).
"""

import math

import chex
import jax
import jax.numpy as jnp
import numpy as np

from che.env.config import EnvConfig
from che.env.tasks import occupancy_grid
from che.env.types import BURNING, BURNT, COLLAPSED, EnvState

# Channel counts. N_PLANES is the *current* (v3) count — networks and
# tests import it instead of hard-coding; archival v1/v2 paths go
# through n_planes(cfg).
N_PLANES = 8
N_PLANES_V2 = 7
N_PLANES_V1 = 5

# S-point quadrature order for the ray integral (M4.1 locked design).
N_QUAD = 4


def n_planes(cfg: EnvConfig) -> int:
    """Channel count for the config's obs_version."""
    return {1: N_PLANES_V1, 2: N_PLANES_V2, 3: N_PLANES}[cfg.obs_version]


def transmittance(
    smoke: jax.Array,
    agent_pos: jax.Array,
    *,
    kappa_B: float,
    k: int,
    n_quad: int = N_QUAD,
) -> jax.Array:
    """Beer-Lambert transmittance tau over each agent's k x k crop (Def. 6).

    tau[a, i, j] = exp(-D) with optical depth D = kappa_B * dist * mean_rho:
    dist the Euclidean cell distance from agent a to crop cell (i, j), and
    mean_rho an n_quad-point midpoint-rule quadrature of the smoke field
    along the ray, t_s = (s + 1/2) / n_quad. DECISION: sample points read
    the nearest cell (rays through the piecewise-constant field; rounding
    is jnp.round, shared by every caller), out-of-grid smoke reads 0.
    Own cell: dist 0 => tau = 1.

    This is THE ONE transmittance code path (M4.1 locked design): the env
    observation kernel, the E2C Thm.-1 validation, and any diagnostic must
    all call it — the theory<->implementation handshake is only meaningful
    if they share the literal code. Do not fork or inline variants.

    **Documented kernel property (M4.2, human-ruled — not a bug).** The
    n_quad midpoint samples never land on the ray's endpoint beyond axis
    distance ~4, so a *single-cell* smoke source contributes no occlusion
    to its own line of sight at longer range: tau == 1 exactly, at any
    kappa_B. Spatially extended smoke — what the CA actually produces —
    is unaffected, and short rays (e.g. the M4.3 detection band at crop
    distance 3) sit inside the well-sampled regime; E2C's geometry is
    sized to stay there (`che/env/e2c.py`). An endpoint-inclusive
    quadrature was considered and rejected at the M4.2 ruling: it would
    re-open locked M4.1, invalidate its bench row, and change obs-v3
    semantics to serve a regime production rarely enters. Pinned by
    tests/test_coupling_b.py.
    """
    chex.assert_rank(smoke, 2)
    chex.assert_type(smoke, jnp.float32)
    chex.assert_shape(agent_pos, (None, 2))
    r = k // 2
    span = jnp.arange(-r, r + 1)
    offs = jnp.stack(jnp.meshgrid(span, span, indexing="ij"), axis=-1)  # [k, k, 2]
    dist = jnp.sqrt((offs.astype(jnp.float32) ** 2).sum(-1))  # [k, k]
    t = (jnp.arange(n_quad, dtype=jnp.float32) + 0.5) / n_quad  # [S]
    samp = jnp.round(t[:, None, None, None] * offs.astype(jnp.float32)).astype(
        jnp.int32
    )  # [S, k, k, 2]; |entries| <= r, so an r-pad covers every gather
    padded = jnp.pad(smoke, r)

    def tau_one(pos: jax.Array) -> jax.Array:
        idx = pos[None, None, None, :] + samp + r
        mean_rho = padded[idx[..., 0], idx[..., 1]].mean(axis=0)  # [k, k]
        return jnp.exp(-kappa_B * dist * mean_rho)

    tau = jax.vmap(tau_one)(agent_pos)
    chex.assert_shape(tau, (agent_pos.shape[0], k, k))
    return tau


def per_agent_masked(grid: jax.Array, cfg: EnvConfig) -> jax.Array:
    """[n_agents] masked share of each agent's crop this step.

    Subtract before averaging: an all-ones visibility plane then yields
    an exact 0.0 (mean-of-ones is 1 - 2^-27 in float32, not 1). Obs
    v1/v2 have no masking, so the share is identically 0 there.
    """
    if cfg.obs_version in (1, 2):  # static branch — config is not traced
        return jnp.zeros((grid.shape[0],), jnp.float32)
    return (1.0 - grid[..., -1]).mean(axis=(-2, -1))


def masked_fraction(grid: jax.Array, alive: jax.Array, cfg: EnvConfig) -> jax.Array:
    """M4.0 harness addendum: per-step masked-crop share for the info dict.

    Mean over *alive* agents of the fraction of crop cells whose content
    planes were masked by Coupling B this step; 0 when no one is alive.
    """
    masked = per_agent_masked(grid, cfg)
    return jnp.where(alive, masked, 0.0).sum() / jnp.maximum(
        alive.sum(dtype=jnp.float32), 1.0
    )


def rho_max(cfg: EnvConfig) -> float:
    """Supremum of the smoke field (Def. 6): rho' = e^-eta rho + sigma_s on a
    permanently burning cell converges to sigma_s / (1 - e^-eta)."""
    return float(cfg.theta.sigma_s / (1.0 - math.exp(-cfg.theta.eta)))


def plane_scales(cfg: EnvConfig) -> tuple[float, ...]:
    """Per-plane upper bound, used as the uint8 quantization scale (M5.1f).

    Every plane is an indicator in {0, 1} — or, on archival v1, an ordinal in
    {0, 0.5, 1} — except smoke, which is continuous on [0, rho_max]. So only
    smoke is genuinely lossy under 8-bit storage; the rest round-trip exactly.
    Smoke sits at index 2 on v2/v3 and index 1 on v1 (see the plane tables
    above); the visibility plane appended by v3 is an indicator.
    """
    n = n_planes(cfg)
    smoke_idx = 1 if cfg.obs_version == 1 else 2
    return tuple(rho_max(cfg) if i == smoke_idx else 1.0 for i in range(n))


def quantize_grid(grid: jax.Array, cfg: EnvConfig) -> jax.Array:
    """float32 crop -> uint8, per-plane scaled (M5.1f uint8 obs storage).

    Activated as the pre-registered contingency (standing rule 2026-07-21).
    The trigger turned out to be capacity rather than speed: at the Phase-6/7
    configuration the float32 population obs trajectory is 11.39 GiB and the
    minibatch permutation copies it, which does not fit a 32 GiB card.

    Quantization is deterministic and consumes no PRNG, so it cannot perturb
    any kernel stream (invariant #3) and the ablation nesting still holds
    bitwise *within* uint8 mode. It is NOT bitwise-comparable across modes:
    a uint8 run and a float32 run of the same seed are different runs, and
    the config hash separates their checkpoints.
    """
    scales = jnp.asarray(plane_scales(cfg), dtype=jnp.float32)
    normed = jnp.clip(grid / scales, 0.0, 1.0)
    return jnp.round(normed * 255.0).astype(jnp.uint8)


def dequantize_grid(grid_u8: jax.Array, scales) -> jax.Array:
    """uint8 -> float32, the in-network half of the contingency.

    `scales` is a plain tuple so callers can hold it as a static attribute
    (see networks.ActorCritic.obs_scale) rather than threading cfg into the
    module.

    The reciprocal is folded on the HOST, in numpy, and the device sees a
    single multiply by a literal. This is not micro-optimization: fp32
    division is *not* correctly rounded on the GPU backend, which lowers it
    to an approximate reciprocal sequence. Dividing on device made a full-
    scale code reconstruct as 0.99999994 instead of 1.0, so an indicator
    plane no longer round-tripped exactly and two M5.1f tests failed on the
    box while passing on CPU (correctly-rounded there). IEEE fp32
    multiplication *is* exact-rounded on both backends and there is no
    addend for XLA to fuse an FMA against, so the host-folded constant makes
    the round trip exact by construction rather than by luck of rounding.
    `test_dequantize_does_no_device_division` guards the property on any
    backend by inspecting the lowered HLO.
    """
    return grid_u8.astype(jnp.float32) * jnp.asarray(
        _recip_scales(scales), dtype=jnp.float32
    )


def _recip_scales(scales) -> tuple[float, ...]:
    """scale/255 per plane, evaluated in host float32 (correctly rounded)."""
    return tuple(
        float(np.float32(s) / np.float32(255.0)) for s in np.atleast_1d(scales)
    )


def observe(
    state: EnvState, cfg: EnvConfig, key: jax.Array | None = None
) -> dict[str, jax.Array]:
    """O_{kappa_B}(. | x', h', rho', c', k'): observations from the
    post-step state (Prop. 1 / CLAUDE.md invariant #2 — call this on the
    *new* state).

    `key` drives the obs v3 per-cell reveal draw (required for v3; the
    caller derives it from a dedicated stream — see env._OBS_STREAM).
    v1/v2 are deterministic and ignore it.

    Returns {"grid": float32 [n_agents, k, k, n_planes(cfg)],
             "vec": float32 [n_agents, 4]}.
    """
    k = cfg.obs_window
    r = k // 2
    n_ch = n_planes(cfg)
    occ = occupancy_grid(state.agent_pos, state.agent_alive, cfg.grid_size)
    if cfg.obs_version in (2, 3):  # static Python branch — config is not traced
        plane_list = [
            (state.hazard == BURNING).astype(jnp.float32),
            (state.hazard == BURNT).astype(jnp.float32),
            state.smoke,
            state.food.astype(jnp.float32),
            state.weak.astype(jnp.float32),
            (state.structure == COLLAPSED).astype(jnp.float32),
            occ.astype(jnp.float32),
        ]
    else:
        plane_list = [
            state.hazard.astype(jnp.float32) / 2.0,
            state.smoke,
            state.food.astype(jnp.float32),
            jnp.where(
                state.structure == COLLAPSED,
                1.0,
                jnp.where(state.weak, 0.5, 0.0),
            ),
            occ.astype(jnp.float32),
        ]
    planes = jnp.stack(plane_list, axis=-1)
    n_content = len(plane_list)
    padded = jnp.pad(planes, ((r, r), (r, r), (0, 0)))

    def crop_one(pos: jax.Array) -> jax.Array:
        # Padded by r, so the slice starting at `pos` is centered on the agent.
        return jax.lax.dynamic_slice(padded, (pos[0], pos[1], 0), (k, k, n_content))

    grid = jax.vmap(crop_one)(state.agent_pos)
    if cfg.obs_version == 3:
        # Coupling B (Def. 6, M4.1): per-cell stochastic masking of the
        # content planes + the realized reveal mask as the final plane.
        # The uniforms are drawn unconditionally (invariant #3): at
        # kappa_B = 0, tau == 1 and u < 1 always, so the mask is all-ones
        # and the content planes are bitwise those of the pre-masking env.
        if key is None:
            raise ValueError("obs v3 requires a PRNG key for the reveal draw")
        # M6.0: kappa_B is traced, per episode, from the state — the mixture
        # varies it. Everything else observe() reads off cfg is static
        # (obs_version, window, grid size) and cannot be varied by a mixture.
        tau = transmittance(
            state.smoke, state.agent_pos, kappa_B=state.theta_live.kappa_B, k=k
        )
        reveal = jax.random.uniform(key, tau.shape) < tau  # P(seen) = tau
        grid = jnp.concatenate(
            [
                grid * reveal[..., None].astype(jnp.float32),
                reveal[..., None].astype(jnp.float32),
            ],
            axis=-1,
        )
    vec = jnp.concatenate(
        [
            state.agent_pos.astype(jnp.float32) / cfg.grid_size,
            state.agent_alive.astype(jnp.float32)[:, None],
            jnp.full(
                (cfg.n_agents, 1), 1.0, dtype=jnp.float32
            ) * state.t.astype(jnp.float32) / cfg.horizon,
        ],
        axis=1,
    )
    chex.assert_shape(grid, (cfg.n_agents, k, k, n_ch))
    chex.assert_shape(vec, (cfg.n_agents, 4))
    return {"grid": grid, "vec": vec}
