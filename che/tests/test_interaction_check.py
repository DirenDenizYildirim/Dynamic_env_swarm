"""The interaction check at θ* (POST HOC, eval-only; PAPER V3 item 2(a)).

Configs: each 2×2 condition is θ* with exactly its κ values replaced, the
links-open condition is θ* with exactly δ set to 0 (PLAN AMENDMENT item 4), and
'both' is θ*'s own file. Run script: refuses without the plan, plans exactly
PLAN.md's 865 evals, declares every cross-config eval, verifies archives, and
asserts its results archive (one real CPU end-to-end run on a tiny
checkpoint). Analysis: refuses an uncommitted or edited plan, a run that did
not record the committed plan, and a partial family; computes I, D, the
stratified pool, the PLAN §7 readings, the disagreement headline, the context
table and the logit block correctly on synthetic artifacts; and its --verify
mode recomputes the committed report without git and catches a changed eval.
"""

from __future__ import annotations

import dataclasses
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest

from che.env.config import load_config
from che.scripts import interaction_analysis as IA
from che.scripts import make_interaction_configs as MIC
from che.scripts.p6_unblind import Refusal

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "che" / "scripts" / "run_interaction_evals.sh"
PLAN = REPO_ROOT / "che/bench/results/phase6/post_v3_interaction/PLAN.md"
THETA_STAR = REPO_ROOT / MIC.THETA_STAR


# ------------------------------------------------------------------ configs


def test_generated_configs_are_current():
    assert MIC.main(["--check"]) == 0


def test_both_is_theta_star_itself():
    assert MIC.config_path("both") == "che/configs/theta_star_holdout.yaml"


KAPPA_CONDITIONS = tuple(c for c in MIC.NEW_CONDITIONS if c in MIC.CONDITIONS)


def test_condition_sets():
    assert KAPPA_CONDITIONS == ("neither", "a_only", "b_only")
    assert MIC.ALL_CONDITIONS == ("neither", "a_only", "b_only", "both", "links_open")
    assert MIC.LINKS_OPEN in MIC.NEW_CONDITIONS


@pytest.mark.parametrize("cond", KAPPA_CONDITIONS)
def test_condition_is_theta_star_with_only_its_kappas_replaced(cond):
    star = load_config(THETA_STAR)
    got = load_config(REPO_ROOT / MIC.config_path(cond))
    a_on, b_on = MIC.CONDITIONS[cond]
    t = star.env.theta
    assert t.kappa_A > 0 and t.kappa_B > 0  # else the check is trivial
    want_theta = dataclasses.replace(
        t, kappa_A=t.kappa_A if a_on else 0.0, kappa_B=t.kappa_B if b_on else 0.0
    )
    want = dataclasses.replace(
        star, env=dataclasses.replace(star.env, theta=want_theta)
    )
    assert got == want
    assert got.env.theta.delta == t.delta == 1.0  # δ stays at θ*'s value
    assert got.env.theta.beta == t.beta == 0.49


def test_links_open_is_theta_star_with_only_delta_zero():
    star = load_config(THETA_STAR)
    got = load_config(REPO_ROOT / MIC.config_path(MIC.LINKS_OPEN))
    t = star.env.theta
    assert t.delta == 1.0  # else "opening the links" is not a change
    want = dataclasses.replace(
        star, env=dataclasses.replace(star.env, theta=dataclasses.replace(t, delta=0.0))
    )
    assert got == want
    assert (got.env.theta.kappa_A, got.env.theta.kappa_B) == (t.kappa_A, t.kappa_B)


def test_condition_kappa_table():
    t = load_config(THETA_STAR).env.theta
    want = {
        "neither": (0.0, 0.0),
        "a_only": (t.kappa_A, 0.0),
        "b_only": (0.0, t.kappa_B),
        "both": (t.kappa_A, t.kappa_B),
    }
    want["links_open"] = (t.kappa_A, t.kappa_B)
    for cond, (ka, kb) in want.items():
        th = load_config(REPO_ROOT / MIC.config_path(cond)).env.theta
        assert (th.kappa_A, th.kappa_B) == (ka, kb), cond
        assert th.delta == (0.0 if cond == MIC.LINKS_OPEN else t.delta), cond


