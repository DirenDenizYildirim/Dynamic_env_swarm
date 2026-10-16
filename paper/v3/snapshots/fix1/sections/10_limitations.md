<!-- PAPER V3 DRAFT (PAPER V3 ruling, 2026-10-12): builder-drafted, not owner-approved -->

## 7 Limitations and scope

<!-- STUB-SPEC
JOB: Only what §1's three up-front limitations did not carry, as pointers or one line each.
WRITER: W5.
BUDGET: 200 prose words.
FROM: P1 §4.2 §7; P3 §2.2 and §1.4; READS RULING item 4.
ORDER:
  - matched compute, never convergence (one line; DES-13)
  - no theorem says joint training wins (TF:686; HOME)
  - one budget; one held-out point between the training severities (pointer §6.2)
  - the d_p ablation's scope (ENV-2 to ENV-5: 500 updates, 3 seeds, fire only)
  - no heuristic baselines; the task needs no coordination and the agents share parameters (pointer §1)
  - no adaptive curriculum is evaluated (READS RULING item 4)
  - cross-GPU blocks and the δ train/test difference by pointer only (§6.3, §6.2)
ROWS: DES-13, ENV-2, ENV-3, ENV-4, ENV-5, ENV-11.
REGISTERED STRINGS: "at matched compute" (one line).
CAVEATS HOMED HERE (state each in full, once; the detection pattern, from checks/caveats.yaml, must match your home sentence):
  C38 no_theorem_joint_wins: No theorem says joint training wins. Pattern: (?i)\bno theorem\b
SHORT FORMS ALLOWED HERE (at most one sentence each; the full statement is at the home):
  C11 matched_compute_never_convergence (home 06_example_design.md)
EVERY OTHER CAVEAT in checks/caveats.yaml: pointer only ("§6.3", "Appendix D"), never restated. C26: any sentence about the interaction check carries "post hoc".
NOT HERE: anything §1 already states (sited where composition is weak; the inert label; one algorithm, one map, 12 agents) beyond a pointer; the word "mismatch" (home §6.2); secondary intervals not family-corrected (home §6.3); dates; Proposition 4.
V2 MATERIAL: paper/v2/sections/10_limitations.md.
DEPENDENCIES: §1 (W1) carries the three up-front limitations.
-->

§1 lists the largest limitations first, and each sits where it arises: how much composition the test configuration offered, and what the post hoc interaction check measured there (§6.1, §6.4); the coarse and unevenly applied inert label for communication denial (§4.4); the communication setting that differs between training and test for two arms (§6.2); and one learner, one map and one team size (§1).

Every comparison in the worked example is at matched compute, 1000<!-- N:DES-13 --> updates per run, and says nothing about other budgets (§6.2). No theorem in this paper says that joint training should win; the hypothesis the worked example tests is empirical. The test configuration is one held-out severity between the two training severities (§6.2). The hazard is simple, with one ignition at reset, a one-step burn and no wind or uneven fuel (§3.1). The only ablation of the death price is narrow, with three seeds<!-- N:ENV-2 -->, 500<!-- N:ENV-2 --> updates and the fire as the only hazard (§3.3). The task needs no coordination, the agents share one set of parameters, and no heuristic or scripted baseline is reported (§1). We compare fixed training distributions and evaluate no adaptive curriculum. Comparisons across GPUs are marked where they occur (§6.3).
