# RN2: numbers, part 2 (Paper v3, step 4.2, draft1 snapshot)

Reviewer lane RN2, 2026-10-14. Read-only except this file.

## Summary

- **Counts:** MUST 0 · SHOULD 7 · OWNER 1.
- **MUST items:** none. Every tagged number in scope matches its row (rounding, points against rates, units), every tag resolves to exactly one row, and every new row's source and arithmetic checks out when redone.
- **OWNER item:** RN2-1. "615 of 615" archives (App. D.8) still matches DX-408 and `phase6_report.md:101`. The report's own table still sums to 636, and `m62b/SHA256_CKPT.txt` still holds 18 entries where the table says 16. v3 carries v2's open question (DISPOSITIONS F1, "carries") but keeps the count in the text, and the v3 provenance row no longer records the inconsistency.

**Scope.** All `<!-- N:ID -->` tags (105 distinct IDs) and every number in snapshot `paper/v3/snapshots/draft1/sections/` files 06, 07, 08, 09, 10, 11, 16, 17, 18, 19, 20 and 21. Every row in `paper/v3/ledger_proposals/W4.md` (X4-1 to X4-5), `W5.md` (X5-1, X5-2) and `IC.md` (IC-1 to IC-6). The snapshot is byte-identical to `paper/v3/sections/` for these files (`diff -q`, no output).

**Method.**
- **The rules.** I read `paper_v3_prompt.md` in full, the decision log from PAPER V2 to the end (log:6036-6244), `paper/v3/BRIEF.md`, and the planner notes.
- **Tag resolution.** A script indexed every row ID in the canonical ledger, `paper/v2/ledger_supplement.md`, `paper/v2/ledger_proposals/*.md` and `paper/v3/ledger_proposals/*.md`. Result: 0 missing IDs, 0 duplicate IDs.
- **Values against rows.** I compared each tagged value with its row by hand.
- **Γ(t) tables.** App. E's two tables were compared cell by cell with `post_evalfloor_gamma_t_high.md:26-54`. They match.
- **New rows.** I re-read every new row's source at its cited file:line and redid each derivation in Python (`statistics.NormalDist`).
- **Build.** I ran `build_v3.py --out <scratch>`: build OK, M1 0, terms, dates and caveats PASS. Its gate lists the 7 PENDING IC tags as final-only failures.
- **Registered strings.** Each quoted registered passage in App. D was checked against the log, `phase6_design_v2.md` and `phase6_framing_branches.md`.
- **Not re-read.** Sources of v2-verified rows used unchanged (v2 RN2 and the provenance record that work). I re-read sources only where v3 adds or recombines.

## Findings

