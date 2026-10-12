<!-- PAPER V2 DRAFT (PAPER V2 ruling, 2026-10-11): builder-drafted, not owner-approved -->

### B Locks and hyperparameters

<!-- STUB-SPEC
PURPOSE: Appendix B: every locked constant with its value, ruling date and record, then the training hyperparameters and the budget. Appendix C: every reproducibility floor the paper uses, with its GPU, run length, artifact and number of identical reruns, and the key to the study codes (the one place the codes appear, F5). These files continue the appendix after W6's Appendix A; they open with an H3 by design (STRUCTURE.md section 13).
WRITER: W5 (moved from W6 for load and because Appendix C holds the exhibits of section 8: STRUCTURE.md section 10). BUDGET: about 350 prose words across both, plus the tables.
APPENDIX B REQUIRED FACTS: the environment locks (CAL-1 with its O-2 caveat: the lock record's value, the committed estimators beside it; CAL-3; CA-1; CB-1; COM-6; ENV-1; DX-401 for every ruling date and for the weak-floor smoothing passes and the observation version; DX-1 for σ_s, η, ι, not locked, held by convention); the analysis constants (DES-1, DES-3, DES-13, DES-4 for the 0.03 band, DX-402 for every date, METH-6 for the retired convergence check's constants, which grade nothing); the hyperparameters (DX-2: learning rate 3e-4 constant; γ 0.99; GAE λ 0.95; clip 0.2; entropy 0.01; value 0.5; gradient-norm clip 0.5; Adam ε 1e-5; 256 environments; 128 steps; 4 minibatches; 4 epochs; checkpoint every 50 updates) and the budget (DX-3). The demo's tables (sections/12_appendix.md:39-81) are the template; keep code identifiers such as K_CONFIRMATORY only as table labels, with a plain description beside each.
APPENDIX C REQUIRED FACTS: each floor row of the demo's table (sections/12_appendix.md:83-102) with its IDs: METH-1, DX-403, DX-412, COM-5, CB-7, DX-40, METH-2, DX-5, DX-34, METH-5, DES-1, DES-5, DES-2, DES-10, DX-35, DES-3, HW-2, HW-4, DX-36; the ±40 % uncertainty of a four-run floor (DX-403 or DX-303); the overlap of the RTX 5090 and RTX PRO 6000 intervals and that no claim is made that either GPU is less reproducible (DX-35). Add a key mapping each study code to its plain name as sections 5 to 9 use it (for example, the four-run Medium floor study on an RTX 5090, the Coupling-B calibration grid); add, in one or two sentences each, the exhibit details section 8 moved here (the refactor exhibit's two code versions; the run-length exhibit's two machines).
FIGURES, LISTINGS, LATEX: none; tables only (no pipes inside math in a cell).
HONESTY LINES AND REGISTERED STRINGS: "reference scale (cross-artifact)" for the High floor's use beside the Coupling-B grid; floors are per metric, per GPU and per artifact; the partial re-measurement of 2026-08-14 is provenance only and grades nothing.
FIX-LIST AND FINDINGS ITEMS OWNED: F5 (the key; "card" to GPU; "unit" to GPU n; "rep" to identical rerun; launch batch to "the first floor study"; G1.2 named in plain words); LEN (the demo's App. C ratios paragraph already moved; keep it to the table and the key); OI-5 (never "different hardware" for M5.3's floor); Q20.
DEMO KEEPS (sections/12_appendix.md:39-102): both lock tables, the hyperparameter table, the floors table and the overlap sentence. CHANGES: jargon to plain names with the key; GPU naming. DROPS: nothing.
NOT HERE: GPU addresses or UUIDs; commit hashes; any number not in the ledger or the supplement.
-->

Each locked constant below was fixed by a ruling on the date given, and the test described in §11 checks each against the configurations, the code defaults or the analysis scripts.

