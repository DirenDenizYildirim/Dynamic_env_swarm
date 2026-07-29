
## M0.6 — second gate measurement: training throughput

- Device: **NVIDIA GeForce RTX 5090**; population 12, n_envs 256, grid 64², 12 agents, rollout 128, K_pbt 20
- Compile: 55.28 s; window rates: 142,277, 142,477, 142,421
- **Aggregate training throughput: 142,421 steps/s** (IQR 200); peak device memory 22.78 GiB
- **Verdict (training thresholds): PASS — acceptable**
- Budget: 86e9 steps -> 167.7 GPU-hours; ~$151 at $0.45/h with x2 buffer

