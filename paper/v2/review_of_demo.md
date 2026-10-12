# Review of the demonstration (Paper v2, phase 1, step 2)

Step-2 reviewer, 2026-10-11. Scope: `paper/demo_beyond/` (sections, `REVIEW.md`,
`KIT_BUILD.md`, `BRIEF.md`, `ledger_supplement.md`, `src/build_demo.py`,
`submission_demo.md`, `out/index.html`), read against the record. The record
here means the decision log from UNBLIND RESULT (`docs/decision_log.md:4978`)
to the end, the ledger, `paper/branch_B.md` §5 and §8, `docs/theory_foundations.md`,
`paper/related_work_verification.md`, `paper/beyond_pdf/KIT_NOTES.md` and the
committed result reports. Companion file: `paper/v2/citations/C1_verification.md`.

**How to read the labels.**

- **checked from source this session** means I re-derived it here, from the
  section files, the `.bib`, the kit's own files or a committed report.
- **per KIT_BUILD.md, prior session, not re-run** means it rests on the
  2026-10-11 kit build record.
- **UNVERIFIED** means I could not check it.

Line numbers are per section file (`sections/NN_*.md:line`) unless a path is
given.

**What I ran.**

- My own scans, in the scratchpad: pipes, bib markup, a Distill-normalization
  emulation, word counts, jargon counts and tag sampling.
- A diff of the six listings against the tree, which is clean apart from
  `paper/v2/`.
- I read the kit zip in place (sha256 `e531434b…bacc2d5`, equal to
  `KIT_NOTES.md` §S1.1), plus kramdown 2.4.0's `table.rb` and the GFM
  parser from their public repositories.
- **No kit build, no test run, no project code.** Nothing outside `paper/v2/`
  was edited.

---

# Part 1. Findings

## 1.1 The owner's fix list

### M1. The |Δ| table bug: CONFIRMED, and the trigger CORRECTED

- **Locations, checked from source this session.** Exactly two prose lines
  carry unescaped pipes outside code spans and outside Markdown tables:
  - `09_compositional_test.md:134` ("… max |Δ| = 2.44 × 10⁻⁴");
  - `11_reproducibility.md:7` (same phrase).

  The assembled `submission_demo.md` shows the same two lines (`:863`,
  `:901`). The abstract has none.
- **Source table count:** 17 intended Markdown tables, checked from source
  this session. They are §2: 1, §3: 1, §4: 1, §9: 3 and App.: 11.
- **The kit's 19:** the fix list records 19 tables in the kit build
  (`paper_v2_prompt.md:99`). That count is not in `KIT_BUILD.md`, so it is
  per the builder's 2026-10-11 verification, not re-run.
- **Correction to the trigger.** The fix list says "two pipes". kramdown
  2.4.0's table parser (`kramdown/parser/kramdown/table.rb`, tag REL_2_4_0)
  is stricter than that:
  - `TABLE_PIPE_CHECK = /(?:\||.*?[^\\\n]\|)/`. A line at a block boundary
    with **one** unescaped `|` outside a code span starts a table, and a
    single row is a table.
  - Code spans protect a pipe. **Math does not**, because table detection
    runs before math, so `$|x|$` would also split a row.
  - The GFM input (kramdown-parser-gfm) keeps this parser unchanged. Only
    the fenced-code and ATX-header parsers are swapped.
  - List-item and blockquote content is block-parsed too. Raw HTML blocks
    are safe, because `:block_html` precedes `:table` in the parser order.
  - No demo line has exactly one pipe, so the observed 19 against 17 fits
    either rule.
- **Fix:** as listed. Write `$\lvert\Delta\rvert$`, or "largest absolute
  difference".
  - Better still, state the cross-card figure once (it is also a
    restatement, see N16) and point back to it.
  - B2's checks should be two:
    1. **Source side:** fail on any unescaped `|` outside code spans in a
       non-table, non-HTML line, math included.
    2. **Kit side:** the kit table count equals the source count.

### M2. Broken references: CONFIRMED, with the list CORRECTED and extended

What Distill renders and how is checked from kit source this session:

- **Fields rendered:** title, url, author, year or date,
  journal/booktitle, volume, number/issue, pages, publisher and doi. This is
  `bibliography_cite`, `venue_string` and `hover_cite` in the kit's
  `template.v2.js:960-1060`. `editor` and `month` are never rendered.
- **Normalization:** `normalizeTag` (`template.v2.js:1976-1981`) collapses
  whitespace. It reduces any brace-wrapped accent macro `{\X c}` to the
  **bare letter, dropping the diacritic**, for X one of 12 characters:
  double quote, caret, backtick, period, apostrophe, a, c, u, tilde, H, v
  and s. It reduces `{\i}` to `i`.
- **`KIT_NOTES.md` §S1.5 understates this.** It says only `{\"a}` and `{\i}`
  are handled, and that they are "resolved".

I applied the same regexes in Python to every rendered field of the 40
entries (this session, an emulation, not a render):

