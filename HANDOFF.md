# HANDOFF — session state for the next model (rewritten 2026-09-27)

**Phase 6 is CLOSED. This is the writing phase.** Read, in order:

1. `docs/decision_log.md` from **UNBLIND RESULT** (2026-09-26) to the end.
   That tail is the law; this file only points at it.
2. `che/bench/results/phase6/phase6_report.md`: the closing index (result
   table, milestones, artifacts, what is graded and what is only recorded).
3. `paper/branch_B.md`: the landed branch, filled with measured numbers.
4. `paper/99_pre_submission_checklist.md`: everything owed before submission.

## Where things stand

- **Branch B**, with the registered inert-share qualifier: survival Γ
  +0.0096 (z 4.43), completion null; Γ₄ ≈ 0, so the survival effect is
  **exposure, not composition**, and the abstract must say so. Γ(t) suffix:
  "sign unstable over the final half" on both co-primaries. High readout:
  exclusions. Evals reproduce bit-for-bit across cards.
- **No GPU spend, and none to propose** (owner, 2026-09-26). Every remaining
  analysis is $0 on committed per-episode `eval_*.npz` files.
- **GPU boxes: none.** Unit 1 is gone (vast.ai re-rented it); units 2 and 3
  were destroyed by the owner (unit 3 confirmed 2026-09-27). Nothing lived
  only on any of them.
- **Format: TMLR Beyond PDF** (SUBMISSION FORMAT RULING, 2026-09-27): a
  Markdown/HTML article with GIFs and interactive figures, submitted on
  OpenReview. The venue pair (TMLR, then DMLR) is unchanged. Addendum, same
  day: author kit + Docker ALLOWED (the owner runs the download and the
  install; the classifier refuses the download from the session), and
  `paper/tex/` FROZEN as the DMLR fallback. **The scaffolding moves to a
  Claude Code web session** (decision log, *SCAFFOLDING SITE*, 2026-09-27).
  Its container has Docker, and its default network reaches GitHub, PyPI
  and Docker Hub. The session follows `beyond_pdf_scaffold_prompt.md`
  (kit notes, skeleton, bib, preview) and pushes a branch for the owner to
  review. The local `pacman -Syu` + Docker route is now only the fallback.
  **GIFs of trained policies stay a laptop job:** the checkpoints are
  gitignored and not on GitHub. Still owed by the builder, locally: check
  `render_episode.py` on Phase-6 checkpoints, then render the GIFs.
- **Backup, in progress.** All Phase-6 archives were re-verified against
  their committed hashes on 2026-09-27 (`phase6_report.md` §3). A second
  copy was built that day at `~/che_backup_2026-09-27/`:
  `che_results_2026-09-27.tar` (all of `che/bench/results/` +
  `phase2_results/`, 10,353 entries, sha256 `fd7f31df…b5fda402`) and a git
  bundle at `2f1e386` (sha256 `af00b53f…aa8b8699`); full hashes in its
  `SHA256SUMS.txt`. **The owner is uploading it to their cloud server;
  once confirmed, record it in `phase6_report.md` §3.** `main` was pushed to
  GitHub the same day.

## Next, in order

1. ~~Definition 2 wording~~ **DONE 2026-09-27** (DEF. 2 WORDING RULING,
   Option 2): the reward is hazard-blind, prices deaths whatever their cause
   (new `test_death_penalty_is_cause_blind`), and "no shaping term" /
   "solely" are struck. When porting, carry the hazard-blind note and the
   Phase-2 d_p ablation **with its scope** into `submission.md`.
2. ~~Splice branch B into the spine~~ **DONE 2026-09-27.** The spine
   (`paper/00_common_spine.md`) now carries the branch-B abstract, §9.1
   design at k = 72 (the 40 → 46 → 72 history stated as a deviation),
   §9.2 results, the DBCA sentence moved to the sweep, the §2
   endpoint-confound bullet, the counter's scope note (§6) and the actual
   hardware blocks (§10 item 8). "Rare and bursty" was measured on
   single-config A+B runs, not mixtures, so it stands. **Fixed on the way:**
   `branch_B.md` said "hazard-free episodes", but under D1 the δ-only
   episodes are **fire-only**. The spine is the source the Beyond PDF
   `submission.md` is ported from.
