# Paper v3: rewrite the TMLR Beyond PDF paper as an environment paper; builder subagents draft, and the owner checks every word

Written 2026-10-12 under the decision log's **PAPER V3** ruling. Read that
ruling first, then **PAPER V2** and **DEMONSTRATION DRAFT** before it.
Paste this whole file as the first message of a fresh session.

## What this session produces, and why

The session produces a rewritten TMLR Beyond PDF paper:

- the title, `description`, abstract, body, appendix, bibliography and
  interactive figures;
- in the author kit's format, built with the **real kit**;
- checked by independent reviewers;
- with an **anonymized code supplement**;
- and with **one new post hoc analysis**, the interaction check.

**The starting point is `paper/v2/`.** That is Paper v2 phase 1, complete
and committed at `f744ae2`: plans, a reviewed draft, per-sentence
provenance, verified ledger rows, the build and its checks, the reviews and
a blind review. Reuse it. Do not redo v2's verification work. Re-verify only
what v3 changes or adds.

**Why v3 exists.** A professor reviewed the v2 paper (PAPER V3 item 1), and
so did a blind agent (`paper/v2/review/blind_review.md`). Their verdicts
agree:

- the compositional test sits where composition is weak;
- its effect is tiny;
- the recommendation undermines itself;
- the paper reads like an audit log;
- the pre-registration cannot be checked.

**The owner's answer** (PAPER V3 items 2–4):

- an **environment-first** paper, with the pre-registered test as its
  worked example;
- a much shorter, plainer text: 12–15 printed pages of main text;
- the eval-only **interaction check**;
- the **code ships**;
- ISO-4 at 2000 updates is **future work**.

**The owner checks every word and is responsible for the paper.** TMLR's
rules, as read on 2026-10-11 (PAPER V2 item 2):

- LLMs may be used as assistive tools.
- Authors are fully responsible for every word, and LLMs cannot be authors.
- Tool use is disclosed "as a footnote on the first page".
- The ideas, claims and results are expected to be "human-sourced".
- Papers that look largely LLM-generated "will be closely examined".

So, non-negotiable:

- **Every claim traces to the record:** the owner's rulings
  (`docs/decision_log.md`), the ledgers, and committed artifacts. Nothing is
  invented, extrapolated or "improved".
- **The owner can defend every sentence.** Every sentence gets a provenance
  row, as in v2.
- **The result is described accurately** (PAPER V3 item 3):
  - it is not a plain null;
  - the registered strings stay verbatim;
  - the framing change is disclosed in the paper.
- **Anything post hoc is labelled post hoc wherever it appears**, abstract
  included, and never joins the registered confirmatory family (CLAUDE.md,
  "Instruments state what they are blind to", clause 2).

## Read first (lean; the project is large)

1. **Orientation:** `CLAUDE.md` (auto-loaded), then the top block of
   `HANDOFF.md`.
2. **The rulings:** `docs/decision_log.md`, from **UNBLIND RESULT** to the
   end, and closely: DEMONSTRATION DRAFT, PAPER V2 (with its process
   amendment), PAPER V3.
3. **The v2 hand-back, in this order:**
   - `paper/v2/HANDBACK.md`;
   - `paper/v2/OWNER_QUESTIONS.md`: which questions PAPER V3 settles, and
     which stay open;
   - `paper/v2/REVIEW.md`, its "Status" section;
   - `paper/v2/review/blind_review.md`, W1–W10 and the 101 unclear
     sentences, which v3 must not reproduce.
4. **The v2 scaffold, as material:**
   - `paper/v2/BRIEF.md`:
     - §5.2, the glossary;
     - §6, registered strings;
     - §7, the F3 timeline;
     - §9, traps;
     - §12, disclosure;
     - §14, kit syntax;
   - `paper/v2/STRUCTURE.md` and `paper/v2/INTERFACE.md`;
   - `paper/v2/src/README.md` and `paper/v2/src/VALIDATION.md`;
   - `paper/v2/sections/` with `paper/v2/provenance/`.
5. **Numbers:** `paper/numbers_ledger.md`, `paper/v2/ledger_supplement.md`
   and `paper/v2/ledger_proposals/*.md`. These are the only sources of
   numbers.
6. **Registered framing and honesty lines:**
   - `paper/branch_B.md` §5 (honesty lines) and §8 (what not to claim);
   - `phase6_framing_branches.md`, the registered original framing.
