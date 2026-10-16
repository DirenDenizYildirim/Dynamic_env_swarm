#!/usr/bin/env bash
# INTERACTION CHECK AT theta* — eval-only, POST HOC, over hash-verified archives.
#
# Authorized by docs/decision_log.md, PAPER V3 item 2(a); scope theta* ONLY
# (PAPER V3 PHASE 1 START item 2); the links-open condition by PLAN AMENDMENT
# item 4 (2026-10-17). The analysis plan is
# che/bench/results/phase6/post_v3_interaction/PLAN.md, committed BEFORE this
# runs. Nothing here trains.
#
#   MAIN    the final (T* = 1000) checkpoint of every ISO (72), JOINT (72) and
#           ISO-4 (20) run, evaluated under the five conditions
#           {neither, a_only, b_only, both, links_open} on the common draw
#           (seed 0, 512 episodes). 164 x 5 = 820 evals. 'both' is theta*
#           itself; 'links_open' is theta* with delta = 0.
#   FLOOR   the eval self-floor on THIS card (per artifact: every condition is
#           its own artifact): iso_s1, joint_s1, iso4_s1, each condition 3 more
#           times. 3 x 5 x 3 = 45 evals. 865 in all.
#
# IT REFUSES WITHOUT THE PLAN. PLAN.md must exist and be non-empty; its sha256
# is recorded in provenance.txt, and the analysis refuses unless that hash
# matches the COMMITTED plan (the box has no .git, so the commit check happens
# in the analysis, not here). PLAN_SHA256=<hash> makes this script assert the
# hash too.
#
# THIS SCRIPT COMPUTES NO CONTRAST. Every eval is DECLARED cross-config via
# --allow-hash with the training hash, at an EXPLICIT --step, and the written
# ckpt_step and config are re-asserted. Every archive is verified against its
# SHA256_CKPT.txt (by basename) before extraction. Resumable: an eval whose
# JSON exists and passes the same assertion is skipped.
#
# ARTIFACT PERSISTENCE (CLAUDE.md): on completion it writes
# v3_interaction_results.tar.zst (evals/, floor/, timings.txt, provenance.txt
# and a copy of PLAN.md as .plan_at_run.md) and SHA256_RESULTS.txt, then
# ASSERTS: every planned JSON and NPZ is present, the archive lists every one
# of them, and its hash verifies. Copy BOTH files off the box before
# releasing it.
#
# Usage on the box, from the repo root:
#   GIT_COMMIT=<hash> bash che/scripts/run_interaction_evals.sh 2>&1 | tee interaction_console.log
#   BLOCKS="main floor" (default both)   DRY_RUN=1 enumerates and spends $0
#   VERIFY_ONLY=1 checks every needed archive against SHA256_CKPT.txt, evaluates
#   nothing, and exits non-zero if any is missing or does not match.
set -uo pipefail

OUT=${OUT:-che/bench/results/phase6/post_v3_interaction}
PLAN_FILE=${PLAN_FILE:-$OUT/PLAN.md}
BLOCKS=${BLOCKS:-"main floor"}
CONF_DIR=${CONF_DIR:-che/bench/results/phase6/g1_conf_5090}
ISO4_DIR=${ISO4_DIR:-che/bench/results/phase6/g1_iso4_5090}
K_CONF=${K_CONF:-72}
K_ISO4=${K_ISO4:-20}
T_STAR=${T_STAR:-1000}
N_EVAL=${N_EVAL:-512}
EVAL_SEED=${EVAL_SEED:-0}
FLOOR_TAGS=${FLOOR_TAGS:-"iso_s1 joint_s1 iso4_s1"}
FLOOR_REPS=${FLOOR_REPS:-3}
# condition -> config. 'both' is theta* itself (PLAN.md §2).
CFG_NEITHER=${CFG_NEITHER:-che/configs/interaction_neither.yaml}
CFG_A_ONLY=${CFG_A_ONLY:-che/configs/interaction_a_only.yaml}
CFG_B_ONLY=${CFG_B_ONLY:-che/configs/interaction_b_only.yaml}
CFG_BOTH=${CFG_BOTH:-che/configs/theta_star_holdout.yaml}
CFG_LINKS_OPEN=${CFG_LINKS_OPEN:-che/configs/interaction_links_open.yaml}
CONDITIONS="neither a_only b_only both links_open"
PY=${PY:-uv run --no-sync python}
DRY_RUN=${DRY_RUN:-0}
SCRATCH=${SCRATCH:-.interaction_scratch}
ARCHIVE_NAME=v3_interaction_results.tar.zst

