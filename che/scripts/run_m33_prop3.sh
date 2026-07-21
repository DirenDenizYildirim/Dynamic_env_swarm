#!/usr/bin/env bash
# M3.3 GPU job — full-scale Prop.-3 sweep (theory §10 handshake).
#
# L = 64, beta = 0.43 (Low), iota = 0, no primary ignition; lambda_0 sweep
# per che/calibration/prop3.py defaults; chi-hat reference is the
# size-matched Phase-2 value chi_hat_L64(0.43) = 66.38 read from
# che/bench/results/phase2/estimates.npz by the CLI itself.
# n-seeds 4096 (>= the 512 floor; GPU makes the extra precision free —
# at CPU scale 512-run chi-hat estimates moved ~±10%).
#
# Run on the GPU box from the repo root (after git pull):
#   bash che/scripts/run_m33_prop3.sh 2>&1 | tee m33_console.log
# Expected wall time: a few minutes.
# Bring back che/bench/results/phase3/m33/ + m33_console.log.
set -euo pipefail

uv run python -m che.calibration.prop3 \
  --grid-size 64 \
  --n-seeds 4096 \
  --out-dir che/bench/results/phase3/m33

echo "M3.3 GPU job complete — bring back che/bench/results/phase3/m33/ and m33_console.log"
