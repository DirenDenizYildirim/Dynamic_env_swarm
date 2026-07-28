# Architecture Decisions — Compound Hostile Environment Swarm Robotics Project

**Purpose of this document:** a running record of the design decisions made while
reworking the original ICRA/IROS gap-hunting Cowork prompt, so they can be
cascaded into a rewritten Stage 0 (and the rest of the pipeline) without having
to re-derive the reasoning each time.

---

## 1. Starting point

Original prompt used **three co-equal, independently-tunable stressor axes**:
1. Structural/physical instability
2. Degraded/denied inter-agent communication
3. Distributed passive hazards (**static** — fixed lethal/disabling elements)

Goal for this revision: make the "hostile environment" as hostile as it
realistically gets, without turning it into an adversarial-pursuer design
(which was explicitly out of scope from the start).

---

## 2. Real-world grounding exercise

Rather than invent new stressors from scratch, we pulled recurring stressor
patterns from real hostile-environment robotics domains: urban search & rescue,
underwater/deep-sea, planetary/space, wildfire response, nuclear/contamination
zones, arctic/polar, underground mining.

Recurring threads identified that weren't already covered:
- **Sensory/perceptual denial** (dust, smoke, darkness, turbidity, whiteout) —
  the single most consistent stressor across every domain surveyed.
- **Resource/energy attrition** (battery/fuel scarcity compounding over mission
  duration) — changes problem character (long-horizon decay vs. moment-to-moment
  danger). *Considered but ultimately not carried forward as a separate axis.*
- **Dynamic/evolving hazards** — the existing "distributed passive hazards" axis
  was static in the original design, but every real-world analogue (fire, flood,
  ice cracking, gas dispersion) evolves on its own timeline, independent of
  agent behavior. Identified as the most interesting upgrade, because a static
  hazard can be memorized as a fixed distribution; an evolving one forces
  generalization to a hazard *dynamic*.

**Decision:** dynamic/evolving hazards was selected as the strongest candidate
and promoted from "axis 3, upgraded" to **the central pillar** of the project,
pending literature validation.

---

## 3. First research pass — findings

A scoped research prompt was run to check literature coverage before locking
the design. Key findings:

- Evolving hazard fields are **well-studied but almost always framed as a
  monitoring/suppression target** (wildfire tracking, gas source localization,
  radiation mapping) — **never as a passive survival stressor** for a swarm
  doing an unrelated task. This distinction was identified as the core reframe
  that makes the pillar novel.
- **Structural-failure → hazard-emergence causal coupling** (e.g. collapse
  triggers gas release/flooding/new fire path) is mature in civil-engineering /
  Na-tech cascading-disaster literature, but **has never migrated into any
  MARL or swarm-robotics benchmark.** Flagged as the strongest single novelty
  candidate.
- **Comms denial + dynamic hazard combined is already precedented** (Haksar &
  Schwager, IROS 2018 — fire spread + restrictive comms, distributed MADQN).
  Not a stretch to combine, but not novel as a standalone pairing either.
- **Sensory/perceptual denial** confirmed as a real, independent gap — distinct
  from comms denial (which perturbs inter-agent messages, not an agent's own
  exteroceptive sensing) and not covered by existing hazard-field framings.
  A natural physical coupling was identified: hazard evolution should degrade
  perception as it progresses (thicker smoke → worse vision).
- Caveat noted: this pass's search budget was exhausted at 18 queries; some
  areas (Isaac Lab/MuJoCo specifics, deeper Chinese-venue coverage) were left
  incomplete and flagged for re-verification.

---

## 4. Resulting architecture (pre-validation)

Rather than 3 or 4 co-equal independent axes, the architecture converged on a
**pillar + two causal couplings + one independent load-bearing axis** shape:

- **PILLAR:** non-adversarial, dynamic/evolving hazard field, modeled as a
  passive **survival** stressor (not a monitoring/suppression target).
- **CAUSAL COUPLING A:** structural/physical failure (collapse, terrain
  give-way) can **seed or intensify** the hazard field. Not two independent
  stressors running in parallel — one causally triggers the other.
- **CAUSAL COUPLING B:** as the hazard evolves, it **degrades agent
  perception/sensing** (smoke thickening, turbidity rising) as a tunable,
  physically-coupled side effect of the hazard's own state — not an
  always-on independent sensory-noise axis.
- **INDEPENDENT LOAD-BEARING AXIS:** degraded/denied inter-agent communication,
  trained jointly (not staged, not ablated in isolation) with the above.
- **Training methodology unchanged:** evolutionary + MARL hybrid, applied
  jointly.

Rationale for demoting structural instability and sensory denial from
"independent axes" to "causal couplings": this is both more novel (the
coupling itself is the confirmed gap) and reduces engineering burden (one
coupled hazard system instead of independently-tunable severity sliders on
every axis) — which also strengthens the feasibility story for a solo
researcher on moderate cloud compute.

---

## 5. Extreme-search validation pass — result: **GO (conditional)**

A harder, adversarial six-agent validation pass (126 searches total) was run
specifically to try to kill this architecture before committing to it.
Headline result: **GO**, on the right claim, with two binding conditions.