7. **Kit and citations:** `paper/beyond_pdf/KIT_NOTES.md` §S1.3–S1.9, and
   `paper/related_work_verification.md`, the only source of `.bib` entries.
   It now has a Part 4 and Unicode names, from v2's M2 work.
8. **Only for the interaction check and the code supplement:**
   - `che/eval/harness.py`, whose `--config` selects θ;
   - `che/configs/theta_star_holdout.yaml` and the `severity_*.yaml` files;
   - `che/scripts/make_phase6_configs.py`;
   - `che/scripts/run_p6_post_unblind_evals.sh` and
     `che/scripts/p6_post_analysis.py`, the pattern for refusing to run out
     of order;
   - `che/bench/results/phase6/phase6_report.md` §3 (archives and hashes)
     and the `SHA256_CKPT.txt` files.

## Rules that bind every agent

- **Numbers.** A number comes only from the ledger, the supplement or a
  ledger proposal, tagged `<!-- N:ID -->`. A number with no row gets a
  VERIFIED row first, read from a committed file at file:line, or it is cut.
  Never from memory, the spine or `branch_B.md` alone. Derived numbers show
  their derivation in the row.
- **Registered strings stay verbatim** where the registration requires them:
  - "does not survive the inert-share correction";
  - "sign unstable over the final half", on both co-primaries;
  - completion null as an exclusion with its bound;
  - matched compute, never convergence;
  - B̂ gets no verdict;
  - bias (b) reverses sign on the grid GPU.
- **Citations.** Keys come from the v3 bib only. A new citation is verified
  through `related_work_verification.md` first, read in full where its claim
  needs it. Never write a `.bib` entry from memory.
- **Double-blind, for the paper and the code supplement alike.**
  - No repository URL, no names, no account-resolving hashes, no absolute
    paths.
  - The supplement ships without `.git`, and author strings are scrubbed
    from code, configs and comments.
  - The disclosure names the tool, not the author.
- **Post hoc is labelled** (see above), and **every new analysis has a
  measured floor** (CLAUDE.md, "Bars come with floors", per-artifact).
- **Runs.**
  - Only PAPER V3 item 2(a) is authorized: the **eval-only** interaction
    check, at the scope the owner sets in step 0. No training.
  - **This session has no GPU.** It prepares and tests on CPU. The owner
    rents the GPU, restores the checkpoint archives and runs the job. The
    artifact-persistence rule binds, and the run script asserts it.
- **Code.** Allowed only for:
  1. the interaction check's configs, run script, analysis script and tests;
  2. the code-supplement packaging script and its checks;
  3. the paper build in `paper/v3/src/` (adapted from `paper/v2/src/`);
  4. new figures from committed artifacts, plus label-only rebuilds of
     existing figures, if the owner agrees (v2 Q11).

  CLAUDE.md's coding conventions apply. After each code milestone, run
  `ruff` and the full CPU test suite, and get both green. Do not change
  environment semantics, locks, constants, existing configs or any
  registered analysis code. New configs are added; existing ones are never
  edited.
- **Do not edit:**
  - `CLAUDE.md`. Its layout block is refreshed at phase close, only with the
    owner's OK.
  - `docs/theory_foundations.md`.
  - The canonical ledger.
  - Registered documents.
  - `paper/finale.md`, `paper/beyond_pdf/` and `paper/v2/`. v2 is the
    record; v3 works in `paper/v3/`.

  Where the record is wrong, report it.
- **Rulings bind once transcribed.** Every owner decision in this session is
  transcribed into `docs/decision_log.md` in the same session, before it is
  acted on.
- **Commits.** At the end of each step, commit and push to the session's
  designated branch. Nothing enters `paper/finale.md` or the submission
  until the owner approves it. The owner may change this rule at the start.
- **Hooks.** If a harness hook refuses an action, do not route around it. In
  v2, a file named `FINDINGS.md` was refused and then written through the
  shell. Rename the file, or ask.

## The owner's change list for v3

The codes are V3-*. Each item cites its source:

- **PROF n:** PAPER V3 item 1, point n;
- **BLIND Wn:** the blind review;
- **v2 IDs:** `paper/v2/FINDINGS.md` and `REVIEW.md`.

### Framing

- **V3-F1. Environment first.**
  - CHE is the contribution. Its properties are each stated with the rows
    that carry them:
    - collapse seeds the fire (Coupling A);
    - smoke attenuates perception (Coupling B);
    - a hazard-blind reward with a cause-blind death price;
    - severity placed by a measured percolation threshold;
    - ablations that are bitwise-exact nested models;
    - theory checked as unit tests;
    - the floors protocol.
  - The pre-registered test becomes the worked example (PAPER V3 item 3).
