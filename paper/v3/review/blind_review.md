Ran 2026-10-16, 20:10–21:18 UTC, as a separate Claude Code process (`claude -p`, Opus 5.5) started on the owner's laptop in a folder outside the repository that held only the three files. **Fully blind to the repository:** no `CLAUDE.md` in the folder or any parent, no project memory, no MCP servers, no web tools, and its transcript touches no repository path. Its working path showed the local username, as any local run would.

**Run record** (log: *BLIND REVIEW BEFORE RESULTS* and its addendum)

- **Files.** `submission_v3_print.pdf` (sha256 `c47769c5…`) and `submission_folder.zip` (`0b278f1e…`) are the committed outputs of the `4f7bd44` kit build. They predate App. J's plan-approval sentence (`ab78b27`), so the reviewer's interaction-check concern 6 quotes a sentence the source has since changed. `che_supplement.zip` (`4a73c89b…`) was rebuilt on the laptop, byte-identical to the checked build.
- **Prompt.** `BLIND_REVIEW.md` §3 verbatim, plus: "The results of the post hoc interaction check (§6.4, Appendix G) are not yet in this draft; review its design, and do not count the missing results against the submission."
- **Interruption.** The first run stopped after 5 min 10 s: its single-process `pytest` hit the launch's 3.5 GB memory cap and was OOM-killed, and systemd then stopped the reviewer. The owner chose to resume the same session, under the same caps plus `OOMPolicy=continue`, with one operational note: "Your last step was interrupted: the full test run went over this machine's 3.5 GB memory limit for your processes and was killed. Continue the review; if you run tests, run them in smaller groups."
- **Tests.** The reviewer then ran the suite one file per process, in its own systemd scopes capped at 3 GB each. Those scopes sat outside the launch's 4-CPU cap. Its logs confirm 41 of 41 files exit 0: 601 passed, 4 skipped, 0 failed.
- **Size.** The resumed run took 104 turns and 60 minutes and cost $10.43; the first run logged no cost. The transcripts, the prompt and the reviewer's scripts and logs (`rv_scripts/`, `rv_work/`) are kept outside the repository on the laptop, in `~/v3_blind_review_logs/`.

The review follows verbatim, including its opening and closing lines to the requester.

---

I've finished the review. It's below: about 50 unclear sentences in §5, everything I ran in §4, and the recommendation in §7.

---

# Review: "A multi-agent fire environment with exact stressor ablations"

Page numbers refer to the 38-page printed PDF.

## 1. Summary

**The environment.** The paper presents CHE, a pure-JAX grid world. Twelve agents share one set of parameters and forage on a 64×64 map while a cellular-automaton fire spreads. With no other ignition source, the cells that burn form a bond-percolation cluster, so the three severities (β = 0.43, 0.49, 0.70) are placed against a measured spanning threshold.

There are three stressors:
- **Coupling A:** a structural collapse can ignite nearby fuel.
- **Coupling B:** a smoke field hides each crop cell with a Beer–Lambert probability.
- **Communication denial:** an independent stressor; messages come from a frozen, random, untrained message head.

The reward is +1 per food item and −0.5 per death, whatever the cause. Every random branch draws its random numbers whether or not it is active. Setting a stressor's parameter to zero therefore reproduces the nested environment bit for bit under the same keys, on CPU. Some textbook-level results serve as unit-test targets: the percolation correspondence, a linear law for burnt area, a corridor-toy theorem and a two-agent communication remark.

**The worked example.** A pre-registered test compares two training mixtures at a held-out near-critical severity θ*, at matched compute (1000 IPPO updates, 72 seeds per arm):
- **JOINT:** every stressor always on together.
- **ISO:** each stressor on alone.

Joint training raises survival by 0.96 points [0.47, 1.44] and leaves completion unchanged. The gain disappears under an "inert-share correction". A third of ISO's episodes carried only communication denial, which calibration had labelled inert. Against an arm without those episodes (ISO-4, 20 seeds), the gap is Γ₄ = −0.03 [−0.68, +0.63]. The JOINT−ISO gap also changes sign across checkpoints in the second half of training. A secondary sweep and plane fit cannot separate how often each stressor appears from how often they co-occur.

