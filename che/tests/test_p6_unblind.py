"""The unblind instrument, exercised on SYNTHETIC artifacts only.

Nothing here opens a file under che/bench/results/. Every artifact is built in
tmp_path with per-seed values chosen so the registered arithmetic has a known
answer, and the branch table is walked cell by cell — including the cell the
registered table does not contain, which must STOP rather than guess.

Deterministic dispersion: seed i takes mean + sd·(+1 if i odd else −1), so
with an even k the sample mean is exact and the sample sd is
sd·sqrt(k/(k−1)). Both arms share the pattern, so Γ carries no noise and the
z targets below are hit exactly.
"""

from __future__ import annotations

import json
import math
import statistics
from pathlib import Path

import pytest

from che.scripts import p6_unblind as U
from che.scripts.m62_report import K_LADDER_CAP, METRICS, T_STAR

K = U.K_CONFIRMATORY_REALIZED
SD = 0.01  # per-arm dispersion amplitude, every metric


def _sd_gamma(k: int, sd: float = SD) -> float:
    s = sd * math.sqrt(k / (k - 1))
    return math.sqrt(2 * s * s / k)


def _stamp(k: int, **over) -> str:
    d = {
        "updates": T_STAR,
        "k_conf": k,
        "k_sec": 0,
        "n_eval": 512,
        "eval_seed": 0,
        "eval_config": "che/configs/theta_star_holdout.yaml",
        "conf_arms": "iso:che/configs/p6_iso.yaml joint:che/configs/p6_joint.yaml ",
        "sec_arms": "",
    }
    d.update(over)
    return "".join(f"{a}: {b}\n" for a, b in d.items())


def make_artifact(
    root: Path,
    k: int,
    gamma: dict[str, float],
    *,
    sd: float = SD,
    base: float = 0.5,
    ckpt_step: int = T_STAR,
    stamp_over: dict | None = None,
    per_seed_bump: dict[tuple[str, int], float] | None = None,
    manifest: bool = True,
) -> Path:
    """gamma[m] = JOINT − ISO mean on metric m (default 0). ISO mean = base."""
    root.mkdir(parents=True, exist_ok=True)
    (root / "grid_params.txt").write_text(_stamp(k, **(stamp_over or {})))
    man = root / ".manifest"
    man.mkdir(exist_ok=True)
    for arm in ("iso", "joint"):
        for s in range(1, k + 1):
            wig = sd if s % 2 else -sd
            mets = {}
            for m in METRICS:
                mu = base + (gamma.get(m, 0.0) if arm == "joint" else 0.0)
                mu += (per_seed_bump or {}).get((arm, s), 0.0)
                mets[m] = {"mean": mu + wig}
            tag = f"{arm}_s{s}"
            (root / f"eval_{tag}.json").write_text(
                json.dumps(
                    {
                        "config": "che/configs/theta_star_holdout.yaml",
                        "ckpt_step": ckpt_step,
                        "n_episodes": 512,
                        "seed": 0,
                        "metrics": mets,
                    }
                )
            )
            if manifest:
                (man / f"{tag}.done").write_text(
                    f"{'0' * 64}  {root}/ckpt_{tag}.tar.zst\n"
                )
    return root


def _run(art: Path, tmp: Path, **kw) -> dict:
    return U.run(art, tmp / "out", None, None, unblind=False, allow_dirty=False, **kw)


# ------------------------------------------------------------ the arithmetic


def test_sidak_z_is_the_frozen_value():
    assert U.Z_ALPHA == pytest.approx(2.2365, abs=5e-5)


def test_contrast_matches_the_registered_formulas(tmp_path):
    art = make_artifact(tmp_path / "a", K, {"completion": 0.02})
    r = _run(art, tmp_path)["primary"]["family"]["completion"]
    s = SD * math.sqrt(K / (K - 1))
    assert r["sd_iso"] == pytest.approx(s) and r["sd_joint"] == pytest.approx(s)
    assert r["gamma"] == pytest.approx(0.02)
    assert r["sd_gamma"] == pytest.approx(math.sqrt((s * s + s * s) / K))
    assert r["z"] == pytest.approx(0.02 / r["sd_gamma"])
    lo, hi = r["ci_sidak"]
    assert lo == pytest.approx(0.02 - U.Z_ALPHA * r["sd_gamma"])
    assert hi == pytest.approx(0.02 + U.Z_ALPHA * r["sd_gamma"])
    # exclusion X is the 80 %-power MDE at the corrected alpha, on realized sd
    assert r["exclusion_mde80"] == pytest.approx(
        (U.Z_ALPHA + U.Z_POWER) * r["sd_gamma"]
    )


# ------------------------------------------------------------ the branches


def _gam(z: float, k: int = K) -> float:
    return z * _sd_gamma(k)


