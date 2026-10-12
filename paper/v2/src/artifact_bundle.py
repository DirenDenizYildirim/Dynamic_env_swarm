"""Package the real-kit build of paper/v2 as a private claude.ai Artifact (orchestrator, 2026-10-12).

The kit's Jekyll output (``serve/main/tmlr-beyond-pdf/`` inside a ``kit_build.sh`` run
directory) is a multi-file site with absolute ``/tmlr-beyond-pdf/`` paths and several
third-party stylesheets. The Artifact viewer's CSP admits external *scripts* only from a few
CDNs and external *stylesheets* only from Google Fonts. This script makes a self-contained
copy without changing the paper:

- rewrites ``/tmlr-beyond-pdf/`` to relative paths;
- vendors every non-Google-Fonts stylesheet (and the fonts/images its ``url()``s name) under
  ``vendor/``;
- points MathJax 3.2.0 (CHTML, as the kit uses it) at vendored copies of its woff-v2 fonts;
- removes the kit's utteranc.es comment widget (no repository is set; it only errors);
- drops the doctype/html/head wrapper (the Artifact skeleton supplies one) and puts a
  ``<title>`` first.

Scripts from cdn.jsdelivr.net/npm (pinned) and cdnjs (pinned) are left as they are.

Usage (repository root):
    python paper/v2/src/artifact_bundle.py <kit_run_dir> <out_dir>
Prints the file count and total size; ``<out_dir>/index.html`` is the page and every other
file under ``<out_dir>`` is a supporting file, published at its relative path.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import urljoin, urlparse

TITLE = "CHE Paper v2"
PREFIX = "/tmlr-beyond-pdf/"
MATHJAX_FLAT = "https://data.jsdelivr.com/v1/package/npm/mathjax@3.2.0/flat"
MATHJAX_FONTS = "https://cdn.jsdelivr.net/npm/mathjax@3.2.0/es5/output/chtml/fonts/woff-v2/"


def fetch(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["curl", "-sSfL", "-o", str(dest), url], check=True)


def vendor_css(url: str, out: Path) -> str:
    """Download a stylesheet and every relative url() it names; return its local path."""
    u = urlparse(url)
    local = Path("vendor") / u.netloc / u.path.lstrip("/")
    fetch(url, out / local)
    css = (out / local).read_text(encoding="utf-8", errors="replace")
    for ref in sorted(set(re.findall(r"url\(\s*['\"]?([^'\")]+)['\"]?\s*\)", css))):
        if ref.startswith(("data:", "#")) or "://" in ref:
            continue
        clean = ref.split("?")[0].split("#")[0]
        # Legacy font formats the Artifact host refuses (.eot is not a served type; SVG fonts
        # carry a DOCTYPE). Browsers use the woff2/woff entries in the same src lists.
        if clean.endswith(".eot") or (clean.endswith(".svg") and "font" in clean):
            continue
        target = urljoin(url, clean)
        tu = urlparse(target)
        dest = out / "vendor" / tu.netloc / tu.path.lstrip("/")
        if not dest.exists():
            try:
                fetch(target, dest)
            except subprocess.CalledProcessError:
                print(f"  (not found, skipped) {target}")
    return local.as_posix()


def main() -> None:
    run, out = Path(sys.argv[1]), Path(sys.argv[2])
    site = run / "serve" / "main" / "tmlr-beyond-pdf"
    page = site / "under_review" / "submission" / "index.html"
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    html = page.read_text(encoding="utf-8")

    # 1. the site's own assets, at relative paths
    shutil.copytree(site / "assets", out / "assets")
    html = html.replace('"' + PREFIX, '"').replace("'" + PREFIX, "'").replace("(" + PREFIX, "(")

    # 2. third-party stylesheets other than Google Fonts -> vendored files
    for m in re.finditer(r'<link\b[^>]*>', html):
        tag = m.group(0)
        href = re.search(r'href="([^"]+)"', tag)
        if not href or "stylesheet" not in tag:
            continue
        url = href.group(1)
        if url.startswith("https://") and "fonts.googleapis.com" not in url:
            local = vendor_css(url, out)
            new = re.sub(r'\s(integrity|crossorigin)="[^"]*"', "", tag).replace(url, local)
            html = html.replace(tag, new)

    # 3. MathJax CHTML fonts, vendored (the CSP blocks font files from the CDN)
    listing = json.loads(subprocess.run(["curl", "-sSfL", MATHJAX_FLAT], check=True,
                                        capture_output=True, text=True).stdout)
    fonts = [f["name"].rsplit("/", 1)[1] for f in listing["files"]
             if f["name"].startswith("/es5/output/chtml/fonts/woff-v2/")]
    for name in fonts:
        fetch(MATHJAX_FONTS + name, out / "vendor" / "mathjax-fonts" / name)
    html = html.replace("tex: {", "chtml: { fontURL: 'vendor/mathjax-fonts' },\n    tex: {", 1)

    # 4. the comment widget (no repository set; it only throws)
    html = re.sub(r'<script[^>]*utteranc\.es[^>]*>.*?</script>', "", html, flags=re.S)

    # 5. wrapper: the Artifact skeleton supplies doctype/html/head/body
    html = re.sub(r"<!DOCTYPE[^>]*>", "", html, flags=re.I)
    html = re.sub(r"</?html[^>]*>|</?head>", "", html)
    html = re.sub(r"<title>.*?</title>", "", html, flags=re.S)
    head = (f"<title>{TITLE}</title>\n"
            "<style>:root{color-scheme:light} body{background:#fff}</style>\n")
    (out / "index.html").write_text(head + html, encoding="utf-8")

    for junk in list(out.rglob("*.map")):
        junk.unlink()  # source maps: not needed by the page
    files = [p for p in out.rglob("*") if p.is_file()]
    size = sum(p.stat().st_size for p in files)
    print(f"{len(files)} files, {size / 1e6:.1f} MB ({len(fonts)} MathJax fonts) -> {out}")
    left = sorted(set(re.findall(r'(?:src|href)="(https?://[^"]+)"', html)))
    print("external URLs left in the page:")
    for u in left:
        print("  ", u)


if __name__ == "__main__":
    main()
