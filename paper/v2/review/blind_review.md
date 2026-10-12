# Review: "A pre-registered test of training on co-occurring versus isolated stressors in a multi-agent fire environment" (TMLR, Beyond PDF track)

Reviewer's note on sources. I read `paper.pdf` (all 46 pages), `submission_folder/submission.md`, `submission.bib`, and the HTML source of all eleven interactive figures in `assets/html/submission/`. I made **no web lookups**. Where I comment on cited works (Kesten 1980, Bernstein et al. 2002, Pynadath & Tambe 2002, and others), I rely on my own background knowledge and say so. PDF page numbers refer to the printed `paper.pdf` ("N of 46").

---

## 1. Summary of contributions

The paper introduces the Compound Hostile Environment (CHE). It is a pure-JAX, grid-world, multi-agent foraging environment (64×64 grid, 12 agents, horizon 256) in which a cellular-automaton fire burns in every episode. Three "stressors" are parameters of the transition or observation kernels:

- **Coupling A** (κ_A): structural collapse of "weak" cells seeds ignitions.
- **Coupling B** (κ_B): smoke attenuates each agent's egocentric observation by Beer–Lambert transmittance.
- **Communication denial** (δ): links are dropped. This stressor is independent of the fire.

The reward reads only food collection and a fixed per-death penalty (d_p = 0.5). The authors call this an "ambient hazard" (Def. 2).

The paper claims three contributions.

1. **The environment as an instrument.**
   - Severity levels are placed relative to a measured percolation threshold of the fire kernel. The idealized kernel is proved equivalent to bond percolation (Prop. 2, Cor. 1).
   - Nested ablations are bitwise exact, because every stochastic branch consumes its random numbers unconditionally.
   - Small theoretical results (Props. 1–4, Thm. 1, Remark 2′) double as unit tests.
2. **Calibration findings.**
   - Collapse-seeded ignitions fall about 4.8-fold from Low to High severity (fuel exhaustion).
   - Smoke costs survival at High severity in 3 of 3 replicates.
   - Communication denial is "inert" under a frozen random-projection message encoder.
   - A measurement protocol of reproducibility "floors": per-metric, per-GPU, per-artifact standard deviations over identical reruns, used to gate acceptance thresholds.
3. **A pre-registered confirmatory test** of joint (JOINT: all stressors co-occur) against isolated (ISO: a mixture of single-stressor configurations) training, at matched compute, evaluated at a held-out near-critical severity θ\*. There are two Šidák-corrected co-primaries, completion and survival, with 72 seeds per arm.
   - Γ (JOINT − ISO) is +0.96 survival points (rejects) and −1.73 completion points (null).
   - Both co-primaries are "sign unstable" over the last half of training.
   - Because δ was found inert, a third of ISO's training episodes are effectively fire-only. The authors call this a design error. It was registered with a correction (ISO-4: ISO without δ-only episodes, 20 seeds, on another GPU) before unblinding.
   - The corrected gap Γ₄ is −0.03 survival points [−0.68, +0.63], so the survival effect "does not survive the inert-share correction."
   - The paper ends with one recommendation: compositional-generalization studies should match the share of training episodes that contain an active stressor before attributing a gain to composition.

---

## 2. Strengths

1. **Unusual transparency and pre-registration discipline for RL.**
   - The design, outcome branches, falsifiers, reading rules and deviations are quoted verbatim with dates (App. D, E).
   - Post hoc analyses are labelled as such, for example the same-GPU replicate Γ₄′.
   - The authors report a correction that dissolves their own headline effect, and the design error is stated plainly in the abstract.
   - This is rare and commendable. The paper is a useful case study of what pre-registration looks like in deep RL.
2. **Careful environment engineering.**
   - Bitwise nested ablations come from unconditional PRNG consumption and are checked by both behavioural and structural tests (§3.4).
   - The kernel factorization order is documented against verbatim code (Listing 1).
   - Reward independence is tested (§3.3).
   - These are good practices that many JAX environment papers would benefit from copying.
3. **Principled severity calibration.**
   - The bond-percolation coupling (Prop. 2) is correct and well explained.
   - Severity levels are locked to observable bands: P_span, burnt fraction, front speed (§4.3).
   - The paper honestly reports that a pre-stated prediction (outcome variance peaks at Medium) was refuted for survival (§4.4).
4. **Statistical hygiene in the confirmatory analysis.**
   - Šidák-corrected co-primaries; the contrast's own standard error; MDEs at 80% power.
   - Measured hardware nondeterminism floors; explicit UNDERPOWERED flags.
   - A full Γ(t) trajectory in App. G.
   - The numbers are internally consistent where I checked them. For example, CI = Γ ± 2.2365·sd(Γ), and X = 3.078·sd(Γ) = 3.29 points for completion.
5. **Honest figure annotations.** Each figure carries a status label (registered / secondary / illustrative) and a "cannot show" statement. The interactive figures are self-contained (no external scripts), keyboard accessible, offer table views and dark mode, and come with static companions for print.
6. **A useful cautionary observation.** Joint-versus-isolated comparisons confound co-occurrence with per-stressor frequency and with the share of training that has any active stressor. This is a real pitfall for compositional-generalization studies, and the paper documents a concrete instance of it.
7. **Modest compute.** Timings are reported (about 520 s per 1000-update run on an RTX 5090).

---

## 3. Weaknesses

Ordered from most to least serious.

### W1. The central reinterpretation rests on an "inert" label established at far coarser resolution than the effect it explains, and applied asymmetrically

Everything after the confirmatory result depends on treating ISO's δ-only episodes as "fire-only in effect": the inert-share correction, Γ₄, B̂, the plane's γ_n prediction, and the §9.3 recommendation. The evidence that δ is inert (§7.3) is weak at the relevant scale.

- **The denial study is too coarse.** It uses four seeds at Medium. It reports survival **1.43 points lower** with links open, against a bar of **2.60 points**, and completion within a bar of **7.99 points**.
- **The content ablation is also coarse.** It uses two seeds and a bar of about 3 points.
- **Bars versus effects.** The quantities these bars are meant to rule out are larger than the effects being explained: Γ = 0.96 survival points and B̂ = 0.98. The point estimate of δ's own survival effect (1.43) exceeds Γ.
- **The paper concedes these are half-power, post hoc floor gradings** ("none of these results is a point null"). Yet the abstract, the title of §7, the contributions and Limitation 5 all assert "inert".
- **The rule is applied asymmetrically.** By the paper's own calibration:
  - Coupling A is "marginal by construction" at High (§5.3, §10 item 1).
  - Coupling B is "behaviourally quiet" at Medium and masks 0.07% of crop cells at Low (§6.4).
  - Even so, ISO's A-only-at-High and B-only-at-Low components (and ISO-4's) are counted as fully "active", while δ-only episodes are counted as inert.
  - "Behaviourally active" is never defined operationally. Under any uniform threshold, the stated active shares (2/3 for ISO, 1 for ISO-4 and JOINT) would change.
- **There is also a train/test mismatch that the paper does not discuss.** ISO's A-only and B-only components use δ = 0 (`composer_training_mixtures.html` data), so ISO-4 trains entirely with communication open. JOINT trains entirely with δ = 1, which matches θ\*. At test time ISO-4 sees an all-zero message aggregate it essentially never saw in training. If δ is truly inert this does not matter, but that is the assumption under question.

### W2. In this design family, composition cannot be separated from frequency and active share, and the recommendation does not say so

With two stressors, the episode shares (A-only, B-only, A+B, fire-only) obey the inclusion–exclusion identity

  active share = μ_A + μ_B − p,

where μ is per-coupling frequency and p is co-occurrence.

- **Consequence.** Co-occurrence cannot be varied while both per-coupling frequency and active share are held fixed. Fixing μ and the active share determines p.
- **Every contrast in the paper therefore trades one confound for another:**
  - Γ: frequency and active share both differ.
  - Γ₄: active share is matched; frequency differs 2×.
  - The sweep: frequency is matched; the fire-only share ν equals p.
  - The plane: only two degrees of freedom for three quantities.
