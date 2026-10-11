"""F2 Registered-readings ladder: Γ → Γ₄ → Γ₄′ → B̂, in registered order.

Sources (committed, read-only):
  che/bench/results/phase6/unblind/unblind.json
      primary, prefix, beat_reproducibility
  che/bench/results/phase6/post_unblind_analysis/post_gamma4_t2000.json
      gamma4.per_metric.*
  che/bench/results/phase6/secondary/secondary.json        replicate.*.gamma4_prime
Every stated number goes through ledger.stated(); the values are asserted equal
to their ledger rows' printed values before anything is drawn.

Run from the repo root:  uv run python paper/figures/interactive/src/build_ladder.py
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
FIG = "F2 ladder"


def f4(x: float) -> str:
    s = f"{abs(x):.4f}"
    return ("+" if x > 0 else ("−" if x < 0 else "")) + s


def ci4(a) -> str:
    return f"[{f4(a[0])}, {f4(a[1])}]"


def load():
    ub = json.loads((P6 / "unblind/unblind.json").read_text())
    g4 = json.loads((P6 / "post_unblind_analysis/post_gamma4_t2000.json").read_text())
    sc = json.loads((P6 / "secondary/secondary.json").read_text())
    src = {
        "G": (
            "unblind/unblind.json → primary.family.<metric>",
            lambda m: ub["primary"]["family"][m],
        ),
        "G60": (
            "unblind/unblind.json → prefix.family.<metric>",
            lambda m: ub["prefix"]["family"][m],
        ),
        "G4": (
            "post_gamma4_t2000.json → gamma4.per_metric.<metric>.gamma4",
            lambda m: g4["gamma4"]["per_metric"][m]["gamma4"],
        ),
        "G4p": (
            "secondary.json → replicate.<metric>.gamma4_prime",
            lambda m: sc["replicate"][m]["gamma4_prime"],
        ),
        "B": (
            "post_gamma4_t2000.json → gamma4.per_metric.<metric>.b_hat",
            lambda m: g4["gamma4"]["per_metric"][m]["b_hat"],
        ),
    }
    floor = {
        m: ub["beat_reproducibility"][m]["sd_gamma_floor_basis"]
        for m in ("completion", "survival_rate")
    }
    labels = {
        m: g4["gamma4"]["per_metric"][m]["label"]
        for m in ("completion", "survival_rate")
    }
    return src, floor, labels


# Ledger rows for each (row, metric, field). None = no row (NEEDS LEDGER ROW).
LEDGER = {
    ("G", "completion"): dict(est="RES-1", ci="RES-1", z="RES-1", X="RES-1"),
    ("G", "survival_rate"): dict(est="RES-2", ci="RES-2", z="RES-2", X=None),
    ("G60", "completion"): dict(est="RES-3", ci=None, z="RES-3", X=None),
    ("G60", "survival_rate"): dict(est="RES-3", ci=None, z="RES-3", X=None),
    ("G4", "completion"): dict(est="RES-6", ci=None, z=None, X="RES-6"),
    ("G4", "survival_rate"): dict(est="RES-6", ci="RES-6", z="RES-6", X=None),
    ("G4p", "completion"): dict(est="RES-8", ci=None, z=None, X=None),
    ("G4p", "survival_rate"): dict(est="RES-8", ci="RES-8", z="RES-8", X=None),
    ("B", "completion"): dict(est="RES-7", ci=None, z=None, X=None),
    ("B", "survival_rate"): dict(est="RES-7", ci="RES-7", z="RES-7", X=None),
}
# Printed values in the ledger rows (asserted against the JSON).
LEDGER_TEXT = {
    ("G", "completion"): dict(
        est="−0.0173", ci="[−0.0412, +0.0066]", z="−1.62", X="0.0329"
    ),
    ("G", "survival_rate"): dict(est="+0.0096", ci="[+0.0047, +0.0144]", z="+4.43"),
    ("G60", "completion"): dict(est="−0.0217", z="−1.80"),
    ("G60", "survival_rate"): dict(est="+0.0104", z="+4.67"),
    ("G4", "completion"): dict(est="−0.0126", X="0.0488"),
    ("G4", "survival_rate"): dict(est="−0.0003", ci="[−0.0068, +0.0063]", z="−0.09"),
    ("G4p", "completion"): dict(est="−0.0247"),
    ("G4p", "survival_rate"): dict(est="+0.0013", ci="[−0.0056, +0.0081]", z="+0.41"),
    ("B", "completion"): dict(est="−0.0046"),
    ("B", "survival_rate"): dict(est="+0.0098", ci="[+0.0033, +0.0163]", z="+3.39"),
}

ROWS = [
    dict(
        id="G",
        rung=1,
        sym="Γ",
        contrast="JOINT − ISO",
        k="k 72 / 72 †",
        unit="unit 1, both arms",
        family="confirmatory family (Šidák m = 2)",
        date=None,
        shape="dot",
    ),
    dict(
        id="G60",
        rung=1,
        sym="Γ",
        contrast="JOINT − ISO, k = 60 prefix",
        k="k 60 / 60, seeds 1–60",
        unit="unit 1, both arms",
        family=None,
        date=None,
        shape="ring",
        optional=True,
        chips=["UNDERPOWERED"],
    ),
    dict(
        id="G4",
        rung=2,
        sym="Γ₄",
        contrast="JOINT − ISO-4",
        k="k 72 / 20",
        unit="cross-unit: JOINT unit 1, ISO-4 unit 2",
        family="outside the confirmatory family",
        date="ISO-4 rule registered 2026-09-18, pre-unblind",
        shape="tri",
    ),
    dict(
        id="G4p",
        rung=3,
        sym="Γ₄′",
        contrast="JOINT − sweep_c50_p000",
        k="k 72 / 20",
        unit="unit 1, both arms",
        family=None,
        date="proposed 2026-09-26, after Γ₄ was seen",
        shape="diamond",
    ),
    # B̂ has no registered test and no recorded verdict word (UNBLIND RESULT gives
    # only the estimate, z and interval): estimate and interval only, no chip.
    dict(
        id="B",
        rung=4,
        sym="B̂",
        contrast="ISO-4 − ISO",
        k="k 20 / 72",
        unit="cross-unit: ISO-4 unit 2, ISO unit 1",
        family=None,
        date=None,
        shape="square",
        noverdict=True,
    ),
]
# Ledger for the row labels: k 72/72 DES-3, DES-13; k 60 RES-3, DES-1;
# k 20 DES-13, DES-15;
# m = 2 DES-13; units HW-4 and spine §10 item 8; dates DES-15, DES-3 (2026-09-22).
FOOT = (
    "† k = 72 is a recorded deviation: the registered seed ladder's cap was 60, "
    "raised to 72 on 2026-09-22, pre-unblind."
)


def build_data():
    ledger.reset()
    src, floor, labels = load()
    assert (
        labels["survival_rate"] == "DOES_NOT_SURVIVE"
        and labels["completion"] == "SECOND_EXCLUSION"
    )
    out_rows = []
    for r in ROWS:
        srcname, get = src[r["id"]]
        per = {}
        for m in ("completion", "survival_rate"):
            g = get(m)
            led, txt = LEDGER[(r["id"], m)], LEDGER_TEXT[(r["id"], m)]
            vals = dict(
                est=f4(g["gamma"]),
                ci=ci4(g["ci_sidak"]),
                z=f"{g['z']:+.2f}".replace("-", "−"),
                X=f"{g['exclusion_mde80']:.4f}",
            )
            for key, t in txt.items():
                assert vals[key] == t, (r["id"], m, key, vals[key], t)
            where = f"{srcname.replace('<metric>', m)}"
            per[m] = dict(
                gamma=g["gamma"],
                lo=g["ci_sidak"][0],
                hi=g["ci_sidak"][1],
                X=g["exclusion_mde80"],
                reject=(None if r.get("noverdict") else bool(g["reject"])),
                k=[g.get("k_a", g.get("k")), g.get("k_b", g.get("k"))],
                est=ledger.stated(
                    vals["est"],
                    led["est"],
                    figure=FIG,
                    what=f"{r['id']} {m} estimate",
                    source=where,
                ),
                ci=ledger.stated(
                    vals["ci"],
                    led["ci"],
                    figure=FIG,
                    what=f"{r['id']} {m} Šidák CI",
                    source=where,
                ),
                z=(
                    None
                    if r.get("noverdict")
                    # estimate and interval only
                    else ledger.stated(
                        vals["z"],
                        led["z"],
                        figure=FIG,
                        what=f"{r['id']} {m} z",
                        source=where,
                    )
                ),
                Xt=(
                    ledger.stated(
                        vals["X"],
                        led["X"],
                        figure=FIG,
                        what=f"{r['id']} {m} 80 %-power MDE X",
                        source=where,
                    )
                    if (
                        r["id"] in ("G", "G60")
                        or (r["id"] == "G4" and m == "completion")
                    )
                    else None
                ),
                floor=(floor[m] if r["id"] == "G" else None),
                # MDE80 band only on the confirmatory family and where the record
                # states an exclusion bound (X₄, completion); out-of-family rows
                # otherwise show estimate and interval only
                # (builder's audit, 2026-10-10)
                band=(
                    r["id"] in ("G", "G60") or (r["id"] == "G4" and m == "completion")
                ),
            )
        out_rows.append({**{k: v for k, v in r.items()}, "m": per})
    # registered consequences (UNBLIND RESULT; post_gamma4_t2000.md:18-19)
    consequence = {
        "survival_rate": "does not survive the inert-share correction",
        "completion": "second exclusion bound",
    }
    return dict(
        rows=out_rows,
        foot=FOOT,
        consequence=consequence,
        metrics=[
            dict(
                k="completion",
                name="completion",
                axis="Δ completion (fraction of food collected)",
                dom=[-0.068, 0.056],
            ),
            dict(
                k="survival_rate",
                name="survival",
                axis="Δ survival rate (fraction of agents alive at t = 256)",
                dom=[-0.0115, 0.0185],
            ),
        ],
    )


CSS = load_template("ladder.css")

BODY = load_template("ladder.html")

JS = load_template("ladder.js")


def main():
    data = build_data()
    html = page("Registered readings", BODY, CSS, JS, data)
    out = OUT_HTML / "ladder_registered_readings.html"
    out.write_text(html, encoding="utf-8")
    hits = check_html(out)
    assert not hits, hits
    (OUT_DATA / "ladder_pending.json").write_text(
        json.dumps(ledger.pending(), indent=1, ensure_ascii=False) + "\n"
    )
    print(
        f"{out.name}: {out.stat().st_size / 1e3:.1f} KB; "
        f"pending ledger rows: {len(ledger.pending())}"
    )
    return data


if __name__ == "__main__":
    main()
