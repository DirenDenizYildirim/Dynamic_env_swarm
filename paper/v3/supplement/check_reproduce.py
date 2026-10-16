"""Check (e) REPRODUCE: inside the unpacked supplement, the registered analysis
scripts recompute the committed confirmatory, follow-up and secondary outputs.

    .venv/bin/python paper/v3/supplement/check_reproduce.py --workdir DIR

DIR is the directory check_tests.py unpacked and synced (it holds
che_supplement/ with its .venv). Runs, with outputs to DIR/repro/:

  p6_unblind          -> compared with che/bench/results/phase6/unblind/
  p6_post_analysis x2 -> compared with .../phase6/post_unblind_analysis/
  p6_secondary        -> compared with .../phase6/secondary/

JSON is compared exactly except the provenance keys git_commit,
git_dirty_files and timestamp; Markdown exactly except its provenance header
line (the one carrying "dirty files"). Exit 0 = PASS, 1 = FAIL.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

P6 = "che/bench/results/phase6"
IGNORE_KEYS = {"git_commit", "git_dirty_files", "timestamp"}
RUNS = (
    (
        "unblind",
        [
            "che.scripts.p6_unblind",
            "--artifact",
            f"{P6}/g1_conf_5090",
            "--floors",
            f"{P6}/g1_floors_5090/floors.json",
            "--card-diag",
            f"{P6}/g1_grid",
            "--unblind",
            "--allow-dirty",
        ],
    ),
    (
        "post",
        [
            "che.scripts.p6_post_analysis",
            "--sections",
            "gamma4",
            "t2000",
            "--allow-dirty",
        ],
    ),
    (
        "post",
        [
            "che.scripts.p6_post_analysis",
            "--sections",
            "evalfloor",
            "gamma_t",
            "high",
            "--allow-dirty",
        ],
    ),
    ("secondary", ["che.scripts.p6_secondary", "--allow-dirty"]),
)
COMPARE = (
    ("unblind", "unblind", ("unblind.json", "report.md")),
    (
        "post",
        "post_unblind_analysis",
        (
            "post_gamma4_t2000.json",
            "post_gamma4_t2000.md",
            "post_evalfloor_gamma_t_high.json",
            "post_evalfloor_gamma_t_high.md",
        ),
    ),
    ("secondary", "secondary", ("secondary.json", "secondary.md")),
)


def strip(o):
    if isinstance(o, dict):
        return {k: strip(v) for k, v in o.items() if k not in IGNORE_KEYS}
    if isinstance(o, list):
        return [strip(v) for v in o]
    return o


def md_lines(p: Path) -> list[str]:
    return [ln for ln in p.read_text().splitlines() if "dirty files" not in ln]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workdir", type=Path, required=True)
    a = ap.parse_args(argv)
    root = a.workdir / "che_supplement"
    repro = a.workdir / "repro"
    if repro.exists():
        raise SystemExit(f"{repro} exists; use a fresh workdir")
    env = {
        k: v
        for k, v in os.environ.items()
        if k not in ("VIRTUAL_ENV", "UV_PROJECT_ENVIRONMENT", "PYTHONPATH")
    }
    ok = True
    for out, cmd in RUNS:
        r = subprocess.run(
            [
                "uv",
                "run",
                "--no-sync",
                "python",
                "-m",
                cmd[0],
                *cmd[1:],
                "--out",
                str(repro / out),
            ],
            cwd=root,
            env=env,
            capture_output=True,
            text=True,
        )
        print(
            f"{cmd[0]} {' '.join(c for c in cmd[1:] if not c.startswith('che/'))}: "
            f"exit {r.returncode}"
        )
        if r.returncode != 0:
            print(r.stderr[-2000:])
            ok = False
    for out, committed, names in COMPARE:
        for n in names:
            new, old = repro / out / n, root / P6 / committed / n
            if not new.is_file():
                print(f"  {committed}/{n}: NOT PRODUCED")
                ok = False
                continue
            if n.endswith(".json"):
                same = strip(json.loads(new.read_text())) == strip(
                    json.loads(old.read_text())
                )
            else:
                same = md_lines(new) == md_lines(old)
            print(
                f"  {committed}/{n}: {'identical' if same else 'DIFFERS'} "
                f"(provenance fields excluded)"
            )
            ok &= same
    print(f"REPRODUCE CHECK: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