- **The paper half-acknowledges this** ("cannot all be held fixed on the triangle", App. H), but never states the identity or draws its consequence.
- **Consequence for the §9.3 recommendation.** "Match the active share before attributing a gain to composition" necessarily **un-matches** per-stressor frequency in exactly the comparison the paper is about. The recommendation therefore cannot by itself license a composition attribution.
- **What is needed.** The paper should state this explicitly and say what could identify composition. Options include varying stressor intensity or training compute, adding a third factor, or a model-based decomposition.

### W3. The confirmatory test had little capacity to detect composition, and the effects are practically negligible

- **One of the two composed stressors is near-null at θ\*.** Coupling B's own survival effect is −0.03 points at Medium (§6.4). By the authors' own account, "no severity has both couplings strongly live" (§10 item 1). The A × B composition tested at θ\* is therefore a composition of one live stressor and one near-null stressor. A null or fragile composition result is close to expected by design.
- **The effects are tiny.**
  - The uncorrected survival gain is about 0.11 agents out of 12 per episode.
  - Survival Γ(t)'s Šidák interval excludes zero only at updates 900–1000, the last tenth of a non-converged training budget (App. G).
  - Completion leans negative.
- **The budget is short and non-converged.** The 1000-update budget is never justified relative to learning progress: no absolute learning curves for ISO or JOINT are shown. The 2000-update subsample (4 seeds) cannot settle anything.
- **Limited relevance.** These are matched-compute readings of a still-moving comparison. That limits their relevance to practitioners, who mostly care about trained-to-convergence policies.

### W4. Statistical terminology and some claims do not match the evidence

- **"Exclusion bound X" is the 80%-power MDE, not an interval bound.**
  - The text alternates between excluding by the CI ("excludes a joint-training gain larger than 0.66 points") and excluding by the MDE.
  - The High-readout sentence states "no gap larger than 3.40 completion points or 2.54 survival points". Those numbers are MDEs, not CI bounds.
  - For Γ on completion, the CI [−4.12, +0.66] does **not** exclude a negative gap of 3.29 points, yet X = 3.29 is described as "the gap of either sign the design would detect".
  - A post hoc MDE does not exclude anything. Exclusion statements should come from CI (equivalence-style) bounds.
- **Realized power at the motivating effect falls below the registered threshold, but this is not flagged.**
  - The registered `POWER_STOP = 0.80` (App. B) is defined on design-stage power. That figure was 80.4% at k = 72 on GPU 1's floors (App. D), so the rule was formally met.
  - §8.4 calls floor-based design-stage power an upper bound. The realized completion power at the registered 0.03 effect is **71.6% at k = 72** (§9.1), below that threshold.
  - Only the k = 60 analysis is flagged UNDERPOWERED. In the spirit of the paper's own rules, the k = 72 completion null should state that it is underpowered against its motivating effect.
- **Γ₄'s survival MDE is never stated in the text.**
  - From the figure's embedded data (`opening_ladder.html`) it is about 0.90 points, and about 0.94 points for Γ₄′.
  - So the correction has roughly 85% power against an effect the size of Γ, but only about 25–30% power against half of it.
  - The text says "excludes only a large composition effect", which is fair, but the actual detectable size should be stated.
- **"Smoke costs survival at High severity, in the same direction in three of three replicates" is presented as a calibration finding** (Contribution 2). This does not meet the paper's own evidential standard:
  - The three contrasts are single runs per cell, with no intervals.
  - Two share a seed (a same-seed retrain), so they are not independent.
  - The first estimate is only 1.41× a cross-artifact single-run floor; a two-run contrast has noise √2 times larger.
  - Even if independent, 3/3 signs give a one-sided sign-test p of 0.125.
  - "Consistent effect of modest size" overstates this. It should be labelled descriptive or ungraded.
- **"Conservative" is misused.** Raising k from 60 to 72 is called "conservative, since added seeds favour neither sign of Γ" (§9.1). More seeds increase power; this is neutral with respect to sign, not conservative.
- **The covariance argument is unsupported.** "Positive cross-arm covariance, the expected sign given the shared seed integers, makes the unpaired test conservative" (§9.1). Why shared seed integers would induce positive covariance between differently configured training runs is never argued.
- **The sign-stability rule is close to vacuous for small effects.** The Γ(t) rule (all 11 point estimates must share a nonzero sign) nearly always reads "unstable" for small or null effects. The authors accept this in advance (App. D, item 9(iv)). It should be described as low-informative rather than as "the finding".

### W5. Verifiability: no code, internal-only registration, self-attested blinding

- **No code or artifacts are available to reviewers.**
  - The environment is Contribution 1, and the paper cites file:line references and tests throughout (`che/env/env.py:298-358`, `che/tests/test_nesting.py:222-240`, …).
  - Yet there is no anonymized code link, supplementary archive, or per-seed results table.
  - None of the bitwise-nesting, reward-independence or registry-consistency claims can be checked.
- **The pre-registration is not independently timestamped.**
  - The registration documents are internal ("lock record", "ruling", "review §6 item 1", "§5, superseded note").
  - Blinding rests on "our attestation, recorded with the ruling" (§9.1).
- **Blinding needs clarification.** Unblinding is described as "the first computation of any outcome contrast" (§1, §9.1), but before unblinding:
  - The differential JOINT − ISO completion drift ("bias (b)") was computed from four floor studies (§9.1). That is a cross-arm, outcome-derived quantity.
  - Floor studies necessarily produce per-arm outcome values at seed 0. The floors figure embeds individual rerun completion values for ISO and JOINT from the RTX PRO 6000 studies. App. F says "the floor reports print dispersions only".
  - The GPU 1 floor study drove the decision to raise k to 72. Were its arm-level values visible?
  - The authors should state exactly which outcome-derived numbers were visible when the k = 72 and ISO-4 decisions were made, and reconcile this with the claim above.

### W6. Theory: mostly elementary, partly imprecise, and partly inconsistent with the reported tests

- **Most results are elementary.**
  - Prop. 1 (well-posedness) is routine.
  - Prop. 2 is the standard epidemic–percolation coupling.
  - Cor. 1 restates known percolation results.
  - Prop. 3 is linearity of expectation.
  - Thm. 1 is a two-line toy calculation.
  - Presenting these as theorems that "double as unit tests" is fine. Describing them as a theoretical contribution overstates them.
- **Prop. 4 is not a proposition.**
  - "Bounded above by a term that grows with how far their transition and observation kernels differ" has no stated metric, constant or form, and only a "proof idea" is given.
  - App. A states that the authors' "formal specification" contains a version that "concludes more about ISO's slack than an upper bound can show". That is an admission that an internal document contains an incorrect conclusion.
  - Prop. 4 should be stated precisely (it is a standard simulation-lemma-type bound) or demoted to a remark.
- **Prop. 3 is imprecise.**
  - "(1 + o(1))" has no stated limit.
  - Differentiating an asymptotic equality to get ∂E[B_T]/∂λ_A = Tχ(β) is not justified.
  - The title "Collapse events dominate hazard exposure" is not what is proved: with no primary ignition, collapse is trivially the only source.
- **Thm. 1 appears inconsistent with its reported test.**
  - The theorem's signal model is "Beer–Lambert over the current distance to the fire, unit smoke density", with ℓ_f ≥ 1. With these definitions, q(κ_B = 8) ≤ e^{−8}/(1 − e^{−8}) ≈ 3.4 × 10⁻⁴.
  - The paper reports "q = 0.0056" at κ_B = 8, about 17 times larger, and "J\* − ½ = 0.0000", whereas the theorem predicts ½q = 0.0028.
  - §6.3 refers to "the toy's single smoke source". This suggests the implemented toy uses the four-point midpoint transmittance on a single smoke cell, not unit density along the path.
  - The theorem that is stated and the toy that is tested appear to differ. The paper should reconcile them.
