"""M3.1 tests: weak-cell terrain mask + live structural dynamics.

Covers the phase-prompt acceptance list: only weak cells collapse; the load
term fires only under occupancy; collapsed is absorbing; weak and collapsed
are observable (obs v2 indicator planes 4/5 per D5); the terrain mask uses a
dedicated reset stream; and lambda = 0 bitwise-recovers the Phase-2
(structure-off) trajectories.
"""

import dataclasses

import jax
import jax.numpy as jnp

from che.env.config import EnvConfig, ThetaConfig
from che.env.env import reset, step
from che.env.observation import observe
from che.env.structure import generate_weak_mask, structure_step
from che.env.types import COLLAPSED, INTACT, zeros_state
from che.tests.test_nesting import _assert_bitwise_equal, _traj

L = 16


def _mask_half(ll: int) -> jax.Array:
    """Deterministic weak mask: left half of the grid."""
    return jnp.broadcast_to(jnp.arange(ll)[None, :] < ll // 2, (ll, ll))


def test_only_weak_cells_collapse():
    weak = _mask_half(L)
    structure = jnp.full((L, L), INTACT, jnp.uint8)
    load = jnp.zeros((L, L), jnp.float32)
    out = structure_step(
        jax.random.PRNGKey(0), structure, weak, load, lambda_0=1.0, lambda_load=0.0
    )
    # lambda_0 = 1: every weak cell collapses, no non-weak cell ever does.
    assert ((out == COLLAPSED) == weak).all()


def test_load_term_fires_only_under_occupancy():
    weak = _mask_half(L)
    structure = jnp.full((L, L), INTACT, jnp.uint8)
    load = jnp.zeros((L, L), jnp.float32).at[2, 2].set(1.0).at[2, 12].set(1.0)
    out = structure_step(
        jax.random.PRNGKey(0), structure, weak, load, lambda_0=0.0, lambda_load=1.0
    )
    collapsed = out == COLLAPSED
    assert collapsed[2, 2]  # occupied weak cell falls
    assert not collapsed[2, 12]  # occupied but not weak: never
    assert int(collapsed.sum()) == 1  # nothing else moved


def test_collapsed_is_absorbing_and_increment_only_from_intact():
    weak = jnp.ones((L, L), jnp.bool_)
    structure = jnp.full((L, L), INTACT, jnp.uint8).at[5, 5].set(COLLAPSED)
    load = jnp.zeros((L, L), jnp.float32)
    out = structure_step(
        jax.random.PRNGKey(1), structure, weak, load, lambda_0=0.0, lambda_load=0.0
    )
    assert out[5, 5] == COLLAPSED  # absorbing even with lambdas at 0
    assert (out == structure).all()
    inc = (out == COLLAPSED) & (structure == INTACT)
    assert not inc.any()


def test_obs_plane_encoding():
    cfg = EnvConfig(grid_size=L, n_agents=1, horizon=32)
    s = zeros_state(L, 1, jax.random.PRNGKey(0))
    r = cfg.obs_window // 2
    # Agent at center; weak-intact west, collapsed east, sound elsewhere.
    c = L // 2
    s = dataclasses.replace(
        s,
        agent_pos=jnp.array([[c, c]], jnp.int32),
        weak=jnp.zeros((L, L), jnp.bool_).at[c, c - 1].set(True),
        structure=jnp.full((L, L), INTACT, jnp.uint8).at[c, c + 1].set(COLLAPSED),
    )
    grid = observe(s, cfg)["grid"][0]
    # Obs v2 (D5): weak is indicator plane 4, collapsed indicator plane 5.
    assert grid[r, r - 1, 4] == 1.0  # weak west
    assert grid[r, r - 1, 5] == 0.0  # ...but not collapsed
    assert grid[r, r + 1, 5] == 1.0  # collapsed east
    assert grid[r, r + 1, 4] == 0.0  # ...not weak in this state
    assert grid[r, r, 4] == 0.0 and grid[r, r, 5] == 0.0  # sound center
    # A collapsed cell that is also weak sets BOTH indicators (D5 DECISION:
    # two bits carry strictly more information than v1's collapse-wins).
    s2 = dataclasses.replace(s, weak=s.weak.at[c, c + 1].set(True))
    grid2 = observe(s2, cfg)["grid"][0]
    assert grid2[r, r + 1, 4] == 1.0 and grid2[r, r + 1, 5] == 1.0


def test_weak_mask_fraction_and_clustering():
    key = jax.random.PRNGKey(7)
    for f_weak in (0.0, 0.15, 0.4):
        m = generate_weak_mask(key, 64, f_weak=f_weak, n_smooth=2)
        assert abs(float(m.mean()) - f_weak) < 0.01, f_weak
    # Clustering: among weak cells, the mean weak-neighbor fraction beats
    # the iid expectation (= f_weak) by a wide margin after smoothing.
    f = 0.15
    m = generate_weak_mask(key, 64, f_weak=f, n_smooth=2)
    p = jnp.pad(m.astype(jnp.float32), 1)
    neigh = (
        sum(p[i : i + 64, j : j + 64] for i in (0, 1, 2) for j in (0, 1, 2))
        - m.astype(jnp.float32)
    ) / 8.0
    assert float(neigh[m].mean()) > 2.0 * f


def test_terrain_stream_is_dedicated():
    # Same reset key, f_weak on vs off: every non-weak reset field bitwise
    # identical (the terrain stream cannot perturb food/agents/ignition).
    theta_on = ThetaConfig(beta=0.5, f_weak=0.4)
    cfg_on = EnvConfig(grid_size=L, n_agents=4, horizon=64, theta=theta_on)
    cfg_off = dataclasses.replace(
        cfg_on, theta=dataclasses.replace(theta_on, f_weak=0.0)
    )
    key = jax.random.PRNGKey(11)
    _, s_on = reset(key, cfg_on)
    obs_off, s_off = reset(key, cfg_off)
    assert s_on.weak.any() and not s_off.weak.any()  # knob is live
    for f in ("food", "agent_pos", "agent_alive", "hazard", "structure", "smoke"):
        assert (getattr(s_on, f) == getattr(s_off, f)).all(), f
    # The weak mask is visible at reset (M3.1 DECISION: observable; obs v2
    # plane 4 per D5).
    obs_on = observe(s_on, cfg_on)
    assert (obs_on["grid"][..., 4] != obs_off["grid"][..., 4]).any()


def test_lambda_zero_bitwise_recovers_structure_off_trajectories():
    """Phase-2 recovery: with lambda_0 = lambda_load = 0, the weak mask is
    inert — every state trajectory is bitwise identical to the f_weak = 0
    nested model under the same keys (random actions, obs-independent)."""
    off = ThetaConfig(beta=0.5, lambda_0=0.0, lambda_load=0.0, f_weak=0.0)
    weak_only = dataclasses.replace(off, f_weak=0.4)
    a, b = _traj(off), _traj(weak_only)
    _assert_bitwise_equal(
        a, b, ("hazard", "smoke", "structure", "food", "pos", "alive", "reward")
    )


def test_deaths_collapse_counted_in_env():
    # End-to-end: an all-weak arena with lambda_0 = 1 collapses everything
    # at t = 1; all agents fall (deaths_collapse) and no one burns.
    theta = ThetaConfig(beta=0.0, lambda_0=1.0, f_weak=1.0, weak_smooth=0)
    cfg = EnvConfig(grid_size=L, n_agents=4, horizon=8, theta=theta)
    key = jax.random.PRNGKey(2)
    _, s = reset(key, cfg)
    # f_weak = 1 thresholds at the max: the argmax cell stays non-weak, so
    # place no agent there — use the mask itself to check.
    actions = jnp.zeros((4,), jnp.int32)
    _, s1, _, _, info = step(jax.random.PRNGKey(3), s, actions, cfg)
    on_weak = s.weak[s.agent_pos[:, 0], s.agent_pos[:, 1]]
    assert int(info["deaths_collapse"]) == int(on_weak.sum())
    assert int(info["deaths_fire"]) == 0
    assert (s1.structure[s.weak] == COLLAPSED).all()
