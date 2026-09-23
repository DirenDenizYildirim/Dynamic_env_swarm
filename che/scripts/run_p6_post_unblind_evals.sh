#!/usr/bin/env bash
# POST-UNBLIND EVALUATION STAGE — eval-only, over hash-verified archives.
#
# Three blocks, all registered before the grid ran, none of which trains:
#
#   GAMMA_T   T* ruling (2026-08-11), item 3: Gamma(t) over the FINAL HALF of
#             training is REQUIRED robustness evidence. Every confirmatory
#             checkpoint retained for it (updates 500..950; 1000 is the grid's
#             own eval) is evaluated at theta* on the common set.
#             144 runs x 10 steps = 1440 evals.
#   HIGH      S7 ruling (2026-09-18), proposal 3 as replaced: the T* = 1000
#             checkpoint of every ISO, JOINT and ISO-4 run, plus the 16 same-
#             seed floor reps, evaluated once under joint_high.yaml (theta*
#             with beta 0.49 -> 0.70, verified one-line diff). NOT a held-out
#             test; its reading rule is asymmetric and registered there.
#   EVALFLOOR CARD RULING amendment (2026-09-22): a cross-card eval floor is
#             owed before Gamma(t) is read. Same checkpoint, same card, N
#             repeated evals (A-vs-A) -- the eval-only reproducibility of THIS
#             card, which is what the Gamma(t) numbers inherit.
#
# IT CANNOT RUN BEFORE THE UNBLIND STEP. The unblind instrument appends to
# UNBLIND_LOG.txt on every real look; this script refuses unless that file
# exists and is non-empty. Ship it with the tree. (Evaluating Gamma(t) before
# the branch is fixed would let the trajectory inform the reading of T*.)
#
# THIS SCRIPT COMPUTES NO CONTRAST. Every eval is DECLARED cross-config via
# --allow-hash with the training hash, evaluated at an EXPLICIT --step, and
# the written ckpt_step is re-asserted. Outputs go to their own directories;
# METRICS, the grid script and every lock are untouched. Resumable: an eval
# whose JSON exists is skipped.
#
# Usage on the box, from the repo root:
#   GIT_COMMIT=<hash> bash che/scripts/run_p6_post_unblind_evals.sh 2>&1 | tee p6_post_console.log
#   BLOCKS="gamma_t high evalfloor" (default all three)   DRY_RUN=1 enumerates
set -uo pipefail

UNBLIND_MARKER=${UNBLIND_MARKER:-che/bench/results/phase6/unblind/UNBLIND_LOG.txt}
BLOCKS=${BLOCKS:-"gamma_t high evalfloor"}
CONF_DIR=${CONF_DIR:-che/bench/results/phase6/g1_conf_5090}
ISO4_DIR=${ISO4_DIR:-che/bench/results/phase6/g1_iso4_5090}
FLOORS_DIR=${FLOORS_DIR:-che/bench/results/phase6/g1_floors_5090}
OUT_GT=${OUT_GT:-che/bench/results/phase6/post_gamma_t}
OUT_HIGH=${OUT_HIGH:-che/bench/results/phase6/post_high}
OUT_EF=${OUT_EF:-che/bench/results/phase6/post_evalfloor}
THETA_STAR=${THETA_STAR:-che/configs/theta_star_holdout.yaml}
HIGH_CFG=${HIGH_CFG:-che/configs/joint_high.yaml}
K_CONF=${K_CONF:-72}
K_ISO4=${K_ISO4:-20}
N_FLOOR_REPS=${N_FLOOR_REPS:-8}
T_STAR=${T_STAR:-1000}
GAMMA_T_STEPS=${GAMMA_T_STEPS:-"500 550 600 650 700 750 800 850 900 950"}
EVALFLOOR_REPS=${EVALFLOOR_REPS:-4}
EVALFLOOR_TAGS=${EVALFLOOR_TAGS:-"iso_s1 joint_s1"}
N_EVAL=${N_EVAL:-512}
EVAL_SEED=${EVAL_SEED:-0}
DRY_RUN=${DRY_RUN:-0}
SCRATCH=${SCRATCH:-.post_unblind_scratch}

if [ ! -s "$UNBLIND_MARKER" ]; then
  echo "FATAL: $UNBLIND_MARKER missing or empty." >&2
  echo "  This is the POST-UNBLIND evaluation stage. The unblind instrument" >&2
  echo "  writes that file on every real look; until it exists, Gamma(t) and" >&2
  echo "  the High readout must not run (T* ruling item 3; S7 ruling)." >&2
  exit 1
fi

