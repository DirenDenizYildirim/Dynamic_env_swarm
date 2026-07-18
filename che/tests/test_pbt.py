"""M0.6 tests: truncation selection/mutation logic, population training
smoke (exploits trigger, diversity persists), and population resume."""

import jax
import jax.numpy as jnp
import numpy as np

from che.env.config import Config, EnvConfig, TrainConfig
from che.train.pbt import (
    fitness_from_metrics,
    make_pbt_fns,
    select_and_mutate,
    train_population,
)

CFG = Config(
    env=EnvConfig(grid_size=12, n_agents=3, horizon=32, n_food=6),
    train=TrainConfig(
        n_envs=2,
        rollout_len=16,
        n_minibatches=2,
        n_epochs=2,
        pop_size=4,
        pbt_interval=2,
    ),
)


def _params_equal(a, b) -> bool:
    return all(
        bool(jnp.array_equal(x, y))
        for x, y in zip(
            jax.tree_util.tree_leaves(a), jax.tree_util.tree_leaves(b),
            strict=True,
        )
    )


def _member(tree, i):
    return jax.tree_util.tree_map(lambda x: x[i], tree)


def test_fitness_nan_aware():
    mr = np.array([[1.0, np.nan], [np.nan, np.nan], [2.0, 4.0]])
    fit = fitness_from_metrics(mr)
    np.testing.assert_allclose(fit, [1.0, 0.0, 3.0])


def test_select_and_mutate_truncation():
    pop = make_pbt_fns(CFG).init(jax.random.PRNGKey(0))
    fitness = np.array([0.0, 1.0, 2.0, 3.0])  # member 0 worst, 3 best
    lr_before = np.asarray(pop.hyper["lr"]).copy()
    new_pop, events = select_and_mutate(
        pop, fitness, np.random.default_rng(0)
    )
    # P=4 -> quartile of 1: exactly one exploit, 0 <- 3.
    assert len(events) == 1
    assert events[0]["target"] == 0 and events[0]["source"] == 3
    # Weights copied from the source...
    assert _params_equal(
        _member(new_pop.train_state.params, 0),
        _member(pop.train_state.params, 3),
    )
    # ...survivors untouched (params and hyper).
    for m in (1, 2, 3):
        assert _params_equal(
            _member(new_pop.train_state.params, m),
            _member(pop.train_state.params, m),
        )
        assert float(new_pop.hyper["lr"][m]) == lr_before[m]
    # Mutated hyper is source value x 0.8 or x 1.25.
    ratio = float(new_pop.hyper["lr"][0]) / lr_before[3]
    assert min(abs(ratio - 0.8), abs(ratio - 1.25)) < 1e-6
    # Hyperparam diversity persists.
    assert len(set(np.asarray(new_pop.hyper["lr"]).tolist())) > 1


def test_population_trains_and_logs_exploits(tmp_path):
    metrics_path = tmp_path / "m.jsonl"
    events_path = tmp_path / "e.jsonl"
    pop, rows, events = train_population(
        CFG,
        rounds=2,
        seed=0,
        metrics_path=metrics_path,
        events_path=events_path,
    )
    # 2 rounds x K_pbt=2 updates x P=4 members of metric rows.
    assert len(rows) == 2 * 2 * 4
    assert all(np.isfinite(r["total_loss"]) for r in rows)
    # Selection provably triggered: one exploit per round at P=4.
    assert len(events) == 2
    assert metrics_path.exists() and events_path.exists()
    # Diversity has not collapsed to a single value.
    assert len(set(np.asarray(pop.hyper["lr"]).tolist())) > 1
    assert len(set(np.asarray(pop.hyper["ent_coef"]).tolist())) > 1


def test_population_resume(tmp_path):
    ckpt = tmp_path / "ckpt_pop"
    train_population(CFG, rounds=1, seed=0, ckpt_dir=ckpt)
    pop, rows, _ = train_population(
        CFG, rounds=2, seed=0, ckpt_dir=ckpt, resume=True
    )
    # Only round 1 (index 1..2) ran in the second call.
    assert {r["round"] for r in rows} == {1}
    assert all(np.isfinite(r["total_loss"]) for r in rows)
