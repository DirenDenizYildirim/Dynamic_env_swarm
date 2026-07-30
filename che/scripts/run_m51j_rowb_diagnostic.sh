#!/usr/bin/env bash
# M5.1j GPU job — diagnose row B, and settle the requirement drift (~15 GPU-min).
#
# Row B has failed three times and produced no rate:
#   m51d  OOM naming 49.08 GiB (float32 obs; uint8 contingency activated)
#   m51i  bounded OOM after 1112 s retrying a fixed 5.72 GiB allocation
#   m51i  bare rc=137 at the 1800 s backstop — NO diagnostic at all
#
# This job does not attempt row B a fourth time blind. It answers two
# questions first, both of which change how a fourth attempt is read
# (docs/decision_log.md, "Phase-5 delegated rulings, round 2"):
#
# Q1 WHAT IS THE REQUIREMENT? The same byte-identical config priced 24.6872
#    GiB at m51g (fa32113) and 27.5349 GiB at m51i (dbdb15c) — +11.53 % — and
#    `jax.checkpoint` went from saving 2.09 GiB to saving 5 KB. The local CPU
#    bisect cleared the instrument (probe order, candidate-vs-baseline path)
#    and both obvious code suspects (M5.1h dequantize: 0.00 MiB; msg_mode:
#    0.14 MiB at probe scale). What is left is GPU-specific fusion from one of
#    five commits, or a TOOLCHAIN change between two rentals that no
#    provenance file recorded. Sections 1-2 below are that 2x2: same box, same
#    flags, same session, today's code and fa32113's code.
#
# Q2 WHERE DOES ROW B STOP? `pbt.py --bench` is atomic from outside — init,
#    compile, warm-up and the timing windows are one call, so a kill anywhere
#    looks identical. `che/bench/rowb_probe.py` runs the same ladder in stages
#    that report as they go and rewrite their JSON after every stage, with
#    device memory_stats() at each one. A sampler records GPU memory,
#    utilisation and host RSS every 5 s, which is what separates an
#    allocator-retry loop (GPU pinned at the limit, util 0 %) from host swap
#    (RSS at host RAM, util 0 %) from slow-but-progressing (util > 0).
#
# THE 100 k LINE IS NOT RENORMALIZED AND NO EXPERIMENT QUANTITY IS TOUCHED.
# If a rate comes back under the line, that is reported to the Phase-6 entry
# gate. If no rate comes back, the trail says where it stopped and that also
# goes to the entry gate. Row B is not attempted again inside Phase 5.
#
# Run on the GPU box from the repo root, on main (after git pull):
#   bash che/scripts/run_m51j_rowb_diagnostic.sh 2>&1 | tee m51j_console.log
# Bring back che/bench/results/phase5/m51j/ and m51j_console.log.
# Bench only: trains nothing to convergence, produces no checkpoint, so the
# artifact-persistence assert covers metrics + provenance (m51i precedent).
set -uo pipefail   # NOT -e: a failing stage is a measurement here

OUT=che/bench/results/phase5/m51j
CFG=${CFG:-che/configs/gate_pop12.yaml}
OLD_REF=${OLD_REF:-fa32113}          # the m51g tree, for the code/toolchain 2x2
WINDOWS=${WINDOWS:-3}
WINDOW_SECS=${WINDOW_SECS:-30}
REPO=$(pwd)
WT=${WT:-/tmp/che_m51g_tree}

# Instrument settings, carried forward from m51i (they are why row B got as
# far as it did): the autotuner allocates scratch to TIME candidate
# algorithms, on top of the working set, and that is what killed the
# original row B during compilation.
BENCH_FLAGS=${BENCH_FLAGS:-"--xla_gpu_autotune_level=0"}
export XLA_PYTHON_CLIENT_MEM_FRACTION=${XLA_PYTHON_CLIENT_MEM_FRACTION:-0.95}

# Timeouts sit ABOVE the longest observed natural failure (1112 s), because a
# guard that fires first replaces a real diagnostic with a return code — the
# m51i lesson. Unlike m51i, a kill now still leaves the stage trail on disk.
PROBE_TIMEOUT=${PROBE_TIMEOUT:-1200}
STAGE_TIMEOUT=${STAGE_TIMEOUT:-1500}

