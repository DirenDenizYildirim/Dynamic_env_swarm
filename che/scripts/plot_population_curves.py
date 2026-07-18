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

SERIES = "#2a78d6"
MEMBER = "#9fb6cc"
INK = "#3d3d3a"
MUTED = "#8a8a85"


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
    args = p.parse_args()

    members = defaultdict(list)  # member -> [(update, return, lr)]
    for line in Path(args.metrics).read_text().splitlines():
        r = json.loads(line)
        members[r["member"]].append((r["update"], r["mean_return"], r["lr"]))

    fig, (ax, ax_lr) = plt.subplots(
        2, 1, figsize=(7.5, 6.5), dpi=150, sharex=True,
        height_ratios=[2.2, 1],
    )
    per_update = defaultdict(list)
    for _m, rows in sorted(members.items()):
        pts = [(u, v) for u, v, _ in rows if not math.isnan(v)]
        if pts:
            us = [u for u, _ in pts]
            vs = rolling_mean([v for _, v in pts], args.window)
            ax.plot(us, vs, color=MEMBER, lw=0.8, alpha=0.7)
            for u, v in zip(us, vs, strict=True):
                per_update[u].append(v)
        ax_lr.plot(
            [u for u, _, _ in rows],
            [lr for _, _, lr in rows],
            color=MEMBER, lw=0.8, alpha=0.7,
        )
    med_u = sorted(per_update)
    med_v = [sorted(per_update[u])[len(per_update[u]) // 2] for u in med_u]
    ax.plot(med_u, med_v, color=SERIES, lw=2, label="population median")
    if args.baseline is not None:
        ax.axhline(args.baseline, color=MUTED, lw=1.5, ls=(0, (4, 3)))
        ax.annotate(f"random policy: {args.baseline:.2f}",
                    xy=(med_u[-1], args.baseline), xytext=(-4, 5),
                    textcoords="offset points", ha="right",
                    color=MUTED, fontsize=9)
    ax.plot([], [], color=MEMBER, lw=0.8, label="members")
    ax.set_ylabel("Mean episodic return", color=INK)
    ax.set_title("M0.6 — PBT population on the foraging stub",
                 color=INK, loc="left")
    ax.legend(frameon=False, loc="lower right", fontsize=9)
    ax_lr.set_yscale("log")
    ax_lr.set_ylabel("learning rate", color=INK)
    ax_lr.set_xlabel("PPO update", color=INK)
    for a in (ax, ax_lr):
        a.spines[["top", "right"]].set_visible(False)
        a.spines[["left", "bottom"]].set_color(MUTED)
        a.tick_params(colors=MUTED)
        a.grid(axis="y", color=MUTED, alpha=0.25, lw=0.5)
    fig.tight_layout()
    fig.savefig(args.out)
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
