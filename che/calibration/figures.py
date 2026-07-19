"""M2.2 report figures (P_span sigmoids, chi-hat, front speed).

House chart style (see che/scripts/plot_learning_curve.py): validated
categorical palette in fixed slot order — one color per grid size, the same
in every figure — thin marks, recessive axes/grid, direct labels + legend.
"""

from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

# Fixed slot order (dataviz reference): L=32 blue, L=48 green, L=64 magenta.
L_COLORS = {32: "#2a78d6", 48: "#008300", 64: "#e87ba4"}
INK = "#3d3d3a"
MUTED = "#8a8a85"


def _style(ax):
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color(MUTED)
    ax.tick_params(colors=MUTED)
    ax.grid(axis="y", color=MUTED, alpha=0.25, lw=0.5)


def _sizes(arrays: dict) -> list[int]:
    return [int(s) for s in arrays["sizes"]]


def plot_p_span(arrays: dict, summary: dict, out: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 4.2), dpi=150)
    betas = arrays["betas"]
    for size in _sizes(arrays):
        p = arrays[f"p_span_L{size}"]
        se = arrays[f"p_span_se_L{size}"]
        c = L_COLORS[size]
        ax.fill_between(betas, p - 2 * se, p + 2 * se, color=c, alpha=0.15,
                        lw=0)
        ax.plot(betas, p, color=c, lw=2, label=f"L = {size}")
    bc = summary["beta_c_half_locus_L_pow_-3/4"]
    ax.axvline(bc, color=MUTED, lw=1.5, ls=(0, (4, 3)))
    ax.annotate(
        f"$\\hat\\beta_c$ = {bc:.3f} (½-locus, $L^{{-3/4}}$ extrapolation)",
        xy=(bc, 0.03), xytext=(6, 0), textcoords="offset points",
        color=MUTED, fontsize=9,
    )
    ax.set_xlabel("spread probability $\\beta$", color=INK)
    ax.set_ylabel("$P_{span}(\\beta)$", color=INK)
    ax.set_title(
        "Spanning probability, center ignition (512 seeds, $\\pm 2\\sigma$)",
        color=INK, loc="left",
    )
    ax.set_ylim(-0.02, 1.02)
    ax.legend(frameon=False, loc="center right", fontsize=9)
    _style(ax)
    fig.tight_layout()
    fig.savefig(out)
    plt.close(fig)


def plot_chi_hat(arrays: dict, out: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 4.2), dpi=150)
    betas = arrays["betas"]
    for size in _sizes(arrays):
        chi = arrays[f"chi_hat_L{size}"]
        n = arrays[f"n_non_spanning_L{size}"]
        c = L_COLORS[size]
        # Solid where the estimate is well-supported; the sparse tail
        # (< 32 non-spanning runs of 512) is shown faded, not hidden.
        solid = np.isfinite(chi) & (n >= 32)
        faded = np.isfinite(chi) & (n >= 1)
        ax.plot(betas[faded], chi[faded], color=c, lw=1, alpha=0.3, ls=":")
        ax.plot(betas[solid], chi[solid], color=c, lw=2, marker="o", ms=3,
                label=f"L = {size}")
        peak = int(np.nanargmax(chi))
        ax.annotate(
            f"{chi[peak]:.0f}", xy=(betas[peak], chi[peak]),
            xytext=(0, 6), textcoords="offset points",
            ha="center", color=c, fontsize=8,
        )
    ax.set_yscale("log")
    ax.set_xlabel("spread probability $\\beta$", color=INK)
    ax.set_ylabel("$\\hat\\chi(\\beta)$  (mean burnt cluster, cells)",
                  color=INK)
    ax.set_title(
        "Mean burnt cluster size, non-spanning runs\n"
        "(peak grows with L: near-critical susceptibility; dotted where "
        "< 32 runs)",
        color=INK, loc="left", fontsize=10,
    )
    ax.legend(frameon=False, loc="upper right", fontsize=9)
    _style(ax)
    fig.tight_layout()
    fig.savefig(out)
    plt.close(fig)


