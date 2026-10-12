# RN2 — numbers review, part 2 (§8–§11, Appendices A–I, alt §11; every new ledger row)

Reviewer RN2, Paper v2 phase 1 step 4 pass 2, snapshot `paper/v2/snapshots/draft1/`. Line numbers are the snapshot's. Every check below was run in this session (2026-10-11/12).

## Summary

**Counts: 6 MUST, 18 SHOULD, 1 OWNER.**

The MUST items:
- **RN2-1:** "four bars set without floors" contradicts the paper's own description of two of the four.
- **RN2-2:** "280 of 288 paired evaluations": the 288 are checkpoint–metric pairs, from 144 evaluations.
- **RN2-3:** "the first floor study (2026-08-10)": two earlier floor studies of the same arms are in App C's own table.
- **RN2-4:** "§9.1 reports every reading" of bias (b): M6.2b's reading is left out.
- **RN2-5:** App C claims to list every floor the paper uses but omits the High-readout floor.
- **RN2-6:** untagged record numbers in §9.

The OWNER item (RN2-7): the record's archive count "615 of 615" does not match its own table.

**Method.** All helper scripts are in `scratchpad/RN2/`:
- `extract.py` pulls every `<!-- N:ID -->` tag in scope, outside STUB-SPEC blocks, with its context, and looks up its row in `paper/numbers_ledger.md`, `paper/v2/ledger_supplement.md` and the snapshot's `ledger_proposals/*.md`.
- `untagged2.py` lists every numeral not followed by a tag before the next numeral or the end of the clause; each hit was then judged by hand.
- `sample.py` draws the canonical-ledger sample.
- `appg.py` compares App G with its source and recomputes every CI.
- `quotes.py` compares the App D quotations with their sources.

Each source was read at its file:line this session.

**Coverage.**
- **Tags:** 527 tags in scope (113 unique IDs) across the eight files: §8 30, §9 164, §10 15, §11 10, App A 7, App B–C 123, App D–I 168, alt §11 10. 100 % were checked against their rows for value, scope and wording. Every ID resolves to exactly one row; none is missing.
- **New ledger rows:** V4-1, V4-2, V5-1 and V6-1–V6-3 are 100 % checked at source, including their uses outside my files (`01_introduction.md:40` V6-1; `07_comms.md:73` V4-1, V4-2).
- **Supplement rows:** 44 of 44 DX rows used were checked at source.
- **Canonical rows:** 64 used in scope. The random 30 % sample was 20 rows (Python `random.Random(20261011).sample`, k = 20): CA-1, CAL-3, CB-1, DES-4, DES-5, DES-11, DES-15, ENV-6, ENV-9, HW-2, METH-3, METH-7, RES-9, RES-10, RES-11, RES-14, RES-15, SEC-1, SEC-6, SEC-7. Adding all 35 RES/SEC/HW/DES rows §9 uses gives 45 rows (70 %). I then extended the check to all 64.
- **Arithmetic:** recomputed in full (see "Checked and clean").

**Class column.** B = the fix follows from a standing written rule: the numbers rule, the record winning over a row, or BRIEF §10. C = needs an owner ruling or choice.

## Findings

