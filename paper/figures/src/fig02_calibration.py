# ruff: noqa: E501  (inline JS/CSS of a self-contained HTML figure)
"""Figure 2 (slot): percolation calibration. P_span(β) and R_L(β) at
L = 32, 48, 64 with their committed binomial SEs (512 seeds per point), the
locked critical point β̂_c = 0.500 ± 0.005 and the three locked severity
levels. Ledger O-2 is open: there is no committed artifact for the R_L
logistic centres behind β̂_c, so no logistic fit or centre is computed or
drawn; the band is the lock's value (docs/locks.yaml, severity_lock.md).

Outputs: out/img/fig02_calibration.png, out/html/fig02_calibration.html
"""

from __future__ import annotations

import common as C
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

EST = C.RES / "phase2" / "estimates.npz"
LS = (32, 48, 64)
LCOL = {32: C.SEV["Low"], 48: C.SEV["Medium"], 64: C.SEV["High"]}  # ordinal ramp
LMK = {32: "o", 48: "s", 64: "^"}
LEVELS = (("Low", 0.43), ("Medium", 0.49), ("High", 0.70))  # CAL-3
BETA_C, BETA_C_TOL = 0.500, 0.005  # CAL-1 (locked)
CAL3 = {0.43: 0.021, 0.49: 0.547, 0.70: 0.998}  # P_span at L = 64, CAL-3


def load():
    d = np.load(EST)
    out = dict(betas=d["betas"].astype(float), r_betas=d["r_betas"].astype(float))
    for L in LS:
        out[f"p{L}"] = d[f"p_span_L{L}"]
        out[f"pse{L}"] = d[f"p_span_se_L{L}"]
        out[f"r{L}"] = d[f"r_L{L}"]
        out[f"rse{L}"] = d[f"r_se_L{L}"]
    # the CAL-3 labels must be what the committed curve says at L = 64
    for b, v in CAL3.items():
        i = int(np.argmin(np.abs(out["betas"] - b)))
        assert (
            abs(out["betas"][i] - b) < 1e-6 and round(float(out["p64"][i]), 3) == v
        ), (b, out["p64"][i])
    return out


