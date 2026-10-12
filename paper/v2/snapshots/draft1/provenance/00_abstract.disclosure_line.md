# Provenance: sections/alt/00_abstract.disclosure_line.md

Writer: W1. Checked against the alternate on 2026-10-11. This alternate (owner
question Q4f; review N1) is `sections/00_abstract.md` with the disclosure
moved out of the `<d-footnote>` into a visible italic paragraph directly
after the abstract and before the hero. The text of the disclosure is
unchanged. Every other sentence is identical to the default; the support
and the full change notes are in `provenance/00_abstract.md`, row for row.

Counts (P3's method): the abstract as in the default, **372 prose words,
2,457 characters**; the visible line **49 words** (budget ≤ 50).

| # | sentence (verbatim) | support | change from the demo, and why |
|---|---|---|---|
| 1 | We report a pre-registered test of whether training one policy on co-occurring stressors beats training it on each in isolation, in the Compound Hostile Environment (CHE), a pure-JAX multi-agent environment where a cellular-automaton fire burns in every episode. | DES-12; ENV-6; ENV-11; decision log, TITLE AND TERMINOLOGY RULINGS items 1 and 6 (docs/decision_log.md:5592-5594, :5610-5619); decision log, ABSTRACT item 3 (docs/decision_log.md:5667-5670); CLAUDE.md:14; CLAUDE.md:62-63; docs/theory_foundations.md:173 | as `provenance/00_abstract.md` row 1 |
| 2 | Two stressors are coupled to the fire: structural collapse can add ignitions, and smoke attenuates perception by Beer–Lambert transmittance; the third, communication denial, is independent. | decision log, TITLE AND TERMINOLOGY RULINGS item 1 (docs/decision_log.md:5592-5594); docs/theory_foundations.md:286; docs/theory_foundations.md:344; docs/theory_foundations.md:561; docs/theory_foundations.md:663-667; CA-1; CB-1; COM-6 | as `provenance/00_abstract.md` row 4 |
| 3 | Both arms train at matched compute and are evaluated at a held-out near-critical severity, with task completion and survival as Šidák-corrected co-primaries. | DES-13; DES-12 (co-primary ruled 2026-08-02); CAL-3; DX-401 (β_holdout locked); decision log, T\* RULING (docs/decision_log.md:2980-2981) | as `provenance/00_abstract.md` row 5 |
| 4 | We ran 72 seeds per arm, above the registered cap of 60, a recorded deviation made before unblinding. | DES-3; DES-1; decision log, LADDER BRANCH C (docs/decision_log.md:4616-4623) | as `provenance/00_abstract.md` row 6 |
| 5 | Joint training raises survival by 0.96 points (Šidák-corrected 95 % CI [0.47, 1.44]); completion shows no detectable change (−1.73 points, CI [−4.12, +0.66]), which excludes a joint-training gain larger than 0.66 points. | RES-2; DES-13; RES-1; decision log, UNBLIND RESULT (docs/decision_log.md:4985-4987) | as `provenance/00_abstract.md` row 7 |
| 6 | Both differences are sign unstable over the final half of training: the survival gap opens only in the last fifth, and completion leans negative from 70 % of the budget. | RES-11; RES-12; RES-13; decision log, POST-UNBLIND STAGE RESULT (docs/decision_log.md:5167-5179) | as `provenance/00_abstract.md` row 8 |
| 7 | The survival gain does not survive the inert-share correction. | decision log, UNBLIND RESULT (docs/decision_log.md:4989-4993); RES-6 | as `provenance/00_abstract.md` row 9 |
| 8 | Communication denial is inert under a frozen random-projection encoder at this scale, so the third of the isolated arm's training episodes that carry only it are fire-only. | COM-4; ENV-12; V6-2; DES-8; DES-16; decision log, M5.3 CLOSURE RULING (docs/decision_log.md:1065) | as `provenance/00_abstract.md` row 10 |
| 9 | This is our design error: we kept a stressor already found inert and did not count the fire-only share it created; found before the main training runs, the bias was registered with its correction while they ran, before unblinding. | V6-2; V6-3; V6-1; DES-12; DES-15; decision log, §7 PROPOSALS RULING (docs/decision_log.md:3902-3913); docs/venue_review_2026-08-16.md:122-133; phase6_design_v2.md:30-33; phase6_design_v2.md:69-71 | as `provenance/00_abstract.md` row 11 |
| 10 | The correction is a 20-seed sensitivity arm without those episodes, outside the confirmatory family; joint training's survival differs from that arm's by −0.03 points (CI [−0.68, +0.63]), though it still sees each coupling twice as often, always combined. | DES-13; DES-15; RES-6; DES-14; decision log, UNBLIND RESULT (docs/decision_log.md:4987-4993) | as `provenance/00_abstract.md` row 12 |
| 11 | The fire is an ambient hazard that no reward, cost or constraint channel reads; the reward reads only task variables and agent deaths, pricing every death the same. | ENV-1; docs/theory_foundations.md:66-90; decision log, DEF. 2 WORDING RULING (docs/decision_log.md:5314-5323); decision log, TITLE AND TERMINOLOGY RULINGS item 2 (docs/decision_log.md:5601-5604) | as `provenance/00_abstract.md` row 13 |
| 12 | Severity is set relative to a measured percolation threshold, and each stressor is a parameter of one transition or observation kernel, so ablations are bitwise-exact nested models. | CAL-1; CAL-3; DX-201; DX-204; docs/theory_foundations.md:663-667; CLAUDE.md:46-51; che/tests/test_nesting.py:222 | as `provenance/00_abstract.md` row 14 |
| 13 | We describe a measurement protocol with reproducibility floors per metric, per GPU and per artifact. | METH-1; METH-2; CLAUDE.md:331; CLAUDE.md:353; CLAUDE.md:359 | as `provenance/00_abstract.md` row 15 |
| 14 | We recommend, from this single environment, that studies of compositional generalization match the share of training with an active stressor before attributing a gain to composition. | DES-14; DES-8; RES-6; decision log, ENDPOINT CONFOUND (docs/decision_log.md:4549); paper_v2_prompt.md:176-182 | as `provenance/00_abstract.md` row 16 |
| 15 | We used the LLM assistant Claude as a tool: under our rulings it implemented the environment, training and analysis code, built the figures, helped search the literature, verified the citations, and drafted this text from our recorded rulings and results. | decision log, PAPER V2 items 1 and 2 (docs/decision_log.md:6047-6064); writing_session_prompt.md:17-18 (builder sessions are Claude); CLAUDE.md:3 (the coding agent is the implementation engineer); decision log, FIGURES (docs/decision_log.md:5789-5791: figures "made by the builder (an agent)"); decision log, NO-SCOOP CHECKS (docs/decision_log.md:3334: search checks run by the builder); decision log, READS RULING (docs/decision_log.md:5744-5745: full reads by Claude's web-verification agents); paper/related_work_verification.md:928; decision log, SCAFFOLDING SITE (docs/decision_log.md:5364-5376); paper_v2_prompt.md:32-34 | new: the disclosure as a visible first-page paragraph instead of a `<d-footnote>` (class C, review N1; Q4f). Text identical to `provenance/00_abstract.md` row 2. Recommended over keeping both, so the disclosure is stated once (P3-§6) |
| 16 | We checked every word and are responsible for it. | decision log, PAPER V2 item 1 (docs/decision_log.md:6047-6052); decision log, PAPER V2 item 2 (docs/decision_log.md:6053-6056) | new: the disclosure as a visible first-page paragraph instead of a `<d-footnote>` (class C, review N1; Q4f). Text identical to `provenance/00_abstract.md` row 3. Recommended over keeping both, so the disclosure is stated once (P3-§6) |

## Demo sentences not carried

As in `provenance/00_abstract.md`.

## Alternates

- This file is the Q4f alternate, drafted in the form I recommend: the
  visible line **instead of** the `<d-footnote>`. To keep both, re-insert
  the default's `<d-footnote>` element after the first sentence; nothing
  else changes.

## Open items

1. **Where the line prints.** It sits after the abstract, so in print it
   lands wherever the abstract ends; B2 measured the one-paragraph demo
   abstract on page 2 (`paper/v2/src/VALIDATION.md:152-157`). A variant
   that puts the line **before** the abstract, as the first body
   paragraph, would be the text most likely to print on page 1 under the
   contents box; unmeasured, and it departs from the stub's "directly
   after the abstract". Proposed direction: let the kit build's
   footnote/page-1 report decide (Q4f).
2. A visible paragraph is not literally "a footnote on the first page"
   (PAPER V2 item 2, docs/decision_log.md:6057-6058); whether it meets
   TMLR's FAQ is the owner's reading (Q4f).
3. Kept in step with the default by construction (generated from it this
   session). The open items of `provenance/00_abstract.md` apply.