| ID | severity | file:line | quoted text (short) | problem | evidence (record file:line, ledger ID, log heading:line) | proposed fix | class |
|---|---|---|---|---|---|---|---|
| RN2-1 | MUST | `08_methodology.md:33`; `13_appendix_locks_floors.md:80` | "The rule followed four bars set without floors" | The count is right, but the description contradicts the paper's own App C paragraph for two of the four bars. App C says the message-use test "applied a floor hard-coded from the study of row M5.1e", so it had a floor. It says the High re-siting "measured its floor first", so its bar had a floor but could not be reached. The source row agrees: DX-302 has "given the High floor M5.3b measured first" and calls the four "floor-less or unreachable". Only M4.4 and M5.5 lacked a floor. The wording comes from the record (`CLAUDE.md:343`; log:1192, "a bar chosen without a measured floor"). V5-1 copies it. | `CLAUDE.md:343-348`; log:1192-1196 (M5.5 report entry); log:1241-1252 (PHASE-5 CLOSE RULINGS, item 2: "The four invented constants are the builder's", :1248); DX-302 note; `phase5_report.md:916-922` | §8.1: "The rule followed four bars that broke it (Appendix C)." App C:80: "The rule of §8.1 followed four bars that broke it". Then give each bar's defect in one clause: no floor (M4.4); a floor hard-coded from an earlier study, not measured for its run (M5.3); a bar no affordable seed count could reach, with no UNDERPOWERED flag (M5.3b); a threshold below its floor (M5.5). In V5-1, change "what" to "the four bars that broke the rule". The OI-5 phrase stays out. | B |
| RN2-2 | MUST | `11_reproducibility.md:20`; `alt/11_reproducibility.supplement.md:13` | "280 of 288 paired evaluations are identical" | The 288 are (checkpoint, metric) pairs, not evaluations. The 144 T\* checkpoints were re-evaluated on GPU 3, and each evaluation gives completion and survival: 70 + 70 + 69 + 71 = 280 identical out of 4 × 72 = 288. Calling them 288 "evaluations" doubles the number of evaluations. HW-3's row wording ("paired cross-card evals") is just as loose; that is a record item, and the text fix is enough. | `post_evalfloor_gamma_t_high.md:58-66`; log:5186-5187 (POST-UNBLIND STAGE RESULT: "144 checkpoints paired: 280 of 288 (checkpoint, metric) evals identical"); HW-3 | "Across GPUs, re-evaluating every T\* checkpoint of both arms gave identical completion and survival values in 280 of 288<!-- N:HW-3 --> checkpoint–metric pairs, and the largest absolute difference is 2.44 × 10⁻⁴<!-- N:HW-3 -->." Apply to both files. | B |
| RN2-3 | MUST | `09_compositional_test.md:56`; `14_appendix_plan_provenance.md:49` | "on the first floor study (2026-08-10)"; "The first floor study (an RTX PRO 6000, 2026-08-10) gave, at k = 40, an MDE₈₀ of …" | Factually wrong, and it contradicts App C. M6.2 (500 updates, 2026-08-02) and M6.2b (1000 updates, 2026-08-02/03) measured floors of the same ISO and JOINT arms before the 2026-08-10 study. App C lists both (`13:70-71`), and M6.2b's floors are the ones that set k = 40 (App C:71). The 2026-08-10 study is G1.2, which App C's key correctly calls "the grid's launch floor study" (`13:91`). The phrase comes from the scaffold glossary (`BRIEF.md` §5.2: "launch batch → the first floor study (2026-08-10)"). | `R/phase6/phase6_report.md:62-65` (M6.2 2026-08-02; M6.2b 2026-08-02/03; G1.2 2026-08-10); `R/phase6/m62b/m62b_report.md:40-54`; log:2185-2194 (M6.2b CLOSE-OUT: k = 40 from the M6.2b floors); DES-5 | Write "the grid's launch floor study (2026-08-10)" in both places. Correct the BRIEF §5.2 glossary row so that other sections do not repeat the phrase. | B |
| RN2-4 | MUST | `08_methodology.md:71` (and `09_compositional_test.md:56`) | "changed sign between the three floor studies that read it before unblinding; §9.1 reports every reading" | "Every reading" is not true. M6.2b (1000 updates, RTX PRO 6000) used the same estimator: completion drift over the final 100 updates per arm. It measured ISO +0.0034 and JOINT +0.0276 per 100 updates, a differential of +0.0242 (DERIVED: 0.0276 − 0.0034). §9.1 does not report it. The three DES-10 readings are the three studies run on the grid's floor protocol. | `R/phase6/m62b/m62b_report.md:80-85`; `R/phase6/g1/g1_2_report.md:44-47` (the same M6.2b drifts); DES-10; `R/phase6/by_card/README.md:31` ("G1.2-protocol floors") | Default: "Bias (b) of §9.1 changed sign between the three floor studies run on the grid's protocol before unblinding (§9.1)". Delete "§9.1 reports every reading". Alternative (owner choice): add M6.2b's +0.0242 as a DERIVED row from `m62b_report.md:84-85` and report it in §9.1. It is positive like both RTX PRO 6000 readings, so "the sign reverses on the grid GPU" still holds. | B |
| RN2-5 | MUST | `13_appendix_locks_floors.md:61` | "the table lists each one this paper uses" | One floor the paper uses is missing from the table. §9.2:125 says "Γ_H lies within rerun noise, at 0.73 and 0.75 times its floor-based standard error" (RES-14). That rests on a separate High-readout floor: the 8 ISO and 8 JOINT rep checkpoints of the 2026-09-08 re-floor, evaluated at β = 0.70 on GPU 3. The rep evaluations are committed (`R/phase6/post_high/evalhigh_*_rep*.json`). | log:4164-4170 (§7 PROPOSALS RULING, "Floors, per-artifact and per-hardware"); `post_evalfloor_gamma_t_high.md:84, :86` ("floor (8 reps, this card)"); RES-14 | Add a row: High-readout floor; checkpoints trained on the RTX PRO 6000 (2026-09-08 re-floor) and evaluated on GPU 3; 1000 updates; ISO and JOINT at β = 0.70; 8 reruns; use: the check against rerun noise for Γ_H (§9.2). It needs a VERIFIED row in `W5.md` citing the lines above. Or narrow the sentence to "each training floor and the evaluation floor". | B |
| RN2-6 | MUST | `09_compositional_test.md:73`; `:66, :82, :84, :93, :116`; `:80` (status cell) | "detect with 80 % power"; "the p = 0 sweep arm"; "seeds 1–60, UNDERPOWERED" | These record numbers have no tag, and none is exempt under BRIEF §10. They are not section, figure or definition numbers, and not definitional counts. At :73, the 80 % is METH-7's ruled convention (tagged at :66 and in §8). At :66, :82, :84, :93 and :116, "p = 0" is a configured value (DX-28); only its first use, at :52, is tagged. At :80, "seeds 1–60" is the prefix analysis (RES-3, DX-20). | BRIEF.md §10 ("Every record number carries a tag right after it"); METH-7; DX-28; RES-3 | Add `<!-- N:METH-7 -->` after "80 %" at :73. Add `<!-- N:DX-28 -->` after the first "p = 0" in each of :66, :82, :84, :93 and :116. Add `<!-- N:RES-3 -->` after "1–60" at :80. | B |
| RN2-7 | OWNER | `14_appendix_plan_provenance.md:112` (and DX-408) | "615 of 615" | The paper's number matches its row, and the row matches `phase6_report.md:101`. But the same report's archive table (:85-99) gives verified counts of 144 + 252 + 96 + 20 + 8 + 24 + 24 + 24 + 24 + 16 + 3 + 1 = **636**, not 615. Also, `m62b/SHA256_CKPT.txt` holds 18 archive entries where the table says 16. The record is internally inconsistent, and I cannot tell which count is right. | `R/phase6/phase6_report.md:85-101`; `R/phase6/*/SHA256_CKPT.txt` (line counts read this session); DX-408 | The owner reconciles the record. Until then, App F can say "every recorded archive hash matched on re-verification on 2026-09-27", with no count, as §11:24 already does. | C |
| RN2-8 | SHOULD | `ledger_proposals/W4.md:10` (V4-1); `08_methodology.md:55` | "about 50 % power"; "which it detects with 50 % power" | **Is the source acceptable?** Yes, as a ruled convention: CLAUDE.md is where human rulings are transcribed, and the claim is a mathematical fact. The row still needs four fixes. (a) The cited lines are off by one: the 50 % sentence is at `CLAUDE.md:390-391`, the label clause at `:386-388`. (b) Stronger committed sources exist: the ruling itself and the registered design. (c) The number-entry rule wants the derivation shown. An unbiased, symmetric estimate centred on a true effect equal to the bar exceeds the bar with probability ½. Against an uncorrected two-sided 5 % test, 2σ√(2/k) has power Φ(2 − 1.96) = 51.6 %. At the paper's Šidák z_α = 2.2365 it is Φ(−0.2365) = 40.7 %. (d) §8.2 writes a bare "50 %" (the row says "about"), right after defining the Šidák z_α. A reader may apply 50 % at the corrected level, where it is wrong. `07_comms.md:73` ("about half the time") is accurate as written. | log:1801-1805 (AMENDMENT 2026-08-02 to REMEDY RULING 3: "a 50 %-power detection threshold — the project's customary 2σ√(2/k) bar"); `phase6_design_v2.md:198, :207`; `docs/locks.yaml:305` | V4-1: correct the lines, add the log and design sources, and add the one-line derivation (status VERIFIED (DERIVED)). §8.2:55: "… is the effect at which an uncorrected test would just reject, which it detects about half the time;" | B |
| RN2-9 | SHOULD | `ledger_proposals/W5.md:14` (V5-1) | "log:1192-1196" | **Is the source acceptable?** Yes for the count: a count of named record items, and "four" holds at all three places. But log:1192-1196 is the builder's recommendation in the M5.5 report entry. The ruling that counts the four is PHASE-5 CLOSE RULINGS item 2. The "what" column carries RN2-1's wording problem. | log:1241-1252 (":1248 The four invented constants are the builder's"); `CLAUDE.md:343` | Cite log:1248 as the ruling and keep `CLAUDE.md:343` as its transcription. Reword "what" as RN2-1 proposes. | B |
| RN2-10 | SHOULD | `ledger_proposals/W4.md:11` (V4-2); `W6.md:11-13` (V6-1–V6-3) | — | All four values are VERIFIED, but stronger sources exist. **V4-2:** `R/phase5/m55/verdict.txt:3` states the factor outright ("Grading bar: 2x the floor measured on THIS card"), which beats the ratio derivation. **V6-1:** the substantive finding is at log:3661-3676, beyond the cited :3643-3655. **V6-2:** §9.1:54 says "Communication denial had been found inert". The denial study's own verdict is PHASE-5 CLOSE RULINGS item 1, log:1211-1236, on the same date; log:1065 closes the communication axis on message use. **V6-3:** the registration date is ruled at log:1872 ("v2 registered"; PHASE-6 FRAMING + ALLOCATION RULING, owner-approved 2026-08-02). That beats the design header's "rulings incorporated" date. | the lines named | Add the lines to each row's source column. No value changes. | B |
| RN2-11 | SHOULD | `08_methodology.md:47` | "at k = 34, ISO's gave 92.1 % power and JOINT's 62.8 %, where the contrast's power was 76.7 %" | The three powers have no metric, effect size or σ basis. A power figure without its effect cannot be read. The source: completion, a 0.03 effect, σ = M6.2b's 1000-update floors (0.0339 and 0.0483), at the Šidák z_α. All three powers recompute from those inputs to within 0.1 point. | `R/phase6/m62b/m62b_report.md:105-114, :169-177`; METH-3; DES-4 (0.03) | "at $k = 34$`<!-- N:METH-3 -->`, on the 1000-update completion floors and a 0.03`<!-- N:DES-4 -->` effect, ISO's gave …" | B |
| RN2-12 | SHOULD | `09_compositional_test.md:56` | "+0.01209 per 100 updates on the first floor study (2026-08-10<!-- N:DES-5 -->) and +0.0179 …" | The first tag after +0.01209 is DES-5, whose row does not contain 0.01209. DES-10, which holds +0.01209, +0.0179 and −0.0083, comes only at the end of the sentence. A tag-to-number reading pairs the value with the wrong row. | DES-5; DES-10 | Put `<!-- N:DES-10 -->` immediately after +0.01209 and after +0.0179. | B |
| RN2-13 | SHOULD | `09_compositional_test.md:50` | "72 on GPU 1, the RTX 5090 that ran the grid" | The grid's seeds 1–12 of all ten arms ran on an RTX PRO 6000 (App F `14:110`). GPU 1 ran the rest of the grid and the whole confirmatory artifact. | DX-30; `R/phase6/by_card/README.md:49-55` | "… 72 on GPU 1, the RTX 5090 that ran the rest of the grid and every confirmatory run …" | B |
| RN2-14 | SHOULD | `09_compositional_test.md:50` ("seeds 1–60<!-- N:DES-1 -->"), `:66`, `:73`, `:80` | "the registered k = 60<!-- N:DES-1 --> analysis" | DES-1 holds the cap (K_LADDER_CAP 60), not the prefix analysis on seeds 1–60. RES-3 ("registered-ladder prefix") and DX-20 hold that. The value matches, but the row's description does not. | DES-1; RES-3; DX-20 | Add `<!-- N:RES-3 -->` beside DES-1 wherever the k = 60 analysis or seeds 1–60 is meant. | B |
| RN2-15 | SHOULD | `09_compositional_test.md:75` | "All contrasts at θ\*, T\* = 1000, in points …" | Wrong scope for three rows: Γ_H and Γ_H,4 are at β = 0.70, and Γ(2000) is at T = 2000. Each row says so, but the caption's blanket statement does not hold. | DX-26; RES-14; RES-15 | "All contrasts at θ\* and T\* = 1000 unless the row says otherwise, in points …" | B |
| RN2-16 | SHOULD | `09_compositional_test.md:110` | "The drift has not visibly reversed" | §9.1:56 says bias (b)'s sign reverses on the grid GPU (−0.0083). Here "the drift" is a different quantity: the T = 2000 subsample's own training-log slope on GPU 2. It is positive over (500, 1000] (DES-11) and (1000, 2000] (DX-23), and the source compares it with the launch batch's +0.01209. A reader can take the two sentences as contradicting each other. | `post_gamma4_t2000.md:30-35`; DES-10; DES-11; DX-23 | "The subsample's differential slope stays positive from updates 500–1000 to 1000–2000, so the drift it measures has not visibly reversed, which is all it may be cited for." | B |
| RN2-17 | SHOULD | `09_compositional_test.md:125` | "at 0.73 and 0.75 times its floor-based standard error" | The metrics are not named. In the source, completion is 0.73× and survival 0.75×. | `post_evalfloor_gamma_t_high.md:84, :86`; RES-14 | Add "(completion, survival)". | B |
| RN2-18 | SHOULD | `10_limitations.md:30` | "every analysed secondary run, the same-GPU replicate's included, trained on GPU 1 …<!-- N:HW-4 -->" | HW-4 covers Γ, ISO-4, T = 2000 and the post-unblind evaluations. It does not cover the secondary runs on GPU 1; DX-5 does. | HW-4; DX-5 | Add `<!-- N:DX-5 -->`. | B |
| RN2-19 | SHOULD | `13_appendix_locks_floors.md:72` | "design-stage sd(Γ) at k = 40: 0.00504 / 0.00310" | The metrics are not named. | DES-5; `g1_2_report.md:87-88` | Add "(completion / survival)". | B |
| RN2-20 | SHOULD | `13_appendix_locks_floors.md:76` | updates "n/a" | Wrong cell. The partial re-measurement ran the G1.2 protocol at T = 1000 (`g1_floors_card2/README.md:11-12`), so the update count applies. DX-36 does not carry T. | `R/phase6/g1_floors_card2/README.md:11-12`; DX-36 | Write "1000" with a VERIFIED row in `W5.md` (README:11-12), or "—". | B |
| RN2-21 | SHOULD | `13_appendix_locks_floors.md:78` | "cannot be distinguished from the RTX PRO 6000's … [0.0186, 0.0571]" | App C lists three RTX PRO 6000 floor studies at 1000 updates. The interval quoted belongs to the 2026-09-08 re-measurement (ISO completion 0.0281; 7 degrees of freedom gives [0.0186, 0.0571]). | log:4635-4651 (LADDER BRANCH C); `g1_floors_2026-09-08/verdict.txt:10`; DX-35 | "… from the 2026-09-08 RTX PRO 6000 re-measurement's: …" | B |
| RN2-22 | SHOULD | `14_appendix_plan_provenance.md:170, :177` | header "estimate (points)"; "change point … 0.375 [0.125, 0.375]" | The change point is a value of p, not points. | DX-28; `secondary.md:27, :40` | Label the row "change point in p (labelled “knee”)". | B |
| RN2-23 | SHOULD | `08_methodology.md:69` | "the agents drifted towards a wall (rendered-pixel centroids, a diagnostic)" | The measurement is the alive agents' centroid (row 32.3 → 49.2 of 64). The record warns that a centroid cannot separate "all twelve drifted a little" from "four parked on the wall". "The agents drifted" claims more than that. | log:2609-2621 (RENDER-GATE FINDINGS); DX-32 | "In 24 of 24 rendered episodes of the Coupling-B calibration grid, the alive agents' centroid drifted towards a wall (rendered-pixel centroids, a diagnostic)." | B |
| RN2-24 | SHOULD | `14_appendix_plan_provenance.md:45` | "amended 2026-08-13<!-- N:DES-12 -->" | DES-12's 2026-08-13 is the branch registration. The analysis-plan amendment was written into design v2 in the same 2026-08-13 entry, but no row says so. The value matches; the description does not. | log:3104 (PRE-RENTAL DELEGATION AND RATIFICATIONS, 2026-08-13), :3326-3328; `phase6_design_v2.md:343` | Add a VERIFIED row (log:3326-3328), or write "(the frozen analysis plan, amended in the 2026-08-13 ratification that registered the branches)". | B |
| RN2-25 | SHOULD | `09_compositional_test.md:58` | "and a fifth cell, $A_c$" | The count is untagged here; §1:38 tags the same count. | DX-405; `01_introduction.md:38` | Add `<!-- N:DX-405 -->` after "fifth". | B |

