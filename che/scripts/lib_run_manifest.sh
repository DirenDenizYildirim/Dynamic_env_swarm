#!/usr/bin/env bash
# Per-run completion manifest — the grid's resume story (T* ruling, 2026-08-11,
# item 8). Source it; it defines functions and touches nothing on load.
#
# WHY. The grid is 240 independent runs across a ~36-hour spot rental. An
# interruption must cost <= 1 run, so a restart has to know exactly which runs
# finished. The floor script keeps its refuse-nonempty guard instead (integrity
# over convenience there: 24 runs are cheap to restart) — this library is for
# the grid.
#
# TWO DEFECTS IN THE OBVIOUS IMPLEMENTATION, both found in the existing floor
# script and both the project's recurring shape — a check that passes for the
# wrong reason:
#
#   (a) APPEND IS NOT IDEMPOTENT. run_m62_floors.sh:88 does
#       `sha256sum ... | tee -a SHA256_CKPT.txt`, and run_m62b_t1000.sh:135
#       asserts `wc -l == expected`. Under a resume, a re-executed run appends
#       a SECOND line for the same tag. One missing run plus one duplicated
#       line gives exactly the expected count, and the assertion PASSES WITH A
#       RUN ABSENT. Here every entry is KEYED BY TAG and rewritten, so a tag
#       can never contribute two records, and the aggregate SHA256_CKPT.txt is
#       DERIVED from the keyed entries rather than appended to.
#
#   (b) EXISTENCE IS NOT INTEGRITY. "the archive and its hash exist" is
#       satisfied by a truncated archive from a run killed mid-tar. So
#       `manifest_complete` re-verifies the recorded hash against the file,
#       and `manifest_record` writes the archive to a temp name, hashes it,
#       moves it into place, and only THEN writes the manifest entry. A crash
#       at any point leaves no entry, so the run is correctly not-done.
#
# Usage:
#   source che/scripts/lib_run_manifest.sh
#   manifest_complete "$OUT" "$tag" && { echo "skip $tag"; continue; }
#   ... train + eval into $OUT/ckpt_$tag ...
#   manifest_record "$OUT" "$tag"
#   manifest_write_aggregate "$OUT"     # derives SHA256_CKPT.txt
#   manifest_assert_all "$OUT" tag1 tag2 ...

manifest_dir() { printf '%s/.manifest' "$1"; }

# Exit 0 iff the run finished AND its archive still verifies against the hash
# recorded at the time it finished.
manifest_complete() {
  local out="$1" tag="$2"
  local entry; entry="$(manifest_dir "$out")/${tag}.done"
  local archive="$out/ckpt_${tag}.tar.zst"
  [ -s "$entry" ] || return 1
  [ -s "$archive" ] || return 1
  local want; want="$(cut -d' ' -f1 < "$entry")"
  [ -n "$want" ] || return 1
  local got; got="$(sha256sum "$archive" | cut -d' ' -f1)"
  [ "$want" = "$got" ]
}

# Archive the run's checkpoint dir and mark it complete. Atomic: the entry is
# the LAST thing written, so it exists only if everything before it succeeded.
manifest_record() {
  local out="$1" tag="$2"
  local src="ckpt_${tag}"
  local final="$out/ckpt_${tag}.tar.zst"
  local tmp="$out/.tmp.${tag}.$$.tar.zst"
  [ -d "$out/$src" ] || { echo "manifest_record: no $out/$src" >&2; return 1; }
  mkdir -p "$(manifest_dir "$out")" || return 1
  tar --zstd -cf "$tmp" -C "$out" "$src" || { rm -f "$tmp"; return 1; }
  local h; h="$(sha256sum "$tmp" | cut -d' ' -f1)" || { rm -f "$tmp"; return 1; }
  mv -f "$tmp" "$final" || { rm -f "$tmp"; return 1; }
  # Entry last, and REWRITTEN rather than appended: a tag has exactly one,
  # so a re-executed run replaces its record instead of duplicating it.
  printf '%s  %s\n' "$h" "$final" > "$(manifest_dir "$out")/${tag}.done"
}

# Rebuild SHA256_CKPT.txt from the keyed entries. DERIVED, never appended, so
# it cannot carry a duplicate or a stale line from an interrupted attempt.
manifest_write_aggregate() {
  local out="$1"
  local d; d="$(manifest_dir "$out")"
  : > "$out/SHA256_CKPT.txt"
  [ -d "$d" ] || return 0
  local f
  for f in $(ls -1 "$d"/*.done 2>/dev/null | sort); do
    cat "$f" >> "$out/SHA256_CKPT.txt"
  done
}

# Fail loudly if any expected tag is missing or fails verification. Counts are
# not trusted — every tag is checked by name, which is defect (a)'s fix.
manifest_assert_all() {
  local out="$1"; shift
  local missing=0 tag
  for tag in "$@"; do
    if ! manifest_complete "$out" "$tag"; then
      echo "INCOMPLETE OR CORRUPT RUN: $tag" >&2
      missing=$((missing + 1))
    fi
  done
  if [ "$missing" -ne 0 ]; then
    echo "FATAL: $missing of $# runs incomplete — DO NOT RELEASE THE INSTANCE." >&2
    return 1
  fi
  echo "OK: $# runs complete and verified."
}
