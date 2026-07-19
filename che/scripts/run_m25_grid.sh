#!/usr/bin/env bash
# M2.5 pillar-only training probe: 3 locked severities x death_penalty
# {0.0, 0.5} x 3 seeds = 18 runs (dynamic mode, single policy, n_envs 256,
# 500 updates each) + one random-baseline row per severity.
# Run on the GPU box from the repo root:
#   bash che/scripts/run_m25_grid.sh 2>&1 | tee m25_console.log
# Results land in che/bench/results/phase2/m25/ (JSONL per run + baselines
# + timing log); bring the whole directory (and m25_console.log) back.
set -euo pipefail

OUT=che/bench/results/phase2/m25
mkdir -p "$OUT"
: > "$OUT/timings.txt"

for sev in low medium high; do
  cfg="che/configs/severity_${sev}.yaml"
  echo "=== baseline ${sev} ==="
  uv run python -m che.train.ippo --config "$cfg" --baseline \
    > "$OUT/baseline_${sev}.json"
  for dp in 0.0 0.5; do
    for seed in 0 1 2; do
      tag="${sev}_dp${dp}_s${seed}"
      echo "=== run ${tag} ($(date -u +%H:%M:%S)) ==="
      t0=$SECONDS
      uv run python -m che.train.ippo \
        --config "$cfg" \
        --updates 500 \
        --seed "$seed" \
        --death-penalty "$dp" \
        --metrics "$OUT/${tag}.jsonl"
      echo "${tag} $((SECONDS - t0))s" | tee -a "$OUT/timings.txt"
    done
  done
done

echo "all 18 runs + 3 baselines complete"
