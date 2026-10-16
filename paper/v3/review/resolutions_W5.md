# Resolutions — writer W5 (Paper v3, step 4.3 fix round, 2026-10-14)

Every finding in RC1, RC2, RN1, RN2 and RM that touches W5's files:
`sections/08_interaction_check.md`, `09_example_lesson.md`, `10_limitations.md`,
`11_using_che.md`, `17_appendix_results.md`, `19_appendix_interaction.md`,
`20_appendix_episodes.md`, `21_appendix_making.md`, their provenance, and
`ledger_proposals/W5.md`. RC1 and RN1 have no finding in these files; their
scope does not include them. Line numbers are of the live section files after
the fix. Every changed sentence has a provenance row noting "fix round: <ID>".

| finding | outcome | what changed (file:line) | reason |
|---|---|---|---|
| RC2-2 (MUST) | FIXED (OWNER-EDITS kept) | 21_appendix_making.md:31, :35 | "The authors made the study's decisions" became "made or ratified". The list no longer names the registered design or the interaction-check plan. A new sentence records delegation: pre-rental design decisions including the outcome-framing ratification (log:3104-3112; PFB:3-4), and later builder-ruled or delegated entries (log:3450, :5961). "Each decision was written … before it was acted on" became "From early in the project, a decision bound only once it was written …; before that rule, some directives existed only in conversation" (log:465-468; log:455-460). A new sentence says the interaction-check plan was written by the assistant and no approval by the authors is yet recorded, with `<!-- OWNER-PENDING:PLAN_OK -->` to change it once the owner's OK is transcribed. The OWNER-EDITS block and `OWNER-PENDING:A1` are kept. |
| RC2-2, "Also for the owner" (tool naming) | OWNER | none (21_appendix_making.md:31 unchanged) | Whether "Claude (Anthropic), used through Claude Code" covers every tool (chat-relayed rulings and reviews; App. I's "LLM-based research assistants") is the owner's call: carried v2 A1, marker `OWNER-PENDING:A1` in place. |
| RC2-4 (MUST), §8 part | FIXED | 11_using_che.md:46 | "the supplement's hash manifest shows that the registration documents are the files this paper describes" became "the hash manifest shows only that the archive arrived unaltered". RC2-4's "not when the documents were written" is implied by "only" and was cut for the page budget (RM-1). |
| RC2-4 (MUST), App. D.1 part | NOT MINE: belongs to W4 | — | 16_appendix_timeline.md:38 is W4's file. |
| RC2-5 (SHOULD) | FIXED | 08_interaction_check.md:45 | PLAN §8 item 3's qualification is restored ("where a ceiling can create or hide an interaction"), and so is item 8's pooled-reading clause ("which pooling averages but does not remove"). The optional item-5 clause was not added (budget); "holds δ at 1" stays in the list. |
| RC2-6 (SHOULD) | FIXED | 19_appendix_interaction.md:28, :30 | "compared with the main runs' own evaluation" became "compared, descriptively, with the original evaluation of the same checkpoint at θ\*, and the report states how many agree on both co-primaries". "the comparison with the main runs" became "the comparison with the original evaluations". |
| RC2-7 (SHOULD) | FIXED, in part | 09_example_lesson.md:36 | "Two designs would come closer" became "Two experiments would go further". The ISO-4 sentence adds "leaving co-occurrence as the main remaining difference", the ruling's reading (log:6170-6173). The strength sentence now says what it would test: "whether composition appears where both couplings are strong (§6.1)". RC2-7's "which the test configuration did not offer" was left out, so as not to pre-judge the post hoc check (RC2-1's concern). |
| RC2-8 (SHOULD) | NOT MINE: belongs to W1 | — | 12_conclusion.md is W1's. §6.5's lesson sentence is unchanged and can be pointed to. |
| RC2-19 (SHOULD) | FIXED, adapted | 11_using_che.md:35 | "against its registry" became "against a registry of the fixed constants (Appendix B)". RC2-19's "configurations and code defaults" was not used: RC1-1 shows `test_locks.py` checks code defaults for four constants only. |
| RN2-4 (SHOULD) | FIXED | 09_example_lesson.md:36; ledger_proposals/W5.md (new row X5-3) | New DERIVED row X5-3: per-coupling frequency ½ (ISO-4) against 1 (JOINT) (DES-14). Episodes per update are equal across arms: 256 envs × 128 steps (DX-3), and episodes end only at the fixed horizon 256 (`che/env/env.py:361`; ENV-6). So 2000 = 2 × 1000 (DES-13). The 2000 in §6.5 is tagged X5-3. |
| RN2-6 (SHOULD) | FIXED | 19_appendix_interaction.md:26 | "as for the study's other contrasts" became "as for the registered contrasts and Γ₄" (the secondary contrasts use bootstrap intervals). |
| RN2 note (IC tags cited while PENDING-COMMIT) | no action | — | Acceptable by design while the `--final` gate stands (RN2's own note). The orchestrator retagged my IC-? tags as IC-1 to IC-5. I removed the two HOLE markers that only waited for those rows (08, 19). |
| RM-1 (MUST) | FIXED for W5's main text | 08 (200 words), 09 (138), 10 (198), 11 (239) | All four are now at or under budget (§6.4 200/200, §6.5 138/150 before its HOLE, §7 198/200, §8 239/240). §6.4: the self-floor's definition, δ = 1.0 and the per-arm training detail moved to App. G (19_appendix_interaction.md:24); the full blind-spot list stays (C25 home). §8 cuts: the step count, the toolchain, the map-size sentence, "under jit and vmap", "so retraining needs a GPU". No registered string, honesty line or caveat home was cut. |
| RM-6 (SHOULD) | FIXED | 11_using_che.md:37 | The commands now read `uv run python -m che.train.ippo` and `uv run python -m che.eval.harness`. |
| RM-7 (SHOULD) | FIXED | 11_using_che.md:39; 19_appendix_interaction.md:20 | §8: "The post hoc interaction check's analysis needs version history, so it does not run there." App. G: "The supplement carries no version history, so the analysis does not run from it (§8)." If the orchestrator adds F2's git-free mode, both sentences change. |
| RM-8 (SHOULD) | NOT MINE: belongs to W1 (flagged) | — | The §1 HOLE sits before the sentence that introduces the check (01_introduction.md:49-52). Either move the marker after that sentence or fold the result into it (also RC1-9). |
| RM-9 (SHOULD) | FIXED | 08_interaction_check.md:37 | "over eight estimates" became "over eight tests" (4 estimates × 2 co-primaries; App. G gives the count). |
| RM-OWNER-1 (OWNER) | OWNER | 11_using_che.md:41-42 (the V3Q16 marker and its comment, updated) | Default kept: §8's contents sentence lists neither the theory document nor the lock records. The `OWNER-PENDING:V3Q16` comment now holds the clause to add ("the theory document and the records of how each fixed constant was measured") if they ship. |
| RM-13, RM-14, RM-15, RM-16 | NOT MINE: supplement builder / orchestrator | — | `paper/v3/supplement/` files, the supplement's selection rule R5 and `che/tests/test_locks.py`; none of my files. |

## Counts

- FIXED: 12 (RC2-2, RC2-4 §8 part, RC2-5, RC2-6, RC2-7 in part, RC2-19 adapted, RN2-4, RN2-6, RM-1, RM-6, RM-7, RM-9).
- OWNER: 2 (RC2-2's tool naming, A1; RM-OWNER-1, V3Q16).
- NOT MINE: RC2-4's D.1 part (W4), RC2-8 (W1), RM-8 (W1, flagged), RM-13 to RM-16 (supplement/orchestrator).
- DECLINED: none. Two fixes leave out part of the proposed wording, with the reasons above (RC2-7's last clause; RC2-19's "code defaults").

## Checks run after the fix

- `provenance_check.py --root paper/v3 --strict` on all eight W5 files: OK (0 unsourced, 0 stale, 0 support problems).
- `v3_checks.py` terms, dates and caveats: all PASS.
