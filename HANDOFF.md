# HANDOFF — session state for the next model (written 2026-07-27)

You are picking up mid-Phase-4 as the implementation engineer. Read, in
order, before doing anything: `CLAUDE.md` (invariants — non-negotiable),
`phase4_prompt.md` (the milestone spec governing all current work),
`docs/theory_foundations.md` §5 (Def. 6, Thm. 1) and §10 (Phase-4 hook).

## Where things stand

- **Phases 0–3: complete and locked.** Severities β = 0.43/0.49/0.70
  (Low/Med/High, β_c = 0.500), Coupling A locked (f_weak 0.15, λ₀ 5e-5,
  λ_load 4e-4, κ_A 0.06, r_seed 1), dp = 0.5 (D4), obs v2 was D5.
- **M4.0 (30905c9): done.** `burnt_fraction` + `masked_frac` info
  channels and eval-harness metrics.
- **M4.1 (bfab1d2 code, 52e8a76 close): done, STOP satisfied.** Obs v3 =
  Coupling B live: per-cell stochastic masking by Beer–Lambert
  transmittance + visibility plane 7 (8 planes total, schema frozen —
  Phase 5 adds message inputs, not grid planes).
  - `transmittance()` in `che/env/observation.py` is **THE ONE** shared
    code path — env, E2C validation, diagnostics must all call it. Never
    fork or inline a variant.
  - Reveal uniforms come from `jax.random.fold_in(key, _OBS_STREAM=47)`
    (see `che/env/env.py`) so kernel streams are untouched; κ_B=0 is
    bitwise-identical to the pre-masking env (tests prove it).
  - Bench row (RTX 5090, in `che/bench/results/gate_report.md`):
    env-only 8,375,048 steps/s (−12.6 % vs v2); training projection ÷81
    = **103.4k ≥ 100k → uint8 contingency UNTRIGGERED**, margin ~3 %.
    End-to-end training neutral (276 s vs 285 s medium probe). PASS with
    flag: any further env-side cost (Phase 5 comms) will cross the line
    and auto-trigger the contingency (standing rule 2026-07-21: activate
    and re-bench, don't ask; the 100k line moves only via a human budget
    recalc in the decision log).
- Suite: **103 passed** (+7 `@slow` deselected), `ruff check` clean.
  Note: `ruff format` is NOT enforced (pre-existing files aren't
  format-clean). CPU suite wall time ~140 s — slightly past the ~2 min
  CLAUDE.md guidance, flagged but not acted on.

## Next: M4.2 — E2C micro-env, Theorem-1 validation (per phase4_prompt.md)

Wait for the human's go-ahead, then:

- Build `che/env/e2c.py`: two-corridor environment, d=6, ℓ_f=2, k=17;
  smoke via the standard σ_s=1.0 / η=0.5 dynamics from t=0; the agent's
  information about the correct corridor flows **only** through the real
  Coupling-B code path (`observation.transmittance` + reveal draw).
- Predicted J*(κ_B) = ½ + q(κ_B)/2 with q computed **numerically by MC**
  through the shared `transmittance` (robustness note replaces the
  closed form q = 1 − ∏_{j=ℓ_f}^{d+ℓ_f} (1 − e^{−κ_B j})).
- Empirical: hand-coded optimal policy, ≥4096 episodes per κ_B point,
  plus an always-L memorizing policy.
- Acceptance (@slow, CPU): empirical within 2·SE of predicted
  everywhere; memorizing policy flat at ½; J*(0) ≥ 0.99; large-κ_B gap
  ≤ 0.02. Figure goes into `phase4_report.md`. **STOP — human reviews
  the figure.**

## Then

- **M4.3:** κ_B sweep (≥5 candidates; random + 200-update probe policies
  per severity, obs v3, both couplings on) against three bands: Medium
  masked_frac ∈ [0.15, 0.45] on fire-active steps; P(Burning at crop
  distance 3 revealed) ∈ [0.4, 0.7]; E2C q ∈ [0.3, 0.7]. Propose in
  `kappa_b_lock.md`. **STOP — human locks κ_B.** (σ_s, η stay fixed;
  optical depth is the κ_B·ρ product, so sweeping κ_B alone is general.
  Pattern to follow: `che/calibration/coupling_a.py` — CRN pairing,
  reference-scale 64²/12 agents/horizon 256.)
- **M4.4:** acceptance grid — 3 severities × κ_B ∈ {0, locked} × 2
  seeds, dp 0.5, 500 updates, Coupling A ON; report the per-episode
  coupling-co-active distribution (first nonzero data); render audit ≥6
  eps/severity incl. the m31b fire-free-coverage watch item conditioned
  on burnt_fraction; complete `phase4_report.md`. **STOP — Phase 4 end;
  Phase 5 GO/NO-GO is human.**

## Working agreements (beyond CLAUDE.md)

- GPU jobs: no local CUDA (GTX 1650 display only). The human runs shell
  scripts you place in `che/scripts/` on a vast.ai RTX 5090 box (git
  pull → `bash che/scripts/<job>.sh 2>&1 | tee <tag>_console.log`) and
  brings results back into `che/bench/results/`. Orbax checkpoint dirs
  stay on disk, out of git (m31b/m41 precedent).
- After each milestone: `uv run ruff check che/`, full CPU suite
  (`uv run pytest che/tests -m "not slow"`), commit naming the
  milestone. Never start the next milestone red.
- Obs v1/v2 are archival — no cross-version comparisons, ever.
- Milestones marked STOP end the turn: report and wait for the human.
