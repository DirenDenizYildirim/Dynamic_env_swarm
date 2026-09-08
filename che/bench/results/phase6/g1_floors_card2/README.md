# g1_floors_card2 — a partial G1.2 re-floor on a second card, RECORDED 2026-09-08

**Status: provenance only. These runs grade nothing.** No ladder was
computed from them, no report exists, no decision-log entry authorized or
closed them, and the card that ran them is not recorded anywhere. Under the
per-hardware floor rule the card that runs the grid gets its own G1.2
re-floor before G1.3, and this directory does not substitute for it.

## What is here

The G1.2 protocol (`../g1_floors/`, `../g1/g1_2_report.md`): same-seed
reproducibility reps at seed 0, T = 1000, evaluated on
`che/configs/theta_star_holdout.yaml` with eval seed 0 and 512 episodes.
This copy is **incomplete**: G1.2 ran 12 ISO + 12 JOINT reps; this directory
holds

| artifact | ISO | JOINT |
|---|---|---|
| `eval_*.json` + `.npz` | rep1–rep8 | rep1–rep4 |
| training logs `*.jsonl` | rep1–rep8 | rep1–rep5 (rep5 has no eval: training started, run did not finish) |
| checkpoint archives `ckpt_*.tar.zst` (gitignored, local only) | rep1–rep8 | rep1–rep4 |

- The first eval is stamped `2026-08-14T18:20:03Z`; local file times run
  21:20 to 23:19 (+03) the same day.
- `timings.txt` records only the first run (train 501 s, eval 15 s).
- **`ckpt_iso_rep2.tar.zst` is truncated** (14.6 MB against ~44.8 MB for
  its siblings; `zstd -t` reports a premature end). Its eval exists because
  the harness evaluated the raw checkpoint directory before the archive was
  written. The other eleven archives were **not** re-verified against
  `SHA256_CKPT.txt` when this README was written.
- `SHA256_CKPT.txt` names this directory's path on the box
  (`che/bench/results/phase6/g1_floors_card2/`); the files were pulled to a
  local staging directory `_box_pull/` and relocated here on 2026-09-08 to
  match.

## What is not known

- Which card ran it. The floor script does not write per-run card records;
  that mechanism (`.manifest/<tag>.card`, `cards.txt`) shipped for the grid
  in 48fbf2b, after this rental.
- Why it stopped at 12 of 24 plus a partial thirteenth.
- Whether the rental was the one `HANDOFF.md` §1a anticipated ("one
  re-floor, first card") or a separate trip. `HANDOFF.md` as of 2026-09-08
  stated no box had run since G1.2 on 2026-08-10; that statement was wrong
  and is corrected there.

## Owed

An owner entry in `docs/decision_log.md` stating the card, the reason for
the stop, and whether these artifacts are discarded or kept as an
informational second-card sample. Until that entry exists this directory
is inert.
