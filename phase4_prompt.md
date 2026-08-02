# Phase 4 — Coupling B live + Theorem-1 E2C validation + κ_B lock

> Fresh session at repo root. Prerequisites: Phase 3 complete and accepted
> (GO recorded), obs v2 in force, Coupling-A params locked
> (`coupling_a_lock.md`), D4 dp=0.5, standing throughput rule in the
> decision log. Milestone by milestone; STOP and report.

## Context

Coupling B (Def. 6): the smoke field attenuates perception via
Beer–Lambert transmittance τ = exp(−κ_B ∫ ρ dℓ) along the line of sight.
This is the coupling Theorem 1 is *about* — perception decay destroys
exactly the information that makes adaptivity valuable — and Phase 4 must
(i) implement it with the same PRNG/nesting discipline as everything
else, (ii) validate the code path against the theorem's semi-closed form
in the E2C micro-environment, (iii) calibrate and lock κ_B, and (iv) run
the acceptance grid — which lights up the coupling-co-active counter for
the first time (κ_A and κ_B simultaneously nonzero).

Note on parameters: (σ_s, η) stay at their long-standing config values —
optical depth is the product κ_B·ρ, so sweeping κ_B alone is fully
general; changing smoke constants now would change the env family for no
expressive gain. State this in the code where κ_B is defined.

## Milestone 4.0 — Harness addendum (Phase-3 carry-overs)

- Add per-episode `burnt_fraction` (final) and `masked_frac`
  (mean fraction of crop cells masked, alive agents, defined in M4.1) to
  env info + eval harness npz/JSON. Small, do first — Phase-3 lesson:
  retrofit metrics before, not after, the phase that needs them.
- **Accept:** harness tests updated, suite green. No STOP.

## Milestone 4.1 — Coupling B implementation (obs v3)

Design (locked by RA+human at phase planning; deviations need a STOP):

- **Per-cell stochastic masking.** For each cell y in agent i's k×k crop:
  optical depth D(i,y) = κ_B · dist(x_i, y) · mean_ρ(ray), with mean_ρ
  from an S=4-point quadrature along the ray through the *current* smoke
  field (vmap over agents × cells; bench it). τ = exp(−D). The cell's
  content planes are revealed with probability τ, else zeroed. Own cell:
  dist 0 ⇒ always visible. Own-state vec unaffected.
- **Visibility plane.** Append plane 8: the realized per-cell reveal mask
  (1 = seen). Agents must be able to distinguish "unseen" from "absent" —
  zero-fill without a mask conflates them and would confound the
  ISO/JOINT comparison with an artificial memory burden. This is obs v3;
  config obs_version: 3; prior checkpoints archival-only (same D5
  protocol; this is the *designed* Phase-4 obs change, schema frozen
  after this milestone — Phase 5 adds message inputs, not grid planes).
- **PRNG discipline:** the per-cell reveal uniforms are drawn
  unconditionally; κ_B = 0 ⇒ τ ≡ 1 ⇒ bitwise-identical trajectories to
  the pre-masking env given the same keys. Nesting-suite test required.
- **Transmittance is ONE function** (`che/env/observation.py:
  transmittance(...)`) used by the env, by the E2C validation, and by
  any diagnostic — the Thm.-1 comparison is only meaningful if the
  micro-env and the swarm env share the literal code path.
- Tests: τ monotone decreasing in distance, in smoke, in κ_B; masking
  respects the visibility plane exactly; nesting; per-plane border
  correctness updated for 8 planes.
- Bench: reference cell row (env-only + one training run for the
  end-to-end number). **Standing rule applies:** if the training
  projection < 100k steps/s, activate the uint8 contingency and re-bench
  before proceeding — do not ask, do not renormalize.
- **Accept:** suite green, bench row appended with verdict. STOP.

## Milestone 4.2 — ★ E2C micro-environment: Theorem-1 validation ★

