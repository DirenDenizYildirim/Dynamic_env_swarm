# TMLR Beyond PDF author kit: builder's notes

Written 2026-09-27 in a Claude Code web session, following
`beyond_pdf_scaffold_prompt.md` (milestones S0–S5). **This file is
builder tooling. It never goes into the upload.** The upload is
`submission.md` + `assets/` only (§S1.8).

---

## S0: environment check (2026-09-27)

| check | result |
|---|---|
| `docker` client | present: Docker 29.3.1, buildx, compose |
| Docker daemon | **not running**: no `/var/run/docker.sock`. `dockerd` is installed, but this session's permission classifier **refused** starting it ("Containment Escape"). Not worked around. |
| kit source | reachable: `https://tmlr-beyond-pdf.org/assets/tmlr-beyond-pdf-author-kit.zip`, HTTP 200, `server: GitHub.com` (GitHub Pages) |
| hosts the kit's Docker build needs, probed from the host with `curl -I` | Docker Hub registry 401 (reachable, auth challenge), `deb.debian.org` 200, `rubygems.org` 200, `pypi.org` 200 |

The network policy did not deny any host the build needs. **The blocker is
the Docker daemon**, not the network. The kit's build also needs two hosts
beyond GitHub, PyPI and Docker Hub: the Debian apt mirrors and rubygems.org
(§S1.6). The session brief makes that a stop-and-ask, so it is an open
question for the owner, not a thing this session decides.

---

## S1: the kit, read in full (2026-09-27)

Every file was read before anything entered the tree: the README, the
compile script, the Dockerfile, Gemfile, `docker_run.sh`, `_config.yml`,
every `_includes/`, `_layouts/`, `_plugins/`, `_sass/` and `assets/css|js`
file, and the example `submission_folder/`. The two minified Distill bundles
(`template.v2.js`, 298 KB; `transforms.v2.js`, 529 KB) and their source maps
were read for licence headers, every URL literal, and the code paths that
load URLs, parse BibTeX and render citations. They were not read line by
line.

### S1.1 Source and version

- **URL:** `https://tmlr-beyond-pdf.org/assets/tmlr-beyond-pdf-author-kit.zip`,
  linked from `https://tmlr-beyond-pdf.org/submission-instructions`.
  Served by GitHub Pages. Headers on 2026-09-27: `last-modified: Fri, 28 Aug
  2026 14:42:21 GMT`, `etag: "6a919e4d-3035c7"`.
- **Identity:** 3,159,495 bytes,
  sha256 `e531434b698e04dc9e07e4100c8eb21f3a5a9caca873c102b589af4e9bacc2d5`.
- **No version, tag or commit** is stated anywhere in the kit. The newest
  member timestamp in the zip is 2026-07-08. Identify the kit by the sha256
  above; the file at that URL can change without notice.
- The kit's own README points to `…/submission-process`, which returned
  **HTTP 404** on 2026-09-27. The live instructions are at
  `…/submission-instructions`.
- Fetched into a scratch directory outside the repository and never copied
  into it (§S1.8).

### S1.2 Licence

- **The kit states no licence.** It ships no LICENSE file, and no file in
  it names one for the kit as a whole.
- The vendored Distill bundles carry "Copyright 2018 The Distill Template
  Authors, Licensed under the Apache License, Version 2.0" headers, plus
  bundled third-party notices (MIT, SIL Open Font License).
- `_config.yml` credits Jekyll and the al-folio theme, and the Dockerfile
  carries a `MAINTAINER` label from that theme. The kit does not include
  al-folio's licence text.
- **Consequence:** no kit file enters our tree (§S1.8), so our tree
  redistributes nothing whose terms are unstated. If a kit file ever has to
  be committed, that is an owner question first.

### S1.3 File layout

54 files once the zip's `__MACOSX/` metadata and `.DS_Store` files are
dropped (5.3 MB unpacked).

