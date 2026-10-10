# ruff: noqa: E501  (inline JS/CSS of a self-contained HTML figure)
"""Figure 10 (slot), SECONDARY and non-verdict-bearing: the dose sweep
(m = 0.5, n = p) and the identification arm (m = 0.4, n = 0.2 + p) at θ*,
T* = 1000; the committed confound-plane fit per arm; the design space with
JOINT's position outside the sampled region; the plane's committed
prediction for JOINT − ISO-4 (γ_p × 1) beside the measured Γ₄ and Γ₄′; the
committed secondary estimates. Every interval is the committed one: 95 %
bootstrap-over-seeds for the secondary family (not family-corrected), Šidák
for Γ₄ and Γ₄′. Nothing is re-estimated; per-seed values are plotted only,
and their means are asserted equal to the committed arm means.

Outputs: out/img/fig10_secondary.png, out/html/fig10_secondary.html
"""

from __future__ import annotations

import math

import common as C
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

SEC = C.P6 / "secondary" / "secondary.json"
G4 = C.P6 / "post_unblind_analysis" / "post_gamma4_t2000.json"
METRICS = ("survival_rate", "completion")
MLABEL = {"completion": "completion", "survival_rate": "survival rate"}
THETA = "che/configs/theta_star_holdout.yaml"
# reference arms' design coordinates (p = P(A∧B), n = P(no active element)):
# ISO (0, 1/3): ledger DES-7, DES-8; ISO-4 (0, 0) and JOINT (1, 0): DES-14
REF = {"ISO": (0.0, 1 / 3), "ISO-4": (0.0, 0.0), "JOINT": (1.0, 0.0)}


def read_eval(p, m):
    d = C.load_json(p)
    assert d["ckpt_step"] == 1000 and d["n_episodes"] == 512 and d["seed"] == 0, p
    assert d["config"] == THETA, p
    return float(d["metrics"][m]["mean"])


def load():
    s = C.load_json(SEC)
    g4 = C.load_json(G4)
    design = s["design"]
    arms = {}
    for row in design:
        a = row["arm"]
        arms[a] = dict(
            m=row["m"],
            p=row["p"],
            n=row["n"],
            fam="sweep" if a.startswith("sweep") else "ident",
            seeds={},
            mean={},
            fit={},
            rz={},
        )
        for met in METRICS:
            arms[a]["seeds"][met] = [
                read_eval(
                    (C.P6 / ("g1_sec_s1_12_5090" if k <= 12 else "g1_grid"))
                    / f"eval_{a}_s{k}.json",
                    met,
                )
                for k in range(1, 21)
            ]
            rec = next(
                r
                for r in s["metrics"][met]["confound"]["arm_means_vs_plane"]
                if r["arm"] == a
            )
            arms[a]["mean"][met] = rec["mean"]
            arms[a]["fit"][met] = rec["fit"]
            arms[a]["rz"][met] = rec["resid_over_se"]
            v = arms[a]["seeds"][met]
            assert math.isclose(sum(v) / len(v), rec["mean"], abs_tol=1e-9), (a, met)
    est = {}
    for met in METRICS:
        M = s["metrics"][met]
        dt, kn, cf, eg = M["dose_trend"], M["knee"], M["confound"], M["endpoint_grade"]
        G = g4["gamma4"]["per_metric"][met]["gamma4"]
        R = s["replicate"][met]["gamma4_prime"]
        est[met] = dict(
            rows=[
                dict(
                    lab="dose slope (sweep), per unit p",
                    g=dt["ols_slope_per_unit_p"],
                    ci=dt["ols_slope_ci95"],
                    lvl="95 %",
                    floor=None,
                ),
                dict(
                    lab="endpoint, sweep p = 0.5 − p = 0",
                    g=eg["endpoint_diff"],
                    ci=eg["ci95"],
                    lvl="95 %",
                    floor=eg["se_floor_basis"],
                ),
                dict(
                    lab="γ_p, per unit p (plane)",
                    g=cf["gamma_p"],
                    ci=cf["gamma_p_ci95"],
                    lvl="95 %",
                    floor=None,
                ),
                dict(
                    lab="γ_n, per unit n (plane)",
                    g=cf["gamma_n"],
                    ci=cf["gamma_n_ci95"],
                    lvl="95 %",
                    floor=None,
                ),
                dict(
                    lab="bound, no-element share of sweep change",
                    g=cf["bound_confound_share_of_sweep_change"],
                    ci=cf["bound_ci95"],
                    lvl="95 %",
                    floor=None,
                ),
            ],
            pred=[
                dict(
                    lab="plane prediction, γ_p × 1 (p: 0 → 1, n: 0 → 0)",
                    g=cf["gamma_p"],
                    ci=cf["gamma_p_ci95"],
                    lvl="95 %",
                    kind="pred",
                ),
                dict(
                    lab="Γ₄ = JOINT − ISO-4, measured",
                    g=G["gamma"],
                    ci=G["ci_sidak"],
                    lvl="Šidák 95 %",
                    kind="meas",
                ),
                dict(
                    lab="Γ₄′ = JOINT − sweep_c50_p000, measured",
                    g=R["gamma"],
                    ci=R["ci_sidak"],
                    lvl="Šidák 95 %",
                    kind="meas",
                ),
            ],
            knee=dict(
                kappa=kn["kappa"],
                ci=kn["ci95"],
                flag=kn["flag"].split(" —")[0],
                underpowered=kn["underpowered"],
            ),
            iso=dict(dt["isotonic_fit"]),
            floor_p500=eg["floor_sd_sweep_p500"],
            floor_note=eg["floor_note"],
        )
        assert kn["underpowered"] is True
    med = dict(
        void=s["mediation"]["void"], verdict=s["mediation"]["verdict"].split(" —")[0]
    )
    return arms, est, med


