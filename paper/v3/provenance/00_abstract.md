# Provenance: sections/00_abstract.md

Writer: W1 (Paper v3, step 4.1, 2026-10-14). Checked against the section
with `paper/v3/src/provenance_check.py --root paper/v3 --strict 00_abstract`
(no snapshot label taken). "v2" is `paper/v2/sections/00_abstract.md`, whose
provenance is `paper/v2/provenance/00_abstract.md` ("v2 row n"); the owner's
earlier abstract is `paper/finale.md:13`. Also in this file, as BRIEF §13
asks of W1: the title candidates (V3Q1), the `description`, the v2
sentences not carried, the holes and the owner-pending markers.

Counts (P3's method, `paper/v3/src/wordcount.py`; comments and inline math
dropped): **242 prose words** after the final pass (draft1: 250; fix round:
234) against the budget of ≤ 250 (STRUCTURE §3), leaving 8 words for the
check's result (RM-1); a longer sentence needs row 11 shortened. Longest sentence: 31 words (row 4). No footnote text (the owner writes it,
PAPER V3 item 6; BRIEF §12).

| # | sentence (verbatim) | support | change from v2, and why |
|---|---|---|---|
| 1 | We present the Compound Hostile Environment (CHE), a pure-JAX multi-agent environment in which a cellular-automaton fire burns in every episode. | CLAUDE.md:14 (pure JAX, multi-agent); CLAUDE.md:62-63 (D1: dynamic hazard in every config); docs/theory_foundations.md:173 (Def. 3, fire-CA kernel); ENV-6; decision log, PAPER V3 item 3 (docs/decision_log.md:6158-6162: "The paper leads with CHE as the contribution"); decision log, TITLE AND TERMINOLOGY RULINGS (docs/decision_log.md:5583) | edited from v2 row 1 toward the owner's own opening (paper/finale.md:13: "We introduce the Compound Hostile Environment (CHE), a pure-JAX multi-agent reinforcement-learning environment in which a cellular-automaton fire burns in every episode"): V3-F1 and V3-F2 put the environment first, so the v2 lead "We report a pre-registered test …" moves to row 4. "reinforcement-learning" cut for the budget. CHE stays named in full (carried v2 B3 default; OWNER-PENDING marker). The disclosure slot follows this sentence (BRIEF §12) |
| 2 | Collapse seeds ignitions (Coupling A), smoke attenuates perception (Coupling B) and communication denial is an independent third stressor; the reward never reads the fire. | docs/theory_foundations.md:286 (Def. 5); docs/theory_foundations.md:344 (Def. 6); docs/theory_foundations.md:561-569 (Def. 7: comms denial "mechanistically independent of the hazard"); CLAUDE.md:18-21; CA-1; CB-1; COM-6; ENV-1; docs/theory_foundations.md:86-97 (Def. 2 clause 1: no term of R references h, ρ or c); che/env/tasks.py:31-43; che/tests/test_reward_independence.py; decision log, TITLE AND TERMINOLOGY RULINGS item 1 (docs/decision_log.md:5583) | edited from v2 row 4 and v2 row 13. **Fix round (RM-1, MUST; budget so the check's result fits):** draft1's two sentences ("Structural collapse seeds ignitions (Coupling A), smoke attenuates perception by Beer–Lambert transmittance (Coupling B), and communication denial is an independent third stressor." and "The reward never reads the fire and prices every death the same.") are merged; "Structural", "by Beer–Lambert transmittance" (RC1-22's suggested cut) and "prices every death the same" are cut here and stay in §1 (Beer–Lambert, the death price) and §3 (homes) |
| 4 | As a worked example, a pre-registered test asks whether one policy trained on co-occurring stressors beats one trained on each in isolation, at matched compute and a held-out near-critical severity. | DES-12; DES-13; CAL-3; decision log, PAPER V3 item 3 (docs/decision_log.md:6161-6162: "the pre-registered test becomes the worked example"); decision log, T\* RULING (docs/decision_log.md:2940) | edited from v2 rows 1 and 5 (the test becomes the worked example; V3-F1; P1 §3.1 move 2). "Pre-registered" attaches to the test only (BRIEF §5.1); "at matched compute" (C11 short form). **Fix round (RM-1):** draft1's "we report a pre-registered test of whether training one policy … beats training it …, at matched compute, at a held-out …" tightened by three words. "Held-out" kept here: the abstract names the severity it qualifies, unlike the hero (RC1-16) |
| 5 | Joint training raises survival by 0.96 percentage points (Šidák-corrected 95 % CI [+0.47, +1.44]), about a tenth of an agent per episode, detectable only in the last fifth of training. | RES-2; DES-13; X4-3 (W4's DERIVED row: 0.0095531 × 12 = 0.1146, "about a tenth of an agent"); RES-12 (Šidák CI excludes 0 only at t = 900, 950, 1000; "last fifth" DERIVED, t ≥ 900 > 800) | edited from v2 rows 7–8; size in agents added (V3-F3), from X4-3, never the professor's "0.11" (BRIEF §9.2 trap 4). **Fix round:** "visible" → "detectable" (RC1-3, RN1-4, RC2-14: survival's point estimate is positive from update 650, so only the detectable gain is confined to the last fifth); "points" → "percentage points" (RC1 readability item 1); "(0.11 of 12 agents)" cut for the budget (RC1-22's suggested cut; §1 keeps it). The wording "detectable only in the last fifth of training" is the same in §1, which adds the checkpoints (RC2-14) |
| R1 | Severity is placed relative to a measured percolation threshold, switching a stressor off reproduces the environment without it bit for bit under the same random keys on one backend, and the code is supplied. | CAL-1; CAL-3; DX-204; che/tests/test_nesting.py:78-88, :222-240; che/tests/test_coupling_b.py:131-156; che/tests/test_comms.py:272-319; CLAUDE.md:46-51 ("given the same PRNG keys"); decision log, PAPER V3 item 2(e) (docs/decision_log.md:6157: "we will ship the code") | edited (blind-review revision, 2026-11-03; was row 3: “Severity is placed relative to a measured percolation threshold, switching a stressor off reproduces the environment without it bit for bit under the same ra…”) |
| R2 | The gain does not survive a correction for our design error: a third of the isolated arm's episodes carried only communication denial, which had no detectable effect in calibration. | DES-8; DES-14 (active share: isolated arm 2/3, corrected arm 1, joint arm 1); DES-16; COM-4; che/configs/p6_iso4.yaml:36-39 (the correcting arm is ISO without its δ-only components) | edited (blind-review revision, 2026-11-03; was row 7: “The correction trains an isolated arm without the third of episodes whose only stressor, communication denial, had no detectable effect in calibration, match…”) |
| R3 | Against an arm trained without them, registered outside the pre-registered test, before any outcome contrast was computed, joint training shows no detectable survival difference. | DES-8; DES-15 (sensitivity arm outside the confirmatory family; registered mid-grid, pre-unblind); V6-1; V6-2; V6-3; decision log, §7 PROPOSALS RULING (docs/decision_log.md:3902); paper/v3/BRIEF.md §7.1 | edited (blind-review revision, 2026-11-03; was row 8: “Keeping that third was our design error; we registered the correction, outside the pre-registered test, before any outcome contrast was computed.”) |
| R4 | Because the share of training with an active stressor equals the couplings' frequencies summed, less their co-occurrence ($\mu_A + \mu_B - p$), holding that share fixed cannot isolate co-occurrence. | X4-1 (W4's DERIVED row: the identity at each arm); DES-14; DES-7; DES-16; paper_v3_prompt.md:205-213 (V3-F4); paper/v3/BRIEF.md §9.2 trap 2; DES-7; paper/v3/review/blind_review.md W1 | edited (blind-review revision, 2026-11-03; was row 11: “Because the share of training with an active stressor equals the couplings' frequencies summed, less their co-occurrence ($\mu_A + \mu_B - p$), matching it a…”); W1: identity recast as a design note |
| R5 | The example leaves co-occurrence unidentified but yields a design note. | paper/v3/review/blind_review.md W1 and §6 item 1; RES-2; RES-6; paper/v3/review/blind_review.md W1 and §6 item 1; RES-2; RES-6 | edited (blind-review revision, 2026-11-03; was row R5: “The example finds no co-occurrence effect but yields a design note.”); W1: state the null plainly; identity recast as a design note |
| R6 | The uncorrected completion difference excludes a joint-training gain larger than 0.66 points, and both uncorrected differences change sign across checkpoints in the final half of training. | RES-1; decision log, PAPER V3 item 3 (docs/decision_log.md:6165-6166: completion "as an exclusion with its bound") | edited (blind-review revision, 2026-11-03; was row R5: “The uncorrected completion difference excludes a joint-training gain larger than 0.66 points, and both uncorrected differences change sign across checkpoints…”) |
| R7 | We used Claude (Anthropic), an LLM assistant, through Claude Code. | owner statement, 2026-11-03 (the owner's disclosure; TMLR FAQ: LLM use stated in a first-page footnote) | new (blind-review revision, 2026-11-03); A1: footnote drafted from the owner's statement |
| R8 | Claude wrote the simulator's code and tests, and we debugged it; some of the simulator's design decisions were left to Claude. | owner statement, 2026-11-03 | new (blind-review revision, 2026-11-03); A1: who built and who debugged the simulator, in the owner's words |
| R9 | Claude also ran the analyses and drafted the text. | docs/decision_log.md:6193-6202 | new (blind-review revision, 2026-11-03); A1: footnote |
| R10 | Appendix I states who did what. | framing | new (blind-review revision, 2026-11-03); A1: footnote |

## v2 sentences not carried

| # | v2 text | why |
|---|---|---|
| D1 | "We ran 72 seeds per arm, above the registered cap of 60, a recorded deviation made before unblinding." (v2 row 6) | stub: "The 72-seed deviation is not needed here"; BR §8 #1; home §6.2 (C09) |
| D2 | "The correction is a 20-seed sensitivity arm …; joint training's survival differs from that arm's by −0.03 points (Šidák-corrected CI [−0.68, +0.63]), though it still sees each coupling twice as often, always combined." (v2 row 12) | BR §8 #6; length; "twice as often" is homed in §6.3 (C06) and not allowed in the abstract |
| D3 | "We describe a measurement protocol with reproducibility floors per metric, per GPU and per artifact." (v2 row 15) | BR §8 #8 ("floor" undefined); length; §1 and §5 carry it |
| D4 | "We recommend, from this single environment, that studies of compositional generalization match the share of training with an active stressor before attributing a gain to composition." (v2 row 16) | replaced by the identity lesson (row 12; V3-F4; v2 B5 settled) |
| D5 | v2 rows 2–3, the disclosure footnote | the owner writes the footnote in v3 (PAPER V3 item 6); only the slot is left |

## Holes and owner-pending markers in the section

- `<!-- OWNER: disclosure d-footnote here … -->` after sentence 1 (BRIEF §12).
- `<!-- OWNER-PENDING:V3Q1 … -->` (title; candidates below).
- `<!-- OWNER-PENDING:B3 … -->` (CHE named in full; carried v2 default).
- `<!-- OWNER-PENDING:V3Q7 -->` before row 11. The interaction check's
  slot is removed (NO INTERACTION CHECK, 2026-10-19); row 11, the identity
  lesson, stands alone (row M without the check). The abstract is 242
  words, so 8 words are free under 250.
- `<!-- OWNER-PENDING:V3Q7 also RC1-22 / RC2-18 … -->` before row 4: the
  central limitation (C01, "sited where composition is weak") is not in the
  abstract. Both claims reviewers raised it as OWNER (RC1-22, RC2-18); it is
  allowed here; with the check's sentence gone, the 8 free words could hold
  a short form (the owner decides).
  §1 carries it first. RC1-22's proposal (17 words, "The test sits where
  composition is weak: at its severity, smoke's own survival effect was too
  small to detect in calibration.") or RC2-18's clause on row 4 are the
  options; the owner decides, possibly beside the lesson
  (RC2-18). There is no V3Q id for it, so the marker uses V3Q7, the
  abstract's lesson.

## Title candidates (V3Q1; `front_matter.yaml` holds T5 since the final pass)

**Final pass (orchestrator, RM-1 / RM-OWNER-2):** the default in
`front_matter.yaml` switched from T1 (118 characters, 7 printed lines) to
T5, the shortest candidate W1 judges accurate: 60 characters, inside P1's
~75-character guide. "Exact stressor ablations" is the bitwise nesting
property (under the same random keys, on one backend; §3.4). T5 omits the
worked example and the couplings, which the `description` and the abstract
carry. T6 (74) is also accurate and names all three stressors; T1 remains
the option that names the worked example. All candidates stay listed; the
choice is the owner's (OWNER-PENDING:V3Q1 kept).

T1–T4 from P1 §2 (`paper/v3/plans/P1.md:100-124`), unchanged in wording; T5
and T6 added in the fix round as shorter options (RM-OWNER-2; RC1-24); lengths
counted this session with Python `len()`. All are environment-first, state
no result, use "multi-agent" and "stressor", attach "pre-registered" to the
test only, and are YAML-safe (no `"`, no backslash, no `: `) except T3,
which needs single quotes for its colon. No title carries post hoc content
(it could not carry the label).

| # | candidate | leads with | characters | support | note |
|---|---|---|---|---|---|
| T1 (default until the final pass) | A multi-agent fire environment with coupled stressors, and a pre-registered test of training on them together or apart | the environment, then the worked example | 118 | ENV-6; DES-12; decision log, TITLE AND TERMINOLOGY RULINGS (docs/decision_log.md:5583); P1 §2 T1 | the ratified title's structure without the reward lead (PAPER V2 item 4); well over P1's ~75-character guide; the v3 kit build prints it on 7 lines of page 1 (RM-1, RM-OWNER-2) |
| T1s | A multi-agent fire environment with coupled stressors | the environment only | 53 | ENV-6; P1 §2 T1s | fits the preview; the `description` then carries the worked example |
| T2 | A multi-agent fire environment in which collapse seeds fire and smoke attenuates perception | the two couplings, in plain words | 91 | CA-1; CB-1; docs/theory_foundations.md:286, :344; P1 §2 T2 | omits communication denial and the test |
| T3 | The Compound Hostile Environment: coupled fire stressors for multi-agent reinforcement learning | the name | 95 | P1 §2 T3; carried v2 B3 | names CHE; the colon needs single quotes in YAML |
| T4 | Coupled stressors in a multi-agent fire environment, with exact ablations and a pre-registered worked example | the stressors, then exact ablations | 109 | che/tests/test_nesting.py:78-88; DES-12; P1 §2 T4 | "exact ablations" names the bitwise nesting property (V3-F1) |
| T5 (new, fix round; RM-OWNER-2, RC1-24; default in `front_matter.yaml` since the final pass) | A multi-agent fire environment with exact stressor ablations | the environment and its nesting property | 60 | che/tests/test_nesting.py:78-88; CLAUDE.md:44-50 | short (fits P1's ~75-character guide, saving page-1 lines, RM-1); avoids "coupled stressors" for all three (RC1-24); omits the worked example, which the `description` carries |
| T6 (new, fix round; RM-OWNER-2, RC1-24) | Collapse, smoke and communication denial in a multi-agent fire environment | the three stressors by name | 74 | docs/theory_foundations.md:286, :344, :561; CA-1; CB-1; COM-6 | names all three stressors without calling all three coupled (RC1-24); under 75 characters; omits the worked example |

RC1-24 notes that "coupled stressors" (T1, T1s, T4, and T3's "coupled fire
stressors") may read as all three being coupled, while communication denial
is independent. Not changed in T1–T4 (owner's choice, V3Q1). RC1-24's T1′
("… whose collapse and smoke feed the hazard …") is not offered: smoke does
not feed the hazard, it attenuates perception (Def. 6).

Rejected (P1 §2): lesson-led titles (depend on the post hoc check);
"a pre-registered null" (log:6166, "null" at most an informal gloss); any
hazard-blind lead.

## `description` (`front_matter.yaml`)

| field | text | support | note |
|---|---|---|---|
| new (in `front_matter.yaml`) | A pure-JAX multi-agent environment in which collapse seeds fire, smoke attenuates perception and every stressor switches off exactly, with a pre-registered test as a worked example. | rows 1–4 of this abstract; CLAUDE.md:14; docs/theory_foundations.md:286, :344; che/tests/test_nesting.py:78-88; DES-12 | P1 §3.2's direction, rechecked against this abstract (V3-F2): environment first, then the worked example; no result. **Fix round (RC1-6, SHOULD):** draft1's "…, every stressor switches off exactly, and a pre-registered test serves as a worked example" put the test inside "in which"; now RC1-6's wording. One line; no `"`, no backslash, no `: `, no digit; 181 characters; parses with `yaml.safe_load` (this session). **HOLE:** recheck once the abstract's lesson is final (STRUCTURE §9) |
| alternative A | P1 §3.2's line: "A pure-JAX multi-agent fire environment whose stressors are coupled to the fire and switch off exactly, with a pre-registered test as a worked example." | P1 §3.2 | vaguer about what the couplings do |

## Findings

- **record / scaffold, class C (report only).** `paper/v3/front_matter.yaml`
  did not exist when W1 started and was created during step 4 (by the
  orchestrator, per its header). W1 edited only its `title` and
  `description` lines.
- **budget (final pass, RM-1).** The abstract is 242 words; 8 words are
  free (the check's sentence is removed; see "Holes" above).

**NO INTERACTION CHECK (2026-10-19).** The owner ruled that the post hoc interaction check is not run before submission and leaves the paper (decision log, NO INTERACTION CHECK (docs/decision_log.md:6495)). §6.4 and Appendix G were removed; §6.5 became §6.4 and Appendices H, I and J became G, H and I. This file was updated to match: the HOLE:INTERACTION marker and its fill comment were removed; no prose sentence changed.
