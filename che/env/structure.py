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


def generate_weak_mask(
    key: jax.Array, grid_size: int, *, f_weak: float, n_smooth: int
) -> jax.Array:
    """M3.1 weak-cell terrain mask (Def. 5 substrate).

    Uniform noise, `n_smooth` 3x3 box-smoothing passes (edge-padded), then
    thresholded at the f_weak-quantile of the smoothed field, so a fraction
    ~f_weak of cells is weak and spatially clustered. Sampled once per
    episode at reset from a dedicated stream; the noise is drawn
    unconditionally even at f_weak = 0 (invariant #3), where the
    below-minimum threshold yields an empty mask.
    """
    x = jax.random.uniform(key, (grid_size, grid_size))
    for _ in range(n_smooth):  # static unroll — a fixed stencil, no cell loop
        p = jnp.pad(x, 1, mode="edge")
        x = (
            sum(
                p[i : i + grid_size, j : j + grid_size]
                for i in (0, 1, 2)
                for j in (0, 1, 2)
            )
            / 9.0
        )
    return x < jnp.quantile(x, f_weak)


def structure_step(
    key: jax.Array,
    structure: jax.Array,
    weak: jax.Array,
    load: jax.Array,
    *,
    lambda_0: float,
    lambda_load: float,
) -> jax.Array:
    """T_C (Def. 5, M3.1): weak intact cell g collapses w.p. lambda(g) =
    lambda_0 * weak(g) + lambda_load * weak(g) * load(g); non-weak cells
    never collapse; collapsed is absorbing. `load` is the (pre-step)
    alive-agent occupancy grid — T_C reads x, not x' (Prop. 1 order).
    """
    chex.assert_rank(structure, 2)
    chex.assert_type(structure, jnp.uint8)
    chex.assert_type(weak, jnp.bool_)
    chex.assert_equal_shape([structure, weak, load])
    # Invariant #3: uniforms drawn even when both lambdas are 0.
    u = jax.random.uniform(key, structure.shape)
    p = (lambda_0 + lambda_load * load) * weak.astype(jnp.float32)
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
