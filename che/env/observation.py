"""Egocentric observations, obs v1 (M1.2 — the locked perception model).

Planes, in order (all float32, k x k crops centered on the agent):
    0. hazard / 2      — {0, .5, 1} for {Fuel, Burning, Burnt}
    1. smoke           — raw rho (bounded by sigma_s / (1 - e^-eta))
    2. food            — {0, 1}
    3. structure       — {0, .5, 1} for {sound, weak-intact, collapsed}
       (M3.1 DECISION: the weak mask is observable — risk-aware locomotion
       is the interesting behavior; a blind variant is a later ablation)
    4. alive occupancy — 1 where an alive agent stands (DECISION,
       human-locked: includes the observer itself; the own-state vector
       disambiguates self). Dead agents disappear from this plane —
       they are attrition, not obstacles (M1.1).

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
from che.env.types import COLLAPSED, EnvState

# Number of observation planes (obs v1). Networks and tests import this
# instead of hard-coding the channel count.
N_PLANES = 5


def observe(state: EnvState, cfg: EnvConfig) -> dict[str, jax.Array]:
    """O(. | x', h', rho', c', k'): observations from the post-step state
    (Prop. 1 / CLAUDE.md invariant #2 — call this on the *new* state).

    Returns {"grid": float32 [n_agents, k, k, N_PLANES],
             "vec": float32 [n_agents, 4]}.
    """
    k = cfg.obs_window
    r = k // 2
    occ = occupancy_grid(state.agent_pos, state.agent_alive, cfg.grid_size)
    planes = jnp.stack(
        [
            state.hazard.astype(jnp.float32) / 2.0,
            state.smoke,
            state.food.astype(jnp.float32),
            jnp.where(
                state.structure == COLLAPSED,
                1.0,
                jnp.where(state.weak, 0.5, 0.0),
            ),
            occ.astype(jnp.float32),
        ],
        axis=-1,
    )
    padded = jnp.pad(planes, ((r, r), (r, r), (0, 0)))

    def crop_one(pos: jax.Array) -> jax.Array:
        # Padded by r, so the slice starting at `pos` is centered on the agent.
        return jax.lax.dynamic_slice(padded, (pos[0], pos[1], 0), (k, k, N_PLANES))

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
    chex.assert_shape(grid, (cfg.n_agents, k, k, N_PLANES))
    chex.assert_shape(vec, (cfg.n_agents, 4))
    return {"grid": grid, "vec": vec}
