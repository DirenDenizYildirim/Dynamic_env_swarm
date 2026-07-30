#!/usr/bin/env bash
# M5.1k GPU job — throughput levers at the gate config (~40 GPU-min).
#
# WHY. M5.1j measured the gate row at 62,084 steps/s, which prices 86e9
# planned steps at 384.8 GPU-hours (~$385 at $1/h) against a $150-215
# budget. Before any experiment quantity is cut, price the levers that cost
# NOTHING scientifically — because a 1.5x throughput win is worth more than
# a seed, and seeds are what M5.1e showed we cannot spare.
#
# The evidence that a lever exists: per-env efficiency is 40.4 steps/s/env
# here (62,084 / 1536) against 51.8 at Phase 0 (159,000 / 3072). Fewer,
# larger batches would say the opposite, so part of the gap is launch
# overhead rather than work — and more concurrent envs should recover it.
#
# EVERY ROW RUNS WITH AUTOTUNING ON. M5.1j: the same code on the same card
# on the same day measures 3,795 steps/s with `--xla_gpu_autotune_level=0`
# and 62,186 with it on, so a rate without its flags is not a measurement.
# The flags are recorded in the provenance and printed in the table.
#
# WHAT IS AND IS NOT FREE — stated per row, never inferred by the reader:
#   * n_envs with n_minibatches scaled to hold MINIBATCH ROWS CONSTANT keeps
#     activation memory flat and changes how many gradient steps an epoch
#     takes. That is an OPTIMIZATION CHANGE, not a free win, and it needs
#     the same human agreement `n_minibatches` needed at M5.1d (where it was
#     rejected as off-ladder for exactly this reason).
#   * pop_size changes the PBT design outright.
# Nothing here is adopted. This prices options for the Phase-6 entry gate.
#
# Comparison metric is COST FOR A FIXED EXPERIMENT, not steps/update:
# every row is priced for the same 196.6e6-step run (the committed
# pop12 x 128 envs x 128 rollout x 1000 updates), so rows with different
# n_envs are compared at equal science rather than equal update counts.
#
# Run on the GPU box from the repo root. It WAITS for M5.3b to finish
# first — a concurrent bench would contend for the card and corrupt both:
#   nohup bash che/scripts/run_m51k_throughput_levers.sh \
#     > /workspace/m51k_console.log 2>&1 &
set -uo pipefail   # NOT -e: a lever that OOMs is a measurement

OUT=che/bench/results/phase5/m51k
CFG=${CFG:-che/configs/gate_pop12.yaml}
WINDOWS=${WINDOWS:-3}
WINDOW_SECS=${WINDOW_SECS:-30}
LEVER_TIMEOUT=${LEVER_TIMEOUT:-2400}
# Reference experiment size: the committed gate config's 1000-update run.
REF_STEPS=${REF_STEPS:-196608000}

export XLA_PYTHON_CLIENT_MEM_FRACTION=${XLA_PYTHON_CLIENT_MEM_FRACTION:-0.95}
# Deliberately EMPTY: autotuning on is the default and is the only setting
# under which this configuration performs. Recorded rather than assumed.
BENCH_FLAGS=${BENCH_FLAGS:-""}

mkdir -p "$OUT"
: > "$OUT/timings.txt"

[ -e che/bench/rowb_probe.py ] || {
  echo "FATAL: not an M5.1j+ tree — git pull before running this." >&2
  exit 1
}

# ------------------------------------------------- 0. wait for the card
echo "=== waiting for M5.3b (or any probe) to release the GPU ==="
waited=0
while pgrep -f "run_m53b_high_utility_gate.sh" >/dev/null 2>&1 \
   || pgrep -f "che.bench.rowb_probe" >/dev/null 2>&1 \
   || pgrep -f "che.train.ippo" >/dev/null 2>&1; do
  sleep 60
  waited=$((waited + 1))
  [ $((waited % 10)) -eq 0 ] && echo "  ... still waiting, ${waited} min"
done
echo "GPU released after ${waited} min of waiting."
sleep 20   # let the last process actually free its arena
nvidia-smi --query-compute-apps=pid,used_memory --format=csv,noheader
echo "(empty above = free)"

