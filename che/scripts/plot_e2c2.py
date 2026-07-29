"""M5.2 figure: Remark 2 as a picture (theory §5 Remark 2′/2″/2‴).

The companion panel to the Theorem-1 figure. Runs the E2C-2 courier sweep
and renders J vs kappa_B for the free and denied arms with the VoC gap
shaded, plus the dawdle correction — the residual Remark 2″ admitted and
Remark 2‴ deferred to this milestone for its constants.

    uv run python -m che.scripts.plot_e2c2

CPU-only; ~15 minutes at the default sizes on two threads.
"""

import argparse
import json
import subprocess
from pathlib import Path

import jax
import numpy as np

from che.env.e2c2 import (
    CORRIDOR_LEN,
    D_PATH,
    E2C2_HORIZON,
    ETA,
    GRID,
    IDLE_SCHEDULES,
    K_OBS,
    KAPPA_GRID,
    L_F,
    PINNED_SCHEDULE,
    SIGMA_S,
    run_sweep,
)

OUT_DIR = Path("che/bench/results/phase5/m52")


def render_figure(sweep: list[dict], out_path: Path, *, n_episodes: int) -> None:
    """J vs kappa_B, both arms, VoC shaded — and the dawdle curve between
    them, which is the whole point of the correction."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    kb = np.array([p["kappa_B"] for p in sweep])
    j_free = np.array([p["j_free"] for p in sweep])
    se_free = np.array([p["se_j_free"] for p in sweep])
    j_pin = np.array([p["j_pinned"] for p in sweep])
    se_pin = np.array([p["se_j_pinned"] for p in sweep])
    j_pred = np.array([p["j_predicted"] for p in sweep])
    j_daw = np.array([0.5 + p["q_tilde"] / 2.0 for p in sweep])
    voc_g = np.array([p["voc_gated"] for p in sweep])
    voc_t = np.array([p["voc_true"] for p in sweep])

    fig, (ax, ax2) = plt.subplots(
        2, 1, figsize=(5.8, 6.4), height_ratios=[2.0, 1.0],
        sharex=True, constrained_layout=True,
    )

    # --- top: the two arms and the gap ---------------------------------
    # Disjoint bands, not overlapping alphas: the true VoC is the gap the
    # courier cannot close by idling, and the correction is the slice
    # dawdling recovers. Stacked they are VoC_gated.
    ax.fill_between(kb, j_daw, j_free, color="tab:green", alpha=0.14,
                    label=r"VoC$_{\mathrm{true}} = \frac{1}{2}(1-\tilde q)$")
    ax.fill_between(kb, j_pin, j_daw, color="tab:orange", alpha=0.30,
                    label="dawdle correction (Remark 2″ residual)")
    ax.errorbar(kb, j_free, yerr=2 * se_free, fmt="o-", ms=5, capsize=3,
                lw=1.8, color="tab:green", mfc="white",
                label=r"free comms ($\delta=0$)")
    ax.plot(kb, j_pred, "-", lw=1.6, color="tab:blue",
            label=r"predicted $\frac{1}{2}+\frac{q}{2}$ (MC, shared $\tau$)")
    ax.errorbar(kb, j_pin, yerr=2 * se_pin, fmt="s", ms=5, capsize=3,
                color="tab:blue", mfc="white",
                label=r"denied, pinned ($\delta=1$) — gated arm")
    ax.plot(kb, j_daw, "^--", ms=4, lw=1.2, color="tab:orange",
            label=r"denied + dawdle: $\frac{1}{2}+\frac{\tilde q}{2}$")
    ax.axhline(0.5, ls="--", lw=1.0, color="tab:gray")
    ax.set_ylabel("value (courier reaches the goal)")
    ax.set_ylim(0.45, 1.03)
    ax.set_title(
        f"Remark 2 in $E_{{2C}}$-courier: d={D_PATH}, $\\ell_f$={L_F}, "
        f"$\\ell$={CORRIDOR_LEN}, T={E2C2_HORIZON}, k={K_OBS}, "
        f"{n_episodes} eps/pt",
        fontsize=9.5,
    )
    ax.legend(fontsize=7.2, loc="center right")

    # --- bottom: the correction itself ---------------------------------
    ax2.plot(kb, voc_g, "s-", ms=4, lw=1.6, color="tab:green",
             label=r"VoC$_{\mathrm{gated}}$ (protocol-matched)")
    ax2.plot(kb, voc_t, "^--", ms=4, lw=1.4, color="tab:orange",
             label=r"VoC$_{\mathrm{true}}$ (open-loop optimum)")
    ax2.axhline(0.5, ls=":", lw=0.9, color="tab:gray")
    ax2.set_xlabel(r"$\kappa_B$")
    ax2.set_ylabel("VoC")
    ax2.set_ylim(-0.02, 0.55)
    ax2.legend(fontsize=7.2, loc="lower right")
    ax2.fill_between(kb, voc_t, voc_g, color="tab:orange", alpha=0.30)
    # Point at where the *relative* correction is largest, which is the
    # non-obvious half of Remark 2‴: in absolute terms the band looks
    # widest in the middle, but VoC lives in 1 - q and the margin is
    # thinnest at low kappa_B.
    rel = np.divide(voc_g - voc_t, voc_g, out=np.zeros_like(voc_g), where=voc_g > 1e-9)
    i = int(np.argmax(rel[1:])) + 1
    ax2.annotate(
        f"relative correction peaks here:\n{100 * rel[i]:.0f} % of VoC$_"
        r"{\mathrm{gated}}$ at $\kappa_B$=" + f"{kb[i]:g}",
        xy=(kb[i], 0.5 * (voc_g[i] + voc_t[i])), xytext=(2.6, 0.06),
        fontsize=7.2, arrowprops={"arrowstyle": "->", "lw": 0.8},
    )
    fig.savefig(out_path, dpi=150)


def replicate_diagnostic(
    n_seeds: int, n_episodes: int, n_mc: int, kappas: tuple[float, ...]
) -> dict:
    """Is the M5.2 gate calibrated? Measure z over independent seeds.

    The first M5.2 sweep returned sum z^2 = 0.51 on 7 informative dof
    where 7 is expected — a fit that is *too good*, which is the
    signature of overstated SEs, i.e. a gate that would not catch a real
    defect. M4.2 faced the mirror-image question and settled it by
    measuring the z distribution rather than arguing about it; same here.
    Under a correct implementation with correct SEs, z ~ N(0, 1).

    Runs the gated arm only (pinned + its MC prediction) — the dawdle
    family is ~75 % of a sweep point's cost and is not what is being
    calibrated.
    """
    from che.env.e2c2 import PINNED_SCHEDULE as PIN
    from che.env.e2c2 import _rate_se, e2c2_config, predict_q, run_episodes

    per_point, pooled = [], []
    for kb in kappas:
        cfg = e2c2_config(kb, 1.0)
        z = []
        for s in range(n_seeds):
            k_emp, k_mc = jax.random.split(jax.random.PRNGKey(1000 + s))
            ep = run_episodes(k_emp, cfg, n_episodes, PIN)
            j, se_j = _rate_se(ep["success_pinned"])
            q, se_q = _rate_se(predict_q(k_mc, cfg, n_mc, PIN))
            se = float(np.hypot(se_j, se_q / 2.0))
            z.append((j - (0.5 + q / 2.0)) / se if se > 0 else 0.0)
        z = np.array(z)
        per_point.append({
            "kappa_B": float(kb),
            "mean_z": float(z.mean()),
            "sd_z": float(z.std(ddof=1)),
            "n_exceed_2sigma": int((np.abs(z) > 2).sum()),
        })
        pooled.extend(z.tolist())
    pooled = np.array(pooled)
    return {
        "n_seeds": n_seeds,
        "n_episodes": n_episodes,
        "n_mc": n_mc,
        "per_point": per_point,
        "pooled_mean_z": float(pooled.mean()),
        "pooled_sd_z": float(pooled.std(ddof=1)),
        "pooled_frac_exceed_2sigma": float((np.abs(pooled) > 2).mean()),
        "pooled_n": int(pooled.size),
        # sd_z well below 1 => the SEs are conservative and the gate is
        # under-powered; well above 1 => the SEs are optimistic and the
        # gate over-rejects. Either is a finding about the gate.
        "verdict_hint": "sd_z ~ 1 means the gate is calibrated",
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
    p.add_argument("--n-episodes", type=int, default=4096)
    p.add_argument("--n-mc", type=int, default=8192)
    p.add_argument("--out-dir", type=Path, default=OUT_DIR)
    p.add_argument(
        "--replicates",
        type=int,
        default=0,
        help="run the z-calibration diagnostic over N seeds instead of the sweep",
    )
    p.add_argument(
        "--from-json",
        action="store_true",
        help="re-render the figure from the saved sweep instead of re-measuring",
    )
    args = p.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    if args.replicates:
        diag = replicate_diagnostic(
            args.replicates, args.n_episodes, args.n_mc,
            tuple(k for k in KAPPA_GRID if 0.0 < k <= 3.0),
        )
        (args.out_dir / "e2c2_replicates.json").write_text(json.dumps(diag, indent=2))
        print(f"z calibration, {diag['n_seeds']} seeds "
              f"({args.n_episodes} eps / {args.n_mc} mc):")
        for r in diag["per_point"]:
            print(f"  kappa_B={r['kappa_B']:>4.1f}  mean z={r['mean_z']:+.3f}  "
                  f"sd z={r['sd_z']:.3f}  |z|>2: {r['n_exceed_2sigma']}")
        print(f"  pooled: mean {diag['pooled_mean_z']:+.3f}  "
              f"sd {diag['pooled_sd_z']:.3f}  "
              f"frac|z|>2 {diag['pooled_frac_exceed_2sigma']:.3f}  "
              f"(n={diag['pooled_n']})")
        return

    # Re-rendering must not cost another sweep: the figure is iterated on
    # far more often than the measurement changes, and re-running would
    # also silently re-roll the numbers the report quotes.
    cached = args.out_dir / "e2c2_sweep.json"
    if args.from_json:
        sweep = json.loads(cached.read_text())["sweep"]
        render_figure(sweep, args.out_dir / "e2c2_remark2.png",
                      n_episodes=sweep[0]["n_episodes"])
        print(f"re-rendered {args.out_dir}/e2c2_remark2.png from {cached}")
        return

    sweep = run_sweep(
        jax.random.PRNGKey(args.seed),
        n_episodes=args.n_episodes,
        n_mc=args.n_mc,
    )
    payload = {
        "commit": _git_commit(),
        "geometry": {
            "d": D_PATH, "l_f": L_F, "ell": CORRIDOR_LEN, "k": K_OBS,
            "grid": GRID, "horizon": E2C2_HORIZON,
            "sigma_s": SIGMA_S, "eta": ETA,
            "horizon_rule": "T = d + l_f + ell (fire-anchored scouting)",
        },
        "protocol": (
            "courier + scout; the scout probes corridor L to depth l_f and "
            "certifies it at step d + l_f if alive. Delivery through the "
            "production Def.-7 kernel (comms.in_range_mask + "
            "comms.sample_links). The courier reads content planes only "
            "(never plane 6, never plane 7), so the scout's fate reaches it "
            "only as a message. Prediction MC draws Bernoulli(tau) from the "
            "shared transmittance on an independent PRNG stream."
        ),
        "schedules": {
            "pinned": list(PINNED_SCHEDULE),
            "idle_family": [list(s) for s in IDLE_SCHEDULES],
        },
        "seed": args.seed,
        "sweep": sweep,
    }
    (args.out_dir / "e2c2_sweep.json").write_text(json.dumps(payload, indent=2))
    render_figure(sweep, args.out_dir / "e2c2_remark2.png",
                  n_episodes=args.n_episodes)

    print(f"{'kappa_B':>8} {'J_free':>7} {'J_pin':>7} {'J_pred':>7} {'z':>6} "
          f"{'q':>7} {'q~':>7} {'q~/q':>6} {'VoC_g':>7} {'VoC_t':>7}  best")
    for r in sweep:
        z = r["delta_gate"] / r["se_delta_gate"] if r["se_delta_gate"] > 0 else 0.0
        ratio = r["q_tilde"] / r["q_mc"] if r["q_mc"] > 0 else float("nan")
        print(f"{r['kappa_B']:8.2f} {r['j_free']:7.4f} {r['j_pinned']:7.4f} "
              f"{r['j_predicted']:7.4f} {z:+6.2f} {r['q_mc']:7.4f} "
              f"{r['q_tilde']:7.4f} {ratio:6.3f} {r['voc_gated']:7.4f} "
              f"{r['voc_true']:7.4f}  {r['best_schedule']}")
    print(f"\nwrote {args.out_dir}/e2c2_sweep.json and e2c2_remark2.png")


if __name__ == "__main__":
    main()
