"""Check (a) SCRUB: the SHIPPED supplement carries no identifying string.

    .venv/bin/python paper/v3/supplement/check_scrub.py [--zip PATH]

Unpacks the zip into a fresh temporary directory and scans every file (text
line by line; binary files as bytes, and `.npz` members decompressed) and every
path for `rules.FORBIDDEN` patterns (author names, handle, e-mail, repository
name, GitHub / claude.ai URLs, absolute paths, session branch and id, GPU
UUID, IPv4) and for any 7-40 hex token that prefixes a commit of this
repository (`git rev-list --all --reflog`). Any hit is a FAIL. `rules.WARN`
patterns and every URL domain are listed for a human look.

Exit 0 = PASS, 1 = FAIL.
"""

from __future__ import annotations

import argparse
import bisect
import collections
import re
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(HERE))
import rules as R  # noqa: E402

URL = re.compile(r"https?://([A-Za-z0-9.-]+)")
BIN_FORBIDDEN = (
    "name/handle/email",
    "repository name",
    "GitHub URL",
    "claude.ai URL",
    "absolute path",
    "session branch",
    "session id",
    "GPU UUID",
)


def commits() -> list[str]:
    return sorted(
        set(
            subprocess.run(
                ["git", "rev-list", "--all", "--reflog"],
                cwd=REPO,
                capture_output=True,
                text=True,
                check=True,
            ).stdout.split()
        )
    )


def is_commit_prefix(tok: str, cs: list[str]) -> bool:
    i = bisect.bisect_left(cs, tok)
    return i < len(cs) and cs[i].startswith(tok)


def scan(root: Path) -> tuple[list[str], list[str], dict]:
    cs = commits()
    fails: list[str] = []
    warns: list[str] = []
    info = {
        "url_domains": collections.Counter(),
        "workspace_paths": 0,
        "vast_mentions": 0,
        "hidden": [],
        "files": 0,
        "binary": 0,
    }
    forb = [(e[0], e[1], e[2] if len(e) > 2 else None) for e in R.FORBIDDEN]
    tops = {p.name for p in root.iterdir()}
    if tops != {"che_supplement"}:
        fails.append(f"zip top level is {sorted(tops)}, expected ['che_supplement']")
    for p in sorted(root.rglob("*")):
        rel = p.relative_to(root).as_posix()
        if any(part == ".git" for part in p.parts):
            fails.append(f"{rel}: .git present")
        for name, rx, _skip in forb:
            if name in BIN_FORBIDDEN and rx.search(rel):
                fails.append(f"{rel}: [path] {name}")
        for m in R.HEX_TOKEN.finditer(rel):
            if is_commit_prefix(m.group(1), cs):
                fails.append(f"{rel}: [path] commit hash of this repository")
        if not p.is_file():
            continue
        info["files"] += 1
        if any(part.startswith(".") for part in Path(rel).parts[1:]):
            info["hidden"].append(rel)
        data = p.read_bytes()
        try:
            if b"\0" in data[:8192]:
                raise UnicodeDecodeError("x", b"", 0, 1, "nul")
            text = data.decode("utf-8")
            binary = False
        except UnicodeDecodeError:
            binary = True
        if binary:
            info["binary"] += 1
            blobs = [data]
            if p.suffix == ".npz":
                with zipfile.ZipFile(p) as z:
                    blobs += [n.encode() for n in z.namelist()]
                    blobs += [z.read(n) for n in z.namelist()]
            for b in blobs:
                s = b.decode("latin-1")
                for name, rx, _skip in forb:
                    if name in BIN_FORBIDDEN and rx.search(s):
                        fails.append(
                            f"{rel}: [binary] {name}: {rx.search(s).group(0)!r}"
                        )
            continue
        for ln_no, line in enumerate(text.splitlines(), 1):
            for name, rx, skip in forb:
                if skip and re.search(skip, rel):
                    continue
                for m in rx.finditer(line):
                    if name == "email" and m.group(0) in R.EMAIL_ALLOW:
                        continue
                    fails.append(f"{rel}:{ln_no}: {name}: {m.group(0)[:80]!r}")
            for m in R.HEX_TOKEN.finditer(line):
                if is_commit_prefix(m.group(1), cs):
                    fails.append(
                        f"{rel}:{ln_no}: commit hash of this repository: {m.group(1)}"
                    )
            for name, rx in R.WARN:
                for m in rx.finditer(line):
                    warns.append(f"{rel}:{ln_no}: {name}: {m.group(0)[:100]!r}")
            for m in URL.finditer(line):
                info["url_domains"][m.group(1).lower()] += 1
            info["workspace_paths"] += line.count("/workspace")
            info["vast_mentions"] += len(re.findall(r"(?i)vast", line))
    return fails, warns, info


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--zip", type=Path, default=REPO / "paper/v3/out/che_supplement.zip"
    )
    ap.add_argument("--max-list", type=int, default=60)
    a = ap.parse_args(argv)
    with tempfile.TemporaryDirectory(prefix="che_scrub_") as td:
        with zipfile.ZipFile(a.zip) as z:
            z.extractall(td)
        fails, warns, info = scan(Path(td))
    print(f"scanned {info['files']} files ({info['binary']} binary) from {a.zip.name}")
    print("URL domains (info):", dict(info["url_domains"]))
    print(
        f"'/workspace' occurrences (info; container default dir, not "
        f"identifying): {info['workspace_paths']}"
    )
    print(
        f"'vast' mentions (info; GPU rental provider named in reports): "
        f"{info['vast_mentions']}"
    )
    hid = collections.Counter(Path(h).parent.name for h in info["hidden"])
    print(f"hidden files (info): {len(info['hidden'])} in {dict(hid)}")
    print(f"WARN ({len(warns)}; review by hand):")
    for w in warns[: a.max_list]:
        print("  ", w)
    if fails:
        print(f"FAIL ({len(fails)}):")
        for f in fails[: a.max_list]:
            print("  ", f)
        print("SCRUB CHECK: FAIL")
        return 1
    print("SCRUB CHECK: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
