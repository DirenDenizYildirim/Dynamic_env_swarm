# Common spine — the Γ-independent paper

Target: TMLR. No page limit; length must be justified by content. Two
acceptance criteria only: (i) claims supported by evidence, (ii) some of the
audience would be interested. Write every section to criterion (i) and let
the tier-1 findings carry (ii).

Sections marked **[Γ]** receive content from the branch file. Everything
else can be drafted today.

---

## Title candidates (branch-neutral; the branch file may override)

- *Compound Hostility: a calibrated multi-agent RL environment where the
  hazard makes its own danger*
- *Ambient stressors, exact ablations, and a pre-registered test of
  compositional generalization in swarm RL*
- *CHE: measuring what a swarm learns when the environment is the adversary
  and the reward does not say so*

Avoid "swarm" in the title unless the task is reframed; the foraging task
requires no coordination (see Limitations). "Multi-agent" is safe.

## Abstract — template

> We introduce the Compound Hostile Environment (CHE), a pure-JAX
> multi-agent RL environment in which a cellular-automaton fire is causally
> coupled to structural collapse (collapse seeds fire) and to perception
> (smoke attenuates observation by Beer–Lambert transmittance), with an
> independent communication-denial axis. The hazard is an *ambient survival
> stressor*: it never enters the reward or any cost channel, so survival is
> learned only through the task return. Three properties make CHE an
> instrument rather than a demo: severity is defined by a *measured*
> percolation critical point (β̂_c = 0.500 ± 0.005, reproducing Kesten's
> exact value), every stressor is a parameter of one kernel so that
> ablations are *bitwise exact* nested models, and every acceptance bar in
> the paper is graded against a measured reproducibility floor. Calibration
> yields four findings independent of any training comparison: collapse-
> seeded fire self-limits where the hazard is worst; compound hostility is
> rare and bursty; perception decay cannot be behaviourally suppressed; and
> inter-agent communication is inert at swarm scale. We then run a
> pre-registered, mechanically blinded test of compositional generalization:
> whether training on co-active stressors beats training on the same
> stressors in isolation, at a held-out severity and matched compute
> (k = 40 seeds per arm). **[Γ: one sentence from the branch file.]** All
> code, configs, locks and the frozen analysis plan are released.

## Contribution list — order for the intro

1. **The environment as an instrument.** Def. 2 reward independence,
   Prop. 1 kernel factorization, bitwise nested ablations, severity by
   measured phase. (Tier 1, items 1–3.)
2. **Four calibration findings** that stand without Γ. (Tier 1, items 4–8.)
3. **A measurement methodology** for empirical RL: per-metric, per-hardware,
   per-artifact floors; contrasts graded on the contrast's SE; 80 %-power
   MDEs at family-corrected α; "measuring is not grading".
4. **A pre-registered compositional-generalization test** with mechanical
   blinding, and its result. **[Γ]**

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
  co-occur to survive their co-occurrence? State it as a question with
  priority holders (Agrawal 2023, Erdem & Üre 2025 `[VERIFY]`); our
  contribution is the design, named by DBCA (Keysers et al. 2020): atom
  divergence → 0, compound divergence → max, instantiated in MARL dynamics.
- Why an instrument first: three of the four registered outcomes of the
  compositional test are not the founding hypothesis, and the paper was
  designed so that a paper exists on every branch. Say this plainly. It is
  what makes the pre-registration credible.
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
| JAX × MARL × hazards | JaxMARL, Multi-Agent Craftax, Assistax, POBAX, BenchMARL | none carry an evolving lethal field |

Neighbours and how they are positioned (rulings 2026-08-05):

- **Hazard in the reward**: Haksar & Schwager 2018 (distributed MADQN under
  fire spread). Def. 2 clause 1 separates us.
- **Hazard in a cost/constraint channel**: VULCAN `[VERIFY]` is the nearest
  domain neighbour on the far side of the Def. 2 boundary; safe-RL / CMDP
  generally.
- **Compositional generalization in RL**: Agrawal 2023, Erdem & Üre 2025
  `[VERIFY]` as priority holders on the question; Keysers et al. 2020 for
  the split methodology; arXiv:2604.26150 `[READ THE PDF]` (single-agent,
  reward penalizes burning cells; cite as contrast, not as prior).