3. ~~`paper/numbers_ledger.md`~~ **BUILT 2026-09-27.** Every spine number
   and all 14 tex `\todo{verify}` values have a row naming their committed
   source, each checked against it this session. Building it found errors
   in the spine, now **FIXED**:
   - "PBT population 12": no reported run used PBT.
   - Def.-4 refutation labelled M3.5; it is M3.0, and survival only.
   - Two Prop.-3 runs merged into one.
   - Ignition figures attributed to m35; they are m44.
   - The High Coupling-B effect led with −8.8; lead with the correction's
     3/3 replication.
   - Bias (b) quoted launch-batch drift as general; **its sign reverses on
     the grid card**.
   - An untested "curriculum difficulty" hypothesis stated as a finding.

   **Four ledger OPEN items:**
   - **O-1 (owner): PBT framing.** `README.md:28` and the `CLAUDE.md`
     project description still say training is a PBT hybrid.
   - **O-2 (builder, $0 CPU, owner go-ahead):** a committed artifact for
     β̂_c's R_L logistic centres.
   - **O-3 (builder):** re-measure the supplement size with `git archive`.
   - **O-4 (owner):** confirm TMLR's 100 MB limit on the venue page.
4. **Beyond PDF scaffolding runs in a Claude Code web session** following
   `beyond_pdf_scaffold_prompt.md` (S0–S5). If a pushed `paper/beyond_pdf/`
   branch exists, review it before starting new paper work.
   **`paper/tex/` is FROZEN** as the DMLR-fallback source (addendum,
   2026-09-27). It does not compile (`main.tex` inputs sections 02, 04–07 and
   `references.bib`, none of which exist); do not develop it.
5. **Builder item still owed from the §7 ruling (2026-09-18):** item 2's
   first half, the dated amendment to `phase6_design_v2.md` §2 carrying
   proposal 0's four points. The spine halves were done in the splice
   (2026-09-27): proposal 0 is in spine §9.1 bias (a), and the "no severity
   has both couplings strongly live" line is in spine §10 item 1, the §4a
   limitation. (Item 5, the ISO config header, was done 2026-09-27.)
6. **Bibliography**, for the owner to read by hand: Gao et al. RSS 2024,
   Chen et al. ICLR 2022, Erdem & Üre 2025 (in full: does it match exposure?),
   the JaxWildfire PDF, arXiv:2604.26150, arXiv:2507.10142. Build the `.bib`
   **only** from the BibTeX in `paper/related_work_verification.md`. Then
   write the UED/DR paragraph from its Part 2 draft.
7. **Owner decisions:**
   - ratify "ambient" (pending since 2026-08-05);
   - TMLR's actual time-to-decision;
   - whether to run the optional $0 analyses (eval-draw sensitivity,
     floor-graded mechanism channels, pooled ISO-4 + sweep_p000). Any of these
     must be built on synthetic data before reading and labelled exploratory;
   - floors for the render-gate drift channels, or the paper says they grade
     nothing;
   - **the card-2 entry**. `g1_floors_card2/` (2026-08-14) still has no
     decision-log entry. New fact from 2026-09-27: its `SHA256_CKPT.txt`
     holds **one** hash (rep1, which verifies); the other 11 archives were
     never hashed, and rep2 is truncated. It grades nothing either way.

After submission: the follow-up is the separate `Expendable_swarm` repo.

## Working agreements (unchanged)

Rulings bind only once transcribed. Numbers enter documents derived or
measured. Bars come with floors — per-metric, per-hardware, per-artifact.
Contrasts graded on the contrast's SE. Instruments state what they are blind
to. Run the CPU suite chunked and thread-capped (and never `pkill -f pytest`
from a shell whose own command line contains "pytest" — it kills itself and
leaves the old run alive). TMLR is double-blind: no repo links, OSF links or
account-resolving commit hashes in anything that ships.
