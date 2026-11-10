# Interaction check at θ\* and at High: analysis plan (POST HOC)

Written 2026-10-14, **before any run**; **amended 2026-10-17, still before
any run**, on a blind review's design concerns (decision log: *PLAN
AMENDMENT*); and **amended again 2026-11-10, still before any run** (decision
log: *GO/NO-GO PROBE*). §11 and §12 list every change. Authorized by the
decision log's *PAPER V3* item 2(a): eval-only, labelled post hoc. Scope:
**θ\* and High** (*GO/NO-GO PROBE* item 2, which supersedes the "θ\* only" of
*PAPER V3 PHASE 1 START* item 2). No training of any kind.

**The amended text needs the owner's OK before any run** (§12). No eval has
run under any version of this plan.

`che/scripts/interaction_analysis.py` implements this plan. It refuses to run
unless this file is committed in git and unchanged since that commit. It also
refuses unless the eval run recorded this file's sha256 in its provenance, and
that hash matches the committed file. Any edit to this plan after the run
therefore shows up as a refusal, not as a silent change. A public timestamp
of this file, made before the run, lets a reader check outside this
repository that it existed before the run's recorded start (§10).

## 1. Status: what this analysis is and is not

- **Post hoc.** The check was proposed after the Phase-6 result was known
  (a professor's review, *PAPER V3* item 1(1)). It carries no confirmatory
  weight. Every place it appears, abstract included, labels it post hoc.
- **Out of the registered family.** It does not join the confirmatory family
  {Γ_completion, Γ_survival} (Šidák m = 2, `m62_report.py::SIDAK_M`). It
  changes no reading of Γ, Γ₄, B̂, Γ(t) or Γ_H, and no branch. Branch B stands
  (*PAPER V3*, "What changes, and what does not").
- **Its questions.**
  - At θ\*, do trained policies' outcomes show a *non-additive* interaction
    between Coupling A (collapse seeds fire) and Coupling B (smoke attenuates
    perception)? Put plainly: does the composition the registered test was
    about exist, measurably, at the point where it was tested?
  - At θ\*, with both couplings on, does opening the links (δ = 0 against
    θ\*'s δ = 1) change trained policies' outcomes? This measures directly
    the train/test mismatch that the "inert" label for communication denial
    is asked to make harmless (added by the amendment, §11).
  - At θ\* and at High, does each coupling, on its own, change trained
    policies' outcomes by an amount a training study of this project's size
    could detect? This is the **go/no-go question** (§7): it decides whether
    further GPU money is spent on an environment paper. It is a project
    decision, not a finding (added by the second amendment, §12).
  - At High, the first question again: do the two couplings' effects add?
- **Its use.** The owner ruled on 2026-10-19 that the check leaves the paper
  then being prepared (*NO INTERACTION CHECK BEFORE SUBMISSION*). That stands
  for that draft. This run is a probe for the owner's next decision. Whether
  any of its numbers enters a later paper is not decided here; if one does, it
  is labelled post hoc, as below.

## 2. Conditions

Nine environment configurations: five at θ\* and four at High.

**At θ\*.** The first four are θ\*
(`che/configs/theta_star_holdout.yaml`) with only κ_A and κ_B changed. The
fifth is θ\* with only δ changed. β = 0.49 and every other locked value stay at
θ\*'s value in all five.

| condition | config | κ_A | κ_B | δ |
|---|---|---|---|---|
| neither | `che/configs/interaction_neither.yaml` | 0 | 0 | θ\*'s (1.0) |
| A only | `che/configs/interaction_a_only.yaml` | θ\*'s (0.06) | 0 | θ\*'s |
| B only | `che/configs/interaction_b_only.yaml` | 0 | θ\*'s (1.0) | θ\*'s |
| both | `che/configs/theta_star_holdout.yaml` (θ\* itself) | θ\*'s | θ\*'s | θ\*'s |
| links open | `che/configs/interaction_links_open.yaml` | θ\*'s | θ\*'s | 0 |

**At High.** The same 2×2 on the all-on High configuration,
`che/configs/joint_high.yaml`, which is θ\* with only β changed, to the locked
High severity 0.70. Only κ_A and κ_B change; δ stays 1.0.

| condition | config | κ_A | κ_B | β |
|---|---|---|---|---|
| high neither | `che/configs/interaction_high_neither.yaml` | 0 | 0 | 0.70 |
| high A only | `che/configs/interaction_high_a_only.yaml` | 0.06 | 0 | 0.70 |
| high B only | `che/configs/interaction_high_b_only.yaml` | 0 | 1.0 | 0.70 |
| high both | `che/configs/joint_high.yaml` (itself) | 0.06 | 1.0 | 0.70 |

High is added because calibration found Coupling B nearly silent at θ\*'s
severity (its masking ceiling runs 0.028 / 0.130 / 0.419 across Low / Medium /
High, `kappa_b_lock.md`), so θ\* alone cannot say whether Coupling B ever
changes outcomes. There is no links-open condition at High.

The seven new configs are generated from their base files by
`che/scripts/make_interaction_configs.py`. `che/tests/test_interaction_check.py`
asserts that each loads to its base with exactly its κ or δ values replaced,
that "both" is θ\*'s own file, and that "high both" is `joint_high.yaml`.

With κ_A = 0, κ_B = 0 or δ = 0, the environment is the corresponding nested
model, bitwise, given the same PRNG keys (CLAUDE.md invariant 3;
`che/tests/test_nesting.py`).

## 3. Policies and eval draw

- **Policies:** the final checkpoint (update 1000 = T\*) of every run in:
  - ISO, seeds 1–72 (`g1_conf_5090/ckpt_iso_s*.tar.zst`);
  - JOINT, seeds 1–72 (`g1_conf_5090/ckpt_joint_s*.tar.zst`);
  - ISO-4, seeds 1–20 (`g1_iso4_5090/ckpt_iso4_s*.tar.zst`).

  That is 164 policies. Each archive is verified against its directory's
  `SHA256_CKPT.txt` (by basename) before extraction. A mismatch fails that
  policy's evals; it is not skipped silently.
- **Eval draw:** the registered one. `che/eval/harness.py`, policy
  stochastic as trained, 512 episodes, seed 0, at an explicit `--step 1000`,
  cross-config declared with `--allow-hash` (the pattern of
  `run_p6_post_unblind_evals.sh`). The written `ckpt_step` is re-asserted.
- **Common random numbers.** All nine conditions use the same eval seed. So
  each policy meets the same 512 initial states and the same random streams
  in every condition. By invariant 3, the conditions of one site differ only
  through the couplings and the links themselves. Across sites they also
  differ in β.
- **Main evals:** 164 policies × 9 conditions = **1476**.
- **Floor evals:** see §6. Checkpoints `iso_s1`, `joint_s1` and `iso4_s1`,
  each condition repeated 3 more times: 3 × 9 × 3 = **81**.
- **Total: 1557 evals.** Cost estimate, from *PAPER V3* item 5's measured
  per-eval times (9.40 s; mean 14.8 s): 1557 × 9.40 s ≈ 4.1 h to
  1557 × 14.8 s ≈ 6.4 h, plus archive extraction, setup and the checkpoint
  upload. **An estimate, not a trigger.** Realized time is read from the
  run's `timings.txt`.

## 4. Outcomes and estimands

- **Co-primaries:** completion and survival rate, the registered pair
  (`p6_unblind.FAMILY`). For policy i in condition c, J_i(c) is the metric's
  mean over the 512 episodes, as the harness's summary JSON records it.
- **The interaction, per policy and co-primary, at each site** (θ\*, and
  High with its own four conditions):

  I_i = J_i(both) − J_i(A only) − J_i(B only) + J_i(neither).

  I = 0 means the two couplings' effects add. I < 0 means the outcome under
  both is worse than the sum of the separate effects predicts (the couplings
  compound). I > 0 means it is better than additive (they overlap or offset).
- **The main effects, per policy and co-primary, at each site:**

  A_i = J_i(A only) − J_i(neither), B_i = J_i(B only) − J_i(neither).

  Each is one coupling's effect with the other switched off. A < 0 means
  Coupling A lowers the outcome for that policy. The second amendment moves
  these from description to a graded family (§5, §7, §12).
- **The links-open effect, per policy and co-primary:**

  D_i = J_i(links open) − J_i(both).

  D is the effect of opening the links (δ = 0 against δ = 1) with both
  couplings on. D > 0 means policies do better with the links open; D < 0
  means they do worse.
- **Descriptive, outside every family, no reading rule:**
  - the nine condition means per arm, for all four `m62_report.METRICS`;
  - I on the logit scale, at each site (§5).

## 5. Test and family correction

- **Per arm** a ∈ {ISO, JOINT, ISO-4}: Ī_a = the mean of I_i over the arm's
  k_a seeds, with s_a = their sd (ddof 1) and SE_a = s_a / √k_a. Because I_i
  is a within-policy contrast, its spread across seeds carries both seed
  variation and episode-sampling variation. This is the artifact's own seed
  dispersion (CLAUDE.md, amendment of 2026-08-03). D̄_a is formed the same way
  from D_i.
- **Pooled:** all 164 policies, stratified by arm. Ī_pool = Σ_a w_a Ī_a with
  w_a = k_a / 164. SE_pool = √(Σ_a w_a² s_a² / k_a). It answers "averaged over
  the study's policies, weighted by seed count". It does not assume the arms
  share one I. D̄_pool is formed the same way.
- **Families: three separate families of 8 intervals, and one family of 32.**
  - The interaction family at θ\*: 4 estimates (ISO, JOINT, ISO-4, pooled) × 2
    co-primaries of I = 8 intervals.
  - The links-open family: the same 4 estimates × 2 co-primaries of D = 8
    intervals.
  - The interaction family at High: the same 4 estimates × 2 co-primaries of
    High's I = 8 intervals. It is separate, so adding High changes no interval
    of the first two families.
  - The main-effects family: 2 sites × 2 couplings × 2 co-primaries × 4
    estimates = 32 intervals of A and B, formed per arm and pooled exactly as
    Ī is.

  In each family of 8, Šidák: α' = 1 − 0.95^(1/8), with two-sided z_α'
  (≈ 2.73). In the family of 32: α' = 1 − 0.95^(1/32), z_α' (≈ 3.15).
  Interval: estimate ± z_α' · SE. These are normal intervals, as the project's
  other contrasts use (Γ₄ at k = 20 included, *PRE-UNBLIND RULINGS* (v)).
  ISO-4's k = 20 is the smallest, and the report says so beside its row.
- **80 %-power MDE** for each estimate, from its observed SE:
  (z_α' + z_0.80) · SE (CLAUDE.md, "Power statements are 80 %-power MDEs").
  It is labelled "observed-SE MDE80". It is a detection limit, not a bound.
- **I on the logit scale (descriptive).** Per policy and site, I is recomputed
  on the logit of each of the four condition means, logit(p) = ln(p / (1 − p)).
  Per arm and pooled, it gets the same interval form. It is outside every
  family, and it has no reading rule. A policy with any of the four means
  at exactly 0 or 1 has no finite logit: it is left out of this block, and
  the report counts it. An arm left with fewer than two policies is reported
  as not computable, and so is the pool.
- **No cross-arm test.** Differences in I or D between arms are reported
  descriptively only. No reading rule is attached to them.

## 6. Floors (per artifact, on the run GPU)

- **Eval self-floor (A-vs-A).** For each of `iso_s1`, `joint_s1` and
  `iso4_s1`, every condition is evaluated three more times on the same card.
  Together with the main eval, that gives four copies per (checkpoint,
  condition). The analysis reports:
  - whether the copies are bitwise identical, per condition;
  - their per-metric sd;
  - the sd of I across the four copies (I recomputed from copy r of each
    condition), per checkpoint;
  - the sd of D across the four copies, per checkpoint, likewise;
  - the same for I at High and for each main effect at each site.

  Every condition is its own artifact, so each is floored separately
  (CLAUDE.md, per-artifact floors). The earlier finding that θ\* evals are
  deterministic on an RTX 5090 (`post_evalfloor_gamma_t_high.md`) covers
  θ\* only. It is not assumed for the other conditions. The copies' episode
  means are summed in float64.
- **Reproducibility hurdle.** If every copy is bitwise identical, the floor
  is zero and the hurdle is met. Otherwise, a rejection of I also needs
  |Ī| > 2 × (the largest floor sd of I), and a rejection of D needs
  |D̄| > 2 × (the largest floor sd of D). I at High and each main effect have
  their own hurdle, from their own floor sd (per site, co-primary and
  coupling). This is the post-hoc 2-sigma floor-grading convention, labelled
  as such.
- **Cross-card check (descriptive).** The "both" eval of every policy is
  compared with the grid's own θ\* eval of the same checkpoint
  (`g1_conf_5090/eval_*.json`, `g1_iso4_5090/eval_iso4_s*.json`). The report
  states how many of the 164 are identical on both co-primaries. If they all
  are, the run reproduces the registered evals. If not, the differences are
  reported, and the self-floor above decides how to read them. The "high
  both" eval of every policy is compared the same way with the post-unblind
  High readout's eval of the same checkpoint
  (`che/bench/results/phase6/post_high/evalhigh_*.json`).

## 7. Reading rules (fixed now)

For each of the 8 estimates of I at θ\*, separately for each of the 8 of D,
separately for each of the 8 of I at High, and for each of the 32 main
effects in their own family:

- **Detectable:** the Šidák interval excludes 0 and the hurdle of §6 is met.
  Report its sign and its size in the metric's own units. For survival, also
  report it in agents per episode (× 12 agents).
- **Not detectable:** otherwise. This is stated as an **exclusion with its
  bound**: "|I| < B at the family-corrected level" (or |D| for D), with
  B = max(|lower|, |upper|) of the Šidák interval, and the observed-SE MDE80
  beside it. It is never stated as "no interaction", "additive" or "no
  effect".
- **The headline, and when the arms disagree.** The paper's headline reading
  is the pooled pair (survival and completion), for I and for D, **only if
  the three arms' readings agree**: the same reading and, if detectable, the
  same sign. If the arms' readings differ in sign or in detectability, the
  headline is that **the answer depends on how the policy was trained**, and
  the pooled estimate is reported only as an average over the arms' different
  exposures (§8, item 8), not as the environment's own interaction. The
  per-arm rows are read with the same rule, in the same family.
- **Context, not a new threshold.** Every reading, detectable or not, is
  reported beside the main effects A and B for the same estimate, and beside
  Γ, the registered contrast (its estimate and registered interval, read from
  `che/bench/results/phase6/unblind/unblind.json`), in the same units, with
  survival also in agents per episode. No smallest effect of interest is set.
  A detectable but small I or D is read as small through that comparison.
- **The go/no-go reading** (second amendment, §12). It answers one
  question for the owner: is there evidence, cheap to get, that each coupling
  changes what happens to trained policies somewhere? It is fixed now so that
  it cannot be bent after the numbers are seen.
  - **A coupling bites in a cell** (a site and a co-primary) if and only if
    all three hold for its main effect there:
    1. the pooled estimate is detectable in the main-effects family (its
       Šidák interval excludes 0 and its hurdle of §6 is met);
    2. each of the three arms' estimates has the pooled estimate's sign;
    3. the pooled estimate's size is at least **the size bar**: the
       registered design's 80 %-power detection limit for that co-primary,
       (z_α + z_0.80) · sd(Γ), with z_α and sd(Γ) read from
       `che/bench/results/phase6/unblind/unblind.json`. From the committed
       file that is 0.0066 for survival (0.66 points, 0.08 of 12 agents) and
       0.0329 for completion (3.29 points).
  - **Why that bar.** A within-policy contrast under common random numbers
    can detect effects far smaller than any training study could. The bar
    asks for an effect at least as large as the smallest one the registered
    72-seed-per-arm design was built to detect. It is derived from a measured
    seed dispersion, and the quantity it grades has its own floor (§6). It is
    a proxy: an effect on evaluation outcomes is not an effect on learning
    (§8, item 2).
  - **The verdict.** **GO** if both couplings bite in at least one cell each.
    **PARTIAL** if exactly one does. **NO-GO** if neither does. Either sign
    counts: the question is whether a coupling changes outcomes.
  - **What it is for.** GO supports spending on the follow-up training study.
    NO-GO says the environment's couplings have no demonstrated effect on
    these policies, and the owner has said they would then look elsewhere.
    PARTIAL is the owner's call. The verdict is a decision aid. It is not a
    finding, and no paper may quote it as one.
- **A void reading.** If the floor block, a cross-card check or Γ's file
  cannot be read (missing files, failed evals), the analysis refuses. It does
  not report a partial family.

## 8. What this analysis is blind to

Stated here, and repeated wherever the result is reported:

1. **θ\* and High only.** It says nothing about Low (β = 0.43), where the
   couplings' strengths differ again (`theta_star_holdout.yaml` header,
   "WHY THE MIDDLE").
2. **Fixed policies.** It measures how the couplings act and combine for
   these trained policies at evaluation. A main effect says that switching a
   coupling on changes these policies' outcomes. It does not say that the
   coupling changes what a policy learns: that needs training with the
   coupling on and off. Nor does it measure whether training on co-occurring
   couplings teaches anything. That is Γ, the registered test.
3. **The additive scale.** I is computed on episode means of bounded rates.
   Ceiling and floor effects of a bounded rate can create or hide an
   additive interaction. The logit block shows I on one other scale,
   descriptively; it is not tested there or on any other scale.
4. **One eval draw.** Every interval is conditional on the single common
   draw (seed 0, 512 episodes), as every other Phase-6 interval is.
5. **Comms denial in the 2×2 is held fixed.** δ = 1.0 in all four
   interaction conditions at each site, so interactions involving comms
   denial are not measured. D measures opening the links only with both
   couplings on, at θ\* only: it does not say what opening the links does
   under one coupling or none, or at High.
6. **Not a cross-arm test.** I and D are within-policy contrasts. Whether
   they differ between ISO, JOINT and ISO-4 is reported but not tested.
7. **Post hoc.** The check was chosen with the Phase-6 result known, and
   amended after a blind review but before any run (§11). Its result cannot
   strengthen or weaken the registered conclusions. It can only describe the
   test point.
8. **The arms saw the nine conditions differently in training.** Each arm's
   I, D, A and B mix how the environment behaves with how familiar that arm's
   policies are with each condition. All training was at β ∈ {0.43, 0.70},
   never at θ\*'s 0.49. **High's β = 0.70 is a training severity,** so the
   High conditions are not held out: JOINT trained on "high both" itself, ISO
   and ISO-4 on "high A only" and "high B only" with the links open, and ISO
   on High's couplings-off configuration with the links denied, which is
   "high neither":
   - ISO trained on A-only and B-only components at δ = 0, and on
     comms-only components at δ = 1, which are the "neither" condition's
     couplings (`che/configs/p6_iso.yaml`);
   - ISO-4 trained on A-only and B-only components at δ = 0 only. It never
     saw δ = 1, which the four interaction conditions use, as θ\* does
     (`che/configs/p6_iso4.yaml`);
   - JOINT trained only with every element on (κ_A and κ_B at θ\*'s values,
     δ = 1), which is the "both" condition's couplings and links
     (`che/configs/p6_joint.yaml`). It never saw δ = 0.
   - No arm trained with both couplings on and the links open, the "links
     open" condition. ISO and ISO-4 met δ = 0 with one coupling at a time;
     JOINT never met it.

   This is why the per-arm rows are reported beside the pooled one, why
   the headline follows the pool only when the arms agree (§7), and why the
   go/no-go reading asks every arm to share the pooled sign. The pooled
   reading averages over these differences; it does not remove them.
9. **Policies without memory, at 1000 updates.** Every policy is a
   feed-forward network evaluated at the registered budget, where training
   had not plateaued. A coupling that does not bite here could still bite for
   a policy that remembers, or one trained longer.

## 9. Outputs, and verification without version history

All under `che/bench/results/phase6/post_v3_interaction/`:

- `evals/eval_<tag>_<cond>.{npz,json}`: the 1476 main evals;
- `floor/floor_<tag>_<cond>_rep<r>.{npz,json}`: the 81 floor evals;
- `timings.txt`, `provenance.txt` (it includes this file's sha256);
- `v3_interaction_results.tar.zst` with `SHA256_RESULTS.txt`. The run script
  asserts both before it exits 0 (CLAUDE.md, artifact persistence);
- written later by the analysis: `interaction_report.md`,
  `interaction_report.json` and `ANALYSIS_LOG.txt`;
- the timestamp proofs of §10: `PLAN.md.ots` and `SHA256_RESULTS.txt.ots`.

**Verification without version history.** `uv run python -m
che.scripts.interaction_analysis --verify` needs no git, so it runs from the
code supplement. It:

- checks this file's sha256 against the hash the committed report was made
  under and against every hash the run recorded in `provenance.txt`;
- checks that `.plan_at_run.md` is byte-identical to this file;
- checks that the run started after this file's commit, as the committed
  report records that commit's time;
- recomputes every analysed key of `interaction_report.json` (all but its
  provenance and timestamp) from the shipped evals and compares. Floats agree
  to a relative tolerance of 10⁻⁹, which covers float64 summation order
  across platforms; everything else agrees exactly;
- states what it cannot check: that this file was committed before the run
  (that needs version history; §10 is the outside check), the git tree's
  state when the report was made, and the results archive's hash if the
  archive is not shipped.

It writes nothing and logs nothing. The supplement ships what it needs: this
file, its proof, every eval JSON, the floor checkpoints' NPZ files (the main
evals of `iso_s1`, `joint_s1` and `iso4_s1` and every `floor/` file),
`provenance.txt`, `timings.txt`, `.plan_at_run.md`, `SHA256_RESULTS.txt` and
its proof, and the committed report.

## 10. Public timestamps

- **Before the run.** Once this text has the owner's OK and is committed, its
  sha256 is timestamped with OpenTimestamps, which anchors the hash in a
  Bitcoin block. The proof, `PLAN.md.ots`, is committed beside this file. The
  run does not start until the proof carries the Bitcoin attestation.
- **After the run.** Once the results archive's hash verifies on the laptop,
  `SHA256_RESULTS.txt` is timestamped the same way, and its proof is
  committed.
- **What this shows, and what it does not.** Anyone with the proofs can
  check, outside this repository, that this plan existed no later than the
  block that anchors it, which is before the run's recorded start, and that
  the results existed no later than their own block. A timestamp shows only
  that a file existed by a time. It cannot show that the run did not happen
  earlier: that still rests on the run's own record (`provenance.txt`) and on
  the analysis's refusal of a run dated before the plan's commit. Only the two
  hashes leave the laptop, to the public calendar servers. No name or account
  is involved.

## 11. Amendment record (2026-10-17, before any run)

The plan approved on 2026-10-16 (decision log: *PLAN OK*; sha256
`c3ec2dd147479b6b88ff36c30002d8e6e30873e997798b92935d8c40b2a1b809`) was
amended before any eval ran. A blind review of the paper raised six concerns
about the check's design (`paper/v3/review/blind_review.md`, "Design review
of the post hoc interaction check"). The builder set out options
(`paper/v3/review/blind_review_checks.md` §2), and the owner chose the
recommended one for each (decision log: *PLAN AMENDMENT*):

1. **The disagreement rule** (§7): the pooled headline holds only if the
   arms' readings agree.
2. **Context, not a threshold** (§7): every reading is reported beside A, B
   and Γ, in the same units.
3. **The logit block** (§5): I on the logit scale, descriptive.
4. **The links-open condition** (§2, §4–§7): θ\* with δ = 0, the contrast D,
   and its own family of 8. This answers owner question Q9. It raises the
   run from 692 evals to 865.
5. **Verification without version history** (§9).
6. **Public timestamps** (§10).

Two smaller changes follow from these: the floor's episode means are summed in
float64 (§6), so verification is robust across platforms, and the blind spots
(§8) cover the fifth condition.

**Unchanged:** the policies, the eval draw, the estimand I, its family of 8,
its intervals, its floor and hurdle, its reading rule, the cross-card check,
and the labels: post hoc and outside every registered family.

## 12. Second amendment record (2026-11-10, before any run)

The plan as amended on 2026-10-17 (sha256
`0d7a866d1364047ba2c6379eaf6b29998f25aa22fec8de296f597e7358f37371`, never OK'd
by the owner and never stamped) was amended again before any eval ran. On
2026-10-19 the owner had ruled that the check would not run before submission
(decision log: *NO INTERACTION CHECK BEFORE SUBMISSION*). On 2026-11-10 the
owner reopened it as a cheap probe before deciding whether to spend on new
training runs, and asked for High severity to be added (decision log:
*GO/NO-GO PROBE*). What changed:

1. **The High 2×2** (§2–§4): four conditions on the all-on High configuration,
   three of them new files. The run grows from 865 evals to 1557.
2. **I at High** (§5–§7): its own family of 8, with the same interval, floor,
   hurdle, reading rule and disagreement rule as I at θ\*.
3. **The main effects are graded** (§4, §5, §7): A and B at both sites, one
   family of 32, the same reading rule. Under the earlier text they were
   descriptive, at θ\* only.
4. **The go/no-go reading** (§7), with its size bar read from the registered
   contrast.
5. **A second cross-card check** (§6): "high both" against the post-unblind
   High readout.
6. **Blind spots** (§8): items 1, 2, 5 and 8 follow the new conditions, and
   item 9 is new.

**Unchanged:** the policies, the eval draw, the estimands I and D at θ\*, their
two families of 8 and every interval in them, their floors and hurdles, their
reading rules, the θ\* cross-card check, the logit block's form, verification
without version history (§9), the timestamps (§10), and the labels: post hoc
and outside every registered family.

**The builder's choices in this amendment, for the owner to confirm or
change before the run:** the main effects as one family of 32 (not one per
site); the three conditions of "bites", among them the size bar and its
source; GO as "both couplings", with PARTIAL left to the owner; no links-open
condition at High.
