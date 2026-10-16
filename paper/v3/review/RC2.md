# RC2: claims (part 2) and whole-paper consistency

Reviewer lane RC2, step 4.2 of `paper_v3_prompt.md`, 2026-10-14. Snapshot reviewed:
`paper/v3/snapshots/draft1/` (sections and provenance). All `file:line` cites below
are snapshot section files unless a path is given.

## Summary

**Counts:** MUST 4, SHOULD 13, OWNER 2 (19 findings).

**MUST items, one line each:**

- **RC2-1**: §6.1 says "so little beyond Coupling A was under test" and that the registration "stated this in advance". That repeats the professor's "mostly Coupling A" as fact, goes beyond CB-9, misstates the registered §4a text, and pre-judges the interaction check.
- **RC2-2**: App. J says "the authors made the study's decisions" and "each decision was written into the … record before it was acted on". The record contradicts both: pre-rental design decisions, including the ratification of the outcome framings, were delegated to the builder; some rulings were builder-ruled; transcription was required only from 2026-07-28; and no owner approval of the interaction-check plan is transcribed.
- **RC2-3**: The App. D.2 row for 2026-08-14 cites "dated log" as its record. DX-36 says that log entry is still owed; the date comes from the floor study's README.
- **RC2-4**: App. D.1 says a reader "can check that the documents quoted here are the documents shipped". Most of D.3's quotations come from the dated log, which the supplement does not ship (D.1 says so itself). §8 also credits the self-made hash manifest with more than it shows.

**Scope and method.** I read in full:

- `paper_v3_prompt.md`;
- `docs/decision_log.md` from PAPER V2 to the end;
- `paper/v3/BRIEF.md`, `STRUCTURE.md` and the orchestrator notes;
- `che/bench/results/phase6/post_v3_interaction/PLAN.md`;
- every snapshot section 00–21, with the STUB-SPEC of each scope file;
- `paper/v3/front_matter.yaml`;
- `paper/v3/supplement/SHIPPED_README.md`.

I checked these claims against the record:

- the D.3 quotations, word for word, against:
  - log:2977-2993 (T\* ruling);
  - log:3970-4152 (§7 PROPOSALS: inert-share rule, 2000-update subsample, High readout);
  - log:4913-4950 (pre-unblind rulings);
  - log:5057-5062 (S1–S6);
  - `phase6_framing_branches.md:3-16, :50-104, :155-166, :230-256`;
  - `phase6_design_v2.md:340-366, :428-433`;
  - `docs/venue_review_2026-08-16.md:158-163`;
- the ledger rows behind each claim, where the claim depends on a row's scope (RES-12, DES-3, DES-10, DES-15, DX-30, DX-36, DX-413, HW-2/3/4, X4-1 to X4-5, CB-9, COM-6);
- the log entries on delegation (log:3104-3125, :3450, :5961, :2940) and the rule's start date (log:465);
- `che/tests/test_p6_grid.py:210-219` (the D.9 claim);
- `phase6/by_card/README.md:28-56`;
- `git rev-parse --is-shallow-repository` (true, the D.1 claim).

Tools run:

- `v3_checks.py caveats` on the snapshot: **PASS**, 39 of 39.
- `provenance_check.py --strict` on the snapshot root: every scope file has one row per sentence and no stale rows. Its "support problems" exist only because the snapshot root carries no `ledger_proposals/`, so they are not findings.
  - The checker wrote `snapshots/draft1/out/provenance_check.md`, which my run created. I moved that file to my scratch directory and removed the empty directory, so the snapshot is as I found it.

All of the following hold:

- the registered strings (BRIEF §6): verbatim at their homes;
- branch_B.md §5 and §8: no violation found;
- V3-F4: the identity is in §6.2; the plane leads §6.3 and is labelled non-verdict-bearing; it is never said to separate co-occurrence from frequency (06:62, 07:41-43, 18:30); Γ stays the test; future work is named; no advice; nothing follows a "therefore";
- V3-F5: in §6.1 (06:54) and App. D.10 (16:184);
- V3-F6: in §1 (01:52);
- the post hoc label: on every mention of the check outside §6.4 and App. G (01:52, 06:56, 06:67, 10:30);
- the F3 timeline (BRIEF §7, rows 1–11): every row is present in App. D (16:45-66, :157) with matching dates and sources;
- the HOLE surroundings: they read correctly whatever the result, except RC2-1.

