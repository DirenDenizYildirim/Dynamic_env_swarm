#!/usr/bin/env bash
# G1.3 — THE PHASE-6 GRID. 240 runs, ~33 GPU-h, the phase's headline spend.
#
# Registered design: phase6_design_v2.md; layout in gpu_launch_prompt.md G1.3.
# Seed counts are LOCKED analysis constants (docs/locks.yaml: K_CONFIRMATORY
# 40, K_SECONDARY 20) and are read from there by test_p6_grid.py, not chosen
# here.
#
#   confirmatory  ISO, JOINT-classic          k = 40   ->  80 runs
#   secondary     dose sweep c=0.5, 5 points  k = 20   -> 100 runs
#   secondary     identification c=0.4, 3 pts k = 20   ->  60 runs
#                                                          --- 240
#
# Every run: train on its protocol config at T*, then evaluate at theta* on a
# COMMON 512-episode set. The per-run eval JSON is the grid's product; Gamma is
# computed from it POST-UNBLIND, by a different instrument, on a frozen tree.
#
# THIS SCRIPT COMPUTES NOTHING AND PRINTS NO OUTCOME. It trains, evaluates,
# archives and verifies. There is no call to m62_report here and there must
# never be one: Gamma is a cross-arm quantity and NO-PEEKING is in force until
# unblinding (docs/decision_log.md, PHASE-6 RULINGS FINAL FIVE; T* ruling §3).
# The eval JSONs on disk do contain per-arm means -- writing them is not
# reading them, and nobody reads them on the box.
#
# ---------------------------------------------------------------------------
# WHY THIS IS NOT run_m62_floors.sh WITH A BIGGER LOOP
#
# Three properties the floor script does not have and must not grow, because
# the floor script is the provenance of the M6.2/M6.2b/G1.2 floors and stays
# untouched.
#
#   1. RESUME. 240 runs across a ~36-hour spot rental; an interruption must
#      cost <= 1 run (T* ruling §8). The floor script keeps its refuse-nonempty
#      guard instead -- integrity over convenience there, since 24 runs are
#      cheap to restart. Here resume comes from lib_run_manifest.sh, whose
#      entries are KEYED and hash-VERIFYING; re-running this script retries
#      exactly what is missing and nothing else.
#
#   2. A PARAMETER-IDENTITY GUARD IN PLACE OF REFUSE-NONEMPTY. Resume means the
#      output directory is legitimately non-empty, so the guard that stops two
#      artifacts merging into one directory cannot be "is it empty". It is
#      instead a stamp: the arm set, T*, k, eval config and eval seed are
#      written on first run and re-checked on every resume. A resume with a
#      different T* or a different k is refused. Without this, the floors'
#      per-artifact protection is simply absent from the larger run -- the
#      same defect reached by a different door.
#
#   3. SEED-MAJOR ORDERING. See below; it is a robustness property, not a
#      style choice.
#
# ---------------------------------------------------------------------------
# THREE BUILDER DECISIONS, FLAGGED FOR RATIFICATION RATHER THAN ASSUMED
#
# None of these is a registered constant. The locks fix HOW MANY seeds; they
# do not fix WHICH integers, in what order, or against which eval draw. Stated
# here so they are visible before the spend rather than inferred after it.
#
# (a) SEEDS ARE 1..k, AND THE SAME INTEGERS IN EVERY ARM.
#
#     Starting at 1 rather than 0 is load-bearing: the floor runs are seed 0
#     (run_m62_floors.sh FLOOR_SEED=0). A grid run at seed 0 on iso, joint or
#     sweep_p500 would be the SAME config at the SAME seed for the SAME T as a
#     floor rep -- a reproducibility rep wearing a seed's name, contributing
#     zero seed variance to an arm whose dispersion is the confirmatory test's
#     denominator. Excluding 0 costs nothing and closes that.
#
#     Sharing the integers across arms is the conservative direction, not the
#     neutral one. The registered variance basis is the UNPAIRED combined form
#     sd(Gamma) = sqrt((s_iso^2 + s_joint^2)/k) (M6.2b close-out). True
#     Var(mean_J - mean_I) = (s_J^2 + s_I^2 - 2cov)/k, so any positive
#     cross-arm correlation makes the registered formula an OVERestimate of
#     sd(Gamma) -- conservative. Shared PRNG streams across two different
#     mixture configs can plausibly induce a small positive cov and implausibly
#     a negative one, so shared seeds put the residual error on the safe side
#     of the test. Disjoint ranges would be defensible too; they would just
#     forfeit that.
#
# (b) THE EVAL SET IS A CONSTANT: eval seed 0, 512 episodes, every run.
#
#     Identical to the floor protocol, deliberately -- floors and grid must be
#     the same instrument or the beat-reproducibility hurdle compares two
#     different measurements. It also makes cross-run variance TRAINING-seed
#     variance rather than training-seed plus eval-sampling noise, which is the
#     quantity the confirmatory test is registered to use.
#
# (c) RUN ORDER IS SEED-MAJOR, ARM-MINOR -- ALL 10 ARMS AT SEED 1, THEN SEED 2.
#
#     Arm-major ordering (all 40 ISO, then all 40 JOINT) has a failure mode
#     that costs the whole rental: a box lost at 60 % yields a complete ISO
#     arm, a partial JOINT arm, and NO usable Gamma at any k. Seed-major
#     truncation instead yields a smaller BALANCED design -- every arm at
#     k = floor(progress) -- which is a reportable result with stated power.
#     The interruption cost is thereby bounded in POWER rather than in
#     VALIDITY. Secondary arms run at seeds 1..20 only, so they complete
#     early and the tail is confirmatory-only.
#
#     This is not a licence to stop early and pick k after the fact. k is
#     locked; a short grid is an incident to report, and its realized k is
#     whatever the manifest says, chosen by the failure and not by the analyst.
#
# ---------------------------------------------------------------------------
# Run on the GPU box from the repo root:
#   GIT_COMMIT=$(git rev-parse HEAD) bash che/scripts/run_p6_grid.sh 2>&1 \
#     | tee p6_grid_console.log
#
# Re-run the identical command after any interruption. It resumes.
#   DRY_RUN=1 bash che/scripts/run_p6_grid.sh   # enumerate the layout, spend $0
set -uo pipefail

