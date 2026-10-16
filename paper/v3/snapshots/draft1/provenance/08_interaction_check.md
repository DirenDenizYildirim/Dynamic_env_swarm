# Provenance: sections/08_interaction_check.md

Writer: W5 (Paper v3, step 4.1, 2026-10-14). Checked against the section with
`paper/v3/src/provenance_check.py --strict`. `PLAN` =
`che/bench/results/phase6/post_v3_interaction/PLAN.md` (read in full; written
2026-10-14 before any run; **uncommitted** while the owner's commit ban holds,
log:6236-6243). `log` = `docs/decision_log.md`. The section is new in v3 (no v2
material); every row's change column reads "new".

| # | sentence (verbatim) | support | change from v2, and why |
|---|---|---|---|
| 1 | 6.4 A post hoc interaction check | framing; che/bench/results/phase6/post_v3_interaction/PLAN.md:1 ("analysis plan (POST HOC)"); decision log, PAPER V3 (docs/decision_log.md:6115), item 2(a) | new (heading as the stub fixes it, STRUCTURE §2) |
| 2 | To measure what composition the test configuration offered (§6.1), we added a post hoc, evaluation-only check, planned before it ran (Appendix G); it stays outside the confirmatory family and changes no registered reading. | che/bench/results/phase6/post_v3_interaction/PLAN.md:3-5 (written before any run; eval-only; post hoc), :13-26 (§1: post hoc, out of the registered family, changes no reading; its question "does the composition the registered test was about exist, measurably, at the point where it was tested?"); decision log, PAPER V3 PHASE 1 START (docs/decision_log.md:6218), item 2 | new. "planned before it ran" rests on PLAN:3 and on the run recording the plan's hash (PLAN:7-11); the plan is not yet committed, so the claim becomes checkable only once the owner names the branch (V3Q25). The professor's review that proposed the check (PLAN:16) is not named: it is a review, not a ruling (log:6121-6122), and naming review history is not needed |
| 3 | The final checkpoint of every ISO, JOINT and ISO-4 run is evaluated at θ\ in four conditions: neither coupling, Coupling A only, Coupling B only, and both, with δ = 1.0 throughout. | che/bench/results/phase6/post_v3_interaction/PLAN.md:28-39 (§2 conditions table; δ = 1.0 in all four), :52-56 (§3 policies, update 1000 of ISO 1–72, JOINT 1–72, ISO‑4 1–20); COM-6 (δ = 1.0); che/configs/interaction_neither.yaml; che/tests/test_interaction_check.py:46-68 | new. Seed counts are not repeated here (they sit in §6.2 and App. G with DES rows) |
| 4 | Switching a coupling off gives the exact nested model (§3.4), so the four conditions share the registered evaluation draw's initial states and random streams. | che/bench/results/phase6/post_v3_interaction/PLAN.md:46-48 (κ = 0 is the nested model, bitwise, given the same keys), :60-67 (registered draw; common random numbers: same eval seed, same 512 initial states and streams); che/tests/test_nesting.py:78-88; DES-13 (the registered draw) | new |
| 5 | For each policy and co-primary, the post hoc interaction contrast is | che/bench/results/phase6/post_v3_interaction/PLAN.md:76-83 (§4 estimand, per policy and co-primary; the display that follows is PLAN:83 in the paper's notation) | new. The display (ignored by the checker) is I = J(both) − J(A only) − J(B only) + J(neither), PLAN:83 |
| 6 | $J$ is a rate where higher is better, so $I = 0$ means that the couplings' effects add, and $I < 0$ that together they cost more than the sum of their separate costs. | che/bench/results/phase6/post_v3_interaction/PLAN.md:78-80 (J is the metric's mean over the 512 episodes), :85-87 (I = 0: the effects add; I < 0: worse under both than the sum of separate effects predicts) | new. Sign convention stated once (BRIEF §5.2 glossary row "interaction contrast I"); PLAN:87's "I > 0" case is left to App. G's reading rules to save words |
| 7 | $I$ is estimated for each arm and pooled over the arms, with Šidák-corrected intervals over eight estimates, beside an evaluation self-floor: the spread of repeated evaluations of one checkpoint in one condition on the check's GPU. | che/bench/results/phase6/post_v3_interaction/PLAN.md:95-110 (§5 per arm, pooled by seed count, family of 4 × 2 = 8 Šidák intervals), :117-131 (§6 eval self-floor, A-vs-A on the run's card); che/scripts/interaction_analysis.py:62, :65 | new. "eight" is tagged `N:IC-4` (IC.md, PENDING-COMMIT; retagged by the orchestrator 2026-10-14); "evaluation self-floor" defined here (BRIEF §5.2) |
| 8 | Besides being post hoc, the check is blind to several things. | che/bench/results/phase6/post_v3_interaction/PLAN.md:161-163 (§8, "What this analysis is blind to"), :181-183 (item 7, post hoc) | new. HOME of caveat C25 (the full list once); PLAN's item 7 is folded into this opening clause |
| 9 | With the policies fixed, it cannot say whether training on co-occurring couplings helps, which is what Γ tests. | che/bench/results/phase6/post_v3_interaction/PLAN.md:168-170 (item 2: fixed policies; "That is Γ, the registered test") | new |
| 10 | It covers θ\ only, tests additivity only on the scale of rates, holds δ at 1, tests no difference between arms, and is conditional on the one evaluation draw. | che/bench/results/phase6/post_v3_interaction/PLAN.md:165-167 (item 1, θ\* only), :171-174 (item 3, the additive scale), :175-178 (items 4 and 5, one draw; δ = 1.0 fixed), :179-180 (item 6, not a cross-arm test); decision log, PAPER V3 PHASE 1 START (docs/decision_log.md:6234-6235: Low and High not run) | new. Item 3's ceiling clause ("ceiling and floor effects ... can create or hide an additive interaction", PLAN:173-174) was cut for the budget; restore if the owner wants it. C12's short form (one evaluation draw) is used once, as allowed here |
| 11 | The arms also met the four conditions differently in training: ISO saw each coupling alone with links intact and neither coupling with links denied, ISO-4 never saw links denied, and JOINT saw only every stressor on, all at β 0.43 and 0.70, never at 0.49. | che/bench/results/phase6/post_v3_interaction/PLAN.md:184-196 (item 8); che/configs/p6_iso.yaml:41-46; che/configs/p6_iso4.yaml:36-39; che/configs/p6_joint.yaml:36-37; X4-2; CAL-3 | new. "neither coupling with links denied" = ISO's two δ-only components (κ_A = κ_B = 0, δ = 1, p6_iso.yaml:43, :46), which have the "neither" condition's couplings (PLAN:189-190) |
| 12 | Each arm's $I$ therefore also reflects how familiar its policies are with each condition. | che/bench/results/phase6/post_v3_interaction/PLAN.md:185-187 ("Each arm's I mixes how the environment combines the couplings with how familiar that arm's policies are with each condition"), :198-199 | new. PLAN:198-199's "why the per-arm rows are reported beside the pooled one" is left to the result paragraph (HOLE) |