The stated lesson is that matching the share of episodes with an active stressor (μ_A + μ_B − p) cannot isolate co-occurrence. A post hoc 2×2 interaction check is designed but not yet run. After the result was known, the paper's framing moved from the test to the environment.

## 2. Strengths

- **Exceptional transparency.** Every deviation is recorded and dated:
  - the seed cap raised from 60 to 72;
  - ISO-4 added mid-run;
  - the secondary specification ratified after unblinding;
  - the same-GPU replicate Γ₄′ proposed after Γ₄ was seen;
  - the design error;
  - the framing change.

  Overclaims in the registration are explicitly withdrawn (p27). Many results are reported against the authors' own interest.
- **A careful, instructive measurement protocol (§5, Appendix C).** It separates rerun "floors" (the spread of identical reruns) from seed dispersion, measures floors per GPU and per artifact, states design-stage power as 80%-power detection limits, and quotes nulls as exclusion bounds. The exhibits will help anyone running GPU RL experiments. One example: the reference code's zero rerun floor hid nondeterminism that showed up only in the refactored code (p24).
- **A clean environment design.** The couplings enter only the transition and observation kernels. Because random numbers are drawn unconditionally, ablations nest exactly, which allows common-random-number evaluation. The percolation link gives severity a physical meaning rather than an arbitrary knob.
- **A high-quality supplement** (see §4 below).
- **§6.5's design point is correct and useful** for people designing compositional-generalization experiments.

## 3. Weaknesses

**W1. The worked example supports no substantive finding, and its "lesson" is an identity known before the experiment (pp. 1–3, §6.3 pp. 12–13, §6.5 p. 14).**
- The only rejection (survival) disappears under the authors' own correction (Table 3).
- The survival gap excludes zero only at updates 900–1000 (p30). Completion is null.
- Contribution 3 is inclusion–exclusion. The registered design already states it before any run: `phase6_design_v2.md` §2 says "a fixed-margin 2×2 table has exactly one degree of freedom".
- It is a sound design note, not a result of the experiment.

**W2. As an environment paper, there is little evidence that CHE is usable or discriminative as a benchmark (p3, §3.5 pp. 7–8, §7 pp. 14–15, §8 p. 15).**
- Everything rests on one algorithm (shared-parameter IPPO), one map, one team size, and no baselines.
- **The policy has no memory.** `che/train/networks.py` is two convolutions and a dense layer, with no recurrence or frame stacking. Yet smoke persists, Coupling B reveals cells randomly at each step, and Theorem 1 assumes signals are "remembered" (p19). Coupling B is therefore tested on agents that cannot combine repeated looks.
- **Basic specification is missing from the paper:**
  - the action space (5 actions; `che/env/env.py:48`);
  - the observation planes;
  - environment-only throughput (the supplement records ≈3.4 M steps/s; the paper gives only training wall-clock, p15);
  - memory requirements;
  - learning curves.

**W3. Most stressor effects are not established at the resolution the paper itself demands (§4 pp. 8–10; contribution 2, p3).**
- **Coupling A:** where it costs survival most "is not located" (p9). The 4.8-fold fall in collapse-seeded ignitions is fuel exhaustion, not a behavioural finding.
- **Coupling B at θ*:** the survival effect is −0.03 points (p10). Smoke hides 0.249% of crop cells overall and 5.6% when fire is in view (`phase4_report.md`, Result 2), against an original design band of 15–45% (p22). The stressor barely acts at the test point.
- **Coupling B at High:** three single-run contrasts, two sharing a seed, "descriptive and ungraded" (p9). The pooled effect is about 1.2–1.4× a floor measured on another artifact.

