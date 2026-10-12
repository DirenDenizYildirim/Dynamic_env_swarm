# RN1: numbers review, part 1 (draft1 snapshot)

Reviewer RN1 (numbers lane), Paper v2 phase 1, step 4, pass 2. Reviewed state:
`paper/v2/snapshots/draft1/sections/` (line numbers below refer to it). Ran
2026-10-11/12, this session. I edited nothing except this file.

## Summary

**Counts: 10 MUST, 5 SHOULD, 1 OWNER.**

The tags themselves hold. All 319 tags in scope resolve to a row, and every
value, sign, rounding and conversion to points matches its row. Every row
used matches its committed source. The MUST items fall into three groups:

- **Two wrong statements.**
  - `03_environment.md:158` says d_p = 0.5 "in every configuration reported
    here". The same subsection reports runs at d_p = 0 (RN1-1).
  - `07_comms.md:71` calls DX-16's "~11 points" the High bar. The row records
    it as the null's resolution, and the bars are 10.44 and 12.43 points
    (RN1-2).
- **Seven untagged record numbers.** Counts of seeds, cells, replicates and
  runs, plus the ratios "twice" and "tripling", and one configured value with
  no row (RN1-3 to RN1-9).
- **One breach of the BRIEF §10 interval convention.** The abstract and both
  of its alternates give "[0.47, 1.44]" (RN1-10).

### What I checked, how, and coverage

| check | method (run this session) | coverage |
|---|---|---|
| 1. every `<!-- N:ID -->` tag in scope against its row (value, scope, wording) | Script `scratchpad/RN1/extract.py` extracts every tag outside STUB-SPEC blocks, with 160 characters of the preceding sentence and the row text. Rows come from `paper/numbers_ledger.md`, `paper/v2/ledger_supplement.md` and `paper/v2/snapshots/draft1/ledger_proposals/W4–W6.md`; the snapshot proposals were checked with `diff -r` and are identical to the live ones. I then read each tag by hand. | **319 of 319 tags (100 %).** By file: abstract 17, hero 1, §1 40, §2 5, §3 29, §4 43, §5 33, §6 49, §7 23. Alternates: disclosure_line 17, no_recommendation 17, hero.ladder 2, severity.no_item4 43. 95 unique IDs, 0 unresolved, 0 duplicate IDs across the three ledger files, and 0 tags preceded by a space. Every tagged ID also appears in that section's provenance support column (script). |
| 2a. supplement and proposal rows against source file:line | I read every cited source line (sed or grep at the file:line each row names). | **31 of 31 (100 %):** DX-1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 33, 37, 40, 101, 102, 201, 202, 203, 204, 301, 304, 305, 401; V4-1, V4-2, V6-1 |
| 2b. canonical-ledger rows against source | Random sample `random.Random(20261011).sample(canon, 20)` over the 64 canonical IDs in scope: CA-1, CA-3, CA-4, CAL-5, CB-4, CB-8, CB-9, COM-4, COM-6, DES-12, DES-7, ENV-10, ENV-12, ENV-13, ENV-4, ENV-5, METH-7, RES-1, RES-6, RES-7. To that I added every row the abstract, hero and §1 use (DES-1, DES-3, DES-8, DES-9, DES-13, DES-14, DES-15, RES-2, RES-11, RES-12, RES-13, ENV-1, ENV-11, CAL-3, CB-5, HW-4, CA-4). The other 28 rows were then checked too. | **64 of 64 (100 %)**. The required 30 % sample plus the mandated rows came to 36 rows (56 %). |
| 3. untagged numerals | Script `scratchpad/RN1/untagged2.py` flags every digit or number word with no tag before the next number or the sentence end. I reviewed each hit by hand. My classification rule: counts of seeds, runs, replicates, cells, ratios and configured values are record numbers (BRIEF §10). Structural counts of arms, tests, panels, conditions, kernels and figure series are definitional (exempt). Section, figure, listing, definition, citation-locator and code-line numbers are exempt. | all 13 files, front matter, title candidates |
| 4. arithmetic | I recomputed each derived number (Python) and show it in the table at the end. | every derived number in scope |
| 5. registered strings and bounds | Read against RES-1, RES-2, RES-6, RES-7, RES-11 to RES-13, DES-1, DES-3 and DES-15. | abstract (all three variants), hero alternate, §1 |
| 6. figure-printed numbers | I extracted the embedded data and labels from `opening_ladder.html`, `composer_training_mixtures.html`, `severity_explorer.html`, `coupling_a_explorer.html` and `explorer_thetastar_random_seed0.html` (default view). I viewed `fig04_coupling_b.png`, `fig05_coactive.png`, `fig06_comms.png` and `severity_explorer.png`. | Figures 1, 2, 3, 5, 6, 7, 8, 9 and the hero-ladder alternate |
| front matter and title candidates | `yaml.safe_load` of `front_matter.yaml`, regex for digits; `len()` of the five candidates in `provenance/00_abstract.md:55-59` | title, `description`: 0 numerals. Candidate lengths 109 / 75 / 171 / 172 / 139 match the stated counts. No candidate contains a numeral. |
| built page | grep of the draft1 kit `index.html` for 11 tagged strings (for example "20-seed", "4.83-fold", "32,768,000", "agent 7") and for `<!--` | every number renders as written, with tags stripped; 0 `<!--` |

