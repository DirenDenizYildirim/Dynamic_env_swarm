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

# A failing row must not cost the whole session. The first run of this
# script died on row B (OOM in XLA autotuning) and `set -e` took rows C and
# D down with it — 15 GPU-min bought one number. Rows are independent
# measurements and are now treated as such: failures are recorded and the
# session continues.
bench_row () {  # $1 = label, $2 = config, $3 = extra XLA_FLAGS, $4 = extra env
  local label=$1 cfg=$2 flags=${3:-} extra=${4:-}
  echo "=== row ${label}: pbt --bench --config ${cfg} ${flags:+[XLA_FLAGS: $flags]}"\
       "${extra:+[$extra]} ==="
  local t0=$SECONDS rc=0
  env ${extra} XLA_FLAGS="${flags}" uv run python -m che.train.pbt --bench \
    --config "$cfg" --windows "$WINDOWS" --window-secs 30 \
    --report "$OUT/gate_rows_${label}.md" || rc=$?
  if [ "$rc" -eq 0 ]; then
    echo "row_${label} $((SECONDS - t0))s OK" | tee -a "$OUT/timings.txt"
  else
    echo "row_${label} $((SECONDS - t0))s FAILED(rc=${rc})" | tee -a "$OUT/timings.txt"
  fi
  return "$rc"
}

B_OK=0
bench_row A che/configs/m06_probe.yaml || true
bench_row B che/configs/gate_pop12.yaml && B_OK=1

# --- Row B diagnostics, only if B failed --------------------------------
# The gate config's population obs trajectory is 128 x 256 x 12 agents x
# 9 x 9 x 8 planes x 4 B x 12 members = 11.39 GiB, and ippo.py:268 takes a
# full permuted copy for minibatching, so steady state needs ~22.8 GiB of
# obs alone against a 31.8 GiB card — and JAX preallocates only 75 % (23.9
# GiB) by default. B1/B2 separate "autotuning scratch tipped it over" from
# "this configuration does not fit", which are different findings with
# different remedies. Neither is a fix; both are diagnosis.
if [ "$B_OK" -eq 0 ]; then
  echo "=== row B failed — running memory diagnostics B1/B2 ==="
  bench_row B1 che/configs/gate_pop12.yaml "--xla_gpu_autotune_level=0" || true
  bench_row B2 che/configs/gate_pop12.yaml "--xla_gpu_autotune_level=0" \
    "XLA_PYTHON_CLIENT_MEM_FRACTION=0.95" || true
fi

# Row C only runs if XLA accepts the flags — an unknown flag aborts the
# process, and a silent skip would be worse than a loud one.
DET_OK=0
if XLA_FLAGS="$DET_FLAGS" uv run python -c "import jax; jax.numpy.ones(1).sum()" \
     >/dev/null 2>&1; then
  DET_OK=1
  # Pricing determinism against a config that cannot compile is pointless;
  # fall back to the config row A used so the number still gets measured.
  if [ "$B_OK" -eq 1 ]; then
    bench_row C che/configs/gate_pop12.yaml "$DET_FLAGS" || true
  else
    echo "NOTE: row B did not compile; pricing determinism on m06_probe.yaml" \
      "instead so ruling 1d still gets a number." | tee -a "$OUT/timings.txt"
    bench_row C che/configs/m06_probe.yaml "$DET_FLAGS" || true
  fi
else
  echo "WARNING: XLA rejected '$DET_FLAGS' on this build — rows C and D skipped." \
    | tee -a "$OUT/timings.txt"
fi

# Row D — does determinism actually determinize? Two short single-learner
# runs, same seed, flags on; the metrics must match exactly.
if [ "$DET_OK" = "1" ]; then
  echo "=== row D: determinism verification (2 x 20 updates, flags on) ==="
  # Single-learner run at the severity operating point: unaffected by row
  # B's capacity problem, so this answers ruling 1d regardless.
  for rep in 1 2; do
    XLA_FLAGS="$DET_FLAGS" uv run python -m che.train.ippo \
      --config che/configs/severity_medium.yaml \
      --updates 20 --seed 0 --death-penalty 0.5 \
      --metrics "$OUT/det_rep${rep}.jsonl" || true
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
b1, b2 = rate("B1"), rate("B2")
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
if b is None and (b1 or b2):
    which = "autotune off" if b1 else "autotune off + 95 % mem fraction"
    got = b1 or b2
    print(f"  row B via diagnostics ({which}): {got:>10,.0f} steps/s")
    print("\nVERDICT: UNRESOLVED — the gate config only compiles under altered "
          "memory settings. That is a capacity finding, not a throughput "
          "verdict: a configuration that needs 95 % of the card to compile is "
          "not a safe operating point for a 14-run grid. Human ruling needed "
          "on whether the gate config changes (fallback-ladder rung) or uint8 "
          "obs storage lands first.")
elif b is None:
    print("VERDICT: UNRESOLVED — row B did not compile at all (OOM). The "
          "population obs trajectory is 11.4 GiB and minibatching copies it, "
          "so ~22.8 GiB of obs alone must fit beside params, optimizer state "
          "and activations. This is a CAPACITY finding: the Phase-6/7 "
          "configuration does not fit the card as specified. Not a "
          "throughput verdict, and not something to fix by quietly shrinking "
          "the config — human ruling.")
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
