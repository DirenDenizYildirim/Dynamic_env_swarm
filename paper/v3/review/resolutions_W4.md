# Resolutions — writer W4 (fix round, step 4.3, 2026-10-14)

Files: `sections/06_example_design.md`, `07_example_results.md`,
`16_appendix_timeline.md`, `18_appendix_secondary.md`, their provenance files,
and `ledger_proposals/W4.md`. Line numbers are the live files after this
round. Every changed sentence's provenance row says "fix round: <ID>".

Checks rerun after the edits:
- `provenance_check.py --root paper/v3 --strict` on the four files: OK
  (35/35, 48/48, 154/154, 45/45 rows; 0 support problems).
- `v3_checks.py terms`, `dates` and `caveats`: PASS (39 caveat entries, 0
  failing).
- `build_v3.py`: no failure in these files.

Word counts (`wordcount.py`, prose):

| file | prose | budget |
|---|---|---|
| §6.1–6.2 | 500 (was 595) | 500 |
| §6.3 | 477 (was 550) | 480 |
| App. D | 1,993 (595 of them verbatim quotations) | about 1,000 + quotations |
| App. F | 467 | about 400 |

Captions: §6.1–6.2 has 57 caption words, of which Figure 6 is about 49 (cap
50). §6.3 has 196, two 8-word print-companion captions included, so Figures 7
and 8 have about 105 and 75 words against a cap of 60 each. The overage is the
required label glosses; RM-10 added two more.

| finding | outcome | what changed (file:line) | reason |
|---|---|---|---|
| RC2-1 (MUST) | FIXED | 06:56 | Removed "so little beyond Coupling A was under test", which is the professor's phrase. It now reads "so the test point may have offered little composition". The registration is now credited only with the Coupling-B half, quoting PFB:252-253 verbatim. "A post hoc interaction check measures this (§6.4)" no longer pre-judges the check. RC2-1's wording was shortened to fit RM-1. C01 and C34 still pass. |
| RC2-3 (MUST) | FIXED | 16:54 | The record column now reads "the floor study's own record (results directory)". The log has no entry for this study; DX-36 says that entry is still owed. |
| RC2-4 (MUST), App. D part | FIXED | 16:38 | D.1 now says the reader can compare the quoted registration text with the shipped documents, and that the manifest shows only that the archive arrived unaltered. It names the quotations that come from the dated log and says they cannot be checked against the supplement unless log excerpts ship. |
| RC2-4, §8 part | NOT MINE: W5 | — | `11_using_che.md:46`. |
| RC2-9 / RC1-14, §6.3 part; RN2-2 | FIXED | 07:58 (two sentences) | "On completion both gaps are null, so Γ₄ is a second exclusion bound, the registration's term for its detection limit, X₄ = 4.88 points". The registered string stays verbatim, and X₄ is named as a detection limit (BRIEF §9.2 trap 5). |
| RC2-9 / RC1-14, §5 part | NOT MINE: W3 | — | `05_measurement.md` (definition of "exclusion bound"). |
| RC2-11 | FIXED | 16:51 | The 2026-08-11 row now records that the convergence check was retired (METH-6; log:2940-2955), which Appendices B and C point to. |
| RC2-12 (OWNER) | FIXED (after the full-history check) | 16:38; 16:39 (marker); ledger_proposals/W4.md X4-6 | The orchestrator unshallowed the checkout, and I re-read each date with `git log --follow --diff-filter=A`. D.1's shallow-clone sentence is replaced by the variant for a completed check. It gives the commit dates: the frozen design was first committed 2026-08-02 and last changed 2026-08-13, the outcome framings were committed 2026-08-13 and never changed after, the first provenance file of the main runs 2026-09-09, the confirmatory hash file 2026-09-23 and the unblinding log 2026-09-26. The sentence keeps the limit: these are self-reported commit dates in a private repository, set by the committer's clock, not externally timestamped. No hash appears in the text. The new row is X4-6. The V3Q16 marker stays for the supplement half (log excerpts, content hashes). Correction to the orchestrator's note: the design's last change is 2026-08-13 23:58 (the dated amendment), not 2026-08-02 15:14. |
| RC2-13 | FIXED | 18:18, :30, :48 | "GPU 1" becomes "the GPU that ran Γ", and "GPU 2" becomes "second GPU". Numbered GPUs now appear only in D.6. |
| RC2-14, §6.3 part (with RN1-4) | FIXED | 07:62 | "appears only in the last fifth" becomes "detectable only in the last fifth". The precise checkpoints (900, 950, 1000) stay in the Γ(t) paragraph (07:60). |
| RC2-14 / RN1-4, abstract and §1 parts | NOT MINE: W1 | — | `00_abstract.md:41`, `01_introduction.md:47`. |
| RC2-15 | NOT MINE: W1, W3 | — | The fix trims §1 and §4.3. The full statement stays at its home, 06:56, as RC2-1 rewrote it. |
| RC2-16 | FIXED | 06:60 | Unblinding's second definition was removed: "a recorded deviation made before unblinding". The definition stays at its first use in §1. |
| RC2-17 | FIXED | 16:91, :94, :97 | Row A's addition is now in square brackets. Row D is rendered as registered: "− (either)", survival cell empty. A note under the table explains both. |
| RN2-1 (OWNER) | OWNER | 16:181-182 (marker); provenance/16 row 147 | "615 of 615" is kept. An OWNER-PENDING:F1 marker was added (DISPOSITIONS §5 F1; this item has no V3Q id). The provenance row again records the inconsistency: the report's table sums to 636, and `m62b/SHA256_CKPT.txt` has 18 lines where the table says 16. The untagged 2026-09-27 is now tagged DX-408. |
| RN2-3 | FIXED | 06:56; 07:80; 16:38, :58, :157; 18:44 | Tags added to my files' untagged numbers: "three-seed" (CB-9); "60-seed" (DES-1); "2000-update" (RES-15) in D.1, D.2 and D.6; "eight" (DX-28). Inside quotations, for consistency with the tagged 2.2365: "All 11" (DES-13) and "144" (DES-3; 2 × 72) at 16:141 and :145. |
| RN2-5 | FIXED | 16:178 | The G1.2 key row now names the floor-study protocol: the launch study of 2026-08-10, the re-measurement of 2026-09-08, and the RTX 5090 re-measurement (phase6_report.md:65, :68; log:4617). |
| RN2-7 (a) | FIXED | ledger_proposals/W4.md, X4-3 | Added `che/eval/harness.py:40, :45` (`_FINAL`, the value at the last step) to the identity's support. |
| RN2-7 (b) | FIXED | provenance/16 rows 130, 133, 137 | PFB:73 corrected to PFB:71. |
| RN2-7 (c) | NOT MINE: orchestrator | — | IC-4's PLAN line. |
| RM-1 (MUST), my part | FIXED | 06 and 07, throughout | §6.1–6.2 cut from 595 to 500 words, §6.3 from 550 to 477, both within budget. No registered string, honesty line or caveat home was cut; each cut is named in its provenance row. Cut from §6.3: the PFB:15-16 quotation in §6.1, the lead sentences, "70 % of the budget", the linearity pointer (the check is in App. F), the headline quotation (it is in App. D.3), and the B̂ value (it is in Table 3). |
| RM-10 | FIXED | 07:49 | The Figure 7 caption now glosses the printed "m" and "n" in the exact gloss form. |
| RM-11 | FIXED | 06:62; 07:41, :43, :58 | $p$, $\nu$ and $p = 0$ are now typeset as math in the prose. The captions keep Unicode, since they are raw HTML. |
| RM-12 | FIXED | 16:38 | D.1 now says the design review is also not shipped. |

