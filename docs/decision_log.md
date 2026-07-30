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

## Phase-5 pre-flight rulings, round 3 (human + RA, 2026-07-28) — M5.0 accepted

M5.0 (e7dd62e) **accepted at its STOP**. All three objections raised against
the round-2 rulings are ruled and approved.

1. **Remark 2‴ — the 5/3 clause is struck.** `q~/q -> 5/3 as kappa_B -> inf`
   was wrong: the five draws do not share an exponent (optical depths 0.71,
   0.90, 0.99 for the M4.2 pre-commitment draws; 1.10, 1.17 for the two
   branch-idle draws), so the lowest-depth draw dominates both products and
   the ratio tends to **1**. The gap peaks at moderate kappa_B and vanishes
   at both ends. The VoC correction runs the other way — VoC lives in 1 - q,
   so the relative bite is largest at **low** kappa_B, and the corrected
   curve is *steeper*, not merely shifted. Theory doc amended in place with
   a dated banner; **constants deferred to M5.2**, which measures q and q~
   on one grid through the shared MC machinery.
   *Accountability, both ways:* the heuristic originated with the builder,
   who offered `q ~ 3p` vs `q~ ~ 5p` as a small-p, equal-exponent estimate
   and did not label the assumption; it was then hardened into an asymptotic
   claim in transcription by the RA and written into the theory doc. Three
   corrections to one remark in one day — all caught pre-measurement.
   New **CLAUDE.md sub-rule**: numerical claims enter documents *derived*,
   never transliterated from chat heuristics; if a constant cannot be
   derived on the spot, state the inequality and defer it to the milestone
   that measures it. Binds both roles.
   *Model provenance for the record* (not doc constants): the per-step
   optical-depth model that produced the correction reproduces the measured
   E2C q at three points — 0.810 / 0.770 / 0.699 predicted against 0.812 /
   0.762 / 0.694 measured at kappa_B = 1.0 / 1.11 / 1.3 (kappa_b_lock.md).
   It estimates ratio ~1.13 at the locked kappa_B and a peak ~1.25-1.3 near
   kappa_B 2-3. M5.2's MC is the authority; these are the estimates that
   justified spending the CPU-hour, nothing more.
2. **Dawdle — the bound becomes an equality.** M5.2 enumerates the **full
   open-loop idle-placement family** (all ways of spending the ell_f idle
   steps before commitment), reports the max, and states the two-line
   open-loop-optimality argument, so `1/2 + q~/2` is the denied optimum
   rather than a lower bound on it. The Q2 scout-death check is a **@fast
   test in `che/tests/test_e2c.py`** (scout dies at step d + ell_f), not a
   runtime assert; the derived horizon T = d + ell + ell_f stands.
