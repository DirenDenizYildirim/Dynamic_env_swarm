"""Figure 5 (slot): the per-episode distribution of the invariant-#5
co-active counter (collapse-seeded ignitions inside an alive agent's crop)
at the three severities, m44 κ_B = 1.0 arm, pooled over seeds. The
distribution is shown, never the mean alone. Read from the committed
histogram in m44_analysis.json (bins 0, 1, 2, 3, ≥ 4).

Output: out/img/fig05_coactive.png
"""

from __future__ import annotations

import common as C
import matplotlib.pyplot as plt

M44 = C.RES / "phase4" / "m44" / "m44_analysis.json"
LEVELS = (
    ("low", "Low, β = 0.43"),
    ("medium", "Medium, β = 0.49"),
    ("high", "High, β = 0.70"),
)
BINS = ("0", "1", "2", "3", "≥ 4")
CO2 = {"low": 0.563, "medium": 0.578, "high": 0.883}  # ledger CO-2


def load():
    d = C.load_json(M44)["co_active"]
    out = {}
    for lv, _ in LEVELS:
        c = d[f"{lv}/kbL"]
        h = c["hist_0_1_2_3_4plus"]
        assert abs(sum(h) - 1.0) < 1e-9 and h[0] == c["share_zero"]
        assert round(c["share_zero"], 3) == CO2[lv]
        out[lv] = dict(h=h, n=c["n_episodes"], p0=c["share_zero"], mx=c["max"])
    return out


def static(D):
    C.mpl_setup()
    fig, axes = plt.subplots(
        1, 3, figsize=(7.0, 2.6), sharey=True, gridspec_kw={"wspace": 0.12}
    )
    for ax, (lv, lab), col in zip(
        axes, LEVELS, (C.SEV["Low"], C.SEV["Medium"], C.SEV["High"]), strict=False
    ):
        h = D[lv]["h"]
        ax.bar(range(5), h, width=0.62, color=col, edgecolor=C.SURFACE, lw=0)
        ax.text(
            0,
            h[0] + 0.02,
            f"{D[lv]['p0']:.3f}",
            ha="center",
            va="bottom",
            fontsize=7.2,
            color=C.INK,
        )
        ax.set_xticks(range(5))
        ax.set_xticklabels(BINS)
        ax.tick_params(axis="x", length=0)
        ax.set_title(lab, fontsize=8.4)
        ax.text(
            0.97,
            0.95,
            f"n = {D[lv]['n']} episodes",
            transform=ax.transAxes,
            ha="right",
            va="top",
            fontsize=7,
            color=C.INK2,
        )
        ax.grid(axis="y")
        ax.set_axisbelow(True)
        ax.set_ylim(0, 1.0)
    axes[0].set_ylabel("share of episodes")
    axes[1].set_xlabel(
        "co-active events per episode  ·  m44, κ_B = 1.0 arm, seeds pooled"
    )
    return C.save_png(fig, "fig05_coactive.png")


def main():
    D = load()
    print(static(D).name)
    print(
        {lv: (D[lv]["n"], [round(x, 4) for x in D[lv]["h"]], D[lv]["mx"]) for lv in D}
    )


if __name__ == "__main__":
    main()
