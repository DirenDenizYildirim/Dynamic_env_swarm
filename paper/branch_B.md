# Branch B — completion null, survival positive, falsifier PASSES

**Rewritten 2026-09-26, post-unblind.** The pre-unblind version assumed the
survival effect would be read as a *composition* effect; the registered
inert-share rule (§7 ruling proposal 1, 2026-09-18) now forbids that, and the
secondary arms say why. Every number below is measured and committed; the
source of each is listed at the end. The post-unblind stage is in
(2026-09-27): **budget-robustness suffix = "sign unstable over the final
half"** on both co-primaries; High readout null; evals reproduce
bit-for-bit across cards.

The registered text governs where this file differs from it
(`phase6_framing_branches.md` §3–§4b; decision log: §7 PROPOSALS RULING,
PRE-UNBLIND RULINGS, UNBLIND RESULT, SECONDARY RESULT).

---

## 0. What landed

| contrast (θ\*, matched budget T = 1000) | completion | survival |
|---|---|---|
| **Γ = JOINT − ISO**, k = 72 / 72 (confirmatory) | −0.0173, z −1.62, **null**; Šidák CI [−0.0412, +0.0066] | **+0.0096, z +4.43, REJECT**, p = 9.3 × 10⁻⁶; Šidák CI [+0.0047, +0.0144] |
| registered-ladder prefix, k = 60 | −0.0217, z −1.80, null | +0.0104, z +4.67, REJECT |
| **Γ₄ = JOINT − ISO-4**, k = 72 / 20 | −0.0126, null; X₄ = 0.0488 | **−0.0003, z −0.09, null**; CI [−0.0068, +0.0063] |
| **Γ₄′ = JOINT − sweep_c50_p000**, same card, k = 72 / 20 | −0.0247, null | **+0.0013, z +0.41, null**; CI [−0.0056, +0.0081] |
| **B̂ = ISO-4 − ISO** | −0.0046, null | **+0.0098, z +3.39**; 95 % [+0.0041, +0.0155] |
| fire deaths per episode, JOINT − ISO (secondary) | | −0.118, z −4.59 |
| **Γ_H** at High, β = 0.70 (out of family, rule vi) | −0.0079, null; X = 0.0340 | +0.0038, null; X = 0.0254 |
| **Γ(t)** signs, t = 500…1000 (rule iv) | `+ − + + − − − − − − −` → **UNSTABLE** | `+ − − + + + + + + + +` → **UNSTABLE** |

Arm means: completion ISO 0.7772, JOINT 0.7600, ISO-4 0.7726; survival ISO
0.9158, JOINT 0.9254, ISO-4 0.9256, sweep_c50_p000 0.9241.

**Registered falsifier:** |z_c| + z_α = 1.618 + 2.2365 = **3.855 < 4.433** =
|z_s|, margin 0.578 (k = 60: 4.040 < 4.673). Branch B stands; it is not C.

**Registered consequence of Γ₄** (UNBLIND RESULT entry): Γ rejects on
survival and Γ₄'s CI contains 0, so **the survival effect does not survive
the inert-share correction. This is stated in the abstract-level summary;
the label stays B; the text may not call the survival effect a composition
effect.** The same-card replicate Γ₄′ agrees, so the correction does not
rest on a cross-card comparison.

## 1. The claim, as the evidence supports it

**What JOINT's survival advantage is.** ISO spends a third of training on
δ-only episodes, and δ was certified inert in Phase 5, so behaviourally those
episodes carry no active element. They are **fire-only**, not hazard-free:
the fire burns in every episode (D1; the δ-only components run at β 0.43 and
0.70). Removing them (ISO-4) raises survival by the
whole ISO→JOINT gap (B̂ +0.0098 vs Γ +0.0096); training on the stressors
**together** adds nothing detectable on top (Γ₄, Γ₄′ ≈ 0, bounded at ±0.7
points). An independent family of arms on the confirmatory card says the same
thing: across the two secondary sweeps, the **no-element share costs survival**
(γ_n = −0.0237 per unit share, 95 % [−0.0419, −0.0057]), and at ISO's
behavioural empty share of 1/3 that slope predicts ISO-4 − ISO = +0.0079
against the measured +0.0098.

