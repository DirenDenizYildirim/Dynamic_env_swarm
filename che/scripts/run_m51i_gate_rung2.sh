#!/usr/bin/env bash
# M5.1i GPU job — row B, re-benched after fallback-ladder rung 2 (~8 GPU-min).
#
# The gate configuration needed 49.31 GiB against a 31.8 GiB card, and
# nothing experiment-preserving fit: XLA's own rematerialization pass
# reported it could not get below 28.31 GiB (89 % of the card), which is
# also why jax.checkpoint only bought 4 % — the compiler was already
# rematerializing.
#
# Remedy = the pre-agreed fallback ladder (phase0_substrate_prompt.md),
# rung 2 (n_envs tuning), applied for the second time: Phase 0 moved
# 1024 -> 256 envs/member for this same reason, and gate_pop12.yaml now
# carries 256 -> 128. Rungs 1/3/4 are unavailable because they move
# quantities that Phases 2-4 calibrated (grid size, agent count). Full
# reasoning: docs/decision_log.md, "Phase-5 delegated rulings".
#
# The ladder says "re-measure after each rung", and that is the whole
# job here. Two things must come back true, not one:
#   * it COMPILES and runs (the memory probe predicted 24.69 GiB);
#   * the throughput number, which is what the gate actually guards.
#
# The 100k line is NOT renormalized and NOT re-litigated. If row B lands
# under it, that is a finding for the Phase-6 entry gate, not something
# this script resolves.
#
# NOTE ON BUDGET: halving envs/member halves env-steps per update, so
# Phase-6/7 runs at this config need 1000 updates rather than 500 to
# preserve planned experiment steps (the ladder forbids reducing them
# silently). Total cost is unchanged only if steps/s holds — which is
# precisely what row B now measures.
#
# Run on the GPU box from the repo root, on main (after git pull):
#   bash che/scripts/run_m51i_gate_rung2.sh 2>&1 | tee m51i_console.log
# Bring back che/bench/results/phase5/m51i/ + m51i_console.log.
set -euo pipefail

OUT=che/bench/results/phase5/m51i
mkdir -p "$OUT"
: > "$OUT/timings.txt"
WINDOWS=${WINDOWS:-3}

[ -e che/env/e2c2.py ] || {
  echo "FATAL: not an M5.2+ tree — git pull before running this." >&2
  exit 1
}
grep -q "n_envs: 128" che/configs/gate_pop12.yaml || {
  echo "FATAL: gate_pop12.yaml is not at rung 2 (n_envs 128). Refusing to" >&2
  echo "       measure a config that is not the one the ruling applied." >&2
  exit 1
}

# Instrument settings, not experiment settings. Both are forced because
# the first m51i row B ran out of memory after 1112 s: elapsed climbed
# while CPU time stayed flat, the process retrying a fixed 5.72 GiB
# allocation that nothing was ever going to free. It was reported as a
# hang and I agreed too readily; it was in fact a slow, bounded failure
# that raised a proper OOM. The distinction matters for how long the
# guard below waits.
#
#   autotune off   — the autotuner allocates scratch to TIME candidate
#                    algorithms, on top of the working set. That is what
#                    killed the original row B during compilation (m51d
#                    rows B1/B2 worked around it; m51i failed to carry it
#                    forward, which is a script defect, not a finding).
#   mem fraction   — JAX preallocates 75 % of the card by default = 23.85
#                    GiB, which is BELOW the 24.69 GiB this config needs.
#                    0.95 gives 30.2 GiB for a 24.69 GiB requirement.
#
# Autotuning off makes the measurement SLOWER, so the resulting throughput
# is a conservative lower bound — and it is the operative number anyway:
# if Phase-6/7 runs can only execute with the autotuner off, then that is
# the throughput the configuration actually has.
BENCH_FLAGS=${BENCH_FLAGS:-"--xla_gpu_autotune_level=0"}
export XLA_PYTHON_CLIENT_MEM_FRACTION=${XLA_PYTHON_CLIENT_MEM_FRACTION:-0.95}
# Backstop for a genuine hang — deliberately set ABOVE the longest
# observed natural failure, not below it.
#
# The first m51i row B looked hung (elapsed climbing, CPU time flat, a
# ~10 s retry loop on a fixed allocation) and was reported as such. It
# was not: the BFC allocator's retry budget is bounded and it raised a
# real OOM at 1112 s, carrying the allocation size in the message. A
# 900 s guard would have killed it at 900 s and replaced that diagnostic
# with a bare rc=137 — a timeout that fires before the tool's own error
# handling makes the artifact *less* informative, which is the opposite
# of the point.
#
# So: a healthy row finishes in ~3 min (compile with autotune off plus
# WINDOWS x 30 s), a natural failure surfaces its own error around
# ~1100 s, and only something genuinely stuck reaches 1800 s.
ROW_TIMEOUT=${ROW_TIMEOUT:-1800}

