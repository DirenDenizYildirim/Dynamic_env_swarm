"""P6 POST-UNBLIND ANALYSIS — Γ(t), Γ₄/B̂, Γ_H, T = 2000 and the eval floor.

The unblind instrument (`p6_unblind.py`) computes Γ at T* and labels the
branch. Everything registered to be read AFTER that look lives here, and this
module was written, tested on SYNTHETIC artifacts only, and committed BEFORE
the unblind — so none of its reading rules can be chosen with the numbers in
view. It computes no branch and relabels none.

Sections, and where each reading rule was registered:

  EVALFLOOR  CARD RULING amendment (2026-09-22): a cross-card eval floor is
             owed before Γ(t) is read. The same checkpoint evaluated N times
             on the post-unblind card (A-vs-A), and against the grid's own
             eval of it (cross-unit). Descriptive; no threshold.
  GAMMA_T    T* ruling (2026-08-11) item 3: "budget-robust iff the sign of Γ
             is stable over the final half of training. If the sign is still
             moving at T, that instability IS the finding." REQUIRED evidence.
             Refused unless the eval floor is present. Ruling (viii),
             2026-09-26: the T* checkpoints are also re-evaluated on the post
             card, giving a paired cross-card check and a single-card curve —
             both descriptive; the sign rule stays on the grid's own eval.
  GAMMA4     §7 ruling (2026-09-18) proposal 1: Γ₄ = JOINT − ISO-4 and
             B̂ = ISO-4 − ISO, side by side with Γ on every branch; the
             inert-share qualifier rule; no magnitude threshold on B̂.
  HIGH       §7 ruling proposal 3 as replaced: Γ_H at β = 0.70 with the
             asymmetric reading (null → a-fortiori exclusion; positive → NOT
             separable from in-distribution advantage; negative →
             exploratory). Γ_H,4 beside it with no reading rule.
  T2000      §7 ruling proposal 2: DESCRIPTIVE ONLY, UNDERPOWERED. Per-arm
             learning curves with seed spread, Γ(2000) with its CI, and the
             differential training-surface slope against the T = 1000
             reference. Enters no branch decision.

Interpretations the registered text did not spell out, RULED by the owner
pre-unblind (`docs/decision_log.md`, PRE-UNBLIND RULINGS, 2026-09-26):

  (iv)  Γ(t) "sign stable" = the POINT ESTIMATE of Γ(t) has one nonzero sign
        at all 11 retained points t = 500, 550, …, 1000, per co-primary.
        t = 1000 is the grid's own eval, i.e. the primary Γ itself. No CI
        criterion and no fraction threshold.
  (v)   Γ₄ uses JOINT at the realized primary k = 72 against ISO-4 at k = 20,
        SE sqrt(s_J²/72 + s_4²/20). "Rejects" / "CI includes 0" are read at
        the family's Šidák z_α (the ruling's own power calculation used it).
        The cell (Γ null, Γ₄ rejects POSITIVE) is not in the registered rule:
        labelled UNREGISTERED, reported, never framed.
  (vi)  Γ_H "null / positive / negative" is read as in (i): rejection at the
        same z_α, with its sign. A non-rejecting negative estimate is a null.

USAGE on the frozen tree, after `p6_unblind` has logged its look:

    uv run python -m che.scripts.p6_post_analysis --sections gamma4 t2000
    # after the post-unblind box stage has been pulled:
    uv run python -m che.scripts.p6_post_analysis --sections evalfloor gamma_t high

It REFUSES unless `<unblind-dir>/UNBLIND_LOG.txt` exists and is non-empty
(Γ₄, B̂ and Γ(2000) read the confirmatory arms' means, which is unblinding),
refuses a dirty tree for real artifacts, and appends every real invocation to
`<out>/POST_UNBLIND_LOG.txt`.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import math
import statistics
from pathlib import Path

from che.scripts import p6_unblind as U
from che.scripts.m62_report import (
    GAMMA_T_RETENTION,
    K_SECONDARY,
    METRICS,
    SIDAK_M,
    T_STAR,
    TARGET_EFFECT,
    _slope,
)

Refusal = U.Refusal
N = U.N
Z_ALPHA = U.Z_ALPHA
Z_POWER = U.Z_POWER
FAMILY = U.FAMILY

# ------------------------------------------------------------------ design
# Every value below mirrors a registered design or a shell default; the tests
# assert the mirror so a drift fails loudly.
THETA_STAR = U.EVAL_CONFIG
HIGH_CONFIG = "che/configs/joint_high.yaml"  # θ* with β 0.49 → 0.70 (§7 ruling)
K_CONF = U.K_CONFIRMATORY_REALIZED  # 72
K_ISO4 = K_SECONDARY  # 20 (§7 ruling proposal 1)
K_T2000 = 4  # §7 ruling proposal 2
T_2000 = 2000
# Retained checkpoints over the final half: T*/(2·interval) + 1 = 11 points.
_GT_INTERVAL = T_STAR // (2 * (GAMMA_T_RETENTION - 1))
GAMMA_T_STEPS = tuple(range(T_STAR // 2, T_STAR + 1, _GT_INTERVAL))
N_FLOOR_REPS = 8  # g1_floors_5090 same-seed reps per arm
EVALFLOOR_TAGS = ("iso_s1", "joint_s1")  # run_p6_post_unblind_evals.sh default
EVALFLOOR_REPS = 4
# Differential training-surface drift at T = 1000, per 100 updates (review §6
# item 1, cited by the §7 ruling proposal 2 as the reference T = 2000 may be
# compared against). A reference, not a bar.
DRIFT_REF_PER_100 = 0.01209
CURVE_BIN = 100  # learning-curve bin width, updates

SECTIONS = ("evalfloor", "gamma_t", "gamma4", "high", "t2000")
P6 = Path("che/bench/results/phase6")


# ------------------------------------------------------------------ reading


def read_eval(f: Path, step: int, config: str) -> dict[str, float]:
    """One eval JSON's metric means, with the common-draw guards re-applied."""
    if not f.is_file():
        raise Refusal(f"{f} missing.")
    d = json.loads(f.read_text())
    if d.get("ckpt_step") != step:
        raise Refusal(f"{f}: ckpt_step {d.get('ckpt_step')} != {step}.")
    if d.get("n_episodes") != U.N_EVAL or d.get("seed") != U.EVAL_SEED:
        raise Refusal(f"{f}: eval draw is not the common set (seed 0, 512).")
    if d.get("config") != config:
        raise Refusal(f"{f}: evaluated under {d.get('config')}, not {config}.")
    return {m: float(d["metrics"][m]["mean"]) for m in METRICS}