**The asymmetry survives the reattribution.** Every survival-moving contrast
above leaves completion unresolved (Γ, Γ₄, Γ₄′, B̂, γ_p, γ_n all null on
completion). Under a reward that cannot see the hazard (Def. 2) — it sees
*deaths*, through the 0.5 penalty — training exposure to live hazard is paid
back in agents, not task return.

**One-sentence claim:**

> Joint training keeps more of the swarm alive than isolated training at a
> held-out severity, but the advantage is accounted for by the isolated arm's
> fire-only training episodes, not by composition; at matched active share
> composition adds nothing detectable, and every effect of hazard exposure
> lands on survival rather than on the task.

**What composition does show, stated as a tension, not a finding.** At fixed
empty share, moving single-stressor episodes into both-stressor episodes
raises survival across the sweep region (γ_p = +0.0326, 95 %
[+0.0137, +0.0502]) — but that move also raises per-element exposure, which
the simplex does not let the design separate, and it **does not extrapolate**:
the plane predicts JOINT − ISO-4 ≈ +0.033 at full co-occurrence, while Γ₄ and
Γ₄′ measure ≈ 0. A local slope that saturates, reported with its confound;
non-verdict-bearing.

## 2. Title

- *Paid in agents, not in composition: a pre-registered test of joint vs
  isolated training under ambient hazards*
- *What joint training buys under ambient hazards is exposure, and it is
  paid in agents*
- *Compound Hostility: a calibrated environment and a pre-registered test
  that finds exposure, not composition* (spine-style)

Drop the pre-unblind candidates that say "compound hazards cost survival" —
the evidence attributes the cost to exposure share, not to compounding.

## 3. Abstract — the **[Γ]** sentences

> At matched compute, joint training improves survival at the held-out
> severity by 0.96 points (family-wise 95 % CI [0.47, 1.44], Šidák-corrected
> for the two co-primaries) while task completion shows no gain larger than
> 0.66 points at the same level, an asymmetry the registered falsifier
> requires. **The survival
> advantage does not survive the pre-registered inert-share correction:** an
> isolated-training arm without its fire-only episodes matches joint training
> (difference −0.03 points, replicated on the same hardware), and a
> secondary dose design attributes the gap to fire-only training episodes
> rather than to composition. The contrast's sign is not stable over the
> final half of training: the survival gap opens only in the last fifth of the
> budget and is still growing at the matched budget.

Keep the qualifier in the abstract on every revision; it is registered.

## 4. §9 results subsection — skeleton

1. **The confirmatory contrast.** Table §0 rows 1–2, both co-primaries, k = 72
   primary with the k = 60 prefix beside it (UNDERPOWERED-flagged, 60.2 %
   completion power at 0.03; k = 72 gives 71.6 %). Intervals conditional on
   the one 512-episode eval draw (§4b).
2. **The falsifier, shown with its margin** (3.855 < 4.433). The completion
   null as an **exclusion**: JOINT gains at most 0.66 points of completion
   (Šidák upper bound +0.0066). The point estimate is −1.7 points; say so,
   without calling it a loss (it does not reject).
3. **The inert-share correction** — Γ₄, Γ₄′, B̂ side by side. This is now
   the centre of the section, not a footnote. State the registered rule and
   that it was registered pre-unblind (2026-09-18) and ISO-4 run pre-unblind.
   Γ₄′ was proposed after Γ₄ was seen and before its arm was read; say so.
4. **The secondary dose design** (non-verdict-bearing, 95 %, many
   intervals): sweep means; γ_n and γ_p with the simplex caveat; the bound on
   the no-element confound (−0.0119, [−0.0210, −0.0028]) — the confound is
   bounded away from zero; γ_p's failure to extrapolate; completion flat
   throughout; both knees UNDERPOWERED.
