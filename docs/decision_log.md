# Decision log

Locked design decisions. Entries are append-only; reopening one requires an
explicit human call recorded here. D1–D3 predate this file and are restated
from `CLAUDE.md` (which remains authoritative for them); D4 onward are
recorded here first.

## D1 — Dynamic hazard is the baseline substrate (Phase 0)

Dynamic hazard (β > 0) is the baseline substrate in all configs; the
composable "elements" are {Coupling A, Coupling B, comms denial}.

## D2 — ISO baseline definition (Phase 0)

ISO baseline = one policy trained on a mixture of single-element configs;
same architecture/compute as JOINT.

## D3 — Smoke outlives flame (Phase 0)

Smoke field ρ with emission σ_s and decay η is a state component (Def. 6);
smoke persists after flame passes.

## D4 — death_penalty = 0.5 default for all training from Phase 3 onward (2026-07-19)

dp = 0 is demoted to a secondary ablation slot.

**Evidence (M2.5 pillar-only grid, 3 severities × dp ∈ {0.0, 0.5} × 3 seeds,
500 updates; `che/bench/results/phase2/phase2_report.md`):**

- Low: tied — survival at ceiling under both arms.
- Medium: modest consistent gain (survival 0.931 → 0.951, deaths −28%).
- High: decisive — survival 0.575 → 0.866, deaths_fire 5.10 → 1.61 (−68%),
  and completion *also* improves (0.765 → 0.821). At dp = 0 the
  return-optimal High policy spends agents for food; dp = 0.5 finds a policy
  better on both axes.

Note: dp = 0.5 is a shaping term on the task reward (agent death is a task
variable); reward independence (Def. 2) is unaffected — the reward still
reads no hazard/smoke/structure state.

Confirmed by human 2026-07-19 at Phase 3 start.

## D5 — obs v2: separate indicator planes (2026-07-20)

Observation grid moves from 5 mixed-encoding planes to 7 indicator planes
(smoke stays continuous): **burning, burnt, smoke, food, weak, collapsed,
alive-occupancy**, in that order. `EnvConfig` gains `obs_version: 2`;
v1 remains restorable for archival evaluation only (`--obs-version 1` in
the eval/render CLIs). M3.2 onward is v2-only; all v1 results stay
archived and labeled obs-v1 probes; **no cross-version comparisons, ever**.

**Motivating evidence (M3.0b audits 1–2,
`che/bench/results/phase3/m30b/`):** v1 plane 0 encodes hazard state / 2,
so Burnt (1.0) reads *higher* than Burning (0.5) — ash looks maximally
dangerous. Medium-trained policies abandon the burnt region after fire
death (rendered: 11 agents idle at the ash boundary for 128 steps, 13
food items stranded); the 3×3 cross matrix shows the same signature in
zero-death conditioning (Low/Medium-trained on High complete 0.688/0.749
vs High-trained 0.836 with nobody dying — terrain avoidance, not
attrition). Indicator planes remove the spurious ordinal structure.

Causal-mechanism check (registered before running): retrain
{low, medium, high} seed 0 under v2, re-render medium's exact m30b
episode seeds — does post-fire burnt-region abandonment disappear, and
does the completion ordering flatten? → `phase3/m31b_obs_v2.md`.

Locked by human 2026-07-20 (M3.0b review).

## Standing rule (logged after D5, human-issued 2026-07-21) — 100k line auto-triggers the uint8 contingency

If any future phase's bench row projects training throughput below
**100k steps/s** (at the Phase-0 env:train projection method), the
**uint8 obs-storage contingency activates and is re-benched before that
phase's acceptance runs** — not discussed, activated. The 100k line
itself does not move without a budget recalculation recorded in this
decision log.

Context: the M3.1b obs-v2 bench row projected ~118.3k (margin over the
line shrank from ~56k to ~18k; `gate_report.md`, "M3.1b / D5" section).

## M3.3 ruling (human, 2026-07-21) — Prop.-3 acceptance test v2; band change human-locked

**Spec error logged (RA):** acceptance test v1 (phase3_prompt.md M3.3 /
commit d208645) compared protocol-mismatched quantities: the sweep slope
(uniform seed locations, uniform birth times, unconditional cluster mass)
against the Phase-2 χ̂ estimator (center ignition, non-spanning-
conditioned, T = 4L). The L = 32 in-band pass (ratio 1.025 in
[0.75, 1.05]) was a *cancellation* of the two protocols' opposite biases
(conditioning ×1.727 up vs location/age/overlap down); at L = 64 the
conditioning bias nearly vanishes (2% span) and the same sweep measured
slope/χ̂ = 0.686. Full accounting: phase3_report.md M3.3 +
`m33/deficit_decomposition.json`.

**Ruling (verbatim intent):**
1. The dense L = 64 sweep stays the headline artifact; the matched-
   reference line (54.48) is added to the figure beside the naive χ̂
   line; the four-factor waterfall goes in the report as an appendix-
   style panel. Re-running to chase a prettier ratio was declined —
   the dense regime is the informative one.
2. Acceptance test v2 (`che/tests/test_prop3.py`): the reference is
   computed *matched to the sweep's protocol* inside the test
   (`matched_reference`: single-seed rollouts at the test's own L,
   uniform locations, uniform birth times via age-averaging,
   unconditional mass), and the sweep runs in a purified sparse regime:
   κ_A with P(≥2 seeds | ≥1) ≤ 2% and overlap proxy ≤ 3%.
   **Acceptance band [0.90, 1.02] × matched_ref, R² ≥ 0.99 —
   human-locked here** (supersedes the v1 [0.75, 1.05] × χ̂ band; not
   an RA tolerance change).
3. The L = 32 cancellation analysis stays in the report verbatim
   (paper-appendix candidate).
4. The finite-protocol-corrections remark (human-authored) was added to
   docs/theory_foundations.md after Prop. 3.

**Implementation constants (RA, from a measured pilot at L = 32,
N = 2048):** κ_A_PURE = 0.003 (P(≥2|≥1) = 1.3%; 0.005 was piloted and
rejected — its sibling birth-adjacency floor alone puts the proxy at
~3.5% > 3%); LAMBDAS_L32_PURE = (4e-5..2e-4), realized E[N_seeds]
0.11–0.56, top burnt density ~2.2% → proxy ≈ 2.4%. SWEEP_MC = 8192,
MATCHED_MC = 16384 → combined MC error ≈ 2.4% on the ratio.

**Margin analysis on record:** the pilot found a previously-buried +~2%
seed-location edge effect (the 3×3 seeding dilation underweights border
cells, whose clusters are boundary-clipped, relative to the exactly-
uniform reference), so the purified ratio centers near 1.00, not ~0.97:
measured pilot ratio 1.003. Against the locked band the upper margin
(1.02) is therefore ~1σ of MC error at the affordable CPU sizes; the
test's pinned PRNG keys make the committed outcome deterministic, and
the measured ratio ± SE is printed by the test and recorded in the
report. If a future re-keying lands outside the band, that is a
report-and-ask event, not a tolerance adjustment.
