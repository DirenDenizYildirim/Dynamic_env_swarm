# Phase 3 — Coupling A live + evaluation harness (+ the Def.-4 variance re-test)

> Fresh Claude Code session at repo root. Prerequisites: Phase 2 complete
> (`phase2_report.md`), GO recorded, decision **D4: death_penalty = 0.5
> default for all training from Phase 3 onward** (dp=0 demoted to
> secondary ablation; M2.5 evidence — confirm D4 is committed in the
> decision log before starting). Milestone by milestone; STOP and report.

## Context

Phase 2 locked severities as measured dynamical phases and saved χ̂(β)
(`estimates.npz`) specifically so this phase can test Prop. 3: expected
burnt area per collapse-seeded ignition equals the mean percolation
cluster size. Phase 3 activates structural collapse and Coupling A
(collapse → ignition seeding), calibrates its parameters against target
observables, and validates the implementation against the theory
quantitatively. It also builds the evaluation harness (needed for Phases
6–7 regardless) and uses it to re-test the Def.-4 variance prediction the
M2.5 probe could not cleanly measure.

Coupling B stays inert (Phase 4). Comms stays absent (Phase 5). All
invariants in force; the nesting suite extends with every milestone.

---

## Milestone 3.0 — Evaluation harness + Def.-4 variance re-test

