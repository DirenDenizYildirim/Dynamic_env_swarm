"""M2.1 tests: hazard-only calibration engine sanity (CPU-fast).

The full theory test (Prop. 2 / Cor. 1 sigmoid, beta_c band, front speed)
is M2.3's `test_percolation.py`; here we pin the engine's measurement
semantics on hand-checkable extremes (beta = 0 and beta = 1, where the CA
is deterministic) plus determinism and shapes.
"""

import jax
import jax.numpy as jnp
import numpy as np

from che.calibration.percolation import (
    beta_grid,
    crossing_run,
    fine_beta_grid,
    percolation_run,
    run_ensemble,
)

L = 16
T_MAX = 4 * L


def test_beta_grid_dedup_sorted():
    betas = np.asarray(beta_grid())
    # 19 coarse + 21 fine - 5 shared hundredths.
    assert betas.shape == (35,)
    assert (np.diff(betas) > 0).all()
    assert betas[0] == np.float32(0.05) and betas[-1] == np.float32(0.95)


def test_shapes_and_dtypes():
    out = run_ensemble(
        jax.random.PRNGKey(0),
        jnp.asarray([0.3, 0.6], dtype=jnp.float32),
        grid_size=L,
        n_seeds=4,
        t_max=T_MAX,
    )
    assert out["spanned"].shape == (2, 4)
    assert out["spanned"].dtype == jnp.bool_
    assert out["burnt_fraction"].shape == (2, 4)
    assert out["burnt_fraction"].dtype == jnp.float32
    assert out["extinction_time"].shape == (2, 4)
    assert out["extinction_time"].dtype == jnp.int32
    assert out["front_radius"].shape == (2, 4, T_MAX)
    assert out["front_radius"].dtype == jnp.int32


def test_same_key_bitwise_identical():
    betas = jnp.asarray([0.5], dtype=jnp.float32)
    a = run_ensemble(
        jax.random.PRNGKey(3), betas, grid_size=L, n_seeds=4, t_max=T_MAX
    )
    b = run_ensemble(
        jax.random.PRNGKey(3), betas, grid_size=L, n_seeds=4, t_max=T_MAX
    )
    for name in a:
        assert (np.asarray(a[name]) == np.asarray(b[name])).all(), name


def test_beta_zero_never_spreads():
    out = percolation_run(
        jax.random.PRNGKey(1),
        jnp.float32(0.0),
        grid_size=L,
        t_max=T_MAX,
    )
    # Only the center ignition ever burns; it burns out after step 1.
    assert not bool(out["spanned"])
    assert float(out["burnt_fraction"]) == 1.0 / L**2
    assert int(out["extinction_time"]) == 1
    assert (np.asarray(out["front_radius"]) == 0).all()


def test_beta_one_deterministic_full_burn():
    out = percolation_run(
        jax.random.PRNGKey(2),
        jnp.float32(1.0),
        grid_size=L,
        t_max=T_MAX,
    )
    center = L // 2
    # At beta = 1 the front covers Manhattan distance t at step t; the last
    # cell to ignite is the corner at max Manhattan distance from center.
    max_manhattan = 2 * center  # corner (0, 0) for even L
    assert bool(out["spanned"])
    assert float(out["burnt_fraction"]) == 1.0
    assert int(out["extinction_time"]) == max_manhattan + 1
    front = np.asarray(out["front_radius"])
    expected = np.minimum(np.arange(1, T_MAX + 1), center)
    assert (front == expected).all()


def test_burnt_fraction_monotone_smoke():
    """Qualitative stand-in until M2.3: mean mass grows sub -> super."""
    out = run_ensemble(
        jax.random.PRNGKey(4),
        jnp.asarray([0.1, 0.9], dtype=jnp.float32),
        grid_size=L,
        n_seeds=32,
        t_max=T_MAX,
    )
    mean_bf = np.asarray(out["burnt_fraction"]).mean(axis=1)
    assert mean_bf[1] > 10 * mean_bf[0]


def test_fine_beta_grid():
    betas = np.asarray(fine_beta_grid())
    assert betas.shape == (21,)
    assert betas[0] == np.float32(0.40) and betas[-1] == np.float32(0.60)
    assert (np.diff(betas) > 0).all()


def test_crossing_beta_zero_never_crosses():
    out = crossing_run(
        jax.random.PRNGKey(1), jnp.float32(0.0), grid_size=L, t_max=T_MAX
    )
    assert not bool(out["crossed"])


def test_crossing_beta_one_deterministic_cross():
    # At beta = 1 the front advances one column per step and reaches the
    # right column at t = L - 1 <= T_max deterministically.
    out = crossing_run(
        jax.random.PRNGKey(2), jnp.float32(1.0), grid_size=L, t_max=T_MAX
    )
    assert bool(out["crossed"])


def test_crossing_ensemble_shapes_and_determinism():
    betas = jnp.asarray([0.45, 0.55], dtype=jnp.float32)
    a = run_ensemble(
        jax.random.PRNGKey(7), betas, grid_size=L, n_seeds=8,
        t_max=T_MAX, mode="crossing",
    )
    b = run_ensemble(
        jax.random.PRNGKey(7), betas, grid_size=L, n_seeds=8,
        t_max=T_MAX, mode="crossing",
    )
    assert a["crossed"].shape == (2, 8)
    assert a["crossed"].dtype == jnp.bool_
    assert (np.asarray(a["crossed"]) == np.asarray(b["crossed"])).all()


def test_front_radius_running_max_monotone():
    out = run_ensemble(
        jax.random.PRNGKey(5),
        jnp.asarray([0.55], dtype=jnp.float32),
        grid_size=L,
        n_seeds=8,
        t_max=T_MAX,
    )
    front = np.asarray(out["front_radius"])
    assert (np.diff(front, axis=-1) >= 0).all()
