#!/usr/bin/env bash
# M5.3b GPU job — the utility gate, re-sited at High (~2.2 GPU-hours).
#
# WHY THIS EXISTS. M5.3 ran the three-arm utility gate at Medium and
# returned the null branch. The human discussion the prompt required
# (decision_log.md, "M5.3 null branch settled", 2026-07-30) found that the
# gate was run at the severity where its own mechanism measures zero:
#
#   severity | dSurvival(kappa_B 0 -> 1.0) | verdict     | masked@danger
#   ---------|----------------------------|-------------|--------------
#   low      | +0.0059                    | strong      | 0.0809
#   MEDIUM   | -0.0003                    | WITHIN NOISE| 0.0560
#   high     | -0.0876                    | strong, x2.6| 0.2424     (M4.4 Result 1)
#
# M5.3 asked whether neighbours can supply information the hazard
# withholds, in the cell where our own prior measurement says the hazard
# withholds nothing. This job asks the same question where the hazard
# demonstrably takes 8.8 points of survival.
#
# NOT BAND-SHOPPING (M4.3 precedent, as institutionalized for R_comm by the
# Q5 ruling): no threshold, label or grading rule moves. Adding a severity
# is covering the range. MEDIUM'S NULL STANDS AS REPORTED, is not
# superseded, and both cells are reported together whatever this returns.
#
# THREE THINGS FIXED BEFORE ANY NUMBER EXISTS:
#
# 1. THE FLOOR IS MEASURED HERE, FIRST, AND THE VERDICT READS IT.
#    M5.3's script hardcoded the M5.1e floor, which is Medium-specific AND
#    card-specific; M4.4's sigma_seed at High (0.0227/0.0295) is 2-4x
#    Medium's (0.0107/0.0072). So section 1 runs 4 identical High runs on
#    THIS card and section 4 grades against that file. A bar transcribed
#    from another severity on another card is exactly the stale-number
#    defect M5.1j caught.
#
# 2. THREE SEEDS, not two (M4.4 precedent: a third seed where variance is
#    large).
#
# 3. TWO CELLS, because at High the swarm loses agents, so the comms graph
#    is sparser exactly where the need is greatest — High raises demand and
#    cuts supply at once.
#      CELL A (verdict)     R_comm = 8  — one change from M5.3, attributable
#      CELL B (sensitivity) R_comm = 16 — separates "no content is useful"
#                                         from "no one was in range to hear"
#
# PRE-REGISTERED LABELS (decision_log.md; fixed now, not renegotiated after):
#   A separates            -> comms load-bearing where perception fails;
#                             Remark 2 confirmed at swarm scale; go to M5.4
#   A null, B separates    -> the constraint is CONNECTIVITY, not content or
#                             regime; R_comm is load-bearing and M5.4 must
#                             lock it where the channel is usable
#   A and B both null      -> regime- and connectivity-independent across the
#                             tested range; the reading returns to Remark
#                             2'(i) (redundancy substitutes for comms, as
#                             M5.2's coverage arm measured). Human then
#                             chooses: reportable negative, or DIAL — with
#                             two cells of evidence instead of one.
#
# Run on the GPU box from the repo root, on main (after git pull):
#   bash che/scripts/run_m53b_high_utility_gate.sh 2>&1 | tee m53b_console.log
# Bring back che/bench/results/phase5/m53b/ (incl. every .tar.zst + .sha256)
# and m53b_console.log. These checkpoints cannot be regenerated: GPU
# training is not reproducible run-to-run (M5.1e).
set -euo pipefail

OUT=che/bench/results/phase5/m53b
CFG=${CFG:-che/configs/severity_high.yaml}
DP=${DP:-0.5}
UPDATES=${UPDATES:-500}
N_EVAL=${N_EVAL:-512}
SEEDS=${SEEDS:-"0 1 2"}
MODES=${MODES:-"live zeroed shuffled"}
FLOOR_REPS=${FLOOR_REPS:-4}
FLOOR_SEED=${FLOOR_SEED:-0}
R_A=${R_A:-8}      # cell A: the M5.3-matched range
R_B=${R_B:-16}     # cell B: the connectivity sensitivity range

mkdir -p "$OUT"
: > "$OUT/timings.txt"

