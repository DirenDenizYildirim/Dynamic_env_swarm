"""F5 Secondary simplex: where the secondary arms sit relative to ISO, ISO-4 and
JOINT, and whether the plane fitted over them reaches JOINT.

Non-verdict-bearing throughout. Sources (committed, read-only):
  che/bench/results/phase6/secondary/secondary.json     design, metrics.*, mediation, replicate
  che/bench/results/phase6/post_unblind_analysis/post_gamma4_t2000.json   gamma4 (Γ₄, B̂)
Arm coordinates: sweep and identification from `design` (DES-9); ISO (p 0, n 1/3)
DES-7/DES-8; ISO-4 and sweep_c50_p000 (0, 0) and JOINT (1, 0) DES-14.
In (p, n), the per-stressor marginal is m = (1 + p − n)/2 (single-stressor
episodes split evenly between A and B): sweep m 0.5, identification m 0.4,
ISO m 1/3, JOINT m 1 — the iso-m lines are drawn as reference lines.

Run from the repo root:  uv run python paper/figures/interactive/src/build_simplex.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ledger  # noqa: E402
from common_web import OUT_DATA, OUT_HTML, REPO, check_html, page  # noqa: E402

P6 = REPO / "che/bench/results/phase6"
FIG = "F5 simplex"


def f4(x):
    return ("+" if x > 0 else ("−" if x < 0 else "")) + f"{abs(x):.4f}"


def ci(a):
    return f"[{f4(a[0])}, {f4(a[1])}]"


def build_data():
    ledger.reset()
    sc = json.loads((P6 / "secondary/secondary.json").read_text())
    g4 = json.loads((P6 / "post_unblind_analysis/post_gamma4_t2000.json").read_text())
    design = sc["design"]
    for a in design:  # m = (1 + p - n)/2 holds for every secondary arm
        assert abs((1 + a["p"] - a["n"]) / 2 - a["m"]) < 1e-9, a
    assert sc["mediation"]["void"] is True
    metrics = {}
    for m, name in (("survival_rate", "survival"), ("completion", "completion")):
        M = sc["metrics"][m]
        cf, dt, ep, kn = M["confound"], M["dose_trend"], M["endpoint_grade"], M["knee"]
        assert kn["underpowered"] is True
        surv = m == "survival_rate"
        src = f"secondary.json → metrics.{m}"

        def row(key, label, est, ci95, rowid, kind, what, extra_src="", est_rowid="same"):
            est_rowid = rowid if est_rowid == "same" else est_rowid
            return dict(key=key, label=label, g=est, lo=ci95[0] if ci95 else None, hi=ci95[1] if ci95 else None,
                        kind=kind,
                        est=ledger.stated(f4(est), est_rowid, figure=FIG, what=f"{name} {what}", source=src + extra_src),
                        ci=(ledger.stated(ci(ci95), rowid, figure=FIG, what=f"{name} {what} 95 % CI", source=src + extra_src)
                            if ci95 else None))
        rows_sec = [
            row("slope", "dose slope, sweep, per unit p", dt["ols_slope_per_unit_p"], dt["ols_slope_ci95"],
                "SEC-5" if surv else None, "sec", "dose slope", ".dose_trend"),
            row("endpoint", "endpoint, sweep p = 0.5 − p = 0", ep["endpoint_diff"], ep["ci95"],
                "SEC-5" if surv else None, "sec", "endpoint", ".endpoint_grade"),
            row("gp", "γ_p, per unit p (plane)", cf["gamma_p"], cf["gamma_p_ci95"],
                "SEC-1" if surv else None, "sec", "γ_p", ".confound"),
            row("gn", "γ_n, per unit n (plane)", cf["gamma_n"], cf["gamma_n_ci95"],
                "SEC-1" if surv else None, "sec", "γ_n", ".confound"),
            row("bound", "no-element share of the sweep's endpoint change", cf["bound_confound_share_of_sweep_change"],
                cf["bound_ci95"], "SEC-2" if surv else None, "sec", "bound", ".confound"),
        ]
        G4 = g4["gamma4"]["per_metric"][m]["gamma4"]
        BH = g4["gamma4"]["per_metric"][m]["b_hat"]
        G4p = sc["replicate"][m]["gamma4_prime"]
        rows_pred = [
            row("predJ", "plane prediction, JOINT − ISO-4 = γ_p × 1", cf["gamma_p"], cf["gamma_p_ci95"],
                "SEC-4" if surv else None, "pred", "plane prediction JOINT − ISO-4", ".confound.gamma_p"),
            row("g4", "Γ₄ = JOINT − ISO-4, measured", G4["gamma"], G4["ci_sidak"],
                "RES-6" if surv else None, "meas", "Γ₄", " (post_gamma4_t2000.json → gamma4)", est_rowid="RES-6"),
            row("g4p", "Γ₄′ = JOINT − sweep_c50_p000, measured", G4p["gamma"], G4p["ci_sidak"],
                "RES-8" if surv else None, "meas", "Γ₄′", ".replicate", est_rowid="RES-8"),
        ]
        if surv:
            # SEC-3: γ_n × (0 − 1/3), no committed interval -> point only
            pred_b = cf["gamma_n"] * (0 - 1 / 3)
            assert f4(pred_b) == "+0.0079"
            rows_pred += [
                dict(key="predB", label="plane prediction, ISO-4 − ISO = γ_n × (0 − 1/3)", g=pred_b, lo=None, hi=None,
                     kind="pred", est=ledger.stated("+0.0079", "SEC-3", figure=FIG, what="SEC-3", source="SEC-3"), ci=None),
                row("bh", "B̂ = ISO-4 − ISO, measured", BH["gamma"], BH["ci_sidak"], "RES-7", "meas", "B̂",
                    " (post_gamma4_t2000.json → gamma4)"),
            ]
            # ledger checks
            assert f4(cf["gamma_p"]) == "+0.0326" and ci(cf["gamma_p_ci95"]) == "[+0.0137, +0.0502]"
            assert f4(cf["gamma_n"]) == "−0.0237" and ci(cf["gamma_n_ci95"]) == "[−0.0419, −0.0057]"
            assert f4(cf["bound_confound_share_of_sweep_change"]) == "−0.0119"
            assert ci(cf["bound_ci95"]) == "[−0.0210, −0.0028]"
            assert f4(dt["ols_slope_per_unit_p"]) == "+0.0089" and ci(dt["ols_slope_ci95"]) == "[−0.0033, +0.0211]"
            assert f4(ep["endpoint_diff"]) == "+0.0048" and ci(ep["ci95"]) == "[−0.0021, +0.0117]"
            assert f4(G4["gamma"]) == "−0.0003" and f4(G4p["gamma"]) == "+0.0013" and f4(BH["gamma"]) == "+0.0098"
        means = {a["arm"]: dict(mean=a["mean"], fit=a["fit"]) for a in cf["arm_means_vs_plane"]}
        metrics[m] = dict(name=name, sec=rows_sec, pred=rows_pred, means=means,
                          dom=[-0.045, 0.056] if surv else [-0.17, 0.14])
    arms = [dict(arm=a["arm"], p=a["p"], n=round(a["n"], 6), m=a["m"],
                 kind="sweep" if a["arm"].startswith("sweep") else "ident") for a in design]
    refs = [dict(arm="ISO", p=0, n=1 / 3, m="1/3"), dict(arm="ISO-4 = sweep_c50_p000", p=0, n=0, m="0.5"),
            dict(arm="JOINT", p=1, n=0, m="1")]
    return dict(arms=arms, refs=refs, metrics=metrics,
                isom=[dict(m="1/3", c=-1 / 3), dict(m="0.4", c=-0.2), dict(m="0.5", c=0.0), dict(m="1", c=1.0)])


CSS = r"""
.top{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin-bottom:8px}
.cols{display:grid;grid-template-columns:minmax(0,0.9fr) minmax(0,1.1fr);gap:12px 22px;align-items:start}
@media (max-width:760px){.cols{grid-template-columns:1fr}}
.cols svg{display:block;width:100%;height:auto}
.cols h3{font-size:13px;margin:0 0 4px;font-weight:600}
.legend{display:flex;flex-wrap:wrap;gap:4px 14px;font-size:11px;color:var(--ink2);margin-top:6px;align-items:center}
.legend span{display:inline-flex;align-items:center;gap:5px}
g.it:focus{outline:none} g.it:focus .hit{stroke:var(--ink);stroke-width:1.5}
"""

BODY = r"""
<div class="wrap">
  <div class="top">
    <span class="chip line">secondary</span><span class="chip line">non-verdict-bearing</span>
    <span class="chip line">95 %, not family-corrected</span>
    <span class="chip weak">knee: UNDERPOWERED</span><span class="chip weak">mediation: VOID</span>
  </div>
  <div class="ctl" role="group" aria-label="metric">
    <span class="lab">metric</span>
    <button class="pill" id="msurv" aria-pressed="true">survival</button>
    <button class="pill" id="mcomp" aria-pressed="false">completion</button>
    <button class="pill" id="tpred" aria-pressed="true">plane prediction vs measured</button>
  </div>
  <div class="cols">
    <div><h3>training mixtures in (p, n); single-stressor share 1 − p − n</h3><div id="simplex"></div>
      <h3 style="margin-top:10px" id="mh">arm means at θ*, k = 20 per arm</h3><div id="means"></div></div>
    <div><h3 id="eh">estimates</h3><div id="est"></div></div>
  </div>
  <div class="legend">
    <span><svg width="12" height="12"><circle cx="6" cy="6" r="4.2" fill="var(--ink)"/></svg>sweep arm (m = 0.5)</span>
    <span><svg width="12" height="12"><rect x="2" y="2" width="8" height="8" fill="var(--surface)" stroke="var(--ink)" stroke-width="1.5"/></svg>identification arm (m = 0.4)</span>
    <span><svg width="22" height="10"><line x1="1" x2="21" y1="5" y2="5" stroke="var(--ink)" stroke-width="1"/><circle cx="11" cy="5" r="3.4" fill="var(--surface)" stroke="var(--ink)" stroke-width="1.4"/></svg>secondary estimate, 95 %</span>
    <span><svg width="22" height="10"><line x1="1" x2="21" y1="5" y2="5" stroke="var(--ink)" stroke-width="1"/><path d="M11,1 L15,5 L11,9 L7,5Z" fill="var(--surface)" stroke="var(--ink)" stroke-width="1.4"/></svg>plane prediction</span>
    <span><svg width="22" height="10"><line x1="1" x2="21" y1="5" y2="5" stroke="var(--ink)" stroke-width="2"/><path d="M11,1 L15,8 L7,8Z" fill="var(--ink)"/></svg>measured contrast, Šidák 95 %</span>
  </div>
  <details class="tbl"><summary>table view</summary><div id="tbl"></div></details>