- **Remark 2′ has unresolved issues.**
  - Part (i) (value "scales with the deficit of agents relative to hypotheses"; a death cost "prices the redundancy") is unproven and imprecise.
  - Part (ii) reuses ℓ_f as "slack" with "equality iff ℓ_f = 0", which contradicts ℓ_f ≥ 1 in Thm. 1.
  - Calling Remark 2′ a "refinement" of Pynadath & Tambe (2002) is a category mismatch. From my own knowledge, their results classify computational complexity by observability and communication cost. Remark 2′ is a value-of-information statement in a toy.
- **The paper is not self-contained.** The appendix repeatedly refers to "the formal specification", which is not provided.

### W7. The "ambient hazard / hazard-blind reward" framing is thinner than presented

- **The death penalty is effectively a hazard-contact penalty.** In CHE an agent dies if and only if it stands on a cell that is Burning in h′ or that collapses this step (§3.3). The death penalty is therefore, functionally, a one-time penalty for hazard contact.
- **The distinction drawn in Table 1 is semantic.** CHE's reward is "hazard-blind" while JaxWildfire's is "hazard-priced". But JaxWildfire's penalty depends on the global count of burning cells, while CHE's depends on contact. Neither is "ambient" in any learning-relevant sense once d_p > 0.
- **The paper's own ablation shows the penalty drives survival learning.** Raising d_p from 0 to 0.5 moves High survival from 0.575 to 0.866 (§3.3).
- **The paper's reading of the asymmetric outcome becomes moot.** It explains the asymmetry as "penalized channel versus rewarded channel". That is an untested post hoc account, and after the correction there is no asymmetry left to explain.
- **Suggestion.** I suggest de-emphasizing Def. 2 as a contribution.

### W8. Limited scope as an environment and as a multi-agent study

- One instance (64×64, 12 agents), one learner (shared-parameter IPPO), and one hyperparameter set.
- No algorithmic baselines and no heuristic reference policies; only a random policy is shown.
- One held-out test point, interpolated in β between the training severities.
- The task "requires no coordination" (Limitation 3), communication is inert, and all agents share parameters. The multi-agent aspect is therefore nominal.
- For an environment contribution, at least a few learners and an absolute performance table would be expected.

### W9. Presentation makes the paper very hard to read

- **The paper is organized around the project's internal history** rather than the scientific argument. Dated rulings and "locks" dominate (2026-07-19, 2026-08-02, 2026-08-13, …). Internal study codes are used throughout (M3.5, M4.4, m44, M5.1e, M5.3b, M5.5, M6.0, M6.2b, G1.2). The text refers to records the reader cannot see ("lock record", "re-test report", "the ruling", "review §6 item 1", "Q3 ruling").
- **Idiosyncratic vocabulary is used without definition at first use:** "bars", "floors", "grades nothing", "carries no verdict", "rung", "card", "unit", "knee", "cross-artifact", "VOID", "branch A_c", "strongly live", "co-active".
- **Key caveats are repeated many times.** For example, "JOINT still sees each coupling twice as often as ISO-4 and always in combination" appears at least four times, and "a recorded deviation made before unblinding" three times.
- **I list over 100 unclear sentences in §8 of this review.**
- **There is no abstract proper.** The opening three paragraphs (about 400 words) serve as one and are extremely dense.
- **§8 reads as a lab notebook of past mistakes.** It presents textbook statistical points (MDE versus a 2σ bar; the SE of a difference; hardware nondeterminism) as rules born of project defects. It cites none of the substantial literature on RL evaluation and reproducibility. From my own knowledge, relevant works include:
  - Henderson et al., 2018, "Deep Reinforcement Learning that Matters";
  - Colas et al., 2018, "How Many Random Seeds?";
  - Agarwal et al., 2021, "Deep RL at the Edge of the Statistical Precipice";
  - Patterson et al., "Empirical Design in Reinforcement Learning";
  - on tooling and hardware nondeterminism, Pham et al., 2020, and Zhuang et al., 2022.
  
  Without this context, the contribution of the "measurement protocol" cannot be judged.

### W10. Gaps in related work, and LLM-assisted literature search

- **Safe RL is represented only by a 2015 survey.** Hazard-and-cost benchmarks such as Safety Gym and Safety-Gymnasium are absent, though they are the obvious comparison for "where the hazard enters the learning problem".
- **Generalization in MARL** (for example, Melting Pot-style held-out evaluation) is not discussed.
- **The search method limits the novelty claims.** The search was LLM-assisted, and "the remaining citations rest on their abstracts" (§2). Strong negative claims ("we found no reinforcement-learning environment whose observation kernel attenuates by transmittance") are scoped to this search. That is honest, but it limits how far they can be relied upon.

---

## 4. Claims and evidence

Each claim from the opening (abstract-equivalent) and Introduction is listed with a verdict and the evidence I found.

| # | Claim | Verdict | Evidence and comment |
|---|---|---|---|
| 1 | A pre-registered test, with branches and falsifiers registered 2026-08-13 before the grid; 72 seeds/arm as a recorded pre-unblinding deviation (opening; §1) | **Documented but not verifiable** | App. D–F quote the rules with dates. The registration is internal and blinding is self-attested. Pre-unblinding cross-arm drift computations (bias (b)) sit uneasily with "first computation of any outcome contrast" (W5). |
| 2 | Joint training raises survival by 0.96 points, Šidák CI [+0.47, +1.44] (opening; §1) | **Supported, as stated** | §9.2 table; App. G (sd(Γ) = 0.00216; CI and z consistent). Valid only at θ\*, at T\* = 1000, conditional on one evaluation draw. Practically very small (about 0.11 agents/episode). |
| 3 | Completion shows no detectable change (−1.73 points, CI [−4.12, +0.66]), "which excludes a joint-training gain larger than 0.66 points" (opening; §1) | **Supported for the positive side; power caveat missing** | The CI supports excluding a gain above 0.66 points. Realized power at the registered 0.03 effect is 71.6%, below the 0.80 threshold registered for design-stage power, and this is not flagged (W4). Elsewhere "exclusion bound X = 3.29" is an MDE and does not exclude a negative gap of that size. |
| 4 | Both differences are sign unstable over the final half; the survival gap opens only in the last fifth; completion leans negative from 70% (opening; §1) | **Supported** | App. G, Fig. 12. The registered rule is almost bound to read "unstable" for small effects, so this is weakly informative (W4). |
| 5 | The survival gain does not survive the inert-share correction: Γ₄ = −0.03 [−0.68, +0.63] (opening; §1) | **Supported under the registered rule, with caveats** | §9.2. ISO-4 has 20 seeds, on a different GPU, with no identical reruns. The same-GPU Γ₄′ agrees but was proposed after Γ₄ was seen. Survival MDE is about 0.9 points (figure data). The correction changes active share and frequency together (W2). Its premise, that δ-only episodes are fire-only, is under-resolved (W1). |
| 6 | Communication denial is inert under a frozen random-projection encoder at this scale (opening; §1; Contribution 2; §7) | **Overstated** | §7.3: half-power post hoc bars of 2.6 survival / 8 completion points with 4 seeds; δ's survival point estimate is −1.43 points with links open. That is "no effect detected at ±2.6 points", not "inert", and it is coarser than the ~1-point effects it is used to explain (W1). The "demand side, not channel side" inference from the content ablation is plausible but untested. |
| 7 | The design error was found before the main runs and registered with its correction before unblinding (opening; §1; §9.1) | **Documented, not verifiable** | §9.1 and App. D item 5. Same caveat as claim 1. |
| 8 | No reward, cost or constraint reads the fire; the reward reads only task variables and deaths, pricing every death the same (opening; §1; §3.3) | **Supported as a code property; framing overstated** | Listings 1–2 and the cited tests (unverifiable without code). Death ⇔ hazard contact, so "hazard-blind" is largely semantic (W7). |
| 9 | Severity is set relative to a measured percolation threshold (opening; §1; §4) | **Supported, with a reproducibility caveat** | §4.3 bands and table, Fig. 5. The locked β̂_c's own estimator is not reproducible from committed scripts (stated by the authors). Other estimators span [0.480, 0.513]. The levels are locked to observable bands, so this matters little. |
| 10 | Each stressor is a parameter of one kernel, and switching it off reproduces the nested model bit for bit (opening; §1; §3.4) | **Plausibly supported, unverifiable** | Listing 3 and the described tests. The κ_A test compares only fire and smoke, and the δ test compares to a pre-channel digest on CPU. No code is available. |
| 11 | A measurement protocol with floors per metric, per GPU and per artifact (opening; Contribution 2; §8) | **Described; novelty and evidence limited** | §8 and App. C. The per-GPU exhibit is confounded by GPU, code version and configuration (stated). Floors from 4 reruns are ±40% uncertain (stated). No positioning against prior RL-statistics work (W9). |
| 12 | Recommendation: match the active share before attributing a gain to composition (opening; §1; §9.3) | **Weakly supported; incomplete** | It rests on one environment, Γ₄, and a non-verdict secondary plane whose fit "fails" at JOINT. By the inclusion–exclusion identity, matching the active share un-matches frequency, so the recommendation is necessary but not sufficient (W2). |
| 13 | Prop. 1: CHE is a well-defined Dec-POMDP whose reachable states form a finite set (§1, §3.1) | **Supported (routine)** | App. A proof is correct. |
| 14 | For the idealized kernel the burnt region is exactly a bond-percolation cluster (Prop. 2) (§1) | **Supported** | App. A coupling proof is correct, and the implementation mapping is stated. |
| 15 | No RL comparison found trains its isolated arm on a mixture of single stressors and matches it to the joint arm on active share (§1) | **Scoped search claim** | §2 describes an LLM-assisted search with many citations resting on abstracts. Acceptable as scoped. |
| 16 | Contribution 1: "theory that doubles as unit tests" (§1) | **Partly supported** | Thm. 1 and Prop. 3 have test "handshakes", but the Thm. 1 test appears to check a different signal model from the one stated (W6). Prop. 4 has no testable statement. |
| 17 | Contribution 2a: collapse-seeded ignitions fall 4.8-fold from Low to High under trained policies (§1; §5.3) | **Supported but expected** | §5.3: 4.05 → 0.84 and 4.08 → 0.83 across two grids. This is a mechanical fuel-exhaustion effect already seen with random policies (5.7-fold). |
| 18 | Contribution 2b: smoke costs survival at High in 3/3 replicates (§1; §6.4) | **Not supported at the paper's own standard** | Single runs, no intervals, non-independent replicates, about 1.2–1.4× a cross-artifact single-run floor (W4). |
| 19 | Contribution 3: the survival advantage does not survive the correction, registered before unblinding (§1) | **Supported as a report of the registered rule** | Same caveats as claims 5 and 7. |
| 20 | "We claim no convergence guarantee and no survival gap robust to the training budget" (§1) | **Accurate** | Consistent with §9.2 and App. G. |

