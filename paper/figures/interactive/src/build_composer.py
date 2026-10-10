"""F3 Training-mixture composer: what each arm's training distribution contained.

Display only: no slider, no prediction. Sources: the committed configs
che/configs/p6_iso.yaml, p6_iso4.yaml, p6_joint.yaml (mixture.components),
read with che.env.config.load_config. The behavioural reading of ISO's
δ-only third (no active stressor) is DES-8; the active share and the 2×
ratio are DES-14; the 3× ratio is DES-7.

Run from the repo root:  uv run python paper/figures/interactive/src/build_composer.py
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common_web import OUT_DATA, OUT_HTML, REPO, check_html, page  # noqa: E402

sys.path.insert(0, str(REPO))
from che.env.config import load_config  # noqa: E402

ARMS = [("ISO", "p6_iso.yaml"), ("ISO-4", "p6_iso4.yaml"), ("JOINT", "p6_joint.yaml")]


def frac(w: float) -> Fraction:
    f = Fraction(w).limit_denominator(12)
    assert abs(float(f) - w) < 1e-5, (w, f)
    return f


def arm_data(name: str, cfgfile: str) -> dict:
    cfg = load_config(str(REPO / "che/configs" / cfgfile))
    comps = []
    total = sum(c.weight for c in cfg.env.mixture.components)
    for c in cfg.env.mixture.components:
        w = frac(c.weight / total)
        comps.append(dict(name=c.name, w=str(w), wf=float(w), beta=c.beta, kA=c.kappa_A, kB=c.kappa_B,
                          d=c.delta, A=c.kappa_A > 0, B=c.kappa_B > 0, D=c.delta > 0))
    # behavioural type: delta inert (DES-8); nominal type: delta counted
    def typ(c, behavioural):
        if c["A"] and c["B"]:
            return "AB"
        if c["A"]:
            return "A"
        if c["B"]:
            return "B"
        return "F" if behavioural else "D"
    out = {"name": name, "components": comps}
    for view in ("beh", "nom"):
        shares = {}
        for c in comps:
            t = typ(c, view == "beh")
            shares[t] = shares.get(t, Fraction(0)) + Fraction(c["w"])
        mA = sum((Fraction(c["w"]) for c in comps if c["A"]), Fraction(0))
        mB = sum((Fraction(c["w"]) for c in comps if c["B"]), Fraction(0))
        active = sum((Fraction(c["w"]) for c in comps
                      if c["A"] or c["B"] or (view == "nom" and c["D"])), Fraction(0))
        out[view] = dict(shares={k: str(v) for k, v in shares.items()}, mA=str(mA), mB=str(mB),
                         active=str(active))
    return out


def build_data():
    arms = [arm_data(n, f) for n, f in ARMS]
    a = {x["name"]: x for x in arms}
    # Assert the ledger rows before anything is drawn.
    assert a["ISO"]["beh"]["mA"] == "1/3" and a["ISO"]["beh"]["mB"] == "1/3"          # DES-7
    assert a["JOINT"]["beh"]["mA"] == "1" and a["JOINT"]["beh"]["mB"] == "1"          # DES-7
    assert a["ISO"]["beh"]["shares"]["F"] == "1/3"                                     # DES-8
    assert a["ISO-4"]["beh"]["mA"] == "1/2" and a["ISO-4"]["beh"]["mB"] == "1/2"      # DES-14
    assert [a[k]["beh"]["active"] for k in ("ISO", "ISO-4", "JOINT")] == ["2/3", "1", "1"]  # DES-14
    assert Fraction(a["JOINT"]["beh"]["mA"]) / Fraction(a["ISO"]["beh"]["mA"]) == 3     # DES-7
    assert Fraction(a["JOINT"]["beh"]["mA"]) / Fraction(a["ISO-4"]["beh"]["mA"]) == 2   # DES-14
    assert a["ISO"]["nom"]["active"] == "1"  # config header "no-element 0.0000" (p6_iso.yaml:7)
    return dict(arms=arms, ratios={"JOINT": "3× ISO · 2× ISO-4"})


CSS = r"""
.grid{display:grid;grid-template-columns:64px minmax(0,1fr) 230px;gap:10px 14px;align-items:center}
.grid .arm{font-weight:600;font-size:14px}
.grid svg{display:block;width:100%;height:auto;overflow:visible}
.hd{font-size:11px;color:var(--muted)}
@media (max-width:700px){.grid{grid-template-columns:52px minmax(0,1fr)} .grid .meters{grid-column:2} .grid .hdm{display:none}}
.meters svg{max-width:230px}
.legend{display:flex;flex-wrap:wrap;gap:4px 14px;font-size:11px;color:var(--ink2);margin:10px 0 0}
.legend span{display:inline-flex;align-items:center;gap:5px}
"""

BODY = r"""
<div class="wrap">
  <p class="sub">training mixtures, read from the committed configs · each component is one episode type at one training severity · display only</p>
  <div class="ctl" role="group" aria-label="view">
    <span class="lab">δ-only episodes</span>
    <button class="pill" id="vbeh" aria-pressed="true">as certified: δ inert → fire-only</button>
    <button class="pill" id="vnom" aria-pressed="false">nominal: δ counted</button>
    <span class="lab" style="margin-left:8px">severity</span>
    <button class="pill" id="vsev" aria-pressed="false">split by β 0.43 / 0.70</button>
  </div>
  <div class="grid" id="grid"></div>
  <div class="legend" id="legend"></div>
  <p class="sub" style="margin-top:8px" id="note"></p>
  <details class="tbl"><summary>table view</summary><div id="tbl"></div></details>