def static(D):
    C.mpl_setup()
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.0, 3.2), gridspec_kw={"wspace": 0.28})
    for L in LS:
        a1.errorbar(
            D["betas"],
            D[f"p{L}"],
            yerr=D[f"pse{L}"],
            color=LCOL[L],
            marker=LMK[L],
            ms=3.6,
            lw=1.3,
            elinewidth=0.8,
            capsize=0,
            mec=C.SURFACE,
            mew=0.6,
            label=f"L = {L}",
        )
        a2.errorbar(
            D["r_betas"],
            D[f"r{L}"],
            yerr=D[f"rse{L}"],
            color=LCOL[L],
            marker=LMK[L],
            ms=3.6,
            lw=1.3,
            elinewidth=0.8,
            capsize=0,
            mec=C.SURFACE,
            mew=0.6,
        )
    for ax in (a1, a2):
        ax.axvspan(
            BETA_C - BETA_C_TOL, BETA_C + BETA_C_TOL, color=C.BAND, lw=0, zorder=0
        )
        ax.axvline(BETA_C, color=C.INK2, lw=0.8, zorder=0.5)
        ax.grid(axis="y")
        ax.set_axisbelow(True)
        ax.set_xlabel("β, per-neighbour ignition probability")
    for name, b in LEVELS:
        a1.axvline(b, color=C.INK, lw=0.7, ls=(0, (1, 2)), zorder=0.6)
        ha, dx = {
            "Low": ("right", -0.006),
            "Medium": ("left", 0.006),
            "High": ("center", 0),
        }[name]
        a1.text(
            b + dx,
            1.03,
            f"{name}\n{b:.2f}",
            transform=a1.get_xaxis_transform(),
            ha=ha,
            va="bottom",
            fontsize=7,
            color=C.INK,
        )
        if b <= 0.60:
            a2.axvline(b, color=C.INK, lw=0.7, ls=(0, (1, 2)), zorder=0.6)
            a2.text(
                b,
                1.04,
                f"{name}\n{b:.2f}",
                transform=a2.get_xaxis_transform(),
                ha="center",
                va="bottom",
                fontsize=7,
                color=C.INK,
            )
    for b, v in CAL3.items():
        tx, ty, ha = {
            0.43: (0.415, 0.09, "right"),
            0.49: (0.51, 0.547, "left"),
            0.70: (0.72, 0.90, "left"),
        }[b]
        a1.annotate(
            f"{v:.3f}",
            (b, v),
            xytext=(tx, ty),
            fontsize=6.8,
            color=C.INK,
            ha=ha,
            va="center",
            arrowprops=dict(arrowstyle="-", color=C.INK2, lw=0.6),
        )
    a1.set_ylabel("P_span, centre ignition reaches the boundary")
    a1.set_xlim(0.03, 0.97)
    a1.set_ylim(-0.03, 1.03)
    a2.axhline(0.5, color=C.MUTED, lw=0.8, zorder=0.5)
    a2.text(0.598, 0.5, "R = 1/2", ha="right", va="bottom", fontsize=6.8, color=C.INK2)
    a2.set_ylabel("R_L, left–right crossing probability")
    a2.set_xlim(0.395, 0.605)
    a2.set_ylim(-0.03, 1.03)
    a2.text(
        BETA_C + 0.004,
        0.06,
        "β̂_c = 0.500 ± 0.005 (locked)",
        fontsize=6.8,
        color=C.INK2,
        ha="left",
    )
    handles = [
        Line2D(
            [0],
            [0],
            color=LCOL[L],
            marker=LMK[L],
            ms=4,
            lw=1.3,
            mec=C.SURFACE,
            label=f"L = {L}",
        )
        for L in LS
    ]
    handles += [
        Line2D([0], [0], color=C.INK2, lw=0.8, label="±1 SE (binomial, 512 seeds)"),
        Patch(
            facecolor=C.BAND,
            edgecolor=C.INK2,
            lw=0.6,
            label="β̂_c = 0.500 ± 0.005, locked",
        ),
        Line2D(
            [0],
            [0],
            color=C.INK,
            lw=0.7,
            ls=(0, (1, 2)),
            label="locked severity levels",
        ),
    ]
    fig.legend(
        handles=handles,
        loc="lower center",
        ncol=3,
        bbox_to_anchor=(0.5, -0.17),
        fontsize=7.2,
    )
    return C.save_png(fig, "fig02_calibration.png")


BODY = """
<div class="controls"><span class="lab">observable</span><span id="co"></span>
<span class="lab">grid size</span><span id="cl" style="display:inline-flex;gap:10px"></span></div>
<div class="legend" id="lg"></div>
<div id="chart"></div>
<div class="lab">β̂_c band: the locked value (severity lock record).</div>
<details><summary>Table view</summary><div class="tw" id="tbl"></div></details>
"""