- **V3-F2. The abstract gives one question, one result and one lesson**
  (PROF 4).
  - Write it **after** the interaction check, because the lesson depends on
    its result.
  - Keep the registered strings, the completion bound and the Γ(t) suffix.
  - Recheck `description` against it: one line, no `"`.
- **V3-F3. State the size plainly** (PROF 2). The survival gain is about a
  tenth of an agent per episode; that needs a derived VERIFIED row. It
  appears only in the last fifth of training. The paper no longer rests on
  it.
- **V3-F4. Rewrite the lesson and the recommendation** (PROF 3; BLIND W2).
  - State the identity: active share = μ_A + μ_B − p.
  - So matching the active share alone cannot isolate co-occurrence.
  - The secondary plane decomposition separates the two; it leads the
    worked example's results (PAPER V3 item 2(c)). Label it
    non-verdict-bearing, as registered. Γ stays the registered test.
  - Future work: exposure-matched ISO-4 at 2000 updates, and varying
    coupling strength.
  - The advice is never a "therefore".
- **V3-F5. Disclose the framing change in the paper** (PAPER V3 item 3). It
  goes in the worked example's opening and in the registration timeline.
  The registered outcome branches stay the record of the original framing.
- **V3-F6. Limitations in front** (PROF 1; BLIND W1, W3).
  - The test was sited where composition is weak. State this as central, not
    as a caveat. The interaction check measures it.
  - The δ "inert" label rests on coarse bars, and is applied asymmetrically
    across the couplings.
  - One algorithm, one map size, 12 agents (BLIND W8).

### Style

- **V3-S1. 12–15 printed pages of main text** (PROF 4), measured on the
  kit's printed PDF. The appendix is not capped, but stays tight.
- **V3-S2. A registration-timeline appendix** holds the audit trail. The
  main text carries none of it, except at most the unblinding date and the
  fact of registration. The trail covers:
  - every date and ruling;
  - provenance;
  - GPU blocks;
  - study codes;
  - seeds and archives.
- **V3-S3. No internal codes or private vocabulary in the main text.**
  - Codes: M5.5, G1.2, m44, GPU 1/2/3, ….
  - Vocabulary: "rung", "card", "knee", "grades nothing", "floor basis", ….
  - Extend v2's glossary (BRIEF §5.2). Figure labels that cannot be rebuilt
    are glossed once.
- **V3-S4. Captions say what the figure shows.** Its limits are stated once,
  in the text.
- **V3-S5. Each caveat once.** In v2, "JOINT still sees each coupling twice
  as often" appears about six times. Keep a one-home map, as v2's
  STRUCTURE §7 does.
- **V3-S6. Cut theory that does no work** (PROF 4).
  - Remark 1 goes.
  - Prop. 4 becomes a remark in the appendix, in words, with its honesty
    note. Dropping it is the owner's alternative.
  - Keep what the environment's claims use (Props. 1–3, Thm. 1, Cor. 1),
    at the level v2 verified.
- **V3-S7. Write for a reader new to the project.** Plain sentences. Avoid
  the patterns in v2's `plans/P3.md` §6, and the 101 unclear sentences the
  blind review listed.

### Evidence

- **V3-E1. The interaction check:** step 0 below.
- **V3-E2. Theorem 1's toy** (BLIND W6). Read-only: check whether the stated
  signal model matches the implemented toy (`che/env/e2c.py`; the Phase-4
  report, the DX-14 source). Make the paper's statement match the code, or
  report the mismatch.
- **V3-E3. New numbers** need VERIFIED rows before use. Examples: the effect
  in agents per episode, and Γ₄'s and B̂'s detection limits (v2 Q18) if
  used.

### Verifiability

- **V3-V1. The anonymized code supplement** (PROF 5; PAPER V3 item 2(e)).
  - **Contents:**
    - the `che/` package, configs, tests and the scripts that reproduce the
      paper's numbers from committed artifacts;
    - the registration documents (`phase6_design_v2.md`,
      `phase6_framing_branches.md`);
    - a hash manifest.
  - **Checks:**
    - the CPU test suite passes inside the unpacked supplement;
    - a scrub check (names, URLs, absolute paths, hashes) passes;
    - its size is within TMLR's limit. Verify that limit on TMLR's own
      pages; the professor said "up to 100 MB", which is unverified.
  - **Owner decides** whether decision-log excerpts go in. They quote the
    owner.