3. **M5.3 gains a shuffled-message arm.** Sender identities are permuted
   within the step, preserving the delivery pattern and the marginal content
   distribution while destroying who-said-what. Pre-registered verdict
   labels:
   - live > shuffled  -> **sender-specific content used**;
   - live ~ shuffled > zeroed -> **connectivity / global content only**;
   - all three indistinguishable -> **null branch** (architecture goes to
     the human discussion; DIAL-style differentiable comms is item #1).

### Git reconciliation note (same session)

Executed against the *measured* repository state, which differed from the
state assumed when the reconciliation was ordered — recorded because the
difference changed what was done:

- `fe98e02` was already an ancestor of local `main`; the branches had not
  diverged (`main` was 2 ahead, 0 behind). The merge was a no-op and the
  anticipated `decision_log.md` conflict could not occur.
- `integrity-audit` (e636af4) already existed and already matched
  `origin/integrity-audit` exactly; nothing to push there.
- The PHASE 6 ENTRY GATE text existed **twice** (a stray indented copy
  inside the M4.4 amendments entry, and fe98e02's copy). Both removed and
  re-added once, as a top-level final section of this log so later appends
  cannot bury it. Content verbatim; position and heading are the only
  changes, and one line reverts it.
- `docs/architecture_decisions_v1.md` registered on `main` (88fa8e3),
  byte-identical to the `integrity-audit` copy; sha256 recomputed after the
  copy rather than transliterated from the ruling text.

## M5.1 STOP rulings (human + RA, 2026-07-28) — gate re-anchored, Phase-4 claim restated

Issued on the M5.1 bench findings. Transcribed before any of the runs they
authorize.

1. **The gate — non-activation UPHELD, on narrow ground.** The standing
   rule's "activate, don't ask" exists to prevent *renormalization*: moving
   the line when a valid trigger fires. Challenging the INSTRUMENT is
   different in kind, and was backed by direct evidence (training
   throughput unchanged, 68,598 -> 68,475 env-steps/s, across the exact
   interval the M4.0/M4.4 channels landed). A line defended against
   renormalization must still be attached to a measurement that means what
   the rule assumed, and "env-only throughput" has been shown not to exist
   as a single quantity under XLA dead-code elimination.
   a. **M5.1c decomposition APPROVED** (~8 GPU-min, four keep-alive sets,
      no verdict computed — correct design).
   b. **The gate is RE-ANCHORED.** The env-only ÷81 projection is retired
      entirely. The guarded quantity is DIRECTLY MEASURED population-
      aggregate training throughput at the Phase-6/7 reference
      configuration (`configs/gate_pop12.yaml`, measured by
      `pbt.py --bench` — the instrument that produced Phase-0's 159.0 k, so
      the number is comparable to it and to the 100 k line with no
      projection in between). Training is what spends the budget, so
      training is what the line guards. Env-only rows are demoted to
      diagnostics and must declare their keep-alive set forever after.
   c. **PRE-COMMITTED, no further appeals:** if the direct measurement
      lands under 100 k, uint8 activates in that session, mechanically. The
      instrument challenge has been heard exactly once; the next trigger on
      the re-anchored number is final.
   d. **Determinism priced** while the box is up: one short run under XLA
      deterministic flags (deterministic ops + autotune off), plus — added
      in implementation — a verification that the flags actually
      determinize, since pricing a knob without checking it works is how
      the ÷81 projection survived three phases.
2. **The Phase-4 claim — RESTATE, not retract wholesale.** The survival
   half is *strengthened* by replication (direction 3/3, magnitude −0.05 to
   −0.11, several times the measured noise floor); the completion half is
   UNRESOLVED, not reversed. Dated correction note appended to
   `phase4_report.md` (never a silent edit), withdrawing "completion
   intact", restating it as "no completion effect resolvable above the
   reproducibility floor", and retracting all "|Δ| = k·σ_seed" phrasings
   project-wide in favour of intervals and measured floors. The asymmetry
   headline survives in honest form: survival clearly moves; completion
   does not clearly move.
3. **M5.5 falsifier — REVISED NOW,** as a dated pre-registration amendment
   *before* the grid it governs.
   a. **Mini replication study approved** (M5.1e): 4 identical re-runs of
      one cell, same seed, same config, ~20 GPU-min, so the floor is a
      measured distribution rather than an n = 1 anecdote — the two pre-task
      arms disagreed about their own noise, which is the reason.
   b. Falsifier condition (i) becomes **"within the measured
      reproducibility floor (replication study, cited)"**. Completion-based
      sub-claims are graded against their own floor and may return
      UNINFORMATIVE at 2-3 seeds; if so, the falsifier verdict rests on
      survival, delivery-rate and danger-moment channels, stated as such.
   c. **Propagates to D6** (appended to that entry): the dose-response power
      analysis uses the measured floor; the registered 4 seeds per mixture
      point are checked against it; if deterministic flags price at < 10 %,
      headline runs go deterministic.
4. **Accountability (human):** the ÷81 projection convention, and the rule
   wording that bound "activate" to it, were the author's constructs; the
   consumer-dependence of DCE'd throughput should have been flagged when the
   M4.0/M4.4 channels landed unbenched. New CLAUDE.md rule: *throughput
   gates bind only to measured training throughput of the spending consumer;
   any env-only figure states its keep-alive set; projections are estimates,
   never triggers.*
5. **Housekeeping:** the full suite goes green on this commit (box CPU or
   overnight local) before M5.2 opens. Machine constraint accepted, gap not
   carried forward.

**Transcription deviations, flagged not silent:** (a) the correction note
was dated **2026-07-28**, today, not the 2026-07-30 in the ruling text — a
report line post-dating its own commit would be self-refuting provenance in
a document whose subject is provenance; one line reverts it if the later
date was deliberate. (b) Ruling 1c's "activates in that session" is only
executable if the uint8 code exists *before* the session — it does not yet.
Raised with the scripts.

## PHASE 6 ENTRY GATE (human, 2026-07-28) — owed before any Phase-6 work

PHASE 6 ENTRY GATE (do not start Phase 6 without executing this line):
Re-read D6-proposal with the RA. Decisions owed before any Phase-6 run:
(1) dose-response design formalized into the phase prompt;
(2) pilot scoped (2 mixture points);
(3) one-paper vs two-paper fork scheduled for after the pilot;
(4) [appended 2026-07-28, ruling 3c] the dose-response power analysis uses
    the MEASURED reproducibility floor (M5.1e), not an assumed sigma. The
    registered 4 seeds per mixture point are checked against that floor
    before the pilot runs. If deterministic XLA flags price at < 10 %
    throughput (M5.1d row C), headline runs go deterministic: eliminating
    run noise outright is worth a modest slowdown in a project whose
    contribution is methodological credibility.

## Phase-5 delegated rulings (human 2026-07-29, RA-executed)

Human directive, verbatim in effect: *"You shall proceed with M5.2 if
there are important decisions this time I am handing them to you."* The
two decisions outstanding at the M5.2 STOP are therefore taken by the RA
and transcribed here before being acted on, per the meta-rule. Both are
reversible by the human; neither invents scope beyond the two items that
were explicitly parked.

### 1. Gate-config remedy — fallback-ladder rung 2, applied a second time

`gate_pop12.yaml` needs 49.31 GiB against a 31.8 GiB card and nothing
experiment-preserving fits (M5.1g probe; XLA's own remat pass reports it
cannot go below 28.31 GiB = 89 % of the card). This was parked as a
"scope decision". On inspection it is **not** a free choice: the
pre-agreed fallback ladder exists — in `phase0_substrate_prompt.md`, not
in the Phase-5 prompt, which is why it was not found earlier — and reads
"apply in order, re-measure after each; never skip to escalation while
rungs remain": 1) grid 64²→48²; 2) n_envs tuning for occupancy;
3) n_agents 12→8; 4) grid 48²→32²; 5) population 12→10 (M0.6 only).

