"""P6 UNBLIND — the confirmatory instrument for Γ, built BEFORE the look.

Computes the registered confirmatory contrast from a completed Phase-6
artifact and resolves the outcome branch from the registered table. Every
constant it applies was frozen before the grid ran; the instrument itself was
written, tested on SYNTHETIC artifacts only, and committed before any real
eval JSON was read (frozen-tree clause of the analysis plan,
`phase6_design_v2.md` §7; NO-PEEKING ruling, 2026-08-02).

What it applies, and where each rule was registered:

  FAMILY      {Γ_completion, Γ_survival} at θ*, Šidák m = 2, z_α = 2.2365.
              Final-five ruling 4 (2026-08-02).
  ESTIMAND    Γ = mean_JOINT − mean_ISO at MATCHED BUDGET T* = 1000. Never
              "at convergence". T* ruling (2026-08-11).
  VARIANCE    sd(Γ) = sqrt((s_iso² + s_joint²)/k) from the GRID'S OWN per-arm
              seed dispersion — UNPAIRED (shared seed integers create no
              pairs; pre-rental ratification 2026-08-13) and graded on the
              CONTRAST's SE (amendment 2026-08-03). The floors are NOT the
              test variance (design v2 §7, amended 2026-08-13); they survive
              here only as the beat-reproducibility hurdle.
  INTERVAL    Conditional on the common eval draw (seed 0, 512 episodes):
              training-seed variance only. §4b of the framing registration.
  BRANCHES    A (+,+)  B (null,+ AND falsifier)  C (null,null)  D (− either),
              `phase6_framing_branches.md` §3, ratified 2026-08-13; and
              A_c (+,null), registered pre-unblind 2026-09-26 (ruling ii).
              "+" and "null" mean rejection / non-rejection in the family;
              "−" is read the same way — a REJECTION with negative sign. A
              negative point estimate that does not reject is a null.
  FALSIFIER   Branch B only if |z_c| + z_α < |z_s|. Registered 2026-08-13.
              If it fails: branch C with an asymmetry note, never B.
  EXCLUSION   A null is quoted as an EXCLUSION, never an absence: X = the
              80 %-power MDE at the corrected α on the realized sd(Γ).
  PRIMARY k   72, designated pre-unblind (LADDER BRANCH C ruling, 2026-09-22).
              The registered-ladder analysis at k = 60 = K_LADDER_CAP is a
              PREFIX of the same seeds and is reported beside it with its
              UNDERPOWERED flag and realized power. Nothing is swapped.
  D is NOT a threshold. Branch D's discriminator is Γ(t), which needs the
              retained checkpoints evaluated on a box; this instrument only
              LABELS D and says so.

Interpretations the registered text did not spell out, RULED by the owner
pre-unblind (`docs/decision_log.md`, PRE-UNBLIND RULINGS, 2026-09-26):

  (i)   "−" in the branch table = rejection with negative sign (above).
  (ii)  The cell (completion +, survival null) was not in the registered
        table. It is registered as BRANCH A_c: the founding claim on the
        founding primary (completion), with the survival null quoted as an
        exclusion. No asymmetry claim, so B's falsifier is not applied.
  (iii) The test statistic is the normal z the frozen plan wrote, not a t.
        At k = 72 the t_{142} critical value differs from z_α in the third
        decimal; the difference is stated in the report, not applied.

USAGE on the frozen tree, once, with the owner present:

    uv run python -m che.scripts.p6_unblind \\
        --artifact che/bench/results/phase6/g1_conf_5090 \\
        --floors   che/bench/results/phase6/g1_floors_5090/floors.json \\
        --card-diag che/bench/results/phase6/g1_grid \\
        --out      che/bench/results/phase6/unblind \\
        --unblind

The `--unblind` flag is REQUIRED for any artifact under che/bench/results/;
without it the instrument refuses. It also refuses a dirty git tree there
(`--allow-dirty` exists for the tests, which run on temporary directories and
never need the flag at all). Every real invocation appends to
`<out>/UNBLIND_LOG.txt` with the commit hash and a timestamp: the look is
auditable, and a second look is a recorded second look, not a silent one.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import math
import statistics
import subprocess
import sys
from pathlib import Path
from statistics import NormalDist

from che.scripts.m62_report import (
    K_LADDER_CAP,
    METRICS,
    SIDAK_M,
    T_STAR,
    TARGET_EFFECT,
    _mde80_contrast,
    _power_contrast,
    _sd_contrast,
    _sidak_z,
)

N = NormalDist()

# --------------------------------------------------------------------------
# REGISTERED. Mirrored in docs/locks.yaml under `analysis:` with
# `module: che.scripts.p6_unblind`; test_locks.py asserts agreement.
K_CONFIRMATORY_REALIZED = 72  # LADDER BRANCH C ruling, 2026-09-22
# --------------------------------------------------------------------------

FAMILY = ("completion", "survival_rate")  # the Šidák m = 2 family, in order
SECONDARY = tuple(m for m in METRICS if m not in FAMILY)  # descriptive only
CONF_ARMS = ("iso", "joint")  # Γ = joint − iso
EVAL_CONFIG = "che/configs/theta_star_holdout.yaml"
N_EVAL = 512
EVAL_SEED = 0
CARD_DIAG_SEEDS = tuple(range(1, 13))  # the PRO 6000 seeds superseded by the re-card

REPO_ROOT = Path(__file__).resolve().parents[2]
# Any artifact under here is REAL. Module-level so the tests can point it at a
# temporary directory and exercise the refusal without touching the results.
RESULTS_ROOT = REPO_ROOT / "che" / "bench" / "results"

Z_ALPHA = _sidak_z()  # 2.2365 at m = 2
Z_POWER = N.inv_cdf(0.80)


class Refusal(SystemExit):
    """A structural refusal. Exit code 2 so a wrapper can tell it from a crash."""

    def __init__(self, msg: str):
        super().__init__(2)
        self.msg = msg
        print(f"REFUSED: {msg}", file=sys.stderr)


# ------------------------------------------------------------------ reading


def read_stamp(artifact: Path) -> dict[str, str]:
    """Parse `grid_params.txt`, the parameter-identity stamp the grid wrote."""
    p = artifact / "grid_params.txt"
    if not p.is_file():
        raise Refusal(f"{p} missing — not a grid artifact, or an unstamped one.")
    out: dict[str, str] = {}
    for ln in p.read_text().splitlines():
        if ":" in ln:
            k, v = ln.split(":", 1)
            out[k.strip()] = v.strip()
    return out


def check_stamp(stamp: dict[str, str], k: int) -> None:
    """The artifact must be the registered instrument, not merely a grid."""
    want = {
        "updates": str(T_STAR),
        "n_eval": str(N_EVAL),
        "eval_seed": str(EVAL_SEED),
        "eval_config": EVAL_CONFIG,
        "k_conf": str(k),
    }
    for key, val in want.items():
        got = stamp.get(key)
        if got != val:
            raise Refusal(
                f"stamp {key} = {got!r}, the registered analysis needs {val!r}. "
                "Per-artifact: this instrument grades exactly one design."
            )
    arms = {a.split(":")[0] for a in stamp.get("conf_arms", "").split()}
    if not set(CONF_ARMS) <= arms:
        raise Refusal(f"stamp conf_arms {sorted(arms)} lacks {CONF_ARMS}.")


def load_arm(artifact: Path, arm: str, seeds: range) -> dict[str, list[float]]:
    """Per-seed metric means for one arm, with every per-run guard re-applied.

    The grid asserted `ckpt_step == T*` per run when it wrote these; a reader
    that trusts that is a reader that would also count a stray file. Every
    JSON is re-checked here, and the run must be manifest-complete (an eval
    exists IFF its run finished — the grid's own invariant).
    """
    vals: dict[str, list[float]] = {m: [] for m in METRICS}
    for s in seeds:
        tag = f"{arm}_s{s}"
        f = artifact / f"eval_{tag}.json"
        if not f.is_file():
            raise Refusal(f"{f} missing — arm {arm} is not complete at seed {s}.")
        entry = artifact / ".manifest" / f"{tag}.done"
        if not (entry.is_file() and entry.stat().st_size > 0):
            raise Refusal(f"{tag}: eval exists but no manifest entry — orphaned eval.")
        d = json.loads(f.read_text())
        if d.get("ckpt_step") != T_STAR:
            raise Refusal(f"{tag}: ckpt_step {d.get('ckpt_step')} != T* {T_STAR}.")
        if d.get("n_episodes") != N_EVAL or d.get("seed") != EVAL_SEED:
            raise Refusal(f"{tag}: eval draw is not the common set (seed 0, 512).")
        if d.get("config") != EVAL_CONFIG:
            raise Refusal(f"{tag}: evaluated under {d.get('config')}, not θ*.")
        for m in METRICS:
            vals[m].append(float(d["metrics"][m]["mean"]))
    return vals


# --------------------------------------------------------------- statistics


def contrast(iso: list[float], joint: list[float]) -> dict:
    """One co-primary's registered contrast. Unpaired, combined-variance SE."""
    k = len(iso)
    if k != len(joint) or k < 2:
        raise Refusal(f"unbalanced or degenerate arms: {len(iso)} vs {len(joint)}")
    m_i, m_j = statistics.mean(iso), statistics.mean(joint)
    s_i, s_j = statistics.stdev(iso), statistics.stdev(joint)
    gamma = m_j - m_i
    sd_g = _sd_contrast(s_i, s_j, k)
    z = gamma / sd_g if sd_g > 0 else math.copysign(math.inf, gamma) if gamma else 0.0
    p2 = 2.0 * (1.0 - N.cdf(abs(z))) if math.isfinite(z) else 0.0
    return {
        "k": k,
        "mean_iso": m_i,
        "mean_joint": m_j,
        "sd_iso": s_i,
        "sd_joint": s_j,
        "gamma": gamma,
        "sd_gamma": sd_g,
        "z": z,
        "p_two_sided": p2,
        "z_alpha": Z_ALPHA,
        "reject": bool(abs(z) > Z_ALPHA),
        "sign": "+" if gamma > 0 else "-" if gamma < 0 else "0",
        # Šidák-level interval (the one the decision is read from) and the
        # familiar 95 % one, both CONDITIONAL on the common eval draw.
        "ci_sidak": [gamma - Z_ALPHA * sd_g, gamma + Z_ALPHA * sd_g],
        "ci95": [gamma - 1.959964 * sd_g, gamma + 1.959964 * sd_g],
        # A null is an exclusion: the effect the realized sd(Γ) finds at 80 %.
        "exclusion_mde80": _mde80_contrast(s_i, s_j, k),
        "power_at_target": _power_contrast(TARGET_EFFECT, s_i, s_j, k),
        "target_effect": TARGET_EFFECT,
    }


def resolve_branch(c: dict, s: dict) -> dict:
    """The registered table, applied. Returns the label and the falsifier."""
    zc, zs = abs(c["z"]), abs(s["z"])
    falsifier = {
        "lhs_abs_zc_plus_z_alpha": zc + Z_ALPHA,
        "rhs_abs_zs": zs,
        "passes": bool(zc + Z_ALPHA < zs),
        "rule": "|z_c| + z_alpha < |z_s|  (registered 2026-08-13)",
    }
    neg_c = c["reject"] and c["gamma"] < 0
    neg_s = s["reject"] and s["gamma"] < 0
    if neg_c or neg_s:
        label, why = (
            "D",
            (
                "Γ rejects with NEGATIVE sign on "
                + " and ".join(
                    n for n, f in (("completion", neg_c), ("survival", neg_s)) if f
                )
                + ". Branch D has NO magnitude threshold; Γ(t) is the discriminator "
                "and it is not computed here (needs the retained checkpoints "
                "evaluated)."
            ),
        )
    elif c["reject"] and s["reject"]:
        label, why = "A", "both co-primaries reject with positive sign."
    elif (not c["reject"]) and s["reject"]:
        if falsifier["passes"]:
            label, why = (
                "B",
                (
                    "completion null, survival positive, and the registered "
                    "falsifier PASSES: the completion exclusion is tighter than the "
                    "survival effect in standardized units."
                ),
            )
        else:
            label, why = (
                "C",
                (
                    "ASYMMETRY NOTE: survival rejects, completion does not, but the "
                    "registered falsifier FAILS (|z_c| + z_alpha >= |z_s|). Reported "
                    "as branch C with the asymmetry left open — never as branch B."
                ),
            )
    elif (not c["reject"]) and (not s["reject"]):
        label, why = "C", "neither co-primary rejects. Quote exclusions, not absences."
    else:
        label, why = (
            "A_c",
            (
                "completion rejects POSITIVE, survival null: the founding claim on "
                "the founding primary (ruling ii, 2026-09-26). Claim JOINT > ISO on "
                "task completion at matched compute; quote the survival null as an "
                f"EXCLUSION, no survival gap larger than X = "
                f"{s['exclusion_mde80']:.4f}. No asymmetry claim; branch-A honesty "
                "lines apply."
            ),
        )
    return {"label": label, "why": why, "falsifier": falsifier}


def analyse(artifact: Path, k: int) -> dict:
    """Family contrasts, secondary descriptives and the branch, at one k."""
    seeds = range(1, k + 1)
    arms = {a: load_arm(artifact, a, seeds) for a in CONF_ARMS}
    fam = {m: contrast(arms["iso"][m], arms["joint"][m]) for m in FAMILY}
    sec = {m: contrast(arms["iso"][m], arms["joint"][m]) for m in SECONDARY}
    for v in sec.values():  # descriptive: no decision fields survive
        for key in ("reject", "ci_sidak", "exclusion_mde80", "power_at_target"):
            v.pop(key, None)
    branch = resolve_branch(fam["completion"], fam["survival_rate"])
    return {
        "k": k,
        "family": fam,
        "secondary": sec,
        "branch": branch,
        "per_seed": {a: arms[a] for a in CONF_ARMS},
    }


def beat_reproducibility(full: dict, floors: dict | None) -> dict | None:
    """Seed dispersion against the artifact's own rerun floor, per arm.

    Theory requires seed sd >= rerun sd (σ²_seed-arm = σ²_rerun + σ²_seed);
    a ratio below 1 is estimator noise at n = 8 reps, not a finding. And Γ
    against the FLOOR-based sd(Γ): does the contrast exceed what identical
    reruns alone would produce? Descriptive on both counts — the test
    variance is the seed dispersion, not this.
    """
    if not floors:
        return None
    out: dict = {}
    for m in FAMILY:
        f_i = floors.get("iso", {}).get(m, {}).get("sd")
        f_j = floors.get("joint", {}).get(m, {}).get("sd")
        if f_i is None or f_j is None:
            out[m] = {"graded": False, "why": "no floor for both arms"}
            continue
        c = full["family"][m]
        sd_floor_g = _sd_contrast(f_i, f_j, c["k"])
        out[m] = {
            "graded": True,
            "floor_sd_iso": f_i,
            "floor_sd_joint": f_j,
            "ratio_seed_over_floor_iso": c["sd_iso"] / f_i if f_i else math.inf,
            "ratio_seed_over_floor_joint": c["sd_joint"] / f_j if f_j else math.inf,
            "sd_gamma_floor_basis": sd_floor_g,
            "gamma_over_floor_sd": abs(c["gamma"]) / sd_floor_g
            if sd_floor_g
            else math.inf,
        }
    return out


def card_diagnostic(artifact: Path, other: Path) -> dict:
    """Same seed, same arm, two cards: the PRO 6000 seeds 1–12 that the
    re-card superseded, against their 5090 replacements. PAIRED by seed.
    Descriptive — it grades nothing and carries no floor of its own; it is
    the 'free card-effect diagnostic' the single-card ruling named.
    """
    seeds = range(CARD_DIAG_SEEDS[0], CARD_DIAG_SEEDS[-1] + 1)
    st_o = read_stamp(other)
    if st_o.get("updates") != str(T_STAR) or st_o.get("eval_config") != EVAL_CONFIG:
        raise Refusal(f"{other}: not a T*={T_STAR} θ* artifact; card diagnostic void.")
    here = {a: load_arm(artifact, a, seeds) for a in CONF_ARMS}
    there = {a: load_arm(other, a, seeds) for a in CONF_ARMS}
    out: dict = {"seeds": list(seeds), "note": "paired by seed; this_card − other_card"}
    for m in FAMILY:
        d = {
            a: [h - t for h, t in zip(here[a][m], there[a][m], strict=True)]
            for a in CONF_ARMS
        }
        inter = [dj - di for di, dj in zip(d["iso"], d["joint"], strict=True)]
        n = len(inter)
        out[m] = {
            a: {
                "mean_diff": statistics.mean(d[a]),
                "se": statistics.stdev(d[a]) / math.sqrt(n),
            }
            for a in CONF_ARMS
        }
        out[m]["interaction_joint_minus_iso"] = {
            "mean": statistics.mean(inter),
            "se": statistics.stdev(inter) / math.sqrt(n),
        }
    return out


# ------------------------------------------------------------------ guards


def _git(*args: str) -> str:
    try:
        return subprocess.run(
            ["git", *args], cwd=REPO_ROOT, capture_output=True, text=True, check=True
        ).stdout.strip()
    except Exception:  # noqa: BLE001 — provenance, not control flow
        return "UNKNOWN"


def guard_real_artifact(artifact: Path, unblind: bool, allow_dirty: bool) -> dict:
    """A real artifact needs the flag and a frozen tree. Synthetic ones do not."""
    real = RESULTS_ROOT.resolve() in artifact.resolve().parents
    head = _git("rev-parse", "HEAD")
    dirty = _git("status", "--porcelain")
    if real and not unblind:
        raise Refusal(
            f"{artifact} is a REAL Phase-6 artifact and --unblind was not given. "
            "Unblinding is a human-gated step on a frozen tree."
        )
    if real and dirty and not allow_dirty:
        raise Refusal(
            "the git tree is DIRTY. The analysis plan freezes the pipeline by "
            "commit hash before unblinding; commit first (or --allow-dirty, "
            "which is recorded)."
        )
    return {
        "real_artifact": real,
        "git_commit": head,
        "git_dirty_files": len(dirty.splitlines()) if dirty else 0,
    }


# ------------------------------------------------------------------ report


def _fmt_contrast(name: str, c: dict, decision: bool = True) -> list[str]:
    rows = [
        f"| {name} | {c['mean_iso']:.4f} | {c['mean_joint']:.4f} | {c['sd_iso']:.4f} | "
        f"{c['sd_joint']:.4f} | {c['gamma']:+.4f} | {c['sd_gamma']:.5f} | "
        f"{c['z']:+.2f} |"
    ]
    if decision:
        rows[0] += (
            f" {c['p_two_sided']:.4g} | {'REJECT' if c['reject'] else 'null'} | "
            f"[{c['ci_sidak'][0]:+.4f}, {c['ci_sidak'][1]:+.4f}] | "
            f"{c['exclusion_mde80']:.4f} | {c['power_at_target']:.1%} |"
        )
    return rows


def render_report(res: dict) -> str:
    full, pre = res["primary"], res["prefix"]
    L: list[str] = []
    L += [
        "# Phase-6 UNBLIND — confirmatory contrast Γ at θ*, matched budget "
        f"T* = {T_STAR}",
        "",
        f"artifact: `{res['artifact']}`  ·  git: `{res['provenance']['git_commit']}` "
        f"(dirty files: {res['provenance']['git_dirty_files']})  ·  "
        f"{res['timestamp']}",
        "",
        f"Family {{Γ_completion, Γ_survival}}, Šidák m = {SIDAK_M}, "
        f"z_α = {Z_ALPHA:.4f}. "
        "sd(Γ) is the grid's own UNPAIRED per-arm seed dispersion in the combined "
        "form. Intervals are CONDITIONAL on the common eval draw (seed 0, 512 "
        "episodes) and carry training-seed variance only.",
        "",
    ]
    hdr = (
        "| metric | ISO | JOINT | sd ISO | sd JOINT | Γ | sd(Γ) | z | p | decision "
        "| Šidák CI | exclusion X (MDE80) | power@0.03 |"
    )
    sep = "|---|---|---|---|---|---|---|---|---|---|---|---|---|"
    for title, r, flag in (
        (f"PRIMARY — k = {full['k']} (designated pre-unblind)", full, ""),
        (
            f"REGISTERED-LADDER PREFIX — k = {pre['k']} (seeds 1..{pre['k']})",
            pre,
            " — UNDERPOWERED flag per branch C as written; realized power stated",
        ),
    ):
        L += [f"## {title}{flag}", "", hdr, sep]
        for m in FAMILY:
            L += _fmt_contrast(m, r["family"][m])
        b = r["branch"]
        L += [
            "",
            f"**BRANCH {b['label']}** — {b['why']}",
            f"falsifier: {b['falsifier']['rule']}: "
            f"{b['falsifier']['lhs_abs_zc_plus_z_alpha']:.3f} < "
            f"{b['falsifier']['rhs_abs_zs']:.3f} → "
            f"{'passes' if b['falsifier']['passes'] else 'FAILS'}",
            "",
        ]
    L += [
        "## Secondary metrics — descriptive, NOT in the family, no decision",
        "",
        "| metric | ISO | JOINT | sd ISO | sd JOINT | Γ | sd(Γ) | z |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for m in SECONDARY:
        L += _fmt_contrast(m, full["secondary"][m], decision=False)
    L += [""]
    if res.get("beat_reproducibility"):
        L += [
            "## Beat-reproducibility hurdle — floors are the hurdle, not the test "
            "variance",
            "",
            "| metric | seed sd / floor (ISO) | seed sd / floor (JOINT) "
            "| sd(Γ) floor basis | Γ / floor sd(Γ) |",
            "|---|---|---|---|---|",
        ]
        for m, v in res["beat_reproducibility"].items():
            if v.get("graded"):
                L.append(
                    f"| {m} | {v['ratio_seed_over_floor_iso']:.2f}× | "
                    f"{v['ratio_seed_over_floor_joint']:.2f}× | "
                    f"{v['sd_gamma_floor_basis']:.5f} | "
                    f"{v['gamma_over_floor_sd']:.2f}× |"
                )
            else:
                L.append(f"| {m} | UNGRADED — {v.get('why')} | | | |")
        L += [
            "",
            "A seed/floor ratio below 1 is n = 8 estimator noise, not a finding.",
            "",
        ]
    else:
        L += ["## Beat-reproducibility hurdle — NOT GRADED (no floors supplied)", ""]
    if res.get("card_diagnostic"):
        cd = res["card_diagnostic"]
        L += [
            "## Card diagnostic — seeds 1..12, this card − other card, paired by "
            "seed (descriptive)",
            "",
            "| metric | ISO Δ (se) | JOINT Δ (se) | interaction JOINT−ISO (se) |",
            "|---|---|---|---|",
        ]
        for m in FAMILY:
            v = cd[m]
            L.append(
                f"| {m} | {v['iso']['mean_diff']:+.4f} ({v['iso']['se']:.4f}) | "
                f"{v['joint']['mean_diff']:+.4f} ({v['joint']['se']:.4f}) | "
                f"{v['interaction_joint_minus_iso']['mean']:+.4f} "
                f"({v['interaction_joint_minus_iso']['se']:.4f}) |"
            )
        L += [""]
    k = full["k"]
    t_crit = _t_crit_two_sided(2 * k - 2)
    L += [
        "## What this instrument is blind to (instruments law, 2026-08-10)",
        "",
        "- Arm-SYMMETRIC effects cancel in Γ and are invisible here.",
        "- Eval-set sampling: the interval conditions on one 512-episode draw.",
        "- Convergence: Γ is at matched budget T* = 1000, never at convergence; "
        "Γ(t) over the retained checkpoints is REQUIRED evidence and is a "
        "separate stage.",
        "- Branch D's discriminator (Γ(t)) is not computed here; D is only labelled.",
        f"- The statistic is the registered normal z. The t critical value at "
        f"{2 * k - 2} dof and the same α is {t_crit:.4f} vs z_α {Z_ALPHA:.4f}; "
        "stated, not applied.",
        "",
    ]
    return "\n".join(L)


def _t_crit_two_sided(dof: int) -> float:
    """Two-sided t critical value at the Šidák per-comparison α — for the
    report's honesty line only. Cornish–Fisher expansion of the normal
    quantile, accurate to ~1e-4 at dof > 30; no scipy dependency."""
    z = Z_ALPHA
    g1 = (z**3 + z) / 4
    g2 = (5 * z**5 + 16 * z**3 + 3 * z) / 96
    g3 = (3 * z**7 + 19 * z**5 + 17 * z**3 - 15 * z) / 384
    return z + g1 / dof + g2 / dof**2 + g3 / dof**3


# -------------------------------------------------------------------- main


def run(
    artifact: Path,
    out: Path,
    floors_path: Path | None,
    card_diag: Path | None,
    unblind: bool,
    allow_dirty: bool,
    k: int = K_CONFIRMATORY_REALIZED,
    prefix_k: int = K_LADDER_CAP,
) -> dict:
    prov = guard_real_artifact(artifact, unblind, allow_dirty)
    stamp = read_stamp(artifact)
    check_stamp(stamp, k)
    if prefix_k > k:
        raise Refusal(f"prefix k {prefix_k} exceeds artifact k {k}.")
    floors = json.loads(floors_path.read_text()) if floors_path else None
    res = {
        "artifact": str(artifact),
        "stamp": stamp,
        "provenance": prov,
        "timestamp": _dt.datetime.now(_dt.UTC).isoformat(timespec="seconds"),
        "constants": {
            "T_STAR": T_STAR,
            "SIDAK_M": SIDAK_M,
            "z_alpha": Z_ALPHA,
            "K_CONFIRMATORY_REALIZED": K_CONFIRMATORY_REALIZED,
            "K_LADDER_CAP": K_LADDER_CAP,
            "TARGET_EFFECT": TARGET_EFFECT,
        },
        "primary": analyse(artifact, k),
        "prefix": analyse(artifact, prefix_k),
    }
    res["beat_reproducibility"] = beat_reproducibility(res["primary"], floors)
    if card_diag is not None:
        res["card_diagnostic"] = card_diagnostic(artifact, card_diag)
    out.mkdir(parents=True, exist_ok=True)
    (out / "unblind.json").write_text(json.dumps(res, indent=1) + "\n")
    report = render_report(res)
    (out / "report.md").write_text(report)
    if prov["real_artifact"]:
        with (out / "UNBLIND_LOG.txt").open("a") as f:
            f.write(
                f"{res['timestamp']}  git {prov['git_commit']}  "
                f"dirty={prov['git_dirty_files']}  artifact={artifact}  "
                f"branch={res['primary']['branch']['label']}\n"
            )
    print(report)
    return res


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--artifact", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument(
        "--floors",
        type=Path,
        default=None,
        help="floors.json measured on the SAME card as the artifact",
    )
    ap.add_argument(
        "--card-diag",
        type=Path,
        default=None,
        help="the two-card grid dir holding the superseded seeds 1..12",
    )
    ap.add_argument("--k", type=int, default=K_CONFIRMATORY_REALIZED)
    ap.add_argument("--prefix-k", type=int, default=K_LADDER_CAP)
    ap.add_argument(
        "--unblind",
        action="store_true",
        help="REQUIRED for a real artifact; the look is logged",
    )
    ap.add_argument("--allow-dirty", action="store_true")
    a = ap.parse_args(argv)
    run(
        a.artifact,
        a.out,
        a.floors,
        a.card_diag,
        a.unblind,
        a.allow_dirty,
        k=a.k,
        prefix_k=a.prefix_k,
    )


if __name__ == "__main__":
    main()
