# Provenance: sections/alt/00_abstract.no_recommendation.md

Writer: W1. Checked against the alternate on 2026-10-11. This alternate (owner
question Q6; F4) is `sections/00_abstract.md` without its last sentence, the
labelled recommendation (row 16 of `provenance/00_abstract.md`), which then
lives only in §9.3. Every other sentence, the footnote included, is
identical to the default; the support and the full change notes are in
`provenance/00_abstract.md`, row for row.

Counts (P3's method; footnote excluded): **358 prose words, 2,356 characters** (draft1: 346, 2,274; the fix round's changes are mirrored from the default).

| # | sentence (verbatim) | support | change from the demo, and why |
|---|---|---|---|
| 1 | We report a pre-registered test of whether training one policy on co-occurring stressors beats training it on each in isolation, in the Compound Hostile Environment (CHE), a pure-JAX multi-agent environment where a cellular-automaton fire burns in every episode. | DES-12; ENV-6; ENV-11; decision log, TITLE AND TERMINOLOGY RULINGS items 1 and 6 (docs/decision_log.md:5592-5594, :5610-5619); decision log, ABSTRACT item 3 (docs/decision_log.md:5667-5670); CLAUDE.md:14; CLAUDE.md:62-63; docs/theory_foundations.md:173 | as `provenance/00_abstract.md` row 1 |
| 2 | We used the LLM assistant Claude under our direction; its uses included drafting design documents and reviews, proposing options for our decisions, writing and running the code, analyses and figures, helping with literature search and citations, and drafting this text from our records. | decision log, PAPER V2 items 1 and 2 (docs/decision_log.md:6047-6064); writing_session_prompt.md:17-18 (builder sessions are Claude); CLAUDE.md:3 (the coding agent is the implementation engineer); phase6_design_v2.md:13-15 (the registered design "drafted by the same agent that produced the red team and proposed the remedies it now adopts"); phase6_redteam_v1.md:3 ("Reviewer: RA (internal)"); phase6_redteam_remedies.md:8 ("RA proposal"); kappa_b_lock.md:303 ("RA recommendation"); severity_lock.md:3-5 ("Decided jointly (owner + RA) … independently recomputed by the RA"); decision log, M4.3 lock revision (docs/decision_log.md:276: "The RA measured"); decision log, FIGURES (docs/decision_log.md:5789-5791: figures "made by the builder (an agent)"); decision log, NO-SCOOP CHECKS (docs/decision_log.md:3334: search checks run by the builder); decision log, READS RULING (docs/decision_log.md:5744-5745: full reads by Claude's web-verification agents); decision log, §1 INTRODUCTION item 2 (docs/decision_log.md:5709: "with LLM summaries alongside"); paper_v2_prompt.md:32-34 | as `provenance/00_abstract.md` row 2; changed in the fix round (RC1-1, RC1-8), mirrored here |
| 3 | The authors are responsible for every word. | decision log, PAPER V2 item 1 (docs/decision_log.md:6047-6052: the owner "is responsible for the result"); decision log, PAPER V2 item 2 (docs/decision_log.md:6055-6056: "Authors are fully responsible for every word") | as `provenance/00_abstract.md` row 3; changed in the fix round (RC1-2), mirrored here |
| 4 | Two stressors are coupled to the fire: structural collapse can add ignitions, and smoke attenuates perception by Beer–Lambert transmittance; a third, communication denial, is independent. | decision log, TITLE AND TERMINOLOGY RULINGS item 1 (docs/decision_log.md:5592-5594); docs/theory_foundations.md:286; docs/theory_foundations.md:344; docs/theory_foundations.md:561; docs/theory_foundations.md:663-667; CA-1; CB-1; COM-6 | as `provenance/00_abstract.md` row 4; changed in the fix round (RC1-5), mirrored here |
| 5 | Joint and isolated training are run at matched compute and evaluated at a held-out near-critical severity, with task completion and survival as Šidák-corrected co-primaries. | DES-13; DES-12 (co-primary ruled 2026-08-02); CAL-3; DX-401 (β_holdout locked); CLAUDE.md:64-65 (D2: same architecture and compute); decision log, T\* RULING (docs/decision_log.md:2980-2981) | as `provenance/00_abstract.md` row 5; changed in the fix round (RC1-5), mirrored here |
| 6 | We ran 72 seeds per arm, above the registered cap of 60, a recorded deviation made before unblinding. | DES-3; DES-1; decision log, LADDER BRANCH C (docs/decision_log.md:4616-4623) | as `provenance/00_abstract.md` row 6 |
| 7 | Joint training raises survival by 0.96 points (Šidák-corrected 95 % CI [+0.47, +1.44]); completion shows no detectable change (−1.73 points, CI [−4.12, +0.66]), which excludes a joint-training gain larger than 0.66 points. | RES-2; DES-13; RES-1; decision log, UNBLIND RESULT (docs/decision_log.md:4985-4987) | as `provenance/00_abstract.md` row 7; changed in the fix round (RN1-10, RC1-7, RC2-31), mirrored here |
| 8 | Both differences are sign unstable over the final half of training: the survival gap opens only in the last fifth, and completion leans negative from 70 % of the budget. | RES-11; RES-12; RES-13; decision log, POST-UNBLIND STAGE RESULT (docs/decision_log.md:5167-5179) | as `provenance/00_abstract.md` row 8 |
| 9 | The survival gain does not survive the inert-share correction. | decision log, UNBLIND RESULT (docs/decision_log.md:4989-4993); RES-6 | as `provenance/00_abstract.md` row 9 |
| 10 | Communication denial, inert under a frozen random-projection encoder at this scale, is the only stressor in a third of the isolated arm's training episodes, which are thus fire-only in effect. | COM-4; ENV-12; V6-2; DES-8; DES-16; decision log, M5.3 CLOSURE RULING (docs/decision_log.md:1065) | as `provenance/00_abstract.md` row 10; changed in the fix round (RC1-6, RC1-38), mirrored here |
| 11 | This is our design error: we kept a stressor already found inert and did not count the fire-only share it created; found before the main training runs, the bias was registered with its correction while they ran, before unblinding. | V6-2; V6-3; V6-1; DES-12; DES-15; decision log, §7 PROPOSALS RULING (docs/decision_log.md:3902-3913); docs/venue_review_2026-08-16.md:122-133; phase6_design_v2.md:30-33; phase6_design_v2.md:69-71 | as `provenance/00_abstract.md` row 11 |
| 12 | The correction is a 20-seed sensitivity arm without those episodes, outside the two confirmatory tests; joint training's survival differs from that arm's by −0.03 points (Šidák-corrected CI [−0.68, +0.63]), though it still sees each coupling twice as often, always combined. | DES-13; DES-15; RES-6; DES-14; decision log, UNBLIND RESULT (docs/decision_log.md:4987-4993); che/bench/results/phase6/post_unblind_analysis/post_gamma4_t2000.md:5 (Šidák m = 2 applied to Γ₄ "as the family") | as `provenance/00_abstract.md` row 12; changed in the fix round (RC1-6, RN1-14), mirrored here |
| 13 | The fire is an ambient hazard that no reward, cost or constraint channel reads; the reward reads only task variables and agent deaths, pricing every death the same. | ENV-1; docs/theory_foundations.md:66-90; decision log, DEF. 2 WORDING RULING (docs/decision_log.md:5314-5323); decision log, TITLE AND TERMINOLOGY RULINGS item 2 (docs/decision_log.md:5601-5604) | as `provenance/00_abstract.md` row 13 |
| 14 | Severity is set relative to a measured percolation threshold; each stressor is a parameter of one transition or observation kernel, and switching it off reproduces the nested model's trajectories bit for bit. | CAL-1; CAL-3; DX-201; DX-204; docs/theory_foundations.md:663-667; CLAUDE.md:46-51; che/tests/test_nesting.py:222 | as `provenance/00_abstract.md` row 14; changed in the fix round (RC1-4, RC1-38), mirrored here |
| 15 | We describe a measurement protocol with reproducibility floors per metric, per GPU and per artifact. | METH-1; METH-2; CLAUDE.md:331; CLAUDE.md:353; CLAUDE.md:359 | as `provenance/00_abstract.md` row 15 |

## Demo sentences not carried

| # | demo text (paper/finale.md:13) | why |
|---|---|---|
| D0 | "Studies of compositional generalization should therefore match the share of training that contains an active stressor before attributing a gain to composition." | the advice after "therefore": class A, F4. In this alternate it is not in the abstract at all; §9.3 holds the labelled recommendation (`STRUCTURE.md` §5) |
| D1–D3 | as in `provenance/00_abstract.md` | as there |

## Alternates

- This file is the Q6 alternate. The default, with the labelled sentence, is
  `sections/00_abstract.md`; the disclosure-line alternate is
  `sections/alt/00_abstract.disclosure_line.md`.

## Open items

1. Kept in step with the default by construction (generated from it this
   session); any later edit to the default must be mirrored here.
2. Without the recommendation the abstract ends on the protocol (row 15).
   Whether §1 then needs a pointer to §9.3 is W2's (`STRUCTURE.md` §5).
3. The open items of `provenance/00_abstract.md` apply unchanged.