def _collect(rows: list[dict[str, float]]) -> dict[str, list[float]]:
    return {m: [r[m] for r in rows] for m in METRICS}


def load_grid_arm(
    artifact: Path, arm: str, k: int, step: int
) -> dict[str, list[float]]:
    """A grid-produced arm: every eval needs its manifest entry (U.load_arm's
    invariant), at the given step, under θ*."""
    rows = []
    for s in range(1, k + 1):
        tag = f"{arm}_s{s}"
        entry = artifact / ".manifest" / f"{tag}.done"
        if not (entry.is_file() and entry.stat().st_size > 0):
            raise Refusal(f"{artifact}/{tag}: no manifest entry — incomplete run.")
        rows.append(read_eval(artifact / f"eval_{tag}.json", step, THETA_STAR))
    return _collect(rows)


def load_post(
    d: Path, stems: list[str], step: int, config: str
) -> dict[str, list[float]]:
    """Post-unblind evals: written only on success with the step re-asserted
    (`run_p6_post_unblind_evals.sh`), so there is no manifest to check."""
    return _collect([read_eval(d / f"{s}.json", step, config) for s in stems])


def check_block_stamp(artifact: Path, updates: int, k: int, arms: tuple[str, ...]):
    st = U.read_stamp(artifact)
    want = {
        "updates": str(updates),
        "k_conf": str(k),
        "n_eval": str(U.N_EVAL),
        "eval_seed": str(U.EVAL_SEED),
        "eval_config": THETA_STAR,
    }
    for key, val in want.items():
        if st.get(key) != val:
            raise Refusal(f"{artifact}: stamp {key} = {st.get(key)!r}, need {val!r}.")
    have = {a.split(":")[0] for a in st.get("conf_arms", "").split()}
    if not set(arms) <= have:
        raise Refusal(f"{artifact}: stamp conf_arms {sorted(have)} lacks {arms}.")


# --------------------------------------------------------------- statistics


