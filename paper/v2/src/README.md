# `paper/v2/src/`: the Paper v2 build, the real-kit build, and their checks

Builder B2, Paper v2 phase 1, step 3 (2026-10-11). Nothing here writes paper
prose. These scripts assemble the sections that B1 and the writers own,
check them, and build them with the real TMLR Beyond PDF author kit. The
contract they implement is `paper/v2/INTERFACE.md`. What ran, and the
negative controls, are in `VALIDATION.md`.

| file | what |
|---|---|
| `build_v2.py` | assembles `front_matter.yaml` + `sections/` into the kit source `out/submission_v2.md`, the owner's preview `out/index.html`, `out/files.json`, `out/build_report.json` and `out/crossrefs.md` |
| `kit_build.sh` | the real-kit build: fetch and verify the kit, stage, merge, Jekyll, headless Chromium, grade. Writes `out/kit_checks.{json,md}`, `out/submission_v2_print.pdf`, `out/submission_folder.zip`, `out/kit_screens/` |
| `kit_stage.py`, `kit_merge.py`, `kit_checks.mjs`, `kit_report.py` | the steps `kit_build.sh` calls: staging and the browser-free checks; the kit's own `merge_files()`; the browser measurements; the grading |
| `bib_diff.py` | checks (or regenerates) `assets/bibliography/submission.bib` against the BibTeX blocks of `paper/related_work_verification.md` |
| `provenance_check.py` | compares each section's sentences with its `provenance/<section>.md` rows |
| `snapshot.sh` | snapshots of `sections/` and `provenance/`, and the lines that changed between two |
| `distill_port.py` | Python ports of the kit's Distill reference rendering, kramdown's header ids and Jekyll's `slugify` (shared) |
| `kit_styles.css` | the page CSS that `build_v2.py` puts in the YAML `_styles` field (comments stripped): print companions, listings, wide math, print overflow, and the explorer height pins |
| `kit_preview.css`, `preview_extra.css` | the preview's look (the kit's Distill CSS, carried from the demo, plus preview-only additions) |

## What you need

- **Python** with pyyaml, markdown-it-py and pygments (pinned to `uv.lock`).
  There is no project venv; this session used
  `<session scratchpad>/buildvenv/bin/python`. Every script is run with it
  below, written as `$PY`.
- For `kit_build.sh` also: `curl`, `unzip`, `zip`, `sha256sum`; Ruby 3.3 with
  Bundler; Node 22 with the global `playwright` 1.56.1 and `http-server`
  (under `/opt/node22/lib/node_modules`); Chromium at
  `$PLAYWRIGHT_BROWSERS_PATH` (never run `playwright install`); poppler's
  `pdfinfo`, `pdftotext`. Network: `tmlr-beyond-pdf.org` (the kit),
  `rubygems.org` (the gems), and the CDNs the kit's pages load (jsDelivr,
  Google Fonts, cdnjs, utteranc.es), all through `$HTTPS_PROXY`.
- No Docker. The kit's own route is Docker (`KIT_NOTES.md` §S1.6); this
  container has no daemon, so the local-Ruby route is used, as in
  `paper/demo_beyond/KIT_BUILD.md`.

## How to run

From the repository root:

```sh
$PY paper/v2/src/build_v2.py                    # draft build of paper/v2; exit 1 on a hard failure
$PY paper/v2/src/build_v2.py --final            # also fail on M1 flags, STUB-SPEC blocks, placeholders,
                                                #   unresolved cross-references and warnings
$PY paper/v2/src/build_v2.py --alt no_item4     # swap in every sections/alt/*.no_item4.md
$PY paper/v2/src/build_v2.py --alt 00_abstract.disclosure_line
$PY paper/v2/src/build_v2.py --copy-assets      # also copy the assets into out/ to open the preview from disk

PY=$PY paper/v2/src/kit_build.sh --scratch <session scratchpad>/B2     # the real-kit build of paper/v2
PY=$PY paper/v2/src/kit_build.sh --scratch <dir> --final --alt no_item4  # flags pass through to build_v2.py

$PY paper/v2/src/bib_diff.py                    # check the v2 bib (exit 1 on any difference)
$PY paper/v2/src/bib_diff.py --write            # regenerate it from related_work_verification.md, then check

$PY paper/v2/src/provenance_check.py            # all sections; or name some: 03_environment 09_compositional_test
$PY paper/v2/src/provenance_check.py --strict   # also fail on unresolvable support

paper/v2/src/snapshot.sh before_fixes           # copy sections/ and provenance/ to snapshots/before_fixes/
paper/v2/src/snapshot.sh diff before_fixes current          # changed lines since then
paper/v2/src/snapshot.sh diff before_fixes after_fixes --word
```

