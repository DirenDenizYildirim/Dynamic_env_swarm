#!/usr/bin/env bash
# M3.1b GPU job — D5 obs-v2 causal-mechanism probes + reference bench row.
#
# (a) Retrain the three seed-0 severity probes under obs v2 (indicator
#     planes, D5) — same configs/seed/updates/dp as the M3.0 runs, so the
#     ONLY change vs ckpt_{sev}_dp0.5_s0 is the observation encoding.
# (b) 512 stochastic eval episodes per checkpoint through che.eval.harness.
# (c) Re-measure the M0.4 reference bench cell (64^2, 1024, 12) under v2 —
#     D5 expects ~neutral vs obs_v1_ref_cell.json (12,652,933 median).
#
# Run on the GPU box from the repo root (after git pull):
#   bash che/scripts/run_m31b_obs_v2.sh 2>&1 | tee m31b_console.log
# Expected wall time ~15-20 min (3 x ~265 s training + evals + bench).
# Bring back che/bench/results/phase3/m31b/ + m31b_console.log.
set -euo pipefail

OUT=che/bench/results/phase3/m31b
mkdir -p "$OUT"
: > "$OUT/timings.txt"

for sev in low medium high; do
  cfg="che/configs/severity_${sev}.yaml"
  tag="${sev}_v2_dp0.5_s0"
  echo "=== train ${tag} ($(date -u +%H:%M:%S)) ==="
  t0=$SECONDS
  uv run python -m che.train.ippo \
    --config "$cfg" \
    --updates 500 \
    --seed 0 \
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

echo "=== bench reference cell (obs v2) ==="
t0=$SECONDS
uv run python -m che.bench.throughput --cell 64,1024,12 \
  > "$OUT/obs_v2_ref_cell.json"
echo "bench_ref_cell $((SECONDS - t0))s" | tee -a "$OUT/timings.txt"
cat "$OUT/obs_v2_ref_cell.json"

echo "M3.1b GPU job complete — bring back $OUT/ and m31b_console.log"
