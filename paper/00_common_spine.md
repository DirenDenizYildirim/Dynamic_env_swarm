# Common spine — the Γ-independent paper

Target: TMLR. No page limit; length must be justified by content. Two
acceptance criteria only: (i) claims supported by evidence, (ii) some of the
audience would be interested. Write every section to criterion (i) and let
the tier-1 findings carry (ii).

**Branch B landed (2026-09-26) and is spliced in (2026-09-27).** Sections
marked **[Γ]** now carry its content, taken from `paper/branch_B.md`. The
spine is the source that `submission.md` is ported from. `branch_B.md`
stays as the record of the branch text, its per-number sources, the
reviewer-objection table (§7) and the do-not-claim list (§8). Where either
file differs from the registered text, the registered text governs
(`phase6_framing_branches.md` §3–§4b; decision log *UNBLIND RESULT*,
*SECONDARY RESULT*, *POST-UNBLIND STAGE RESULT*).

**Every number here has a row in `paper/numbers_ledger.md`** (built
2026-09-27) naming its committed source. A number enters `submission.md`
only with its row ID.

**Terminology, fixed by D1:** the fire burns in every training episode.
The composable **elements** are Coupling A, Coupling B and δ. An episode
with "no element" is a **fire-only** episode, not a hazard-free one.

---

## Title candidates (branch B)

- *Paid in agents, not in composition: a pre-registered test of joint vs
  isolated training under ambient hazards*
- *What joint training buys under ambient hazards is exposure, and it is
  paid in agents*
- *Compound Hostility: a calibrated environment and a pre-registered test
  that finds exposure, not composition*

Pre-unblind, branch-neutral candidates, kept as fallbacks:
*Compound Hostility: a calibrated multi-agent RL environment where the
hazard makes its own danger*; *CHE: measuring what a multi-agent team learns
when the environment is the adversary and the reward does not say so*.
Drop any candidate that says "compound hazards cost survival", because the
evidence attributes the effect to exposure share. Keep "swarm" out of the
title: the foraging task requires no coordination (see Limitations).
"Multi-agent" is safe.

## Abstract — branch B

> We introduce the Compound Hostile Environment (CHE), a pure-JAX
> multi-agent RL environment in which a cellular-automaton fire is causally
> coupled to structural collapse (collapse seeds fire) and to perception
> (smoke attenuates observation by Beer–Lambert transmittance), with an
> independent communication-denial axis. The hazard is an *ambient survival
> stressor*: it enters neither the reward nor any cost or constraint channel;
> the reward sees only task variables and agent deaths, which it prices the
> same whatever their cause. Three properties make CHE an
> instrument rather than a demo: severity is defined by a *measured*
> percolation critical point (β̂_c = 0.500 ± 0.005, reproducing Kesten's
> exact value), every stressor is a parameter of one kernel so that
> ablations are *bitwise exact* nested models, and every acceptance bar in
> the paper is graded against a measured reproducibility floor. Calibration
> yields four findings independent of any training comparison: collapse-
> seeded fire self-limits where the hazard is worst; compound hostility is
> rare and bursty; perception decay cannot be behaviourally suppressed; and
> inter-agent communication is inert under a frozen random-projection
> message encoder at this scale. We then run a pre-registered, mechanically
> blinded test of compositional generalization: whether training on
> co-occurring stressors beats training on the same stressors in isolation,
> at a held-out severity and matched compute (k = 72 seeds per arm; the
> registered k = 60 prefix reads the same). At matched compute, joint
> training improves survival at the held-out severity by 0.96 points
> (family-wise 95 % CI [0.47, 1.44], Šidák-corrected for the two
> co-primaries), while task completion shows no gain larger than 0.66 points
> at the same level: the asymmetry the registered falsifier requires. **The
> survival advantage does not survive the pre-registered inert-share
> correction.** An isolated-training arm without its fire-only episodes
> matches joint training (difference −0.03 points, replicated on the same
> hardware), and a secondary dose design attributes the gap to fire-only
> training episodes rather than to composition. The contrast's sign is not
> stable over the final half of training: the survival gap opens only in the
> last fifth of the budget and is still growing at the matched budget. All
> code, configs, locks and the frozen analysis plan are released.

Keep the inert-share qualifier in the abstract on every revision; it is
registered (*UNBLIND RESULT*). "Fire-only" replaces `branch_B.md`'s
"hazard-free". Under D1 the fire burns in the δ-only components
(`p6_iso.yaml`: β 0.43 / 0.70), so those episodes are free of *elements*,
not of hazard. "Co-occurring" replaces "co-active" here so the word does
not collide with the invariant-#5 counter (§6).

## Contribution list — order for the intro

1. **The environment as an instrument.** Def. 2 reward independence,
   Prop. 1 kernel factorization, bitwise nested ablations, severity by
   measured phase. (Tier 1, items 1–3.)
2. **Four calibration findings** that stand without Γ. (Tier 1, items 4–8.)
3. **A measurement methodology** for empirical RL: per-metric, per-hardware,
   per-artifact floors; contrasts graded on the contrast's SE; 80 %-power
   MDEs at family-corrected α; "measuring is not grading".