| # | Claim | Verdict |
|---|---|---|
| 1 | Causal Coupling A is a genuine open gap | **CONFIRMED OPEN** |
| 2 | Causal Coupling B is a genuine open gap | **CONFIRMED OPEN** (narrower — a novel combination, not a new primitive) |
| 3 | Comms-denial + dynamic hazard is novel *on its own* | **PARTIALLY CLOSED — do not lean on this claim** |
| 4 | No existing system combines all four elements jointly | **CONFIRMED OPEN — this is the load-bearing claim** |
| 5 | System is buildable solo, moderate cloud budget, ICRA/IROS timeline | **CONDITIONAL — feasible only on an abstract vectorized-grid path, not 3D** |

### Two binding conditions attached to the GO

1. **Rest the novelty on the causal couplings and the compound system, not on
   comms+hazard.** Comms denial is a load-bearing stressor axis the system is
   stress-tested against — not itself the novelty claim. The contribution is
   the two causal couplings (A and B) and their joint composition into one
   trained environment.
2. **Scope to an abstract vectorized-grid simulator from day one**, not
   photorealistic 3D. Viable path: **VMAS or JaxMARL** as the swarm-MARL
   substrate, with a GPU cellular-automata hazard kernel ported from
   **PyTorchFire or JaxWildfire**, and collapse / perception-degradation /
   comms-denial implemented as grid-state coupling functions. Estimated
   ~5–10 person-months, fits on a single 4090/A100. This is an **engineering
   risk, not a novelty risk** — the couplings are equally novel in 2D as in 3D.

### The validated novelty statement

> The first trained multi-agent reinforcement-learning environment in which a
> non-adversarial physical hazard acts as a passive survival stressor that is
> causally coupled to the environment on two axes at once: a structural
> failure can seed or intensify the hazard field, and the hazard's own
> evolving state degrades agent perception as a tunable side effect — with
> degraded inter-agent communication as an independent, jointly-trained
> load-bearing axis, optimized by an evolutionary+MARL hybrid.

The load-bearing claim is specifically **Coupling A** (structural failure →
hazard emergence inside a trained MARL environment) — confirmed absent from
every benchmark surveyed, English and Chinese, including the nearest
neighbors (RoboCupRescue, HAZARD, Vulcan).

### Open tripwires (not yet fully closed — watch these)

- A handful of Chinese-language sources were never fully read (four
  paywalled CNKI/Wanfang items, one robots-blocked Zhihu column) — titles
  suggest generic MARL/evacuation scope, not compound disaster coupling, but
  this is the one place the load-bearing claim could still be overturned.
- Whether the coupled CA-hazard grid can be kept GPU-batched inside
  VMAS/JaxMARL at swarm scale on a single GPU is an **unverified performance
  assumption** — if it fails in prototyping, scope must drop further (fewer
  agents, smaller grid), which is a schedule risk, not a novelty risk.

---

## 6. Target venue and timeline

- **ICRA 2027** (deadline ~Sept 15, 2026, ~2 months out from decision point) —
  ruled out as too tight for a near-zero-prototype project with a novel
  training loop.
- **Target: RA-L with IROS 2027 presentation option.** IROS 2027's main paper
  deadline is confirmed for **March 1, 2027**; the RA-L+IROS option deadline
  historically lands roughly one week earlier (**estimated late Feb 2027,
  not yet officially posted for this cycle**). This gives **~7 months** from
  the decision point, working near-full-time.
- Build order (Phase 0–7, see below) mapped against this timeline is tight but
  plausible, with Phases 0–3 alone serving as a fallback smaller-scope
  submission if later phases slip.

### MVP / build order (locked)

| Phase | What gets built | Why this order |
|---|---|---|
| 0 — Substrate | VMAS/JaxMARL + evolutionary+MARL hybrid training loop, no hazards yet | Validates the hardest engineering risk (the hybrid loop) before any domain complexity |
| 1 — Static hazard (control case) | Fixed hazard field baseline | Doubles as the paper's control condition |
| 2 — Dynamic hazard (pillar) | CA fire-spread kernel ported in (PyTorchFire/JaxWildfire) | Confirms the pillar is genuinely different from Phase 1 before adding couplings |
| 3 — Coupling A | Structural collapse seeds/intensifies hazard | The single load-bearing novelty claim — validated in isolation first |
| 4 — Coupling B | Hazard state degrades perception | Second novel coupling, validated in isolation |
| 5 — Comms denial | Independent tunable axis, jointly trained | Precedented mechanism (Haksar & Schwager) — lowest risk, goes last |
| 6 — Full compound system + severity sweep | All stressors/couplings jointly trained | The paper's headline system |
| 7 — Ablations | Isolate each stressor/coupling vs. joint training | Directly proves the core hypothesis (joint beats isolated-then-combined) |

---

## 7. Compute budget (cost-constrained revision)

Throughput benchmark anchor: published JAX-based MARL environments run
**~50,000–150,000 steps/sec on a single A100** once JIT-compiled and
vectorized, depending on per-step complexity (CA hazard physics + collapse +
perception/comms coupling logic sits mid-range, not toy-gridworld-fast).