Overall, the authors are careful not to over-claim on the confirmatory test, and the main numerical claims are accurately reported. The weaker links are claims 6, 12 and 18, the framing of claim 8, and the verifiability of claims 1, 7 and 10.

---

## 5. Audience

Several parts of TMLR's readership could find this useful.

- **Researchers on generalization and robustness in RL** (compositional generalization, domain randomization, curriculum and environment design). The confound between co-occurrence, per-stressor frequency and active share is a real design pitfall, and this paper is a concrete, well-documented instance.
- **People building JAX environments.** The unconditional-PRNG rule for bitwise nested ablations, the structural test for gated key consumption, and the step-order documentation are directly reusable.
- **People interested in evaluation methodology, reproducibility and meta-science in deep RL.** A fully pre-registered deep-RL experiment, with registered branches and falsifiers, a recorded design error, measured hardware nondeterminism floors, and a correction that removes the headline effect, is rare and instructive.
- **Safe RL and MARL researchers**, to a lesser extent. The "ambient hazard" framing and the smoke-attenuated observation model are of some interest, but the multi-agent aspects are nominal (W8) and the safe-RL positioning is thin (W10).

The audience would be larger if the paper were readable without the project's internal vocabulary (W9) and if the code were available (W5).

---

## 6. Requested changes

### Critical (needed for acceptance)

1. **Release anonymized code, configurations and analysis scripts, plus per-seed results** (CSV: arm, seed, GPU, completion, survival, at each retained checkpoint). If possible, also provide the registration records with verifiable timestamps (for example an anonymized registry snapshot or hashed commits). The environment is the first contribution, and the paper's reproducibility claims are currently unverifiable.
2. **Re-scope and re-examine the δ "inert" claim (W1).**
   - Report the denial and content-ablation results as intervals with their resolution.
   - Replace "inert" by "no effect detected at ±X points" throughout: abstract, §7 title, contributions, Limitation 5.
   - Define "behaviourally active" operationally and apply the definition uniformly to A at High, B at Low/Medium, and δ. Report the resulting active shares.
   - Ideally, add a direct check that δ-only episodes behave like fire-only episodes at the ~1-point scale. For example, compare ISO with an ISO variant whose δ-only episodes are replaced by δ = 0 fire-only episodes, or evaluate ISO-4 at θ\* with δ = 0 against δ = 1.
   - Discuss the train/test comms mismatch: ISO-4 is trained with δ = 0 and tested at δ = 1.
3. **State the identifiability limit (W2).**
   - Write out the identity active share = μ_A + μ_B − p and its consequence: no contrast in this design family varies co-occurrence at fixed frequency and fixed active share.
   - Revise the §9.3 recommendation accordingly: say what must be matched, and what, if anything, can then be attributed to composition.
   - Discuss designs that could identify composition.
4. **Correct the statistical terminology and claims (W4).**
   - Call X the MDE. Make every exclusion statement from CI bounds; fix in particular the High-readout sentence and the "gap of either sign" sentence.
   - Flag or explain the k = 72 completion null's 71.6% realized power at the 0.03 effect, which is below the 0.80 POWER_STOP registered for design-stage power.
   - Report Γ₄'s and Γ₄′'s survival MDEs in the text.
   - Downgrade the High-severity smoke result to descriptive/ungraded, or provide a proper test with intervals.
   - Remove "conservative" for the k increase and justify or drop the covariance argument.
5. **Clarify blinding (W5).** List every outcome-derived quantity visible before unblinding: floor-run arm means, differential drift (bias (b)), per-arm logs. State which were seen when the k = 72 and ISO-4 decisions were made, and reconcile this with "the first computation of any outcome contrast".
6. **Make the theory self-contained and consistent (W6).**
   - State Prop. 4 precisely, or demote it to a remark.
   - Specify the limit in Prop. 3 and justify (or drop) the derivative claim; retitle it.
   - Reconcile Thm. 1's stated signal model with the implemented toy and the reported q(8) = 0.0056 and J\* − ½ = 0.0000.
   - Fix the ℓ_f clash in Remark 2′; prove or demote Remark 2′(i); drop "refines Pynadath & Tambe".
   - Remove all references to the unavailable "formal specification".
7. **Rewrite for readability (W9).**
   - A proper abstract of at most about 250 words.
   - Move dated rulings and project history to an appendix.
   - Remove internal study codes from the main text and figures.
   - Define each term at first use and cut repeated caveats.
   - Relabel figures in plain language rather than translating their labels in captions ("labelled m44", "'unit 1' is GPU 1", "labelled 'knee'").
   - Fix the sentences listed in §8 below.
   - Position §8 against the RL evaluation and reproducibility literature.

### Minor

