# Paper v2: builder subagents draft the TMLR Beyond PDF paper; the owner checks every word

Written 2026-10-11 under the decision log's **PAPER V2** ruling (read it
first, with **DEMONSTRATION DRAFT** before it). Paste this whole file as the
first message of a fresh session.

## What this session produces, and why the line is where it is

A complete TMLR Beyond PDF paper (title, `description`, abstract, body,
appendix, bibliography, interactive figures) in the author kit's format,
built with the **real kit** and checked by independent reviewers. The
starting point is the demonstration at `paper/demo_beyond/`, which the owner
reviewed and liked. Change only what this prompt and the owner direct.

**The owner checks every word and is responsible for the paper.** Your job is
to make that check fast and complete. Every sentence you draft has a stated
source, and nothing you write enters `paper/finale.md` or the submission
until the owner has approved it section by section.

TMLR's rules, as read on 2026-10-11 (PAPER V2 item 2):

- LLMs may be used as general-purpose assistive tools.
- Authors are fully responsible for every word, and LLMs cannot be authors.
- The tool's use is mentioned "as a footnote on the first page".
- The ideas, claims and results are expected to be "human-sourced".
- Papers that look largely LLM-generated "will be closely examined". In
  2026-09 a co-editor-in-chief questioned the authors of papers headed for
  desk rejection about their own work.

So two things are non-negotiable:

- **Every claim traces to the record.** That means the owner's rulings
  (`docs/decision_log.md`) and measured artifacts. Nothing is invented,
  extrapolated or "improved" beyond what the record supports.
- **The owner can defend every sentence.** The per-sentence provenance tables
  (step 4) exist for this.

## Read first (lean; the project is large)

1. `CLAUDE.md` (auto-loaded) and `HANDOFF.md`.
2. `docs/decision_log.md` from **UNBLIND RESULT** to the end, especially:
   - **DEMONSTRATION DRAFT** and its amendment;
   - **PAPER V2**.
3. `writing_session_prompt.md`, for its "Numbers", "Known traps" and
   check-category rules. Its "you never supply prose" rule is superseded for
   v2 by PAPER V2 item 1.
4. The scaffold, `paper/demo_beyond/`:
   - `README.md`;
   - `BRIEF.md` (rules, traps, kit syntax and per-section facts; it was
     corrected once, see `review/claims.md`);
   - `REVIEW.md` (its six OWNER ITEMS);
   - `KIT_BUILD.md` (how the real kit build ran and what differed);
   - `sections/`;
   - `ledger_supplement.md`;
   - `src/build_demo.py`.
5. `paper/numbers_ledger.md`, the only source of numbers, together with the
   scaffold's `ledger_supplement.md`.
6. `paper/branch_B.md` §5 (required honesty lines) and §8 (what not to claim).
7. `paper/finale.md`: the owner's earlier title, abstract, `description`, §1
   and §2. This is material, not binding text, except where a ruling says
   otherwise.
8. `paper/beyond_pdf/KIT_NOTES.md` §S1.3–S1.9, and
   `paper/related_work_verification.md` (the only source a `.bib` entry may
   come from).

## Rules that bind every agent

- **Numbers:** a number comes only from the ledger or the supplement, tagged
  `<!-- N:ID -->`. A number with no row gets a VERIFIED row first, read from
  a committed file at file:line, or it is cut. Never from memory, the spine
  or `branch_B.md` alone, which lag the ledger.
- **Registered strings stay verbatim** where the registration requires them,
  even while §9's jargon is cut: "does not survive the inert-share
  correction"; "sign unstable over the final half" on both co-primaries.
  Completion null is an exclusion with its bound. Matched compute, never
  convergence. B̂ gets no verdict. Bias (b) reverses sign on the grid card.
- **Citations:** keys from `submission.bib` only. A new citation is verified
  through `related_work_verification.md` first; never write a `.bib` entry
  from memory.
- **Double-blind:** no repository URL, no names, no account-resolving hashes,
  no absolute paths. The disclosure footnote names the tool, not the author.
- **No new runs and no GPU spend.** No training, no test-suite runs and no
  project code. The only things you run are the scaffold's build and the
  real kit build (steps 3 and 4).
- **Do not edit** `CLAUDE.md`, `docs/theory_foundations.md`, the canonical
  ledger, the configs or any code. Do not edit `paper/finale.md` until the
  owner approves a section. Where the record itself is wrong (OWNER ITEMS),
  report it.
- **Commit nothing unless the owner says so** in this session. Work goes in
  a new folder, `paper/v2/`, with the scaffold's layout. `paper/demo_beyond/`
  stays as it is, for comparison.

## The owner's fix list, with locations (verified 2026-10-11)

### Mechanical

