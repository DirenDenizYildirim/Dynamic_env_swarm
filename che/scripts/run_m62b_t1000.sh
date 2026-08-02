#!/usr/bin/env bash
# M6.2b — the floor milestone RE-RUN at T = 1000. Sequence step (b) of the
# PHASE-6 FRAMING + ALLOCATION RULING (docs/decision_log.md, 2026-08-02).
#
# WHY THIS EXISTS. M6.2 ran at 500 updates and its plateau guard fired on BOTH
# confirmatory arms: ISO drifted 1.06x its own floor over the final 100
# updates, JOINT 3.17x (sweep_p500 plateaued at 0.36x, and is secondary --
# it does not gate). The sharp part was the asymmetry: JOINT was still
# improving 1.69x faster than ISO at end of training, and since Gamma is
# exactly their difference, an asymmetric convergence rate is a direct
# confound on the headline quantity. The ruling orders a re-run at T = 1000
# rather than a discretionary extension, with the verdict fixed in advance.
#
# THE REGISTERED CRITERION, so it cannot be chosen after seeing the numbers:
#   T* = 1000 IFF BOTH confirmatory arms pass the plateau guard here.
#   Anything else STOPs to a human ruling. Specifically --
#     power@0.03 (Sidak m=2, k=34) below 80% on either confirmatory arm's
#       measured floor  ->  STOP, k is re-ruled by a human.
#     either confirmatory arm still climbing  ->  STOP, report drift ratios;
#       T* escalation is a human ruling. DO NOT self-extend run length.
#   At any STOP: report drift ratios and floors, NOT cross-arm means.
#
# THREE THINGS THIS SCRIPT WILL NOT LET YOU DO BY ACCIDENT:
#
#   1. CARRY THE T = 500 FLOORS FORWARD. It writes to a FRESH directory and
#      refuses to start if that directory already holds results. Floors are
#      per-artifact facts and a T = 500 floor does not grade a T = 1000 run
#      (CLAUDE.md, per-artifact amendment 2026-08-02). The old floors are
#      still on disk at results/phase6/m62/ and are still correct -- for the
#      artifact they were measured on, which is not this one.
#
#   2. START A MILESTONE RED. The three Monte-Carlo calibration test files
#      could not be run locally (they saturated the machine) and are owed;
#      they run here as a pre-flight, on a box that is rented anyway, before
#      a single training run starts.
#
#   3. RELEASE THE BOX WITHOUT THE ARCHIVES. The per-run tar.zst + sha256 come
#      from the inner script; this one asserts at the end that all of them
#      exist and that the hash file has one line per run. An un-archived
#      checkpoint is a result that cannot be re-rendered or audited after the
#      instance is gone (CLAUDE.md artifact-persistence rule).
#
# TAIL WINDOW IS DELIBERATELY UNCHANGED AT 100 UPDATES. The registered
# criterion is "final-100-update slope, floor-graded". At T = 1000 that is the
# last 10% rather than the last 20%; that is the criterion as written, and
# widening it to keep the fraction constant would be exercising discretion the
# ruling removed. Recorded here so the choice is visible rather than inherited.
#
# EXPECT ~3.7 GPU-h / ~$4: 24 runs at ~557 s each (2 x 269 s train + 19 s
# eval), extrapolated from M6.2's MEASURED 288 s/run at T = 500. Train scales
# linearly in updates; eval is flat. That extrapolation is an estimate and the
# script prints the measured figure at the end, which supersedes it.
#
# Run on the GPU box from the repo root:
#   GIT_COMMIT=<hash> bash che/scripts/run_m62b_t1000.sh 2>&1 | tee m62b_console.log
set -uo pipefail

OUT=${OUT:-che/bench/results/phase6/m62b}
UPDATES=${UPDATES:-1000}
REPS=${REPS:-8}

# ---------------------------------------------------------------- guard (1)
# A fresh directory, or an explicit decision to reuse one. Never a silent
# merge of two run lengths into one floors.json.
if [ -e "$OUT" ] && [ -n "$(ls -A "$OUT" 2>/dev/null)" ]; then
  echo "FATAL: $OUT already exists and is non-empty." >&2
  echo "  Floors are PER-ARTIFACT. Mixing run lengths in one output" >&2
  echo "  directory produces a floors.json that grades nothing. Move it" >&2
  echo "  aside or set OUT= to a new path." >&2
  exit 1
