# Def.-4 variance re-test (M3.0)

Per-episode variance of completion and survival_rate at **fixed policy** (final checkpoints of the re-run M2.5 dp=0.5 grid; 512 stochastic eval episodes per checkpoint, eval seed 0).

**Checkpoint provenance:** M2.5 saved no checkpoints, so the 9 dp=0.5 runs were re-run with identical configs/seeds (run_m30_def4.sh, 2026-07-20). The re-runs diverge from the M2.5 originals from update ~1-7 onward (GPU float nondeterminism compounding over training — same PRNG streams, nondeterministic reduction order), but final-20-update means match within across-seed noise (survival within ±0.02, completion within ±0.06 per seed). The evaluated policies are M2.5-equivalent, not bitwise-identical.

**Prediction on record (Def. 4 / phase2_report.md):** Medium (near-critical) has the highest per-episode variance. The M2.5 training-log probe could not cleanly measure this; this is the honest re-test. Outcome reported verbatim either way.

Bootstrap 95% CIs: percentile method, episode resampling, 5000 resamples, fixed RNG seed 0.

## completion

| severity | scope | N | mean | variance | 95% CI |
|---|---|---|---|---|---|
| low | seed 0 | 512 | 0.7476 | 0.01184 | [0.01033, 0.01337] |
| low | seed 1 | 512 | 0.6951 | 0.01412 | [0.01259, 0.01571] |
| low | seed 2 | 512 | 0.7679 | 0.01109 | [0.00988, 0.01230] |
| low | pooled (policy+episode) | 1536 | 0.7369 | 0.01328 | [0.01240, 0.01418] |
| low | **mean within-seed (fixed policy)** | 3×512 | — | **0.01235** | — |
| low | between-seed var of means | 3 | — | 0.00141 | — |
| medium | seed 0 | 512 | 0.7889 | 0.01064 | [0.00923, 0.01217] |
| medium | seed 1 | 512 | 0.7376 | 0.01377 | [0.01203, 0.01547] |
| medium | seed 2 | 512 | 0.7583 | 0.01293 | [0.01142, 0.01452] |
| medium | pooled (policy+episode) | 1536 | 0.7616 | 0.01288 | [0.01194, 0.01381] |
| medium | **mean within-seed (fixed policy)** | 3×512 | — | **0.01245** | — |
| medium | between-seed var of means | 3 | — | 0.00067 | — |
| high | seed 0 | 512 | 0.7858 | 0.00984 | [0.00857, 0.01115] |
| high | seed 1 | 512 | 0.7357 | 0.01305 | [0.01146, 0.01471] |
| high | seed 2 | 512 | 0.8681 | 0.00891 | [0.00779, 0.01006] |
| high | pooled (policy+episode) | 1536 | 0.7965 | 0.01356 | [0.01259, 0.01456] |
| high | **mean within-seed (fixed policy)** | 3×512 | — | **0.01060** | — |
| high | between-seed var of means | 3 | — | 0.00447 | — |

Fixed-policy (mean within-seed) ranking: **medium > low > high**. Pooled (policy+episode) ranking: high > low > medium.

Note: pooled variance mixes within-seed (episode) variance with between-seed policy differences — it is *not* the registered quantity (the registered quantity is per-episode variance at fixed policy, i.e. the mean-within-seed row); the between-seed row shows how much of the pooled figure is seed-to-seed.

## survival_rate

| severity | scope | N | mean | variance | 95% CI |
|---|---|---|---|---|---|
| low | seed 0 | 512 | 0.9906 | 0.00100 | [0.00064, 0.00142] |
| low | seed 1 | 512 | 0.9930 | 0.00094 | [0.00047, 0.00155] |
| low | seed 2 | 512 | 0.9940 | 0.00079 | [0.00037, 0.00137] |
| low | pooled (policy+episode) | 1536 | 0.9925 | 0.00091 | [0.00066, 0.00121] |
| low | **mean within-seed (fixed policy)** | 3×512 | — | **0.00091** | — |
| low | between-seed var of means | 3 | — | 0.00000 | — |
| medium | seed 0 | 512 | 0.9652 | 0.00490 | [0.00369, 0.00630] |
| medium | seed 1 | 512 | 0.9631 | 0.00498 | [0.00399, 0.00601] |
| medium | seed 2 | 512 | 0.9342 | 0.01138 | [0.00909, 0.01394] |
| medium | pooled (policy+episode) | 1536 | 0.9542 | 0.00728 | [0.00630, 0.00840] |
| medium | **mean within-seed (fixed policy)** | 3×512 | — | **0.00709** | — |
| medium | between-seed var of means | 3 | — | 0.00030 | — |
| high | seed 0 | 512 | 0.8638 | 0.01121 | [0.00973, 0.01279] |
| high | seed 1 | 512 | 0.8483 | 0.01171 | [0.01034, 0.01318] |
| high | seed 2 | 512 | 0.9562 | 0.00364 | [0.00312, 0.00416] |
| high | pooled (policy+episode) | 1536 | 0.8894 | 0.01111 | [0.01025, 0.01199] |
| high | **mean within-seed (fixed policy)** | 3×512 | — | **0.00885** | — |
| high | between-seed var of means | 3 | — | 0.00341 | — |