## Findings

### RC2-1 (MUST): §6.1 states the siting limitation beyond the record, in the professor's words, and misdescribes what was registered

- **Location:** 06_example_design.md:56; its tension with 04_calibration.md:98.
- **What is wrong.**
  - (a) "so little beyond Coupling A was under test" turns one calibration measurement into a conclusion about what the test contained.
    - That measurement is CB-9: one co-primary (survival); three seeds; 500-update calibration policies; graded against a three-seed spread, not a floor.
    - It is the substance of the professor's "mostly Coupling A". BRIEF:133 says that phrase is the review's and must "never" be cited as fact (log:6121-6122, "The review is not a ruling").
  - (b) "The registration stated this in advance" is not accurate.
    - PFB §4a registered: B's own measured survival effect at Medium was −0.0003; its 8.8-point effect is at High; choosing Medium because both couplings clear their lock criteria "is not the same as both producing behavioural effects there".
    - It registered nothing about communication denial, and nothing about "little beyond Coupling A".
  - (c) The sentence pre-judges the interaction check. PLAN §4 reports the main effect J(B only) − J(neither) precisely to show "whether each coupling, on its own, moves trained policies at θ\*". If it does, §6.1 is contradicted by §6.4/App. G.
  - (d) It sits uneasily with §4.4's "The composition the worked example tests is therefore, in effect, Coupling A with Coupling B" (04:98), which is honesty line 4.