4. **A pre-registered compositional-generalization test** with mechanical
   blinding, and its result. **[Γ]** Joint training's survival advantage is
   exposure, not composition. It was caught by an inert-share correction
   that was registered (2026-09-18) and run (ISO-4) before the look. The
   discussion's methods lesson follows from it: match active share before
   claiming composition.

Do not promote 4 above 1–3 on any branch. TMLR does not reward it and the
evidence does not support it.

---

## §1 Introduction

- Open on the reframe: most hazard environments put the hazard *in the
  reward* (monitoring, suppression, coverage) or *in a constraint* (CMDP,
  safe RL). CHE puts it in the **transition and observation kernels only**.
  From a single agent's view the hazard looks like nonstationarity; Prop. 1
  says it is state under a stationary kernel, so every standard MARL tool
  applies unmodified.
- The compound question: stressors that co-occur interact causally
  (collapse → fire → smoke → blindness). Does a policy need to *see* them
  co-occur to survive their co-occurrence? State it as a question with a
  priority holder (Gao et al., RSS 2024 — compositional generalization over
  environmental factors). Our contribution is the design: **matched-marginal
  composition variation under causally coupled stressors** (ENDPOINT
  CONFOUND entry, 2026-09-22). Lead with that, not with "joint vs
  isolated", which is a crowded claim-space. The DBCA split (Keysers et al.
  2020) fixes the atom distribution and varies compound divergence, and
  **that describes the secondary sweep** (per-element marginals held at 0.5
  while co-occurrence moves 0 → 0.5), **not the ISO/JOINT endpoints**, whose
  per-element frequencies differ 3×. Name DBCA where the sweep is
  introduced (§9), and state the endpoint confound there.
- The answer, in one line: at matched active share, training on the
  couplings together adds nothing detectable to survival. This is an
  exclusion, not an absence: Γ₄'s Šidák upper bound is +0.63 points. The
  confirmatory
  gain comes from the isolated arm's fire-only episodes, which a correction
  registered before the look was built to catch (§9).
- Why an instrument first: three of the four registered outcomes of the
  compositional test are not the founding hypothesis, and the paper was
  designed so that a paper exists on every branch. Say this plainly. It is
  what makes the pre-registration credible. **Branch A (the founding
  hypothesis) did not occur. Say that flatly.**
- One paragraph on what the paper does *not* claim (theory §9): no
  convergence guarantees, no theorem that joint training wins, no exact
  critical value for the implemented kernel.

## §2 Related work

Four claim-spaces the no-scoop checks (2026-08-13) found empty; lead with
them, then the neighbours.

| space | nearest neighbour | separation |
|---|---|---|
| severity by measured critical point | wildfire simulators (JaxWildfire arXiv:2512.06102 `[READ THE PDF]`) | they parameterize; we calibrate to a measured phase |
| hazard generates hazard | none found | Coupling A |
| Beer–Lambert on a POMDP observation kernel | none found | Coupling B |
| JAX × MARL × hazard survival under a hazard-independent reward | JaxMARL, Multi-Agent Craftax, Assistax (JAX MARL); POBAX (JAX, **single-agent**); BenchMARL (MARL, **TorchRL, not JAX**) | none carry an evolving lethal field |

Neighbours and how they are positioned (rulings 2026-08-05):

- **Hazard in the reward**: Haksar & Schwager 2018 (distributed MADQN under
  fire spread). Def. 2 clause 1 separates us.
- **Hazard in the reward or a cost channel**: JaxWildfire (arXiv:2512.06102;
  reward penalizes burning cells) is the foil across the Def. 2 boundary;
  safe-RL / CMDP generally.
- **Fire / smoke multi-agent domain neighbour**: VULCAN (Liu & Yan,
  arXiv:2604.12831, INFOCOM EIN Workshop 2026) — VLM-based cooperative
  navigation in indoor fire with smoke; not RL, not a CMDP.
- **Compositional generalization**: Gao et al., RSS 2024 (arXiv:2403.05110)
  as the priority holder on the question — it matches data-collection
  *effort*, not active share; Keysers et al. 2020 (DBCA) for the split
  methodology. `[OWNER READS Gao 2024]`
- **Joint vs isolated training** (multi-task RL, domain randomization,
  curricula) is routine, and it almost always confounds "saw more" with
  "saw it combined". State the endpoint confound here (ENDPOINT CONFOUND
  entry, branch-invariant). JOINT sees each coupling 3× as often as ISO as
  well as seeing them co-occur. The separation from that literature is the
  matched-marginal sweep plus the ISO-4 active-share control. Branch B is
  the exhibit: the one uncontrolled quantity, active share, accounts for
  the whole effect.
- **Simultaneous / mixed perturbations**: Agrawal et al. 2023
  (arXiv:2310.08746; multiple concurrent environmental uncertainties in MARL,
  curriculum) and Erdem & Üre 2025 (MAKE 7(4):108; mixed state+action
  adversarial attacks — reported direction opposite to ours; `[OWNER READS:
  does it match exposure?]`). Neighbours, not priority holders.
