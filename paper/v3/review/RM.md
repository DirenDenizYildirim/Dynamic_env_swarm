# RM: mechanics review of Paper v3, draft1

Lane RM (mechanics), step 4.2 of `paper_v3_prompt.md`, 2026-10-14. Reviewed
snapshot `paper/v3/snapshots/draft1/` (sections, `alt/`, provenance), plus
`paper/v3/front_matter.yaml`, `paper/v3/ledger_proposals/W2.md`, the
supplement builder (`paper/v3/supplement/`) and its outputs (`paper/v3/out/`).
`diff -rq` showed `paper/v3/sections` = `snapshots/draft1/sections` and
`paper/v3/provenance` = `snapshots/draft1/provenance` at review time, so the
kit build of `paper/v3` builds the snapshot. Nothing in the repository was
edited except this file. Scratch files are in `scratchpad/RM/`.

## Summary

**Findings: 2 MUST, 14 SHOULD, 4 OWNER.**

MUST:

- **RM-1** The main text is **16.08 printed pages from page 1** (the graded
  default, V3Q2) against the ceiling of 15. It is 14.40 from §1, but the
  interaction-check holes (the result paragraph, Figure 9, and the §1 and §9
  sentences) are still empty.
- **RM-2** Two departures from the theory document that v2 stated (Def. 5:
  per-event impulse against a per-cell uniform; Def. 7: range-dependent link
  probability against a hard Chebyshev range) are no longer stated in v3.

**What passed.**

- **Real-kit build:** ran once, 39 PASS, 2 FAIL (pages; print legibility),
  6 INFO.
- **Source and kit mechanics:**
  - every d-cite key resolves: 33 keys, alternates included;
  - MathJax: 0 errors in 323 expressions;
  - tables: 17 = 17, with 0 prose pipes;
  - cross-references: 252, 0 unresolved, and every target I read is the
    right one;
  - links, iframes, print, listings and leaks: all PASS.
- **Listings:** 8 of 8 listing blocks, alternates included, are
  byte-identical to HEAD and to the working tree.
- **Double-blind:** clean in the text, comments included, and in the staged
  folder, the PDF and the supplement.
- **Theorem 1 (V3-E2):** the default statement matches `che/env/e2c.py`, and
  its departure text is accurate.
- **The supplement:** its full check run finished during this review and
  passed:
  - scrub, size (37.7 MB of a verified 100 MB) and manifest;
  - **598 tests passed, 7 skipped and 0 failed inside the unpacked
    supplement**;
  - the four registered instruments reproduced their committed outputs.

**Scope and method.** I read the following:

- `paper_v3_prompt.md`, in full;
- the decision log from PAPER V2 to the end;
- `BRIEF.md`, `STRUCTURE.md` and the planner notes;
- v2 BRIEF §14 (kit syntax) and `paper/v3/src/README.md`;
- every snapshot section and both alternates;
- TF Defs. 1–8, Props. 1–4, Cor. 1, Thm. 1 and Remark 2′
  (`docs/theory_foundations.md:29-660`);
- `che/env/e2c.py`;
- the interaction-check `PLAN.md`;
- the supplement's README, SHIPPED_README and outputs.

Rule 5 limits what I re-verified. I diffed each v3 formal statement against
v2's (`scratchpad/RM/formal.py`) and checked against TF only what v3
changed. Numbers and claims belong to the other lanes; I flag one only where
it is mechanical.

---

## Checks run (command → result)

From the repository root, `PY=.venv/bin/python`, `S=<scratchpad>/RM`.

