"""Double-blind and self-containment check over every output file.

HTML: no http(s) URL (the SVG namespace identifier excepted), no external
script/link/@import/iframe/fetch, no home path, user or account name, no
40-hex commit hash, no tool name. PNG: no tEXt/zTXt/iTXt/eXIf/tIME chunk.
Writes out/data/output_checks.json and exits non-zero on any finding.

Run from the repo root:  uv run python paper/figures/interactive/src/check_outputs.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common_web import OUT_DATA, OUT_HTML, OUT_IMG, check_html, check_png  # noqa: E402


def main():
    report = {"html": {}, "png": {}}
    bad = []
    for p in sorted(OUT_HTML.glob("*.html")):
        hits = check_html(p)
        report["html"][p.name] = {"bytes": p.stat().st_size, "findings": hits}
        bad += hits
    for p in sorted(OUT_IMG.glob("*.png")):
        hits = check_png(p)
        report["png"][p.name] = {"bytes": p.stat().st_size, "findings": hits}
        bad += hits
    (OUT_DATA / "output_checks.json").write_text(json.dumps(report, indent=1) + "\n")
    for kind in ("html", "png"):
        for name, r in report[kind].items():
            print(
                f"{kind:4s} {name:58s} {r['bytes'] / 1e3:8.1f} KB  "
                f"{'OK' if not r['findings'] else r['findings']}"
            )
    if bad:
        sys.exit(1)


if __name__ == "__main__":
    main()
