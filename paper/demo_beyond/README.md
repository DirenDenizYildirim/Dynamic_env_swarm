# `paper/demo_beyond/`: a builder-written Beyond PDF demonstration

**Not the owner's paper.** Written 2026-10-11 under the decision log's
*DEMONSTRATION DRAFT* ruling. The owner wanted to see how a static paper
becomes a TMLR Beyond PDF paper. The title, abstract and `description` are
the owner's, copied verbatim from `paper/finale.md` at build time. Every
other word is builder text. `paper/finale.md` is untouched, and whether
any of this moves into it is the owner's decision.

| path | what |
|---|---|
| `sections/00_hero.md` … `12_appendix.md` | the body, in the kit's syntax: Markdown, raw HTML, the two Liquid forms, MathJax, `<d-cite>`, iframes. Line 1 of each carries the builder-written label |
| `submission_demo.md` | **generated.** The assembled kit source: what `submission_folder/submission.md` would hold, with the YAML header (owner's fields, plus a generated `toc` and `_styles`) |
| `out/index.html`, `out/files.json` | **generated.** A preview in the kit's Distill look (the kit's CSS via the 2026-09-28 preview), and the map from published asset path to repository file |
| `BRIEF.md` | the keeper's brief to the four section writers: rulings, registered strings, honesty lines, traps, kit syntax, per-section facts |
| `ledger_supplement.md` | numbers the paper needs that have no row in `paper/numbers_ledger.md`, each verified against its committed source (DX-1 … DX-40, then the writers' DX-1xx … DX-4xx) |
| `REVIEW.md`, `review/` | the three independent reviews (claims, numbers, mechanics), the fix-round decisions, each writer's resolutions, and the re-check |
| `src/build_demo.py` | the assembler (pyyaml, markdown-it and pygments, all already in the venv) |

Build from the repository root:

```sh
.venv/bin/python paper/demo_beyond/src/build_demo.py
```

The build fails if a ledger ID or a citation key does not resolve, or if
any Liquid form other than the kit's two appears.

The preview imitates the kit; it is not the kit's Jekyll build. The kit
preview (`paper/beyond_pdf/KIT_NOTES.md` §S4) is still owed before any
upload. Before upload, strip the HTML comments (ledger IDs included), as
the checklist's comment-stripping item requires.