| ID | sev | location (snapshot) | what is wrong | evidence | proposed fix |
|---|---|---|---|---|---|
| RN2-1 | OWNER | `16_appendix_timeline.md:179` (D.8), and D.2 row :63 | "615 of 615" matches DX-408 and its source line, but the source contradicts itself. Its verified column, 144 + 252 + 96 + 20 + 8 + 24 + 24 + 24 + 24 + 16 + 3 + 1, sums to **636**. Of the hash files, `m62b/SHA256_CKPT.txt` has 18 lines where the table says 16. The other directories' files match the table's verified counts; `m60` has no `SHA256_CKPT.txt` (the table puts its hashes in `m06_ARCHIVE.md`). v3 keeps the count. The v3 provenance row (`provenance/16_appendix_timeline.md:162`) drops v2's note of the inconsistency. Separately, the date 2026-09-27 in D.8 is untagged. | `che/bench/results/phase6/phase6_report.md:85-101`; `grep -c . */SHA256_CKPT.txt` (run this session); v2 `REVIEW.md:149` (RN2-7, owner); v3 `DISPOSITIONS.md:192` (F1 carries) | Until the owner reconciles the record: "Every checkpoint archive's recorded sha256 matched on re-verification on 2026-09-27<!-- N:DX-408 -->", with no count. Restore the 636 note in the provenance row. |
| RN2-2 | SHOULD | `07_example_results.md:58` | "on completion, where both gaps are null, Γ₄ is a second exclusion bound". The registered string is present, but the bound is not. The instrument's registered reading names it, "X₄ = 0.0488". BRIEF §6.1 lists the string with that value, and v2 printed it (v2 Figure 3 caption). As written, the sentence excludes nothing a reader can see. | `P6/post_unblind_analysis/post_gamma4_t2000.md:18`; RES-6 ("X₄ 0.0488"); `paper/v3/BRIEF.md:232` (v2 §6.1 copy) | "…Γ₄ is a second exclusion bound, with a detection limit (the registered X₄) of 4.88 points<!-- N:RES-6 -->." Per BRIEF §9.2 trap 5, call it the detection limit, never a CI bound. |
| RN2-3 | SHOULD | `06_example_design.md:56`; `07_example_results.md:80` (Fig. 8 caption); `16_appendix_timeline.md:58`, `:157`; `18_appendix_secondary.md:44` | Untagged numbers that have rows: "a three-seed spread" (CB-9: "3 seeds per arm, graded against a 3-seed σ_seed"; §4.3 tags the same phrase at `04_calibration.md:86`); "the registered 60-seed analysis" (DES-1 / RES-3); "the 2000-update subsample" in the D.2 row and in D.6 (RES-15); "all eight arms" (DX-28: 5 + 3 arms). Minor, inside quoted registered text: D.3 ruling (iv) "All 11" (DES-13) and (viii) "the 144 T\* = 1000 checkpoints" (2 × 72, DES-3). | rows as named | Add the tags: `three-seed<!-- N:CB-9 -->`, `60-seed<!-- N:DES-1 -->`, `2000-update<!-- N:RES-15 -->` (twice), `eight<!-- N:DX-28 -->`. Tags inside quotations are optional; D.3 already tags 2.2365 inside quotes, so tag them consistently or not at all. |
| RN2-4 | SHOULD | `09_example_lesson.md:36` | "ISO-4 trained for 2000<!-- N:DES-13 --><!-- N:DES-14 --> updates would meet each coupling as often as JOINT does in the registered budget". 2000 is a derived number: 1000 (DES-13) × the 2× frequency ratio (DES-14). It also rests on a fixed number of episodes per update, which holds because episodes end only at the horizon (`che/env/env.py:361`, `done = t_new >= cfg.horizon`; DX-3: 256 envs × 128 steps per update). Neither row shows this arithmetic, and the rules say "Derived numbers show their derivation in the row". | DES-13, DES-14; `che/env/env.py:361`; DX-3; log:6160-6161 and item 4, where PAPER V3 names "ISO-4 at 2000 updates" | Add a DERIVED row (W5's file, e.g. X5-3): "2000 updates: ISO-4's per-coupling frequency 1/2 × 2000 = JOINT's 1 × 1000 coupling-episodes per coupling, at equal episodes per update (fixed horizon, env.py:361; DX-3)". Tag 2000 with it. |
| RN2-5 | SHOULD | `16_appendix_timeline.md:176` (D.7, G1.2 row) | The key says "G1.2 \| the main runs' launch floor study (2026-08-10)". In the record, G1.2 names the floor protocol used three times: the 2026-08-10 launch batch, the "G1.2 re-floor on the grid card" of 2026-09-08/09, and the RTX 5090 re-floor ("24 runs, G1.2 protocol"). A figure label "G1.2" on either re-floor would be glossed wrongly. | `phase6_report.md:65`, `:68`; log:4617 ("The 5090 re-floor (24 runs, G1.2 protocol, `g1_floors_5090`)"); V5-3 ("the G1.2 protocol") | "G1.2 \| the floor-study protocol of the main runs: the launch floor study (2026-08-10<!-- N:DES-5 -->) and its re-measurements of 2026-09-08 and on the RTX 5090". |
| RN2-6 | SHOULD | `19_appendix_interaction.md:26` | "the intervals are normal, as for the study's other contrasts". The secondary contrasts (App. F) use 95 % bootstrap intervals over seeds, not normal ones (`18_appendix_secondary.md:18`; DX-27, DX-28 "bootstrap B = 2000"). PLAN's own comparison is with the confirmatory and sensitivity contrasts ("as the project's other contrasts use (Γ₄ at k = 20 included)"). | `che/bench/results/phase6/post_v3_interaction/PLAN.md:108-110`; `P6/secondary/secondary.md:5` | "…the intervals are normal, as for the registered contrasts and Γ₄." |
| RN2-7 | SHOULD | rows and provenance (no text change) | (a) **X4-3.** The identity cites `env.py:446` ("valid at done"). It does not cite the step that makes the evaluated J the final-step value: the harness reduces `survival_rate` with `_FINAL`. The derivation is right; the support is incomplete. (b) **Provenance.** `provenance/16_appendix_timeline.md:145, :148, :152` cite `phase6_framing_branches.md:73` for the M3.3, M4.2 and M5.2 key rows. The line is :71; :73 is the "rare and bursty" row. (c) **IC-4.** It cites PLAN:105-107; the family sentence is at :106-107 (:105 ends the pooled bullet). | `che/eval/harness.py:40, :45`; `phase6_framing_branches.md:71`; PLAN:106-107 | (a) Add `che/eval/harness.py:40, :45` to X4-3's source. (b) Change the citation to `:71`. (c) Change it to PLAN:106-107. |

## Notes (not findings)

- **IC rows in the text.** IC-1 to IC-5 are cited at `08_interaction_check.md:39` and `19_appendix_interaction.md:24-28`. BRIEF §10 says PENDING-COMMIT rows "may not be cited in text until they are VERIFIED". The build gate enforces this: all 7 tags are listed as `--final` failures. They are acceptable by design (preamble rule 4) only while that gate stands, and must flip to VERIFIED once PLAN.md is committed unchanged.
- **The registered-strings sentences carry the registered numbers:**
  - completion Γ "excludes a joint-training gain larger than 0.66 points" (RES-1);
  - the falsifier 3.855 < 4.433 and 4.040 < 4.673 (RES-5), with z_α = 2.2365 (`phase6_framing_branches.md:166`);
  - "11 retained checkpoints, updates 500–1000 at interval 50" (`phase6_framing_branches.md:240`);
  - "MATCHED BUDGET T = 1000" (log:2977);
  - "8 identical reps" (`phase6_design_v2.md:346-347`);
  - "0.01209 per 100 updates" (log:4089-4090);
  - "PROCEED at k = 60…" (log:4620-4621);
  - S1–S6 with {0.125 … 0.375} (log:5058-5063);
  - rulings (iii)–(vii) (log:4921-4930);
  - "Neither protocol trains on δ = 1.0" (`phase6_design_v2.md:431`);
  - the a-fortiori sentence with X = 3.40 and 2.54 points, labelled as detection limits (RES-14).
- **The interaction design text agrees with PLAN.md** (working file, untracked: `git status` shows `?? che/bench/results/phase6/post_v3_interaction/`):
  - the four conditions, with κ_A 0.06 and κ_B 1.0 (the three new configs read this session);
  - δ = 1.0 and β = 0.49;
  - 72 / 72 / 20 final checkpoints at update 1000;
  - seed 0 × 512 with common random numbers;
  - I's definition and sign;
  - Šidák over 8;
  - the observed-SE MDE80;
  - the floor block, 3 × 4 × 3 = 36, and the 2-sigma hurdle labelled post hoc;
  - the cross-GPU comparison and the refusal rule;
  - the pooled pair as headline;
  - §8's blind spots, all present in `08_interaction_check.md:50`.
- **The text around each HOLE reads correctly whatever the result** (08:41-48, 09:33, 19:32-36). Each hole sits between complete sentences that state no sign or size.

## New rows: re-verification (sources re-read this session)

| row | source re-read | arithmetic redone | verdict |
|---|---|---|---|
| X4-1 | `p6_iso.yaml:7`, `p6_iso4.yaml:7`, `p6_joint.yaml:7` (realized marginals); components `p6_iso.yaml:41-46`, `p6_iso4.yaml:36-39`, `p6_joint.yaml:36-37`; `secondary.md:7-16`; the 8 secondary configs' line 7; log:3977-3980 | ISO 1/3 + 1/3 − 0 = 2/3; ISO-4 1; JOINT 1 + 1 − 1 = 1; sweep 1 − p = 1, 0.875, 0.75, 0.625, 0.5; identification 0.8 − p = 0.8, 0.6, 0.4. Each equals 1 − (no-element share) printed in the config headers and in `secondary.md`. ν = 1 − 2μ + p holds at all 8 arms | correct |
| X4-2 | the same component lines; sweep and identification configs `:36-43` (8 components each, all δ 0.0); `theta_star_holdout.yaml:76` (δ 1.0) | n/a | correct |
| X4-3 | `unblind.json:55` (`"survival_rate"`), `:61` (`"gamma": 0.009553128646479725`); `p6_joint.yaml:12` (`n_agents: 12`); `env.py:443-446`; `test_lethality.py:202-203` (the row's correction of DX-406's :201-202 is right); `harness.py:40, :45` | 0.009553128646479725 × 12 = 0.114638 → 0.11 | correct (see RN2-7a) |
| X4-4 | `post_gamma4_t2000.md:9, :15-16`; `p6_post_analysis.py:83-84, :208`; `p6_unblind.py:116-117` | z_α (m = 2) = 2.236477; z_0.8 = 0.841621; sum 3.078098; × 0.00294 = 0.009050; × 0.00289 = 0.008896 | correct. The text uses only Γ₄'s 0.90 points (`07:58`) |
| X4-5 | log:6115 (heading, 2026-10-12), :6158-6169 (item 3); committed, since the working-tree diff starts at :6213 | n/a | correct. Used only in App. D (`16:64`, `:184`) |
| X5-1 | `paper/v3/out/build_summary.json:3` (`zip_bytes` 37705078), `:5` (`files_shipped` 4168); `ls -l out/che_supplement.zip` gives 37705078 | 37,705,078 / 10⁶ = 37.705 → 37.7 MB | value correct; PENDING-COMMIT as marked; cited in no section (grep) |
| X5-2 | `supplement/README.md:126-139` (quote at :130-131; "Not verified" at :136-139); `check_size.py:8, :25` (`LIMIT_BYTES = 100 * 10**6`) | n/a | value correct; PENDING as marked (V3Q24); cited in no section |
| IC-1 | PLAN:68 | (72 + 72 + 20) × 4 = 656 | correct; PENDING-COMMIT |
| IC-2 | PLAN:69-70 | 3 × 4 × 3 = 36 | correct; PENDING-COMMIT |
| IC-3 | PLAN:119-121 | 1 + 3 = 4 copies | correct; PENDING-COMMIT |
| IC-4 | PLAN:106-107; `interaction_analysis.py:61` (`M_FAMILY = len(ESTIMATES) * len(FAMILY)  # 8`) | 4 × 2 = 8 | correct (line nit, RN2-7c); PENDING-COMMIT |
| IC-5 | PLAN:107; `interaction_analysis.py:62`; `test_interaction_check.py:179-182` (asserts 2.7270 ± 1e-3 and "≈ 2.73" in PLAN) | α′ = 1 − 0.95^(1/8) = 0.0063912; z = Φ⁻¹(1 − α′/2) = 2.727008 → 2.73 | correct; PENDING-COMMIT |
| IC-6 | PLAN:71 | 656 + 36 = 692 (not cited in any section) | correct; PENDING-COMMIT |

## Tagged numbers checked (all match; no finding unless listed above)

- **06.** CAL-3 (0.43, 0.70, 0.49); ENV-11; DES-13 (1000, m = 2, 512, seed 0); DES-3 72; DES-1 60; DES-7 (3×); X4-1, DES-14 (2/3, 1, 1); DES-16 (two of six); DES-8 (a third); DES-15 (20); X4-2; DES-10 (last 100 updates).
- **07.** DX-413; DES-9 (0.5, 0.4); DX-28 (p 0–0.5).
  - SEC-1: +3.26 [+1.37, +5.02] and −2.37 [−4.19, −0.57].
  - SEC-3 +0.79, inside B̂'s Šidák interval [+0.33, +1.63]. SEC-4 +3.26 (row value "≈ +0.033"; the text uses the row's own +0.0326 × 1).
  - RES-2, RES-1 (−1.73 [−4.12, +0.66]; 0.66; X 3.29); DES-6 71.6 %; RES-5.
  - RES-6 (−0.03 [−0.68, +0.63]; completion −1.26 [−4.81, +2.28]); X4-4 0.90.
  - RES-8, DX-19 (Γ₄′ −2.47 [−6.16, +1.22]; +0.13 [−0.56, +0.81]); RES-7 (+0.98 [+0.33, +1.63]; −0.46 [−4.05, +3.12]).
  - RES-11; RES-12 (900, 950, 1000; last fifth); RES-13 (700, 70 %); X4-3 0.11, ENV-6 12.
  - Table 3: RES-4, DX-18. The k order follows each contrast's arms (B̂ 20 / 72).
  - Γ = Γ₄ + B̂: −0.0003 + 0.0098 = 0.0095 against 0.0096, which is rounding.