## Checked and clean

**New ledger rows (100 %, at source, this session)**
- **V4-1:** the 50 % sentence is in `CLAUDE.md:390-391`, with lines off by one (RN2-8). Its use at `07_comms.md:73` is accurate.
- **V4-2:** bars 0.0799 and 0.0260 are at `phase5_report.md:979-980`, floors 0.0399 and 0.0130 at `:1014-1015`. 2 × 0.039938 = 0.0799 and 2 × 0.0130 = 0.0260. The `m55/verdict.txt:3` statement of the factor confirms the row's value.
- **V5-1:** "four" holds at `CLAUDE.md:343`, log:1192 and log:1248.
- **V6-1 to V6-3, with the orchestrator's four checks:**
  - The comms axis was closed on 2026-07-30 (log:1065; `comms_lock.md:3`); the denial verdict has the same date (log:1211-1236).
  - The inert-share bias was raised on 2026-08-16, pre-grid and pre-unblind (`venue_review_2026-08-16.md:1, :11-14, :112-125, :154, :160-163`; log:3551, :3643-3676). A grep of the log and design v2 before line 3551 found no earlier mention.
  - It was registered with ISO-4 on 2026-09-18, mid-grid at 120 of 252 runs, on the owner's attestation (log:3902-3925, :3970-3989, :4016-4029). 120 = 10 arms × seeds 1–12.
  - The design statements are at `phase6_design_v2.md:29-33` (δ "certified inert", "retained in θ\* for registration fidelity at zero cost") and `:128-133` (the sweeps exclude δ). Its date, 2026-08-02, holds at `:9-10` and log:1872.
  - The premise "Neither protocol trains on δ = 1.0" is at `phase6_design_v2.md:431-433`, and it is false for both arms (`p6_iso.yaml:43, :46`; `p6_joint.yaml:36-37`).
  - All four dates also hold where they are used: `01_introduction.md:40` and `09:54`.

