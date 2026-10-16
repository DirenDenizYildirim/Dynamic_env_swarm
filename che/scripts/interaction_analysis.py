"""INTERACTION CHECK AT θ* — the analysis (POST HOC, out of every registered family).

Implements `che/bench/results/phase6/post_v3_interaction/PLAN.md`, which was
written and committed before any eval ran. Authorized by the decision log's
PAPER V3 item 2(a); scope θ* only (PAPER V3 PHASE 1 START item 2).

Per policy and co-primary (completion, survival rate):

    I = J(both) − J(a_only) − J(b_only) + J(neither)

Per arm (ISO 72, JOINT 72, ISO-4 20) and pooled (stratified by arm, weights
k_a / 164): the mean, its SE from the artifact's own seed dispersion, and a
Šidák interval over the family of 4 estimates × 2 co-primaries = 8 (PLAN §5).
Main effects A and B are descriptive, with no reading rule (PLAN §4). The eval
self-floor and the cross-card check are PLAN §6; the reading rules are PLAN §7.

It REFUSES (exit 2) unless:
  - PLAN.md is tracked by git and unchanged since its last commit;
  - every `plan_sha256:` line in the run's provenance.txt equals the hash of
    that committed plan, and the run's first `date_utc` is not earlier than
    the plan's commit time (the plan predates the run);
  - SHA256_RESULTS.txt, when present, verifies the returned results archive;
  - every planned eval and floor JSON is present, at step T* = 1000, on the
    common draw (seed 0, 512 episodes), under its condition's config (no
    partial family is ever reported);
  - the git tree is clean (or --allow-dirty, which is recorded).

Every real invocation appends a line to `<out>/ANALYSIS_LOG.txt`, so a second
look is a recorded second look.

Usage, after the box's results are copied back, hash-checked and committed:
    uv run python -m che.scripts.interaction_analysis
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import math
import statistics
import subprocess
from pathlib import Path
from statistics import NormalDist

import numpy as np

from che.scripts.m62_report import METRICS, T_STAR, _sidak_z
from che.scripts.make_interaction_configs import CONDITIONS, config_path
from che.scripts.p6_unblind import EVAL_SEED, FAMILY, N_EVAL, Refusal

N = NormalDist()

# ------------------------------------------------------------------ design
# Every value mirrors PLAN.md; test_interaction_check.py asserts the mirror.
ARMS = (("iso", 72), ("joint", 72), ("iso4", 20))
K_TOTAL = sum(k for _, k in ARMS)  # 164
CONDS = tuple(CONDITIONS)  # neither, a_only, b_only, both
ESTIMATES = ("iso", "joint", "iso4", "pooled")
M_FAMILY = len(ESTIMATES) * len(FAMILY)  # 8 (PLAN §5)
Z_ALPHA = _sidak_z(M_FAMILY)  # ≈ 2.73
Z_POWER = N.inv_cdf(0.80)
FLOOR_TAGS = ("iso_s1", "joint_s1", "iso4_s1")
FLOOR_REPS = 3  # extra copies per (tag, condition); the main eval is copy 0
N_AGENTS = 12  # θ*'s env.n_agents, for survival in agents per episode
P6 = Path("che/bench/results/phase6")
OUT = P6 / "post_v3_interaction"
GRID_EVAL_DIRS = {
    "iso": P6 / "g1_conf_5090",
    "joint": P6 / "g1_conf_5090",
    "iso4": P6 / "g1_iso4_5090",
}
GRID_EVAL_CONFIG = "che/configs/theta_star_holdout.yaml"


def _tags(arm: str, k: int) -> list[str]:
    return [f"{arm}_s{s}" for s in range(1, k + 1)]


# ------------------------------------------------------------------ guards


def _git(cwd: Path, *args: str) -> str:
    r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        raise Refusal(f"git {' '.join(args)} failed in {cwd}: {r.stderr.strip()}")
    return r.stdout.strip()


def _sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def plan_guard(plan: Path) -> dict:
    """The plan must be committed and unchanged since (PLAN preamble)."""
    if not plan.is_file() or plan.stat().st_size == 0:
        raise Refusal(f"{plan} missing or empty — the plan comes before the run.")
    cwd = plan.parent
    try:
        _git(cwd, "ls-files", "--error-unmatch", plan.name)
    except Refusal:
        raise Refusal(
            f"{plan} is not committed — commit the plan before any analysis."
        ) from None
    if _git(cwd, "status", "--porcelain", "--", plan.name):
        raise Refusal(
            f"{plan} has uncommitted changes — the plan is frozen at its commit."
        )
    commit, when = _git(cwd, "log", "-1", "--format=%H %cI", "--", plan.name).split()
    return {
        "plan_commit": commit,
        "plan_committed_at": when,
        "plan_sha256": _sha256(plan),
    }


def provenance_guard(out: Path, plan_info: dict) -> dict:
    """The run recorded the committed plan's hash and ran after its commit."""
    prov = out / "provenance.txt"
    if not prov.is_file():
        raise Refusal(f"{prov} missing — no record of the run.")
    lines = prov.read_text().splitlines()
    hashes = [
        ln.split(":", 1)[1].strip() for ln in lines if ln.startswith("plan_sha256:")
    ]
    dates = [ln.split(":", 1)[1].strip() for ln in lines if ln.startswith("date_utc:")]
    if not hashes or not dates:
        raise Refusal(f"{prov}: no plan_sha256 / date_utc recorded.")
    if set(hashes) != {plan_info["plan_sha256"]}:
        raise Refusal(
            f"{prov}: the run recorded plan hash(es) {sorted(set(hashes))}, but the "
            f"committed plan hashes to {plan_info['plan_sha256']}."
        )
    first_run = _dt.datetime.fromisoformat(dates[0].replace("Z", "+00:00"))
    committed = _dt.datetime.fromisoformat(plan_info["plan_committed_at"])
    if first_run < committed:
        raise Refusal(
            f"{prov}: the run started {dates[0]}, before the plan was committed "
            f"({plan_info['plan_committed_at']})."
        )
    res = out / "SHA256_RESULTS.txt"
    archive_ok = None
    if res.is_file():
        want, name = res.read_text().split()[:2]
        arc = out / name
        if not arc.is_file() or _sha256(arc) != want:
            raise Refusal(f"{arc} does not verify against {res}.")
        archive_ok = True
    return {
        "run_started": dates[0],
        "run_invocations": len(dates),
        "results_archive_verified": archive_ok,
    }