fi
if [ "$OUT" = "che/bench/results/phase6/m62" ]; then
  echo "FATAL: refusing to write into the T = 500 milestone directory." >&2
  exit 1
fi

# ---------------------------------------------------------------- guard (2)
# The owed CPU suite files, before any spend. These are cheap here and were
# not cheap locally. Fail loudly: CLAUDE.md forbids starting a milestone red.
OWED_TESTS=${OWED_TESTS:-"che/tests/test_prop3.py che/tests/test_calibration.py
                          che/tests/test_percolation.py che/tests/test_locks.py
                          che/tests/test_phase6_configs.py"}
echo "########## PRE-FLIGHT — the owed test files, before any training run"
echo "# NOTE these run under CUDA jax here, not the CPU jax they were owed"
echo "# under. A pass is good evidence, not the identical execution path."
# shellcheck disable=SC2086
uv run pytest $OWED_TESTS -q -p no:warnings || {
  echo "FATAL: owed tests are RED. Not spending GPU time on a red tree." >&2
  exit 1
}
echo "PRE-FLIGHT PASSED"

# --------------------------------------------------------------- the re-run
# Delegates to the M6.2 script UNMODIFIED, so the two milestones are the same
# instrument at two run lengths -- the only difference that may show up in the
# floors is the one being tested. That script is left untouched on purpose:
# it is the provenance of the T = 500 results.
echo ""
echo "########## M6.2b — ${REPS} reps x 3 arms at T = ${UPDATES}, out: ${OUT}"
OUT="$OUT" UPDATES="$UPDATES" REPS="$REPS" \
  bash che/scripts/run_m62_floors.sh || {
    echo "FATAL: the re-run failed — see above. SHAKEDOWN STOP." >&2
    exit 1
  }

# -------------------------------------------------------- toolchain record
# The inner script records jax/jaxlib but NOT the Python version, and on
# 2026-08-02 the Python version turned out to be the variable that silently
# chose the jax version: a box whose venv landed on 3.11 resolved jax 0.10.2
# (0.11.0 requires >= 3.12) while M6.0 and M6.2 had both run 0.11.0. uv.lock
# pinned 0.10.2 the whole time and bound neither. Nothing failed, because
# nothing recorded it. It is recorded now.
{
  echo ""
  echo "--- TOOLCHAIN (appended by run_m62b_t1000.sh) ---"
  uv run --no-sync python -c \
    'import sys, jax, jaxlib; print("python:", sys.version.split()[0]); \
print("jax:", jax.__version__, jaxlib.__version__); print("devices:", jax.devices())' \
    2>/dev/null || echo "TOOLCHAIN PROBE FAILED"
  echo "jax pinned to 0.11.0 deliberately, to match the toolchain M6.0"
  echo "certified traced-theta bitwise on and M6.2 measured its floors under."
} >> "$OUT/provenance.txt"

# ---------------------------------------------------------------- guard (3)
echo ""
echo "########## ARTIFACT-PERSISTENCE ASSERTION"
missing=0
for arm in iso joint sweep_p500; do
  for rep in $(seq 1 "$REPS"); do
    a="$OUT/ckpt_${arm}_rep${rep}.tar.zst"
    [ -s "$a" ] || { echo "MISSING ARCHIVE: $a" >&2; missing=$((missing + 1)); }
  done
done
want=$((REPS * 3))
got=$(wc -l < "$OUT/SHA256_CKPT.txt" 2>/dev/null || echo 0)
[ "$got" -eq "$want" ] || {
  echo "SHA256_CKPT.txt has $got lines, expected $want" >&2
  missing=$((missing + 1))
}
[ "$missing" -eq 0 ] || {
  echo "FATAL: $missing archive problem(s) — DO NOT RELEASE THE INSTANCE." >&2
  exit 1
}
echo "OK: $want archives present, $want hashes recorded."

cat <<EOF

##########  M6.2b COMPLETE — read the verdict, then STOP if it says STOP.

  Bring back $OUT/ in full, INCLUDING every .tar.zst and SHA256_CKPT.txt,
  and verify the sha256 of the transfer archive BEFORE releasing the box.

  The verdict in $OUT/verdict.txt is registered, not advisory:
    both confirmatory arms plateaued + power >= 80%  ->  T* = 1000, step (c)
    anything else                                    ->  STOP to a human

  Record the card in provenance.txt (the inner script does). Floors are
  per-hardware facts, so the grid must run on the SAME card that produced
  these floors.
EOF