| what the reader sees | entries (field) |
|---|---|
| **raw TeX braces** | `liu2026vulcan` title `{VULCAN}`; `agrawal2023multimodal` title `{MARL}`; `bernstein2002` title `{M}arkov` |
| **raw math** | `kesten1980` title `$\frac{1}{2}$` |
| **raw macros** | `rutherford2024jaxmarl` author `Gar\dh ar` **and** `Rockt\"{a}schel`; `jiang2021robustplr` author `Rockt\"{a}schel`; `cakir2025jaxwildfire` author `{\c{C}}akir` |
| **raw `\&`** | `zscheischler2020typology` journal |
| **`--` page ranges** (22 entries) | bernstein2002, kesten1980, grassberger1983, haksar2018, pynadath2002, rutherford2024jaxmarl, bettini2024benchmarl, lu2022dpo, dennis2020paired, jiang2021plr, jiang2021robustplr, parkerholder2022accel, tobin2017dr, zhao2020simtoreal, kirk2023zsg, hsiung2023compositional, mendez2022composuite, zscheischler2018compound, zscheischler2020typology, crain2008stressors, garcia2015safe, matthews2024craftax |
| **diacritic silently dropped** (no raw TeX, but misspelt) | `erdem2025mixed` "Ure, Nazim" (the paper's own prose says Üre); `keysers2020` "Scharli"; `jiang2021plr`, `parkerholder2022accel`, `kirk2023zsg` "Rocktaschel"; `zhao2020simtoreal` "Pena Queralta"; `zscheischler2020typology` "Jezequel, Aglae"; `cote2016stressors` "Cote"; `cakir2025jaxwildfire` "akir" (ı lost) |
| never rendered | `tramer2019multiple` editor; `matthews2024craftax` month |

- **`KIT_BUILD.md` difference 1 disagrees with the kit's source in two of its
  examples.**
  - It lists `C{\^o}t{\'e}` as raw. Per `normalizeTag` that entry renders
    "Cote", which is wrong but not raw.
  - It lists `{\c{C}}akır` with a dotless ı. The kit turns `{\i}` into a
    dotted i.
  - The dotless ı matches the demo preview's own emulation
    (`src/build_demo.py:131-137` maps `{\i}` to U+0131). So those examples
    may come from the preview, not the kit page (UNVERIFIED which).
  - The step-3 kit build must re-check every rendered entry and every hover
    card, as the fix list says.
- **Records behind the fix (side check, this session, Crossref API):**
  - `kesten1980` comes back as "…equals 1/2" with pages "41-59".
  - `bernstein2002` comes back as "…of Markov Decision Processes" (no
    braces).
  - So Unicode or plain-text entries match the records.
  - **The fix as listed stands:** Unicode at the source in
    `related_work_verification.md`, an en dash in `pages`, then re-copy all
    40 entries verbatim.
- **Citation resolution, checked from source this session:**
  - 55 `<d-cite>` tags with 38 distinct keys, all in the bib.
  - `jaderberg2017pbt` and `zhao2020simtoreal` are uncited. That fits
    `KIT_BUILD.md`'s 38-entry reference list.
- **Cross-references, checked from source this session:**
  - Every `§N` and `§N.k` target, every Figure 1–13, J1 and J2, Listings 1–6
    and Appendices A–J exists.
  - One pointer is partial: `09_compositional_test.md:15` sends the reader
    to "(§6)" for evidence from M3.5 and M4.4. M3.5 is in §5.

### M3. Empty BibTeX year: CONFIRMED, plus two kit details

- **Front matter, checked from source this session.**
  - `submission_demo.md:1-26` sets `layout`, `title`, `description`,
    `htmlwidgets`, `authors` (Anonymous), `bibliography`, `toc` and
    `_styles`.
  - It sets no `date`, no `submitted_date` and no `openreview_id`.
- **The kit's layout, checked from kit source this session.**
  - `distill.html:23` sets `publishedWhen = "{{ page.date | date: '%B %-d, %Y' }}"`,
    and `:38` writes `year = {${publishedWhen}}`.
  - So with `date` set, the box's `year` field holds a **full date** such as
    "October 11, 2026", not "2026". That is the kit's format and authors
    cannot change it.
  - The academic-attribution line hard-codes 2026 (`:52`).
- **`submitted_date` is visible on the page.**
  - `distill.html:89` passes it to Distill's front matter.
  - Distill's byline (`template.v2.js:2099-2122`) prints "Submitted: *Not
    submitted yet.*" when it is unset.
  - The demo preview replaced this with its own line, so the preview never
    showed it.
- **Fix:** as listed, with `date` set by the owner. Decide `submitted_date`
  knowing it fills the byline (owner question Q2).

### M4. HTML comments: CONFIRMED, count reconciled

- **Count, checked from source this session.** `submission_demo.md` holds
  869 `<!--`:
  - 856 `<!-- N:ID -->` ledger tags (17 in the abstract, 839 in the
    sections);
  - 13 line-1 labels, "BUILDER-WRITTEN DEMONSTRATION … not the owner's
    text".

  This equals `KIT_BUILD.md`'s 869.
- **The labels must not ship in v2.** They would be false for an
  owner-approved paper, and the disclosure footnote replaces them (PAPER V2
  item 2).
- **Facts for the owner's question, checked from kit source this session.**
  - The kit's README tells authors to upload `submission_folder.zip` to
    OpenReview, and TMLR's system builds the public page from it. The raw
    `submission.md` therefore travels in the upload. Whether reviewers can
    download the zip on OpenReview is UNVERIFIED.
  - `jekyll-minifier` is in the kit's Gemfile and `_config.yml`. It removes
    comments only in a production build. Whether TMLR's site builds in
    production is UNVERIFIED (`KIT_NOTES.md` §S1.7 says the same).
- **Sibling item, the bib's `%` lines.**
  - `submission.bib:1-4, :27, :183, :194, :204, :298, :309, :394, :406`
    carry process notes, such as "READ by the owner 2026-10-10" and paths to
    `paper/related_work_verification.md`.
  - The bib is served publicly under `assets/bibliography/`.
  - WRITING ROLES already lists "% lines" with the comments as OWED
    (`docs/decision_log.md:5474-5485`).
- **Fix:** as listed. Keep tags in the repository copy and generate a
  stripped staging copy with 0 `<!--` and 0 `%` lines. Owner question Q1
  covers the OpenReview upload.

### C1. Corollary 1(3) and (4): CONFIRMED, and the error is in the theory doc too

Full record: `paper/v2/citations/C1_verification.md`.

- **Theory doc** (`docs/theory_foundations.md:210-225`, tagged [CITED]):
  > 3. **Critical scaling.** … $\chi(\beta) \sim |\beta - \beta_c|^{-\gamma_p}$
  > with $\gamma_p = 43/18$, and $\xi(\beta) \sim |\beta - \beta_c|^{-\nu_p}$
  > with $\nu_p = 4/3$ (2D percolation universality).
  > 4. **Supercritical** … the burnt region grows linearly in time with an
  > asymptotic front speed $v(\beta) > 0$ and a deterministic limiting shape
  > (shape-theorem behavior for spatial epidemics).

  No source is given for either. **Record item for the owner.**
- **Demo locations:**
  - `04_severity.md:22-23`.
  - **Also carried into Proposition 3:** "diverges as β ↑ β_c like
    |β − β_c|^{−43/18}" (`05_coupling_a.md:68`; "the divergence is
    Corollary 1", `:70`). The theory doc has it at `:309-311`.
  - App. A repeats it: "The divergence rate is Corollary 1(3)"
    (`12_appendix.md:23`; theory doc `:318`).
  - `03_environment.md:28`'s notation note exists only because of the
    exponents.
- **(3) verified level.**
  - Proved by Smirnov & Werner (2001, Theorem 1) for **site percolation on
    the triangular lattice**, and only up to o(1) in the exponent:
    χ(p) = |p − ½|^{−43/18+o(1)}.
  - **Not proved for bond percolation on ℤ²**, where the values are the
    universality conjecture. Grimmett & Manolescu (2013) prove agreement
    across bond lattices "assuming the exponents exist" and make "no
    progress … on the problem of existence".
  - The builder's understanding is confirmed. One sharpening: "∼"
    overstates what is proved on any lattice.
  - **Recommendation: drop (3), and drop the 43/18 rate from Proposition 3.**
    The alternative is a conjecture with a citation.
- **(4) verified level.**
  - With ι = 0, one ignition and Prop. 2's coupling, the region burnt by
    step t is the chemical-distance ball of radius t in the open cluster.
    This is my derivation, in the C1 file.
  - For supercritical bond percolation on ℤ², conditioned on the origin
    being in the infinite cluster, that ball rescaled by t converges almost
    surely in Hausdorff distance to a deterministic convex compact set with
    non-empty interior. This is Garet & Marchand (2004, Corollary 5.4,
    p. 188), proved for all p > p_c.
  - Cox & Durrett (1988, (1.4), p. 174) state the same for this "burning
    percolation cluster" without a full proof.
  - **It falls short of the current wording on one point.** "An asymptotic
    front speed v(β)" is a single number, but the speed depends on direction.
    The limiting set is symmetric only under coordinate permutations and
    reflections.
  - **Recommendation: state (4) at the verified level with
    `garet2004chemical`**, entered through `related_work_verification.md`
    in step 3. Otherwise drop it. Nothing depends on it.
- **Related item outside C1's scope:** see N7 (the uncited "universal"
  caveat and Cor. 1(2)).

### C2. Remark 1: CONFIRMED, and the theory doc carries it too

- **Theory doc** (`docs/theory_foundations.md:163-168`):
  > Finite-horizon Dec-POMDPs are NEXP-complete (Bernstein, Givan, Immerman,
  > Zilberstein, 2002). With comms denial ($\delta > 0$) the CHE does not
  > collapse to an MPOMDP, so the hardness framing applies and justifies the
  > learning-based (rather than planning-based) approach.

  **Record item for the owner.**
- **Demo locations:**
  - `03_environment.md:36`: "so this hardness applies; it is why we learn
    policies rather than plan".
  - `01_introduction.md:7`: "so we learn policies rather than plan (Remark 1)".
  - The owner's §1 has the same at `paper/finale.md:52-55`.
- **What the cited work licenses.** The UAI 2000 version of Bernstein et al.
  (arXiv:1301.3836) says the problems "most likely require doubly
  exponential time to solve in the worst case". I read that abstract this
  session; the 2002 journal version's abstract was not read.
  - That is a worst-case result for the class. It licenses "no general
    exact planner is expected to scale", not hardness of CHE's instances.
