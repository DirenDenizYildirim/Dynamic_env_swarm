"""Figure 3 (slot): Coupling A. (a) The Prop.-3 dense sweep at L = 64 (the
CA-2 run: κ_A 0.02, f_weak 0.4, β 0.43; not the locked parameters):
E[B_T] against the realized E[N_seeds] with the committed ±1 SE and the
committed through-origin fit. The CA-3 handshake (purified L = 32 CPU test,
κ_A 0.003) is a different run with no committed data file, so it is not
drawn. (b) Collapse-seeded ignitions per episode against severity under
trained policies: m44 (Coupling-B grid, κ_B = 1.0 arm; CA-4) and its m35
replication (Coupling-A grid, κ_A on; CA-5), per seed and pooled.

Output: out/img/fig03_coupling_a.png
"""

from __future__ import annotations

import math

import common as C
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

PROP3 = C.RES / "phase3" / "m33" / "prop3_L64.json"
SEV = C.RES / "e1" / "severity" / "severity.json"
M44 = C.RES / "phase4" / "m44" / "m44_analysis.json"
M35 = C.RES / "phase3" / "m35"
LEVELS = ("low", "medium", "high")
LAB = {"low": "Low\nβ = 0.43", "medium": "Medium\nβ = 0.49", "high": "High\nβ = 0.70"}


def load():
    p3 = C.load_json(PROP3)
    sev = C.load_json(SEV)
    m44 = C.load_json(M44)
    out = dict(p3=p3, m44={}, m35={})
    for lv in LEVELS:
        cell = sev["grids"]["m44"]["cells"][f"{lv}|kbL"]["seeded_ignitions"]
        seeds = m44["arm_comparison"][f"{lv}/seeded_ignitions"]["kbL_seed_means"]
        assert math.isclose(sum(seeds) / len(seeds), cell["mean"], abs_tol=1e-9)
        out["m44"][lv] = dict(mean=cell["mean"], seeds=seeds)
        cell = sev["grids"]["m35"]["cells"][f"{lv}|kaL"]["seeded_ignitions"]
        seeds = []
        for s in (0, 1):
            d = C.load_json(M35 / f"eval_{lv}_kaL_dp0.5_s{s}.json")
            seeds.append(float(d["metrics"]["seeded_ignitions"]["mean"]))
        assert math.isclose(sum(seeds) / len(seeds), cell["mean"], abs_tol=1e-9)
        out["m35"][lv] = dict(mean=cell["mean"], seeds=seeds)
    # CA-4 / CA-5 values, as the ledger states them
    assert [round(out["m44"][lv]["mean"], 2) for lv in LEVELS] == [4.05, 3.41, 0.84]
    assert [round(out["m35"][lv]["mean"], 2) for lv in LEVELS] == [4.08, 3.42, 0.83]
    return out


