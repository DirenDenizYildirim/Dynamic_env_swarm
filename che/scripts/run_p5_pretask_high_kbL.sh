#!/usr/bin/env bash
# Phase-5 pre-task, part 2 — the MATCHED HALF of the High render pair.
#
# Why this exists. Part 1 (High, kappa_B = 0, seed 0) did not reproduce
# M4.4: completion 0.7905 -> 0.8412, survival 0.9408 -> 0.9160, return
# 24.939 -> 26.414 — same commit (0c612b6; no che/ change since the M4.4
# close), same config, same seed, same GPU model. GPU training is not
# run-to-run reproducible: XLA picks kernels by autotuned timing and some
# reductions use atomics, so 500 updates of a chaotic optimization diverge.
# An un-archived checkpoint is therefore gone, not "re-derivable" — the
# artifact-persistence lapse cashing out on the exact artifact the rule was
# written about.
#
# Consequence: part 1's renders are NOT comparable to M4.4's locked-arm
# renders. They ARE comparable to a locked-arm replicate trained the same
# way, which is what this job makes. Both arms then come from the same
# recipe at the same commit, rendered on the same six episode seeds, so the
# audit's actual question — does the kappa_B = 1.0 arm position itself
# differently around smoke — is answered by a matched *pair*.
#
# Second, unplanned value: this is also a same-seed replicate of the kbL
# arm, so the pair measures run-to-run nondeterminism on BOTH arms and says
# what M4.4's two-seed "sigma_seed" was actually measuring. The cross-arm
# effect recomputed on replicates is a free robustness check of the Phase-4
# headline (-8.8 pt survival at High).
#
# MUST run on this branch (based on 0c612b6): after M5.0 the network has a
# message head, and a retrain there would be a different architecture.
#
# Run on the GPU box from the repo root:
#   git fetch origin && git checkout pretask-replicates
#   bash che/scripts/run_p5_pretask_high_kbL.sh 2>&1 | tee p5pre_kbL_console.log
# Expected wall time ~7 GPU-min. Bring back che/bench/results/phase5/pretask/
# (this job adds to part 1's directory) + p5pre_kbL_console.log.
set -euo pipefail

OUT=che/bench/results/phase5/pretask
REF=che/bench/results/phase4/m44
CFG=che/configs/severity_high.yaml
DP=0.5                                    # D4
KB=1.0                                    # the M4.3-locked arm
SEED=0
N_EVAL=${N_EVAL:-512}
TAG="high_kbL_dp${DP}_s${SEED}"
CKPT="$OUT/ckpt_${TAG}"
mkdir -p "$OUT/renders"

[ -e che/env/comms.py ] && {
  echo "FATAL: che/env/comms.py exists -> M5.0 has landed in this tree." >&2
  echo "Run from the pretask-replicates branch (based on 0c612b6)." >&2
  exit 1
}
tar --zstd -cf /dev/null --files-from /dev/null 2>/dev/null || {
  echo "FATAL: 'tar --zstd' unavailable (needs GNU tar >= 1.31 + zstd)." >&2
  exit 1
}
[ -f "$REF/eval_${TAG}.json" ] || {
  echo "FATAL: missing $REF/eval_${TAG}.json — nothing to compare against." >&2
  exit 1
}

echo "=== train ${TAG} ($(date -u +%H:%M:%S)) ==="
t0=$SECONDS
uv run python -m che.train.ippo \
  --config "$CFG" \
  --updates 500 \
  --seed "$SEED" \
  --death-penalty "$DP" \
  --kappa-B "$KB" \
  --ckpt-dir "$CKPT" \
  --metrics "$OUT/${TAG}.jsonl"
echo "train_${TAG} $((SECONDS - t0))s" | tee -a "$OUT/timings.txt"

