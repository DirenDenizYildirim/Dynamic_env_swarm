# Provenance: sections/09_example_lesson.md

Writer: W5 (Paper v3, step 4.1, 2026-10-14). Checked with
`paper/v3/src/provenance_check.py --strict`. `log` = `docs/decision_log.md`.
v2's §9.3 (`paper/v2/sections/09_compositional_test.md:131-135`, "A
recommendation and its scope") is **replaced, not reused** (V3-F4; STUB-SPEC):
its advice, "match the share of training that contains an active stressor",
un-matches per-coupling frequency by the identity (PAPER V3 item 1(3), a
review relayed in the ruling; BRIEF §9.3).

| # | sentence (verbatim) | support | change from v2, and why |
|---|---|---|---|
| 1 | 6.5 What the example teaches | framing | new (heading as the stub fixes it) |
| 2 | By the identity of §6.2, holding the active share fixed while co-occurrence changes forces per-coupling frequency to change with it, so matching the active share alone cannot isolate co-occurrence. | X4-1 (active share = μ_A + μ_B − p at every arm); DES-14; paper_v3_prompt.md:207 (V3-F4: "So matching the active share alone cannot isolate co-occurrence") | new; replaces v2 09:133 ("We make one recommendation ... match the share of training that contains an active stressor"). HOME of C27. Derivation in words: at fixed active share a, μ_A + μ_B = a + p, so a change in p moves the frequencies. The identity itself is not restated (home §6.2, C08) |
| 3 | None of the study's designs isolates it. | DES-9; DES-14; X4-1; paper/v3/BRIEF.md:464 (§9.2 trap 2: "No design in the record isolates co-occurrence") | new |
| 4 | The sweep holds each coupling's frequency fixed and moves the fire-only share with co-occurrence. | DES-9 ("sweep: m = 0.5, n = p"); SEC-5; che/bench/results/phase6/secondary/secondary.md:7-16 | new. "The sweep" matches §6.3's name for it (W4) |
| 5 | The inert-share correction holds the active share fixed and moves frequency along with co-occurrence (§6.3). | DES-14 (active share ISO‑4 1, JOINT 1; per-coupling frequency 0.5 against 1.0, ratio 2×; ISO‑4 co-occurrence 0) | new. "twice as often" is not repeated (home §6.3, C06) |
| 6 | The plane's co-occurrence slope holds the fire-only share fixed and moves frequency with co-occurrence. | SEC-1; DES-9; paper/v3/BRIEF.md:461-463 (ν = 1 − 2μ + p in every arm, so each slope moves frequency with it); paper/v2/sections/14_appendix_plan_provenance.md:154 | new. Never "separates co-occurrence from frequency" (`checks/terms.txt`) |
| 7 | Two experiments would go further. | framing; decision log, PAPER V3 (docs/decision_log.md:6170-6173, item 4); paper_v3_prompt.md:211-212 | edited; fix round RC2-7 ("Two designs would come closer" claimed isolation for the strength design) |
| 8 | ISO-4 trained for 2000 updates would meet each coupling as often as JOINT does in the registered budget, at the cost of matched compute, leaving co-occurrence as the main remaining difference. | X5-3; DES-13; DES-14; decision log, PAPER V3 (docs/decision_log.md:6170-6173: "the experiment that would separate frequency from co-occurrence"); paper/v3/BRIEF.md:508-510 | edited; fix round RN2-4 (2000 now tagged with the DERIVED row X5-3) and RC2-7 ("leaving co-occurrence as the main remaining difference", the ruling's reading of this experiment) |
| 9 | Varying the couplings' strength, with frequency, co-occurrence and the active share fixed, would test whether composition appears where both couplings are strong (§6.1). | paper_v3_prompt.md:211-212; decision log, PAPER V3 (docs/decision_log.md:6134-6137, item 1(3), as relayed) | edited; fix round RC2-7: says what the design would test (composition where both couplings are strong, the siting limitation of §6.1), not that it isolates co-occurrence; RC2-7's "which the test configuration did not offer" left out, so as not to pre-judge the interaction check (RC2-1) |

## Markers left

- `<!-- HOLE:INTERACTION -->` ×1, between the identity half and the future
  work: (b) the check-dependent half of the lesson, labelled post hoc, and (c)
  the one advice sentence, "We suggest, from this one environment, …", never
  after "therefore", "so" or "thus".
- If the results are not back in time (WRITERS §4 item 4, V3Q7), the
  section already reads as the identity lesson without the HOLE. A candidate
  advice sentence that does not depend on the check, for the owner to accept
  or drop (not written into the section): "We suggest, from this one
  environment, that studies comparing joint and isolated training report each
  arm's per-coupling frequency, co-occurrence and active share side by side."
  It is a builder suggestion with no ruling behind it.
- The optional third future-work item (a test point where both couplings are
  active) is not included (V3Q20 default).

## Findings

- **Word budget.** 138 prose words now, against 150; the HOLE's one or two
  sentences will bring it to about 175. Fix round: RC2-7 and RN2-4 (X5-3).