1. Tone down the "ambient hazard / hazard-blind reward" framing and discuss that the death penalty is functionally a hazard-contact penalty (W7).
2. Add safe-RL hazard benchmarks (Safety Gym, Safety-Gymnasium, safe multi-agent suites) to Table 1, and discuss generalization benchmarks in MARL.
3. Report absolute arm means (ISO, JOINT, ISO-4) at θ\* in the main results table. Show absolute learning curves for both arms, so readers can judge how far from convergence T\* = 1000 is.
4. Report total compute (GPU-hours) across grid, floors, ISO-4, secondary arms and calibration.
5. Seeds per cell in the calibration grids are inconsistent:
   - the Coupling-B grid has "two seeds" at High but a "three-seed spread" at Medium (§6.4);
   - in `coupling_a_explorer.html`, the m35 whiskers have zero width at High and near-zero width at Medium, which suggests one seed despite "two seeds per arm".
   
   Please state the counts per cell.
6. Justify the Γ(t) sign-stability rule, or supplement it with an interval-based robustness criterion.
7. Prop. 3 handshake run 1: an R² from 5 points through the origin is weak evidence. Report the slope against the χ(β) reference, with a CI.
8. Strip internal comments from the code listings ("M1.3", "invariant #3", "Q3 ruling", "DECISION:") or explain them.
9. Define "weak-floor smoothing passes" (App. B) and how the "spatially clustered" weak terrain is generated (Def. 5).
10. Fig. 3: print the Γ₄ completion interval (the figure data have `ci: null` for it, while the table gives [−4.81, +2.28]). Use one unit (points or fractions) consistently across text and figures.
11. Consider a test configuration where both couplings are behaviourally live (for example a larger κ_B at Medium, or a severity where both clear a measured effect bar). Without one, the study cannot address its own question.
12. References: give arXiv identifiers or venues for preprints. Several print with only authors and year, for example de Witt et al. 2020, JaxWildfire, Raut et al., Multi-Agent Craftax, Assistax, POBAX, Hu et al. Remove the unused `.bib` entries (`jaderberg2017pbt`, `zhao2020simtoreal`). Fix the BibTeX citation block's `year = {October 11, 2026}`.

---

## 7. Broader concerns

- **Ethics.** I see no significant ethical risk. The environment is abstract; there are no human subjects or personal data, and the dual-use potential is negligible. The fire-rescue motivation is never claimed to transfer to real robots, and Limitation 3 explicitly disclaims "swarm".
- **Reproducibility.**
  - No code or data are provided to reviewers (W5).
  - Checkpoints are said to be archived with sha256 hashes, but they are not shared.
  - The locked critical point β̂_c has no committed estimator (stated by the authors).
  - One floor set has 1 of 12 archives hashed.
  - The registry-consistency test and the bitwise-nesting tests are good ideas, but unverifiable here.
- **Use of LLM assistance.** The authors disclose extensive LLM involvement: "drafting design documents and reviews, proposing options for our decisions, writing and running code and analyses, making figures, helping with literature search and citations, and drafting this text from our records". Disclosure is appreciated and appropriate. Several consequences concern me:
  - Some literature characterizations are very specific: which tables of Erdem & Üre (2025) show what, sections of Gao et al. (2024), the construction in Chen et al. (2022, Prop. 1), theorem numbers in Pynadath & Tambe (2002). Yet the search notes say non-detailed citations "rest on their abstracts". I did not verify these (no web lookups). The authors should confirm every specific claim against the full text.
  - The manuscript reads as generated from internal logs: internal codes, references to unseen records ("lock record", "re-test report", "the ruling", "review §6", "formal specification"), and a pervasive procedural register. This substantially harms readability (W9).
  - The footnote says the LLM drafted "design documents and reviews". The registered design contained "a question it set for reviewers" that rested on a premise "false for both" arms. The resulting error was caught by "a review of the registered design" (§9.1). It would help to state which documents, reviews and design decisions were written or checked by humans.
- **The registration's outcome-dependent "framings" and "venue-lean column"** (App. E). Pre-writing a framing per outcome branch is a legitimate registered-report practice. A per-branch venue column is unusual and unexplained, though not by itself a scientific problem. The authors handle the branch-B headline transparently by stating it "no longer holds as worded".

---

## 8. Unclear or garbled sentences

Quotations are verbatim from the manuscript. Mathematical notation is transcribed from the PDF rendering into plain text and Unicode. "p." is the printed PDF page.

**Opening paragraphs (abstract-equivalent) and Figure 1**

1. p.1 — "We ran 72 seeds per arm, above the registered cap of 60, a recorded deviation made before unblinding." — "Registered cap" and "unblinding" are undefined at first reading, so the reader cannot tell what rule was deviated from.
2. p.2 — "Both differences are sign unstable over the final half of training: the survival gap opens only in the last fifth, and completion leans negative from 70 % of the budget." — "Sign unstable" is a registered term not yet defined; "last fifth" of what is left implicit.
3. p.2 — "The survival gain does not survive the inert-share correction." — The "inert-share correction" is used before it is explained.
4. p.2 — "Communication denial, inert under a frozen random-projection encoder at this scale, is the only stressor in a third of the isolated arm's training episodes, which are thus fire-only in effect." — Stacked qualifiers; "at this scale" is vague; the encoder has not been introduced.
5. p.2 — "This is our design error: we kept a stressor already found inert and did not count the fire-only share it created; found before the main training runs, the bias was registered with its correction while they ran, before unblinding." — Dangling participle ("found before …"); "while they ran" has an ambiguous referent.
6. p.2 — "The correction is a 20-seed sensitivity arm without those episodes, outside the two confirmatory tests; joint training's survival differs from that arm's by −0.03 points (Šidák-corrected CI [−0.68, +0.63]), though it still sees each coupling twice as often, always combined." — "It" is ambiguous; "always combined" is unclear.
7. p.2 — "Severity is set relative to a measured percolation threshold; each stressor is a parameter of one transition or observation kernel, and switching it off reproduces the nested model's trajectories bit for bit." — "The nested model" is undefined in the abstract.
8. p.2 — "We describe a measurement protocol with reproducibility floors per metric, per GPU and per artifact." — "Floor" and "per artifact" are undefined at this point.
9. p.2 (Fig. 1 caption) — "Only the selected agent's three panels concern perception: its observation as produced (labelled obs v3, the masking observation), those cells' true state, for comparison, and P(seen) = τ, the transmittance through smoke." — "Obs v3" and "masking observation" are internal version names; "as produced" is unclear.
10. p.2 — "Recurring statuses: illustrative (grades nothing); registered (read by a rule fixed before unblinding); sensitivity arm (outside the two confirmatory tests); secondary (carries no verdict); descriptive (no test); reference scale (cross-artifact), a spread measured on other runs, shown for scale only." — "Grades nothing", "carries no verdict" and "cross-artifact" are idiosyncratic and undefined.

**§1 Introduction**

11. p.3 — "Four outcome branches, a framing for each and a falsifier were registered on 2026-08-13, before the grid began (a fifth was added before unblinding, the first computation of any outcome contrast; Appendix E)." — "The grid" is undefined; the appositive attaches ambiguously.
12. p.4 — "A secondary sweep in the spirit of DBCA varies co-occurrence at fixed frequency, but its fire-only share rises with co-occurrence, and it bears no verdict (§9.1)." — "Bears no verdict" is jargon.
13. p.4 — "At the test's severity Coupling B was behaviourally quiet in calibration: its own survival effect was within the spread over three seeds (§6.4), and none of the three severities has both couplings strongly live (§10)." — "Strongly live" is undefined.
14. p.4 (Fig. 3 caption) — "Survival: Γ REJECT; the gain “does not survive the inert-share correction” (Γ₄ null). Completion: Γ null; Γ₄ null, a second exclusion bound." — Telegraphic; "a second exclusion bound" is meaningless at this point.
15. p.4 (Fig. 3 caption) — "The text quotes the printed rate differences × 100, as points." — Hard to parse; "printed" where?
16. p.4 — "The founding hypothesis, that joint training improves both outcomes, did not occur." — A hypothesis is supported or not; it does not "occur".
17. p.4 — "The falsifier registered for an asymmetric outcome passes (§9.2); under Definition 2 the asymmetry lies between a penalized channel, deaths, and a rewarded one, the task." — "Passes" is ambiguous for a falsifier: was the claim falsified, or did it survive?
18. p.4 — "A same-GPU replicate, proposed after Γ₄ was seen, agrees." — A replicate of what, on which GPU, is not said.
19. p.4 — "The correction excludes only a large composition effect, and ISO-4 changes the active share and each coupling's frequency together; §9.2 states both limits, what the secondary design adds and where its fit fails." — "Its fit" is ambiguous.
20. p.5 — "CHE, an environment built as an instrument, with severity by measured dynamical phase, bitwise-exact nested ablations and theory that doubles as unit tests (§3–§7)." — "Theory that doubles as unit tests" is unclear.
21. p.5 — "Under the measurement protocol of §8, acceptance bars come with floors measured per metric, per GPU and per artifact, and the bars that lack one are named." — "Bars" is undefined jargon.
22. p.5 — "A pre-registered test of joint against isolated training (§9), whose survival advantage does not survive the inert-share correction, which was registered before unblinding." — "Which" is ambiguous: the test or the correction?

