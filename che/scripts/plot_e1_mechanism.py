"""E1.3 figures: what compound hostility measurably IS in this environment.

    uv run python -m che.scripts.plot_e1_mechanism

Pure replot from committed E1 artifacts and Phase 3-5 eval npz -- no
simulation, no new compute. Phase 6 is refused structurally by
`e1_inventory._assert_not_phase6`, which every npz load here passes through.

Three figures, one claim each:

  fig1_mechanism      co_active = seeded x share across severity. The
                      severity response lives entirely in Coupling A's
                      productivity; the near-agent share is flat.
  fig2_distribution   The counter is zero-inflated and over-dispersed --
                      compound hostility is a RARE BURSTY event, not a
                      background rate. phase4_report.md Result 4 warned the
                      mean alone would mislead; this is that warning, drawn.
  fig3_endogeneity    The endogeneity null: seed dispersion does not exceed
                      the reproducibility floor, and no training treatment
                      moves realized co-activity beyond its own dispersion.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from che.scripts.e1_inventory import _assert_not_phase6

SEVS = ("low", "medium", "high")
SEV_LABEL = {"low": "Low\nβ=0.43", "medium": "Medium\nβ=0.49",
             "high": "High\nβ=0.70"}
M44 = Path("che/bench/results/phase4/m44")


def _load(pattern: str) -> np.ndarray:
    """Concatenated per-episode co-active counts over matching files."""
    files = sorted(M44.glob(pattern))
    out = []
    for f in files:
        _assert_not_phase6(f)
        out.append(np.load(f)["coupling_co_active"])
    return np.concatenate(out) if out else np.array([])


def _cells(sev_json: dict, grid: str, arm: str) -> dict:
    return {s: sev_json["grids"][grid]["cells"].get(f"{s}|{arm}", {})
            for s in SEVS}


def fig_mechanism(sev: dict, out: Path) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    on = _cells(sev, "m44", "kbL")
    x = np.arange(3)
    fig, axes = plt.subplots(1, 3, figsize=(11.5, 3.9),
                             constrained_layout=True)

    panels = (
        ("seeded_ignitions", "seeded ignitions / episode",
         "Coupling A's productivity\n(collapse CREATES hazard)", "tab:orange"),
        ("share", "P(near an agent | seeded)",
         "The near-agent share\n(geometry — flat)", "tab:green"),
        ("coupling_co_active", "co-active events / episode",
         "Their product: co-activity\n(what the counter logs)", "tab:blue"),
    )
    for ax, (key, ylab, title, colour) in zip(axes, panels, strict=True):
        means = [on[s][key]["mean"] for s in SEVS]
        lo = [on[s][key]["min"] for s in SEVS]
        hi = [on[s][key]["max"] for s in SEVS]
        ax.plot(x, means, "o-", ms=7, lw=2, color=colour, zorder=3)
        ax.vlines(x, lo, hi, color=colour, lw=6, alpha=0.28, zorder=2)
        # The measured reproducibility floors, where they exist (m55 Medium,
        # m53b High). No floor exists at Low for any artifact -- say so.
        for i, s in enumerate(SEVS):
            f = sev["floors"].get(s, {}).get(key)
            if f:
                ax.errorbar(i, means[i], yerr=f["sd"], color="k", capsize=4,
                            lw=1.2, zorder=4)
            else:
                # No reproducibility floor exists at Low for ANY artifact.
                # Say so on the figure rather than leaving a bare point that
                # reads as if it had been graded.
                ax.annotate("no floor\nmeasured", (i, 0),
                            textcoords="offset points", xytext=(0, 6),
                            ha="center", fontsize=7, color="tab:red",
                            style="italic")
        ax.set_xticks(x)
        ax.set_xticklabels([SEV_LABEL[s] for s in SEVS], fontsize=8.5)
        ax.set_ylabel(ylab, fontsize=9)
        ax.set_title(title, fontsize=10)
        ax.set_ylim(bottom=0)
        ax.grid(alpha=0.25, axis="y")

    ratio = (on["low"]["seeded_ignitions"]["mean"]
             / on["high"]["seeded_ignitions"]["mean"])
    axes[0].annotate(f"{ratio:.1f}× drop\n(fuel exhaustion)", (2, 0.84),
                     textcoords="offset points", xytext=(-6, 26), ha="right",
                     fontsize=8.5, color="tab:red", weight="bold")
    shares = [on[s]["share"]["mean"] for s in SEVS]
    axes[1].annotate(f"span {max(shares) - min(shares):.3f}\nacross severity",
                     (1, min(shares)), textcoords="offset points",
                     xytext=(0, -30), ha="center", fontsize=8.5,
                     color="tab:green", weight="bold")

    fig.suptitle("Compound hostility decomposes: the severity response is "
                 "Coupling A's, not the swarm's\n"
                 "m44, κ_B locked — shaded bar = seed range, whisker = "
                 "measured reproducibility floor", fontsize=10)
    fig.savefig(out, dpi=150)
    plt.close(fig)


def fig_distribution(out: Path) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 3, figsize=(11.5, 3.6),
                             constrained_layout=True)
    for ax, s in zip(axes, SEVS, strict=True):
        a = _load(f"eval_{s}_kbL_*.npz")
        ks = np.arange(0, 5)
        p = [(a == k).mean() for k in ks[:-1]] + [(a >= 4).mean()]
        ax.bar([str(k) for k in ks[:-1]] + ["4+"], p, color="tab:blue",
               alpha=0.85)
        ax.set_ylim(0, 1)
        ax.set_xlabel("co-active events in an episode", fontsize=9)
        ax.set_title(f"{s.capitalize()}   P(0) = {(a == 0).mean():.3f}",
                     fontsize=10)
        ax.grid(alpha=0.25, axis="y")
        ax.annotate(f"mean {a.mean():.3f}\nmax {a.max():.0f}\n"
                    f"var/mean {a.var() / a.mean():.2f}",
                    (0.97, 0.72), xycoords="axes fraction", ha="right",
                    fontsize=8.5)
    axes[0].set_ylabel("share of episodes", fontsize=9)
    fig.suptitle("The counter is zero-inflated and over-dispersed: compound "
                 "hostility is a RARE BURSTY event, not a background rate  "
                 "(var/mean > 1 = over-dispersed vs Poisson)", fontsize=10)
    fig.savefig(out, dpi=150)
    plt.close(fig)


def fig_endogeneity(endo: dict, out: Path) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 3.8),
                             constrained_layout=True,
                             gridspec_kw={"width_ratios": [1, 1.35]})

    # --- left: seed dispersion / reproducibility floor, same artifact
    ax = axes[0]
    labels, vals = [], []
    for pair, rec in endo["test1"].items():
        for key in ("coupling_co_active", "share"):
            if key in rec["ratio"]:
                labels.append(f"{pair}\n{key.split('_')[0]}")
                vals.append(rec["ratio"][key])
    y = np.arange(len(vals))
    ax.barh(y, vals, color="tab:blue", alpha=0.85)
    ax.axvline(1.0, color="k", lw=1.5, ls="--")
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=7.5)
    ax.set_xlabel("seed dispersion ÷ reproducibility floor", fontsize=9)
    ax.set_title("Does WHICH POLICY you got move co-activity?\n"
                 "(same artifact + config hash → a real floor grade)",
                 fontsize=9.5)
    ax.set_xlim(0, 2)
    ax.annotate("1× = policy identity adds nothing beyond rerun noise.\n"
                "At n = 3–4, 1.25× is NOT a detection.",
                (0.03, 0.03), xycoords="axes fraction", fontsize=7.5,
                style="italic")
    ax.grid(alpha=0.25, axis="x")

    # --- right: training treatments vs their own pooled seed dispersion
    ax = axes[1]
    labels, vals = [], []
    for lab, rec in endo["test3"].items():
        if "coupling_co_active" in rec:
            labels.append(lab)
            vals.append(rec["coupling_co_active"]["ratio"])
    y = np.arange(len(vals))
    ax.barh(y, vals, color="tab:blue", alpha=0.85)
    ax.axvline(1.0, color="k", lw=1.5, ls="--")
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=7.5)
    ax.set_xlabel("|Δ co-active| ÷ pooled seed dispersion of the contrast",
                  fontsize=9)
    ax.set_title("Does any TRAINING TREATMENT move it?\n"
                 "(all below 1.5×, and signs disagree across severity)",
                 fontsize=9.5)
    ax.set_xlim(0, 2)
    ax.grid(alpha=0.25, axis="x")

    fig.suptitle("The endogeneity null: realized co-activity is not "
                 "measurably a policy choice  (n = 3–4 per arm — a failure "
                 "to detect, not proof of absence)", fontsize=10)
    fig.savefig(out, dpi=150)
    plt.close(fig)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default="che/bench/results/e1/figures")
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    sev = json.loads(
        Path("che/bench/results/e1/severity/severity.json").read_text())
    endo = json.loads(
        Path("che/bench/results/e1/endogeneity/endogeneity.json").read_text())

    fig_mechanism(sev, out / "fig1_mechanism.png")
    fig_distribution(out / "fig2_distribution.png")
    fig_endogeneity(endo, out / "fig3_endogeneity.png")
    for f in sorted(out.glob("*.png")):
        print(f"wrote {f}  ({f.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
