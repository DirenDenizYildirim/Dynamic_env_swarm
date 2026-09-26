"""The post-unblind analysis, exercised on SYNTHETIC artifacts only.

Nothing here opens a file under che/bench/results/. Every artifact is built in
tmp_path with per-seed values chosen so each registered reading rule has a
known answer, and each rule's cells are walked one by one — including the
cells the registered text does not contain, which must be labelled
UNREGISTERED rather than framed.

Deterministic dispersion, as in test_p6_unblind: seed i takes
mean + sd·(+1 if i odd else −1), so with an even k the sample mean is exact.
"""

from __future__ import annotations

import inspect
import json
import math
import re
from pathlib import Path

import pytest

from che.scripts import p6_post_analysis as P
from che.scripts import p6_unblind as U
from che.scripts.m62_report import GAMMA_T_RETENTION, METRICS, T_STAR

SD = 0.01
THETA = P.THETA_STAR
REPO = Path(__file__).resolve().parents[2]


def _vals(k: int, mean: float, sd: float = SD) -> list[float]:
    return [mean + (sd if s % 2 else -sd) for s in range(1, k + 1)]


def _eval(f: Path, step: int, config: str, means: dict[str, float]) -> None:
    f.write_text(
        json.dumps(
            {
                "config": config,
                "ckpt_step": step,
                "n_episodes": 512,
                "seed": 0,
                "metrics": {m: {"mean": means.get(m, 0.5)} for m in METRICS},
            }
        )
    )


def _grid(
    root: Path,
    arms: dict[str, dict[str, list[float]]],
    *,
    updates: int = T_STAR,
    stamp_over: dict | None = None,
) -> Path:
    """A grid-shaped artifact: stamp, eval_<arm>_s<s>.json, manifest entries.
    arms[arm][metric] = per-seed values (metrics not given default to 0.5)."""
    root.mkdir(parents=True, exist_ok=True)
    k = len(next(iter(next(iter(arms.values())).values())))
    stamp = {
        "updates": updates,
        "k_conf": k,
        "k_sec": 0,
        "n_eval": 512,
        "eval_seed": 0,
        "eval_config": THETA,
        "conf_arms": " ".join(f"{a}:che/configs/p6_{a}.yaml" for a in arms) + " ",
        "sec_arms": "",
    }
    stamp.update(stamp_over or {})
    (root / "grid_params.txt").write_text(
        "".join(f"{a}: {b}\n" for a, b in stamp.items())
    )
    man = root / ".manifest"
    man.mkdir(exist_ok=True)
    for arm, per in arms.items():
        for i in range(k):
            tag = f"{arm}_s{i + 1}"
            _eval(
                root / f"eval_{tag}.json",
                updates,
                THETA,
                {m: v[i] for m, v in per.items()},
            )
            (man / f"{tag}.done").write_text(f"{'0' * 64}  ckpt_{tag}.tar.zst\n")
    return root


def _fam(c: float, s: float, k: int) -> dict[str, list[float]]:
    return {"completion": _vals(k, c), "survival_rate": _vals(k, s)}


def _conf(root: Path, g_c: float = 0.0, g_s: float = 0.0) -> Path:
    k = P.K_CONF
    return _grid(
        root, {"iso": _fam(0.5, 0.5, k), "joint": _fam(0.5 + g_c, 0.5 + g_s, k)}
    )


def _unblind(tmp: Path, conf: Path, log: bool = True) -> Path:
    """The unblind step as the real run leaves it: unblind.json + the log."""
    d = tmp / "unblind"
    U.run(conf, d, None, None, unblind=False, allow_dirty=False)
    if log:
        (d / "UNBLIND_LOG.txt").write_text(
            "2026-09-26T00:00:00+00:00  git x  branch=C\n"
        )
    return d


