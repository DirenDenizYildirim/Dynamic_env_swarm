#!/usr/bin/env bash
# The §7 BLOCKS (ruled 2026-09-18; built 2026-09-23): ISO-4 and the T = 2000
# subsample. Two invocations of run_p6_grid.sh, each with ITS OWN output
# directory and ITS OWN parameter stamp — the open grid's stamp is not touched,
# and neither block can merge into the other or into the confirmatory artifact.
#
#   ISO-4    p6_iso4.yaml, seeds 1..20 (= K_SECONDARY), T* = 1000, eval at
#            theta* on the common set.  SENSITIVITY ARM, out of family.
#   T=2000   p6_iso_t2000 + p6_joint_t2000, seeds 1..4, UPDATES=2000, eval at
#            theta* on the common set.  DESCRIPTIVE ONLY, flagged UNDERPOWERED
#            at design time (MDE80 ~0.10 against a 0.03 band).
#
# THIS SCRIPT COMPUTES NOTHING. It inherits every guard of run_p6_grid.sh
# (stamp, ckpt_step == UPDATES per run, archive + manifest, no orphaned evals)
# and adds one provenance line: the SCIENCE TREE must be identical to the
# commit the grid froze on. The box has no .git, so that identity is asserted
# LOCALLY by che/tests/test_p6_s7_blocks.py before the tree ships, and this
# script only RECORDS the base commit it was shipped against. Gamma_4 and
# Gamma(2000) are computed post-unblind by the unblind instrument, not here.
#
# Usage on the box, from the repo root, AFTER the secondary re-card has exited:
#   GIT_COMMIT=<hash> bash che/scripts/run_p6_s7_blocks.sh 2>&1 | tee p6_s7_console.log
#   BLOCK=iso4|t2000|all (default all)   DRY_RUN=1 enumerates and spends $0
set -uo pipefail

HERE=$(dirname "$0")
BLOCK=${BLOCK:-all}
SCIENCE_TREE_BASE=${SCIENCE_TREE_BASE:-51e489a031b0e213d18644dbae19fc92052ede82}
OUT_ISO4=${OUT_ISO4:-che/bench/results/phase6/g1_iso4_5090}
OUT_T2000=${OUT_T2000:-che/bench/results/phase6/g1_t2000_5090}
K_ISO4=${K_ISO4:-20}     # = K_SECONDARY (docs/locks.yaml); asserted by test
K_T2000=${K_T2000:-4}    # §7 proposal 2, as ruled
T2000_UPDATES=${T2000_UPDATES:-2000}
MIN_FREE_GB=${MIN_FREE_GB:-6}

record_base () {
  # Appended to the block's own provenance, next to git_commit.
  [ "${DRY_RUN:-0}" != "0" ] && return 0
  {
    echo "science_tree_base: ${SCIENCE_TREE_BASE}"
    echo "science_tree_identity: asserted locally by che/tests/test_p6_s7_blocks.py before shipping (box has no .git)"
    echo "block: $1"
  } >> "$2/provenance.txt"
}

rc=0
if [ "$BLOCK" = "all" ] || [ "$BLOCK" = "iso4" ]; then
  echo "########## S7 BLOCK: ISO-4  (k = ${K_ISO4}, T* = 1000, own stamp at ${OUT_ISO4})"
  OUT="$OUT_ISO4" K_CONF="$K_ISO4" K_SEC=0 UPDATES=1000 MIN_FREE_GB="$MIN_FREE_GB" \
    CONF_ARMS="iso4:che/configs/p6_iso4.yaml" SEC_ARMS="" \
    bash "$HERE/run_p6_grid.sh" || rc=1
  record_base iso4 "$OUT_ISO4"
fi
if [ "$BLOCK" = "all" ] || [ "$BLOCK" = "t2000" ]; then
  echo "########## S7 BLOCK: T = ${T2000_UPDATES}  (k = ${K_T2000}, own stamp at ${OUT_T2000})"
  OUT="$OUT_T2000" K_CONF="$K_T2000" K_SEC=0 UPDATES="$T2000_UPDATES" MIN_FREE_GB="$MIN_FREE_GB" \
    CONF_ARMS="iso_t2000:che/configs/p6_iso_t2000.yaml joint_t2000:che/configs/p6_joint_t2000.yaml" \
    SEC_ARMS="" bash "$HERE/run_p6_grid.sh" || rc=1
  record_base t2000 "$OUT_T2000"
fi
[ "$rc" -eq 0 ] && echo "S7 BLOCKS: exit green. DO NOT UNBLIND HERE — pull, then the instrument runs on the frozen tree with the owner present."
exit $rc
