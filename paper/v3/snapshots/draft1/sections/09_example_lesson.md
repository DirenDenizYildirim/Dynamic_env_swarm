<!-- PAPER V3 DRAFT (PAPER V3 ruling, 2026-10-12): builder-drafted, not owner-approved -->

### 6.5 What the example teaches

<!-- STUB-SPEC
JOB: The lesson (V3-F4; PROF 3; BLIND W2): by the identity, matching the active share alone cannot isolate co-occurrence, and no design in this study isolates it; the check-dependent half of the lesson; one labelled advice sentence; future work.
WRITER: W5.
BUDGET: 150 prose words.
FROM: P1 §5.2 and §3.3; P3 §3.1 point (3); V3-F4; PAPER V3 item 4.
ORDER:
  - (a) the identity half (write now; HOME of "cannot isolate co-occurrence"): by the identity of §6.2 (point, do not restate it), matching the active share moves per-coupling frequency, so it cannot isolate co-occurrence; the three designs side by side: the sweep fixes frequency and moves the fire-only share (DES-9, SEC-5); the correction fixes the active share and moves frequency (point to §6.3, do not say "twice as often"); the plane fixes the fire-only share and moves frequency with p. None isolates co-occurrence.
  - (b) the check-dependent half (HOLE): one or two sentences from the matching row of P1 §3.3, labelled post hoc.
  - (c) advice, if any: one sentence of its own, labelled "We suggest, from this one environment, …"; never after therefore, so or thus; not a contribution.
  - (d) future work: ISO-4 trained for 2000 updates, which would match each coupling's exposure count to JOINT's but gives up matched compute (PAPER V3 item 4; no run authorized); varying coupling strength instead of frequency. A third item (a test point where both couplings are active) only if the owner adds it (V3Q20).
ROWS: DES-9, DES-14 (pointer), SEC-5, X4-1 (pointer), IC-* (for the HOLE).
REGISTERED STRINGS: none required; "non-verdict-bearing" is not repeated here.
CAVEATS HOMED HERE (state each in full, once; the detection pattern, from checks/caveats.yaml, must match your home sentence):
  C27 cannot_isolate_co_occurrence: Matching the active share alone cannot isolate co-occurrence; no design here isolates it (the lesson, never after "therefore"). Pattern: (?i)\bisolat\w* co-occurrence\b
SHORT FORMS ALLOWED HERE (at most one sentence each; the full statement is at the home):
  C08 active_share_identity (home 06_example_design.md)
  C11 matched_compute_never_convergence (home 06_example_design.md)
EVERY OTHER CAVEAT in checks/caveats.yaml: pointer only ("§6.3", "Appendix D"), never restated. C26: any sentence about the interaction check carries "post hoc".
HOLES:
  - (b) the check-dependent lesson
  - (c) the advice sentence's content, which depends on (b)
NOT HERE: "match the active share" as advice (by the identity it un-matches frequency); "the plane separates co-occurrence from frequency"; "therefore"; "twice as often" (home §6.3); the identity restated in full (home §6.2); any claim about Low, High or training effects from the check.
V2 MATERIAL: paper/v2/sections/09_compositional_test.md §9.3 (replaced, not reused).
DEPENDENCIES: §6.2 (identity), §6.3 (Γ₄'s limits), §6.4 (the check); the abstract's lesson (W1) must match (b) and (c).
-->

By the identity of §6.2, holding the active share fixed while co-occurrence changes forces per-coupling frequency to change with it, so matching the active share alone cannot isolate co-occurrence. None of the study's designs isolates it. The sweep holds each coupling's frequency fixed and moves the fire-only share with co-occurrence. The inert-share correction holds the active share fixed and moves frequency along with co-occurrence (§6.3). The plane's co-occurrence slope holds the fire-only share fixed and moves frequency with co-occurrence.

<!-- HOLE:INTERACTION -->
<!-- fills: (b) the check-dependent half of the lesson, labelled post hoc; (c) the labelled advice sentence -->

Two designs would come closer. ISO-4 trained for 2000<!-- N:DES-13 --><!-- N:DES-14 --> updates would meet each coupling as often as JOINT does in the registered budget, at the cost of matched compute. Varying the couplings' strength instead of how often each is on would change what the couplings do while frequency, co-occurrence and the active share stay fixed.