def test_conditions_differ_from_theta_star_text_only_in_header_and_kappa_lines():
    star = THETA_STAR.read_text().splitlines()
    body = star[next(i for i, ln in enumerate(star) if ln.startswith("env:")) :]
    for cond in MIC.NEW_CONDITIONS:
        new = (REPO_ROOT / MIC.config_path(cond)).read_text().splitlines()
        nbody = new[next(i for i, ln in enumerate(new) if ln.startswith("env:")) :]
        assert len(nbody) == len(body)
        diff = [(a, b) for a, b in zip(body, nbody, strict=True) if a != b]
        if cond == MIC.LINKS_OPEN:
            assert len(diff) == 1 and re.match(r"^  delta: 1\.0$", diff[0][0])
            assert re.match(r"^  delta: 0\.0  #", diff[0][1])
        else:
            assert 1 <= len(diff) <= 2
            assert all(re.match(r"^  kappa_(A|B): ", a) for a, _ in diff)


# ------------------------------------------------------------------ run script


def _run(env_extra: dict, cwd: Path = REPO_ROOT) -> subprocess.CompletedProcess:
    skip = ("OUT", "K_", "BLOCKS", "FLOOR_", "CFG_", "PLAN", "T_STAR", "N_EVAL")
    e = {k: v for k, v in os.environ.items() if not k.startswith(skip)}
    e.update({"PY": sys.executable, **env_extra})
    return subprocess.run(
        ["bash", str(SCRIPT)], cwd=cwd, capture_output=True, text=True, env=e
    )


def test_refuses_without_the_plan(tmp_path):
    r = _run({"PLAN_FILE": str(tmp_path / "PLAN.md"), "DRY_RUN": "1"})
    assert r.returncode == 1 and "BEFORE any eval runs" in r.stderr
    (tmp_path / "PLAN.md").write_text("")
    r = _run({"PLAN_FILE": str(tmp_path / "PLAN.md"), "DRY_RUN": "1"})
    assert r.returncode == 1


def test_refuses_a_plan_hash_mismatch():
    r = _run({"PLAN_SHA256": "0" * 64, "DRY_RUN": "1"})
    assert r.returncode == 1 and "PLAN_SHA256" in r.stderr


def _plan_lines(r) -> list[str]:
    return [ln for ln in r.stdout.splitlines() if ln.startswith(("eval_", "floor_"))]


def test_dry_run_plans_exactly_the_plan_md_evals():
    r = _run({"DRY_RUN": "1"})
    assert r.returncode == 0, r.stderr
    assert "planned: 865" in r.stdout
    lines = _plan_lines(r)
    main = [ln for ln in lines if ln.startswith("eval_")]
    floor = [ln for ln in lines if ln.startswith("floor_")]
    assert len(main) == 164 * 5 == 820 and len(floor) == 3 * 5 * 3 == 45
    assert all("step=1000" in ln for ln in lines)
    for cond in MIC.ALL_CONDITIONS:
        mine = [ln for ln in main if ln.split()[0].endswith(f"_{cond}")]
        assert len(mine) == 164
        assert all(f"cfg={MIC.config_path(cond)}" in ln for ln in mine)
    iso4 = [ln for ln in main if ln.startswith("eval_iso4_")]
    assert len(iso4) == 100 and all("g1_iso4_5090/ckpt_iso4_s" in ln for ln in iso4)
    assert all("g1_conf_5090/ckpt_" in ln for ln in main if ln not in iso4)
    assert {ln.split()[0] for ln in floor} == {
        f"floor_{t}_{c}_rep{r}"
        for t in IA.FLOOR_TAGS
        for c in MIC.ALL_CONDITIONS
        for r in range(1, IA.FLOOR_REPS + 1)
    }


def _body(p: Path) -> str:
    return "\n".join(
        ln for ln in p.read_text().splitlines() if not ln.lstrip().startswith("#")
    )


def test_every_eval_is_declared_verified_and_asserted():
    body = _body(SCRIPT)
    assert "--allow-hash" in body and '--step "$T_STAR"' in body
    assert "ckpt_step" in body and "SHA256_CKPT.txt" in body
    assert "sha256sum -c" in body and "SHA256_RESULTS.txt" in body
    for forbidden in ("interaction_analysis", "m62_report", "p6_unblind", "train"):
        assert forbidden not in body.replace("training", "")