Rung availability **now**, which is not what it was when the ladder was
written (nothing was locked in Phase 0):

- **Rung 1 (grid 64²→48²) — UNAVAILABLE.** β_c = 0.500 and the three
  severity levels were calibrated at 64² (Phase 2, `severity_lock.md`);
  percolation thresholds are finite-size dependent, so shrinking the grid
  invalidates that calibration and the Coupling-A/B locks that sit on it.
  Phase 0 skipped this rung too, and correctly.
- **Rung 2 (n_envs) — AVAILABLE, and already applied once**: Phase 0 moved
  1024 → 256 envs/member for this same reason (`phase0_report.md`,
  "Deviation applied (fallback ladder rung 2 — reported, not silent)").
  Applying it again gives 256 → 128 and a measured 24.69 GiB (78 % of the
  card). Touches no calibrated quantity — the environment, the task and
  every locked θ are unchanged.
- **Rung 3 (n_agents 12→8) — UNAVAILABLE during Phase 5.** M5.4's R_comm
  band is *defined* at "reference density (12 agents, 64²)"; changing the
  agent count changes the observable the lock is measured against.
- **Rung 4** = rung 1. **Rung 5** is marked "M0.6 only".

**RULING: apply rung 2 again — `n_envs` 256 → 128 in `gate_pop12.yaml` —
and re-bench row B.** Reported, not silent, as the ladder requires.

Consequences recorded because the ladder demands it:

