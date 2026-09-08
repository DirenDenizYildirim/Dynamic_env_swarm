# Branch B — completion null, survival positive, falsifier PASSES

Registered claim (`phase6_framing_branches.md` §3): *under a hazard-
independent reward, compound stress is paid in agents, not in task return.
The composition affects survival while leaving the task metric unresolvable
above its floor.*

**Gate before writing this file:** the registered falsifier must pass:

    |z_c| + z_α  <  |z_s|,   z = Γ / sd(Γ) per metric,   z_α = 2.2365

If it fails, this is **branch C with an unresolved asymmetry**. Go to
`branch_C.md` and use its "asymmetry note". Do not write branch B.

## Title

- *Paid in agents: compound hazards cost survival, not task return, under
  a hazard-independent reward*
- *Where the reward cannot see the hazard, composition is paid in
  survival*

## Abstract sentence for the **[Γ]** slot

> At matched budget, joint training improves survival at the held-out
> severity by ⟨Γ_s⟩ (95 % CI ⟨·⟩, rejecting at Šidák-corrected α) while
> the completion contrast excludes any effect larger than ⟨bound⟩ in
> standardized units, an asymmetry the registered falsifier requires and
> the construction predicts; the survival gap's sign is ⟨stable /
> unstable⟩ over the final half of training.

## §9 results subsection — skeleton

1. **The contrast**, both co-primaries, same table as branch A.
2. **The falsifier, shown.** Report |z_c|, |z_s|, z_α and the inequality
   with its margin. The completion null is an **exclusion** with a stated
   bound, never an absence.
3. **Budget robustness** on survival (Fig. 9). The completion Γ(t) is
   shown too; a completion sign that is drifting toward rejection over the
   final half undercuts the asymmetry and must be reported if seen.
4. **The three pre-dating supports**, each with its date against the grid
   date. This is what makes the co-primary an addition rather than a
   rescue, and the paper must show it:
   - Def. 2 clause 1 predicts the asymmetry: the only path from hazard to
     return is death truncating future task return.
   - Phase 4 showed the same asymmetry one level down: Coupling B moved
     survival 5–11 points at High with no resolvable completion effect.
   - The co-primary was ruled in on 2026-08-02, justified by M3.5 and
     M4.4, before any Phase-6 run.
5. **Registered biases.** ISO's inert third inflates Γ on both metrics;
   ⟨ISO-4 if run⟩. Differential drift: state the sensitivity, not a bound.
6. **Where the survival gap lives.** Deaths by cause (fire vs collapse),
   co-active visitation, failure rate inside the co-active region.
7. **Secondary sweeps**, labelled.

## Required honesty lines

1. Matched budget, never convergence.
2. δ inert; composition tested is A × B.
3. Medium siting: Coupling B measured −0.0003 on survival at Medium alone,
   so a survival effect here is a **composition** effect that the single
   coupling did not show at this severity. State this as the interesting
   part and do not overreach on why.
4. Co-activity is rare and bursty; distribution not mean.
5. **The death penalty.** On this branch the reward *does* carry a
   survival-shaped term (0.5 per death), so "the reward cannot see
   survival" is false as stated. The correct sentence: the reward cannot
   see the *hazard*; it sees deaths. The asymmetry is between a metric the
   reward penalizes (death) and one it rewards (collection). Write the
   discussion in those terms or a reviewer will write it for you.

## Discussion points

- The environment's reward structure routes compound stress into a
  specific channel, and the design measured that channel because two
  earlier phases said it would matter.
- Practitioner reading: a task-only evaluation would have called this a
  null. Survival must be a co-primary in ambient-stressor settings.
- Connects to Coupling B's own signature (survival, not completion) one
  level up.

## Reviewer objections and prepared answers

| objection | answer |
|---|---|
| "You added survival after completion failed." | Ruled in 2026-08-02 with cited pre-Phase-6 evidence; the four branches were registered 2026-08-13; grid ran ⟨date⟩. Appendix E. |
| "A completion null is just underpowered." | It is an exclusion with a stated bound, and the falsifier requires the bound to be tighter than the survival effect in standardized units. Reported with margin. |
| "The death penalty makes survival a rewarded quantity." | Yes. Spine §3 wording change; the asymmetry is between penalized and rewarded channels, and the claim is scoped that way. dp = 0 ablation from Phase 2 shown. |
| "Coupling B is quiet at Medium; what composed?" | That is the point: the single coupling showed nothing here and the composition does. Mechanism limited to Fig. ⟨deaths by cause⟩. |

## What NOT to claim

- Not "composition does not affect the task". It affects it below the
  bound; the bound is the claim.
- Not the founding hypothesis. Say flatly that branch A did not occur.
