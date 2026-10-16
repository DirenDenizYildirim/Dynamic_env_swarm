# CHE — code supplement

This archive accompanies the submission. It contains the Compound Hostile
Environment (CHE), the training and evaluation code, the configurations, the
test suite, the registration documents, and the committed result artifacts
from which the paper's numbers are computed. It is anonymized for review.

## Contents

| path | what |
|---|---|
| `che/env/` | the environment, in pure JAX (hazard, smoke, structure, observation, comms, tasks, the composed step) |
| `che/train/` | IPPO training (shared-parameter actor-critic, rollouts, PBT harness) |
| `che/eval/harness.py` | checkpoint → episodes → summary JSON and per-episode NPZ |
| `che/calibration/` | the measurements behind the locked constants (percolation threshold, coupling calibrations) |
| `che/configs/` | every configuration; `theta_star_holdout.yaml` is the held-out test point |
| `che/tests/` | the CPU test suite, including the theory checks and the bitwise ablation-nesting tests |
| `che/scripts/` | GPU job scripts, the registered analysis scripts, report and figure scripts |
| `che/bench/results/` | committed result artifacts (see below) |
| `docs/locks.yaml` | machine-readable registry of every locked constant (asserted by `che/tests/test_locks.py`) |
| `docs/theory_foundations.md` | the formal specification the code and the paper's appendix refer to |
| `phase6_design_v2.md`, `phase6_framing_branches.md` | the registration documents: the experimental design and the pre-registered outcome branches |
| `*_lock.md` | records of how each locked environment constant was measured and fixed |
| `SHA256SUMS` | the sha256 of every file in this archive |

Internal milestone codes (e.g. `M5.5`, `G1.3`) appear in comments and file
names; they index the project's record and carry no meaning beyond that.
Commit hashes, host identifiers and absolute paths have been replaced by
placeholders such as `COMMIT_REDACTED_07`, `<host>` and `<abs-path>`. The
same commit always maps to the same placeholder.

## Install

Requires Python 3.12 and [uv](https://docs.astral.sh/uv/). The lock file pins
the exact versions the results were produced with (jax 0.11.0, CPU build by
default).

    uv sync --python 3.12 --group dev

For a CUDA machine add `--extra cuda`.

## Run the tests (CPU)

    uv run pytest -q che/tests

The suite runs on CPU only. It is not quick: on a 4-core machine that was
also running another CPU job, it took about 56 minutes. Budget an hour. One
test compares the science code against a fixed base revision. It is reported
as skipped, because the archive carries no version-control history. Three
parametrized tests are reported as skipped because their parameter set is
empty: no configuration has the role they check.

## Verify the archive

    sha256sum -c SHA256SUMS

## Reproduce the paper's numbers from the committed artifacts

No GPU is needed: the confirmatory analysis reads the committed evaluation
summaries. The analysis scripts refuse to run on real artifacts without an
explicit flag, and refuse a tree they cannot verify as unmodified; outside
version control pass `--allow-dirty`, which is recorded in the output.

    mkdir -p repro
    P6=che/bench/results/phase6

    # the registered confirmatory contrast and its outcome branch
    uv run python -m che.scripts.p6_unblind --artifact $P6/g1_conf_5090 \
        --floors $P6/g1_floors_5090/floors.json --card-diag $P6/g1_grid \
        --out repro/unblind --unblind --allow-dirty

    # the registered follow-up analyses (ISO-4, T = 2000, eval floor, Γ(t), High)
    uv run python -m che.scripts.p6_post_analysis --sections gamma4 t2000 \
        --out repro/post --allow-dirty
    uv run python -m che.scripts.p6_post_analysis --sections evalfloor gamma_t high \
        --out repro/post --allow-dirty

    # the registered secondary analyses (frequency sweep, plane decomposition)
    uv run python -m che.scripts.p6_secondary --out repro/secondary --allow-dirty

Compare the outputs with the committed ones in `$P6/unblind/`,
`$P6/post_unblind_analysis/` and `$P6/secondary/`. Apart from the provenance
fields (commit, dirty-file count, timestamp), they are identical.

## Verify the post hoc interaction check

The post hoc interaction check has its own analysis plan,
`che/bench/results/phase6/post_v3_interaction/PLAN.md`. Its analysis refuses to
run outside version control, so a verification mode recomputes it here:

    uv run python -m che.scripts.interaction_analysis --verify

It checks that the shipped plan's sha256 is the one the evaluation run
recorded and the report was made under. It then recomputes every number in
`interaction_report.json` from the shipped evaluation summaries, compares, and
prints what it cannot check without version history. The plan's and the
results' public timestamps are `PLAN.md.ots` and `SHA256_RESULTS.txt.ots` in
the same folder; any OpenTimestamps verifier checks them.

The result directories contain `.manifest/` entries, one per evaluated run,
which the analysis scripts require. They were reconstructed when this archive
was packaged from each directory's `SHA256_CKPT.txt` (see
`.manifest/RECONSTRUCTED.txt`).

## What is not included, and why

- **Checkpoints.** The trained policies (one archive per training seed) are
  too large for the supplementary-material limit. Their sha256 hashes are in
  each result directory's `SHA256_CKPT.txt`.
- **Most training logs and per-episode arrays.** Included are the training
  logs the registered analyses read and the per-episode evaluation arrays of
  the policies the results are about. The rest are left out for size; every
  number taken from them is in the committed evaluation summaries (`eval_*.json`)
  and reports.
- **Renders and figures** (GIF/PNG).

## Licence

MIT; see `LICENSE`.
