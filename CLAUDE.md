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

Refreshed against the tree 2026-07-31. **Keep it that way**: the
phase-close checklist requires re-reading this block against the actual
tree, because a new session treats it as authoritative before it has read
any code. It previously omitted `che/calibration/` and `che/eval/`
entirely — about a third of the codebase.

```
CLAUDE.md
HANDOFF.md                        # session state for the next model
docs/
  theory_foundations.md           # formal spec — the source of truth
  locks.yaml                      # MACHINE-READABLE registry of every locked
                                  #   constant; asserted by tests/test_locks.py
  decision_log.md                 # rulings, in the order they were issued
  architecture_decisions_v1.md    # pre-Phase-0 architecture record
*_lock.md                         # per-axis lock records at repo root:
                                  #   severity_, coupling_a_, kappa_b_, comms_
che/
  env/
    types.py        # chex.dataclass state containers (EnvState incl. rho)
    config.py       # frozen dataclasses; theta=(beta,kappa_A,kappa_B,delta)
                    #   + sub-params (sigma_s, eta, iota, collapse params,
                    #   seeding radius, r_comm)
    hazard.py       # CA fire kernel (Def. 3) + smoke field (Def. 6)
    structure.py    # collapse dynamics + Coupling A impulse (Def. 5)
    observation.py  # egocentric crops + Beer–Lambert attenuation (Coupling B)
    comms.py        # link graph sampling + message masking (Def. 7)
    tasks.py        # task dynamics + reward (reward-independent, Def. 2)
    env.py          # composed reset/step in the Prop.-1 order
    e2c.py          # Thm.-1 memorization-gap harness (E2C, Phase 4)
    e2c2.py         # E2C² — the comms-coupled variant (Remark 2″, Phase 5)
  train/
    networks.py     # shared-parameter actor-critic (swarm homogeneity)
    ippo.py         # PureJaxRL-style IPPO: GAE, clipped surrogate
    rollout.py      # lax.scan rollouts, batched via vmap
    pbt.py          # population outer loop (vmap over members, exploit/explore)
                    #   `--bench` is the throughput gate instrument
  calibration/      # measurement code behind the locks — NOT training
    percolation.py  # Prop. 2 / Cor. 1: P_span, R_L crossings, beta_c
    coupling_a.py   # Def. 5 calibration (collapse/seeding rates)
    coupling_b.py   # Def. 6 calibration (detection band, masked_frac)
    prop3.py        # Prop. 3 acceptance machinery
    estimates.py    # estimators + CIs shared by the above
    figures.py      # calibration figures
  eval/
    harness.py      # checkpoint -> policy -> episode eval -> summary JSON/NPZ
  bench/
    throughput.py   # Phase 0 gate benchmark (env-only; states keep-alive set)
    memprobe.py     # compile-time memory probe (M5.1 arena ladder)
    rowb_probe.py   # M5.1j row-B diagnostic
    results/        # phase{0..5} reports, metrics, provenance (large; most
                    #   checkpoints + renders are gitignored)
  tests/            # 29 files; theory tests are ground truth (invariant #4)
    golden/         # committed pre-refactor trajectory digests (M6.0a); the
                    #   cross-tree bitwise baseline for the traced-theta spike
  configs/          # severity_{low,medium,high}.yaml + gate_pop12.yaml are
                    #   live; debug.yaml is the CPU fixture; reference.yaml,
                    #   m06_probe.yaml, phase1_accept.yaml are ARCHIVAL
                    #   (pre-Phase-2 placeholder theta) — see docs/locks.yaml
  scripts/          # run_m*.sh GPU job scripts + plotting/report .py
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

### Phase-close checklist

At the close of every phase, in addition to the per-milestone routine:

- [ ] **CLAUDE.md layout refreshed against the tree.** (human-issued
      2026-07-31) Doc-rot here is worse than elsewhere: a new session reads
      the layout block on day zero and treats it as authoritative. It had
      drifted to omit `che/calibration/` and `che/eval/` entirely.
- [ ] Every lock ruled during the phase is in `docs/locks.yaml` and
      `che/tests/test_locks.py` is green.
- [ ] Phase report written; GPU artifacts archived off-instance with
      `sha256` recorded (see the artifact-persistence rule).
- [ ] `HANDOFF.md` rewritten for the next session.

## Rulings bind only once transcribed (meta-rule, human-issued 2026-07-28)

**A chat ruling binds only once it is transcribed into `decision_log.md` or
`CLAUDE.md` in the same session.** Untranscribed directives are proposals;
citing one as if it were repo law is an error, not a shortcut. Transcribe
first, then act. (Origin: "tooling rule 3c/3d" was cited for months as
binding and existed only in a chat transcript — its archive half was never
implemented, and M4.4 shipped without a checkpoint archive as a result.)

### Sub-rule: numerical claims enter documents *derived* (human-issued 2026-07-28)

**A number reaches `docs/` only through a derivation or a measurement made
in the same session — never transliterated from a chat heuristic, however
plausible it sounded in conversation.** Heuristics carry their assumptions
silently: `q̃/q → 5/3` was a small-`p`, equal-exponent approximation, and
writing it into Remark 2″ as `κ_B → ∞` behaviour turned a safe estimate into
a false asymptotic claim. If a constant cannot be derived on the spot, state
the inequality and defer the constant to the milestone that measures it.
This binds both roles: the builder who offers a heuristic must label it one,
and the transcriber must harden it or drop it before it enters a document.

## Locks are enforced by test, not by memory (human-issued 2026-07-31)

**Every locked constant lands in `docs/locks.yaml` in the same commit its
ruling is transcribed, and `che/tests/test_locks.py` asserts that the
configs and the `che/env/config.py` defaults agree with it.** A locked
value must be *reachable from a config* — never supplied only by a
command-line flag, and never left to a dataclass default in the configs
that are required to carry it. `locks.yaml` records constants only; every
entry cites the document that ruled it.

Origin: **R_comm was locked at 16 on 2026-07-30 and was unreachable from
any config for a day.** `ThetaConfig.r_comm` defaulted to 8.0, no YAML set
it, and the locked geometry existed only as `--r-comm 16` inside two shell
scripts — a geometry whose own lock record notes that R = 8 misses the
prior band it was locked to hit. Nothing failed, because nothing checked.
The same defect class is currently open for `death_penalty` (D4 locks 0.5;
the configs carry 0.0 and every script passes `--death-penalty 0.5`),
recorded in `locks.yaml` with a human ruling owed.

This rule is the class-level fix for the same failure the transcription
meta-rule addresses at the ruling level: **a lock that lives only in prose
is inherited by memory, and memory is not a mechanism.**

## Throughput gates bind to measured training throughput (human-issued 2026-07-28)

**Throughput gates bind only to measured training throughput of the
spending consumer; any env-only figure states its keep-alive set;
projections are estimates, never triggers.** Under XLA dead-code
elimination "env-only throughput" is not a single quantity — the compiler
deletes whatever the consumer does not read, so the same env measures
8.6 M steps/s for a probe that ignores the info channels and 3.4 M for one
that reads them all. The ÷81 projection that gated Phases 0–4 was therefore
attached to a number whose meaning drifted every time a diagnostic channel
was added unbenched. Measure what actually spends the budget: population-
aggregate training throughput at the phase's real configuration
(`pbt.py --bench`, `configs/gate_pop12.yaml`).

## Bars come with floors (human-issued 2026-07-30)

**No acceptance threshold enters any script without either a measured
floor for the quantity it grades (cited) or an explicit UNDERPOWERED flag
in its output. Thresholds finer than their instruments are void by
construction.**

A threshold set below its instrument's measured noise cannot pass under
the null, so it is not a test and its output is not evidence — void, not
failed, and the distinction is load-bearing because a *void* test voids a
PASS identically.

Origin: four bars set without floors in one phase. M4.4's `σ_seed` 0.0295
against a later-measured High floor of 0.0621; M5.3's hardcoded Medium
floor applied to a run on different hardware; M5.3b's 2×sd bar at High,
which no affordable seed count could reach (~46 seeds/arm); and M5.5's
20 % relative threshold on a quantity whose measured nondeterminism is
27.2 %. Accountability splits both ways: the invented constants were the
builder's, and the framework that asked for "within seed noise" and "no
cross-arm difference" four times without ever specifying *against what
floor* was the author's. This rule closes both ends.

**Floors are per-metric AND per-hardware facts.** Motivating exhibit
(M5.5): re-measuring the Medium floor on a different card moved the
completion floor 2.75× (0.0145 → 0.0399) while leaving survival identical
(0.0129 → 0.0130). Neither "it will be the same" nor "it will differ" is
safe to assume — measure it on the card that runs the grid.

## Artifact persistence for GPU runs (human-issued 2026-07-28)

**Every GPU run persists metrics + provenance + a checkpoint archive
(`tar.zst` + `sha256`, recorded in the phase report) off-instance before the
instance is released. Grid scripts assert it.** Rented boxes are ephemeral;
an un-archived checkpoint is a result that cannot be re-rendered, re-probed,
or audited after release. The assertion belongs in the job script (fail the
run if the archive or its hash is missing), not in a README.
