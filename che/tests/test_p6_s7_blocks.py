"""The §7 blocks job script: layout, locks, no peeking, and the science-tree
identity the ruling requires (`git diff 51e489a..HEAD -- che/env che/train
che/eval` empty). The identity is asserted HERE, locally, because the box has
no .git; the script records the base it was shipped against."""

from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "che" / "scripts" / "run_p6_s7_blocks.sh"
GRID = REPO_ROOT / "che" / "scripts" / "run_p6_grid.sh"
LOCKS = yaml.safe_load((REPO_ROOT / "docs" / "locks.yaml").read_text())
ANALYSIS = LOCKS["analysis"]["constants"]
TAG_RE = r"[a-z0-9_]+_s\d+"
FROZEN_BASE = "51e489a031b0e213d18644dbae19fc92052ede82"


def _default(name: str) -> str:
    m = re.search(rf"^{name}=\$\{{{name}:-([^}}]*)\}}", SCRIPT.read_text(), re.M)
    assert m, f"no default for {name}"
    return m.group(1)


def _dry(block: str) -> list[str]:
    e = {k: v for k, v in os.environ.items()
         if not k.startswith(("OUT", "K_", "UPDATES", "CONF_ARMS", "SEC_ARMS"))}
    e.update({"DRY_RUN": "1", "BLOCK": block})
    r = subprocess.run(["bash", str(SCRIPT)], cwd=REPO_ROOT, capture_output=True,
                       text=True, env=e)
    assert r.returncode == 0, r.stderr
    return r.stdout.splitlines()


def test_iso4_layout_is_20_seeds_one_arm():
    lines = _dry("iso4")
    tags = [ln for ln in lines if re.fullmatch(TAG_RE, ln)]
    assert tags == [f"iso4_s{s}" for s in range(1, 21)]
    assert any("updates: 1000" in ln and "k_conf: 20" in ln for ln in lines)


def test_t2000_layout_is_4_seeds_two_arms_at_2000():
    lines = _dry("t2000")
    tags = [ln for ln in lines if re.fullmatch(TAG_RE, ln)]
    want = [t for s in range(1, 5) for t in (f"iso_t2000_s{s}", f"joint_t2000_s{s}")]
    assert tags == want
    assert any("updates: 2000" in ln and "k_conf: 4" in ln for ln in lines)


def test_seed_counts_follow_the_ruling_and_the_locks():
    assert int(_default("K_ISO4")) == ANALYSIS["K_SECONDARY"]["value"] == 20
    assert int(_default("K_T2000")) == 4
    assert int(_default("T2000_UPDATES")) == 2000
    assert _default("SCIENCE_TREE_BASE") == FROZEN_BASE


def test_own_output_directories_never_the_confirmatory_one():
    for name in ("OUT_ISO4", "OUT_T2000"):
        out = _default(name)
        assert out.startswith("che/bench/results/phase6/g1_")
        assert out not in ("che/bench/results/phase6/g1_conf_5090",
                           "che/bench/results/phase6/g1_grid")
    assert _default("OUT_ISO4") != _default("OUT_T2000")


def test_script_computes_no_cross_arm_quantity():
    body = "\n".join(ln for ln in SCRIPT.read_text().splitlines()
                     if not ln.lstrip().startswith("#"))
    for forbidden in ("m62_report", "p6_unblind", "--unblind", "floors.json"):
        assert forbidden not in body


def test_grid_script_is_not_modified_by_this_feature():
    """The ruling: 'The grid script is not modified.' Its no-peeking test and
    its defaults are exercised elsewhere; here, just that it exists and still
    carries no analysis call."""
    body = "\n".join(ln for ln in GRID.read_text().splitlines()
                     if not ln.lstrip().startswith("#"))
    assert "m62_report" not in body and "p6_unblind" not in body


def test_science_tree_identical_to_the_frozen_base():
    """`git diff 51e489a..HEAD -- che/env che/train che/eval` must be empty.
    Skips where there is no .git (the box); that is why the script RECORDS
    rather than asserts, and why this test is in the pre-ship path."""
    if not (REPO_ROOT / ".git").exists():
        pytest.skip("no .git here — identity is asserted before shipping")
    r = subprocess.run(["git", "diff", "--stat", FROZEN_BASE, "HEAD", "--",
                        "che/env", "che/train", "che/eval"],
                       cwd=REPO_ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip() == "", (
        "the science tree differs from the frozen base:\n" + r.stdout)
