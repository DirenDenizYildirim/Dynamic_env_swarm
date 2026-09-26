"""P6 SECONDARY — the dose sweep, the identification arm and mediation.

Labelled NON-VERDICT-BEARING throughout (design v2 §7, final-five ruling 4;
ENDPOINT CONFOUND entry, 2026-09-22): nothing here enters the confirmatory
family, decides a branch, or relabels one. Written, tested on SYNTHETIC
artifacts only, and committed BEFORE any sweep or identification-arm eval was
read — the sweep's numbers are unseen at this commit even though Γ is not.

What is registered (design v2 §7; decision log 2026-08-02, remedy ruling 2):

  DOSE TREND   isotonic dose-trend on the c = 0.5 sweep, p ∈ {0 … 0.5}.
  KNEE         bootstrap-over-seeds knee CI, with an AUTOMATIC UNDERPOWERED
               flag if the CI spans the sweep.
  CONFOUND     the c = 0.4 identification-arm confound bound: two sweeps at
               different marginals make co-occurrence and the no-element share
               separately identifiable, so the confound is BOUNDED.
  MEDIATION    realized co-active visitation is endogenous, so it is presented
               as mediation, never as causal regression. "If realized dose
               does not vary with assigned p, the dose figure has no x-axis
               and is declared VOID."
  FLOORS       every claim carries its floor-grade; the sweep_p500 floor is
               ASSUMED COMMON for the intermediate points (flagged); the
               identification arm has no floor (UNGRADED).

Builder interpretations the registered text did not spell out — OWED OWNER
RATIFICATION BEFORE this runs on the real sweep (decision log 2026-09-26):

  (S1) DOSE TREND: pool-adjacent-violators on the five arm means, in the
       direction of the sign of the seed-level OLS slope of y on p; the OLS
       slope and its bootstrap 95 % CI are the trend statistic; the endpoint
       difference y(0.5) − y(0) is floor-graded against the sweep floor.
  (S2) KNEE: the breakpoint κ ∈ {0.125, 0.25, 0.375} of the best single-hinge
       fit y = a + b·p + c·(p − κ)₊ on seed-level data. B = 2000 bootstrap
       resamples of seeds WITHIN each arm (unpaired). "Spans the sweep" =
       the 95 % percentile interval contains both 0.125 and 0.375 →
       UNDERPOWERED.
  (S3) CONFOUND BOUND: seed-level OLS y = γ0 + γ_p·p + γ_n·n on all eight
       arms (n = 1 − 2m + p, the no-element share). γ_p = co-occurrence at
       fixed no-element share; γ_n = the no-element share at fixed
       co-occurrence. The c = 0.5 sweep's slope decomposes as γ_p + γ_n;
       THE BOUND is the bootstrap 95 % CI of 0.5·γ_n, the confound's share of
       the sweep's endpoint change. Linearity is an assumption: the residual
       of the 8 arm means about the fit is reported against their SE.
  (S4) MEDIATION: realized dose = a run's training-log `co_active_per_step`
       averaged over updates 1…1000. First stage: its seed-level OLS slope on
       p over the c = 0.5 sweep. VOID iff that slope's bootstrap 95 % CI
       contains 0. If not void, only the per-arm (realized dose, outcome)
       table for the figure is produced — no second-stage coefficient.
  (S5) NEW — SAME-CARD REPLICATE of the inert-share check. `sweep_c50_p000`
       and ISO-4 have the IDENTICAL training mixture ({A-only, B-only} ×
       {0.43, 0.70} at 0.25), the sweep's trained on the confirmatory card.
       Γ₄' = JOINT − sweep_c50_p000 (k 72 vs 20, z_α = 2.2365, as ruling v)
       is reported BESIDE the registered Γ₄; R = sweep_c50_p000 − ISO-4 is
       the cross-card replicate difference (descriptive, 95 %). Neither can
       change the registered Γ₄ qualifier; a disagreement is reported, not
       resolved.
  (S6) Every secondary interval is a two-sided 95 % interval (not family-
       corrected, because nothing here is in the family), except Γ₄', which
       is read at z_α to be comparable with Γ₄.

USAGE on the frozen tree, after the unblind has been logged:

    uv run python -m che.scripts.p6_secondary
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import math
import statistics
from pathlib import Path

import numpy as np

from che.scripts import p6_post_analysis as PA
from che.scripts import p6_unblind as U
from che.scripts.m62_report import K_SECONDARY, T_STAR

Refusal = U.Refusal
FAMILY = U.FAMILY
THETA = U.EVAL_CONFIG

# ------------------------------------------------------------------ design
# (arm, per-element marginal m, co-occurrence p). The no-element share is
# n = 1 − 2m + p; test_p6_secondary asserts all three against the generated
# config headers, so a regenerated config cannot drift silently.
SWEEP = (
    ("sweep_c50_p000", 0.5, 0.0),
    ("sweep_c50_p125", 0.5, 0.125),
    ("sweep_c50_p250", 0.5, 0.25),
    ("sweep_c50_p375", 0.5, 0.375),
    ("sweep_c50_p500", 0.5, 0.5),
)
IDENT = (
    ("ident_c40_p000", 0.4, 0.0),
    ("ident_c40_p200", 0.4, 0.2),
    ("ident_c40_p400", 0.4, 0.4),
)
ARMS = SWEEP + IDENT
KNEES = (0.125, 0.25, 0.375)  # interior sweep points
K_SEC = K_SECONDARY  # 20
RECARD_SEEDS = tuple(range(1, 13))  # single-card re-card (SINGLE-CARD amendment)
GRID_SEEDS = tuple(range(13, K_SEC + 1))  # g1_grid seeds 13..20, 5090
N_BOOT = 2000
BOOT_SEED = 20260926  # registered with the instrument; fixes every resample
Z95 = 1.959964
P6 = Path("che/bench/results/phase6")


def no_element(m: float, p: float) -> float:
    """P(neither) = 1 − P(A) − P(B) + P(A∧B) for a symmetric pair."""
    return 1.0 - 2.0 * m + p


# ------------------------------------------------------------------ reading


def _source(recard: Path, grid: Path, seed: int) -> Path:
    """Seeds 1–12 come ONLY from the single-card re-card; 13–20 from g1_grid.
    g1_grid's own seeds 1–12 (PRO 6000, superseded) are never opened."""
    if seed in RECARD_SEEDS:
        return recard
    if seed in GRID_SEEDS:
        return grid
    raise Refusal(f"seed {seed} outside 1..{K_SEC}")