[ -e che/bench/rowb_probe.py ] || {
  echo "FATAL: not an M5.1j+ tree — git pull before running this." >&2
  exit 1
}
uv run python -m che.train.ippo --help 2>/dev/null | grep -q -- "--r-comm" || {
  echo "FATAL: this tree has no --r-comm override; cell B cannot run." >&2
  exit 1
}
tar --zstd -cf /dev/null --files-from /dev/null 2>/dev/null || {
  echo "FATAL: 'tar --zstd' unavailable (needs GNU tar >= 1.31 + zstd)." >&2
  exit 1
}

# One trained cell + its CRN-paired eval + its archive.
#   $1 tag  $2 seed  $3 msg_mode  $4 r_comm
train_eval () {
  local tag=$1 seed=$2 mode=$3 rcomm=$4 t0=$SECONDS
  echo ""
  echo "=== ${tag}: train ${UPDATES} updates (High, mode=${mode}, R=${rcomm}) ==="
  uv run python -m che.train.ippo \
    --config "$CFG" \
    --updates "$UPDATES" \
    --seed "$seed" \
    --death-penalty "$DP" \
    --msg-mode "$mode" \
    --r-comm "$rcomm" \
    --ckpt-dir "$OUT/ckpt_${tag}" \
    --metrics "$OUT/${tag}.jsonl"
  echo "train_${tag} $((SECONDS - t0))s" | tee -a "$OUT/timings.txt"

  # CRN-paired: the SAME eval seed everywhere, so every arm and every cell
  # faces an identical episode set and comparisons are paired, not averaged.
  uv run python -m che.eval.harness \
    --config "$CFG" \
    --death-penalty "$DP" \
    --msg-mode "$mode" \
    --r-comm "$rcomm" \
    --ckpt-dir "$OUT/ckpt_${tag}" \
    --n-episodes "$N_EVAL" \
    --seed 0 \
    --out-npz "$OUT/eval_${tag}.npz" \
    --out-json "$OUT/eval_${tag}.json"

  tar --zstd -cf "$OUT/ckpt_${tag}.tar.zst" -C "$OUT" "ckpt_${tag}"
  sha256sum "$OUT/ckpt_${tag}.tar.zst" | tee "$OUT/ckpt_${tag}.tar.zst.sha256"
  [ -s "$OUT/ckpt_${tag}.tar.zst.sha256" ] || {
    echo "FATAL: archive missing for ${tag} — do NOT release the instance" >&2
    exit 1
  }
}

# ------------------------------------------- 1. the floor, BEFORE the gate
# Same seed every time: this is nondeterminism alone, not seed spread. It
# runs first so the bar exists before the numbers it will grade.
echo "########## SECTION 1 — High reproducibility floor (${FLOOR_REPS} identical runs)"
for rep in $(seq 1 "$FLOOR_REPS"); do
  train_eval "floor_rep${rep}" "$FLOOR_SEED" live "$R_A"
done

uv run python - "$OUT" "$FLOOR_REPS" <<'PY' | tee "$OUT/reproducibility_floor_high.txt"
import json, os, statistics, sys
out, reps = sys.argv[1], int(sys.argv[2])
keys = ("completion", "survival_rate", "episode_return", "deaths_fire",
        "mean_smoke_exposure")
vals = {k: [] for k in keys}
for rep in range(1, reps + 1):
    m = json.load(open(os.path.join(out, f"eval_floor_rep{rep}.json")))["metrics"]
    for k in keys:
        if k in m:
            vals[k].append(m[k]["mean"])

print(f"HIGH reproducibility floor — {reps} identical runs (High, dp 0.5,")
print(f"seed fixed, 500 updates, couplings locked, comms live at delta = 0).")
print("Same seed throughout: nondeterminism alone, NOT seed spread.\n")
print(f"  {'metric':22s} {'mean':>10s} {'sd':>10s} {'range':>10s} {'max|dev|':>10s}")
floor = {}
for k in keys:
    v = vals[k]
    if len(v) < 2:
        continue
    mu, sd = statistics.mean(v), statistics.stdev(v)
    floor[k] = {"mean": mu, "sd": sd, "range": max(v) - min(v),
                "max_abs_dev": max(abs(x - mu) for x in v), "values": v,
                "n": len(v)}
    print(f"  {k:22s} {mu:10.4f} {sd:10.4f} {max(v) - min(v):10.4f} "
          f"{max(abs(x - mu) for x in v):10.4f}")
