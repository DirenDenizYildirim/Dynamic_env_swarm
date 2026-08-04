# E1.2 — Is co-active visitation endogenous?

**Status: the milestone's motivating premise is retracted, and on independent
evidence the answer is NO — co-activity is not measurably policy-driven. That
negative has a concrete, actionable consequence for the Phase-6 grid, stated
in §5.**

Work package E1, milestone 2 (`env_native_prompt.md`). Zero compute; Phase 3–5
artifacts only, Phase 6 refused structurally. Instrument
`che/scripts/e1_endogeneity.py`; data `results/e1/endogeneity/endogeneity.json`.

---

## 1. The premise this milestone was given is retracted

The work package motivates E1.2 with: *"M4.3 established that policies
regulate their own exposure… Co-active visitation is therefore endogenous."*
It also, correctly, instructs us to read the retraction first. Having read it:

`phase4_report.md` **Result 3 — "the provisional perception-exposure finding
does NOT survive"**. Two independent controls fail it:

- **Training length.** The 3× suppression at Medium that motivated the finding
  is a **200-update transient**; by 500 updates trained policies sit at or
  *above* the random-policy masked-frac ceiling at every severity.
- **The κ_B = 0 control.** At Low and Medium the *uncoupled* arm is **less**
  exposed than the coupled one — the opposite of what perception-driven
  regulation predicts. At High the coupled arm is less exposed but also loses
  8.8 points of survival, and the metric averages over *alive* agents, so
  losing the most-exposed agents lowers it mechanically. Conditioning on
  zero-death episodes is a collider and retains two different populations.

The ruling restated it as a fire-avoidance byproduct and concluded:
**"perception attenuation is not behaviourally suppressible — the swarm cannot
position its way out of it, and pays in survival."**

**So E1.2 may not lean on M4.3.** The "therefore endogenous" step in the
prompt does not follow, and this milestone has to answer the question on its
own evidence.

---

## 2. Test 1 — seed dispersion vs reproducibility, on the same artifact

This is the identifying test, and unlike E1.1's contrasts it is a **genuine
floor grade**: both sides share a config hash (asserted by the instrument, not
assumed), so the comparison is within one artifact.

- `eval_floor_rep*` — identical config, identical seed → **nondeterminism**.
- `eval_<arm>_s<N>` — same config, **different training seeds** →
  nondeterminism **+ which policy you got**.

If policy identity moves co-activity, seed dispersion must exceed the floor.

| pair | severity | quantity | seed sd | repro sd | ratio |
|---|---|---|---|---|---|
| m55 / d0.0 | Medium | co-active | 0.06729 (n=4) | 0.05376 (n=4) | **1.25×** |
| | | share | 0.02032 | 0.01575 | **1.29×** |
| | | seeded | 0.01660 | 0.00754 | 2.20× |
| m53b / A_live | High | co-active | 0.00963 (n=3) | 0.01698 (n=4) | **0.57×** |
| | | share | 0.01089 | 0.02034 | **0.54×** |
| | | seeded | 0.00298 | 0.00293 | 1.02× |

**No endogeneity signal.** At Medium seed dispersion is 1.25× the floor; at
High it is **below** it (0.57×). Different training seeds produce policies
whose realized co-activity is not distinguishable from the same policy rerun.

**Honest limits, and they are severe.** n = 3–4 per side, so these ratios are
variance ratios on 2–3 degrees of freedom and carry enormous uncertainty; the
sd estimates themselves are good to roughly ±40 %. **This is a failure to
detect, not a demonstration of absence.** What it does rule out is a *large*
effect: policy identity does not dominate co-activity the way severity does
(where E1.1 measured ~30× the reference scale).

---

## 3. Test 2 — same weights, one input cut

`m55`'s `muted_s<N>` evaluates **the same checkpoints** as `d0.0_s<N>` with the
message channel cut at eval time — identical weights, identical config hash,
a single input changed. Any difference is behaviour and nothing else, and it
pairs by seed.

| seed | co-active, live → muted | delta |
|---|---|---|
| 0 | 0.6191 → 0.6094 | −0.0098 |
| 1 | 0.6270 → 0.5879 | −0.0391 |
| 2 | 0.5020 → 0.5527 | +0.0508 |
| 3 | 0.5117 → 0.5410 | +0.0293 |

**Paired mean +0.0078, which is 0.15× this arm's own reproducibility floor**,
with deltas in both directions. Cutting the comms channel does not change
realized co-activity — consistent with comms having been certified inert
(M5.3/M5.5), and a useful check that this instrument would have shown a
behavioural change had one existed.

---

## 4. Test 3 — do training treatments move it?

Each contrast graded on the **pooled seed dispersion of its own two arms** —
the dispersion the contrast actually has, per the contrast-SE rule adopted
2026-08-03.

