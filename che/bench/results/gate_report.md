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
