# E1.1 — Severity response of co-active visitation

**Status: the pre-registered prediction is REFUTED in its specific form, its
premise is confirmed and quantified, and the milestone produced a stronger
finding than the one it was asked for.**

Work package E1, milestone 1 (`env_native_prompt.md`). Zero compute; Phase
3–5 artifacts only, Phase 6 refused structurally. Instrument:
`che/scripts/e1_severity.py`; data `results/e1/severity/severity.json`.

---

## 1. The prediction, and the verdict

**Pre-registered** in `env_native_prompt.md` at `ce7ec3d`, before any number
below existed:

> Coupling A is "marginal by construction" at High because supercritical fire
> consumes the fuel collapse would ignite, while Coupling B's masking ceiling
> *rises* with severity. **So co-activity need not be monotone in severity —
> and Medium may be its peak.** Medium is also θ\*.

| claim | verdict |
|---|---|
| Coupling A is fuel-limited at High | **CONFIRMED and quantified** — seeded ignitions fall 4.83× from Low to High |
| Co-activity need not be monotone | **Not supported** — it is monotone non-increasing |
| **Medium is the peak** | **REFUTED** — Low and Medium are indistinguishable; neither peaks |

Measured on `m44`, the coupling-enabled (`kbL`) arm, both couplings live:

| severity | co-active / ep | seeded / ep | share |
|---|---|---|---|
| Low | **0.6631** | 4.0527 | 0.164 |
| Medium | **0.6426** | 3.4134 | 0.188 |
| High | **0.1523** | 0.8398 | 0.181 |

Low → Medium is **−0.0205 (0.4× the reference scale)** — inside noise.
Medium → High is **−0.4902 (28.9×)**. Replicated on `m35` (the *Coupling-A*
ablation, obs v2, entirely different policies): Low 0.7070, Medium 0.6943,
High 0.1426, with Low → Medium at 0.2× and Medium → High at 32.5×.

**So the shape is a plateau and a cliff, not a peak.** Low ≈ Medium
(1.03× and 1.02× across the two milestones), and both are ~4.2–5.0× High.

---

## 2. The finding this milestone was not asked for

`co_active = seeded × share`, where `share = P(seeded ignition within
perception range of an alive agent)`. Splitting the response that way:

| quantity | Low | Medium | High | Low/High |
|---|---|---|---|---|
| seeded ignitions | 4.0527 | 3.4134 | 0.8398 | **4.83×** |
| **share** | 0.164 | 0.188 | 0.181 | **0.90×** |
| co-active | 0.6631 | 0.6426 | 0.1523 | 4.35× |

**The entire severity response of co-activity is upstream, in Coupling A's
productivity. The near-agent share is flat.** Across all nine measured cells
in both milestones — three severities × two arms in `m44`, three in `m35` —
the share lies in **[0.164, 0.203]**, a span of 0.040, i.e. about two share
floor-sds. Roughly **one collapse-seeded ignition in five lands within
perception range of a living agent, and that fraction does not care about
severity.**

### And the reproducibility floors say which half the policy controls

From the identical-config replicate sets (the only ones that exist), as
*relative* floors:

| severity | set | rel. floor: seeded | share | co-active |
|---|---|---|---|---|
| Medium | m55, n=4 | **0.22 %** | 9.07 % | **9.04 %** |
| High | m53b, n=4 | **0.35 %** | 10.01 % | **10.08 %** |

`rel(co_active) ≈ rel(share)`, to two decimal places, at both severities —
while `rel(seeded)` is **~40× tighter**. Seeded ignition count is very nearly
a deterministic property of the environment; **all run-to-run variation in
co-activity is inherited from where the agents are.**

That is a statement about which half of the mechanism a policy can actually
move, it was measured rather than assumed, and it is the natural entry point
for E1.2's endogeneity question.

---

## 3. κ_B does not move co-activity, and that is the right answer

`m44`'s κ_B ablation, within severity, on co-activity:

| severity | κ_B on − off | grade |
|---|---|---|
| Low | −0.0312 | NO FLOOR — UNDERPOWERED |
| Medium | +0.0781 | 1.5× reference scale |
| High | −0.0098 | 0.6× reference scale |

Small, and **sign-inconsistent**. The counter is purely geometric — it never
reads smoke or transmittance — so κ_B could only move it *endogenously*, by
changing where agents choose to be. On this evidence it does not, measurably.

**This is what makes the plateau-and-cliff shape coherent with E1.0.** The
prediction expected Coupling B's rising masking ceiling to push the
co-activity peak toward Medium. It cannot: Coupling B governs what agents
*see* of co-active hazard, not how much co-active hazard *exists*. E1.0
established that the counter is an **opportunity** measure; E1.1 confirms it
behaves like one. The two halves of compound hostility are measured by
different channels, and conflating them was the prediction's error.

---

## 4. Floor honesty — what could not be graded, and why

**No contrast in §1–§3 is floor-graded on its own artifact, and none is
claimed to be.**

- **The only identical-config replicate sets in Phase 3–5 are `eval_floor_rep*`
  in m55 (Medium) and m53b (High), n = 4 each.** Both are Phase-5 artifacts.
