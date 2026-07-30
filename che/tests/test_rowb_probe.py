"""M5.1j staged row-B probe: the trail must survive the process (CPU, tiny).

The module exists because three row-B failures produced no diagnostic, so the
properties worth pinning are about the ARTIFACT, not about throughput:

1. the JSON is rewritten after every stage, so a SIGKILL mid-ladder still
   leaves everything up to that stage on disk;
2. stages are recorded in ladder order with the depth the caller asked for;
3. a stage that raises is recorded and stops the ladder rather than
   propagating — a failed row B is a measurement here, not a crash;
4. the toolchain keys the 2x2 verdict reads are actually present.
"""

import json

import jax
import pytest

from che.bench.rowb_probe import STAGES, Trail, run, toolchain
from che.env.config import Config, EnvConfig, ThetaConfig, TrainConfig

TINY = Config(
    env=EnvConfig(grid_size=16, n_agents=4, horizon=32, n_food=6,
                  theta=ThetaConfig(beta=0.35, kappa_B=1.0)),
    train=TrainConfig(n_envs=2, pop_size=2, rollout_len=8, n_minibatches=2,
                      n_epochs=2, pbt_interval=2),
)


def test_trail_is_on_disk_after_every_add(tmp_path):
    """The whole point: no artifact is deferred to the end of the run."""
    path = tmp_path / "trail.json"
    trail = Trail(path)
    trail.add(stage="provenance", ok=True)
    assert json.loads(path.read_text()) == [{"stage": "provenance", "ok": True}]
    trail.add(stage="init", ok=True, seconds=1.0)
    rows = json.loads(path.read_text())
    assert [r["stage"] for r in rows] == ["provenance", "init"]


def test_toolchain_carries_what_the_2x2_verdict_reads():
    tc = toolchain()
    for key in ("jax", "jaxlib", "backend", "device_kind", "disable_jit"):
        assert key in tc, key
    json.dumps(tc)  # the script parses this out of the artifact


def test_unknown_stage_is_a_loud_error():
    with pytest.raises(ValueError, match="unknown stage"):
        run(TINY, stage="nonsense")


def test_provenance_stage_touches_no_device_memory(tmp_path):
    rows = run(TINY, stage="provenance", out_json=tmp_path / "p.json")
    assert [r["stage"] for r in rows] == ["provenance"]
    assert (tmp_path / "p.json").exists()


@pytest.mark.skipif(
    bool(jax.config.jax_disable_jit),
    reason="compile/one stages AOT-compile by design; skipped without jit",
)
def test_ladder_reaches_one_and_reports_a_cold_rate(tmp_path):
    rows = run(TINY, stage="one", out_json=tmp_path / "one.json")
    reached = [r["stage"] for r in rows if r.get("ok")]
    assert reached == ["provenance", "init", "compile", "one"], rows
    assert reached == list(STAGES[: len(reached)])  # ladder order, no skipping
    one = next(r for r in rows if r["stage"] == "one")
    assert one["steps"] == 2 * 2 * 8 * 2  # pop x envs x rollout x K_pbt
    assert one["steps_per_s"] > 0
    json.dumps(rows)  # the verdict script re-reads this


def test_disable_jit_degrades_to_init_without_pretending_otherwise():
    """Under JAX_DISABLE_JIT the compile stages are skipped, and the skip is
    RECORDED — a probe that silently measured eager execution would report a
    throughput the gate config does not have."""
    with jax.disable_jit():
        rows = run(TINY, stage="windows")
    stages = [r["stage"] for r in rows]
    assert "compile" in stages
    skipped = next(r for r in rows if r["stage"] == "compile")
    assert skipped.get("skipped") == "JAX_DISABLE_JIT=1"
    assert not any(r["stage"] == "windows" for r in rows)
