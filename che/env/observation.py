"""Egocentric observations: k x k crops of (hazard, smoke, food) planes.

Phase-0 status: crops only. Beer-Lambert attenuation (Coupling B, Def. 6)
enters here in Phase 4 as a transmittance gate on these planes; kappa_B is
already in ThetaConfig so the signature will not change.

DECISION (placeholders until Phase 1 fixes the perception model):
- plane normalization: hazard/2 in {0, .5, 1}; smoke raw (bounded by
  sigma_s / (1 - e^-eta)); food in {0, 1};
- out-of-bounds cells pad with 0 on all planes (reads as Fuel/no-smoke/no
  -food; a dedicated out-of-bounds indicator plane is a Phase 1 option);
- own-state vector: (row/L, col/L, alive, t/horizon).
"""

import chex
import jax
import jax.numpy as jnp

from che.env.config import EnvConfig
from che.env.types import EnvState


def observe(state: EnvState, cfg: EnvConfig) -> dict[str, jax.Array]:
    """O(. | x', h', rho', c', k'): observations from the post-step state
    (Prop. 1 / CLAUDE.md invariant #2 — call this on the *new* state).

    Returns {"grid": float32 [n_agents, k, k, 3], "vec": float32 [n_agents, 4]}.
    """
    k = cfg.obs_window
    r = k // 2
    planes = jnp.stack(
        [
            state.hazard.astype(jnp.float32) / 2.0,
            state.smoke,
            state.food.astype(jnp.float32),
        ],
        axis=-1,
    )
    padded = jnp.pad(planes, ((r, r), (r, r), (0, 0)))

    def crop_one(pos: jax.Array) -> jax.Array:
        # Padded by r, so the slice starting at `pos` is centered on the agent.
        return jax.lax.dynamic_slice(padded, (pos[0], pos[1], 0), (k, k, 3))

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
    chex.assert_shape(grid, (cfg.n_agents, k, k, 3))
    chex.assert_shape(vec, (cfg.n_agents, 4))
    return {"grid": grid, "vec": vec}