json.dump(floor, open(os.path.join(out, "reproducibility_floor_high.json"), "w"),
          indent=1)
print("\nThis file is what section 4 grades against. It is NOT the M5.1e")
print("Medium floor, and the two are not interchangeable: M4.4 measured")
print("sigma_seed 2-4x larger at High than at Medium.")
print(f"\nCAVEAT: n = {reps} gives an sd with {reps - 1} dof, itself uncertain by")
print("roughly +/-40 %. An order of magnitude, not a threshold to three")
print("decimals. It describes the NON-DETERMINISTIC regime only.")
PY

# ----------------------------------------------------- 2-3. the two cells
echo ""
echo "########## SECTION 2 — CELL A (verdict): High, R_comm = ${R_A}"
for mode in $MODES; do
  for seed in $SEEDS; do
    train_eval "A_${mode}_s${seed}" "$seed" "$mode" "$R_A"
  done
done

echo ""
echo "########## SECTION 3 — CELL B (sensitivity): High, R_comm = ${R_B}"
for mode in $MODES; do
  for seed in $SEEDS; do
    train_eval "B_${mode}_s${seed}" "$seed" "$mode" "$R_B"
  done
done

# --------------------------------------------------------- 4. the verdict
echo ""
echo "########## SECTION 4 — verdict, graded against the measured High floor"
uv run python - "$OUT" "$SEEDS" "$MODES" "$R_A" "$R_B" <<'PY' | tee "$OUT/verdict.txt"
import itertools, json, os, sys
import numpy as np

out, seeds, modes = sys.argv[1], sys.argv[2].split(), sys.argv[3].split()
r_a, r_b = sys.argv[4], sys.argv[5]
KEYS = ("completion", "survival_rate", "episode_return")

# The bar is READ, not transcribed (the whole point of section 1).
floor_path = os.path.join(out, "reproducibility_floor_high.json")
if not os.path.exists(floor_path):
    print("INCOMPLETE — no measured High floor; refusing to grade against a")
    print("floor from another severity or another card. No verdict.")
    raise SystemExit(0)
fl = json.load(open(floor_path))
FLOOR = {k: fl[k]["sd"] for k in ("completion", "survival_rate") if k in fl}
print("M5.3b — utility gate re-sited at High (both couplings, delta = 0,")
print(f"{len(seeds)} seeds, CRN-paired eval episodes)\n")
print("Grading bar: 2x the MEASURED High floor, from this run's own "
      "replication study")
for k, v in FLOOR.items():
    print(f"  {k:16s} sd {v:.4f}  ->  bar {2 * v:.4f}")
print(f"  (M5.1e's Medium floor was completion 0.0145 / survival 0.0129 — "
      f"NOT used here)")


def load(cell, mode, seed):
    p = os.path.join(out, f"eval_{cell}_{mode}_s{seed}.npz")
    return {k: np.asarray(v) for k, v in np.load(p).items()} if os.path.exists(p) else None


def analyse(cell, label):
    per = {(m, s): load(cell, m, s) for m in modes for s in seeds}
    if any(v is None for v in per.values()):
        missing = [k for k, v in per.items() if v is None]
        print(f"\n{label}: INCOMPLETE — missing {missing}")
        return None
    print(f"\n{label}")
    print(f"  {'arm':10s} " + "  ".join(f"{k:>16s}" for k in KEYS))
    means = {}
    for m in modes:
        row = {}
        for k in KEYS:
            vals = [per[(m, s)][k].mean() for s in seeds]
            row[k] = (float(np.mean(vals)), float(np.std(vals, ddof=1)))
        means[m] = row
        print(f"  {m:10s} " + "  ".join(
            f"{row[k][0]:8.4f}+-{row[k][1]:<6.4f}" for k in KEYS))
    print("  pairwise (positive = first arm better):")
    for a, b in itertools.combinations(modes, 2):
        parts = []
        for k in KEYS:
            d = means[a][k][0] - means[b][k][0]
            paired = np.concatenate([per[(a, s)][k] - per[(b, s)][k] for s in seeds])
            se = paired.std(ddof=1) / np.sqrt(paired.size)
            note = ""
            if k in FLOOR:
                bar = 2 * FLOOR[k]
                note = f" [{abs(d) / bar:.2f}x bar]"
            parts.append(f"{k} {d:+.4f} (SE {se:.4f}){note}")
        print(f"    {a} - {b}: " + "; ".join(parts))
    # Channel diagnostics: did the knob we changed actually move?
    for m in modes:
        la = sum(per[(m, s)]["links_alive"].sum() for s in seeds)
        aa = sum(per[(m, s)]["alive_agents"].sum() for s in seeds)
        lr = sum(per[(m, s)]["links_in_range"].sum() for s in seeds)
        print(f"    {m:10s} out-degree {la / aa:.3f}  delivery {la / lr:.4f}")
    return means