def tree_guard(repo: Path, allow_dirty: bool) -> dict:
    head = _git(repo, "rev-parse", "HEAD")
    dirty = _git(repo, "status", "--porcelain")
    if dirty and not allow_dirty:
        raise Refusal(
            "the git tree is DIRTY; commit the returned results first "
            "(or --allow-dirty, which is recorded)."
        )
    return {
        "git_commit": head,
        "git_dirty_files": len(dirty.splitlines()) if dirty else 0,
    }


# ------------------------------------------------------------------ reading


def read_eval(f: Path, config: str) -> dict:
    """One eval JSON's metric means, with the common-draw guards re-applied."""
    if not f.is_file():
        raise Refusal(f"{f} missing — no partial family is reported (PLAN §7).")
    d = json.loads(f.read_text())
    if d.get("ckpt_step") != T_STAR:
        raise Refusal(f"{f}: ckpt_step {d.get('ckpt_step')} != {T_STAR}.")
    if d.get("n_episodes") != N_EVAL or d.get("seed") != EVAL_SEED:
        raise Refusal(f"{f}: eval draw is not the common set (seed 0, 512).")
    if d.get("config") != config:
        raise Refusal(f"{f}: evaluated under {d.get('config')}, not {config}.")
    return {m: float(d["metrics"][m]["mean"]) for m in METRICS}


def load_main(out: Path) -> dict[str, dict[str, dict[str, dict]]]:
    """arm -> tag -> condition -> metric means."""
    data: dict = {}
    for arm, k in ARMS:
        data[arm] = {
            t: {
                c: read_eval(out / "evals" / f"eval_{t}_{c}.json", config_path(c))
                for c in CONDS
            }
            for t in _tags(arm, k)
        }
    return data


def interaction(j: dict[str, float]) -> float:
    return j["both"] - j["a_only"] - j["b_only"] + j["neither"]


# ------------------------------------------------------------------ stats


def one_sample(xs: list[float]) -> dict:
    k = len(xs)
    if k < 2:
        raise Refusal(f"degenerate arm: k = {k}")
    m, s = statistics.mean(xs), statistics.stdev(xs)
    return {"k": k, "mean": m, "sd": s, "se": s / math.sqrt(k)}


def pooled(per_arm: dict[str, dict]) -> dict:
    """Stratified by arm, weights k_a / K (PLAN §5)."""
    K = sum(per_arm[a]["k"] for a in per_arm)
    m = sum(per_arm[a]["k"] / K * per_arm[a]["mean"] for a in per_arm)
    se = math.sqrt(
        sum(
            (per_arm[a]["k"] / K) ** 2 * per_arm[a]["sd"] ** 2 / per_arm[a]["k"]
            for a in per_arm
        )
    )
    return {"k": K, "mean": m, "sd": float("nan"), "se": se}


