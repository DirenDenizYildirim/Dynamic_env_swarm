# HANDOFF — session state for the next model (rewritten 2026-09-27; updated 2026-09-28; v3 pointers 2026-10-12, 2026-10-16)

> **Start here (2026-10-16).** Paper v3 phase 1 is handed back on branch
> `claude/fervent-newton-ws5yub`. Read `paper/v3/HANDBACK.md` and the one-page
> `paper/v3/OWNER_QUESTIONS.md`. Two things wait on the owner: the OK on the
> interaction-check plan (`che/bench/results/phase6/post_v3_interaction/PLAN.md`,
> committed) and the GPU run (`RUNBOOK.md` there). After the results return, a
> session verifies them, runs `che.scripts.interaction_analysis` once, fills
> the 7 `HOLE:INTERACTION` markers, Figure 9 and the IC rows, and rebuilds.
> Nothing from v3 is in `paper/finale.md` until the owner rules.
>
> **Start here (2026-10-12).** The next paper session is the **v3 rewrite**.
> Paste `paper_v3_prompt.md` as its first message. That prompt is
> self-contained and supersedes the older pointers below for paper work.
>
> **The rulings.** The rulings it rests on are the decision log's
> *DEMONSTRATION DRAFT* and *PAPER V2* (2026-10-11) and *PAPER V3*
> (2026-10-12). *PAPER V3* adopts a professor's review and switches to an
> environment-first framing. It authorizes one eval-only interaction check,
> whose scope is still OPEN. It defers ISO-4 at 2000 updates, and the code
> ships.
>
> **The v2 output.** Paper v2 phase 1 is complete in `paper/v2/` (commit
> `f744ae2`). Start with `paper/v2/HANDBACK.md` and
> `paper/v2/OWNER_QUESTIONS.md`.
>
> **No GPU box exists.** The interaction check needs the owner to rent one
> and restore the checkpoint archives.

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
  gitignored and not on GitHub. The first three renders (random, ISO s1,
  JOINT s1 at θ\*) are done and committed at `paper/renders/2026-09-27/`
  with their selection rule. `render_episode.py` works on Phase-6
  checkpoints unchanged. Any further render needs the laptop.
- **Backup, in progress.** All Phase-6 archives were re-verified against
  their committed hashes on 2026-09-27 (`phase6_report.md` §3). A second
  copy was built that day at `~/che_backup_2026-09-27/`:
  `che_results_2026-09-27.tar` (all of `che/bench/results/` +
  `phase2_results/`, 10,353 entries, sha256 `fd7f31df…b5fda402`) and a git
  bundle at `2f1e386` (sha256 `af00b53f…aa8b8699`); full hashes in its
  `SHA256SUMS.txt`. **The owner is uploading it to their cloud server;
  once confirmed, record it in `phase6_report.md` §3.** `main` was pushed to
  GitHub the same day.