def separates(means):
    """The M4.4 strong-grade rule, against the floor measured in section 1."""
    if means is None:
        return False
    return any(means["live"][k][0] - means["zeroed"][k][0] > 2 * FLOOR[k]
               for k in FLOOR)


a = analyse("A", f"CELL A (verdict) — High, R_comm = {r_a}")
b = analyse("B", f"CELL B (sensitivity) — High, R_comm = {r_b}")

print("\n" + "=" * 70)
a_sep, b_sep = separates(a), separates(b)
if a_sep:
    print("VERDICT: COMMS IS LOAD-BEARING AT HIGH — live > zeroed at R_comm =",
          r_a)
    if a and any(a["live"][k][0] - a["shuffled"][k][0] > 2 * FLOOR[k]
                 for k in FLOOR):
        print("  ...and live > shuffled: SENDER-SPECIFIC CONTENT is used.")
    else:
        print("  ...but live ~ shuffled: CONNECTIVITY / GLOBAL CONTENT only.")
    print("  Remark 2's prediction confirmed at swarm scale: the channel")
    print("  matters where perception fails. Medium's null is not overturned")
    print("  — it is explained. Proceed to M5.4.")
elif b_sep:
    print("VERDICT: THE CONSTRAINT IS CONNECTIVITY — null at R_comm =", r_a,
          "and separating at R_comm =", r_b)
    print("  Content is usable; there was nobody in range to hear it. R_comm")
    print("  is load-bearing rather than a plumbing default, and M5.4 must")
    print("  lock it where the channel is usable. Reportable finding.")
else:
    print("VERDICT: NULL AT HIGH TOO, AT BOTH RANGES.")
    print("  The null is regime- and connectivity-independent across the")
    print("  tested range. The reading returns to Remark 2'(i): redundancy")
    print("  substitutes for communication, exactly as M5.2's coverage arm")
    print("  measured (J = 1 under total denial with interchangeable agents).")
    print("  STOP — human chooses between a reportable negative and DIAL,")
    print("  now with two cells and two severities of evidence. Do NOT")
    print("  iterate the architecture here.")
print("=" * 70)
print("\nBoth cells are reported together, and M5.3's Medium null stands as")
print("reported either way (decision_log.md, 2026-07-30). The floor above")
print(f"has {fl['completion']['n'] - 1} dof and is uncertain by ~+-40 %:")
print("differences near the bar are near the bar, not resolved.")
PY

{
  echo "run: M5.3b utility gate re-sited at High (2 cells x 3 arms x 3 seeds)"
  echo "date_utc: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "git_commit: $(git rev-parse HEAD)"
  echo "git_dirty: $(git status --porcelain | wc -l) file(s)"
  echo "config: $CFG   dp: $DP   updates: $UPDATES"
  echo "seeds: $SEEDS   modes: $MODES   eval_episodes: $N_EVAL"
  echo "cell A R_comm: $R_A   cell B R_comm: $R_B"
  echo "floor: $FLOOR_REPS identical runs at seed $FLOOR_SEED, R_comm $R_A"
  echo "gpu: $(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null || echo unknown)"
  echo "jax: $(uv run python -c 'import jax, jaxlib; print(jax.__version__, jaxlib.__version__)' 2>/dev/null || echo unknown)"
} | tee "$OUT/provenance.txt"

for f in provenance.txt timings.txt verdict.txt reproducibility_floor_high.json; do
  [ -s "$OUT/$f" ] || {
    echo "FATAL: $OUT/$f missing or empty — do NOT release the instance" >&2
    exit 1
  }
done

echo ""
echo "M5.3b complete — bring back $OUT/ (incl. all .tar.zst + .sha256) and"
echo "m53b_console.log. These checkpoints cannot be regenerated."