- **DR theory**: Chen et al., ICLR 2022 (arXiv:2110.03239). `[OWNER READS
  before claiming Theorem 1 is unsubsumed]`
- **arXiv:2604.26150**: single-agent; reward is negative operating cost — no
  burning-cell penalty, no CA fire (verification 2026-09-26). Cite as a
  contrast only if still relevant after reading. `[READ THE PDF]`
- **UED / domain randomization**: search run 2026-09-26; a DRAFT paragraph
  and verified entries are in `paper/related_work_verification.md`
  (Part 2). Previously: **this paragraph is owed and no search
  had been run.** PLR, ACCEL, PAIRED, and the DR literature ask joint-vs-
  isolated training-distribution questions routinely. Write this paragraph
  after a real search; a TMLR reviewer will ask.
- **Communication value**: Pynadath & Tambe 2002 (COM-MTDP: observability
  gates communication value) is cited first; Remark 2′ refines it with the
  collective-redundancy conjunct. Cite, then refine, in that order.
- **Multiple stressors / compound events**: ecology and climate literatures
  as supportive analogies for the word "compound", one sentence.
- ~~SMART (RA-L 2026)~~: **REMOVED** — no record found (2026-09-26).
- **arXiv:2507.10142**: owner reads before submission; the one place a
  subsuming memorization-gap theorem could hide.

## §3 The environment

Follow `docs/theory_foundations.md` §1–§6, compressed. TMLR has no page
limit, so full statements can stay in the main text; proofs of Prop. 1,
Prop. 2's coupling, and a compact Thm. 1 inline; Prop. 3–4 as statements
with sketches and full proofs in the appendix.

- **Def. 1** factored Dec-POMDP; **Prop. 1** the step order
  collapse → hazard → smoke → agents → comms, observations from the
  post-step state. State it as the hypothesis of the theorems, which it is.
- **Def. 2** ambient survival stressor, **as reworded 2026-09-27** (DEF. 2
  WORDING RULING; `docs/theory_foundations.md` Def. 2 is the text): R is a
  function of task variables and the alive transition only; no term reads
  h, ρ or c; no cost/constraint channel. Survival is learned through two
  hazard-blind routes, truncated task return and a fixed d_p = 0.5 per
  death whatever its cause. Include the **hazard-blind vs hazard-priced**
  note (JaxWildfire prices burning cells; we price outcomes; the
  cause-blindness test) and the Phase-2 d_p ablation **with its scope**
  (pillar-only, 500 updates, 3 seeds): High survival 0.575 → 0.866 and
  completion 0.765 → 0.821; Medium survival 0.931 → 0.951 at unchanged
  completion; Low tied.
- **Def. 3 / Prop. 2 / Cor. 1** fire CA and its exact bond-percolation
  equivalence for the idealized kernel. Burn time is exactly one step;
  single ignition at reset; say so.
- **Def. 4** severity by dynamical phase; the calibration protocol.
- **Def. 5** Coupling A, **Prop. 3** linear scaling with the four-factor
  protocol correction.
- **Def. 6** Coupling B, Beer–Lambert on the egocentric crop; **Thm. 1**
  memorization gap and its erosion.
- **Def. 7** comms denial; **Remark 2′** VoC.
- **Def. 8** ISO / JOINT / Γ.
- **Nested-model semantics** (theory §8): the table of five elements, each
  a parameter of one kernel, each recovering a nested model bitwise. Frame
  as *"ablations are exact by construction"*.
- Concrete instance: 64 × 64 grid, 12 agents, horizon 256, 9 × 9 egocentric
  crop with 7 indicator planes plus smoke, own-state vector with absolute
  position, alive flag and time, 5 actions, foraging task with 32 items and
  +1 team reward per collected item. Shared-parameter actor-critic
  (Conv 16 → Conv 32 → Dense 128 → actor and critic heads, each with a
  64-unit hidden layer; a stop-gradient message head), **trained by IPPO,
  one policy per training seed.** Every reported run used single-policy
  IPPO. The PBT population loop exists in the code and was exercised only
  by the throughput benchmark, so it must not be described as the training
  method (`paper/numbers_ledger.md` ENV-11, O-1).

## §4 Severity calibration

- β̂_c = 0.500 ± 0.005 from the R_L logistic-centre family at
  L ∈ {32, 48, 64}, 512 seeds; self-duality R(β_c) ≈ 1/2 at all three sizes.
  Present the Kesten reproduction as **validation of the method**, not as
  a result. **Provenance owed (ledger O-2):** the R_L logistic centres
  exist only in `severity_lock.md`. The committed estimator outputs use
  other estimators (crossing mean 0.504, consensus 0.499).
- Locked levels and what they mean:

  | level | β | P_span | burnt fraction |
  |---|---|---|---|
  | Low | 0.43 | 0.021 | 1.9 % |
  | Medium | 0.49 | 0.547 | 19.8 % |
  | High | 0.70 | 0.998 | 98.3 % |

