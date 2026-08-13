"""The G1.3 grid layout, asserted before $41 of GPU time is spent on it.

`run_p6_grid.sh` is the phase's headline spend and it runs unattended for
~33 hours on a rented box. Three classes of defect are cheap to catch here and
expensive to catch there:

  1. THE LAYOUT DISAGREEING WITH THE LOCKS. k is a registered analysis constant
     (`docs/locks.yaml`: K_CONFIRMATORY, K_SECONDARY). A script default that
     drifts from it produces a grid whose power statement is about a different
     design than the one that ran -- and nothing would go red, which is the
     failure mode the locks-are-enforced-by-test rule exists for.

  2. SEED 0 REACHING THE GRID. The floor runs are seed 0. A grid run at seed 0
     on iso, joint or sweep_c50_p500 is the same config at the same seed for
     the same T as a floor rep: a reproducibility rep contributing zero seed
     variance to the arm dispersion the confirmatory test divides by.

  3. AN ANALYSIS CALL REACHING THE BOX. NO-PEEKING is in force until
     unblinding; the grid script must compute no cross-arm quantity.

The parameter-identity guard is driven through bash, because it is the guard
that replaces the floor script's refuse-nonempty protection under resume and a
resume that silently merges two artifacts is unrecoverable after the fact.
"""

from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "che" / "scripts" / "run_p6_grid.sh"
LOCKS_PATH = REPO_ROOT / "docs" / "locks.yaml"
TAG_RE = r"[a-z0-9_]+_s\d+"


def _analysis_constants() -> dict:
    with open(LOCKS_PATH) as f:
        return yaml.safe_load(f)["analysis"]["constants"]


ANALYSIS = _analysis_constants()


def _script_default(name: str) -> str:
    """Read a `NAME=${NAME:-value}` default out of the script."""
    m = re.search(rf"^{name}=\$\{{{name}:-([^}}]*)\}}", SCRIPT.read_text(), re.M)
    assert m, f"no default for {name} in {SCRIPT.name}"
    return m.group(1)


def _dry_run(**env) -> subprocess.CompletedProcess:
    e = dict(os.environ, DRY_RUN="1", **env)
    return subprocess.run(
        ["bash", str(SCRIPT)], cwd=REPO_ROOT, capture_output=True, text=True, env=e
    )


@pytest.fixture(scope="module")
def tags() -> list[str]:
    r = _dry_run()
    assert r.returncode == 0, r.stderr
    return [ln for ln in r.stdout.splitlines() if re.fullmatch(TAG_RE, ln)]


# --------------------------------------------------------------- the locks

def test_seed_counts_come_from_the_locks_not_from_the_script():
    """k is locked. The script may parameterize it; its default must be it."""
    assert int(_script_default("K_CONF")) == ANALYSIS["K_CONFIRMATORY"]["value"]
    assert int(_script_default("K_SEC")) == ANALYSIS["K_SECONDARY"]["value"]


def test_updates_default_is_t_star():
    assert int(_script_default("UPDATES")) == ANALYSIS["T_STAR"]["value"]


def test_k_conf_may_be_raised_to_the_ladder_cap(tags):
    """Ladder branch B raises k with no round-trip, so K_CONF must be live."""
    cap = ANALYSIS["K_LADDER_CAP"]["value"]
    r = _dry_run(K_CONF=str(cap))
    assert r.returncode == 0, r.stderr
    raised = [ln for ln in r.stdout.splitlines() if re.fullmatch(TAG_RE, ln)]
    assert len(raised) == len(tags) + 2 * (cap - ANALYSIS["K_CONFIRMATORY"]["value"])


# -------------------------------------------------------------- the layout

def test_grid_is_240_runs(tags):
    assert len(tags) == 240


def test_arm_composition(tags):
    by_arm: dict[str, list[int]] = {}
    for t in tags:
        arm, seed = t.rsplit("_s", 1)
        by_arm.setdefault(arm, []).append(int(seed))

    conf = {"iso", "joint"}
    sweep = {f"sweep_c50_p{p}" for p in ("000", "125", "250", "375", "500")}
    ident = {f"ident_c40_p{p}" for p in ("000", "200", "400")}
    assert set(by_arm) == conf | sweep | ident

    k_conf = ANALYSIS["K_CONFIRMATORY"]["value"]
    k_sec = ANALYSIS["K_SECONDARY"]["value"]
    for arm in conf:
        assert sorted(by_arm[arm]) == list(range(1, k_conf + 1))
    for arm in sweep | ident:
        assert sorted(by_arm[arm]) == list(range(1, k_sec + 1))


