# Provenance: sections/18_appendix_secondary.md

Writer: W4 (Paper v3, step 4, 2026-10-14). Checked against the section on 2026-10-14.
v2 sources: `paper/v2/sections/14_appendix_plan_provenance.md` (Appendix H) and
`paper/v2/sections/09_compositional_test.md` §9.2 (mediation, the replicate rows).

Word counts (`paper/v3/src/wordcount.py`): see the hand-back; budget about 400
prose words plus tables.

| # | sentence (verbatim) | support | change from v2, and why |
|---|---|---|---|
| 1 | F The secondary design | framing | edited: v2 'H The secondary design' re-lettered F (STRUCTURE §2) |
| 2 | Everything here is secondary and non-verdict-bearing, with 95 % intervals bootstrapped over seeds within arm (B = 2000), conditional on the common evaluation draw and not family-corrected. | DX-28; docs/decision_log.md:5072-5074; che/bench/results/phase6/secondary/secondary.md:5 | edited from paper/v2/sections/14_appendix_plan_provenance.md:154: 'non-verdict-bearing' added (registered string, stub) |
| 3 | Each secondary arm has k = 20 seeds, trained on the GPU that ran Γ (Appendix D) with communication denial off in every component. | DES-13; DX-5; X4-2 | edited from paper/v2/sections/14_appendix_plan_provenance.md:154; fix round, RC2-13: 'GPU 1' made 'the GPU that ran Γ' (numbered GPUs only in App. D) |
| 4 | Write μ for the per-coupling frequency (equal for the two couplings in every arm here), p for the co-occurrence and ν for the fire-only share, as in §6.2. | DES-9; paper/v3/BRIEF.md:176-179 (glossary) | new: μ, p, ν defined here as the stub asks (BRIEF §5.2) |
| 5 | On the triangle of training mixtures $\nu = 1 - 2\mu + p$, so the active share is $1 - \nu = 2\mu - p$. | DES-9; X4-1 | edited from paper/v2/sections/14_appendix_plan_provenance.md:154 ('the triangle gives ν = 1 − 2μ + p'); the active share added (X4-1) |
| 6 | Figure 7 prints μ as m and ν as n; the arm names below are the labels of its table view. | paper/figures/interactive/MANIFEST.md:278-280 (axes p, n; lines m) | edited from paper/v2/sections/14_appendix_plan_provenance.md:154 and paper/v2/sections/09_compositional_test.md:116 (m, n labels) |
| 7 | arm / p / active share / survival / completion | framing | edited: header with the active-share column (X4-1) |
| 8 | sweep_c50_p000 / 0.5 / 0 / 0 / 1 / 0.9241 / 0.7847 | DES-9; DX-28; X4-1 | kept from paper/v2/sections/14_appendix_plan_provenance.md:158, active share added |
| 9 | sweep_c50_p125 / 0.5 / 0.125 / 0.125 / 0.875 / 0.9249 / 0.7775 | DES-9; DX-28; X4-1 | kept from paper/v2/sections/14_appendix_plan_provenance.md:159, active share added |
| 10 | sweep_c50_p250 / 0.5 / 0.25 / 0.25 / 0.75 / 0.9261 / 0.7797 | DES-9; DX-28; X4-1 | kept from paper/v2/sections/14_appendix_plan_provenance.md:160, active share added |
| 11 | sweep_c50_p375 / 0.5 / 0.375 / 0.375 / 0.625 / 0.9264 / 0.7656 | DES-9; DX-28; X4-1 | kept from paper/v2/sections/14_appendix_plan_provenance.md:161, active share added |
| 12 | sweep_c50_p500 / 0.5 / 0.5 / 0.5 / 0.5 / 0.9289 / 0.7749 | DES-9; DX-28; X4-1 | kept from paper/v2/sections/14_appendix_plan_provenance.md:162, active share added |
| 13 | ident_c40_p000 / 0.4 / 0 / 0.2 / 0.8 | DES-9; DX-28; X4-1 | kept from paper/v2/sections/14_appendix_plan_provenance.md:163, active share added (no arm means are ledgered for the identification arms) |
| 14 | ident_c40_p200 / 0.4 / 0.2 / 0.4 / 0.6 | DES-9; DX-28; X4-1 | kept from paper/v2/sections/14_appendix_plan_provenance.md:164, active share added |
| 15 | ident_c40_p400 / 0.4 / 0.4 / 0.6 / 0.4 | DES-9; DX-28; X4-1 | kept from paper/v2/sections/14_appendix_plan_provenance.md:165, active share added |
| 16 | ISO-4 (second GPU) / 0.5 / 0 / 0 / 1 / 0.9256 / 0.7726 | DES-14; DX-18; HW-4 | kept from v2 App. H with active share added; fix round, RC2-13: 'GPU 2' made 'second GPU' |
| 17 | The p = 0 sweep arm carries exactly ISO-4's training mixture. | docs/decision_log.md:5043-5045 | kept from paper/v2/sections/14_appendix_plan_provenance.md:168 |
| 18 | Along the sweep, μ stays fixed while p and ν rise together, so the active share falls as co-occurrence rises; along the identification line the same holds 0.2 lower in active share. | DES-9; X4-1 | new: what the active-share column shows (V3-F4) |
| 19 | estimate (points) / survival / completion | framing | kept (paper/v2/sections/14_appendix_plan_provenance.md:170) |
| 20 | sweep slope per unit p (labelled “dose slope”; separate fit) / +0.89 [−0.33, +2.11] / −2.51 [−9.43, +4.12] | SEC-5; DX-27 | kept (paper/v2/sections/14_appendix_plan_provenance.md:172); 'dose slope' stays inside the figure-label phrase (appendix) |
| 21 | sweep endpoint, p = 0.5 minus p = 0 / +0.48 [−0.21, +1.17] / −0.97 [−4.82, +2.87] | SEC-5; DX-27 | kept (paper/v2/sections/14_appendix_plan_provenance.md:173) |
| 22 | γ p, the co-occurrence slope, per unit p / +3.26 [+1.37, +5.02] / +2.69 [−6.75, +12.45] | SEC-1; DX-27 | kept (paper/v2/sections/14_appendix_plan_provenance.md:174) |
| 23 | γ n, the fire-only-share slope, per unit ν / −2.37 [−4.19, −0.57] / −6.52 [−15.34, +2.42] | SEC-1; DX-27 | kept (paper/v2/sections/14_appendix_plan_provenance.md:175) |
| 24 | bound, 0.5 γ n / −1.19 [−2.10, −0.28] / −3.26 [−7.67, +1.21] | SEC-2; DX-27 | kept (paper/v2/sections/14_appendix_plan_provenance.md:176) |
| 25 | change point in p (labelled “knee”) / 0.375 [0.125, 0.375], UNDERPOWERED / 0.375 [0.125, 0.375], UNDERPOWERED | DX-28; SEC-6 | kept (paper/v2/sections/14_appendix_plan_provenance.md:177) |
| 26 | plane prediction of JOINT − ISO-4 (γ p × 1) / §6.3 / +2.69; γ p 's interval contains both measured values | DX-417; DX-27; RES-6; RES-8 | kept (paper/v2/sections/14_appendix_plan_provenance.md:178; '§9.2' made '§6.3') |
| 27 | The plane $y = \gamma_0 + \gamma_p p + \gamma_n \nu$ is a seed-level ordinary least squares (OLS) fit over all eight arms; $\gamma_p$ is the co-occurrence slope and $\gamma_n$ the fire-only-share slope. | docs/decision_log.md:5030-5034, :5084-5087; che/bench/results/phase6/secondary/secondary.md:41 | edited from paper/v2/sections/14_appendix_plan_provenance.md:180: the slopes' plain names attached to the symbols (stub: define γ_p, γ_n here) |
| 28 | The bound, the fire-only share's part of the sweep's endpoint change, excludes zero on survival. | SEC-2; che/bench/results/phase6/secondary/secondary.md:41 | edited from paper/v2/sections/14_appendix_plan_provenance.md:180 (split) |
| 29 | The sweep slope is a separate seed-level OLS fit over the five sweep arms, with an isotonic fit by the pool-adjacent-violators algorithm (PAVA) giving its monotone shape. | docs/decision_log.md:5016-5019 | edited from paper/v2/sections/14_appendix_plan_provenance.md:180: PAVA spelled out (stub: define PAVA) |
| 30 | The plane's slope along the sweep is $\gamma_p + \gamma_n$, so the two need not agree, and on completion they do not. | docs/decision_log.md:5030-5032; DX-27; SEC-5 | kept (paper/v2/sections/14_appendix_plan_provenance.md:180) |
| 31 | The change point is the breakpoint of the best single-hinge fit. | docs/decision_log.md:5021-5023 | kept (paper/v2/sections/14_appendix_plan_provenance.md:180) |
| 32 | Linearity is assumed and checked only coarsely: arm-mean residuals lie within ±0.4 SE on survival and ±1.1 SE on completion, 8 points for 3 parameters. | DX-39 | kept (paper/v2/sections/14_appendix_plan_provenance.md:180) |
| 33 | Because $1 - \nu = 2\mu - p$, a step in $\gamma_p$'s direction at fixed ν moves μ by half as much as p, and a step in $\gamma_n$'s direction at fixed p moves μ too. | DES-9 | new: the derivation behind 'the plane separates co-occurrence from the active share only' (μ = (1 + p − ν)/2, DES-9; BRIEF §9.2 trap 2) |
| 34 | Per-coupling frequency, co-occurrence and active share cannot all be held fixed on the triangle, so the plane separates co-occurrence from the active share only. | che/bench/results/phase6/secondary/secondary.md:60; DX-306; X4-1 | edited from paper/v2/sections/14_appendix_plan_provenance.md:182 ('Per-coupling frequency, co-occurrence and active share cannot all be held fixed on the triangle'): the consequence stated in the ruled form (V3-F4) |
| 35 | The same-GPU replicate of the correction subtracts the p = 0 sweep arm from JOINT, both trained on the GPU that ran Γ (§6.3): | RES-8; DX-5; docs/decision_log.md:5043-5047 | new; fix round, RC2-13: 'GPU 1' made 'the GPU that ran Γ' |
| 36 | contrast / k / completion / survival / level | framing | new (table header) |
| 37 | Γ₄′ = JOINT − the p = 0 sweep arm / 72 / 20 / −2.47 [−6.16, +1.22], z −1.50 / +0.13 [−0.56, +0.81], z +0.41 / Šidák-corrected 95 % | DES-3; DES-13; RES-8; DX-19 | new row (v2 §9.2 table, paper/v2/sections/09_compositional_test.md:82), z values kept here |
| 38 | replicate difference: the p = 0 sweep arm − ISO-4 / 20 / 20 / +1.21 [−2.79, +5.20] / −0.15 [−0.86, +0.56] / 95 %, across GPUs | DES-13; DX-19; RES-9 | new row (v2 §9.2 table, paper/v2/sections/09_compositional_test.md:84) |
| 39 | The replicate is reported beside the registered Γ₄ and cannot change its reading. | docs/decision_log.md:5045-5050 ('Neither may change the registered Γ₄ qualifier'); che/bench/results/phase6/secondary/secondary.md:55 | new: S5's rule |
| 40 | Mediation is VOID. | SEC-7 | edited from paper/v2/sections/09_compositional_test.md:127 ('Mediation is VOID'): moved to its appendix home (stub) |
| 41 | The registered mediator, the counter's realized count during training, had a first-stage slope on p of −1.03 × 10⁻⁵, 95 % [−2.91 × 10⁻⁵, +0.93 × 10⁻⁵], and a rule fixed before the sweep was read voids the analysis when that interval contains zero (Appendix D). | DX-29; DX-414; docs/decision_log.md:5099-5108 | kept from paper/v2/sections/09_compositional_test.md:127, merged; 'Appendix D' points to the quoted rule |
| 42 | Diagnosed after the run, with the rule unchanged: the counter counts collapse-seeded ignitions inside an alive agent's crop, which only Coupling A produces. | CO-4; che/env/env.py:398-404 | kept from paper/v2/sections/09_compositional_test.md:127 |
| 43 | In these mixtures it measures the Coupling-A frequency that the sweep holds fixed, and it cannot register co-occurrence. | CO-4; DX-306; che/bench/results/phase6/secondary/secondary.md:62 | edited from paper/v2/sections/09_compositional_test.md:127 ('In mixtures it measures the Coupling-A frequency that the sweep holds fixed and is blind to co-occurrence'): 'blind to' made 'cannot register' (C25's pattern is reserved for §6.4's home) |
| 44 | Floors exist only for the sweep's p = 0.5 arm: the other sweep arms assume that floor, and the identification arms are ungraded. | DX-306 | kept (paper/v2/sections/14_appendix_plan_provenance.md:182) |
| 45 | The counter's realized count is endogenous, so nothing here is its causal effect. | DX-306; che/bench/results/phase6/secondary/secondary.md:62 | edited from paper/v2/sections/14_appendix_plan_provenance.md:182: the VOID pointer moved up (mediation now stated here) |

## Findings

None beyond those in `provenance/06_example_design.md` and
`provenance/07_example_results.md`.

## Alternates

None.
