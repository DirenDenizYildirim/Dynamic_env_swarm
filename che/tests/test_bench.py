"""Smoke test for the M0.4 gate benchmark harness (tiny cell, CPU)."""

import json

import jax
import pytest

from che.bench.throughput import bench_cell, verdict_for


@pytest.mark.skipif(
    bool(jax.config.jax_disable_jit),
    reason="bench AOT-compiles by design; meaningless without jit",
)
def test_bench_cell_runs_and_is_serializable():
    r = bench_cell(16, 4, 4, windows=2, window_secs=0.3, chunk=8)
    assert r["median"] > 0
    assert len(r["rates"]) == 2
    assert all(rate > 0 for rate in r["rates"])
    assert r["compile_s"] > 0
    json.dumps(r)  # subprocess protocol requires JSON-serializable output


@pytest.mark.skipif(
    bool(jax.config.jax_disable_jit),
    reason="dead-code elimination is a compiler behaviour; needs jit",
)
def test_probe_keeps_every_subsystem_alive_including_comms():
    """The bench must measure the env it claims to measure.

    M5.1 regression: `obs["links"]` was not reduced, XLA eliminated the
    whole M5.0 link kernel, and the first comms bench row measured an env
    with no comms in it — reporting a *faster* env after work was added.
    The link graph is the only [n_agents, n_agents] tensor in the step, so
    counting those in the optimized HLO detects its removal exactly.
    """
    import jax.numpy as jnp

    from che.bench.throughput import keepalive_probe
    from che.env.config import EnvConfig
    from che.env.env import N_ACTIONS, reset, step

    n_agents, n_envs = 4, 2
    cfg = EnvConfig(grid_size=16, n_agents=n_agents, horizon=256, n_food=8)
    key = jax.random.PRNGKey(0)
    k_reset, k_step, k_act = jax.random.split(key, 3)
    _, states = jax.jit(jax.vmap(reset, in_axes=(0, None)), static_argnums=1)(
        jax.random.split(k_reset, n_envs), cfg
    )
    actions = jax.random.randint(
        k_act, (n_envs, n_agents), 0, N_ACTIONS, dtype=jnp.int32
    )

    def body(key, states, actions):
        obs, states, rew, done, info = jax.vmap(step, in_axes=(0, 0, 0, None))(
            jax.random.split(key, n_envs), states, actions, cfg
        )
        return keepalive_probe(rew, done, obs, info)

    hlo = jax.jit(body).lower(k_step, states, actions).compile().as_text()
    n_link_tensors = hlo.count(f"[{n_agents},{n_agents}]") + hlo.count(
        f"[{n_envs},{n_agents},{n_agents}]"
    )
    assert n_link_tensors > 1, (
        "comms kernel appears dead-code-eliminated: no [n_agents, n_agents] "
        "tensors survived in the optimized HLO — the bench would silently "
        "measure an env without the comms axis"
    )


def test_verdict_thresholds():
    assert verdict_for(2_000_000).startswith("PASS — comfortable")
    assert verdict_for(600_000).startswith("PASS — acceptable")
    assert verdict_for(200_000) == "FALLBACK LADDER"
    assert verdict_for(50_000).startswith("STOP")