def test_script_defaults_mirror_the_analysis_design():
    txt = SCRIPT.read_text()

    def default(name):
        return re.search(rf"^{name}=\$\{{{name}:-([^}}]*)\}}", txt, re.M).group(1)

    arms = dict(IA.ARMS)
    assert int(default("K_CONF")) == arms["iso"] == arms["joint"] == 72
    assert int(default("K_ISO4")) == arms["iso4"] == 20
    assert int(default("T_STAR")) == IA.T_STAR == 1000
    assert int(default("N_EVAL")) == IA.N_EVAL and int(default("EVAL_SEED")) == 0
    assert tuple(default("FLOOR_TAGS").strip('"').split()) == IA.FLOOR_TAGS
    assert int(default("FLOOR_REPS")) == IA.FLOOR_REPS
    assert default("OUT") == str(IA.OUT)
    for cond in MIC.ALL_CONDITIONS:
        assert default(f"CFG_{cond.upper()}") == MIC.config_path(cond)
    assert IA.ALL_CONDS == MIC.ALL_CONDITIONS


def test_analysis_family_mirrors_the_plan():
    assert IA.K_TOTAL == 164 and IA.M_FAMILY == 8 and IA.M_FAMILY_D == 8
    assert IA.Z_ALPHA == pytest.approx(2.7270, abs=1e-3)
    txt = PLAN.read_text()
    assert "≈ 2.73" in txt and "865" in txt
    assert "two separate families" in txt


TINY = """env:
  grid_size: 12
  n_agents: 3
  horizon: 32
  n_food: 6
theta:
  beta: 0.49
  kappa_A: {ka}
  kappa_B: {kb}
  delta: {d}
train:
  n_envs: 2
  rollout_len: 16
  n_minibatches: 2
  n_epochs: 2
  ckpt_interval: 2
"""