| constant | value | ruled | record |
|---|---|---|---|
| critical point $\hat\beta_c$ | 0.500 ± 0.005<!-- N:CAL-1 --> | 2026-07-19<!-- N:DX-401 --> | severity lock record; no committed script reproduces its estimator, and the committed estimators give a crossing mean of 0.504 and a consensus of 0.499<!-- N:CAL-1 --> |
| β Low / Medium / High | 0.43 / 0.49 / 0.70<!-- N:CAL-3 --> | 2026-07-19<!-- N:DX-401 --> | severity lock record |
| β held out (θ\*) | 0.49<!-- N:CAL-3 --> | 2026-08-02<!-- N:DX-401 --> | the ruling that sited θ\*: train at the two extremes and hold out the middle |
| $f_{\mathrm{weak}}$, $\lambda_0$, $\lambda_{\mathrm{load}}$, $\kappa_A$, $r_A$ | 0.15, 5e-5, 4e-4, 0.06, 1<!-- N:CA-1 --> | 2026-07-21<!-- N:DX-401 --> | Coupling-A lock record |
| weak-floor smoothing passes | 2<!-- N:DX-401 --> | 2026-07-21<!-- N:DX-401 --> | Coupling-A lock record, locked as the code default |
| $\kappa_B$ | 1.0<!-- N:CB-1 --> | 2026-07-27<!-- N:DX-401 --> | Coupling-B lock record, on the detection band alone |
| δ off / on; $R_{\mathrm{comm}}$ | 0.0 / 1.0<!-- N:DX-401 -->; 16<!-- N:COM-6 --> | 2026-07-30<!-- N:DX-401 --> | communication lock record |
| death penalty $d_p$ | 0.5<!-- N:ENV-1 --> | 2026-07-19<!-- N:DX-401 --> | the death-penalty design decision |
| observation encoding | 3<!-- N:DX-401 -->, the masking observation (§3) | 2026-07-24<!-- N:DX-401 --> | the observation design decision |
| $\sigma_s$, η, ι | 1.0, 0.5, 0.0<!-- N:DX-1 --> | not locked | held fixed by convention, never calibrated |

| analysis constant | value | ruled | role |
|---|---|---|---|
| `K_CONFIRMATORY` | 40<!-- N:DES-1 --> | 2026-08-03<!-- N:DX-402 --> | the design seed count per confirmatory arm, against which the registered seed rule computes |
| `K_LADDER_CAP` | 60<!-- N:DES-1 --> | 2026-08-03<!-- N:DX-402 --> | the seed rule's cap |
| `K_CONFIRMATORY_REALIZED` | 72<!-- N:DES-3 --> | 2026-09-22<!-- N:DX-402 --> | the seed count at which Γ is read, a recorded deviation (§9.1) |
| `K_SECONDARY` | 20<!-- N:DES-13 --> | 2026-08-02<!-- N:DX-402 --> | seeds per secondary arm; ISO-4 uses the same count |
| `SIDAK_M`; $z_\alpha$ | 2; 2.2365<!-- N:DES-13 --> | 2026-08-02<!-- N:DX-402 --> | the confirmatory family: the two co-primary tests, Šidák-corrected |
| `POWER_STOP` | 0.80<!-- N:DX-402 --> | 2026-08-02<!-- N:DX-402 --> | the minimum design-stage power at the 0.03<!-- N:DES-4 --> band |
| `T_STAR` | 1000<!-- N:DES-13 --> | 2026-08-11<!-- N:DX-402 --> | the fixed training budget in updates, a value unchanged since 2026-08-03<!-- N:DX-402 --> |
| `GAMMA_T_RETENTION` | 11<!-- N:DES-13 --> | 2026-08-11<!-- N:DX-402 --> | checkpoints kept for Γ(t): updates 500–1000 every 50<!-- N:DES-13 --> |
| evaluation draw | seed 0 × 512 episodes<!-- N:DES-13 --> | registered with the grid layout | common to every run; not in the lock registry |
| `PLATEAU_PASS`; `PLATEAU_REVIEW` | 1.0; 1.5<!-- N:DX-402 --> | 2026-08-02<!-- N:DX-402 --> | thresholds of the registered convergence check, retired as a gate on 2026-08-11<!-- N:METH-6 -->; they grade nothing |

