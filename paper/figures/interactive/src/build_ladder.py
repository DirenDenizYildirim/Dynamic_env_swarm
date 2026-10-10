"""F2 Registered-readings ladder: Γ → Γ₄ → Γ₄′ → B̂, in registered order.

Sources (committed, read-only):
  che/bench/results/phase6/unblind/unblind.json            primary, prefix, beat_reproducibility
  che/bench/results/phase6/post_unblind_analysis/post_gamma4_t2000.json   gamma4.per_metric.*
  che/bench/results/phase6/secondary/secondary.json        replicate.*.gamma4_prime
Every stated number goes through ledger.stated(); the values are asserted equal
to their ledger rows' printed values before anything is drawn.

Run from the repo root:  uv run python paper/figures/interactive/src/build_ladder.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ledger  # noqa: E402
from common_web import OUT_DATA, OUT_HTML, REPO, check_html, page  # noqa: E402

P6 = REPO / "che/bench/results/phase6"
FIG = "F2 ladder"


def f4(x: float) -> str:
    s = f"{abs(x):.4f}"
    return ("+" if x > 0 else ("−" if x < 0 else "")) + s


def ci4(a) -> str:
    return f"[{f4(a[0])}, {f4(a[1])}]"


def load():
    ub = json.loads((P6 / "unblind/unblind.json").read_text())
    g4 = json.loads((P6 / "post_unblind_analysis/post_gamma4_t2000.json").read_text())
    sc = json.loads((P6 / "secondary/secondary.json").read_text())
    src = {
        "G": ("unblind/unblind.json → primary.family.<metric>", lambda m: ub["primary"]["family"][m]),
        "G60": ("unblind/unblind.json → prefix.family.<metric>", lambda m: ub["prefix"]["family"][m]),
        "G4": ("post_gamma4_t2000.json → gamma4.per_metric.<metric>.gamma4",
               lambda m: g4["gamma4"]["per_metric"][m]["gamma4"]),
        "G4p": ("secondary.json → replicate.<metric>.gamma4_prime",
                lambda m: sc["replicate"][m]["gamma4_prime"]),
        "B": ("post_gamma4_t2000.json → gamma4.per_metric.<metric>.b_hat",
              lambda m: g4["gamma4"]["per_metric"][m]["b_hat"]),
    }
    floor = {m: ub["beat_reproducibility"][m]["sd_gamma_floor_basis"]
             for m in ("completion", "survival_rate")}
    labels = {m: g4["gamma4"]["per_metric"][m]["label"] for m in ("completion", "survival_rate")}
    return src, floor, labels


# Ledger rows for each (row, metric, field). None = no row (NEEDS LEDGER ROW).
LEDGER = {
    ("G", "completion"): dict(est="RES-1", ci="RES-1", z="RES-1", X="RES-1"),
    ("G", "survival_rate"): dict(est="RES-2", ci="RES-2", z="RES-2", X=None),
    ("G60", "completion"): dict(est="RES-3", ci=None, z="RES-3", X=None),
    ("G60", "survival_rate"): dict(est="RES-3", ci=None, z="RES-3", X=None),
    ("G4", "completion"): dict(est="RES-6", ci=None, z=None, X="RES-6"),
    ("G4", "survival_rate"): dict(est="RES-6", ci="RES-6", z="RES-6", X=None),
    ("G4p", "completion"): dict(est="RES-8", ci=None, z=None, X=None),
    ("G4p", "survival_rate"): dict(est="RES-8", ci="RES-8", z="RES-8", X=None),
    ("B", "completion"): dict(est="RES-7", ci=None, z=None, X=None),
    ("B", "survival_rate"): dict(est="RES-7", ci="RES-7", z="RES-7", X=None),
}
# Printed values in the ledger rows (asserted against the JSON).
LEDGER_TEXT = {
    ("G", "completion"): dict(est="−0.0173", ci="[−0.0412, +0.0066]", z="−1.62", X="0.0329"),
    ("G", "survival_rate"): dict(est="+0.0096", ci="[+0.0047, +0.0144]", z="+4.43"),
    ("G60", "completion"): dict(est="−0.0217", z="−1.80"),
    ("G60", "survival_rate"): dict(est="+0.0104", z="+4.67"),
    ("G4", "completion"): dict(est="−0.0126", X="0.0488"),
    ("G4", "survival_rate"): dict(est="−0.0003", ci="[−0.0068, +0.0063]", z="−0.09"),
    ("G4p", "completion"): dict(est="−0.0247"),
    ("G4p", "survival_rate"): dict(est="+0.0013", ci="[−0.0056, +0.0081]", z="+0.41"),
    ("B", "completion"): dict(est="−0.0046"),
    ("B", "survival_rate"): dict(est="+0.0098", ci="[+0.0033, +0.0163]", z="+3.39"),
}

ROWS = [
    dict(id="G", rung=1, sym="Γ", contrast="JOINT − ISO", k="k 72 / 72 †", unit="unit 1, both arms",
         family="confirmatory family (Šidák m = 2)", date=None, shape="dot"),
    dict(id="G60", rung=1, sym="Γ", contrast="JOINT − ISO, k = 60 prefix", k="k 60 / 60, seeds 1–60",
         unit="unit 1, both arms", family=None, date=None, shape="ring", optional=True,
         chips=["UNDERPOWERED"]),
    dict(id="G4", rung=2, sym="Γ₄", contrast="JOINT − ISO-4", k="k 72 / 20",
         unit="cross-unit: JOINT unit 1, ISO-4 unit 2",
         family="outside the confirmatory family", date="ISO-4 rule registered 2026-09-18, pre-unblind",
         shape="tri"),
    dict(id="G4p", rung=3, sym="Γ₄′", contrast="JOINT − sweep_c50_p000", k="k 72 / 20",
         unit="unit 1, both arms", family=None, date="proposed 2026-09-26, after Γ₄ was seen",
         shape="diamond"),
    # B̂ has no registered test and no recorded verdict word (UNBLIND RESULT gives
    # only the estimate, z and interval): estimate and interval only, no chip.
    dict(id="B", rung=4, sym="B̂", contrast="ISO-4 − ISO", k="k 20 / 72",
         unit="cross-unit: ISO-4 unit 2, ISO unit 1", family=None, date=None, shape="square",
         noverdict=True),
]
# Ledger for the row labels: k 72/72 DES-3, DES-13; k 60 RES-3, DES-1; k 20 DES-13, DES-15;
# m = 2 DES-13; units HW-4 and spine §10 item 8; dates DES-15, DES-3 (2026-09-22).
FOOT = ("† k = 72 is a recorded deviation: the registered seed ladder's cap was 60, "
        "raised to 72 on 2026-09-22, pre-unblind.")


def build_data():
    ledger.reset()
    src, floor, labels = load()
    assert labels["survival_rate"] == "DOES_NOT_SURVIVE" and labels["completion"] == "SECOND_EXCLUSION"
    out_rows = []
    for r in ROWS:
        srcname, get = src[r["id"]]
        per = {}
        for m in ("completion", "survival_rate"):
            g = get(m)
            led, txt = LEDGER[(r["id"], m)], LEDGER_TEXT[(r["id"], m)]
            vals = dict(est=f4(g["gamma"]), ci=ci4(g["ci_sidak"]), z=f"{g['z']:+.2f}".replace("-", "−"),
                        X=f"{g['exclusion_mde80']:.4f}")
            for key, t in txt.items():
                assert vals[key] == t, (r["id"], m, key, vals[key], t)
            where = f"{srcname.replace('<metric>', m)}"
            per[m] = dict(
                gamma=g["gamma"], lo=g["ci_sidak"][0], hi=g["ci_sidak"][1], X=g["exclusion_mde80"],
                reject=(None if r.get("noverdict") else bool(g["reject"])), k=[g.get("k_a", g.get("k")), g.get("k_b", g.get("k"))],
                est=ledger.stated(vals["est"], led["est"], figure=FIG, what=f"{r['id']} {m} estimate", source=where),
                ci=ledger.stated(vals["ci"], led["ci"], figure=FIG, what=f"{r['id']} {m} Šidák CI", source=where),
                z=(None if r.get("noverdict") else  # estimate and interval only
                   ledger.stated(vals["z"], led["z"], figure=FIG, what=f"{r['id']} {m} z", source=where)),
                Xt=(ledger.stated(vals["X"], led["X"], figure=FIG, what=f"{r['id']} {m} 80 %-power MDE X", source=where)
                    if (r["id"] in ("G", "G60") or (r["id"] == "G4" and m == "completion")) else None),
                floor=(floor[m] if r["id"] == "G" else None),
                # MDE80 band only on the confirmatory family and where the record
                # states an exclusion bound (X₄, completion); out-of-family rows
                # otherwise show estimate and interval only (builder's audit, 2026-10-10)
                band=(r["id"] in ("G", "G60") or (r["id"] == "G4" and m == "completion")),
            )
        out_rows.append({**{k: v for k, v in r.items()}, "m": per})
    # registered consequences (UNBLIND RESULT; post_gamma4_t2000.md:18-19)
    consequence = {"survival_rate": "does not survive the inert-share correction",
                   "completion": "second exclusion bound"}
    return dict(rows=out_rows, foot=FOOT, consequence=consequence,
                metrics=[dict(k="completion", name="completion", axis="Δ completion (fraction of food collected)",
                              dom=[-0.068, 0.056]),
                         dict(k="survival_rate", name="survival", axis="Δ survival rate (fraction of agents alive at t = 256)",
                              dom=[-0.0115, 0.0185])])


CSS = r"""
.steps{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 6px}
.steps button.pill{font-size:12px}
.panels{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px 18px}
@media (max-width:760px){.panels{grid-template-columns:1fr}}
.panel h3{font-size:14px;margin:0 0 2px;font-weight:600}
.panel svg{display:block;width:100%;height:auto}
.foot{font-size:11px;color:var(--ink2);margin-top:6px}
.legend{display:flex;flex-wrap:wrap;gap:4px 14px;font-size:11px;color:var(--ink2);margin-top:6px;align-items:center}
.legend span{display:inline-flex;align-items:center;gap:5px}
g.row text{paint-order:stroke;stroke:var(--surface);stroke-width:3px;stroke-linejoin:round} g.row text.ct{stroke:none} g.row{cursor:default} g.row:focus{outline:none} g.row:focus .hit{stroke:var(--ink);stroke-width:1.5}
.dim{opacity:.5}
"""

BODY = r"""
<div class="wrap">
  <p class="sub">registered readings at θ*, matched budget T* = 1000 · intervals: Šidák 95 % (m = 2), conditional on the common eval draw</p>
  <div class="steps" role="group" aria-label="registered order">
    <button class="pill" id="prev" aria-label="previous rung">&#9664;</button>
    <span id="rungs" class="row"></span>
    <button class="pill" id="next" aria-label="next rung">&#9654;</button>
    <button class="pill" id="all" aria-pressed="false">show all</button>
  </div>
  <div class="ctl" role="group" aria-label="overlays">
    <button class="pill" id="tmde" aria-pressed="true"><svg width="16" height="10"><rect width="16" height="10" fill="var(--band)"/></svg>80 %-power MDE, ±X</button>
    <button class="pill" id="tfloor" aria-pressed="true"><svg width="16" height="10"><defs><pattern id="stip0" width="3" height="3" patternUnits="userSpaceOnUse"><circle cx="1.5" cy="1.5" r="0.7" fill="var(--muted)"/></pattern></defs><rect width="16" height="10" fill="url(#stip0)"/></svg>floor, ±1 sd(Γ) floor basis</button>
    <button class="pill" id="t60" aria-pressed="false">k = 60 prefix</button>
  </div>
  <div class="panels" id="panels"></div>
  <div class="legend">
    <span><svg width="26" height="10"><line x1="1" x2="25" y1="5" y2="5" stroke="var(--ink)" stroke-width="2"/><circle cx="13" cy="5" r="3.6" fill="var(--ink)"/></svg>estimate, Šidák 95 % CI</span>
    <span>● Γ · ○ Γ, k = 60 · ▲ Γ₄ · ◆ Γ₄′ · ■ B̂</span>
  </div>
  <div class="foot" id="foot"></div>
  <details class="tbl"><summary>table view</summary><div id="tbl"></div></details>