# ------------------------------------------------------------------ static
SW_STYLE = dict(color=C.S1, marker="o")
ID_STYLE = dict(color=C.S2, marker="s")


def dose_panel(ax, arms, est, met):
    for fam, st, off in (("sweep", SW_STYLE, -0.012), ("ident", ID_STYLE, 0.012)):
        A = [a for a in arms.values() if a["fam"] == fam]
        A.sort(key=lambda a: a["p"])
        for a in A:
            v = a["seeds"][met]
            xs = [
                a["p"] + off + 0.016 * (((j * 0.6180339887) % 1.0) - 0.5)
                for j in range(len(v))
            ]
            ax.scatter(
                xs,
                v,
                s=5,
                marker=st["marker"],
                facecolors="none",
                edgecolors=st["color"],
                linewidths=0.5,
                alpha=0.55,
                zorder=2,
            )
        ps = [a["p"] + off for a in A]
        ax.plot(ps, [a["mean"][met] for a in A], color=st["color"], lw=1.6, zorder=3)
        ax.plot(
            ps,
            [a["mean"][met] for a in A],
            st["marker"],
            color=st["color"],
            ms=5.5,
            mec=C.SURFACE,
            mew=1.0,
            zorder=4,
        )
        ax.plot(
            ps,
            [a["fit"][met] for a in A],
            color=C.INK,
            lw=0.9,
            ls=(0, (1, 1.6)),
            zorder=3.5,
        )
    # floor: rerun sd at sweep p = 0.5 only (the only floored arm)
    a5 = arms["sweep_c50_p500"]
    f = est[met]["floor_p500"]
    ax.add_patch(
        plt.Rectangle(
            (0.5 + 0.03, a5["mean"][met] - f),
            0.022,
            2 * f,
            facecolor="none",
            edgecolor=C.HATCH,
            hatch="////",
            lw=0,
            zorder=2,
        )
    )
    # knee CI bracket on the p axis, UNDERPOWERED
    kn = est[met]["knee"]
    ylo, yhi = ax.get_ylim()
    yk = yhi + 0.04 * (yhi - ylo)
    ax.plot(kn["ci"], [yk, yk], color=C.INK2, lw=1.2, clip_on=False)
    for xe in kn["ci"]:
        ax.plot(
            [xe, xe],
            [yk - 0.012 * (yhi - ylo), yk + 0.012 * (yhi - ylo)],
            color=C.INK2,
            lw=1.0,
            clip_on=False,
        )
    ax.plot([kn["kappa"]], [yk], "v", color=C.INK2, ms=4, clip_on=False)
    ax.text(
        kn["ci"][1] + 0.02,
        yk,
        "knee 95 % CI: " + kn["flag"],
        fontsize=6.8,
        color=C.INK2,
        va="center",
        clip_on=False,
    )
    ax.set_ylim(ylo, yhi)
    ax.set_xlim(-0.04, 0.6)
    ax.set_xticks([0, 0.125, 0.25, 0.375, 0.5])
    ax.set_xticklabels(["0", "0.125", "0.25", "0.375", "0.5"])
    ax.set_xlabel("p, share of training episodes with both elements")
    ax.set_ylabel(f"{MLABEL[met]} at θ*")
    ax.grid(axis="y")
    ax.set_axisbelow(True)
    ax.set_title(MLABEL[met], pad=16)


