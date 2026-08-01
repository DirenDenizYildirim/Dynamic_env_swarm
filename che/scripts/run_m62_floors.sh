#!/usr/bin/env bash
# M6.2 — the Phase-6 floor milestone. RUNS BEFORE ANY BAR EXISTS.
#
# Registered in phase6_design_v2.md §4; rulings in docs/decision_log.md
# ("PHASE-6 REMEDY RULINGS" 4, "PHASE-6 RULINGS, FINAL FIVE" 1a and 3, and
# the seed amendment).
#
# FOUR JOBS, and it is worth naming them because this one milestone absorbed
# the work of three things that used to be separate:
#
#   1. FLOORS, PER-ARM. 8 identical reps (same seed) of ISO, JOINT-classic and
#      the p = 0.5 sweep point, each evaluated at theta*. The sd across reps
#      is run-to-run nondeterminism -- NOT seed spread -- and it is measured
#      per arm because floors are PER-ARTIFACT (CLAUDE.md, 2026-08-02): ISO
#      and JOINT are different artifacts and a floor measured on one may not
#      grade the other. 8 rather than 4 because n = 4 leaves the sd uncertain
#      by ~+/-40% (M5.5) and every threshold in the phase rests on these.
#
#   2. SHAKEDOWN. This replaces the dropped pilot's only surviving purpose: 24
#      full runs end-to-end with evals before the grid. ANY process surprise
#      STOPs the phase.
#
#   3. PLATEAU GUARD for the 500-update ruling. Final-100-update slope against
#      zero, floor-graded. If the headline configs are still climbing, STOP
#      and re-rule -- the length question becomes a measurement instead of an
#      argument.
#
#   4. EVAL COST, measured. v2 section 6 estimates it; this discharges the
#      estimate by timing train and eval separately.
#
# CROSS-CONFIG EVALUATION IS THE POINT, AND IS DECLARED. Policies train on a
# protocol config and are evaluated at theta* -- a different config, so the
# harness's config-hash guard refuses by default. That guard is correct and is
# not bypassed: each eval passes --allow-hash with the TRAINING config's hash,
# which the harness records in its provenance (the m30b cross-severity
# precedent). The generalization test is thereby declared, not smuggled.
#
# Run on the GPU box from the repo root:
#   bash che/scripts/run_m62_floors.sh 2>&1 | tee m62_console.log
set -uo pipefail

OUT=${OUT:-che/bench/results/phase6/m62}
REPS=${REPS:-8}
UPDATES=${UPDATES:-500}
N_EVAL=${N_EVAL:-512}
FLOOR_SEED=${FLOOR_SEED:-0}
THETA_STAR=che/configs/theta_star_holdout.yaml
# arm name -> training config
ARMS=${ARMS:-"iso:che/configs/p6_iso.yaml joint:che/configs/p6_joint.yaml sweep_p500:che/configs/p6_sweep_c50_p500.yaml"}

mkdir -p "$OUT"
: > "$OUT/timings.txt"

# Fail early rather than 20 runs in.
uv run python -m che.eval.harness --help 2>/dev/null | grep -q -- "--allow-hash" || {
  echo "FATAL: eval harness has no --allow-hash; cross-config eval impossible" >&2
  exit 1
}
tar --zstd -cf /dev/null --files-from /dev/null 2>/dev/null || {
  echo "FATAL: 'tar --zstd' unavailable" >&2; exit 1
}

# $1 arm  $2 training config  $3 rep
run_one () {
  local arm=$1 cfg=$2 rep=$3 tag t0 t1
  tag="${arm}_rep${rep}"
  echo ""
  echo "=== ${tag}: train ${UPDATES} updates on ${cfg}"
  t0=$SECONDS
  uv run python -m che.train.ippo \
    --config "$cfg" --updates "$UPDATES" --seed "$FLOOR_SEED" \
    --ckpt-dir "$OUT/ckpt_${tag}" --metrics "$OUT/${tag}.jsonl" || return 1
  t1=$SECONDS
  echo "train_${tag} $((t1 - t0))s" | tee -a "$OUT/timings.txt"

  # The training config's hash — declared to the guard, recorded by it.
  local train_hash
  train_hash=$(cat "$OUT/ckpt_${tag}/config_hash.txt")
  echo "=== ${tag}: eval ${N_EVAL} episodes AT THETA* (allow-hash ${train_hash})"
  uv run python -m che.eval.harness \
    --config "$THETA_STAR" --ckpt-dir "$OUT/ckpt_${tag}" \
    --allow-hash "$train_hash" \
    --n-episodes "$N_EVAL" --seed 0 \
    --out-npz "$OUT/eval_${tag}.npz" --out-json "$OUT/eval_${tag}.json" || return 1
  echo "eval_${tag} $((SECONDS - t1))s" | tee -a "$OUT/timings.txt"

  tar --zstd -cf "$OUT/ckpt_${tag}.tar.zst" -C "$OUT" "ckpt_${tag}"
  sha256sum "$OUT/ckpt_${tag}.tar.zst" | tee -a "$OUT/SHA256_CKPT.txt"
}

echo "########## M6.2 — per-arm floors, ${REPS} reps x $(echo $ARMS | wc -w) arms"
for pair in $ARMS; do
  arm="${pair%%:*}"; cfg="${pair##*:}"
  for rep in $(seq 1 "$REPS"); do
    run_one "$arm" "$cfg" "$rep" || {
      echo "FATAL: ${arm} rep ${rep} failed — SHAKEDOWN STOP" >&2
      exit 1
    }
  done
done

echo ""
echo "########## ANALYSIS"
uv run python -m che.scripts.m62_report --out "$OUT" --reps "$REPS" \
  --arms "$ARMS" --updates "$UPDATES" 2>&1 | tee "$OUT/verdict.txt"

{
  echo "run: M6.2 Phase-6 floor milestone (per-arm floors + plateau + eval cost)"
  echo "date_utc: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  # The box has no .git (source is shipped as a tarball), so the commit
  # is passed in explicitly. Provenance must not silently read "unknown".
  echo "git_commit: ${GIT_COMMIT:-$(git rev-parse HEAD 2>/dev/null || echo UNKNOWN-PROVENANCE-GAP)}"
  echo "git_dirty: $(git status --porcelain 2>/dev/null | wc -l) file(s)"
  echo "arms: $ARMS"
  echo "reps: $REPS (IDENTICAL runs at seed $FLOOR_SEED — nondeterminism, not seed spread)"
  echo "updates: $UPDATES   eval_episodes: $N_EVAL   eval_config: $THETA_STAR"
  echo "cross-config eval: declared via --allow-hash (training-config hash)"
  echo "gpu: $(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null || echo unknown)"
  echo "jax: $(uv run python -c 'import jax,jaxlib;print(jax.__version__,jaxlib.__version__)' 2>/dev/null || echo unknown)"
} | tee "$OUT/provenance.txt"

for f in provenance.txt timings.txt verdict.txt floors.json; do
  [ -s "$OUT/$f" ] || { echo "FATAL: $OUT/$f missing — do NOT release" >&2; exit 1; }
done
echo ""
echo "M6.2 complete — bring back $OUT/ (incl. every .tar.zst + SHA256_CKPT.txt)"