**Supplement rows, 44 of 44, at their cited lines**
- DX-1 to DX-5, DX-15, DX-18 to DX-21, DX-23 to DX-32, DX-34 to DX-36, DX-38 to DX-40, DX-302, DX-303, DX-306, DX-401 to DX-403, DX-405 to DX-414, DX-416, DX-417.
- DX-401 and DX-402: every `ruled:` date and value checked at the cited `locks.yaml` lines.
- DX-4: train 518–521 s and eval 9–10 s, taken as the min and max over the 76 lines of `g1_conf_5090/timings.txt`.
- DX-406: 0.0095531 × 12 = 0.1146.
- DX-417: 0.0269 × 100 = 2.69.
- DX-408's value matches its source; the source is inconsistent (RN2-7).

**Canonical rows, all 64 in scope, at source**
- The random 20 plus the 35 §9 rows are listed in the Summary; the other 19 were checked as well.
- Line refs held, with one exception: METH-3's alternate figure (92.2 % at `m62b_report.md:112`), which the ledger already notes.

**Tags against rows**
- Every tag has the right value, sign and points conversion (×100, two decimals, no re-rounding).
- Fold changes: 2.75 = 0.039938/0.014541; 2.1 = 0.0339/0.0165; 5.2 = 0.0483/0.0093; 1.5 = 1/(2/3); 3× and 2×; 5.40 = 0.0095531/0.00177; 1.78 = 0.0173/0.00970. HW-1's ratios hold from `unblind/report.md:11-12` seed sds over the GPU-1 floors, e.g. 0.0654/0.0587 and 0.0133/0.0112 give 1.11–1.12 and 1.19 from the rounded inputs.
- Scope (arm, k, severity, GPU, run length) is right except for RN2-11, RN2-14, RN2-15, RN2-18 and RN2-24.

