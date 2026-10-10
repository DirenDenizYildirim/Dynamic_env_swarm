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

# --- palette (DESIGN.md section 3); light / dark ---------------------------
TOKENS_LIGHT = {
    "surface": "#fcfcfb", "ink": "#0b0b0b", "ink2": "#52514e", "muted": "#898781",
    "grid": "#e1e0d9", "axis": "#c3c2b7", "band": "#ecebe5", "chipfill": "#0b0b0b",
    "chiptext": "#fcfcfb", "focus": "#0b0b0b", "hover": "rgba(11,11,11,0.06)",
    "A": "#4a3aa7", "B": "#e87ba4", "fireonly": "#c3c2b7",
}
# Map imagery (hazard field, 9x9 panels) keeps ONE palette in both themes: it is
# a picture of the state, and its lightness order (fuel > burning > burnt) is
# what makes it greyscale-readable. Only the page chrome around it themes.
MAP_TOKENS = {
    # identical to the restyled GIFs (paper/renders/2026-10-10/src/render_restyle.py)
    "fuel": "#e9ebe0", "burning": "#eb6834", "burnt": "#3d3a36", "smoke_hatch": "#f4f1eb",
    "map_gridline": "#8c8a83", "agent": "#2a78d6", "food": "#1baf7a", "map_white": "#ffffff",
    "map_bg": "#fcfcfb", "map_ink": "#0b0b0b", "outside": "#f4f3ef",
    # explorer-only marks
    "unseen": "#a9a59a", "unseen_mark": "#3d3a36", "map_grid": "#e1e0d9", "map_axis": "#c3c2b7",
    "map_A": "#4a3aa7", "tau_end": "#9c2f5c",
}
TOKENS_LIGHT.update(MAP_TOKENS)

TOKENS_DARK = {
    "surface": "#1a1a19", "ink": "#f5f5f2", "ink2": "#c3c2b7", "muted": "#898781",
    "grid": "#2c2c2a", "axis": "#383835", "band": "#2a2a27", "chipfill": "#f5f5f2",
    "chiptext": "#1a1a19", "focus": "#f5f5f2", "hover": "rgba(255,255,255,0.08)",
    "A": "#9085e9", "B": "#d55181", "fireonly": "#4a4945",
}
TOKENS_DARK.update(MAP_TOKENS)


def _vars(tokens: dict) -> str:
    return "".join(f"--{k}:{v};" for k, v in tokens.items())


BASE_CSS = (
    ":root{" + _vars(TOKENS_LIGHT) + "color-scheme:light;}"
    "@media (prefers-color-scheme: dark){:root:not([data-theme=\"light\"]){"
    + _vars(TOKENS_DARK) + "color-scheme:dark;}}"
    ":root[data-theme=\"dark\"]{" + _vars(TOKENS_DARK) + "color-scheme:dark;}"
    + r"""
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:var(--surface);color:var(--ink);
 font:13px/1.45 system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif}
.wrap{padding:12px 16px 14px;max-width:980px;margin:0 auto}
.sub{color:var(--ink2);font-size:12px;margin:0 0 8px}
.muted{color:var(--muted)}
.row{display:flex;flex-wrap:wrap;gap:6px;align-items:center}
.ctl{display:flex;flex-wrap:wrap;gap:6px 8px;align-items:center;margin:0 0 8px}
.ctl .lab{font-size:11px;color:var(--muted);margin-right:2px;text-transform:none}
button.pill{font:inherit;font-size:12px;min-height:28px;padding:3px 10px;border-radius:14px;
 border:1px solid var(--axis);background:var(--surface);color:var(--ink);cursor:pointer;
 display:inline-flex;align-items:center;gap:6px;line-height:1}
button.pill[aria-pressed="true"]{background:var(--ink);color:var(--surface);border-color:var(--ink)}
button.pill:hover{background:var(--hover)}
button.pill[aria-pressed="true"]:hover{background:var(--ink)}
button.pill:disabled{opacity:.4;cursor:default}
button:focus-visible,input:focus-visible,[tabindex]:focus-visible,summary:focus-visible{
 outline:2px solid var(--focus);outline-offset:2px}
input[type=range]{accent-color:var(--ink)}
.chip{display:inline-block;font-size:11px;font-weight:600;letter-spacing:.02em;padding:2px 7px;
 border-radius:10px;border:1px solid var(--ink);white-space:nowrap;line-height:1.35}
.chip.fill{background:var(--chipfill);color:var(--chiptext)}
.chip.line{background:transparent;color:var(--ink)}
.chip.weak{color:var(--ink);background-image:radial-gradient(var(--muted) 0.8px,transparent 1px);
 background-size:4px 4px}
.tt{position:fixed;pointer-events:none;z-index:9;background:var(--surface);color:var(--ink);
 border:1px solid var(--axis);border-radius:6px;padding:6px 8px;font-size:12px;line-height:1.35;
 box-shadow:0 2px 8px rgba(0,0,0,.12);max-width:280px;display:none}
.tt b{font-variant-numeric:tabular-nums}
.num{font-variant-numeric:tabular-nums}
details.tbl{margin-top:8px;font-size:12px}
details.tbl summary{cursor:pointer;color:var(--ink2)}
details.tbl table{border-collapse:collapse;margin-top:6px;font-variant-numeric:tabular-nums}
details.tbl th,details.tbl td{border-bottom:1px solid var(--grid);padding:3px 8px;text-align:left;
 vertical-align:top}
svg text{fill:var(--ink);font-family:inherit}
svg .tick{fill:var(--muted);font-size:11px}
svg .gl{stroke:var(--grid);stroke-width:1}
svg .ax{stroke:var(--axis);stroke-width:1}
svg .zero{stroke:var(--muted);stroke-width:1}
@media (prefers-reduced-motion: reduce){*{transition:none!important;animation:none!important}}
@media print{.ctl,.noprint,details.tbl{display:none!important} .tt{display:none!important}}
"""
)

