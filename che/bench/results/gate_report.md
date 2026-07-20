# M0.4 throughput gate report

- Device: **NVIDIA GeForce RTX 5090** (gpu), jax 0.11.0
- Generated: 2026-07-18 13:02:20 UTC
- Protocol: jitted batched step, random actions, AOT compile timed separately, median/IQR over measurement windows, aggregate env-steps/sec = n_envs x steps-per-env / elapsed.

| grid | n_envs | n_agents | compile (s) | median steps/s | IQR | peak mem (GiB) |
|---|---|---|---|---|---|---|
| 32² | 256 | 8 | 2.2 | 8,430,360 | 30,423 | 0.02 |
| 32² | 256 | 12 | 2.14 | 8,427,177 | 32,962 | 0.02 |
| 48² | 256 | 8 | 2.29 | 7,382,591 | 17,830 | 0.02 |
| 48² | 256 | 12 | 2.22 | 6,978,834 | 21,407 | 0.02 |
| 32² | 1024 | 8 | 2.32 | 24,249,914 | 312,675 | 0.03 |
| 64² | 256 | 8 | 2.22 | 6,359,129 | 11,425 | 0.03 |
| 32² | 1024 | 12 | 2.28 | 23,929,838 | 76,522 | 0.03 |
| 64² | 256 | 12 | 2.28 | 6,302,872 | 10,603 | 0.03 |
| 48² | 1024 | 8 | 2.29 | 17,912,485 | 7,683 | 0.06 |
| 48² | 1024 | 12 | 2.22 | 17,315,204 | 18,215 | 0.06 |
| 32² | 4096 | 8 | 2.3 | 50,053,325 | 58,543 | 0.12 |
| 64² | 1024 | 8 | 2.18 | 12,888,852 | 27,359 | 0.12 |
| 32² | 4096 | 12 | 2.19 | 48,817,642 | 30,674 | 0.12 |
| 64² ★ | 1024 | 12 | 2.24 | 12,861,356 | 23,347 | 0.12 |
| 48² | 4096 | 8 | 2.11 | 27,484,445 | 68,744 | 0.28 |
| 48² | 4096 | 12 | 2.07 | 26,666,055 | 31,417 | 0.29 |
| 64² | 4096 | 8 | 2.26 | 15,506,815 | 27,470 | 0.49 |
| 64² | 4096 | 12 | 2.22 | 15,322,470 | 22,526 | 0.50 |

## Verdict — reference cell (64², 1024, 12)

- Env-only aggregate throughput: **12,861,356 steps/s**
- Env-only verdict (5x training thresholds): **PASS — comfortable**

Budget projection (86e9 aggregate steps; training typically 2-5x slower than env-only):

| assumed training slowdown | training steps/s | GPU-hours | spot cost (x2 buffer @ $0.45/h) |
|---|---|---|---|
| 2x | 6,430,678 | 4 | ~$3 |
| 5x | 2,572,271 | 9 | ~$8 |

Final go/no-go uses *training* throughput measured at M0.6; this env-only figure is the leading indicator.

## M0.6 — second gate measurement: training throughput

- Device: **NVIDIA GeForce RTX 5090**; population 12, n_envs 256, grid 64², 12 agents, rollout 128, K_pbt 20
- Compile: 57.94 s; window rates: 159,042, 159,011, 159,030, 158,953, 158,996
- **Aggregate training throughput: 159,011 steps/s** (IQR 61); peak device memory 19.20 GiB
- **Verdict (training thresholds): PASS — acceptable**
- Budget: 86e9 steps -> 150.2 GPU-hours; ~$93 at $0.31/h with x2 buffer

## Phase 1 obs v1 — reference cell re-measurement (M1.2)

| grid | n_envs | n_agents | compile (s) | median steps/s | IQR | peak mem (GiB) | obs |
|---|---|---|---|---|---|---|---|
| 64² ★ | 1024 | 12 | 2.28 | 12,652,933 | 210,353 | 0.12 | v1: k=9, 5 planes |

- Same protocol/device as M0.4 (RTX 5090, jax 0.11.0); raw JSON:
  `obs_v1_ref_cell.json` (commit 046dccc code state).
- Env-only cost of the k=5→9, 3→5-plane crop vs the M0.4 row: **−1.6 %**
  (12,861,356 → 12,652,933) — the obs pipeline is not the bottleneck.
- Training projection at the measured Phase-0 env:train ratio (÷81):
  **~156.2k train steps/s**, comfortably above the 100k contingency line —
  the uint8-obs-storage contingency stays untriggered.
- **Verdict: PASS — obs v1 locked with no operating-point change.**

## Phase 3 obs v2 — reference cell re-measurement (M3.1b / D5)

| grid | n_envs | n_agents | compile (s) | median steps/s | IQR | peak mem (GiB) | obs |
|---|---|---|---|---|---|---|---|
| 64² ★ | 1024 | 12 | 1.92 | 9,580,456 | 10,985 | 0.15 | v2: k=9, 7 planes |

- Same protocol/device as M1.2 (RTX 5090, jax 0.11.0); raw JSON:
  `phase3/m31b/obs_v2_ref_cell.json` (commit 1706cb6 code state).
- Env-only cost of the 5→7-plane indicator crop vs the M1.2 row:
  **−24.3 %** (12,652,933 → 9,580,456) — **not** the ~neutral D5 expected;
  deviation flagged, no scope change made (see `phase3/m31b_obs_v2.md`).
- End-to-end training cost is much smaller: −7 % (70.9k → 66.0k
  env-steps/s on the M3.0-vs-M3.1b severity probes, 266 s → 285 s per
  500-update run) — the env is a small share of a train step.
- Training projection at the measured Phase-0 env:train ratio (÷81):
  **~118.3k train steps/s — above the 100k contingency line**, margin
  reduced from ~56k to ~18k. Contingency stays untriggered.
- **Verdict: PASS with flag — obs v2 locked (D5); throughput margin
  thinner than expected, human review at the M3.1b STOP.**

