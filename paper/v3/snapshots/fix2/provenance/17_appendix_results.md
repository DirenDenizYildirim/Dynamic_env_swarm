# Provenance: sections/17_appendix_results.md

Writer: W5 (Paper v3, step 4.1, 2026-10-14). Checked with
`paper/v3/src/provenance_check.py --strict`. `log` = `docs/decision_log.md`.
v2 material: App. G (`paper/v2/sections/14_appendix_plan_provenance.md:116-150`),
§9.2 (`paper/v2/sections/09_compositional_test.md:62-129`: k = 60, T = 2000, the High
readout, fire deaths, seed dispersion) and §7's Figure 9 (`paper/v2/sections/07_comms.md:23-25`).
Table rows are one unit each (cells joined by " / "; the sign column is not
alphanumeric and is dropped by the checker).

| # | sentence (verbatim) | support | change from v2, and why |
|---|---|---|---|
| 1 | E Additional results | framing | edited (v2 App. G "G Gamma over the final half of training" widened to App. E; heading as the stub fixes it) |
| 2 | Sign unstable over the final half, on both co-primaries: neither meets the registered rule that all 11 point estimates over updates 500–1000 share one sign (Appendix D). | RES-11; DES-13; docs/decision_log.md:4926 (PRE-UNBLIND RULINGS (iv): all 11 point estimates share one sign) | edited from v2 paper/v2/sections/14_appendix_plan_provenance.md:118 (registered string first); "Appendix D, items 2 and 9" → "Appendix D" (W4 owns the v3 timeline's numbering) |
| 3 | The intervals are Šidák-corrected, registered at update 1000 and descriptive before it. | DES-13; DX-24; DX-25 (descriptive at t ≠ 1000) | edited from v2 paper/v2/sections/14_appendix_plan_provenance.md:118 ("Values are rates, and the Šidák-corrected intervals are registered at update 1000 and descriptive before it"); "values are rates" moved to the table labels |
| 4 | Checkpoints before update 1000 were evaluated after unblinding, on a different GPU of the same model; update 1000 is the main runs' own evaluation, and re-evaluating it on that GPU leaves every sign unchanged (§8). | DX-24; HW-4; che/bench/results/phase6/post_unblind_analysis/post_evalfloor_gamma_t_high.md:69-70; docs/decision_log.md:4962-4968 | edited from v2 paper/v2/sections/14_appendix_plan_provenance.md:118 ("Checkpoints before update 1000 were evaluated on GPU 3 ..."): "GPU 3" in plain words (the numbered GPUs live in App. D); "the grid's" → "the main runs'"; pointer §11 → §8 |
| 5 | Gamma over the final half of training, completion and survival | framing (iframe title; paper/figures/interactive/out/html/gamma_t_final_half.html) | kept (iframe title carried from v2 09:101 by the stub) |
| 6 | Figure E1. Sign unstable over the final half, on both co-primaries. | RES-11 | edited from v2 Figure 12 caption (paper/v2/sections/09_compositional_test.md:114): renumbered E1; registered string first |
| 7 | Γ(t) with Šidák-corrected intervals; only the last checkpoint is the registered Γ. | DX-24; DX-25; DES-13 | edited from v2 Figure 12 caption ("Only the checkpoint at T* is the registered Γ; earlier intervals are descriptive"), shortened to the cap |
| 8 | Rings mark signs that differ from the final one, under the sign rule labelled “rule (iv)” on the figure. | RES-11; docs/decision_log.md:4926 (rule (iv)); paper/figures/interactive/out/html/gamma_t_final_half.html | edited from v2 Figure 12 caption ("A ringed sign differs from the sign at T*; rule (iv) is the pre-unblind sign ruling quoted in Appendix D"); glossed in the v3 form |
| 9 | The main runs’ GPU is labelled “grid card” on the figure; the “single-card curve” re-evaluates the last checkpoint on another GPU. | HW-4; che/bench/results/phase6/post_unblind_analysis/post_evalfloor_gamma_t_high.md:69-70 | edited from v2 Figure 12 caption ("“Grid card” is GPU 1 and “post-unblind card” GPU 3; the “single-card curve” re-evaluates the T* checkpoints on GPU 3"): numbered GPUs dropped; the glosses the stub names ("grid card", "single-card curve"); "post-unblind card" is left unglossed for the cap (Findings) |
| 10 | The dotted box is ±1 floor-based standard error of Γ. | DX-21 (floor-based sd(Γ)); paper/figures/interactive/out/html/gamma_t_final_half.html | edited from v2 Figure 12 caption (the "floor basis" gloss dropped for the cap; appendix captions are not term-checked) |
| 11 | The retained checkpoints over the final half of training of the joint-minus-isolated difference in completion and in survival, each with its Šidák interval, labelled sign unstable over the final half | RES-11; DX-24; DX-25 | kept (alt text carried by the stub from v2) |
| 12 | Static companion of Figure E1 for the printed PDF. | framing | kept (renumbered by the stub) |
| 13 | Completion, k = 72 per arm, in rates: | DES-13 | edited from v2 paper/v2/sections/14_appendix_plan_provenance.md:120, :134 ("in rates" added: the main text uses points, V3Q12) |
| 14 | update / Γ(t) / sd(Γ) / Šidák CI / sign | framing | kept (v2 App. G table header) |
| 15 | 500 / +0.0017 / 0.00321 / [−0.0055, +0.0089] | DX-24 | kept (v2 App. G table row, values and tags unchanged) |
| 16 | 550 / −0.0017 / 0.00353 / [−0.0096, +0.0062] | DX-24 | kept (v2 App. G table row, values and tags unchanged) |
| 17 | 600 / +0.0018 / 0.00362 / [−0.0063, +0.0099] | DX-24 | kept (v2 App. G table row, values and tags unchanged) |
| 18 | 650 / +0.0015 / 0.00481 / [−0.0093, +0.0122] | DX-24 | kept (v2 App. G table row, values and tags unchanged) |
| 19 | 700 / −0.0037 / 0.00470 / [−0.0142, +0.0068] | DX-24 | kept (v2 App. G table row, values and tags unchanged) |
| 20 | 750 / −0.0147 / 0.00610 / [−0.0283, −0.0010] | RES-13; DX-24 | kept (v2 App. G table row, values and tags unchanged) |
| 21 | 800 / −0.0035 / 0.00677 / [−0.0187, +0.0116] | DX-24 | kept (v2 App. G table row, values and tags unchanged) |
| 22 | 850 / −0.0053 / 0.00729 / [−0.0216, +0.0110] | DX-24 | kept (v2 App. G table row, values and tags unchanged) |
| 23 | 900 / −0.0039 / 0.00843 / [−0.0228, +0.0149] | DX-24 | kept (v2 App. G table row, values and tags unchanged) |
| 24 | 950 / −0.0016 / 0.01021 / [−0.0245, +0.0212] | DX-24 | kept (v2 App. G table row, values and tags unchanged) |
| 25 | 1000 / −0.0173 / 0.01068 / [−0.0412, +0.0066] | RES-1; DX-24 | kept (v2 App. G table row, values and tags unchanged) |
| 26 | Survival rate, k = 72 per arm, in rates: | DES-13 | edited from v2 paper/v2/sections/14_appendix_plan_provenance.md:120, :134 ("in rates" added: the main text uses points, V3Q12) |
| 27 | update / Γ(t) / sd(Γ) / Šidák CI / sign | framing | kept (v2 App. G table header) |
| 28 | 500 / +0.0022 / 0.00228 / [−0.0029, +0.0073] | DX-25 | kept (v2 App. G table row, values and tags unchanged) |
| 29 | 550 / −0.0037 / 0.00220 / [−0.0086, +0.0013] | DX-25 | kept (v2 App. G table row, values and tags unchanged) |
| 30 | 600 / −0.0027 / 0.00232 / [−0.0078, +0.0025] | DX-25 | kept (v2 App. G table row, values and tags unchanged) |
| 31 | 650 / +0.0011 / 0.00242 / [−0.0043, +0.0065] | DX-25 | kept (v2 App. G table row, values and tags unchanged) |
| 32 | 700 / +0.0031 / 0.00235 / [−0.0021, +0.0084] | DX-25 | kept (v2 App. G table row, values and tags unchanged) |
| 33 | 750 / +0.0036 / 0.00255 / [−0.0021, +0.0093] | DX-25 | kept (v2 App. G table row, values and tags unchanged) |
| 34 | 800 / +0.0020 / 0.00232 / [−0.0032, +0.0072] | DX-25 | kept (v2 App. G table row, values and tags unchanged) |
| 35 | 850 / +0.0018 / 0.00234 / [−0.0034, +0.0071] | DX-25 | kept (v2 App. G table row, values and tags unchanged) |
| 36 | 900 / +0.0056 / 0.00231 / [+0.0004, +0.0108] | RES-12; DX-25 | kept (v2 App. G table row, values and tags unchanged) |
| 37 | 950 / +0.0083 / 0.00219 / [+0.0034, +0.0132] | RES-12; DX-25 | kept (v2 App. G table row, values and tags unchanged) |
| 38 | 1000 / +0.0096 / 0.00216 / [+0.0047, +0.0144] | RES-2; DX-25 | kept (v2 App. G table row, values and tags unchanged) |
| 39 | The registered k = 60 analysis, on seeds 1–60, reads as the k = 72 analysis does and is flagged UNDERPOWERED; the registered seed rule had required 72 seeds for completion. | DES-1; RES-3; DES-3; decision log, PRE-UNBLIND RULINGS (docs/decision_log.md:4929, ruling vii: the k = 60 prefix reported beside k = 72, UNDERPOWERED-flagged) | edited from v2 paper/v2/sections/09_compositional_test.md:73 ("The registered k = 60 analysis reads the same and is flagged UNDERPOWERED"); "seeds 1–60" from v2's table row; the seed rule's requirement (DES-3: k_req 72 for completion) added as a fact beside the flag, not as its stated reason |
| 40 | Completion is null at −2.17 points [−4.86, +0.52], z −1.80, and survival rejects at +1.04 points [+0.54, +1.55], z +4.67, with Šidák-corrected intervals. | RES-3; DX-20 | edited from v2 paper/v2/sections/09_compositional_test.md:80 (table row) into prose: values and tags unchanged |
| 41 | Realized completion power against a 3-point effect is 60.2 % at k = 60 and 71.6 % at k = 72. | DES-6 | edited from v2 paper/v2/sections/09_compositional_test.md:32-33 (design paragraph: "realized completion power at a 0.03 effect is 60.2 % and 71.6 % at k = 60 and 72"); 0.03 → "a 3-point effect" (exact conversion). C23's home is §6.3; appendix files are not scanned for it |
| 42 | The 2000-update subsample (4 seeds per arm, trained on a second GPU of the same model) is descriptive and UNDERPOWERED by registration. | RES-15; HW-4; DX-23 ("4 seeds per arm, unit 2, UNDERPOWERED"); docs/decision_log.md:3928 | edited from v2 paper/v2/sections/09_compositional_test.md:110 ("The 2000-update subsample (4 seeds per arm, UNDERPOWERED)"); the GPU in plain words (HW-4: unit 2) |
| 43 | Its Γ(2000) is +0.03 points [−3.63, +3.69] on completion and +1.59 points [−0.02, +3.19] on survival, with 95 % intervals that are not family-corrected. | RES-15; DX-23 | edited from v2 paper/v2/sections/09_compositional_test.md:87 (table row) into prose; values and tags unchanged |
| 44 | The difference between JOINT's and ISO's training-curve slopes stays positive over updates 1000–2000, at +0.00384 (completion) and +0.00204 (survival) per 100 updates, as it was over updates 500–1000. | DX-23; DES-11; docs/decision_log.md:4084-4091 | edited from v2 paper/v2/sections/09_compositional_test.md:110 ("keeps a positive differential training-log slope over updates 1000–2000 ... as over 500–1000"): "differential training-log slope" in plain words |
| 45 | The drift it measures has not visibly reversed, which is all it may be cited for. | docs/decision_log.md:4088-4091; che/bench/results/phase6/post_unblind_analysis/post_gamma4_t2000.md:30-35 | kept (v2 paper/v2/sections/09_compositional_test.md:111) |
| 46 | The High-severity readout re-evaluated every final checkpoint of ISO, JOINT and ISO-4 with every stressor on at β = 0.70, outside the confirmatory family. | CAL-3; decision log, §7 PROPOSALS RULING (docs/decision_log.md:4112-4127) | edited from v2 paper/v2/sections/09_compositional_test.md:125 ("every T* checkpoint" → "every final checkpoint"; "out of family" → "outside the confirmatory family") |
| 47 | Both co-primaries are null, so the reading is an a-fortiori exclusion: no gap larger than 3.40 completion points or 2.54 survival points at High even where JOINT trained on the evaluated configuration and ISO never saw a composed one. | RES-14; docs/decision_log.md:4141-4145 (the registered sentence) | kept (registered sentence verbatim; v2 paper/v2/sections/09_compositional_test.md:125). HOME of C24 |
| 48 | Those two values are the readout's 80 %-power detection limits (the registered sentence's X), and its Šidák-corrected intervals are [−3.26, +1.68] (completion) and [−1.46, +2.23] (survival) points. | RES-14 (X = MDE80, 0.0340 and 0.0254); DX-26; che/bench/results/phase6/post_unblind_analysis/post_evalfloor_gamma_t_high.md:76-81 (column "X (MDE80)"); METH-7 | new: BRIEF §9.2 trap 5 (the High-readout numbers are MDEs: label them); the intervals moved from v2's table row (v2 paper/v2/sections/09_compositional_test.md:85) |
| 49 | JOINT − ISO-4 at High is null too, at −0.75 [−3.87, +2.36] and −1.28 [−3.50, +0.95] points, with no reading rule of its own. | DX-26; docs/decision_log.md:4123-4124 (Γ_H,4 "reported beside it with no reading rule of its own") | edited from v2 paper/v2/sections/09_compositional_test.md:86 (table row) into prose |
| 50 | The JOINT − ISO gap lies within rerun noise, at 0.73 and 0.75 times its floor-based standard error (completion, survival); ISO-4 has no identical reruns, so that check is UNDERPOWERED for it. | RES-14; che/bench/results/phase6/post_unblind_analysis/post_evalfloor_gamma_t_high.md:84-87 | edited from v2 paper/v2/sections/09_compositional_test.md:125 ("$\\Gamma_H$ lies within rerun noise ..."): Γ_H named in words |
| 51 | The readout is not a held-out test: JOINT trained on this configuration at weight 1/2, and ISO never trained with more than one stressor on. | DES-16; docs/decision_log.md:4134-4137 (JOINT trained on this exact configuration at weight 1/2; ISO "never on any all-on configuration"); che/configs/p6_iso.yaml:41-46 | edited from v2 paper/v2/sections/09_compositional_test.md:125; "ISO never trained with more than one stressor on" added from the ruling (ISO's six components each carry one stressor) |
| 52 | On secondary metrics outside the family, descriptive and without a floor, JOINT has 0.1177 fewer fire deaths per episode than ISO (z = −4.59), at 0.6949 against 0.8126, and its episode return differs by −0.4958 (z = −1.44). | RES-10; DX-22 | edited from v2 paper/v2/sections/09_compositional_test.md:122: the arm values and episode return added from DX-22 (stub ROWS); the agents restatement (DX-406) dropped, since the size statement is §6.3's (X4-3, W4) |
| 53 | Seed dispersion exceeds the rerun floor in both arms, 1.12 and 1.09 times on completion and 1.25 and 1.19 times on survival (ISO, JOINT). | HW-1 | kept (v2 paper/v2/sections/09_compositional_test.md:129) |
| 54 | Survival Γ, at 5.40 times its floor-based standard error (completion 1.78 times), clears the check that an effect exceeds rerun noise. | HW-1; DX-21 | kept (v2 paper/v2/sections/09_compositional_test.md:129) |
| 55 | Figure E2 shows the measurements behind the inert label of §4.4. | COM-2; COM-3; COM-4; DX-16 | new (the stub moves v2's Figure 9 here; §4.4 points to it) |
| 56 | In the two-agent courier toy, the value of communication rises from 0 to 0.498 as perception decays (Figure E2(a)). | COM-1; DX-15; che/bench/results/phase5/phase5_report.md:540-560 | edited from v2 paper/v2/sections/07_comms.md:51 ("... rises monotonically from 0 to 0.498 (Figure 9(a); Appendix A)"); "corridor toy" naming per BRIEF §5.2 ("the two-agent courier toy") |
| 57 | Top left, courier success rate against perception attenuation in the two-agent toy, for free and for denied communication, with the predicted curve. | paper/figures/MANIFEST.md:390-412 | kept (alt text carried by the stub from v2 07:23) |
| 58 | Top right, the denial contrasts at medium severity with their bars. | paper/figures/MANIFEST.md:390-412 | kept (alt text) |
| 59 | Bottom, the per-run values behind those contrasts. | paper/figures/MANIFEST.md:390-412 | kept (alt text) |
| 60 | Figure E2. Communication in the toy, and denial in CHE at Medium. | paper/figures/MANIFEST.md:390-392 | kept (include caption; renumbered E2 by the stub) |
| 61 | (a) The two-agent courier toy (labelled “E2C²” and “M5.2” on the figure), with scripted policies: success with free and with denied communication; the shaded gap is the value of communication. (b–d) The denial study at Medium (labelled “M5.5” on the figure): contrasts between open and denied links against bars of twice the floor sd, and the per-run values. | paper/figures/MANIFEST.md:390-412; COM-4; V4-2; che/bench/results/phase5/phase5_report.md:540-560 | edited from v2 07:25 caption paragraph: renumbered; "E2C²", "M5.2" and "M5.5" glossed in the v3 form; "pinned" and "post-hoc floor grading" dropped for the cap; "No panel grades inertness ..." dropped (V3-S4: limits in the text, §4.4) |

## Findings

- **Caption caps.** Figure E1's caption is about 69 words against 60 (the
  registered string, the GPU gloss and the rule gloss take the room); Figure
  E2's caption paragraph is 58. "post-unblind card" (printed on Figure E1) is
  not glossed; v2 glossed it.
- **Change points.** BRIEF §6.4 lists "change points" under UNDERPOWERED in
  App. E, but the sweep's change point lives in App. F (W4, the secondary
  design); App. E does not repeat it.
- **Fire deaths in agents.** v2 put DX-406 ("about 0.11 of the 12 agents")
  beside the fire-death contrast. App. E drops it: the size statement's home
  is §6.3 with row X4-3, and DX-406 is scoped to that comparison (BRIEF §9.2
  trap 4).
- **Word count.** 529 prose words against about 550, plus the two Γ(t) tables.
