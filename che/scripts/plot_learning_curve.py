"""Plot IPPO learning curves from a JSONL metrics file.

M0.5: mean episodic return vs the random baseline. M1.4: two further
panels when the log carries episode metrics — survival_rate + completion
(shared [0, 1] axis) and per-episode deaths by cause (own axis; counts and
rates are different scales, so never one axis).

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

# Validated categorical palette, fixed slot order (dataviz reference).
SERIES = "#2a78d6"  # slot 1 (blue): return
SURVIVAL = "#008300"  # slot 2 (green)
COMPLETION = "#e87ba4"  # slot 3 (magenta)
DEATHS_FIRE = "#eb6834"  # slot 6 (orange)
DEATHS_COLLAPSE = "#4a3aa7"  # slot 7 (violet)
INK = "#3d3d3a"
MUTED = "#8a8a85"


def rolling_mean(xs: list[float], w: int) -> list[float]:
    out = []
    for i in range(len(xs)):
        lo = max(0, i - w + 1)
        out.append(sum(xs[lo : i + 1]) / (i + 1 - lo))
    return out


def _series(rows, key, w):
    pts = [
        (r["update"], r[key])
        for r in rows
        if key in r and not math.isnan(r[key])
    ]
    if not pts:
        return [], []
    return [u for u, _ in pts], rolling_mean([v for _, v in pts], w)


def _style(ax):
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color(MUTED)
    ax.tick_params(colors=MUTED)
    ax.grid(axis="y", color=MUTED, alpha=0.25, lw=0.5)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--metrics", required=True)
    p.add_argument("--baseline", type=float, default=None,
                   help="random-policy mean episodic return")
    p.add_argument("--out", default="learning_curve.png")
    p.add_argument("--window", type=int, default=15)
    p.add_argument("--title", default="IPPO learning curves")
    args = p.parse_args()

    rows = [json.loads(line) for line in Path(args.metrics).read_text().splitlines()]
    has_ep = any("survival_rate" in r for r in rows)  # M1.4 logs

    n_panels = 3 if has_ep else 1
    fig, axes = plt.subplots(
        n_panels, 1, figsize=(7, 4.2 if n_panels == 1 else 8.6), dpi=150,
        sharex=True,
        height_ratios=[2, 1, 1] if has_ep else [1],
    )
    axes = [axes] if n_panels == 1 else list(axes)

    ax = axes[0]
    updates, smooth = _series(rows, "mean_return", args.window)
    raw = [
        r["mean_return"] for r in rows if not math.isnan(r["mean_return"])
    ]
    ax.plot(updates, raw, color=SERIES, lw=0.8, alpha=0.25)
    ax.plot(updates, smooth, color=SERIES, lw=2,
            label=f"mean episodic return (rolling {args.window})")
    if args.baseline is not None:
        ax.axhline(args.baseline, color=MUTED, lw=1.5, ls=(0, (4, 3)))
        ax.annotate(f"random policy: {args.baseline:.2f}",
                    xy=(updates[-1], args.baseline),
                    xytext=(-4, 5), textcoords="offset points",
                    ha="right", color=MUTED, fontsize=9)
    ax.set_ylabel("Mean episodic return", color=INK)
    ax.set_title(args.title, color=INK, loc="left")
    ax.legend(frameon=False, loc="lower right", fontsize=9)

    if has_ep:
        ax_r = axes[1]
        for key, color, label in (
            ("survival_rate", SURVIVAL, "survival rate"),
            ("completion", COMPLETION, "completion"),
        ):
            us, vs = _series(rows, key, args.window)
            ax_r.plot(us, vs, color=color, lw=2, label=label)
        ax_r.set_ylim(-0.02, 1.02)
        ax_r.set_ylabel("Episode rate [0, 1]", color=INK)
        ax_r.legend(frameon=False, loc="lower right", fontsize=9)

        ax_d = axes[2]
        for key, color, label in (
            ("deaths_fire", DEATHS_FIRE, "deaths (fire)"),
            ("deaths_collapse", DEATHS_COLLAPSE, "deaths (collapse)"),
        ):
            us, vs = _series(rows, key, args.window)
            ax_d.plot(us, vs, color=color, lw=2, label=label)
        ax_d.set_ylabel("Deaths / episode", color=INK)
        ax_d.legend(frameon=False, loc="upper right", fontsize=9)

    axes[-1].set_xlabel("PPO update", color=INK)
    for a in axes:
        _style(a)
    fig.tight_layout()
    fig.savefig(args.out)
    print(f"wrote {args.out}")
    final = sum(smooth[-20:]) / min(20, len(smooth))
    print(f"final smoothed return (last 20 logged updates): {final:.2f}")
    if has_ep:
        for key in ("survival_rate", "completion"):
            _, vs = _series(rows, key, args.window)
            if vs:
                print(f"final smoothed {key}: {vs[-1]:.3f}")


if __name__ == "__main__":
    main()
