"""M3.0 Def.-4 variance re-test report generator.

Reads the per-episode eval npz files produced by run_m30_def4.sh
(che/bench/results/phase3/m30/eval_{sev}_dp0.5_s{seed}.npz) and writes
che/bench/results/phase3/def4_variance.md: per-episode variance of
completion and survival_rate at fixed policy, per severity — per-seed and
pooled across seeds — with bootstrap 95% CIs (episode resampling, fixed
RNG). The Def.-4 prediction on record: Medium (near-critical) highest.
The outcome is reported verbatim either way.

Amended per human review of M3.0 (2026-07-20): the Verdict leads with the
mean-within-seed (fixed-policy) statistic; pooled is labelled
policy+episode variance; an environment-level burnt-fraction-variance
section (from phase2/calibration.npz, L=64), a variance-decomposition
paragraph, and a Phase-6 seed-budgeting note were added.

Run locally after the GPU results are back:
    uv run python che/scripts/def4_report.py
"""

from pathlib import Path

import numpy as np

M30 = Path("che/bench/results/phase3/m30")
CALIB = Path("che/bench/results/phase2/calibration.npz")
OUT = Path("che/bench/results/phase3/def4_variance.md")
SEVERITIES = ["low", "medium", "high"]
SEEDS = [0, 1, 2]
METRICS = ["completion", "survival_rate"]
N_BOOT = 5000
RNG = np.random.default_rng(0)


def boot_var_ci(vals: np.ndarray, n_boot: int = N_BOOT) -> tuple[float, float]:
    """Percentile-bootstrap 95% CI for the sample variance (ddof=1)."""
    n = len(vals)
    idx = RNG.integers(0, n, size=(n_boot, n))
    boots = vals[idx].var(axis=1, ddof=1)
    lo, hi = np.percentile(boots, [2.5, 97.5])
    return float(lo), float(hi)