def contrast(a: list[float], b: list[float], *, decision: bool = True) -> dict:
    """Γ = mean(b) − mean(a), unpaired, graded on the CONTRAST's SE
    (amendment 2026-08-03) in its unequal-k form sqrt(s_a²/k_a + s_b²/k_b).
    At k_a = k_b it is exactly `p6_unblind.contrast` (asserted by test)."""
    ka, kb = len(a), len(b)
    if ka < 2 or kb < 2:
        raise Refusal(f"degenerate arm: k = {ka}, {kb}")
    ma, mb = statistics.mean(a), statistics.mean(b)
    sa, sb = statistics.stdev(a), statistics.stdev(b)
    g = mb - ma
    sd = math.sqrt(sa * sa / ka + sb * sb / kb)
    z = g / sd if sd > 0 else (math.copysign(math.inf, g) if g else 0.0)
    out = {
        "k_a": ka,
        "k_b": kb,
        "mean_a": ma,
        "mean_b": mb,
        "sd_a": sa,
        "sd_b": sb,
        "gamma": g,
        "sd_gamma": sd,
        "z": z,
        "sign": "+" if g > 0 else "-" if g < 0 else "0",
        "ci95": [g - 1.959964 * sd, g + 1.959964 * sd],
    }
    if decision:
        out.update(
            {
                "p_two_sided": 2.0 * (1.0 - N.cdf(abs(z))) if math.isfinite(z) else 0.0,
                "z_alpha": Z_ALPHA,
                "reject": bool(abs(z) > Z_ALPHA),
                "ci_sidak": [g - Z_ALPHA * sd, g + Z_ALPHA * sd],
                "exclusion_mde80": (Z_ALPHA + Z_POWER) * sd,
                "power_at_target": N.cdf(TARGET_EFFECT / sd - Z_ALPHA)
                if sd > 0
                else float("nan"),
            }
        )
    return out


def _ci_includes_zero(c: dict) -> bool:
    lo, hi = c["ci_sidak"]
    return lo <= 0.0 <= hi


# ----------------------------------------------------------------- sections


def sec_evalfloor(conf: Path, ef: Path) -> dict:
    """A-vs-A on the post-unblind card, and each rep against the grid's own
    eval of the same checkpoint (cross-unit). Exact float equality is the
    question; magnitudes are reported, no threshold is applied."""
    out: dict = {"tags": {}}
    all_det, all_cross = True, True
    for tag in EVALFLOOR_TAGS:
        stems = [f"evalfloor_{tag}_rep{r}" for r in range(1, EVALFLOOR_REPS + 1)]
        reps = load_post(ef, stems, T_STAR, THETA_STAR)
        grid = read_eval(conf / f"eval_{tag}.json", T_STAR, THETA_STAR)
        per: dict = {}
        for m in FAMILY:
            v = reps[m]
            det = len(set(v)) == 1
            cross = all(x == grid[m] for x in v)
            all_det &= det
            all_cross &= cross
            per[m] = {
                "reps": v,
                "grid_eval": grid[m],
                "reps_identical": det,
                "rep_sd": statistics.stdev(v) if len(v) > 1 else 0.0,
                "cross_unit_identical": cross,
                "cross_unit_diff": statistics.mean(v) - grid[m],
            }
        out["tags"][tag] = per
    out["deterministic_on_post_card"] = all_det
    out["cross_unit_identical"] = all_cross
    return out


def sec_gamma_t(conf: Path, gt: Path, evalfloor: dict | None) -> dict:
    if evalfloor is None:
        raise Refusal(
            "Γ(t) is refused without the eval floor (CARD RULING amendment, "
            "2026-09-22: owed BEFORE Γ(t) is read)."
        )
    seeds = range(1, K_CONF + 1)
    pts: dict = {m: [] for m in FAMILY}
    for t in GAMMA_T_STEPS:
        if t == T_STAR:  # the grid's own eval: the primary Γ itself
            arms = {a: U.load_arm(conf, a, seeds) for a in U.CONF_ARMS}
        else:
            arms = {
                a: load_post(gt, [f"eval_{a}_s{s}_u{t}" for s in seeds], t, THETA_STAR)
                for a in U.CONF_ARMS
            }
        for m in FAMILY:
            c = contrast(arms["iso"][m], arms["joint"][m])
            pts[m].append({"t": t, **c})
    # Ruling (viii): the T* checkpoints re-evaluated on the post card.
    post_t = {
        a: load_post(
            gt, [f"eval_{a}_s{s}_u{T_STAR}" for s in seeds], T_STAR, THETA_STAR
        )
        for a in U.CONF_ARMS
    }
    grid_t = {a: U.load_arm(conf, a, seeds) for a in U.CONF_ARMS}
    cross = _cross_card(post_t, grid_t)
    verdict: dict = {}
    for m in FAMILY:
        single = contrast(post_t["iso"][m], post_t["joint"][m])
        signs_sc = [p["sign"] for p in pts[m][:-1]] + [single["sign"]]
        cross[m]["gamma_post_card_T_star"] = single
        cross[m]["single_card_signs"] = signs_sc
        cross[m]["single_card_stable"] = signs_sc[-1] != "0" and len(set(signs_sc)) == 1
        signs = [p["sign"] for p in pts[m]]
        ref = signs[-1]
        stable = ref != "0" and all(s == ref for s in signs)
        verdict[m] = {
            "signs": signs,
            "sign_at_T_star": ref,
            "stable": stable,
            "t_disagreeing": [p["t"] for p in pts[m] if p["sign"] != ref],
            "n_sidak_ci_excludes_zero": sum(not _ci_includes_zero(p) for p in pts[m]),
            "reading": "BUDGET-ROBUST: the sign of Γ is stable over the final half"
            if stable
            else "UNSTABLE: the sign of Γ is still moving over the final half — "
            "that instability IS the finding (T* ruling item 3)",
        }
    return {
        "steps": list(GAMMA_T_STEPS),
        "points": pts,
        "verdict": verdict,
        "cross_card_T_star": cross,
    }


