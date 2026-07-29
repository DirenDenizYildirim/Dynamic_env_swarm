#!/usr/bin/env bash
# M5.3 GPU job — utility gate: does the swarm USE messages? (~35 GPU-min)
#
# The denial axis is vacuous if messages carry nothing, so this is the
# milestone that decides whether Phase 5 has an experiment at all.
#
# THREE ARMS, all at Medium, both couplings on, delta = 0, 500 updates,
# 2 seeds. Identical architecture and parameter count throughout — the
# ablation is message CONTENT, never capacity (test_msg_modes.py pins
# that, including that the three arms init to bitwise identical params):
#
#   live      messages as emitted.
#   zeroed    aggregate hard-zeroed at the aggregation point. Note this
#             cuts content while leaving the link graph intact — it is NOT
#             the delta = 1 denial arm, which cuts the graph.
#   shuffled  sender identities permuted within the step (round-2 ruling
#             item 3). Delivery pattern and marginal content distribution
#             are preserved exactly; only who-said-what is destroyed.
#
# The shuffled arm is what makes the verdict interpretable. Without it,
# "live > zeroed" cannot distinguish "the swarm reads sender-specific
# content" from "the swarm just needs to know someone is out there".
#
# PRE-REGISTERED VERDICT LABELS (decision_log.md, round-2 ruling item 3 —
# fixed before the numbers exist, and not to be renegotiated after):
#   live > shuffled            -> sender-specific content used
#   live ~ shuffled > zeroed   -> connectivity / global content only
#   all three indistinguishable-> NULL BRANCH: architecture goes to the
#                                 human; DIAL-style differentiable comms
#                                 is pre-registered as item #1. Do NOT
#                                 iterate the design silently.
#
# Grading uses the M4.4 rule and the M5.1e reproducibility floor: an arm
# difference smaller than ~2x the measured nondeterminism sd (completion
# 0.0145, survival 0.0129) is NOT resolvable at one run per cell, which is
# why there are 2 seeds and why the script prints the floor beside the
# deltas rather than leaving the reader to remember it.
#
# Run on the GPU box from the repo root, on main (after git pull):
#   bash che/scripts/run_m53_utility_gate.sh 2>&1 | tee m53_console.log
# Bring back che/bench/results/phase5/m53/ (incl. every .tar.zst +
# .sha256) and m53_console.log. These checkpoints cannot be regenerated:
# GPU training is not reproducible run-to-run (M5.1e).
set -euo pipefail

OUT=che/bench/results/phase5/m53
CFG=${CFG:-che/configs/severity_medium.yaml}
DP=${DP:-0.5}
UPDATES=${UPDATES:-500}
N_EVAL=${N_EVAL:-512}
SEEDS=${SEEDS:-"0 1"}
MODES=${MODES:-"live zeroed shuffled"}

mkdir -p "$OUT"
: > "$OUT/timings.txt"

[ -e che/tests/test_msg_modes.py ] || {
  echo "FATAL: not an M5.3 tree — git pull before running this." >&2
  exit 1
}
tar --zstd -cf /dev/null --files-from /dev/null 2>/dev/null || {
  echo "FATAL: 'tar --zstd' unavailable (needs GNU tar >= 1.31 + zstd)." >&2
  exit 1
}

for mode in $MODES; do
  for seed in $SEEDS; do
    TAG="${mode}_s${seed}"
    echo "=== arm ${mode}, seed ${seed}: train ${UPDATES} updates ==="
    t0=$SECONDS
    uv run python -m che.train.ippo \
      --config "$CFG" \
      --updates "$UPDATES" \
      --seed "$seed" \
      --death-penalty "$DP" \
      --msg-mode "$mode" \
      --ckpt-dir "$OUT/ckpt_${TAG}" \
      --metrics "$OUT/${TAG}.jsonl"
    echo "train_${TAG} $((SECONDS - t0))s" | tee -a "$OUT/timings.txt"

    # CRN-paired eval: the SAME eval seed across every arm and training
    # seed, so the arms face an identical episode set and the comparison
    # is paired rather than merely averaged.
    uv run python -m che.eval.harness \
      --config "$CFG" \
      --death-penalty "$DP" \
      --msg-mode "$mode" \
      --ckpt-dir "$OUT/ckpt_${TAG}" \
      --n-episodes "$N_EVAL" \
      --seed 0 \
      --out-npz "$OUT/eval_${TAG}.npz" \
      --out-json "$OUT/eval_${TAG}.json"

    # Artifact persistence (CLAUDE.md, human-issued 2026-07-28): the
    # assertion belongs in the job script, not a README.
    tar --zstd -cf "$OUT/ckpt_${TAG}.tar.zst" -C "$OUT" "ckpt_${TAG}"
    sha256sum "$OUT/ckpt_${TAG}.tar.zst" | tee "$OUT/ckpt_${TAG}.tar.zst.sha256"
    [ -s "$OUT/ckpt_${TAG}.tar.zst.sha256" ] || {
      echo "FATAL: archive missing for ${TAG} — do NOT release the instance" >&2
      exit 1
    }
  done
