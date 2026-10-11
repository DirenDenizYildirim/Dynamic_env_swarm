"""F4 Γ(t) over the final half: the registered verdict first, points and Šidák
whiskers at the 11 retained checkpoints, no connecting line, no trend line.

Source: che/bench/results/phase6/post_unblind_analysis/post_evalfloor_gamma_t_high.json
(gamma_t.points, gamma_t.verdict, gamma_t.cross_card_T_star); floor:
che/bench/results/phase6/unblind/unblind.json beat_reproducibility.

Run from the repo root:  uv run python paper/figures/interactive/src/build_gamma_t.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ledger  # noqa: E402
from common_web import (  # noqa: E402
    OUT_DATA,
    OUT_HTML,
    REPO,
    check_html,
    load_template,
    page,
)

P6 = REPO / "che/bench/results/phase6"
FIG = "F4 Γ(t)"
SRC = (
    "post_unblind_analysis/post_evalfloor_gamma_t_high.json"
    " → gamma_t.points.<metric>[t]"
)


def f4(x):
    return ("+" if x > 0 else ("−" if x < 0 else "")) + f"{abs(x):.4f}"


# (metric, t) -> which fields have a ledger row
LEDGERED = {
    ("completion", 1000): dict(est="RES-1", ci="RES-1"),
    ("survival_rate", 1000): dict(est="RES-2", ci="RES-2"),
    ("survival_rate", 900): dict(est="RES-12", ci=None),
    ("survival_rate", 950): dict(est="RES-12", ci=None),
    ("completion", 750): dict(est="RES-13", ci="RES-13"),
}
LEDGER_TEXT = {
    ("completion", 1000): ("−0.0173", "[−0.0412, +0.0066]"),
    ("survival_rate", 1000): ("+0.0096", "[+0.0047, +0.0144]"),
    ("survival_rate", 900): ("+0.0056", None),
    ("survival_rate", 950): ("+0.0083", None),
    ("completion", 750): ("−0.0147", "[−0.0283, −0.0010]"),
}
SIGNS = {"completion": "+-++-------", "survival_rate": "+--++++++++"}  # RES-11


def build_data():
    ledger.reset()
    j = json.loads(
        (P6 / "post_unblind_analysis/post_evalfloor_gamma_t_high.json").read_text()
    )
    ub = json.loads((P6 / "unblind/unblind.json").read_text())
    gt = j["gamma_t"]
    assert gt["steps"] == list(range(500, 1001, 50))
    metrics = []
    for m, name, dom in (
        ("completion", "completion", [-0.044, 0.024]),
        ("survival_rate", "survival", [-0.0095, 0.0155]),
    ):
        v = gt["verdict"][m]
        assert v["stable"] is False and "".join(v["signs"]) == SIGNS[m]
        assert v["reading"].startswith("UNSTABLE")
        tstar_sign = v["sign_at_T_star"]
        pts = []
        for p in gt["points"][m]:
            t = p["t"]
            led = LEDGERED.get((m, t), {})
            est, ci = (
                f4(p["gamma"]),
                f"[{f4(p['ci_sidak'][0])}, {f4(p['ci_sidak'][1])}]",
            )
            if (m, t) in LEDGER_TEXT:
                e_t, c_t = LEDGER_TEXT[(m, t)]
                assert est == e_t, (m, t, est, e_t)
                if c_t:
                    assert ci == c_t, (m, t, ci, c_t)
            where = SRC.replace("<metric>", m).replace("[t]", f"[t = {t}]")
            pts.append(
                dict(
                    t=t,
                    g=p["gamma"],
                    lo=p["ci_sidak"][0],
                    hi=p["ci_sidak"][1],
                    sign=p["sign"],
                    disagree=p["sign"] != tstar_sign,
                    est=ledger.stated(
                        est,
                        led.get("est"),
                        figure=FIG,
                        what=f"{m} Γ({t}) estimate",
                        source=where,
                    ),
                    ci=ledger.stated(
                        ci,
                        led.get("ci"),
                        figure=FIG,
                        what=f"{m} Γ({t}) Šidák CI",
                        source=where,
                    ),
                )
            )
        assert sorted(x["t"] for x in pts if x["disagree"]) == sorted(
            v["t_disagreeing"]
        )
        cc = gt["cross_card_T_star"][m]
        assert (
            cc["single_card_signs"] == v["signs"] and cc["single_card_stable"] is False
        )
        pc = cc["gamma_post_card_T_star"]
        single = dict(
            t=1000,
            g=pc["gamma"],
            lo=pc["ci_sidak"][0],
            hi=pc["ci_sidak"][1],
            est=ledger.stated(
                f4(pc["gamma"]),
                None,
                figure=FIG,
                what=f"{m} single-card Γ(1000)",
                source=(
                    "post_evalfloor_gamma_t_high.json → gamma_t.cross_card_T_star."
                    f"{m}.gamma_post_card_T_star"
                ),
            ),
            ci=ledger.stated(
                f"[{f4(pc['ci_sidak'][0])}, {f4(pc['ci_sidak'][1])}]",
                None,
                figure=FIG,
                what=f"{m} single-card Γ(1000) Šidák CI",
                source=(
                    "post_evalfloor_gamma_t_high.json → gamma_t.cross_card_T_star."
                    f"{m}.gamma_post_card_T_star"
                ),
            ),
        )
        metrics.append(
            dict(
                k=m,
                name=name,
                dom=dom,
                pts=pts,
                single=single,
                floor=ub["beat_reproducibility"][m]["sd_gamma_floor_basis"],
                signs=v["signs"],
            )
        )
    return dict(metrics=metrics, verdict="sign unstable over the final half")


CSS = load_template("gamma_t.css")

BODY = load_template("gamma_t.html")

JS = load_template("gamma_t.js")


def main():
    data = build_data()
    out = OUT_HTML / "gamma_t_final_half.html"
    out.write_text(page("Gamma over training", BODY, CSS, JS, data), encoding="utf-8")
    hits = check_html(out)
    assert not hits, hits
    (OUT_DATA / "gamma_t_pending.json").write_text(
        json.dumps(ledger.pending(), indent=1, ensure_ascii=False) + "\n"
    )
    print(
        f"{out.name}: {out.stat().st_size / 1e3:.1f} KB; "
        f"pending: {len(ledger.pending())}"
    )


if __name__ == "__main__":
    main()