- **Second defect, the condition "δ > 0".** CHE does not reduce to an MPOMDP
  at δ = 0 either. Links are range-limited (Chebyshev R_comm = 16 on a
  64-cell side, COM-6, DX-17), delivered one step late, and carry a frozen
  projection rather than observations (ENV-12). θ\* has δ = 1. So the
  sentence's condition is not the operative one.
- **Fix:** as listed, and drop "(δ > 0)" or reword it.

### C3. Proposition 4: CONFIRMED, locations CORRECTED, plus a stronger problem

- **Theory doc** (`docs/theory_foundations.md:610`, `:620-625`):
  > Proposition 4 (Why the hypothesis is plausible: an irreducible shift
  > term for ISO) [PROVEN, bound-shaped] … the transfer guarantee available
  > to ISO carries an **irreducible slack** $\propto \varepsilon_{\min}$,
  > whereas JOINT trains at $\varepsilon = 0$ on the element combination
  > (slack only in the held-out severity direction).

  **Record item for the owner.**
- **Where "irreducible" actually is (checked from source this session):**
  `09_compositional_test.md:17` (title), `:23` ("an irreducible slack") and
  `12_appendix.md:31` (title).
- `01_introduction.md:39` and `10_limitations.md:23` contain no
  "irreducible". They already say the bound limits what ISO "can be
  guaranteed" to transfer. They need only the new name if they use one.
- **Fix:** as listed. Rename it, for example "A transfer upper bound for
  ISO", and say what the bound cannot certify.
- **Stronger problem:** see N6. At CHE's scale the bound is not informative
  for any arm, and the "JOINT trains at ε = 0" contrast does not follow from
  the stated ε.

### F1. Retitle: CONFIRMED

- **Current title** (`paper/finale.md:3`): "A multi-agent fire environment
  with a hazard-blind reward, and a pre-registered test …". It leads with
  the hazard-blind reward.
- **Kit constraints, checked from kit source this session.**
  - The title is interpolated into a JavaScript string
    (`distill.html:24`) and into the `<h1>` raw (`:130`).
  - So it must be one line, with no `"`, no backslash, and no `<` or `&`.
- **Ruled constraints that still stand:**
  - "multi-agent", not "swarm";
  - "stressor" for the elements and "ambient hazard" for the fire;
  - "pre-registered" attaches to the test.
- Nothing may imply a composition effect (`writing_session_prompt.md:233-245`).
- The TITLE ruling's "the environment is not named" was a choice for the old
  title (`docs/decision_log.md:5610-5620`).
- **Reviewer's candidates,** to be merged with P1's (the owner chooses):
  1. *A pre-registered test of joint versus isolated training on co-occurring
     stressors, in a multi-agent environment with an ambient fire hazard*.
     Leads with the test; no result.
  2. *Co-occurring or isolated stressors in multi-agent reinforcement
     learning: a pre-registered test whose survival gain does not survive the
     inert-share correction*. Leads with the question and the corrected
     result. Long.
  3. *Matched compute, unmatched active share: a pre-registered test of
     training on co-occurring versus isolated stressors*. Leads with the
     design lesson. F4 risk: it can read as a rule.
  4. *Training on co-occurring stressors in a multi-agent fire environment:
     a pre-registered null after an inert-share correction*. Leads with the
     outcome. Risk: "null" undersells completion's exclusion.

### F2. Abstract leads with the plain result: CONFIRMED

The current abstract (`paper/finale.md:13`, 2,424 characters, under the
5,000 limit, ABSTRACT entry item 4) leads with the environment. Defects that
v2's rewrite must not carry over:

- **OWNER ITEM 1:** "As predicted before measurement".
- **N9:** "each stressor is a parameter of one transition kernel".
- **N10:** both registered strings appear only in paraphrase ("does not
  survive an inert-share correction registered before unblinding"; "Neither
  … keeps a stable sign over the final half").
- **N10:** the completion null has its interval but not its bound ("excludes
  a gain larger than 0.66 points", RES-1).
- **N11:** B̂ is stated as an effect ("raises isolated training's survival by
  0.98 points") with no interval and no "no registered test".
- **F4:** "should therefore".

Must keep:

- the inert-share qualifier, verbatim;
- "sign unstable over the final half" on both co-primaries, with the
  survival gap opening in the last fifth and the completion lean from 70 %
  (RES-11, RES-12, RES-13);
- matched compute;
- 72 seeds as a recorded deviation (DES-3, DES-1);
- δ inert under the frozen encoder at this scale, so a third fire-only
  (DES-8);
- ISO-4 with 20 seeds (DES-13);
- Γ₄ with its interval (RES-6);
- "still sees each coupling twice as often and always in combination"
  (DES-14).

`description` (`paper/finale.md:4`) passes the kit checks: one line, no `"`,
no backslash, no ": ". It restates the old abstract's opening (DESCRIPTION
entry item 3). Re-check it once the abstract no longer opens on the
environment.

### F3. The δ confound as a design error: CONFIRMED, facts CORRECTED

- **Locations, checked from source this session:**
  - `01_introduction.md:37`: "The fire-only third was registered as a bias,
    with ISO-4 to remove it".
  - `09_compositional_test.md:49`: "**Registered biases, stated before the
    result.**" and "Registered on 2026-09-18 with its direction".
  - `09_compositional_test.md:136`: "A registered design caught it".
  - `10_limitations.md:5`: "properties of the design, registered or recorded
    before the outcome was known".
  - The owner's §1 has "We registered this bias" (`paper/finale.md:113`).
- **The timeline in the record is not "proved inert … found mid-grid".**
  1. **δ was certified inert before the Phase-6 design was registered.**
     This was M5.5 and the M5.3 closure, 2026-07-30
     (`docs/decision_log.md:1065`, `:1153`, `:1211`).
  2. Design v2 (rulings of 2026-08-02) states "comms **certified inert**
     (M5.3/M5.5) and retained in θ\* for registration fidelity"
     (`phase6_design_v2.md:30-33`).
  3. It still gave δ-only components a third of ISO's mixture (`:69-71`),
     while excluding δ from the sweeps *because* it is inert (`:129-132`).
  4. Its own review question rested on "Neither protocol trains on δ = 1.0"
     (`:431`). That is false for both arms: `p6_iso.yaml:43, :46` and
     `p6_joint.yaml:36-37` carry δ = 1.0.
  5. **The consequence was found pre-grid.** It is in the venue review dated
     2026-08-16, §4, "A registered-halfway bias in the confirmatory
     contrast" (`docs/venue_review_2026-08-16.md:11, :112-163`). It closes:
     "The confirmatory arm applies a different rule to the same fact" (`:162-163`).
  6. It was carried "AWAITING RULING" and **registered mid-grid on
     2026-09-18**, with 120 of 252 runs done, on the owner's attestation
     that no outcome mean had been viewed (`docs/decision_log.md:3902-3917`).
- **Direction:** say plainly that:
  - the design kept an element it had already found inert;
  - it applied inconsistent rules to it;
  - it did not count the resulting fire-only share;
  - a review caught this three days after the outcome branches were
    registered, before the grid ran;
  - the correction was registered mid-grid, before unblinding.

  Keep the dates and the ISO-4 rule, and drop the foresight framing
  ("registered as a bias", "a registered design caught it").
  The exact wording is the owner's (Q4h).

### F4. Advice separated from "therefore": CONFIRMED

- **Locations, checked from source this session:**
  - `paper/finale.md:13`: "Studies of compositional generalization should
    therefore match …".
  - `01_introduction.md:39`: "The argument is general …".
  - `01_introduction.md:46`: contribution 4, "a rule whose argument is
    general: match the active share …".
  - `09_compositional_test.md:136`: "**Discussion.** Match the active share
    before claiming composition."
  - `10_limitations.md:27`.
  - The owner's §1 contribution 4 reads "points to a rule"
    (`paper/finale.md:177`).
- **Direction:** one labelled recommendation, for example "We recommend
  …, motivated by this result in one environment". Use it once, in §9.2 or
  the discussion. Elsewhere, point to it. "Rule" goes.

### F5. Jargon in §9: CONFIRMED, counts below

Method: whole file with HTML comments removed (they do not render), case as
written, alt and title attributes included. Checked from source this session.

| term | §9 count | lines |
|---|---|---|
| card (7 "card", 2 "cards", 2 "same-card", 2 "single-card") | 13 | 43, 45, 49×2, 59, 69, 83, 94×2, 104, 111, 134×2 |
| ladder (5 in text and attributes, plus 2 in the asset filename `ladder_registered_readings`) | 7 | 43, 65, 68×2, 73, 81, 88 |
| rung | 6 | 65×2, 69×4 |
| `sweep_c50…` | 7 | 47, 69, 83, 94×3, 119 |
| re-floor | 4 | 43×3, 49 |
| S1–S6 labels | 4 | 59, 69, 83, 94 |
| floor-basis | 3 | 69, 130, 134 |
| beat-reproducibility | 2 | 41, 134 |
| Γ₄′ | 9 | 59, 69×2, 83, 94, 119×2, 126, 134 |

All nine counts match the fix list's; "ladder" matches only when the two
filename occurrences are included. Other §9 internal terms:

- "unit" in the GPU sense: about 15;
- "prefix": 6;
- `k_req`: 2;
- B̂: 15.

**Same pass over the other sections** (same method):

| section | internal terms |
|---|---|
| §8 | card 10; M-milestone labels (M4.4, M5.3, M5.3b, M5.5, M6.0) 6; m44/m35 2; floor-basis 2; re-floor 1; beat-reproducibility 1 |
| §10 | card 4; unit 5; Γ₄′ 2; "Phase-N" 3 |
| App. | card 17; unit 14; `sweep_c50…` 9 and `ident_c40…` 3; S-labels 7; re-floor 5; ladder 5; M-labels 9; G1.2 1 |
| §5 | m44 5, m35 5 ("the Coupling-B grid m44"); "Phase-3" |

Direction:

- Give each internal name a plain name once, for example "the Coupling-B
  grid" and "the Coupling-A grid".
- Keep M-labels only in App. C's study column, with a key.
- Name Γ₄′ "the same-GPU replicate".
- Keep the registered strings verbatim.

### OWNER ITEMS 1–4: CONFIRMED (all in the owner's own text)

1. **"As predicted before measurement"**, at `paper/finale.md:13, :159-160`.
   - E1.1's prediction was registered before its own analysis
     (`che/bench/results/e1/e11_report.md:12-27`).
   - Its CORRECTION records that the trained ordering and its fuel cause
     were already on record in Phase-4 Result 4 (`:170-197`).
   - What predates any trained policy is the lock's random-policy
     observation, ≈ 5.7× fuel-limited at every κ_A (`coupling_a_lock.md:45-50`,
     `:82-90`; DX-9).
   - **The demo already says this correctly** (`01_introduction.md:44`;
     `05_coupling_a.md:80`). Only the owner's abstract carries the phrase.
2. **Proposition 1's finiteness.**
   - The theory doc's proof says "$\mathcal{S}$, … and $\Omega_i$ are
     finite, so $\mathcal{M}_\theta$ is a finite Dec-POMDP"
     (`docs/theory_foundations.md:151-153`).
   - That is false with $\mathcal{P} = \mathbb{R}_{\ge 0}^G$ in the state
     (`:40`, `:53`).
   - Def. 1's observation line is stale (`:62-63`: $O^i_{\kappa_B}(o_i \mid
     x, h, c, k)$, with no ρ and pre-step).
   - The owner's §1 says "finite Dec-POMDP" (`paper/finale.md:51-52`).
   - **The demo fixed it.** It uses one reachable-set argument in §3 and
     App. A (`03_environment.md:32`; `12_appendix.md:11, :13`), and §1 says
     "whose states reachable within the horizon form a finite set"
     (`01_introduction.md:7`).
   - `HANDOFF.md:227` still lists "the theory-doc ρ amendment" as open. The
     ρ amendment was applied 2026-10-10 (log:5888-5960, C11); only this
     finiteness line remains. **Record item.**