if [ ! -s "$PLAN_FILE" ]; then
  echo "FATAL: $PLAN_FILE missing or empty." >&2
  echo "  The interaction check's analysis plan must be written and committed" >&2
  echo "  BEFORE any eval runs (PAPER V3 item 2(a); paper_v3_prompt.md step 0)." >&2
  exit 1
fi
plan_sha=$(sha256sum "$PLAN_FILE" | cut -d' ' -f1)
if [ -n "${PLAN_SHA256:-}" ] && [ "$PLAN_SHA256" != "$plan_sha" ]; then
  echo "FATAL: $PLAN_FILE sha256 $plan_sha != PLAN_SHA256 $PLAN_SHA256." >&2
  exit 1
fi

cfg_of () {
  case "$1" in
    neither) echo "$CFG_NEITHER" ;; a_only) echo "$CFG_A_ONLY" ;;
    b_only) echo "$CFG_B_ONLY" ;; both) echo "$CFG_BOTH" ;;
    links_open) echo "$CFG_LINKS_OPEN" ;;
    *) echo "FATAL: unknown condition $1" >&2; return 1 ;;
  esac
}
archive_of () {  # tag -> archive path
  case "$1" in
    iso4_s*) echo "$ISO4_DIR/ckpt_$1.tar.zst" ;;
    *) echo "$CONF_DIR/ckpt_$1.tar.zst" ;;
  esac
}

# --------------------------------------------------------------- the plan
# (tag, condition, out_subdir, out_stem). Grouped by archive, so each archive
# is extracted once per block.
PLAN=()
plan_add () { PLAN+=("$1|$2|$3|$4"); }
for blk in $BLOCKS; do
  case "$blk" in
    main)
      tags=()
      for arm in iso joint; do for s in $(seq 1 "$K_CONF"); do tags+=("${arm}_s${s}"); done; done
      for s in $(seq 1 "$K_ISO4"); do tags+=("iso4_s${s}"); done
      for tag in "${tags[@]}"; do for c in $CONDITIONS; do
        plan_add "$tag" "$c" evals "eval_${tag}_${c}"
      done; done ;;
    floor)
      for tag in $FLOOR_TAGS; do for r in $(seq 1 "$FLOOR_REPS"); do for c in $CONDITIONS; do
        plan_add "$tag" "$c" floor "floor_${tag}_${c}_rep${r}"
      done; done; done ;;
    *) echo "FATAL: unknown block '$blk'" >&2; exit 1 ;;
  esac
done
echo "interaction evals planned: ${#PLAN[@]}  (blocks: $BLOCKS)"
if [ "$DRY_RUN" != "0" ]; then
  for e in "${PLAN[@]}"; do
    IFS='|' read -r tag c sub stem <<< "$e"
    echo "$stem  step=$T_STAR  cfg=$(cfg_of "$c")  archive=$(archive_of "$tag")"
  done
  exit 0
fi

tar --zstd -cf /dev/null --files-from /dev/null 2>/dev/null || {
  echo "FATAL: 'tar --zstd' unavailable" >&2; exit 1; }

# A finished eval: JSON at the explicit step, under the condition's config,
# on the common draw. Used for both resume and post-eval assertion.
eval_ok () {  # json step cfg
  $PY -c "
import json,sys
d=json.load(open('$1'))
ok = d.get('ckpt_step') == $2 and d.get('config') == '$3' \
     and d.get('n_episodes') == $N_EVAL and d.get('seed') == $EVAL_SEED
sys.exit(0 if ok else print(f'bad eval record: $1') or 1)" 2>/dev/null
}

