# RC2 — claims (part 2) and whole-paper consistency, draft1

Reviewer RC2, Paper v2 phase 1, step 4, pass 2 (2026-10-11/12). Snapshot reviewed:
`paper/v2/snapshots/draft1/sections/` (the live `paper/v2/sections/` files in my scope are
byte-identical to it, checked with `diff -q` this session). Line numbers are snapshot lines.

## Summary

**Counts: 1 MUST, 32 SHOULD, 2 OWNER** (35 rows).

The one MUST is a factual error that is also a contradiction between sections. §9.1 and App. D
call the 2026-08-10 launch batch "the first floor study". App. C's own table lists earlier
floor studies of the same arms (M6.2, M6.2b), and its key calls the batch "the grid's launch
floor study". This is the conflict W5 flagged (W5-F4). The scaffold's glossary (BRIEF §5.2)
is the source of the wrong name.

Everything else the owner directed holds:

- **F3** is owned plainly, with the record's timeline, and its dates agree in the abstract,
  §1, §9.1 and §10.
- **F4** sits only where STRUCTURE §5 puts it.
- **C3/N6** hold: Proposition 4 is an upper bound in words, with one name.
- **The App. D quotations** are verbatim.
- **The registered strings** are intact.

Most SHOULDs fall into four groups: wrong or empty pointers, one-name-per-object slips, unclear
sentences, and LLM-style patterns.

### What I checked, how, and coverage

- **Provenance validity, §9 and §10 (every sentence).** I opened the support of every row of
  `provenance/09_compositional_test.md` (149 rows) and `provenance/10_limitations.md` (38 rows),
  at the entry or line it names, and compared it with the sentence as written. Sources opened:
  - the decision log: T\* RULING; FINAL FIVE; PRE-RENTAL :3136-3160; G1.2 RE-FLOOR :3838-3880;
    §7 PROPOSALS :3900-4175; ENDPOINT CONFOUND; LADDER BRANCH C; PRE-UNBLIND RULINGS; UNBLIND
    RESULT; SECONDARY INSTRUMENT and RESULT; POST-UNBLIND STAGE RESULT; M5.3 CLOSURE and
    PHASE-5 CLOSE; M4.4 :296-340; READS RULING item 4;
  - TF Def. 8, Cor. 1 caveat, Props 3 and 4 with the honesty note, Remark 2‴;
  - `phase6_design_v2.md` :1-40, :55-75, :120-135, :330-372, :418-440;
  - `phase6_framing_branches.md` :90-180, :225-275;
  - `docs/venue_review_2026-08-16.md` :1-16, :108-168;
  - the spine's §10 as committed pre-unblind (`git show f683dd7`, 2026-09-22);
  - `unblind/report.md`, `post_gamma4_t2000.md`, `secondary.md`, `g1/g1_2_report.md` and
    `m62/m62_report.md`;
  - `test_p6_grid.py` :150-215, `test_locks.py` :1-12 and :305-365, and `p6_unblind.py`
    :320-336;
  - the figure HTML labels for Figs 10–13.
- **Provenance validity elsewhere in my scope.** I checked these rows against their sources:
  - §8: 34 of 66 rows (52 %), all of its decision-log citations included;
  - §11: 10 of 17 (59 %);
  - App. A: 7 of about 12 claim units (Props 2–4 and Remark 2′ against TF, `hazard.py` and
    DX-15);
  - App. B–C: 25 of 70 (36 %);
  - App. E–I: about 45 %.

  Every decision-log citation in provenance files 08, 10, 11, 12, 13 and 14 was opened. Class-B
  and "new" rows were prioritised: W5-F1 to F4, N12, N13, N17, P3-N14, P3-N18, O1, the F3 rows
  and the new App. C key.
- **App. D verbatim check (script, scratch `RC2/appd_quotes.py` and `appd_table.py`).**
  - All 10 blockquotes are exact substrings of their sources, after normalising whitespace and
    line wrap and dropping backticks and ledger comments.
  - All 8 rows of the pre-unblind table are identical to log:4923-4930, except two tails cut
    and marked `[…]`.
  - All 10 dates are correct.