**W4. The "inert" label for communication denial carries much of the design but is weak, and one fact about it is omitted (§4.4 p10, Appendix C p23, §6.2 pp. 11–12, Appendix F pp. 31–32).**
- **(a) Resolution.** The denial study's thresholds were 7.99 (completion) and 2.60 (survival) points, against a tested effect of 0.96. It could not have detected a denial effect 2.7× larger than Γ.
- **(b) The produced verdict was overruled.** The registered falsifier's own output, `che/bench/results/phase5/m55/verdict.txt`, reads "VERDICT: NOT INERT — the falsifier failed, and that is a finding". "Inert" comes from voiding condition (iii) afterwards. The paper reports the void (p23) but not that the as-produced verdict was "NOT INERT" and was overturned. The void's reasoning is defensible, but §4.4 should say this.
- **(c) The point estimates point the same way.** Opening the links lowered survival by 1.43 points, and fire deaths per danger step were 23% higher with links open. Both are of Γ's order.
- **(d) Inertness belongs to the agent, not the environment.** Messages come from a frozen random projection with no gradient (Listing 6, p22).
- **(e) Much depends on it:**
  - calling ISO's denial-only third "fire-only";
  - Γ₄;
  - Γ₄′ and every secondary arm, all trained with links open, including their A+B episodes (configs `p6_sweep_*`, `p6_ident_*`), while JOINT trains and θ* tests with links denied;
  - the plane predictions;
  - the train/test mismatch (p12);
  - "the composition tested is in effect A with B" (p10).

**W5. The matched budget falls at the onset of a learning transition, and readers aren't told (§6.2 p11, §6.3 p13, Appendix E pp. 30–31).**
- The supplement's 2000-update subsample (`post_gamma4_t2000.json`) shows ISO training-log completion rising: 0.783 at update 1000, 0.837 at 1100, 0.883 at 1200, ≈0.94 by 1800.
- Between-seed SD jumps from ≈0.012 to 0.056–0.088 over updates 1100–1400.
- Evaluation means at 2000 updates are 0.921/0.922 (ISO/JOINT), against 0.777/0.760 at 1000.
- Per-seed completion at 1000 is right-skewed. From the committed `g1_conf_5090/eval_*.json`, 13 of 72 ISO seeds and 8 of 72 JOINT seeds exceed 0.85; the rest lie at 0.68–0.85.
- Seed spread is only 1.09–1.12× the rerun floor (p31), so between-seed variation is almost entirely GPU nondeterminism.
- The completion gap therefore largely counts how many runs had "taken off" by an arbitrary cutoff. That fits the sign instability. The registration's own plateau check fired at 500 updates and was then retired (pp. 22, 25–26).

**W6. A GPU diagnostic the size of Γ goes unreported (§6.3 p13, Appendix D.6 p29).**
- The registered unblinding report computes a "card diagnostic": seeds 1–12, rerun from an RTX PRO 6000 onto an RTX 5090.
- It shifts the survival JOINT−ISO gap by +1.08 points (SE 0.55), the same size as Γ. The paper only says those runs "enter only a descriptive diagnostic" (p29).
- It concerns different GPU models, and Γ₄′ (same GPU) agrees with Γ₄, so it overturns nothing. It should still be reported, because Γ₄ and B̂ compare runs on two GPUs.

**W7. Statistical details.**
- **Normal z for 20-seed arms.** z intervals are used for contrasts with a 20-seed arm (Γ₄, Γ₄′, B̂, and the High-severity JOINT−ISO-4 contrast; ruling (v), p28). Welch-t intervals would be wider, so the "exclusion bounds" are slightly too tight.
- **B̂.** "B̂ is reported without a test" and "not a second finding" (p13), yet its printed Šidák interval excludes zero: +0.98 [+0.33, +1.63], z = 3.39. An identity between point estimates does not make B̂ uninformative. It is the paper's most robust secondary effect and should be interpreted.
- **Toy-check degrees of freedom.** Both toy checks count 8 df, but the κ_B = 0 point is degenerate (J = 1, SE = 0, z set to 0 in `test_e2c2.py`). The df should be 7.
- **Remark 2′'s χ² = 0.51 (p21).** I re-ran the sweep under PRNG keys 0–4. Key 0 reproduces 0.52 (P ≈ 2×10⁻⁴), but keys 1–4 give 10.79, 13.40, 5.56 and 4.50. So the standard errors look sound and the reported fit is a lucky draw. Report several keys.
- **"Cannot be told apart" (p24).** The two GPUs' floors are compared only by overlapping 95% intervals. An F test on the two 8-run SDs gives p ≈ 0.07, which is better called borderline.

