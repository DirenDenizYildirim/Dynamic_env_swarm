# Provenance: sections/13_appendix_locks_floors.md

Writer: W5. Checked against the section on 2026-10-11 (Paper v2, step 4, pass 1), with
`paper/v2/src/provenance_check.py`. Demo line references are to
`paper/demo_beyond/sections/` ("demo 08:18" = `08_methodology.md:18`). `log` =
`docs/decision_log.md`. Classes follow `paper/v2/FINDINGS.md`; W5-F* findings are
listed under Open items.

| # | sentence (verbatim) | support | change from the demo, and why |
|---|---|---|---|
| 1 | B Locks and hyperparameters | framing | kept (demo 12:39; W5's file from v2, STRUCTURE §10) |
| 2 | Each locked constant below was fixed by a ruling on the date given, and the test described in §11 checks each against the configurations, the code defaults or the analysis scripts. | DX-401; DX-402; che/tests/test_locks.py:4-9, :313-319, :347-361 | edited (demo 12:41): the test is described once, in §11, and pointed to here (LEN); the file path is dropped from prose (in-text paths presuppose a supplement, N14; BRIEF §11) |
| 3 | constant / value / ruled / record | framing | kept |
| 4 | critical point $\hat\beta_c$ / 0.500 ± 0.005 / 2026-07-19 / severity lock record; no committed script reproduces its estimator, and the committed estimators give a crossing mean of 0.504 and a consensus of 0.499 | CAL-1 (its note, the open item on provenance: no committed script produces the R_L logistic centres; committed estimators give a crossing mean of 0.504 and a consensus of 0.499); DX-401 | edited (demo 12:45): "its estimator (R_L logistic centres) has no committed script" → "no committed script reproduces its estimator" |
| 5 | β Low / Medium / High / 0.43 / 0.49 / 0.70 / 2026-07-19 / severity lock record | CAL-3; DX-401 | kept |
| 6 | β held out (θ\) / 0.49 / 2026-08-02 / the ruling that sited θ\: train at the two extremes and hold out the middle | CAL-3; DX-401; docs/locks.yaml:90-100 ("Phase 6 trains on the EXTREMES {0.43, 0.70} and holds out the middle") | edited (demo 12:47): "Phase-6 design ruling; equal to β Medium, kept separate because the role differs" → the ruling's own description (class A, F5: Phase-N; "kept separate because the role differs" has no source in the lock entry) |
| 7 | $f_{\mathrm{weak}}$, $\lambda_0$, $\lambda_{\mathrm{load}}$, $\kappa_A$, $r_A$ / 0.15, 5e-5, 4e-4, 0.06, 1 / 2026-07-21 / Coupling-A lock record | CA-1; DX-401 | kept |
| 8 | weak-floor smoothing passes / 2 / 2026-07-21 / Coupling-A lock record, locked as the code default | DX-401 (weak_smooth 2, "locked as-is"); docs/locks.yaml:150-156 ("supplied_by: default") | edited (demo 12:49): "Coupling-A lock record" → "…, locked as the code default" |
| 9 | $\kappa_B$ / 1.0 / 2026-07-27 / Coupling-B lock record, on the detection band alone | CB-1; DX-401 | edited (demo 12:50): "κ_B lock record" → "Coupling-B lock record" |
| 10 | δ off / on; $R_{\mathrm{comm}}$ / 0.0 / 1.0; 16 / 2026-07-30 / communication lock record | DX-401; COM-6 | kept |
| 11 | death penalty $d_p$ / 0.5 / 2026-07-19 / the death-penalty design decision | ENV-1; DX-401 | kept |
| 12 | observation encoding / 3, the masking observation (§3) / 2026-07-24 / the observation design decision | DX-401 (obs_version 3, ruled 2026-07-24); docs/locks.yaml:242-247 | edited (demo 12:53): "v3" → "3, the masking observation (§3)" (class A, F5: obs v3, BRIEF §5.2); "frozen after the Coupling-B observation milestone" cut (its source names a milestone code) |
| 13 | $\sigma_s$, η, ι / 1.0, 0.5, 0.0 / not locked / held fixed by convention, never calibrated | DX-1 | kept |
| 14 | analysis constant / value / ruled / role | framing | kept |
| 15 | K_CONFIRMATORY / 40 / 2026-08-03 / the design seed count per confirmatory arm, against which the registered seed rule computes | DES-1; DX-402; docs/locks.yaml:295-300 | edited (demo 12:58): "the re-floor ladder computes against it" → "against which the registered seed rule computes" (class A, F5); the code identifier kept as a table label (STUB-SPEC) |
| 16 | K_LADDER_CAP / 60 / 2026-08-03 / the seed rule's cap | DES-1; DX-402 | edited (demo 12:59): "the ladder's cap" → "the seed rule's cap" (class A, F5) |
| 17 | K_CONFIRMATORY_REALIZED / 72 / 2026-09-22 / the seed count at which Γ is read, a recorded deviation (§9.1) | DES-3; DX-402 | edited (demo 12:60): pointer "(§9.1)" added |
| 18 | K_SECONDARY / 20 / 2026-08-02 / seeds per secondary arm; ISO-4 uses the same count | DES-13; DX-402 | edited (demo 12:61): "the same k" → "the same count" |
| 19 | SIDAK_M; $z_\alpha$ / 2; 2.2365 / 2026-08-02 / the confirmatory family: the two co-primary tests, Šidák-corrected | DES-13; DX-402 | edited (demo 12:62): "the confirmatory family of two co-primaries" → the glossary's definition (BRIEF §5.2; class A, F5) |
| 20 | POWER_STOP / 0.80 / 2026-08-02 / the minimum design-stage power at the 0.03 band | DX-402; DES-4 | kept |
| 21 | T_STAR / 1000 / 2026-08-11 / the fixed training budget in updates, a value unchanged since 2026-08-03 | DES-13; DX-402 | edited (demo 12:64): "(provenance re-pointed; value unchanged since 2026-08-03)" → "a value unchanged since 2026-08-03" |
| 22 | GAMMA_T_RETENTION / 11 / 2026-08-11 / checkpoints kept for Γ(t): updates 500–1000 every 50 | DES-13; DX-402 | kept |
| 23 | evaluation draw / seed 0 × 512 episodes / registered with the grid layout / common to every run; not in the lock registry | DES-13; phase6_framing_branches.md:264-267 ("Registered with the grid layout … All 240 runs are evaluated on the same 512-episode set (eval seed 0)"); docs/locks.yaml:293-462 (no entry for the draw) | edited (demo 12:66, "with the grid layout / common to every run"): "registered" and "not in the lock registry" added, since the opening sentence speaks of locked constants only (accuracy) |
| 24 | PLATEAU_PASS; PLATEAU_REVIEW / 1.0; 1.5 / 2026-08-02 / thresholds of the registered convergence check, retired as a gate on 2026-08-11; they grade nothing | DX-402; METH-6 | edited (demo 12:67): "the plateau criterion, retired as a certification instrument" → "the registered convergence check, retired as a gate" (class A, F5) |
| 25 | The training hyperparameters are identical for every run of §9; the grid passes none on the command line, so the configured defaults apply. | DX-2 (note: "the grid passes no hyperparameter flag, so the dataclass defaults apply") | edited (demo 12:69): "every Phase-6 arm" → "every run of §9" (class A, F5) |
| 26 | hyperparameter / value | framing | kept |
| 27 | learning rate / 3e-4, constant, no schedule | DX-2 | kept |
| 28 | discount γ; GAE λ / 0.99; 0.95 | DX-2 | kept |
| 29 | PPO clip ε / 0.2 | DX-2 | kept |
| 30 | entropy coefficient; value coefficient / 0.01; 0.5 | DX-2 | kept |
| 31 | global gradient-norm clip; Adam ε / 0.5; 1e-5 | DX-2 | kept |
| 32 | parallel environments; steps per update / 256; 128 | DX-2 | kept |
| 33 | minibatches; epochs / 4; 4 | DX-2 | kept |
| 34 | checkpoint interval / 50 updates | DX-2 | kept |
| 35 | budget / 32,768 environment steps per update, 32,768,000 per run | DX-3 | kept |
| 36 | C Floors | framing | kept |
| 37 | A floor is the standard deviation of a metric over identical reruns at one seed, so it measures nondeterminism alone. | che/bench/results/phase5/phase5_report.md:220-221 ("this is nondeterminism alone, not seed spread") | edited (demo 12:85): ": nondeterminism alone, not seed spread" → ", so it measures nondeterminism alone" (P3 §6); "reps" → "reruns" (class A, F5) |
| 38 | Floors are per metric, per GPU, per artifact and per run length; the table lists each one this paper uses, under its study code (key below). | CLAUDE.md:353-380; che/bench/results/phase6/m62b/m62b_report.md:128-129 | edited (demo 12:85): "per card" → "per GPU"; "with its card, run length, artifact and number of reps" → "under its study code (key below)" (class A, F5: codes keyed once here) |
| 39 | With four reruns a standard deviation has three degrees of freedom and is uncertain by about ±40 %, and the confirmatory training floors use eight. | DX-403 | edited (demo 12:85): "With four reps an sd has 3 degrees of freedom" → words; "the Phase-6 training floors" → "the confirmatory training floors" (class A, F5) |
| 40 | study / GPU / updates / artifact / reruns / floor / use | framing | edited (demo 12:87): "card" → "GPU", "reps" → "reruns" (class A, F5) |
| 41 | M5.1e / RTX 5090 / 500 / Medium, couplings locked, communication live at δ = 0 / 4 / completion 0.0145, survival 0.0129 / the Medium bars of the communication studies | DX-403; METH-1 (note: comms live at δ = 0); che/bench/results/phase5/phase5_report.md:229-230 | edited (demo 12:89): "Phase-5 bars" → "the Medium bars of the communication studies" (class A, F5) |
| 42 | M5.5 / RTX PRO 6000 / 500 / Medium, $R_{\mathrm{comm}}$ 16 / 4 / completion 0.0399, survival 0.0130 / with M5.1e, the per-GPU exhibit of §8.1; GPU, code version and configuration all differ | DX-412; METH-1 | edited (demo 12:90): "the per-hardware exhibit; card, code tree and configuration all differ" → GPU and code version (class A, F5); "of §8.1" pointer |
| 43 | M5.5, danger moments / RTX PRO 6000 / 500 / Medium / 4 / 27.2 % relative nondeterminism (sd 0.00182) / makes the 20 % third condition of the communication-denial test VOID (§8.1) | DX-412; COM-5 | edited (demo 12:91): "M5.5 danger-moment"; "voids the 20 % condition (iii)" → plain words, pointer to §8.1 |
| 44 | M5.3b / RTX PRO 6000 / 500 / High / 4 / survival 0.0621 / reference scale (cross-artifact) for the Coupling-B grid's High effect | DX-403; DX-40; CB-7; che/bench/results/e1/e11_report.md:116-121 (REFERENCE SCALE (cross-artifact)) | edited (demo 12:92): "the Phase-4 High effect" → "the Coupling-B grid's High effect" (class A, F5) |
| 45 | M6.0 / RTX PRO 6000 / n/a / per-field trajectory hashes, refactored against reference version of the code / 4 comparisons / reference version: 0 of 760 differing, in 4 of 4; refactored version against itself: 1 of 4 differing, on two diagnostic channels / the per-artifact exhibit of §8.1 | DX-5; METH-2 | edited (demo 12:93): "field digests, traced vs reference tree" → "per-field trajectory hashes, refactored against reference version of the code"; "tree" → "version" (class A, F5) |
| 46 | M6.2 / RTX PRO 6000 / 500 / ISO, JOINT / 8 / completion ISO 0.0165, JOINT 0.0093 / the registered convergence check | DX-34; DX-403; che/bench/results/phase6/m62/m62_report.md:3-5 (the plateau guard fired on these floors) | edited (demo 12:94): "plateau guard" → "the registered convergence check" (class A, F5) |
| 47 | M6.2b / RTX PRO 6000, another machine / 1000 / ISO, JOINT / 8 / completion ISO 0.0339, JOINT 0.0483 / set the design k = 40; with M6.2, floor growth 2.1× and 5.2×, length confounded with machine | DX-34; DX-403; DES-1; METH-5; docs/locks.yaml:295-300 (K_CONFIRMATORY's evidence is the M6.2b floors) | edited (demo 12:95): "another box" → "another machine", "length confounded with box" → machine (class A, F5) |
| 48 | G1.2, 2026-08-10 / RTX PRO 6000 / 1000 / ISO, JOINT, sweep arm at p = 0.5 / 8 / design-stage sd(Γ) at k = 40: 0.00504 / 0.00310 / design-stage power; drift ISO 0.56×, JOINT 1.02× its floor | DES-5; DX-403; DX-28; DES-10 | edited (demo 12:96): "G1.2 launch batch" → code only, its plain name in the key (class A, F5); "sweep endpoint" → "sweep arm at p = 0.5" |
| 49 | re-measured, 2026-09-08 / RTX PRO 6000 / 1000 / ISO, JOINT, sweep arm at p = 0.5 / 8 / the seed rule required k = 46 / the registered seed rule; drift ISO 0.80×, JOINT 0.68× | DES-2; DX-412; DX-403; DX-28; DES-10 | edited (demo 12:97): "re-floor" → "re-measured"; "k_req 46" → "the seed rule required k = 46"; "the ladder" → "the registered seed rule" (class A, F5) |
| 50 | re-measured on GPU 1 / RTX 5090 / 1000 / ISO, JOINT, sweep arm at p = 0.5 / 8 / completion ISO 0.0587, JOINT 0.0577; survival 0.0100, 0.0112 / the seed rule, which required 72 for completion and 3 for survival; the check against rerun noise; drift ISO 0.33×, JOINT 0.19× | DX-35; DX-412; DES-3; DES-10; DX-28 | edited (demo 12:98): "grid-card re-floor", "RTX 5090, unit 1" → "re-measured on GPU 1"; "k_req 72 / 3" → words; "the beat-reproducibility hurdle" → "the check against rerun noise" (class A, F5) |
| 51 | evaluation floor / RTX 5090, GPU 3 / evaluation only / two checkpoints / 4 / bit-identical, and identical to the grid's evaluations / evaluation reproducibility (§11) | HW-4; HW-2 | edited (demo 12:99): "unit 3" → "GPU 3" (class A, F5); pointer "(§11)" |
| 52 | partial re-measurement, 2026-08-14 / not recorded / n/a / ISO, JOINT / 8 ISO + 4 JOINT evaluated / none reported / provenance only; grades nothing | DX-36 | edited (demo 12:100): "partial re-floor" → "partial re-measurement" (class A, F5) |
| 53 | The floors of GPU 1 cannot be distinguished from the RTX PRO 6000's: the 95 % intervals for the standard deviation overlap (ISO completion [0.0186, 0.0571] on the RTX PRO 6000 against [0.0388, 0.1194] on the RTX 5090). | DX-35; docs/decision_log.md:4650 ("No claim is made that the 5090 is less reproducible") | edited (demo 12:102): "The grid card's floors" → "The floors of GPU 1"; "either card" → "either GPU" (class A, F5) |
| 54 | No claim is made that either GPU is less reproducible. | DX-35 (note: "No claim is made that the 5090 is less reproducible", log:4650) | edited (demo 12:102): split from the previous sentence; "either card" → "either GPU" (class A, F5) |
| 55 | The rule of §8.1 followed four bars set without floors. | V5-1; CLAUDE.md:343-351; docs/decision_log.md:1192-1198 | new here (moved from demo 08:18; class A, LEN; STRUCTURE §11 row 17) |
| 56 | The Coupling-B calibration grid graded its High survival effect against a two-seed spread of 0.0295, below the High floor of row M5.3b, and its "strong" grade was retracted (§6.4). | DX-38; CB-7; che/bench/results/phase4/phase4_report.md:603-608 (the "3σ/strong" label retracted) | moved from demo 08:18 ("M4.4 graded its High survival effect against σ_seed = 0.0295 …"): "M4.4" → "The Coupling-B calibration grid" (class A, F5); 0.0621 by pointer to the M5.3b row |
| 57 | The message-use test at Medium applied a floor hard-coded from the study of row M5.1e. | che/bench/results/phase5/phase5_report.md:830-833 ("M5.3's script hardcoded the M5.1e floor, which is Medium- and card-specific") | moved from demo 08:18 ("M5.3 graded its content ablation against a Medium floor hard-coded from an earlier run"): "M5.3" → "The message-use test at Medium" (class A, F5); never "different hardware" (OI-5) |
| 58 | Re-sited at High, it measured its floor first and found that matching Medium's resolution would take roughly 46 seeds per arm. | DX-302; che/bench/results/phase5/phase5_report.md:829-833, :917-922 | moved from demo 08:18 ("M5.3b measured its High floor first, on its own card …"): plain name (class A, F5) |
| 59 | The communication-denial test set its third condition's threshold below the rerun nondeterminism of row M5.5, danger moments. | COM-5; DX-412 | moved from demo 08:18; the numbers are in the M5.5 rows above |
| 60 | Those floor data predate the comparison, and the ruling records that a difference above the floor would have left the verdict NOT INERT standing. | decision log, Phase-5 close rulings (docs/decision_log.md:1211), item 1 (:1223-1228: "(a) the floor data pre-date the comparison … (c) the counterfactual is recorded") | moved from demo 08:18 ("The floor data predate the comparison, and had the difference exceeded the floor, the verdict as produced, NOT INERT, would have stood.") |
| 61 | In the per-artifact exhibit, both versions of the code ran on one GPU, and the two channels that differed were masking diagnostics at High severity. | METH-2 (note: the channels are `masked_frac` and `masked_danger_sum`, on severity_high seed 0); che/bench/results/phase6/m60/m60_report.md:9-11 (all GPU rows on one card) | new (STUB-SPEC APPENDIX C: the refactor exhibit's detail that §8 moved here) |
| 62 | code / plain name in the text | framing | new: the key to study codes, the one place the codes appear in prose tables (class A, F5; STUB-SPEC) |
| 63 | M3.5 (printed m35) / the Coupling-A calibration grid | DX-40 ("M3.5 (m35)"); che/bench/results/phase3/phase3_report.md:153-157 | new (class A, F5); "m35" is printed on Figure 6 |
| 64 | M4.4 (printed m44) / the Coupling-B calibration grid | DX-40 ("M4.4 (m44)"); che/bench/results/phase4/phase4_report.md:229-231 | new (class A, F5); "m44" is printed on Figure 6 |
| 65 | M5.1e / the four-run Medium floor study on an RTX 5090 | DX-403; che/bench/results/phase5/phase5_report.md:218-221 | new (class A, F5); BRIEF §5.2's example name |
| 66 | M5.3, M5.3b / the message-use test at Medium, and the same test re-sited at High with its own floor study | che/bench/results/phase5/phase5_report.md:648 ("Utility gate: does the swarm USE messages?"), :868, :829-833 | new (class A, F5) |
| 67 | M5.5 / the communication-denial test, with its Medium floor study on an RTX PRO 6000 | che/bench/results/phase5/phase5_report.md:953 ("Phase-5 acceptance: the denial element"); DX-412 | new (class A, F5) |
| 68 | M6.0 / the refactor that turned the environment configuration into data, and its rerun comparisons | che/bench/results/phase6/m60/m60_report.md:1-7 ("theta was a compile-time constant rather than data") | new (class A, F5) |
| 69 | M6.2, M6.2b / the confirmatory arms' floor studies at 500 and 1000 updates | che/bench/results/phase6/m62/m62_report.md:1, :21-23; che/bench/results/phase6/m62b/m62b_report.md:1 | new (class A, F5) |
| 70 | G1.2 / the grid's launch floor study | che/bench/results/phase6/g1/g1_2_report.md:1-5 ("the launch batch", 2026-08-10); DES-5 | new (class A, F5); class B, finding W5-F4: BRIEF §5.2's "the first floor study" misdescribes it (M5.1e, M6.2 and M6.2b came earlier), so the key says "the grid's launch floor study" |

## Alternates

None.

## Open items

- **W5-F4 (class B, applied here).** BRIEF §5.2 names the launch batch "the first floor
  study (2026-08-10)". It was not the first floor study: M5.1e (Medium), M6.2 and M6.2b
  (the confirmatory arms, at 500 and 1000 updates) came before it (DX-403, DX-34). The key
  calls G1.2 "the grid's launch floor study". W6's §9.1 uses the glossary's name
  (`09_compositional_test.md:56`). Direction: the orchestrator picks one accurate name for
  both files.
- **Evaluation draw row (accuracy).** The draw is registered with the grid layout
  (`phase6_framing_branches.md:264-267`) but has no entry in `docs/locks.yaml`, so the row
  says so; the opening sentence speaks of locked constants only. z_α also has no
  registry entry: it follows from `SIDAK_M` = 2 (DES-13).
- **Exhibits moved from §8.** The four floor-less bars (DX-38, CB-7, DX-302, the M5.3
  hard-coded floor) and the M5.5 counterfactual (log:1223-1228) are here, as STRUCTURE §11
  row 17 directs; §8.1 points here.
- **Codes.** Study codes appear only in this appendix (the floors table and its key) and on
  the figures that print them (Figures 6 and 10); the key covers every code printed there.
  M3.0, M3.3, M3.4, M4.2 and M5.2 are not keyed: no v2 file I can see prints them; if
  another writer's section or quotation keeps one, add a key row.
- **"Not locked" row.** σ_s, η and ι are held by convention, never calibrated (DX-1); the
  row keeps the demo's wording.
- **Budget.** 313 prose words across Appendices B and C against about 350, plus the five
  tables.

Nothing in the file is unsourced.
