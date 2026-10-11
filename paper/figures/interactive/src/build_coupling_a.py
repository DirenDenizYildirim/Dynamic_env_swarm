"""F6b Coupling A explorer (§5): collapse-seeded ignitions fall with severity
while their near-agent share stays flat; the two Prop. 3 handshake runs in
separate panels (they are two different runs, ledger CA-2 and CA-3).

Sources (committed, read-only):
  che/bench/results/e1/severity/severity.json
      grids.m44.cells (κ_B 1.0 arm "kbL", and "kb0"),
                                                grids.m35.cells (κ_A on arm "kaL")
  che/bench/results/phase3/m33/prop3_L64.json
      e_n_seeds, e_b_t, se_b_t, slope_through_origin, r2_through_origin
Ledger: CA-2, CA-3 (report text only, no data file), CA-4, CA-5, CA-6, CAL-3.

Run from the repo root:  uv run python paper/figures/interactive/src/build_coupling_a.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common_web import OUT_HTML, REPO, check_html, load_template, page  # noqa: E402

R = REPO / "che/bench/results"
SEV = [("low", "Low", 0.43), ("medium", "Medium", 0.49), ("high", "High", 0.70)]


def build_data():
    j = json.loads((R / "e1/severity/severity.json").read_text())
    m44, m35 = j["grids"]["m44"]["cells"], j["grids"]["m35"]["cells"]
    s44 = [m44[f"{k}|kbL"]["seeded_ignitions"] for k, *_ in SEV]
    s35 = [m35[f"{k}|kaL"]["seeded_ignitions"] for k, *_ in SEV]
    assert [f"{c['mean']:.2f}" for c in s44] == ["4.05", "3.41", "0.84"]  # CA-4
    assert [f"{c['mean']:.2f}" for c in s35] == ["4.08", "3.42", "0.83"]  # CA-5
    assert (
        f"{s44[0]['mean'] / s44[2]['mean']:.2f}" == "4.83"
        and f"{s35[0]['mean'] / s35[2]['mean']:.2f}" == "4.92"
    )
    shares = []
    for _g, cells, arm, lab in (
        ("m44", m44, "kbL", "m44, κ_B 1.0 arm"),
        ("m44", m44, "kb0", "m44, κ_B 0 arm"),
        ("m35", m35, "kaL", "m35, κ_A on arm"),
    ):
        for k, name, _beta in SEV:
            c = cells[f"{k}|{arm}"]["share"]
            shares.append(
                dict(sev=name, series=lab, mean=c["mean"], lo=c["min"], hi=c["max"])
            )
    assert len(shares) == 9
    lo, hi = min(s["mean"] for s in shares), max(s["mean"] for s in shares)
    assert f"{lo:.3f}" == "0.164" and f"{hi:.3f}" == "0.203"  # CA-6
    p3 = json.loads((R / "phase3/m33/prop3_L64.json").read_text())
    assert f"{p3['r2_through_origin']:.3f}" == "0.998"  # CA-2
    assert round(p3["e_n_seeds"][-1] / p3["e_n_seeds"][0]) == 14  # CA-2 "14× range"
    assert (
        p3["grid_size"] == 64
        and abs(p3["kappa_A"] - 0.02) < 1e-12
        and abs(p3["f_weak"] - 0.4) < 1e-12
    )
    sev = [dict(name=n, beta=b) for _, n, b in SEV]
    return dict(
        sev=sev,
        seeded=[
            dict(
                series="m44, κ_B 1.0 arm",
                vals=[dict(mean=c["mean"], lo=c["min"], hi=c["max"]) for c in s44],
                text=["4.05", "3.41", "0.84"],
                fall="4.83×",
            ),
            dict(
                series="m35, κ_A on arm",
                vals=[dict(mean=c["mean"], lo=c["min"], hi=c["max"]) for c in s35],
                text=["4.08", "3.42", "0.83"],
                fall="4.92×",
            ),
        ],
        shares=shares,
        share_range="[0.164, 0.203]",
        prop3=dict(
            x=p3["e_n_seeds"],
            y=p3["e_b_t"],
            se=p3["se_b_t"],
            slope=p3["slope_through_origin"],
            r2="0.998",
            note="L = 64 dense sweep · κ_A 0.02 · f_weak 0.4 · no agents",
        ),
        handshake=dict(
            lines=[
                "matched-reference ratio 0.992, inside [0.90, 1.02]",
                "R² 0.9995",
                "v2 purified test · L = 32 · CPU · κ_A 0.003",
                "a different run from the L = 64 sweep; reported in text, "
                "no committed data file",
            ]
        ),
    )


CSS = load_template("coupling_a.css")

BODY = load_template("coupling_a.html")

JS = load_template("coupling_a.js")


def main():
    data = build_data()
    out = OUT_HTML / "coupling_a_explorer.html"
    out.write_text(page("Coupling A explorer", BODY, CSS, JS, data), encoding="utf-8")
    hits = check_html(out)
    assert not hits, hits
    print(f"{out.name}: {out.stat().st_size / 1e3:.1f} KB")
    return data


if __name__ == "__main__":
    main()
