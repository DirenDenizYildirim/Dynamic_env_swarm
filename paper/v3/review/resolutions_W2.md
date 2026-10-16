# Resolutions — writer W2 (fix round, step 4.3)

Writer W2, 2026-10-14. Files: `sections/03_environment.md`,
`sections/13_appendix_proofs.md` and both alternates,
`sections/14_appendix_locks.md`, their provenance files, and
`ledger_proposals/W2.md`. Line numbers are in the post-fix files. I read all
five reviews (RC1, RC2, RM, RN1, RN2) in full; RN2 has no finding on my files.
Pre-fix copies of my files are in the scratchpad (`W2/pre_fix/`) and in
`snapshots/draft1/`.

After the fix: §3 prose is **1,040** words (budget 1,050; draft1 1,129).
App. A is 2,345 (draft1 2,087), App. B 376 (about 350; draft1 294); the
appendix is not capped. Checks I reran: `provenance_check.py --root paper/v3
--strict` on my five files (0 without a row, 0 stale, 0 support problems);
`v3_checks.py` terms, dates and caveats (all PASS); `build_v3.py`, plus
`--alt thm1_tf` and `--alt no_prop4` (build OK, listings 6/6 identical, 0
unresolved cross-references, 0 M1 flags in my files).

| finding | sev | outcome | what changed (file:line) | reason |
|---|---|---|---|---|
| RC1-1 | MUST | FIXED | 14_appendix_locks.md:19 | v2's "or" restored: "checks each against the configurations, the code defaults or the analysis scripts that must carry it". d_p's code default is 0.0 (`che/env/config.py:37`; ENV-1) |
| RC1-2 | MUST | FIXED | 03_environment.md:187 (Table 2) | The listing cell is now "3 (Appendix A)", the step listing, whose comms call reads no h′, ρ′ or c′ (`che/env/env.py:352-358`). I added no encoder row: no test asserts the `stop_gradient` (grep of `che/tests/` for `stop_gradient`: none), and the table is at its page cost |
| RC2-10 | SHOULD | FIXED | as RC1-2 | the same finding |
| RM-2 | MUST | FIXED | 13_appendix_proofs.md:52 | v2's two departures are restored nearly word for word: Def. 5 (impulse per event against a per-cell uniform; v2 05:42) and Def. 7 (range-dependent link probability against a hard Chebyshev range; v2 07:35). I placed them in RM-2's fallback location, a "definitions as implemented" paragraph at the head of Appendix A, because RM-1 forbids adding words to §3. App. A's promise ("the departure is noted", :50) now holds for every definition |
| RM-1 | MUST | FIXED (my part) | 03_environment.md (whole); 13_appendix_proofs.md:132-171; 14_appendix_locks.md:67 | §3 is cut to 1,040 words, under its 1,050 budget, which is 89 below draft1. The cuts: (a) Listings 2 and 4 (23 code lines) move to Appendix A as Listings 4 and 5, which RM proposes and no stub line forbids; Table 2 and two pointers carry them, and listings are renumbered in reading order (1–2 in §3, 3–5 in App. A, 6 in App. B); no other file cites a listing number. (b) The d_p ablation's scope and its other settings move to App. B, the cut P/03 named, so §3 keeps only the High survival pair as the evidence for caveat C29. (c) CA-9's clause and the message-head sentence go. (d) Smaller merges are listed in the provenance rows. No caveat home, honesty line or registered string was cut. The page count is the orchestrator's to remeasure after all writers |
| RM-3 | SHOULD | FIXED | 13_appendix_proofs.md:52, :188 | Def. 1's post-step observation and Def. 3's smoke update with fixed ι = 0 are noted in the departures paragraph. One sentence after Cor. 1 says TF's items 2 and 3 are omitted and item 4 is numbered 2 |
| RM-4 | SHOULD | FIXED | 13_appendix_proofs.md:52 | One sentence explains that statements keep the theory document's numbers, which the docstrings cite. It sits in App. A, not §3, because of the page ceiling |
| RM-5 | SHOULD | FIXED | 13_appendix_proofs.md:229 | "Remark 2′ (Value of communication). Extend the corridor toy of Theorem 1 with a second agent; §4.4 refers to this remark." The same change is in both alternates |
| RM-OWNER-1 | OWNER | OWNER (V3Q16) | 13_appendix_proofs.md:50 | Whether the theory document ships is not mine to decide. The `<!-- OWNER-PENDING:V3Q16 -->` marker is in place. If it does not ship, the departures paragraph and the departure notes at Props. 1 and 3, Thm. 1 and the transfer remark need another referent |
| RC1-10 | SHOULD | FIXED | 03_environment.md:195 | Now reads "Every trained policy, and every evaluation of one, uses one instance" |
| RC1-15 | SHOULD | FIXED | 03_environment.md:165 | Now reads "a death by fire or by collapse changes the reward by $-d_p$" |
| RC1-18 | SHOULD | FIXED (my part) | §3 | §3 is now 1,040, against 1,050. §2, §4 and §5 are W3's |
| RC1-19 | SHOULD | OWNER (V3Q4) | none | TF's Remark 2′(ii) itself writes "with slack ℓ_f … (equality iff ℓ_f = 0)" (`docs/theory_foundations.md:497-501`), and the record does not say whether this slack is a separate quantity or follows from the fire depth in the courier variant. Renaming the symbol would decide part of V3Q4 (the ℓ_f clash, P3-20). The V3Q4 marker stays |
| RC1-20 | SHOULD | FIXED | 13_appendix_proofs.md:227 (and the thm1_tf alternate) | Now reads "The measured value of the policy the proof shows optimal (if informed, take the corridor other than Z; else a fixed one) matches ½ + ½q …" (`phase4_report.md:52-55`; `e2c.py:240-241`) |
| RC1-21 | SHOULD | FIXED | 03_environment.md:177 | Now reads "Propositions 2 and 3, Corollary 1 and Theorem 1 are exact results that the code is tested against …" |
| RC1-23 | OWNER | OWNER (V3Q4) | none | The "Remark 2′" name is kept. App. A now explains the numbering (RM-4), and the V3Q4 marker is in place |
| RC1 readability 11 | — | DECLINED | none | The rewrite is about 15 words longer, and §3 is at its page budget. The current sentence states the same quantity (half the probability of being informed before committing) |
| RC1 readability 12 | — | FIXED | 03_environment.md:167; 14_appendix_locks.md:67 | The five-qualifier parenthesis left §3. App. B says "seeds per setting", not "per cell" |
| RC2-11 | SHOULD | FIXED (my part) | 14_appendix_locks.md:47 | The pointer "(Appendix D)" is dropped. The cell says the check was "retired when the estimand was fixed at a matched budget, before the main training runs" (METH-6). Adding the retirement to App. D's 2026-08-11 row is W4's part |
| RN1-1 | SHOULD | FIXED | 14_appendix_locks.md:67 | The ablation's scope now lives in App. B and says it "reports training-log means over the final updates" (`phase2_report.md:35`) |
| RN1-6 | SHOULD | FIXED (my row) | 03_environment.md:104 | "two" is tagged DX-304. The other rows in that table are W3's |
| RN1-7 | SHOULD | FIXED | ledger_proposals/W2.md:15 (X2-2) | The note now says that 1.60653 and 1.97441 come from Def. 6 arithmetic, and that the printed 1.607 and 1.974 give 0.89832 and 0.98700, so the three-decimal values are unaffected |
| RC1-7, RC1-8, RC1-9, RC1-17 and others in 00/01 | — | NOT MINE: W1 | — | — |
| RC1-11, RC1-12, RC1-13, RC1-14, RN1-2, RN1-3, RN1-5 | — | NOT MINE: W1 or W3 | — | — |
| RM-6 to RM-16, RM-OWNER-2 to RM-OWNER-4, RC2 except RC2-10 and RC2-11, RN2-* | — | NOT MINE (W1, W3, W4, W5, the supplement builder or the orchestrator) | — | — |