- The ladder's "**never** silently reduce planned experiment steps" binds:
  halving envs/member halves env-steps per update, so Phase-6/7 runs at
  this config take **1000 updates, not 500**, to preserve planned steps.
  Total steps and therefore budget are unchanged if throughput holds —
  which is why the ladder says re-measure, and row B must now be
  re-measured before any Phase-6 costing is quoted.
- We are now **8× below the Phase-0 reference n_envs** (1024 → 128). That
  is a fact for the Phase-6 entry gate to weigh, not a blocker here.

**Considered and rejected: `n_minibatches` 4 → 16** (18.66 GiB, the most
headroom of any candidate). It is not on the ladder, it is not reported
anywhere as a deviation mechanism, and it changes the optimization
(sixteen smaller gradient steps per epoch instead of four) without any
pre-agreement about what that does to PBT selection. Preferring an
unlisted knob because it measures better is precisely the
band-shopping the M4.3 precedent forbids.

### 2. Remark 2‴'s deferred constants — written in

Remark 2‴ states its constants "are deferred to M5.2, where q and q̃ are
measured on the same grid by the shared MC machinery; no numeric ratio
belongs in this document before then." M5.2 has now measured them, in
this session, by that machinery — so the sub-rule on numbers entering
documents *derived* is satisfied, and the deferral has been discharged.

**RULING: amend Remark 2‴ in `docs/theory_foundations.md` with the
measured constants.** Theory-doc edits are a Phase-5 non-goal; this edit
is authorized by the delegation above and is confined to discharging a
deferral the document itself created. No other theory text is touched.

Measured (analytic, MC-free where the asymptotics are claimed): q̃/q
peaks at **1.235 near κ_B ≈ 2**, equals **1.126 at the locked
κ_B = 1.0**, and → 1 at both ends. The struck 5/3 = 1.667 claim exceeds
the measured maximum anywhere on the grid, confirming the strike. The
relative VoC correction is largest at low κ_B: 79 % of VoC_gated at
κ_B = 0.5, 54 % at 1.0, 7 % at 3.0.

## Phase-5 delegated rulings, round 2 (human 2026-07-30, RA-executed)

Human directive, verbatim: *"You are given creative freedom moving
forward for this problem"*, issued on the row-B failure after the M5.3
report section was accepted. Decisions taken under that delegation are
transcribed here before being acted on, per the meta-rule. All are
reversible by the human.

### 1. The gate requirement DRIFTED, and the drift invalidates the rung-2 arithmetic

Measured, from two committed GPU artifacts on the same card with the same
`--xla_gpu_autotune_level=0` flag:

| config: envs 128 / pop 12 / nmb 4 / uint8 / remat off | temp GiB | total GiB |
|---|---|---|
| `m51g/memprobe.json`, candidate `envs128` (fa32113, 2026-07-28) | 24.5467 | **24.6872** |
| `m51i/memprobe_rung2.json`, `baseline` (dbdb15c, 2026-07-29) | 27.3944 | **27.5349** |

**+2.8477 GiB, +11.53 %, for a byte-identical configuration.** In the same
pair of runs `jax.checkpoint` went from saving 2.09 GiB to saving 5 KB
(27.394371 → 27.394376), so what changed is *activation retention*, not
merely a level.

Consequences, which is why this is a ruling and not a note:

- The delegated rung-2 ruling of 2026-07-29 chose `n_envs` 256 → 128 on the
  strength of "24.69 GiB (78 % of the card)". At the measured 27.53 GiB it
  is **87 %** of a 31.8 GiB card. The rung is still the only available one
  and the choice does not change, but the *headroom claim* attached to it
  was wrong by 2.85 GiB.
- `run_m51i_gate_rung2.sh` sized `XLA_PYTHON_CLIENT_MEM_FRACTION=0.95`
  as "30.2 GiB for a 24.69 GiB requirement" — 5.5 GiB of slack. The real
  slack is 2.7 GiB, 8.8 % of the arena, which BFC fragmentation can
  plausibly consume.
