#!/usr/bin/env bash
# M5.5 GPU job — Phase-5 acceptance grid, RESCOPED (~1.3 GPU-hours).
#
# THIS RUN IS CERTIFICATION, NOT EXPLORATION. The M5.3 closure ruling
# (2026-07-30, docs/decision_log.md) certified the comms axis as a
# reportable negative and locked delta = 1.0 by convention with R_comm = 16
# on the geometric observable alone. The expected verdict here is INERT,
# and that expectation is the point: a certified negative needs the
# symmetric falsifier run, not skipped because we know the answer.
#
# RESCOPE vs the phase-5 prompt's "3 severities x delta x 2 seeds":
#   Medium x delta in {0, 1.0} x 4 SEEDS.
# Medium is comms' best-chance cell (Remark 2), and the M5.3b severity
# comparison is why the High cells are gone: the measured High floor is
# 3.6-4.8x the Medium one, so High resolves only ~11-point effects where
# Medium resolves ~3-point ones. Three severities at 2 seeds would have
# spent budget producing uninformative High nulls.
#
# THE MESSAGE PATH IS LIVE IN BOTH ARMS. The ablation is DENIAL (delta),
# never architecture — msg_mode stays "live" throughout, so this grid is
# not a second copy of M5.3.
#
# PRE-REGISTERED FALSIFIER (M4.4 pattern, restated by the closure ruling).
# The denial element is INERT at swarm scale iff ALL THREE hold:
#   (i)   Delta-completion AND Delta-survival within the MEASURED
#         reproducibility floor, with its regime named;
#   (ii)  the delivery-rate difference confirms the knob actually moved;
#   (iii) no cross-arm difference in danger-moment outcomes (fire deaths
#         per danger agent-step).
# All three -> reportable negative, certified. Any failing -> the element
# is NOT inert and that is a finding, not a nuisance.
#
# FLOOR PROVENANCE, and a flagged interaction between two rulings: the
# closure ruling says "graded against the M5.1e reproducibility floor",
# while the same day's hardware-split ruling requires a CARD-SPECIFIC
# floor -- and M5.1e was measured on a 5090. Cheapest reconciliation,
# adopted here and reported, not hidden: section 1 re-measures the Medium
# floor ON THIS CARD (4 identical runs, ~20 GPU-min) and the verdict
# grades against that, printing M5.1e's figures beside it. If the two
# agree, nothing turned on the choice; if they differ, the reader sees it.
#
# Run on the GPU box from the repo root, on main (after git pull):
#   bash che/scripts/run_m55_acceptance.sh 2>&1 | tee m55_console.log
# Bring back che/bench/results/phase5/m55/ (incl. every .tar.zst + .sha256)
# and m55_console.log. These checkpoints cannot be regenerated (M5.1e).
set -euo pipefail

OUT=che/bench/results/phase5/m55
CFG=${CFG:-che/configs/severity_medium.yaml}
DP=${DP:-0.5}
UPDATES=${UPDATES:-500}
N_EVAL=${N_EVAL:-512}
SEEDS=${SEEDS:-"0 1 2 3"}
DELTAS=${DELTAS:-"0.0 1.0"}
R_COMM=${R_COMM:-16}          # LOCKED, comms_lock.md 2026-07-30
FLOOR_REPS=${FLOOR_REPS:-4}
FLOOR_SEED=${FLOOR_SEED:-0}
RENDER_EPS=${RENDER_EPS:-"0 1 2 3 4 5"}

mkdir -p "$OUT"
: > "$OUT/timings.txt"

uv run python -m che.train.ippo --help 2>/dev/null | grep -q -- "--delta" || {
  echo "FATAL: this tree has no --delta override; the grid cannot run." >&2
  exit 1
}
tar --zstd -cf /dev/null --files-from /dev/null 2>/dev/null || {
  echo "FATAL: 'tar --zstd' unavailable (needs GNU tar >= 1.31 + zstd)." >&2
  exit 1
}

