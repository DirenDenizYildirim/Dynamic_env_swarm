# Resolutions — writer W4 (§5–§7), fix round (step 4, pass 3), 2026-10-12

Every finding in RC1, RC2, RN1, RN2 and RM that touches `sections/05_coupling_a.md`,
`06_coupling_b.md`, `07_comms.md`, their provenance files or `ledger_proposals/W4.md`.
Line numbers in the findings refer to `snapshots/draft1/`. Each changed sentence's
provenance row names its finding in the change column ("fix round (2026-10-12): …").

**Counts: 23 fixed, 5 declined, 3 owner.** No MUST declined.

| finding ID | outcome (fixed / declined / owner) | what changed, or why not |
|---|---|---|
| RN1-2 (MUST) | fixed | §7.3: "The wider High floor puts that bar at about 11 points" misread DX-16 (the null's resolution, not the bar). Now "The wider High floors put its bars at 10.44 (completion) and 12.43 points (survival)", with a new VERIFIED row V4-3 (`phase5_report.md:877-880`). RN1's first wording ("excludes only effects larger than …") was not used, because the stub forbids "excludes effects larger than" for these post-hoc bars |
| RN1-3 (MUST) | fixed | §5.3: "nine [tag CA-6] measured cells" |
| RN1-4 (MUST) | fixed | §5.3: "two seeds per arm [tag CA-7]" (in the sentence rewritten for RC1-32) |
| RN1-5 (MUST) | fixed | Fig. 7 caption: "three replicates [tag DX-13]" |
| RN1-6 (MUST) | fixed | §6.4: "two seeds" → DX-40; "one run per cell" → DX-13; "the mean of its two seeds" → CB-6; "two-seed spread" → DX-38; and the leading "three replicate contrasts" → DX-13 |
| RN1-7 (MUST) | fixed | §6.4: "a three-seed [tag CB-9] spread" |
| RN1-8 (MUST) | fixed | §7.3: "twice [tag COM-2] the earlier Medium floor"; "tripling the mean alive out-degree, from 1.01 to 2.99" → "raising the mean alive out-degree from 1.01 to 2.99" (the ratio word is gone; COM-3 tags the two values); "three seeds" tagged DX-16 and "four seeds" tagged COM-4 for the same rule |
| RN1-11 (SHOULD) | fixed | "(from unrounded counts)" after the 4.83-fold fall (§5.3) and "(ratios of unrounded shares; …)" after 118, 22 and 16 (§6.4) |
| RN1-12 (SHOULD) | fixed | §7.3: "measured on that GPU" → "measured on the GPU that ran the study" |
| RN1-13 (SHOULD) | fixed | §6.4: "the Medium survival floor measured later is 1.29 points" → "the Medium survival floors measured later, on two GPUs, are 1.29 and 1.30 points" (METH-1) |
| RN1-15 (SHOULD) | fixed | Prose counts tagged in my files, as §1 tags them: "three-condition" (CB-4), "three bands" (DX-301), and "three severities" in §5.3 (CAL-3). The §6.3 heading stays bare (a tag would break its slug) |
| RN2-8 (SHOULD; orchestrator decision 8) | fixed | V4-1: lines corrected to `CLAUDE.md:390-391` and `:386-388`; the ruling (log:1801-1805) and the registered design (`phase6_design_v2.md:198-201, :207`) and `docs/locks.yaml:305` added as sources; status VERIFIED (DERIVED) with the derivation shown (Φ(0) = ½ for a true effect at the bar; the 51.6 % and 40.7 % figures for a 2σ test noted). §7's "about half the time", which RN2 calls accurate, is unchanged |
| RN2-10 (SHOULD) | fixed | V4-2: `m55/verdict.txt:3-5` added as the source that states the factor of two outright, with the GPU line (`phase5_report.md:955`). V6-1–V6-3 are W6's |
| RM-2 (MUST) | fixed | Proposition 3's display split into two `aligned` lines ("E[B_T] = λ_A T χ(β)(1 + o(1))," / "and in general E[B_T] ≤ λ_A T χ(β),"). No wording change (orchestrator decision 3) |
| RC2-5 (SHOULD, class B) | fixed | §5.2: "each correction has a known sign (Appendix A)" pointed to signs that Appendix A does not give. The signs are now stated in §5.2 as the theory document records them (TF:328-340; `phase3_report.md:106-108` for seed age): "an unconditional cluster-mass reference (a spanning-conditioned one understates the mass), matched seed locations and ages, and sparse seeding; boundary clipping, seed age and overlapping seeds each lower the measured slope (Appendix A)". Appendix A is now cited for the details only |
| RC1-31 (SHOULD) | fixed | Fig. 6 status: "Status: top, trained policies, 500 updates, seed ranges; bottom, no agents · …" (caption kept at 120 words) |
| RC1-32 (SHOULD) | fixed | §5.3: the hedged claim → "which suggests, on two seeds per arm, that the policies do not learn to avoid weak cells"; §5.1: the antithesis closer → "Agents cannot ignite a cell, but where they stand changes collapse rates, and a collapse can seed fire."; §5.3: the opener "The fall happens upstream of the agents." merged into the next sentence ("… stays in [0.164, 0.203]") |
| RC1-33 (SHOULD) | fixed | §6.1: the uncited clause "Beer–Lambert attenuation is the standard optical model for light through smoke" cut |
| RC1-34 (SHOULD, class B under N17) | fixed | §6.4 heading "The cost is paid in survival, at High" → "Survival cost at High severity" |
| RC1-35 (SHOULD) | fixed | §7 opening: "in CHE it had no measurable effect" → "In CHE, with a frozen message encoder, no measured effect of it cleared its bar (Figure 9)." |
| RC1-36 (SHOULD) | fixed | §7.3: "completion is 0.38 points higher and survival 1.43 points lower with links open (δ = 0) than with links denied (δ = 1), against bars of 7.99 and 2.60 points" |
| RC1-37 (SHOULD) | fixed | §7.3: "Because deaths are priced, Remark 2′(i) leaves communication some value here, which the measurements find weak at this scale and this death price." (after log:1086-1088; "small" in RC1's wording replaced by the record's "weak") |
| RC1-38 (SHOULD) | fixed | Nine ", so" clauses varied (Fig. 6 caption ×2; §5.1 occupancy sentence; §5.3 "Collapse never reads β"; §5.3 weak cells, the priority line; §6.3 bands; §6.4 floor; §7.1 receivers' weights; §7.2 toy). The remaining ones state a real inference or sit inside a formal statement |
| RC2-20 (SHOULD) | declined | No change needed in §7: its names ("a content ablation at Medium", "the same ablation at High", "the denial study") are the ones RC2 proposes as the standard. The change is W5's (§8.1 and App. C) |
| RC1-11 (SHOULD) | declined | The finding is in W1's reading note; my captions are cited only as evidence. Fig. 6's status was rewritten for RC1-31 |
| RC1-28 (SHOULD) | declined | The definition of "locked" goes in W3's §4; §5–§7 use "locked" with its date, as BRIEF §5.2 asks |
| RM-16 (SHOULD, class C) | declined | RM's own proposal is to leave Theorem 1's corridor letters L and R, which are the theory document's (TF:378); the change it proposes is in §3.5 (W3) |
| RM-18 (SHOULD, class C) | declined | Def. 7's k′ is the theory document's notation; RM's fix is a gloss in §8.2 (W5) |
| RM-10 (OWNER) | owner | Proposition 3's "Consequently … ∂E[B_T]/∂λ_A = Tχ(β)" stated as exact; not changed (orchestrator instruction); recorded in `provenance/05_coupling_a.md` Open items 4 and 7 |
| RM-9 (OWNER) | owner | Definition 1 omits the weak-terrain mask w (read by Def. 5 in §5.1) and the messages (Def. 7 in §7.1); recorded in the §5 and §7 provenance Open items |
| RM-6 (OWNER, class C, Q8) | owner | Under the hero-ladder alternate, §5's "Figure 1's event track … press ] in Figure 1" and §6's "Figure 1 opens on agent 7" point at the ladder. The fix is B2's build flag (block move and figure renumbering); no text change in my files |

Not applicable to my files (checked): orchestrator decisions 1 and 2 (neither the launch floor study nor Proposition 4 is named in §5–§7); decisions 3–7 assign work to other writers or B2.

**Checks after the fixes (2026-10-12):**
- `build_v2.py`: 0 failures, 0 warnings, 0 M1 flags; listings 6/6 identical.
- `provenance_check.py --strict 05_coupling_a 06_coupling_b 07_comms`: 55, 68 and 48 sentences, all with a row, 0 stale, 0 support problems. The checker now splits four pass-1 rows that it previously joined (§5 rows 13, 15, 17; §6 row 54); each gained a second row.
- Prose words (P3's counter): §5 935 (budget 850, +10.0 %), §6 1,145 (1,050, +9.0 %), §7 877 (800, +9.6 %). Captions: Fig. 6 120 (cap 120), Fig. 7 78, Fig. 8 64, Fig. 9 80 (caps 80).

## Re-check items

From the "Re-check (draft2)" sections of RN1 and RC1 (2026-10-12). **4 fixed.**

| finding ID | outcome (fixed / declined / owner) | what changed, or why not |
|---|---|---|
| RN1-R1 (MUST) | fixed | §6.4: "−6.87 and −10.66 points [tag DX-13] for the grid's two seeds [tag DX-40] and −4.70 points for a same-seed retrain [tag DX-13]". Each value now carries the row that holds it, and DX-40 tags only "two seeds" |
| RN1-R2 (SHOULD) | fixed | §7.3: COM-4 now tags 0.38, 1.43, 7.99 and 2.60 each at the number |
| RN1-R3 (SHOULD) | fixed | §7 opening: "In CHE, under a frozen encoder, no measured effect of it cleared a valid bar (Figure 9; one threshold is VOID, §7.3)." This uses only existing rows (COM-2 to COM-5, DX-16, V4-1, V4-3); "message" was dropped from "frozen message encoder" to stay within budget |
| RC1-R4 (SHOULD) | fixed | Fig. 6 caption: "and is shown as values" → "so its panel gives the reported values". To stay at the 120-word cap, "the two Proposition 3 runs" → "the Proposition 3 runs" in the caption's first sentence, and "a revised suite test" → "a revised test" |

**Checks after the re-check fixes:**
- `build_v2.py`: 0 failures, 0 warnings, 0 M1 flags. Its two final-only items, the front-matter date and the STUB-SPEC blocks, are not in my files.
- `provenance_check.py --strict 05_coupling_a 06_coupling_b 07_comms`: 55, 68 and 48 sentences, 0 unsourced, 0 stale, 0 support problems.
- Words: §5 935, §6 1,145, §7 880, all within the ±10 % tolerance. The Fig. 6 caption block is 120 words, at its cap.