- **M1. The |Δ| table bug.** The kit parses Markdown as GFM, so a prose line
  containing two pipes becomes a table. Two paragraphs render as one-row
  tables in the real kit build (19 tables against 17 in the source):
  - `sections/09_compositional_test.md:134` ("Reproducibility and
    hardware … max |Δ| = 2.44 × 10⁻⁴");
  - `sections/11_reproducibility.md:7` ("What is exact, and what is not").

  Fix: write the absolute value as `$\lvert\Delta\rvert$`, or in words. Add a
  build check that the kit build's table count equals the source's.
- **M2. Broken references.** Distill's reference list shows raw LaTeX in
  several entries: `C{\^o}t{\'e}`, `{\c{C}}akır`, `{VULCAN}`, `Gar\dh ar`,
  `Rockt\"{a}schel`, `$\frac{1}{2}$` and `--` page ranges (`KIT_BUILD.md`
  difference 1). Fix the entries at their source, using Unicode in
  `related_work_verification.md`, then re-copy the `.bib` verbatim (40
  entries). Re-check every rendered entry, and every in-text hover card, in
  the kit build. Also confirm that every `d-cite` resolves and every
  cross-reference (§, Figure, Table, Listing, Appendix) points at the right
  target.
- **M3. The empty BibTeX year.** The kit's "cite this work" box (layout
  `distill.html`, `year = {${publishedWhen}}`) is built from `page.date`, and
  the front matter sets none. Set `date`, and decide `submitted_date`, in the
  YAML header; the owner chooses the date. Confirm the box in the kit build.
- **M4. HTML comments.** The built page source carries 869 HTML comments
  (ledger tags, line-1 labels). Keep them in the repository copy. Strip them
  in the staged `submission_folder/` if the preprint links to the rendered
  site.

  Note that `KIT_NOTES.md` §S1.9 item 6 also says the Beyond PDF assets and
  the page source are public during review. Ask the owner whether to strip
  for the OpenReview upload too.

### Correctness

Check each against `docs/theory_foundations.md` and report any matching
error in the theory doc to the owner. Do not fix the theory doc.

- **C1. Corollary 1(3) and (4),** at `sections/04_severity.md:18-24` and
  wherever App. A repeats them.
  - (3) states the critical exponents 43/18 and 4/3 as inherited facts. The
    builder's understanding, **to be verified through the citation
    process**: they are proved for site percolation on the triangular
    lattice and only conjectured, by universality, for bond percolation on
    ℤ². State them at the level a verified source supports, or drop them.
  - (4), linear growth with a front speed and a deterministic limiting
    shape, has no citation and no bib key. Find and verify a theorem that
    covers this process, or soften or drop the item.
  - Nothing in the design depends on (3) or (4), as §4 already says.
- **C2. Soften Remark 1** (`sections/03_environment.md:36`). "So this hardness
  applies" overreaches. NEXP-completeness is a worst-case result for the
  general class, not a property of every instance. State what it actually
  licenses: no general exact planner is expected to scale, which motivates
  learning.
- **C3. Proposition 4 is an upper bound, not "irreducible"**
  (`sections/09_compositional_test.md:17`, `:23`; `12_appendix.md:31`; also
  `01_introduction.md:39` and `10_limitations.md:23`). Rename the proposition
  and reword "irreducible slack". A bound's slack is not shown irreducible
  without a matching lower bound. Check the theory doc's own statement.

### Framing (a day of writing, no new runs)

- **F1. Retitle** so that the hazard-blind reward is not the lead (PAPER V2
  item 3). Draft 3 to 5 candidate titles for the owner, each with a one-line
  note on what it leads with. Keep the ratified terminology.
- **F2. Rewrite the abstract to lead with the plain result.** In order:
  - what was tested;
  - what happened: survival up, completion with no detectable change, and
    the gain does not survive the correction;
  - why, then what the environment and method contribute.

  Keep the required lines, including the inert-share qualifier at abstract
  level and the Γ(t) suffix. Re-check `description` against the new
  abstract; it must be one line with no `"`.
- **F3. Own the δ confound as a design error.** The ISO mixture included an
  element (δ) that proved inert under the frozen encoder at this scale, so
  a third of ISO's training episodes were fire-only. Say plainly that the
  design did not anticipate this. It was found and registered, with ISO-4
  to correct it, mid-grid and before unblinding. The scaffold frames it as
  "registered as a bias" (`01_introduction.md:37`, §9.1, §10); keep that
  fact, but stop presenting it as foresight.
- **F4. Separate the advice from "therefore."** The owner's abstract ends
  "Studies of compositional generalization should therefore match the share
  …" (`paper/finale.md:13`). One environment's result does not entail a
  field-wide rule. Present the advice as a recommendation the result
  motivates, labelled as such, and keep it out of any sentence that reads
  as a conclusion. Apply the same check everywhere the advice recurs (§1,
  §9.2, §10).