def test_every_arm_uses_the_same_seed_integers(tags):
    """Shared integers put any induced cross-arm covariance on the safe side
    of the registered UNPAIRED sd(Gamma) -- see the script's decision (a)."""
    by_arm: dict[str, set[int]] = {}
    for t in tags:
        arm, seed = t.rsplit("_s", 1)
        by_arm.setdefault(arm, set()).add(int(seed))
    k_sec = ANALYSIS["K_SECONDARY"]["value"]
    for arm, seeds in by_arm.items():
        common = set(range(1, k_sec + 1))
        assert common <= seeds, f"{arm} does not share the common seed block"


def test_seed_zero_never_appears(tags):
    """Seed 0 is the FLOOR seed. A grid run at 0 is a rep, not a draw."""
    assert not [t for t in tags if t.endswith("_s0")]


def test_run_order_is_seed_major(tags):
    """Truncation must cost power, not validity: a box lost at 60 % should
    leave a smaller BALANCED design, not a complete arm and an empty one."""
    seeds = [int(t.rsplit("_s", 1)[1]) for t in tags]
    assert seeds == sorted(seeds), "arm-major ordering: an interruption voids Gamma"
    # Within the common block every arm appears once before any seed advances.
    first_block = [
        t.rsplit("_s", 1)[0] for t, s in zip(tags, seeds, strict=True) if s == 1
    ]
    assert len(first_block) == len(set(first_block)) == 10


def test_chunks_of_60_land_on_seed_boundaries(tags):
    """MAX_RUNS=60 runs the grid in quarters. Each quarter must be a whole
    block of seeds: a chunk that split a seed would leave ISO and JOINT for
    that seed on different rented cards, and the card effect only cancels in
    Γ because both arms of a seed share one."""
    seeds = [int(t.rsplit("_s", 1)[1]) for t in tags]
    for c in range(4):
        block = seeds[c * 60 : (c + 1) * 60]
        assert len(block) == 60
        before = seeds[: c * 60]
        after = seeds[(c + 1) * 60 :]
        # No seed may appear both inside this chunk and outside it.
        assert not (set(block) & set(before)), f"chunk {c + 1} resumes a prior seed"
        assert not (set(block) & set(after)), f"chunk {c + 1} splits a seed"


def test_configs_referenced_all_exist(tags):
    for t in tags:
        arm = t.rsplit("_s", 1)[0]
        assert (REPO_ROOT / "che" / "configs" / f"p6_{arm}.yaml").is_file()


# --------------------------------------------------------------- no peeking

def test_script_computes_no_cross_arm_quantity():
    # Executable lines only. The script's header DISCUSSES m62_report, at
    # length, in order to say it must never be called here -- a comment cannot
    # peek, and a rule that forbids naming the thing it forbids is unwritable.
    body = "\n".join(
        ln for ln in SCRIPT.read_text().splitlines() if not ln.lstrip().startswith("#")
    )
    for forbidden in ("m62_report", "--unblind", "floors.json"):
        assert forbidden not in body, (
            f"{forbidden!r} in the grid script: Gamma is a cross-arm quantity "
            "and NO-PEEKING binds until unblinding"
        )


def test_eval_set_is_a_common_constant():
    """Same eval draw as the floor protocol, so floors and grid are one
    instrument and cross-run variance is training-seed variance."""
    assert int(_script_default("EVAL_SEED")) == 0
    assert int(_script_default("N_EVAL")) == 512
    assert _script_default("THETA_STAR") == "che/configs/theta_star_holdout.yaml"


# ------------------------------------------------- the resume-safety guard

def _run_until_stamp_check(out: Path, **env) -> subprocess.CompletedProcess:
    """Invoke the real script far enough to hit the stamp guard, then stop at
    the pre-flight -- pointed at a nonexistent file so it fails immediately and
    no GPU-shaped work is attempted."""
    e = dict(
        os.environ, OUT=str(out), OWED_TESTS="che/tests/__no_such_file__.py", **env
    )
    return subprocess.run(
        ["bash", str(SCRIPT)], cwd=REPO_ROOT, capture_output=True, text=True, env=e
    )


