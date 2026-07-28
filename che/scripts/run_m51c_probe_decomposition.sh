#!/usr/bin/env bash
# M5.1c GPU job — attribute the env-only throughput drop (~8 GPU-min).
#
# Why this exists. M5.1b re-measured the reference cell at 3,390,689
# steps/s, -59.5 % vs the M4.1 row, and the script labelled that "the comms
# cost". THAT LABEL IS WRONG and this job replaces it with a measurement.
#
# The old keep-alive probe consumed only grid/vec/rew/done + two info keys,
# so XLA deleted *everything else* — not just the M5.0 link kernel but also
# the M4.0 masked_frac channel and the M4.4 danger-moment channel, which
# dilates the whole 64^2 hazard grid and recomputes per-agent masked shares
# every step. Neither of those existed in the probe when the M4.1 row was
# published, so the -59.5 % conflates at least three separate costs.
#
# It matters which consumer you bench for, because XLA deletes whatever the
# consumer does not read:
#   * the IPPO collector reads EP_METRICS + the comms counters -> the M4.4
#     diagnostics are dead code IN TRAINING and cost nothing there;
#   * the eval harness reads nearly all of EVAL_METRICS -> it pays in full.
# Direct evidence that training does not pay: the M5.1 training run measured
# 68,475 env-steps/s against M4.1's 68,598, unchanged, even though the M4.4
# channels landed in between.
#
# The standing rule's 100k line is a TRAINING projection, so the row that
# decides it is `--probe training`. This job measures all four so the human
# can rule on which row is canonical with the decomposition in hand rather
# than in the abstract.
#
# Run on the GPU box from the repo root, on main (after git pull):
#   bash che/scripts/run_m51c_probe_decomposition.sh 2>&1 | tee m51c_console.log
# Bring back che/bench/results/phase5/m51c/ + m51c_console.log.
set -euo pipefail

OUT=che/bench/results/phase5/m51c
mkdir -p "$OUT"
: > "$OUT/timings.txt"

[ -e che/env/comms.py ] || {
  echo "FATAL: not an M5.0+ tree — checkout main before running this." >&2
  exit 1
}

# 3 windows, not 5: the M5.1b IQR was 2,114 on 3.39M (0.06 %), so the
# measurement is far more repeatable than the between-session variation
# that separates these rows anyway. Four rows at 5 windows would cost 12
# GPU-min to buy precision the comparison cannot use.
for mode in legacy comms training all; do
  echo "=== reference cell, probe=${mode} ==="
  t0=$SECONDS
  uv run python -m che.bench.throughput --cell 64,1024,12 \
    --windows 3 --probe "$mode" > "$OUT/cell_${mode}.json"
  echo "cell_${mode} $((SECONDS - t0))s" | tee -a "$OUT/timings.txt"
  cat "$OUT/cell_${mode}.json"
done

uv run python - "$OUT" <<'PY' | tee "$OUT/decomposition.txt"
import json, os, sys
out = sys.argv[1]
r = {m: json.load(open(os.path.join(out, f"cell_{m}.json")))
     for m in ("legacy", "comms", "training", "all")}
med = {m: v["median"] for m, v in r.items()}
M41 = 8_375_048  # obs v3 row, measured under the legacy probe

print("Reference cell 64^2 / 1024 envs / 12 agents, by keep-alive set:\n")
print(f"  {'probe':9s} {'median steps/s':>16s} {'proj (/81)':>12s}  vs legacy")
for m in ("legacy", "comms", "training", "all"):
    rel = 100 * (med[m] / med["legacy"] - 1)
    print(f"  {m:9s} {med[m]:>16,} {med[m]/81:>12,.0f}  {rel:+6.1f} %")

print(f"\n  legacy vs the published M4.1 row ({M41:,}): "
      f"{100*(med['legacy']/M41-1):+.1f} %  <- same probe, so this is "
      f"between-session\n     variation plus any real change since M4.1")
print(f"  comms axis alone (legacy -> comms):      "
      f"{100*(med['comms']/med['legacy']-1):+.1f} %")
print(f"  what TRAINING pays (legacy -> training): "
      f"{100*(med['training']/med['legacy']-1):+.1f} %")
print(f"  what EVAL pays    (legacy -> all):       "
      f"{100*(med['all']/med['legacy']-1):+.1f} %")

proj = med["training"] / 81
print(f"\nStanding-rule arithmetic on the TRAINING row: {proj:,.0f} train steps/s")
if proj >= 100_000:
    print("  -> above the 100k line on the training-faithful measurement.")
else:
    print("  -> below the 100k line on the training-faithful measurement.")
print("\nNOT a verdict. Which row is canonical for the standing rule is a")
print("human ruling (the rule predates the discovery that 'the env cost'")
print("depends on the consumer). The direct end-to-end evidence — 68,475")
print("env-steps/s in M5.1 vs 68,598 in M4.1 — is the other half of it.")
PY

{
  echo "run: M5.1c probe decomposition"
  echo "date_utc: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "git_commit: $(git rev-parse HEAD)"
  echo "git_dirty: $(git status --porcelain | wc -l) file(s)"
  echo "gpu: $(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null || echo unknown)"
} | tee "$OUT/provenance.txt"

echo "M5.1c complete — bring back $OUT/ and m51c_console.log (trains nothing,"
echo "so no checkpoint archive)."
