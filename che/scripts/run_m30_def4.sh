#!/usr/bin/env bash
# M3.0 GPU job — Def.-4 variance re-test data.
#
# (a) Re-run the 9 M2.5 dp=0.5 runs (3 severities x 3 seeds, 500 updates)
#     WITH checkpointing this time — same configs/seeds, so each run
#     reproduces its M2.5 counterpart (the JSONLs can be diffed against
#     che/bench/results/phase2/m25/ to confirm).
# (b) For each final checkpoint, run 512 stochastic eval episodes through
#     che.eval.harness -> per-episode npz + summary JSON.
#
# Run on the GPU box from the repo root (after git pull):
#   bash che/scripts/run_m30_def4.sh 2>&1 | tee m30_console.log
# Expected wall time ~45-55 min (training ~265 s/run at M2.5 throughput).
# Bring back the whole che/bench/results/phase3/m30/ directory (checkpoints
# included — they are small and later milestones reuse them) + m30_console.log.
set -euo pipefail

OUT=che/bench/results/phase3/m30
mkdir -p "$OUT"
: > "$OUT/timings.txt"

for sev in low medium high; do
  cfg="che/configs/severity_${sev}.yaml"
  for seed in 0 1 2; do
    tag="${sev}_dp0.5_s${seed}"
    echo "=== train ${tag} ($(date -u +%H:%M:%S)) ==="
    t0=$SECONDS
    uv run python -m che.train.ippo \
      --config "$cfg" \
      --updates 500 \
      --seed "$seed" \
      --death-penalty 0.5 \
      --ckpt-dir "$OUT/ckpt_${tag}" \
      --metrics "$OUT/${tag}.jsonl"
    echo "train_${tag} $((SECONDS - t0))s" | tee -a "$OUT/timings.txt"
    echo "=== eval ${tag} ==="
    t0=$SECONDS
    uv run python -m che.eval.harness \
      --config "$cfg" \
      --death-penalty 0.5 \
      --ckpt-dir "$OUT/ckpt_${tag}" \
      --n-episodes 512 \
      --seed 0 \
      --out-npz "$OUT/eval_${tag}.npz" \
      --out-json "$OUT/eval_${tag}.json"
    echo "eval_${tag} $((SECONDS - t0))s" | tee -a "$OUT/timings.txt"
  done
done

echo "M3.0 GPU job complete — bring back $OUT/ and m30_console.log"
