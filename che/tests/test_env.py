"""M0.3 tests: composed env purity, food conservation, border crops,
movement, the coupling-co-active counter plumbing, and batched rollouts."""

import dataclasses
from pathlib import Path

import jax
import jax.numpy as jnp

from che.env.config import ThetaConfig, load_config
from che.env.env import agent_step, reset, step
from che.env.observation import N_PLANES, observe
from che.env.types import BURNING, BURNT, COLLAPSED, FUEL, INTACT
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
    assert (
        not jnp.array_equal(r_a.cumsum()[-1:], r_c.cumsum()[-1:])
        or not (r_a == r_c).all()
    )


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
    new, alive_new, d_fire, d_coll, n_blocked = agent_step(
        pos, alive, actions, fuel, intact, no_inc, ll
    )
    expect = jnp.array([[5, 5], [0, 0], [15, 15], [0, 15]], dtype=jnp.int32)
    assert (new == expect).all()
    assert (alive_new == alive).all()
    assert int(d_fire) + int(d_coll) == 0
    assert int(n_blocked) == 0  # nothing collapsed anywhere
    actions2 = jnp.array([1, 2, 3, 4], dtype=jnp.int32)  # up, down, left, right
    new2, _, _, _, _ = agent_step(
        pos, jnp.ones(4, bool), actions2, fuel, intact, no_inc, ll
    )
    expect2 = jnp.array([[4, 5], [1, 0], [15, 14], [0, 15]], dtype=jnp.int32)
    assert (new2 == expect2).all()


def test_food_conservation_over_episode():
    policy = make_random_policy(CFG.n_agents)
    rewards, _, infos = jax.jit(lambda k: rollout_episode(k, CFG, policy, CFG.horizon))(
        jax.random.PRNGKey(3)
    )
    collected_cum = rewards.cumsum()
    # Conservation at every step: remaining + collected == initial F.
    assert (infos["food_remaining"] + collected_cum == CFG.n_food).all()
    assert (rewards >= 0).all()
    # Random policy on 16x16 with 4 agents collects something in 256 steps.
    assert collected_cum[-1] > 0


def _obs_probe_state(s):
    """Hand-built state with one probe per obs channel, each at a distinct
    asymmetric offset from agent 0 at (0, 0) — kills plane swaps AND crop
    transpositions (M3.0b mutations c/d)."""
    ll = CFG.grid_size
    hazard = (
        jnp.full((ll, ll), FUEL, dtype=jnp.uint8)
        .at[1, 0]
        .set(BURNING)
        .at[0, 2]
        .set(BURNT)
    )
    return dataclasses.replace(
        s,
        agent_pos=jnp.array([[0, 0], [8, 8], [15, 15], [8, 9]], dtype=jnp.int32),
        agent_alive=jnp.array([True, True, True, False]),
        food=jnp.zeros((ll, ll), dtype=jnp.uint8).at[0, 1].set(1),
        hazard=hazard,
        smoke=jnp.zeros((ll, ll), dtype=jnp.float32).at[2, 1].set(0.75),
        weak=jnp.zeros((ll, ll), dtype=jnp.bool_).at[1, 2].set(True),
        structure=(jnp.full((ll, ll), INTACT, dtype=jnp.uint8).at[1, 1].set(COLLAPSED)),
    )


def test_obs_crop_border_correctness():
    """Obs v2 (D5): 7 planes in order, out-of-bounds pads 0, every probe
    lands in exactly its own plane, alive-occupancy includes self and drops
    the dead."""
    _, s = reset(jax.random.PRNGKey(0), CFG)
    s = _obs_probe_state(s)
    obs = observe(s, CFG)
    grid = obs["grid"]
    assert grid.shape == (CFG.n_agents, CFG.obs_window, CFG.obs_window, N_PLANES)
    r = CFG.obs_window // 2
    corner = grid[0]  # agent at (0, 0): rows/cols < r are out of bounds
    assert (corner[:r, :, :] == 0).all()
    assert (corner[:, :r, :] == 0).all()
    # One probe per plane, each at its own (row, col) offset from the agent:
    # (plane, crop row, crop col, value).
    probes = [
        (0, r + 1, r, 1.0),  # Burning at world (1, 0)
        (1, r, r + 2, 1.0),  # Burnt at world (0, 2)
        (2, r + 2, r + 1, 0.75),  # smoke at world (2, 1) — continuous
        (3, r, r + 1, 1.0),  # food at world (0, 1)
        (4, r + 1, r + 2, 1.0),  # weak at world (1, 2)
        (5, r + 1, r + 1, 1.0),  # collapsed at world (1, 1)
        (6, r, r, 1.0),  # alive occ: the observer itself at the center
    ]
    for pl, row, col, val in probes:
        assert corner[row, col, pl] == val, f"plane {pl}"
        # Cross-plane isolation: the probe cell is 0 in every OTHER plane.
        for other in range(N_PLANES):
            if other != pl:
                assert corner[row, col, other] == 0.0, f"{pl} leaked to {other}"
    # Indicator purity: everything but smoke (plane 2) is in {0, 1}.
    ind = jnp.delete(corner, 2, axis=-1)
    assert jnp.isin(ind, jnp.array([0.0, 1.0])).all()
    # Dead agents disappear: agent 3 (dead) sits at (8, 9), one cell right
    # of agent 1 — absent from agent 1's occupancy plane.
    mid = grid[1]
    assert mid[r, r, 6] == 1.0  # self
    assert mid[r, r + 1, 6] == 0.0  # dead neighbor invisible
    # Bottom-right corner agent: high rows/cols are out of bounds.
    br = grid[2]
    assert (br[-r:, :, :] == 0).all()
    assert (br[:, -r:, :] == 0).all()
    # Own-state vec: normalized position, alive, t/horizon.
    assert obs["vec"].shape == (CFG.n_agents, 4)
    assert obs["vec"][0, 2] == 1.0
    assert obs["vec"][3, 2] == 0.0  # dead agent's own alive flag


