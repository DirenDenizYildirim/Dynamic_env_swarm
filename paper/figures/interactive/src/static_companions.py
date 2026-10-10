"""Static PNG companions for every interactive figure (the browser-printed PDF
shows these; GIFs and iframes do not print reliably).

Same data, same palette (common_web tokens, light theme), same stated numbers
(ledger rows only) as the HTML defaults. Written with
savefig(metadata={"Software": None}) and checked for PNG text chunks.

Run from the repo root:  OMP_NUM_THREADS=4 ... nice -n 15 uv run python \
    paper/figures/interactive/src/static_companions.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib import patches  # noqa: E402
from matplotlib.colors import to_rgb  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_composer  # noqa: E402
import build_coupling_a  # noqa: E402
import build_explorer  # noqa: E402
import build_floors  # noqa: E402
import build_gamma_t  # noqa: E402
import build_ladder  # noqa: E402
import build_severity  # noqa: E402
import build_simplex  # noqa: E402
from common_web import OUT_DATA, OUT_IMG, TOKENS_LIGHT as T, savefig  # noqa: E402

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": T["axis"],
    "axes.labelcolor": T["ink2"], "xtick.color": T["muted"], "ytick.color": T["muted"],
    "axes.spines.top": False, "axes.spines.right": False, "figure.facecolor": T["surface"],
    "axes.facecolor": T["surface"], "text.color": T["ink"],
})
MINUS = "−"


def chip(ax, x, y, text, kind="line", fs=7.5, transform=None, ha="left"):
    fc = {"fill": T["ink"], "line": T["surface"], "weak": T["band"]}[kind]
    tc = T["surface"] if kind == "fill" else T["ink"]
    ax.text(x, y, text, fontsize=fs, fontweight="bold", color=tc, ha=ha, va="center",
            transform=transform or ax.transAxes,
            bbox=dict(boxstyle="round,pad=0.28,rounding_size=0.6", fc=fc, ec=T["ink"], lw=0.8,
                      ls=":" if kind == "weak" else "-"))


# --------------------------------------------------------------------------- F1
def _rgb(h):
    return np.array(to_rgb(T[h]))


HZ = np.stack([_rgb("fuel"), _rgb("burning"), _rgb("burnt")])
INK, WHITE = _rgb("map_ink"), _rgb("map_white")


def compose(hz, sm, weak, coll, food, S=8):
    """RGB raster of a cell grid with the explorer's (= the restyled GIFs') rules."""
    up = lambda a: np.repeat(np.repeat(a, S, 0), S, 1)  # noqa: E731
    img = up(HZ[hz])
    nh, nw = img.shape[:2]
    yy, xx = np.indices((nh, nw))
    py, px = yy % S, xx % S
    g = max(1, S // 8)
    grid = (py >= S - g) | (px >= S - g)
    img[grid] = img[grid] * 0.84 + _rgb("map_gridline") * 0.16
    alpha = up(np.round(np.asarray(sm, float) * 15) / 15 * 0.9)
    hatch = ((xx + yy) % max(2, S // 2) < g) & ~grid & (alpha > 0)
    a = alpha[hatch][:, None]
    img[hatch] = img[hatch] * (1 - a) + _rgb("smoke_hatch") * a
    dotc = np.stack([HZ[0] * 0.5 + INK * 0.5, HZ[1] * 0.5 + INK * 0.5, HZ[2] * 0.5 + WHITE * 0.5])
    lo, hi = 3 * S // 8, 3 * S // 8 + max(1, S // 4)
    dot = (py >= lo) & (py < hi) & (px >= lo) & (px < hi)
    m = dot & up(np.asarray(weak, bool) & ~np.asarray(coll, bool))
    img[m] = up(dotc[hz])[m]
    inner = (py <= S - 1 - g) & (px <= S - 1 - g)
    e = S - 1 - g
    void = inner & ((py < g) | (py > e - g) | (px < g) | (px > e - g) | (np.abs(py - px) < g) | (np.abs(py + px - e) < g))
    voidc = np.stack([INK, INK, WHITE])
    m = void & up(np.asarray(coll, bool))
    img[m] = up(voidc[hz])[m]
    fd = up(np.asarray(food, bool))
    f_in = (py >= g) & (py <= S - 1 - 2 * g) & (px >= g) & (px <= S - 1 - 2 * g)
    img[fd & inner & ~f_in] = INK
    img[fd & f_in] = _rgb("food")
    return img


def stamp_agent(img, r, c, S, alive, scale=1.0):
    cy, cx = (r + 0.5) * S - 0.5, (c + 0.5) * S - 0.5
    h, w = img.shape[:2]
    y0, y1, x0, x1 = int(max(0, cy - S)), int(min(h, cy + S + 1)), int(max(0, cx - S)), int(min(w, cx + S + 1))
    yy, xx = np.indices((y1 - y0, x1 - x0))
    d = np.hypot(yy + y0 - cy, xx + x0 - cx) / (S * scale)
    win = img[y0:y1, x0:x1]
    if alive:
        win[d <= 0.82] = INK
        win[d <= 0.70] = WHITE
        win[d <= 0.56] = _rgb("agent")
    else:
        ringm = lambda a, b: (d > a) & (d <= b)  # noqa: E731
        win[ringm(0.70, 0.82)] = WHITE
        win[ringm(0.45, 0.70)] = INK
        win[ringm(0.325, 0.45)] = WHITE


def draw_map(ax, d, t, agent, S=8):
    hz, sm, food = d["hazard"][t], d["smoke"][t], d["food"][t]
    coll = d["structure"][t].astype(bool)
    L = hz.shape[0]
    img = compose(hz, sm, d["weak"], coll, food, S)
    pos, alive = d["pos"][t], d["alive"][t]
    for (r, c), al in sorted(zip(pos.tolist(), alive.tolist()), key=lambda z: z[1]):
        stamp_agent(img, r, c, S, al)
    ax.imshow(img, interpolation="nearest", extent=(-0.5, L - 0.5, L - 0.5, -0.5))
    seeded = d["seeded"]
    past = seeded[:t].any(0)
    for mask, rad, lw in ((past, 0.42, 0.9), (seeded[t], 1.35, 1.8)):
        for r, c in zip(*np.nonzero(mask)):
            ax.add_patch(patches.Circle((c, r), rad, fill=False, ec=T["map_white"], lw=lw + 1.6, zorder=5))
            ax.add_patch(patches.Circle((c, r), rad, fill=False, ec=T["map_A"], lw=lw, zorder=6))
    if agent is not None and agent >= 0:
        p = pos[agent]
        ax.add_patch(patches.Rectangle((p[1] - 4.5, p[0] - 4.5), 9, 9, fill=False, ec=T["map_white"], lw=2.6, zorder=6))
        ax.add_patch(patches.Rectangle((p[1] - 4.5, p[0] - 4.5), 9, 9, fill=False, ec=T["map_ink"], lw=1.2, zorder=7))
        ax.add_patch(patches.Circle((p[1], p[0]), 1.25, fill=False, ec=T["map_ink"], lw=1.1, zorder=7))
    ax.set_xlim(-0.5, L - 0.5)
    ax.set_ylim(L - 0.5, -0.5)
    ax.set_xticks([])
    ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(True)
        sp.set_color(T["muted"])


def draw_panel(ax, d, t, a, which, S=24):
    K, R = 9, 4
    L = d["hazard"].shape[1]
    p = d["pos"][t, a]
    rr, cc = np.meshgrid(np.arange(K) + p[0] - R, np.arange(K) + p[1] - R, indexing="ij")
    inside = (rr >= 0) & (rr < L) & (cc >= 0) & (cc < L)
    r0, c0 = np.clip(rr, 0, L - 1), np.clip(cc, 0, L - 1)
    hz = np.where(inside, d["hazard"][t][r0, c0], 0)
    sm = np.where(inside, d["smoke"][t][r0, c0], 0)
    wk = inside & d["weak"][r0, c0]
    co = inside & d["structure"][t].astype(bool)[r0, c0]
    fd = inside & d["food"][t].astype(bool)[r0, c0]
    rev, tau = d["reveal"][t, a], d["tau"][t, a]
    up = lambda x: np.repeat(np.repeat(x, S, 0), S, 1)  # noqa: E731
    if which == "tau":
        u = 1 - tau.astype(float)
        img = _rgb("map_bg")[None, None] * (1 - u[..., None]) + _rgb("tau_end")[None, None] * u[..., None]
        img = up(img)
        yy, xx = np.indices(img.shape[:2])
        gl = ((yy % S) == S - 1) | ((xx % S) == S - 1)
        img[gl] = _rgb("map_grid")
    else:
        img = compose(hz, sm, wk, co, fd, S)
        occ = {}  # observation: alive occupancy only (plane 6); state: alive and dead agents
        for (r, c), al in zip(d["pos"][t].tolist(), d["alive"][t].tolist()):
            if al:
                occ[(r, c)] = True
            elif which == "state":
                occ.setdefault((r, c), False)
        for (r, c), al in occ.items():
            dr, dc = r - p[0] + R, c - p[1] + R
            if 0 <= dr < K and 0 <= dc < K:
                cy, cx = (dr + 0.5) * S - 0.5, (dc + 0.5) * S - 0.5
                yy, xx = np.indices(img.shape[:2])
                dd = np.hypot(yy - cy, xx - cx) / (S * 0.55)
                if al:
                    img[dd <= 0.82] = INK
                    img[dd <= 0.70] = WHITE
                    img[dd <= 0.56] = _rgb("agent")
                else:
                    img[(dd > 0.70) & (dd <= 0.82)] = WHITE
                    img[(dd > 0.45) & (dd <= 0.70)] = INK
                    img[(dd > 0.325) & (dd <= 0.45)] = WHITE
        out = up(~inside)
        if which == "state":
            img[out] = _rgb("outside")
        else:
            img[out] = compose(np.zeros((K, K), int), np.zeros((K, K)), np.zeros((K, K), bool),
                               np.zeros((K, K), bool), np.zeros((K, K), bool), S)[out]
            img[up(~rev)] = _rgb("unseen")
    ax.imshow(img, interpolation="nearest", extent=(-0.5, K - 0.5, K - 0.5, -0.5))
    if which == "obs":
        for r, c in zip(*np.nonzero(~rev)):
            ax.text(c, r + 0.03, "?", ha="center", va="center", fontsize=7.5, fontweight="bold", color=T["unseen_mark"])
    ax.add_patch(patches.Rectangle((R - 0.5, R - 0.5), 1, 1, fill=False, ec=T["map_ink"], lw=1.6, zorder=6))
    ax.set_xticks([])
    ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(True)
        sp.set_color(T["map_axis"])


def explorer_static(stem: str, label: str):
    d = np.load(OUT_DATA / f"{stem}_frames.npz")
    a = build_explorer.default_agent(d["alive"], d["reveal"])
    fig = plt.figure(figsize=(9.2, 6.9))
    gs = fig.add_gridspec(3, 3, height_ratios=[1.0, 0.62, 0.17], hspace=0.3, wspace=0.08,
                          left=0.03, right=0.97, top=0.87, bottom=0.02)
    fig.text(0.03, 0.968, label, fontsize=10.5, fontweight="bold", va="center")
    fig.text(0.03, 0.937, build_explorer.SUB, fontsize=8, color=T["ink2"], va="center")
    for i, t in enumerate((0, 128, 256)):
        ax = fig.add_subplot(gs[0, i])
        draw_map(ax, d, t, a if t == 128 else None)
        ax.set_title(f"t = {t} / 256" + (f" · agent {a + 1} selected" if t == 128 else ""), fontsize=8.5, loc="left")
    for j, (which, title) in enumerate((("obs", "observation, as produced (obs v3)"),
                                         ("state", "state, same 9 × 9 cells"),
                                         ("tau", "P(seen) = τ, Beer–Lambert transmittance"))):
        ax = fig.add_subplot(gs[1, j])
        draw_panel(ax, d, 128, a, which)
        ax.set_title(f"agent {a + 1}, t = 128\n{title}", fontsize=7.5, loc="left")
    lax = fig.add_subplot(gs[2, :])
    lax.axis("off")
    lax.set_xlim(0, 1)
    lax.set_ylim(0, 1)
    items = [("fuel", dict(hz=0)), ("burning", dict(hz=1, sm=1.0)), ("burnt", dict(hz=2)),
             ("smoke density ρ (environment field)", dict(hz=2, sm=1.0)), ("weak floor", dict(wk=True)),
             ("collapsed floor", dict(co=True)), ("food item", dict(fd=True)), ("agent", "alive"),
             ("agent, dead", "dead"), ("collapse-seeded ignition (Coupling A)", "seed"),
             ("unseen (masked), observation only", "unseen"), ("τ: 1 (white) to 0 (dark)", "tau")]
    cols, w = 4, 0.25
    for k, (txt, kw) in enumerate(items):
        x, y = (k % cols) * w, 0.82 - (k // cols) * 0.33
        ext = (x + 0.005, x + 0.02, y - 0.12, y + 0.12)
        if isinstance(kw, dict):
            cell = compose(np.full((1, 1), kw.get("hz", 0)), np.full((1, 1), kw.get("sm", 0.0)),
                           np.full((1, 1), kw.get("wk", False)), np.full((1, 1), kw.get("co", False)),
                           np.full((1, 1), kw.get("fd", False)), 24)
            lax.imshow(cell, extent=ext, interpolation="nearest", aspect="auto")
        elif kw in ("alive", "dead"):
            tmp = np.tile(_rgb("fuel")[None, None], (24, 24, 1))
            stamp_agent(tmp, 0, 0, 24, kw == "alive", scale=0.55)
            lax.imshow(tmp, extent=ext, interpolation="nearest", aspect="auto")
        elif kw == "seed":
            lax.add_patch(patches.Ellipse((x + 0.0125, y), 0.012, 0.2, fill=False, ec=T["map_A"], lw=1.6))
        elif kw == "unseen":
            lax.add_patch(patches.Rectangle((ext[0], ext[2]), 0.015, 0.24, fc=T["unseen"], lw=0))
            lax.text(x + 0.0125, y, "?", fontsize=6.5, fontweight="bold", ha="center", va="center", color=T["unseen_mark"])
        elif kw == "tau":
            ramp = np.linspace(0, 1, 32)[None, :, None]
            img = _rgb("map_bg")[None, None] * (1 - ramp) + _rgb("tau_end")[None, None] * ramp
            lax.imshow(img, extent=(x + 0.005, x + 0.04, y - 0.1, y + 0.1), aspect="auto")
        lax.text(x + (0.047 if kw == "tau" else 0.027), y, txt, fontsize=7, va="center")
    lax.set_xlim(0, 1)
    lax.set_ylim(0, 1)
    out = OUT_IMG / f"explorer_{stem}_static.png"
    savefig(fig, out, dpi=170)
    plt.close(fig)
    return out, a


# --------------------------------------------------------------------------- F2
SHAPES = {"dot": ("o", True), "ring": ("o", False), "tri": ("^", True), "diamond": ("D", True), "square": ("s", True)}


def ladder_static():
    data = build_ladder.build_data()
    rows = data["rows"]
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 7.4))
    fig.subplots_adjust(left=0.02, right=0.98, top=0.9, bottom=0.17, wspace=0.08)
    fig.text(0.02, 0.965, "registered readings at θ*, matched budget T* = 1000 · intervals: Šidák 95 % (m = 2), "
             "conditional on the common eval draw · all four rungs shown", fontsize=8, color=T["ink2"])
    for ax, mt in zip(axes, data["metrics"]):
        lo, hi = mt["dom"]
        ax.set_xlim(lo, hi)
        ys, yacc = [], 0.0
        for r in rows:
            yacc += 1.1 if r.get("family") and yacc > 0 else 0.0
            ys.append(yacc)
            yacc += 3.5 + (0.9 if r["id"] == "G4" else 0.0)
        ax.set_ylim(yacc + 0.2, -0.9)
        ax.set_yticks([])
        ax.spines["left"].set_visible(False)
        ax.axvline(0, color=T["muted"], lw=0.8, zorder=1)
        ax.grid(axis="x", color=T["grid"], lw=0.6)
        ax.set_axisbelow(True)
        ax.set_xlabel(mt["axis"], fontsize=8.5)
        ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(
            lambda v, _: "0" if abs(v) < 1e-12 else ("+" if v > 0 else MINUS) + f"{abs(v):.{2 if mt['k'] == 'completion' else 3}f}"))
        ax.set_title(mt["name"], loc="left", fontsize=11, fontweight="bold")
        for i, r in enumerate(rows):
            y0 = ys[i]
            d = r["m"][mt["k"]]
            tr = matplotlib.transforms.blended_transform_factory(ax.transAxes, ax.transData)
            if r.get("family"):
                ax.text(0.0, y0 - 0.55, r["family"], fontsize=7, style="italic", color=T["muted"], transform=tr)
                if i:
                    ax.axhline(y0 - 1.05, color=T["axis"], lw=0.6)
            ax.text(0.0, y0 + 0.15, f"{r['sym']}  {r['contrast']}", fontsize=8.5, fontweight="bold", transform=tr)
            ax.text(0.0, y0 + 0.75, f"{r['k']} · {r['unit']}" + (f" · {r['date']}" if r["date"] else ""),
                    fontsize=6.6, color=T["ink2"], transform=tr)
            x = 0.0
            for c in r.get("chips", []):
                chip(ax, x, y0 + 1.45, c, "weak", fs=6.6, transform=tr)
                x += 0.2
            if not r.get("noverdict"):
                chip(ax, x, y0 + 1.45, "REJECT" if d["reject"] else "null", "fill" if d["reject"] else "line", fs=6.6, transform=tr)
                x += 0.12 if not d["reject"] else 0.14
            ax.text(x, y0 + 1.45, (d["est"] or "") + ("  " + d["ci"] if d["ci"] else ""), fontsize=7.5, va="center",
                    transform=tr)
            yb = y0 + 2.3
            if d["band"]:
                ax.add_patch(patches.Rectangle((-d["X"], yb - 0.35), 2 * d["X"], 0.7, fc=T["band"], lw=0, zorder=0))
            if d["floor"]:
                ax.add_patch(patches.Rectangle((-d["floor"], yb - 0.35), 2 * d["floor"], 0.7, fc="none",
                                               ec=T["muted"], lw=0, hatch="....", zorder=1))
            ax.plot([d["lo"], d["hi"]], [yb, yb], color=T["ink"], lw=1.8, zorder=3)
            for v in (d["lo"], d["hi"]):
                ax.plot([v, v], [yb - 0.22, yb + 0.22], color=T["ink"], lw=1.8, zorder=3)
            mk, filled = SHAPES[r["shape"]]
            ax.scatter([d["gamma"]], [yb], marker=mk, s=34, c=T["ink"] if filled else T["surface"],
                       edgecolors=T["ink"] if not filled else T["surface"], linewidths=1.3, zorder=4)
            if r["id"] == "G4":
                cq = data["consequence"][mt["k"]]
                if mt["k"] == "completion" and d["Xt"]:
                    cq += f", X₄ = {d['Xt']}"
                chip(ax, 0.0, y0 + 3.35, cq, "fill" if mt["k"] == "survival_rate" else "line", fs=6.6, transform=tr)
    leg = [patches.Patch(fc=T["band"], label="80 %-power MDE, ±X"),
           patches.Patch(fc="none", ec=T["muted"], hatch="....", lw=0, label="floor, ±1 sd(Γ) floor basis (Γ, k = 72 only)"),
           matplotlib.lines.Line2D([], [], color=T["ink"], marker="o", lw=1.8, label="estimate, Šidák 95 % CI")]
    fig.legend(handles=leg, loc="lower left", bbox_to_anchor=(0.02, 0.0), ncol=3, frameon=False, fontsize=7.5)
    fig.text(0.02, 0.05, data["foot"] + "   Markers: ● Γ · ○ Γ, k = 60 · ▲ Γ₄ · ◆ Γ₄′ · ■ B̂", fontsize=7, color=T["ink2"])
    out = OUT_IMG / "ladder_registered_readings.png"
    savefig(fig, out, dpi=180)
    plt.close(fig)
    return out


# --------------------------------------------------------------------------- F3
def hatch_fill(ax, x, y, w, h, kind):
    base = {"A": T["A"], "B": T["B"], "AB": T["A"], "F": T["fireonly"]}[kind]
    alpha = 1.0 if kind == "F" else 0.3
    ax.add_patch(patches.Rectangle((x, y), w, h, fc=base, alpha=alpha, lw=0))
    if kind in ("A", "AB"):
        ax.add_patch(patches.Rectangle((x, y), w, h, fc="none", ec=T["A"], hatch="////", lw=0))
    if kind in ("B", "AB"):
        ax.add_patch(patches.Rectangle((x, y), w, h, fc="none", ec=T["B"], hatch="\\\\\\\\", lw=0))


def composer_static():
    data = build_composer.build_data()
    from fractions import Fraction
    fig = plt.figure(figsize=(9.6, 3.6))
    ax = fig.add_axes([0.08, 0.2, 0.6, 0.66])
    mx = fig.add_axes([0.72, 0.2, 0.26, 0.6])
    fig.text(0.02, 0.95, "training mixtures, read from the committed configs · as certified: δ inert under a frozen "
             "random-projection encoder at this scale · the fire burns in every episode", fontsize=7.6, color=T["ink2"])
    names = {"A": "Coupling A only", "B": "Coupling B only", "AB": "A + B together", "F": "fire-only (δ-only; no active stressor)"}
    for i, arm in enumerate(data["arms"]):
        y = 2 - i
        x = 0.0
        order = ["A", "B", "AB", "F"]
        for typ in order:
            comps = sorted([c for c in arm["components"] if (("AB" if c["A"] and c["B"] else "A" if c["A"] else "B" if c["B"] else "F") == typ)],
                           key=lambda c: c["beta"])
            for c in comps:
                w = c["wf"]
                hatch_fill(ax, x + 0.003, y - 0.3, w - 0.006, 0.6, typ)
                ax.text(x + w / 2, y, f"{Fraction(c['w'])}\nβ {c['beta']:.2f}", ha="center", va="center", fontsize=7,
                        fontweight="bold", bbox=dict(fc=T["surface"], ec="none", pad=0.6, alpha=0.85))
                x += w
        ax.text(-0.02, y, arm["name"], ha="right", va="center", fontsize=10, fontweight="bold")
        v = arm["beh"]
        for k, (lab, val, kind) in enumerate((("A", v["mA"], "A"), ("B", v["mB"], "B"), ("active", v["active"], "ink"))):
            yy = y + 0.25 - k * 0.25
            mx.add_patch(patches.Rectangle((0, yy - 0.08), 1, 0.16, fc=T["band"], lw=0))
            f = float(Fraction(val))
            if kind == "ink":
                mx.add_patch(patches.Rectangle((0, yy - 0.08), f, 0.16, fc=T["ink"], lw=0))
            else:
                hatch_fill(mx, 0, yy - 0.08, f, 0.16, kind)
            mx.text(-0.04, yy, lab, ha="right", va="center", fontsize=7, color=T["ink2"])
            mx.text(1.04, yy, val, ha="left", va="center", fontsize=7.5, fontweight="bold")
        if arm["name"] == "JOINT":
            mx.text(0, y - 0.5, "per-stressor marginal: " + data["ratios"]["JOINT"], fontsize=7, color=T["ink2"])
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.6, 2.6)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.set_xticks([0, 1 / 3, 0.5, 2 / 3, 1])
    ax.set_xticklabels(["0", "1/3", "1/2", "2/3", "1"])
    ax.set_xlabel("share of training episodes, by episode type and training severity", fontsize=8)
    mx.set_xlim(-0.3, 1.25)
    mx.set_ylim(-0.75, 2.6)
    mx.axis("off")
    mx.set_title("per-stressor marginal, and the share\nwith an active stressor", fontsize=7.5, color=T["ink2"], loc="left")
    handles = []
    for typ in ("A", "B", "AB", "F"):
        p = patches.Patch(fc={"A": T["A"], "B": T["B"], "AB": T["A"], "F": T["fireonly"]}[typ],
                          alpha=1.0 if typ == "F" else 0.45,
                          hatch={"A": "////", "B": "\\\\\\\\", "AB": "xxxx", "F": None}[typ], label=names[typ])
        handles.append(p)
    fig.legend(handles=handles, loc="lower left", bbox_to_anchor=(0.06, 0.0), ncol=4, frameon=False, fontsize=7.2)
    out = OUT_IMG / "composer_training_mixtures.png"
    savefig(fig, out, dpi=180)
    plt.close(fig)
    return out


# --------------------------------------------------------------------------- F4
def gamma_t_static():
    data = build_gamma_t.build_data()
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.6))
    fig.subplots_adjust(left=0.08, right=0.98, top=0.74, bottom=0.2, wspace=0.22)
    fig.text(0.02, 0.965, "Γ(t) = JOINT − ISO at the 11 retained checkpoints, k = 72 per arm · Šidák 95 % (m = 2) · "
             "registered rule (iv): all 11 signs must agree", fontsize=8, color=T["ink2"])
    for ax, mt in zip(axes, data["metrics"]):
        ts = [p["t"] for p in mt["pts"]]
        ax.set_xlim(475, 1025)
        ax.set_ylim(*mt["dom"])
        ax.axhline(0, color=T["muted"], lw=0.8)
        ax.grid(axis="y", color=T["grid"], lw=0.6)
        ax.set_axisbelow(True)
        ax.add_patch(patches.Rectangle((1000 - 13, -mt["floor"]), 26, 2 * mt["floor"], fc="none", ec=T["muted"],
                                       hatch="....", lw=0))
        for p in mt["pts"]:
            ax.plot([p["t"], p["t"]], [p["lo"], p["hi"]], color=T["ink"], lw=1.6)
            for v in (p["lo"], p["hi"]):
                ax.plot([p["t"] - 5, p["t"] + 5], [v, v], color=T["ink"], lw=1.6)
            ax.scatter([p["t"]], [p["g"]], s=26, c=T["ink"], edgecolors=T["surface"], linewidths=1.2, zorder=4)
        ax.set_xticks([500, 600, 700, 800, 900, 1000])
        ax.set_xlabel("training update t", fontsize=8.5)
        ax.set_ylabel(f"Γ(t), Δ {mt['name']}", fontsize=8.5)
        ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(
            lambda v, _: "0" if abs(v) < 1e-12 else ("+" if v > 0 else MINUS) + f"{abs(v):.{2 if mt['k'] == 'completion' else 3}f}"))
        tr = matplotlib.transforms.blended_transform_factory(ax.transData, ax.transAxes)
        for p in mt["pts"]:
            ax.text(p["t"], 1.04, "+" if p["sign"] == "+" else MINUS, ha="center", va="center", fontsize=11,
                    fontweight="bold", transform=tr)
            if p["disagree"]:
                ax.scatter([p["t"]], [1.04], s=150, facecolors="none", edgecolors=T["ink"], linewidths=1.0,
                           transform=tr, clip_on=False)
        ax.text(462, 1.04, "sign", ha="right", va="center", fontsize=7.5, color=T["muted"], transform=tr)
        ax.text(0.0, 1.27, mt["name"], fontsize=10.5, fontweight="bold", va="center", transform=ax.transAxes)
        chip(ax, 0.0, 1.15, data["verdict"], "line", fs=7.5)
    fig.text(0.02, 0.055, "● Γ(t), Šidák 95 % CI · ◯ around a sign: differs from the sign at T* · dotted box at "
             "t = 1000: floor, ±1 sd(Γ) floor basis", fontsize=7, color=T["ink2"])
    fig.text(0.02, 0.02, "t = 1000: the grid card's own eval (the registered Γ); t < 1000: post-unblind card", fontsize=7,
             color=T["ink2"])
    out = OUT_IMG / "gamma_t_final_half.png"
    savefig(fig, out, dpi=180)
    plt.close(fig)
    return out


# --------------------------------------------------------------------------- F5
def simplex_static():
    data = build_simplex.build_data()
    mt = data["metrics"]["survival_rate"]
    fig = plt.figure(figsize=(10.4, 5.6))
    a1 = fig.add_axes([0.06, 0.12, 0.34, 0.74])
    a2 = fig.add_axes([0.47, 0.12, 0.51, 0.74])
    x = 0.02
    for txt, kind in (("secondary", "line"), ("non-verdict-bearing", "line"), ("95 %, not family-corrected", "line"),
                      ("knee: UNDERPOWERED", "weak"), ("mediation: VOID", "weak")):
        fig.text(x, 0.95, txt, fontsize=7.2, fontweight="bold", va="center",
                 bbox=dict(boxstyle="round,pad=0.28", fc=T["band"] if kind == "weak" else T["surface"], ec=T["ink"], lw=0.8,
                           ls=":" if kind == "weak" else "-"))
        x += 0.012 + 0.0068 * len(txt)
    tri = patches.Polygon([[0, 0], [1, 0], [0, 1]], closed=True, fc=T["band"], lw=0)
    a1.add_patch(tri)
    for q in data["isom"]:
        c = q["c"]
        pts = []
        if c <= 0 and -c <= 1:
            pts.append((0, -c))
        if 0 <= c <= 1:
            pts.append((c, 0))
        pp, nn = (1 + c) / 2, (1 - c) / 2
        if 0 <= pp <= 1 and 0 <= nn <= 1:
            pts.append((pp, nn))
        if len(pts) < 2 or pts[0] == pts[1]:
            continue
        a1.plot([pts[0][0], pts[-1][0]], [pts[0][1], pts[-1][1]], color=T["muted"], lw=0.7)
        a1.text(pts[-1][0] + 0.02, pts[-1][1] + (-0.05 if q["m"] == "0.5" else 0.01), f"m = {q['m']}", fontsize=7,
                color=T["muted"])
    a1.add_patch(patches.Polygon([[0, 0], [0.5, 0.5], [0.4, 0.6], [0, 0.2]], closed=True, fc=T["muted"], alpha=0.18,
                                 ec=T["muted"], lw=0.7))
    a1.text(0.13, 0.27, "sampled region", fontsize=7, color=T["ink2"])
    for arm in data["arms"]:
        if arm["kind"] == "sweep":
            a1.scatter([arm["p"]], [arm["n"]], s=26, c=T["ink"], edgecolors=T["surface"], linewidths=1.2, zorder=4)
        else:
            a1.scatter([arm["p"]], [arm["n"]], marker="s", s=24, c=T["surface"], edgecolors=T["ink"], linewidths=1.2, zorder=4)
    for ref, (dx, dy, ha) in zip(data["refs"], ((0.04, 0.0, "left"), (0.04, 0.04, "left"), (-0.03, 0.05, "right"))):
        a1.scatter([ref["p"]], [ref["n"]], s=110, facecolors="none", edgecolors=T["ink"], linewidths=1.5, zorder=5, clip_on=False)
        lab = {"ISO": "ISO", "JOINT": "JOINT, m = 1"}.get(ref["arm"], "ISO-4")
        a1.text(ref["p"] + dx, ref["n"] + dy, lab, fontsize=8.5, fontweight="bold", ha=ha, va="center")
    a1.set_xlim(-0.02, 1.05)
    a1.set_ylim(-0.02, 1.02)
    a1.set_xlabel("p, share of episodes with A + B together", fontsize=8.5)
    a1.set_ylabel("n, fire-only share", fontsize=8.5)
    a1.set_title("training mixtures in (p, n); single-stressor share 1 − p − n", fontsize=8.5, loc="left")
    rows = [("g", "secondary estimates, 95 %")] + [("r", r) for r in mt["sec"]] + \
           [("g", "plane prediction vs measured")] + [("r", r) for r in mt["pred"]]
    y = 0
    a2.set_xlim(*mt["dom"])
    a2.axvline(0, color=T["muted"], lw=0.8)
    a2.grid(axis="x", color=T["grid"], lw=0.6)
    a2.set_axisbelow(True)
    tr = matplotlib.transforms.blended_transform_factory(a2.transAxes, a2.transData)
    for kind, r in rows:
        if kind == "g":
            a2.text(0.0, y + 0.3, r, fontsize=7, style="italic", color=T["muted"], transform=tr)
            y += 0.9
            continue
        a2.text(0.0, y, r["label"] + (f"   {r['est']}" + (f" {r['ci']}" if r["ci"] else "") if r["est"] else ""),
                fontsize=7.3, transform=tr, va="center")
        yb = y + 0.55
        meas = r["kind"] == "meas"
        if r["lo"] is not None:
            a2.plot([r["lo"], r["hi"]], [yb, yb], color=T["ink"], lw=1.8 if meas else 0.9)
            if meas:
                for v in (r["lo"], r["hi"]):
                    a2.plot([v, v], [yb - 0.15, yb + 0.15], color=T["ink"], lw=1.8)
        mk = {"sec": ("o", False), "pred": ("D", False)}.get(r["kind"])
        if meas:
            mk = ({"g4": "^", "g4p": "D", "bh": "s"}[r["key"]], True)
        a2.scatter([r["g"]], [yb], marker=mk[0], s=30, c=T["ink"] if mk[1] else T["surface"],
                   edgecolors=T["ink"] if not mk[1] else T["surface"], linewidths=1.2, zorder=4)
        y += 1.45
    a2.set_ylim(y + 0.1, -0.4)
    a2.set_yticks([])
    a2.spines["left"].set_visible(False)
    a2.set_xlabel("Δ survival (fraction), or per unit p / n", fontsize=8.5)
    a2.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(
        lambda v, _: "0" if abs(v) < 1e-12 else ("+" if v > 0 else MINUS) + f"{abs(v):.2f}"))
    a2.set_title("survival: estimates", fontsize=8.5, loc="left")
    fig.text(0.02, 0.025, "● sweep arm (m = 0.5) · ■ identification arm (m = 0.4) · ○ secondary estimate, 95 % · "
             "◇ plane prediction · ▲◆■ measured contrast, Šidák 95 %", fontsize=7, color=T["ink2"])
    out = OUT_IMG / "simplex_secondary.png"
    savefig(fig, out, dpi=180)
    plt.close(fig)
    return out


# --------------------------------------------------------------------------- F6a
def severity_static():
    data = build_severity.build_data()
    fr = build_severity.load_frames()
    fig = plt.figure(figsize=(10.4, 4.3))
    ax = fig.add_axes([0.06, 0.14, 0.3, 0.7])
    fig.text(0.02, 0.95, "fire calibration: P_span = P(a centre ignition reaches the boundary), "
             "all-fuel grid, no agents · renders: illustrative · random policy · episode key 0 · t = 128 · "
             "severity configs (κ_A 0.06, κ_B 1.0, δ 0)",
             fontsize=7.6, color=T["ink2"])
    betas = np.array(data["betas"])
    o = np.argsort(betas)
    shades, mks = [T["muted"], T["ink2"], T["ink"]], ["o", "s", "^"]
    for cv, col, mk in zip(data["curves"], shades, mks):
        p, se = np.array(cv["p"])[o], np.array(cv["se"])[o]
        b = betas[o]
        keep = (b >= 0.3) & (b <= 0.8)
        ax.errorbar(b[keep], p[keep], yerr=se[keep], color=col, marker=mk, ms=3.2, lw=1.2, elinewidth=0.8,
                    mfc=T["surface"] if mk == "o" else col, label=f"L = {cv['L']}")
    for lv in data["levels"]:
        ax.axvline(lv["beta"], color=T["ink"], lw=1.0)
        ax.text(lv["beta"] + (-0.005 if lv["name"] == "Low" else 0.005), 1.04 if lv["name"] != "Medium" else 0.04,
                f"{lv['name']} {lv['beta']:.2f}", fontsize=7.5, ha="right" if lv["name"] == "Low" else "left")
    ax.axhline(0.5, color=T["muted"], lw=0.7)
    ax.plot([float(data["betac64"])], [-0.03], marker="^", color=T["ink"], ms=5, clip_on=False)
    ax.text(0.535, 0.36, f"▲ β_c(64) ≈ {data['betac64']}\n(P_span = ½, L = 64)", fontsize=7, color=T["ink2"])
    ax.set_xlim(0.3, 0.8)
    ax.set_ylim(-0.02, 1.02)
    ax.set_xlabel("β, per-neighbour ignition probability", fontsize=8.5)
    ax.set_ylabel("P_span, ±1 SE (binomial)", fontsize=8.5)
    ax.grid(axis="y", color=T["grid"], lw=0.6)
    ax.legend(frameon=False, fontsize=7.5, loc="center right")
    for i, lv in enumerate(data["levels"]):
        a = fig.add_axes([0.42 + i * 0.195, 0.2, 0.18, 0.64])
        hz, sm = fr[lv["name"]]["hazard"][128], fr[lv["name"]]["smoke"][128]
        L = hz.shape[0]
        a.imshow(compose(hz, sm, np.zeros_like(hz, bool), np.zeros_like(hz, bool), np.zeros_like(hz, bool), 8),
                 interpolation="nearest", extent=(-0.5, L - 0.5, L - 0.5, -0.5))
        a.set_xticks([])
        a.set_yticks([])
        a.set_title(f"{lv['name']} · β {lv['beta']:.2f}", fontsize=8.5, loc="left")
        a.text(0, -0.05, lv["txt"] + "\n(no agents)", fontsize=6.8, color=T["ink2"], transform=a.transAxes, va="top")
    out = OUT_IMG / "severity_explorer.png"
    savefig(fig, out, dpi=180)
    plt.close(fig)
    return out


# --------------------------------------------------------------------------- F6c
def floors_static():
    d = build_floors.build_data()
    fig, axs = plt.subplots(2, 2, figsize=(10.4, 7.0))
    fig.subplots_adjust(left=0.23, right=0.96, top=0.93, bottom=0.15, hspace=0.75, wspace=0.62)
    # per card
    ax = axs[0, 0]
    labels, vals, txts = [], [], []
    for m, key, tkey in (("completion", "completion", "ct"), ("survival rate", "survival", "st")):
        for r in d["card"]["runs"]:
            labels.append(f"{m} · {r['name']}")
            vals.append(r[key])
            txts.append(r[tkey])
    y = np.arange(len(vals))[::-1]
    ax.barh(y, vals, color=[T["muted"], T["ink"]] * 2, height=0.55)
    for yy, v, t in zip(y, vals, txts):
        ax.text(v + 0.0008, yy, t, va="center", fontsize=7.5, fontweight="bold")
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=7.2)
    ax.set_xlim(0, 0.05)
    ax.set_xlabel("rerun floor: sd over identical runs, same seed (Medium)", fontsize=7.8)
    ax.set_title("per card (and tree, and config)", loc="left", fontsize=9, fontweight="bold")
    ax.text(0, -0.36, "confound: " + d["card"]["confound"], transform=ax.transAxes, fontsize=6.6, va="top")
    # per artifact
    ax = axs[0, 1]
    for i, r in enumerate(d["artifact"]["rows"]):
        yy = 2 - i
        for k in range(r["n"]):
            ax.add_patch(patches.Rectangle((k * 1.2, yy - 0.35), 0.9, 0.7, fc=T["ink"] if k < r["diff"] else T["surface"],
                                           ec=T["ink"], lw=1.0))
        ax.text(-0.4, yy, r["name"], ha="right", va="center", fontsize=7.4)
        if r["text"]:
            ax.text(6.3, yy, r["text"].replace(": ", ":\n").replace(", in", ",\nin"), va="center", fontsize=6.3, color=T["ink2"])
    ax.set_xlim(-0.2, 12)
    ax.set_ylim(-0.7, 2.7)
    ax.axis("off")
    ax.set_title("per artifact (filled: field digests differed)", loc="left", fontsize=9, fontweight="bold")
    ax.text(0, -0.12, d["artifact"]["sub"], transform=ax.transAxes, fontsize=6.6, color=T["ink2"], va="top", wrap=True)
    # per run length
    ax = axs[1, 0]
    for i, a in enumerate(d["length"]["arms"]):
        for j, (vals_, lab) in enumerate(((a["v500"], "T = 500"), (a["v1000"], "T = 1000"))):
            x = i * 2.6 + j * 1.1
            v = np.sort(np.array(vals_))
            ax.scatter(x + np.where(np.arange(len(v)) % 2, 0.12, -0.12), v, s=16,
                       facecolors=T["ink"] if j else T["surface"], edgecolors=T["ink"], linewidths=1.0, zorder=3)
            ax.plot([x - 0.3, x + 0.3], [v.mean()] * 2, color=T["muted"], lw=1.4)
            ax.text(x, -0.13, lab, transform=matplotlib.transforms.blended_transform_factory(ax.transData, ax.transAxes),
                    ha="center", fontsize=7, color=T["muted"])
        ax.text(i * 2.6 + 0.55, -0.27, f"{a['name']} · floor growth {a['g']}",
                transform=matplotlib.transforms.blended_transform_factory(ax.transData, ax.transAxes), ha="center",
                fontsize=7.2, fontweight="bold")
    ax.set_xticks([])
    ax.set_xlim(-0.6, 4.3)
    ax.set_ylabel("completion, one dot per run", fontsize=7.8)
    ax.set_title("per run length (identical runs, same seed)", loc="left", fontsize=9, fontweight="bold")
    ax.grid(axis="y", color=T["grid"], lw=0.6)
    ax.text(0, -0.33, "confound: " + d["length"]["confound"], transform=ax.transAxes, fontsize=6.6, va="top")
    # the grid against its floor
    ax = axs[1, 1]
    rows = d["beat"]["rows"] + [dict(name="survival Γ / floor-basis sd(Γ)", v=d["beat"]["gamma"]["v"], t=d["beat"]["gamma"]["t"])]
    y = np.arange(len(rows))[::-1]
    ax.barh(y, [r["v"] for r in rows], color=[T["muted"]] * 4 + [T["ink"]], height=0.55)
    for yy, r in zip(y, rows):
        ax.text(r["v"] + 0.08, yy, r["t"], va="center", fontsize=7.5, fontweight="bold")
    ax.axvline(1, color=T["ink"], lw=0.8)
    ax.set_yticks(y)
    ax.set_yticklabels([r["name"] for r in rows], fontsize=7.2)
    ax.set_xlim(0, 6.4)
    ax.set_xlabel("ratio to the rerun floor (1× = the floor)", fontsize=7.8)
    ax.set_title("the grid against its floor (k = 72 per arm)", loc="left", fontsize=9, fontweight="bold")
    out = OUT_IMG / "floors_explorer.png"
    savefig(fig, out, dpi=180)
    plt.close(fig)
    return out


# --------------------------------------------------------------------------- F6b
def coupling_a_static():
    d = build_coupling_a.build_data()
    fig, axs = plt.subplots(2, 2, figsize=(10.4, 6.6))
    fig.subplots_adjust(left=0.08, right=0.97, top=0.88, bottom=0.1, hspace=0.6, wspace=0.28)
    fig.text(0.02, 0.965, "Coupling A: structural collapse seeds fire · trained policies, single-configuration runs "
             "(Phases 3 and 4) · ranges: min–max over training seeds", fontsize=7.8, color=T["ink2"])
    xs = np.arange(3)
    ax = axs[0, 0]
    for j, sr in enumerate(d["seeded"]):
        off = -0.08 if j == 0 else 0.08
        for i, v in enumerate(sr["vals"]):
            ax.plot([i + off] * 2, [v["lo"], v["hi"]], color=T["ink"], lw=1.4)
        ax.scatter(xs + off, [v["mean"] for v in sr["vals"]], marker="o" if j == 0 else "s", s=30,
                   c=T["ink"] if j == 0 else T["surface"], edgecolors=T["ink"], linewidths=1.2, zorder=3,
                   label=f"{sr['series']} · Low / High {sr['fall']}")
    ax.set_xticks(xs)
    ax.set_xticklabels([f"{s['name']}\nβ {s['beta']:.2f}" for s in d["sev"]], fontsize=8)
    ax.set_ylim(0, 4.9)
    ax.set_ylabel("per episode", fontsize=8.5)
    ax.grid(axis="y", color=T["grid"], lw=0.6)
    ax.legend(frameon=False, fontsize=7.2, loc="upper right")
    ax.set_title("collapse-seeded ignitions per episode", loc="left", fontsize=9, fontweight="bold")
    ax = axs[0, 1]
    shares = d["shares"]
    lo, hi = min(x["mean"] for x in shares), max(x["mean"] for x in shares)
    ax.axhspan(lo, hi, color=T["band"], lw=0)
    ax.text(2.35, (lo + hi) / 2, d["share_range"] + "\nrange, 9 cells", fontsize=7.2, va="center")
    ser = ["m44, κ_B 1.0 arm", "m44, κ_B 0 arm", "m35, κ_A on arm"]
    mk = {0: ("o", T["ink"]), 1: ("o", T["surface"]), 2: ("s", T["surface"])}
    names = [s["name"] for s in d["sev"]]
    for j, sname in enumerate(ser):
        pts = [x for x in shares if x["series"] == sname]
        for x in pts:
            i = names.index(x["sev"]) + (j - 1) * 0.12
            ax.plot([i, i], [x["lo"], x["hi"]], color=T["muted"], lw=1.1)
        ax.scatter([names.index(x["sev"]) + (j - 1) * 0.12 for x in pts], [x["mean"] for x in pts], marker=mk[j][0], s=26,
                   c=mk[j][1], edgecolors=T["ink"], linewidths=1.1, zorder=3, label=sname)
    ax.set_xticks(xs)
    ax.set_xticklabels(names, fontsize=8)
    ax.set_xlim(-0.5, 2.9)
    ax.set_ylim(0.10, 0.25)
    ax.set_ylabel("share", fontsize=8.5)
    ax.grid(axis="y", color=T["grid"], lw=0.6)
    ax.legend(frameon=False, fontsize=7, loc="upper left", ncol=3)
    ax.set_title("share of seeded ignitions inside an alive agent's 9 × 9 crop", loc="left", fontsize=9, fontweight="bold")
    ax = axs[1, 0]
    p = d["prop3"]
    ax.errorbar(p["x"], p["y"], yerr=p["se"], fmt="o", color=T["ink"], ms=4, elinewidth=1.2)
    xe = min(11, 500 / p["slope"])
    ax.plot([0, xe], [0, p["slope"] * xe], color=T["ink2"], lw=1.1)
    ax.text(0.4, 470, f"committed through-origin fit, R² {p['r2']}", fontsize=7.8)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 510)
    ax.set_xlabel("E[N_seeds], collapse-seeded ignitions per run", fontsize=8)
    ax.set_ylabel("E[B_T], burnt cells at the horizon", fontsize=8)
    ax.grid(color=T["grid"], lw=0.6)
    ax.set_title("Prop. 3 linearity, run 1 of 2", loc="left", fontsize=9, fontweight="bold", pad=16)
    ax.text(0, 1.02, p["note"], transform=ax.transAxes, fontsize=6.8, color=T["ink2"])
    ax = axs[1, 1]
    ax.axis("off")
    ax.set_title("Prop. 3 matched-reference handshake, run 2 of 2", loc="left", fontsize=9, fontweight="bold")
    ax.add_patch(patches.FancyBboxPatch((0.0, 0.45), 1.0, 0.5, boxstyle="round,pad=0.02", fc=T["surface"], ec=T["axis"],
                                        transform=ax.transAxes))
    for k, line in enumerate(d["handshake"]["lines"]):
        ax.text(0.04, 0.86 - k * 0.11, line, fontsize=8 if k < 2 else 7.2, fontweight="bold" if k < 2 else None,
                color=T["ink"] if k < 2 else T["ink2"], transform=ax.transAxes)
    out = OUT_IMG / "coupling_a_explorer.png"
    savefig(fig, out, dpi=180)
    plt.close(fig)
    return out


def main():
    outs = []
    for stem, label in build_explorer.EPISODES.items():
        out, a = explorer_static(stem, label)
        outs.append(out)
        print(out.name, "agent", a + 1)
    outs += [ladder_static(), composer_static(), gamma_t_static(), simplex_static(), severity_static(), floors_static(), coupling_a_static()]
    for o in outs:
        print(f"{o.name}: {o.stat().st_size / 1e3:.0f} KB")


if __name__ == "__main__":
    main()
