#!/usr/bin/env bash
# The real TMLR Beyond PDF author-kit build of Paper v2, with every automated check.
# See paper/v2/src/README.md. Usage (from anywhere):
#
#   PY=<python with pyyaml, markdown-it-py, pygments> \
#   paper/v2/src/kit_build.sh --scratch DIR [--root DIR] [--bib FILE] [--alt X]... [--final]
#
#   --scratch DIR  where downloads, the unzipped kit and the built site go. Each run makes a
#                  new directory DIR/kit_run_<time>_<pid>/ with a new, empty subdirectory per
#                  download; the Ruby gems are cached in DIR/gems. Nothing goes in the repo.
#   --root DIR     the v2 folder to build (default paper/v2); outputs go to DIR/out/.
#   --bib FILE     a bibliography to use instead of DIR/assets/bibliography/submission.bib.
#   --alt X        passed to build_v2.py (swap in sections/alt/ variants).
#   --final        passed to build_v2.py (also fail on M1 flags, STUB-SPEC blocks, ...).
#   --styles FILE  passed to build_v2.py (another _styles CSS; layout experiments only).
#
# Steps: build_v2.py; fetch the kit and verify its sha256 (fail on a mismatch); unzip without
# __MACOSX; stage submission_folder/ (kit_stage.py: comments stripped, bib % lines stripped,
# assets) and zip it; run the kit's own merge_files() (kit_merge.py, python -I; the kit's
# Docker launch is skipped, KIT_NOTES §S1.6); bundle install; LANG=C.UTF-8 bundle exec jekyll
# build --future; the same for an unstripped control copy; serve both _site trees with
# http-server; inspect with headless Chromium (kit_checks.mjs); grade (kit_report.py).
# Exit status: 0 if every check passes, 1 if any fails, 2 on a usage error, 3 on a kit
# sha256 mismatch.
set -euo pipefail

KIT_URL="https://tmlr-beyond-pdf.org/assets/tmlr-beyond-pdf-author-kit.zip"
KIT_SHA="e531434b698e04dc9e07e4100c8eb21f3a5a9caca873c102b589af4e9bacc2d5"
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$SRC/../../.." && pwd)"
PY="${PY:-python3}"
NODE_MODULES="${NODE_MODULES:-/opt/node22/lib/node_modules}"

SCRATCH="" ROOT="$REPO/paper/v2" BIB="" FINAL="" STYLES="" ALTS=()
while [ $# -gt 0 ]; do
  case "$1" in
    --scratch) SCRATCH="$2"; shift 2 ;;
    --root) ROOT="$(cd "$2" && pwd)"; shift 2 ;;
    --bib) BIB="$(cd "$(dirname "$2")" && pwd)/$(basename "$2")"; shift 2 ;;
    --alt) ALTS+=(--alt "$2"); shift 2 ;;
    --final) FINAL="--final"; shift ;;
    --styles) STYLES="$(cd "$(dirname "$2")" && pwd)/$(basename "$2")"; shift 2 ;;
    *) echo "unknown argument $1" >&2; exit 2 ;;
  esac
done
[ -n "$SCRATCH" ] || { echo "--scratch DIR is required" >&2; exit 2; }
mkdir -p "$SCRATCH"
SCRATCH="$(cd "$SCRATCH" && pwd)"
[ -n "$BIB" ] || BIB="$ROOT/assets/bibliography/submission.bib"
[ -f "$BIB" ] || BIB="$REPO/paper/v2/assets/bibliography/submission.bib"
OUT="$ROOT/out"

RUN_NAME="kit_run_$(date +%Y%m%d_%H%M%S)_$$"
RUN="$SCRATCH/$RUN_NAME"
mkdir "$RUN"
mkdir "$RUN/download" "$RUN/kit" "$RUN/kit_control" "$RUN/stage" "$RUN/serve" "$RUN/logs"
LOG="$RUN/logs"
echo "kit_build: run directory $RUN"

