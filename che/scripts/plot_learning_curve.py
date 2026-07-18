"""Plot the IPPO learning curve from a JSONL metrics file (M0.5 acceptance).

Usage:
  uv run python che/scripts/plot_learning_curve.py \
      --metrics metrics.jsonl --baseline 3.31 --out learning_curve.png
"""

import argparse
import json
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

SERIES = "#2a78d6"  # validated categorical slot 1 (light surface)
INK = "#3d3d3a"
MUTED = "#8a8a85"


def rolling_mean(xs: list[float], w: int) -> list[float]:
    out = []
    for i in range(len(xs)):
        lo = max(0, i - w + 1)
        out.append(sum(xs[lo : i + 1]) / (i + 1 - lo))
    return out


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--metrics", required=True)
    p.add_argument("--baseline", type=float, default=None,
                   help="random-policy mean episodic return")
    p.add_argument("--out", default="learning_curve.png")
    p.add_argument("--window", type=int, default=15)
    args = p.parse_args()

    rows = [json.loads(line) for line in Path(args.metrics).read_text().splitlines()]
    pts = [
        (r["update"], r["mean_return"])
        for r in rows
        if not math.isnan(r["mean_return"])
    ]
    updates = [u for u, _ in pts]
    returns = [v for _, v in pts]
    smooth = rolling_mean(returns, args.window)

    fig, ax = plt.subplots(figsize=(7, 4.2), dpi=150)
    ax.plot(updates, returns, color=SERIES, lw=0.8, alpha=0.25)
    ax.plot(updates, smooth, color=SERIES, lw=2,
            label=f"IPPO mean episodic return (rolling {args.window})")
    if args.baseline is not None:
        ax.axhline(args.baseline, color=MUTED, lw=1.5, ls=(0, (4, 3)))
        ax.annotate(f"random policy: {args.baseline:.2f}",
                    xy=(updates[-1], args.baseline),
                    xytext=(-4, 5), textcoords="offset points",
                    ha="right", color=MUTED, fontsize=9)
    ax.set_xlabel("PPO update", color=INK)
    ax.set_ylabel("Mean episodic return (team food collected)", color=INK)
    ax.set_title("M0.5 — IPPO on the foraging stub", color=INK, loc="left")
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color(MUTED)
    ax.tick_params(colors=MUTED)
    ax.grid(axis="y", color=MUTED, alpha=0.25, lw=0.5)
    ax.legend(frameon=False, loc="lower right", fontsize=9)
    fig.tight_layout()
    fig.savefig(args.out)
    print(f"wrote {args.out}")
    final = sum(smooth[-20:]) / min(20, len(smooth))
    print(f"final smoothed return (last 20 logged updates): {final:.2f}")


if __name__ == "__main__":
    main()
