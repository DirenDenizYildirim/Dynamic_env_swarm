# HANDOFF — session state for the next model (rewritten 2026-09-26)

You are picking up **post-grid, PRE-UNBLIND**, with the §7 blocks running on a
new box. Read `docs/decision_log.md` from the **§7 PROPOSALS RULING
(2026-09-18)** to the end before anything else; the last entry (*BOX CHANGE …
and the POST-UNBLIND ANALYSIS INSTRUMENT*, 2026-09-26) is the newest law and
this file only points at it.

## Where the artifacts are

| artifact | dir under `che/bench/results/phase6/` | state |
|---|---|---|
| **Confirmatory, k = 72, one card (RTX 5090 unit 1), one stamp** | `g1_conf_5090` | COMPLETE, verified, committed. **NOT UNBLINDED.** |
| Two-card grid, 252 runs | `g1_grid` | secondary seeds 13–20 live; conf seeds 1–12 SUPERSEDED (card diagnostic only) |
| 5090 floors (ladder BRANCH C) | `g1_floors_5090` | committed `e88e5fd`, 24/24 verified. `floors.json` = the `--floors` input |
| Secondary re-card, seeds 1–12, 8 arms, 96 runs | `g1_sec_s1_12_5090` | committed `e88e5fd`, **96/96 verified locally** against the box-written `SHA256_CKPT.txt` (the old pull never reached its own verification pass) |
| ISO-4 (k = 20), T = 2000 (4 seeds × 2 arms) | `g1_iso4_5090`, `g1_t2000_5090` | **COMPLETE** on unit 2 (2026-09-26, "S7 BLOCKS: exit green"), pulled and verified (20/20, 8/8), committed `968a781` and the T = 2000 commit. Not analysed. |

**Old box (unit 1, `180.189.55.43:13768`) is GONE** — vast.ai rented its GPU
to someone else after it was stopped. Nothing lived only there.

**Unit 2 was DESTROYED by the owner after the §7 pulls (2026-09-26 evening); the post-unblind stage needs a NEW 5090 (unit 3) and a fresh 6.8 GB upload — use six parallel rsyncs, the uplink is per-connection limited (~40 KB/s one stream, ~260 KB/s six).** Former unit 2: `ssh -p 36005 root@179.255.106.231`, repo `~/che_repo`
(shipped as `git archive e88e5fd`, no `.git`), identity in
`~/che_repo/UNIT.txt` (RTX 5090 `GPU-cc0a5b55-…`, driver 580.173.02, CUDA
13.0). Venv verified 3.12.3 / jax 0.11.0 / CudaDevice. 311 GB free.
Download speed measured 2.6–14.9 MB/s. **Keep this box through the
post-unblind eval stage** — ISO-4, T = 2000, Γ(t), High readout and the eval
floor all then run on one unit.

**Uploads to unit 2 were done and verified — now gone with the box; redo on unit 3.** `g1_conf_5090` 144/144 and
`g1_floors_5090` 24/24 are on the box for the post-unblind stage. **Verify
conf by FILENAME, not with `sha256sum -c SHA256_CKPT.txt`:** 68 of its 144
lines still carry `g1_grid/` paths (seeds 13–46 were copied from there), so
`-c` reports "FAILED open or read" on any other machine. Compare the box's
`sha256sum ckpt_*.tar.zst` against `g1_conf_5090/.remote_sha256.txt`
(basenames) — that is how the 144/144 was established.

## Built this session (pre-unblind, synthetic data only)

- **`che/scripts/p6_post_analysis.py`** + `test_p6_post_analysis.py`: the
  reading instrument for EVALFLOOR, Γ(t), Γ₄/B̂, Γ_H and T = 2000. Refuses
  without a non-empty `unblind/UNBLIND_LOG.txt`; refuses Γ(t) without the eval
  floor; re-derives Γ and refuses if it moved since `unblind.json`; logs every
  real run to `POST_UNBLIND_LOG.txt`. Computes no branch.

## THE UNBLIND — sequence, and what the owner must rule first

1. ~~Wait for the §7 blocks~~ — DONE 2026-09-26: both pulled, verified, committed.
2. **Owner ratifies, BEFORE the run, SIX builder interpretations**: (i)–(iii)
   in the 2026-09-23 entry, (iv)–(vi) in the 2026-09-26 entry. Also decides
   the optional §5 of the 2026-09-26 entry (re-evaluate the 144 T\* = 1000
   checkpoints on unit 2 too) — **before the unblind or not at all**, and the
   k = 72 primary designation stands unless reversed now.
3. On a **clean tree**, with the owner present:

       uv run python -m che.scripts.p6_unblind \
         --artifact che/bench/results/phase6/g1_conf_5090 \
         --floors   che/bench/results/phase6/g1_floors_5090/floors.json \
         --card-diag che/bench/results/phase6/g1_grid \
         --out      che/bench/results/phase6/unblind --unblind
       uv run python -m che.scripts.p6_post_analysis --sections gamma4 t2000

   Read the branch from `unblind/report.md`; open the matching
   `paper/branch_*.md`.
4. Ship `unblind/UNBLIND_LOG.txt` to the box (same relative path), run
   `run_p6_post_unblind_evals.sh` in tmux (set `GAMMA_T_STEPS` per the §5
   decision), pull `post_gamma_t/`, `post_high/`, `post_evalfloor/`, then
   `p6_post_analysis --sections evalfloor gamma_t high`.
5. Archive, then release the box. Correct the `no-element` header line of
   `p6_iso.yaml` (§7 OWED item 5); keep the ten configs otherwise identical.

## The paper (unchanged since 2026-09-24)

`paper/tex/` — TMLR style + drafted sections, **not yet compiled**
(`~/.local/bin/tectonic`). Still owed: **numbers ledger**
(`paper/numbers_ledger.md`), **bibliography verification**
(`paper/related_work_verification.md`; a fabricated citation is a desk
reject), Def. 2 reword into the theory doc, the two arXiv PDFs, TMLR
time-to-decision, "ambient", the card-2 partial re-floor owner entry. §7 OWED
items 2 and 3 look undone: no 2026-09-18 amendment in `phase6_design_v2.md`
§2, and no "no severity has both couplings strongly live" line in
`paper/00_common_spine.md` beside §4a.

## Working agreements (unchanged)

Rulings bind only once transcribed. Numbers enter documents derived or
measured. Bars come with floors — per-metric, per-hardware, per-artifact.
Contrasts graded on the contrast's SE. Instruments state what they are blind
to. Run the CPU suite chunked and thread-capped (and never `pkill -f pytest`
from a shell whose own command line contains "pytest" — it kills itself and
leaves the old run alive). Do not tail training logs on the box beyond
progress lines; never compute a cross-arm mean on the box.