mkdir -p "$OUT"
: > "$OUT/timings.txt"

[ -e che/bench/rowb_probe.py ] || {
  echo "FATAL: not an M5.1j tree — git pull before running this." >&2
  exit 1
}
grep -q "n_envs: 128" "$CFG" || {
  echo "FATAL: $CFG is not at rung 2 (n_envs 128). Refusing to measure a" >&2
  echo "       config that is not the one the ruling applied." >&2
  exit 1
}

# --------------------------------------------------------------- 0. provenance
# The card must be EMPTY before we start. A leftover process from one of the
# three killed attempts holding memory would explain every symptom at once,
# and it is the cheapest hypothesis to eliminate.
{
  echo "run: M5.1j row-B diagnostic + requirement 2x2"
  echo "date_utc: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "git_commit: $(git rev-parse HEAD)"
  echo "git_dirty: $(git status --porcelain | wc -l) file(s)"
  echo "config: $CFG"
  echo "old_ref: $OLD_REF ($(git rev-parse --short "$OLD_REF" 2>/dev/null || echo MISSING))"
  echo "xla_flags: $BENCH_FLAGS"
  echo "mem_fraction: $XLA_PYTHON_CLIENT_MEM_FRACTION"
  echo "gpu: $(nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader 2>/dev/null || echo unknown)"
  echo "cuda_smi: $(nvidia-smi --query-gpu=vbios_version --format=csv,noheader 2>/dev/null | head -1)"
  echo "nvcc: $(nvcc --version 2>/dev/null | tail -1 || echo absent)"
  echo "host_ram_gib: $(free -g 2>/dev/null | awk '/^Mem:/{print $2" total, "$7" available"}')"
  echo "nproc: $(nproc 2>/dev/null || echo unknown)"
  echo "compute_apps_before: $(nvidia-smi --query-compute-apps=pid,used_memory --format=csv,noheader 2>/dev/null | paste -sd';' || echo none)"
} | tee "$OUT/provenance.txt"

APPS=$(nvidia-smi --query-compute-apps=pid,used_memory --format=csv,noheader 2>/dev/null | wc -l)
if [ "${APPS:-0}" -gt 0 ]; then
  echo "WARNING: the GPU is not idle — $APPS compute app(s) hold memory." | tee -a "$OUT/provenance.txt"
  echo "         Every row below is measured against a card that is already" | tee -a "$OUT/provenance.txt"
  echo "         partly occupied. Kill them and re-run, or read with care." | tee -a "$OUT/provenance.txt"
fi

# 5 s sampler: the three failure modes look different here and nowhere else.
SAMPLE="$OUT/sampler.csv"
echo "elapsed_s,gpu_mem_used_mib,gpu_util_pct,top_rss_kib,host_avail_mib" > "$SAMPLE"
(
  t0=$SECONDS
  while true; do
    gpu=$(nvidia-smi --query-gpu=memory.used,utilization.gpu --format=csv,noheader,nounits 2>/dev/null | tr -d ' ')
    rss=$(ps -eo rss --sort=-rss --no-headers 2>/dev/null | head -1 | tr -d ' ')
    avail=$(free -m 2>/dev/null | awk '/^Mem:/{print $7}')
    echo "$((SECONDS - t0)),${gpu:-,},${rss:-},${avail:-}" >> "$SAMPLE"
    sleep 5
  done
) &
SAMPLER_PID=$!
trap 'kill $SAMPLER_PID 2>/dev/null; git worktree remove --force "$WT" 2>/dev/null' EXIT

