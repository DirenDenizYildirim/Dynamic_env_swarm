"""M4.1 tests: Coupling B (Def. 6) — transmittance properties, per-cell
masking semantics, the obs v3 schema, and the nesting invariant.

The masking design is human-locked (phase4 prompt M4.1): optical depth
D = kappa_B * dist * mean_rho(ray) with an S=4 midpoint quadrature over
the current smoke field, tau = exp(-D), content planes revealed w.p. tau,
realized reveal mask appended as plane 7. Nesting (invariant #3):
kappa_B = 0 => tau == 1 => bitwise recovery of the pre-masking env, and
Coupling B lives in the observation kernel only — no kappa_B value may
perturb any state trajectory.
"""

import dataclasses

import jax
import jax.numpy as jnp

from che.env.config import EnvConfig, ThetaConfig
from che.env.env import reset, step
from che.env.observation import N_PLANES, masked_fraction, observe, transmittance
from che.env.types import BURNING, zeros_state
from che.tests.test_nesting import _assert_bitwise_equal, _traj

L = 16
K = 9
R = K // 2

# Fire/smoke-heavy theta so masking has something to bite on.
_HOT = ThetaConfig(beta=0.6, iota=0.02, sigma_s=1.0, eta=0.5)


def _uniform_smoke_state(rho: float, n_agents: int = 4):
    """All-Fuel state with a uniform smoke field and agents away from the
    border (every quadrature sample stays in-grid => mean_rho == rho)."""
    s = zeros_state(L, n_agents, jax.random.PRNGKey(0))
    pos = jnp.array([[8, 8], [7, 6], [9, 10], [6, 9]], jnp.int32)[:n_agents]
    return dataclasses.replace(
        s,
        smoke=jnp.full((L, L), rho, jnp.float32),
        agent_pos=pos,
    )


def test_transmittance_exact_on_uniform_smoke():
    """Uniform smoke of density rho: every ray sample reads rho, so
    tau = exp(-kappa_B * dist * rho) in closed form; own cell tau = 1."""
    rho, kb = 0.8, 0.7
    s = _uniform_smoke_state(rho)
    tau = transmittance(s.smoke, s.agent_pos, kappa_B=kb, k=K)
    span = jnp.arange(-R, R + 1, dtype=jnp.float32)
    dist = jnp.sqrt(span[:, None] ** 2 + span[None, :] ** 2)
    expected = jnp.exp(-kb * dist * rho)
    assert jnp.allclose(tau, expected[None], rtol=1e-6)
    assert (tau[:, R, R] == 1.0).all()  # dist 0 => always visible


def test_transmittance_monotone_in_distance_smoke_and_kappa():
    rho_lo, rho_hi = 0.3, 0.9
    s_lo, s_hi = _uniform_smoke_state(rho_lo), _uniform_smoke_state(rho_hi)
    tau = transmittance(s_lo.smoke, s_lo.agent_pos, kappa_B=0.5, k=K)
    # Distance: strictly decreasing along a ray from the agent.
    row = tau[0, R, R:]  # dist 0, 1, ..., R along one axis
    assert (jnp.diff(row) < 0).all()
    # Smoke: elementwise <= (strict off-center) for the denser field.
    tau_hi = transmittance(s_hi.smoke, s_hi.agent_pos, kappa_B=0.5, k=K)
    assert (tau_hi <= tau).all()
    assert (tau_hi[:, R, R + 1] < tau[:, R, R + 1]).all()
    # kappa_B: elementwise <= (strict off-center) for the stronger coupling.
    tau_kb = transmittance(s_lo.smoke, s_lo.agent_pos, kappa_B=1.5, k=K)
    assert (tau_kb <= tau).all()
    assert (tau_kb[:, R, R + 1] < tau[:, R, R + 1]).all()
    # kappa_B = 0: tau identically 1 no matter the smoke.
    tau0 = transmittance(s_hi.smoke, s_hi.agent_pos, kappa_B=0.0, k=K)
    assert (tau0 == 1.0).all()