def _paths(tmp: Path, conf: Path, ub: Path) -> dict:
    return {
        "conf": conf,
        "unblind_dir": ub,
        "iso4": tmp / "iso4",
        "t2000": tmp / "t2000",
        "post_gamma_t": tmp / "post_gamma_t",
        "post_high": tmp / "post_high",
        "post_evalfloor": tmp / "post_evalfloor",
    }


def _evalfloor(d: Path, conf: Path, bump: float = 0.0) -> None:
    """Reps identical to the grid's own eval of the same checkpoint, unless
    `bump` perturbs rep 2."""
    d.mkdir(parents=True, exist_ok=True)
    for tag in P.EVALFLOOR_TAGS:
        g = json.loads((conf / f"eval_{tag}.json").read_text())["metrics"]
        for r in range(1, P.EVALFLOOR_REPS + 1):
            means = {m: g[m]["mean"] + (bump if r == 2 else 0.0) for m in METRICS}
            _eval(d / f"evalfloor_{tag}_rep{r}.json", T_STAR, THETA, means)


def _gamma_t(d: Path, gamma_at: dict[int, float]) -> None:
    """Post evals at t < T*: ISO at 0.5, JOINT at 0.5 + gamma_at[t], both metrics."""
    d.mkdir(parents=True, exist_ok=True)
    k = P.K_CONF
    for t in P.GAMMA_T_STEPS:
        if t == T_STAR:
            continue
        for arm, mu in (("iso", 0.5), ("joint", 0.5 + gamma_at[t])):
            for i, v in enumerate(_vals(k, mu)):
                _eval(
                    d / f"eval_{arm}_s{i + 1}_u{t}.json",
                    t,
                    THETA,
                    {"completion": v, "survival_rate": v},
                )


# --------------------------------------------------------- the arithmetic


def test_contrast_equals_the_unblind_instrument_at_equal_k():
    a, b = _vals(72, 0.5), _vals(72, 0.53, sd=0.02)
    mine, theirs = P.contrast(a, b), U.contrast(a, b)
    for key in ("gamma", "sd_gamma", "z", "reject", "p_two_sided", "exclusion_mde80"):
        assert mine[key] == pytest.approx(theirs[key])
    assert mine["ci_sidak"] == pytest.approx(theirs["ci_sidak"])
    assert mine["power_at_target"] == pytest.approx(theirs["power_at_target"])


def test_contrast_uses_the_unequal_k_combined_form():
    a, b = _vals(20, 0.5, sd=0.03), _vals(72, 0.5, sd=0.06)
    c = P.contrast(a, b)
    sa = 0.03 * math.sqrt(20 / 19)
    sb = 0.06 * math.sqrt(72 / 71)
    assert c["sd_gamma"] == pytest.approx(math.sqrt(sa**2 / 20 + sb**2 / 72))


def test_descriptive_contrast_carries_no_decision_field():
    c = P.contrast(_vals(4, 0.5), _vals(4, 0.6), decision=False)
    assert not {"reject", "ci_sidak", "exclusion_mde80", "p_two_sided"} & set(c)


def test_gamma_t_steps_are_the_retained_final_half():
    assert P.GAMMA_T_STEPS == tuple(range(500, 1001, 50))
    assert len(P.GAMMA_T_STEPS) == GAMMA_T_RETENTION


def test_design_mirrors_the_job_scripts():
    """The shell scripts produce what this module reads; a drift fails here."""
    post = (REPO / "che/scripts/run_p6_post_unblind_evals.sh").read_text()
    s7 = (REPO / "che/scripts/run_p6_s7_blocks.sh").read_text()

    def default(src: str, var: str) -> str:
        return re.search(rf"^{var}=\$\{{{var}:-\"?([^}}\"]*)\"?\}}", src, re.M).group(1)

    assert int(default(post, "K_CONF")) == P.K_CONF
    assert int(default(post, "K_ISO4")) == P.K_ISO4
    assert int(default(post, "N_FLOOR_REPS")) == P.N_FLOOR_REPS
    assert int(default(post, "EVALFLOOR_REPS")) == P.EVALFLOOR_REPS
    assert tuple(default(post, "EVALFLOOR_TAGS").split()) == P.EVALFLOOR_TAGS
    assert default(post, "HIGH_CFG") == P.HIGH_CONFIG
    assert default(post, "THETA_STAR") == P.THETA_STAR
    gt = tuple(int(x) for x in default(post, "GAMMA_T_STEPS").split())
    assert gt + (T_STAR,) == P.GAMMA_T_STEPS  # 1000 is the grid's own eval
    assert int(default(s7, "K_T2000")) == P.K_T2000
    assert int(default(s7, "T2000_UPDATES")) == P.T_2000


