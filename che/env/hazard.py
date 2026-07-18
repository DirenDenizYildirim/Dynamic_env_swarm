"""CA fire kernel (Def. 3) and smoke field (Def. 6).

PRNG discipline (CLAUDE.md invariant #3): every stochastic branch consumes
its uniforms unconditionally — with beta = 0 or iota = 0 the same number of
random draws happen and every comparison is simply never true, so setting a
parameter to zero recovers the nested model bitwise under identical keys.

Sampling scheme vs. Prop. 2 (bond percolation): Def. 3 asks for independent
ignition attempts per ordered pair (Burning cell g, Fuel neighbor g'). We
sample one uniform per cell per incoming direction, u[d, g']; the ordered
pair (g -> g') maps bijectively to the slot (g', direction of g from g'), so
per-ordered-pair independence is exact, not approximate. Moreover, with the
constant-burn-time-1 kernel each *unordered* edge sees at most one attempt
over the whole trajectory (an attempt needs one Burning and one Fuel
endpoint, and the Burning one is Burnt afterwards), so these uniforms also
realize the per-edge Bernoulli variables of Prop. 2's coupling exactly.
"""

import chex
import jax
import jax.numpy as jnp

from che.env.types import BURNING, BURNT, FUEL

# Von Neumann neighborhood: offsets (dr, dc) of the 4 neighbors.
_NEIGHBOR_OFFSETS = ((-1, 0), (1, 0), (0, -1), (0, 1))


def _shifted(mask: jax.Array, dr: int, dc: int) -> jax.Array:
    """shifted[i, j] = mask[i + dr, j + dc], False outside the grid.

    Zero padding makes the boundary permanently non-burning (no wraparound).
    """
    padded = jnp.pad(mask, 1, constant_values=False)
    ll, lc = mask.shape
    return padded[1 + dr : 1 + dr + ll, 1 + dc : 1 + dc + lc]


def hazard_step(
    key: jax.Array, hazard: jax.Array, *, beta: float, iota: float = 0.0
) -> jax.Array:
    """One fire-CA transition h' ~ T_H (Def. 3).

    Each Burning cell independently ignites each Fuel von-Neumann neighbor
    w.p. beta; each Fuel cell spontaneously ignites w.p. iota; Burning
    becomes Burnt after exactly one step; Burnt is absorbing.
    """
    chex.assert_rank(hazard, 2)
    chex.assert_type(hazard, jnp.uint8)
    key_dir, key_spont = jax.random.split(key)
    # Invariant #3: always draw, even when beta == 0 or iota == 0.
    u_dir = jax.random.uniform(key_dir, (len(_NEIGHBOR_OFFSETS), *hazard.shape))
    u_spont = jax.random.uniform(key_spont, hazard.shape)

    burning = hazard == BURNING
    fuel = hazard == FUEL
    caught = jnp.zeros_like(burning)
    for d, (dr, dc) in enumerate(_NEIGHBOR_OFFSETS):  # static 4-way stencil
        caught = caught | (_shifted(burning, dr, dc) & (u_dir[d] < beta))
    ignited = fuel & (caught | (u_spont < iota))

    new = jnp.where(burning, jnp.uint8(BURNT), hazard)
    new = jnp.where(ignited, jnp.uint8(BURNING), new)
    return new.astype(jnp.uint8)


def smoke_step(
    smoke: jax.Array, hazard: jax.Array, *, sigma_s: float, eta: float
) -> jax.Array:
    """Def. 6 / D3 smoke update: rho' = e^{-eta} * rho + sigma_s * 1[Burning].

    Smoke outlives flame: emission stops when a cell burns out, but the
    deposited density persists with exponential decay rate eta.
    """
    chex.assert_rank(smoke, 2)
    chex.assert_type(smoke, jnp.float32)
    chex.assert_equal_shape([smoke, hazard])
    emission = sigma_s * (hazard == BURNING)
    return (jnp.exp(-eta) * smoke + emission).astype(jnp.float32)


def hazard_and_smoke_step(
    key: jax.Array,
    hazard: jax.Array,
    smoke: jax.Array,
    *,
    beta: float,
    iota: float = 0.0,
    sigma_s: float,
    eta: float,
) -> tuple[jax.Array, jax.Array]:
    """The (h, rho) sub-step of the Prop.-1 order: h' ~ T_H, then rho' from h'.

    DECISION: smoke emission reads the *post-update* burning set h' (the
    Prop.-1 order computes rho' after h'), so a cell that burns for its one
    step emits sigma_s exactly once, in the step it ignites.
    """
    hazard_new = hazard_step(key, hazard, beta=beta, iota=iota)
    smoke_new = smoke_step(smoke, hazard_new, sigma_s=sigma_s, eta=eta)
    return hazard_new, smoke_new


def seed_ignitions(hazard: jax.Array, mask: jax.Array) -> jax.Array:
    """Ignite Fuel cells where mask is True (Coupling A impulse, Def. 5).

    Non-Fuel cells are unaffected; the caller supplies the (already sampled)
    boolean seeding mask, so this helper is deterministic.
    """
    chex.assert_type(hazard, jnp.uint8)
    chex.assert_type(mask, jnp.bool_)
    chex.assert_equal_shape([hazard, mask])
    return jnp.where(
        (hazard == FUEL) & mask, jnp.uint8(BURNING), hazard
    ).astype(jnp.uint8)
