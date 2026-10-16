# Provenance: sections/19_appendix_interaction.md

Writer: W5 (Paper v3, step 4.1, 2026-10-14). Checked with
`paper/v3/src/provenance_check.py --strict`. New in v3 (no v2 material). Every
sentence summarizes `che/bench/results/phase6/post_v3_interaction/PLAN.md`
(read in full; **uncommitted** while the owner's commit ban holds) by section,
without reproducing it. Results do not exist: the tables, floors, the
cross-GPU count, the main effects and the realized GPU-hours are HOLEs.

| # | sentence (verbatim) | support | change from v2, and why |
|---|---|---|---|
| 1 | G The interaction check in full | framing | new (heading as the stub fixes it) |
| 2 | The interaction check of §6.4 is post hoc. | che/bench/results/phase6/post_v3_interaction/PLAN.md:1, :15-17 | new |
| 3 | It was proposed after the registered result was known and was fixed in a written analysis plan before any of its evaluations ran. | che/bench/results/phase6/post_v3_interaction/PLAN.md:3-5 (written 2026-10-14, before any run), :15-16 (proposed after the result was known) | new. True once the plan is committed before the run (see 08's provenance, Findings) |
| 4 | The analysis script refuses to run unless that plan is committed and unchanged and its hash matches the one the evaluation run recorded, so a later edit to the plan shows as a refusal. | che/bench/results/phase6/post_v3_interaction/PLAN.md:7-11; che/scripts/interaction_analysis.py:20-21, :96-127; che/tests/test_interaction_check.py:394-413 | new |
| 5 | The supplement carries no version history, so the analysis does not run from it (§8). | che/scripts/interaction_analysis.py:95-112, :157-167; paper/v3/supplement/README.md (finding F2) | new; fix round RM-7 |
| 6 | The check never joins the confirmatory family and changes no registered reading. | che/bench/results/phase6/post_v3_interaction/PLAN.md:18-21 | new |
| 7 | Each condition is θ\ with only $\kappa_A$ and $\kappa_B$ changed: neither coupling (both 0), Coupling A only ($\kappa_A = 0.06$, $\kappa_B = 0$), Coupling B only ($\kappa_A = 0$, $\kappa_B = 1.0$), and both, which is θ\ itself. | che/bench/results/phase6/post_v3_interaction/PLAN.md:28-39 (§2 conditions table); CA-1 (κ_A 0.06); CB-1 (κ_B 1.0) | new |
| 8 | β = 0.49, δ = 1.0 and every other fixed value stay at θ\'s. | che/bench/results/phase6/post_v3_interaction/PLAN.md:30-32; CAL-3; COM-6 | new |
| 9 | The three new configurations are generated from θ\'s file, and a test asserts that each loads to θ\ with exactly its κ values replaced. | che/bench/results/phase6/post_v3_interaction/PLAN.md:41-44; che/scripts/make_interaction_configs.py:1; che/tests/test_interaction_check.py:46-68 | new |
| 10 | The policies are the final checkpoints, at update 1000, of every ISO and JOINT run (72 seeds each) and every ISO-4 run (20 seeds), each archive verified against its recorded sha256 before use. | che/bench/results/phase6/post_v3_interaction/PLAN.md:52-59 (§3 policies; each archive verified against SHA256_CKPT.txt before extraction); DES-13 (T* = 1000; ISO‑4 k = 20); DES-3 (72 per arm) | new. The seed counts carry the registered rows (DES-3, DES-13), not IC rows: they are the study's arm sizes, and the check uses every final checkpoint |
| 11 | Each policy is evaluated in each condition on the registered draw, 512 episodes from evaluation seed 0, with actions sampled as trained. | che/bench/results/phase6/post_v3_interaction/PLAN.md:60-63 (harness, policy stochastic as trained, 512 episodes, seed 0); DES-13 (the registered draw) | new. 512 and seed 0 carry DES-13 (the registered draw), which the check reuses |
| 12 | Because every condition uses the same seed, each policy meets the same initial states and random streams in all four, and the conditions differ only through the couplings. | che/bench/results/phase6/post_v3_interaction/PLAN.md:64-67 (common random numbers); che/tests/test_nesting.py:78-88 | new |
| 13 | That gives 656 main evaluations and 36 more for the self-floor. | che/bench/results/phase6/post_v3_interaction/PLAN.md:68-70 (164 × 4 = 656; 3 × 4 × 3 = 36) | new. tagged `N:IC-1` and `N:IC-2` (IC.md, PENDING-COMMIT; retagged by the orchestrator 2026-10-14) |
| 14 | The arms met the four conditions differently in training: ISO trained on each coupling alone with links intact and on neither coupling with links denied, ISO-4 only on each coupling alone with links intact, and JOINT only with every stressor on, all at β = 0.43 and 0.70, never at 0.49. | che/bench/results/phase6/post_v3_interaction/PLAN.md:184-196; che/configs/p6_iso.yaml:41-46; che/configs/p6_iso4.yaml:36-39; che/configs/p6_joint.yaml:36-37; X4-2; CAL-3 | new; fix round RM-1: moved here from §6.4 (the blind-spot item stays in §6.4, the detail here) |
| 15 | This is why the arm rows are reported beside the pooled one. | che/bench/results/phase6/post_v3_interaction/PLAN.md:198-199 | new; fix round RM-1 (moved from §6.4's plan) |
| 16 | For policy $i$, $J_i(c)$ is its mean completion or survival over the episodes in condition $c$, and $I_i$ is the contrast displayed in §6.4. | che/bench/results/phase6/post_v3_interaction/PLAN.md:78-83 | new |
| 17 | An arm's estimate is the mean of $I_i$ over its seeds, with the standard error from their spread, which carries both seed and episode-sampling variation. | che/bench/results/phase6/post_v3_interaction/PLAN.md:97-101 (per arm: mean, sd ddof 1, SE = s/√k; seed and episode-sampling variation) | new |
| 18 | The pooled estimate weights each arm by its number of seeds and does not assume that the arms share one $I$. | che/bench/results/phase6/post_v3_interaction/PLAN.md:102-105 (w_a = k_a / 164; does not assume the arms share one I) | new. The pooled SE formula is not printed (App. G stays tight); it is PLAN:103-104 |
| 19 | The family is three arms and the pool on two co-primaries, eight intervals, Šidák-corrected (z ≈ 2.73); the intervals are normal, as for the registered contrasts and Γ₄. | che/bench/results/phase6/post_v3_interaction/PLAN.md:106-110; che/scripts/interaction_analysis.py:62; IC row 4 (PENDING-COMMIT); IC row 5 (PENDING-COMMIT) | edited; fix round RN2-6 ("as for the study's other contrasts" → "as for the registered contrasts and Γ₄": the secondary contrasts use bootstrap intervals) |
| 20 | Each estimate's detection limit is its 80 %-power MDE from the observed standard error. | che/bench/results/phase6/post_v3_interaction/PLAN.md:111-113 (observed-SE MDE80, "a detection limit, not a bound"); METH-7 | new; "detection limit" as defined in §5 (BRIEF §5.2) |
| 21 | Differences in $I$ between arms are reported without a test. | che/bench/results/phase6/post_v3_interaction/PLAN.md:114-115 | new |
| 22 | Outside the family and with no reading rule, the report also gives each arm's four condition means and the main effects $J(\text{A only}) - J(\text{neither})$ and $J(\text{B only}) - J(\text{neither})$, which show whether each coupling alone moves the trained policies at θ\. | che/bench/results/phase6/post_v3_interaction/PLAN.md:88-93 (§4 descriptive: four condition means per arm; main effects A and B per arm, context for I, not tests) | new (BRIEF §5.2: "main effect" defined in App. G) |
| 23 | For the first-seed checkpoint of each arm, every condition is evaluated three more times on the run's GPU, so each checkpoint and condition has four copies. | che/bench/results/phase6/post_v3_interaction/PLAN.md:69-70, :119-122 (iso_s1, joint_s1, iso4_s1; three more copies; four copies); che/scripts/interaction_analysis.py:65 | new. "three" and "four" tagged `N:IC-3` (IC.md, PENDING-COMMIT) |
| 24 | The analysis reports whether the copies are bit-identical, their spread per metric and the spread of $I$ across copies. | che/bench/results/phase6/post_v3_interaction/PLAN.md:122-126 | new |
| 25 | Each condition is floored separately: the earlier finding that evaluations at θ\ reproduce exactly on one GPU (§8) is not assumed for the other conditions. | che/bench/results/phase6/post_v3_interaction/PLAN.md:128-131; HW-2 | new. "θ* evaluations are deterministic on an RTX 5090" (PLAN:129-130) written as "reproduce exactly on one GPU (§8)", the scope HW-2 carries |
| 26 | If any copy differs, a detectable reading also needs the estimate to exceed, in absolute value, twice the largest floor spread of $I$, the post hoc two-sigma floor-grading convention. | che/bench/results/phase6/post_v3_interaction/PLAN.md:132-135 (\|Ī\| > 2 × the largest floor sd of I; "the post-hoc 2-sigma floor-grading convention, labelled as such"); che/scripts/interaction_analysis.py:230-243 | new. Labelled as CLAUDE.md requires for the 2-sigma convention |
| 27 | The "both" evaluation of every policy is also compared, descriptively, with the original evaluation of the same checkpoint at θ\, and the report states how many agree on both co-primaries. | che/bench/results/phase6/post_v3_interaction/PLAN.md:136-141 | edited; fix round RC2-6 ("the main runs' own evaluation" did not fit ISO-4; "descriptively" and the agreement count restored from PLAN) |
| 28 | An estimate shows a detectable interaction if its Šidák interval excludes zero and the floor check is met; its sign and size are then reported, for survival also in agents per episode (× 12). | che/bench/results/phase6/post_v3_interaction/PLAN.md:147-149; ENV-6 (12 agents) | new |
| 29 | Otherwise it is an exclusion with its bound: $\lvert I\rvert < B$ at the family-corrected level, where $B$ is the larger absolute end of the interval, with the detection limit beside it. | che/bench/results/phase6/post_v3_interaction/PLAN.md:150-153 | new. Never "no interaction" or "additive" (PLAN:153) |
| 30 | The pooled pair is the headline; the arm rows say whether the answer depends on how the policies were trained. | che/bench/results/phase6/post_v3_interaction/PLAN.md:154-156 | new |
| 31 | If the floor or the comparison with the original evaluations cannot be computed, the analysis refuses rather than report part of the family. | che/bench/results/phase6/post_v3_interaction/PLAN.md:157-159 | edited; fix round RC2-6 |
| 32 | What the check is blind to is listed in §6.4; the arms' training conditions are given above. | che/bench/results/phase6/post_v3_interaction/PLAN.md:161-199; paper/v3/checks/caveats.yaml (C25 home 08_interaction_check.md) | edited; final pass: RC2-21 (the arms' training conditions now sit in App. G, so "listed once, in §6.4" was false) |

## Markers left

- `<!-- HOLE:INTERACTION -->` ×1 at the end: the per-arm and pooled table (I
  with Šidák interval, bound B and observed-SE MDE80 per co-primary; survival
  also in agents per episode), the floor block, the cross-GPU agreement count
  out of 164, the condition means and main effects per arm, and the realized
  GPU-hours from the run's `timings.txt` (never the 1.7–2.7 GPU-hour
  estimate). The HOLE for the design-number rows was removed in the fix
  round: the orchestrator retagged them IC-1 to IC-5 (PENDING-COMMIT).

## Findings

- **Word count.** About 690 prose words against about 400, before the result
  tables (fix round: RM-7's sentence and the per-arm training detail moved
  here from §6.4 to keep §6.4 at its budget). The appendix is not in the page
  count; the owner may cut the refusal sentence (row 4).
