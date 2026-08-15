# VENUE REVIEW — pre-grid, pre-unblind (2026-08-16)

**Status: an assessment, not a ruling.** Nothing in this document changes a
constant, a config, a lock, an analysis family or a threshold. `SIDAK_M`,
`K_CONFIRMATORY`, `K_SECONDARY`, `T_STAR`, `m62_report.py::METRICS` and every
entry in `docs/locks.yaml` are untouched. The proposals in §7 are **PROPOSALS
AWAITING RULING**; the one decision taken here — venue — is transcribed
separately in `docs/decision_log.md` (*VENUE RULING*, 2026-08-16) and binds
from that entry, not from this file.

**Written pre-grid and pre-unblind.** No Phase-6 outcome mean exists and
nothing below is conditioned on one. That timing is what makes §3 and §5
sayable: they identify a bias whose *direction* is known and whose
*realization* is not.

**Provenance of every number.** Each figure below is either quoted from a
committed artifact with its path, or derived in-session from such figures with
the arithmetic shown. Per the derived-numbers sub-rule (2026-07-28), nothing is
transliterated. Estimates are labelled as estimates and carry their inputs'
limits.

**Scope of the reviewer's standing.** This review was produced from the
repository — theory doc, design v2, framing branches, the phase 3–6 reports,
`g1_2_report.md`, and the generated Phase-6 configs. It contains **no
independent literature search**: §6's positioning items are gaps to close, not
scoop findings.

---

## 1. The verdict, stated first

The measurement and engineering discipline in this repository exceeds normal
published practice in empirical RL. The **scientific payload is thinner than
the process around it**, and the registered target venue is the wrong one for
what the project actually holds.

Three of the four registered outcome branches
(`phase6_framing_branches.md` §3) are not the founding claim, and by the
project's own measurements the modal outcome is **branch C** (§5).

| venue | fit | assessed chance | basis |
|---|---|---|---|
| **NeurIPS D&B** | strong | **moderate** | Tier-1 items in `phase6_framing_branches.md` §2 are benchmark contributions verbatim. Competitive track; pre-registration + bitwise ablations + calibrated severity differentiate. |
| **TMLR** | strong | **high** | No novelty bar, rewards rigor and well-powered nulls, no page ceiling. The measurement methodology alone clears it. |
| **AAMAS (full)** | good | **moderate** | Dec-POMDP formalism + swarm + empirical study is in scope. |
| **RLC** | good | **moderate** | Empirical-rigor culture; environment contributions welcome. |
| **RA-L / IROS** | **weak** | **low, and low even on branch A** | §2. |

---

## 2. RA-L/IROS fit is structural, not a writing problem

The artifact is a 64² discrete grid, 12 agents, 5 discrete actions
(`env.py:N_ACTIONS`), food collection (`tasks.py::task_step`), CA fire. There
is no robot, no continuous control, no dynamics model, no hardware, no
sim-to-real. The only embodiment argument in the tree is one clause of the
theory doc — *"robots walking on weak floors"* (Def. 2, clause 2 note).

Two consequences the project has already half-recorded:

1. **Page budget.** Positioning ruling 6a (2026-08-05) records RA-L as 6+2
   pages with **appendices included**, and declares the appendix-manifest
   strategy dead. What must then fit in 8 self-contained pages: Prop. 1,
   Prop. 2's coupling proof, Thm. 1, Def. 5/6, the calibration phase, a
   240-run grid, a 5-point dose sweep, a 3-point identification arm, a
   co-primary family with its correction, and a pre-registration description.
   It does not fit. What survives that cut reads as a small gridworld study —
   the version most likely to be rejected.

2. **Reviewer prior.** The theory is percolation and Dec-POMDP hardness; the
   novelty spine (positioning ruling 1, as narrowed 2026-08-13) is
   measured-critical-point severity, hazard-generates-hazard, Beer–Lambert on
   an observation kernel, and JAX × MARL × hazard-independent reward. Every
   item is an ML-methods claim. None is a robotics claim.

**This is not a downgrade.** A well-powered null at a venue that reads nulls is
a better paper than a compressed positive at a venue that does not.

---

## 3. The interesting outcome is registered as the consolation prize

JOINT trains at the exact θ\* composition (`p6_joint.yaml`: both components
carry `kappa_A 0.06, kappa_B 1.0, delta 1.0`); ISO never sees co-activity at
all (`p6_iso.yaml`: co-occurrence 0.0000). Therefore:

- **Γ > 0** has a trivial reading — *training on the test distribution beats
  training on its marginals*. That is the standard prior in compositional
  generalization, and confirming it is a weak result.