The training hyperparameters are identical for every run of §9; the grid passes none on the command line, so the configured defaults apply.

| hyperparameter | value |
|---|---|
| learning rate | 3e-4, constant, no schedule<!-- N:DX-2 --> |
| discount γ; GAE λ | 0.99; 0.95<!-- N:DX-2 --> |
| PPO clip ε | 0.2<!-- N:DX-2 --> |
| entropy coefficient; value coefficient | 0.01; 0.5<!-- N:DX-2 --> |
| global gradient-norm clip; Adam ε | 0.5; 1e-5<!-- N:DX-2 --> |
| parallel environments; steps per update | 256; 128<!-- N:DX-2 --> |
| minibatches; epochs | 4; 4<!-- N:DX-2 --> |
| checkpoint interval | 50 updates<!-- N:DX-2 --> |
| budget | 32,768 environment steps per update, 32,768,000 per run<!-- N:DX-3 --> |

### C Floors

A floor is the standard deviation of a metric over identical reruns at one seed, so it measures nondeterminism alone. Floors are per metric, per GPU, per artifact and per run length; the table lists each one this paper uses, under its study code (key below). With four reruns a standard deviation has three degrees of freedom and is uncertain by about ±40 %<!-- N:DX-403 -->, and the confirmatory training floors use eight<!-- N:DX-403 -->.

| study | GPU | updates | artifact | reruns | floor | use |
|---|---|---|---|---|---|---|
| M5.1e | RTX 5090<!-- N:DX-403 --> | 500<!-- N:DX-403 --> | Medium, couplings locked, communication live at δ = 0<!-- N:METH-1 --> | 4<!-- N:DX-403 --> | completion 0.0145, survival 0.0129<!-- N:METH-1 --> | the Medium bars of the communication studies |
| M5.5 | RTX PRO 6000<!-- N:DX-412 --> | 500<!-- N:DX-412 --> | Medium, $R_{\mathrm{comm}}$ 16<!-- N:METH-1 --> | 4<!-- N:DX-412 --> | completion 0.0399, survival 0.0130<!-- N:METH-1 --> | with M5.1e, the per-GPU exhibit of §8.1; GPU, code version and configuration all differ |
| M5.5, danger moments | RTX PRO 6000<!-- N:DX-412 --> | 500<!-- N:DX-412 --> | Medium | 4<!-- N:DX-412 --> | 27.2 % relative nondeterminism (sd 0.00182)<!-- N:COM-5 --> | makes the 20 %<!-- N:COM-5 --> third condition of the communication-denial test VOID (§8.1) |
| M5.3b | RTX PRO 6000<!-- N:DX-403 --> | 500<!-- N:DX-40 --> | High | 4<!-- N:DX-40 --> | survival 0.0621<!-- N:CB-7 --> | reference scale (cross-artifact) for the Coupling-B grid's High effect |
| M6.0 | RTX PRO 6000<!-- N:DX-5 --> | n/a | per-field trajectory hashes, refactored against reference version of the code | 4 comparisons<!-- N:METH-2 --> | reference version: 0 of 760 differing, in 4 of 4; refactored version against itself: 1 of 4 differing, on two diagnostic channels<!-- N:METH-2 --> | the per-artifact exhibit of §8.1 |
| M6.2 | RTX PRO 6000<!-- N:DX-34 --> | 500<!-- N:DX-34 --> | ISO, JOINT | 8<!-- N:DX-403 --> | completion ISO 0.0165, JOINT 0.0093<!-- N:DX-34 --> | the registered convergence check |
| M6.2b | RTX PRO 6000, another machine<!-- N:DX-34 --> | 1000<!-- N:DX-34 --> | ISO, JOINT | 8<!-- N:DX-403 --> | completion ISO 0.0339, JOINT 0.0483<!-- N:DX-34 --> | set the design k = 40<!-- N:DES-1 -->; with M6.2, floor growth 2.1× and 5.2×<!-- N:METH-5 -->, length confounded with machine |
| G1.2, 2026-08-10<!-- N:DES-5 --> | RTX PRO 6000<!-- N:DES-5 --> | 1000<!-- N:DX-403 --> | ISO, JOINT, sweep arm at p = 0.5<!-- N:DX-28 --> | 8<!-- N:DX-403 --> | design-stage sd(Γ) at k = 40: 0.00504 / 0.00310<!-- N:DES-5 --> | design-stage power; drift ISO 0.56×, JOINT 1.02× its floor<!-- N:DES-10 --> |
| re-measured, 2026-09-08<!-- N:DES-2 --> | RTX PRO 6000<!-- N:DES-2 --> | 1000<!-- N:DX-412 --> | ISO, JOINT, sweep arm at p = 0.5<!-- N:DX-28 --> | 8<!-- N:DX-403 --> | the seed rule required k = 46<!-- N:DES-2 --> | the registered seed rule; drift ISO 0.80×, JOINT 0.68×<!-- N:DES-10 --> |
| re-measured on GPU 1 | RTX 5090<!-- N:DX-35 --> | 1000<!-- N:DX-412 --> | ISO, JOINT, sweep arm at p = 0.5<!-- N:DX-28 --> | 8<!-- N:DX-35 --> | completion ISO 0.0587, JOINT 0.0577; survival 0.0100, 0.0112<!-- N:DX-35 --> | the seed rule, which required 72 for completion and 3 for survival<!-- N:DES-3 -->; the check against rerun noise; drift ISO 0.33×, JOINT 0.19×<!-- N:DES-10 --> |
| evaluation floor | RTX 5090, GPU 3<!-- N:HW-4 --> | evaluation only | two checkpoints<!-- N:HW-2 --> | 4<!-- N:HW-2 --> | bit-identical, and identical to the grid's evaluations<!-- N:HW-2 --> | evaluation reproducibility (§11) |
| partial re-measurement, 2026-08-14<!-- N:DX-36 --> | not recorded<!-- N:DX-36 --> | n/a | ISO, JOINT | 8 ISO + 4 JOINT evaluated<!-- N:DX-36 --> | none reported | provenance only; grades nothing |

