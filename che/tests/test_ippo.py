"""M0.5 tests: networks, autoreset, GAE, training smoke, kill-and-resume,
SIGTERM checkpointing. Tiny shared config keeps compiles cached (lru_cache
in make_train_fns) and the CPU suite under budget."""

import dataclasses
import os
import signal
import threading

import jax
import jax.numpy as jnp
import numpy as np
import pytest

from che.env.config import Config, EnvConfig, TrainConfig
from che.env.env import N_ACTIONS, reset
from che.env.observation import N_PLANES
from che.train.ippo import (
    compute_gae,
    config_hash,
    make_train_fns,
    random_baseline,
    train,
)
from che.train.networks import ActorCritic
from che.train.rollout import step_autoreset

CFG = Config(
    env=EnvConfig(grid_size=12, n_agents=3, horizon=32, n_food=6),
    train=TrainConfig(
        n_envs=2, rollout_len=16, n_minibatches=2, n_epochs=2, ckpt_interval=2
    ),
)


def test_network_shapes_arbitrary_batch_dims():
    net = ActorCritic(N_ACTIONS)
    k = CFG.env.obs_window
    params = net.init(
        jax.random.PRNGKey(0),
        jnp.zeros((1, k, k, N_PLANES)),
        jnp.zeros((1, 4)),
    )
    grid = jnp.zeros((5, 3, k, k, N_PLANES))
    vec = jnp.zeros((5, 3, 4))
    logits, value = net.apply(params, grid, vec)
    assert logits.shape == (5, 3, N_ACTIONS)
    assert value.shape == (5, 3)
    assert jnp.isfinite(logits).all() and jnp.isfinite(value).all()


def test_autoreset_on_horizon():
    _, state = reset(jax.random.PRNGKey(0), CFG.env)
    state = dataclasses.replace(
        state,
        t=jnp.array(CFG.env.horizon - 1, jnp.int32),
        food=jnp.zeros_like(state.food),
    )
    actions = jnp.zeros((CFG.env.n_agents,), jnp.int32)
    _, new_state, _, done, _ = step_autoreset(
        jax.random.PRNGKey(1), state, actions, CFG.env
    )
    assert bool(done)
    assert int(new_state.t) == 0  # fresh episode
    assert int(new_state.food.sum()) == CFG.env.n_food  # food respawned


def test_gae_closed_form():
    # T=2, single env/agent, no dones: hand-computed GAE.
    gamma, lam = 0.9, 0.8
    rewards = jnp.array([[1.0], [2.0]])
    values = jnp.array([[0.5], [1.5]])
    dones = jnp.array([[False], [False]])
    last_value = jnp.array([2.5])
    adv, targets = compute_gae(
        rewards, values, dones, last_value, gamma=gamma, gae_lambda=lam
    )
    delta1 = 2.0 + gamma * 2.5 - 1.5
    delta0 = 1.0 + gamma * 1.5 - 0.5
    expect1 = delta1
    expect0 = delta0 + gamma * lam * expect1
    np.testing.assert_allclose(adv[:, 0], [expect0, expect1], rtol=1e-6)
    np.testing.assert_allclose(targets, adv + values, rtol=1e-6)
    # A done at t=0 must cut bootstrapping and the GAE recursion.
    adv_cut, _ = compute_gae(
        rewards, values, jnp.array([[True], [False]]), last_value,
        gamma=gamma, gae_lambda=lam,
    )
    np.testing.assert_allclose(adv_cut[0, 0], 1.0 - 0.5, rtol=1e-6)


def test_training_smoke_and_params_change():
    fns = make_train_fns(CFG)
    runner = fns.init(jax.random.PRNGKey(0))
    params_before = jax.tree_util.tree_map(
        lambda x: x.copy(), runner.train_state.params
    )
    runner, metrics = fns.chunk(runner, 2)
    for name in ("total_loss", "pg_loss", "v_loss", "entropy"):
        assert jnp.isfinite(metrics[name]).all(), name
    assert metrics["n_episodes"].sum() >= 2  # horizon 32, 16*2 steps/update
    diffs = jax.tree_util.tree_map(
        lambda a, b: float(jnp.abs(a - b).max()),
        params_before,
        runner.train_state.params,
    )
    assert max(jax.tree_util.tree_leaves(diffs)) > 0.0


def test_kill_and_resume(tmp_path):
    ckpt = tmp_path / "ckpt"
    _, hist1 = train(CFG, n_updates=2, ckpt_dir=ckpt, seed=0)
    assert [r["update"] for r in hist1] == [1, 2]
    # Resume continues the counter and losses stay sane.
    _, hist2 = train(CFG, n_updates=4, ckpt_dir=ckpt, seed=0, resume=True)
    assert [r["update"] for r in hist2] == [3, 4]
    assert all(np.isfinite(r["total_loss"]) for r in hist2)
    # Config-hash mismatch must refuse to resume.
    other = dataclasses.replace(
        CFG, train=dataclasses.replace(CFG.train, lr=1e-3)
    )
    assert config_hash(other) != config_hash(CFG)
    with pytest.raises(ValueError, match="hash mismatch"):
        train(other, n_updates=6, ckpt_dir=ckpt, resume=True)


def test_sigterm_saves_and_stops_early(tmp_path):
    ckpt = tmp_path / "ckpt_sigterm"
    timer = threading.Timer(0.5, os.kill, (os.getpid(), signal.SIGTERM))
    timer.start()
    try:
        _, hist = train(
            CFG, n_updates=500, ckpt_dir=ckpt, seed=0, handle_sigterm=True
        )
    finally:
        timer.cancel()
    assert len(hist) < 500  # interrupted well before completion
    # The interrupt left a usable checkpoint: resume works.
    _, hist2 = train(
        CFG, n_updates=len(hist) + 2, ckpt_dir=ckpt, seed=0, resume=True
    )
    assert [r["update"] for r in hist2] == [len(hist) + 1, len(hist) + 2]


def test_random_baseline_runs():
    b = random_baseline(CFG, n_episodes=8)
    assert 0.0 <= b["mean_return"] <= CFG.env.n_food
    assert 0.0 <= b["survival_rate"] <= 1.0
    assert 0.0 <= b["completion"] <= 1.0
    assert b["deaths_fire"] >= 0.0 and b["deaths_collapse"] >= 0.0
