# Ledger proposals — the interaction check (orchestrator, Paper v3, 2026-10-14)

Rows for the post hoc interaction check at θ\* (PAPER V3 item 2(a); scope θ\*
only, PAPER V3 PHASE 1 START item 2). Row format as
`paper/v2/ledger_supplement.md`. `PLAN` =
`che/bench/results/phase6/post_v3_interaction/PLAN.md`, read by the
orchestrator this session at the lines given.

**Status.** IC-1 to IC-6 are DESIGN rows. Their source, PLAN, is written but
**not yet committed** (the owner's commit ban, PAPER V3 PHASE 1 START item 3),
so each is PENDING-COMMIT. They become VERIFIED once PLAN is committed
unchanged. RESULT rows (IC-7 onward) are written only after step 0.5: the
results returned, their hashes verified, the analysis run once, and the report
committed. Every IC number is post hoc and outside every registered family.

| ID | value | what | source | status / note |
|---|---|---|---|---|
| IC-1 | 656 | main evaluations: 164 policies (ISO 72, JOINT 72, ISO-4 20) × 4 conditions | PLAN:68 (read: "164 policies × 4 conditions = **656**") | PENDING-COMMIT. DERIVED arithmetic: (72 + 72 + 20) × 4 = 656 |
| IC-2 | 36 | floor evaluations: 3 checkpoints × 4 conditions × 3 extra copies | PLAN:69-70 (read: "each condition repeated 3 more times: 3 × 4 × 3 = **36**") | PENDING-COMMIT. 3 × 4 × 3 = 36 |
| IC-3 | three; four | extra evaluations per (checkpoint, condition) in the floor block; copies per (checkpoint, condition) with the main eval | PLAN:120-121 (read: "evaluated three more times … that gives four copies per (checkpoint, condition)") | PENDING-COMMIT |
| IC-4 | eight | the family: 4 estimates (ISO, JOINT, ISO-4, pooled) × 2 co-primaries | PLAN:106-107 (read: "4 estimates (ISO, JOINT, ISO-4, pooled) × 2 co-primaries = 8 intervals") | PENDING-COMMIT. 4 × 2 = 8 |
| IC-5 | 2.73 (2.7270 unrounded) | the two-sided Šidák z at m = 8, family α 0.05 | PLAN:107 (read: "α' = 1 − 0.95^(1/8), with two-sided z_α' (≈ 2.73)"); implemented as `_sidak_z(M_FAMILY)` in `che/scripts/interaction_analysis.py`, asserted by `che/tests/test_interaction_check.py::test_analysis_family_mirrors_the_plan` | PENDING-COMMIT. DERIVED this session: α' = 1 − 0.95^(1/8) = 0.0063912; z = Φ⁻¹(1 − α'/2) = 2.7270 |
| IC-6 | 692 | total evaluations (main + floor) | PLAN:71 | PENDING-COMMIT. 656 + 36 = 692 |
