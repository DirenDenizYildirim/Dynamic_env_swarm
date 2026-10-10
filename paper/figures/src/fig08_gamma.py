# ruff: noqa: E501  (inline JS/CSS of a self-contained HTML figure)
"""Figure 8 (slot): the confirmatory contrast Γ = JOINT − ISO at θ*, T* = 1000,
with its Šidák CI, its 80 %-power MDE band (exclusion X) and its floor bar;
Γ₄, Γ₄′ and B̂ beside it. Every value is read from a committed report JSON;
nothing is re-estimated. The per-seed view re-reads the committed eval JSONs
only to plot them, and asserts that they reproduce the committed arm means.

Outputs: out/img/fig08_gamma_contrasts.png, out/img/fig08b_gamma_arms_per_seed.png,
out/html/fig08_gamma_contrasts.html
"""

from __future__ import annotations

import math

import common as C
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

UNBLIND = C.P6 / "unblind" / "unblind.json"
GAMMA4 = C.P6 / "post_unblind_analysis" / "post_gamma4_t2000.json"
SECOND = C.P6 / "secondary" / "secondary.json"
METRICS = ("completion", "survival_rate")
MLABEL = {"completion": "completion", "survival_rate": "survival rate"}
THETA = "che/configs/theta_star_holdout.yaml"


def read_eval(p, metric):
    d = C.load_json(p)
    # the confirmatory reader's guards (p6_post_analysis.read_eval)
    assert d["ckpt_step"] == 1000 and d["n_episodes"] == 512 and d["seed"] == 0, p
    assert d["config"] == THETA, p
    return float(d["metrics"][metric]["mean"])


def load():
    ub = C.load_json(UNBLIND)
    g4 = C.load_json(GAMMA4)
    sec = C.load_json(SECOND)
    rows = {}
    for m in METRICS:
        P = ub["primary"]["family"][m]
        Q = ub["prefix"]["family"][m]
        G4 = g4["gamma4"]["per_metric"][m]
        R = sec["replicate"][m]["gamma4_prime"]
        fl = ub["beat_reproducibility"][m]
        rows[m] = [
            dict(
                key="gamma",
                sym="Γ",
                what="JOINT − ISO",
                k=f"k = {P['k']}, {P['k']}",
                g=P["gamma"],
                ci=P["ci_sidak"],
                X=P["exclusion_mde80"],
                sd=P["sd_gamma"],
                z=P["z"],
                rej=P["reject"],
                floor=fl["sd_gamma_floor_basis"],
                src="unblind/unblind.json primary.family." + m,
            ),
            dict(
                key="prefix",
                sym="Γ",
                what="JOINT − ISO, k = 60 prefix",
                k=f"k = {Q['k']}, {Q['k']} (seeds 1–60)",
                g=Q["gamma"],
                ci=Q["ci_sidak"],
                X=Q["exclusion_mde80"],
                sd=Q["sd_gamma"],
                z=Q["z"],
                rej=Q["reject"],
                floor=None,
                src="unblind/unblind.json prefix.family." + m,
            ),
            dict(
                key="gamma4",
                sym="Γ₄",
                what="JOINT − ISO-4",
                k=f"k = {G4['gamma4']['k_b']}, {G4['gamma4']['k_a']}",
                g=G4["gamma4"]["gamma"],
                ci=G4["gamma4"]["ci_sidak"],
                X=G4["gamma4"]["exclusion_mde80"],
                sd=G4["gamma4"]["sd_gamma"],
                z=G4["gamma4"]["z"],
                rej=G4["gamma4"]["reject"],
                floor=None,
                src="post_unblind_analysis/post_gamma4_t2000.json gamma4.per_metric."
                + m
                + ".gamma4",
            ),
            dict(
                key="gamma4p",
                sym="Γ₄′",
                what="JOINT − sweep_c50_p000",
                k=f"k = {R['k_b']}, {R['k_a']}",
                g=R["gamma"],
                ci=R["ci_sidak"],
                X=R["exclusion_mde80"],
                sd=R["sd_gamma"],
                z=R["z"],
                rej=R["reject"],
                floor=None,
                src="secondary/secondary.json replicate." + m + ".gamma4_prime",
            ),
            dict(
                key="bhat",
                sym="B̂",
                what="ISO-4 − ISO",
                k=f"k = {G4['b_hat']['k_b']}, {G4['b_hat']['k_a']}",
                g=G4["b_hat"]["gamma"],
                ci=G4["b_hat"]["ci_sidak"],
                X=G4["b_hat"]["exclusion_mde80"],
                sd=G4["b_hat"]["sd_gamma"],
                z=G4["b_hat"]["z"],
                rej=G4["b_hat"]["reject"],
                floor=None,
                src="post_unblind_analysis/post_gamma4_t2000.json gamma4.per_metric."
                + m
                + ".b_hat",
            ),
        ]
    # ---- per-seed arm values (plotted only; arm means asserted committed)
    seeds = {m: {} for m in METRICS}
    means = {m: {} for m in METRICS}
    for m in METRICS:
        seeds[m]["iso"] = ub["primary"]["per_seed"]["iso"][m]
        seeds[m]["joint"] = ub["primary"]["per_seed"]["joint"][m]
        seeds[m]["iso4"] = [
            read_eval(C.P6 / "g1_iso4_5090" / f"eval_iso4_s{s}.json", m)
            for s in range(1, 21)
        ]
        seeds[m]["sweep_c50_p000"] = [
            read_eval(
                (C.P6 / ("g1_sec_s1_12_5090" if s <= 12 else "g1_grid"))
                / f"eval_sweep_c50_p000_s{s}.json",
                m,
            )
            for s in range(1, 21)
        ]
        means[m]["iso"] = ub["primary"]["family"][m]["mean_iso"]
        means[m]["joint"] = ub["primary"]["family"][m]["mean_joint"]
        means[m]["iso4"] = g4["gamma4"]["per_metric"][m]["gamma4"]["mean_a"]
        means[m]["sweep_c50_p000"] = sec["metrics"][m]["sweep_means"]["sweep_c50_p000"]
        for arm, v in seeds[m].items():
            mu = sum(v) / len(v)
            assert math.isclose(mu, means[m][arm], rel_tol=0, abs_tol=1e-9), (
                m,
                arm,
                mu,
            )
    return rows, seeds, means


