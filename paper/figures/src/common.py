# ruff: noqa: E501  (inline JS/CSS of a self-contained HTML figure)
"""Shared paths, palette, matplotlib style and the self-contained HTML shell
for the candidate figures (decision log, FIGURES entry, 2026-10-10).

Read-only with respect to the repository: every loader opens committed
artifacts; every writer writes under paper/figures/out/. No figure states a
number that is not read from a committed file or a ledger row (MANIFEST.md
lists both). No output file carries a path, name, host or hash.
"""

from __future__ import annotations

import html
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[3]
RES = ROOT / "che" / "bench" / "results"
P6 = RES / "phase6"
OUT = ROOT / "paper" / "figures" / "out"
IMG, GIF, HTML_DIR = OUT / "img", OUT / "gif", OUT / "html"
for _d in (IMG, GIF, HTML_DIR):
    _d.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------- palette
# dataviz reference palette, first three categorical slots (validated
# all-pairs, light and dark: validate_palette.js, 2026-10-10). Greyscale
# readability comes from marker shape and line style, never colour alone.
INK = "#0b0b0b"
INK2 = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
AXIS = "#c3c2b7"
SURFACE = "#ffffff"
BAND = "#ecebe6"  # one step off the surface: MDE / exclusion bands
HATCH = "#898781"  # floor bars: muted ink, thin 45° hatch
S1, S2, S3 = "#2a78d6", "#eb6834", "#1baf7a"  # blue, orange, aqua
# ordinal blue ramp (palette.md sequential, steps 250 / 450 / 650) for the
# three ordered severity levels Low < Medium < High
SEV = {"Low": "#86b6ef", "Medium": "#2a78d6", "High": "#104281"}
SEV_MARK = {"Low": "o", "Medium": "s", "High": "^"}

ARM_STYLE = {
    # arm: (colour, marker, label)
    "iso": (S1, "o", "ISO"),
    "joint": (S2, "s", "JOINT"),
    "iso4": (S3, "^", "ISO-4"),
    "sweep_c50_p000": (INK2, "D", "sweep_c50_p000"),
}

MINUS = "−"


def fmt(v: float, nd: int = 4, sign: bool = True) -> str:
    """Signed decimal with a typographic minus (labels only, never maths)."""
    s = f"{abs(v):.{nd}f}"
    if v < 0 and float(s) != 0.0:
        return MINUS + s
    return ("+" + s) if sign else s


def ci_text(lo: float, hi: float, nd: int = 4) -> str:
    return f"[{fmt(lo, nd)}, {fmt(hi, nd)}]"


def load_json(p: Path) -> dict:
    return json.loads(p.read_text())


def rel(p: Path) -> str:
    """Repo-relative path for the manifest (never an absolute path)."""
    return str(Path(p).resolve().relative_to(ROOT))


# ---------------------------------------------------------------- matplotlib
def mpl_setup() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 8.5,
            "axes.titlesize": 9,
            "axes.titleweight": "bold",
            "axes.titlelocation": "left",
            "axes.labelsize": 8.5,
            "axes.labelcolor": INK2,
            "axes.edgecolor": AXIS,
            "axes.linewidth": 0.8,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": False,
            "grid.color": GRID,
            "grid.linewidth": 0.6,
            "xtick.color": MUTED,
            "ytick.color": MUTED,
            "xtick.labelcolor": INK2,
            "ytick.labelcolor": INK2,
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
            "legend.fontsize": 8,
            "legend.frameon": False,
            "text.color": INK,
            "figure.facecolor": SURFACE,
            "axes.facecolor": SURFACE,
            "savefig.facecolor": SURFACE,
            "lines.linewidth": 1.6,
            "lines.solid_capstyle": "round",
            "svg.fonttype": "path",
            "hatch.linewidth": 0.6,
            "svg.hashsalt": "che-figures",  # deterministic SVG ids
        }
    )


def save_png(fig, name: str, dpi: int = 200) -> Path:
    """PNG with no text chunks: matplotlib writes only 'Software', and it is
    suppressed here; the metadata check re-reads every chunk afterwards."""
    p = IMG / name
    fig.savefig(
        p, dpi=dpi, metadata={"Software": None}, bbox_inches="tight", pad_inches=0.06
    )
    plt.close(fig)
    return p