**Key cost-cutting decisions**, given independent/self-funded constraints:

1. **Phases 0–5 are build/debug checkpoints, not publication-grade
   experiments.** Single seed, no population — just confirming each mechanism
   behaves correctly before the expensive runs.
2. **Only Phase 6 (severity sweep) and Phase 7 (ablations) need full
   statistical rigor** — these generate the actual paper results.
3. **Severity sweep trimmed from 5 levels to 3** (low/medium/high) — still
   shows a trend, half the runs.
4. **Ablations trimmed to 5 essential configs**: no-Coupling-A,
   no-Coupling-B, no-comms, static-hazard-trained-then-combined (the direct
   hypothesis test), and full joint. Extra combinations deferred to
   future work, not blocking submission.
5. **Population size cut from ~30 to 10–15** — a legitimate, citable
   methodology choice for compute-constrained solo research. Seeds were
   **not** cut (kept at 3) — seeds are what reviewers check for statistical
   validity; population size is the more defensible place to economize.
6. **Spot/interruptible vast.ai pricing** instead of on-demand (typically
   50–80% cheaper), acceptable given periodic checkpointing.

### Revised budget

| Phase | Configs | Population | Steps/config | Subtotal |
|---|---|---|---|---|
| 0–5 (dev/debug) | ~6 | 1 | ~50M | ~0.3B |
| 6 — Compound system + severity sweep | 3 severities × 3 seeds = 9 | 12 | 300M | ~32B |
| 7 — Core ablations | 5 configs × 3 seeds = 15 | 12 | 300M | ~54B |
| **Total** | | | | **~86B steps** |

At ~100,000 steps/sec on a single A100: **~65 GPU-hours total.**
At vast.ai spot pricing (~$0.25–0.45/hr for A100): **~$16–$30 raw compute**;
budgeting ~2x for failed runs/debugging/hyperparameter search gives a
realistic total of **~$50–$150** for the whole project — self-fundable on an
independent budget.

**Caveats:**
- Throughput and total-step estimates could be off 3–5x in either direction;
  the real number should be measured empirically after Phase 0–1, not trusted
  from this armchair estimate.
- This assumes the PBT-style evolutionary+MARL hybrid (population trains
  continuously, mutated periodically) rather than pure evolution-strategies-
  on-weights, which would need substantially more samples.

---

## 8. Core hypothesis (locked)

Two possible framings were considered for "transfer to novel combinations":

- **Reading 1 — Compositional generalization:** train on the 4 individual
  elements (and jointly-trained combinations of them), test on the full joint
  combination never seen jointly during training. Coherent with the existing
  build plan (Phase 6 = full joint system, Phase 7 = isolated-vs-joint
  ablations).
- **Reading 2 — Zero-shot stressor generalization:** hold out one entire
  element from training, test whether the policy handles it anyway. A bigger,
  riskier claim, but conflicts with the Phase 6 plan (full system trained on
  all four elements jointly) and isn't buildable within the current
  timeline/budget with only 4 building blocks.

**Decision: Reading 1 locked as the paper's hypothesis. Reading 2 deferred to
the paper's future-work section, not claimed in this cycle.**

**Final hypothesis statement:**

> A swarm policy trained via an evolutionary+MARL hybrid on the individual
> compound-stressor elements (structural-triggered hazard emergence,
> hazard-driven perception decay, comms denial) — and on jointly-trained
> combinations of them — will achieve higher task-completion rates under the
> full, novel joint combination of all elements at test time than a policy
> trained on each element in isolation and only combined at evaluation.

**Primary success metric:** task completion rate under compound stress, at
held-out severity levels and the never-jointly-trained full combination.

This hypothesis is directly tested by the already-locked Phase 7 ablations
(isolated-vs-joint comparison) and instantiated by the Phase 6 full-compound
system — no changes needed to the MVP, timeline, or compute budget already
locked above.

---

## 9. Status / next step

All three goal-setting pieces are now locked: **scope (Phase 0–7 MVP)**,
**timeline (RA-L + IROS 2027, ~7 months)**, and **hypothesis** (compositional
generalization, task-completion-rate metric). Ready to cascade all of this
into a rewritten Stage 0 (and propagate through Stages 1–6) of the original
Cowork pipeline prompt.

**Simulator scope decision (locked):** the rewritten prompt will **not**
hard-lock VMAS/JaxMARL by name. Instead, Stage 4 stays open to propose any
simulator/substrate, but every project must justify its choice against a
stated **abstract-grid / GPU-batched compute ceiling** (i.e. must run at
swarm scale, batched, on a single rented consumer/datacenter GPU, within the
~65 GPU-hour / ~$50–150 compute budget locked in Section 7) — not
photorealistic 3D by default. This preserves flexibility while still
protecting the feasibility constraints already validated.

**All open decisions from the goal-setting phase are now resolved.** Next
step: rewrite Stage 0 (and cascade through Stages 1–6) of the original
Cowork pipeline prompt using everything locked in this document.
