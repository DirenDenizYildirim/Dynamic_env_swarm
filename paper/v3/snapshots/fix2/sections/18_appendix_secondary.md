<!-- PAPER V3 DRAFT (PAPER V3 ruling, 2026-10-12): builder-drafted, not owner-approved -->

### F The secondary design

<!-- STUB-SPEC
JOB: The secondary design in full: arms (with code names as labels matching Figure 7), the sweep, the plane fit and its coarse linearity check, the same-GPU replicate table, mediation (VOID), and what that analysis could not see.
WRITER: W4.
BUDGET: about 400 prose words plus tables.
FROM: P1 §6.1 F; v2 Appendix H.
ROWS: DES-9, DX-28, SEC-1 to SEC-7, DX-27, DX-29, DX-306, DX-417, DX-39, RES-6, RES-7, RES-8, RES-9, DX-18, DX-19.
REGISTERED STRINGS: "non-verdict-bearing"; VOID (mediation); UNDERPOWERED (change points); "95 %, not family-corrected".
EVERY OTHER CAVEAT in checks/caveats.yaml: pointer only ("§6.3", "Appendix D"), never restated. C26: any sentence about the interaction check carries "post hoc".
NOT HERE: "the plane separates co-occurrence from frequency"; mediation as a finding.
V2 MATERIAL: paper/v2/sections/14_appendix_plan_provenance.md (H).
DEPENDENCIES: §6.3 points here.
-->

Everything here is secondary and non-verdict-bearing, with 95 % intervals bootstrapped over seeds within arm (B = 2000<!-- N:DX-28 -->), conditional on the common evaluation draw and not family-corrected. Each secondary arm has k = 20<!-- N:DES-13 --> seeds, trained on the GPU that ran Γ (Appendix D) with communication denial off in every component<!-- N:X4-2 -->. Write μ for the per-coupling frequency (equal for the two couplings in every arm here), p for the co-occurrence and ν for the fire-only share, as in §6.2. On the triangle of training mixtures $\nu = 1 - 2\mu + p$<!-- N:DES-9 -->, so the active share is $1 - \nu = 2\mu - p$<!-- N:X4-1 -->. Figure 7 prints μ as m and ν as n; the arm names below are the labels of its table view.

| arm | μ | p | ν | active share | survival | completion |
|---|---|---|---|---|---|---|
| `sweep_c50_p000` | 0.5<!-- N:DES-9 --> | 0<!-- N:DX-28 --> | 0<!-- N:DES-9 --> | 1<!-- N:X4-1 --> | 0.9241<!-- N:DX-28 --> | 0.7847<!-- N:DX-28 --> |
| `sweep_c50_p125` | 0.5<!-- N:DES-9 --> | 0.125<!-- N:DX-28 --> | 0.125<!-- N:DES-9 --> | 0.875<!-- N:X4-1 --> | 0.9249<!-- N:DX-28 --> | 0.7775<!-- N:DX-28 --> |
| `sweep_c50_p250` | 0.5<!-- N:DES-9 --> | 0.25<!-- N:DX-28 --> | 0.25<!-- N:DES-9 --> | 0.75<!-- N:X4-1 --> | 0.9261<!-- N:DX-28 --> | 0.7797<!-- N:DX-28 --> |
| `sweep_c50_p375` | 0.5<!-- N:DES-9 --> | 0.375<!-- N:DX-28 --> | 0.375<!-- N:DES-9 --> | 0.625<!-- N:X4-1 --> | 0.9264<!-- N:DX-28 --> | 0.7656<!-- N:DX-28 --> |
| `sweep_c50_p500` | 0.5<!-- N:DES-9 --> | 0.5<!-- N:DX-28 --> | 0.5<!-- N:DES-9 --> | 0.5<!-- N:X4-1 --> | 0.9289<!-- N:DX-28 --> | 0.7749<!-- N:DX-28 --> |
| `ident_c40_p000` | 0.4<!-- N:DES-9 --> | 0<!-- N:DX-28 --> | 0.2<!-- N:DES-9 --> | 0.8<!-- N:X4-1 --> | — | — |
| `ident_c40_p200` | 0.4<!-- N:DES-9 --> | 0.2<!-- N:DX-28 --> | 0.4<!-- N:DES-9 --> | 0.6<!-- N:X4-1 --> | — | — |
| `ident_c40_p400` | 0.4<!-- N:DES-9 --> | 0.4<!-- N:DX-28 --> | 0.6<!-- N:DES-9 --> | 0.4<!-- N:X4-1 --> | — | — |
| ISO-4 (second GPU) | 0.5<!-- N:DES-14 --> | 0<!-- N:DES-14 --> | 0<!-- N:DES-14 --> | 1<!-- N:DES-14 --> | 0.9256<!-- N:DX-18 --> | 0.7726<!-- N:DX-18 --> |