**§2 Related work**

23. p.5 — "VULCAN's preliminary evaluation covers baselines only, and its evaluation metric, cumulative hazard exposure, is also abbreviated CHE, unrelated to our environment's name." — "Covers baselines only" is unclear.
24. p.7 — "Their design thus bundles per-modality frequency, co-occurrence and a larger budget, which is nearer to what our corrected contrast leaves in, where JOINT still sees each coupling twice as often as ISO-4; it neither supports nor contradicts our corrected null." — A chain of relative clauses; unclear what is "nearer" to what.
25. p.8 — "Theorem 1 (§6) is kin to the construction of their Proposition 1, in which an irreversible choice is made before anything distinguishes the candidate MDPs, but that construction does not cover Theorem 1." — "Does not cover" is unclear.
26. p.8 — "Read as a latent MDP with the signals encoded as states, the toy has an absorbing failure, so their upper bounds do not apply either." — "Either" has no clear antecedent.
27. p.8 — "Remark 2′ (§7) refines this for collective partial observability: communication's marginal value vanishes when interchangeable agents' views are redundant, and returns when roles are irreplaceable or deaths are costly." — A value-of-communication statement cannot "refine" a complexity classification.

**§3 The environment**

28. p.8 (Fig. 4 caption) — "Arrow colours are this figure's own." — Unclear; presumably the colours do not match other figures.
29. p.9 — "In the listing, tl is the episode's θ, and no configuration here uses the early frozen control branch." — The "early frozen control branch" is never explained.
30. p.12 — "One test of clause (i) asserts identical rewards, with and without the death penalty, for states that differ only in fire, smoke or structure; fire and structure differ only far from every agent, which pins the alive transition equal (che/tests/test_reward_independence.py:6-15)." — "Pins the alive transition equal" is awkward and unclear.
31. p.12 — "The draws for Coupling B's reveal, the links and the per-episode mixture use streams derived from the reset or step key by a fixed tag, so adding them left the existing streams untouched." — "By a fixed tag" is implementation jargon.
32. p.12 — "Setting a stressor to zero therefore changes comparisons only, and the same keys reproduce the nested model's trajectory bit for bit." — "Changes comparisons only" is unclear.
33. p.13 — "A structural test also asserts that the traced computation keeps its random-number primitives at parameter value zero, catching a gate such as if kappa_A > 0: that behavioural tests miss (che/tests/test_nesting.py:222-240)." — "Traced computation" and "keeps its random-number primitives" are JAX-internal and unexplained.

**§4 Severity calibration**

34. p.13–14 (Fig. 5 caption) — "Right: one random-policy episode per level under the severity configurations, with δ 0; only the fire and its smoke (hatching) are drawn." — "With δ 0" is garbled (δ = 0); "the severity configurations" are undefined.
35. p.14 — "The correlation length motivates the levels; operationally, each level is the observable band it was locked to, that is, fixed on 2026-07-19, before the main experiment (§4.3)." — "Each level is the observable band it was locked to" is garbled; "locked" is undefined.
36. p.15 — "The lock record states that they were recomputed independently from the committed raw data; no committed script or artifact produces the logistic centres." — Refers to internal documents; the implication (the locked estimate cannot be reproduced) is left implicit.
37. p.15 — "Among the committed estimators, pairwise crossings of R_L average 0.504; the family spans [0.480, 0.513], with consensus mean 0.499." — "The family" and "consensus mean" are undefined.
38. p.15 — "The re-test at fixed policy re-ran it from the same configurations and seeds (equivalent, not bitwise identical) and evaluated each final checkpoint on 512 episodes." — "Re-test at fixed policy" is unclear.
39. p.15 — "The re-test report offers an account it did not test: outcome variance is roughly the environment's variance, which peaks near criticality, times the policy's sensitivity to it, which grows with severity." — "The re-test report" is an internal document the reader does not have.

**§5 Coupling A**

40. p.16 (Fig. 6 caption) — "Top: collapse-seeded ignitions per episode by severity, and their share inside an alive agent's crop, in the Coupling-B and Coupling-A calibration grids (labelled m44 and m35; Phases 3 and 4 are calibration stages)." — "Phases 3 and 4" are undefined anywhere in the paper.
41. p.16 (Fig. 6 caption) — "Bottom: the two runs, kept apart, neither at the locked parameters; the second (v2, a revised test) has no committed data file, so its panel gives the reported values." — "Kept apart", "committed data file" and "reported values" are unclear.
42. p.16 — "The theory states the impulse per collapse event; the implementation draws one uniform per cell, and the two rules coincide wherever seeding neighbourhoods do not overlap." — "The theory" refers to a document not in the paper.
43. p.16 — "Load adds 0.4 to 1.4 % to that count under trained policies (the Coupling-A calibration grid of §5.3) and 7.4 to 8.3 % under random ones, which is 6.9 to 7.6 % of all collapses." — Percentages relative to different bases; hard to parse.
44. p.17 — "In a finite protocol the equality is approached only with an unconditional cluster-mass reference (a spanning-conditioned one understates the mass), matched seed locations and ages, and sparse seeding; boundary clipping, seed age and overlapping seeds each lower the measured slope (Appendix A)." — "Cluster-mass reference" and "spanning-conditioned" are unexplained.
45. p.17 — "The second, a slower test in the suite on a 32 × 32 grid (κ_A = 0.003), divides its slope by a protocol-matched reference computed inside the test: 0.992, inside the band [0.90, 1.02], with R² = 0.9995." — "Protocol-matched reference" is unexplained; the origin of the band is not stated.
46. p.18 — "This concerns ignitions only: the Coupling-A grid's survival contrasts, on two seeds per arm and with no floor, cannot locate the coupling's largest effect on outcomes." — "Locate the coupling's largest effect" is unclear.
47. p.18 — "A later prediction was written after the trained results existed and before its own analysis." — "Before its own analysis" is unclear.
48. p.18 — "The 4.83-fold fall confirms the first, which earlier reports already answered." — "Earlier reports already answered" is unclear.
49. p.18 — "The count is monotone non-increasing and Low and Medium are indistinguishable, so the second is not supported and the third is refuted." — The second "prediction" ("need not be monotone") is not a falsifiable claim, so "not supported" is unclear.
50. p.18 — "No contrast in this section has a floor on its own artifact, since neither grid has identical reruns; any floor beside them is a reference scale (cross-artifact); see §8.6." — Chain of undefined jargon.

**§6 Coupling B**

