# RM: mechanics review of draft1 (whole paper)

Reviewer RM, Paper v2 phase 1, step 4, pass 2. Reviewed state: `paper/v2/snapshots/draft1/` (byte-identical to `paper/v2/sections/` when checked), `paper/v2/front_matter.yaml`, `paper/v2/out/submission_v2.md`, the draft1 real-kit build (`.../scratchpad/kit/kit_run_20261011_233532_5425/`), its printed PDF (`out/submission_v2_print.pdf` = `scratchpad/kit/draft1_print.pdf`, same sha256), `out/kit_checks.md`/`.json`, `out/kit_screens/`, and `out/submission_folder.zip`. Line numbers are snapshot line numbers.

## Summary

**26 findings: 7 MUST, 15 SHOULD, 4 OWNER.**

The most important:

- **RM-1, RM-2, RM-3.** The printed PDF cuts off content in 7 places:
  - the right end of Definition 2's display;
  - the upper bound in Proposition 3's display;
  - parts of five tables. App. C's floor table loses its "floor" and "use" columns entirely, and §9.1's arm table loses ISO's fire-only share of 1/3.
- **RM-4.** The three episode-explorer iframes resize themselves without limit, at about 31 px/s. The kit check's "measured" heights are snapshots of that growth.
- **RM-5.** Two reference-list names are garbled: "Witt, C.S.d." and "Omari, B.A."
- **RM-6.** The hero-ladder alternate builds with exit 0, but the page it produces is incoherent.
- **RM-7.** One cross-reference points at the wrong target.

**How I checked, and what I covered.** Every check below was run in this session.

1. **Reading.** I read every line of the 16 section files and the 5 alternates, with each STUB-SPEC read against its text.
2. **Kit syntax** (`scratchpad/RM/scan.py`). My own scanner models kramdown 2.4.0's table detection, as read from the installed gem's `parser/kramdown/table.rb`: a pipe outside a code span, after a block boundary, starts a table. The scanner also covers:
   - Liquid forms;
   - `$` in raw HTML, code and comments;
   - math commands;
   - `<d-cite>` syntax;
   - headings;
   - prose traps;
   - LISTING headers.

   A second pass checked delimiter parity, link-like syntax and display-block blank lines in the generated kit source.
3. **Listings** (`listings.py`). Each fence body was compared with `git show HEAD:<path>` and with the working tree.
4. **Formal statements.** I compared every Definition, Proposition, Corollary, Theorem and Remark with `docs/theory_foundations.md` (TF), with `citations/C1_verification.md` and with `citations/theory_cites.md`, and I compared the App. A proofs with their statements.
5. **Cross-references** (`xref.py`). My own extractor works on snapshot line numbers and found 329 references. All resolve to an existing label. I read-verified the target content of every one, including all 41 in §1 and all 41 in §9; the abstract has none. 13 references to a cited work's own numbering are out of scope.
6. **Double-blind** (`blind.py`). Scanned for identity tokens, URLs, absolute paths, hosts and hex strings of 7 or more characters, with every hex hit tested against all 131 commit hashes. Inputs:
   - the sections and alternates, comments included;
   - the front matter;
   - all 28 files of the staged zip;
   - the PDF's text (`pdftotext`, 50 pages);
   - the 11 figure HTML sources;
   - the built kit page;
   - PNG text chunks.
7. **The built page.** I served it and inspected it in headless Chromium with my own scripts (`page.mjs`, `grow.mjs`, `content.mjs`, `printov.mjs`, `shot.mjs`):
   - tables, the reference list, the 49 hover cards, the cite box, the byline, the toc and footnote placement;
   - iframe heights over 110 s at 1280 px, and content heights at 1280, 1024 and 390 px;
   - a print-media overflow scan.
8. **The printed PDF.** I viewed all 50 pages as contact sheets at 60 dpi, and 7 pages (10, 11, 13, 18, 28, 40, 46) at 100–110 dpi.
9. **Alternates.** I ran `build_v2.py --alt` for all 5 alternates, then re-ran the default build. The five `out/` build files are byte-identical to my pre-run backup, and nothing else in `out/` changed.

**Iframes whose height attribute is more than 5 % off (item 7).** The table uses the kit check's measured values. My reading of each frame is given beside them.

