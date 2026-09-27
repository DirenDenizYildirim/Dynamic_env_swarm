# Beyond PDF scaffolding — prompt for a Claude Code web session

Written 2026-09-27 (decision log, *SCAFFOLDING SITE*). You are the builder,
working in a Claude Code web container from this repository's GitHub copy.
**Your job is structure, not prose:** a TMLR Beyond PDF submission skeleton
the owner and later sessions can port the paper into.

## Read first, in order

1. `CLAUDE.md`: the working rules. Transcription, derived numbers and the
   instruments law all apply to paper work.
2. `HANDOFF.md`.
3. `docs/decision_log.md` from *UNBLIND RESULT* (2026-09-26) to the end,
   especially *SUBMISSION FORMAT RULING* + its addendum, and *SCAFFOLDING
   SITE*.
4. `paper/00_common_spine.md`: the port source. `paper/branch_B.md`: the
   record behind its §9.
5. `paper/numbers_ledger.md`: every number's source and row ID.
6. `paper/99_pre_submission_checklist.md`, the "Beyond PDF format" and
   "TMLR mechanics" sections.
7. `paper/related_work_verification.md`: the **only** allowed source of
   BibTeX.

## Hard constraints (from the rulings; not yours to relax)

- **Double-blind, strictly.** `authors` anonymous. No repo URL, OSF link,
  GitHub username, owner name, or account-resolving commit hash anywhere in
  `submission.md` or `assets/`. No script, font or data loaded from a URL
  tied to the authors.
- **Numbers:** add no number the ledger does not have. Every number you
  place carries its row ID as an HTML comment, e.g. `<!-- N:RES-2 -->`. If
  you need one that has no row, stop and list it; do not derive it.
- **Do not touch** `che/`, `docs/locks.yaml`, `pyproject.toml`, `uv.lock`,
  or `paper/tex/` (frozen DMLR fallback). The kit and preview are paper
  tooling only.
- **The kit is read in full before any of its files enter the tree.**
- **GIFs illustrate and never grade.** No acceptance-rate or odds figure
  anywhere.
- If the kit forces a choice the rulings don't cover, **stop and ask the
  owner.** A choice you make is a proposal until it is transcribed.

## GIFs: use the committed renders, never render trained policies here

Checkpoint archives are gitignored and live only on the owner's laptop, so
you **cannot** render trained Phase-6 policies here. Three renders made on
the laptop are committed at **`paper/renders/2026-09-27/`**: a random
policy, ISO seed 1 and JOINT seed 1, at θ\*, each with a `*_static.png`
companion. The owner may also upload the same files as a tar; if so, check
them against that directory's `SHA256SUMS`.

**Read its `README.md` before placing anything.** It carries the selection
rule and the reading rules: single episodes, illustrate and never grade.
The ISO/JOINT pair must not be captioned as showing the result, and
whether to show them side by side is the owner's call. In S2, copy the GIFs
into `assets/gif/submission/` and the PNGs into `assets/img/submission/`.
The JSON sidecars and the README stay out of `assets/`. Any further GIF
slot is a marked placeholder (`<!-- GIF: rendered on laptop -->`); never
fill it with a random-policy render standing in for a trained one.

## Milestones: commit after each, with the milestone name in the message

**S0 — environment check.** Confirm `docker` runs and the kit's source is
reachable. The default "Trusted" network covers GitHub, PyPI and Docker
Hub. If the kit's build fetches from anywhere else and fails, stop and tell
the owner to switch this environment's network access to "Full". Do not
work around it.

**S1 — kit notes.** Fetch the official *TMLR Beyond PDF Author Kit* into a
scratch directory **outside the repo** and read all of it. Write
`paper/beyond_pdf/KIT_NOTES.md` covering:
- source URL and the kit's commit or version;
- licence;
- file layout;
- the `submission.md` YAML header fields;
- how the bibliography and assets are resolved;
- the preview command and its Docker image;
- every external URL the template loads (fonts, scripts, CDNs), checked
  against the double-blind constraint;
- which kit files, if any, must enter our tree for the preview to work;
- anything that conflicts with the constraints above.

Commit only the notes.

**S2 — skeleton.** Create `paper/beyond_pdf/` in the kit's layout
(`submission.md`, `assets/{img,gif,html}/submission/`,
`assets/bibliography/submission.bib`), bringing in only the kit files S1
showed are required.
- **YAML header:** anonymous authors. The title is the first spine
  candidate, marked `<!-- PROVISIONAL: owner chooses the title -->`.
- **Sections:** follow the spine's order (§1–§11, then the appendix
  manifest). Each body is one line pointing at its spine section plus
  `<!-- TODO(port) -->`.
- **Abstract:** the one piece of prose. Port the spine's "Abstract —
  branch B" verbatim, with a ledger ID beside every number.
- **Figures:** figures 1–10 from the spine's figure list become labelled
  slots, each naming its committed data source. GIF slots are placeholders,
  as above.

**S3 — bibliography.** Fill `submission.bib` by copying the verified BibTeX
entries from `paper/related_work_verification.md` verbatim. Never write an
entry from memory. Entries the spine marks `[OWNER READS]` go in with a `%`
comment saying so.

**S4 — preview.** Build the skeleton with the kit's preview. Record the
exact command and the result in `KIT_NOTES.md`. Keep build outputs out of
git (a `.gitignore` inside `paper/beyond_pdf/` is fine). If the preview
fails, record the failure and stop. Don't fix it by editing anything
outside `paper/beyond_pdf/`.

**S5 — hand back.** Update `HANDOFF.md` ("Next, in order") and tick what's
done in the checklist's Beyond PDF section. Push your branch. **Do not merge
to `main`.** The owner reviews the diff.

## Out of scope for this session

Porting prose beyond the abstract. Rendering figures. Any `che/` code.
Ledger items O-1 to O-4 (owner decisions or later builder work). The
`phase6_design_v2.md` §2 amendment.
