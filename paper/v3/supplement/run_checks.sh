#!/usr/bin/env bash
# Build the supplement and run every check. Usage (from the repository root):
#   bash paper/v3/supplement/run_checks.sh WORKDIR [package.py switches...]
# WORKDIR must not exist; the unpacked supplement and its venv are kept there.
set -u
W=${1:?usage: run_checks.sh WORKDIR [package.py switches]}; shift
PY=${PY:-.venv/bin/python}
D=paper/v3/supplement
LOG=paper/v3/out/checks_summary.txt
$PY $D/package.py "$@" > paper/v3/out/package_console.txt || { echo "PACKAGE FAILED"; exit 1; }
rc=0; : > "$LOG"
for c in "check_scrub.py" "check_size.py" "check_manifest.py" \
         "check_tests.py --workdir $W" "check_reproduce.py --workdir $W"; do
  echo "== $c" | tee -a "$LOG"
  $PY $D/$c 2>&1 | tee -a "$LOG" | tail -n 25
  [ "${PIPESTATUS[0]}" -eq 0 ] || rc=1
done
echo "== overall: $([ $rc -eq 0 ] && echo PASS || echo FAIL)" | tee -a "$LOG"
exit $rc