- **F5 jargon sweep (script, `RC2/jargon.py`)** over §8–§11, the alternate and the appendix.
  Counts outside verbatim quotations and figure-label glosses:

  | term | count outside quotations and glosses |
  |---|---|
  | "card" | 0 (seven occurrences: five caption glosses, one App. D quotation, one gloss of that quotation) |
  | "ladder" | 0 |
  | "rung" | 0 |
  | `sweep_c50…` | 0 in prose (two caption glosses; five App. H table labels, as allowed) |
  | "re-floor" | 0 |
  | S1–S6 | 0 (six inside App. D's quotation, two in its preface explaining them) |
  | "floor-basis" | 0 (three glosses) |
  | "beat-reproducibility" | 0 (one, in a quotation) |
  | Γ₄′ | defined at first use (Fig. 11 caption, then the table, then §9.2:93 in full) |

  Residual internal terms are filed below (RC2-9, -10, -21, -24, -25).
- **LLM-pattern counts (script, `RC2/llm.py`):** bold-led paragraphs, ", not" antitheses,
  sentences over 40 words, body dates, and announced enumerations and signposts. In my files I
  found no announced enumeration or "this section" signpost, and three ", not" antitheses, all
  registered or rule names.
- **Whole-paper consistency.**
  - Every "Appendix X", "Figure n", "Listing n" and "§n.m" pointer from all sections into my
    files was checked against its target content.
  - Figure numbers 1–13, I1 and I2 are in order.
  - The F3 and F4 wording was compared across the abstract, §1, §7, §9 and §10, and the
    Proposition 4 name across every section.
  - Glossary terms were swept across all sections.
- **Not run by me:** the kit build (its draft1 results were read from `out/kit_checks.md`) and
  the printed PDF. I make no claim about rendering.

## Findings

| ID | severity | file:line | quoted text (short) | problem | evidence | proposed fix | class |
|---|---|---|---|---|---|---|---|
| RC2-1 | MUST | `09_compositional_test.md:56`; `14_appendix_plan_provenance.md:49` | "on the first floor study (2026-08-10)"; "The first floor study (an RTX PRO 6000, 2026-08-10)" | False, and it contradicts App. C. The 2026-08-10 batch (G1.2) was not the first floor study. M6.2 (T = 500) and M6.2b (T = 1000) measured floors of the same ISO and JOINT arms earlier, and App. C's own table lists them (`13:70-71`; M6.2b "set the design k = 40"). App. C's key names the batch "the grid's launch floor study" (`13:91`), so the paper has two names for one study, one of them wrong. | `g1/g1_2_report.md:1-5` ("the launch batch", 2026-08-10); `m62/m62_report.md:1` ("the Phase-6 floor milestone"); `docs/locks.yaml:295-300` (K_CONFIRMATORY 40 ruled 2026-08-03 on `m62b/floors.json`); DX-403; DX-34; W5-F4 (`provenance/13:88-92`, `provenance/08:107-112`) | Use one accurate name in both W6 lines, matching App. C: "the grid's launch floor study (2026-08-10)". The orchestrator corrects BRIEF §5.2's row "launch batch → the first floor study". | B |
| RC2-2 | SHOULD | `11_reproducibility.md:24` (and the alternate `:17`) | "each stage's log records a single run (§9.1)" | Empty pointer: §9.1 does not state this. W6 moved the logs and refusals to App. F (`14:114`, DX-411). | `09:60`; `provenance/09` row 57 ("logs moved to Appendix F") | "(Appendix F)". | B |
| RC2-3 | SHOULD | `09_compositional_test.md:99` | "Γ(t) is **sign unstable over the final half** … (Figure 12)" | App. G (the Γ(t) tables) is referenced nowhere in the body; only the index lists it. STRUCTURE §7 makes App. G hold the tables. | grep of all sections: "Appendix G" occurs only at `12:24` | "(Figure 12; Appendix G gives every value)". | A (LEN / one home) |
| RC2-4 | SHOULD | `12_appendix.md:48` | "a divergence rate taken from Corollary 1(3), which the paper does not state (§4.1)" | The paper's Corollary 1 has items (1) and (2) only (`04:37-38`), so "Corollary 1(3)" points to an item a reader cannot find. §4.1 does not mention the dropped item either. | `04_severity.md:35-40`; TF:217-225 | "The formal specification adds to Proposition 3 a divergence rate from critical exponents; the paper states only what verified sources support (§4.1)." | A (C1 knock-on) |
| RC2-5 | SHOULD | `05_coupling_a.md:85` → `12_appendix.md:48` | "each correction has a known sign (Appendix A)" | The pointer is unsupported at its target. App. A lists the four conditions but gives no signs. TF does record them. | TF:330-339 ((i) a spanning-conditioned reference underestimates χ; (ii) boundary clipping reduces uniform-seed masses; (iii) age-averaging, saturating by about 64 steps; (iv) sibling and overlap effects deflate the slope; "all corrections carry known signs") | W6 adds one sentence to App. A with the four directions as TF states them, or W4 drops "(Appendix A)" from the sign clause. | B |
| RC2-6 | SHOULD | `09_compositional_test.md:32` | "because both couplings' calibration grids had moved survival while their completion effects sat at or below the reproducibility floor (§5–§6)" | Attribution lost. The demo said "as the registration records". As now written, the reason reads as the paper's own finding in §5–§6, while §5.3, §6.4 and §8.6 say these grids have no floor on their own artifact, only cross-artifact reference scales. | log:1695-1701 (the justification chain); `05:99`; `08:75` | "…because, as that ruling records, both couplings' calibration grids had moved survival while their completion effects sat at or below the floors then measured (§5–§6; §8.6 says which have no floor of their own)." | B |
| RC2-7 | SHOULD | `09_compositional_test.md:73` (with `08:55`, `09:48`) | "excludes a joint-training gain larger than 0.66 points. Its bound X … is 3.29 points" | Two quantities are both called the exclusion. "Exclusion bound X" (§8.2, §9.1) is the 80 %-power MDE (3.29), while the stated exclusion is the CI's upper end (0.66). A referee may read them as conflicting. | RES-1 (CI [−4.12, +0.66], X 0.0329); 3.0781 × 0.01068 = 0.0329 (recomputed) | "The completion interval excludes a joint-training gain larger than 0.66 points. Its registered exclusion bound X, the gap of either sign the design would detect with 80 % power on the realized seed dispersion, is 3.29 points, and the negative point estimate does not reject." | A (clarity) |
| RC2-8 | SHOULD | `10_limitations.md:43`; `09_compositional_test.md:66` (Fig. 11 caption) | "carries ISO-4's rise over ISO"; "carries ISO-4's rise" | "Rise" presents B̂ as an established effect. B̂ has no test and no verdict, and FINDINGS N11 rules out "raises" for it. (BRIEF §9.2 uses the phrase too.) | RES-7; FIGURE BATCH B7; FINDINGS N11; `09:95` | §10: "…carries the difference between ISO-4 and ISO (B̂, reported without a test)". Fig. 11: "…carries the ISO-4 − ISO difference". | B |
| RC2-9 | SHOULD | `09_compositional_test.md:54` | "on the owner's attestation that no outcome mean had been computed or viewed" | "Owner" is project vocabulary (F5). A reader of a double-blind paper does not know who "the owner" is. | log:3907-3909 | "on the author's written attestation, recorded with the ruling, that no outcome mean had been computed or viewed". | A (F5) |
| RC2-10 | SHOULD | `09_compositional_test.md:56` | "Bias (b), the second registered caveat, is differential drift … The T = 2000 subsample's differential training-log slopes …" | Three issues in one paragraph: (1) the label "(b)" is orphaned, since no bias (a) appears, and "the second registered caveat" faintly echoes the struck "Registered biases, stated before the result" framing (F3); (2) "The T = 2000 subsample" is used before it is introduced (§9.2:110); (3) the dates 2026-08-10 and 2026-09-08 are outside STYLE's body-date list. | T\* RULING §4 (log:3013-3021, the caveat registered from the launch batch); DES-10; DES-11; STUB-SPEC STYLE (`09:18`) | "A second caveat, registered from the grid's launch floor study, is the differential drift, bias (b): … It read +0.01209 per 100 updates on the launch floor study and +0.0179 on the re-measured floor, both on an RTX PRO 6000, but −0.0083 on GPU 1. In a four-seed-per-arm subsample trained to T = 2000 (§9.2), the differential training-log slopes over updates 500–1000 are …". The label question is RC2-34. | A (F3, F5) |
| RC2-11 | SHOULD | `08_methodology.md:71` | "Bias (b) of §9.1 changed sign between the three floor studies that read it before unblinding; §9.1 reports every reading." | A forward reference to an undefined label, and the sentence does not connect to the paragraph's rule ("measuring is not grading"). | STRUCTURE §11 row 16 (§8.5 states the rule and points) | "A registered caveat is reported at every reading, not only the convenient one: the differential drift of §9.1 changed sign between the three floor studies that read it before unblinding, and §9.1 reports all three." | A (clarity) |
| RC2-12 | SHOULD | `09_compositional_test.md:52` | "with δ off, so the p = 0 sweep arm trains on ISO-4's mixture on JOINT's GPU" | Non-sequitur: δ being off does not imply which GPU the arm ran on, and the GPU is stated nowhere else in §9.1. | DX-5; DX-30 (secondary arms re-run on unit 1) | "Secondary arms run k = 20 seeds, with δ off, on GPU 1. The p = 0 sweep arm therefore carries exactly ISO-4's mixture, on JOINT's GPU, and JOINT, unlike every secondary arm, carries δ = 1.0, inert (§7)." | A (clarity) |
| RC2-13 | SHOULD | `09_compositional_test.md:54` | "Its review question on δ judged the arms symmetric" | A reader cannot tell what a "review question" is. In the record it is one of the questions the design listed for an independent reviewer. | `phase6_design_v2.md:418-433` | "Among the questions it set for an independent reviewer, it judged the arms symmetric on δ, on the premise that neither trains on δ = 1.0 (false for both), and asked for a second opinion." | A (clarity) |
| RC2-14 | SHOULD | `09_compositional_test.md:60` | "fixed the statistic, the sign rule, k = 72 as primary and $A_c$, and unblinding, the first computation …, followed that day" | Garden-path run-on: "and $A_c$, and unblinding" first reads as a list of things the rulings fixed. | — | "The grid ended on 2026-09-22; its runner computes no cross-arm quantity. On 2026-09-26 the pre-unblind rulings fixed the statistic, the sign rule, k = 72 as primary and $A_c$. Unblinding, the first computation of any outcome contrast, followed the same day (Appendix F)." | A (clarity) |
| RC2-15 | SHOULD | `09_compositional_test.md:123` | "the survival gap is about 0.11 per episode of 12" | Unclear unit: 0.11 of what, per episode of 12 what? | DX-406 (0.0096 × 12 agents) | "the survival gap is about 0.11 of the 12 agents per episode". | A (clarity) |
| RC2-16 | SHOULD | `09_compositional_test.md:133` | "This holds by construction, as JOINT's threefold per-coupling frequency over ISO does." | Unclear comparison: a logical possibility is compared with a configured ratio. | ENDPOINT CONFOUND log:4567-4570 | "This is a property of the comparison's design, not of any result, like JOINT's threefold per-coupling frequency over ISO." | A (clarity, F4 home) |
| RC2-17 | SHOULD | `08_methodology.md:33` | "the observed 23.2 % exceeded the one and fell short of the other" | The referents of "the one" and "the other" are left to the reader. | COM-5 | "the observed 23.2 % exceeded the threshold but not the noise." | A (clarity) |
| RC2-18 | SHOULD | `08_methodology.md:69` | "the agents drifted towards a wall (rendered-pixel centroids, a diagnostic)" | Slightly stronger than the instrument. The record says the centroid "cannot separate 'all twelve drifted a little' from 'four parked on the wall'". | log:2614-2622; DX-32 note | "the rendered centroid of the alive agents drifted towards a wall (a diagnostic: it cannot tell all agents drifting a little from a few parked at the wall)". | B (claim to its record) |
| RC2-19 | SHOULD | `13_appendix_locks_floors.md:80` (with `08:33`) | "four bars set without floors … Re-sited at High, it measured its floor first and found that matching Medium's resolution would take roughly 46 seeds" | Internal inconsistency: one of the "four bars set without floors" is described as having measured its floor first. Its record defect is an unreachable 2 × sd bar. | log:1192-1196 ("M5.3b's 2×sd bar at High, which no affordable seed count could reach"); DX-302 note ("floor-less or unreachable bars") | §8.1 and App. C: "four bars set without a floor or, in one case, out of reach". App. C: "Re-sited at High, the test measured its floor first, and its bar of twice that floor proved out of reach: matching Medium's resolution would take roughly 46 seeds per arm." | B |
| RC2-20 | SHOULD | `07_comms.md:25, :71, :73` against `08_methodology.md:33` and `13_appendix_locks_floors.md:80, :82-91` | §7 "content ablation", "the denial study"; §8.1 and App. C "the communication-denial test", "the message-use test at Medium" | One name per object is broken: M5.3 and M5.5 each carry two plain names. App. C's key is headed "plain name in the text", but five of its names occur nowhere else ("the four-run Medium floor study…", "the message-use test", "the refactor that turned…", "the confirmatory arms' floor studies…", "the grid's launch floor study"). | BRIEF §5.2 (one replacement, defined once); STRUCTURE §1 | Pick one name per study across §7, §8 and App. C, for example §7's "content ablation" and "denial study". Head the key column "plain name". | A (F5) |
| RC2-21 | SHOULD | `13_appendix_locks_floors.md:80` | "below the High floor of row M5.3b … the study of row M5.1e … row M5.5, danger moments" | Study codes are used in prose before the key that defines them (`:82-91`). | BRIEF §5.2 (codes only in App. C's study column, with a key) | Move the key above this paragraph, or say "the High floor in the table" and "the Medium floor study on an RTX 5090". | A (F5) |
| RC2-22 | SHOULD | `10_limitations.md:36` | "The registered design kept δ-only episodes in ISO's training mixture after … and left δ out of the secondary sweeps for that reason. It did not count …; … and the branch label stays B (§9.1)." | (1) The F3 mechanism is stated in full a fourth time (abstract `00:26`, §1 `01:40`, §9.1 `09:54`, here). STRUCTURE §5 gives §10 a bullet with consequences and a pointer. (2) "the branch label stays B" is a post-unblind outcome inside the "Registered or recorded before unblinding" list. | STRUCTURE §5 (§10 row), §7 (F3 row: "§7 and §10 point") | "The confirmatory comparison carries the design error of §9.1, which inflates Γ: a third of ISO's training episodes are fire-only. Its correction, registered before unblinding, rests on a 20-seed sensitivity arm outside the confirmatory family, trained on another GPU." Move "the branch label stays B" to the found-after list, or drop it. | A (LEN, F3) |
| RC2-23 | SHOULD | `01_introduction.md:53` against `09_compositional_test.md:97` | "Once the active share is matched, JOINT's remaining differences add nothing detectable to survival, although it still sees each coupling twice as often as ISO-4 and always in combination." | The sentence repeats §9.2:97 almost word for word. STRUCTURE §7 gives §1 one clause for the correction's limits. | STRUCTURE §7 ("the correction's two limits … §1, one clause") | Cut it from §1, or shorten it to "JOINT still sees each coupling twice as often as ISO-4, always in combination (§9.2)". (W2's file.) | A (LEN) |
| RC2-24 | SHOULD | `12_appendix.md:60` | "The handshake gate on the pinned arm passes …, and the free arm scores 1.0000" | Undefined jargon: "handshake gate", "pinned arm" and "free arm". §7 names the arms only in Fig. 9's caption. | `07:25` ("no-idle schedule (pinned)"); DX-15 | "The check that the no-idle denied arm matches ½ + ½q passes (largest absolute z 0.44; χ² 0.51 on 8 degrees of freedom), and the arm with free communication scores 1.0000 at every κ_B." | A (F5) |
| RC2-25 | SHOULD | `08_methodology.md:24` (Fig. 10 caption) | glosses "card", "box", the codes, "Traced", "baseline", "field digests" | The figure also prints "tree" ("per card (and tree, and config)") and "reps" ("completion floor reps at two run lengths"), and neither is glossed. | `paper/figures/interactive/out/html/floors_explorer.html` (TABS titles; length tab label) | Add: "“tree” is a code version and “reps” are identical reruns". | A (F5, R5) |
| RC2-26 | SHOULD | `08_methodology.md:33, 35, 37, 41, 49, 59, 61, 65, 69, 71` | ten paragraphs each opening with a bolded rule sentence | This is the pattern P3 §6 flags first ("bold label opening a paragraph"). §8 has ten such paragraphs in about 940 words, two or three per H3. The stub allowed one bold rule each, but the result reads as mechanical. | `plans/P3.md` §6 table, row 1 | Unbold the rule sentences and let the H3 carry each rule. For example, §8.1 would open: "No acceptance threshold enters an analysis script without a measured floor for the quantity it grades, or an explicit UNDERPOWERED flag." | A (P3 §6) |
| RC2-27 | SHOULD | `14_appendix_plan_provenance.md:49` | "The first floor study … gave … ; the grid GPU's floors gave completion power at a 0.03 effect of 72.2 % at k = 60 and 80.4 % at k = 72." | A 48-word sentence. Its 72.2 % and 80.4 % sit near §9.1's realized 60.2 % and 71.6 % (`09:50`) without the word "design-stage", so they can be misread as the same quantity. | DES-4; DES-6; P3 §6 (≤ 40 words) | "On the grid's launch floor study (an RTX PRO 6000, 2026-08-10), the design-stage MDE₈₀ at k = 40 was 1.55 completion and 0.95 survival points. On the floors of GPU 1, design-stage completion power at a 0.03 effect was 72.2 % at k = 60 and 80.4 % at k = 72; §9.1 gives the realized power." | A |
| RC2-28 | SHOULD | `14_appendix_plan_provenance.md:23` with `:27-29`, `:47`, `:61` | "omissions are marked […]" | Three quotations stop before their source paragraph or list ends, with no mark: item 1 (log:2982-2984 continues), item 4 (design v2:353-354 continues) and item 6 (three further bullets, paraphrased at `:63`). The text quoted is verbatim; only the preface's promise is not kept. | `RC2/appd_quotes.py` output; log:2977-2985; `phase6_design_v2.md:346-354`; log:4140-4150 | "omissions inside a quotation are marked […]", or add a trailing "[…]" to items 1, 4 and 6. | A |
| RC2-29 | SHOULD | `14_appendix_plan_provenance.md:100` | "A … founding registration, verbatim" | Under a column headed "headline claim, as registered", the cell reads as an editor's note rather than a claim. It is literally the registered cell. | `phase6_framing_branches.md:100` | "the founding claim, Γ(θ\*) > 0 on both co-primaries (the registered cell reads “founding registration, verbatim”)". | A (clarity) |
| RC2-30 | SHOULD | `10_limitations.md:23` | "θ\* sits at Medium, where Coupling B's own measured survival effect was … Its survival effect is at High" | "Its" can be read as θ\*'s. | — | "Coupling B's survival effect is at High, …". | A (clarity) |
| RC2-31 | SHOULD | `00_abstract.md:26` | "CI [0.47, 1.44]" | Inconsistent with §1 `01:51` and the §9.2 table ("[+0.47, +1.44]") and with BRIEF §10's "+ on positive interval ends". (W1's file; flagged here for consistency.) | BRIEF §10 (units) | "CI [+0.47, +1.44]". | A |
| RC2-32 | SHOULD | `01_introduction.md:61` | "whose survival advantage does not survive the inert-share correction, registered before unblinding." | Dangling modifier. It can be read as the test being "registered before unblinding", which blurs the paper's own distinction: "pre-registered" for the 2026-08-13 test, "registered before unblinding" for the correction (P1-N3). (W2's file.) | FINDINGS P1-N3; DES-12; DES-15 | "…does not survive the inert-share correction, a correction registered before unblinding." | B (P1-N3) |
| RC2-33 | SHOULD | `09_compositional_test.md:93` | "Proposed on 2026-09-26 after Γ₄ was seen, before that arm was read, and unable by rule to change Γ₄'s qualifier, it agrees" | Three stacked participial phrases before the subject. | — | "It was proposed on 2026-09-26, after Γ₄ was seen and before that arm was read, and by rule it cannot change Γ₄'s qualifier. It agrees: null on both co-primaries." | A (clarity) |
| RC2-34 | OWNER | `09_compositional_test.md:56`; `08_methodology.md:71` | "Bias (b)" | With F3 applied, no "bias (a)" appears anywhere in the paper, so the label "(b)" is orphaned. The owner's rule text says "Bias (b) reverses sign on the grid card". The choice is to keep the record's label (and say once that (a) is the δ design error), or rename it "the differential-drift caveat" and keep "(b)" only as the record's name. | `paper_v2_prompt.md` rules ("Bias (b) reverses sign on the grid card"); spine `00_common_spine.md:432-454` (the old (a) and (b)) | Default: keep "bias (b)", introduced as in RC2-10. The owner decides. | C |
| RC2-35 | OWNER | `12_appendix.md:30, :36, :48, :58` | "The proofs follow the formal specification …"; "The formal specification states that …"; "… displays the bound with an explicit constant …" | App. A grounds its departure notes in "the formal specification", a document the reader cannot see unless a code or record supplement exists. That is undecided (Q4e; the §11 default promises nothing). The notes are accurate but cannot be checked. | FINDINGS Q4e, Q4k; `11:18` | Either put the formal specification in any supplement (Q4e) or reword each note as a statement about this paper ("an earlier, unpublished version of this specification stated …"). | C |

