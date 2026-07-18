# Phase 0 — Substrate + Hybrid Training Loop (with go/no-go throughput gate)

> Paste this into a fresh Claude Code session at the repo root. `CLAUDE.md`
> and `docs/theory_foundations.md` must already be in place. Work strictly
> milestone by milestone; stop at each STOP line and report before continuing.

## Context

You are building Phase 0 of the CHE project (see CLAUDE.md). Phase 0 validates
the two hardest engineering risks before any domain complexity: (1) can the
CA-hazard grid stay GPU-batched at swarm scale inside a pure-JAX rollout, and
(2) does the vmap'd-population PBT + IPPO hybrid train end to end. The hazard
kernel is *built and benchmarked* in this phase but does **not** yet affect
agents (that's Phases 1–2). No couplings yet (Phases 3–4). No comms yet
(Phase 5).

## Objective

A repo where: `pytest` passes on CPU in <2 min; `bench/throughput.py`
produces the gate report; and a 12-member population of IPPO learners trains
on a stub foraging task inside one compiled call, with checkpoint/resume
proven by a kill-and-resume test.

---

## Milestone 0.1 — Scaffold

- `uv` project, deps per CLAUDE.md stack list, `ruff` config, `pytest` config.
- `che/env/types.py`: `EnvState` as a `chex.dataclass` with fields for agent
  positions/alive flags/task state, hazard grid (uint8: Fuel/Burning/Burnt),
  smoke grid (float32), structure grid (uint8), PRNG key, timestep.
- `che/env/config.py`: frozen dataclasses. `ThetaConfig(beta, kappa_A,
  kappa_B, delta)` + sub-params `(sigma_s, eta, iota, ...)`; `EnvConfig(grid
  side L, n_agents, horizon, obs window k, ...)`; `TrainConfig`;
  `configs/debug.yaml` (16×16, 4 agents, 2 envs, pop 2) and
  `configs/reference.yaml` (64×64, 12 agents, 1024 envs, pop 12).
- **Accept:** `uv run pytest` runs (trivial test), `ruff` clean.

## Milestone 0.2 — CA hazard kernel + smoke field (standalone)

Implement `che/env/hazard.py` per Def. 3 and Def. 6 of the theory doc:

- Constant-burn-time fire CA: each Burning cell ignites each Fuel von-Neumann
  neighbor independently w.p. `beta`; Burning→Burnt after one step; optional
  spontaneous ignition `iota` (default 0). Implement neighbor influence as a
  convolution / padded shifts; per-cell independent transmission implemented
  so the bond-percolation coupling of Prop. 2 holds (per-edge independent
  uniforms are fine to approximate with per-cell-per-direction uniforms —
  document the choice in a comment; exactness of Prop. 2 is only needed
  qualitatively, Phase 2 calibrates empirically).
- Smoke: `rho' = exp(-eta)*rho + sigma_s * (h == Burning)`.
- A `seed_ignitions(h, mask)` helper (used later by Coupling A; here for tests).
- Honor invariant #3: unconditional PRNG consumption.
- **Tests:** purity/determinism (same key ⇒ identical rollout; different keys
  ⇒ different); chex shapes/dtypes; absorbing Burnt; smoke decays
  exponentially after burnout (fit log-slope ≈ −eta); monotonicity smoke test:
  on 32×32, single center ignition, mean burnt fraction over ≥200 keys is
  increasing across beta ∈ {0.2, 0.5, 0.8} with clear separation.
- **Accept:** suite green on CPU. STOP: report kernel design choices.

## Milestone 0.3 — Stub environment + batched rollouts

- `che/env/tasks.py`: foraging stub — F food items on the grid; an agent on a
  food cell collects it (+1 team reward, item disappears); horizon 256.
  Reward reads task variables only (invariant #1) — add
  `tests/test_reward_independence.py` now.
- `che/env/env.py`: `reset(key, cfg) -> (obs, state)` and `step(key, state,
  actions) -> (obs, state, reward, done, info)` composing the Prop.-1 order.
  In Phase 0 the hazard/smoke/structure updates run every step (so the gate
  measures the real per-step cost) but do not affect agents; agents take
  5 discrete actions (4 moves + stay). Egocentric observation: k×k crop of
  (hazard, smoke, food) planes via `lax.dynamic_slice` on a padded grid +
  own-state vector. `info` includes the coupling-co-active counter (zeros for
  now, but the field and plumbing exist — invariant #5).
- `che/train/rollout.py`: `lax.scan` episode rollout; `vmap` over `n_envs`.
- **Tests:** env purity; food conservation; obs crop correctness at borders;
  a random-policy rollout at debug scale returns finite rewards.
- **Accept:** suite green. STOP.

## Milestone 0.4 — ★ THE GATE ★ env throughput on target GPU

`bench/throughput.py`:

- Protocol: build jitted batched `step` with random actions; report compile
  time separately; then time ≥5 measurement windows of ≥30s each; report
  median and IQR of **aggregate env-steps/sec = n_envs × steps/sec-per-env**.
- Measure the matrix: grid ∈ {32², 48², 64²} × n_envs ∈ {256, 1024, 4096} ×
  n_agents ∈ {8, 12} — reference cell is (64², 1024, 12). Also report peak
  device memory. Output a markdown table to `bench/results/`.
- Run on the actual rented GPU (4090 or A100 spot). Provide the exact
  command and a one-line vast.ai-friendly setup script.

**Corrected budget math the gate protects (do not use the stale 65-hour
figure):** total experiment budget ≈ 86B aggregate steps. Hours =
86e9 / throughput / 3600. Thresholds on *training* throughput (measured at
M0.6, but env-only throughput at M0.4 is the leading indicator — training is
typically 2–5× slower than env-only, so apply the ladder if env-only < 5×
the training threshold):

| Aggregate training steps/sec | GPU-hours | Spot cost (×2 buffer) | Verdict |
|---|---|---|---|
| ≥ 200k | ≤ 120 | ≤ ~$110 | PASS — comfortable |
| 100k–200k | 120–240 | ~$110–215 | PASS — acceptable |
| 30k–100k | 240–800 | ~$215–720 | FALLBACK LADDER |
| < 30k | > 800 | > $720 | STOP — escalate to human |

**Fallback ladder (apply in order, re-measure after each; never skip to
escalation while rungs remain):** 1) grid 64²→48²; 2) n_envs tuning for
occupancy; 3) n_agents 12→8; 4) grid 48²→32²; 5) population 12→10 (M0.6
only). Report every rung applied. **Never** change horizon accounting, seed
count, or silently reduce planned experiment steps.