```
tmlr-beyond-pdf-author-kit/
  README.md                   # 4 steps: Docker, compile, zip, OpenReview + browser PDF
  compile_submission.py       # merge submission_folder/ into the site, then serve (S1.6)
  submission_folder/          # THE AUTHOR'S FOLDER — the only thing uploaded
    submission.md             # example article (YAML header + Markdown/Liquid/HTML)
    assets/
      bibliography/submission.bib    # 2 example entries
      gif/submission/Frog.gif        # example GIF, 2.3 MB
      html/submission/graph.html     # example interactive figure (loads d3 from d3js.org)
      html/submission/tangent.html   # example interactive figure (self-contained canvas)
      img/submission/TMLR_Static_Image.jpg
  tmlr_do_not_modify/         # the Jekyll site; "do not modify, do not rename"
    Dockerfile, Gemfile, bin/docker_run.sh, _config.yml, index.md
    _includes/  figure.html, head.html, header.html, footer.html,
                metadata.html, pagination.html,
                scripts/{bootstrap,jquery,masonry,mathjax,misc}.html
    _layouts/   distill.html (the one submissions use), default, page,
                post, about, bib, archive-{category,tag,year}, none
    _plugins/   hideCustomBibtex.rb
    _sass/      _base, _distill, _layout, _themes, _variables
    _under_review/            # empty; compile copies submission.md here
    assets/css/{main.scss,main.css}, assets/img/{favicons},
    assets/js/{common,masonry,theme,zoom}.js,
    assets/js/distillpub/{template.v2.js, transforms.v2.js, *.map, overrides.js}
```

### S1.4 `submission.md` YAML header

From the kit's example and the instructions page:

| field | rule | how the layout uses it |
|---|---|---|
| `layout: distill` | required | selects `_layouts/distill.html` |
| `title` | required | `<h1>` in `<d-title>`; Distill front-matter JSON; **a JS string literal** in the layout's inline script |
| `description` | instructions: "[Your abstract]"; kit example: one sentence | subtitle `<p>` under the title; `<meta name="description">`; front-matter JSON; **a JS string literal** |
| `htmlwidgets: true` | in the example | not read by any kit template (builder's search) |
| `authors` | list of `{name, affiliations: {name}}`; **must be `Anonymous` during review**; optional `url` for camera-ready | Distill byline; the generated "cite this work" BibTeX box |
| `bibliography: submission.bib` | must be exactly this name | `<d-bibliography src=".../assets/bibliography/submission.bib">` |
| `toc` | optional list of `{name, subsections: [{name}]}` | contents box; each link is `#{{ name \| slugify }}`, so a name must match its heading's generated id |

Also read by `distill.html` but absent from the example: `openreview_id`
(adds a link to `dev.openreview.net`; **do not set during review**),
`submitted_date`, `date`, and `_styles` (inlined as page CSS).

Two consequences of the layout, from reading it (**not verified by a
preview**):

- `title` and `description` are interpolated raw into
  `let title = "…"; let description = "…";`. A double quote or a line break
  in either would break that script (it builds the "cite this work" box).
  So both must be **one line, with no `"`**. YAML `>-` folding is safe;
  `>` or `|` is not.
- The live under-review submissions (checked 2026-09-27) use `description`
  for **one or two sentences** and put the longer text in the body. None of
  them has an "Abstract" heading.

### S1.5 How the bibliography and assets are resolved

**Bibliography.**

- `compile_submission.py` copies `assets/bibliography/*` into the site.
  The Distill layout points `<d-bibliography>` at `submission.bib`.
- The `.bib` is fetched and parsed **in the reader's browser** by the
  vendored Distill template (`bibtexParse` 0.0.22 plus Distill's
  `normalizeTag`). The site's `jekyll-scholar` setup reads
  `_bibliography/papers.bib`, which the Distill layout never uses.
- Cite with `<d-cite key="…"></d-cite>`. The kit's example puts one key in
  each tag.
- `normalizeTag` only collapses whitespace and strips accent macros of the
  exact forms `{\"a}` and `{\i}`. Any other LaTeX in a field is shown as
  literal text in the reference list, for example `\"{a}`, `{\c{C}}`, `\dh`,
  `\textquotesingle` or `$\frac{1}{2}$`.
- Each reference renders its title, a `[link]` or `[PDF]` from `url`
  (arXiv `abs` URLs are rewritten to `arxiv.org/pdf/…`) and a DOI link.
  These point at the cited works, never at us.

**Assets.**

- `compile_submission.py` copies `assets/{html,img,gif}/<dir>/*` into the
  site: one level of subdirectory, files only.
- Images and GIFs are placed with
  `{% include figure.html path="assets/…" %}`, which
  accepts `caption`, `alt`, `class`, `style`, `width` and `height`.
- Interactive HTML is placed as an `<iframe src="{{ 'assets/html/submission/x.html' | relative_url }}">`.
- `figure.html` adds WebP `<source>` variants (480, 800 and 1400 px) that
  `jekyll-imagemagick` generates for `.jpg`, `.jpeg`, `.png` and `.tiff`
  under `assets/img/`. A GIF gets the same `<source>` tags, which 404; the
  tag's `onerror` handler removes them. The kit's own example GIF uses this
  path.
- The preview page is `/tmlr-beyond-pdf/under_review/submission/`.

### S1.6 The preview: command and Docker image

**Command.** Run `python compile_submission.py` from the kit root, with our
files sitting at `submission_folder/`. In order, it:

1. copies `submission.md` to `tmlr_do_not_modify/_under_review/`;
2. **rewrites every standalone `$` in the body to `$$`** (regex
   `(?<![\\\$])\$(?!\$)`, applied to the whole body, including code blocks
   and HTML comments);
3. copies the bibliography and assets;
4. runs `tmlr_do_not_modify/bin/docker_run.sh`:
   ```
   docker build -t "tmlr-beyond-dev:latest" .
   docker run --rm -v "$PWD:/srv/jekyll/" -p "8080:8080" -it tmlr-beyond-dev:latest \
       bundler exec jekyll serve --trace --future --watch --port=8080 --host=0.0.0.0
   ```
   It serves at `http://0.0.0.0:8080/tmlr-beyond-pdf/under_review/submission/`.

**Image.** Built locally from `tmlr_do_not_modify/Dockerfile`:

- `FROM bitnami/minideb:latest` (Docker Hub);
- `apt-get install` of `locales`, `ruby-full`, `build-essential`,
  `zlib1g-dev` and `imagemagick` (**Debian apt mirrors**);
- `gem install jekyll bundler`, then `bundle install` of the Gemfile
  (**rubygems.org**): `github-pages` plus 15 plugins.

There is no `Gemfile.lock`, and `docker_run.sh` deletes one if present, so
**gem versions float**. The base image is `:latest`. Two previews on
different days can therefore build different sites.

**Mechanics that matter for a headless container:**

- `docker run -it` needs a TTY.
- `jekyll serve --watch` runs until interrupted. It is not a one-shot
  build.
- The script mutates `tmlr_do_not_modify/` (it copies our files in) and
  writes `tmlr_do_not_modify/_site/`.

So run it on a scratch copy of the kit, never inside this repository.

**Network the build needs:** Docker Hub, the Debian mirrors and
rubygems.org. **The last two are outside "GitHub, PyPI, Docker Hub".**

**Alternatives without Docker:**

- the web editor at `https://tmlr-beyond-pdf.org/editor`, which imports and
  exports project zips (the owner, in a browser);
- a local Ruby + Jekyll install from rubygems.org, which the kit does not
  document.

### S1.7 Every external URL the template loads, checked against double-blind

Every URL below is loaded by `tmlr_do_not_modify/`, which authors may not
change, so **every Beyond PDF submission loads the same set.** None is tied
to the authors. The double-blind duty is about what *we* add.

| host | what | loaded by | when |
|---|---|---|---|
| `cdn.jsdelivr.net` | bootstrap 4.6.1 (css, js), mdbootstrap 4.20.0 (css, js), fontawesome-free 5.15.4, academicons 1.9.1, jquery 3.6.0, masonry-layout 4.2.2, imagesloaded@4, mathjax 3.2.0, medium-zoom 1.0.6 | `head.html`, `scripts/*.html` | every page |
| `cdn.jsdelivr.net/gh/jwarby/jekyll-pygments-themes@master` | code-highlight CSS, **unpinned** (`@master`) | `head.html` | every page |
| `fonts.googleapis.com` | Roboto, Roboto Slab, Material Icons | `head.html` | every page |
| `cdnjs.cloudflare.com` | prism 1.29.0 (+ python, bash, json, yaml) | `head.html` | every page |
| `utteranc.es/client.js` | comments widget, `repo=""` (no repository configured) | `_layouts/distill.html` | every page |
| `distill.pub/third-party/katex/` | KaTeX js + css | `template.v2.js` | only if a `<d-math>` element is used |
| `cdnjs.cloudflare.com/…/webcomponents-loader.js` | polyfill | `transforms.v2.js` | only if a Distill transform runs; the layout calls none (builder's reading) |
| `dev.openreview.net` | forum link | `_layouts/distill.html` | only if `openreview_id` is set |

- **Off in `_config.yml`:** Google / Panelbear analytics, site
  verification, Open Graph and Schema.org metadata, dark mode. The
  `site.first_name` / `last_name` fields are empty, so the author `<meta>`
  and the footer name no one (the footer is commented out anyway).
- **What we add must stay self-contained.** Every figure in
  `assets/html/submission/` inlines its own JS, CSS and data. **The kit's
  example `graph.html` does not** (it loads `https://d3js.org/d3.v7.min.js`),
  and it is not copied.
- **Everything under `assets/` is public during review**
  (`tmlr-beyond-pdf.org/under_review`, anonymous).
- **HTML comments** (ledger IDs, TODOs) are invisible on the page but
  present in its source, unless the site's production build minifies them
  away (`jekyll-minifier`, not verified). They must never name a person,
  account, repository or resolving hash.

### S1.8 Which kit files must enter our tree

**None.** The preview needs `compile_submission.py` and
`tmlr_do_not_modify/` *beside* a folder named `submission_folder/`, and it
writes into `tmlr_do_not_modify/`. So:

- unzip the kit to a scratch directory;
- copy `submission.md` and `assets/` from `paper/beyond_pdf/` into the
  kit's `submission_folder/`, after first emptying that folder of the
  kit's example files;
- run the preview there (§S4).

The upload is built the same way: `zip -r submission_folder.zip
submission_folder` from that staged copy, so the zip's top-level folder
keeps the kit's name ("do not change file/folder names"). **`KIT_NOTES.md`
and `.gitignore` are never staged.**

None of the kit's example files are copied into our tree: `Frog.gif`,
`TMLR_Static_Image.jpg`, `graph.html`, `tangent.html` and the two example
`.bib` entries.

### S1.9 Conflicts with the project's constraints

1. **`description` vs the abstract** (a choice the rulings do not cover).
   The instructions say description = abstract. The layout needs it as one
   line with no `"`. Live submissions use one or two sentences.
   - **Proposed in S2, owner to rule:** `description` carries the spine
     abstract's first sentence, verbatim (no numbers). The full abstract,
     with ledger IDs, is the first body section.
2. **`$` → `$$`.** Any literal dollar sign in the body becomes a math
   delimiter, including one inside a comment or code block. The paper's
   cost figures (e.g. GPU spend) must be written `\$` when ported.
3. **Liquid runs over `submission.md`.** `{{` or `{%` anywhere, comments
   included, is executed. Ledger comments and TODO markers must avoid both.
4. **Distill's BibTeX renderer is shallow** (§S1.5). S3 copies entries
   verbatim, so some names and titles will show raw LaTeX in the reference
   list. This is cosmetic. Editing an entry would break "verbatim", so it
   is an owner decision.
5. **The preview needs Docker plus rubygems.org and the Debian mirrors**,
   and floats its versions (§S1.6). A preview result is therefore evidence
   about one build on one day, not about the build TMLR's site runs.
6. **Public rendering during review.** Everything in `assets/` is served
   publicly (anonymously). So:
   - the render JSON sidecars and render README stay out of `assets/`
     (already the rule);
   - the renders' own metadata was checked in S2;
   - HTML comments are visible in the page source (item 3 above;
     §S1.7).
7. **The browser-printed PDF is the archival copy.** GIFs are static in
   it, so every GIF needs its static companion beside it (the SUBMISSION
   FORMAT RULING). The README forbids any other PDF route.
8. **Nothing in the kit conflicts with strict double-blind** once
   `authors` is Anonymous, no author `url` is set, and `openreview_id` is
   left unset.

---

## S4: preview (2026-09-27): FAILED at the Docker step, stopped there

### Exact command

Staged in a scratch directory outside the repository, from the tree at
the S3 commit:

```
unzip -q tmlr-beyond-pdf-author-kit.zip -x '__MACOSX/*'   # sha256 e531434b…bacc2d5 (S1.1)
cd tmlr-beyond-pdf-author-kit
rm -rf submission_folder && mkdir submission_folder        # drop the kit's example files
cp <repo>/paper/beyond_pdf/submission.md submission_folder/
cp -r <repo>/paper/beyond_pdf/assets submission_folder/    # never KIT_NOTES.md or .gitignore
python3 compile_submission.py
```

### Result

- **Merge step: OK.** The bib, 3 PNGs, 3 GIFs and `.gitkeep` were copied
  into `tmlr_do_not_modify/`. The merged `_under_review/submission.md` is
  byte-identical to ours, so the `$` → `$$` rewrite changed nothing.
- **Build step: FAILED.** `docker_run.sh` printed:
  `ERROR: failed to connect to the docker API at unix:///var/run/docker.sock;
  check if the path is correct and if the daemon is running: dial unix
  /var/run/docker.sock: connect: no such file or directory`.
  No image was built and no `_site/` was written.
- **`compile_submission.py` still exited 0.** It ignores the result of
  `os.system`, so its exit code cannot be used to detect a failed preview.
- **Therefore nothing about the rendered page is verified:** layout, TOC
  anchors, math, GIF display, citations and the printed PDF are all
  untested.

Stopped here, per the session brief. Nothing outside `paper/beyond_pdf/` was
edited, and the daemon was not started by any other route.

### Why it fails here, and what else would fail after that (not tested)

1. **No Docker daemon.** Starting `dockerd` was refused by this session's
   permission classifier (S0).
2. **The build needs the Debian mirrors and rubygems.org**, which lie
   outside "GitHub, PyPI, Docker Hub" (S1.6). This is an owner question.
3. **Containers cannot reach this session's egress proxy.** Per this
   environment's proxy README, processes inside containers cannot reach it
   and do not trust its CA. The kit's `Dockerfile` and `docker_run.sh` (do
   not modify) pass neither `--network host` nor the CA, so `apt-get` would
   likely fail even with a daemon.
4. **`docker run -it` needs a TTY**, which this session's shell does not
   have.

### Checks run instead: static, NOT a preview

They show the skeleton is well-formed for the kit's parsers. They show
nothing about how it renders.

- `submission.md` front matter, split exactly as `compile_submission.py`
  splits it:
  - `layout: distill`, `bibliography: submission.bib`;
  - every author Anonymous, with no `url`; no `openreview_id`;
  - `title` and `description` each one line with no `"`.
- **Ledger:** 14 `N:` comments; every ID is a row in
  `paper/numbers_ledger.md`.
- **Kit mechanics:**
  - no `$` in the body;
  - the only Liquid tags are the 2 figure includes;
  - no comment holds a Liquid delimiter or a nested comment;
  - both included asset paths exist.
- **TOC anchors:** all 15 TOC names equal their heading text, and Jekyll's
  `slugify` (default mode) of each name equals the kramdown-GFM id of its
  heading, emulated in Python from the two algorithms. Heading ids are
  unique.
- **Double-blind:**
  - no owner name, account, e-mail, `github.com` or OSF string in
    `submission.md` or the text files under `assets/`;
  - no token in `submission.md` resolves to a commit of this repository;
  - the GIFs carry only the loop and frame-timing extension blocks, and
    the PNGs only IHDR, IDAT and IEND (no text or EXIF chunks).
- **Bibliography, with the kit's own in-browser parser** (Distill
  `bibtexParse` 0.0.22 plus `parseBibtex`, lifted from the kit's
  `template.v2.js` and run under node in the scratch copy):
  - **37 of 37 entries parse.**
  - 8 rendered fields would show raw LaTeX or braces:
    - the titles of `liu2026vulcan` (`{VULCAN}`),
      `agrawal2023multimodal` (`{MARL}`), `bernstein2002` (`{M}arkov`) and
      `kesten1980` (`$\frac{1}{2}$`);
    - the authors of `rutherford2024jaxmarl` (`Gar\dh ar`),
      `cakir2025jaxwildfire` (`{\c{C}}akir`) and `jiang2021robustplr`
      (`Rockt\"{a}schel`);
    - the journal of `zscheischler2020typology` (`\&`).
  - A 9th such field, `tramer2019multiple`'s editor, is never rendered.
  - **Cosmetic.** Fixing any of them edits a verified entry, which is the
    owner's call (S1.9 item 4).

### Routes to a real preview (owner's choice)

- **(a) Laptop with Docker** (the HANDOFF fallback route): the command
  above, in a terminal. The page is at
  `http://0.0.0.0:8080/tmlr-beyond-pdf/under_review/submission/`.
- **(b) This web environment.**
  - It needs the daemon allowed: a permission rule for starting `dockerd`,
    or `dockerd` started by the environment's setup script.
  - It needs the owner's ruling on rubygems.org and the Debian mirrors.
  - Even then, item 3 above may still block the build without kit edits,
    which are not ours to make.
- **(c) The web editor** at `https://tmlr-beyond-pdf.org/editor`, fed a zip
  of the staged `submission_folder/`, in the owner's browser.

Build outputs stay out of git: everything above ran in a scratch directory.
`paper/beyond_pdf/.gitignore` ignores kit copies, `_site/`, `.jekyll-cache/`
and `*.zip` for anyone who stages inside the folder.