- **V3-V2. A registration statement**, honest about its limits. The record
  is internal and version-controlled, its dates are self-reported, and the
  supplement carries the documents. Next time, a public registry (OSF).
- **V3-V3. §11 describes the supplement.** v2's Q4e is now settled for the
  supplement option.

### Carried from v2 (all still bind)

- **Checks:** M1–M4 and the kit checks: print clipping, iframe growth pins,
  `date_confirmed`, comment stripping.
- **Disclosure** (PAPER V3 item 6). The owner writes the `<d-footnote>`. The
  appendix "How this paper was made" starts from the builder's draft quoted
  in PAPER V3 item 6, and the owner edits it. Agents do not write the
  owner's footnote.
- **Open questions.** v2's open owner questions that PAPER V3 does not
  settle go into a new **one-page** `paper/v3/OWNER_QUESTIONS.md` at step
  4.5. The title is reopened for the new framing.

## Phase 1 process (v3)

Steps run in order, except where a step says it runs in parallel. Every
agent gets this file's rules and change list in its prompt.

### Step 0: the interaction check (prepared here, run by the owner)

1. **Before anything else, confirm two things with the owner.** Ask nothing
   else up front.
   - (a) Phase 1 starts.
   - (b) The interaction-check scope (PAPER V3 item 5): θ\* only (about
     1.7–2.7 GPU-h), or θ\* plus Low and High (about 5–8 GPU-h).

   Transcribe the answer before acting.
2. **The analysis plan:** `che/bench/results/phase6/post_v3_interaction/PLAN.md`,
   written and committed **before any run**.
   - **Conditions:** neither coupling, A only, B only, both, at each
     severity in scope. δ stays at θ\*'s value.
   - **Policies:** the final checkpoints of ISO (72), JOINT (72) and ISO-4
     (20).
   - **Eval draw:** the registered one (seed 0, 512 episodes), with common
     random numbers across conditions.
   - **Estimand, per policy and co-primary:** the interaction contrast
     I = J(both) − J(A) − J(B) + J(neither).
   - **The test:** per arm and pooled, intervals on seed dispersion, with
     the family correction stated.
   - **A measured eval self-floor on the run GPU.**
   - **Reading rules:** "no detectable interaction" is an exclusion with
     its bound.
   - **Labels:** post hoc, and what the analysis is blind to.

   Show the plan to the owner for an OK before the run.
3. **Configs and scripts, with tests on CPU (debug config).**
   - New configs for the three new conditions per severity, reachable from
     config (the locks rule). A test asserts their κ values, and that
     "both" equals θ\*.
   - A resumable run script that writes eval `.npz`/`.json`, `timings.txt`,
     provenance and a `tar.zst` archive with its `sha256`, and **asserts**
     them.
   - An analysis script that refuses to run before `PLAN.md` is committed.
   - `ruff` and the full CPU suite green; then commit.
4. **A runbook for the owner:**
   - rent the card (the RTX 5090 class, as for the grid);
   - restore the archives from the 2026-09-27 backup, verifying each
     against `SHA256_CKPT.txt`;
   - run;
   - copy the results back.
5. **When the artifacts return:**
   - verify their hashes;
   - run the analysis once;
   - commit the results and a report;
   - add VERIFIED ledger rows.

   Steps 1–3 do not wait for this. The abstract and the worked example's
   results are written after it.

### Step 1: three planners (parallel, independent; parallel with step 0)

Each writes `paper/v3/plans/P<n>.md`. Each cites the record, states what it
would not do, and measures, rather than guesses, the v2 printed page count
per section.

- **P1, the argument.**
  - The environment-first spine.
  - 3–5 title candidates.
  - The abstract's question, result and lesson, with the lesson conditional
    on the interaction check.
  - The section list, with each section's job and the rows that carry it.
  - What moves to the registration timeline, and what is cut.
- **P2, the Beyond PDF reading path.**
  - Which figures carry the environment's claims.
  - A figure for the interaction check.
  - Which v2 figures go.
  - Label-only rebuilds (v2 Q11), if the owner agrees.
  - How a 12–15-page main text uses the interactive figures.
- **P3, the referee's view.** What environment-paper reviewers need:
  - claims supported;
  - usability;
  - the code;
  - scope limits;
  - the page budget per section;
  - the up-front limitations.

  P3 also checks v3's plan against the professor's five points and BLIND
  W1–W10.