- **08.** COM-6 (δ 1.0); IC-4; CAL-3.
- **10.** DES-13; ENV-2 (3 seeds, 500 updates).
- **11.** DX-5, DX-3 (32,768,000), DX-4 (518–521 s, 9–10 s), DX-407, ENV-6, HW-2, HW-3 (280 of 288, 2.44 × 10⁻⁴).
- **16.**
  - Dates: DX-401, V6-2, V6-3, DES-12 (×5 uses), DX-402, DX-414, DES-5, METH-6, V6-5, DX-36, V6-1, DES-2, DES-15, DES-3, DX-405, DX-102, DX-413, DX-408, X4-5.
  - Counts: DX-30 (252, 76, 96), DX-403 (8; four-run), DX-34, DX-416, DX-411.
  - Statistics: RES-5, ENV-1 (0.5), DES-4 (72.2 / 80.4 %), DES-6 (60.2 / 71.6 %), DES-5 (1.55 / 0.95 points).
  - Bias (b): V6-4 +0.0242; DES-10 (+0.01209, +0.0179, −0.0083; four studies, three on the RTX PRO 6000); DES-11 (+0.00247, +0.00718).
  - GPUs: HW-4, DX-5.
- **17.**
  - DES-13 (11; 500–1000; k = 20); DX-24 and DX-25 (both tables, every cell); RES-13; RES-12; RES-2.
  - k = 60: RES-3, DX-20 (−2.17 [−4.86, +0.52], z −1.80; +1.04 [+0.54, +1.55], z +4.67); DES-6.
  - T = 2000: RES-15 and DX-23 (+0.03 [−3.63, +3.69]; +1.59 [−0.02, +3.19]; +0.00384, +0.00204).
  - High readout: RES-14 (3.40, 2.54; 0.73×, 0.75×); DX-26 (Šidák intervals; Γ_H,4 −0.75, −1.28).
  - Secondary metrics: RES-10, DX-22 (0.1177, z −4.59, 0.6949, 0.8126, −0.4958, z −1.44); HW-1, DX-21 (1.12 / 1.09, 1.25 / 1.19, 5.40, 1.78).
  - Communication: COM-1 (0.498); V4-2 (twice).
