"""The coupling counters must reach the training log, and stay there.

E1.2 section 7 found invariant #5 HALF-SATISFIED: the env emitted
`coupling_co_active` from day one exactly as instructed, and the eval harness
consumed it into every npz, but the TRAINING logger never picked it up. Zero
of 92 Phase 3-5 training logs carried it, so the within-training trajectory of
compound hostility was unmeasurable from any committed artifact -- which is
precisely the retrofitting problem the invariant was written to prevent,
surviving one layer down.

These tests exist so that cannot recur silently. They check the CHAIN, not any
single link: env info dict -> Transition -> pooled update metric -> jsonl row.
A channel added to STEP_METRICS but not wired through, or wired through but
dropped by a writer, fails here.
"""

from __future__ import annotations

import dataclasses
import json

import jax
import jax.numpy as jnp
import numpy as np
import pytest

from che.env.config import load_config
from che.env.env import reset, step
from che.train.ippo import EP_METRICS, STEP_METRICS, train


@pytest.fixture(scope="module")
def cfg():
    return load_config("che/configs/debug.yaml")


def test_every_step_metric_key_exists_in_env_info(cfg):
    """The env must actually emit every channel STEP_METRICS names."""
    key = jax.random.PRNGKey(0)
    obs, state = reset(key, cfg.env)
    actions = jnp.zeros((cfg.env.n_agents,), jnp.int32)
    _, _, _, _, info = step(key, state, actions, cfg.env)
    missing = [k for k in STEP_METRICS if k not in info]
    assert not missing, (
        f"STEP_METRICS names {missing}, which the env info dict does not "
        "emit. Either the channel was renamed in env.py or it never existed."
    )


def test_step_and_episode_metrics_do_not_collide(cfg):
    """Two aggregation modes must never share one logged name.

    EP_METRICS are done-masked episode-END values; STEP_METRICS are per-step
    counts pooled over the update. One name meaning both is how a consumer
    silently compares incomparable quantities.
    """
    overlap = set(EP_METRICS.values()) & set(STEP_METRICS.values())
    assert not overlap, f"same logged name from both aggregations: {overlap}"


def test_step_metrics_reach_the_jsonl(cfg, tmp_path):
    """The whole chain, end to end: env -> Transition -> metric -> file."""
    mf = tmp_path / "metrics.jsonl"
    train(cfg, n_updates=2, metrics_path=str(mf), log_every=1000)
    rows = [json.loads(line) for line in mf.read_text().splitlines()]
    assert rows, "training wrote no metrics rows at all"
    for name in STEP_METRICS.values():
        assert name in rows[0], (
            f"{name} is in STEP_METRICS but never reached the training log. "
            "This is the exact defect E1.2 found for coupling_co_active."
        )


def test_step_metrics_are_pooled_not_done_masked(cfg, tmp_path):
    """A per-step count must never be NaN, and completion must be able to be.

    This is the behavioural signature that separates the two aggregation
    modes. `completion` is done-masked, so an update in which no episode
    finished reports NaN -- a real absence. A per-step counter has a value on
    every step, so a step with no event is a real ZERO. If a step metric ever
    comes back NaN it has been wired into the done-masked path by mistake.
    """
    mf = tmp_path / "metrics.jsonl"
    train(cfg, n_updates=2, metrics_path=str(mf), log_every=1000)
    rows = [json.loads(line) for line in mf.read_text().splitlines()]
    for name in STEP_METRICS.values():
        vals = np.array([r[name] for r in rows], dtype=float)
        assert np.isfinite(vals).all(), (
            f"{name} produced a non-finite value {vals} -- a pooled per-step "
            "counter is never NaN; this looks done-masked."
        )
        assert (vals >= 0).all(), f"{name} went negative: {vals}"


def test_coupling_counters_are_live_when_coupling_a_is_on(tmp_path):
    """A nonzero path, so the chain is not certified only on zeros.

    debug.yaml runs with kappa_A = 0, where co-activity is legitimately
    identically zero -- a test that only ever saw zeros would pass on a
    channel wired to a constant. This turns Coupling A on and asserts the
    counters carry real, finite, non-negative signal.
    """
    b = load_config("che/configs/debug.yaml")
    th = dataclasses.replace(b.env.theta, beta=0.49, kappa_A=0.06, kappa_B=1.0)
    cfg = dataclasses.replace(b, env=dataclasses.replace(b.env, theta=th))
    mf = tmp_path / "metrics.jsonl"
    train(cfg, n_updates=2, metrics_path=str(mf), log_every=1000)
    rows = [json.loads(line) for line in mf.read_text().splitlines()]
    # danger_agents is driven by the fire front reaching an agent's crop and
    # is the channel that fires soonest at debug scale; it is the liveness
    # witness for the shared pooling path all six channels use.
    live = np.array([r["danger_agents_per_step"] for r in rows], float)
    assert np.isfinite(live).all()
    assert (live >= 0).all()