- **`m51i/verdict.txt`'s framing is therefore NOT ESTABLISHED.** It says
  "Rung 2 already cut the requirement 49.31 → ~24.7 GiB, so a failure here
  is about how the row is measured, not about whether the rung worked."
  Against 27.53 GiB the failure may be capacity after all. The artifact is
  **not edited** — run artifacts are immutable; the correction goes in the
  phase report, which is the document of record.

**RULING: the 24.69 GiB figure is corrected to the measured 27.53 GiB
wherever it is load-bearing** — `phase5_report.md` (dated correction note,
never a silent edit, M5.1 precedent) and `gate_pop12.yaml`'s header — and
the "78 % of card" claim is retracted in favour of 87 %.

*Accountability:* this is the ÷81 pattern one level down. A number was
measured once, written into a config header and a ladder decision, and
then cited for two milestones while the thing it measured moved
underneath it. It was the RA's number and the RA's citation both times.

### 2. Row B gets an instrument, not a fourth attempt

Three attempts have produced three artifacts and no rate: an OOM at
49.08 GiB (m51d), a bounded OOM after 1112 s retrying a fixed 5.72 GiB
allocation (m51i, first), and `rc=137` at the 1800 s backstop (m51i,
second). The last one carries **no diagnostic at all** — a bare SIGKILL
cannot distinguish an allocator-retry loop from a genuine hang from host
swap, and re-running the same command measures the same unknown again.

**RULING: no further row-B attempt without staging and sampling.**
`che/bench/rowb_probe.py` + `run_m51j_rowb_diagnostic.sh` run the ladder
`init → compile → one chunk → windows`, each stage timed, flushed and
guarded on its own, with device `memory_stats()` reported at every stage
and on failure, and a 5 s background sampler recording GPU memory,
utilisation and process RSS. A kill at any point then leaves a trail
instead of a return code.

### 3. Code vs toolchain is decided by a 2×2, not by argument

The local CPU bisect (this session) cleared what it could and named what
it could not:

- reverting the M5.1h dequantize hunk changes the compiled temp by
  **0.00 MiB**;
- `msg_mode` moves it by 0.14 MiB at probe scale, ~54 MiB scaled to the
  gate — it cannot be 2,848 MiB;
- probe **order** inside one process: 0.00 MiB (`lru_cache` eviction
  cleared);
- **candidate path vs baseline path** for the identical config: 0.00 MiB
  (so m51g pricing `envs128` 7th and m51i pricing it 1st is not the
  difference).

CPU fusion is not GPU fusion, so a null on this backend does not clear a
suspect on the box — M5.1h in particular touches the differentiated
forward path, where a multiply-by-literal and a divide can fuse
differently on GPU only. What remains is exactly two candidates: a
GPU-specific fusion change from one of the five commits, or a **toolchain
change between two rentals**, which no provenance file records.

**RULING: the diagnostic job settles it with two compiles** — memprobe at
HEAD and at fa32113 (git worktree), on the same box, same flags, same
session. Old code reading 24.69 ⇒ the code moved it; old code reading
27.53 ⇒ the toolchain moved it and the five commits are innocent.

### 4. Provenance must record the toolchain (proposed rule, human to ratify)

A memory requirement compared across two rentals without the jax/jaxlib/
CUDA/driver versions is not a comparison — it is the env-only-throughput
mistake in a different unit. `memprobe.py` now records them in its JSON
and the diagnostic script prints them first.

**Proposed for `CLAUDE.md`, NOT written there by the RA:** *every
measurement persisted off-instance records its toolchain (jax, jaxlib,
CUDA, driver, device, host RAM) alongside the git commit; a figure
compared across instances without them is a diagnostic, not a
measurement.* Flagged for human ratification because CLAUDE.md rules have
been human-issued to date.

### 5. Scope, stated so it cannot drift

Row B guards **Phase-6/7 spending only**. No Phase-5 milestone uses the
population path (M5.3–M5.5 are single-learner runs at the severity
operating point, and that path is healthy at 68.5 k steps/s). The gate
number is owed to the **Phase-6 entry gate**, which is already blocked on
four other decisions. The diagnostic job is ~15 GPU-min; if it lands
without a rate, the finding goes to the entry gate and row B is not
attempted again in Phase 5.

