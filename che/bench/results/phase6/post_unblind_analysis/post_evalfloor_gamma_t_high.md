# Phase-6 POST-UNBLIND analysis

git `c36cf51941c82f7926292c06080eb99aba004bc3` (dirty files: 0) · 2026-09-26T22:38:19+00:00 · sections: evalfloor, gamma_t, high

Šidák m = 2, z_α = 2.2365, as the family. Every interval is CONDITIONAL on its common eval draw (seed 0, 512 episodes). Nothing here decides or relabels a branch.

## Eval floor — A-vs-A on the post-unblind card, and cross-unit

deterministic on this card: **True** · identical to the grid's own eval: **True**

| checkpoint | metric | reps identical | rep sd | cross-unit identical | mean(reps) − grid |
|---|---|---|---|---|---|
| iso_s1 | completion | True | 0.00e+00 | True | +0.00e+00 |
| iso_s1 | survival_rate | True | 0.00e+00 | True | +0.00e+00 |
| joint_s1 | completion | True | 0.00e+00 | True | +0.00e+00 |
| joint_s1 | survival_rate | True | 0.00e+00 | True | +0.00e+00 |

Blind to: two checkpoints only; the grid card's own eval self-floor is unmeasured (that box is gone), so a cross-unit difference cannot be assigned to either unit.

## Γ(t) — final half, REQUIRED robustness evidence

### completion: **UNSTABLE: the sign of Γ is still moving over the final half — that instability IS the finding (T* ruling item 3)**

| t | Γ(t) | sd(Γ) | Šidák CI |
|---|---|---|---|
| 500 | +0.0017 | 0.00321 | [-0.0055, +0.0089] |
| 550 | -0.0017 | 0.00353 | [-0.0096, +0.0062] |
| 600 | +0.0018 | 0.00362 | [-0.0063, +0.0099] |
| 650 | +0.0015 | 0.00481 | [-0.0093, +0.0122] |
| 700 | -0.0037 | 0.00470 | [-0.0142, +0.0068] |
| 750 | -0.0147 | 0.00610 | [-0.0283, -0.0010] |
| 800 | -0.0035 | 0.00677 | [-0.0187, +0.0116] |
| 850 | -0.0053 | 0.00729 | [-0.0216, +0.0110] |
| 900 | -0.0039 | 0.00843 | [-0.0228, +0.0149] |
| 950 | -0.0016 | 0.01021 | [-0.0245, +0.0212] |
| 1000 | -0.0173 | 0.01068 | [-0.0412, +0.0066] |

signs + - + + - - - - - - -; disagreeing with T*: [500, 600, 650]; Šidák CI excludes 0 at 1/11 points (descriptive — the rule reads signs only).

### survival_rate: **UNSTABLE: the sign of Γ is still moving over the final half — that instability IS the finding (T* ruling item 3)**

| t | Γ(t) | sd(Γ) | Šidák CI |
|---|---|---|---|
| 500 | +0.0022 | 0.00228 | [-0.0029, +0.0073] |
| 550 | -0.0037 | 0.00220 | [-0.0086, +0.0013] |
| 600 | -0.0027 | 0.00232 | [-0.0078, +0.0025] |
| 650 | +0.0011 | 0.00242 | [-0.0043, +0.0065] |
| 700 | +0.0031 | 0.00235 | [-0.0021, +0.0084] |
| 750 | +0.0036 | 0.00255 | [-0.0021, +0.0093] |
| 800 | +0.0020 | 0.00232 | [-0.0032, +0.0072] |
| 850 | +0.0018 | 0.00234 | [-0.0034, +0.0071] |
| 900 | +0.0056 | 0.00231 | [+0.0004, +0.0108] |
| 950 | +0.0083 | 0.00219 | [+0.0034, +0.0132] |
| 1000 | +0.0096 | 0.00216 | [+0.0047, +0.0144] |

signs + - - + + + + + + + +; disagreeing with T*: [550, 600]; Šidák CI excludes 0 at 3/11 points (descriptive — the rule reads signs only).

### Cross-card check at T* — post card − grid card, paired by seed (ruling viii, descriptive)

| metric | arm | identical | mean Δ (se) | max \|Δ\| |
|---|---|---|---|---|
| completion | iso | 70/72 | +1.70e-06 (3.81e-06) | 2.44e-04 |
| completion | joint | 70/72 | -2.54e-06 (1.88e-06) | 1.22e-04 |
| completion | JOINT − ISO | | -4.24e-06 (4.24e-06) | |
| survival_rate | iso | 69/72 | -6.78e-06 (3.86e-06) | 1.63e-04 |
| survival_rate | joint | 71/72 | +2.26e-06 (2.26e-06) | 1.63e-04 |
| survival_rate | JOINT − ISO | | +9.04e-06 (4.42e-06) | |

- completion: single-card curve signs + - + + - - - - - - - → NOT stable (descriptive; the rule above reads the grid's own T* eval). Γ at T* on the post card: -0.0173.
- survival_rate: single-card curve signs + - - + + + + + + + + → NOT stable (descriptive; the rule above reads the grid's own T* eval). Γ at T* on the post card: +0.0096.

Blind to: t < 1000 is evaluated on the post-unblind card, t = 1000 is the grid's own eval — read with the eval floor and the cross-card check above.

## High readout — Γ_H at β = 0.70 (§7 proposal 3, out of family)

| contrast | a | b | Γ = b − a | sd(Γ) | z | decision | Šidák CI | X (MDE80) |
|---|---|---|---|---|---|---|---|---|
| Γ_H completion | 0.8027 (k=72) | 0.7948 (k=72) | -0.0079 | 0.01105 | -0.71 | null | [-0.0326, +0.0168] | 0.0340 |
| Γ_H,4 completion | 0.8024 (k=20) | 0.7948 (k=72) | -0.0075 | 0.01392 | -0.54 | null | [-0.0387, +0.0236] | 0.0429 |
| Γ_H survival_rate | 0.8179 (k=72) | 0.8217 (k=72) | +0.0038 | 0.00826 | +0.46 | null | [-0.0146, +0.0223] | 0.0254 |
| Γ_H,4 survival_rate | 0.8345 (k=20) | 0.8217 (k=72) | -0.0128 | 0.00996 | -1.28 | null | [-0.0350, +0.0095] | 0.0307 |

- **completion: EXCLUSION** — a-fortiori EXCLUSION: no gap larger than X = 0.0340 at High even where JOINT trained on the evaluated configuration and ISO never saw a composed one. Never an absence.
  floor (8 reps, this card): seed/floor ISO 0.96×, JOINT 1.10×; Γ_H / floor sd(Γ) 0.73×. ISO-4: UNDERPOWERED for the beat-reproducibility hurdle (no rep set); graded on seed dispersion only.
- **survival_rate: EXCLUSION** — a-fortiori EXCLUSION: no gap larger than X = 0.0254 at High even where JOINT trained on the evaluated configuration and ISO never saw a composed one. Never an absence.
  floor (8 reps, this card): seed/floor ISO 2.74×, JOINT 1.26×; Γ_H / floor sd(Γ) 0.75×. ISO-4: UNDERPOWERED for the beat-reproducibility hurdle (no rep set); graded on seed dispersion only.

Blind to: NOT a held-out test (JOINT trained on this configuration at weight 1/2). Coupling A is marginal at High while B is live — the mirror of Medium; no severity has both couplings strongly live.