# $1 tag  $2 seed  $3 delta
train_eval () {
  local tag=$1 seed=$2 delta=$3 t0=$SECONDS
  echo ""
  echo "=== ${tag}: train ${UPDATES} updates (Medium, delta=${delta}, R=${R_COMM}) ==="
  uv run python -m che.train.ippo \
    --config "$CFG" --updates "$UPDATES" --seed "$seed" \
    --death-penalty "$DP" --delta "$delta" --r-comm "$R_COMM" \
    --ckpt-dir "$OUT/ckpt_${tag}" --metrics "$OUT/${tag}.jsonl"
  echo "train_${tag} $((SECONDS - t0))s" | tee -a "$OUT/timings.txt"

  # CRN-paired: same eval seed everywhere, so both arms face an identical
  # episode set and the comparison is paired rather than merely averaged.
  uv run python -m che.eval.harness \
    --config "$CFG" --death-penalty "$DP" --delta "$delta" --r-comm "$R_COMM" \
    --ckpt-dir "$OUT/ckpt_${tag}" --n-episodes "$N_EVAL" --seed 0 \
    --out-npz "$OUT/eval_${tag}.npz" --out-json "$OUT/eval_${tag}.json"

  tar --zstd -cf "$OUT/ckpt_${tag}.tar.zst" -C "$OUT" "ckpt_${tag}"
  sha256sum "$OUT/ckpt_${tag}.tar.zst" | tee "$OUT/ckpt_${tag}.tar.zst.sha256"
  [ -s "$OUT/ckpt_${tag}.tar.zst.sha256" ] || {
    echo "FATAL: archive missing for ${tag} — do NOT release the instance" >&2
    exit 1
  }
}

# ------------------------------------- 1. the floor, on THIS card, first
echo "########## SECTION 1 — Medium reproducibility floor, this card"
for rep in $(seq 1 "$FLOOR_REPS"); do
  train_eval "floor_rep${rep}" "$FLOOR_SEED" 0.0
done

uv run python - "$OUT" "$FLOOR_REPS" <<'PY' | tee "$OUT/reproducibility_floor_medium.txt"
import json, os, statistics, sys
out, reps = sys.argv[1], int(sys.argv[2])
keys = ("completion", "survival_rate", "episode_return", "deaths_fire")
vals = {k: [] for k in keys}
for rep in range(1, reps + 1):
    m = json.load(open(os.path.join(out, f"eval_floor_rep{rep}.json")))["metrics"]
    for k in keys:
        if k in m:
            vals[k].append(m[k]["mean"])
print(f"MEDIUM reproducibility floor — {reps} identical runs, same seed.")
print("Nondeterminism alone, NOT seed spread. Measured on the card this")
print("grid runs on (hardware-split ruling); M5.1e's 5090 figures are")
print("printed beside it in the verdict.\n")
print(f"  {'metric':20s} {'mean':>10s} {'sd':>10s} {'range':>10s}")
floor = {}
for k in keys:
    v = vals[k]
    if len(v) < 2:
        continue
    mu, sd = statistics.mean(v), statistics.stdev(v)
    floor[k] = {"mean": mu, "sd": sd, "range": max(v) - min(v), "values": v,
                "n": len(v)}
    print(f"  {k:20s} {mu:10.4f} {sd:10.4f} {max(v) - min(v):10.4f}")
json.dump(floor, open(os.path.join(out, "reproducibility_floor_medium.json"), "w"),
          indent=1)
print(f"\nCAVEAT: n = {reps} gives an sd with {reps - 1} dof, uncertain by ~+/-40 %.")
PY

# ------------------------------------------------------ 2. the delta grid
echo ""
echo "########## SECTION 2 — grid: Medium x delta in {${DELTAS}} x seeds {${SEEDS}}"
for delta in $DELTAS; do
  for seed in $SEEDS; do
    train_eval "d${delta}_s${seed}" "$seed" "$delta"
  done
done

# ------------------- 3. message-usage diagnostic on the delta = 0 policies
# Free re-check of M5.3 at the locked R_comm: zero the channel at EVAL time
# on policies TRAINED with it live. Distinct from M5.3's trained-arm
# comparison, and distinct from delta = 1 (which cuts the graph, not the
# content).
echo ""
echo "########## SECTION 3 — message-usage diagnostic (--mute on delta=0 policies)"
for seed in $SEEDS; do
  uv run python -m che.eval.harness \
    --config "$CFG" --death-penalty "$DP" --delta 0.0 --r-comm "$R_COMM" \
    --ckpt-dir "$OUT/ckpt_d0.0_s${seed}" --n-episodes "$N_EVAL" --seed 0 --mute \
    --out-npz "$OUT/eval_muted_s${seed}.npz" \
    --out-json "$OUT/eval_muted_s${seed}.json"
