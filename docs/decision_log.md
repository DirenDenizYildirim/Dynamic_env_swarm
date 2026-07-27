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

**Margin analysis on record (M3.3):** the pilot found a previously-buried +~2%
seed-location edge effect (the 3×3 seeding dilation underweights border
cells, whose clusters are boundary-clipped, relative to the exactly-
uniform reference), so the purified ratio centers near 1.00, not ~0.97:
measured pilot ratio 1.003. Against the locked band the upper margin
(1.02) is therefore ~1σ of MC error at the affordable CPU sizes; the
test's pinned PRNG keys make the committed outcome deterministic, and
the measured ratio ± SE is printed by the test and recorded in the
report. If a future re-keying lands outside the band, that is a
report-and-ask event, not a tolerance adjustment.

## M4.2 ruling (human + RA, 2026-07-27) — E2C geometry; two kernel findings

**Measured blocker (RA, before implementation):** the phase-4 prompt's
*illustrative* E2C geometry (d = 6, l_f = 2, k = 17) cannot satisfy its
own acceptance criteria. With a single-cell smoke source the locked
M4.1 quadrature (n_quad = 4 midpoint samples) never lands on the ray's
endpoint beyond axis distance ~4, so tau = 1.0000 exactly at the first
two pre-commitment steps for every kappa_B up to 8 — hence q == 1, a
flat J* = 1 curve, and `J*(large) - 1/2 <= 0.02` unreachable.

**Ruling:**

1. **Option A approved** — shrink the geometry so every pre-commitment
   distance sits in the quadrature-sampled regime: **d = 2, l_f = 2,
   ell = 4, k = 9** (the prompt's rule k >= 2(d + l_f) + 1 holds; its
   d = 6 / k = 17 was illustrative, never locked). Measured q spans
   1.0000 -> 0.0056 over kappa_B in [0, 8].
   - **Option B rejected** (keep d = 6, add an approach-side smoke bank
     so the line of sight has a real medium): an unauthorized second
     smoke source and more bespoke micro-env machinery than the theorem
     needs.
   - **Option C rejected** (endpoint-inclusive quadrature): would
     re-open locked M4.1, invalidate its fresh bench row, and change
     obs-v3 semantics to serve a regime production rarely enters.
2. **Finding 1 is a documented kernel property, not a bug.** Recorded in
   the `transmittance` docstring, pinned by a test in
   `test_coupling_b.py`, and written up in `phase4_report.md` with a
   candidate limitations sentence for the paper: single-cell smoke
   sources contribute no occlusion beyond axis distance ~4; spatially
   extended sources (what the CA produces) are unaffected. **M4.3 must
   state explicitly in `kappa_b_lock.md` that its detection-band
   measurement (crop distance 3) sits in the well-sampled regime.**
3. **Finding 2 — the visibility plane is a side channel.** Smoke is
   co-located with the fire, so the mirror corridor cell's ray carries
   no smoke and is always revealed; "exactly one candidate masked"
   identifies Z without ever seeing fire content. Handling: q and the
   scored policies are **content-only** (test-enforced end to end:
   destroying plane 7 must not change the optimal/memorizing outcomes),
   the prediction MC and the empirical rollouts use **independent PRNG
   streams** (shared keys would reduce the acceptance test to the
   arithmetic identity J = q + (1-q)/2), and the side channel is
   **quantified per kappa_B**: a plane-7-only oracle identifies Z with
   accuracy 0.508 (kappa_B = 0), 0.989 (1.5), >= 0.9999 (>= 3).
4. **Scripted hazard + one smoke step before the first observation
   approved**; the prediction MC mirrors that protocol identically and
   the protocol is stated in the report (M3.3 lesson applied forward).
5. **Downstream, acknowledged:** under Option A the E2C cross-reference
   band (q in [0.3, 0.7]) maps to **kappa_B ~ 1.3-2.6**. If M4.3's three
   lock bands fail to intersect, **STOP** and bring the three curves to
   the lock discussion — a non-empty intersection was an assumption, and
   its failure is a finding, not something to route around.

**Open item carried to the M4.2 STOP (RA, not an RA decision):** the
prompt's acceptance criterion "empirical within 2·SE at every grid
point", applied per-point across 7 informative kappa_B values, rejects a
correct implementation ~28% of the time (1 - 0.9545^7). An 8-seed
replicate diagnostic measures the z-scores as N(0, 1) (pooled mean
+0.025, sd 0.990, 5.4% beyond 2 sigma vs 4.6% expected; no per-point
bias above ~0.13 SE), so the implementation is unbiased and the gate is
under-powered. On the pinned seed 0 the kappa_B = 5 point lands at
2.11 SE and the `@slow` test fails as written. No tolerance was adjusted
(invariant 4); recommended restatement is the Sidak family-wise
2.69 SE per point (5% overall), a one-constant change at `ACCEPT_Z` in
`che/tests/test_e2c.py`. Re-keying to a passing seed was considered and
rejected as seed-shopping.

