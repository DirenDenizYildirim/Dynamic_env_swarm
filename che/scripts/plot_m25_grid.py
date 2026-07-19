"""M2.5 grid analysis: comparison table + curves for phase2_report.md.

Reads che/bench/results/phase2/m25/{sev}_dp{dp}_s{seed}.jsonl (18 runs) and
baseline_{sev}.json, prints the per-(severity, dp) markdown table (final
metrics: NaN-safe mean over the last --tail logged updates; across-seed
mean +/- half the min-max range), and renders m25_curves.png (per-severity
panels, survival + completion, per-dp mean across seeds with min-max band).

Usage:
  uv run python che/scripts/plot_m25_grid.py
"""

import argparse
import json
import math
import warnings
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

# House palette (fixed slots; see plot_learning_curve.py). Identity here is
# the death-penalty arm, constant across all panels.
DP_COLORS = {"0.0": "#2a78d6", "0.5": "#eb6834"}  # blue / orange
INK = "#3d3d3a"
MUTED = "#8a8a85"

SEVERITIES = ("low", "medium", "high")
DPS = ("0.0", "0.5")
SEEDS = (0, 1, 2)
METRICS = (
    "completion",
    "survival_rate",
    "deaths_fire",
    "deaths_collapse",
    "mean_smoke_exposure",
    "mean_return",
)


def _style(ax):
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color(MUTED)
    ax.tick_params(colors=MUTED)
    ax.grid(axis="y", color=MUTED, alpha=0.25, lw=0.5)


def load_run(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines()]


def final_metrics(rows: list[dict], tail: int) -> dict[str, float]:
    """NaN-safe means over the last `tail` logged updates."""
    out = {}
    for m in METRICS:
        vals = [
            r[m] for r in rows[-tail:] if m in r and not math.isnan(r[m])
        ]
        out[m] = sum(vals) / len(vals) if vals else float("nan")
    return out


def curve(rows: list[dict], metric: str, n_updates: int) -> np.ndarray:
    """Metric vs update as a length-n array (NaN where no episode ended)."""
    ys = np.full(n_updates, np.nan)
    for r in rows:
        u = int(r["update"]) - 1
        if 0 <= u < n_updates and not math.isnan(r.get(metric, math.nan)):
            ys[u] = r[metric]
    return ys


def rolling_nanmean(ys: np.ndarray, w: int) -> np.ndarray:
    out = np.full_like(ys, np.nan)
    for i in range(len(ys)):
        window = ys[max(0, i - w + 1) : i + 1]
        if np.isfinite(window).any():
            out[i] = np.nanmean(window)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--dir", type=Path, default=Path("che/bench/results/phase2/m25")
    )
    ap.add_argument("--tail", type=int, default=50)
    ap.add_argument("--window", type=int, default=15)
    args = ap.parse_args()

    runs = {
        (sev, dp, s): load_run(args.dir / f"{sev}_dp{dp}_s{s}.jsonl")
        for sev in SEVERITIES
        for dp in DPS
        for s in SEEDS
    }
    baselines = {
        sev: json.loads((args.dir / f"baseline_{sev}.json").read_text())
        for sev in SEVERITIES
    }
    n_updates = max(len(r) for r in runs.values())

    # ---- comparison table ----
    hdr = (
        "| severity | dp | completion | survival_rate | deaths_fire "
        "| mean_smoke_exposure |"
    )
    print(hdr)
    print("|---" * 5 + "|---|")
    agg: dict[tuple[str, str], dict[str, list[float]]] = {}
    for sev in SEVERITIES:
        for dp in DPS:
            per_seed = [
                final_metrics(runs[(sev, dp, s)], args.tail) for s in SEEDS
            ]
            agg[(sev, dp)] = {
                m: [p[m] for p in per_seed] for m in METRICS
            }
            cells = []
            for m in (
                "completion",
                "survival_rate",
                "deaths_fire",
                "mean_smoke_exposure",
            ):
                vals = agg[(sev, dp)][m]
                mean = sum(vals) / len(vals)
                half = (max(vals) - min(vals)) / 2.0
                fmt = ".4f" if m == "mean_smoke_exposure" else ".3f"
                cells.append(f"{mean:{fmt}} ± {half:{fmt}}")
            print(f"| {sev} | {dp} | " + " | ".join(cells) + " |")
        b = baselines[sev]
        print(
            f"| {sev} | random | {b['completion']:.3f} | "
            f"{b['survival_rate']:.3f} | {b['deaths_fire']:.3f} | "
            f"{b['mean_smoke_exposure']:.4f} |"
        )

    # Across-seed range highlight (theory Def. 4 near-critical prediction).
    print("\nacross-seed ranges (max - min of final survival_rate):")
    for sev in SEVERITIES:
        for dp in DPS:
            vals = agg[(sev, dp)]["survival_rate"]
            print(f"  {sev} dp={dp}: {max(vals) - min(vals):.4f}")

    # ---- curves figure: rows = {survival, completion}, cols = severity --
    fig, axes = plt.subplots(
        2, 3, figsize=(11, 6), dpi=150, sharex=True, sharey="row"
    )
    for j, sev in enumerate(SEVERITIES):
        for i, metric in enumerate(("survival_rate", "completion")):
            ax = axes[i][j]
            for dp in DPS:
                smoothed = np.stack([
                    rolling_nanmean(
                        curve(runs[(sev, dp, s)], metric, n_updates),
                        args.window,
                    )
                    for s in SEEDS
                ])
                # All-NaN columns (pre-first-episode updates) stay NaN and
                # plot as gaps; silence the benign numpy warnings.
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", RuntimeWarning)
                    mean = np.nanmean(smoothed, axis=0)
                    lo = np.nanmin(smoothed, axis=0)
                    hi = np.nanmax(smoothed, axis=0)
                x = np.arange(1, n_updates + 1)
                c = DP_COLORS[dp]
                ax.fill_between(x, lo, hi, color=c, alpha=0.15, lw=0)
                ax.plot(x, mean, color=c, lw=2, label=f"dp = {dp}")
            ax.axhline(
                baselines[sev][metric], color=MUTED, lw=1.2,
                ls=(0, (4, 3)),
            )
            ax.set_ylim(-0.02, 1.02)
            if i == 0:
                ax.set_title(f"{sev} (β = "
                             f"{ {'low': 0.43, 'medium': 0.49, 'high': 0.70}[sev] })",
                             color=INK, loc="left", fontsize=10)
            if j == 0:
                ax.set_ylabel(metric.replace("_", " "), color=INK)
            if i == 1:
                ax.set_xlabel("PPO update", color=INK)
            _style(ax)
    axes[0][0].legend(frameon=False, loc="lower right", fontsize=9)
    axes[0][0].annotate("dashed: random baseline", xy=(0.03, 0.03),
                        xycoords="axes fraction", color=MUTED, fontsize=8)
    fig.suptitle(
        "M2.5 pillar-only probe: 3 severities × death penalty × 3 seeds "
        "(mean across seeds, min–max band)",
        color=INK, x=0.01, ha="left", fontsize=11,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    out = args.dir / "m25_curves.png"
    fig.savefig(out)
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