**Arithmetic recomputed**
- **Differences of arm means:**
  - Γ: 0.7600 − 0.7772 and 0.9254 − 0.9158.
  - Γ₄: 0.7600 − 0.7726 and 0.9254 − 0.9256.
  - B̂: 0.7726 − 0.7772 and 0.9256 − 0.9158.
  - Γ₄′: 0.7600 − 0.7847 = −0.0247 and 0.9254 − 0.9241.
  - Replicate difference: +0.0121 and −0.0015.
  - Γ_H and Γ_H,4: from DX-26's arm means.
  - Γ(2000) and the k = 60 analysis.
  - All agree with the rows to the source's unrounded last digit.
- **CIs:** every Šidák CI recomputes as Γ ± 2.2365·sd(Γ):
  - the §9.2 table rows, by hand;
  - all 22 App G rows, by script (0 mismatches against `post_evalfloor_gamma_t_high.md:26-54`, with signs).
- **CI bounds read as exclusions:**
  - +0.66 excludes a completion gain.
  - Γ₄'s +0.63 lies above Γ's +0.47.
  - "Every interval containing zero" through t = 850 holds, and survival excludes zero only at 900, 950 and 1000.
  - Completion excludes zero only at t = 750.
- **Exclusion bounds and detection limits:**
  - X = 3.0781 × sd(Γ): 3.29 (0.01068), 4.88 (0.01587), 3.40 (0.01105) and 2.54 (0.00826).
  - Design-stage MDE₈₀: 0.00504 × 3.0781 = 1.55 and 0.00310 × 3.0781 = 0.95.
