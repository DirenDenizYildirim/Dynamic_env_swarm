"""Figure 1 (slot): the environment schematic. One step of the CHE in the
Prop.-1 kernel order (CLAUDE.md invariant #2; `che/env/env.py:1-9`):

  1. collapse  c' ~ T_C(c, x)          reads pre-step occupancy (agent load)
  2. hazard    h' ~ T_H(h, c, c')      CA spread, then Coupling A seeds from c' − c
  3. smoke     ρ' = e^{−η} ρ + σ_s·1[h' burning]
  4. agents    x' ~ T_X(x, a, h', c')  kills/blocking against h', c' (as implemented)
  5. comms     k' ~ T_K(x')            δ; no hazard input (Def. 7)
  observation  o' ~ O_{κ_B}(· | x', h', ρ', c', k')   Coupling B: Beer–Lambert on ρ'

No data; the labels are the theory doc's notation (Def. 1, 5, 6, 7) and the
step order of `env.py`. Outputs: out/img/fig01_schematic.svg and .png.
"""

from __future__ import annotations

import re

import common as C
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

W, H = 10.4, 4.2


def box(ax, x, y, w, h, title, body, num=None, fc=C.SURFACE, ec=C.INK, lw=1.1):
    ax.add_patch(
        FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0,rounding_size=0.08",
            fc=fc,
            ec=ec,
            lw=lw,
            zorder=2,
        )
    )
    if num is not None:
        ax.add_patch(
            plt.Circle((x + 0.2, y + h - 0.2), 0.13, fc=C.INK, ec="none", zorder=3)
        )
        ax.text(
            x + 0.2,
            y + h - 0.2,
            str(num),
            color=C.SURFACE,
            fontsize=7.5,
            ha="center",
            va="center",
            weight="bold",
            zorder=4,
        )
    ax.text(
        x + (0.4 if num is not None else 0.12),
        y + h - 0.2,
        title,
        fontsize=8.6,
        weight="bold",
        va="center",
        ha="left",
        color=C.INK,
        zorder=4,
    )
    ax.text(
        x + w / 2,
        y + h / 2 - 0.12,
        body,
        fontsize=8.4,
        ha="center",
        va="center",
        color=C.INK,
        zorder=4,
    )


def arrow(ax, p, q, color=C.INK2, lw=1.2, style="-|>", rad=0.0, ms=9, z=1.5):
    ax.add_patch(
        FancyArrowPatch(
            p,
            q,
            arrowstyle=style,
            mutation_scale=ms,
            color=color,
            lw=lw,
            connectionstyle=f"arc3,rad={rad}",
            zorder=z,
            shrinkA=0,
            shrinkB=0,
        )
    )


