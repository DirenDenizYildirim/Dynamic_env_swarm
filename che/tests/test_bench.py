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


def test_verdict_thresholds():
    assert verdict_for(2_000_000).startswith("PASS — comfortable")
    assert verdict_for(600_000).startswith("PASS — acceptable")
    assert verdict_for(200_000) == "FALLBACK LADDER"
    assert verdict_for(50_000).startswith("STOP")