5. **Where the survival gap lives:** fire deaths (JOINT − ISO −0.118 per
   episode, z −4.59, secondary). ⟨Collapse deaths, danger-moment channels, if
   graded — out-of-family channels grade nothing without their own floor.⟩
6. **Budget robustness — "sign unstable over the final half"** (rule iv, both
   co-primaries). Survival Γ(t) ≈ 0 through t = 850 (flips at 550, 600), then
   +0.0056, +0.0083, +0.0096 at 900–1000 — the gap **opens late and is still
   growing** at T\* (T = 2000 subsample, descriptive: +0.0159). Report the
   registered verdict first, then the shape; never re-read the rule.
   **Completion leans negative in the second half** (negative from t = 700;
   Šidák CI excludes 0 at t = 750 only, −0.0147 [−0.0283, −0.0010],
   descriptive — no registered test at t ≠ T\*). This is the case the
   pre-unblind file said must be reported if seen: the asymmetry holds at T\*
   (falsifier passes), but "completion unaffected" is not the right gloss —
   "completion unresolved, leaning negative" is. Fig.: Γ(t) both metrics with
   Šidák bands; the single-card curve has identical signs (ruling viii).
7. **The High readout — a-fortiori exclusions** (rule vi): Γ_H completion
   −0.0079 (X = 0.0340), survival +0.0038 (X = 0.0254), Γ_H,4 null on both;
   Γ_H within rerun noise (0.73× / 0.75× floor-basis sd). "No gap larger than
   2.5 survival points at High, even where JOINT trained on the evaluated
   configuration and ISO never saw a composed one." Coupling B is live at
   High and A is marginal (the mirror of Medium) — state it.
8. **T = 2000, descriptive only** (4 seeds): Γ(2000) completion +0.0003,
   survival +0.0159 (95 % [−0.0002, +0.0319]); differential training-surface
   slope per 100 updates, survival 0.0072 → 0.0020, completion 0.0025 →
   0.0038. Cite only for whether the drift persists; never that Γ "holds".
9. **Mediation — VOID, and why.** The realized-dose channel does not vary
   with p (slope −1.0 × 10⁻⁵, CI ∋ 0), because the invariant-#5 counter
   counts Coupling-A-seeded ignitions near agents whether or not Coupling B is
   on; it tracks the A marginal the sweep holds fixed (identification arms
   read 0.80×, their 0.4/0.5 A share).
10. **Reproducibility and hardware.** Seed dispersion over the rerun floor:
    1.12× / 1.09× completion, 1.25× / 1.19× survival (ISO / JOINT); Γ_survival
    is 5.40× the floor-basis sd(Γ). Card diagnostic on seeds 1–12
    (descriptive). **Eval reproducibility is exact:** 4 reps × 2 checkpoints
    bit-identical on the post-unblind card and to the grid's own evals; 280 of
    288 paired cross-card evals identical, max |Δ| 2.4 × 10⁻⁴ (one agent in
    one of 512 episodes).

## 5. Required honesty lines

1. **The inert-share qualifier**, abstract-level (registered).
2. **Matched compute, never convergence** (T\* ruling) + the Γ(t) suffix.
3. **Completion null = exclusion with its bound**, never "no effect".
4. **δ is inert**; the composition tested is A × B.
5. **Medium siting (§4a):** Coupling B's own survival effect at Medium was
   −0.0003; its 8.8-point effect is at High. *The pre-unblind line calling a
   Medium survival effect "a composition effect the single coupling did not
   show" is STRUCK* — Γ₄ and Γ₄′ contradict it.
6. **The death penalty:** the reward sees deaths (0.5 each), not the hazard.
   The asymmetry is between a penalized channel and a rewarded one; write it
   that way.
7. **The endpoint confound** (branch-invariant): JOINT sees each coupling 3×
   as often as ISO; the sweep holds marginals fixed and cannot hold the empty
   share fixed at the same time (the simplex).
