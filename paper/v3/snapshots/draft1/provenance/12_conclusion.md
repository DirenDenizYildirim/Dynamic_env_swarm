# Provenance: sections/12_conclusion.md

Writer: W1 (Paper v3, step 4.1, 2026-10-14). Checked against the section
with `paper/v3/src/provenance_check.py --root paper/v3 --strict
12_conclusion` (no snapshot label taken). v2 had no conclusion (STRUCTURE
§11 row 19), so every sentence is new.

Counts (P3's method): **88 prose words** against the budget of 90. No
numbers, no dates, no caveat restated (stub: every caveat pointer-only
here).

| # | sentence (verbatim) | support | change from v2, and why |
|---|---|---|---|
| 1 | 9 Conclusion | framing | new (STRUCTURE §2 heading) |
| 2 | CHE is for studying how stressors coupled to an evolving fire shape what multi-agent policies learn, with each stressor a parameter that can be switched off to reproduce the environment without it exactly. | CLAUDE.md:14-21; CLAUDE.md:44-50 (bitwise ablation nesting); decision log, PAPER V3 item 3 (docs/decision_log.md:6161) | new: what CHE is for (stub sentence 1; P1 §4.2 §9) |
| 3 | Its worked example, a pre-registered test of training on stressors together or apart, is read in §6.3 exactly as registered. | DES-12; decision log, PAPER V3 item 3 (docs/decision_log.md:6163-6166: registered results and strings in full, verbatim) | new: what the example showed, by pointer only (stub: "if the result is restated, only by pointer") |
| 4 | The next experiments would train the corrected isolated arm for longer, so that each coupling's exposure count matches the joint arm's, and would vary coupling strength instead of how often each coupling is on (§6.5). | decision log, PAPER V3 item 4 (docs/decision_log.md:6170-6173: the corrected isolated arm at 2000 updates is future work, no run authorized); paper_v3_prompt.md:210-211 (V3-F4 future work: the exposure-matched corrected arm at 2000 updates, and varying coupling strength) | new: what to run next (stub sentence 3), the two future-work items of §6.5 without numbers (stub: no numbers here). That the longer run gives up matched compute is §6.5's sentence (C11 is not allowed here) |

## HOLE

- `<!-- HOLE:INTERACTION -->` between rows 3 and 4: one clause on the
  check's reading, labelled post hoc (pointer §6.4). It can join row 3
  ("…, and a post hoc check at the test configuration …") or stand as a
  short sentence; about 10 words fit in the remaining budget only if row 2
  is shortened.
