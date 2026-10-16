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
| 2 | CHE is a functional JAX environment: reset(key, cfg) returns the observations and the state, step(key, state, actions, cfg) returns the observations, the next state, the team reward, a done flag and an info dictionary, and both work under jit and vmap. | che/env/env.py:200 (reset signature and return type); che/env/env.py:283-290 (step signature; "Returns (obs, state', team_reward, done, info)"); CLAUDE.md:226-233 (functional purity; per-agent vmap, time lax.scan, population outermost vmap) | new (P3 §1.2: the API in two lines). No JaxMARL compatibility is claimed (BRIEF §8.1; DISPOSITIONS R-9) |
| 3 | YAML configurations set θ, the sub-parameters fixed before the main experiment and any training mixture, and a test checks every fixed value against its registry. | che/env/config.py:21 (ThetaConfig), :76-131 (MixtureComponent, MixtureConfig); che/tests/test_locks.py:1-9 (configs and dataclass defaults asserted against docs/locks.yaml; locked values written explicitly in the configs) | edited from v2 11:22 ("A test asserts that the configurations and code defaults agree with the registry ..."); shortened |
| 4 | In the anonymized code supplement submitted with this paper, uv run pytest -q che/tests runs the CPU tests, python -m che.train.ippo trains a policy, and python -m che.eval.harness evaluates a checkpoint under any configuration. | paper/v3/supplement/SHIPPED_README.md:44 (`uv run pytest -q che/tests`); che/train/ippo.py:668-674 (`--config`, `--updates`, `--seed`, `--ckpt-dir`); che/eval/harness.py:240-244 (`--config`, `--ckpt-dir`, `--step`, `--n-episodes` 512, `--seed` 0); che/scripts/run_p6_grid.sh:299 (`che.train.ippo`) | new; defines "code supplement" at first use (BRIEF §5.2). Replaces v2 11:22's "The code behind this paper is one repository" (v2 Q4e settled, V3-V3) |
| 5 | On one RTX 5090, a 1000-update run of 32,768,000 environment steps took 518–521 s and a 512-episode evaluation 9–10 s, with Python 3.12.3 and jax 0.11.0. | DX-5; DX-3; DX-4; DX-407 | edited from v2 11:26 ("On GPU 1, an RTX 5090 ..."): "GPU 1" is banned in the main text; the "each advancing all 12 agents" clause cut; DX-4's scope (the 76 runs timed in the confirmatory directory) is not narrowed further in the sentence |
| 6 | Every reported result uses one 64 × 64 map with 12 agents, although the trainer accepts others. | ENV-6; che/train/ippo.py:676-677 (`--grid-size`, `--n-envs`) | new (stub: what can be varied, and that every reported result uses one instance) |
| 7 | Once unpacked, the supplement holds the package, the configurations, the tests, the analysis scripts with the committed evaluation outputs they read, the registration documents and a sha256 manifest of every file; its README gives the commands that recompute the registered analyses on a CPU. | paper/v3/supplement/README.md:49-60 (selection rules C1, D1, D2, R1–R5); paper/v3/supplement/SHIPPED_README.md:1-24 (contents; `SHA256SUMS`), :54-81 ("No GPU is needed"; the p6_unblind, p6_post_analysis and p6_secondary commands) | edited from v2 alt 11:13 (the supplement framing): contents per step 2. The interaction check's own analysis cannot run inside the supplement as built (supplement README finding F2: it needs git), so the sentence names only the registered analyses |
| 8 | Trained checkpoints are not included, only their hashes, so retraining needs a GPU. | paper/v3/supplement/SHIPPED_README.md:87-91 (checkpoints not included; their sha256 in each `SHA256_CKPT.txt`); DX-4 (training measured on a GPU) | edited from v2 alt 11:13 ("The trained checkpoints are not in the supplement"); "retraining needs a GPU" from the stub |
| 9 | The registration record is internal and version-controlled, so its dates are our own report; the supplement's hash manifest shows that the registration documents are the files this paper describes, not when they were written (Appendix D). | paper_v3_prompt.md:283-285 (V3-V2: "The record is internal and version-controlled, its dates are self-reported, and the supplement carries the documents"); paper/v3/supplement/README.md:175-178 (commit hashes are replaced by placeholders, so the supplement does not let reviewers verify dates by commit) | new (V3-V2, two sentences; full account App. D, W4). "not when they were written" follows step 2's warning that the registration statement must not imply commit-level date checks |
| 10 | A public registry such as OSF would remove this limit, and we intend to use one in future studies. | paper_v3_prompt.md:285 (V3-V2: "Next time, a public registry (OSF)"); decision log, PAPER V3 (docs/decision_log.md:6144-6146, item 1(5), as relayed) | new. The intention is the owner's to confirm (OWNER-PENDING wording) |
| 11 | Evaluation reproduced exactly on one GPU: four repeated evaluations of each of two checkpoints were bit-identical, and identical to the main runs' own evaluations. | HW-2 | edited from v2 11:24 ("... identical to the grid's own evaluations"): "the grid" → "the main runs" (BRIEF §5.2) |
| 12 | Across GPUs, 280 of 288 paired checkpoint and metric values agreed exactly, differing by at most 2.44 × 10⁻⁴. | HW-3 | edited from v2 11:24 (HOME of C37); "the largest absolute difference is" → "differing by at most" (no pipe, M1) |
| 13 | GPU training is not bitwise reproducible from run to run, which is why reproducibility floors are measured (§5). | che/bench/results/phase4/phase4_report.md:637-639 ("GPU training is not run-to-run reproducible (XLA autotunes kernels by timing; some reductions use atomics)") | kept in substance from v2 11:24 ("GPU training is not run-to-run reproducible (§8), which is why floors are measured (Appendix C)"); pointer now §5 |

## Markers left

- `<!-- OWNER-PENDING:V3Q16 -->` with a comment: what else ships
  (`docs/theory_foundations.md` and the four lock records ship by default in
  step 2's build, rules D3 and D4, while DISPOSITIONS V3Q16's default is "the
  hash manifest only"; decision-log excerpts are off by default, a V3-V1 owner
  decision). The section's list names only what ships under both readings.
- The supplement's size and TMLR's limit are **not stated**: rows X5-1 and
  X5-2 are PENDING (`ledger_proposals/W5.md`).

## Findings

- **Conflict between step 2 and DISPOSITIONS V3Q16.** Step 2 ships the theory
  document by default and recommends it ("App. A calls it 'the formal
  specification'", `supplement/README.md:143-150`), while V3Q16's default is
  "'formal specification' references removed; ... ship TF in the supplement"
  as the alternative. The owner needs to pick one; §8's wording does not
  depend on it.
- **The interaction check cannot be re-analysed inside the supplement**
  (`supplement/README.md` finding F2: `interaction_analysis.py` needs the
  plan tracked in git). If the owner wants §8 to say the supplement
  reproduces the post hoc check too, the orchestrator's git-free mode is
  needed first.
- **Commands.** The training and evaluation commands are written
  `python -m …` (run inside the synced environment); the supplement's README
  writes `uv run python -m …`. Harmless, but the mechanics reviewer may want
  them identical.
- **`SHIPPED_README.md:12`** describes `che/train/` as including a "PBT
  harness". It exists (`che/train/pbt.py`), but no reported run used it
  (ENV-11, O-1); §8 does not mention it.
- **Word budget.** 307 prose words against 240 (+28 %); inline code spans
  count as words. The owner may cut the compute sentence's toolchain clause
  and the "although the trainer accepts others" clause (about 15 words).