The p = 0 sweep arm carries exactly ISO-4's training mixture. Along the sweep, μ stays fixed while p and ν rise together, so the active share falls as co-occurrence rises; along the identification line the same holds 0.2<!-- N:DES-9 --> lower in active share.

| estimate (points) | survival | completion |
|---|---|---|
| sweep slope per unit p (labelled “dose slope”; separate fit) | +0.89 [−0.33, +2.11]<!-- N:SEC-5 --> | −2.51 [−9.43, +4.12]<!-- N:DX-27 --> |
| sweep endpoint, p = 0.5 minus p = 0 | +0.48 [−0.21, +1.17]<!-- N:SEC-5 --> | −0.97 [−4.82, +2.87]<!-- N:DX-27 --> |
| γ<sub>p</sub>, the co-occurrence slope, per unit p | +3.26 [+1.37, +5.02]<!-- N:SEC-1 --> | +2.69 [−6.75, +12.45]<!-- N:DX-27 --> |
| γ<sub>n</sub>, the fire-only-share slope, per unit ν | −2.37 [−4.19, −0.57]<!-- N:SEC-1 --> | −6.52 [−15.34, +2.42]<!-- N:DX-27 --> |
| bound, 0.5 γ<sub>n</sub> | −1.19 [−2.10, −0.28]<!-- N:SEC-2 --> | −3.26 [−7.67, +1.21]<!-- N:DX-27 --> |
| change point in p (labelled “knee”) | 0.375 [0.125, 0.375]<!-- N:DX-28 -->, UNDERPOWERED<!-- N:SEC-6 --> | 0.375 [0.125, 0.375]<!-- N:DX-28 -->, UNDERPOWERED<!-- N:SEC-6 --> |
| plane prediction of JOINT − ISO-4 (γ<sub>p</sub> × 1) | §6.3 | +2.69<!-- N:DX-417 -->; γ<sub>p</sub>'s interval contains both measured values |

The plane $y = \gamma_0 + \gamma_p p + \gamma_n \nu$ is a seed-level ordinary least squares (OLS) fit over all eight<!-- N:DX-28 --> arms; $\gamma_p$ is the co-occurrence slope and $\gamma_n$ the fire-only-share slope. The bound, the fire-only share's part of the sweep's endpoint change, excludes zero on survival. The sweep slope is a separate seed-level OLS fit over the five sweep arms, with an isotonic fit by the pool-adjacent-violators algorithm (PAVA) giving its monotone shape. The plane's slope along the sweep is $\gamma_p + \gamma_n$, so the two need not agree, and on completion they do not. The change point is the breakpoint of the best single-hinge fit. Linearity is assumed and checked only coarsely: arm-mean residuals lie within ±0.4 SE on survival and ±1.1 SE on completion, 8 points for 3 parameters<!-- N:DX-39 -->.

Because $1 - \nu = 2\mu - p$, a step in $\gamma_p$'s direction at fixed ν moves μ by half as much as p<!-- N:DES-9 -->, and a step in $\gamma_n$'s direction at fixed p moves μ too. Per-coupling frequency, co-occurrence and active share cannot all be held fixed on the triangle, so the plane separates co-occurrence from the active share only.

The same-GPU replicate of the correction subtracts the p = 0 sweep arm from JOINT, both trained on the GPU that ran Γ (§6.3):

| contrast | k | completion | survival | level |
|---|---|---|---|---|
| Γ₄′ = JOINT − the p = 0 sweep arm | 72 / 20<!-- N:DES-3 --><!-- N:DES-13 --> | −2.47 [−6.16, +1.22], z −1.50<!-- N:RES-8 --><!-- N:DX-19 --> | +0.13 [−0.56, +0.81], z +0.41<!-- N:RES-8 --> | Šidák-corrected 95 % |
| replicate difference: the p = 0 sweep arm − ISO-4 | 20 / 20<!-- N:DES-13 --> | +1.21 [−2.79, +5.20]<!-- N:DX-19 --> | −0.15 [−0.86, +0.56]<!-- N:RES-9 --> | 95 %, across GPUs |

The replicate is reported beside the registered Γ₄ and cannot change its reading.

Mediation is VOID<!-- N:SEC-7 -->. The registered mediator, the counter's realized count during training, had a first-stage slope on p of −1.03 × 10⁻⁵, 95 % [−2.91 × 10⁻⁵, +0.93 × 10⁻⁵]<!-- N:DX-29 -->, and a rule fixed before the sweep was read voids the analysis when that interval contains zero (Appendix D). Diagnosed after the run, with the rule unchanged: the counter counts collapse-seeded ignitions inside an alive agent's crop<!-- N:CO-4 -->, which only Coupling A produces. In these mixtures it measures the Coupling-A frequency that the sweep holds fixed, and it cannot register co-occurrence.

Floors exist only for the sweep's p = 0.5 arm: the other sweep arms assume that floor, and the identification arms are ungraded<!-- N:DX-306 -->. The counter's realized count is endogenous, so nothing here is its causal effect.
