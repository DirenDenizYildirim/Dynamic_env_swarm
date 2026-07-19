"""M1.4 tests: episode metrics — identities over a rollout, autoreset
boundary semantics, and visibility in a debug-scale training log."""

import dataclasses
import math

import jax
import jax.numpy as jnp

from che.env.config import Config, EnvConfig, ThetaConfig, TrainConfig
from che.env.types import zeros_state
from che.train.ippo import train
from che.train.rollout import make_random_policy, rollout_episode, step_autoreset


def test_episode_metric_identities_over_rollout():
    theta = ThetaConfig(beta=0.7, iota=0.03, lambda_0=0.01)
    cfg = EnvConfig(grid_size=16, n_agents=4, horizon=64, n_food=8, theta=theta)
    policy = make_random_policy(cfg.n_agents)
    _, dones, infos = jax.jit(
        lambda k: rollout_episode(k, cfg, policy, cfg.horizon)
    )(jax.random.PRNGKey(0))
    assert bool(dones[-1])
    # Episode totals are exactly the running sums of the per-step counts.
    assert (
        jnp.cumsum(infos["deaths_fire"]) == infos["ep_deaths_fire"]
    ).all()
    assert (
        jnp.cumsum(infos["deaths_collapse"]) == infos["ep_deaths_collapse"]
    ).all()
    # At done: survival_rate = 1 - total deaths / n (all start alive).
    total = int(infos["ep_deaths_fire"][-1]) + int(
        infos["ep_deaths_collapse"][-1]
    )
    assert total > 0  # this theta actually kills (fire + collapse)
    assert float(infos["survival_rate"][-1]) == 1.0 - total / cfg.n_agents
    # completion = collected / n_food.
    assert float(infos["completion"][-1]) == 1.0 - float(
        infos["food_remaining"][-1]
    ) / cfg.n_food
    # Both causes individually exercised across the suite matters less than
    # fire here; collapse-kill is pinned in test_lethality.
    assert int(infos["ep_deaths_fire"][-1]) > 0


def test_autoreset_surfaces_ending_episode_and_zeroes_counters():
    cfg = EnvConfig(
        grid_size=8, n_agents=4, horizon=4, n_food=4, theta=ThetaConfig(beta=0.0)
    )
    s = zeros_state(cfg.grid_size, cfg.n_agents, jax.random.PRNGKey(0))
    food = s.food.at[5, 5].set(1).at[6, 6].set(1)  # 2 of 4 uncollected
    s = dataclasses.replace(
        s,
        t=jnp.array(cfg.horizon - 1, jnp.int32),
        agent_alive=jnp.array([True, True, False, False]),
        food=food,
        ep_deaths_fire=jnp.array(1, jnp.int32),
        ep_deaths_collapse=jnp.array(1, jnp.int32),
        ep_smoke_sum=jnp.array(2.0, jnp.float32),
    )
    actions = jnp.zeros((cfg.n_agents,), jnp.int32)  # all stay
    _, s_new, _, done, info = step_autoreset(
        jax.random.PRNGKey(1), s, actions, cfg
    )
    assert bool(done)
    # Info describes the *ending* episode...
    assert float(info["survival_rate"]) == 0.5
    assert float(info["completion"]) == 0.5
    assert int(info["ep_deaths_fire"]) == 1
    assert int(info["ep_deaths_collapse"]) == 1
    # ...while the returned state is the fresh reset.
    assert int(s_new.t) == 0
    assert int(s_new.ep_deaths_fire) == 0
    assert int(s_new.ep_deaths_collapse) == 0
    assert float(s_new.ep_smoke_sum) == 0.0
    assert bool(s_new.agent_alive.all())


def test_mean_smoke_exposure_exact_and_alive_only():
    """Hand-checked exposure: beta=0 (no fire, no emission) with a preset
    uniform smoke field rho = v. Then rho' = e^{-eta} v everywhere, so
    per-step exposure over alive agents is exactly e^{-eta} v regardless of
    positions; dead agents must not contribute."""
    from che.env.env import step

    theta = ThetaConfig(beta=0.0, iota=0.0, lambda_0=0.0, eta=0.25)
    cfg = EnvConfig(grid_size=8, n_agents=4, horizon=16, n_food=4, theta=theta)
    v = 0.8
    s = zeros_state(cfg.grid_size, cfg.n_agents, jax.random.PRNGKey(0))
    s = dataclasses.replace(
        s,
        smoke=jnp.full((8, 8), v, jnp.float32),
        agent_alive=jnp.array([True, True, True, False]),
    )
    actions = jnp.zeros((cfg.n_agents,), jnp.int32)  # all stay
    expected = math.exp(-theta.eta) * v
    _, s1, _, _, info1 = step(jax.random.PRNGKey(1), s, actions, cfg)
    assert float(info1["mean_smoke_exposure"]) == jnp.float32(expected)
    # Step 2: field decays again; running mean averages the two exposures.
    _, _, _, _, info2 = step(jax.random.PRNGKey(2), s1, actions, cfg)
    expected2 = (expected + math.exp(-2 * theta.eta) * v) / 2.0
    assert abs(float(info2["mean_smoke_exposure"]) - expected2) < 1e-6
    # All-dead swarm: exposure contribution is 0, not NaN.
    s_dead = dataclasses.replace(s, agent_alive=jnp.zeros((4,), jnp.bool_))
    _, _, _, _, info_d = step(jax.random.PRNGKey(3), s_dead, actions, cfg)
    assert float(info_d["mean_smoke_exposure"]) == 0.0


def test_metrics_visible_in_debug_training_log():
    cfg = Config(
        env=EnvConfig(grid_size=12, n_agents=3, horizon=32, n_food=6),
        train=TrainConfig(
            n_envs=2, rollout_len=16, n_minibatches=2, n_epochs=2
        ),
    )
    _, history = train(cfg, n_updates=6, seed=0)
    keys = (
        "survival_rate",
        "completion",
        "deaths_fire",
        "deaths_collapse",
        "mean_smoke_exposure",
    )
    assert all(k in row for row in history for k in keys)
    finished = [r for r in history if r["n_episodes"] > 0]
    assert finished  # horizon 32 / rollout 16: episodes end every 2nd update
    for r in finished:
        assert 0.0 <= r["survival_rate"] <= 1.0
        assert 0.0 <= r["completion"] <= 1.0
        assert r["deaths_fire"] >= 0.0 and r["deaths_collapse"] >= 0.0
    # Updates with no finished episode log NaN (NaN-safe aggregation).
    unfinished = [r for r in history if r["n_episodes"] == 0]
    for r in unfinished:
        assert r["survival_rate"] != r["survival_rate"]
