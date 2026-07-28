#!/usr/bin/env bash
# M5.1d GPU job — RE-ANCHOR THE THROUGHPUT GATE (~15 GPU-min).
#
# Human ruling 2026-07-28 (M5.1 STOP, ruling 1b/1c/1d): the env-only ÷81
# projection is retired. The guarded quantity is directly measured
# population-aggregate training throughput at the Phase-6/7 configuration,
# measured with pbt.py --bench — the same instrument that produced the
# Phase-0 159.0 k steps/s row, so no projection sits between measurement
# and gate. Ruling 1c is PRE-COMMITTED and final: if row B lands under
# 100 k, uint8 obs storage + in-network normalization activate in this
# session, mechanically, no further appeal.
#
# Rows:
#   A  m06_probe.yaml — the exact Phase-0 M0.6 config, on today's code.
#      Comparable to 159.0 k, so it prices everything the project has added
#      since Phase 0. CAVEAT: that config carries obs_window 5, superseded
#      by k=9 at M1.2, so row A is "same config, new code", not "the env we
#      run". It is a drift reference, never the gate.
#   B  gate_pop12.yaml — the Phase-6/7 spending configuration (M0.6
#      operating point + every locked stressor + comms live). THE GATE.
#   C  row B again under XLA deterministic flags — prices determinism
#      (ruling 1d).
#   D  determinism VERIFICATION: two short training runs under the flags,
#      metrics compared exactly. Pricing a knob without checking it does
#      what it claims is how the ÷81 projection survived three phases.
#
# Run on the GPU box from the repo root, on main (after git pull):
#   bash che/scripts/run_m51d_gate_reanchor.sh 2>&1 | tee m51d_console.log
# Bring back che/bench/results/phase5/m51d/ + m51d_console.log.
set -euo pipefail

OUT=che/bench/results/phase5/m51d
mkdir -p "$OUT"
: > "$OUT/timings.txt"
WINDOWS=${WINDOWS:-3}
DET_FLAGS="--xla_gpu_deterministic_ops=true --xla_gpu_autotune_level=0"

[ -e che/env/comms.py ] || {
  echo "FATAL: not an M5.0+ tree — checkout main before running this." >&2
  exit 1
}

bench_row () {  # $1 = label, $2 = config, $3 = extra XLA_FLAGS (may be empty)
  local label=$1 cfg=$2 flags=${3:-}
  echo "=== row ${label}: pbt --bench --config ${cfg} ${flags:+[XLA_FLAGS: $flags]} ==="
  local t0=$SECONDS
  XLA_FLAGS="${flags}" uv run python -m che.train.pbt --bench \
    --config "$cfg" --windows "$WINDOWS" --window-secs 30 \
    --report "$OUT/gate_rows_${label}.md"
  echo "row_${label} $((SECONDS - t0))s" | tee -a "$OUT/timings.txt"
}

bench_row A che/configs/m06_probe.yaml
bench_row B che/configs/gate_pop12.yaml

# Row C only runs if XLA accepts the flags — an unknown flag aborts the
# process, and a silent skip would be worse than a loud one.
if XLA_FLAGS="$DET_FLAGS" uv run python -c "import jax; jax.numpy.ones(1).sum()" \
     >/dev/null 2>&1; then
  bench_row C che/configs/gate_pop12.yaml "$DET_FLAGS"
  DET_OK=1
else
  echo "WARNING: XLA rejected '$DET_FLAGS' on this build — rows C and D skipped." \
    | tee -a "$OUT/timings.txt"
  DET_OK=0
fi

# Row D — does determinism actually determinize? Two short single-learner
# runs, same seed, flags on; the metrics must match exactly.
if [ "$DET_OK" = "1" ]; then
  echo "=== row D: determinism verification (2 x 20 updates, flags on) ==="
  for rep in 1 2; do
    XLA_FLAGS="$DET_FLAGS" uv run python -m che.train.ippo \
      --config che/configs/severity_medium.yaml \
      --updates 20 --seed 0 --death-penalty 0.5 \
      --metrics "$OUT/det_rep${rep}.jsonl"
  done
  if diff -q "$OUT/det_rep1.jsonl" "$OUT/det_rep2.jsonl" >/dev/null; then
    echo "DETERMINISM: VERIFIED — two runs produced byte-identical metrics." \
      | tee "$OUT/determinism.txt"
  else
    echo "DETERMINISM: NOT ACHIEVED — runs still differ under the flags." \
      | tee "$OUT/determinism.txt"
    uv run python - "$OUT/det_rep1.jsonl" "$OUT/det_rep2.jsonl" \
      >> "$OUT/determinism.txt" <<'PY'
