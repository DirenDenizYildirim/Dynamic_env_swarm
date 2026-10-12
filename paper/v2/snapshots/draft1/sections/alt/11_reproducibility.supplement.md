<!-- PAPER V2 DRAFT (PAPER V2 ruling, 2026-10-11): builder-drafted, not owner-approved -->

## 11 Reproducibility

<!-- STUB-SPEC
ALTERNATE FOR OWNER CHOICE Q4e (N14): section 11 describing an anonymized code supplement, as the demo's did (sections/11_reproducibility.md:5): the environment, training, evaluation and calibration code; every configuration including θ* and the generated protocol configurations; the analysis scripts that produced every Phase-6 number; the registry of locked constants with the test that asserts it; the CPU test suite. No size and no venue limit (O-3, O-4 OPEN); no URL; no promise about after review unless the owner rules one. Everything else as sections/11_reproducibility.md.
WRITER: W5. BUDGET: section 11's budget plus at most 80 words.
KEEP IN STEP: every change to sections/11_reproducibility.md is mirrored here, so the two differ only in the supplement paragraph.
-->

The anonymized code supplement contains the environment (`che/env/`), training (`che/train/`), evaluation (`che/eval/`) and calibration (`che/calibration/`) code, and every configuration (`che/configs/`), θ\* and the generated protocol configurations included. It also contains the analysis scripts that produced the results of §9 (`che/scripts/p6_unblind.py`, `che/scripts/p6_post_analysis.py`, `che/scripts/p6_secondary.py`), the registry of locked constants (`docs/locks.yaml`), and the CPU test suite (`che/tests/`), which runs the theory checks as unit tests. A test in it (`che/tests/test_locks.py`) asserts that the configurations and code defaults agree with the registry and that each registered analysis constant equals the literal in the script that uses it. Each listing in this paper is a verbatim excerpt of the supplement, labelled with its file and lines. The trained checkpoints are not in the supplement.

Ablations are exact by construction: every stochastic branch consumes its random numbers whether or not its stressor is on, so switching a stressor off reproduces the nested model's trajectories bit for bit under the same keys (§3.4, Listing 3). Four repeated evaluations of each of two checkpoints are bit-identical on one GPU and identical to the grid's own evaluations<!-- N:HW-2 -->. Across GPUs, 280 of 288<!-- N:HW-3 --> paired evaluations are identical, and the largest absolute difference is 2.44 × 10⁻⁴<!-- N:HW-3 -->. GPU training is not run-to-run reproducible (§8), which is why floors are measured (Appendix C).

On GPU 1, an RTX 5090<!-- N:DX-5 -->, a 1000-update training run took 518–521 s and a 512-episode evaluation 9–10 s<!-- N:DX-4 --> (Python 3.12.3, jax 0.11.0<!-- N:DX-407 -->). A run is 32,768,000<!-- N:DX-3 --> environment steps, each advancing all 12<!-- N:ENV-6 --> agents; Appendix B gives the hyperparameters. These are training measurements. The paper states no environment-only throughput figure, because under the compiler's dead-code elimination such a figure depends on which outputs its consumer reads.

The checkpoints of the experiment in §9 were archived off the rented machines with recorded sha256 hashes, except a partial floor set that grades nothing, in which one of 12<!-- N:DX-408 --> archives has a hash (Appendix F). A re-verification matched every recorded hash<!-- N:DX-408 -->. The analysis scripts refuse to run out of order, and each stage's log records a single run (§9.1).
