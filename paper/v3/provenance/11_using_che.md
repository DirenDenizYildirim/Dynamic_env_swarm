# Provenance: sections/11_using_che.md

Writer: W5 (Paper v3, step 4.1, 2026-10-14). Checked with
`paper/v3/src/provenance_check.py --strict`. `log` = `docs/decision_log.md`.
v2 material: `paper/v2/sections/11_reproducibility.md` (main draft, :22-28) and
its alternate `paper/v2/sections/alt/11_reproducibility.supplement.md` (:13),
which described a supplement; v3 settles v2 Q4e for the supplement option
(V3-V3). Step 2's supplement files (`paper/v3/supplement/README.md`,
`SHIPPED_README.md`, `paper/v3/out/*`) are **uncommitted** while the owner's
commit ban holds (V3Q25); no number in this section comes from them.

| # | sentence (verbatim) | support | change from v2, and why |
|---|---|---|---|
| 1 | 8 Using CHE and reproducing the paper | framing | edited (v2 "11 Reproducibility"; heading as the stub fixes it) |
| 2 | CHE is a functional JAX environment: reset(key, cfg) returns observations and state, and step(key, state, actions, cfg) also returns the team reward, a done flag and an info dictionary. | che/env/env.py:200; che/env/env.py:283-290 | edited; fix round RM-1 (shortened; "under jit and vmap" cut) |
| 3 | YAML configurations set θ, the fixed sub-parameters and any training mixture, and a test checks them against a registry of the fixed constants (Appendix B). | che/env/config.py:21, :76-131; che/tests/test_locks.py:1-9 | edited; fix round RC2-19 ("its registry" → "a registry of the fixed constants (Appendix B)"). RC2-19's proposed "configurations and code defaults" was not used: RC1-1 found that test_locks checks code defaults for four constants only |
| 4 | In the anonymized code supplement, uv run pytest -q che/tests runs the CPU tests, and uv run python -m che.train.ippo and uv run python -m che.eval.harness train and evaluate. | paper/v3/supplement/SHIPPED_README.md:44, :65; che/train/ippo.py:668-674; che/eval/harness.py:240-244 | edited; fix round RM-6 (`uv run python -m …`, as the shipped README writes it) and RM-1 ("submitted with this paper", "a policy", "under any configuration" cut) |
| 5 | On one RTX 5090, a 1000-update run took 518–521 s and a 512-episode evaluation 9–10 s. | DX-5; DX-4 | edited; fix round RM-1: the step count (DX-3) and the toolchain (DX-407) cut; the "one 64 × 64 map with 12 agents" sentence cut (§1 and §3.5 state the instance) |
| 6 | The supplement holds the package, configurations, tests, registration documents, analysis scripts with the committed outputs they read, and a sha256 manifest; its README recomputes the registered analyses on a CPU. | paper/v3/supplement/README.md:49-60; paper/v3/supplement/SHIPPED_README.md:1-24, :54-81 | edited; fix round RM-1 (shortened). TF and lock records still not listed: RM-OWNER-1, OWNER-PENDING V3Q16 |
| 7 | For the post hoc interaction check, whose analysis needs version history, a verification mode checks the plan's hash against the run's record and recomputes the report there. | che/scripts/interaction_analysis.py:132-153 (needs git), :826-900 (verify); che/bench/results/phase6/post_v3_interaction/PLAN.md:267-289; paper/v3/supplement/SHIPPED_README.md:85-98; decision log, PLAN AMENDMENT (docs/decision_log.md:6436), item 5 | new; fix round RM-7. Amended 2026-10-17 (PLAN AMENDMENT item 5): '… needs version history, so it does not run there' → the verification mode (supplement README finding F2, addressed) |
| 8 | Checkpoints ship only as hashes. | paper/v3/supplement/SHIPPED_README.md:87-91 | edited; fix round RM-1 ("so retraining needs a GPU" cut) |
| 9 | Our registration record is internal and version-controlled, so its dates are self-reported; the hash manifest shows only that the archive arrived unaltered (Appendix D). | paper_v3_prompt.md:283-285; paper/v3/supplement/README.md:175-178 | edited; fix round RC2-4 (MUST): the manifest "shows only that the archive arrived unaltered", no longer that the documents are the files described; "our own report" → "self-reported" (V3-V2's word). RC2-4's "not when the documents were written" is implied by "only" and was cut for RM-1 |
| 10 | A public registry such as OSF would remove this limit; we intend to use one next time. | paper_v3_prompt.md:285; decision log, PAPER V3 (docs/decision_log.md:6144-6146, item 1(5), as relayed) | edited; fix round RM-1. The commitment is OWNER-PENDING (V3_V2 marker) |
| 11 | Evaluation reproduces closely: repeated evaluations of two checkpoints on one GPU were bit-identical and matched the main runs' own, and across GPUs 280 of 288 paired checkpoint and metric values agreed exactly, differing by at most 2.44 × 10⁻⁴. | HW-2; HW-3 | edited; fix round RM-1: v2-derived HW-2 and HW-3 sentences merged (HOME of C37). "reproduces closely" because 8 of 288 cross-GPU pairs differ |
| 12 | GPU training is not, which is why reproducibility floors are measured (§5). | che/bench/results/phase4/phase4_report.md:637-639 | edited; fix round RM-1 (shortened) |

## Markers left

- `<!-- OWNER-PENDING:V3Q16 -->` with a comment: what else ships
  (`docs/theory_foundations.md` and the four lock records ship by default in
  step 2's build, rules D3 and D4, while DISPOSITIONS V3Q16's default is "the
  hash manifest only"; decision-log excerpts are off by default, a V3-V1 owner
  decision). The section's list names only what ships under both readings.
- The supplement's size and TMLR's limit are **not stated**: rows X5-1 and
  X5-2 are PENDING (`ledger_proposals/W5.md`).

## Findings

- **Word budget (fix round, RM-1).** 239 prose words against 240. Cut: the
  step count (DX-3), the toolchain (DX-407), the map-size sentence, "under
  jit and vmap", "so retraining needs a GPU". Added: RM-7's sentence.
- **RM-OWNER-1 / V3Q16** (OWNER): whether the theory document and lock
  records ship decides whether the contents sentence lists them; the marker
  comment holds the wording to add.
- **Commands** now read `uv run python -m …` (RM-6), as the shipped README.
- **`SHIPPED_README.md:12`** describes a "PBT harness" (it exists, unused by
  any reported run; ENV-11); §8 does not mention it.
