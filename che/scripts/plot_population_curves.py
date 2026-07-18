"""Plot PBT population learning curves + lr trajectories (M0.6 acceptance).

Usage:
  uv run python che/scripts/plot_population_curves.py \
      --metrics pbt_metrics.jsonl --baseline 3.31 --out pbt_curves.png

Members are drawn as thin muted lines (12 series get no per-member hues —
identity is not the point), the population median as the single bold series;
the lr panel shows mutation-driven diversity on a log scale.
"""

import argparse
import json
import math
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

SERIES = "#2a78d6"  # slot 1 (blue): return median
SURVIVAL = "#008300"  # slot 2 (green)
COMPLETION = "#e87ba4"  # slot 3 (magenta)
MEMBER = "#9fb6cc"
INK = "#3d3d3a"
MUTED = "#8a8a85"


def _median_curve(members, idx, window):
    """Population median of a per-member metric column (NaN-dropped)."""
    per_update = defaultdict(list)
    for _m, rows in sorted(members.items()):
        pts = [(r[0], r[idx]) for r in rows if not math.isnan(r[idx])]
        if pts:
            us = [u for u, _ in pts]
            vs = rolling_mean([v for _, v in pts], window)
            for u, v in zip(us, vs, strict=True):
                per_update[u].append(v)
    med_u = sorted(per_update)
    med_v = [sorted(per_update[u])[len(per_update[u]) // 2] for u in med_u]
    return med_u, med_v


def rolling_mean(xs, w):
    out = []
    for i in range(len(xs)):
        lo = max(0, i - w + 1)
        out.append(sum(xs[lo : i + 1]) / (i + 1 - lo))
    return out


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--metrics", required=True)
    p.add_argument("--baseline", type=float, default=None)
    p.add_argument("--out", default="pbt_curves.png")
    p.add_argument("--window", type=int, default=10)
    p.add_argument("--title", default="PBT population curves")
    args = p.parse_args()

    members = defaultdict(list)  # member -> [(update, return, lr, surv, comp)]
    has_ep = False
    for line in Path(args.metrics).read_text().splitlines():
        r = json.loads(line)
        has_ep = has_ep or "survival_rate" in r
        members[r["member"]].append(
            (
                r["update"],
                r["mean_return"],
                r["lr"],
                r.get("survival_rate", math.nan),
                r.get("completion", math.nan),
            )
        )

    n_panels = 3 if has_ep else 2
    fig, axes = plt.subplots(
        n_panels, 1, figsize=(7.5, 6.5 if n_panels == 2 else 8.6), dpi=150,
        sharex=True,
        height_ratios=[2.2, 1, 1] if has_ep else [2.2, 1],
    )
    ax, ax_lr = axes[0], axes[-1]
    for _m, rows in sorted(members.items()):
        pts = [(r[0], r[1]) for r in rows if not math.isnan(r[1])]
        if pts:
            us = [u for u, _ in pts]
            vs = rolling_mean([v for _, v in pts], args.window)
            ax.plot(us, vs, color=MEMBER, lw=0.8, alpha=0.7)
        ax_lr.plot(
            [r[0] for r in rows],
            [r[2] for r in rows],
            color=MEMBER, lw=0.8, alpha=0.7,
        )
    med_u, med_v = _median_curve(members, 1, args.window)
    ax.plot(med_u, med_v, color=SERIES, lw=2, label="population median")
    if has_ep:
        ax_ep = axes[1]
        for idx, color, label in (
            (3, SURVIVAL, "survival rate (median)"),
            (4, COMPLETION, "completion (median)"),
        ):
            us, vs = _median_curve(members, idx, args.window)
            ax_ep.plot(us, vs, color=color, lw=2, label=label)
        ax_ep.set_ylim(-0.02, 1.02)
        ax_ep.set_ylabel("Episode rate [0, 1]", color=INK)
        ax_ep.legend(frameon=False, loc="lower right", fontsize=9)
    if args.baseline is not None:
        ax.axhline(args.baseline, color=MUTED, lw=1.5, ls=(0, (4, 3)))
        ax.annotate(f"random policy: {args.baseline:.2f}",
                    xy=(med_u[-1], args.baseline), xytext=(-4, 5),
                    textcoords="offset points", ha="right",
                    color=MUTED, fontsize=9)
    ax.plot([], [], color=MEMBER, lw=0.8, label="members")
    ax.set_ylabel("Mean episodic return", color=INK)
    ax.set_title(args.title, color=INK, loc="left")
    ax.legend(frameon=False, loc="lower right", fontsize=9)
    ax_lr.set_yscale("log")
    ax_lr.set_ylabel("learning rate", color=INK)
    ax_lr.set_xlabel("PPO update", color=INK)
    for a in axes:
        a.spines[["top", "right"]].set_visible(False)
        a.spines[["left", "bottom"]].set_color(MUTED)
        a.tick_params(colors=MUTED)
        a.grid(axis="y", color=MUTED, alpha=0.25, lw=0.5)
    fig.tight_layout()
    fig.savefig(args.out)
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