3. **"every arm is perturbed throughout"**, at `paper/finale.md:310-311`.
   - Part 3 records six training arms, including the unattacked
     Non-Robust baseline (`paper/related_work_verification.md:1004-1012`).
   - The demo's repair, "Every adversarially trained arm is perturbed
     throughout" (`02_related_work.md:31`), is still a shade strong. Part 3
     says the attack "is computed at every step (Alg. 1)", is "a capped
     magnitude that may be near zero (unreported)", and that "every arm
     perturbed at every step" holds "by inference only" (`:918`, `:1010-1014`).
   - Accurate form: "in each adversarially trained arm an attack is computed
     at every step (their Algorithm 1)".
   - **Ruling-level:** READS RULING item 2 recorded both phrases as "Left as
     written, by the owner's call" (`docs/decision_log.md:5760-5765`). See Q4a.
4. **"about seven percent"**, at `paper/finale.md:217-218`.
   - CA-9 gives 7.4–8.3 % as an increase over the base count and 6.9–7.6 %
     as a share. "Agents add about … seven percent to the number" is an
     increase, so it rounds to about eight.
   - **The demo states the range** (`02_related_work.md:21`).
   - Same ruling-level note as item 3.

### OWNER ITEMS 5–6: reported (record fixes, CONFIRMED)