# ------------------------------------------------------------------ static
ROW_MARK = {
    "gamma": ("o", True),
    "prefix": ("o", False),
    "gamma4": ("^", True),
    "gamma4p": ("D", True),
    "bhat": ("s", True),
}
YPOS = {"gamma": 0.0, "prefix": 1.0, "gamma4": 2.55, "gamma4p": 3.55, "bhat": 4.55}


def static_forest(rows):
    C.mpl_setup()
    fig, axes = plt.subplots(2, 1, figsize=(6.9, 5.5), gridspec_kw={"hspace": 0.62})
    for ax, m in zip(axes, METRICS, strict=False):
        R = rows[m]
        lo = min(min(r["ci"][0] for r in R), min(-r["X"] for r in R))
        hi = max(max(r["ci"][1] for r in R), max(r["X"] for r in R))
        pad = 0.06 * (hi - lo)
        ax.set_xlim(lo - pad, hi + pad)
        ax.set_ylim(5.25, -0.75)
        ax.axvline(0, color=C.MUTED, lw=0.8, zorder=1)
        for r in R:
            y = YPOS[r["key"]]
            ax.add_patch(
                plt.Rectangle(
                    (-r["X"], y - 0.32),
                    2 * r["X"],
                    0.64,
                    facecolor=C.BAND,
                    edgecolor="none",
                    zorder=0,
                )
            )
            if r["floor"] is not None:
                ax.add_patch(
                    plt.Rectangle(
                        (-r["floor"], y - 0.32),
                        2 * r["floor"],
                        0.64,
                        facecolor="none",
                        edgecolor=C.HATCH,
                        lw=0,
                        hatch="////",
                        zorder=0.5,
                    )
                )
            col = C.INK if r["key"] in ("gamma", "prefix") else C.INK2
            ax.plot(r["ci"], [y, y], color=col, lw=1.8, solid_capstyle="butt", zorder=3)
            for xe in r["ci"]:
                ax.plot([xe, xe], [y - 0.14, y + 0.14], color=col, lw=1.2, zorder=3)
            mk, filled = ROW_MARK[r["key"]]
            ax.plot(
                [r["g"]],
                [y],
                marker=mk,
                ms=6.5,
                color=col,
                mfc=col if filled else C.SURFACE,
                mec=col,
                mew=1.4,
                zorder=4,
                linestyle="none",
            )
            ax.text(
                1.015,
                y,
                f"{C.fmt(r['g'])}  {C.ci_text(*r['ci'])}",
                transform=ax.get_yaxis_transform(),
                va="center",
                ha="left",
                fontsize=7.6,
                color=C.INK,
                family="DejaVu Sans",
            )
            ax.text(
                1.39,
                y,
                "REJECT" if r["rej"] else "null",
                transform=ax.get_yaxis_transform(),
                va="center",
                ha="left",
                fontsize=7.6,
                color=C.INK2,
            )
        ax.set_yticks([YPOS[r["key"]] for r in R])
        ax.set_yticklabels(
            [f"{r['sym']}  {r['what']}\n{r['k']}" for r in R], fontsize=7.8, color=C.INK
        )
        ax.tick_params(axis="y", length=0)
        ax.spines["left"].set_visible(False)
        ax.axhline(1.78, color=C.GRID, lw=0.8, zorder=0)
        ax.set_xlabel(f"difference in {MLABEL[m]} (fraction)")
        ax.set_title(MLABEL[m], pad=14)
        ax.text(
            1.015,
            -0.95,
            "estimate  Šidák 95 % CI",
            transform=ax.get_yaxis_transform(),
            fontsize=7.2,
            color=C.MUTED,
            ha="left",
            va="bottom",
        )
        ax.text(
            1.39,
            -0.95,
            "test",
            transform=ax.get_yaxis_transform(),
            fontsize=7.2,
            color=C.MUTED,
            ha="left",
            va="bottom",
        )
        ax.text(
            -0.01,
            -0.62,
            "confirmatory family",
            transform=ax.get_yaxis_transform(),
            fontsize=7.2,
            color=C.MUTED,
            ha="right",
            va="center",
            style="italic",
        )
        ax.text(
            -0.01,
            1.95,
            "outside the confirmatory family",
            transform=ax.get_yaxis_transform(),
            fontsize=7.2,
            color=C.MUTED,
            ha="right",
            va="center",
            style="italic",
        )
    handles = [
        Line2D(
            [0],
            [0],
            color=C.INK,
            lw=1.8,
            marker="o",
            ms=5.5,
            label="estimate, Šidák 95 % CI (m = 2)",
        ),
        Patch(facecolor=C.BAND, edgecolor="none", label="±X, 80 %-power MDE"),
        Patch(
            facecolor="none",
            edgecolor=C.HATCH,
            hatch="////",
            lw=0,
            label="floor: ±1 sd(Γ), floor basis",
        ),
    ]
    fig.legend(
        handles=handles,
        loc="lower center",
        ncol=3,
        bbox_to_anchor=(0.5, -0.035),
        fontsize=7.6,
        handlelength=2.2,
    )
    return C.save_png(fig, "fig08_gamma_contrasts.png")