def grade(est: dict, floor_sd: float) -> dict:
    """Šidák interval, observed-SE MDE80 and the PLAN §7 reading."""
    m, se = est["mean"], est["se"]
    lo, hi = m - Z_ALPHA * se, m + Z_ALPHA * se
    excludes0 = lo > 0 or hi < 0
    hurdle = floor_sd == 0.0 or abs(m) > 2.0 * floor_sd
    out = dict(est)
    out.update(
        {
            "z": m / se if se > 0 else (math.copysign(math.inf, m) if m else 0.0),
            "ci_sidak": [lo, hi],
            "mde80_observed_se": (Z_ALPHA + Z_POWER) * se,
            "exclusion_bound": max(abs(lo), abs(hi)),
            "floor_hurdle_met": hurdle,
        }
    )
    if excludes0 and hurdle:
        out["reading"] = "DETECTABLE INTERACTION"
        out["sign"] = "+" if m > 0 else "-"
    else:
        out["reading"] = "NO DETECTABLE INTERACTION"
        out["sign"] = None
    return out


def describe(est: dict) -> dict:
    """Descriptive interval for a main effect: same form, no reading rule."""
    out = dict(est)
    out["ci_sidak"] = [
        est["mean"] - Z_ALPHA * est["se"],
        est["mean"] + Z_ALPHA * est["se"],
    ]
    return out


# ------------------------------------------------------------------ floor


def _npz_metric(f: Path, metric: str) -> np.ndarray:
    if not f.is_file():
        raise Refusal(f"{f} missing — the floor block is required (PLAN §6).")
    with np.load(f) as z:
        return np.asarray(z[metric])


def sec_floor(out: Path) -> dict:
    """A-vs-A copies per (tag, condition): bitwise identity, sd, sd of I."""
    rows, worst = [], {m: 0.0 for m in FAMILY}
    for tag in FLOOR_TAGS:
        copies = {c: [out / "evals" / f"eval_{tag}_{c}"] for c in CONDS}
        for c in CONDS:
            copies[c] += [
                out / "floor" / f"floor_{tag}_{c}_rep{r}"
                for r in range(1, FLOOR_REPS + 1)
            ]
            for p in copies[c]:
                read_eval(p.with_suffix(".json"), config_path(c))
        for m in FAMILY:
            ident, sds = {}, {}
            for c in CONDS:
                arrs = [_npz_metric(p.with_suffix(".npz"), m) for p in copies[c]]
                ident[c] = all(np.array_equal(arrs[0], a) for a in arrs[1:])
                sds[c] = float(np.std([a.mean() for a in arrs], ddof=1))
            i_copies = [
                interaction(
                    {
                        c: float(
                            _npz_metric(copies[c][r].with_suffix(".npz"), m).mean()
                        )
                        for c in CONDS
                    }
                )
                for r in range(FLOOR_REPS + 1)
            ]
            sd_i = float(np.std(i_copies, ddof=1))
            worst[m] = max(worst[m], sd_i)
            rows.append(
                {
                    "tag": tag,
                    "metric": m,
                    "identical": ident,
                    "copy_sd": sds,
                    "sd_I": sd_i,
                }
            )
    deterministic = all(all(r["identical"].values()) for r in rows)
    return {"rows": rows, "deterministic": deterministic, "floor_sd_I": worst}


def sec_cross_card(data: dict, grid_dirs: dict[str, Path]) -> dict:
    """'both' evals against the grid's own θ* evals (descriptive, PLAN §6)."""
    n_ident, diffs = 0, []
    for arm, k in ARMS:
        for t in _tags(arm, k):
            g = read_eval(grid_dirs[arm] / f"eval_{t}.json", GRID_EVAL_CONFIG)
            mine = data[arm][t]["both"]
            same = all(g[m] == mine[m] for m in FAMILY)
            n_ident += same
            if not same:
                diffs.append({"tag": t, **{m: mine[m] - g[m] for m in FAMILY}})
    return {"n": K_TOTAL, "n_identical": n_ident, "differences": diffs}


# ------------------------------------------------------------------ analysis


