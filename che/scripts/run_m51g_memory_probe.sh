#!/usr/bin/env bash
# M5.1g GPU job — price every way of making the gate config fit (~5 GPU-min).
#
# Row B has now failed twice. First at float32 obs storage (11.39 GiB
# trajectory). Then, after M5.1f's uint8 storage cut that tensor to 2.85
# GiB, it failed again wanting 49.08 GiB — with autotuning disabled and at
# a 95 % memory fraction, so it is a capacity number, not an allocator or
# tuning artifact.
#
# Arithmetic says storage was never the elephant at gate scale: backprop
# activations across the population vmap are. Per minibatch each member
# retains ~18.7 KiB of convolution activations for 98,304 agent-rows =
# 1.75 GiB, times 12 members = 21.06 GiB, doubled by the backward pass =
# 42.1 GiB, plus 5.7 GiB of uint8 obs and a 2.85 GiB dequantized minibatch:
# ~50.7 GiB against XLA's reported 49.08. Within 3 %, which is close enough
# to trust the model for picking candidates and not close enough to pick
# one without measuring.
#
# So this job compiles — does not run — each candidate and asks XLA what it
# would need. Compile-only with autotuning off does not allocate the working
# set, and when XLA refuses outright the requirement it names is itself the
# measurement.
#
# The candidates split into two kinds, and the script keeps them labelled:
#   * remat (gradient checkpointing) is ENGINEERING-NEUTRAL — same
#     hyperparameters, same updates, loss verified identical on CPU. It buys
#     memory with compute.
#   * n_minibatches / pop_size / n_envs CHANGE THE EXPERIMENT. Cheaper in
#     compute, but they are scope decisions and belong to the human.
#
# No config is edited here. This produces the table the ruling needs.
#
# Run on the GPU box from the repo root, on main (after git pull):
#   bash che/scripts/run_m51g_memory_probe.sh 2>&1 | tee m51g_console.log
# Bring back che/bench/results/phase5/m51g/ + m51g_console.log.
set -euo pipefail

OUT=che/bench/results/phase5/m51g
mkdir -p "$OUT"

[ -e che/env/comms.py ] || {
  echo "FATAL: not an M5.0+ tree — checkout main before running this." >&2
  exit 1
}

# Autotuning off: it allocates scratch to time candidate algorithms, which
# is precisely what made row B die during *compilation*. We want buffer
# assignment's answer, not the tuner's.
export XLA_FLAGS="--xla_gpu_autotune_level=0"

t0=$SECONDS
uv run python -m che.bench.memprobe \
  --config che/configs/gate_pop12.yaml \
  --out-json "$OUT/memprobe.json" | tee "$OUT/memprobe.txt"
echo "memprobe $((SECONDS - t0))s" | tee "$OUT/timings.txt"

uv run python - "$OUT/memprobe.json" <<'PY' | tee -a "$OUT/memprobe.txt"
import json, sys
rows = json.load(open(sys.argv[1]))
CARD = 31.8  # GiB usable on the RTX 5090
fits = [r for r in rows
        if r["ok"] and r.get("total_gib") is not None and r["total_gib"] < CARD]
print(f"\nAgainst a {CARD} GiB card:")
if not fits:
    print("  NOTHING FITS. The configuration needs a scope decision, not a")
    print("  memory setting — report the table and STOP.")
else:
    neutral = [r for r in fits if r["label"] in ("baseline", "remat")]
    print(f"  fits: {', '.join(r['label'] for r in fits)}")
    if neutral:
        best = min(neutral, key=lambda r: r["total_gib"])
        print(f"  cheapest EXPERIMENT-PRESERVING option that fits: "
              f"{best['label']} at {best['total_gib']:.2f} GiB")
        print("  -> this one needs no scope ruling; it changes compute, not the run.")
    else:
        print("  no experiment-preserving option fits: every candidate that")
        print("  fits alters n_minibatches, pop_size or n_envs. HUMAN RULING")
        print("  REQUIRED — do not pick one to make the gate pass.")
print("\nHeadroom matters as much as fitting: a config that needs ~95 % of the")
print("card is not a safe operating point for a 14-run grid.")
PY

{
  echo "run: M5.1g memory probe (compile-only)"
  echo "date_utc: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "git_commit: $(git rev-parse HEAD)"
  echo "git_dirty: $(git status --porcelain | wc -l) file(s)"
  echo "xla_flags: $XLA_FLAGS"
  echo "gpu: $(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null || echo unknown)"
} | tee "$OUT/provenance.txt"

echo "M5.1g complete — bring back $OUT/ and m51g_console.log (compiles only,"
echo "trains nothing, no checkpoint)."