def static_arms(seeds, means):
    C.mpl_setup()
    order = ["iso", "iso4", "sweep_c50_p000", "joint"]
    fig, axes = plt.subplots(1, 2, figsize=(6.9, 3.0), gridspec_kw={"wspace": 0.32})
    for ax, m in zip(axes, METRICS, strict=False):
        for i, arm in enumerate(order):
            col, mk, lab = C.ARM_STYLE[arm]
            v = seeds[m][arm]
            n = len(v)
            # deterministic horizontal offsets by seed index (no randomness)
            xs = [i + 0.26 * (((j * 0.6180339887) % 1.0) - 0.5) for j in range(n)]
            ax.scatter(
                xs,
                v,
                s=11,
                marker=mk,
                facecolors="none",
                edgecolors=col,
                linewidths=0.8,
                zorder=2,
            )
            ax.plot(
                [i - 0.24, i + 0.24], [means[m][arm]] * 2, color=C.INK, lw=2.0, zorder=3
            )
        ax.set_xticks(range(len(order)))
        names = {
            "iso": "ISO\n",
            "iso4": "ISO-4\n",
            "sweep_c50_p000": "sweep_c50\n_p000",
            "joint": "JOINT\n",
        }
        ax.set_xticklabels(
            [f"{names[a]}\nk = {len(seeds[m][a])}" for a in order], fontsize=7.4
        )
        ax.tick_params(axis="x", length=0)
        ax.set_ylabel(f"{MLABEL[m]} at θ*, per seed")
        ax.set_title(MLABEL[m])
        ax.grid(axis="y")
        ax.set_axisbelow(True)
    handles = [
        Line2D(
            [0],
            [0],
            marker="o",
            ls="none",
            mfc="none",
            mec=C.INK2,
            ms=4,
            label="one training seed (mean over 512 eval episodes)",
        ),
        Line2D([0], [0], color=C.INK, lw=2.0, label="arm mean"),
    ]
    fig.legend(
        handles=handles,
        loc="lower center",
        ncol=2,
        bbox_to_anchor=(0.5, -0.12),
        fontsize=7.6,
    )
    return C.save_png(fig, "fig08b_gamma_arms_per_seed.png")