</div>
"""

JS = r"""
var D = JSON.parse(document.getElementById('data').textContent);
var S = {rung: 1, all: false, mde: true, floor: true, k60: false};
(function(){ var h=(location.hash||'').replace('#',''); h.split('&').forEach(function(kv){ var p=kv.split('=');
  if(p[0]==='rung'){ var r=parseInt(p[1],10); if(r>=1&&r<=4) S.rung=r; } if(p[0]==='all'&&p[1]==='1') S.all=true; if(p[0]==='k60'&&p[1]==='1') S.k60=true; }); })();
if(window.matchMedia && window.matchMedia('print').matches) S.all = true;
var RUNGS = [{n:1, t:'1  Γ'}, {n:2, t:'2  Γ₄'}, {n:3, t:'3  Γ₄′'}, {n:4, t:'4  B̂'}];
var rb = document.getElementById('rungs');
RUNGS.forEach(function(r){ var b = U.el('button', {'class':'pill', 'aria-pressed':'false'}, r.t);
  b.addEventListener('click', function(){ S.rung = r.n; S.all = false; render(); }); rb.appendChild(b); });
document.getElementById('prev').onclick = function(){ S.all=false; S.rung = Math.max(1, S.rung-1); render(); };
document.getElementById('next').onclick = function(){ S.all=false; S.rung = Math.min(4, S.rung+1); render(); };
document.getElementById('all').onclick = function(){ S.all = !S.all; if(S.all) S.rung = 4; render(); };
function tog(id, key){ var b = document.getElementById(id); b.onclick = function(){ S[key] = !S[key]; render(); }; }
tog('tmde','mde'); tog('tfloor','floor'); tog('t60','k60');
document.addEventListener('keydown', function(e){
  if(e.key==='ArrowRight'){ S.all=false; S.rung=Math.min(4,S.rung+1); render(); }
  if(e.key==='ArrowLeft'){ S.all=false; S.rung=Math.max(1,S.rung-1); render(); }
  if(/^[1-4]$/.test(e.key)){ S.all=false; S.rung=parseInt(e.key,10); render(); }
});
document.getElementById('foot').textContent = D.foot;