@pytest.mark.skipif(shutil.which("zstd") is None, reason="tar --zstd needs zstd")
def test_end_to_end_floor_block_on_cpu(tmp_path):
    """One real run: verify, extract, eval x 5 conditions, archive, assert;
    then a resume that skips everything; then a tampered archive that fails."""
    from che.train.ippo import train

    cfgs = {}
    for cond in MIC.ALL_CONDITIONS:
        a_on, b_on = MIC.CONDITIONS.get(cond, (True, True))
        d = 0.0 if cond == MIC.LINKS_OPEN else 1.0
        p = tmp_path / f"{cond}.yaml"
        p.write_text(
            TINY.format(ka=0.06 if a_on else 0.0, kb=1.0 if b_on else 0.0, d=d)
        )
        cfgs[cond] = str(p)
    conf = tmp_path / "conf"
    conf.mkdir()
    train(load_config(cfgs["both"]), n_updates=2, ckpt_dir=conf / "ckpt_iso_s1", seed=0)
    subprocess.run(
        ["tar", "--zstd", "-cf", "ckpt_iso_s1.tar.zst", "ckpt_iso_s1"],
        cwd=conf,
        check=True,
    )
    shutil.rmtree(conf / "ckpt_iso_s1")
    h = hashlib.sha256((conf / "ckpt_iso_s1.tar.zst").read_bytes()).hexdigest()
    (conf / "SHA256_CKPT.txt").write_text(f"{h}  some/where/ckpt_iso_s1.tar.zst\n")
    out = tmp_path / "out"
    out.mkdir()
    (out / "PLAN.md").write_text("plan\n")
    env = {
        "OUT": str(out),
        "CONF_DIR": str(conf),
        "BLOCKS": "floor",
        "FLOOR_TAGS": "iso_s1",
        "FLOOR_REPS": "1",
        "T_STAR": "2",
        "N_EVAL": "2",
        "SCRATCH": str(tmp_path / "scratch"),
        "GIT_COMMIT": "test",
        **{f"CFG_{c.upper()}": v for c, v in cfgs.items()},
    }
    r = _run(env, cwd=REPO_ROOT)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "done=5 skipped=0 failed=0" in r.stdout and "ARCHIVE OK" in r.stdout
    for c in MIC.ALL_CONDITIONS:
        d = json.loads((out / "floor" / f"floor_iso_s1_{c}_rep1.json").read_text())
        assert d["ckpt_step"] == 2 and d["config"] == cfgs[c]
    sha = hashlib.sha256((out / "PLAN.md").read_bytes()).hexdigest()
    assert f"plan_sha256: {sha}" in (out / "provenance.txt").read_text()
    subprocess.run(["sha256sum", "-c", "SHA256_RESULTS.txt"], cwd=out, check=True)
    listed = subprocess.run(
        ["tar", "--zstd", "-tf", "v3_interaction_results.tar.zst"],
        cwd=out,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.split()
    assert "floor/floor_iso_s1_neither_rep1.npz" in listed
    assert "provenance.txt" in listed and "timings.txt" in listed

    r = _run(env, cwd=REPO_ROOT)  # resume: nothing re-evaluated
    assert r.returncode == 0 and "done=0 skipped=5 failed=0" in r.stdout

    (conf / "SHA256_CKPT.txt").write_text(f"{'0' * 64}  ckpt_iso_s1.tar.zst\n")
    shutil.rmtree(out / "floor")
    r = _run(env, cwd=REPO_ROOT)
    assert r.returncode == 1 and "sha256 mismatch" in r.stderr


# ------------------------------------------------------------------ analysis

CONDS = tuple(MIC.ALL_CONDITIONS)


def _write_eval(path: Path, cfg: str, comp: np.ndarray, surv: np.ndarray):
    path.parent.mkdir(parents=True, exist_ok=True)
    np.savez(path.with_suffix(".npz"), completion=comp, survival_rate=surv)
    metrics = {
        "completion": {"mean": float(comp.mean())},
        "survival_rate": {"mean": float(surv.mean())},
        "episode_return": {"mean": 0.0},
        "deaths_fire": {"mean": 0.0},
    }
    path.with_suffix(".json").write_text(
        json.dumps(
            {
                "ckpt_step": 1000,
                "n_episodes": 512,
                "seed": 0,
                "config": cfg,
                "metrics": metrics,
            }
        )
    )


def _git(cwd, *a):
    subprocess.run(["git", *a], cwd=cwd, check=True, capture_output=True)


def _synthetic(
    tmp: Path, i_true, noise: float = 0.002, floor_jitter=0.0, d_true: float = 0.0
):
    """A temp repo holding a committed plan and a synthetic returned run.

    `i_true` is one planted I for every arm, or a dict arm -> I; `d_true` is
    the planted links-open effect D.
    """
    rng = np.random.default_rng(0)
    repo = tmp / "repo"
    out = repo / "out"
    out.mkdir(parents=True)
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "t@t")
    _git(repo, "config", "user.name", "t")
    (out / "PLAN.md").write_text("the plan\n")
    _git(repo, "add", ".")
    _git(repo, "commit", "-qm", "plan")
    grid = {a: tmp / "grid" / a for a, _ in IA.ARMS}
    effects = {"neither": 0.0, "a_only": -0.02, "b_only": -0.01}
    for arm, k in IA.ARMS:
        i_arm = i_true[arm] if isinstance(i_true, dict) else i_true
        for s in range(1, k + 1):
            tag = f"{arm}_s{s}"
            base = 0.5 + rng.normal(0, 0.01)
            eps = rng.normal(0, noise)
            eps_d = rng.normal(0, noise)
            both = -0.03 + i_arm + eps
            for c in CONDS:
                shift = effects.get(c, both)
                if c == MIC.LINKS_OPEN:
                    shift = both + d_true + eps_d
                v = np.full(512, base + shift, np.float32)
                _write_eval(out / "evals" / f"eval_{tag}_{c}", MIC.config_path(c), v, v)
                if c == "both":
                    _write_eval(grid[arm] / f"eval_{tag}", IA.GRID_EVAL_CONFIG, v, v)
                if tag in IA.FLOOR_TAGS:
                    for r in range(1, IA.FLOOR_REPS + 1):
                        j = v + np.float32(floor_jitter * r * (c == "both"))
                        _write_eval(
                            out / "floor" / f"floor_{tag}_{c}_rep{r}",
                            MIC.config_path(c),
                            j,
                            j,
                        )
    when = (dt.datetime.now(dt.UTC) + dt.timedelta(minutes=1)).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )
    sha = hashlib.sha256((out / "PLAN.md").read_bytes()).hexdigest()
    (out / "provenance.txt").write_text(f"date_utc: {when}\nplan_sha256: {sha}\n")
    gamma = tmp / "unblind.json"
    fam = {
        m: {"k": 72, "gamma": 0.0096, "sd_gamma": 0.0022, "z_alpha": 2.2365}
        for m in IA.FAMILY
    }
    gamma.write_text(json.dumps({"primary": {"family": fam}}))
    grid["gamma_source"] = gamma
    return repo, out, grid