# ------------------------------------------------------------------ interactive
BODY = """
<div class="controls"><span class="lab">metric</span><span id="cm"></span>
<span class="lab">view</span><span id="cv"></span></div>
<div class="legend" id="lg"></div>
<div id="chart"></div>
<details><summary>Table view</summary><div class="tw" id="tbl"></div></details>
"""

SCRIPT = r"""
let metric='survival_rate', view='contrasts';
const ML={completion:'completion',survival_rate:'survival rate'};
const ARMS=[['iso','ISO','--s1','o'],['iso4','ISO-4','--s3','^'],['sweep_c50_p000','sweep_c50_p000','--neutral','D'],['joint','JOINT','--s2','s']];
const RM={gamma:['o',true],prefix:['o',false],gamma4:['^',true],gamma4p:['D',true],bhat:['s',true]};
const YP={gamma:0,prefix:1,gamma4:2.55,gamma4p:3.55,bhat:4.55};
function legend(){const lg=document.getElementById('lg');lg.replaceChildren();
const items=view==='contrasts'?[['ci','estimate, Šidák 95 % CI (m = 2)'],['band','±X, 80 %-power MDE'],['floor','floor: ±1 sd(Γ), floor basis']]
:ARMS.map(a=>['arm',a[1],a]).concat([['mean','arm mean']]);
for(const [kind,lab,a] of items){const s=document.createElement('span');const sv=S('svg',{width:26,height:12,viewBox:'0 0 26 12'});
if(kind==='ci'){S('line',{x1:2,x2:24,y1:6,y2:6,stroke:'var(--ink)','stroke-width':2},sv);S('circle',{cx:13,cy:6,r:4,fill:'var(--ink)'},sv);}
if(kind==='band')S('rect',{x:1,y:1,width:24,height:10,fill:'var(--band)'},sv);
if(kind==='floor'){const d=S('defs',null,sv);const pt=S('pattern',{id:'hl',width:4,height:4,patternUnits:'userSpaceOnUse',patternTransform:'rotate(45)'},d);S('line',{x1:0,y1:0,x2:0,y2:4,stroke:'var(--muted)','stroke-width':1},pt);S('rect',{x:1,y:1,width:24,height:10,fill:'url(#hl)'},sv);}
if(kind==='arm')marker(a[3],13,6,4,{fill:'none',stroke:`var(${a[2]})`,'stroke-width':1.5},sv);
if(kind==='mean')S('line',{x1:3,x2:23,y1:6,y2:6,stroke:'var(--ink)','stroke-width':2.5},sv);
s.appendChild(sv);s.appendChild(document.createTextNode(lab));lg.appendChild(s);}}
function drawContrasts(){const R=DATA.rows[metric];const W=760,H=330,ml=230,mr=200,mt=34,mb=46;
const svg=S('svg',{viewBox:`0 0 ${W} ${H}`,'aria-label':'Forest plot of contrasts for '+ML[metric]});
let lo=Math.min(...R.map(r=>Math.min(r.ci[0],-r.X))),hi=Math.max(...R.map(r=>Math.max(r.ci[1],r.X)));const pad=0.06*(hi-lo);lo-=pad;hi+=pad;
const x=lin(lo,hi,ml,W-mr),y=lin(-0.75,5.25,mt,H-mb),rh=(y(1)-y(0));
const ts=niceTicks(lo,hi,6),tf=tickFmt(ts);
for(const t of ts){S('line',{x1:x(t),x2:x(t),y1:mt-6,y2:H-mb,stroke:'var(--grid)'},svg);T({x:x(t),y:H-mb+16,'text-anchor':'middle',class:'tick'},tf(t),svg);}
S('line',{x1:ml,x2:W-mr,y1:H-mb,y2:H-mb,stroke:'var(--axis)'},svg);
S('line',{x1:x(0),x2:x(0),y1:mt-6,y2:H-mb,stroke:'var(--muted)','stroke-width':1},svg);
T({x:(ml+W-mr)/2,y:H-8,'text-anchor':'middle',class:'axt'},'difference in '+ML[metric]+' (fraction)',svg);
T({x:ml-8,y:y(-0.62),'text-anchor':'end',class:'note','font-style':'italic'},'confirmatory family',svg);
T({x:ml-8,y:y(1.95),'text-anchor':'end',class:'note','font-style':'italic'},'outside the confirmatory family',svg);
S('line',{x1:20,x2:W-10,y1:y(1.78),y2:y(1.78),stroke:'var(--grid)'},svg);
T({x:W-mr+10,y:mt-14,class:'note'},'estimate  Šidák 95 % CI',svg);T({x:W-46,y:mt-14,class:'note'},'test',svg);
const d=S('defs',null,svg);const pt=S('pattern',{id:'hf',width:5,height:5,patternUnits:'userSpaceOnUse',patternTransform:'rotate(45)'},d);S('line',{x1:0,y1:0,x2:0,y2:5,stroke:'var(--muted)','stroke-width':1},pt);
for(const r of R){const yy=y(YP[r.key]);const g=S('g',null,svg);
S('rect',{x:x(-r.X),y:yy-rh*0.32,width:x(r.X)-x(-r.X),height:rh*0.64,fill:'var(--band)'},g);
if(r.floor!==null)S('rect',{x:x(-r.floor),y:yy-rh*0.32,width:x(r.floor)-x(-r.floor),height:rh*0.64,fill:'url(#hf)'},g);
const col=(r.key==='gamma'||r.key==='prefix')?'var(--ink)':'var(--ink2)';
S('line',{x1:x(r.ci[0]),x2:x(r.ci[1]),y1:yy,y2:yy,stroke:col,'stroke-width':2},g);
for(const e of r.ci)S('line',{x1:x(e),x2:x(e),y1:yy-5,y2:yy+5,stroke:col,'stroke-width':1.5},g);
const [mk,f]=RM[r.key];marker(mk,x(r.g),yy,5,{fill:f?col:'var(--surface)',stroke:col,'stroke-width':1.6},g);
T({x:20,y:yy-3,class:'tick',fill:'var(--ink)'},r.sym+'  '+r.what,svg).style.fill='var(--ink)';
T({x:20,y:yy+11,class:'note'},r.k,svg);
T({x:W-mr+10,y:yy+4,class:'tick'},fmt(r.g,4)+'  ['+fmt(r.ci[0],4)+', '+fmt(r.ci[1],4)+']',svg).style.fill='var(--ink)';
T({x:W-46,y:yy+4,class:'tick'},r.rej?'REJECT':'null',svg);
const hit=S('rect',{x:ml,y:yy-rh*0.45,width:W-mr-ml,height:rh*0.9,class:'hit'},svg);
const rows=[[fmt(r.g,4),'estimate'],['['+fmt(r.ci[0],4)+', '+fmt(r.ci[1],4)+']','Šidák 95 % CI'],[r.sd.toFixed(5),'sd(Γ)'],[fmt(r.z,2),'z'],['±'+r.X.toFixed(4),'X, 80 %-power MDE']];
if(r.floor!==null)rows.push(['±'+r.floor.toFixed(5),'floor-basis sd(Γ)']);rows.push([r.rej?'REJECT':'null','test at Šidák level'],[r.k,'']);
bindTip(hit,r.sym+'  '+r.what+' ('+ML[metric]+')',rows);}
return svg;}
function drawArms(){const W=760,H=330,ml=64,mr=20,mt=24,mb=56;const svg=S('svg',{viewBox:`0 0 ${W} ${H}`,'aria-label':'Per-seed '+ML[metric]+' by arm'});
const all=ARMS.flatMap(a=>DATA.seeds[metric][a[0]]);let lo=Math.min(...all),hi=Math.max(...all);const pad=0.06*(hi-lo);lo-=pad;hi+=pad;
const y=lin(lo,hi,H-mb,mt),bw=(W-ml-mr)/ARMS.length,xc=i=>ml+bw*(i+0.5);
const ts=niceTicks(lo,hi,6),tf=tickFmt(ts);
for(const t of ts){S('line',{x1:ml,x2:W-mr,y1:y(t),y2:y(t),stroke:'var(--grid)'},svg);T({x:ml-8,y:y(t)+4,'text-anchor':'end',class:'tick'},tf(t),svg);}
T({x:14,y:(mt+H-mb)/2,transform:`rotate(-90 14 ${(mt+H-mb)/2})`,'text-anchor':'middle',class:'axt'},ML[metric]+' at θ*, per seed',svg);
ARMS.forEach((a,i)=>{const v=DATA.seeds[metric][a[0]],mu=DATA.means[metric][a[0]];
T({x:xc(i),y:H-mb+18,'text-anchor':'middle',class:'tick'},a[1],svg).style.fill='var(--ink)';T({x:xc(i),y:H-mb+33,'text-anchor':'middle',class:'note'},'k = '+v.length,svg);
v.forEach((val,j)=>{const xx=xc(i)+bw*0.42*(((j*0.6180339887)%1)-0.5);
marker(a[3],xx,y(val),3.6,{fill:'none',stroke:`var(${a[2]})`,'stroke-width':1.3},svg);
const h=S('circle',{cx:xx,cy:y(val),r:9,class:'hit'},svg);bindTip(h,a[1]+', seed '+(j+1),[[val.toFixed(4),ML[metric]+' (mean of 512 eval episodes)']]);});
S('line',{x1:xc(i)-bw*0.3,x2:xc(i)+bw*0.3,y1:y(mu),y2:y(mu),stroke:'var(--ink)','stroke-width':2.5},svg);
const hm=S('rect',{x:xc(i)-bw*0.3,y:y(mu)-6,width:bw*0.6,height:12,class:'hit'},svg);bindTip(hm,a[1]+' arm mean',[[mu.toFixed(4),ML[metric]],['k = '+v.length,'']]);});
return svg;}
function render(){legend();const c=document.getElementById('chart');c.replaceChildren(view==='contrasts'?drawContrasts():drawArms());
if(view==='contrasts')table(document.getElementById('tbl'),['contrast','k','estimate','Šidák 95 % CI','sd(Γ)','z','X (MDE80)','floor-basis sd(Γ)','test'],
DATA.rows[metric].map(r=>[r.sym+' '+r.what,r.k.replace('k = ',''),fmt(r.g,4),'['+fmt(r.ci[0],4)+', '+fmt(r.ci[1],4)+']',r.sd.toFixed(5),fmt(r.z,2),r.X.toFixed(4),r.floor===null?'—':r.floor.toFixed(5),r.rej?'REJECT':'null']));
else table(document.getElementById('tbl'),['arm','k','arm mean'].concat(Array.from({length:72},(_,i)=>'seed '+(i+1))),
ARMS.map(a=>[a[1],String(DATA.seeds[metric][a[0]].length),DATA.means[metric][a[0]].toFixed(4)].concat(DATA.seeds[metric][a[0]].map(v=>v.toFixed(4)))));}
seg(document.getElementById('cm'),[['completion','completion'],['survival_rate','survival rate']],metric,v=>{metric=v;render();});
seg(document.getElementById('cv'),[['contrasts','contrasts'],['arms','per-seed arm values']],view,v=>{view=v;render();});
render();
"""


