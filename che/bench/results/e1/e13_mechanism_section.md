# DRAFT PAPER SECTION — Compound hostility, measured

> **Status: draft for the paper, produced by work package E1.** Written to be
> lifted into the manuscript, not to be read as a milestone report — the
> milestone report is `e13_report.md`. Every number is measured from
> committed Phase 3–5 artifacts in the E1 session; figures are
> `results/e1/figures/`. Phase-6 data is excluded throughout (§6).

---

## N. What compound hostility is in this environment

The environment's claim on the reader's attention is not that it contains two
stressors. It is that the stressors are **causally coupled to each other
through the task substrate**, so that hostility compounds rather than adds:

- **Coupling A** makes structural collapse *create* hazard: collapse events
  seed ignitions in the fire CA (Def. 5).
- **Coupling B** makes that hazard's smoke *degrade perception of it*, through
  Beer–Lambert transmittance over the agent's observation crop (Def. 6).

Composed, these describe a specific failure mode: **the environment
manufactures a threat in the place where it has simultaneously destroyed the
agent's ability to see that threat.** That is the claim this section makes
measurable.

### N.1 The observable

We log, per step, the number of **collapse-seeded ignitions falling within an
alive agent's perception window** — the `coupling_co_active` counter,
instrumented from the project's first commit precisely so that it would not
have to be retrofitted. The counter is the intersection of Coupling A's output
with Coupling B's domain, and it is a strict subset of the seeded-ignition set
by construction: over the 38,912 evaluation episodes in which both channels
are recorded, the subset relation holds with **zero violations**, and it is
attained (there exist episodes in which every seeded ignition was within
perception range).

Two properties of the counter should be stated before any result rests on it.

**It is an opportunity measure, not a realized-perception measure.** The
counter's radius is the Chebyshev half-width of the observation crop, which
coincides *exactly* with the outer bound of Coupling B's attenuation — a cell
outside the crop is not observed at all, so the binary test is the correct
"could this agent perceive it" boundary. Inside that bound the two differ:
optical depth is `κ_B · d · ρ̄` with `d` **Euclidean**, so across the
outermost shell the optical depth varies by a factor of **1.414** (axis 4.000,
corner 5.657 at the locked window of 9) between cells the counter treats
identically. The counter therefore measures *co-location* — an upper bound on
events that were both co-active and actually perceived. The realized half is
carried by separate channels (`masked_danger_sum`, `danger_agents`).

**It is a count, and a badly behaved one.** Compound hostility in this
environment is **rare and bursty, not a background rate** (Fig. 2):
**56.3 %, 57.8 % and 88.3 %** of episodes at Low, Medium and High severity
contain *no* co-active event at all, while the tail reaches 7 events in an
episode. Variance-to-mean ratios of **1.31–1.40** confirm over-dispersion
against a Poisson reference of 1. Reporting only a mean would misrepresent
the phenomenon as a steady pressure; it is an occasional, concentrated one.

### N.2 The severity response decomposes, and the swarm owns neither half

Co-activity is the product of two mechanisms that can be measured separately:

```
    co_active  =  seeded  ×  share
                    ↑         ↑
     Coupling A's productivity │ the fraction of created hazard
     (how much hazard collapse │ that lands within perception
      actually creates)        │ range of a living agent
```

Across the three calibrated severities (Fig. 1), these behave completely
differently:

| | Low (β=0.43) | Medium (β=0.49) | High (β=0.70) | Low/High |
|---|---|---|---|---|
| seeded ignitions / ep | 4.0527 | 3.4134 | 0.8398 | **4.83×** |
| **share** | 0.164 | 0.188 | 0.181 | **0.90×** |
| co-active / ep | 0.6631 | 0.6426 | 0.1523 | 4.35× |

**The entire severity response lives in Coupling A's productivity.** The
near-agent share is flat: across all nine measured cells — three severities ×
two κ_B arms, plus a three-severity replication on a different milestone with
a different observation schema — it lies in **[0.164, 0.203]**. Roughly **one
collapse-seeded ignition in five lands within perception range of a living
agent, and that fraction is indifferent to severity.**

The mechanism behind the collapse at High is fuel exhaustion: the
supercritical front has already consumed the material that collapse debris
would otherwise ignite, so Coupling A's ignition channel **self-limits exactly
where the hazard is most severe**. The two couplings are therefore strongest
in *different regimes* — which is itself a compound-hostility observation, and
one that constrains where a composition experiment can meaningfully be sited.

### N.3 The swarm does not steer it