- **F5. Cut the internal jargon in §9.** In `09_compositional_test.md`:
  - "card": 13 uses;
  - "ladder": 7, and "rung": 6;
  - "sweep_c50…": 7;
  - "re-floor": 4;
  - S1–S6 labels: 4;
  - "floor-basis": 3, and "beat-reproducibility": 2;
  - Γ₄′: 9, which needs a plain name at first use.

  Replace each with a plain term defined once ("GPU", "the registered
  reading order", "the no-coupling sweep arm", "re-measured reproducibility
  floor"), or move it to the appendix. Registered strings stay verbatim.
  Run the same pass over §8, §10 and the appendix.

### Already known, carried over

- `REVIEW.md` OWNER ITEMS 1–4, which are in the owner's own text:
  1. "As predicted before measurement", in the abstract and §1;
  2. Proposition 1's finiteness, in the theory doc and in "finite
     Dec-POMDP";
  3. "every arm is perturbed throughout", in §2;
  4. "about seven percent", in §2.

  Make v2 accurate on all four. Report items 5 and 6, which are record
  fixes.
- `KIT_BUILD.md` differences:
  - long code lines cut on screen; consider wrapping in the listing CSS or
    shorter ranges;
  - the reference-list LaTeX (M2).
- Length: §9 and the appendix ran well over the brief's targets. v2 should
  be tighter. Do not restate a result in several places; point back to
  where it is stated.

### "Stuff like this"

PAPER V2 item 4 says the list is not exhaustive. The step-2 reviewer and the
step-4.5 blind agent look for more findings of these three kinds. **Report new findings
to the owner before fixing them**, with locations and a proposed direction.

## Phase 1 process (owner's plan, PAPER V2 amendment, 2026-10-11)

Five steps, in this order. Steps 1 and 2 run in parallel. Each later step
starts only when the one before it has handed back. Every agent gets this
file's rules ("Rules that bind every agent") and the fix list in its prompt.
All work goes under `paper/v2/`. Before step 1, confirm with the owner that
phase 1 should start. Ask nothing else up front: owner decisions are
collected and put to the owner at step 4.5.

### Step 1: three planners (parallel, independent)

Each planner reads:

- the scaffold (`paper/demo_beyond/`, as rendered and as source);
- the owner's earlier text (`paper/finale.md`);
- the record: the decision-log tail, the ledger, and `branch_B.md` §5 and §8;
- the kit notes;
- the figure set (`paper/figures/interactive/DESIGN.md` and its MANIFEST).

Each writes `paper/v2/plans/P<n>.md`, using a different lens, so that the
three plans differ:

- **P1, the argument.** What the paper claims, and in what order:
  - title candidates (3–5; F1);
  - the abstract's spine, leading with the plain result (F2);
  - the section list, with one sentence per section on what it establishes
    and which ledger rows carry it;
  - where the δ design error (F3) and the advice (F4) sit;
  - what to cut.
- **P2, the Beyond PDF reading path.**
  - Which interactive figure leads each section, and what the reader does
    with it.
  - Where code listings and LaTeX earn their place.
  - What moves to the appendix.
  - The kit mechanics that constrain the layout.
- **P3, the referee's view.**
  - What a TMLR reviewer needs to accept the claims (TMLR's criteria:
    claims supported by evidence; of interest to part of the audience).
  - Which limitations must be up front.
  - The jargon to cut (F5).
  - A word budget per section, targeting a paper clearly shorter than the
    scaffold.

Each plan cites the record for every claim it proposes, and states what it
would not do.

### Step 2: one reviewer, on this session's paper (parallel with step 1)

The reviewer reads the demonstration (`paper/demo_beyond/`: sections,
`REVIEW.md`, `KIT_BUILD.md`, and the built page). It writes
`paper/v2/review_of_demo.md` with three parts:

- **Findings.** Confirm or correct every item of the owner's fix list at its
  location (M1–M4, C1–C3, F1–F5), the four OWNER ITEMS and the kit-build
  differences. Then add new findings of the same three kinds, each with its
  location and evidence.
- **Decisions.** What v2 keeps from the demonstration, what changes and what
  goes, section by section, each with a reason. These are builder decisions
  inside the owner's rulings. Any decision that would change a ruling is
  listed separately, for the owner.
- **Owner questions** for step 4.5:
  - whether to strip comments for the OpenReview upload (M4);
  - the `date` value (M3);
  - the title choice;
  - any ruling-level item.

### Step 3: two builders, the v2 scaffold

The builders read the three plans, the step-2 review and the demonstration.
They do not write paper prose. They split the work and own disjoint files:

- **B1, content scaffold.**
  - Reconcile the three plans into one structure, and record in
    `paper/v2/STRUCTURE.md` which plan each choice came from and why.
  - Write `paper/v2/BRIEF.md`. It carries over the demonstration's
    `BRIEF.md` with every fact re-verified, plus:
    - the PAPER V2 roles;
    - the fix list, with an owner for each item;
    - the plain-term glossary (F5);
    - the disclosure-footnote rule;
    - the provenance rule.
  - Create `paper/v2/sections/*.md` stubs, each with:
    - its heading;
    - its purpose;
    - its required facts (ledger IDs);
    - its figures, listings and LaTeX items;
    - the honesty lines that land in it;
    - its word budget.
  - Assign the sections to step-4 writers.
- **B2, build and checks.**
  - Adapt `paper/demo_beyond/src/build_demo.py` to `paper/v2/src/`.
  - Fix the bibliography at its source (M2): Unicode in
    `related_work_verification.md`, then re-copy the `.bib` verbatim.
  - Add `date` to the front matter (M3, as a placeholder until the owner
    sets it).
  - Script the real-kit build (fetch the kit, verify its sha256, stage
    `submission_folder/`, run the kit's `merge_files()`, then
    `bundle exec jekyll build` with a UTF-8 locale) together with the
    automated checks:
    - math errors 0, and no raw `$`/TeX;
    - kit table count equals the source's (M1);
    - no raw LaTeX in the reference list (M2);
    - the citation box has a year (M3);
    - 0 Liquid left;
    - every `toc` link resolves;
    - every iframe loads and sizes itself;
    - images load;
    - print companions hidden on screen and shown in print;
    - 0 failed requests;
    - the printed PDF;
    - a comment-stripped staged copy with 0 `<!--` (M4).
  - Write the provenance template.

### Step 4: many agents, the final version

The final version is built in four passes.

1. **Writers, 5–6 in parallel.** One per section group, as B1 assigned.
   The default split:
   - title candidates, `description`, abstract and hero, plus the
     disclosure `<d-footnote>`;
   - §1–§2;
   - §3–§4;
   - §5–§7;
   - §8 and §10–§11;
   - §9 and the appendix.

   Each writer fills its stubs and writes `paper/v2/provenance/<section>.md`.
   That file has one row per sentence, giving:
   - the sentence;
   - its support (ledger ID(s), a decision-log entry or file:line, or
     "framing" if it makes no claim);
   - what changed from the demonstration, and why.

   New rows go to `paper/v2/ledger_proposals/W<n>.md`, VERIFIED.
2. **Reviewers, in independent lanes,** writing to `paper/v2/review/`:
   - **claims:** overreach, undersell, conflict, missing,
     cross-section, and F1–F5 as directed;
   - **numbers:** every tag against its row and source, every new row,
     and all arithmetic;
   - **mechanics:**
     - kit syntax;
     - listings byte-identical to their files;
     - LaTeX against the theory doc (C1–C3 and every other formal
       statement);
     - cross-references and double-blind;
     - M1–M4.
3. **Fix and re-check.**
   - The writers fix their own files.
   - The claims and numbers reviewers re-check the changed lines only,
     against a snapshot diff.
   - Every finding's outcome is recorded in `paper/v2/REVIEW.md`.
4. **Build with the real kit** (B2's script), all checks green. Publish the
   built page as a private artifact. Produce the `submission_folder` zip
   and the printed PDF.

### Step 4.5: the owner and one blind agent review the final version

- **The blind agent** sees only the paper. Copy the built PDF and the
  submission folder to a fresh scratch directory, and give the agent that
  path alone. Tell it to read nothing else (no repository, no record, no
  brief, no reviews).
  - It writes a TMLR-style review: summary of contributions, strengths
    and weaknesses, whether claims are supported by clear and convincing
    evidence, requested changes, and broader concerns.
  - It also lists every sentence it found unclear or garbled.
  - The blindness is by instruction, since the agent shares this
    container. Say so in its hand-back.
- **The owner** reads for anything wrong that could have been said and for
  garbled text. Give the owner:
  - the artifact link and the printed PDF;
  - the per-section provenance tables;
  - the list of changes from the demonstration;
  - every open finding;
  - the step-2 owner questions;
  - the blind review.

This is the end of phase 1. Nothing enters `paper/finale.md` or the
submission, and nothing is committed, until the owner rules on what to do
with the review results.

## Hand-back to the owner (each phase)

Keep it short:
- what changed;
- what is waiting on the owner's decision;
- the findings that are not fixed, and why;
- where to look (paths and the artifact link).

Never report a check as passed unless it ran in this session.
