#!/usr/bin/env bash
# M3.5 GPU job — Coupling-A acceptance training grid (phase3_prompt.md).
#
# Grid: 3 severities x kappa_A in {0, 0.06 (M3.4 lock)} x 2 seeds,
# dp = 0.5 (D4), 500 updates, locked Coupling-A params from the severity
# configs (coupling_a_lock.md). 12 train runs + 12 evals (512 stochastic
# episodes each). The kappa_A = 0 arm keeps the full structural dynamics
# (collapses, blocking, collapse-kill) and removes only the ignition
# coupling — the nesting-invariant ablation semantics.
#
# The eval harness records the M3.4-lock addendum channels
# (collapse_events, seeded_ignitions, blocked_moves, weak_occupancy) for
# the drift check against the random-policy calibration values.
#
# Run on the GPU box from the repo root (after git pull):
#   bash che/scripts/run_m35_grid.sh 2>&1 | tee m35_console.log
# Expected wall time ~1.2 GPU-h (12 x ~265 s training + evals).
# Bring back che/bench/results/phase3/m35/ + m35_console.log.
set -euo pipefail

OUT=che/bench/results/phase3/m35
KAPPA_LOCKED=0.06  # coupling_a_lock.md, human-locked 2026-07-21
mkdir -p "$OUT"
: > "$OUT/timings.txt"

for sev in low medium high; do
  cfg="che/configs/severity_${sev}.yaml"
  for ka in 0.0 "$KAPPA_LOCKED"; do
    ka_tag=$([ "$ka" = "0.0" ] && echo "ka0" || echo "kaL")
    for seed in 0 1; do
      tag="${sev}_${ka_tag}_dp0.5_s${seed}"
      echo "=== train ${tag} ($(date -u +%H:%M:%S)) ==="
      t0=$SECONDS
      uv run python -m che.train.ippo \
        --config "$cfg" \
        --updates 500 \
        --seed "$seed" \
        --death-penalty 0.5 \
        --kappa-A "$ka" \
        --ckpt-dir "$OUT/ckpt_${tag}" \
        --metrics "$OUT/${tag}.jsonl"
      echo "train_${tag} $((SECONDS - t0))s" | tee -a "$OUT/timings.txt"
      echo "=== eval ${tag} ==="
      t0=$SECONDS
      uv run python -m che.eval.harness \
        --config "$cfg" \
        --death-penalty 0.5 \
        --kappa-A "$ka" \
        --ckpt-dir "$OUT/ckpt_${tag}" \
        --n-episodes 512 \
        --seed 0 \
        --out-npz "$OUT/eval_${tag}.npz" \
        --out-json "$OUT/eval_${tag}.json"
      echo "eval_${tag} $((SECONDS - t0))s" | tee -a "$OUT/timings.txt"
    done
  done
done

echo "M3.5 GPU job complete — bring back $OUT/ and m35_console.log"