@pytest.mark.parametrize(
    "zc,zs,label",
    [
        (6.0, 6.0, "A"),
        (1.0, 5.0, "B"),  # 1 + 2.2365 < 5: falsifier passes
        (1.0, 3.0, "C"),  # survival rejects, but 3.2365 >= 3: asymmetry note
        (0.5, -0.5, "C"),  # both null; negative POINT ESTIMATE is a null
        (-6.0, 6.0, "D"),  # completion rejects negative
        (6.0, -6.0, "D"),  # survival rejects negative
        (-6.0, -6.0, "D"),
        (6.0, 1.0, "A_c"),  # (+, null): registered pre-unblind, ruling (ii)
    ],
)
def test_branch_table(tmp_path, zc, zs, label):
    art = make_artifact(
        tmp_path / "a", K, {"completion": _gam(zc), "survival_rate": _gam(zs)}
    )
    res = _run(art, tmp_path)
    b = res["primary"]["branch"]
    assert b["label"] == label, b["why"]
    fam = res["primary"]["family"]
    assert fam["completion"]["z"] == pytest.approx(zc, abs=1e-6)
    assert fam["survival_rate"]["z"] == pytest.approx(zs, abs=1e-6)


def test_falsifier_is_reported_with_margin(tmp_path):
    art = make_artifact(
        tmp_path / "a", K, {"completion": _gam(1.0), "survival_rate": _gam(3.0)}
    )
    f = _run(art, tmp_path)["primary"]["branch"]["falsifier"]
    assert f["lhs_abs_zc_plus_z_alpha"] == pytest.approx(1.0 + U.Z_ALPHA, abs=1e-6)
    assert f["rhs_abs_zs"] == pytest.approx(3.0, abs=1e-6)
    assert f["passes"] is False


def test_asymmetry_case_says_so_and_never_says_B(tmp_path):
    art = make_artifact(
        tmp_path / "a", K, {"survival_rate": _gam(2.3), "completion": _gam(0.5)}
    )
    b = _run(art, tmp_path)["primary"]["branch"]
    assert b["label"] == "C" and "ASYMMETRY NOTE" in b["why"]


def test_completion_only_cell_is_branch_a_c_with_a_survival_exclusion(tmp_path):
    """Ruling (ii), 2026-09-26: (+, null) is the founding claim on completion;
    the survival null is quoted as an exclusion with its X, and no asymmetry
    (falsifier) reading is attached."""
    art = make_artifact(tmp_path / "a", K, {"completion": _gam(4.0)})
    r = _run(art, tmp_path)["primary"]
    b = r["branch"]
    assert b["label"] == "A_c" and "EXCLUSION" in b["why"]
    x = r["family"]["survival_rate"]["exclusion_mde80"]
    assert f"{x:.4f}" in b["why"]
    assert "UNREGISTERED" not in json.dumps(r)


# ------------------------------------------------- primary k and the prefix


def test_prefix_analysis_uses_exactly_the_first_60_seeds(tmp_path):
    """Seeds 61..72 carry a large JOINT effect; the prefix must not see it."""
    bump = {("joint", s): 0.5 for s in range(K_LADDER_CAP + 1, K + 1)}
    art = make_artifact(tmp_path / "a", K, {}, per_seed_bump=bump)
    res = _run(art, tmp_path)
    assert res["prefix"]["k"] == K_LADDER_CAP == 60
    assert res["primary"]["k"] == K == 72
    assert res["prefix"]["family"]["completion"]["gamma"] == pytest.approx(
        0.0, abs=1e-12
    )
    assert res["primary"]["family"]["completion"]["gamma"] > 0.05
    assert len(res["prefix"]["per_seed"]["iso"]["completion"]) == 60


def test_both_analyses_are_written(tmp_path):
    art = make_artifact(tmp_path / "a", K, {})
    _run(art, tmp_path)
    j = json.loads((tmp_path / "out" / "unblind.json").read_text())
    assert j["primary"]["k"] == 72 and j["prefix"]["k"] == 60
    rep = (tmp_path / "out" / "report.md").read_text()
    assert "PRIMARY — k = 72" in rep and "PREFIX — k = 60" in rep
    assert "UNDERPOWERED" in rep and "matched budget" in rep
    assert not (tmp_path / "out" / "UNBLIND_LOG.txt").exists()  # synthetic: no log


# ------------------------------------------------------------ the refusals


def test_refuses_wrong_checkpoint_step(tmp_path):
    art = make_artifact(tmp_path / "a", K, {}, ckpt_step=T_STAR - 50)
    with pytest.raises(SystemExit) as e:
        _run(art, tmp_path)
    assert e.value.code == 2


def test_refuses_missing_seed(tmp_path):
    art = make_artifact(tmp_path / "a", K, {})
    (art / "eval_joint_s37.json").unlink()
    with pytest.raises(SystemExit):
        _run(art, tmp_path)


def test_refuses_orphaned_eval(tmp_path):
    art = make_artifact(tmp_path / "a", K, {})
    (art / ".manifest" / "iso_s5.done").unlink()
    with pytest.raises(SystemExit):
        _run(art, tmp_path)


