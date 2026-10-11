# The demonstration built with the real TMLR Beyond PDF author kit (2026-10-11)

The kit's own Jekyll build was run on `submission_demo.md`, with the kit's
own merge step. Nothing from the kit entered the repository: the kit was
fetched and built in a scratch directory (`KIT_NOTES.md` §S1.8).

## What ran

- **Kit:** `tmlr-beyond-pdf-author-kit.zip`, sha256 `e531434b…bacc2d5`. This
  is the same file `KIT_NOTES.md` §S1.1 recorded on 2026-09-27.
- **Staging:** `submission_folder/` held `submission_demo.md` as
  `submission.md`, the 40-entry `submission.bib`, and the 26 assets of
  `out/files.json` (11 HTML figures, 15 PNGs, no GIFs).
- **Merge:** the kit's own `merge_files()` from `compile_submission.py`. It
  copied the files into `tmlr_do_not_modify/` and rewrote every lone `$` to
  `$$`. The kit's Docker launch was skipped, because this container has no
  Docker daemon.
- **Build:** the second route in `KIT_NOTES.md` §S1.6, local Ruby 3.3.6.
  The kit's Gemfile resolved, unlocked, to github-pages 232, jekyll 3.10.0
  and kramdown 2.4.0 (GFM input). Then `bundle exec jekyll build --future`
  ran. It needs a UTF-8 locale (`LANG=C.UTF-8`), as the kit's Dockerfile
  sets; without one, a theme stylesheet fails to compile. The build
  finished with exit 0 in about 3 s.
- **Inspection:** headless Chromium on
  `/tmlr-beyond-pdf/under_review/submission/`, then the page printed to PDF
  (the archival copy).

The gem versions float (no lockfile), so this is evidence about one build
on one day, not about the build TMLR's site runs.

## Results

| check | result |
|---|---|
| math (the kit's MathJax 3.2.0, CHTML) | 578 expressions, 0 errors; no unrendered `$` or TeX in the text |
| Liquid left in the page | 0 |
| citations | 55 `<d-cite>` tags; Distill's reference list has 38 entries |
| `toc` links | 12 of 12 resolve to a heading id |
| interactive figures | 11 of 11 iframes load and resize themselves (same-origin) |
| images | 15 of 15 load |
| print companions (`_styles`) | on screen 0 of 11 shown; in print media all 11 shown with their images, all 11 iframes hidden |
| GFM hard breaks (`<br>`), literal `**`, fences, links | 0 |
| console errors | one, from the kit's own comment widget (utteranc.es, no repository set); none from the submission |
| failed requests | 0 |
| browser-printed PDF | 40 pages (US Letter), 3.7 MB |

## Differences from this folder's preview, and what they mean

1. **The reference list shows raw LaTeX** in several entries, for example
   `C{\^o}t{\'e}`, `{\c{C}}akır`, `{VULCAN}`, `Gar\dh ar`,
   `Rockt\"{a}schel`, `$\frac{1}{2}$` and `--` page ranges. Distill's bib
   renderer resolves almost no LaTeX (`KIT_NOTES.md` §S1.5). The preview's
   reference list once hid this; it now renders references as Distill
   does. Fixing it is the owner decision already open in `HANDOFF.md`:
   Unicode in `related_work_verification.md`, then re-copy the `.bib`.
2. **Long code lines are cut at the text column on screen** and scroll
   sideways (Listing 1 in particular). In the printed PDF they show in full.
3. **The page source carries 869 HTML comments**, mostly the `<!-- N:ID -->`
   ledger tags. They do not render, but the source is public during review,
   so they must be stripped when staging for upload (the checklist's
   comment-stripping item).
4. The kit adds its own navbar and footer, and at 1280 px it shows the
   contents box as a sidebar. The preview puts that box above the text
   below 1400 px.

Not checked: the kit's web editor, the OpenReview upload, and anything on
TMLR's own site.
