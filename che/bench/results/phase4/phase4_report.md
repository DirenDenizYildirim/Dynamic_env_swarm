# Phase 4 report

Coupling B live (Def. 6), the Theorem-1 handshake, the κ_B lock and the
acceptance grid. Where the phase-prompt accept criteria live: the M4.0
harness addendum and the M4.1 obs-v3 bench row are recorded in
`che/bench/results/gate_report.md` ("Phase 4 obs v3 — reference cell
re-measurement"); the E2C figure is the M4.2 section below; the κ_B lock
proposal will be `kappa_b_lock.md` (M4.3, repo root, same format as
`coupling_a_lock.md`); the acceptance grid closes this document (M4.4).

## M4.2 — ★ Theorem-1 E2C validation ★ (theory §5 Thm. 1, §10 hook)

**Claim under test (Thm. 1).** In the two-corridor environment
E_2C(κ_B), the optimal value is J\*(κ_B) = ½ + q(κ_B)/2, where q is the
probability of being informed by the commitment point; the memorizing
(signal-blind) policy is worth ½ for every κ_B, so the memorization gap
is exactly q/2 — and Coupling B erodes it continuously, to zero under
total perceptual denial.

### Protocol

`che/env/e2c.py`, engine shared with the `@slow` test and the figure
script (`che/scripts/plot_e2c.py`). Constants are shared by the predicted
and empirical curves — the M3.3 protocol-matching lesson, applied
forward.

- **Geometry (Option A, human ruling 2026-07-27):** d = 2, ℓ_f = 2,
  ℓ = 4, k = 9, grid 13², horizon T = d + ℓ = 6 (zero slack), branch at
  (6, 6), corridors along the row, fire at depth ℓ_f into corridor
  Z ~ U{L, R}. The phase-prompt rule k ≥ 2(d + ℓ_f) + 1 = 9 holds.
- **Hazard:** scripted — the fire cell is held Burning for the whole
  episode. Thm. 1 defines E_2C structurally (corridor Z lethal
  throughout) and the CA kernel is validated elsewhere (Prop. 2,
  Prop. 3); Def. 3's one-step burn-out would delete the theorem's
  hypothesis. What this milestone validates is the *observation* path.
- **Smoke:** the standard (σ_s, η) = (1.0, 0.5) dynamics via the
  production `hazard.smoke_step`, with **one smoke step before the first
  observation** (the fire has been burning since t = 0). Without it
  ρ₀ = 0 ⇒ τ₀ = 1 ⇒ q = 1 trivially at every κ_B. ρ at the fire cell
  therefore runs 1.000, 1.607, 1.974 over the three pre-commitment steps.
- **Observations:** `observation.observe` at obs v3 — the production
  crop, the shared `transmittance`, the per-cell reveal draw, and the
  same `env._OBS_STREAM` fold_in the swarm env uses. No bespoke signal
  channel exists; wrong crop offsets or plane order would collapse J\*
  onto the ½ floor.
- **Predicted curve:** q by Monte Carlo over the reveal randomness —
  Bernoulli(τ) with τ from the shared `transmittance` against the same
  smoke trajectory. It mirrors the rollout protocol exactly but does
  **not** pass through `observe`, and runs on an **independent PRNG
  stream**. Both properties are load-bearing: with shared keys and a
  shared path the test would reduce to the arithmetic identity
  J = q + (1 − q)/2 and would prove nothing.
- **Empirical curve:** the hand-coded policy of the prompt (walk to b;
  if informed take the corridor ≠ Z, else tie-break to L), 8192 episodes
  per κ_B (≥ the 4096 floor), plus the memorizing always-L policy.
- **Grid:** κ_B ∈ {0, 0.5, 1, 1.5, 2, 3, 5, 8}, spanning q ≈ 1 → q ≈ 0.

Raw: `phase4/m42/e2c_sweep.json` (commit 3dbc080 code state),
`e2c_replicates.json`; figure `e2c_theorem1.png`.

### Result

| κ_B | q (MC) | q (analytic) | q (via `observe`) | J\*_emp ± SE | J\*_pred | Δ | z | J_memorizing | plane-7 oracle |
|---|---|---|---|---|---|---|---|---|---|
| 0.00 | 1.0000 | 1.0000 | 1.0000 | 1.0000 ± 0.0000 | 1.0000 | +0.0000 | +0.00 | 0.4922 | 0.5078 |
| 0.50 | 0.9573 | 0.9580 | 0.9562 | 0.9790 ± 0.0016 | 0.9786 | +0.0004 | +0.19 | 0.4973 | 0.8566 |
| 1.00 | 0.8104 | 0.8115 | 0.8143 | 0.9080 ± 0.0032 | 0.9052 | +0.0027 | +0.71 | 0.5054 | 0.9656 |
| 1.50 | 0.6274 | 0.6262 | 0.6283 | 0.8091 ± 0.0043 | 0.8137 | −0.0046 | −0.91 | 0.4933 | 0.9891 |
| 2.00 | 0.4602 | 0.4564 | 0.4523 | 0.7266 ± 0.0049 | 0.7301 | −0.0035 | −0.63 | 0.4985 | 0.9977 |
| 3.00 | 0.2145 | 0.2218 | 0.2190 | 0.6055 ± 0.0054 | 0.6072 | −0.0018 | −0.30 | 0.4956 | 0.9999 |
| 5.00 | 0.0485 | 0.0469 | 0.0432 | 0.5123 ± 0.0055 | 0.5242 | **−0.0119** | **−2.11** | 0.4916 | 1.0000 |
| 8.00 | 0.0056 | 0.0046 | 0.0052 | 0.5000 ± 0.0055 | 0.5028 | −0.0028 | −0.51 | 0.4974 | 1.0000 |

![Theorem 1 in E_2C](m42/e2c_theorem1.png)

**Three independent routes to q agree at every point** — the MC
prediction (Bernoulli on `transmittance`), the closed product
1 − ∏(1 − τ_t), and the rate measured through the full `observe`
pipeline. The third is the substance of the handshake: it exercises the
crop offsets, the plane order and the reveal plumbing that the
prediction path never touches.

Acceptance, criterion by criterion:

1. **Empirical matches the numeric prediction** — PASS under the final
   three-condition gate (human ruling 2026-07-27, below): (a) max |z| =
   2.11 ≤ 2.69, (b) Σz² = 6.55 on 8 dof → p = 0.586 ≥ 0.05, (c) mean
   z = −0.44, within 0.71.
2. **Memorizing policy flat at ½** — PASS: every point within 2·SE of ½
   (max deviation 0.0084 at κ_B = 5, against 2·SE = 0.0110), no trend
   in κ_B.
3. **J\*(0) ≥ 0.99** — PASS: exactly 1.0000 (τ ≡ 1 ⇒ informed at t = 0
   in every episode).
4. **J\*(large) − ½ ≤ 0.02** — PASS: 0.0000 at κ_B = 8 (q = 0.0056).

### Acceptance gate for criterion 1 — final ruling (human, 2026-07-27)

Supersedes both the phase prompt's per-point 2·SE spec and the interim
joint-χ²-only amendment. Three conditions on the per-point
z = Δ / SE(Δ), **all required**, each catching what the others cannot:

| | condition | catches | measured |
|---|---|---|---|
| (a) | max \|z\| ≤ 2.69 (Šidák FWER 5%) | localized gross error at one κ_B | **2.11** ✓ |
| (b) | Σz² vs χ²(n), p ≥ 0.05 | diffuse magnitude misfit no single point flags (every point at −2σ passes (a), fails (b)) | **6.55 on 8 dof, p = 0.586** ✓ |
| (c) | \|mean z\| ≤ 2/√n = 0.71 | signed systematic drift passing both (every point at −1σ passes (a) and (b), fails (c)) | **−0.44** ✓ |

**GREEN under the final gate.** n counts every grid point; κ_B = 0 is
deterministic (τ ≡ 1 ⇒ q ≡ 1) and contributes z = 0 to all three
statistics. Constants live at the top of `che/tests/test_e2c.py` with
the rationale as one comment block.

Why the prompt's per-point 2·SE was replaced: applied across the 7
informative κ_B values it rejects a *correct* implementation with
probability 1 − 0.9545⁷ = **28%**, and on the pinned seed 0 the κ_B = 5
point lands at 2.11·SE. The replicate diagnostic (8 independent seeds ×
8 points, `e2c_replicates.json`, reproducible with
`plot_e2c.py --replicates 8`) settles which side of that we were on:

| κ_B | 0.5 | 1.0 | 1.5 | 2.0 | 3.0 | 5.0 | 8.0 |
|---|---|---|---|---|---|---|---|
| mean z over 8 seeds | +0.16 | +0.22 | +0.56 | −0.19 | −0.17 | −0.36 | −0.06 |
| sd z | 0.82 | 1.23 | 1.06 | 1.39 | 0.74 | 0.75 | 0.82 |
| \|z\| > 2 count | 0 | 1 | 1 | 1 | 0 | 0 | 0 |

Pooled over the 56 informative (seed, κ_B) cells: **mean z = +0.025,
sd = 0.990, 5.4 % beyond 2σ against 4.6 % expected** — the z-scores are
N(0, 1) to measurement resolution, and a systematic offset larger than
~0.13·SE (≈ 0.0007 in J) would have shown. κ_B = 5's mean z over seeds
is −0.36; seed 0's −2.11 is a fluctuation, not a defect. So the gate was
under-powered, not the implementation biased.

No tolerance was ever adjusted by the RA (CLAUDE.md invariant 4): the
gate was carried to the M4.2 STOP as a report-and-ask under the M3.3
protocol (pinned keys, deterministic committed outcome) and replaced by
the human ruling above. Re-keying to a seed that happens to pass was
considered and rejected as seed-shopping.

### Finding 1 — a documented kernel property (not a bug)

The prompt's *illustrative* geometry (d = 6, k = 17) was measured
unusable before implementation: with a single-cell smoke source the
n_quad = 4 midpoint quadrature never samples the ray's endpoint beyond
axis distance ≈ 4, so **τ = 1.0000 exactly** at the first two steps
(distances 6.32 and 5.39) for every κ_B up to 8 — hence q ≡ 1, a flat
J\* = 1 curve, and criterion 4 unreachable. Shrinking to d = 2 puts all
three pre-commitment distances (2.83, 2.24, 2.00) inside the sampled
regime; the τ profile at κ_B = 1.5 is (0.346, 0.260, 0.228).

Ruled a documented property of the locked M4.1 kernel, recorded in the
`transmittance` docstring and pinned by
`test_isolated_smoke_cell_is_unoccluded_beyond_quadrature_range`
(`che/tests/test_coupling_b.py`): *single-cell smoke sources contribute
no occlusion beyond axis distance ~4 under the midpoint quadrature;
spatially extended sources — what the CA actually produces — are
unaffected.* Option C (an endpoint-inclusive quadrature) was considered
and **rejected**: it would re-open locked M4.1, invalidate its fresh
bench row, and change obs-v3 semantics to serve a regime production
rarely enters. Option B (keeping d = 6 by adding an approach-side smoke
bank) was **rejected** as an unauthorized second smoke source and more
bespoke micro-env machinery than the theorem needs.

*Candidate limitations sentence for the paper:* "Perceptual attenuation
is integrated by a four-point midpoint quadrature along each line of
sight, which resolves the spatially extended smoke plumes the fire
kernel produces but under-resolves isolated single-cell sources at
ranges beyond about four cells; occlusion there is therefore a lower
bound."

### Finding 2 — masking is itself informative (quantified)

Smoke is co-located with the fire, so the ray to the *mirror* corridor
cell crosses no smoke and that cell is always revealed (τ ≡ 1 exactly —
asserted in `test_corridors_are_exchangeable`). "Exactly one candidate
masked" therefore identifies Z from the visibility plane alone, without
ever seeing fire content. Measured accuracy of an oracle that guesses Z
from the plane-7 pattern only (last column of the result table): **0.508
at κ_B = 0 — chance, nothing is masked — then 0.857, 0.966, 0.989,
0.998, and ≥ 0.9999 from κ_B = 3 up.**

So the *implemented* micro-environment's true optimal value is ≈ 1 at
every κ_B, and Thm. 1's J\* is the value of the **content channel
only** — which is what the prompt's q defines and what the scored
policies read. `test_scored_policies_never_read_the_visibility_plane`
enforces this end to end: destroying plane 7 leaves the optimal and
memorizing outcomes bitwise unchanged and collapses the oracle to
chance.

*Candidate footnote for the paper:* "Thm. 1 idealizes occlusion as pure
information loss. In any implementation where attenuation co-locates
with the threat, the mask is itself a signal: in E_2C an observer using
only the visibility channel identifies the burning corridor with
accuracy 0.99 at κ_B = 1.5 and ≈ 1 beyond, while never observing fire.
We score the content channel alone, and note that a learned policy is
free to exploit the residual channel — a conservative choice for the
memorization-gap claim."

### Forward obligations for M4.3

1. **Confirm the detection band sits in the well-sampled regime.** The
   band "P(a Burning cell at crop distance 3 is revealed)" probes
   distance 3 ≤ 4, so Finding 1 does not touch it — make this
   confirmation explicit in `kappa_b_lock.md` rather than implicit.
2. **The E2C cross-reference band maps to κ_B ≈ 1.3–2.6** under Option-A
   geometry (q ∈ [0.3, 0.7] read off the table above: q = 0.70 near
   κ_B = 1.3, q = 0.30 near κ_B = 2.6). This mapping is geometry-
   dependent and must be quoted as such.
3. **If the three lock bands fail to intersect, STOP** with the three
   curves side by side (human ruling 2026-07-27): a non-empty
   intersection was an assumption, and its failure is a finding for the
   lock discussion, not something to route around.

## M4.3 — κ_B lock (record: `kappa_b_lock.md`)

The three lock bands did **not** intersect, which triggered the
pre-agreed STOP (M4.2 ruling item 5). Full analysis, the three curves,
the two probe arms and the human ruling are in `kappa_b_lock.md`;
in brief: the `masked_frac` band was retired as a lock criterion (it
measures a policy-suppressible quantity), the E2C band was demoted to a
consistency check (geometry-contingent under the Option-A ruling), the
environment-native detection band bound the choice, and the human
locked **κ_B = 1.0** on 2026-07-27. The locked value now lives in the
three severity YAMLs. M4.4 below is the first grid run under it.

## M4.4 — acceptance training grid (Coupling-B ablation)

### Protocol

3 severities × κ_B ∈ {0, **1.0** (locked)} × seeds, dp = 0.5, 500
updates, Coupling A ON at its M3.4-locked parameters — the ablation
isolates perception decay *within* the compound, the same design logic
as M3.5's κ_A arm. Medium carries a **third seed** (human amendment 4):
Def.-4 variance concentrates near criticality, and "small but real" was
a pre-registered possibility there that two seeds cannot separate from
noise. 14 train + 14 eval cells; 512 stochastic episodes per eval.

Both arms run **obs v3**. At κ_B = 0 the visibility plane is present but
masking is bitwise-inert (invariant #3), so the ablation is the nested
model rather than a different observation schema.

All evals use eval seed 0, and `evaluate` derives every episode key from
that seed alone, so episode *i* starts from a **bitwise identical reset
state in both arms** — the arms are CRN-paired and diverge only through
the actions. The render audit confirms this visually (below).

Wall time on the 5090: 14 × 360 s training + 14 × 13 s eval + 2 × 30 s
calibration + renders ≈ 1.5 GPU-h. Artifacts:
`che/bench/results/phase4/m44/`, analysis JSON `m44_analysis.json`,
figures `m44_grid.png` (grid) and `m44_coactive.png` (Prop.-4
distribution), regenerated by `uv run python -m che.scripts.m44_report`.

### How "within seed noise" is decided

Fixed before the analysis so the falsifier's clause has one meaning.
**Provenance, stated precisely:** the *falsifier* was logged pre-data by
the human (amendment 3); this *operationalization* of its "within seed
noise" phrase was written by the RA after a first look at the
completion and survival means, and before any of the tables below were
produced. It is therefore not blind pre-registration, and is reported as
a stated rule rather than a pre-registered one. The headline result
(Result 1, High survival) is insensitive to the choice: it fires both
clauses with |delta| = 3.0 sigma_seed and seed ranges 5 points apart,
and would be flagged by any reasonable rule.

```
sigma_seed      = sqrt(mean over arms of Var(seed means, ddof=1))
within-noise   := ranges OVERLAP and |delta| <= 2 * sigma_seed
SEPARATED      := otherwise, graded:
                  (strong) ranges disjoint AND |delta| > 2*sigma_seed
                  (weak)   exactly one clause fires
```

The grading is not decoration. **No formal test is available at this
seed count**: a seed-level permutation test has minimum two-sided
p = 1/3 at 2v2 and 1/10 at 3v3, so no arrangement can reach 0.05. Each
clause alone is weak — range-disjointness happens with probability 1/3
under the null at 2v2, and `Var` of two points can collapse toward zero
by chance and make `2*sigma_seed` absurdly small. Only findings firing
**both** clauses are reported as robust. This is the same standard
Phase 3 used ("seed ranges overlap on one side"), made explicit.

At two seeds per arm the second clause provably cannot fire alone
(overlap forces `|delta| <= 2*sigma_seed`; see `classify`'s docstring
and `test_m44_stats.py`), so at Low and High "weak" always means
"disjoint ranges, small delta" — the p = 1/3 case.

### Per-cell means (512 episodes each)

| cell | completion | survival_rate | deaths_fire | deaths_collapse | burnt_fraction | mean_smoke_exposure | masked_frac | coupling_co_active |
|---|---|---|---|---|---|---|---|---|
| low_kb0_s0 | 0.7245 | 0.9539 | 0.3418 | 0.2109 | 0.0547 | 0.0001 | 0.0000 | 0.7910 |
| low_kb0_s1 | 0.6805 | 0.9489 | 0.3418 | 0.2715 | 0.0544 | 0.0002 | 0.0000 | 0.5977 |
| low_kbL_s0 | 0.7032 | 0.9569 | 0.3027 | 0.2148 | 0.0547 | 0.0002 | 0.0007 | 0.6328 |
| low_kbL_s1 | 0.7294 | 0.9577 | 0.3203 | 0.1875 | 0.0544 | 0.0001 | 0.0007 | 0.6934 |
| medium_kb0_s0 | 0.7443 | 0.9272 | 0.6719 | 0.2012 | 0.3203 | 0.0001 | 0.0000 | 0.5840 |
| medium_kb0_s1 | 0.7365 | 0.9378 | 0.5625 | 0.1836 | 0.3235 | 0.0001 | 0.0000 | 0.5957 |
| medium_kb0_s2 | 0.7253 | 0.9440 | 0.4590 | 0.2129 | 0.3212 | 0.0003 | 0.0000 | 0.5137 |
| medium_kbL_s0 | 0.7596 | 0.9416 | 0.4961 | 0.2051 | 0.3216 | 0.0001 | 0.0026 | 0.6387 |
| medium_kbL_s1 | 0.7406 | 0.9362 | 0.5996 | 0.1660 | 0.3215 | 0.0002 | 0.0025 | 0.5781 |
| medium_kbL_s2 | 0.7622 | 0.9305 | 0.6230 | 0.2109 | 0.3224 | 0.0001 | 0.0024 | 0.7109 |
| high_kb0_s0 | 0.7905 | 0.9408 | 0.5430 | 0.1680 | 0.9848 | 0.0075 | 0.0000 | 0.1680 |
| high_kb0_s1 | 0.8077 | 0.9225 | 0.7188 | 0.2109 | 0.9848 | 0.0120 | 0.0000 | 0.1562 |
| high_kbL_s0 | 0.8017 | 0.8721 | 1.3145 | 0.2207 | 0.9848 | 0.0060 | 0.0146 | 0.1406 |
| high_kbL_s1 | 0.8436 | 0.8159 | 2.0039 | 0.2051 | 0.9848 | 0.0075 | 0.0166 | 0.1641 |

### Result 1 — Coupling B charges survival, not task completion

| severity | metric | κ_B = 0 (per-seed) | κ_B = 1.0 (per-seed) | delta | sigma_seed | verdict |
|---|---|---|---|---|---|---|
| low | completion | 0.7025 (0.7245, 0.6805) | 0.7163 (0.7032, 0.7294) | +0.0138 | 0.0256 | within-noise |
| low | survival_rate | 0.9514 (0.9539, 0.9489) | 0.9573 (0.9569, 0.9577) | +0.0059 | 0.0026 | **SEPARATED(strong)** |
| medium | completion | 0.7354 (0.7443, 0.7365, 0.7253) | 0.7541 (0.7596, 0.7406, 0.7622) | +0.0188 | 0.0107 | within-noise |
| medium | survival_rate | 0.9364 (0.9272, 0.9378, 0.9440) | 0.9361 (0.9416, 0.9362, 0.9305) | −0.0003 | 0.0072 | within-noise |
| high | completion | 0.7991 (0.7905, 0.8077) | 0.8227 (0.8017, 0.8436) | +0.0236 | 0.0227 | within-noise |
| high | survival_rate | 0.9316 (0.9408, 0.9225) | **0.8440** (0.8721, 0.8159) | **−0.0876** | 0.0295 | **SEPARATED(strong)** |
| high | deaths_fire | 0.6309 (0.5430, 0.7188) | **1.6592** (1.3145, 2.0039) | **+1.0283** | 0.3558 | **SEPARATED(strong)** |

**At High, perception decay costs 8.8 points of survival and multiplies
fire deaths by 2.6×, while completion does not fall** (+0.024, within
noise; the sign is positive at all three severities). This is the
phase prompt's "expected-not-forced" prediction — the cost lands where
smoke is abundant — but with a sharper shape than expected: it is a
*survival* cost, not a task cost. The swarm trades agents for coverage.

The comparison is clean because the environment realization is held
essentially fixed across arms: `burnt_fraction` agrees to four decimals
at every severity (0.0545/0.0546, 0.3216/0.3219, 0.9848/0.9848), and
`collapse_events` and `seeded_ignitions` agree to within 0.03 and 0.03
events per episode. The arms differ in behaviour, not in the fire they
faced.

The table above shows the metrics the falsifier's condition (i) is
defined on; the full ten-metric comparison is in `m44_analysis.json`.
Three further rows there carry a SEPARATED grade on effects too small to
interpret — `low/deaths_fire` (−0.030), `low/seeded_ignitions` (−0.027)
and `high/collapse_events` (+0.026). The first is the documented
degenerate-variance failure mode: both κ_B = 0 Low seeds returned
*exactly* 0.3418 fire deaths (175/512), so that arm's sampled variance
is zero and `2*sigma_seed` collapses. Recorded rather than quietly
dropped; none of them enters the falsifier.

**Low reverses sign, and that is a hypothesis, not a result.** Survival
is *higher* with Coupling B live (+0.0059). The rule calls it strong,
but it sits at 1.16× its own threshold, is a 0.6-point effect, and rests
on two seeds. The mechanism worth testing is in Result 2: where
occlusion is rare (Low masks 0.07 % of the crop on average but 8.1 % of
it at danger moments — the largest amplification of the three
severities), masking may act mainly as a *threat marker* rather
than as information loss. Recorded as a hypothesis; a targeted test
(more Low seeds, or an arm with the visibility plane zeroed) would
settle it.

### Result 2 — danger-moment masking (amendment 4a)

Masking is emitted as poolable counts, so the conditional mean is
`sum(masked_danger_sum) / sum(danger_agents)` over all steps and
episodes — never an average of per-step conditional means over steps
where the condition never fired.

| severity | danger rate (danger/alive) | masked_frac (unconditional) | masked_frac at danger moments | amplification |
|---|---|---|---|---|
| low | 0.0068 | 0.00068 | 0.0809 | **118×** |
| medium | 0.0396 | 0.00249 | 0.0560 | **22×** |
| high | 0.0621 | 0.01559 | 0.2424 | **16×** |

When a Burning cell is inside an agent's crop, a sixth to a quarter of
that crop is masked; averaged over the swarm the same quantity reads as
0.07 %–1.6 %. This is M4.2's Finding 2 ("masking is itself informative
when occlusion co-locates with threat") reproduced at swarm scale in the
full environment, and it is the quantitative reason the unconditional
`masked_frac` was a bad calibration band: it averages over a swarm that
is mostly nowhere near fire. The M4.3 decision to retire that band is
vindicated by its own diagnostic.

### Result 3 — the provisional perception-exposure finding does NOT survive

Amendment 2 set the test: the κ_B = 0 arm is the free control —
identical lethality incentives, masking bitwise-inert — so *different* →
perception-driven regulation confirmed, *indistinguishable* → restate as
fire-avoidance byproduct. Two independent controls both fail it.

**(a) Training length.** `masked_frac` ceiling (κ_B → ∞, evaluated on
the states each policy actually visited, so it is a κ_B-free measure of
*where the swarm stood*). The random-policy column is bitwise identical
across the M4.3 and M4.4 calibration runs, so the columns are directly
comparable:

| severity | random | M4.3 200u κ_B=0.5 | M4.3 200u κ_B=1.5 | M4.4 500u κ_B=0 | M4.4 500u κ_B=1.0 |
|---|---|---|---|---|---|
| low | 0.0279 | 0.0092 | 0.0152 | 0.0258 | 0.0306 |
| medium | 0.1278 | 0.0433 | 0.0404 | 0.1016 | 0.1341 |
| high | 0.4153 | 0.5172 | 0.4498 | 0.5357 | 0.5014 |

The 3× suppression at Medium that motivated the finding is a **200-update
transient**. By 500 updates the trained policies sit at or above the
random-policy ceiling at every severity.

**(b) The κ_B = 0 control.** At Low and Medium the κ_B = 0 arm is *less*
exposed than the κ_B = 1.0 arm (ceiling +0.005 / +0.033, exposed-agent
share +0.002 / +0.028 in the coupled arm) — the opposite of what
perception-driven regulation predicts. At High the coupled arm is less
exposed (ceiling −0.034, exposure −0.0031), but that arm also loses 8.8
points of survival, and `mean_smoke_exposure` averages over **alive**
agents, so losing the most-exposed agents lowers it mechanically.
Conditioning on zero-death episodes does not repair this — it is a
collider, and it retains 44 % of κ_B = 0 episodes against 14 % of
κ_B = 1.0 episodes, i.e. two different populations.

**Ruling applied (amendment 2): restated as a fire-avoidance byproduct**,
and further as an artifact of early training. The paper sentence is
stronger for it: *perception attenuation is not behaviourally
suppressible — the swarm cannot position its way out of it, and pays in
survival.* Smoke outlives flame by design (D3), so smoke exposure is a
poor proxy for danger and avoiding it earns nothing; the threat-aligned
quantity is the conditional masking of Result 2, not the unconditional
exposure.

### Result 4 — coupling-co-active visitation: first data (Prop.-4 diagnostic)

| severity | arm | mean | share = 0 | q90 | q99 | max | counts 0/1/2/3/4+ |
|---|---|---|---|---|---|---|---|
| low | κ_B=0 | 0.694 | 0.587 | 2 | 5 | 9 | 0.587/0.239/0.106/0.046/0.021 |
| low | κ_B=1.0 | 0.663 | 0.563 | 2 | 4 | 5 | 0.563/0.284/0.097/0.041/0.015 |
| medium | κ_B=0 | 0.564 | 0.621 | 2 | 4 | 6 | 0.621/0.253/0.082/0.031/0.013 |
| medium | κ_B=1.0 | 0.643 | 0.578 | 2 | 4 | 7 | 0.578/0.268/0.108/0.030/0.016 |
| high | κ_B=0 | 0.162 | 0.872 | 1 | 2 | 3 | 0.872/0.100/0.022/0.006/0.000 |
| high | κ_B=1.0 | 0.152 | 0.883 | 1 | 2 | 3 | 0.883/0.089/0.021/0.007/0.000 |

The counter (invariant #5, logged from day one) finally has data. The
distribution is **zero-inflated and over-dispersed** — 56–88 % of
episodes contain no co-active event at all, while the tail reaches 9 —
so the mean alone would have been actively misleading. The phase
prompt's insistence on the distribution was right.

No cross-arm difference at any severity, which is expected: the counter
is a Coupling-A observable and κ_B does not enter it.

The severity ordering is **inverted** (High lowest, 0.16 vs 0.69 at
Low). This is the Phase-3 fuel-exhaustion result recurring: at High,
`seeded_ignitions` is 0.83/episode against 4.08 at Low, because the
primary front has already consumed the fuel that collapse debris would
otherwise ignite. Coupling A's *ignition* channel self-limits exactly
where the hazard is most severe — so the two couplings are strongest in
different regimes, which is itself a compound-hostility observation.

### Result 5 — detection drift at the locked κ_B (amendment 1)

Detection band (Medium — the binding one for the lock): [0.4, 0.7].
Values are P(a Burning cell at crop distance 3 is revealed) at
κ_B = 1.0.

| severity | random | M4.3 200u κ_B=0.5 | M4.3 200u κ_B=1.5 | M4.4 500u κ_B=0 | M4.4 500u κ_B=1.0 | in band |
|---|---|---|---|---|---|---|
| low | 0.3932 | 0.4151 | 0.4073 | 0.3969 | 0.4004 | yes (marginal) |
| medium | 0.3836 | 0.4383 | 0.4266 | 0.4452 | **0.4465** | **yes** |
| high | 0.3615 | 0.2809 | 0.3515 | 0.2972 | 0.3336 | no (not binding) |

**The lock holds under the longer-trained policies.** Medium, the
severity the band was defined on, reads 0.4465 — inside the band and
slightly further from its floor than the 200-update probes were. Two
honest flags: Low clears the floor by 0.0004, which is marginal enough
that it should not be quoted as independent support; and High sits below
the band, as it did at M4.3 (0.281 / 0.352), because dense smoke at
`burnt_fraction` ≈ 0.98 attenuates more than the Medium-calibrated band
contemplates. The band was Medium-specific and High was never binding,
but the deviation is recorded rather than dropped.

### Result 6 — m31b watch item (carried from Phase 3): closed

Completion conditioned on per-episode `burnt_fraction`, now that M4.0
makes it measurable per episode:

| severity | arm | <0.05 (fire-free) | 0.05–0.20 | 0.20–0.40 | 0.40–0.60 | >0.60 |
|---|---|---|---|---|---|---|
| medium | κ_B=0 | 0.721 (n=107) | 0.720 (n=320) | 0.730 (n=544) | 0.749 (n=504) | 0.777 (n=61) |
| medium | κ_B=1.0 | 0.752 (n=111) | 0.743 (n=313) | 0.746 (n=548) | 0.766 (n=506) | 0.789 (n=58) |
| low | κ_B=1.0 | 0.714 (n=553) | 0.720 (n=463) | 0.676 (n=8) | – | – |

The watch item was a suspected coverage regression: obs-v2 Medium
appeared to stall at arena edges in fire-free episodes where v1 swept
better. Under obs v3 there is **no such signal**. Medium completion
*rises* monotonically with burnt_fraction rather than falling, and
Medium fire-free completion (0.721 / 0.752) is at or above Low's overall
completion (0.703 / 0.716) — the severity that burns ~5 % of the arena
and sits in the fire-free bucket half the time. The Phase-3 caveat
stands: the env family changed since
m31b, so this is a fresh measurement rather than a re-test.
**Recommend closing the watch item.**

### Inertness falsifier (amendment 3, logged pre-data)

| condition | holds? | evidence against |
|---|---|---|
| (i) Δcompletion, Δsurvival within seed noise | **NO** | low/survival_rate (+0.0059, strong); high/survival_rate (−0.0876, strong) |
| (ii) no cross-arm exposure/positioning difference | **NO** | low/danger_rate (+0.00067, weak); high/mean_smoke_exposure (−0.00306, weak) |
| (iii) danger-moment masking negligible | **NO** | low 118×; medium 22×; high 16× |
| (iv) no co-active visitation difference | yes | — |

**Verdict: NOT INERT.** Three of four conditions fail, and condition (i)
fails on the strong grade at High — the one place where both clauses of
the stated rule fire on a large effect (−0.088 survival, ranges
disjoint by 5 points). The reportable-negative-result branch is not
taken. Note that (ii) fails only on *weak* evidence and in
inconsistent directions, which is exactly the reading that demoted the
perception-exposure finding in Result 3; the falsifier's verdict does
not rest on it.

### Render audit (standing rule + amendment 4c)

24 GIFs in `m44/renders/`: 6 episodes per severity at the locked κ_B
(18), plus the same 6 episode seeds re-rendered on the κ_B = 0 arm at
Medium (6).

- **CRN pairing confirmed visually.** Matched Medium pairs show
  identical hazard and smoke fields at matched timesteps — same burn
  scars, same burning counts (0/10/16/0 at t = 64/128/192/254) — with
  only the agent positions differing. This is invariant #3 checked at
  the trajectory level, by eye, on the real environment.
- **High is a single front passage.** Burning peaks near 86 cells around
  t ≈ 38, and by t ≈ 89 the fire is out with the arena ~98 % burnt; the
  remaining two thirds of the episode is foraging in ash with zero
  burning cells. The entire risk budget is spent in one window — which
  is precisely why Coupling B's cost lands on survival (agents die
  during the passage) and not on completion (the post-fire ash field is
  safe and still holds food).
- **Periphery audit (4c): negative.** No visually evident smoke-avoidance
  or periphery-hugging in either arm, at any severity, consistent with
  the Result-3 numbers.

**Gap, flagged rather than filled:** matched κ_B = 0 renders exist only
at Medium, which is what amendment 4c specified — but the headline
result is at High. A matched High pair (6 renders, ≈2 GPU-min) would be
the natural visual control for it. Not run without a ruling, per the
no-silent-scope-change rule.

## Phase-4 acceptance status

Accept list from the phase prompt, item by item:

- **E2C figure** — M4.2 section above, `m42/e2c_theorem1.png`, gate GREEN under
  the human's final three-condition ruling.
- **Lock** — `kappa_b_lock.md`, κ_B = 1.0 human-locked 2026-07-27;
  M4.3 summary section above. Re-validated under M4.4's 500-update
  policies (Result 5).
- **Grid** — M4.4 section above, 14 cells, `m44_grid.png`.
- **Renders** — 24 GIFs, audit above, m31b watch item closed.
- **Co-active analysis** — Result 4, with the per-episode distribution
  and `m44_coactive.png`.

**Headline for the paper:** Coupling B is not inert and is not
behaviourally suppressible. Under severe hazard it converts a perception
cost into an 8.8-point survival cost while leaving task completion
intact, and its masking is 16–118× concentrated on exactly the moments
when a threat is in view.

**STOP — Phase 4 complete; GO/NO-GO on Phase 5 (comms) is a human call.**
