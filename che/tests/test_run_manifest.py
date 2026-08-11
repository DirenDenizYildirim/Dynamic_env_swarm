"""The grid's resume story must cost <= 1 run per interruption, and must not
pass while a run is absent (T* ruling 2026-08-11, item 8 + builder hardening).

These drive `che/scripts/lib_run_manifest.sh` through bash. The two tests that
matter most are the regression tests for defects the existing floor script
still has, and which the naive resume implementation would inherit:

  (a) APPEND IS NOT IDEMPOTENT. `sha256sum | tee -a` plus a `wc -l` count
      assertion passes when one run is missing and another is duplicated.
  (b) EXISTENCE IS NOT INTEGRITY. A truncated archive from a run killed
      mid-tar satisfies "the archive and its hash exist".
"""

from __future__ import annotations

import subprocess
import textwrap

import pytest

LIB = "che/scripts/lib_run_manifest.sh"


def sh(script: str, cwd) -> subprocess.CompletedProcess:
    """Run a bash snippet with the library sourced, from the repo root."""
    import os

    body = f'set -uo pipefail\nsource "{os.path.abspath(LIB)}"\n' + textwrap.dedent(
        script
    )
    return subprocess.run(
        ["bash", "-c", body], cwd=cwd, capture_output=True, text=True
    )


@pytest.fixture
def out(tmp_path):
    """An OUT dir holding two finished checkpoint dirs, ready to record."""
    d = tmp_path / "grid"
    for tag in ("iso_rep1", "iso_rep2"):
        ck = d / f"ckpt_{tag}"
        ck.mkdir(parents=True)
        (ck / "params.msgpack").write_bytes(b"weights-for-" + tag.encode())
    return d


def test_incomplete_run_is_not_complete(out, tmp_path):
    r = sh(f'manifest_complete "{out}" iso_rep1 && echo YES || echo NO', tmp_path)
    assert r.stdout.strip() == "NO"


def test_recorded_run_is_complete_and_skippable(out, tmp_path):
    r = sh(
        f"""
        manifest_record "{out}" iso_rep1 || exit 9
        manifest_complete "{out}" iso_rep1 && echo YES || echo NO
        """,
        tmp_path,
    )
    assert r.stdout.strip() == "YES", r.stderr
    assert (out / "ckpt_iso_rep1.tar.zst").exists()


# ------------------------------------------------- (b) existence != integrity


def test_truncated_archive_is_not_complete(out, tmp_path):
    """A run killed mid-tar must re-run, not be skipped.

    This is the test the `[ -s "$archive" ]` check alone would fail: the file
    exists and is non-empty, but it is not the artifact that was hashed.
    """
    sh(f'manifest_record "{out}" iso_rep1', tmp_path)
    archive = out / "ckpt_iso_rep1.tar.zst"
    data = archive.read_bytes()
    archive.write_bytes(data[: len(data) // 2])  # truncate, as a kill would

    r = sh(f'manifest_complete "{out}" iso_rep1 && echo YES || echo NO', tmp_path)
    assert r.stdout.strip() == "NO", (
        "a truncated archive was accepted as a finished run; the manifest is "
        "checking existence rather than integrity"
    )


def test_crash_before_the_entry_leaves_the_run_incomplete(out, tmp_path):
    """Ordering guarantee: the entry is written last, so a crash never lies.

    Simulated by removing the entry while leaving a valid archive behind --
    exactly the state a kill between `mv` and the entry write would produce.
    """
    sh(f'manifest_record "{out}" iso_rep1', tmp_path)
    (out / ".manifest" / "iso_rep1.done").unlink()
    r = sh(f'manifest_complete "{out}" iso_rep1 && echo YES || echo NO', tmp_path)
    assert r.stdout.strip() == "NO"


def test_no_temp_files_survive_a_successful_record(out, tmp_path):
    sh(f'manifest_record "{out}" iso_rep1', tmp_path)
    assert not list(out.glob(".tmp.*")), "a temp archive was left behind"


# ------------------------------------------------- (a) append != idempotent


def test_rerunning_a_tag_does_not_duplicate_its_record(out, tmp_path):
    """The defect that makes a count assertion pass with a run missing.

    Under `tee -a`, recording iso_rep1 twice leaves two lines. Combined with a
    genuinely missing iso_rep2 the total still equals the expected count, and
    the assertion passes while a run is absent.
    """
    sh(
        f"""
        manifest_record "{out}" iso_rep1
        manifest_record "{out}" iso_rep1
        manifest_record "{out}" iso_rep1
        manifest_write_aggregate "{out}"
        """,
        tmp_path,
    )
    lines = (out / "SHA256_CKPT.txt").read_text().splitlines()
    assert len(lines) == 1, f"a tag contributed {len(lines)} records: {lines}"


def test_a_missing_run_fails_even_when_the_count_would_match(out, tmp_path):
    """The exact scenario spelled out above, asserted end to end."""
    r = sh(
        f"""
        manifest_record "{out}" iso_rep1
        manifest_record "{out}" iso_rep1
        manifest_write_aggregate "{out}"
        manifest_assert_all "{out}" iso_rep1 iso_rep2 && echo PASSED || echo FAILED
        """,
        tmp_path,
    )
    assert r.stdout.strip().endswith("FAILED"), (
        "the assertion passed with iso_rep2 absent -- this is the count-based "
        "defect the keyed manifest exists to prevent"
    )
    assert "iso_rep2" in r.stderr


def test_aggregate_is_derived_not_appended(out, tmp_path):
    """Rebuilding twice must not grow the file."""
    r = sh(
        f"""
        manifest_record "{out}" iso_rep1
        manifest_record "{out}" iso_rep2
        manifest_write_aggregate "{out}"
        manifest_write_aggregate "{out}"
        manifest_write_aggregate "{out}"
        wc -l < "{out}/SHA256_CKPT.txt"
        """,
        tmp_path,
    )
    assert r.stdout.strip().endswith("2"), r.stdout


def test_all_complete_reports_ok(out, tmp_path):
    r = sh(
        f"""
        manifest_record "{out}" iso_rep1
        manifest_record "{out}" iso_rep2
        manifest_assert_all "{out}" iso_rep1 iso_rep2
        """,
        tmp_path,
    )
    assert "OK: 2 runs complete and verified." in r.stdout, r.stderr


def test_aggregate_verifies_with_sha256sum_c(out, tmp_path):
    """The file we ship must be checkable by the standard tool, as M6.2b's was."""
    r = sh(
        f"""
        manifest_record "{out}" iso_rep1
        manifest_record "{out}" iso_rep2
        manifest_write_aggregate "{out}"
        sha256sum -c "{out}/SHA256_CKPT.txt"
        """,
        tmp_path,
    )
    assert r.returncode == 0, r.stdout + r.stderr
    assert r.stdout.count(": OK") == 2
