#!/usr/bin/env bash
# Snapshots of the v3 sections and provenance tables, and the lines that changed between two
# of them, so that reviewers re-check only changed lines (paper_v3_prompt.md, step 4.3).
#
#   snapshot.sh <label>                copy sections/ and provenance/ to snapshots/<label>/
#   snapshot.sh diff <a> <b> [--word]  the changed lines from snapshot a to snapshot b
#                                      (b may be "current", the live files); --word marks
#                                      changed words instead of whole lines
#   snapshot.sh list                   the existing snapshots
#
# V2_ROOT (or V3_ROOT) overrides the paper folder (default: the folder above this script). A label is
# letters, digits, '.', '_' or '-', and an existing snapshot is never overwritten. Read-only
# apart from creating snapshots/<label>/. Uses diff, or git diff --no-index for --word
# (which reads files and changes no repository state).
set -euo pipefail
V2="${V3_ROOT:-${V2_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}}"  # paper/v3
SNAP="$V2/snapshots"

usage() { sed -n '2,15p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'; exit 2; }
valid() { [[ "$1" =~ ^[A-Za-z0-9._-]+$ ]] || { echo "bad label: $1" >&2; exit 2; }; }
where() {
  if [ "$1" = current ]; then
    mkdir -p "$TMPV/current"
    for d in sections provenance; do [ -d "$V2/$d" ] && cp -r "$V2/$d" "$TMPV/current/"; done
    echo "$TMPV/current"
  else
    valid "$1"; [ -d "$SNAP/$1" ] || { echo "no snapshot $1" >&2; exit 1; }; echo "$SNAP/$1"
  fi
}

[ $# -ge 1 ] || usage
case "$1" in
  list)
    [ -d "$SNAP" ] && ls -1 "$SNAP" || echo "(no snapshots)" ;;
  diff)
    [ $# -ge 3 ] || usage
    TMPV="$(mktemp -d)"; trap 'rm -rf "$TMPV"' EXIT
    A="$(where "$2")"; B="$(where "$3")"
    if [ "${4:-}" = "--word" ]; then
      git diff --no-index --no-color --word-diff=plain -U0 "$A" "$B" \
        | sed "s#a$A/#a/#g; s#b$B/#b/#g; s#$A/##g; s#$B/##g" || true
    else
      (cd "$A/.." && diff -r -U0 "$(basename "$A")" "$B" | sed "s#$B/##g") || true
    fi ;;
  -h|--help) usage ;;
  *)
    valid "$1"
    [ ! -e "$SNAP/$1" ] || { echo "snapshot $1 exists; pick another label" >&2; exit 1; }
    mkdir -p "$SNAP/$1"
    for d in sections provenance; do
      if [ -d "$V2/$d" ]; then cp -r "$V2/$d" "$SNAP/$1/"; else mkdir -p "$SNAP/$1/$d"; fi
    done
    echo "snapshot $1: $(find "$SNAP/$1" -type f | wc -l) files -> ${SNAP#"$V2"/}/$1/" ;;
esac
