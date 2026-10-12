# Provenance: sections/00_abstract.md

Writer: W1. Checked against the section on 2026-10-11 (no `snapshot.sh` label
taken). The demo's abstract is the owner's (`paper/finale.md:13`, carried
verbatim into the demo by `paper/demo_beyond/src/build_demo.py:3`), so the
"change" column compares each sentence with the owner's text. Also in this
file, as `BRIEF.md` §13 asks of W1: the title candidates, the `description`,
the demo sentences not carried, the alternates and the open items.

Counts (P3's method, `plans/P3.md` §5, script at the session scratchpad
`P3/wordcount.py`; footnote excluded): **384 prose words, 2,539 characters**
with the three paragraphs joined by spaces, against the budget of ≤ 360 words
and ≤ 2,600 characters (`STRUCTURE.md` §4) and the owner's 359 words and
2,424 characters. The footnote is 50 words, 333 characters. Longest sentence:
40 words. (Draft1: 372 words, 2,457 characters; the 12 added words are
the fix round's RC1-4, RC1-5, RC1-6 and RN1-14.)

| # | sentence (verbatim) | support | change from the demo, and why |
|---|---|---|---|
| 1 | We report a pre-registered test of whether training one policy on co-occurring stressors beats training it on each in isolation, in the Compound Hostile Environment (CHE), a pure-JAX multi-agent environment where a cellular-automaton fire burns in every episode. | DES-12; ENV-6; ENV-11; decision log, TITLE AND TERMINOLOGY RULINGS items 1 and 6 (docs/decision_log.md:5592-5594, :5610-5619); decision log, ABSTRACT item 3 (docs/decision_log.md:5667-5670); CLAUDE.md:14; CLAUDE.md:62-63; docs/theory_foundations.md:173 | edited, from owner text (paper/finale.md:13). The owner's opening ("We introduce the Compound Hostile Environment (CHE), a pure-JAX multi-agent reinforcement-learning environment in which a cellular-automaton fire burns in every episode, …") is merged with the owner's test clause from the same line ("We then pre-register a test of whether training on co-occurring stressors beats training on each in isolation"), so the abstract leads with what was tested: class A, F2. "Pre-registered" attaches to the 2026-08-13 test only: class B, finding P1-N3. CHE stays named (RV-R4; Q4c default) |
| 2 | We used the LLM assistant Claude under our direction; its uses included drafting design documents and reviews, proposing options for our decisions, writing and running code and analyses, making figures, helping with literature search and citations, and drafting this text from our records. | decision log, PAPER V2 items 1 and 2 (docs/decision_log.md:6047-6064); writing_session_prompt.md:17-18 (builder sessions are Claude); CLAUDE.md:3 (the coding agent is the implementation engineer); phase6_design_v2.md:13-15 (the registered design "drafted by the same agent that produced the red team and proposed the remedies it now adopts"); phase6_redteam_v1.md:3 ("Reviewer: RA (internal)"); phase6_redteam_remedies.md:8 ("RA proposal"); kappa_b_lock.md:303 ("RA recommendation"); severity_lock.md:3-5 ("Decided jointly (owner + RA) … independently recomputed by the RA"); decision log, M4.3 lock revision (docs/decision_log.md:276: "The RA measured"); decision log, FIGURES (docs/decision_log.md:5789-5791: figures "made by the builder (an agent)"); decision log, NO-SCOOP CHECKS (docs/decision_log.md:3334: search checks run by the builder); decision log, READS RULING (docs/decision_log.md:5744-5745: full reads by Claude's web-verification agents); decision log, §1 INTRODUCTION item 2 (docs/decision_log.md:5709: "with LLM summaries alongside"); paper_v2_prompt.md:32-34 | new in draft1 (the disclosure `<d-footnote>`, BRIEF §12; class A, PAPER V2 item 2; review N1). **Fix round (RC1-1, MUST; RC1-8, SHOULD; orchestrator decision 7):** draft1's list ("under our rulings it implemented the environment, training and analysis code, built the figures, helped search the literature, verified the citations, and drafted this text from our recorded rulings and results") read as complete and omitted uses the record documents: design documents and reviews drafted by the agent, and options it proposed for the owner's rulings. Now "its uses included" (not a complete list), with those uses added, and "under our direction" and "our records" in place of the internal word "rulings" (RC1-8). It names no specific review, so it neither asserts nor contradicts RC1-3 (who wrote the 2026-08-16 review; owner item, Q4h and Q16). Draft1's provenance said the footnote "lists every use the record documents"; that was wrong and is withdrawn **Re-check (RC1-R6, SHOULD):** "writing and running the code, analyses and figures" was a zeugma (figures are not run); now "writing and running code and analyses, making figures" (log:5789-5791: figures "made by the builder"). |
| 3 | The authors are responsible for every word. | decision log, PAPER V2 item 1 (docs/decision_log.md:6047-6052: the owner "is responsible for the result"); decision log, PAPER V2 item 2 (docs/decision_log.md:6055-6056: "Authors are fully responsible for every word") | new in draft1 as "We checked every word and are responsible for it." **Fix round (RC1-2, MUST; orchestrator decision 7):** the check had not happened, so the sentence was not true of the draft. Responsibility holds now; the check is the owner's to state, if wanted, at approval |
| 4 | Two stressors are coupled to the fire: structural collapse can add ignitions, and smoke attenuates perception by Beer–Lambert transmittance; a third, communication denial, is independent. | decision log, TITLE AND TERMINOLOGY RULINGS item 1 (docs/decision_log.md:5592-5594); docs/theory_foundations.md:286; docs/theory_foundations.md:344; docs/theory_foundations.md:561; docs/theory_foundations.md:663-667; CA-1; CB-1; COM-6 | from owner text (paper/finale.md:63-66, the owner's §1: "Two stressors are coupled to the fire. Structural collapse can add ignitions (Coupling A), and smoke attenuates each agent's egocentric observation by Beer–Lambert transmittance (Coupling B). A third, the denial of inter-agent links (δ), is independent of it."), shortened. Moved into the opening so that "stressor" and "coupling" are defined before the result: class A, F2. **Fix round (RC1-5, SHOULD):** draft1's "the third" became the owner's "a third" |
| 5 | Joint and isolated training are run at matched compute and evaluated at a held-out near-critical severity, with task completion and survival as Šidák-corrected co-primaries. | DES-13; DES-12 (co-primary ruled 2026-08-02); CAL-3; DX-401 (β_holdout locked); CLAUDE.md:64-65 (D2: same architecture and compute); decision log, T\* RULING (docs/decision_log.md:2980-2981) | from owner text (paper/finale.md:13, "at a held-out severity and matched compute"; paper/finale.md:76-82, the owner's §1, "evaluated at the near-critical severity … which neither saw. Architecture and compute are matched … The co-primary outcomes are task completion and survival, Šidák-corrected"), condensed. "At matched compute" is the ruled phrase (BRIEF §5.3). **Fix round (RC1-5, SHOULD):** draft1's "Both arms train" named no arm; the two arms are now named here, before "Joint training" first appears |
| 6 | We ran 72 seeds per arm, above the registered cap of 60, a recorded deviation made before unblinding. | DES-3; DES-1; decision log, LADDER BRANCH C (docs/decision_log.md:4616-4623) | from owner text (paper/finale.md:13: "with 72 seeds per arm (above the registered seed ladder's cap of 60, a recorded deviation made before unblinding)"); "seed ladder's" cut: class A, F5 (BRIEF §5.2) |
| 7 | Joint training raises survival by 0.96 points (Šidák-corrected 95 % CI [+0.47, +1.44]); completion shows no detectable change (−1.73 points, CI [−4.12, +0.66]), which excludes a joint-training gain larger than 0.66 points. | RES-2; DES-13; RES-1; decision log, UNBLIND RESULT (docs/decision_log.md:4985-4987) | edited, from owner text (paper/finale.md:13: "Joint training raises survival by 0.96 points (Šidák-corrected 95 % CI [0.47, 1.44]); task completion shows no detectable change (−1.73 points, CI [−4.12, +0.66])."). Added: the exclusion bound, "which excludes a joint-training gain larger than 0.66 points" (class B, finding N10), in the owner's own §1 wording (paper/finale.md:101). "Task" dropped before "completion", which the sentence before names. **Fix round (RN1-10, MUST; RC1-7, RC2-31, SHOULD):** "[0.47, 1.44]" became "[+0.47, +1.44]" (BRIEF §10, `+` on positive interval ends; matches §1). Revert form: the owner's "[0.47, 1.44]" |
| 8 | Both differences are sign unstable over the final half of training: the survival gap opens only in the last fifth, and completion leans negative from 70 % of the budget. | RES-11; RES-12; RES-13; decision log, POST-UNBLIND STAGE RESULT (docs/decision_log.md:5167-5179) | edited, from owner text (paper/finale.md:13: "Neither joint-versus-isolated difference keeps a stable sign over the final half of training: the survival gap opens only in the last fifth of the budget, and completion leans negative from 70 % of it onward."). The registered string "sign unstable over the final half" verbatim, on both co-primaries: class B, finding N10 (RV-R2; Q4b) |
| 9 | The survival gain does not survive the inert-share correction. | decision log, UNBLIND RESULT (docs/decision_log.md:4989-4993); RES-6 | edited, from owner text (paper/finale.md:13: "The survival gain does not survive an inert-share correction registered before unblinding."). The registered string verbatim, with "the": class B, finding N10 (RV-R2; Q4b). "Registered before unblinding" moves to row 11, beside the design error |
| 10 | Communication denial, inert under a frozen random-projection encoder at this scale, is the only stressor in a third of the isolated arm's training episodes, which are thus fire-only in effect. | COM-4; ENV-12; V6-2; DES-8; DES-16; decision log, M5.3 CLOSURE RULING (docs/decision_log.md:1065) | edited, from owner text (paper/finale.md:13: "Because communication denial is inert under our frozen random-projection message encoder at this scale, a third of the isolated arm's training episodes contain no active stressor."). The ruled phrase "inert under a frozen random-projection encoder at this scale" exactly (BRIEF §5.1, §5.3); "fire-only" (BRIEF §5.1). **Fix round (RC1-6, RC1-38, SHOULD):** draft1's "so the third of the isolated arm's training episodes that carry only it are fire-only" presupposed the third; the sentence now states that denial is the only stressor in a third of the episodes, and "in effect" marks that they are fire-only behaviourally, not nominally (DES-16) |
| 11 | This is our design error: we kept a stressor already found inert and did not count the fire-only share it created; found before the main training runs, the bias was registered with its correction while they ran, before unblinding. | V6-2; V6-3; V6-1; DES-12; DES-15; decision log, §7 PROPOSALS RULING (docs/decision_log.md:3902-3913); docs/venue_review_2026-08-16.md:122-133; phase6_design_v2.md:30-33; phase6_design_v2.md:69-71 | new: class A, F3, on the record's timeline (class B, finding O1; P1-N1). The design kept δ after δ had been found inert (2026-07-30, V6-2; design 2026-08-02, V6-3) and did not count the fire-only third (venue review :132-133, "What is not registered is that the residual third is behaviourally empty"); identified 2026-08-16 (V6-1), before the grid began on 2026-09-09 (DES-12); registered with ISO-4 on 2026-09-18, mid-grid and before unblinding (DES-15). "Registered", never "pre-registered", for the correction. Replaces the owner's framing "an inert-share correction registered before unblinding" (paper/finale.md:13), which reads as foresight. Dates left to §1 and §9.1 (`STRUCTURE.md` §5). The wording is the owner's to approve (Q4h) |
| 12 | The correction is a 20-seed sensitivity arm without those episodes, outside the two confirmatory tests; joint training's survival differs from that arm's by −0.03 points (Šidák-corrected CI [−0.68, +0.63]), though it still sees each coupling twice as often, always combined. | DES-13; DES-15; RES-6; DES-14; decision log, UNBLIND RESULT (docs/decision_log.md:4987-4993); che/bench/results/phase6/post_unblind_analysis/post_gamma4_t2000.md:5 (Šidák m = 2 applied to Γ₄ "as the family") | edited, from owner text (paper/finale.md:13: "Removing them, in a 20-seed sensitivity arm, raises isolated training's survival by 0.98 points; joint training then differs from it by −0.03 points (CI [−0.68, +0.63]), although it still sees each coupling twice as often and always in combination."). ISO-4 − ISO is omitted, which the stub allows, so B̂ carries no verdict: class B, finding N11 (the owner's words: "raises isolated training's survival by 0.98 points"). "Survival" named, since Γ₄'s completion estimate is a different number (RES-6). **Fix round:** "outside the confirmatory family" became "outside the two confirmatory tests" (RC1-6, SHOULD; BRIEF §5.2 defines "family" only in §9.1); the interval is labelled "Šidák-corrected" (RN1-14, SHOULD; BRIEF §10) |
| 13 | The fire is an ambient hazard that no reward, cost or constraint channel reads; the reward reads only task variables and agent deaths, pricing every death the same. | ENV-1; docs/theory_foundations.md:66-90; decision log, DEF. 2 WORDING RULING (docs/decision_log.md:5314-5323); decision log, TITLE AND TERMINOLOGY RULINGS item 2 (docs/decision_log.md:5601-5604) | from owner text (paper/finale.md:13: "The fire is an ambient hazard: a fixed stochastic process with nothing in it optimizing against the agents, carried by no cost or constraint channel, and invisible to the reward, which reads only task variables and agent deaths and prices every death the same whatever its cause."), shortened, and moved from the opening to the contribution move: class A, F2 (F1 demotes the hazard-blind reward from the lead) |
| 14 | Severity is set relative to a measured percolation threshold; each stressor is a parameter of one transition or observation kernel, and switching it off reproduces the nested model's trajectories bit for bit. | CAL-1; CAL-3; DX-201; DX-204; docs/theory_foundations.md:663-667; CLAUDE.md:46-51; che/tests/test_nesting.py:222 | edited, from owner text (paper/finale.md:13: "Severity levels are placed relative to a measured percolation threshold, and each stressor is a parameter of one transition kernel, so ablations are bitwise-exact nested models"). "Transition or observation kernel", since κ_B lives in the observation kernel: class B, finding N9, in the owner's own §1 wording (paper/finale.md:66-67). **Fix round (RC1-4, RC1-38, SHOULD):** draft1's "so ablations are bitwise-exact nested models" drew exactness from parameterization alone (exactness also needs every draw to be made whether or not the stressor is on, CLAUDE.md:46-51); the clause now states the property itself, in the owner's §1 words (paper/finale.md:68-70, "Switching a stressor off therefore reproduces the nested model's trajectories bit for bit"), without the inference |
| 15 | We describe a measurement protocol with reproducibility floors per metric, per GPU and per artifact. | METH-1; METH-2; CLAUDE.md:331; CLAUDE.md:353; CLAUDE.md:359 | from owner text (paper/finale.md:13: "we also describe a measurement protocol in which reproducibility floors are measured per metric, per GPU and per artifact"), shortened. "We describe" kept: it describes the protocol and does not claim every bar has a floor (BRIEF §9.1) |
| 16 | We recommend, from this single environment, that studies of compositional generalization match the share of training with an active stressor before attributing a gain to composition. | DES-14; DES-8; RES-6; decision log, ENDPOINT CONFOUND (docs/decision_log.md:4549); paper_v2_prompt.md:176-182 | edited, from owner text (paper/finale.md:13: "Studies of compositional generalization should therefore match the share of training that contains an active stressor before attributing a gain to composition."). "Therefore" removed; the advice is labelled as a recommendation and scoped to one environment: class A, F4. The owner's scope ("studies of compositional generalization") kept, the Q6 default. Alternate without it: `alt/00_abstract.no_recommendation.md` |

## Demo sentences not carried

| # | demo text (paper/finale.md:13) | why |
|---|---|---|
| D1 | "As predicted before measurement, the supercritical fire consumes the fuel that collapse would ignite: under trained policies, collapse-seeded ignitions per episode fall 4.8-fold from low to high severity." | "As predicted before measurement" is out: class A, OWNER ITEM 1 (the fall was first seen at the random-policy calibration, DX-9). The finding itself is dropped from the abstract to stay near the budget; it lives in §1 and §5.3 (`STRUCTURE.md` §7). Restoring it corrected is Q5 (Open item 6) |
| D2 | "Removing them, in a 20-seed sensitivity arm, raises isolated training's survival by 0.98 points" | B̂ stated as a verdict: class B, finding N11. Omitted, as the stub allows (row 12) |
| D3 | "The fire is an ambient hazard: a fixed stochastic process with nothing in it optimizing against the agents" | the "non-adversarial" gloss is cut for length; Def. 2's name carries it, and §3 states it (row 13) |

## Title candidates (F1; `front_matter.yaml` holds candidate 1)

Lengths counted this session with Python `len()`. Line estimate: about 26
characters a line at 1280 px (P2 §3, a preview estimate, not a kit
measurement). None leads with the hazard-blind reward (PAPER V2 item 3). All
use the ratified terms ("stressor", "multi-agent", "pre-registered" for the
2026-08-13 test, DES-12; log:5592-5619) and are YAML-safe (no `"`, no
backslash, no `: `, no `<` or `&`).

| # | candidate | leads with | characters | support | note |
|---|---|---|---|---|---|
| T1 (recommended) | A pre-registered test of training on co-occurring versus isolated stressors in a multi-agent fire environment | the test | 109 | DES-12; ENV-6; log:5610-5619 (the ratified title); `plans/P1.md` T1 | the smallest amendment to the ratified title (it drops "A multi-agent fire environment with a hazard-blind reward, and"); states no result, so it cannot show the gain without its qualifier and needs no ruling on whether a title naming the gain must also carry "sign unstable over the final half" (Q3). About five lines at 1280 px |
| T1s | A pre-registered test of training on co-occurring versus isolated stressors | the test, without the domain | 75 | DES-12; log:5610-5619 | the shortened form of T1 for the length limit (P2-7: about 75 characters keeps three lines); the `description` then carries the environment |
| T2 | Training on co-occurring versus isolated stressors in a multi-agent fire environment, a pre-registered test in which joint training's survival gain does not survive the inert-share correction | the question, then the plain result with the registered qualifier | 191 | RES-2; log:4989-4993; `plans/P1.md` T2 (P1's recommendation); review F1 candidate 2 | matches F2's lead and never shows the gain without its qualifier; omits completion's exclusion and the Γ(t) suffix, which is a Q3 ruling; about seven lines. Fix round (RC1-13, SHOULD): draft1's "a pre-registered test whose survival gain" gave the gain to the test; the gain is joint training's |
| T3 | A multi-agent fire environment in which collapse seeds fire and smoke attenuates perception, and a pre-registered test of training on co-occurring versus isolated stressors | the environment's two couplings | 172 | CA-1; CB-1; docs/theory_foundations.md:286, :344; `plans/P1.md` T3 | no result and no communication denial |
| T4 | A pre-registered test of training on co-occurring versus isolated stressors, in a multi-agent environment with an ambient fire hazard | the test, with the ruled term "ambient" | 133 | DES-12; log:5601-5604; log:5610-5619; review F1 candidate 1 | no result. Fix round (RC1-13, SHOULD): draft1's "joint versus isolated training on co-occurring stressors" departed from the ratified wording and misdescribed isolated training; T4 now uses the ratified phrase |

Rejected, with `STRUCTURE.md` §3's reasons: a lead on matching the active
share (F4); "exposure, not composition"; "… accounts for the survival gain"
(B̂ has no verdict); a lead on the sweep; a question title; "a pre-registered
null". A lead on the design error (`STRUCTURE.md` §3 T5, 170 characters) is
not offered: it may read as if the error were the main finding, and it loses
the encoder scope.

## `description` (Q4d)

| field | text | support | note |
|---|---|---|---|
| new (in `front_matter.yaml`) | A pre-registered test of whether training a single policy on co-occurring stressors beats training it on each in isolation, in the Compound Hostile Environment (CHE), a multi-agent environment where a fire burns in every episode. | restates the abstract's new opening, as DESCRIPTION item 3 requires (log:5692-5693); DES-12; ENV-6; CLAUDE.md:62-63 | P1's option A (the test, no result), the Q4d default. One line; no `"`, no backslash, no `: `, no number (DESCRIPTION item 1, log:5687-5689); parses as the YAML value (checked with `yaml.safe_load`). RM-22 (SHOULD, class C) notes that it nearly repeats the abstract's first sentence, so page 1 says it twice; DESCRIPTION item 3 asks for exactly that restatement, so changing it is the owner's (Q4d; option B is the measured alternative) |
| option B | the new line plus: "; the survival gain from joint training does not survive the inert-share correction" | log:4989-4993 | carries the gain with its qualifier but not the completion exclusion or the Γ(t) suffix (P1 option B) |
| revert (the owner's, `paper/finale.md:4`) | In the Compound Hostile Environment (CHE), structural collapse can add ignitions to a cellular-automaton fire, the fire’s smoke attenuates what agents perceive, and inter-agent communication can be denied; the fire itself optimizes against no one and enters no reward, cost or constraint channel. | DESCRIPTION (log:5680) | restates the old opening, which led with the environment and ended on the ambient hazard that F1 demotes |

## Alternates

- `sections/alt/00_abstract.no_recommendation.md` (Q6): the same abstract
  without row 16. Everything else is identical, footnote included.
- `sections/alt/00_abstract.disclosure_line.md` (Q4f): the same abstract
  with the disclosure moved out of the `<d-footnote>` into a visible italic
  paragraph after the abstract and before the hero. I recommend this
  version **instead of** the footnote, not in addition, so the disclosure is
  stated once (P3 §6). Keeping both is a one-line change.
- Default: this file (labelled recommendation; disclosure in a
  `<d-footnote>`).

## Open items

1. **Where the disclosure prints (class C; Q4f, Q22; RM-8, OWNER).** RM
   printed draft1 with the real kit: the footnote marker is on printed
   page 1, after "episode."; its text prints in Distill's footnote list on
   page 47 of 50; page 1 holds the title (six lines in print), the
   `description`, the byline, the contents list and the abstract's first
   paragraph up to "We ran 72 seeds per" (`review/RM.md`, RM-8;
   `out/kit_checks.md`, "Footnote (N1)"). The fix round lengthened the
   first paragraph by three words, so the page break may move; the next
   kit build reports it. RM-8's options for the owner: (a) keep the
   `<d-footnote>` and add the visible line as the abstract's first
   paragraph or right after its first sentence, which would print on page
   1; (b) shorten the title and `description` so that more of the
   abstract lands on page 1; (c) accept the marker on page 1 with the
   text at the end.
2. **The footnote's scope (class C; Q16; RC1-1, RC1-3).** Since the fix
   round it lists uses with "included", so it does not claim to be
   complete, and adds the design documents, reviews and proposed options
   that the record shows the agent drafted. Open for the owner:
   (a) **RC1-3 (OWNER):** the record indicates that a builder (LLM) session
   wrote the 2026-08-16 review that identified the inert-share bias
   (log:3557-3560; `docs/venue_review_2026-08-16.md:22-26`), and the
   registered design says it was drafted by the agent that red-teamed it
   (`phase6_design_v2.md:13-15`). Whether the footnote, §1 and §9.1 should
   say that an LLM-assisted review found the bias is Q4h and Q16. The
   default text neither says nor denies it ("reviews", unnamed);
   (b) whether every LLM-assisted step was Claude: the record does not show
   it for every relay (RC1-1; for example the "independent external
   assessment" of `phase6_framing_allocation_ruling.txt:5-6`);
   (c) the vendor, "(Anthropic)", which the decision log does not state;
   (d) the product name, Claude Code (log:5364);
   (e) whether any code is the owner's own, which the record does not say;
   if so, "writing and running the code" overstates the tool's part.
3. **"We checked every word" is withdrawn (RC1-2, fixed).** The footnote now
   says only "The authors are responsible for every word", which holds now
   (PAPER V2 item 1; TMLR as read, log:6055-6056). If the owner wants the
   check stated, it is theirs to add at approval.
4. **The footnote is 50 words**, so the same text fits the visible-line
   alternate's 50-word budget; a longer, fuller list would need that
   budget relaxed.
5. **Length (LEN; Q20).** 384 words against ≤ 360 (inside the ±10 %
   tolerance), and 2,539 characters against ≤ 2,600 (the owner's: 359,
   2,424). Draft1 was 372 words; the fix round added 12 (RC1-4, RC1-5,
   RC1-6, RN1-14). Cuts that would close the gap, each with a cost: drop
   row 15 (the protocol, contribution 3); drop "pure-JAX" and
   "cellular-automaton" (both on `BRIEF.md` §9.2's floor list); or decline
   RC1-5 and RN1-14 again.
6. **The 4.8-fold finding (class C; Q5).** Dropped for length. Restored
   with the corrected timing it would add about 22 words, for example
   "Under trained policies, collapse-seeded ignitions fall 4.8-fold from low
   to high severity, a fall the random-policy calibration had already
   shown." (CA-4; DX-9; never "as predicted before measurement").
7. **Paragraphing.** The owner's abstract was one paragraph; v2 uses three
   (the test; the results and why the correction exists; the
   contributions and the recommendation). Rejoining them changes no
   sentence, but RM-8 measured that only the first paragraph fits on page 1.
8. **B̂ omitted (finding N11).** If the owner wants it at abstract level,
   the estimate form adds about 15 words: "ISO-4's survival is 0.98 points
   above ISO's, an estimate with no registered test" (RES-7).
9. **The pre-grid identification is unattributed** ("found before the main
   training runs"; V6-1). See item 2(a) for RC1-3's new fact; the
   attribution is Q4h.
10. **Scope wording kept from the owner (Q6):** "studies of compositional
    generalization"; P1 prefers "joint-versus-isolated comparisons".
11. **Not applied (no class-B finding covers it):** P3's suggestion
    (`plans/P3.md` §1.2 A4) to add "under the same random keys, on one
    backend" to the bit-for-bit clause (row 14). Class C, for the owner.
12. **"Measured percolation threshold"** stands as the owner wrote it; the
    lock record's β̂_c has no committed script (O-2, CAL-1 note), and §4
    carries that caveat (Q19).
13. **Title length.** The recommended T1 is 109 characters, over P2-7's
    about-75 guide; T1s is the 75-character form. RM measured T1 at six
    printed lines (RM-8). Choice: Q3.
