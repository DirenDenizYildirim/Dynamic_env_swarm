# Branch A — both co-primaries positive

Registered claim (`phase6_framing_branches.md` §3): *joint training on
co-active stressors outperforms isolated-element training at a held-out
severity, Γ(θ\*) > 0 at matched budget, β = 0.49 held out from both arms.*

This is the founding registration and the least surprising outcome. Write
it **conservatively**: the trivial reading is "training on the test
composition beats training on its marginals", which is the standard prior.
What makes it a finding is the design, the blinding, and the power.

## Title

- *Co-activity matters: a pre-registered compositional gap in a calibrated
  compound-hazard environment*
- Keep a spine title and put the result in the abstract if the gap is
  small.

## Abstract sentence for the **[Γ]** slot

> At matched budget, the jointly trained policy exceeds the isolated-element
> policy on task completion by ⟨Γ_c⟩ (95 % CI ⟨·⟩) and on survival by
> ⟨Γ_s⟩ (⟨·⟩), both rejecting at Šidák-corrected α with k = 40 seeds per
> arm; the sign of both gaps is ⟨stable / unstable⟩ over the final half of
> training.

## §9 results subsection — skeleton

1. **The contrast.** Table: arm means, seed sd, Γ, sd(Γ), z, corrected
   p, for both co-primaries. State that sd(Γ) is the grid's own seed
   dispersion, not the launch-batch floor.
2. **Against the design-stage MDE.** Where does ⟨Γ⟩ sit relative to
   MDE80 = 0.0155 / 0.0095? If below, say the effect is real but smaller
   than the design was built to find, which is a legitimate outcome.
3. **Budget robustness.** Fig. 9. If sign-stable: "budget-robust". If
   unstable: the instability is the headline of this subsection, and the
   fixed-budget conclusion is reported as fixed-budget only.
4. **The registered biases, quantified.** (a) ISO's inert third: ⟨ISO-4
   arm if run⟩; otherwise state the direction (inflates Γ) and that no
   correction is applied. (b) Differential drift: JOINT is the arm further
   from its asymptote, so Γ at T\* is *understated* on this branch.
5. **Where the gap lives.** Prop. 4's measurement corollary: co-active
   visitation and failure rates inside the co-active region, ISO vs JOINT.
   This is the mechanism figure. Show the distribution.
6. **Secondary sweeps.** Dose response at c = 0.5 across p; identification
   arm at c = 0.4. Labelled non-verdict-bearing, UNDERPOWERED flag where the
   MDE exceeds the effect band.

## Required honesty lines (registered, verbatim in spirit)

1. "At matched compute", never "at convergence".
2. The measurement is conservative: ISO at 0.56× floor, JOINT at 1.02× at
   T = 1000, so the gap is understated if anything.
3. δ is inert and carried for registration fidelity; the composition tested
   is A × B.
4. The gap, if real, is produced by a rare-event region: 0.64 co-active
   events/episode, P(zero) = 0.578. Distribution, never the mean alone.
5. Medium siting (spine §10 item 1).

## Discussion points

- Compositional generalization in *dynamics* is not free even when
  per-element marginals are matched; DBCA's compound-divergence framing
  predicts this and the result instantiates it in MARL.
- Practitioner reading: cheap decompositions do not suffice; train on
  co-occurrence. Scope it to this environment and this severity.
- The effect is on both survival and completion, unlike Coupling B alone
  (survival only). Discuss why composition reaches the task metric where a
  single coupling did not, without inventing a mechanism.

## Reviewer objections and prepared answers

| objection | answer |
|---|---|
| "Training on the test distribution wins. Trivial." | Marginals are matched; only co-occurrence differs (DBCA). The question had priority holders and no clean instantiation in MARL dynamics. And the outcome was one of four registered branches with three registered as non-confirmations. |
| "ISO wasted a third of its budget on an inert element." | Registered before unblinding as inflating Γ. ⟨ISO-4 arm result⟩ / no correction applied, direction stated. |
| "JOINT was still climbing." | Estimand is fixed-budget, registered pre-grid; Γ(t) sign stability reported; on this branch the drift understates the gap. |
| "One held-out severity." | Spine §10 item 2. |
| "Coupling B does nothing at Medium, so what composed?" | Spine §10 item 1; the co-active region is rare, and Fig. ⟨mechanism⟩ shows where failures concentrate. |

## What NOT to claim

- Not "compound training is necessary for robustness". One environment,
  one severity, one task.
- Not a robotics result. RA-L/IROS is a branch-A-conditional stretch and a
  separate paper.
- No mechanism beyond what the co-active visitation figure shows.