- Medium sits between the finite-size pseudo-critical point β_c(64) ≈ 0.486
  and β̂_c; it is the held-out severity for the compositional test.
- Def. 4's variance-peaks-at-Medium prediction was **refuted for
  survival** (M3.0, `def4_variance.md`: fixed-policy variance monotone,
  highest at High). For completion it is inconclusive: Medium is nominally
  highest but within CI of Low. The environment-level mechanism was
  confirmed. Report all three; do not generalize the refutation beyond
  survival.

## §5 Coupling A — hazard begets hazard

- Lock: f_weak 0.15, λ₀ 5·10⁻⁵, λ_load 4·10⁻⁴, κ_A 0.06, r_A 1.
- Prop. 3 handshake, **two runs, report them as two**: linearity R² = 0.998
  over a 14× range of E[N_seeds] (L = 64 dense sweep), and matched-reference
  ratio 0.992 ∈ [0.90, 1.02] with R² 0.9995 (v2 purified test, L = 32).
  Both are handshake regimes (κ_A 0.02 and 0.003), not the locked
  parameters.
- **Finding: the ignition channel self-limits where the hazard is worst.**
  Seeded ignitions per episode 4.05 / 3.41 / 0.84 across Low / Medium /
  High, a 4.83× fall, by fuel exhaustion (the Phase-4 grid, κ_B = 1.0 arm).
  Replicated on m35, the Coupling-A grid: 4.08 / 3.42 / 0.83, 4.92×.
- **Finding: the near-agent share is flat** across severity, [0.164, 0.203];
  the whole severity response is upstream of the agents.
- Low leaves the survival ceiling (0.979 → 0.961). No weak-cell avoidance
  detected.

## §6 Coupling B — hazard degrades perception

- Lock κ_B = 1.0 on the detection band alone; the three lock bands did not
  intersect (masked-frac band unreachable at Medium for any κ_B; E2C band disjoint from
  detection band by 1.35× under the random policy, 1.15× under the probe
  policies). Say this; it is honest and it is interesting.
- Thm. 1 E2C gate green: max |z| 2.11, χ² p = 0.586 against the closed-form
  1/2 + q/2.
- **Finding: perception decay is paid in survival, not completion.** High:
  the survival effect replicates in direction 3/3, range −0.047 to −0.107,
  pooled 1.41× the measured floor (sd 0.062) (Phase-4 correction,
  2026-07-30). Lead with that; the first 2-seed estimate, −8.8 points, is
  quoted only beside it. The completion effect flipped sign on a same-seed
  retrain and is **unresolved**. Medium: −0.0003, within noise, graded
  against a 3-seed σ_seed of 0.0072, not a measured floor; the later Medium
  survival floor is 0.0129. **This Medium number is load-bearing for the
  Limitations section on every branch.**
- **Finding: masking concentrates 16–118× on danger moments.** The coupling
  cannot be behaviourally suppressed.
- Co-active visitation (Prop. 4 diagnostic): 0.64 events/episode at Medium,
  P(zero) = 0.563 / 0.578 / 0.883, var/mean 1.31–1.40. **Rare and bursty.**
  Always show the distribution, never the mean alone.
