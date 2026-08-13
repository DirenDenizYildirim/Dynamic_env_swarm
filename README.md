# Compound Hostile Environment (CHE) — a swarm RL benchmark in pure JAX

A multi-agent reinforcement learning environment and training pipeline in
**pure JAX**, in which a swarm performs a task while surviving a
**non-adversarial, evolving hazard field** (cellular-automaton fire) that is
causally coupled to the environment in two directions, alongside an
independent communications-denial axis.

The research question is **compositional**: does training on stressors that
are *co-active* produce a policy that generalizes better to a held-out
composition than training on the same stressors *in isolation*?

> **Status: pre-registration complete, confirmatory grid not yet run.** No
> result of that comparison is reported here or anywhere in this repository.
> The analysis plan is frozen and the pipeline is blinded; see *Blinding*
> below. Everything stated as a finding below is from the calibration and
> ablation phases, not from the headline comparison.

## The setting

- **Coupling A — hazard begets hazard.** Structural collapse events seed and
  intensify the fire field, so the environment manufactures its own danger.
- **Coupling B — hazard degrades perception.** The smoke field attenuates
  agent observation via Beer–Lambert transmittance. Smoke **outlives flame**:
  it is a state component with its own emission and decay.
- **Independent axis — communications denial** at level δ, degrading the
  inter-agent link graph.
- **Training** is a PBT-style evolutionary/MARL hybrid: a population `vmap`'d
  over IPPO learners, PureJaxRL-style.

Severity is not a knob setting. The three levels are defined by **measured
dynamical phase** — sub-critical, near-critical, super-critical — calibrated
against a percolation critical point measured at 512 seeds (β̂_c = 0.500 at
L = 64, reproducing the idealized kernel's exact Kesten value to three
decimals).

The formal specification is `docs/theory_foundations.md`. It is not
decoration: several propositions are implemented as unit tests, and the
environment's step order and reward structure are theorem hypotheses.

## What makes it a benchmark rather than a demo

Four properties, each enforced by test rather than by convention:

1. **Reward independence (Def. 2).** The reward function reads task variables
   only — never hazard, smoke, or structural state, and no auxiliary cost or
   constraint channel either. Survival is learned *solely* because death
   truncates future task return. `che/tests/test_reward_independence.py`.
2. **Bitwise-exact nested ablations.** With `kappa_A=0`, `kappa_B=0` or
   `delta=0`, trajectories are **bitwise identical** to the corresponding
   nested model under the same PRNG keys — achieved by having every
   stochastic branch consume its PRNG stream unconditionally.
   `che/tests/test_nesting.py`.
3. **Theory as unit test.** The percolation sigmoid, Coupling A's linear
   scaling, and the memorization-gap value curve are asserted, not assumed.
4. **Locks enforced mechanically.** Every locked constant lives in
   `docs/locks.yaml` and `che/tests/test_locks.py` asserts that the configs
   and dataclass defaults agree with it. A constant reachable only from a
   command-line flag is a defect the suite fails on.

## Layout

```
che/env/          environment kernels — hazard, smoke, structure, observation,
                  comms, tasks, composed step
che/train/        IPPO, networks, scanned rollouts, PBT population loop
che/calibration/  the measurement code behind the locks (not training)
che/eval/         checkpoint -> policy -> episode eval -> summary
che/bench/        throughput and memory probes; per-phase results and reports
che/tests/        35 files; the theory tests are ground truth
docs/             theory_foundations.md, locks.yaml, decision_log.md
```

`CLAUDE.md` carries the working rules and the annotated tree.

## Running it

Python 3.12+ managed with [`uv`](https://docs.astral.sh/uv/). The toolchain is
pinned — jax/jaxlib **0.11.0** — and the pin is load-bearing rather than
incidental: the bitwise-nesting certification was made on it.

```sh
uv sync
uv run pytest che/tests -q          # CPU suite; see the note below
uv run ruff check che/
```

The suite runs on CPU against `che/configs/debug.yaml` (16×16 grid, 4 agents).
**Run it chunked and thread-capped** — `test_prop3`, `test_calibration` and
`test_percolation` are Monte-Carlo scale and an unbounded parallel run has
saturated a workstation. Every module also runs under `JAX_DISABLE_JIT=1`.

## Blinding

The confirmatory comparison is pre-registered and blinded, and the repository
is arranged so that the blind is a property of the tooling rather than of
anyone's restraint:

- The analysis family is frozen at two co-primaries with a Šidák correction,
  registered before any run.
- The report script **mechanically suppresses cross-arm outcome means** until
  unblinding.
- The grid runner computes no cross-arm quantity at all, and a test asserts
  the absence of any analysis call in it.
- The outcome-conditional framing — what the paper claims under each possible
  result — is registered in advance in `phase6_framing_branches.md`, so the
  narrative cannot be selected after seeing the outcome.

`docs/decision_log.md` records every ruling in the order it was issued,
including the ones that went against the author.

## Reproducibility notes worth borrowing

Two measurement rules emerged here and are enforced throughout, because both
were learned by getting them wrong first:

- **Bars come with floors, per-metric, per-hardware *and* per-artifact.** A
  threshold set below its instrument's measured noise cannot fail under the
  null, so it is not a test — and a floor measured on the *reference* artifact
  describes that artifact's stability, not the candidate's.
- **Design-stage power statements are 80 %-power MDEs at the family-corrected
  α**, and a contrast is graded on the *contrast's* standard error, never on
  either arm's.

## License and status

Research code accompanying a paper in preparation. Interfaces are not stable.
