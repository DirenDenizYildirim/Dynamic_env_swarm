"""M0.3 tests: composed env purity, food conservation, border crops,
movement, the coupling-co-active counter plumbing, and batched rollouts."""

import dataclasses
from pathlib import Path

import jax
import jax.numpy as jnp

from che.env.config import ThetaConfig, load_config
from che.env.env import agent_step, reset, step
from che.env.observation import observe
from che.env.types import BURNING, FUEL, INTACT
from che.train.rollout import batch_rollout, make_random_policy, rollout_episode

CONFIG_DIR = Path(__file__).resolve().parent.parent / "configs"
CFG = load_config(CONFIG_DIR / "debug.yaml").env


def test_env_purity_same_key_same_everything():
    key = jax.random.PRNGKey(0)
    _, s0 = reset(key, CFG)
    actions = jnp.array([0, 1, 2, 3], dtype=jnp.int32)
    k = jax.random.PRNGKey(5)
    out_a = step(k, s0, actions, CFG)
    out_b = step(k, s0, actions, CFG)
    for leaf_a, leaf_b in zip(
        jax.tree_util.tree_leaves(out_a),
        jax.tree_util.tree_leaves(out_b),
        strict=True,
    ):
        assert (leaf_a == leaf_b).all()


def test_rollout_deterministic_and_key_sensitive():
    policy = make_random_policy(CFG.n_agents)
    run = jax.jit(lambda k: rollout_episode(k, CFG, policy, 32))
    r_a, _, _ = run(jax.random.PRNGKey(1))
    r_b, _, _ = run(jax.random.PRNGKey(1))
    r_c, _, _ = run(jax.random.PRNGKey(2))
    assert (r_a == r_b).all()
    assert not jnp.array_equal(
        r_a.cumsum()[-1:], r_c.cumsum()[-1:]
    ) or not (r_a == r_c).all()


def test_movement_and_border_clipping():
    # Benign fields (no fire, intact, no collapses): agent_step reduces to
    # clip-to-grid movement with dead agents holding still.
    ll = CFG.grid_size
    fuel = jnp.full((ll, ll), FUEL, dtype=jnp.uint8)
    intact = jnp.full((ll, ll), INTACT, dtype=jnp.uint8)
    no_inc = jnp.zeros((ll, ll), dtype=jnp.bool_)
    pos = jnp.array([[5, 5], [0, 0], [15, 15], [0, 15]], dtype=jnp.int32)
    alive = jnp.array([True, True, True, False])
    # stay, up (clipped), down (clipped), right (dead: holds still)
    actions = jnp.array([0, 1, 2, 4], dtype=jnp.int32)
    new, alive_new, d_fire, d_coll = agent_step(
        pos, alive, actions, fuel, intact, no_inc, ll
    )
    expect = jnp.array([[5, 5], [0, 0], [15, 15], [0, 15]], dtype=jnp.int32)
    assert (new == expect).all()
    assert (alive_new == alive).all()
    assert int(d_fire) + int(d_coll) == 0
    actions2 = jnp.array([1, 2, 3, 4], dtype=jnp.int32)  # up, down, left, right
    new2, _, _, _ = agent_step(
        pos, jnp.ones(4, bool), actions2, fuel, intact, no_inc, ll
    )
    expect2 = jnp.array([[4, 5], [1, 0], [15, 14], [0, 15]], dtype=jnp.int32)
    assert (new2 == expect2).all()


def test_food_conservation_over_episode():
    policy = make_random_policy(CFG.n_agents)
    rewards, _, infos = jax.jit(
        lambda k: rollout_episode(k, CFG, policy, CFG.horizon)
    )(jax.random.PRNGKey(3))
    collected_cum = rewards.cumsum()
    # Conservation at every step: remaining + collected == initial F.
    assert (infos["food_remaining"] + collected_cum == CFG.n_food).all()
    assert (rewards >= 0).all()
    # Random policy on 16x16 with 4 agents collects something in 256 steps.
    assert collected_cum[-1] > 0


def test_obs_crop_border_correctness():
    """Agent at the corner: out-of-bounds pads 0; in-bounds cells line up."""
    _, s = reset(jax.random.PRNGKey(0), CFG)
    ll = CFG.grid_size
    food = jnp.zeros((ll, ll), dtype=jnp.uint8).at[0, 1].set(1)
    hazard = jnp.full((ll, ll), FUEL, dtype=jnp.uint8).at[1, 0].set(BURNING)
    s = dataclasses.replace(
        s,
        agent_pos=jnp.array([[0, 0], [8, 8], [15, 15], [8, 8]], dtype=jnp.int32),
        food=food,
        hazard=hazard,
    )
    obs = observe(s, CFG)
    grid = obs["grid"]
    r = CFG.obs_window // 2  # = 2 for k=5
    corner = grid[0]  # agent at (0, 0): rows/cols < r are out of bounds
    assert (corner[:r, :, :] == 0).all()
    assert (corner[:, :r, :] == 0).all()
    # Food at (0, 1) appears at crop cell (r, r+1) in plane 2.
    assert corner[r, r + 1, 2] == 1.0
    # Burning at (1, 0) appears at crop cell (r+1, r) in plane 0, value 1/2.
    assert corner[r + 1, r, 0] == 0.5
    # Bottom-right corner agent: high rows/cols are out of bounds.
    br = grid[2]
    assert (br[-r:, :, :] == 0).all()
    assert (br[:, -r:, :] == 0).all()
    # Own-state vec: normalized position, alive, t/horizon.
    assert obs["vec"].shape == (CFG.n_agents, 4)
    assert obs["vec"][0, 2] == 1.0


def test_batch_rollout_shapes_and_finite():
    policy = make_random_policy(CFG.n_agents)
    rewards, dones, infos = jax.jit(
        lambda k: batch_rollout(k, CFG, policy, 64, n_envs=2)
    )(jax.random.PRNGKey(0))
    assert rewards.shape == (2, 64)
    assert dones.shape == (2, 64)
    assert infos["coupling_co_active"].shape == (2, 64)
    assert jnp.isfinite(rewards).all()
    assert not dones[:, :-1].any() or CFG.horizon <= 64


def test_done_exactly_at_horizon():
    policy = make_random_policy(CFG.n_agents)
    _, dones, _ = jax.jit(
        lambda k: rollout_episode(k, CFG, policy, CFG.horizon)
    )(jax.random.PRNGKey(0))
    assert not dones[:-1].any()
    assert dones[-1]


def test_coupling_co_active_counter_plumbing():
    """kappa_A = 0 -> counter is identically 0; hot theta -> it fires."""
    policy = make_random_policy(CFG.n_agents)
    _, _, infos = jax.jit(
        lambda k: rollout_episode(k, CFG, policy, 64)
    )(jax.random.PRNGKey(0))
    assert (infos["coupling_co_active"] == 0).all()  # debug config: kappa_A=0

    hot = dataclasses.replace(
        CFG,
        theta=ThetaConfig(beta=0.3, kappa_A=1.0, lambda_0=0.05, r_seed=2),
    )
    _, _, infos_hot = jax.jit(
        lambda k: rollout_episode(k, hot, policy, 64)
    )(jax.random.PRNGKey(0))
    assert int(infos_hot["coupling_co_active"].sum()) > 0