- **Demonstration draft (2026-10-11, uncommitted on the owner's word).**
  Under the decision log's *DEMONSTRATION DRAFT* ruling, a builder-written
  Beyond PDF demonstration of the whole body is in `paper/demo_beyond/`
  (read its `README.md`; reviews in `REVIEW.md`, including six OWNER ITEMS
  the reviews found in the owner's text and the record). Private artifact:
  https://claude.ai/artifact/541rk1RcCKs1trTe64Y4aX . `paper/finale.md` is
  untouched, and *WRITING ROLES* still governs it.
- **Paper v2 (2026-10-11, PAPER V2 ruling).** Builder subagents draft the paper
  from the demonstration scaffold; the owner checks every word. *WRITING ROLES*
  is superseded for v2, and the title and abstract are reopened. Start a v2
  session by pasting `paper_v2_prompt.md`, which carries the owner's fix list
  with verified locations and TMLR's LLM policy (disclosure footnote on the
  first page).

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
4. **Beyond PDF scaffold: MERGED** by the owner 2026-09-28 (PR #1,
   `e2d1618`; built in a web session 2026-09-27, one commit per milestone
   S0–S5). **Reviewed 2026-09-28, no defect found.** Checked independently:
   no change under `che/`, `docs/`, `pyproject.toml`, `uv.lock` or
   `paper/tex/`. The abstract is word-for-word the spine's (one declared
   line-break join). All 14 ledger IDs point at the right rows. The bib is
   the 37 source entries, exactly. The assets match the renders' hashes.
   The GIFs carry only loop and frame-timing blocks, and the PNGs no text
   chunks. The remote branch `claude/cool-cori-dg8c4u` can be deleted
   (owner).
   **Writing starts 2026-09-28 under the WRITING ROLES ruling:** the owner
   writes **`paper/finale.md`** (later copied to `submission.md`); the
   builder supplies numbers (ledger ID + source + scope), constraints,
   choices and questions, then checks, and writes no paper text. **Every
   writing session starts from `writing_session_prompt.md`.** Step 1, the
   title, is **DONE 2026-10-10** (TITLE AND TERMINOLOGY RULINGS) and is in
   `paper/finale.md`. Step 2, the **Abstract, is DONE 2026-10-10**
   (ABSTRACT entry): a body section, the environment named in full. Step
   3, **`description`, is DONE 2026-10-10** (DESCRIPTION entry): one
   owner-written sentence. Step 4, **§1 Introduction, is DONE 2026-10-10**
   (§1 INTRODUCTION entry). Step 5, **§2 Related work, is DONE 2026-10-10**
   (READS RULING entry; the recorded full reads discharge the owner reads).
   **SESSION END 2026-10-10. Start here next time.** The owner will decide,
   fresh, whether to restart the paper beyond the §1 rewrite; the builder's
   delegated call (decision log, OPENING AND §1 REOPENED) is: keep the title,
   abstract and `description`; hero explorer under the abstract; §1 rewritten
   figure-led (composer + compact Γ/Γ₄ ladder); §2 kept. **The §1 rewrite step
   is prepared** (session record); its essentials: the three opening figures
   and their ledger rows (ENV-13, DES-7/8/14/16, RES-1/2/6, DES-13/15);
   §2 depends on §1 twice ("§1 stated what our comparison holds fixed"; the
   3× endpoint confound "(§1, §9)"); the old §1 text is reusable from
   `paper/writing_drafts.md`. **Review page** (private artifact, every figure
   live, in reading order): https://claude.ai/artifact/HkpD3sho2QhJLdnX8BKveS .
   **Uncommitted** at session end (the owner commits only on their word): the
   OPENING entry, ledger rows DES-16/ENV-13/RES-6, and the interactive set's
   B8/B10 fixes, compact ladder and lint cleanup. Before that: **Writing resumes at §3, figure-first** (FIGURE BATCH RULINGS, 2026-10-10:
   the figure-led path of `paper/figures/interactive/DESIGN.md` §5 is adopted
   within the current structure; §1–§2 stay). §3 is prepared; ask its open
   questions again (formal depth, PBT, where the hyperparameters go). **Owed
   figure work:** the B8 presentation fixes (composer "as certified"; Γ(t)
   descriptive label; slot labels if used); deterministic selection rules,
   then the §5/§6 explorer deep links; ledger rows for every number in the
   figures kept (C13; lists in `paper/figures/MANIFEST.md` and
   `paper/figures/interactive/MANIFEST.md`).
   **Lint debt (2026-10-10):** `ruff check` is clean on `paper/figures/src/`
   and `paper/renders/2026-10-10/src/`, but reports 813 findings in
   `paper/figures/interactive/src/` (792 E501 long lines, mostly embedded
   JS/CSS/HTML strings; 13 B905; 6 B023 loop-variable closures, worth a look;
   2 B007). The outputs were verified independently; fix with the B8 rebuild. Owed from §1: §9.2
   reports γ_n *and* where the plane fit fails (γ_p vs Γ₄); a verified
   CMDP / safe-RL entry. Drafts are typed in chat and kept verbatim in
   `paper/writing_drafts.md` (DRAFTS FILE, 2026-10-06).
   **The spine abstract (builder text) still carries lags**, verified
   2026-10-10 and avoided by the owner's abstract: it omits the completion
   lean; its Γ(t) suffix names one contrast, not both co-primaries; "every
   acceptance bar is graded against a measured floor" is contradicted by
   CB-9 and by `e11_report.md:113-121`; β̂_c is O-2 open; "a secondary dose
   design attributes the gap" overreaches (non-verdict-bearing, γ_p
   positive); k = 72 is not called a deviation. "Not behaviourally
   suppressible" is in the post-correction headline too
   (`phase4_report.md:647-648`); its problem is scope (trained policies at
   500 updates), not the correction.
   - **Built.** `paper/beyond_pdf/` in the kit's layout:
     - `KIT_NOTES.md` covers the kit (URL and sha256; no version or licence
       stated), its YAML fields, how bib and assets resolve, the preview
       and its image, every external URL (all kit-level, none author-tied)
       and the conflicts.
     - `submission.md` is the skeleton: the abstract verbatim with ledger
       IDs, sections in spine order, figure slots 1–10 naming their data,
       and GIF slots.
     - `assets/` holds the three renders and their static PNGs,
       byte-identical to `paper/renders/2026-09-27/`.
     - `submission.bib` holds the 37 verified entries, verbatim.
   - **No kit file is in the tree.** The preview and the upload are staged
     in a scratch copy of the kit (`KIT_NOTES.md` §S1.8).
   - **S4 preview FAILED at the Docker step:** the web container has no
     Docker daemon, and starting it was refused by the session's permission
     classifier. Static checks passed, including the bib through the kit's
     own Distill parser (37/37). **Interim preview (owner, 2026-09-28):** an
     HTML/CSS artifact that mimics the style. It is a writing aid, not the
     kit's build, so the kit preview (`KIT_NOTES.md` §S4, route (a) laptop
     Docker or (c) web editor) is still owed before upload.
   - **Owner decisions the scaffold raised** (proposals until transcribed),
     with the builder's recommendation from the 2026-09-28 review:
     - ~~what `description` carries~~ **RULED 2026-10-10** (DESCRIPTION
       entry): one owner-written sentence; it restates the abstract's
       opening, so look again once a kit preview runs.
     - ~~the title~~ **RULED 2026-10-10** (TITLE AND TERMINOLOGY
       RULINGS), in `paper/finale.md`.
     - whether to show the ISO/JOINT GIFs at all (in `assets/`, not
       placed). Recommended: not in the main text. One episode each differs
       by 2 of 12 agents against a +0.96-point effect; an appendix with the
       required caption at most.
     - whether to touch the 8 bib fields that render raw LaTeX.
       Recommended: fix them in `related_work_verification.md` (Unicode
       characters), then re-copy, so the bib stays verbatim.
     - rubygems.org and the Debian mirrors: moot unless the preview runs in
       the web container (route b).
   - `CLAUDE.md`'s layout block lists `paper/beyond_pdf/`, `paper/renders/`
     and `paper/numbers_ledger.md` (refreshed 2026-09-28).
   **`paper/tex/` is FROZEN** as the DMLR-fallback source (addendum,
   2026-09-27). It does not compile (`main.tex` inputs sections 02, 04–07 and
   `references.bib`, none of which exist); do not develop it.
