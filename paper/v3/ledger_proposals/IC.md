# Ledger proposals — the interaction check (orchestrator, Paper v3, 2026-10-14; amended 2026-10-17)

Rows for the post hoc interaction check at θ\* (PAPER V3 item 2(a); scope θ\*
only, PAPER V3 PHASE 1 START item 2; amended before any run, PLAN AMENDMENT,
2026-10-17). Row format as `paper/v2/ledger_supplement.md`. `PLAN` =
`che/bench/results/phase6/post_v3_interaction/PLAN.md`, read at the lines
given.

**Status.** IC-1 to IC-6 are DESIGN rows, read from the **amended** plan,
committed at `ab50d53` (decision log: *PLAN AMENDMENT*). They are VERIFIED
against that commit. The values IC-1, IC-2 and IC-6 changed with the
amendment (the fifth condition); the plan *PLAN OK* approved (sha256
`c3ec2dd1…`, committed at `415b784`) gave 656, 36 and 692 at its lines 68-71.
The owner's OK of the amended text is still owed (*PLAN AMENDMENT* item 7);
if the text changes, these rows are re-read. RESULT rows (IC-7 onward) are
written only after step 0.5: the results returned, their hashes verified, the
analysis run once, and the report committed. Every IC number is post hoc and
outside every registered family.

| ID | value | what | source | status / note |
|---|---|---|---|---|
| IC-1 | 820 | main evaluations: 164 policies (ISO 72, JOINT 72, ISO-4 20) × 5 conditions | PLAN:78 (read: "164 policies × 5 conditions = **820**") | VERIFIED. DERIVED arithmetic: (72 + 72 + 20) × 5 = 820. Was 656 (× 4) before the amendment |
| IC-2 | 45 | floor evaluations: 3 checkpoints × 5 conditions × 3 extra copies | PLAN:79-80 (read: "each condition repeated 3 more times: 3 × 5 × 3 = **45**") | VERIFIED. 3 × 5 × 3 = 45. Was 36 before the amendment |
| IC-3 | three; four | extra evaluations per (checkpoint, condition) in the floor block; copies per (checkpoint, condition) with the main eval | PLAN:151-153 (read: "evaluated three more times on the same card. Together with the main eval, that gives four copies per (checkpoint, condition)") | VERIFIED |
| IC-4 | eight | each family's size: 4 estimates (ISO, JOINT, ISO-4, pooled) × 2 co-primaries; two separate families, one for I and one for D | PLAN:125-129 (read: "two separate families of 8 intervals"; "4 estimates (ISO, JOINT, ISO-4, pooled) × 2 co-primaries of I = 8 intervals"; "the same 4 estimates × 2 co-primaries of D = 8 intervals") | VERIFIED. 4 × 2 = 8, per family |
| IC-5 | 2.73 (2.7270 unrounded) | the two-sided Šidák z at m = 8, family α 0.05, the same for both families | PLAN:131 (read: "α' = 1 − 0.95^(1/8), with two-sided z_α' (≈ 2.73)"); implemented as `_sidak_z(M_FAMILY)` in `che/scripts/interaction_analysis.py:80`, asserted by `che/tests/test_interaction_check.py::test_analysis_family_mirrors_the_plan` | VERIFIED. DERIVED: α' = 1 − 0.95^(1/8) = 0.0063912; z = Φ⁻¹(1 − α'/2) = 2.7270 |
| IC-6 | 865 | total evaluations (main + floor) | PLAN:81 (read: "**Total: 865 evals.**") | VERIFIED. 820 + 45 = 865. Was 692 before the amendment |