def _refused(fn, needle: str):
    """Refusal is a SystemExit(2); its reason is in `.msg`."""
    with pytest.raises(Refusal) as e:
        fn()
    assert needle in e.value.msg, e.value.msg


def _grid(grid):
    return {a: grid[a] for a, _ in IA.ARMS}


def _analyse(repo, out, grid, **kw):
    return IA.run(
        out,
        out / "PLAN.md",
        repo,
        allow_dirty=True,
        log=False,
        grid_dirs=_grid(grid),
        gamma_source=grid["gamma_source"],
        **kw,
    )


def test_detects_a_planted_negative_interaction(tmp_path):
    repo, out, grid = _synthetic(tmp_path, i_true=-0.02)
    res = _analyse(repo, out, grid)
    for m in IA.FAMILY:
        pool = res["interaction"][m]["pooled"]
        assert pool["reading"] == "DETECTABLE INTERACTION" and pool["sign"] == "-"
        assert pool["mean"] == pytest.approx(-0.02, abs=1e-3)
        arms = {a: res["interaction"][m][a] for a, _ in IA.ARMS}
        want = sum(k / 164 * arms[a]["mean"] for a, k in IA.ARMS)
        assert pool["mean"] == pytest.approx(want)
        ma = res["main_effects"][m]["A"]["pooled"]["mean"]
        assert ma == pytest.approx(-0.02, abs=1e-5)
    assert res["floor"]["deterministic"] and res["cross_card"]["n_identical"] == 164
    assert (out / "interaction_report.md").is_file()
    assert "POST HOC" in (out / "interaction_report.md").read_text()


def test_null_is_an_exclusion_with_its_bound(tmp_path):
    repo, out, grid = _synthetic(tmp_path, i_true=0.0)
    res = _analyse(repo, out, grid)
    g = res["interaction"]["survival_rate"]["pooled"]
    assert g["reading"] == "NO DETECTABLE INTERACTION" and g["sign"] is None
    lo, hi = g["ci_sidak"]
    assert g["exclusion_bound"] == pytest.approx(max(abs(lo), abs(hi)))
    assert g["mde80_observed_se"] == pytest.approx((IA.Z_ALPHA + IA.Z_POWER) * g["se"])


def test_nonzero_floor_raises_the_hurdle(tmp_path):
    repo, out, grid = _synthetic(
        tmp_path, i_true=-0.004, noise=0.0005, floor_jitter=0.01
    )
    res = _analyse(repo, out, grid)
    assert not res["floor"]["deterministic"]
    g = res["interaction"]["completion"]["pooled"]
    lo, hi = g["ci_sidak"]
    assert hi < 0  # the interval alone would reject ...
    assert not g["floor_hurdle_met"] and g["reading"] == "NO DETECTABLE INTERACTION"


def test_refuses_an_uncommitted_or_edited_plan(tmp_path):
    repo, out, grid = _synthetic(tmp_path, i_true=0.0)
    (out / "PLAN.md").write_text("edited after commit\n")
    _refused(lambda: _analyse(repo, out, grid), "uncommitted changes")
    other = tmp_path / "loose"
    other.mkdir()
    (other / "PLAN.md").write_text("never committed\n")
    with pytest.raises(Refusal):
        IA.plan_guard(other / "PLAN.md")


