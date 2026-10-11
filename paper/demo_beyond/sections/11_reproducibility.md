<!-- BUILDER-WRITTEN DEMONSTRATION (DEMONSTRATION DRAFT ruling, 2026-10-11); not the owner's text -->

## 11 Reproducibility

**What the anonymized code supplement contains.** The environment (`che/env/`), training (`che/train/`), evaluation (`che/eval/`) and calibration (`che/calibration/`) code; every configuration (`che/configs/`), including the generated Phase-6 protocol configurations and θ\*; the analysis instruments that produced every Phase-6 number (`che/scripts/p6_unblind.py`, `che/scripts/p6_post_analysis.py`, `che/scripts/p6_secondary.py`); the registry of locked constants (`docs/locks.yaml`) with the test that asserts the configurations and code defaults agree with it (`che/tests/test_locks.py`); and the CPU test suite (`che/tests/`), which runs the theory checks as unit tests. Every locked environment constant is reachable from a configuration and checked by that test, and every locked analysis constant is checked against the literal in the instrument that uses it, so a lock cannot live only in prose or on a command line.

**What is exact, and what is not.** Ablations are exact by construction: every stochastic branch consumes its random numbers whether or not its stressor is on, so switching a stressor off reproduces the nested model's trajectories bit for bit under the same keys (Listing 3, §3). Evaluation is reproducible: four repeated evaluations of each of two checkpoints are bit-identical on one card and identical to the grid's own evaluations<!-- N:HW-2 -->, and across cards 280 of 288 paired evaluations are identical, max |Δ| = 2.44 × 10⁻⁴<!-- N:HW-3 -->. GPU training is not run-to-run reproducible, because the compiler autotunes kernels by timing and some reductions use atomics. That is why reproducibility floors are measured, as identical reruns on the card that ran each study (Appendix C); the tests of §9 use each arm's own seed dispersion instead, because a mean over k seeds varies by seed as well as by nondeterminism (§8).

**Cost of a re-run.** A 1000-update training run took 518–521 s and a 512-episode evaluation 9–10 s on one RTX 5090<!-- N:DX-4 --> (Python 3.12.3, jax 0.11.0<!-- N:DX-407 -->), for 32,768,000 environment steps per run<!-- N:DX-3 -->. The IPPO hyperparameters are in Appendix B<!-- N:DX-2 -->, the seed layout and card blocks in Appendix F.

**Checkpoints.** The trained checkpoints are not in the supplement. Each archive has a recorded sha256, and a re-verification matched every recorded hash<!-- N:DX-408 -->; Appendix F states the one floor set whose archives were mostly never hashed, which grades nothing.

**One look per stage.** The analysis instruments refuse to run out of order, and each stage's log records a single run (§9.1, blinding).

**Appendices.**

- A. Proofs: Propositions 1–4, Theorem 1 and Remark 2′.
- B. Every locked constant with its ruling date; the IPPO hyperparameters and the budget.
- C. Every measured floor, with card, run length, artifact and sample size.
- D. The frozen analysis plan: registered constants and reading rules, verbatim, with dates.
- E. The registered outcome branches and the falsifier.
- F. Grid provenance: runs, seed layout, card blocks, archives.
- G. Throughput: what the paper does and does not state.
- H. Γ(t): both full tables and the sign reading.
- I. The secondary design: every arm and interval.
- J. Trained-policy episodes: one illustrative episode per arm, shown separately.