- **Scope of "co-active", required wherever the counter is used.** These
  figures are the κ_B = 1.0 rows of `phase4_report.md` Result 4, with
  var/mean from the same cells in E1.1 (`e1/e11_report.md:208-210`):
  single-configuration runs with both couplings on, **not training
  mixtures**, so "rare and bursty" stands as measured. The counter (inv.
  #5, `che/env/env.py:398-404`) counts collapse-seeded ignitions inside an
  alive agent's 9 × 9 perception crop. Only Coupling A produces those, and
  κ_B does not enter the count:
  the same table's κ_B = 0 rows show no cross-arm difference at any
  severity. So the counter is co-active only in configurations where B is
  also on. In mixed training it reads the A marginal alone, which is why
  the Phase-6 mediation analysis is VOID (§9; *SECONDARY RESULT*).

## §7 The comms axis — inert under this encoder at this scale, by a joint argument

- Remark 2′ handshake: VoC monotone 0 → 0.498.
- M5.3 Medium: utility bound < ~3 points (2 seeds). M5.3b High: out-degree
  1.01 → 2.99 changes nothing; eliminates connectivity as the cause. M5.5:
  δ = 1 vs 0 within measured floors on both metrics; condition (iii) VOID
  because its threshold sat below its floor (state this, it is a
  methodology exhibit).
- **Honesty lines, required:** the message head receives no gradient; the
  encoder is a frozen random projection; gradient-shaped messaging is
  untested. Foreground the demand-side argument (the unused connectivity bit
  needs no encoder, so its neglect cannot be blamed on the projection).
  Write "inert under this encoder at this scale", not "certified inert".
- Consequence for §8: the effective composition under test is A × B; δ is
  carried for registration fidelity.

## §8 Methodology — bars come with floors

This is a methods contribution and should be written as one.

- **Floors are per-metric, per-hardware, per-artifact.** Exhibits:
  Medium completion floor 0.0145 on one card vs 0.0399 on another while
  survival stayed 0.0129 / 0.0130 (the code tree also differed between the
  two runs, so say "card and tree", not "card"); the traced tree differing
  from itself
  1 time in 4 on two channels (M6.0), which a reference-measured floor of
  zero had read as a real difference.
- **Contrasts are graded on the contrast's SE**, sd(Γ) = √((σ_A² + σ_B²)/k),
  never on either arm's own dispersion. Exhibit: the per-arm reads bracket
  the truth at 92.1 % and 62.8 % where Γ's power was 76.7 %.
- **Design-stage power is the 80 %-power MDE at the family-corrected α.**
  Exhibit: k = 20 on a bare 2σ figure had 55.6 % power against its own
  motivating effect band; caught at registration.
- **Measuring is not grading.** A channel becomes evidence only with a
  registered family and a floor. Exhibit: the render-gate drift channels
  are recorded by the grid and grade nothing.
- **Differenced tests are blind to arm-symmetric effects.** Exhibit: the
  wall-drift artifact present in every episode of both arms, invisible to
  a "no cross-arm difference" falsifier for three phases.
- **Detectability-relative gates diverge on improving hardware** (tier 2):
  a plateau criterion with a floor in its denominator cannot certify on a
  perfect instrument; retired and replaced by an explicit fixed-budget
  estimand.
- **Reproducibility floors grow with run length** (tier 2): the completion
  floor grew 2.1× for ISO and 5.2× for JOINT from T = 500 → 1000, so a
  floor measured at one budget does not grade runs at another. That the
  growth is *ordered by curriculum difficulty* is a hypothesis, labelled
  untested at its source (n = 2 arms), and the two budgets' floors ran on
  different boxes. Offer it as a hypothesis or not at all.

## §9 The compositional test — design, and the branch-B result **[Γ]**

### §9.1 Design (Γ-independent)

- ISO: 6-component uniform mixture {A-only, B-only, δ-only} × {Low, High}.
  JOINT: {all-on} × {Low, High}. θ\* = all-on at **held-out** β = 0.49.
  Same architecture, same compute, same eval set. **ISO-4** (sensitivity
  arm, outside the family, k = 20; §7 PROPOSALS RULING, 2026-09-18): ISO
  with the two δ-only components removed, i.e. {A-only, B-only} ×
  {Low, High} at 0.25 each, and nothing else changed.
- Estimand: Γ = J_θ\*(JOINT) − J_θ\*(ISO) at **matched budget T\* = 1000
  updates**. Co-primaries completion and survival, Šidák m = 2
  (z_α = 2.2365), **k = 72 per arm (primary)** with the registered-ladder
  prefix **k = 60** reported beside it, unpaired contrast SE from the
  grid's own seed dispersion. Secondary: dose sweep c = 0.5 at five p points
  and identification c = 0.4 at three, k = 20, labelled non-verdict-bearing.
- **How k reached 72, stated as a deviation.** Registered k = 40. The seed
  ladder raised it to 46 on the re-floor run 2026-09-08 (logged 2026-09-09).
  The grid card changed
  to an RTX 5090 (CARD RULING, 2026-09-21), and that card's re-floor
  returned k_req 72 for completion against the registered cap of 60. The cap
  was **raised to 72 on 2026-09-22, pre-unblind, with no outcome seen**
  (LADDER BRANCH C). This is recorded as a deviation from a registered
  rule. It is conservative: added seeds raise power symmetrically and
  cannot move Γ's sign. Seeds 1–60 are a prefix of 1–72, so the registered
  k = 60 analysis is reported in full. It reads the same (table below).
- Design-stage power from the launch batch (PRO 6000): sd(Γ) 0.00504 /
  0.00310, MDE80 0.0155 / 0.0095, k_req 11 / 5. On the grid card's
  re-floor, completion power at the 0.03 target effect was 72.2 % at k = 60
  and 80.4 % at k = 72. Label both as an **upper bound on power**, since
  floors are a lower bound on seed dispersion. **Realized** completion power
  at 0.03, from the grid's own dispersion, is 71.6 % at k = 72 and 60.2 % at
  k = 60. Report it, never re-engineer it.
- **The endpoint confound and the matched instrument** (ENDPOINT CONFOUND
  entry, branch-invariant). Γ confounds dose with composition: JOINT sees
  each coupling 3× as often as ISO. The **sweep** holds the per-element
  marginals at exactly 0.5 while co-occurrence moves 0 → 0.5. That is the
  DBCA split (fixed atom distribution, varied compound divergence), and it
  is the place to name DBCA. It cannot be perfectly clean: the simplex
  forces the fire-only share up with p (n = p on the c = 0.5 sweep). The
  c = 0.4 identification arms sit on a parallel line offset by 0.2 in
  fire-only share, and that offset identifies the plane (correction S3).
  State this before a reviewer finds it.
- **Blinding, described in-text without links:** the report script
  suppresses cross-arm means; the grid runner computes no cross-arm quantity
  and a test asserts it; the four outcome branches and their framings were
  registered on 2026-08-13; the venue was ruled 2026-08-24; all pre-grid.
  Quote dates, not hashes that resolve to an account.
- **Budget robustness:** Γ(t) over 11 checkpoints (updates 500–1000) on
  the confirmatory arms, read for sign stability over the final half.
  "Sign unstable" is a finding and is reported as one.
- **Registered biases, stated before the result:**
  (a) **The inert-share bias** (§7 PROPOSALS RULING, proposal 0,
  2026-09-18; branch-invariant). 2/6 of ISO's training episodes are δ-only,
  and δ is inert (§7), so they carry no behaviourally active element.
  Under the project's own certification, ISO effectively trains on
  {A 1/3, B 1/3, fire only 1/3}, while every JOINT episode carries both
  live couplings. **Direction: the bias inflates Γ.** The config's nominal
  "no-element 0.0000" is true nominally and false behaviourally. The design
  defended the *marginal* imbalance, and the symmetry defence covers test
  time only. ISO-4 is the arm that removes the bias. **Its reading rule was
  registered, and ISO-4 was trained, before the look.** If Γ rejects and
  Γ₄'s CI contains 0, the effect does not survive the correction, and the
  text may not call it a composition effect.
  (b) **Differential drift at T\*.** Registered from the launch batch (RTX
  PRO 6000, 2026-08-10): over the last 100 updates, ISO drifted 0.56× its
  completion floor and JOINT 1.02×, a JOINT − ISO differential of +0.012
  per 100 updates, stated as a local sensitivity estimate, never a bound.
  **It did not hold in sign on the grid card.** The 5090 re-floor reads
  ISO 0.33× and JOINT 0.19×, a differential of −0.008; the second PRO 6000
  re-floor reads +0.018. On the grid card's model, the T = 2000
  subsample's training-surface slope over updates 500–1000 is +0.0025
  (completion) and +0.0072 (survival) per 100 updates. Report all four and
  claim no direction (ledger DES-10, DES-11).

### §9.2 Results — branch B, with the inert-share qualifier **[Γ]**

Every number below is quoted from its committed source (listed at the end
of `branch_B.md`). The registered reading comes first in every item.

| contrast (θ\*, matched budget T = 1000) | completion | survival |
|---|---|---|
| **Γ = JOINT − ISO**, k = 72 / 72 (primary) | −0.0173, z −1.62, **null**; Šidák CI [−0.0412, +0.0066] | **+0.0096, z +4.43, REJECT**; Šidák CI [+0.0047, +0.0144] |
| registered-ladder prefix, k = 60 | −0.0217, z −1.80, null | +0.0104, z +4.67, REJECT |
| **Γ₄ = JOINT − ISO-4**, k = 72 / 20 | −0.0126, null; X₄ = 0.0488 | **−0.0003, z −0.09, null**; Šidák CI [−0.0068, +0.0063] |
| **Γ₄′ = JOINT − sweep_c50_p000**, same card, k = 72 / 20 | −0.0247, null | **+0.0013, z +0.41, null**; Šidák CI [−0.0056, +0.0081] |
| **B̂ = ISO-4 − ISO** | −0.0046, null | **+0.0098, z +3.39**; Šidák CI [+0.0033, +0.0163] |
| fire deaths per episode, JOINT − ISO (secondary) | | −0.1177, z −4.59 |
| **Γ_H** at High, β = 0.70 (out of family) | −0.0079, null; X = 0.0340 | +0.0038, null; X = 0.0254 |
| **Γ(t)** signs, t = 500…1000 | `+ − + + − − − − − − −` → **UNSTABLE** | `+ − − + + + + + + + +` → **UNSTABLE** |

1. **The confirmatory contrast**, rows 1–2: k = 72 primary, with the k = 60
   prefix beside it (UNDERPOWERED-flagged). Arm means: completion ISO
   0.7772, JOINT 0.7600; survival ISO 0.9158, JOINT 0.9254. Intervals are
   conditional on the one 512-episode eval draw (§10 item 7).
2. **The falsifier, shown with its margin:** |z_c| + z_α = 3.855 < 4.433 =
   |z_s| (k = 60: 4.040 < 4.673). Branch B stands; it is not C. Report the
   completion null as an **exclusion**: JOINT gains at most 0.66 points
   (Šidák upper bound +0.0066). The point estimate is −1.7 points. Say so
   without calling it a loss, because it does not reject.
3. **The inert-share correction** is now the centre of the section, not a
   footnote. Show Γ₄, Γ₄′ and B̂ side by side. Removing the fire-only
   episodes (ISO-4) raises survival by the whole ISO→JOINT gap (B̂ +0.0098
   against Γ +0.0096). Training on the couplings together adds nothing
   detectable on top of that: Γ₄ −0.03 points, Šidák CI [−0.68, +0.63];
   Γ₄′ +0.13, [−0.56, +0.81]. These are exclusions, not absences.
   State the rule's registration date (2026-09-18). Γ₄′ was proposed
   after Γ₄ was seen and before its arm was read; say so. Γ₄′ is on the
   confirmatory card, so the correction does not rest on a cross-card
   comparison. The disclosed cross-card caveat on Γ₄ finds no support: the
   replicate difference is −0.0015, 95 % [−0.0086, +0.0056].
4. **The secondary dose design** (non-verdict-bearing, 95 %, many intervals
   none family-corrected). The fire-only share costs survival: γ_n = −0.0237
   per unit share [−0.0419, −0.0057]. At ISO's behavioural fire-only share
   of 1/3, that predicts ISO-4 − ISO = +0.0079 against the measured +0.0098.
   The no-element confound's share of the sweep's endpoint change is
   −0.0119 [−0.0210, −0.0028], bounded away from zero as the
   identification arm was designed to do. γ_p = +0.0326 [+0.0137, +0.0502]
   is **a tension, not a finding**: at fixed fire-only share, moving
   single-element into both-element episodes also raises per-element
   exposure, which the simplex cannot separate. It also **does not
   extrapolate**: the plane predicts JOINT − ISO-4 ≈ +0.033, while Γ₄ and
   Γ₄′ measure ≈ 0. Survival sweep: monotone, slope +0.0089 [−0.0033,
   +0.0211]. Completion resolves nothing. Both knees are UNDERPOWERED.
5. **Where the survival gap lives:** fire deaths (JOINT − ISO −0.118 per
   episode, z −4.59, secondary). Out-of-family channels grade nothing
   without their own floor.
6. **Budget robustness — "sign unstable over the final half"** (rule iv,
   both co-primaries). Survival Γ(t) is ≈ 0 through t = 850 (flips at 550
   and 600), then +0.0056, +0.0083 and +0.0096 at 900–1000. The gap **opens
   late and is still growing** at T\* (T = 2000 subsample, descriptive:
   +0.0159). **Completion leans negative in the second half**: negative
   from t = 700, and its Šidák CI excludes 0 at t = 750 only (−0.0147
   [−0.0283, −0.0010]). That is descriptive, since no registered test
   exists at t ≠ T\*. "Completion unaffected" is the wrong gloss;
   "unresolved, leaning negative" is right. Report the registered verdict
   first and the shape second, and never re-read the rule. The
   single-card curve has the same signs.
7. **The High readout — a-fortiori exclusions** (rule vi): Γ_H completion
   −0.0079 (X = 0.0340), survival +0.0038 (X = 0.0254), Γ_H,4 null on both,
   Γ_H within rerun noise (0.73× / 0.75× the floor-basis sd). "No gap larger
   than 2.5 survival points at High, even where JOINT trained on the
   evaluated configuration and ISO never saw a composed one." It is not a
   held-out test.
8. **T = 2000, descriptive only** (4 seeds): Γ(2000) completion +0.0003,
   survival +0.0159 (95 % [−0.0002, +0.0319]). Cite it only for whether the
   drift persists, never to say that Γ "holds".
9. **Mediation — VOID, and why.** Realized training dose does not vary
   with p (slope CI ∋ 0), because the invariant-#5 counter tracks the A
   marginal that the sweep holds fixed (§6 scope note). **Instruments law:
   the registered mediator was blind to co-occurrence in mixed training.**
10. **Reproducibility and hardware.** Seed dispersion over the rerun
    floor: 1.12× / 1.09× completion and 1.25× / 1.19× survival (ISO /
    JOINT). Γ_survival is 5.40× the floor-basis sd(Γ). **Eval
    reproducibility is exact:** 4 reps × 2 checkpoints are bit-identical on
    the post-unblind card and to the grid's own evals, and 280 of 288
    paired cross-card evals are identical (max |Δ| 2.4 × 10⁻⁴).

**The claim, in one sentence:**

> Joint training keeps more agents alive than isolated training at a
> held-out severity, but the advantage is accounted for by the isolated
> arm's fire-only training episodes, not by composition: at matched active
> share, composition adds nothing detectable, and every contrast that
> moves survival leaves the task unresolved.

**Discussion points:** (i) match active share before claiming composition;
the ISO-4 arm cost 20 runs. (ii) A registered design caught it; the
confirmatory result alone would have been reported as a composition
effect. (iii) Paid in agents: the reward sees deaths (d_p = 0.5), not the
hazard, so the asymmetry is between a penalized channel and a rewarded one
(Def. 2 as reworded). The same pattern appeared one level down in Phase 4,
where Coupling B moved survival while its completion effect stayed
unresolved (§6). A task-only evaluation would have seen nothing. (iv) The local composition slope that saturates (γ_p) is
worth a sentence and a figure, not a claim. For reviewer objections and the
do-not-claim list, see `branch_B.md` §7–§8.

## §10 Limitations — shared by every branch

Required on every branch, in this order. Omitting one where the outcome
makes it awkward is outcome-dependent disclosure.

1. **Medium siting.** θ\* is where Coupling B measured −0.0003 on survival;
   its survival effect is at High (replicated 3/3 at 4.7–10.7 points; the
   registered §4a text quotes the first estimate, 8.8). Medium was chosen
   because both couplings
   clear their lock criteria there and floors are smallest. That trades
   effect existence for measurability, and the paper says so. **By the
   project's own locks, no severity has both couplings strongly live**
   (§7 PROPOSALS RULING, 2026-09-18). At Medium, B is quiet and A is live.
   At High, A is marginal by construction (the supercritical fire consumes
   the fuel collapse would ignite) and B is live. The High readout adds
   breadth in severity; it does not test composition where both elements
   bite. State this once, here, on every branch.
2. **One held-out severity**, interpolated in one scalar between the
   training severities. Defence: the near-critical regime is the test point
   and no training data lies near criticality.
3. **The task requires no coordination.** Foraging with a team reward on
   twelve shared-parameter agents. Swarm effects are a choice, not a
   requirement. Do not use "swarm" as a claim.
4. **The death penalty** (see §3 wording change). The reward sees deaths,
   not the hazard, so write the survival/completion asymmetry as a
   penalized channel against a rewarded one.
5. **Comms encoder is frozen.** "Inert" is scoped to this encoder.
6. **Observation contains absolute position and time**; Thm. 1 addresses
   memorization, but the confound is real and the wall-drift artifact
   (every episode of every arm ends near a boundary) is its visible form.
   The drift channels are recorded, ungraded, floors owed.
7. **Γ's interval is conditional on the common eval draw** (512 episodes,
   seed 0); it reflects training-seed variance only.
