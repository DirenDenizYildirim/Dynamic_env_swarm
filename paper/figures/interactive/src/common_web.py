"""Shared inline component set for every interactive figure in this directory.

Each output HTML file is self-contained: the CSS and JS below are copied into
every file (no external URL, script, font or library; no network at view
time). One visual language (DESIGN.md section 3):

- colour means stressor identity (Coupling A violet, Coupling B magenta) or
  map state in the restyled GIFs' palette (fuel, burning, burnt, food,
  agents) and nothing else; statistics are ink
  and grey; verdicts are chips holding the registered strings verbatim;
- theme follows the host page's data-theme when same-origin, else the OS;
- no autoplay; prefers-reduced-motion disables transitions;
- @media print hides controls; the file sizes its own iframe when it can.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT_HTML = HERE.parent / "out" / "html"
OUT_IMG = HERE.parent / "out" / "img"
OUT_DATA = HERE.parent / "out" / "data"
REPO = HERE.parents[3]
TEMPLATES = HERE / "templates"


def load_template(name: str) -> str:
    """Inline CSS/HTML/JS of a figure, kept in src/templates/ and copied
    verbatim into each self-contained output file at build time."""
    return (TEMPLATES / name).read_text(encoding="utf-8")


# --- palette (DESIGN.md section 3); light / dark ---------------------------
TOKENS_LIGHT = {
    "surface": "#fcfcfb",
    "ink": "#0b0b0b",
    "ink2": "#52514e",
    "muted": "#898781",
    "grid": "#e1e0d9",
    "axis": "#c3c2b7",
    "band": "#ecebe5",
    "chipfill": "#0b0b0b",
    "chiptext": "#fcfcfb",
    "focus": "#0b0b0b",
    "hover": "rgba(11,11,11,0.06)",
    "A": "#4a3aa7",
    "B": "#e87ba4",
    "fireonly": "#c3c2b7",
}
# Map imagery (hazard field, 9x9 panels) keeps ONE palette in both themes: it is
# a picture of the state, and its lightness order (fuel > burning > burnt) is
# what makes it greyscale-readable. Only the page chrome around it themes.
MAP_TOKENS = {
    # identical to the restyled GIFs (paper/renders/2026-10-10/src/render_restyle.py)
    "fuel": "#e9ebe0",
    "burning": "#eb6834",
    "burnt": "#3d3a36",
    "smoke_hatch": "#f4f1eb",
    "map_gridline": "#8c8a83",
    "agent": "#2a78d6",
    "food": "#1baf7a",
    "map_white": "#ffffff",
    "map_bg": "#fcfcfb",
    "map_ink": "#0b0b0b",
    "outside": "#f4f3ef",
    # explorer-only marks
    "unseen": "#a9a59a",
    "unseen_mark": "#3d3a36",
    "map_grid": "#e1e0d9",
    "map_axis": "#c3c2b7",
    "map_A": "#4a3aa7",
    "tau_end": "#9c2f5c",
}
TOKENS_LIGHT.update(MAP_TOKENS)

TOKENS_DARK = {
    "surface": "#1a1a19",
    "ink": "#f5f5f2",
    "ink2": "#c3c2b7",
    "muted": "#898781",
    "grid": "#2c2c2a",
    "axis": "#383835",
    "band": "#2a2a27",
    "chipfill": "#f5f5f2",
    "chiptext": "#1a1a19",
    "focus": "#f5f5f2",
    "hover": "rgba(255,255,255,0.08)",
    "A": "#9085e9",
    "B": "#d55181",
    "fireonly": "#4a4945",
}
TOKENS_DARK.update(MAP_TOKENS)


def _vars(tokens: dict) -> str:
    return "".join(f"--{k}:{v};" for k, v in tokens.items())


BASE_CSS = (
    ":root{" + _vars(TOKENS_LIGHT) + "color-scheme:light;}"
    '@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){'
    + _vars(TOKENS_DARK)
    + "color-scheme:dark;}}"
    ':root[data-theme="dark"]{'
    + _vars(TOKENS_DARK)
    + "color-scheme:dark;}"
    + load_template("base.css")
)

BASE_JS = load_template("base.js")


def page(
    title: str,
    body: str,
    css: str = "",
    js: str = "",
    data: dict | None = None,
    lang: str = "en",
) -> str:
    """Assemble one self-contained HTML document."""
    data_tag = ""
    if data is not None:
        payload = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
        payload = payload.replace("</", "<\\/")
        data_tag = f'<script type="application/json" id="data">{payload}</script>\n'
    return (
        "<!doctype html>\n"
        f'<html lang="{lang}">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"<title>{title}</title>\n<style>{BASE_CSS}{css}</style>\n</head>\n<body>\n"
        f"{body}\n{data_tag}<script>{BASE_JS}</script>\n<script>{js}</script>\n</body>\n</html>\n"
    )


# --- double-blind checks ----------------------------------------------------
_FORBIDDEN = [
    re.compile(r"https?://", re.I),
    re.compile(r"/home/", re.I),
    re.compile(r"diren", re.I),
    re.compile(r"yildirim", re.I),
    re.compile(r"github", re.I),
    re.compile(r"\b[0-9a-f]{40}\b"),
    re.compile(r"/tmp/"),
    re.compile(r"claude", re.I),
    re.compile(r"\bche/bench\b"),
]
# The SVG namespace URI is a fixed W3C identifier, not a network resource.
_ALLOWED = ["http://www.w3.org/2000/svg"]


def check_html(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    for a in _ALLOWED:
        text = text.replace(a, "")
    hits = []
    for rx in _FORBIDDEN:
        for m in rx.finditer(text):
            hits.append(
                f"{path.name}: {rx.pattern} -> "
                f"{text[max(0, m.start() - 30) : m.end() + 30]!r}"
            )
    for tag in (
        "<script src",
        "<link ",
        "@import",
        "url(http",
        "<iframe",
        "fetch(",
        "XMLHttpRequest",
    ):
        if tag in text:
            hits.append(f"{path.name}: contains {tag}")
    return hits


def check_png(path: Path) -> list[str]:
    """Return any text chunk (tEXt/zTXt/iTXt/eXIf/tIME) found in a PNG."""
    data = path.read_bytes()
    assert data[:8] == b"\x89PNG\r\n\x1a\n"
    i, found = 8, []
    while i < len(data):
        n = int.from_bytes(data[i : i + 4], "big")
        typ = data[i + 4 : i + 8].decode("latin-1")
        if typ in ("tEXt", "zTXt", "iTXt", "eXIf", "tIME"):
            found.append(f"{path.name}: {typ} {data[i + 8 : i + 8 + min(n, 60)]!r}")
        i += 12 + n
    return found


def savefig(fig, path: Path, dpi: int = 200):
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(
        path, dpi=dpi, metadata={"Software": None}, facecolor=fig.get_facecolor()
    )
    bad = check_png(path)
    assert not bad, bad