PIDS=()
cleanup() { for p in "${PIDS[@]:-}"; do [ -n "$p" ] && kill "$p" 2>/dev/null || true; done; }
trap cleanup EXIT

# 1. the v2 build (its own failures are graded later; outputs are written either way)
BUILD_ARGS=(--root "$ROOT" --bib "$BIB")
[ ${#ALTS[@]} -gt 0 ] && BUILD_ARGS+=("${ALTS[@]}")
[ -n "$FINAL" ] && BUILD_ARGS+=("$FINAL")
[ -n "$STYLES" ] && BUILD_ARGS+=(--styles "$STYLES")
set +e
"$PY" "$SRC/build_v2.py" "${BUILD_ARGS[@]}" | tee "$LOG/build_v2.log"
BUILD_RC=${PIPESTATUS[0]}
set -e
echo "kit_build: build_v2.py exit $BUILD_RC"

# 2. fetch the kit into its own new, empty directory, and verify it
curl -sS --fail -o "$RUN/download/kit.zip" "$KIT_URL"
GOT_SHA="$(sha256sum "$RUN/download/kit.zip" | cut -d' ' -f1)"
if [ "$GOT_SHA" != "$KIT_SHA" ]; then
  echo "kit_build: FAIL kit sha256 $GOT_SHA, expected $KIT_SHA" >&2
  printf '{"sha256": "%s", "sha_ok": false}\n' "$GOT_SHA" > "$RUN/run.json"
  exit 3
fi
echo "kit_build: kit sha256 verified"

# 3. unzip (twice: the staged build and the unstripped control), without __MACOSX
unzip -q "$RUN/download/kit.zip" -x '__MACOSX/*' -d "$RUN/kit"
unzip -q "$RUN/download/kit.zip" -x '__MACOSX/*' -d "$RUN/kit_control"
KIT="$RUN/kit/tmlr-beyond-pdf-author-kit"
CTRL="$RUN/kit_control/tmlr-beyond-pdf-author-kit"

# 4. stage submission_folder/ and zip it
"$PY" "$SRC/kit_stage.py" --root "$ROOT" --bib "$BIB" --stage "$RUN/stage" \
  --control-md "$RUN/control_submission.md" --expected "$RUN/expected.json" --report "$RUN/stage.json"
mkdir -p "$OUT"
rm -f "$OUT/submission_folder.zip"
(cd "$RUN/stage" && zip -X -r -q "$OUT/submission_folder.zip" submission_folder)
for K in "$KIT" "$CTRL"; do
  rm -rf "$K/submission_folder"
  cp -r "$RUN/stage/submission_folder" "$K/submission_folder"
done
cp "$RUN/control_submission.md" "$CTRL/submission_folder/submission.md"

# 5. the kit's own merge_files(), isolated Python
set +e
python3 -I "$SRC/kit_merge.py" "$KIT" > "$LOG/merge.log" 2>&1; MERGE_RC=$?
python3 -I "$SRC/kit_merge.py" "$CTRL" > "$LOG/merge_control.log" 2>&1; MERGE_RC=$((MERGE_RC + $?))
set -e

# 6. bundle install (gems cached under the scratch directory) and jekyll build
export BUNDLE_PATH="$SCRATCH/gems" BUNDLE_APP_CONFIG="$RUN/bundle_config"
set +e
(cd "$KIT/tmlr_do_not_modify" && bundle install > "$LOG/bundle.log" 2>&1); BUNDLE_RC=$?
(cd "$KIT/tmlr_do_not_modify" && LANG=C.UTF-8 LC_ALL=C.UTF-8 bundle exec jekyll build --future \
   > "$LOG/jekyll.log" 2>&1); JEKYLL_RC=$?
(cd "$CTRL/tmlr_do_not_modify" && bundle install > "$LOG/bundle_control.log" 2>&1 && \
   LANG=C.UTF-8 LC_ALL=C.UTF-8 bundle exec jekyll build --future > "$LOG/jekyll_control.log" 2>&1)
CJEKYLL_RC=$?
set -e
[ $BUNDLE_RC -eq 0 ] || { echo "kit_build: bundle install failed, see $LOG/bundle.log" >&2; tail -20 "$LOG/bundle.log" >&2; }
[ $JEKYLL_RC -eq 0 ] || { echo "kit_build: jekyll build failed, see $LOG/jekyll.log" >&2; tail -20 "$LOG/jekyll.log" >&2; }
GEMS="$(grep -E '^    (github-pages|jekyll|kramdown|kramdown-parser-gfm) \(' "$KIT/tmlr_do_not_modify/Gemfile.lock" 2>/dev/null \
        | sed -E 's/^ +//' | tr '\n' ' ' | sed 's/ $//')"
echo "kit_build: merge $MERGE_RC, bundle $BUNDLE_RC, jekyll $JEKYLL_RC, control $CJEKYLL_RC; $GEMS"

# 7. serve both sites at the kit's base URL
mkdir -p "$RUN/serve/main" "$RUN/serve/control"
cp -r "$KIT/tmlr_do_not_modify/_site" "$RUN/serve/main/tmlr-beyond-pdf"
cp -r "$CTRL/tmlr_do_not_modify/_site" "$RUN/serve/control/tmlr-beyond-pdf"
free_port() { python3 -I -c 'import socket; s=socket.socket(); s.bind(("127.0.0.1",0)); print(s.getsockname()[1]); s.close()'; }
P1="$(free_port)"; P2="$(free_port)"
# the server's own node process (not an npx wrapper), so the exit trap can stop it
HTTP_SERVER="$NODE_MODULES/http-server/bin/http-server"
node "$HTTP_SERVER" "$RUN/serve/main" -a 127.0.0.1 -p "$P1" -c-1 -s > "$LOG/serve.log" 2>&1 &
PIDS+=($!)
node "$HTTP_SERVER" "$RUN/serve/control" -a 127.0.0.1 -p "$P2" -c-1 -s > "$LOG/serve_control.log" 2>&1 &
PIDS+=($!)
PAGE="tmlr-beyond-pdf/under_review/submission/"
for _ in $(seq 1 60); do
  curl -s -o /dev/null "http://127.0.0.1:$P1/$PAGE" && curl -s -o /dev/null "http://127.0.0.1:$P2/$PAGE" && break
  sleep 0.5
done

cat > "$RUN/run.json" <<JSON
{"run_name": "$RUN_NAME", "root": "$(basename "$ROOT")", "sha256": "$GOT_SHA", "sha_ok": true, "build_rc": $BUILD_RC,
 "merge_rc": $MERGE_RC, "bundle_rc": $BUNDLE_RC, "jekyll_rc": $JEKYLL_RC,
 "control_jekyll_rc": $CJEKYLL_RC, "gems": "$GEMS"}
JSON

# 8. inspect with headless Chromium, then grade
set +e
PLAYWRIGHT_DISABLE_FORCED_CHROMIUM_PROXIED_LOOPBACK=1 NODE_PATH="$NODE_MODULES" node "$SRC/kit_checks.mjs" \
  --url "http://127.0.0.1:$P1/$PAGE" --control-url "http://127.0.0.1:$P2/$PAGE" \
  --expected "$RUN/expected.json" --out "$RUN/browser.json" \
  --pdf "$OUT/submission_v2_print.pdf" --screens "$OUT/kit_screens" 2>&1 | tee "$LOG/kit_checks.log"
CHECKS_RC=${PIPESTATUS[0]}
set -e
[ $CHECKS_RC -eq 0 ] || { echo "kit_build: the browser checks crashed (exit $CHECKS_RC)" >&2; exit 1; }
"$PY" "$SRC/kit_report.py" --stage "$RUN/stage.json" --browser "$RUN/browser.json" \
  --expected "$RUN/expected.json" --build-report "$OUT/build_report.json" --run "$RUN/run.json" \
  --pdf "$OUT/submission_v2_print.pdf" --zip "$OUT/submission_folder.zip" \
  --out-json "$OUT/kit_checks.json" --out-md "$OUT/kit_checks.md"