- `che/eval/harness.py`: load an orbax checkpoint (config-hash guarded),
  run N eval episodes (vmap'd; default N=512) with the policy as-trained
  (stochastic; `--greedy` flag optional), emit **per-episode** metrics —
  completion, survival_rate, deaths_fire, deaths_collapse,
  mean_smoke_exposure, coupling-co-active count — to npz + summary JSON
  (mean, std, quartiles). No training-code changes.
- **Def.-4 re-test:** for the final checkpoints of M2.5's dp=0.5 runs
  (3 severities × 3 seeds), run 512 eval episodes each; report the
  *per-episode* variance of completion and survival at fixed policy, per
  severity (pool across seeds and per-seed). Prediction on record: Medium
  highest. Report the outcome either way (confirmation or refutation both
  go in the record verbatim); note episode-count-based CIs.
- **Accept:** harness tests green (fixed-seed reproducibility; per-episode
  row count; checkpoint-hash guard) + variance report in
  `che/bench/results/phase3/def4_variance.md`. STOP — human reads this
  before anything else in the phase.

## Milestone 3.1 — Structural dynamics live

- Activate `structure_step` for real use: per-cell per-step collapse
  probability λ(g) = `lambda_0 · weak(g)` + `lambda_load · weak(g) ·
  occupied(g)`, with a **weak-cell terrain mask** generated at reset
  (fraction `f_weak` of cells, spatially clustered via a few smoothing
  passes on noise — parameters in config; collapsed is absorbing). Only
  weak cells can collapse; the mask is visible as the structure obs plane
  value 0.5 (weak-intact) vs 1.0 (collapsed) — agents can perceive risk.
  DECISION default: weak mask *observable* (risk-aware locomotion is the
  interesting behavior; a blind variant is a later ablation knob).
- Tests: only-weak-cells collapse; load term fires only under occupancy;
  absorbing; obs plane encoding; nesting (terrain-mask generation consumes
  a dedicated key stream; λ=0 bitwise-recovers Phase-2 trajectories).
- **Accept:** suite green. STOP.

## Milestone 3.2 — Coupling A active

- `coupling_a_seed_mask` goes live: each collapse event ignites each Fuel
  cell within Chebyshev radius `r_A` (default 1 ⇒ 3×3 neighborhood)
  independently w.p. κ_A. Verify plumbing end-to-end: seeded ignitions
  join the same Burning population (spread, smoke, lethality identical to
  primary fire); `info` gains `seeded_ignitions` count; the
  coupling-co-active counter now counts (per M0.3 plumbing) — confirm it
  goes nonzero in a hand-built scenario test.
- Tests: seeding occurs iff (collapse ∧ Fuel ∧ within r_A); κ_A=0 bitwise
  nesting still green; smoke from seeded fires behaves identically.
- **Accept:** suite green. STOP.

## Milestone 3.3 — ★ Prop.-3 quantitative test ★ (theory §10 hook)

Hazard+structure-only rollouts (no agents ⇒ lambda_load inert), at
**Low severity β=0.43**, iota=0, **no primary ignition** (all fire born
from collapses — the "collapse is the only birth channel" regime of
Prop. 3):

- Sweep lambda_0 over ~5 values spanning sparse to moderate (target: mean
  seeded-cluster mass ≪ arena; report the disjointness diagnostic —
  overlap fraction of seeded clusters); ≥512 seeds per value; horizon 256.
- Measure per run: total burnt area B_T and realized seeded-ignition count
  N_seeds. **Test:** the least-squares slope of E[B_T] vs E[N_seeds]
  equals χ̂(0.43) from Phase 2's `estimates.npz` (measured value ≈ 52)
  within a tolerance that accounts for (i) MC error and (ii) the
  *directional* bias of cluster overlap (overlap only reduces — the
  measured slope may sit slightly below χ̂, never meaningfully above).
  Suggested acceptance: slope ∈ [0.75, 1.05] × χ̂(0.43), plus linearity
  R² ≥ 0.99 across the sparse points. Implement as a @slow test at L=32
  with its own CPU-scale χ̂ reference (recompute χ̂ at L=32 inside the
  test — do not compare across grid sizes), and as a full-scale GPU
  script whose result goes in the phase report.
- **Accept:** slow test green; GPU-scale figure (E[B_T] vs E[N_seeds],
  fitted slope vs χ̂ line) in `phase3_report.md`. STOP — this is the
  quantitative theory↔implementation handshake; human reviews the figure.

## Milestone 3.4 — Coupling-A parameter calibration → human lock

Propose defaults for (f_weak, lambda_0, lambda_load, κ_A, r_A) against
target observables, measured with random-policy rollouts at each severity
(fast; reuse the calibration engine pattern):

- collapse events/episode ∈ [3, 10] (enough to matter, not dominating);
- seeded ignitions/episode ∈ [1, 5];
- at **Low**, seeded fires contribute ≥ 50% of total burnt area (the
  Prop.-3 regime where Coupling A dominates the hazard budget — with a
  primary ignition restored, measure the split via provenance-tagged
  burnt masks or paired runs with κ_A ∈ {0, κ_A*});
- deaths_collapse/episode (random policy) ∈ [0.05, 0.5].

Emit a `coupling_a_lock.md` proposal table (candidate values + measured
observables, same format as `severity_lock.md`). **STOP — human locks.**

## Milestone 3.5 — Acceptance training

- Grid: 3 severities × κ_A ∈ {0, locked} × 2 seeds, dp=0.5 (D4), 500
  updates, locked Coupling-A params. (12 runs, ~1 GPU-h at measured
  throughput.)
- Report per cell: completion, survival, deaths_fire, deaths_collapse,
  seeded_ignitions, smoke exposure; eval-harness per-episode stats at
  final checkpoints (not just training-log tails). Questions the report
  must answer: does Coupling A shift behavior (load-avoidance on weak
  cells — e.g., occupancy rate of weak cells vs κ_A=0)? Does Low-severity
  survival finally leave the ceiling once collapse-seeded fire dominates?
- **Accept:** `phase3_report.md` complete with the Prop.-3 figure, the
  Def.-4 re-test outcome, and the acceptance grid. STOP — Phase 3
  complete; GO/NO-GO on Phase 4 (Coupling B + Thm.-1 E2C micro-env) is a
  human call.

## Non-goals

Coupling B, comms, E2C, ISO/JOINT, food destructibility (open design
note from the severity lock — raise, don't implement), any theory-doc
edits, dp=0 beyond the named ablation slot.
