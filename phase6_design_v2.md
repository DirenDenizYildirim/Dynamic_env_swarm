# Phase 6 Design — v2 (REGISTRATION)

**Status: registration draft, written against a complete ruling set.** Every
constant below either cites a measured artifact or names the ruling that
fixed it. Supersedes `phase6_design_v1.md`, which is retained in the repo as
the reviewed draft together with its red team (`phase6_redteam_v1.md`) and
the remedy options (`phase6_redteam_remedies.md`).

Rulings incorporated: **PHASE-6 REMEDY RULINGS** (2026-08-02, four decisions)
and **PHASE-6 RULINGS, FINAL FIVE** (2026-08-02), both in
`docs/decision_log.md`, plus two dated amendments registered there.

> **Author caveat, stated up front and not withdrawn.** This document was
> drafted by the same agent that produced the red team and proposed the
> remedies it now adopts. That is the failure mode this project keeps
> catching — an author checking their own work. **§10 lists what an
> independent reviewer should attack first.** One item in §5 is already an
> instance: writing the power section correctly overturned a number this
> document's own author supplied to the gate.

---

## 0. What is being tested

Founding registration (`docs/architecture_decisions_v1.md`): a policy
trained on the individual compound-stressor elements *and* on jointly-trained
combinations of them outperforms, at the full joint combination, a policy
trained on each element in isolation. **Γ(θ\*) > 0**, completion primary.

D6 upgraded the binary to a dose-response. Post-Phase-5 state: the elements
are **{Coupling A (κ_A = 0.06), Coupling B (κ_B = 1.0), comms denial
(δ = 1.0)}**, with comms **certified inert** (M5.3/M5.5) and retained in θ\*
for registration fidelity at zero cost.

---

## 1. Protocols and configurations

**Training severities: {β = 0.43 (Low), 0.70 (High)}, uniform.**
**Held-out severity: β = 0.49**, which is θ\*'s. *(Remedy ruling 1.)*

Why the middle is held out rather than an interpolated point: the two
couplings have **opposite severity gradients**. Coupling A is "marginal by
construction" at High — the supercritical fire consumes the fuel collapse
would ignite (`coupling_a_lock.md`) — while Coupling B's masking ceiling runs
**0.028 / 0.130 / 0.419** across Low / Medium / High (`kappa_b_lock.md`). The
v1 candidates 0.46 and 0.60 each had **one element effectively inert**, so
Γ ≈ 0 was the expected outcome *even under a true hypothesis*. Medium is the
only severity where both couplings satisfy their own lock criteria, and it
carries the **smallest measured floors** of the three cells.

β = 0.49 needed no new calibration: Phase 2 measured it at 512 seeds
(P_span 0.547, burnt fraction 19.8 %, L = 64). Registered as its own locked
constant `beta_holdout` — numerically equal to `beta_medium` but a different
role, so a future re-siting moves one without the other.

### The three element configurations

| name | κ_A | κ_B | δ |
|---|---|---|---|
| A-only | 0.06 | 0 | 0 |
| B-only | 0 | 1.0 | 0 |
| δ-only | 0 | 0 | 1.0 |
| all-on (joint) | 0.06 | 1.0 | 1.0 |

All carry the locked remainder: `r_comm` 16, `death_penalty` 0.5, obs v3,
64², 12 agents, horizon 256, `n_envs` 256, `rollout_len` 128.

### ISO (D2) — 6 components, uniform
{A-only, B-only, δ-only} × {0.43, 0.70}, weight 1/6 each. Each element is
seen **only in isolation**.

### JOINT-classic — 2 components, uniform
{all-on} × {0.43, 0.70}, weight 1/2 each. These are exactly
`joint_low.yaml` and `joint_high.yaml`.

**The endpoint pair is deliberately unmatched in per-element marginal** (1/3
in ISO vs 1 in JOINT) — that is how the founding registration defines the
contrast, and v1 registered it the same way. The marginal question is
answered separately, by the sweep, precisely because the two cannot be
answered by one arm (see §2).

