# Phase 1 — Final Report (hazard–agent interaction + static control)

Date: 2026-07-19. Milestones M1.1–M1.5 complete; suite: 69 tests green on
CPU (~77 s jitted; everything also runs under `JAX_DISABLE_JIT=1`).
Training runs: RTX 5090, jax 0.11, commit `ceef08c` code state.

## What Phase 1 built

- **M1.1 lethality/blocking:** T_X reads h'/c' — Burning kills (evaluated
  post-move against the post-update hazard), Collapsed blocks (Burnt is
  passable), collapse under an occupant kills with no same-step escape
  (human-locked), dead agents are inert attrition. Optional
  Def.-2-compliant `death_penalty` (reads only the α transition).
- **M1.2 obs v1 locked:** 5 planes (hazard/2, smoke, food, structure,
  alive occupancy incl. self), k = 9. Reference-cell bench: **12.65M
  env-steps/s** (−1.6 % vs Phase 0's 3-plane k=5 obs) — see gate report;
  uint8 contingency untriggered.
- **M1.3 frozen-hazard control:** `hazard_mode="frozen"`, t_gen burn-in
  (default horizon/2), bitwise PRNG discipline across modes (nesting-suite
  proven). Note: at 64²/β=0.35 the subcritical fire typically burns out
  before the freeze — the control matches the dynamic env's (mostly
  hazard-free) mid-episode marginal, faithfully.
- **M1.4 episode metrics:** survival_rate, completion, deaths_fire,
  deaths_collapse at done; NaN-safe wiring through IPPO/PBT logs + plots.

## M1.5 acceptance runs

Config: `phase1_accept.yaml` — dynamic mode, β=0.35 (placeholder), 64²,
12 agents, horizon 256, single policy, n_envs 256, rollout 128,
500 updates; seeds 0. Two runs: death_penalty 0.0 and 0.5.

| Metric (final-100-update mean) | random baseline | dp = 0.0 | dp = 0.5 |
|---|---|---|---|
| mean episodic return | 7.28 | **23.10** | **23.30** |
| completion | 0.227 | **0.722** | **0.729** |
| survival_rate | 0.99821 | 0.99648 | 0.99687 |
| deaths_fire / episode | 0.0215 | 0.0416 | 0.0373 |
| deaths_collapse / episode | 0 | 0 | 0 (λ₀ = 0) |

Baseline provenance: GPU run (64 episodes: return 6.86, survival 1.0, 0
deaths — small-sample) refined on CPU with 512 episodes (seed 1):
return 7.28, survival 0.99821, deaths 0.0215/ep. The 512-episode row is
used above. Raw files: `random_baseline.json`, `ippo_dp00.jsonl`,
`ippo_dp05.jsonl`; curves: `curves_dp00.png`, `curves_dp05.png`.

## Verdict against the acceptance criterion

- **Completion: PASS, decisively.** 0.72–0.73 vs 0.23 — a 3.2× margin,
  stable from ~update 100 onward.
- **Survival_rate: the criterion is unmeetable at this β, and the trained
  policy is marginally *below* baseline.** At β=0.35 (subcritical, single
  ignition) the expected burnt cluster is a handful of cells on a 4096-cell
  arena: random walkers rarely meet it (survival 0.9982 ≈ ceiling).
  Trained foragers sweep far more area, so their exposure roughly doubles
  (0.042 vs 0.021 deaths per 12-agent episode; every gap here is ≪ 1 agent
  per episode). "Beating the baseline visibly" on survival is impossible
  when the baseline sits at a 99.8 % ceiling — the placeholder severity,
  not the policy, is the binding constraint.
- Death penalty does act in the right direction: at equal completion,
  dp=0.5 lowers fire deaths ~11 % (0.0416 → 0.0373). The reward channel
  works; the incentive is just tiny (0.5 penalty vs ~23 of food return).

**Recommendation (human call required — criterion not literally met):**
accept Phase 1 on the completion margin + mechanism evidence (deaths
occur, penalty shifts them, all M1.1 semantics unit-pinned), and treat
survival as a discriminating axis only at Phase-2-calibrated severities —
Medium/High are precisely the regimes where the ceiling disappears. The
alternative is one more GPU run pair at a hotter placeholder (e.g.
β=0.5) purely to demonstrate a survival margin pre-calibration.

## Engineering invariants extended this phase

Nesting suite grew from 3 to 8 bitwise tests (death logic consumes no
PRNG; death_penalty is reward-only; dynamic↔frozen differ only through
the freeze; sharpened structure/β cross-tests for the legitimately opened
T_X channels). Reward-independence now pins the α transition equal
(far-field construction) including death_penalty > 0.