def _cross_card(post: dict, grid: dict) -> dict:
    """Same checkpoint, post card − grid card, PAIRED by seed. Descriptive:
    it grades nothing (ruling viii). Exact-equality counts first, because two
    deterministic evals of one checkpoint either match bit for bit or not."""
    out: dict = {}
    for m in FAMILY:
        d = {
            a: [x - y for x, y in zip(post[a][m], grid[a][m], strict=True)]
            for a in U.CONF_ARMS
        }
        inter = [dj - di for di, dj in zip(d["iso"], d["joint"], strict=True)]
        n = len(inter)
        out[m] = {
            a: {
                "n_identical": sum(x == 0.0 for x in d[a]),
                "mean_diff": statistics.mean(d[a]),
                "se": statistics.stdev(d[a]) / math.sqrt(n),
                "max_abs_diff": max(abs(x) for x in d[a]),
            }
            for a in U.CONF_ARMS
        }
        out[m]["interaction_joint_minus_iso"] = {
            "mean": statistics.mean(inter),
            "se": statistics.stdev(inter) / math.sqrt(n),
        }
    return out


def _gamma4_reading(g: dict, g4: dict) -> tuple[str, str]:
    """§7 proposal 1's rule, per co-primary. `g` is the registered Γ as the
    unblind instrument recorded it; `g4` is Γ₄."""
    if g["reject"]:
        opposite = g4["sign"] != g["sign"]
        if _ci_includes_zero(g4) or opposite:
            return (
                "DOES_NOT_SURVIVE",
                "Γ rejects but Γ₄'s CI includes 0 or its sign is opposite: the "
                "effect DOES NOT SURVIVE the inert-share correction. Stated in "
                "the abstract-level summary; the branch label does not change; "
                "A/B text may not call it a composition effect without this "
                "qualifier.",
            )
        return ("SURVIVES", "Γ rejects and Γ₄ rejects with the same sign.")
    if not g4["reject"]:
        return (
            "SECOND_EXCLUSION",
            f"Γ and Γ₄ both null: Γ₄ is quoted as a second exclusion bound, "
            f"X₄ = {g4['exclusion_mde80']:.4f}.",
        )
    if g4["gamma"] < 0:
        return (
            "BRANCH_D_SECONDARY",
            "Γ null, Γ₄ rejects NEGATIVE: reported under branch D's framing "
            "(matched-budget asymmetry) as a secondary observation, never as a "
            "confirmatory finding.",
        )
    return (
        "UNREGISTERED",
        "Γ null, Γ₄ rejects POSITIVE: this cell is not in the registered rule. "
        "Reported with no framing; an owner ruling is required.",
    )


def sec_gamma4(conf: Path, iso4: Path, unblind_json: Path) -> dict:
    check_block_stamp(iso4, T_STAR, K_ISO4, ("iso4",))
    if not unblind_json.is_file():
        raise Refusal(f"{unblind_json} missing — Γ₄'s rule reads the recorded Γ.")
    rec = json.loads(unblind_json.read_text())["primary"]
    if rec["k"] != K_CONF:
        raise Refusal(f"recorded primary k {rec['k']} != {K_CONF}.")
    seeds = range(1, K_CONF + 1)
    iso = U.load_arm(conf, "iso", seeds)
    joint = U.load_arm(conf, "joint", seeds)
    i4 = load_grid_arm(iso4, "iso4", K_ISO4, T_STAR)
    out: dict = {"per_metric": {}}
    for m in FAMILY:
        g_rec = rec["family"][m]
        g = contrast(iso[m], joint[m])
        if abs(g["gamma"] - g_rec["gamma"]) > 1e-12:
            raise Refusal(
                f"{m}: Γ recomputed {g['gamma']!r} != recorded {g_rec['gamma']!r} — "
                "the artifact changed since the unblind look."
            )
        g4 = contrast(i4[m], joint[m])
        bhat = contrast(iso[m], i4[m])  # ISO-4 − ISO
        label, why = _gamma4_reading(g_rec, g4)
        out["per_metric"][m] = {
            "gamma": g,
            "gamma4": g4,
            "b_hat": bhat,
            "label": label,
            "why": why,
        }
    return out


