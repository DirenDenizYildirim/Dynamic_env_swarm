# Coupling-A Lock — M3.4 proposal (awaiting human lock)

Date: 2026-07-21. RA proposal from random-policy calibration of the full
environment (`che/calibration/coupling_a.py`; 128 episodes/cell, L = 64,
12 agents, horizon 256, obs v2, primary reset ignition active; raw data
`che/bench/results/phase3/m34/coupling_a_calibration.json`, wall 363 s,
CPU). The Low seeded-burnt share uses CRN-paired κ_A ∈ {0, κ*} runs on
identical episode keys (the nesting invariant makes the κ_A = 0 member
the exact nested model). r_seed = 1 (3×3 ball, Def. 5 default) — not
swept; no target constrains it and the Prop.-3 machinery (M3.3) is
calibrated at 1.

## Targets (phase3_prompt.md M3.4)

| observable (per episode, random policy) | band |
|---|---|
| collapse events | [3, 10] |
| seeded ignitions | [1, 5] |
| Low: seeded share of total burnt area | ≥ 50% |
| deaths_collapse | [0.05, 0.5] |

## Measured candidates

Factored design around a center candidate (each observable driven by one
axis; the cross adds compiles, not information). ✓/✗ against the bands;
collapse counts are severity-independent (structure never reads β — a
design sanity check that the data confirms: every row's coll varies < 2%
across severities).

| # | f_weak | λ₀ | κ_A | λ_load | Low coll / seeded / dc / share | Med seeded / dc | High seeded / dc |
|---|---|---|---|---|---|---|---|
| 1 | 0.15 | 3e-5 | 0.06 | 4e-4 | 4.7 ✓ / 2.45 ✓ / 0.172 ✓ / **0.615 ✓** | 2.04 ✓ / 0.164 ✓ | 0.46 ✗ / 0.055 ✓ |
| **2** | **0.15** | **5e-5** | **0.06** | **4e-4** | **8.5 ✓ / 4.47 ✓ / 0.180 ✓ / 0.763 ✓** | **3.70 ✓ / 0.141 ✓** | **0.78 ✗ / 0.102 ✓** |
| 3 | 0.15 | 8e-5 | 0.06 | 4e-4 | 13.0 ✗ / 6.45 ✗ / 0.219 ✓ / 0.825 ✓ | 5.24 ✗ / 0.188 ✓ | 1.31 ✓ / 0.094 ✓ |
| 4 | 0.25 | 3e-5 | 0.06 | 4e-4 | 8.1 ✓ / 3.91 ✓ / 0.336 ✓ / 0.726 ✓ | 3.27 ✓ / 0.305 ✓ | 0.71 ✗ / 0.203 ✓ |
| 5 | 0.15 | 5e-5 | 0.03 | 4e-4 | 8.2 ✓ / 2.18 ✓ / 0.133 ✓ / 0.696 ✓ | 1.90 ✓ / 0.109 ✓ | 0.36 ✗ / 0.070 ✓ |
| 6 | 0.15 | 5e-5 | 0.10 | 4e-4 | 7.8 ✓ / 6.79 ✗ / 0.211 ✓ / 0.820 ✓ | 5.55 ✗ / 0.180 ✓ | 1.53 ✓ / 0.117 ✓ |
| 7 | 0.15 | 5e-5 | 0.06 | 1e-4 | 7.9 ✓ / 3.79 ✓ / 0.086 ✓ / 0.638 ✓ | 3.12 ✓ / 0.070 ✓ | 0.65 ✗ / 0.031 ✗ |
| 8 | 0.15 | 5e-5 | 0.06 | 1e-3 | 8.4 ✓ / 4.20 ✓ / 0.445 ✓ / 0.709 ✓ | 3.33 ✓ / 0.406 ✓ | 0.73 ✗ / 0.281 ✓ |

Supporting columns (candidate 2): burnt cells 234 / 1403 / 4036,
deaths_fire 0.52 / 2.52 / 7.02, survival 0.94 / 0.78 / 0.41 across
Low / Medium / High — the severity ladder is intact under Coupling A.

## Structural finding — High-severity seeding is Fuel-limited

Realized seeded ignitions at High are ~5.7× below Low at *every* κ_A
(the ratio is κ-independent): the supercritical primary fire consumes
~98% of the arena early, so most seed attempts land on already-burnt
cells and are filtered by the Fuel-only rule (Def. 5). Consequently **no
κ_A satisfies seeded ∈ [1, 5] at High without pushing Low over 5**
(candidates 3 and 6 show the trade). This is physics, not
mis-calibration — at High, structural fire-seeding is marginal by
construction, consistent with Prop. 3 making Coupling A the *Low/
near-critical* regime's storyline. Proposal treats the seeded band as
binding at Low and Medium; the human lock should confirm or override
that reading.

## Recommendation — lock candidate 2

**(f_weak, λ₀, λ_load, κ_A, r_A) = (0.15, 5e-5, 4e-4, 0.06, 1)**

- Every band satisfied at Low and Medium; deaths_collapse in-band at all
  three severities (0.10–0.18).
- Low seeded share 0.763 — comfortably in the Prop.-3 regime where
  Coupling A dominates the hazard budget, giving M3.5's key question
  ("does Low survival leave the ceiling once collapse-seeded fire
  dominates?") the strongest fair test among in-band candidates.
- High realized seeding 0.78/ep is the best achievable without breaking
  the Low band (see finding above).
- Alternative if a gentler regime is preferred: candidate 1 (λ₀ = 3e-5)
  centers every Low band (4.7 / 2.45 / 0.172 / 0.615) at the cost of a
  weaker Low share and near-floor High deaths_collapse (0.055).

## LOCK — human decision 2026-07-21 (joint w/ RA)

**LOCKED: (f_weak, λ₀, λ_load, κ_A, r_A) = (0.15, 5e-5, 4e-4, 0.06, 1)**
(candidate 2). Rationale: ablation power within bands; deaths_collapse
centered; seeded-burnt share 0.763 = the Prop.-3 regime. Candidate 1
(λ₀ = 3e-5) recorded as the rejected gentler alternative.

**Seeded band CONFIRMED as binding at Low/Medium only.** The High
behavior is recorded as **fuel-exhaustion self-limitation of the
ignition channel** — the empirical mirror of Prop. 3's χ-divergence:
collapse matters most where fire is rare. Candidate sentence for the
paper: *"At high severity the ignition channel of structural coupling
is self-limiting — the primary fire exhausts the fuel that collapse
events would ignite — so structural fire-seeding matters most precisely
where fire is otherwise rare, the empirical mirror of the
χ(β)-divergence in Prop. 3."* Per-severity κ_A was considered and
**rejected** (it would break Phase-7 factorial semantics).

Sanity acknowledged: collapse-count β-independence (< 2%) confirms the
T_C factorization.

**M3.5 addendum (drift + channel evidence), human-ordered:** the M3.5
report must compare realized collapses/ep, seeded/ep, and
deaths_collapse under *trained* policies per severity against the
random-policy calibration values above; Low drift outside [3, 10] /
[1, 5] is flagged for human review, never auto-adjusted. At High,
deaths_collapse and blocked-move encounters are reported to document
the non-ignition structural channels. (Supported by the
collapse_events / blocked_moves / weak_occupancy info channels and
eval-harness metrics added at this lock.)

Locked values written into `che/configs/severity_{low,medium,high}.yaml`
with provenance comments. GO M3.5 as scripted (+ addendum).
