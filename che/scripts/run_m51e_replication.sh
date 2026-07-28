#!/usr/bin/env bash
# M5.1e GPU job — MINI REPLICATION STUDY: measure the reproducibility floor
# (~22 GPU-min).
#
# Human ruling 2026-07-28 (M5.1 STOP, ruling 3a). The pre-task produced a
# single same-seed replicate pair, which showed run-to-run nondeterminism
# large enough to flip the sign of the M4.4 completion effect — but n=1 per
# arm is an anecdote, and the two arms disagreed about how noisy they were
# (survival delta -0.0247 on kb0, -0.0031 on kbL). This runs the SAME cell
# four times, identically, so the floor becomes a measured distribution.
#
# The cell is what M5.5 will actually run: Medium severity, both couplings
# at locked values, comms live at delta = 0, dp = 0.5, 500 updates, seed 0.
# Same seed every time — the variation measured here is nondeterminism
# alone, with seed variation deliberately held out. That is the quantity
# falsifier condition (i) needs (ruling 3b), and it is NOT the same thing
# as across-seed spread.
#
# These four checkpoints are, by construction, unreproducible: they are the
# evidence. All four are archived (persistence rule) — re-running the script
# would produce four different policies.
#
# Run on the GPU box from the repo root, on main (after git pull):
#   bash che/scripts/run_m51e_replication.sh 2>&1 | tee m51e_console.log
# Bring back che/bench/results/phase5/m51e/ + m51e_console.log.
set -euo pipefail

OUT=che/bench/results/phase5/m51e
CFG=che/configs/severity_medium.yaml
DP=0.5
SEED=0
N_EVAL=${N_EVAL:-512}
REPS=${REPS:-4}
mkdir -p "$OUT"
: > "$OUT/timings.txt"

[ -e che/env/comms.py ] || {
  echo "FATAL: not an M5.0+ tree — the floor must be measured on the code" >&2
  echo "M5.5 will run. Checkout main." >&2
  exit 1
}
tar --zstd -cf /dev/null --files-from /dev/null 2>/dev/null || {
  echo "FATAL: 'tar --zstd' unavailable (needs GNU tar >= 1.31 + zstd)." >&2
  exit 1
}

for rep in $(seq 1 "$REPS"); do
  TAG="medium_rep${rep}"
  echo "=== replicate ${rep}/${REPS}: train (identical config, identical seed) ==="
  t0=$SECONDS
  uv run python -m che.train.ippo \
    --config "$CFG" \
    --updates 500 \
    --seed "$SEED" \
    --death-penalty "$DP" \
    --ckpt-dir "$OUT/ckpt_${TAG}" \
    --metrics "$OUT/${TAG}.jsonl"
  echo "train_${TAG} $((SECONDS - t0))s" | tee -a "$OUT/timings.txt"

  uv run python -m che.eval.harness \
    --config "$CFG" \
    --death-penalty "$DP" \
    --ckpt-dir "$OUT/ckpt_${TAG}" \
    --n-episodes "$N_EVAL" \
    --seed 0 \
    --out-npz "$OUT/eval_${TAG}.npz" \
    --out-json "$OUT/eval_${TAG}.json"

  tar --zstd -cf "$OUT/ckpt_${TAG}.tar.zst" -C "$OUT" "ckpt_${TAG}"
  sha256sum "$OUT/ckpt_${TAG}.tar.zst" | tee "$OUT/ckpt_${TAG}.tar.zst.sha256"
  [ -s "$OUT/ckpt_${TAG}.tar.zst.sha256" ] || {
    echo "FATAL: archive missing for ${TAG} — do NOT release the instance" >&2
    exit 1
  }
done

uv run python - "$OUT" "$REPS" <<'PY' | tee "$OUT/reproducibility_floor.txt"
import json, os, statistics, sys
out, reps = sys.argv[1], int(sys.argv[2])
keys = ("completion", "survival_rate", "episode_return", "deaths_fire",
        "mean_smoke_exposure")
vals = {k: [] for k in keys}
for rep in range(1, reps + 1):
    m = json.load(open(os.path.join(out, f"eval_medium_rep{rep}.json")))["metrics"]
    for k in keys:
        if k in m:
            vals[k].append(m[k]["mean"])

print(f"Reproducibility floor — {reps} identical runs (Medium, dp 0.5, seed 0,")
print("500 updates, couplings locked, comms live at delta = 0).")
print("Same seed throughout: this is nondeterminism alone, NOT seed spread.\n")
print(f"  {'metric':22s} {'mean':>10s} {'sd':>10s} {'range':>10s} {'max|dev|':>10s}")
floor = {}
for k in keys:
    v = vals[k]
    if len(v) < 2:
        continue
    mu = statistics.mean(v)
    sd = statistics.stdev(v)
    rng = max(v) - min(v)
    dev = max(abs(x - mu) for x in v)
    floor[k] = {"mean": mu, "sd": sd, "range": rng, "max_abs_dev": dev,
                "values": v, "n": len(v)}
    print(f"  {k:22s} {mu:10.4f} {sd:10.4f} {rng:10.4f} {dev:10.4f}")
json.dump(floor, open(os.path.join(out, "reproducibility_floor.json"), "w"),
          indent=1)

print("\nHow to use this (ruling 3b): falsifier condition (i) reads 'within the")
print("measured reproducibility floor', citing this study. A cross-arm effect")
print("smaller than ~2x the sd here is NOT resolvable at one run per cell.")
print(f"\nCAVEAT, stated because it bounds every use: n = {reps} gives an sd with")
print(f"{reps - 1} degrees of freedom — itself uncertain by roughly +/-40 %. Treat")
print("the floor as an order of magnitude, not a threshold to three decimals.")
print("It also describes the NON-DETERMINISTIC regime; if headline runs go")
print("deterministic (ruling 1d/3c), their floor is a different, smaller")
print("quantity dominated by seed variation and must be measured separately.")
PY

{
  echo "run: M5.1e mini replication study (reproducibility floor)"
  echo "date_utc: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "git_commit: $(git rev-parse HEAD)"
  echo "git_dirty: $(git status --porcelain | wc -l) file(s)"
  echo "config: $CFG  dp=$DP  seed=$SEED (identical across replicates)  reps=$REPS"
  echo "gpu: $(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null || echo unknown)"
} | tee "$OUT/provenance.txt"

echo "M5.1e complete — bring back $OUT/ (incl. all .tar.zst + .sha256) and"
echo "m51e_console.log. These checkpoints cannot be regenerated."
