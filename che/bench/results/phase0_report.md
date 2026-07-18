# Phase 0 — Final Report (substrate + hybrid training loop)

Date: 2026-07-18. All six milestones complete; suite: 38 tests green on CPU
(~43 s jitted; everything also runs under `JAX_DISABLE_JIT=1`).

## Gate verdicts (RTX 5090, jax 0.11)

| Measurement | Config | Result | Verdict |
|---|---|---|---|
| M0.4 env-only | 64², 1024 envs, 12 agents | **12.86 M steps/s** (IQR 23 k) | PASS — comfortable |
| M0.6 training (PBT pop 12) | 64², **256 envs/member**, 12 agents, rollout 128, K_pbt 20 | **159.0 k steps/s** (IQR 61) | **PASS — acceptable** |

Budget at measured training throughput: 86e9 steps → **150.2 GPU-hours ≈
$93** at the actual $0.31/h spot rate with the ×2 buffer — inside the
locked $110–215 acceptable band (and under the $110 comfortable line).

### Deviation applied (fallback ladder rung 2 — reported, not silent)

The M0.6 bench at the reference `n_envs=1024` exceeds device memory:
peak is already 19.2 GiB at 256 envs/member (the PPO minibatch pipeline
holds each member's full rollout batch plus permutation copies), so 1024
envs/member (~4×) does not fit a 32 GB card. Operating point moved to
`n_envs=256` per member (12 members × 256 = 3 072 concurrent envs), i.e.
rung 2 of the pre-agreed ladder (n_envs tuning). No change to horizon
accounting, seed counts, or planned experiment steps. Config recorded in
`che/configs/m06_probe.yaml`.

Note the env-only:training gap is ~81×, far beyond the 2–5× heuristic —
as anticipated, the env is so fast that training is network-bound. The
margin absorbs it; the binding number above is the measured 159 k/s.

## Training acceptance evidence

- **M0.5 single-policy IPPO** (24², 4 agents, 16 envs, 300 updates):
  final return ~5.6 vs random baseline 3.31 (+70 %).
  `m05/learning_curve.png`.
- **M0.6 PBT population** (64², 12 agents, pop 12, 40 rounds × K_pbt 20 =
  800 updates): every member improves — first-40-update means 13.2–15.5 →
  final-100-update means 18.0–19.1, vs random baseline 6.86.
  `m06/pbt_curves.png`.
- **Selection provably triggers:** 120 exploit events (3/round × 40
  rounds), logged with source/target fitness and hyper mutations in
  `m06/events.jsonl`.
- **Hyperparam diversity persists:** 6 distinct learning rates at update
  800; the lr trajectories show mutation-driven drift from ~5e-4 toward
  ~2e-4 (population-discovered annealing), not collapse.
- **Spot-instance resilience:** kill-and-resume and SIGTERM-save tests
  green for both single-policy and population checkpoints (orbax, config-
  hash-guarded).

## Engineering invariants in force since day one

reward independence test (Def. 2); Prop.-1 kernel order in `env.step`;
unconditional PRNG consumption (bitwise nesting at kappa/delta = 0);
coupling-co-active counter live in `info`; theory tests as ground truth
(beta-monotonicity: burnt fraction 0.003 / 0.32 / 0.996 at beta
0.2 / 0.5 / 0.8 — consistent with beta_c = 1/2).

## Verdict

**Phase 0 complete — GO for Phase 1** (hazard–agent interaction) at the
recorded operating point.