def _high_reading(c: dict) -> tuple[str, str]:
    if not c["reject"]:
        return (
            "EXCLUSION",
            f"a-fortiori EXCLUSION: no gap larger than X = "
            f"{c['exclusion_mde80']:.4f} at High even where JOINT trained on the "
            "evaluated configuration and ISO never saw a composed one. Never an "
            "absence.",
        )
    if c["gamma"] > 0:
        return (
            "IN_DISTRIBUTION",
            "Γ_H positive: NOT separable from in-distribution advantage. May not "
            "be cited as compositional generalization on any branch, nor used to "
            "soften a θ* null.",
        )
    return (
        "EXPLORATORY_NEGATIVE",
        "Γ_H negative: exploratory, reported under branch D's matched-budget-"
        "asymmetry framing, never as a finding.",
    )


def sec_high(high: Path) -> dict:
    s72 = range(1, K_CONF + 1)
    step = T_STAR
    iso = load_post(high, [f"evalhigh_iso_s{s}" for s in s72], step, HIGH_CONFIG)
    joint = load_post(high, [f"evalhigh_joint_s{s}" for s in s72], step, HIGH_CONFIG)
    i4 = load_post(
        high, [f"evalhigh_iso4_s{s}" for s in range(1, K_ISO4 + 1)], step, HIGH_CONFIG
    )
    reps = {
        a: load_post(
            high,
            [f"evalhigh_{a}_rep{r}" for r in range(1, N_FLOOR_REPS + 1)],
            step,
            HIGH_CONFIG,
        )
        for a in U.CONF_ARMS
    }
    out: dict = {"per_metric": {}}
    for m in FAMILY:
        c = contrast(iso[m], joint[m])
        c4 = contrast(i4[m], joint[m])
        label, why = _high_reading(c)
        f_i, f_j = statistics.stdev(reps["iso"][m]), statistics.stdev(reps["joint"][m])
        sd_floor = math.sqrt((f_i * f_i + f_j * f_j) / K_CONF)
        out["per_metric"][m] = {
            "gamma_H": c,
            "gamma_H4": {**c4, "reading_rule": "none registered — reported beside"},
            "label": label,
            "why": why,
            "floor": {
                "floor_sd_iso": f_i,
                "floor_sd_joint": f_j,
                "ratio_seed_over_floor_iso": c["sd_a"] / f_i if f_i else math.inf,
                "ratio_seed_over_floor_joint": c["sd_b"] / f_j if f_j else math.inf,
                "sd_gamma_floor_basis": sd_floor,
                "gamma_over_floor_sd": abs(c["gamma"]) / sd_floor
                if sd_floor
                else math.inf,
                "iso4": "UNDERPOWERED for the beat-reproducibility hurdle "
                "(no rep set); graded on seed dispersion only",
            },
        }
    return out


def _curve(log: Path, metric: str) -> dict[int, float]:
    """Per-bin mean of a training-log metric, NaN/None rows skipped (completion
    is logged only on updates that finished an episode)."""
    bins: dict[int, list[float]] = {}
    for ln in log.read_text().splitlines():
        if not ln.strip():
            continue
        r = json.loads(ln)
        y = r.get(metric)
        if y is None or (isinstance(y, float) and math.isnan(y)):
            continue
        b = math.ceil(int(r["update"]) / CURVE_BIN) * CURVE_BIN
        bins.setdefault(b, []).append(float(y))
    return {b: statistics.mean(v) for b, v in sorted(bins.items()) if b > 0}


def _points(log: Path, metric: str, lo: int, hi: int) -> list[tuple[int, float]]:
    pts = []
    for ln in log.read_text().splitlines():
        if not ln.strip():
            continue
        r = json.loads(ln)
        u, y = int(r["update"]), r.get(metric)
        if (
            lo < u <= hi
            and y is not None
            and not (isinstance(y, float) and math.isnan(y))
        ):
            pts.append((u, float(y)))
    return pts


