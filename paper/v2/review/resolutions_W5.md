# Resolutions — writer W5 (step 4, pass 3, fix round, 2026-10-12)

Every review finding that touches W5's files (§8, §10, §11, Appendices B–C, and
`sections/alt/11_reproducibility.supplement.md`), plus the orchestrator's items for W5.
Each changed sentence's provenance row names its finding ID
(`paper/v2/provenance/<file>.md`). Totals: **29 fixed, 1 declined, 2 owner** (one row per finding, with RN2-3, RC2-1 and W5-F4 sharing one row).

After the fixes: `build_v2.py` reported 0 failures, 0 warnings and 0 M1 flags, with and without
`--alt 11_reproducibility.supplement`. `provenance_check.py --strict` on all five files found 0
unsourced sentences, 0 stale rows and 0 support problems. Prose words (P3 method):
- §8: 938 against 850, with caption and note at 119 against a cap of 120;
- §10: 745 against 700;
- §11: 328 against 300, and its alternate 343 against 380;
- App. B–C: 345 against about 350.

| finding ID | outcome | what changed, or why not |
|---|---|---|
| RN2-1 (MUST) | fixed | "four bars set without floors" was wrong for two of the four. §8.1 now says "four bars with invented constants", in the ruling's words (log:1248). App. C states each bar's defect: no floor; a floor hard-coded from another study, not measured on its own runs; a bar on a measured floor that was out of reach; a threshold below the noise. |
| RN2-9 | fixed | V5-1 now cites the ruling (log:1248, Phase-5 close rulings item 2) with `CLAUDE.md:343-348` as its transcription. "What" is reworded and the derivation (a count of named items) shown (orchestrator decision 8). |
| RC2-19 | fixed | Same fix as RN2-1. App. C: "Re-sited at High, the ablation measured its floor first, but a bar set on that floor was out of reach …". |
| RN2-2 (MUST) | fixed | §11 and its alternate: "Re-evaluated on another GPU, the final checkpoints of all confirmatory runs gave identical completion and survival values in 280 of 288 checkpoint–metric pairs …" (log:5186-5187). |
| RN2-5 (MUST) | fixed | App. C gains a row for the High readout's floor: the 8 ISO and 8 JOINT reruns of the 2026-09-08 study, evaluated at High on GPU 3. The floor values come from the committed JSON, through the new VERIFIED row V5-2. |
| RM-3 (MUST) | fixed | App. C's cells are shortened: GPU and updates merged, arm names given once above the table, "use" cells cut to their pointers. The per-arm drift-to-floor ratios (DES-10) are cut, since no sentence uses them. Four role cells in App. B are shortened too. Table words dropped from 770 to 649. B2 handles the print CSS. |
| RM-7 (MUST) | fixed | "(§9.1)" → "(Appendix F)" in §11 and the alternate (orchestrator decision 6). |
| RC2-2 | fixed | Same change as RM-7. |
| RN2-3 / RC2-1 / W5-F4 | fixed | No W5 file used "the first floor study". App. C's key now reads "the grid's launch floor study (2026-08-10)" (orchestrator decision 1). |
| RN2-4 | fixed (cross-section) | Per decision 5, W6 added M6.2b's reading to §9.1 as V6-4, and §8.5 keeps "§9.1 reports every reading". |
| V6-4 alignment | fixed | Cross-section alignment with V6-4 (W6). §9.1 now gives four readings from four floor studies (`09_compositional_test.md:56`), so §8.5 says "the four floor studies", tagged DES-10 and V6-4. |
| RC2-11 | fixed | The bias (b) sentence is now its own paragraph. It names the drift before the label and links it to the reporting: "…changed sign between the four floor studies that read it before unblinding, so §9.1 reports every reading." |
| RC2-17 | fixed | "exceeded the one and fell short of the other" → "exceeded the threshold but not the noise". |
| RN2-23 | fixed | "the agents drifted" → "the alive agents' centroid drifted". |
| RC2-18 | fixed | Fixed with RN2-23's wording. The longer clause about what a centroid cannot separate was left out for budget, since "(rendered-pixel centroids, a diagnostic)" keeps the limit. |
| RN2-8 | fixed | §8.2: "the effect at which an uncorrected test would just reject, which it detects about half the time". The V4-1 tag is kept; W4 corrects that row (decision 8). |
| RN2-11 | fixed | §8.2 now names the metric, the effect and the σ basis: "on the 1000-update completion floors and a 0.03 effect", tagged DX-34 and DES-4. |
| RC2-20 | fixed | One name per study, taken from §7: "the content ablation at Medium", "the same ablation at High", "the denial study". These are used in §8.1 and App. C, and the key matches. The key's header is now "plain name". |
| RC2-21 | fixed | App. C's prose no longer uses study codes ("the High floor in the table", "the four-run Medium floor study on an RTX 5090", "its quantity"). |
| RC2-25 | fixed | Figure 10's caption now glosses "tree" (a code version) and "reps" (identical reruns). The caption stays within its cap. |
| RC2-26 | fixed | The ten bold rule sentences in §8 are unbolded; the H3s carry the rules. |
| RC2-8 | fixed | §10: "carries ISO-4's rise over ISO" → "carries the ISO-4 − ISO difference, which is reported without a test". B̂ gets no verdict. |
| RC2-22 | fixed | §10's F3 bullet now points to §9.1 instead of restating the mechanism: "carries a design error, which inflates Γ: a third of ISO's training episodes are fire-only (§9.1)". "The branch label stays B" moved to the found-after list. |
| RC2-30 | fixed | "Its survival effect" → "Coupling B's survival effect". |
| Proposition 4 name (decision 2) | fixed | §10: "Proposition 4 (A transfer bound for a fixed policy) bounds …". |
| RN2-18 | fixed | §10 item 8: DX-5 is now tagged after GPU 1. |
| RN2-19 | fixed | App. C, launch floor study: "sd(Γ) at k = 40: completion 0.00504, survival 0.00310". |
| RN2-20 | fixed | The 2026-08-14 set's updates cell "n/a" → "1000", with the new VERIFIED row V5-3 (`g1_floors_card2/README.md:11-12`). |
| RN2-21 | fixed | The overlap sentence now names the 2026-09-08 re-measurement, and each interval names its GPU. |
| RM-18 | declined | Class C. §8.2 already writes "k … seeds" at each use, so the k clash does not arise there. The Proposition 4 half of the finding is W6's. |
| RM-17 | owner | Class C. T is used both for the training budget and for the episode horizon (§10, "the T = 2000 subsample"). A local rewording would leave §10 out of step with §9 and App. G, so the choice belongs to the owner, once for the whole paper. |
| RC2-34 | owner | Class C. With no "bias (a)" left, the label "(b)" is orphaned. §8.5 now names the drift before the label; whether to keep the record's label is the owner's call. |

