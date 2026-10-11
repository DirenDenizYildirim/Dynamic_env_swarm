"""F6c Floors explorer (§8): floors are per metric, per card, per artifact, and
grow with run length; and the grid's seed dispersion against its floor.

Every panel states its confound on the figure (METH-1: card, code tree and
config differ between the two Medium floors; METH-5: run length and box
differ between the two floor sets).

Sources (committed, read-only):
  METH-1  che/bench/results/phase5/m51e/reproducibility_floor.txt,
          che/bench/results/phase5/m55/reproducibility_floor_medium.txt,
          cards: che/bench/results/phase5/phase5_report.md:1011-1014
  METH-2  che/bench/results/phase6/m60/m60_report.md (comparison table)
  METH-5  che/bench/results/phase6/m62/floors.json (T = 500),
          m62b/floors.json (T = 1000)
  HW-1    che/bench/results/phase6/unblind/unblind.json → beat_reproducibility

Run from the repo root:  uv run python paper/figures/interactive/src/build_floors.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common_web import OUT_HTML, REPO, check_html, load_template, page  # noqa: E402

R = REPO / "che/bench/results"


def floor_txt(p: Path) -> dict:
    out = {}
    for line in p.read_text().splitlines():
        m = re.match(r"\s+(completion|survival_rate)\s+([\d.]+)\s+([\d.]+)", line)
        if m:
            out[m.group(1)] = float(m.group(3))
    return out


def build_data():
    a = floor_txt(R / "phase5/m51e/reproducibility_floor.txt")
    b = floor_txt(R / "phase5/m55/reproducibility_floor_medium.txt")
    assert (
        f"{a['completion']:.4f}" == "0.0145" and f"{b['completion']:.4f}" == "0.0399"
    )  # METH-1
    assert (
        f"{a['survival_rate']:.4f}" == "0.0129"
        and f"{b['survival_rate']:.4f}" == "0.0130"
    )
    rep = (R / "phase5/phase5_report.md").read_text()
    assert "| metric | M5.1e (5090) | M5.5 (PRO 6000) | ratio |" in rep
    m60 = (R / "phase6/m60/m60_report.md").read_text()
    for row in (
        "| baseline vs baseline (same code) | 4 | **0** |",
        "| traced vs traced (same code) | 4 | **1** |",
        "| traced vs baseline | 5 | **2** |",
    ):
        assert row in m60, row
    f500 = json.loads((R / "phase6/m62/floors.json").read_text())
    f1000 = json.loads((R / "phase6/m62b/floors.json").read_text())
    growth = {
        k: f1000[k]["completion"]["sd"] / f500[k]["completion"]["sd"]
        for k in ("iso", "joint")
    }
    assert (
        f"{growth['iso']:.1f}" == "2.1" and f"{growth['joint']:.1f}" == "5.2"
    )  # METH-5
    ub = json.loads((R / "phase6/unblind/unblind.json").read_text())[
        "beat_reproducibility"
    ]
    hw = {
        m: dict(
            iso=ub[m]["ratio_seed_over_floor_iso"],
            joint=ub[m]["ratio_seed_over_floor_joint"],
            gamma=ub[m]["gamma_over_floor_sd"],
        )
        for m in ("completion", "survival_rate")
    }
    assert [
        f"{hw['completion']['iso']:.2f}",
        f"{hw['completion']['joint']:.2f}",
        f"{hw['survival_rate']['iso']:.2f}",
        f"{hw['survival_rate']['joint']:.2f}",
    ] == ["1.12", "1.09", "1.25", "1.19"]
    assert f"{hw['survival_rate']['gamma']:.2f}" == "5.40"  # HW-1
    return dict(
        card=dict(
            runs=[
                dict(
                    name="M5.1e · RTX 5090",
                    completion=a["completion"],
                    survival=a["survival_rate"],
                    ct="0.0145",
                    st="0.0129",
                ),
                dict(
                    name="M5.5 · RTX PRO 6000",
                    completion=b["completion"],
                    survival=b["survival_rate"],
                    ct="0.0399",
                    st="0.0130",
                ),
            ],
            ratio="2.75×",
            confound=(
                "card, code tree and config all differ between the two runs "
                "(M5.5 records R_comm 16; M5.1e predates the R_comm lock)"
            ),
            sub="Medium, identical runs per floor, same seed: nondeterminism only",
        ),
        artifact=dict(
            rows=[
                dict(
                    name="baseline vs baseline",
                    n=4,
                    diff=0,
                    text="0 of 760 field digests differ, in 4 of 4",
                ),
                dict(
                    name="traced vs traced",
                    n=4,
                    diff=1,
                    text="1 of 4: masked_frac, masked_danger_sum",
                ),
                dict(name="traced vs baseline", n=5, diff=2, text=None),
            ],
            sub=(
                "M6.0 GPU rerun comparisons, severity_high seed 0; "
                "no trajectory field differed in any comparison"
            ),
        ),
        length=dict(
            arms=[
                dict(
                    name="ISO",
                    v500=f500["iso"]["completion"]["values"],
                    v1000=f1000["iso"]["completion"]["values"],
                    g="2.1×",
                ),
                dict(
                    name="JOINT",
                    v500=f500["joint"]["completion"]["values"],
                    v1000=f1000["joint"]["completion"]["values"],
                    g="5.2×",
                ),
            ],
            confound=(
                "run length and box both differ: the T = 500 and T = 1000 "
                "floors ran on different RTX PRO 6000 boxes"
            ),
            sub="completion floor, identical runs per arm and length, same seed",
        ),
        beat=dict(
            rows=[
                dict(name="completion · ISO", v=hw["completion"]["iso"], t="1.12×"),
                dict(name="completion · JOINT", v=hw["completion"]["joint"], t="1.09×"),
                dict(name="survival · ISO", v=hw["survival_rate"]["iso"], t="1.25×"),
                dict(
                    name="survival · JOINT", v=hw["survival_rate"]["joint"], t="1.19×"
                ),
            ],
            gamma=dict(v=hw["survival_rate"]["gamma"], t="5.40×"),
            sub=(
                "the confirmatory grid (k = 72 per arm): seed sd over the "
                "rerun floor; survival Γ over the floor-basis sd(Γ)"
            ),
        ),
    )


CSS = load_template("floors.css")

BODY = load_template("floors.html")

JS = load_template("floors.js")


def main():
    data = build_data()
    out = OUT_HTML / "floors_explorer.html"
    out.write_text(page("Floors explorer", BODY, CSS, JS, data), encoding="utf-8")
    hits = check_html(out)
    assert not hits, hits
    print(f"{out.name}: {out.stat().st_size / 1e3:.1f} KB")


if __name__ == "__main__":
    main()