- **18.**
  - DX-28 (B = 2000; the arm means); DES-9, X4-1 (the arm table; ν = 1 − 2μ + p; the 0.2 offset); X4-2; DX-18.
  - SEC-5, DX-27, SEC-1, SEC-2, SEC-6, DX-417 (+2.69), DX-39 (±0.4, ±1.1 SE, 8 points, 3 parameters).
  - RES-8, DX-19 (z −1.50; replicate +1.21 [−2.79, +5.20]); RES-9 (−0.15 [−0.86, +0.56]).
  - DX-29 (−1.03 × 10⁻⁵ [−2.91, +0.93] × 10⁻⁵); SEC-7; CO-4; DX-306.
- **19.** CA-1 (0.06); CB-1 (1.0); CAL-3; COM-6; DES-13; DES-3; IC-1 to IC-5; METH-7; ENV-6 (× 12).
- **20.** ENV-13; DX-410 (step 128); ENV-6 (256); DES-3; DES-13.
- **21.** DX-101 (August to October 2026).

## App. D: dates, study codes, seeds, archives

- **Dates.** Every D.2 date matches its row. The rows' sources were checked at v2, and the recombinations are new in v3. One wording point: "2026-07-19 to 2026-07-30" for "the severities" is right, because β_holdout (2026-08-02, DX-401) is the Medium value and is not listed as a separate event.
- **Seeds.** DX-416 and DX-30 match.
- **Archives.** RN2-1.
- **New study-code key rows.** M3.0 (DX-8), M3.4 (DX-9), E1.1 (`e1/e11_report.md:1`) and G1.3 (DX-30) are supported. M3.3, M4.2 and M5.2 are supported at `phase6_framing_branches.md:71` (citation line, RN2-7b). G1.2 is too narrow (RN2-5).
- **The shallow-clone statement** (D.1, `16:38`) holds. `git rev-parse --is-shallow-repository` returns true, and the earliest commit in this checkout is dated 2026-09-22, after the 2026-08-13 registration.

