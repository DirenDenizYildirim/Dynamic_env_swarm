# Phase 6 Design — v1 (RA draft for the entry gate + external red team)

Status: PROPOSAL. Becomes registration only when committed after the gate
session, with rulings applied. Every constant below either cites a
measured artifact or is flagged [GATE] (decision owed) or [RT] (question
posed to the red team).

## 0. What is being tested

Founding registration (docs/architecture_decisions_v1.md): compound
generalization — policies trained with stressor elements jointly
generalize to the full compound at held-out severities better than
policies trained on elements in isolation; Γ(θ*) > 0, completion primary.
D6 (decision_log.md): the binary is upgraded to a dose-response.
Post-Phase-5 state: elements = {Coupling A (κ_A=0.06), Coupling B
(κ_B=1.0)}; comms certified inert (M5.3/M5.5), δ=1.0 retained in θ* for
registration fidelity at zero cost.

## 1. Treatment variable and mixtures — the confound handled first

Naive mixtures {A-only:(1−p)/2, B-only:(1−p)/2, joint:p} confound joint
exposure with total per-element exposure (element marginal = (1+p)/2
rises with p). A dose-response on that family measures "more of
everything," not composition. Design:

- **Primary sweep (marginal-matched):** mixture(p) = {A-only: (c−p),
  B-only: (c−p), joint: p, pillar-only: 1−2c+p} with per-element
  marginal fixed at c = 0.5, so p ∈ {0, 0.125, 0.25, 0.375, 0.5}.
  Across the sweep, each element appears in exactly half of training
  episodes; ONLY co-occurrence varies. Severity marginal uniform over
  the three locked levels in every config (constant across p).
- **Registered endpoints (unmatched, as originally defined):** ISO ≡
  p=0 above (identical to D2's locked ISO); JOINT-classic ≡ {joint:
  1.0}. The founding Γ(θ*) > 0 contrast is evaluated on these two,
  verbatim, so the original registration is answered untouched while
  the matched sweep carries the law-shaped claim.
- [RT] Attack the matched-mixture construction: is pillar-only filler
  itself a treatment (less total stressor time at high p... no —
  filler *falls* as p rises; check the sign and the implied
  total-stressor-exposure gradient and whether it needs reporting as
  a covariate)?
- **MECHANISM NOTE (added 2026-08-01, post-review).** *Mixture machinery
  did not exist at drafting; flagged in review; the M6.0 spike de-risks
  it before registration.* Everything in this section assumes the trainer
  can sample θ per episode from a mixture spec. It cannot: θ is a frozen
  dataclass closed over by the jitted train function, i.e. a compile-time
  constant. M6.0 (authorized pre-gate, `decision_log.md`) makes
  {β, κ_A, κ_B, δ} per-env traced fields sampled at reset/autoreset, and
  reports feasibility + **measured** cost to the gate, so §1 is registered
  against a demonstrated mechanism rather than an assumed one.
  **Fallback if the spike fails: precompiled variants** — sample one
  component per *update* and cycle ≤ 4 precompiled step functions, needing
  no traced θ. **Its granularity cost, recorded now:** the mixture is then
  realized at update rather than episode granularity, so every env within
  an update shares a component and PPO's advantage normalization sees a
  homogeneous batch — a different effective objective from per-env mixing,
  plus ~2.2 % MC error on the realized ratio at 500 updates. Acceptable as
  a fallback, not equivalent to the real thing.

## 2. Causal structure: assigned p is the x-axis; measured dose is the mediator

M4.3 proved policies behaviorally regulate their own exposure; co-active
visitation is therefore ENDOGENOUS — an outcome of training, not an
assignment. Analysis structure:
- **Intent-to-treat (primary):** performance at θ* vs assigned p.
  Clean causal claim; no endogeneity.
- **Dose–mediation (mechanistic, the "law" figure):** realized
  co-active training visitation (logged since M0.3) vs p (first
  stage), and performance vs realized dose (second stage), presented
  as mediation, not as causal regression. The knee, if any, is
  reported on both axes.
- [RT] Is the mediation framing sufficient, or does the dose figure
  need a formal sensitivity analysis to be publishable as "law-shaped"?

## 3. Evaluation: θ* and held-out severity

- θ* = all elements active (κ_A=0.06, κ_B=1.0, δ=1.0) at **held-out**
  β ∈ {0.46, 0.60}: 0.46 sits on the subcritical→near-critical edge
  (ξ growing toward L), 0.60 is mid-supercritical (v̂≈0.69) — one
  interpolation per phase boundary, chosen by phase structure, not
  arbitrarily. Trained-severity θ* evals reported as within-
  distribution reference. [GATE] confirm the two β values.
