# Provenance: sections/alt/00_hero.ladder.md

Writer: W1. Checked against the alternate on 2026-10-11. This is P2's option B
(owner question Q8; `STRUCTURE.md` §9): the opening ladder as the hero,
numbered Figure 1, in place of the explorer. The figure block is the demo's
§1 Figure 3 (`paper/demo_beyond/sections/01_introduction.md:26-33`), with the
iframe `height` set to 427 (the measured self-sized height at 1280 px, from
the orchestrator's table of `paper/v2/out/kit_checks.md`) and a caption
rewritten for the hero position. The figure's printed labels were read this
session from `paper/figures/interactive/out/html/opening_ladder.html` (its
data block, line 72): "registered readings at θ\*, matched budget T\* = 1000 ·
intervals: Šidák 95 % (m = 2)", "full ladder: §9.2", "k 72 / 72", "k 72 / 20",
"unit 1", "cross-unit: JOINT unit 1, ISO-4 unit 2", "outside the confirmatory
family", the verdicts, "does not survive the inert-share correction",
"second exclusion bound, X₄ = 0.0488", and a note defining ISO-4 and
recording k = 72 as a deviation from the cap of 60. No "rung" is printed.

Counts (P3's method, which counts the companion's include caption with the
figure caption): caption 112 words plus figure note 8 = **120** against the
cap of 120 (the stub); reading note 46 words.

**Status: a caption draft, not a buildable page (RM-6, MUST, class C).**
Built with `--alt 00_hero.ladder`, the page loses the explorer, shows the
opening ladder twice and leaves §1, §5 and §6's references to the explorer
as Figure 1 pointing at the ladder (`review/RM.md`, RM-6). The fix is B2's
option-B build flag (`STRUCTURE.md` §9), not text in this file. Show this
file to the owner as a caption draft only, until the flag exists.

| # | sentence (verbatim) | support | change from the demo, and why |
|---|---|---|---|
| 1 | Registered readings: Γ and Γ₄ on survival and completion | RES-1; RES-2; RES-6 | kept (iframe `title`) |
| 2 | Figure 1. The figure prints rates, with intervals conditional on one common evaluation draw; the text quotes them × 100, as points. | DES-13 (the evaluation draw, seed 0 × 512 episodes, common to every run); paper/figures/interactive/out/html/opening_ladder.html:72 (axes "Δ survival rate (fraction)", "Δ completion (fraction)") | edited (demo: "Estimates are rate differences at θ&#42; and matched compute (T&#42; = 1000 updates); the text quotes them × 100, as points. Intervals are Šidák-corrected 95 % (m = 2), conditional on one common evaluation draw;"). Moved to the first line, as P2 §3's hero-position obligation asks; θ\*, T\* and the interval level are not repeated, because the figure prints them (rule R3); renumbered Figure 1 (option B) |
| 3 | Survival: JOINT − ISO (Γ) is REJECT, and the gain does not survive the inert-share correction: JOINT − ISO-4 (Γ₄) is null. | RES-2; RES-6; decision log, UNBLIND RESULT (docs/decision_log.md:4985-4993) | edited (demo: "Survival: Γ REJECT; beneath it, Γ₄ null, “does not survive the inert-share correction”."). The registered verdicts first, the registered string beside the gain (the A1 condition, log:5899-5901); the contrasts named, since in the hero position no text before the figure defines Γ or Γ₄ |
| 4 | Completion: both null; Γ₄ is a second exclusion bound (X₄: its 80 %-power minimum detectable effect). | RES-1; RES-6; METH-7; decision log, UNBLIND RESULT (docs/decision_log.md:4993-4994) | edited (demo: "Completion: Γ null; Γ₄ null, “second exclusion bound, X₄ = 0.0488” (X₄ is Γ₄'s 80 %-power minimum detectable effect)."). X₄'s value is not repeated, because the figure prints it (rule R3). Fix round: "X₄ is its" became "X₄: its" to hold the 120-word cap after RC1-12 |
| 5 | JOINT trains on all stressors together, ISO on each alone; the figure's note defines ISO-4. | CLAUDE.md:64-65 (D2); DES-16; phase6_design_v2.md:60-75 (the components: ISO's single-stressor rows, JOINT's all-on row); paper/figures/interactive/out/html/opening_ladder.html:72 (its note defines the sensitivity arm as ISO without its δ-only components) | new: in the hero position the abstract precedes the figure and does not use the arm names, which the figure prints. **Fix round (RC1-12, SHOULD):** draft1's "JOINT is joint and ISO isolated training" read as circular; the gloss now says what each arm trains on (DES-16: JOINT's components carry every stressor, ISO's one each) |
| 6 | Unit n is GPU n; cross-unit means different GPUs. | HW-4; DX-5; paper/v2/BRIEF.md:221 | new: the gloss of the printed labels "unit 1" and "cross-unit" (class A, F5; BRIEF §5.2; rule R5). The demo's caption carried "one GPU unit" and "cross-unit" unglossed |
| 7 | Not shown: Γ is sign unstable over the final half on both outcomes (Figure 12). | RES-11; decision log, POST-UNBLIND STAGE RESULT (docs/decision_log.md:5167-5168) | edited (demo: "The figure cannot show how Γ moved during training (sign unstable over the final half; Figure 12)"). The registered string kept verbatim; "on both outcomes" added, since the suffix is registered on both co-primaries (BRIEF §6.1) |
| 8 | Its “full ladder: §9.2” is Figure 11. | framing; paper/figures/interactive/out/html/opening_ladder.html:72 (the printed "full ladder: §9.2") | edited (demo: "the full ladder is Figure 11 (§9.2)"). **Fix round (RC1-12, SHOULD):** draft1's "The full ladder is Figure 11 (§9.2)" used "ladder" as the caption's own noun, which BRIEF §5.2 replaces; the printed label is now quoted and pointed to Figure 11 |
| 9 | Status: registered (Γ) · sensitivity arm (Γ₄) · Interact: none. | DES-12; DES-15; DES-13 | edited (demo: "Status: registered (Šidák-corrected 95 %, k = 72) for Γ · sensitivity arm, outside the confirmatory family, for Γ₄ · Interact: none; a fixed reading of two rungs, which Figure 11 steps through with the rest."). The interval level, k and "outside the confirmatory family" are printed on the figure (rule R3); "rungs" is internal jargon (class A, F5). Fix round: "for Γ" became "(Γ)" to hold the 120-word cap after RC1-12 |
| 10 | Joint minus isolated training and joint minus ISO-4, for survival and completion, each with its Šidák-corrected interval and registered verdict; the survival gain is shown beside the ISO-4 contrast, labelled does not survive the inert-share correction. | paper/figures/interactive/MANIFEST.md:212-215 | kept (companion `alt` text) |
| 11 | Static companion of Figure 1 for the printed PDF. | decision log, SUBMISSION FORMAT RULING constraint 4 (docs/decision_log.md:5251-5252) | edited: renumbered from Figure 3 (option B) |
| 12 | Captions carry a status; the recurring ones are illustrative (grades nothing); registered (read by a rule fixed before unblinding); sensitivity arm (outside the two confirmatory tests); secondary (carries no verdict); descriptive (no test); reference scale (cross-artifact), a spread measured on other runs, shown for scale only. | as `provenance/00_hero.md` row 9: decision log, SUBMISSION FORMAT RULING constraint 2 (docs/decision_log.md:5245-5247); DES-12; DES-15; decision log, SECONDARY RESULT (docs/decision_log.md:5073); decision log, POST-UNBLIND STAGE RESULT (docs/decision_log.md:5172-5173); decision log, FIGURE BATCH RULINGS B9 (docs/decision_log.md:5922-5923) | new: the same reading note as the default hero. Fix round (RC1-11, SHOULD), mirrored from `provenance/00_hero.md` row 9 |

## Demo sentences not carried

| # | demo text (`paper/demo_beyond/sections/01_introduction.md:28`) | why |
|---|---|---|
| D1 | "Γ is JOINT − ISO (k = 72 per arm, one GPU unit); Γ₄ is JOINT − ISO-4 (k = 72 / 20, cross-unit), and ISO-4 is a sensitivity arm outside the confirmatory family." | k, the GPU unit and the family are printed on the figure (rule R3); row 3 names the contrasts |
| D2 | "Γ₄'s completion interval, [−0.0481, +0.0228], is drawn but not printed." | cut to meet the 120-word cap; RES-6 holds it and §9.2's table states it |
| D3 | "k = 72 is a recorded deviation from the registered cap of 60." | printed in the figure's note (rule R3) |

## Alternates

- This file is the Q8 alternate (P2 option B). The default hero is
  `sections/00_hero.md` (the explorer, OPENING item 2).

## Open items

1. **The full option-B page needs B2's build flag (class C; Q8;
   `STRUCTURE.md` §9, §13 item 6).** `build_v2.py --alt 00_hero.ladder`
   swaps this file in and nothing else (checked this session: the build
   passes, and §1 then still carries its own opening ladder as Figure 3
   while the explorer is absent). The block move of the explorer to the
   head of §3 and the Figure 1 ↔ 3 renumbering are not implemented.
2. **Printed jargon not glossed here.** The figure's note says "the
   registered seed ladder's cap was 60" ("seed ladder" is the registered
   seed rule, BRIEF §5.2), and its subtitle says "matched budget" where the
   text says "at matched compute". Both are cut from the caption by the
   120-word cap. A label rebuild is Q11.
3. **The stub asked for a gloss of "rung"**, which the opening ladder does
   not print (checked in its data and render code this session); none is
   given.