## Markers left

- `<!-- HOLE:INTERACTION -->` ×3: the IC row for "eight" (now tagged IC-4; the marker
  can go once IC-4 is VERIFIED); the result paragraph (b), pooled pair first, per PLAN §7; the
  Figure 9 block.
- RESOLVED (orchestrator, 2026-10-14): the `N:IC-?` tag on "eight" is now
  `N:IC-4` (`ledger_proposals/IC.md`, PENDING-COMMIT until PLAN.md is
  committed). The build passes; `--final` fails while the row is PENDING.

## Findings

- **Word budget.** 278 prose words against 200 (+39 %). The stub requires the
  design, the sign convention, the self-floor's definition and all eight of
  PLAN §8's blind spots in this section (C25 home); the list alone is about
  110 words. Cutting further means dropping blind-spot items, which the
  stub forbids. The owner may move the design paragraph to App. G and keep
  only the first sentence and the list here (about 170 words).
- **"planned before it ran"** is true only if the plan is committed before the
  owner's run, which the analysis script enforces: it refuses an uncommitted
  plan and a run whose first `date_utc` is earlier than the plan's commit time
  (`che/scripts/interaction_analysis.py:20-21`, :96-127). If the commit ban
  still holds when the owner runs the job, the analysis will refuse that run.
  For the orchestrator (V3Q25).
