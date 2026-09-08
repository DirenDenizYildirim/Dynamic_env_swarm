#!/usr/bin/env bash
# pull_box_artifacts.sh — copy one results directory from the GPU box to this
# machine with rsync, then verify every checkpoint archive against a hash
# computed on the box at pull time.
#
# RESUMABLE. Re-run the identical command after any interruption: rsync
# resumes partial files (--partial --append-verify), and the verification
# pass deletes any archive whose local hash does not match the box's so the
# next run re-fetches it. Exits non-zero if any archive still fails to verify
# or if the box holds no archives at all.
#
# WHY VERIFY AFTER RSYNC. rsync checks its own transfer, but the manifest's
# hash certifies the archive as it was on the box and this pass certifies
# the COPY against that. The card-2 re-floor
# (results/phase6/g1_floors_card2/README.md) holds an archive that is 14.6 MB
# against 44.8 MB for its siblings and does not decompress — an eval that
# exists beside an archive that does not. That is what an unverified pull
# looks like.
#
# Raw checkpoint directories (ckpt_<tag>/) are never pulled: the grid reclaims
# them after archiving, and the floor script's copies are inside the archives.
#
# Usage, from the repo root on the laptop:
#   BOX=root@<host> PORT=<port> bash che/scripts/pull_box_artifacts.sh \
#       che/bench/results/phase6/g1_floors [local_dir]
# Optional: REMOTE_REPO=che_repo (path of the repo on the box, relative to ~).
set -uo pipefail

BOX=${BOX:?set BOX=root@host}
PORT=${PORT:?set PORT=}
REMOTE_REPO=${REMOTE_REPO:-che_repo}
rel=${1:?remote results dir, relative to the repo root}
local_dir=${2:-$rel}

SSH_CMD="ssh -p $PORT -o ServerAliveInterval=30 -o ConnectTimeout=20"
mkdir -p "$local_dir" || exit 1

# GUARD — never pull into a directory that already holds archives from a
# DIFFERENT run. On 2026-09-09 the grid card's re-floor was pulled into
# results/phase6/g1_floors, which held the 2026-08-10 launch batch under the
# same filenames; 20 August archives were overwritten and 4 removed before
# the hash check noticed (README_ARCHIVES_REBUILT.md there). The box writes
# each milestone to a fixed relative path, so the LOCAL path must be per
# rental. If archives exist locally, every one of them must already match a
# hash on the box, i.e. this is a resume of the same pull; otherwise refuse.
if ls "$local_dir"/ckpt_*.tar.zst >/dev/null 2>&1; then
  remote_hashes=$($SSH_CMD "$BOX" "cd $REMOTE_REPO/$rel && sha256sum ckpt_*.tar.zst 2>/dev/null | cut -d' ' -f1") || {
    echo "FATAL: cannot hash remote archives to check resume safety" >&2; exit 1; }
  for f in "$local_dir"/ckpt_*.tar.zst; do
    h=$(sha256sum "$f" | cut -d' ' -f1)
    if ! grep -q "$h" <<< "$remote_hashes"; then
      echo "FATAL: $f exists locally and matches NO archive on the box." >&2
      echo "  This local directory holds a different run. Pull into a fresh," >&2
      echo "  dated directory instead (e.g. ${rel}_$(date +%F))." >&2
      exit 1
    fi
  done
fi

echo "== rsync $BOX:$REMOTE_REPO/$rel/ -> $local_dir/"
for attempt in 1 2 3; do
  rsync -a --partial --append-verify --info=progress2 \
    --exclude 'ckpt_*/' --exclude '.tmp.*' \
    -e "$SSH_CMD" "$BOX:$REMOTE_REPO/$rel/" "$local_dir/" && break
  echo "     rsync attempt $attempt failed; retrying in 15 s"; sleep 15
done

echo "== verifying archives against hashes computed on the box now"
$SSH_CMD "$BOX" "cd $REMOTE_REPO/$rel && (ls ckpt_*.tar.zst >/dev/null 2>&1 && sha256sum ckpt_*.tar.zst || true)" \
  > "$local_dir/.remote_sha256.txt" || { echo "FATAL: remote hash failed" >&2; exit 1; }

n=0; ok=0; bad=0
while read -r want name; do
  [ -n "$name" ] || continue
  n=$((n+1))
  have=$(sha256sum "$local_dir/$name" 2>/dev/null | cut -d' ' -f1)
  if [ "$have" = "$want" ]; then
    ok=$((ok+1))
  else
    echo "BAD  $name (local hash mismatch or missing) — removed; re-run to re-fetch"
    rm -f "$local_dir/$name"; bad=$((bad+1))
  fi
done < "$local_dir/.remote_sha256.txt"

echo "== archives on box: $n   verified locally: $ok   FAILED: $bad"
[ "$bad" -eq 0 ] && [ "$n" -gt 0 ]
