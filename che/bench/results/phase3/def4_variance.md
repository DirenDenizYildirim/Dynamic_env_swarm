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
| low | **pooled** | 1536 | 0.7369 | **0.01328** | [0.01240, 0.01418] |
| low | mean within-seed (fixed policy) | 3×512 | — | 0.01235 | — |
| low | between-seed var of means | 3 | — | 0.00141 | — |
| medium | seed 0 | 512 | 0.7889 | 0.01064 | [0.00923, 0.01217] |
| medium | seed 1 | 512 | 0.7376 | 0.01377 | [0.01203, 0.01547] |
| medium | seed 2 | 512 | 0.7583 | 0.01293 | [0.01142, 0.01452] |
| medium | **pooled** | 1536 | 0.7616 | **0.01288** | [0.01194, 0.01381] |
| medium | mean within-seed (fixed policy) | 3×512 | — | 0.01245 | — |
| medium | between-seed var of means | 3 | — | 0.00067 | — |
| high | seed 0 | 512 | 0.7858 | 0.00984 | [0.00857, 0.01115] |
| high | seed 1 | 512 | 0.7357 | 0.01305 | [0.01146, 0.01471] |
| high | seed 2 | 512 | 0.8681 | 0.00891 | [0.00779, 0.01006] |
| high | **pooled** | 1536 | 0.7965 | **0.01356** | [0.01259, 0.01456] |
| high | mean within-seed (fixed policy) | 3×512 | — | 0.01060 | — |
| high | between-seed var of means | 3 | — | 0.00447 | — |

Pooled-variance ranking: high > low > medium. **Prediction REFUTED (high highest, not Medium).**

Mean-within-seed (fixed-policy) ranking: medium > low > high.

Note: pooled variance mixes within-seed (episode) variance with between-seed policy differences; the between-seed row above shows how much of the pooled figure is seed-to-seed. The mean-within-seed row is the cleanest fixed-policy statistic.

## survival_rate

| severity | scope | N | mean | variance | 95% CI |
|---|---|---|---|---|---|
| low | seed 0 | 512 | 0.9906 | 0.00100 | [0.00064, 0.00142] |
| low | seed 1 | 512 | 0.9930 | 0.00094 | [0.00047, 0.00155] |
| low | seed 2 | 512 | 0.9940 | 0.00079 | [0.00037, 0.00137] |
| low | **pooled** | 1536 | 0.9925 | **0.00091** | [0.00066, 0.00121] |
| low | mean within-seed (fixed policy) | 3×512 | — | 0.00091 | — |
| low | between-seed var of means | 3 | — | 0.00000 | — |
| medium | seed 0 | 512 | 0.9652 | 0.00490 | [0.00369, 0.00630] |
| medium | seed 1 | 512 | 0.9631 | 0.00498 | [0.00399, 0.00601] |
| medium | seed 2 | 512 | 0.9342 | 0.01138 | [0.00909, 0.01394] |
| medium | **pooled** | 1536 | 0.9542 | **0.00728** | [0.00630, 0.00840] |
| medium | mean within-seed (fixed policy) | 3×512 | — | 0.00709 | — |
| medium | between-seed var of means | 3 | — | 0.00030 | — |
| high | seed 0 | 512 | 0.8638 | 0.01121 | [0.00973, 0.01279] |
| high | seed 1 | 512 | 0.8483 | 0.01171 | [0.01034, 0.01318] |
| high | seed 2 | 512 | 0.9562 | 0.00364 | [0.00312, 0.00416] |
| high | **pooled** | 1536 | 0.8894 | **0.01111** | [0.01025, 0.01199] |
| high | mean within-seed (fixed policy) | 3×512 | — | 0.00885 | — |
| high | between-seed var of means | 3 | — | 0.00341 | — |

Pooled-variance ranking: high > medium > low. **Prediction REFUTED (high highest, not Medium).**

Mean-within-seed (fixed-policy) ranking: high > medium > low.

Note: pooled variance mixes within-seed (episode) variance with between-seed policy differences; the between-seed row above shows how much of the pooled figure is seed-to-seed. The mean-within-seed row is the cleanest fixed-policy statistic.

## Verdict

- completion: REFUTED on pooled variance (ranking high > low > medium); fixed-policy (mean within-seed) ranking medium > low > high.
- survival_rate: REFUTED on pooled variance (ranking high > medium > low); fixed-policy (mean within-seed) ranking high > medium > low.
