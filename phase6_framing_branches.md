# Phase 6 — OUTCOME-CONDITIONAL FRAMING REGISTRATION (v2, ratified)

**Status: RATIFIED 2026-08-13** — `docs/decision_log.md`, *PRE-RENTAL
DELEGATION AND RATIFICATIONS*, transcribed in the same session per the
meta-rule (2026-07-28). Written 2026-08-11, **pre-grid and pre-unblind**: the
grid has not run, no Phase-6 outcome mean has been read, and nothing below is
conditioned on one.

**What v2 changed:** §2 is partitioned into two tiers (§6 item 3); branch B
gains a **registered falsifier** (§6 item 1); branch D's qualitative threshold
is **struck** and replaced by the Γ(t) reading rule (§6 item 2); the
Medium-siting limitation is promoted to **branch-invariant** §4a (§6 item 4).
The four branches of §3 are ratified verbatim.

**What it registers:** the *claim the paper makes*, as a function of the
confirmatory outcome — decided before the outcome exists.

**What it does NOT touch:** `m62_report.py::METRICS`, `SIDAK_M`,
`K_CONFIRMATORY`, `T_STAR`, any entry in `docs/locks.yaml`, or any
threshold. No constant is ruled here and no analysis family is enlarged.
**Venue is deliberately not decided** (see §7).

---

## 1. Why this document exists

It closes an open question the project raised against itself and never
answered — `phase6_design_v2.md` §10, *"what an independent reviewer should
attack first"*, item 5:

> **The co-primary's role.** If completion returns null and survival returns
> positive, is the paper's claim the founding one?

Raised 2026-08-02. Unanswered as of this draft.

**The general form of the defect.** Every registered guard in this phase
protects a *statistic*: floors before bars, Šidák before the family, void
rules fixed in advance, outcome means suppressed mechanically until
unblinding. None of it protects the *claim*. Selecting the narrative after
seeing Γ is the same error one layer up — and it is the layer no reviewer
can audit, which is precisely why it has to be self-imposed.

This is the cheapest registration in the phase: it costs $0 and it can only
be written honestly *now*.

---

## 2. What is branch-invariant

Stated first, because it is the larger part of the paper and it does not
depend on Γ at all. Every item below is measured and committed.

**Two tiers, partitioned and counted 2026-08-13 (§6 item 3).** Tier 1 is
environment and measurement contributions that stand alone. Tier 2 is protocol
observations whose contribution status is **venue-dependent** — a D&B reviewer
reads them as findings, an RA-L reviewer may read them as lab notes. The
partition exists so that no reviewer is asked to accept a tier-2 item as a
tier-1 contribution, and so that the claim below is checkable rather than
asserted.

**The check, and its result: "a paper exists on every branch" survives on
TIER 1 ALONE (eight items).** Tier 2 is therefore **additive, not
load-bearing**, and §2 is not overclaiming.

### Tier 1 — stands alone (eight)

| contribution | evidence |
|---|---|
| Severity calibrated to a **measured** critical point, not a knob | β̂_c = 0.500 at L = 64, 512 seeds; `phase2_report.md`, `severity_lock.md` |
| **Bitwise-exact nested ablations** — κ_A, κ_B, δ off recovers the nested model to the bit | invariant #3; `test_nesting.py`, `test_comms.py` golden digest |
| Theory-as-unit-test handshakes | Prop. 3 linear, R² = 0.998 (M3.3); Thm. 1 E2C gate green under the three-condition ruling (M4.2); Remark 2′ VoC monotone 0.0000 → 0.4982 (M5.2) |
| **Coupling A self-limits where the hazard is worst** — seeded ignitions 4.05 / 3.41 / 0.84 across Low/Med/High, a 4.83× fall | `e11_report.md` §2, replicated on m35 |
| Compound hostility is **rare and bursty** — P(zero co-active event) = 0.563 / 0.578 / 0.883; var/mean 1.31–1.40 | `e13_report.md`, `phase4_report.md` Result 4 |
| The near-agent **share is flat** across severity, [0.164, 0.203] — the whole severity response is upstream | `e11_report.md` §2 |
| **Comms certified inert** at swarm scale, via a joint argument | M5.3 (Medium, bounds effect < ~3 pts), M5.3b (High, eliminates connectivity: out-degree 1.01 → 2.99 changes nothing), M5.5 (δ = 1 vs 0 within measured bars) |
| **Perception decay is not behaviourally suppressible** — masking 16–118× concentrated on danger moments | `phase4_report.md` Results 2–3 |

