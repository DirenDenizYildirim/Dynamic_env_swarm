#!/usr/bin/env bash
# M4.3 GPU job — probe policies for the kappa_B calibration
# (phase4_prompt.md M4.3: "random policy + one fresh 200-update probe
# policy per severity, obs v3, both couplings on").
#
# Trains one 200-update probe per severity at KAPPA_PROBE with Coupling A
# live at its M3.4-locked values, then re-runs the M4.3 calibration under
# those policies — the probe supplies a realistic *state distribution*;
# the sweep still evaluates every kappa_B candidate on it (CRN), so the
# observable's kappa_B dependence is not confounded with the policy's
# reaction to kappa_B.
#
# KAPPA_PROBE is provisional: kappa_B is exactly what M4.3 is trying to
# lock, so the probe is trained at the RA-recommended candidate
# (kappa_b_lock.md option A). Override to match whatever the lock
# discussion settles on:
#
#   KAPPA_PROBE=1.5 bash che/scripts/run_m43_probes.sh
#
# Run on the GPU box from the repo root (after git pull):
#   bash che/scripts/run_m43_probes.sh 2>&1 | tee m43_console.log
# Expected wall time ~10 GPU-min (3 x ~110 s training + one CPU sweep).
# Bring back che/bench/results/phase4/m43/ + m43_console.log.
set -euo pipefail

OUT=che/bench/results/phase4/m43
KAPPA_PROBE=${KAPPA_PROBE:-0.5}
N_EPS=${N_EPS:-64}
mkdir -p "$OUT"
: > "$OUT/probe_timings.txt"

probe_args=()
for sev in low medium high; do
  tag="probe_${sev}_kB${KAPPA_PROBE}"
  echo "=== train ${tag} ($(date -u +%H:%M:%S)) ==="
  t0=$SECONDS
  uv run python -m che.train.ippo \
    --config "che/configs/severity_${sev}.yaml" \
    --updates 200 \
    --seed 0 \
    --death-penalty 0.5 \
    --kappa-B "$KAPPA_PROBE" \
    --ckpt-dir "$OUT/ckpt_${tag}" \
    --metrics "$OUT/${tag}.jsonl"
  echo "train_${tag} $((SECONDS - t0))s" | tee -a "$OUT/probe_timings.txt"
  probe_args+=(--probe-ckpt "${sev}=$OUT/ckpt_${tag}")
done

echo "=== calibration sweep under the probe policies ==="
t0=$SECONDS
uv run python -m che.calibration.coupling_b \
  --n-eps "$N_EPS" \
  --probe-kappa-B "$KAPPA_PROBE" \
  "${probe_args[@]}" \
  --out-name coupling_b_calibration_probe.json
echo "calibration $((SECONDS - t0))s" | tee -a "$OUT/probe_timings.txt"

uv run python -m che.scripts.plot_m43_bands \
  --json "$OUT/coupling_b_calibration_probe.json" \
  --out "$OUT/kappa_b_bands_probe.png"

echo "M4.3 probe job complete — bring back $OUT/ and m43_console.log"