`--root DIR` (both builds and the provenance check) points the tools at
another folder with the same layout; the validation used scratch copies.
`kit_build.sh --bib FILE` and `build_v2.py --bib FILE` build with another
bibliography (the M2 negative control). `--styles FILE` builds with another
`_styles` CSS (layout experiments only).

**`kit_build.sh` in detail.** Each run makes `<scratch>/kit_run_<time>_<pid>/`
with a new, empty directory per download and per unzip; the gems are cached
in `<scratch>/gems`. Nothing from the kit enters the repository
(`KIT_NOTES.md` §S1.8). The steps:

1. `build_v2.py` (its failures are graded in step 8, so a failing draft still
   gets a kit build);
2. fetch `tmlr-beyond-pdf-author-kit.zip` and verify sha256
   `e531434b…bacc2d5`; **a mismatch stops the run (exit 3)**;
3. unzip twice without `__MACOSX` (the staged build and an unstripped
   control);
4. `kit_stage.py` stages `submission_folder/`: `submission.md` with every HTML
   comment removed (ledger tags, line-1 status comments, STUB-SPEC blocks,
   LISTING markers), the bib with its `%` lines removed, the assets of
   `files.json` at their kit paths. It is zipped as `out/submission_folder.zip`
   (top-level folder `submission_folder`, as the kit requires);
5. `kit_merge.py` runs the kit's own `merge_files()` under `python3 -I`, without
   the kit's Docker launch (it executes only the kit script's imports and
   function definitions). The merge rewrites every lone `$` to `$$`;
6. `bundle install`, then `LANG=C.UTF-8 bundle exec jekyll build --future`, for
   the staged build and the control. The gems float (the kit ships no
   lockfile): this session resolved github-pages 232, jekyll 3.10.0, kramdown
   2.4.0 and kramdown-parser-gfm 1.1.0;
7. both `_site` trees are served with `http-server` at the kit's base URL;
8. `kit_checks.mjs` measures the page in headless Chromium at 1280 px (and 1024
   and 390 px for overflow), prints it to PDF (US Letter, print media), then
   `kit_report.py` grades. **Exit 1 if any check fails.**

A result is evidence about one build on one day with floating gems, not
about TMLR's own build (`KIT_NOTES.md` §S1.6).

## What each check means

### `build_v2.py` (source side)

Hard failures (exit 1):

- **Status line.** Line 1 of every section file, alternates included, is
  exactly the INTERFACE status comment. `00_abstract.md` and `00_hero.md` come
  first; the rest assemble in filename order.
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
  under `paper/v2/assets/<kind>/` wins; otherwise one of the figure
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
- **Cross-references** (`out/crossrefs.md`). Every "§N", "§N.k", "Section N",
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

The preview (`out/index.html`) shows the build findings at the top, marks
each M1 line in red, shows ledger IDs and comments (STUB-SPEC blocks
included) on demand, puts each section's source beside it, and shows the
byline and "cite this work" box as the kit's layout builds them. It is not
the kit: kramdown's table and math rules are not emulated (hence the M1
marks), and its reference list is a **labelled emulation**: a Python port of
the kit's Distill code (`distill_port.py`), checked equal to the kit's own
JavaScript on all 81 entries of the old and new bibs, with a re-implemented
field parser.

### `kit_build.sh` (`out/kit_checks.md`)

Each line is PASS, FAIL or INFO, with counts.

- **Pipeline.** `build_v2.py` had no hard failure; the kit's sha256 matched;
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

1. While writing: `$PY paper/v2/src/build_v2.py` after each edit (seconds),
   and `provenance_check.py <section>` for the provenance table.
2. Before the review lanes start: `snapshot.sh <label>`. After the fixes:
   `snapshot.sh diff <label> current` gives the lines to re-check.
3. The final pass: `PY=$PY paper/v2/src/kit_build.sh --scratch <session
   scratchpad>/B2 --final` (about 4 minutes once the gems are cached; the
   growth check waits 60 s). Every
   check must PASS. `--final` also fails while a STUB-SPEC block or
   placeholder remains, so for the owner's review, before the STUB-SPEC
   blocks are removed, run it without `--final` and read the build line.
   Then publish `out/index.html` (with `out/files.json`) or the kit page as the
   private artifact, and hand over `out/submission_v2_print.pdf`,
   `out/submission_folder.zip` and `out/kit_checks.md`.
4. To compare an owner option, build with `--alt <variant>`; to compare a
   print layout, with `--styles <file>`.

## Owner questions

These come from building and checking, and add facts to the step-2 owner
questions (`paper/v2/review_of_demo.md` Part 3).

