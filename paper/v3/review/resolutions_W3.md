# Resolutions — W3 (fix round, step 4.3)

Writer W3, 2026-10-14. Files: `sections/02_related_work.md`, `04_calibration.md`,
`05_measurement.md`, `15_appendix_floors.md` and their provenance files. I read
all five reviews of snapshot `draft1` (RC1, RC2, RM, RN1, RN2) in full. Below is
one row per finding that touches these files. Line numbers are the live
`paper/v3/sections/` files after this round. Draft1's text is in
`paper/v3/snapshots/draft1/sections/`, and the provenance rows quote it ("fix
round: <ID>").

**Checks after this round:**
- `provenance_check.py --root paper/v3 --strict` on the four files: OK.
  - §2: 22 sentences and 22 rows. §4: 56 and 56. §5: 12 and 12. App. C: 62 and 62.
  - No unsourced sentences, no stale rows, no support problems.
- `v3_checks.py terms`, `dates` and `caveats`: all PASS.
  - My caveat homes each occur once: C02, C03, C31–C35 and C36.
  - C39's short form is still in Figure 3's caption.

**Word counts** (prose, `wordcount.py`):

| file | words | budget | draft1 |
|---|---|---|---|
| §2 | 400 | 400 | 420 |
| §4 | 700 | 700 | 770 |
| §5 | 269 | 270 | 302 |
| App. C | 641 | about 500 (the appendix is not capped) | 590 |

- §2's Table 1 has 119 words in its cells, against a cap of 120.
- §4's captions total 210 words, each figure at or under 60 counting the hidden `interact` span:
  - Figure 3: 58;
  - Figure 4: 59;
  - Figure 5: 60, including its include caption.
- App. C grew because it now holds §4.4's content checks (RM-1).

| finding | outcome | what changed (file:line) | reason |
|---|---|---|---|
| RM-1 (MUST) | FIXED (my part) | §2 cut to 400 words, §4 to 700 and §5 to 269; Figure 4 caption shortened (04:75). Cuts: §2's Agrawal / Tramèr / Hsiung sentence and some shortening; §4.4's content-checks sentence, moved to App. C (15:40); §4.3's High completion sentence (CB-8) and RC2-15's sentence; §5's floor-coverage sentence, whose content App. C carries | Every main-text file of mine is now at or under its STRUCTURE §3 budget. Each cut is one the provenance files named, or a repetition. No registered string, honesty line or caveat home was cut. The page count is measured on the whole paper; that is not mine to re-run |
| RC1-18 (SHOULD) | FIXED | as RM-1 | Budgets met. RC1-11 and RC1-13 were applied, with equal-length cuts as RC1-18 asks |
| RC1-11 (SHOULD) | FIXED | 04:98, now two sentences | Draft1's one sentence read as if the value clause were Pynadath & Tambe's result. Their result is now stated as a complexity result (RWV:978, Thm 4). Remark 2′(i)'s conditions are taken from TF:486-495 (interchangeable, expendable, at least as numerous as the hypotheses; value returns when any of them fails). The team-any reward condition is left to App. A, for budget. Remains OWNER-PENDING V3Q4 |
| RC1-12 (SHOULD) | FIXED | 02:28 | "proposed" restored (RWV:967: VULCAN itself is not evaluated) |
| RC1-13 (SHOULD) | FIXED | 02:35, the Gao sentence | The strategy comparison is restored in short form, so "cycling through factors" is defined. OWNER-PENDING v2C1 kept |
| RC1-14 (SHOULD) | FIXED (my part) | 05:36, the exclusion-bound definition | Now: "each end is an exclusion bound in its direction: … a gain larger than the upper end and a loss larger than the lower end, and the larger absolute end bounds the effect's size". This fits the registered "excludes a joint-training gain larger than 0.66 points" (the upper end of [−4.12, +0.66], RES-1), and App. G's "\|I\| < B". The registered sentence is unchanged. The second part (saying in §6.3 that the registered "second exclusion bound", X₄, is a detection limit) is NOT MINE: it belongs to W4 |
| RC2-9 (SHOULD) | FIXED (my part) | 05:36 | Same fix as RC1-14. Giving Γ₄'s gain bound in §6.3 belongs to W4 |
| RC2-11 (SHOULD) | FIXED (my part) | 15:46, "(Appendix D)" dropped | App. D does not record the retirement of the convergence check. Fixing App. D.2's 2026-08-11 row belongs to W4 |
| RC2-15 (SHOULD) | FIXED (my part) | 04:86, the last sentence of §4.3 cut | It was a third statement of the siting caveat. Trimming §1's short form belongs to W1 |
| RC2-1 (MUST), part (d) | NOT MINE: W4 | none | The tension is in §6.1 (06:56), and the fix is W4's. §4.4's "in effect, Coupling A with Coupling B" (04:98) is registered honesty line 4 (`branch_B.md:177`), so it stays |
| RN1-2 (SHOULD) | FIXED | 04:69 | "(from unrounded counts)" restored, since 4.05 / 0.84 gives 4.82 (CA-4 note) |
| RN1-5 (SHOULD) | FIXED | 15:39 | "four thresholds were set on constants the record later called invented". M5.3b measured its floor first (V5-1 note) |
| RN1-6 (SHOULD) | FIXED (my rows) | 04:48 ($L = 64$, DX-7); 04:54 ("64-cell", DX-7); 04:92 ("two-seed", DX-40); 15:54 ("1000 updates", DX-34) | Tags added. The `03_environment.md:104` row belongs to W2 |
| RN2-5 (SHOULD) | FIXED (my part) | 15:30, "(G1.2)" changed to "(G1.2 protocol)" | G1.2 names the floor protocol (log:4617; V5-3), which the two re-measurement rows also used. The App. D key belongs to W4 |
| RC1 readability 9 | FIXED | 02:35, the DBCA clause | "atom/compound distributions" changed to "similar distributions of single elements and different distributions of their combinations" (RWV:253-273) |
| RC1 readability 10 | FIXED | 02:35, the Erdem & Üre second sentence | Reworded inside RWV:974 and :1061-1069 (no scheduled clean steps; runs attacked on both modalities carry both budgets) |
| RC1 readability 14 | FIXED | 04:69, 04:84 | "coupled arm" replaced by "with Coupling B on" and "with masking on" |
| RC1 readability 15 | FIXED | 04:46 | "committed with the calibration data" changed to "shipped with the calibration data". C31's phrase "no committed estimator" stays in its home sentence |
| RC1 readability 16 | FIXED | 05:28 | The floor definition's parenthesis now defines "artifact" (the same code, configuration and seed) |
| RC1 readability 17 | FIXED | 05:38 | "A recorded channel" changed to "A logged diagnostic"; "registered analysis family" changed to "registered family of tests" |
| RC1 readability 18 | FIXED | as RC1-13 | |
| RC1-23 (OWNER) | OWNER (V3Q4) | none; the `OWNER-PENDING:V3Q4` marker stays at 04:98 | The name "Remark 2′" is part of V3Q4. Not decided here. App. A's naming belongs to W2 |
| RM-4, RM-5 (SHOULD) | NOT MINE: W2 | none | Statement numbering and App. A's remark heading. §4.4 uses the name App. A gives |
| RM-OWNER-3 (OWNER) | OWNER (V3Q8, V3Q11) | none | Printed figure legibility covers my Figures 3, 4, 5 and C1. Rebuilds or print-size companions are the owner's choice; captions and glosses are unchanged |
| RM-3 (SHOULD) | NOT MINE: W2 | none | Corollary 1's omitted items need a note in App. A. §4.1 states Corollary 1's items 1 and 4 in words and points to App. A |

**Counts:** FIXED 20 (7 of them fixed in part, with the rest belonging to another writer); NOT MINE 3; OWNER 2; DECLINED 0.

**Owner-pending markers in my files, unchanged:**
- `v2C1` ×3 in §2;
- `v2D2` in §4.1;
- `V3Q14` and `V3Q4` in §4.4.

DISPOSITIONS §5 still gives v2 C1 and D2 no V3Q number; this was reported in step 4.1.

## Final pass (re-check of snapshot fix2)

I read the "Re-check (fix2)" sections of RC1, RC2, RN1, RN2 and RM. None of my fix-round items was reopened: RC1-11, -12 and -14 are OK, as are RC2-9, RN1-2, -5 and -6, and RN2-5.

| finding | outcome | what changed (file:line) | reason |
|---|---|---|---|
| RC1-28 (SHOULD) | FIXED | 05:28, new sentence "Not every comparison has a floor (Appendix C)." | The fix round's cut had left the rule stated universally (BRIEF §8.1). The sentence is offset by shortenings elsewhere in §5, all with meaning unchanged, which keeps §5 at 270/270 |
| RC1-31, §2 part (SHOULD) | FIXED | 02:37 "…none found by the search of Appendix I."; 02:31 "Our search found no …" | "that search" pointed two paragraphs back. The §1 part is W1's |
| RC2-20 (SHOULD) | FIXED | 05:36, new sentence "The registration also calls its detection limit X an exclusion bound (§6.3)." | Connects §5's interval-end definition to the registered wording for X and X₄. The registered sentence in §6.3 (W4) is unchanged |
| RM-1 re-check: captions at their caps | FIXED (my part) | 04:60 (Fig. 3), 04:75 (Fig. 4), 04:92 (Fig. 5) | §4 captions are 210 → 180, each figure ≤ 60 words with its print-companion caption: Fig. 3 51 + 9, Fig. 4 51 + 9, Fig. 5 47 + 13. All glosses stay in their captions (the terms check exempts glosses only there). No prose cut beyond offsetting the two new §5 sentences. No figure moved |

**Word counts:**
- §2: 399 of 400.
- §4: 700 of 700.
- §5: 270 of 270.
- App. C: 641, unchanged. Its Figure C1 caption (138 words) is in the appendix and has no cap.

**Checks:**
- `provenance_check.py --root paper/v3 --strict` on the four files: OK.
- `v3_checks.py` terms, dates and caveats: all PASS.