- 512 stochastic episodes per (checkpoint, eval config), eval seed
  fixed, CRN across arms; all evals on ONE card model (5090) — the
  M5.5 card-reconciliation showed completion floors differ 2.75×
  across cards; floors are per-hardware facts.

## 4. Metrics — the pre-registered amendment, formalized

- **Completion: primary** for the task-performance claim (founding
  registration, unchanged).
- **Survival: registered co-primary** for coupling/composition
  effects. Justification pre-dates Phase 6 by weeks and is cited in
  D6: M3.5 and M4.4 showed both couplings move survival while
  completion effects sit at/below reproducibility floors. Amendment
  is dated, reasoned, and made before any Phase-6 run.
- Secondary (reported, floor-graded, never verdict-bearing alone):
  deaths by cause, co-active visitation, danger-moment channels.

## 5. Power, from measured floors (bars-with-floors rule applied)

Floors (m51e, 5090, Medium, 512-episode evals, stochastic runs):
survival sd_floor ≈ 0.013; completion sd_floor ≈ 0.0145. Seed count 4
per point (registered). Approximate MDE for a two-point contrast at
k=4 seeds, 2σ: survival ≈ 0.018, completion ≈ 0.021.
- Reference effect sizes: High-severity coupling survival effects
  measured at 0.05–0.11 (resolvable); completion effects historically
  ≤ 0.03 (MARGINAL → any completion-based dose claim carries an
  UNDERPOWERED flag unless the measured effect clears its floor).
- **Deterministic-flags option:** [GATE input — rows C/D verdict from
  m51d artifacts: did the flags determinize, at what cost?] If
  determinization costs <10% throughput, headline runs go
  deterministic and the floor becomes seed-variation only (regime
  named per M5.5's rule); MDEs shrink accordingly and get recomputed
  in the registered analysis plan.
- [RT] Check the MDE arithmetic and the seeds-per-point allocation:
  is 4×7 points the right shape, or fewer points × more seeds?

## 6. Run plan and cost (measured throughput: 142,421 steps/s, m51d row A)

- Training: 7 mixture points (5 matched + JOINT-classic + [GATE:
  optional pure-pillar control]) × 4 seeds = 28 runs at headline
  length [GATE: 500 updates as in all phase grids, or longer for the
  headline? — decide against learning curves from the pilot].
- Ablation certification table: the five founding nested configs × 3
  seeds (bitwise-nested; interpretation, not hypothesis).
- Cost at measured rates: ≈ $0.88/run training → ~$40–60 all-in with
  evals and the pilot; memory: reference config peaks 22.78 GiB on
  the 5090 (m51d) — [GATE: reconcile with the m51g 28.31 GiB
  floor — which config hit the wall, and does any Phase-6 config
  match it? Arena-ladder (m51j) data decides; larger-card rental
  remains the fallback that preserves scope].

## 7. Pilot (gates the paper fork)

- p=0 and JOINT-classic, 2 seeds each, full eval battery + θ*.
- Decision rule, registered now: if the endpoint contrast (either
  co-primary) clears its floor OR the co-active mechanism figure
  shows failure concentration (Prop-4 corollary), proceed one-paper
  with the full sweep. If both null AND mechanism flat: convene the
  fork — the environment paper exists in the phase reports; the
  sweep becomes the follow-up.
- Pilot runs are sweep points (nothing discarded either way).

## 8. Analysis pre-registration (sketch; full plan is a gate deliverable)

Primary family = {Γ_completion, Γ_survival, dose-trend (isotonic test
on the matched sweep, survival)} with Šidák correction; knee/changepoint
estimated with bootstrap-over-seeds CI, reported with its
[UNDERPOWERED] flag if the CI spans the sweep; Prop-4 mechanism figure:
failure-location concentration in coupling-co-active states, ISO vs
JOINT. All thresholds cite floors; every claim carries its
replication-floor grade (M5.1 correction, project-wide).

## 9. Enumerated gate docket

(1) mixture family + endpoints [§1]; (2) held-out β [§3]; (3) metric
amendment ratification [§4]; (4) rows C/D + deterministic decision
[§5]; (5) m51g/m51j memory reconciliation [§6]; (6) run length; (7)
pilot decision-rule ratification [§7]; (8) analysis plan [§8]; (9)
budget sign-off; (10) red-team findings adjudication.

## 10. Red-team brief (hand this whole document to the external reviewer)

You are reviewing the headline-experiment design for a project whose
contribution is methodological credibility. Attack, in order of value:
the matched-mixture construction (§1), the ITT/mediation split (§2),
the held-out-severity choice (§3), the amendment's legitimacy (§4),
the power arithmetic (§5), the pilot decision rule (§7), and anything
the structure itself hides. Constants marked [GATE] are undecided —
propose values with reasons. You have no stake in the design surviving.
