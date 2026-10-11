# Review record: the demonstration draft (2026-10-11)

DEMONSTRATION DRAFT ruling, item 5. This file indexes the reviews; the
findings themselves are in `review/`.

## Process

1. **Brief.** The keeper read `writing_session_prompt.md` and the record and
   wrote `BRIEF.md`, the 40 supplement rows DX-1 … DX-40, and the "no source"
   list (BRIEF §E).
2. **Draft.** Four writers worked in parallel, one file set each (W1 §0–§2,
   W2 §3–§4, W3 §5–§8, W4 §9–§12). Rows they needed were verified at their
   source first.
3. **Review.** Three independent reviews, each in its own lane:
   - claims (the keeper, by `writing_session_prompt.md` step-4 categories):
     `review/claims.md`;
   - numbers (every tag against its row and the row's source):
     `review/numbers.md`;
   - mechanics (kit syntax, listings, theory fidelity, cross-references,
     double-blind): `review/mechanics.md`.
4. **Fix round.** The writers fixed their own files under
   `review/DECISIONS.md`, recording each finding's outcome in
   `review/resolutions_W1.md` … `W4.md`. The change is
   `review/fix_round.diff`.
5. **Re-check** of the changed lines only, by the numbers auditor and the
   keeper (each review file's "Fix-round re-check" section). The orchestrator
   fixed the last items (below) and consolidated the writers' rows into
   `ledger_supplement.md`.

## Tallies

| review | findings | MUST | SHOULD | NOTE | outcome |
|---|---|---|---|---|---|
| claims | 34 | 4 | 8 | 22 | 34 of 34 pass the re-check; all 4 MUST closed |
| numbers | 26 | 1 | 10 | 15 | 25 fixed, 1 skipped as definitional (accepted); no tagged value was wrong in either pass (788 tags in round 1, 832 after the fixes) |
| mechanics | 42 | 1 | 16 | 25 | MUST closed; listings byte-identical to the repository (6 of 6); no double-blind leak |
| re-check, claims | 5 | 0 | 1 | 4 | all fixed by the orchestrator (below) |
| re-check, numbers | 4 | 0 | 0 | 4 | all fixed by the orchestrator (below) |

## The MUST items and how they closed

- **C-1:** §1 said the 4.8-fold fall was "registered before that
  measurement". The keeper's brief had the timing wrong, and the brief was
  corrected. §1 and §5 now say what the record supports: the fuel limitation
  was recorded at the Coupling-A lock from the random-policy calibration,
  before any trained policy.
- **C-8 / C-32 / M-1:** Prop. 1's proof. The smoke field is real-valued, so
  the state space is not finite. §3 and App. A now share one argument: the
  states reachable within the horizon are finite, and the model restricted
  to them is a finite Dec-POMDP. App. A says that this departs from the
  theory doc.
- **C-22:** the Fig. 11 status labels. Γ₄ is the sensitivity arm, Γ₄′ is
  secondary (S5), and B̂ is a registered estimand with no test.
- **N-1:** §8 called M5.5's 20 % threshold "registered". It was chosen at
  implementation (log:1170-1171).

## Last items, fixed by the orchestrator after the re-check

- **C-R1 (SHOULD):** §7 restated 2σ bars as exclusions ("the null excludes
  effects larger than …"), and took a 27 % bound from the VOID condition.
  Each bound is now stated as a bar, a post-hoc floor grading at about 50 %
  power (§8.2). The VOID-derived bound is dropped.
- **C-R2:** §5 now says that what the lock recorded before training was the
  fuel limitation (2026-07-21), not the trained fall.
- **C-R3:** §3 and App. A now name the restriction to reachable states
  before using the finite-model argument, in identical words.
- **C-R4:** B̂ is labelled a registered estimand (2026-09-18) with no test.
- **C-R5:** DECISIONS item 9 is corrected to the ledger rule (a new number
  gets a verified row first, or is cut).
- **N-R1:** DX-417 added (DERIVED: the +2.69-point completion plane
  prediction, with γ_p's interval).
- **N-R2 / N-R3:** four untagged repeats tagged (CA-7, DES-1, DES-13,
  DES-14).
- **N-R4:** DX-415 merged into DX-306, its duplicate.

## What the reviews did not check

- **No kit build ran** (KIT_NOTES §S4). The preview imitates the kit's CSS.
  The kit's MathJax configuration, its `_styles` handling and its
  print-companion behaviour are unverified.
- **The claims review is a read against the record** by the agent that
  wrote the brief. It is independent of the writers, but not of the brief,
  and one error in the brief (C-1) reached a draft before the review
  caught it.
- **Lengths run over the brief's targets** (§3 ≈ 2,660, §9 ≈ 3,350 prose
  words; the appendix ≈ 5,470). The keeper's named cuts were applied, and
  no further cut was made.

## OWNER ITEMS

Found by the reviews in the owner's own text or in the record. The
demonstration edits none of these.

1. **Abstract and §1:** "As predicted before measurement" (CA-4) overreaches
   mildly. The trained-policy ordering was already on record before the
   E1.1 prediction (`e11_report.md:170-197`). What was recorded before any
   trained policy is the lock's fuel limitation (`coupling_a_lock.md:82-90`).
   (`paper/finale.md:13, :159-160`)
2. **Theory doc, Prop. 1:** the proof still says S and Ω are finite
   (`docs/theory_foundations.md:151-153`), and Def. 1's observation line
   (:62-63) is stale. The owner's §1 phrase "finite Dec-POMDP" inherits both.
   HANDOFF's "theory-doc ρ amendment" item is out of date.
3. **§2, Erdem & Üre:** "every arm is perturbed throughout"
   (`finale.md:310-311`) is inaccurate. The Non-Robust baseline is
   unattacked.
4. **§2:** "about seven percent" (`finale.md:217-218`) reads as about eight
   if it is meant as an increase (CA-9: 7.4–8.3 %).
5. **`CLAUDE.md:344` and log:1194** say M5.3's floor came from "different
   hardware". Both provenance files record an RTX 5090. Nobody edited
   `CLAUDE.md`.
6. **`phase4_report.md:366`** ("a sixth to a quarter") contradicts its own
   table, and the ceiling claim at :394-395 holds only for the κ_B = 1.0
   arm.
