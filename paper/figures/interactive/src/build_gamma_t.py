"""F4 Γ(t) over the final half: the registered verdict first, points and Šidák
whiskers at the 11 retained checkpoints, no connecting line, no trend line.

Source: che/bench/results/phase6/post_unblind_analysis/post_evalfloor_gamma_t_high.json
(gamma_t.points, gamma_t.verdict, gamma_t.cross_card_T_star); floor:
che/bench/results/phase6/unblind/unblind.json beat_reproducibility.

Run from the repo root:  uv run python paper/figures/interactive/src/build_gamma_t.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ledger  # noqa: E402
from common_web import OUT_DATA, OUT_HTML, REPO, check_html, page  # noqa: E402

P6 = REPO / "che/bench/results/phase6"
FIG = "F4 Γ(t)"
SRC = "post_unblind_analysis/post_evalfloor_gamma_t_high.json → gamma_t.points.<metric>[t]"


def f4(x):
    return ("+" if x > 0 else ("−" if x < 0 else "")) + f"{abs(x):.4f}"


# (metric, t) -> which fields have a ledger row
LEDGERED = {
    ("completion", 1000): dict(est="RES-1", ci="RES-1"),
    ("survival_rate", 1000): dict(est="RES-2", ci="RES-2"),
    ("survival_rate", 900): dict(est="RES-12", ci=None),
    ("survival_rate", 950): dict(est="RES-12", ci=None),
    ("completion", 750): dict(est="RES-13", ci="RES-13"),
}
LEDGER_TEXT = {
    ("completion", 1000): ("−0.0173", "[−0.0412, +0.0066]"),
    ("survival_rate", 1000): ("+0.0096", "[+0.0047, +0.0144]"),
    ("survival_rate", 900): ("+0.0056", None),
    ("survival_rate", 950): ("+0.0083", None),
    ("completion", 750): ("−0.0147", "[−0.0283, −0.0010]"),
}
SIGNS = {"completion": "+-++-------", "survival_rate": "+--++++++++"}  # RES-11


def build_data():
    ledger.reset()
    j = json.loads((P6 / "post_unblind_analysis/post_evalfloor_gamma_t_high.json").read_text())
    ub = json.loads((P6 / "unblind/unblind.json").read_text())
    gt = j["gamma_t"]
    assert gt["steps"] == list(range(500, 1001, 50))
    metrics = []
    for m, name, dom in (("completion", "completion", [-0.044, 0.024]),
                         ("survival_rate", "survival", [-0.0095, 0.0155])):
        v = gt["verdict"][m]
        assert v["stable"] is False and "".join(v["signs"]) == SIGNS[m]
        assert v["reading"].startswith("UNSTABLE")
        tstar_sign = v["sign_at_T_star"]
        pts = []
        for p in gt["points"][m]:
            t = p["t"]
            led = LEDGERED.get((m, t), {})
            est, ci = f4(p["gamma"]), f"[{f4(p['ci_sidak'][0])}, {f4(p['ci_sidak'][1])}]"
            if (m, t) in LEDGER_TEXT:
                e_t, c_t = LEDGER_TEXT[(m, t)]
                assert est == e_t, (m, t, est, e_t)
                if c_t:
                    assert ci == c_t, (m, t, ci, c_t)
            where = SRC.replace("<metric>", m).replace("[t]", f"[t = {t}]")
            pts.append(dict(t=t, g=p["gamma"], lo=p["ci_sidak"][0], hi=p["ci_sidak"][1], sign=p["sign"],
                            disagree=p["sign"] != tstar_sign,
                            est=ledger.stated(est, led.get("est"), figure=FIG, what=f"{m} Γ({t}) estimate", source=where),
                            ci=ledger.stated(ci, led.get("ci"), figure=FIG, what=f"{m} Γ({t}) Šidák CI", source=where)))
        assert sorted(x["t"] for x in pts if x["disagree"]) == sorted(v["t_disagreeing"])
        cc = gt["cross_card_T_star"][m]
        assert cc["single_card_signs"] == v["signs"] and cc["single_card_stable"] is False
        pc = cc["gamma_post_card_T_star"]
        single = dict(t=1000, g=pc["gamma"], lo=pc["ci_sidak"][0], hi=pc["ci_sidak"][1],
                      est=ledger.stated(f4(pc["gamma"]), None, figure=FIG, what=f"{m} single-card Γ(1000)",
                                        source=f"post_evalfloor_gamma_t_high.json → gamma_t.cross_card_T_star.{m}.gamma_post_card_T_star"),
                      ci=ledger.stated(f"[{f4(pc['ci_sidak'][0])}, {f4(pc['ci_sidak'][1])}]", None, figure=FIG,
                                       what=f"{m} single-card Γ(1000) Šidák CI",
                                       source=f"post_evalfloor_gamma_t_high.json → gamma_t.cross_card_T_star.{m}.gamma_post_card_T_star"))
        metrics.append(dict(k=m, name=name, dom=dom, pts=pts, single=single,
                            floor=ub["beat_reproducibility"][m]["sd_gamma_floor_basis"],
                            signs=v["signs"]))
    return dict(metrics=metrics, verdict="sign unstable over the final half")


CSS = r"""
.panels{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px 22px}
@media (max-width:760px){.panels{grid-template-columns:1fr}}
.panel h3{font-size:14px;margin:0 0 4px;font-weight:600;display:flex;flex-wrap:wrap;gap:6px;align-items:center}
.panel svg{display:block;width:100%;height:auto}
.legend{display:flex;flex-wrap:wrap;gap:4px 14px;font-size:11px;color:var(--ink2);margin-top:6px;align-items:center}
.legend span{display:inline-flex;align-items:center;gap:5px}
g.pt:focus{outline:none} g.pt:focus .hit{stroke:var(--ink);stroke-width:1.5}
"""

BODY = r"""
<div class="wrap">
  <p class="sub">Γ(t) = JOINT − ISO at the 11 retained checkpoints, k = 72 per arm · Šidák 95 % (m = 2) · registered rule (iv): all 11 signs must agree</p>
  <div class="ctl" role="group" aria-label="overlays">
    <button class="pill" id="tsingle" aria-pressed="false">single-card curve (t = 1000 re-evaluated on the post-unblind card)</button>
    <button class="pill" id="tfloor" aria-pressed="true"><svg width="16" height="10"><defs><pattern id="stip0" width="3" height="3" patternUnits="userSpaceOnUse"><circle cx="1.5" cy="1.5" r="0.7" fill="var(--muted)"/></pattern></defs><rect width="16" height="10" fill="url(#stip0)"/></svg>floor at T* = 1000</button>
  </div>
  <div class="panels" id="panels"></div>
  <div class="legend">
    <span><svg width="26" height="12"><line x1="13" x2="13" y1="1" y2="11" stroke="var(--ink)" stroke-width="2"/><circle cx="13" cy="6" r="3.6" fill="var(--ink)"/></svg>Γ(t), Šidák 95 % CI</span>
    <span><svg width="14" height="14"><circle cx="7" cy="7" r="5.5" fill="none" stroke="var(--ink)" stroke-width="1.3"/></svg>sign differs from the sign at T*</span>
    <span id="cardnote">t = 1000: the grid card's own eval (the registered Γ) · t &lt; 1000: post-unblind card</span>
  </div>
  <details class="tbl"><summary>table view</summary><div id="tbl"></div></details>