def test_isolated_smoke_cell_is_unoccluded_beyond_quadrature_range():
    """M4.2 Finding 1, pinned as a *documented kernel property* (human
    ruling 2026-07-27): the S=4 midpoint samples never land on the ray's
    endpoint beyond axis distance ~4, so a single-cell smoke source
    contributes no occlusion to its own line of sight at longer range —
    tau == 1 exactly, at any kappa_B. Spatially extended smoke (what the
    swarm env produces) is unaffected, and the M4.3 detection band at
    crop distance 3 sits inside the well-sampled regime. E2C's geometry
    is sized to stay there; see che/env/e2c.py."""
    k_wide, r_wide = 17, 8  # wide enough to hold the far probes
    smoke = jnp.zeros((L, L), jnp.float32).at[8, 8].set(2.5)  # one cell
    for d, expect_occluded in ((1, True), (3, True), (4, True), (5, False)):
        pos = jnp.array([[8 - d, 8]], jnp.int32)  # d cells away, same column
        tau = transmittance(smoke, pos, kappa_B=5.0, k=k_wide)
        at_source = float(tau[0, r_wide + d, r_wide])
        assert (at_source < 1.0) == expect_occluded, (d, at_source)
    # An extended source along the same ray does occlude at that range.
    lane = smoke.at[4:9, 8].set(1.0)
    far = jnp.array([[3, 8]], jnp.int32)
    tau_lane = transmittance(lane, far, kappa_B=5.0, k=k_wide)
    assert float(tau_lane[0, r_wide + 5, r_wide]) < 0.05


def test_masking_respects_visibility_plane_exactly():
    """Obs v3 content == obs v2 content * reveal mask, cell by cell, and
    the own cell is always revealed even under heavy smoke."""
    cfg3 = EnvConfig(
        grid_size=L,
        n_agents=4,
        horizon=32,
        theta=ThetaConfig(kappa_B=1.0),
    )
    cfg2 = dataclasses.replace(cfg3, obs_version=2)
    s = _uniform_smoke_state(1.5)
    # Real content everywhere the probes can land: fire + food + occupancy.
    s = dataclasses.replace(
        s,
        hazard=s.hazard.at[8, 6].set(BURNING).at[5, 9].set(BURNING),
        food=s.food.at[7, 8].set(1).at[10, 10].set(1),
    )
    obs3 = observe(s, cfg3, jax.random.PRNGKey(5))
    obs2 = observe(s, cfg2)
    assert obs3["grid"].shape == (4, K, K, N_PLANES)
    vis = obs3["grid"][..., 7]
    assert jnp.isin(vis, jnp.array([0.0, 1.0])).all()
    assert (vis[:, R, R] == 1.0).all()  # own cell: dist 0
    assert 0.0 < float(vis.mean()) < 1.0  # masking is live, not total
    assert (obs3["grid"][..., :7] == obs2["grid"] * vis[..., None]).all()
    # Own-state vec is never attenuated.
    assert (obs3["vec"] == obs2["vec"]).all()