# ---------------------------------------------------------------- HTML shell
CSS = r"""
:root{color-scheme:light;--surface:#ffffff;--ink:#0b0b0b;--ink2:#52514e;
--muted:#898781;--grid:#e1e0d9;--axis:#c3c2b7;--band:#ecebe6;--band2:#d9d8d1;
--s1:#2a78d6;--s2:#eb6834;--s3:#1baf7a;--neutral:#52514e;
--sev1:#86b6ef;--sev2:#2a78d6;--sev3:#104281;
--ring:rgba(11,11,11,0.10);--shadow:0 2px 8px rgba(0,0,0,0.12)}
@media (prefers-color-scheme:dark){:root:where(:not([data-theme="light"])){
color-scheme:dark;--surface:#1a1a19;--ink:#ffffff;--ink2:#c3c2b7;--muted:#898781;
--grid:#2c2c2a;--axis:#383835;--band:#2a2a28;--band2:#3a3a37;--s1:#3987e5;
--s2:#d95926;--s3:#199e70;--neutral:#c3c2b7;--sev1:#86b6ef;--sev2:#3987e5;
--sev3:#b7d3f6;--ring:rgba(255,255,255,0.10);--shadow:0 2px 8px rgba(0,0,0,0.5)}}
:root[data-theme="dark"]{color-scheme:dark;--surface:#1a1a19;--ink:#ffffff;
--ink2:#c3c2b7;--muted:#898781;--grid:#2c2c2a;--axis:#383835;--band:#2a2a28;
--band2:#3a3a37;--s1:#3987e5;--s2:#d95926;--s3:#199e70;--neutral:#c3c2b7;
--sev1:#86b6ef;--sev2:#3987e5;--sev3:#b7d3f6;--ring:rgba(255,255,255,0.10);
--shadow:0 2px 8px rgba(0,0,0,0.5)}
*{box-sizing:border-box}
html,body{margin:0;background:var(--surface);color:var(--ink)}
body{font:13px/1.4 system-ui,-apple-system,"Segoe UI",sans-serif;padding:10px 16px 14px}
.controls{display:flex;flex-wrap:wrap;gap:6px 14px;align-items:center;margin:0 0 6px}
.seg{display:inline-flex;border:1px solid var(--axis);border-radius:6px;overflow:hidden}
.seg button{font:inherit;font-size:12px;color:var(--ink2);background:transparent;border:0;
padding:4px 10px;cursor:pointer}
.seg button+button{border-left:1px solid var(--axis)}
.seg button[aria-pressed="true"]{background:var(--band);color:var(--ink);font-weight:600}
.seg button:focus-visible{outline:2px solid var(--s1);outline-offset:-2px}
.lab{font-size:12px;color:var(--muted)}
svg{display:block;width:100%;height:auto;overflow:visible}
svg text{fill:var(--ink2);font-family:system-ui,-apple-system,"Segoe UI",sans-serif}
.tick{font-size:11px;font-variant-numeric:tabular-nums}
.axt{font-size:12px}
.ttl{font-size:13px;font-weight:600;fill:var(--ink)}
.note{font-size:11px;fill:var(--muted)}
.hit{fill:transparent;cursor:default}
.hit:focus{outline:none}
.hit:focus-visible{stroke:var(--s1);stroke-width:1.5}
#tip{position:fixed;pointer-events:none;display:none;z-index:9;background:var(--surface);
color:var(--ink);border:1px solid var(--ring);box-shadow:var(--shadow);border-radius:6px;
padding:6px 9px;font-size:12px;max-width:300px;font-variant-numeric:tabular-nums}
#tip strong{font-weight:600}
#tip span{color:var(--ink2)}
#tip .h{color:var(--ink);font-weight:600;margin-bottom:2px}
.legend{display:flex;flex-wrap:wrap;gap:4px 14px;font-size:12px;color:var(--ink2);margin:2px 0 4px}
.legend svg{display:inline-block;width:auto;vertical-align:middle;margin-right:4px}
details{margin-top:8px;font-size:12px;color:var(--ink2)}
summary{cursor:pointer}
table{border-collapse:collapse;margin-top:6px;font-variant-numeric:tabular-nums}
th,td{padding:3px 8px;border-bottom:1px solid var(--grid);text-align:right;white-space:nowrap}
th:first-child,td:first-child{text-align:left}
th{color:var(--ink);font-weight:600}
.tw{overflow-x:auto;max-width:100%}
"""

