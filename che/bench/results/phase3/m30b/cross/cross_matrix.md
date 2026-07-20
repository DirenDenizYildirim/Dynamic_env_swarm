# M3.0b Audit 2 — cross-severity 3x3 matrix

9 checkpoints (3 train severities x 3 seeds, dp=0.5) x 3 eval envs, 512 episodes/cell/seed, eval seed 0, stochastic policy as-trained. Code: pinned 8de4976 worktree.

**Completion** (rows = training severity, cols = eval severity; pooled over seeds [0, 1, 2], per-episode mean ± std)

| train \ eval | Low | Medium | High |
|---|---|---|---|
| **Low** | 0.737 ± 0.115 | 0.728 ± 0.118 | 0.604 ± 0.123 |
| **Medium** | 0.764 ± 0.114 | 0.762 ± 0.114 | 0.690 ± 0.132 |
| **High** | 0.738 ± 0.119 | 0.739 ± 0.119 | 0.797 ± 0.117 |

**Survival rate** (rows = training severity, cols = eval severity; pooled over seeds [0, 1, 2], per-episode mean ± std)

| train \ eval | Low | Medium | High |
|---|---|---|---|
| **Low** | 0.993 ± 0.030 | 0.927 ± 0.118 | 0.420 ± 0.164 |
| **Medium** | 0.997 ± 0.019 | 0.954 ± 0.085 | 0.452 ± 0.172 |
| **High** | 0.995 ± 0.021 | 0.968 ± 0.067 | 0.889 ± 0.105 |

**Completion | zero-deaths (episodes with no fire or collapse deaths)** (rows = training severity, cols = eval severity; pooled over seeds [0, 1, 2], per-episode mean ± std)

| train \ eval | Low | Medium | High |
|---|---|---|---|
| **Low** | 0.739 ± 0.115 (N=1425) | 0.734 ± 0.118 (N=936) | 0.688 ± 0.133 (N=24) |
| **Medium** | 0.765 ± 0.114 (N=1482) | 0.766 ± 0.115 (N=1072) | 0.749 ± 0.130 (N=24) |
| **High** | 0.739 ± 0.119 (N=1459) | 0.744 ± 0.116 (N=1147) | 0.836 ± 0.110 (N=489) |

## Reading (local run 2026-07-20; H1/H2 verdict mapping left to the human's
## registered hypothesis statements, which this file does not restate)

Integrity: the 9 diagonal cells reproduce the M3.0 GPU eval means to 3
decimals (max |Δ| = 0.001; per-episode arrays differ bitwise — known
GPU-vs-CPU float divergence, platform-level, same caveat as the M3.0
checkpoint provenance note). 25/27 cells from one driver run at pinned
8de4976; the 2 remaining (train_high_s2 × eval {medium, high}) were
topped up by the identical code path after the run was interrupted.

- **Fixed policy, varying environment (across a row):** every policy is
  near-indifferent between Low and Medium environments (completion drops
  ≤ 0.01, survival ≥ 0.93 everywhere) — the discriminating environment is
  High only. Low/Medium-trained policies lose about half the swarm there
  (survival 0.42 / 0.45; only 24/1536 episodes death-free) and completion
  falls to 0.60 / 0.69.
- **Fixed environment, varying training (down a column):** survival on any
  environment orders monotonically with training severity (High column:
  0.889 vs 0.452 vs 0.420) — hazard-coping transfers *down* and is never
  costly (High-trained survival matches Low-trained even on Low, 0.995 vs
  0.993). Completion does **not** order the same way: in benign
  environments the best collector is Medium-trained (0.764/0.762 vs
  High-trained 0.738/0.739 and Low-trained 0.737/0.728); High-trained
  completion dominance exists only on High (0.797 vs 0.690/0.604).
- **The specialization is not (only) attrition.** Conditioning on
  zero-death episodes, Low/Medium-trained policies on High still complete
  only 0.688/0.749 vs High-trained 0.836 — even when nobody dies, they
  collect less. This matches Audit 1's behavioral finding
  (`render_notes.md`): non-High policies avoid burnt terrain, and on the
  High environment nearly the whole arena is burnt from mid-episode on,
  so terrain avoidance directly caps collection. High training is, in
  part, learning that ash is safe.
- **Seed caveat:** High-trained pooled numbers lean on seed 2
  (diagonal completion 0.869/0.956 survival vs 0.786/0.863 and
  0.736/0.848 for seeds 0/1) — the known High-severity training-solution
  diversity (Phase-6 seed-budgeting note in `def4_variance.md`).