### Tier 2 — protocol observations, venue-dependent (two)

| observation | evidence |
|---|---|
| **Reproducibility floors grow with run length, ordered by curriculum difficulty** — ISO 2.1×, JOINT 5.2× from T = 500 → 1000 | `m62b_report.md` §5; flagged there as environment-native |
| **Detectability-relative gates diverge on improving hardware** — a criterion whose denominator is a floor cannot certify on a perfect instrument | `g1_2_report.md`; T\* ruling §1 |

**None of the above is contingent on Γ.** A paper exists on every branch —
**on tier 1 alone**, which is what makes that sentence a claim rather than a
hope.

---

## 3. The branches

"Positive" and "null" below mean **exactly** what the frozen analysis plan
means: rejection or non-rejection in the confirmatory family
{Γ_completion, Γ_survival} at θ\*, Šidák m = 2, graded on the grid's own
measured per-arm seed dispersion (M6.2b close-out, item 5). **No new
threshold is introduced by this document.**

| branch | completion | survival | headline claim | venue lean |
|---|---|---|---|---|
| **A** | + | + | founding registration, verbatim | RA-L / IROS |
| **B** | null | + | composition is paid in **agents**, not task return | either |
| **C** | null | null | the instrument, and what it excludes | D&B / TMLR |
| **D** | − (either) | | not separable from the matched-budget asymmetry | D&B / TMLR |

### Branch A — both co-primaries positive

**Claim:** joint training on co-active stressors outperforms isolated-element
training at a held-out severity — Γ(θ\*) > 0 at **matched budget**, β = 0.49
held out from both arms.

**Honesty lines, pre-drafted and required:**

1. **"At matched compute", never "at convergence."** T\* ruling §2. The
   fixed-budget estimand is the registered one and is also the
   practitioner-relevant question.
2. **The measurement is conservative on this branch, and say so.** At
   T = 1000 ISO sits at 0.56× its own floor and JOINT at 1.02×
   (`g1_2_report.md`), so JOINT is the arm further from its asymptote. A
   positive Γ measured there is *understated*, not inflated.
3. **δ is inert and is carried for registration fidelity only** — the
   effective composition tested is A × B. Phase 5 established this before
   Phase 6 was designed.
4. **The gap, if real, is produced by a rare-event region.** Co-activity at
   Medium is 0.64 events/episode with P(zero) = 0.578. State the
   distribution, never the mean alone (`phase4_report.md` Result 4).

### Branch B — completion null, survival positive

This is the branch §10 item 5 asks about, and the answer is **no, it is not
the founding claim** — stated flatly rather than finessed.

**Claim:** under a hazard-independent reward (Def. 2), compound stress is
paid in **agents, not in task return**. The composition affects survival
while leaving the task metric unresolvable above its floor.

**Why this is a finding and not a consolation prize — three supports, all
pre-dating the grid:**

1. **It is predicted by the construction.** Def. 2 clause 1 excludes the
   hazard from the reward *and* from every auxiliary cost channel, so the
   only path from hazard to return is death truncating future task return.
   An asymmetry favouring survival is what that construction implies.
2. **It replicates a Phase-4 result one level up.** Coupling B moved
   survival 5–11 points at High with **no completion effect resolvable
   above the reproducibility floor** (`phase4_report.md`, correction
   2026-07-28). Branch B is the same asymmetry at the composition level.
3. **The co-primary was ruled in on exactly this reasoning, before any
   Phase-6 run** — final-five ruling 2 (2026-08-02), justified by M3.5 and
   M4.4 showing couplings move survival while completion sits at floor.
   **That pre-dating is what makes the co-primary an addition rather than a
   rescue, and the paper must show it** — cite the ruling date against the
   grid date.

**REGISTERED FALSIFIER (§6 item 1, ruled 2026-08-13).** The claim is an
**asymmetry**, so its failure mode is a completion null that is an *absence*
rather than an *exclusion* — the distinction branch C already owes, applied
one level up.

