"""F6b Coupling A explorer (§5): collapse-seeded ignitions fall with severity
while their near-agent share stays flat; the two Prop. 3 handshake runs in
separate panels (they are two different runs, ledger CA-2 and CA-3).

Sources (committed, read-only):
  che/bench/results/e1/severity/severity.json   grids.m44.cells (κ_B 1.0 arm "kbL", and "kb0"),
                                                grids.m35.cells (κ_A on arm "kaL")
  che/bench/results/phase3/m33/prop3_L64.json   e_n_seeds, e_b_t, se_b_t, slope_through_origin, r2_through_origin
Ledger: CA-2, CA-3 (report text only, no data file), CA-4, CA-5, CA-6, CAL-3.

Run from the repo root:  uv run python paper/figures/interactive/src/build_coupling_a.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common_web import OUT_HTML, REPO, check_html, page  # noqa: E402

R = REPO / "che/bench/results"
SEV = [("low", "Low", 0.43), ("medium", "Medium", 0.49), ("high", "High", 0.70)]


def build_data():
    j = json.loads((R / "e1/severity/severity.json").read_text())
    m44, m35 = j["grids"]["m44"]["cells"], j["grids"]["m35"]["cells"]
    s44 = [m44[f"{k}|kbL"]["seeded_ignitions"] for k, *_ in SEV]
    s35 = [m35[f"{k}|kaL"]["seeded_ignitions"] for k, *_ in SEV]
    assert [f"{c['mean']:.2f}" for c in s44] == ["4.05", "3.41", "0.84"]                   # CA-4
    assert [f"{c['mean']:.2f}" for c in s35] == ["4.08", "3.42", "0.83"]                   # CA-5
    assert f"{s44[0]['mean'] / s44[2]['mean']:.2f}" == "4.83" and f"{s35[0]['mean'] / s35[2]['mean']:.2f}" == "4.92"
    shares = []
    for g, cells, arm, lab in (("m44", m44, "kbL", "m44, κ_B 1.0 arm"), ("m44", m44, "kb0", "m44, κ_B 0 arm"),
                               ("m35", m35, "kaL", "m35, κ_A on arm")):
        for k, name, beta in SEV:
            c = cells[f"{k}|{arm}"]["share"]
            shares.append(dict(sev=name, series=lab, mean=c["mean"], lo=c["min"], hi=c["max"]))
    assert len(shares) == 9
    lo, hi = min(s["mean"] for s in shares), max(s["mean"] for s in shares)
    assert f"{lo:.3f}" == "0.164" and f"{hi:.3f}" == "0.203"                                # CA-6
    p3 = json.loads((R / "phase3/m33/prop3_L64.json").read_text())
    assert f"{p3['r2_through_origin']:.3f}" == "0.998"                                     # CA-2
    assert round(p3["e_n_seeds"][-1] / p3["e_n_seeds"][0]) == 14                           # CA-2 "14× range"
    assert p3["grid_size"] == 64 and abs(p3["kappa_A"] - 0.02) < 1e-12 and abs(p3["f_weak"] - 0.4) < 1e-12
    sev = [dict(name=n, beta=b) for _, n, b in SEV]
    return dict(
        sev=sev,
        seeded=[dict(series="m44, κ_B 1.0 arm", vals=[dict(mean=c["mean"], lo=c["min"], hi=c["max"]) for c in s44],
                     text=["4.05", "3.41", "0.84"], fall="4.83×"),
                dict(series="m35, κ_A on arm", vals=[dict(mean=c["mean"], lo=c["min"], hi=c["max"]) for c in s35],
                     text=["4.08", "3.42", "0.83"], fall="4.92×")],
        shares=shares, share_range="[0.164, 0.203]",
        prop3=dict(x=p3["e_n_seeds"], y=p3["e_b_t"], se=p3["se_b_t"], slope=p3["slope_through_origin"],
                   r2="0.998", note="L = 64 dense sweep · κ_A 0.02 · f_weak 0.4 · no agents"),
        handshake=dict(lines=["matched-reference ratio 0.992, inside [0.90, 1.02]", "R² 0.9995",
                              "v2 purified test · L = 32 · CPU · κ_A 0.003",
                              "a different run from the L = 64 sweep; reported in text, no committed data file"]),
    )


CSS = r"""
.grid4{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px 22px}
@media (max-width:760px){.grid4{grid-template-columns:1fr}}
.grid4 svg{display:block;width:100%;height:auto}
.grid4 h3{font-size:13px;margin:0 0 2px;font-weight:600}
.grid4 .s{font-size:11px;color:var(--ink2);margin:0 0 4px}
.card{border:1px solid var(--axis);border-radius:8px;padding:10px 12px;font-size:12.5px;line-height:1.6}
"""

BODY = r"""
<div class="wrap">
  <p class="sub">Coupling A: structural collapse seeds fire · trained policies, single-configuration runs (Phases 3 and 4) · ranges: min–max over training seeds</p>
  <div class="grid4">
    <div><h3>collapse-seeded ignitions per episode</h3><p class="s">by severity of the training and evaluation configuration</p><div id="pA"></div></div>
    <div><h3>share of seeded ignitions inside an alive agent's 9 × 9 crop</h3><p class="s">9 cells: m44 both κ_B arms, m35 κ_A on</p><div id="pB"></div></div>
    <div><h3>Prop. 3 linearity, run 1 of 2</h3><p class="s" id="p3n"></p><div id="pC"></div></div>
    <div><h3>Prop. 3 matched-reference handshake, run 2 of 2</h3><div class="card" id="pD"></div></div>
  </div>
  <details class="tbl"><summary>table view</summary><div id="tbl"></div></details>