Counts: FIXED 20, OWNER 1, NOT MINE 5 (part-findings counted once per row),
DECLINED 0.

## Final pass (step 4.3, last round, 2026-10-16)

| finding | outcome | what changed (file:line) | reason |
|---|---|---|---|
| RN2-8 | FIXED | 16:38; ledger_proposals/W4.md X4-6 | D.1 now gives the time zone: "(dates in the committer's local time, UTC+3)". Row X4-6 records that the design's first commit, 2026-08-02 01:10 +0300, is 2026-08-01 22:10 UTC, and that the other four dates fall on the same day in UTC. |
| RC2-22 | FIXED | 06:56 | (a) "calibrated survival effect" is now "survival effect in calibration". (b) "here" is now "at Medium"; the PFB quotation is unchanged. |
| RM-19 | FIXED | 16:94, :97 | Row D's survival cell now reads "[− (either)]". The square brackets mark our addition, so the registered row stays verbatim. This also respects RC2-17. The note now says the registered table writes "− (either)" once, under completion. |
| RM-1 (REOPEN), my part: captions | FIXED | 07:49, :80; 07:43, :56 | Figure 7 and Figure 8 captions are now 60 words each, at the cap and down from about 105 and 75. The m/n gloss and "the figure prints rates" moved into the sentences that introduce the figures. The banned-term glosses (knee, dose slope, no-element share, sweep_c50_p000, rung, unit 1, cross-unit, floor basis) stay in the captions, because the terms check exempts a gloss only inside a caption. Figure 6 is about 49 words (cap 50). |
| RM-1, prose | — | 06, 07 | Prose stays within budget: §6.1–6.2 has 499 words (budget 500) and §6.3 has 479 (budget 480). The words the moved glosses and RC2-22 added were offset by small rewordings, each recorded in its provenance row. |

Checks: `provenance_check.py --root paper/v3 --strict` on the four files is OK
(35/35, 47/47, 156/156, 45/45). `v3_checks.py` terms, dates and caveats all
PASS.
