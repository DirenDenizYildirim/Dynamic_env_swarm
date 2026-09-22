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

## M5.3 null branch settled (human, 2026-07-30) — the gate is re-sited at High

The M5.3 STOP required a human discussion before any lock. Held; the
decision is **re-site the utility gate at High severity (M5.3b)** before
either accepting the null or building DIAL.

**Basis — the gate was run where its own mechanism measures zero.** M4.4
Result 1 measured Coupling B's effect per severity:

| severity | Δsurvival (κ_B 0 → 1.0) | verdict | masked at danger | danger rate |
|---|---|---|---|---|
| low | +0.0059 | strong (1.16× threshold, 2 seeds) | 0.0809 | 0.0068 |
| **medium** | **−0.0003** | **within noise** | 0.0560 | 0.0396 |
| high | **−0.0876** | **strong**, deaths_fire ×2.6 | **0.2424** | 0.0621 |

M5.3 asked whether neighbours can supply information the hazard withholds,
at the severity where our own prior measurement says the hazard withholds
nothing. The phase prompt's stated expectation ("masked perception at
Medium leaves information on the table that neighbours can supply") is
contradicted by M4.4's Medium row, which predates it.

**This is covering the range, not band-shopping** (M4.3 precedent, as
institutionalized for R_comm by the Q5 ruling): no threshold, label or
grading rule moves. **Medium's null stands as reported, is not superseded,
and both cells are reported together whatever High returns.**

**What M5.3 established that re-siting does not disturb:** zeroed ≈
shuffled (0.10–0.22 of the bar). Had sender identity carried anything,
shuffled would sit between live and zeroed; it sits on zeroed. **No
sender-specific content is used at Medium**, independent of why.

**DIAL (item #1) is deferred on a dependency, not rejected.** It fixes
*what gets said*; whether the encoding binds cannot be measured in a cell
with nothing to encode, so a differentiable channel at Medium would return
the same null for the same reason. Even if built, it has to be evaluated
at High to be interpretable — so High precedes it on either path.

**Design, fixed before the numbers exist:**

1. **Floor first.** The M5.1e floor is Medium-specific *and* card-specific;
   M4.4's σ_seed at High (0.0227 / 0.0295) is 2–4× Medium's (0.0107 /
   0.0072). So a High reproducibility floor is measured **on the same card,
   before the gate cells run** (4 identical runs, same seed), and the
   verdict grades against *that* file rather than a transcribed constant.
   M5.3's script hardcoded the Medium floor; M5.3b reads the measured one.
2. **3 seeds, not 2**, per the M4.4 precedent that approved a third seed
   where variance is large.
3. **Cell A (verdict cell):** High, δ = 0, R_comm = 8 — one change from
   M5.3, so the comparison is attributable.
4. **Cell B (sensitivity cell):** High, δ = 0, R_comm = 16. At High the
   swarm loses agents, so the comms graph is *sparser* exactly where the
   need is greatest; High raises demand and cuts supply at once. Cell B
   separates "no content is useful" from "no one was in range to hear it",
   and it feeds M5.4's R_comm lock directly.

**Pre-registered labels, all three fixed now:**

- **A separates** (live > zeroed by > 2× the measured High floor on
  completion or survival) → comms is load-bearing where perception fails;
  Remark 2's prediction confirmed at swarm scale; proceed to M5.4.
- **A null, B separates** → the binding constraint is **connectivity**, not
  content or regime. R_comm becomes load-bearing rather than a plumbing
  default, and M5.4 must lock it where the channel is usable. Reportable
  finding either way.
- **A and B both null** → the null is regime- and connectivity-independent
  across the tested range, and the reading returns to Remark 2′(i):
  redundancy substitutes for communication, as M5.2's coverage arm measured
  (J = 1 under total denial with interchangeable agents). At that point the
  human chooses between accepting it as a reportable negative and building
  DIAL — with two cells of evidence instead of one.

Cost ~2.2 GPU-hours (~$2.20 at the PRO 6000 rate): 4 floor runs + 2 cells ×
3 arms × 3 seeds, CRN-paired evals throughout.

## M5.1j outcome (RA, 2026-07-30) — three findings, one of them budgetary

Measured on an RTX PRO 6000 Blackwell, jax/jaxlib 0.11.0. Full record:
`phase5_report.md`, "M5.1j results". Recorded here because two prior
rulings are superseded by measurement and one budget line is retired.

1. **The requirement drift was the TOOLCHAIN.** fa32113 and HEAD measure
   27.534881 / 27.534886 GiB on the same box today, and today's figure
   matches m51i's 27.534882 *on a different GPU*. Two cards agree, two dates
   do not. The five commits between m51g and m51i are cleared; ruling 3 of
   the round-2 delegated rulings is discharged.
2. **Row B was never broken — `--xla_gpu_autotune_level=0` was.** With it:
   1036 s per chunk, 3,795 steps/s, 27.53 GiB. Without it: 63 s, 62,186
   steps/s, 61.56 GiB *at compile*. The autotuner's scratch is what never
   fit a 5090; disabling it bought a fit at 16.4× the cost, and three
   attempts were then spent diagnosing that cost behind guards sized for
   the OOM the flag had removed.
   **Consequence: the hardware split ruled earlier today is SUPERSEDED.**
   Phase 6/7 cannot run on a 5090 at this configuration — autotuning on
   OOMs at 31.8 GiB, autotuning off costs 6,295 GPU-hours.
3. **The budget was computed from the wrong configuration.** The "86e9
   steps → 167.7 GPU-h, ~$151" line came from row A, which runs
   `m06_probe.yaml` at obs_window 5 — superseded at M1.2. The real
   Phase-6/7 configuration measures 62,084 steps/s (IQR 25), so it needs
   **384.8 GPU-hours**: $173 at $0.45/h, $385 at $1.00/h, against a
   $150–215 total budget. **RULING: the $151 figure is retired.** No
   replacement is set here — the entry gate recomputes it, because the
   remedy (cheaper card vs cheaper configuration) changes the number.

**The 100 k line is NOT renormalized.** The measured 62,084 sits below it;
the pre-committed contingency (uint8) is already active, so the ladder is
exhausted and this is a Phase-6-entry-gate decision, exactly as ruling 1c
anticipated. Noted for that gate: the measurement is not on the spending
consumer, and what the spending consumer will be is now itself open.

**Proposed for `CLAUDE.md`, NOT written there by the RA** (same handling as
the toolchain-provenance proposal): *every throughput figure states the XLA
flags it was measured under, exactly as it must state its keep-alive set. A
rate without its flags is not a measurement* — 3,795 and 62,084 steps/s are
the same code, the same card and the same day.

## M5.3b outcome (RA, 2026-07-30) — pre-registered branch 3 taken, decision owed

Both cells null. No pairwise difference reaches 0.65× the bar in either
cell. Full record: `phase5_report.md`, "M5.3b". No ruling was made here —
the branch was fixed in advance and the data selected it.

1. **Connectivity is eliminated.** Cell B tripled mean alive out-degree
   (1.01 → 2.99, delivery 1.0000) and changed nothing. That was the cell's
   pre-registered purpose and it discharged it.
2. **The completion difference flips sign between cells** (−0.0338 at
   R = 8, +0.0354 at R = 16), which is noise with a sign rather than a
   mechanism.
3. **The High floor is the milestone's most consequential number:**
   completion sd 0.0522, survival 0.0621 — 3.6× and 4.8× the Medium floor.
   Measured before the arms were compared, so it could not be chosen after.

**Correction the RA owes on its own recommendation:** re-siting at High was
argued on the mechanism being 4.3× stronger there. It is, but the floor is
3.6–4.8× larger, so the bar rose in step and **High is worse powered than
Medium, not better** — Medium bounds the effect at < 3 points, High only at
< 11. Reaching Medium's bar at High needs ~46 seeds per arm. The noise side
should have been checked before the recommendation was made.

**Owed to the human, not actioned:**

- The pre-registered choice: accept the null as a **reportable negative**
  (Remark 2′(i) confirmed at swarm scale) or build **DIAL**. If DIAL, it
  must be evaluated at **Medium** — High cannot resolve a comms-scale
  effect at any affordable seed count.
- **Downstream:** M5.4 locks δ and M5.5 ablates it. Both assume δ removes
  something the swarm uses. On two severities and two connectivity regimes
  that premise is now unsupported, so the Phase-6/7 element set may be
  {Coupling A, Coupling B} plus a δ that is inert by construction.
- **A power ruling worth making beyond comms:** M4.4's High survival result
  (−0.0876, graded "strong" against σ_seed = 0.0295 from two seeds) is
  **1.41× the measured High floor**, not 3σ. The direction survives (M5.1
  replication 3/3); the confidence language does not. M5.5's High cells at
  2 seeds inherit the same limit. Recommend: **grades cite a measured floor
  or declare themselves underpowered.**

**M5.4 datum recorded regardless:** R_comm = 16 gives mean alive out-degree
2.99–3.37 under trained High policies, inside the [2, 5] prior band that
R = 8 (1.0) misses.

## M5.3 CLOSURE RULING (human + RA, 2026-07-30) — comms axis closed as a certified negative

Issued at the M5.3b STOP, on the third pre-registered branch (both cells
null). Transcribed before any of the work it authorizes.

### 1. Reportable negative ADOPTED

The null is certified as the **swarm-scale manifestation of Remark 2″(i)**:
redundancy substitutes for communication in a homogeneous, expendable
swarm.

**The load-bearing evidence is the unused CONNECTIVITY bit.** That signal
needs no encoder to be decodable — a receiver knows it heard from someone
without decoding anything — so its worthlessness is **demand-side** (the
swarm does not need the information) rather than **channel-side** (the
swarm cannot read the message). This is what makes the negative certifiable
rather than merely unmeasured, and it is why the frozen-encoder objection
does not rescue the channel.

**Hedge stated honestly:** `dp = 0.5` prices deaths, so the theory's
clean-zero conditions (interchangeable, *expendable*, ≥ as numerous as the
hypotheses) were **not fully met**. The measured null therefore also says
the deficit formulation's "value returns" term is **weak at this scale and
this death price** — a stronger statement than the clean-zero case would
have supported, and it belongs in the paper as such.

### 2. DIAL formally DECLINED — with reasons, because it was item #1

DIAL was the pre-registered first item of this discussion, so the
declination is recorded with its grounds rather than by omission:

(a) **The demand-side evidence above.** The channel's cheapest,
    encoder-free signal already goes unused.
(b) **A memory constraint not raised in the options:** DIAL's ~2× batch
    memory collides head-on with the m51g wall (XLA's own 28.31 GiB
    rematerialization floor against a 32 GB card). Building it means
    fighting the memory decision early and twice.
(c) **The capped upside** — with the honest caveat that a < 3-point cap
    measured on a *frozen random encoder* does not strictly bound a
    *trained* encoder.

**Paper limitation, carried explicitly:** *"gradient-shaped messaging
remains untested; the channel was a fixed random projection."*

Options 3 and 4 rejected: 3 (irreplaceable roles) re-runs the project
against the deadline; 4 (drop comms) amends registered scope to discard a
finding we can instead certify.

### 3. M5.4 FOLDED INTO THIS RULING — δ locked, bands void-by-null

The performance-cost δ bands are **void-by-null**: one cannot pick "the
smallest δ whose cost carries a strong grade" when the cost is ≈ 0 at every
δ. That is not a band failure to be re-shopped; it is the band's premise
being falsified.

- **LOCKED: δ = 1.0 by convention** — maximal denial, the cleanest element
  semantics for θ*.
- **R_comm locked on the geometric observable alone** (mean alive-degree
  band), with performance-insensitivity recorded beside it.
- `comms_lock.md` documents the void-by-null status **explicitly**. A lock
  that says *"this knob does nothing, and here is the certification"* is a
  legitimate lock.

### 4. M5.5 RESCOPED

Medium × δ ∈ {0, 1.0} × **4 seeds** — Medium is comms' best-chance cell per
Remark 2 and per the M5.3b severity comparison (Medium bounds the effect at
< 3 points; High only at < 11). Falsifier graded against the M5.1e
reproducibility floor with **its regime named**. Matched renders kept; watch
item is **branch-loitering / information-buying behaviour**. **Expected
verdict: INERT — and that expectation is the point. This run is
certification, not exploration.**

*RA flag, raised not resolved:* the M5.1e floor was measured on a **5090**,
and the hardware-split ruling of the same day requires a card-specific
floor. The two rulings interact. Cheapest reconciliation, adopted unless
overridden: **re-measure the Medium floor on the card M5.5 actually runs on
(4 runs, ~20 GPU-min, ~$0.35) and report both**, grading against the
same-card figure and printing M5.1e's beside it. Naming the regime is
satisfied either way.

### 5. D6 APPEND

With comms certified inert, the composition experiment is effectively over
**{Coupling A, Coupling B}**. **δ = 1.0 is retained in θ\*** for
registration fidelity at zero cost. The dose-response x-axis (A×B
co-active visitation) is unaffected.

## M5.5 outcome (RA, 2026-07-30) — falsifier failed on an RA-chosen threshold

**Verdict as computed: NOT INERT**, failing condition (iii) alone. Reported
as the instrument produced it; the script's own instruction ("do not
reconcile it here") is honoured — what follows is analysis for the human,
not a re-grade.

| δ | completion | survival | delivery | out-deg | fire/danger |
|---|---|---|---|---|---|
| 0.0 | 0.7396 ± 0.0195 | 0.9188 ± 0.0114 | 1.0000 | 3.213 | 0.00744 |
| 1.0 | 0.7358 ± 0.0131 | 0.9331 ± 0.0065 | 0.0000 | 0.000 | 0.00571 |

Conditions (i) and (ii) hold: Δcompletion +0.0038 and Δsurvival −0.0143
against bars of 0.0799 / 0.0260, and the knob provably moved (delivery
1.0000 → 0.0000, out-degree 3.213 → 0.000 — the empty graph `comms.py`
specifies).

**Condition (iii) failed at 23.2 % against a 20 % threshold that the RA
chose, and that threshold is finer than the quantity's own noise.** The
floor study — collected in Section 1, *before* the arms were compared —
gives fire deaths per danger agent-step across four identical runs as
0.00810 / 0.00408 / 0.00776 / 0.00688: **sd 0.00182, 27.2 % relative**. The
cross-arm difference of 0.00172 is **0.95× that floor sd**, and the δ = 0
arm's own per-seed spread (0.00517–0.01041) is wider than the difference
it is being compared against.

So the two readings are:

- **as operationalized by the RA** — 23.2 % > 20 % → NOT INERT;
- **as the human specified it** ("no cross-arm difference in danger-moment
  outcomes"), graded against the measured floor → 0.95 σ → no difference,
  and all three conditions hold → **INERT**.

**This is offered knowing it looks like special pleading after a failed
test.** Two things distinguish it: the floor data predate the comparison,
and the defect is structural rather than convenient — a threshold finer
than its own instrument cannot pass whatever the truth is. The RA does not
re-grade; the human rules.

**The systemic finding, and the fourth instance of it today:** a bar chosen
without a measured floor. M4.4's σ_seed (0.0295 vs a measured 0.0621 at
High); M5.3's hardcoded Medium floor applied to a different card; M5.3b's
2×sd bar at High, which no affordable seed count could reach; and now a
20 % relative threshold below a 27.2 % noise level. **Recommended ruling:
no acceptance threshold enters a script without a measured floor for the
quantity it grades, or an explicit statement that it is underpowered.**

**Floor note (the card reconciliation, discharged):** the Medium floor
re-measured on the PRO 6000 is completion sd 0.0399, survival sd 0.0130 —
survival matches M5.1e's 5090 figure (0.0129) almost exactly, completion is
2.75× larger (0.0145). The re-measurement therefore mattered for one metric
and not the other, which is why it was not assumed either way.

**Instance released** after all 12 checkpoint archives were pulled and
verified against their committed sha256 (12/12 OK). `workspace_is_volume`
was False, so nothing survives on the box; the archives are local and the
`.sha256`/provenance are committed.

## PHASE-5 CLOSE RULINGS (human + RA, 2026-07-30)

Issued on the M5.5 report. Transcribed verbatim in intent before action.

### 1. M5.5 verdict — condition (iii) is VOID, not failed

**The distinction is load-bearing.** A threshold set below its instrument's
measured floor cannot pass under the null; a test that cannot pass
regardless of the truth is not a test, and its output is not evidence.

Three clauses license the re-grade against the charge of special pleading,
and are stated explicitly in the report rather than assumed:

(a) the floor data **pre-date the comparison** — instrument calibration,
    not post-hoc rescue;
(b) the defect is **structural** — it would void a PASS identically;
(c) the **counterfactual is recorded**: had the 23.2 % exceeded the 27.2 %
    floor, NOT INERT would stand, and this ruling says so.

**FINAL VERDICT for the report, verbatim:** *"INERT WITHIN MEASUREMENT
RESOLUTION — conditions (i),(ii) pass against measured bars; condition
(iii) as-registered is retracted as structurally defective (threshold
20 % < instrument floor 27.2 %) and re-graded against the pre-dated floor:
23.2 % < 27.2 %, not resolvable. The inertness claim rests jointly on this
certification and on M5.3's demand-side mechanism evidence (the unused
connectivity bit)."*

The verdict-as-produced stays in the artifact with this adjudication
beside it — exactly as the RA left it.

### 2. Bars-with-floors rule — ADOPTED into CLAUDE.md, effective now

> *"No acceptance threshold enters any script without either a measured
> floor for the quantity it grades (cited) or an explicit UNDERPOWERED
> flag in its output. Thresholds finer than their instruments are void by
> construction."*

**Accountability, split honestly.** The four invented constants are the
builder's. The framework that requested conditions without specifying how
their bars derive is the author's — "within seed noise" and "no cross-arm
difference" were written four times without once writing *against what
floor*. The rule closes both ends.

The card-reconciliation finding is the rule's **motivating exhibit**:
completion floor 2.75× across cards (0.0145 → 0.0399), survival identical
(0.0129 → 0.0130). **Floors are per-metric AND per-hardware facts.**

### 3. M4.4 High survival label — RULED

Dated correction appended to `phase4_report.md`, verbatim:

> *"The High survival effect stands on REPLICATION (direction 3/3, range
> −0.047 to −0.107); its pooled magnitude is 1.41× the measured
> reproducibility floor. Reported as a consistent, modest effect. The
> '3σ/strong' label is retracted — its σ was a two-point spread, per the
> M5.1 correction."*

Direction: robust. Magnitude language: honest. Claim: survives.

*Flagged three times before being ruled, which the author records as
their own lapse: the M5.1 correction retracted σ-phrasings project-wide
and this label survived twice afterwards.*

### 4. Budget — decomposition DEFERRED INTO the Phase-6 entry gate

It belongs there because it **is** the same computation as the D6 power
analysis: runs = design × seeds-derived-from-measured-floors, costed
directly. The $81 figure is noted for what it means rather than as a
target: **money is not a constraint on any Phase-6 decision; wall-clock
and statistical power are the real currencies.**

## REPO-EXPLORER RULINGS (human, 2026-07-31) — pre-Phase-6 structural

Issued after a read-only structural review of the tree found two defects
that are invisible from inside any single milestone: a locked constant
that no config could reach, and a layout block that new sessions treat as
authoritative on day zero. Both are doc/plumbing defects, not science
defects; no measured result changes.

### 1. Comms-lock reachability — the lock existed only in prose

`comms_lock.md` locks **δ = 1.0** and **R_comm = 16**. Neither was
reachable from a config: `ThetaConfig.r_comm` defaulted to **8.0**, no
YAML set `r_comm` at all, and the locked geometry was supplied only by
`--r-comm 16` inside two milestone shell scripts.

**The δ half is NOT a defect, and the ruling says so explicitly.** All
eight configs carrying `delta: 0.0` is *correct*: base configs are
**element-OFF**, and δ = 1.0 is the **element-ON** value belonging to
θ*/joint configs, which do not exist yet. Reading the uniform `delta: 0.0`
as drift would have been a misdiagnosis. The real defects are `r_comm`
and the silent-inheritance path that let a locked value be supplied by
argv.

**Consequence check, ordered before any edit and answered from run
provenance — the certificate is CLEAN.** The question was which geometry
the M5.5 inertness grid actually ran at, because a certificate measured
at R = 8 would not cover a lock at R = 16.

| source | evidence | R_comm |
|---|---|---|
| `che/scripts/run_m55_acceptance.sh` | `R_COMM=${R_COMM:-16}  # LOCKED`, passed to train, eval **and** render | 16 |
| `results/phase5/m55/provenance.txt` | `R_comm: 16 (LOCKED)`, RTX PRO 6000, jax 0.11.0 | 16 |
| `results/phase5/m55/verdict.txt` | measured out-degree **3.213** at δ = 0 | 16 |

The out-degree is the decisive line: R = 8 measures 0.93–1.06 on this
geometry (`comms_lock.md`), R = 16 measures 2.99–3.37. M5.5 reports
3.213. **The falsifier ran on the locked geometry**, so no patch
certification is owed and no ruling on "inertness-at-8 transferred to 16"
is needed. Content ablation additionally spans both points by
construction (M5.3 + M5.3b Cell A at R = 8, Cell B at R = 16).

Three fixes, ruled:

**(a) `r_comm` becomes reachable.** `ThetaConfig.r_comm` default
8.0 → **16.0**, and `r_comm` written explicitly into
`severity_{low,medium,high}.yaml` and `gate_pop12.yaml` with provenance
citing `comms_lock.md`. The stale in-code comment "r_comm is locked at
M5.4 against measured degree/connectivity curves" is corrected: M5.4 was
folded into the M5.3 closure ruling and R_comm is locked **on the
geometric observable alone**, with the un-run {6…28} sweep recorded as a
limitation of the lock.

