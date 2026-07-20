"""Egocentric observations — obs v2 (D5), v1 kept for archival eval.

obs v2 planes, in order (float32, k x k crops centered on the agent;
all indicators {0, 1} except smoke, which stays continuous):
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

Out-of-bounds cells pad 0 on all planes. Own-state vector unchanged:
(row/L, col/L, alive, t/horizon).

Beer-Lambert attenuation (Coupling B, Def. 6) enters here in Phase 4 as a
transmittance gate on these planes; kappa_B is already in ThetaConfig so
the signature will not change.
"""

import chex
import jax
import jax.numpy as jnp

from che.env.config import EnvConfig
from che.env.tasks import occupancy_grid
from che.env.types import BURNING, BURNT, COLLAPSED, EnvState

# Channel counts. N_PLANES is the *current* (v2) count — networks and
# tests import it instead of hard-coding; the archival v1 path goes
# through n_planes(cfg).
N_PLANES = 7
N_PLANES_V1 = 5


def n_planes(cfg: EnvConfig) -> int:
    """Channel count for the config's obs_version."""
    return N_PLANES if cfg.obs_version == 2 else N_PLANES_V1


def observe(state: EnvState, cfg: EnvConfig) -> dict[str, jax.Array]:
    """O(. | x', h', rho', c', k'): observations from the post-step state
    (Prop. 1 / CLAUDE.md invariant #2 — call this on the *new* state).

    Returns {"grid": float32 [n_agents, k, k, n_planes(cfg)],
             "vec": float32 [n_agents, 4]}.
    """
    k = cfg.obs_window
    r = k // 2
    n_ch = n_planes(cfg)
    occ = occupancy_grid(state.agent_pos, state.agent_alive, cfg.grid_size)
    if cfg.obs_version == 2:  # static Python branch — config is not traced
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
    padded = jnp.pad(planes, ((r, r), (r, r), (0, 0)))

    def crop_one(pos: jax.Array) -> jax.Array:
        # Padded by r, so the slice starting at `pos` is centered on the agent.
        return jax.lax.dynamic_slice(padded, (pos[0], pos[1], 0), (k, k, n_ch))

    grid = jax.vmap(crop_one)(state.agent_pos)
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
