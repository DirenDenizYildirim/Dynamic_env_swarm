# Phase-6 SECONDARY — dose sweep, identification arm, mediation

git `742c74c8ff6e029ce8751a4f2f4bfa91b41e4bd9` (dirty files: 0) · 2026-09-26T18:50:09+00:00

**NON-VERDICT-BEARING.** Nothing here enters the confirmatory family or moves a branch. Intervals are 95 %, bootstrap-over-seeds within arm (B = 2000, seed 20260926), conditional on the common eval draw.

| arm | m | p | no-element n |
|---|---|---|---|
| sweep_c50_p000 | 0.5 | 0.0 | 0.000 |
| sweep_c50_p125 | 0.5 | 0.125 | 0.125 |
| sweep_c50_p250 | 0.5 | 0.25 | 0.250 |
| sweep_c50_p375 | 0.5 | 0.375 | 0.375 |
| sweep_c50_p500 | 0.5 | 0.5 | 0.500 |
| ident_c40_p000 | 0.4 | 0.0 | 0.200 |
| ident_c40_p200 | 0.4 | 0.2 | 0.400 |
| ident_c40_p400 | 0.4 | 0.4 | 0.600 |

## completion

| p | 0.0 | 0.125 | 0.25 | 0.375 | 0.5 |
|---|---|---|---|---|---|
| mean | 0.7847 | 0.7775 | 0.7797 | 0.7656 | 0.7749 |
| isotonic (nonincreasing) | 0.7847 | 0.7786 | 0.7786 | 0.7703 | 0.7703 |

- dose trend: OLS slope -0.0251 per unit p, 95 % CI [-0.0943, +0.0412]; isotonic SSE 4.56e-05 vs opposite 1.98e-04
- endpoint p=0.5 − p=0: -0.0097 [-0.0482, +0.0287]; 1.57× the floor-basis SE (sweep_p500 floor ASSUMED COMMON at p = 0 (flagged))
- knee κ = 0.375, 95 % CI [0.125, 0.375], bootstrap freq {'0.125': 0.313, '0.25': 0.318, '0.375': 0.369} UNDERPOWERED — the knee CI spans the sweep
- confound (both sweeps, y = γ0 + γ_p·p + γ_n·n): γ_p +0.0269 [-0.0675, +0.1245], γ_n -0.0652 [-0.1534, +0.0242]. **Bound:** the no-element confound's share of the sweep's endpoint change is -0.0326 [-0.0767, +0.0121]
- linearity check, arm mean − plane (in SE units): c50_p000 -0.1, c50_p125 -0.3, c50_p250 +0.2, c50_p375 -0.5, c50_p500 +0.6, c40_p000 +0.1, c40_p200 +0.6, c40_p400 -1.1

## survival_rate

| p | 0.0 | 0.125 | 0.25 | 0.375 | 0.5 |
|---|---|---|---|---|---|
| mean | 0.9241 | 0.9249 | 0.9261 | 0.9264 | 0.9289 |
| isotonic (nondecreasing) | 0.9241 | 0.9249 | 0.9261 | 0.9264 | 0.9289 |

- dose trend: OLS slope +0.0089 per unit p, 95 % CI [-0.0033, +0.0211]; isotonic SSE 0.00e+00 vs opposite 1.33e-05
- endpoint p=0.5 − p=0: +0.0048 [-0.0021, +0.0117]; 1.17× the floor-basis SE (sweep_p500 floor ASSUMED COMMON at p = 0 (flagged))
- knee κ = 0.375, 95 % CI [0.125, 0.375], bootstrap freq {'0.125': 0.3205, '0.25': 0.3805, '0.375': 0.299} UNDERPOWERED — the knee CI spans the sweep
- confound (both sweeps, y = γ0 + γ_p·p + γ_n·n): γ_p +0.0326 [+0.0137, +0.0502], γ_n -0.0237 [-0.0419, -0.0057]. **Bound:** the no-element confound's share of the sweep's endpoint change is -0.0119 [-0.0210, -0.0028]
- linearity check, arm mean − plane (in SE units): c50_p000 +0.1, c50_p125 -0.0, c50_p250 +0.0, c50_p375 -0.4, c50_p500 +0.2, c40_p000 +0.1, c40_p200 -0.2, c40_p400 +0.1

## Mediation — realized training dose (co_active_per_step, updates 1…1000)

first stage slope -0.0000 per unit p, 95 % CI [-0.0000, +0.0000] → **VOID — realized dose does not vary with assigned p; the dose figure has no x-axis**

## Same-card replicate of the inert-share check (S5)

| metric | Γ₄' = JOINT − sweep_p000 (z_α) | sweep_p000 − ISO-4 (95 %) |
|---|---|---|
| completion | -0.0247 (z -1.50, null; Šidák CI [-0.0616, +0.0122]) | +0.0121 [-0.0279, +0.0520] |
| survival_rate | +0.0013 (z +0.41, null; Šidák CI [-0.0056, +0.0081]) | -0.0015 [-0.0086, +0.0056] |

Reported BESIDE the registered Γ₄; it cannot change the registered inert-share qualifier. A disagreement is reported, not resolved.

## What this instrument is blind to

- Linearity in (p, n) is an assumption; the arm-mean residuals above test it only coarsely (8 points, 3 parameters).
- Per-element marginal, co-occurrence and active-episode share cannot all be held fixed (the simplex); γ_p moves single-element mass into both-element episodes, which also raises per-element exposure.
- Floors exist only for sweep p = 0.5; intermediate points ASSUME it, the identification arm is UNGRADED.
- Realized dose is endogenous; nothing here is a causal effect of it.
