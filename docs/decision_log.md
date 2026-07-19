# Decision log

Locked design decisions. Entries are append-only; reopening one requires an
explicit human call recorded here. D1–D3 predate this file and are restated
from `CLAUDE.md` (which remains authoritative for them); D4 onward are
recorded here first.

## D1 — Dynamic hazard is the baseline substrate (Phase 0)

Dynamic hazard (β > 0) is the baseline substrate in all configs; the
composable "elements" are {Coupling A, Coupling B, comms denial}.

## D2 — ISO baseline definition (Phase 0)

ISO baseline = one policy trained on a mixture of single-element configs;
same architecture/compute as JOINT.

## D3 — Smoke outlives flame (Phase 0)

Smoke field ρ with emission σ_s and decay η is a state component (Def. 6);
smoke persists after flame passes.

## D4 — death_penalty = 0.5 default for all training from Phase 3 onward (2026-07-19)

dp = 0 is demoted to a secondary ablation slot.

**Evidence (M2.5 pillar-only grid, 3 severities × dp ∈ {0.0, 0.5} × 3 seeds,
500 updates; `che/bench/results/phase2/phase2_report.md`):**

- Low: tied — survival at ceiling under both arms.
- Medium: modest consistent gain (survival 0.931 → 0.951, deaths −28%).
- High: decisive — survival 0.575 → 0.866, deaths_fire 5.10 → 1.61 (−68%),
  and completion *also* improves (0.765 → 0.821). At dp = 0 the
  return-optimal High policy spends agents for food; dp = 0.5 finds a policy
  better on both axes.

Note: dp = 0.5 is a shaping term on the task reward (agent death is a task
variable); reward independence (Def. 2) is unaffected — the reward still
reads no hazard/smoke/structure state.

Confirmed by human 2026-07-19 at Phase 3 start.
