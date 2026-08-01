# Phase 6 — remedy options for the red-team findings

**STATUS: RULED 2026-08-02.** The human selected the recommended option in
all four decisions; the rulings are transcribed in `docs/decision_log.md`
under "PHASE-6 REMEDY RULINGS". Selections are marked ✔ below. This document
is retained as the reasoning record, not as an open question.

RA proposal, 2026-08-02. One section per open finding from
`phase6_redteam_v1.md`. Every cost uses the **measured** rate: a 500-update
single-policy run is **257 s ≈ $0.07** (`results/phase5/m55/timings.txt`).
Nothing here is registered until the gate selects.

**Two findings are already closed and need no decision:**

- **Part 1 (cost/hardware basis).** Resolved by measurement. The correct
  figures are **62,084 steps/s** for the gate config (or **257 s/run** for
  single-policy grid runs), not row A's 142,421 — and the 5090 is out
  (~61.6 GiB at compile vs 31.8 GiB). M6.0 re-measured the gate config on an
  RTX PRO 6000 at **60,037 steps/s**, 3.3 % from the Phase-5 record.
- **Part 6 (no mixture machinery).** Resolved by the M6.0 spike: per-episode
  mixtures work, cost ≤ 0.62 % throughput and +30 KB, and the
  precompiled-variant fallback is not needed.

---

## Decision 1 — where θ\* sits (red team Part 5, the scissors)

**The problem.** The two elements have *opposite* severity gradients, from
their own lock records. Coupling A: "at High, structural fire-seeding is
marginal by construction" (seeded ignitions ~5.7× below Low at every κ_A,
because the supercritical fire consumes the fuel collapse would ignite).
Coupling B: masked_frac ceiling **0.028 / 0.130 / 0.419** at Low / Medium /
High. So β = 0.46 has A live and B nearly dead; β = 0.60 has B live and A
fuel-limited. **Neither drafted evaluation point has both elements
simultaneously active** — and Γ(θ\*) ≈ 0 is then the expected result *even
if the hypothesis is true*.

### Option 1-D — retrain on the extremes, hold out the middle ✔ SELECTED
Train on **{0.43, 0.70}**; evaluate at **θ\* = Medium (β 0.49)**.
- Satisfies Def. 8 **literally** — one θ\*, at a severity neither protocol
  trained on — while putting it where both couplings meet their own lock
  criteria (A's bands hold at Low *and* Medium; B's detection band was
  locked on Medium probes at 0.438/0.427).
