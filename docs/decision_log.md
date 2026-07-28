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

## M4.4 amendments (human, 2026-07-27) — lock revised to kappa_B = 1.0

Issued before any M4.4 run; supersedes the kappa_B = 1.1 entry above.

1. **LOCK REVISED: kappa_B = 1.0.** The RA measured the detection margin
   after the initial ruling: kappa_B = 1.1 satisfies the *dominant*
   environment-native band under only 1 of 3 measurement conditions
   (det 0.4045 / 0.3933 / 0.3515 under the kB=0.5 probe / kB=1.5 probe /
   random), where 1.0 satisfies it under both probe arms (0.4383 /
   0.4266). Applied consistently the dominance ordering points below
   1.1 — the step from 1.0 to 1.1 buys ~4 points on the *demoted* E2C
   constraint and spends the margin on the band that dominates.
   **0.95 recorded as considered** (inside under 3/3, E2C 18% off);
   **1.1 recorded as considered and superseded** (E2C 10% off but
   detection only at the floor). At the locked 1.0 the E2C consistency
   check is q = 0.812 vs a 0.70 ceiling — a 16% miss. The locked value
   is written into the three severity YAMLs (M3.4 -> M3.5 precedent);
   M4.4 overrides to 0.0 for the ablation arm. A **detection-drift
   check** under the M4.4 500-update checkpoints is folded into the grid
   job (`coupling_b.py --probe-ckpt`; M3.5 drift precedent).
2. **Finding (behavioural perception-exposure regulation) DEMOTED to
   provisional.** Both M4.3 probe arms trained with Coupling B live, so
   exposure suppression is not separable from a fire-avoidance byproduct
   (smoke co-locates with fire). The M4.4 kappa_B = 0 arm is the free
   control — identical lethality incentives, masking bitwise-inert.
   Cross-arm exposure/ceiling/periphery comparison decides: different ->
   perception-driven regulation confirmed; indistinguishable -> restated
   as a fire-avoidance byproduct.
3. **Inertness falsifier logged pre-data** (restores symmetry to the
   "a small delta is not evidence of inertness" pre-registration): the
   coupling is inert at swarm scale **iff** (i) Delta-completion and
   Delta-survival within seed noise AND (ii) no cross-arm
   exposure/positioning difference AND (iii) danger-moment masking
   negligible AND (iv) no co-active visitation difference. All four -> a
   reportable negative result.
4. **Third seed at Medium approved** (+4 runs, ~20 GPU-min): Def.-4
   variance concentrates near criticality, and "small but real" is now a
   pre-registered possibility that two seeds cannot separate from noise.
   Low/High stay at two seeds. Grid is therefore 14 train + 14 eval runs.


   PHASE 6 ENTRY GATE (do not start Phase 6 without executing this line):
Re-read D6-proposal with the RA. Decisions owed before any Phase-6 run:
(1) dose-response design formalized into the phase prompt;
(2) pilot scoped (2 mixture points);
(3) one-paper vs two-paper fork scheduled for after the pilot.


## M4.4 outcome (RA, 2026-07-28) — pre-committed rules applied, no new rulings

Recorded because two decisions were *executed* here rather than made:
both branches were fixed in advance by the M4.4 amendments, and the data
selected the branch.

1. **Amendment 2 (provisional finding) — branch taken: "indistinguishable
   -> restated as a fire-avoidance byproduct."** Two independent
   controls agreed. (a) Training length: the masked_frac ceiling
   suppression that motivated the finding (Medium 0.128 random -> 0.043
   at 200 updates) is gone by 500 updates (0.102 / 0.134). (b) The
   kappa_B = 0 control is the *less* exposed arm at Low and Medium,
   which is the opposite sign to perception-driven regulation; at High
   the coupled arm is less exposed but also loses 8.8 points of
   survival, and exposure averages over alive agents, so the confound
   cannot be removed (conditioning on zero-death episodes is a collider,
   44 % vs 14 % retention). Finding 3 in kappa_b_lock.md is marked NOT
   CONFIRMED with its resolution appended. The M4.3 measurement stands;
   what fails is the inference from it.
2. **Amendment 3 (inertness falsifier) — verdict NOT INERT.** Conditions
   (i), (ii) and (iii) fail; (iv) holds. The reportable-negative-result
   branch is not taken. (i) fails on the strong grade at High
   (survival -0.0876, ranges disjoint, |delta| = 3.0 sigma_seed); the
   verdict does not rest on (ii), which fails only weakly and in
   inconsistent directions.