echo "=== eval ${TAG} ==="
t0=$SECONDS
uv run python -m che.eval.harness \
  --config "$CFG" \
  --death-penalty "$DP" \
  --kappa-B "$KB" \
  --ckpt-dir "$CKPT" \
  --n-episodes "$N_EVAL" \
  --seed 0 \
  --out-npz "$OUT/eval_${TAG}.npz" \
  --out-json "$OUT/eval_${TAG}.json"
echo "eval_${TAG} $((SECONDS - t0))s" | tee -a "$OUT/timings.txt"

# Evidence table for the human: replicate-vs-original deltas on both arms,
# and the cross-arm effect computed both ways. No verdict is decided here.
uv run python - "$OUT" "$REF" <<'PY' | tee "$OUT/replicate_deltas.txt"
import json, os, sys
out, ref = sys.argv[1], sys.argv[2]
keys = ("completion", "survival_rate", "episode_return")


def metrics(path):
    return json.load(open(path))["metrics"]


data = {}
for arm in ("kb0", "kbL"):
    name = f"eval_high_{arm}_dp0.5_s0.json"
    new = metrics(os.path.join(out, name))
    old = metrics(os.path.join(ref, name))
    data[arm] = {k: (new[k]["mean"], old[k]["mean"]) for k in keys}

print("Same-seed replicate vs M4.4 original (High, dp 0.5, seed 0):")
for arm in ("kb0", "kbL"):
    for k in keys:
        a, b = data[arm][k]
        print(f"  {arm}  {k:15s} replicate={a:8.4f}  m44={b:8.4f}  "
              f"delta={a - b:+.4f}")

print("\nCross-arm effect (kbL - kb0), computed two ways:")
for label, idx in (("replicate pair", 0), ("M4.4 originals", 1)):
    for k in keys:
        d = data["kbL"][k][idx] - data["kb0"][k][idx]
        print(f"  {label:16s} {k:15s} {d:+.4f}")
print("\nSame sign and rough size across the two rows => the Phase-4 finding")
print("is robust to run-to-run nondeterminism. A sign flip or a collapse in")
print("magnitude is a STOP and goes to the human with these numbers.")
PY

echo "=== renders: the same six episode seeds as part 1 ==="
for ep in 0 1 2 3 4 5; do
  uv run python -m che.scripts.render_episode \
    --config "$CFG" \
    --death-penalty "$DP" \
    --kappa-B "$KB" \
    --ckpt-dir "$CKPT" \
    --seed "$ep" \
    --out "$OUT/renders/high_kbL_replicate_ep${ep}.gif" \
    --tag "high kappa_B=1.0 ep${ep} (replicate)"
done

# --- Artifact persistence (CLAUDE.md, human-issued 2026-07-28) ---------
ARCHIVE="$OUT/ckpt_${TAG}.tar.zst"
echo "=== archive ${ARCHIVE} ==="
tar --zstd -cf "$ARCHIVE" -C "$OUT" "ckpt_${TAG}"
sha256sum "$ARCHIVE" | tee "$ARCHIVE.sha256"
[ -s "$ARCHIVE" ] && [ -s "$ARCHIVE.sha256" ] || {
  echo "FATAL: archive or sha256 missing — do NOT release the instance" >&2
  exit 1
}
{
  echo "run: phase-5 pre-task part 2 (High kappa_B=1.0 replicate + renders)"
  echo "date_utc: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "git_commit: $(git rev-parse HEAD)"
  echo "git_dirty: $(git status --porcelain | wc -l) file(s)"
  echo "config: $CFG  dp=$DP  kappa_B=$KB  seed=$SEED  updates=500"
  echo "archive_sha256: $(cut -d' ' -f1 < "$ARCHIVE.sha256")"
  echo "gpu: $(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null || echo unknown)"
} | tee "$OUT/provenance_kbL.txt"

echo
echo "Part 2 complete — bring back $OUT/ (incl. both .tar.zst + .sha256) and"
echo "p5pre_kbL_console.log. Instance may be released ONLY after that copy."
