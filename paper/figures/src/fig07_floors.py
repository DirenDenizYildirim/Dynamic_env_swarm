"""Figure 7 (slot): floors are per-card, per-run-length and per-artifact.
(a) Medium reproducibility floor, 4 identical runs each, on two cards
(M5.1e, RTX 5090; M5.5, RTX PRO 6000). The pair also differs in code tree
and in config hash, so card is not isolated. (b) Completion floor, 8
identical runs each, at T = 500 (M6.2) and T = 1000 (M6.2b); the two ran on
different PRO 6000 boxes, so run length is not isolated. (c) M6.0's
digest comparisons: how many same-code reruns differed, per tree.

Output: out/img/fig07_floors.png
"""

from __future__ import annotations

import json
import re
import statistics

import common as C
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

M51E = C.RES / "phase5" / "m51e"
M55 = C.RES / "phase5" / "m55"
M62 = C.P6 / "m62" / "floors.json"
M62B = C.P6 / "m62b" / "floors.json"
M60 = C.P6 / "m60" / "m60_report.md"
METRICS = ("completion", "survival_rate")
MLABEL = {"completion": "completion", "survival_rate": "survival rate"}


def floor_txt(p, m):
    return float(
        re.search(rf"^\s*{m}\s+[\d.]+\s+([\d.]+)", p.read_text(), re.M).group(1)
    )


def load():
    card = {}
    for key, d, pat, txt in (
        ("5090", M51E, "eval_medium_rep{}.json", "reproducibility_floor.txt"),
        ("pro", M55, "eval_floor_rep{}.json", "reproducibility_floor_medium.txt"),
    ):
        card[key] = {}
        for m in METRICS:
            reps = [
                float(json.loads((d / pat.format(r)).read_text())["metrics"][m]["mean"])
                for r in range(1, 5)
            ]
            sd = floor_txt(d / txt, m)
            assert round(statistics.stdev(reps), 4) == sd, (key, m)
            card[key][m] = dict(reps=reps, sd=sd)
    hashes = {
        key: {
            json.loads((d / pat.format(r)).read_text())["config_hash"]
            for r in range(1, 5)
        }
        for key, d, pat in (
            ("5090", M51E, "eval_medium_rep{}.json"),
            ("pro", M55, "eval_floor_rep{}.json"),
        )
    }
    assert len(hashes["5090"]) == 1 and len(hashes["pro"]) == 1
    assert hashes["5090"] != hashes["pro"]  # the legend's "config hash A / B"
    assert (
        card["5090"]["completion"]["sd"],
        card["pro"]["completion"]["sd"],
        card["5090"]["survival_rate"]["sd"],
        card["pro"]["survival_rate"]["sd"],
    ) == (0.0145, 0.0399, 0.0129, 0.0130)  # METH-1
    t500, t1000 = C.load_json(M62), C.load_json(M62B)
    length = {}
    for arm in ("iso", "joint"):
        length[arm] = {
            T: dict(
                reps=src[arm]["completion"]["values"], sd=src[arm]["completion"]["sd"]
            )
            for T, src in ((500, t500), (1000, t1000))
        }
        for T in (500, 1000):
            r = length[arm][T]
            assert abs(statistics.stdev(r["reps"]) - r["sd"]) < 1e-9
    ratios = {arm: length[arm][1000]["sd"] / length[arm][500]["sd"] for arm in length}
    assert round(ratios["iso"], 1) == 2.1 and round(ratios["joint"], 1) == 5.2  # METH-5
    txt = M60.read_text()
    tab = {}
    for lab, pat in (
        (
            "baseline vs baseline",
            r"\| baseline vs baseline \(same code\) \| (\d+) \| \*\*(\d+)\*\*",
        ),
        (
            "traced vs traced",
            r"\| traced vs traced \(same code\) \| (\d+) \| \*\*(\d+)\*\*",
        ),
        ("traced vs baseline", r"\| traced vs baseline \| (\d+) \| \*\*(\d+)\*\*"),
    ):
        mm = re.search(pat, txt)
        tab[lab] = (int(mm.group(1)), int(mm.group(2)))
    assert tab == {
        "baseline vs baseline": (4, 0),
        "traced vs traced": (4, 1),
        "traced vs baseline": (5, 2),
    }
    return dict(card=card, length=length, ratios=ratios, m60=tab)


