# Interaction check: the owner's runbook (eval-only, θ\* only)

For the owner, who rents the GPU and runs the job (or hands the box to a
session; decision log: *BOX HANDOVER*). The plan is `PLAN.md` in this folder,
as amended on 2026-10-17 (*PLAN AMENDMENT*). It must be **committed, OK'd by
you, and publicly timestamped (step 0.7) before step 1**. Nothing here trains.
Expected spend is about 2.3–3.6 GPU-hours plus setup, which is an estimate and
not a trigger (PLAN §3).

Commands run from the repository root unless a step says otherwise. Write
down the values marked ✎ as you go; the last step needs them.

## 0. Before you rent (on your laptop)

1. The branch with this session's work is checked out and clean:
   `git status` shows nothing to commit.
2. Note the commit: `git rev-parse HEAD` ✎ `C`.
3. Note the plan's hash at that commit:
   `sha256sum che/bench/results/phase6/post_v3_interaction/PLAN.md` ✎ `P`.
4. The tests for this job pass locally:
   `uv run pytest -q che/tests/test_interaction_check.py`.
5. Find the 164 archives you need. Each is about 45 MB, so about 7.4 GB in
   all. (That size is from `g1_floors_card2/README.md:26`; the real files may
   differ a little.)
   - `che/bench/results/phase6/g1_conf_5090/ckpt_iso_s{1..72}.tar.zst`
   - `che/bench/results/phase6/g1_conf_5090/ckpt_joint_s{1..72}.tar.zst`
   - `che/bench/results/phase6/g1_iso4_5090/ckpt_iso4_s{1..20}.tar.zst`

   They are on your laptop, and in the 2026-09-27 backup
   (`che_results_2026-09-27.tar`, sha256 in that backup's `SHA256SUMS.txt`;
   HANDOFF.md, "Backup"). If you restore from the backup, check the backup
   tar against `SHA256SUMS.txt` first (`sha256sum -c SHA256SUMS.txt`).
   Then list one path to see its prefix before extracting, for example
   `tar -tf che_results_2026-09-27.tar | grep -m3 'g1_conf_5090/ckpt_'`.
6. Verify the archives on the laptop, against the committed hash files. This
   checks every one of the 164 and evaluates nothing:

   ```
   VERIFY_ONLY=1 bash che/scripts/run_interaction_evals.sh
   ```

   It must print `ARCHIVES: verified=164 bad_or_missing=0`. The check is by
   basename, because the confirmatory hash file still carries `g1_grid/`
   paths for seeds 13–46 (`phase6_report.md` §3). **If any archive fails,
   stop.** Do not substitute another file. Tell the next session which one
   failed.
7. The plan's public timestamp is confirmed (PLAN §10). `PLAN.md.ots` sits
   beside `PLAN.md`, committed. In this folder, `ots upgrade PLAN.md.ots`
   must report the proof complete, and `ots info PLAN.md.ots` must show a
   Bitcoin block attestation. If the proof is still pending, wait: it usually
   completes within a few hours of the stamp. Do not rent before it does.

## 1. Rent the card

- An **RTX 5090**, the class the grid and every Phase-6 eval ran on
  (`phase6_report.md` §3; `by_card/README.md`). Floors are per-hardware
  facts (CLAUDE.md), and the cross-card check in PLAN §6 compares against
  5090 evals.
- CUDA 12 drivers, Ubuntu, at least **20 GB free disk** (7.4 GB of archives,
  one extracted checkpoint at a time, the venv, and the results).
- `tar` and `zstd` installed (`apt-get install -y zstd` if `zstd` is missing).

## 2. Put the tree and the archives on the box

1. Ship the tree at commit `C`, without `.git`:
   `git archive --format=tar.gz -o che_tree.tgz C` on the laptop. Note
   `sha256sum che_tree.tgz` ✎, copy the file to the box, and check the same
   hash there. Then `mkdir Dynamic_env_swarm && tar -xzf che_tree.tgz -C Dynamic_env_swarm`.
   (Cloning the private repository with a token also works. Then check
   `git rev-parse HEAD` = `C`.)