5. **M5.3's floor "on different hardware".**
   - The claim: `CLAUDE.md:344` and `docs/decision_log.md:1194` ("a
     different card").
   - The record: `che/bench/results/phase5/m51e/provenance.txt` and
     `…/m53/provenance.txt` both record "NVIDIA GeForce RTX 5090".
   - Provenance records the card model, not the unit, so "different
     hardware" is unsupported rather than proven false.
   - The demo avoids the phrase (`08_methodology.md:18`).
6. **`phase4_report.md:366`.**
   - It says "a sixth to a quarter" against its own table at `:362-364`
     (0.0809, 0.0560, 0.2424).
   - `:394-395` ("at or above the random-policy ceiling at every severity")
     holds for the κ_B = 1.0 arm only. The κ_B = 0 arm reads 0.0258 < 0.0279
     at Low and 0.1016 < 0.1278 at Medium (`:390-392`).
   - The demo scopes it correctly (`06_coupling_b.md:83`).

### KIT_BUILD.md differences

1. **Reference-list LaTeX:** this is M2, above. Two of its examples disagree
   with the kit's source.
2. **Long code lines cut on screen.** Per KIT_BUILD.md, prior session, not
   re-run.
   - From source this session: 37 listing lines exceed 72 characters, with a
     maximum of 85. Listing 1 has 17 of its 61 lines over 72 (`03_environment.md:43-104`).
   - The six listings are byte-identical to the tree, checked this session.
   - **Direction:** a `_styles` rule such as
     `d-article pre { white-space: pre-wrap; }` keeps the bytes. Untested in
     the kit. Shorter contiguous ranges also work: Listing 1 could stop at
     the reward line.
3. **869 comments:** this is M4, reconciled above.
4. **Kit navbar, footer and sidebar contents** at ≥ 1280 px. Per
   KIT_BUILD.md, not re-run. No action; preview-only difference.

### Length: CONFIRMED and CORRECTED (the overrun is general)

Prose word counts (scratch script).

- **Method:** HTML comments, Liquid, HTML tags and code fences removed.
  Figure blocks and caption paragraphs are counted separately. Each math
  span counts as one word.
- `REVIEW.md` used a different count (§3 ≈ 2,660, §9 ≈ 3,350, App.
  ≈ 5,470).

| section | prose | captions | brief target (`BRIEF.md` §C) |
|---|---|---|---|
| hero | — | 147 | caption ≤ 150 |
| §1 | 1,401 | 340 | 900–1,200 |
| §2 | 1,717 | 0 | 900–1,300 |
| §3 | 2,583 | 128 | 1,400–2,000 |
| §4 | 1,076 | 212 | 700–1,000 |
| §5 | 1,376 | 225 | 700–1,000 |
| §6 | 1,784 | 274 | 1,000–1,400 |
| §7 | 1,371 | 156 | 700–1,000 |
| §8 | 1,524 | 199 | 900–1,300 |
| §9 | 3,485 | 689 | 2,000–2,800 |
| §10 | 1,069 | 0 | 700–1,000 |
| §11 | 476 | 0 | 300–500 |
| App. | 3,996 | 329 | as needed |
| **total** | **21,858** | **2,699** | |

Ten of the eleven body sections exceed their upper target, not only §9 and
the appendix. The biggest single source is restatement (N16); see the
section decisions in Part 2.

## 1.2 New findings (reported to the owner before any fix)

Kinds: **[mech]** mechanical, **[corr]** correctness, **[fram]** framing.

### N1 [mech]. The disclosure footnote will not print on the first page as a footnote

- **Evidence:** the kit layout places `<d-footnote-list>` inside
  `<d-appendix>`, after the article (`distill.html:161-164`), and
  `overrides.js:2-9` styles `d-footnote`. A `<d-footnote>` therefore shows
  on page 1 as a superscript and hover box. Its text is listed at the end of
  the page, and of the browser-printed PDF.
- TMLR's FAQ asks for the disclosure "as a footnote on the first page"
  (PAPER V2 item 2).
- `BRIEF.md` §B3 told writers to avoid `<d-footnote>` as unverified, and
  `KIT_BUILD.md` did not test it.
- **Direction:** test it in the step-3 kit build, screen and print. If the
  text lands at the end, the owner decides on an alternative, such as a
  visible first-page note beside the abstract (Q4f).

### N2 [mech]. The demo's preview cannot catch M1 or M2, and it reads the wrong title source for v2

- `src/build_demo.py:286-287` renders with markdown-it's GFM table rule,
  which needs a delimiter row. So prose pipes never become tables in the
  preview.
- Its `_distill_tex` (`:131-137`) emulates `normalizeTag` incorrectly (see
  M2).
- It reads the title, `description` and abstract from `paper/finale.md`
  (`:71-79`). In v2 these are builder-drafted and must not come from
  `finale.md` until the owner approves them.
- It is invoked as `.venv/bin/python` (`:18`, `README.md:23`), which does
  not exist in this container.
- **Direction (B2):**
  - read front matter from `paper/v2/`;
  - make the M1 source check and the kit-side table count the real checks;
  - drop the emulated reference list, or port the kit's exact regexes;
  - drop the line-1 label requirement (`:472-474`).

### N3 [mech]. The bib's `%` lines are public

Covered under M4. Listed separately because the WRITING ROLES OWED item
names it and B2 must strip it.

### N4 [corr]. Record items in builder bookkeeping

- **`KIT_NOTES.md` §S1.5:**
  - It says `normalizeTag` "only … strips accent macros of the exact forms
    `{\"a}` and `{\i}`".
  - The kit's code strips any `{\X c}` form for 12 accent characters, and
    drops the accent rather than resolving it.
- **`KIT_NOTES.md` §S4:** its "8 rendered fields" (37-entry era) omits:
  - the 22 `--` page ranges;
  - `rutherford2024jaxmarl`'s second raw macro;
  - all silent diacritic drops.
- **`paper/branch_B.md:225`:**
  - It quotes the registered branch-B headline as "compound stress is paid
    in agents".
  - The registration reads "composition is paid in **agents**, not task
    return" (`phase6_framing_branches.md:102`).
  - The demo quotes it correctly (`12_appendix.md:178`, `09_compositional_test.md:92`).
- Report only.

### N5 [corr]. A second registered document premise

- Design v2 asks its reviewers about "§1's δ retention. Neither protocol
  trains on δ = 1.0" (`phase6_design_v2.md:431`). Both do (see F3).
- Registered documents are never edited, so this is report only. It is the
  record of the design error F3 asks v2 to own.

### N6 [corr]. Proposition 4's bound is not informative at CHE's scale, and the JOINT contrast does not follow

- **Status:** reviewer's derivation, this session, for the owner to check.
  No number below is for the paper without a ledger row.
- **The derivation.**
  - The trivial bound is |J_θ − J_θ′| ≤ 2R_max/(1 − γ). The proposition's
    right side divided by it is γε/(2(1 − γ)).
  - So the bound is weaker than the trivial one whenever γ > 2/(2 + ε).
  - ε is a supremum over (s, a) of two L1 terms, each at most 2.
  - **Every** training configuration, JOINT's included, has β ∈ {0.43, 0.70}
    ≠ 0.49 (CAL-3). A single Burning–Fuel edge therefore gives a
    transition-L1 of at least 2 × 0.06 = 0.12, so ε ≥ 0.12 for ISO and
    JOINT alike.
  - Then γ > 0.943 already makes the bound vacuous. The training discount is
    0.99 (DX-2).
  - For ISO's A-only and δ-only configurations (κ_B = 0 against θ\*'s 1.0),
    the observation term alone can approach 2 on smoky rays (τ ≈ 0 against
    τ = 1).
- **Consequences:**
  1. The bound certifies nothing at this scale, for either arm.
  2. "JOINT trains at ε = 0 on the stressor combination" (`09_compositional_test.md:23`;
     theory doc `:623-625`) is not a quantity the stated ε defines. ε is one
     supremum, and JOINT's configurations differ from θ\* in β.
- The honesty note (bounds guarantees, not outcomes) stays true.
- **Direction:**
  - keep Proposition 4 as a renamed upper bound, with the honesty note;
  - drop the ISO-vs-JOINT slack contrast;
  - say it motivates where to look and certifies nothing here; or move it to
    App. A.
- **Record item** for the theory doc. Owner question Q4i.

### N7 [corr]. Corollary 1's caveat sentence and item (2) are uncited

- `04_severity.md:25`, from theory doc `:227-232`, says "the existence of
  the transition and the divergence of χ and ξ near it are universal" for
  other neighbourhoods, heterogeneous fuel, wind or geometric burn times.
  - No source is recorded.
  - Cox & Durrett (1988, pp. 172-173, 177) show that random burn times
    change the percolation structure (locally dependent bonds), and that
    the diagonal-neighbour discrete model was open to them.
- Item (2), exponential tails of the subcritical cluster size, is stated
  without a citation. Kesten (1980) was not read this session (UNVERIFIED
  what it covers).
- **Direction:** soften to "are expected to persist", or cut, and keep the
  measured-threshold sentence. Drop the "exponential tails" clause unless a
  verified source is entered.

### N8 [corr]. Definition 4 defines levels by ξ, which was never measured

- `04_severity.md:29-33` defines Low, Medium and High through ξ(β) ≪ L,
  ∼ L, and so on, including "fluctuations are maximal" at Medium.
- The levels were locked by observable bands (DX-201; `04_severity.md:43-49`),
  and no artifact measures ξ.
- §4.4 then shows the burnt-fraction variance peaks near β ≈ 0.53 (DX-8),
  not at 0.49.
- **Direction:** keep Def. 4 as the motivation. State plainly that the
  operational definition is the bands. Move "fluctuations are maximal" out
  of the definition, or qualify it as the idealized-kernel expectation.
- Low priority.

### N9 [corr]. Abstract: "each stressor is a parameter of one transition kernel"

- At `paper/finale.md:13`. Coupling B parameterizes the observation kernel
  (Def. 1; the nested-model table at `03_environment.md:178-182`;
  `docs/theory_foundations.md:667`).