51. p.19 — "The theorem also tests the code." — A theorem cannot test code; presumably its closed form is used as a test oracle.
52. p.19 — "The measured optimal value matches ½ + ½q under a three-condition gate: largest |z| 2.11, Σz² = 6.55 on 8 degrees of freedom (p = 0.586), and mean z −0.44." — The "three-condition gate" thresholds are not stated.
53. p.19 — "The memorizing policy stays flat at ½, J*(0) = 1.0000, and J* − ½ = 0.0000 at κ_B = 8, where q = 0.0056." — Thm. 1 predicts J\* − ½ = q/2 = 0.0028 here; it is unclear whether 0.0000 is a measurement (a mismatch) or a rounding. Also, q(8) = 0.0056 is not attainable from the stated formula with ℓ_f ≥ 1.
54. p.20 — "The same κ_B attenuates the arena's extended smoke more strongly than the toy's single smoke source, which leaves the detection and toy bands disjoint by a factor of 1.35 under a random policy and 1.15 under probe policies." — "Disjoint by a factor" and "probe policies" are undefined; "single smoke source" conflicts with Thm. 1's "unit smoke density".
55. p.20 — "It was judged against a three-seed spread, σ_seed = 0.72 points, with no measured floor; the Medium survival floors measured later, on two GPUs, are 1.29 and 1.30 points." — The same grid is described as having two seeds (High, same section) and three seeds (Medium).
56. p.21 — "Within trained policies at 500 updates the attenuation was not behaviourally suppressed: the coupled policies' masking ceiling, which does not depend on κ_B, sat at or above its random-policy value at every severity." — "Masking ceiling" is undefined.
57. p.21 — "It was meant to catch both couplings at once, but only Coupling A produces those ignitions and κ_B does not enter the count, so the counter is co-active only in all-on configurations." — "Co-active" is undefined.

**§7 Communication denial**

58. p.21 — "In CHE, under a frozen encoder, no measured effect of it cleared a valid bar (Figure 9; one threshold is VOID, §7.3)." — "Valid bar" is jargon.
59. p.22 (Fig. 9 caption) — "(a) The courier variant of the corridor toy (labelled E2C² and M5.2), scripted policies: success with free and with denied communication on the no-idle schedule (pinned); the shaded gap is VoC_gated (§7.2)." — "(Pinned)" is unexplained.
60. p.22 — "The theory's range-dependent link probability is implemented as this hard Chebyshev range." — "The theory" is not in the paper.
61. p.23 — "When any qualifier fails, value returns; in general it scales with the deficit of agents relative to hypotheses, and a death cost, such as CHE's d_p = 0.5, prices the redundancy that substitution spends." — "Prices the redundancy that substitution spends" is opaque; "scales with" is unquantified.
62. p.23 — "…with slack ℓ_f, optimal denied play buys information by idling at the branch and achieves ½ + ½q̃(κ_B), where q̃ is the probability of being informed by the commitment point under the best idling schedule, with q̃ ≥ q (equality iff ℓ_f = 0), so" — ℓ_f is the fire depth (≥ 1 in Thm. 1) but is reused here as "slack"; "equality iff ℓ_f = 0" contradicts Thm. 1.
63. p.23 — "Both q and q̃ decrease in κ_B, so the value of communication increases with perception decay." — "Perception decay" is ambiguous (it presumably means increasing κ_B).
64. p.23 — "Nothing establishes that they are at least as numerous as the hypotheses, and their deaths are priced (d_p = 0.5), so the clean-zero conditions are not fully met." — "Hypotheses" is undefined for CHE.
65. p.23 — "Every bar here is a post-hoc floor grading that a true effect of its size would clear only about half the time (§8.2), so none of these results is a point null." — "None of these results is a point null" is unclear.

**§8 Methodology**

66. p.24 (Fig. 10 caption) — "Reproducibility floors per GPU, per artifact and per run length, and the confirmatory grid against its floor, one tab each, with its confound." — "With its confound" is unclear.
67. p.24 — "A threshold below its instrument's noise cannot pass under the null, so its output is void, and a void test voids a PASS as it voids a FAIL." — "Cannot pass" holds only for equivalence-type ("no difference") tests; the direction is unstated.
68. p.24 — "The rule followed four bars with invented constants (Appendix C)." — "Followed" is ambiguous (came after, or adhered to).
69. p.25 — "Re-measuring the Medium floor moved completion's 2.75-fold and left survival's unchanged, 0.0129 against 0.0130." — Garbled ellipsis ("completion's" what?).
70. p.25 — "The per-arm forms, each arm's own s√(2/k), bracket that value without equalling it: at k = 34, on the 1000-update completion floors and a 0.03 effect, ISO's gave 92.1 % power and JOINT's 62.8 %, where the contrast's power was 76.7 %." — The origin of k = 34 is never explained.
71. p.25 — "The confirmatory seed count was first ruled at k = 20 on such a figure, without the Šidák correction; corrected, completion had 55.6 % power against its motivating effect band, a slip caught before any run." — "Motivating effect band" is undefined.
72. p.25 — "A registered convergence check, retired before the grid, divided each arm's late-training drift by its floor, so any nonzero drift fails as the floor goes to zero; it fired when JOINT's floor fell faster than its drift." — Floors elsewhere grow with run length; "fell faster than its drift" is unclear.
73. p.26 — "That grid's inertness falsifier, logged before its data, included the condition “no cross-arm exposure/positioning difference”, which could not see a drift present in both arms; the verdict it fed rests on its other conditions." — "Inertness falsifier" of what? "Logged before its data" is unclear.
74. p.26 — "The differential drift between the arms, bias (b) of §9.1, changed sign between the four floor studies that read it at 1000 updates before unblinding, so §9.1 reports every reading." — No "bias (a)" is ever defined.

**§9 The pre-registered test**

75. p.27 — "Every configuration in Θ_iso differs from θ* on the states where both couplings act at once, a collapse-seeded fire within perception-attenuation range of an agent (proof idea in Appendix A)." — Configurations also differ in β everywhere; what "differs on states" means is unclear.
76. p.27 — "Its prediction about ISO's exposure to that region was not tested, because the counter built to measure visits there (§6.5) is co-active only in all-on configurations (§9.2)." — An upper bound does not make a "prediction".
77. p.27 — "Positive cross-arm covariance, the expected sign given the shared seed integers, makes the unpaired test conservative." — Why shared seed integers would induce covariance between differently configured runs is not explained.
78. p.28 — "Raising the cap to 72 on 2026-09-22 was a deviation from a registered rule, recorded as one, made before unblinding, and conservative, since added seeds favour neither sign of Γ." — "Conservative" is misused: added seeds raise power and are sign-neutral.
79. p.28 — "A question it set for reviewers judged the arms symmetric on δ, on the premise that neither trains on δ = 1.0, which is false for both, and asked for a second opinion." — Garbled: a question cannot "judge"; the subject of "asked" is unclear.
80. p.28 — "A review of the registered design identified this on 2026-08-16, before the grid, noting that the confirmatory arm applied a different rule to the same fact as the sweeps." — "Applied a different rule to the same fact" is unclear.
81. p.28 — "The bias, its direction and ISO-4 with its reading rule were registered on 2026-09-18, mid-grid (120 of 252 runs) and before unblinding, on our attestation, recorded with the ruling, that no outcome mean had been computed or viewed." — Garbled clause order.
82. p.28 — "Bias (b) is the registered caveat on differential drift: JOINT − ISO completion drift over the last 100 of 1000 training updates, a local sensitivity estimate and never a bound." — "Local sensitivity estimate" is undefined; bias (a) is missing.
83. p.29 — "Its exclusion bound X, the gap of either sign the design would detect with 80 % power, is 3.29 points, and the negative point estimate does not reject." — Conflates the MDE with exclusion; the CI does not exclude a gap of −3.29.
84. p.30 — "Branch B's registered headline, “composition is paid in agents, not task return”, no longer holds as worded." — The headline itself is cryptic and never explained.
85. p.31 (Fig. 13 caption; also App. H, p.42) — "…the “no-element share” is the fire-only share's part of the sweep's endpoint change." — Unclear what "part" means.
86. p.31 — "Both co-primaries are null, so the reading is an a-fortiori exclusion: no gap larger than 3.40 completion points or 2.54 survival points at High even where JOINT trained on the evaluated configuration and ISO never saw a composed one." — The numbers are MDEs, not interval bounds; the a fortiori logic is unclear.
87. p.31 — "At High, Coupling B's survival effect replicated in direction in 3 of 3 contrasts (§6.4) while Coupling A is marginal (§5.3), the mirror image of θ*'s Medium siting (§10)." — "Mirror image of θ\*'s Medium siting" is unclear.
88. p.32 — "This follows from the comparison's design alone, as JOINT's threefold per-coupling frequency over ISO does." — Garbled comparison.

