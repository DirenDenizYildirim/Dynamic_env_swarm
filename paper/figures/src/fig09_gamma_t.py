# ruff: noqa: E501  (inline JS/CSS of a self-contained HTML figure)
"""Figure 9 (slot): Γ(t) over the final half (updates 500–1000, 11 retained
checkpoints), both co-primaries, Šidák bands; the registered sign rule (iv)
verdict stated first. Companion: the single-card curve (ruling viii), where
t = 1000 is the post-unblind card's re-evaluation instead of the grid's own
eval. Everything is read from the committed post-unblind analysis JSON.

Outputs: out/img/fig09_gamma_t.png, out/img/fig09b_gamma_t_single_card.png,
out/html/fig09_gamma_t.html
"""

from __future__ import annotations

import common as C
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

SRC = C.P6 / "post_unblind_analysis" / "post_evalfloor_gamma_t_high.json"
UNBLIND = C.P6 / "unblind" / "unblind.json"
METRICS = ("completion", "survival_rate")
MLABEL = {"completion": "completion", "survival_rate": "survival rate"}


def load():
    d = C.load_json(SRC)
    ub = C.load_json(UNBLIND)
    gt = d["gamma_t"]
    out = {}
    for m in METRICS:
        pts = gt["points"][m]
        assert [p["t"] for p in pts] == gt["steps"]
        # the t = 1000 point IS the registered primary Γ (grid card eval)
        assert abs(pts[-1]["gamma"] - ub["primary"]["family"][m]["gamma"]) < 1e-12
        cc = gt["cross_card_T_star"][m]
        post = cc["gamma_post_card_T_star"]
        single = [dict(p) for p in pts[:-1]] + [dict(post, t=1000)]
        v = gt["verdict"][m]
        out[m] = dict(
            grid=[
                dict(
                    t=p["t"],
                    g=p["gamma"],
                    ci=p["ci_sidak"],
                    sd=p["sd_gamma"],
                    z=p["z"],
                    iso=p["mean_a"],
                    joint=p["mean_b"],
                    k=p["k_a"],
                )
                for p in pts
            ],
            single=[
                dict(
                    t=p["t"],
                    g=p["gamma"],
                    ci=p["ci_sidak"],
                    sd=p["sd_gamma"],
                    z=p["z"],
                    iso=p["mean_a"],
                    joint=p["mean_b"],
                    k=p["k_a"],
                )
                for p in single
            ],
            signs=v["signs"],
            stable=v["stable"],
            single_signs=cc["single_card_signs"],
            single_stable=cc["single_card_stable"],
            floor=ub["beat_reproducibility"][m]["sd_gamma_floor_basis"],
        )
        assert out[m]["signs"] == ["+" if p["gamma"] > 0 else "-" for p in pts]
    return out


def panel(ax, m, D, which):
    pts = D[which]
    ts = [p["t"] for p in pts]
    lo = [p["ci"][0] for p in pts]
    hi = [p["ci"][1] for p in pts]
    g = [p["g"] for p in pts]
    ax.axhline(0, color=C.MUTED, lw=0.8, zorder=1)
    ax.fill_between(ts, lo, hi, color=C.INK, alpha=0.10, lw=0, zorder=1.5)
    ax.plot(ts, lo, color=C.INK2, lw=0.6, zorder=2)
    ax.plot(ts, hi, color=C.INK2, lw=0.6, zorder=2)
    ax.plot(ts, g, color=C.INK, lw=1.8, zorder=3)
    ax.plot(ts, g, "o", color=C.INK, ms=4.6, mec=C.SURFACE, mew=1.2, zorder=4)
    f = D["floor"]
    ax.add_patch(
        plt.Rectangle(
            (1008, -f),
            14,
            2 * f,
            facecolor="none",
            edgecolor=C.HATCH,
            hatch="////",
            lw=0,
            zorder=2.5,
        )
    )
    ax.set_xlim(480, 1028)
    ax.set_xticks(ts)
    ax.set_xticklabels([str(t) if t % 100 == 0 else "" for t in ts])
    ax.set_xlabel("training update t")
    ax.set_ylabel(f"Γ(t), difference in {MLABEL[m]}")
    ax.grid(axis="y")
    ax.set_axisbelow(True)
    signs = D["signs"] if which == "grid" else D["single_signs"]
    stable = D["stable"] if which == "grid" else D["single_stable"]
    tr = ax.get_xaxis_transform()
    ax.text(
        470,
        1.035,
        "sign",
        ha="right",
        va="center",
        fontsize=7.4,
        color=C.MUTED,
        transform=tr,
    )
    for t, s in zip(ts, signs, strict=False):
        ax.text(
            t,
            1.035,
            "+" if s == "+" else C.MINUS,
            ha="center",
            va="center",
            fontsize=8.5,
            color=C.INK,
            transform=tr,
        )
    # registered verdict string, verbatim (FIGURES FIRST ruling, item 3)
    if which == "grid":
        lab = (
            "rule (iv): sign unstable over the final half"
            if not stable
            else "rule (iv): sign stable"
        )
    else:
        lab = (
            "single-card signs: not stable (descriptive)"
            if not stable
            else "single-card signs: stable (descriptive)"
        )
    ax.set_title(f"{MLABEL[m]}\n{lab}", fontsize=8.4, pad=17)