### θ\* — the evaluation point
`che/configs/theta_star_holdout.yaml`: all-on at β = 0.49. Neither protocol
trains on this severity.

> **Design property, stated rather than left for a reviewer:** training now
> spans sub- and super-critical only, so the **near-critical regime is the
> test point** and no training data sits near criticality.

> **Trap, and it is enforced by test:** `joint_medium.yaml` must **not** be
> trained on — it is θ\*'s severity, and training on it would destroy the
> held-out property Γ depends on.

---

## 2. The estimand, and the confound that forced it

*(Remedy ruling 2.)*

**The confound is structural, not an algebra error.** For two binary
elements, P(neither) = 1 − P(A) − P(B) + P(A∧B). Fixing both marginals
**forces** P(neither) to move 1:1 with co-occurrence — a fixed-margin 2×2
table has exactly one degree of freedom. At v1's c = 0.5 the no-element
share is exactly *p*, so at p = 0.5 **half of all training episodes contain
no stressor at all**. No re-parameterization escapes this, so the estimand
changes rather than the mixture.

### Confirmatory (verdict-bearing)
**ISO vs JOINT-classic at θ\***. Unconfounded, needs no mixture algebra, and
answers the founding hypothesis verbatim.

### Secondary — dose-response (labelled, non-verdict-bearing)
5-point matched sweep at c = 0.5, p ∈ {0, 0.125, 0.25, 0.375, 0.5},
**with the induced gradient stated numerically in the paper, not a
footnote**:

| p (co-occurrence) | 0 | 0.125 | 0.25 | 0.375 | 0.5 |
|---|---|---|---|---|---|
| no-element share | 0 | 0.125 | 0.25 | 0.375 | 0.5 |
| episodes with any element | 1.00 | 0.875 | 0.75 | 0.625 | 0.50 |

### Identification arm
Second sweep at **c = 0.4**, p ∈ {0, 0.2, 0.4}, where the no-element share is
0.2 + p. Two **non-parallel** paths through the simplex make marginal and
co-occurrence separately identifiable, so the confound is **bounded** rather
than merely acknowledged.

**Both sweeps vary A and B only; δ stays off.** Comms is certified inert, so
including it would multiply components without adding information, and the
sweeps are secondary. Consequence, stated: the sweep's p = 0.5 arm is **not**
JOINT-classic (which carries δ = 1.0). They are different arms answering
different questions.

---

## 3. Metrics

*(Final-five ruling 2.)*

- **Completion — primary**, for the task-performance claim (founding
  registration, unchanged).
- **Survival — registered co-primary**, for coupling and composition claims.
  Justification pre-dates Phase 6: M3.5 and M4.4 showed both couplings move
  survival while completion effects sit at or below reproducibility floors
  (D6 addendum).
- **Secondary, reported and floor-graded, never verdict-bearing alone:**
  deaths by cause, co-active visitation, danger-moment channels, delivery
  rate, realized mixture weights.

**What makes the amendment an addition rather than a substitution: k = 20.**
At k = 4 the founding primary was unresolvable by MDE before a single run, so
a co-primary would have been a rescue wearing an addition's clothes. See §5
— including a correction the gate should read.

---

## 4. The floor milestone (M6.2) — runs before any bar exists

*(Remedy ruling 4; final-five ruling 1a and 3.)*

**8 reps × 3 arms {ISO, JOINT-classic, sweep p = 0.5} = 24 full runs with
evals**, on the card that runs the grid.

- **Per-arm, because floors are per-artifact** (CLAUDE.md, adopted
  2026-08-02): ISO and JOINT are different artifacts with potentially
  different stability, so a floor measured on one may not grade the other.
  Floors for intermediate sweep points are **assumed common and that
  assumption is flagged**; the sweep is not verdict-bearing.
- **8 rather than 4:** M5.5 recorded that n = 4 leaves the sd uncertain by
  ~±40 % (3 dof). Every threshold in the phase rests on these numbers and
  the extra 4 reps cost ~$1.
- **This is also the shakedown** that the dropped pilot used to provide: 24
  full runs end-to-end with evals. **Any process surprise STOPs the phase.**
