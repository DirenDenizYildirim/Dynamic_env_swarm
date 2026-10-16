# WRITERS — step-4 assignments for Paper v3 (builder B1, step 3)

Written 2026-10-14. Five writers work in parallel. Each reads `BRIEF.md`,
then their stubs (each `STUB-SPEC` is the specification), then
`STRUCTURE.md` §2–§7 for their files. Budgets are prose words counted by
P3's method (STRUCTURE §3). Each writer owns exactly the files in their
row, plus:

- `paper/v3/provenance/<section file name>` for every section file they
  own (one row per sentence; `provenance_check.py --strict`);
- `paper/v3/ledger_proposals/W<n>.md` for their new rows, IDs `X<n>-<k>`
  (STRUCTURE §12 item 3), each VERIFIED from a committed file at file:line
  or DERIVED with its arithmetic, written **before** the number is used.

Nothing is committed (log:6236-6243). No writer edits another writer's file,
`BRIEF.md`, `STRUCTURE.md`, `DISPOSITIONS.md`, `checks/`, `src/`, the
ledgers, `paper/v2/` or anything outside `paper/v3/`.

## 1. Assignments

| writer | files | main-text prose | appendix prose | figures | listings | rows owed | holes (wait for step 0.5) |
|---|---|---|---|---|---|---|---|
| **W1** | `00_abstract.md`, `00_hero.md`, `01_introduction.md`, `12_conclusion.md`; `front_matter.yaml` `title` and `description` (B2 owns the file's other fields) | 250 + 30 + 600 + 90 = **970** (+ hero caption 60) | — | 1 | — | none (cites X4-2, X4-3, IC-*) | abstract lesson; §1 one sentence; §9 one clause; `description` recheck |
| **W2** | `03_environment.md`, `13_appendix_proofs.md`, `14_appendix_locks.md`; alternates `alt/13_appendix_proofs.thm1_tf.md` (V3Q5), `alt/13_appendix_proofs.no_prop4.md` (V3Q3) | **1,050** (+ Fig. 2 caption 50, Table 2 160) | ≈ 1,350 | 2 | 1–6 | X2-1, X2-2 | — |
| **W3** | `02_related_work.md`, `04_calibration.md`, `05_measurement.md`, `15_appendix_floors.md` | 400 + 700 + 270 = **1,370** (+ Table 1 120; Figs. 3–5 captions 180) | ≈ 500 | 3, 4, 5, C1 | — | none expected (all rows exist; add one only if a number lacks a row) | — |
| **W4** | `06_example_design.md`, `07_example_results.md`, `16_appendix_timeline.md`, `18_appendix_secondary.md` | 500 + 480 = **980** (+ Figs. 6–8 captions 170; Table 3) | ≈ 1,400 + quotations | 6, 7, 8 | — | X4-1, X4-2, X4-3, X4-4, X4-5 | — (W4's text does not depend on the check) |
| **W5** | `08_interaction_check.md`, `09_example_lesson.md`, `10_limitations.md`, `11_using_che.md`, `17_appendix_results.md`, `19_appendix_interaction.md`, `20_appendix_episodes.md`, `21_appendix_making.md` | 200 + 150 + 200 + 240 = **790** (+ Fig. 9 caption 60) | ≈ 1,430 | 9 (after step 0.5), E1, E2, H1, H2 | — | X5-1, X5-2 (both PENDING until committed / transcribed); optional X5-3 throughput (V3Q18) | §6.4 result and Figure 9; §6.5 lesson half and advice; App. G tables |

**Balance (B1's reasoning).** Main-text prose ranges 790–1,370 words; the
lighter main-text loads carry the heavier appendices (W2, W4, W5) or the
abstract and title work (W1). W4 keeps the whole worked-example design and
results plus the timeline, because the F3 account, the identity and the
registered strings must read as one; the interaction-dependent text is
concentrated in W5 (and W1's abstract), so only two writers wait for step
0.5. W3 takes §2 so W1's load stays on the abstract, the introduction and
the title candidates.

## 2. Rows owed before use (V3-E3)

| ID | value | source / derivation | writer | used in |
|---|---|---|---|---|
| X2-1 | 0.5000 ± 0.0055 measured, 0.5028 predicted, z −0.51 at κ_B = 8 | VERIFIED `che/bench/results/phase4/phase4_report.md:72` | W2 | App. A (Thm. 1) |
| X2-2 | the corridor toy's optical depths (P3: ≈ 0.707, 0.898, 0.987) | DERIVED from `tau_profile` in `che/bench/results/phase4/m42/e2c_sweep.json`: D_t = −ln τ_t / κ_B; show one κ_B | W2 | App. A (only if V3Q5's default stands) |
| X4-1 | the identity at each arm: ISO 2/3, ISO-4 1, JOINT 1; sweep 1 − p; identification 0.8 − p | DERIVED from DES-7, DES-14, DES-16, DES-9 (P1 §5.2) | W4 | §6.2; pointed to by §6.5, abstract |
| X4-2 | training δ per arm: ISO's A-only and B-only components δ 0, δ-only components δ 1; ISO-4 all δ 0; JOINT δ 1; θ\* δ 1 | VERIFIED `che/configs/p6_iso.yaml:41-46`, `p6_iso4.yaml:36-39`, `p6_joint.yaml:36-37`, `theta_star_holdout.yaml:76` | W4 | §6.2; §1 |
| X4-3 | about 0.11 agents per episode ("about a tenth") | DERIVED: 0.0095531 (`che/bench/results/phase6/unblind/unblind.json:61`) × 12 (ENV-6) = 0.1146; identity as DX-406 (`che/env/env.py:446`; `che/tests/test_lethality.py:201-202`); scope: the size statement (DX-406 is scoped to the fire-death comparison) | W4 | §6.3; abstract, §1 |
| X4-4 | Γ₄ and B̂ survival detection limits 0.0090 and 0.0089 | VERIFIED `che/bench/results/phase6/post_unblind_analysis/post_gamma4_t2000.md:15-16`, last column; confirm what the column is (80 %-power, family level) at its source before use | W4 | §6.3 (Γ₄'s, one clause); V3Q18 |
| X4-5 | 2026-10-12, the framing change | VERIFIED `docs/decision_log.md:6115`, :6158-6169 | W4 | App. D only |
| X5-1 | the supplement zip's size | step 2's output (`paper/v3/out/build_summary.json`) once **committed**; PENDING-COMMIT until then (V3Q25) | W5 | §8 |
| X5-2 | TMLR's supplementary-material limit | only after TMLR's author guide is re-read directly and the reading transcribed (V3Q24); otherwise cut | W5 | §8 |
| X5-3 (optional) | training throughput | DERIVED from DX-3 ÷ DX-4, if the owner wants it (V3Q18) | W5 | §8 |
| IC-* | every interaction-check number (evaluation count, Šidák m and z, per-arm and pooled I with interval ends, MDE80s, self-floor results, cross-GPU identical count, realized GPU-hours) | the committed step-0.5 report (`che/bench/results/phase6/post_v3_interaction/interaction_report.{md,json}`), by the **orchestrator**, in `paper/v3/ledger_proposals/IC.md` | orchestrator | §6.4, App. G, abstract, §1, §6.5, §9 |

## 3. Cross-writer facts fixed now (so nobody waits)

- **Figure numbers** (STRUCTURE §4): 1 hero; 2 schematic; 3 severity; 4
  Coupling A; 5 Coupling B; 6 composer; 7 simplex; 8 registered readings;
  9 interaction check; appendix C1, E1, E2, H1, H2. **Listings** (STRUCTURE
  §5): 1–4 in §3, 5 in App. A, 6 in App. B. **Appendix letters** A–J
  (STRUCTURE §2). **Tables:** 1 related work (§2), 2 claims (§3.4), 3 the
  registered readings (§6.3).
- **Section numbers:** §1 Introduction … §6.1–§6.5 the worked example, §7
  Limitations, §8 Using CHE, §9 Conclusion.
- **Plain names** (BRIEF §5.2): W4 defines ISO, ISO-4, JOINT, Γ, Γ₄, B̂, μ,
  p, active share and fire-only share in §6.2 (W1 may use the arm names in
  §1 with a one-clause gloss); W5 defines the interaction check, the
  conditions and I in §6.4; W3 defines floor, bar, detection limit and
  exclusion bound in §5; W2 defines θ, "locked" and co-active in §3.
- **Caveat homes** (`checks/caveats.yaml`): each writer states their homes
  in full once and only points elsewhere. In particular W1's §1 carries
  short forms of C01, C02, C03, C04, C10, C11, C16, C17, C18, C27, C32,
  C33, C34 and the full C05.
- **The lesson** in the abstract (W1) and §6.5 (W5) must be the same
  reading; W5 drafts §6.5 first once IC rows exist, and W1 follows it.

## 4. Order and the interaction check

1. All five start now. Everything except the HOLEs is writable today.
2. The orchestrator writes `IC.md` after step 0.5 (results returned,
   hashes verified, analysis run once, report committed — commits need the
   owner's branch, log:6236-6243).
3. W5 fills §6.4, App. G and §6.5's lesson; a figure builder makes Figure 9
   from the committed outputs (new output directory, P2 §9); W1 then fills
   the abstract's lesson, §1's sentence, §9's clause and rechecks
   `description`.
4. If the results are not back when step 4's review starts: the abstract and
   §6.5 use the identity lesson (P1 §3.3, "not back in time"), §6.4 states
   the check as planned with its HOLEs visible to the reviewers, and V3Q7
   records it.

## 5. Hand-back

BRIEF §18, plus: the output of B2's term, date and one-home checks on your
files (if available), every HOLE and OWNER-PENDING marker left, and every
row you wrote with its verification line.