</div>
"""

JS = r"""
var D = JSON.parse(document.getElementById('data').textContent);
var S = {single:false, floor:true};
function panel(mt){
  var W = 470, H = 300, l = 62, r = 14, top = 44, bot = 46;
  var svg = U.svg('svg', {viewBox:'0 0 '+W+' '+H, role:'img', 'aria-label': mt.name + ': Γ(t) at 11 checkpoints'});
  var defs = U.svg('defs'); var pat = U.svg('pattern', {id:'stip'+mt.k, width:3, height:3, patternUnits:'userSpaceOnUse'});
  pat.appendChild(U.svg('circle', {cx:1.5, cy:1.5, r:0.75, fill:'var(--muted)'})); defs.appendChild(pat); svg.appendChild(defs);
  var X = function(t){ return l + (t-475)/(1025-475)*(W-l-r); }, Y = function(v){ return top + (mt.dom[1]-v)/(mt.dom[1]-mt.dom[0])*(H-top-bot); };
  var step = mt.k==='completion' ? 0.01 : 0.005;
  for(var v = Math.ceil(mt.dom[0]/step)*step; v <= mt.dom[1]+1e-12; v += step){
    svg.appendChild(U.svg('line', {x1:l, x2:W-r, y1:Y(v), y2:Y(v), 'class': Math.abs(v)<1e-12 ? 'zero':'gl'}));
    svg.appendChild(U.svg('text', {x:l-6, y:Y(v)+4, 'text-anchor':'end', 'class':'tick'}, Math.abs(v)<1e-12 ? '0' : (v>0?'+':'−') + Math.abs(v).toFixed(mt.k==='completion'?2:3)));
  }
  [500,600,700,800,900,1000].forEach(function(t){ svg.appendChild(U.svg('text', {x:X(t), y:H-bot+16, 'text-anchor':'middle', 'class':'tick'}, String(t))); });
  svg.appendChild(U.svg('text', {x:(l+W-r)/2, y:H-8, 'text-anchor':'middle', 'font-size':11.5, style:'fill:var(--ink2)'}, 'training update t'));
  svg.appendChild(U.svg('text', {x:12, y:(top+H-bot)/2, 'text-anchor':'middle', 'font-size':11.5, style:'fill:var(--ink2)', transform:'rotate(-90 12 '+((top+H-bot)/2)+')'}, 'Γ(t), Δ ' + mt.name));
  // sign string, first
  svg.appendChild(U.svg('text', {x:l-6, y:20, 'text-anchor':'end', 'font-size':10.5, style:'fill:var(--muted)'}, 'sign'));
  mt.pts.forEach(function(p){
    if(p.disagree) svg.appendChild(U.svg('circle', {cx:X(p.t), cy:16, r:8, fill:'none', stroke:'var(--ink)', 'stroke-width':1.3}));
    svg.appendChild(U.svg('text', {x:X(p.t), y:21, 'text-anchor':'middle', 'font-size':14, 'font-weight':600}, p.sign==='+'?'+':'−'));
  });
  if(S.floor){ var x = X(1000); svg.appendChild(U.svg('rect', {x:x-13, y:Y(mt.floor), width:26, height:Y(-mt.floor)-Y(mt.floor), fill:'url(#stip'+mt.k+')'})); }
  mt.pts.forEach(function(p){
    var q = (S.single && p.t===1000) ? Object.assign({}, p, mt.single) : p;
    var g = U.svg('g', {'class':'pt', tabindex:0}), x = X(q.t);
    g.appendChild(U.svg('rect', {'class':'hit', x:x-12, y:top-6, width:24, height:H-top-bot+6, fill:'transparent', rx:4}));
    g.appendChild(U.svg('line', {x1:x, x2:x, y1:Y(q.lo), y2:Y(q.hi), stroke:'var(--ink)', 'stroke-width':2}));
    [q.lo, q.hi].forEach(function(v){ g.appendChild(U.svg('line', {x1:x-4, x2:x+4, y1:Y(v), y2:Y(v), stroke:'var(--ink)', 'stroke-width':2})); });
    var single = S.single && p.t===1000;
    g.appendChild(U.svg('circle', {cx:x, cy:Y(q.g), r:4.4, fill: single ? 'var(--surface)' : 'var(--ink)', stroke: single ? 'var(--ink)' : 'var(--surface)', 'stroke-width':2}));
    var lines = [['t = ' + q.t, '· ' + mt.name], ['sign', p.sign==='+'?'+':'−'] ];
    if(q.est) lines.push(['Γ(t)', q.est]); if(q.ci) lines.push(['Šidák 95 % CI', q.ci]);
    lines.push(q.t===1000 ? (single ? 'post-unblind card (single-card curve), descriptive' : 'grid card, the registered Γ') : 'post-unblind card; descriptive (no registered test at t ≠ T*)');
    g.addEventListener('mousemove', function(e){ U.tip.show(lines, e.clientX, e.clientY); });
    g.addEventListener('mouseleave', function(){ U.tip.hide(); });
    g.addEventListener('focus', function(){ U.tipAt(g, lines); }); g.addEventListener('blur', function(){ U.tip.hide(); });
    svg.appendChild(g);
  });
  return svg;
}
function render(){
  document.getElementById('tsingle').setAttribute('aria-pressed', S.single?'true':'false');
  document.getElementById('tfloor').setAttribute('aria-pressed', S.floor?'true':'false');
  var host = document.getElementById('panels'); U.clear(host);
  D.metrics.forEach(function(mt){ var p = U.el('div', {'class':'panel'}), h = U.el('h3');
    h.appendChild(U.el('span', {'class':'chip line'}, D.verdict)); h.appendChild(document.createTextNode(mt.name));
    p.appendChild(h); p.appendChild(panel(mt)); host.appendChild(p); });
  var host2 = document.getElementById('tbl'); U.clear(host2); var tb = U.el('table'), hr = U.el('tr');
  ['metric','t','sign','Γ(t)','Šidák 95 % CI'].forEach(function(h){ hr.appendChild(U.el('th', null, h)); }); tb.appendChild(hr);
  D.metrics.forEach(function(mt){ mt.pts.forEach(function(p){ var tr = U.el('tr');
    [mt.name, p.t, p.sign==='+'?'+':'−', p.est||'(plotted)', p.ci||'(plotted)'].forEach(function(c){ tr.appendChild(U.el('td', null, String(c))); }); tb.appendChild(tr); }); });
  host2.appendChild(tb); U.tip.hide(); if(window.__fit) window.__fit();
}
document.getElementById('tsingle').onclick = function(){ S.single = !S.single; render(); };
document.getElementById('tfloor').onclick = function(){ S.floor = !S.floor; render(); };
window.__redraw = render; render();
"""


def main():
    data = build_data()
    out = OUT_HTML / "gamma_t_final_half.html"
    out.write_text(page("Gamma over training", BODY, CSS, JS, data), encoding="utf-8")
    hits = check_html(out)
    assert not hits, hits
    (OUT_DATA / "gamma_t_pending.json").write_text(json.dumps(ledger.pending(), indent=1, ensure_ascii=False) + "\n")
    print(f"{out.name}: {out.stat().st_size/1e3:.1f} KB; pending: {len(ledger.pending())}")


if __name__ == "__main__":
    main()
