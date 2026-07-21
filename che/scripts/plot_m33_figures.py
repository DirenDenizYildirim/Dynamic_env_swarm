"""M3.3 ruling figures (human ruling 2026-07-21, options 1-2 accepted).

Re-renders the headline L = 64 sweep figure with the protocol-matched
reference line (uniform location + uniform age, unconditional mass)
beside the naive chi-hat line, and renders the four-factor deficit
waterfall panel for the phase report. Pure replot from the committed
JSONs — no simulation, no GPU.

    uv run python -m che.scripts.plot_m33_figures
"""

import json
from pathlib import Path

from che.calibration.prop3 import render_sweep_figure

M33 = Path("che/bench/results/phase3/m33")


def waterfall(block: dict, sweep: dict, out_path: Path) -> None:
    """Horizontal waterfall: chi-hat re-estimate -> drop conditioning ->
    uniform location -> age average (= matched ref) -> measured slope
    (residual = sibling seeds + cross-cluster overlap)."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    steps = [
        (
            f"χ̂ (center, non-span cond., 4L)\n{block['n_runs']} runs",
            block["chi_cond_center_4L"],
        ),
        ("drop conditioning\n(sweep keeps all runs)", block["m_center_uncond_4L"]),
        ("uniform seed location\n(boundary clipping)", block["m_unif_uncond_4L"]),
        (
            "uniform birth time\n(age-average = matched ref)",
            block["predicted_sweep_slope"],
        ),
        (
            "sibling seeds + overlap\n(= measured sweep slope)",
            sweep["slope_through_origin"],
        ),
    ]
    labels = [s[0] for s in steps]
    values = [s[1] for s in steps]
    fig, ax = plt.subplots(figsize=(6.4, 3.6), constrained_layout=True)
    y = range(len(steps))
    colors = ["tab:gray"] + [
        "tab:green" if values[i] > values[i - 1] else "tab:orange"
        for i in range(1, len(values))
    ]
    ax.barh(list(y), values, color=colors, height=0.6)
    for i, v in enumerate(values):
        factor = "" if i == 0 else f"  (×{values[i] / values[i - 1]:.3f})"
        ax.text(v + 0.6, i, f"{v:.1f}{factor}", va="center", fontsize=8)
    naive = sweep["chi_hat_ref"]
    ax.axvline(
        naive,
        ls="--",
        color="tab:green",
        lw=1,
        label=f"Phase-2 χ̂ ref (512 runs) = {naive:.1f}",
    )
    ax.set_yticks(list(y), labels, fontsize=8)
    ax.invert_yaxis()
    ax.set_xlabel("per-seed expected burnt mass (cells)")
    ax.set_title(
        f"Prop. 3 deficit decomposition, L={block['grid_size']}, β={sweep['beta']}"
    )
    ax.set_xlim(0, max(max(values), naive) * 1.22)
    ax.legend(fontsize=8, loc="lower right")
    fig.savefig(out_path, dpi=150)


def main() -> None:
    sweep = json.loads((M33 / "prop3_L64.json").read_text())
    deficit = json.loads((M33 / "deficit_decomposition.json").read_text())
    block = next(b for b in deficit["blocks"] if b["grid_size"] == sweep["grid_size"])
    render_sweep_figure(
        sweep,
        sweep["chi_hat_ref"],
        M33 / "prop3_L64.png",
        grid_size=sweep["grid_size"],
        n_runs=sweep["n_seeds_mc"],
        matched_ref=block["predicted_sweep_slope"],
    )
    waterfall(block, sweep, M33 / "deficit_waterfall.png")
    print(f"re-rendered {M33 / 'prop3_L64.png'}")
    print(f"wrote {M33 / 'deficit_waterfall.png'}")


if __name__ == "__main__":
    main()