# --------------------------------------------------------- the guards


def test_refuses_before_the_unblind_step(tmp_path):
    conf = _conf(tmp_path / "conf")
    ub = _unblind(tmp_path, conf, log=False)
    with pytest.raises(SystemExit) as e:
        P.run(["t2000"], tmp_path / "out", **_paths(tmp_path, conf, ub))
    assert e.value.code == 2
    (ub / "UNBLIND_LOG.txt").write_text("")  # an empty log is not a look
    with pytest.raises(SystemExit):
        P.run(["t2000"], tmp_path / "out", **_paths(tmp_path, conf, ub))


def test_run_has_no_default_path_into_the_results():
    """Only the CLI carries real defaults; run() must be given every path."""
    sig = inspect.signature(P.run)
    for name in ("conf", "unblind_dir", "iso4", "t2000", "post_gamma_t", "post_high"):
        assert sig.parameters[name].default is inspect.Parameter.empty


def test_unknown_section_is_refused(tmp_path):
    conf = _conf(tmp_path / "conf")
    ub = _unblind(tmp_path, conf)
    with pytest.raises(SystemExit):
        P.run(["gamma5"], tmp_path / "out", **_paths(tmp_path, conf, ub))


def test_real_artifact_invocation_is_logged(tmp_path, monkeypatch):
    monkeypatch.setattr(U, "RESULTS_ROOT", tmp_path / "results")
    conf = _conf(tmp_path / "results" / "phase6" / "conf")
    ub = tmp_path / "unblind"
    U.run(conf, ub, None, None, unblind=True, allow_dirty=True)  # writes the log
    _evalfloor(tmp_path / "post_evalfloor", conf)
    P.run(
        ["evalfloor"], tmp_path / "out", allow_dirty=True, **_paths(tmp_path, conf, ub)
    )
    log = (tmp_path / "out" / "POST_UNBLIND_LOG.txt").read_text()
    assert "sections=evalfloor" in log and "git" in log


# --------------------------------------------------------- eval floor


def test_eval_floor_identical_reps_and_cross_unit(tmp_path):
    conf = _conf(tmp_path / "conf")
    ub = _unblind(tmp_path, conf)
    _evalfloor(tmp_path / "post_evalfloor", conf)
    e = P.run(["evalfloor"], tmp_path / "out", **_paths(tmp_path, conf, ub))[
        "evalfloor"
    ]
    assert e["deterministic_on_post_card"] and e["cross_unit_identical"]


def test_eval_floor_reports_a_nonzero_floor(tmp_path):
    conf = _conf(tmp_path / "conf")
    ub = _unblind(tmp_path, conf)
    _evalfloor(tmp_path / "post_evalfloor", conf, bump=1e-3)
    e = P.run(["evalfloor"], tmp_path / "out", **_paths(tmp_path, conf, ub))[
        "evalfloor"
    ]
    assert not e["deterministic_on_post_card"] and not e["cross_unit_identical"]
    v = e["tags"]["iso_s1"]["completion"]
    assert v["cross_unit_diff"] == pytest.approx(1e-3 / P.EVALFLOOR_REPS)
    assert v["rep_sd"] > 0


# --------------------------------------------------------- Γ(t)