Build `che/env/e2c.py` per theory §5/§10: start cell, path length d to
branch b, corridors length ℓ, fire at depth ℓ_f in corridor Z ~ U{L,R},
horizon d+ℓ (zero slack), reward 1 on reaching the goal. Geometry must
fit perception: micro-env config uses its own k ≥ 2(d+ℓ_f)+1 (e.g.
d=6, ℓ_f=2, k=17). The fire cell emits smoke per the standard (σ_s, η)
dynamics from t=0; the agent's information about Z arrives only through
the real Coupling-B code path (transmittance + masking of the burning/
smoke planes in its crop) — no bespoke signal channel.

- **Predicted curve:** J*(κ_B) = 1/2 + q(κ_B)/2 where q = P(the burning
  corridor is revealed in the crop at any pre-commitment step), computed
  *numerically* by Monte Carlo over the reveal randomness using the
  shared transmittance function and the actual smoke trajectory
  (theory Thm.-1 robustness note: the closed form's e^{−κ_B j} is
  replaced by the implemented optical depths; monotonicity is
  guaranteed, the specific curve is computed).
- **Empirical curve:** a hand-coded optimal policy (proceed to b; if
  informed take the safe corridor, else tie-break to L) run over ≥4096
  episodes per κ_B on a grid spanning q ≈ 1 → q ≈ 0 (include κ_B = 0 and
  a large-κ_B point). Also run the memorizing policy (always-L) — must
  sit at 1/2 ± MC error, flat in κ_B.
- **Acceptance (@slow, CPU):** empirical J* within 2·SE of the numeric
  prediction at every grid point; memorizing policy flat at 1/2;
  J*(0) ≥ 0.99; J*(κ_B→large) − 1/2 ≤ 0.02.
- Figure for the report (and likely the paper): J* vs κ_B, predicted
  curve + empirical points + the 1/2 memorization floor — Theorem 1 as
  a picture.
- **Accept:** slow test green; figure in phase4_report.md. STOP — human
  reviews the figure (this is the second theory↔implementation
  handshake; protocol-matching lesson from M3.3 applies — the predicted
  and empirical curves must share every constant).

## Milestone 4.3 — κ_B calibration → human lock

Propose the locked κ_B against target observables (random policy + one
fresh 200-update probe policy per severity, obs v3, both couplings on):

- At Medium with active fire: masked_frac (alive agents, fire-active
  steps) ∈ [0.15, 0.45] — perception meaningfully degraded, not blind.
- Detection band: P(a Burning cell at crop distance 3 is revealed |
  typical Medium smoke) ∈ [0.4, 0.7].
- E2C cross-reference: q(κ_B) at the proposed value ∈ [0.3, 0.7] in the
  standard E2C geometry — the partial-information regime where Thm. 1
  says the coupling has maximal bite.
- Report the κ_B sweep table (≥5 candidates) with all three observables
  + Low/High values for context → `kappa_b_lock.md` proposal, same
  format as previous locks. **STOP — human locks.**

## Milestone 4.4 — Acceptance training grid

- 3 severities × κ_B ∈ {0, locked} × 2 seeds, dp=0.5, 500 updates,
  Coupling A ON at locked params (the ablation isolates perception decay
  *within the compound* — same design logic as M3.5's κ_A arm).
- Report per arm: completion, survival, deaths by cause, smoke exposure,
  masked_frac, burnt_fraction, **coupling-co-active visitation** (first
  nonzero readings — the Prop.-4 diagnostic finally has data; include
  its per-episode distribution, not just the mean).
- Expected-not-forced: perception decay should cost completion/survival
  most where smoke is abundant (Medium/High); note whatever happens.
- **Render audit (standing rule):** ≥6 episodes per severity at the
  locked κ_B, plus the m31b watch item: fire-free-episode coverage at
  Medium under the current env (burnt_fraction now measurable per
  episode — condition on it).
- **Accept:** phase4_report.md complete (E2C figure, lock, grid, renders,
  co-active analysis). STOP — Phase 4 complete; GO/NO-GO on Phase 5
  (comms) is a human call.

## Non-goals

Comms (Phase 5), ISO/JOINT (6–7), message-channel obs, smoke-parameter
changes, any further obs-schema changes after M4.1, theory-doc edits
beyond none (the Thm.-1 robustness note already covers the numeric-q
substitution).