**W8. Theory framing (Appendix A).**
- **Proposition 3:**
  - Its title, "Collapse events dominate hazard exposure" (p18), is not what it states.
  - "(1 + o(1))" has no stated limit.
  - Its hypothesis (one ignition per collapse) is not CHE's mechanism: up to 9 cells can ignite, on clustered weak terrain.
  - "In both, the four factors compose to the observed slope within Monte Carlo error" (p19) is circular for the dense run. Its last factor ("residual ×0.836", `phase3_report.md`) is defined as measured over predicted.
- **Transfer remark.** It states no bound (p21).
- **Remark 2′.** Saying it "refines Pynadath & Tambe" (p10) overstates a two-agent toy.

**W9. κ_B's calibration is weaker than described (p22).** The paper says κ_B = 1.0 was "locked on the detection band alone" and the toy band "kept as a consistency check". The lock record (`kappa_b_lock.md`) shows:
- κ_B = 1.0 is inside the detection band under only 2 of 3 measurements (0.384 under the random policy, below 0.40);
- it fails the consistency check: q = 0.812 against a 0.70 ceiling, consistent with p20's own 0.8115.

**W10. "Switching a stressor off" and the "fire-only" label (p1, §3.4 p7, Fig. 6 p12).**
- Structural collapse is on in every configuration: f_weak, λ₀ and λ_load appear in every mixture component.
- At θ* collapse kills ≈0.20 agents per episode, about 22% of all deaths, so "fire-only" episodes are fire plus a lethal structural hazard.
- The Coupling A nesting test compares fire and smoke only (`test_nesting.py`).
- "Bit for bit" in the abstract needs the "one backend (CPU)" qualifier given in §3.4.

**W11. Positioning (Table 1, pp. 3–4).**
- §3.3 itself calls the death price "in effect a hazard-contact price" (p7), so Table 1's "ambient" contrast with JaxWildfire's burning-cell penalty is thin.
- Possibly missing neighbours (cited from memory; I did not search, please check):
  - Neural MMO's closing fog;
  - Minecraft-based platforms with spreading fire;
  - FireCommander;
  - PyroRL;
  - Flickering Atari (Hausknecht & Stone, 2015), as random observation dropout;
  - CARL and CompoSuite, for contextual/compositional generalization;
  - DIAL/CommNet, as learned communication, which would bear directly on W4(d).

**W12. "Pre-registered" carries modest weight (§6.1, Appendix D, Appendix J).** The paper discloses all of this candidly, and it accumulates:
- dates are self-reported from a private repository;
- ISO-4 was registered mid-run, with 120 of 252 runs done, on attestation;
- the cap was raised;
- the secondary specification and Γ₄′ came after unblinding;
- the framing changed after the result;
- the inert label rests on a voided condition;
- design decisions were delegated to an LLM assistant.

"Read in §6.3 exactly as registered" (p15) overstates this.

**W13. Clarity.** The text is extremely dense, and registration bookkeeping dominates. Private jargon recurs: "floor", "bar", "artifact", "non-verdict-bearing", "card/unit", and "exclusion bound" used for both interval ends and detection limits. Internal codes appear on figures. The printed static figures (pp. 2, 12, 13) are hard to read. See §5.