def test_gamma_t_is_refused_without_the_eval_floor(tmp_path):
    conf = _conf(tmp_path / "conf", g_c=0.02, g_s=0.02)
    ub = _unblind(tmp_path, conf)
    _gamma_t(tmp_path / "post_gamma_t", {t: 0.02 for t in P.GAMMA_T_STEPS})
    with pytest.raises(SystemExit):  # post_evalfloor absent
        P.run(["gamma_t"], tmp_path / "out", **_paths(tmp_path, conf, ub))
    with pytest.raises(SystemExit):
        P.sec_gamma_t(conf, tmp_path / "post_gamma_t", None)


def test_gamma_t_stable_sign_is_budget_robust(tmp_path):
    conf = _conf(tmp_path / "conf", g_c=0.02, g_s=0.02)
    ub = _unblind(tmp_path, conf)
    _evalfloor(tmp_path / "post_evalfloor", conf)
    _gamma_t(tmp_path / "post_gamma_t", {t: 0.001 * (t / 100) for t in P.GAMMA_T_STEPS})
    g = P.run(["gamma_t"], tmp_path / "out", **_paths(tmp_path, conf, ub))["gamma_t"]
    for m in U.FAMILY:
        v = g["verdict"][m]
        assert v["stable"] and v["reading"].startswith("BUDGET-ROBUST")
        assert len(v["signs"]) == 11
    # the T* point IS the primary Γ, read from the grid's own evals
    last = g["points"]["completion"][-1]
    assert last["t"] == T_STAR and last["gamma"] == pytest.approx(0.02)


def test_gamma_t_sign_change_is_the_finding(tmp_path):
    conf = _conf(tmp_path / "conf", g_c=0.02, g_s=0.02)
    ub = _unblind(tmp_path, conf)
    _evalfloor(tmp_path / "post_evalfloor", conf)
    gam = {t: 0.02 for t in P.GAMMA_T_STEPS}
    gam[750] = -0.001  # one tiny flip — the rule reads signs, not significance
    _gamma_t(tmp_path / "post_gamma_t", gam)
    v = P.run(["gamma_t"], tmp_path / "out", **_paths(tmp_path, conf, ub))["gamma_t"][
        "verdict"
    ]["completion"]
    assert not v["stable"] and v["t_disagreeing"] == [750]
    assert "instability IS the finding" in v["reading"]


def test_gamma_t_refuses_a_wrong_step(tmp_path):
    conf = _conf(tmp_path / "conf")
    ub = _unblind(tmp_path, conf)
    _evalfloor(tmp_path / "post_evalfloor", conf)
    _gamma_t(tmp_path / "post_gamma_t", {t: 0.0 for t in P.GAMMA_T_STEPS})
    f = tmp_path / "post_gamma_t" / "eval_iso_s3_u600.json"
    d = json.loads(f.read_text())
    d["ckpt_step"] = 1000
    f.write_text(json.dumps(d))
    with pytest.raises(SystemExit):
        P.run(["gamma_t"], tmp_path / "out", **_paths(tmp_path, conf, ub))


# --------------------------------------------------------- Γ₄ and B̂


def _g4(z: float, k_a: int = 20, k_b: int = 72) -> dict:
    """A Γ₄-shaped contrast whose z is (very nearly) `z`."""
    sd = math.sqrt(
        (SD * SD) * (k_a / (k_a - 1)) / k_a + (SD * SD) * (k_b / (k_b - 1)) / k_b
    )
    return P.contrast(_vals(k_a, 0.5), _vals(k_b, 0.5 + z * sd))


def _g(reject: bool, sign: str) -> dict:
    return {
        "reject": reject,
        "sign": sign,
        "gamma": {"+": 0.05, "-": -0.05, "0": 0.0}[sign],
    }