- **`m44` and `m35` have no identical-rep set at all**, so under the
  per-artifact amendment (2026-08-02) their contrasts *cannot* be floor-graded.
  Every ratio above is therefore labelled **REFERENCE SCALE (cross-artifact)**
  in the instrument's output, not "×floor".
- **There is no reproducibility floor at Low for any artifact.** The
  Low-severity κ_B contrast is reported **NO FLOOR — UNDERPOWERED**.
- **n = 4 leaves an sd uncertain by roughly ±40 % (3 dof)** — the reason M5.5
  bought 8 reps over 4 for the Phase-6 floors. The instrument prints this
  warning next to every floor it reports.

No threshold was invented. Where a grade could not be earned, the output says
so rather than substituting a number.

**Why the headline survives this anyway:** the Medium → High contrast is
**28.9–32.5×** any reference scale available, and it replicates across two
milestones with different obs versions and different policies. A 4× miss in
the floor would not touch it. The Low ≈ Medium claim is the weaker one — it
is a *failure to distinguish* at 0.2–0.4× reference scale, not a demonstrated
equality, and it should be stated that way.

---

## 5. What this says about θ\*, stated without overclaiming

The prompt hoped a Medium peak would give the θ\*-siting ruling an
independent, mechanism-based justification. **It does not, and the honest
version is weaker:**

- Siting θ\* at Medium places it **on the co-activity plateau** — ~4.2× the
  co-activity available at High.
- Siting at **High** would have cut measured compound-hostility opportunity by
  a factor of ~4, which is a real argument *against* the severity the v1
  design nearly chose.
- But co-activity **does not distinguish Medium from Low**, so it cannot be
  cited as singling Medium out. The θ\*-siting ruling's actual justification —
  both couplings satisfying their own lock criteria, and Medium carrying the
  smallest measured floors — stands unchanged and un-reinforced.

---

## 6. STOP

Deliverable was the severity response of co-activity, floor-graded. Delivered,
with the grading limits stated explicitly rather than papered over. E1.2
(endogeneity) is unblocked and not started; §2's variance decomposition is its
natural starting point.

Nothing in `che/env/`, the protocol, `docs/locks.yaml` or any registered
constant was touched.

---

## CORRECTION (same day, found while reading into E1.2)

**Two claims above need correcting. Recorded rather than silently edited.**

### 1. The counter had been analysed before. Part of §1 and §3 is a replication, not a discovery.

The E1 work package states the counter has **"never been analysed"**, and
E1.1 was written on that basis. It is **false**.
`results/phase4/phase4_report.md`, **Result 4 — "coupling-co-active
visitation: first data (Prop.-4 diagnostic)"** already analysed it on exactly
the m44 artifacts used here, and already reported:

- the same six cell means (0.694/0.663 Low, 0.564/0.643 Medium,
  0.162/0.152 High) — E1.1 re-derived them **independently and identically**,
  which is a clean reproducibility check but *not* a new result;
- **"No cross-arm difference at any severity, which is expected: the counter
  is a Coupling-A observable and κ_B does not enter it"** — i.e. §3's κ_B null
  and its explanation were already on record;
- the **inverted severity ordering** and its fuel-exhaustion cause, with the
  same seeded-ignition figures (0.83 at High vs 4.08 at Low).

**What in E1.1 remains genuinely new:** the `seeded × share` decomposition
and the flatness of the share; the relative-floor variance result
(`rel(co_active) ≈ rel(share) ≫ rel(seeded)`); the m35 replication on a
different milestone, obs version and coupling; and the floor grading with its
limits. **The severity ordering and the κ_B null are Phase-4 results,
reproduced.** §1's "refuted" verdict on the pre-registered prediction stands —
but note the prediction was already answerable from Result 4 before E1 began.

### 2. The mean alone is a weak summary here, and Result 4 said so first

Result 4 flagged the distribution as **zero-inflated and over-dispersed**, and
warned that "the mean alone would have been actively misleading". **E1.1 uses
per-file means throughout and did not state this.** Measured now, on the same
cells:

| cell | episodes | mean | P(zero) | q90 | q99 | max | var/mean |
|---|---|---|---|---|---|---|---|
| m44 Low kbL | 1024 | 0.6631 | **0.563** | 2 | 4 | 5 | 1.31 |
| m44 Medium kbL | 1536 | 0.6426 | **0.578** | 2 | 4 | 7 | 1.34 |
| m44 High kbL | 1024 | 0.1523 | **0.883** | 1 | 2 | 3 | 1.40 |
| m55 d0.0 | 2048 | 0.5649 | **0.631** | 2 | 4 | 7 | 1.44 |

**56–88 % of episodes contain no co-active event at all**, and `var/mean` of
1.31–1.44 confirms over-dispersion against a Poisson reference of 1.0.

This does **not** overturn §1–§3: those contrasts compare *means across files*,
and a mean is a legitimate statistic of a skewed variable — the dispersions
they are graded against are dispersions of the same means. But it does mean
**co-activity is a rare, bursty event rather than a steady background rate**,
and any figure in E1.3 must show the distribution, not just the mean.