def build():
    C.mpl_setup()
    fig = plt.figure(figsize=(W, H))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.axis("off")

    bw, bh, y0, gap = 1.52, 1.0, 2.25, 0.27
    xs = [0.95 + i * (bw + gap) for i in range(5)]
    # state at t
    box(
        ax,
        0.08,
        y0 + 0.05,
        0.62,
        bh - 0.1,
        "",
        r"$s_t$" + "\n" + r"$(x, h, \rho, c, k)$",
        fc=C.BAND,
        ec=C.AXIS,
    )
    arrow(ax, (0.70, y0 + bh / 2), (xs[0], y0 + bh / 2))
    specs = [
        (
            "collapse",
            r"$c' \sim T_C(c,\, x)$" + "\n" + "agent load raises\ncollapse probability",
        ),
        ("hazard", r"$h' \sim T_H(h,\, c,\, c')$" + "\n" + r"fire CA, $\beta$"),
        (
            "smoke",
            r"$\rho' = e^{-\eta}\rho$"
            + "\n"
            + r"$+\ \sigma_s\,\mathbf{1}[h'\ \mathrm{burning}]$",
        ),
        (
            "agents",
            r"$x' \sim T_X(x,\, a,\, h',\, c')$"
            + "\n"
            + "fire and collapse kill,\ncollapse blocks",
        ),
        ("comms", r"$k' \sim T_K(x')$" + "\n" + r"link denial $\delta$"),
    ]
    for i, (t, b) in enumerate(specs):
        box(ax, xs[i], y0, bw, bh, t, b, num=i + 1)
    for i in range(1, 4):
        arrow(ax, (xs[i] + bw, y0 + bh / 2), (xs[i + 1], y0 + bh / 2))
    # Coupling A: the collapse increment seeds the hazard
    mid = (xs[0] + bw + xs[1]) / 2
    arrow(
        ax,
        (xs[0] + bw, y0 + bh / 2),
        (xs[1], y0 + bh / 2),
        color=C.S2,
        lw=2.6,
        ms=13,
        z=3,
    )
    ax.text(
        mid,
        y0 + bh + 0.42,
        "Coupling A",
        fontsize=8.6,
        weight="bold",
        ha="center",
        color=C.INK,
    )
    ax.text(
        mid,
        y0 + bh + 0.18,
        r"$c' - c$ seeds ignitions, $\kappa_A$",
        fontsize=7.8,
        ha="center",
        color=C.INK,
    )
    ax.plot(
        [mid, mid], [y0 + bh + 0.1, y0 + bh / 2 + 0.08], color=C.S2, lw=1.0, zorder=2.5
    )
    # actions enter the agents kernel
    ax.text(
        xs[3] + bw / 2,
        y0 + bh + 0.42,
        "actions a",
        fontsize=8.6,
        weight="bold",
        ha="center",
        color=C.INK,
    )
    arrow(
        ax,
        (xs[3] + bw / 2, y0 + bh + 0.35),
        (xs[3] + bw / 2, y0 + bh),
        color=C.INK,
        lw=1.2,
    )
    # delta: independent of the hazard
    ax.text(
        xs[4] + bw / 2,
        y0 + bh + 0.42,
        "comms denial δ",
        fontsize=8.6,
        weight="bold",
        ha="center",
        color=C.INK,
    )
    ax.text(
        xs[4] + bw / 2,
        y0 + bh + 0.18,
        "independent: no hazard input",
        fontsize=7.8,
        ha="center",
        color=C.INK,
    )
    arrow(
        ax,
        (xs[4] + bw / 2, y0 + bh + 0.1),
        (xs[4] + bw / 2, y0 + bh),
        color=C.INK,
        lw=1.2,
        ms=8,
        z=3,
    )
    # post-step state, then the observation drawn from it
    sx = xs[4] + bw + 0.42
    arrow(ax, (xs[4] + bw, y0 + bh / 2), (sx - 0.12, y0 + bh / 2))
    ax.text(
        sx, y0 + bh / 2, r"$s'$", fontsize=10, va="center", ha="center", color=C.INK
    )
    ob_x, ob_y, ob_h = xs[2], 0.3, 0.82
    ob_w = sx + 0.3 - ob_x
    box(
        ax,
        ob_x,
        ob_y,
        ob_w,
        ob_h,
        "observation, drawn from the post-step state",
        r"$o'_i \sim O^{\,i}_{\kappa_B}(\,\cdot \mid x',\, h',\, \rho',\, c',\, k')$"
        + ",  9 × 9 egocentric crop",
    )
    arrow(ax, (sx, y0 + bh / 2 - 0.2), (sx, ob_y + ob_h), color=C.INK2)
    # Coupling B: smoke attenuates perception
    cbx = xs[2] + bw / 2
    arrow(ax, (cbx, y0), (cbx, ob_y + ob_h), color=C.S1, lw=2.6, ms=13, z=3)
    ax.text(
        cbx - 0.14,
        (y0 + ob_y + ob_h) / 2 + 0.14,
        "Coupling B",
        fontsize=8.6,
        weight="bold",
        ha="right",
        color=C.INK,
    )
    ax.text(
        cbx - 0.14,
        (y0 + ob_y + ob_h) / 2 - 0.1,
        r"Beer–Lambert on $\rho'$, $\kappa_B$",
        fontsize=7.8,
        ha="right",
        color=C.INK,
    )
    ax.text(
        0.1,
        H - 0.14,
        "one environment step: kernels in sampling order (Prop. 1)",
        fontsize=8,
        color=C.INK2,
        va="top",
    )
    return fig


def strip_svg(p):
    s = p.read_text()
    s = re.sub(r"<!-- Created with matplotlib.*?-->\n?", "", s)
    s = re.sub(r"<metadata>.*?</metadata>\n?", "", s, flags=re.S)
    s = re.sub(r"<!DOCTYPE svg.*?>\n?", "", s, flags=re.S)
    p.write_text(s)


def main():
    fig = build()
    svg = C.IMG / "fig01_schematic.svg"
    fig.savefig(
        svg, metadata={"Creator": None, "Date": None, "Format": None, "Type": None}
    )
    strip_svg(svg)
    print(C.save_png(fig, "fig01_schematic.png").name, svg.name)


if __name__ == "__main__":
    main()