stage () {  # $1 = label, $2 = timeout, rest = command
  local label=$1 tmo=$2; shift 2
  local rc=0 t0=$SECONDS
  echo ""
  echo "=== $label ==="
  timeout --signal=KILL "$tmo" "$@" || rc=$?
  local dt=$((SECONDS - t0))
  if [ "$rc" -eq 0 ]; then
    echo "$label ${dt}s OK" | tee -a "$OUT/timings.txt"
  elif [ "$rc" -eq 137 ]; then
    echo "$label ${dt}s KILLED at ${tmo}s guard — read the stage trail and" \
      "the sampler; a natural OOM surfaces its own error near 1100 s" \
      | tee -a "$OUT/timings.txt"
  else
    echo "$label ${dt}s FAILED(rc=$rc)" | tee -a "$OUT/timings.txt"
  fi
  return "$rc"
}

# ------------------------------------------- 1. requirement, TODAY's code
stage "requirement HEAD ($(git rev-parse --short HEAD))" "$PROBE_TIMEOUT" \
  env XLA_FLAGS="$BENCH_FLAGS" uv run python -m che.bench.memprobe \
  --config "$CFG" --only baseline,remat \
  --out-json "$OUT/requirement_head.json" | tee "$OUT/requirement_head.txt"

# ------------------------------------- 2. requirement, m51g's code, same box
# sys.path is prepended explicitly and the resolved module path is ASSERTED,
# so a silent fall-back to today's code cannot happen: the run dies instead.
if git rev-parse "$OLD_REF" >/dev/null 2>&1; then
  git worktree add --detach --force "$WT" "$OLD_REF" >/dev/null 2>&1 || true
  if [ -e "$WT/che/bench/memprobe.py" ]; then
    stage "requirement $OLD_REF (old code, today's toolchain)" "$PROBE_TIMEOUT" \
      env XLA_FLAGS="$BENCH_FLAGS" uv run python -c "
import sys, runpy
sys.path.insert(0, '$WT')
import che.bench.memprobe as m
assert m.__file__.startswith('$WT'), ('resolved today\'s code, not $OLD_REF: ' + m.__file__)
print('[2x2] probing with', m.__file__, flush=True)
sys.argv = ['memprobe', '--config', '$REPO/$CFG', '--only', 'baseline,remat',
            '--out-json', '$REPO/$OUT/requirement_${OLD_REF}.json']
runpy.run_module('che.bench.memprobe', run_name='__main__')
" | tee "$OUT/requirement_${OLD_REF}.txt"
  else
    echo "SKIP 2x2: $OLD_REF worktree unavailable" | tee -a "$OUT/timings.txt"
  fi
fi

# ------------------------------------------------- 3. where does row B stop?
# Preallocated, exactly as the gate would run. --stage one is the decisive
# depth: it allocates the population, compiles, and executes ONE K_pbt chunk.
ONE_OK=0
stage "rowb --stage one (preallocated)" "$STAGE_TIMEOUT" \
  env XLA_FLAGS="$BENCH_FLAGS" uv run python -m che.bench.rowb_probe \
  --config "$CFG" --stage one --out-json "$OUT/rowb_one.json" \
  && ONE_OK=1

# ---------------------------------- 4. if it stopped, localize the allocation
# With preallocation off, an allocation failure surfaces at the point of need
# and names the buffer, instead of being masked by a pre-carved arena. This
# changes fragmentation behaviour, so it is a DIAGNOSTIC and its timings are
# never comparable to a gate number.
if [ "$ONE_OK" -eq 0 ]; then
  stage "rowb --stage one (preallocate=false, diagnostic only)" "$STAGE_TIMEOUT" \
    env XLA_FLAGS="$BENCH_FLAGS" XLA_PYTHON_CLIENT_PREALLOCATE=false \
    uv run python -m che.bench.rowb_probe \
    --config "$CFG" --stage one --out-json "$OUT/rowb_one_noprealloc.json" || true
fi

