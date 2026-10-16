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
| 2 | To measure what composition θ\ offered (§6.1), we added a post hoc, evaluation-only check, planned before it ran and outside the confirmatory family (Appendix G). | che/bench/results/phase6/post_v3_interaction/PLAN.md:3-5, :13-26; decision log, PAPER V3 PHASE 1 START (docs/decision_log.md:6218), item 2 | new; fix round RM-1: merged with the old "it stays outside the confirmatory family and changes no registered reading" (the no-reading-change clause now lives in App. G only, which states it); "the test configuration" → θ\* (defined in §6.2) |
| 3 | The final checkpoint of every ISO, JOINT and ISO-4 run is evaluated at θ\ in four conditions, neither coupling, Coupling A only, Coupling B only and both, on the registered evaluation draw with common random numbers (§3.4). | che/bench/results/phase6/post_v3_interaction/PLAN.md:28-39, :52-56, :60-67 (conditions; policies; registered draw; common random numbers); che/tests/test_nesting.py:78-88; DES-13 | new; fix round RM-1: the two sentences on conditions and common random numbers merged; δ = 1.0 moved to the blind list ("holds δ at 1") and App. G |
| 4 | Per policy and co-primary, the post hoc interaction contrast is | che/bench/results/phase6/post_v3_interaction/PLAN.md:76-83 | new; fix round RM-1 ("For each policy" → "Per policy") |
| 5 | Higher $J$ is better, so $I = 0$ means that the couplings' effects add, and $I < 0$ that together they cost more than their separate costs summed. | che/bench/results/phase6/post_v3_interaction/PLAN.md:78-80, :85-87 | new; fix round RM-1 (shortened; sign convention kept) |
| 6 | $I$ is estimated per arm and pooled, with Šidák-corrected intervals over eight tests and a measured evaluation self-floor (Appendix G). | che/bench/results/phase6/post_v3_interaction/PLAN.md:95-110, :117-131; IC row 4 (PENDING-COMMIT) | new; fix round RM-9 ("eight estimates" → "eight tests": 4 estimates × 2 co-primaries) and RM-1 (the self-floor's definition moved to App. G) |
| 7 | Besides being post hoc, the check is blind to several things. | che/bench/results/phase6/post_v3_interaction/PLAN.md:161-163 (§8, "What this analysis is blind to"), :181-183 (item 7, post hoc) | new. HOME of caveat C25 (the full list once); PLAN's item 7 is folded into this opening clause |
| 8 | Holding policies fixed, it cannot say whether training on co-occurrence helps, which Γ tests. | che/bench/results/phase6/post_v3_interaction/PLAN.md:168-170 | new; fix round RM-1 (shortened) |
| 9 | It covers θ\ only, tests additivity only on the scale of rates, where a ceiling can create or hide an interaction, holds δ at 1, tests no difference between arms, and is conditional on the one evaluation draw. | che/bench/results/phase6/post_v3_interaction/PLAN.md:165-167, :171-174, :175-180; COM-6; decision log, PAPER V3 PHASE 1 START (docs/decision_log.md:6234-6235) | new; fix round RC2-5: PLAN §8 item 3's ceiling clause restored ("where a ceiling can create or hide an interaction"); δ tagged COM-6 |
| 10 | The arms also met the four conditions differently in training (Appendix G), so each arm's $I$ also reflects its policies' familiarity with each condition, which pooling averages but does not remove. | che/bench/results/phase6/post_v3_interaction/PLAN.md:184-199 (item 8, including "The pooled reading averages over these differences; it does not remove them") | new; fix round RM-1 (the per-arm training detail moved to App. G) and RC2-5 (the pooled-reading clause from PLAN:198-199 added) |

## Markers left

- `<!-- HOLE:INTERACTION -->` ×2: the result paragraph (b), pooled pair first,
  per PLAN §7; the Figure 9 block. The third HOLE (the row for "eight") was
  removed in the fix round: the orchestrator retagged it IC-4.

## Findings

- **Word budget (fix round, RM-1).** 200 prose words against 200. The
  self-floor's definition, δ = 1.0 and the per-arm training detail moved to
  App. G; PLAN §8 item 3's ceiling clause and item 8's pooled-reading clause
  were restored (RC2-5). The C25 home still lists every PLAN §8 item.
- **"planned before it ran"** is true only if the plan is committed before the
  owner's run: the analysis refuses an uncommitted plan and a run whose first
  `date_utc` is earlier than the plan's commit time
  (`che/scripts/interaction_analysis.py:20-21`, :96-127). For the
  orchestrator (V3Q25).
