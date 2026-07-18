"""M0.4 gate benchmark: aggregate env-steps/sec of the jitted batched step.

Protocol (phase0 prompt, M0.4):
- jitted batched `step` with uniform-random actions; compile time reported
  separately (AOT lower+compile, not first-call latency);
- >=5 measurement windows of >=30 s each; report median and IQR of
  aggregate env-steps/sec = n_envs * steps-per-env / elapsed;
- matrix: grid {32, 48, 64}^2 x n_envs {256, 1024, 4096} x n_agents {8, 12};
  reference cell (64^2, 1024, 12); peak device memory per cell;
- markdown report to che/bench/results/.

Each matrix cell runs in its own subprocess so peak-memory attribution is
exact and an OOM in one cell cannot kill the sweep. The scan body reduces
every step output (obs, reward, done, info) into a probe scalar — without
this XLA would dead-code-eliminate the observation pipeline and the gate
would overstate throughput.

Usage:
  uv run python -m che.bench.throughput                 # full matrix + report
  uv run python -m che.bench.throughput --quick         # fast smoke run
  uv run python -m che.bench.throughput --cell 64,1024,12   # one cell, JSON
"""

import argparse
import json
import statistics
import subprocess
import sys
import time
from pathlib import Path

GRIDS = (32, 48, 64)
N_ENVS = (256, 1024, 4096)
N_AGENTS = (8, 12)
REFERENCE = (64, 1024, 12)

# Env-only thresholds = 5x the training-throughput gate table (training is
# typically 2-5x slower than env-only; see phase0 prompt M0.4).
TOTAL_STEPS = 86e9
ENV_VERDICTS = (  # (min aggregate env-steps/sec, verdict)
    (1_000_000, "PASS — comfortable"),
    (500_000, "PASS — acceptable"),
    (150_000, "FALLBACK LADDER"),
    (0, "STOP — escalate to human"),
)


def bench_cell(
    grid: int,
    n_envs: int,
    n_agents: int,
    *,
    windows: int,
    window_secs: float,
    chunk: int,
    seed: int = 0,
) -> dict:
    """Benchmark one (grid, n_envs, n_agents) cell; returns a result dict."""
    import jax
    import jax.numpy as jnp

    from che.env.config import EnvConfig
    from che.env.env import N_ACTIONS, reset, step

    cfg = EnvConfig(grid_size=grid, n_agents=n_agents, horizon=256, n_food=32)
    key = jax.random.PRNGKey(seed)
    key, k_reset = jax.random.split(key)
    _, states = jax.jit(
        jax.vmap(reset, in_axes=(0, None)), static_argnums=1
    )(jax.random.split(k_reset, n_envs), cfg)

    step_v = jax.vmap(step, in_axes=(0, 0, 0, None))

    def run_chunk(key, states):
        def body(carry, _):
            key, states = carry
            key, k_act, k_step = jax.random.split(key, 3)
            actions = jax.random.randint(
                k_act, (n_envs, cfg.n_agents), 0, N_ACTIONS, dtype=jnp.int32
            )
            obs, states, rew, done, info = step_v(
                jax.random.split(k_step, n_envs), states, actions, cfg
            )
            # Reduce every output so nothing is dead-code-eliminated.
            probe = (
                rew.sum()
                + obs["grid"].mean()
                + obs["vec"].mean()
                + done.sum().astype(jnp.float32)
                + info["coupling_co_active"].sum().astype(jnp.float32)
                + info["food_remaining"].sum().astype(jnp.float32)
            )
            return (key, states), probe
        (key, states), probes = jax.lax.scan(
            body, (key, states), None, length=chunk
        )
        return key, states, probes.sum()

    donate = (1,) if jax.default_backend() != "cpu" else ()
    jitted = jax.jit(run_chunk, donate_argnums=donate)

    t0 = time.perf_counter()
    compiled = jitted.lower(key, states).compile()
    compile_s = time.perf_counter() - t0

    # Warm-up chunk (excluded from measurement).
    key, states, probe = compiled(key, states)
    jax.block_until_ready(probe)

    rates = []
    for _ in range(windows):
        steps = 0
        t_win = time.perf_counter()
        while time.perf_counter() - t_win < window_secs:
            key, states, probe = compiled(key, states)
            jax.block_until_ready(probe)
            steps += chunk
        elapsed = time.perf_counter() - t_win
        rates.append(n_envs * steps / elapsed)

    if len(rates) >= 2:
        q1, _, q3 = statistics.quantiles(rates, n=4)
        iqr = q3 - q1
    else:
        iqr = 0.0
    dev = jax.local_devices()[0]
    stats = dev.memory_stats() or {}
    return {
        "grid": grid,
        "n_envs": n_envs,
        "n_agents": n_agents,
        "compile_s": round(compile_s, 2),
        "rates": [round(r) for r in rates],
        "median": round(statistics.median(rates)),
        "iqr": round(iqr),
        "peak_bytes": stats.get("peak_bytes_in_use"),
        "platform": dev.platform,
        "device": dev.device_kind,
        "jax_version": jax.__version__,
    }


def verdict_for(env_rate: float) -> str:
    for floor, verdict in ENV_VERDICTS:
        if env_rate >= floor:
            return verdict
    return ENV_VERDICTS[-1][1]


def _fmt_mem(peak_bytes) -> str:
    return f"{peak_bytes / 2**30:.2f}" if peak_bytes else "n/a"