@pytest.mark.parametrize(
    "over",
    [
        {"updates": 500},
        {"k_conf": 46},
        {"eval_seed": 1},
        {"n_eval": 256},
        {"eval_config": "che/configs/joint_high.yaml"},
    ],
)
def test_refuses_a_stamp_that_is_not_the_registered_design(tmp_path, over):
    art = make_artifact(tmp_path / "a", K, {}, stamp_over=over)
    with pytest.raises(SystemExit):
        _run(art, tmp_path)


def test_refuses_a_shorter_artifact_at_the_primary_k(tmp_path):
    """k = 46 exists as a superseded artifact; the primary analysis is k = 72."""
    art = make_artifact(tmp_path / "a", 46, {})
    with pytest.raises(SystemExit):
        _run(art, tmp_path)


def test_real_artifact_needs_the_flag(tmp_path, monkeypatch):
    monkeypatch.setattr(U, "RESULTS_ROOT", tmp_path / "results")
    art = make_artifact(tmp_path / "results" / "phase6" / "g1", K, {})
    with pytest.raises(SystemExit) as e:
        U.run(art, tmp_path / "out", None, None, unblind=False, allow_dirty=False)
    assert e.value.code == 2
    # With the flag (and a possibly dirty dev tree tolerated) it runs and LOGS.
    U.run(art, tmp_path / "out", None, None, unblind=True, allow_dirty=True)
    log = (tmp_path / "out" / "UNBLIND_LOG.txt").read_text()
    assert "git" in log and "branch=" in log


def test_synthetic_artifact_outside_results_needs_no_flag(tmp_path):
    art = make_artifact(tmp_path / "a", K, {})
    res = _run(art, tmp_path)
    assert res["provenance"]["real_artifact"] is False


# ------------------------------------------------- floors and the card diag


def test_floor_hurdle_is_descriptive_and_ratio_reads_as_expected(tmp_path):
    art = make_artifact(tmp_path / "a", K, {})
    s = SD * math.sqrt(K / (K - 1))
    floors = {
        "iso": {"completion": {"sd": s / 2}, "survival_rate": {"sd": s}},
        "joint": {"completion": {"sd": s / 2}, "survival_rate": {"sd": s}},
    }
    fp = tmp_path / "floors.json"
    fp.write_text(json.dumps(floors))
    res = U.run(art, tmp_path / "out", fp, None, unblind=False, allow_dirty=False)
    h = res["beat_reproducibility"]
    assert h["completion"]["ratio_seed_over_floor_iso"] == pytest.approx(2.0)
    assert h["survival_rate"]["ratio_seed_over_floor_joint"] == pytest.approx(1.0)
    # no decision field anywhere in the hurdle
    assert "reject" not in json.dumps(h)


def test_card_diagnostic_is_paired_and_reports_the_interaction(tmp_path):
    here = make_artifact(tmp_path / "a", K, {})
    # other card: ISO shifted −0.01, JOINT shifted +0.02 on seeds 1..12
    bump = {("iso", s): -0.01 for s in range(1, 13)}
    bump.update({("joint", s): 0.02 for s in range(1, 13)})
    other = make_artifact(tmp_path / "b", 46, {}, per_seed_bump=bump)
    res = U.run(here, tmp_path / "out", None, other, unblind=False, allow_dirty=False)
    cd = res["card_diagnostic"]["completion"]
    assert cd["iso"]["mean_diff"] == pytest.approx(0.01)
    assert cd["joint"]["mean_diff"] == pytest.approx(-0.02)
    assert cd["interaction_joint_minus_iso"]["mean"] == pytest.approx(-0.03)
    assert res["card_diagnostic"]["seeds"] == list(range(1, 13))


# ------------------------------------------------- what it never touches


def test_module_reads_no_real_artifact_at_import_or_in_tests():
    """Belt and braces: the module has no literal path into a results dir."""
    src = Path(U.__file__).read_text()
    body = "\n".join(
        ln
        for ln in src.splitlines()
        if not ln.lstrip().startswith("#") and "USAGE" not in ln
    )
    # the docstring shows the command; executable code must not hardcode it
    code = body.split('"""')[-1]
    assert "g1_conf_5090" not in code and "g1_grid" not in code


def test_t_honesty_line_is_close_to_the_true_t_quantile():
    """t_{142} two-sided at the Šidák α is ~2.26; the expansion must land there."""
    assert U._t_crit_two_sided(142) == pytest.approx(2.262, abs=0.005)
    assert U._t_crit_two_sided(10**9) == pytest.approx(U.Z_ALPHA, abs=1e-6)


def test_family_and_secondary_partition_metrics():
    assert set(U.FAMILY) | set(U.SECONDARY) == set(METRICS)
    assert not set(U.FAMILY) & set(U.SECONDARY)
    assert statistics.mean([1, 2]) == 1.5  # keep the import honest
