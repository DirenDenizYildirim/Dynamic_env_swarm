"""Collapse dynamics T_C and the Coupling A impulse (Def. 5).

Phase-0 status: the full sampling path is implemented and runs every step
(so the M0.4 gate measures its real cost, and the PRNG stream is fixed from
day one per invariant #3), but debug/reference configs set lambda_0 =
lambda_load = kappa_A = 0, making it inert. Calibration and the Prop. 3
linear-scaling test are Phase 3 deliverables.
"""

import chex
import jax
import jax.numpy as jnp

from che.env.types import COLLAPSED, INTACT


def dilate(mask: jax.Array, radius: int) -> jax.Array:
    """Chebyshev dilation: True within `radius` (L-inf) of a True cell."""
    chex.assert_rank(mask, 2)
    w = 2 * radius + 1
    hits = jax.lax.reduce_window(
        mask.astype(jnp.int32),
        jnp.array(0, jnp.int32),
        jax.lax.max,
        window_dimensions=(w, w),
        window_strides=(1, 1),
        padding="SAME",
    )
    return hits > 0


def structure_step(
    key: jax.Array,
    structure: jax.Array,
    load: jax.Array,
    *,
    lambda_0: float,
    lambda_load: float,
) -> jax.Array:
    """T_C (Def. 5): intact cell g collapses w.p. lambda_0 + lambda_load *
    load(g); collapsed is absorbing. `load` is the (pre-step) alive-agent
    occupancy grid — T_C reads x, not x' (Prop. 1 order).
    """
    chex.assert_rank(structure, 2)
    chex.assert_type(structure, jnp.uint8)
    chex.assert_equal_shape([structure, load])
    # Invariant #3: uniforms drawn even when both lambdas are 0.
    u = jax.random.uniform(key, structure.shape)
    p = lambda_0 + lambda_load * load
    collapse_now = (structure == INTACT) & (u < p)
    return jnp.where(collapse_now, jnp.uint8(COLLAPSED), structure).astype(jnp.uint8)


def coupling_a_seed_mask(
    key: jax.Array,
    collapse_increment: jax.Array,
    *,
    kappa_A: float,
    r_seed: int,
) -> jax.Array:
    """Coupling A (Def. 5): each cell in the seeding neighborhood N_A of a
    new collapse (Chebyshev radius r_seed) ignites independently w.p.
    kappa_A. `collapse_increment` is the boolean mask of c' - c, i.e. cells
    that collapsed *this step* — T_H reads the increment, not the stock.
    Returns the candidate ignition mask; `hazard.seed_ignitions` applies it
    to Fuel cells only.
    """
    chex.assert_rank(collapse_increment, 2)
    chex.assert_type(collapse_increment, jnp.bool_)
    # Invariant #3: uniforms drawn even when kappa_A == 0.
    u = jax.random.uniform(key, collapse_increment.shape)
    near_new_collapse = dilate(collapse_increment, r_seed)
    return near_new_collapse & (u < kappa_A)