def write_report(results: list[dict], out_path: Path, dollars_per_hour: float):
    """Render the (possibly partial) matrix into the gate report."""
    ok = [r for r in results if "error" not in r]
    header = ok[0] if ok else {"device": "?", "platform": "?", "jax_version": "?"}
    lines = [
        "# M0.4 throughput gate report",
        "",
        f"- Device: **{header['device']}** ({header['platform']}), "
        f"jax {header['jax_version']}",
        f"- Generated: {time.strftime('%Y-%m-%d %H:%M:%S %Z')}",
        "- Protocol: jitted batched step, random actions, AOT compile timed "
        "separately, median/IQR over measurement windows, "
        "aggregate env-steps/sec = n_envs x steps-per-env / elapsed.",
        "",
        "| grid | n_envs | n_agents | compile (s) | median steps/s | IQR "
        "| peak mem (GiB) |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in results:
        mark = " ★" if (r["grid"], r["n_envs"], r["n_agents"]) == REFERENCE else ""
        if "error" in r:
            lines.append(
                f"| {r['grid']}²{mark} | {r['n_envs']} | {r['n_agents']} "
                f"| — | FAILED | — | — |"
            )
        else:
            lines.append(
                f"| {r['grid']}²{mark} | {r['n_envs']} | {r['n_agents']} "
                f"| {r['compile_s']} | {r['median']:,} | {r['iqr']:,} "
                f"| {_fmt_mem(r['peak_bytes'])} |"
            )
    ref = next(
        (
            r
            for r in ok
            if (r["grid"], r["n_envs"], r["n_agents"]) == REFERENCE
        ),
        None,
    )
    best = max(ok, key=lambda r: r["median"], default=None)
    lines.append("")
    if ref is not None:
        lines += _verdict_section(ref, "reference cell (64², 1024, 12)",
                                  dollars_per_hour)
    elif best is not None:
        lines += _verdict_section(
            best,
            f"best measured cell ({best['grid']}², {best['n_envs']}, "
            f"{best['n_agents']}) — reference cell missing",
            dollars_per_hour,
        )
    for r in results:
        if "error" in r:
            lines += ["", f"## Failure: {r['grid']}²/{r['n_envs']}/"
                      f"{r['n_agents']}", "```", r["error"][-2000:], "```"]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n")


def _verdict_section(r: dict, label: str, dollars_per_hour: float) -> list[str]:
    env_rate = r["median"]
    lines = [
        f"## Verdict — {label}",
        "",
        f"- Env-only aggregate throughput: **{env_rate:,} steps/s**",
        f"- Env-only verdict (5x training thresholds): "
        f"**{verdict_for(env_rate)}**",
        "",
        "Budget projection (86e9 aggregate steps; training typically 2-5x "
        "slower than env-only):",
        "",
        "| assumed training slowdown | training steps/s | GPU-hours | "
        f"spot cost (x2 buffer @ ${dollars_per_hour}/h) |",
        "|---|---|---|---|",
    ]
    for slow in (2, 5):
        tp = env_rate / slow
        hours = TOTAL_STEPS / tp / 3600 if tp else float("inf")
        cost = hours * dollars_per_hour * 2
        lines.append(
            f"| {slow}x | {tp:,.0f} | {hours:,.0f} | ~${cost:,.0f} |"
        )
    lines.append("")
    lines.append(
        "Final go/no-go uses *training* throughput measured at M0.6; this "
        "env-only figure is the leading indicator."
    )
    return lines


def run_matrix(args) -> list[dict]:
    cells = (
        [tuple(int(x) for x in c.split(",")) for c in args.cells.split(";")]
        if args.cells
        else [
            (g, e, a) for g in GRIDS for e in N_ENVS for a in N_AGENTS
        ]
    )
    # Ascending footprint: cheap cells first, so a late OOM leaves a report.
    cells.sort(key=lambda c: c[0] * c[0] * c[1] * c[2])
    results = []
    out_path = Path(args.out)
    for grid, n_envs, n_agents in cells:
        print(f"[gate] cell grid={grid}² envs={n_envs} agents={n_agents} ...",
              flush=True)
        cmd = [
            sys.executable, "-m", "che.bench.throughput",
            "--cell", f"{grid},{n_envs},{n_agents}",
            "--windows", str(args.windows),
            "--window-secs", str(args.window_secs),
            "--chunk", str(args.chunk),
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode == 0:
            results.append(json.loads(proc.stdout.strip().splitlines()[-1]))
            print(f"[gate]   median {results[-1]['median']:,} steps/s")
        else:
            results.append({
                "grid": grid, "n_envs": n_envs, "n_agents": n_agents,
                "error": proc.stderr,
            })
            print("[gate]   FAILED (see report)")
        write_report(results, out_path, args.dollars_per_hour)  # incremental
    print(f"[gate] report written to {out_path}")
    return results


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--cell", help="G,E,A: run one cell, print JSON")
    p.add_argument("--cells", help='subset, e.g. "32,256,8;64,1024,12"')
    p.add_argument("--windows", type=int, default=5)
    p.add_argument("--window-secs", type=float, default=30.0)
    p.add_argument("--chunk", type=int, default=256,
                   help="env steps per compiled call")
    p.add_argument("--quick", action="store_true",
                   help="smoke-run: 2 windows x 3 s, chunk 64")
    p.add_argument("--out", default="che/bench/results/gate_report.md")
    p.add_argument("--dollars-per-hour", type=float, default=0.45)
    args = p.parse_args()
    if args.quick:
        args.windows, args.window_secs, args.chunk = 2, 3.0, 64
    if args.cell:
        grid, n_envs, n_agents = (int(x) for x in args.cell.split(","))
        result = bench_cell(
            grid, n_envs, n_agents,
            windows=args.windows, window_secs=args.window_secs,
            chunk=args.chunk,
        )
        print(json.dumps(result))
    else:
        run_matrix(args)


if __name__ == "__main__":
    main()