def analyse(out: Path, grid_dirs: dict[str, Path]) -> dict:
    data = load_main(out)
    floor = sec_floor(out)
    cross = sec_cross_card(data, grid_dirs)
    res: dict = {
        "family": {
            "m": M_FAMILY,
            "z_alpha": Z_ALPHA,
            "estimates": list(ESTIMATES),
            "metrics": list(FAMILY),
        },
        "floor": floor,
        "cross_card": cross,
        "interaction": {},
        "main_effects": {},
        "condition_means": {},
        "arm_differences": {},
    }
    for m in FAMILY:
        per_arm = {}
        for arm, k in ARMS:
            per_arm[arm] = one_sample(
                [
                    interaction({c: data[arm][t][c][m] for c in CONDS})
                    for t in _tags(arm, k)
                ]
            )
        ests = dict(per_arm)
        ests["pooled"] = pooled(per_arm)
        res["interaction"][m] = {
            e: grade(ests[e], floor["floor_sd_I"][m]) for e in ESTIMATES
        }
        res["arm_differences"][m] = {  # descriptive only (PLAN §5)
            "joint_minus_iso": per_arm["joint"]["mean"] - per_arm["iso"]["mean"],
            "iso4_minus_iso": per_arm["iso4"]["mean"] - per_arm["iso"]["mean"],
        }
        eff = {}
        for name, cond in (("A", "a_only"), ("B", "b_only")):
            pa = {
                arm: one_sample(
                    [
                        data[arm][t][cond][m] - data[arm][t]["neither"][m]
                        for t in _tags(arm, k)
                    ]
                )
                for arm, k in ARMS
            }
            pa["pooled"] = pooled({a: pa[a] for a, _ in ARMS})
            eff[name] = {e: describe(pa[e]) for e in ESTIMATES}
        res["main_effects"][m] = eff
    for arm, k in ARMS:
        res["condition_means"][arm] = {
            c: {
                mm: statistics.mean(data[arm][t][c][mm] for t in _tags(arm, k))
                for mm in METRICS
            }
            for c in CONDS
        }
    return res


# ------------------------------------------------------------------ report


def _f(x: float, p: int = 4) -> str:
    return f"{x:+.{p}f}" if math.isfinite(x) else "—"


BLIND = (
    "θ* only (nothing about Low or High); fixed policies (not whether training on "
    "co-occurrence teaches anything — that is Γ); the additive scale on bounded "
    "rates; one eval draw (seed 0, 512 episodes); δ = 1.0 throughout (comms denial "
    "interactions not measured); not a cross-arm test; post hoc (PLAN §8)."
)


