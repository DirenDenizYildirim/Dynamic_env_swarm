# Provenance: sections/00_abstract.md

Writer: W1 (Paper v3, step 4.1, 2026-10-14). Checked against the section
with `paper/v3/src/provenance_check.py --root paper/v3 --strict 00_abstract`
(no snapshot label taken). "v2" is `paper/v2/sections/00_abstract.md`, whose
provenance is `paper/v2/provenance/00_abstract.md` ("v2 row n"); the owner's
earlier abstract is `paper/finale.md:13`. Also in this file, as BRIEF §13
asks of W1: the title candidates (V3Q1), the `description`, the v2
sentences not carried, the holes and the owner-pending markers.

Counts (P3's method, `scratchpad/P3/wordcount.py`; comments and inline math
dropped): **250 prose words** against the budget of ≤ 250 (STRUCTURE §3).
Longest sentence: 32 words (row 6). No footnote text (the owner writes it,
PAPER V3 item 6; BRIEF §12).

| # | sentence (verbatim) | support | change from v2, and why |
|---|---|---|---|
| 1 | We present the Compound Hostile Environment (CHE), a pure-JAX multi-agent environment in which a cellular-automaton fire burns in every episode. | CLAUDE.md:14 (pure JAX, multi-agent); CLAUDE.md:62-63 (D1: dynamic hazard in every config); docs/theory_foundations.md:173 (Def. 3, fire-CA kernel); ENV-6; decision log, PAPER V3 item 3 (docs/decision_log.md:6158-6162: "The paper leads with CHE as the contribution"); decision log, TITLE AND TERMINOLOGY RULINGS (docs/decision_log.md:5583) | edited from v2 row 1 toward the owner's own opening (paper/finale.md:13: "We introduce the Compound Hostile Environment (CHE), a pure-JAX multi-agent reinforcement-learning environment in which a cellular-automaton fire burns in every episode"): V3-F1 and V3-F2 put the environment first, so the v2 lead "We report a pre-registered test …" moves to row 5. "reinforcement-learning" cut for the 250-word budget. CHE stays named in full (carried v2 B3 default; OWNER-PENDING marker). The disclosure slot follows this sentence (BRIEF §12) |
| 2 | Structural collapse seeds ignitions (Coupling A), smoke attenuates perception by Beer–Lambert transmittance (Coupling B), and communication denial is an independent third stressor. | docs/theory_foundations.md:286 (Def. 5); docs/theory_foundations.md:344 (Def. 6); docs/theory_foundations.md:561-569 (Def. 7: comms denial "mechanistically independent of the hazard"); CLAUDE.md:18-21; CA-1; CB-1; COM-6; decision log, TITLE AND TERMINOLOGY RULINGS item 1 (docs/decision_log.md:5583) | edited from v2 row 4 ("Two stressors are coupled to the fire: structural collapse can add ignitions, and smoke attenuates perception by Beer–Lambert transmittance; a third, communication denial, is independent."): the coupling names are attached to their mechanisms (V3-F1 lists them by name); "seeds" is BRIEF §8.1's wording ("collapse seeds the fire") and CLAUDE.md:18 ("seed/intensify") |
| 3 | The reward never reads the fire and prices every death the same. | ENV-1; docs/theory_foundations.md:86-97 (Def. 2 clause 1: R reads task variables and the alive transition; no term references h, ρ or c; each death costs d_p whatever its cause); che/env/tasks.py:31-43; che/tests/test_reward_independence.py; che/tests/test_lethality.py:143-162; decision log, DEF. 2 WORDING RULING (docs/decision_log.md:5287) | edited from v2 row 13 ("The fire is an ambient hazard that no reward, cost or constraint channel reads; the reward reads only task variables and agent deaths, pricing every death the same."), shortened to the stub's move (1) wording; kept out of the lead (PAPER V2 item 4: the hazard-blind reward does not lead). The contact-price narrowing (BRIEF §8.1; caveat C29) is §3.3's, not restated here |
| 4 | Severity is placed relative to a measured percolation threshold, switching a stressor off reproduces the environment without it bit for bit, and the code is supplied. | CAL-1; CAL-3; DX-204; che/tests/test_nesting.py:78-88, :222-240; che/tests/test_coupling_b.py:131-156; che/tests/test_comms.py:272-319; CLAUDE.md:46-51; decision log, PAPER V3 item 2(e) (docs/decision_log.md:6157: "we will ship the code") | edited from v2 row 14 ("Severity is set relative to a measured percolation threshold; each stressor is a parameter of one transition or observation kernel, and switching it off reproduces the nested model's trajectories bit for bit."): "the nested model" became "the environment without it" (BR §8 #7: "the nested model is undefined in the abstract"); the kernel clause cut for length; "the code is supplied" added (V3-V1; stub move (1)). Not added for length: "under the same random keys" (P3 §1.2 A4); §1 does not carry it either; §3.4 is its home (BRIEF §8.1) |
| 5 | As a worked example, we report a pre-registered test of whether training one policy on co-occurring stressors beats training it on each in isolation, at matched compute, at a held-out near-critical severity. | DES-12; DES-13; CAL-3; decision log, PAPER V3 item 3 (docs/decision_log.md:6161-6162: "the pre-registered test becomes the worked example"); decision log, T\* RULING (docs/decision_log.md:2940) | edited from v2 row 1 (its test clause) and v2 row 5 ("Joint and isolated training are run at matched compute and evaluated at a held-out near-critical severity …"): the test becomes the worked example (V3-F1; P1 §3.1 move 2's wording). "Pre-registered" attaches to the test only (BRIEF §5.1). "At matched compute" is the ruled phrase (C11 short form) |
| 6 | Joint training raises survival by 0.96 points (Šidák-corrected 95 % CI [+0.47, +1.44]), about a tenth of an agent per episode (0.11 of 12 agents), visible only in the last fifth of training. | RES-2; DES-13; X4-3 (W4's DERIVED row: 0.0095531 × 12 = 0.1146; BRIEF §10's form "about a tenth of an agent per episode (0.11 of 12)"); ENV-6; RES-12 ("last fifth" DERIVED: every exclusion at t ≥ 900 > 800) | edited from v2 rows 7 and 8: the survival result kept with its interval; the size in agents added (V3-F3; BRIEF §9.3 floor), from row X4-3, never from the professor's "0.11" (BRIEF §9.2 trap 4; DX-406 is scoped to the fire-death comparison); the "last fifth" clause moves here from v2 row 8 so that the size and its timing sit together (V3-F3: "It appears only in the last fifth of training") |
| 7 | The survival gain does not survive the inert-share correction. | RES-6; decision log, UNBLIND RESULT (docs/decision_log.md:4978); decision log, PAPER V3 item 3 (docs/decision_log.md:6163-6166) | kept (v2 row 9). Registered string verbatim (C18 short form); the next sentence now defines the correction at once (BR §8 #3: "used before it is explained") |
| 8 | The correction removes from isolated training the third of episodes whose only stressor, communication denial, is inert under a frozen random-projection encoder at this scale. | DES-8; DES-14; DES-16; COM-4; ENV-12; decision log, M5.3 CLOSURE RULING (docs/decision_log.md:1065); che/configs/p6_iso4.yaml:36-39 (the correcting arm is ISO without its δ-only components) | edited from v2 row 10 ("Communication denial, inert under a frozen random-projection encoder at this scale, is the only stressor in a third of the isolated arm's training episodes, which are thus fire-only in effect."), which BR §8 #4 lists for stacked qualifiers; the sentence now says what the correction does and why. The ruled phrase stays whole (C02 short form; BRIEF §5.1). "Fire-only" is §6.2's term, not needed here. The correcting arm's code name is not used (stub: no arm codes needed at abstract level) |
| 9 | Keeping that third was our design error; we registered the correction before any outcome contrast was computed. | DES-8; DES-15 (registered mid-grid and pre-unblind); V6-1; V6-2; V6-3; decision log, §7 PROPOSALS RULING (docs/decision_log.md:3902); paper/v3/BRIEF.md §7.1 | edited from v2 row 11 ("This is our design error: we kept a stressor already found inert and did not count the fire-only share it created; found before the main training runs, the bias was registered with its correction while they ran, before unblinding."), which BR §8 #5 lists (dangling participle; "while they ran" ambiguous). Kept: the owned error and the fact that the correction was registered before unblinding (BRIEF §7 wording constraints), with "unblinding" replaced by its plain definition (BRIEF §5.2: "the first computation of any outcome contrast"). No dates (V3-S2). "Registered", never "pre-registered", for the correction. Wording is the owner's to approve (carried Q4h / A1(ii)) |
| 10 | Completion shows no detectable change and excludes a joint-training gain larger than 0.66 points. | RES-1; decision log, PAPER V3 item 3 (docs/decision_log.md:6165-6166: completion "as an exclusion with its bound") | edited from v2 row 7's completion half; the point estimate −1.73 and its interval are cut for length (the bound is what the registration requires; BRIEF §6.1). Registered wording verbatim (C17 short form) |
| 11 | Both differences are sign unstable over the final half of training: each changes sign between checkpoints. | RES-11; DES-13 (Γ(t) at 11 checkpoints, updates 500–1000); decision log, POST-UNBLIND STAGE RESULT (docs/decision_log.md:5161) | edited from v2 row 8: the registered string verbatim (C16 short form), now with a plain gloss after the colon (BR §8 #2: "sign unstable" undefined). RES-11's sign strings change sign on both co-primaries within the retained span. The "last fifth" clause moved to row 6; "completion leans negative from 70 %" (RES-13) cut for length |
| 12 | Because the share of training with an active stressor equals the two couplings' frequencies summed, less their co-occurrence ($\mu_A + \mu_B - p$), matching that share alone cannot isolate co-occurrence. | X4-1 (W4's DERIVED row: the identity at each arm); DES-14; DES-7; DES-16; paper_v3_prompt.md:205-213 (V3-F4: "State the identity … So matching the active share alone cannot isolate co-occurrence … The advice is never a 'therefore'"); paper/v3/BRIEF.md §9.2 trap 2 | new: the lesson (V3-F2), drafted now as the identity lesson because the interaction check has not run (WRITERS §4 item 4; P1 §3.3 row "Not back in time"; orchestrator instruction). It is a consequence of an identity, not of the result, so it carries no "post hoc" label and no "therefore", "so" or "thus" (V3-F4). It gives no advice. It replaces v2 row 16's recommendation ("match the share of training with an active stressor"), which by the identity un-matches frequency (PROF 3, as relayed in PAPER V3 item 1(3), not a ruling; BRIEF §9.3). Marked `HOLE:INTERACTION` and `OWNER-PENDING:V3Q7`; W5's §6.5 must state the same lesson. C08 and C27 short forms |

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
- `<!-- HOLE:INTERACTION -->` and `<!-- OWNER-PENDING:V3Q7 -->` before
  row 12. When IC rows exist: keep row 12, add one sentence with the
  check's pooled reading labelled post hoc (P1 §3.3 rows N, Pn, Pp), or
  keep row 12 alone (row M). The budget is already at 250, so an added
  sentence needs a cut elsewhere (candidates: the gloss in row 11, "As a
  worked example" → "As an example", or row 4's code clause).
- The central limitation (C01, "sited where composition is weak") is not
  in the abstract: allowed there, but there is no room at 250 words.
  §1 carries it first. Owner's call whether it should replace something.

## Title candidates (V3Q1; `front_matter.yaml` holds T1)

From P1 §2 (`paper/v3/plans/P1.md:100-124`), unchanged in wording; lengths
counted this session with Python `len()`. All are environment-first, state
no result, use "multi-agent" and "stressor", attach "pre-registered" to the
test only, and are YAML-safe (no `"`, no backslash, no `: `) except T3,
which needs single quotes for its colon. No title carries post hoc content
(it could not carry the label).

| # | candidate | leads with | characters | support | note |
|---|---|---|---|---|---|
| T1 (default, in `front_matter.yaml`) | A multi-agent fire environment with coupled stressors, and a pre-registered test of training on them together or apart | the environment, then the worked example | 118 | ENV-6; DES-12; decision log, TITLE AND TERMINOLOGY RULINGS (docs/decision_log.md:5583); P1 §2 T1 | the ratified title's structure without the reward lead (PAPER V2 item 4); well over P1's ~75-character guide (about five printed title lines, by v2's RM-8 measure for a 109-character title) |
| T1s | A multi-agent fire environment with coupled stressors | the environment only | 53 | ENV-6; P1 §2 T1s | fits the preview; the `description` then carries the worked example |
| T2 | A multi-agent fire environment in which collapse seeds fire and smoke attenuates perception | the two couplings, in plain words | 91 | CA-1; CB-1; docs/theory_foundations.md:286, :344; P1 §2 T2 | omits communication denial and the test |
| T3 | The Compound Hostile Environment: coupled fire stressors for multi-agent reinforcement learning | the name | 95 | P1 §2 T3; carried v2 B3 | names CHE; the colon needs single quotes in YAML |
| T4 | Coupled stressors in a multi-agent fire environment, with exact ablations and a pre-registered worked example | the stressors, then exact ablations | 109 | che/tests/test_nesting.py:78-88; DES-12; P1 §2 T4 | "exact ablations" names the bitwise nesting property (V3-F1) |

Rejected (P1 §2): lesson-led titles (depend on the post hoc check);
"a pre-registered null" (log:6166, "null" at most an informal gloss); any
hazard-blind lead.

## `description` (`front_matter.yaml`)

| field | text | support | note |
|---|---|---|---|
| new (in `front_matter.yaml`) | A pure-JAX multi-agent environment in which collapse seeds fire and smoke attenuates perception, every stressor switches off exactly, and a pre-registered test serves as a worked example. | rows 1, 2, 4 and 5 of this abstract; CLAUDE.md:14; docs/theory_foundations.md:286, :344; che/tests/test_nesting.py:78-88; DES-12 | P1 §3.2's direction, rechecked against this abstract (V3-F2): environment first, then the worked example; no result. One line; no `"`, no backslash, no `: `, no digit; 187 characters; parses as the YAML value (`yaml.safe_load`, this session). **HOLE:** recheck once the abstract's lesson is final (STRUCTURE §9) |
| alternative A | P1 §3.2's line: "A pure-JAX multi-agent fire environment whose stressors are coupled to the fire and switch off exactly, with a pre-registered test as a worked example." | P1 §3.2 | vaguer about what the couplings do |

## Findings

- **record / scaffold, class C (report only).** `paper/v3/front_matter.yaml`
  did not exist when W1 started and was created during step 4 (by the
  orchestrator, per its header). W1 edited only its `title` and
  `description` lines.
- **budget, class C.** The abstract is at its 250-word ceiling with the
  identity lesson. Any interaction-check sentence added at step 0.5 needs a
  cut (see "Holes" above).