> Branch B is claimable **only if** the completion contrast excludes an effect
> as large, in standardized units, as the observed survival effect:
>
>     |z_c| + z_α  <  |z_s|,     z = Γ / sd(Γ) per metric
>
> with `sd(Γ)` the grid's own measured per-arm seed dispersion in the combined
> form and `z_α = 2.2365` the two-sided Šidák critical value at m = 2. **If it
> fails, the result is branch C with an asymmetry the design could not
> resolve — not branch B.**

No constant is invented: `z_α` is the frozen analysis plan's own correction,
and standardized units are used precisely so no cross-metric conversion factor
must be chosen. The reference is survival's **point** estimate because
survival must separately reject to reach branch B at all, so its uncertainty
is already graded there.

**It is inside the grid's resolution and it bites.** At the G1.2 floors,
k = 40 (`sd(Γ)` = 0.00504 completion, 0.00310 survival): a survival effect of
0.010 admits |completion| < 0.0050, and 0.020 admits < 0.0212 (0.0016 and
0.0179 under the §5 ×1.3 inflation). A barely-rejecting survival result
therefore **cannot** support the asymmetry claim, which is the correct
behaviour. Floors are a lower bound on `sd(Γ)`; the grid's own dispersion
supersedes them.

### Branch C — both null

**Claim:** a calibrated instrument for compound hostility, and a set of
nulls it can establish *with measured power* — which is what separates a
result from a failure.

**The null must be quoted as an exclusion, never as an absence.** From the
G1.2 floors: sd(Γ) = 0.00504 completion / 0.00310 survival at k = 40, MDE80
= 0.0155 / 0.0095, k_req = 11 / 5. Carrying the §5 inflation bound below,
the grid resolves roughly a 2-point completion effect. **"No compositional
gap larger than X at matched budget"** is the sentence; X comes from the
grid's own seed dispersion, not from these floors.

Three nulls, each with its own bar: comms inert (Phase 5, joint argument),
κ_B completion-null (Phase 4), Γ null (Phase 6). Plus every item in §2.

**This branch is not RA-L-shaped and the document says so in advance**, so
that discovering it does not feel like a defeat.

### Branch D — Γ negative on either co-primary

**Pre-drafted honesty line, and it is the reason this branch is registered
separately:** the measured differential drift at T = 1000 is **~0.012 per
100 updates** (JOINT 0.02411 − ISO 0.01202, `g1_2_report.md`), i.e. **~40 %
of the 0.03 target effect per 100 updates** (T\* ruling §3) — quoted as a
**local sensitivity estimate**, never as a bound.

**NO MAGNITUDE THRESHOLD IS REGISTERED (§6 item 2, ruled 2026-08-13), and the
draft's "magnitude comparable to that" is STRUCK.** Turning the differential
drift into a threshold on Γ would extrapolate a local training-surface slope
across an **invented horizon**, which is the constant the
numbers-enter-derived sub-rule exists to stop. **Γ(t) is not a proxy for that
quantity — it measures Γ's own trajectory at θ\* directly**, and it is already
mandated (T\* ruling §3). A threshold on the proxy would be strictly worse
than the reading rule on the instrument.

> **Γ(t) IS THE DISCRIMINATOR, and it is the whole of it.** A negative Γ at T
> whose Γ(t) trends toward zero or positive across the final half is reported
> as **not separable from the matched-budget asymmetry**. A negative Γ whose
> Γ(t) is flat or stably negative is reported as a **real reversal**. Neither
> reading is evidence against composition on its own.

**No magnitude threshold may be introduced post-unblind.** Declining one now
is only honest if it also forecloses inventing one later.

---

## 4. The budget-robustness qualifier applies to every branch

Registered already (T\* ruling §3) and restated here so no branch is written
without it:

> The fixed-budget conclusion is **budget-robust iff the sign of Γ is stable
> over the final half of training**. If the sign is still moving at T, **that
> instability IS the finding** and is reported as such.

Mechanism: 11 retained checkpoints, updates 500–1000 at interval 50,
confirmatory arms only, **evaluated post-unblind**. Every branch above gains
"— budget-robust" or "— sign unstable over the final half" as a suffix, and
the suffix is not optional.

