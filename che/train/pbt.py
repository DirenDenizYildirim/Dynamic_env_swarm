"""PBT population outer loop (Milestone 0.6) — the evolutionary+MARL hybrid.

Population P as the *outermost vmap* over per-member (params, opt_state,
hyperparams {lr, ent_coef}, env batch, PRNG key): the K_pbt inner IPPO
updates for all members run inside one compiled call. Every K_pbt updates,
truncation selection (Jaderberg et al. 2017) runs at the PBT boundary,
*outside* jit: fitness = mean episodic return over the chunk window; the
bottom quartile copies a uniformly sampled top-quartile member's weights and
optimizer state and mutates its hyperparams by xU{0.8, 1.25}. Exploit events
are logged (JSONL) so selection is provably triggering; env states and PRNG
streams stay member-own.

Also provides the M0.6 second gate measurement: aggregate *training*
steps/sec with the full population, appended to the M0.4 gate report and
judged against the phase-prompt training thresholds.
"""

import argparse
import functools
import json
import signal
import statistics
import time
from pathlib import Path
from typing import NamedTuple

import jax
import jax.numpy as jnp
import numpy as np
import orbax.checkpoint as ocp

from che.env.config import Config, load_config
from che.train.ippo import (
    _SIGTERM,
    Runner,
    _ckpt_manager,
    _sigterm_handler,
    config_hash,
    make_train_fns,
)

TOTAL_STEPS = 86e9
TRAIN_VERDICTS = (  # (min aggregate training steps/sec, verdict) — phase table
    (200_000, "PASS — comfortable"),
    (100_000, "PASS — acceptable"),
    (30_000, "FALLBACK LADDER"),
    (0, "STOP — escalate to human"),
)


class PBTFns(NamedTuple):
    init: object  # jitted (key) -> population Runner (leading axis P)
    chunk: object  # jitted (pop Runner) -> (pop Runner, metrics [P, K_pbt])


@functools.lru_cache(maxsize=8)
def make_pbt_fns(cfg: Config) -> PBTFns:
    fns = make_train_fns(cfg)
    pop_size = cfg.train.pop_size
    k_pbt = cfg.train.pbt_interval

    def init_pop(key: jax.Array) -> Runner:
        key, k_init, k_lr, k_ent = jax.random.split(key, 4)
        pop = jax.vmap(fns.init_raw)(jax.random.split(k_init, pop_size))
        # DECISION: initial hyperparam diversity is log-uniform x2^U(-1, 1)
        # around the config values; PBT mutation then explores from there.
        lr_f = 2.0 ** jax.random.uniform(k_lr, (pop_size,), minval=-1.0, maxval=1.0)
        ent_f = 2.0 ** jax.random.uniform(k_ent, (pop_size,), minval=-1.0, maxval=1.0)
        return pop._replace(
            hyper={
                "lr": pop.hyper["lr"] * lr_f,
                "ent_coef": pop.hyper["ent_coef"] * ent_f,
            }
        )

    def chunk_pop(pop: Runner):
        return jax.vmap(lambda r: fns.chunk_raw(r, k_pbt))(pop)

    donate = (0,) if jax.default_backend() != "cpu" else ()
    return PBTFns(
        init=jax.jit(init_pop),
        chunk=jax.jit(chunk_pop, donate_argnums=donate),
    )


def fitness_from_metrics(mean_return: np.ndarray) -> np.ndarray:
    """Per-member fitness: NaN-aware mean over the chunk window [P, K]."""
    valid = ~np.isnan(mean_return)
    s = np.where(valid, mean_return, 0.0).sum(axis=1)
    c = valid.sum(axis=1)
    return np.where(c > 0, s / np.maximum(c, 1), 0.0)