# --------------------------------------------------------------- the plan
# (tag, archive, step, config, out_dir, out_stem)
PLAN=()
plan_add () { PLAN+=("$1|$2|$3|$4|$5|$6"); }
for blk in $BLOCKS; do
  case "$blk" in
    gamma_t)
      for arm in iso joint; do for s in $(seq 1 "$K_CONF"); do for u in $GAMMA_T_STEPS; do
        plan_add "${arm}_s${s}" "$CONF_DIR/ckpt_${arm}_s${s}.tar.zst" "$u" "$THETA_STAR" "$OUT_GT" "eval_${arm}_s${s}_u${u}"
      done; done; done ;;
    high)
      for arm in iso joint; do for s in $(seq 1 "$K_CONF"); do
        plan_add "${arm}_s${s}" "$CONF_DIR/ckpt_${arm}_s${s}.tar.zst" "$T_STAR" "$HIGH_CFG" "$OUT_HIGH" "evalhigh_${arm}_s${s}"
      done; done
      for s in $(seq 1 "$K_ISO4"); do
        plan_add "iso4_s${s}" "$ISO4_DIR/ckpt_iso4_s${s}.tar.zst" "$T_STAR" "$HIGH_CFG" "$OUT_HIGH" "evalhigh_iso4_s${s}"
      done
      for arm in iso joint; do for r in $(seq 1 "$N_FLOOR_REPS"); do
        plan_add "${arm}_rep${r}" "$FLOORS_DIR/ckpt_${arm}_rep${r}.tar.zst" "$T_STAR" "$HIGH_CFG" "$OUT_HIGH" "evalhigh_${arm}_rep${r}"
      done; done ;;
    evalfloor)
      for tag in $EVALFLOOR_TAGS; do for r in $(seq 1 "$EVALFLOOR_REPS"); do
        plan_add "$tag" "$CONF_DIR/ckpt_${tag}.tar.zst" "$T_STAR" "$THETA_STAR" "$OUT_EF" "evalfloor_${tag}_rep${r}"
      done; done ;;
    *) echo "FATAL: unknown block '$blk'" >&2; exit 1 ;;
  esac
done
echo "post-unblind evals planned: ${#PLAN[@]}  (blocks: $BLOCKS)"
if [ "$DRY_RUN" != "0" ]; then
  for e in "${PLAN[@]}"; do IFS='|' read -r tag arc u cfg od stem <<< "$e"; echo "$stem  step=$u  cfg=$cfg"; done
  exit 0
fi

mkdir -p "$OUT_GT" "$OUT_HIGH" "$OUT_EF" "$SCRATCH" || exit 1
started=$SECONDS; n_done=0; n_skip=0; n_fail=0; cur_arc=""; cur_dir=""
extract () {  # one archive resident at a time
  [ "$1" = "$cur_arc" ] && return 0
  [ -n "$cur_dir" ] && rm -rf "$cur_dir"
  [ -s "$1" ] || { echo "FATAL: archive missing: $1" >&2; return 1; }
  tar --zstd -xf "$1" -C "$SCRATCH" || return 1
  cur_arc=$1; cur_dir="$SCRATCH/ckpt_$2"
  [ -f "$cur_dir/config_hash.txt" ] || { echo "FATAL: no config_hash.txt in $cur_dir" >&2; return 1; }
}
for e in "${PLAN[@]}"; do
  IFS='|' read -r tag arc u cfg od stem <<< "$e"
  if [ -s "$od/$stem.json" ]; then n_skip=$((n_skip+1)); continue; fi
  extract "$arc" "$tag" || { n_fail=$((n_fail+1)); continue; }
  h=$(cat "$cur_dir/config_hash.txt")
  # DECLARED cross-config eval at an EXPLICIT step; the written step re-asserted.
  if uv run --no-sync python -m che.eval.harness \
       --config "$cfg" --ckpt-dir "$cur_dir" --step "$u" --allow-hash "$h" \
       --n-episodes "$N_EVAL" --seed "$EVAL_SEED" \
       --out-npz "$od/$stem.npz" --out-json "$od/$stem.json" >/dev/null \
     && uv run --no-sync python -c "
import json,sys; s=json.load(open('$od/$stem.json'))['ckpt_step']
sys.exit(0 if s == $u else print(f'ckpt_step={s}, want $u') or 1)"; then
    n_done=$((n_done+1))
  else
    rm -f "$od/$stem.json" "$od/$stem.npz"; n_fail=$((n_fail+1))
    echo "EVAL FAILED: $stem" >&2
  fi
  tot=$((n_done+n_skip+n_fail))
  if [ $((tot % 50)) -eq 0 ]; then
    echo "[$tot/${#PLAN[@]}] done=$n_done skip=$n_skip fail=$n_fail  elapsed $(( (SECONDS-started)/60 )) min"
  fi
done
[ -n "$cur_dir" ] && rm -rf "$cur_dir"
for od in "$OUT_GT" "$OUT_HIGH" "$OUT_EF"; do
  {
    echo "stage: post-unblind evals (blocks: $BLOCKS)"
    echo "date_utc: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo "git_commit: ${GIT_COMMIT:-$(git rev-parse HEAD 2>/dev/null || echo UNKNOWN-PROVENANCE-GAP)}"
    echo "unblind_marker: $UNBLIND_MARKER ($(wc -l < "$UNBLIND_MARKER") look(s) logged)"
    echo "gpu: $(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null || echo unknown)"
    echo "eval: n_episodes=$N_EVAL seed=$EVAL_SEED  theta_star=$THETA_STAR  high=$HIGH_CFG"
    echo "counts: planned=${#PLAN[@]} done=$n_done skipped=$n_skip failed=$n_fail"
  } >> "$od/provenance.txt"
done
echo "POST-UNBLIND EVALS: planned=${#PLAN[@]} done=$n_done skipped=$n_skip failed=$n_fail"
[ "$n_fail" -eq 0 ] || { echo "FATAL: $n_fail eval(s) failed — re-run to retry only those." >&2; exit 1; }
