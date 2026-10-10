"""Figure 4 (slot): Coupling B. (a) Masking concentration on danger moments
(m44, κ_B = 1.0 arm): the share of an agent's crop that is masked,
unconditionally and at danger moments (a Burning cell in the crop), per
severity, with the committed amplification ratio. (b) The High survival
effect, κ_B = 1.0 − κ_B = 0, led by the three committed replicate
contrasts (seed 0 and seed 1 of M4.4, and the same-seed seed-0 retrain),
with the measured High reproducibility floor; the first 2-seed M4.4
estimate is drawn beside them, set apart.

Output: out/img/fig04_coupling_b.png
"""

from __future__ import annotations

import re

import common as C
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

M44 = C.RES / "phase4" / "m44" / "m44_analysis.json"
REPL = C.RES / "phase5" / "pretask" / "replicate_deltas.txt"
FLOOR = C.RES / "phase5" / "m53b" / "reproducibility_floor_high.txt"
LEVELS = ("low", "medium", "high")
NAME = {"low": "Low", "medium": "Medium", "high": "High"}


def load():
    m44 = C.load_json(M44)
    mask = {lv: m44["danger_moment_masking"][f"{lv}/kbL"] for lv in LEVELS}
    hs = m44["arm_comparison"]["high/survival_rate"]
    d_s0 = hs["kbL_seed_means"][0] - hs["kb0_seed_means"][0]
    d_s1 = hs["kbL_seed_means"][1] - hs["kb0_seed_means"][1]
    txt = REPL.read_text()
    rep = float(
        re.search(r"replicate pair\s+survival_rate\s+([-+]\d+\.\d+)", txt).group(1)
    )
    orig0 = float(
        re.search(r"M4\.4 originals\s+survival_rate\s+([-+]\d+\.\d+)", txt).group(1)
    )
    assert round(d_s0, 4) == orig0  # the file's seed-0 original
    assert round(d_s1, 4) == -0.1066  # phase4_report.md:641
    fl = re.search(r"survival_rate\s+[\d.]+\s+([\d.]+)", FLOOR.read_text())
    floor = float(fl.group(1))
    return dict(
        mask=mask, d_s0=d_s0, d_s1=d_s1, rep=rep, first=hs["delta"], floor=floor
    )


def static(D):
    C.mpl_setup()
    fig, (a1, a2) = plt.subplots(
        1, 2, figsize=(7.0, 3.1), gridspec_kw={"wspace": 0.55, "width_ratios": [1.1, 1]}
    )
    for i, lv in enumerate(LEVELS):
        m = D["mask"][lv]
        u, dn = m["masked_frac_uncond"], m["masked_frac_danger"]
        a1.plot([u, dn], [i, i], color=C.AXIS, lw=2.0, zorder=1, solid_capstyle="butt")
        a1.plot([u], [i], "o", ms=7, mfc=C.SURFACE, mec=C.INK, mew=1.4, zorder=3)
        a1.plot([dn], [i], "o", ms=7, color=C.INK, mec=C.SURFACE, mew=1.0, zorder=3)
        a1.text(
            (u * dn) ** 0.5,
            i - 0.22,
            f"{m['amplification']:.0f}×",
            ha="center",
            va="bottom",
            fontsize=7.4,
            color=C.INK,
        )
    a1.set_xscale("log")
    a1.set_xlim(3e-4, 0.6)
    a1.set_yticks(range(3))
    a1.set_yticklabels([NAME[lv] for lv in LEVELS])
    a1.set_ylim(2.6, -0.6)
    a1.tick_params(axis="y", length=0)
    a1.spines["left"].set_visible(False)
    a1.set_xlabel("masked share of the agent's crop (log scale)")
    a1.set_title("(a) masking, κ_B = 1.0 arm (m44)")
    a1.grid(axis="x", which="major")
    a1.set_axisbelow(True)
    a1.legend(
        handles=[
            Line2D(
                [0],
                [0],
                marker="o",
                ls="none",
                mfc=C.SURFACE,
                mec=C.INK,
                mew=1.4,
                ms=6,
                label="all alive agent-steps",
            ),
            Line2D(
                [0],
                [0],
                marker="o",
                ls="none",
                color=C.INK,
                ms=6,
                label="danger moments (fire in crop)",
            ),
        ],
        loc="lower center",
        bbox_to_anchor=(0.5, -0.42),
        ncol=1,
        fontsize=7.0,
    )

    rows = [
        ("seed 0 (M4.4)", D["d_s0"], "o"),
        ("seed 1 (M4.4)", D["d_s1"], "o"),
        ("seed 0 retrain\n(same seed, commit, config)", D["rep"], "s"),
    ]
    f = D["floor"]
    a2.axvspan(-f, f, facecolor="none", edgecolor=C.HATCH, hatch="////", lw=0, zorder=0)
    a2.axvline(0, color=C.MUTED, lw=0.8, zorder=1)
    for i, (_lab, v, mk) in enumerate(rows):
        a2.plot([v], [i], mk, ms=6.5, color=C.INK, mec=C.SURFACE, mew=1.0, zorder=3)
    a2.plot(
        [D["first"]], [3.55], "D", ms=6, mfc=C.SURFACE, mec=C.INK2, mew=1.3, zorder=3
    )
    a2.axhline(2.75, color=C.GRID, lw=0.8)
    a2.set_yticks([0, 1, 2, 3.55])
    a2.set_yticklabels(
        [r[0] for r in rows] + ["first estimate:\nmean of seeds 0, 1"], fontsize=7.2
    )
    a2.set_ylim(4.1, -0.6)
    a2.tick_params(axis="y", length=0)
    a2.spines["left"].set_visible(False)
    a2.set_xlim(-0.125, 0.075)
    a2.set_xlabel("Δ survival rate at High, κ_B 1.0 − 0")
    a2.set_title("(b) High survival, κ_B effect")
    for i, (_lab, v, _mk) in enumerate(rows):
        a2.text(
            v, i - 0.32, C.fmt(v), ha="center", va="bottom", fontsize=6.8, color=C.INK
        )
    a2.text(
        D["first"],
        3.55 - 0.32,
        C.fmt(D["first"]),
        ha="center",
        va="bottom",
        fontsize=6.8,
        color=C.INK2,
    )
    a2.legend(
        handles=[
            Patch(
                facecolor="none",
                edgecolor=C.HATCH,
                hatch="////",
                lw=0,
                label=f"floor: ±1 sd = {f:.4f}, 4 identical High runs",
            )
        ],
        loc="lower center",
        bbox_to_anchor=(0.4, -0.36),
        fontsize=7.0,
    )
    return C.save_png(fig, "fig04_coupling_b.png")


def main():
    D = load()
    print(static(D).name)
    print(
        {
            k: (
                v
                if k != "mask"
                else {
                    lv: {kk: round(vv, 5) for kk, vv in v[lv].items() if vv is not None}
                    for lv in LEVELS
                }
            )
            for k, v in D.items()
        }
    )


if __name__ == "__main__":
    main()