</div>
"""

JS = r"""
var D = JSON.parse(document.getElementById('data').textContent);
function hover(g, lines){ g.setAttribute('tabindex', 0);
  g.addEventListener('mousemove', function(e){ U.tip.show(lines, e.clientX, e.clientY); }); g.addEventListener('mouseleave', function(){ U.tip.hide(); });
  g.addEventListener('focus', function(){ U.tipAt(g, lines); }); g.addEventListener('blur', function(){ U.tip.hide(); }); }
function frame(W, H, l, b, t, r, ymin, ymax, yticks, fmt, ylab){
  var svg = U.svg('svg', {viewBox:'0 0 '+W+' '+H, role:'img'}), Y = function(v){ return t + (ymax-v)/(ymax-ymin)*(H-t-b); };
  yticks.forEach(function(v){ svg.appendChild(U.svg('line', {x1:l, x2:W-r, y1:Y(v), y2:Y(v), 'class':'gl'})); svg.appendChild(U.svg('text', {x:l-6, y:Y(v)+4, 'text-anchor':'end', 'class':'tick'}, fmt(v))); });
  svg.appendChild(U.svg('text', {x:12, y:(t+H-b)/2, 'text-anchor':'middle', 'font-size':11, style:'fill:var(--ink2)', transform:'rotate(-90 12 '+((t+H-b)/2)+')'}, ylab));
  return {svg:svg, Y:Y};
}
function panelA(){
  var W = 420, H = 250, l = 48, b = 40, t = 40, r = 14, f = frame(W, H, l, b, t, r, 0, 4.6, [0,1,2,3,4], String, 'per episode'), svg = f.svg, Y = f.Y;
  var X = function(i){ return l + 40 + i*((W-l-r-80)/2); };
  D.sev.forEach(function(s, i){ svg.appendChild(U.svg('text', {x:X(i), y:H-b+16, 'text-anchor':'middle', 'class':'tick'}, s.name)); svg.appendChild(U.svg('text', {x:X(i), y:H-b+29, 'text-anchor':'middle', 'class':'tick'}, 'β ' + s.beta.toFixed(2))); });
  D.seeded.forEach(function(sr, j){ var off = j ? 9 : -9;
    sr.vals.forEach(function(v, i){ var g = U.svg('g'), x = X(i) + off;
      g.appendChild(U.svg('line', {x1:x, x2:x, y1:Y(v.lo), y2:Y(v.hi), stroke:'var(--ink)', 'stroke-width':1.5}));
      if(j===0) g.appendChild(U.svg('circle', {cx:x, cy:Y(v.mean), r:4.4, fill:'var(--ink)', stroke:'var(--surface)', 'stroke-width':1.5}));
      else g.appendChild(U.svg('rect', {x:x-4, y:Y(v.mean)-4, width:8, height:8, fill:'var(--surface)', stroke:'var(--ink)', 'stroke-width':1.5}));
      hover(g, [[sr.series, '· ' + D.sev[i].name], ['seeded ignitions per episode', sr.text[i]]]); svg.appendChild(g); });
    svg.appendChild(U.svg('text', {x:l+4, y:12 + j*14, 'font-size':11}, (j ? '■ ' : '● ') + sr.series + ' · Low / High ' + sr.fall));
  });
  return svg;
}
function panelB(){
  var W = 420, H = 250, l = 48, b = 40, t = 12, r = 96, f = frame(W, H, l, b, t, r, 0.10, 0.25, [0.10,0.15,0.20,0.25], function(v){ return v.toFixed(2); }, 'share'), svg = f.svg, Y = f.Y;
  var X = function(i){ return l + 30 + i*((W-l-r-60)/2); };
  var lo = Math.min.apply(null, D.shares.map(function(s){return s.mean;})), hi = Math.max.apply(null, D.shares.map(function(s){return s.mean;}));
  svg.appendChild(U.svg('rect', {x:l, y:Y(hi), width:W-l-r, height:Y(lo)-Y(hi), fill:'var(--band)'}));
  svg.appendChild(U.svg('text', {x:W-r+6, y:(Y(hi)+Y(lo))/2+4, 'font-size':11}, D.share_range));
  svg.appendChild(U.svg('text', {x:W-r+6, y:(Y(hi)+Y(lo))/2+18, 'font-size':10, style:'fill:var(--muted)'}, 'range, 9 cells'));
  D.sev.forEach(function(s, i){ svg.appendChild(U.svg('text', {x:X(i), y:H-b+16, 'text-anchor':'middle', 'class':'tick'}, s.name)); });
  var ser = ['m44, κ_B 1.0 arm', 'm44, κ_B 0 arm', 'm35, κ_A on arm'];
  D.shares.forEach(function(s){ var j = ser.indexOf(s.series), i = D.sev.findIndex(function(q){return q.name===s.sev;}), x = X(i) + (j-1)*12, g = U.svg('g');
    g.appendChild(U.svg('line', {x1:x, x2:x, y1:Y(s.lo), y2:Y(s.hi), stroke:'var(--muted)', 'stroke-width':1.2}));
    if(j===0) g.appendChild(U.svg('circle', {cx:x, cy:Y(s.mean), r:4, fill:'var(--ink)', stroke:'var(--surface)', 'stroke-width':1.5}));
    if(j===1) g.appendChild(U.svg('circle', {cx:x, cy:Y(s.mean), r:4, fill:'var(--surface)', stroke:'var(--ink)', 'stroke-width':1.5}));
    if(j===2) g.appendChild(U.svg('rect', {x:x-4, y:Y(s.mean)-4, width:8, height:8, fill:'var(--surface)', stroke:'var(--ink)', 'stroke-width':1.5}));
    hover(g, [[s.series, '· ' + s.sev], 'inside the range ' + D.share_range]); svg.appendChild(g); });
  svg.appendChild(U.svg('text', {x:l+4, y:t+12, 'font-size':10, style:'fill:var(--muted)'}, '● m44 κ_B 1.0 · ○ m44 κ_B 0 · ■ m35 κ_A on'));
  return svg;
}
function panelC(){
  var p = D.prop3, W = 420, H = 250, l = 54, b = 40, t = 12, r = 14, f = frame(W, H, l, b, t, r, 0, 500, [0,100,200,300,400,500], String, 'E[B_T], burnt cells at the horizon'), svg = f.svg, Y = f.Y;
  var X = function(v){ return l + v/11*(W-l-r); };
  [0,2,4,6,8,10].forEach(function(v){ svg.appendChild(U.svg('text', {x:X(v), y:H-b+16, 'text-anchor':'middle', 'class':'tick'}, String(v))); });
  svg.appendChild(U.svg('text', {x:(l+W-r)/2, y:H-6, 'text-anchor':'middle', 'font-size':11, style:'fill:var(--ink2)'}, 'E[N_seeds], collapse-seeded ignitions per run'));
  var xe = Math.min(11, 500/p.slope); svg.appendChild(U.svg('line', {x1:X(0), y1:Y(0), x2:X(xe), y2:Y(p.slope*xe), stroke:'var(--ink2)', 'stroke-width':1.2}));
  p.x.forEach(function(x, i){ var g = U.svg('g');
    g.appendChild(U.svg('line', {x1:X(x), x2:X(x), y1:Y(p.y[i]-p.se[i]), y2:Y(p.y[i]+p.se[i]), stroke:'var(--ink)', 'stroke-width':1.5}));
    g.appendChild(U.svg('circle', {cx:X(x), cy:Y(p.y[i]), r:4.2, fill:'var(--ink)', stroke:'var(--surface)', 'stroke-width':1.5}));
    hover(g, [['λ₀ sweep point', ''], 'mean ± 1 SE']); svg.appendChild(g); });
  svg.appendChild(U.svg('text', {x:l+10, y:t+14, 'font-size':11.5}, 'committed through-origin fit, R² ' + p.r2));
  return svg;
}
function render(){
  [['pA', panelA], ['pB', panelB], ['pC', panelC]].forEach(function(q){ var h = document.getElementById(q[0]); U.clear(h); h.appendChild(q[1]()); });
  document.getElementById('p3n').textContent = D.prop3.note;
  var c = document.getElementById('pD'); U.clear(c); D.handshake.lines.forEach(function(s, i){ c.appendChild(U.el('div', i < 2 ? {style:'font-weight:600'} : {style:'color:var(--ink2)'}, s)); });
  var host = document.getElementById('tbl'); U.clear(host); var tb = U.el('table'), hr = U.el('tr');
  ['series','Low','Medium','High','Low / High'].forEach(function(h){ hr.appendChild(U.el('th', null, h)); }); tb.appendChild(hr);
  D.seeded.forEach(function(sr){ var tr = U.el('tr'); [sr.series].concat(sr.text).concat([sr.fall]).forEach(function(v){ tr.appendChild(U.el('td', null, v)); }); tb.appendChild(tr); });
  host.appendChild(tb); if(window.__fit) window.__fit();
}
window.__redraw = render; render();
"""


def main():
    data = build_data()
    out = OUT_HTML / "coupling_a_explorer.html"
    out.write_text(page("Coupling A explorer", BODY, CSS, JS, data), encoding="utf-8")
    hits = check_html(out)
    assert not hits, hits
    print(f"{out.name}: {out.stat().st_size / 1e3:.1f} KB")
    return data


if __name__ == "__main__":
    main()