def plot_front_speed(arrays: dict, summary: dict, out: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 4.2), dpi=150)
    betas = arrays["betas"]
    # Def.-4 High band criterion (M2.4): v-hat in [0.5, 1.0] cells/step.
    ax.axhspan(0.5, 1.0, color=MUTED, alpha=0.12, lw=0)
    ax.annotate("High-severity band criterion (0.5–1.0 cells/step)",
                xy=(0.02, 0.97), xycoords="axes fraction",
                color=MUTED, fontsize=8, va="top")
    for size in _sizes(arrays):
        v = arrays[f"v_hat_L{size}"]
        m = np.isfinite(v)
        ax.plot(betas[m], v[m], color=L_COLORS[size], lw=2, marker="o",
                ms=3, label=f"L = {size}")
    bc = summary["beta_c_half_locus_L_pow_-3/4"]
    ax.axvline(bc, color=MUTED, lw=1.5, ls=(0, (4, 3)))
    ax.set_xlabel("spread probability $\\beta$", color=INK)
    ax.set_ylabel("$\\hat v(\\beta)$  (cells / step)", color=INK)
    ax.set_title(
        "Supercritical front speed\n(slope of mean front radius over its "
        "linear regime)", color=INK, loc="left", fontsize=10,
    )
    ax.legend(frameon=False, loc="lower right", fontsize=9)
    _style(ax)
    fig.tight_layout()
    fig.savefig(out)
    plt.close(fig)


def plot_r_crossing(arrays: dict, summary: dict, out: Path) -> None:
    """R_L(beta) sigmoids on the fine grid — the finite-size curves that DO
    cross (2026-07-19 amendment); crossing marks + self-duality line."""
    fig, ax = plt.subplots(figsize=(7, 4.2), dpi=150)
    betas = arrays["r_betas"]
    for size in _sizes(arrays):
        r = arrays[f"r_L{size}"]
        se = arrays[f"r_se_L{size}"]
        c = L_COLORS[size]
        ax.fill_between(betas, r - 2 * se, r + 2 * se, color=c, alpha=0.15,
                        lw=0)
        ax.plot(betas, r, color=c, lw=2, label=f"L = {size}")
    ax.axhline(0.5, color=MUTED, lw=1, ls=(0, (2, 2)))
    ax.annotate("self-duality: R = ½ at $\\beta_c$", xy=(0.985, 0.515),
                xycoords=("axes fraction", "data"), ha="right",
                color=MUTED, fontsize=8)
    for pair, vals in summary.get("beta_c_R_crossings", {}).items():
        for v in vals:
            ax.axvline(v, color=MUTED, lw=1, ls=(0, (4, 3)), alpha=0.7)
            ax.annotate(f"{pair}: {v:.3f}", xy=(v, 0.06),
                        xytext=(4, 0), textcoords="offset points",
                        color=MUTED, fontsize=8, rotation=90, va="bottom")
    ax.set_xlabel("spread probability $\\beta$", color=INK)
    ax.set_ylabel("$R_L(\\beta)$", color=INK)
    ax.set_title(
        "Left–right crossing probability, full-left-column ignition\n"
        "(512 seeds, $\\pm 2\\sigma$; curve crossings estimate "
        "$\\beta_c$)", color=INK, loc="left", fontsize=10,
    )
    ax.set_ylim(-0.02, 1.02)
    ax.legend(frameon=False, loc="center right", fontsize=9)
    _style(ax)
    fig.tight_layout()
    fig.savefig(out)
    plt.close(fig)


def render_all(arrays: dict, summary: dict, out_dir: Path) -> None:
    plot_p_span(arrays, summary, out_dir / "p_span_sigmoids.png")
    plot_chi_hat(arrays, out_dir / "chi_hat.png")
    plot_front_speed(arrays, summary, out_dir / "front_speed.png")
    if "r_betas" in arrays:
        plot_r_crossing(arrays, summary, out_dir / "r_crossing.png")
