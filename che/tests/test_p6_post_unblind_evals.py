"""The post-unblind evaluation stage: refuses before the unblind step, plans
exactly the registered evals, declares every cross-config eval, and touches
neither METRICS nor the grid script."""

from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "che" / "scripts" / "run_p6_post_unblind_evals.sh"
GRID = REPO_ROOT / "che" / "scripts" / "run_p6_grid.sh"


def _run(tmp: Path, marker: bool, **env) -> subprocess.CompletedProcess:
    skip = ("OUT_", "BLOCKS", "K_")
    e = {k: v for k, v in os.environ.items() if not k.startswith(skip)}
    m = tmp / "UNBLIND_LOG.txt"
    if marker:
        m.write_text("2026-01-01T00:00:00+00:00  git deadbeef  branch=C\n")
    e.update({"UNBLIND_MARKER": str(m), "DRY_RUN": "1", **env})
    return subprocess.run(
        ["bash", str(SCRIPT)], cwd=REPO_ROOT, capture_output=True, text=True, env=e
    )


def test_refuses_before_the_unblind_step(tmp_path):
    r = _run(tmp_path, marker=False)
    assert r.returncode == 1
    assert "POST-UNBLIND" in r.stderr and "must not run" in r.stderr


def test_empty_marker_is_not_a_marker(tmp_path):
    (tmp_path / "UNBLIND_LOG.txt").write_text("")
    r = _run(tmp_path, marker=False)
    assert r.returncode == 1


def _stems(r):
    return [ln.split()[0] for ln in r.stdout.splitlines() if ln.startswith("eval")]


def test_gamma_t_block_is_the_final_half_on_both_confirmatory_arms(tmp_path):
    r = _run(tmp_path, marker=True, BLOCKS="gamma_t")
    assert r.returncode == 0, r.stderr
    stems = _stems(r)
    assert len(stems) == 2 * 72 * 10 == 1440
    steps = {int(re.search(r"_u(\d+)$", s).group(1)) for s in stems}
    # updates 500..950; 1000 is the grid's own eval
    assert steps == set(range(500, 1000, 50))
    assert sum(s.startswith("eval_iso_s") for s in stems) == 720
    assert "eval_joint_s72_u950" in stems


def test_high_readout_covers_conf_iso4_and_the_floor_reps(tmp_path):
    r = _run(tmp_path, marker=True, BLOCKS="high")
    assert r.returncode == 0, r.stderr
    stems = _stems(r)
    assert len(stems) == 144 + 20 + 16 == 180
    high = [ln for ln in r.stdout.splitlines() if ln.startswith("evalhigh")]
    assert all("step=1000" in ln for ln in high)
    assert all("joint_high.yaml" in ln for ln in high)
    assert "evalhigh_iso4_s20" in stems and "evalhigh_joint_rep8" in stems


def test_evalfloor_is_repeated_evals_of_the_same_checkpoint(tmp_path):
    r = _run(tmp_path, marker=True, BLOCKS="evalfloor")
    assert r.returncode == 0, r.stderr
    stems = _stems(r)
    want = [
        f"evalfloor_{t}_rep{i}" for t in ("iso_s1", "joint_s1") for i in range(1, 5)
    ]
    assert stems == want


def test_default_is_all_three_blocks(tmp_path):
    r = _run(tmp_path, marker=True)
    assert r.returncode == 0, r.stderr
    assert "planned: 1628" in r.stdout  # 1440 + 180 + 8


def test_every_eval_is_declared_and_at_an_explicit_step():
    body = "\n".join(
        ln for ln in SCRIPT.read_text().splitlines() if not ln.lstrip().startswith("#")
    )
    assert "--allow-hash" in body and "--step" in body
    assert "ckpt_step" in body  # the written step is re-asserted


def test_computes_no_contrast_and_leaves_the_grid_script_alone():
    body = "\n".join(
        ln for ln in SCRIPT.read_text().splitlines() if not ln.lstrip().startswith("#")
    )
    for forbidden in ("m62_report", "p6_unblind", "floors.json", "METRICS"):
        assert forbidden not in body
    grid = "\n".join(
        ln for ln in GRID.read_text().splitlines() if not ln.lstrip().startswith("#")
    )
    assert "post_unblind" not in grid


def test_outputs_go_to_their_own_directories():
    txt = SCRIPT.read_text()
    outs = re.findall(r"^OUT_\w+=\$\{OUT_\w+:-([^}]+)\}", txt, re.M)
    assert len(outs) == 3 and len(set(outs)) == 3
    for o in outs:
        assert o.startswith("che/bench/results/phase6/post_")