bench_row () {  # $1 = label, $2 = config, $3 = extra XLA_FLAGS
  local label=$1 cfg=$2 flags=${3:-$BENCH_FLAGS} rc=0 t0=$SECONDS
  echo "=== row ${label}: pbt --bench --config ${cfg} ${flags:+[$flags]} ==="
  timeout --signal=KILL "$ROW_TIMEOUT" \
    env XLA_FLAGS="${flags}" uv run python -m che.train.pbt --bench \
    --config "$cfg" --windows "$WINDOWS" --window-secs 30 \
    --report "$OUT/gate_rows_${label}.md" || rc=$?
  if [ "$rc" -eq 137 ]; then
    echo "row_${label}: KILLED after ${ROW_TIMEOUT}s — genuinely stuck." \
      | tee -a "$OUT/timings.txt"
    echo "  (a natural OOM surfaces its own error well before this; if" \
      "this fires, the process was not making progress at all)" \
      | tee -a "$OUT/timings.txt"
  fi
  if [ "$rc" -eq 0 ]; then
    echo "row_${label} $((SECONDS - t0))s OK" | tee -a "$OUT/timings.txt"
  else
    echo "row_${label} $((SECONDS - t0))s FAILED(rc=${rc})" | tee -a "$OUT/timings.txt"
  fi
  return "$rc"
}

# Row B: THE GATE, at rung 2.
B_OK=0
bench_row B che/configs/gate_pop12.yaml && B_OK=1

# Row C: determinism pricing (ruling 1d) — never got a number at the gate
# config because row B did not compile. Now it can. Note row B already
# runs with autotuning off, so C-vs-B isolates the deterministic-ops flag
# rather than confounding it with the autotuner.
DET_FLAGS="--xla_gpu_deterministic_ops=true --xla_gpu_autotune_level=0"
if [ "$B_OK" -eq 1 ]; then
  bench_row C che/configs/gate_pop12.yaml "$DET_FLAGS" || true
else
  echo "row C skipped: row B did not run." | tee -a "$OUT/timings.txt"
fi

# If it still does not fit, price the next rung rather than guessing.
if [ "$B_OK" -eq 0 ]; then
  echo "=== row B still failed — pricing the remaining ladder ==="
  XLA_FLAGS="--xla_gpu_autotune_level=0" uv run python -m che.bench.memprobe \
    --config che/configs/gate_pop12.yaml \
    --out-json "$OUT/memprobe_rung2.json" | tee "$OUT/memprobe_rung2.txt" || true
fi

uv run python - "$OUT" <<'PY' | tee "$OUT/verdict.txt"
import os, re, sys
out = sys.argv[1]


def rate(label):
    path = os.path.join(out, f"gate_rows_{label}.md")
    if not os.path.exists(path):
        return None
    text = open(path).read()
    nums = re.findall(r"([\d,]+)\s*steps/s", text, re.I)
    return float(nums[-1].replace(",", "")) if nums else None


b, c = rate("B"), rate("C")
print("Re-anchored gate at fallback-ladder rung 2 (n_envs 128/member)")
print("(pbt.py --bench, pop 12 x 128 envs x rollout 128)\n")
if b:
    print(f"  row B  THE GATE                    : {b:>12,.0f} steps/s")
if c and b:
    print(f"  row C  same, deterministic flags   : {c:>12,.0f} steps/s "
          f"({100 * (c / b - 1):+.1f} %)")
print()
if b is None:
    print("VERDICT: NO NUMBER — row B did not produce a rate.")
    print("Read the memprobe beside this before concluding anything about "
          "the ladder: the probe runs with autotuning off, so a 'fits' "
          "there alongside a failed run is NOT a contradiction — it means "
          "buffer assignment fits and the instrument on top of it did not. "
          "Rung 2 already cut the requirement 49.31 -> ~24.7 GiB, so a "
          "failure here is about how the row is measured, not about "
          "whether the rung worked. Only if the probe ALSO reports no fit "
          "is this a ladder question for the Phase-6 entry gate.")
elif b >= 100_000:
    print(f"VERDICT: PASS — {b:,.0f} >= 100k at the applied rung.")
    print("Budget note: envs/member halved, so Phase-6/7 runs need 1000 "
          "updates rather than 500 to preserve planned experiment steps. "
          "Total steps are unchanged, so cost tracks steps/s alone.")
else:
    print(f"VERDICT: BELOW THE LINE — {b:,.0f} < 100k at the applied rung. "
          "The line is not renormalized. Rung 2 is the last rung that does "
          "not move a calibrated quantity, so this is a Phase-6 entry-gate "
          "decision (scope or hardware), and it is reported, not resolved "
          "here.")
if c and b:
    pct = 100 * (1 - c / b)
    print(f"\nDETERMINISM: costs {pct:.1f} % — "
          + ("under the 10 % bar (ruling 3c), headline runs may go "
             "deterministic." if pct < 10 else
             "above the 10 % bar (ruling 3c); a human call."))
PY

{
  echo "run: M5.1i gate re-bench at fallback-ladder rung 2"
  echo "date_utc: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "git_commit: $(git rev-parse HEAD)"
  echo "git_dirty: $(git status --porcelain | wc -l) file(s)"
  echo "n_envs: $(grep -E '^\s+n_envs:' che/configs/gate_pop12.yaml)"
  echo "windows_per_row: $WINDOWS x 30 s"
  echo "gpu: $(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null || echo unknown)"
} | tee "$OUT/provenance.txt"

echo "M5.1i complete — bring back $OUT/ and m51i_console.log (bench only,"
echo "trains nothing to convergence, no checkpoint)."