def test_resume_with_matching_parameters_is_allowed(tmp_path):
    out = tmp_path / "grid"
    first = _run_until_stamp_check(out)
    assert (out / "grid_params.txt").is_file(), first.stderr
    second = _run_until_stamp_check(out)
    assert "Resuming into" in second.stdout, second.stdout + second.stderr
    assert "DIFFERENT grid parameters" not in second.stderr


@pytest.mark.parametrize(
    "changed", [{"UPDATES": "500"}, {"K_CONF": "20"}, {"EVAL_SEED": "7"}]
)
def test_resume_with_changed_parameters_is_refused(tmp_path, changed):
    """Floors and dispersions are PER-ARTIFACT. Resuming into a directory built
    under different parameters merges two artifacts into one, and the merged
    per-arm dispersion grades nothing."""
    out = tmp_path / "grid"
    _run_until_stamp_check(out)
    r = _run_until_stamp_check(out, **changed)
    assert r.returncode == 1
    assert "DIFFERENT grid parameters" in r.stderr


def test_stamp_records_the_arm_set(tmp_path):
    """An arm added or dropped mid-grid is the same merge defect."""
    out = tmp_path / "grid"
    _run_until_stamp_check(out)
    r = _run_until_stamp_check(
        out, SEC_ARMS="sweep_c50_p000:che/configs/p6_sweep_c50_p000.yaml"
    )
    assert r.returncode == 1
    assert "DIFFERENT grid parameters" in r.stderr


# ------------------------------------------------------------- end to end

# The script runs unattended for ~33 hours on a rented box. Every control path
# below -- train, cross-config eval, archive, manifest, skip-on-resume, the
# completeness assertion -- is exercised here on `debug.yaml` at 2 updates, on
# CPU, for about a minute. A typo in any of them costs a rental to discover.
SMOKE = dict(
    UPDATES="2",
    K_CONF="2",
    K_SEC="1",
    N_EVAL="4",
    MIN_FREE_GB="0",
    CONF_ARMS="iso:che/configs/debug.yaml",
    SEC_ARMS="sweep_c50_p000:che/configs/debug.yaml",
    THETA_STAR="che/configs/debug.yaml",
    # A real but trivial test file: the pre-flight must genuinely run and pass,
    # not be bypassed. There is deliberately no skip switch in the script.
    OWED_TESTS="che/tests/test_p6_grid.py::test_seed_counts_come_from_the_locks_not_from_the_script",
)


def _smoke(out: Path, **over) -> subprocess.CompletedProcess:
    e = dict(os.environ, OUT=str(out), **SMOKE, **over)
    return subprocess.run(
        ["bash", str(SCRIPT)], cwd=REPO_ROOT, capture_output=True, text=True, env=e
    )


@pytest.mark.slow
def test_end_to_end_runs_archives_and_resumes(tmp_path):
    out = tmp_path / "grid"
    r = _smoke(out)
    assert r.returncode == 0, r.stdout[-4000:] + r.stderr[-4000:]

    tags = ["iso_s1", "sweep_c50_p000_s1", "iso_s2"]
    for tag in tags:
        assert (out / f"eval_{tag}.json").is_file(), f"{tag} produced no eval"
        assert (out / f"ckpt_{tag}.tar.zst").is_file(), f"{tag} was not archived"
        assert (out / ".manifest" / f"{tag}.done").is_file()
        # Redundant with a hash-verified archive, and 240 of them will not fit.
        assert not (out / f"ckpt_{tag}").exists(), "raw ckpt dir not reclaimed"

    # SHA256_CKPT.txt is DERIVED from the keyed entries, never appended.
    lines = (out / "SHA256_CKPT.txt").read_text().splitlines()
    assert len(lines) == len(tags)
    assert "OK: 3 runs complete and verified." in r.stdout
    assert "DO NOT UNBLIND" in r.stdout

    prov = (out / "provenance.txt").read_text()
    assert "ran_this_invocation: 3" in prov
    assert "skipped_complete: 0" in prov

    # Resume: everything is complete, so a second invocation trains nothing and
    # the aggregate does not grow a duplicate line.
    r2 = _smoke(out)
    assert r2.returncode == 0, r2.stdout[-4000:] + r2.stderr[-4000:]
    assert r2.stdout.count("complete and verified") >= len(tags)
    assert "ran_this_invocation: 0" in (out / "provenance.txt").read_text()
    assert (out / "SHA256_CKPT.txt").read_text().splitlines() == lines


