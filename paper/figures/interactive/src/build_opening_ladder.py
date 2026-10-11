"""Compact opening ladder for §1: Γ (k = 72) and Γ₄ on both co-primaries,
always together (OPENING AND §1 REOPENED, item 3; FIGURE BATCH RULINGS A1:
never Γ without Γ₄'s "does not survive the inert-share correction").

Built from the full ladder's own data (`build_ladder.build_data()`), so every
value, assertion and ledger routing is shared with F2. No toggles: the figure
cannot be put in a state that shows Γ alone.

Run from the repo root:
    uv run python paper/figures/interactive/src/build_opening_ladder.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_ladder  # noqa: E402
from common_web import OUT_HTML, check_html, load_template, page  # noqa: E402

CSS = load_template("opening_ladder.css")
BODY = load_template("opening_ladder.html")
JS = load_template("opening_ladder.js")

META = {
    "G": "k 72 / 72 · confirmatory family · unit 1",
    "G4": "k 72 / 20 · ISO-4: sensitivity arm, outside the confirmatory family "
    "· cross-unit",
}
FOOT = (
    "ISO-4 is ISO without its δ-only components; its reading rule was "
    "registered on 2026-09-18, before unblinding. k = 72 is a recorded "
    "deviation: the registered seed ladder's cap was 60, raised to 72 on "
    "2026-09-22, pre-unblind."
)


def build_data():
    full = build_ladder.build_data()
    rows = [r for r in full["rows"] if r["id"] in ("G", "G4")]
    assert [r["id"] for r in rows] == ["G", "G4"]
    for r in rows:
        r["meta"] = META[r["id"]]
        for m in ("completion", "survival_rate"):
            assert r["m"][m]["reject"] is not None  # both carry a recorded verdict
    g4c = rows[1]["m"]["completion"]
    assert g4c["Xt"] == "0.0488"  # RES-6
    consequence = {
        "survival_rate": dict(text=full["consequence"]["survival_rate"], kind="fill"),
        "completion": dict(
            text=full["consequence"]["completion"] + ", X₄ = " + g4c["Xt"],
            kind="line",
        ),
    }
    assert consequence["survival_rate"]["text"] == (
        "does not survive the inert-share correction"
    )
    metrics = [
        dict(
            k="survival_rate",
            name="survival",
            axis="Δ survival rate (fraction)",
            dom=[-0.009, 0.0165],
            ticks=[-0.005, 0.0, 0.005, 0.01, 0.015],
            dp=3,
        ),
        dict(
            k="completion",
            name="completion",
            axis="Δ completion (fraction)",
            dom=[-0.055, 0.03],
            ticks=[-0.04, -0.02, 0.0, 0.02],
            dp=2,
        ),
    ]
    return dict(rows=rows, metrics=metrics, consequence=consequence, foot=FOOT)


def main():
    data = build_data()
    out = OUT_HTML / "opening_ladder.html"
    out.write_text(page("Registered readings", BODY, CSS, JS, data), encoding="utf-8")
    hits = check_html(out)
    assert not hits, hits
    print(f"{out.name}: {out.stat().st_size / 1e3:.1f} KB")
    return data


if __name__ == "__main__":
    main()