## M4.2 statistical gate — final ruling (human, 2026-07-27)

Reconciled and final; **supersedes both** the phase-4 prompt's per-point
2·SE acceptance spec **and** the interim joint-chi2-only amendment, and
closes the open item logged at the end of the M4.2 ruling above.

Acceptance criterion 1 (empirical J* vs the numeric prediction) is
gated on the per-point z = delta / SE(delta) by **three conditions, all
required**, each catching a failure mode the others cannot:

- **(a) per-point |z| <= 2.69** (Sidak FWER 5%) — catches a localized
  gross error at a single kappa_B.
- **(b) joint sum z^2 against chi2(n), p >= 0.05** — catches diffuse
  magnitude misfit that no single point flags (every point sitting at
  -2 sigma passes (a) and fails (b)).
- **(c) |mean z| <= 2/sqrt(n) = 0.71** — catches signed systematic
  drift that passes both (every point at -1 sigma passes (a) and (b)
  and fails (c)).

n counts every grid point (kappa_B = 0 is deterministic, tau == 1 =>
q == 1, and contributes z = 0). Constants live at the top of
`che/tests/test_e2c.py` with the rationale as a single comment block.

**Measured at the M4.2 close: max|z| = 2.11, sum z^2 = 6.55 on 8 dof
(p = 0.586), mean z = -0.44 — GREEN on all three.**

Basis for replacing the per-point 2·SE spec: applied across the 7
informative kappa_B values it rejects a *correct* implementation ~28% of
the time (1 - 0.9545^7), and the 8-seed replicate diagnostic
(`phase4/m42/e2c_replicates.json`) measured the z-scores as N(0, 1)
(pooled mean +0.025, sd 0.990, 5.4% beyond 2 sigma vs 4.6% expected;
no per-point bias resolvable above ~0.13 SE). The gate was
under-powered; the implementation is unbiased. Not an RA tolerance
change — the RA carried it to the STOP as a report-and-ask.

## M4.3 lock (human + RA, 2026-07-27) — kappa_B = 1.1

**LOCKED: kappa_B = 1.1.** Full record and the calibration behind it:
`kappa_b_lock.md`.

1. **Dominance ordering, logged as predating the decision:**
   environment-native bands outrank toy-geometry cross-references. The
   E2C band is geometry-contingent per the M4.2 Option-A ruling (its
   constants were already re-chosen once, for quadrature reasons), so
   **E2C is demoted from hard constraint to consistency check**,
   satisfied within 10% (q = 0.765 vs the 0.70 ceiling). Rejected mirror
   choice kappa_B = 1.3 (q = 0.694 inside E2C; detection 0.347, outside
   the detection band by 0.053).
2. **The masked_frac band is RETIRED as a lock criterion** — not
   widened, not replaced post-hoc. It measures a policy-suppressible
   quantity; the suppression is a finding, not a calibration failure.
   Post-hoc replacement bands would be band-shopping; declined.
3. **Finding recorded (paper candidate):** behavioural
   perception-exposure regulation, mechanism = positioning (trained
   policies keep fire at the crop periphery: Medium masked_frac ceiling
   0.130 random -> 0.043 probe at identical burnt_fraction, survival
   0.784 -> 0.893). Third member of the endogeneity family.
4. **M4.4 addenda:** (a) masked_frac conditioned on burning-within-crop
   (danger-moment masking) reported as a diagnostic, not a band;
   (b) **logged pre-data:** positional suppression may mute the
   swarm-level kappa_B ablation delta — if the delta is small, the
   co-active analysis and danger-moment masking carry the interpretive
   weight, and a small delta is NOT evidence the coupling is inert;
   (c) render audit looks for smoke-periphery positioning.
5. Circularity check closed: the 0.5/1.5 two-arm probe bracket was the
   right design and cost one extra probe.

**Margin recorded by the RA after the ruling (not a challenge to it):**
detection at kappa_B = 1.1 sits *at* the 0.40 floor and the sign of the
margin depends on the measuring policy — 0.4045 (probe trained at 0.5),
0.3933 (probe at 1.5), 0.3515 (random). A probe trained at the locked
value interpolates to ~0.40. The paper should say "at the detection
floor", not "inside the band".