2. Copy the 164 archives into the same paths under the box's tree
   (`che/bench/results/phase6/g1_conf_5090/` and `.../g1_iso4_5090/`).
   The committed `SHA256_CKPT.txt` files are already there from the tree.
3. On the box, from the repo root:

   ```
   VERIFY_ONLY=1 bash che/scripts/run_interaction_evals.sh
   ```

   Again it must print `verified=164 bad_or_missing=0`. If not, stop.

## 3. Set up the environment

```
command -v uv || { curl -LsSf https://astral.sh/uv/install.sh | sh; export PATH="$HOME/.local/bin:$PATH"; }
uv sync --extra cuda
uv run python -c "import jax; print(jax.__version__, jax.devices())"
```

The last line must show `0.11.0` and a CUDA device. A CPU device means the
CUDA install failed: stop and fix it, because a CPU run would take days.
Do not run `che/scripts/vast_setup.sh`; it also runs the throughput gate,
which this job does not need.

## 4. Dry run ($0)

```
DRY_RUN=1 bash che/scripts/run_interaction_evals.sh | head -3
```

It must print `interaction evals planned: 865  (blocks: main floor)`.

## 5. Run

Inside `tmux` (or `screen`), so a dropped SSH session does not kill the job:

```
GIT_COMMIT=C PLAN_SHA256=P bash che/scripts/run_interaction_evals.sh 2>&1 | tee interaction_console.log
```

Replace `C` and `P` with the values you noted. `PLAN_SHA256` makes the
script refuse to start if the plan on the box differs from the one you
committed.

- Progress prints every 50 evals.
- **If it stops** (interruption, a failed eval), run the same command again.
  Finished evals are skipped, and only the missing ones run.
- It ends with `ARCHIVE OK: …/v3_interaction_results.tar.zst  sha256 …` ✎.
  Any `FATAL` line means it is not done.

## 6. Copy the results off the box, then release it

1. Copy these three files to your laptop:
   - `che/bench/results/phase6/post_v3_interaction/v3_interaction_results.tar.zst`
   - `che/bench/results/phase6/post_v3_interaction/SHA256_RESULTS.txt`
   - `interaction_console.log`
2. On the laptop, in the folder you copied them to:
   `sha256sum -c SHA256_RESULTS.txt` must say `OK`.
3. **Only then release the box** (CLAUDE.md, artifact persistence).
4. Timestamp the results' hash (PLAN §10): `ots stamp SHA256_RESULTS.txt`,
   then commit `SHA256_RESULTS.txt.ots` beside it with the results. Run
   `ots upgrade SHA256_RESULTS.txt.ots` again a few hours later, and commit
   the completed proof.

## 7. Back in a session

Give the next session the three files and the ✎ values. That session:

1. verifies `SHA256_RESULTS.txt` again;
2. extracts the archive into `che/bench/results/phase6/post_v3_interaction/`
   (`evals/`, `floor/`, `timings.txt`, `provenance.txt`, `.plan_at_run.md`)
   and checks that `.plan_at_run.md` is byte-identical to the committed
   `PLAN.md`;
3. commits the results;
4. runs the analysis once, on the clean tree:
   `uv run python -m che.scripts.interaction_analysis`. It refuses if the
   plan is not committed or was changed, if the run did not record the
   committed plan's hash, or if any eval is missing. Every run of it is
   logged in `ANALYSIS_LOG.txt`;
5. commits the report, and adds VERIFIED ledger rows for any number the
   paper uses (paper_v3_prompt.md, step 0.5).

## Do not

- edit `PLAN.md`, the configs or the scripts on the box;
- change `N_EVAL`, `EVAL_SEED`, `T_STAR`, `K_CONF`, `K_ISO4` or the floor
  settings;
- run the analysis on the box, or look at the numbers to decide anything
  about the run;
- run Low or High: they are not authorized (*PAPER V3 PHASE 1 START*
  item 2).