@pytest.mark.slow
def test_max_runs_pauses_at_a_seed_boundary_and_resumes(tmp_path):
    """A chunked run must (a) stop cleanly with exit 0 — a planned pause is not
    a failure — (b) overrun MAX_RUNS rather than split a seed, and (c) resume
    into exactly the remaining runs."""
    out = tmp_path / "grid"
    # SMOKE has 2 arms; MAX_RUNS=1 is reached mid-seed 1, so the loop must
    # finish seed 1 (2 runs) before stopping rather than stopping at 1.
    r = _smoke(out, MAX_RUNS="1")
    assert r.returncode == 0, r.stdout[-3000:] + r.stderr[-3000:]
    assert "CHUNK COMPLETE" in r.stdout
    assert "SEED BOUNDARY" in r.stdout

    done = sorted(p.name for p in (out / ".manifest").glob("*.done"))
    assert done == ["iso_s1.done", "sweep_c50_p000_s1.done"], done
    assert not (out / "eval_iso_s2.json").exists()

    # Resume: the remaining run completes and the grid closes green.
    r2 = _smoke(out)
    assert r2.returncode == 0, r2.stdout[-3000:] + r2.stderr[-3000:]
    assert "G1.3 COMPLETE" in r2.stdout
    assert "ran_this_invocation: 1" in (out / "provenance.txt").read_text()


@pytest.mark.slow
def test_provenance_accumulates_across_invocations(tmp_path):
    """`tee` would erase which card ran the earlier chunks the moment a second
    invocation started, and on a multi-card grid that record IS the audit
    trail. Latent even without chunking: every resume overwrote it."""
    out = tmp_path / "grid"
    assert _smoke(out, MAX_RUNS="1").returncode == 0
    first = (out / "provenance.txt").read_text()
    assert first.count("run: G1.3") == 1

    assert _smoke(out).returncode == 0
    second = (out / "provenance.txt").read_text()
    assert second.count("run: G1.3") == 2, "provenance was overwritten, not appended"
    assert second.startswith(first), "the earlier invocation's record was altered"


@pytest.mark.slow
def test_card_block_structure_is_recorded_per_run(tmp_path):
    """One card per seed is what makes the common-mode cancellation argument
    checkable rather than assumed, so it is recorded per run and derived."""
    out = tmp_path / "grid"
    assert _smoke(out).returncode == 0
    cards = sorted(p.name for p in (out / ".manifest").glob("*.card"))
    assert cards == ["iso_s1.card", "iso_s2.card", "sweep_c50_p000_s1.card"]
    summary = (out / "cards.txt").read_text()
    assert summary.startswith("# card")
    # One row per (card, arm); iso ran two seeds on the one card here.
    assert "\tiso\t2\t" in summary


@pytest.mark.slow
def test_an_orphaned_eval_is_refused(tmp_path):
    """The post-unblind analysis finds eval JSONs by glob. One left behind by a
    run that died between its eval and its manifest entry would enter that
    analysis as a completed run, with no archive to audit it against."""
    out = tmp_path / "grid"
    assert _smoke(out).returncode == 0
    (out / "eval_iso_s99.json").write_text('{"ckpt_step": 2}')

    r = _smoke(out)
    assert r.returncode == 1
    assert "ORPHANED EVAL" in r.stderr
    assert "eval_iso_s99.json" in r.stderr


@pytest.mark.slow
def test_a_corrupted_archive_is_re_run_not_trusted(tmp_path):
    """Existence is not integrity: a truncated archive from a run killed
    mid-tar must not read as a finished run on resume."""
    out = tmp_path / "grid"
    assert _smoke(out).returncode == 0
    (out / "ckpt_iso_s2.tar.zst").write_bytes(b"truncated")

    r = _smoke(out)
    assert r.returncode == 0, r.stdout[-4000:] + r.stderr[-4000:]
    assert "ran_this_invocation: 1" in (out / "provenance.txt").read_text()
    assert (out / "ckpt_iso_s2.tar.zst").read_bytes() != b"truncated"
