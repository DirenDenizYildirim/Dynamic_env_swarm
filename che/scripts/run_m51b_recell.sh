#!/usr/bin/env bash
# M5.1b GPU job — re-measure the env-only reference cell with the comms
# kernel ACTUALLY EXECUTING.
#
# Why this exists: the first M5.1 row (2026-07-28, 8,630,698 steps/s) did
# not measure the comms axis. che/bench/throughput.py's keep-alive probe
# was a hand-written list of outputs; M5.0 added obs["links"] and two info
# counters that were not in it, so XLA dead-code-eliminated the entire link
# kernel. Evidence: tensors of shape [n_agents, n_agents] in the optimized
# HLO went 1 -> 189 once the reduction was restored. The row therefore
# re-measured the M4.1 env, which is why it came out 3.1 % *faster* after
# work was added — you cannot get faster by adding work, and that is the
# tell we followed.
#
# The probe now enumerates the obs/info trees instead of naming fields
# (throughput.py::keepalive_probe), and che/tests/test_bench.py asserts the
# comms tensors survive compilation, so this class of silent
# under-measurement cannot recur.
#
# The M5.1 TRAINING row is unaffected and stands: the message path is
# consumed by the network there, so nothing was eliminated.
#
# Run on the GPU box from the repo root, on main (after git pull):
#   bash che/scripts/run_m51b_recell.sh 2>&1 | tee m51b_console.log
# Expected wall time ~3 min (one reference cell, 5 x 30 s windows).
# Bring back che/bench/results/phase5/m51b/ + m51b_console.log.
set -euo pipefail

OUT=che/bench/results/phase5/m51b
mkdir -p "$OUT"

[ -e che/env/comms.py ] || {
  echo "FATAL: not an M5.0+ tree — checkout main before running this." >&2
  exit 1
}

echo "=== bench reference cell, comms kernel verified live ==="
t0=$SECONDS
uv run python -m che.bench.throughput --cell 64,1024,12 \
  > "$OUT/comms_ref_cell_fixed.json"
echo "bench_ref_cell $((SECONDS - t0))s" | tee "$OUT/timings.txt"
cat "$OUT/comms_ref_cell_fixed.json"

uv run python - "$OUT/comms_ref_cell_fixed.json" <<'PY' | tee "$OUT/verdict.txt"
import json, sys
cell = json.load(open(sys.argv[1]))
env_rate = cell["median"]
proj = env_rate / 81.0
print(f"env-only median   : {env_rate:,.0f} steps/s   (IQR {cell['iqr']:,})")
print(f"projection (/81)  : {proj:,.0f} train steps/s")
print(f"vs M4.1 obs v3    : 8,375,048 -> {env_rate:,.0f} "
      f"({100*(env_rate/8375048-1):+.1f} %)")
print(f"vs the DCE'd row  : 8,630,698 -> {env_rate:,.0f} "
      f"({100*(env_rate/8630698-1):+.1f} %)")
print("  NB (corrected 2026-07-28): this delta is NOT the comms cost. The new")
print("  probe also revives the M4.0 masked_frac and M4.4 danger-moment")
print("  channels, which the old probe had been deleting. Attribution is")
print("  run_m51c_probe_decomposition.sh; do not quote this row as a")
print("  comms measurement.")
print()
if proj >= 100_000:
    print("VERDICT: PASS — projection above the 100k line, contingency UNTRIGGERED.")
else:
    print("VERDICT: CONTINGENCY TRIGGERED (pre-registered, standing rule "
          "2026-07-21): uint8 obs storage + in-network normalization, then "
          "re-bench as row 2. Do not renormalize the 100k line.")
PY

{
  echo "run: M5.1b env-only re-measurement (comms kernel live)"
  echo "date_utc: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "git_commit: $(git rev-parse HEAD)"
  echo "git_dirty: $(git status --porcelain | wc -l) file(s)"
  echo "gpu: $(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null || echo unknown)"
} | tee "$OUT/provenance.txt"

echo "M5.1b complete — bring back $OUT/ and m51b_console.log (no checkpoint,"
echo "so no archive: this job trains nothing)."
