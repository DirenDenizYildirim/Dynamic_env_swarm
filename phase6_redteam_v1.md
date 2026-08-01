# Phase 6 Design v1 — Red Team Report

Reviewer: RA (internal), 2026-08-01. Target: `phase6_design_v1.md`.
Every number below is traced to a measured artifact in this repo; none is
transliterated from a heuristic (CLAUDE.md numerical sub-rule). Artifact
paths are cited inline so the gate can re-check each claim independently.

**Verdict: do not register v1.** Four of its findings are sound and should
survive into v2. Three defects are fatal as written — one of them repeats,
verbatim, the exact error the Phase-5 report diagnosed one commit earlier.
One further defect is structural (a mathematical impossibility the design
believes it has solved), and one is a physics trap that would likely
produce a null for reasons unrelated to the hypothesis.

The good news is the largest: **the design is rationing the wrong
resource.** A training run costs 257 s and about $0.07. Seeds are nearly
free, and almost every power problem below dissolves for ~$10.

---

## Part 0 — What is right, and should be kept

Stated first because a red team that only attacks is not calibrated.

1. **The marginal-confound insight (§1) is real and important.** Naive
   mixtures do confound co-occurrence with per-element exposure. Catching
   that before registration is the single most valuable thing in the draft.
2. **The ITT/mediation split (§2) is correct.** Co-active visitation is
   endogenous — M4.3 established that policies regulate their own exposure —
   and refusing to regress performance on a realized mediator as if it were
   assigned is exactly right.
3. **The held-out β values are measured, not invented.** β = 0.46 and
   β = 0.60 are both grid points in `results/phase2/estimates.npz`:
   P_span(0.46) = 0.1719, P_span(0.60) = 0.9492, v̂(0.60) = 0.6911 — the
   draft's "v̂ ≈ 0.69" is the measured value. This is the numerical
   discipline the project's rules ask for, and it held.
4. **"Pilot runs are sweep points" (§7)** is good experimental hygiene.

---

## Part 1 — FATAL: the cost and hardware basis is the ÷81 pattern, a fourth time

**§6 opens: "Run plan and cost (measured throughput: 142,421 steps/s, m51d
row A)". §6 also cites "reference config peaks 22.78 GiB on the 5090". §3
requires "all evals on ONE card model (5090)".**

All three are wrong, and the repo already says so.

`results/phase5/m51d/gate_rows_A.md` — the source of 142,421 — is **row A**,
and `results/phase5/phase5_report.md:119` labels it:

