<!-- PAPER V3 DRAFT (PAPER V3 ruling, 2026-10-12): builder-drafted, not owner-approved -->

### G The interaction check in full

<!-- STUB-SPEC
JOB: The interaction check's full record: what was planned and fixed before the run (PLAN.md, by section, not reproduced), the floors and the cross-GPU check, the per-arm and pooled table, the main effects (descriptive), and realized cost.
WRITER: W5.
BUDGET: about 400 prose words plus tables.
FROM: P1 §6.1 G; PLAN.md §2 to §9.
ROWS: IC-* only (orchestrator, from the committed step-0.5 report).
REGISTERED STRINGS: none; label "post hoc"; the PLAN's "observed-SE MDE80" is a detection limit, not a bound.
EVERY OTHER CAVEAT in checks/caveats.yaml: pointer only ("§6.3", "Appendix D"), never restated. C26: any sentence about the interaction check carries "post hoc".
HOLES:
  - everything numeric; the tables; the realized GPU-hours (from the run's timings.txt, never the estimate).
NOT HERE: a cross-arm test; Low or High; the estimate of 1.7 to 2.7 GPU-hours as if realized.
V2 MATERIAL: none.
DEPENDENCIES: step 0.5 results and their commit; §6.4 points here.
-->

The interaction check of §6.4 is post hoc. It was proposed after the registered result was known and was fixed in a written analysis plan before any of its evaluations ran. The analysis script refuses to run unless that plan is committed and unchanged and its hash matches the one the evaluation run recorded, so a later edit to the plan shows as a refusal. The check never joins the confirmatory family and changes no registered reading.

Each condition is θ\* with only $\kappa_A$ and $\kappa_B$ changed: neither coupling (both 0), Coupling A only ($\kappa_A = 0.06$<!-- N:CA-1 -->, $\kappa_B = 0$), Coupling B only ($\kappa_A = 0$, $\kappa_B = 1.0$<!-- N:CB-1 -->), and both, which is θ\* itself. β = 0.49<!-- N:CAL-3 -->, δ = 1.0<!-- N:COM-6 --> and every other fixed value stay at θ\*'s. The three new configurations are generated from θ\*'s file, and a test asserts that each loads to θ\* with exactly its κ values replaced.

The policies are the final checkpoints, at update 1000<!-- N:DES-13 -->, of every ISO and JOINT run (72 seeds each<!-- N:DES-3 -->) and every ISO-4 run (20 seeds<!-- N:DES-13 -->), each archive verified against its recorded sha256 before use. Each policy is evaluated in each condition on the registered draw, 512 episodes from evaluation seed 0<!-- N:DES-13 -->, with actions sampled as trained. Because every condition uses the same seed, each policy meets the same initial states and random streams in all four, and the conditions differ only through the couplings. That gives 656<!-- N:IC-1 --> main evaluations and 36<!-- N:IC-2 --> more for the self-floor.

For policy $i$, $J_i(c)$ is its mean completion or survival over the episodes in condition $c$, and $I_i$ is the contrast displayed in §6.4. An arm's estimate is the mean of $I_i$ over its seeds, with the standard error from their spread, which carries both seed and episode-sampling variation. The pooled estimate weights each arm by its number of seeds and does not assume that the arms share one $I$. The family is three arms and the pool on two co-primaries, eight<!-- N:IC-4 --> intervals, Šidák-corrected (z ≈ 2.73<!-- N:IC-5 -->); the intervals are normal, as for the study's other contrasts. Each estimate's detection limit is its 80 %-power MDE from the observed standard error<!-- N:METH-7 -->. Differences in $I$ between arms are reported without a test. Outside the family and with no reading rule, the report also gives each arm's four condition means and the main effects $J(\text{A only}) - J(\text{neither})$ and $J(\text{B only}) - J(\text{neither})$, which show whether each coupling alone moves the trained policies at θ\*.

For the first-seed checkpoint of each arm, every condition is evaluated three<!-- N:IC-3 --> more times on the run's GPU, so each checkpoint and condition has four<!-- N:IC-3 --> copies. The analysis reports whether the copies are bit-identical, their spread per metric and the spread of $I$ across copies. Each condition is floored separately: the earlier finding that evaluations at θ\* reproduce exactly on one GPU (§8) is not assumed for the other conditions. If any copy differs, a detectable reading also needs the estimate to exceed, in absolute value, twice the largest floor spread of $I$, the post hoc two-sigma floor-grading convention. The "both" evaluation of every policy is also compared with the main runs' own evaluation of the same checkpoint at θ\*.

An estimate shows a detectable interaction if its Šidák interval excludes zero and the floor check is met; its sign and size are then reported, for survival also in agents per episode (× 12<!-- N:ENV-6 -->). Otherwise it is an exclusion with its bound: $\lvert I\rvert < B$ at the family-corrected level, where $B$ is the larger absolute end of the interval, with the detection limit beside it. The pooled pair is the headline; the arm rows say whether the answer depends on how the policies were trained. If the floor or the comparison with the main runs cannot be computed, the analysis refuses rather than report part of the family. What the check is blind to is listed once, in §6.4.

<!-- HOLE:INTERACTION -->
<!-- orchestrator 2026-10-14: the design numbers above are tagged IC-1 to IC-5 (ledger_proposals/IC.md, PENDING-COMMIT until PLAN.md is committed) -->

<!-- HOLE:INTERACTION -->
<!-- fills: per-arm and pooled table; floors; cross-GPU identical count; main effects; realized GPU-hours (IC rows) -->
