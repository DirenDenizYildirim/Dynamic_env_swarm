"""Figure 6 (slot): the comms axis. (a) The Remark-2′ handshake in the
courier variant E2C² (M5.2): J for the free-comms arm, the measured
denied (pinned) arm with its committed ±1 SE, and the predicted ½ + q/2,
against κ_B; VoC_gated is the gap. (b) δ = 0 vs δ = 1 at Medium (M5.5):
the committed contrasts, Δ = (δ = 0) − (δ = 1), with the registered M5.5
bars (2 × the floor measured on that card: post-hoc floor grading, the
2σ form CLAUDE.md allows only for it). (c, d) the per-seed values behind
them and the four identical-seed floor runs.

Output: out/img/fig06_comms.png
"""

from __future__ import annotations

import json
import re
import statistics

import common as C
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

E2C2 = C.RES / "phase5" / "m52" / "e2c2_sweep.json"
M55 = C.RES / "phase5" / "m55"
METRICS = ("completion", "survival_rate")
MLABEL = {"completion": "completion", "survival_rate": "survival rate"}


def load():
    sw = C.load_json(E2C2)["sweep"]
    v = (
        C.load_json(M55 / "reproducibility_floor_medium.json")
        if (M55 / "reproducibility_floor_medium.json").is_file()
        else None
    )
    txt = (M55 / "verdict.txt").read_text()
    bars, deltas = {}, {}
    for m in METRICS:
        b = re.search(rf"{m}\s+sd\s+([\d.]+)\s+->\s+bar\s+([\d.]+)", txt)
        bars[m] = (float(b.group(1)), float(b.group(2)))
        dd = re.search(rf"\(i\)\s+d{m}\s+([-+][\d.]+)\s+vs bar\s+([\d.]+)", txt)
        deltas[m] = float(dd.group(1))
        assert float(dd.group(2)) == bars[m][1]
    seeds = {m: {"d0": [], "d1": [], "floor": []} for m in METRICS}
    for m in METRICS:
        for s in range(4):
            for arm, tag in (("d0", f"d0.0_s{s}"), ("d1", f"d1.0_s{s}")):
                d = json.loads((M55 / f"eval_{tag}.json").read_text())
                seeds[m][arm].append(float(d["metrics"][m]["mean"]))
        for r in range(1, 5):
            d = json.loads((M55 / f"eval_floor_rep{r}.json").read_text())
            seeds[m]["floor"].append(float(d["metrics"][m]["mean"]))
        # the committed contrast and floor are what these files say
        mu0, mu1 = statistics.mean(seeds[m]["d0"]), statistics.mean(seeds[m]["d1"])
        assert round(mu0 - mu1, 4) == deltas[m], (m, mu0 - mu1, deltas[m])
        assert round(statistics.stdev(seeds[m]["floor"]), 4) == bars[m][0], m
    return dict(sw=sw, bars=bars, deltas=deltas, seeds=seeds, floor_json=v is not None)