def interactive(rows, seeds, means):
    data = {
        "rows": {
            m: [
                {
                    k: r[k]
                    for k in (
                        "key",
                        "sym",
                        "what",
                        "k",
                        "g",
                        "ci",
                        "X",
                        "sd",
                        "z",
                        "rej",
                        "floor",
                    )
                }
                for r in rows[m]
            ]
            for m in METRICS
        },
        "seeds": seeds,
        "means": means,
    }
    return C.write_html(
        "fig08_gamma_contrasts.html", "Confirmatory contrast Γ", BODY, data, SCRIPT
    )


def main():
    rows, seeds, means = load()
    print(static_forest(rows).name)
    print(static_arms(seeds, means).name)
    print(interactive(rows, seeds, means).name)
    print("\nnumbers stated (text) in fig08_gamma_contrasts.png / .html:")
    for m in METRICS:
        for r in rows[m]:
            print(
                f"  {m:13s} {r['key']:8s} {C.fmt(r['g'])} {C.ci_text(*r['ci'])} "
                f"X={r['X']:.4f} sd={r['sd']:.5f} z={r['z']:+.2f} rej={r['rej']} "
                f"floor={r['floor']}  <- {r['src']}"
            )
    for m in METRICS:
        print(m, {a: (len(v), round(means[m][a], 4)) for a, v in seeds[m].items()})


if __name__ == "__main__":
    main()
