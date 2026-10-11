# Numbers audit — demonstration draft, sections 00–12

Reviewer: numbers auditor (read-only), 2026-10-11. Scope: `paper/demo_beyond/sections/00_hero.md` … `12_appendix.md`, against `paper/numbers_ledger.md`, `paper/demo_beyond/ledger_supplement.md` (DX-1…DX-40) and `paper/demo_beyond/ledger_proposals/W1–W4.md`, and through them the committed sources. `R/` = `che/bench/results/`, `P6/` = `R/phase6/`, `log` = `docs/decision_log.md`. Claims (overreach or undersell) and kit mechanics are left to the other reviewers.

**Bottom line.** No tagged **value** is wrong. Every one of the 788 tags carries the right value, sign, rounding and conversion to points for its row, and the row agrees with its source. The findings are about **scope**: one registration-status misstatement that contradicts the log (N-1, MUST), several tags that point at a row that does not hold the stated fact, untagged record numbers, and one identity that does not hold on the printed completion numbers (N-10). Nothing from BRIEF §E's NO SOURCE list appears. Nothing contradicts the owner's abstract (`paper/finale.md:13`).

## Findings (non-OK only)

| id | file:line | the text, quoted | tag | row/source value | verdict | severity | fix |
|---|---|---|---|---|---|---|---|
| N-1 | 08_methodology.md:18 | "M5.5 registered a 20 % threshold on a quantity whose run-to-run nondeterminism measures 27.2 %; the observed 23.2 %" | COM-5 | COM-5's note says the report calls the 20 % "registered" and the log calls it "a threshold the RA chose". The log, which wins over the report: "a 20 % threshold that the RA chose" (log:1170-1171). The human had specified only "no cross-arm difference in danger-moment outcomes" (log:1181-1183). | SCOPE | MUST | "M5.5's condition (iii), specified as no cross-arm difference in danger-moment outcomes, was operationalized by the builder with a 20 % threshold, on a quantity whose …". Do not call the threshold registered. |
| N-2 | 07_comms.md:58 | "A third registered condition, on fire deaths per danger agent-step, is VOID, not failed: its 20 % threshold sat below …" | COM-5 | same as N-1 | SCOPE | NOTE | This is consistent with the log only if "registered" attaches to the condition and not to the threshold. Add "a threshold the builder chose". |
| N-3 | 12_appendix.md:29 | "Empirically (M3.3, at L = 32<!-- N:CA-3 --> and L = 64<!-- N:CA-2 -->), the four measured factors compose to the observed slope …" | CA-3 | CA-3 is the **v2 purified** L = 32 test (κ_A 0.003), written after the M3.3 ruling (`R/phase3/phase3_report.md:136-146`). The factor composition at L = 32 used the **v1** slow test ("the slow test measured 1.025", `phase3_report.md:95-104`). The ledger already FIXED one merge of these runs (CA-3 note). | SCOPE | SHOULD | Drop the CA-3 tag. Use the theory doc's wording ("M3.3, L ∈ {32, 64}", `docs/theory_foundations.md:336-338`) with a supplement row for the v1 L = 32 run, or remove "at L = 32". |
| N-4 | 12_appendix.md:77 | "observation version \| v3<!-- N:ENV-7 -->" | ENV-7 | ENV-7 records the 8 channels, not the version. obs_version 3 is in DX-401 (`docs/locks.yaml:243-247`) | MISMATCH | SHOULD | Retag `<!-- N:DX-401 -->`. |
| N-5 | 12_appendix.md:117 | "M6.0 \| RTX PRO 6000<!-- N:METH-2 -->" | METH-2 | METH-2's value and cited lines (`m60_report.md:69-71, :90-91, :109-110`) name no card. DX-5 does ("PRO 6000: … M6.0"; `m60_report.md:10`) | MISMATCH | SHOULD | Retag `<!-- N:DX-5 -->`. |
| N-6 | 12_appendix.md:119 | "M6.2b … \| k = 40; floors grow with run length …" | none | K_CONFIRMATORY 40, ruled 2026-08-03 from the M6.2b CLOSE-OUT (`locks.yaml:295-299`; DES-1, DX-402). M6.2b itself computed power at k = 34 (METH-3) | UNTAGGED | SHOULD | Add `<!-- N:DES-1 --><!-- N:DX-402 -->`. Consider "set k = 40" so the reader does not mistake 40 for M6.2b's own k. |
| N-7 | 08_methodology.md:20 | "The two runs differ in card (RTX 5090 against RTX PRO 6000), code tree and configuration" | none | DX-403: M5.1e on RTX 5090 (`R/phase5/phase5_report.md:1011`), M5.5 on RTX PRO 6000 (`R/phase5/m55/provenance.txt:9`) | UNTAGGED | SHOULD | Add `<!-- N:DX-403 -->` after the parenthesis. |
| N-8 | 05_coupling_a.md:78; 05_coupling_a.md:84 | "The first is confirmed by the 4.83-fold fall"; "The 4.83-fold fall lies far outside those ranges" | none | CA-4 (4.83×) | UNTAGGED | SHOULD | Add `<!-- N:CA-4 -->` at both. |
| N-9 | 12_appendix.md:231-257 | Appendix H: every sd(Γ) cell, and the Šidák CI cells at t = 500–700 and 800–950 (completion) and t = 500–850 (survival) | none (only the Γ(t) cell is tagged) | All 44 sd and CI values match `P6/post_unblind_analysis/post_evalfloor_gamma_t_high.md:26-36, :44-54` digit for digit. DX-24 and DX-25 cover them ("each with its sd(Γ) and Šidák CI") | UNTAGGED | SHOULD | BRIEF B7 puts the tag in the same cell: add DX-24 or DX-25 to each sd and CI cell, or get the keeper's ruling on a single tag in the table lead-in. |
| N-10 | 12_appendix.md:291 | "the sweep slope decomposes as $\gamma_p + \gamma_n$" | none | Survival: +3.26 − 2.37 = +0.89, equal to the sweep slope in the table (:282). **Completion: +2.69 − 6.52 = −3.83, against the printed sweep slope −2.51** (:282, :284, :285; `secondary.md:25, :28`). The identity holds for the plane's slope along the sweep, not for the separately fitted OLS slope in the first row (log:5029-5030 states it as a design property) | ARITH | SHOULD | Write "in the plane, the slope along the sweep is γ_p + γ_n; the sweep's own OLS slope (first row) is a separate fit (completion −2.51 against the plane's −3.83)", or drop the sentence. |
| N-11 | 12_appendix.md:189 | "The secondary specification (ratified 2026-09-26<!-- N:DX-405 -->, before the sweep was read)" | DX-405 | DX-405 is the PRE-UNBLIND RULINGS (i)–(viii), "before the look" (log:4911-4916). S1–S6 were ratified in a later entry the same day, **after** unblinding and before the sweep was read (log:5005, :5058-5063) | SCOPE | SHOULD | The date is right but the row is wrong, and the tag implies the specification came before unblinding. Add a supplement row for log:5058-5063, or cite DES-15 (S5 proposal date, log:5043-5051). |
| N-12 | 10_limitations.md:14 | "Γ uses all 72 seeds of both arms on unit 1, as does every analysed secondary run (seeds 1–12 re-run there, 13–20 from the grid)" | none here (HW-4 closes the next sentence) | 72: DES-3. Seed blocks: log:5013-5016 and DX-30 (secondary re-card, 96 runs) | UNTAGGED | SHOULD | Add `<!-- N:DES-3 -->` and `<!-- N:DX-30 -->`. |
| N-13 | 12_appendix.md:170 | "The mediation void rule (the frozen analysis plan, 2026-08-02<!-- N:DX-402 -->)" | DX-402 | DX-402 holds SIDAK_M's ruling date, not the void rule. The quoted rule is `phase6_design_v2.md:361-364`, a design written against the 2026-08-02 rulings (:9-11) | SCOPE | NOTE | Add a row for the void rule's source and date, or cite the design file. |
| N-14 | 12_appendix.md:212 | "76 runs executed there (seeds 1–12 and 47–72 of both arms) plus seeds 13–46 copied from the grid<!-- N:DX-30 -->" | DX-30 | DX-30 gives 76 executed and 13–46 copied. The seed list "1–12 and 47–72" is in DX-4 (`P6/g1_conf_5090/timings.txt`). Arithmetic: (12 + 26) × 2 = 76 ✓ | SCOPE | NOTE | Add `<!-- N:DX-4 -->`. |
| N-15 | 12_appendix.md:114; :115; 07_comms.md:56 | M5.5 "\| 500<!-- N:DX-40 -->" (two rows); M5.3 "500 updates<!-- N:DX-40 -->" | DX-40 | DX-40's value lists only M4.4, M3.5 and the M5.3b floor; only its note ("all trained policies outside Phase 6 … ran 500 updates") covers M5.5 and M5.3. The sources confirm 500: `R/phase5/m55/provenance.txt:5`; `phase5_report.md` M5.3 protocol ("500 updates") | SCOPE | NOTE | Extend DX-40's value to M5.3 and M5.5, or cite the provenance in DX-403. |
| N-16 | 04_severity.md:43 | "(calibration at $L = 64$<!-- N:CAL-3 -->, 512 seeds<!-- N:CAL-3 -->, no agents)" | CAL-3 ×2 | CAL-3's value has neither L nor seed count (its cited source line does: `calibration_report.md:107`, "L = 64, 512 seeds"). DX-7 and DX-6 carry them | SCOPE | NOTE | Retag `<!-- N:DX-7 -->`. |
| N-17 | 04_severity.md:9 | Figure 5: "one random-policy episode at each level … episode key 0" | none on "episode key 0" | Render rule `paper/figures/interactive/MANIFEST.md:314-317` (`PRNGKey(0)`), DX-202's source | UNTAGGED | NOTE | Add `<!-- N:DX-202 -->` after "episode key 0". |
| N-18 | 08_methodology.md:62; 12_appendix.md:304 | "floors exist only for the sweep's $p = 0.5$<!-- N:DX-28 --> arm"; "Floors exist only for the sweep endpoint p = 0.5" | DX-28; none | True (`P6/secondary/secondary.md:61`), but DX-28's value holds only the p grid, not the floor fact | SCOPE | NOTE | Add the floor fact to a supplement row (secondary.md:61) and tag both places. |
| N-19 | 12_appendix.md:73 | "weak-floor smoothing passes (3 × 3 box)" | none on 3 × 3 | `che/env/structure.py:36` ("3x3 box-smoothing passes"). No ledger row | UNTAGGED | NOTE | Add it to a supplement row (with DX-401's weak_smooth 2) or drop "(3 × 3 box)". |
| N-20 | 09_compositional_test.md:95, :97, :133 | "CI [−0.68, +0.63]" (Γ₄); "CI [−0.56, +0.81]", "CI [−6.16, +1.22]" (Γ₄′); "−0.79 [−3.26, +1.68] and +0.38 [−1.46, +2.23]", "−0.75 [−3.87, +2.36] and −1.28 [−3.50, +0.95]" (Γ_H, Γ_H,4) | RES-6, RES-8, DX-19, RES-14, DX-26 | all Šidák-corrected in source; values OK | SCOPE | NOTE | BRIEF A11 wants the level named in prose. The table lead-in at :79 does not reach these paragraphs. Add "Šidák-corrected 95 %". |
| N-21 | 09_compositional_test.md:97 | "The two copies of the ISO-4 mixture differ across cards by −0.15 survival points … and +1.21 completion points" | RES-9, DX-19 | sweep_c50_p000 − ISO-4 (`secondary.md:52-53`) | SCOPE | NOTE | The sign means nothing without the direction: write "sweep_c50_p000 − ISO-4 is −0.15 …". |
| N-22 | 06_coupling_b.md:73, :75; 08_methodology.md:18; 12_appendix.md:116 | High survival floor as "0.0621", "sd 6.2 points", "0.062" | CB-7 | 0.0621 (`m53b/reproducibility_floor_high.txt:7`) | ROUNDING (consistency) | NOTE | Use one precision: 0.0621, or 6.21 points in prose (A11's two decimals). |
| N-23 | 08_methodology.md:50 | "survival Γ is 5.40 times<!-- N:HW-1 --> its floor-basis sd(Γ) of 0.00177, and completion Γ is 1.78 times its 0.00970 in magnitude<!-- N:DX-21 -->" | DX-21 | 0.00177 is DX-21 (`unblind/report.md:39`), but its tag sits after 0.00970 | UNTAGGED (placement) | NOTE | Put `<!-- N:DX-21 -->` after 0.00177 as well. |
| N-24 | several | Untagged repeats of tagged quantities: 09:29-31, :49 β 0.43/0.70 (CAL-3); 09:55, :72 (figure-note), :91 "k = 72" (DES-3); 09:43 "Seeds 1–60 … 1–72" (DES-1/DES-3); 09:64 and 12:215 "seed 0" (the floor seed; DX-35); 09:72 "RTX 5090 unit(s)" (DX-5); 09:79 "T\* = 1000" (DES-13); 09:122 "p = 1" (DES-7); 09:129 "fitted on p ≤ 0.5" (DX-28); 09:114 "70 % of the budget" sits after its RES-13 tag; 12:113 "δ = 0" and 12:114 "R_comm 16" (METH-1 note, COM-4); 12:121-122 "1000" updates (DX-403); 12:268-274 m and n cells after the first row (DES-9); 12:312 "9 × 9 panels" (ENV-6); 07:50 "1.0000 at every κ_B" (DX-15; the tag is not right after it) | none | all values correct | UNTAGGED | NOTE | Add the tags shown in parentheses. |
| N-25 | 08_methodology.md:54 | "It could never have seen the drift, and nothing said so for three phases." | none | a count taken from `CLAUDE.md` (instruments law, 2026-08-10); no ledger row | UNTAGGED | NOTE | Drop the count ("for several phases") or add a row. |
| N-26 | 06_coupling_b.md:9 | "the four points $x_i + t_s(y - x_i)$, $t_s = (s + \tfrac12)/4$ for $s = 0, \dots, 3$" | none | `che/env/observation.py` (log, Def. 6 note: "a 4-point quadrature"). An implementation constant inside a definition | UNTAGGED | NOTE | It is the keeper's call whether this counts as definitional (A11 exempts theory constants); if not, add a row. |

## Tally

- **Tags.** There are 788 `N:` tags outside code blocks across the 13 files, with 157 distinct IDs, and every ID exists in one of the three ledgers. I checked every one against its row for value, sign, rounding, conversion to points, CI level and scope, and against the committed source wherever a row was opened (below). **0 value mismatches.** 18 tags carry a scope or placement finding: N-1 (MUST); N-3, N-4, N-5, N-11 (SHOULD); N-13, N-14, N-15 ×3, N-16 ×2, N-18, N-20 ×5 (NOTE). **770 tags pass with no finding.**
- **Untagged record numbers.** 8 SHOULD findings (N-6, N-7, N-8 ×2, N-9 covering 44 cells, N-12; N-10 is arithmetic), and about 25 NOTE-level repeats (N-17, N-19, N-23–N-26).
- **Arithmetic recomputed (all OK except N-10).**
  - Ratios: 3× and 2× (1 ÷ ⅓, 1 ÷ ½); 1.5× (1 ÷ ⅔); 4.83× = 4.0527/0.8398; 4.92× = 4.075/0.828; 3.7× = 0.229/0.062.
  - Floors: 1.41× = 0.08765/0.0621; 1.19× = ((−0.0470 − 0.0687 − 0.1066)/3 = −0.0741)/0.0621; 2.75× = 0.0399/0.0145; 2.1× = 0.0339/0.0165; 5.2× = 0.0483/0.0093.
  - "About 0.11 agents per episode": Γ_surv = 0.0095531 (`unblind/unblind.json:61`) × 12 = 0.1146 ✓. DX-406's own arithmetic, 0.0096 × 12 = 0.115, would round to 0.12, but the text is right.
  - Fire deaths 0.8126 − 0.6949 = 0.1177.
  - Hurdle: 5.40× = 0.0095531/0.00177; 1.78× = 0.01727/0.00970.
  - Falsifier: 1.618 + 2.2365 = 3.855 and 1.80 + 2.2365 = 4.04.
  - Drift differentials: 0.02411 − 0.01202 = +0.01209; 0.0405 − 0.0226 = +0.0179; 0.0109 − 0.0192 = −0.0083.
  - Secondary design: 0.5γ_n = −1.19; γ_n·(−⅓) = +0.79; γ_p·1 = +3.26.
  - Γ = Γ₄ + B̂ on arm means: completion −0.0126 − 0.0046 = −0.0172 ≈ −0.0173; survival −0.0003 + 0.0098 ≈ +0.0096.
  - Arm-mean differences reproduce Γ₄, B̂, Γ₄′ and the replicate on both metrics (DX-18 with RES-4).
  - Collapses: 7.81 = 614.4 × 0.012719. "0.4–1.4 %" = (7.848…7.922 − 7.815)/7.815. "7.4–8.3 %" = (8.391…8.461 − 7.815)/7.815.
  - Run counts: 76 = (12 + 26) × 2; 96 = 8 × 12; 144 = 72 × 2; 252 = 120 + 80 + 52; 280 = 70 + 70 + 69 + 71.
  - Budget: 32,768 = 256 × 128; 32,768,000 = 32,768 × 1000.
  - Toy bands: 1.35 = 1.28/0.95; 1.15 = 1.28/1.11.
  - t critical value: Cornish–Fisher on z_α gives 2.2365 + 0.0236 + 0.0002 = 2.2604 = DX-404. The log's "≈ 2.262" (log:4760) is an approximation, not a conflict.
- **Consistency.** No value conflicts between sections, and none with the owner's abstract (4.8-fold, 72 / 60, 0.96 [0.47, 1.44], −1.73 [−4.12, +0.66], final half / last fifth / 70 %, a third, 20 seeds, 0.98, −0.03 [−0.68, +0.63], twice). The only precision split is CB-7 (N-22). "4.8-fold" in §1 against "4.83-fold" in §5, §9 and §10 is the abstract's precision against the row's, and is fine.
- **BRIEF §E NO SOURCE:** none appears. No R_L-centre reproduction claim, no realized-dose values or "0.80×" dose ratio, no supplement size or TMLR limit, no acceptance or odds figure, no drift floor, no "4096 runs per Prop.-3 point" (§7's 4096 is M5.2's episodes, DX-15), no outcome of a rendered episode, no dollars or GPU-hours, nothing beyond DX-24/25 or RES-15/DX-23, no "one in five", no out-degree beyond 1.01 → 2.99.
- **BRIEF A9 lags:** none repeated. B̂ uses the Šidák interval and carries no verdict. T = 2000 slopes come from DES-11/DX-23. 1.41× is scoped as the first estimate. "Seven content planes" is ENV-7-consistent. The grid dates are 09-09 → 09-22.

## Rows opened against their sources

- **Canonical rows used in §9, all VERIFIED:**
  - RES-1–RES-15 (`P6/unblind/report.md:5-41`; `P6/post_unblind_analysis/post_gamma4_t2000.md:9-33`; `post_evalfloor_gamma_t_high.md:20-88`; `P6/secondary/secondary.md:50-53`).
  - SEC-1–SEC-7 (`secondary.md:25-46`; `secondary.json:300-306`).
  - DES-1–DES-16 (log:3868-3876, :3902-3925, :3970-3998, :4558-4566, :4612-4650, :4760-4768, :4911-4950; `P6/g1/g1_2_report.md:3-5, :24-29, :80-88`; `P6/g1_floors_2026-09-08/verdict.txt:32-50`; `P6/g1_floors_5090/verdict.txt:31-50`; `docs/locks.yaml:295-462`; `che/configs/p6_{iso,iso4,joint}.yaml`; `phase6_framing_branches.md:3`; `P6/phase6_report.md:68-76`).
  - HW-1–HW-4, METH-1–METH-7, ENV-2–ENV-7, ENV-10, CAL-1–CAL-5, CA-2–CA-7, CA-9, CB-2–CB-10, CO-1–CO-3, COM-1–COM-5, at their cited lines.
- **Supplement rows spot-checked:** 38 of DX-1…DX-40, all VERIFIED: DX-1–DX-36 and DX-38–DX-40. DX-37 was checked as code (`env.py:398-404`, `structure.py:36-55`).
  - Source quirk, unused in the text: `P6/g1_floors_card2/README.md` says G1.2 ran "12 ISO + 12 JOINT reps", while `g1_2_report.md:5` says 3 arms × 8.

## Proposals rows (DX-1xx … DX-4xx)

| row | verdict | checked at | note |
|---|---|---|---|
| DX-101 | VERIFIED | `paper/finale.md:362-363`; log:2488, :3334; `related_work_verification.md:3, :559, :897`; log:5737 | owner's wording "between August and October 2026" |
| DX-102 | VERIFIED | log:4913-4950 | A_c registered 2026-09-26, pre-look ("no per-arm or cross-arm Phase-6 mean has been computed or viewed") |
| DX-201 | VERIFIED | `severity_lock.md:25-31`; `calibration_report.md:107-109` | |
| DX-202 | VERIFIED | `severity_{low,medium,high}.yaml` (κ_A :30/:33/:32, κ_B :44/:47/:46, δ :54/:58/:57); `MANIFEST.md:314-317` | cited line numbers are ±1–2 off but the values hold |
| DX-203 | VERIFIED | `R/phase3/def4_variance.md:3, :5`; `R/phase2/phase2_report.md:27-30` | |
| DX-204 | VERIFIED | `calibration_report.md:18-26` | (a) 0.504, (b) 0.513 / 0.504, (c) 0.480, [0.480, 0.513], 0.499 |
| DX-301 | VERIFIED | `kappa_b_lock.md:113-119` | |
| DX-302 | VERIFIED | `R/phase5/phase5_report.md:917-922` | |
| DX-303 | VERIFIED | `R/e1/e11_report.md:124-125`; `phase5_report.md:230-231`; also `m55/reproducibility_floor_medium.txt:12` | |
| DX-304 | VERIFIED | `che/calibration/prop3.py:3-6, :67`; `phase3_report.md:20-22` | |
| DX-401 | VERIFIED | `docs/locks.yaml` ruled lines :52 … :247 | every date matches |
| DX-402 | VERIFIED | `locks.yaml:295-462` | T_STAR comment "value unchanged since 08-03" ✓ |
| DX-403 | VERIFIED | `m51e/reproducibility_floor.txt:1-2`; `m55/reproducibility_floor_medium.txt:1, :12`; `m55/provenance.txt:5, :9`; `m53b/provenance.txt:8-9`; `P6/m62/m62_report.md:22-23`; `P6/m62b/m62b_report.md:42, :56`; `g1_2_report.md:3-5`; `g1_floors_2026-09-08/verdict.txt:8, :15` | the M5.1e card (5090) comes from `phase5_report.md:1011`, not from the floor file, which names no card |
| DX-404 | VERIFIED | `P6/unblind/report.md:56` | log:4760 has "≈ 2.262", an approximation; 2.2604 recomputed |
| DX-405 | VERIFIED | log:4911-4930 | do not reuse it for the post-unblind secondary ratification (N-11) |
| DX-406 | VERIFIED (DERIVED) | `unblind/report.md:12`; `unblind/unblind.json:61` | "≈ 0.11" holds on the unrounded Γ (0.0095531 × 12 = 0.1146). The row's shown arithmetic (0.0096 × 12 = 0.115) would round to 0.12: show the unrounded input |
| DX-407 | VERIFIED | `P6/g1_conf_5090/provenance.txt:12-14` | |
| DX-408 | VERIFIED | `P6/phase6_report.md:81-101` | 615 / 615; card2 12 archives, 1 hashed |
| DX-409 | VERIFIED | `phase3_report.md:106-108`; `docs/theory_foundations.md:333-334` | |
| DX-410 | VERIFIED | `paper/figures/interactive/MANIFEST.md:101-104`; `DESIGN.md:424-427` | |
| DX-411 | VERIFIED | `P6/unblind/UNBLIND_LOG.txt`; `POST_UNBLIND_LOG.txt` (2 lines); `SECONDARY_LOG.txt` (1 line) | |

No proposals row is WRONG or UNSUPPORTED.

## Fix-round re-check

Scope: the lines changed in `review/fix_round.diff`, read as word diffs of `sections_v1/` against the current `sections/`; resolutions in `resolutions_W2–W4.md`. The changed lines carry 560 tags (44 more tags than before across the sections: 832 now, against 788; 164 distinct IDs, all present in a ledger). I checked every number that was added or edited for tag, value, rounding and scope.

**Result:** no MUST, no SHOULD. No value is wrong.

**Your N-items:** all 25 items marked fixed are fixed (N-1 to N-25). N-26 was skipped as definitional, which A11 allows, and I accept that.

**New arithmetic, recomputed:**
- **App. I, completion plane prediction:** +2.69 = γ_p 0.0269 × (1 − 0). The ν term is 0 because ν = 0 for both JOINT and ISO-4.
- **§9.2 identity:** deaths per episode = 12 × (1 − survival). Then 12 × 0.0095531 = 0.1146, so "about 0.11" holds.
- **Simplex:** ν = 1 − 2μ + p ⇔ μ = (1 + p − ν)/2.
- **Γ₄ and Γ₄′ completion values in App. I:** these are RES-6 and RES-8.

| id | file:line | the text, quoted | tag | row/source value | verdict | severity | fix |
|---|---|---|---|---|---|---|---|
| N-R1 | 12_appendix.md:263 | "+2.69 ($\gamma_p$ × 1)<!-- N:DX-27 -->" | DX-27 | γ_p (completion) +0.0269 [−0.0675, +0.1245]. The derived +2.69 has no row of its own; SEC-4 is survival only | UNTAGGED (derived, no row) | NOTE | Add a DERIVED row (the completion twin of SEC-4), or accept the inline arithmetic. Consider giving γ_p's 95 % interval beside the prediction, since it contains both measured values. |
| N-R2 | 05_coupling_a.md:78 | "the Coupling-A grid's survival contrasts, on two seeds per arm and with no floor" | none | CA-7 (2 seeds per arm) | UNTAGGED | NOTE | Add `<!-- N:CA-7 -->`. |
| N-R3 | 09_compositional_test.md:69; :100; :136 | "(with its k = 60 prefix as an optional row)"; "Figure 12 shows the 11 checkpoints"; "twice the per-coupling frequency" | none | DES-1; DES-13; DES-14 | UNTAGGED (repeats) | NOTE | Add the three tags. |
| N-R4 | ledger_proposals W3.md (DX-306) and W4.md (DX-415) | the same fact under two IDs | — | both cite `secondary.md:61` ("floors exist only for sweep p = 0.5 …") | duplicate row | NOTE | Merge into one ID when the supplement is consolidated, and retag §8.6 or App. I to match. |

**Changed or new proposals rows, verified at their sources:**

| row | verdict | checked at |
|---|---|---|
| DX-406 | VERIFIED (DERIVED) | `unblind/unblind.json:61` (0.009553…); `che/env/env.py:446` (survival_rate = alive mean); `che/tests/test_lethality.py:201-202` (alive is monotone non-increasing). Arithmetic now uses the unrounded input |
| DX-412 | VERIFIED | `R/phase5/m55/provenance.txt:5` (500 updates), `:8-9` (4 identical runs at seed 0, RTX PRO 6000); `P6/g1_floors_2026-09-08/provenance.txt:7` and `P6/g1_floors_5090/provenance.txt:7` (updates 1000) |
| DX-413 | VERIFIED | log:5005-5008 ("Post-unblind for Γ, pre-look for the sweep"); log:5058-5063 (RATIFIED 2026-09-26, before the sweep was read) |
| DX-414 | VERIFIED | `phase6_design_v2.md:338-340` (§7 Analysis plan (frozen), final-five ruling 4), `:359-364` (void rule); log:1655 (FINAL FIVE, 2026-08-02) |
| DX-415 | VERIFIED | `P6/secondary/secondary.md:61` (duplicates DX-306; see N-R4) |
| DX-416 | VERIFIED | `che/tests/test_p6_grid.py:155-165` (common seed block), `:168-170` (seed 0 never appears) |

DX-202, DX-305 and DX-306 were skipped as instructed: the orchestrator had already verified them.
