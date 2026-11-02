<!-- PAPER V3 DRAFT (PAPER V3 ruling, 2026-10-12): builder-drafted, not owner-approved -->

## 8 Using CHE and reproducing the paper

CHE is a functional JAX environment: `reset(key, cfg)` returns observations and state, and `step(key, state, actions, cfg)` also returns the team reward, a done flag and an info dictionary. YAML configurations set θ, the fixed sub-parameters and any training mixture, and a test checks them against a registry of the fixed constants (Appendix B).

In the anonymized code supplement, `uv run pytest -q che/tests` runs the CPU tests, and `uv run python -m che.train.ippo` and `uv run python -m che.eval.harness` train and evaluate. On one RTX 5090<!-- N:DX-5 -->, a 1000-update run took 518–521 s and a 512-episode evaluation 9–10 s<!-- N:DX-4 -->.

The supplement holds the package, configurations, tests, registration documents, the theory document and the records of how each fixed constant was measured, analysis scripts with the committed outputs they read, and a sha256 manifest; its README recomputes the registered analyses on a CPU. Checkpoints ship only as hashes.

<!-- V3Q16 settled 2026-10-19 (log: OWNER QUESTIONS SETTLED, item 2, Q1): the theory document and the lock records ship, and the list above names them. The note below is kept as the record. -->
<!-- what else ships was the owner's call (RM-OWNER-1): the supplement builder ships docs/theory_foundations.md and the four lock records by default (paper/v3/supplement/README.md, rules D3, D4), while DISPOSITIONS V3Q16's default ships the hash manifest only; if they ship, add "the theory document and the records of how each fixed constant was measured" to the list above. Decision-log excerpts are off by default (V3-V1 owner decision). The supplement's size and TMLR's limit wait for rows X5-1 and X5-2 (PENDING; V3Q24, V3Q25) and are not stated. -->

<!-- SETTLED:V3_V2 (2026-10-19, log OWNER QUESTIONS SETTLED: the default stands) the registration statement's wording, in particular the commitment to a public registry next time, is the owner's to confirm -->

Our registration record is internal and version-controlled, so its dates are self-reported; the hash manifest shows only that the archive arrived unaltered (Appendix D). A public registry such as OSF would remove this limit; we intend to use one next time.

Evaluation reproduces closely: repeated evaluations of two checkpoints on one GPU were bit-identical and matched the main runs' own<!-- N:HW-2 -->, and across GPUs 280 of 288<!-- N:HW-3 --> paired checkpoint and metric values agreed exactly, differing by at most 2.44 × 10⁻⁴<!-- N:HW-3 -->. GPU training is not, which is why reproducibility floors are measured (§5).
