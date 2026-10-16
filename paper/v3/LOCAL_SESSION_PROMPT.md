# Kickstart prompt: the local session that runs the interaction check and closes step 0

Paste everything below the line as the first message of a Claude Code session
started on your laptop, in the repository, on branch
`claude/fervent-newton-ws5yub`.

---

This session continues Paper v3. It runs on my laptop, which holds the
Phase-6 checkpoint archives. Its job is to get the eval-only interaction
check run on a rented RTX 5090, bring the results back, analyse them once,
and finish the paper's interaction-dependent parts. Follow `CLAUDE.md`
(auto-loaded) and the rules in `paper_v3_prompt.md`, "Rules that bind every
agent".

## Read first (lean)

1. The decision log (`docs/decision_log.md`), from "## PAPER V3 —" to the end:
   PAPER V3, PAPER V3 PHASE 1 START, COMMITS AUTHORIZED, PLAN OK.
2. `paper/v3/HANDBACK.md` and `paper/v3/OWNER_QUESTIONS.md`.
3. `che/bench/results/phase6/post_v3_interaction/PLAN.md` (approved, frozen)
   and `RUNBOOK.md` in the same folder. The runbook is the procedure. Follow
   it step by step, and tell me each command before I run it on the GPU box.

## State and fixed values

- Branch `claude/fervent-newton-ws5yub`. The plan was approved unchanged
  (log: PLAN OK, 2026-10-16).
  - **C** (commit to ship) = `ab78b27dab97e6be45abbdbe2e9e1bf43b170a05`, or a
    later commit on this branch that leaves PLAN.md, the configs, `che/env`,
    `che/train`, `che/eval` and the run script unchanged. If you ship a later
    commit, confirm that with `git diff C..HEAD`.
  - **P** (PLAN.md sha256) =
    `c3ec2dd147479b6b88ff36c30002d8e6e30873e997798b92935d8c40b2a1b809`.
- Scope: θ\* only. 692 evals (656 main + 36 floor). No training; Low and
  High are not authorized. Cost estimate 1.8–2.8 GPU-hours, which is not a
  trigger.
- Commits: allowed, to this branch only. Commit and push at the end of each
  step below.

## Steps

1. **Check the tree.** Run `git status`, `git rev-parse HEAD`, and
   `sha256sum che/bench/results/phase6/post_v3_interaction/PLAN.md` (it must
   equal P). Then run `uv run pytest -q che/tests/test_interaction_check.py`.
2. **Find and verify the archives** (RUNBOOK §0). Locate the 164 archives
   on this laptop or in the 2026-09-27 backup. Ask me where they are; do not
   search my whole disk. Restore them into `che/bench/results/phase6/g1_conf_5090/`
   and `.../g1_iso4_5090/`. Then run
   `VERIFY_ONLY=1 bash che/scripts/run_interaction_evals.sh`; it must report
   `verified=164 bad_or_missing=0`. If any archive fails, stop and report
   it. Never substitute another file.
3. **Prepare the box** (RUNBOOK §1–§3). I rent the RTX 5090. Then:
   - build the tree tarball with `git archive` at C, plus a tarball of the
     164 archives, each with its sha256;
   - give me the copy commands;
   - on the box: run the verify-only check again, set up with
     `uv sync --extra cuda`, and confirm `jax 0.11.0` and a CUDA device.
4. **Run** (RUNBOOK §4–§5). Do the dry run (it must say 692), then the real
   run, inside tmux:
   `GIT_COMMIT=C PLAN_SHA256=P bash che/scripts/run_interaction_evals.sh`.
   If it stops, re-run the same command. Never edit anything on the box.
5. **Bring the results back** (RUNBOOK §6). Copy
   `v3_interaction_results.tar.zst`, `SHA256_RESULTS.txt` and
   `interaction_console.log` to the laptop, and verify the hash. Only then
   tell me the box can be released.
6. **Analyse once** (RUNBOOK §7).
   - Extract the archive into `che/bench/results/phase6/post_v3_interaction/`.
   - Check that `.plan_at_run.md` is byte-identical to the committed PLAN.md.
   - Commit the results, then run
     `uv run python -m che.scripts.interaction_analysis` once, on the clean
     tree, and commit its report.
   - Do not re-run it to get a different answer. Every run is logged in
     `ANALYSIS_LOG.txt`.
7. **Rows.** In `paper/v3/ledger_proposals/IC.md`:
   - flip IC-1 to IC-6 from PENDING-COMMIT to VERIFIED, since PLAN.md is
     committed;
   - add VERIFIED result rows IC-7 onward, each read from the committed
     `interaction_report.{md,json}` at file:line. They cover the per-arm and
     pooled I with interval ends, the MDE80s, the self-floor result, the
     cross-GPU identical count, and the realized GPU-hours from
     `timings.txt`.
8. **Fill the holes.** Fill the 7 `<!-- HOLE:INTERACTION -->` markers in
   `paper/v3/sections/`: §6.4, §6.5's lesson, App. G's tables, the abstract's
   lesson sentence, §1's sentence and §9's clause.
   - Build Figure 9 from the committed outputs, into a new output directory
     (`paper/v3/plans/P2.md` §3).
   - Follow PLAN.md §7's reading rules exactly. If there is no detectable
     interaction, state it as an exclusion with its bound, never as "no
     interaction". The check is labelled post hoc everywhere.
   - Keep one provenance row per changed sentence
     (`paper/v3/src/provenance_check.py --root paper/v3 --strict`).
   - Run the v3 checks (`paper/v3/src/v3_checks.py` terms, dates, caveats).
9. **Review and rebuild.** Take a snapshot (`paper/v3/src/snapshot.sh`).
   - Have the changed lines re-checked in independent lanes (claims and
     numbers), and record the outcomes in `paper/v3/REVIEW.md`.
   - Then run the real-kit build (`paper/v3/src/kit_build.sh`). The main text
     must stay at or under 15 printed pages from page 1, unless I rule
     otherwise (owner question Q3).
   - Rebuild the supplement (`paper/v3/supplement/package.py`, then
     `run_checks.sh`).
10. **Hand back** in a short update to `paper/v3/HANDBACK.md`: the reading,
    what changed, every check that ran, and what still waits on me. The other
    owner questions (Q1–Q10, C1–C6) stay open until I answer them.

## Do not

- Do not edit PLAN.md, the configs or the run and analysis scripts. If one
  of them looks wrong, stop and tell me.
- Do not edit `CLAUDE.md`, `docs/theory_foundations.md`, the canonical
  ledger, the registered documents, `paper/finale.md`, `paper/beyond_pdf/`
  or `paper/v2/`.
- Do not put anything into `paper/finale.md` or the submission. That waits
  for my section-by-section approval.
- Every new ruling of mine is transcribed into the decision log before it
  is acted on.