8. **Hardware block structure** (`che/bench/results/phase6/by_card/`).
   Three rented units of one card model, the RTX 5090. Γ uses all 72
   seeds of both arms on **one** unit, as does every analysed secondary
   run (seeds 1–12 re-carded, 13–20 from the grid). Γ₄′ is therefore
   same-card. ISO-4 and the T = 2000 subsample trained on a second unit, so
   Γ₄ and B̂ are cross-unit contrasts. The post-unblind evals (Γ(t) at
   t < 1000, the High readout, the eval floor) ran on a third unit. Γ(t)
   at t = 1000 is the grid's own eval, and the cross-card check shows the
   mix costs nothing measurable (§9.2 item 10). The grid's first 12 seeds, run on an
   RTX PRO 6000, were superseded by the single-card re-run and enter only
   a descriptive card diagnostic.
9. **No external baseline** (no DR schedule, no PLR/ACCEL curriculum). The
   paper compares two training distributions on one environment.
10. **Hazard simplicity**: burn time one step, single ignition, no wind or
    fuel heterogeneity; the fire is a percolation front by construction.
11. ~~SMART (RA-L 2026)~~ — removed; nothing to pre-empt until a real record
    exists (CITATION REPOSITIONING RULING, 2026-09-26).

## §11 Reproducibility and appendix manifest