## Findings

| ID | severity | file:line | quoted text (short) | problem | evidence | proposed fix | class |
|---|---|---|---|---|---|---|---|
| RN1-1 | MUST | `03_environment.md:158` | "each death costs a fixed $d_p = 0.5$ … in every configuration reported here (the code's default is 0)" | The scope is wrong, and the claim contradicts the same subsection. `:186` reports results at d_p = 0 ("Raising $d_p$ from 0 to 0.5 moved High survival from 0.575 …"). ENV-1's scope is "every **live** config carries 0.5", not every configuration the paper reports. The error came from the stub (`03_environment.md:9`, "in every configuration reported") and the demo ("in every configuration this paper reports"). | ENV-1 (`numbers_ledger.md:30`); M2.5 grid "death_penalty ∈ {0.0, 0.5}" (`che/bench/results/phase2/phase2_report.md:29`, table :38-47); ENV-2 to ENV-5 | Write "in every configuration reported here except the d_p ablation below (the code's default is 0)", or "in every trained configuration of the main experiment and the calibration grids". | B |
| RN1-2 | MUST | `07_comms.md:71` | "The wider High floor puts that bar at about 11 points<!-- N:DX-16 -->." | This misreads the row. DX-16 records the High null's **resolution**, "no effect larger than ~11 points", not its bar. The M5.3b bars are twice the measured High floors: completion 0.1044 and survival 0.1243, so 10.44 and 12.43 points. Neither is "about 11". The sentence is new in v2 (provenance row 35, "split from the previous sentence"). | DX-16 (`ledger_supplement.md:51`); `phase5_report.md:877-880` (High floor 0.0522 / 0.0621; "bar = 2×" 0.1044 / 0.1243); `:912-914` ("This null means 'no effect larger than ~11 points'"); `comms_lock.md:38-40` ("bound < 11 points") | Use the row's wording: "At High the wider floor means that null excludes only effects larger than about 11 points<!-- N:DX-16 -->." Alternatively, give both bars (10.44, 12.43) after adding a VERIFIED row at `phase5_report.md:879-880`. | B |
| RN1-3 | MUST | `05_coupling_a.md:97` | "Across all nine measured cells (two arms of the Coupling-B grid and one of the Coupling-A grid, at three severities)" | Untagged record count. The only tag in the sentence, CA-6, follows the range [0.164, 0.203] at its end. BRIEF §10 requires the tag right after the number. | CA-6 note: "9 cells: m44 × 6 and m35 × 3" (`numbers_ledger.md:63`); source `R/e1/e11_report.md:59-60` | "nine<!-- N:CA-6 --> measured cells" | B |
| RN1-4 | MUST | `05_coupling_a.md:99` | "which two seeds per arm only suggest" | Untagged seed count. The same count is tagged at `:93` but not here. | CA-7 note: "2 seeds per arm" (`numbers_ledger.md:64`); `phase3_report.md:153` | "two seeds per arm<!-- N:CA-7 -->" | B |
| RN1-5 | MUST | `06_coupling_b.md:76` (Figure 7 caption) | "(b) The High survival contrasts between the arms: three replicates, then the first estimate." | Untagged replicate count in a `<p class="caption">`, which can carry tags. | CB-5 "direction 3/3"; DX-13 lists the three contrasts (`ledger_supplement.md:48`) | "three replicates<!-- N:DX-13 -->" | B |
| RN1-6 | MUST | `06_coupling_b.md:78` | "for the grid's two seeds"; "the mean of its two seeds, was −8.8 points"; "against a two-seed spread"; "each one run per cell" | Four untagged seed or run counts. The tags present (DX-13, CB-6) do not sit after these numbers. | DX-40 "2 seeds (3 at Medium)" (`ledger_supplement.md:75`); CB-6 "the first 2-seed M4.4 estimate" (`numbers_ledger.md:77`); DX-38 "the two-seed spread M4.4 graded its High survival effect against" (`ledger_supplement.md:73`); DX-13 note "one run per cell" | "two seeds<!-- N:DX-40 -->" (both places, or CB-6 on the second); "a two-seed<!-- N:DX-38 --> spread"; "one run per cell<!-- N:DX-13 -->" | B |
| RN1-7 | MUST | `06_coupling_b.md:80` | "It was judged against a three-seed spread, $\sigma_{\mathrm{seed}} = 0.72$ points" | Untagged seed count. The CB-9 tag after 0.72 covers σ_seed, not the "three". | CB-9 note: "3 seeds per arm, graded against a 3-seed σ_seed of 0.0072" (`numbers_ledger.md:80`); `phase4_report.md:313` (three per-seed values) | "a three-seed<!-- N:CB-9 --> spread" | B |
| RN1-8 | MUST | `07_comms.md:71` | "a bar of twice the earlier Medium floor, about 3 points<!-- N:COM-2 -->"; "found that tripling the mean alive out-degree, from 1.01 to 2.99<!-- N:COM-3 -->" | Two untagged ratios. BRIEF §10 names "twice" as a record number. "Tripling" is 2.99 / 1.01 = 2.96. COM-3's row value does not contain the word, but its source does. | COM-2 note: "Bar = 2 × the M5.1e floor" (`numbers_ledger.md:97`); `phase5_report.md:684-685` (bars 0.0290 / 0.0258); `phase5_report.md:902-903` ("Cell B tripled mean alive out-degree (1.01 → 2.99)") | "twice<!-- N:COM-2 --> the earlier Medium floor"; "tripling<!-- N:COM-3 -->", or "raising … from 1.01 to 2.99" | B |
| RN1-9 | MUST | `03_environment.md:128` | "Every episode starts from an all-Fuel grid with one Burning cell at a uniformly random position (`che/env/env.py:241-243`)" | A configured value (one initial ignition per episode) with no ledger row. It is supported only by an inline file:line, which BRIEF §2 and §10 do not accept for a number. No row in the ledger, the supplement or the proposals covers it (grep, this session). | `che/env/env.py:241-243` (`fire_cell = jax.random.randint(...)`; `hazard.at[fire_cell[0], fire_cell[1]].set(BURNING)`), read this session; BRIEF §10 "configured … value" | Add a VERIFIED row read at `env.py:241-243` (W3 has no proposals file, so open `ledger_proposals/W3.md`, V3-1) and tag "one<!-- N:V3-1 -->". If the owner rules the count definitional (it is Proposition 2's hypothesis), record that ruling instead. | B |
| RN1-10 | MUST | `00_abstract.md:26`; `alt/00_abstract.disclosure_line.md:11`; `alt/00_abstract.no_recommendation.md:11` | "(Šidák-corrected 95 % CI [0.47, 1.44])" | Breaks BRIEF §10's units rule ("`+` on positive interval ends"). The same sentence writes "[−4.12, +0.66]", and §1 (`01_introduction.md:51`) writes "[+0.47, +1.44]", so the abstract and §1 disagree in form. The values are right (RES-2 [+0.0047, +0.0144]). The owner's abstract (`paper/finale.md:13`) and the abstract stub both read "[0.47, 1.44]". | BRIEF §10 (units); RES-2 (`numbers_ledger.md:141`); `unblind/report.md:12` | "[+0.47, +1.44]" in all three files. The provenance row keeps the owner's "[0.47, 1.44]" for revert. | B |
| RN1-11 | SHOULD | `06_coupling_b.md:82`; `05_coupling_a.md:91` | "against 0.00068, 0.00249 and 0.01559 …: 118, 22 and 16 times"; "4.05, 3.41 and 0.84 … a 4.83-fold fall" | The ratios are right, but they were computed from unrounded inputs. A reader who recomputes from the printed values gets 0.0809 / 0.00068 = **119.0** (not 118) and 4.05 / 0.84 = **4.82** (not 4.83), which looks like an arithmetic slip. | CB-10 note "15.55 / 22.47 / 118.31" (`numbers_ledger.md:81`); unrounded 0.0006837, 0.08089 → 118.31 (`R/phase4/m44/m44_analysis.json:585-587`); CA-4 note "4.0527 / 0.8398 = 4.83 (from the rounded inputs, 4.82)" (`numbers_ledger.md:61`) | Print the unrounded denominators (0.000684; 4.053 and 0.840), or add "(ratios of unrounded values)". | B |
| RN1-12 | SHOULD | `07_comms.md:73` | "Both bars are twice<!-- N:V4-2 --> the floor sd measured on that GPU" | "That GPU" has no antecedent: §7.3 names no GPU. The row's scope is "measured on the same GPU" as the study (RTX PRO 6000). | V4-2 (`ledger_proposals/W4.md:11`); `phase5_report.md:955` ("Run 2026-07-30 on an RTX PRO 6000"), `:1012-1015` | "the floor sd measured on the GPU that ran the study" | B |
| RN1-13 | SHOULD | `06_coupling_b.md:80` | "the Medium survival floor measured later is 1.29 points<!-- N:METH-1 -->" | Two Medium survival floors were measured later, on two GPUs: 0.0129 (M5.1e, RTX 5090) and 0.0130 (M5.5, RTX PRO 6000). "The" floor picks one without naming its GPU. Floors are per-hardware facts (`CLAUDE.md`, "Bars come with floors"). | METH-1 (`numbers_ledger.md:107`); `phase5_report.md:1012-1015` | "the Medium survival floors measured later are 1.29 and 1.30 points, on two GPUs<!-- N:METH-1 -->", or name the RTX 5090 | B |
| RN1-14 | SHOULD | `00_abstract.md:26` (and both abstract alternates, `:11`) | "joint training's survival differs from that arm's by −0.03 points (CI [−0.68, +0.63])" | The Γ₄ interval is unlabelled. ISO-4 is outside the confirmatory family yet corrected at Šidák m = 2 "as the family", so a reader cannot infer the correction. BRIEF §10 labels Γ₄'s interval "Šidák-corrected 95 % CI". §1:53 labels it; the abstract does not. Budget: 2,457 of 2,600 characters, so "Šidák-corrected " (16) fits. The word budget is already exceeded (372 of 360, disclosed in the provenance). | RES-6 "Šidák CI" (`numbers_ledger.md:145`); `post_gamma4_t2000.md:5` ("Šidák m = 2 … as the family"); BRIEF §10 interval labels | "(Šidák-corrected CI [−0.68, +0.63])", or leave as is if the owner accepts the abbreviation after the first label | B |
| RN1-15 | SHOULD | `06_coupling_b.md:66`, `:68` (H3), `:70`; `04_severity.md:22` (and `alt/04_severity.no_item4.md:11`) | "under a three-condition gate"; "6.3 The lock: three bands that did not intersect"; "three bands set before calibration"; "the three levels" | Untagged structural counts that the record states. I judged them definitional under BRIEF §10, so this is not a MUST. However, §1:25 tags the same kind of count ("the three<!-- N:CAL-3 --> severities"), so the paper is inconsistent. | CB-4 (gate statistics; "three-condition gate", `phase4_report.md:85-87`); DX-301 ("the three bands", `ledger_supplement.md:89`); CAL-3 | Either tag the prose counts (CB-4, DX-301, CAL-3) and leave the heading bare (a tag there would break the slug), or untag §1:25's "three" | B |
| RN1-16 | OWNER | `02_related_work.md:45`, `:47` (and author-year citations throughout §2–§4) | "in all six cells, one a tie"; "Of their six training arms"; "one or two types at a time"; "(Hu et al., 2025, revised 2026)" | A rule gap. BRIEF §10 defines a record number as a measured, ruled, configured, derived or dated value, and exempts section, figure and definition numbers, definitional counts and theory constants. It says nothing about numerals that describe **cited works**, which carry no tag. I verified each against its citation record, so none is wrong. | `paper/related_work_verification.md:1038-1043` ("6 of 6 cells, one tie"; "Six training arms"); `:951` (Hu et al., v2, 2026); `paper/finale.md:320` ("one or two noise types at a time"); every citation year matches `paper/v2/assets/bibliography/submission.bib` (checked for 20 keys) | Owner: rule that cited-work numerals are exempt because the citation audit governs them, or ask writers to put the audit's line in the provenance support column. The provenance already cites it for these rows. | C |

## Arithmetic, recomputed (Python, this session)

| where | number | computation | result |
|---|---|---|---|
| abstract, §1 | 0.96 [0.47, 1.44]; −1.73 [−4.12, +0.66]; bound 0.66 | RES-2 +0.0096 [+0.0047, +0.0144] × 100; RES-1 −0.0173 [−0.0412, +0.0066] × 100; bound = upper end | ✓ |
| abstract, §1 | −0.03 [−0.68, +0.63]; 0.98 | RES-6 −0.0003 (unrounded −0.000263 → −0.026) [−0.0068, +0.0063] × 100; RES-7 +0.0098 × 100 | ✓ |
| abstract, §1 | "last fifth" | exclusions only at t = 900, 950, 1000, all above 0.8 × 1000 (`post_evalfloor_gamma_t_high.md:52-54`) | ✓ |
| abstract, §1 | "70 %" | completion signs negative at t = 700…1000 (`:38`); 700 / 1000 | ✓ |
| abstract, §1, §7 | "a third", "two thirds", "one" | δ-only 2 of 6 components at 1/6 each = 1/3; active share 1 − 1/3 = 2/3; JOINT 1 (`p6_iso.yaml:41-46`, `p6_joint.yaml:36-37`) | ✓ |
| §1, §2 | "three times", "twice" | marginal 1.0 / 0.3333 = 3; 1.0 / 0.5 = 2 (log:4562-4563; `p6_iso4.yaml:36-39`) | ✓ |
| §1 | "a fifth" outcome | four on 2026-08-13 (DES-12) + A_c (DX-102) = 5 | ✓ |
| §1 | 4.8-fold | 4.0527 / 0.8398 = 4.826 → 4.83 → 4.8 (BRIEF §9.2 and the stub use 4.8) | ✓ |
| §3 | 32,768; 32,768,000 | 128 × 256; × 1000 | ✓ |
| §3, §5 | nine times | (5e-5 + 4e-4) / 5e-5 = 9 | ✓ |
| §5 | 7.81; 0.4–1.4 %; 7.4–8.3 %; 6.9–7.6 % | 0.15 × 4096 × [1 − (1 − 5e-5)^256] = 7.8144. Trained 7.848–7.922: increase 0.43 %–1.38 %. Random 8.391–8.461: increase 7.38 %–8.27 %, share 6.87 %–7.64 % (`phase3_report.md:187-218`) | ✓ |
| §5 | 3 × 3 | 2 r_A + 1 = 3 (r_A = 1) | ✓ |
| §5 | 14× | 10.283 / 0.716 = 14.36 (`coupling_a_explorer.html` prop3 x) | ✓ |
| §5 | 4.83-fold; 4.92-fold | 4.0527 / 0.8398 = 4.826; 4.0752 / 0.8281 = 4.921 | ✓ (see RN1-11) |
| §4 | 83 % | 0.83 / 1 cell per step | ✓ |
| §4 | Medium between 0.486 and 0.500 | 0.486 < 0.49 < 0.500 | ✓ |
| §4 | estimators "bracket ½" | spread [0.480, 0.513] contains 0.5 | ✓ |
| §6 | 1.41×; 1.19× | 0.0876 / 0.0621 = 1.411; (0.0687 + 0.1066 + 0.0470) / 3 = 0.0741, / 0.0621 = 1.193 | ✓ |
| §6 | −8.8 | (−6.87 − 10.66) / 2 = −8.765. Matches CB-6's stated value "−8.8 points (−0.08765)" and the registered "8.8-point". | ✓ |
| §6 | −0.03; 0.72; 1.29; 6.21 points | CB-9 −0.000271 × 100; 0.00716 × 100; METH-1 0.0129 × 100; CB-7 0.0621 × 100 | ✓ |
| §6 | 118 / 22 / 16 | unrounded 118.31 / 22.47 / 15.55 | ✓ (see RN1-11) |
| §6 | 1.35×; 1.15× | 1.28 / 0.95 = 1.347; 1.28 / 1.11 = 1.153 (`kappa_b_lock.md:150-151`, `:262-265`) | ✓ |
| §6 | 0.130 below 0.150 | as stated (`kappa_b_lock.md:163-169`) | ✓ |
| §6 | radius 4 | 9 // 2 | ✓ |
| §6 | seven plus eighth plane | 6 indicators + smoke = 7; + visibility = 8 (`observation.py:22-33`) | ✓ |
| §7 | +0.38 / 7.99; −1.43 / 2.60 | COM-4 × 100 | ✓ |
| §7 | twice (denial bars) | 2 × 0.039938 = 0.0799; 2 × 0.0130 = 0.0260 | ✓ |
| §7 | about 3 points | 2 × 0.0145 = 0.0290; 2 × 0.0129 = 0.0258 | ✓ |
| §7 | about 11 points | the bars are 0.1044 and 0.1243 | ✗ as a bar (RN1-2) |
| §7 | tripling | 2.99 / 1.01 = 2.96 (2.981 / 1.013 = 2.94) | ✓ (untagged, RN1-8) |
| §7 | 0.498 | 0.4982 (`phase5_report.md:558`) | ✓ |
| provenance | title lengths | `len()` = 109, 75, 171, 172, 139; ≈ 26 characters a line (P2.md:215-216): 109/26 = 4.2, 75/26 = 2.9, 171/26 = 6.6 | ✓ |

## Checked and clean

- **Results rows at source.**
  - RES-1, RES-2: `unblind/report.md:11-12`.
  - RES-6, RES-7: `post_gamma4_t2000.md:12-18`.
  - X and X₄ are the "MDE80" columns, so Figure 3's "minimum detectable effect at 80 % power" holds.
  - RES-11: `post_evalfloor_gamma_t_high.md:38, :56`. RES-12: `:52-54`. RES-13: `:31, :38`.
  - All conversions to points are exact, with two decimals and no re-rounding.
- **Registered strings and bounds** (abstract and both alternates, §1, hero alternate):
  - "sign unstable over the final half" is on both co-primaries.
  - "does not survive the inert-share correction" is verbatim, with "the".
  - "excludes a joint-training gain larger than 0.66 points" is present; it is not confused with X 3.29.
  - k = 72 appears with "above the registered cap of 60, a recorded deviation made before unblinding". DES-1 is at log:4765 and DES-3 at log:4616-4623 (cap raised 60 → 72, "a deviation from a registered rule … pre-unblind").
  - B̂ (§1:53) is "an estimate with no registered test", with no verdict word. The abstract omits B̂, as its stub allows.
  - "Šidák-corrected for m = 2" is present.
- **Design and registration rows.**
  - DES-7, DES-8, DES-9, DES-12, DES-13, DES-14, DES-15 and HW-4 read at their sources (log:3902-3913, :3970-3999, :4560-4564; the p6 configs; `secondary.md:7-16`; `phase6_framing_branches.md:1-5, :99-104`; `phase6_report.md:68-76`; `docs/locks.yaml:323, :342, :373, :405, :458`; `by_card/README.md:29-36`).
  - V6-1 read at `docs/venue_review_2026-08-16.md:1, :11-14, :112, :120-124, :152-164` and log:3551, :3643-3655.
  - The F3 dates in §1:40 (2026-08-16, 2026-09-18) and "mid-grid, before unblinding" match V6-1 and DES-15.
- **Environment rows.**
  - ENV-1: `locks.yaml:223-228`, `config.py:37`, log:23.
  - ENV-2 to ENV-5: `phase2_report.md:28-47`. This confirms §3.3's scope wording: fire only, 3 seeds, 500 updates, "means over the last 50 logged updates".
  - ENV-6: `p6_joint.yaml:11-16`. The same instance is in `severity_{low,medium,high}.yaml`, `p6_iso.yaml`, `p6_iso4.yaml` and `theta_star_holdout.yaml`, so §3.5's "every trained policy … one instance" holds for the live configs.
  - ENV-7: `observation.py:22-33`; the six named indicators are right.
  - ENV-8 to ENV-12: `env.py:48`, `tasks.py:31-34`, `networks.py:70, :85-111` (hidden 128, heads 64, tanh message head), `run_p6_grid.sh:299`, `ippo.py:323-329`.
  - Completion = 1 − F/32 (`env.py:447`); survival = final alive fraction (`env.py:446`; `harness.py:42-46`).
- **Calibration rows.**
  - CAL-1, CAL-2: `severity_lock.md:3-16`. This includes "independently recomputed by the RA", which §4.3 paraphrases correctly.
  - CAL-3, CAL-4, DX-6, DX-201: `calibration_report.md:105-110`, `severity_lock.md:22-31`.
  - DX-7, DX-204: `calibration_report.md:1-36`.
  - CAL-5, DX-8, DX-203: `def4_variance.md:1-8, :40-62, :100-112`. "Both above High" and "medium >> high > low" are verbatim at the source.
- **Coupling A.**
  - CA-1: `coupling_a_lock.md:77`.
  - CA-2: `phase3_report.md:110-116`; `prop3_L64.json:44-53` (R² 0.99789, κ_A 0.02, f_weak 0.4, fit through the origin on realized seeds).
  - CA-3: `:144-145`. CA-4, CA-6: `e11_report.md:50-62`. CA-5, CA-7, CA-9, DX-10: `phase3_report.md:178-245`.
  - CA-8: `structure.py:76-79`, `tasks.py:16-19`.
  - DX-9: `coupling_a_lock.md:44-52, :75-92`; `e11_report.md:10-30, :168-198`. §5.3's account of the three-part prediction matches the source, including the CORRECTION.
  - DX-304: `prop3.py:1-12, :60-70`; `phase3_report.md:18-23`. DX-37: `env.py:396-404`. DX-40: `phase4_report.md:227-236`, `phase3_report.md:153-157`, `reproducibility_floor_high.txt:1-8`.
- **Coupling B.**
  - CB-1, CB-2, DX-12, DX-301: `kappa_b_lock.md:1-9, :111-190, :248-266, :410-418`; `locks.yaml:160-167`.
  - CB-4, DX-14: `phase4_report.md:83-106`. CB-5, CB-7, DX-13, CB-8: `phase4_report.md:594-610, :636-644`; `replicate_deltas.txt:1-19`.
  - CB-6, CB-9: `phase4_report.md:310-316`; `m44_analysis.json:205-218`. DX-11, CB-10: `phase4_report.md:355-366`, `m44_analysis.json:576-612`.
  - CO-1 to CO-4: `phase4_report.md:420-428`, `e11_report.md:205-211`, `env.py:398-404`.
  - DX-33: the MANIFEST lines and the digests JSON (11 collapses, 7 seeded ignitions). The explorer's state is `t0 = 128`, `agent0 = 6`, displayed as agent 7.
- **Comms.**
  - COM-1, DX-15: `phase5_report.md:538-589`. COM-2: `:655-660, :684-685`. COM-3: `:888-904`. COM-4: `:955-982`. METH-1, V4-2: `:1008-1028`.
  - DX-16: `:912-914` (and bars `:877-880`); `comms_lock.md:36-40`. DX-17: `comms.py:60-63`, `networks.py:18-37, :105-112`. DX-305: `m53/provenance.txt:1-7`.
  - COM-6, DX-401: `locks.yaml` "ruled:" lines 52 to 247, all as DX-401 lists.
  - V4-1: `CLAUDE.md:383-391`. DX-101: `paper/finale.md:362-363`. DX-102: log:4913-4916, :4924.
- **Figures.**
  - Figure 2 (composer data): 1/6, 1/4, 1/2 components; per-coupling 1/3, 1/2, 1; active 2/3, 1, 1; "3× ISO · 2× ISO-4". This matches §1:40 and §2:43, :45.
  - Figure 3 (opening ladder data): REJECT and null flags; X₄ = 0.0488; Γ₄ completion interval with `ci: null` ("drawn but not printed" holds); k 72, cap 60, 2026-09-18 and 2026-09-22 in the foot. Neither caption repeats a printed number.
  - Figure 5: the subtitle prints "δ 0" and the caption repeats it. This is deliberate: class B, P2-1, because the static companion cuts "δ" at the edge, which I confirmed in `severity_explorer.png`.
  - Figure 6 (data): 4.05, 3.41, 0.84 / 4.83×; 4.08, 3.42, 0.83 / 4.92×; [0.164, 0.203]; R² 0.998; 0.992, [0.90, 1.02], R² 0.9995; L = 32, κ_A 0.003. All match §5.
  - Figure 7 (PNG): −0.0687, −0.1066, −0.0470, −0.0876, 118×/22×/16×, and "floor: ±1 sd = 0.0621, 4 identical High runs". These match §6.4, and the caption repeats none of them.
  - Figure 8: 0.563 / 0.578 / 0.883 match §6.5.
  - Figure 9: +0.0038 / −0.0143, "±2 × floor sd: the M5.5 bar", 4 seeds. These match §7.3.
- **Alternates.**
  - Both abstract alternates have the same tag sequence as the abstract (md5 of the tag list) and identical text apart from the recommendation and footnote changes (diff).
  - `alt/04_severity.no_item4.md` differs from §4 only in Corollary 1 (diff); its numbers are identical.
  - `alt/00_hero.ladder.md`: DES-13 ("one common evaluation draw", seed 0 × 512, `unblind/report.md:5`) and METH-7 are correct.
- **Other.**
  - No BRIEF §17 "NO SOURCE" number appears in scope. Grep this session for 43/18, 4/3, "one in five", 0.0090, 0.0089, 0.80×, $ amounts and GPU-hours: hits occur only inside STUB-SPEC blocks.
  - Citation years in §2–§4 match the bib for all 20 keys checked. The Garet & Marchand 2004 entry includes pages 169–199, which contain Corollary 5.4.
  - Code line ranges cited in §3 hold where I spot-checked them: `test_lethality.py:143-162`, `test_nesting.py:78-88, :222-240`, `test_comms.py:272-319`, `env.py:241-243, :359-361`.

**Out of lane, passed on without severity:**

- The iframe heights in scope differ from BRIEF §16's table: Figure 1 is 1100 against 720, Figure 2 442 against 430, Figure 3 427 against 400, Figure 5 528 against 520, Figure 6 736 against 680. This is RM's lane (P2-5).
- The abstract is 372 words against a 360 budget, which W1 disclosed.
- "Completion shows no detectable change" (abstract and §1) is for the claims lane to judge against BRIEF §6.3, "not 'completion is unaffected'".
