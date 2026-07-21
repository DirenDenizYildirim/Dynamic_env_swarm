"""M3.2 tests: Coupling A active (Def. 5 impulse, end-to-end).

Phase-prompt acceptance list: seeding occurs iff (new collapse ∧ Fuel ∧
within Chebyshev r_seed); seeded ignitions join the same Burning population
(same-step smoke emission and lethality, one-step burn-out); `info` reports
the `seeded_ignitions` count; the invariant-#5 co-active counter goes
nonzero in a hand-built scenario. kappa_A = 0 bitwise nesting is already
pinned in test_nesting.py (structure activity cannot perturb the hazard/
smoke streams) and the structural PRNG-consumption test covers the kernel.
"""

import dataclasses

import jax
import jax.numpy as jnp

from che.env.config import EnvConfig, ThetaConfig
from che.env.env import reset, step
from che.env.hazard import seed_ignitions
from che.env.structure import coupling_a_seed_mask
from che.env.types import BURNING, BURNT, COLLAPSED, FUEL, INTACT

L = 16


def _cheb_ball(center: tuple[int, int], radius: int, ll: int) -> jax.Array:
    r = jnp.arange(ll)
    dr = jnp.abs(r[:, None] - center[0])
    dc = jnp.abs(r[None, :] - center[1])
    return jnp.maximum(dr, dc) <= radius


def test_seed_mask_iff_new_collapse_within_radius():
    """Kernel level: kappa_A = 1 seeds exactly the Chebyshev-r_seed ball of
    the collapse increment; kappa_A = 0 seeds nothing; the Fuel filter in
    seed_ignitions leaves non-Fuel cells untouched."""
    key = jax.random.PRNGKey(0)
    inc = jnp.zeros((L, L), dtype=jnp.bool_).at[5, 5].set(True)
    mask = coupling_a_seed_mask(key, inc, kappa_A=1.0, r_seed=1)
    assert (mask == _cheb_ball((5, 5), 1, L)).all()
    mask0 = coupling_a_seed_mask(key, inc, kappa_A=0.0, r_seed=1)
    assert not mask0.any()

    hazard = (
        jnp.full((L, L), FUEL, dtype=jnp.uint8)
        .at[5, 6].set(BURNT)
        .at[4, 5].set(BURNING)
    )
    h2 = seed_ignitions(hazard, mask)
    assert h2[5, 6] == BURNT  # non-Fuel in the ball: untouched
    assert h2[4, 5] == BURNING
    ball_fuel = _cheb_ball((5, 5), 1, L) & (hazard == FUEL)
    assert (h2[ball_fuel] == BURNING).all()  # every Fuel cell in the ball lit
    assert (h2[~_cheb_ball((5, 5), 1, L)] == hazard[~_cheb_ball((5, 5), 1, L)]).all()


def _hand_built(agent_pos, extra_weak=()):
    """Deterministic single-step scenario: beta = iota = 0 (no primary
    fire), all-Fuel hazard, lambda_0 = 1 and one weak intact cell at (8, 8)
    -> the increment is exactly {(8, 8)}; kappa_A = 1, r_seed = 1 seeds its
    full 3x3 ball. A pre-existing COLLAPSED (also weak) cell at (2, 2)
    checks increment-not-stock: absorbing, so it never re-seeds."""
    theta = ThetaConfig(beta=0.0, iota=0.0, kappa_A=1.0, lambda_0=1.0, r_seed=1)
    cfg = EnvConfig(grid_size=L, n_agents=len(agent_pos), horizon=8, theta=theta)
    _, s = reset(jax.random.PRNGKey(0), cfg)
    weak = jnp.zeros((L, L), dtype=jnp.bool_).at[8, 8].set(True).at[2, 2].set(True)
    for cell in extra_weak:
        weak = weak.at[cell].set(True)
    s = dataclasses.replace(
        s,
        hazard=jnp.full((L, L), FUEL, dtype=jnp.uint8),
        smoke=jnp.zeros((L, L), dtype=jnp.float32),
        structure=jnp.full((L, L), INTACT, dtype=jnp.uint8).at[2, 2].set(COLLAPSED),
        weak=weak,
        agent_pos=jnp.array(agent_pos, dtype=jnp.int32),
        agent_alive=jnp.ones((len(agent_pos),), dtype=jnp.bool_),
    )
    return cfg, s


