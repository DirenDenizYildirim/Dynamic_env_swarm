"""F3 Training-mixture composer: what each arm's training distribution contained.

Display only: no slider, no prediction. Sources: the committed configs
che/configs/p6_iso.yaml, p6_iso4.yaml, p6_joint.yaml (mixture.components),
read with che.env.config.load_config. The behavioural reading of ISO's
δ-only third (no active stressor) is DES-8; the active share and the 2×
ratio are DES-14; the 3× ratio is DES-7.

Run from the repo root:  uv run python paper/figures/interactive/src/build_composer.py
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common_web import (  # noqa: E402
    OUT_DATA,
    OUT_HTML,
    REPO,
    check_html,
    load_template,
    page,
)

sys.path.insert(0, str(REPO))
from che.env.config import load_config  # noqa: E402

ARMS = [("ISO", "p6_iso.yaml"), ("ISO-4", "p6_iso4.yaml"), ("JOINT", "p6_joint.yaml")]


def frac(w: float) -> Fraction:
    f = Fraction(w).limit_denominator(12)
    assert abs(float(f) - w) < 1e-5, (w, f)
    return f


def arm_data(name: str, cfgfile: str) -> dict:
    cfg = load_config(str(REPO / "che/configs" / cfgfile))
    comps = []
    total = sum(c.weight for c in cfg.env.mixture.components)
    for c in cfg.env.mixture.components:
        w = frac(c.weight / total)
        comps.append(
            dict(
                name=c.name,
                w=str(w),
                wf=float(w),
                beta=c.beta,
                kA=c.kappa_A,
                kB=c.kappa_B,
                d=c.delta,
                A=c.kappa_A > 0,
                B=c.kappa_B > 0,
                D=c.delta > 0,
            )
        )

    # behavioural type: delta inert (DES-8); nominal type: delta counted
    def typ(c, behavioural):
        if c["A"] and c["B"]:
            return "AB"
        if c["A"]:
            return "A"
        if c["B"]:
            return "B"
        return "F" if behavioural else "D"

    out = {"name": name, "components": comps}
    for view in ("beh", "nom"):
        shares = {}
        for c in comps:
            t = typ(c, view == "beh")
            shares[t] = shares.get(t, Fraction(0)) + Fraction(c["w"])
        mA = sum((Fraction(c["w"]) for c in comps if c["A"]), Fraction(0))
        mB = sum((Fraction(c["w"]) for c in comps if c["B"]), Fraction(0))
        active = sum(
            (
                Fraction(c["w"])
                for c in comps
                if c["A"] or c["B"] or (view == "nom" and c["D"])
            ),
            Fraction(0),
        )
        out[view] = dict(
            shares={k: str(v) for k, v in shares.items()},
            mA=str(mA),
            mB=str(mB),
            active=str(active),
        )
    return out


def build_data():
    arms = [arm_data(n, f) for n, f in ARMS]
    a = {x["name"]: x for x in arms}
    # Assert the ledger rows before anything is drawn.
    assert a["ISO"]["beh"]["mA"] == "1/3" and a["ISO"]["beh"]["mB"] == "1/3"  # DES-7
    assert a["JOINT"]["beh"]["mA"] == "1" and a["JOINT"]["beh"]["mB"] == "1"  # DES-7
    assert a["ISO"]["beh"]["shares"]["F"] == "1/3"  # DES-8
    assert (
        a["ISO-4"]["beh"]["mA"] == "1/2" and a["ISO-4"]["beh"]["mB"] == "1/2"
    )  # DES-14
    assert [a[k]["beh"]["active"] for k in ("ISO", "ISO-4", "JOINT")] == [
        "2/3",
        "1",
        "1",
    ]  # DES-14
    assert (
        Fraction(a["JOINT"]["beh"]["mA"]) / Fraction(a["ISO"]["beh"]["mA"]) == 3
    )  # DES-7
    assert (
        Fraction(a["JOINT"]["beh"]["mA"]) / Fraction(a["ISO-4"]["beh"]["mA"]) == 2
    )  # DES-14
    assert (
        a["ISO"]["nom"]["active"] == "1"
    )  # config header "no-element 0.0000" (p6_iso.yaml:7)
    return dict(arms=arms, ratios={"JOINT": "3× ISO · 2× ISO-4"})


CSS = load_template("composer.css")

BODY = load_template("composer.html")

JS = load_template("composer.js")


def main():
    data = build_data()
    out = OUT_HTML / "composer_training_mixtures.html"
    out.write_text(page("Training mixtures", BODY, CSS, JS, data), encoding="utf-8")
    hits = check_html(out)
    assert not hits, hits
    (OUT_DATA / "composer_data.json").write_text(
        json.dumps(data, indent=1, ensure_ascii=False) + "\n"
    )
    print(f"{out.name}: {out.stat().st_size / 1e3:.1f} KB")


if __name__ == "__main__":
    main()