def test_refuses_a_run_that_did_not_record_the_committed_plan(tmp_path):
    repo, out, grid = _synthetic(tmp_path, i_true=0.0)
    prov = out / "provenance.txt"
    good = prov.read_text()
    prov.write_text(good + "date_utc: 2099-01-01T00:00:00Z\nplan_sha256: " + "f" * 64)
    _refused(lambda: _analyse(repo, out, grid), "recorded plan hash")
    prov.write_text(re.sub(r"date_utc: \S+", "date_utc: 2001-01-01T00:00:00Z", good))
    _refused(lambda: _analyse(repo, out, grid), "before the plan was committed")


def test_refuses_a_partial_family_or_a_wrong_config(tmp_path):
    repo, out, grid = _synthetic(tmp_path, i_true=0.0)
    f = out / "evals" / "eval_joint_s7_b_only.json"
    d = json.loads(f.read_text())
    f.write_text(json.dumps({**d, "config": "che/configs/theta_star_holdout.yaml"}))
    _refused(lambda: _analyse(repo, out, grid), "evaluated under")
    f.unlink()
    _refused(lambda: _analyse(repo, out, grid), "no partial family")


def test_refuses_a_dirty_tree_without_the_flag(tmp_path):
    repo, out, grid = _synthetic(tmp_path, i_true=0.0)
    _refused(
        lambda: IA.run(
            out,
            out / "PLAN.md",
            repo,
            log=False,
            grid_dirs=_grid(grid),
            gamma_source=grid["gamma_source"],
        ),
        "DIRTY",
    )


def test_detects_a_planted_links_open_effect(tmp_path):
    repo, out, grid = _synthetic(tmp_path, i_true=0.0, d_true=-0.03)
    res = _analyse(repo, out, grid)
    for m in IA.FAMILY:
        pool = res["links_open"][m]["pooled"]
        assert pool["reading"] == "DETECTABLE LINKS-OPEN EFFECT"
        assert pool["sign"] == "-" and pool["mean"] == pytest.approx(-0.03, abs=1e-3)
        g = res["interaction"][m]["pooled"]
        assert g["reading"] == "NO DETECTABLE INTERACTION"  # I untouched by D
    text = (out / "interaction_report.md").read_text()
    assert "Links-open contrast D" in text and "links_open" in text


def test_headline_follows_the_pool_only_when_the_arms_agree(tmp_path):
    repo, out, grid = _synthetic(tmp_path, i_true=-0.02)
    res = _analyse(repo, out, grid)
    h = res["headline"]["survival_rate"]["interaction"]
    assert h["arms_agree"] and not h["pooled_is_average_only"]
    assert h["headline"] == "DETECTABLE INTERACTION -"

    split = {"iso": -0.02, "joint": 0.02, "iso4": 0.0}
    repo, out, grid = _synthetic(tmp_path / "b", i_true=split)
    res = _analyse(repo, out, grid)
    h = res["headline"]["survival_rate"]["interaction"]
    assert h["arm_readings"]["iso"] == "DETECTABLE INTERACTION -"
    assert h["arm_readings"]["joint"] == "DETECTABLE INTERACTION +"
    assert not h["arms_agree"] and h["pooled_is_average_only"]
    assert h["headline"] == "DEPENDS ON TRAINING"
    assert "DEPENDS ON TRAINING" in (out / "interaction_report.md").read_text()


def test_context_puts_every_reading_beside_a_b_and_gamma(tmp_path):
    repo, out, grid = _synthetic(tmp_path, i_true=-0.02, d_true=0.01)
    res = _analyse(repo, out, grid)
    for m in IA.FAMILY:
        cx = res["context"][m]
        for q, src in (("I", "interaction"), ("D", "links_open")):
            assert cx[q] == {e: res[src][m][e]["mean"] for e in IA.ESTIMATES}
        assert cx["A"]["pooled"] == pytest.approx(-0.02, abs=1e-5)
        g = cx["gamma_registered"]
        assert g["mean"] == 0.0096 and g["ci"] == pytest.approx(
            [0.0096 - 2.2365 * 0.0022, 0.0096 + 2.2365 * 0.0022]
        )
    assert "Γ (registered" in (out / "interaction_report.md").read_text()
    grid["gamma_source"].unlink()
    _refused(lambda: _analyse(repo, out, grid), "context table")