*Throughput provenance is not disturbed by the default change.*
`in_range_mask` builds the full [n, n] Chebyshev matrix and `sample_links`
draws [n, n] uniforms unconditionally (invariant #3), so cost is
shape-invariant in `r_comm`. The gate figure keeps its meaning; the pin is
for explicitness, not for cost.

**(b) θ\* becomes an explicit committed config.** `theta_star_*.yaml`
carrying κ_A = 0.06, κ_B = 1.0, δ = 1.0, R_comm = 16 and a held-out β —
every locked value **written out**, **constructed from locks, never
derived by inheritance**. Born in the Phase-6 prompt.

**(c) SYSTEMIC FIX — locks stop being enforced by memory.** `docs/locks.yaml`
becomes the single machine-readable source for every locked constant (βs,
κ_A, κ_B, δ_element, R_comm, dp, obs_version) with provenance keys, and
`che/tests/test_locks.py` asserts configs and code defaults agree with it.
**Standing rule: every future lock lands in `locks.yaml` in the same commit
it is ruled.** This is the ruling that matters — (a) fixes one constant,
(c) fixes the class. A lock recorded only in prose is a lock that the next
session inherits by memory, and this project has now been bitten by that
twice (tooling rule 3c/3d; R_comm).

### 2. CLAUDE.md layout block refreshed, and kept refreshed

The layout block omitted `che/calibration/` (6 modules) and `che/eval/`
entirely, listed only `throughput.py` under `bench/`, and did not mention
`e2c.py` / `e2c2.py`. Refreshed from the actual tree. Added to the
phase-close checklist: **"CLAUDE.md layout refreshed against the tree."**
Doc-rot is worse here than elsewhere because a new session reads this
block before it reads any code.

### Flagged, NOT acted on — `death_penalty` is the same defect class as `r_comm`

Recorded because the audit surfaced it and silence would repeat the
pattern: **D4 locks `dp = 0.5` for all training from Phase 3 onward**, yet
all three `severity_*.yaml` carry `death_penalty: 0.0` and every milestone
script supplies `--death-penalty 0.5` on the command line. That is a
locked value reachable only from argv — structurally identical to the
`r_comm` defect just fixed.

It is **not** changed here, because unlike `r_comm` the value is load-
bearing at run time: editing it would change what a bare
`--config severity_medium.yaml` run does, and every Phase-3/4/5 result was
produced with the override present. `locks.yaml` records it as
`supplied_by: cli` with the discrepancy explicit, and `test_locks.py`
asserts that documented state rather than forcing a change. **A human
ruling is owed on whether Phase 6 configs carry `dp: 0.5` inline.**
*(Ruled the same session — see "dp lock" below.)*

## Repo-explorer rulings, round 2 (human 2026-07-31, RA-executed)

Two questions raised by executing round 1; both answered the same session.

### 1. θ\* vs JOINT — the ruling's filename met Def. 8, and Def. 8 won

Ruling 1b named `theta_star_*.yaml` carrying a **held-out β**. Executing it
surfaced a conflict the ruling could not have known about: **Def. 8 fixes
θ\* at "all elements active, at held-out severity levels", and the JOINT
protocol trains on a mixture "still excluding θ\*'s held-out severities".**
No repo document fixes a held-out β — it is Phase-6 entry-gate item 1 — and
inventing one would violate the numbers-enter-derived sub-rule.

Naming an all-elements-ON config at β ∈ {0.43, 0.49, 0.70} `theta_star_`
would have blurred exactly the distinction the compositional-gap claim
rests on: Γ(θ\*) = J(π_joint) − J(π_iso) is only meaningful if θ\* is a
point **neither** protocol trained on.

**RULED: ship both, named for what they are.**

- **`joint_{low,medium,high}.yaml`** — all elements ON (κ_A = 0.06,
  κ_B = 1.0, **δ = 1.0**, R_comm = 16) at the three *calibrated* severities.
  This is the **JOINT protocol's multi-element training support** (Def. 8),
  runnable today, every locked value written out, enforced by
  `test_locks.py`.
- **`theta_star_holdout.yaml`** — the Def.-8 composition point. Every
  locked element value written out; **β is a sentinel that makes the config
  fail to load**, so it cannot be run by accident and cannot silently
  inherit the placeholder 0.35. `beta_holdout.value` stays **null** in
  `locks.yaml` until Phase 6 fixes *and calibrates* it the way Phase 2
  calibrated the other three.

The tripwire is the point: the held-out β is now a **loud missing value**
in the tree rather than an absence nobody would notice.

### 2. dp lock — `death_penalty: 0.5` goes inline

**RULED: write `death_penalty: 0.5` into the severity configs**, and flip
`locks.yaml` to `supplied_by: config`.

The reasoning that made this safe rather than disruptive: **no past run
changes.** Every Phase-3/4/5 script passes `--death-penalty 0.5`
explicitly, so the override sets the same value it always did and the
scripts are bit-identical. The only behaviour that changes is a **bare
`--config severity_medium.yaml` run with no flag** — which today silently
runs at dp = 0.0, i.e. **silently violates D4**. Making the lock reachable
removes a D4-violating default; it does not create a new configuration.

With this, every locked constant in `locks.yaml` is `supplied_by: config`
or `default` — none is reachable only from argv. That was the point of the
round-1 systemic fix, and this closes the last instance of the class.

## M6.0 SPIKE — authorized pre-gate (human, 2026-08-01)

Origin: the Phase-6 design v1 red team (`phase6_redteam_v1.md`) found that
**the mixture-training machinery the headline experiment depends on does
not exist**, and that θ is a frozen dataclass closed over by the jitted
train function (`ippo.py: make_train_fns(cfg)`; `env.py: th = cfg.theta`),
i.e. a compile-time constant rather than a traced value. §1 of the design
therefore registered a treatment structure against an assumed mechanism.

**RULED: run an M6.0 spike NOW, before the gate convenes** — Phase-0 logic,
de-risk the largest unknown before the design session, so the gate
registers §1 against a *demonstrated* mechanism and a *measured* cost.

**Scope.** θ becomes per-env traced fields sampled at reset/autoreset from
a mixture spec on a dedicated PRNG stream; minimal end-to-end path.

### 1. Bench targets — APPROVED as proposed, with the tax named

Rows: **`gate_pop12.yaml` (the spending consumer) + a single-policy grid
row**, each stating its keep-alive set. **`reference.yaml` is explicitly
NOT a headline row** — it is archival (`n_envs` 1024, `obs_window` 9,
elements off, placeholder β) and quoting it would be the row-A error class,
here named in advance rather than diagnosed afterwards.

**The elements-OFF traced row is REQUIRED**, and the ruling records what it
means so the docket cannot miss it: **under per-env traced θ a mixed batch
is never constant-foldable for ANY env.** Today `κ_A = 0` lets XLA delete
the seeding path outright; once θ is traced, that work runs for every env
in every batch regardless of the value it carries. The elements-OFF delta
is therefore **the permanent DCE tax the mixture design pays everywhere**,
not a corner-case measurement. **That number feeds the gate's cost line
directly.**

### 2. Bitwise fallback ladder — RATIFIED, with a floor requirement added

Ratified as proposed: bitwise required on CPU (jitted and
`JAX_DISABLE_JIT=1`); on GPU bitwise preferred, else equivalence within a
tolerance, with the regime named and the divergence localized to a specific
op. Any outcome off the ladder: **stop and report.**

**Added per bars-with-floors:** before grading any GPU divergence,
**measure the same-code GPU rerun floor under the flags in use** (the
deterministic flags if rows C/D verified them). The floor **may be exactly
zero** — in which case any traced-vs-folded difference is real and the
localize-to-an-op branch applies rather than a tolerance. A tolerance may
only be graded against that measured floor, with its regime named. No bar
before its floor, here as everywhere.

### 3. δ in scope — APPROVED

Traced set is **{β, κ_A, κ_B, δ}**. θ\* is then constructible without a
second refactor, and the marginal cost is one more compared scalar in a
kernel (`sample_links`) that already draws its uniforms unconditionally
(invariant #3).

### Scope fence — ACCEPTED as stated

**Out of scope:** traced `r_seed` and any shape/loop parameter;
`sigma_s`/`eta`; PBT integration; the full 4-component *c*-parameterized
matched mixture of design §1 (the smoke test is 2 components).

**`sigma_s`/`eta` are a HARD exclusion with a verified mechanism, not a
preference.** `observation.plane_scales` → `rho_max` reads them, those
scales are the uint8 quantization scales, and `dequantize_grid` folds their
reciprocal **on the host** precisely because fp32 division is not correctly
rounded on the GPU backend — the M5.1h incident where a full-scale code
reconstructed as 0.99999994 and an indicator plane stopped round-tripping.
`test_dequantize_does_no_device_division` guards it by inspecting lowered
HLO. Tracing σ_s/η would make the scales traced and dismantle that fix.
Verified this session: **`plane_scales` does not depend on κ_B**, so the
uint8 path is untouched by the mixture as scoped.

### Ordering — the one irreversible constraint

**The golden artifact (M6.0a) is the first commit; nothing lands on the
refactor path before its hash exists.** Acceptance 2a compares against a
baseline that ceases to exist the moment the tree changes.

### Acceptance, in order (2a → 2d)

- **a. BITWISE REGRESSION** — traced-θ at fixed locked values reproduces
  current-main trajectories bitwise under matched keys (cross-tree hash
  pattern). *This is the safety proof of the whole refactor.*
- **b.** Nesting suite green **unmodified**.
- **c.** Bench row per §1 above — traced θ defeats constant folding, so the
  cost is **measured, not assumed**; the standing throughput rule applies.
- **d.** 50-update smoke train on a 2-component mixture; per-episode
  component labels logged; realized mixture ratio ≈ weights.

### Deliverable

Report lands **on the gate docket**: feasibility + measured cost + any
surprises. Design doc v1 gains the honest line: *"Mixture machinery did not
exist at drafting; flagged in review; M6.0 spike de-risks before
registration."* The precompiled-variant fallback is recorded with its
**granularity cost**: the mixture would be realized at *update* rather than
*episode* granularity, so every env within an update shares a component and
PPO's advantage normalization sees a homogeneous batch — a different
effective objective from per-env mixing, and the reason the traced path is
worth the spike.

## Per-artifact floors — ADOPTED (human, 2026-08-02)

**RULED: the per-artifact floor amendment proposed by the M6.0 report is
adopted into CLAUDE.md**, alongside per-metric and per-hardware.

**Measure the floor on the artifact being graded, never on its reference.**
A floor taken on the comparison target describes *that* thing's stability;
if the reference is the more deterministic of the two, the floor reads zero
and the candidate's own noise gets promoted to a finding.

Origin (M6.0, `che/bench/results/phase6/m60/m60_report.md` §2): the GPU
rerun floor was measured on the **pre-refactor** tree — 0 differing digests
in 4 of 4 comparisons. Against that zero floor, `info.masked_frac` and
`info.masked_danger_sum` differing between traced and folded trees read as a
real traced-vs-folded semantic difference, which by the ratified ladder
meant "localize to a specific op, do not tolerance". Direct localization
found **identical float32 bit patterns**. Repeating both arms resolved it:
the **traced tree differs from itself 1 time in 4** on exactly those
channels. The difference was inside the candidate's own floor throughout;
the floor had been measured on the wrong tree.

**Operational form:** an equivalence or bitwise claim between A and B
requires **A-vs-A and B-vs-B**, not only A-vs-B graded against one of them.
An intermittent cross-comparison between two artifacts is itself proof that
at least one self-floor is nonzero and unmeasured — two deterministic
artifacts cannot compare intermittently.

Scope note: this does not reopen any Phase-0–5 result. It binds Phase 6
onward and any future equivalence claim.

## PHASE-6 REMEDY RULINGS (human, 2026-08-02) — the red-team findings answered

Selected from `phase6_redteam_remedies.md`. These are gate decisions on four
of the red team's open findings. Two further findings needed no decision:
**Part 1** (cost/hardware basis) was resolved by measurement — 62,084
steps/s for the gate config or 257 s/run single-policy, and the 5090 is out —
and **Part 6** (no mixture machinery) was resolved by the M6.0 spike.

### 1. θ\* siting — TRAIN ON THE EXTREMES, HOLD OUT THE MIDDLE

**RULED: train on {β = 0.43, 0.70}; evaluate at θ\* = Medium (β = 0.49).**

This answers the scissors: Coupling A is "marginal by construction" at High
(`coupling_a_lock.md`) while Coupling B's masking ceiling runs
0.028 / 0.130 / 0.419 across Low / Medium / High (`kappa_b_lock.md`), so the
drafted points at 0.46 and 0.60 each had one element effectively inert.
Medium is the only severity where **both** couplings meet their own lock
criteria — A's bands hold at Low *and* Medium; B's detection band was locked
on Medium probes (0.438/0.427, inside [0.4, 0.7]).

Three consequences, recorded because they are not obvious:

- **Def. 8 is satisfied literally.** One θ\*, at a severity neither protocol
  trained on. This is *not* the weaker "elements-only" reading.
- **It fixes half the power problem for free.** Medium carries the smallest
  measured floors of the three cells (survival 0.0130 vs High's 0.0621).
- **`beta_holdout` is resolved immediately and needs no new calibration.**
  The held-out β is 0.49, which Phase 2 already measured at 512 seeds
  (P_span 0.547, burnt fraction 19.8 %). The tripwire built at M6.0 —
  `theta_star_holdout.yaml` refusing to load while `beta_holdout` was null —
  can be closed with a *measured* value, which is exactly the condition it
  was written to demand.

**Design property, stated rather than discovered by a reviewer:** training
now spans sub- and super-critical only, and the **near-critical regime is
the test point**. Testing where correlation length ~ L is defensible and
arguably the most interesting choice, but the paper must say plainly that no
training data sits near criticality.

### 2. Estimand — ENDPOINTS CONFIRMATORY, DOSE SECONDARY, PLUS AN IDENTIFICATION ARM

**RULED: Option 2-A.**

- **Primary (confirmatory):** ISO vs JOINT-classic, verbatim as the founding
  registration defines them. Unconfounded, and needs no mixture algebra.
- **Secondary (mechanism):** the 5-point matched sweep at c = 0.5, reported
  **with its induced no-element gradient stated numerically in the paper**,
  not in a footnote.
- **Identification arm:** a second sweep at **c = 0.4**. Two non-parallel
  paths through the simplex make marginal and co-occurrence separately
  identifiable, so the design can *bound* the confound rather than merely
  acknowledge it.

The confound itself is structural and cannot be parameterized away: for two
binary elements P(neither) = 1 − P(A) − P(B) + P(A∧B), so fixing both
marginals forces P(neither) to move 1:1 with co-occurrence. The draft's own
[RT] note reasoned to the opposite sign.

### 3. Seeds — k = 20 UNIFORMLY

**RULED: k = 20.** MDE = 2σ√(2/k); at k = 4 the completion MDE is 0.0564
against historical effects ≤ 0.03, i.e. **the founding primary metric was
unresolvable before a single run**. At k = 20 completion resolves at Medium
(0.0252) and survival has margin everywhere. ≈ $15 at the measured
$0.07/run: the power problem was self-inflicted by rationing a resource that
is not scarce.

### 4. Floors — 8 REPS PER EVALUATION CONFIG, BEFORE ANY BAR

**RULED: 8 reps.** M5.5 recorded that n = 4 leaves the sd uncertain by
~±40 % (3 dof); 8 roughly halves that, for ~$1 more. Every threshold in the
phase rests on these numbers.

**Per-artifact floors apply (rule adopted this same session), and here that
means PER-ARM:** ISO and JOINT are different artifacts with potentially
different stability, so a floor measured on one may not grade the other. The
milestone therefore measures ISO, JOINT-classic and the p = 0.5 sweep point
separately. Floors for the intermediate sweep points are **assumed common
and that assumption is flagged**, not silently taken — the sweep is
secondary and not verdict-bearing.

**Ordering:** this milestone runs before any bar is written, on the card
that runs the grid.

### Still open after these rulings

The ablation certification table (5 nested configs × 3 seeds) was questioned
by the red team as 15 runs for a property `test_nesting.py` already proves.
Not ruled here.

## PHASE-6 RULINGS, FINAL FIVE (human, 2026-08-02) — register, then v2

Closes the Phase-6 entry gate. With these, every item on the original gate
queue and on design v1's own docket is either ruled or resolved by
measurement.

### 1. Pilot — DROPPED, with its two jobs re-housed rather than lost

**RULED: no pilot.** Its protective purpose — gating a large spend — is void
at ~$20 total. A k = 10 pilot would spend half the grid to protect the other
half, which is not risk management, it is arithmetic run backwards.

The pilot did two other jobs, and both are re-sited, not dropped:

- **(a) Shakedown → M6.2 IS the shakedown.** The floor milestone runs 24
  full runs exercising ISO, JOINT-classic and p = 0.5 end-to-end *with
  evals* before the grid. Any process surprise surfaces there and **STOPs**.
  This is strictly better than the old pilot: it was going to be run anyway,
  and it grades the instrument instead of guessing at the result.
- **(b) The one-paper/two-paper FORK is re-sited** from a *pre-sweep spend*
  decision to a **post-unblind framing** decision at the results-accepted
  gate. With everything run, the fork chooses **how to write, not what to
  buy** — which is what it should always have been, since the two-paper
  option was only ever a way to avoid spending money that turns out to cost
  $20.

  > **Cross-reference (added when the framing ruling was transcribed,
  > 2026-08-02):** the *PHASE-6 FRAMING + ALLOCATION RULING* at the end of
  > this log registers the **success condition PRE-unblind** (environment-
  > first; the condition is not Γ's sign). **This clause is unchanged by it**
  > — the fork stays a **POST-unblind** framing decision at the
  > results-accepted gate. Both rulings stand and compose.

**Registrar: dated amendment to the D6 gate entry — pilot clause voided by
the corrected cost basis** (recorded below).

### 2. Metric amendment — RATIFIED EXPLICITLY

**Completion is primary** (the task-performance claim, founding
registration). **Survival is registered co-primary** for coupling and
composition claims.

Justification chain, all of it pre-dating Phase 6: **M3.5** and **M4.4**
showed both couplings move survival while completion effects sit at or below
reproducibility floors; the **D6 addendum** carries it. Ratified here as an
explicit act rather than inherited, because the red team correctly noted it
was doing load-bearing rescue work.

**And the thing that makes the amendment honest rather than convenient:
k = 20.** At k = 4 the founding primary metric was unresolvable *by MDE,
before a single run* (completion MDE 0.0564 vs historical effects ≤ 0.03) —
a co-primary would then have been a substitution dressed as an addition. At
k = 20 completion resolves (0.0252), so survival is genuinely an *addition*
to a measurable primary.

### 3. Run length — 500 UPDATES, with a plateau guard

**RULED: 500.** Every floor, every throughput number and every historical
effect size this project owns was measured at 500 updates. Changing the
length **orphans the M6.2 floor milestone and the priors behind k = 20** —
the floors would no longer describe the runs they grade.

**Guard instead of guess:** M6.2 adds a **plateau check** — final-100-update
slope against zero, floor-graded. If the headline configs are still climbing,
**STOP and re-rule**. This converts "is 500 enough?" from an argument into a
measurement, and puts it where the answer is cheap.

### 4. Analysis plan — FAMILY APPROVED, specifics frozen in v2

- **Confirmatory:** {Γ_completion, Γ_survival} at θ\*, **Šidák with m = 2**,
  bars taken from the **M6.2 per-arm floors** (per-artifact rule).
- **Secondary — labelled, non-verdict-bearing:** isotonic dose-trend on the
  c = 0.5 sweep; bootstrap knee CI with an **automatic UNDERPOWERED flag if
  the CI spans the sweep**; and the c = 0.4 identification-arm confound
  bound.
- **Blind protocol governs: the analysis pipeline is frozen by commit hash
  before unblinding.**

### 5. Ablation certification table — CUT, by dated amendment

**RULED: cut from the confirmatory plan.** This amends founding scope, so it
is registered as a **dated amendment, not a quiet omission.**

Grounds:

- Its **certification** content is already *proven*, not merely evidenced:
  `test_nesting.py` plus the 1520-field-digest goldens are stronger evidence
  of exact nesting than 15 retrainings could be. Retraining demonstrates a
  property that a bitwise test establishes.
- Its **attribution** content already exists in the Phase 3–5 acceptance
  grids, which are cited with their floor-graded honesty intact.

Recorded as an **optional revision-time table (~$1)** if a reviewer asks for
same-protocol attribution.

---

## DATED AMENDMENT (2026-08-02) — to the PHASE 6 ENTRY GATE / D6 entry

The gate entry of 2026-07-28 reads, in part: *"(2) pilot scoped (2 mixture
points); (3) one-paper vs two-paper fork scheduled for after the pilot"*.

**Both clauses are amended, and the reason is a corrected number, not a
change of mind.** That entry was written when Phase 6/7 was believed to cost
enough for a pilot to be worth its own spend. The cost basis was wrong — it
descended from row A (`m06_probe.yaml`, obs_window 5), the ÷81 pattern's
fourth appearance, found by the design-v1 red team. Measured, a 500-update
run is **257 s ≈ $0.07** and the whole phase is ~$20.

- **Clause (2) — pilot: VOIDED.** A pilot cannot protect a spend smaller
  than itself. Shakedown moves to M6.2 (24 full runs with evals, STOP on
  surprise).
- **Clause (3) — fork: RE-SITED**, not cancelled. It moves from a pre-sweep
  spend decision to a post-unblind framing decision at the results-accepted
  gate. **Still post-unblind after the framing ruling of 2026-08-02** (end of
  this log), which registers the success condition pre-unblind but leaves the
  fork's siting untouched.

Item (4) of that entry (power analysis against the measured floor, checking
the registered 4 seeds) is **discharged**: the check was run, the 4 seeds
**failed** it, and k = 20 is the replacement.

---

## DATED AMENDMENT (2026-08-02) — founding scope: the ablation table

`docs/architecture_decisions_v1.md` budgets *"7 — Core ablations | 5 configs
× 3 seeds = 15"*, and `docs/theory_foundations.md` §8 refers to *"the five
locked Phase 7 configs"*.

**Amended: the 15-run ablation certification table is cut from the Phase-6
confirmatory plan.** The nested-model semantics of §8 are **unchanged and
un-weakened** — what changes is only the *evidence vehicle*: exactness is
established by `test_nesting.py` and the M6.0 goldens rather than
re-demonstrated by retraining. The five configs remain five points in Θ, as
§8 says; nothing about the ablation *semantics* is retracted.

This is recorded here so a reader of the founding document is not left to
discover a silent omission by comparing budget tables.

## AMENDMENT (2026-08-02) to PHASE-6 REMEDY RULING 3 — seeds, split by role

**Ruled:** **k = 34 on ISO and JOINT-classic** (the Γ-graded, verdict-bearing
arms); **k = 20 on both sweeps and the identification arm** (secondary,
non-verdict-bearing). **+28 runs ≈ $2.**

**Grounds.** At k = 20 the founding primary metric had **55.6 % power against
its own motivating effect band** (≤ 0.03). The ruled number was a **50 %-power
detection threshold** — the project's customary 2σ√(2/k) bar — and it omitted
the **Šidák correction that the same session's ruling 4 mandates**. Caught
during v2 drafting, **before any run**.

The amendment also restores ruling 2's logic: the co-primary is an *addition*
to a measurable primary only if the primary is actually measurable.

### NEW STANDING RULE — power statements are 80 %-power MDEs at the family-corrected α

**Every design-stage power statement uses**

    MDE(80 %) = (z_{α_family-corrected} + z_{0.8}) · σ · √(2/k)

**never a bare 2σ√(2/k).** The 2σ convention **survives only for post-hoc
floor-grading of an observed effect**, and must be **labelled as such**
wherever it appears.

This is the class-level fix, not the instance. The two are different
quantities and conflating them silently halves the power of every design it
touches: a bare 2σ bar names the effect at which one would *just* reject —
50 % power — while a design needs the effect it can *find*. The instance here
cost nothing because it was caught pre-run; the same slip inside a phase
report would have produced an underpowered null presented as a result.

### PROVISIONAL ON M6.2 — these powers use pre-M6.2 floors

The k values above are computed against **current** floors (Medium, RTX PRO
6000: completion σ 0.0399, survival σ 0.0130). Those are priors, not the
bars. After the M6.2 **per-arm** floors land:

- **Recompute.**
- **If confirmatory completion power at k = 34 falls below 75 % on the
  measured floors → STOP and re-rule.** More seeds cost $0.07 each; an
  underpowered confirmatory arm costs the phase.
- **If the floors come in smaller → record the surplus and proceed.**

This is bars-with-floors applied to the seed count itself: the design is
registered against a prior and re-graded against a measurement, with the
re-grading rule fixed in advance so it cannot be chosen after seeing the
floors.

---

## PHASE-6 FRAMING + ALLOCATION RULING (human, owner-approved 2026-08-02)

Source: `phase6_framing_allocation_ruling.txt`, RA-relayed and owner-approved,
retained at the repo root as the relay of record. Transcribed in the session
that received it, per the standing meta-rule — **nothing in it bound until
this entry existed.** Cross-referenced to the pilot/fork re-siting of the same
date (final-five ruling 1b, above); see *Reconciliation*.

### 1. FRAMING — ENVIRONMENT-FIRST

**RULED: the paper's contribution is the calibrated, theory-certified
compound-hostility environment and its measurement discipline.** The Γ
experiment is the demonstration that the environment uniquely enables, and it
is **reported whichever way it lands**.

**The paper's success condition is NOT Γ's sign.** A null or negative Γ at the
only severity where both couplings are alive is a publishable finding, not a
failure.

This is registered **pre-unblind, deliberately**, so that a null Γ cannot
later be read as post-hoc reframing. (An independent external assessment
converged on the same conclusion; the authority here is this ruling, not that
assessment.)

### 2. STATISTICS FREEZE

**RULED: the Phase-6 statistical protocol is complete** — v2 registered, and
the per-arm floor *instrument* validated by M6.2. M6.2's T = 500 floors are
**length-specific artifacts that die with the re-run**; the floors that grade
the grid come from the T\* artifact produced at sequence step (b).

**T\* is the sole open instrument question, and it is resolved by registered
criterion, not by discretion at run time:**

> **T\* = 1000 iff both confirmatory arms pass the plateau guard at the
> T = 1000 re-run.** Any other outcome **STOPs to a human ruling** (the
> else-branches in *The sequence*, below).

**No further protocol elaboration** — no new bars, corrections or power
machinery — **unless a registered guard fires.**

**Grounds.** An allocation audit found two weeks of near-total protocol work
protecting a ~3-point effect while environment-native content sat untouched.
The −8.8 pt Coupling-B survival result needed no power analysis; the machinery
exists because *this* effect is small, and it is now sufficient.

### 3. NO-PEEKING

**RULED: M6.2 cross-arm outcome comparisons are calibration by-catch.** No
design, framing or scope decision may cite them, and **any document that
quotes a cross-arm M6.2 mean gets flagged.** The confirmatory contrast is read
**once**, at T\*, through the blind pipeline frozen by commit hash (design v2
§7; the analysis-plan ruling of 2026-08-02).

Per-arm floor computation legitimately uses arm labels. **Comparing arm
*outcomes* does not happen until unblinding.**

**Operationalization** — sanctioned by this rule, and explicitly *not*
frozen-protocol elaboration: the regenerated floor report prints **per-arm sd,
range and drift only, with no per-arm outcome means**, until unblinding.
`floors.json` retains the raw values, which are needed at unblinding. Make
no-peeking **mechanical, not behavioral.**

#### The honesty note, corrected: 2 of 3, not 3 of 3

The relayed ruling's honesty note reads *"ALL THREE arms failed the plateau
guard"*. **That reflects the pre-fix instrument.** It is corrected here rather
than transliterated, per the standing sub-rule that numerical claims enter
documents derived or measured in the same session.

`m62_report.py` sliced the **NaN-filtered** completion series by `--tail`.
Completion is NaN on updates with no finished episode — at horizon 256 and
`rollout_len` 128 that is every other update, uniformly (measured on the M6.2
logs: 250 non-NaN rows of 500, inter-point gap exactly 2, no exceptions) — so
the "final-100-update" window in fact spanned **200 updates** and inflated
every reported drift ≈ 2×.

Re-measured on the M6.2 artifacts with the corrected window, this session:

| arm | drift over final 100 updates | its own floor sd | ratio | verdict |
|---|---|---|---|---|
| ISO | +0.0174 | 0.0165 | **1.06×** | climbing |
| JOINT-classic | +0.0295 | 0.0093 | **3.17×** | climbing |
| sweep p = 0.5 | +0.0056 | 0.0157 | **0.36×** | plateaued |

**Two of three, not three of three.** The ruling's operative content is
unaffected — the plateau STOP fires either way, and the T = 1000 re-run is
ordered either way. The correction *strengthens* the case for that order
rather than weakening it: the two arms still climbing are **exactly the two
arms Γ contrasts**, and they climb at different rates (JOINT ≈ 1.7× ISO's
per-update slope), so what remains is an **asymmetric convergence confound on
the headline quantity** — a worse failure than symmetric non-convergence,
which would at least partially cancel in a difference.

Drift ratios are explicitly reportable at a STOP (step (d)); no cross-arm
outcome mean appears above.

### 4. ALLOCATION CORRECTION

**RULED: reclaimed protocol effort goes to environment-native content** — the
behavioral findings family (endogenous exposure, the ash-encoding arc,
perception self-regulation, information-buying / branch-loitering), the
co-active-visitation mechanism material (invariant #5's counter has been
logged since day one), and figure production. **These are paper SECTIONS, not
garnish.**

### 5. INTRODUCTION MATERIAL (owner-approved)

The **symbiosis argument**, for the introduction skeleton: bitwise ablation
nesting, unconditional PRNG consumption and traced-θ (0 changed digests of
1520) are scientifically meaningful **because** the comparison requires ISO
and JOINT to be literally the same kernel with parameters zeroed. The
experiment justifies the engineering; the engineering enables the experiment.
**Neither half of the paper stands without the other.**

### Reconciliation with the pilot/fork re-siting (same date)

**Both rulings stand and they compose.**

- The **success-condition framing** (item 1 here) is registered **PRE-unblind**,
  on purpose.
- The **one-paper / two-paper fork** remains a **POST-unblind** decision at the
  results-accepted gate, **unchanged** — see final-five ruling 1b and its dated
  amendment, above, which are cross-referenced to this entry.

There is no tension: one fixes what counts as success before the data are
seen; the other chooses how to write up whatever is found.

### The sequence, as ordered

**0. Clean the instrument before any run.** `che/scripts/m62_report.py` carries
uncommitted changes on top of `7710bba`; fold in the item-3 mean suppression
and commit, or revert. The blind protocol freezes the pipeline by commit hash,
and **a dirty script cannot be a frozen instrument.**

**a. [OWNER-ASSIGNED] render inspection of the 24 M5.5 episodes** — the third
flag; it precedes the grid.

**b. M6.2 re-run at T = 1000.** Fresh per-arm floors (length-specific
artifacts, **never carried forward**), plateau verdict per the registered
criterion, power recompute **on the measured T = 1000 floors**. The outcome is
not to be presumed: floors are per-artifact facts and may grow with T.
→ **ELSE:** if power@0.03 (Šidák m = 2, k = 34) falls below **80 %** on either
confirmatory arm's floor → **STOP, report; k is re-ruled by a human.**

**c. If both confirmatory arms certify** (plateau guard passes; the sweep is
secondary and **does not gate**) → grid at **T\* = 1000** per the item-2
criterion, no discretion exercised, k = 34 confirmatory / k = 20 secondary as
amended → freeze → blind → unblind per protocol.
→ **ELSE:** if either confirmatory arm is still climbing at T = 1000 →
**STOP, report drift ratios; T\* escalation is a human ruling — run length is
not to be self-extended.**

**d. At any STOP:** report drift ratios and floors; **do not report cross-arm
means.**

#### Registered note — the step-(b) power threshold moved from 75 % to 80 %

M6.2's registered STOP was **75 %** (the *PROVISIONAL ON M6.2* subsection
above). **This ruling sets 80 % for step (b)**, and the difference is recorded
here rather than absorbed silently, because the 75 % figure is also a literal
in `m62_report.py` and the two must not be allowed to disagree.

*(Resolved the same day by the ruling below: `POWER_STOP` is now a registered
analysis constant at **0.80**, mirrored in `docs/locks.yaml` and asserted
against the module literal by `test_locks.py`. The 75 % history is kept in the
registry entry's provenance.)*

---

## ANALYSIS-CONSTANT REGISTRY (human, 2026-08-02)

**Context.** Raised as a flag while transcribing the framing ruling:
`k = 34 / 20`, the power STOP and the plateau threshold are registered
constants that lived only in decision-log prose and as Python literals in
`che/scripts/m62_report.py`. That is the shape of the defect the
locks-are-enforced-by-test rule was written for after R_comm — with one
genuine difference, which is why it needed a ruling rather than a mechanical
application: **an analysis threshold has no config to be reachable from.**

**RULED, in three parts.**

### 1. `docs/locks.yaml` gains an `analysis:` section

Carrying **`K_CONFIRMATORY` = 34, `K_SECONDARY` = 20, `POWER_STOP`,
`PLATEAU_PASS` = 1.0, `PLATEAU_REVIEW` = 1.5, `SIDAK_M` = 2**, each with
provenance keys citing the ruling that fixed it.

### 2. `test_locks.py` imports the analysis module and asserts equality

**Single source of truth, enforced by test, with no pretense that analysis
thresholds are environment configuration.** The env constants are enforced by
*config reachability*; these are enforced by *module import*. Same guarantee,
honestly different route — and the section says so in its own header, so a
future reader does not conclude the config-reachability rule was quietly
weakened.

### 3. `T*` does **not** enter the registry yet

**T\* is a measured outcome of the plateau procedure, not a chosen constant.**
Registering 1000 now would convert the criterion registered hours earlier —
*T\* = 1000 iff both confirmatory arms pass the plateau guard at the T = 1000
re-run* — into an assumption.

It enters at the step-(b) analysis **with its provenance** (floors file,
verdict, card, date), exactly as the severity βs did. **A slot pre-created
with `value: null` and a loud sentinel is the correct form**, and it matches
the `beta_holdout` precedent, which sat null behind a sentinel that refused to
load until Phase 2's measurement filled it. `test_locks.py` asserts the slot
stays empty **on both sides** — registry *and* module — until then.

### Two collisions found while implementing, resolved by the human

**(a) `POWER_STOP` — the ruling named 0.75; the framing ruling sets 80 % for
step (b).** Had the registry carried 0.75, step 0's required edit would have
turned the suite red and the decision log would have said 80 % while
`locks.yaml` said 75 % — precisely the disagreement the registry exists to
prevent. **Resolved: the registry carries the live value, 0.80**, with the
superseded 0.75 recorded in that entry's provenance note. M6.2's T = 500
floors are length-specific artifacts that die with the re-run, so 0.75 grades
nothing further.

**(b) `PLATEAU_REVIEW` = 1.5 had no counterpart in the instrument.**
`m62_report.py` tested `abs(drift) > sd_floor` — a single binary bar at an
implicit ratio of 1.0 — and 1.5 appeared in no document. Making it
verdict-bearing would add a third state to branches the framing ruling
registers as two-way, under a statistics freeze that forbids new bars unless a
registered guard fires. **Resolved: `PLATEAU_REVIEW` is REPORTING-ONLY.** It
labels an arm whose drift sits in (1.0, 1.5] × its own floor as *marginal*;
the verdict stays strictly binary at `PLATEAU_PASS`. The registry entry
carries `verdict_bearing: false` and a test asserts it. Motivating case: ISO
at 1.06× is climbing, but only just, and a report that says so is more useful
than one that does not.

`PLATEAU_PASS` = 1.0 was likewise an *implicit* literal until this ruling
required it be named; naming it is a faithful no-op refactor, not a change of
bar.

---

## TOOLCHAIN PINNING — the lock bound nothing (human, 2026-08-02)

**Found while provisioning the step-(b) box.** `uv.lock` has pinned
**jax/jaxlib 0.10.2 since 2026-07-18** (commit `648c2be`, unchanged since).
It bound **nothing**:

| where | jax actually run |
|---|---|
| M6.0 spike (GPU) | **0.11.0** |
| M6.2 floors (GPU) | **0.11.0** |
| this machine (local CPU venv) | **0.11.0** |
| a fresh box, 2026-08-02 | **0.10.2** |

**The interpreter was the real determinant, and no artifact recorded it.**
`jax 0.11.0` requires Python ≥ 3.12; `pyproject.toml` declared
`requires-python = ">=3.11"`. A box whose venv landed on 3.11 therefore
resolved 0.10.2 and would have run the phase's most expensive measurement on
a toolchain no Phase-6 result was taken under — silently, because
`provenance.txt` recorded jax but not Python.

**This is the third instance of one defect class**: a value the repo
*declares* with no mechanism that makes runs *use* it. Tooling rule 3c/3d
existed only in a chat transcript; `r_comm` was locked at 16 and reachable
only from two shell scripts; the toolchain was pinned in a lock file that
resolution ignored. **A declaration is not a mechanism.**

### RULED

**Run jax 0.11.0, and fix the lock to declare it — do not switch the science
to match a stale lock.** 0.11.0 is the toolchain **M6.0 certified traced-θ
bitwise on** (1520 digests, 0 changed) and the one **M6.2 measured its floors
under**. The grid at step (c) must run on it too.

Implemented in the same commit as this entry:

- `pyproject.toml`: `requires-python = ">=3.12"`, `jax>=0.11.0`.
- `uv.lock` regenerated — jax, jaxlib, `jax-cuda12-plugin` and
  `jax-cuda12-pjrt` all pin **0.11.0**. The previous lock carried a *forked*
  resolution (3.11 and 3.12 branches); dropping 3.11 collapses it to the
  single branch that was always the one actually used.
- `CLAUDE.md` stack line: Python **3.12+**, with the reason.
- `provenance.txt` now records **python, jax, jaxlib and devices**
  (`run_m62b_t1000.sh`, commit `1309ef3`) — appended by the step-(b) wrapper
  so the M6.2 script stays untouched as the provenance of the T = 500 run.

### Scope

**Phase 6 is unaffected and internally consistent**: M6.0, M6.2 and the
T = 1000 re-run are all 0.11.0, verified on the box mid-run. This does **not**
reopen Phase 0–5, whose toolchains were whatever their provenance files
record. What changes is that a future run cannot drift without the artifact
saying so.

---

## M6.2b CLOSE-OUT — CERTIFY (relayed, owner-approved 2026-08-03)

Discharges the STOP that `che/bench/results/phase6/m62b/m62b_report.md` left
open. Relayed in two rounds (the three headline rulings, then the six-flag
answers and the branch ladder), owner-approved, transcribed here in the
session that received them. **Nothing below bound until this entry existed.**

Every number in this entry is derived in-session from the M6.2b measured
floors (`results/phase6/m62b/floors.json`) at the measured 686 s/run on that
card, Šidák m = 2 (z_crit = 2.2365), target effect 0.03. Arithmetic is shown
wherever a figure is load-bearing, per the standing sub-rule.

> **Precision note, so a recompute does not read as a discrepancy.** Every
> figure below is computed on `floors.json` at **full precision**
> (σ_iso = 0.033870017, σ_joint = 0.048264641 completion; 0.009284654 /
> 0.015872252 survival), not on the 4-dp values the M6.2b report *displays*
> (0.0339 / 0.0483). Recomputing from the displayed table gives answers low
> by ~0.1 pt — e.g. 83.6 % where the instrument returns 83.7 %. The
> full-precision path is the one the instrument takes and the one that
> reproduces the report's own k = 34 figures (92.2 % / 62.8 %) exactly.

### 1. VARIANCE BASIS — the combined form, and the standing rule is amended

**RULED: contrasts are graded on the contrast's standard error.**

    sd(Γ) = √( (σ_iso² + σ_joint²) / k )

The per-arm `σ√(2/k)` form is **superseded for contrasts** and survives only
for describing a single arm's own dispersion. This is a **guard-fired
exception** to the statistics freeze, which permits revisiting power
machinery exactly when a registered guard fires — one did.

Grounds, quoting the defect the report caught in itself: the project adopted
**per-artifact floors** *because* the two arms differ in stability, then
retained a power formula that assumes they do not. The per-arm reads bracket
the truth (92.15 % on ISO's floor, 62.8 % on JOINT's; the report writes this
as 92.1 % in §6 and 92.2 % in §4 — both are that one number, rounded two
ways); neither is Γ's power.

**The standing rule in `CLAUDE.md` ("Power statements are 80 %-power MDEs")
is amended in this commit** to carry the contrast clause. Same class as the
2σ defect it already records: a formula whose variance assumption does not
match the quantity it grades.

### 2. SEEDS — k = 40 confirmatory, k = 20 secondary

**RULED: k = 40** on ISO and JOINT-classic; **k = 20** unchanged on the
sweeps and the identification arm.

Derived at k = 40: σ_iso² + σ_joint² = 3.476654e-3, sd(Γ) = √(3.476654e-3/40)
= 0.009323, power@0.03 = Φ(0.03/0.009323 − 2.2365) = **83.7 %**.

The registered 80 % minimum is **k = 37** (80.5 %; k = 36 gives 79.3 %; the
unrounded solution is k = 36.60). **k = 40 is deliberately above it**, as
margin against the 7-dof floor CIs the report itself flagged — [0.0224,
0.0690] on ISO, [0.0319, 0.0983] on JOINT at n = 8.

**Recorded because the margin is thinner than it sounds:** k = 40 buys only
**4.6 % RMS floor growth** before power falls back through 80 %. Derivation:
the 80 %-power SE is sd₈₀ = 0.03/(z_crit + z₀.₈) = 9.746279e-3, so at k = 40
the allowed variance sum is 40 × sd₈₀² = 3.799598e-3 against the measured
3.476654e-3 — ratio 1.0929, **√ = 1.0454**. That thinness is what motivated
the ladder in item 6.

### 3. BUDGET — registered here for the first time

**The `$40 grid line item` cited in the relay does not exist.** Verified
against the tree in this session by both the builder and the owner: there is
no 2026-08-02 budget registration in `docs/` or at the repo root, no $140
envelope and no $65 GPU allocation. What exists is the entry above at
*"4. Budget — decomposition DEFERRED INTO the Phase-6 entry gate"*, and that
deferral never discharged. **It is therefore registered here as new, not
cited as prior law** — the meta-rule working as designed.

**RULED (owner, 2026-08-03): ~$140 remains for the project**, GPU allocation
**~$65 reserve-inclusive**. Phase-6 spend to date is ~$5.30 (M6.2 ~$2,
M6.2b ~$3.30).

#### The delta, decomposed against baselines that are in the tree

The relay attributed the overrun to "power correction + plateau-doubled T".
**Corrected on derivation: against design v2 §6's step-(c) line the T
doubling is already inside the baseline, and the largest component is
neither — it is card throughput.** Registered against both tree baselines:

| basis | runs | s/run | cost |
|---|---|---|---|
| design v2 §6, as registered (T = 500, M6.2 card, k = 34) | 228 | 288 | **$18.24** |
| design v2 §6 UPDATE step (c) (T = 1000, M6.2 card, k = 34) | 228 | 557 | **$35.28** |
| **grid as now authorized** (T = 1000, M6.2b card, k = 40) | **240** | **686** | **$45.73** |

Three causes, each derived, summing to the total:

| cause | arithmetic | cost |
|---|---|---|
| plateau-doubled T (ordered by the plateau guard) | 228 × (557 − 288) s | **$17.04** |
| card throughput (~60,900 → ~52,000 steps/s) | 228 × (686 − 557) s | **$8.17** |
| k re-ruling 34 → 40 (power correction) | 12 × 686 s | **$2.29** |
| | $18.24 + 17.04 + 8.17 + 2.29 | **$45.74** |

**No component is scope growth.** Two are instrument facts the project
ordered or measured (run length, card); one is the power correction.

### 4. VERDICT — CERTIFY

- **T\* = 1000.** Both confirmatory arms passed the plateau guard at the
  T = 1000 re-run (ISO 0.10×, JOINT 0.57× of their own floors), which is the
  registered criterion in full — it was conditioned on the plateau guard
  alone. The report withheld registration because step (b) STOPped on the
  power branch; with that branch discharged by item 2, the conditions are
  jointly met. **Enters `docs/locks.yaml` in this commit with provenance.**
- **Grid authorized at 240 runs** (40 + 40 confirmatory, 100 sweep, 60
  identification) ≈ **$45.73**.
- **Launch gates:** owner render pass of the 24 M5.5 episodes, **and** the
  launch batch of item 6. `M6.1` engineering is **confirmed shipped** at
  `64a7397` (per-component logging, the ten `p6_*.yaml` protocol configs, the
  β = 0.49 trap test) — `HANDOFF.md` listed it as owed and was stale.

### 5. FLAG ① — confirmatory tests use the grid's own seed dispersion

**RULED.** Confirmatory tests and CIs use the **grid's own measured per-arm
seed dispersion** — the actual sampling variance of the means being
contrasted. The M6.2b floors keep two other roles and lose the one they were
wrongly carrying:

1. **Design-stage power basis, now registered as an UPPER BOUND on power**
   (to be stated in design v2). The floors are 8 identical reps at the *same
   seed*, i.e. run-to-run nondeterminism; the grid averages over k *distinct*
   seeds, whose per-run variance is σ²_rerun + σ²_seed-variation ≥ the floor.
   So 83.7 % is a ceiling, not an estimate.
2. **The separate beat-reproducibility hurdle** they were always meant to be.

**k = 40 stands as the ex-ante choice under budget. If the measured seed-sd
yields lower realized power, that is REPORTED, not re-engineered** —
registered now so it cannot become a post-hoc rescue.

Zero-compute gap-sizing from Phase 3–5 multi-seed artifacts: **approved,
informational**, not verdict-bearing.

**A consequence worth recording, because it answers an objection nobody has
raised yet.** Item 6 sets k from measured variance, which is an internal-pilot
design and normally carries a small Type-I inflation — the sample-size rule
touches the same data as the test. **Here it does not:** this ruling moves the
test's variance onto the grid's own seed dispersion, while item 6 sets k from
an *independent* rerun-floor artifact. Different samples, so the inflation
term is zero. ① and ⑥ compose to something stronger than either alone.

### 6. FLAG ② — re-floor on the rented card, with a pre-registered ladder

**RULED: the per-hardware rule holds; no transfer assumption.** The launch
batch includes **8 × ISO + 8 × JOINT floor reps** on whatever card the grid
rents (prefer the same model, RTX PRO 6000, to minimise drift), plus item 7's
sweep reps. **Launch batch = 24 runs ≈ $4.57.**

Grounds for refusing the transfer: `CLAUDE.md`'s own per-hardware exhibit
records the Medium **completion** floor moving **2.75×** across cards
(0.0145 → 0.0399) while survival held (0.0129 → 0.0130) — the metric that
moved is the one under test. And the M6.2 and M6.2b cards were **both**
PRO 6000 and still differed ~15 % in throughput, so within-model drift is not
negligible. We have **never measured the same artifact's floor on two cards**
(M6.2 was T = 500, M6.2b T = 1000), so the drift being gated on is unmeasured,
not assumed small.

#### THE LADDER — supersedes the 75 % STOP clause

On the rented card's fresh floors, compute **k_req = smallest k with combined
power ≥ 80 % at the 0.03 band**. The ladder replaces a human round-trip with
pre-registered branches:

| branch | condition | action |
|---|---|---|
| **A** | k_req ≤ 40 | proceed at k = 40; surplus recorded |
| **B** | 40 < k_req ≤ 60 | raise confirmatory k to k_req, **no round-trip**; registrar logs k and delta, derived |
| **C** | k_req > 60 | run at **k = 60** and **DEGRADE HONESTLY, never chase** |
| **D** | survival power also < 80 % | **STOP** — broken box, not floor drift; different card |

**Branch B cost cap:** k = 60 is +20 seeds/arm = **+40 runs ≈ $7.62**, inside
the ~$14.5 headroom.

**Two ladder figures are corrected on derivation** (both relayed
conservatively; the structural claims are unaffected):

- **B absorbs RMS floor growth up to ~28.0 %**, not ~22 %. At k = 60 the
  allowed variance sum is 60 × sd₈₀² = 5.699397e-3 against the measured
  3.476654e-3 — ratio 1.6393, **√ = 1.2804**.
- **The +10.5 % growth scenario costs ~+$1.91**, not ~+$3.5. (+10.5 % is the
  growth that would have fired the superseded 75 % clause.) It puts the
  summed variance at 4.2483e-3, so k_req = 4.2483e-3/9.498995e-5 = 44.7 →
  **k = 45**, i.e. +5 seeds/arm = **+10 runs**.

**Branch C's justification, and why it is not a rescue.** Survival was
ratified **co-primary** by final-five ruling 2 — months before this ladder
needed it — for exactly the coupling and composition claims at issue, and the
framing ruling already registered that **Γ's sign is not the paper's success
condition**. Under C, completion-Γ carries a **pre-registered UNDERPOWERED
flag with realized power stated**, and both metrics are still tested under
Šidák m = 2. **The family stays 2, so there is no alpha inflation** — what
shifts is narrative weight, not the test set.

**The branch trigger is OUTCOME-BLIND, and this is the load-bearing property.**
`k_req` is computed from launch-batch **rerun floors** — 24 fixed-seed reps
carrying zero cross-arm outcome information — before any grid run exists. The
ladder cannot see an effect, only a nuisance variance. Recorded explicitly
because "confirmatory verdict weight shifts to survival" reads, on its face,
like outcome-dependent metric selection, and it is not.

**Branch D is well-separated, which is what makes C honest.** Survival floors
would have to grow **3.35× RMS** to drop survival below 80 % at k = 40
(√(3.799598e-3 / 3.381332e-4) = 3.3522) — a larger move than the worst card
excursion this project has ever recorded, and in that excursion survival was
the metric that *held*.

**Worst realistic branch (B at cap):** $4.57 launch batch + $53.36 grid at
k = 60 = **$57.93**, inside the ~$65 GPU allocation. C costs the same.

### 7. FLAG ③ — sweep floor funded

**RULED:** 8 reps ≈ **$1.52**, in the same launch batch. The M6.2b outage left
the p = 0.5 arm at 1 of 8 reps and no floor at all. Without it the secondary
dose analysis (isotonic trend, bootstrap knee CI) would be **auto-flagged
UNDERPOWERED** under *bars come with floors*; with it, the analysis is
honestly graded. Floors for the intermediate sweep points remain **assumed
common, and that assumption stays flagged** (design v2 §4) — the sweep is
non-verdict-bearing.

### 8. FLAGS ⑤ and ⑥ — housekeeping, ruled

- **⑤ `HANDOFF.md` refresh approved.** Launch gates are the owner render pass
  plus the launch batch. M6.1 confirmed shipped at `64a7397`.
- **⑥a Flag numbering.** The relay calls the render pass the *sixth flag*; the
  framing ruling's sequence step (a) calls it *the third*. Both transcribed;
  **the registered count in the framing ruling governs**, the relay's informal
  count is cross-referenced. No substantive difference — same artifact, same
  gate.
- **⑥b `K_CONFIRMATORY` 34 → 40 enters as a dated addendum** to the M6.2b
  report, **never mutating** a report that correctly records the constants of
  its own era. The report's k = 34 figures stay exactly as measured.

### What this entry changes in the tree, in this commit

1. `CLAUDE.md` — the power standing rule gains the contrast-SE clause.
2. `docs/locks.yaml` — `K_CONFIRMATORY` 34 → 40; `T_STAR` null → 1000 with
   provenance; `K_LADDER_CAP` = 60 registered new.
3. `che/scripts/m62_report.py` — combined-variance power, the `k_req` solver,
   the three literals; per-arm power demoted to a labelled diagnostic.
   **Plus a latent defect found while validating the change** (below).
4. `che/tests/test_locks.py` — green on all three (it imports the module and
   asserts equality; the T\* owed-slot test flips automatically once the value
   is non-null).
5. `results/phase6/m62b/m62b_report.md` — dated addendum.
6. `HANDOFF.md` — rewritten.

---

## TRAINING LOGGER GAINS THE COUPLING COUNTERS (human, 2026-08-04)

**RULED: add them.** Issued in response to E1.2's finding that invariant #5 is
**half-satisfied** — the env emits `coupling_co_active` from day one exactly
as instructed and the eval harness consumes it into every `.npz`, but the
**training logger never picked it up**. `0 of 92` Phase 3–5 training logs
carry it, so the within-training trajectory of compound hostility is
unmeasurable from any committed artifact. That is the retrofitting problem the
invariant was written to prevent, surviving one layer down.

### What was added

Six per-step channels, in `che/train/ippo.py` as a new `STEP_METRICS` table:
`coupling_co_active`, `seeded_ignitions`, `collapse_events`, `danger_agents`,
`masked_danger_sum`, `blocked_moves`.

**They are pooled over the update, NOT done-masked**, following the M5.0 comms
pair rather than `EP_METRICS`. The reason is that these are per-step *counts*,
not episode-end values: done-masking a count records whatever the final step
happened to hold, which is neither the episode total nor a rate.

**Units, recorded because two conventions under one name is how this project
gets hurt:** the log carries the **mean per env-step**, suffixed `_per_step`.
The eval `.npz` carry the same channels **summed per episode**. Multiplying by
the horizon converts, exactly only for episodes that run to the horizon.
`test_step_metrics.py` asserts the two naming spaces cannot collide.

### Scope, and what did NOT change

**`che/env/` is untouched.** The channels already existed in the info dict;
this wires the consumer. No new state, no new PRNG draw, no change to any
kernel — `test_theta_golden`, `test_frozen`, `test_nesting` and
`test_reward_independence` are green, so trajectories are bitwise unchanged.

Both writers are covered: `ippo.py`'s row builder is generic, and `pbt.py`'s
explicit one now **enumerates from `STEP_METRICS`** rather than listing names,
so a future channel cannot be added to the metrics and silently miss the file
— which is how this defect happened in the first place.

### THE OPEN COST, and it is a real one

**Adding channels the training loop reads costs throughput, and the size is
NOT yet measured on the hardware that matters.** Under XLA dead-code
elimination the compiler deletes whatever the consumer does not read, so this
change makes the env compute six channels it was previously free to discard.
The standing throughput rule is explicit that gates bind to **measured
training throughput of the spending consumer** (`pbt.py --bench`,
`configs/gate_pop12.yaml`), which needs the RTX PRO 6000 — a 5090 cannot load
that config.

**Consequence for the grid, stated plainly:** the M6.2b floors and the
686 s/run cost basis were measured on the **pre-change** training loop. If
this change is material, both move. The launch batch already re-measures
floors on the rented card and the ladder already absorbs floor growth, so the
mechanism to handle it exists — but the **cost basis** is not covered by that
ladder and would need re-deriving.

**Owed before the grid:** run `pbt.py --bench` on the rented card with and
without the channels, record the delta, and re-derive the run cost if it is
material. If the cost is unacceptable, the fallback is to log a subset — the
co-active counter alone answers E1.2's question — and that is a human call,
not a builder's.

### Defect found while validating this change: a missing floor read as a PASS

Not part of the ruling; found by re-running the instrument on the real M6.2b
artifacts **with all three arms**, which no prior run of the analysis had
done — M6.2b's sweep arm has **1 rep and therefore no floor**.

**The plateau guard printed `-> plateaued` for it.** With no floor, `ratio`
is NaN, and `NaN > PLATEAU_PASS` evaluates False, so the arm fell through the
not-climbing branch and rendered as having **passed a guard it was never
graded by**.

This is precisely the class *bars come with floors* was written against — **a
test finer than its instrument is VOID, and a void test voids a PASS
identically** — reaching the instrument through a NaN rather than through a
threshold. It has been latent since M6.2 and was invisible because the
analysis was only ever run on arms that had floors.

**Fixed:** an ungraded arm now renders `NO FLOOR — UNGRADED (not a pass)` and
carries `graded: false` in `plateau.json`. **Verdict logic is unchanged and
still binary at `PLATEAU_PASS`** — the freeze forbids new verdict-bearing
states, and none is added. An ungraded arm simply never enters
`stop_plateau`, which is correct for the secondary sweep (it does not gate)
and is caught for the confirmatory arms by the power section, which resolves
no branch unless both are present.

**Why it matters going forward rather than backward:** no past verdict
changes — M6.2b's confirmatory arms both had floors and both genuinely
passed. But the launch batch of item 6 runs a sweep arm, and any failed rep
in it would have produced a silent false pass.

## POSITIONING RULINGS (relayed, 2026-08-05)

Relayed from the positioning review with the instruction "registrar
transcribes; skeleton amends to v2." Transcribed here in this commit.
**Neither the paper skeleton nor the DR-defense memo is a file in this
tree** — their amendments are recorded below as *owed by their holder*,
not performed. The theory-doc amendments (rulings 2, 3, 5, and a note for
4) ARE performed in this commit, in `docs/theory_foundations.md`, dated.

### 1. NO-SCOOP FINDING — ACCEPTED, with its stated limits

The four empty claim-spaces are now the paper's **novelty spine**, and C2
leads with them:

- measured-critical-point severity;
- hazard-generates-hazard;
- Beer–Lambert on a POMDP observation kernel;
- JAX × MARL × hazards.

**Three residual checks are OWNER TASKS before submission:** the IEEE
Xplore query, the NeurIPS-D&B / ICLR-2026 census, and reading
**arXiv:2507.10142** — the one place a subsuming memorization-gap theorem
could hide.

### 2. DEFINITION 2 STRENGTHENED (theory-doc amendment, dated)

New wording: the hazard appears in **neither the reward nor any auxiliary
cost or constraint channel** — survival is learned solely because death
truncates future task return. This is what actually separates the setting
from CMDP/safe-RL and from VULCAN; the old wording invited the CMDP reader
to see themselves. **VULCAN enters related work as the nearest domain
neighbor on the far side of that boundary.** Applied to Def. 2 in this
commit.

### 3. TERMINOLOGY — "passive" is STRUCK; replacement pending ratification

At a control venue "passive" asserts a formal energy property that fire,
an energy-injecting process, violates — a reviewer reads the coinage as
false. Proposed replacement: **"ambient survival stressor"**
(non-adversarial, not-instrumented, no energy claim). **"stressor" and
"compound" are KEPT** — the ecology multiple-stressors and climate
compound-events literatures are supportive analogies, not collisions.
**The strike is ruled; the replacement word awaits owner ratification.**
The theory doc carries "ambient" as of this commit, flagged pending.
`docs/architecture_decisions_v1.md` is a pre-Phase-0 archival record and
retains the struck term as history.

### 4. C4 REFRAMED — the question has priority holders; the DESIGN is ours

Cite **Agrawal 2023** and **Erdem & Üre 2025** as priority holders on the
question. Our novelty is the design, and **Keysers et al.'s DBCA gives it
a name**: matched per-element marginals = atom divergence → 0; varied
co-occurrence = compound divergence → max — **instantiated in MARL
dynamics for the first time.** The DR-defense memo now closes with DBCA:
"this is the accepted compositional-split methodology, applied where it
has never been applied." Best citation of the study; it goes in §1 of the
design description AND related work. A dated note now sits beside Def. 8
in the theory doc; the memo's closing is owed by the memo's holder.

### 5. VoC REPOSITIONED — a refinement of Pynadath & Tambe's COM-MTDP result

The 24-year-old part — **observability gates communication value**
(COM-MTDP, Pynadath & Tambe 2002) — is cited, not claimed. Our
contribution is the **second conjunct**: inertness under COLLECTIVE
partial observability when views are mutually redundant, plus the measured
swarm-scale certification (Phase 5). **Remark 2‴'s presentation order
flips accordingly** — cite first, refine second. Dated note applied in
this commit.

### 6. VENUE MECHANICS — three hard consequences

**a. PAGE BUDGET.** 6+2 pages, **appendices INCLUDED**; supplementary
text = editorial rejection. The skeleton's appendix-manifest strategy is
**DEAD for the review copy**. Restructure: 8 fully self-contained pages;
in-line only the short proofs (Prop 1, Prop 2's coupling, Thm 1 compact);
Props 3–4 as statements + one-line sketches; everything else becomes the
post-acceptance extended arXiv version, **unreferenced during review**.

**b. ANONYMITY.** No GitHub/OSF/registration links in the review copy —
pre-registration described in-text (timestamped commit hashes quoted,
artifacts "released upon publication"). Desk-reject risk eliminated.

**c. ICRA 2027** downgraded from "minority outcome" to **"improbable"**
on the transfer-window math; **IROS 2027 is THE planned stage.** Owner
emails EiC.RA.Letters@ieee.org to confirm — the $140 plan's value was
always finish-early + journal, unchanged.

**d. SMART (RA-L 2026)** is cited and pre-empted in limitations.

### What this entry changes in the tree, in this commit

- `docs/theory_foundations.md`: Def. 2 renamed ("ambient", flagged pending
  ratification) and clause 1 strengthened, dated; positioning note on the
  Remark 2′ amendment chain; DBCA note beside Def. 8; references extended.
- **No constant is ruled here; `docs/locks.yaml` is untouched.**

### Owed, and by whom

- **Owner:** IEEE Xplore query; NeurIPS-D&B / ICLR-2026 census; read
  arXiv:2507.10142; ratify "ambient"; email EiC.RA.Letters@ieee.org.
- **Skeleton holder:** amend skeleton to v2 (rulings 3, 6a, 6b); close the
  DR-defense memo with DBCA (ruling 4). Neither artifact is in this repo.
- **Bibliography:** full entries for VULCAN, Agrawal 2023, Erdem & Üre
  2025, and SMART (RA-L 2026). The relay supplied names only; details are
  deliberately NOT reconstructed here — relayed citations have previously
  named documents that do not exist, so each is verified at citation time.

## RENDER-GATE FINDINGS (registrar, 2026-08-10) — the render inspection, closed

Discharges gate 1 of the two that stood before the grid (`HANDOFF.md`:
"[OWNER] render inspection of the 24 M5.5 episodes — owner-assigned,
precedes the grid, not delegable"). The inspection asked why agents appear
to cluster at the bottom of the arena by the end of the Phase-4 and Phase-5
episodes.

### What the inspection measured

Agents spawn uniformly, so the expected starting centroid is the arena
centre, row 31.5 of 64. Measured centroid of the alive-agent marker over
the committed renders:

| render set | start row | end row | episodes drifting down |
|---|---|---|---|
| phase3 m30b (obs-v1) | 31.4 | 32.6 | 11/24 |
| phase3 m31b (obs-v2) | 31.4 | 51.0 | 8/8 |
| phase4 m44 | 32.3 | 49.2 | 24/24 |
| phase5 (m55 + pretask) | 32.3 | 44.4 | 20/24 |

**PROVENANCE AND ITS LIMIT, stated because this number will be quoted.**
These are **rendered-pixel centroids**, not state reads: the cyan alive-agent
marker was segmented out of each GIF frame and its centroid rescaled by the
axes bounding box. Marker size, antialiasing and overplotting all enter, and
the reduction is a centroid over agents, so it cannot separate "all twelve
drifted a little" from "four parked on the wall". **It is a diagnostic
instrument, adequate to establish that the effect is real and
per-checkpoint, and it is NOT the measurement instrument.** The measurement
instrument is the diagnostic adopted in ruling 3, which reads state.

### 1. DIAGNOSIS ACCEPTED

Per-checkpoint residual action bias, integrated by the absorbing boundary,
mildly attracted by the OOB-zero half-window. **Not an env bug.**

Env symmetry verified in this session: agents spawn
`jax.random.randint(minval=0, maxval=ll)`, food scatters uniformly,
ignition is a single uniform cell (`env.py` `reset`), and the action table
`_ACTION_OFFSETS = [[0,0],[-1,0],[1,0],[0,-1],[0,1]]` (`env.py:68`) is
symmetric. The direction is **per-training-run, not per-codebase**: m30b
drifts right (+8.5 columns) rather than down, and the Phase-5
`high_kbL_replicate` arm — the same High κ_B = L cell retrained — drifts
**up**, ending at row 27.6.

Two mechanisms convert a small residual bias into a wall pile-up:

1. **The boundary is absorbing.**
   `proposed = jnp.clip(agent_pos + _ACTION_OFFSETS[actions], 0, grid_size - 1)`
   (`env.py:185`) makes a move into the wall a **no-op, not a bounce**, so a
   directional bias accumulates monotonically over the horizon and does not
   relax.
2. **The wall reads as the safest cell on the map.** The egocentric crop
   pads out-of-bounds with 0 (`observation.py:282`), and 0 on the content
   planes is no hazard, no smoke, no fire. `observation.py:51` already
   documents the conflation — an out-of-bounds cell "can read *seen and
   empty*" — and names the own-position vector as the only disambiguator.

**No invariant is touched.** Reward independence (Def. 2) is untouched: the
reward reads food and occupancy only. Ablation nesting is untouched: no
mechanism here consumes PRNG.

### 2. NOT A LAUNCH BLOCKER, on stated grounds

- The confirmatory contrast compares arms whose policies **all** carry
  idiosyncratic drift, so the effect is common-mode across the comparison.
- The replicate pair bounds its completion cost at approximately zero:
  `high_kbL` ends at row 51.7 with completion 0.781, `high_kbL_replicate`
  at row 27.6 with completion **0.781** — a 24-row positional swing at
  identical completion.
- The effect predates every certified result without moving one.

The δ arms make the same point and supply their own floor: δ = 0.0 ends at
row 42.2 (completion 0.740), δ = 1.0 at row 57.7 (0.734). The 15-row gap is
well inside the 24-row swing the replicate pair shows a **fixed** config
producing between training runs, so **nothing is read into it** — the
replicate pair is the per-artifact floor for this statistic, per the
2026-08-02 amendment. The pooled correlation between end row and completion
over the 48 episodes is −0.207 and is **confounded by severity and
floorless**; it is recorded as not-evidence, and is not used above.

### 3. DIAGNOSTIC ADOPTED — draft approved, one addition

Per episode, log **mean |position − centre|** AND the **boundary-contact
fraction** (steps spent on edge rows/cols); the second is the direct
wall-pile-up statistic. Per-artifact floor from the grid's own seeds, per
the seed-dispersion ruling.

**Ships BEFORE the grid**, so 240 runs measure it for free — the
cheap-now-impossible-later window, and it converts "probably costless" into
a measured sentence for the paper.

### 4. INSTRUMENT NOTE — cross-arm falsifiers are blind to arm-symmetric effects

Recorded as a **stated limitation of condition-(ii)-style tests**, with this
as the exhibit. M4.4's inertness falsifier condition (ii) reads "no cross-arm
exposure/positioning difference" (`phase4_report.md:495`): an effect present
in **both** arms cancels exactly and cannot be detected by it. The rule
generalizes to every differenced falsifier in the project — a differenced
test measures asymmetry, and its silence is evidence about asymmetry only,
never about presence.

**The m31b watch item is reopened and closed CORRECTLY this time.** It was
closed at M4.4 (`phase4_report.md`, Result 6) on completion conditioned by
`burnt_fraction` — a completion-inferred closure of a positional claim
("obs-v2 Medium appeared to stall at arena edges", `phase4_report.md:480`).
The phenomenon was **real, positional, and benign**. Closed measured, not
inferred. Neither closure was wrong on its own terms; the first simply
graded the wrong quantity.

### 5. PAPER

One honest limitation sentence, plus the diagnostic cited:

> Boundary absorption combined with zero-padded out-of-bounds observations
> can park directionally-biased policies against arena walls; we measure the
> effect and find its cost on task completion to be approximately zero.

Discussion-section family: **the endogeneity family's fifth member** —
policies acquiring idiosyncratic spatial habits the aggregates never see.

**TRANSCRIPTION NOTE, per the derived-numbers sub-rule.** The ordinal is
recorded as the registrar issued it and is **not verified by this repo**:
the family has never been enumerated anywhere in the tree. The only labelled
member is the third (this log, 2026-07-27, behavioural perception-exposure
regulation), and `kappa_b_lock.md:28` records **that** member as demoted to
**provisional** the same day. Members one, two and four exist in no
document. An enumeration is owed before the sentence enters the paper, or
the ordinal drops and the member is cited by name.

### What this entry changes in the tree, in this commit

- `che/env/env.py`: two info channels, `center_dist_sum` and
  `boundary_agents`. Deterministic, info-only, no PRNG (invariant #3), never
  read by the reward (Def. 2).
- `che/eval/harness.py`: both added to `EVAL_METRICS` as `_SUM`.
- `che/train/ippo.py`: both added to `STEP_METRICS`, plus `alive_agents`
  (see builder decisions).
- `che/bench/throughput.py`: `_training_info_keys()` corrected — see the
  defect below.
- `che/tests/test_positional_drift.py`: new.
- `che/bench/results/phase4/phase4_report.md`: dated addendum re-closing the
  m31b watch item. The report body is **not revised**, following the M6.2b
  precedent.
- **No constant is ruled here; `docs/locks.yaml` is untouched.**

### Builder decisions, flagged for ratification rather than assumed

1. **The norm is Chebyshev (L∞).** "Distance from centre" was not specified.
   L∞ is chosen because it makes the two approved channels one statistic
   rather than two: boundary contact is exactly the event
   `chebyshev_dist == (L−1)/2`, so the fraction is the tail of the
   distribution the mean summarizes. It also matches the project's existing
   Chebyshev convention (the co-active test and the danger-moment test both
   use the crop radius). Under L2 or L1 the two channels would answer
   subtly different questions.
2. **`alive_agents` added to `STEP_METRICS`.** Not an expansion of the
   diagnostic — a denominator without which it is wrong. Both approved
   channels are sums over alive agents, so in the training log they fall as
   agents die; at High, where survival moves 8.8 points between arms, an
   undenominated numerator would confound drift with mortality. It is
   already in `EVAL_METRICS` and already in the IPPO `Transition`, so this
   is the training log catching up to the eval path, and it retroactively
   makes the existing `danger_agents_per_step` readable as a rate.
3. **Direction is NOT emitted.** A signed centroid would recover
   "which wall", and the approved channels cannot — they are magnitude-only,
   so a top-parked and a bottom-parked policy are indistinguishable in the
   log. Magnitude is what the paper sentence needs and what the cost
   question needs. Adding the signed pair is a third and fourth channel and
   therefore a human call, deliberately not taken here.

### Defect found while implementing: the bench's training keep-alive set had drifted

`che/bench/throughput.py::_training_info_keys()` documents itself as
"sourced from the collector itself so the bench cannot drift away from what
training does", and enumerated `EP_METRICS` plus the three comms keys. It
never enumerated `STEP_METRICS`. So from **2026-08-04**, when the coupling
counters were added, the `training` probe row measured an env whose six
newest channels XLA was free to delete — the identical failure mode the
function's own docstring was written against (M5.1, where enumerating the
trees replaced a hand-written list precisely so this could not recur; the
list simply grew a second home).

**Fixed structurally:** the function now enumerates `EP_METRICS` **and**
`STEP_METRICS`, so a channel added to either table is kept alive
automatically. `test_positional_drift.py` asserts the keep-alive set is a
superset of both tables, so a third table would fail rather than drift.

**Consequence, stated plainly:** every `training`-mode env-only throughput
row taken since 2026-08-04 undercounts the work the real collector does.
No gate binds to those rows — the standing rule already re-anchored gates
to measured *training* throughput (`pbt.py --bench`) — so no verdict moves.
The owed `pbt.py --bench` comparison is unaffected in kind and now covers
two more channels than when it was written.

### Owed

- **Before the grid:** the `pbt.py --bench` throughput comparison already
  owed from the 2026-08-04 entry now covers NINE channels rather than six.
  Run it on the rented card with and without, record the delta, re-derive
  the 686 s/run cost basis if material. Unchanged in kind; the fallback
  ladder (log a subset) still applies and is still a human call.
- **After the grid:** the per-artifact floor for both channels, from the
  grid's own seeds. Until it exists, neither channel grades anything —
  bars come with floors.

  **RECORDED BUT NOT GRADED, and deliberately so.** The grid writes both
  channels into every eval `.npz` (that is the free measurement this ships
  for), but `che/scripts/m62_report.py::METRICS` is
  `("completion", "survival_rate", "episode_return", "deaths_fire")` and is
  **left untouched**. That tuple drives the registered confirmatory
  machinery — the Šidák family at `SIDAK_M = 2`, the contrast power, the
  plateau guard — so adding a channel to it would enlarge a pre-registered
  family after registration, which the freeze forbids and which no
  diagnostic is worth. Computing the drift floors is therefore a **separate
  post-grid analysis with its own instrument**, not something the grid
  report will produce on its own. Stated here because "the grid measures it"
  and "the grid grades it" are one word apart and this project has been hurt
  by exactly that distance before.
- **Before the paper sentence:** enumerate the endogeneity family, or drop
  the ordinal (see the transcription note in ruling 5).

## RENDER-GATE RULINGS, ROUND 2 (registrar, 2026-08-10) — pre-launch-batch

Answers the three items the entry above flagged for ratification, closes the
DCE defect class, enumerates the endogeneity family, and promotes the
instrument note to standing law.

### 1a. `alive_agents` in `STEP_METRICS` — RATIFIED

Denominators are not scope creep; they are what make the approved channels
readable as rates. At High the denominator moves more than the effect.

### 1b. Signed direction — DECLINED, with the reason on record

Direction is **per-checkpoint idiosyncrasy** — the replicate pair proved the
same config drifts in opposite directions — so **any aggregate over signs
washes toward zero by construction**. Magnitude *is* the phenomenon. The
render archive preserves direction for any future per-checkpoint question.
Two channels not bought.

This reason is recorded rather than the decision alone, because the naive
future move is to "improve" the diagnostic by adding sign, and the aggregate
it would produce is guaranteed uninformative.

### 2. The DCE fix — RATIFIED, and the CLASS is closed

The registrar annotates env-only rows dated **2026-08-04 → the fix** as
non-comparable (undercounted keep-alive set).

**The class note matters more than the instance: the defect recurred INSIDE
the function whose docstring exists to prevent it.** Hand-enumerated
keep-alive lists rot. The structural fix — **derive the keys from the metric
tables, and assert completeness** — is the permanent shape. Second
recurrence closes the class.

**DATE, DERIVED RATHER THAN TRANSLITERATED.** The ruling gives the window as
2026-08-04 → 08-09. The fix actually landed **2026-08-10** in `9ea5629`; the
counters landed 2026-08-04 in `d513e2f`. The window is therefore
`d513e2f .. 9ea5629`, and an 08-09-or-08-10 row taken before the fix would
escape a window that ends on 08-09. **Commit-bounded, not date-bounded**, is
the durable form and is what is recorded.

**THE ANNOTATION APPLIES TO ZERO COMMITTED ARTIFACTS.** Verified this
session: exactly one commit exists between the two (`59c7409`, 2026-08-05,
positioning docs), and it touched no file under `che/bench/results/`. No GPU
box ran in the window (`HANDOFF.md`). So there is nothing in the record to
mark, and the annotation is **forward-looking only** — stated so a later
reader does not go hunting for rows that were never taken.

### 3. THE ENDOGENEITY FAMILY — ENUMERATED, and this registry is canonical

The registrar records that the ordinals were narrative memory, and that
declining to harden them was the derived-numbers rule correctly applied to
**ordinals** — which carry an implied completed enumeration exactly as a
constant carries an implied derivation.

**The paper cites members BY NAME, never by ordinal.**

| member | status |
|---|---|
| **exposure-rises-with-competence** (M1.5) | ESTABLISHED |
| **survivorship exposure** (dp arms; survivors inhale because they live) | ESTABLISHED |
| **perception-exposure regulation** (M4.3) | **REFUTED** by its own M4.4 control; retained as the family's corrected entry |
| **solution diversity under nondeterminism** (High seed spread; floors growing with T; M6.2b) | ESTABLISHED |
| **boundary drift** (render gate) | ESTABLISHED; cost bounded ≈ 0 by the replicate control |

**Family definition, for the ledger:** *measured quantities that depend on
the trained policy in ways naive instrument design assumes away.*

Two notes, recorded because the registry is now the citable source:

- The **refuted** entry is deliberately retained rather than deleted. A
  family whose failed member is erased reads as five-for-five; the corrected
  entry is what makes the definition falsifiable. `kappa_b_lock.md:28`
  independently records that member's demotion to provisional, and the two
  now agree.
- **Boundary drift is dated 2026-08-10**, matching the entry above and
  `9ea5629`. The ruling wrote 2026-08-09; the discrepancy is noted rather
  than propagated.

### 4. The instrument note — PROMOTED to `CLAUDE.md`, both halves as one law

> **Instruments state what they are blind to: cross-arm tests cannot see
> arm-symmetric effects; recording a channel is not grading it — grading
> requires a registered family and a floor.**

Landed this commit as a standing rule with both clauses and both exhibits.
The measure/grade distinction is clause 2 verbatim.

### What this entry changes in the tree, in this commit

- `CLAUDE.md`: new standing rule (above), between the contrast amendment and
  the artifact-persistence rule.
- `docs/decision_log.md`: this entry; the endogeneity registry is canonical
  and supersedes the "third member" label at 2026-07-27 and the ordinal in
  the previous entry's ruling 5.
- `gpu_launch_prompt.md`: G1.0(a) and G1.1 marked discharged, G1.0(b) widened
  to nine channels — see below.
- `HANDOFF.md`: owed list updated.
- **No constant is ruled here; `docs/locks.yaml` is untouched.**

### Consequence for G1, and it is an ORDERING consequence

`gpu_launch_prompt.md` was written 2026-08-04 at `d513e2f` and two of its
preconditions have moved:

- **G1.0(a)** (the SIGTERM-killed test chunk) — **discharged 2026-08-10**,
  green locally against both the coupling counters and the render-gate
  channels. Retained on the box as a toolchain smoke test, not as an owed
  item.
- **G1.1** (the owner render pass) — **discharged 2026-08-10**, this entry
  and the one above it. The prompt's instruction not to waive it is
  satisfied by a ruling, not by a waiver.
- **G1.0(b)** (the throughput A/B) — **widened from six channels to nine**.
  Its `STEP_METRICS.clear()` mechanism is unaffected and now measures more.

**G1.0(b) MUST PRECEDE G1.2, and the reason is stronger than sequencing
hygiene.** The A/B's `> 15 %` branch is *drop channels*, which changes the
artifact. Floors are **per-artifact**. A launch batch run before the A/B
would therefore measure floors on an artifact the grid might not use, and
those floors would grade nothing — the exact defect the per-artifact
amendment was written against, reached by ordering instead of by
substitution.

## T\* RULING (registrar, 2026-08-11) — guard-fired amendment, pre-grid, pre-unblind

Issued in response to G1.2's STOP. **The amendment window is open and no
outcome was peeked:** the grid has not run, unblinding has not happened, and
`m62_report.py` suppresses outcome means mechanically — the STOP was read off
drift ratios and floors only.

### 1. The plateau criterion is RETIRED as a certification instrument

**Reason: it is detectability-relative, so it diverges on improving
hardware.** `drift / floor` with `floor → 0` fails for any nonzero residual
drift, however scientifically negligible. On a perfect instrument nothing
ever certifies. **RA-authored flaw, logged as such.**

**It survives demoted**: a *reported* sensitivity-scaled drift statistic,
stated with its blindness, per the standing instruments-state-their-blindness
law. It grades nothing.

**Why this is not band-shopping, recorded because the shape is identical.**
A criterion retired after it fired is exactly what tolerance-loosening looks
like. Two structural facts distinguish this case:

1. **The flaw is identifiable a priori, from the formula alone, with no
   data.** `floor → 0 ⟹ ratio → ∞` needed no run to notice. The firing
   *surfaced* the defect; it did not *define* it.
2. **The amendment adds obligations rather than removing them.** It narrows
   the claim (convergence → matched budget, ruling 2) *and* introduces a new
   falsifiable requirement whose failure mode is a reportable finding
   (ruling 3). A self-serving amendment relaxes; this one trades a claim the
   design could not support for a test it can fail.

The RA's G1.2 report framed the STOP as "the guard working as designed" and
stopped one step short: **the detection was real, and wiring detectability to
a certification gate was the defect.** Both halves are recorded.

### 2. THE ESTIMAND, FIXED EXPLICITLY

**Primary Γ = the confirmatory contrast at MATCHED BUDGET T = 1000, all
arms — registered as a fixed-budget claim.**

**"At convergence" is explicitly NOT claimed anywhere.** The paper says **"at
matched compute"** throughout, which is also the practitioner-relevant
question. This is what the design always measured: ISO and JOINT receive
identical compute and Γ is their difference; convergence was an assumption
the design never needed.

### 3. Γ(t) PROMOTED — descriptive → REQUIRED robustness evidence

The per-checkpoint trajectory of the contrast, with the **pre-registered
reading rule**:

> The fixed-budget conclusion is reported as **budget-robust iff the sign of
> Γ is stable over the final half of training**. If the sign is still moving
> at T, **that instability IS the finding** and is reported as such.

**Justification, and it is arithmetic rather than taste:** the measured
differential drift is ~0.012 per 100 updates, which is **~40 % of the 0.03
target effect per 100 updates**. That is not small, and it is why this ruling
is load-bearing rather than decorative.

**MECHANISM — retain-and-eval-after, confirmatory arms only.**

- Checkpoint retention on the two confirmatory arms covers **updates
  500–1000 at interval 50 (11 points)**. ~44 MB/run, ~3.5 GB total; storage
  is free at this scale.
- **Evaluation at θ\* happens POST-UNBLIND**, as an analysis artifact: the
  frozen pipeline gains a registered Γ(t) stage. **Nobody evaluates
  checkpoints during the grid.** Γ is a cross-arm quantity, so computing it
  before unblinding would breach NO-PEEKING; the reading rule is registered
  now, the computation exists only after the salt is revealed.
- **11 points, not 6:** the $1.60 difference buys sign-stability resolution
  at the exact granularity the reading rule needs.

### 4. HONESTY LINES, pre-drafted

- Residual drift at T = 1000, quoted as the **triple**: **ISO 0.56×,
  JOINT 1.02×, sweep 1.14×** of their own floors. (The earlier "~1.0–1.1×"
  understated the sweep arm.)
- The differential drift ~0.012/100u is quoted as a **local sensitivity
  estimate — a training-surface proxy for the quantity Γ(t) measures
  directly** — never as a "bound". One linear slope, one budget, one card,
  and measured on training-log completion rather than on Γ's own
  eval-at-θ\* surface.

### 5. T = 2000 DECLINED

Reasons above, plus its price (**$80+, outside the authorization**) and its
**expected hollowness**: floors grow with T (the endogeneity family's
solution-diversity member), so doubling the budget may not improve the ratio
it was meant to fix. With the criterion retired, extending buys nothing it
was meant to buy.

### 6. COST CORRECTIONS RATIFIED

Rate table → **$1.2358/h measured**. Grid re-projection **$40.9**, inside the
**$45.73** authorization, which **stays as-registered**.

**The +$3.60 Γ(t) eval block is a RESERVE DRAW, not an authorization
amendment** — logged as its own line item against the ~$65 GPU reserve,
cause: Γ(t) promotion. **Registrar records trip total ~$48.6 projected.**

Next-trip sequence **CONFIRMED, one rental**: G1.2 re-floor on the rented
card (~$4.08) → ladder → grid (~$40.9) → post-unblind Γ(t) eval (~$3.60).

### 7. LOCKS PROVENANCE

`T_STAR`'s **value is unchanged at 1000**; its **evidence key is re-pointed
in the same commit**. Source becomes the fixed-budget estimand ruling above;
`m62b/plateau.json` is demoted to historical context carrying the
underpowered-null annotation.

**Green tests are how stale provenance survives** — `test_locks.py` asserts
the value, which would never have gone red on a justification that had
quietly expired.

### 8. RESUME STORY — decided before the rental

- The grid script gains **per-run completion manifests**: a run is done iff
  its archive and hash exist *and verify*.
- On restart it **skips manifested runs**.
- The floor script's **refuse-nonempty guard is KEPT** — integrity over
  convenience there, since 24 runs are cheap to restart.
- The grid, being **240 independent runs, must cost ≤ 1 run per
  interruption**.

**A 36-hour spot rental without a resume story is a $45 coin flip.** Builder
implements before rental.

### Builder hardening, flagged for ratification rather than assumed

Two defects found while implementing ruling 8 and ruling 3. Both are the
project's recurring shape — *a check that passes for the wrong reason*.

**(a) `sha256sum | tee -a` is APPEND, not IDEMPOTENT — and the count
assertion can pass with a missing run.** `run_m62_floors.sh:88` appends one
line per archive, and `run_m62b_t1000.sh:135` asserts
`wc -l == REPS × arms`. Under the resume design a re-executed run appends a
**second** line for the same tag. One missing run plus one duplicated line
yields exactly the expected count and the assertion **passes while a run is
absent**. Existence is also not integrity: the manifest check must **verify
the recorded hash against the file**, not merely observe that both exist.
Implemented as a keyed, rewritten manifest with hash verification.

**(b) The retention ↔ "final half" coupling is implicit and would break
silently.** `max_to_keep = 11` equals updates 500–1000 *only because*
T = 1000 and `ckpt_interval = 50`. If `T_STAR` ever moves, 11 stops meaning
"the final half", the registered Γ(t) window breaks, and **every test stays
green** — the same rot ruling 7 was issued against, one layer down. Locked as
the **relationship** (`retention ≥ T/(2·interval) + 1`) and asserted, not as
the literal 11.

### What this entry changes in the tree, in this commit

- `docs/locks.yaml`: `T_STAR` provenance re-pointed; `CKPT_MAX_TO_KEEP_CONFIRMATORY`
  added with its derived-window assertion.
- `che/env/config.py`: `TrainConfig.ckpt_max_to_keep` (default 3 — every
  pre-existing config keeps its exact behaviour).
- `che/train/ippo.py`: `_ckpt_manager` reads it instead of hardcoding 3.
- `che/configs/p6_iso.yaml`, `p6_joint.yaml`: `ckpt_max_to_keep: 11`.
- `che/scripts/lib_run_manifest.sh`: keyed, verifying completion manifest.
- `che/tests/test_locks.py`, `che/tests/test_gamma_t_retention.py`: assertions.
- **No secondary arm gains retention** — Γ is defined on the confirmatory
  contrast only, and the sweep arms stay at 3.

## PRE-RENTAL DELEGATION AND RATIFICATIONS (owner-delegated, 2026-08-13)

Issued **pre-grid, pre-unblind**: the grid has not run, no Phase-6 outcome
mean has been read, and nothing below is conditioned on one.

### 0. THE DELEGATION, and what it does and does not buy

The owner delegated the pre-rental design decisions to the builder, stating
bias avoidance as the reason: *"the decisions are yours this time and I am
making it to save potential bias now."*

**Recorded honestly, because the delegation is itself a design choice.**
Delegation **relocates** bias; it does not remove it. What actually protects
these decisions is that they are made **pre-grid and pre-unblind with no
outcome visible** — true of both parties — and that each one is either
asserted by a test or stated with its falsifier. What the delegation does buy
is narrower and real: the owner's priors about Γ's *direction* did not shape
the seed scheme, the run order, or the branch rules.

What it **costs** is a check: a builder ruling on the builder's own proposals
is weaker than an independent one. The mitigation adopted here is that **every
decision below is recorded with the argument AGAINST it**, not only the
argument for it. A reader who disagrees should be able to find the strongest
objection already stated.

### 1. THE GRID LAYOUT — RATIFIED, with two constraints the proposal did not carry

`che/scripts/run_p6_grid.sh` (committed `6bdbbc1`). The locks fix **how many**
seeds; they do not fix which integers, in what order, or against which eval
draw. Those three are ruled here.

**(a) Seeds 1..k, the SAME integers in every arm — RATIFIED.**

Starting at 1 excludes 0, which is the **floor seed**: a grid run at seed 0 on
iso, joint or sweep_p500 would be the same config at the same seed for the
same T as a floor rep — a reproducibility rep wearing a seed's name,
contributing **zero** seed variance to the arm dispersion the confirmatory
test divides by.

Sharing integers across arms is the **conservative** direction. `sd(Γ)` is
registered in the unpaired combined form, while
`Var(mean_J − mean_I) = (σ_J² + σ_I² − 2·cov)/k`; positive cross-arm
covariance therefore makes the registered formula an **over**-estimate.

*Argument against:* shared integers create no matched pairs — the arms train
on different mixture configs, so seed s produces unrelated trajectories — yet
they **look** like matched pairs, which invites a paired analysis that would
be spurious and anti-conservative.

> **CONSTRAINT, registered: the confirmatory analysis is UNPAIRED. Seed
> identity across arms carries no pairing information and must never be used
> as a blocking factor.** The shared integers exist for the covariance-sign
> argument above and for nothing else.

**(b) The eval set is a CONSTANT — seed 0, 512 episodes, every run —
RATIFIED, on a stronger argument than the proposal gave.**

The proposal justified it as variance reduction. The **load-bearing** reason
is different and better: because both arms are evaluated on the **same
episode set**, the eval draw is **common-mode and cancels in Γ**, which is a
difference of arm means. It is also identical to the floor protocol, so floors
and grid are one instrument.

*Argument against:* Γ's interval then reflects training-seed variance only and
**does not propagate eval-set sampling**, so the interval is conditional on
this draw.

> **CONSTRAINT, registered, per the instruments-state-their-blindness law:
> Γ's confidence interval is CONDITIONAL ON THE COMMON EVAL DRAW and does not
> propagate eval-set sampling variance. This is stated wherever Γ's interval
> is reported.** The cancellation argument bounds the damage in the
> *difference*; it does not licence silence about the *interval*.

**(c) Run order SEED-MAJOR, arm-minor — RATIFIED.**

Arm-major ordering loses the rental to a mid-run failure: a complete ISO arm,
a partial JOINT arm, and **no Γ at any k**. Seed-major truncation yields a
smaller **balanced** design, so an interruption costs **power, not validity**.

*Argument against, checked and dismissed:* interleaving ten configs looked
like it would force a recompile per run instead of per arm. It does not —
**every run is a separate process** (`uv run python -m che.train.ippo`) and
pays its own compile either way, which the 497 s/run G1.2 figure already
includes. Ordering is throughput-neutral. Recorded because the objection is
the obvious one and its answer is not.

**This is not a licence to stop early and pick k afterwards.** k is locked; a
short grid is an incident to report, and its realized k is whatever the
manifest says — chosen by the failure, never by the analyst.

### 2. `phase6_framing_branches.md` — RATIFIED as amended below

The outcome-conditional framing registration, drafted 2026-08-11. Its four
branches (§3) are ratified **verbatim**. It closes design v2 §10 item 5, open
since 2026-08-02. No constant, config, test or locked value changes with it,
and `m62_report.py::METRICS` / `SIDAK_M` / `K_CONFIRMATORY` / `T_STAR` are
untouched — the confirmatory family is **not** enlarged by any ruling here.

### 3. §6 ITEM 1 — BRANCH B GAINS A FALSIFIER, and it is DERIVED

The question: *"'paid in agents, not task return' is consistent with a wide
range of outcomes. Is there a completion effect size that would refute it, and
is it inside the grid's resolution?"*

**Yes to both.** Branch B is a claim about an **asymmetry**, so its failure
mode is a completion null that is an *absence* rather than an *exclusion* —
the same distinction the document already demands of branch C, applied one
level up.

> **REGISTERED FALSIFIER. Branch B is claimable only if the completion
> contrast EXCLUDES an effect as large, in standardized units, as the observed
> survival effect:**
>
>     |z_c| + z_α  <  |z_s|
>
> **where z = Γ/sd(Γ) per metric, sd(Γ) is the grid's own measured per-arm
> seed dispersion in the combined form, and z_α = 2.2365 is the two-sided
> Šidák-corrected critical value at m = 2 (α_per = 0.025321). If the
> inequality fails, the result is reported as BRANCH C with an asymmetry the
> design could not resolve — never as branch B.**

**No constant is invented.** `z_α` is the analysis plan's own already-frozen
correction; the comparison is in standardized units precisely so that no
cross-metric conversion factor has to be chosen. `|z_c| + z_α` is the upper
limit of |d_c|'s interval, so the rule reads exactly as written: *the
completion channel excluded an effect the size survival showed*.

**Why the reference is the survival POINT estimate and not its lower limit:**
the survival effect must separately reject to reach branch B at all, so its
own uncertainty is already graded there. This rule grades **the completion
channel's resolution**, and loading survival's uncertainty into it a second
time would double-count.

**Derived this session — it is inside the grid's resolution, and it has
bite.** From the G1.2 floors (`g1_floors/floors.json`, full precision) at
k = 40: `sd(Γ) = 0.00504` completion, `0.00310` survival; MDE80 = 0.01552 and
0.00955.

| observed survival Γ | max admissible \|completion Γ\| — at the floors | — at ×1.3 inflation |
|---|---|---|
| +0.010 | 0.0050 | 0.0016 |
| +0.015 | 0.0131 | 0.0097 |
| +0.020 | 0.0212 | 0.0179 |
| +0.030 | 0.0375 | 0.0341 |

The ×1.3 column carries the §5 seed-dispersion inflation bound. **The rule
bites exactly where it should:** a marginal survival effect (≈0.010) makes
branch B essentially unclaimable, which is correct — a barely-rejecting
survival result cannot support an asymmetry claim — while a solid one
(≥0.020) admits completion effects up to ~1.8–2.1 points, which is the
design's actual resolution. Floors are a **lower bound** on `sd(Γ)`, so the
left column is optimistic and is labelled as such; the grid's own dispersion
supersedes both.

### 4. §6 ITEM 2 — A MAGNITUDE THRESHOLD FOR BRANCH D IS DECLINED, with reason

The question: *"'magnitude comparable to the differential drift' is not a
number. Should it be one, and can it be set before unblinding without
inventing a constant?"*

**It should not be one, and the reason is that the design already measures the
quantity a number would only proxy for.**

The differential drift (~0.0121/100 updates, JOINT 0.02411 − ISO 0.01202,
`g1_2_report.md`) is a **training-surface local sensitivity**, and the T\*
ruling §4 already forbids quoting it as a bound. Converting it into a
magnitude threshold on Γ would require extrapolating a local slope across an
**invented horizon** — precisely the constant the numbers-enter-derived
sub-rule exists to stop.

**Γ(t) is not a proxy: it measures Γ's own trajectory at θ\*, directly, and
it is already mandated** (T\* ruling §3, 11 retained checkpoints, updates
500–1000, evaluated post-unblind). A threshold on the proxy would be strictly
worse than the reading rule on the instrument.

> **RULED. The qualitative phrase is STRUCK from branch D and replaced by the
> registered Γ(t) reading rule, made explicit: a negative Γ at T whose Γ(t)
> trends toward zero or positive across the final half is reported as NOT
> SEPARABLE from the matched-budget asymmetry; a negative Γ whose Γ(t) is flat
> or stably negative is reported as a REAL REVERSAL. No magnitude threshold is
> registered, and none may be introduced post-unblind.**

The last clause is the point: declining a threshold now is only honest if it
also forecloses inventing one later.

### 5. §6 ITEM 3 — §2's BRANCH-INVARIANCE, CHECKED RATHER THAN ASSERTED

The question: whether §2's ten items are contributions or lab notes, and
whether "a paper exists on every branch" is optimistic.

**Partitioned and counted this session.** Eight of the ten are environment or
measurement contributions that stand alone (measured critical point; bitwise
nested ablations; the three theory handshakes; Coupling A's 4.83× self-limit;
rare-and-bursty compound hostility; the flat near-agent share; comms inert
with bounds; perception decay not suppressible). **Two are protocol
observations** whose contribution status is venue-dependent: floor growth with
run length, and detectability-relative gates diverging on improving hardware.

> **RULED. §2 is NOT overclaiming — the claim "a paper exists on every branch"
> survives on the eight alone, so the two protocol observations are ADDITIVE
> rather than load-bearing. §2 is partitioned into those two tiers so a
> reviewer is never asked to accept a lab note as a contribution, and the
> venue decision (deliberately deferred, §7) places the second tier.**

### 6. §6 ITEM 4 — THE MEDIUM-SITING LIMITATION IS REQUIRED ON EVERY BRANCH

θ\* is sited at Medium, where Coupling B's own measured survival effect was
−0.0003 (within noise); its 8.8-point effect is at High, which is not θ\*.
The draft stated this on branch B only.

> **RULED. The limitation is REQUIRED on branches A, B and C alike.** It is a
> property of **θ\***, not of the outcome, so stating it only where the
> outcome makes it awkward is **outcome-dependent disclosure** — the exact
> defect this document exists to prevent, committed inside the document
> itself. Branch D inherits it through whichever co-primary it is negative on.

### What this entry changes in the tree, in this commit

- `phase6_framing_branches.md`: status DRAFT → **RATIFIED**; §3 branch B gains
  the registered falsifier; §3 branch D's qualitative phrase struck and
  replaced; §2 partitioned into two tiers; the Medium-siting limitation moved
  to a branch-invariant §4a. **The file enters the tree** — it was untracked.
- `phase6_design_v2.md`: §5 gains the upper-bound framing and the k = 34 → 40
  history; §7 gains the seed-dispersion test basis. Both were **ruled at the
  M6.2b close-out and never written into v2** — the owed text update.
- **No constant, config, lock or test threshold changes.** `SIDAK_M`,
  `K_CONFIRMATORY`, `K_SECONDARY`, `T_STAR`, `m62_report.py::METRICS`
  untouched. The two rules registered in §3 and §4 are **reporting rules on an
  existing family**, not new family members.

## NO-SCOOP CHECKS — RUN, and one spine item NARROWS (builder, 2026-08-13)

The three residual checks from *POSITIONING RULINGS* §1 (2026-08-05), run
under the same delegation as the entry above. **Verdict: NO SCOOP — the
rental proceeds.** One of the four novelty-spine claims must be **reworded**,
and one check is **only partially discharged** and stays owed.

### Check 3 — arXiv:2507.10142 — DISCHARGED, and its premise was wrong

Recorded as *"the one place a subsuming memorization-gap theorem could
hide."* It is not that. **arXiv:2507.10142 is a SURVEY** — *"Adaptability in
Multi-Agent Reinforcement Learning: A Framework and Unified Review"* (v2
retitled *"Toward Adaptable Multi-Agent Reinforcement Learning: An
Assumption-Aware Review"*), Hu et al., **cs.AI, 14 July 2025**. Identity
confirmed against two independent routes because the whole check hinged on
it. It organizes MARL adaptability into learning / policy / scenario-driven
dimensions and **contains no theorem of any kind**, let alone one subsuming
Thm. 1.

**The check is discharged, and the file that recorded it was wrong about what
it was.** Recorded as such rather than quietly closed: a check whose target
was misidentified would have been reported as "cleared" either way, and the
distinction matters for how much assurance the clearance carries.

**Re-aimed, since the designated hiding place was empty.** A broader search
for a subsuming result — a value-gap theorem for joint-versus-isolated
training over task variations — returned generic generalization-gap bounds
(Rademacher / PAC-Bayes for reparameterizable RL) and compositional
benchmarks (CompoSuite and successors). **None has a theorem of E2C's form.**
Thm. 1 stands unsubsumed on the evidence available.

### Check 2 — the D&B / ICLR census — DISCHARGED, no collision

The JAX-MARL benchmark neighbourhood is **JaxMARL** (NeurIPS 2024 D&B),
**Multi-Agent Craftax**, **Assistax**, **POBAX**, **BenchMARL**. All are
task/coordination benchmarks; **none is a hazard-survival environment, and
none carries a hazard-independent reward.** No collision.

### Check 1 — the IEEE Xplore query — **PARTIALLY discharged, still OWED**

**Stated plainly: IEEE Xplore was not queried.** It requires authenticated
access. What was run is a general-web search of the RA-L / IROS swarm
robotics literature, which surfaced the collective-perception-under-degraded-
sensing line (**BayesCPF**, adaptive self-calibration for imperfect swarms,
decentralised resilience to malicious influence). All of it is
**single-stressor and task-coupled** — no compound-stressor benchmark.

**That is evidence, not the check.** The Xplore query remains an owner task.
It does not gate the rental: the grid measures Γ in this environment
regardless of what the venue search returns, and a collision would change the
paper's framing, not its data.

### THE MATERIAL FINDING — spine item 4 NARROWS

**`JaxWildfire`, arXiv:2512.06102** — *"A GPU-Accelerated Wildfire Simulator
for Reinforcement Learning"*, December 2025 — occupies part of the claim
space the spine recorded as empty. It postdates the 2026-08-05 positioning
review, which is why that review did not see it.

**It is not a scoop, and the reasons are structural rather than
convenient.** On the characterization obtained:

| | JaxWildfire | CHE |
|---|---|---|
| agents | **single** (multi-agent named as future work) | swarm, 12 agents, shared-parameter IPPO |
| reward | **penalty ∝ burning cells, +10 for extinguishing** | **hazard-independent (Def. 2)** — no hazard term in reward or any auxiliary channel |
| task | fight the fire | unrelated task **while surviving** the fire |
| perception | egocentric, **unattenuated** | Beer–Lambert smoke attenuation of the observation kernel |
| hazard→hazard | none | Coupling A: collapse seeds ignition |
| severity | fitted to historical burns | **measured critical point** (β̂_c = 0.500, 512 seeds) |

**The reward row is the whole argument.** JaxWildfire's reward is a penalty
proportional to burning cells — precisely the CMDP / safe-RL shape Def. 2
excludes. It is therefore **the nearest neighbour on the far side of Def. 2's
boundary, and a better foil than VULCAN** (positioning ruling 2), because the
boundary is visible in one line of its reward function rather than argued
from domain.

> **RULED. Spine item 4 is reworded from "JAX × MARL × hazards" to
> "JAX × MARL × hazard survival under a HAZARD-INDEPENDENT reward."**
> The unqualified form is no longer true and must not be written. JaxWildfire
> enters related work beside VULCAN, as the nearest neighbour across Def. 2.

**Spine items 1–3 return no collision:** measured-critical-point severity;
hazard-generates-hazard (see the caveat below); Beer–Lambert on a POMDP
observation kernel — the last returned **no hits at all** in the RL
literature.

**One neighbour for item 2 that must be cited rather than missed:**
*Reinforcement Learning for Public Safety Power Shutoffs Under
Decision-Dependent Uncertainty and Nonlinear Wildfire Ignition Models*
(arXiv:2604.26150) makes ignition probability **endogenous to the operator's
decisions**. That is **agent-mediated** endogeneity; **Coupling A is not** —
collapse seeds fire with no action in the path. The claim survives as
*"hazard generates hazard without agent mediation"*, and the paper cites this
one rather than letting a reviewer find it.

### CONFIDENCE, stated because it bounds every row above

The JaxWildfire characterization comes from an **automated summary of the
paper's HTML**, not from a reading of the PDF by the author. It is strong
enough to rule on positioning **pre-rental** and is **not** strong enough to
write related work from.

> **OWED before submission (not before the rental): read the JaxWildfire PDF
> and the arXiv:2604.26150 PDF directly, and confirm the two rows this entry
> leans on — single-agent, and the burning-cell reward.** If either is wrong,
> the spine rewording above stands anyway (it only narrows a claim), but the
> foil argument would need rebuilding.

### What this changes in the tree, in this commit

- `phase6_framing_branches.md` §7: the three checks gain their status.
- **No constant, config, lock or threshold changes.** Nothing here touches
  the grid, the analysis family, or the blind.

## GRID CHUNKING — RATIFIED at 4 × 60 (owner-requested, builder-ruled, 2026-08-14)

Owner asked whether the 240-run grid can run in four chunks of 60 rather than
one ~33-hour session. **Yes, and it is now supported explicitly** (`MAX_RUNS`,
`che/scripts/run_p6_grid.sh`). Issued pre-grid, pre-unblind.

### 1. The chunks land on seed boundaries, and that IS the safety argument

Derived this session from the script's own layout: at `MAX_RUNS = 60` the four
chunks are **seeds 1–6, 7–12, 13–18, and 19–40** (the last being seeds 19–20
across all ten arms plus the confirmatory tail 21–40). Exact, with no
remainder.

**Chunks will in general run on different rented cards, and floors are
per-hardware.** What makes that safe is the seed-major ordering already ruled
in §1(c) of the pre-rental entry: a chunk contains **every arm at a contiguous
block of seeds**, so within any seed **ISO and JOINT ran on the same card**. A
card effect is therefore **common-mode within a seed and cancels in Γ**, which
is a difference of arm means — the identical argument that justifies the
common eval draw (§1b).

**This is a property the ordering decision bought before anyone asked for
chunking**, and it is recorded that way rather than claimed as foresight: the
ordering was ruled for interruption-robustness, and multi-card safety fell out
of it.

### 2. The stop OVERRUNS `MAX_RUNS` to reach a seed boundary

**Splitting a seed across two cards breaks the cancellation for that seed** —
ISO on the old card, JOINT on the new one — and the asymmetry points the same
way every time, because arms run in a fixed order within a seed. So when
`MAX_RUNS` is reached mid-seed the loop **finishes that seed before stopping**.
Overrunning a cap by a few runs is strictly cheaper than hand-auditing a split
seed. Asserted by `test_p6_grid.py`.

### 3. WHAT IT COSTS — power, not validity

Each arm's variance gains a between-card component, so `sd(Γ)` inflates.
**Derived from the G1.2 floors at k = 40 against the 0.03 target:** `sd(Γ)` may
inflate **1.93×** (completion) or **3.14×** (survival) before power falls to
80 %. The ~1.3× already anticipated for seed dispersion leaves roughly **1.5×**
for card blocks.

**The registered clause already governs the outcome: realized power is
REPORTED, not re-engineered** (M6.2b close-out, item 5). Chunking does not
create a new escape hatch and none is added here.

**Money is roughly unchanged.** The GPU-hours are identical — 240 runs plus one
re-floor ≈ 36.4 h ≈ **$45.0** at the measured $1.2358/h — plus **four setups
instead of one** (sync, `uv sync`, pre-flight), ≈ **+$1.5**. Chunk wall-clock
will vary with the card, since `MAX_RUNS` counts runs and not hours.

### 4. IT DOES NOT REQUIRE RE-FLOORING EACH CARD, and the reason is structural

One re-floor, on the first card, as already budgeted.

The confirmatory test uses the **grid's own per-arm seed dispersion**, and on a
multi-card grid that dispersion **already contains the card variance**:
`σ²_arm = σ²_rerun + σ²_seed + σ²_card ≥ σ²_rerun`, which is the floor. So the
**beat-reproducibility hurdle is SUBSUMED, not bypassed** — an effect clearing
the grid's own dispersion has cleared reproducibility on every card involved.
The floor keeps its two other roles unchanged: it set **k** through the ladder
(a one-time determination, already resolved to branch A), and it is the
design-stage power basis **registered as an upper bound**.

### 5. REGISTERED OBLIGATION — the block structure is recorded AND reported

The cancellation argument in §1 is only sound if one card really did run both
arms of every seed. That is now **checkable rather than assumed**: the card is
recorded **per run** (`.manifest/<tag>.card`, per-tag and overwritten, so it is
idempotent under retry) and `cards.txt` is **derived** from those records, one
row per (card, arm) with its seed range.

> **The paper reports the card-block structure whenever the grid ran on more
> than one card, and states the cancellation argument alongside it.** A split
> seed, if one ever occurs, is disclosed rather than absorbed.

### Defect found while implementing, and it was latent already

**`provenance.txt` was written with `tee`, which OVERWRITES.** A second
invocation would erase the record of which card ran the earlier chunks — and on
a chunked multi-card grid that record *is* the audit trail for §5. **The defect
did not need chunking to exist: every resume overwrote it**, and the resume
path shipped in `6bdbbc1`. Now appended, with a per-invocation header carrying
the seed range covered. Regression test added.

Same shape as the `/m06/` gitignore entry closed yesterday: **a mechanism that
looked like it was working while quietly discarding what it was meant to
keep.**

### What this changes in the tree, in this commit

- `che/scripts/run_p6_grid.sh`: `MAX_RUNS` with a seed-boundary stop; per-run
  card records; derived `cards.txt`; provenance appended not overwritten; a
  **CHUNK COMPLETE** exit that is **green**, because a planned pause is not a
  failure and an operator who sees red on a deliberate stop learns to distrust
  the exit code on the invocation that matters.
- `che/tests/test_p6_grid.py`: 23 tests — chunk/seed-boundary alignment, the
  mid-seed overrun, provenance accumulation, card-block recording.
- **No constant, config, lock or analysis threshold changes.**

## VENUE RULING — NeurIPS D&B is the primary target (owner, 2026-08-16)

Transcribed in the same session it was issued, per the meta-rule (2026-07-28).
**Pre-grid and pre-unblind:** no Phase-6 outcome mean exists, so this decision
is provably not outcome-selected — which is the property that makes it worth
more than the deferral it replaces.

Issued in response to `docs/venue_review_2026-08-16.md`, an assessment written
this session from the repository. **That review is not a ruling and rules
nothing**; it binds only what this entry transcribes.

### THE RULING

> **The primary venue is NeurIPS Datasets & Benchmarks.** TMLR is the
> registered fallback. **RA-L / IROS is demoted to a branch-A-conditional
> stretch** and is not written for by default.

### What it supersedes

1. **`phase6_framing_branches.md` §7 — "venue is deliberately NOT decided
   here."** That deferral was ruled on the grounds that venue is legitimately
   outcome-conditional. **Deciding it now strengthens the blind rather than
   weakening it:** an outcome-conditional venue choice is one more thing that
   could be selected after seeing Γ, and this removes it. §7's companion claim
   — that the *claim* is what cannot wait — is unaffected; the four branches
   stand ratified verbatim and no branch table is edited.
2. **POSITIONING RULING 6c (2026-08-05) — "IROS 2027 is THE planned stage."**
   Reversed. The owner-owed email to `EiC.RA.Letters@ieee.org` is **struck
   from the owed list**, not deferred.
3. **POSITIONING RULING 6a — the 6+2-page, appendices-included budget.** No
   longer the binding constraint, so the appendix-manifest strategy that 6a
   declared **DEAD** is **provisionally revived**. *No page count is recorded
   here:* the derived-numbers sub-rule forbids transliterating a CfP figure
   from memory, and the current call has not been read. Revival is conditional
   on the verification below.

**POSITIONING RULING 6b (anonymity) is NOT superseded and needs re-checking in
the opposite direction.** 6b forbade repository links in the review copy to
eliminate desk-reject risk. A benchmark track may instead *require* reviewer
access to the artifact. These two pull opposite ways and the conflict is
unresolved until the CfP is read.

### Grounds, in the order they carry weight

1. **The artifact is not a robotics artifact.** 64² discrete grid, 12 agents,
   5 discrete actions, food collection, CA fire; no robot, no continuous
   control, no hardware, no sim-to-real. The only embodiment argument in the
   tree is one clause of Def. 2's note.
2. **The novelty spine is four ML-methods claims**, none of them a robotics
   claim (positioning ruling 1, as narrowed 2026-08-13).
3. **The tier-1 contribution set is a benchmark contribution verbatim** and was
   already **checked** to carry a paper on its own
   (`phase6_framing_branches.md` §2, eight items). The paper does not depend
   on Γ, which is what makes retargeting safe rather than hopeful.
4. **The modal branch is C**, and branch C is the branch §3 itself records as
   *"not RA-L-shaped"*. Design v2 §5 reached the same conclusion from the
   statistics and called it *"scientifically good and strategically
   uncomfortable"*. **The discomfort was an artifact of the venue target.** It
   is now retired: at a benchmark venue a calibrated instrument plus a
   well-powered exclusion is the scored object.

### What this ruling does NOT do

- **It does not edit the branch table.** The four branches of
  `phase6_framing_branches.md` §3 stand ratified verbatim. What changes is
  which branch the paper is *written for by default*, which §7 left open.
- **It changes no constant.** `SIDAK_M`, `K_CONFIRMATORY`, `K_SECONDARY`,
  `T_STAR`, `m62_report.py::METRICS` and every entry in `docs/locks.yaml` are
  untouched. No config, script or test changes in this commit.
- **It does not authorize spend.** The §7 proposals below are unruled.

### OWED — owner tasks created or changed by this ruling

1. **Read the current NeurIPS D&B call for papers** and record, derived from
   the call itself: page limit and whether appendices count; anonymity and
   artifact-access handling (resolves the 6a/6b conflict above); submission
   dates. **No figure from this class enters any document until it is read
   from the call** — the same sub-rule that has already stopped one plausible
   constant in this project.
2. **Benchmark-track deliverables not yet owed under an RA-L target**, to be
   scoped once (1) is read: artifact documentation of datasheet shape,
   hosting/accessibility for reviewers, licensing (MIT is in tree),
   reproduction instructions beyond the current `README.md`, and a limitations
   section that carries §4a and the frozen-random-projection caveat.
3. **Unchanged and still owed:** the IEEE Xplore query (partially discharged,
   2026-08-13) — **retained despite the demotion**, because it checks for a
   colliding *benchmark*, and a collision would move framing at any venue;
   reading the JaxWildfire and arXiv:2604.26150 PDFs; verifying VULCAN,
   Agrawal 2023, Erdem & Üre 2025 and SMART (RA-L 2026), which are relayed
   names only in a project whose log records relays naming documents that do
   not exist.

### The review's proposals are OWED RULING, and none is taken here

`docs/venue_review_2026-08-16.md` §7 raises four items. They are recorded as
**proposals awaiting an owner ruling**, and each may be adopted **only
pre-unblind** — their entire value is in having been chosen with no outcome
visible.

| # | proposal | derived cost | status |
|---|---|---|---|
| 0 | Register in writing, pre-unblind, that ISO spends 1/3 of its training budget on a **certified-inert** element, and that the resulting bias **inflates Γ** | $0 | **AWAITING RULING** — the review argues it is non-optional under the standing discipline |
| 1 | `ISO-4` secondary arm, {A-only, B-only} × {0.43, 0.70}, k = 20 | $3.41 | AWAITING RULING |
| 2 | T = 2000 subsample, confirmatory arms only, 4 seeds each | $2.68 | AWAITING RULING |
| 3 | High-severity secondary point, 2 arms × k = 20, UNDERPOWERED-flagged | $6.82 | AWAITING RULING |

Costs are derived in the review from the measured 497 s/run and $1.2358/h;
the three run-bearing proposals total **$12.91** against a **~$16.4** free
reserve, so they are **ranked, not bundled** (recommended order 0, 1, 2, 3).

**The finding behind proposal 0, recorded here because it is the substantive
one and it is only sayable pre-unblind:** `p6_iso.yaml` carries 6 uniform
components, of which `d_low` and `d_high` are δ-only
(`kappa_A: 0.0, kappa_B: 0.0`), and Phase 5 certified δ inert. So 2/6 = 0.3333
of ISO's training episodes carry **no behaviourally active element**, against
100 % of JOINT's carrying both live couplings. The generated header's
`no-element 0.0000` is true **nominally** and false **behaviourally** under the
project's own certification. Design v2 §2 registers the *marginal* imbalance
and defends it as definitional — that defence holds — but the *inert*-share
accounting is unregistered, and it is the same confound §2 polices for the
sweeps ("at p = 0.5 half of all training episodes contain no stressor at all")
reappearing inside the confirmatory arm at p = 1/3. Design v2 §10 item 4's
symmetry defence covers test time and not train time: in JOINT δ rides free
inside an all-on component, in ISO it costs a third of the budget.
**Note the internal precedent — the sweeps already exclude δ on exactly this
reasoning.**

### What this entry changes in the tree, in this commit

- `docs/venue_review_2026-08-16.md`: new, the assessment this ruling responds
  to. It states its own blindnesses (§9) and rules nothing.
- `docs/decision_log.md`: this entry.
- `HANDOFF.md`: venue pointer for the next session.
- **No constant, config, lock, test or analysis threshold changes.**

## VENUE RULING II — TMLR primary, DMLR fallback (owner, 2026-08-24)

Transcribed in the same session it was issued, per the meta-rule (2026-07-28).
**Pre-grid and pre-unblind:** `run_p6_grid.sh` has not run, there is no box,
and no Phase-6 outcome mean exists — so this decision retains the property
that made the 2026-08-16 ruling worth more than the deferral it replaced.

Issued in response to `docs/venue_review_2026-08-24.md`, an assessment written
this session from the repository and from the venues' own published pages.
**That review is not a ruling and rules nothing**; it binds only what this
entry transcribes.

### THE RULING

> **The primary venue is TMLR.** **DMLR** (Journal of Data-centric Machine
> Learning Research) is the registered fallback. **Both are rolling**, and
> they are attempted **sequentially**, never in parallel.

### What it supersedes

1. **VENUE RULING (2026-08-16) — "the primary venue is NeurIPS Datasets &
   Benchmarks; TMLR is the registered fallback."** Superseded on the
   primary/fallback pair only. NeurIPS D&B is **not** registered anywhere in
   the ladder; a deadline venue is declined as primary for the reason in §2
   below.
2. **That ruling's owed item 1** — "read the current NeurIPS D&B call for
   papers and record page limit, anonymity handling, submission dates."
   **Struck**, not deferred. It is replaced by the single unverified item in
   §5.

**What it does NOT supersede.** The 2026-08-16 grounds for demoting RA-L/IROS
(§1 items 1–2: the artifact is not a robotics artifact; the novelty spine is
four ML-methods claims) are structural and independent of which ML venue is
primary. **RA-L/IROS remains demoted to a branch-A-conditional stretch and is
not written for by default.** The struck email to `EiC.RA.Letters@ieee.org`
stays struck.

### Grounds, in the order they carry weight

1. **Rolling, because a rejection must not cost the calendar.** Runway is
   ~7 months (`CLAUDE.md`) and the project has one grid's worth of results. A
   deadline primary charges a full cycle for a rejection; a rolling primary
   charges a review. This is the reason the pair is rolling at all, and it is
   the owner's stated motivation for reopening.
2. **TMLR's criteria eliminate this paper's dominant rejection risk.** Read
   from the criteria page 2026-08-24: two criteria, evidence and audience
   interest; "significant", "impactful" and "novel" explicitly declined as
   rejection grounds; state-of-the-art not required; and the one subjective
   criterion carries an **assume-satisfied-when-uncertain** instruction to
   reviewers. The modal branch is **C** — a well-powered null
   (`venue_review_2026-08-16.md` §5). A venue that refuses novelty as a
   rejection ground is the correct first attempt for a null.
3. **Parallel submission is forbidden, so the ladder is sequential by rule and
   not by preference.** TMLR's originality policy bars reuse of text, figures
   or results from any paper submitted in parallel at another archival
   peer-reviewed venue. Ordering is therefore the only free variable, and
   ground 2 fixes it.
4. **DMLR is the fallback because it grades the artifact and TMLR does not.**
   DMLR's stated scope names "Data generators and reinforcement learning
   environments" and "Benchmarking tools and methods"; its acceptance criteria
   are close to a transcription of the benchmark deliverables already owed.
   Neither TMLR criterion asks anyone to evaluate the environment *as* a
   benchmark. The fallback is where the tier-1 artifact payload is scored.

### The ordering's second support DID NOT SURVIVE VERIFICATION, and the ruling is issued anyway

Recorded here rather than in the review alone, because it qualifies the
ruling's own reasoning.

The proposal that produced this ruling argued TMLR-first on two legs:
acceptance probability, and speed — "a TMLR rejection at ~2–3 months still
leaves room for DMLR inside the runway." **The speed leg is unsupported.**
TMLR publishes stage deadlines only (action editor within a week; final
recommendation once at least two weeks have elapsed after all 3 reviews became
public) and **no total time to decision**. DMLR publishes an expected **4–6
months**, up to 10 in exceptional cases. No comparison follows from those two.

The "~2–3 months" figure was asserted from memory in chat, is retracted in
`venue_review_2026-08-24.md` §5, and **enters no document**. Per the
derived-numbers sub-rule, **no runway arithmetic involving TMLR may be written
anywhere until §5's check is discharged.**

**The ruling stands on ground 2 alone**, which is the stronger leg and does not
depend on timing. The sequencing *benefit* is unquantified and is not claimed.

### The Journal-to-Conference track is NOT a ground

Verified from the track's own page 2026-08-24 and recorded so it is not later
mistaken for a reason: eligibility requires a TMLR paper to hold **a J2C,
Featured or Outstanding certification** — not an ordinary acceptance — within a
rolling two-year publication window opening 2025-01-01; the format is typically
a **poster**; and the paper "shall not be considered as being published in the
proceedings of the chosen conference." It is a conditional visibility bonus
whose condition no design decision can secure in advance. An earlier
characterization of it as materially changing TMLR's standing is corrected in
`venue_review_2026-08-24.md` §6.

### Consequences for the standing positioning rulings

- **POSITIONING RULING 6b (anonymity, no repo links) STANDS, and the conflict
  the 2026-08-16 ruling left open is CLOSED under the primary.** TMLR is
  double-blind, requires anonymized submissions, forbids linkage to a
  non-anonymous preprint, and requires supplementary code to be anonymized
  (≤100 MB). No benchmark-track artifact-access requirement arises.
  **The conflict RETURNS if the DMLR fallback is exercised** — DMLR is
  single-blind and requires availability and maintenance documentation — and
  is to be re-ruled at that point, not pre-emptively.
- **POSITIONING RULING 6a's page budget is DISCHARGED as a constraint.** TMLR
  states no strict page limit ("may be any length, but a paper's length should
  be justified by its content"). The appendix-manifest strategy, revived
  *provisionally* on 2026-08-16 pending a CfP reading, is now **unconditional
  under the primary**. The conditionality is discharged by verification, not
  waived.
- **Benchmark-track deliverables (2026-08-16 owed item 2) are OPTIONAL under
  the primary and REQUIRED under the fallback.** They remain worth doing: they
  are the artifact's adoption path, which a claims venue does not supply.

### What this ruling does NOT do

- **It does not edit the branch table.** The four branches of
  `phase6_framing_branches.md` §3 stand ratified verbatim, exactly as the
  2026-08-16 ruling left them. The `venue lean` column is descriptive and is
  not a registration; branches C and D already lean TMLR.
- **It changes no constant.** `SIDAK_M`, `K_CONFIRMATORY`, `K_SECONDARY`,
  `T_STAR`, `m62_report.py::METRICS` and every entry in `docs/locks.yaml` are
  untouched. No config, script or test changes in this commit.
- **It does not authorize spend**, and it does not rule on the four §7
  proposals of `venue_review_2026-08-16.md` (0, 1, 2, 3), which remain
  **AWAITING RULING** and adoptable **only pre-unblind**.
- **It does not reopen the RA-L/IROS demotion.**

### OWED — the owner task list after this ruling

1. **Obtain TMLR's total time to decision** from its published statistics or
   the OpenReview record — not from an estimate. This is the *only* venue
   mechanic left unverified, and until it is discharged no runway arithmetic
   involving TMLR may be written. (Replaces the struck D&B CfP task.)
2. **Unchanged and still owed:** the IEEE Xplore query (partially discharged
   2026-08-13); reading the JaxWildfire (arXiv:2512.06102) and
   arXiv:2604.26150 PDFs; verifying VULCAN, Agrawal 2023, Erdem & Üre 2025 and
   SMART (RA-L 2026). **The bibliography remains the highest-severity
   non-technical risk in the project and no venue decision touches it.**

### What this entry changes in the tree, in this commit

- `docs/venue_review_2026-08-24.md`: new, the assessment this ruling responds
  to. It states its own blindnesses (§5), carries a retraction, and rules
  nothing.
- `docs/decision_log.md`: this entry.
- `CLAUDE.md`, `HANDOFF.md`, `docs/theory_foundations.md`: venue pointers
  updated to match.
- **No constant, config, lock, test or analysis threshold changes.**


## G1.2 RE-FLOOR ON THE GRID CARD — LADDER BRANCH B, k = 46 (registrar transcription, 2026-09-09)

Not a ruling. The re-floor's verdict is pre-registered (`gpu_launch_prompt.md`
G1.2; `run_m62b_t1000.sh` header) and this entry logs its outcome and the
derived cost delta, which the verdict line itself instructs the registrar to
do. **Pre-grid and pre-unblind: no grid run has started.**

**Rental.** vast.ai, RTX PRO 6000 Blackwell Workstation (97,887 MiB), 32 GB
disk, ~50 MB/s network, rented 2026-09-08. Repo shipped by `git archive` of
commit `51e489a` (no `.git`); toolchain verified Python 3.12.3, jax/jaxlib
0.11.0, one CudaDevice. Re-floor launched 17:55 UTC 2026-09-08 in tmux,
`OUT=che/bench/results/phase6/g1_floors UPDATES=1000 REPS=8`, exit 0 at
~21:30 UTC. 501 s/run train, 15 s eval — the G1.2 card's 497 s.

**Measured per-arm floors (same seed, identical runs), completion / survival:**

| arm | completion sd | survival sd |
|---|---|---|
| ISO | 0.0281 | 0.0070 |
| JOINT | 0.0598 | 0.0129 |
| sweep_p500 | 0.0383 | — |

Against the 2026-08-10 card (ISO 0.0214 / JOINT 0.0236 completion): this
card's JOINT completion floor is **2.5×** larger. Floors are per-hardware;
this is the exhibit.

**Plateau (descriptive only — criterion retired by the T\* ruling):** drift
over the final 100 updates / own floor: ISO 0.80×, JOINT 0.68×, sweep 0.26×.
All three below 1.0×.

**Power on the contrast basis, Šidák m = 2, k = 40:** sd(Γ) completion
0.01044, survival 0.00232; MDE80 0.0321 / 0.0071; power@0.03 **73.8 %** /
100 %; **k_req 46 / 3.**

**LADDER: BRANCH B** (40 < k_req ≤ 60). Registered action executed as written:
**the grid runs at K_CONF = 46**, no human round-trip. Realized power@0.03
at k = 46: **80.1 %**.

**Derived cost delta:** +12 confirmatory runs (6 seeds × 2 arms) → 252 runs.
At the measured 8.8 min/run including archiving, +1.8 GPU-h ≈ **+$2.2** at
$1.2358/h; grid total ≈ 37 GPU-h ≈ **$45.7**. Chunks at `MAX_RUNS=60` land on
seed boundaries as before, then a fifth invocation covers seeds 41–46
(12 runs).

**Box disk guard:** the box has 32 GB; the grid will run with
`MIN_FREE_GB=10` (an env var the script header invites when measured):
chunked operation holds ≤ ~4 GB of archives at a time and the archives are
pulled and verified off-box after every chunk.

**Artifacts.** The new floors are at
`che/bench/results/phase6/g1_floors_2026-09-08/` (24 archives, pulled and
hash-verified 2026-09-09; small files tracked). **Incident:** the first pull
went into `g1_floors/`, the 2026-08-10 batch's directory, and overwrote or
removed its 24 gitignored archives. Tracked files were restored from git;
raw checkpoint directories were untouched; the archives were rebuilt from
them and hashed to `SHA256_CKPT_rebuilt_2026-09-09.txt`. No number moves.
Full record: `g1_floors/README_ARCHIVES_REBUILT.md`. The pull script now
refuses a directory holding foreign archives.

**Owner is shown the branch before the grid starts**, per the G1.2 STOP.


## §7 PROPOSALS RULING — 0, 1, 2 adopted; 3 declined and replaced by an eval-only High readout (owner, 2026-09-18)

Transcribed in the same session it was issued, per the meta-rule (2026-07-28).
**Mid-grid and pre-unblind:** G1.3 chunks 1–2 are run, pulled and verified
(seeds 1–12, 10 arms, 120 of 252 runs; commits `f658bd3`, `17389cc`); the box
is paused; `run_p6_grid.sh` computes no cross-arm quantity and no analysis
stage has been invoked. **Owner attestation (2026-09-18, this session): no Phase-6
outcome mean, per-arm or cross-arm, has been computed or viewed by anyone.**
The builder's own check is weaker and is stated as such: no analysis output
exists under `che/bench/results/phase6/`, which shows the absence of an
artifact, not the absence of a look. The attestation is the owner's, and
proposals 1 and 2 rest on it.

Rules on the four proposals of `docs/venue_review_2026-08-16.md` §7, carried
AWAITING RULING by the 2026-08-16 and 2026-08-24 venue rulings. **That review
is not a ruling**; it binds only what this entry transcribes.

### THE RULING

> **Proposal 0 is ADOPTED.** The inert-share bias in the confirmatory contrast,
> and its direction, are registered below.
>
> **Proposal 1 (`ISO-4`) is ADOPTED** as a **sensitivity arm outside the
> confirmatory family**, k = 20, with the reading rule below.
>
> **Proposal 2 (T = 2000 subsample) is ADOPTED** as **DESCRIPTIVE ONLY**,
> 4 seeds per confirmatory arm, flagged **UNDERPOWERED**, graded by no test.
>
> **Proposal 3 (High-severity point) is DECLINED as written** (40 new training
> runs). It is **replaced by an eval-only High readout** of the checkpoints the
> grid already produces — **unconditional, run on every branch**, out of
> family, executed in the post-unblind evaluation stage beside Γ(t).

### Cost basis — re-derived this session, because the review's is stale

The review priced runs at 497 s and a ~$16.4 free reserve. Both have moved.

Per run, from the 2026-09-09 entry's measured **8.8 min/run including
archiving** at the measured **$1.2358/h**:

    8.8 / 60 × 1.2358 = $0.1813 per run          (review: $0.1706)

T = 2000 run length, from the same entry's 501 s train / 15 s eval, with
archiving taken as the remainder 528 − 501 − 15 = 12 s and **doubled** because
retention doubles (below):

    2 × 501 + 15 + 24 = 1041 s  →  1041 / 3600 × 1.2358 = $0.3574 per run

| # | runs | cost |
|---|---|---|
| 1 | 20 | 20 × 0.1813 = **$3.63** |
| 2 | 8 | 8 × 0.3574 = **$2.86** |
| 3 as written | 40 | 40 × 0.1813 = **$7.25** |
| 3 as replaced (eval-only) | 0 train, 128 evals | 128 × 15 s = 1920 s → **$0.66** |

Free reserve: $65 − $48.6 = $16.4 (`HANDOFF.md` §2), less **$2.2** (ladder
branch B, 2026-09-09), less **~$2** (the card-2 partial re-floor, estimated by
run count and **in no ledger** — `HANDOFF.md`, hardware facts) → **~$12.2**.
**Owner confirmed (2026-09-18) that ~$12.2 stands as the working reserve.**
Not itemised and so not deducted: the paused box's storage charges and the
~$1.5 of per-chunk setup (`HANDOFF.md` §1a). Both can only shrink the figure;
the adopted spend below leaves ~$5 of margin against them.

Adopted spend: $3.63 + $2.86 + $0.66 = **$7.15** against ~$12.2. All three as
written would be **$13.74** and do not fit. **This entry authorizes $7.15 as a reserve draw**, on the same
footing as the Γ(t) block (not an amendment to the $45.73 grid
authorization).

### Proposal 0 — what is registered

Transcribed from the review §4 and re-checked against `che/configs/p6_iso.yaml`
this session: 6 uniform components at weight 0.166667, of which `d_low` and
`d_high` are `kappa_A: 0.0, kappa_B: 0.0, delta: 1.0`. Phase 5 certified δ
inert (`phase5_report.md`, M5.5 final verdict).

1. **2/6 = 0.3333 of ISO's training episodes carry no behaviourally active
   element; 100 % of JOINT's carry both live couplings.** ISO's effective
   composition under the project's own certification is
   `{A 1/3, B 1/3, nothing 1/3}`.
2. **Direction: the bias inflates Γ.** A positive Γ is partly purchasable by
   JOINT's 1.5× larger share of behaviourally active training episodes.
3. **The generated header's `no-element 0.0000` is true nominally and false
   behaviourally.** Design v2 §2's defence of the *marginal* imbalance stands;
   design v2 §10 item 4's symmetry defence covers **test time only**.
4. **Disclosure is branch-invariant**, on the §4a precedent
   (`phase6_framing_branches.md`): it is a property of the design, not of the
   outcome, and is required on A, B, C and D alike.

**`p6_iso.yaml` is NOT edited or regenerated while the grid is open.** The
grid resumes against a stamped parameter identity and a pinned commit
(`51e489a`); a header-only regeneration changes the file the box hashes. The
registration lives in this entry and in a dated amendment to design v2 §2;
the config header is corrected **after** the last chunk is pulled.

### Proposal 1 — `ISO-4`, as adopted

**Arm.** One policy trained on the uniform 4-component mixture
{`a_low`, `b_low`, `a_high`, `b_high`} at weight 0.25 — `p6_iso.yaml` with the
two δ-only components removed and nothing else changed. Same architecture,
T\* = 1000, same eval config (`theta_star_holdout.yaml`), eval seed 0, 512
episodes. **Seeds 1..20**, the same integers as every other arm. k = 20 =
`K_SECONDARY`; no lock changes.

**Status: sensitivity arm. It is NOT a member of the confirmatory family.**
`SIDAK_M = 2`, `K_CONFIRMATORY`, and `m62_report.py::METRICS` are untouched
(instruments law, clause 2: a diagnostic is never added to a registered
family after registration). Γ remains JOINT − ISO as registered and remains
the only quantity that decides the branch.

**Estimand.** Γ₄ = JOINT − ISO-4 at θ\*, matched budget T = 1000, on both
co-primaries; and the bias estimate B̂ = ISO-4 − ISO. Unpaired, graded on the
contrast's own seed-dispersion SE (2026-08-03 amendment), CI conditional on
the common eval draw (§4b).

**Reading rule, registered now and not revisable post-unblind:**

- Γ and Γ₄ are reported **side by side on every branch**, with B̂ and its CI.
- If Γ rejects on a co-primary and **Γ₄'s CI on that co-primary includes 0 or
  its sign is opposite**, the paper states that the effect **does not survive
  the inert-share correction**, in the abstract-level summary and not only in
  an appendix. **The branch label does not change** — it is fixed by Γ — but
  branch A/B text may not describe the effect as a composition effect without
  that qualifier.
- If Γ is null and Γ₄ is null, Γ₄ is quoted as a second exclusion bound.
- If Γ is null and Γ₄ rejects **negative**, it is reported under branch D's
  framing (matched-budget asymmetry) as a secondary observation, never as a
  confirmatory finding.
- **No magnitude threshold on B̂ is introduced**, now or later.

**Design-stage power (an UPPER bound, labelled as one).** No floor exists for
ISO-4; this uses ISO's 2026-09-08 floors as a stand-in, which the
per-artifact rule says is an assumption and not a measurement.

    completion: sqrt(0.0281²/20 + 0.0598²/46)
              = sqrt(0.00003948 + 0.00007774) = 0.01083
    survival:   sqrt(0.0070²/20 + 0.0129²/46)
              = sqrt(0.00000245 + 0.00000362) = 0.00246

    MDE80 at the Šidák z-sum 3.0781 (conservative for an out-of-family arm):
    completion 0.0333, survival 0.0076

against the confirmatory contrast's own 0.0300 / 0.0067 at k = 46
(`sqrt((0.0281² + 0.0598²)/46) = 0.00974`,
`sqrt((0.0070² + 0.0129²)/46) = 0.00216`, each × 3.0781). JOINT's dispersion dominates both,
which is why k = 20 on the quiet arm costs almost nothing in resolution.
**Realized power is reported, not re-engineered.**

**Execution constraints.**

- **Its own invocation and its own `$OUT`.** `run_p6_grid.sh` stamps the arm
  set and refuses a mismatched resume; the open grid's stamp is not touched.
- **Same card as the seeds it is compared against, where possible.** Seeds
  1–12 already ran; ISO-4's seeds 1–12 are a backfill. If the paused box is
  resumed, the card is common and the §1a common-mode argument holds. If it
  is not, the card goes in `cards.txt` and **the paper reports the block
  structure**; the cost is power, not validity, on the §1a reasoning.
- **The science tree must be identical to `51e489a`.** The ISO-4 commit adds
  a generated config and its test only. The job script asserts
  `git diff 51e489a..HEAD -- che/env che/train che/eval` is empty and records
  both hashes in provenance.
- `make_phase6_configs.py` emits `p6_iso4.yaml`; `test_phase6_configs.py`
  re-derives its weights. **No existing generated file changes.**
- Blinding is unchanged: the ISO-4 invocation computes no cross-arm quantity.

### Proposal 2 — T = 2000 subsample, as adopted

**What runs.** Fresh runs of ISO and JOINT at **T = 2000, seeds 1–4** (8
runs), same eval protocol, own `$OUT`. `T_STAR` stays 1000 and the primary
estimand is unchanged: Γ at matched budget T = 1000, *"at convergence" is
never claimed anywhere* (T\* ruling). Checkpoint retention follows the locked
**relationship**, not the number: `T / (2 × ckpt_interval) + 1` = **21** at
T = 2000 (`docs/locks.yaml`), supplied by a generated `_t2000` config variant
and asserted by test, never by a command-line flag.

Verified this session: `che/train/ippo.py` and `che/train/pbt.py` carry no
learning-rate schedule (no anneal/warmup), so updates 1–1000 of a T = 2000
run are the same procedure as a T = 1000 run and the curves are comparable.

**Why it is descriptive only.** At 4 seeds per arm, on the 2026-09-08 floors:

    sd(Γ) = sqrt((0.0281² + 0.0598²)/4) = 0.0330  →  MDE80 = 3.0781 × 0.0330 = 0.1017

against a 0.03 target band. **It cannot test anything and is flagged
UNDERPOWERED under the bars-come-with-floors rule.**

**What is reported:** per-arm learning curves to T = 2000 with seed spread,
and Γ(2000) with its CI, labelled descriptive. **What it may be cited for:**
whether the differential drift measured at T = 1000 (review §6 item 1: 0.01209
per 100 updates) visibly persists, closes or reverses. **What it may not be
cited for:** any claim that Γ "holds" or "vanishes" at T = 2000. It does not
replace the registered Γ(t) sign-stability rule and enters no branch decision.

Distinct from the T = 2000 the T\* ruling **declined**: that was the whole
grid; this is an 8-run robustness figure.

### Proposal 3 — declined as written, replaced by an eval-only High readout

**Why the 40-run version is declined.** Closing its design showed that the
review's "2 arms × k = 20" names no design that is both held out and clean:

- **β = 0.70 is a training severity in both arms** (`p6_iso.yaml`,
  `p6_joint.yaml`; design v2 §1), so new runs of the *registered* mixtures
  buy nothing a re-evaluation of the existing checkpoints does not.
- **Making High genuinely held out** means retraining on {0.43, 0.49} and
  testing at 0.70: that puts θ\*'s severity into a training set (the trap
  design v2 §1 names), and turns the test from interpolation into
  **extrapolation beyond the training range**, which confounds composition
  with severity extrapolation. A result there could not be read either way.
- It costs $7.25 of a ~$12.2 reserve for ~4.9 pt / ~7.7 pt resolution.

**What replaces it — the High readout.** Every T\* = 1000 checkpoint of ISO,
JOINT (k = 46 each) and ISO-4 (k = 20) is evaluated once more under
`che/configs/joint_high.yaml`, eval seed 0, 512 episodes. Verified this
session: comments stripped, `joint_high.yaml` differs from
`theta_star_holdout.yaml` in **exactly one line, `beta: 0.49 → 0.70`** — it
*is* θ\* moved to High — and the harness already supports declared
cross-config evaluation (`--allow-hash`, as `run_p6_grid.sh` uses for θ\*).

**Estimand.** Γ_H = J_High(π_joint) − J_High(π_iso), all-on at β = 0.70,
matched budget T = 1000, both co-primaries, unpaired, graded on the contrast's
own seed-dispersion SE, CI conditional on the common eval draw. Γ_H,4 =
JOINT − ISO-4 is reported beside it with no reading rule of its own.

**Status.** Secondary, **out of family** — `SIDAK_M = 2` and
`m62_report.py::METRICS` untouched. **It never decides or relabels a branch.**

**It is unconditional, and that is deliberate.** At $0.66 there is no budget
case for running it on branch C only, and §4a's own principle applies:
running or reporting it only when the outcome makes it useful would be
**outcome-dependent disclosure**. It runs and is reported on A, B, C and D.

**It is NOT a held-out test, and the entry says so before a reviewer does.**
JOINT trained on *this exact configuration* at weight 1/2. ISO trained at
β = 0.70 on A-only, B-only and δ-only at weight 1/6 each and **never on any
all-on configuration**. Every known asymmetry favours JOINT: in-distribution
evaluation, a 3× larger budget share on the evaluated configuration than ISO
gives any one High component, and the proposal-0 inert share. **That
one-sidedness is what makes the reading rule asymmetric:**

- **Γ_H null → an *a fortiori* exclusion**, and the only outcome this
  readout can establish: *"no gap larger than X at High even where JOINT
  trained on the evaluated configuration and ISO never saw a composed one."*
  Quoted as an exclusion with X from the grid's own seed dispersion, never as
  an absence.
- **Γ_H positive → NOT separable from in-distribution advantage.** Reported
  in those words. It may **not** be cited as compositional generalization, on
  any branch, and it may not be used to soften a θ\* null.
- **Γ_H negative → exploratory**, reported under branch D's
  matched-budget-asymmetry framing, never as a finding.
- **No magnitude threshold is introduced**, now or post-unblind.

**What it is blind to (instruments law).** Coupling A is **"marginal by
construction" at High** — the supercritical fire consumes the fuel collapse
would ignite (`coupling_a_lock.md`; design v2 §1) — while Coupling B's
8.8-point survival effect lives there (`phase4_report.md` Result 1). So High
is the **mirror image** of the Medium siting, not its remedy: at Medium B is
quiet and A is live; at High A is marginal and B is live. **By the project's
own locks there is no severity at which both couplings are strongly
behaviourally live**, and the paper states that once, beside §4a, on every
branch. The High readout adds **breadth in severity**; it does not supply a
test of composition where both elements bite.

**Floors, per-artifact and per-hardware, at no training cost.** The
2026-09-08 re-floor left 8 ISO + 8 JOINT same-seed rep checkpoints
(`g1_floors_2026-09-08/`, 16 of its 24 archives). They are evaluated under
`joint_high.yaml` **in the same session and on the same card** as the High
readout, giving the reproducibility floor of the artifact actually graded.
ISO-4 has no rep set; its High numbers ship **UNDERPOWERED-flagged for the
beat-reproducibility hurdle** and are graded on seed dispersion only.

**Design-stage resolution (an assumption, labelled as one).** No High
dispersion exists for these artifacts. Using the single-element High cells
quoted in the review §5 — completion 0.0485 / 0.0517, survival 0.0794 /
0.0783, **n = 3, T = 500, transfer to T = 1000 and to mixture-trained
policies assumed** — at the k = 46 the readout inherits for free:

    completion: sqrt((0.0485² + 0.0517²)/46) = sqrt(0.00502514/46) = 0.01045
    survival:   sqrt((0.0794² + 0.0783²)/46) = sqrt(0.01243525/46) = 0.01644

    MDE80 at z-sum 3.0781:  completion 0.0322,  survival 0.0506

against 0.0488 / 0.0768 for the declined k = 20 version: **better resolution
than the proposal it replaces, at a tenth of the cost.** κ_B's own 8.8-point
survival effect is resolvable on this basis; realized power is reported, not
re-engineered.

**Cost.** 92 + 20 + 16 = 128 evals × 15 s (measured, 2026-09-09 entry) =
1920 s → 1920 / 3600 × 1.2358 = **$0.66**. It rides the rental that runs the
registered post-unblind Γ(t) block.

**Execution constraints.** Post-unblind evaluation stage only, on the frozen
tree, from the hash-verified archives; `ckpt_step == T*` asserted per
checkpoint exactly as the grid asserts it; outputs to their own directory;
the cross-config evaluation is **declared** (`--allow-hash`), never smuggled.
The grid script is not modified.

### What this ruling does NOT do

- **It changes no lock.** `SIDAK_M`, `K_CONFIRMATORY` (46 by ladder branch B),
  `K_SECONDARY`, `T_STAR`, `METRICS` and every entry in `docs/locks.yaml` are
  untouched.
- **It does not edit the branch table.** The four branches stand verbatim;
  Γ₄ and Γ_H qualify branch text, they never relabel a branch.
- **It does not touch the open grid** — not its stamp, its commit, its
  configs or its run order. Chunks 3–5 proceed exactly as registered.
- **It does not authorize unblinding**, which stays a separate human-gated
  step on a frozen tree, and now waits on the ISO-4 and T = 2000 runs too.

### OWED — created or changed by this ruling

1. **Builder:** `p6_iso4.yaml` + the `_t2000` variants via
   `make_phase6_configs.py`, with tests; separate invocations with their own
   `$OUT` and stamps; the science-tree identity assertion against `51e489a`.
2. **Builder:** dated amendment to design v2 §2 carrying proposal 0's four
   points; the same text into `paper/00_common_spine.md` as branch-invariant.
3. **Builder:** a post-unblind High-readout script (128 declared
   cross-config evals under `joint_high.yaml`, own output directory,
   `ckpt_step == T*` asserted), with a test that it cannot run before the
   unblind step and that it touches neither `METRICS` nor the grid script.
   The "no severity with both couplings strongly live" statement into
   `paper/00_common_spine.md` beside §4a, branch-invariant.
4. **Owner confirmations: DISCHARGED in this entry** — the no-outcome-seen
   attestation and the reserve figure, both above.
5. **After the last chunk is pulled:** correct the `no-element` header line
   in the generated ISO config (proposal 0, last paragraph).
6. **`HANDOFF.md` §2a:** strike "Four proposals are OWED RULING" and point
   here.

### What this entry changes in the tree, in this commit

- `docs/decision_log.md`: this entry.
- `HANDOFF.md`: §2a pointer updated.
- **No constant, config, lock, test, script or analysis threshold changes.**
  Every implementation item above lands in its own later commit.


## CARD RULING — the Phase-6 grid remainder runs on an RTX 5090 (owner, 2026-09-21)

**Ruled:** G1.3 chunks 3–5 (seeds 13–46, 132 runs) and the post-unblind /
§7 blocks run on an **RTX GeForce 5090 (32,607 MiB)**, not an RTX PRO 6000.
Seeds 1–12 (120 runs) stay as-run on the PRO 6000. Issued pre-unblind, with
no cross-arm quantity computed.

### 1. This does not need a new authorization — the chunking ruling already covers it

The 2026-08-14 chunking ruling states chunks "may therefore run on different
rented cards", and gives the safety argument: seed-major order puts **both
arms of every seed on the same card**, so a card effect is common-mode within
a seed and **cancels in Γ**. The grid is stopped at **seed 12 — a seed
boundary**, which is exactly the condition that argument requires. Validity is
untouched; the cost is power, and realized power is **reported, not
re-engineered**.

What is new here is that the switch crosses a card *model*, not just a box.
That is a larger block effect than the one the chunking ruling costed. It
remains inside the same argument, and the stated headroom (sd(Γ) may inflate
1.93× completion / 3.14× survival before power falls to 80 %) is the budget it
spends against.

### 2. What is being corrected: a conflation, not a waiver

`decision_log.md:1570` reads: *"62,084 steps/s for the gate config or 257 s/run
single-policy, and the 5090 is out."* That sentence bundles two workloads and
the exclusion has since been read as global.

**The exclusion was measured on `gate_pop12.yaml`** — a **population** config
(12 members × 128 envs) needing ~61.6 GiB at autotune. Its own header calls
itself "the Phase-6/7 spending configuration", but **the Phase-6 grid does not
run it.** The grid runs `p6_iso.yaml` and its siblings: **single learner, 256
envs, no `pop_size`.**

This entry does not reopen the gate-config exclusion. **If Phase 7 runs the
PBT population path, the 5090 remains out on 31.8 GiB.**

### 3. Evidence for the single-learner path (verified this session)

- `p6_iso.yaml`'s `env:` and `train:` blocks are **identical** to
  `severity_medium.yaml` — 64², 12 agents, horizon 256, obs_window 9,
  obs_version 3, 32 food; 256 envs, rollout 128, 4 minibatches, 4 epochs.
  The only additions are `ckpt_max_to_keep: 11` (disk, not VRAM) and the
  `mixture:` block.
- **`severity_medium.yaml` / `severity_high.yaml` ran on an RTX 5090** in
  M5.1, M5.1b, M5.1c, M5.1e, M5.3 and the Phase-5 pre-task. Each
  `provenance.txt` records `gpu: NVIDIA GeForce RTX 5090`.
- The mixture machinery is not a memory risk: M6.0 measured traced-θ at
  **+30,720 B peak (+0.00004 %)** and ≤ 0.6 % throughput.

### 4. What is NOT measured — stated so it is chosen, not discovered

**No peak-memory figure exists for any single-learner config.** `memprobe.py`
was written for the population path and only ever ran on `gate_pop12.yaml`.
The Phase-5 5090 runs prove the config *fit* 31.8 GiB at their commits; they
do not say with how much headroom. G1.0b's nine added diagnostic channels were
measured at **< 0.25 % throughput** but their **memory cost was not reported**.

The footprint claim is therefore an **inference**, and it is discharged by a
**compile go/no-go on the first run**, not by advance measurement. If it OOMs
at autotune the fallback is a PRO 6000. **`--xla_gpu_autotune_level=0` is not
available** (2026-07-30: it bought a fit at 16.4× the cost).

### 5. Throughput expectation — an estimate, not a trigger

| card | config | updates | s/run | n |
|---|---|---|---|---|
| RTX 5090 | `severity_medium.yaml` | 500 | **283.9** (282–286) | 11 |
| RTX PRO 6000 | `p6_iso.yaml` | 1000 | **501.2** (sd 1.3) | 120 |

Attributing the 1000-update run's fixed overhead two ways (naive halving vs.
subtracting 42.6 s of non-steady time, derived from 32,768 env-steps/update at
the measured 71,450 steps/s) brackets the 5090 at **1.05×–1.13× slower**.

Per the throughput-gate rule this is an **estimate and gates nothing**.
Realized per-run time is read from `timings.txt` on the artifact itself.

### 6. Cost — at the rate measured this session

**Rate: $0.549/h** (owner-reported, this box, 2026-09-21).

Remaining work is **28.49 GPU-bound hours + 0.56 h CPU/disk**, derived this
session from the 120-run `timings.txt` (132 grid runs at 516.4 s GPU + 12 s
archive; ISO-4 k = 20; T = 2000 k = 4 × 2; High readout 128 evals; Γ(t)
920 evals).

| card | hours | cost |
|---|---|---|
| 5090 @ 1.05× | 30.47 | **$16.73** |
| 5090 @ 1.13× | 32.75 | **$17.98** |
| PRO 6000 @ $1.2358/h (projected) | 29.05 | $35.90 |
| PRO 6000 @ ~$1.50/h (billed precedent) | 29.05 | $43.57 |

**Saving: $17.92–$26.84** depending on which PRO 6000 rate is the counterfactual
and where in the bracket the 5090 lands.

**Derived consequence, recorded not acted on:** the §7 blocks were authorized
at **$7.15** on PRO 6000 pricing ($0.1813/run). Re-derived at $0.549/h they cost
**$3.33–$3.58** (ISO-4 $1.69–1.82 + T=2000 $1.33–1.43 + High readout
$0.31–0.34). The **$7.15 authorization stands as-registered** — an under-spend
needs no amendment — and the difference returns to the ~$12.2 working reserve.

### 7. Obligations carried

1. **`cards.txt` records the block structure** — mechanized: `run_p6_grid.sh`
   writes `.manifest/<tag>.card` per run and aggregates. **The paper reports
   the two-card structure**, per the chunking ruling.
2. **No seed may be split across the two cards.** The stop at seed 12 satisfies
   this; `MAX_RUNS` finishes a seed before stopping.
3. **Realized power is reported, never re-engineered.**

### 8. Γ₄ is a cross-card contrast — PROVISIONALLY ACCEPTED with disclosure

ISO-4 (§7 proposal 1, k = 20, seeds 1–20) would run **entirely on the 5090**,
while its comparator ISO has seeds 1–12 on the PRO 6000. **Γ₄ therefore
lacks the within-seed cancellation** that protects the primary Γ. ISO-4 is
**out of family**, so no confirmatory quantity moves and its registered reading
rule is unaffected.

**Owner ruled 2026-09-21: ACCEPT the cross-card Γ₄ with disclosure --
explicitly PROVISIONAL ("for now").** The disclosure is branch-invariant, on the
§4a precedent: it is a property of the design, not of the outcome.

**The reversal window closes when ISO-4 runs.** Until then the alternative --
ISO-4 seeds 1–12 on a PRO 6000 — costs only the rental. After ISO-4 has run on
the 5090, reversing means re-running it. ISO-4 is **not** on the critical path
for the grid, so this decision can be revisited at any point before that block
is launched, and is flagged here so that it is revisited deliberately rather
than by default.


### AMENDMENT to the CARD RULING — realized timing, measured (2026-09-22)

§5 registered the 1.05×–1.13× bracket as an **estimate that gates nothing**
and said realized per-run time is read from `timings.txt` on the artifact.
Chunk 3 is complete (seeds 13–18, 60 runs, all verified), so it is read here.
**This records a measurement the ruling anticipated; it changes no decision,
no constant and no threshold.**

| | PRO 6000 (n=120) | RTX 5090 (n=60) | ratio |
|---|---|---|---|
| train, T = 1000 | 501.23 s (sd 1.26) | **519.35 s** (sd 0.57) | 1.0361× |
| eval, 512 eps | 15.17 s (sd 0.52) | **9.40 s** (sd 0.49) | **0.6198×** |
| per-run marginal | 516.4 s | **528.8 s** | **1.0239×** |

**The registered bracket was pessimistic, and the reason is worth keeping.**
It was derived by scaling the whole GPU portion by the steady-state throughput
ratio (71,450 → 66,400 steps/s = 1.076×). But a run is not all steady-state
compute: compile, checkpoint I/O and setup do not scale with steps/s, so the
throughput ratio is an **upper bound** on the run-time ratio, not an estimate
of it. Realized train is 1.036×, per-run 1.024×.

**The eval figure is FASTER on the slower card and is UNEXPLAINED.** 9.40 s
against 15.17 s, consistent across 60 runs at sd 0.49. No mechanism is
asserted here; candidates (checkpoint-load I/O, host CPU) are untested. It is
recorded as measured and unexplained rather than rationalised.

**Cost, re-derived:** 72 grid runs + the §7 and post-unblind blocks =
**18.99 h → $10.43** at the measured $0.549/h. Phase-6 grid spend stays far
inside the $45.73 authorization.

#### OWED — a cross-card eval floor, raised by the eval anomaly

Within the grid this does not arise: **each run's eval executes on the same
card that trained it**, so no cross-card eval comparison exists in the
confirmatory data. But **Γ(t) and the High readout evaluate retained
checkpoints post-unblind**, on whatever card is rented then — which will in
general differ from the card that trained seeds 1–12 (PRO 6000) or 13–46
(5090). Whether evaluating one checkpoint on two cards yields identical
metrics is **unmeasured**. Per the per-artifact floor amendment (2026-08-02),
that comparison needs **its own floor, measured on the artifact being graded**
— A-vs-A and B-vs-B, not a single cross-comparison. A 1.6× timing difference
is not evidence of a numerical difference, and is not evidence against one
either. **Flagged pre-unblind; owed before Γ(t) is read.**


## SINGLE-CARD CONFIRMATORY RULING — ISO/JOINT seeds 1–12 re-run on the 5090 (owner, 2026-09-22)

**Ruled:** the 24 confirmatory runs at seeds 1–12 (ISO and JOINT) are **re-run
on the RTX 5090**. Those runs **supersede** their PRO 6000 counterparts for the
confirmatory contrast Γ. The PRO 6000 versions are **retained, not deleted**,
and remain committed. **Γ becomes single-card at k = 46.**

Issued **pre-unblind, with nothing seen** — the §7 attestation (no Phase-6
outcome mean, per-arm or cross-arm, computed or viewed) still holds and is what
makes this **provably not outcome-selected**. That timing is the load-bearing
fact: the identical decision taken after unblinding would be indefensible.

### Why — the chunking ruling's argument covers less than it appears to

The 2026-08-14 argument is that a card effect is common-mode within a seed and
cancels in Γ. Checked properly this session, it is **exact rather than
approximate, for additive effects only**:

ISO and JOINT both run seeds 1–46 with an **identical card split** (12 on the
PRO 6000, 34 on the 5090), so an additive per-card offset δ enters both arm
means as the same `(12·δ_P + 34·δ_5)/46` and cancels exactly in the difference.
The eight secondary arms are likewise mutually balanced (all seeds 1–20, split
12/8), and **no registered contrast crosses the two families** —
`m62_report.py` sets `conf = ("iso", "joint")` at `SIDAK_M = 2`, and the sweep
analyses are within-family.

**What balance does NOT cover is a card × arm INTERACTION.** If the 5090 moved
JOINT differently from ISO, Γ absorbs
`(34/46)(δ_5^J − δ_5^I) + (12/46)(δ_P^J − δ_P^I)` and no balance removes it.
The chunking ruling never addressed this term.

**The mechanism argument against an interaction is strong but is not a
measurement.** After M6.0, θ is **traced, not a compile-time constant**
(`config.py`: only the four traced fields may be patched, everything else is
static; the observable surface has fixed width regardless of mixture). ISO and
JOINT therefore compile to the **same executable with the same kernel
selection**, differing only in runtime values, and XLA autotuning selects on
shape rather than on data. An interaction would require a card's numerics to
depend on the values flowing through an identical kernel.

This ruling buys the measurement instead of relying on the argument.

### Why it could not simply be checked

The direct diagnostic — ISO's mean over seeds 1–12 against its mean over 13–18
— is **embargoed**: the attestation covers per-arm means, not merely cross-arm
ones, and a within-arm card comparison is still a per-arm mean. It is
computable only post-unblind. Spending $1.94 now is cheaper than pre-registering
a diagnostic whose result could only ever arrive too late to act on.

### Cost and layout

**24 runs × 528.8 s = 3.53 h ≈ $1.94** at the measured $0.549/h, against the
~$12.2 reserve. Runs **after chunk 5** — two grid jobs cannot share the card,
because JAX preallocates 75 % of it.

Own output directory and own stamp, since the main grid's manifest already
marks these tags done:

    OUT=che/bench/results/phase6/g1_conf_s1_12_5090 K_CONF=12 K_SEC=0 \
      MIN_FREE_GB=10 GIT_COMMIT=c3ae125... bash che/scripts/run_p6_grid.sh

### Scope — what this does NOT change

- **No constant, threshold, lock, config or analysis family moves.** k stays
  46/20, T\* stays 1000, the eval draw stays seed 0 / 512 episodes, `METRICS`
  and `SIDAK_M = 2` are untouched.
- **The secondary arms stay two-card** and stay non-verdict-bearing; their
  balance argument is unaffected and still carries.
- **The chunking ruling is not reopened.** It remains correct for what it
  claimed; this entry records the interaction term it did not cover.
- **`cards.txt` obligation persists** — the paper still reports the grid's card
  structure, which after this is single-card confirmatory and two-card
  secondary.


### AMENDMENT — extended to a FULL single-card conversion (owner, 2026-09-22)

The SINGLE-CARD CONFIRMATORY RULING above is **extended**. Instead of 24
confirmatory runs, the re-card covers **all 120 runs at seeds 1–12 (all ten
arms)**, plus a **G1.2-protocol re-floor on the 5090 (24 runs)**. On
completion every run and every floor in Phase 6 sits on one card.

**Why the floor is included — the conf-only option relocated the problem.**
Design v2 states floors are **per-hardware AND per-artifact**, and that a
released card means "the next trip re-floors". The G1.2 re-floor ran on the
PRO 6000 (2026-09-08), and `m62_report.py` feeds those floors into the per-arm
power diagnostics, `sd(Γ)`, MDE₈₀ and `k_required` — every power statement the
paper reports. A single-card 5090 grid whose power analysis is calibrated on a
PRO 6000 moves the inconsistency from the runs into the methods section; it
does not remove it.

**Owner's reasoning, recorded because it is the operative one:** the risk is
asymmetric. The increment over the conf-only option is **$9.68, ~2 % of the
GPU budget**; the downside insured against is a rejection cycle whose calendar
cost is **unmeasured** — `HANDOFF.md` records that TMLR publishes no total time
to decision, marks it UNVERIFIED, and forbids runway arithmetic until it is
checked. Against a ~7-month deadline the unpriceable resource is calendar, not
money. Owner added **$20 to the reserve** as margin.

**The builder's prior recommendation (conf-only, on value-for-money) is
RETRACTED**, and recorded rather than quietly dropped because the error is
instructive: it optimised the measurable variable ($9.68) against a risk it
had not priced, which is the same class of error as grading a bar without a
floor.

**Cost:** base **$21.88 (39.9 GPU-h)**, worst case **$24.13 (44.0 h)** with the
ladder tail. The tail is **bounded** — `ladder.json` carries `k_cap: 60`, so at
most 14 extra seeds (28 runs, $2.26). Even at worst case this leaves **$21.60
of the $45.73 grid authorization unspent**.

**Order — chunks 4 and 5 run FIRST, deliberately.** It is the fail-safe
ordering: a complete 252-run artifact exists on disk at every moment, so a box
failure during the re-card degrades to a publishable two-card grid rather than
to a partial one. Nothing in the re-floor or re-card depends on chunk order.

**Known operational consequence, stated so it is handled rather than
discovered.** `grid_params.txt` records `k_conf: 46`, stamped 2026-09-08, and a
resume under a different k is refused by design. So **if the 5090 floors raise
k above 46, the extra seeds land in their own `$OUT`** — reordering would not
have avoided this, because the stamp was fixed two weeks ago. The re-card is
likewise its own `$OUT`. **The confirmatory arm may therefore span more than
one output directory, and the analysis must merge them deliberately.**

**Ladder outcomes, both already pre-registered** (design v2): floors smaller →
record the surplus and proceed, nothing to run; floors larger → top up to
k_req, capped at 60. No run already completed is invalidated either way — k
governs how many seeds exist, not whether each is sound.

**Scope unchanged:** no constant, threshold, lock, config or analysis family
moves. `METRICS` and `SIDAK_M = 2` untouched. The PRO 6000 runs are **retained**
and become a free 12-seed, 10-arm card-effect diagnostic.


## ENDPOINT CONFOUND — Γ mixes dose with composition; the SWEEP is the matched instrument (builder finding, 2026-09-22)

Raised by the owner while the grid ran ("mostly there is joint vs iso"), i.e.
the observation that joint-vs-isolated training comparisons are common in
multi-task RL, domain randomization and curriculum learning, so the ISO/JOINT
contrast does not by itself separate this work from that literature. Checked
against the generated configs this session. **The owner is right, and the
separation lives somewhere other than where the spine currently puts it.**

### Measured marginals — read off the generated configs, this session

| arm | A | B | co-occurrence | no-element |
|---|---|---|---|---|
| `p6_iso` | 0.3333 | 0.3333 | 0.0000 | 0.0000 |
| `p6_joint` | **1.0000** | **1.0000** | 1.0000 | 0.0000 |
| `p6_sweep_c50_p000` | 0.5000 | 0.5000 | 0.0000 | 0.0000 |
| `p6_sweep_c50_p250` | 0.5000 | 0.5000 | 0.2500 | 0.2500 |
| `p6_sweep_c50_p500` | 0.5000 | 0.5000 | 0.5000 | 0.5000 |

**Γ confounds dose with composition.** JOINT sees each element **3× more
often** than ISO *and* sees them co-occur. Design v2 §10 item 3 already
flagged this ("the confirmatory contrast differs in per-element marginal
**and** in co-occurrence"); this entry records the magnitude and its
consequence for positioning.

**The sweep is the matched instrument.** A and B are held at exactly 0.5
across all five points while co-occurrence moves 0 → 0.5. That is the
comparison standard joint-vs-iso work does **not** run: multi-task and
domain-randomization baselines almost always confound "saw more" with "saw it
combined". This is the real separation from that literature.

### Correction to the spine's DBCA framing

`paper/00_common_spine.md` §1 names the contribution via DBCA (Keysers et al.
2020) as "atom divergence → 0, compound divergence → max". **Measured, that
describes the SWEEP, not the endpoints.** At the endpoints atom frequencies
differ 3×, so atom divergence is substantial. The DBCA sentence must either
move to the sweep or be qualified where it stands. **Not corrected in this
commit** — `p6_iso.yaml` must not be regenerated while the grid is open, and
this is a prose change owed to the writing pass.

### The sweep is not perfectly clean either, and cannot be

Holding A and B at 0.5 while raising co-occurrence **forces the no-element
share up with it** (p = 0.5 → 50 % empty episodes). Per-element marginal,
co-occurrence and active-episode share cannot all be held fixed — the simplex
forbids it. The c = 0.4 identification family probes the same trade at a
different coverage. **State this rather than let a reviewer find it.**

### What this does NOT change

- **The sweep stays non-verdict-bearing.** It is not promoted, now or
  post-unblind; that would enlarge the registered family and inflate the
  correction. `m62_report.py::METRICS` and `SIDAK_M = 2` are untouched.
- No constant, threshold, lock or config changes. Nothing is regenerated.
- Γ remains the registered confirmatory contrast at matched budget T = 1000.

### Obligation — disclosure, branch-invariant

**§2 states the endpoint confound explicitly**, on the §4a precedent: it is a
property of the design, not of the outcome, and is owed on branches A–D
alike. Positioning leads with **matched-marginal composition variation under
causally coupled stressors**, not with "joint vs isolated" — the latter
claim-space is crowded and the former is the one the no-scoop checks found
empty.


## LADDER BRANCH C, AND THE CAP RAISED 60 → 72 (owner, 2026-09-22)

The 5090 re-floor (24 runs, G1.2 protocol, `g1_floors_5090`) returned
**BRANCH C**: `k_req` completion **72**, survival **3**, against
`k_cap: 60`. Registered action: *"PROCEED at k = 60 and DEGRADE HONESTLY,
never chase."* Realized completion power at k = 60 is **72.2 %**.

**RULED: the cap is raised to 72 and the confirmatory arms run at k = 72.**
This is a **deviation from a registered rule**, recorded as one, issued
**pre-unblind with no outcome seen**.

### Measured floors — 5090, sd only (means deliberately not read)

| arm | completion | survival |
|---|---|---|
| iso | 0.05867 | 0.01004 |
| joint | 0.05769 | 0.01116 |
| sweep_p500 | 0.01958 | 0.01301 |

Against the PRO 6000 floors: iso completion **2.09×**, joint completion
0.96×, iso survival 1.44×, joint survival 0.87×.

Completion power at the 0.03 target effect:

| floors | k = 46 | k = 60 | k = 72 |
|---|---|---|---|
| PRO 6000 | 80.1 % | 90.0 % | 94.7 % |
| **5090** | 59.3 % | **72.2 %** | **80.4 %** |

### The floor shift is NOT distinguishable from sampling noise

Each floor is estimated from **8 reps**. The 95 % CIs for sd all overlap —
iso completion PRO 6000 [0.0186, 0.0571] against 5090 [0.0388, 0.1194]. The
2.09× shift is within what an n = 8 variance estimate produces by chance.
**No claim is made that the 5090 is less reproducible.** The ladder acts on
point estimates, which is correct for a ladder and insufficient for a claim.

### Why raising the cap is not "chasing"

1. **`k_cap = 60` is a COST cap, not a statistical one.** Its own basis
   (`decision_log.md:2317`): *"k = 60 is +20 seeds/arm = +40 runs ≈ $7.62"*,
   i.e. ~$0.19/run on a PRO 6000. **On the 5090 a run costs $0.081** — the
   budget constraint that set the ceiling has fallen 2.3×. Honouring a budget
   cap whose budget no longer binds is not rigour.
2. **`k_req` is computed from FLOORS, not outcomes.** Floors are
   reproducibility reps at seed 0, which is excluded from the grid. No Γ, no
   per-arm grid mean, has been computed or viewed.
3. **Adding seeds raises power SYMMETRICALLY.** It cannot move Γ's sign or
   magnitude in any preferred direction. This is a *conservative* deviation,
   which is a different object from a self-serving one.

### Both analyses are reported

Seeds 1–60 are a **prefix** of seeds 1–72, so **the registered branch-C
analysis at k = 60 remains exactly computable** and is reported in full
alongside k = 72. Nothing is swapped after the fact.

**Primary is designated NOW, pre-unblind: k = 72.** The k = 60 registered-
ladder result is reported beside it with its UNDERPOWERED flag and realized
power stated, per branch C as written. **Owner may reverse this designation;
it must be reversed before unblinding or not at all.**

### Why returning to a PRO 6000 was REJECTED

It would mean **selecting hardware because its floor estimate was more
favourable**, when the CIs cannot distinguish the two. That is selection on a
measured quantity — the family of error the project's rules exist to prevent.
Note also that the 5090 gives iso 0.0587 and joint 0.0577, nearly identical,
which is what two configs differing only in mixture weights should produce;
the PRO 6000's 0.0281 / 0.0598 asymmetry has no mechanism and is **more
likely the outlier**. At ~$29 it may buy nothing.

### Cost and layout

**172 runs ≈ 25.3 GPU-h ≈ $13.87** at $0.549/h. Owner waived the budget
constraint for this decision ("I don't mind about the budget anymore"),
stating rigour as the operative criterion.

1. **Confirmatory, one directory, one stamp:** `g1_conf_5090`, seeded by
   copying conf seeds 13–46 (already 5090) from `g1_grid`, then run at
   `K_CONF=72 K_SEC=0`. Resume skips the copied seeds — **`manifest_complete`
   re-hashes every archive, so a bad copy fails loudly** — and runs seeds
   1–12 and 47–72. **76 runs.** Result: all 72 confirmatory seeds, one card,
   one stamp, no cross-directory merge for the primary contrast.
2. **Secondary re-card:** seeds 1–12, the 8 secondary arms, own directory.
   **96 runs.** `K_SECONDARY` stays **20**; secondaries are not extended.

### Scope — unchanged

`m62_report.py::METRICS`, `SIDAK_M = 2`, the 0.03 target effect, T\* = 1000,
the eval draw (seed 0, 512 episodes) and `K_SECONDARY = 20` are all
untouched. No lock, no config regenerated.