5. **Builder item still owed from the §7 ruling (2026-09-18):** item 2's
   first half, the dated amendment to `phase6_design_v2.md` §2 carrying
   proposal 0's four points. The spine halves were done in the splice
   (2026-09-27): proposal 0 is in spine §9.1 bias (a), and the "no severity
   has both couplings strongly live" line is in spine §10 item 1, the §4a
   limitation. (Item 5, the ISO config header, was done 2026-09-27.)
6. **Bibliography: reads DISCHARGED 2026-10-10** (READS RULING;
   `related_work_verification.md` Part 3; `submission.bib` now 40 entries).
   Was, for the owner to read by hand: Gao et al. RSS 2024, Chen et al. ICLR 2022, Erdem & Üre 2025 (in full: does it match exposure?),
   the JaxWildfire PDF, arXiv:2604.26150, arXiv:2507.10142. The `.bib` is
   **built** (item 4 branch: `paper/beyond_pdf/assets/bibliography/
   submission.bib`, verbatim from `paper/related_work_verification.md`,
   those six entries `%`-flagged); no entry is ever written from memory.
   Then write the UED/DR paragraph from its Part 2 draft.
7. **Owner decisions:**
   - ~~Batched figure decisions~~ **RULED 2026-10-10** (FIGURE BATCH
     RULINGS: all accepted). Was: the
     restyled GIFs (`paper/renders/2026-10-10/`): keep `provenance/` or fold
     it into `src/`; policy labels on the GIFs (with GIF slot 2, whether ISO
     and JOINT appear at all); when the restyle replaces the 2026-09-27 files
     in `assets/`. Plus whatever the slot-figure agent (`paper/figures/`) and
     the Opus design agent (`paper/figures/interactive/DESIGN.md`) raise, and
     §3's four questions. Also open: the theory-doc ρ amendment; a commit
     checkpoint.
   - ~~ratify "ambient"~~ **DONE 2026-10-10**: Def. 2 is the "ambient
     hazard"; "stressor" names only the composable elements;
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
   - **repository private before upload** (REPO VISIBILITY, 2026-10-10):
     the owner switches it; the builder verifies with an unauthenticated
     request (404 expected).
   - **comment stripping before upload** (decision log, WRITING ROLES,
     OWED). `assets/` and the page source are public during review, so the
     bib's `%` notes and `submission.md`'s ledger/TODO comments would ship
     as they stand. Builder's proposal: strip them when staging into
     `submission_folder/`, and keep them in the repository copy.

After submission: the follow-up is the separate `Expendable_swarm` repo.

## Working agreements

**Writing roles (2026-09-28, WRITING ROLES):** the owner writes the paper;
the builder gives numbers with ledger ID, source and scope, plus labelled
suggestions, never paper text or placement. Rulings bind only once
transcribed. Numbers enter documents derived or
measured. Bars come with floors — per-metric, per-hardware, per-artifact.
Contrasts graded on the contrast's SE. Instruments state what they are blind
to. Run the CPU suite chunked and thread-capped (and never `pkill -f pytest`
from a shell whose own command line contains "pytest" — it kills itself and
leaves the old run alive). TMLR is double-blind: no repo links, OSF links or
account-resolving commit hashes in anything that ships.