1. **Q1 (M4, N3), comments and `%` lines in the upload.** `kit_stage.py`
   always strips them in the staged folder, and therefore in the zip, which is
   what OpenReview receives. The repository copies keep them. If the owner
   wants them kept in the upload, that is a one-line change; the default
   follows the reviewer's recommendation.
2. **Q2 (M3), `date` and `submitted_date`.** Placeholder `date: 2026-10-11`,
   with `date_confirmed: false`: `build_v2.py --final` fails until the owner
   sets the date and changes it to `true` (review RM-23). The kit build shows
   `year = {October 11, 2026}` in the "cite this work" box. With
   `submitted_date` unset the byline reads "Not submitted yet."; set, it reads
   "Oct. 11, 2026" (`VALIDATION.md`).
3. **Q4f (N1), the disclosure footnote.** Measured in the kit build: the
   `<d-footnote>` marker renders on screen with a hover box, and its text is
   listed only in the footnote list at the end of the page (96 % down). In the
   printed PDF the text prints near the end (page 56–57 of 58–59). Worse, the
   abstract itself, and so the marker, printed on **page 2**: page 1 held
   only the title, byline and contents box, because Distill's print CSS forbids
   a page break inside a paragraph (`p { page-break-inside: avoid }`) and the
   abstract is one long paragraph. Measured options, not applied:
   - adding `@media print { d-article p { page-break-inside: auto; break-inside: auto; } }`
     to `kit_styles.css` moved the abstract and the marker to page 1 (contents
     box kept); the footnote text still printed at the end (page 56);
   - hiding the contents box in print alone did **not** move the abstract to
     page 1.

   So a `<d-footnote>` alone does not print as "a footnote on the first
   page". The visible first-page line (B1's
   `sections/alt/00_abstract.disclosure_line.md`) does, if the abstract reaches
   page 1. Which, and whether to apply the print rule, is the owner's choice.
   (On draft1, with a shorter abstract in several paragraphs, review RM-8 found
   the marker on page 1 and the text on page 47 of 50.)
4. **The Garet & Marchand entry differs from its record in one more place than
   the key.** Crossref returns `month=Sept`, a bare word the kit's parser
   rejects: verbatim, it emptied every citation and the reference list in a
   real kit build (`VALIDATION.md`, M2b). The entry braces it, `month={Sept}`,
   and `related_work_verification.md` Part 4 keeps the record verbatim beside
   it and says why. Alternative: drop `month` (Distill never shows it).
5. **Author names, fixed in the fix round (reviews RM-5, RM-24).** Distill
   took the last word of a "First Last" name as the surname
   ("Witt, C.S.d.", "Omari, B.A."). Both first authors are now written
   "Last, First" at the source ("de Witt, Christian Schroeder", "Al Omari,
   Bassel"), following the paper's "de Witt et al." and the JaxMARL record, and
   a real kit build renders "de Witt, C.S." and "Al Omari, B.". "Tramèr" is
   entered with its accent, as the arXiv record gives it. Each change has a
   dated note in `related_work_verification.md`. `build_v2.py` now warns on any
   cited "First … Last" name with a particle before the last word. The
   remaining owner point: the same author appears as "de Witt, C.S." and as
   "Schroeder de Witt, C." (`lu2022dpo`), because the two records split his
   name differently.
6. **The current submission's bib.** `paper/beyond_pdf/assets/bibliography/submission.bib`
   is untouched, so it is no longer a verbatim copy of
   `related_work_verification.md`. It should be re-copied (from the v2 bib)
   when the owner approves.
7. **Wide display math, tables and listings.** On screen a display wider than
   its column scrolls inside itself. In print (reviews RM-1 to RM-3, RM-25),
   tables, displays and listings now take the page column (594 px, against
   472 px for text), tables print at 10 px with wrapping cells, and listings at
   9 px. On draft1 this CSS alone removed all 7 print cuts and all 46 wrapped
   listing lines. A display wider than 594 px would still be cut, and the
   print-overflow check would fail on it.
8. **Iframe heights.** The three episode explorers resized their own frames
   without bound (review RM-4). `kit_styles.css` pins them with `!important`,
   per Distill grid width: 700 px from 1180 px, 764 px for 1000–1179, 1248 px
   for 768–999, and 1360 px below 768 (the explorers' measured
   `body.scrollHeight` plus 23–26 px). Their `height` attributes should equal
   the 1280 px value, 700. The other eight frames size themselves stably; set
   each attribute to its height at 60 s from `out/kit_checks.md`. The pins work
   only while the explorer files are unchanged: a rebuilt explorer needs its
   heights re-measured.