**§10 Limitations**

89. p.32 — "By the project's own locks, no severity has both couplings strongly live: at Medium B is quiet and A live, and at High A is marginal by construction (§5.3) and B live." — "Locks" and "live" are jargon.
90. p.32 — "The pre-unblind line that read a Medium survival effect as one “the single coupling did not show” is struck: Γ₄ and Γ₄′ contradict it." — Garbled; unclear what was claimed and what is retracted.
91. p.32 — "Every interval in §9 is conditional on one common evaluation draw, seed 0 × 512 episodes, which cancels in Γ; the intervals carry training-seed variance only." — "Cancels in Γ" holds only absent policy × episode interaction; unclear.

**§11 Reproducibility**

92. p.34 — "The §9 checkpoints were archived off the rented machines with recorded sha256 hashes, except a partial floor set that grades nothing, in which one of 12 archives has a hash (Appendix F)." — Confusing: which set, and why does it matter?

**Appendices**

93. p.34 — "The proofs follow the formal specification in the notation of Definition 1, and departures from it are noted." — "The formal specification" is not provided.
94. p.35 — "The formal specification adds a divergence rate near the critical point, which rests on critical exponents the paper does not state (§4.1)." — Refers to an unseen document.
95. p.35 — "In the Proposition 3 measurements (§5.2) the four factors compose to the observed slope within Monte Carlo error." — "Compose to" is unclear; no numbers are given.
96. p.36 — "The formal specification displays the bound with an explicit constant and concludes more about ISO's slack than an upper bound can show; the paper states the bound in words and draws no such conclusion (§9.1)." — Unseen document; "ISO's slack" is undefined.
97. p.36 — "The correction peaks at moderate κ_B, and its relative bite on the value of communication is largest at low κ_B, where q is near 1." — "Relative bite" is informal and undefined.
98. p.38 — "The rule of §8.1 followed four bars whose constants the ruling calls invented." — "The ruling" is unidentified; "followed" is ambiguous.
99. p.38 — "Those floor data predate the comparison, and the ruling records that a difference above the floor would have left the verdict NOT INERT standing." — Hard to parse.
100. p.40 — "Branches A–D were registered on 2026-08-13, each with a framing; the registered table's venue-lean column is omitted." — "Venue-lean column" is unexplained.
101. p.40–41 — "The confirmatory artifact holds all 72 seeds of ISO and JOINT on GPU 1: 76 runs executed there and seeds 13–46 copied from the grid." — The reader must reconstruct the arithmetic (144 runs = 76 executed + 68 copied).

---

## 9. Presentation and format

### Printed PDF

- **Layout wastes the page.** Text occupies a narrow column (roughly 40% of the page width), producing 46 pages for what is a medium-length paper.
- **Figures are illegible in print.** The static companions of Figs. 2, 3, 4, 6, 10, 11, 12 and 13 are printed at a size where axis labels, tick labels and annotations cannot be read (pp. 3, 4, 8, 16, 24, 29, 30, 31).
- **Small fonts.** Tables print at about 10 px and code listings at about 9 px. This is hard to read on p. 10 (Listing 1), p. 15, p. 27 and pp. 36–37.
- **Page footers appear clipped.** The "N of 46" footer appears cut off at the right edge on every page.
- **Orphaned and split elements.**
  - The Listing 1 caption is orphaned at the bottom of p. 9 while its code is on p. 10.
  - The Fig. 5 caption is split across pp. 13–14, with its first half running down to the footer line of p. 13.
- **Interactive instructions in print.** Print captions still carry "Interact: play, scrub, …" text (Figs. 1, 2, 5, 6, 10–13), and the body says "press ] in Figure 1" (p. 15). Both are meaningless in print.
- **Double captions.** Each printed figure has two captions: the figure caption, and "Static companion of Figure N for the printed PDF". This is redundant.
- **Results table wraps badly** (p. 29). Intervals wrap mid-entry, and "95 %" breaks with "%" on the next line.
- **Line-break artefact.** On p. 16, the locked-values tuple in Def. 5 breaks so that ", so the seeding neighbourhood…" begins a new line with a comma.
- **References are incomplete.** Several preprints print without an arXiv ID or venue (de Witt et al. 2020; JaxWildfire; Raut et al.; Multi-Agent Craftax; Assistax; POBAX; Hu et al.).
- **Malformed citation block.** The BibTeX block at the end has `year = {October 11, 2026}`.
- **There is no labelled abstract.**

### Interactive version (from HTML source)

- **Strengths.** All figures are self-contained (no external scripts), with sensible keyboard handling, tooltips with keyboard parity, table views, and dark-mode support.
- **Internal codes in figure labels.** Labels use internal codes ("m44", "M4.4", "M5.2", "M5.5", "E2C²", "unit", "card", "rung", "knee", "sweep_c50_p000", "obs v3"), which the captions then have to translate. Relabel the figures directly.
- **Fig. 3 (`opening_ladder.html`) omits a number.** It prints no interval for Γ₄ on completion (`ci: null`) although the text table gives one. Its units (fractions) differ from the text (points).
- **Fig. 11 (`ladder_registered_readings.html`)** likewise prints numeric intervals only for some rows.
- **Episode explorers (Figs. 1, I1, I2).** Keyboard agent selection covers "1–9" for 12 agents, so agents 10–12 are reachable only by clicking.
- **Iframe sizing.** Self-sizing relies on same-origin `frameElement`. Otherwise the fixed heights set in `_styles` apply, which the figure code's own comment notes "clip on phones".
- **Fig. 5 caption versus figure.** The figure's header states "severity configs (κ_A 0.06, κ_B 1.0, δ 0)", so its renders include Coupling A seeding. The caption says only "with δ 0" and "only the fire and its smoke … are drawn", which may suggest the pure fire kernel.

### Consistency

- **Calibration seed counts are reported inconsistently.** The Coupling-B grid has "two seeds" at High but a "three-seed spread" at Medium (§6.4). The m35 whiskers have zero width at High (near-zero at Medium) in Fig. 6's data.
- **Thm. 1 is inconsistent with its handshake numbers** (q(8) = 0.0056; J\* − ½ = 0.0000), and ℓ_f is used inconsistently between Thm. 1 and Remark 2′ (see W6).
- **"Exclusion bound" is used for two different quantities:** CI bounds in the abstract, MDEs in §9.2 (see W4).

---

## 10. Recommendation

**Major revision.**

The confirmatory analysis is executed with a level of transparency and statistical care that is rare in deep RL. The numerical claims about Γ and Γ₄ are accurately reported, and the authors do not over-claim the confirmatory result. However:

- the reinterpretation that drives the paper's take-away depends on an "inert" label that is under-resolved and applied asymmetrically (W1);
- the recommendation omits a basic identifiability limit that undercuts it (W2);
- the test configuration gave composition little chance to show (W3);
- several statistical statements conflate MDEs with exclusions, and one "finding" does not meet the paper's own evidential bar (W4);
- the environment contribution cannot be checked without code, and the blinding narrative needs clarification (W5);
- parts of the theory are imprecise or inconsistent with the reported tests (W6);
- the manuscript is very hard to read in its current form (W9).

These are fixable, and the paper would interest a real part of TMLR's audience once fixed.

**Confidence: 4/5 (fairly confident).** I am confident in the assessment of the statistics, design logic and presentation. I am less certain about the completeness of the related-work search in fire, hazard and MARL environments, and I did not verify cited works online.