def test_logit_block_is_descriptive_and_counts_what_it_leaves_out(tmp_path):
    repo, out, grid = _synthetic(tmp_path, i_true=-0.02)
    f = out / "evals" / "eval_iso_s2_neither.json"
    d = json.loads(f.read_text())
    d["metrics"]["completion"]["mean"] = 1.0  # no finite logit
    f.write_text(json.dumps(d))
    res = _analyse(repo, out, grid)
    lg = res["logit"]
    assert lg["completion"]["left_out"] == {"iso": 1, "joint": 0, "iso4": 0}
    assert lg["survival_rate"]["left_out"] == {"iso": 0, "joint": 0, "iso4": 0}
    assert lg["completion"]["estimates"]["iso"]["k"] == 71
    for m in IA.FAMILY:
        for e in IA.ESTIMATES:
            est = lg[m]["estimates"][e]
            assert "reading" not in est and len(est["ci_sidak"]) == 2
    assert lg["survival_rate"]["estimates"]["pooled"]["mean"] < 0


def _detach(out: Path, tmp: Path) -> Path:
    """A copy of the returned run outside any git repository."""
    loose = tmp / "loose_supplement" / "out"
    shutil.copytree(out, loose)
    return loose


def test_verify_without_git_matches_then_catches_a_changed_eval(tmp_path):
    repo, out, grid = _synthetic(tmp_path, i_true=-0.02, d_true=0.01)
    _analyse(repo, out, grid)
    loose = _detach(out, tmp_path)
    v = IA.verify(loose, loose / "PLAN.md", _grid(grid), grid["gamma_source"])
    assert v["matches"] and v["n_differences"] == 0
    assert any("version history" in n for n in v["not_checked"])
    assert "VERIFIED" in IA.render_verify(v)

    f = loose / "evals" / "eval_joint_s3_both.json"
    d = json.loads(f.read_text())
    d["metrics"]["survival_rate"]["mean"] += 0.01
    f.write_text(json.dumps(d))
    v = IA.verify(loose, loose / "PLAN.md", _grid(grid), grid["gamma_source"])
    assert not v["matches"] and v["n_differences"] > 0
    assert "MISMATCH" in IA.render_verify(v)

    (loose / "PLAN.md").write_text("another plan\n")
    _refused(
        lambda: IA.verify(loose, loose / "PLAN.md", _grid(grid), grid["gamma_source"]),
        "the report was made under",
    )


def test_verify_refuses_without_a_report(tmp_path):
    repo, out, grid = _synthetic(tmp_path, i_true=0.0)
    _refused(
        lambda: IA.verify(out, out / "PLAN.md", _grid(grid), grid["gamma_source"]),
        "nothing to verify against",
    )


def test_verify_only_checks_every_needed_archive_and_evaluates_nothing(tmp_path):
    conf, iso4 = tmp_path / "conf", tmp_path / "iso4"
    conf.mkdir()
    iso4.mkdir()
    lines = {conf: [], iso4: []}
    for d, tags in ((conf, ["iso_s1", "joint_s1"]), (iso4, ["iso4_s1"])):
        for t in tags:
            f = d / f"ckpt_{t}.tar.zst"
            f.write_bytes(t.encode())
            h = hashlib.sha256(t.encode()).hexdigest()
            lines[d].append(f"{h}  che/bench/results/elsewhere/{f.name}")
        (d / "SHA256_CKPT.txt").write_text("\n".join(lines[d]) + "\n")
    env = {
        "CONF_DIR": str(conf),
        "ISO4_DIR": str(iso4),
        "K_CONF": "1",
        "K_ISO4": "1",
        "VERIFY_ONLY": "1",
        "OUT": str(tmp_path / "out"),
    }
    (tmp_path / "out").mkdir()
    (tmp_path / "out" / "PLAN.md").write_text("plan\n")
    r = _run(env)
    assert r.returncode == 0, r.stderr
    assert "ARCHIVES: verified=3 bad_or_missing=0" in r.stdout
    assert not (tmp_path / "out" / "evals").exists()
    (iso4 / "ckpt_iso4_s1.tar.zst").write_bytes(b"tampered")
    r = _run(env)
    assert r.returncode == 1 and "bad_or_missing=1" in r.stdout