def render(res: dict) -> str:
    fam = res["family"]
    L = ["# Interaction check at θ* — POST HOC, out of every registered family", ""]
    pv = res["provenance"]
    L += [
        f"git `{pv['git_commit']}` (dirty files: {pv['git_dirty_files']}) · "
        f"plan `{pv['plan_commit']}` (sha256 `{pv['plan_sha256'][:12]}…`, committed "
        f"{pv['plan_committed_at']}) · run started {pv['run_started']} · "
        f"{res['timestamp']}",
        "",
    ]
    L += [
        f"I = J(both) − J(A only) − J(B only) + J(neither), per policy. Šidák over "
        f"{fam['m']} intervals (4 estimates × 2 co-primaries), z_α = "
        f"{fam['z_alpha']:.4f}. Normal intervals on each artifact's own seed "
        "dispersion; pooled is stratified by arm (weights k/164). Every interval "
        "is conditional on the common eval draw.",
        "",
    ]
    L += [
        "## Interaction I",
        "",
        "| metric | estimate | k | Ī | SE | Šidák CI | observed-SE MDE80 | "
        "exclusion bound | reading |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for m in fam["metrics"]:
        for e in fam["estimates"]:
            g = res["interaction"][m][e]
            note = " (smallest k)" if e == "iso4" else ""
            L.append(
                f"| {m} | {e}{note} | {g['k']} | {_f(g['mean'])} | "
                f"{g['se']:.5f} | [{_f(g['ci_sidak'][0])}, {_f(g['ci_sidak'][1])}] "
                f"| {g['mde80_observed_se']:.4f} | {g['exclusion_bound']:.4f} | "
                f"{g['reading']}{' ' + g['sign'] if g['sign'] else ''} |"
            )
    L.append("")
    for e in fam["estimates"]:
        g = res["interaction"]["survival_rate"][e]
        L.append(
            f"- survival, {e}: Ī = {_f(g['mean'] * N_AGENTS, 3)} agents per "
            f"episode (× {N_AGENTS}); exclusion bound "
            f"{g['exclusion_bound'] * N_AGENTS:.3f} agents."
        )
    L += [
        "",
        "Reading rule (PLAN §7): DETECTABLE iff the Šidák CI excludes 0 and the "
        'floor hurdle is met; otherwise an exclusion |I| < bound, never "no '
        'interaction".',
        "",
    ]
    fl = res["floor"]
    L += [
        "## Eval self-floor (A-vs-A on the run card, per condition)",
        "",
        f"deterministic on this card: **{fl['deterministic']}** · floor sd of I: "
        + ", ".join(f"{m} {v:.2e}" for m, v in fl["floor_sd_I"].items()),
        "",
        "| checkpoint | metric | identical (neither/a_only/b_only/both) | sd of I |",
        "|---|---|---|---|",
    ]
    for r in fl["rows"]:
        ident = "/".join(str(r["identical"][c]) for c in CONDS)
        L.append(f"| {r['tag']} | {r['metric']} | {ident} | {r['sd_I']:.2e} |")
    cc = res["cross_card"]
    L += [
        "",
        "## Cross-card check: 'both' against the grid's own θ* evals",
        "",
        f"{cc['n_identical']} of {cc['n']} identical on both co-primaries "
        "(descriptive).",
        "",
    ]
    if cc["differences"]:
        L += ["| tag | Δ completion | Δ survival |", "|---|---|---|"]
        L += [
            f"| {d['tag']} | {_f(d['completion'])} | {_f(d['survival_rate'])} |"
            for d in cc["differences"]
        ]
        L.append("")
    L += [
        "## Main effects (descriptive, no reading rule)",
        "",
        "| metric | effect | estimate | mean | Šidák-width CI |",
        "|---|---|---|---|---|",
    ]
    for m in fam["metrics"]:
        for name in ("A", "B"):
            for e in fam["estimates"]:
                d = res["main_effects"][m][name][e]
                L.append(
                    f"| {m} | {name} | {e} | {_f(d['mean'])} | "
                    f"[{_f(d['ci_sidak'][0])}, {_f(d['ci_sidak'][1])}] |"
                )
    L += [
        "",
        "## Condition means (descriptive)",
        "",
        "| arm | condition | " + " | ".join(METRICS) + " |",
        "|---|---|" + "---|" * len(METRICS),
    ]
    for arm, conds in res["condition_means"].items():
        for c, ms in conds.items():
            L.append(
                f"| {arm} | {c} | "
                + " | ".join(f"{ms[mm]:.4f}" for mm in METRICS)
                + " |"
            )
    L += [
        "",
        "Arm differences in Ī (descriptive, no test): "
        + "; ".join(
            f"{m}: JOINT − ISO {_f(v['joint_minus_iso'])}, ISO-4 − ISO "
            f"{_f(v['iso4_minus_iso'])}"
            for m, v in res["arm_differences"].items()
        ),
        "",
        f"Blind to: {BLIND}",
        "",
    ]
    return "\n".join(L)


def run(
    out: Path,
    plan: Path,
    repo: Path,
    allow_dirty: bool = False,
    log: bool = True,
    grid_dirs: dict[str, Path] | None = None,
) -> dict:
    plan_info = plan_guard(plan)
    prov = provenance_guard(out, plan_info)
    tree = tree_guard(repo, allow_dirty)
    if grid_dirs is None:
        grid_dirs = {a: repo / d for a, d in GRID_EVAL_DIRS.items()}
    res = analyse(out, grid_dirs)
    res["timestamp"] = _dt.datetime.now(_dt.UTC).isoformat(timespec="seconds")
    res["provenance"] = {**plan_info, **prov, **tree, "allow_dirty": allow_dirty}
    res["label"] = (
        "POST HOC; out of every registered family; changes no branch reading."
    )
    (out / "interaction_report.json").write_text(json.dumps(res, indent=1) + "\n")
    (out / "interaction_report.md").write_text(render(res))
    if log:
        with (out / "ANALYSIS_LOG.txt").open("a") as f:
            f.write(
                f"{res['timestamp']}  git {tree['git_commit']}  "
                f"dirty={tree['git_dirty_files']}  plan {plan_info['plan_commit']}\n"
            )
    return res


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path, default=OUT)
    ap.add_argument("--plan", type=Path, default=None)
    ap.add_argument("--allow-dirty", action="store_true")
    a = ap.parse_args(argv)
    repo = Path(__file__).resolve().parents[2]
    out = a.out if a.out.is_absolute() else repo / a.out
    plan = a.plan or out / "PLAN.md"
    try:
        res = run(out, plan, repo, allow_dirty=a.allow_dirty)
    except Refusal as r:
        print(f"REFUSED: {r.msg}")
        raise
    print(render(res))


if __name__ == "__main__":
    main()