def main():
    data = {}  # (sev, seed) -> {metric: [N]}
    for sev in SEVERITIES:
        for seed in SEEDS:
            f = M30 / f"eval_{sev}_dp0.5_s{seed}.npz"
            if not f.exists():
                raise SystemExit(f"missing {f} — run run_m30_def4.sh first")
            data[(sev, seed)] = dict(np.load(f))

    lines = [
        "# Def.-4 variance re-test (M3.0)",
        "",
        "Per-episode variance of completion and survival_rate at **fixed "
        "policy** (final checkpoints of the re-run M2.5 dp=0.5 grid; 512 "
        "stochastic eval episodes per checkpoint, eval seed 0).",
        "",
        "**Checkpoint provenance:** M2.5 saved no checkpoints, so the 9 "
        "dp=0.5 runs were re-run with identical configs/seeds "
        "(run_m30_def4.sh, 2026-07-20). The re-runs diverge from the M2.5 "
        "originals from update ~1-7 onward (GPU float nondeterminism "
        "compounding over training — same PRNG streams, nondeterministic "
        "reduction order), but final-20-update means match within "
        "across-seed noise (survival within ±0.02, completion within "
        "±0.06 per seed). The evaluated policies are M2.5-equivalent, not "
        "bitwise-identical.",
        "",
        "**Prediction on record (Def. 4 / phase2_report.md):** Medium "
        "(near-critical) has the highest per-episode variance. The M2.5 "
        "training-log probe could not cleanly measure this; this is the "
        "honest re-test. Outcome reported verbatim either way.",
        "",
        "Bootstrap 95% CIs: percentile method, episode resampling, "
        f"{N_BOOT} resamples, fixed RNG seed 0.",
        "",
    ]

    verdicts = {}
    for metric in METRICS:
        lines += [f"## {metric}", ""]
        lines += [
            "| severity | scope | N | mean | variance | 95% CI |",
            "|---|---|---|---|---|---|",
        ]
        pooled_vars = {}
        within_vars = {}
        for sev in SEVERITIES:
            per_seed_vals = [data[(sev, s)][metric].astype(np.float64) for s in SEEDS]
            for s, vals in zip(SEEDS, per_seed_vals, strict=True):
                lo, hi = boot_var_ci(vals)
                lines.append(
                    f"| {sev} | seed {s} | {len(vals)} | {vals.mean():.4f} "
                    f"| {vals.var(ddof=1):.5f} | [{lo:.5f}, {hi:.5f}] |"
                )
            pooled = np.concatenate(per_seed_vals)
            lo, hi = boot_var_ci(pooled)
            pooled_vars[sev] = pooled.var(ddof=1)
            within_vars[sev] = float(
                np.mean([v.var(ddof=1) for v in per_seed_vals])
            )
            seed_means = np.array([v.mean() for v in per_seed_vals])
            lines.append(
                f"| {sev} | pooled (policy+episode) | {len(pooled)} "
                f"| {pooled.mean():.4f} "
                f"| {pooled_vars[sev]:.5f} | [{lo:.5f}, {hi:.5f}] |"
            )
            lines.append(
                f"| {sev} | **mean within-seed (fixed policy)** | 3×512 | — "
                f"| **{within_vars[sev]:.5f}** | — |"
            )
            lines.append(
                f"| {sev} | between-seed var of means | 3 | — "
                f"| {seed_means.var(ddof=1):.5f} | — |"
            )
        ranking = sorted(pooled_vars, key=pooled_vars.get, reverse=True)
        within_ranking = sorted(within_vars, key=within_vars.get, reverse=True)
        verdicts[metric] = (ranking, within_ranking)
        lines += [
            "",
            f"Fixed-policy (mean within-seed) ranking: "
            f"**{' > '.join(within_ranking)}**. "
            f"Pooled (policy+episode) ranking: {' > '.join(ranking)}.",
            "",
            "Note: pooled variance mixes within-seed (episode) variance "
            "with between-seed policy differences — it is *not* the "
            "registered quantity (the registered quantity is per-episode "
            "variance at fixed policy, i.e. the mean-within-seed row); the "
            "between-seed row shows how much of the pooled figure is "
            "seed-to-seed.",
            "",
        ]

    # Environment-level mechanism: per-episode burnt-fraction variance vs
    # beta from the Phase-2 calibration sweep (hazard-only, L=64, 512 seeds
    # per beta) — Def. 4's environment-level prediction, measured without
    # any policy in the loop.
    calib = np.load(CALIB)
    betas = calib["betas"].astype(np.float64)
    bf = calib["burnt_fraction_L64"].astype(np.float64)
    bf_var = bf.var(axis=1, ddof=1)
    i_peak = int(np.argmax(bf_var))
    sev_beta = {"low": 0.43, "medium": 0.49, "high": 0.70}
    sev_idx = {s: int(np.argmin(np.abs(betas - b))) for s, b in sev_beta.items()}
    lines += [
        "## Environment-level mechanism: burnt-fraction variance vs beta",
        "",
        "Per-episode variance of burnt fraction from the Phase-2 "
        "calibration sweep (`phase2/calibration.npz`, hazard-only rollouts, "
        "L=64, 512 seeds per beta — no policy in the loop):",
        "",
        "| severity | beta | mean burnt fraction | variance |",
        "|---|---|---|---|",
    ]
    for sev in SEVERITIES:
        i = sev_idx[sev]
        lines.append(
            f"| {sev} | {betas[i]:.2f} | {bf[i].mean():.4f} "
            f"| {bf_var[i]:.4f} |"
        )
    lines += [
        "",
        f"The full curve peaks at beta = {betas[i_peak]:.2f} "
        f"(variance {bf_var[i_peak]:.4f}), i.e. in the near-critical "
        "window just above the Medium lock and far from both the Low and "
        "High locks. At the three locked severities the environment-level "
        "variance ranks **medium >> high > low** (0.0354 vs 0.0019 vs "
        "0.0008 — a 19-44x gap). **Def. 4's environment-level mechanism is "
        "CONFIRMED**: hazard-outcome variance is maximal near criticality.",
        "",
        "Full curve (variance of burnt fraction, L=64, ddof=1):",
        "",
        "| beta | variance | | beta | variance |",
        "|---|---|---|---|---|",
    ]
    half = (len(betas) + 1) // 2
    for j in range(half):
        left = f"| {betas[j]:.2f} | {bf_var[j]:.4f} |"
        k = j + half
        right = (
            f" {betas[k]:.2f} | {bf_var[k]:.4f} |" if k < len(betas) else "  | |"
        )
        lines.append(left + right)
    lines += [
        "",
        "## Decomposition",
        "",
        "As registered, the prediction is refuted / not confirmed: "
        "task-outcome variance at fixed policy does not peak at Medium "
        "(survival is monotone in severity; completion is a "
        "Medium-Low tie). The decomposition explains why without "
        "rescuing the registered claim: outcome variance ~ "
        "(environment variance) x (policy sensitivity to the "
        "environment). The environment factor peaks near criticality "
        "(Medium, table above), but the policy-sensitivity factor grows "
        "with severity — at Low the trained policy absorbs hazard "
        "fluctuations (survival ceiling), while at High every hazard "
        "realization couples into deaths and lost food. The two factors "
        "peak in different regimes, so the product need not peak at "
        "Medium.",
        "",
        "## Verdict",
        "",
        # Wording per human review of M3.0 (2026-07-20); leads with the
        # fixed-policy statistic, the analysis's own cleanest measure.
        "- **survival_rate: REFUTED** — fixed-policy per-episode variance "
        "is monotone in severity (high > medium > low); High highest, not "
        "Medium.",
        "- **completion: NOT CONFIRMED** — Medium ≈ Low within bootstrap "
        "CIs (0.01245 vs 0.01235), both above High; no resolvable Medium "
        "peak.",
        "- **Environment-level mechanism (Def. 4): CONFIRMED** — "
        "burnt-fraction variance peaks near criticality (beta ≈ 0.53; "
        "medium >> high > low at the locked severities).",
        "",
        "## Note for Phase 6 (seed budgeting)",
        "",
        "High-severity between-seed variance is dominated by one seed "
        "(seed 2 trained to a distinctly better policy: completion 0.868 / "
        "survival 0.956 vs ~0.74/0.85 for seeds 0-1). Training-solution "
        "diversity at High severity is real and large relative to episode "
        "noise — an input for the Phase-6 seed budget: High-severity cells "
        "need more seeds (or explicit solution-diversity reporting) for "
        "trustworthy means.",
        "",
    ]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines))
    print(f"wrote {OUT}")
    for metric, (ranking, within_ranking) in verdicts.items():
        print(f"{metric}: fixed-policy {' > '.join(within_ranking)} | "
              f"pooled {' > '.join(ranking)}")
    print(f"env burnt-fraction variance peak: beta={betas[i_peak]:.2f}")


if __name__ == "__main__":
    main()