def test_obs_v1_archival_encoding_unchanged():
    """D5: obs v1 stays restorable for archival eval — the M1.2 mixed
    encodings must not drift (never compared against v2, only preserved)."""
    cfg1 = dataclasses.replace(CFG, obs_version=1)
    _, s = reset(jax.random.PRNGKey(0), cfg1)
    s = _obs_probe_state(s)
    grid = observe(s, cfg1)["grid"]
    assert grid.shape == (CFG.n_agents, CFG.obs_window, CFG.obs_window, 5)
    r = CFG.obs_window // 2
    corner = grid[0]
    assert corner[r + 1, r, 0] == 0.5  # Burning = 1/2 on the hazard plane
    assert corner[r, r + 2, 0] == 1.0  # Burnt = 1 (the D5-motivating quirk)
    assert corner[r + 2, r + 1, 1] == 0.75  # smoke
    assert corner[r, r + 1, 2] == 1.0  # food
    assert corner[r + 1, r + 1, 3] == 1.0  # collapsed (tri-level plane)
    assert corner[r + 1, r + 2, 3] == 0.5  # weak-intact
    assert corner[r, r, 4] == 1.0  # occ self


def test_batch_rollout_shapes_and_finite():
    policy = make_random_policy(CFG.n_agents)
    rewards, dones, infos = jax.jit(
        lambda k: batch_rollout(k, CFG, policy, 64, n_envs=2)
    )(jax.random.PRNGKey(0))
    assert rewards.shape == (2, 64)
    assert dones.shape == (2, 64)
    assert infos["coupling_co_active"].shape == (2, 64)
    assert infos["seeded_ignitions"].shape == (2, 64)  # M3.2 info channel
    assert jnp.isfinite(rewards).all()
    assert not dones[:, :-1].any() or CFG.horizon <= 64


def test_done_exactly_at_horizon():
    policy = make_random_policy(CFG.n_agents)
    _, dones, _ = jax.jit(lambda k: rollout_episode(k, CFG, policy, CFG.horizon))(
        jax.random.PRNGKey(0)
    )
    assert not dones[:-1].any()
    assert dones[-1]


def test_coupling_co_active_counter_plumbing():
    """kappa_A = 0 -> counter is identically 0; hot theta -> it fires."""
    policy = make_random_policy(CFG.n_agents)
    _, _, infos = jax.jit(lambda k: rollout_episode(k, CFG, policy, 64))(
        jax.random.PRNGKey(0)
    )
    assert (infos["coupling_co_active"] == 0).all()  # debug config: kappa_A=0
    assert (infos["seeded_ignitions"] == 0).all()  # M3.2: same gate
    # M3.4-lock addendum channels: no weak cells in the debug config, so
    # nothing collapses, nothing blocks; occupancy share is a valid rate.
    assert (infos["collapse_events"] == 0).all()
    assert (infos["blocked_moves"] == 0).all()
    assert (infos["weak_occupancy"] == 0).all()

    hot = dataclasses.replace(
        CFG,
        # M3.1: collapse requires weak cells — f_weak > 0 keeps the knob hot.
        theta=ThetaConfig(beta=0.3, kappa_A=1.0, lambda_0=0.05, r_seed=2, f_weak=0.5),
    )
    _, _, infos_hot = jax.jit(lambda k: rollout_episode(k, hot, policy, 64))(
        jax.random.PRNGKey(0)
    )
    assert int(infos_hot["coupling_co_active"].sum()) > 0
    # M3.2: co-active counts the perception-range subset of seeded cells,
    # so per step seeded >= co-active, and seeding is live here too.
    assert (infos_hot["seeded_ignitions"] >= infos_hot["coupling_co_active"]).all()
    assert int(infos_hot["seeded_ignitions"].sum()) > 0
    # M3.4-lock addendum channels fire under the hot theta, and every
    # seeded ignition descends from a collapse ball (r_seed = 2 -> 25x).
    assert int(infos_hot["collapse_events"].sum()) > 0
    assert (infos_hot["seeded_ignitions"] <= 25 * infos_hot["collapse_events"]).all()
    assert (
        (infos_hot["weak_occupancy"] >= 0) & (infos_hot["weak_occupancy"] <= 1)
    ).all()
