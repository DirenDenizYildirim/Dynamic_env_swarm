# Severity Lock — M2.4 decision record

Date: 2026-07-19. Decided jointly (owner + RA) from the raw M2.1/M2.2
calibration data (`calibration.npz` @ 5129c53, `calibration_crossing.npz`
@ 206b024; 512 seeds, L ∈ {32,48,64}), independently recomputed by the RA.

## Critical point — LOCKED: β̂_c = 0.500 ± 0.005

| Estimator | Value | Note |
|---|---|---|
| R_L logistic centers (32/48/64) | 0.4985 / 0.5006 / 0.4999 | L-independent; the pivot |
| Fit-based R_L pairwise crossings | 0.498–0.507 | ill-conditioned (curves coincident) — consistent |
| ½-locus of P_span, L^(−3/4) extrapolation | 0.5127 | scaling-correction limited (3 sizes) |
| ½-locus of P_span, 1/L extrapolation | 0.5037 | sensitivity fit |
| Steepest slope, L=64 | 0.480 | known downward bias for center seed |
| Self-duality check R_L(0.500) | 0.488 / 0.502 / 0.494 | all within 1σ of the exact ½ |

The idealized kernel's exact β_c = 1/2 (Kesten) is reproduced to three
decimal places by the crossing family, and the parameter-free self-duality
value R(β_c) = ½ holds at all three sizes. **The CA port is quantitatively
validated.** χ̂(β) rises ~17× from β = 0.30 to its censoring point
(effective exponent ≈ 1.6 in the accessible window; asymptotic γ = 43/18
not reachable at L = 64 — reported honestly, not claimed).

## Bands — LOCKED (L = 64, horizon 256, agent speed 1)

| Severity | β | Measured observables (512 seeds) | Regime / spec band |
|---|---|---|---|
| **Low** | **0.43** | P_span = 0.021, burnt fraction = 1.9 % | subcritical; spec: P_span<0.05 ∧ bf∈[1,5]% ✓ |
| **Medium** | **0.49** | P_span = 0.547, burnt fraction = 19.8 % | near-critical; spec: P_span∈[0.3,0.7] ✓; sits between the finite-size pseudo-critical point β_c(64) ≈ 0.486 and β̂_c = 0.500 — the arena's own maximal-fluctuation regime |
| **High** | **0.70** | v̂ = 0.83 cells/step, burnt fraction = 98.3 %, P_span = 0.998 | supercritical race; spec: v̂∈[0.5,1.0] ✓; fronts at 83 % of agent speed — outrunnable, barely |

Rationale notes: Medium is deliberately at 0.49 rather than 0.50 because
"near-critical" for a finite arena means correlation length ~ L, which the
finite-size pseudo-critical point locates; 0.49 also centers the P_span
spec band. High at 0.70 leaves headroom below v̂ = 1 so escape is possible
in principle (v̂ = 0.83); note ~98 % of the arena eventually burns — High
is an evacuation-while-foraging regime by construction.

## Instructions to Claude Code (M2.4 completion)

Emit `che/configs/severity_{low,medium,high}.yaml` with β ∈
{0.43, 0.49, 0.70}, provenance comments quoting this file, the calibration
npz hashes, and the measured observables above. M2.3's unit-test band
[0.42, 0.58] is confirmed satisfied (β̂_c = 0.500) — no test changes.
Then proceed to M2.5 (18-run grid) unchanged.