- **Plateau check:** final-100-update slope against zero, floor-graded. If
  the headline configs are still climbing at 500 updates, **STOP and
  re-rule** (final-five ruling 3).
- **It also measures the eval cost**, discharging the estimate in §6.

---

## 5. Power — and a correction the gate should read before proceeding

Floors in hand (Medium, RTX PRO 6000, 512-episode evals, `m55` /`m53b`):
**completion σ = 0.0399, survival σ = 0.0130.** These justify the seed
count; the **actual bars come from M6.2**.

With Šidák at m = 2 (family α = 0.05 → per-comparison α = 0.02532,
z_crit = 2.2365):

| metric | k | sd of Γ | detection threshold (50 % power) | **MDE at 80 % power** | power at a 0.03 effect |
|---|---|---|---|---|---|
| completion | 20 | 0.01262 | 0.0282 | **0.0388** | **55.6 %** |
| completion | 34 | 0.00968 | 0.0216 | **0.0298** | 80.6 % |
| survival | 20 | 0.00411 | 0.0092 | 0.0127 | > 99 % |

> ### ⚠ CORRECTION OWED TO THE GATE
>
> **k = 20 was ruled on a number this document's author supplied, and that
> number was a detection threshold, not a power calculation.** The remedies
> table quoted "completion MDE 0.0252 at k = 20", computed as 2σ√(2/k) — the
> project's customary 2σ bar. That is the effect size at which one would
> *just* reject, i.e. **50 % power**, and it omitted the Šidák correction the
> analysis plan requires.
>
> Correctly: at k = 20 the completion contrast has **55.6 % power against a
> 0.03 effect**, and reaches 80 % power only at **0.0388** — above the
> historical effect band (≤ 0.03) that motivated the whole seed discussion.
>
> **Survival is unaffected** — its floor is 3× smaller, so it clears any of
> these comfortably.
>
> **The cheap fix, offered not assumed:** raise k on the **two confirmatory
> arms only** (where Γ_completion is graded) to **k = 34**, leaving the
> non-verdict-bearing sweeps at k = 20. That is **+28 runs ≈ 2.0 GPU-h ≈
> $2**, and it puts completion at 80.6 % power against a 0.03 effect.
>
> **This document registers k = 20 as ruled.** The amendment above is a
> proposal, not an edit — it needs a ruling, and the honest reading of the
> founding primary metric depends on it.

Caveat that applies either way: "historical effects ≤ 0.03" is an upper
bound on *observed* completion effects in earlier phases, not a prior on the
true effect at θ\*. It is the best anchor available and it is what the seed
count is calibrated against.

---

## 6. Run plan and cost

**Correct basis.** A 500-update single-policy run measures **257 s**
(`results/phase5/m55/timings.txt`, RTX PRO 6000). The gate config measures
**62,084 steps/s** (Phase 5) and **60,037 steps/s** re-measured at M6.0.
**Row A's 142,421 steps/s is not a valid basis** — it is `m06_probe.yaml` at
obs_window 5 with every element off, which `phase5_report.md:119` labels "a
drift reference, not the gate". v1 used it; that is the ÷81 pattern's fourth
appearance. **The 5090 is excluded** (~61.6 GiB at compile vs 31.8 GiB).

| arm | points | k | runs |
|---|---|---|---|
| ISO | 1 | 20 | 20 |
| JOINT-classic | 1 | 20 | 20 |
| dose sweep, c = 0.5 | 5 | 20 | 100 |
| identification, c = 0.4 | 3 | 20 | 60 |
| M6.2 floors | 3 arms | 8 reps | 24 |
| **total training runs** | | | **224** |

224 × 257 s = **16.0 GPU-hours ≈ $16** at ~$1/h. Evaluation adds materially
and is **estimated, not measured** — M6.2 discharges that estimate. Budget
**~$25 with margin**, against a project budget where the binding constraints
were always wall-clock and statistical power, not money.

*(With the §5 amendment: 252 runs, ~18 GPU-h, ~$27.)*