New ledger rows (`paper/v2/ledger_proposals/W5.md`): V5-2 (the High readout's floor: 8 reruns per arm and four floor values) and V5-3 (1000 updates for the 2026-08-14 set). V5-1 is corrected.

## Re-check items (step 4.3, 2026-10-12)

| finding ID | outcome | what changed, or why not |
|---|---|---|
| RN2-R1 (MUST) | fixed | The High readout's floor reruns are GPU 1's re-measured floor runs (RTX 5090, `g1_floors_5090`): `p6_post_analysis.py:99`, and `run_p6_post_unblind_evals.sh:44` and `:87-88`, identical at the shipped tree. The 2026-09-08 RTX PRO 6000 reruns were only what the plan named. App. C's cell now reads "GPU 1's runs, 1000, evaluated on GPU 3" (DX-412). V5-2's "what" and source are corrected, read this session and marked VERIFIED; the values are unchanged. This supersedes the description in the RN2-5 row above. |
| RC2-R1 | fixed | §8.1: "which of them" → "which of the three", meaning the three factors. |
| RN2-R3 | fixed | §8.5: "…the four floor studies that read it at 1000 updates before unblinding…" (tagged DES-13), matching W6's §9.1 wording. M6.2's 500-update reading falls outside that scope. |
| RC2-R2 | fixed | §10: "the T = 2000 subsample" → "the 2000-update subsample" (orchestrator decision). No other prose use of "T = 2000" is in a W5 file. |

After these fixes: `build_v2.py` reported 0 failures and 0 M1 flags. Its two final-only items are not in W5's files: the owner's date confirmation and the STUB-SPEC count. `provenance_check.py --strict` on all five files found 0 unsourced sentences, 0 stale rows and 0 support problems. §8 is 942 prose words; §10 is 744.