## Re-check (fix2)

Re-checked 2026-10-16 against `paper/v3/snapshots/fix2/` and the live `paper/v3/ledger_proposals/`. Inputs: the writers' resolutions (`resolutions_W3.md:50`, `resolutions_W4.md:35, :45-50`, `resolutions_W5.md:22-23`). I diffed every changed line in sections 06–11 and 16–21, line by line, against draft1 (59 changed lines) and read the new rows X4-6 and X5-3 at their sources. `build_v3.py --out <scratch>/build2`: build OK (0 failures, 9 final-only); M1 0; terms, dates and caveats PASS; the 7 IC tags are still gated as final-only failures.

| finding | verdict | note |
|---|---|---|
| RN2-1 | OWNER | "615 of 615" is kept at `16:181`, with an `OWNER-PENDING:F1` marker at `:182`. Provenance row 149 again records the 636 table sum and the 18-against-16 count for `m62b`. The 2026-09-27 date is now tagged DX-408. |
| RN2-2 | OK | `07:58`: "…so Γ₄ is a second exclusion bound, the registration's term for its detection limit, X₄ = 4.88 points<!-- N:RES-6 -->". The value matches RES-6 (0.0488) and `post_gamma4_t2000.md:18`. It is called a detection limit, as BRIEF trap 5 requires. |
| RN2-3 | OK | Every tag I asked for is present: CB-9 (`06:56`), DES-1 (`07:80`), RES-15 (`16:38`, `:58`, `:159`), DX-28 (`18:44`; also "three" at `07:41`). Inside quotations: DES-13 "All 11" (`16:141`) and DES-3 "144" (`16:145`). |
| RN2-4 | OK | New row X5-3, tagged at `09:36`. Re-derived: per-coupling frequency is 1/2 for ISO-4 and 1 for JOINT (DES-14). Episodes per update E = 256 × 128 / 256 = 128 for every arm, because `done = t_new >= cfg.horizon` (`che/env/env.py:361`), with horizon 256 (ENV-6) and DX-3. ½ · E · U = 1 · E · 1000 gives U = 2000. The design is named at log:6170-6173 (PAPER V3 item 4). The row also states that the cost is matched compute. |
| RN2-5 | OK | `16:178` now names the G1.2 protocol and its three uses (2026-08-10 DES-5; 2026-09-08 DES-2; the RTX 5090 re-measurement). This matches `phase6_report.md:65, :68` and log:4617. W3's `15:30` change ("G1.2 protocol") is consistent. |
| RN2-6 | OK | `19:26`: "the intervals are normal, as for the registered contrasts and Γ₄". This matches PLAN:108-110. |
| RN2-7 (a) | OK | X4-3 now cites `che/eval/harness.py:40, :45` (`_FINAL`), re-read this session. |
| RN2-7 (b) | OK | Provenance/16 now cites `phase6_framing_branches.md:71` three times and `:73` no longer appears. |
| RN2-7 (c) | OK | The orchestrator's fix is in place: IC-4 cites PLAN:106-107 (`IC.md:21`). |