A last pair of unclear sentences, below SHOULD and with no row: `09:50` "GPU 1, the RTX 5090 that ran the grid" (App. F `14:110`: seeds 1–12 first ran on an RTX PRO 6000; "that ran the confirmatory arms" is exact), and `08:35` "moved completion's 2.75-fold and left survival's unchanged" (elliptical; "moved the completion floor 2.75-fold and left the survival floor unchanged"). I offer both for the writers to take or leave.

## Checked and clean

- **Registered strings, verbatim, where BRIEF §6 lands them:**
  - "does not survive the inert-share correction" at `09:91`, `10:43`, App. D `14:54`, plus the
    abstract, §1 and the Fig. 3 caption;
  - "sign unstable over the final half" on both co-primaries at `09:99`, the `09:103` caption,
    App. G `14:118` and `10:44`;
  - "second exclusion bound" with X₄ 0.0488 at `09:81` and `09:91`;
  - "a-fortiori exclusion" with its sentence verbatim at `09:125`;
  - "non-verdict-bearing" once in §9.1 (`09:52`);
  - "the branch label stays B" at `09:91`;
  - "Branch A … did not occur" at `09:89`;
  - "reference scale (cross-artifact)" at `08:75`;
  - "recorded, not graded" at `08:71` and `10:28`;
  - "at matched compute" and convergence claimed nowhere at `09:48`, `10:44` and App. D item 1;
  - completion null as an exclusion with its bound at `09:73`;
  - B̂ with no verdict word in the table, at `09:95` and in the Fig. 11 caption;
  - bias (b) reversing sign on the grid GPU at `09:56`;
  - UNDERPOWERED on the k = 60 analysis, T = 2000, ISO-4's check at High and both change
    points (App. H);
  - VOID for mediation and comms condition (iii).