| iframe | attribute | kit "self-sized" at 1280 | off, as % of measured | RM reading |
|---|---|---|---|---|
| `explorer_thetastar_random_seed0.html` (Fig. 1) | 1100 | 1212 | 9.2 % | grows without bound (1284 px at 5 s, 4596 px at 110 s); content 677 px |
| `explorer_thetastar_joint_s1_T1000_ep0.html` (Fig. I2) | 872 | 952 | 8.4 % | grows without bound; content 677 px |
| `explorer_thetastar_iso_s1_T1000_ep0.html` (Fig. I1) | 868 | 912 | 4.8 % (5.1 % of the attribute) | grows without bound; content 677 px |

The other 8 iframes are stable, with attributes 1.2–2.7 % below their self-sized heights.

## Findings

| ID | severity | file:line | quoted text (short) | problem | evidence (record file:line, ledger ID, log heading:line) | proposed fix | class |
|---|---|---|---|---|---|---|---|
| RM-1 | MUST | 03_environment.md:151 | "R(s,a,s') = R_task(…) − d_p ∣{i : α_i = 1, α′_i = 0}∣ ," | **The printed PDF cuts off Definition 2's display at the column edge.** Page 11 ends at "− d_p ∣{i : α_i = 1, α" and loses "′_i = 0}∣,". On screen the display scrolls inside itself, but print cannot scroll. | PDF p. 11, viewed at 110 dpi. Print-media emulation at 816 px: the display needs 536 px in a 472 px column, so 64 px are clipped. `src/kit_styles.css` sets display math to `overflow-x: auto` and has no `@media print` override. The kit_checks.md row "display math wider than the column" measured screen widths only. | **Writer:** split the display into two `aligned` lines, breaking after the R_task term, as Def. 1's kernel display already does. **B2:** add a print-overflow check to `kit_checks.mjs`: under `emulateMedia('print')`, flag any element whose scrollWidth exceeds its clientWidth. | B (the printed PDF must stand alone: SUBMISSION FORMAT constraint 4, as cited for P2-1) |
| RM-2 | MUST | 05_coupling_a.md:80 | "E[B_T] = λ_A T χ(β)(1 + o(1)), and in general E[B_T] ≤ λ_A T χ(β)" | **The printed PDF cuts off Proposition 3's display.** Page 18 ends at "and in general E[B_T]" and loses "≤ λ_A T χ(β)". That upper bound is the one the C3 and Prop. 3 edits rest on. | PDF p. 18, viewed at 110 dpi. Print emulation: needs 577 px in 472 px, so 105 px are clipped. Same CSS cause as RM-1. | Set "and in general E[B_T] ≤ λ_A T χ(β)" as a second line (`aligned`) or as its own display. Add the print-overflow check from RM-1. | B (SUBMISSION FORMAT constraint 4) |
| RM-3 | MUST | 03_environment.md:194-198; 09_compositional_test.md:40-44; 13_appendix_locks_floors.md:32-43, :63-76; 14_appendix_plan_provenance.md:156-166 | "asserted by"; "fire-only share ν (behavioural)"; App. C "floor", "use"; App. H "completion mean" | **Five tables are clipped in print.** Each is listed with the width lost:<br>• §3.4 (163 px): `che/tests/test_nesting.py` and `che/tests/test_comms.py` print as "che/test".<br>• §9.1 arm table (78 px): the "fire-only share ν" column is cut, including ISO's 1/3, the design-error fact.<br>• App. B analysis-constant table (12 px): part of the "role" column.<br>• App. C floors table (265 px): the whole "floor" and "use" columns are missing (pp. 40–41).<br>• App. H arm table (57 px): the completion means print as "0.78" and "0.77". | PDF pp. 13, 28, 39, 40, 41, 46, viewed. `printov.mjs` print emulation lists exactly these five tables and the two displays of RM-1 and RM-2. Cause: `kit_styles.css` "d-article table { display: block; overflow-x: auto; }", with no print override. | **B2:** add `@media print { d-article table { display: table; overflow: visible; font-size: 10px; } d-article table code { white-space: normal; overflow-wrap: anywhere; } }`, and set wide tables in the page grid column in print. **Writers:** shorten App. C's "use" cells, or move them to prose. **Then:** re-print and grade print overflow as 0. | B (SUBMISSION FORMAT constraint 4) |
| RM-4 | MUST | 00_hero.md:45; 14_appendix_plan_provenance.md:189, :200 | `height="1100"`, `height="868"`, `height="872"` | **The three episode explorers resize their own iframe without bound.**<br>**Mechanism:** `fit()` sets `frameElement.style.height = documentElement.scrollHeight + 4`. The frame's resize event runs `full()` 80 ms later, and `full()` calls `__fit()` again. `documentElement.scrollHeight` is never less than the frame's height, so each cycle adds 4 px, about 31 px/s at 1280 px.<br>**Measured:** the hero frame was 1284 px at 5 s, 2744 at 50 s and 4596 at 110 s, still growing. Fig. I1 and Fig. I2 grow the same way. The real content (`body.scrollHeight`) is 677 px at 1280 px, 717 at 1024 and 1150 at 390. After 30 s, a screenshot shows a 2152 px frame with about 1470 px of blank space under the figure.<br>**Consequence:** the kit check's 1212, 912 and 952 px, and P2's 1,096 px behind P2-5, are snapshots of the growth, not content heights. At 1280 px the attributes are 62 %, 28 % and 29 % taller than the content. The 8 other iframes are stable. | Source: `paper/figures/interactive/out/html/explorer_thetastar_random_seed0.html` (function `fit`; `full()` → `__fit()`; `addEventListener('resize', … setTimeout(full, 80))`). Evidence: my Playwright time series (`grow.mjs`) and screenshot (`hero_30s.png`), this session; kit_checks.md, iframe rows; FINDINGS P2-5. | **With a figure rebuild:** `fit()` measures `document.body`, or the html element with `height: auto`, and skips the write when the height has not changed. **Without one:** add `sandbox="allow-scripts"` to these three iframes, which makes `frameElement` null so `fit` does nothing (theme sync is already wrapped in try/catch), and set each height to about 700 at 1280 px. Narrow widths then clip, the reason `fit` exists, so this is the owner's choice under Q22. **Either way:** re-grade the 5 % check after waiting about 60 s. | C (needs a figure rebuild, and P2 §0 says no rebuilds this phase; Q22) |
| RM-5 | MUST | `paper/v2/assets/bibliography/submission.bib`:175, :123 (verbatim from `paper/related_work_verification.md`:478, :394) | "Christian Schroeder de Witt", "Bassel Al Omari" | **Two names are garbled in the reference list.** Distill splits "First … Last" names at the last space:<br>• reference 11 renders "Witt, C.S.d.";<br>• reference 17 renders "Omari, B.A.";<br>• their hover cards are garbled the same way.<br>The same author also appears as "de Witt, C.S." (ref. 16) and "Schroeder de Witt, C." (ref. 38), while §3.5 says "de Witt et al. (2020)". The M2 check compares fields as strings, so it cannot see the split. | The built page's reference list, refs. 11, 16, 17 and 38, read with Playwright; PDF p. 48; kit_checks.md "rendered authors and titles equal the bib's Unicode fields: PASS". | Write both names as "Last, First" in `related_work_verification.md` ("Schroeder de Witt, Christian"; "Al Omari, Bassel"), with a dated M2-style note, then re-copy the bib (`bib_diff.py`). Add a check that each rendered surname equals the bib entry's surname. | A (M2) |
| RM-6 | MUST | alt/00_hero.ladder.md:9-16, built with `src/build_v2.py --alt 00_hero.ladder` | `<strong>Figure 1.</strong>` (the opening ladder) | **The hero-ladder alternate builds with 0 failures but produces an incoherent page.**<br>• The explorer is gone: 0 occurrences, and 24 assets against 26.<br>• The opening ladder appears twice, as the hero's "Figure 1" and as §1's "Figure 3".<br>• Every reference to the explorer as Figure 1 now points at the ladder: 01:25 "(Figure 1)"; 05:21 "Figure 1's event track … press ] in Figure 1"; 06:20 "Figure 1 opens on agent 7".<br>STRUCTURE.md §9 asked B2 for a build flag that moves the blocks and swaps Figures 1 and 3. `build_v2.py` has no such flag (its arguments are `--root`, `--bib`, `--alt`, `--final`, `--copy-assets` and `--styles`). | My alternate builds, this session (`scratchpad/RM/alt_out/00_hero.ladder/`); STRUCTURE.md §9; build_v2.py:983-998. | **B2:** implement the option-B flag: §1's ladder block goes to the hero slot, the explorer block to the head of §3, Figures 1 and 3 swap throughout, and the alternate's duplicate goes. **Until then:** show the owner this file as a caption draft only, not as a buildable page. | C (Q8; the flag is B2's to accept) |
| RM-7 | MUST | 11_reproducibility.md:24; alt/11_reproducibility.supplement.md:17 | "and each stage's log records a single run (§9.1)" | **The cross-reference points at the wrong section.** §9.1 says only that the runner computes no cross-arm quantity (09:60). The refusal to run out of order, and the one-run logs, are stated in App. F. | 14_appendix_plan_provenance.md:114: "later analysis scripts refuse to run before its log exists, and each log records one run of its stage". | Change "(§9.1)" to "(Appendix F)". | A (M2: every cross-reference points at the right target) |
| RM-8 | OWNER | 00_abstract.md:24; alt/00_abstract.disclosure_line.md:15 | `<d-footnote>We used the LLM assistant Claude as a tool: …</d-footnote>` | **This is the finding behind Q4f.**<br>**Default:**<br>• the footnote marker is on printed page 1, after "episode.";<br>• its text prints in Distill's footnote list after the article, on page 47 of 50 (bottom third);<br>• on screen the marker sits at 0.9 % of the page height and the text at 95.5 %.<br>**What fits on page 1:** the title (6 lines in print), the description, the byline, the contents list, and the abstract's first paragraph up to "We ran 72 seeds per". The abstract continues onto page 2.<br>**The visible-line alternate** puts the line after the abstract's third paragraph, so it would also print on page 2. This is an inference from the default PDF's pagination; the alternate itself was not printed.<br>**The alternate's markup is sound:** one `*…*` paragraph, no `$`, no `"`, no `<d-cite>`. It drops the footnote. | kit_checks.md "Footnote (N1)"; PDF pp. 1, 2 and 47 (`pdftotext`, this session); `kit_screens/top_1280.png`; BRIEF §12 (TMLR FAQ, "footnote on the first page", log:6057-6058). | Options for the owner:<br>(a) keep the `<d-footnote>`, and place the visible line as the abstract's first paragraph or directly after its first sentence, which puts it on page 1 in print;<br>(b) shorten the title (109 characters; 4 lines at 1280 px, 6 in print) and the description, so that more of the abstract lands on page 1;<br>(c) accept the marker on page 1 with the text at the end. | C (Q4f; also Q3) |
| RM-9 | OWNER | 03_environment.md:31-37, :46, :48; 05_coupling_a.md:34; 07_comms.md:35; 12_appendix.md:34 | "𝒮 = 𝒳 × ℋ × 𝒫 × 𝒞 × 𝒦 × {0,…,T}"; "s_t = (x_t, h_t, ρ_t, c_t, k_t, t) … is a Markov chain" | **Definition 1's state and kernel arguments omit two things the as-implemented definitions use.**<br>(a) The weak-terrain mask w, "drawn once per episode" (Def. 5). T_C reads it through λ_t(g) = (λ_0 + λ_load o_t(g)) w(g), and the observation's "weak" channel reads it (03:229).<br>(b) The messages emitted at step t (Def. 7). The observation at t+1 carries their delivered aggregate (03:231), yet O^i_{κ_B}(· ∣ x′, h′, ρ′, c′, k′) has no action argument.<br>As written, (s_t) is Markov only given w. The fix is formal and changes no number or claim. The theory doc has the same gap. | Listing 1 passes `state.weak` to `structure_step` (03:68, i.e. `che/env/env.py:300`); `che/env/structure.py` `structure_step` takes `weak`; TF Def. 1 (:33-64) and TF Def. 5 (:286-296). | Owner: add w to the structural factor (𝒞 = {intact, collapsed}^G × {0,1}^G, with w fixed after reset), and write the observation kernel as O^i(· ∣ s′, a), with messages part of a. Apply this in Def. 1 and App. A, and record it as a theory-doc item. | C (new; a departure from the theory doc beyond C1–C3) |
| RM-10 | OWNER | 05_coupling_a.md:83; 12_appendix.md:46 | "Consequently the marginal hazard exposure … is ∂E[B_T]/∂λ_A = Tχ(β)." | **The derivative is stated as an exact equality, which the proof does not establish.** The statement's own equality is E[B_T] = λ_A T χ(β)(1 + o(1)). App. A proves only the disjoint-cluster value λ_A T χ(β) and says nothing about the derivative. The sentence is carried verbatim from TF, so softening it would be a new departure. | TF Prop. 3 (:306-311); App. A proof (12:46). | "… is Tχ(β) to leading order in the sparse regime", or use "≈". | C |
| RM-11 | OWNER | 12_appendix.md:30, :36, :48, :58 | "the formal specification …" | **App. A refers four times to a document no reader can see.** §11 promises no supplement (Q4e). Line 58 also tells the reader that the authors' own specification "concludes more about ISO's slack than an upper bound can show". These sentences carry the OWNER ITEM 2 and C3 disclosures, so where they belong is the owner's choice. | 11_reproducibility.md:18; FINDINGS C3; OWNER ITEM 2. | Default suggestion: keep the factual notes without the external reference (for example: "ρ is real-valued, so the state space is not finite; the argument uses only the reachable states"), drop line 58's comparison, and keep the theory-doc record items for the owner. | C |
| RM-12 | SHOULD | 12_appendix.md:48 | "a divergence rate taken from Corollary 1(3), which the paper does not state" | **"Corollary 1(3)" is a dangling reference for a reader.** The paper's Corollary 1 has only items 1–2, and in the alternate it has no items at all. | 04_severity.md:35-38; alt/04_severity.no_item4.md:24. | "a divergence rate near β_c, which the paper does not state (§4.1)" | A (C1; M2) |
| RM-13 | SHOULD | 04_severity.md:40; alt/04_severity.no_item4.md:26 | "with ignitions added by Coupling A (§3.2)" | **Wrong target.** Coupling A is defined in §5.1 (Def. 5); §3.2 mentions it only in passing (03:132). | 05_coupling_a.md:34 | "(§5.1)" | A (M2) |
| RM-14 | SHOULD | 14_appendix_plan_provenance.md:190 | "(labelled obs v3: the masking observation, §3.4)" | **Wrong target.** §3.4 is the section on nested models. The masking observation is defined in §6.1 (Def. 6), and its channels are listed in §3.5. | 06_coupling_b.md:24-30; 03_environment.md:229 | "§6.1" | A (M2) |
| RM-15 | SHOULD | 12_appendix.md:23 | "Appendix F: grid provenance and blinding." | **The index entry does not match the heading**, which is "### F Grid provenance" (14:108). | 14_appendix_plan_provenance.md:108 | Make the two match, either with the heading "F Grid provenance and blinding" (ASCII, toc-safe) or by dropping "and blinding" from the index. | A (M2) |
| RM-16 | SHOULD | 03_environment.md:229; 06_coupling_b.md:56 | "row and column over $L$"; "two disjoint corridors $L$ and $R$" | **L is used before it is defined, and then reused.** §3.5 uses L before Def. 4 defines it as the arena side (04:44). Theorem 1 reuses L for a corridor. | 04_severity.md:44; TF :378 (the corridor letters are the theory doc's). | In §3.5, write "over the grid side L = 64" (or "over 64"). Leave Theorem 1's letters, which follow TF. | C (new) |
| RM-17 | SHOULD | 03_environment.md:37 against 09_compositional_test.md:56, :87, :99, :110; 10_limitations.md:44; 14_appendix_plan_provenance.md:110, :118-150 | "with horizon $T$"; "The T = 2000 subsample"; "through t = 850" | **T and t each mean two things.** Def. 1 makes T the episode horizon (256 steps) and t the step index. §9, §10 and App. G use T for the training budget in updates (T = 2000) and t for a Γ(t) update checkpoint. | 03_environment.md:37 | Write "the 2000-update subsample" and "at update 850", or say once in §9.1 that there t counts training updates and T the budget. Quoted registered text (App. D, "T = 1000") stays as it is. | C (new) |
| RM-18 | SHOULD | 09_compositional_test.md:26, :34; 03_environment.md:37 against 08_methodology.md:41 | "the expected episodic return"; "its discounted returns"; "k ∈ 𝒦 is the realized communication graph" against "k seeds" | **Two inherited notation clashes.** Def. 8 defines J as an episodic return, while Prop. 4 speaks of discounted returns. The letter k names both the link graph (Def. 1; k′_ij in Def. 7) and the seed count. Both come from TF. | TF Notation (:20-21) | Prop. 4: "the difference between its returns". For k, add "(k here counts seeds)" in §8.2. | C (new) |
| RM-19 | SHOULD | 09_compositional_test.md:89 | "∣z_c∣ + z_α = 3.855 < 4.433 = ∣z_s∣" | **z_c and z_s are never defined in the body.** Only App. D's quotation defines z = Γ / sd(Γ). | 14_appendix_plan_provenance.md:41-43 | Add "where z_c and z_s are the completion and survival statistics Γ / sd(Γ)". | C (new) |
| RM-20 | SHOULD | 03_environment.md:126, :146 | "**Definition 3 (Fire kernel).**" printed before "**Definition 2 (Ambient hazard).**" | **The definitions print out of order:** 1, 3, 2, 4, … Def. 2 is cited from §1 and from Def. 1 before it appears. The numbering follows TF. | — | Move Def. 2, with §3.3's lead paragraph, before §3.2. Or keep the numbers and say once that they follow the specification. | C (new) |
| RM-21 | SHOULD | 02_related_work.md:23; 09_compositional_test.md:73 | "**Table 1.**"; "(Figure 11 and the contrast table)" | **Only 1 of the 16 tables is numbered**, and §9.2 cites "the contrast table" by description. | Kit table count 16 (my own count in the built page). | Number every table, or at least those the text cites, and refer to them by number. Otherwise drop "Table 1". | C (new) |
| RM-22 | SHOULD | front_matter.yaml:17 against 00_abstract.md:24 | "A pre-registered test of whether training a single policy on co-occurring stressors beats training it on each in isolation, in the Compound Hostile Environment (CHE), …" | **The description repeats the abstract's first sentence almost word for word**, and both restate the title. The first screen and printed page 1 therefore say the same sentence twice. F2 asks for the description to be re-checked against the new abstract. | `kit_screens/top_1280.png`; PDF p. 1 | Make the description say something the abstract's first sentence does not, for example the result in words, with no number. W1's description table; the owner chooses. | C (Q3, F2) |
| RM-23 | SHOULD | front_matter.yaml:25 | "date: 2026-10-11" | **A final build will accept this date unreviewed.** The date is marked PLACEHOLDER only in a YAML comment, and `build_v2.py --final` checks for placeholders only on string fields that begin with "PLACEHOLDER". The kit prints the date as the cite box's BibTeX year, "year = {October 11, 2026}", and authors cannot change that format. | build_v2.py:340-347; kit layout `distill.html`:23, :38 (`page.date \| date: '%B %-d, %Y'`) | B2: make `--final` fail until the date is confirmed, for example with an explicit `date_confirmed: true` field in the front matter. | C (Q2) |
| RM-24 | SHOULD | 02_related_work.md:45; submission.bib:314 | "Tramèr & Boneh (2019)" against the rendered "Tramer, F. and Boneh, D." | **The text and the reference list spell the author differently.** M2 asked for Unicode names at the source. | Rendered reference list, entry 32 | Enter "Tramèr" in `related_work_verification.md`, with a dated M2 note, and re-copy the bib. | A (M2) |
| RM-25 | SHOULD | 03_environment.md:58-122 (Listing 1); `src/kit_styles.css`, the print listing rule | `white-space: pre-wrap` (print) | **Listings wrap badly in print.** They stay in the narrow text column and wrap at about 60 characters, and each continuation line starts at column 0 (for example `occ_pre = occupancy_grid(state.agent_pos,` / `state.agent_alive, cfg.grid_size)`). That misreads Python's indentation, the hazard the CSS comment itself names. | PDF p. 10, viewed at 100 dpi | B2: add `@media print { d-article > div.highlighter-rouge { grid-column: page; } d-article div.highlighter-rouge pre { font-size: 9px; } }`, then count wrapped lines per listing in the PDF. | C (follow-up to KB-2) |
| RM-26 | SHOULD | 01_introduction.md:40 | "within the spread over three seeds (§10)" | **The reference points at a restatement instead of the result's home.** CB-9's home is §6.4; §10 item 1 restates it. | STRUCTURE.md §7 (one home per result); 06_coupling_b.md:80 | "(§6.4)" | A (LEN; N16) |

## Checked and clean

**Kit syntax and M1**

- **Prose pipes.** My scan found 0 unescaped pipes outside a code span on any prose, list or blockquote line, in all 21 files (16 main and 5 alternates). App. D's pipe-bearing strings are inside code spans or escaped as `\|`.
- **Table count.** The source has 16 tables, all after a blank line. The built kit page has 16 (my own count), matching kit_checks.md.
- **Liquid.** Only the two kit forms occur: `include figure.html` and the `relative_url` filter. There is no `{{` or `{%` anywhere else, comments included.
- **MathJax.**
  - There is no `$` in raw HTML, in code fences or in comments, and no odd count of `$` on any line.
  - No paragraph is a lone inline expression.
  - All 13 display blocks have blank lines around their `$$` lines.
  - None of `\newcommand`, `\label`, `\eqref` or `\tag` appears.
  - The page has 412 rendered expressions, 0 MathJax errors, and no raw TeX in the article's rendered text.
- **`<d-cite>`.** All 54 tags use the `key="…"` form. Their 39 distinct keys all exist in the 41-entry bib; the two uncited keys are `jaderberg2017pbt` and `zhao2020simtoreal`.
- **Headings and toc.**
  - The H2 headings are toc-safe, and all 12 toc links resolve on the built page (my own check). The hyphen in "9 The pre-registered compositional test" falls outside BRIEF §14's letter, but its id resolves.
  - No heading carries Γ, β, math, an em dash, quotes or parentheses.
  - The H3-led files are `13_` ("B …") and `14_` ("D …"), each after the line-1 status comment.
  - Appendix letters run A–I without a gap.
- **Prose traps.** None found: no `--`, `...`, `<<` or `>>` in prose, no stray `<` before a letter, no `{:`, and no line-start traps. The only stray underscore is `Γ_H` inside App. D's verbatim quotation (14:61, :82), where kramdown treats it as intra-word, so it renders literally.
- **Figures.** Each of the 11 iframe figures has its print companion. The static Figures 4, 7, 8 and 9 use a short include caption followed by `<p class="caption">`. All companions print in the PDF, and no figure is broken.

**Listings**

- **Byte identity.** All 6 are byte-identical to `HEAD` and to the working tree; the source files are unmodified:
  - `env.py:298-358`, 61 lines;
  - `tasks.py:31-43`, 13 lines;
  - `test_coupling_b.py:131-142`, 12 lines;
  - `structure.py:83-102`, 20 lines;
  - `observation.py:300-310`, 11 lines;
  - `ippo.py:323-329`, 7 lines.

  Each fence's header line equals its LISTING line. Every listing line is present in the PDF's text.
- **Labels.** Listings 1–6 are numbered in order, and each label matches what its text says the listing shows. For example, `tl` is `state.theta_live` (env.py:297), and the early `frozen` branch is visible in Listing 1.
- **Code line references in prose.** All were checked against HEAD and point at the claimed code:
  - `env.py:241-243`, :159-173, :361 and :394-396;
  - `hazard.py:8-16` and :67-79;
  - `harness.py:44-45`;
  - `test_reward_independence.py:6-15`;
  - `test_lethality.py:143-162`;
  - `test_coupling_b.py:143-156`;
  - `test_nesting.py:78-88` and :222-240.

**Formal statements against TF**

- **C1.** Corollary 1's item 2 is stated at the level C1_verification §2 verified (Garet & Marchand, Cor. 5.4):
  - "on that event" = the origin's cluster is infinite;
  - almost-sure convergence in Hausdorff distance;
  - a convex compact limit set with non-empty interior, invariant under permutations and reflections of the coordinates;
  - a speed that depends on direction.

  The old item (3), its exponents and "∼" are gone everywhere ("43/18" and "4/3": 0 hits). The "universal" caveat is cut. Item (2) is cut per N7, with χ and ξ defined where they are used and no claim of finiteness. The alternate drops item 2 and its citation, and builds with 38 keys.
- **C2.** Remark 1 matches the support record in `theory_cites.md` for `bernstein2002`: NEXP-hard, NEXP-complete when the horizon is below the number of states, and a worst-case result for the class, licensing only "no general exact planner is expected to scale".
- **C3.** Proposition 4 is renamed "A transfer bound for a fixed policy" and stated as an upper bound, in words, with no display. "Irreducible" has 0 hits. The honesty note is kept (09:36, 10:39), and App. A gives a proof idea with no constant.
- **OWNER ITEM 2.** Proposition 1's statement matches TF. The finiteness claim is restricted to reachable states (03:50; 12:34-36), and the proof's premises hold: ρ_0 = 0 at reset (`env.py:257`), and every stochastic factor has finite support.
- **Prop. 3.** The rate is gone from the statement, the title and the proof; 12:48 notes the omission.
- **Everything else matches TF**, apart from RM-9 and RM-10:
  - Def. 2, in its 2026-09-27 wording;
  - Def. 3, and Prop. 2 with its coupling proof;
  - Def. 4;
  - Defs. 5, 6 and 7 ("as implemented"), which match `structure.py`, `observation.py:86-126` and the hard-range note;
  - Def. 8;
  - Theorem 1 and its proof;
  - Remark 2′ (i) and (ii), and App. A's paragraph on the size of the correction (1.126, 1.235, 79/54/7 %, as TF:529-537).

**Cross-references**

- **Resolution.** All 329 resolve, and I read-verified every target. Apart from RM-7 and RM-12–RM-15, each points at the right content. The parser quirk (W6) produced no wrong target in this snapshot.
- **Figure numbering.** Figures 1–13, I1 and I2 are numbered in order, as in BRIEF §16.
- **Re-lettering.** "Appendix J", "Figure J1" and "J2" appear nowhere, and the old letters G, H and I are used correctly.
- **Figure HTML.** The figures print no appendix or figure letter. The only section reference is opening_ladder's "§9.2", which is correct.

**M2–M4 on the built page**

- **M2.**
  - The reference list has 39 entries, one per cited key, with no raw LaTeX and no `--`.
  - All 49 hover cards render, with no raw TeX.
  - Every `<d-cite>` resolves.
  - RM-5 and RM-24 are the exceptions.
- **M3.**
  - The cite box has a year, in the kit's format.
  - The byline reads "Submitted: Not submitted yet."
  - The title is intact in the h1 and in the cite box.
- **M4.**
  - The staged `submission.md` has 0 `<!--`, and equals the comment-stripped `out/submission_v2.md` after whitespace normalization.
  - The staged bib has 0 `%` lines and is identical to the v2 bib without its 4 `%` lines.
  - All 26 staged assets are byte-identical to their sources.
  - The rendered article contains 0 comment nodes.

**Double-blind**

- **Coverage.** All scanned sources are clean: the sections and alternates (comments included), the front matter, the staged zip, the PDF text, the 11 figure HTML files and the built page.
- **Identity.** No identity token appears: account or repository name, e-mail, or session string.
- **URLs.** None appears beyond the kit's own CDN and utterances links, the bib's links to cited works, and the SVG namespace string.
- **Paths, hosts and hashes.**
  - No absolute path appears.
  - No host or IP address appears.
  - No hex string of 7 or more characters matches any of the 131 commit hashes.
  - The PNGs carry no text chunks.
- **Footnote.** The disclosure footnote names the tool ("the LLM assistant Claude"), not the author.

**Alternates (item 9)**

- **Builds.** All 5 exit 0, with 0 failures, 0 warnings, 0 M1 flags and 0 unresolved cross-references. The single final-only item is the STUB-SPEC blocks.
- **Content.**
  - `disclosure_line` and `no_recommendation` differ from the default only as intended.
  - `no_item4` is sound apart from RM-13.
  - `supplement` names only in-repository paths and carries RM-7.
  - `hero.ladder` is RM-6.

**Front matter (item 11)**

- **Title and description.** The title is 109 characters and the description 229. Each:
  - is one line;
  - contains no `"`, backslash, `<`, `>`, `&` or ": ";
  - is single-quoted, and parses back unchanged from the generated header.

  The description holds no number.
- **Dates.** `date` is a YAML date no later than the build day. `submitted_date` is absent.
- **Authors and fields.** The authors are Anonymous, with no url. `openreview_id`, `toc` and `_styles` are not set by hand.

**Other**

- **Kit page error.** The page error "Invalid repo" comes from the kit template's own utterances widget (`repo=""`), not from our source.
- **Leftovers.** My preview server is stopped. `out/` is byte-identical to its state before my builds.