**New rows X4-6 and X5-3.**
- **X4-6.** The checkout is no longer shallow (`git rev-parse --is-shallow-repository` returns false; 211 commits, the first dated 2026-07-18). I re-ran `git log --follow` on all five paths; author and committer dates are identical:
  - `phase6_design_v2.md`: 2026-08-02 01:10:01, 01:16:27 and 15:14:38, then 2026-08-13 23:58:17 (four commits);
  - `phase6_framing_branches.md`: 2026-08-13 23:58:17 (one commit);
  - `g1_grid/provenance.txt`: first committed 2026-09-09 09:57:52;
  - `g1_conf_5090/SHA256_CKPT.txt`: 2026-09-23 10:45:02;
  - `unblind/UNBLIND_LOG.txt`: 2026-09-26 20:49:32.

  All are +0300, and `git status` shows no working-tree change to either registration document. The row's values and D.1's sentence (`16:38`) match. D.1 states no commit hash.
- **X5-3.** Correct (see RN2-4).

**New findings on the changed lines**

| ID | sev | location (fix2) | what is wrong | evidence | proposed fix |
|---|---|---|---|---|---|
| RN2-8 | SHOULD | `16:38` (D.1) and row X4-6 | The commit dates are local dates at UTC+3. The frozen design's first commit, "2026-08-02 01:10:01 +0300", is 2026-08-01 22:10 UTC, so in UTC the design's first commit falls on a different date from the one printed. The row says "+0300"; the text gives no time zone. The other four dates fall on the same day in UTC. This does not change any ordering claim. It matters only because the sentence offers these dates as checkable facts. | `git log --follow --format='%ad \| %cd' --date=iso -- phase6_design_v2.md` | Add "(dates in the committer's local time, UTC+3)" after "…the unblinding log on 2026-09-26<!-- N:X4-6 -->", or carry the time-zone note in X4-6's "what" column and in the provenance row. |

**Other changed lines in my lane checked, all clean.**
- `06:60, :62, :65, :67, :70`: the same tags and values; the per-arm identity values are shortened to 2/3, 1 and 1 (X4-1, DES-14).
- `07:41, :43, :56, :60, :62, :64`. "Detectable only in the last fifth" fits RES-12, whose Šidák exclusions are at t ≥ 900. `07:58` keeps a RES-7 tag on a sentence that no longer states B̂'s value, which still appears in Table 3. That is harmless.
- `08:31, :37, :45`; `10:30, :32`; `11:37, :46, :48` (DX-4's row covers the "1000-update" and "512-episode" figures).
- `16:51, :54, :58, :91-97` (row D now matches the registered table at `phase6_framing_branches.md:104`), `:159`, `:178`, `:181`.
- `18:18, :30, :44, :48`; `19:20, :24, :28, :30`; `21:31, :35` (no numbers).

**Counts (re-check).** Original findings: 7 OK, 1 OWNER, 0 REOPEN, 0 OK-DECLINED. New: 0 MUST, 1 SHOULD (RN2-8), 0 OWNER.
