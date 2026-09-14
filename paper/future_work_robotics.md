> **SUPERSEDED IN PART 2026-09-14.** The two ruled follow-ups (Stage 0
> Coupling C, and expendability economics) are now ONE paper in a separate
> repository, `/home/diren/A_Research/Expendable_swarm` (its own theory doc,
> decision log and novelty audit). The compositional-gap successor framing
> below (Stages 1–3 as "does the gap survive embodiment") is retained as the
> record but is no longer the plan of record for RA-L; see that repository's
> `README.md` and `docs/theory_foundations.md`.

# Future work — the embodied successor, made outcome-robust and staged

> **DECIDED 2026-09-09 (owner):** build Stage 0 (Coupling C on the grid) and
> the expendability-economics paper (robotics plan §4.4). Ideas 4.1, 4.2,
> 4.3, 4.5 and 4.6 are dropped and are not to be reopened. Stages 1–3 below
> remain conditional on Stage 0's go criterion.

Companion to `chaos_robotics_research_plan.md` §3. That document describes
the full paper. This one describes how to start it without betting a year
on a CHE result that does not exist yet, and what each stage must show
before the next is funded.

Written 2026-09-07, pre-grid. Same rules as the rest of `paper/`: no CHE
grid number appears here, and every citation in the plan's novelty audit
is `[VERIFY]` until checked by hand.

---

## 1. The thesis, restated so it does not depend on CHE's branch

The plan's thesis is *"the gap measured on the grid predicts the gap in an
embodied simulation."* That sentence has content only if the grid produces
a gap. CHE's registered modal outcome is branch C, both null. So the
successor needs a thesis that is a real question on every branch:

> **Does embodiment change whether co-active training matters?**

Under each CHE branch it reads differently, and each reading is a paper:

| CHE branch | what the grid established | what the embodied test asks | a positive result | a null result |
|---|---|---|---|---|
| A | co-activity matters on the grid | does the gap survive dynamics, sensor physics, and degradation? | the grid is a cheap proxy | embodiment washes out the gap; which factor did it |
| B | paid in survival, not task | does embodiment move the cost into task return? | embodiment couples survival to task | the asymmetry is robust to embodiment |
| C | isolated training suffices, up to X | does adding a coupling the grid cannot express (heat → actuators) create a gap? | embodiment is what makes composition matter | a broad null: isolated training suffices even with capability degradation |
| D | reversal or budget artifact | resolve first; do not build on D | | |

Branch C is the one that changes the paper most, and it is the modal one.
Under C the interesting claim is not transfer but **whether Coupling C is
the missing ingredient**. Prop. 4's mechanism says a new co-active region
(smoke × heat, or collapse × heat) is a region ISO never sees. If ISO still
matches JOINT there, the null is much broader than the grid's. If it does
not, the paper has located what makes composition matter. Either is a
result.

## 2. Two couplings, chosen now

The plan says pick two and it is right. Pick **B and C**.

- **B (smoke → sensor physics)** is the coupling the plan itself says
  changes most with embodiment: range attenuation plus scattering-induced
  dropout and false near returns. The policy has to reason about what
  kind of corruption it sees, not a dimmer image.
- **C (heat → actuator and energy degradation)** is the only genuinely new
  mechanism in the plan and is absent from CHE. Per-agent heat state
  accumulates near burning cells, reduces achievable speed or action
  success, drains energy, recovers slowly or never.
- **A (collapse → fire)** is dropped to an appendix ablation. The grid
  already showed it self-limits where the hazard is worst, and it is the
  coupling least sensitive to embodiment.

Reward independence carries over unchanged: heat, energy, smoke and fire
never enter the reward. Death and immobilization truncate return. The
Def. 2 wording fix from the checklist applies here too; decide before
building whether an energy-exhaustion penalty exists and state it.

## 3. Stages, each with a kill criterion

### Stage 0 — Coupling C on the grid (2–4 weeks, ~$30)

The plan's own step 3, "embodiment decomposition, one factor at a time on
the gridworld", moved to the front because it is the cheapest experiment
that can change the successor's thesis.

- Add a per-agent heat state to `che/env/`: accumulate from adjacency to
  Burning cells, decay slowly, and let it reduce move success probability
  (sample the uniform unconditionally, compare against a heat-dependent
  threshold, so nesting stays bitwise at κ_C = 0).