The floors of GPU 1 cannot be distinguished from the RTX PRO 6000's: the 95 %<!-- N:DX-35 --> intervals for the standard deviation overlap (ISO completion [0.0186, 0.0571] on the RTX PRO 6000 against [0.0388, 0.1194] on the RTX 5090<!-- N:DX-35 -->). No claim is made that either GPU is less reproducible.

The rule of §8.1 followed four<!-- N:V5-1 --> bars set without floors. The Coupling-B calibration grid graded its High survival effect against a two-seed spread of 0.0295<!-- N:DX-38 -->, below the High floor of row M5.3b, and its "strong" grade was retracted (§6.4). The message-use test at Medium applied a floor hard-coded from the study of row M5.1e. Re-sited at High, it measured its floor first and found that matching Medium's resolution would take roughly 46<!-- N:DX-302 --> seeds per arm. The communication-denial test set its third condition's threshold below the rerun nondeterminism of row M5.5, danger moments. Those floor data predate the comparison, and the ruling records that a difference above the floor would have left the verdict NOT INERT standing. In the per-artifact exhibit, both versions of the code ran on one GPU, and the two<!-- N:METH-2 --> channels that differed were masking diagnostics at High severity.

| code | plain name in the text |
|---|---|
| M3.5 (printed m35) | the Coupling-A calibration grid |
| M4.4 (printed m44) | the Coupling-B calibration grid |
| M5.1e | the four-run<!-- N:DX-403 --> Medium floor study on an RTX 5090 |
| M5.3, M5.3b | the message-use test at Medium, and the same test re-sited at High with its own floor study |
| M5.5 | the communication-denial test, with its Medium floor study on an RTX PRO 6000 |
| M6.0 | the refactor that turned the environment configuration into data, and its rerun comparisons |
| M6.2, M6.2b | the confirmatory arms' floor studies at 500 and 1000<!-- N:DX-34 --> updates |
| G1.2 | the grid's launch floor study |