**The 100 k line is not renormalized here, and no experiment quantity is
touched.**

### 6. Recorded as unpriced, NOT implemented: sequential population groups

The ladder's remaining rungs all move calibrated quantities, and the
off-ladder knobs (`n_minibatches`, `pop_size`) change the optimization or
the design. There is one option in the class `remat` belongs to —
mathematically neutral, same hyperparameters, same updates, same PBT
selection, trading wall-clock for memory — that nobody has priced:
**evaluate the population vmap in G sequential groups** (`lax.map` /
scan over groups of `pop_size / G`) instead of one 12-wide vmap.

Estimate, labelled an estimate per the derived-numbers sub-rule: the
measured `pop6` candidate is 13.77 GiB, so two groups of six should peak
near 13.9 GiB (pop6 plus the full population's 0.14 GiB of state), at
roughly 2× the update-phase wall clock. **This is arithmetic from
measured numbers, not a measurement**, and implementing it is a
Phase-6-entry-gate decision, not an RA one. Recorded here so the entry
gate sees an experiment-preserving option beside the ones that cost
calibration.

## Hardware split (human, 2026-07-30) — big card for Phase 5, 5090 for Phase 6/7

**Human decision:** finish Phase 5 on an RTX PRO 6000 Blackwell (96 GB) at
~$1.00/h; spend Phase 6/7 on a 5090 at ~$0.40/h.

Cost basis, derived here from the committed budget line (86e9 steps;
cost = $/h × 23,888,889 / rate): the required rate to keep 86e9 steps
inside $150 scales linearly with price — 71.7 k steps/s at $0.45/h,
239 k at $1.50/h. Two same-generation Blackwell cards of comparable
bandwidth will not differ by 3×, so the cheap card wins the bulk spend by
a wide margin. Phase 5's remaining GPU work is a few hours, so the
premium there is a couple of dollars. The split is sound; what follows
are the obligations it creates, none of which are optional.

1. **The gate still binds to the 5090.** CLAUDE.md: throughput gates bind
   to measured training throughput of the *spending consumer*. Phase 6/7
   spends on the 5090, so no PRO 6000 rate can stand in for row B — the
   verdict script detects the device and refuses to compare a non-5090
   rate to the 100 k line. What the big card produces instead is the
   **minimum viable arena** (M5.1j section 3), which decides whether
   renting a 5090 for Phase 6/7 is worth doing *before* it is rented.
2. **The M5.1e reproducibility floor is CARD-SPECIFIC and must be
   re-measured.** The floor (completion 0.0145, survival 0.0129) was
   measured on the 5090, and M5.5's pre-registered falsifier condition (i)
   reads "within the measured reproducibility floor (replication study,
   cited)". Grading M5.5 against a floor measured on different hardware is
   the same defect M5.1j just caught one level up — a number cited past
   the conditions it was measured under. **RULING: if M5.4/M5.5 run on the
   PRO 6000, `run_m51e_replication.sh` is re-run there first** (4 runs,
   ~20 GPU-min, ~$0.35) and M5.5 cites that floor. Same 3-dof, ±40 %
   caveat applies to the new estimate.
3. **No comparison may straddle cards.** Every arm of a comparison runs on
   one card. Two consequences, both satisfiable: M5.4 evaluates M5.3's
   5090-trained checkpoints, which is eval-only and internally consistent
   as long as *all* δ arms are evaluated on the same card; and M5.5's
   message-usage re-check is internal to M5.5's own δ = 0 policies, so it
   does not reach back to the 5090-trained M5.3 arms.
4. **M5.3 is closed on the 5090 and is not re-run.** Its three arms were
   CRN-paired on one card, which is what its verdict rests on. A card
   change does not reopen it.
5. Provenance already records the device (M5.1j); with the split in force,
   **every Phase-5 result from here states its card in the report table**,
   not only in the artifact.