- **Evidence:**
  - `paper/numbers_ledger.md:80` (CB-9: "3 seeds per arm, graded against a 3-seed σ_seed … not a measured floor");
  - `phase6_framing_branches.md:248-256`;
  - BRIEF.md:133;
  - PLAN.md:88-93;
  - provenance/06_example_design.md:19 (the writer's note calls the phrase "W4's wording of PFB:248-252").
- **Fix.** Replace 06:56 with:

  > The test was sited where composition is weak. At the test severity, Coupling B's own survival effect in calibration was within a three-seed spread, not a measured floor (§4.3), and communication denial had no detectable effect (§4.4), so the test configuration may have offered little composition to find. The registration stated the Coupling-B half in advance, as a limitation of every outcome: Medium was chosen because both couplings meet their fixed-value criteria there, "which is not the same as both producing behavioural effects there". A post hoc interaction check measures what the configuration offered (§6.4).

  The quotation keeps PFB's words. Check the caveat pattern `sited where` and C34's three-seed pattern after the edit.

### RC2-2 (MUST): Appendix J claims a division of labour that the record contradicts

- **Location:** 21_appendix_making.md:31 (sentences 2 and 3).
- **What is wrong.**
  - (a) "The authors made the study's decisions: … the registered design and its amendments, the plan of the post hoc interaction check …" The record shows:
    - the owner **delegated** the pre-rental design decisions to the builder ("the decisions are yours this time", log:3104-3112, PRE-RENTAL DELEGATION AND RATIFICATIONS, 2026-08-13);
    - the registered outcome framings were ratified in that entry (`phase6_framing_branches.md:3-4`);
    - GRID CHUNKING was "builder-ruled" (log:3450);
    - OPENING AND §1 REOPENED was "owner delegated, builder's call" (log:5961);
    - several entries are issued by the "registrar" or the "RA", e.g. the T\* RULING that fixed the estimand (log:2940);
    - the interaction-check plan was written by the builder (PLAN.md:3), and no owner approval of it is transcribed (the log ends at log:6244).
  - (b) "Each decision was written into the project's dated decision record before it was acted on." The transcription meta-rule dates from 2026-07-28 (log:465). CLAUDE.md records its origin: a rule "was cited for months as binding and existed only in a chat transcript". Provenance row 11 cites only that rule, which does not show the rule was kept before it existed.
  - Under TMLR's "human-sourced" expectation (log:6057-6058) this is the paper's most consequential factual claim about itself. App. J is the owner's to edit, but the builder draft must not overstate.
- **Evidence:**
  - log:3104-3112, :3450, :5961, :2940, :465;
  - `phase6_framing_branches.md:3-4`;
  - PLAN.md:3;
  - provenance/21_appendix_making.md:24-25.
- **Fix.** Proposed builder draft, for the owner to edit:

  > The authors made or ratified the study's decisions. Some, including the ratification of the registered outcome framings, were delegated to the assistant by the authors and are recorded as delegated in the project's dated decision record. From early in the project, a decision bound only once it was written into that record.

  Before App. J states that the authors approved the interaction-check plan, transcribe the owner's OK of PLAN.md. Otherwise drop "the plan of the post hoc interaction check" from the list.
- **Also for the owner:** App. J names one tool, "used through Claude Code". The log records chat-relayed rulings and reviews ("registrar", "relayed", log:2490, :2717). App. I says "LLM-based research assistants" (21:23), plural and unnamed. Confirm that one tool and one interface cover all of it, or widen the sentence.

### RC2-3 (MUST): App. D.2 names a record that does not date the 2026-08-14 event

- **Location:** 16_appendix_timeline.md:54.
- **What is wrong.** The row "2026-08-14 | a partial re-measurement of floors on another rented GPU (provenance only) | dated log" cites the dated log. The table's own rule (16:41) is "Each row names the record that dates it". The decision log has no entry for this event; it mentions the "card-2 partial re-floor" only as a cost line (log:3958). DX-36 says "its decision-log entry is still owed by the owner".
- **Evidence:** `paper/v2/ledger_supplement.md` DX-36 (source `P6/g1_floors_card2/README.md:1-25`); log:3958.
- **Fix.** Record column: "floor study's README (results directory)".

### RC2-4 (MUST): the registration statement says more can be checked than can be

- **Location:** 16_appendix_timeline.md:38 (D.1); 11_using_che.md:46 (§8).
- **What is wrong.**
  - (a) D.1: "so a reader can check that the documents quoted here are the documents shipped". This is true only of quotations from the two registration documents.
    - D.3 also quotes, from the **dated log** alone:
      - the estimand (log:2977-2983);
      - the inert-share rule (log:3998-4012);
      - the High readout (log:4133-4152);
      - the 2000-update rule (log:4088-4091);
      - the pre-unblind rulings (log:4923-4930);
      - S1–S6 (log:5057-5062).
    - D.1 itself says the log "is not part of the supplement by default". The supplement rules exclude it (`paper/v3/supplement/rules.py:167`), and SHIPPED_README's contents list has no log.
  - (b) §8: "the supplement's hash manifest shows that the registration documents are the files this paper describes". The manifest is computed by the authors when they package the archive. It shows the archive arrived unaltered. Agreement between the shipped documents and the paper's quotations is checked by reading them, not by the hashes. V3-V2 asks for a statement "honest about its limits".
- **Evidence:**
  - `paper/v3/supplement/SHIPPED_README.md` (Contents table; `SHA256SUMS`);
  - `paper/v3/supplement/rules.py:167`;
  - the log lines above;
  - PR:283-285.
- **Fix.**
  - D.1, replacing the sentence from "so a reader can check" onwards:

    > so a reader can compare the quoted registration text with the shipped documents, check with the manifest that the archive arrived unaltered, and rerun the analysis scripts on the committed results. Quotations from the dated log (the estimand, the inert-share rule, the High readout, the 2000-update subsample, the rulings before unblinding and the secondary specification) cannot be checked against the supplement unless log excerpts ship with it.

    The last clause follows the owner's V3-V1 decision on excerpts.
  - §8, second clause:

    > the supplement carries the registration documents, and its hash manifest shows only that the archive arrived unaltered, not when the documents were written

### RC2-5 (SHOULD): §6.4's blind-spot list drops two qualifications PLAN §8 gives

- **Location:** 08_interaction_check.md:50.
- **What is wrong.**
  - PLAN §8 item 3: "Ceiling and floor effects of a bounded rate can create or hide an additive interaction." §6.4 says only "tests additivity only on the scale of rates". Survival is near its ceiling (arm means 0.916–0.926, Table 3, 07:68-70), so this is the qualification that matters most.
  - PLAN §8 item 8 ends with "The pooled reading averages over these differences; it does not remove them". That bears on the headline pooled reading and is missing.
- **Evidence:** PLAN.md:171-174, :198-199.
- **Fix.**
  - Change "tests additivity only on the scale of rates" to:

    > tests additivity only on the scale of rates, where a rate's ceiling or floor can create or hide an interaction

  - End the paragraph with:

    > The pooled estimate averages over these differences; it does not remove them.

  - Optional, from PLAN item 5: after "holds δ at 1", add "so it measures no interaction involving communication denial".

### RC2-6 (SHOULD): App. G misnames the reference of the cross-GPU comparison

- **Location:** 19_appendix_interaction.md:28 (last sentence) and :30 ("the comparison with the main runs").
- **What is wrong.** "compared with the main runs' own evaluation of the same checkpoint" does not fit ISO-4. The glossary's "main training runs" are the grid (BRIEF:165). ISO-4 was trained separately, on another GPU (16:157; DES-15), and PLAN §6 compares with `g1_iso4_5090/eval_iso4_s*.json` as well. PLAN also calls this check "descriptive", and App. G drops that word.
- **Evidence:** PLAN.md:136-141; BRIEF.md:165.
- **Fix.** Use:

  > The "both" evaluation of every policy is also compared, descriptively, with the original evaluation of the same checkpoint at θ\*, and the report states how many agree on both co-primaries.

  At :30, use "the comparison with the original evaluations".

### RC2-7 (SHOULD): §6.5's second future-work design does not "come closer" to what the paragraph is about

- **Location:** 09_example_lesson.md:36.
- **What is wrong.** "Two designs would come closer", that is, to isolating co-occurrence. Varying coupling strength at fixed frequency, co-occurrence and active share does not isolate co-occurrence. It asks whether composition appears where both couplings are behaviourally active, which is the siting limitation of §6.1. The professor offered it as a way out of the thin recommendation (log:6134-6137), not as an isolation design. As written, the paragraph claims more for it than it can give.
- **Fix.** Use:

  > Two experiments would go further. ISO-4 trained for 2000 updates would meet each coupling as often as JOINT does in the registered budget, at the cost of matched compute, leaving co-occurrence as the main remaining difference. Varying the couplings' strength, with frequency, co-occurrence and active share fixed, would test whether composition shows where both couplings are strong, which the test configuration did not offer (§6.1).

  Check the C01 pattern ("sited where") is not triggered; this text contains no such phrase. The 2000 tag (DES-13, DES-14) is the numbers lane's to check.

### RC2-8 (SHOULD): §9 does not state the lesson that the abstract, §1 and §6.5 share

- **Location:** 12_conclusion.md:19-22.
- **What is wrong.** The abstract (00:46), §1 (01:58) and §6.5 (09:31) all state the lesson: matching the active share alone cannot isolate co-occurrence. §9 says only that the example "is read in §6.3 exactly as registered", then gives future work. A reader of the conclusion meets no lesson. The caveat map lists C27's short forms for the abstract and §1 only, so §9 cannot restate it without a map change.
- **Fix (either):**
  - (a) Add a pointer clause:

    > Its worked example … is read in §6.3 exactly as registered, and §6.5 draws its lesson for how such tests are designed.

  - (b) Allow C27's short form in `12_conclusion.md` in `checks/caveats.yaml` (B1/B2) and write:

    > …; matching the share of training with an active stressor cannot by itself isolate co-occurrence (§6.5).

  Fill the HOLE clause to agree with the abstract's final lesson.

### RC2-9 (SHOULD): "exclusion bound" is defined one way and used another

- **Location:** 05_measurement.md:36 (definition); 07_example_results.md:56, :58; 00_abstract.md:41; 01_introduction.md:47.
- **What is wrong.**
  - §5 defines the exclusion bound as an interval's "larger absolute end". For completion Γ, [−4.12, +0.66], that is 4.12. The registered sentence instead excludes "a joint-training gain larger than 0.66 points", the upper end, read in one direction.
  - §6.3 then calls completion Γ₄ "a second exclusion bound" and states no number. Under §5's definition that number would be 4.81, from [−4.81, +2.28].
  - A careful reader sees two rules for one term. App. G (19:30) uses the larger-absolute-end form, which is correct for the check.
- **Fix.** Extend §5's sentence:

  > When a confidence interval contains zero, its larger absolute end is an exclusion bound: the data exclude a larger effect, of either sign, at the interval's level. A one-sided statement uses the end on that side: the registered completion result "excludes a joint-training gain larger than" the interval's upper end.

  In §6.3, optionally give Γ₄'s completion gain bound, +2.28, beside "second exclusion bound". It is already in Table 3.

### RC2-10 (SHOULD): Table 2 points the communication row at a listing that does not show it

- **Location:** 03_environment.md:228 (row "communication denial reads no hazard | 6 (Appendix B)"); 14_appendix_locks.md:71-83.
- **What is wrong.** Listing 6 shows `stop_gradient` on delivered messages, a frozen encoder. It does not show that T_K reads no hazard. §3.2 states that property in prose (03:146).
- **Fix.** Either put "—" in the listing column, or reword the row to "communication denial reads no hazard; the message encoder is frozen", which Listing 6 then carries in part.

### RC2-11 (SHOULD): two pointers send the reader to App. D for a retirement App. D never records

- **Location:** 14_appendix_locks.md:47 ("thresholds of a convergence check retired before the main training runs (Appendix D)"); 15_appendix_floors.md:45 ("It was retired before the grid … (Appendix D)").
- **What is wrong.** App. D's 2026-08-11 row (16:51) records only that "the estimand is fixed at a matched budget". It does not record that the plateau or convergence check was retired. The T\* ruling did both (log:2940-2955; METH-6: "plateau criterion retired; fixed-budget estimand").
- **Fix.** D.2, 2026-08-11 row:

  > the convergence check is retired, and the estimand is fixed at a matched budget of 1000 updates, with the rule for Γ(t)

  Keep tag METH-6.

### RC2-12 (OWNER): D.1 reports the drafting session's checkout as a fact about the paper

- **Location:** 16_appendix_timeline.md:38 ("The copy of the repository this appendix was prepared from is a shallow clone whose history begins after the registration …").
- **What is wrong.** The sentence is true today (`git rev-parse --is-shallow-repository` = true; first commit 2026-09-22). But it describes the builder's environment, not the study. Once the owner runs the full-history check (V3Q16), it will be wrong or beside the point.
- **Fix.** After V3Q16:
  - if the check is done: "The authors checked that the registration documents' commits predate the main training runs; the history itself is not public";
  - otherwise: "The repository's history is not part of the supplement."

### RC2-13 (SHOULD): App. F uses the numbered GPUs that the glossary keeps in App. D

- **Location:** 18_appendix_secondary.md:2 ("trained on GPU 1"), :14 ("ISO-4 (GPU 2)"), :32 ("both trained on GPU 1").
- **What is wrong.** BRIEF:191 says the numbered GPUs "appear only in App. D", and D's STUB-SPEC says the same (16:16). The terms check scans only the main text, so it does not catch this.
- **Fix.** At :2 and :32, say "on the GPU that ran Γ". At :14, say "ISO-4 (second GPU)". The GPU map stays in D.6.

### RC2-14 (SHOULD): the survival window is described two ways

- **Location:** 00_abstract.md:41 ("visible only in the last fifth"); 01_introduction.md:47 ("detectable only at updates 900 to 1000 of 1000"); 07_example_results.md:60, :62 (both forms).
- **What is wrong.** Both forms are supported: RES-12 derives "last fifth" from t ≥ 900 > 800. But the same quantity gets two wordings in the abstract and §1, and "visible" against "detectable" differ. The precise form also places the gain in the last tenth, which the "fifth" wording hides. BRIEF:104 names "only at updates 900–1000" as the precise form.
- **Fix.** Use one wording in the abstract and §1, e.g. "detectable only at the last three checkpoints, updates 900–1000". If the owner prefers the professor's "last fifth", keep it in §6.3 with the precise checkpoints beside it.

### RC2-15 (SHOULD): the siting caveat is stated in near-full form three times

- **Location:** 01_introduction.md:52 (sentence 1); 06_example_design.md:56; 04_calibration.md:86 (last sentence).
- **What is wrong.** The one-home check passes, because each file carries an allowed form. But §1's "short form" holds both reasons with their evidence and is nearly word for word §6.1. §4.3 adds a third statement: "Coupling B's measured survival cost is therefore at High, while the worked example tests at Medium (§6.1)". This is the semantic repeat V3-S5 targets.
- **Fix.**
  - §1, keeping it up front (V3-F6):

    > The test was sited where composition is weak: at its severity Coupling B had no measurable survival effect in calibration and communication denial no detectable effect (§6.1).

  - In §4.3, cut the last sentence, or reduce it to "This is the test severity (§6.1)."

### RC2-16 (SHOULD): "unblinding" is defined twice

- **Location:** 01_introduction.md:47 ("before unblinding, the first computation of any outcome contrast (§6.2)"); 06_example_design.md:60 (same definition again).
- **What is wrong.** The glossary defines the term once, in `06_` (BRIEF:166).
- **Fix.** Keep the definition at §1, its first use. At 06:60, write "a recorded deviation made before unblinding (Appendix D)".

### RC2-17 (SHOULD): D.3's "as registered" branch table edits registered cells without marking them

- **Location:** 16_appendix_timeline.md:89-95.
- **What is wrong.**
  - Row A's claim cell adds "(Γ(θ\*) > 0)" to "founding registration, verbatim".
  - Row D reads "− on either co-primary | − on either co-primary". The registered row is "− (either) | (blank)" (PFB:104).
  - D.3 says omissions are marked [ ] and quotations are verbatim. The column header says "as registered".
- **Fix.** Put additions in square brackets ("founding registration, verbatim [Γ(θ\*) > 0]"). Render row D as registered ("− (either)" in the completion column, the survival cell empty), with a note under the table: "− (either): rejection with negative sign on either co-primary."

### RC2-18 (OWNER): the abstract carries no limitation

- **Location:** 00_abstract.md:39-46.
- **What is wrong.** V3-F6 asks for the limitations in front, with the siting stated "as central, not as a caveat" (PR:217-219). The professor's first point is the siting (log:6123-6127). The abstract reports the test and its result but never says the test point offered weak composition. The caveat map allows a C01 short form here (00:16). The lesson sentence will change after the check returns (V3Q7), so the owner may prefer to carry the siting there.
- **Fix (owner's choice; the budget is 250 words).** Add a clause to the question sentence:

  > …at a held-out near-critical severity where, in calibration, Coupling B had no measurable survival effect.

  Or carry it in the post-check lesson sentence.

### RC2-19 (SHOULD): "registry" is undefined in §8

- **Location:** 11_using_che.md:35 ("a test checks every fixed value against its registry").
- **What is wrong.** A reader new to the project does not know what "its registry" is. The registry is `docs/locks.yaml`, which ships in the supplement (V3-S7; BRIEF §9.4, "pointing at records the reader cannot see").
- **Fix.** Use:

  > and a test checks every fixed value in the configurations and code defaults against one machine-readable list of them, shipped in the supplement (Appendix B)

## Checked and found consistent (no finding)

- **Lesson.** The abstract (00:46), §1 (01:58) and §6.5 (09:31) give the same lesson in the same words. §9 is RC2-8.
- **Numbering.**
  - Main-text figures 1–9, in reading order; Figure 9 is a HOLE.
  - Tables 1–3; Listings 1–4 in §3, 5 in App. A, 6 in App. B.
  - Appendix figures C1, E1, E2, H1, H2.
  - The App. A–J index (13:37-46) matches the headings.
- **Every cross-section pointer in files 00–21 resolves to the place it names,** except RC2-10, RC2-11 and RC2-6's "main runs".
- **The quantities hold across files:**
  - Γ, Γ₄, Γ₄′ and B̂ values;
  - "a third", 2/3 and 1;
  - 72/72/20 seeds;
  - the identity;
  - "three times" (§6.2 only) and "twice" (§6.3 only);
  - the inert phrase (abstract, §1, §4.4);
  - the δ train/test mismatch (§1, §6.2; §6.4's version is PLAN §8 item 8);
  - the counter's radius (§3.5 "Chebyshev radius 4" = App. F's "inside an alive agent's crop", 9 × 9).
- **App. D.3 quotations** are verbatim against the record for:
  - the estimand;
  - budget robustness and its mechanism;
  - the test's variance;
  - the falsifier;
  - the inert-share rule;
  - the High readout;
  - the 2000-update rule;
  - the mediation void rule;
  - rulings (i)–(viii);
  - S1–S6, where "[…]" correctly drops "All as built at" and the commit.
- **The attestation wording** (16:66) matches log:3908-3909. D.9's unit-test claim matches `test_p6_grid.py:210-219`. D.6 matches `by_card/README.md:28-34` and DX-30.
- **App. G against PLAN §2–§7:**
  - conditions, policies, CRN, estimand, per-arm and pooled estimators: match;
  - family 8 with z ≈ 2.73, normal intervals, observed-SE MDE80: match;
  - self-floor design and the hurdle with its post hoc 2σ label: match;
  - the refusal rule and the reading rules (detectable vs. "|I| < B" with MDE80 beside it, pooled headline): match.
  - §6.4 lists all eight PLAN §8 blind spots; the gaps are RC2-5.
- **App. E's High-readout sentence** keeps the registered words with X substituted, and labels 3.40/2.54 as detection limits (BRIEF trap 5). "Not a held-out test" is stated. The T = 2000 subsample is cited only for drift.
- **§8's supplement description** matches `SHIPPED_README.md`: contents, CPU commands, checkpoints not shipped, hashes in `SHA256_CKPT.txt`.

## Re-check (fix2)

Re-checked on 2026-10-16 against `paper/v3/snapshots/fix2/`, using the draft1→fix2 diff and `resolutions_W1.md` to `resolutions_W5.md`. I read only the changed lines.

Checks run:

- `v3_checks.py caveats` on fix2: **PASS**, 39 of 39.
- I re-ran the commit dates of row X4-6. The checkout is no longer shallow. `git log --follow` on the two registration documents agrees with D.1:
  - design: first committed 2026-08-02, last changed 2026-08-13;
  - framings: committed 2026-08-13 only.
- I checked the step listing now cited by Table 2's comms row against `che/env/env.py:353-358`. Its comms call reads positions and aliveness only, as the row says.

### Verdicts

| finding | verdict | note |
|---|---|---|
| RC2-1 (MUST) | OK | 06:56 no longer says "little beyond Coupling A". The registration is credited with the Coupling-B half only, quoting PFB verbatim. "A post hoc interaction check measures this" no longer pre-judges the check. §4.4's honesty line 4 stays, and the tension has gone, since §6.1 now says "may have offered little composition". Two small wording problems remain in the new sentence: see RC2-22. |
| RC2-2 (MUST) | **REOPEN** | Partly fixed. 21:31 now says "the authors delegated the design decisions taken before the main training runs". The record contradicts that. The registered design itself (2026-08-02) came from owner rulings marked "human" (PHASE-6 REMEDY RULINGS, log:1565; FINAL FIVE, log:1655). The delegation of 2026-08-13 covered the remaining *pre-rental* decisions: the grid layout, the seed integers and order, the branch rules and the ratification of the framings (log:3104-3112, :3129-3135). Replacement below. The "made or ratified", rule-start and PLAN_OK parts are fixed correctly. The tool-naming note is correctly left to the owner, with the A1 marker in place. |
| RC2-3 (MUST) | OK | 16:54's record now reads "the floor study's own record (results directory)". |
| RC2-4 (MUST) | OK | D.1 now names the quotations that come from the log and says they cannot be checked unless excerpts ship, and that the manifest shows only that the archive arrived unaltered. §8 (11:46) says the same, "shows only that the archive arrived unaltered". |
| RC2-5 | OK | The ceiling clause and the pooling clause are both in 08:45. The optional item-5 clause was left out for budget; acceptable. |
| RC2-6 | OK | 19:28 and :30 now say "original evaluation", "descriptively". |
| RC2-7 | OK | Fixed. The writer left out my last clause because it would pre-judge the post hoc check, and that reason holds. |
| RC2-8 | OK | 12:19 points to §6.5's lesson (option a). |
| RC2-9 | OK | §5 now defines a directional exclusion bound and the bound on the effect's size. §6.3 names X₄ as the registration's use of "exclusion bound". The definitions now differ openly; see new RC2-20. |
| RC2-10 | OK | Table 2's comms row now cites Listing 3, the step listing (Appendix A), whose comms call reads no h′, ρ′ or c′. |
| RC2-11 | OK | App. D's 2026-08-11 row records the retirement (16:51). App. B (14:47) and App. C (15:46) no longer point to App. D for it. |
| RC2-12 (OWNER) | OK | Resolved after the full-history check. D.1 states the commit dates (X4-6) and their limit: self-reported, set by the committer's clock, private repository. No hash appears. The V3Q16 marker stays for content hashes and log excerpts. |
| RC2-13 | OK | App. F uses "the GPU that ran Γ" and "second GPU". |
| RC2-14 | OK | The abstract, §1 and §6.3 all say "detectable only in the last fifth". §1 adds the checkpoints at updates 900 to 1000, and §6.3 keeps 900/950/1000 in the Γ(t) paragraph. |
| RC2-15 | OK | §1 now points to the home (§6.1). The last sentence of §4.3 is cut. |
| RC2-16 | OK | 06:60 no longer defines unblinding. Note that 06:60 also dropped the "(Appendix D)" pointer for the 72-seed history. App. D.4 still holds that history, and §1 points to App. D generally. Not a finding. |
| RC2-17 | OK | The bracketed addition, the registered rendering of row D and the note are all present (16:89-97). |
| RC2-18 (OWNER) | OWNER | The marker `OWNER-PENDING:V3Q7 also RC1-22 / RC2-18` is in place at 00:41. |
| RC2-19 | OK | Adapted: "a registry of the fixed constants (Appendix B)". The writer's reason for leaving out "code defaults" holds: RC1-1 found that `test_locks.py` checks code defaults for four constants only. |

**RC2-2, replacement for the second sentence at 21:31** (OWNER-EDITS):

> Some decisions are recorded as delegated to the assistant: on the authors' instruction, the assistant made the remaining design decisions before the GPU rental, among them the seed layout, the run order and the ratification of the registered outcome framings, and the authors gave avoiding their own bias as the reason. A few later rulings were the assistant's call at the authors' request.

### New findings (changed lines only)

#### RC2-20 (SHOULD): "exclusion bound" now has two meanings that §5 does not connect

- **Location:** 05_measurement.md:36; 07_example_results.md:58.
- **What is wrong.**
  - §5 defines an exclusion bound as an interval end: either end, read in its direction, or the larger absolute end.
  - §6.3 says completion Γ₄ "is a second exclusion bound, the registration's term for its detection limit, X₄ = 4.88 points".
  - Both are accurate. The registration's X is the 80 %-power MDE (PFB:190-195; RES-6). But a reader who has just learned §5's definition meets the same term meaning a detection limit two pages later, with no warning from §5.
- **Fix.** End §5's sentence with:

  > The registration also calls its detection limit, X, an exclusion bound; §6.3 keeps that registered wording.

  Or leave §5 alone and accept §6.3's own gloss. One clause either way.

#### RC2-21 (SHOULD): App. G now holds part of the blind-spot list it says is listed once in §6.4

- **Location:** 19_appendix_interaction.md:24 (new sentence "The arms met the four conditions differently in training: …"); :30 ("What the check is blind to is listed once, in §6.4"); 08_interaction_check.md:45 (points to Appendix G for it).
- **What is wrong.** PLAN §8 item 8's detail moved from §6.4 to App. G, and §6.4 now points there. App. G's closing sentence still says the list is in §6.4 alone. The content is correct (it matches PLAN.md:184-199), but the pointer is now false.
- **Fix.** At 19:30:

  > What the check is blind to is listed in §6.4; the arms' training conditions are given above.

#### RC2-22 (SHOULD): two wording slips in the rewritten siting paragraph

- **Location:** 06_example_design.md:56.
- **What is wrong.**
  - (a) "Coupling B's calibrated survival effect" says the effect was calibrated. What is meant is the effect measured in calibration (§4.3; CB-9).
  - (b) "that both couplings meet their fixed-value criteria here 'is not the same as both producing behavioural effects there'" puts "here" and "there" in one sentence for one place.
- **Fix.**
  - (a) "Coupling B's survival effect in calibration".
  - (b) "…that both couplings meet their fixed-value criteria at Medium "is not the same as both producing behavioural effects there"". The quotation is unchanged.

### Counts (re-check)

- **Original findings (19):** OK 17 (RC2-12 is included: it was resolved by the full-history check), REOPEN 1 (RC2-2), OWNER 1 (RC2-18).
- **New findings:** MUST 0, SHOULD 3 (RC2-20, RC2-21, RC2-22), OWNER 0.