**No pilot** (final-five ruling 1): a pilot cannot protect a spend smaller
than itself.

---

## 7. Analysis plan (frozen)

*(Final-five ruling 4.)*

- **Confirmatory family:** {Γ_completion, Γ_survival} at θ\*, **Šidák
  m = 2**, bars from the **M6.2 per-arm floors**.
- **Secondary, labelled non-verdict-bearing:** isotonic dose-trend on the
  c = 0.5 sweep; bootstrap-over-seeds knee CI with an **automatic
  UNDERPOWERED flag if the CI spans the sweep**; the c = 0.4
  identification-arm confound bound.
- **Mediation, with a pre-registered void rule:** realized co-active
  visitation is endogenous (M4.3 showed policies regulate their own
  exposure), so it is presented as mediation, never as causal regression.
  **If realized dose does not vary with assigned p, the dose figure has no
  x-axis and is declared VOID** — registered now, not decided after seeing
  the first stage.
- **Blind protocol governs: the pipeline is frozen by commit hash before
  unblinding.**
- Every claim carries its floor-grade.

**Post-unblind fork.** The one-paper/two-paper decision is a **framing**
decision at the results-accepted gate, not a spend decision (final-five
ruling 1b). With everything run, it chooses how to write, not what to buy.

---

## 8. What changed from v1, and where each change is registered

| v1 | v2 | ruling |
|---|---|---|
| θ\* at held-out β ∈ {0.46, 0.60} | θ\* at held-out **0.49**; train on {0.43, 0.70} | Remedy 1 |
| Matched sweep primary | **Endpoints** primary; sweep secondary; **c = 0.4 identification arm** | Remedy 2 |
| k = 4 | **k = 20** | Remedy 3 |
| Floors assumed from Medium | **M6.2, 8 reps, per-arm, before any bar** | Remedy 4 |
| Pilot, 2 arms × 2 seeds | **Dropped**; shakedown → M6.2; fork → post-unblind | Final-five 1 + amendment |
| Metric amendment proposed | **Ratified** | Final-five 2 |
| Run length open | **500 updates** + plateau guard | Final-five 3 |
| Analysis sketch | **Frozen family**, blind protocol | Final-five 4 |
| Ablation table, 15 runs | **Cut**, by dated amendment; optional at revision | Final-five 5 + amendment |
| Cost from row A (142,421 steps/s) | **257 s/run measured**; 5090 excluded | Red team Part 1 |
| Mixture machinery assumed | **Built and certified** (M6.0) | M6.0 spike |

---

## 9. Engineering still owed before the grid (M6.1)

The ruled design needs **up to 8 mixture components**; M6.0 certified the
machinery at 2.

1. **Per-component count logging.** `mixture_component` currently logs a mean
   over component *indices*, which reads as a ratio only for two components.
2. **Protocol configs** for ISO, JOINT-classic and both sweep families.
3. **A test that no training config carries β = 0.49** — the `joint_medium`
   trap, enforced rather than commented.
4. Tests for realized per-component weights and training/θ\* severity
   disjointness.

---

## 10. What an independent reviewer should attack first

Ordered by how much damage the finding would do, and written by the author
who has the least standing to judge his own work here:

1. **§5's power correction** — is 55.6 % power on the founding primary
   metric acceptable, or does k = 34 become mandatory?
2. **§1's severity restructure.** Training on the extremes means no training
   data near criticality. Is testing at the near-critical point a strength
   (hardest regime, both couplings live) or a confound (the test point is
   dynamically unlike either training point)?
3. **§2's unmatched endpoints.** The confirmatory contrast differs in
   per-element marginal *and* in co-occurrence. The sweep is supposed to
   separate these — does it, given the sweep is non-verdict-bearing?
4. **§1's δ retention.** Neither protocol trains on δ = 1.0 but θ\* carries
   it. Symmetric, so it should not bias Γ — but it is an unseen element at
   test time for both arms, and that deserves a second opinion.
5. **The co-primary's role.** If completion returns null and survival
   returns positive, is the paper's claim the founding one?