import json, sys
a = [json.loads(x) for x in open(sys.argv[1])]
b = [json.loads(x) for x in open(sys.argv[2])]
for k in ("mean_return", "survival_rate", "completion", "total_loss"):
    va, vb = a[-1].get(k), b[-1].get(k)
    if va is not None and vb is not None:
        print(f"  {k:15s} {va!r} vs {vb!r}   delta={va - vb:+.3e}")
first = next((i for i, (x, y) in enumerate(zip(a, b)) if x != y), None)
print(f"  first differing update: {first if first is not None else 'none'}")
PY
  fi
fi

# --- Verdict: mechanical, on row B, per ruling 1c ----------------------
uv run python - "$OUT" <<'PY' | tee "$OUT/verdict.txt"
import re, sys, os
out = sys.argv[1]


def rate(label):
    path = os.path.join(out, f"gate_rows_{label}.md")
    if not os.path.exists(path):
        return None
    nums = re.findall(r"([\d,]+)\s*(?:k)?\s*steps/s", open(path).read(), re.I)
    if not nums:
        nums = re.findall(r"\*\*([\d,]+(?:\.\d+)?)\s*k\*\*", open(path).read())
        return float(nums[-1].replace(",", "")) * 1000 if nums else None
    return float(nums[-1].replace(",", ""))


a, b, c = rate("A"), rate("B"), rate("C")
print("Re-anchored gate — population-aggregate training throughput")
print("(pbt.py --bench, pop 12 x 256 envs x rollout 128; the Phase-0 instrument)\n")
if a:
    print(f"  row A  Phase-0 config, today's code : {a:>12,.0f} steps/s "
          f"({100*(a/159000-1):+.1f} % vs the Phase-0 159.0 k)")
if b:
    print(f"  row B  Phase-6/7 config (THE GATE)  : {b:>12,.0f} steps/s")
if c and b:
    print(f"  row C  row B, deterministic flags   : {c:>12,.0f} steps/s "
          f"({100*(c/b-1):+.1f} % — the price of determinism)")
print()
if b is None:
    print("VERDICT: UNRESOLVED — could not parse row B; read the gate_rows_*.md "
          "files by hand before ruling.")
elif b >= 100_000:
    print(f"VERDICT: PASS — {b:,.0f} >= 100k on the re-anchored measurement. "
          "Contingency UNTRIGGERED.")
else:
    print(f"VERDICT: CONTINGENCY TRIGGERED — {b:,.0f} < 100k on the "
          "re-anchored, directly measured number. Per ruling 1c this is "
          "final and mechanical: activate uint8 obs storage + in-network "
          "normalization and re-bench row B in this session. Do not "
          "renormalize the line; do not re-litigate the instrument.")
if c and b and c / b >= 0.90:
    print("\nDETERMINISM: costs <10 % (ruling 3c) — headline runs may go "
          "deterministic; see determinism.txt for whether it actually "
          "determinizes.")
elif c and b:
    print(f"\nDETERMINISM: costs {100*(1-c/b):.1f} % — above the 10 % bar in "
          "ruling 3c; deterministic headline runs are a human call.")
PY

{
  echo "run: M5.1d re-anchored gate + determinism pricing"
  echo "date_utc: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "git_commit: $(git rev-parse HEAD)"
  echo "git_dirty: $(git status --porcelain | wc -l) file(s)"
  echo "windows_per_row: $WINDOWS x 30 s"
  echo "det_flags: $DET_FLAGS"
  echo "gpu: $(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null || echo unknown)"
} | tee "$OUT/provenance.txt"

echo "M5.1d complete — bring back $OUT/ and m51d_console.log."
