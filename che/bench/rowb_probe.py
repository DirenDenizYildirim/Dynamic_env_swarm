"""Staged execution probe for the population training step (M5.1j).

Why this exists. Row B — the re-anchored gate measurement
(`pbt.py --bench --config gate_pop12.yaml`) — has failed three times and
produced three different artifacts: an OOM naming 49.08 GiB (m51d), a
bounded OOM after 1112 s retrying a fixed 5.72 GiB allocation (m51i, first
attempt), and a bare `rc=137` at the 1800 s backstop (m51i, second). The
last one carries no diagnostic at all, and `pbt.bench_population` is
atomic from the outside: init, compile, warm-up and five timing windows all
happen inside one call, so a kill anywhere in it looks the same.

This module runs the same ladder in *stages that report as they go*:

    provenance -> init -> compile -> one -> windows

Each stage prints one flushed line, records device `memory_stats()`, and
the JSON is rewritten after **every** stage. So a SIGKILL mid-stage leaves
everything up to that stage on disk, and the artifact says how deep the
process got instead of only that it died. `--stage` selects the deepest
stage to attempt; a stage that raises records the exception, writes, and
exits non-zero.

What each stage separates:

- **init** allocates the population state (params, optimizer state, env
  states, ~0.14 GiB at the gate config) and nothing else. If this hangs,
  the problem is upstream of the update step — driver, context creation,
  or the preallocated arena itself.
- **compile** is what `memprobe.py` already measures, repeated here so the
  requirement is recorded in the same artifact as the execution attempt
  rather than in a different run.
- **one** executes exactly one K_pbt-update chunk. This is the decisive
  stage: it separates "compiles but cannot allocate its working set at
  runtime" from "cannot compile" from "runs, and the bench harness on top
  is the problem".
- **windows** defers to `pbt.bench_population`, so a green ladder ends in
  the real gate number produced by the instrument the ruling named.

Nothing here changes a config or an experiment quantity; it is a
measurement of an instrument that has been failing opaquely.

  uv run python -m che.bench.rowb_probe --config che/configs/gate_pop12.yaml \
      --stage one --out-json rowb.json
"""

import argparse
import json
import time
from pathlib import Path

GIB = 2**30
STAGES = ("provenance", "init", "compile", "one", "windows")


def toolchain() -> dict:
    """Toolchain identity — the thing two rentals can differ in silently.

    The +2.85 GiB requirement drift between m51g and m51i (decision_log.md,
    "Phase-5 delegated rulings, round 2") is either a GPU-specific fusion
    change or a toolchain change, and no artifact from either run recorded
    enough to tell. Everything cheap enough to collect is collected.
    """
    import jax
    import jaxlib

    dev = jax.local_devices()[0]
    return {
        "jax": jax.__version__,
        "jaxlib": getattr(jaxlib, "__version__", "unknown"),
        "backend": jax.default_backend(),
        "device_kind": dev.device_kind,
        "device_count": jax.local_device_count(),
        "disable_jit": bool(jax.config.jax_disable_jit),
    }


def device_memory() -> dict:
    """Raw `memory_stats()` in bytes, or {} on a backend that declines.

    Kept in bytes: the GiB conversion is for the printed line only, and a
    figure that has been through a float division twice is harder to
    reconcile against XLA's own error text.
    """
    import jax

    stats = jax.local_devices()[0].memory_stats() or {}
    return {k: int(v) for k, v in stats.items() if isinstance(v, (int, float))}


def _mem_line(stats: dict) -> str:
    if not stats:
        return "memory_stats unavailable"
    parts = []
    for key, label in (
        ("bytes_in_use", "in-use"),
        ("peak_bytes_in_use", "peak"),
        ("bytes_limit", "limit"),
        ("largest_free_block_bytes", "largest-free"),
    ):
        if key in stats:
            parts.append(f"{label} {stats[key] / GIB:.2f} GiB")
    return ", ".join(parts) or "memory_stats empty"


class Trail:
    """Append-and-flush record of stages, rewritten to disk after each one.

    The whole point of this module is that the artifact survives a SIGKILL,
    so the file is rewritten every time rather than once at the end.
    """

    def __init__(self, out_json: str | Path | None):
        self.out_json = Path(out_json) if out_json else None
        self.rows: list[dict] = []

    def add(self, **row) -> dict:
        self.rows.append(row)
        self.flush()
        return row

    def flush(self) -> None:
        if self.out_json:
            self.out_json.parent.mkdir(parents=True, exist_ok=True)
            self.out_json.write_text(json.dumps(self.rows, indent=1) + "\n")