def static(D, which, name):
    C.mpl_setup()
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.1), gridspec_kw={"wspace": 0.34})
    for ax, m in zip(axes, METRICS, strict=False):
        panel(ax, m, D[m], which)
    t1000 = (
        "t = 1000: grid-card eval (the registered Γ);  t < 1000: post-unblind card"
        if which == "grid"
        else "all 11 checkpoints evaluated on the post-unblind card (single-card curve)"
    )
    handles = [
        Line2D(
            [0],
            [0],
            color=C.INK,
            lw=1.8,
            marker="o",
            ms=4.6,
            mec=C.SURFACE,
            label="Γ(t) = JOINT − ISO, k = 72, 72",
        ),
        Patch(
            facecolor=C.INK,
            alpha=0.10,
            edgecolor=C.INK2,
            lw=0.6,
            label="Šidák 95 % CI (m = 2)",
        ),
        Patch(
            facecolor="none",
            edgecolor=C.HATCH,
            hatch="////",
            lw=0,
            label="floor at T* = 1000: ±1 sd(Γ), floor basis",
        ),
    ]
    fig.legend(
        handles=handles,
        loc="lower center",
        ncol=3,
        bbox_to_anchor=(0.5, -0.1),
        fontsize=7.4,
    )
    fig.text(0.5, -0.135, t1000, ha="center", va="top", fontsize=7.2, color=C.MUTED)
    return C.save_png(fig, name)


BODY = """
<div class="controls"><span class="lab">t = 1000 evaluated on</span><span id="cs"></span></div>
<div class="legend" id="lg"></div>
<div id="chart" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(330px,1fr));gap:8px 18px"></div>
<div class="lab" id="note" style="margin-top:2px"></div>
<details><summary>Table view</summary><div class="tw" id="tbl"></div></details>
"""