- The demo's §1 already says "transition or observation kernel"
  (`01_introduction.md:9`).
- **Direction:** fix in v2's abstract.

### N10 [corr]. Registered strings are paraphrased in the owner's abstract, and the completion bound is missing there

- **The inert-share string.** The registration requires the abstract-level
  summary to state that "the effect does not survive the inert-share
  correction" (`docs/decision_log.md:4989-4993`; App. D item 4).
  `paper/finale.md:13` writes "does not survive an inert-share correction
  registered before unblinding".
- **The suffix.** The T\* rule makes "— sign unstable over the final half"
  a non-optional suffix (App. D item 2). The abstract paraphrases it as
  "Neither … keeps a stable sign over the final half".
- The ABSTRACT ruling accepted these (`docs/decision_log.md:5659-5664`), so
  this is a recommendation for v2, not a defect in the record.
- **Completion:** the abstract gives the CI but never says "excludes a
  joint-training gain larger than 0.66 points" (RES-1). "Completion null is
  an exclusion with its bound" is a binding rule.
- **Direction:** carry all three verbatim in v2's abstract.

### N11 [fram]. B̂ is phrased as an established effect at abstract level

- At `paper/finale.md:13`: "raises isolated training's survival by 0.98
  points". B̂ has no registered test and no verdict (FIGURE BATCH B7;
  RES-7). It is cross-unit (HW-4).