3. **Amendment 1 (drift check) — lock re-validated, no action.** Medium
   detection at the locked kappa_B reads 0.4465 under the 500-update
   policies, inside the [0.4, 0.7] band and slightly further from its
   floor than the 200-update probes. kappa_B = 1.0 stands.
4. **m31b watch item (carried from Phase 3): recommend CLOSE.** No
   fire-free coverage deficit at Medium under obs v3; completion rises
   with burnt_fraction rather than falling. Human call, flagged not
   taken.

**Open items for the human, neither actioned:** (a) matched kappa_B = 0
renders exist only at Medium per amendment 4c, but the headline result
is at High — a matched High pair is ~2 GPU-min; (b) the Low survival
reversal (+0.0059, opposite sign to High) is at 1.16x its own threshold
on two seeds and is recorded as a hypothesis, not a result.

PHASE 6 ENTRY GATE (do not start Phase 6 without executing this line):
Re-read D6-proposal with the RA. Decisions owed before any Phase-6 run:
(1) dose-response design formalized into the phase prompt;
(2) pilot scoped (2 mixture points);
(3) one-paper vs two-paper fork scheduled for after the pilot.


## Phase-5 pre-flight rulings (human + RA, 2026-07-28) — Q1–Q6 raised before M5.0

Issued in response to six questions raised on reading `phase5_prompt.md`,
before any Phase-5 code was written.

1. **Q1 — courier variant adopted** as the gated M5.2 validation. Reward
   keyed to *agent 1* reaching the goal (agent 2 scouts, cannot score);
   agent 1 blinded to the agent-occupancy plane (required for exactness —
   stigmergic leakage would reopen a side channel). Under this variant the
   denied optimum is 1/2 + q/2 and VoC = 1/2 (1 - q) is exact against it.
   The **any-agent coverage policy is also measured** as a reported third
   curve — flat at ~1 under total denial — labeled "redundancy substitutes
   for communication": a real swarm result, not a disclosure burden.
   Cause: the original Remark 2 denied baseline was an **RA theory error**
   (role splitting achieves 1 with no message). Theory doc amended by the
   author as **Remark 2′**; original Remark 2 marked superseded in part.