def static(D):
    C.mpl_setup()
    fig, axes = plt.subplots(
        1,
        3,
        figsize=(7.2, 3.0),
        gridspec_kw={"wspace": 0.42, "width_ratios": [1.2, 1, 1.0]},
    )
    W = 0.34
    a = axes[0]
    for i, m in enumerate(METRICS):
        for j, (key, col, hat) in enumerate(
            (("5090", C.S1, None), ("pro", C.S2, "////"))
        ):
            x = i + (j - 0.5) * (W + 0.1)
            sd = D["card"][key][m]["sd"]
            a.bar(x, sd, width=W, color=col, lw=0, hatch=hat, edgecolor=C.SURFACE)
            a.text(
                x,
                sd + 0.0007,
                f"{sd:.4f}",
                ha="center",
                va="bottom",
                fontsize=6.0,
                color=C.INK,
            )
    a.text(
        0,
        D["card"]["pro"]["completion"]["sd"] + 0.0055,
        "2.75×",
        ha="center",
        fontsize=7,
        color=C.INK2,
    )
    a.set_xticks([0, 1])
    a.set_xticklabels(["completion", "survival\nrate"])
    a.tick_params(axis="x", length=0)
    a.set_xlim(-0.6, 1.6)
    a.set_ylabel("floor sd, 4 identical runs (Medium)")
    a.set_ylim(0, 0.05)
    a.set_title("(a) per card")
    a.grid(axis="y")
    a.set_axisbelow(True)
    a.legend(
        handles=[
            Patch(
                facecolor=C.S1,
                lw=0,
                label="M5.1e: RTX 5090,\ncode tree A, config hash A",
            ),
            Patch(
                facecolor=C.S2,
                hatch="////",
                edgecolor=C.SURFACE,
                lw=0,
                label="M5.5: RTX PRO 6000,\ncode tree B, config hash B",
            ),
        ],
        loc="upper center",
        bbox_to_anchor=(0.5, -0.14),
        fontsize=6.4,
    )

    b = axes[1]
    for i, arm in enumerate(("iso", "joint")):
        for j, T in enumerate((500, 1000)):
            x = i + (j - 0.5) * (W + 0.1)
            sd = D["length"][arm][T]["sd"]
            b.bar(
                x, sd, width=W, color=C.SEV["Low"] if T == 500 else C.SEV["High"], lw=0
            )
            b.text(
                x,
                sd + 0.0008,
                f"{sd:.4f}",
                ha="center",
                va="bottom",
                fontsize=6.0,
                color=C.INK,
            )
        b.text(
            i,
            max(D["length"][arm][500]["sd"], D["length"][arm][1000]["sd"]) + 0.0068,
            f"{D['ratios'][arm]:.1f}×",
            ha="center",
            fontsize=7,
            color=C.INK2,
        )
    b.set_xticks([0, 1])
    b.set_xticklabels(["ISO", "JOINT"])
    b.tick_params(axis="x", length=0)
    b.set_xlim(-0.6, 1.6)
    b.set_ylabel("completion floor sd, 8 identical runs")
    b.set_ylim(0, 0.065)
    b.set_title("(b) per run length")
    b.grid(axis="y")
    b.set_axisbelow(True)
    b.legend(
        handles=[
            Patch(
                facecolor=C.SEV["Low"],
                lw=0,
                label="T = 500 (M6.2):\nRTX PRO 6000, box 1",
            ),
            Patch(
                facecolor=C.SEV["High"],
                lw=0,
                label="T = 1000 (M6.2b):\nRTX PRO 6000, box 2",
            ),
        ],
        loc="upper center",
        bbox_to_anchor=(0.5, -0.14),
        fontsize=6.4,
    )

    c = axes[2]
    labs = list(D["m60"])
    for i, lab in enumerate(labs):
        n, k = D["m60"][lab]
        c.barh(i, n, height=0.42, color=C.BAND, lw=0)
        c.barh(i, k, height=0.42, color=C.INK, lw=0)
        c.text(n + 0.15, i, f"{k} of {n}", va="center", fontsize=7, color=C.INK)
    c.set_yticks(range(len(labs)))
    c.set_yticklabels(
        ["baseline tree\nvs itself", "traced tree\nvs itself", "traced vs\nbaseline"],
        fontsize=7,
    )
    c.set_ylim(len(labs) - 0.4, -0.6)
    c.set_xlim(0, 6.6)
    c.set_xticks(range(0, 6))
    c.tick_params(axis="y", length=0)
    c.spines["left"].set_visible(False)
    c.set_xlabel("same-code GPU rerun comparisons")
    c.set_title("(c) per artifact (M6.0)")
    c.legend(
        handles=[
            Patch(
                facecolor=C.INK,
                lw=0,
                label="differed (2 diagnostic\nchannels, no trajectory field)",
            ),
            Patch(facecolor=C.BAND, lw=0, label="identical digests"),
        ],
        loc="upper center",
        bbox_to_anchor=(0.4, -0.3),
        fontsize=6.4,
    )
    return C.save_png(fig, "fig07_floors.png")


def main():
    D = load()
    print(static(D).name)
    print({k: {m: D["card"][k][m]["sd"] for m in METRICS} for k in D["card"]})
    print(
        {
            a: {T: round(D["length"][a][T]["sd"], 4) for T in (500, 1000)}
            for a in D["length"]
        },
        D["ratios"],
        D["m60"],
    )


if __name__ == "__main__":
    main()
