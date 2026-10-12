# Resolutions — W6 (§9, `12_appendix.md`, `14_appendix_plan_provenance.md`), step 4, pass 3

Writer W6, 2026-10-12. Every finding of RC1, RC2, RN1, RN2 and RM that touches
W6's files, in review order. Line numbers are draft1 snapshot lines. RN1 has
no finding in W6's files. Findings whose fix lies wholly in another writer's
file (RC2-2, RC2-11, RC2-22, RC2-23; RM-7) are not listed. Each changed
sentence's provenance row names its finding ID.

| finding ID | outcome (fixed / declined / owner) | what changed, or why not |
|---|---|---|
| RC1-3 | owner | Not resolved in text (orchestrator decision 7). §9.1 keeps "a review of the registered design identified this on 2026-08-16" and names no author. The fact that an LLM builder session wrote that review and drafted the registered design goes to Q4h and Q16 (recorded in `provenance/09_compositional_test.md`, Open items). |
| RC1-18 | fixed | §9.1:32: "on which the founding hypothesis was Γ(θ\*) > 0" dropped, so §9.1 no longer defines the founding hypothesis differently from §1 and App. E. |
| RC1-39 | fixed | App. A:48: "Corollary 1(3)" removed; the rate is now described as resting on critical exponents the paper does not state (§4.1). Same edit as RC2-4 and RM-12. |
| RC2-1 | fixed | MUST. §9.1:56 and App. D:49: "the first floor study" becomes "the grid's launch floor study (2026-08-10)" (orchestrator decision 1). |
| RC2-3 | fixed | §9.2:99: "(Figure 12; Appendix G gives every value)". |
| RC2-4 | fixed | As RC1-39. |
| RC2-5 | fixed | App. A:48: each of the four finite-protocol conditions now carries its known sign, as TF:328-339 states them, so §5.2's pointer to Appendix A lands. |
| RC2-6 | fixed | §9.1:32: "as that ruling records" restores the attribution; "the reproducibility floor" becomes "the floors then measured". The proposed parenthesis "(§8.6 says which have no floor of their own)" is not added (budget). |
| RC2-7 | fixed | §9.2:73: 0.66 is now "the upper end of its interval"; 3.29 is "its exclusion bound X, the gap of either sign the design would detect with 80 % power". |
| RC2-8 | fixed | Figure 11's caption: "carries ISO-4's rise" becomes "carries the ISO-4 − ISO difference" (B̂ keeps no verdict). The §10 half is W5's. |
| RC2-9 | fixed | §9.1:54: "the owner's attestation" becomes "our attestation, recorded with the ruling". |
| RC2-10 | fixed (in part) | §9.1:56: "the second registered caveat" is removed ("Bias (b) is the registered caveat on differential drift"). The subsample is now "the 2000-update subsample (§9.2)". The dates stay, because 2026-08-10 is part of the study's name under decision 1 and 2026-09-08 identifies the re-measured floor. The label question is RC2-34. |
| RC2-12 | fixed | §9.1:52 split: "Secondary arms run k = 20 seeds, with δ off, on GPU 1. The p = 0 sweep arm therefore trains on ISO-4's mixture on JOINT's GPU, …". |
| RC2-13 | fixed | §9.1:54: "A question it set for reviewers judged the arms symmetric on δ, …". |
| RC2-14 | fixed | §9.1:60 split into three sentences. |
| RC2-15 | fixed | §9.2:123: "about 0.11 of the 12 agents per episode". |
| RC2-16 | fixed | §9.3:133: "This follows from the comparison's design alone, as JOINT's threefold per-coupling frequency over ISO does." The proposed ", not of any result" is not used: one contrast construction per section (P3 §6), and §9.1 already has it. |
| RC2-24 | fixed | App. A:60: "handshake gate", "pinned arm" and "free arm" become "the check that the denied arm under the no-idle schedule matches ½ + ½q" and "the arm with free communication". |
| RC2-27 | fixed | App. D:49 split. "Design-stage" is added to both figures, and "§9.1 gives the realized power" closes the passage. |
| RC2-28 | fixed | A trailing "[…]" is added to App. D items 1, 4 and 6, whose source paragraphs or lists continue. |
| RC2-29 | fixed | App. E branch A cell: "founding registration, verbatim (Γ(θ\*) > 0)". |
| RC2-33 | fixed | §9.2:93: "It was proposed on 2026-09-26, after Γ₄ was seen and before that arm was read, and by rule it cannot change Γ₄'s qualifier. It agrees: null on both co-primaries." |
| RC2 (unnumbered, `09:50`) | fixed | As RN2-13. |
| RC2-34 | owner | The label "bias (b)" is kept, the default; the owner decides whether to rename it. |
| RC2-35 | owner | App. A's references to "the formal specification" are unchanged (Q4e, Q4k); same as RM-11. |
| RN2-3 | fixed | MUST. As RC2-1. |
| RN2-4 | fixed | MUST, orchestrator decision 5. §9.1 now reports M6.2b's reading: "+0.0242 per 100 updates on the confirmatory arms' floor study at 1000 updates". New row V6-4 (VERIFIED (DERIVED), `m62b_report.md:80-86`; unrounded check from `g1_2_report.md:44-47`). It is positive like both RTX PRO 6000 readings, so "the sign reverses on the grid GPU" still holds. |
| RN2-6 | fixed | MUST. "80 %" at :73 is tagged METH-7; "p = 0" at :66, :82, :84, :93 and :116 is tagged DX-28; "seeds 1–60" at :80 is tagged RES-3. |
| RN2-7 | owner | "615 of 615" is unchanged. The record is inconsistent (its own table sums to 636), so the owner reconciles it. Recorded in `provenance/14_appendix_plan_provenance.md`. |
| RN2-10 | fixed | Sources added to the W6 rows, with no value change: V6-1 gains log:3661-3676, V6-2 gains log:1211-1236 (PHASE-5 CLOSE RULINGS item 1), and V6-3 gains log:1846 and :1872. |
| RN2-12 | fixed | §9.1:56: DES-10 tags now sit next to +0.01209 and +0.0179. |
| RN2-13 | fixed | §9.1:50: "GPU 1, the RTX 5090 that ran the rest of the grid and every confirmatory run". |
| RN2-14 | fixed | RES-3 is added beside DES-1 wherever the k = 60 analysis or seeds 1–60 is meant (:50, :66, :73). |
| RN2-15 | fixed | The table lead reads "All contrasts at θ\* and T\* = 1000 unless the row says otherwise". |
| RN2-16 | fixed | §9.2:110: the subsample's slope is stated as positive in both windows, and "the drift it measures has not visibly reversed". This separates it from bias (b)'s grid-GPU reading. |
| RN2-17 | fixed | §9.2:125: "(completion, survival)" added. |
| RN2-22 | fixed | App. H: the row is now "change point in p (labelled “knee”)". |
| RN2-24 | fixed | App. D item 4's date now carries the new row V6-5 (the analysis plan's 2026-08-13 amendment: `phase6_design_v2.md:343-351`; log:3104, :3326-3328), not DES-12. |
| RN2-25 | fixed | §9.1:58: "fifth" tagged DX-405. |
| RM-3 | fixed | MUST, text half. §9.1's arm table is narrowed: "weight each" is folded into the components cell, the headers are μ, p, active share and fire-only ν, and the definitions moved into the sentence before it. The fire-only column (ISO's 1/3) is kept. App. H's arm table headers are shortened to μ, p, ν, survival and completion, and "ISO-4, for comparison (GPU 2)" to "ISO-4 (GPU 2)". The print width is to be re-checked after B2's print CSS (decision 3). |
| RM-4 | declined | Orchestrator decision 4: Figures I1 and I2 keep their height attributes; B2 pins the explorers in CSS, and the orchestrator sets the attributes afterwards. |
| RM-9 | owner | App. A:34's Proposition 1 proof inherits Definition 1's omission of the weak-terrain mask and the emitted messages. Not changed (theory-doc item). |
| RM-10 | owner | Not changed: Proposition 3's derivative equality is carried from TF and stated in §5.2 (W4). App. A proves the disjoint-cluster value only, as before. |
| RM-11 | owner | As RC2-35. |
| RM-12 | fixed | As RC1-39. |
| RM-14 | fixed | Figure I1's caption: "§3.4" becomes "§6.1", where Definition 6 defines the masking observation. |
| RM-15 | fixed | App. F's heading becomes "F Grid provenance and blinding", matching the index line. |
| RM-17 | fixed (W6's files) | In §9 prose and App. G, "T = 2000" becomes "2000-update" and "t = 850, 900, …" becomes "update 850, 900, …". App. G's column header "t" becomes "update". Quoted registered text and figure labels are unchanged. |
| RM-18 | declined | Proposition 4 keeps "discounted returns". The theory states the bound for the discounted return (TF:610-625), so "returns" alone would misstate it. The clash with Definition 8's episodic J is inherited from TF and is a record item. |
| RM-19 | fixed | §9.2:89: "With z_c and z_s the two statistics Γ / sd(Γ), …" (the registration's own definition). |
| RM-21 | owner | Only one table in the paper is numbered, and §9.2 cites "the contrast table" by description. Numbering every table is a paper-wide choice across W2, W3, W5 and W6, so it is not applied in one file. |

**Counts:** 41 fixed (two of them in part: RC2-10, RM-17), 2 declined (RM-4 under orchestrator decision 4; RM-18), 8 owner (RC1-3, RC2-34, RC2-35, RN2-7, RM-9, RM-10, RM-11, RM-21). No MUST was declined on the merits; RM-4 is left to B2 by decision 4.

**New rows:** V6-4 (+0.0242 per 100 updates, M6.2b's bias (b) reading, VERIFIED (DERIVED)) and V6-5 (2026-08-13, the analysis plan's amendment, VERIFIED), in `ledger_proposals/W6.md`.

**Budget after pass 3:**

| part | words | target |
|---|---|---|
| §9 | 2,398 (9.1 1,199; 9.2 1,094; 9.3 105) | 2,100 (+14 %) |
| index + App. A | 953 | about 800 |
| App. D–I | 969 (quotations excluded) | about 850 |