It is tempting to read realized co-activity as partly a behavioural choice —
a swarm that positioned itself better would encounter less of it. **We find no
evidence for that, on three independent tests** (Fig. 3).

**Policy identity.** Comparing dispersion across *different training seeds*
against the reproducibility floor from *identical reruns of the same
configuration* — same artifact, same config hash, so this is a genuine floor
grade — gives ratios of **1.25×** (Medium) and **0.57×** (High). Which policy
you obtained does not move co-activity beyond the noise of rerunning the same
policy.

**A behavioural intervention.** Evaluating identical checkpoints with the
inter-agent message channel cut changes realized co-activity by a paired mean
of **+0.008, or 0.15× that arm's own reproducibility floor**, with
seed-level deltas in both directions.

**Training treatments.** Comms denial, message-content ablation, and Coupling-B
strength at three severities all move co-activity by **≤ 1.4× the pooled seed
dispersion of the contrast**, with signs that disagree across severities.

This is consistent with an earlier and independently-derived result in this
project: a provisional finding that policies suppress their own perceptual
exposure did not survive its controls, and was restated as *perception
attenuation is not behaviourally suppressible — the swarm cannot position its
way out of it, and pays in survival.* The present measurements extend that
conclusion from exposure to co-activity.

The variance decomposition sharpens what remains. The relative reproducibility
floors are **0.22 % / 0.35 %** for seeded ignitions against **9.07 % / 10.01 %**
for the share, at Medium and High. Seeded ignition count is very nearly a
deterministic property of the environment; **essentially all run-to-run
variation in co-activity is inherited from where the agents happen to be.**
The share is thus the *labile* half of the mechanism — but labile to
nondeterminism, not, on this evidence, to policy.

### N.4 What this establishes

Compound hostility in this environment is **an environment-determined,
rare, bursty phenomenon whose magnitude is set by the hazard-creation channel
and whose incidence the swarm does not measurably control.** That is a
stronger and more useful claim than "two stressors are present": it is
falsifiable, it was falsified in one of its parts (the swarm-agency part), and
what survives is a property of the environment rather than of any policy
trained in it.

It also constrains the composition experiment. Because Coupling A self-limits
at high severity while Coupling B's masking ceiling rises with it, **the two
couplings do not attain their maxima together**, and a composition test sited
at an extreme severity would be testing a regime in which one of its two
elements is nearly inert.

---

## Limits

Stated here rather than left to a reader to reconstruct.

1. **The counter bounds, it does not resolve.** As established in §N.1, it
   measures co-location within the perception window, not whether the agent
   in fact perceived the hazard. Optical depth varies by 1.414× across the
   outermost shell alone. Every co-activity number in this section is an
   **upper bound** on genuinely co-active-and-perceived events.

2. **The endogeneity result is a failure to detect, not a proof of absence.**
   The comparisons in §N.3 rest on **3–4 runs per arm**, so the variance
   ratios carry 2–3 degrees of freedom and the underlying sd estimates are
   good to roughly ±40 %. These data exclude a *large* endogenous component;
   a small one is entirely consistent with them.

3. **No reproducibility floor exists at Low severity for any artifact**, so
   contrasts anchored there are reported ungraded rather than graded against
   a substitute. Where floors from one milestone are used to scale another
   milestone's contrast, they are labelled a *reference scale*, not a floor —
   floors in this project are per-metric, per-hardware **and per-artifact**.

4. **The within-training trajectory could not be measured.** The counter is
   emitted by the environment and consumed by the evaluation harness, but is
   absent from all 92 training logs, so whether co-activity changes as a
   policy learns is unanswerable from existing artifacts and is not
   speculated about here.

5. **All artifacts here are 500-update checkpoints.** The confirmatory
   experiment runs at twice that length, and training length is known to move
   this environment's dispersion statistics materially. These are 500-update
   quantities.

6. **Phase-6 data is deliberately excluded.** The confirmatory arms are under
   a pre-registered blind protocol; co-activity is an outcome channel of those
   runs, so comparing it across arms before unblinding is forbidden. Nothing
   in this section uses them, and the analysis code refuses those paths
   structurally rather than by convention.

---

## Figures

| file | claim |
|---|---|
| `fig1_mechanism.png` | `co_active = seeded × share`; the severity response is Coupling A's, the share is flat |
| `fig2_distribution.png` | zero-inflated, over-dispersed — rare and bursty, not a background rate |
| `fig3_endogeneity.png` | the endogeneity null, on the same-artifact floor grade and on training treatments |
