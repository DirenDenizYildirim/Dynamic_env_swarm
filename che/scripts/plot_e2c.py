"""M4.2 figure: Theorem 1 as a picture (theory §5 Thm. 1, §10 hook).

Runs the E2C sweep and renders J* vs kappa_B — numeric predicted curve,
empirical points with error bars, and the 1/2 memorization floor — plus
the plane-7 side-channel oracle on a twin axis (M4.2 ruling item 3: the
side channel gets a number, not a remark). Writes the raw sweep to JSON
beside the figure.

    uv run python -m che.scripts.plot_e2c

CPU-only; a few minutes at the default sizes.
"""

import argparse
import json
import subprocess
from pathlib import Path

import jax
import numpy as np

from che.env.e2c import (
    B_COL,
    B_ROW,
    CORRIDOR_LEN,
    D_PATH,
    ETA,
    GRID,
    HORIZON,
    K_OBS,
    KAPPA_GRID,
    L_F,
    SIGMA_S,
    run_sweep,
)

OUT_DIR = Path("che/bench/results/phase4/m42")


def render_figure(sweep: list[dict], out_path: Path, *, n_episodes: int) -> None:
    """J* vs kappa_B: predicted curve, empirical points, 1/2 floor, and
    the plane-7 oracle's accuracy (the residual side channel)."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    kb = np.array([p["kappa_B"] for p in sweep])
    j_emp = np.array([p["j_optimal"] for p in sweep])
    se_emp = np.array([p["se_j_optimal"] for p in sweep])
    j_pred = np.array([p["j_predicted"] for p in sweep])
    j_mem = np.array([p["j_memorizing"] for p in sweep])
    se_mem = np.array([p["se_j_memorizing"] for p in sweep])
    oracle = np.array([p["oracle_accuracy"] for p in sweep])

    fig, ax = plt.subplots(figsize=(5.6, 4.2), constrained_layout=True)
    ax.plot(kb, j_pred, "-", color="tab:blue", lw=1.8,
            label=r"predicted $\frac{1}{2}+\frac{q(\kappa_B)}{2}$ (MC, shared $\tau$)")
    ax.errorbar(kb, j_emp, yerr=2 * se_emp, fmt="o", ms=5, capsize=3,
                color="tab:blue", mfc="white", label="empirical $J^*$ (±2·SE)")
    ax.errorbar(kb, j_mem, yerr=2 * se_mem, fmt="s", ms=4, capsize=3,
                color="tab:gray", label="memorizing (always-L)")
    ax.axhline(0.5, ls="--", lw=1.0, color="tab:gray")
    ax.fill_between(kb, j_mem, j_pred, color="tab:blue", alpha=0.08)
    ax.annotate("memorization gap = q/2", xy=(kb[2], (j_pred[2] + 0.5) / 2),
                xytext=(kb[2] + 0.6, 0.85), fontsize=8,
                arrowprops={"arrowstyle": "->", "lw": 0.8})
    ax.set_xlabel(r"$\kappa_B$")
    ax.set_ylabel("value (task completion rate)")
    ax.set_ylim(0.45, 1.03)
    ax.set_title(
        f"Thm. 1 in $E_{{2C}}$: d={D_PATH}, $\\ell_f$={L_F}, "
        f"$\\ell$={CORRIDOR_LEN}, k={K_OBS}, {n_episodes} eps/point"
    )

    ax2 = ax.twinx()
    ax2.plot(kb, oracle, "^:", ms=4, color="tab:red", lw=1.0,
             label="plane-7 oracle accuracy")
    ax2.set_ylabel("side-channel oracle accuracy", color="tab:red")
    ax2.tick_params(axis="y", labelcolor="tab:red")
    ax2.set_ylim(0.45, 1.03)

    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, fontsize=7.5, loc="center right")
    fig.savefig(out_path, dpi=150)


def replicate_diagnostic(n_seeds: int, n_episodes: int, n_mc: int) -> dict:
    """Replicate the sweep over independent seeds and report the z-score
    (delta / SE_delta) distribution per kappa_B.

    Evidence for the M4.2 acceptance-criterion ruling request: under a
    correct implementation z ~ N(0, 1) per point, so the phase prompt's
    per-point 2·SE gate fails ~28% of the time across 7 informative
    points. This separates "the implementation is biased" from "the gate
    is under-powered" — only the first would be a code problem.
    """
    sweeps = [
        run_sweep(jax.random.PRNGKey(100 + s), n_episodes=n_episodes, n_mc=n_mc)
        for s in range(n_seeds)
    ]
    per_point, pooled = [], []
    for j, kb in enumerate(KAPPA_GRID):
        z = np.array([
            (r[j]["delta"] / r[j]["se_delta"]) if r[j]["se_delta"] > 0 else 0.0
            for r in sweeps
        ])
        dq = np.array([r[j]["q_mc"] - r[j]["q_empirical"] for r in sweeps])
        per_point.append({
            "kappa_B": float(kb),
            "mean_z": float(z.mean()),
            "sd_z": float(z.std(ddof=1)),
            "n_exceed_2sigma": int((np.abs(z) > 2).sum()),
            "mean_q_mc_minus_q_observed": float(dq.mean()),
        })
        if kb > 0:  # kappa_B = 0 is deterministic (tau == 1 => q == 1)
            pooled.extend(z.tolist())
    pooled = np.array(pooled)
    return {
        "n_seeds": n_seeds,
        "per_point": per_point,
        "pooled_mean_z": float(pooled.mean()),
        "pooled_sd_z": float(pooled.std(ddof=1)),
        "pooled_frac_exceed_2sigma": float((np.abs(pooled) > 2).mean()),
        "pooled_n": int(pooled.size),
        # A systematic offset larger than this (in units of SE) would show.
        "detectable_bias_sigma": float(1.0 / np.sqrt(pooled.size)),
    }


def _git_commit() -> str:
    try:
        return subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--n-episodes", type=int, default=8192)
    p.add_argument("--n-mc", type=int, default=8192)
    p.add_argument("--out-dir", type=Path, default=OUT_DIR)
    p.add_argument(
        "--replicates",
        type=int,
        default=0,
        help="also run the z-score replicate diagnostic over N seeds",
    )
    args = p.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    sweep = run_sweep(
        jax.random.PRNGKey(args.seed),
        n_episodes=args.n_episodes,
        n_mc=args.n_mc,
    )
    payload = {
        "commit": _git_commit(),
        "geometry": {
            "d": D_PATH, "l_f": L_F, "ell": CORRIDOR_LEN, "k": K_OBS,
            "grid": GRID, "horizon": HORIZON, "branch": [B_ROW, B_COL],
            "sigma_s": SIGMA_S, "eta": ETA,
        },
        "protocol": (
            "scripted hazard (fire cell held Burning); one smoke_step "
            "before the first observation, then one per step; observations "
            "via observation.observe at obs v3 with the env._OBS_STREAM "
            "fold_in; prediction MC draws Bernoulli(tau) from the shared "
            "transmittance on an independent PRNG stream."
        ),
        "seed": args.seed,
        "sweep": sweep,
    }
    (args.out_dir / "e2c_sweep.json").write_text(json.dumps(payload, indent=2))
    render_figure(sweep, args.out_dir / "e2c_theorem1.png",
                  n_episodes=args.n_episodes)

    print(f"{'kappa_B':>8} {'J*_emp':>8} {'J*_pred':>8} {'delta':>8} "
          f"{'2*SE':>7} {'q_mc':>7} {'q_obs':>7} {'J_mem':>7} {'oracle':>7}")
    for r in sweep:
        print(f"{r['kappa_B']:8.2f} {r['j_optimal']:8.4f} "
              f"{r['j_predicted']:8.4f} {r['delta']:+8.4f} "
              f"{2 * r['se_delta']:7.4f} {r['q_mc']:7.4f} "
              f"{r['q_empirical']:7.4f} {r['j_memorizing']:7.4f} "
              f"{r['oracle_accuracy']:7.4f}")
    print(f"\nwrote {args.out_dir}/e2c_sweep.json and e2c_theorem1.png")

    if args.replicates:
        diag = replicate_diagnostic(args.replicates, args.n_episodes, args.n_mc)
        (args.out_dir / "e2c_replicates.json").write_text(
            json.dumps(diag, indent=2)
        )
        print(f"\nreplicate diagnostic ({diag['n_seeds']} seeds):")
        print(f"{'kappa_B':>8} {'mean z':>8} {'sd z':>7} {'|z|>2':>6}")
        for r in diag["per_point"]:
            print(f"{r['kappa_B']:8.2f} {r['mean_z']:+8.3f} "
                  f"{r['sd_z']:7.3f} {r['n_exceed_2sigma']:6d}")
        print(f"pooled (kappa_B>0, n={diag['pooled_n']}): "
              f"mean z={diag['pooled_mean_z']:+.3f} "
              f"sd={diag['pooled_sd_z']:.3f} "
              f"|z|>2 in {100 * diag['pooled_frac_exceed_2sigma']:.1f}% "
              f"(4.6% expected)")
        print(f"wrote {args.out_dir}/e2c_replicates.json")


if __name__ == "__main__":
    main()