# shellcheck source=che/scripts/lib_run_manifest.sh
source "$(dirname "$0")/lib_run_manifest.sh"

OUT=${OUT:-che/bench/results/phase6/g1_grid}
UPDATES=${UPDATES:-1000}          # T*, locks.yaml
K_CONF=${K_CONF:-40}              # K_CONFIRMATORY, or k_req under ladder branch B
K_SEC=${K_SEC:-20}                # K_SECONDARY
N_EVAL=${N_EVAL:-512}
EVAL_SEED=${EVAL_SEED:-0}
# Overridable ONLY so the script itself is end-to-end testable on CPU --
# test_p6_grid.py drives train, eval, archive, manifest, resume and the
# completeness assertion on debug configs in about a minute, which is the
# alternative to discovering a typo 33 hours into a rental. The default is
# asserted by that test, the value is written into grid_params.txt,
# and a resume under a different one is REFUSED — so a deviation cannot be
# silent, which is the property that matters. Nothing on the box sets it.
THETA_STAR=${THETA_STAR:-che/configs/theta_star_holdout.yaml}
DRY_RUN=${DRY_RUN:-0}
KEEP_CKPT_DIRS=${KEEP_CKPT_DIRS:-0}
MIN_FREE_GB=${MIN_FREE_GB:-25}
MAX_CONSECUTIVE_FAILURES=${MAX_CONSECUTIVE_FAILURES:-3}
MAX_HOURS=${MAX_HOURS:-0}         # 0 = no wall-clock stop