def design_panel(ax, arms):
    sw = sorted([a for a in arms.values() if a["fam"] == "sweep"], key=lambda a: a["p"])
    idn = sorted(
        [a for a in arms.values() if a["fam"] == "ident"], key=lambda a: a["p"]
    )
    ax.axvspan(0, 0.5, color=C.BAND, zorder=0, lw=0)
    ax.text(
        0.25, 0.71, "sampled p range", ha="center", va="top", fontsize=6.4, color=C.INK2
    )
    ax.plot(
        [a["p"] for a in sw],
        [a["n"] for a in sw],
        "-o",
        color=C.S1,
        ms=4.5,
        lw=1.2,
        mec=C.SURFACE,
        zorder=3,
    )
    ax.plot(
        [a["p"] for a in idn],
        [a["n"] for a in idn],
        "-s",
        color=C.S2,
        ms=4.5,
        lw=1.2,
        mec=C.SURFACE,
        zorder=3,
    )
    for name, (p, n) in REF.items():
        mk = {"ISO": "o", "ISO-4": "^", "JOINT": "s"}[name]
        ax.plot([p], [n], mk, ms=7.5, mfc="none", mec=C.INK, mew=1.4, zorder=5)
    ax.text(
        0.98,
        0.07,
        "JOINT\n(p = 1, n = 0)",
        fontsize=6.8,
        ha="right",
        va="bottom",
        color=C.INK,
    )
    ax.text(
        0.06,
        -0.07,
        "ISO-4 and sweep_c50_p000 (p = 0, n = 0)",
        fontsize=6.6,
        va="top",
        color=C.INK,
    )
    ax.text(
        -0.05,
        1 / 3,
        "ISO\n(p = 0,\nn = 1/3)",
        fontsize=6.6,
        ha="right",
        va="center",
        color=C.INK,
    )
    ax.set_xlim(-0.3, 1.08)
    ax.set_ylim(-0.2, 0.72)
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_xticklabels(["0", "0.25", "0.5", "0.75", "1"])
    ax.set_yticks([0, 0.2, 0.4, 0.6])
    ax.set_xlabel("p, both-element share")
    ax.set_ylabel("n, no-element share")
    ax.set_title("design space (p, n)", pad=6)
    ax.grid(True)
    ax.set_axisbelow(True)


def forest(ax, rows, title):
    lo = min(r["ci"][0] for r in rows)
    hi = max(r["ci"][1] for r in rows)
    for r in rows:
        if r.get("floor"):
            lo, hi = min(lo, -r["floor"]), max(hi, r["floor"])
    pad = 0.06 * (hi - lo)
    ax.set_xlim(lo - pad, hi + pad)
    ax.axvline(0, color=C.MUTED, lw=0.8)
    n = len(rows)
    for i, r in enumerate(rows):
        y = i
        if r.get("floor"):
            ax.add_patch(
                plt.Rectangle(
                    (-r["floor"], y - 0.22),
                    2 * r["floor"],
                    0.44,
                    facecolor="none",
                    edgecolor=C.HATCH,
                    hatch="////",
                    lw=0,
                    zorder=0,
                )
            )
        meas = r.get("kind") == "meas"
        col = C.INK2 if meas else C.INK
        ax.plot(r["ci"], [y, y], color=col, lw=1.6, solid_capstyle="butt")
        for xe in r["ci"]:
            ax.plot([xe, xe], [y - 0.11, y + 0.11], color=col, lw=1.0)
        mk = "D" if r.get("kind") == "pred" else ("^" if meas else "o")
        ax.plot(
            [r["g"]],
            [y],
            mk,
            color=col,
            ms=5.2,
            mfc=C.SURFACE if r.get("kind") == "pred" else col,
            mec=col,
            mew=1.3,
        )
        ax.text(
            0.0,
            y - 0.3,
            f"{r['lab']}  ·  {r['lvl']} CI",
            transform=ax.get_yaxis_transform(),
            fontsize=6.7,
            color=C.INK,
            va="bottom",
            ha="left",
            zorder=6,
            bbox=dict(facecolor=C.SURFACE, edgecolor="none", pad=0.6, alpha=0.9),
        )
    ax.set_yticks([])
    ax.set_ylim(n - 0.55, -0.85)
    ax.spines["left"].set_visible(False)
    ax.set_title(title, pad=4, fontsize=8.4)


