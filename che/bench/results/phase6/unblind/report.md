# Phase-6 UNBLIND — confirmatory contrast Γ at θ*, matched budget T* = 1000

artifact: `che/bench/results/phase6/g1_conf_5090`  ·  git: `41b11cd774eb469f05f7b4c40e5bc23c905ccc00` (dirty files: 0)  ·  2026-09-26T17:49:13+00:00

Family {Γ_completion, Γ_survival}, Šidák m = 2, z_α = 2.2365. sd(Γ) is the grid's own UNPAIRED per-arm seed dispersion in the combined form. Intervals are CONDITIONAL on the common eval draw (seed 0, 512 episodes) and carry training-seed variance only.

## PRIMARY — k = 72 (designated pre-unblind)

| metric | ISO | JOINT | sd ISO | sd JOINT | Γ | sd(Γ) | z | p | decision | Šidák CI | exclusion X (MDE80) | power@0.03 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| completion | 0.7772 | 0.7600 | 0.0654 | 0.0627 | -0.0173 | 0.01068 | -1.62 | 0.1056 | null | [-0.0412, +0.0066] | 0.0329 | 71.6% |
| survival_rate | 0.9158 | 0.9254 | 0.0126 | 0.0133 | +0.0096 | 0.00216 | +4.43 | 9.296e-06 | REJECT | [+0.0047, +0.0144] | 0.0066 | 100.0% |

**BRANCH B** — completion null, survival positive, and the registered falsifier PASSES: the completion exclusion is tighter than the survival effect in standardized units.
falsifier: |z_c| + z_alpha < |z_s|  (registered 2026-08-13): 3.855 < 4.433 → passes

## REGISTERED-LADDER PREFIX — k = 60 (seeds 1..60) — UNDERPOWERED flag per branch C as written; realized power stated

| metric | ISO | JOINT | sd ISO | sd JOINT | Γ | sd(Γ) | z | p | decision | Šidák CI | exclusion X (MDE80) | power@0.03 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| completion | 0.7843 | 0.7626 | 0.0679 | 0.0638 | -0.0217 | 0.01203 | -1.80 | 0.07126 | null | [-0.0486, +0.0052] | 0.0370 | 60.2% |
| survival_rate | 0.9149 | 0.9254 | 0.0127 | 0.0118 | +0.0104 | 0.00224 | +4.67 | 2.972e-06 | REJECT | [+0.0054, +0.0155] | 0.0069 | 100.0% |

**BRANCH B** — completion null, survival positive, and the registered falsifier PASSES: the completion exclusion is tighter than the survival effect in standardized units.
falsifier: |z_c| + z_alpha < |z_s|  (registered 2026-08-13): 4.040 < 4.673 → passes

## Secondary metrics — descriptive, NOT in the family, no decision

| metric | ISO | JOINT | sd ISO | sd JOINT | Γ | sd(Γ) | z |
|---|---|---|---|---|---|---|---|
| episode_return | 24.3666 | 23.8708 | 2.1116 | 2.0236 | -0.4958 | 0.34468 | -1.44 |
| deaths_fire | 0.8126 | 0.6949 | 0.1514 | 0.1561 | -0.1177 | 0.02563 | -4.59 |

## Beat-reproducibility hurdle — floors are the hurdle, not the test variance

| metric | seed sd / floor (ISO) | seed sd / floor (JOINT) | sd(Γ) floor basis | Γ / floor sd(Γ) |
|---|---|---|---|---|
| completion | 1.12× | 1.09× | 0.00970 | 1.78× |
| survival_rate | 1.25× | 1.19× | 0.00177 | 5.40× |

A seed/floor ratio below 1 is n = 8 estimator noise, not a finding.

## Card diagnostic — seeds 1..12, this card − other card, paired by seed (descriptive)

| metric | ISO Δ (se) | JOINT Δ (se) | interaction JOINT−ISO (se) |
|---|---|---|---|
| completion | -0.0052 (0.0361) | -0.0001 (0.0268) | +0.0051 (0.0367) |
| survival_rate | -0.0024 (0.0048) | +0.0084 (0.0056) | +0.0108 (0.0055) |

## What this instrument is blind to (instruments law, 2026-08-10)

- Arm-SYMMETRIC effects cancel in Γ and are invisible here.
- Eval-set sampling: the interval conditions on one 512-episode draw.
- Convergence: Γ is at matched budget T* = 1000, never at convergence; Γ(t) over the retained checkpoints is REQUIRED evidence and is a separate stage.
- Branch D's discriminator (Γ(t)) is not computed here; D is only labelled.
- The statistic is the registered normal z. The t critical value at 142 dof and the same α is 2.2604 vs z_α 2.2365; stated, not applied.