JS_LIB = r"""
const NS='http://www.w3.org/2000/svg';
function S(tag,a,p){const e=document.createElementNS(NS,tag);if(a)for(const k in a)e.setAttribute(k,a[k]);if(p)p.appendChild(e);return e;}
function T(a,txt,p){const e=S('text',a,p);e.textContent=txt;return e;}
function lin(d0,d1,r0,r1){return v=>r0+(v-d0)*(r1-r0)/(d1-d0);}
function niceTicks(lo,hi,n){const sp=hi-lo,s0=sp/Math.max(1,n),m=Math.pow(10,Math.floor(Math.log10(s0))),e=s0/m;
const st=e>=7.5?10*m:e>=3.5?5*m:e>=1.5?2*m:m;const o=[];for(let v=Math.ceil(lo/st-1e-9)*st;v<=hi+st*1e-9;v+=st)o.push(+v.toFixed(12));return o;}
const MINUS='−';
function fmt(v,nd){const s=Math.abs(v).toFixed(nd);if(v<0&&+s!==0)return MINUS+s;return '+'+s;}
function fmtU(v,nd){const s=Math.abs(v).toFixed(nd);return (v<0&&+s!==0?MINUS:'')+s;}
function decimals(step){return Math.max(0,-Math.floor(Math.log10(step)+1e-9));}
function tickFmt(ts){const st=ts.length>1?Math.abs(ts[1]-ts[0]):1;const d=decimals(st);return v=>fmtU(v,d);}
const tip=document.getElementById('tip');
function showTip(x,y,head,rows){tip.replaceChildren();if(head){const h=document.createElement('div');h.className='h';h.textContent=head;tip.appendChild(h);}
for(const [val,lab] of rows){const r=document.createElement('div');const b=document.createElement('strong');b.textContent=val;r.appendChild(b);
if(lab){const s=document.createElement('span');s.textContent=' '+lab;r.appendChild(s);}tip.appendChild(r);}
tip.style.display='block';const w=tip.offsetWidth,h=tip.offsetHeight;let L=x+14,Tp=y+14;
if(L+w>window.innerWidth-4)L=x-w-14;if(Tp+h>window.innerHeight-4)Tp=y-h-14;tip.style.left=Math.max(4,L)+'px';tip.style.top=Math.max(4,Tp)+'px';}
function hideTip(){tip.style.display='none';}
function bindTip(node,head,rows){node.setAttribute('tabindex','0');node.setAttribute('role','img');
node.setAttribute('aria-label',head+': '+rows.map(r=>r.join(' ')).join('; '));
node.addEventListener('pointermove',ev=>showTip(ev.clientX,ev.clientY,head,rows));
node.addEventListener('pointerleave',hideTip);
node.addEventListener('focus',()=>{const r=node.getBoundingClientRect();showTip(r.right,r.top,head,rows);});
node.addEventListener('blur',hideTip);}
function seg(container,opts,init,onChange){const d=document.createElement('div');d.className='seg';d.setAttribute('role','group');
const bs=[];for(const [val,lab] of opts){const b=document.createElement('button');b.type='button';b.textContent=lab;
b.setAttribute('aria-pressed',String(val===init));b.addEventListener('click',()=>{bs.forEach(x=>x.setAttribute('aria-pressed',String(x===b)));onChange(val);});bs.push(b);d.appendChild(b);}
container.appendChild(d);return d;}
function table(container,head,rows){const t=document.createElement('table');const tr=document.createElement('tr');
for(const h of head){const th=document.createElement('th');th.textContent=h;tr.appendChild(th);}t.appendChild(tr);
for(const r of rows){const x=document.createElement('tr');for(const c of r){const td=document.createElement('td');td.textContent=c;x.appendChild(td);}t.appendChild(x);}
container.replaceChildren(t);}
function marker(shape,cx,cy,r,a,p){if(shape==='s')return S('rect',Object.assign({x:cx-r*0.9,y:cy-r*0.9,width:r*1.8,height:r*1.8},a),p);
if(shape==='^'){const h=r*1.15;return S('path',Object.assign({d:`M${cx},${cy-h}L${cx+h},${cy+h*0.8}L${cx-h},${cy+h*0.8}Z`},a),p);}
if(shape==='D'){const h=r*1.2;return S('path',Object.assign({d:`M${cx},${cy-h}L${cx+h},${cy}L${cx},${cy+h}L${cx-h},${cy}Z`},a),p);}
return S('circle',Object.assign({cx:cx,cy:cy,r:r},a),p);}
// follow the embedding page's theme when it sets one (same-origin iframe)
(function(){function sync(){try{const t=window.parent&&window.parent!==window?window.parent.document.documentElement.getAttribute('data-theme'):null;
if(t==='dark'||t==='light')document.documentElement.setAttribute('data-theme',t);}catch(e){}}
sync();try{if(window.parent!==window)new MutationObserver(sync).observe(window.parent.document.documentElement,{attributes:true,attributeFilter:['data-theme']});}catch(e){}})();
"""


def write_html(name: str, title: str, body: str, data: dict, script: str) -> Path:
    """One self-contained page: inline CSS, inline data, inline JS, inline
    SVG built at load. No external URL, font, script or library."""
    doc = (
        '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        f"<title>{html.escape(title)}</title>\n<style>{CSS}</style>\n</head>\n<body>\n"
        f'{body}\n<div id="tip" role="tooltip"></div>\n'
        f"<script>\nconst DATA={json.dumps(data, ensure_ascii=False, separators=(',', ':'))};\n"
        f"{JS_LIB}\n{script}\n</script>\n</body>\n</html>\n"
    )
    p = HTML_DIR / name
    p.write_text(doc)
    return p
