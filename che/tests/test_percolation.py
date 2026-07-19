"""M2.3 theory unit test — the Phase-2 hook from theory §10.

Percolation sigmoid (Prop. 2 / Cor. 1) at CPU scale: L = 32, 256 seeds,
coarse beta grid, single shared ensemble (< 60 s budget). Ground-truth
rules (CLAUDE.md invariant #4): never loosen these tolerances without
human sign-off; a beta_c outside [0.42, 0.58] means the CA kernel is
mis-ported (idealized von-Neumann kernel: exactly 1/2 — Kesten; the band
covers finite-size + estimator bias and is unchanged by the 2026-07-19
M2.2 amendment; confirmed satisfied by the M2.4 severity lock,
beta_c_hat = 0.500).
"""

import jax
import jax.numpy as jnp
import numpy as np
import pytest

from che.calibration.estimates import beta_half, front_speed, p_span_curve
from che.calibration.percolation import run_ensemble

pytestmark = pytest.mark.slow

L = 32
T_MAX = 4 * L
N_SEEDS = 256
# Coarse grid per the M2.3 spec; 0.05 steps span sub- to supercritical.
BETAS = np.round(np.arange(0.05, 0.96, 0.05), 2)


@pytest.fixture(scope="module")
def ensemble() -> dict[str, np.ndarray]:
    out = run_ensemble(
        jax.random.PRNGKey(0),
        jnp.asarray(BETAS, dtype=jnp.float32),
        grid_size=L,
        n_seeds=N_SEEDS,
        t_max=T_MAX,
    )
    return {k: np.asarray(v) for k, v in out.items()}


def test_p_span_isotonic_within_2sigma(ensemble):
    """P_span monotone non-decreasing in beta, allowing MC noise: any
    decrease between consecutive betas must be within 2 sigma of the
    pooled binomial error (Prop. 2 monotone coupling; with common random
    numbers the violation is expected to be exactly zero)."""
    p, se = p_span_curve(ensemble["spanned"])
    pooled = np.sqrt(se[:-1] ** 2 + se[1:] ** 2)
    violations = p[:-1] - p[1:]  # positive where the curve decreases
    assert (violations <= 2.0 * pooled).all(), (
        f"non-isotonic beyond 2 sigma at "
        f"beta={BETAS[1:][violations > 2.0 * pooled]}"
    )


def test_beta_c_in_band(ensemble):
    """beta_c_hat in [0.42, 0.58] — DO NOT widen without human sign-off
    (theory §10: outside the band the kernel is mis-ported)."""
    p, _ = p_span_curve(ensemble["spanned"])
    beta_c = beta_half(BETAS, p)
    assert 0.42 <= beta_c <= 0.58, f"beta_c_hat={beta_c:.4f} out of band"


def test_front_speed_increasing_top_betas(ensemble):
    """v_hat strictly increasing over the three largest tested betas
    (supercritical front accelerates with beta toward 1 cell/step)."""
    v, _, _ = front_speed(ensemble["front_radius"], L)
    top3 = v[-3:]  # betas 0.85, 0.90, 0.95
    assert np.isfinite(top3).all(), f"v_hat undefined in top betas: {top3}"
    assert (np.diff(top3) > 0).all(), f"v_hat not increasing: {top3}"
