#!/usr/bin/env bash
# M5.1 GPU job — comms-axis reference bench row (Phase-5 prompt M5.1).
#
# (a) Re-measure the M0.4 reference bench cell (64^2, 1024, 12) with the
#     comms axis live. The link draw is unconditional (invariant #3: one
#     uniform per ordered pair per step, whatever delta is), so measuring
#     at the config default delta = 0 gives the true mechanism cost — the
#     same logic as M4.1 measuring Coupling B at kappa_B = 0. r_comm only
#     decides how many drawn links survive the range test, not how many
#     uniforms are drawn, so the row is insensitive to M5.4's lock.
# (b) One end-to-end training run (Medium, 500 updates, seed 0, dp 0.5 per
#     D4) with the FULL message path live at delta = 0 — messages emitted,
#     delivered at t+1, aggregated, and replayed by the PPO loss.
#
# Standing rule (decision log, 2026-07-21): if the training projection at
# the Phase-0 env:train ratio (env-only median / 81) lands below 100k
# steps/s, the uint8 obs-storage contingency ACTIVATES — not discussed,
# activated. The M4.1 row left ~3 % of margin (103.4k), and the Phase-5
# prompt expects this row to cross the line: a planned non-event.
#
# THIS SCRIPT CANNOT PRODUCE THE SECOND ROW. If the contingency fires, the
# uint8 obs storage + in-network normalization have to be implemented and
# CPU-tested first; the re-bench is then a separate ~10 min job. The script
# says so loudly at the end rather than leaving the operator to infer it.
#
# Run on the GPU box from the repo root, on main (after git pull):
#   bash che/scripts/run_m51_comms_bench.sh 2>&1 | tee m51_console.log
# Expected wall time ~10 min (bench windows + one ~300 s training run).
# Bring back che/bench/results/phase5/m51/ + m51_console.log.
set -euo pipefail

OUT=che/bench/results/phase5/m51
CFG=che/configs/severity_medium.yaml
DP=0.5                                   # D4
TAG="medium_comms_dp${DP}_s0"
CKPT="$OUT/ckpt_${TAG}"
mkdir -p "$OUT"
: > "$OUT/timings.txt"

# Pre-flight: the persistence rule's archiver must exist before we spend
# GPU minutes (CLAUDE.md, artifact persistence).
tar --zstd -cf /dev/null --files-from /dev/null 2>/dev/null || {
  echo "FATAL: 'tar --zstd' unavailable (needs GNU tar >= 1.31 + zstd)." >&2
  exit 1
}
[ -e che/env/comms.py ] || {
  echo "FATAL: che/env/comms.py missing — this is not an M5.0+ tree." >&2
  echo "Did you leave the box on the pre-task's 0c612b6 checkout?" >&2
  exit 1
}

echo "=== (a) bench reference cell, comms live ==="
t0=$SECONDS
uv run python -m che.bench.throughput --cell 64,1024,12 > "$OUT/comms_ref_cell.json"
echo "bench_ref_cell $((SECONDS - t0))s" | tee -a "$OUT/timings.txt"
cat "$OUT/comms_ref_cell.json"

echo "=== (b) train ${TAG} — full message path, delta = 0 ==="
t0=$SECONDS
uv run python -m che.train.ippo \
  --config "$CFG" \
  --updates 500 \
  --seed 0 \
  --death-penalty "$DP" \
  --ckpt-dir "$CKPT" \
  --metrics "$OUT/${TAG}.jsonl"
train_s=$((SECONDS - t0))
echo "train_${TAG} ${train_s}s" | tee -a "$OUT/timings.txt"

# --- Gate arithmetic, computed here so the verdict is mechanical --------
uv run python - "$OUT/comms_ref_cell.json" "$OUT/${TAG}.jsonl" "$train_s" \
  <<'PY' | tee "$OUT/verdict.txt"
import json, sys
cell = json.load(open(sys.argv[1]))
rows = [json.loads(line) for line in open(sys.argv[2])]
train_s = float(sys.argv[3])
env_rate = cell["median"]
proj = env_rate / 81.0                      # Phase-0 measured env:train ratio
# Measured end-to-end env-steps/s for this run (256 envs x 128 rollout x 500).
e2e = 256 * 128 * 500 / train_s
print(f"env-only median      : {env_rate:,.0f} steps/s")
print(f"projection (/81)     : {proj:,.0f} train steps/s")
print(f"end-to-end training  : {e2e:,.0f} env-steps/s over {train_s:.0f} s")
print(f"M4.1 comparison      : env-only 8,375,048 -> {env_rate:,.0f} "
      f"({100*(env_rate/8375048-1):+.1f} %); training 276 s -> {train_s:.0f} s")
# Comms channel readout — free early evidence for the M5.4 degree band.
tail = [r for r in rows[-50:] if r.get("delivery_rate") == r.get("delivery_rate")]
if tail:
    dr = sum(r["delivery_rate"] for r in tail) / len(tail)
    od = sum(r["mean_out_degree"] for r in tail) / len(tail)
    print(f"delivery rate (last 50 updates): {dr:.4f}   (expect ~1.0 at delta=0)")
    print(f"mean alive out-degree           : {od:.3f}   "
          f"(r_comm = 8.0 plumbing default, 12 agents on 64^2; M5.4 band [2, 5])")
print()
if proj >= 100_000:
    print("VERDICT: PASS — projection above the 100k line, contingency UNTRIGGERED.")
else:
    print("VERDICT: CONTINGENCY TRIGGERED (pre-registered, standing rule "
          "2026-07-21). uint8 obs storage + in-network normalization must be "
          "implemented and CPU-tested, then re-benched as row 2. Do not "
          "renormalize the 100k line; do not treat this as a failure.")
PY

# --- Artifact persistence (CLAUDE.md, human-issued 2026-07-28) ---------
ARCHIVE="$OUT/ckpt_${TAG}.tar.zst"
echo "=== archive ${ARCHIVE} ==="
tar --zstd -cf "$ARCHIVE" -C "$OUT" "ckpt_${TAG}"
sha256sum "$ARCHIVE" | tee "$ARCHIVE.sha256"
[ -s "$ARCHIVE" ] && [ -s "$ARCHIVE.sha256" ] || {
  echo "FATAL: checkpoint archive or sha256 missing — do NOT release the instance" >&2
  exit 1
}
{
  echo "run: M5.1 comms bench row"
  echo "date_utc: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "git_commit: $(git rev-parse HEAD)"
  echo "git_dirty: $(git status --porcelain | wc -l) file(s)"
  echo "config: $CFG  dp=$DP  delta=0 (message path live)  updates=500  seed=0"
  echo "archive_sha256: $(cut -d' ' -f1 < "$ARCHIVE.sha256")"
  echo "gpu: $(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null || echo unknown)"
} | tee "$OUT/provenance.txt"

echo
echo "M5.1 complete — bring back $OUT/ (incl. .tar.zst + .sha256) and"
echo "m51_console.log. Instance may be released ONLY after that copy."
echo "If the verdict says CONTINGENCY TRIGGERED, the second row needs a code"
echo "change first — keep the box only if you want the re-bench in the same"
echo "session; otherwise release it and re-rent for the ~10 min row-2 job."