- **Γ ≈ 0** is the surprising, practitioner-actionable result — *isolated
  stressor training suffices, so you may train on cheap decompositions*.

`phase6_framing_branches.md` §3 assigns branch A the RA-L lean and states of
branch C that it *"is not RA-L-shaped"*. Design v2 §5 already reaches the same
place from the statistics: a null here is *"more likely to be a real null than
an underpowered one — which is scientifically good and strategically
uncomfortable"*.

**The discomfort is an artifact of the venue target, not of the science.**
Under §1's retarget it inverts: branch C is the headline-capable branch at a
benchmark venue, because a calibrated instrument plus a well-powered
exclusion is exactly what that venue scores.

**No branch table is edited by this document.** The four branches stand
ratified verbatim (2026-08-13). What changes is which branch the paper is
*written for by default* — and that is a framing decision the framing
registration explicitly left open (§7, *"venue is deliberately NOT decided
here"*).

---

## 4. A registered-halfway bias in the confirmatory contrast

**This is the highest-value finding in this review, and it is only sayable
pre-unblind.**

`p6_iso.yaml` carries 6 uniform components at weight 0.166667. Two of them —
`d_low`, `d_high` — are δ-only: `kappa_A: 0.0, kappa_B: 0.0, delta: 1.0`.
Phase 5 certified δ **inert** (`phase5_report.md` M5.5 final verdict; M5.3/M5.3b
mechanism). Therefore:

> **2/6 = 0.3333 of ISO's training episodes carry no behaviourally active
> element.** They are hazard-only baseline episodes. 100 % of JOINT's episodes
> carry both live couplings.

### What is registered, and what is not

Design v2 §2 **registers the marginal imbalance** — *"deliberately unmatched in
per-element marginal (1/3 in ISO vs 1 in JOINT)"* — and defends it as
definitional under the founding registration. That defence holds.

What is **not** registered is that the residual third is behaviourally
*empty* rather than a third element. The generated header asserts
`no-element 0.0000`. That is true **nominally** and false **behaviourally**,
given the project's own Phase-5 certification. Under that certification ISO's
effective composition is `{A 1/3, B 1/3, nothing 1/3}`, not
`{A 1/3, B 1/3, δ 1/3}`.

This is the same confound design v2 §2 polices for the sweeps — *"at p = 0.5
half of all training episodes contain no stressor at all"* — reappearing
**inside the confirmatory arm at p = 1/3, uncounted**.

### Why §1's symmetry defence does not cover it

Design v2 §10 item 4 defends δ retention as symmetric: neither arm trains on
δ = 1.0 in isolation at θ\*, so it should not bias Γ. **That symmetry holds at
test time and fails at train time.** In JOINT, δ rides free inside an all-on
component and costs nothing. In ISO, δ occupies two dedicated components and
costs a third of the training budget. The arms are symmetric in *exposure* and
asymmetric in *price*.

### Direction, and why it matters now

**The bias inflates Γ.** If branch A lands, *"ISO spent a third of its budget
on an element you yourselves certified inert"* is an objection with no
post-hoc answer. Registering the direction now costs $0 and is not optional
under the bars-come-with-floors discipline; §7 proposes the $3.41 measurement
that converts it from a caveat into a number.

Note the internal precedent: the sweeps **already** exclude δ for exactly this
reason — design v2 §2, *"comms is certified inert, so including it would
multiply components without adding information"*. The confirmatory arm applies
a different rule to the same fact.

---

## 5. Siting at Medium buys measurability and may buy away the effect

Recorded already as branch-invariant §4a, and restated here with its
consequence made explicit.

At θ\* (β = 0.49, Medium), by the project's own measurements:

| element | measured behaviour at Medium | source |
|---|---|---|
| Coupling B | survival effect **−0.0003**, within noise; its 8.8-point effect is at **High** | `phase4_report.md` Result 1 |
| comms δ | **inert** | `phase5_report.md` M5.5 |
| co-activity | **0.64 events/episode**, P(zero) = **0.578** | `phase4_report.md` Result 4 |

So the confirmatory point is well-powered
(`g1_2_report.md`: sd(Γ) = 0.00504 completion / 0.00310 survival at k = 40 →
MDE80 0.0155 / 0.0095, k_req 11 / 5) to find an effect that may not exist
there, and the composition under test is effectively A × B where B is
individually quiet.

**Consequence for branch C, stated because it is the modal branch:** a null
sited at the one severity where both live elements are individually quiet is a
**narrow** null. Its value as a finding scales with its breadth.

### Would a High secondary arm rescue it? — derived in-session

Inputs, quoted: `phase6_framing_branches.md` §5, High cell seed dispersions —
completion 0.0485 (A_live) / 0.0517 (B_live); survival 0.0794 / 0.0783.
**Limits carried from that table: n = 3 per entry (≈ ±60 %), T = 500
artifacts, transfer to T = 1000 is an assumption flagged there.**

Contrast SE (M6.2b close-out form), k = 20:

    sd(Γ) = sqrt((σ_A² + σ_B²)/k)

    completion: sqrt((0.0485² + 0.0517²)/20) = sqrt(0.00502514/20) = 0.01585
    survival:   sqrt((0.0794² + 0.0783²)/20) = sqrt(0.01243525/20) = 0.02494

MDE at 80 % power, Šidák m = 2 (z_α = 2.2365, z_0.8 = 0.8416, sum 3.0781):

    completion: 3.0781 × 0.01585 = 0.0488
    survival:   3.0781 × 0.02494 = 0.0768

**Reading.** A High arm at k = 20 resolves ~4.9 points completion and ~7.7
points survival. κ_B's own measured High survival effect is 8.8 points
(`phase4_report.md` Result 1), so such an arm could **just** resolve an effect
the size of the single-element one and nothing smaller. **It would ship with
the UNDERPOWERED flag** under the standing rule, and it is offered in §7 on
that basis only — as breadth for a null, never as a second confirmatory test.

This is also the honest defence of the Medium siting: it trades effect
*existence* for effect *measurability*, the survival floor at High being 0.0621
against 0.0130 at Medium (`phase5_report.md` M5.3b / M5.5). The trade was made
correctly. It should be **stated in the paper**, not left for a reviewer.

---

## 6. What reviewers will ask for that the project does not have

1. **The fixed-budget estimand versus differential drift.** Measured at
   T = 1000 (`g1_2_report.md`): ISO +0.01202 per 100 updates, JOINT +0.02411.
   Derived: differential **0.01209 per 100 updates**, i.e. over the final 500
   updates **0.0605 — 2.02× the 0.03 target effect**. The arms sit at
   different points on their learning curves, so Γ at T = 1000 partly measures
   who is climbing faster. Γ(t) sign-stability (T\* ruling §3) is the
   registered mitigation and is the right one, but it is a *diagnosis*, not an
   *answer*: a reviewer reads "ISO plateaued, JOINT still climbing, JOINT
   wins" as a run-length artifact. §7 item 3 preempts it for $2.68.

2. **No baseline outside the project's own two arms.** No domain-randomization
   schedule, no PLR/ACCEL-style curriculum, no robustness method. Acceptable at
   a benchmark venue where the environment is the contribution; thin at
   AAMAS/IROS.

3. **Comms inertness rests on a frozen random projection.**
   `phase5_report.md` carries this as an explicit limitation
   (*"gradient-shaped messaging remains untested"*). M5.3's demand-side
   argument — the unused connectivity bit needs no encoder, so its neglect
   cannot be blamed on the projection — is the correct defence and should be
   **foregrounded rather than carried**. Expect this to be the main attack on
   the comms half.

4. **Positioning gap: UED / domain randomization.** The no-scoop checks
   (2026-08-13) covered JAX-MARL benchmarks (JaxMARL, Multi-Agent Craftax,
   Assistax, POBAX, BenchMARL), wildfire simulators, and CompoSuite. The
   literature where *joint-versus-isolated training-distribution* questions are
   standard — unsupervised environment design and domain randomization — is not
   engaged anywhere in the tree. **This is a related-work hole, not a scoop
   finding**: no search was run for this review. Any ML-venue reviewer will
   ask.

5. **β = 0.49 is interpolation in one scalar** between 0.43 and 0.70. Expect
   *"weak held-out condition"*. Design v2 §1's defence (near-critical regime is
   the test point, no training data near criticality) is sound and must land
   explicitly.