## 4a. The Medium-siting limitation applies to every branch

Ruled 2026-08-13 (§6 item 4). The draft stated this on branch B only.

> θ\* is sited at Medium, where Coupling B's own measured survival effect was
> **−0.0003** (`phase4_report.md` Result 1, within noise); its 8.8-point
> effect is at **High**, which is not θ\*. Medium was chosen because both
> couplings clear their *lock* criteria there and it carries the smallest
> floors — **which is not the same as both producing behavioural effects
> there.**

**It is a property of θ\*, not of the outcome.** Stating it only where the
outcome makes it awkward would be **outcome-dependent disclosure** — the exact
defect this document exists to prevent, committed inside the document itself.
Required on A, B and C alike; D inherits it through whichever co-primary it is
negative on.

## 4b. Γ's interval is conditional on the common eval draw

Registered with the grid layout (`decision_log.md`, same entry, ruling 1b) and
restated here because it qualifies every branch's reported interval.

All 240 runs are evaluated on the **same** 512-episode set (eval seed 0). That
is deliberate: the eval draw is then **common-mode and cancels in Γ**, which is
a difference of arm means. The cost is that **Γ's confidence interval reflects
training-seed variance only and does not propagate eval-set sampling.** The
cancellation bounds the damage in the *difference*; it does not licence silence
about the *interval*, so the conditioning is stated wherever the interval is.

---

## 5. Informational — seed dispersion vs the rerun floor

Measured this session on committed Phase-5 evals, per the gap-sizing
authorized in `HANDOFF.md` ("informational and non-verdict-bearing").
Within-arm dispersion only; **no cross-arm quantity is computed and no blind
protocol is touched.** Phase-6 artifacts are excluded.

| cell | metric | seed sd (n) | rerun floor (n = 4) | ratio |
|---|---|---|---|---|
| Medium δ = 0 | completion | 0.0195 (4) | 0.0399 | 0.49× |
| Medium δ = 1 | completion | 0.0131 (4) | 0.0399 | 0.33× |
| Medium δ = 0 | survival | 0.0114 (4) | 0.0130 | 0.87× |
| Medium δ = 1 | survival | 0.0065 (4) | 0.0130 | 0.50× |
| High A_live | completion | 0.0485 (3) | 0.0522 | 0.93× |
| High B_live | completion | 0.0517 (3) | 0.0522 | 0.99× |
| High A_live | survival | 0.0794 (3) | 0.0621 | 1.28× |
| High B_live | survival | 0.0783 (3) | 0.0621 | 1.26× |

Sources: `phase5/m55/eval_{d0.0,d1.0}_s*.json`, `eval_floor_rep*.json`;
`phase5/m53b/eval_{A,B}_live_s*.json`, `eval_floor_rep*.json`.

**Limits, which bound every use of this table.** n = 3–4 on *both* sides, so
each ratio carries roughly ±60 %. Theory requires the ratio ≥ 1.0
(σ²_arm = σ²_rerun + σ²_seed); the sub-1 entries are estimator noise, not
evidence that seeds vary less than reruns. **These are T = 500 artifacts and
the grid runs T = 1000**, where floors are known to grow (M6.2b §5) — the
transfer is an assumption, flagged as one.

**What it supports, and only this:** the registered "83.7 % power is an
UPPER BOUND" caveat has a *bounded* gap rather than an unbounded one — 8 of
8 comparisons land at ≤ 1.3×. Propagating 1.3× through the G1.2 floors moves
completion MDE80 from 0.0155 to ~0.0202; a 2× inflation moves it to ~0.031.
**The design retains ~80 % power at 0.03 even under a doubling.** So a null
on branch C is more likely to be a real null than an underpowered one —
which is scientifically good and strategically uncomfortable, and is stated
in that order.

**This table grades nothing.** It is not a member of the confirmatory
family, it has no per-artifact floor of its own, and the grid's own seed
dispersion supersedes it the moment that exists.

---

## 6. What a reviewer should attack in *this* document

Same discipline as design v2 §10, and by the same author with the same
limited standing to judge it. **All four items below were ruled 2026-08-13**
(`docs/decision_log.md`, *PRE-RENTAL DELEGATION AND RATIFICATIONS*, rulings
3–6) — **pre-grid and pre-unblind**, which is the only time they could be
answered honestly.