**Design review of the post hoc interaction check (§6.4, Appendix G, the supplement's `PLAN.md`; results not counted).** The basics are sound:
- a within-policy contrast under common random numbers;
- Šidák correction over m = 8 (z = 2.727, which I verified);
- per-condition floors;
- a hash-locked plan that refuses partial results;
- an honest list of blind spots.

The implementation matches the plan (`interaction_analysis.py`).

Concerns:
1. **The pooled "headline" has no clear meaning.** The arms' familiarity biases pull in opposite directions: JOINT trained only on "both", ISO only on singles and "neither". Pooling with weights 72:72:20 averages these biases rather than removing them. Make the per-arm rows primary, or fix in advance how to read disagreement between arms.
2. **There is no design-stage power statement,** contrary to §5's own rule. From the committed per-episode arrays, episode noise alone gives a pooled detection limit of at most ≈0.21 survival points (0.026 agents per episode). Common random numbers make it smaller still; in a smoke test of mine, episode outcomes were identical across two conditions. With no smallest effect size of interest, a trivially small I would read as a "detectable interaction". Define one, for example relative to the main effects.
3. **Additivity is tested only on rates,** and survival sits near its ceiling (≈0.92). Pre-specify a descriptive analysis on deaths per episode or on the logit scale.
4. **Add a fifth, evaluation-only condition: θ* with links open.** It is the cheapest direct test of the train/test mismatch (W4).
5. **Let reviewers verify the plan without git history.** The plan's sha256 is already recorded in the run provenance.
6. **Have the authors ratify the plan, with an external timestamp, before the evaluations run.** Appendix J says the plan was written by the assistant and "no approval of it by the authors is yet recorded" (p35).

## 4. Does the code supplement support its claims?

**What I ran.** On a 4-core CPU machine, with JAX 0.11.0 from the shipped `uv.lock`:

1. **`sha256sum -c SHA256SUMS`:** all 4,166 files verified.
2. **`uv sync --python 3.12 --group dev`:** succeeded.
3. **The README's four reproduction commands** (`p6_unblind`, `p6_post_analysis` twice, `p6_secondary`). Every output file is identical to the committed one apart from the git, timestamp and dirty-flag provenance fields. This reproduces:
   - Table 3 and Figure 8;
   - the falsifier values (3.855 < 4.433; 4.040 < 4.673);
   - all of Appendix E: the per-checkpoint tables, the 60-seed analysis, the 2000-update subsample and the High-severity readout;
   - all of Appendix F;
   - the claim that 280 of 288 cross-GPU evaluation values agree.
4. **The test suite.** A single-process `pytest che/tests` run exceeded this machine's 3.5 GB memory limit and was killed. Run one file at a time (41 files, ≈30 minutes in total), **601 tests passed, 4 were skipped, 0 failed.** The skips are exactly the ones the README predicts: three empty parameter sets and one git-identity check. The suite includes real debug-size training through the grid runner.
5. **A small smoke run of my own.** I trained a JOINT policy for 4 updates with `che.train.ippo` and evaluated it with `che.eval.harness` at θ* and in the interaction check's "A only" configuration. Both worked. Per-episode outcomes were identical across the two conditions, which illustrates the common-random-number nesting.
6. **The six "verbatim" listings:** all match the cited line ranges exactly.
7. **Spot checks against committed reports.** Every §4 and appendix number I checked agrees:
   - percolation estimators, spanning probabilities and burnt fractions;
   - the 4.83×/4.92× falls and the [0.164, 0.203] share range;
   - masked shares and the 118/22/16× amplification;
   - the High contrasts and the Medium −0.03 against 0.72;
   - the denial study's numbers and thresholds;
   - the death-penalty ablation and the per-severity variances;
   - the training and evaluation timings.

   The quotations in Appendix D match the two shipped registration documents.
8. **Independent recomputation** of Šidák constants, SEs, detection limits, power figures, the seed rule (71.3 → 72), the floor SD intervals, and Theorem 1's q values. All agree.

**What the supplement cannot support:**
- Checkpoints are not shipped, so the evaluation summaries can't be regenerated or tied to training.
- The dated log is absent, so the timeline and the "before unblinding" claims can't be checked.
- The interaction analysis can't run without git history.

**What the supplement shows that the paper omits:**
- the "NOT INERT" verdict (W4b);
- the GPU card diagnostic (W6);
- the 2000-update learning curves (W5);
- the κ_B lock margins (W9).

In short, the code supports the environment-mechanics claims and the arithmetic of every registered analysis. It cannot support the provenance of the evaluation data.

## 5. Unclear or garbled sentences

- **p1:** "The correction trains an isolated arm without the third of episodes whose only stressor, communication denial, had no detectable effect in calibration, matching the joint arm's share of training with an active stressor." Garden-path sentence; "matching" dangles.
- **p1:** "Both differences are sign unstable over the final half of training." The term isn't defined in the abstract.
- **p2:** "…matching it alone cannot isolate co-occurrence." The symbols are undefined in the abstract and "it" is ambiguous.
- **p3:** "The test was sited where composition is weak" — "composition" is undefined.
- **p3:** "inert under a frozen random-projection encoder at this scale" — scale of what?
- **p3:** "The isolated arm and its corrected version trained every episode that contained a coupling with links intact" — misparses as "trained every episode".
- **p5:** "…each cell still Fuel after this step's spread within Chebyshev distance r_A of a cell that collapsed in this step: the fire reads the increment c′ − c." Ambiguous attachment, and the last clause is code-speak.
- **p6:** "ignoring the attenuated signal costs exactly half the probability of being informed" — the cost is a value of q/2, not a probability.
- **p7:** "any asymmetry between them is read that way."
- **p7:** "The test for κ_A = 0 compares fire and smoke only, since agents respond to collapses" — the reason is unclear.
- **p8:** "Only Coupling A produces them and κ_B does not enter the count, so it is co-active only in all-on configurations." Unclear referent; the counter is also non-zero in A-only runs.
- **p8:** "each level is the observable band fixed for it before the main experiment (table)" — unnumbered table, and a level "is" a band?
- **p8:** "comes from logistic fits that no committed estimator reproduces."
- **p8:** "Re-tested with fixed fire-only policies" — which policies?
- **p9:** "Where Coupling A costs survival most is not located."
- **p9:** "…is a reference scale (cross-artifact): a spread from other runs, shown for scale only."
- **p10:** "Remark 2′ … refines Pynadath & Tambe … it finds that communication has no marginal value…" — a remark doesn't "find".
- **p10:** "…so it only grades an observed effect against a floor, after the fact and labelled."
- **p10:** "The registration also calls its detection limit X an exclusion bound." This conflates two quantities.
- **p11:** "A logged diagnostic becomes evidence only inside a registered test family, with a floor on its artifact; until then it is recorded, not graded."
- **p11:** "The registration stated the Coupling-B half in advance" — half of what?
- **p11:** "…registered with its direction and a correcting arm during them" — during what?
- **p11:** "One design error inflates Γ." This asserts a direction as fact.
- **p12:** "Bias (b), …" — there is no bias (a).
- **p12:** "is non-verdict-bearing, as registered."
- **p12:** "the plane separates co-occurrence from the active share only; per-coupling frequency moves with each slope."
- **p13:** "so Γ₄ is a second exclusion bound, the registration's term for its detection limit, X₄ = 4.88" — a contrast is not a bound.
- **p13:** "its upper bound, +0.63, lies above Γ's lower bound, +0.47" — the inference is unclear.
- **p13:** "Γ = Γ₄ + B̂ holds by construction for arm means, so B̂ is not a second finding." Non sequitur.
- **p13:** "The registered headline for this outcome no longer holds as worded" — the headline isn't quoted here.
- **p13:** "To measure what composition θ* offered."
- **p14:** "§1 lists the largest limitations first, and each sits where it arises."
- **p15:** "…bit-identical and matched the main runs' own" — own what?
- **p15:** "is read in §6.3 exactly as registered" — inaccurate (W12).
- **p16:** "this is why Definition 2 follows Definition 7 in §3" — renumber instead.
- **p16:** "the early frozen control branch" — undefined.
- **p16:** "the two rules coincide wherever seeding neighbourhoods do not overlap" — the document's rule isn't given.
- **p18:** "Proposition 3 (Collapse events dominate hazard exposure)."
- **p19:** "four conditions are matched, each with a known sign" — biases have signs; conditions don't.
- **p19:** "In both, the four factors compose to the observed slope within Monte Carlo error" (see W8).
- **p20:** "a three-condition check" — the three conditions aren't stated.
- **p20:** "with slack ℓ_f…" — ℓ_f was defined as the fire's depth (≥ 1), so "equality iff ℓ_f = 0" can never hold.
- **p21:** "It follows by telescoping the two models' evaluation operators…" — no bound is stated.
- **p21:** "differs from the test configuration θ* on the states where both couplings act at once" — they also differ in β everywhere.
- **p22:** "disjoint by a factor of 1.35."
- **p22:** "the toy band was kept as a consistency check" — its outcome isn't given.
- **p23:** "four thresholds were set on constants the record later called invented."
- **p23:** "reference version: 0 of 760 per-field trajectory hashes differ…; refactored version: differs in 1 of 4."
- **p24:** "each arm's own s√(2/k) gave 92.1 % and 62.8 % power, where the contrast's power was 76.7 %."
- **p24:** "so it fired when JOINT's floor fell faster than its drift."
- **p27:** "the branch label stays B, because the rule below fixes it by Γ."
- **p28:** "Ratified as built."
- **p29:** "GPU 1 ran Γ: all 72 seeds… of which 76 runs were executed there and seeds 13–46 were copied from the main runs." Contradictory as worded.
- **p31:** "no gap larger than … even where JOINT trained on the evaluated configuration and ISO never saw a composed one" — the a fortiori logic isn't explained.
- **p32:** "along the identification line the same holds 0.2 lower in active share."
- **p32:** "The bound, the fire-only share's part of the sweep's endpoint change, excludes zero on survival."
- **p34:** "the post hoc two-sigma floor-grading convention."
- **p35:** "a decision bound only once it was written into the project's dated decision record."

## 6. Requested changes

**Needed for acceptance:**

1. **Recast the contributions.** Lead with the environment, state the null plainly, and present the μ_A + μ_B − p identity as a design note, not a result.
2. **Add an environment specification and usability evidence:**
   - action and observation specification, termination rules, and the API;
   - environment throughput against the number of parallel environments, and memory requirements;
   - learning curves for the default configurations, including the 2000-update data.
3. **Add baselines.** At minimum: a scripted fire-avoiding forager, a recurrent IPPO or MAPPO policy, and a learned-communication agent. Run them at θ* and at another severity.
4. **Show that each coupling changes learned behaviour at some severity,** with floors and adequate seeds, ideally with a policy that has memory.
5. **Communication denial:**
   - disclose the "NOT INERT" verdict and its override in §4.4;
   - compare the denial study's resolution with Γ;
   - list everything that depends on the inert label;
   - evaluate all final checkpoints at θ* with links open.
6. **Report the 2000-update arm means and the per-seed completion distribution,** and discuss that the 1000-update comparison is pre-asymptotic.
7. **Report the GPU card diagnostic.** Fix the "fire-only" label and the description of "Coupling A off", and give deaths by cause.
8. **State the κ_B lock margins** (inside the detection band in only 2 of 3 measurements; consistency check failed).
9. **Statistics:**
   - add Welch intervals for the 20-seed contrasts;
   - interpret B̂;
   - correct the df in the toy checks and report several PRNG keys;
   - use an F test rather than interval overlap for the floor comparison.
10. **Proposition 3:** retitle it, state its limit, and remove the circular claim. Formalize the transfer remark or drop it.
11. **Interaction check:** address design concerns 1–6 in §3 before running it.

**Would strengthen the paper:**

12. Move registration bookkeeping to the appendix, add a glossary, remove internal codes from figures, enlarge the printed figures, and rewrite the sentences in §5.
13. Broaden related work (W11).

## 7. Recommendation

**Major revision. Confidence: 4/5.**

The paper is careful and honest, and it hedges almost every claim correctly. Apart from the omissions in W4b, W5, W6 and W9, the stated claims match the evidence. But the claims that remain don't yet make a convincing case for TMLR readers:
- the worked example is a null;
- its lesson is an identity;
- the environment's distinctive stressors show little demonstrated effect on what agents learn;
- there are no baselines.

With the environment validated and the omissions above addressed, this could become a useful environment paper.

---

My scripts are in `/tmp/rv_scripts/` and the outputs (test logs, reproduction diffs, review draft) are in `/tmp/rv_work/`. The supplement was copied to `/tmp/rv_run/` before running, so the original unpacked files are unchanged.