SCRIPT = r"""
let obs='p';const on={32:true,48:true,64:true};
const LV={32:['--sev1','o'],48:['--sev2','s'],64:['--sev3','^']};
const LEVELS=[['Low',0.43],['Medium',0.49],['High',0.70]];
const cl=document.getElementById('cl');
for(const L of [32,48,64]){const lab=document.createElement('label');lab.style.fontSize='12px';lab.style.color='var(--ink2)';
const cb=document.createElement('input');cb.type='checkbox';cb.checked=true;cb.addEventListener('change',()=>{on[L]=cb.checked;render();});
lab.appendChild(cb);lab.appendChild(document.createTextNode(' L = '+L));cl.appendChild(lab);}
function legend(){const lg=document.getElementById('lg');lg.replaceChildren();
for(const L of [32,48,64]){const s=document.createElement('span');const sv=S('svg',{width:26,height:12,viewBox:'0 0 26 12'});
S('line',{x1:2,x2:24,y1:6,y2:6,stroke:`var(${LV[L][0]})`,'stroke-width':2},sv);marker(LV[L][1],13,6,3.5,{fill:`var(${LV[L][0]})`,stroke:'var(--surface)','stroke-width':1},sv);
s.appendChild(sv);s.appendChild(document.createTextNode('L = '+L));lg.appendChild(s);}
const s2=document.createElement('span');const sv2=S('svg',{width:26,height:12,viewBox:'0 0 26 12'});S('rect',{x:1,y:1,width:24,height:10,fill:'var(--band)',stroke:'var(--ink2)','stroke-width':0.6},sv2);
s2.appendChild(sv2);s2.appendChild(document.createTextNode('β̂_c = 0.500 ± 0.005, locked'));lg.appendChild(s2);
const s3=document.createElement('span');const sv3=S('svg',{width:26,height:12,viewBox:'0 0 26 12'});S('line',{x1:13,x2:13,y1:0,y2:12,stroke:'var(--ink)','stroke-width':1,'stroke-dasharray':'1.5 2.5'},sv3);
s3.appendChild(sv3);s3.appendChild(document.createTextNode('locked severity levels'));lg.appendChild(s3);
const s4=document.createElement('span');s4.textContent='bars: ±1 SE (binomial, 512 seeds)';lg.appendChild(s4);}
function render(){legend();const W=760,H=360,ml=62,mr=20,mt=40,mb=46;const svg=S('svg',{viewBox:`0 0 ${W} ${H}`});
const xs=obs==='p'?DATA.betas:DATA.r_betas;const x0=obs==='p'?0.03:0.395,x1=obs==='p'?0.97:0.605;
const x=lin(x0,x1,ml,W-mr),y=lin(-0.03,1.03,H-mb,mt);
S('rect',{x:x(0.495),y:mt,width:x(0.505)-x(0.495),height:H-mb-mt,fill:'var(--band)'},svg);
S('line',{x1:x(0.5),x2:x(0.5),y1:mt,y2:H-mb,stroke:'var(--ink2)'},svg);
for(const t of [0,0.25,0.5,0.75,1]){S('line',{x1:ml,x2:W-mr,y1:y(t),y2:y(t),stroke:'var(--grid)'},svg);T({x:ml-6,y:y(t)+4,'text-anchor':'end',class:'tick'},String(t),svg);}
const xt=obs==='p'?[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]:[0.40,0.45,0.50,0.55,0.60];
for(const t of xt)T({x:x(t),y:H-mb+16,'text-anchor':'middle',class:'tick'},t.toFixed(2),svg);
S('line',{x1:ml,x2:W-mr,y1:H-mb,y2:H-mb,stroke:'var(--axis)'},svg);
T({x:(ml+W-mr)/2,y:H-6,'text-anchor':'middle',class:'axt'},'β, per-neighbour ignition probability',svg);
T({x:14,y:(mt+H-mb)/2,transform:`rotate(-90 14 ${(mt+H-mb)/2})`,'text-anchor':'middle',class:'axt'},obs==='p'?'P_span, centre ignition reaches the boundary':'R_L, left–right crossing probability',svg);
if(obs==='r'){S('line',{x1:ml,x2:W-mr,y1:y(0.5),y2:y(0.5),stroke:'var(--muted)'},svg);T({x:W-mr-4,y:y(0.5)-4,'text-anchor':'end',class:'note'},'R = 1/2',svg);}
for(const [nm,b] of LEVELS){if(b<x0||b>x1)continue;S('line',{x1:x(b),x2:x(b),y1:mt,y2:H-mb,stroke:'var(--ink)','stroke-dasharray':'1.5 2.5'},svg);
T({x:x(b),y:mt-18,'text-anchor':'middle',class:'tick'},nm,svg).style.fill='var(--ink)';T({x:x(b),y:mt-5,'text-anchor':'middle',class:'note'},b.toFixed(2),svg);}
for(const L of [32,48,64]){if(!on[L])continue;const v=DATA[obs+L],se=DATA[obs+'se'+L];const col=`var(${LV[L][0]})`;
xs.forEach((b,i)=>S('line',{x1:x(b),x2:x(b),y1:y(v[i]-se[i]),y2:y(v[i]+se[i]),stroke:col,'stroke-width':1},svg));
S('path',{d:'M'+xs.map((b,i)=>x(b)+','+y(v[i])).join('L'),fill:'none',stroke:col,'stroke-width':2,'stroke-linejoin':'round'},svg);
xs.forEach((b,i)=>marker(LV[L][1],x(b),y(v[i]),3.4,{fill:col,stroke:'var(--surface)','stroke-width':1},svg));}
const cross=S('line',{y1:mt,y2:H-mb,stroke:'var(--muted)',visibility:'hidden'},svg);
const hit=S('rect',{x:ml,y:mt,width:W-mr-ml,height:H-mb-mt,class:'hit',tabindex:0},svg);let cur=Math.floor(xs.length/2);
function at(i,cx,cy){cross.setAttribute('x1',x(xs[i]));cross.setAttribute('x2',x(xs[i]));cross.setAttribute('visibility','visible');
const rows=[];for(const L of [32,48,64])if(on[L])rows.push([DATA[obs+L][i].toFixed(3)+' ± '+DATA[obs+'se'+L][i].toFixed(3),'L = '+L]);showTip(cx,cy,'β = '+xs[i].toFixed(2),rows);}
hit.addEventListener('pointermove',ev=>{const r=svg.getBoundingClientRect();const sx=(ev.clientX-r.left)*W/r.width;let b=0,bd=1e9;xs.forEach((v,i)=>{const d=Math.abs(x(v)-sx);if(d<bd){bd=d;b=i;}});cur=b;at(b,ev.clientX,ev.clientY);});
hit.addEventListener('pointerleave',()=>{cross.setAttribute('visibility','hidden');hideTip();});
hit.addEventListener('keydown',ev=>{if(ev.key==='ArrowLeft'||ev.key==='ArrowRight'){cur=Math.max(0,Math.min(xs.length-1,cur+(ev.key==='ArrowLeft'?-1:1)));const r=svg.getBoundingClientRect();at(cur,r.left+x(xs[cur])*r.width/W,r.top+mt*r.height/H+40);ev.preventDefault();}});
hit.addEventListener('blur',()=>{cross.setAttribute('visibility','hidden');hideTip();});
document.getElementById('chart').replaceChildren(svg);
table(document.getElementById('tbl'),['β','L = 32','L = 48','L = 64'],xs.map((b,i)=>[b.toFixed(2)].concat([32,48,64].map(L=>DATA[obs+L][i].toFixed(3)+' ± '+DATA[obs+'se'+L][i].toFixed(3)))));}
seg(document.getElementById('co'),[['p','P_span'],['r','R_L']],obs,v=>{obs=v;render();});
render();
"""


def main():
    D = load()
    print(static(D).name)
    data = {
        "betas": [round(float(b), 4) for b in D["betas"]],
        "r_betas": [round(float(b), 4) for b in D["r_betas"]],
    }
    for L in LS:
        data[f"p{L}"] = D[f"p{L}"].tolist()
        data[f"pse{L}"] = D[f"pse{L}"].tolist()
        data[f"r{L}"] = D[f"r{L}"].tolist()
        data[f"rse{L}"] = D[f"rse{L}"].tolist()
    print(
        C.write_html(
            "fig02_calibration.html", "Percolation calibration", BODY, data, SCRIPT
        ).name
    )


if __name__ == "__main__":
    main()
