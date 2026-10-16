# Resolutions — the supplement builder (Paper v3, step 2; recorded by the orchestrator, 2026-10-16)

Findings from `review/RM.md` that touch `paper/v3/supplement/` and the zip.
Source: the supplement builder's final report and `paper/v3/supplement/README.md`
("Check results"). The zip is `paper/v3/out/che_supplement.zip`, sha256
`4a73c89b57b923a0a13576fb9b0ac2f5184126ec55c5d205ce302a7ec4edcbfb`.

## Final pass

| finding | outcome | what changed | reason |
|---|---|---|---|
| RM-13 | FIXED | `supplement/README.md` "Check results" filled: scrub PASS (190 rewrites, 0 warnings), size PASS (37.7 % of 100 MB), tests PASS on re-run (601 passed, 4 skipped, 0 failed), manifest PASS (4,166 files), reproduce PASS (8 of 8) | the section was empty |
| RM-14 | FIXED | the shipped README gives the measured suite time (about 52–56 min on 4 cores) and lists the four skips | "in minutes" was wrong |
| RM-15 | FIXED | `post_v3_interaction/RUNBOOK*` is on a deny list checked before any include rule; absent from the zip, listed in `out/excluded_summary.txt` | the runbook addresses the owner |