8. **Hardware block structure:** Γ on one card; ISO-4 on a second unit of the
   same model; Γ₄′ on the confirmatory card; post-unblind evals on a third
   unit.
9. **Many secondary intervals, none family-corrected.**
10. **The co-active counter** means co-active only in all-on configurations.

## 6. Discussion points

- **Match active share before claiming composition.** Joint-vs-isolated
  comparisons in multi-task RL, domain randomization and curricula rarely
  control how much of training carries the stressor at all. Here that one
  uncontrolled quantity accounts for the whole effect. The ISO-4 arm cost
  20 runs.
- **A registered design caught it.** The inert-share bias was named and its
  reading rule registered before the look (2026-09-18); the confirmatory
  result alone would have been reported as a composition effect.
- **Paid in agents.** Predicted by Def. 2 and seen one level down in Phase 4
  (Coupling B moved survival, not completion). A task-only evaluation would
  have seen nothing here at all.
- **A local composition slope that saturates** — worth a sentence and a
  figure, not a claim.

## 7. Reviewer objections and prepared answers

| objection | answer |
|---|---|
| "Isn't JOINT's gain just more exposure?" | Yes — measured, not conceded: ISO-4 and a same-card replicate close the gap; the dose design attributes it to empty episodes. |
| "You added survival after completion failed." | Co-primary ruled 2026-08-02 with pre-Phase-6 evidence; branches registered 2026-08-13; grid 2026-09-08 → 09-23; unblind 2026-09-26. |
| "The completion null is underpowered." | It is an exclusion (≤ +0.66 points for JOINT), and the falsifier requires it to be tighter than the survival effect in standardized units; shown with margin. |
| "Γ₄ compares two GPUs." | Γ₄′ repeats it on the confirmatory card: +0.0013, null; the replicate difference is −0.0015, [−0.0086, +0.0056]. |
| "The death penalty makes survival rewarded." | Yes; the claim is scoped to penalized vs rewarded channels. |
| "Why not report γ_p as a composition effect?" | It moves per-element exposure with co-occurrence and does not extrapolate to JOINT; reported as a tension. |
| "The survival gap only appears at the end of training." | Yes, and the registered rule says so: sign unstable over the final half. The claim is at matched compute only; the gap was still opening at T\* (T = 2000 descriptive: +1.6 points). |
| "Completion goes negative." | It leans negative from t = 700 and rejects descriptively at one point (t = 750); at T\* it is a null that excludes any JOINT gain above 0.66 points. Reported, not explained away. |

## 8. What NOT to claim

- Not "compound stress is paid in agents" — the registered wording no longer
  holds; it is *exposure*.
- Not "composition does not matter" — Γ₄ and Γ₄′ are exclusions (≈ ±0.7
  points on survival), not absences, and γ_p is a local positive slope.
- Not "composition does not affect the task" — the completion bounds are the
  claim.
- Not the founding hypothesis. Say flatly that branch A did not occur.
- Not mediation — the mediator was blind.
- Not "budget-robust" and not a converged gap — the registered suffix is
  "sign unstable over the final half".
- Not "completion is unaffected" — it is unresolved and leans negative.

## Sources (all committed 2026-09-26)

- `che/bench/results/phase6/unblind/{report.md,unblind.json}` — Γ, k = 72
  and 60, falsifier, secondary metrics, floors, card diagnostic.
- `che/bench/results/phase6/post_unblind_analysis/post_gamma4_t2000.{md,json}`
  — Γ₄, B̂, T = 2000.
- `che/bench/results/phase6/secondary/secondary.{md,json}` — Γ₄′, replicate,
  sweep, plane, knees, mediation.
- `che/bench/results/phase6/post_unblind_analysis/post_evalfloor_gamma_t_high.{md,json}`
  — Γ(t), cross-card check, High readout, eval floor.
- `docs/decision_log.md` — UNBLIND RESULT, SECONDARY RESULT and POST-UNBLIND
  STAGE RESULT entries.
