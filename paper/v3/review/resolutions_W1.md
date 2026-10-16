# Resolutions — W1 (fix round, step 4.3, 2026-10-14)

W1's files: `sections/00_abstract.md`, `00_hero.md`, `01_introduction.md`,
`12_conclusion.md`; `front_matter.yaml` `title` and `description`; their
provenance. Every changed sentence has its provenance row updated with
"Fix round: <finding ID>".

After the fix, with P3's method (`paper/v3/src/wordcount.py`):

| file | draft1 | now | budget |
|---|---|---|---|
| abstract | 250 | 234 | ≤ 250 |
| hero (caption + companion) | 60 | 60 | ≤ 60 |
| hero (reading note) | 30 | 30 | ≤ 30 |
| §1 | 600 | 587 | 600 |
| §9 | 88 | 83 | 90 |

That leaves room for the interaction check's results:
- abstract: up to 16 words;
- §1: 13 words, extending the check sentence in place;
- §9: a 7-word clause.

Checks rerun:
- `provenance_check.py --root paper/v3 --strict` (4 files): OK.
- `v3_checks.py` terms PASS, dates PASS, caveats PASS (39 of 39).

| finding | outcome | what changed (file:line) | reason |
|---|---|---|---|
| RM-1 (MUST) page ceiling | FIXED (W1's part) | abstract 250 → 234 (`00_abstract.md:39-47`); §1 600 → 587 (`01_introduction.md:43-55`); §9 88 → 83 (`12_conclusion.md:19-22`) | room is left for the step-0.5 sentences, as instructed. The other sections' cuts, the listings move and the kit re-measure belong to W2–W5 and B2 |
| RM-OWNER-2 (OWNER) title length | OWNER | `provenance/00_abstract.md`, title table: T5 (60 characters) and T6 (74) added; T1 kept in `front_matter.yaml:17`; `OWNER-PENDING:V3Q1` in place (`00_abstract.md:39`) | V3Q1 is the owner's. T1 prints on 7 lines (RM); T5 and T6 fit the ~75-character guide |
| RM-OWNER-4 (OWNER) date and footnote | OWNER | none; the disclosure slot comment stays at `00_abstract.md:39` | the footnote text is the owner's (PAPER V3 item 6). `date` and `date_confirmed` are not W1's fields (B2 owns them; owner Q2) |
| RM-8 (SHOULD) hole before the check is introduced | FIXED | `01_introduction.md:49`: the separate HOLE slot after the worked-example paragraph is deleted; `HOLE:INTERACTION` now follows the check sentence, with a note to extend it in place | same fix as RC1-9 |
| RC1-3 (SHOULD) "visible" in the last fifth | FIXED | `00_abstract.md:42` | "visible" → "detectable" (RES-11, RES-12) |
| RC1-4 (SHOULD) lesson not connected to the correction | FIXED | `00_abstract.md:42` (correction sentence), `:47` (lesson) | the correction sentence now names the corrected arm and its matched share (DES-14), and the lesson says "that share … matching it". The ruled inert phrase was replaced by "had no detectable effect" (COM-4) to pay for the clause; it is allowed but not required here, and stays whole in §1 and §4.4 |
| RC1-5 (SHOULD) "registered the correction" reads as amending the test | FIXED | `00_abstract.md:42`; `01_introduction.md:47` | "outside the pre-registered test" added in both. In §1, "corrected by an arm" (which implied a repair) is gone |
| RC1-6 (SHOULD) `description` grammar | FIXED | `front_matter.yaml:18` | RC1-6's wording, checked: one line, no `"`, no `: `, no digit, 181 characters, `yaml.safe_load` round trip |
| RC1-7 (SHOULD) "bit for bit" without the keys | FIXED | `00_abstract.md:39`; `01_introduction.md:45` | "under the same random keys" added in both. One backend and the κ_A test's scope stay at §3.4 |
| RC1-8 (SHOULD) CB-9 "not measurable" | FIXED | `01_introduction.md:49` | now "was within a three-seed spread" (CB-9: "within noise") |
| RC1-9 (SHOULD) the check described twice | FIXED | `01_introduction.md:49` | the hole is folded into the check sentence (see RM-8) |
| RC1-16 (SHOULD) "held-out" before it is defined | FIXED | `00_hero.md:21-22` (iframe title, caption); `01_introduction.md:47` | hero: "the test configuration of §6", shorter than RC1-16's proposal so the caption stays at 60 words. §1: "a near-critical configuration neither arm trained on". The abstract keeps "held-out near-critical severity", because it names what is held out |
| RC1-17 (SHOULD) "Both isolated arms … coupling episode" | FIXED | `01_introduction.md:49` | RC1-17's wording |
| RC1-22 (OWNER) siting limitation missing from the abstract | OWNER | `00_abstract.md:41`: marker `OWNER-PENDING:V3Q7 also RC1-22 / RC2-18`; options recorded in `provenance/00_abstract.md` "Holes" | not decided by W1. There is no V3Q id for it, so the marker uses V3Q7 (the abstract's lesson), since RC2-18 suggests carrying it in the post-check lesson. Adding RC1-22's 17 words now would fill the room left for the check |
| RC1-24 (OWNER) "coupled stressors" in the titles | OWNER | title table note; T5 and T6 avoid the phrase | V3Q1. RC1-24's T1′ is not offered: "collapse and smoke feed the hazard" is wrong for smoke, which attenuates perception (Def. 6, `docs/theory_foundations.md:344`) |
| RC1 readability items 1, 3–8 (abstract, §1) | FIXED in part | "percentage points" (`00_abstract.md:42`, `01_introduction.md:47`); the correction split into two sentences in §1 (item 6); item 5 rewritten (RC1-5); items 2, 4 and 8 covered by RC1-4 and RC1-17 | item 3 ("which two differences"): the abstract names both just before, and its gloss was cut for room. Item 7 ("composition" undefined): C01's detection phrase is required at its short form, and §1's first paragraph sets up co-occurrence. Not changed |
| RC2-8 (SHOULD) §9 skips the lesson | FIXED | `12_conclusion.md:19` | option (a): "and §6.5 draws its lesson for how such tests are designed". Option (b) would need a `caveats.yaml` change (B1/B2) |
| RC2-9 (SHOULD) "exclusion bound" defined one way and used another | NOT MINE: belongs to W3 (§5 definition) and W4 (§6.3) | none | the abstract and §1 carry only the registered completion sentence, verbatim. The fix is to §5's definition |
| RC2-14 (SHOULD) two wordings for the survival window | FIXED | `00_abstract.md:42`; `01_introduction.md:47` | one wording in both, "detectable only in the last fifth of training"; §1 adds "(the checkpoints at updates 900 to 1000)". §6.3 is W4's |
| RC2-15 (SHOULD) siting near-full in §1 | FIXED (W1's part) | `01_introduction.md:49` | the pointers reduced to the home "(§6.1)", with RC1-8's shorter wording. The §4.3 cut is W3's |
| RC2-16 (SHOULD) "unblinding" defined twice | FIXED (no change in W1's files) / NOT MINE for 06 | `01_introduction.md:47` keeps the definition at first use | the fix at 06:60 is W4's |
| RC2-18 (OWNER) abstract carries no limitation | OWNER | as RC1-22 | — |
| RN1-3 (SHOULD) CB-9 wording | FIXED | `01_introduction.md:49` | as RC1-8 |
| RN1-4 (SHOULD) RES-12's scope | FIXED | `00_abstract.md:42`; `01_introduction.md:47` | "detectable"; §1 no longer says "of 1000", which read as if every update had been tested, and names the checkpoints instead |
| RN1 "Šidák-corrected 95 %" tagged DES-13 (not re-opened by RN1) | no change | — | RN1 records it as carried from v2 and not a finding |