verify_archive () {  # archive -> 0 iff its sha256 matches SHA256_CKPT.txt by basename
  local arc="$1" dir base want got
  dir=$(dirname "$arc"); base=$(basename "$arc")
  [ -s "$arc" ] || { echo "FATAL: archive missing: $arc" >&2; return 1; }
  want=$(awk -v b="$base" '{n=split($2,p,"/"); if (p[n]==b) print $1}' "$dir/SHA256_CKPT.txt" 2>/dev/null | head -1)
  [ -n "$want" ] || { echo "FATAL: no recorded hash for $base in $dir/SHA256_CKPT.txt" >&2; return 1; }
  got=$(sha256sum "$arc" | cut -d' ' -f1)
  [ "$want" = "$got" ] || { echo "FATAL: sha256 mismatch for $arc" >&2; return 1; }
}

if [ "${VERIFY_ONLY:-0}" != "0" ]; then
  n_ok=0; n_bad=0; seen=""
  for e in "${PLAN[@]}"; do
    IFS='|' read -r tag c sub stem <<< "$e"
    arc=$(archive_of "$tag")
    case " $seen " in *" $arc "*) continue ;; esac
    seen="$seen $arc"
    if verify_archive "$arc"; then n_ok=$((n_ok+1)); else n_bad=$((n_bad+1)); fi
  done
  echo "ARCHIVES: verified=$n_ok bad_or_missing=$n_bad"
  [ "$n_bad" -eq 0 ] || exit 1
  exit 0
fi

mkdir -p "$OUT/evals" "$OUT/floor" "$SCRATCH" || exit 1
touch "$OUT/timings.txt"
started=$SECONDS; n_done=0; n_skip=0; n_fail=0; cur_arc=""; cur_dir=""
extract () {  # one archive resident at a time; verified before extraction
  local arc; arc=$(archive_of "$1")
  [ "$arc" = "$cur_arc" ] && return 0
  [ -n "$cur_dir" ] && rm -rf "$cur_dir"
  cur_arc=""; cur_dir=""
  verify_archive "$arc" || return 1
  tar --zstd -xf "$arc" -C "$SCRATCH" || return 1
  cur_arc=$arc; cur_dir="$SCRATCH/ckpt_$1"
  [ -f "$cur_dir/config_hash.txt" ] || { echo "FATAL: no config_hash.txt in $cur_dir" >&2; return 1; }
}
for e in "${PLAN[@]}"; do
  IFS='|' read -r tag c sub stem <<< "$e"
  cfg=$(cfg_of "$c") || exit 1
  js="$OUT/$sub/$stem.json"; nz="$OUT/$sub/$stem.npz"
  if [ -s "$js" ] && [ -s "$nz" ] && eval_ok "$js" "$T_STAR" "$cfg"; then
    n_skip=$((n_skip+1)); continue
  fi
  extract "$tag" || { n_fail=$((n_fail+1)); echo "EVAL FAILED (archive): $stem" >&2; continue; }
  h=$(cat "$cur_dir/config_hash.txt")
  t0=$SECONDS
  # DECLARED cross-config eval at an EXPLICIT step; the written record re-asserted.
  if $PY -m che.eval.harness \
       --config "$cfg" --ckpt-dir "$cur_dir" --step "$T_STAR" --allow-hash "$h" \
       --n-episodes "$N_EVAL" --seed "$EVAL_SEED" \
       --out-npz "$nz" --out-json "$js" >/dev/null \
     && eval_ok "$js" "$T_STAR" "$cfg"; then
    n_done=$((n_done+1))
    echo "${stem} $((SECONDS - t0))s" >> "$OUT/timings.txt"
  else
    rm -f "$js" "$nz"; n_fail=$((n_fail+1))
    echo "EVAL FAILED: $stem" >&2
  fi
  tot=$((n_done+n_skip+n_fail))
  if [ $((tot % 50)) -eq 0 ]; then
    echo "[$tot/${#PLAN[@]}] done=$n_done skip=$n_skip fail=$n_fail  elapsed $(( (SECONDS-started)/60 )) min"
  fi
