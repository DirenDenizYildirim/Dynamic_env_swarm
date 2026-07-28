#!/usr/bin/env bash
# Phase-5 PRE-TASK — matched High kappa_B = 0 render control set.
#
# Why this exists: phase4_report.md flagged that matched kappa_B = 0
# renders exist only at Medium (M4.4 amendment 4c), while the headline
# Coupling-B result — survival -8.8 pt — is at High. The Phase-5 prompt
# requires the matched High control (6 episodes, the same episode seeds as
# the locked-arm High renders) before M5.0 starts.
#
# Why it retrains: the M4.4 checkpoints were never archived off-instance
# ("stay on the box", run_m44_grid.sh) and the box was released. That is
# the violation the CLAUDE.md artifact-persistence rule now forbids, and
# this script is the first one written under it — it archives its own
# checkpoint (tar.zst + sha256) and FAILS if the archive is missing.
#
# Retrain reproduces M4.4's high/kb0/s0 arm: same code (no che/ change
# since the M4.4 close), same config, same seed, same 500 updates. The
# script re-runs the eval and diffs it against the archived M4.4 eval JSON
# so reproduction is *verified*, not assumed — if the numbers drift, the
# renders are not a matched control and the script says so loudly.
#
# Run on the GPU box from the repo root (after git pull):
#   bash che/scripts/run_p5_pretask_high_kb0.sh 2>&1 | tee p5pre_console.log
# Expected wall time ~7 GPU-min (1 x ~280 s train + eval + 6 renders).
# Bring back che/bench/results/phase5/pretask/ + p5pre_console.log.
set -euo pipefail

OUT=che/bench/results/phase5/pretask
REF=che/bench/results/phase4/m44          # M4.4 artifacts, in git
CFG=che/configs/severity_high.yaml
DP=0.5                                    # D4
KB=0.0                                    # the control arm
SEED=0                                    # M4.4 render arm is s0
N_EVAL=${N_EVAL:-512}                     # match M4.4 eval_* n_episodes
TAG="high_kb0_dp${DP}_s${SEED}"
CKPT="$OUT/ckpt_${TAG}"
mkdir -p "$OUT/renders"
: > "$OUT/timings.txt"

# Pre-flight: this script MUST run at a pre-M5.0 commit (0c612b6 or
# earlier). M5.0 adds a message head to ActorCritic, so after it lands the
# M4.4 architecture no longer exists in the tree: a "retrain" would train a
# different network and the renders would not be a matched control for the
# locked-arm High renders. `che/env/comms.py` is the M5.0 marker.
[ -e che/env/comms.py ] && {
  echo "FATAL: che/env/comms.py exists -> M5.0 (message head) has landed." >&2
  echo "The M4.4 architecture is gone from this tree, so a retrain here is" >&2
  echo "NOT a matched control. Run this script from commit 0c612b6:" >&2
  echo "  git stash && git checkout 0c612b6 && bash \$0" >&2
  exit 1
}
# Pre-flight: fail in 1 s, not after 7 GPU-min, if the archiver the
# persistence rule requires is not on the box.
tar --zstd -cf /dev/null --files-from /dev/null 2>/dev/null || {
  echo "FATAL: 'tar --zstd' unavailable (needs GNU tar >= 1.31 + zstd)." >&2
  echo "Install zstd before running — the archive step is not optional." >&2
  exit 1
}
[ -f "$REF/eval_${TAG}.json" ] || {
  echo "FATAL: missing $REF/eval_${TAG}.json — the reproduction check" >&2
  echo "has nothing to compare against; did the repo pull complete?" >&2
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

echo "=== eval ${TAG} (reproduction check vs M4.4) ==="
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

# Reproduction verdict: compare the fresh eval against the M4.4 JSON that
# is already in git. Reported, never silently tolerated — a mismatch means
# the render set is NOT matched to the locked-arm High renders.
uv run python - "$OUT/eval_${TAG}.json" "$REF/eval_${TAG}.json" <<'PY' | tee "$OUT/reproduction.txt"
import json, sys
new, ref = (json.load(open(p))["metrics"] for p in sys.argv[1:3])
keys = ("episode_return", "completion", "survival_rate")
rows, worst = [], 0.0
for k in keys:
    a, b = new[k]["mean"], ref[k]["mean"]
    d = abs(a - b)
    worst = max(worst, d / (abs(b) + 1e-9))
    rows.append(f"  {k:16s} fresh={a:.6f}  m44={b:.6f}  |delta|={d:.2e}")
print("M4.4 reproduction check (High, kappa_B=0, dp=0.5, seed 0):")
print("\n".join(rows))
print(f"worst relative delta: {worst:.3e}")
print("VERDICT: BITWISE-ISH REPRODUCTION" if worst < 1e-6 else
      "VERDICT: DRIFT — renders are NOT a matched control; report before use")
PY

# --- Render audit: the 6 episode seeds M4.4 rendered on the locked arm ---
# Same seeds as $REF/renders/high_kbL_ep{0..5}.gif, kappa_B = 0 policy.
for ep in 0 1 2 3 4 5; do
  uv run python -m che.scripts.render_episode \
    --config "$CFG" \
    --death-penalty "$DP" \
    --kappa-B "$KB" \
    --ckpt-dir "$CKPT" \
    --seed "$ep" \
    --out "$OUT/renders/high_kb0_ep${ep}.gif" \
    --tag "high kappa_B=0 ep${ep} (matched control)"
done

# --- Artifact persistence (CLAUDE.md, human-issued 2026-07-28) ----------
# Archive the checkpoint off-instance and assert it exists. This is the
# rule M4.4 violated; the assert is what makes the rule real.
ARCHIVE="$OUT/ckpt_${TAG}.tar.zst"
echo "=== archive ${ARCHIVE} ==="
tar --zstd -cf "$ARCHIVE" -C "$OUT" "ckpt_${TAG}"
sha256sum "$ARCHIVE" | tee "$ARCHIVE.sha256"
[ -s "$ARCHIVE" ] && [ -s "$ARCHIVE.sha256" ] || {
  echo "FATAL: checkpoint archive or sha256 missing — do NOT release the instance" >&2
  exit 1
}
# Provenance alongside the archive, so the phase report can cite it.
{
  echo "run: phase-5 pre-task (matched High kappa_B=0 renders)"
  echo "date_utc: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "git_commit: $(git rev-parse HEAD)"
  echo "git_dirty: $(git status --porcelain | wc -l) file(s)"
  echo "config: $CFG  dp=$DP  kappa_B=$KB  seed=$SEED  updates=500"
  echo "archive_sha256: $(cut -d' ' -f1 < "$ARCHIVE.sha256")"
  echo "gpu: $(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null || echo unknown)"
} | tee "$OUT/provenance.txt"

echo "PRE-TASK complete — bring back $OUT/ (incl. the .tar.zst + .sha256)"
echo "and p5pre_console.log. Instance may be released ONLY after that copy."