### Step 2: the code supplement (one builder, parallel with step 1)

Build `paper/v3/supplement/`. It holds:

- a packaging script;
- the scrub and size checks;
- a CPU test run inside the unpacked supplement;
- a manifest.

The output zip goes to `paper/v3/out/`. Report what goes in and why, and
anything that cannot be anonymized.

### Step 3: two builders, the v3 scaffold

- **B1, the content scaffold:**
  - `paper/v3/STRUCTURE.md`: which plan each choice came from;
  - `BRIEF.md`: v2's brief, re-verified only where v3 changes it, plus
    V3-* with an owner for each item;
  - `DISPOSITIONS.md` (not "FINDINGS.md");
  - section stubs with STUB-SPEC blocks;
  - the registration-timeline appendix stub;
  - writer assignments.
- **B2, build and checks.**
  - Copy `paper/v2/src/` to `paper/v3/src/` and adapt it.
  - Keep every v2 check.
  - Add these checks:
    - main-text printed pages ≤ 15;
    - no internal code or private-vocabulary term in the main text, from a
      list B1 owns;
    - no date in the main text outside an allow-list;
    - each caveat in the one-home map appears once.
  - Show each new check failing on v2's text (a negative control) before
    trusting it.

### Step 4: the final version

1. **Writers (4–5 in parallel)** fill the stubs. Each also writes
   `paper/v3/provenance/<section>.md`, with one row per sentence and its
   support, and new rows in `paper/v3/ledger_proposals/W<n>.md`. A writer
   whose text depends on the interaction check leaves a marked hole until
   step 0.5 lands.
2. **Reviewers, in independent lanes,** writing to `paper/v3/review/`:
   - claims, split across two agents, one of which owns whole-paper
     consistency;
   - numbers, split across two agents, covering every tag, every new row
     and all arithmetic;
   - mechanics: kit syntax, listings, formal statements against the theory
     doc, cross-references, double-blind, the page count, and the
     supplement.
3. **Fix and re-check.**
   - Writers fix their own files.
   - Reviewers re-check the changed lines against a snapshot diff, then do
     one final small pass.
   - Every finding's outcome goes in `paper/v3/REVIEW.md`. Compile it with
     `paper/v2/src/make_review.py`, copied into v3.
4. **The real-kit build:**
   - all checks green;
   - the private artifact, using `paper/v2/src/artifact_bundle.py`;
   - the `submission_folder` zip;
   - the printed PDF;
   - the supplement zip.

### Step 4.5: the owner and one blind reviewer

- **The blind review runs in a separate session** that the owner starts
  outside this repository. That stops `CLAUDE.md` loading into the
  reviewer's context, which happened in v2. Give it only the PDF, the
  submission folder and the supplement. If that is not possible, record that
  the review was not fully blind.
- **The owner gets:**
  - the artifact link and the PDF;
  - the provenance tables;
  - the changes from v2;
  - every open finding;
  - a one-page `paper/v3/OWNER_QUESTIONS.md`;
  - the blind review.
- **Nothing enters `paper/finale.md` until the owner rules.** This is the
  end of phase 1.

## What v2 taught, kept here so it is not relearned

- **Rows and provenance work.** Write the row first. Keep one provenance row
  per sentence. Use the strict checker (`provenance_check.py --strict`).
- **Snapshot before each review pass.** Re-check only the changed lines.
  Expect a last small round of fixes after the re-check.
- **Agents can stop on usage limits.** Resume them with SendMessage, from
  their own transcripts. Commit at the end of every step.
- **Builds overwrite each other.** Concurrent `build_v2.py` runs overwrite
  `out/`, so read the console summary. Run `kit_build.sh` only when nobody
  is editing.
- **Kit and artifact traps are fixed in `paper/v2/src/`. Do not undo the
  fixes.**
  - Prose pipes become tables.
  - Distill drops accents, and `--` page ranges render raw.
  - The explorer iframes grow without bound unless pinned.
  - Print clips wide tables and displays.
  - The artifact host refuses `.eot` and DOCTYPE'd SVG fonts.
  - MathJax fonts must be served locally in the artifact.
- **Count words one way:** P3's method, everywhere.
- **No finding without an outcome.** Every finding gets a recorded outcome,
  and `make_review.py` lists the gaps.

## Hand-back to the owner (each phase)

Keep it short:

- what changed;
- what is waiting on the owner's decision;
- the findings that are not fixed, and why;
- where to look: paths and the artifact link.

Never report a check as passed unless it ran in this session.