def static(D):
    C.mpl_setup()
    fig = plt.figure(figsize=(7.0, 5.6))
    gs = fig.add_gridspec(2, 2, hspace=0.72, wspace=0.38)
    a = fig.add_subplot(gs[0, 0])
    sw = D["sw"]
    kb = [r["kappa_B"] for r in sw]
    a.fill_between(
        kb,
        [r["j_pinned"] for r in sw],
        [r["j_free"] for r in sw],
        color=C.BAND,
        lw=0,
        zorder=0,
    )
    a.plot(
        kb,
        [r["j_free"] for r in sw],
        color=C.S1,
        marker="s",
        ms=4,
        lw=1.5,
        mec=C.SURFACE,
        label="J, free comms",
    )
    a.plot(
        kb,
        [r["j_predicted"] for r in sw],
        color=C.INK2,
        lw=1.0,
        ls=(0, (1, 1.6)),
        label="predicted ½ + q/2",
    )
    a.errorbar(
        kb,
        [r["j_pinned"] for r in sw],
        yerr=[r["se_j_pinned"] for r in sw],
        color=C.S2,
        marker="o",
        ms=4,
        lw=1.5,
        mec=C.SURFACE,
        elinewidth=0.9,
        capsize=0,
        label="J, denied (pinned), ±1 SE",
    )
    a.text(6.3, 0.66, "VoC_gated", fontsize=7, color=C.INK2, ha="center")
    a.set_xlabel("κ_B, perception attenuation")
    a.set_ylabel("J, courier success rate")
    a.set_ylim(0.45, 1.04)
    a.set_title("(a) E2C² handshake (M5.2)")
    a.grid(axis="y")
    a.set_axisbelow(True)
    a.legend(
        loc="upper right",
        bbox_to_anchor=(1.0, 0.95),
        fontsize=6.6,
        frameon=True,
        facecolor=C.SURFACE,
        edgecolor="none",
        framealpha=0.95,
    )

    b = fig.add_subplot(gs[0, 1])
    for i, m in enumerate(METRICS):
        bar = D["bars"][m][1]
        b.add_patch(
            plt.Rectangle(
                (-bar, i - 0.25),
                2 * bar,
                0.5,
                facecolor="none",
                edgecolor=C.HATCH,
                hatch="////",
                lw=0,
                zorder=0,
            )
        )
        b.plot([D["deltas"][m]], [i], "o", ms=6.5, color=C.INK, mec=C.SURFACE, zorder=3)
        b.text(
            D["deltas"][m],
            i - 0.3,
            C.fmt(D["deltas"][m]),
            ha="center",
            va="bottom",
            fontsize=6.8,
            color=C.INK,
        )
    b.axvline(0, color=C.MUTED, lw=0.8)
    b.set_yticks([0, 1])
    b.set_yticklabels([MLABEL[m] for m in METRICS])
    b.set_ylim(1.6, -0.6)
    b.tick_params(axis="y", length=0)
    b.spines["left"].set_visible(False)
    b.set_xlim(-0.095, 0.095)
    b.set_xlabel("Δ = (δ = 0) − (δ = 1), Medium")
    b.set_title("(b) denial contrast (M5.5)")
    b.legend(
        handles=[
            Patch(
                facecolor="none",
                edgecolor=C.HATCH,
                hatch="////",
                lw=0,
                label="±2 × floor sd: the M5.5 bar\n(post-hoc floor grading)",
            )
        ],
        loc="lower center",
        bbox_to_anchor=(0.5, -0.62),
        fontsize=6.8,
    )

    for j, m in enumerate(METRICS):
        ax = fig.add_subplot(gs[1, j])
        S = D["seeds"][m]
        for i, (arm, _lab, col, mk) in enumerate(
            (
                ("d0", "δ = 0\n4 seeds", C.S1, "o"),
                ("d1", "δ = 1\n4 seeds", C.S2, "s"),
                ("floor", "floor runs\n4 × seed 0, δ = 0", C.INK2, "D"),
            )
        ):
            v = S[arm]
            xs = [i + 0.18 * (((k * 0.6180339887) % 1.0) - 0.5) for k in range(len(v))]
            ax.plot(xs, v, mk, ms=5, mfc="none", mec=col, mew=1.1, zorder=3)
            mu = statistics.mean(v)
            ax.plot([i - 0.2, i + 0.2], [mu, mu], color=C.INK, lw=1.8, zorder=4)
        ax.set_xticks(range(3))
        ax.set_xticklabels(
            [
                "δ = 0\ncomms live\n4 seeds",
                "δ = 1\ndenied\n4 seeds",
                "floor runs\n4 × seed 0\nδ = 0",
            ],
            fontsize=7.2,
        )
        ax.tick_params(axis="x", length=0)
        ax.set_xlim(-0.5, 2.5)
        ax.set_ylabel(f"{MLABEL[m]} at Medium")
        ax.set_title(f"({'c' if j == 0 else 'd'}) {MLABEL[m]}, per run (M5.5)")
        ax.grid(axis="y")
        ax.set_axisbelow(True)
    fig.legend(
        handles=[
            Line2D([0], [0], color=C.INK, lw=1.8, label="mean of the 4 runs"),
            Line2D(
                [0],
                [0],
                marker="o",
                ls="none",
                mfc="none",
                mec=C.INK2,
                ms=4,
                label="one run (mean of 512 eval episodes)",
            ),
        ],
        loc="lower center",
        ncol=2,
        bbox_to_anchor=(0.5, -0.04),
        fontsize=7.0,
    )
    return C.save_png(fig, "fig06_comms.png")


def main():
    D = load()
    print(static(D).name)
    print("bars", D["bars"], "deltas", D["deltas"])
    print("voc", [(r["kappa_B"], round(r["voc_gated"], 4)) for r in D["sw"]])


if __name__ == "__main__":
    main()
