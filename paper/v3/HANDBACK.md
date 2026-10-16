# Paper v3, phase 1: hand-back to the owner (step 4.5)

Orchestrator, 2026-10-16. Phase 1 ran every step of `paper_v3_prompt.md`
except the GPU run, which is yours. **Nothing is approved or adopted:**
`paper/finale.md`, `paper/beyond_pdf/` and `paper/v2/` are untouched. Work is
committed on `claude/fervent-newton-ws5yub` (log: *PAPER V3 PHASE 1 START*,
*COMMITS AUTHORIZED*).

## Where to look

| what | where |
|---|---|
| **Your decisions (one page)** | `paper/v3/OWNER_QUESTIONS.md` |
| The built page (private artifact) | ARTIFACT_LINK |
| Printed PDF (real-kit build) | `paper/v3/out/submission_v3_print.pdf` |
| Staged submission (comments stripped) | `paper/v3/out/submission_folder.zip` |
| Code supplement (37.7 MB; not in git) | `paper/v3/out/che_supplement.zip`; contents, rules and checks in `paper/v3/supplement/README.md` |
| The source, one file per section, plus alternates | `paper/v3/sections/`, `paper/v3/sections/alt/` |
| Per-sentence provenance | `paper/v3/provenance/<section>.md` |
| New rows | `paper/v3/ledger_proposals/W2.md`, `W4.md`, `W5.md`, `IC.md` |
| Every finding and its outcome | `paper/v3/REVIEW.md`; raw reviews and resolutions in `paper/v3/review/` |
| The interaction check: plan, runbook | `che/bench/results/phase6/post_v3_interaction/PLAN.md`, `RUNBOOK.md` |
| The blind review (you run it) | `paper/v3/BLIND_REVIEW.md` |
| How it was planned and built | `plans/P1–P3.md`, `STRUCTURE.md`, `BRIEF.md`, `DISPOSITIONS.md`, `WRITERS.md`, `src/README.md`, `src/VALIDATION.md` |

## What changed from v2

- **Environment first.** CHE is the contribution (§3–§5: the couplings, the
  hazard-blind reward, severity placed by measured percolation, exact nested
  ablations, theory as unit tests, the floors protocol), each property with
  the rows, listing and test that carry it (Table 2). The pre-registered test
  is the worked example (§6), opening with the framing-change disclosure.
- **Shorter and plainer.** 14 main-text section files; the audit trail moved
  to a registration-timeline appendix (App. D). No internal codes, private
  vocabulary or dates in the main text except the unblinding date (checked).
  Each caveat has one home (checked, 39 of 39).
- **The professor's points:** the size is stated plainly (about a tenth of an
  agent per episode, detectable only in the last fifth); the identity
  active share = μ_A + μ_B − p replaces the "match the active share" advice;
  the plane decomposition leads §6.3 as non-verdict-bearing; Remark 1 is cut
  and Prop. 4 is an appendix remark; limitations are up front.
- **Theorem 1 (V3-E2).** The paper's closed form did not describe the tested
  toy; the default now states it for per-step optical depths, as the code
  implements it (owner question Q4).
- **Verifiability.** An anonymized supplement, and App. D now gives the
  registration documents' commit dates, read from the full history, stated
  as self-reported.
- **The interaction check** is prepared, not run: §6.4 and App. G describe the
  design exactly as `PLAN.md` states it, and every result is a marked hole.

## Waiting on you

1. **Q0, the plan's OK**, then the GPU run (`RUNBOOK.md`; about 1.8–2.8
   GPU-hours, an estimate). After the results return, a session verifies
   them, runs the analysis once and fills the 7 holes, Figure 9 and the IC rows.
2. The rest of `OWNER_QUESTIONS.md`: title, page measure, Theorem 1, Prop. 4,
   figures, the disclosure footnote (yours to write) and App. J, the δ label,
   the date, and the record items.
3. The blind review (`BLIND_REVIEW.md`), outside this repository.

## Findings not fixed, and why

- **Print legibility** (RM-OWNER-3): every figure's labels print at 2.5–4.3 pt.
  Fixing it needs figure rebuilds, which need your agreement (Q6).
- **Owner-marked items** (28 `OWNER-PENDING` markers): defaults are in the
  text; each is in `OWNER_QUESTIONS.md`.
- **RM-13**: STATUS_RM13
- **CA-9's scale clause** (RN1-8): did not fit §3's budget; the stray
  punctuation it left is fixed. A 12-word restore is possible if you accept
  the overrun.

## Checks that ran this session

| check | result |
|---|---|
| Real-kit build (kit sha256 verified) | 40 PASS, 1 FAIL (print legibility), 6 INFO |
| Main-text printed pages | 14.70 from page 1, 13.27 from §1 (ceiling 15; results not yet added) |
| v3 checks: terms, dates, caveats | PASS, PASS, PASS (39 of 39) |
| MathJax; tables; cross-references | 0 errors in 341; 0 prose pipes; 0 unresolved of 264 |
| Provenance (`--strict`), every section and alternate | every sentence has a row; 0 stale; 0 support problems |
| `build_v3.py --final` | blocked only by `date_confirmed`, 23 STUB-SPEC blocks and 7 tags on PENDING IC rows (expected) |
| Artifact bundle in headless Chromium | 0 failed requests; 341 of 341 math; 10 of 10 iframes; 13 of 13 images |
| Step-0 tests (`test_interaction_check.py`, incl. a real CPU end-to-end run) | PASS |
| Full CPU suite | 598 passed, 6 skipped, 1 failed: the frozen-base test, which fails on the untouched `7a5e009` too (record item C1) |
| Supplement: scrub, size, manifest | PASS, PASS (37.7 of 100 MB), PASS; tests inside the unpacked supplement: STATUS_SUPP |
| Reviews | 5 lanes; 92 findings (9 MUST, 73 SHOULD, 10 OWNER). The 8 MUSTs on draft1 were fixed and re-checked OK by their reviewers (one after a reopen and a final pass); the 1 MUST the re-check found (a stray ",." in §3) was fixed in the final pass and confirmed by the final build, not by a reviewer |

**Not checked:** TMLR's site, the OpenReview upload, the kit's web editor;
the artifact in claude.ai's own viewer beyond publishing it; a Docker-route
PDF (the PDF comes from headless Chromium, as in v2).