# --------------------------------------------- 5. the gate number, if earned
WIN_OK=0
if [ "$ONE_OK" -eq 1 ]; then
  stage "rowb --stage windows (THE GATE)" "$STAGE_TIMEOUT" \
    env XLA_FLAGS="$BENCH_FLAGS" uv run python -m che.bench.rowb_probe \
    --config "$CFG" --stage windows --windows "$WINDOWS" \
    --window-secs "$WINDOW_SECS" --out-json "$OUT/rowb_windows.json" \
    && WIN_OK=1
  if [ "$WIN_OK" -eq 1 ]; then
    # Ruling 1d: determinism pricing, which never got a number at this
    # config. Row B already runs with autotuning off, so this isolates the
    # deterministic-ops flag rather than confounding it with the autotuner.
    stage "rowb --stage windows (deterministic flags, ruling 1d)" "$STAGE_TIMEOUT" \
      env XLA_FLAGS="--xla_gpu_deterministic_ops=true $BENCH_FLAGS" \
      uv run python -m che.bench.rowb_probe \
      --config "$CFG" --stage windows --windows "$WINDOWS" \
      --window-secs "$WINDOW_SECS" --out-json "$OUT/rowb_windows_det.json" || true
  fi
fi

kill $SAMPLER_PID 2>/dev/null

# --------------------------------------------------------------- 6. verdict
uv run python - "$OUT" "$OLD_REF" <<'PY' | tee "$OUT/verdict.txt"
import json, os, sys

out, old_ref = sys.argv[1], sys.argv[2]
GIB = 2**30


def load(name):
    p = os.path.join(out, name)
    if not os.path.exists(p):
        return None
    try:
        return json.load(open(p))
    except Exception:
        return None


def baseline_gib(rows):
    if not rows:
        return None
    for r in rows:
        if r.get("label") == "baseline" and r.get("ok"):
            return r.get("total_gib")
    return None


def toolchain_of(rows):
    for r in rows or []:
        if r.get("label") == "_toolchain":
            return f"jax {r.get('jax')} / jaxlib {r.get('jaxlib')}"
    return "unrecorded"


head, old = load("requirement_head.json"), load(f"requirement_{old_ref}.json")
h, o = baseline_gib(head), baseline_gib(old)

print("M5.1j — row-B diagnostic and the requirement 2x2\n")
print("Q1  WHAT IS THE REQUIREMENT? (envs 128 / pop 12 / nmb 4 / uint8)")
print(f"  m51g 2026-07-28, fa32113, toolchain unrecorded : 24.6872 GiB")
print(f"  m51i 2026-07-29, dbdb15c, toolchain unrecorded : 27.5349 GiB")
if h is not None:
    print(f"  M5.1j today, HEAD, {toolchain_of(head):32s}: {h:.4f} GiB")
if o is not None:
    print(f"  M5.1j today, {old_ref}, same toolchain{'':13s}: {o:.4f} GiB")

if h is not None and o is not None:
    drift = h - o
    print()
    if abs(drift) < 0.15:
        print(f"  VERDICT Q1: TOOLCHAIN. Old and new code agree today "
              f"({drift:+.4f} GiB), so the five commits between m51g and "
              f"m51i are innocent and the +2.85 GiB came from the box's "
              f"toolchain. The requirement is not a function of the config "
              f"alone across rentals, which is why provenance now records "
              f"jax/jaxlib (decision_log ruling 4).")
    else:
        print(f"  VERDICT Q1: CODE. Today's code needs {drift:+.4f} GiB more "
              f"than {old_ref} on the SAME toolchain, so one of the five "
              f"commits moved activation retention on GPU. The local CPU "
              f"bisect could not see it because CPU fusion is not GPU "
              f"fusion. Next step is a per-commit bisect of those five, "
              f"compile-only, ~2 GPU-min each.")
elif h is not None:
    print("\n  VERDICT Q1: PARTIAL — the 2x2's old-code arm did not run, so "
          "code and toolchain are not separated. Today's number stands on "
          "its own and supersedes the stale 24.69 GiB either way.")
else:
    print("\n  VERDICT Q1: NO NUMBER — even the compile-only probe failed. "
          "That is itself new: at m51i it succeeded on this card.")

