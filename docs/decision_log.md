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
