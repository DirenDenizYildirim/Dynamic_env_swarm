"""The secondary (sweep / identification / mediation) instrument, on SYNTHETIC
artifacts only. Nothing here opens a file under che/bench/results/.

Each arm's per-seed value is f(m, p, n) + sd·(±1 alternating by seed), so arm
means are exact and every registered estimator has a known answer.
"""

from __future__ import annotations

import inspect
import json
import re
from pathlib import Path

import pytest

from che.scripts import p6_secondary as S
from che.scripts import p6_unblind as U
from che.scripts.m62_report import METRICS, T_STAR

THETA = U.EVAL_CONFIG
REPO = Path(__file__).resolve().parents[2]
SD = 0.01


@pytest.fixture(autouse=True)
def _fast_bootstrap(monkeypatch):
    monkeypatch.setattr(S, "N_BOOT", 300)


def _wig(s: int, sd: float) -> float:
    return sd if s % 2 else -sd


def _eval(f: Path, means: dict[str, float], step: int = T_STAR) -> None:
    f.write_text(
        json.dumps(
            {
                "config": THETA,
                "ckpt_step": step,
                "n_episodes": 512,
                "seed": 0,
                "metrics": {m: {"mean": means.get(m, 0.5)} for m in METRICS},
            }
        )
    )


def _stamp(d: Path, k_sec: int, **over) -> None:
    st = {
        "updates": T_STAR,
        "k_conf": 0,
        "k_sec": k_sec,
        "n_eval": 512,
        "eval_seed": 0,
        "eval_config": THETA,
        "conf_arms": "",
        "sec_arms": " ".join(f"{a}:x" for a, _, _ in S.ARMS) + " ",
    }
    st.update(over)
    (d / "grid_params.txt").write_text("".join(f"{a}: {b}\n" for a, b in st.items()))


def build(
    root: Path,
    f=lambda m, p, n: 0.5,
    dose=lambda p: 1.0 + p,
    sd: float = SD,
    dose_sd: float = 0.01,
    poison_grid_low_seeds: bool = False,
) -> tuple[Path, Path]:
    """Two dirs laid out as the real ones: re-card seeds 1..12, grid 13..20."""
    rec, grid = root / "recard", root / "grid"
    for d, k in ((rec, 12), (grid, 20)):
        d.mkdir(parents=True)
        (d / ".manifest").mkdir()
        _stamp(d, k)
    for a, m, p in S.ARMS:
        n = S.no_element(m, p)
        for s in range(1, 21):
            d = rec if s <= 12 else grid
            v = f(m, p, n) + _wig(s, sd)
            _eval(d / f"eval_{a}_s{s}.json", {"completion": v, "survival_rate": v})
            (d / ".manifest" / f"{a}_s{s}.done").write_text("0" * 64 + "\n")
            rows = [
                json.dumps(
                    {"update": u, "co_active_per_step": dose(p) + _wig(s, dose_sd)}
                )
                for u in range(0, T_STAR + 1, 50)
            ]
            (d / f"{a}_s{s}.jsonl").write_text("\n".join(rows) + "\n")
            if poison_grid_low_seeds and s <= 12:  # PRO 6000 seeds: must be ignored
                _eval(
                    grid / f"eval_{a}_s{s}.json",
                    {"completion": 99.0, "survival_rate": 99.0},
                )
    return rec, grid


def _ub(root: Path) -> Path:
    d = root / "unblind"
    d.mkdir()
    (d / "UNBLIND_LOG.txt").write_text("2026-09-26  git x  branch=B\n")
    return d


def _run(root: Path, rec: Path, grid: Path, **kw) -> dict:
    kw.setdefault("floors", None)
    kw.setdefault("conf", None)
    kw.setdefault("iso4", None)
    return S.run(root / "out", recard=rec, grid=grid, unblind_dir=_ub(root), **kw)


# ------------------------------------------------------------ design


def test_design_matches_the_generated_configs():
    pat = re.compile(
        r"# Realized marginals: A ([\d.]+)\s+B ([\d.]+)\s+co-occurrence ([\d.]+)"
        r"\s+no-element ([\d.]+)"
    )
    for a, m, p in S.ARMS:
        head = (REPO / "che/configs" / f"p6_{a}.yaml").read_text()
        A, B, co, ne = (float(x) for x in pat.search(head).groups())
        assert (A, B, co) == (m, m, p)
        assert ne == pytest.approx(S.no_element(m, p))


