"""F5 Secondary simplex: where the secondary arms sit relative to ISO, ISO-4 and
JOINT, and whether the plane fitted over them reaches JOINT.

Non-verdict-bearing throughout. Sources (committed, read-only):
  che/bench/results/phase6/secondary/secondary.json
      design, metrics.*, mediation, replicate
  che/bench/results/phase6/post_unblind_analysis/post_gamma4_t2000.json   gamma4 (Γ₄, B̂)
Arm coordinates: sweep and identification from `design` (DES-9); ISO (p 0, n 1/3)
DES-7/DES-8; ISO-4 and sweep_c50_p000 (0, 0) and JOINT (1, 0) DES-14.
In (p, n), the per-stressor marginal is m = (1 + p − n)/2 (single-stressor
episodes split evenly between A and B): sweep m 0.5, identification m 0.4,
ISO m 1/3, JOINT m 1 — the iso-m lines are drawn as reference lines.

Run from the repo root:  uv run python paper/figures/interactive/src/build_simplex.py
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
FIG = "F5 simplex"


def f4(x):
    return ("+" if x > 0 else ("−" if x < 0 else "")) + f"{abs(x):.4f}"


def ci(a):
    return f"[{f4(a[0])}, {f4(a[1])}]"


def build_data():
    ledger.reset()
    sc = json.loads((P6 / "secondary/secondary.json").read_text())
    g4 = json.loads((P6 / "post_unblind_analysis/post_gamma4_t2000.json").read_text())
    design = sc["design"]
    for a in design:  # m = (1 + p - n)/2 holds for every secondary arm
        assert abs((1 + a["p"] - a["n"]) / 2 - a["m"]) < 1e-9, a
    assert sc["mediation"]["void"] is True
    metrics = {}
    for m, name in (("survival_rate", "survival"), ("completion", "completion")):
        M = sc["metrics"][m]
        cf, dt, ep, kn = M["confound"], M["dose_trend"], M["endpoint_grade"], M["knee"]
        assert kn["underpowered"] is True
        surv = m == "survival_rate"
        src = f"secondary.json → metrics.{m}"

        def row(
            key,
            label,
            est,
            ci95,
            rowid,
            kind,
            what,
            extra_src="",
            est_rowid="same",
            name=name,
            src=src,
        ):
            est_rowid = rowid if est_rowid == "same" else est_rowid
            return dict(
                key=key,
                label=label,
                g=est,
                lo=ci95[0] if ci95 else None,
                hi=ci95[1] if ci95 else None,
                kind=kind,
                est=ledger.stated(
                    f4(est),
                    est_rowid,
                    figure=FIG,
                    what=f"{name} {what}",
                    source=src + extra_src,
                ),
                ci=(
                    ledger.stated(
                        ci(ci95),
                        rowid,
                        figure=FIG,
                        what=f"{name} {what} 95 % CI",
                        source=src + extra_src,
                    )
                    if ci95
                    else None
                ),
            )

        rows_sec = [
            row(
                "slope",
                "dose slope, sweep, per unit p",
                dt["ols_slope_per_unit_p"],
                dt["ols_slope_ci95"],
                "SEC-5" if surv else None,
                "sec",
                "dose slope",
                ".dose_trend",
            ),
            row(
                "endpoint",
                "endpoint, sweep p = 0.5 − p = 0",
                ep["endpoint_diff"],
                ep["ci95"],
                "SEC-5" if surv else None,
                "sec",
                "endpoint",
                ".endpoint_grade",
            ),
            row(
                "gp",
                "γ_p, per unit p (plane)",
                cf["gamma_p"],
                cf["gamma_p_ci95"],
                "SEC-1" if surv else None,
                "sec",
                "γ_p",
                ".confound",
            ),
            row(
                "gn",
                "γ_n, per unit n (plane)",
                cf["gamma_n"],
                cf["gamma_n_ci95"],
                "SEC-1" if surv else None,
                "sec",
                "γ_n",
                ".confound",
            ),
            row(
                "bound",
                "no-element share of the sweep's endpoint change",
                cf["bound_confound_share_of_sweep_change"],
                cf["bound_ci95"],
                "SEC-2" if surv else None,
                "sec",
                "bound",
                ".confound",
            ),
        ]
        G4 = g4["gamma4"]["per_metric"][m]["gamma4"]
        BH = g4["gamma4"]["per_metric"][m]["b_hat"]
        G4p = sc["replicate"][m]["gamma4_prime"]
        rows_pred = [
            row(
                "predJ",
                "plane prediction, JOINT − ISO-4 = γ_p × 1",
                cf["gamma_p"],
                cf["gamma_p_ci95"],
                "SEC-4" if surv else None,
                "pred",
                "plane prediction JOINT − ISO-4",
                ".confound.gamma_p",
            ),
            row(
                "g4",
                "Γ₄ = JOINT − ISO-4, measured",
                G4["gamma"],
                G4["ci_sidak"],
                "RES-6" if surv else None,
                "meas",
                "Γ₄",
                " (post_gamma4_t2000.json → gamma4)",
                est_rowid="RES-6",
            ),
            row(
                "g4p",
                "Γ₄′ = JOINT − sweep_c50_p000, measured",
                G4p["gamma"],
                G4p["ci_sidak"],
                "RES-8" if surv else None,
                "meas",
                "Γ₄′",
                ".replicate",
                est_rowid="RES-8",
            ),
        ]
        grp_j = dict(
            group="JOINT − ISO-4: plane prediction from γ_p, measured Γ₄ and Γ₄′"
        )
        grp_b = dict(group="ISO-4 − ISO: plane prediction from γ_n, measured B̂")
        if surv:
            rows_pred[0]["est"] = (
                "≈ +0.033"  # SEC-4 as printed; its interval is γ_p's (SEC-1)
            )
        rows_pred = [grp_j] + rows_pred
        if surv:
            # SEC-3: γ_n × (0 − 1/3), no committed interval -> point only
            pred_b = cf["gamma_n"] * (0 - 1 / 3)
            assert f4(pred_b) == "+0.0079"
            rows_pred = (
                [grp_b]
                + [
                    dict(
                        key="predB",
                        label="plane prediction, ISO-4 − ISO = γ_n × (0 − 1/3)",
                        g=pred_b,
                        lo=None,
                        hi=None,
                        kind="pred",
                        est=ledger.stated(
                            "+0.0079", "SEC-3", figure=FIG, what="SEC-3", source="SEC-3"
                        ),
                        ci=None,
                    ),
                    row(
                        "bh",
                        "B̂ = ISO-4 − ISO, measured",
                        BH["gamma"],
                        BH["ci_sidak"],
                        "RES-7",
                        "meas",
                        "B̂",
                        " (post_gamma4_t2000.json → gamma4)",
                    ),
                ]
                + rows_pred
            )
            # ledger checks
            assert (
                f4(cf["gamma_p"]) == "+0.0326"
                and ci(cf["gamma_p_ci95"]) == "[+0.0137, +0.0502]"
            )
            assert (
                f4(cf["gamma_n"]) == "−0.0237"
                and ci(cf["gamma_n_ci95"]) == "[−0.0419, −0.0057]"
            )
            assert f4(cf["bound_confound_share_of_sweep_change"]) == "−0.0119"
            assert ci(cf["bound_ci95"]) == "[−0.0210, −0.0028]"
            assert (
                f4(dt["ols_slope_per_unit_p"]) == "+0.0089"
                and ci(dt["ols_slope_ci95"]) == "[−0.0033, +0.0211]"
            )
            assert (
                f4(ep["endpoint_diff"]) == "+0.0048"
                and ci(ep["ci95"]) == "[−0.0021, +0.0117]"
            )
            assert (
                f4(G4["gamma"]) == "−0.0003"
                and f4(G4p["gamma"]) == "+0.0013"
                and f4(BH["gamma"]) == "+0.0098"
            )
        means = {
            a["arm"]: dict(mean=a["mean"], fit=a["fit"])
            for a in cf["arm_means_vs_plane"]
        }
        metrics[m] = dict(
            name=name,
            sec=rows_sec,
            pred=rows_pred,
            means=means,
            dom=[-0.045, 0.056] if surv else [-0.17, 0.14],
        )
    arms = [
        dict(
            arm=a["arm"],
            p=a["p"],
            n=round(a["n"], 6),
            m=a["m"],
            kind="sweep" if a["arm"].startswith("sweep") else "ident",
        )
        for a in design
    ]
    refs = [
        dict(arm="ISO", p=0, n=1 / 3, m="1/3"),
        dict(arm="ISO-4 = sweep_c50_p000", p=0, n=0, m="0.5"),
        dict(arm="JOINT", p=1, n=0, m="1"),
    ]
    return dict(
        arms=arms,
        refs=refs,
        metrics=metrics,
        isom=[
            dict(m="1/3", c=-1 / 3),
            dict(m="0.4", c=-0.2),
            dict(m="0.5", c=0.0),
            dict(m="1", c=1.0),
        ],
    )


CSS = load_template("simplex.css")

BODY = load_template("simplex.html")

JS = load_template("simplex.js")


def main():
    data = build_data()
    out = OUT_HTML / "simplex_secondary.html"
    out.write_text(page("Secondary design", BODY, CSS, JS, data), encoding="utf-8")
    hits = check_html(out)
    assert not hits, hits
    (OUT_DATA / "simplex_pending.json").write_text(
        json.dumps(ledger.pending(), indent=1, ensure_ascii=False) + "\n"
    )
    print(
        f"{out.name}: {out.stat().st_size / 1e3:.1f} KB; "
        f"pending: {len(ledger.pending())}"
    )


if __name__ == "__main__":
    main()