SCRIPT = r"""
let which='grid';
const ML={completion:'completion',survival_rate:'survival rate'};
function legend(){const lg=document.getElementById('lg');lg.replaceChildren();
const it=[['l','Γ(t) = JOINT − ISO, k = 72, 72'],['b','Šidák 95 % CI (m = 2)'],['f','floor at T* = 1000: ±1 sd(Γ), floor basis']];
for(const [k,lab] of it){const s=document.createElement('span');const sv=S('svg',{width:26,height:12,viewBox:'0 0 26 12'});
if(k==='l'){S('line',{x1:2,x2:24,y1:6,y2:6,stroke:'var(--ink)','stroke-width':2},sv);S('circle',{cx:13,cy:6,r:3.5,fill:'var(--ink)',stroke:'var(--surface)','stroke-width':1.5},sv);}
if(k==='b')S('rect',{x:1,y:1,width:24,height:10,fill:'var(--ink)','fill-opacity':0.1,stroke:'var(--ink2)','stroke-width':0.6},sv);
if(k==='f'){const d=S('defs',null,sv);const p=S('pattern',{id:'lf',width:4,height:4,patternUnits:'userSpaceOnUse',patternTransform:'rotate(45)'},d);S('line',{x1:0,y1:0,x2:0,y2:4,stroke:'var(--muted)','stroke-width':1},p);S('rect',{x:1,y:1,width:24,height:10,fill:'url(#lf)'},sv);}
s.appendChild(sv);s.appendChild(document.createTextNode(lab));lg.appendChild(s);}}
function draw(m){const D=DATA[m],P=D[which];const W=380,H=300,ml=58,mr=12,mt=40,mb=62;
const svg=S('svg',{viewBox:`0 0 ${W} ${H}`,'aria-label':'Gamma of t for '+ML[m]});
let lo=Math.min(...P.map(p=>p.ci[0]),-D.floor),hi=Math.max(...P.map(p=>p.ci[1]),D.floor);const pad=0.08*(hi-lo);lo-=pad;hi+=pad;
const x=lin(480,1028,ml,W-mr),y=lin(lo,hi,H-mb,mt);const ts=niceTicks(lo,hi,5),tf=tickFmt(ts);
for(const t of ts){S('line',{x1:ml,x2:W-mr,y1:y(t),y2:y(t),stroke:'var(--grid)'},svg);T({x:ml-6,y:y(t)+4,'text-anchor':'end',class:'tick'},tf(t),svg);}
S('line',{x1:ml,x2:W-mr,y1:y(0),y2:y(0),stroke:'var(--muted)'},svg);
S('line',{x1:ml,x2:W-mr,y1:H-mb,y2:H-mb,stroke:'var(--axis)'},svg);
for(const p of P){if(p.t%100===0)T({x:x(p.t),y:H-mb+15,'text-anchor':'middle',class:'tick'},String(p.t),svg);
S('line',{x1:x(p.t),x2:x(p.t),y1:H-mb,y2:H-mb+3,stroke:'var(--axis)'},svg);}
T({x:(ml+W-mr)/2,y:H-8,'text-anchor':'middle',class:'axt'},'training update t',svg);
T({x:12,y:(mt+H-mb)/2,transform:`rotate(-90 12 ${(mt+H-mb)/2})`,'text-anchor':'middle',class:'axt'},'Γ(t), difference in '+ML[m],svg);
const signs=which==='grid'?D.signs:D.single_signs,stable=which==='grid'?D.stable:D.single_stable;
T({x:ml-6,y:H-mb+32,'text-anchor':'end',class:'note'},'sign',svg);
P.forEach((p,i)=>T({x:x(p.t),y:H-mb+33,'text-anchor':'middle',class:'tick'},signs[i]==='+'?'+':MINUS,svg).style.fill='var(--ink)');
T({x:ml-50,y:18,class:'ttl'},ML[m],svg);
T({x:ml-50,y:33,class:'note'},which==='grid'?(stable?'rule (iv): sign stable':'rule (iv): sign unstable over the final half'):(stable?'single-card signs: stable (descriptive)':'single-card signs: not stable (descriptive)'),svg).style.fill='var(--ink2)';
const dfs=S('defs',null,svg);const pt=S('pattern',{id:'hp'+m,width:5,height:5,patternUnits:'userSpaceOnUse',patternTransform:'rotate(45)'},dfs);S('line',{x1:0,y1:0,x2:0,y2:5,stroke:'var(--muted)','stroke-width':1},pt);
S('rect',{x:x(1008),y:y(D.floor),width:x(1022)-x(1008),height:y(-D.floor)-y(D.floor),fill:`url(#hp${m})`},svg);
let band='M'+P.map(p=>x(p.t)+','+y(p.ci[1])).join('L')+'L'+P.slice().reverse().map(p=>x(p.t)+','+y(p.ci[0])).join('L')+'Z';
S('path',{d:band,fill:'var(--ink)','fill-opacity':0.1},svg);
S('path',{d:'M'+P.map(p=>x(p.t)+','+y(p.ci[1])).join('L'),fill:'none',stroke:'var(--ink2)','stroke-width':0.7},svg);
S('path',{d:'M'+P.map(p=>x(p.t)+','+y(p.ci[0])).join('L'),fill:'none',stroke:'var(--ink2)','stroke-width':0.7},svg);
S('path',{d:'M'+P.map(p=>x(p.t)+','+y(p.g)).join('L'),fill:'none',stroke:'var(--ink)','stroke-width':2,'stroke-linejoin':'round'},svg);
const cross=S('line',{y1:mt,y2:H-mb,stroke:'var(--muted)','stroke-width':1,visibility:'hidden'},svg);
const dots=P.map(p=>S('circle',{cx:x(p.t),cy:y(p.g),r:4.5,fill:'var(--ink)',stroke:'var(--surface)','stroke-width':2},svg));
const hit=S('rect',{x:ml,y:mt,width:W-mr-ml,height:H-mb-mt,class:'hit',tabindex:0},svg);
function at(i,cx,cy){const p=P[i];cross.setAttribute('x1',x(p.t));cross.setAttribute('x2',x(p.t));cross.setAttribute('visibility','visible');
dots.forEach((d,j)=>d.setAttribute('r',j===i?6:4.5));
const card=p.t<1000?'post-unblind card':(which==='grid'?'grid card (registered Γ)':'post-unblind card');
showTip(cx,cy,ML[m]+', t = '+p.t,[[fmt(p.g,4),'Γ(t)'],['['+fmt(p.ci[0],4)+', '+fmt(p.ci[1],4)+']','Šidák 95 % CI'],[p.sd.toFixed(5),'sd(Γ)'],[fmt(p.z,2),'z'],
[p.iso.toFixed(4),'ISO mean'],[p.joint.toFixed(4),'JOINT mean'],[card,'']]);}
let cur=P.length-1;
hit.addEventListener('pointermove',ev=>{const r=svg.getBoundingClientRect();const sx=(ev.clientX-r.left)*W/r.width;let b=0,bd=1e9;
P.forEach((p,i)=>{const dd=Math.abs(x(p.t)-sx);if(dd<bd){bd=dd;b=i;}});cur=b;at(b,ev.clientX,ev.clientY);});
hit.addEventListener('pointerleave',()=>{cross.setAttribute('visibility','hidden');dots.forEach(d=>d.setAttribute('r',4.5));hideTip();});
hit.addEventListener('keydown',ev=>{if(ev.key==='ArrowLeft'||ev.key==='ArrowRight'){cur=Math.max(0,Math.min(P.length-1,cur+(ev.key==='ArrowLeft'?-1:1)));
const r=svg.getBoundingClientRect();at(cur,r.left+x(P[cur].t)*r.width/W,r.top+y(P[cur].g)*r.height/H);ev.preventDefault();}});
hit.addEventListener('focus',()=>{const r=svg.getBoundingClientRect();at(cur,r.left+x(P[cur].t)*r.width/W,r.top+y(P[cur].g)*r.height/H);});
hit.addEventListener('blur',()=>{cross.setAttribute('visibility','hidden');hideTip();});
return svg;}
function render(){legend();const c=document.getElementById('chart');c.replaceChildren(draw('completion'),draw('survival_rate'));
document.getElementById('note').textContent=which==='grid'?'t = 1000: grid-card eval (the registered Γ); t < 1000: post-unblind card. Arrow keys step through checkpoints when a chart has focus.':'Single-card curve: all 11 checkpoints evaluated on the post-unblind card. Arrow keys step through checkpoints when a chart has focus.';
const rows=[];for(const m of ['completion','survival_rate']){DATA[m][which].forEach((p,i)=>rows.push([ML[m],String(p.t),fmt(p.g,4),'['+fmt(p.ci[0],4)+', '+fmt(p.ci[1],4)+']',p.sd.toFixed(5),fmt(p.z,2),p.iso.toFixed(4),p.joint.toFixed(4),(which==='grid'?DATA[m].signs:DATA[m].single_signs)[i]==='+'?'+':MINUS]));}
table(document.getElementById('tbl'),['metric','t','Γ(t)','Šidák 95 % CI','sd(Γ)','z','ISO mean','JOINT mean','sign'],rows);}
seg(document.getElementById('cs'),[['grid','grid card (registered)'],['single','post-unblind card (single-card curve)']],which,v=>{which=v;render();});
render();
"""


def main():
    D = load()
    print(static(D, "grid", "fig09_gamma_t.png").name)
    print(static(D, "single", "fig09b_gamma_t_single_card.png").name)
    print(
        C.write_html(
            "fig09_gamma_t.html", "Contrast over training", BODY, D, SCRIPT
        ).name
    )
    for m in METRICS:
        print(
            m,
            "signs",
            "".join(D[m]["signs"]),
            "single",
            "".join(D[m]["single_signs"]),
            "stable",
            D[m]["stable"],
            D[m]["single_stable"],
            "floor",
            D[m]["floor"],
        )
        print(
            "  t=1000 grid",
            C.fmt(D[m]["grid"][-1]["g"]),
            C.ci_text(*D[m]["grid"][-1]["ci"]),
            " single",
            C.fmt(D[m]["single"][-1]["g"]),
            C.ci_text(*D[m]["single"][-1]["ci"]),
        )


if __name__ == "__main__":
    main()
