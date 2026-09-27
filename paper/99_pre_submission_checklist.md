# Pre-submission checklist

Compiled 2026-09-07 from the repository review of that date plus the
standing owed items in `HANDOFF.md` and `docs/decision_log.md`. Ordered by
how badly each one could hurt the submission.

## Defects found 2026-09-07 (not previously recorded anywhere in the tree)

- [x] **DONE 2026-09-27 (DEF. 2 WORDING RULING, Option 2)**: clause 1
      reworded, hazard-blind note + cause-blindness test added, README,
      spine and CLAUDE.md updated. Still owed: carry the note and the scoped
      ablation into `submission.md` when porting. Original defect:
      **Definition 2 wording vs the death penalty.** Def. 2 (amended
      2026-08-05) says "no shaping term" and "survival is learned solely
      because death truncates future task return". Every training config
      carries `death_penalty: 0.5`, applied per newly disabled agent at
      `che/env/env.py:349`, and Phase 2 measured it decisive at High
      (survival 0.575 → 0.866). The reward-independence test varies hazard
      only in a far corner where it cannot kill, so it tests "no direct
      read of h", not the sentence. **Reword Def. 2** (spine §3), report
      the dp = 0 ablation, and update `README.md` item 1 which repeats the
      "solely" claim. Transcribe the reword into `docs/decision_log.md`
      first; it is a theory-doc change.
- [ ] **Unrecorded card-2 re-floor runs.** `che/bench/results/phase6/
      _box_pull/g1_floors_card2/` holds 8 ISO + 4 JOINT re-floor runs
      dated 2026-08-14, one archive a third the size of the others, and
      no decision-log entry, report, or HANDOFF line mentions the rental.
      Record it: what card, what happened, why it stopped at 12, whether
      the truncated archive lists. Under the artifact-persistence rule
      this needs an entry before the grid runs.
- [ ] **"Certified inert" → "inert under a frozen random-projection encoder
      at this scale".** The message head receives no gradient by design.
      Soften everywhere the certification language appears in the paper.
      (Spine abstract and §7 heading softened 2026-09-27; still owed in
      `submission.md` when it is written.)
- [ ] **Drop "swarm" as a claim.** The foraging task requires no
      coordination; twelve shared-parameter agents with a team reward.
      "Multi-agent" in the title; "swarm" only where it names the
      homogeneity assumption.

## Owed before the grid

- [ ] Rule on the four pre-unblind proposals. Recommended: adopt 0 ($0,
      register ISO's inert third as inflating Γ) and 1 ($3.41, ISO-4
      control arm). Decline 2 and 3 unless the reserve allows.
- [ ] G1.2 re-floor on the grid card (~$4.08) before G1.3.
- [ ] `cards.txt` block structure recorded if more than one card runs.

## Owed before submission, independent of the grid

- [x] **Relayed citations resolved** (2026-09-26, abstract-level, four
      identities re-checked independently): VULCAN, Agrawal 2023, Erdem & Üre
      2025 repositioned; SMART removed (CITATION REPOSITIONING RULING).
- [ ] **Still owed by hand:** read Gao et al. RSS 2024, Chen et al. ICLR
      2022, and Erdem & Üre 2025 in full (does it match exposure?); build the
      `.bib` only from the BibTeX in `paper/related_work_verification.md`,
      never from memory.
- [ ] Read the JaxWildfire PDF (arXiv:2512.06102) and arXiv:2604.26150
      directly; the related-work rows currently rest on automated
      summaries.
- [ ] Read arXiv:2507.10142 for a subsuming memorization-gap theorem.
- [ ] **Write the UED / domain-randomization related-work paragraph** from
      the DRAFT in `paper/related_work_verification.md` Part 2 (search run
      2026-09-26; no scoop found).
- [ ] IEEE Xplore query (needs authenticated access).
- [ ] Ratify the word "ambient" (pending since 2026-08-05).
- [ ] Obtain TMLR's actual time-to-decision from published statistics or
      OpenReview before writing any runway arithmetic.
- [ ] Per-artifact floors for the two render-gate drift channels from the
      grid's own seeds, via their own post-grid instrument; until then the
      channels grade nothing and the paper says so.