TMLR: anonymized supplementary code; the ≤ 100 MB limit is recorded only
in the decision log, so confirm it on TMLR's page (ledger O-4). Ship
`che/ docs/ pyproject.toml uv.lock`, not `m06/`, built with `git archive`
so gitignored checkpoint archives stay out. The old "454 KB" figure dates
from 2026-08-04, before most results were committed; re-measure it
(ledger O-3).

Appendices:

- A. Full proofs (Props. 1–4, Thm. 1, Remark 2′).
- B. Calibration protocol and every lock with its record.
- C. Floors: every measured floor with card, run length, and artifact.
- D. The frozen analysis plan, verbatim, with its registration date.
- E. The four registered outcome branches, verbatim, with the falsifiers.
- F. Grid provenance: cards, block structure, chunk boundaries, archive
  hashes.
- G. Throughput and the keep-alive-set statement for every env-only figure.
- H. Γ(t) curves and the sign-stability reading.
- I. Secondary sweeps with UNDERPOWERED flags where applicable.

## Figure list

| # | figure | status |
|---|---|---|
| 1 | Env schematic: the five kernels and the step order, with the two couplings drawn as arrows | draft now |
| 2 | Percolation calibration: P_span and R_L vs β at three L; β̂_c marked; the three severity levels | data committed |
| 3 | Coupling A: Prop. 3 linear handshake; seeded ignitions vs severity (the 4.83× fall) | data committed |
| 4 | Coupling B: masking concentration on danger moments; High survival effect with floor bars | data committed |
| 5 | Co-active event distribution per episode at three severities | data committed |
| 6 | Comms: VoC handshake; δ = 0 vs 1 with floor bars | data committed |
| 7 | Floors: per-card, per-run-length, per-artifact bar chart | data committed |
| 8 | **[Γ]** the confirmatory contrast with CI and MDE band, **with Γ₄, Γ₄′ and B̂ beside it** (the inert-share correction is the centre of §9.2) | data committed (`unblind/`, `post_unblind_analysis/`, `secondary/`) |
| 9 | **[Γ]** Γ(t) over the final half, both co-primaries, Šidák bands; the single-card curve as a companion | data committed (`post_unblind_analysis/`) |
| 10 | Dose sweep and identification arm, labelled secondary; the γ_p plane with its non-extrapolation to JOINT marked | data committed (`secondary/`) |
