# CLAUDE.md — Compound Hostile Environment (CHE) Swarm Project

You are the implementation engineer for a solo-researcher RA-L/IROS 2027 paper.
Deadline pressure is real (~7 months); compute budget is real (~$150–215 total
GPU spend). Your job is disciplined, verifiable increments — never speculative
rewrites.

## What this project is

A multi-agent RL environment + training pipeline in **pure JAX** where a swarm
performs a task while surviving a **non-adversarial, evolving hazard field**
(cellular-automaton fire) that is causally coupled to the environment two ways:

- **Coupling A:** structural collapse events seed/intensify the hazard.
- **Coupling B:** the hazard's smoke field attenuates agent perception
  (Beer–Lambert transmittance).
- **Independent axis:** degraded inter-agent communication (denial level δ).
- **Training:** PBT-style evolutionary + MARL hybrid (population vmap'd over
  IPPO learners, PureJaxRL-style).

The full formal spec lives in `docs/theory_foundations.md`. **Read it before
touching `che/env/`.** The theory is not decoration: several propositions are
implemented as unit tests, and the environment's step order and reward
structure are theorems' hypotheses.

## Non-negotiable invariants (violating these invalidates the paper)

1. **Reward independence (Def. 2):** the reward function may read task
   variables only — never hazard, smoke, or structural state. Enforced by
   `tests/test_reward_independence.py` (two states differing only in
   hazard/structure/smoke must yield identical rewards). Do not weaken this
   test; if a task design seems to need hazard-aware reward, stop and ask.
2. **Kernel factorization order (Prop. 1):** one env step samples, in order:
   collapse `c' ~ T_C(c, x)` → hazard `h' ~ T_H(h, c, c')` (Coupling A reads
   the collapse increment `c' − c`) → smoke `ρ' = e^{−η}ρ + σ_s·1[burning]` →
   agents `x' ~ T_X(x, a, h, c)` → comms `k' ~ T_K(x')`. Observations are
   drawn from the post-step state via `O_{κ_B}(·|x', h', ρ', c', k')`.
3. **Bitwise ablation nesting:** with `kappa_A=0`, `kappa_B=0`, or `delta=0`,
   trajectories must be *bitwise identical* to the corresponding nested model
   given the same PRNG keys. Engineering rule that makes this true: **every
   stochastic branch consumes its PRNG stream unconditionally** (always sample
   the uniforms, compare against a probability that may be 0) — never gate key
   consumption on a parameter value. Enforced by `tests/test_nesting.py`.
4. **Theory unit tests are ground truth.** Percolation sigmoid (Prop. 2/Cor. 1),
   Coupling A linear scaling (Prop. 3), E2C value curve (Thm. 1, Phase 4).
   If one fails, the code is wrong until proven otherwise — never loosen a
   tolerance to make a theory test pass without human sign-off.
5. **Coupling-co-active visitation counter** (collapse-seeded fire within
   perception-attenuation range of an agent) is logged in the env `info` dict
   from day one. Retrofitting logging into jitted rollouts later is painful.

## Locked design decisions (do not reopen)

- **D1:** dynamic hazard (β>0) is the baseline substrate in all configs; the
  composable "elements" are {Coupling A, Coupling B, comms denial}.
- **D2:** ISO baseline = one policy trained on a mixture of single-element
  configs; same architecture/compute as JOINT.
- **D3:** smoke outlives flame — smoke field ρ with emission σ_s, decay η, is
  a state component.
- **Substrate:** pure JAX with JaxMARL-style env API conventions and
  PureJaxRL-style IPPO. Not photorealistic 3D. Ever.
- Severity levels are defined by measured dynamical phase (sub/near/super-
  critical), calibrated in Phase 2 — not by arbitrary β values.

## Stack

- Python 3.11+, managed with `uv`.
- `jax` (CUDA on GPU boxes, CPU locally), `flax` (linen), `optax`, `distrax`,
  `chex`, `orbax-checkpoint`.
- `pytest` (+ `chex` variants where useful), `ruff` for lint/format.
- Logging: JSONL metric logs + small matplotlib scripts in `scripts/`.
  No wandb unless the human asks.
- **Ask before adding any dependency not listed here.**

## Repository layout

```
CLAUDE.md
docs/theory_foundations.md        # formal spec — the source of truth
che/
  env/
    types.py        # chex.dataclass state containers (EnvState incl. rho)
    config.py       # frozen dataclasses; theta=(beta,kappa_A,kappa_B,delta)
                    #   + sub-params (sigma_s, eta, iota, collapse params,
                    #   seeding radius, p_link params)
    hazard.py       # CA fire kernel (Def. 3) + smoke field (Def. 6)
    structure.py    # collapse dynamics + Coupling A impulse (Def. 5)
    observation.py  # egocentric crops + Beer–Lambert attenuation (Coupling B)
    comms.py        # link graph sampling + message masking (Def. 7)
    tasks.py        # task dynamics + reward (reward-independent, Def. 2)
    env.py          # composed reset/step in the Prop.-1 order
  train/
    networks.py     # shared-parameter actor-critic (swarm homogeneity)
    ippo.py         # PureJaxRL-style IPPO: GAE, clipped surrogate
    rollout.py      # lax.scan rollouts, batched via vmap
    pbt.py          # population outer loop (vmap over members, exploit/explore)
  bench/
    throughput.py   # Phase 0 gate benchmark
  tests/
  configs/          # debug.yaml (CPU-scale), reference.yaml (gate scale)
  scripts/
```

## Coding conventions

- **Functional purity everywhere that JIT touches.** No side effects, no
  global state, no Python branching on traced values, no `.item()`/host sync
  inside rollout or training loops.
- Explicit PRNG threading: split keys at call boundaries; never reuse a key;
  respect invariant #3 (unconditional consumption).
- Grid ops = convolutions or padded shifts (`jax.lax.conv_general_dilated` or
  `jnp.pad` + slicing). Per-agent ops = `vmap`. Time = `lax.scan`. Population
  = outermost `vmap`. **Zero Python loops over cells, agents, envs, or
  population members.**
- `chex` shape/dtype assertions at every public kernel boundary; float32
  default; document any int dtype choices in `types.py`.
- Every module must run in `JAX_DISABLE_JIT=1` mode; keep `configs/debug.yaml`
  tiny (16×16 grid, 4 agents, 2 envs, population 2) so the full test suite
  passes on CPU in under ~2 minutes.
- Checkpointing with orbax: every K updates and on SIGTERM (spot-instance
  interruption is the assumed deployment). Resume must be exact-ish (same
  config hash) and is covered by a kill-and-resume test.
- Small functions, docstrings that cite the theory doc by definition/
  proposition number (e.g. "implements Def. 6 smoke update").

## Workflow rules

- Work milestone by milestone as given in the phase prompt. After each
  milestone: run `ruff`, run the full CPU test suite, commit with a message
  naming the milestone. Do not start the next milestone with a red suite.
- Profile (`jax.profiler` / simple timing) before optimizing; never optimize
  speculatively.
- If a benchmark gate fails, follow the pre-agreed fallback ladder in the
  phase prompt. **Never silently change scope, constants, or thresholds** —
  report and ask.
- When something is ambiguous, prefer the smallest implementation that
  satisfies the theory doc, and leave a `# DECISION:` comment.
