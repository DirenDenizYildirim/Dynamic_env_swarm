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
DP=${DP:-0.5}  # D4; must match what the calibration reproduces (hash guard)
N_EPS=${N_EPS:-64}
TAG="kB${KAPPA_PROBE}"  # every artifact is tagged, so runs at two
                        # candidate kappa_B values do not clobber
mkdir -p "$OUT"
: > "$OUT/probe_timings_${TAG}.txt"

probe_args=()
for sev in low medium high; do
  tag="probe_${sev}_${TAG}"
  echo "=== train ${tag} ($(date -u +%H:%M:%S)) ==="
  t0=$SECONDS
  uv run python -m che.train.ippo \
    --config "che/configs/severity_${sev}.yaml" \
    --updates 200 \
    --seed 0 \
    --death-penalty "$DP" \
    --kappa-B "$KAPPA_PROBE" \
    --ckpt-dir "$OUT/ckpt_${tag}" \
    --metrics "$OUT/${tag}.jsonl"
  echo "train_${tag} $((SECONDS - t0))s" | tee -a "$OUT/probe_timings_${TAG}.txt"
  probe_args+=(--probe-ckpt "${sev}=$OUT/ckpt_${tag}")
done

echo "=== calibration sweep under the probe policies ==="
t0=$SECONDS
uv run python -m che.calibration.coupling_b \
  --n-eps "$N_EPS" \
  --probe-kappa-B "$KAPPA_PROBE" \
  --probe-death-penalty "$DP" \
  "${probe_args[@]}" \
  --out-name "coupling_b_calibration_probe_${TAG}.json"
echo "calibration $((SECONDS - t0))s" | tee -a "$OUT/probe_timings_${TAG}.txt"

uv run python -m che.scripts.plot_m43_bands \
  --json "$OUT/coupling_b_calibration_probe_${TAG}.json" \
  --out "$OUT/kappa_b_bands_probe_${TAG}.png"

echo "M4.3 probe job complete (${TAG}) — bring back $OUT/ and the console log"