def select_and_mutate(
    pop: Runner,
    fitness: np.ndarray,
    rng: np.random.Generator,
    *,
    mutation: tuple[float, float] = (0.8, 1.25),
) -> tuple[Runner, list[dict]]:
    """Truncation selection at the PBT boundary (host-side, outside jit).

    Bottom quartile copies weights + optimizer state from a uniformly chosen
    top-quartile member and perturbs each hyperparameter by xU{0.8, 1.25}.
    Survivors are untouched; env states and PRNG keys stay member-own.
    Returns the new population and the exploit-event log.
    """
    pop_size = fitness.shape[0]
    q = max(1, pop_size // 4)
    order = np.argsort(fitness)
    bottom, top = order[:q], order[pop_size - q :]
    src = np.arange(pop_size)
    hyper = {k: np.asarray(v).copy() for k, v in pop.hyper.items()}
    events = []
    for b in bottom:
        s = int(rng.choice(top))
        src[b] = s
        old = {k: float(hyper[k][b]) for k in hyper}
        for k in hyper:
            hyper[k][b] = float(hyper[k][s]) * float(rng.choice(mutation))
        events.append(
            {
                "target": int(b),
                "source": s,
                "fitness_target": float(fitness[b]),
                "fitness_source": float(fitness[s]),
                "hyper_old": old,
                "hyper_new": {k: float(hyper[k][b]) for k in hyper},
            }
        )
    train_state = jax.tree_util.tree_map(lambda x: x[src], pop.train_state)
    hyper = {k: jnp.asarray(v, jnp.float32) for k, v in hyper.items()}
    return pop._replace(train_state=train_state, hyper=hyper), events


def _save_pop(mngr, pop: Runner, round_idx: int):
    mngr.save(
        round_idx,
        args=ocp.args.StandardSave(
            {
                "params": pop.train_state.params,
                "opt_state": pop.train_state.opt_state,
                "hyper": pop.hyper,
                "keys": pop.key,
                "round": round_idx,
            }
        ),
    )


def train_population(
    cfg: Config,
    *,
    rounds: int,
    seed: int = 0,
    ckpt_dir: str | Path | None = None,
    metrics_path: str | Path | None = None,
    events_path: str | Path | None = None,
    resume: bool = False,
    handle_sigterm: bool = False,
):
    """Run PBT for `rounds` boundaries of K_pbt updates each.

    Returns (population Runner, metric rows, exploit events). Metric rows are
    one dict per (update, member): round, update, member, mean_return, lr,
    ent_coef, losses.
    """
    pfns = make_pbt_fns(cfg)
    k_pbt = cfg.train.pbt_interval
    pop = pfns.init(jax.random.PRNGKey(seed))
    rng = np.random.default_rng(seed + 1)  # host-side selection stream
    start_round = 0
    mngr = _ckpt_manager(ckpt_dir) if ckpt_dir else None
    if mngr:
        hash_file = Path(ckpt_dir) / "config_hash.txt"
        if resume and mngr.latest_step() is not None:
            if hash_file.exists() and hash_file.read_text() != config_hash(cfg):
                raise ValueError(
                    "checkpoint config hash mismatch — refusing to resume"
                )
            start_round = mngr.latest_step()
            template = {
                "params": pop.train_state.params,
                "opt_state": pop.train_state.opt_state,
                "hyper": pop.hyper,
                "keys": pop.key,
                "round": 0,
            }
            restored = mngr.restore(
                start_round, args=ocp.args.StandardRestore(template)
            )
            pop = pop._replace(
                train_state=pop.train_state.replace(
                    params=restored["params"], opt_state=restored["opt_state"]
                ),
                hyper=restored["hyper"],
                key=restored["keys"],
            )
        else:
            hash_file.parent.mkdir(parents=True, exist_ok=True)
            hash_file.write_text(config_hash(cfg))
    prev_handler = None
    if handle_sigterm:
        _SIGTERM["received"] = False
        prev_handler = signal.signal(signal.SIGTERM, _sigterm_handler)

    rows, all_events = [], []
    m_file = open(metrics_path, "a") if metrics_path else None
    e_file = open(events_path, "a") if events_path else None
    try:
        for r in range(start_round, rounds):
            if handle_sigterm and _SIGTERM["received"]:
                break
            t0 = time.perf_counter()
            pop, metrics = pfns.chunk(pop)
            jax.block_until_ready(metrics["total_loss"])
            dt = time.perf_counter() - t0
            metrics = {k: np.asarray(v) for k, v in metrics.items()}
            for i in range(k_pbt):
                for m in range(cfg.train.pop_size):
                    row = {
                        "round": r,
                        "update": r * k_pbt + i + 1,
                        "member": m,
                        "mean_return": float(metrics["mean_return"][m, i]),
                        # M1.4 episode metrics (NaN when no episode ended).
                        "survival_rate": float(metrics["survival_rate"][m, i]),
                        "completion": float(metrics["completion"][m, i]),
                        "deaths_fire": float(metrics["deaths_fire"][m, i]),
                        "deaths_collapse": float(
                            metrics["deaths_collapse"][m, i]
                        ),
                        "lr": float(metrics["lr"][m, i]),
                        "ent_coef": float(metrics["ent_coef"][m, i]),
                        "total_loss": float(metrics["total_loss"][m, i]),
                        "entropy": float(metrics["entropy"][m, i]),
                    }
                    rows.append(row)
                    if m_file:
                        m_file.write(json.dumps(row) + "\n")
            fitness = fitness_from_metrics(metrics["mean_return"])
            pop, events = select_and_mutate(pop, fitness, rng)
            for ev in events:
                ev["round"] = r
                all_events.append(ev)
                if e_file:
                    e_file.write(json.dumps(ev) + "\n")
            if m_file:
                m_file.flush()
            if e_file:
                e_file.flush()
            steps = cfg.train.pop_size * cfg.train.n_envs * cfg.train.rollout_len
            print(
                f"[pbt] round {r + 1}/{rounds} "
                f"fitness min/med/max = {fitness.min():.2f}/"
                f"{np.median(fitness):.2f}/{fitness.max():.2f} "
                f"exploits={len(events)} "
                f"({steps * k_pbt / dt:,.0f} train steps/s)",
                flush=True,
            )
            if mngr:
                _save_pop(mngr, pop, r + 1)
        if mngr:
            mngr.wait_until_finished()
    finally:
        if m_file:
            m_file.close()
        if e_file:
            e_file.close()
        if prev_handler is not None:
            signal.signal(signal.SIGTERM, prev_handler)
    return pop, rows, all_events


# ------------------------------------------------- second gate measurement


def bench_population(
    cfg: Config, *, windows: int = 5, window_secs: float = 30.0, seed: int = 0
) -> dict:
    """Aggregate *training* steps/sec with the full population.

    One measured unit = one compiled K_pbt-update chunk for all members plus
    the host-side selection at the boundary (honest wall-clock accounting).
    """
    pfns = make_pbt_fns(cfg)
    tcfg = cfg.train
    steps_per_round = tcfg.pop_size * tcfg.n_envs * tcfg.rollout_len * tcfg.pbt_interval

    pop = pfns.init(jax.random.PRNGKey(seed))
    rng = np.random.default_rng(seed + 1)
    t0 = time.perf_counter()
    compiled = pfns.chunk.lower(pop).compile()
    compile_s = time.perf_counter() - t0

    def one_round(pop):
        pop, metrics = compiled(pop)
        jax.block_until_ready(metrics["total_loss"])
        fitness = fitness_from_metrics(np.asarray(metrics["mean_return"]))
        pop, _ = select_and_mutate(pop, fitness, rng)
        return pop

    pop = one_round(pop)  # warm-up (excluded)
    rates = []
    for _ in range(windows):
        n = 0
        t_win = time.perf_counter()
        while time.perf_counter() - t_win < window_secs:
            pop = one_round(pop)
            n += 1
        rates.append(n * steps_per_round / (time.perf_counter() - t_win))
    iqr = 0.0
    if len(rates) >= 2:
        q1, _, q3 = statistics.quantiles(rates, n=4)
        iqr = q3 - q1
    dev = jax.local_devices()[0]
    stats = dev.memory_stats() or {}
    return {
        "pop_size": tcfg.pop_size,
        "n_envs": tcfg.n_envs,
        "n_agents": cfg.env.n_agents,
        "grid": cfg.env.grid_size,
        "rollout_len": tcfg.rollout_len,
        "k_pbt": tcfg.pbt_interval,
        "compile_s": round(compile_s, 2),
        "rates": [round(x) for x in rates],
        "median": round(statistics.median(rates)),
        "iqr": round(iqr),
        "peak_bytes": stats.get("peak_bytes_in_use"),
        "device": dev.device_kind,
    }


def train_verdict(rate: float) -> str:
    for floor, verdict in TRAIN_VERDICTS:
        if rate >= floor:
            return verdict
    return TRAIN_VERDICTS[-1][1]


def append_gate_report(result: dict, path: str | Path, dollars_per_hour: float):
    rate = result["median"]
    hours = TOTAL_STEPS / rate / 3600
    cost = hours * dollars_per_hour * 2
    peak = result["peak_bytes"]
    lines = [
        "",
        "## M0.6 — second gate measurement: training throughput",
        "",
        f"- Device: **{result['device']}**; population {result['pop_size']}, "
        f"n_envs {result['n_envs']}, grid {result['grid']}², "
        f"{result['n_agents']} agents, rollout {result['rollout_len']}, "
        f"K_pbt {result['k_pbt']}",
        f"- Compile: {result['compile_s']} s; window rates: "
        f"{', '.join(f'{x:,}' for x in result['rates'])}",
        f"- **Aggregate training throughput: {rate:,} steps/s** "
        f"(IQR {result['iqr']:,}); peak device memory "
        + (f"{peak / 2**30:.2f} GiB" if peak else "n/a"),
        f"- **Verdict (training thresholds): {train_verdict(rate)}**",
        f"- Budget: 86e9 steps -> {hours:,.1f} GPU-hours; "
        f"~${cost:,.0f} at ${dollars_per_hour}/h with x2 buffer",
        "",
    ]
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "a") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--config", default="che/configs/reference.yaml")
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--bench", action="store_true",
                   help="second gate measurement; appends to the gate report")
    p.add_argument("--windows", type=int, default=5)
    p.add_argument("--window-secs", type=float, default=30.0)
    p.add_argument("--report", default="che/bench/results/gate_report.md")
    p.add_argument("--dollars-per-hour", type=float, default=0.45)
    p.add_argument("--rounds", type=int, default=40)
    p.add_argument("--metrics", help="JSONL metrics output path")
    p.add_argument("--events", help="JSONL exploit-event output path")
    p.add_argument("--ckpt-dir")
    p.add_argument("--resume", action="store_true")
    args = p.parse_args()
    cfg = load_config(args.config)
    if args.bench:
        result = bench_population(
            cfg, windows=args.windows, window_secs=args.window_secs,
            seed=args.seed,
        )
        append_gate_report(result, args.report, args.dollars_per_hour)
    else:
        train_population(
            cfg,
            rounds=args.rounds,
            seed=args.seed,
            ckpt_dir=args.ckpt_dir,
            metrics_path=args.metrics,
            events_path=args.events,
            resume=args.resume,
            handle_sigterm=True,
        )


if __name__ == "__main__":
    main()
