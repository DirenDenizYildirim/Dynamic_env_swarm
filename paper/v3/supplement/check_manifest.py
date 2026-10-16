"""Check (d) MANIFEST: every file in the unpacked zip matches SHA256SUMS, and
SHA256SUMS lists every file (no extra, no missing).

    .venv/bin/python paper/v3/supplement/check_manifest.py [--zip ...]

Exit 0 = PASS, 1 = FAIL.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
import tempfile
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--zip", type=Path, default=REPO / "paper/v3/out/che_supplement.zip"
    )
    a = ap.parse_args(argv)
    with tempfile.TemporaryDirectory(prefix="che_manifest_") as td:
        with zipfile.ZipFile(a.zip) as z:
            z.extractall(td)
        root = Path(td) / "che_supplement"
        listed: dict[str, str] = {}
        for ln in (root / "SHA256SUMS").read_text().splitlines():
            h, rel = ln.split("  ", 1)
            listed[rel] = h
        present = {
            p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()
        } - {"SHA256SUMS"}
        missing = sorted(set(listed) - present)
        extra = sorted(present - set(listed))
        bad = sorted(r for r in set(listed) & present if sha256(root / r) != listed[r])
    print(
        f"SHA256SUMS lists {len(listed)} files; tree has {len(present)} "
        f"(excluding SHA256SUMS)"
    )
    for name, xs in (("missing", missing), ("unlisted", extra), ("hash mismatch", bad)):
        print(f"{name}: {len(xs)}")
        for x in xs[:20]:
            print("   ", x)
    ok = not (missing or extra or bad)
    print(f"MANIFEST CHECK: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