> Row A (Phase-0 M0.6 config, today's code): 142,421 steps/s […] **This is a
> drift reference, not the gate** — that config carries `obs_window` 5,
> superseded at M1.2.

Row A runs `m06_probe.yaml`: an **archival** config (`docs/locks.yaml`) with
`obs_window: 5`, placeholder β = 0.35, and **every element switched off**
(κ_A = 0, κ_B = 0, δ = 0). It is not the configuration Phase 6 spends on.

The Phase-5 report then puts the two side by side, under a heading that
names the failure:

> **The budget was computed from the wrong configuration**
>
> | config | rate | GPU-h for 86e9 steps | @$1.00/h |
> |---|---|---|---|
> | row A — `m06_probe.yaml`, obs_window 5 | 142,421 | 167.7 | $168 |
> | **gate config — obs_window 9, autotune on** | **62,084** | **384.8** | **$385** |
> | gate config, autotune off | 3,795 | 6,294.8 | $6,295 |
>
> […] It is the ÷81 pattern a third time: a headline number attached to a
> configuration that is not the one that spends.

**Phase 6 v1 §6 cites row A. That is the ÷81 pattern a fourth time**, and
this time it happens after the rule was written into CLAUDE.md ("Throughput
gates bind to measured training throughput… Measure what actually spends
the budget") and after the report that named it. The overstatement is
**2.29×**.

The memory figure fails identically: 22.78 GiB is row A's peak. The gate
config measures 27.53 GiB stage-one peak, and **~61.6 GiB at compile with
autotuning on**.

And §3's hardware requirement is contradicted outright by the same report:

> **The 5090 is not viable at this configuration.** Autotuning on needs
> ~61.6 GiB at compile against a 5090's 31.8 GiB → OOM. Autotuning off fits,
> at 3,795 steps/s → 6,295 GPU-hours → $2,833. Both fail.

So §3 registers all evaluation onto a card that cannot run the workload, and
§6's memory reconciliation ("[GATE: reconcile with the m51g 28.31 GiB
floor]") is posed as an open question when the answer is already measured
and recorded.

**Why this one matters most:** the project's contribution is *methodological
credibility*. A registration whose cost basis is the very error the previous
phase's report is built around is the most damaging single line in the
document, independent of whether the arithmetic downstream happens to work.

### The correction is good news

Milestone grids do not run the population gate config. They run
single-policy IPPO, and `results/phase5/m55/timings.txt` measures every one
of the twelve M5.5 runs at **256–258 s** (500 updates, Medium, n_envs 256,
RTX PRO 6000). At ~$1/h that is:

| unit | measured | cost |
|---|---|---|
| one 500-update training run | 257 s | **$0.071** |
| 28 runs (v1's plan) | 2.0 h | **$2.00** |
| 140 runs | 10.0 h | $10.0 |
| 200 runs | 14.3 h | $14.3 |

Against a $150–215 project budget. **Compute is not scarce. Seeds are not
scarce. Statistical power was rationed against a constraint that does not
exist.**

*Unresolved and owed to the gate:* v1 never states whether Phase 6 trains
with `ippo.py` (single policy — what every Phase-3/4/5 grid did) or `pbt.py`
(population — the founding architecture, and what the gate config prices).
The two differ by ~12× in cost per run. D2 registers "same architecture/
compute as JOINT", so this is a registration-level omission, not a detail.

---

## Part 2 — FATAL: every bar in §5 is void, because no floor exists where the experiment measures

CLAUDE.md: *"No acceptance threshold enters any script without either a
measured floor for the quantity it grades (cited) or an explicit
UNDERPOWERED flag… Thresholds finer than their instruments are void by
construction."* And: *"Floors are per-metric AND per-hardware facts."*

§5 grades with floors measured at **Medium (β = 0.49)**. The primary
evaluation happens at **θ\*(0.46) and θ\*(0.60)**. No floor has ever been
measured at either.

That would be a stretch even if floors were stable across severity. They are
not — and the repo has the measurement:

| floor (4 identical runs, 512-ep evals) | completion sd | survival sd | source |
|---|---|---|---|
| Medium, 5090 | 0.01454 | 0.01292 | `m51e/reproducibility_floor.json` |
| Medium, RTX PRO 6000 | **0.03994** | 0.01300 | `m55/reproducibility_floor_medium.json` |
| High, RTX PRO 6000 | 0.05218 | **0.06215** | `m53b/reproducibility_floor_high.json` |

Two independent gradients, both large:

- **Across hardware** (Medium): completion moves **2.75×** (0.0145 → 0.0399)
  while survival is unchanged (0.0129 → 0.0130). This is the exact exhibit
  CLAUDE.md cites for the per-hardware rule.
- **Across severity** (same card): survival moves **4.8×** (0.0130 → 0.0621),
  completion 1.3×.

β = 0.60 has P_span 0.9492 — dynamically much closer to High (0.9980) than
to Medium (0.5469). Grading it with Medium's survival floor plausibly
**understates the floor by ~5×**.

**Consequence:** §5's MDEs, its "resolvable" label, and the pilot decision
rule in §7 are all computed against a floor that does not apply where the
measurement happens. Under the project's own rule these are not optimistic
estimates — they are **void**, and a void bar voids a PASS identically.

**Fix (cheap, mandatory, and it must land first):** a floor-measurement
milestone at both evaluation points, on the card that will run the grid.
4 identical reps × 2 severities × (ISO, JOINT) = 16 runs ≈ **68 min ≈ $1.14**.
No bar may be written before it lands.

---

## Part 3 — FATAL: k = 4 seeds is roughly 5× too small, and the design believes seeds are expensive

For a two-arm contrast with k seeds per arm, sd of the difference of arm
means is σ√(2/k); a 2σ bar gives **MDE = 2σ√(2/k)**. (Note in passing: M5.5
graded at 2×σ *without* the √(2/k) term — worth reconciling in the analysis
plan, since it is conservative by a factor of √(k/2).)

Using the floors measured on the card that can actually run this:

| metric / severity | σ | k=4 (v1) | k=10 | k=20 | k=30 |
|---|---|---|---|---|---|
| completion, Medium | 0.0399 | **0.0564** | 0.0357 | 0.0252 | 0.0206 |
| survival, Medium | 0.0130 | 0.0184 | 0.0116 | 0.0082 | 0.0067 |
| completion, High | 0.0522 | 0.0738 | 0.0467 | 0.0330 | 0.0269 |
| survival, High | 0.0621 | **0.0878** | 0.0556 | 0.0393 | 0.0321 |

Against v1's own stated reference effect sizes:

- **Completion effects historically ≤ 0.03.** At k = 4 the MDE is 0.0564.
  **The founding primary metric is unresolvable at the registered seed
  count** — by a factor of ~2. v1 half-sees this ("MARGINAL → carries an
  UNDERPOWERED flag") but then registers k = 4 anyway. A metric that is
  guaranteed to be flagged underpowered before a single run is not a
  primary endpoint; it is a void test with a label.
- **Survival coupling effect at High, measured at the Phase-4 close: −8.8 pt.**
  At k = 4 the High MDE is 0.0878 — the effect and the detection threshold
  are the same number, i.e. ~50 % power. v1 calls this range "resolvable".
  It is not; it is a coin flip.

v1's §5 asks the right question ("is 4×7 the right shape, or fewer points ×
more seeds?"). Given Part 1, the answer is neither — **it is the same number
of points with 5× the seeds**, because seeds cost $0.07:

- completion at Medium needs **k ≈ 20–30**
- survival at High-like severity needs **k ≈ 20–30**
- survival at Medium is fine at k ≈ 10

---

## Part 4 — STRUCTURAL: the matched mixture cannot do what §1 claims, and the draft's own sign check is backwards

§1 defines mixture(p) = {A-only: c−p, B-only: c−p, joint: p, pillar-only:
1−2c+p} at c = 0.5, and asserts that "ONLY co-occurrence varies."

The algebra checks out for the marginals (A marginal = (0.5−p) + p = 0.5,
constant ✓). But substituting c = 0.5 into the filler term:

> pillar-only = 1 − 2(0.5) + p = **p**

So across p ∈ {0, 0.125, 0.25, 0.375, 0.5}:

| p (co-occurrence) | 0 | 0.125 | 0.25 | 0.375 | 0.5 |
|---|---|---|---|---|---|
| pillar-only (no element) | 0 | 0.125 | 0.25 | 0.375 | **0.5** |
| episodes containing any element | 1.00 | 0.875 | 0.75 | 0.625 | **0.50** |

**Filler rises 1:1 with p; it does not fall.** v1's [RT] note reasons aloud
— *"less total stressor time at high p… no — filler falls as p rises"* — and
lands on the wrong sign. At the top of the sweep **half of all training
episodes contain no stressor element at all.**

So the design did not remove a confound; it exchanged one for another. The
naive family confounds co-occurrence with per-element exposure; the matched
family confounds it with **total stressor-episode exposure and no-element
training time**, which halves across the sweep.

### This is not fixable by re-parameterization

For two binary indicators, the 2×2 table has three free cells, and

  P(neither) = 1 − P(A) − P(B) + P(A∧B).

Fix both marginals → **P(neither) must move 1:1 with P(A∧B)**. A fixed-margin
2×2 table has exactly one degree of freedom. No choice of c escapes it, and
moving the manipulation inside the episode (time-gating the elements)
reproduces the identity in the time domain.

**Therefore: a single-knob dose-response on co-occurrence with fixed
marginals is mathematically impossible to run clean.** v1's central
construction promises something no design can deliver, and registering that
promise is what makes it fatal rather than merely imperfect.

The estimand has to change. See Part 6.

---

## Part 5 — SEVERE: the two held-out severities are the two places where composition is weakest

This is the deepest problem, and it comes entirely from the existing locks.

The two elements have **opposite severity gradients**:

**Coupling A weakens as β rises** (`coupling_a_lock.md`):
> Realized seeded ignitions at High are ~5.7× below Low at *every* κ_A […]
> the supercritical primary fire consumes ~98 % of the arena early, so most
> seed attempts land on already-burnt cells […] **at High, structural
> fire-seeding is marginal by construction**, consistent with Prop. 3 making
> Coupling A the *Low/near-critical* regime's storyline.

Low seeded-burnt share **0.763**; High realized seeding **0.78/ep**, below
the [1, 5] band.

**Coupling B strengthens as β rises** (`kappa_b_lock.md`, masked_frac ceiling
as κ_B → ∞):

| severity | masked_frac ceiling | exposed-agent share |
|---|---|---|
| Low | 0.028 | 0.093 |
| Medium | 0.130 | 0.266 |
| High | 0.419 | 0.529 |

Now place the two chosen evaluation points:

| θ\* | P_span | Coupling A | Coupling B |
|---|---|---|---|
| **β = 0.46** | 0.172 (sub-critical, between Low and Medium) | strong | **near-dead** — ceiling between 0.028 and 0.130; at admissible κ_B the observable reads 0.004–0.014 |
| **β = 0.60** | 0.949 (supercritical, between Medium and High) | **marginal** — fuel-limited | strong |

**Neither held-out point has both elements simultaneously live.** And
composition is precisely the claim that co-training on *both* helps at a
point where *both* act. If one element is inert at θ\*, there is nothing to
compose, and Γ(θ\*) ≈ 0 is the expected result **under the hypothesis being
true**.

The severity where both are most jointly active is Medium (β ≈ 0.49) — A's
bands hold at Low *and* Medium, B's ceiling is 10× Low's. Medium is a
training severity, so v1's own rule forbids evaluating there.

**This is a trap, not a detail.** v1 as written has a substantial chance of
producing a null at both evaluation points for a reason that has nothing to
do with compositional generalization, and no post-hoc analysis could
distinguish that from a true null. Registering it would burn the phase.

---

## Part 6 — Proposed v2

Six changes. Total ≈ 200 runs ≈ 14 GPU-hours ≈ **$15**.

### V2-A. Separate the two generalization axes (fixes Part 5)

v1 bundles two independent out-of-distribution moves into one θ\*: held-out
*element combination* and held-out *severity*. Def. 8 bundles them, but the
founding claim is about **composition**, and for ISO the element combination
is **already** out-of-distribution — ISO never trains on co-active A∧B at
any severity. The severity hold-out is a second, harder axis.

Evaluate on both, and rank them:

- **Primary — θ\*_comp at β = 0.49 (Medium).** All elements active; severity
  in-distribution; **element co-activity held out for ISO by construction.**
  This is a genuine compositional-generalization test, and it is sited where
  both couplings are demonstrably live and where the floors are smallest
  (survival 0.0130). Maximum power, mechanism alive.
- **Secondary — θ\*_gen at β = 0.60**, and optionally 0.46. The harder,
  doubly-held-out test. A positive here is the stronger paper; a null here
  with a positive primary is an honest, publishable scope statement
  ("composition transfers across combination but not across phase regime"),
  not a dead phase.

This one change converts the Part-5 trap from fatal to informative, and it
costs nothing.

*If the gate insists on a single held-out severity for registration
fidelity, the least-bad choice is β = 0.52 (measured: P_span 0.8047,
v̂ 0.4487) — held out from all three training levels, and closer to Medium's
joint-activity region than 0.60 is.*

### V2-B. Change the estimand; stop promising a clean single knob (fixes Part 4)

Since a fixed-margin 2×2 has one degree of freedom, stop pretending
otherwise and identify the surface instead:

- **Confirmatory primary: the two registered endpoints, ISO vs
  JOINT-classic**, exactly as the founding registration defines them. Clean,
  unconfounded, answers the actual locked hypothesis, and needs no mixture
  algebra.
- **Dose-response demoted to secondary/mechanism**, reported *with* its
  induced covariate stated numerically (the no-element fraction table in
  Part 4 goes in the paper, not in a footnote).
- **Add the identification arm that makes the dose claim defensible:** a
  second sweep at c = 0.4 alongside c = 0.5. Two non-parallel paths through
  the simplex let you regress the outcome on (marginal c, co-occurrence p₁₁)
  jointly and show the effect is carried by p₁₁ rather than by the
  no-element fraction. Three extra cells × k seeds. This is the difference
  between "we noticed a confound" and "we bounded it."

### V2-C. Measure floors where you measure outcomes (fixes Part 2)

New first milestone, before any bar is written: 4 identical reps at each
evaluation configuration, on the grid's card. 16 runs ≈ 68 min ≈ $1.14.
Every threshold in the analysis plan cites one of these, or carries
UNDERPOWERED.

### V2-D. Seeds: k = 20, not 4 (fixes Part 3)

| arm | k | runs |
|---|---|---|
| endpoints (ISO, JOINT-classic) × 2 eval severities | 20 | 80 |
| matched sweep, 5 points, c = 0.5 | 10 | 50 |
| identification sweep, 3 points, c = 0.4 | 10 | 30 |
| floors | 4 | 16 |
| ablation certification table | 3 | 15 |
| **total** | | **191 ≈ 13.6 GPU-h ≈ $14** |

### V2-E. Re-power the pilot, or drop it

v1's pilot is 2 arms × 2 seeds. MDE = 2σ√(2/2) = 2σ: **0.0798 completion**
at Medium, 0.124 survival at High. It cannot clear its own floor under any
plausible effect size, so it will return null essentially regardless of the
truth — and §7 hands that null the authority to **fork the paper**. That is
M5.5's error with much higher stakes: a decision rule finer than its
instrument, which under the project's own rule is void, not failed.

Either run the pilot at k = 10 on the primary endpoint pair only (20 runs,
86 min, $1.43), or drop it — at $14 for the full design, the pilot's original
purpose (protecting a large spend) no longer exists.

### V2-F. Correct the cost/hardware basis (fixes Part 1)

State throughput as measured on the spending consumer and the card that will
run it: **62,084 steps/s** for the population gate config, or **257 s/run**
for single-policy grid runs, with the training procedure (`ippo.py` vs
`pbt.py`) named explicitly. Delete row A's 142,421 and 22.78 GiB. Record the
5090 as excluded with its measured reason. Retire the m51g reconciliation
question as already answered.

---

## Part 7 — Smaller findings

1. **§7 "pilot runs are sweep points" is not quite true.** JOINT-classic is
   {joint: 1.0}; the matched sweep tops out at p = 0.5. JOINT-classic pilot
   runs feed the endpoint contrast only.
2. **The mediation first stage may have no range.** M4.3 showed policies
   regulate their own exposure; if that regulation compresses realized
   co-active visitation across p, the "law" figure has no x-axis. Pre-register
   a check that realized dose varies with assigned p, and a void rule if it
   does not — before the figure is built.
3. **The ablation certification table is 15 runs for a property already
   proved by test.** Bitwise nesting is enforced by `test_nesting.py`
   (invariant #3). If the table's purpose is performance-at-each-nested-config
   rather than certification, say so; if it is certification, the tests
   already did it.
4. **Both held-out severities are interpolations** between training levels.
   That is defensible and probably forced (β > 0.70 saturates at P_span
   1.000; β < 0.43 barely burns), but the paper must not phrase it as
   extrapolation to unseen regimes.
5. **The co-primary amendment (§4) is legitimate but load-bearing.** It is
   dated, reasoned, pre-registered, and cited in D6 — genuinely fine. But
   Part 3 shows completion is unresolvable at k = 4, so in practice the
   amendment is what rescues the phase from a metric that cannot be
   measured. Better to state that openly than to have a reviewer notice it:
   with k = 20 completion becomes resolvable and the amendment reverts to
   what it claims to be.
6. **No mixture-training machinery exists.** θ is a frozen dataclass closed
   over by the jitted train function (`ippo.py: make_train_fns(cfg)`,
   `env.py: th = cfg.theta`), i.e. static, not traced. Training on a mixture
   of configs requires either making θ traced through every kernel (a large
   refactor touching the Prop.-1 order and all nesting tests) or — much
   cheaper — **sampling one config per update from the mixture weights and
   cycling precompiled step functions** (≤ 4 compiled variants, `lru_cache`
   already sized for it). The design does not mention this at all; it is the
   largest unstated engineering risk in the plan, and the cheap route should
   be named in the registration.

---

## Part 8 — Recommended gate docket edits

v1's docket has ten items. After this review:

**Newly decided (evidence already exists — remove from the docket):**
- rows C/D memory reconciliation → answered by the Phase-5 report
- hardware → 5090 excluded, measured
- throughput/cost basis → 62,084 steps/s or 257 s/run, measured

**Newly owed (add):**
- **G-A** Training procedure: `ippo.py` or `pbt.py`? (D2 "same compute")
- **G-B** Mixture implementation: per-update config sampling, ratified
- **G-C** Estimand: endpoints-confirmatory + dose-secondary (V2-B)
- **G-D** Evaluation siting: θ\*_comp at Medium as primary (V2-A)
- **G-E** Seed count k = 20 (V2-D)
- **G-F** Floor milestone ordered before any bar (V2-C)
- **G-G** Pilot re-powered to k = 10 or dropped (V2-E)

**Unchanged and still owed:** metric amendment ratification; run length;
analysis plan; budget sign-off.