- **Also fixes half of the power problem for free**: Medium has the smallest
  measured floors of the three (survival 0.0130 vs High's 0.0621).
- Cost: training severity coverage drops to two points. Both protocols lose
  Medium equally, so Γ stays a fair comparison.

### Option 1-A — split the two generalization axes
Primary **θ\*_comp at Medium** (severity in-distribution, but co-active
A∧B is out-of-distribution *for ISO by construction*); secondary
**θ\*_gen at a held-out β** for the harder claim.
- Most robust: a null at the harder point becomes an honest scope statement
  ("composition transfers across combination, not across phase regime")
  rather than a dead phase.
- Weaker headline: the primary Γ is at a trained severity, so "generalization"
  is over elements only, and a reviewer may read that as the easier claim.

### Option 1-B — keep one held-out β, move it to 0.52
Measured grid point: P_span 0.8047, v̂ 0.4487 — between Medium and High and
closer to the joint-activity region than 0.60.
- Minimal change from the draft; still one θ\*.
- A is already weakening at P_span 0.80, so the scissors are reduced, not
  removed. No floor measured there either (Decision 4 covers that).

### Option 1-C — keep 0.46 / 0.60 as drafted
Register unchanged; report the element-strength asymmetry as a limitation.
- Maximum fidelity to the draft; zero redesign.
- Accepts a substantial chance of a null at both points for reasons that
  have nothing to do with the hypothesis, with no post-hoc way to tell the
  two apart.

---

## Decision 2 — the estimand (red team Part 4, the fixed-margin confound)

**The problem.** For two binary elements,
P(neither) = 1 − P(A) − P(B) + P(A∧B). Fixing both marginals forces
P(neither) to move **1:1** with co-occurrence — a fixed-margin 2×2 table has
exactly one degree of freedom. At the draft's c = 0.5 the filler is exactly
p, so at p = 0.5 **half of all training episodes contain no stressor at
all** (the draft's own [RT] note reasons to the opposite sign). No
re-parameterization escapes this; it is structural, so the estimand has to
change rather than the algebra.

### Option 2-A — endpoints confirmatory, dose secondary, + identification arm ✔ SELECTED
- **Primary (confirmatory):** the two registered endpoints, ISO vs
  JOINT-classic, exactly as the founding registration defines them. Clean,
  unconfounded, answers the locked hypothesis, needs no mixture algebra.
- **Secondary (mechanism):** the 5-point matched sweep, reported *with* its
  induced no-element gradient stated numerically in the paper.
- **Identification arm:** a second sweep at **c = 0.4**. Two non-parallel
  paths through the simplex let you regress on (marginal, co-occurrence)
  jointly and show the effect is carried by co-occurrence rather than by
  no-element time. This is the difference between "we noticed a confound"
  and "we bounded it".

### Option 2-B — matched sweep primary, covariate reported, no second sweep
Cheapest honest version: keep the draft's structure, report the gradient.
- Saves ~30 runs (~$2).
- Leaves the confound *acknowledged but unbounded* — a reviewer can ask
  "is your dose effect just less-stressor-time?" and the design has no answer.

### Option 2-C — drop the dose-response entirely
Two endpoints only; all seeds concentrated there.
- Maximum power on the founding claim; simplest possible analysis.
- Abandons D6's dose-response upgrade and the "law-shaped" figure.

---

## Decision 3 — seed budget (red team Part 3)

**The problem.** MDE for a two-arm contrast at k seeds is 2σ√(2/k). Against
the measured floors, k = 4 gives completion MDE **0.0564** vs historical
effects **≤ 0.03** — the founding primary metric is unresolvable *before a
single run*. Seeds cost $0.07 each.

| metric / cell | σ | k=4 | k=10 | k=20 | k=30 |
|---|---|---|---|---|---|
| completion, Medium | 0.0399 | 0.0564 | 0.0357 | **0.0252** | 0.0206 |
| survival, Medium | 0.0130 | 0.0184 | 0.0116 | 0.0082 | 0.0067 |
| survival, High | 0.0621 | 0.0878 | 0.0556 | 0.0393 | 0.0321 |

### Option 3-A — k = 20 uniformly ✔ SELECTED
≈ 191 runs ≈ 14 GPU-h ≈ **$15**. Completion becomes resolvable at Medium
(0.0252 < 0.03); survival has margin everywhere.

### Option 3-B — k = 30 endpoints / k = 10 sweep
Concentrates power on the confirmatory claim (completion MDE 0.0206) and
accepts a coarser dose curve. Similar total cost.

### Option 3-C — k = 10 uniformly
≈ $8. Survival fine; completion MDE 0.0357 stays marginally above the
historical effect band, so completion claims would still carry
UNDERPOWERED.

---

## Decision 4 — the floor milestone (red team Part 2)

**The problem.** Every bar in the draft grades against **Medium** floors
while the evaluation happens where **no floor has ever been measured**, and
floors move **4.8×** across severity (survival 0.0130 → 0.0621) and **2.75×**
across cards (completion 0.0145 → 0.0399). Under bars-with-floors those bars
are **void, not merely optimistic**.

All options run **before any bar is written**, on the card that will run the
grid, and now also record **per-artifact self-floors** (the amendment adopted
2026-08-02) rather than floors taken on a reference.

### Option 4-C — 8 reps per evaluation config ✔ SELECTED
≈ 32 runs ≈ 2.3 GPU-h ≈ **$2.30**. M5.5 flagged that **n = 4 leaves the sd
uncertain by ~±40 %** (3 dof); 8 reps roughly halves that. Since every
threshold in the phase rests on these numbers and they cost ~$2, buying the
tighter estimate is the cheapest risk reduction available anywhere in the
design.

### Option 4-A — 4 reps per evaluation config
≈ $1.15, matches the M5.5/M5.3b precedent exactly. Inherits the ±40 %
uncertainty, which then propagates into every bar.

### Option 4-B — 4 reps at the primary evaluation config only
Cheapest. Leaves any secondary evaluation point ungraded, i.e. its bars
would be void by the same rule that motivated this milestone.
