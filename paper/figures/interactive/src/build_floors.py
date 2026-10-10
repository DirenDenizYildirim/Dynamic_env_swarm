"""F6c Floors explorer (§8): floors are per metric, per card, per artifact, and
grow with run length; and the grid's seed dispersion against its floor.

Every panel states its confound on the figure (METH-1: card, code tree and
config differ between the two Medium floors; METH-5: run length and box
differ between the two floor sets).

Sources (committed, read-only):
  METH-1  che/bench/results/phase5/m51e/reproducibility_floor.txt,
          che/bench/results/phase5/m55/reproducibility_floor_medium.txt,
          cards: che/bench/results/phase5/phase5_report.md:1011-1014
  METH-2  che/bench/results/phase6/m60/m60_report.md (comparison table)
  METH-5  che/bench/results/phase6/m62/floors.json (T = 500), m62b/floors.json (T = 1000)
  HW-1    che/bench/results/phase6/unblind/unblind.json → beat_reproducibility

Run from the repo root:  uv run python paper/figures/interactive/src/build_floors.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common_web import OUT_HTML, REPO, check_html, page  # noqa: E402

R = REPO / "che/bench/results"


def floor_txt(p: Path) -> dict:
    out = {}
    for line in p.read_text().splitlines():
        m = re.match(r"\s+(completion|survival_rate)\s+([\d.]+)\s+([\d.]+)", line)
        if m:
            out[m.group(1)] = float(m.group(3))
    return out


def build_data():
    a = floor_txt(R / "phase5/m51e/reproducibility_floor.txt")
    b = floor_txt(R / "phase5/m55/reproducibility_floor_medium.txt")
    assert f"{a['completion']:.4f}" == "0.0145" and f"{b['completion']:.4f}" == "0.0399"   # METH-1
    assert f"{a['survival_rate']:.4f}" == "0.0129" and f"{b['survival_rate']:.4f}" == "0.0130"
    rep = (R / "phase5/phase5_report.md").read_text()
    assert "| metric | M5.1e (5090) | M5.5 (PRO 6000) | ratio |" in rep
    m60 = (R / "phase6/m60/m60_report.md").read_text()
    for row in ("| baseline vs baseline (same code) | 4 | **0** |", "| traced vs traced (same code) | 4 | **1** |",
                "| traced vs baseline | 5 | **2** |"):
        assert row in m60, row
    f500 = json.loads((R / "phase6/m62/floors.json").read_text())
    f1000 = json.loads((R / "phase6/m62b/floors.json").read_text())
    growth = {k: f1000[k]["completion"]["sd"] / f500[k]["completion"]["sd"] for k in ("iso", "joint")}
    assert f"{growth['iso']:.1f}" == "2.1" and f"{growth['joint']:.1f}" == "5.2"            # METH-5
    ub = json.loads((R / "phase6/unblind/unblind.json").read_text())["beat_reproducibility"]
    hw = {m: dict(iso=ub[m]["ratio_seed_over_floor_iso"], joint=ub[m]["ratio_seed_over_floor_joint"],
                  gamma=ub[m]["gamma_over_floor_sd"]) for m in ("completion", "survival_rate")}
    assert [f"{hw['completion']['iso']:.2f}", f"{hw['completion']['joint']:.2f}",
            f"{hw['survival_rate']['iso']:.2f}", f"{hw['survival_rate']['joint']:.2f}"] == ["1.12", "1.09", "1.25", "1.19"]
    assert f"{hw['survival_rate']['gamma']:.2f}" == "5.40"                                   # HW-1
    return dict(
        card=dict(runs=[dict(name="M5.1e · RTX 5090", completion=a["completion"], survival=a["survival_rate"],
                             ct="0.0145", st="0.0129"),
                        dict(name="M5.5 · RTX PRO 6000", completion=b["completion"], survival=b["survival_rate"],
                             ct="0.0399", st="0.0130")],
                  ratio="2.75×",
                  confound="card, code tree and config all differ between the two runs (M5.5 records R_comm 16; M5.1e predates the R_comm lock)",
                  sub="Medium, identical runs per floor, same seed: nondeterminism only"),
        artifact=dict(rows=[dict(name="baseline vs baseline", n=4, diff=0, text="0 of 760 field digests differ, in 4 of 4"),
                            dict(name="traced vs traced", n=4, diff=1, text="1 of 4: masked_frac, masked_danger_sum"),
                            dict(name="traced vs baseline", n=5, diff=2, text=None)],
                      sub="M6.0 GPU rerun comparisons, severity_high seed 0; no trajectory field differed in any comparison"),
        length=dict(arms=[dict(name="ISO", v500=f500["iso"]["completion"]["values"], v1000=f1000["iso"]["completion"]["values"],
                               g="2.1×"),
                          dict(name="JOINT", v500=f500["joint"]["completion"]["values"], v1000=f1000["joint"]["completion"]["values"],
                               g="5.2×")],
                    confound="run length and box both differ: the T = 500 and T = 1000 floors ran on different RTX PRO 6000 boxes",
                    sub="completion floor, identical runs per arm and length, same seed"),
        beat=dict(rows=[dict(name="completion · ISO", v=hw["completion"]["iso"], t="1.12×"),
                        dict(name="completion · JOINT", v=hw["completion"]["joint"], t="1.09×"),
                        dict(name="survival · ISO", v=hw["survival_rate"]["iso"], t="1.25×"),
                        dict(name="survival · JOINT", v=hw["survival_rate"]["joint"], t="1.19×")],
                  gamma=dict(v=hw["survival_rate"]["gamma"], t="5.40×"),
                  sub="the confirmatory grid (k = 72 per arm): seed sd over the rerun floor; survival Γ over the floor-basis sd(Γ)"),
    )


CSS = r"""
#panel svg{display:block;width:100%;height:auto;max-width:760px}
.conf{font-size:12px;color:var(--ink);border-left:3px solid var(--ink);padding:2px 8px;margin:8px 0 0}
"""

BODY = r"""
<div class="wrap">
  <div class="ctl" role="tablist" aria-label="floor exhibits" id="tabs"></div>
  <p class="sub" id="sub"></p>
  <div id="panel"></div>
  <p class="conf" id="conf"></p>