done

uv run python - "$OUT" "$SEEDS" "$MODES" <<'PY' | tee "$OUT/verdict.txt"
import itertools, json, os, sys
import numpy as np

out, seeds, modes = sys.argv[1], sys.argv[2].split(), sys.argv[3].split()

# M5.1e measured reproducibility floor (nondeterminism alone, same seed).
# Stated as an order of magnitude: n = 4 gives an sd with 3 dof.
FLOOR = {"completion": 0.0145, "survival_rate": 0.0129}
KEYS = ("completion", "survival_rate", "episode_return")


def load(mode, seed):
    p = os.path.join(out, f"eval_{mode}_s{seed}.npz")
    return {k: np.asarray(v) for k, v in np.load(p).items()} if os.path.exists(p) else None


per = {(m, s): load(m, s) for m in modes for s in seeds}
missing = [k for k, v in per.items() if v is None]
if missing:
    print(f"INCOMPLETE — missing evals: {missing}\nNo verdict.")
    raise SystemExit(0)

print("M5.3 utility gate — Medium, both couplings, delta = 0, "
      f"{len(seeds)} seeds, CRN-paired eval episodes\n")
print(f"{'arm':10s} " + "  ".join(f"{k:>16s}" for k in KEYS))
means = {}
for m in modes:
    row = {}
    for k in KEYS:
        vals = [per[(m, s)][k].mean() for s in seeds]
        row[k] = (float(np.mean(vals)), float(np.std(vals, ddof=1)) if len(vals) > 1 else 0.0)
    means[m] = row
    print(f"{m:10s} " + "  ".join(f"{row[k][0]:8.4f}+-{row[k][1]:<6.4f}" for k in KEYS))

print("\nPairwise deltas (positive = first arm better), against the M5.1e floor:")
resolvable = {}
for a, b in itertools.combinations(modes, 2):
    print(f"  {a} - {b}:")
    for k in KEYS:
        d = means[a][k][0] - means[b][k][0]
        # Paired across the shared eval episode set, pooled over seeds.
        paired = np.concatenate([per[(a, s)][k] - per[(b, s)][k] for s in seeds])
        se = paired.std(ddof=1) / np.sqrt(paired.size)
        bar = 2.0 * FLOOR.get(k, float("nan"))
        note = ""
        if k in FLOOR:
            note = ("ABOVE floor" if abs(d) > bar else "within floor")
            resolvable[(a, b, k)] = abs(d) > bar
        print(f"    {k:20s} {d:+8.4f}  (paired SE {se:.4f}"
              + (f", 2x floor {bar:.4f} -> {note}" if note else "") + ")")

# --- Pre-registered labels, applied mechanically -----------------------
def better(a, b):
    """a beats b iff it clears 2x the measured floor on completion or
    survival — the M4.4 strong-grade rule, with the floor measured rather
    than assumed (ruling 3b)."""
    return any(
        means[a][k][0] - means[b][k][0] > 2.0 * FLOOR[k] for k in FLOOR
    )


print("\n" + "=" * 68)
if set(modes) >= {"live", "zeroed", "shuffled"}:
    if better("live", "shuffled"):
        print("VERDICT: SENDER-SPECIFIC CONTENT USED — live > shuffled.")
        print("The swarm reads who said what, not merely that someone did.")
        print("Comms is load-bearing; proceed to M5.4.")
    elif better("live", "zeroed") or better("shuffled", "zeroed"):
        print("VERDICT: CONNECTIVITY / GLOBAL CONTENT ONLY — "
              "live ~ shuffled > zeroed.")
        print("Messages matter but sender identity does not. Comms is still")
        print("load-bearing, and this is a reportable finding about WHAT the")
        print("channel carries — it constrains the Phase-6/7 interpretation.")
    else:
        print("VERDICT: NULL BRANCH — all three arms indistinguishable.")
        print("STOP. Per the phase prompt this goes to a human discussion")
        print("before any lock; DIAL-style differentiable comms is the")
        print("pre-registered item #1. Do NOT iterate the architecture here.")
else:
    print("VERDICT: partial run — the three-arm labels need all three arms.")
print("=" * 68)
print("\nCaveat carried from M5.1e: the floor has 3 dof and is uncertain by")
print("~+-40 %. Differences near the bar are near the bar, not resolved.")
PY

{
  echo "run: M5.3 utility gate (live / zeroed / shuffled)"
  echo "date_utc: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "git_commit: $(git rev-parse HEAD)"
  echo "git_dirty: $(git status --porcelain | wc -l) file(s)"
  echo "config: $CFG   dp: $DP   updates: $UPDATES"
  echo "seeds: $SEEDS   modes: $MODES   eval_episodes: $N_EVAL"
  echo "gpu: $(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null || echo unknown)"
} | tee "$OUT/provenance.txt"

echo "M5.3 complete — bring back $OUT/ (incl. all .tar.zst + .sha256) and"
echo "m53_console.log. These checkpoints cannot be regenerated."