def _realized_dose(log: Path) -> float:
    ys = []
    for ln in log.read_text().splitlines():
        if not ln.strip():
            continue
        r = json.loads(ln)
        u, y = int(r["update"]), r.get("co_active_per_step")
        if (
            1 <= u <= T_STAR
            and y is not None
            and not (isinstance(y, float) and math.isnan(y))
        ):
            ys.append(float(y))
    if not ys:
        raise Refusal(f"{log}: no co_active_per_step rows in updates 1..{T_STAR}")
    return statistics.mean(ys)


def load_arm(recard: Path, grid: Path, arm: str) -> dict:
    """Per-seed metric means at θ* (every guard of the confirmatory reader)
    plus the run's realized training dose."""
    vals: dict = {m: [] for m in FAMILY}
    dose: list[float] = []
    for s in range(1, K_SEC + 1):
        d = _source(recard, grid, s)
        tag = f"{arm}_s{s}"
        entry = d / ".manifest" / f"{tag}.done"
        if not (entry.is_file() and entry.stat().st_size > 0):
            raise Refusal(f"{d}/{tag}: no manifest entry — incomplete run.")
        ev = PA.read_eval(d / f"eval_{tag}.json", T_STAR, THETA)
        for m in FAMILY:
            vals[m].append(ev[m])
        dose.append(_realized_dose(d / f"{tag}.jsonl"))
    return {"metrics": vals, "dose": dose}


