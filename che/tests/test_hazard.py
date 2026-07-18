"""M0.2 tests: fire-CA kernel (Def. 3) + smoke field (Def. 6).

The monotonicity test is the Phase-0 qualitative stand-in for the Prop. 2 /
Cor. 1 phase-structure tests (full sigmoid calibration is Phase 2).
"""

import chex
import jax
import jax.numpy as jnp
import numpy as np

from che.env.hazard import (
    hazard_and_smoke_step,
    hazard_step,
    seed_ignitions,
    smoke_step,
)
from che.env.types import BURNING, BURNT, FUEL, INTACT  # noqa: F401

L = 32


def center_ignition(size: int) -> jax.Array:
    h = jnp.full((size, size), FUEL, dtype=jnp.uint8)
    return h.at[size // 2, size // 2].set(BURNING)


def rollout_hazard(key, h0, beta, iota, n_steps):
    """Scan the CA forward; returns (final h, stacked per-step h)."""

    def body(carry, _):
        key, h = carry
        key, sub = jax.random.split(key)
        h_new = hazard_step(sub, h, beta=beta, iota=iota)
        return (key, h_new), h_new

    (_, h_final), hs = jax.lax.scan(body, (key, h0), None, length=n_steps)
    return h_final, hs


# ---------------------------------------------------------------- determinism


def test_same_key_bitwise_identical():
    h0 = center_ignition(L)
    key = jax.random.PRNGKey(7)
    _, hs_a = rollout_hazard(key, h0, beta=0.5, iota=0.0, n_steps=20)
    _, hs_b = rollout_hazard(key, h0, beta=0.5, iota=0.0, n_steps=20)
    assert (hs_a == hs_b).all()


def test_different_keys_differ():
    h0 = center_ignition(L)
    _, hs_a = rollout_hazard(jax.random.PRNGKey(0), h0, 0.5, 0.0, 20)
    _, hs_b = rollout_hazard(jax.random.PRNGKey(1), h0, 0.5, 0.0, 20)
    assert (hs_a != hs_b).any()


# ------------------------------------------------------------- shapes/dtypes


def test_shapes_and_dtypes_preserved():
    h0 = center_ignition(L)
    rho0 = jnp.zeros((L, L), dtype=jnp.float32)
    h1, rho1 = hazard_and_smoke_step(
        jax.random.PRNGKey(0), h0, rho0, beta=0.5, sigma_s=1.0, eta=0.5
    )
    chex.assert_shape(h1, (L, L))
    chex.assert_shape(rho1, (L, L))
    chex.assert_type(h1, jnp.uint8)
    chex.assert_type(rho1, jnp.float32)


# ------------------------------------------------- CA transition-rule checks


def test_absorbing_burnt_and_one_step_burn():
    h0 = center_ignition(L)
    _, hs = rollout_hazard(jax.random.PRNGKey(3), h0, 0.6, 0.0, 30)
    hs = jnp.concatenate([h0[None], hs], axis=0)
    prev, curr = hs[:-1], hs[1:]
    # Burnt is absorbing.
    assert ((prev == BURNT) <= (curr == BURNT)).all()
    # Burning -> Burnt after exactly one step.
    assert (curr[prev == BURNING] == BURNT).all()
    # Fuel never jumps straight to Burnt.
    assert ((prev == FUEL) & (curr == BURNT)).sum() == 0


def test_beta_zero_never_spreads_beta_one_is_plus_shape():
    h0 = center_ignition(L)
    h_final, _ = rollout_hazard(jax.random.PRNGKey(0), h0, 0.0, 0.0, 10)
    assert int((h_final == BURNT).sum()) == 1  # only the seed burns
    h1 = hazard_step(jax.random.PRNGKey(0), h0, beta=1.0)
    c = L // 2
    assert h1[c, c] == BURNT
    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        assert h1[c + dr, c + dc] == BURNING
    assert int((h1 == BURNING).sum()) == 4


def test_spontaneous_ignition_iota_one():
    h0 = jnp.full((8, 8), FUEL, dtype=jnp.uint8)
    h1 = hazard_step(jax.random.PRNGKey(0), h0, beta=0.0, iota=1.0)
    assert (h1 == BURNING).all()


def test_seed_ignitions_only_fuel():
    h = jnp.array([[FUEL, BURNING], [BURNT, FUEL]], dtype=jnp.uint8)
    mask = jnp.ones((2, 2), dtype=jnp.bool_)
    out = seed_ignitions(h, mask)
    expect = jnp.array([[BURNING, BURNING], [BURNT, BURNING]], dtype=jnp.uint8)
    assert (out == expect).all()
    # Empty mask is the identity (kappa_A = 0 nesting direction).
    out2 = seed_ignitions(h, jnp.zeros((2, 2), dtype=jnp.bool_))
    assert (out2 == h).all()


# -------------------------------------------------------------------- smoke


def test_smoke_emission_and_exponential_decay_after_burnout():
    """Full burn on 8x8 (beta=1), then log-total-smoke slope must be -eta."""
    eta, sigma_s = 0.5, 1.0
    size = 8
    h = center_ignition(size)
    rho = jnp.zeros((size, size), dtype=jnp.float32)
    key = jax.random.PRNGKey(0)
    totals = []
    for _ in range(30):
        key, sub = jax.random.split(key)
        h, rho = hazard_and_smoke_step(
            sub, h, rho, beta=1.0, sigma_s=sigma_s, eta=eta
        )
        totals.append(float(rho.sum()))
    assert not (h == BURNING).any()  # fully burnt out well before step 30
    assert totals[0] > 0.0  # emission happened
    # Post-burnout tail: pure decay, so log totals are linear with slope -eta.
    tail = np.log(np.asarray(totals[-10:]))
    slope = np.polyfit(np.arange(10), tail, 1)[0]
    assert abs(slope - (-eta)) < 1e-3


def test_smoke_reads_post_update_burning():
    # A cell igniting this step emits immediately (DECISION in hazard.py).
    h = center_ignition(4)
    rho = jnp.zeros((4, 4), dtype=jnp.float32)
    h1, rho1 = hazard_and_smoke_step(
        jax.random.PRNGKey(0), h, rho, beta=1.0, sigma_s=2.0, eta=0.5
    )
    assert (rho1[h1 == BURNING] == 2.0).all()
    assert rho1[2, 2] == 0.0  # the now-Burnt seed emitted only while Burning


def test_smoke_step_no_burning_is_pure_decay():
    rho = jnp.linspace(0.0, 3.0, 16, dtype=jnp.float32).reshape(4, 4)
    h = jnp.full((4, 4), BURNT, dtype=jnp.uint8)
    rho1 = smoke_step(rho, h, sigma_s=5.0, eta=0.25)
    np.testing.assert_allclose(rho1, np.exp(-0.25) * np.asarray(rho), rtol=1e-6)


# ------------------------------------------------------- phase monotonicity


def test_burnt_fraction_monotone_in_beta():
    """32x32, center ignition, >=200 keys: mean burnt fraction increases
    with clear separation across beta in {0.2, 0.5, 0.8}."""
    n_keys, n_steps = 200, 48
    h0 = center_ignition(L)
    keys = jax.random.split(jax.random.PRNGKey(42), n_keys)

    @jax.jit
    def mean_burnt_fraction(beta):
        def one(key):
            h_final, _ = rollout_hazard(key, h0, beta, 0.0, n_steps)
            return (h_final == BURNT).mean()

        return jax.vmap(one)(keys).mean()

    fractions = [float(mean_burnt_fraction(b)) for b in (0.2, 0.5, 0.8)]
    f_low, f_mid, f_high = fractions
    assert f_low < f_mid < f_high
    # "Clear separation": sub- vs near- vs super-critical regimes.
    assert f_mid > f_low + 0.03
    assert f_high > f_mid + 0.15
    assert f_low < 0.05  # subcritical stays local
    assert f_high > 0.5  # supercritical burns most of the arena