- Log the new co-active counter (heat-elevated agent inside a smoke-
  attenuated window) from day one.
- Calibrate κ_C the way κ_B was calibrated: a detection band, a floor,
  a lock. Reuse `che/calibration/`.
- Run ISO vs JOINT with C included, at the CHE design's k and T\*, on the
  same held-out severity. Same blinding machinery, same report script.

**Kill criterion:** if Γ with C included is a null with an exclusion bound
no tighter than CHE's, and the co-active region including heat is visited
as rarely as CHE's, stop here and publish Stage 0 as a short extension or
a workshop paper. Do not build the continuous simulator to chase a null
the grid already excluded.

**Go criterion:** a gap appears with C that was absent without it, or the
survival/task asymmetry changes. That is the successor's headline and it
justifies Stage 1.

### Stage 1 — continuous dynamics, minimal (3 months)

- 2D differential-drive agents in Brax or MJX. Stay in JAX so the PBT/IPPO
  pipeline is reused verbatim.
- The fire CA and the smoke field stay on an underlying grid. This is
  deliberate: the hazard object is identical, so the comparison isolates
  embodiment.
- Sensor model: Beer–Lambert on max range plus a dropout rate and a
  false-near-return rate above a density threshold. Cite a published
  lidar-in-fog model; do not derive one.
- Task: reach and hold waypoints, or transport between stations.
  Achievable by one robot, so coordination stays a choice.
- Rerun ISO vs JOINT. Same design, same power discipline, same floors
  measured on the new artifact.

**Kill criterion:** if the embodied floors are so large that MDE80 exceeds
any plausible effect at affordable k, the paper becomes "the embodied
instrument and its power", which is publishable but should be decided
before Stage 2.

### Stage 2 — decomposition and behaviour (2 months)

- Add embodiment factors one at a time: dynamics only, sensor physics only,
  degradation only. Which one moves Γ. This is the mechanism section.
- Behavioural analysis: distance kept from the front as a function of heat
  state, the dropout rate at which agents slow, retreat events. Two or
  three figures, quantified, floors stated.

### Stage 3 — hardware, optional and detachable (2–4 weeks)

The plan's fog-machine experiment: a scripted policy, fog alone, moving
obstacles alone, both. The claim is non-additivity of failure rate on a
fixed policy. It does not test learning transfer and should not be
described as if it did.

It is a standalone workshop paper whether or not Stages 1–2 happen. Do it
if a room and two robots are available; do not let it gate the RA-L
submission.

## 4. Budget and time, honestly

| stage | GPU | wall time | can stop after |
|---|---|---|---|
| 0 | ~$30 | 2–4 weeks part-time | yes, with a short paper |
| 1 | ~$100 | 3 months | yes, with an instrument paper |
| 2 | ~$50 | 2 months | this is the RA-L paper |
| 3 | $0 | 2–4 weeks | standalone workshop paper |

The full sequence is the plan's nine to twelve months. Stage 0 alone is a
month and answers whether the rest is worth doing.

## 5. What the plan gets right and should keep

- Severity by dynamical phase, reused unchanged. The single most
  reviewer-proof design choice, and it transfers for free because the
  hazard kernel is the same object.
- Nested ablations, bitwise. Every new coupling is a parameter of one
  kernel with unconditional PRNG consumption.
- Distributional metrics: survival, completion conditional on survival,
  CVaR at a stated α, time to first loss.
- The pitfalls section. Especially "no new methodological document after
  the design is registered." This directory is the last one.

## 6. What to fix in `chaos_robotics_research_plan.md`

- §7 step 1 says submit CHE to Swarm Intelligence. The ruled venue is
  TMLR, DMLR fallback.
- Every arXiv identifier in the novelty verdicts is unverified. Vulcan's
  matters most, since it is already named in CHE's related work.
- §3 "Experiment design" step 2 assumes a grid gap exists. Replace with
  the branch table in §1 above.

## 7. Sequence, given a side project and a TMLR submission in flight

1. Submit CHE.
2. Stage 0 while CHE is in review. One month, one number.
3. If Stage 0 says go: Stage 1. If not: publish Stage 0 short, and pick
   4.4 (expendability) as the second paper.
4. Stage 3 whenever hardware is at hand; it is independent.
