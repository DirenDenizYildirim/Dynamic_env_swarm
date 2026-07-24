#!/usr/bin/env bash
# M4.1 GPU job — obs v3 (Coupling B) reference bench row.
#
# (a) Re-measure the M0.4 reference bench cell (64^2, 1024, 12) under
#     obs v3 (7 content planes masked by Beer-Lambert transmittance +
#     visibility plane). The transmittance quadrature and the reveal
#     uniforms run unconditionally (invariant #3), so the config's
#     kappa_B = 0 measures the true v3 cost.
# (b) One end-to-end training run (medium severity, 500 updates, seed 0,
#     dp 0.5 per D4) for the measured env-steps/s of a real train step.
#
# Standing rule (decision log, 2026-07-21): if the training projection at
# the Phase-0 env:train ratio (env-only median / 81) lands below 100k
# steps/s, the uint8 obs-storage contingency activates and is re-benched
# before the M4.2+ acceptance runs — not discussed, activated.
#
# Run on the GPU box from the repo root (after git pull):
#   bash che/scripts/run_m41_obs_v3_bench.sh 2>&1 | tee m41_console.log
# Expected wall time ~10 min (bench windows + one ~300 s training run).
# Bring back che/bench/results/phase4/m41/ + m41_console.log.
set -euo pipefail

OUT=che/bench/results/phase4/m41
mkdir -p "$OUT"
: > "$OUT/timings.txt"

echo "=== bench reference cell (obs v3) ==="
t0=$SECONDS
uv run python -m che.bench.throughput --cell 64,1024,12 \
  > "$OUT/obs_v3_ref_cell.json"
echo "bench_ref_cell $((SECONDS - t0))s" | tee -a "$OUT/timings.txt"
cat "$OUT/obs_v3_ref_cell.json"

tag="medium_v3_dp0.5_s0"
echo "=== train ${tag} ($(date -u +%H:%M:%S)) ==="
t0=$SECONDS
uv run python -m che.train.ippo \
  --config che/configs/severity_medium.yaml \
  --updates 500 \
  --seed 0 \
  --death-penalty 0.5 \
  --ckpt-dir "$OUT/ckpt_${tag}" \
  --metrics "$OUT/${tag}.jsonl"
echo "train_${tag} $((SECONDS - t0))s" | tee -a "$OUT/timings.txt"

echo "M4.1 GPU job complete — bring back $OUT/ and m41_console.log"