Fixed-policy (mean within-seed) ranking: **high > medium > low**. Pooled (policy+episode) ranking: high > medium > low.

Note: pooled variance mixes within-seed (episode) variance with between-seed policy differences — it is *not* the registered quantity (the registered quantity is per-episode variance at fixed policy, i.e. the mean-within-seed row); the between-seed row shows how much of the pooled figure is seed-to-seed.

## Environment-level mechanism: burnt-fraction variance vs beta

Per-episode variance of burnt fraction from the Phase-2 calibration sweep (`phase2/calibration.npz`, hazard-only rollouts, L=64, 512 seeds per beta — no policy in the loop):

| severity | beta | mean burnt fraction | variance |
|---|---|---|---|
| low | 0.43 | 0.0185 | 0.0008 |
| medium | 0.49 | 0.1981 | 0.0354 |
| high | 0.70 | 0.9830 | 0.0019 |

The full curve peaks at beta = 0.53 (variance 0.0847), i.e. in the near-critical window just above the Medium lock and far from both the Low and High locks. At the three locked severities the environment-level variance ranks **medium >> high > low** (0.0354 vs 0.0019 vs 0.0008 — a 19-44x gap). **Def. 4's environment-level mechanism is CONFIRMED**: hazard-outcome variance is maximal near criticality.

Full curve (variance of burnt fraction, L=64, ddof=1):

| beta | variance | | beta | variance |
|---|---|---|---|---|
| 0.05 | 0.0000 | 0.51 | 0.0692 |
| 0.10 | 0.0000 | 0.52 | 0.0784 |
| 0.15 | 0.0000 | 0.53 | 0.0847 |
| 0.20 | 0.0000 | 0.54 | 0.0760 |
| 0.25 | 0.0000 | 0.55 | 0.0648 |
| 0.30 | 0.0000 | 0.56 | 0.0631 |
| 0.35 | 0.0000 | 0.57 | 0.0573 |
| 0.40 | 0.0002 | 0.58 | 0.0528 |
| 0.41 | 0.0003 | 0.59 | 0.0499 |
| 0.42 | 0.0005 | 0.60 | 0.0420 |
| 0.43 | 0.0008 | 0.65 | 0.0267 |
| 0.44 | 0.0014 | 0.70 | 0.0019 |
| 0.45 | 0.0030 | 0.75 | 0.0000 |
| 0.46 | 0.0058 | 0.80 | 0.0000 |
| 0.47 | 0.0106 | 0.85 | 0.0000 |
| 0.48 | 0.0200 | 0.90 | 0.0000 |
| 0.49 | 0.0354 | 0.95 | 0.0000 |
| 0.50 | 0.0544 |  | |

## Decomposition

As registered, the prediction is refuted / not confirmed: task-outcome variance at fixed policy does not peak at Medium (survival is monotone in severity; completion is a Medium-Low tie). The decomposition explains why without rescuing the registered claim: outcome variance ~ (environment variance) x (policy sensitivity to the environment). The environment factor peaks near criticality (Medium, table above), but the policy-sensitivity factor grows with severity — at Low the trained policy absorbs hazard fluctuations (survival ceiling), while at High every hazard realization couples into deaths and lost food. The two factors peak in different regimes, so the product need not peak at Medium.

## Verdict

- **survival_rate: REFUTED** — fixed-policy per-episode variance is monotone in severity (high > medium > low); High highest, not Medium.
- **completion: NOT CONFIRMED** — Medium ≈ Low within bootstrap CIs (0.01245 vs 0.01235), both above High; no resolvable Medium peak.
- **Environment-level mechanism (Def. 4): CONFIRMED** — burnt-fraction variance peaks near criticality (beta ≈ 0.53; medium >> high > low at the locked severities).

## Note for Phase 6 (seed budgeting)

High-severity between-seed variance is dominated by one seed (seed 2 trained to a distinctly better policy: completion 0.868 / survival 0.956 vs ~0.74/0.85 for seeds 0-1). Training-solution diversity at High severity is real and large relative to episode noise — an input for the Phase-6 seed budget: High-severity cells need more seeds (or explicit solution-diversity reporting) for trustworthy means.