- **Falsifier:** 1.618 + 2.2365 = 3.855 < 4.433; 1.8035 + 2.2365 = 4.040 < 4.673.
- **Powers:**
  - DES-4's 72.2 % and 80.4 %, from sd(Γ) 0.01301 × √(40/k).
  - DES-6's 71.6 % and 60.2 %, from the realized sd.
  - METH-3's three powers (RN2-11).
  - METH-4's 55.6 %, from sd 0.01262.
  - The contrast-SE form matches ruling (v): `sqrt(s_J²/72 + s_4²/20)`.
- **Floor-based sd(Γ):** 0.00970 and 0.00177, from the GPU-1 floors at k = 72.
- **Shares of the budget:** "last fifth" (900 > 800) and "70 %" (700/1000).
- **T = 2000:** the 95 % intervals are ±1.96·sd.
- **Secondary design:**
  - SEC-3: −0.0237 × (0 − 1/3) = +0.0079.
  - SEC-2 = 0.5 γ_n.
  - γ_p + γ_n equals the sweep slope on survival (3.26 − 2.37 = 0.89) and not on completion (−3.83 against −2.51), as App H says.
  - The triangle identity μ = (1 + p − ν)/2 checks at ISO, ISO-4, JOINT, the sweep (ν = p) and the identification arms (ν = 0.2 + p).