@pytest.mark.parametrize(
    "g,z4,label",
    [
        (_g(True, "+"), 6.0, "SURVIVES"),
        (_g(True, "+"), 1.0, "DOES_NOT_SURVIVE"),  # Γ₄ CI includes 0
        (_g(True, "+"), -6.0, "DOES_NOT_SURVIVE"),  # opposite sign
        (_g(True, "-"), -6.0, "SURVIVES"),
        (_g(False, "+"), 1.0, "SECOND_EXCLUSION"),
        (_g(False, "-"), -1.0, "SECOND_EXCLUSION"),
        (_g(False, "+"), -6.0, "BRANCH_D_SECONDARY"),
        (_g(False, "-"), 6.0, "UNREGISTERED"),  # not in the registered rule
    ],
)
def test_gamma4_reading_rule_cells(g, z4, label):
    assert P._gamma4_reading(g, _g4(z4))[0] == label


def test_gamma4_end_to_end_and_b_hat(tmp_path):
    conf = _conf(tmp_path / "conf", g_c=0.03, g_s=0.0)
    ub = _unblind(tmp_path, conf)
    _grid(tmp_path / "iso4", {"iso4": _fam(0.51, 0.49, P.K_ISO4)})
    r = P.run(["gamma4"], tmp_path / "out", **_paths(tmp_path, conf, ub))["gamma4"]
    c = r["per_metric"]["completion"]
    assert c["gamma"]["gamma"] == pytest.approx(0.03)
    assert c["gamma4"]["gamma"] == pytest.approx(0.02)  # 0.53 − 0.51
    assert c["b_hat"]["gamma"] == pytest.approx(0.01)  # ISO-4 − ISO
    assert (c["gamma4"]["k_a"], c["gamma4"]["k_b"]) == (P.K_ISO4, P.K_CONF)
    s = r["per_metric"]["survival_rate"]
    assert s["b_hat"]["gamma"] == pytest.approx(-0.01)


def test_gamma4_refuses_if_the_artifact_moved_since_the_look(tmp_path):
    conf = _conf(tmp_path / "conf", g_c=0.03)
    ub = _unblind(tmp_path, conf)
    _grid(tmp_path / "iso4", {"iso4": _fam(0.5, 0.5, P.K_ISO4)})
    f = conf / "eval_joint_s7.json"
    d = json.loads(f.read_text())
    d["metrics"]["completion"]["mean"] += 0.1
    f.write_text(json.dumps(d))
    with pytest.raises(SystemExit):
        P.run(["gamma4"], tmp_path / "out", **_paths(tmp_path, conf, ub))


@pytest.mark.parametrize(
    "over", [{"k_conf": 12}, {"updates": 2000}, {"conf_arms": "iso:x "}]
)
def test_gamma4_refuses_a_wrong_iso4_stamp(tmp_path, over):
    conf = _conf(tmp_path / "conf")
    ub = _unblind(tmp_path, conf)
    _grid(tmp_path / "iso4", {"iso4": _fam(0.5, 0.5, P.K_ISO4)}, stamp_over=over)
    with pytest.raises(SystemExit):
        P.run(["gamma4"], tmp_path / "out", **_paths(tmp_path, conf, ub))


# --------------------------------------------------------- High readout


@pytest.mark.parametrize(
    "z,label",
    [
        (0.5, "EXCLUSION"),
        (-0.5, "EXCLUSION"),
        (6.0, "IN_DISTRIBUTION"),
        (-6.0, "EXPLORATORY_NEGATIVE"),
    ],
)
def test_high_reading_is_asymmetric(z, label):
    sd = math.sqrt(2 * SD * SD * (72 / 71) / 72)
    c = P.contrast(_vals(72, 0.5), _vals(72, 0.5 + z * sd))
    assert P._high_reading(c)[0] == label


