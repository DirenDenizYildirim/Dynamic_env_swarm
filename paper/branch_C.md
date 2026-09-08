# Branch C — both null

Registered claim (`phase6_framing_branches.md` §3): *a calibrated
instrument for compound hostility, and a set of nulls it can establish with
measured power.*

This is the **modal branch** by the project's own pre-grid assessment, and
it is the branch the venue ruling was made for. TMLR refuses "not novel"
as a rejection ground and its criteria page treats a systematic robustness
study with actionable insight as sufficient interest. Write to that.

**The null must be quoted as an exclusion, never as an absence.** The
sentence is: *"no compositional gap larger than X at matched budget"*, with
X from the grid's own seed dispersion.

## Also use this file for the failed-falsifier case

Survival rejects, completion does not, but |z_c| + z_α ≥ |z_s|. Report:
survival positive, completion null, **asymmetry not resolvable by this
design**. Do not write branch B's claim. Add the "asymmetry note" below to
§9 item 2.

## Title

- *An instrument for compound hostility, and what it excludes*
- *Isolated stressor training suffices, up to X: a pre-registered null in
  a calibrated compound-hazard environment*
- Lead with the environment; the null is the last contribution.

## Abstract sentence for the **[Γ]** slot

> At matched budget and k = 40 seeds per arm, the jointly trained policy
> and the isolated-element policy are indistinguishable at the held-out
> severity: the contrast excludes a completion gap larger than ⟨X_c⟩ and
> a survival gap larger than ⟨X_s⟩ (80 %-power MDE at Šidák-corrected α,
> from the grid's own seed dispersion), and both signs are ⟨stable /
> unstable⟩ over the final half of training.

## Contribution ordering on this branch

Reorder the spine's list so that the instrument and the four calibration
findings are contributions 1–2, the methodology is 3, and the confirmatory
test is 4 and phrased as *"a well-powered exclusion"*. This branch is
written as a benchmark-and-methods paper with one registered experiment.

## §9 results subsection — skeleton

1. **The contrast**, both co-primaries, with the MDE band drawn on the
   figure so the reader sees what was excludable.
2. **The exclusion bounds.** X_c, X_s computed from the realized sd(Γ) at
   80 % power and corrected α. Compare to the design-stage MDE
   (0.0155 / 0.0095) and to the motivating effect band (~0.03). If the
   realized power against the motivating band is < 80 %, say so and give
   the number; power is reported, not re-engineered.
   *Asymmetry note (failed-falsifier case only):* survival rejects with
   z_s = ⟨·⟩; the completion exclusion bound ⟨·⟩ is not tighter than the
   survival effect in standardized units, so whether the composition is
   paid asymmetrically is left open by this design.
3. **Budget robustness.** Both Γ(t) curves. A null whose sign wanders is
   still a null at T\*; say what the final-half trajectory shows.
4. **Why this null is narrow, stated by the authors first.** Medium is
   where Coupling B measured −0.0003 on its own; the composition tested is
   A × B with B individually quiet. The null is about this severity. A
   High point ⟨was / was not⟩ run; if run, it carries the UNDERPOWERED flag
   and is shown as breadth, never as a second confirmatory test.
5. **Why this null is still informative.** Three nulls now stand, each with
   its own measured bar: comms inert (Phase 5), κ_B completion-null
   (Phase 4), Γ null (Phase 6). The environment has a compound region that
   is visited (0.64 events/episode) and that a policy trained without ever
   seeing it handles as well as one trained on it, up to X.
6. **Registered biases.** ISO's inert third inflates Γ, so a null here is
   a null *despite* a bias toward JOINT, which strengthens it. Say this
   once, without leaning on it. Differential drift: sensitivity estimate.
7. **Secondary sweeps.** The dose response is the most useful figure on
   this branch: if Γ is flat in p as well, the null has breadth in
   co-occurrence fraction even if not in severity.

## Required honesty lines

1. Matched budget, never convergence; a null at T\* is not a null at
   convergence.
2. Medium siting, stated as a limitation of θ\*, not of the outcome.
3. δ inert; composition tested is A × B.
4. Co-activity rare and bursty; ISO's exposure to the co-active region is
   near zero by construction and it still matched JOINT there, up to X.
5. Eval-draw conditioning on the interval.

## Discussion points

- The practitioner-actionable reading: **cheap decompositions may suffice**
  for this class of coupled ambient stressors, at least at near-critical
  severity and this compute. Scope it tightly and say what would move it
  (High severity, longer budget, a coordination-requiring task).
- Prop. 4 bounds what can be guaranteed, not what happens; the honesty
  note in the theory doc already says compositional generalization can
  emerge from isolated training. This branch is that case.
- Methods reading: the pre-registration is what makes this a result. An
  unregistered null of this shape would not be publishable, and the
  paper should say why.

## Reviewer objections and prepared answers

| objection | answer |
|---|---|
| "A null on a toy task is not interesting." | The task is simple by design (reward independence needs a task-only reward); the environment is calibrated to a measured phase; the null is an exclusion with a bound; and three nulls with bars now characterize the instrument. TMLR's criteria page: systematic robustness study with actionable insight. |
| "Underpowered." | Realized sd(Γ), realized power against the motivating band, and the exclusion bound are all reported. If power is below 80 % against the band, the paper says so in the abstract. |
| "You picked the severity where nothing happens." | Medium was locked 2026-07-19 for lock-criteria and floor reasons, before any composition run, and the limitation is stated on every branch. ⟨High point, UNDERPOWERED, if run.⟩ |
| "Why should I care about the environment?" | The four empty claim-spaces in related work; the calibration findings; the exact ablations; the methodology. |

## What NOT to claim

- Not "composition does not matter". Not "ISO is as good as JOINT". Only
  "not distinguishable up to X at this budget and severity".
- Not that the null generalizes to High.