def run(
    cfg,
    *,
    stage: str = "one",
    seed: int = 0,
    windows: int = 3,
    window_secs: float = 30.0,
    out_json: str | Path | None = None,
) -> list[dict]:
    """Run the ladder up to and including `stage`; return the trail.

    Raises nothing: a failing stage is recorded with its exception text and
    the ladder stops there. The caller decides what a partial trail means
    (see `main`, which exits non-zero on one).
    """
    import jax

    from che.train.pbt import bench_population, make_pbt_fns

    if stage not in STAGES:
        raise ValueError(f"unknown stage {stage!r}; pick one of {STAGES}")
    depth = STAGES.index(stage)
    trail = Trail(out_json)

    tcfg = cfg.train
    tc = toolchain()
    # The artifact must say what was probed, not only what it found — a size
    # bisect produces several trails and they have to be tellable apart.
    trail.add(stage="provenance", ok=True, **tc, memory=device_memory(),
              pop_size=tcfg.pop_size, n_envs=tcfg.n_envs,
              n_minibatches=tcfg.n_minibatches, rollout_len=tcfg.rollout_len,
              pbt_interval=tcfg.pbt_interval, uint8_obs=tcfg.uint8_obs,
              remat=tcfg.remat)
    print(f"[rowb] toolchain jax {tc['jax']} / jaxlib {tc['jaxlib']} on "
          f"{tc['backend']} ({tc['device_kind']}, {tc['device_count']} dev)",
          flush=True)
    print(f"[rowb] probing pop {tcfg.pop_size} x envs {tcfg.n_envs} x rollout "
          f"{tcfg.rollout_len}, K_pbt {tcfg.pbt_interval}, nmb "
          f"{tcfg.n_minibatches}, uint8 {tcfg.uint8_obs}, remat {tcfg.remat}",
          flush=True)
    print(f"[rowb] device at rest: {_mem_line(device_memory())}", flush=True)
    if depth == 0:
        return trail.rows

    # Stages that AOT-compile are meaningless without jit (test_bench.py
    # precedent), so they are skipped rather than silently measuring eager.
    if tc["disable_jit"] and depth >= STAGES.index("compile"):
        trail.add(stage="compile", ok=None, skipped="JAX_DISABLE_JIT=1")
        print("[rowb] compile/one/windows skipped: JAX_DISABLE_JIT=1", flush=True)
        depth = STAGES.index("init")

    pfns = make_pbt_fns(cfg)

    print("[rowb] stage init: allocating the population state ...", flush=True)
    t0 = time.perf_counter()
    try:
        pop = jax.block_until_ready(pfns.init(jax.random.PRNGKey(seed)))
    except Exception as exc:  # noqa: BLE001 — the text carries the diagnosis
        trail.add(stage="init", ok=False, seconds=time.perf_counter() - t0,
                  error=str(exc)[:2000], memory=device_memory())
        print(f"[rowb] stage init FAILED: {str(exc)[:200]}", flush=True)
        return trail.rows
    dt = time.perf_counter() - t0
    mem = device_memory()
    trail.add(stage="init", ok=True, seconds=dt, memory=mem)
    print(f"[rowb] stage init OK in {dt:.1f} s — {_mem_line(mem)}", flush=True)
    if depth <= STAGES.index("init"):
        return trail.rows

    print("[rowb] stage compile: lowering + compiling the pop chunk ...", flush=True)
    t0 = time.perf_counter()
    try:
        compiled = pfns.chunk.lower(pop).compile()
        analysis = compiled.memory_analysis()
    except Exception as exc:  # noqa: BLE001
        trail.add(stage="compile", ok=False, seconds=time.perf_counter() - t0,
                  error=str(exc)[:2000], memory=device_memory())
        print(f"[rowb] stage compile FAILED: {str(exc)[:200]}", flush=True)
        return trail.rows
    dt = time.perf_counter() - t0
    temp = getattr(analysis, "temp_size_in_bytes", 0) or 0 if analysis else 0
    trail.add(stage="compile", ok=True, seconds=dt, temp_bytes=int(temp),
              temp_gib=temp / GIB, memory=device_memory())
    print(f"[rowb] stage compile OK in {dt:.1f} s — temp {temp / GIB:.2f} GiB",
          flush=True)
    if depth <= STAGES.index("compile"):
        return trail.rows

    print("[rowb] stage one: executing a single K_pbt chunk ...", flush=True)
    t0 = time.perf_counter()
    try:
        pop_out, metrics = compiled(pop)
        jax.block_until_ready(metrics["total_loss"])
    except Exception as exc:  # noqa: BLE001
        trail.add(stage="one", ok=False, seconds=time.perf_counter() - t0,
                  error=str(exc)[:2000], memory=device_memory())
        print(f"[rowb] stage one FAILED: {str(exc)[:200]}", flush=True)
        return trail.rows
    dt = time.perf_counter() - t0
    tcfg = cfg.train
    steps = tcfg.pop_size * tcfg.n_envs * tcfg.rollout_len * tcfg.pbt_interval
    mem = device_memory()
    trail.add(stage="one", ok=True, seconds=dt, steps=steps,
              steps_per_s=steps / dt, memory=mem)
    print(f"[rowb] stage one OK in {dt:.1f} s — {steps:,} steps, "
          f"{steps / dt:,.0f} steps/s (first call, includes no warm-up "
          f"amortization) — {_mem_line(mem)}", flush=True)
    del pop_out
    if depth <= STAGES.index("one"):
        return trail.rows

    print(f"[rowb] stage windows: {windows} x {window_secs:.0f} s ...", flush=True)
    t0 = time.perf_counter()
    try:
        result = bench_population(cfg, windows=windows,
                                  window_secs=window_secs, seed=seed)
    except Exception as exc:  # noqa: BLE001
        trail.add(stage="windows", ok=False, seconds=time.perf_counter() - t0,
                  error=str(exc)[:2000], memory=device_memory())
        print(f"[rowb] stage windows FAILED: {str(exc)[:200]}", flush=True)
        return trail.rows
    trail.add(stage="windows", ok=True, seconds=time.perf_counter() - t0,
              **result)
    print(f"[rowb] stage windows OK — median {result['median']:,} steps/s "
          f"(IQR {result['iqr']:,})", flush=True)
    return trail.rows


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--config", default="che/configs/gate_pop12.yaml")
    p.add_argument("--stage", default="one", choices=STAGES,
                   help="deepest stage to attempt (cumulative)")
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--windows", type=int, default=3)
    p.add_argument("--window-secs", type=float, default=30.0)
    p.add_argument("--out-json")
    # Size overrides for a "does it execute AT ALL" bisect. These change what
    # is being run and can never produce a gate number — a rate measured under
    # them is a diagnostic, and the trail records the effective config so the
    # two can never be confused later.
    p.add_argument("--pop-size", type=int, help="diagnostic override")
    p.add_argument("--n-envs", type=int, help="diagnostic override")
    p.add_argument("--n-minibatches", type=int, help="diagnostic override")
    args = p.parse_args(argv)

    import dataclasses

    from che.env.config import load_config

    cfg = load_config(args.config)
    overrides = {k: v for k, v in (("pop_size", args.pop_size),
                                   ("n_envs", args.n_envs),
                                   ("n_minibatches", args.n_minibatches))
                 if v is not None}
    if overrides:
        cfg = dataclasses.replace(cfg,
                                  train=dataclasses.replace(cfg.train, **overrides))
        print(f"[rowb] DIAGNOSTIC OVERRIDES {overrides} — this is not a gate "
              "configuration and any rate below is not a gate number",
              flush=True)
    rows = run(cfg, stage=args.stage, seed=args.seed,
               windows=args.windows, window_secs=args.window_secs,
               out_json=args.out_json)
    reached = [r["stage"] for r in rows if r.get("ok")]
    failed = [r for r in rows if r.get("ok") is False]
    print(f"\n[rowb] reached: {' -> '.join(reached) or 'nothing'}")
    if failed:
        print(f"[rowb] FAILED AT: {failed[-1]['stage']}")
        return 2
    if args.stage not in reached:
        print(f"[rowb] INCOMPLETE: asked for {args.stage}, did not reach it")
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