- [ ] The endogeneity family is cited by member name, never by ordinal.
- [x] **`paper/numbers_ledger.md` built (2026-09-27).** Every number in
      `submission.md` carries a ledger row ID, and new numbers get a row
      first.
- [ ] **Ledger O-1 (owner): PBT.** No reported run used PBT. Every run is
      single-policy IPPO. Decide the wording; `README.md:28` and the
      `CLAUDE.md` project description still say PBT hybrid.
- [ ] **Ledger O-2:** a committed artifact for β̂_c's R_L logistic
      centres, or restate §4 with the committed estimator.
- [ ] **Ledger O-3:** measure the real supplement size (`git archive`); the
      454 KB figure is from 2026-08-04.
- [ ] **Ledger O-4 (owner):** confirm TMLR's supplement limit on its own
      page.

## TMLR mechanics

- [ ] Double-blind: no repo, OSF or registration links; no commit hashes
      that resolve to an account; pre-registration described in-text by
      date. Anonymized supplementary code ≤ 100 MB (ship 454 KB, not
      `m06/`).
- [ ] No parallel submission anywhere archival. DMLR is sequential fallback
      only.
- [ ] Length justified by content; use the appendix manifest (spine §11).
- [ ] Every figure readable in greyscale; floor bars on every bar chart
      that has a floor.

## Beyond PDF format (SUBMISSION FORMAT RULING, 2026-09-27)

- [x] Owner: author kit + Docker ALLOWED (addendum, 2026-09-27); the owner
      runs the download and the Docker install. Kit read in full before use.
- [x] Owner: `paper/tex/` FROZEN as the DMLR-fallback source (addendum).
- [ ] `render_episode.py` checked on Phase-6 checkpoints (last touched
      2026-07-30, before the traced-theta refactor).
- [ ] `authors` anonymous in `submission.md`; every interactive figure
      self-contained (no author-linked URL, font or data source).
- [ ] Every GIF has a static companion or a caption that carries it, so the
      browser-printed PDF stands alone.
- [ ] GIFs illustrate recorded behaviour and grade nothing; any claim is made
      in the text with its floor.
- [ ] No acceptance-rate figure anywhere: the advice behind the ruling is
      advice, and no statistics are published.

## Post-unblind, before writing §9

- [x] Identify the branch from the registered table, apply the falsifier
      for B (2026-09-26: branch B, 3.855 < 4.433); Γ(t) suffix (2026-09-27):
      "sign unstable over the final half" on both co-primaries.
- [x] Realized power against the motivating effect band, reported not
      re-engineered (completion 71.6 % at k = 72, 60.2 % at k = 60).
- [x] **DONE 2026-09-27 (branch-B splice):** abstract and §9 at k = 72 with
      the k = 60 prefix and the 40 → 46 → 72 history stated as a deviation;
      DBCA moved to the sweep (§1, §9.1) and the endpoint confound stated in
      §2; the counter's scope added (§6). "Rare and bursty" was measured on
      single-configuration A+B runs (the κ_B = 1.0 rows of Phase-4 Result 4),
      not on mixtures, so it stands. The splice also found and fixed
      "hazard-free" in `branch_B.md`: those episodes are fire-only (D1).
      Original item: **Branch-B carry-overs into the spine (2026-09-26):** abstract and §9
      say k = 40 — the realized primary is k = 72 (k = 60 prefix beside it);
      ~~the abstract's "…learned only through the task return"~~ (reworded
      2026-09-27, DEF. 2 WORDING RULING); the DBCA sentence belongs
      to the sweep (ENDPOINT CONFOUND entry); the invariant-#5 "co-active"
      counter is co-active only in all-on configurations (SECONDARY RESULT) —
      qualify every use, including tier-1 "rare and bursty" if it was
      measured on mixtures.
- [x] `branch_B.md` slots filled from the post-unblind stage (2026-09-27): Γ(t)
      suffix, Γ_H exclusions, eval floor, cross-card check.
- [ ] Delete the three unused branch files from the submission tree; keep
      them in the repo.