def test_high_end_to_end_with_its_floor(tmp_path):
    conf = _conf(tmp_path / "conf")
    ub = _unblind(tmp_path, conf)
    d = tmp_path / "post_high"
    d.mkdir()
    cfg, k = P.HIGH_CONFIG, P.K_CONF
    for arm, mu, n, stem in (
        ("iso", 0.40, k, "s"),
        ("joint", 0.40, k, "s"),
        ("iso4", 0.41, P.K_ISO4, "s"),
        ("iso", 0.40, P.N_FLOOR_REPS, "rep"),
        ("joint", 0.40, P.N_FLOOR_REPS, "rep"),
    ):
        amp = SD / 2 if stem == "rep" else SD
        for i, v in enumerate(_vals(n, mu, amp)):
            _eval(
                d / f"evalhigh_{arm}_{stem}{i + 1}.json",
                T_STAR,
                cfg,
                {"completion": v, "survival_rate": v},
            )
    h = P.run(["high"], tmp_path / "out", **_paths(tmp_path, conf, ub))["high"]
    c = h["per_metric"]["completion"]
    assert c["label"] == "EXCLUSION" and "Never an absence" in c["why"]
    assert c["gamma_H4"]["gamma"] == pytest.approx(-0.01)
    ratio = (SD * math.sqrt(72 / 71)) / (SD / 2 * math.sqrt(8 / 7))
    assert c["floor"]["ratio_seed_over_floor_iso"] == pytest.approx(ratio)
    assert "UNDERPOWERED" in c["floor"]["iso4"]


def test_high_refuses_a_theta_star_eval(tmp_path):
    """A High eval must be DECLARED under joint_high; a θ* file is refused."""
    conf = _conf(tmp_path / "conf")
    ub = _unblind(tmp_path, conf)
    d = tmp_path / "post_high"
    d.mkdir()
    _eval(d / "evalhigh_iso_s1.json", T_STAR, THETA, {})
    with pytest.raises(SystemExit):
        P.run(["high"], tmp_path / "out", **_paths(tmp_path, conf, ub))


# --------------------------------------------------------- T = 2000


def _t2000(root: Path, slope_joint: float) -> Path:
    arms = ("iso_t2000", "joint_t2000")
    _grid(root, {a: _fam(0.5, 0.5, P.K_T2000) for a in arms}, updates=P.T_2000)
    for a in arms:
        for s in range(1, P.K_T2000 + 1):
            rows = []
            for u in range(1, P.T_2000 + 1):
                y = 0.3 + (slope_joint * u if a == "joint_t2000" else 0.0) + 0.001 * s
                # completion is gappy in real logs: every 3rd update has none
                c = float("nan") if u % 3 == 0 else y
                rows.append(
                    json.dumps({"update": u, "completion": c, "survival_rate": y})
                )
            (root / f"{a}_s{s}.jsonl").write_text("\n".join(rows) + "\n")
    return root


def test_t2000_is_descriptive_and_slopes_are_exact(tmp_path):
    conf = _conf(tmp_path / "conf")
    ub = _unblind(tmp_path, conf)
    _t2000(tmp_path / "t2000", slope_joint=1e-4)
    t = P.run(["t2000"], tmp_path / "out", **_paths(tmp_path, conf, ub))["t2000"]
    assert "UNDERPOWERED" in t["flag"]
    assert "reject" not in json.dumps(t["gamma_2000"])
    for m in U.FAMILY:
        for w in ("(500,1000]", "(1000,2000]"):
            assert t["differential_slope_per_100"][m][w] == pytest.approx(0.01)
    cur = t["curves"]["survival_rate"]
    assert sorted(cur["iso_t2000"]) == list(range(100, 2001, 100))
    # seed spread survives: seeds differ by 0.001 steps
    assert cur["iso_t2000"][100]["sd"] == pytest.approx(
        0.001 * math.sqrt(sum((s - 2.5) ** 2 for s in range(1, 5)) / 3)
    )


def test_t2000_refuses_a_t1000_stamp(tmp_path):
    conf = _conf(tmp_path / "conf")
    ub = _unblind(tmp_path, conf)
    root = _t2000(tmp_path / "t2000", slope_joint=0.0)
    txt = (
        (root / "grid_params.txt").read_text().replace("updates: 2000", "updates: 1000")
    )
    (root / "grid_params.txt").write_text(txt)
    with pytest.raises(SystemExit):
        P.run(["t2000"], tmp_path / "out", **_paths(tmp_path, conf, ub))