BASE_JS = r"""
(function(){
  // Theme: follow the embedding page when same-origin (al-folio sets data-theme).
  function syncTheme(){
    try{
      var p = window.parent && window.parent !== window && window.parent.document;
      var t = p && p.documentElement.getAttribute('data-theme');
      if(t==='dark'||t==='light'){document.documentElement.setAttribute('data-theme',t);return;}
    }catch(e){}
  }
  syncTheme();
  try{
    var pd = window.parent && window.parent !== window && window.parent.document;
    if(pd && window.MutationObserver){
      new MutationObserver(function(){syncTheme(); if(window.__redraw) window.__redraw();})
        .observe(pd.documentElement,{attributes:true,attributeFilter:['data-theme']});
    }
  }catch(e){}
  // Self-size the iframe when same-origin (fixed iframe heights clip on phones).
  function fit(){
    try{
      var fe = window.frameElement;
      if(fe){ fe.style.height = (document.documentElement.scrollHeight + 4) + 'px'; }
    }catch(e){}
  }
  window.__fit = fit;
  window.addEventListener('load', fit);
  if(window.ResizeObserver){ new ResizeObserver(fit).observe(document.body); }
  window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)')
    .addEventListener && window.matchMedia('(prefers-color-scheme: dark)')
    .addEventListener('change', function(){ if(window.__redraw) window.__redraw(); });
})();
var U = {
  css: function(name){ return getComputedStyle(document.documentElement).getPropertyValue('--'+name).trim(); },
  reduced: function(){ return !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches); },
  el: function(tag, attrs, text){
    var e = document.createElement(tag);
    if(attrs) for(var k in attrs){ if(attrs[k]!==null && attrs[k]!==undefined) e.setAttribute(k, attrs[k]); }
    if(text!==undefined && text!==null) e.textContent = text;
    return e;
  },
  svg: function(tag, attrs, text){
    var e = document.createElementNS('http://www.w3.org/2000/svg', tag);
    if(attrs) for(var k in attrs){ if(attrs[k]!==null && attrs[k]!==undefined) e.setAttribute(k, attrs[k]); }
    if(text!==undefined && text!==null) e.textContent = text;
    return e;
  },
  clear: function(n){ while(n.firstChild) n.removeChild(n.firstChild); },
  sgn: function(x, d){ var s = (x>0?'+':(x<0?'−':'')); return s + Math.abs(x).toFixed(d); },
  ci: function(a, d){ return '[' + U.sgn(a[0],d) + ', ' + U.sgn(a[1],d) + ']'; },
  tip: (function(){
    var t = null;
    function node(){ if(!t){ t = document.createElement('div'); t.className='tt'; t.setAttribute('role','tooltip'); document.body.appendChild(t);} return t; }
    return {
      show: function(lines, x, y){
        var n = node(); U.clear(n);
        lines.forEach(function(l, i){
          var d = document.createElement('div');
          if(Array.isArray(l)){ var b=document.createElement('b'); b.textContent=l[0]; d.appendChild(b);
            if(l[1]) d.appendChild(document.createTextNode(' ' + l[1])); }
          else d.textContent = l;
          n.appendChild(d);
        });
        n.style.display='block';
        var w = n.offsetWidth, h = n.offsetHeight;
        var vx = Math.min(x + 14, window.innerWidth - w - 6), vy = y + 14;
        if(vy + h > window.innerHeight - 4) vy = Math.max(4, y - h - 10);
        n.style.left = Math.max(4, vx) + 'px'; n.style.top = vy + 'px';
      },
      hide: function(){ if(t) t.style.display='none'; }
    };
  })(),
  b64: function(s){ var bin = atob(s), n = bin.length, out = new Uint8Array(n);
    for(var i=0;i<n;i++) out[i] = bin.charCodeAt(i); return out; },
  // Tooltip at a focused element's position (keyboard parity with hover).
  tipAt: function(el, lines){ var r = el.getBoundingClientRect(); U.tip.show(lines, r.left + r.width/2, r.top + r.height/2); }
};
"""


def page(title: str, body: str, css: str = "", js: str = "", data: dict | None = None,
         lang: str = "en") -> str:
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
            hits.append(f"{path.name}: {rx.pattern} -> {text[max(0, m.start()-30):m.end()+30]!r}")
    for tag in ("<script src", "<link ", "@import", "url(http", "<iframe", "fetch(", "XMLHttpRequest"):
        if tag in text:
            hits.append(f"{path.name}: contains {tag}")
    return hits


def check_png(path: Path) -> list[str]:
    """Return any text chunk (tEXt/zTXt/iTXt/eXIf/tIME) found in a PNG."""
    data = path.read_bytes()
    assert data[:8] == b"\x89PNG\r\n\x1a\n"
    i, found = 8, []
    while i < len(data):
        n = int.from_bytes(data[i:i + 4], "big")
        typ = data[i + 4:i + 8].decode("latin-1")
        if typ in ("tEXt", "zTXt", "iTXt", "eXIf", "tIME"):
            found.append(f"{path.name}: {typ} {data[i + 8:i + 8 + min(n, 60)]!r}")
        i += 12 + n
    return found


def savefig(fig, path: Path, dpi: int = 200):
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=dpi, metadata={"Software": None}, facecolor=fig.get_facecolor())
    bad = check_png(path)
    assert not bad, bad
