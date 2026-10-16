# Interaction check at θ\*: analysis plan (POST HOC)

Written 2026-10-14, **before any run**. Authorized by the decision log's
*PAPER V3* item 2(a): eval-only, labelled post hoc. Scope set by *PAPER V3
PHASE 1 START* item 2: **θ\* only.** No training of any kind.

`che/scripts/interaction_analysis.py` implements this plan. It refuses to run
unless this file is committed in git and unchanged since that commit. It also
refuses unless the eval run recorded this file's sha256 in its provenance, and
that hash matches the committed file. Any edit to this plan after the run
therefore shows up as a refusal, not as a silent change.

## 1. Status: what this analysis is and is not

- **Post hoc.** The check was proposed after the Phase-6 result was known
  (a professor's review, *PAPER V3* item 1(1)). It carries no confirmatory
  weight. Every place it appears, abstract included, labels it post hoc.
- **Out of the registered family.** It does not join the confirmatory family
  {Γ_completion, Γ_survival} (Šidák m = 2, `m62_report.py::SIDAK_M`). It
  changes no reading of Γ, Γ₄, B̂, Γ(t) or Γ_H, and no branch. Branch B stands
  (*PAPER V3*, "What changes, and what does not").
- **Its question.** At θ\*, do trained policies' outcomes show a
  *non-additive* interaction between Coupling A (collapse seeds fire) and
  Coupling B (smoke attenuates perception)? Put plainly: does the
  composition the registered test was about exist, measurably, at the point
  where it was tested?

## 2. Conditions

Four environment configurations. Each is θ\* (`che/configs/theta_star_holdout.yaml`)
with only κ_A and κ_B changed. β = 0.49, δ = 1.0 and every other locked value
stay at θ\*'s value in all four.

| condition | config | κ_A | κ_B |
|---|---|---|---|
| neither | `che/configs/interaction_neither.yaml` | 0 | 0 |
| A only | `che/configs/interaction_a_only.yaml` | θ\*'s (0.06) | 0 |
| B only | `che/configs/interaction_b_only.yaml` | 0 | θ\*'s (1.0) |
| both | `che/configs/theta_star_holdout.yaml` (θ\* itself) | θ\*'s | θ\*'s |

The three new configs are generated from θ\*'s file by
`che/scripts/make_interaction_configs.py`. `che/tests/test_interaction_check.py`
asserts that each loads to θ\* with exactly its κ values replaced, and that
"both" is θ\*'s own file.

With κ_A = 0 or κ_B = 0, the environment is the corresponding nested model,
bitwise, given the same PRNG keys (CLAUDE.md invariant 3;
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
- **Common random numbers.** All four conditions use the same eval seed. So
  each policy meets the same 512 initial states and the same random streams
  in every condition. By invariant 3, the conditions differ only through the
  couplings themselves.
- **Main evals:** 164 policies × 4 conditions = **656**.
- **Floor evals:** see §6. Checkpoints `iso_s1`, `joint_s1` and `iso4_s1`,
  each condition repeated 3 more times: 3 × 4 × 3 = **36**.
- **Total: 692 evals.** Cost estimate, from *PAPER V3* item 5's measured
  per-eval times (9.40 s; mean 14.8 s): 692 × 9.40 s ≈ 1.8 h to
  692 × 14.8 s ≈ 2.8 h, plus archive extraction. **An estimate, not a
  trigger.** Realized time is read from the run's `timings.txt`.

## 4. Outcomes and estimand

- **Co-primaries:** completion and survival rate, the registered pair
  (`p6_unblind.FAMILY`). For policy i in condition c, J_i(c) is the metric's
  mean over the 512 episodes, as the harness's summary JSON records it.
- **Estimand, per policy and co-primary:**

  I_i = J_i(both) − J_i(A only) − J_i(B only) + J_i(neither).

  I = 0 means the two couplings' effects add. I < 0 means the outcome under
  both is worse than the sum of the separate effects predicts (the couplings
  compound). I > 0 means it is better than additive (they overlap or offset).
- **Descriptive, outside the family, no reading rule:**
  - the four condition means per arm, for all four `m62_report.METRICS`;
  - the main effects A = J(A only) − J(neither) and B = J(B only) − J(neither)
    per arm and co-primary, each with the same interval form. They say
    whether each coupling, on its own, moves trained policies at θ\*. They
    are context for I, not tests.

## 5. Test and family correction

- **Per arm** a ∈ {ISO, JOINT, ISO-4}: Ī_a = the mean of I_i over the arm's
  k_a seeds, with s_a = their sd (ddof 1) and SE_a = s_a / √k_a. Because I_i
  is a within-policy contrast, its spread across seeds carries both seed
  variation and episode-sampling variation. This is the artifact's own seed
  dispersion (CLAUDE.md, amendment of 2026-08-03).
- **Pooled:** all 164 policies, stratified by arm. Ī_pool = Σ_a w_a Ī_a with
  w_a = k_a / 164. SE_pool = √(Σ_a w_a² s_a² / k_a). It answers "averaged over
  the study's policies, weighted by seed count". It does not assume the arms
  share one I.
- **Family:** 4 estimates (ISO, JOINT, ISO-4, pooled) × 2 co-primaries = 8
  intervals. Šidák: α' = 1 − 0.95^(1/8), with two-sided z_α' (≈ 2.73).
  Interval: Ī ± z_α' · SE. These are normal intervals, as the project's other
  contrasts use (Γ₄ at k = 20 included, *PRE-UNBLIND RULINGS* (v)). ISO-4's
  k = 20 is the smallest, and the report says so beside its row.
- **80 %-power MDE** for each estimate, from its observed SE:
  (z_α' + z_0.80) · SE (CLAUDE.md, "Power statements are 80 %-power MDEs").
  It is labelled "observed-SE MDE80". It is a detection limit, not a bound.
- **No cross-arm test.** Differences in I between arms are reported
  descriptively only. No reading rule is attached to them.

## 6. Floors (per artifact, on the run GPU)

- **Eval self-floor (A-vs-A).** For each of `iso_s1`, `joint_s1` and
  `iso4_s1`, every condition is evaluated three more times on the same card.
  Together with the main eval, that gives four copies per (checkpoint,
  condition). The analysis reports:
  - whether the copies are bitwise identical, per condition;
  - their per-metric sd;
  - the sd of I across the four copies (I recomputed from copy r of each
    condition), per checkpoint.

  Every condition is its own artifact, so each is floored separately
  (CLAUDE.md, per-artifact floors). The earlier finding that θ\* evals are
  deterministic on an RTX 5090 (`post_evalfloor_gamma_t_high.md`) covers
  θ\* only. It is not assumed for the κ = 0 conditions.
- **Reproducibility hurdle.** If every copy is bitwise identical, the floor
  is zero and the hurdle is met. Otherwise, a rejection also needs
  |Ī| > 2 × (the largest floor sd of I). This is the post-hoc 2-sigma
  floor-grading convention, labelled as such.
- **Cross-card check (descriptive).** The "both" eval of every policy is
  compared with the grid's own θ\* eval of the same checkpoint
  (`g1_conf_5090/eval_*.json`, `g1_iso4_5090/eval_iso4_s*.json`). The report
  states how many of the 164 are identical on both co-primaries. If they all
  are, the run reproduces the registered evals. If not, the differences are
  reported, and the self-floor above decides how to read them.

## 7. Reading rules (fixed now)

For each of the 8 estimates:

- **Detectable interaction:** the Šidák interval excludes 0 and the hurdle
  of §6 is met. Report its sign and its size in the metric's own units. For
  survival, also report it in agents per episode (× 12 agents).
- **No detectable interaction:** otherwise. This is stated as an
  **exclusion with its bound**: "|I| < B at the family-corrected level", with
  B = max(|lower|, |upper|) of the Šidák interval, and the observed-SE
  MDE80 beside it. It is never stated as "no interaction" or "additive".
- **The paper's headline reading is the pooled pair** (survival and
  completion). The per-arm rows say whether the answer depends on how the
  policy was trained. They are read with the same rule, in the same family.
- **A void reading.** If the floor block or the cross-card check cannot be
  computed (missing files, failed evals), the analysis refuses. It does not
  report a partial family.

## 8. What this analysis is blind to

Stated here, and repeated wherever the result is reported:

1. **θ\* only.** It says nothing about Low (β = 0.43) or High (β = 0.70),
   where the couplings' strengths differ (`theta_star_holdout.yaml` header,
   "WHY THE MIDDLE").
2. **Fixed policies.** It measures how the couplings combine for these
   trained policies at evaluation. It does not measure whether training on
   co-occurring couplings teaches anything. That is Γ, the registered test.
3. **The additive scale.** I is computed on episode means of bounded rates.
   An interaction on another scale (odds, log) is not tested. Ceiling and
   floor effects of a bounded rate can create or hide an additive
   interaction.
4. **One eval draw.** Every interval is conditional on the single common
   draw (seed 0, 512 episodes), as every other Phase-6 interval is.
5. **Comms denial held fixed.** δ = 1.0 in all four conditions.
   Interactions involving comms denial are not measured.
6. **Not a cross-arm test.** I is a within-policy contrast. Whether I
   differs between ISO, JOINT and ISO-4 is reported but not tested.
7. **Post hoc.** The check was chosen with the Phase-6 result known. Its
   result cannot strengthen or weaken the registered conclusions. It can
   only describe the test point.
8. **The arms saw the four conditions differently in training.** Each
   arm's I mixes how the environment combines the couplings with how
   familiar that arm's policies are with each condition. All training was
   at β ∈ {0.43, 0.70}, never at θ\*'s 0.49:
   - ISO trained on A-only and B-only components at δ = 0, and on
     comms-only components at δ = 1, which are the "neither" condition's
     couplings (`che/configs/p6_iso.yaml`);
   - ISO-4 trained on A-only and B-only components at δ = 0 only. It never
     saw δ = 1, which all four conditions use here, as θ\* does
     (`che/configs/p6_iso4.yaml`);
   - JOINT trained only with every element on (κ_A and κ_B at θ\*'s values,
     δ = 1), which is the "both" condition's couplings
     (`che/configs/p6_joint.yaml`).

   This is why the per-arm rows are reported beside the pooled one. The
   pooled reading averages over these differences; it does not remove them.

## 9. Outputs

All under `che/bench/results/phase6/post_v3_interaction/`:

- `evals/eval_<tag>_<cond>.{npz,json}`: the 656 main evals;
- `floor/floor_<tag>_<cond>_rep<r>.{npz,json}`: the 36 floor evals;
- `timings.txt`, `provenance.txt` (it includes this file's sha256);
- `v3_interaction_results.tar.zst` with `SHA256_RESULTS.txt`. The run script
  asserts both before it exits 0 (CLAUDE.md, artifact persistence);
- written later by the analysis: `interaction_report.md`,
  `interaction_report.json` and `ANALYSIS_LOG.txt`.