print("\nQ2  WHERE DOES ROW B STOP?")
for name, label in (("rowb_one.json", "stage one, preallocated"),
                    ("rowb_one_noprealloc.json", "stage one, preallocate=false"),
                    ("rowb_windows.json", "stage windows (THE GATE)"),
                    ("rowb_windows_det.json", "stage windows, deterministic")):
    rows = load(name)
    if rows is None:
        continue
    reached = [r["stage"] for r in rows if r.get("ok")]
    failed = [r for r in rows if r.get("ok") is False]
    print(f"  {label:32s} reached: {' -> '.join(reached) or 'nothing'}")
    for r in rows:
        if r.get("stage") == "compile" and r.get("ok"):
            print(f"{'':36s}compile {r['seconds']:.0f} s, "
                  f"temp {r['temp_gib']:.2f} GiB")
        if r.get("stage") == "one" and r.get("ok"):
            print(f"{'':36s}one chunk {r['seconds']:.1f} s, "
                  f"{r['steps_per_s']:,.0f} steps/s (cold)")
        if r.get("stage") == "windows" and r.get("ok"):
            print(f"{'':36s}median {r['median']:,} steps/s (IQR {r['iqr']:,}), "
                  f"peak {(r.get('peak_bytes') or 0) / GIB:.2f} GiB")
    if failed:
        f = failed[-1]
        mem = f.get("memory") or {}
        print(f"{'':36s}FAILED at {f['stage']} after {f['seconds']:.0f} s")
        if mem:
            print(f"{'':36s}at failure: in-use "
                  f"{mem.get('bytes_in_use', 0) / GIB:.2f} GiB, limit "
                  f"{mem.get('bytes_limit', 0) / GIB:.2f} GiB, largest free "
                  f"{mem.get('largest_free_block_bytes', 0) / GIB:.2f} GiB")
        print(f"{'':36s}{f.get('error', '')[:300]}")

gate = load("rowb_windows.json")
rate = None
for r in gate or []:
    if r.get("stage") == "windows" and r.get("ok"):
        rate = r.get("median")
print()
if rate is None:
    print("GATE: still no rate. The trail above says how deep it got and the")
    print("sampler says what the process was doing — which is the whole point")
    print("of this job. This goes to the PHASE 6 ENTRY GATE, not to a fourth")
    print("blind attempt. Row B is not re-run inside Phase 5.")
elif rate >= 100_000:
    print(f"GATE: PASS — {rate:,.0f} >= 100k at fallback-ladder rung 2.")
    print("Budget: envs/member halved, so Phase-6/7 runs need 1000 updates")
    print("rather than 500 to preserve planned experiment steps; total steps")
    print("are unchanged, so cost tracks steps/s alone.")
else:
    print(f"GATE: BELOW THE LINE — {rate:,.0f} < 100k at rung 2. The line is")
    print("NOT renormalized. Rung 2 is the last rung that moves no calibrated")
    print("quantity, so this is a Phase-6 entry-gate decision (scope or")
    print("hardware) and it is reported here, not resolved here.")

det = load("rowb_windows_det.json")
d_rate = None
for r in det or []:
    if r.get("stage") == "windows" and r.get("ok"):
        d_rate = r.get("median")
if rate and d_rate:
    pct = 100 * (1 - d_rate / rate)
    print(f"\nDETERMINISM (ruling 1d): {d_rate:,.0f} steps/s, costs {pct:.1f} % — "
          + ("under the 10 % bar; headline runs MAY go deterministic, human call."
             if pct < 10 else "above the 10 % bar; a human call."))
PY

# ----------------------------------------------------- 7. persistence assert
# Bench only — no checkpoint exists to archive, so the assert covers what this
# run does produce (m51i precedent). It fails the run rather than a README.
{
  echo "compute_apps_after: $(nvidia-smi --query-compute-apps=pid,used_memory --format=csv,noheader 2>/dev/null | paste -sd';' || echo none)"
  echo "sampler_rows: $(wc -l < "$SAMPLE")"
} | tee -a "$OUT/provenance.txt"

for f in provenance.txt timings.txt verdict.txt sampler.csv; do
  [ -s "$OUT/$f" ] || {
    echo "FATAL: $OUT/$f missing or empty — do NOT release the instance" >&2
    exit 1
  }
done

echo ""
echo "M5.1j complete — bring back $OUT/ and m51j_console.log."
echo "Bench only: nothing trained to convergence, no checkpoint to archive."