| contrast | Δ co-active | Δ share | grade |
|---|---|---|---|
| m55 Medium: δ 0.0 → 1.0 | −0.0054 | −0.0013 | 0.1× pooled sd |
| m53b High: A_live → B_live | −0.0059 | −0.0061 | 0.7× / 0.6× |
| m44 Low: κ_B 0 → locked | −0.0312 | −0.0065 | 0.3× |
| m44 Medium: κ_B 0 → locked | +0.0781 | +0.0230 | 1.4× |
| m44 High: κ_B 0 → locked | −0.0098 | −0.0134 | 0.7× / 0.8× |

**Nothing moves it.** Every contrast is ≤ 1.4× its own pooled seed dispersion,
and the signs are inconsistent across severities for the one treatment tested
at all three. **No training treatment available in Phase 3–5 — comms denial,
message-content arm, or Coupling-B strength — measurably changes realized
co-active visitation.**

Taken with E1.1, the picture is coherent: co-activity is
`seeded × share`; `seeded` is a near-deterministic environment quantity
(relative floor 0.22–0.35 %); and the `share` sits at ~0.17–0.20 regardless of
severity, treatment, or policy.

---

## 5. What this means for Phase 6 — a registered guard is likely to fire

**Design v2 §7 pre-registers a void rule:** realized co-active visitation is
presented as *mediation*, and *"if realized dose does not vary with assigned
p, the dose figure has no x-axis and is declared VOID."*

**E1.2 is advance evidence that this rule will fire.** The argument is
structural, not merely empirical:

1. At θ\* **all elements are on**, so `seeded` is fixed by the environment —
   E1.1 measured its relative floor at 0.22–0.35 %, i.e. essentially constant.
2. Realized co-activity at θ\* can therefore only vary through the **share**.
3. The share is what Tests 1–3 find **not measurably movable** by policy
   identity, by an eval-time input change, or by any training treatment tested.

The Phase-6 sweep varies the training *mixture*, which is a broader
intervention than anything tested here, so this is a warning rather than a
verdict — but the mechanism by which a dose response would have to appear is
the one channel that this milestone finds inert.

**Recommended, and explicitly not a re-ruling** (E1 is not a protocol
milestone and must not become one): the dose figure's first-stage check —
does realized dose vary with assigned p? — should be run **as soon as the
confirmatory arms are unblinded**, before any effort is spent on the
isotonic-trend and bootstrap-knee machinery §7 registers downstream of it. If
it voids, that machinery is never needed. This costs nothing and is a
sequencing note, not a design change.

---

## 6. The answer, stated precisely

**Is co-activity endogenous? On the available evidence, no — with the
precision the evidence supports:**

- It is **not** the case that policies measurably regulate their co-active
  exposure. The claim that they do rested on M4.3, which is retracted, and
  three independent tests here find no replacement for it.
- Co-activity is **environment-determined to first order**: set by Coupling
  A's productivity, which is near-deterministic, times a share that is
  near-invariant across every condition measured.
- The residual variation that does exist is **nondeterminism, not policy
  choice** — seed dispersion does not exceed the reproducibility floor.
- **This is a failure to detect at n = 3–4, not a proof of absence.** A small
  endogenous component is entirely consistent with these data.

**The mediation framing is preserved throughout and no causal regression was
run.** Realized co-activity is an outcome of the policy; regressing anything
on it would identify nothing. Every number above is descriptive.

---

## 7. What could not be measured, and why

**The within-run training trajectory of co-activity is not measurable from
committed artifacts.** The prompt asked whether co-activity changes over
training and told us to check what the logs actually carry rather than assume.
Checked, across **all 92 Phase 3–5 training `.jsonl` files**:

| channel | in training logs |
|---|---|
| `completion`, `survival_rate`, `deaths_fire`, `deaths_collapse`, `mean_smoke_exposure`, losses | 92 / 92 |
| `delivery_rate`, `mean_out_degree` | 45 / 92 |
| **`coupling_co_active`** | **0 / 92** |
| `seeded_ignitions`, `collapse_events`, `danger_agents`, `masked_danger_sum` | **0 / 92** |

**Invariant #5 is half-satisfied, and this is worth recording as an
engineering finding.** The counter *is* emitted by the env `info` dict from
day one exactly as instructed, and the eval harness *does* consume it into
every `.npz`. The **training logger never picked it up.** So the counter is
available per-episode at evaluation and nowhere per-update during training —
which is precisely the retrofitting problem the invariant was written to
prevent, surviving at a different layer.

Answering the training-trajectory question needs new runs. **The work package
forbids new compute, so it is not answered here and is not worked around.**
Whether to add these channels to the training logger is an engineering
decision for a human; it is cheap to do before the grid and impossible after.

---

## 8. STOP

Deliverable was endogeneity evidence with the mediation framing explicit.
Delivered — as a negative, with its limits stated. E1.3 (figures + drafted
section) is unblocked and not started.

Nothing in `che/env/`, the protocol, `docs/locks.yaml` or any registered
constant was touched.