</div>
"""

JS = r"""
var D = JSON.parse(document.getElementById('data').textContent);
var TABS = [{k:'card', t:'per card (and tree, and config)'}, {k:'artifact', t:'per artifact'}, {k:'length', t:'per run length'}, {k:'beat', t:'the grid against its floor'}];
var S = {tab: 'card'};
(function(){ var h=(location.hash||'').replace('#',''); TABS.forEach(function(x){ if(h==='tab='+x.k) S.tab=x.k; }); })();
var tabs = document.getElementById('tabs');
TABS.forEach(function(x){ var b = U.el('button', {'class':'pill', role:'tab', 'aria-selected':'false', 'aria-pressed':'false'}, x.t);
  b.onclick = function(){ S.tab = x.k; render(); }; tabs.appendChild(b); });
function txt(svg, x, y, s, o){ var a = {x:x, y:y, 'font-size':11.5}; for(var k in (o||{})) a[k]=o[k]; svg.appendChild(U.svg('text', a, s)); }
function hover(g, lines){ g.setAttribute('tabindex', 0);
  g.addEventListener('mousemove', function(e){ U.tip.show(lines, e.clientX, e.clientY); }); g.addEventListener('mouseleave', function(){ U.tip.hide(); });
  g.addEventListener('focus', function(){ U.tipAt(g, lines); }); g.addEventListener('blur', function(){ U.tip.hide(); }); }