def static(arms, est, med):
    C.mpl_setup()
    fig = plt.figure(figsize=(7.2, 8.6))
    gs = fig.add_gridspec(3, 2, height_ratios=[1.1, 1.0, 1.15], hspace=0.62, wspace=0.3)
    ax_s = fig.add_subplot(gs[0, 0])
    ax_c = fig.add_subplot(gs[0, 1])
    dose_panel(ax_s, arms, est, "survival_rate")
    dose_panel(ax_c, arms, est, "completion")
    ax_d = fig.add_subplot(gs[1, 0])
    design_panel(ax_d, arms)
    ax_p = fig.add_subplot(gs[1, 1])
    forest(
        ax_p,
        est["survival_rate"]["pred"],
        "survival rate: JOINT minus a (p = 0, n = 0) arm",
    )
    ax_p.set_xlabel("difference in survival rate (fraction)")
    ax_e1 = fig.add_subplot(gs[2, 0])
    ax_e2 = fig.add_subplot(gs[2, 1])
    forest(ax_e1, est["survival_rate"]["rows"], "survival rate: secondary estimates")
    forest(ax_e2, est["completion"]["rows"], "completion: secondary estimates")
    for ax in (ax_e1, ax_e2):
        ax.set_xlabel("fraction, or fraction per unit p / n")
    fig.text(
        0.5,
        0.985,
        "SECONDARY · non-verdict-bearing · 95 % bootstrap-over-seeds "
        "intervals, not family-corrected · k = 20 per arm",
        ha="center",
        fontsize=7.8,
        color=C.INK,
        weight="bold",
    )
    fig.text(
        0.98,
        0.035,
        f"mediation: {med['verdict']}",
        ha="right",
        fontsize=7.2,
        color=C.INK2,
    )
    handles = [
        Line2D(
            [0],
            [0],
            color=C.S1,
            marker="o",
            lw=1.6,
            ms=5,
            mec=C.SURFACE,
            label="sweep arms (m = 0.5, n = p): arm mean",
        ),
        Line2D(
            [0],
            [0],
            color=C.S2,
            marker="s",
            lw=1.6,
            ms=5,
            mec=C.SURFACE,
            label="identification arms (m = 0.4, n = 0.2 + p): arm mean",
        ),
        Line2D(
            [0],
            [0],
            marker="o",
            ls="none",
            mfc="none",
            mec=C.INK2,
            ms=3.5,
            label="one training seed",
        ),
        Line2D(
            [0], [0], color=C.INK, lw=0.9, ls=(0, (1, 1.6)), label="confound-plane fit"
        ),
        Patch(
            facecolor="none",
            edgecolor=C.HATCH,
            hatch="////",
            lw=0,
            label="floor: ±1 rerun sd (sweep p = 0.5) / ±1 floor-basis SE (endpoint)",
        ),
        Line2D(
            [0],
            [0],
            marker="D",
            color=C.INK,
            mfc=C.SURFACE,
            lw=1.6,
            ms=5,
            label="plane prediction, 95 % CI",
        ),
        Line2D(
            [0],
            [0],
            marker="^",
            color=C.INK2,
            lw=1.6,
            ms=5,
            label="measured contrast, Šidák 95 % CI",
        ),
        Line2D(
            [0],
            [0],
            marker="o",
            color=C.INK,
            lw=1.6,
            ms=5,
            label="secondary estimate, 95 % CI",
        ),
    ]
    fig.legend(
        handles=handles,
        loc="lower center",
        ncol=2,
        bbox_to_anchor=(0.5, -0.045),
        fontsize=6.9,
    )
    return C.save_png(fig, "fig10_secondary.png")


