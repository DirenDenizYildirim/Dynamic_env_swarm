# Provenance: sections/11_reproducibility.md

Writer: W5. Checked against the section on 2026-10-11 (Paper v2, step 4, pass 1), with
`paper/v2/src/provenance_check.py`. Demo line references are to
`paper/demo_beyond/sections/` ("demo 08:18" = `08_methodology.md:18`). `log` =
`docs/decision_log.md`. Classes follow `paper/v2/FINDINGS.md`; W5-F* findings are
listed under Open items.

| # | sentence (verbatim) | support | change from the demo, and why |
|---|---|---|---|
| 1 | 11 Reproducibility | framing | kept |
| 2 | The code behind this paper is one repository. | CLAUDE.md:162-221 (the repository layout: `che/env/`, `che/train/`, `che/eval/`, `che/calibration/`, `che/configs/`, `che/scripts/`, `che/tests/`, `docs/locks.yaml`) | edited (demo 11:5): class C, finding N14 (Q4e): the demo's "What the anonymized code supplement contains" became a description of what exists, promising no release (STUB-SPEC PURPOSE; BRIEF §11). The supplement wording is the alternate `sections/alt/11_reproducibility.supplement.md` |
| 3 | It holds the environment, training, evaluation and calibration code, and every configuration, θ\ and the generated protocol configurations included. | CLAUDE.md:162-211 (layout: env, train, eval, calibration; configs incl. `theta_star_holdout` and the generated `p6_*` protocol configurations, CLAUDE.md:206-211) | edited (demo 11:5): directory paths dropped from prose (in-text paths presuppose a supplement, N14; BRIEF §11) |
| 4 | It also holds the analysis scripts that produced the results of §9, a registry of the locked constants, and a CPU test suite that runs the theory checks as unit tests. | CLAUDE.md:212-221 (the analysis scripts `p6_unblind.py`, `p6_post_analysis.py`, `p6_secondary.py`); CLAUDE.md:104-105 (`docs/locks.yaml`); CLAUDE.md:52-55 and :203 (theory tests run as unit tests; CPU suite, CLAUDE.md:236-239) | edited (demo 11:5): "that produced every Phase-6 number" → "that produced the results of §9" (class A, F5: Phase-N named; also narrower: DX-406 is a hand derivation) |
| 5 | A test asserts that the configurations and code defaults agree with the registry and that each registered analysis constant equals the literal in the script that uses it. | che/tests/test_locks.py:4-9 (configs and `config.py` defaults agree with `locks.yaml`), :313-319, :347-361 (each analysis constant's module literal is compared with the registry); CLAUDE.md:294-300 | edited (demo 11:5): "so a lock cannot live only in prose or on a command line" cut (LEN); "instrument" → "script" (class A, F5) |
| 6 | Each listing is a verbatim excerpt of the repository, labelled with file and lines. | paper/v2/src/README.md:119-125 (the build checks that each listing's body equals the named lines of the committed file) | new: what a reader holds without the code: the listings are verbatim, each labelled with its path and lines; fix round (budget): "Each listing in this paper is a verbatim excerpt of the repository, labelled with its file and lines" shortened |
| 7 | Ablations are exact by construction: every stochastic branch consumes its random numbers whether or not its stressor is on, so switching a stressor off reproduces the nested model's trajectories bit for bit under the same keys (§3.4, Listing 3). | CLAUDE.md:46-51 (invariant 3: every stochastic branch consumes its PRNG stream unconditionally; nested models bitwise identical under the same keys) | kept (demo 11:7); the bold label "What is exact, and what is not." dropped: that demo line was one of the two M1 table bugs (class A, M1), and bold labels are out (P3 §6) |
| 8 | Four repeated evaluations of each of two checkpoints are bit-identical on one GPU and identical to the grid's own evaluations. | HW-2; decision log, POST-UNBLIND STAGE RESULT (docs/decision_log.md:5161) | edited (demo 11:7): "on one card" → "on one GPU" (class A, F5); "Evaluation is reproducible:" cut (LEN); evaluation reproducibility is stated once, here (P3-U4; STRUCTURE §7) |
| 9 | Re-evaluated on another GPU, the final checkpoints of all confirmatory runs gave identical completion and survival values in 280 of 288 checkpoint–metric pairs, and the largest absolute difference is 2.44 × 10⁻⁴. | HW-3; decision log, POST-UNBLIND STAGE RESULT (docs/decision_log.md:5161), :5186-5187 ("144 checkpoints paired: 280 of 288 (checkpoint, metric) evals identical"); che/bench/results/phase6/post_unblind_analysis/post_evalfloor_gamma_t_high.md:60-66 | edited: class A, M1. Demo wording: "across cards 280 of 288 paired evaluations are identical, max \|Δ\| = 2.44 × 10⁻⁴", one of the two lines that rendered as a one-row table; now "the largest absolute difference", in words, with no pipe; "cards" → "GPUs" (class A, F5). Home of HW-2 and HW-3 (STRUCTURE §7); fix round, RN2-2 (MUST): the 288 are checkpoint–metric pairs from the re-evaluation of every final confirmatory checkpoint, not 288 evaluations; now "the final checkpoints of all confirmatory runs gave identical completion and survival values in 280 of 288 checkpoint–metric pairs" |
| 10 | GPU training is not run-to-run reproducible (§8), which is why floors are measured (Appendix C). | che/bench/results/phase4/phase4_report.md:637-639; pointer to §8, where the reason is stated | edited (demo 11:7): the reason ("the compiler autotunes kernels by timing and some reductions use atomics") is stated once, in §8's opening, and pointed to here (LEN, N16); "as identical reruns on the card that ran each study" and "the tests of §9 use each arm's own seed dispersion instead …" cut (§8.4 holds it) |
| 11 | On GPU 1, an RTX 5090, a 1000-update training run took 518–521 s and a 512-episode evaluation 9–10 s (Python 3.12.3, jax 0.11.0). | DX-4 (scope: the 76 runs executed on unit 1); DX-5; DX-407 | edited (demo 11:9): "on one RTX 5090" → "On GPU 1, an RTX 5090" (BRIEF §5.2, GPU naming) |
| 12 | A run is 32,768,000 environment steps, each advancing all 12 agents; Appendix B gives the hyperparameters. | DX-3; ENV-6 (12 agents); DX-2 (hyperparameters, Appendix B) | edited (demo 11:9): "for 32,768,000 environment steps per run" kept; "each advancing all 12 agents" from the demo's Appendix G (12:197), which folds into §11 (STRUCTURE §2; P1 §8b, P2 §6.1); "the seed layout and card blocks in Appendix F" cut (Appendix F is indexed) |
| 13 | These are training measurements. | CLAUDE.md:317-322 ("Throughput gates bind only to measured training throughput … any env-only figure states its keep-alive set") | new (folded from demo 12:197, Appendix G): "The only cost figures are training measurements" |
| 14 | The paper states no environment-only throughput figure, because under the compiler's dead-code elimination such a figure depends on which outputs its consumer reads. | CLAUDE.md:320-324 ("Under XLA dead-code elimination 'env-only throughput' is not a single quantity — the compiler deletes whatever the consumer does not read") | edited (demo 12:197, Appendix G): "so any such figure would have to state its keep-alive set; none is needed here" shortened; "keep-alive set" → "which outputs its consumer reads" (class A, F5) |
| 15 | The §9 checkpoints were archived off the rented machines with recorded sha256 hashes, except a partial floor set that grades nothing, in which one of 12 archives has a hash (Appendix F). | DX-408 ("the card-2 partial re-floor holds 12 archives of which 1 has a recorded hash"); DX-36; che/bench/results/phase6/phase6_report.md:78-97; CLAUDE.md:462-469 (archives persisted off-instance) | edited (demo 11:11): "The trained checkpoints are not in the supplement. Each archive has a recorded sha256" → the archive statement without the supplement (class C, N14), with the one exception stated here, since Appendix F does not give the hash count (`14_appendix_plan_provenance.md:112`); the demo's "Appendix F states the one floor set whose archives were mostly never hashed" is replaced; fix round (budget): "The checkpoints of the experiment in §9" → "The §9 checkpoints" |
| 16 | A re-verification matched every recorded hash. | DX-408 (615 of 615 recorded hashes match, re-verified 2026-09-27) | kept (demo 11:11: "a re-verification matched every recorded hash") |
| 17 | The analysis scripts refuse to run out of order, and each stage's log records a single run (Appendix F). | CLAUDE.md:216-217 ("The one-look instruments, each refusing to run out of order"); DX-411 (each stage's log records one invocation) | edited (demo 11:13): "The analysis instruments" → "The analysis scripts" (class A, F5); "(§9.1, blinding)" → "(§9.1)"; the demo's appendix list (11:15-26) is cut, replaced by the appendix index (P2-h; class A, LEN); fix round, RM-7 (MUST) and RC2-2, orchestrator decision 6: "(§9.1)" → "(Appendix F)", where the refusals and one-run logs are stated (`14_appendix_plan_provenance.md:114`) |

## Alternates

- `sections/alt/11_reproducibility.supplement.md`: the first paragraph describes an
  anonymized code supplement (contents with paths; checkpoints excluded), as the demo did;
  every other sentence is identical to the default, and each change is mirrored. The
  default needs no ruling, so it is the one recommended until the owner decides Q4e.

## Open items

- **N14 / Q4e (class C, default kept).** The default §11 states what exists and promises
  no release; it also carries no availability statement, since any wording of one (none,
  "on acceptance", an anonymized supplement) is the owner's call. The supplement framing is
  the alternate. Other sections' in-text code paths presuppose access to the code (N14);
  under the default they name files the reader cannot open. Direction: decide Q4e, then
  either keep the paths as names (listings and their labels, BRIEF §11) or add one sentence
  here on how the code is shared.
- **M1 (class A, applied).** The evaluation figure is stated once, in words ("the largest
  absolute difference is 2.44 × 10⁻⁴"), with no pipe; §9.2 points here (W6).
- **Folded Appendix G (class A).** The throughput statement of the demo's Appendix G
  (12:195-197) is now two sentences here; no environment-only figure and no derived
  training throughput is stated (P3-U5 / Q18 not applied: no row).
- **Appendix F (cross-file).** W6's Appendix F names the 2026-08-14 partial floor set but
  not its hash count (`14_appendix_plan_provenance.md:112`). §11 therefore states it
  (DX-408: one of 12 archives hashed) and points to Appendix F for the set. If W6 adds the
  count there, the clause here can become a pointer.
- **Restatement removed.** The nondeterminism reason is stated once, in §8's opening; §11
  points to it.
- **Budget.** After the fix round: 328 prose words against 300 (+9 %); the alternate is 343 against its cap of 380.

Nothing in the section is unsourced.
- **Fix round (2026-10-12).** RN2-2: the 288 are checkpoint–metric pairs from re-evaluating every final confirmatory checkpoint (log:5186-5187), not 288 evaluations; HW-3's own wording ("paired cross-card evals") is a record item. RM-7 / RC2-2: the one-look pointer is now Appendix F (decision 6).