def sec_t2000(t2000: Path) -> dict:
    arms = ("iso_t2000", "joint_t2000")
    check_block_stamp(t2000, T_2000, K_T2000, arms)
    ev = {a: load_grid_arm(t2000, a, K_T2000, T_2000) for a in arms}
    out: dict = {
        "flag": "DESCRIPTIVE ONLY — UNDERPOWERED (§7 ruling proposal 2); "
        "graded by no test; enters no branch decision",
        "gamma_2000": {
            m: contrast(ev["iso_t2000"][m], ev["joint_t2000"][m], decision=False)
            for m in FAMILY
        },
        "curves": {},
        "differential_slope_per_100": {},
        "drift_reference_per_100": DRIFT_REF_PER_100,
    }
    for m in FAMILY:
        per_arm: dict = {}
        for a in arms:
            curves = [
                _curve(t2000 / f"{a}_s{s}.jsonl", m) for s in range(1, K_T2000 + 1)
            ]
            bins = sorted(set().union(*curves))
            per_arm[a] = {
                b: {
                    "mean": statistics.mean(c[b] for c in curves),
                    "sd": statistics.stdev(c[b] for c in curves),
                }
                for b in bins
                if all(b in c for c in curves)
            }
        out["curves"][m] = per_arm
        slopes: dict = {}
        for lo, hi in ((T_STAR // 2, T_STAR), (T_STAR, T_2000)):
            s = {
                a: statistics.mean(
                    _slope(_points(t2000 / f"{a}_s{s_}.jsonl", m, lo, hi))
                    for s_ in range(1, K_T2000 + 1)
                )
                for a in arms
            }
            slopes[f"({lo},{hi}]"] = 100.0 * (s["joint_t2000"] - s["iso_t2000"])
        out["differential_slope_per_100"][m] = slopes
    return out


# ------------------------------------------------------------------ report


def _f(x: float, p: int = 4) -> str:
    return f"{x:+.{p}f}"


def _row(name: str, c: dict) -> str:
    s = (
        f"| {name} | {c['mean_a']:.4f} (k={c['k_a']}) | {c['mean_b']:.4f} "
        f"(k={c['k_b']}) | {_f(c['gamma'])} | {c['sd_gamma']:.5f} | {c['z']:+.2f} |"
    )
    if "reject" in c:
        s += (
            f" {'REJECT' if c['reject'] else 'null'} | "
            f"[{_f(c['ci_sidak'][0])}, {_f(c['ci_sidak'][1])}] | "
            f"{c['exclusion_mde80']:.4f} |"
        )
    else:
        s += f" [{_f(c['ci95'][0])}, {_f(c['ci95'][1])}] (95 %, descriptive) |"
    return s


_HDR = (
    "| contrast | a | b | Γ = b − a | sd(Γ) | z | decision | Šidák CI | X (MDE80) |\n"
    "|---|---|---|---|---|---|---|---|---|"
)


def render(res: dict) -> str:
    L = [
        "# Phase-6 POST-UNBLIND analysis",
        "",
        f"git `{res['provenance']['git_commit']}` (dirty files: "
        f"{res['provenance']['git_dirty_files']}) · {res['timestamp']} · "
        f"sections: {', '.join(res['sections'])}",
        "",
        f"Šidák m = {SIDAK_M}, z_α = {Z_ALPHA:.4f}, as the family. Every interval "
        "is CONDITIONAL on its common eval draw (seed 0, 512 episodes). Nothing "
        "here decides or relabels a branch.",
        "",
    ]
    if "evalfloor" in res:
        e = res["evalfloor"]
        L += [
            "## Eval floor — A-vs-A on the post-unblind card, and cross-unit",
            "",
            f"deterministic on this card: **{e['deterministic_on_post_card']}** · "
            f"identical to the grid's own eval: **{e['cross_unit_identical']}**",
            "",
            "| checkpoint | metric | reps identical | rep sd | cross-unit identical "
            "| mean(reps) − grid |",
            "|---|---|---|---|---|---|",
        ]
        for tag, per in e["tags"].items():
            for m, v in per.items():
                L.append(
                    f"| {tag} | {m} | {v['reps_identical']} | {v['rep_sd']:.2e} | "
                    f"{v['cross_unit_identical']} | {v['cross_unit_diff']:+.2e} |"
                )
        L += [
            "",
            "Blind to: two checkpoints only; the grid card's own eval self-floor "
            "is unmeasured (that box is gone), so a cross-unit difference cannot "
            "be assigned to either unit.",
            "",
        ]
    if "gamma_t" in res:
        g = res["gamma_t"]
        L += ["## Γ(t) — final half, REQUIRED robustness evidence", ""]
        for m in FAMILY:
            v = g["verdict"][m]
            L += [
                f"### {m}: **{v['reading']}**",
                "",
                "| t | Γ(t) | sd(Γ) | Šidák CI |",
                "|---|---|---|---|",
            ]
            for p in g["points"][m]:
                L.append(
                    f"| {p['t']} | {_f(p['gamma'])} | {p['sd_gamma']:.5f} | "
                    f"[{_f(p['ci_sidak'][0])}, {_f(p['ci_sidak'][1])}] |"
                )
            L += [
                "",
                f"signs {' '.join(v['signs'])}; disagreeing with T*: "
                f"{v['t_disagreeing'] or 'none'}; Šidák CI excludes 0 at "
                f"{v['n_sidak_ci_excludes_zero']}/{len(v['signs'])} points "
                "(descriptive — the rule reads signs only).",
                "",
            ]
        L += [
            "### Cross-card check at T* — post card − grid card, paired by seed "
            "(ruling viii, descriptive)",
            "",
            "| metric | arm | identical | mean Δ (se) | max \\|Δ\\| |",
            "|---|---|---|---|---|",
        ]
        for m in FAMILY:
            cc = g["cross_card_T_star"][m]
            for a in U.CONF_ARMS:
                v = cc[a]
                L.append(
                    f"| {m} | {a} | {v['n_identical']}/{K_CONF} | "
                    f"{v['mean_diff']:+.2e} ({v['se']:.2e}) | "
                    f"{v['max_abs_diff']:.2e} |"
                )
            ix = cc["interaction_joint_minus_iso"]
            L.append(f"| {m} | JOINT − ISO | | {ix['mean']:+.2e} ({ix['se']:.2e}) | |")
        L.append("")
        for m in FAMILY:
            cc = g["cross_card_T_star"][m]
            L.append(
                f"- {m}: single-card curve signs {' '.join(cc['single_card_signs'])}"
                f" → {'stable' if cc['single_card_stable'] else 'NOT stable'} "
                f"(descriptive; the rule above reads the grid's own T* eval). "
                "Γ at T* on the post card: "
                f"{_f(cc['gamma_post_card_T_star']['gamma'])}."
            )
        L += [
            "",
            "Blind to: t < 1000 is evaluated on the post-unblind card, t = 1000 "
            "is the grid's own eval — read with the eval floor and the cross-card "
            "check above.",
            "",
        ]
    if "gamma4" in res:
        L += ["## Γ₄ = JOINT − ISO-4 and B̂ = ISO-4 − ISO (§7 proposal 1)", "", _HDR]
        for m in FAMILY:
            v = res["gamma4"]["per_metric"][m]
            L += [
                _row(f"Γ {m} (ISO→JOINT)", v["gamma"]),
                _row(f"Γ₄ {m} (ISO-4→JOINT)", v["gamma4"]),
                _row(f"B̂ {m} (ISO→ISO-4)", v["b_hat"]),
            ]
        L.append("")
        for m in FAMILY:
            v = res["gamma4"]["per_metric"][m]
            L.append(f"- **{m}: {v['label']}** — {v['why']}")
        L += ["", "No magnitude threshold on B̂ is applied, now or later.", ""]
    if "high" in res:
        L += [
            "## High readout — Γ_H at β = 0.70 (§7 proposal 3, out of family)",
            "",
            _HDR,
        ]
        for m in FAMILY:
            v = res["high"]["per_metric"][m]
            L += [_row(f"Γ_H {m}", v["gamma_H"]), _row(f"Γ_H,4 {m}", v["gamma_H4"])]
        L.append("")
        for m in FAMILY:
            v = res["high"]["per_metric"][m]
            fl = v["floor"]
            L += [
                f"- **{m}: {v['label']}** — {v['why']}",
                f"  floor (8 reps, this card): seed/floor ISO "
                f"{fl['ratio_seed_over_floor_iso']:.2f}×, JOINT "
                f"{fl['ratio_seed_over_floor_joint']:.2f}×; Γ_H / floor sd(Γ) "
                f"{fl['gamma_over_floor_sd']:.2f}×. ISO-4: {fl['iso4']}.",
            ]
        L += [
            "",
            "Blind to: NOT a held-out test (JOINT trained on this configuration at "
            "weight 1/2). Coupling A is marginal at High while B is live — the "
            "mirror of Medium; no severity has both couplings strongly live.",
            "",
        ]
    if "t2000" in res:
        t = res["t2000"]
        L += [
            f"## T = 2000 — {t['flag']}",
            "",
            "| metric | ISO | JOINT | Γ(2000) | sd(Γ) | 95 % CI |",
            "|---|---|---|---|---|---|",
        ]
        for m in FAMILY:
            c = t["gamma_2000"][m]
            L.append(
                f"| {m} | {c['mean_a']:.4f} | {c['mean_b']:.4f} | {_f(c['gamma'])} "
                f"| {c['sd_gamma']:.4f} | [{_f(c['ci95'][0])}, {_f(c['ci95'][1])}] |"
            )
        L += [
            "",
            "Differential training-surface slope JOINT − ISO, per 100 updates "
            f"(reference at T = 1000: {DRIFT_REF_PER_100}):",
            "",
        ]
        for m in FAMILY:
            s = t["differential_slope_per_100"][m]
            L.append(f"- {m}: " + ", ".join(f"{w} {v:+.5f}" for w, v in s.items()))
        L += [
            "",
            "May be cited only for whether the T = 1000 differential drift visibly "
            "persists, closes or reverses — never that Γ 'holds' or 'vanishes' at "
            "T = 2000. Per-arm curves are in the JSON.",
            "",
        ]
    return "\n".join(L)


# -------------------------------------------------------------------- main


def run(
    sections: list[str],
    out: Path,
    *,
    conf: Path,
    unblind_dir: Path,
    iso4: Path,
    t2000: Path,
    post_gamma_t: Path,
    post_high: Path,
    post_evalfloor: Path,
    allow_dirty: bool = False,
) -> dict:
    """Every path is REQUIRED here: only the CLI carries the real defaults, so
    a test that forgets one fails instead of silently reading a real
    artifact (asserted by test)."""
    bad = [s for s in sections if s not in SECTIONS]
    if bad or not sections:
        raise Refusal(f"unknown or empty sections {bad or sections}; one of {SECTIONS}")
    marker = unblind_dir / "UNBLIND_LOG.txt"
    if not (marker.is_file() and marker.stat().st_size > 0):
        raise Refusal(
            f"{marker} missing or empty. This is the POST-unblind stage: Γ₄, B̂ "
            "and Γ(2000) read the confirmatory arms' means."
        )
    prov = U.guard_real_artifact(conf, unblind=True, allow_dirty=allow_dirty)
    res: dict = {
        "sections": [s for s in SECTIONS if s in sections],
        "provenance": prov,
        "timestamp": _dt.datetime.now(_dt.UTC).isoformat(timespec="seconds"),
    }
    ef = None
    if "evalfloor" in sections or "gamma_t" in sections:
        ef = sec_evalfloor(conf, post_evalfloor)
        res["evalfloor"] = ef
    if "gamma_t" in sections:
        res["gamma_t"] = sec_gamma_t(conf, post_gamma_t, ef)
    if "gamma4" in sections:
        res["gamma4"] = sec_gamma4(conf, iso4, unblind_dir / "unblind.json")
    if "high" in sections:
        res["high"] = sec_high(post_high)
    if "t2000" in sections:
        res["t2000"] = sec_t2000(t2000)
    out.mkdir(parents=True, exist_ok=True)
    stem = "post_" + "_".join(res["sections"])
    (out / f"{stem}.json").write_text(json.dumps(res, indent=1) + "\n")
    report = render(res)
    (out / f"{stem}.md").write_text(report)
    if prov["real_artifact"]:
        with (out / "POST_UNBLIND_LOG.txt").open("a") as f:
            f.write(
                f"{res['timestamp']}  git {prov['git_commit']}  "
                f"dirty={prov['git_dirty_files']}  "
                f"sections={','.join(res['sections'])}\n"
            )
    print(report)
    return res


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--sections", nargs="+", default=list(SECTIONS), choices=SECTIONS)
    ap.add_argument("--out", type=Path, default=P6 / "post_unblind_analysis")
    ap.add_argument("--conf", type=Path, default=P6 / "g1_conf_5090")
    ap.add_argument("--unblind-dir", type=Path, default=P6 / "unblind")
    ap.add_argument("--iso4", type=Path, default=P6 / "g1_iso4_5090")
    ap.add_argument("--t2000", type=Path, default=P6 / "g1_t2000_5090")
    ap.add_argument("--post-gamma-t", type=Path, default=P6 / "post_gamma_t")
    ap.add_argument("--post-high", type=Path, default=P6 / "post_high")
    ap.add_argument("--post-evalfloor", type=Path, default=P6 / "post_evalfloor")
    ap.add_argument("--allow-dirty", action="store_true")
    a = ap.parse_args(argv)
    run(
        a.sections,
        a.out,
        conf=a.conf,
        unblind_dir=a.unblind_dir,
        iso4=a.iso4,
        t2000=a.t2000,
        post_gamma_t=a.post_gamma_t,
        post_high=a.post_high,
        post_evalfloor=a.post_evalfloor,
        allow_dirty=a.allow_dirty,
    )


if __name__ == "__main__":
    main()