- **Accept:** gate report table exists with a verdict. STOP: present the
  report to the human before proceeding — this is a go/no-go decision point.

## Milestone 0.5 — IPPO on the stub task (single policy)

- `che/train/networks.py`: shared-parameter actor-critic (parameter sharing
  across agents — standard for homogeneous swarms; leave a `# DECISION:`
  note). Small CNN on the obs crop → MLP heads.
- `che/train/ippo.py`: PureJaxRL-style — collect with `lax.scan`, GAE(λ),
  clipped surrogate, entropy bonus, minibatched epochs, all jitted end to end.
- Orbax checkpointing every K updates + SIGTERM handler; kill-and-resume test
  (resume from checkpoint, loss/metrics continue sanely).
- **Accept:** at debug-or-slightly-larger scale, mean episodic return clearly
  exceeds the random-policy baseline (report a learning curve PNG via a
  `scripts/` plot). Suite green. STOP.

## Milestone 0.6 — PBT population loop (the hybrid)

- `che/train/pbt.py`: population P=12 as an outermost `vmap` over per-member
  (params, opt-state, hyperparams: lr, entropy coef). Every K_pbt updates:
  fitness = mean return over the recent window; bottom quartile copies a
  uniformly sampled top-quartile member's weights and mutates hyperparams by
  ×U{0.8, 1.25} (truncation selection, per Jaderberg et al. 2017). Selection
  can sit outside jit at the PBT boundary; the K_pbt inner updates must be
  one compiled call.
- **Tests/verification:** population trains (all members improve vs random);
  selection provably triggers (log exploit events); hyperparam diversity
  persists (not collapsed to one value immediately).
- **Second gate measurement:** aggregate *training* steps/sec with the full
  population, against the M0.4 table. Append to the gate report.
- **Accept:** report with training-throughput verdict + learning curves.
  STOP: Phase 0 complete — hand the final report to the human.

## Non-goals for Phase 0 (do not build)

Hazard–agent interaction, Coupling A/B logic beyond stubs/plumbing, comms,
severity calibration, evaluation harness, 3D anything, rendering beyond
matplotlib debug frames, hyperparameter search beyond PBT's own mutation.