def test_the_two_sweeps_are_distinct_lines_so_the_plane_is_identified():
    """c = 0.5 has n = p, c = 0.4 has n = 0.2 + p: parallel but offset, which
    is what makes (γ_p, γ_n) estimable."""
    offs = {round(S.no_element(m, p) - p, 6) for _, m, p in S.ARMS}
    assert offs == {0.0, 0.2}


# ------------------------------------------------------------ reading


def test_seeds_1_12_come_only_from_the_re_card(tmp_path):
    rec, grid = build(tmp_path, poison_grid_low_seeds=True)
    r = _run(tmp_path, rec, grid)
    assert r["metrics"]["completion"]["sweep_means"]["sweep_c50_p000"] == pytest.approx(
        0.5
    )


def test_refuses_a_missing_seed_and_a_wrong_stamp(tmp_path):
    rec, grid = build(tmp_path / "a")
    (rec / "eval_sweep_c50_p250_s3.json").unlink()
    with pytest.raises(SystemExit):
        _run(tmp_path / "a", rec, grid)
    rec, grid = build(tmp_path / "b")
    _stamp(grid, 20, updates=2000)
    with pytest.raises(SystemExit):
        _run(tmp_path / "b", rec, grid)


def test_refuses_before_the_unblind(tmp_path):
    rec, grid = build(tmp_path)
    ub = tmp_path / "ub"
    ub.mkdir()
    with pytest.raises(SystemExit):
        S.run(
            tmp_path / "o",
            recard=rec,
            grid=grid,
            floors=None,
            unblind_dir=ub,
            conf=None,
            iso4=None,
        )


def test_run_has_no_default_artifact_paths():
    sig = inspect.signature(S.run)
    for name in ("recard", "grid", "floors", "unblind_dir", "conf", "iso4"):
        assert sig.parameters[name].default is inspect.Parameter.empty


# ------------------------------------------------------------ estimators


def test_pava():
    assert S.pava([1, 3, 2, 4, 5], [1] * 5, True) == pytest.approx([1, 2.5, 2.5, 4, 5])
    assert S.pava([1, 2, 3], [1] * 3, False) == pytest.approx([2, 2, 2])
    assert S.pava([3, 1, 2], [1] * 3, False) == pytest.approx([3, 1.5, 1.5])


def test_dose_trend_direction_and_slope(tmp_path):
    rec, grid = build(tmp_path, f=lambda m, p, n: 0.9 - 0.1 * p)
    t = _run(tmp_path, rec, grid)["metrics"]["survival_rate"]["dose_trend"]
    assert t["direction"] == "nonincreasing"
    assert t["ols_slope_per_unit_p"] == pytest.approx(-0.1, abs=1e-9)
    lo, hi = t["ols_slope_ci95"]
    assert lo < -0.1 < hi


def test_confound_plane_is_recovered_and_the_bound_is_half_gamma_n(tmp_path):
    rec, grid = build(tmp_path, f=lambda m, p, n: 0.9 + 0.02 * p - 0.04 * n)
    c = _run(tmp_path, rec, grid)["metrics"]["completion"]["confound"]
    assert c["gamma_p"] == pytest.approx(0.02, abs=1e-9)
    assert c["gamma_n"] == pytest.approx(-0.04, abs=1e-9)
    assert c["sweep_slope_decomposed"] == pytest.approx(-0.02, abs=1e-9)
    assert c["bound_confound_share_of_sweep_change"] == pytest.approx(-0.02, abs=1e-9)
    lo, hi = c["bound_ci95"]
    assert lo < -0.02 < hi
    assert all(abs(x["resid_over_se"]) < 1e-6 for x in c["arm_means_vs_plane"])


def test_knee_found_and_not_flagged_when_sharp(tmp_path):
    rec, grid = build(
        tmp_path, f=lambda m, p, n: 0.8 + 0.4 * max(p - 0.25, 0.0), sd=1e-4
    )
    k = _run(tmp_path, rec, grid)["metrics"]["completion"]["knee"]
    assert k["kappa"] == 0.25
    assert k["ci95"] == [0.25, 0.25] and not k["underpowered"]


def test_flat_dose_response_flags_the_knee_underpowered(tmp_path):
    rec, grid = build(tmp_path, f=lambda m, p, n: 0.7)
    k = _run(tmp_path, rec, grid)["metrics"]["completion"]["knee"]
    assert k["underpowered"] and "UNDERPOWERED" in k["flag"]