- §1 (`01_introduction.md:37`) and §9.2 (`09_compositional_test.md:96`)
  handle it correctly ("its survival is 0.98 points above ISO's"; "no
  registered test and no verdict").
- **Direction:** at abstract level, state it as an estimate, with its
  interval or "no registered test", or drop it. Γ₄ carries the reading.

### N12 [fram]. "Saturates" is an interpretation the record does not make

- At `09_compositional_test.md:136`: "The co-occurrence slope γ_p, which
  saturates before JOINT". The source is `paper/branch_B.md:79, :207` and
  `BRIEF.md:666` (§D9 item 10).
- The SECONDARY RESULT says only "γ_p does **not** extrapolate … Reported,
  not resolved" (`docs/decision_log.md:5091-5092`).
  - The plane is fitted on p ≤ 0.5 and assumed linear.
  - Both knees are UNDERPOWERED (SEC-6).
  - JOINT differs from the sweep arms in δ.
  - No estimate shows a saturating shape.
- **Direction:** "does not extrapolate to JOINT".

### N13 [fram]. §10's opening claims every limitation was fixed before the outcome

- At `10_limitations.md:5`: "These limitations are properties of the design,
  registered or recorded before the outcome was known".
- The second list ("What the record adds", `:18-27`) includes post-unblind
  findings:
  - the Γ(t) instability and completion lean (2026-09-27);
  - the mediator's blindness, "diagnosed after the run"
    (`docs/decision_log.md:5101-5108`).
- **Direction:** scope the sentence to the first ten items.

### N14 [fram]. §11 describes an "anonymized code supplement" whose existence is undecided

- At `11_reproducibility.md:5` ("What the anonymized code supplement
  contains"). Many in-text file paths (`che/…`) also presuppose it.
- The record leaves this open:
  - "Code availability … moves to §11, with O-3 and O-4" (DESCRIPTION entry
    item 4, `docs/decision_log.md:5694-5695`).
  - The §11 open item asks also "whether a Beyond PDF submission takes a
    supplement" (`writing_session_prompt.md:220`).
  - O-3 and O-4 are OPEN (`paper/numbers_ledger.md:219-222`).
- **Direction:** an owner decision (Q4e). Until then, §11 states what exists,
  not what will be released.

### N15 [corr]. Citation support beyond what `related_work_verification.md` records

- **Theory citations verified for identity only.** `bernstein2002`,
  `kesten1980` and `grassberger1983` are VERIFIED for identity only
  (`paper/related_work_verification.md:218-269`; summary table `:33-35`).
  - No quote supports the claims they carry: NEXP-completeness; β_c = ½,
    which Kesten's title states; and the constant-infectious-period mapping.
  - Cox & Durrett (1988, p. 172) credit the epidemic-to-percolation relation
    to Mollison (1977) and Kuulasmaa (1982). Whether Grassberger (1983)
    describes the constant-period mapping is UNVERIFIED.
  - **Direction:** B2 records an abstract-level support quote for each in
    step 3 before reuse.
- **Erdem & Üre's Table 5.** Part 3 records Table 5 as "ASA-PPO ≥
  N-HYBRID-PPO in 6 of 6 cells, one tie" (`:1008-1009`). The demo
  (`02_related_work.md:31`) and the owner's §2 say "do better". Direction:
  "at least as well in all six cells (one tie)".
- **Erdem & Üre, "perturbed throughout":** see OWNER ITEM 3.

### N16 [fram]. Restatements (the main length driver)

Each result has one home; elsewhere it should be a pointer. Locations,
checked from source this session:

| result | stated at |
|---|---|
| Γ (+0.96 [0.47, 1.44]; −1.73 [−4.12, +0.66], bound 0.66) | abstract; `01:35`; Fig. 3 caption `01:28`; §9.2 table `09:80` **and** prose `09:88`; App. H `12:217, :233` |
| Γ₄ (−0.03 [−0.68, +0.63]) and B̂ (+0.98) | abstract; `01:37`; `09:82, :84` table **and** `09:92, :96` prose; Fig. 11 caption |
| the two limits of the correction | `01:37`; `09:98`; `10:20`; partly `09:136` |
| Γ(t) shape (last fifth, 70 %, t = 750) | abstract; `01:35`; `09:111`; `10:21`; App. H `12:235`; Fig. 12 caption |
| agents' influence on collapse (9×, 0.4–1.4 %, 7.4–8.3 %) | `02:21`; `03:172`; `05:28` |
| Coupling B's Medium −0.03 on a three-seed spread | `01:44`; `06:81`; `08:62`; `10:7`; `10:24` |
| 4.83-fold fuel-limited fall | abstract; `01:44`; `05:78, :80, :86`; `09:130`; `10:7` |
| the counter's scope note | `06:87`; Fig. 8 caption; `09:23`; `09:132`; `12:276`; Fig. 13 caption |
| M5.5's VOID condition (20 % against 27.2 %) | `07:58`; `08:18`; `12:91` |
| max \|Δ\| 2.44 × 10⁻⁴ (both M1 lines) | `09:134`; `11:7` |
| hardware blocks | `09:134`; `10:14`; `12:187-190` |
| Prop. 1's proof (near-identical text) | `03:32`; `12:11` |
| Thm. 1's proof | `06:63` (compact); `12:29` (full) |
| the registered reading rules, quoted | §9.1 table `09:53-57`; App. D `12:110-161` |
| bias (b) readings | `08:58`; `09:49`; App. C `12:96-98` |

### N17 [fram]. Minor wording

- **`09_compositional_test.md:136`**: "Survival moving while completion stays
  unresolved also appeared one level down, for Coupling B at High (§6)".
  - This echoes the struck "paid in agents" headline (branch_B §6, §8).
  - Keep it, if at all, as a descriptive parallel with no inference.
- **`09:136`**: "The arm that showed it cost 20 runs". Process detail; cut.
- **`09:15`**: "(§6)" should be "(§5–§6)" (see M2's cross-reference note).

### Checks that came back clean (this session)

- **Numbers.**
  - **Random sample:** 26 tags drawn with seed 20261011 from 839 section
    tags, across 00, 01, 04, 06, 08, 09, 10 and 12. Each matches its row's
    value, sign, rounding and conversion to points.
  - **Abstract:** all 17 tags match their rows.
  - **§1 and §9:** every number was compared with its tag's row for value,
    scope and conversion to points.
    - The RES, SEC and §9 DX values (DX-18 to DX-29) were also compared
      with the source reports under `che/bench/results/phase6/`:
      `unblind/report.md:9-46`, `post_gamma4_t2000.md:9-35`,
      `post_evalfloor_gamma_t_high.md:20-90` and `secondary.md:1-62`.
    - All match, including Γ, Γ₄, B̂, Γ₄′, Γ_H, Γ(t), T = 2000, the
      falsifier, and the derived "−0.37 to +0.36" survival range through
      t = 850 (DX-25).
    - DES rows were checked against the ledger, not re-opened at their
      sources.
  - Spot-checked rows against their sources: CB-5, CB-7, CB-9, CO-1/CO-2,
    CA-4, CA-6, DX-13, DX-34. All agree.
  - **No tag–row or row–source mismatch found.**
- **Double-blind.**
  - No URL, account, name, absolute path or hex hash in any section file or
    in `submission_demo.md`.
  - The 11 figure HTML files carry only the SVG namespace URI.
- **Listings:** 6 of 6 are byte-identical to the tree.
- **Registered strings:** verbatim in the demo body (§1, §9.2, §10, App. D,
  App. H). B̂ carries no verdict word in the body. Bias (b)'s sign reversal
  is stated (`08:58`, `09:49`).

## 1.3 Record items for the owner (report only; nothing edited)

1. `docs/theory_foundations.md`:
   - Cor. 1(3)–(4) (`:217-225`, [CITED] without a source);
   - the "universal" caveat (`:227-232`);
   - Prop. 3's 43/18 rate (`:309-311`, `:318`);
   - Prop. 1's "S, Ω finite" (`:151-153`);
   - Def. 1's observation line (`:62-63`);
   - Remark 1 (`:166-168`);
   - Prop. 4's "irreducible" title and slack, and the JOINT ε = 0 contrast
     (`:610`, `:623-625`; N6).
2. `severity_lock.md:22-23`: "asymptotic γ = 43/18" (as C1).
3. `CLAUDE.md:344`, `docs/decision_log.md:1194` (OWNER ITEM 5).
4. `che/bench/results/phase4/phase4_report.md:366, :394-395` (OWNER ITEM 6).
5. `HANDOFF.md:227`: the stale "theory-doc ρ amendment" item.
6. `paper/beyond_pdf/KIT_NOTES.md` §S1.5 and §S4 (N4).
7. `paper/branch_B.md:225` misquote (N4).
8. `phase6_design_v2.md:431` premise (N5; registered, never edited).

---

# Part 2. Decisions

These are builder decisions inside the owner's rulings. Each says what v2
keeps from the demonstration, what changes and what goes, with the reason.
Decisions that would change a ruling are listed separately at the end.

### Hero (`00_hero.md`)

- **Keep:**
  - the random-policy explorer directly under the abstract (OPENING AND §1
    REOPENED item 2);
  - the "illustrative · grades nothing" status;
  - the selection rule;
  - the "map is state, panels are perception" sentence.
- **Change:** trim the caption, now 147 words, and keep it under the cap.
  Make sure nothing in it competes with the disclosure footnote on page 1
  (N1).
- **Go:** nothing.

### §1 Introduction

- **Keep:**
  - the order: question; where the hazard sits; CHE; the test (Fig. 2);
    result (Fig. 3); correction; what is not claimed; contributions;
  - Figs. 2–3, because Γ is never shown without Γ₄ (FIGURE BATCH A1);
  - the corrected Prop. 1 sentence (OWNER ITEM 2);
  - the corrected fuel-limitation timing (OWNER ITEM 1).
- **Change:**
  - lead with the plain result, mirroring F2;
  - rewrite Remark 1's clause (C2);
  - restate the δ confound as a design error with the corrected timeline
    (F3);
  - turn "a rule whose argument is general" into a labelled recommendation
    with a pointer (F4);
  - cut the two-limits detail to one clause pointing to §9.2 (N16);
  - target ≤ 1,200 prose words, from 1,401.
- **Go:**
  - "The fire-only third was registered as a bias" as foresight (F3);
  - contribution 4's "rule".

### §2 Related work

- **Keep:** the paragraph set and Table 1. It is verified twice (READS
  RULING) and figure-independent. Keep the "how we searched" paragraph.
- **Change:**
  - Erdem & Üre: "an attack is computed at every step in each adversarially
    trained arm" (OWNER ITEM 3), and "at least as well … one tie" (N15);
  - the agents' influence numbers point to §5 (N16);
  - trim the Chen et al. and Gao et al. paragraphs toward 1,300 words, from
    1,717.
- **Go:** no content. These edits depart from text READS RULING called
  final; see ruling list R1.

### §3 The environment

- **Keep:**
  - Def. 1 with ρ and t;
  - Def. 2 with its formula, the hazard-blind/hazard-priced note, both tests
    and the d_p ablation with its scope;
  - Def. 3, Prop. 2 (statement), the smoke update and §3.5's instance and
    metrics;
  - Listings 1–3.
- **Change:**
  - Remark 1 (C2);
  - Prop. 1: the statement plus one sentence here, the proof only in App. A
    (N16);
  - clause (ii)'s agent-influence paragraph shrinks to a pointer to §5.1;
  - Listing 1: a shorter contiguous range or wrapped CSS (KIT_BUILD 2);
  - drop the Cor. 1 exponent note at `:28` if (3) goes (C1);
  - target ≤ 2,000 words.
- **Go:** the duplicate Prop. 1 proof.

### §4 Severity calibration

- **Keep:** Fig. 5, the measured-threshold provenance (CAL-1 with O-2's
  caveat, DX-204), the locked-levels table and the re-test (§4.4).
- **Change:**
  - Cor. 1: drop (3), and state (4) at the verified level with
    `garet2004chemical`, or drop it (C1);
  - soften the "universal" sentence and item (2) (N7);
  - say that the levels' operational definition is the bands (N8).
- **Go:** the 43/18 and 4/3 exponents.

### §5 Coupling A

- **Keep:** Def. 5 as implemented, Listing 4, Prop. 3 and its remark, the two
  handshake runs reported as two, the self-limiting finding with its m35
  replication, and the floor honesty paragraph.
- **Change:**
  - Prop. 3 loses "like |β − β_c|^{−43/18}" (C1);
  - name the grids in plain words (F5);
  - §5.1 becomes the single home of the agent-influence numbers (N16);
  - target ≤ 1,000 words.
- **Go:** repeated statements of the 4.83× figure beyond §5.3, which become
  pointers.

### §6 Coupling B

- **Keep:**
  - Def. 6 as implemented and Listing 5;
  - Thm. 1's statement and what it buys;
  - the lock story (§6.3), shortened;
  - the High effect led by 3/3 (honesty line 5);
  - the Medium −0.03 with its three-seed scope;
  - the danger-moment masking;
  - the counter with its scope note;
  - Figs. 7–8.
- **Change:**
  - Thm. 1's compact proof goes to App. A (N16);
  - §6.3 shrinks to the outcome (κ_B = 1.0 on the detection band; why the
    bands did not intersect), with details in an appendix;
  - target ≤ 1,400 words.
- **Go:** the duplicated proof.

### §7 Communication denial

- **Keep:**
  - Def. 7 and Listing 6;
  - Remark 2′ as a refinement of Pynadath & Tambe;
  - the M5.3 / M5.3b / M5.5 measurements as bars (post-hoc floor grading);
  - the demand-side argument, which has record support (`docs/decision_log.md:1077-1078`);
  - the frozen-encoder scope.
- **Change:**
  - move the toy's numeric constants (DX-15: q̃/q, the 79 % / 54 % / 7 %) to
    App. A;
  - replace milestone labels with descriptions (F5);
  - target ≤ 1,000 words.
- **Go:** nothing substantive.

### §8 Methodology

- **Keep:** each rule with its exhibit, Fig. 10, §8.6 "where this paper
  falls short" (a strength for a referee), and bias (b)'s three readings.
- **Change:** the F5 pass, which replaces "card" (10) with GPU, and M-labels
  with plain study descriptions plus App. C's key. Target ≤ 1,300 words.
- **Go:** nothing.

### §9 The pre-registered compositional test

- **Keep:**
  - the registered reading order (verdict, then correction, then Γ(t), then
    non-verdict-bearing analyses);
  - Figs. 11–13;
  - one contrast table;
  - the falsifier with its margin;
  - the High readout's registered wording;
  - mediation VOID with its diagnosis;
  - the γ_n-fits / γ_p-fails pair (FIGURE BATCH B10).
- **Change:**
  - F5 throughout: "GPU", "the same-GPU replicate", "the registered reading
    order", "the no-coupling sweep arm", "re-measured reproducibility floor";
  - Prop. 4 renamed and scoped (C3, N6);
  - F3's design-error statement replaces "Registered biases, stated before
    the result";
  - a single labelled recommendation (F4);
  - "does not extrapolate" replaces "saturates" (N12);
  - give each number once: the table **or** the prose (N16);
  - move the reading-rules table's verbatim quotes to App. D only, leaving a
    one-line summary here;
  - target ≤ 2,800 words, from 3,485.
- **Go:**
  - "A registered design caught it";
  - "The arm … cost 20 runs";
  - the second statement of every tabled number.

### §10 Limitations

- **Keep:** the ten branch-invariant items in the registered order. The
  §5 honesty lines and the Medium-siting item are required. Dropping any
  other item because the outcome makes it awkward would be outcome-dependent
  disclosure, which `writing_session_prompt.md:219` labels "a suggestion to
  raise, not a rule". Keep the "recorded deviation" item.
- **Change:**
  - scope the opening sentence to the first ten items (N13);
  - "What the record adds" becomes pointers without numbers (N16);
  - add the design-error sentence (F3) or point to §9.1;
  - the advice item becomes a pointer to the labelled recommendation (F4).
- **Go:** restated numbers.

### §11 Reproducibility

- **Keep:** "what is exact and what is not", the run cost (DX-4, DX-407) and
  "one look per stage".
- **Change:**
  - the M1 line, stated once (N16);
  - the supplement paragraph waits on the owner's code-availability decision
    (N14); until then, describe what exists, not a release.
- **Go:** "the anonymized code supplement contains", pending Q4e.

### Appendix

- **A, Proofs.** Keep. It becomes the single home of the Prop. 1 and Thm. 1
  proofs. Prop. 3's proof loses the 43/18 line, and Prop. 4 is renamed.
- **B, Locks and hyperparameters.** Keep.
- **C, Floors.** Keep, with a key for study labels.
- **D, Frozen analysis plan.** Keep the verbatim quotes, as the home for
  them. Trim to the rules the paper uses.
- **E, Branches.** Keep.
- **F, Grid provenance.** Keep, shorter; it becomes the home of the hardware
  blocks.
- **G, Throughput.** Fold into §11 or F (two sentences).
- **H, Γ(t) tables.** Keep.
- **I, Secondary design.** Keep.
- **J, Trained-policy episodes.** Keep, shown separately (FIGURE BATCH A3).

Global, all sections:

- Strip the 13 line-1 labels from the v2 sources. The disclosure footnote
  replaces them (PAPER V2 item 2; DEMONSTRATION DRAFT item 3 governed the
  demo only).
- Keep `<!-- N:ID -->` tags in the repository copy and strip them in staging
  (M4).

### Decisions that would change, or need, a ruling (for the owner)

- **R1.** §2 edits to "every arm is perturbed throughout" and "about seven
  percent".
  - READS RULING item 2 records both as "Left as written, by the owner's
    call" (`docs/decision_log.md:5760-5765`).
  - The v2 prompt says to make them accurate (`paper_v2_prompt.md:199-206`),
    but no log entry supersedes READS RULING item 2. Under the meta-rule
    (`CLAUDE.md`, "Rulings bind only once transcribed"), the change needs a
    transcribed entry.
- **R2.** v2's abstract would carry the two registered strings verbatim,
  where the ABSTRACT ruling accepted paraphrases (N10).
- **R3.** `description`.
  - DESCRIPTION ruled it final and "restates the abstract's opening".
  - PAPER V2 item 1 includes `description` in what builders draft, but item
    3 reopens only the title and abstract.
- **R4.** Naming CHE in the abstract.
  - ABSTRACT item 3 was the owner's double-blind call under REPO VISIBILITY.
  - v2 reopened the abstract. Keep, or reconsider once the repository is
    confirmed private (an unauthenticated 404 check is listed in the
    checklist).
- **R5.** Comment and `%`-line stripping at staging (WRITING ROLES, OWED,
  `docs/decision_log.md:5474-5485`): not yet ruled.
- **R6.** §2's position, after §1 or after the results (OPENING item 4: "decided at the
  final pass"). Builder default: keep after §1.

---

# Part 3. Owner questions for step 4.5

- **Q1 (M4).** Strip HTML comments and the bib's `%` lines for the
  OpenReview upload as well as for any rendered-site link?
  - Facts: the zip carrying raw `submission.md` is what OpenReview receives
    and what TMLR builds the public page from. Whether reviewers can
    download it, and whether TMLR's build minifies comments away, are both
    UNVERIFIED. The 13 line-1 labels must go in any case.
  - Reviewer's recommendation: strip for every upload, and keep the
    repository copy tagged.
- **Q2 (M3).** Two parts:
  - What `date` should be? It will show in the "cite this work" box as a
    full date in the `year` field (kit format).
  - Set `submitted_date`? Without it the page byline reads "Submitted: *Not
    submitted yet.*"
- **Q3 (F1).** The title, from P1's candidates and the four in F1 above.
- **Q4.** Ruling-level items:
  - **a.** R1: supersede READS RULING item 2 for v2? This is a
    transcription, needed before §2's two phrases change.
  - **b.** R2: the abstract carries "does not survive the inert-share
    correction" and "sign unstable over the final half" verbatim?
  - **c.** R4: keep the environment named in full in the abstract?
  - **d.** R3: may `description` change, and should it follow the new
    abstract's opening?
  - **e.** N14: how §11 describes code availability. The options are an
    anonymized supplement, none, or "on acceptance". This takes in O-3 and
    O-4, and whether a Beyond PDF submission takes a supplement.
  - **f.** N1: if a `<d-footnote>`'s text prints at the end of the page,
    does that satisfy "a footnote on the first page"? Or should v2 add a
    visible first-page disclosure line?
  - **g.** C1: drop Cor. 1(3), and state (4) with `garet2004chemical` (one
    new bib entry, verified in the C1 file) or drop it?
  - **h.** F3: approve the corrected timeline as the basis of the
    design-error wording. δ was certified inert 2026-07-30, before the design
    of 2026-08-02. The bias was found pre-grid on 2026-08-16. It was
    registered mid-grid on 2026-09-18.
  - **i.** N6/C3: keep Proposition 4 in §9.1 as a renamed upper bound, with a
    sentence that it certifies nothing at this scale, or move it to App. A?
    The vacuity argument is the reviewer's derivation and needs the owner's
    check.
  - **j.** O-1 (PBT), still OPEN in the ledger: the demo mentions no PBT
    and cites no `jaderberg2017pbt`. Keep that?
  - **k.** The theory-doc record items (§1.3 item 1): amend the theory doc,
    or let the paper depart from it with a note, as App. A already does for
    Prop. 1?
  - **l.** OWNER ITEMS 5–6 and the other record items in §1.3: who fixes
    them, and when (CLAUDE.md, the phase-4 report, HANDOFF, KIT_NOTES,
    branch_B)?