- **Run and hardware-block counts:**
  - 252 = 10 × 20 + 2 × 26.
  - 76 = 144 − 68 copied (`g1_conf_5090/provenance.txt`: "ran_this_invocation: 76 skipped_complete: 68").
  - 96 = 8 × 12.
  - 144 = 2 × 72.
  - HW-3: 280 = 70 + 70 + 69 + 71 of 288.
- **Other:** DX-35's 5090 interval [0.0388, 0.1194] recomputes from s = 0.0587 at 7 degrees of freedom; DX-3's 256 × 128 = 32,768.

**Bias (b) and interval labels**
- §9.1:56 states "The sign reverses on the grid GPU, and no direction is claimed". All three DES-10 readings and both DES-11 slopes match their sources.
- Every interval label matches the source's column header:
  - Šidák: Γ, the k = 60 analysis, Γ₄, Γ₄′, B̂, Γ_H, Γ_H,4, Γ(t).
  - 95 %, not family-corrected: the replicate difference, Γ(2000), the secondary estimates, the mediation slope.
- B̂ carries no verdict word anywhere in scope.

**Registered strings and quotations**
- Present and verbatim where required: "does not survive the inert-share correction", "sign unstable over the final half" (both co-primaries), "second exclusion bound", the a-fortiori sentence, REJECT/null, UNDERPOWERED, VOID, "non-verdict-bearing" (once, §9.1), "sensitivity arm".
- App D quotations: all 12 blocks and the 8 rows of the pre-unblind table are verbatim against their sources, by script. The sources are log:2977-2982, :2991-2993, :4018-4029, :4087-4091, :4141-4145, :4921-4930 and :5058-5063; `phase6_framing_branches.md:160-168, :240-243`; `phase6_design_v2.md:346-351, :362-364`. Omissions are marked […].
- App E: the branch table matches `phase6_framing_branches.md:99-104`, and A_c matches log:4940-4947.

**Other checks**
- **Untagged numbers:** apart from RN2-6 and RN2-25, every numeral in prose, captions, tables, alt text and iframe titles is tagged or exempt. I treated these as labels or names:
  - App G's t column, covered by DES-13 at `14:118`;
  - the arm codes;
  - "GPU 1–3" and the GPU model names;
  - the study codes;
  - the numbers inside cited theorems.
  - Alt texts and titles contain no numbers.
- **Typography and conventions:**
  - No ASCII hyphen-minus before a digit in prose.
  - Every positive interval end carries "+".
  - No cost or dollar figure appears in scope.
- **alt §11:** its numbers and tags are identical to §11 (so RN2-2 applies to both).