function marker(g, shape, x, y, r){
  var ink = 'var(--ink)', sf = 'var(--surface)';
  if(shape==='dot') g.appendChild(U.svg('circle', {cx:x, cy:y, r:r, fill:ink, stroke:sf, 'stroke-width':2}));
  if(shape==='ring') g.appendChild(U.svg('circle', {cx:x, cy:y, r:r, fill:sf, stroke:ink, 'stroke-width':2}));
  if(shape==='tri') g.appendChild(U.svg('path', {d:'M'+x+','+(y-r*1.25)+'L'+(x+r*1.15)+','+(y+r*0.8)+'L'+(x-r*1.15)+','+(y+r*0.8)+'Z', fill:ink, stroke:sf, 'stroke-width':1.5}));
  if(shape==='diamond') g.appendChild(U.svg('path', {d:'M'+x+','+(y-r*1.3)+'L'+(x+r*1.1)+','+y+'L'+x+','+(y+r*1.3)+'L'+(x-r*1.1)+','+y+'Z', fill:ink, stroke:sf, 'stroke-width':1.5}));
  if(shape==='square') g.appendChild(U.svg('rect', {x:x-r, y:y-r, width:2*r, height:2*r, fill:ink, stroke:sf, 'stroke-width':1.5}));
}
function chip(g, x, y, text, kind){
  var w = 10; for(var i=0;i<text.length;i++){ var ch = text[i]; w += (ch >= 'A' && ch <= 'Z') ? 7.4 : (ch===' ' ? 3.2 : 6.0); }
  var h = 16;
  var fill = kind==='fill' ? 'var(--chipfill)' : (kind==='weak' ? 'url(#stip)' : 'none');
  g.appendChild(U.svg('rect', {x:x, y:y-h+4, width:w, height:h, rx:8, fill:fill, stroke:'var(--ink)', 'stroke-width':1}));
  var t = U.svg('text', {x:x+w/2, y:y-0.5, 'text-anchor':'middle', 'font-size':10.5, 'font-weight':600, 'class':'ct'}, text);
  if(kind==='fill') t.setAttribute('style','fill:var(--chiptext)');
  g.appendChild(t); return w;
}
function visibleRows(){ return D.rows.filter(function(r){ return !(r.optional && !S.k60); }); }

