"""Check (b) SIZE: the zip is within TMLR's supplementary-material limit.

    .venv/bin/python paper/v3/supplement/check_size.py [--zip ...]

The limit, VERIFIED 2026-10-14 on TMLR's author guide,
https://jmlr.org/tmlr/author-guide.html :

    "Authors may submit up to 100MB of supplementary material, such data,
    source code or illustrative videos; all supplementary materials must be
    in PDF or ZIP format."

"100MB" is read conservatively as 100 * 10**6 bytes (smaller than 100 MiB).
The OpenReview form's own enforced setting was not visible without an
account; the guide is the venue's statement. Exit 0 = PASS, 1 = FAIL.
"""

from __future__ import annotations

import argparse
import sys
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
LIMIT_BYTES = 100 * 10**6
SOURCE = "https://jmlr.org/tmlr/author-guide.html (read 2026-10-14)"
HEADROOM_WARN = 0.90


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--zip", type=Path, default=REPO / "paper/v3/out/che_supplement.zip"
    )
    a = ap.parse_args(argv)
    n = a.zip.stat().st_size
    with zipfile.ZipFile(a.zip) as z:
        bad = z.testzip()
        unpacked = sum(i.file_size for i in z.infolist())
        count = len(z.infolist())
    print(
        f"zip: {a.zip.name}  {n} bytes ({n / 1e6:.2f} MB); {count} files, "
        f"{unpacked / 1e6:.2f} MB unpacked"
    )
    print(f"limit: {LIMIT_BYTES} bytes (100 MB), source: {SOURCE}")
    print(f"used: {n / LIMIT_BYTES:.1%} of the limit")
    if bad is not None:
        print(f"zip integrity: corrupt member {bad}\nSIZE CHECK: FAIL")
        return 1
    if n / LIMIT_BYTES > HEADROOM_WARN:
        print(f"WARN: above {HEADROOM_WARN:.0%} of the limit")
    if a.zip.suffix.lower() != ".zip":
        print("format: not .zip\nSIZE CHECK: FAIL")
        return 1
    ok = n <= LIMIT_BYTES
    print(f"SIZE CHECK: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
