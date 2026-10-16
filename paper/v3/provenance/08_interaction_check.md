# Provenance: sections/08_interaction_check.md

Writer: W5 (Paper v3, step 4.1, 2026-10-14). Checked against the section with
`paper/v3/src/provenance_check.py --strict`. `PLAN` =
`che/bench/results/phase6/post_v3_interaction/PLAN.md` (read in full; written
2026-10-14 before any run; **uncommitted** while the owner's commit ban holds,
log:6236-6243). `log` = `docs/decision_log.md`. The section is new in v3 (no v2
material); every row's change column reads "new".
**Amended 2026-10-17** (decision log: *PLAN AMENDMENT*, docs/decision_log.md:6436). The plan was amended before any run, and every `PLAN.md` line below is the amended plan's. Rows whose sentence changed say so in the last column.

| # | sentence (verbatim) | support | change from v2, and why |
|---|---|---|---|
| 1 | 6.4 A post hoc interaction check | framing; che/bench/results/phase6/post_v3_interaction/PLAN.md:1 ("analysis plan (POST HOC)"); decision log, PAPER V3 (docs/decision_log.md:6115), item 2(a) | new (heading as the stub fixes it, STRUCTURE §2) |
| 2 | To measure what composition θ\ offered (§6.1), we added a post hoc, evaluation-only check, planned before it ran and outside the confirmatory family (Appendix G). | che/bench/results/phase6/post_v3_interaction/PLAN.md:3-7, :19-25; decision log, PAPER V3 PHASE 1 START (docs/decision_log.md:6218), item 2 | new; fix round RM-1. Support re-pointed to the amended plan's lines |
| 3 | The final checkpoint of every ISO, JOINT and ISO-4 run is evaluated at θ\ in four conditions, neither coupling, Coupling A only, Coupling B only and both, on the registered evaluation draw with common random numbers (§3.4). | che/bench/results/phase6/post_v3_interaction/PLAN.md:36-48, :62-69, :70-77 (the four interaction conditions; policies; registered draw; common random numbers); che/tests/test_nesting.py:78-88 | new. Support re-pointed to the amended plan's lines |
| 4 | Per policy and co-primary, the post hoc interaction contrast is | che/bench/results/phase6/post_v3_interaction/PLAN.md:88-93 | new; fix round RM-1. Support re-pointed |
| 5 | Higher $J$ is better, so $I = 0$ means that the couplings' effects add, and $I < 0$ that together they cost more than their separate costs summed. | che/bench/results/phase6/post_v3_interaction/PLAN.md:93-97 | new; fix round RM-1. Support re-pointed |
| 6 | A fifth condition, θ\ with the links intact (δ = 0), gives a second post hoc contrast, $D = J(\text{links intact}) - J(\text{both})$, the effect of opening the links with both couplings on (§6.2). | che/bench/results/phase6/post_v3_interaction/PLAN.md:31-34 (the second question), :49 (the condition), :98-104 (D and its sign); che/configs/interaction_links_open.yaml:1; decision log, PLAN AMENDMENT (docs/decision_log.md:6436), item 4 | new, amended 2026-10-17 (PLAN AMENDMENT, before any run): the links-intact condition and D. "Links intact" follows §6.2 and App. G (δ = 0); PLAN and the config call it "links open" |
| 7 | $I$ and $D$ are each estimated per arm and pooled, with Šidák-corrected intervals over eight tests each and a measured evaluation self-floor (Appendix G). | che/bench/results/phase6/post_v3_interaction/PLAN.md:115-134 (per arm, pooled, two families of 8), :150-164 (self-floor); IC-4; che/scripts/interaction_analysis.py:78-80 | amended 2026-10-17 (PLAN AMENDMENT, before any run): "$I$ is estimated … over eight tests" → "$I$ and $D$ are each estimated … over eight tests each" (two families of 8) |
| 8 | Besides being post hoc, the check is blind to several things. | che/bench/results/phase6/post_v3_interaction/PLAN.md:207-209 (§8, "What this analysis is blind to"), :229-232 (item 7, post hoc) | new. HOME of caveat C25 (the full list once). Support re-pointed |
| 9 | Holding policies fixed, it cannot say whether training on co-occurrence helps, which Γ tests. | che/bench/results/phase6/post_v3_interaction/PLAN.md:214-216 | new; fix round RM-1. Support re-pointed |
| 10 | It covers θ\ only, tests additivity only on the scale of rates, where a ceiling can create or hide an interaction, holds δ at 1 except in the fifth condition, tests no difference between arms, and is conditional on the one evaluation draw. | che/bench/results/phase6/post_v3_interaction/PLAN.md:211-213, :217-220, :221-222, :223-226, :227-228; COM-6; decision log, PAPER V3 PHASE 1 START (docs/decision_log.md:6234-6235) | new; fix round RC2-5; amended 2026-10-17 (PLAN AMENDMENT, before any run): "holds δ at 1" → "holds δ at 1 except in the fifth condition" (PLAN §8 item 5) |
| 11 | The arms also met the five conditions differently in training (Appendix G), so each arm's $I$ and $D$ also reflect its policies' familiarity with each condition, which pooling averages but does not remove. | che/bench/results/phase6/post_v3_interaction/PLAN.md:233-252 (item 8, including "The pooled reading averages over these differences; it does not remove them") | new; fix round RM-1; amended 2026-10-17 (PLAN AMENDMENT, before any run): "four conditions" → "five"; "each arm's $I$ also reflects" → "each arm's $I$ and $D$ also reflect" |

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

- **PLAN AMENDMENT (2026-10-17).** The table was regenerated from the section's own sentence split (`provenance_check.section_units`), with every PLAN line re-pointed to the amended plan. The links-intact condition, D, the headline and context rules, the logit view, verification and timestamps are new or changed sentences.