- **UED / domain randomization**: **this paragraph is owed and no search
  has been run.** PLR, ACCEL, PAIRED, and the DR literature ask joint-vs-
  isolated training-distribution questions routinely. Write this paragraph
  after a real search; a TMLR reviewer will ask.
- **Communication value**: Pynadath & Tambe 2002 (COM-MTDP: observability
  gates communication value) is cited first; Remark 2′ refines it with the
  collective-redundancy conjunct. Cite, then refine, in that order.
- **Multiple stressors / compound events**: ecology and climate literatures
  as supportive analogies for the word "compound", one sentence.
- **SMART (RA-L 2026) `[VERIFY]`**: cited and pre-empted in Limitations.
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
- **Def. 2** ambient survival stressor. **Wording must change before
  submission** (checklist item 1): the training reward carries a death
  penalty of 0.5 per newly disabled agent, which reads the alive transition,
  an X variable, and never h, ρ or c. Def. 2 as written says "no shaping
  term" and "solely because death truncates future task return". Replace
  with: *the hazard enters neither R nor any cost/constraint channel; R is a
  function of task variables and the agent-state transition only. A death
  penalty on the alive transition is permitted and is used; the dp = 0
  ablation is reported.* Then report the Phase-2 dp = 0 vs 0.5 numbers so
  the reader sees what the term buys (High survival 0.575 → 0.866).
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
  position and time, 5 actions, foraging task with 32 items and +1 team
  reward per collected item. Shared-parameter actor-critic
  (Conv 16 → Conv 32 → Dense 128 → heads), IPPO, PBT population 12.

## §4 Severity calibration

- β̂_c = 0.500 ± 0.005 from the R_L logistic-centre family at
  L ∈ {32, 48, 64}, 512 seeds; self-duality R(β_c) ≈ 1/2 at all three sizes.
  Present the Kesten reproduction as **validation of the method**, not as
  a result.
- Locked levels and what they mean:

  | level | β | P_span | burnt fraction |
  |---|---|---|---|
  | Low | 0.43 | 0.021 | 1.9 % |
  | Medium | 0.49 | 0.547 | 19.8 % |
  | High | 0.70 | 0.998 | 98.3 % |

- Medium sits between the finite-size pseudo-critical point β_c(64) ≈ 0.486
  and β̂_c; it is the held-out severity for the compositional test.
- Def. 4's variance-peaks-at-Medium prediction was **not observed** (M3.5:
  survival variance monotone, highest at High). Report the refutation.

## §5 Coupling A — hazard begets hazard

- Lock: f_weak 0.15, λ₀ 5·10⁻⁵, λ_load 4·10⁻⁴, κ_A 0.06, r_A 1.
- Prop. 3 handshake: R² = 0.998 over a 14× range; matched-reference ratio
  0.992 ∈ [0.90, 1.02].
- **Finding: the ignition channel self-limits where the hazard is worst.**
  Seeded ignitions per episode 4.05 / 3.41 / 0.84 across Low / Medium /
  High, a 4.83× fall, by fuel exhaustion. Replicated on m35.
- **Finding: the near-agent share is flat** across severity, [0.164, 0.203];
  the whole severity response is upstream of the agents.
- Low leaves the survival ceiling (0.979 → 0.961). No weak-cell avoidance
  detected.

## §6 Coupling B — hazard degrades perception

- Lock κ_B = 1.0 on the detection band alone; the three lock bands did not
  intersect (masked-frac band unreachable at Medium; E2C band disjoint from
  detection band by 1.35×). Say this; it is honest and it is interesting.
- Thm. 1 E2C gate green: max |z| 2.11, χ² p = 0.586 against the closed-form
  1/2 + q/2.
- **Finding: perception decay is paid in survival, not completion.** High:
  −8.8 points survival (range 5–11 across the correction, direction 3/3,
  floor sd 0.062); completion effect flipped sign on a same-seed retrain and
  is **unresolved**. Medium: −0.0003, within noise. **This Medium number is
  load-bearing for the Limitations section on every branch.**
- **Finding: masking concentrates 16–118× on danger moments.** The coupling
  cannot be behaviourally suppressed.
- Co-active visitation (Prop. 4 diagnostic): 0.64 events/episode at Medium,
  P(zero) = 0.563 / 0.578 / 0.883, var/mean 1.31–1.40. **Rare and bursty.**
  Always show the distribution, never the mean alone.