6. **The bibliography is unverified, and this is the highest-severity
   non-technical risk in the project.** VULCAN, Agrawal 2023, Erdem & Üre 2025
   and SMART (RA-L 2026) are relayed names only; the log records that relays
   here have **twice named documents that do not exist**
   (`HANDOFF.md`, working agreements). The JaxWildfire and arXiv:2604.26150
   rows rest on an automated summary, flagged as insufficient to write related
   work from. **A fabricated citation in a submission is worse than every
   statistical defect this project has already fixed.**

7. **The paper is the least-managed artifact in the project.** The skeleton and
   the DR-defense memo are not in this tree. Everything else carries locks,
   tests and a decision log; the deliverable carries none.

---

## 7. Proposals — AWAITING RULING, none taken here

Cost basis, derived in-session: **497 s/run at T = 1000** on the G1.2 card
(`HANDOFF.md`, hardware facts) at the measured **$1.2358/h**
(`g1_2_report.md` / `HANDOFF.md`) →

    497 / 3600 × 1.2358 = $0.1706 per run

Free reserve: **~$65 reserve − ~$48.6 projected trip = ~$16.4**
(`HANDOFF.md` §2). The three proposals total **$12.91**, which fits with
almost no margin — **they are ranked, not bundled.**

| # | proposal | runs | derived cost | what it buys |
|---|---|---|---|---|
| **0** | **Register §4's bias direction in writing, pre-unblind** | 0 | **$0** | Non-optional under the standing discipline. Do this whether or not 1–3 are ruled. |
| **1** | **`ISO-4` secondary arm** — {A-only, B-only} × {0.43, 0.70}, 4 components, k = 20 | 20 | **$3.41** | Converts §4's unanswerable post-hoc objection into a measured number. Applies to the confirmatory arm the rule the sweeps already apply. |
| **2** | **T = 2000 subsample**, confirmatory arms only, 4 seeds each | 8 | **$2.68** | Preempts §6 item 1. Distinct from the T = 2000 the T\* ruling **declined** — that was the whole grid; this is a subsample robustness arm. |
| **3** | **High-severity secondary point**, 2 arms × k = 20, **UNDERPOWERED-flagged** | 40 | **$6.82** | Breadth for a branch-C null (§5). Resolves ~4.9 pt completion / ~7.7 pt survival only. |