def static(D):
    C.mpl_setup()
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.0, 3.2), gridspec_kw={"wspace": 0.34})
    p3 = D["p3"]
    x, y, se = p3["e_n_seeds"], p3["e_b_t"], p3["se_b_t"]
    xm = max(x) * 1.08
    a1.plot(
        [0, xm], [0, p3["slope_through_origin"] * xm], color=C.INK2, lw=1.0, zorder=1
    )
    a1.errorbar(
        x,
        y,
        yerr=se,
        fmt="o",
        color=C.INK,
        ms=5,
        mec=C.SURFACE,
        mew=1.0,
        elinewidth=1.0,
        capsize=0,
        zorder=3,
    )
    a1.set_xlim(0, xm)
    a1.set_ylim(0, max(y) * 1.12)
    a1.set_xlabel("E[N_seeds], collapse-seeded ignitions per run")
    a1.set_ylabel("E[B_T], burnt cells at the horizon")
    a1.text(
        0.04,
        0.95,
        f"through-origin fit, R² = {p3['r2_through_origin']:.3f}",
        transform=a1.transAxes,
        fontsize=7.2,
        color=C.INK,
        va="top",
    )
    a1.text(
        0.04,
        0.87,
        f"L = {p3['grid_size']}, β = {p3['beta']}, κ_A = {p3['kappa_A']}, "
        f"f_weak = {p3['f_weak']}\n{p3['n_seeds_mc']} runs per point, no agents",
        transform=a1.transAxes,
        fontsize=6.8,
        color=C.INK2,
        va="top",
    )
    a1.set_title("(a) Prop. 3 dense sweep, L = 64")
    a1.grid(True)
    a1.set_axisbelow(True)

    xs = {lv: i for i, lv in enumerate(LEVELS)}
    for key, off, col, mk, _lab in (
        ("m44", -0.12, C.S1, "o", "m44: κ_B = 1.0 arm (Coupling-B grid)"),
        ("m35", 0.12, C.S2, "s", "m35: κ_A on arm (Coupling-A grid)"),
    ):
        G = D[key]
        a2.plot(
            [xs[lv] + off for lv in LEVELS],
            [G[lv]["mean"] for lv in LEVELS],
            color=col,
            lw=1.4,
            zorder=2,
        )
        for lv in LEVELS:
            a2.plot(
                [xs[lv] + off] * len(G[lv]["seeds"]),
                G[lv]["seeds"],
                mk,
                ms=3.6,
                mfc="none",
                mec=col,
                mew=0.9,
                zorder=3,
            )
            a2.plot(
                [xs[lv] + off - 0.07, xs[lv] + off + 0.07],
                [G[lv]["mean"]] * 2,
                color=C.INK,
                lw=2.0,
                zorder=4,
            )
    a2.text(
        2.45,
        4.55,
        "Low / High:  m44 4.83×,  m35 4.92×",
        fontsize=7,
        color=C.INK,
        ha="right",
        va="top",
    )
    a2.set_xticks(range(3))
    a2.set_xticklabels([LAB[lv] for lv in LEVELS], fontsize=7.6)
    a2.set_xlim(-0.5, 2.5)
    a2.set_ylim(0, 4.7)
    a2.set_ylabel("collapse-seeded ignitions per episode")
    a2.set_title("(b) seeded ignitions, trained policies")
    a2.grid(axis="y")
    a2.set_axisbelow(True)
    handles = [
        Line2D(
            [0],
            [0],
            color=C.INK,
            lw=0,
            marker="o",
            mec=C.SURFACE,
            ms=5,
            label="(a) λ₀ point, ±1 SE",
        ),
        Line2D(
            [0], [0], color=C.INK2, lw=1.0, label="(a) committed through-origin fit"
        ),
        Line2D(
            [0],
            [0],
            color=C.S1,
            marker="o",
            mfc="none",
            lw=1.4,
            ms=4,
            label="(b) m44, κ_B = 1.0 arm, 500 updates: seeds and pooled mean",
        ),
        Line2D(
            [0],
            [0],
            color=C.S2,
            marker="s",
            mfc="none",
            lw=1.4,
            ms=4,
            label="(b) m35, κ_A on arm, 500 updates: seeds and pooled mean",
        ),
    ]
    fig.legend(
        handles=handles,
        loc="lower center",
        ncol=2,
        bbox_to_anchor=(0.5, -0.16),
        fontsize=7.0,
    )
    return C.save_png(fig, "fig03_coupling_a.png")


def main():
    D = load()
    print(static(D).name)
    p3 = D["p3"]
    print(
        "R2",
        p3["r2_through_origin"],
        "range",
        max(p3["e_n_seeds"]) / min(p3["e_n_seeds"]),
    )
    for k in ("m44", "m35"):
        print(
            k,
            {
                lv: (
                    round(D[k][lv]["mean"], 4),
                    [round(s, 4) for s in D[k][lv]["seeds"]],
                )
                for lv in LEVELS
            },
        )


if __name__ == "__main__":
    main()
