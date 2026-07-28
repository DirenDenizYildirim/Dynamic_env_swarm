#!/usr/bin/env bash
# M4.4 GPU job — Coupling-B acceptance training grid (phase4_prompt.md
# M4.4 + the human M4.4 amendments of 2026-07-27).
#
# Grid: 3 severities x kappa_B in {0, 1.0 (M4.3 lock)} x seeds, dp = 0.5
# (D4), 500 updates, Coupling A ON at its M3.4-locked params. Medium runs
# a THIRD seed (amendment 4): Def.-4 variance concentrates near
# criticality, and "small but real" is now a pre-registered possibility
# there, which two seeds cannot separate from noise. => 14 train + 14
# eval runs.
#
# The kappa_B = 0 arm keeps obs v3 (visibility plane present, masking
# bitwise-inert) — the nesting-invariant ablation, not a different obs
# schema. It is also the free control for the provisional
# perception-exposure finding (amendment 2): identical lethality
# incentives, zero perception incentive.
#
# After the grid:
#   * detection-drift check + cross-arm exposure/ceiling/periphery
#     comparison, by pointing the M4.3 calibration at the seed-0
#     checkpoints of each arm (amendments 1 and 2; M3.5 drift precedent);
#   * render audit, >= 6 episodes per severity at the locked kappa_B,
#     plus the same episodes on the kappa_B = 0 arm at Medium so the
#     smoke-periphery positioning claim can be checked visually
#     (amendment 4c).
#
# Run on the GPU box from the repo root (after git pull):
#   bash che/scripts/run_m44_grid.sh 2>&1 | tee m44_console.log
# Expected wall time ~1.5 GPU-h (14 x ~280 s training + evals + renders).
# Bring back che/bench/results/phase4/m44/ + m44_console.log.
set -euo pipefail

OUT=che/bench/results/phase4/m44
KAPPA_LOCKED=1.0  # kappa_b_lock.md, human-locked 2026-07-27
DP=0.5            # D4
N_EVAL=${N_EVAL:-512}
mkdir -p "$OUT"
: > "$OUT/timings.txt"

for sev in low medium high; do
  cfg="che/configs/severity_${sev}.yaml"
  # Amendment 4: Medium gets a third seed; Low/High stay at two.
  seeds="0 1"
  [ "$sev" = "medium" ] && seeds="0 1 2"
  for kb in 0.0 "$KAPPA_LOCKED"; do
    kb_tag=$([ "$kb" = "0.0" ] && echo "kb0" || echo "kbL")
    for seed in $seeds; do
      tag="${sev}_${kb_tag}_dp${DP}_s${seed}"
      echo "=== train ${tag} ($(date -u +%H:%M:%S)) ==="
      t0=$SECONDS
      uv run python -m che.train.ippo \
        --config "$cfg" \
        --updates 500 \
        --seed "$seed" \
        --death-penalty "$DP" \
        --kappa-B "$kb" \
        --ckpt-dir "$OUT/ckpt_${tag}" \
        --metrics "$OUT/${tag}.jsonl"
      echo "train_${tag} $((SECONDS - t0))s" | tee -a "$OUT/timings.txt"
      echo "=== eval ${tag} ==="
      t0=$SECONDS
      uv run python -m che.eval.harness \
        --config "$cfg" \
        --death-penalty "$DP" \
        --kappa-B "$kb" \
        --ckpt-dir "$OUT/ckpt_${tag}" \
        --n-episodes "$N_EVAL" \
        --seed 0 \
        --out-npz "$OUT/eval_${tag}.npz" \
        --out-json "$OUT/eval_${tag}.json"
      echo "eval_${tag} $((SECONDS - t0))s" | tee -a "$OUT/timings.txt"
    done
  done
done

# --- Amendments 1 + 2: drift check and the cross-arm exposure control ---
# Same calibration engine as the M4.3 lock, pointed at the M4.4 policies.
# Arm kbL gives detection at the locked kappa_B under the 500-update
# checkpoints (drift vs the 200-update probes); the kb0/kbL pair gives
# the exposure/ceiling/periphery comparison that decides whether
# perception-exposure regulation is real or a fire-avoidance byproduct.
for arm in kb0 kbL; do
  kb=$([ "$arm" = "kb0" ] && echo "0.0" || echo "$KAPPA_LOCKED")
  echo "=== calibration under M4.4 policies (${arm}, kappa_B=${kb}) ==="
  t0=$SECONDS
  uv run python -m che.calibration.coupling_b \
    --n-eps 64 \
    --probe-kappa-B "$kb" \
    --probe-death-penalty "$DP" \
    --probe-ckpt "low=$OUT/ckpt_low_${arm}_dp${DP}_s0" \
    --probe-ckpt "medium=$OUT/ckpt_medium_${arm}_dp${DP}_s0" \
    --probe-ckpt "high=$OUT/ckpt_high_${arm}_dp${DP}_s0" \
    --out-dir "$OUT" \
    --out-name "m44_calibration_${arm}.json"
  echo "calibration_${arm} $((SECONDS - t0))s" | tee -a "$OUT/timings.txt"
done

# --- Render audit (standing rule + amendment 4c) ---
# >= 6 episodes per severity at the locked kappa_B. At Medium the same
# episode seeds are also rendered on the kappa_B = 0 arm, so the two arms
# can be compared frame-for-frame for smoke-periphery positioning.
mkdir -p "$OUT/renders"
for sev in low medium high; do
  cfg="che/configs/severity_${sev}.yaml"
  for ep in 0 1 2 3 4 5; do
    uv run python -m che.scripts.render_episode \
      --config "$cfg" \
      --death-penalty "$DP" \
      --kappa-B "$KAPPA_LOCKED" \
      --ckpt-dir "$OUT/ckpt_${sev}_kbL_dp${DP}_s0" \
      --seed "$ep" \
      --out "$OUT/renders/${sev}_kbL_ep${ep}.gif" \
      --tag "${sev} kappa_B=${KAPPA_LOCKED} ep${ep}"
    if [ "$sev" = "medium" ]; then
      uv run python -m che.scripts.render_episode \
        --config "$cfg" \
        --death-penalty "$DP" \
        --kappa-B 0.0 \
        --ckpt-dir "$OUT/ckpt_${sev}_kb0_dp${DP}_s0" \
        --seed "$ep" \
        --out "$OUT/renders/${sev}_kb0_ep${ep}.gif" \
        --tag "${sev} kappa_B=0 ep${ep}"
    fi
  done
done

echo "M4.4 grid complete — bring back $OUT/ and m44_console.log"
# RETRO-FLAG (human, 2026-07-28): the line below was a VIOLATION of the
# artifact-persistence rule now transcribed in CLAUDE.md. "Stay on the box"
# meant that when the instance was released the M4.4 checkpoints were lost,
# so the matched High kappa_B = 0 render set could not be produced from the
# trained policy and had to be retrained (Phase-5 pre-task). Kept, struck
# through, as the evidence: every GPU run archives (tar.zst + sha256)
# off-instance before release, and the job script asserts it.
echo "NOTE (SUPERSEDED — see CLAUDE.md artifact persistence): ckpt_* dirs stay on the box (m31b/m41/m43 precedent)."
