# `paper/v3/src/`: the Paper v3 build, the real-kit build, and their checks

Builder B2, Paper v3 phase 1, step 3 (2026-10-14). Copied from `paper/v2/src/`
(Paper v2's B2 and orchestrator tools) and adapted; **every v2 check and every
kit and artifact fix is kept unchanged**. Nothing here writes paper prose.
What changed from v2, and the new checks, are below; what ran and every
negative control are in `VALIDATION.md` (v2's record, then a v3 section).

| file | what |
|---|---|
| `build_v3.py` | assembles `front_matter.yaml` + `sections/` into the kit source `<out>/submission_v3.md`, the owner's preview `<out>/index.html`, `<out>/files.json`, `<out>/build_report.json` and `<out>/crossrefs.md`; runs the v3 source-side checks |
| `v3_checks.py` | **new**: the v3 main-text checks (pages, terms, dates, caveats, legibility), each runnable on its own (`v3_checks.py <check> --help`) |
| `kit_build.sh` | the real-kit build: fetch and verify the kit, stage, merge, Jekyll, headless Chromium, grade. Writes `<out>/kit_checks.{json,md}`, `<out>/submission_v3_print.pdf`, `<out>/submission_folder.zip`, `<out>/kit_screens/` |
| `kit_stage.py`, `kit_merge.py`, `kit_checks.mjs`, `kit_report.py` | the steps `kit_build.sh` calls; `kit_report.py` now also grades the v3 group |
| `bib_diff.py` | checks (or regenerates) `paper/v3/assets/bibliography/submission.bib` against the BibTeX blocks of `paper/related_work_verification.md` |
| `provenance_check.py` | compares each section's sentences with its `provenance/<section>.md` rows (`--strict`, `--out`) |
| `make_review.py` | compiles `paper/v3/REVIEW.md` from `paper/v3/review/` (orchestrator tool from v2) |
| `artifact_bundle.py` | packages a kit run as the private Artifact (orchestrator tool from v2) |
| `wordcount.py` | **new**: planner P3's word counter (v2 P3 §5's method), copied with its counting function unchanged, so that every writer counts words one way |
| `snapshot.sh` | snapshots of `sections/` and `provenance/`, and the lines that changed between two |
| `distill_port.py` | Python ports of the kit's Distill reference rendering, kramdown's header ids and Jekyll's `slugify` |
| `kit_styles.css`, `kit_preview.css`, `preview_extra.css` | unchanged from v2 (print companions, listings, wide math, print overflow, the explorer height pins; the preview's look) |
| `checks_seed/` | seed lists used only if B1's `paper/v3/checks/` files are absent (`terms.seed.txt` from P3 §5.2; `dates_allow.seed.txt`); `registered.seed.txt` is used until a `paper/v3/checks/registered.txt` exists |
| `fixtures/`, `tests/` | the positive fixture and the v2 negative-control caveat map; `tests/test_v3_checks.py` runs every negative and positive control |

## What changed from v2

- **Paths.** Default root `paper/v3`; bib `paper/v3/assets/bibliography/submission.bib`
  (a verbatim copy of v2's; `bib_diff.py` PASS, 41 of 41). Kit source
  `submission_v3.md`, PDF `submission_v3_print.pdf`.
- **Configurable output directory** (v2 lesson: concurrent builds overwrite
  `out/`). `build_v3.py --out DIR`, `kit_build.sh --out DIR`,
  `kit_stage.py --out DIR`, `provenance_check.py --out DIR`. Default
  `<root>/out`. Every build prints a console summary ending in
  `build OK|FAIL (… failures, … warnings, … final-only) -> <out>/`; read it
  rather than the files when several builds run.
- **Status line.** v3's line 1 (above). `--status-line TEXT` builds another
  folder's sections (the validation built v2's sections with v2's line; the
  kit source came out byte-identical to v2's committed `submission_v2.md`).
  If the v3 contract fixes a different line, change `STATUS_LINE` in
  `build_v3.py` (one constant).
- **Section order.** `00_abstract.md` first; `00_hero.md` optional. Files that
  open with an H3 (B1's `07_`–`09_`, continuing §6, and `14_`–`21_`,
  continuing `## Appendices`; STRUCTURE.md §12 item 2) add nothing to the
  `toc` (H2s only) and resolve as cross-reference targets ("§6.3",
  "Appendix D"), because the appendix state carries across files; the stub
  build resolved "Appendix D" to `16_appendix_timeline.md:3`.
- **Ledger sources** (STRUCTURE.md §12 item 3): the canonical ledger,
  `paper/v2/ledger_supplement.md`, `paper/v2/ledger_proposals/*.md`, then
  `<root>/ledger_supplement.md` (if any) and `<root>/ledger_proposals/*.md`
  (writers' `X<n>-<k>`, the interaction check's `IC-<k>`). A row whose line
  says **PENDING** resolves, but every tag on it is listed ("PENDING ledger
  rows cited", `build_report.json` `pending_ledger_tags`) and fails
  `--final`; `provenance_check.py` reports a PENDING row in a support cell as
  a support problem.
- **Markers** (STRUCTURE.md §12 item 4): `<!-- HOLE:INTERACTION -->` and
  `<!-- OWNER-PENDING:V3Qn -->` are counted and listed with file:line (console
  `INFO markers`, `build_report.json` `markers`, and an INFO line of
  `kit_checks.md`). They are not failures.
- **The v3 checks** below, in `build_report.json` (`v3_checks`), in the build's
  console summary, and as the "v3 main text" group of `kit_checks.md`.

## What you need

- **Python** with pyyaml, markdown-it-py, pygments and Pillow. In this
  session the project venv `.venv/bin/python` has all four (and matplotlib and
  pytest for `tests/`); it is written `$PY` below.
- For `kit_build.sh` also: `curl`, `unzip`, `zip`, `sha256sum`; Ruby 3.3 with
  Bundler; Node 22 with the global `playwright` and `http-server` (under
  `/opt/node22/lib/node_modules`); Chromium at `$PLAYWRIGHT_BROWSERS_PATH`
  (`/opt/pw-browsers`; never run `playwright install`); poppler's `pdfinfo`,
  `pdftotext`, `pdfimages`. Network: `tmlr-beyond-pdf.org` (the kit),
  `rubygems.org` (the gems), and the CDNs the kit's pages load, all through
  `$HTTPS_PROXY`.
- No Docker (`KIT_NOTES.md` §S1.6): the local-Ruby route, as in v2.

## How to run

From the repository root:

```sh
$PY paper/v3/src/build_v3.py                         # draft build of paper/v3 into paper/v3/out
$PY paper/v3/src/build_v3.py --out <scratch>/b1      # the same, into its own directory
$PY paper/v3/src/build_v3.py --final                 # also fail on M1, STUB-SPEC, placeholders,
                                                     #   unresolved cross-references, warnings,
                                                     #   and any v3 terms/dates/caveats FAIL
$PY paper/v3/src/build_v3.py --alt <variant>         # swap in sections/alt/ variants (as in v2)

PY=$PY paper/v3/src/kit_build.sh --scratch <scratch>/kit [--out <dir>] [--final]
PY=$PY paper/v3/src/kit_build.sh --scratch <dir> --grade section1 --max-pages 15   # owner's start point

# the v3 checks on their own (each exits 1 on FAIL)
$PY paper/v3/src/v3_checks.py terms                  # paper/v3; --root DIR for another folder
$PY paper/v3/src/v3_checks.py dates
$PY paper/v3/src/v3_checks.py caveats
$PY paper/v3/src/v3_checks.py pages --pdf paper/v3/out/submission_v3_print.pdf [--grade section1]
$PY paper/v3/src/v3_checks.py legibility --pdf paper/v3/out/submission_v3_print.pdf \
    --kit-source paper/v3/out/submission_v3.md --files paper/v3/out/files.json

PYTHONDONTWRITEBYTECODE=1 $PY -m pytest -p no:cacheprovider paper/v3/src/tests -q   # the controls

$PY paper/v3/src/bib_diff.py                         # the v3 bib against related_work_verification.md
$PY paper/v3/src/provenance_check.py --strict        # all sections; or name some
paper/v3/src/snapshot.sh <label>; paper/v3/src/snapshot.sh diff <label> current
$PY paper/v3/src/make_review.py
$PY paper/v3/src/artifact_bundle.py <kit_run_dir> <out_dir>
```

`kit_build.sh` passes `--status-line`, `--terms`, `--registered`,
`--dates-allow`, `--caveats`, `--alt`, `--final` and `--styles` to
`build_v3.py`, and `--max-pages`, `--grade`, `--label-pt`, `--min-pt` to
`kit_report.py`. Its steps are v2's (the kit is fetched fresh into a new,
empty directory per run and **its sha256 `e531434b…bacc2d5` is verified; a
mismatch stops the run, exit 3**; nothing from the kit enters the repository).

## The v3 checks (`v3_checks.py`)

**Main text** is what lies before the appendix. A section file is appendix if
the one-home map lists it under `appendix_files` (B1's
`paper/v3/checks/caveats.yaml` lists `main_text_files` 00–12 and
`appendix_files` 13–21), or if it holds or follows an H2 matching
`^Appendi` (in the file that holds it, main text ends at that heading). The
front matter's `title` and `description` count as main text for terms and
dates. What a reader sees is scanned: HTML comments (ledger tags, STUB-SPEC
blocks, LISTING lines), tag markup, link targets, Liquid paths and
`<d-cite>` keys are masked; captions, `alt` and `title` text, table cells,
inline code and math are kept. Fenced code bodies (listings, which must stay
byte-identical to their files) are **listed, not graded**, as B1's lists
specify.

1. **`pages`: main-text printed pages ≤ 15** (V3-S1), measured on the kit's
   printed PDF. `pdftotext -bbox-layout` gives each line's page and y; a
   heading's position is `(page − 1) + y / page height`; a heading that
   occurs twice (its table-of-contents entry and itself) is taken where its
   line is tallest, the later on a tie. **Two readings are always
   reported:** from the top of page 1 to the first appendix H2, and from the
   first numbered H2 ("1 …") to it. `--grade page1` (default, P1's
   conservative reading) or `--grade section1` (if the owner rules that main
   text starts at §1) picks the graded one; `--max-pages` sets the ceiling.
   The headings are read from the source; `--end-heading`/`--start-heading`
   override. If the appendix heading is not in the PDF, the main text runs to
   the kit's Footnotes/References and the report says so.
2. **`terms`: no internal code or private vocabulary** (V3-S3), from B1's
   `paper/v3/checks/terms.txt` (B1's format: one Python regex per line, an
   optional TAB note, case-sensitive unless it starts `(?i)`). Exempt:
   (a) a match inside a **registered string** that must stay verbatim
   (`paper/v3/checks/registered.txt` if it exists, else
   `checks_seed/registered.seed.txt`: "does not survive the inert-share
   correction", "sign unstable over the final half", "B̂ gets no verdict",
   "non-verdict-bearing"); (b) a match inside a **figure-label gloss** of
   the exact form `labelled “TERM” on the figure` inside a figure caption
   (`<figcaption>`, `<p class="caption">`, an include's `caption`, or a
   `**Figure N.**` paragraph), **the first gloss of each term only** (B1's
   rule; the count per term is reported).
3. **`dates`: no date outside the allow-list** (V3-S2), from B1's
   `paper/v3/checks/dates_allow.txt`. Detected: ISO dates (and an ISO range's
   `→ MM-DD` end), `Month D, YYYY`, `D Month YYYY`, `Month YYYY`,
   `YYYY-MM`, `Month D` and `D Month` without a year, abbreviated months, and
   a bare **project year** (`--context-years`, default 2025 and 2026) after a
   date word ("in 2026", "by early 2026"). Every other bare year (citation
   years such as "Gao et al. (2024)") is listed, not graded, as B1's list
   requires. Each match is normalized (`YYYY-MM-DD`, `YYYY-MM`, `YYYY`, or
   `--MM-DD`) and compared with the allow-list lines, read the same way (a
   line may also be `re:<regex>` on the matched text); a month and day
   without a year is allowed if an allowed date has them.
4. **`caveats`: each caveat in its one home** (V3-S5), from B1's
   `paper/v3/checks/caveats.yaml`, with B1's semantics. An **occurrence** is
   one unit that matches any of an entry's patterns: a sentence (the
   boundaries `provenance_check.py` draws: abbreviations, initials and math
   are not ends), a table cell, or a whole caption. Patterns are tried on the
   reader-visible text and on the comment-free source of the unit (so a
   pattern written for TeX or for `<sub>` markup can match). Each `home` file
   must hold 1 to `max_home` (default 1) occurrences (an appendix home is
   scanned for that entry only); each `also` file at most `max_also`
   (default 1); every other main-text file 0. **Pointer syntax:** a pointer
   names or links to the home ("see §6.3", `[the design](#6-…)`) without
   restating the caveat, so the patterns do not match it; a match in a
   sentence that links to the home is still counted, and marked
   `links_to_home`. `kind: label_required` entries: every main-text unit that
   matches a `trigger` has a `label` match in the same unit or paragraph (the
   post hoc label of the interaction check).
5. **`legibility`: figure images legible in print** (planner P2 §1.3, §7.2).
   For every image in the printed PDF (`pdfimages -list`: pixel width and
   placed ppi, so printed width = pixels / ppi), matched in document order and
   by aspect ratio to the source image the kit source includes (whose drawn
   width = pixels / its PNG dpi): printed label size = nominal label size ×
   printed width / drawn width. FAIL below `--min-pt` (default 7 pt, P2
   §7.2's print specification) for a `--label-pt` label (default 8 pt, P2
   §1.3's basis). An image with no dpi, or with no matching source, fails as
   UNKNOWN or UNMATCHED.

**What the v3 checks are blind to** (CLAUDE.md, "Instruments state what they
are blind to"):

- `pages` counts space, not words: whitespace, figures and captions count
  with the section they sit in, and page margins are not removed (a full page
  is 1.00). It is a measurement on one build of the kit with floating gems.
- `terms` and `dates` see only what their lists and patterns name: a private
  word not on B1's list, or a date written another way ("the twenty-sixth"),
  passes. Text inside figure images and inside the interactive HTML figures
  is **not** scanned (P2 §7.1's relabelling is the remedy; the gloss rule
  covers labels that cannot be rebuilt). Listings are listed, not graded.
- `caveats` sees a caveat only through its patterns: a paraphrase that the
  patterns miss passes, and a pattern that is too broad flags a correct
  sentence. Both are B1's to tune; B2 reports, never loosens.
- `legibility` is an **estimate**: it assumes one nominal label size per
  image, while real labels vary (6.5–9 pt in v2, P2 §1.3). It grades raster
  images only, not text drawn by the browser.

## What each check means

### `build_v3.py` (source side; every v2 check, unchanged)

Hard failures (exit 1):

- **Status line.** Line 1 of every section file, alternates included, is
  exactly the status comment (v3: `<!-- PAPER V3 DRAFT (PAPER V3 ruling,
  2026-10-12): builder-drafted, not owner-approved -->`, or `--status-line`).
  `00_abstract.md` comes first and `00_hero.md`, if present, second (v2 required
  both); the rest assemble in filename order.
- **Ledger IDs.** Every `<!-- N:ID -->` (or `N:ID1, ID2`) resolves against
  `paper/numbers_ledger.md`, `<root>/ledger_supplement.md` and
  `<root>/ledger_proposals/*.md`. An ID defined twice with different values is
  a warning. The check proves an ID exists, not that its value matches the
  sentence (that is the numbers review).
- **Citations.** Every key of every `<d-cite key="…"></d-cite>` is in the v2
  bib. A malformed tag fails. A bib the kit's parser would reject (a bare
  BibTeX value that is not a number or `jan`…`dec`) fails, because in the
  browser it empties every citation.
- **Listings.** Every fenced code block has a `<!-- LISTING: path:start-end -->`
  line before it (blank lines allowed between), and its body equals those
  lines of the file **as committed at HEAD** (`git show`, read-only). An
  optional first line `# path:start-end (verbatim)` is allowed and must
  agree with the marker (an extension of INTERFACE, used by the demo and
  B1's stubs). A listing holding `$`, `{{` or `{%` fails, because the kit's
  merge or Liquid would change it.
- **Liquid.** Only `{% include figure.html … %}` and `{{ '…' | relative_url }}`,
  anywhere, comments and code included (Liquid runs over the whole file).
  Include attributes must parse; an attribute `figure.html` does not read is
  a warning.
- **Assets.** Every referenced asset resolves to exactly one file (a file
  under `<root>/assets/<kind>/` wins; otherwise one of the figure
  directories).
- **Front matter.** `layout: distill`; `title` and `description` one line,
  with no `"` and no `\` (both sit in JavaScript strings and JSON in
  `distill.html`); authors all Anonymous with no `url`; `bibliography:
  submission.bib`; no `openreview_id`, `toc` or `_styles` (the build makes
  the last two); `date` and `submitted_date` are YAML dates. The generated
  header must round-trip through a YAML parser.
- **toc.** The `toc` is the H2s. Each name's Jekyll slug must equal the id
  kramdown gives the heading (otherwise the contents link breaks); no `"`,
  `$`, backtick, `*` or `\` in an H2; a dot or parenthesis after the number is
  a warning (INTERFACE).
- **Comments.** A comment containing `<!--`, or an unmatched `<!--` or `-->`,
  fails: comments do not nest, so the rest would show on the page.
- **Alternates that a file swap cannot build.** `--alt 00_hero.ladder` (and
  `--alt ladder`) fails with a message: that file is a caption draft for hero
  option B, which also needs §1's ladder block moved to the hero slot, the
  explorer moved to the head of §3 and Figures 1 and 3 swapped throughout
  (review RM-6). Every other alternate swaps its whole file.
- **`date_confirmed`** in `front_matter.yaml`, if present, must be `true` or
  `false`.

Reported (fail only with `--final`):

- **M1 source scan.** Every line that is not fenced code, not a Markdown
  table row and not inside a block-level HTML element, and that carries an
  unescaped `|` outside a code span, **math included** (kramdown checks for
  tables before math; one pipe is enough, `paper/v2/review_of_demo.md` M1).
  Each flag is labelled `prose`, `inline-math` or `display-math`. Table rows
  whose cell count differs from their header's are flagged too (a pipe inside
  a cell). Write `$\lvert x \rvert$`, `\mid`, or words.
- **The date gate** (review RM-23): `--final` fails until `front_matter.yaml`
  has `date_confirmed: true`, which the owner sets once the date is decided.
  The field never reaches the kit source.
- **STUB-SPEC count**, **placeholders** in `front_matter.yaml`,
  **unresolved cross-references**, and every **warning** (for example `$`
  inside raw HTML, which the kit would turn into display math there; a lone
  inline-math paragraph, which becomes display math after `$`→`$$`; `--`
  inside a comment; an HTML comment inside inline code, which staging would
  strip from the shown code; `<br>` in prose; and the **M2 source lint**, which lists
  every cited entry whose Distill rendering would show raw TeX or drop an
  accent, and every cited author written "First … Last" with a particle such
  as "de" or "Al" before the last word, which Distill would split wrongly).
  The sentence splitter of `provenance_check.py` treats "p.", "pp." and "No."
  as abbreviations only before a number, so "a step." ends a sentence.
- **Cross-references** (`<out>/crossrefs.md`). Every "§N", "§N.k", "Section N",
  "Figure N", "Table N", "Listing N", "Appendix X", "Definition N",
  "Proposition N", "Theorem N", "Corollary N" and "Remark N" in the prose,
  with the heading or caption it resolves to. Definitions are found as
  `**Figure N.**`, `<strong>Figure N.</strong>` or `caption="Figure N. …"`,
  and headings as `## N …`, `### N.k …` and appendix `### X …`. A label after
  "their" or a possessive ("their Table 5", "Chen et al.'s Theorem 4") is a
  cited work's numbering and is listed as `external`, unchecked. A list after
  the first label stays in its kind: "(Figure 2, §1)" is Figure 2 and §1, and
  a section list needs "§" after a comma ("§9.2, 4.83-fold" is §9.2 only). The list
  shows *where* each reference points; whether that is the *right* target is
  the mechanics review's call.

The preview (`<out>/index.html`) shows the build findings at the top, marks
each M1 line in red, shows ledger IDs and comments (STUB-SPEC blocks
included) on demand, puts each section's source beside it, and shows the
byline and "cite this work" box as the kit's layout builds them. It is not
the kit: kramdown's table and math rules are not emulated (hence the M1
marks), and its reference list is a **labelled emulation**: a Python port of
the kit's Distill code (`distill_port.py`), checked equal to the kit's own
JavaScript on all 81 entries of the old and new bibs, with a re-implemented
field parser.

### `kit_build.sh` (`<out>/kit_checks.md`; every v2 check, unchanged)

Each line is PASS, FAIL or INFO, with counts.

- **Pipeline.** `build_v3.py` had no hard failure; the kit's sha256 matched;
  `merge_files()` and both Jekyll builds exited 0.
- **Math and Liquid.** 0 MathJax errors (`mjx-merror`, and an undefined macro,
  which MathJax shows as red literal text); no `$`, `\word`,
  `\(`, `\[`, `^{` or `_{` left in the article's text outside rendered math
  and code; 0 `{{` or `{%` left in the page. INFO: math expressions in the
  source against `mjx-container`s rendered.
- **Tables (M1).** The number of `<table>` elements in the article equals the
  source's (Markdown tables plus raw HTML tables). A one-row table made by a
  prose pipe shows up here as an excess.
- **References (M2).** In Distill's reference list: no `\`, `{`, `}`, `$` or
  `--`; every entry's rendered title and authors equal the bib's fields read
  as Unicode (`tex_to_unicode`), which catches an accent that Distill drops
  in silence ("Scharli" for Schärli); every `<d-cite>` shows a number and
  every one of its keys has a bib entry (an empty "[]" fails, and so does a key
  Distill numbers but lists as "?"); one reference per cited key; every hover
  card is non-empty, shows no raw TeX or "?", and has the right title and
  authors; and, if the bib would not parse, a FAIL saying so.
- **Citation box (M3).** The kit's "cite this work" BibTeX has a 4-digit year.
  The kit writes the whole date there (`year = {October 11, 2026}`).
- **Byline.** INFO: what Distill prints under "Submitted" ("Not submitted
  yet." while `submitted_date` is unset). PASS: the rendered title and
  description equal the front matter (a broken JS string would not).
- **Links and frames.** Every `toc` link and every in-page `#` link resolves to
  an element id. Every iframe loads (HTTP 200, same-origin) after it is
  scrolled into view (they are lazy). Every image loads. Then, in a fresh page
  at each of 1280, 1024 and 390 px (run in parallel, about 60 s):
  - **heights stable:** each iframe's height 5 s and 60 s after load are equal.
    This catches a figure that keeps resizing its own frame (review RM-4);
  - **no clipping:** at 60 s each frame is at least as tall as its document's
    `body.scrollHeight`;
  - **attributes:** each `height` attribute is within 5 % of the frame's
    height at 60 s at 1280 px (`plans/P2.md` §7.2: a low attribute shifts the
    page as frames load, and is all a cross-origin viewer would get).
- **Print.** Print companions hidden on screen; shown in print media with
  their images; iframes hidden in print; `.interact` notes hidden in print,
  if the text uses them. **Nothing is cut in print** (reviews RM-1 to RM-3):
  at the US Letter width (816 px) in print media, no table, MathJax container
  or `pre` may be wider than its box or than the article, and the article may
  not overflow. Paper cannot scroll, so anything wider is lost from the
  archival PDF. The details also count listing lines that wrap in print, in
  print media and in the printed PDF's text (reported, not graded; review
  RM-25).
- **Requests.** 0 failed requests (network errors or HTTP ≥ 400) over the whole
  inspection. A request aborted while the page re-lays out and then loaded is
  not counted (it happens to the lazy iframes in some runs). INFO: console and
  page errors (the kit's own comment widget always throws `Invalid repo: ""`).
- **Listings and overflow.** The text of every code block in the built page
  equals its committed file lines byte for byte (after the kit's `$`
  rewrite, Liquid, rouge and Prism). At 1024 and 1280 px no listing is
  cut or scrolls; at every width the page itself has no horizontal
  overflow (at 390 px listings may scroll inside their block). INFO: display
  math wider than its column, and whether it scrolls or is cut off.
- **Footnote (N1).** INFO: where each `<d-footnote>` marker sits on screen and
  where its text is listed; in the printed PDF, the page of the marker's
  sentence and of the footnote text; what printed page 1 holds; and the page
  on which the abstract starts.
- **YAML.** The staged front matter parses; `title` and `description` are
  one line with no `"`, `\` or `</script`; toc names have no `"`; Anonymous
  authors; no `openreview_id`.
- **Leaks and print.**
  - 0 `<!--` in the staged `submission.md` (M4) and 0 `%` lines in the staged
    bib (N3);
  - the stripped build renders the same article text, tables, math and
    listings as the unstripped control, so stripping removed only comments;
  - a double-blind scan of the staged folder: URLs other than a cited work's
    (`url`/`doi` of a bib entry) or a W3C namespace; identity strings taken at
    run time from this repository (every commit author's name, name words and
    e-mail from `git log`, git config, the remote's owner and repository names,
    the directory name) plus any in `KIT_IDENTITY_EXTRA` (comma-separated, for
    example an institution); absolute paths; hex strings of 7 or more characters
    (and whether one resolves to an object in this repository); text chunks in
    PNG and GIF files. Tool identities (Claude, Anthropic) are not tokens,
    because the disclosure footnote names the tool. No identity string is
    written to any file: reports say "identity token #n", and long hashes are
    shortened;
  - the printed PDF exists, is US Letter, and its text holds no identity
    string or absolute path;
  - the zip exists with `submission_folder/` as its only top-level entry.

**What these checks are blind to** (CLAUDE.md, "Instruments state what they
are blind to"):

- the tables check counts tables; it cannot tell an intended table from
  an accidental one if both counts move together;
- the reference check compares against the bib, so a wrong but well-formed
  entry passes;
- the cross-reference list shows the target, not whether it is the right
  one;
- the ledger check proves an ID exists, not that the number beside it equals
  the row;
- the double-blind scan knows only the identity strings git provides and
  the patterns above; a name typed into a sentence is the reviewers' to
  find;
- the build runs Jekyll locally with floating gems, not TMLR's build. It does
  not cover the kit's web editor or OpenReview.


## How step 4 runs the build

1. While writing: `$PY paper/v3/src/build_v3.py --out <own dir>` after each
   edit (seconds), and `provenance_check.py <section>`.
2. Before the review lanes: `snapshot.sh <label>`; after the fixes,
   `snapshot.sh diff <label> current`.
3. The final pass: `PY=$PY paper/v3/src/kit_build.sh --scratch <scratch>
   --final` (several minutes; the growth check waits 60 s). Every check must
   PASS, the v3 group included. For the owner's review before the STUB-SPEC
   blocks are removed, run without `--final` and read the build line.
4. Package the artifact with `artifact_bundle.py`; hand over
   `<out>/submission_v3_print.pdf`, `<out>/submission_folder.zip` and
   `<out>/kit_checks.md`.

## Owner questions carried from v2 (`paper/v2/src/README.md`)

v2's eight build-side owner questions (Q1 comment stripping, Q2 dates and
`date_confirmed`, Q4f the footnote's print placement, the Garet & Marchand
month, author-name forms, the old submission bib, wide displays in print, and
the explorer height pins) are recorded in `paper/v2/src/README.md`, "Owner
questions", and still apply to the v3 build unchanged. Two v3 additions:

1. **Which main-text reading binds** (V3-S1): from page 1 (P1's proposal, the
   default) or from §1. Both are measured every run; `--grade` switches.
2. **The figure-label gloss exemption** is B1's rule, implemented as written;
   if the owner accepts P2's label-only rebuilds, the gloss count should fall
   to 0.
