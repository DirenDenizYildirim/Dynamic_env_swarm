# Pre-submission checklist

Compiled 2026-09-07 from the repository review of that date plus the
standing owed items in `HANDOFF.md` and `docs/decision_log.md`. Ordered by
how badly each one could hurt the submission.

## Defects found 2026-09-07 (not previously recorded anywhere in the tree)

- [ ] **Definition 2 wording vs the death penalty.** Def. 2 (amended
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

- [ ] **Bibliography verified by hand.** Every `[VERIFY]` in the spine:
      VULCAN, Agrawal 2023, Erdem & Üre 2025, SMART (RA-L 2026). Relays
      have twice named documents that do not exist. A fabricated citation
      is a desk reject.
- [ ] Read the JaxWildfire PDF (arXiv:2512.06102) and arXiv:2604.26150
      directly; the related-work rows currently rest on automated
      summaries.
- [ ] Read arXiv:2507.10142 for a subsuming memorization-gap theorem.
- [ ] **Write the UED / domain-randomization related-work paragraph after
      a real search.** No search has been run. PLR, ACCEL, PAIRED, DR.
- [ ] IEEE Xplore query (needs authenticated access).
- [ ] Ratify the word "ambient" (pending since 2026-08-05).
- [ ] Obtain TMLR's actual time-to-decision from published statistics or
      OpenReview before writing any runway arithmetic.
- [ ] Per-artifact floors for the two render-gate drift channels from the
      grid's own seeds, via their own post-grid instrument; until then the
      channels grade nothing and the paper says so.
- [ ] The endogeneity family is cited by member name, never by ordinal.

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

## Post-unblind, before writing §9

- [ ] Identify the branch from the registered table, apply the falsifier
      for B, apply the Γ(t) reading rule for the suffix and for D.
- [ ] Realized power against the motivating effect band, reported not
      re-engineered.
- [ ] Delete the three unused branch files from the submission tree; keep
      them in the repo.
