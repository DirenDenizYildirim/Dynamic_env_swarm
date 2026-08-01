"""M6.0 acceptance 2c — the permanent DCE tax of per-env traced theta.

WHAT THIS MEASURES, and why it is a difference rather than a level.

Before M6.0, theta was a Python constant closed over by the jitted train
function, so XLA constant-folded it: at kappa_A = 0 the entire Coupling-A
seeding path is dead code and gets deleted, and at kappa_B = 0 the
transmittance/masking work goes with it. Once theta is a per-env traced
array, **a mixed batch is never constant-foldable for ANY env** — the work
runs for every env in every batch regardless of the value it carries. That
overhead is the price of the mixture design and it is paid everywhere, so
the gate's cost line needs it as a measured number (human ruling
2026-08-01, decision_log.md).

A tax is a difference, so it is measured PAIRED on ONE card in ONE session:
the same driver runs against the pre-refactor tree and the traced tree,
same configs, same instrument, same toolchain. Cross-rental comparison
would not do — the Phase-5 report records the same config measuring 24.69
and 27.53 GiB on two rentals from a jax/jaxlib change alone.

ROWS. `gate_pop12.yaml` is the spending consumer the throughput rule binds
to; the single-policy row is the configuration the milestone grids actually
run (Phase 3/4/5 used `ippo.py`, not `pbt.py`). Each is measured with
elements ON and elements OFF, because the tax is largest exactly where the
old tree had the most to delete. `reference.yaml` is deliberately NOT a row:
it is archival (obs_window 5 lineage, placeholder beta, elements off) and
quoting it is the row-A error class that has now bitten this project three
times.

KEEP-ALIVE SET (stated per the standing throughput rule): the measured
quantity is population-aggregate *training* throughput from
`pbt.bench_population`, whose compiled chunk returns the training metrics
dict and blocks on `total_loss`, with `mean_return` consumed host-side for
selection. Env `info` channels are not read by this consumer, so any
diagnostic-channel cost is outside this figure by construction.

Usage (on the GPU box, from a repo root):
    uv run python -m che.scripts.bench_dce_tax --tag traced --out rows.json
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import platform
import subprocess
import time
from pathlib import Path

import jax

from che.env.config import load_config
from che.train.pbt import bench_population

# (row name, config path, elements on/off, pop_size override or None)
ROWS: tuple[tuple[str, str, bool, int | None], ...] = (
    ("gate_elements_on", "che/configs/gate_pop12.yaml", True, None),
    ("gate_elements_off", "che/configs/gate_pop12.yaml", False, None),
    ("grid1_elements_on", "che/configs/severity_medium.yaml", True, 1),
    ("grid1_elements_off", "che/configs/severity_medium.yaml", False, 1),
)


def _elements_off(cfg):
    """Switch every composable element off, leaving the pillar (beta) alone.

    D1: the dynamic hazard is the substrate, not an element. Elements are
    {Coupling A, Coupling B, comms denial}. Collapse sub-parameters stay put
    so the structural kernel still runs — only the *ignition coupling* is
    off, which is precisely the branch the old tree could delete.
    """
    theta = dataclasses.replace(cfg.env.theta, kappa_A=0.0, kappa_B=0.0, delta=0.0)
    return dataclasses.replace(cfg, env=dataclasses.replace(cfg.env, theta=theta))


def _provenance(tag: str) -> dict:
    def _git(*a: str) -> str:
        try:
            return subprocess.check_output(
                ["git", *a], text=True, stderr=subprocess.DEVNULL
            ).strip()
        except Exception:  # noqa: BLE001
            return "unknown"

    dev = jax.local_devices()[0]
    return {
        "tag": tag,
        "git_commit": _git("rev-parse", "HEAD"),
        "jax_version": jax.__version__,
        "device": dev.device_kind,
        "platform": platform.platform(),
        "xla_flags": None,  # default flags; autotuning ON (never set level 0)
        "keep_alive": (
            "pbt.bench_population: compiled chunk returns the training metrics "
            "dict, blocks on total_loss, mean_return consumed host-side for "
            "selection; env info channels are NOT read by this consumer"
        ),
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tag", required=True, help="baseline | traced")
    ap.add_argument("--out", required=True)
    ap.add_argument("--windows", type=int, default=3)
    ap.add_argument("--window-secs", type=float, default=15.0)
    ap.add_argument("--only", help="comma-separated row names to run")
    args = ap.parse_args()

    wanted = set(args.only.split(",")) if args.only else None
    out: dict = {"provenance": _provenance(args.tag), "rows": {}}

    for name, cfg_path, elements_on, pop in ROWS:
        if wanted and name not in wanted:
            continue
        cfg = load_config(cfg_path)
        if not elements_on:
            cfg = _elements_off(cfg)
        if pop is not None:
            cfg = dataclasses.replace(
                cfg, train=dataclasses.replace(cfg.train, pop_size=pop)
            )
        th = cfg.env.theta
        print(f"\n=== {args.tag}:{name}  ({cfg_path})", flush=True)
        print(
            f"    beta={th.beta} kappa_A={th.kappa_A} kappa_B={th.kappa_B} "
            f"delta={th.delta} pop={cfg.train.pop_size} n_envs={cfg.train.n_envs}",
            flush=True,
        )
        t0 = time.perf_counter()
        res = bench_population(
            cfg, windows=args.windows, window_secs=args.window_secs
        )
        res["wall_s"] = round(time.perf_counter() - t0, 1)
        res["config"] = cfg_path
        res["elements_on"] = elements_on
        out["rows"][name] = res
        print(
            f"    median {res['median']:,} steps/s  IQR {res['iqr']:,}  "
            f"compile {res['compile_s']}s  peak {res['peak_bytes']} B  "
            f"wall {res['wall_s']}s",
            flush=True,
        )
        Path(args.out).write_text(json.dumps(out, indent=1) + "\n")

    Path(args.out).write_text(json.dumps(out, indent=1) + "\n")
    print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
