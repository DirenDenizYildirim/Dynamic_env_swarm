<!-- PAPER V3 DRAFT (PAPER V3 ruling, 2026-10-12): builder-drafted, not owner-approved -->

## 8 Using CHE and reproducing the paper

<!-- STUB-SPEC
JOB: What a user needs (P3 §1.2) and what the code supplement holds and reproduces (V3-V1, V3-V3), the registration statement (V3-V2), and what is exact (evaluation) and what is not (GPU training).
WRITER: W5.
BUDGET: 240 prose words; one short code block at most (the API, not a LISTING unless copied from a committed file with a LISTING line).
FROM: P3 §1.2 and §1.3; P1 §4.2 §8; V3-V1, V3-V2, V3-V3.
ORDER:
  - the API in two lines: reset(key, cfg) returns (obs, state); step(key, state, actions, cfg) returns (obs, state, team reward, done, info) (che/env/env.py:200, :283-290); functional, jit- and vmap-ready
  - configuration: YAML configs carry θ and the locked sub-parameters and per-episode training mixtures (che/env/config.py); every locked constant is asserted by a test (che/tests/test_locks.py)
  - how to run, as the commands run inside the unpacked supplement: the CPU test suite; training (python -m che.train.ippo with config, updates and seed); evaluation (python -m che.eval.harness with config and checkpoint directory) (ippo.py:668-674; harness.py:240-244; paper/v3/supplement/SHIPPED_README.md)
  - compute: one 1000-update run and one evaluation on one RTX 5090 (DX-4), environment steps per run (DX-3), toolchain (DX-407)
  - what can be varied (the trainer accepts grid-size and n-envs flags, ippo.py:676-677) and that every reported result uses one instance (ENV-6); exact nesting gives common-random-number contrasts (the interaction check uses this)
  - the supplement: what it holds (package, configs, tests, analysis scripts, registration documents, hash manifest) and that it reproduces every analysis from committed evaluation outputs; retraining needs a GPU; checkpoints are not shipped; its size only with a row (PENDING)
  - the registration statement, two sentences: the registration record is internal and version-controlled, its dates are self-reported, the supplement carries the registration documents with a hash manifest; a public registry next time (full account Appendix D)
  - evaluation is bit-identical on one GPU; 280 of 288 paired evaluations agree across GPUs, largest difference stated (HW-2, HW-3; HOME); GPU training is not bitwise reproducible across GPUs
ROWS: DX-3, DX-4, DX-407, ENV-6, HW-2, HW-3; supplement rows X5-1 (size) and X5-2 (TMLR limit) only once VERIFIED (V3Q24, V3Q25).
REGISTERED STRINGS: none.
CAVEATS HOMED HERE (state each in full, once; the detection pattern, from checks/caveats.yaml, must match your home sentence):
  C37 evaluation_reproducibility: Evaluation is bit-identical on one GPU; 280 of 288 paired evaluations agree across GPUs. Pattern: \b280 of 288\b
EVERY OTHER CAVEAT in checks/caveats.yaml: pointer only ("§6.3", "Appendix D"), never restated. C26: any sentence about the interaction check carries "post hoc".
NEW ROWS OWED:
  - X5-1 (W5): the supplement zip's size, from step 2's committed output (paper/v3/out/build_summary.json once committed); PENDING-COMMIT until then.
  - X5-2 (W5): TMLR's supplementary-material limit, only after the page is re-read directly and the reading transcribed (V3Q24); else cut.
  - optional, V3Q18: training throughput DERIVED from DX-3 and DX-4; CPU-suite time from a committed supplement check.
OWNER-PENDING:
  - decision-log excerpts in the supplement (V3-V1 owner decision); content hashes of the registration files in the text (V3Q16).
NOT HERE: JaxMARL compatibility; a repository URL, account, commit hash or absolute path; "the formal specification" (TF does not ship by default, V3Q16); any supplement size or venue limit without a row; total GPU-hours; PBT; dates.
V2 MATERIAL: paper/v2/sections/11_reproducibility.md; paper/v2/sections/alt/ (the supplement alternate, if present); step 2's paper/v3/supplement/SHIPPED_README.md and its report.
DEPENDENCIES: step 2 (supplement contents and commands); Appendix D (W4) carries the full registration account.
-->

CHE is a functional JAX environment: `reset(key, cfg)` returns the observations and the state, `step(key, state, actions, cfg)` returns the observations, the next state, the team reward, a done flag and an info dictionary, and both work under `jit` and `vmap`. YAML configurations set θ, the sub-parameters fixed before the main experiment and any training mixture, and a test checks every fixed value against its registry.

In the anonymized code supplement submitted with this paper, `uv run pytest -q che/tests` runs the CPU tests, `python -m che.train.ippo` trains a policy, and `python -m che.eval.harness` evaluates a checkpoint under any configuration. On one RTX 5090<!-- N:DX-5 -->, a 1000-update run of 32,768,000<!-- N:DX-3 --> environment steps took 518–521 s and a 512-episode evaluation 9–10 s<!-- N:DX-4 -->, with Python 3.12.3 and jax 0.11.0<!-- N:DX-407 -->. Every reported result uses one 64 × 64 map with 12 agents<!-- N:ENV-6 -->, although the trainer accepts others.

Once unpacked, the supplement holds the package, the configurations, the tests, the analysis scripts with the committed evaluation outputs they read, the registration documents and a sha256 manifest of every file; its README gives the commands that recompute the registered analyses on a CPU. Trained checkpoints are not included, only their hashes, so retraining needs a GPU.

<!-- OWNER-PENDING:V3Q16 -->
<!-- what else ships is the owner's call: the supplement builder ships docs/theory_foundations.md and the four lock records by default (paper/v3/supplement/README.md, rules D3, D4), while DISPOSITIONS V3Q16's default ships the hash manifest only; decision-log excerpts are off by default (V3-V1 owner decision). The supplement's size and TMLR's limit wait for rows X5-1 and X5-2 (PENDING; V3Q24, V3Q25) and are not stated. -->

<!-- OWNER-PENDING:V3_V2 the registration statement's wording, in particular the commitment "we intend to use one in future studies", is the owner's to confirm -->

The registration record is internal and version-controlled, so its dates are our own report; the supplement's hash manifest shows that the registration documents are the files this paper describes, not when they were written (Appendix D). A public registry such as OSF would remove this limit, and we intend to use one in future studies.

Evaluation reproduced exactly on one GPU: four repeated evaluations of each of two checkpoints were bit-identical, and identical to the main runs' own evaluations<!-- N:HW-2 -->. Across GPUs, 280 of 288<!-- N:HW-3 --> paired checkpoint and metric values agreed exactly, differing by at most 2.44 × 10⁻⁴<!-- N:HW-3 -->. GPU training is not bitwise reproducible from run to run, which is why reproducibility floors are measured (§5).
