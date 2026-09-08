# Branch D — Γ negative on either co-primary

Registered framing (`phase6_framing_branches.md` §3): *not separable from
the matched-budget asymmetry* unless Γ(t) says otherwise.

**No magnitude threshold is registered, and none may be introduced now.**
Γ(t) is the discriminator, and it is the whole of it:

- Γ(t) trending toward zero or positive over the final half →
  **not separable from the matched-budget asymmetry**.
- Γ(t) flat or stably negative over the final half → **a real reversal**.

Neither reading is evidence against composition on its own. Write the
variant that Γ(t) selects; do not blend them.

## Variant D1 — Γ(t) trending toward zero or positive

This is a fixed-budget artifact paper, and it is honest to write it as one.

**Title:** *Matched budget is not matched progress: a pre-registered
compositional test that its own robustness check overturns*

**Abstract sentence:**
> At the registered budget of 1000 updates the jointly trained policy
> trails the isolated-element policy on ⟨metric⟩ by ⟨Γ⟩ (⟨CI⟩), but the
> gap shrinks monotonically over the final half of training
> (⟨Γ(500)⟩ → ⟨Γ(1000)⟩), so the fixed-budget result is reported as not
> separable from the arms' different positions on their learning curves.

**§9 skeleton:**
1. The contrast at T\*, with the sign stated plainly.
2. Γ(t), Fig. 9, as the primary figure of the section. Show the per-arm
   curves too, so the reader sees which arm is still climbing.
3. The registered differential-drift sensitivity (~0.012 per 100 updates,
   local, never a bound) alongside the observed Γ(t) slope. Do not turn it
   into a threshold.
4. What would resolve it: a longer budget on the confirmatory arms.
   ⟨If the T = 2000 subsample was run, this is where it goes and it may
   change the variant.⟩ Otherwise state it as future work with its cost.
5. The registered biases: ISO's inert third inflates Γ, so a negative Γ
   occurred *despite* a bias toward JOINT. Report the direction; it makes
   the fixed-budget reading more puzzling, not less, and the paper should
   sit with that rather than explain it away.

**Discussion:** the methods contribution becomes the headline. The
detectability-relative plateau gate was retired before the grid precisely
because it could not certify; the explicit fixed-budget estimand plus
Γ(t) is what caught this. That is a methodology result worth stating.

## Variant D2 — Γ(t) flat or stably negative

A real reversal. This is the most interesting outcome the design can
produce and the hardest to write without over-interpreting.

**Title:** *Training on co-active stressors hurts: a pre-registered
reversal in a calibrated compound-hazard environment*

**Abstract sentence:**
> At matched budget, the jointly trained policy underperforms the
> isolated-element policy on ⟨metric⟩ by ⟨Γ⟩ (⟨CI⟩, rejecting at
> Šidák-corrected α), and the sign is stable over the final half of
> training; joint exposure to the compound region at training severities
> transfers worse to the held-out near-critical severity than isolated
> exposure does.

**§9 skeleton:**
1. The contrast, both co-primaries. If only one is negative, report the
   other's exclusion bound.
2. Γ(t) with the sign stability shown.
3. **Candidate explanations, each labelled as a hypothesis and none
   tested here:**
   - JOINT trains only at {0.43, 0.70}, both far from criticality; a policy
     specialized to co-activity at super-critical severity (98 % burnt,
     ignition channel self-limited) may transfer worse to the near-critical
     regime than a policy that never specialized. This connects to the
     Coupling A self-limiting finding and is the most defensible reading.
   - ISO sees three times as many hazard-only episodes (the inert δ
     third), which is a different curriculum, not just a smaller one.
   - Floors: JOINT's reproducibility floor grew 5.2× from T = 500 → 1000
     (tier 2); a curriculum that is harder to reproduce may also be harder
     to transfer. Hypothesis only.
4. The co-active visitation and failure-inside-region diagnostics, ISO vs
   JOINT: where does JOINT fail that ISO does not?
5. Secondary sweeps: does Γ go more negative with co-occurrence fraction
   p? If the dose response is monotone in the same direction, that is the
   strongest supporting evidence available and it is still secondary.

**Discussion:** frame as a negative-transfer finding with a named
candidate mechanism and an explicit statement that the mechanism is not
identified. Practitioner reading: co-occurrence in the training
distribution is not automatically protective; severity placement of the
compound episodes may matter more than their presence.

## Required honesty lines, both variants

1. Matched budget, never convergence.
2. Medium siting.
3. δ inert; the composition trained on is A × B × δ-free-riding in JOINT
   and A, B, nothing in ISO. On this branch the asymmetry of *price*
   between arms (spine §9 bias a) is part of the story and must be stated
   before any mechanism.
4. No magnitude threshold was registered or applied.
5. Eval-draw conditioning.

## Reviewer objections and prepared answers

| objection | answer |
|---|---|
| "You just under-trained JOINT." | D1: agreed, and the paper says so; Γ(t) is the evidence. D2: Γ(t) is flat over the final half; the fixed-budget estimand was registered before the grid; a longer budget is future work with a stated cost. |
| "Post-hoc storytelling." | Every mechanism is labelled hypothesis; the branch and its Γ(t) reading rule were registered 2026-08-13; Appendix E. |
| "Why no threshold on how negative counts?" | Registered decision: a threshold on a proxy would be worse than the reading rule on the instrument itself. Declining one pre-grid forecloses inventing one post-grid. |

## What NOT to claim

- D1: not a result about composition at all. Say so.
- D2: not "isolated training is better". One environment, one severity,
  one budget, one task, and a registered bias toward JOINT that makes the
  reversal harder, not easier, to explain.