# --------------------------------------------------------- 1. the levers
# label|pop|n_envs|n_minibatches|what it changes
LEVERS=${LEVERS:-"
baseline|12|128|4|as committed (M5.1j reference row)
envs256_nmb8|12|256|8|2x envs, minibatch rows HELD CONSTANT (CHANGES optimization: 8 mb/epoch)
envs512_nmb16|12|512|16|4x envs, minibatch rows HELD CONSTANT (CHANGES optimization: 16 mb/epoch)
envs256_nmb4|12|256|4|2x envs AND 2x minibatch rows (may not fit; CHANGES optimization)
nmb16|12|128|16|smaller minibatches only (CHANGES optimization)
pop8|8|128|4|smaller population (CHANGES the PBT design)
"}

echo "$LEVERS" | while IFS='|' read -r label pop envs nmb note; do
  [ -z "${label// }" ] && continue
  echo ""
  echo "=== lever ${label}: pop ${pop}, n_envs ${envs}, nmb ${nmb} ==="
  echo "    ${note}"
  t0=$SECONDS
  rc=0
  timeout --signal=KILL "$LEVER_TIMEOUT" \
    env XLA_FLAGS="$BENCH_FLAGS" uv run python -m che.bench.rowb_probe \
    --config "$CFG" --stage windows --windows "$WINDOWS" \
    --window-secs "$WINDOW_SECS" --pop-size "$pop" --n-envs "$envs" \
    --n-minibatches "$nmb" \
    --out-json "$OUT/lever_${label}.json" || rc=$?
  echo "lever_${label} $((SECONDS - t0))s rc=${rc}" | tee -a "$OUT/timings.txt"
done

# -------------------------------------------------------- 2. the table
uv run python - "$OUT" "$REF_STEPS" <<'PY' | tee "$OUT/levers.md"
import json, os, sys

out, ref_steps = sys.argv[1], int(sys.argv[2])
GIB = 2**30
PRICE = 1.00  # $/h, the PRO 6000 rate the human quoted 2026-07-30

rows = []
for name in sorted(os.listdir(out)):
    if not name.startswith("lever_") or not name.endswith(".json"):
        continue
    label = name[len("lever_"):-len(".json")]
    try:
        trail = json.load(open(os.path.join(out, name)))
    except Exception:
        continue
    prov = next((r for r in trail if r.get("stage") == "provenance"), {})
    win = next((r for r in trail if r.get("stage") == "windows" and r.get("ok")), None)
    fail = [r for r in trail if r.get("ok") is False]
    rows.append({
        "label": label,
        "pop": prov.get("pop_size"), "envs": prov.get("n_envs"),
        "nmb": prov.get("n_minibatches"),
        "rate": win.get("median") if win else None,
        "iqr": win.get("iqr") if win else None,
        "peak": (win.get("peak_bytes") or 0) / GIB if win else None,
        "failed_at": fail[-1]["stage"] if fail else None,
        "error": (fail[-1].get("error", "")[:90] if fail else ""),
    })

print("# M5.1k — throughput levers at the gate config\n")
print("Autotuning ON for every row (M5.1j: the same config measures 3,795 "
      "steps/s with it off). Rows are priced for the SAME experiment — "
      f"{ref_steps / 1e6:.1f}e6 steps, the committed pop12 x 128envs x 128 "
      "rollout x 1000-update run — so different n_envs are compared at "
      "equal science, not equal update counts.\n")
print("| lever | pop | envs | nmb | steps/s | IQR | peak GiB | h/run | $/run | vs baseline |")
print("|---|---|---|---|---|---|---|---|---|---|")
base = next((r for r in rows if r["label"] == "baseline" and r["rate"]), None)
for r in sorted(rows, key=lambda x: -(x["rate"] or 0)):
    if r["rate"]:
        h = ref_steps / r["rate"] / 3600
        rel = f"{r['rate'] / base['rate']:.2f}x" if base else "—"
        print(f"| {r['label']} | {r['pop']} | {r['envs']} | {r['nmb']} | "
              f"{r['rate']:,} | {r['iqr']:,} | {r['peak']:.1f} | {h:.2f} | "
              f"${h * PRICE:.2f} | {rel} |")
    else:
        print(f"| {r['label']} | {r['pop']} | {r['envs']} | {r['nmb']} | "
              f"DID NOT RUN | — | — | — | — | failed at "
              f"{r['failed_at']}: {r['error']} |")

if base:
    print(f"\nBaseline reproduces M5.1j at {base['rate']:,} steps/s "
          f"(M5.1j measured 62,084). A row that does not reproduce it "
          f"invalidates the whole table — the card or the toolchain moved.")
    best = max((r for r in rows if r["rate"]), key=lambda x: x["rate"])
    if best["label"] != "baseline":
        gain = best["rate"] / base["rate"]
        print(f"\nBest lever **{best['label']}** at {gain:.2f}x. Applied to "
              f"the 86e9 planned-step envelope: "
              f"{86e9 / base['rate'] / 3600:.0f} GPU-h -> "
              f"{86e9 / best['rate'] / 3600:.0f} GPU-h "
              f"(${86e9 / base['rate'] / 3600 * PRICE:.0f} -> "
              f"${86e9 / best['rate'] / 3600 * PRICE:.0f} at ${PRICE:.2f}/h).")
        print("\nThat is a PRICE, not a recommendation. Every non-baseline "
              "row changes the optimization or the design, and adopting one "
              "is a Phase-6-entry-gate decision — the same standing that "
              "rejected `n_minibatches` as off-ladder at M5.1d.")
print("\nNOTE: the 86e9 envelope has no decomposition anywhere in the repo. "
      "It is a Phase-0 safety figure, not a bottom-up plan, and pricing a "
      "placeholder is how the $151 line survived three phases. The entry "
      "gate should rebuild it from the actual Phase-6/7 design before any "
      "lever here is adopted to 'fit' it.")
PY

{
  echo "run: M5.1k throughput levers"
  echo "date_utc: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "git_commit: $(git rev-parse HEAD)"
  echo "config: $CFG"
  echo "xla_flags: '${BENCH_FLAGS}' (empty = autotuning ON, the default)"
  echo "mem_fraction: $XLA_PYTHON_CLIENT_MEM_FRACTION"
  echo "windows: $WINDOWS x ${WINDOW_SECS}s   ref_steps: $REF_STEPS"
  echo "gpu: $(nvidia-smi --query-gpu=name,memory.total --format=csv,noheader 2>/dev/null || echo unknown)"
  echo "jax: $(uv run python -c 'import jax, jaxlib; print(jax.__version__, jaxlib.__version__)' 2>/dev/null || echo unknown)"
} | tee "$OUT/provenance.txt"

for f in provenance.txt timings.txt levers.md; do
  [ -s "$OUT/$f" ] || {
    echo "FATAL: $OUT/$f missing or empty — do NOT release the instance" >&2
    exit 1
  }
done

echo ""
echo "M5.1k complete — bring back $OUT/ and m51k_console.log."
