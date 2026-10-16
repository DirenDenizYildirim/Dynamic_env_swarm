<!-- PAPER V3 DRAFT (PAPER V3 ruling, 2026-10-12): builder-drafted, not owner-approved -->

### 6.4 A post hoc interaction check

<!-- STUB-SPEC
JOB: Report the post hoc, evaluation-only interaction check at θ* (V3-E1): what it is, its label, its result under PLAN §7's reading rules, and what it is blind to (the one home of that list). It measures the central limitation of §6.1; it changes no registered reading.
WRITER: W5.
BUDGET: 200 prose words; Figure 9 caption at most 60 words.
FROM: P1 §3.3; P2 §4; PLAN.md §1 to §8; V3-E1.
ORDER:
  - (a) what it is (writable now, with HOLEs for numbers that need IC rows): post hoc and evaluation-only, proposed after the result was known, planned and fixed before its run, outside the registered family; at θ* only; four conditions (neither coupling, Coupling A only, Coupling B only, both), each θ* with κ_A and/or κ_B set to 0 and δ = 1 throughout; the final checkpoints of ISO, JOINT and ISO-4 (DES-3, DES-13); the registered evaluation draw with common random numbers; I = J(both) − J(A only) − J(B only) + J(neither) per policy, sign convention once (I < 0: together they cost more than the sum); per arm and pooled, Šidák-corrected over the family of estimates (count from an IC row); an evaluation self-floor on the run GPU.
  - (b) the result (HOLE): the pooled pair first, per PLAN §7: either a detectable interaction with its sign and size (survival also in agents per episode), or an exclusion "|I| below B points at the family-corrected level" with the detection limit beside it; per-arm rows say whether the answer depends on how the policy was trained; cross-arm differences descriptive only. Figure 9.
  - (c) what it is blind to (HOME, the full list once; use the phrase "blind to"): θ* only (Low and High were not run); fixed policies, so it says nothing about whether training on co-occurrence helps (that is Γ); additivity on the scale of bounded rates; one evaluation draw; δ held at 1; not a cross-arm test; post hoc; the arms met the four conditions differently in training (ISO trained on A-only and B-only at δ = 0, ISO-4 never at δ = 1, JOINT only with every stressor on; all at β 0.43 and 0.70, never 0.49).
ROWS: DES-3, DES-13, CAL-3; IC-* (orchestrator, from the committed step-0.5 report: the number of evaluations, Šidák m and z, per-arm and pooled I with interval ends, MDE80s, self-floor results, the cross-GPU identical count, realized GPU-hours).
FIGURES: Figure 9, the new interaction-check figure (P2 §4: per arm a 2 × 2 condition panel; a forest plot of I by arm and pooled with per-seed points, intervals and the self-floor band; a "post hoc" mark, no verdict mark). It does not exist yet: a figure builder makes it from the committed outputs after step 0.5 (STRUCTURE §4). Caption: what it shows, and the words "post hoc" (V3Q13).
REGISTERED STRINGS: none (the check is not registered). Its label: "post hoc" wherever it appears.
CAVEATS HOMED HERE (state each in full, once; the detection pattern, from checks/caveats.yaml, must match your home sentence):
  C25 interaction_blind_to: What the interaction check is blind to (θ* only; fixed policies; additive scale; one draw; δ held at 1; no cross-arm test; post hoc; arms' training conditions differ). The full list once. Pattern: (?i)\bblind to\b
SHORT FORMS ALLOWED HERE (at most one sentence each; the full statement is at the home):
  C12 one_evaluation_draw (home 06_example_design.md)
EVERY OTHER CAVEAT in checks/caveats.yaml: pointer only ("§6.3", "Appendix D"), never restated. C26: any sentence about the interaction check carries "post hoc".
HOLES:
  - every number in (a) that has no row yet (IC rows)
  - the result paragraph (b)
  - Figure 9 block (with its measured iframe height)
NOT HERE: "pre-check" as if registered; "no interaction" or "additive" (it is an exclusion with its bound); any verdict word (REJECT, null) for I; any cross-arm test; Low or High; any statement about training effects or about δ; the professor's review as authority.
V2 MATERIAL: none (new).
DEPENDENCIES: IC rows (orchestrator, step 0.5); §6.1 points here; §6.5 (W5) and the abstract (W1) use its reading; Appendix G (W5) holds the full tables.
-->

To measure what composition the test configuration offered (§6.1), we added a post hoc, evaluation-only check, planned before it ran (Appendix G); it stays outside the confirmatory family and changes no registered reading.

The final checkpoint of every ISO, JOINT and ISO-4 run is evaluated at θ\* in four conditions: neither coupling, Coupling A only, Coupling B only, and both, with δ = 1.0<!-- N:COM-6 --> throughout. Switching a coupling off gives the exact nested model (§3.4), so the four conditions share the registered evaluation draw's initial states and random streams. For each policy and co-primary, the post hoc interaction contrast is

$$
I = J(\text{both}) - J(\text{A only}) - J(\text{B only}) + J(\text{neither}).
$$

$J$ is a rate where higher is better, so $I = 0$ means that the couplings' effects add, and $I < 0$ that together they cost more than the sum of their separate costs. $I$ is estimated for each arm and pooled over the arms, with Šidák-corrected intervals over eight<!-- N:IC-4 --> estimates, beside an evaluation self-floor: the spread of repeated evaluations of one checkpoint in one condition on the check's GPU.

<!-- HOLE:INTERACTION -->
<!-- orchestrator 2026-10-14: "eight" is now tagged IC-4 (ledger_proposals/IC.md, PENDING-COMMIT until PLAN.md is committed) -->

<!-- HOLE:INTERACTION -->
<!-- fills: (b) the result paragraph, pooled pair first, per PLAN §7 -->

<!-- HOLE:INTERACTION -->
<!-- fills: Figure 9 block: the interaction figure (iframe and print companion), built after step 0.5 -->

Besides being post hoc, the check is blind to several things. With the policies fixed, it cannot say whether training on co-occurring couplings helps, which is what Γ tests. It covers θ\* only, tests additivity only on the scale of rates, holds δ at 1, tests no difference between arms, and is conditional on the one evaluation draw. The arms also met the four conditions differently in training: ISO saw each coupling alone with links intact and neither coupling with links denied, ISO-4 never saw links denied, and JOINT saw only every stressor on, all at β 0.43 and 0.70<!-- N:CAL-3 -->, never at 0.49<!-- N:CAL-3 -->. Each arm's $I$ therefore also reflects how familiar its policies are with each condition.