function card(){
  var d = D.card, W = 620, H = 220, svg = U.svg('svg', {viewBox:'0 0 '+W+' '+H, role:'img', 'aria-label':'Medium reproducibility floors on two runs'});
  var x0 = 170, x1 = 560, X = function(v){ return x0 + v/0.045*(x1-x0); };
  [0,0.01,0.02,0.03,0.04].forEach(function(v){ svg.appendChild(U.svg('line', {x1:X(v), x2:X(v), y1:18, y2:H-34, 'class':'gl'})); txt(svg, X(v), H-18, v.toFixed(2), {'text-anchor':'middle', 'class':'tick'}); });
  txt(svg, (x0+x1)/2, H-2, 'rerun floor: sd over identical runs', {'text-anchor':'middle', style:'fill:var(--ink2)', 'font-size':11});
  [['completion','completion','ct'],['survival','survival rate','st']].forEach(function(m, i){
    var y = 30 + i*86; txt(svg, 6, y+4, m[1], {'font-weight':600});
    d.runs.forEach(function(r, j){ var yy = y + 16 + j*26, v = r[m[0]], g = U.svg('g');
      g.appendChild(U.svg('text', {x:6, y:yy+5, 'font-size':11, style:'fill:var(--ink2)'}, r.name));
      g.appendChild(U.svg('rect', {x:x0, y:yy-7, width:X(v)-x0, height:14, rx:3, fill: j ? 'var(--ink)' : 'var(--muted)'}));
      g.appendChild(U.svg('text', {x:X(v)+6, y:yy+5, 'font-size':11.5, 'font-weight':600, 'class':'num'}, r[m[2]]));
      hover(g, [[r.name, '· ' + m[1]], ['floor (sd)', r[m[2]]], 'identical runs, same seed']); svg.appendChild(g); });
    if(i===0) txt(svg, X(0.0399)+52, y+33, d.ratio, {'font-size':11, style:'fill:var(--ink2)'});
  });
  return svg;
}
function artifact(){
  var d = D.artifact, W = 620, H = 170, svg = U.svg('svg', {viewBox:'0 0 '+W+' '+H, role:'img', 'aria-label':'per-artifact rerun comparisons'});
  txt(svg, 190, 16, 'each square: one rerun comparison · filled: field digests differed', {'font-size':10.5, style:'fill:var(--muted)'});
  d.rows.forEach(function(r, i){ var y = 44 + i*42, g = U.svg('g');
    g.appendChild(U.svg('text', {x:6, y:y+5, 'font-size':12, 'font-weight':600}, r.name));
    for(var k=0;k<r.n;k++){ g.appendChild(U.svg('rect', {x:190+k*26, y:y-10, width:20, height:20, rx:3, fill: k < r.diff ? 'var(--ink)' : 'var(--surface)', stroke:'var(--ink)', 'stroke-width':1.3})); }
    if(r.text) g.appendChild(U.svg('text', {x:190+5*26+12, y:y+5, 'font-size':11, style:'fill:var(--ink2)'}, r.text));
    hover(g, r.text ? [[r.name, ''], r.text] : [[r.name, '']]); svg.appendChild(g); });
  return svg;
}
function length(){
  var d = D.length, W = 620, H = 250, svg = U.svg('svg', {viewBox:'0 0 '+W+' '+H, role:'img', 'aria-label':'completion floor reps at two run lengths'});
  var all = []; d.arms.forEach(function(a){ all = all.concat(a.v500, a.v1000); });
  var lo = Math.min.apply(null, all) - 0.01, hi = Math.max.apply(null, all) + 0.01, y0 = 20, y1 = H-40;
  var Y = function(v){ return y1 - (v-lo)/(hi-lo)*(y1-y0); };
  txt(svg, 6, y0+6, 'completion,', {'font-size':10.5, style:'fill:var(--muted)'}); txt(svg, 6, y0+19, 'one dot per run', {'font-size':10.5, style:'fill:var(--muted)'});
  for(var v = Math.ceil(lo*50)/50; v <= hi; v += 0.02){ svg.appendChild(U.svg('line', {x1:130, x2:W-20, y1:Y(v), y2:Y(v), 'class':'gl'})); txt(svg, 124, Y(v)+4, v.toFixed(2), {'text-anchor':'end', 'class':'tick'}); }
  d.arms.forEach(function(a, i){ var xb = 170 + i*230;
    txt(svg, xb+60, H-6, a.name + ' · floor growth ' + a.g, {'text-anchor':'middle', 'font-weight':600});
    [['T = 500', a.v500, 0], ['T = 1000', a.v1000, 1]].forEach(function(s){ var x = xb + s[2]*120, g = U.svg('g');
      txt(svg, x, H-24, s[0], {'text-anchor':'middle', 'class':'tick'});
      var mean = s[1].reduce(function(p,c){return p+c;},0)/s[1].length;
      s[1].slice().sort(function(p,q){return p-q;}).forEach(function(v, k){ g.appendChild(U.svg('circle', {cx:x + ((k%2)?6:-6), cy:Y(v), r:3.6, fill: s[2] ? 'var(--ink)' : 'var(--surface)', stroke:'var(--ink)', 'stroke-width':1.3})); });
      g.appendChild(U.svg('line', {x1:x-18, x2:x+18, y1:Y(mean), y2:Y(mean), stroke:'var(--muted)', 'stroke-width':1.5}));
      hover(g, [[a.name + ', ' + s[0], ''], 'identical runs, same seed', 'grey tick: their mean']); svg.appendChild(g); });
  });
  return svg;
}
function beat(){
  var d = D.beat, W = 620, H = 210, svg = U.svg('svg', {viewBox:'0 0 '+W+' '+H, role:'img', 'aria-label':'seed dispersion over the rerun floor'});
  var x0 = 170, x1 = 560, X = function(v){ return x0 + v/6*(x1-x0); };
  [0,1,2,3,4,5,6].forEach(function(v){ svg.appendChild(U.svg('line', {x1:X(v), x2:X(v), y1:10, y2:H-34, 'class': v===1 ? 'zero' : 'gl'})); txt(svg, X(v), H-18, v + '×', {'text-anchor':'middle', 'class':'tick'}); });
  txt(svg, X(1)+4, 16, '1× = the floor', {'font-size':10.5, style:'fill:var(--muted)'});
  d.rows.concat([{name:'survival Γ / floor-basis sd(Γ)', v:d.gamma.v, t:d.gamma.t, g:1}]).forEach(function(r, i){ var y = 34 + i*30 + (r.g ? 10 : 0), g = U.svg('g');
    g.appendChild(U.svg('text', {x:6, y:y+4, 'font-size':11, style:'fill:var(--ink2)'}, r.name));
    g.appendChild(U.svg('rect', {x:x0, y:y-7, width:X(r.v)-x0, height:14, rx:3, fill: r.g ? 'var(--ink)' : 'var(--muted)'}));
    g.appendChild(U.svg('text', {x:X(r.v)+6, y:y+4, 'font-size':11.5, 'font-weight':600, 'class':'num'}, r.t));
    hover(g, [[r.name, r.t]]); svg.appendChild(g); });
  return svg;
}
function render(){
  Array.prototype.forEach.call(tabs.children, function(b, i){ var on = TABS[i].k===S.tab; b.setAttribute('aria-selected', on?'true':'false'); b.setAttribute('aria-pressed', on?'true':'false'); });
  var host = document.getElementById('panel'); U.clear(host); var d = D[S.tab];
  host.appendChild({card:card, artifact:artifact, length:length, beat:beat}[S.tab]());
  document.getElementById('sub').textContent = d.sub;
  var cf = document.getElementById('conf'); cf.textContent = d.confound ? 'confound: ' + d.confound : ''; cf.style.display = d.confound ? '' : 'none';
  U.tip.hide(); if(window.__fit) window.__fit();
}
document.addEventListener('keydown', function(e){ var i = TABS.findIndex(function(x){return x.k===S.tab;});
  if(e.key==='ArrowRight'){ S.tab = TABS[Math.min(3,i+1)].k; render(); } if(e.key==='ArrowLeft'){ S.tab = TABS[Math.max(0,i-1)].k; render(); } });
window.__redraw = render; render();
"""


def main():
    data = build_data()
    out = OUT_HTML / "floors_explorer.html"
    out.write_text(page("Floors explorer", BODY, CSS, JS, data), encoding="utf-8")
    hits = check_html(out)
    assert not hits, hits
    print(f"{out.name}: {out.stat().st_size / 1e3:.1f} KB")


if __name__ == "__main__":
    main()