# arm name -> training config. Order here is the order within a seed.
CONF_ARMS=${CONF_ARMS:-"\
iso:che/configs/p6_iso.yaml \
joint:che/configs/p6_joint.yaml"}
SEC_ARMS=${SEC_ARMS:-"\
sweep_c50_p000:che/configs/p6_sweep_c50_p000.yaml \
sweep_c50_p125:che/configs/p6_sweep_c50_p125.yaml \
sweep_c50_p250:che/configs/p6_sweep_c50_p250.yaml \
sweep_c50_p375:che/configs/p6_sweep_c50_p375.yaml \
sweep_c50_p500:che/configs/p6_sweep_c50_p500.yaml \
ident_c40_p000:che/configs/p6_ident_c40_p000.yaml \
ident_c40_p200:che/configs/p6_ident_c40_p200.yaml \
ident_c40_p400:che/configs/p6_ident_c40_p400.yaml"}

# --------------------------------------------------------------- the layout
# Built once, used for the run loop AND for the final assertion, so the two
# can never disagree about what "complete" means.
TAGS=()
for seed in $(seq 1 "$K_CONF"); do
  for pair in $CONF_ARMS; do
    TAGS+=("${pair%%:*}_s${seed}:${pair##*:}:${seed}")
  done
  if [ "$seed" -le "$K_SEC" ]; then
    for pair in $SEC_ARMS; do
      TAGS+=("${pair%%:*}_s${seed}:${pair##*:}:${seed}")
    done
  fi