# ------------------------------------------------------------------ interactive
BODY = """
<div class="controls"><span class="lab">metric</span><span id="cm"></span></div>
<div class="lab" style="color:var(--ink);font-weight:600;margin-bottom:4px">SECONDARY · non-verdict-bearing · 95 % bootstrap-over-seeds intervals, not family-corrected · k = 20 per arm</div>
<div class="legend" id="lg"></div>
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:6px 18px">
<div id="dose"></div><div id="design"></div><div id="pred"></div><div id="est"></div></div>
<div class="lab" id="med"></div>
<details><summary>Table view</summary><div class="tw" id="tbl1"></div><div class="tw" id="tbl2"></div></details>
"""

SCRIPT = r"""
let metric='survival_rate';
const ML={completion:'completion',survival_rate:'survival rate'};
const ARMS=Object.entries(DATA.arms).map(([k,v])=>Object.assign({name:k},v));
function legend(){const lg=document.getElementById('lg');lg.replaceChildren();
const it=[['sw','sweep arms (m = 0.5, n = p)'],['id','identification arms (m = 0.4, n = 0.2 + p)'],['seed','one training seed'],['fit','confound-plane fit'],['floor','floor (see tooltip)'],['pred','plane prediction, 95 % CI'],['meas','measured contrast, Šidák 95 % CI']];
for(const [k,lab] of it){const s=document.createElement('span');const sv=S('svg',{width:26,height:12,viewBox:'0 0 26 12'});
if(k==='sw'){S('line',{x1:2,x2:24,y1:6,y2:6,stroke:'var(--s1)','stroke-width':2},sv);marker('o',13,6,3.5,{fill:'var(--s1)',stroke:'var(--surface)','stroke-width':1.2},sv);}
if(k==='id'){S('line',{x1:2,x2:24,y1:6,y2:6,stroke:'var(--s2)','stroke-width':2},sv);marker('s',13,6,3.5,{fill:'var(--s2)',stroke:'var(--surface)','stroke-width':1.2},sv);}
if(k==='seed')marker('o',13,6,3,{fill:'none',stroke:'var(--ink2)','stroke-width':1},sv);
if(k==='fit')S('line',{x1:2,x2:24,y1:6,y2:6,stroke:'var(--ink)','stroke-width':1.2,'stroke-dasharray':'1.5 2.5'},sv);
if(k==='floor'){const d=S('defs',null,sv);const p=S('pattern',{id:'lf2',width:4,height:4,patternUnits:'userSpaceOnUse',patternTransform:'rotate(45)'},d);S('line',{x1:0,y1:0,x2:0,y2:4,stroke:'var(--muted)','stroke-width':1},p);S('rect',{x:1,y:1,width:24,height:10,fill:'url(#lf2)'},sv);}
if(k==='pred'){S('line',{x1:2,x2:24,y1:6,y2:6,stroke:'var(--ink)','stroke-width':2},sv);marker('D',13,6,3.5,{fill:'var(--surface)',stroke:'var(--ink)','stroke-width':1.5},sv);}
if(k==='meas'){S('line',{x1:2,x2:24,y1:6,y2:6,stroke:'var(--ink2)','stroke-width':2},sv);marker('^',13,6,3.5,{fill:'var(--ink2)'},sv);}
s.appendChild(sv);s.appendChild(document.createTextNode(lab));lg.appendChild(s);}}
function pat(svg,id){const d=S('defs',null,svg);const p=S('pattern',{id:id,width:5,height:5,patternUnits:'userSpaceOnUse',patternTransform:'rotate(45)'},d);S('line',{x1:0,y1:0,x2:0,y2:5,stroke:'var(--muted)','stroke-width':1},p);}
function dose(){const W=380,H=290,ml=56,mr=14,mt=46,mb=44;const svg=S('svg',{viewBox:`0 0 ${W} ${H}`,'aria-label':'Dose sweep, '+ML[metric]});pat(svg,'pd');
const E=DATA.est[metric];const all=ARMS.flatMap(a=>a.seeds[metric]);let lo=Math.min(...all),hi=Math.max(...all);const pd=0.05*(hi-lo);lo-=pd;hi+=pd;
const x=lin(-0.04,0.6,ml,W-mr),y=lin(lo,hi,H-mb,mt);const ts=niceTicks(lo,hi,5),tf=tickFmt(ts);
for(const t of ts){S('line',{x1:ml,x2:W-mr,y1:y(t),y2:y(t),stroke:'var(--grid)'},svg);T({x:ml-6,y:y(t)+4,'text-anchor':'end',class:'tick'},tf(t),svg);}
S('line',{x1:ml,x2:W-mr,y1:H-mb,y2:H-mb,stroke:'var(--axis)'},svg);
for(const p of [0,0.125,0.25,0.375,0.5])T({x:x(p),y:H-mb+15,'text-anchor':'middle',class:'tick'},String(p),svg);
T({x:(ml+W-mr)/2,y:H-6,'text-anchor':'middle',class:'axt'},'p, share of training episodes with both elements',svg);
T({x:12,y:(mt+H-mb)/2,transform:`rotate(-90 12 ${(mt+H-mb)/2})`,'text-anchor':'middle',class:'axt'},ML[metric]+' at θ*',svg);
T({x:4,y:14,class:'ttl'},'dose sweep and identification arms',svg);
const kn=E.knee,yk=mt-12;S('line',{x1:x(kn.ci[0]),x2:x(kn.ci[1]),y1:yk,y2:yk,stroke:'var(--ink2)','stroke-width':1.5},svg);
for(const e of kn.ci)S('line',{x1:x(e),x2:x(e),y1:yk-4,y2:yk+4,stroke:'var(--ink2)','stroke-width':1.2},svg);
marker('^',x(kn.kappa),yk+1,3.5,{fill:'var(--ink2)',transform:`rotate(180 ${x(kn.kappa)} ${yk+1})`},svg);
T({x:x(kn.ci[1])+8,y:yk+4,class:'note'},'knee 95 % CI: '+kn.flag,svg);
const kh=S('rect',{x:x(kn.ci[0])-4,y:yk-8,width:x(kn.ci[1])-x(kn.ci[0])+8,height:16,class:'hit'},svg);
bindTip(kh,'knee ('+ML[metric]+')',[[String(kn.kappa),'κ̂'],['['+kn.ci[0]+', '+kn.ci[1]+']','95 % CI'],[kn.flag,'']]);
const a5=DATA.arms.sweep_c50_p500,f=E.floor_p500;
const fr=S('rect',{x:x(0.53),y:y(a5.mean[metric]+f),width:x(0.552)-x(0.53),height:y(a5.mean[metric]-f)-y(a5.mean[metric]+f),fill:'url(#pd)'},svg);
const fh=S('rect',{x:x(0.525),y:y(a5.mean[metric]+f)-2,width:x(0.56)-x(0.525),height:y(a5.mean[metric]-f)-y(a5.mean[metric]+f)+4,class:'hit'},svg);
bindTip(fh,'floor, sweep_c50_p500',[['±'+f.toFixed(4),'rerun sd (8 reps)'],[E.floor_note,'']]);
for(const [fam,col,mk,off] of [['sweep','var(--s1)','o',-0.012],['ident','var(--s2)','s',0.012]]){
const A=ARMS.filter(a=>a.fam===fam).sort((a,b)=>a.p-b.p);
for(const a of A)a.seeds[metric].forEach((v,j)=>{const xx=x(a.p+off+0.016*(((j*0.6180339887)%1)-0.5));marker(mk,xx,y(v),2.4,{fill:'none',stroke:col,'stroke-width':0.8,'stroke-opacity':0.6},svg);});
S('path',{d:'M'+A.map(a=>x(a.p+off)+','+y(a.mean[metric])).join('L'),fill:'none',stroke:col,'stroke-width':2},svg);
S('path',{d:'M'+A.map(a=>x(a.p+off)+','+y(a.fit[metric])).join('L'),fill:'none',stroke:'var(--ink)','stroke-width':1.2,'stroke-dasharray':'1.5 2.5'},svg);
for(const a of A){marker(mk,x(a.p+off),y(a.mean[metric]),4.5,{fill:col,stroke:'var(--surface)','stroke-width':1.5},svg);
const h=S('circle',{cx:x(a.p+off),cy:y(a.mean[metric]),r:11,class:'hit'},svg);
bindTip(h,a.name,[[a.mean[metric].toFixed(4),'arm mean, '+ML[metric]],[a.fit[metric].toFixed(4),'plane fit'],[fmt(a.rz[metric],1),'(mean − fit) / SE'],['m = '+a.m+', p = '+a.p+', n = '+(+a.n.toFixed(3)),''],['k = 20','']]);}}
return svg;}
function design(){const W=380,H=290,ml=50,mr=14,mt=30,mb=44;const svg=S('svg',{viewBox:`0 0 ${W} ${H}`,'aria-label':'Design space'});
const x=lin(-0.42,1.08,ml,W-mr),y=lin(-0.2,0.72,H-mb,mt);
S('rect',{x:x(0),y:mt,width:x(0.5)-x(0),height:H-mb-mt,fill:'var(--band)'},svg);
T({x:(x(0)+x(0.5))/2,y:mt+12,'text-anchor':'middle',class:'note'},'sampled p range',svg);
for(const t of [0,0.25,0.5,0.75,1]){S('line',{x1:x(t),x2:x(t),y1:mt,y2:H-mb,stroke:'var(--grid)'},svg);T({x:x(t),y:H-mb+15,'text-anchor':'middle',class:'tick'},String(t),svg);}
for(const t of [0,0.2,0.4,0.6]){S('line',{x1:ml,x2:W-mr,y1:y(t),y2:y(t),stroke:'var(--grid)'},svg);T({x:ml-6,y:y(t)+4,'text-anchor':'end',class:'tick'},String(t),svg);}
T({x:(ml+W-mr)/2,y:H-6,'text-anchor':'middle',class:'axt'},'p, both-element share',svg);
T({x:12,y:(mt+H-mb)/2,transform:`rotate(-90 12 ${(mt+H-mb)/2})`,'text-anchor':'middle',class:'axt'},'n, no-element share',svg);
T({x:4,y:14,class:'ttl'},'design space (p, n)',svg);
for(const [fam,col,mk] of [['sweep','var(--s1)','o'],['ident','var(--s2)','s']]){const A=ARMS.filter(a=>a.fam===fam).sort((a,b)=>a.p-b.p);
S('path',{d:'M'+A.map(a=>x(a.p)+','+y(a.n)).join('L'),fill:'none',stroke:col,'stroke-width':1.5},svg);
for(const a of A){marker(mk,x(a.p),y(a.n),4,{fill:col,stroke:'var(--surface)','stroke-width':1.5},svg);const h=S('circle',{cx:x(a.p),cy:y(a.n),r:10,class:'hit'},svg);
bindTip(h,a.name,[['m = '+a.m,''],['p = '+a.p,''],['n = '+(+a.n.toFixed(3)),'']]);}}
for(const [nm,[p,n],mk,lab,dx,dy,anc] of [['ISO',DATA.ref.ISO,'o','ISO (p = 0, n = 1/3)',-10,4,'end'],['ISO-4',DATA.ref['ISO-4'],'^','ISO-4 and sweep_c50_p000 (p = 0, n = 0)',8,22,'start'],['JOINT',DATA.ref.JOINT,'s','JOINT (p = 1, n = 0)',0,-14,'end']]){
marker(mk,x(p),y(n),5.5,{fill:'var(--surface)',stroke:'var(--ink)','stroke-width':1.6},svg);T({x:x(p)+dx,y:y(n)+dy,'text-anchor':anc,class:'note'},lab,svg).style.fill='var(--ink)';
const h=S('circle',{cx:x(p),cy:y(n),r:11,class:'hit'},svg);bindTip(h,nm,[['p = '+(+p.toFixed(3)),'both-element share'],['n = '+(+n.toFixed(3)),'no-element share']]);}
return svg;}
function forest(rows,title,unit,id){const W=380,rh=44,ml=12,mr=14,mt=30,mb=40,H=mt+mb+rh*rows.length;const svg=S('svg',{viewBox:`0 0 ${W} ${H}`,'aria-label':title});pat(svg,id);
let lo=Math.min(...rows.map(r=>Math.min(r.ci[0],r.floor?-r.floor:0))),hi=Math.max(...rows.map(r=>Math.max(r.ci[1],r.floor?r.floor:0)));const pd=0.06*(hi-lo);lo-=pd;hi+=pd;
const x=lin(lo,hi,ml,W-mr),y=i=>mt+rh*(i+0.62);const ts=niceTicks(lo,hi,5),tf=tickFmt(ts);
for(const t of ts){S('line',{x1:x(t),x2:x(t),y1:mt,y2:H-mb,stroke:'var(--grid)'},svg);T({x:x(t),y:H-mb+15,'text-anchor':'middle',class:'tick'},tf(t),svg);}
S('line',{x1:x(0),x2:x(0),y1:mt,y2:H-mb,stroke:'var(--muted)'},svg);S('line',{x1:ml,x2:W-mr,y1:H-mb,y2:H-mb,stroke:'var(--axis)'},svg);
T({x:4,y:14,class:'ttl'},title,svg);T({x:(ml+W-mr)/2,y:H-6,'text-anchor':'middle',class:'axt'},unit,svg);
rows.forEach((r,i)=>{const yy=y(i);if(r.floor)S('rect',{x:x(-r.floor),y:yy-7,width:x(r.floor)-x(-r.floor),height:14,fill:`url(#${id})`},svg);
const meas=r.kind==='meas',col=meas?'var(--ink2)':'var(--ink)';S('line',{x1:x(r.ci[0]),x2:x(r.ci[1]),y1:yy,y2:yy,stroke:col,'stroke-width':2},svg);
for(const e of r.ci)S('line',{x1:x(e),x2:x(e),y1:yy-5,y2:yy+5,stroke:col,'stroke-width':1.3},svg);
const mk=r.kind==='pred'?'D':(meas?'^':'o');marker(mk,x(r.g),yy,4.5,{fill:r.kind==='pred'?'var(--surface)':col,stroke:col,'stroke-width':1.5},svg);
const lab=T({x:ml,y:yy-11,class:'tick','paint-order':'stroke',stroke:'var(--surface)','stroke-width':3},r.lab+'  ·  '+r.lvl+' CI',svg);lab.style.fill='var(--ink)';
const h=S('rect',{x:0,y:yy-rh*0.62,width:W,height:rh,class:'hit'},svg);const tr=[[fmt(r.g,4),'estimate'],['['+fmt(r.ci[0],4)+', '+fmt(r.ci[1],4)+']',r.lvl+' CI']];if(r.floor)tr.push(['±'+r.floor.toFixed(4),'floor-basis SE (p = 0.5 floor assumed common at p = 0)']);bindTip(h,r.lab,tr);});
return svg;}
function render(){legend();const E=DATA.est[metric];
document.getElementById('dose').replaceChildren(dose());document.getElementById('design').replaceChildren(design());
document.getElementById('pred').replaceChildren(metric==='survival_rate'?forest(E.pred,'survival rate: JOINT minus a (p = 0, n = 0) arm','difference in survival rate (fraction)','pp'):forest(E.pred,'completion: JOINT minus a (p = 0, n = 0) arm','difference in completion (fraction)','pp'));
document.getElementById('est').replaceChildren(forest(E.rows,ML[metric]+': secondary estimates','fraction, or fraction per unit p / n','pe'));
document.getElementById('med').textContent='mediation: '+DATA.med.verdict;
table(document.getElementById('tbl1'),['arm','m','p','n','arm mean','plane fit','(mean − fit) / SE','k'],ARMS.map(a=>[a.name,String(a.m),String(a.p),String(+a.n.toFixed(3)),a.mean[metric].toFixed(4),a.fit[metric].toFixed(4),fmt(a.rz[metric],1),'20']));
table(document.getElementById('tbl2'),['estimate','value','interval','level'],E.pred.concat(E.rows).map(r=>[r.lab,fmt(r.g,4),'['+fmt(r.ci[0],4)+', '+fmt(r.ci[1],4)+']',r.lvl]));
document.getElementById('tbl2').style.marginTop='10px';}
seg(document.getElementById('cm'),[['survival_rate','survival rate'],['completion','completion']],metric,v=>{metric=v;render();});
render();
"""


def main():
    arms, est, med = load()
    print(static(arms, est, med).name)
    data = dict(
        arms={
            a: {k: v[k] for k in ("m", "p", "n", "fam", "seeds", "mean", "fit", "rz")}
            for a, v in arms.items()
        },
        est=est,
        med=med,
        ref={k: list(v) for k, v in REF.items()},
    )
    print(
        C.write_html(
            "fig10_secondary.html", "Secondary dose design", BODY, data, SCRIPT
        ).name
    )
    for met in METRICS:
        for r in est[met]["pred"] + est[met]["rows"]:
            print(
                f"  {met:13s} {r['lab']:45s} {C.fmt(r['g'])} {C.ci_text(*r['ci'])} {r['lvl']}"
                + (f" floor={r['floor']:.4f}" if r.get("floor") else "")
            )
        print(
            "  knee", est[met]["knee"], "floor_p500", round(est[met]["floor_p500"], 4)
        )
    print(med)


if __name__ == "__main__":
    main()
