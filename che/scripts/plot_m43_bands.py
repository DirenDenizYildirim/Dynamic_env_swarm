"""M4.3 figure: the three lock bands and where they admit kappa_B.

Renders the three M4.3 target observables against kappa_B with their
bands shaded, plus a shared-axis strip of the admissible kappa_B
intervals — the "three curves side by side" the M4.2 ruling asks for if
the bands fail to intersect.

    uv run python -m che.scripts.plot_m43_bands

Pure replot from the committed calibration JSON — no simulation.
"""

import argparse
import json
from pathlib import Path

import numpy as np

M43 = Path("che/bench/results/phase4/m43")


def admissible_interval(kappas, values, band):
    """kappa_B range where a monotone-decreasing observable is in band.

    Log-linear interpolation between grid points; None when the band lies
    entirely outside the measured range (the curve never enters it).
    """
    k = np.asarray(kappas, float)
    v = np.asarray(values, float)
    lo, hi = band
    if v.max() < lo or v.min() > hi:
        return None
    order = np.argsort(v)  # np.interp needs ascending x
    edges = []
    for target in (hi, lo):
        if target > v.max():
            edges.append(k.min())
        elif target < v.min():
            edges.append(k.max())
        else:
            edges.append(float(np.exp(np.interp(target, v[order], np.log(k)[order]))))
    return (min(edges), max(edges))


def render(payload: dict, out_path: Path) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    kappas = payload["kappa_candidates"]
    src_name = payload["band_check_source"]
    med = payload[f"{src_name}_policy"]["medium"]
    bands = payload["bands"]
    curves = [
        ("masked_frac", med["masked_frac"], bands["masked_frac_medium"],
         "masked_frac (Medium, fire-active)", med["masked_frac_ceiling"]),
        ("detection", med["detection"], bands["detection_medium"],
         "P(Burning cell at crop dist. 3 revealed)", None),
        ("e2c_q", payload["e2c_q"], bands["e2c_q"],
         "E2C $q(\\kappa_B)$  (Option-A geometry)", None),
    ]

    fig = plt.figure(figsize=(11.5, 5.4), constrained_layout=True)
    gs = fig.add_gridspec(2, 3, height_ratios=[3, 1])
    intervals = []
    for i, (_, vals, band, title, ceiling) in enumerate(curves):
        ax = fig.add_subplot(gs[0, i])
        ax.axhspan(band[0], band[1], color="tab:green", alpha=0.15,
                   label=f"target band [{band[0]}, {band[1]}]")
        ax.plot(kappas, vals, "o-", ms=4, color="tab:blue")
        iv = admissible_interval(kappas, vals, band)
        intervals.append(iv)
        if ceiling is not None:
            ax.axhline(ceiling, ls="--", lw=1.2, color="tab:red")
            ax.annotate(
                f"ceiling {ceiling:.3f}\n($\\kappa_B\\to\\infty$)",
                xy=(kappas[1], ceiling), xytext=(kappas[0] * 1.1, ceiling * 1.5),
                fontsize=7.5, color="tab:red",
            )
        ax.set_xscale("log")
        ax.set_xlabel(r"$\kappa_B$")
        ax.set_title(title, fontsize=9)
        ax.legend(fontsize=7, loc="upper right")
        if iv is None:
            ax.text(0.5, 0.5, "band unreachable\nat any $\\kappa_B$",
                    transform=ax.transAxes, ha="center", va="center",
                    fontsize=10, color="tab:red", weight="bold")

    ax = fig.add_subplot(gs[1, :])
    labels = ["masked_frac", "detection", "E2C q"]
    for i, (iv, lab) in enumerate(zip(intervals, labels, strict=True)):
        y = len(labels) - 1 - i
        if iv is None:
            ax.text(min(kappas), y, f"  {lab}: no admissible $\\kappa_B$",
                    va="center", fontsize=9, color="tab:red", weight="bold")
        else:
            ax.plot(iv, [y, y], lw=8, solid_capstyle="butt", color="tab:green",
                    alpha=0.65)
            ax.text(iv[1] * 1.15, y, f"{lab}: [{iv[0]:.2f}, {iv[1]:.2f}]",
                    va="center", fontsize=9)
    ax.set_xscale("log")
    ax.set_xlim(min(kappas) * 0.8, max(kappas) * 4.0)
    ax.set_ylim(-0.6, len(labels) - 0.4)
    ax.set_yticks([])
    ax.set_xlabel(r"admissible $\kappa_B$ per band — the intervals are disjoint")
    fig.savefig(out_path, dpi=150)
    return intervals


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--json", type=Path, default=M43 / "coupling_b_calibration.json")
    p.add_argument("--out", type=Path, default=M43 / "kappa_b_bands.png")
    args = p.parse_args()
    payload = json.loads(args.json.read_text())
    intervals = render(payload, args.out)
    for lab, iv in zip(("masked_frac", "detection", "e2c_q"), intervals, strict=True):
        span = "UNREACHABLE" if iv is None else f"[{iv[0]:.3f}, {iv[1]:.3f}]"
        print(f"{lab:>12}: {span}")
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