## §7 The comms axis — certified inert, by a joint argument

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
  survival stayed 0.0129 / 0.0130; the traced tree differing from itself
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
- **Reproducibility floors grow with run length, ordered by curriculum
  difficulty** (tier 2): ISO 2.1×, JOINT 5.2× from T = 500 → 1000.

## §9 The compositional test — design (Γ-independent) **[Γ: results]**

- ISO: 6-component uniform mixture {A-only, B-only, δ-only} × {Low, High}.
  JOINT: {all-on} × {Low, High}. θ\* = all-on at **held-out** β = 0.49.
  Same architecture, same compute, same eval set.
- Estimand: Γ = J_θ\*(JOINT) − J_θ\*(ISO) at **matched budget T\* = 1000
  updates**. Co-primaries completion and survival, Šidák m = 2
  (z_α = 2.2365), k = 40 per arm, unpaired contrast SE from the grid's own
  seed dispersion. Secondary: dose sweep c = 0.5 at five p points and
  identification c = 0.4 at three, k = 20, labelled non-verdict-bearing.
- Design-stage power from the launch batch: sd(Γ) 0.00504 / 0.00310,
  MDE80 0.0155 / 0.0095, k_req 11 / 5. Label these as an **upper bound on
  power** since floors are a lower bound on seed dispersion.
- **Blinding, described in-text without links:** the report script
  suppresses cross-arm means; the grid runner computes no cross-arm quantity
  and a test asserts it; the four outcome branches and their framings were
  registered on 2026-08-13; the venue was ruled 2026-08-24; all pre-grid.
  Quote dates, not hashes that resolve to an account.
- **Budget robustness:** Γ(t) over 11 checkpoints (updates 500–1000) on
  the confirmatory arms, read for sign stability over the final half.
  "Sign unstable" is a finding and is reported as one.
- **Registered biases, stated before the result:**
  (a) ISO spends 1/3 of its budget on the δ element, which §7 shows is
  inert, so ISO effectively trains on {A, B, nothing}; this **inflates Γ**.
  ⟨If the ISO-4 control arm was run, report it here.⟩
  (b) The arms sit at different points on their learning curves at T\*
  (ISO 0.56× its floor, JOINT 1.02×); the differential drift is
  ~0.012 per 100 updates, a local sensitivity estimate, never a bound.
- **[Γ] Results subsection: from the branch file.**

## §10 Limitations — shared by every branch

Required on every branch, in this order. Omitting one where the outcome
makes it awkward is outcome-dependent disclosure.

1. **Medium siting.** θ\* is where Coupling B measured −0.0003 on survival;
   its 8.8-point effect is at High. Medium was chosen because both couplings
   clear their lock criteria there and floors are smallest. That trades
   effect existence for measurability, and the paper says so.
2. **One held-out severity**, interpolated in one scalar between the
   training severities. Defence: the near-critical regime is the test point
   and no training data lies near criticality.
3. **The task requires no coordination.** Foraging with a team reward on
   twelve shared-parameter agents. Swarm effects are a choice, not a
   requirement. Do not use "swarm" as a claim.
4. **The death penalty** (see §3 wording change).
5. **Comms encoder is frozen.** "Inert" is scoped to this encoder.
6. **Observation contains absolute position and time**; Thm. 1 addresses
   memorization, but the confound is real and the wall-drift artifact
   (every episode of every arm ends near a boundary) is its visible form.
   The drift channels are recorded, ungraded, floors owed.
7. **Γ's interval is conditional on the common eval draw** (512 episodes,
   seed 0); it reflects training-seed variance only.
8. **Four cards may have run the grid.** Seed-major order puts both arms of
   a seed on one card so the card effect cancels in Γ; the block structure
   is reported.
9. **No external baseline** (no DR schedule, no PLR/ACCEL curriculum). The
   paper compares two training distributions on one environment.
10. **Hazard simplicity**: burn time one step, single ignition, no wind or
    fuel heterogeneity; the fire is a percolation front by construction.
11. **SMART (RA-L 2026) `[VERIFY]`** pre-empted here.

## §11 Reproducibility and appendix manifest

TMLR: anonymized supplementary code ≤ 100 MB. Ship `che/ docs/ pyproject.toml
uv.lock` (454 KB), not `m06/`.

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
| 8 | **[Γ]** the confirmatory contrast with CI and MDE band | post-unblind |
| 9 | **[Γ]** Γ(t) over the final half, both co-primaries | post-unblind |
| 10 | Dose sweep and identification arm, labelled secondary | post-unblind |
