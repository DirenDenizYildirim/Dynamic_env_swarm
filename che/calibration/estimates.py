"""M2.2 estimators over the M2.1 calibration data (theory §3 observables).

Pure-numpy estimator functions (importable by M2.3's theory test) plus a CLI
that reads `calibration.npz`, writes `estimates.npz` (chi-hat is reused by
Phase 3's Prop.-3 test) + `estimates.json`, renders the three report figures,
and prints the beta_c summary.

Estimator notes (M2.2 spec vs. this data — preserve):

- **Pairwise crossings of center-seed P_span do not exist.** `spanned` is
  "center ignition ever touches the boundary", so a smaller grid is
  *easier* to span at every beta — the finite-size bias is one-sided and
  P_span^{L32} >= P_span^{L48} >= P_span^{L64} pointwise (verified on the
  data; common random numbers make the ordering exact). Estimator (a)
  therefore runs on the amendment observable R_L(beta) — left-column
  ignition, `crossed` = fire reaches the right column — whose finite-size
  curves do cross; pairs (32,48) and (48,64) per the amended spec.
- Estimator (b): the P_span = 1/2 locus beta_half(L) extrapolated against
  L^(-3/4) (nu = 4/3 exact for 2D percolation), with the plain 1/L fit
  reported as sensitivity.
- Soft check (reported, never a hard test): R_{L}(beta_c_hat) should be
  near 1/2 (self-duality).
- chi-hat (mean burnt cluster size on the subcritical side) = mean over
  *non-spanning* runs of burnt_fraction * L^2; NaN where every run spans.
- v-hat (supercritical front speed) = least-squares slope of the seed-mean
  front radius over its linear regime, defined as the steps where the mean
  radius lies in [20%, 80%] of the saturation radius L//2; NaN when the
  80% level is never reached (front did not establish — not supercritical).

CLI:

    uv run python -m che.calibration.estimates
"""

import argparse
import json
from pathlib import Path

import numpy as np

FINE_LO, FINE_HI = 0.395, 0.605  # the refined 0.40..0.60 window


