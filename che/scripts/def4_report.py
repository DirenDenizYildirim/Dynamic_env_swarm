"""M3.0 Def.-4 variance re-test report generator.

Reads the per-episode eval npz files produced by run_m30_def4.sh
(che/bench/results/phase3/m30/eval_{sev}_dp0.5_s{seed}.npz) and writes
che/bench/results/phase3/def4_variance.md: per-episode variance of
completion and survival_rate at fixed policy, per severity — per-seed and
pooled across seeds — with bootstrap 95% CIs (episode resampling, fixed
RNG). The Def.-4 prediction on record: Medium (near-critical) highest.
The outcome is reported verbatim either way.

Run locally after the GPU results are back:
    uv run python che/scripts/def4_report.py
"""

from pathlib import Path

import numpy as np

M30 = Path("che/bench/results/phase3/m30")
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
            seed_means = np.array([v.mean() for v in per_seed_vals])
            lines.append(
                f"| {sev} | **pooled** | {len(pooled)} | {pooled.mean():.4f} "
                f"| **{pooled_vars[sev]:.5f}** | [{lo:.5f}, {hi:.5f}] |"
            )
            lines.append(
                f"| {sev} | between-seed var of means | 3 | — "
                f"| {seed_means.var(ddof=1):.5f} | — |"
            )
        ranking = sorted(pooled_vars, key=pooled_vars.get, reverse=True)
        verdicts[metric] = ranking
        lines += [
            "",
            f"Pooled-variance ranking: {' > '.join(ranking)}. "
            + (
                "**Prediction CONFIRMED (Medium highest).**"
                if ranking[0] == "medium"
                else f"**Prediction REFUTED ({ranking[0]} highest, not Medium).**"
            ),
            "",
            "Note: pooled variance mixes within-seed (episode) variance with "
            "between-seed policy differences; the between-seed row above "
            "shows how much of the pooled figure is seed-to-seed.",
            "",
        ]

    lines += [
        "## Verdict",
        "",
    ]
    for metric, ranking in verdicts.items():
        outcome = "CONFIRMED" if ranking[0] == "medium" else "REFUTED"
        lines.append(f"- {metric}: {outcome} — ranking {' > '.join(ranking)}.")
    lines.append("")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines))
    print(f"wrote {OUT}")
    for metric, ranking in verdicts.items():
        print(f"{metric}: {' > '.join(ranking)}")


if __name__ == "__main__":
    main()