</div>
"""

JS = r"""
var D = JSON.parse(document.getElementById('data').textContent);
var S = {view:'beh', sev:false};
var TYPES = [
  {k:'A', name:'Coupling A only'}, {k:'B', name:'Coupling B only'}, {k:'AB', name:'A + B together'},
  {k:'F', name:'fire-only (δ-only; no active stressor)'}, {k:'D', name:'δ only (comms denied)'}
];
function fr(s){ var p = s.split('/'); return p.length>1 ? parseInt(p[0],10)/parseInt(p[1],10) : parseFloat(s); }
function fill(defs, k){
  var id = 'pt' + k;
  if(!defs.querySelector('#'+id)){
    var p = U.svg('pattern', {id:id, width:7, height:7, patternUnits:'userSpaceOnUse'});
    var base = k==='A' ? 'var(--A)' : k==='B' ? 'var(--B)' : k==='AB' ? 'var(--A)' : 'var(--fireonly)';
    p.appendChild(U.svg('rect', {width:7, height:7, fill:base, 'fill-opacity': k==='F'||k==='D' ? 1 : 0.30}));
    if(k==='A' || k==='AB') p.appendChild(U.svg('path', {d:'M-1,8 L8,-1 M-1,1 L1,-1 M6,8 L8,6', stroke:'var(--A)', 'stroke-width':1.6}));
    if(k==='B' || k==='AB') p.appendChild(U.svg('path', {d:'M-1,-1 L8,8 M6,-1 L8,1 M-1,6 L1,8', stroke:'var(--B)', 'stroke-width':1.6}));
    if(k==='D') p.appendChild(U.svg('circle', {cx:3.5, cy:3.5, r:1.1, fill:'var(--ink2)'}));
    defs.appendChild(p);
  }
  return 'url(#' + id + ')';
}
function typOf(c){ var beh = S.view==='beh';
  if(c.A && c.B) return 'AB'; if(c.A) return 'A'; if(c.B) return 'B'; return beh ? 'F' : 'D'; }