done
N_RUNS=${#TAGS[@]}

if [ "$DRY_RUN" != "0" ]; then
  echo "DRY RUN — layout only, nothing trained, nothing written."
  echo "runs: $N_RUNS   updates: $UPDATES   k_conf: $K_CONF   k_sec: $K_SEC"
  echo "eval: $THETA_STAR  n_episodes=$N_EVAL  seed=$EVAL_SEED (common set)"
  for t in "${TAGS[@]}"; do echo "${t%%:*}"; done
  exit 0
fi

# ------------------------------------------------------------------ guard 1
# Parameter identity. Replaces the floor script's refuse-nonempty guard, which
# resume makes unusable. A resume that changes T*, k, the arm set or the eval
# draw would merge two artifacts into one directory and produce per-arm
# dispersions that grade nothing.
mkdir -p "$OUT" || exit 1
STAMP="$OUT/grid_params.txt"
stamp_now() {
  echo "updates: $UPDATES"
  echo "k_conf: $K_CONF"
  echo "k_sec: $K_SEC"
  echo "n_eval: $N_EVAL"
  echo "eval_seed: $EVAL_SEED"
  echo "eval_config: $THETA_STAR"
  echo "conf_arms: $(echo $CONF_ARMS | tr ' ' '\n' | sort | tr '\n' ' ')"
  echo "sec_arms: $(echo $SEC_ARMS | tr ' ' '\n' | sort | tr '\n' ' ')"
}
if [ -s "$STAMP" ]; then
  if ! diff -q <(stamp_now) "$STAMP" >/dev/null; then
    echo "FATAL: $OUT was produced under DIFFERENT grid parameters." >&2
    echo "  Floors and dispersions are PER-ARTIFACT. Resuming into it would" >&2
    echo "  merge two artifacts. Diff (want <- vs -> on disk):" >&2
    diff <(stamp_now) "$STAMP" >&2
    echo "  Set OUT= to a new path, or restore the original parameters." >&2
    exit 1
  fi
  echo "Resuming into $OUT — parameters match the recorded stamp."
else
  stamp_now > "$STAMP"
fi

# ------------------------------------------------------------------ guard 2
# Never start a milestone red (CLAUDE.md). Same owed files as the floor runner,
# plus the grid's own layout test.
OWED_TESTS=${OWED_TESTS:-"che/tests/test_prop3.py che/tests/test_calibration.py
                          che/tests/test_percolation.py che/tests/test_locks.py
                          che/tests/test_phase6_configs.py
                          che/tests/test_gamma_t_retention.py
                          che/tests/test_run_manifest.py
                          che/tests/test_p6_grid.py"}
echo "########## PRE-FLIGHT"
# shellcheck disable=SC2086
uv run pytest $OWED_TESTS -q -p no:warnings || {
  echo "FATAL: owed tests are RED. Not spending GPU time on a red tree." >&2
  exit 1
}

uv run python -m che.eval.harness --help 2>/dev/null | grep -q -- "--allow-hash" || {
  echo "FATAL: eval harness has no --allow-hash; cross-config eval impossible" >&2
  exit 1
}
tar --zstd -cf /dev/null --files-from /dev/null 2>/dev/null || {
  echo "FATAL: 'tar --zstd' unavailable" >&2; exit 1
}

# ------------------------------------------------------------------ guard 3
# Disk. The confirmatory arms retain 11 checkpoints each for the Gamma(t)
# window (T* ruling §3), so this grid is several times the footprint of any
# previous milestone. Running out of disk at run 180 of 240 is a preventable
# way to lose a rental.
free_gb=$(df -Pk "$OUT" | awk 'NR==2 {printf "%d", $4/1048576}')
if [ "${free_gb:-0}" -lt "$MIN_FREE_GB" ]; then
  echo "FATAL: only ${free_gb} GiB free at $OUT; want >= ${MIN_FREE_GB}." >&2
  echo "  240 archives, 80 of them carrying 11 checkpoints. Free space or" >&2
  echo "  set MIN_FREE_GB= if you have measured that less is enough." >&2
  exit 1
fi
echo "PRE-FLIGHT PASSED — ${free_gb} GiB free, ${N_RUNS} runs planned."

# Created, never truncated: the floor script truncates because it cannot
# resume, and doing that here would discard the timings of every run completed
# before the interruption.
touch "$OUT/timings.txt"

# ------------------------------------------------------------------ the runs
# $1 tag  $2 training config  $3 seed
run_one () {
  local tag=$1 cfg=$2 seed=$3 t0 t1 train_hash
  echo ""
  echo "=== ${tag}: train ${UPDATES} updates on ${cfg} at seed ${seed}"
  t0=$SECONDS
  uv run python -m che.train.ippo \
    --config "$cfg" --updates "$UPDATES" --seed "$seed" \
    --ckpt-dir "$OUT/ckpt_${tag}" --metrics "$OUT/${tag}.jsonl" || return 1
  t1=$SECONDS
  echo "train_${tag} $((t1 - t0))s" | tee -a "$OUT/timings.txt"

  # Cross-config evaluation, DECLARED not smuggled: the harness's config-hash
  # guard is correct and is satisfied with the TRAINING config's hash, which it
  # records in its own provenance (m30b precedent, and the floor script does
  # the same). Policies train on a protocol config and are graded at theta*.
  train_hash=$(cat "$OUT/ckpt_${tag}/config_hash.txt") || return 1
  echo "=== ${tag}: eval ${N_EVAL} episodes AT THETA* (allow-hash ${train_hash})"
  uv run python -m che.eval.harness \
    --config "$THETA_STAR" --ckpt-dir "$OUT/ckpt_${tag}" \
    --allow-hash "$train_hash" \
    --n-episodes "$N_EVAL" --seed "$EVAL_SEED" \
    --out-npz "$OUT/eval_${tag}.npz" --out-json "$OUT/eval_${tag}.json" || return 1
  echo "eval_${tag} $((SECONDS - t1))s" | tee -a "$OUT/timings.txt"

  # THE POLICY EVALUATED MUST BE THE ONE AT T*. The harness defaults to
  # `latest_step()`, which is correct -- and silently correct-looking if the
  # step-T* save never landed, in which case it grades the step-(T*-50) policy
  # and nothing anywhere says so. It also makes the retention change auditable
  # rather than assumed: the confirmatory arms now keep 11 checkpoints for the
  # Gamma(t) window while the G1.2 floors were measured on 3-checkpoint
  # artifacts, and the floors transfer ONLY because both evaluate the final
  # step. Asserted per run, not once.
  uv run --no-sync python -c "
import json,sys
s=json.load(open('$OUT/eval_${tag}.json'))['ckpt_step']
sys.exit(0 if s == $UPDATES else print(f'ckpt_step={s}, want $UPDATES') or 1)
" || {
    echo "FATAL: ${tag} was evaluated at the wrong checkpoint step." >&2
    return 1
  }

  # Archive + hash + manifest entry, entry written last (see the library).
  manifest_record "$OUT" "$tag" || return 1

  # The raw checkpoint directory is now redundant with a hash-verified archive,
  # and 240 of them will not fit beside their archives. Verified by LISTING the
  # archive -- which decompresses the zstd frame and walks the tar -- before
  # deleting the only other copy. Existence is not integrity; neither is a
  # hash of a file nobody has tried to read back.
  if [ "$KEEP_CKPT_DIRS" = "0" ]; then
    if tar --zstd -tf "$OUT/ckpt_${tag}.tar.zst" >/dev/null 2>&1; then
      rm -rf "$OUT/ckpt_${tag}"
    else
      echo "WARN: ${tag} archive did not list; keeping the directory." >&2
    fi
  fi
}

echo ""
echo "########## G1.3 GRID — ${N_RUNS} runs, seed-major, resumable"
started=$SECONDS
done_n=0; ran_n=0; skipped_n=0; failed_n=0; consec_fail=0
FAILED_TAGS=()
for entry in "${TAGS[@]}"; do
  tag="${entry%%:*}"; rest="${entry#*:}"; cfg="${rest%%:*}"; seed="${rest##*:}"
  done_n=$((done_n + 1))

  if manifest_complete "$OUT" "$tag"; then
    skipped_n=$((skipped_n + 1))
    echo "[${done_n}/${N_RUNS}] skip ${tag} — complete and verified"
    continue
  fi

  echo ""
  echo "[${done_n}/${N_RUNS}] ${tag}  (elapsed $(( (SECONDS - started) / 60 )) min)"
  if run_one "$tag" "$cfg" "$seed"; then
    ran_n=$((ran_n + 1)); consec_fail=0
  else
    failed_n=$((failed_n + 1)); consec_fail=$((consec_fail + 1))
    FAILED_TAGS+=("$tag")
    echo "RUN FAILED: ${tag} (${consec_fail} consecutive)" >&2
    # Leave NOTHING that a later glob could mistake for a result. A run that
    # died after its eval but before its manifest entry would otherwise leave
    # an eval JSON behind, and the post-unblind analysis reads eval JSONs.
    # The invariant is: an eval artifact exists IFF the run is manifest-
    # complete. Asserted below, not merely maintained here.
    rm -rf "$OUT/ckpt_${tag}" "$OUT/eval_${tag}.json" "$OUT/eval_${tag}.npz"
    if [ "$consec_fail" -ge "$MAX_CONSECUTIVE_FAILURES" ]; then
      echo "FATAL: ${consec_fail} consecutive failures — systematic, not transient." >&2
      echo "  Diagnose before burning the rental. Re-running this script" >&2
      echo "  resumes and retries only what is missing." >&2
      break
    fi
  fi

  if [ "$MAX_HOURS" != "0" ]; then
    if [ "$(( (SECONDS - started) / 3600 ))" -ge "$MAX_HOURS" ]; then
      echo "MAX_HOURS=${MAX_HOURS} reached — stopping cleanly after a complete run." >&2
      break
    fi
  fi
done

manifest_write_aggregate "$OUT"

# ----------------------------------------------------------- provenance
{
  echo "run: G1.3 Phase-6 grid (${N_RUNS} runs: confirmatory k=${K_CONF}, secondary k=${K_SEC})"
  echo "date_utc: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  # The box has no .git (source ships as a tarball), so the commit is passed
  # in explicitly. Provenance must not silently read "unknown" -- this is the
  # hash the pipeline is FROZEN at before unblinding.
  echo "git_commit: ${GIT_COMMIT:-$(git rev-parse HEAD 2>/dev/null || echo UNKNOWN-PROVENANCE-GAP)}"
  echo "git_dirty: $(git status --porcelain 2>/dev/null | wc -l) file(s)"
  echo "conf_arms: $CONF_ARMS"
  echo "sec_arms: $SEC_ARMS"
  echo "seeds: 1..${K_CONF} confirmatory, 1..${K_SEC} secondary (SAME integers across arms; 0 excluded — it is the floor seed)"
  echo "updates: $UPDATES   eval_episodes: $N_EVAL   eval_seed: $EVAL_SEED   eval_config: $THETA_STAR"
  echo "cross-config eval: declared via --allow-hash (training-config hash)"
  echo "ran_this_invocation: $ran_n   skipped_complete: $skipped_n   failed: $failed_n"
  echo "gpu: $(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null || echo unknown)"
  echo "python: $(uv run --no-sync python -c 'import sys;print(sys.version.split()[0])' 2>/dev/null || echo unknown)"
  echo "jax: $(uv run --no-sync python -c 'import jax,jaxlib;print(jax.__version__,jaxlib.__version__)' 2>/dev/null || echo unknown)"
} | tee "$OUT/provenance.txt"

# ------------------------------------------------------- completeness
# Counts are not trusted; every tag is checked by name and its archive
# re-hashed (lib_run_manifest.sh defect (a)).
echo ""
echo "########## COMPLETENESS + ARTIFACT PERSISTENCE"
EXPECTED=()
for entry in "${TAGS[@]}"; do EXPECTED+=("${entry%%:*}"); done

# NO ORPHANED EVALS. The post-unblind analysis reads eval JSONs, and it will
# find them by glob -- so an eval artifact left behind by a run that died after
# its eval but before its manifest entry would enter the analysis as a
# completed run, silently, with no archive to audit it against. Enforced here
# as an invariant (an eval exists IFF its run is manifest-complete) rather than
# trusted to the cleanup that maintains it, because the cleanup cannot run if
# the box dies between the two writes.
orphans=0
for f in "$OUT"/eval_*.json; do
  [ -e "$f" ] || continue
  otag=$(basename "$f" .json); otag=${otag#eval_}
  if ! manifest_complete "$OUT" "$otag"; then
    echo "ORPHANED EVAL (no verified archive): $f" >&2
    orphans=$((orphans + 1))
  fi
done
if [ "$orphans" -ne 0 ]; then
  echo "FATAL: $orphans eval artifact(s) without a complete run." >&2
  echo "  Delete them or re-run those tags. An analysis that globs eval_*.json" >&2
  echo "  would otherwise count them." >&2
  exit 1
fi

if manifest_assert_all "$OUT" "${EXPECTED[@]}"; then
  cat <<EOF

##########  G1.3 COMPLETE — ${N_RUNS} runs, all archives verified.

  STOP AND REPORT. DO NOT UNBLIND. Computing Gamma is a separate, human-gated
  step on a frozen tree; this box has produced eval JSONs and nobody reads
  them here.

  Before releasing the instance:
    - bring back $OUT/ IN FULL, including every .tar.zst and SHA256_CKPT.txt
    - the 11-checkpoint archives on iso_* and joint_* are the Gamma(t)
      robustness evidence — without them that ruling is unfulfillable
    - verify the transfer archive's sha256 on BOTH sides, and record
      "N OK, 0 mismatched" in the phase report
    - record git_commit from provenance.txt: it is the frozen pipeline hash
EOF
else
  cat <<EOF

##########  G1.3 INCOMPLETE — ${failed_n} failure(s) this invocation.

  Failed: ${FAILED_TAGS[*]:-none this invocation}

  Re-run the IDENTICAL command; it resumes and retries only what is missing.
  DO NOT RELEASE THE INSTANCE and do not treat the partial grid as a result
  without reporting the realized k per arm — which the manifest, not the
  analyst, determines.
EOF
  exit 1
fi