function panel(mt){
  var W = 470, x0 = 14, x1 = W - 14, top = 26;
  var rows = visibleRows();
  var RH = function(r){ return 80 + (r.date ? 13 : 0) + (r.id==='G4' ? 24 : 0); };
  var H = top + rows.reduce(function(a, r){ return a + RH(r) + (r.family ? 18 : 0); }, 0) + 44;
  var svg = U.svg('svg', {viewBox:'0 0 '+W+' '+H, role:'img', 'aria-label': mt.name + ' contrasts in registered order'});
  var defs = U.svg('defs'); var pat = U.svg('pattern', {id:'stip', width:3, height:3, patternUnits:'userSpaceOnUse'});
  pat.appendChild(U.svg('circle', {cx:1.5, cy:1.5, r:0.75, fill:'var(--muted)'})); defs.appendChild(pat); svg.appendChild(defs);
  var X = function(v){ return x0 + (v - mt.dom[0])/(mt.dom[1]-mt.dom[0])*(x1-x0); };
  var step = (mt.k==='completion') ? 0.02 : 0.005, yAxis = H - 40;
  for(var v = Math.ceil(mt.dom[0]/step)*step; v <= mt.dom[1]+1e-12; v += step){
    var xv = X(v); svg.appendChild(U.svg('line', {x1:xv, x2:xv, y1:top-8, y2:yAxis, 'class': Math.abs(v)<1e-12 ? 'zero':'gl'}));
    svg.appendChild(U.svg('text', {x:xv, y:yAxis+14, 'text-anchor':'middle', 'class':'tick'}, (Math.abs(v)<1e-12?'0':(v>0?'+':'−')+Math.abs(v).toFixed(mt.k==='completion'?2:3))));
  }
  svg.appendChild(U.svg('text', {x:(x0+x1)/2, y:H-6, 'text-anchor':'middle', 'font-size':11.5, style:'fill:var(--ink2)'}, mt.axis));
  var y = top;
  rows.forEach(function(r){
    var d = r.m[mt.k], vis = S.all || r.rung <= S.rung, cur = !S.all && r.rung === S.rung;
    if(r.family){
      var fl = U.svg('text', {x:4, y:y+6, 'font-size':10.5, 'font-style':'italic', style:'fill:var(--muted)'}, r.family);
      svg.appendChild(fl); if(y > top) svg.appendChild(U.svg('line', {x1:2, x2:W-2, y1:y-6, y2:y-6, 'class':'ax'}));
      y += 18;
    }
    var g = U.svg('g', {'class':'row' + (vis && !cur && !S.all ? ' dim' : ''), tabindex: vis ? 0 : null});
    var bg = U.svg('rect', {x:2, y:y-2, width:W-4, height:RH(r)-8, rx:6, fill: cur ? 'var(--hover)' : 'transparent'}); g.appendChild(bg);
    var yy = y + 12;
    var idt = U.svg('text', {x:x0, y:yy, 'font-size':12.5});
    var t1 = U.svg('tspan', {'font-weight':600}, r.sym + '  ' + r.contrast); idt.appendChild(t1);
    g.appendChild(idt); yy += 14;
    g.appendChild(U.svg('text', {x:x0, y:yy, 'font-size':10.5, style:'fill:var(--ink2)'}, r.k + ' · ' + r.unit)); yy += 13;
    if(r.date){ g.appendChild(U.svg('text', {x:x0, y:yy, 'font-size':10.5, style:'fill:var(--muted)'}, r.date)); yy += 13; }
    if(!vis){ g.appendChild(U.svg('text', {x:x0, y:yy+14, 'font-size':11, style:'fill:var(--muted)'}, 'rung ' + r.rung + ': not yet read')); svg.appendChild(g); y += RH(r); return; }
    var cx = x0, cy = yy + 10;
    (r.chips||[]).forEach(function(c){ cx += chip(g, cx, cy, c, 'weak') + 4; });
    if(!r.noverdict) cx += chip(g, cx, cy, d.reject ? 'REJECT' : 'null', d.reject ? 'fill' : 'line') + 8;
    g.appendChild(U.svg('text', {x:cx, y:cy, 'font-size':11.5, 'class':'num'}, (d.est||'') + (d.ci ? '  ' + d.ci : '')));
    var yb = cy + 17;
    if(S.mde && d.band){ g.appendChild(U.svg('rect', {x:X(-d.X), y:yb-8, width:X(d.X)-X(-d.X), height:16, fill:'var(--band)'})); }
    if(S.floor && d.floor){ g.appendChild(U.svg('rect', {x:X(-d.floor), y:yb-8, width:X(d.floor)-X(-d.floor), height:16, fill:'url(#stip)'})); }
    g.appendChild(U.svg('line', {x1:X(d.lo), x2:X(d.hi), y1:yb, y2:yb, stroke:'var(--ink)', 'stroke-width':2}));
    [d.lo, d.hi].forEach(function(v){ g.appendChild(U.svg('line', {x1:X(v), x2:X(v), y1:yb-5, y2:yb+5, stroke:'var(--ink)', 'stroke-width':2})); });
    marker(g, r.shape, X(d.gamma), yb, 4.6);
    if(r.id==='G4'){ var cq = D.consequence[mt.k], kind = mt.k==='survival_rate' ? 'fill' : 'line';
      chip(g, x0, yb + 26, cq + (mt.k==='completion' && d.Xt ? ', X₄ = ' + d.Xt : ''), kind); }
    var lines = [[r.sym + ' = ' + r.contrast, '· ' + mt.name]];
    if(!r.noverdict) lines.push(((r.chips||[]).concat([d.reject ? 'REJECT' : 'null'])).join(' · ') + ' at Šidák z_α (m = 2)');
    else lines.push('no registered test: estimate and interval only');
    if(d.est) lines.push(['estimate', d.est]); if(d.ci) lines.push(['Šidák 95 % CI', d.ci]); if(d.z) lines.push(['z', d.z]);
    if(d.Xt) lines.push(['80 %-power MDE, X', d.Xt]);
    lines.push(r.k.replace(' †','') + ' · ' + r.unit);
    g.addEventListener('mousemove', function(e){ U.tip.show(lines, e.clientX, e.clientY); });
    g.addEventListener('mouseleave', function(){ U.tip.hide(); });
    g.addEventListener('focus', function(){ U.tipAt(g, lines); }); g.addEventListener('blur', function(){ U.tip.hide(); });
    svg.appendChild(g); y += RH(r);
  });
  return svg;
}
function table(){
  var host = document.getElementById('tbl'); U.clear(host); var tb = U.el('table');
  var hr = U.el('tr'); ['contrast','k','metric','reading','estimate','Šidák 95 % CI','z'].forEach(function(h){ hr.appendChild(U.el('th', null, h)); }); tb.appendChild(hr);
  visibleRows().forEach(function(r){ D.metrics.forEach(function(mt){ var d = r.m[mt.k], tr = U.el('tr');
    [r.sym + ' = ' + r.contrast, r.k.replace(' †',''), mt.name, r.noverdict ? '—' : ((r.chips||[]).join(' ') + ' ' + (d.reject?'REJECT':'null')).trim(), d.est||'', d.ci||'(plotted)', d.z||''].forEach(function(c){ tr.appendChild(U.el('td', null, c)); });
    tb.appendChild(tr); }); });
  host.appendChild(tb);
}
function render(){
  Array.prototype.forEach.call(rb.children, function(b, i){ b.setAttribute('aria-pressed', (!S.all && i+1===S.rung) ? 'true':'false'); });
  document.getElementById('all').setAttribute('aria-pressed', S.all?'true':'false');
  document.getElementById('tmde').setAttribute('aria-pressed', S.mde?'true':'false');
  document.getElementById('tfloor').setAttribute('aria-pressed', S.floor?'true':'false');
  document.getElementById('t60').setAttribute('aria-pressed', S.k60?'true':'false');
  var host = document.getElementById('panels'); U.clear(host);
  D.metrics.forEach(function(mt){ var p = U.el('div', {'class':'panel'}); p.appendChild(U.el('h3', null, mt.name)); p.appendChild(panel(mt)); host.appendChild(p); });
  table(); U.tip.hide(); if(window.__fit) window.__fit();
}
window.__redraw = render;
window.addEventListener('beforeprint', function(){ S.all = true; render(); });
render();
"""


def main():
    data = build_data()
    html = page("Registered readings", BODY, CSS, JS, data)
    out = OUT_HTML / "ladder_registered_readings.html"
    out.write_text(html, encoding="utf-8")
    hits = check_html(out)
    assert not hits, hits
    (OUT_DATA / "ladder_pending.json").write_text(json.dumps(ledger.pending(), indent=1, ensure_ascii=False) + "\n")
    print(f"{out.name}: {out.stat().st_size/1e3:.1f} KB; pending ledger rows: {len(ledger.pending())}")
    return data


if __name__ == "__main__":
    main()