2. **Q2 — T = d + ell + ell_f approved** under fire-anchored scout
   semantics (Remark 2's T = d + ell + 1 is the ell_f = 1 case). Binding
   requirement: the horizon is **derived in code from the lethality
   semantics and asserted**, never hard-coded, so a change to the lethal
   region fires the assert. The delta = 1 scripted agent 1 is pinned to
   M4.2's exact commit schedule so q is the M4.2 curve literally; the
   unused slack is caveated in the report.
3. **Q3 — stop-gradient message path approved** (option (a): delivered
   aggregate stored in the PPO batch). Documentation requirement, code and
   report: under (a) the message head is a **frozen-at-init random
   projection of trained trunk features** — receivers can learn to decode
   it (random projections preserve information), but nothing optimizes the
   encoding. **DIAL-style differentiable comms (b) is pre-registered as
   item #1 of the M5.3 null-branch discussion.** Cheap first; escalation
   only through the human branch.
4. **Q4 — checkpoint provenance.** Owner to confirm whether the vast box
   or a local checkpoint archive survives (tar.zst + sha256 per the M3.0
   tooling rule 3c). **Retrain-then-render is pre-authorized either way**
   so the pre-task does not block. Finding at ruling time: no `*.tar.zst`
   or `*.sha256` exists in the repo tree, and `run_m44_grid.sh:128` states
   "ckpt_* dirs stay on the box" — so M4.4 did **not** produce a local
   archive. Flagged as a discipline lapse; rule 3c's text is not present
   anywhere in the repo, so its exact requirement could not be verified.
5. **Q5 — R_comm sweep extension pre-authorized**: {6, 8, 10, 12, 16} ->
   add {20, 24, 28}. *Measuring more of a curve is covering the range;
   moving bands is band-shopping — only the first is authorized.* M5.4's
   R_comm step is **converted to curves-first**: both measured curves
   (mean alive out-degree, P(swarm connected)) come to the lock STOP
   across the full sweep regardless of band intersection; the bands are
   priors to be ranked there. M4.3 precedent institutionalized.
   Accountability: the [2, 5] / [0.3, 0.7] bands were written without the
   geometry arithmetic (uniform 12 agents on 64^2 gives mean degree ~0.41
   at R = 6 rising to only ~2.22 at R = 16) — a violation of the author's
   own post-M4.4 pre-flight commitment, logged.
6. **Q6 — three defaults approved**: `p_link_max` retired with a DECISION
   note under the hard-range kernel; directed links with out-degree
   reporting (documenting that 0 < delta < 1 permits **asymmetric
   delivery** — physically legitimate, fading is directional); agent-plane
   blinding for E2C-2 agent 1.

**Open, raised at ruling time, not actioned** (Remark 2′ wording; see the
M5.2 objections in-session): (a) with slack ell_f the courier-variant
denied agent can *buy information by waiting at the branch*, so the true
denied optimum is 1/2 + q~/2 with q~ >= q measured over a d + ell_f step
pre-commitment window — "true denied optimum" in Remark 2′ (ii) holds for
the commit-at-branch policy class, and a "denied + dawdle" fourth curve is
proposed to measure the gap; (b) Remark 2′ (i)'s zero-VoC claim needs the
qualifier "at least as many interchangeable expendable agents as
hypotheses, with no death cost" — 3 corridors and 2 agents restore
positive VoC, and dp = 0.5 in the swarm env prices redundancy.

## Phase-5 pre-flight rulings, round 2 (human + RA, 2026-07-28)

Issued on the objections raised against the round-1 rulings, still before
any Phase-5 code.

1. **Dawdle residual — CONFIRMED as a second overclaim in the same remark,
   same author.** At large kappa_B, q ~ 3p vs q~ ~ 5p, i.e. ~1.67x exactly
   where the VoC figure lives (M4.2 Option-A pre-commitment distances 2.83
   / 2.24 / 2.00, plus two idle draws at the branch distance 2.00). **Fix
   = measure**, approved as proposed: a fourth scripted M5.2 curve,
   "denied + dawdle" (idle ell_f steps at the branch, commit on best
   evidence), with its own MC prediction from the shared machinery over
   the d + ell_f window. The **acceptance gate stays on the pinned-
   schedule curve** (protocol-matched, exactly predictable). VoC is
   reported two ways: VoC_gated = 1/2 (1 - q) labeled protocol-matched,
   and VoC_true = 1/2 (1 - q~) as measured. ~1 CPU-hour authorized. The
   one-clause reword-around was **rejected**: "we don't paper over a soft
   spot the original remark was just corrected for."
2. **Remark 2″ — second author's amendment**, transcribed into
   `docs/theory_foundations.md` with a dated banner on 2′(ii). Wording
   objection (i) accepted **including the deficit formulation** (VoC under
   team-any reward scales with the hypothesis-count-minus-agent-count
   deficit; death costs price redundancy) as a better theorem-shaped claim
   than "zero".
3. **Q2 assert — placement changed**: the probe-scout death check
   (scout dies at step d + ell_f) goes in `che/tests/test_e2c.py` as an
   executable **fast** test, not a runtime assert — env code is jitted and
   asserts there are stripped or awkward. Same teeth, better home. The
   derived horizon (T = d + ell + ell_f, computed from the lethality
   constants, never hard-coded) stands.
4. **Q4 — "tooling rule 3c/3d" was a phantom.** Owner's finding: it was a
   chat directive from the checkpoint incident; items (a)/(b) and the
   gitignore landed, (c)'s archive half and (d)'s CLAUDE.md transcription
   never did, and it was cited afterwards as repo law without verification.
   Three-part fix, all executed this session:
   (1) the artifact-persistence rule is now in `CLAUDE.md` — every GPU run
   persists metrics + provenance + a checkpoint archive (tar.zst + sha256
   recorded in the phase report) off-instance before release, and grid
   scripts assert it;
   (2) `run_m44_grid.sh`'s "ckpt_* dirs stay on the box" line is
   **retro-flagged in place** as the violation it was — it is why the
   matched High control needs a retrain;
   (3) **new meta-rule in `CLAUDE.md`: a chat ruling binds only once
   transcribed into `decision_log.md` or `CLAUDE.md` in the same session.**
   Untranscribed directives are proposals; citing one is an error. *That
   last rule is the actual lesson.*
5. **Pre-task — GREENLIT** on the retrain-then-render path.
   `che/scripts/run_p5_pretask_high_kb0.sh` is the first script written
   under the persistence rule: it retrains High / kappa_B = 0 / seed 0,
   **verifies reproduction** against the committed M4.4 eval JSON before
   the renders are trusted as a matched control, renders episode seeds
   0-5, then archives (tar.zst + sha256 + provenance) and **fails the run**
   if the archive is missing. Phase-5 checkpoint dirs and archives are
   gitignored; the `.sha256` and `provenance.txt` are committed.
   M5.0 follows.