def test_env_step_seeds_iff_new_collapse():
    # Agent far from everything (Chebyshev > obs_window // 2 from the ball).
    cfg, s = _hand_built([[0, 0]])
    stay = jnp.zeros((1,), jnp.int32)
    _, s1, _, _, info = step(jax.random.PRNGKey(1), s, stay, cfg)
    # The 3x3 ball around the new collapse is Burning — nothing else is.
    ball = _cheb_ball((8, 8), 1, L)
    assert (s1.hazard[ball] == BURNING).all()
    assert not (s1.hazard[~ball] == BURNING).any()  # old collapse never seeds
    assert int(info["seeded_ignitions"]) == 9
    # Far agent: seeded fire outside perception range -> co-active stays 0.
    assert int(info["coupling_co_active"]) == 0
    # Next step: burn time 1 (Def. 3) — seeded cells burn out like any fire;
    # the collapse is absorbing, so the increment (and seeding) is empty.
    _, s2, _, _, info2 = step(jax.random.PRNGKey(2), s1, stay, cfg)
    assert (s2.hazard[ball] == BURNT).all()
    assert int(info2["seeded_ignitions"]) == 0


def test_seeded_fire_smokes_and_kills_like_primary():
    # Agent standing inside the seeding ball at (8, 9): not on the weak
    # cell, so it survives the collapse and is killed by the seeded fire at
    # x' (M1.1 post-move lethality) — same step, same rules as primary fire.
    cfg, s = _hand_built([[8, 9]])
    stay = jnp.zeros((1,), jnp.int32)
    _, s1, reward, _, info = step(jax.random.PRNGKey(1), s, stay, cfg)
    assert int(info["deaths_fire"]) == 1
    assert int(info["deaths_collapse"]) == 0
    # Smoke reads h' (Prop.-1 order): every seeded cell emitted sigma_s in
    # the seeding step itself, from zero initial smoke.
    ball = _cheb_ball((8, 8), 1, L)
    assert (s1.smoke[ball] == cfg.theta.sigma_s).all()
    assert (s1.smoke[~ball] == 0.0).all()


def test_seeded_fire_spreads_like_primary():
    # beta = 1 after the seeding step: the seeded Burning ball must ignite
    # every Fuel von-Neumann neighbor next step, exactly like primary fire.
    cfg, s = _hand_built([[0, 0]])
    stay = jnp.zeros((1,), jnp.int32)
    _, s1, _, _, _ = step(jax.random.PRNGKey(1), s, stay, cfg)
    hot = dataclasses.replace(cfg, theta=dataclasses.replace(cfg.theta, beta=1.0))
    _, s2, _, _, _ = step(jax.random.PRNGKey(2), s1, stay, hot)
    ball = _cheb_ball((8, 8), 1, L)
    ring = _cheb_ball((8, 8), 2, L) & ~ball
    # Von-Neumann spread: the ring cells sharing an edge with the ball.
    edge_ring = ring & (
        jnp.roll(ball, 1, 0) | jnp.roll(ball, -1, 0)
        | jnp.roll(ball, 1, 1) | jnp.roll(ball, -1, 1)
    )
    assert (s2.hazard[edge_ring] == BURNING).all()
    assert (s2.hazard[ball] == BURNT).all()


def test_coactive_counter_hand_built_scenario():
    """Invariant #5 end-to-end: agent at (12, 12) is Chebyshev 4 (= the
    obs_window // 2 perception radius) from the collapse at (8, 8) — the
    seeded cells with row >= 8 and col >= 8 are within range: exactly
    (8,8), (8,9), (9,8), (9,9)."""
    cfg, s = _hand_built([[12, 12]])
    stay = jnp.zeros((1,), jnp.int32)
    _, _, _, _, info = step(jax.random.PRNGKey(1), s, stay, cfg)
    assert int(info["seeded_ignitions"]) == 9
    assert int(info["coupling_co_active"]) == 4