def test_endpoint_floor_grade_and_its_flags(tmp_path):
    rec, grid = build(tmp_path, f=lambda m, p, n: 0.9 - 0.02 * p / 0.5)
    fl = tmp_path / "floors.json"
    fl.write_text(
        json.dumps(
            {"sweep_p500": {"completion": {"sd": 0.02}, "survival_rate": {"sd": 0.01}}}
        )
    )
    e = _run(tmp_path, rec, grid, floors=fl)["metrics"]["completion"]["endpoint_grade"]
    assert e["endpoint_diff"] == pytest.approx(-0.02, abs=1e-9)
    assert e["diff_over_floor_se"] == pytest.approx(0.02 / (2 * 0.02**2 / 20) ** 0.5)
    assert "ASSUMED COMMON" in e["floor_note"]


def test_no_floor_is_ungraded(tmp_path):
    rec, grid = build(tmp_path)
    e = _run(tmp_path, rec, grid)["metrics"]["survival_rate"]["endpoint_grade"]
    assert "UNGRADED" in e["floor_note"]


# ------------------------------------------------------------ mediation


def test_mediation_void_when_realized_dose_does_not_move(tmp_path):
    rec, grid = build(tmp_path, dose=lambda p: 2.0)
    md = _run(tmp_path, rec, grid)["mediation"]
    assert md["void"] and md["figure_table"] is None and "VOID" in md["verdict"]


def test_mediation_first_stage_holds_and_gives_only_a_table(tmp_path):
    rec, grid = build(tmp_path, dose=lambda p: 1.0 + 3.0 * p)
    md = _run(tmp_path, rec, grid)["mediation"]
    assert not md["void"]
    assert md["first_stage_slope"] == pytest.approx(3.0, abs=1e-9)
    assert [r["p"] for r in md["figure_table"]] == [p for _, _, p in S.SWEEP]
    assert "second_stage" not in json.dumps(md)


# ------------------------------------------------------------ S5 replicate


def _grid_arm(root: Path, arm: str, k: int, val: float, conf_arms: str) -> Path:
    root.mkdir(parents=True)
    (root / ".manifest").mkdir()
    (root / "grid_params.txt").write_text(
        f"updates: {T_STAR}\nk_conf: {k}\nk_sec: 0\nn_eval: 512\neval_seed: 0\n"
        f"eval_config: {THETA}\nconf_arms: {conf_arms}\nsec_arms: \n"
    )
    for s in range(1, k + 1):
        v = val + _wig(s, SD)
        _eval(root / f"eval_{arm}_s{s}.json", {"completion": v, "survival_rate": v})
        (root / ".manifest" / f"{arm}_s{s}.done").write_text("0" * 64 + "\n")
    return root


def test_same_card_replicate(tmp_path):
    rec, grid = build(tmp_path, f=lambda m, p, n: 0.92 if (m, p) == (0.5, 0.0) else 0.9)
    conf = _grid_arm(tmp_path / "conf", "joint", 72, 0.925, "iso:x joint:x ")
    for s in range(1, 73):  # the confirmatory reader wants both arms present
        _eval(conf / f"eval_iso_s{s}.json", {})
        (conf / ".manifest" / f"iso_s{s}.done").write_text("0" * 64 + "\n")
    iso4 = _grid_arm(tmp_path / "iso4", "iso4", 20, 0.926, "iso4:x ")
    r = _run(tmp_path, rec, grid, conf=conf, iso4=iso4)["replicate"]["survival_rate"]
    assert r["gamma4_prime"]["gamma"] == pytest.approx(0.005)  # 0.925 − 0.92
    assert (r["gamma4_prime"]["k_a"], r["gamma4_prime"]["k_b"]) == (20, 72)
    assert "reject" in r["gamma4_prime"]  # read at z_alpha, like Γ₄
    assert r["replicate_diff"]["gamma"] == pytest.approx(-0.006)  # p000 − ISO-4
    assert "reject" not in r["replicate_diff"]


def test_real_artifact_run_is_logged(tmp_path, monkeypatch):
    monkeypatch.setattr(U, "RESULTS_ROOT", tmp_path / "results")
    rec, grid = build(tmp_path / "results" / "p6")
    S.run(
        tmp_path / "out",
        recard=rec,
        grid=grid,
        floors=None,
        unblind_dir=_ub(tmp_path),
        conf=None,
        iso4=None,
        allow_dirty=True,
    )
    assert "git" in (tmp_path / "out" / "SECONDARY_LOG.txt").read_text()