def check_stamps(recard: Path, grid: Path) -> None:
    for d, k in ((recard, len(RECARD_SEEDS)), (grid, K_SEC)):
        st = U.read_stamp(d)
        if st.get("updates") != str(T_STAR) or st.get("eval_config") != THETA:
            raise Refusal(f"{d}: not a T*={T_STAR} θ* artifact.")
        if st.get("k_sec") != str(k):
            raise Refusal(f"{d}: stamp k_sec {st.get('k_sec')!r}, need {k}.")
        have = {a.split(":")[0] for a in st.get("sec_arms", "").split()}
        want = {a for a, _, _ in ARMS}
        if not want <= have:
            raise Refusal(f"{d}: stamp lacks secondary arms {sorted(want - have)}.")


# --------------------------------------------------------------- statistics


def _ols(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    return np.linalg.lstsq(x, y, rcond=None)[0]


def pava(y: list[float], w: list[float], increasing: bool) -> list[float]:
    """Weighted pool-adjacent-violators: the isotonic fit to y."""
    sgn = 1.0 if increasing else -1.0
    blocks: list[list[float]] = []  # [weighted mean, weight, count]
    for yi, wi in zip(y, w, strict=True):
        blocks.append([sgn * yi, wi, 1])
        while len(blocks) > 1 and blocks[-2][0] > blocks[-1][0]:
            m2, w2, c2 = blocks.pop()
            m1, w1, c1 = blocks.pop()
            blocks.append([(m1 * w1 + m2 * w2) / (w1 + w2), w1 + w2, c1 + c2])
    out: list[float] = []
    for mu, _, c in blocks:
        out += [sgn * mu] * c
    return out


def _boot_indices(rng: np.random.Generator, sizes: list[int]) -> list[np.ndarray]:
    """One bootstrap draw: seeds resampled WITH replacement within each arm."""
    return [rng.integers(0, n, n) for n in sizes]


def _slope(ps: np.ndarray, ys: np.ndarray) -> float:
    x = np.column_stack([np.ones_like(ps), ps])
    return float(_ols(x, ys)[1])


def _hinge_knee(ps: np.ndarray, ys: np.ndarray) -> float:
    best, arg = math.inf, KNEES[0]
    for k in KNEES:
        x = np.column_stack([np.ones_like(ps), ps, np.maximum(ps - k, 0.0)])
        r = ys - x @ _ols(x, ys)
        sse = float(r @ r)
        if sse < best - 1e-15:
            best, arg = sse, k
    return arg


def _confound_fit(ps: np.ndarray, ns: np.ndarray, ys: np.ndarray) -> np.ndarray:
    x = np.column_stack([np.ones_like(ps), ps, ns])
    return _ols(x, ys)


def _ci(samples: list[float], discrete: bool = False) -> list[float]:
    """Percentile 95 % interval; `discrete` keeps knee bounds on the grid."""
    a = np.asarray(samples)
    method = "inverted_cdf" if discrete else "linear"
    return [
        float(np.quantile(a, 0.025, method=method)),
        float(np.quantile(a, 0.975, method=method)),
    ]


def analyse_metric(arms: dict, metric: str, floor_sd: float | None) -> dict:
    """S1, S2, S3 and the endpoint floor-grade, for one co-primary."""
    rng = np.random.default_rng(BOOT_SEED)
    sw = [a for a, _, _ in SWEEP]
    allarms = [a for a, _, _ in ARMS]
    p_of = {a: p for a, _, p in ARMS}
    n_of = {a: no_element(m, p) for a, m, p in ARMS}

    def data(names, idxs=None):
        ys, ps, ns = [], [], []
        for j, a in enumerate(names):
            v = np.asarray(arms[a]["metrics"][metric])
            if idxs is not None:
                v = v[idxs[j]]
            ys.append(v)
            ps.append(np.full(len(v), p_of[a]))
            ns.append(np.full(len(v), n_of[a]))
        return np.concatenate(ps), np.concatenate(ns), np.concatenate(ys)

    ps, _, ys = data(sw)
    means = [statistics.mean(arms[a]["metrics"][metric]) for a in sw]
    slope = _slope(ps, ys)
    inc = slope >= 0
    w = [float(len(arms[a]["dose"])) for a in sw]
    iso = pava(means, w, inc)
    iso_opp = pava(means, w, not inc)
    knee = _hinge_knee(ps, ys)

    pa, na, ya = data(allarms)
    g = _confound_fit(pa, na, ya)

    sizes = [len(arms[a]["dose"]) for a in allarms]
    b_slope, b_knee, b_gp, b_gn = [], [], [], []
    for _ in range(N_BOOT):
        idx = _boot_indices(rng, sizes)
        pb, _, yb = data(sw, idx[: len(sw)])
        b_slope.append(_slope(pb, yb))
        b_knee.append(_hinge_knee(pb, yb))
        pab, nab, yab = data(allarms, idx)
        gb = _confound_fit(pab, nab, yab)
        b_gp.append(float(gb[1]))
        b_gn.append(float(gb[2]))

    knee_ci = _ci(b_knee, discrete=True)
    spans = knee_ci[0] <= KNEES[0] and knee_ci[1] >= KNEES[-1]
    # residual of the 8 arm means about the (p, n) plane, against their SE
    am = []
    for a in allarms:
        v = arms[a]["metrics"][metric]
        fit = g[0] + g[1] * p_of[a] + g[2] * n_of[a]
        am.append(
            {
                "arm": a,
                "mean": statistics.mean(v),
                "fit": float(fit),
                "resid_over_se": (statistics.mean(v) - float(fit))
                / (statistics.stdev(v) / math.sqrt(len(v))),
            }
        )
    out = {
        "sweep_means": dict(zip(sw, means, strict=True)),
        "dose_trend": {
            "ols_slope_per_unit_p": slope,
            "ols_slope_ci95": _ci(b_slope),
            "direction": "nondecreasing" if inc else "nonincreasing",
            "isotonic_fit": dict(zip(sw, iso, strict=True)),
            "sse_chosen": sum((m - f) ** 2 for m, f in zip(means, iso, strict=True)),
            "sse_opposite": sum(
                (m - f) ** 2 for m, f in zip(means, iso_opp, strict=True)
            ),
        },
        "knee": {
            "kappa": knee,
            "ci95": knee_ci,
            "boot_freq": {str(k): b_knee.count(k) / N_BOOT for k in KNEES},
            "underpowered": spans,
            "flag": "UNDERPOWERED — the knee CI spans the sweep" if spans else "",
        },
        "confound": {
            "gamma_p": float(g[1]),
            "gamma_p_ci95": _ci(b_gp),
            "gamma_n": float(g[2]),
            "gamma_n_ci95": _ci(b_gn),
            "sweep_slope_decomposed": float(g[1] + g[2]),
            "bound_confound_share_of_sweep_change": 0.5 * float(g[2]),
            "bound_ci95": [0.5 * x for x in _ci(b_gn)],
            "arm_means_vs_plane": am,
        },
    }
    # the sweep's endpoint difference, floor-graded
    a0, a5 = sw[0], sw[-1]
    v0, v5 = arms[a0]["metrics"][metric], arms[a5]["metrics"][metric]
    d = statistics.mean(v5) - statistics.mean(v0)
    se = math.sqrt(
        statistics.variance(v0) / len(v0) + statistics.variance(v5) / len(v5)
    )
    grade: dict = {
        "endpoint_diff": d,
        "se_seed": se,
        "ci95": [d - Z95 * se, d + Z95 * se],
    }
    if floor_sd:
        sef = math.sqrt(2 * floor_sd**2 / K_SEC)
        grade.update(
            {
                "floor_sd_sweep_p500": floor_sd,
                "se_floor_basis": sef,
                "diff_over_floor_se": abs(d) / sef,
                "floor_note": "sweep_p500 floor ASSUMED COMMON at p = 0 (flagged)",
            }
        )
    else:
        grade["floor_note"] = "UNGRADED — no sweep floor supplied"
    out["endpoint_grade"] = grade
    return out


def mediation(arms: dict) -> dict:
    """S4: first stage only, and the per-arm table for the dose figure."""
    sw = [a for a, _, _ in SWEEP]
    p_of = {a: p for a, _, p in ARMS}
    rng = np.random.default_rng(BOOT_SEED + 1)
    ps = np.concatenate([np.full(K_SEC, p_of[a]) for a in sw])
    ds = np.concatenate([np.asarray(arms[a]["dose"]) for a in sw])
    slope = _slope(ps, ds)
    boots = []
    for _ in range(N_BOOT):
        idx = _boot_indices(rng, [K_SEC] * len(sw))
        db = np.concatenate(
            [np.asarray(arms[a]["dose"])[i] for a, i in zip(sw, idx, strict=True)]
        )
        boots.append(_slope(ps, db))
    ci = _ci(boots)
    void = ci[0] <= 0.0 <= ci[1]
    table = [
        {
            "arm": a,
            "p": p_of[a],
            "realized_dose_mean": statistics.mean(arms[a]["dose"]),
            "realized_dose_sd": statistics.stdev(arms[a]["dose"]),
            **{f"{m}_mean": statistics.mean(arms[a]["metrics"][m]) for m in FAMILY},
        }
        for a in sw
    ]
    return {
        "first_stage_slope": slope,
        "first_stage_ci95": ci,
        "void": void,
        "verdict": "VOID — realized dose does not vary with assigned p; the dose "
        "figure has no x-axis"
        if void
        else "first stage holds; the dose figure is presented as MEDIATION, never "
        "as causal regression",
        "figure_table": None if void else table,
    }


def replicate(arms: dict, conf: Path, iso4: Path) -> dict:
    """S5: the same-card replicate of the inert-share check."""
    U.check_stamp(U.read_stamp(conf), U.K_CONFIRMATORY_REALIZED)
    PA.check_block_stamp(iso4, T_STAR, K_SEC, ("iso4",))
    joint = U.load_arm(conf, "joint", range(1, U.K_CONFIRMATORY_REALIZED + 1))
    i4 = PA.load_grid_arm(iso4, "iso4", K_SEC, T_STAR)
    out: dict = {}
    for m in FAMILY:
        p0 = arms["sweep_c50_p000"]["metrics"][m]
        g4p = PA.contrast(p0, joint[m])  # z_alpha reading, as ruling (v)
        r = PA.contrast(i4[m], p0, decision=False)  # sweep_p000 − ISO-4
        out[m] = {"gamma4_prime": g4p, "replicate_diff": r}
    return out


# ------------------------------------------------------------------ report


def render(res: dict) -> str:
    L = [
        "# Phase-6 SECONDARY — dose sweep, identification arm, mediation",
        "",
        f"git `{res['provenance']['git_commit']}` (dirty files: "
        f"{res['provenance']['git_dirty_files']}) · {res['timestamp']}",
        "",
        "**NON-VERDICT-BEARING.** Nothing here enters the confirmatory family or "
        "moves a branch. Intervals are 95 %, bootstrap-over-seeds within arm "
        f"(B = {N_BOOT}, seed {BOOT_SEED}), conditional on the common eval draw.",
        "",
        "| arm | m | p | no-element n |",
        "|---|---|---|---|",
    ]
    for a, m, p in ARMS:
        L.append(f"| {a} | {m} | {p} | {no_element(m, p):.3f} |")
    L.append("")
    for metric in FAMILY:
        r = res["metrics"][metric]
        t, k, c, e = r["dose_trend"], r["knee"], r["confound"], r["endpoint_grade"]
        L += [
            f"## {metric}",
            "",
            "| p | " + " | ".join(str(p) for _, _, p in SWEEP) + " |",
            "|---|" + "---|" * len(SWEEP),
            "| mean | "
            + " | ".join(f"{v:.4f}" for v in r["sweep_means"].values())
            + " |",
            f"| isotonic ({t['direction']}) | "
            + " | ".join(f"{v:.4f}" for v in t["isotonic_fit"].values())
            + " |",
            "",
            f"- dose trend: OLS slope {t['ols_slope_per_unit_p']:+.4f} per unit p, "
            f"95 % CI [{t['ols_slope_ci95'][0]:+.4f}, {t['ols_slope_ci95'][1]:+.4f}]; "
            f"isotonic SSE {t['sse_chosen']:.2e} vs opposite {t['sse_opposite']:.2e}",
            f"- endpoint p=0.5 − p=0: {e['endpoint_diff']:+.4f} "
            f"[{e['ci95'][0]:+.4f}, {e['ci95'][1]:+.4f}]; "
            + (
                f"{e['diff_over_floor_se']:.2f}× the floor-basis SE ({e['floor_note']})"
                if "diff_over_floor_se" in e
                else e["floor_note"]
            ),
            f"- knee κ = {k['kappa']}, 95 % CI [{k['ci95'][0]}, {k['ci95'][1]}], "
            f"bootstrap freq {k['boot_freq']} {k['flag']}",
            f"- confound (both sweeps, y = γ0 + γ_p·p + γ_n·n): γ_p "
            f"{c['gamma_p']:+.4f} [{c['gamma_p_ci95'][0]:+.4f}, "
            f"{c['gamma_p_ci95'][1]:+.4f}], γ_n {c['gamma_n']:+.4f} "
            f"[{c['gamma_n_ci95'][0]:+.4f}, {c['gamma_n_ci95'][1]:+.4f}]. "
            f"**Bound:** the no-element confound's share of the sweep's endpoint "
            f"change is {c['bound_confound_share_of_sweep_change']:+.4f} "
            f"[{c['bound_ci95'][0]:+.4f}, {c['bound_ci95'][1]:+.4f}]",
            "- linearity check, arm mean − plane (in SE units): "
            + ", ".join(
                f"{x['arm'].replace('sweep_', '').replace('ident_', '')} "
                f"{x['resid_over_se']:+.1f}"
                for x in c["arm_means_vs_plane"]
            ),
            "",
        ]
    md = res["mediation"]
    L += [
        "## Mediation — realized training dose (co_active_per_step, updates 1…1000)",
        "",
        f"first stage slope {md['first_stage_slope']:+.4f} per unit p, 95 % CI "
        f"[{md['first_stage_ci95'][0]:+.4f}, {md['first_stage_ci95'][1]:+.4f}] → "
        f"**{md['verdict']}**",
        "",
    ]
    if md["figure_table"]:
        L += [
            "| arm | p | realized dose | completion | survival |",
            "|---|---|---|---|---|",
        ]
        for row in md["figure_table"]:
            L.append(
                f"| {row['arm']} | {row['p']} | {row['realized_dose_mean']:.4f} "
                f"(sd {row['realized_dose_sd']:.4f}) | {row['completion_mean']:.4f} | "
                f"{row['survival_rate_mean']:.4f} |"
            )
        L.append("")
    if res.get("replicate"):
        L += [
            "## Same-card replicate of the inert-share check (S5)",
            "",
            "| metric | Γ₄' = JOINT − sweep_p000 (z_α) | sweep_p000 − ISO-4 (95 %) |",
            "|---|---|---|",
        ]
        for m in FAMILY:
            g, r = (
                res["replicate"][m]["gamma4_prime"],
                res["replicate"][m]["replicate_diff"],
            )
            L.append(
                f"| {m} | {g['gamma']:+.4f} (z {g['z']:+.2f}, "
                f"{'REJECT' if g['reject'] else 'null'}; Šidák CI "
                f"[{g['ci_sidak'][0]:+.4f}, {g['ci_sidak'][1]:+.4f}]) | "
                f"{r['gamma']:+.4f} [{r['ci95'][0]:+.4f}, {r['ci95'][1]:+.4f}] |"
            )
        L += [
            "",
            "Reported BESIDE the registered Γ₄; it cannot change the registered "
            "inert-share qualifier. A disagreement is reported, not resolved.",
            "",
        ]
    L += [
        "## What this instrument is blind to",
        "",
        "- Linearity in (p, n) is an assumption; the arm-mean residuals above test "
        "it only coarsely (8 points, 3 parameters).",
        "- Per-element marginal, co-occurrence and active-episode share cannot all "
        "be held fixed (the simplex); γ_p moves single-element mass into "
        "both-element episodes, which also raises per-element exposure.",
        "- Floors exist only for sweep p = 0.5; intermediate points ASSUME it, the "
        "identification arm is UNGRADED.",
        "- Realized dose is endogenous; nothing here is a causal effect of it.",
        "",
    ]
    return "\n".join(L)


# -------------------------------------------------------------------- main


def run(
    out: Path,
    *,
    recard: Path,
    grid: Path,
    floors: Path | None,
    unblind_dir: Path,
    conf: Path | None,
    iso4: Path | None,
    allow_dirty: bool = False,
) -> dict:
    """Every artifact path is REQUIRED (CLI-only defaults), as in
    p6_post_analysis: a test that forgets one fails instead of reading a
    real artifact."""
    marker = unblind_dir / "UNBLIND_LOG.txt"
    if not (marker.is_file() and marker.stat().st_size > 0):
        raise Refusal(
            f"{marker} missing or empty — the secondary stage is post-unblind."
        )
    prov = U.guard_real_artifact(recard, unblind=True, allow_dirty=allow_dirty)
    check_stamps(recard, grid)
    arms = {a: load_arm(recard, grid, a) for a, _, _ in ARMS}
    fl = json.loads(floors.read_text()) if floors else {}
    res: dict = {
        "provenance": prov,
        "timestamp": _dt.datetime.now(_dt.UTC).isoformat(timespec="seconds"),
        "design": [
            {"arm": a, "m": m, "p": p, "n": no_element(m, p)} for a, m, p in ARMS
        ],
        "metrics": {
            m: analyse_metric(arms, m, fl.get("sweep_p500", {}).get(m, {}).get("sd"))
            for m in FAMILY
        },
        "mediation": mediation(arms),
    }
    if conf is not None and iso4 is not None:
        res["replicate"] = replicate(arms, conf, iso4)
    out.mkdir(parents=True, exist_ok=True)
    (out / "secondary.json").write_text(json.dumps(res, indent=1) + "\n")
    report = render(res)
    (out / "secondary.md").write_text(report)
    if prov["real_artifact"]:
        with (out / "SECONDARY_LOG.txt").open("a") as f:
            f.write(
                f"{res['timestamp']}  git {prov['git_commit']}  "
                f"dirty={prov['git_dirty_files']}\n"
            )
    print(report)
    return res


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--out", type=Path, default=P6 / "secondary")
    ap.add_argument("--recard", type=Path, default=P6 / "g1_sec_s1_12_5090")
    ap.add_argument("--grid", type=Path, default=P6 / "g1_grid")
    ap.add_argument("--floors", type=Path, default=P6 / "g1_floors_5090/floors.json")
    ap.add_argument("--unblind-dir", type=Path, default=P6 / "unblind")
    ap.add_argument("--conf", type=Path, default=P6 / "g1_conf_5090")
    ap.add_argument("--iso4", type=Path, default=P6 / "g1_iso4_5090")
    ap.add_argument("--allow-dirty", action="store_true")
    a = ap.parse_args(argv)
    run(
        a.out,
        recard=a.recard,
        grid=a.grid,
        floors=a.floors,
        unblind_dir=a.unblind_dir,
        conf=a.conf,
        iso4=a.iso4,
        allow_dirty=a.allow_dirty,
    )


if __name__ == "__main__":
    main()
