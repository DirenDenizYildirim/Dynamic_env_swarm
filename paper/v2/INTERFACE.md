# paper/v2 interface contract (orchestrator, 2026-10-11)

Fixed before step 3 so that B1 (content scaffold) and B2 (build and checks)
can work in parallel on disjoint files. A builder may extend this contract
but must not break it. Record any extension in your own output file, never
here; this file belongs to the orchestrator.

## Layout

| path | owner (step 3) | owner (step 4) | what |
|---|---|---|---|
| `INTERFACE.md` | orchestrator | orchestrator | this contract |
| `plans/P1–P3.md`, `review_of_demo.md`, `citations/C1_verification.md` | steps 1–2 (done) | read-only | inputs |
| `STRUCTURE.md` | B1 | read-only | the reconciled structure, which plan each choice came from, writer assignments |
| `BRIEF.md` | B1 | read-only (the orchestrator may append rulings) | rules, traps, kit syntax, glossary, per-section facts |
| `FINDINGS.md` | B1 | review lanes append outcomes | the disposition of every finding: fix-list items, N1–N17, the plans' findings, O1 |
| `ledger_supplement.md` | B1 (verbatim carry-over of the demo's, header updated) | read-only | DX rows, IDs unchanged |
| `ledger_proposals/W<n>.md` | — | writer W<n> | new VERIFIED rows, same row format as the supplement; IDs `V<n>-<k>` (e.g. `V3-1`) |
| `front_matter.yaml` | B2 (placeholders) | W1 (title, `description`) | YAML header fields the build reads |
| `sections/NN_slug.md` | B1 (stubs) | the assigned writer | the paper, in kit syntax |
| `sections/alt/NN_slug.<variant>.md` | B1 (only where an owner choice needs one) | the assigned writer | alternates for owner choices, swapped in by a build flag |
| `provenance/TEMPLATE.md` | B2 | read-only | the per-sentence provenance format |
| `provenance/NN_slug.md` | — | the assigned writer | one row per sentence |
| `assets/bibliography/submission.bib` | B2 | read-only | the v2 bibliography: a verbatim copy of the corrected entries of `paper/related_work_verification.md` |
| `src/` | B2 | B2 / orchestrator | the build (`build_v2.py`), the real-kit build and checks, the provenance check, the snapshot/diff helper |
| `out/` | build output | build output | the generated kit source `submission_v2.md`, the preview, `files.json`, check reports |
| `review/` | — | step-4 review lanes | claims, numbers, mechanics |
| `REVIEW.md` | — | orchestrator | the outcome of every finding |

## Section files

- **Order and naming.** Files are named `sections/NN_slug.md` and assembled
  in filename order. Two files come first, in this order:
  `00_abstract.md` (the abstract, body text before the hero) and
  `00_hero.md`. The appendix files come last.
- **Line 1** is the status comment, exactly:
  `<!-- PAPER V2 DRAFT (PAPER V2 ruling, 2026-10-11): builder-drafted, not owner-approved -->`
- **Headings.** Each numbered section opens with one H2, `## N Title`.
  Subsections are H3. The `toc` is generated from the H2s. Keep dots and
  parentheses out of H2 text, beyond the leading section number.
- **Stub specification.** A stub carries its specification in one block,
  `<!-- STUB-SPEC` … `-->`, right after the heading. Writers keep the block
  until the owner's review. The build reports how many STUB-SPEC blocks
  remain, and staging strips them along with every other comment.
- **Numbers.** Every number is followed by `<!-- N:ID -->`. IDs resolve
  against `paper/numbers_ledger.md`, `paper/v2/ledger_supplement.md` and
  `paper/v2/ledger_proposals/*.md`, and the build fails on an ID that does
  not resolve.
- **Citations.** Write `<d-cite key="k1,k2"></d-cite>`. Every key must exist
  in `paper/v2/assets/bibliography/submission.bib`; the build fails
  otherwise.
- **Listings.** Every fenced code listing is preceded, on its own line, by
  `<!-- LISTING: <repo-relative path>:<start>-<end> -->`. The build checks
  that the fence body is byte-identical to those lines of the committed
  file.
- **Cross-references** are written as plain text ("§9.2", "Figure 4",
  "Table 2", "Listing 3", "Appendix C"). The build lists each one with the
  target it resolves to, for the mechanics review.
- **Liquid.** Only the kit's two forms are allowed:
  `{% include figure.html … %}` and `{{ '…' | relative_url }}`.

## Ledger rows (proposals)

Each row uses the format of `paper/demo_beyond/ledger_supplement.md`. A row
carries:

- its ID;
- its value;
- its source as committed file:line;
- `VERIFIED` (read this session from that file:line), or the row is not
  added.

## Provenance rows

`provenance/NN_slug.md` has one table row per sentence of the section, in
order:

| # | sentence (verbatim) | support | change from the demo, and why |
|---|---|---|---|

Support is one of:

- ledger ID(s);
- a decision-log entry heading with its line number;
- file:line;
- a citation key, plus the `related_work_verification.md` line that
  supports the use;
- `framing`, for a sentence that makes no claim.

Captions, table cells with claims, and `alt` text count as sentences.
