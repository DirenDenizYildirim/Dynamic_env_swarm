# Provenance: sections/14_appendix_plan_provenance.md

Writer: W6. Checked against the section on 2026-10-11 (step 4, pass 1) and on 2026-10-12 after the pass-3 fixes and the step-4.3 re-check items.
`log` = `docs/decision_log.md`; `FB` = `phase6_framing_branches.md`.
"Demo" is `paper/demo_beyond/sections/12_appendix.md` (its Appendices D–J).
Every quotation in Appendix D was compared with its source this session at
the lines given. The sentence column is the checker's normalized form.

Word counts (P3's method, verbatim quotations and tables excluded), after
the re-check items: D 248, E 63, F 260, G 84, H 230, I 82 prose words, 967 in all
against about 850 (+14 %); Appendix D's quotations are 563 words; captions I1 and I2 within
the 60-word cap each, notes included.

| # | sentence (verbatim) | support | change from the demo, and why |
|---|---|---|---|
| 1 | D The frozen analysis plan | framing | kept |
| 2 | The registered constants are in Appendix B. The reading rules follow, quoted from the registration record with their dates: emphasis is the record's own, one indented code line is set inline, and omissions are marked […]. | framing; DES-13 (held in Appendix B) | edited (demo 12:106): the constants' list removed, pointing to Appendix B (N16); "S1–S6" explained, since they stay verbatim inside the quotation (class A, F5) |
| 3 | A "§" inside a quotation refers to the record's own sections, and S1–S6 are its labels for the secondary analyses. | framing | kept |
| 4 | 1. | framing | kept |
| 5 | The estimand (T\ ruling, item 2, 2026-08-11): | METH-6; decision log, T* RULING (docs/decision_log.md:2975) | edited: label shortened |
| 6 | Primary Γ = the confirmatory contrast at MATCHED BUDGET T = 1000, all arms — registered as a fixed-budget claim. | docs/decision_log.md:2977-2978 | kept (verbatim quotation; demo 12:110) |
| 7 | "At convergence" is explicitly NOT claimed anywhere. | docs/decision_log.md:2980 | kept (verbatim quotation; demo 12:112) |
| 8 | The paper says "at matched compute" throughout, which is also the practitioner-relevant question. […] | docs/decision_log.md:2980-2982 | kept (verbatim quotation; demo 12:112); pass 3: RC2-28: trailing "[…]" added (the source paragraph continues) |
| 9 | 2. | framing | kept |
| 10 | Budget robustness (item 3 of the same ruling; restated for every branch on 2026-08-13): | decision log, T* RULING (docs/decision_log.md:2986); DES-12; phase6_framing_branches.md:3 | edited: label shortened |
| 11 | The fixed-budget conclusion is reported as budget-robust iff the sign of Γ is stable over the final half of training. | docs/decision_log.md:2991-2992 | kept (verbatim quotation; demo 12:116) |
| 12 | If the sign is still moving at T, that instability IS the finding and is reported as such. | docs/decision_log.md:2992-2993 | kept (verbatim quotation; demo 12:116) |
| 13 | Mechanism: 11 retained checkpoints, updates 500–1000 at interval 50, confirmatory arms only, evaluated post-unblind. | phase6_framing_branches.md:240-241 | kept (verbatim quotation; demo 12:118) |
| 14 | Every branch above gains "— budget-robust" or "— sign unstable over the final half" as a suffix, and the suffix is not optional. | phase6_framing_branches.md:241-243 | kept (verbatim quotation; demo 12:118) |
| 15 | 3. | framing | kept |
| 16 | The branch-B falsifier (2026-08-13): | DES-12; phase6_framing_branches.md:155 | kept |
| 17 | Branch B is claimable only if the completion contrast excludes an effect as large, in standardized units, as the observed survival effect: \|z_c\| + z_α < \|z_s\|, z = Γ / sd(Γ) per metric with sd(Γ) the grid's own measured per-arm seed dispersion in the combined form and z_α = 2.2365 the two-sided Šidák critical value at m = 2. | phase6_framing_branches.md:160-166 | kept (verbatim quotation; demo 12:122-126) |
| 18 | If it fails, the result is branch C with an asymmetry the design could not resolve — not branch B. | phase6_framing_branches.md:166-168 | kept (verbatim quotation; demo 12:126) |
| 19 | 4. | framing | new |
| 20 | Test variance and floor (the frozen analysis plan, amended 2026-08-13): | V6-5; phase6_design_v2.md:340-344 | new: the rule behind §9.1's "floors serve only …" (design-stage power moved from §9.1, LEN); pass 3: RN2-24: the date's tag is now V6-5 (the plan's 2026-08-13 amendment), not DES-12 (the branch registration) |
| 21 | The confirmatory tests and CIs are computed on the GRID'S OWN measured per-arm seed dispersion, not on the floors. | phase6_design_v2.md:346-347 | new (verbatim quotation) |
| 22 | The floors are 8 identical reps at one seed; the grid averages over k distinct seeds, and those are different variances. | phase6_design_v2.md:347-349; DX-403 | new (verbatim quotation) |
| 23 | The floors keep exactly two narrower roles: the beat-reproducibility hurdle, and a design-stage power basis registered as an UPPER BOUND (§5, superseded note, item 2). […] | phase6_design_v2.md:349-351 | new (verbatim quotation; "beat-reproducibility hurdle" stays verbatim inside it); pass 3: RC2-28: trailing "[…]" added |
| 24 | Design-stage power is therefore a ceiling. | phase6_design_v2.md:350-351 | edited (demo 09:45 "Floors come from identical runs at one seed and seed dispersion only adds to them, so floor-based power is a ceiling, registered as one"); moved from §9.1 (LEN) |
| 25 | On the grid's launch floor study (an RTX PRO 6000, 2026-08-10), the design-stage MDE₈₀ at k = 40 was 1.55 completion and 0.95 survival points. | DES-5 | edited (pass 1, moved from demo 09:45); pass 3: RC2-1 and RN2-3 (MUST; orchestrator decision 1): "The first floor study" becomes "the grid's launch floor study (2026-08-10)"; RC2-27: split, "design-stage" added |
| 26 | On the floors of GPU 1, design-stage completion power at a 0.03 effect was 72.2 % at k = 60 and 80.4 % at k = 72; §9.1 gives the realized power. | DES-4; DES-6 | edited; pass 3, RC2-27: split; "the grid GPU's floors" becomes "the floors of GPU 1"; "§9.1 gives the realized power" added so the design-stage figures are not read as realized power |
| 27 | 5. | framing | kept |
| 28 | The inert-share rule (2026-09-18): | DES-15; decision log, §7 PROPOSALS RULING (docs/decision_log.md:3902) | edited: label shortened |
| 29 | - Γ and Γ₄ are reported side by side on every branch, with B̂ and its CI. - If Γ rejects on a co-primary and Γ₄'s CI on that co-primary includes 0 or its sign is opposite, the paper states that the effect does not survive the inert-share correction, in the abstract-level summary and not only in an appendix. | docs/decision_log.md:4018-4022 | kept (verbatim quotation; demo 12:130-131) |
| 30 | The branch label does not change — it is fixed by Γ — but branch A/B text may not describe the effect as a composition effect without that qualifier. - If Γ is null and Γ₄ is null, Γ₄ is quoted as a second exclusion bound. - If Γ is null and Γ₄ rejects negative, it is reported under branch D's framing (matched-budget asymmetry) as a secondary observation, never as a confirmatory finding. - No magnitude threshold on B̂ is introduced, now or later. | docs/decision_log.md:4022-4029 | kept (verbatim quotation; demo 12:131-134) |
| 31 | 6. | framing | kept |
| 32 | The High readout, its reading for a null (same ruling): | docs/decision_log.md:4112-4113 | edited: label shortened |
| 33 | - Γ_H null → an a fortiori exclusion, and the only outcome this readout can establish: "no gap larger than X at High even where JOINT trained on the evaluated configuration and ISO never saw a composed one. | docs/decision_log.md:4141-4144 | kept (verbatim quotation; demo 12:138) |
| 34 | Quoted as an exclusion with X from the grid's own seed dispersion, never as an absence. […] | docs/decision_log.md:4144-4145 | kept (verbatim quotation; demo 12:138); pass 3: RC2-28: trailing "[…]" added (three further bullets follow in the source, paraphrased next) |
| 35 | The same entry states that the readout "is NOT a held-out test", that a positive $\Gamma_H$ is "NOT separable from in-distribution advantage", and that a negative one is "exploratory". | docs/decision_log.md:4133, :4146, :4149 | kept (demo 12:140; quoted fragments) |
| 36 | 7. | framing | kept |
| 37 | The 2000-update subsample (same ruling): | DES-15; docs/decision_log.md:4066 | edited: label shortened; re-check: RC2-R2 (orchestrator decision): label renamed "the 2000-update subsample"; the quotation below is unchanged |
| 38 | What it may be cited for: whether the differential drift measured at T = 1000 (review §6 item 1: 0.01209 per 100 updates) visibly persists, closes or reverses. | docs/decision_log.md:4088-4090; DES-10 | kept (verbatim quotation; demo 12:144) |
| 39 | What it may not be cited for: any claim that Γ "holds" or "vanishes" at T = 2000. | docs/decision_log.md:4090-4091 | kept (verbatim quotation; demo 12:144) |
| 40 | 8. | framing | kept |
| 41 | The mediation void rule (the frozen analysis plan, 2026-08-02): | DX-414; phase6_design_v2.md:335-340 | kept |
| 42 | If realized dose does not vary with assigned p, the dose figure has no x-axis and is declared VOID — registered now, not decided after seeing the first stage. | phase6_design_v2.md:362-364 | kept (verbatim quotation; demo 12:148); "dose" stays verbatim inside the quotation |
| 43 | 9. | framing | kept |
| 44 | The pre-unblind rulings (2026-09-26): | DX-405; decision log, PRE-UNBLIND RULINGS (docs/decision_log.md:4913) | edited: "before the look" dropped (stated in §9.1) |
| 45 | question / RULED | docs/decision_log.md:4921 | kept (verbatim quotation; demo 12:152) |
| 46 | (i) / what "−" means in the branch table / Rejection with negative sign (\|z\| > z_α, Γ < 0). A negative estimate that does not reject is a null. Ratified as built. | docs/decision_log.md:4923 | kept (verbatim quotation; demo 12:154) |
| 47 | (ii) / the cell (completion +, survival null), absent from the registered table / REGISTERED NOW as branch A_c — the founding claim on the founding primary. […] | docs/decision_log.md:4924 | kept (verbatim quotation; demo 12:155), with the record's omission marked |
| 48 | (iii) / test statistic / Normal z, z_α = 2.2365, as the frozen plan wrote; the t critical value is printed, not applied. Ratified as built. | docs/decision_log.md:4925; DES-13 | kept (verbatim quotation; demo 12:156) |
| 49 | (iv) / Γ(t) "sign stable" / All 11 point estimates, t = 500 … 1000, share one nonzero sign, per co-primary; t = 1000 is the grid's own eval. Consequence accepted in advance: on a null Γ, chance flips read UNSTABLE. Ratified as built. | docs/decision_log.md:4926 | kept (verbatim quotation; demo 12:157) |
| 50 | (v) / Γ₄ sample and threshold / JOINT k = 72 vs ISO-4 k = 20, SE sqrt(s_J²/72 + s_4²/20), "rejects" and "CI includes 0" at z_α = 2.2365. (Γ null, Γ₄ rejects positive) stays UNREGISTERED. Ratified as built. | docs/decision_log.md:4927; DES-3; DES-13 | kept (verbatim quotation; demo 12:158) |
| 51 | (vi) / Γ_H reading / As (i), at z_α = 2.2365. Ratified as built. | docs/decision_log.md:4928 | kept (verbatim quotation; demo 12:159) |
| 52 | (vii) / primary k / k = 72 stays primary; the registered-ladder k = 60 prefix is reported beside it, UNDERPOWERED-flagged. | docs/decision_log.md:4929; DES-1 | kept (verbatim quotation; demo 12:160) |
| 53 | (viii) / re-evaluate the 144 T\ = 1000 checkpoints on the post-unblind card / YES. […] | docs/decision_log.md:4930 | kept (verbatim quotation; demo 12:161) |
| 54 | In (viii), "the post-unblind card" is GPU 3. | HW-4 | edited; class A, F5: glosses "card" inside the quotation. Demo: "The 144 checkpoints of (viii) are the 72 seeds of each confirmatory arm. Branch A_c of (ii) is in Appendix E; (viii) produced the single-card curve of Appendix H." |
| 55 | 10. | framing | kept |
| 56 | The secondary specification (2026-09-26, after unblinding and before the sweep was read): | DX-413; decision log, SECONDARY INSTRUMENT BUILT BEFORE THE SWEEP IS READ (docs/decision_log.md:5005, :5058) | edited: "ratified" dropped from the label |
| 57 | (S1) PAVA + OLS slope CI; (S2) single-hinge breakpoint, UNDERPOWERED iff the CI spans {0.125 … 0.375}; (S3) plane fit, bound = 95 % CI of 0.5·γ_n; (S4) training co-activity over updates 1…1000, VOID iff the first-stage CI contains 0; (S5) the same-card replicate is ADDED, beside Γ₄, unable to change its qualifier; (S6) 95 % intervals, Γ₄′ at z_α. […] | docs/decision_log.md:5058-5063; DX-28 | kept (verbatim quotation; demo 12:167); the code-version words omitted, as the demo did |
| 58 | The omitted words name the code version, which identifies the repository. | docs/decision_log.md:5063 | kept (double-blind) |
| 59 | E The registered outcome branches | framing | kept |
| 60 | "Positive" and "null" mean rejection or non-rejection at θ\ in the confirmatory family, and "−" means rejection with negative sign (Appendix D, item 9). | phase6_framing_branches.md:94-97; docs/decision_log.md:4923 | edited: "graded on the grid's own per-arm seed dispersion" cut (Appendix D, item 4) |
| 61 | Branches A–D were registered on 2026-08-13, each with a framing; the registered table's venue-lean column is omitted. | DES-12; phase6_framing_branches.md:3, :101-104 | edited: "the registered table's fifth column, a venue lean, is omitted" shortened |
| 62 | $A_c$ was added on 2026-09-26, before unblinding, for a cell the table lacked. | DX-405; DX-102; docs/decision_log.md:4932-4950 | edited |
| 63 | branch / completion / survival / headline claim, as registered ($A_c$: its registered claims, summarized) | phase6_framing_branches.md:101 | kept |
| 64 | A / founding registration, verbatim (Γ(θ\) > 0) | phase6_framing_branches.md:100, :106-109 | kept; pass 3: RC2-29: "(Γ(θ*) > 0)" added so the cell reads as a claim; the registered words kept |
| 65 | B / null / composition is paid in agents, not task return | phase6_framing_branches.md:102 | kept (registered headline, quoted) |
| 66 | C / null / null / the instrument, and what it excludes | phase6_framing_branches.md:103 | kept |
| 67 | D / − on either co-primary / − on either co-primary / not separable from the matched-budget asymmetry | phase6_framing_branches.md:104; docs/decision_log.md:4923 | kept (the registration's "− (either)" written in both columns, as the demo did) |
| 68 | $A_c$ / null / the founding claim on the founding primary; the survival null quoted as an exclusion; no asymmetry claim | docs/decision_log.md:4932-4950 | kept (summarized, as labelled in the header) |
| 69 | The result is branch B, with the inert-share qualifier attached (§9.2). | decision log, UNBLIND RESULT (docs/decision_log.md:4984-4994) | edited: "with the falsifier passing" left to §9.2 (N16) |
| 70 | F Grid provenance and blinding | framing | kept; pass 3: RM-15: heading made "F Grid provenance and blinding" to match the index line |
| 71 | The grid was 252 runs from 2026-09-09 to 2026-09-22. | DX-30; DES-12 | edited (demo 12:187) |
| 72 | Seeds 1–12 of all ten arms (ISO, JOINT and eight secondary arms) ran on an RTX PRO 6000, then seeds 13–20 of all ten arms and 21–46 of ISO and JOINT on GPU 1. | DX-30; che/bench/results/phase6/by_card/README.md:49-55 | edited; class A, F5: "RTX 5090" made "GPU 1" (defined in §9.1) |
| 73 | The confirmatory artifact holds all 72 seeds of ISO and JOINT on GPU 1: 76 runs executed there and seeds 13–46 copied from the grid. | HW-4; DX-30 | edited; class A, F5 ("unit" becomes GPU); the executed seed list (DX-4) cut (LEN) |
| 74 | The superseded RTX PRO 6000 seeds enter only a descriptive diagnostic of the GPU effect. | docs/decision_log.md:4545-4546; che/bench/results/phase6/by_card/README.md:60 | edited; class A, F5: "card diagnostic" becomes "diagnostic of the GPU effect" |
| 75 | Seeds 1–12 of the secondary arms were re-run on GPU 1 (96 runs), so every analysed secondary run is on GPU 1 and Γ₄′ is a same-GPU contrast. | DX-30; docs/decision_log.md:5010-5013 | edited; class A, F5; Γ₄′'s same-GPU status added (honesty line 8: App. F is its home) |
| 76 | ISO-4 and the 2000-update subsample trained on GPU 2, so Γ₄ and B̂ are across GPUs, and the post-unblind evaluations ran on GPU 3. | HW-4; docs/decision_log.md:4995-4997 | edited; class A, F5: "unit" becomes GPU; Γ₄ and B̂ across GPUs (honesty line 8); re-check: RC2-R2 (orchestrator decision): "the 2000-update subsample" |
| 77 | All arms share seed integers, and seed 0, the floor seed, never enters the grid. | DX-416 | edited (demo 12:191) |
| 78 | Runs are ordered seed-major and chunks end on seed boundaries, so an interruption leaves a smaller balanced design and both arms of a seed share one GPU. | che/tests/test_p6_grid.py:173-197 | edited: "share a card" becomes "share one GPU" (F5); the test file's path cut from prose |
| 79 | Every checkpoint archive's recorded sha256 matched on re-verification on 2026-09-27, 615 of 615. | DX-408 | edited: the archive procedure sentence shortened (LEN); no hash quoted |
| 80 | A partial re-measurement of floors on another rented GPU on 2026-08-14 is provenance only. | DX-36 | edited; class A, F5: "re-floor" and "card" replaced; reps and archive count cut (LEN) |
| 81 | The grid runner computes no cross-arm quantity, which a unit test asserts along with the seed properties above, and the floor reports print dispersions only. | che/tests/test_p6_grid.py:155-170, :205-214; docs/decision_log.md:4627 | edited: moved from demo §9.1 (09:61) as App. F holds the blinding details |
| 82 | The unblinding script refuses an unflagged artifact or a modified code version, later analysis scripts refuse to run before its log exists, and each log records one run of its stage. | DX-411; che/scripts/p6_unblind.py:61-67; che/scripts/p6_post_analysis.py:55-58; CLAUDE.md:216-220 | edited: moved from demo §9.1 (09:61); "instrument" becomes "script", "tree" becomes "code version" (F5) |
| 83 | G Gamma over the final half of training | framing | edited: demo "H Gamma(t) over the final half" re-lettered and made slug-safe (P2-h) |
| 84 | Sign unstable over the final half, on both co-primaries: neither meets the registered rule that all 11 point estimates share one sign (Appendix D, items 2 and 9). | RES-11; docs/decision_log.md:4926 | edited (registered string first) |
| 85 | Values are rates, and the Šidák-corrected intervals are registered at update 1000 and descriptive before it. | DX-24; DX-25 | edited (demo 12:201); pass 3: RM-17: "t = 1000" becomes "update 1000" |
| 86 | Checkpoints before update 1000 were evaluated on GPU 3; update 1000 is the grid's own evaluation, and re-evaluating it on GPU 3 leaves every sign unchanged (cross-GPU agreement: §11). | DX-24; che/bench/results/phase6/post_unblind_analysis/post_evalfloor_gamma_t_high.md:69-70; docs/decision_log.md:4962-4968 | edited (pass 1, F5); pass 3, RM-17: "t = 1000" becomes "update 1000" (t is Def. 1's step index) |
| 87 | Completion, k = 72 per arm: | DES-13 | kept |
| 88 | update / Γ(t) / sd(Γ) / Šidák CI / sign | framing | edited; pass 3, RM-17: column "t" headed "update" |
| 89 | 500 / +0.0017 / 0.00321 / [−0.0055, +0.0089] | DX-24 | kept |
| 90 | 550 / −0.0017 / 0.00353 / [−0.0096, +0.0062] | DX-24 | kept |
| 91 | 600 / +0.0018 / 0.00362 / [−0.0063, +0.0099] | DX-24 | kept |
| 92 | 650 / +0.0015 / 0.00481 / [−0.0093, +0.0122] | DX-24 | kept |
| 93 | 700 / −0.0037 / 0.00470 / [−0.0142, +0.0068] | DX-24 | kept |
| 94 | 750 / −0.0147 / 0.00610 / [−0.0283, −0.0010] | RES-13; DX-24 | kept |
| 95 | 800 / −0.0035 / 0.00677 / [−0.0187, +0.0116] | DX-24 | kept |
| 96 | 850 / −0.0053 / 0.00729 / [−0.0216, +0.0110] | DX-24 | kept |
| 97 | 900 / −0.0039 / 0.00843 / [−0.0228, +0.0149] | DX-24 | kept |
| 98 | 950 / −0.0016 / 0.01021 / [−0.0245, +0.0212] | DX-24 | kept |
| 99 | 1000 / −0.0173 / 0.01068 / [−0.0412, +0.0066] | RES-1; DX-24 | kept |
| 100 | Survival rate, k = 72 per arm: | DES-13 | kept |
| 101 | update / Γ(t) / sd(Γ) / Šidák CI / sign | framing | edited; pass 3, RM-17: column "t" headed "update" |
| 102 | 500 / +0.0022 / 0.00228 / [−0.0029, +0.0073] | DX-25 | kept |
| 103 | 550 / −0.0037 / 0.00220 / [−0.0086, +0.0013] | DX-25 | kept |
| 104 | 600 / −0.0027 / 0.00232 / [−0.0078, +0.0025] | DX-25 | kept |
| 105 | 650 / +0.0011 / 0.00242 / [−0.0043, +0.0065] | DX-25 | kept |
| 106 | 700 / +0.0031 / 0.00235 / [−0.0021, +0.0084] | DX-25 | kept |
| 107 | 750 / +0.0036 / 0.00255 / [−0.0021, +0.0093] | DX-25 | kept |
| 108 | 800 / +0.0020 / 0.00232 / [−0.0032, +0.0072] | DX-25 | kept |
| 109 | 850 / +0.0018 / 0.00234 / [−0.0034, +0.0071] | DX-25 | kept |
| 110 | 900 / +0.0056 / 0.00231 / [+0.0004, +0.0108] | RES-12; DX-25 | kept |
| 111 | 950 / +0.0083 / 0.00219 / [+0.0034, +0.0132] | RES-12; DX-25 | kept |
| 112 | 1000 / +0.0096 / 0.00216 / [+0.0047, +0.0144] | RES-2; DX-25 | kept |
| 113 | H The secondary design | framing | edited: demo "I The secondary design" re-lettered (STRUCTURE §2) |
| 114 | Everything here is secondary, with 95 % intervals bootstrapped over seeds within arm (B = 2000), conditional on the common evaluation draw and not family-corrected. | DX-28; docs/decision_log.md:5072-5074 | edited (demo 12:239); "non-verdict-bearing" not repeated (BRIEF §5.3) |
| 115 | Each arm has k = 20 seeds on GPU 1 with δ off. | DES-13; DX-5 | edited; class A, F5 ("confirmatory unit") |
| 116 | With μ, p and ν as in §9.1, the triangle gives $\nu = 1 - 2\mu + p$, and the arm names are the labels of Figure 13's table view. | DES-9; docs/decision_log.md:5030-5032 | edited (pass 1, F5); pass 3, RM-3: the symbols pointed to §9.1, since the table headers are now μ, p and ν |
| 117 | arm / p / survival / completion | framing | edited; pass 3, RM-3 (MUST, print clipping): headers shortened to μ, p, ν, survival, completion so the completion means print in full |
| 118 | sweep_c50_p000 / 0.5 / 0 / 0 / 0.9241 / 0.7847 | DES-9; DX-28 | edited: means added from demo prose |
| 119 | sweep_c50_p125 / 0.5 / 0.125 / 0.125 / 0.9249 / 0.7775 | DES-9; DX-28 | edited: means added |
| 120 | sweep_c50_p250 / 0.5 / 0.25 / 0.25 / 0.9261 / 0.7797 | DES-9; DX-28 | edited: means added |
| 121 | sweep_c50_p375 / 0.5 / 0.375 / 0.375 / 0.9264 / 0.7656 | DES-9; DX-28 | edited: means added |
| 122 | sweep_c50_p500 / 0.5 / 0.5 / 0.5 / 0.9289 / 0.7749 | DES-9; DX-28 | edited: means added |
| 123 | ident_c40_p000 / 0.4 / 0 / 0.2 | DES-9; DX-28 | kept (no arm means are ledgered for the identification arms) |
| 124 | ident_c40_p200 / 0.4 / 0.2 / 0.4 | DES-9; DX-28 | kept |
| 125 | ident_c40_p400 / 0.4 / 0.4 / 0.6 | DES-9; DX-28 | kept |
| 126 | ISO-4 (GPU 2) / 0.5 / 0 / 0 / 0.9256 / 0.7726 | DES-14; DX-18; HW-4 | new row (pass 1); pass 3, RM-3: label shortened |
| 127 | The p = 0 sweep arm carries exactly ISO-4's training mixture. | docs/decision_log.md:5043-5045 | edited; class B, P3-N18 (the code name replaced in prose) |
| 128 | estimate (points) / survival / completion | framing | kept |
| 129 | sweep slope per unit p (labelled “dose slope”; separate fit) / +0.89 [−0.33, +2.11] / −2.51 [−9.43, +4.12] | SEC-5; DX-27 | edited; class A, F5: "dose slope" glossed as the label it is on Figure 13 |
| 130 | sweep endpoint, p = 0.5 minus p = 0 / +0.48 [−0.21, +1.17] / −0.97 [−4.82, +2.87] | SEC-5; DX-27 | kept |
| 131 | γ p, the co-occurrence slope, per unit p / +3.26 [+1.37, +5.02] / +2.69 [−6.75, +12.45] | SEC-1; DX-27 | edited: plain name added (F5) |
| 132 | γ n, the fire-only-share slope, per unit ν / −2.37 [−4.19, −0.57] / −6.52 [−15.34, +2.42] | SEC-1; DX-27 | edited: plain name added (F5) |
| 133 | bound, 0.5 γ n / −1.19 [−2.10, −0.28] / −3.26 [−7.67, +1.21] | SEC-2; DX-27 | kept |
| 134 | change point in p (labelled “knee”) / 0.375 [0.125, 0.375], UNDERPOWERED / 0.375 [0.125, 0.375], UNDERPOWERED | DX-28; SEC-6 | edited (pass 1, F5); pass 3, RN2-22: the change point is a value of p, not points |
| 135 | plane prediction of JOINT − ISO-4 (γ p × 1) / §9.2 / +2.69; γ p 's interval contains both measured values | DX-417; DX-27; RES-6; RES-8 | edited: the survival predictions (SEC-3, SEC-4) and the measured contrasts are stated once, in §9.2 (N16); the completion prediction (DX-417) is stated only here |
| 136 | The plane $y = \gamma_0 + \gamma_p p + \gamma_n \nu$ is a seed-level ordinary least squares (OLS) fit over all eight arms, and the bound, the fire-only share's part of the sweep's endpoint change, excludes zero on survival. | SEC-2; docs/decision_log.md:5030-5034, :5084-5087; che/bench/results/phase6/secondary/secondary.md:41 | edited (demo 12:265); class A, F5: "no-element confound" becomes "the fire-only share's part"; OLS defined |
| 137 | The sweep slope is a separate seed-level OLS fit over the five sweep arms, with an isotonic fit (PAVA) giving its monotone shape. | docs/decision_log.md:5016-5019 | edited: PAVA defined (BRIEF §5.2: App. H only) |
| 138 | The plane's slope along the sweep is $\gamma_p + \gamma_n$, so the two need not agree, and on completion they do not. | docs/decision_log.md:5030-5032; DX-27; SEC-5 | kept (demo 12:265) |
| 139 | The change point is the breakpoint of the best single-hinge fit. | docs/decision_log.md:5021-5023 | new: definition (BRIEF §5.2) |
| 140 | Linearity is assumed and checked only coarsely: arm-mean residuals lie within ±0.4 SE on survival and ±1.1 SE on completion, 8 points for 3 parameters. | DX-39 | kept |
| 141 | Per-coupling frequency, co-occurrence and active share cannot all be held fixed on the triangle. | DX-306; docs/decision_log.md:5084-5085 | edited (demo 12:278); the γ_p clause cut (stated in §9.2) |
| 142 | Floors exist only for the sweep's p = 0.5 arm: the other sweep arms assume that floor, and the identification arms are ungraded. | DX-306 | kept |
| 143 | The counter's realized count is endogenous, so nothing here is its causal effect, and mediation is VOID (§9.2). | DX-306; SEC-7; docs/decision_log.md:5099-5108 | edited: the demo's App. I mediation paragraph replaced by a pointer to §9.2 (N16); "dose" becomes "realized count" (F5) |
| 144 | I Trained-policy episodes | framing | edited: demo "J Trained-policy episodes" re-lettered I (STRUCTURE §2) |
| 145 | Figures I1 and I2 show one episode of each confirmatory arm, separately, chosen by a rule fixed before any render: θ\, episode key 0, stochastic actions, training seed 1 at update 1000. | ENV-13 | edited (demo 12:282): Figures J1, J2 become I1, I2 |
| 146 | Each opens at step 128 of 256. | DX-410; ENV-6 | new: moved from the demo captions ("Opens at t = 128") |
| 147 | They illustrate the environment under a trained policy and grade nothing. | ENV-13; decision log, FIGURE BATCH RULINGS (docs/decision_log.md:5888) A3 | kept |
| 148 | Episode explorer, ISO policy, training seed 1 | framing | kept |
| 149 | Figure I1. One episode of the ISO policy at θ. | ENV-13; paper/figures/interactive/out/html/explorer_thetastar_iso_s1_T1000_ep0.html | edited: caption cut to 60 words (P2 R2); the printed seed, update and θ* values not repeated (R3) |
| 150 | The map is environment state, the smoke field ρ included. | paper/figures/interactive/MANIFEST.md:101-104 | edited (demo J1 caption) |
| 151 | Selecting an agent shows its observation as produced (labelled obs v3: the masking observation, §6.1), the true cells, and the probability τ that each was seen. | paper/figures/interactive/DESIGN.md:424-427; che/env/observation.py:300-310 | edited; class A, F5: glosses the printed "obs v3" as the masking observation (BRIEF §5.2); pass 3: RM-14: "§3.4" becomes "§6.1", where Definition 6 defines the masking observation |
| 152 | It cannot compare training protocols. | framing | edited (R2): demo "it cannot show any difference between training protocols" |
| 153 | Status: illustrative · grades nothing · Interact: play, step, click an agent. | framing | edited (R4) |
| 154 | Maps of one ISO-policy episode at its start, middle and end, with one agent's observation, the true state of the same cells, and the probability each cell was seen | framing | kept |
| 155 | Static companion of Figure I1 for the printed PDF. | framing | edited: J1 becomes I1 |
| 156 | Figure I2 shows the JOINT policy's episode under the same rule. | ENV-13 | kept (demo 12:293) |
| 157 | One episode of one seed cannot carry a contrast that §9.2 measures over 72 seeds per arm and 512 evaluation episodes. | DES-3; DES-13 | edited: "The two figures are deliberately not placed side by side" cut (FIGURE BATCH A3 is respected by the layout) |
| 158 | Episode explorer, JOINT policy, training seed 1 | framing | kept |
| 159 | Figure I2. One episode of the JOINT policy at θ, with the layers and panels of Figure I1; only the observation panel shows what the selected agent perceives. | ENV-13 | edited: J2 becomes I2; caption cut (R2) |
| 160 | It cannot compare training protocols. | framing | edited (R2): demo "it cannot show any difference between training protocols" |
| 161 | Status: illustrative · grades nothing · Interact: as Figure I1. | framing | edited |
| 162 | Maps of one JOINT-policy episode at its start, middle and end, with one agent's observation, the true state of the same cells, and the probability each cell was seen | framing | kept |
| 163 | Static companion of Figure I2 for the printed PDF. | framing | edited: J2 becomes I2 |

## Findings

- [fram] Appendix D gains one quotation the demo lacked, item 4 (the frozen
  analysis plan's 2026-08-13 amendment: the test uses the grid's seed
  dispersion and the floors keep two narrower roles). It is the registered
  source of §9.1's sentence on what floors are for, and it lets the
  design-stage power figures move out of §9.1. The quotation keeps
  "beat-reproducibility hurdle" verbatim. Class A (LEN), owner-reversible.
- [mech] In Appendix D the pre-unblind rulings stay a Markdown table with
  the demo's escaped pipes (`\|z\|`), so the kit's table count includes it;
  the falsifier's formula keeps its pipes inside a code span (M1). B2's
  table-count check should see the same count in source and kit.

## Alternates

None.

## Open items

- **Q12 (class C).** Appendix I keeps both trained-policy explorers,
  shown separately (FIGURE BATCH A3); dropping them is the owner's choice.
- **Appendix letters** follow STRUCTURE §2: demo H → G, I → H, J → I,
  Figures J1/J2 → I1/I2. Headings are ASCII without parentheses (P2-h).
- **Iframe heights** of Figures I1 and I2 set to the orchestrator's
  measured 868 and 872 px (demo: 720).
- **N16 trims, owner-reversible:** the Γ(t) sign strings and the
  "only t = 900 …" sentence after the App. G tables (stated in §9.2 and in
  the tables' sign column); App. H's restated survival predictions,
  measured contrasts and mediation paragraph (pointers to §9.2); App. F's
  archive procedure, the executed-seed list (DX-4), and the 2026-08-14
  partial re-measurement's rep and archive counts (DX-36, DX-408).
- **Budget.** D–I are 14 % over the 850-word share after pass 3.
- **Pass-3 owner item RN2-7:** App. F's "615 of 615" matches DX-408 and
  `phase6_report.md:101`, but that report's own archive table sums to 636,
  and `m62b/SHA256_CKPT.txt` holds 18 entries where the table says 16. The
  record needs reconciling; the text is unchanged until the owner rules
  (RN2-7's interim option: no count).
- **Pass-3, orchestrator decision 4:** Figures I1 and I2 keep their height
  attributes (868, 872); B2 pins the explorers in CSS (RM-4).