done
[ -n "$cur_dir" ] && rm -rf "$cur_dir"

{
  echo "stage: interaction check at theta* (POST HOC, eval-only; blocks: $BLOCKS)"
  echo "date_utc: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "git_commit: ${GIT_COMMIT:-$(git rev-parse HEAD 2>/dev/null || echo UNKNOWN-PROVENANCE-GAP)}"
  echo "plan: $PLAN_FILE"
  echo "plan_sha256: $plan_sha"
  echo "gpu: $(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null || echo unknown)"
  echo "python: $($PY -c 'import sys; print(sys.version.split()[0])' 2>/dev/null || echo unknown)"
  echo "jax: $($PY -c 'import jax, jaxlib; print(jax.__version__, jaxlib.__version__)' 2>/dev/null || echo unknown)"
  echo "eval: n_episodes=$N_EVAL seed=$EVAL_SEED step=$T_STAR k_conf=$K_CONF k_iso4=$K_ISO4"
  echo "conditions: neither=$CFG_NEITHER a_only=$CFG_A_ONLY b_only=$CFG_B_ONLY both=$CFG_BOTH links_open=$CFG_LINKS_OPEN"
  echo "floor: tags=$FLOOR_TAGS reps=$FLOOR_REPS"
  echo "archives: conf=$CONF_DIR iso4=$ISO4_DIR (each verified against SHA256_CKPT.txt before extraction)"
  echo "cross-config eval: declared via --allow-hash (training-config hash)"
  echo "counts: planned=${#PLAN[@]} done=$n_done skipped=$n_skip failed=$n_fail"
} >> "$OUT/provenance.txt"
echo "INTERACTION EVALS: planned=${#PLAN[@]} done=$n_done skipped=$n_skip failed=$n_fail"
[ "$n_fail" -eq 0 ] || { echo "FATAL: $n_fail eval(s) failed — re-run to retry only those." >&2; exit 1; }

# ------------------------------------------------- persistence, asserted
missing=0; members=()
for e in "${PLAN[@]}"; do
  IFS='|' read -r tag c sub stem <<< "$e"
  for ext in json npz; do
    [ -s "$OUT/$sub/$stem.$ext" ] || { echo "FATAL: missing $OUT/$sub/$stem.$ext" >&2; missing=$((missing+1)); }
    members+=("$sub/$stem.$ext")
  done
done
[ "$missing" -eq 0 ] || exit 1
cp -f "$PLAN_FILE" "$OUT/.plan_at_run.md" 2>/dev/null || true
tmp="$OUT/.tmp.$$.tar.zst"
( cd "$OUT" && tar --zstd -cf "$(basename "$tmp")" "${members[@]}" timings.txt provenance.txt .plan_at_run.md ) \
  || { rm -f "$tmp"; echo "FATAL: archive failed" >&2; exit 1; }
mv -f "$tmp" "$OUT/$ARCHIVE_NAME" || exit 1
( cd "$OUT" && sha256sum "$ARCHIVE_NAME" > SHA256_RESULTS.txt ) || exit 1
( cd "$OUT" && sha256sum -c --quiet SHA256_RESULTS.txt ) || { echo "FATAL: results archive hash does not verify" >&2; exit 1; }
listed=$(tar --zstd -tf "$OUT/$ARCHIVE_NAME" | sort)
for m in "${members[@]}" timings.txt provenance.txt .plan_at_run.md; do
  grep -qxF "$m" <<< "$listed" || { echo "FATAL: $m not in $ARCHIVE_NAME" >&2; exit 1; }
done
echo "ARCHIVE OK: $OUT/$ARCHIVE_NAME  sha256 $(cut -d' ' -f1 < "$OUT/SHA256_RESULTS.txt")"
echo "Copy $OUT/$ARCHIVE_NAME and $OUT/SHA256_RESULTS.txt off the box before releasing it."