</div>
"""

JS = r"""
var D = JSON.parse(document.getElementById('data').textContent);
var S = {m:'survival_rate', pred:true};
function hover(g, lines){
  g.addEventListener('mousemove', function(e){ U.tip.show(lines, e.clientX, e.clientY); });
  g.addEventListener('mouseleave', function(){ U.tip.hide(); });
  g.addEventListener('focus', function(){ U.tipAt(g, lines); }); g.addEventListener('blur', function(){ U.tip.hide(); });
}
function simplex(){
  var W = 380, H = 330, l = 46, r = 16, t = 14, b = 44, svg = U.svg('svg', {viewBox:'0 0 '+W+' '+H, role:'img', 'aria-label':'training simplex in p and n'});
  var X = function(p){ return l + p*(W-l-r); }, Y = function(n){ return t + (1-n)*(H-t-b); };
  svg.appendChild(U.svg('path', {d:'M'+X(0)+','+Y(0)+'L'+X(1)+','+Y(0)+'L'+X(0)+','+Y(1)+'Z', fill:'var(--band)'}));
  [0,0.25,0.5,0.75,1].forEach(function(v){
    svg.appendChild(U.svg('text', {x:X(v), y:H-b+15, 'text-anchor':'middle', 'class':'tick'}, String(v)));
    svg.appendChild(U.svg('text', {x:l-6, y:Y(v)+4, 'text-anchor':'end', 'class':'tick'}, String(v))); });
  svg.appendChild(U.svg('line', {x1:X(0), x2:X(1), y1:Y(0), y2:Y(0), 'class':'ax'}));
  svg.appendChild(U.svg('line', {x1:X(0), x2:X(0), y1:Y(0), y2:Y(1), 'class':'ax'}));
  svg.appendChild(U.svg('text', {x:(X(0)+X(1))/2, y:H-8, 'text-anchor':'middle', 'font-size':11.5, style:'fill:var(--ink2)'}, 'p, share of episodes with A + B together'));
  svg.appendChild(U.svg('text', {x:12, y:(Y(0)+Y(1))/2, 'text-anchor':'middle', 'font-size':11.5, style:'fill:var(--ink2)', transform:'rotate(-90 12 '+((Y(0)+Y(1))/2)+')'}, 'n, fire-only share'));
  // iso-marginal reference lines p − n = 2m − 1 inside the simplex
  D.isom.forEach(function(q){ var c = q.c; // p - n = c
    var pts = []; // intersections with p=0, n=0, p+n=1
    if(c<=0 && -c<=1) pts.push([0, -c]); if(c>=0 && c<=1) pts.push([c, 0]); var pp = (1+c)/2, nn = (1-c)/2; if(pp>=0&&pp<=1&&nn>=0&&nn<=1) pts.push([pp, nn]);
    if(pts.length<2 || (pts[0][0]===pts[1][0] && pts[0][1]===pts[1][1])) return;
    svg.appendChild(U.svg('line', {x1:X(pts[0][0]), y1:Y(pts[0][1]), x2:X(pts[1][0]), y2:Y(pts[1][1]), stroke:'var(--muted)', 'stroke-width':0.8}));
    var e = pts[pts.length-1]; svg.appendChild(U.svg('text', {x:X(e[0])+7, y:Y(e[1])+(q.m==='0.5'?12:-2), 'font-size':10, style:'fill:var(--muted)'}, 'm = ' + q.m)); });
  // sampled region: hull of the 8 arms
  svg.appendChild(U.svg('path', {d:'M'+X(0)+','+Y(0)+'L'+X(0.5)+','+Y(0.5)+'L'+X(0.4)+','+Y(0.6)+'L'+X(0)+','+Y(0.2)+'Z', fill:'var(--muted)', 'fill-opacity':0.18, stroke:'var(--muted)', 'stroke-width':0.8}));
  svg.appendChild(U.svg('text', {x:X(0.13), y:Y(0.29), 'font-size':10, style:'fill:var(--ink2);paint-order:stroke;stroke:var(--band);stroke-width:3px'}, 'sampled region'));
  D.arms.forEach(function(a){ var g = U.svg('g', {'class':'it', tabindex:0}), x = X(a.p), y = Y(a.n);
    g.appendChild(U.svg('circle', {'class':'hit', cx:x, cy:y, r:11, fill:'transparent'}));
    if(a.kind==='sweep') g.appendChild(U.svg('circle', {cx:x, cy:y, r:4.6, fill:'var(--ink)', stroke:'var(--surface)', 'stroke-width':2}));
    else g.appendChild(U.svg('rect', {x:x-4, y:y-4, width:8, height:8, fill:'var(--surface)', stroke:'var(--ink)', 'stroke-width':1.6}));
    hover(g, [[a.arm, ''], 'p ' + a.p + ' · n ' + (+a.n.toFixed(3)) + ' · m ' + a.m, 'k = 20']); svg.appendChild(g); });
  D.refs.forEach(function(a){ var g = U.svg('g', {'class':'it', tabindex:0}), x = X(a.p), y = Y(a.n);
    g.appendChild(U.svg('circle', {'class':'hit', cx:x, cy:y, r:12, fill:'transparent'}));
    g.appendChild(U.svg('circle', {cx:x, cy:y, r:8, fill:'none', stroke:'var(--ink)', 'stroke-width':1.8}));
    var lab = a.arm==='JOINT' ? 'JOINT, m = 1' : (a.arm==='ISO' ? 'ISO' : 'ISO-4');
    var tx = a.arm==='JOINT' ? x-10 : x+12, anchor = a.arm==='JOINT' ? 'end' : 'start', ty = a.arm==='JOINT' ? y-12 : (a.arm==='ISO' ? y+4 : y-10);
    g.appendChild(U.svg('text', {x:tx, y:ty, 'text-anchor':anchor, 'font-size':12, 'font-weight':600, style:'paint-order:stroke;stroke:var(--surface);stroke-width:3px'}, lab));
    hover(g, [[a.arm, ''], 'p ' + (+a.p.toFixed(3)) + ' · n ' + (a.arm==='ISO' ? '1/3' : a.n) + ' · m ' + a.m]); svg.appendChild(g); });
  return svg;
}
function meansPanel(){
  var mt = D.metrics[S.m], W = 380, H = 170, l = 46, r = 16, t = 10, b = 34;
  var vals = []; Object.keys(mt.means).forEach(function(k){ vals.push(mt.means[k].mean, mt.means[k].fit); });
  var lo = Math.min.apply(null, vals), hi = Math.max.apply(null, vals), pad = (hi-lo)*0.15; lo -= pad; hi += pad;
  var svg = U.svg('svg', {viewBox:'0 0 '+W+' '+H, role:'img', 'aria-label':'arm means against p'});
  var X = function(p){ return l + p/0.55*(W-l-r); }, Y = function(v){ return t + (hi-v)/(hi-lo)*(H-t-b); };
  [0,0.125,0.25,0.375,0.5].forEach(function(p){ svg.appendChild(U.svg('text', {x:X(p), y:H-b+14, 'text-anchor':'middle', 'class':'tick'}, String(p))); });
  svg.appendChild(U.svg('text', {x:(l+W-r)/2, y:H-4, 'text-anchor':'middle', 'font-size':11, style:'fill:var(--ink2)'}, 'p'));
  svg.appendChild(U.svg('line', {x1:l, x2:W-r, y1:H-b, y2:H-b, 'class':'ax'}));
  svg.appendChild(U.svg('text', {x:l-6, y:t+8, 'text-anchor':'end', 'class':'tick'}, 'higher'));
  svg.appendChild(U.svg('text', {x:l-6, y:H-b-2, 'text-anchor':'end', 'class':'tick'}, 'lower'));
  D.arms.forEach(function(a){ var d = mt.means[a.arm], x = X(a.p) + (a.kind==='ident'?5:-5);
    svg.appendChild(U.svg('line', {x1:x-7, x2:x+7, y1:Y(d.fit), y2:Y(d.fit), stroke:'var(--muted)', 'stroke-width':1.5}));
    var g = U.svg('g', {'class':'it', tabindex:0});
    g.appendChild(U.svg('circle', {'class':'hit', cx:x, cy:Y(d.mean), r:10, fill:'transparent'}));
    if(a.kind==='sweep') g.appendChild(U.svg('circle', {cx:x, cy:Y(d.mean), r:4.4, fill:'var(--ink)', stroke:'var(--surface)', 'stroke-width':2}));
    else g.appendChild(U.svg('rect', {x:x-4, y:Y(d.mean)-4, width:8, height:8, fill:'var(--surface)', stroke:'var(--ink)', 'stroke-width':1.6}));
    hover(g, [[a.arm, ''], 'arm mean (point) and the committed plane fit at this arm (grey tick)']); svg.appendChild(g); });
  return svg;
}
function estPanel(){
  var mt = D.metrics[S.m], rows = [].concat([{group:'secondary estimates, 95 %'}], mt.sec, S.pred ? [{group:'plane prediction vs measured'}].concat(mt.pred) : []);
  var W = 470, rowH = 40, top = 8, H = top + rows.reduce(function(a, r){ return a + (r.group ? 22 : rowH); }, 0) + 40, x0 = 14, x1 = W - 14;
  var svg = U.svg('svg', {viewBox:'0 0 '+W+' '+H, role:'img', 'aria-label':'secondary estimates and the plane prediction against measured contrasts'});
  var X = function(v){ return x0 + (v - mt.dom[0])/(mt.dom[1]-mt.dom[0])*(x1-x0); }, yAx = H - 32;
  var step = S.m==='survival_rate' ? 0.01 : 0.05;
  for(var v = Math.ceil(mt.dom[0]/step)*step; v <= mt.dom[1]+1e-12; v += step){ var xv = X(v);
    svg.appendChild(U.svg('line', {x1:xv, x2:xv, y1:top, y2:yAx, 'class': Math.abs(v)<1e-12 ? 'zero':'gl'}));
    svg.appendChild(U.svg('text', {x:xv, y:yAx+14, 'text-anchor':'middle', 'class':'tick'}, Math.abs(v)<1e-12 ? '0' : (v>0?'+':'−') + Math.abs(v).toFixed(2))); }
  svg.appendChild(U.svg('text', {x:(x0+x1)/2, y:H-4, 'text-anchor':'middle', 'font-size':11, style:'fill:var(--ink2)'}, 'Δ ' + mt.name + ' (fraction), or per unit p / n'));
  var y = top;
  rows.forEach(function(r){
    if(r.group){ svg.appendChild(U.svg('text', {x:x0, y:y+15, 'font-size':10.5, 'font-style':'italic', style:'fill:var(--muted)'}, r.group)); y += 22; return; }
    var g = U.svg('g', {'class':'it', tabindex:0}), yb = y + 26;
    g.appendChild(U.svg('rect', {'class':'hit', x:2, y:y, width:W-4, height:rowH-2, fill:'transparent', rx:5}));
    g.appendChild(U.svg('text', {x:x0, y:y+11, 'font-size':11.5, style:'paint-order:stroke;stroke:var(--surface);stroke-width:3px'}, r.label + (r.est ? '   ' + r.est + (r.ci ? ' ' + r.ci : '') : '')));
    var meas = r.kind==='meas';
    if(r.lo !== null){ g.appendChild(U.svg('line', {x1:X(r.lo), x2:X(r.hi), y1:yb, y2:yb, stroke:'var(--ink)', 'stroke-width': meas ? 2 : 1.1}));
      if(meas) [r.lo, r.hi].forEach(function(v){ g.appendChild(U.svg('line', {x1:X(v), x2:X(v), y1:yb-4, y2:yb+4, stroke:'var(--ink)', 'stroke-width':2})); }); }
    var x = X(r.g);
    if(r.kind==='sec') g.appendChild(U.svg('circle', {cx:x, cy:yb, r:4, fill:'var(--surface)', stroke:'var(--ink)', 'stroke-width':1.5}));
    if(r.kind==='pred') g.appendChild(U.svg('path', {d:'M'+x+','+(yb-5.5)+'L'+(x+5)+','+yb+'L'+x+','+(yb+5.5)+'L'+(x-5)+','+yb+'Z', fill:'var(--surface)', stroke:'var(--ink)', 'stroke-width':1.5}));
    if(meas){ var sh = r.key==='g4' ? 'M'+x+','+(yb-5.5)+'L'+(x+5)+','+(yb+4)+'L'+(x-5)+','+(yb+4)+'Z' : r.key==='g4p' ? 'M'+x+','+(yb-6)+'L'+(x+5)+','+yb+'L'+x+','+(yb+6)+'L'+(x-5)+','+yb+'Z' : 'M'+(x-4.5)+','+(yb-4.5)+'h9v9h-9Z';
      g.appendChild(U.svg('path', {d:sh, fill:'var(--ink)', stroke:'var(--surface)', 'stroke-width':1.5})); }
    var lines = [[r.label, '']]; if(r.est) lines.push(['estimate', r.est]); if(r.ci) lines.push([meas ? 'Šidák 95 % CI' : '95 % CI', r.ci]);
    lines.push(meas ? 'measured contrast; Šidák 95 %' : (r.kind==='pred' ? 'plane prediction; secondary, non-verdict-bearing' : 'secondary, non-verdict-bearing; 95 % bootstrap, not family-corrected'));
    hover(g, lines); svg.appendChild(g); y += rowH;
  });
  return svg;
}
function table(){
  var host = document.getElementById('tbl'); U.clear(host); var tb = U.el('table'), hr = U.el('tr');
  ['metric','row','estimate','interval'].forEach(function(h){ hr.appendChild(U.el('th', null, h)); }); tb.appendChild(hr);
  Object.keys(D.metrics).forEach(function(k){ var mt = D.metrics[k]; mt.sec.concat(mt.pred).forEach(function(r){ var tr = U.el('tr');
    [mt.name, r.label, r.est || '(plotted)', r.ci || (r.lo===null ? '—' : '(plotted)')].forEach(function(c){ tr.appendChild(U.el('td', null, c)); }); tb.appendChild(tr); }); });
  host.appendChild(tb);
}
function render(){
  document.getElementById('msurv').setAttribute('aria-pressed', S.m==='survival_rate'?'true':'false');
  document.getElementById('mcomp').setAttribute('aria-pressed', S.m==='completion'?'true':'false');
  document.getElementById('tpred').setAttribute('aria-pressed', S.pred?'true':'false');
  var a = document.getElementById('simplex'); U.clear(a); a.appendChild(simplex());
  var b = document.getElementById('means'); U.clear(b); b.appendChild(meansPanel());
  var c = document.getElementById('est'); U.clear(c); c.appendChild(estPanel());
  document.getElementById('mh').textContent = 'arm means at θ*, ' + D.metrics[S.m].name + ', k = 20 per arm (grey tick: committed plane fit)';
  document.getElementById('eh').textContent = D.metrics[S.m].name + ': estimates';
  table(); U.tip.hide(); if(window.__fit) window.__fit();
}
document.getElementById('msurv').onclick = function(){ S.m='survival_rate'; render(); };
document.getElementById('mcomp').onclick = function(){ S.m='completion'; render(); };
document.getElementById('tpred').onclick = function(){ S.pred=!S.pred; render(); };
window.__redraw = render; render();
"""


def main():
    data = build_data()
    out = OUT_HTML / "simplex_secondary.html"
    out.write_text(page("Secondary design", BODY, CSS, JS, data), encoding="utf-8")
    hits = check_html(out)
    assert not hits, hits
    (OUT_DATA / "simplex_pending.json").write_text(json.dumps(ledger.pending(), indent=1, ensure_ascii=False) + "\n")
    print(f"{out.name}: {out.stat().st_size/1e3:.1f} KB; pending: {len(ledger.pending())}")


if __name__ == "__main__":
    main()