done

# ------------------------------------------------- 4. matched render audit
# Same episode seeds across both arms, seed-0 policies. Watch item from the
# closure ruling: branch-loitering / information-buying behaviour.
echo ""
echo "########## SECTION 4 — matched renders (watch: branch-loitering)"
mkdir -p "$OUT/renders"
for delta in $DELTAS; do
  for ep in $RENDER_EPS; do
    uv run python -m che.scripts.render_episode \
      --config "$CFG" --death-penalty "$DP" --delta "$delta" --r-comm "$R_COMM" \
      --ckpt-dir "$OUT/ckpt_d${delta}_s0" --seed "$ep" \
      --out "$OUT/renders/d${delta}_ep${ep}.gif" \
      --tag "delta=${delta} ep${ep}" || echo "  (render d${delta} ep${ep} failed)"
  done
done

# --------------------------------------------------- 5. falsifier verdict
echo ""
echo "########## SECTION 5 — pre-registered inertness falsifier"
uv run python - "$OUT" "$SEEDS" "$DELTAS" <<'PY' | tee "$OUT/verdict.txt"
import json, os, sys
import numpy as np

out, seeds, deltas = sys.argv[1], sys.argv[2].split(), sys.argv[3].split()
KEYS = ("completion", "survival_rate", "episode_return")
M51E = {"completion": 0.0145, "survival_rate": 0.0129}  # 5090, for reference

fp = os.path.join(out, "reproducibility_floor_medium.json")
if not os.path.exists(fp):
    print("INCOMPLETE — no measured floor; refusing to grade. No verdict.")
    raise SystemExit(0)
fl = json.load(open(fp))
FLOOR = {k: fl[k]["sd"] for k in ("completion", "survival_rate") if k in fl}

print("M5.5 — Phase-5 acceptance, RESCOPED: Medium x delta x "
      f"{len(seeds)} seeds, message path LIVE in both arms\n")
print("Grading bar: 2x the floor measured on THIS card, section 1.")
for k, v in FLOOR.items():
    print(f"  {k:16s} sd {v:.4f} -> bar {2 * v:.4f}   "
          f"(M5.1e on a 5090: {M51E[k]:.4f})")

def load(delta, seed):
    p = os.path.join(out, f"eval_d{delta}_s{seed}.npz")
    return {k: np.asarray(v) for k, v in np.load(p).items()} if os.path.exists(p) else None

per = {(d, s): load(d, s) for d in deltas for s in seeds}
if any(v is None for v in per.values()):
    print(f"\nINCOMPLETE — missing {[k for k, v in per.items() if v is None]}")
    raise SystemExit(0)

print(f"\n{'delta':8s} " + "  ".join(f"{k:>16s}" for k in KEYS)
      + "   delivery   out-deg   fire/danger")
stats = {}
for d in deltas:
    row = {}
    for k in KEYS:
        vals = [per[(d, s)][k].mean() for s in seeds]
        row[k] = (float(np.mean(vals)), float(np.std(vals, ddof=1)))
    la = sum(per[(d, s)]["links_alive"].sum() for s in seeds)
    lr = sum(per[(d, s)]["links_in_range"].sum() for s in seeds)
    aa = sum(per[(d, s)]["alive_agents"].sum() for s in seeds)
    da = sum(per[(d, s)]["danger_agents"].sum() for s in seeds)
    df = sum(per[(d, s)]["deaths_fire"].sum() for s in seeds)
    row["delivery"] = la / lr if lr else float("nan")
    row["outdeg"] = la / aa if aa else float("nan")
    # Condition (iii): fire deaths per danger agent-step — the danger-moment
    # outcome, pooled as a ratio of sums rather than a mean of ratios.
    row["fire_per_danger"] = df / da if da else float("nan")
    stats[d] = row
    print(f"{d:8s} " + "  ".join(f"{row[k][0]:8.4f}+-{row[k][1]:<6.4f}" for k in KEYS)
          + f"   {row['delivery']:8.4f}  {row['outdeg']:7.3f}  "
            f"{row['fire_per_danger']:11.5f}")

