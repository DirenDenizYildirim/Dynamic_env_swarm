# Interaction check at θ\*: analysis plan (POST HOC)

Written 2026-10-14, **before any run**, and **amended 2026-10-17, still before
any run**, on a blind review's design concerns (decision log: *PLAN
AMENDMENT*; §11 lists every change). Authorized by the decision log's *PAPER V3*
item 2(a): eval-only, labelled post hoc. Scope set by *PAPER V3 PHASE 1 START*
item 2: **θ\* only.** No training of any kind.

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

## 2. Conditions

Five environment configurations. The first four are θ\*
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

The four new configs are generated from θ\*'s file by
`che/scripts/make_interaction_configs.py`. `che/tests/test_interaction_check.py`
asserts that each loads to θ\* with exactly its κ or δ values replaced, and that
"both" is θ\*'s own file.

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
- **Common random numbers.** All five conditions use the same eval seed. So
  each policy meets the same 512 initial states and the same random streams
  in every condition. By invariant 3, the conditions differ only through the
  couplings and the links themselves.
- **Main evals:** 164 policies × 5 conditions = **820**.
- **Floor evals:** see §6. Checkpoints `iso_s1`, `joint_s1` and `iso4_s1`,
  each condition repeated 3 more times: 3 × 5 × 3 = **45**.
- **Total: 865 evals.** Cost estimate, from *PAPER V3* item 5's measured
  per-eval times (9.40 s; mean 14.8 s): 865 × 9.40 s ≈ 2.3 h to
  865 × 14.8 s ≈ 3.6 h, plus archive extraction. **An estimate, not a
  trigger.** Realized time is read from the run's `timings.txt`.

## 4. Outcomes and estimands

- **Co-primaries:** completion and survival rate, the registered pair
  (`p6_unblind.FAMILY`). For policy i in condition c, J_i(c) is the metric's
  mean over the 512 episodes, as the harness's summary JSON records it.
- **The interaction, per policy and co-primary:**

  I_i = J_i(both) − J_i(A only) − J_i(B only) + J_i(neither).

  I = 0 means the two couplings' effects add. I < 0 means the outcome under
  both is worse than the sum of the separate effects predicts (the couplings
  compound). I > 0 means it is better than additive (they overlap or offset).
- **The links-open effect, per policy and co-primary:**

  D_i = J_i(links open) − J_i(both).

  D is the effect of opening the links (δ = 0 against δ = 1) with both
  couplings on. D > 0 means policies do better with the links open; D < 0
  means they do worse.
- **Descriptive, outside both families, no reading rule:**
  - the five condition means per arm, for all four `m62_report.METRICS`;
  - the main effects A = J(A only) − J(neither) and B = J(B only) − J(neither)
    per arm and co-primary, each with the same interval form. They say
    whether each coupling, on its own, moves trained policies at θ\*. They
    are context for I and D (§7), not tests;
  - I on the logit scale (§5).

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
- **Families: two separate families of 8 intervals.**
  - The interaction family: 4 estimates (ISO, JOINT, ISO-4, pooled) × 2
    co-primaries of I = 8 intervals.
  - The links-open family: the same 4 estimates × 2 co-primaries of D = 8
    intervals.

  In each, Šidák: α' = 1 − 0.95^(1/8), with two-sided z_α' (≈ 2.73).
  Interval: estimate ± z_α' · SE. These are normal intervals, as the project's
  other contrasts use (Γ₄ at k = 20 included, *PRE-UNBLIND RULINGS* (v)).
  ISO-4's k = 20 is the smallest, and the report says so beside its row.
- **80 %-power MDE** for each estimate, from its observed SE:
  (z_α' + z_0.80) · SE (CLAUDE.md, "Power statements are 80 %-power MDEs").
  It is labelled "observed-SE MDE80". It is a detection limit, not a bound.
- **I on the logit scale (descriptive).** Per policy, I is recomputed on the
  logit of each of the four condition means, logit(p) = ln(p / (1 − p)). Per
  arm and pooled, it gets the same interval form. It is outside both
  families, and it has no reading rule. A policy with any of the four means
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
  - the sd of D across the four copies, per checkpoint, likewise.

  Every condition is its own artifact, so each is floored separately
  (CLAUDE.md, per-artifact floors). The earlier finding that θ\* evals are
  deterministic on an RTX 5090 (`post_evalfloor_gamma_t_high.md`) covers
  θ\* only. It is not assumed for the other conditions. The copies' episode
  means are summed in float64.
- **Reproducibility hurdle.** If every copy is bitwise identical, the floor
  is zero and the hurdle is met. Otherwise, a rejection of I also needs
  |Ī| > 2 × (the largest floor sd of I), and a rejection of D needs
  |D̄| > 2 × (the largest floor sd of D). This is the post-hoc 2-sigma
  floor-grading convention, labelled as such.
- **Cross-card check (descriptive).** The "both" eval of every policy is
  compared with the grid's own θ\* eval of the same checkpoint
  (`g1_conf_5090/eval_*.json`, `g1_iso4_5090/eval_iso4_s*.json`). The report
  states how many of the 164 are identical on both co-primaries. If they all
  are, the run reproduces the registered evals. If not, the differences are
  reported, and the self-floor above decides how to read them.

## 7. Reading rules (fixed now)

For each of the 8 estimates of I, and separately for each of the 8 of D:

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
- **A void reading.** If the floor block, the cross-card check or Γ's file
  cannot be read (missing files, failed evals), the analysis refuses. It does
  not report a partial family.

## 8. What this analysis is blind to

Stated here, and repeated wherever the result is reported:

1. **θ\* only.** It says nothing about Low (β = 0.43) or High (β = 0.70),
   where the couplings' strengths differ (`theta_star_holdout.yaml` header,
   "WHY THE MIDDLE").
2. **Fixed policies.** It measures how the couplings combine for these
   trained policies at evaluation. It does not measure whether training on
   co-occurring couplings teaches anything. That is Γ, the registered test.
3. **The additive scale.** I is computed on episode means of bounded rates.
   Ceiling and floor effects of a bounded rate can create or hide an
   additive interaction. The logit block shows I on one other scale,
   descriptively; it is not tested there or on any other scale.
4. **One eval draw.** Every interval is conditional on the single common
   draw (seed 0, 512 episodes), as every other Phase-6 interval is.
5. **Comms denial in the 2×2 is held fixed.** δ = 1.0 in all four
   interaction conditions, so interactions involving comms denial are not
   measured. D measures opening the links only with both couplings on: it
   does not say what opening the links does under one coupling or none.
6. **Not a cross-arm test.** I and D are within-policy contrasts. Whether
   they differ between ISO, JOINT and ISO-4 is reported but not tested.
7. **Post hoc.** The check was chosen with the Phase-6 result known, and
   amended after a blind review but before any run (§11). Its result cannot
   strengthen or weaken the registered conclusions. It can only describe the
   test point.
8. **The arms saw the five conditions differently in training.** Each arm's
   I and D mix how the environment behaves with how familiar that arm's
   policies are with each condition. All training was at β ∈ {0.43, 0.70},
   never at θ\*'s 0.49:
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

   This is why the per-arm rows are reported beside the pooled one, and why
   the headline follows the pool only when the arms agree (§7). The pooled
   reading averages over these differences; it does not remove them.

## 9. Outputs, and verification without version history

All under `che/bench/results/phase6/post_v3_interaction/`:

- `evals/eval_<tag>_<cond>.{npz,json}`: the 820 main evals;
- `floor/floor_<tag>_<cond>_rep<r>.{npz,json}`: the 45 floor evals;
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