- **`branch_B.md` §5 lines 1–10** all land where BRIEF §6.2 puts them in my files (§9.1, §9.2,
  §10 items 1, 4, 5 and 8, App. F, App. H). None of the seven §8 "do not claim" items is
  claimed. `09:97` keeps Γ₄ as an exclusion with its upper bound, not an absence.
- **F3:**
  - Owned plainly at `09:54` ("The registered design contains an error"), `01:40`, `00:26` and
    `10:36`. No foresight framing remains apart from RC2-10's phrase.
  - "A registered design caught it", "registered as a bias" and "stated before the result" occur
    nowhere (grep).
  - The timeline agrees with the record and across sections: inert 2026-07-30 (V6-2); design
    2026-08-02, δ excluded from the sweeps as inert yet two δ-only ISO components (V6-3);
    identified 2026-08-16, pre-grid (V6-1); grid from 2026-09-09; registered 2026-09-18,
    mid-grid at 120 of 252, before unblinding (DES-15).
  - No day count.
- **F4:** the recommendation sits in §9.3 (`09:133`), labelled ("We make one recommendation,
  motivated by this result alone"), with its one-environment scope and no "therefore", "so" or
  "thus". §10 only points to it (`10:49`). §1 keeps the logic with "(§9.3)" and no imperative
  (`01:55`). The abstract's sentence is labelled and its scope wording matches §9.3. §9.2 holds
  no advice, and the contributions list has no recommendation.
- **C3 and N6:**
  - Proposition 4 has one name, "A transfer bound for a fixed policy", used only at `09:34`.
    §1 (`01:55`), §10 (`10:39`) and App. A (`12:54`) say "Proposition 4" with no competing name.
  - It is stated in words as an upper bound, with no display and no constant.
  - "Irreducible" appears in no rendered text (only inside STUB-SPEC comments, which staging
    strips).
  - There is no ISO-vs-JOINT slack contrast (`12:58` says the paper "draws no such
    conclusion").
  - The TF honesty note is present at `09:36`.
- **N12** ("does not extrapolate", `09:112`); **N13** (§10's opening scoped to items 1–10;
  "listed, in this order, before unblinding" verified against the spine's §10 as committed in
  `f683dd7` on 2026-09-22, items 1–10 in the same order; item 1 registered as §4a on
  2026-08-13); **N14** (the default §11 promises nothing, and the alternate differs only in its
  first paragraph, confirmed by `diff`); **N17** ("(§5–§6)" at `09:32`; no "one level down" or
  "cost 20 runs"); **P3-N14** (positive covariance only, `09:48`; log:3143-3146); **P3-N18**
  ("the p = 0 sweep arm, which trains on ISO-4's mixture on JOINT's GPU", `09:93`).
- **"Pre-registered"** is used only for the 2026-08-13 test (the title, abstract, §1:27, §1:61
  and the §9 heading). The correction is "registered before unblinding" throughout.
- **App. D:**
  - All 10 quotations and the 8-row table are verbatim; omissions are marked where they fall
    inside a quotation (the trailing ones are RC2-28).
  - Dates: 2026-08-11 (T\* items 2 and 3), 2026-08-13 (restatement, falsifier, amended plan),
    2026-09-18 (inert-share rule, High readout, T = 2000), 2026-08-02 (mediation void rule),
    2026-09-26 (pre-unblind rulings; S1–S6 after unblinding and before the sweep was read).
  - The "§" convention and the S-label explanation are stated; the code version is omitted and
    the omission explained.
- **Derivations recomputed this session:**
  - X = 3.0781 × 0.01068 = 0.0329 (so §8.2's "X is this quantity on the realized dispersion"
    holds);
  - μ = (1 + p − ν)/2, so ν = p at μ = 0.5 and ν = 0.2 + p at μ = 0.4, which is the same
    triangle as App. H's ν = 1 − 2μ + p;
  - the plane's sweep slope γ_p + γ_n = 3.26 − 2.37 = 0.89, equal to the survival sweep slope
    (App. H);
  - JOINT's active share over ISO's is 1/(2/3) = 1.5;
  - 252 = 10 × 20 + 2 × 26 runs; 76 = 2 × 12 + 2 × 26; 96 = 8 × 12;
  - falsifier 1.618 + 2.2365 = 3.855;
  - 0.0096 × 12 ≈ 0.11 agents.
- **Claims against record:**
  - the gate dividing by a floor fired when JOINT's floor fell 51 % against a 12.6 % drift fall
    (`g1_2_report.md:37-46`);
  - test_locks compares every non-null analysis constant with its module literal
    (`test_locks.py:347-361`), as §11 says;
  - seed-major order and chunk boundaries (`test_p6_grid.py:173-197`);
  - the single-card curve is the t = 1000 checkpoints re-evaluated on GPU 3 (the figure's own
    labels), as Fig. 12's caption and App. G say;
  - the grey band in Fig. 11 is ±X (80 %-power MDE), as its caption says;
  - Remark 2′'s extra step (q̃/q → 1, peak at moderate κ_B, largest relative bite at low κ_B)
    matches TF Remark 2‴ (:509-521);
  - Proposition 4's proof idea matches TF :627-633.
- **Cross-references:**
  - every "Appendix A–I" reference from any section lands on the content it names, except
    RC2-2;
  - Appendix letters are contiguous and agree between the index (`12:18-26`) and the headings;
  - Figures 1–13, I1 and I2 are numbered in reading order and referenced by number only;
  - Listings 1–6 are referenced at their homes.
- **GPU naming:** GPU 1–3 are defined once (`09:50`) and used consistently in §9.2, §10 item 8,
  §11, App. C, App. F and App. G. Every "card" or "unit" left in my files is a gloss of a
  figure-printed label or sits inside a verbatim quotation.
- **Double-blind (text only):**
  - no names, URLs, absolute paths or commit hashes in my files' rendered text;
  - code paths appear only in listing labels, App. H's arm-label table, App. B's code
    identifiers and the alternate §11;
  - App. D's omitted code version is explained, not quoted.
