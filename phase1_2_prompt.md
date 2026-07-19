# Phases 1–2 — Hazard–Agent Interaction, Static Control, Severity Calibration

> Fresh Claude Code session at the repo root. Prerequisites: Phase 0 complete
> (see `che/bench/results/phase0_report.md`), suite green, and
> `che/tests/test_nesting.py` committed. Work strictly milestone by
> milestone; stop at each STOP line and report.

## Context

Phase 0 proved the substrate (12.86M env-steps/s env-only; 159k train
steps/s, PASS). Phases 1–2 make the hazard *matter*: agents can now die, the
static-hazard control variant is built (the memorization comparison of
Thm. 1's framing at system scale), and the pillar's severity levels are
calibrated from measured phase structure per theory doc §3 — replacing the
placeholder β=0.35 with principled Low/Medium/High configs.

Couplings A and B remain inert (Phases 3–4). Comms remains absent (Phase 5).
All Phase-0 invariants stay in force; the nesting suite must be *extended*,
never weakened, by every milestone here.

---

# PHASE 1 — hazard–agent interaction + static-hazard control

## Milestone 1.1 — Lethality and blocking (T_X finally reads h and c)

Semantics (implement exactly; each is a named test):

- **Burning is lethal.** After movement, an alive agent whose cell is
  Burning in h' is disabled: alive' = alive ∧ ¬(cell(x') = Burning in h').
  Note the Prop.-1 order: h' is sampled *before* x', so lethality is
  evaluated against the post-update hazard — a cell igniting under a
  stationary agent kills it.
- **Collapsed is impassable.** A proposed move into a cell Collapsed in c'
  is cancelled (agent stays). Burnt cells are passable (ash).
- **Collapse under an occupant disables it.** An alive agent standing on a
  cell that collapses this step (c increment) is disabled ("falls").
  DECISION default ON — it is the physically honest choice and it is what
  makes load-triggered collapse (Phase 3) strategically meaningful.
- **Dead agents are inert.** Never move, never collect (occupancy already
  filters on alive), exert no load (DECISION: mass removed), and disappear
  from the alive-occupancy observation plane. They are attrition (α_i in
  Def. 1), not obstacles.
- **Optional death penalty, Def.-2-compliant.** `ThetaConfig.death_penalty`
  (default 0.0): reward −c per newly disabled agent this step. This reads
  only the α transition — an X variable — so Def. 2 (reward never reads
  h/ρ/c) still holds; extend `test_reward_independence` with a
  death_penalty>0 case: two states differing only in hazard/smoke/structure
  with identical alive vectors must still yield identical reward.

New `info` fields: `deaths_fire`, `deaths_collapse` (per-step int32 counts).

**Tests:** exact death semantics (construct h'/c' by hand around an agent);
blocking; collapse-kill; dead-agent inertness over a rollout; nesting suite
extended (death logic may not perturb PRNG streams — same-key trajectories
with lethality on vs. a hand-built variant consume identical draws).
**Accept:** suite green (CPU, <2.5 min). STOP.

## Milestone 1.2 — Perception model locked (obs v1)

- Planes (in order): hazard/2, smoke, food, structure (collapsed=1),
  alive-agent occupancy. `obs_window` default 9 (update configs). OOB pads 0.
- Own-state vec unchanged (position, alive, t/horizon).
- Re-run the M0.4 bench at the reference cell only (64², 1024, 12) with the
  new obs; append a "Phase 1 obs v1" row to the gate report. Expect a
  moderate hit from the k=5→9, 3→5-plane crop; if the *training* projection
  (÷81, per the measured Phase-0 ratio) falls below 100k steps/s, flag it —
  the known contingency is uint8 obs storage with in-network normalization
  (phase0 report note), but do NOT implement it without asking.
**Accept:** bench row appended, verdict stated. STOP.

## Milestone 1.3 — Static-hazard control variant (the memorization control)

- `EnvConfig.hazard_mode: {"dynamic", "frozen"}` (env-level protocol knob,
  deliberately not in ThetaConfig — it is a training-protocol variant, not a
  stressor element).
- `frozen`: at reset, run `t_gen` CA steps (default horizon/2) from the
  single ignition, then freeze h for the whole episode. Frozen Burning cells
  stay Burning (lethal, smoke-emitting) but never spread or burn out.
- Rationale to preserve in a docstring: with t_gen = horizon/2 the frozen
  map is a draw from the *same marginal* the dynamic env passes through
  mid-episode — the control differs in evolution, not in hazard mass
  (system-scale analogue of Thm. 1's fixed-map policy).
- PRNG discipline: the frozen branch must consume the identical stream the
  dynamic branch would (hazard_step's draws happen and are discarded), so
  dynamic↔frozen with the same key differ *only* through the freeze.
  Add this as a nesting-suite test (structure/food/agent draws bitwise
  identical across modes until first divergence via hazard-dependent death).
**Tests:** frozen h constant over the episode; smoke still evolves to its
steady state; burn-in reproducibility per key. **Accept:** suite green. STOP.

## Milestone 1.4 — Episode metrics

Per-episode (surfaced at `done` in info, NaN-safe aggregation in training
logs): `survival_rate` (alive fraction at end), `completion` (food collected
/ n_food), `deaths_fire`, `deaths_collapse` (episode totals). Wire into IPPO
and PBT metric rows + the plot scripts.
**Accept:** metrics visible in a debug-scale training log. STOP.

## Milestone 1.5 — Phase 1 acceptance training

- Dynamic mode, β=0.35 (placeholder until Phase 2), 64², 12 agents, single
  policy (n_envs 256), ~500 updates, death_penalty 0.0 and one run at 0.5
  (report both).
- **Accept when:** trained policy beats the random baseline on *both*
  completion and survival_rate with a visible margin (report exact numbers +
  curves to `che/bench/results/phase1/`); random baseline recorded in the
  report (Phase-0 lesson). Write `phase1_report.md` (same format as phase0).
  STOP — human reviews before Phase 2.

---

# PHASE 2 — severity calibration (theory §3 made executable)

## Milestone 2.1 — Hazard-only calibration engine

`che/calibration/percolation.py`:

- Pure-hazard rollouts (no agents, no task — reuse `hazard_step` unchanged;
  it already accepts a traced β, so **vmap over (β, seed)**).
- Protocol per (L, β, seed): all-Fuel L×L grid, single center ignition,
  scan T_max = 4L steps (fixed length; absorption is cheap under jit).
- Measured per run: `spanned` (any Burning/Burnt cell touches the boundary),
  `burnt_fraction` at T_max, `extinction_time` (first step with no Burning,
  else T_max), `front_radius[t]` (max Chebyshev radius of non-Fuel cells,
  running max inside the scan).
- Grids L ∈ {32, 48, 64}; β grid: 0.05..0.95 step 0.05 coarse, refined
  0.40..0.60 step 0.01; ≥512 seeds per (L, β).
- Budget sanity (report actual): ~25+21 β values × 512 seeds × 3 sizes at
  ≤256 steps is minutes at Phase-0 throughput. Run on GPU; results to
  `che/bench/results/phase2/calibration.npz` + provenance JSON (jax version,
  device, seed).
- **Amendment 2026-07-19 (spec correction, accepted from M2.2 findings):**
  the center-seed `spanned` observable has one-sided finite-size bias, so
  its finite-size curves never cross. Add a second calibration mode:
  ignite the **full left column** at t=0 and record `crossed` = fire
  reaches the right column — by the Prop.-2 coupling this equals the
  canonical left–right crossing probability R_L(β). Refined β grid only,
  all three L, ≥512 seeds; results to `calibration_crossing.npz` +
  provenance.

## Milestone 2.2 — Estimates

- `P_span(β)` per L; R_L(β) per L (amendment mode). β̂_c estimators
  (amended 2026-07-19 — report all, with spread): (a) crossings of the
  R_L pairs (32,48) and (48,64); (b) ½-locus of center-seed P_span
  extrapolated against L^(−3/4) (ν = 4/3 exact), with the 1/L fit reported
  too as sensitivity; (c) steepest slope of P_span at L=64.
- Soft check (report, not a hard test): measured R at β̂_c should be near
  0.5 (self-duality); note the value in `calibration_report.md`. Keep the
  one-sided-bias explanation in the report — it is methods text likely to
  survive into the paper's appendix.
- `χ̂(β)`: mean burnt cluster size on the subcritical side (burnt_fraction ×
  L² over non-spanning runs) — this curve is reused by Phase 3's Prop.-3
  test, so save it.
- Supercritical front speed v̂(β): slope of front_radius[t] over its linear
  regime for β > β̂_c.
**Accept:** `calibration_report.md` with three figures (P_span sigmoids,
χ̂(β), v̂(β)) and the β̂_c estimates. STOP.

## Milestone 2.3 — Theory unit test (the Phase-2 hook from theory §10)

`che/tests/test_percolation.py` (marked `@pytest.mark.slow`, CPU-scale
L=32, ≥256 seeds, coarse β grid — keep <60 s):

- P_span monotone non-decreasing in β (allowing MC noise: isotonic within
  2σ binomial error).
- β̂_c ∈ [0.42, 0.58] (idealized von-Neumann kernel: exactly 1/2; the band
  covers finite-size + estimator bias — a kernel outside this band is
  mis-ported, per theory §10; do not widen the band without asking).
  Band unchanged by the 2026-07-19 M2.2 amendment.
- v̂ increasing over the three largest tested β.
**Accept:** slow suite green. STOP.

## Milestone 2.4 — Severity bands → locked configs

Bands per theory Def. 4 (observable-defined; propose exact β per band from
the L=64 measurements):

- **Low** (subcritical): P_span < 0.05 and mean burnt_fraction ∈ [1, 5]%.
- **Medium** (near-critical): P_span ∈ [0.3, 0.7].
- **High** (supercritical): v̂(β) ∈ [0.5, 1.0] cells/step (agent speed = 1).

Emit `che/configs/severity_{low,medium,high}.yaml` (full config, provenance
comment: β chosen, measured observables, calibration file hash). If a band
is empty or ambiguous on this kernel, report the curves and ask — do not
invent a compromise silently.
**Accept:** three configs + report section. STOP — **human locks the bands.**

## Milestone 2.5 — Pillar-only training probe

- Full grid: 3 locked severities × death_penalty ∈ {0.0, 0.5} × 3 seeds =
  18 runs (dynamic mode, single policy, n_envs 256, ~500 updates each;
  ≈ 20 min/run at measured throughput, ~6 GPU-hours total — report actual).
  Rationale (Phase-1 finding): at subcritical severity the two dp values
  are statistically tied because survival is at ceiling; whether an
  explicit death penalty matters is an open question exactly at
  Medium/High, and the near-critical variance prediction requires seeds.
- Report per (severity, dp): completion, survival_rate, deaths_fire —
  mean ± across-seed range — plus curves; a comparison table in
  `phase2_report.md`. Expected qualitative pattern (report, don't force):
  survival degrades with severity; Medium shows the highest across-seed
  variance (near-critical fluctuations, theory Def. 4). Also report
  mean_smoke_exposure if the metric exists on main by then.
**Accept:** report complete. STOP — Phase 2 complete; GO/NO-GO on Phase 3
(Coupling A + Prop.-3 scaling test, which will reuse χ̂ from M2.2).

## Non-goals for Phases 1–2

Couplings A/B active in training, comms, E_2C micro-env (Phase 4), ISO/JOINT
protocols (Phase 6–7), obs-storage optimization (contingency only), any
edit to `docs/theory_foundations.md` (human-owned).