function segs(arm){
  // ordered segments; with severity split, one per (type, beta)
  var order = ['A','B','AB','F','D'], out = [];
  order.forEach(function(t){
    var cs = arm.components.filter(function(c){ return typOf(c)===t; });
    if(!cs.length) return;
    if(S.sev){ cs.slice().sort(function(a,b){return a.beta-b.beta;}).forEach(function(c){ out.push({t:t, w:c.wf, comps:[c], beta:c.beta}); }); }
    else out.push({t:t, w:cs.reduce(function(a,c){return a+c.wf;},0), comps:cs});
  });
  return out;
}
function fracText(w){ var dens=[1,2,3,4,6,12]; for(var i=0;i<dens.length;i++){ var n=Math.round(w*dens[i]); if(Math.abs(n/dens[i]-w)<1e-9) return dens[i]===1 ? String(n) : n+'/'+dens[i]; } return w.toFixed(3); }
function bar(arm){
  var W = 520, H = 46, svg = U.svg('svg', {viewBox:'0 0 '+W+' '+H, role:'img', 'aria-label': arm.name + ' training mixture'}), defs = U.svg('defs'); svg.appendChild(defs);
  var x = 0, gap = 2;
  segs(arm).forEach(function(sg){
    var w = sg.w * W, label = TYPES.filter(function(t){return t.k===sg.t;})[0].name;
    if(S.view==='nom' && sg.t==='AB' && sg.comps.every(function(c){return c.D;})) label = 'A + B + δ together';
    var g = U.svg('g', {tabindex:0});
    g.appendChild(U.svg('rect', {x:x + (x>0?gap/2:0), y:0, width:Math.max(0, w - (x>0?gap/2:0) - (x+w<W-0.5?gap/2:0)), height:30, rx:3, fill:fill(defs, sg.t)}));
    var txt = fracText(sg.w) + (S.sev ? ' · β ' + sg.beta.toFixed(2) : '');
    if(w > txt.length*7 + 10){ var t = U.svg('text', {x:x + w/2, y:20, 'text-anchor':'middle', 'font-size':12, 'font-weight':600,
      style:'paint-order:stroke;stroke:var(--surface);stroke-width:3px'}, txt); g.appendChild(t); }
    var lines = [[arm.name, '· ' + label], ['share', fracText(sg.w)]];
    sg.comps.forEach(function(c){ lines.push(c.name + ': β ' + c.beta.toFixed(2) + ', κ_A ' + c.kA + ', κ_B ' + c.kB + ', δ ' + c.d + ', weight ' + c.w); });
    g.addEventListener('mousemove', function(e){ U.tip.show(lines, e.clientX, e.clientY); });
    g.addEventListener('mouseleave', function(){ U.tip.hide(); });
    g.addEventListener('focus', function(){ U.tipAt(g, lines); }); g.addEventListener('blur', function(){ U.tip.hide(); });
    svg.appendChild(g); x += w;
  });
  // tick marks at thirds and halves (axis 0..1)
  [0, 1/3, 1/2, 2/3, 1].forEach(function(v){ svg.appendChild(U.svg('line', {x1:v*W, x2:v*W, y1:33, y2:37, 'class':'ax'})); });
  ['0','1/3','1/2','2/3','1'].forEach(function(s, i){ var v=[0,1/3,1/2,2/3,1][i]; svg.appendChild(U.svg('text', {x:Math.min(W-6, Math.max(6, v*W)), y:46, 'text-anchor':'middle', 'class':'tick'}, s)); });
  return svg;
}
function meters(arm){
  var v = arm[S.view], W = 230, H = 60, svg = U.svg('svg', {viewBox:'0 0 '+W+' '+H, role:'img', 'aria-label': arm.name + ' per-stressor marginals and active share'}), defs = U.svg('defs'); svg.appendChild(defs);
  var rows = [{lab:'A', v:fr(v.mA), t:v.mA, f:fill(defs,'A')}, {lab:'B', v:fr(v.mB), t:v.mB, f:fill(defs,'B')}, {lab:'active', v:fr(v.active), t:v.active, f:'var(--ink)'}];
  var x0 = 46, x1 = 196;
  rows.forEach(function(r, i){ var y = 4 + i*19;
    svg.appendChild(U.svg('text', {x:0, y:y+10, 'font-size':11, style:'fill:var(--ink2)'}, r.lab));
    svg.appendChild(U.svg('rect', {x:x0, y:y, width:x1-x0, height:12, rx:2, fill:'var(--band)'}));
    if(r.v>0) svg.appendChild(U.svg('rect', {x:x0, y:y, width:(x1-x0)*r.v, height:12, rx:2, fill:r.f}));
    svg.appendChild(U.svg('text', {x:x1+6, y:y+10, 'font-size':11.5, 'font-weight':600, 'class':'num'}, r.t));
  });
  return svg;
}
function render(){
  document.getElementById('vbeh').setAttribute('aria-pressed', S.view==='beh'?'true':'false');
  document.getElementById('vnom').setAttribute('aria-pressed', S.view==='nom'?'true':'false');
  document.getElementById('vsev').setAttribute('aria-pressed', S.sev?'true':'false');
  var g = document.getElementById('grid'); U.clear(g);
  g.appendChild(U.el('div')); g.appendChild(U.el('div', {'class':'hd'}, 'share of training episodes, by episode type'));
  g.appendChild(U.el('div', {'class':'hd hdm'}, 'per-stressor marginal, and the share with an active stressor'));
  D.arms.forEach(function(arm){
    g.appendChild(U.el('div', {'class':'arm'}, arm.name));
    var b = U.el('div'); b.appendChild(bar(arm)); g.appendChild(b);
    var m = U.el('div', {'class':'meters'}); m.appendChild(meters(arm));
    if(arm.name==='JOINT') m.appendChild(U.el('div', {'class':'hd'}, 'per-stressor marginal: ' + D.ratios.JOINT));
    g.appendChild(m);
  });
  var lg = document.getElementById('legend'); U.clear(lg);
  TYPES.filter(function(t){ return S.view==='beh' ? t.k!=='D' : t.k!=='F'; }).forEach(function(t){
    var sp = U.el('span'), s = U.svg('svg', {width:18, height:12}), d = U.svg('defs'); s.appendChild(d);
    s.appendChild(U.svg('rect', {width:18, height:12, rx:2, fill:fill(d, t.k)})); sp.appendChild(s); sp.appendChild(document.createTextNode(t.name)); lg.appendChild(sp); });
  document.getElementById('note').textContent = S.view==='beh'
    ? 'as certified: δ inert under a frozen random-projection encoder at this scale · the fire burns in every episode'
    : 'nominal: δ counted, as the configs’ headers count it · the fire burns in every episode';
  table(); if(window.__fit) window.__fit();
}
function table(){
  var host = document.getElementById('tbl'); U.clear(host); var tb = U.el('table'), hr = U.el('tr');
  ['arm','component','β','κ_A','κ_B','δ','weight'].forEach(function(h){ hr.appendChild(U.el('th', null, h)); }); tb.appendChild(hr);
  D.arms.forEach(function(arm){ arm.components.forEach(function(c){ var tr = U.el('tr');
    [arm.name, c.name, c.beta.toFixed(2), c.kA, c.kB, c.d, c.w].forEach(function(v){ tr.appendChild(U.el('td', null, String(v))); }); tb.appendChild(tr); }); });
  host.appendChild(tb);
}
document.getElementById('vbeh').onclick = function(){ S.view='beh'; render(); };
document.getElementById('vnom').onclick = function(){ S.view='nom'; render(); };
document.getElementById('vsev').onclick = function(){ S.sev=!S.sev; render(); };
window.__redraw = render;
render();
"""


def main():
    data = build_data()
    out = OUT_HTML / "composer_training_mixtures.html"
    out.write_text(page("Training mixtures", BODY, CSS, JS, data), encoding="utf-8")
    hits = check_html(out)
    assert not hits, hits
    (OUT_DATA / "composer_data.json").write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")
    print(f"{out.name}: {out.stat().st_size/1e3:.1f} KB")


if __name__ == "__main__":
    main()