1. ~~**Branch B's claim may be unfalsifiable-sounding.**~~ **RESOLVED — a
   falsifier is registered** (§3 branch B): `|z_c| + z_α < |z_s|`, derived
   from the frozen correction with no new constant, and shown to sit inside
   the grid's resolution.
2. ~~**Branch D's threshold is qualitative.**~~ **RESOLVED — a threshold is
   DECLINED with reason** (§3 branch D). Γ(t) measures directly what a
   threshold would only proxy for, and none may be introduced post-unblind.
3. ~~**§2's branch-invariance may be optimistic.**~~ **RESOLVED — §2 is
   partitioned and the claim CHECKED**: "a paper exists on every branch"
   survives on tier 1's eight items alone, so the two protocol observations
   are additive.
4. ~~**The Medium siting.**~~ **RESOLVED — required on every branch** (§4a).
   It is a property of θ\*, not of the outcome.

**Still open for a reviewer, and deliberately unanswered here:** whether the
tier-1/tier-2 partition in §2 lands the same way for an RA-L reviewer as for
a D&B one. That is a venue question, and §7 defers venue on purpose.

---

## 7. Venue is deliberately NOT decided here

The venue choice is legitimately outcome-conditional — branch A is
RA-L-shaped, branch C is not — and the grid is venue-agnostic, so deciding
now would fix the one thing that genuinely should wait. The *claim* is what
cannot wait, and that is what this document registers.

Venue-independent work that binds **before** the rental, unchanged:

1. The three no-scoop checks — **RUN 2026-08-13** (`decision_log.md`,
   *NO-SCOOP CHECKS*). **Verdict: no scoop.** arXiv:2507.10142 turned out to
   be a **survey**, not the memorization-gap theorem the review assumed, and
   a re-aimed search found no subsuming result; the D&B/ICLR census found no
   collision. **The IEEE Xplore query is only PARTIALLY discharged** — Xplore
   needs authenticated access and was not queried; it stays an owner task and
   does not gate the rental.
   **One spine item narrowed:** `JaxWildfire` (arXiv:2512.06102, Dec 2025)
   occupies JAX × wildfire × *single-agent* × fire-fighting, so item 4 is
   reworded to **"JAX × MARL × hazard survival under a hazard-INDEPENDENT
   reward"**. It becomes the nearest neighbour across Def. 2's boundary — a
   better foil than VULCAN, since its reward is a penalty proportional to
   burning cells.
2. This document — **RATIFIED 2026-08-13** (see §8).
3. Repo release hygiene — **DONE 2026-08-13.** `README.md` written; `m06/`
   (47 MB) archived as `tar.zst` + sha256 and **untracked** — its
   `.gitignore` entry had been in place all along and had done nothing,
   because gitignore does not untrack what is already in the index
   (`che/bench/results/phase6/m60/m06_ARCHIVE.md`); `*_console.log`
   generalized in `.gitignore`. **Two limits recorded there:** a clone is not
   smaller (history keeps the blobs; a rewrite is a separate, destructive,
   owner decision), and the phase prompts still sit at the repo root.

---

## 8. Ratification — DISCHARGED 2026-08-13

- **§3's four branches: ratified verbatim.** §6 items 1–4: all ruled (see §6).
- **Transcribed** into `docs/decision_log.md` in the same session, per the
  meta-rule — *PRE-RENTAL DELEGATION AND RATIFICATIONS*. This file binds from
  that entry, not from itself.
- **No constant, config, test or locked value changed with this document.**
  `m62_report.py::METRICS`, `SIDAK_M`, `K_CONFIRMATORY`, `K_SECONDARY` and
  `T_STAR` are untouched. The rules registered in §3 are **reporting rules on
  the existing confirmatory family**, not new members of it — the family stays
  at m = 2 and the correction is not inflated.
- **Decision authority:** delegated by the owner to the builder for the
  pre-rental set, stated reason being bias avoidance. Recorded in the log
  entry with its limits — delegation relocates bias rather than removing it;
  what protects these rulings is that they were made with **no outcome
  visible**, and that each carries the argument against it.