def p_span_curve(spanned: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """P_span(beta) and its binomial standard error from [n_beta, n_seeds]."""
    n = spanned.shape[1]
    p = spanned.mean(axis=1)
    return p, np.sqrt(p * (1.0 - p) / n)


def pairwise_crossings(
    betas: np.ndarray, p_a: np.ndarray, p_b: np.ndarray
) -> list[float]:
    """Sign-change locations of p_a - p_b on the fine window (linear interp).

    Estimator (a) on R_L pairs; empty on center-seed P_span pairs (their
    finite-size bias is one-sided — see module docstring).
    """
    m = (betas >= FINE_LO) & (betas <= FINE_HI)
    b, d = betas[m], (p_a - p_b)[m]
    out = []
    for i in range(len(b) - 1):
        if d[i] * d[i + 1] < 0.0:  # strict sign change; a touch (d == 0)
            out.append(  # with same-signed neighbors is a tie, not a cross
                float(b[i] + (b[i + 1] - b[i]) * d[i] / (d[i] - d[i + 1]))
            )
    return out


def beta_half(betas: np.ndarray, p: np.ndarray) -> float:
    """First upward crossing of P_span = 1/2 (linear interpolation)."""
    for i in range(len(betas) - 1):
        if p[i] < 0.5 <= p[i + 1]:
            return float(
                betas[i]
                + (betas[i + 1] - betas[i]) * (0.5 - p[i]) / (p[i + 1] - p[i])
            )
    raise ValueError("P_span never crosses 1/2 on the beta grid")


def beta_c_extrapolated(
    sizes: np.ndarray, beta_halves: np.ndarray, exponent: float = 0.75
) -> tuple[float, float]:
    """(intercept, slope) of beta_half(L) ~ beta_c + a * L^(-exponent).

    Default exponent 3/4 = 1/nu with nu = 4/3 (exact, 2D percolation);
    exponent=1.0 gives the plain 1/L sensitivity fit.
    """
    x = np.asarray(sizes, dtype=np.float64) ** (-exponent)
    coeffs = np.polyfit(x, np.asarray(beta_halves, dtype=np.float64), 1)
    return float(coeffs[1]), float(coeffs[0])


def beta_c_steepest_slope(
    betas: np.ndarray, p: np.ndarray
) -> tuple[float, float]:
    """(argmax-slope beta, max slope) via central differences, fine window."""
    m = (betas >= FINE_LO) & (betas <= FINE_HI)
    b, q = betas[m], p[m]
    slope = (q[2:] - q[:-2]) / (b[2:] - b[:-2])
    i = int(np.argmax(slope))
    return float(b[1:-1][i]), float(slope[i])


def logistic_fit(
    betas: np.ndarray, p: np.ndarray
) -> tuple[float, float]:
    """(midpoint b0, scale s) of P = 1/(1 + exp(-(beta - b0)/s)), fit on the
    full grid by SSE grid search + one refinement (numpy-only; no scipy)."""

    def sse(b0: np.ndarray, s: np.ndarray) -> np.ndarray:
        pred = 1.0 / (
            1.0 + np.exp(-(betas[None, None, :] - b0[:, :, None]) / s[:, :, None])
        )
        return ((pred - p[None, None, :]) ** 2).sum(axis=-1)

    b0g = np.linspace(0.40, 0.60, 201)
    sg = np.geomspace(0.005, 0.2, 120)
    b0m, sm = np.meshgrid(b0g, sg, indexing="ij")
    i, j = np.unravel_index(np.argmin(sse(b0m, sm)), b0m.shape)
    b0g2 = np.linspace(b0g[max(i - 1, 0)], b0g[min(i + 1, len(b0g) - 1)], 81)
    sg2 = np.geomspace(sg[max(j - 1, 0)], sg[min(j + 1, len(sg) - 1)], 81)
    b0m2, sm2 = np.meshgrid(b0g2, sg2, indexing="ij")
    i2, j2 = np.unravel_index(np.argmin(sse(b0m2, sm2)), b0m2.shape)
    return float(b0m2[i2, j2]), float(sm2[i2, j2])


def chi_hat(
    burnt_fraction: np.ndarray, spanned: np.ndarray, grid_size: int
) -> tuple[np.ndarray, np.ndarray]:
    """(chi-hat(beta), n_non_spanning(beta)): mean burnt cluster size
    burnt_fraction * L^2 over non-spanning runs; NaN where all runs span."""
    non_span = ~spanned
    n = non_span.sum(axis=1)
    total = (burnt_fraction * grid_size**2 * non_span).sum(axis=1)
    return (
        np.where(n > 0, total / np.maximum(n, 1), np.nan),
        n.astype(np.int32),
    )


def front_speed(
    front_radius: np.ndarray, grid_size: int
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """(v-hat(beta), t_lo(beta), t_hi(beta)) from [n_beta, n_seeds, T].

    Slope of the seed-mean radius over the linear regime (mean radius in
    [0.2, 0.8] * (L // 2)); NaN/-1 when the regime is absent (see module
    docstring). t_lo/t_hi are the fitted 1-based step window bounds.
    """
    r_sat = grid_size // 2
    mean_r = front_radius.mean(axis=1)  # [n_beta, T]
    t = np.arange(1, mean_r.shape[1] + 1, dtype=np.float64)
    v = np.full(mean_r.shape[0], np.nan)
    t_lo = np.full(mean_r.shape[0], -1, dtype=np.int32)
    t_hi = np.full(mean_r.shape[0], -1, dtype=np.int32)
    for i, r in enumerate(mean_r):
        window = (r >= 0.2 * r_sat) & (r <= 0.8 * r_sat)
        if not (r >= 0.8 * r_sat).any() or window.sum() < 3:
            continue
        v[i] = np.polyfit(t[window], r[window], 1)[0]
        t_lo[i], t_hi[i] = int(t[window][0]), int(t[window][-1])
    return v, t_lo, t_hi


def compute_all(
    data: np.lib.npyio.NpzFile,
    crossing_data: np.lib.npyio.NpzFile | None = None,
) -> dict:
    """All M2.2 estimates from the raw calibration arrays, keyed for npz.

    crossing_data is the amendment sweep (R_L observable); estimator (a)
    and the self-duality soft check are skipped with a note if absent.
    """
    betas = np.asarray(data["betas"], dtype=np.float64)
    sizes = [int(s) for s in data["sizes"]]
    out: dict[str, np.ndarray] = {"betas": betas,
                                  "sizes": np.asarray(sizes, np.int32)}
    halves = []
    for size in sizes:
        p, se = p_span_curve(data[f"spanned_L{size}"])
        chi, n_ns = chi_hat(
            data[f"burnt_fraction_L{size}"], data[f"spanned_L{size}"], size
        )
        v, t_lo, t_hi = front_speed(data[f"front_radius_L{size}"], size)
        halves.append(beta_half(betas, p))
        out.update({
            f"p_span_L{size}": p,
            f"p_span_se_L{size}": se,
            f"chi_hat_L{size}": chi,
            f"n_non_spanning_L{size}": n_ns,
            f"v_hat_L{size}": v,
            f"v_fit_t_lo_L{size}": t_lo,
            f"v_fit_t_hi_L{size}": t_hi,
        })
    out["beta_half"] = np.asarray(halves)
    # Kept as a record: one-sided bias means these are empty (module
    # docstring); the live estimator (a) runs on R_L below.
    span_crossings = {
        f"L{a}_L{b}": pairwise_crossings(
            betas, out[f"p_span_L{a}"], out[f"p_span_L{b}"]
        )
        for a, b in [(32, 48), (32, 64), (48, 64)]
        if a in sizes and b in sizes
    }
    bc_nu, slope_nu = beta_c_extrapolated(
        np.asarray(sizes), out["beta_half"], exponent=0.75
    )
    bc_1l, slope_1l = beta_c_extrapolated(
        np.asarray(sizes), out["beta_half"], exponent=1.0
    )
    b_steep, max_slope = beta_c_steepest_slope(betas, out["p_span_L64"])
    b0_fit, s_fit = logistic_fit(betas, out["p_span_L64"])
    summary = {
        "span_pairwise_crossings_empty_by_design": span_crossings,
        "beta_half_per_L": {
            f"L{s}": h for s, h in zip(sizes, halves, strict=True)
        },
        "beta_c_half_locus_L_pow_-3/4": bc_nu,
        "half_locus_slope_L_pow_-3/4": slope_nu,
        "beta_c_half_locus_1_over_L_sensitivity": bc_1l,
        "half_locus_slope_1_over_L": slope_1l,
        "beta_c_steepest_slope_L64": b_steep,
        "max_slope_L64": max_slope,
        "beta_c_logistic_fit_L64": b0_fit,
        "logistic_scale_L64": s_fit,
    }

    if crossing_data is None:
        summary["crossing_mode"] = (
            "calibration_crossing.npz absent - estimator (a) on R_L and "
            "the self-duality soft check are pending the amendment sweep"
        )
        return {"arrays": out, "summary": summary}

    r_betas = np.asarray(crossing_data["betas"], dtype=np.float64)
    r_sizes = [int(s) for s in crossing_data["sizes"]]
    out["r_betas"] = r_betas
    for size in r_sizes:
        r, r_se = p_span_curve(crossing_data[f"crossed_L{size}"])
        out[f"r_L{size}"] = r
        out[f"r_se_L{size}"] = r_se
    r_crossings = {
        f"L{a}_L{b}": pairwise_crossings(
            r_betas, out[f"r_L{a}"], out[f"r_L{b}"]
        )
        for a, b in [(32, 48), (48, 64)]
        if a in r_sizes and b in r_sizes
    }
    cross_vals = [v for vs in r_crossings.values() for v in vs]
    estimates = [bc_nu, b_steep] + (
        [float(np.mean(cross_vals))] if cross_vals else []
    )
    consensus = float(np.mean(estimates))
    summary.update({
        "beta_c_R_crossings": r_crossings,
        "beta_c_R_crossings_mean": (
            float(np.mean(cross_vals)) if cross_vals else None
        ),
        "beta_c_consensus_mean_of_abc": consensus,
        "beta_c_spread_abc": [float(min(estimates)),
                              float(max(estimates))],
        # Self-duality soft check (report, never a hard test).
        "R_at_beta_c_consensus": {
            f"L{s}": float(np.interp(consensus, r_betas, out[f"r_L{s}"]))
            for s in r_sizes
        },
    })
    return {"arrays": out, "summary": summary}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--calibration",
        type=Path,
        default=Path("che/bench/results/phase2/calibration.npz"),
    )
    ap.add_argument(
        "--crossing",
        type=Path,
        default=Path("che/bench/results/phase2/calibration_crossing.npz"),
    )
    ap.add_argument(
        "--out-dir", type=Path, default=Path("che/bench/results/phase2")
    )
    args = ap.parse_args()

    data = np.load(args.calibration)
    crossing = np.load(args.crossing) if args.crossing.exists() else None
    res = compute_all(data, crossing)
    np.savez_compressed(args.out_dir / "estimates.npz", **res["arrays"])
    (args.out_dir / "estimates.json").write_text(
        json.dumps(res["summary"], indent=2) + "\n"
    )
    print(json.dumps(res["summary"], indent=2))

    from che.calibration.figures import render_all

    render_all(res["arrays"], res["summary"], args.out_dir)
    print(f"wrote estimates + figures to {args.out_dir}")


if __name__ == "__main__":
    main()