| # | command | result |
|---|---|---|
| 1 | `diff -rq paper/v3/sections paper/v3/snapshots/draft1/sections`; the same for `provenance` | no differences: live = snapshot |
| 2 | `PY=$PY paper/v3/src/kit_build.sh --scratch $S/kitscratch --out $S/kitout` (exit 1) | kit sha256 verified; merge 0, Jekyll 0, control 0; **39 PASS, 2 FAIL, 6 INFO** (`$S/kitout/kit_checks.md`); PDF 37 pages, US Letter |
| 3 | the same, `v3_checks.py pages --pdf $S/kitout/submission_v3_print.pdf` and `--grade section1` | from page 1: **16.084, FAIL**; from §1: **14.399, PASS**. Appendices heading at p. 17 y 66; "1 Introduction" at p. 2 y 542 |
| 4 | per-section page positions (`pdftotext -bbox-layout`, the check's method; script inline in this session) | table under RM-1 |
| 5 | `$PY paper/v3/src/build_v3.py --out $S/final --final` | exit 1, final-only items only: 23 STUB-SPEC, `date_confirmed: false`, 7 PENDING IC tags. **0 failures, 0 warnings, 0 M1 flags**; 6 of 6 listings identical; 252 cross-references, 0 unresolved |
| 6 | `$PY paper/v3/src/provenance_check.py --root paper/v3 --strict --out $S/prov` | OK: 25 files (alternates included), every sentence has a row, 0 stale, 0 support problems |
| 7 | `$PY paper/v3/src/bib_diff.py` | PASS, 41 of 41 byte-identical, 0 lint |
| 8 | `$PY -m pytest -p no:cacheprovider paper/v3/src/tests -q` | 14 passed (the v3 checks' negative and positive controls) |
| 9 | `$PY paper/v3/src/wordcount.py paper/v3/snapshots/draft1/sections` | table under RM-1 |
| 10 | d-cite keys of all snapshot files (alternates included) against `paper/v3/assets/bibliography/submission.bib` (inline script) | 33 keys, 0 missing, 0 malformed |
| 11 | listing bodies against `git show HEAD:<path>` and the working tree (inline script) | 8 of 8 blocks byte-identical to both; header lines match the LISTING markers |
| 12 | double-blind grep of all snapshot sections, alternates, provenance, ledger proposals and `front_matter.yaml`, **comments included**: author name parts, the e-mail domain, the repository name, `github.com`, `claude.ai`, session ids, branch names, `/home/`, `/root/`, `/Users/`, `/workspace`, `/tmp/`, IPv4, URLs, e-mails | 0 hits |
| 13 | every 7–40-hex token in the sections and front matter against the 59 commits of `git rev-list --all --reflog` | 0 hits (one hex-like token, `0095531`, is the number 0.0095531 in a comment) |
| 14 | the kit's own double-blind scan of the staged folder and the PDF (in #2) | PASS: url 0, identity 0, abs_path 0, hex 0, image text 0 |
| 15 | TF's statements against v3's, and v2's against v3's (`$S/formal.py`, plus TF read at the cited lines) | RM-2, RM-3, RM-4, RM-5; Thm. 1 below |
| 16 | Thm. 1 arithmetic for d = 2, ℓ_f = 2: q at κ_B = 1 with depths 4, 3, 2, and with 0.707, 0.898, 0.987 | 0.1934 and 0.8116, matching 0.193 (X2-4) and 0.8115 (X2-3) |
| 17 | supplement zip, independently (`python -I`, read in place): identity tokens as in #12, this repository's commit prefixes, `.git`, top-level entries | 4168 files; 0 identity hits; 0 commit hits; no `.git`; one top-level directory, `che_supplement/` |
| 18 | `paper/v3/out/checks_summary.txt` (updated 11:50, after the builder's `run_checks.sh` finished) and `scratchpad/supplement/run1_console.txt` | scrub PASS; size PASS (37,705,078 B against 100 × 10⁶); manifest PASS (4167 of 4167); **tests PASS (605: 598 passed, 7 skipped, 0 failed; 3335.8 s)**; reproduce PASS (8 of 8 outputs identical outside provenance); overall PASS |
| 19 | TMLR quote in the builder's saved page (`scratchpad/supplement/tmlr_author_guide.html`) | "Authors may submit up to 100MB of supplementary material …" and "supplementary material must be anonymized" are present verbatim |
| 20 | `find … -newer paper/v3/out/che_supplement.zip` over `che/`, `docs/`, the registration documents, `pyproject.toml`, `uv.lock` and `LICENSE` | nothing newer: the 10:52 zip holds the current tree, including the interaction configs, scripts and test |
| 21 | the interactive figures' text, searched for printed section, figure, table and appendix numbers (inline script) | none (PNG text not scanned) |
| 22 | §6.4 and App. G against `che/bench/results/phase6/post_v3_interaction/PLAN.md` §1–§8; App. G's refusal text against `che/scripts/interaction_analysis.py:18-26, :95-167` | match, except RM-14 |

---

## Findings

### RM-1 (MUST): main text over the 15-page ceiling under the graded reading

**Location.** The main text, `00_abstract.md` to `12_conclusion.md`;
`front_matter.yaml:17`.

**What is wrong.** On the kit's printed PDF the main text is **16.08 pages**
from the top of page 1 to "Appendices". That is the check's default reading
(V3Q2 default; STRUCTURE §3), and the kit check FAILs (check #2/#3). From §1
it is 14.40.

Both readings are measured with every interaction hole still empty. Still to
come are:

- §6.4's result paragraph and the Figure 9 block with its print companion;
- one sentence in §1;
- one clause in §9.

§6.4 is already over its whole budget without them (0.59 against 0.55
pages; 271 against 200 words). Even the §1 reading has about 0.6 page left
for that text.

**Evidence.** Printed pages per part (check #4), against STRUCTURE §3's
budget, and prose words (check #9, P3's method) against the budget:

| part | pages | budget | prose words | budget |
|---|---|---|---|---|
| title, byline, contents, abstract, hero | 1.69 | 1.55 | 250 + 30 | 250 + 30 |
| §1 | 1.22 | 1.3 | 600 | 600 |
| §2 | 0.97 | 0.9 | 420 | 400 |
| §3 | **3.89** | 3.0 | **1,129** | 1,050 |
| §4 | **2.48** | 2.1 | 770 (captions 213) | 700 (captions ≤ 180) |
| §5 | 0.61 | 0.6 | 302 | 270 |
| §6.1–6.2 | 1.41 | 1.3 | 595 | 500 |
| §6.3 | 1.57 | 1.4 | 550 | 480 |
| §6.4 (holes empty) | 0.59 | 0.55 | 271 | 200 |
| §6.5 | 0.29 | 0.35 | 134 | 150 |
| §7 | 0.50 | 0.45 | 201 | 200 |
| §8 | 0.64 | 0.55 | 313 | 240 |
| §9 | 0.21 | 0.2 | 88 | 90 |
| **total** | **16.08** | 14.25 | **5,653** | ≈ 5,130 |

The title is 118 characters and prints on 7 lines on page 1. v2 BRIEF §14
warns that a title over about 75 characters pushes the abstract down.

The abstract (250 of 250) and §1 (600 of 600) are already at their caps,
before their hole sentences.

**Fix.** Before step 0.5's text lands, cut to the STRUCTURE §3 budgets, a
saving of about 520 prose words:

- §3 by about 80 words;
- §4 by 70 words, with its captions to 60 words each;
- §6.1–6.2 by 95;
- §6.3 by 70;
- §6.4 by 70;
- §8 by 75;
- §5 by 30;
- §2 by 20.

Then free at least another half page:

- move Listings 2 and 4 (23 code lines) to Appendix A, beside Listing 5;
  Table 2 already points to the tests;
- shorten the title (V3Q1; RM-OWNER-2).

Re-run `kit_build.sh` and confirm "from page 1 ≤ 15" with the holes
filled. If the owner rules the §1 reading (V3Q2), the cuts can be smaller,
but the holes still need room.

### RM-2 (MUST): two departures from the theory document, stated in v2, dropped in v3

**Location.**

- `03_environment.md:67-73` (Definition 5);
- `03_environment.md:138-146` (Definition 7);
- `13_appendix_proofs.md:50`, which promises that departures are noted.

**What is wrong.** Both definitions are "as implemented" and depart from TF.

- **Definition 5.** TF Def. 5 (`docs/theory_foundations.md:288-292`) seeds
  per collapse event, "each collapse event at g ignites each Fuel cell in a
  seeding neighborhood N_A(g)". The code draws one uniform per cell
  (Listing 1).
- **Definition 7.** TF Def. 7 (`:563-565`) uses a range-dependent link
  probability p_link(‖x_i − x_j‖)(1 − δ). The code uses a hard Chebyshev
  range.

v2 stated both departures:

- `paper/v2/sections/05_coupling_a.md:42`: "The theory states the impulse per
  collapse event; the implementation draws one uniform per cell, and the two
  rules coincide wherever seeding neighbourhoods do not overlap."
- `paper/v2/sections/07_comms.md:35`: "The theory's range-dependent link
  probability is implemented as this hard Chebyshev range."

v3's condensed definitions dropped both sentences. The theory document now
ships with the supplement (rule D3), so a reader can compare the two and
find the difference unannounced. Appendix A says that "where a statement
departs from the project's theory document …, the departure is noted".

**Fix.** Restore both sentences, at about 45 words in all:

- after `03_environment.md:73`: "The theory document states the impulse per
  collapse event; the implementation draws one uniform per cell, and the two
  rules coincide wherever seeding neighbourhoods do not overlap."
- after `:144`: "The theory document's range-dependent link probability is
  implemented as this hard range."

If page budget forbids it, put both in one short "Definitions as
implemented" paragraph at the head of Appendix A, with the RM-3 items.

### RM-3 (SHOULD): smaller unstated departures from TF in the definitions and Corollary 1

**Location.** `03_environment.md:36-45` (Def. 1), `:49-55` (Def. 3),
`:150-159` (Def. 2); `13_appendix_proofs.md:136-143` (Cor. 1).

**Evidence.**

- **Def. 1.** TF draws the observation as
  O^i_{κ_B}(o_i | x, h, c, k) (`TF:62-64`; that line was not touched by the
  2026-10-10 amendment at `:39-45`). The paper's
  O(· | x′, h′, ρ′, c′, k′) follows the code and CLAUDE.md invariant 2.
- **Def. 3.** It is renamed "Fire and smoke". It carries the smoke update,
  which TF holds in Def. 1's 𝒫 and in Def. 6's amendment. It also fixes
  ι = 0, which TF keeps as a knob, ι ≥ 0 (`TF:173-181`).
- **Cor. 1.** TF has four items (`TF:212-226`). The paper keeps TF items 1
  and 4, numbered 1 and 2, and drops item 2 (subcritical) and item 3
  (critical exponents) without saying so. Prop. 3's note at
  `13_appendix_proofs.md:160` does mention the exponents.
- **Def. 2.** TF's "iff" became "if". This is conventional in a definition
  and needs no note.

**Fix.** Add one sentence after `13_appendix_proofs.md:143`: "The theory
document's Corollary 1 also lists the subcritical regime and the critical
exponents near β_c; the paper uses neither, so they are omitted and its item
4 is numbered 2 here." Put the Def. 1 and Def. 3 notes in the RM-2
paragraph, or leave them, since the paper matches the code.

### RM-4 (SHOULD): statement numbering is not explained

**Location.** `03_environment.md` (Definitions in the order 1, 3, 5, 6, 7,
then 2 at §3.3, then 4 at §4.1); `13_appendix_proofs.md:184` (the only
remark is "Remark 2′").

**What is wrong.** A new reader sees Definition 2 after Definition 7, and a
"Remark 2′" with no Remark 1 or 2. The numbers follow the theory document
and the code's docstrings (CLAUDE.md coding conventions). The paper never
says so.

**Fix.** Add one sentence at the start of §3 or of Appendix A: "Definitions
and results keep the numbers of the project's theory document, which the
code's docstrings cite, so Definition 2 appears in §3.3 and the only remark
is numbered 2′."

### RM-5 (SHOULD): "Remark 2′ (§4.4)" puts a cross-reference where the name goes

**Location.** `13_appendix_proofs.md:184`.

**What is wrong.** Elsewhere the parenthesis after a statement's number holds
its name ("Definition 2 (Ambient hazard)"). Here it holds "§4.4", which reads
as if the remark were called "§4.4".

**Fix.** "**Remark 2′ (Value of communication).** … (used in §4.4)", or
"**Remark 2′.**" with "§4.4 refers to it" at the end of the first sentence.

### RM-6 (SHOULD): §8's commands are not runnable as written inside the supplement

**Location.** `11_using_che.md:37`.

**What is wrong.** The sentence reads: "`uv run pytest -q che/tests` runs
the CPU tests, `python -m che.train.ippo` trains a policy, and
`python -m che.eval.harness` evaluates". After `uv sync`, a bare `python`
is not the project's environment unless the reader activates it. The
shipped README uses `uv run python -m …` throughout
(`paper/v3/supplement/SHIPPED_README.md`, "Reproduce").

**Fix.** "`uv run python -m che.train.ippo` trains a policy, and `uv run
python -m che.eval.harness` evaluates a checkpoint".

### RM-7 (SHOULD): the interaction-check analysis cannot run from the supplement, and neither §8 nor App. G says so

**Location.** `19_appendix_interaction.md:20`; `11_using_che.md:39`.

**What is wrong.** `che/scripts/interaction_analysis.py:95-112` refuses
unless PLAN.md is tracked by git and unchanged since its commit, and
`:157-167` reads `git rev-parse HEAD`. The supplement ships without `.git`,
so the refusal App. G describes is permanent there. A reader with the
supplement cannot recompute I.

This is the supplement builder's finding F2 (`paper/v3/supplement/README.md`,
"Findings for the record"). §8 says the supplement holds "the analysis
scripts with the committed evaluation outputs they read", which a reader
will take to include the check once its results ship (rule R5).

**Fix.** Either the orchestrator adds the no-git mode F2 proposes (PLAN.md's
sha256 against the run's `plan_sha256:`, with the git checks recorded as
skipped) and its command to SHIPPED_README, or §8 adds: "The post hoc
interaction check's analysis also checks the version history of its plan,
so it does not run from the supplement; its outputs ship." Rebuild the
supplement once the step-0.5 results are in, since R5 picks them up.

### RM-8 (SHOULD): §1's interaction hole comes before the sentence that introduces the check

**Location.** `01_introduction.md:49-52`.

**What is wrong.** The HOLE at :49 is to hold "the check's pooled reading in
short form". The next paragraph (:52) then introduces the check: "A post hoc
interaction check measures whether the two couplings' effects … add at the
test configuration (§6.4)." Once filled, the result would come before the
reader learns what the check is.

**Fix.** Move the HOLE marker and its comment to just after the :52
sentence, so that the filled sentence follows it, or fold the result into
that sentence ("A post hoc interaction check at the test configuration …
finds …").

### RM-9 (SHOULD): "eight estimates" (§6.4) against "eight intervals" (App. G, PLAN)

**Location.** `08_interaction_check.md:39`.

**What is wrong.** The family is 4 estimates (three arms and the pool) × 2
co-primaries = 8 intervals (PLAN §5; `19_appendix_interaction.md:26` says
"eight intervals"). "Over eight estimates" miscounts the estimates.

**Fix.** "with Šidák-corrected intervals over eight tests (four estimates,
two co-primaries)".

### RM-10 (SHOULD): Figure 7's printed "m" and "n" are not glossed in its caption

**Location.** `07_example_results.md:49`.

**What is wrong.** The simplex figure prints "m = 0.4", "m = 0.5", "n = 0"
and similar (`paper/figures/interactive/out/html/simplex_secondary.html`).
The gloss ("Figure 7 prints μ as m and ν as n") is only in Appendix F
(`18_appendix_secondary.md:18`). The caption glosses the figure's other
labels in the form V3-S3 requires.

**Fix.** Add to the caption: "per-coupling frequency μ and fire-only share
ν (labelled “m” and “n” on the figure)". The term check exempts that form.

### RM-11 (SHOULD): mixed typesetting of p and ν

**Location.** `06_example_design.md:62` ("and p the co-occurrence");
`07_example_results.md:41, :43` ("p moves from 0 to 0.5", "per unit p",
"per unit ν").

**What is wrong.** The same symbols are TeX elsewhere ($p$, $\mu_A$), so
they print upright here and italic elsewhere. The figure captions must use
Unicode (raw HTML); the prose need not.

**Fix.** Write `$p$` and `$\nu$` in the prose of §6.2 and §6.3.

### RM-12 (SHOULD): Appendix D.1 says only the dated log is unshipped, but the design review is unshipped too

**Location.** `16_appendix_timeline.md:38`, with D.2's record column at :55
("design review; dated log").

**What is wrong.** The 2026-08-16 design review (`docs/venue_review_2026-08-16.md`)
is excluded from the supplement ("venue reviews",
`paper/v3/supplement/README.md`, "What is left out").

**Fix.** "The dated log and the design review are not part of the
supplement by default."

### RM-13 (SHOULD): the supplement README's "Check results" section is empty

**Location.** `paper/v3/supplement/README.md`, the last section ("Filled in
from the run of `run_checks.sh` on 2026-10-14 (see below)", with nothing
below it).

**What is wrong.** The run finished at 11:50 (check #18) and passed, but
the README does not record it.

**Fix.** The supplement builder copies the result into the README:

- the scrub, size, manifest, tests and reproduce lines;
- the 605 / 598 / 7 / 0 counts and the 3335.8 s wall time;
- the seven skips.

### RM-14 (SHOULD): the shipped README says the suite "finishes in minutes"; it took 55.6 minutes here

**Location.** `paper/v3/supplement/SHIPPED_README.md`, "Run the tests
(CPU)".

**What is wrong.** The measured `pytest_wall_s` inside the unpacked
supplement was 3335.8 s (check #18). That run shared the CPU with a kit
build and a repository suite run, so it overstates an idle machine. It is
still far from "minutes".

**Fix.** Measure once on an idle CPU and state that time, or write "takes
up to about an hour on a laptop CPU". No paper sentence states a suite time,
which is correct (BRIEF §17).

### RM-15 (SHOULD): `RUNBOOK.md` ships in the supplement

**Location.** `che_supplement/che/bench/results/phase6/post_v3_interaction/RUNBOOK.md`
(rule R5).

**What is wrong.** It is the orchestrator's operating note to the owner:

- "the owner's runbook";
- "Before you rent (on your laptop)";
- the 2026-09-27 backup;
- a scrubbed `mkdir anonymous_repo` command.

It identifies no one, but it is not code, registration or a paper-number
input. It also shows a one-owner workflow, the reason given for excluding
`CLAUDE.md`.

**Fix.** Exclude `RUNBOOK.md` from R5 (keep `PLAN.md`, which is
hash-pinned), or record the owner's choice to ship it.

### RM-16 (SHOULD): the shipped test output labels the interaction configs "archival"

**Location.** `che/tests/test_locks.py:186-187`, as run inside the
supplement.

**What is wrong.** Three of the seven skips are
`test_beta_is_a_calibrated_severity[che/configs/interaction_*.yaml]:
archival config — pre-Phase-2 placeholder beta by design`. The new configs
have role `interaction_check` (`docs/locks.yaml`, working-tree diff), not
an archival role. The skip message is wrong for them, and a reviewer running
the suite reads it.

Their β is still enforced as `beta_holdout` by the configs' lock map, and
`test_interaction_check.py` asserts the values. So this is a wording defect,
not a coverage gap.

**Fix.** For the orchestrator, with the owner's OK, since it touches an
existing test: add `interaction_check` to `CALIBRATED_ROLES` (β 0.49 is
`beta_holdout`), or make the skip message name the role.

### RM-OWNER-1 (OWNER): App. A and §8 against V3Q16's default, on whether the theory document ships

**Location.** `13_appendix_proofs.md:50` ("`docs/theory_foundations.md` in
the code supplement"; also :56, :160, :176, :200 "the theory document");
`11_using_che.md:39`.

**Evidence.** The supplement builder ships TF and the four lock records by
default (rules D3 and D4; `paper/v3/out/build_summary.json`, D3 1 file and
D4 4 files). DISPOSITIONS V3Q16's default is "supplement's hash manifest
only; 'formal specification' references removed"
(`paper/v3/DISPOSITIONS.md:151`). App. A is right for the current zip and
wrong under V3Q16's default. §8's list of contents omits TF and the lock
records, which the current zip does carry. Both places are marked
OWNER-PENDING:V3Q16.

**Decision needed.** Whether TF and the lock records ship. If they ship, add
"the theory document and the records of how each fixed constant was
measured" to `11_using_che.md:39`. If they do not, App. A's departure notes
must name what they depart from without pointing into the supplement.

### RM-OWNER-2 (OWNER): title length

**Location.** `front_matter.yaml:17`.

**Evidence.** 118 characters; 7 printed lines on page 1 (check #2, page-1
text); see RM-1.

**Decision needed.** V3Q1. A title under about 75 characters saves several
lines on page 1.

### RM-OWNER-3 (OWNER): print legibility, a failing kit check

**Location.** All 13 printed figure images.

**Evidence.** `kit_checks.md`: "13 of 13 printed images fail". Each prints
3.27 in wide, and an 8 pt label comes out at 2.5–4.3 pt. Page 13, rendered
at 80 dpi (`scratchpad/RM/p13-13.png`), confirms that Figures 6 and 7 cannot
be read in print. Step 4.4 requires every check green, and this one cannot
pass without figure work.

**Decision needed.** V3Q8, with V3Q11: print-size companions or label
rebuilds. Otherwise the owner accepts a known FAIL and states it.

### RM-OWNER-4 (OWNER): the date and the footnote, carried

**Location.** `front_matter.yaml:26-31`; `00_abstract.md:39`.

**Evidence.**

- `date: 2026-10-11`, printed in the cite box as "October 11, 2026", is
  v2's date and predates v3. `date_confirmed: false` fails `--final`.
- The kit reports "no <d-footnote> in the source": the disclosure slot is a
  comment, as BRIEF §12 requires.

**Decision needed.** Q2 (date) and the owner's footnote text (PAPER V3
item 6). Neither is an agent's to fill.

---

## Theorem 1 (V3-E2): checked, no finding

- **The statement** (`13_appendix_proofs.md:166-172`) matches the
  implemented toy:
  - reveal probability e^{−κ_B D_t} at the steps t = 0, …, d
    (`che/env/e2c.py:161-215, :273-294`; three steps, `D_PATH + 1`);
  - D_t independent of κ_B, since smoke does not depend on κ_B;
  - per-step draws independent and remembered (`informed |= …`).
- **The proof** uses nothing beyond those three properties, and part (3)
  holds for any D_t > 0.
- **The departure text** (`:176-178`) is accurate:
  - it names TF's special case D_t = d − t + ℓ_f;
  - it says why the toy is not that case;
  - it gives the toy's depths and the two q values (both recomputed, check
    #16);
  - it notes the failure when some D_t = 0.
- **The alternate** (`alt/13_appendix_proofs.thm1_tf.md`) differs only in
  Theorem 1's block and the mismatch note (`diff`), and states plainly that
  the toy does not satisfy the stated signal model.
- **Remark 2′** is v2's statement with "E_{2C}" replaced by "the corridor
  toy". Its q is now the general-D_t q, which is consistent with the toy
  measurements it cites. The ℓ_f clash is already V3Q4.
- **The Prop. 4 remark** (`:198-200`) keeps the honesty note's substance
  (`TF:636-643`) and states its departure.
- **Prop. 1 and Prop. 3** state their departures (`:56`, `:160`).

## Interaction-check holes (rule 4): checked

- **Design text.** `08_interaction_check.md:31-39, :50` and
  `19_appendix_interaction.md:20-30` match PLAN §1–§8:
  - the conditions and κ values;
  - 164 policies and 656 + 36 evaluations;
  - common random numbers;
  - I's sign convention;
  - per-arm and pooled estimates, weighted by seed count;
  - Šidák over 8 with z ≈ 2.73;
  - the observed-SE MDE80;
  - the self-floor and its 2σ hurdle, labelled post hoc;
  - the cross-GPU comparison;
  - the reading rules and the refusal on a partial family;
  - every blind spot in PLAN §8.

  The one difference is RM-9.
- **Text around the holes** reads correctly for any result, in §6.4, §6.5,
  §9, the abstract and App. G. The exception is §1's ordering (RM-8).
- **IC tags.** IC-1 to IC-5 are cited in text (`08_interaction_check.md:39`;
  `19_appendix_interaction.md:24-28`) on PENDING-COMMIT rows. The build
  lists all 7 tags and fails `--final` on them, as designed. This is not
  counted as a finding.

## The supplement against V3-V1, and §8 against the supplement

- **Contents (V3-V1).**
  - The `che/` package, configs, tests and scripts are in (rule C1, 160
    files), with `pyproject.toml` and `uv.lock`.
  - So are the registration documents (`phase6_design_v2.md`,
    `phase6_framing_branches.md`) and `SHA256SUMS` over all 4167 other files.
  - The committed text results the scripts read are in (R1–R4).
  - So are `docs/locks.yaml`, TF and the lock records (D3 and D4, on by
    default; RM-OWNER-1).
  - Decision-log excerpts are off by default (the owner's decision).
  - The zip is not older than any shipped source file (check #20).
- **Scrub.** The builder's check PASSES, and my independent scan of the zip
  found no identity token, no commit hash of this repository and no `.git`
  (check #17).
  - The scrub log's 108 rewrites include 71 commit rewrites (40 distinct commits) and 1 name
    handle.
  - PLAN.md ships byte-identical (11,526 B), so its pinned hash still holds.
  - It mentions "a professor's review". That is review history, not
    identity; it is the builder's recorded watch item.
- **Size.** 37.7 MB against TMLR's "up to 100MB", verbatim in the saved
  author guide (check #19). The OpenReview form's own limit is unverified,
  as the builder records.
- **Tests inside the unpacked supplement.** `uv sync --locked`, then
  `pytest`: 598 passed, 7 skipped, 0 failed.
  - One skip is the git-only frozen-base test, which SHIPPED_README
    discloses.
  - Three are RM-16.
  - Three are empty parameter sets.
- **Reproduction.** The four registered instruments, run with
  `--allow-dirty`, give 8 of 8 outputs identical to the committed ones
  outside their provenance fields.
- **§8 (`11_using_che.md:35-48`) is accurate** about:
  - the API: `reset`/`step` signatures (`che/env/env.py:200, :283-290`);
  - the test registry;
  - the commands, except for the missing `uv run` (RM-6);
  - what ships, except TF and the lock records (RM-OWNER-1);
  - checkpoints shipping only as hashes;
  - the README's CPU recomputation of the registered analyses, which the
    reproduce check confirms.

  It omits that the interaction analysis cannot run from the supplement
  (RM-7). It states no size or limit, which is correct while X5-1 and X5-2
  are pending.
- **Still owed** (the builder may still be working):
  - the README's check results (RM-13);
  - a supplement rebuild after step 0.5 and after V3Q16.

## Kit checks in detail (from `$S/kitout/kit_checks.md`)

**PASS:**

- build_v3 source checks (0 failures, 0 M1 flags);
- the kit's sha256;
- merge and Jekyll, plus the control build;
- MathJax (0 errors of 323), no raw TeX, 0 Liquid left;
- tables 17 = 17;
- the M2 references checks: no raw TeX, Unicode authors and titles equal
  the bib's, 33 of 33 d-cites resolve, one entry per key, hover cards clean;
- the M3 cite-box year;
- title and description intact;
- toc 10 of 10, in-page links 10 of 10;
- iframes 10 of 10 load, heights stable at 1280, 1024 and 390 px, none
  clipped, height attributes within 5 %;
- images 13 of 13;
- print: companions hidden on screen and shown in print, iframes hidden in
  print, interact notes hidden in print 9 of 9, nothing cut (0 of 346);
- 0 failed requests;
- listings 6 of 6 byte-identical in the built page, none cut, no page
  overflow;
- the v3 terms check (0 hits; 13 glossed, 2 registered-exempt);
- the v3 dates check (0 dates in the main text);
- the v3 caveats check (0 of 39 fail);
- the YAML check;
- M4: 781 comments stripped, 0 left;
- N3: bib `%` lines stripped;
- the stripped build renders the same as the unstripped one (108,847
  characters; tables, math and listings equal);
- the double-blind grep of the staged folder;
- the printed PDF (US Letter, no identity strings);
- the zip, with `submission_folder/` as its only top-level entry.

**FAIL:**

- pages, from page 1 (RM-1);
- print legibility, 13 of 13 (RM-OWNER-3).

**INFO:**

- math count 323 = 323;
- the byline reads "Not submitted yet.";
- one page error, the kit's comment widget (`Invalid repo: ""`);
- 3 display equations wider than the column at 390 px only, all scrolling
  (Def. 1's kernel, Def. 7's link probability, I);
- no `<d-footnote>` in the source (RM-OWNER-4);
- 9 HOLE:INTERACTION markers, 25 OWNER-PENDING markers and 7 PENDING tags.

## Cross-references and numbering

- **Resolution.** All 252 references resolve. I read every target in
  `$S/kitout/crossrefs.md` against its sentence. None points to the wrong
  section, figure, table, listing, appendix or statement. The 3 external
  references are a cited work's own numbering ("their Tables 3–4",
  "their Corollary 5.4").
- **Quotations.** "§" signs inside App. D quotations resolve to the paper's
  sections, but D.3's opening sentence says they are the record's own, which
  is adequate.
- **Headings.** H2s 1–9, H3s 3.1–3.5, 4.1–4.4 and 6.1–6.5, appendices A–J
  in the index and the headings, App. D run-ins D.1–D.10: all sequential.
- **Figures.** Main text 1–8, in reading order; Figure 9 is a HOLE and
  nothing refers to it yet. Appendix figures C1, E1, E2, H1 and H2.
- **Tables and listings.** Tables 1–3, first cited before or at their
  blocks. Listings 1–4 in §3, 5 in App. A, 6 in App. B.
- **Study codes.** Every code printed in the text or the captions is keyed
  in App. D.7.
- **Numbering of formal statements:** RM-4.

## Double-blind

- **Text.** No name, e-mail, username, repository name or URL, commit hash,
  absolute path, hostname or IP appears anywhere in the snapshot, comments
  included (checks #12–#13). The same holds for the alternates, provenance,
  ledger proposals and front matter, the staged folder, the PDF (check #14)
  and the supplement (check #17).
- **Tool names.** The tool is named only in App. J ("Claude (Anthropic),
  used through Claude Code"), as the disclosure rule allows.
- **Paths.** Repository-relative paths appear only as paths inside the code
  supplement (BRIEF §11).
- **Not scanned:** text inside the PNG figures, beyond the kit's PNG text
  chunks, and inside the GIF frames (none ship).

---

## Re-check (fix2)

Step 4.3, 2026-10-16. Snapshot `paper/v3/snapshots/fix2/`; `diff -rq` shows
the live `sections/` and `provenance/` equal to it. Changed lines read in
`scratchpad/diff_draft1_fix2.txt` (`snapshot.sh diff draft1 fix2`,
re-generated and byte-identical); outcomes in
`review/resolutions_W1.md`–`W5.md`. Only changed lines were reviewed.

### Checks run (fix2)

| # | command | result |
|---|---|---|
| R1 | `PY=$PY paper/v3/src/kit_build.sh --scratch $S/kitscratch --out $S/kitout2` (exit 1) | kit sha256 verified; merge 0, Jekyll 0, control 0; **39 PASS, 2 FAIL, 6 INFO**; PDF 38 pages, US Letter |
| R2 | its page check (`v3_checks.py pages`, inside `kit_report.py`) | **from page 1: 15.218 (FAIL against 15); from §1: 13.548 (PASS)**; Appendices heading on p. 16; 7 HOLE:INTERACTION markers still empty |
| R3 | per-section positions, `pdftotext -bbox-layout` (the check's method) | front matter, abstract and hero 1.67; §1 1.27; §2 0.94; **§3 3.50**; **§4 2.28**; §5 0.64; §6 heading 0.09; §6.1 0.28; §6.2 0.97; **§6.3 1.62**; §6.4 0.43; §6.5 0.33; §7 0.39; §8 0.61; §9 0.20 |
| R4 | `$PY paper/v3/src/wordcount.py paper/v3/snapshots/fix2/sections` | prose: abstract 234, §1 587, §2 400, §3 1,040, §4 700, §5 269, §6.1–6.2 500, §6.3 477, §6.4 200, §6.5 138, §7 198, §8 239, §9 83, which is every file at or under its STRUCTURE §3 budget. Captions: §4 210 (cap 180), §6.3 196 (cap 120 for Figs. 7 and 8) |
| R5 | the other kit checks (`$S/kitout2/kit_checks.md`) | **PASS:** build_v3 (0 failures, 0 M1); MathJax 0 errors of 340; no raw TeX; 0 Liquid; tables 17 = 17; M2 references (30 entries, 30 keys, 30 d-cites resolve, hover cards clean); M3 cite box; title and description; toc 10 of 10; in-page links 10 of 10; iframes 10 of 10 load, heights stable, unclipped, attributes within 5 %; images 13 of 13; print checks (companions, iframes, interact 9 of 9, 0 of 363 cut); 0 failed requests; listings 6 of 6 byte-identical, none cut; v3 terms (0 hits); v3 dates (0); v3 caveats (0 of 39 fail); YAML; M4 (789 comments stripped, 0 left); N3; stripped build = unstripped (110,153 characters; tables, math and listings equal); double-blind grep of the staged folder; PDF identity scan; zip. **FAIL:** pages (RM-1); legibility, 13 of 13 (RM-OWNER-3). **INFO:** math 340 = 340; byline "Not submitted yet."; one kit page error (`Invalid repo: ""`); 3 wide displays at 390 px, all scrolling; no `<d-footnote>`; 7 HOLE, 28 OWNER-PENDING, 7 PENDING tags |
| R6 | `$PY paper/v3/src/build_v3.py --out $S/final2 --final` | final-only items only: `date_confirmed`, 23 STUB-SPEC, 7 PENDING IC tags. 269 cross-references, 0 unresolved (`$S/kitout2/crossrefs.md`; every new target read and correct) |
| R7 | `provenance_check.py --root paper/v3 --strict --out $S/prov2`; `pytest paper/v3/src/tests`; `bib_diff.py` | OK, 0 unsourced or stale; 14 passed; PASS 41 of 41 |
| R8 | listings in fix2 (sections and both alternates) against `git show HEAD:` and the working tree | 12 of 12 blocks byte-identical to both; headers match the markers |
| R9 | d-cite keys in fix2 against the v3 bib | 30 keys, 0 missing |
| R10 | double-blind grep of fix2 (sections, alternates, provenance), `front_matter.yaml` and `ledger_proposals/`, comments included; hex tokens against all 221 commits (the checkout now has full history) | 0 identity hits (one "session_prompt" in a provenance file is the file name `writing_session_prompt.md`); 0 commit hashes; App. D.1 states commit dates only |
| R11 | alternates against the main Appendix A (`diff`) | `thm1_tf` differs only in Theorem 1's block; `no_prop4` only in the transfer remark; both carry the new departures paragraph and listings |
| R12 | supplement as it stands: the zip rebuilt at 16:06 today (copied to `$S/supp_1606.zip`), scanned with `python -I` (identity tokens, all 221 commit prefixes, `.git`, RUNBOOK); `rules.py`; `SHIPPED_README.md`; `che/tests/test_locks.py` (working-tree diff); `paper/v3/supplement/README.md` | 4167 files, one top-level directory; 0 identity hits; 0 commit hashes (one float, 0.008185461…, shares a 7-digit prefix with a commit); no `.git`; **no RUNBOOK**; PLAN.md ships. The builder's run3 (`run_checks.sh`, started 16:03) was still in its scrub step when this was written, so **the rebuilt zip's tests-inside-the-supplement result does not exist yet**. The last complete passing run was run1 (2026-10-14, the earlier zip) |

### Verdicts

| finding | verdict | note |
|---|---|---|
| RM-1 (MUST) page ceiling | **REOPEN** | See the text below the table. |
| RM-2 (MUST) Def. 5 and Def. 7 departures | OK | Restored at `13_appendix_proofs.md:52` (the fallback location RM-2 offered), close to v2's wording; mirrored in both alternates |
| RM-3 Def. 1, Def. 3, Cor. 1 departures | OK | `13_appendix_proofs.md:52` (Defs. 1, 3) and `:188` (Cor. 1's items 2 and 3 omitted, item 4 numbered 2) |
| RM-4 numbering unexplained | OK | `13_appendix_proofs.md:52`; one wording slip, new RM-17 |
| RM-5 "Remark 2′ (§4.4)" | OK | `:229` "Remark 2′ (Value of communication) … §4.4 refers to this remark"; both alternates |
| RM-6 `uv run` | OK | `11_using_che.md:37` |
| RM-7 interaction analysis needs git | OK | `11_using_che.md:39`; `19_appendix_interaction.md:20`. No git-free mode was added (`interaction_analysis.py` unchanged in that respect), so the text is accurate |
| RM-8 §1 hole order | OK | `01_introduction.md:49`: the marker now follows the check sentence, which is to be extended in place |
| RM-9 "eight estimates" | OK | `08_interaction_check.md:37` "eight tests" |
| RM-10 Figure 7 m/n gloss | OK | `07_example_results.md:49`, exact gloss form; the terms check passes |
| RM-11 p and ν typesetting | OK | `06_example_design.md:62`; `07_example_results.md:41, :43, :58` |
| RM-12 design review unshipped | OK | `16_appendix_timeline.md:38` |
| RM-13 supplement README "Check results" empty | **REOPEN** | `paper/v3/supplement/README.md` still ends at "Filled in from the run of `run_checks.sh` on 2026-10-14 (see below)." with nothing below. The zip was rebuilt at 16:06 today (RUNBOOK out, new `test_locks.py`) and run3 has not finished, so even the 2026-10-14 numbers no longer describe the shipped zip. Fix: when run3 ends, copy its scrub, size, manifest, tests (counts, skips, wall time) and reproduce lines into that section, with the zip's sha256 |
| RM-14 "finishes in minutes" | OK | `SHIPPED_README.md:46-47` "about 56 minutes … Budget an hour", with the contention stated |
| RM-15 RUNBOOK ships | OK | `rules.py:110-116` (R5 excludes `RUNBOOK*`); absent from the 16:06 zip (check R12) |
| RM-16 skip message on interaction configs | OK | `che/tests/test_locks.py:45-57` adds `interaction_check` to `CALIBRATED_ROLES` (working-tree change, in the 16:06 zip). The decision log carries no owner OK for editing this existing test, which RM-16 asked for. It is a test, not a lock or a registered analysis, so it is recorded here for the hand-back rather than reopened |
| RM-OWNER-1 theory document in the supplement | OWNER | Markers in place: `13_appendix_proofs.md:50` (V3Q16) and `11_using_che.md:41-42`, with the clause to add if it ships. The 16:06 zip still ships TF and the lock records (D3 and D4 on) |
| RM-OWNER-2 title length | OWNER | V3Q1 marker at `00_abstract.md:39`; candidates T5 (60 characters) and T6 (74) added in provenance; T1 (118 characters, 7 printed lines) still in `front_matter.yaml:17` |
| RM-OWNER-3 print legibility | OWNER | Still 13 of 13 FAIL (check R5). V3Q8 and V3Q11 are open in DISPOSITIONS |
| RM-OWNER-4 date and footnote | OWNER | `date: 2026-10-11` and `date_confirmed: false` unchanged; the footnote slot is in place at `00_abstract.md:39` |

**RM-1, why it is reopened.** The main text is **15.22 printed pages from
page 1**, so it still fails the graded default reading (V3Q2). From §1 it is
13.55. This is still measured with all seven interaction holes empty. Still
to come in the main text:

- the §6.4 result paragraph;
- the Figure 9 block and its print companion, about 0.3–0.4 page at this
  column's figure size (other companions);
- one sentence each in the abstract, §1, §6.5 and §9.

The writers' prose cuts worked. Every main-text file now meets its word
budget (check R4), down from 5,653 to 5,095 words, and the PDF lost
0.87 page. The rest of the overrun is not prose:

| part | pages | budget | mostly |
|---|---|---|---|
| §3 | 3.50 | 3.0 | Table 2, two listings, Figure 2 |
| §4 | 2.28 | 2.1 | captions 210 against a cap of 180 |
| §6.3 | 1.62 | 1.4 | captions 196 against 120 |
| title, byline, abstract, hero | 1.67 | 1.55 | the 7-line title |

**What is still wrong.** At the default reading, 15.22 + the holes, about
15.6–15.8 pages, is over 15.

**Fix: either of two.**

- **(a)** The owner rules V3Q2 for the §1 reading. 13.55 + the holes is about
  14.0–14.2 pages, which passes; the build then uses
  `kit_build.sh --grade section1`.
- **(b)** Keep the page-1 reading and cut about 0.8 page more:
  - a title of 75 characters or fewer (V3Q1, T5 or T6), saving about 0.1;
  - Figures 7 and 8 captions to 60 words each, and Figures 3–5 to 60 each,
    saving about 0.15;
  - Figure 5 and its caption moved to Appendix C, P3's first cut in
    STRUCTURE §3, saving about 0.3;
  - Table 2 compacted, or moved to Appendix A beside Listings 3–5, saving
    about 0.3.

Re-measure with the holes filled.

### New findings (changed lines only)

#### RM-17 (SHOULD): "the one remark is numbered 2′", but Appendix A has two remarks

**Location.** `13_appendix_proofs.md:52`, also in `alt/13_appendix_proofs.thm1_tf.md`.

**What is wrong.** The same appendix carries "**A transfer bound for a fixed
policy (remark).**" (`:243`). With it in place, "the one remark" is false.
It is true only in the `no_prop4` alternate.

**Fix.** "… this is why Definition 2 follows Definition 7 in §3 and the only
numbered remark is 2′." That wording is true in all three files.

#### RM-18 (SHOULD): stray comma, "as often as an empty one,."

**Location.** `03_environment.md:104`.

**What is wrong.** The draft1 clause "although load adds only 0.4 to 1.4 % …"
was cut, and its comma was left before the full stop. It prints as ",.".

**Fix.** "… collapses nine<!-- N:CA-8 --> times as often as an empty one."
The caveat check (C30, pattern "agent-independent") is unaffected.

#### RM-19 (SHOULD): App. D's branch table leaves row D's survival cell empty

**Location.** `16_appendix_timeline.md:94`, with the note at :97.

**What is wrong.** The row reads `| D | − (either) | | not separable … |`. A
reader sees "− (either)" under completion and nothing under survival. The
registered row (draft1: "− on either co-primary" in both cells) applies to
both columns. The note at :97 explains "(either)" but not the blank.

**Fix.** Put `− (either)` in both cells: `| D | − (either) | − (either) | not
separable from the matched-budget asymmetry |`. Keep the note, which then
reads correctly.

### Counts (fix2)

- **Verdicts on the 20 findings:**
  - 14 OK;
  - 0 OK-DECLINED;
  - **2 REOPEN** (RM-1 MUST, RM-13 SHOULD);
  - 4 OWNER.
- **New findings:** 0 MUST, 3 SHOULD (RM-17, RM-18, RM-19), 0 OWNER.
- **Kit:** 39 PASS, 2 FAIL (pages from page 1, 15.218; legibility, 13 of
  13), 6 INFO.
- **v3 checks:**
  - terms PASS;
  - dates PASS;
  - caveats PASS;
  - pages FAIL from page 1, PASS from §1 (13.548);
  - legibility FAIL.

---

## Final build (final1)

Step 4.4, 2026-10-16, on the live tree at commit `3b85a6e` (snapshot
`final1`; `diff -rq paper/v3/sections paper/v3/snapshots/final1/sections`
shows no differences). The build wrote into `paper/v3/out/`. It changed
only its own outputs: `build_report.json`, `crossrefs.md`, `files.json`,
`index.html`, `kit_checks.{md,json}`, `kit_screens/`, `submission_v3.md`,
`submission_folder.zip`, `submission_v3_print.pdf` and `artifact/`. It did
not touch the supplement builder's files (`che_supplement.zip`,
`build_summary.json`, `*_log.tsv`, `checks_summary.txt`,
`package_console.txt`, `excluded_summary.txt`, `provenance_check.md`).

**Commands**, with `PY=.venv/bin/python` and `S=<scratchpad>/RM`:

1. `PY=$PY paper/v3/src/kit_build.sh --scratch $S/kitscratch --out paper/v3/out`
   - exit 1, because of the legibility FAIL;
   - run directory `$S/kitscratch/kit_run_20261016_161541_10896`;
   - console at `$S/kit_console_final.txt`.
2. `$PY paper/v3/src/artifact_bundle.py $S/kitscratch/kit_run_20261016_161541_10896 paper/v3/out/artifact`
3. The bundle served with `http-server` and inspected in headless Chromium
   (playwright, `$S/artcheck/check.cjs`; result in
   `$S/artcheck/result.json`):
   - at 1280 px;
   - every iframe scrolled into view;
   - 8 s settle.
4. `$PY paper/v3/src/build_v3.py --out $S/final3 --final`

### Kit build: 40 PASS, 1 FAIL, 6 INFO

- **Kit:** sha256 `e531434b…bacc2d5`, verified.
- **Toolchain:** github-pages 232, jekyll 3.10.0, kramdown 2.4.0.
- **Build summary:**
  - 23 sections, toc 10;
  - 175 ledger IDs (667 tags);
  - 30 citation keys;
  - listings 6 of 6 identical;
  - 17 tables, 341 math expressions, 23 assets;
  - 0 M1 flags;
  - 264 cross-references, 0 unresolved.
- **Outputs:**
  - PDF: 38 pages, US Letter, 3,302,448 B;
  - `submission_folder.zip`: 2,156,989 B, 32 entries, `submission_folder/`
    its only top-level entry.

| group | check | result | counts |
|---|---|---|---|
| Pipeline | build_v3.py (source checks) | **PASS** | 0 failures, 0 warnings, 23 STUB-SPEC blocks, 0 M1 source flags |
| Pipeline | kit zip sha256 | **PASS** | e531… |
| Pipeline | kit merge_files() and jekyll build --future | **PASS** | merge 0, jekyll 0, control jekyll 0; github-pages (232) jekyll (3.10.0) kramdown (2.4.0) kramdown-parser-gfm (1.1.0) |
| Math and Liquid | MathJax errors | **PASS** | 0 errors in 341 rendered expressions (source count 341) |
| Math and Liquid | no raw $ or TeX in rendered text | **PASS** | 0 hits |
| Math and Liquid | math count, source against rendered | **INFO** | source 341, rendered 341 |
| Math and Liquid | 0 Liquid left | **PASS** | 0 left |
| Tables (M1) | kit table count equals the source's | **PASS** | kit 17 against source 17; build's M1 source scan flagged 0 line(s) |
| References (M2) | no raw LaTeX or -- in Distill's reference list | **PASS** | 0 of 30 entries |
| References (M2) | rendered authors and titles equal the bib's Unicode fields | **PASS** | 0 mismatches in 30 entries |
| References (M2) | every d-cite resolves | **PASS** | 30 d-cite tags, 0 unresolved |
| References (M2) | reference list has one entry per cited key | **PASS** | 30 entries, 30 cited keys |
| References (M2) | hover cards show no raw TeX | **PASS** | 30 hover cards, 0 problems |
| Citation box (M3) | the cite-this-work box has a year | **PASS** | year = {October 11, 2026} |
| Byline | what the byline shows for Submitted | **INFO** | 'Not submitted yet.' (front matter submitted_date: None) |
| Byline | title and description render intact (heading, byline, cite box) | **PASS** | 4 of 4 hold |
| Links and frames | every toc link resolves | **PASS** | 10 of 10 resolve (source toc 10) |
| Links and frames | every in-page # link resolves | **PASS** | 10 of 10 |
| Links and frames | every iframe loads (same origin) | **PASS** | 10 of 10 loaded (source 10) |
| Links and frames | iframe heights stable: 5 s and 60 s after load equal (1280, 1024, 390 px) | **PASS** | 0 frames grew, widths [1280, 1024, 390] |
| Links and frames | no iframe clips its document: frame ≥ body.scrollHeight at 60 s (1280, 1024, 390 px) | **PASS** | 0 problems, widths [1280, 1024, 390] |
| Links and frames | iframe height attributes within 5 % of the height at 60 s, 1280 px (P2 §7.2) | **PASS** | 10 of 10 within 5 % |
| Links and frames | images load | **PASS** | 13 of 13 (source includes 13) |
| Print | print companions hidden on screen | **PASS** | 10 of 10 hidden |
| Print | print companions shown in print media, images loaded | **PASS** | 10 of 10 |
| Print | iframes hidden in print media | **PASS** | 10 of 10 hidden |
| Print | nothing is cut in print: tables, math and listings fit at US Letter width | **PASS** | 0 cut of 364 checked (text column 472 px) |
| Print | 'Interact' notes hidden in print | **PASS** | 9 of 9 |
| Requests | 0 failed requests | **PASS** | 0 failed of 152 (10 aborted during re-layout and then loaded, not counted) |
| Requests | console errors | **INFO** | 0 console, 1 page errors |
| Listings and overflow | listings in the built page equal their committed lines byte for byte | **PASS** | 6 of 6 identical |
| Listings and overflow | no listing cut at 1024 or 1280 px; no page overflow at any width | **PASS** | listing font 12px |
| Listings and overflow | display math wider than the column (reported, not graded) | **INFO** | 3 instances over three widths, 0 cut off with no scrollbar |
| Footnote (N1) | where <d-footnote> text lands, on screen and in print | **INFO** | no <d-footnote> in the source |
| v3 main text | main-text printed pages <= 15 (graded reading: from page 1) | **PASS** | from page 1 14.698; from '1 Introduction' 13.265; to 'Appendices' (PDF 38 pages) |
| v3 main text | no internal code or private-vocabulary term (appendix exempt) | **PASS** | 0 hits; 73 terms (paper/v3/checks/terms.txt); 2 registered-exempt, 13 glossed, 1 in listings (not graded) |
| v3 main text | no date outside the allow-list (appendix exempt) | **PASS** | 0 dates outside the allow-list; 0 allowed (paper/v3/checks/dates_allow.txt) |
| v3 main text | each caveat in its one home (one-home map) | **PASS** | 0 of 39 entries fail (paper/v3/checks/caveats.yaml) |
| v3 main text | HOLE:INTERACTION and OWNER-PENDING markers (reported until step 0.5 and the owner's rulings) | **INFO** | 7 HOLE:INTERACTION, 28 OWNER-PENDING; 7 tags on PENDING ledger rows |
| v3 main text | figure images legible in print: a 8 pt label prints at >= 7 pt (estimate) | **FAIL** | 13 of 13 printed images fail |
| YAML | title and description: one line, no double quote, YAML-safe | **PASS** | staged front matter parses; no problems |
| Leaks and print | comment-stripped staged submission.md (M4) | **PASS** | 788 comments in submission_v3.md (23 STUB-SPEC), 0 '<!--' left in the staged copy |
| Leaks and print | staged bib has no % lines (N3) | **PASS** | 4 % lines in the bib, 0 staged; 41 entries |
| Leaks and print | stripping removed only comments (stripped build = unstripped build) | **PASS** | rendered text identical (109729 chars); tables [17, 17]; math [341, 341]; listings [6, 6] |
| Leaks and print | double-blind grep of the staged folder | **PASS** | 25 files; 5 identity tokens; url 0, identity 0, abs_path 0, hex 0, image_text 0 |
| Leaks and print | printed PDF written (US Letter), no identity strings in its text | **PASS** | 38 pages, 3.3 MB, page size 612 x 792 pts (letter) |
| Leaks and print | staged folder zipped | **PASS** | 32 entries, top level ['submission_folder'], 2.2 MB |

### Page counts (main text, printed PDF)

| reading | pages | ceiling 15 |
|---|---|---|
| from the top of page 1 to "Appendices" (graded default, V3Q2) | **14.698** | PASS |
| from "1 Introduction" (p. 2, y 343) to "Appendices" (p. 15, y 553) | **13.265** | PASS |

Both readings are still measured with the **7 HOLE:INTERACTION markers
empty**. The §6.4 result paragraph, Figure 9 and the sentences in the
abstract, §1, §6.5 and §9 will add to both. At the page-1 reading, 0.30
page is left, which is likely too little for Figure 9's block and print
companion. RM-1 therefore stays open on the page-1 reading until the holes
are filled and the PDF is re-measured, or until V3Q2 rules the §1 reading
(1.73 pages left).

### v3 checks

- **pages:** PASS from page 1 (14.698), PASS from §1 (13.265).
- **terms:** PASS (0 hits; 73 terms; 2 registered-exempt, 13 glossed, 1 in
  listings).
- **dates:** PASS (0 outside the allow-list).
- **caveats:** PASS (0 of 39 entries fail).
- **legibility:** **FAIL** (13 of 13 printed images; an 8 pt label prints at
  2.5–4.3 pt). This waits on V3Q8 and V3Q11 (RM-OWNER-3).
- **markers:** INFO, 7 HOLE:INTERACTION, 28 OWNER-PENDING and 7 tags on
  PENDING IC rows.

### `build_v3.py --final` (exit 1): what blocks it

1. `front_matter.yaml`: `date_confirmed` is not true (owner Q2;
   RM-OWNER-4).
2. 7 tags on PENDING IC rows:
   - `08_interaction_check.md:37` IC-4;
   - `19_appendix_interaction.md:24` IC-1 and IC-2;
   - `:26` IC-4 and IC-5;
   - `:28` IC-3 (twice).
3. 23 STUB-SPEC blocks.

That is 9 final-only items in all, all of them expected. There are 0 hard
failures and 0 warnings, so nothing else blocks the final build.

### Private-artifact bundle

- **Location:** `paper/v3/out/artifact/`. The entry is `index.html`
  (191,577 B), and every other file is supporting, published at its relative
  path.
- **Size:** 133 files, 6,558,205 B in all, under the 16 MB page limit.
- **Not published.** The orchestrator publishes.

What the bundler did:

- rewrote the `/tmlr-beyond-pdf/` paths to relative ones;
- vendored the non-Google stylesheets and their fonts under `vendor/`;
- vendored the MathJax 3.2.0 CHTML woff-v2 fonts locally;
- removed the utteranc.es widget (0 left);
- dropped the doctype/head wrapper and set `<title>` "CHE Paper v3".

**Headless Chromium on the bundle** (`$S/artcheck/result.json`):

- **0 failed requests** (no network error and no HTTP ≥ 400), and 0 page
  errors.
- **Math:** 341 `mjx-container`s (source 341), 0 `mjx-merror`, 0 raw `$$`,
  `\(` or `\[` in the article text.
- **MathJax fonts:** 9 requested, all from `vendor/mathjax-fonts/`.
- **Iframes:** 10 of 10 load with a body. Their heights are the kit's pinned
  values (700, 536, 748, 454, 844, 1024, 484, 515, 700, 700), each at least
  its document's height.
- **Images:** 13 of 13 load. All 30 d-cite tags are present. The comment
  widget is absent.
- **External hosts requested:**
  - fonts.googleapis.com and fonts.gstatic.com (allowed);
  - cdnjs.cloudflare.com and cdn.jsdelivr.net (pinned scripts, allowed);
  - **distill.pub**.

**INFO, distill.pub:** Distill's `template.v2.js` fetches
`https://distill.pub/third-party/katex/katex.min.css` and `katex.min.js`.
Locally both load. The Artifact viewer's CSP admits scripts only from the
listed CDNs and stylesheets only from Google Fonts, so it will refuse these
two requests and log a console error.

The paper uses no `<d-math>`, and all math is MathJax, which renders (341 of
341). So nothing visible depends on these requests; this is my reading of
the template, not tested on the host. If the orchestrator wants a clean
console, `artifact_bundle.py` could vendor the two files, or strip the
reference. That would be a tool change, not done here.

### Findings from the final build

No new findings in my lane. Two items are carried open:

- **RM-1:** PASS at both readings now, but 0.30 page of headroom at the
  page-1 reading with the holes still empty.
- **RM-OWNER-3:** the legibility FAIL.

RM-13 is the supplement builder's and was not re-checked in this step.