Derivation for proposal 2's run length: train scales linearly in updates and
eval is flat (design v2 §6 UPDATE, measured). Taking eval = 19 s
(`results/phase6/m62/timings.txt`, measured on the *slower* M6.2 card, so
conservative), train(T = 1000) ≈ 497 − 19 = 478 s → run(T = 2000) ≈
2 × 478 + 19 = **975 s** → 8 × 975/3600 × 1.2358 = **$2.68**.

**Recommended order if not all three are affordable: 0, then 1, then 2, then
3.** Proposal 1 is ranked above 3 because it removes a *known-direction bias
in the confirmatory contrast*, whereas 3 adds breadth to a secondary claim.

**None of these may be adopted post-unblind.** Each is a design-stage addition
whose value is entirely in having been chosen with no outcome visible.

---

## 8. What is genuinely strong, and should lead

Stated last so it is not read as consolation. These are the items a benchmark
venue scores, and they are all already measured and committed:

1. **Pre-registration with mechanical blinding.** The report script suppresses
   cross-arm means; the grid runner computes no cross-arm quantity and a test
   asserts it; the outcome-conditional framing is registered in advance. This
   is rare, real, and checkable.
2. **Bitwise-exact nested ablations.** Frame as *"ablations are exact by
   construction"* — not as an implementation detail about PRNG consumption.
3. **Severity by measured dynamical phase** rather than knob position, with
   β̂_c = 0.500 at 512 seeds. Present as *methodology* — the reproduction of
   Kesten's value is the **validation** that licenses it, not the contribution.
4. **The measurement methodology itself** — floors per-metric/per-hardware/
   per-artifact, contrasts graded on the contrast's SE, 80 %-power MDEs at the
   corrected α, *measuring is not grading*. Better than most published
   practice, and it is a methods section at a venue that reads methods.
5. **The Γ-independent empirical findings**, which are the most paper-shaped
   results in the tree: Coupling A self-limits where the hazard is worst
   (4.83× fall, `e11_report.md`); compound hostility is rare and bursty
   (`e13_report.md`); masking concentrates 16–118× on danger moments
   (`phase4_report.md`); comms inert at swarm scale via a joint argument
   (Phase 5).

Items 1–5 are `phase6_framing_branches.md` §2's tier 1, which was **checked**
to carry a paper on its own. That check is what makes §1's retarget safe: the
paper does not depend on Γ.

---

## 9. What this review is blind to

Stated under the standing rule that instruments declare their limits.

- **No literature search was run.** §6 item 4 is a gap in the tree, not a
  claim about the field. Whether UED/DR work subsumes any part of the framing
  is unmeasured here.
- **No venue statistics were consulted.** The "assessed chance" column in §1 is
  a judgement from fit, not a base rate.
- **CfP mechanics are unverified.** Page limits, anonymity handling, and
  artifact-link requirements for the retargeted venue are owner tasks
  (`decision_log.md`, *VENUE RULING*, owed items).
- **The reviewer read the repository, not the paper**, because no paper exists
  in this tree. Every judgement about how the work reads is a judgement about
  how it *would* read if written as the documents describe it.
