"""Check (c) TESTS: the CPU test suite passes INSIDE the unpacked supplement.

    .venv/bin/python paper/v3/supplement/check_tests.py --workdir DIR [--zip ...]

Unzips into DIR (must not exist), builds a fresh environment from the SHIPPED
pyproject.toml/uv.lock (`uv sync --python 3.12 --group dev --locked`), and runs
`pytest -vv -rs che/tests` there; a run still going after --timeout-s is
killed and FAILS, naming the test it hung in. Records pass/fail/skip counts,
every skip reason, and wall times in DIR/check_tests.json and the console.
DIR is kept so
check_reproduce.py can reuse the environment.

Exit 0 = PASS (no failure, no error), 1 = FAIL.
"""

from __future__ import annotations

import argparse
import json
import os
import signal
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]


def clean_env() -> dict:
    env = {
        k: v
        for k, v in os.environ.items()
        if k not in ("VIRTUAL_ENV", "UV_PROJECT_ENVIRONMENT", "PYTHONPATH")
    }
    env["JAX_PLATFORMS"] = "cpu"
    return env


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--zip", type=Path, default=REPO / "paper/v3/out/che_supplement.zip"
    )
    ap.add_argument("--workdir", type=Path, required=True)
    ap.add_argument("--pytest-args", nargs="*", default=[])
    ap.add_argument(
        "--timeout-s",
        type=int,
        default=7200,
        help="kill the suite after this wall time and FAIL (a hang is a finding)",
    )
    a = ap.parse_args(argv)
    if a.workdir.exists():
        raise SystemExit(f"--workdir {a.workdir} exists; give a fresh path")
    a.workdir.mkdir(parents=True)
    with zipfile.ZipFile(a.zip) as z:
        z.extractall(a.workdir)
    root = a.workdir / "che_supplement"
    env = clean_env()

    t0 = time.time()
    sync = subprocess.run(
        ["uv", "sync", "--python", "3.12", "--group", "dev", "--locked"],
        cwd=root,
        env=env,
        capture_output=True,
        text=True,
    )
    t_sync = time.time() - t0
    print(f"uv sync: exit {sync.returncode} in {t_sync:.0f} s")
    if sync.returncode != 0:
        print(sync.stdout[-3000:], sync.stderr[-3000:])
        print("TESTS CHECK: FAIL (environment did not build)")
        return 1

    junit = a.workdir / "junit.xml"
    out_txt = a.workdir / "pytest_output.txt"
    cmd = [
        "uv",
        "run",
        "--no-sync",
        "pytest",
        "-vv",  # pyproject addopts has -q; -vv nets one test per line
        "-rs",
        "-p",
        "no:cacheprovider",
        f"--junitxml={junit}",
        "che/tests",
        *a.pytest_args,
    ]
    t0 = time.time()
    with open(out_txt, "w") as fh:
        proc = subprocess.Popen(
            cmd,
            cwd=root,
            env=env,
            stdout=fh,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
        try:
            rc = proc.wait(timeout=a.timeout_s)
            hung = False
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid, signal.SIGKILL)
            proc.wait()
            rc, hung = -9, True
    t_test = time.time() - t0
    lines = [ln for ln in out_txt.read_text().splitlines() if ln.strip()]
    print("\n".join(lines[-25:]))
    if hung or not junit.is_file():
        running = next((ln for ln in reversed(lines) if "test_" in ln), "?")
        rec = {
            "pytest_wall_s": round(t_test, 1),
            "hung": hung,
            "exit": rc,
            "last_test_line": running,
            "tests_reported_done": sum(
                " PASSED" in ln or " SKIPPED" in ln or " FAILED" in ln for ln in lines
            ),
        }
        (a.workdir / "check_tests.json").write_text(json.dumps(rec, indent=1) + "\n")
        print(json.dumps(rec, indent=1))
        why = f"no exit within {a.timeout_s} s" if hung else "no junit report"
        print(f"TESTS CHECK: FAIL ({why})")
        return 1
    run = subprocess.CompletedProcess(cmd, rc)

    suite = ET.parse(junit).getroot()
    suite = suite if suite.tag == "testsuite" else suite.find("testsuite")
    counts = {
        k: int(suite.get(k, 0)) for k in ("tests", "failures", "errors", "skipped")
    }
    counts["passed"] = (
        counts["tests"] - counts["failures"] - counts["errors"] - counts["skipped"]
    )
    skips, failed = [], []
    for tc in suite.iter("testcase"):
        name = f"{tc.get('classname')}::{tc.get('name')}"
        s = tc.find("skipped")
        if s is not None:
            skips.append(f"{name}: {s.get('message')}")
        if tc.find("failure") is not None or tc.find("error") is not None:
            failed.append(name)
    rec = {
        "uv_sync_exit": sync.returncode,
        "uv_sync_s": round(t_sync, 1),
        "pytest_exit": run.returncode,
        "pytest_wall_s": round(t_test, 1),
        **counts,
        "skips": skips,
        "failed": failed,
    }
    (a.workdir / "check_tests.json").write_text(json.dumps(rec, indent=1) + "\n")
    print(json.dumps({k: v for k, v in rec.items() if k not in ("skips",)}, indent=1))
    print("skips:")
    for s in skips:
        print("   ", s)
    ok = run.returncode == 0 and counts["failures"] == 0 and counts["errors"] == 0
    print(f"TESTS CHECK: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