def test_kappa_b_zero_bitwise_recovers_obs_v2():
    """Nesting (M4.1): obs v3 at kappa_B = 0 is the pre-masking env plus a
    constant all-ones visibility plane — state trajectories, rewards, and
    content planes bitwise identical to obs v2 under the same keys."""
    theta = dataclasses.replace(_HOT, kappa_B=0.0)
    cfg3 = EnvConfig(grid_size=L, n_agents=4, horizon=64, theta=theta)
    cfg2 = dataclasses.replace(cfg3, obs_version=2)
    a = _traj(theta, cfg=cfg3)
    b = _traj(theta, cfg=cfg2)
    _assert_bitwise_equal(
        a, b, ("hazard", "smoke", "structure", "food", "pos", "alive", "reward")
    )
    # Obs-level recovery over a hand-stepped rollout with shared keys.
    key = jax.random.PRNGKey(3)
    key, k_reset = jax.random.split(key)
    obs3, s3 = reset(k_reset, cfg3)
    obs2, s2 = reset(k_reset, cfg2)
    for _ in range(20):
        assert (obs3["grid"][..., :7] == obs2["grid"]).all()
        assert (obs3["grid"][..., 7] == 1.0).all()
        key, k_act, k_step = jax.random.split(key, 3)
        actions = jax.random.randint(k_act, (4,), 0, 5, jnp.int32)
        obs3, s3, _, _, info3 = step(k_step, s3, actions, cfg3)
        obs2, s2, _, _, _ = step(k_step, s2, actions, cfg2)
        assert float(info3["masked_frac"]) == 0.0
    assert (s3.smoke > 0).any()  # the fire actually made smoke


def test_kappa_b_cannot_perturb_state_trajectories():
    """Coupling B lives in the observation kernel only: under obs-blind
    (random) actions, any kappa_B leaves every state trajectory bitwise
    unchanged (invariant #3 — the reveal draw is a dedicated stream)."""
    base = dataclasses.replace(_HOT, kappa_B=0.0)
    hot = dataclasses.replace(_HOT, kappa_B=2.0)
    a, b = _traj(base), _traj(hot)
    assert (a["smoke"] > 0).any()  # smoke is live, masking would differ...
    _assert_bitwise_equal(
        a, b, ("hazard", "smoke", "structure", "food", "pos", "alive", "reward")
    )


def test_reveal_draw_present_at_kappa_b_zero():
    """Invariant #3, structural form (as in test_nesting): the obs v3
    reveal uniforms are drawn even at kappa_B = 0 — a `if kappa_B > 0`
    gate would be invisible to the bitwise tests (dedicated stream)."""
    prng_prims = ("random_bits", "threefry2x32", "prng_random_bits")
    cfg = EnvConfig(
        grid_size=L, n_agents=4, horizon=32, theta=ThetaConfig(kappa_B=0.0)
    )
    s = zeros_state(L, 4, jax.random.PRNGKey(0))
    jaxpr = jax.make_jaxpr(lambda st, k: observe(st, cfg, k))(
        s, jax.random.PRNGKey(1)
    )
    assert any(p in str(jaxpr) for p in prng_prims), (
        "obs v3 at kappa_B=0 lost its reveal draw"
    )


def test_masked_frac_info_channel():
    """The masked_frac info channel equals 1 - mean(visibility) over alive
    agents of the returned obs, is > 0 under heavy smoke, and is 0 for an
    all-dead swarm."""
    cfg = EnvConfig(
        grid_size=L, n_agents=4, horizon=32, theta=ThetaConfig(kappa_B=1.0)
    )
    s = _uniform_smoke_state(1.5)
    actions = jnp.zeros((4,), jnp.int32)
    obs, _, _, _, info = step(jax.random.PRNGKey(2), s, actions, cfg)
    vis = obs["grid"][..., 7]
    expected = float((1.0 - vis.mean(axis=(-2, -1))).mean())  # all alive
    assert abs(float(info["masked_frac"]) - expected) < 1e-6
    assert float(info["masked_frac"]) > 0.0
    # masked_fraction is alive-only: dead agents contribute nothing.
    half = jnp.array([True, True, False, False])
    mf_half = masked_fraction(obs["grid"], half, cfg)
    manual = float((1.0 - vis[:2].mean(axis=(-2, -1))).mean())
    assert abs(float(mf_half) - manual) < 1e-6
    s_dead = dataclasses.replace(s, agent_alive=jnp.zeros((4,), jnp.bool_))
    _, _, _, _, info_d = step(jax.random.PRNGKey(2), s_dead, actions, cfg)
    assert float(info_d["masked_frac"]) == 0.0
