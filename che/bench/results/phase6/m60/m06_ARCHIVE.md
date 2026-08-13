# `m06/` — archived and untracked (2026-08-13)

The repo root carried `m06/` (47 MB): the raw orbax checkpoint directory of
the **M6.0 traced-θ spike** — steps 38, 39, 40 plus `config_hash.txt`, 41
files, committed to git in full.

## Why it was untracked

It was **inconsistent with the project's own artifact-persistence rule**.
Every other checkpoint in this repo is archived as `tar.zst` + `sha256` and
gitignored (`.gitignore:227-269`); this one was committed raw.

**The intent to exclude it was already recorded and had silently failed.**
`.gitignore:227` has carried `/m06/` for some time — and did nothing, because
**gitignore does not untrack files already in the index**. So this is not a
new decision; it is the completion of one that was made, recorded, and never
took effect. Same shape as the defects this project keeps finding: *a rule
that passes for the wrong reason*, here by doing nothing at all while looking
like it did something.

## What was done

1. Archived: `m06_spike_ckpt.tar.zst`, 61 entries, in this directory
   (gitignored by `.gitignore:268`, held off-tree with the other archives).
2. **sha256** `e0697f049562d9ab31b282a1235b8a916482ebb86cf4e2aed3700b916be18f53`
3. `git rm -r --cached m06` — the files remain on disk and remain in git
   history; only the index entry is removed.

## Two limits, stated rather than implied

- **This does not shrink a clone.** The 41 blobs stay in history, so a fresh
  clone still transfers them. Removing them from history is a **rewrite** —
  destructive, irreversible, and a separate decision that belongs to the
  owner, not to release hygiene.
- **`che/bench/results/phase0_report.md` references `m06/pbt_curves.png` and
  `m06/events.jsonl`**, neither of which exists on disk any more and neither
  of which was ever tracked. That reference was already stale before this
  change and is unaffected by it; recorded here so it is not later attributed
  to the untracking.