a, b = deltas[0], deltas[-1]
print(f"\nFalsifier conditions ({a} vs {b}):")
cond = {}
for k in FLOOR:
    d = stats[a][k][0] - stats[b][k][0]
    cond[k] = abs(d) <= 2 * FLOOR[k]
    print(f"  (i)   d{k:16s} {d:+.4f}  vs bar {2 * FLOOR[k]:.4f}  -> "
          + ("within floor" if cond[k] else "ABOVE FLOOR"))
knob = abs(stats[a]["delivery"] - stats[b]["delivery"]) > 0.5
print(f"  (ii)  delivery {stats[a]['delivery']:.4f} -> {stats[b]['delivery']:.4f}"
      f"  -> {'knob MOVED' if knob else 'KNOB DID NOT MOVE — grid is void'}")
dd = stats[a]["fire_per_danger"] - stats[b]["fire_per_danger"]
rel = abs(dd) / max(stats[a]["fire_per_danger"], 1e-9)
cond3 = rel <= 0.20
print(f"  (iii) fire deaths per danger agent-step {dd:+.5f} "
      f"({100 * rel:.1f}% relative) -> "
      + ("no danger-moment difference" if cond3 else "DANGER-MOMENT DIFFERENCE"))

print("\n" + "=" * 70)
if not knob:
    print("VERDICT: VOID — the denial knob did not move; nothing is testable.")
elif all(cond.values()) and cond3:
    print("VERDICT: INERT — all three falsifier conditions hold.")
    print("The denial element is certified inert at swarm scale: a")
    print("REPORTABLE NEGATIVE, as the M5.3 closure ruling anticipated.")
    print("delta = 1.0 stays in theta* for registration fidelity at zero")
    print("cost; the Phase-7 composition is over {Coupling A, Coupling B}.")
else:
    print("VERDICT: NOT INERT — the falsifier failed, and that is a finding.")
    failed = [k for k, v in cond.items() if not v] + ([] if cond3 else ["danger-moment"])
    print(f"Failing condition(s): {failed}.")
    print("This CONTRADICTS the M5.3/M5.3b certification and goes straight")
    print("to the human: a certified negative that its own confirmation run")
    print("overturns is the most important result in the phase. Do not")
    print("reconcile it here.")
print("=" * 70)
print("\nThe floor above has 3 dof and is uncertain by ~+/-40 %; differences")
print("near the bar are near the bar. Regime: NON-DETERMINISTIC runs.")
PY

{
  echo "run: M5.5 Phase-5 acceptance (rescoped: Medium x delta x 4 seeds)"
  echo "date_utc: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "git_commit: $(git rev-parse HEAD)"
  echo "git_dirty: $(git status --porcelain | wc -l) file(s)"
  echo "config: $CFG   dp: $DP   updates: $UPDATES   R_comm: $R_COMM (LOCKED)"
  echo "seeds: $SEEDS   deltas: $DELTAS   eval_episodes: $N_EVAL"
  echo "msg_mode: live in BOTH arms (the ablation is denial, not architecture)"
  echo "floor: $FLOOR_REPS identical runs at seed $FLOOR_SEED, delta 0"
  echo "gpu: $(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null || echo unknown)"
  echo "jax: $(uv run python -c 'import jax, jaxlib; print(jax.__version__, jaxlib.__version__)' 2>/dev/null || echo unknown)"
} | tee "$OUT/provenance.txt"

for f in provenance.txt timings.txt verdict.txt reproducibility_floor_medium.json; do
  [ -s "$OUT/$f" ] || {
    echo "FATAL: $OUT/$f missing or empty — do NOT release the instance" >&2
    exit 1
  }
done

echo ""
echo "M5.5 complete — bring back $OUT/ (incl. all .tar.zst + .sha256) and"
echo "m55_console.log. These checkpoints cannot be regenerated."
