# Numbers ledger

Built 2026-09-27, before any number is ported into `submission.md`
(`HANDOFF.md` item 3; numbers-enter-derived sub-rule, 2026-07-28). **Every
number the paper states has a row here, and every row names the committed
artifact that measured or ruled it.** Each row was checked this session
against its source. Nothing was recomputed. **DERIVED** rows show the
arithmetic from verified rows.

**How to use it.** A number enters `submission.md` only with a row ID beside
it (as an HTML comment, `<!-- N:RES-2 -->`, which does not render). A new
number gets its row first. Where a row and its source disagree, the source
wins. Where a source and `docs/decision_log.md` disagree, the log wins. Lock
values also live in `docs/locks.yaml`, which `test_locks.py` enforces.

**Status:** **OK**: the source says this. **OK≈**: the same value after
rounding. **DERIVED**: arithmetic shown. **FIXED**: the spine was wrong,
was corrected in the same commit as this ledger, and the row carries the
right value. **OPEN**: needs an artifact or an owner decision before it
ships (collected in the last section).

Paths: `R/` = `che/bench/results/`; `log` = `docs/decision_log.md`.

---

## ENV — the environment as instantiated

| ID | value | what | source | status / note |
|---|---|---|---|---|
| ENV-1 | d_p = 0.5 | death penalty per newly disabled agent (D4) | `docs/locks.yaml:223-228`; log:23 | OK. `che/env/config.py:37` defaults to 0.0; every live config carries 0.5 |
| ENV-2 | High survival 0.575 → 0.866 | d_p 0 → 0.5 ablation, M2.5 | `R/phase2/phase2_report.md:44-48`; scope :27, :30 | OK. Pillar-only, 500 updates, 3 seeds; ± = half the min–max range. **tex todo** `03_environment.tex:87-88` |
| ENV-3 | High completion 0.765 → 0.821 | same ablation | same | OK. **tex todo** `03_environment.tex:88-89` |
| ENV-4 | Medium survival 0.931 → 0.951; completion 0.750 at both | same ablation | same | OK |
| ENV-5 | Low tied (0.991 vs 0.992) | same ablation | `phase2_report.md:41-42, :63` | OK |
| ENV-6 | 64 × 64 grid, 12 agents, horizon 256, 9 × 9 crop, 32 food items | instance | `che/configs/p6_joint.yaml:11-16` | OK |
| ENV-7 | 8 observation channels: 6 content indicators, smoke, visibility; own-state (row/L, col/L, alive, t/horizon) | observation | `che/env/observation.py:22-33, :56, :73` | OK. "7 indicator planes plus smoke" is right; the spine now also names the alive flag |
| ENV-8 | 5 actions | action set | `che/env/env.py:48` | OK |
| ENV-9 | +1 team reward per collected item | task reward | `che/env/tasks.py:32-34` | OK |
| ENV-10 | Conv 16 → Conv 32 → Dense 128 → actor/critic heads with a 64-unit hidden layer each; message head | network | `che/train/networks.py:87-110` | FIXED. The spine omitted the head layers and the message path |
| ENV-11 | one shared-parameter IPPO policy per training seed | how every reported run trained | `che/scripts/run_p6_grid.sh:299` and every science `run_*.sh` (`che.train.ippo`) | **FIXED**, and **OPEN (O-1)**. The spine said "PBT population 12", but `pop_size: 12` exists only in the throughput config `gate_pop12.yaml:98`, run by `che.train.pbt --bench` (`run_m51d_*`, `run_m51i_*`). No reported result used PBT |
| ENV-12 | message head: zero gradient, frozen-at-init projection of **trained** trunk features | comms encoder | `che/train/networks.py:31-36`; `che/train/ippo.py:327` (`stop_gradient`); `R/phase5/phase5_report.md:61-63` | OK. Receivers' weights on the message inputs *are* trained |

## CAL — severity calibration (Phase 2)

| ID | value | what | source | status / note |
|---|---|---|---|---|
| CAL-1 | β̂_c = 0.500 ± 0.005; R_L logistic centres 0.4985 / 0.5006 / 0.4999 at L = 32 / 48 / 64 | critical point | `severity_lock.md:7, :11`; `docs/locks.yaml:46-57` | OK against the lock record, which says the RA recomputed it (:5). **OPEN (O-2):** no committed script or artifact produces the R_L logistic centres. `R/phase2/estimates.json` and `calibration_report.md:20, :34-36` use other estimators (crossing mean 0.504, consensus 0.499). The raw data is committed (`calibration_crossing.npz`) |
| CAL-2 | R_L(0.500) = 0.488 / 0.502 / 0.494 | self-duality check | `severity_lock.md:16` | OK, with the same provenance caveat as CAL-1 |
| CAL-3 | Low β 0.43: P_span 0.021, burnt 1.9 %; Medium 0.49: 0.547, 19.8 %; High 0.70: 0.998, 98.3 % | locked levels | `R/phase2/calibration_report.md:107-109`; `severity_lock.md:29-31` | OK. Cross-check: `R/phase3/def4_variance.md` burnt fraction 0.0185 / 0.1981 / 0.9830 |
| CAL-4 | β_c(64) ≈ 0.486 | finite-size pseudo-critical point (P_span = ½ at L = 64) | `R/phase2/estimates.json:10`; `calibration_report.md:32` | OK≈ (0.48607) |
| CAL-5 | Def. 4 variance peak at Medium: **refuted for survival** (fixed-policy variance 0.00091 / 0.00709 / 0.00885, High highest); completion inconclusive; env-level mechanism confirmed | Def.-4 re-test | `R/phase3/def4_variance.md:106-108` (table :43-61); `R/phase3/phase3_report.md:4-6` | **FIXED**: the re-test is **M3.0**, not M3.5, and the refutation is scoped to survival |

## CA — Coupling A (Phase 3, E1.1)

| ID | value | what | source | status / note |
|---|---|---|---|---|
| CA-1 | (f_weak, λ₀, λ_load, κ_A, r_A) = (0.15, 5e-5, 4e-4, 0.06, 1) | lock | `coupling_a_lock.md:77`; `docs/locks.yaml:114-148` | OK. r_A is `r_seed` in code |
| CA-2 | R² 0.998 over a 14× range of E[N_seeds] | Prop. 3 linearity | `R/phase3/phase3_report.md:113-114`; `R/phase3/m33/prop3_L64.json:45` | OK. **L = 64 dense sweep, κ_A 0.02, f_weak 0.4**, not the locked parameters |
| CA-3 | matched-reference ratio 0.992 ∈ [0.90, 1.02], R² 0.9995 | Prop. 3 handshake | `phase3_report.md:144-145` | OK. **v2 purified L = 32 CPU test, κ_A 0.003**, a different run from CA-2 (report text only, no JSON). **FIXED**: the spine had merged CA-2 and CA-3 into one run |
| CA-4 | seeded ignitions/episode 4.05 / 3.41 / 0.84, a 4.83× fall | the self-limiting finding | `R/e1/e11_report.md:54` (data `R/e1/severity/severity.json`) | OK. **m44, κ_B = 1.0 arm**. 4.0527 / 0.8398 = 4.83 (from the rounded inputs, 4.82). **FIXED**: the spine now attributes it to m44 |
| CA-5 | m35 replication: 4.08 / 3.42 / 0.83, 4.92× | same, on the Coupling-A grid | `phase3_report.md:188, :196, :204` | OK. 4.075 / 0.828 = 4.92 |
| CA-6 | near-agent share in [0.164, 0.203] | flat across severity | `R/e1/e11_report.md:61` | OK. 9 cells: m44 × 6 and m35 × 3 |
| CA-7 | Low survival 0.979 → 0.961; no weak-cell avoidance | κ_A off → on at Low, M3.5 | `phase3_report.md:184, :225, :241` | OK. 2 seeds per arm. Weak occupancy is actually *higher* under κ_A (+0.054) |

## CB — Coupling B (Phase 4)

| ID | value | what | source | status / note |
|---|---|---|---|---|
| CB-1 | κ_B = 1.0, locked on the detection band alone | lock | `kappa_b_lock.md:415`; `docs/locks.yaml:161-166` | OK |
| CB-2 | detection and E2C bands disjoint by 1.35× (random policy); 1.15× under the probe policies | why the bands did not intersect | `kappa_b_lock.md:187, :150-151`; `:262-265` | OK. **FIXED**: the spine now names the policy |
| CB-3 | masked-frac band unreachable at any κ_B | same | `kappa_b_lock.md:149` | OK |
| CB-4 | E2C gate: max \|z\| 2.11; Σz² 6.55 on 8 dof, p = 0.586; mean z −0.44 | Thm. 1 | `R/phase4/phase4_report.md:85-87, :104-105` | OK. Report only (`m42/e2c_sweep.json` stores no gate statistics) |
| CB-5 | High survival: direction 3/3, range −0.047 to −0.107, pooled 1.41× the floor | Coupling-B effect, as corrected 2026-07-30 | `phase4_report.md:596-601`; replicate deltas `R/phase5/pretask/replicate_deltas.txt` | OK. **FIXED**: the spine led with the pre-correction figure (CB-6) |
| CB-6 | −8.8 points (−0.08765) | the first 2-seed M4.4 estimate | `phase4_report.md:315`; `R/phase4/m44/m44_analysis.json:378` | OK as a historical figure. Quote only beside CB-5. The registered §4a text (`phase6_framing_branches.md` §4a) uses "8.8-point" |
| CB-7 | High survival floor sd 0.062 | reproducibility floor | `R/phase5/m53b/reproducibility_floor_high.txt:7` | OK≈ (0.0621) |
| CB-8 | completion effect sign flip on a same-seed retrain, unresolved | High completion | `phase4_report.md:627, :641-642` | OK |
| CB-9 | Medium survival −0.0003, "within noise" | Coupling B's own effect at θ\*'s severity | `phase4_report.md:313`; `m44_analysis.json:214` | OK. 3 seeds per arm, graded against a 3-seed σ_seed of 0.0072, **not** a measured floor. The later Medium floor is 0.0129 (METH-1) |
| CB-10 | masking 16–118× concentrated on danger moments | the not-suppressible finding | `phase4_report.md:591, :362-364`; `m44_analysis.json:587, :599, :611` | OK≈ (15.55 / 22.47 / 118.31; κ_B = 1.0 rows) |

## CO — the co-active counter (invariant #5)

| ID | value | what | source | status / note |
|---|---|---|---|---|
| CO-1 | 0.64 events/episode at Medium | mean | `phase4_report.md:425`; `R/e1/e11_report.md:209` | OK≈ (0.6426). m44 κ_B = 1.0 arm; the κ_B = 0 arm reads 0.564 |
| CO-2 | P(zero) = 0.563 / 0.578 / 0.883 | Low / Medium / High | `phase4_report.md:423-427`; `e11_report.md:208-210` | OK. m44 κ_B = 1.0, pooled over seeds (1024 / 1536 / 1024 episodes) |
| CO-3 | var/mean 1.31–1.40 | over-dispersion | `R/e1/e11_report.md:208-210` | OK. **FIXED**: this is E1.1, not Phase-4 Result 4. E1.1's own range is 1.31–1.44 because it adds an m55 δ = 0 row |
| CO-4 | counter = collapse-seeded ignitions inside an alive agent's crop (Chebyshev radius obs_window // 2) | definition | `che/env/env.py:398-404` | OK |

## COM — the comms axis (Phase 5)

| ID | value | what | source | status / note |
|---|---|---|---|---|
| COM-1 | VoC monotone 0 → 0.498 | Remark 2′ handshake | `R/phase5/phase5_report.md:558`; `R/phase5/m52/e2c2_sweep.json:1059` | OK≈ (0.4982, VoC_gated) |
| COM-2 | M5.3 Medium: no effect larger than ~3 points (2 seeds) | utility bound | `phase5_report.md:914, :659, :685`; `comms_lock.md:38` | OK. Bar = 2 × the M5.1e floor; R_comm 8, δ = 0 |
| COM-3 | M5.3b High: alive out-degree 1.01 → 2.99 changed nothing | connectivity eliminated | `phase5_report.md:891-904` | OK. `R/phase5/m53b/verdict.txt:18, :31` prints 1.013 / 2.981 (third-decimal disagreement between two artifacts) |
| COM-4 | M5.5: Δcompletion +0.0038 vs bar 0.0799; Δsurvival −0.0143 vs bar 0.0260 | δ = 1 vs 0 within floors | `phase5_report.md:979-980` | OK. Medium, 4 seeds, R_comm 16 |
| COM-5 | condition (iii) VOID: 20 % threshold vs a measured 27.2 % nondeterminism (sd 0.00182); observed 23.2 % | the methods exhibit | `phase5_report.md:991-995`; log:1170-1175 | OK. The report calls the 20 % "registered", the log "a threshold the RA chose" |
| COM-6 | δ = 1.0, R_comm = 16 | locks | `docs/locks.yaml:188-192, :202-206`; `comms_lock.md:12-13` | OK |

## METH — methodology exhibits (§8)

| ID | value | what | source | status / note |
|---|---|---|---|---|
| METH-1 | Medium completion floor 0.0145 → 0.0399 (2.75×); survival 0.0129 → 0.0130 | floors are per-hardware | `R/phase5/phase5_report.md:1014-1015`; raw `R/phase5/m51e/reproducibility_floor.txt:6-7`, `R/phase5/m55/reproducibility_floor_medium.txt:7-8` | OK. 0.039938 / 0.014541 = 2.747. **Caveat now in the spine:** the two runs also used different code trees (M5.1e `fa32113`, M5.5 `1c1ce76`), so card is confounded with tree. **tex todos** `08_methodology.tex:15-17` (four values) |
| METH-2 | traced tree differs from itself 1 time in 4 on 2 channels; reference floor 0 of 760 digests in 4 of 4 | floors are per-artifact | `R/phase6/m60/m60_report.md:69-71, :90-91, :109-110` | OK. The channels are `masked_frac` and `masked_danger_sum`, on severity_high seed 0; no trajectory field differed |
| METH-3 | per-arm reads 92.1 % / 62.8 %, contrast 76.7 % | the contrast-SE exhibit | `R/phase6/m62b/m62b_report.md:175-177`; log:2176-2178 | OK. k = 34. The same report prints 92.2 % at :111 ("one number, rounded two ways"). **tex todos** `08_methodology.tex:31-32` |
| METH-4 | k = 20 on a bare 2σ figure: 55.6 % power | the 80 %-power-MDE exhibit | `phase6_design_v2.md:196, :209-210`; log:1795, :1801-1805 | OK. A design calculation (σ 0.0399, Šidák m = 2). **tex todo** `08_methodology.tex:40` |
| METH-5 | completion floor growth T = 500 → 1000: ISO 2.1×, JOINT 5.2× | floors grow with run length | `R/phase6/m62b/m62b_report.md:134-135`; T = 500 values `R/phase6/m62/floors.json` | OK≈ (2.056×, 5.189×). **FIXED**: "ordered by curriculum difficulty" is labelled at :137 as a hypothesis not tested here (n = 2 arms). M6.2 and M6.2b ran on different PRO 6000 boxes, so length is confounded with box. **tex todos** `08_methodology.tex:79-80` |
| METH-6 | plateau criterion retired; fixed-budget estimand | T\* RULING, **2026-08-11** | defect `R/phase6/g1/g1_2_report.md:51-54`; ruling log:2940-2978 | OK |

## DES — Phase-6 design

| ID | value | what | source | status / note |
|---|---|---|---|---|
| DES-1 | registered k = 40; K_LADDER_CAP 60 | design constants | log:4765 (UNBLIND INSTRUMENT entry); `docs/locks.yaml` | OK |
| DES-2 | k = 46 | seed ladder, re-floor **run 2026-09-08**, logged 2026-09-09 (RTX PRO 6000) | log:3840, :3872-3876; `R/phase6/g1_floors_2026-09-08/verdict.txt:44, :50` | OK. **FIXED**: the spine said "the 2026-09-09 re-floor" |
| DES-3 | k_req 72 (completion), 3 (survival) on the 5090 re-floor; cap raised 60 → 72, 2026-09-22 | ladder branch C, recorded deviation | log:4616-4623 | OK |
| DES-4 | 5090-floor completion power at 0.03: 72.2 % (k = 60), 80.4 % (k = 72) | design-stage power, grid card | log:4643 | OK |
| DES-5 | launch batch (PRO 6000, 2026-08-10), k = 40: sd(Γ) 0.00504 / 0.00310, MDE80 0.0155 / 0.0095, k_req 11 / 5 | design-stage power | `R/phase6/g1/g1_2_report.md:83-88`; raw `R/phase6/g1_floors/verdict.txt:44-45` | OK. The agent's hand check: √((0.021417² + 0.023631²)/40) = 0.00504; × 3.0781 = 0.0155 |
| DES-6 | realized completion power at 0.03: 71.6 % (k = 72), 60.2 % (k = 60) | realized power | `R/phase6/unblind/report.md:11, :21` | OK |
| DES-7 | ISO per-element marginals A 0.3333 / B 0.3333; JOINT 1.0 / 1.0, a 3× ratio | endpoint confound | log:4562-4563; `che/configs/p6_iso.yaml:7` | OK |
| DES-8 | ISO behavioural fire-only share 1/3 (2 of 6 components δ-only) | inert-share bias | `che/configs/p6_iso.yaml:7-12, :43, :46`; log:3970-3985 | OK |
| DES-9 | sweep: m = 0.5, n = p; identification: m = 0.4, n = 0.2 + p | secondary arm geometry | `R/phase6/secondary/secondary.md:7-16` | OK |
| DES-10 | drift over the last 100 updates, JOINT − ISO (completion), floor-graded. **Launch batch (PRO 6000):** ISO +0.01202 (0.56×), JOINT +0.02411 (1.02×), differential +0.01209. **2026-09-08 (PRO 6000):** ISO 0.80×, JOINT 0.68×, differential +0.0179. **5090 grid card:** ISO +0.0192 (0.33×), JOINT +0.0109 (0.19×), differential **−0.0083** | bias (b) | `R/phase6/g1/g1_2_report.md:28-29`; `R/phase6/g1_floors_2026-09-08/verdict.txt:32-33`; `R/phase6/g1_floors_5090/verdict.txt:32-33` | **FIXED**: the spine quoted only the launch batch as if it held generally. **The sign reverses on the grid card.** Differentials DERIVED: 0.02411 − 0.01202, 0.0405 − 0.0226, 0.0109 − 0.0192 |
| DES-11 | training-surface slope JOINT − ISO per 100 updates over (500, 1000]: completion +0.00247, survival +0.00718 | the same drift, from the T = 2000 subsample (grid-card model) | `R/phase6/post_unblind_analysis/post_gamma4_t2000.md:30-33` | OK. Descriptive, 4 seeds, a different estimator from DES-10 |
| DES-13 | Šidák m = 2, z_α = 2.2365; T\* = 1000; Γ(t) at 11 checkpoints, updates 500–1000 every 50; K_SECONDARY = 20 (ISO-4 also k = 20); K_CONFIRMATORY_REALIZED = 72; eval draw seed 0 × 512 episodes, common to every run | registered analysis constants | `docs/locks.yaml:295-458` (SIDAK_M :405, T_STAR :458, GAMMA_T_RETENTION :342, K_SECONDARY :373, K_CONFIRMATORY_REALIZED :323); z_α and the eval draw: `R/phase6/unblind/report.md:5`, `phase6_framing_branches.md` §4b | OK |
| DES-12 | branches registered 2026-08-13; venue ruled 2026-08-24; co-primary ruled 2026-08-02; grid 2026-09-09 → 09-22; unblind 2026-09-26 | registration dates | `phase6_framing_branches.md:3`; log:3686; log:1655, :1691-1694; `R/phase6/phase6_report.md:70, :75` | OK. The earlier NeurIPS D&B venue ruling (2026-08-16) was superseded on 2026-08-24; both are pre-grid |

## RES — Phase-6 confirmatory result (θ\*, T = 1000)

| ID | value | what | source | status / note |
|---|---|---|---|---|
| RES-1 | Γ completion −0.0173, z −1.62, Šidák CI [−0.0412, +0.0066], X 0.0329 | k = 72 | `R/phase6/unblind/report.md:11` | OK. The abstract's "no gain larger than 0.66 points" and §9.2's "−1.7 points" are this row |
| RES-2 | Γ survival +0.0096, z +4.43, p 9.3e−6, Šidák CI [+0.0047, +0.0144] | k = 72 | `unblind/report.md:12` | OK. The abstract's "0.96 points, [0.47, 1.44]" |
| RES-3 | k = 60: completion −0.0217 (z −1.80); survival +0.0104 (z +4.67) | registered-ladder prefix | `unblind/report.md:21-22` | OK |
| RES-4 | arm means: completion ISO 0.7772, JOINT 0.7600; survival ISO 0.9158, JOINT 0.9254 | k = 72 | `unblind/report.md:11-12` | OK |
| RES-5 | falsifier 3.855 < 4.433 (k = 60: 4.040 < 4.673) | branch B, not C | `unblind/report.md:15, :25` | OK. DERIVED check: 1.618 + 2.2365 = 3.855 |
| RES-6 | Γ₄ survival −0.0003, z −0.09, Šidák CI [−0.0068, +0.0063]; completion −0.0126, X₄ 0.0488 | JOINT − ISO-4, k 72 / 20 | `R/phase6/post_unblind_analysis/post_gamma4_t2000.md:12, :15, :18` | OK. The abstract's "−0.03 points". **FIXED**: §9.2 now gives Γ₄ and Γ₄′ their own bounds instead of "about ±0.7" (Γ₄′ reaches +0.81) |
| RES-7 | B̂ survival +0.0098, z +3.39, Šidák CI [+0.0033, +0.0163]; completion −0.0046 | ISO-4 − ISO | `post_gamma4_t2000.md:13, :16` | OK. `branch_B.md` §0's 95 % interval [+0.0041, +0.0155] is DERIVED: 0.0098 ± 1.96 × 0.00289 |
| RES-8 | Γ₄′ survival +0.0013, z +0.41, Šidák CI [−0.0056, +0.0081]; completion −0.0247 | JOINT − sweep_c50_p000, same card | `R/phase6/secondary/secondary.md:52-53` | OK |
| RES-9 | replicate sweep_c50_p000 − ISO-4: survival −0.0015 [−0.0086, +0.0056] | cross-card replicate, 95 % | `secondary.md:53` | OK |
| RES-10 | fire deaths/episode JOINT − ISO −0.1177, z −4.59 | secondary metric | `unblind/report.md:32` | OK |
| RES-11 | Γ(t) signs: completion `+ − + + − − − − − − −`, survival `+ − − + + + + + + + +` → UNSTABLE | rule (iv) | `post_evalfloor_gamma_t_high.md:38, :56` | OK |
| RES-12 | survival Γ(t) +0.0056 / +0.0083 / +0.0096 at t = 900 / 950 / 1000, the only points whose Šidák CI excludes 0 | "opens in the last fifth" | `post_evalfloor_gamma_t_high.md:52-54` | OK. "Last fifth" is DERIVED: every exclusion is at t ≥ 900 > 800 |
| RES-13 | completion Γ(750) −0.0147 [−0.0283, −0.0010]; negative from t = 700 | the completion lean | `post_evalfloor_gamma_t_high.md:31, :38` | OK. Descriptive |
| RES-14 | Γ_H completion −0.0079 (X 0.0340); survival +0.0038 (X 0.0254); 0.73× / 0.75× the floor-basis sd | High readout | `post_evalfloor_gamma_t_high.md:78, :80, :84, :86` | OK |
| RES-15 | Γ(2000): completion +0.0003; survival +0.0159, 95 % [−0.0002, +0.0319]; 4 seeds | T = 2000, descriptive | `post_gamma4_t2000.md:27-28`; log:3928 | OK |

## SEC — secondary dose design (non-verdict-bearing, 95 %)

| ID | value | what | source | status / note |
|---|---|---|---|---|
| SEC-1 | γ_n −0.0237 [−0.0419, −0.0057]; γ_p +0.0326 [+0.0137, +0.0502] | survival confound plane | `secondary.md:41` | OK |
| SEC-2 | no-element confound's share of the endpoint change −0.0119 [−0.0210, −0.0028] | the bound | `secondary.md:41` | OK |
| SEC-3 | predicted ISO-4 − ISO = +0.0079 | from γ_n | DERIVED: −0.0237 × (0 − 1/3) = +0.0079 | OK. Measured value is RES-7 |
| SEC-4 | predicted JOINT − ISO-4 ≈ +0.033 | from γ_p at p = 1 | DERIVED: +0.0326 × 1 | OK. Measured values are RES-6 and RES-8 |
| SEC-5 | survival sweep slope +0.0089 [−0.0033, +0.0211]; endpoint +0.0048 [−0.0021, +0.0117] | dose trend | `secondary.md:38-39` | OK |
| SEC-6 | both knees UNDERPOWERED; completion resolves nothing | knees | `secondary.md:25-28, :40` | OK |
| SEC-7 | mediation VOID: first-stage slope CI contains 0 | mediation | `secondary.md:46`; log:5099-5108 | OK |

## HW — reproducibility and hardware

| ID | value | what | source | status / note |
|---|---|---|---|---|
| HW-1 | seed sd / floor: completion 1.12× / 1.09×, survival 1.25× / 1.19× (ISO / JOINT); Γ_survival 5.40× the floor-basis sd(Γ) | beat-reproducibility hurdle | `unblind/report.md:38-39` | OK |
| HW-2 | eval floor: 4 reps × 2 checkpoints, bit-identical on unit 3 and to the grid's evals | eval reproducibility | `post_evalfloor_gamma_t_high.md:9`; log:5184 | OK |
| HW-3 | 280 of 288 paired cross-card evals identical; max \|Δ\| 2.44e−4 | cross-card check | `post_evalfloor_gamma_t_high.md:62-66` | OK. DERIVED: 70 + 70 + 69 + 71 = 280 |
| HW-4 | Γ: all 72 seeds on unit 1; ISO-4 and T = 2000 on unit 2; post-unblind evals on unit 3 | block structure | `R/phase6/by_card/README.md:31-35` | OK |

## SUP — supplement and venue mechanics

| ID | value | what | source | status / note |
|---|---|---|---|---|
| SUP-1 | ~454 KB (`che docs pyproject.toml uv.lock`) | code supplement size | `gpu_launch_prompt.md:78-79` (2026-08-04) | **OPEN (O-3)**. Written for shipping to a GPU box before most results were committed. It is not a measurement of the supplement, and `che/` now also contains gitignored archives (`R/phase6/m60/m06_spike_ckpt.tar.zst`, ~49 MB) |
| SUP-2 | TMLR supplementary code ≤ 100 MB | venue limit | log:3786-3789 | **OPEN (O-4)**. Secondary source only; no committed copy of TMLR's page records it |

---

## The 14 `\todo{verify}` values in the frozen tex

| tex site | value | row |
|---|---|---|
| `03_environment.tex:87` | 0.575 | ENV-2 |
| `03_environment.tex:88` | 0.866 | ENV-2 |
| `03_environment.tex:88` | 0.765 | ENV-3 |
| `03_environment.tex:89` | 0.821 | ENV-3 |
| `08_methodology.tex:15` | 0.0145 | METH-1 |
| `08_methodology.tex:16` | 0.0399 | METH-1 |
| `08_methodology.tex:17` | 0.0129 | METH-1 |
| `08_methodology.tex:17` | 0.0130 | METH-1 |
| `08_methodology.tex:31` | 92.1 % | METH-3 |
| `08_methodology.tex:31` | 62.8 % | METH-3 |
| `08_methodology.tex:32` | 76.7 % | METH-3 |
| `08_methodology.tex:40` | 55.6 % | METH-4 |
| `08_methodology.tex:79` | 2.1× | METH-5 (the hypothesis caveat applies) |
| `08_methodology.tex:80` | 5.2× | METH-5 |

All 14 are verified. `paper/tex/` is frozen, so the `\todo`s stay in the tex.
Any text ported from it cites these rows.

## OPEN — before these numbers ship

- **O-1 (owner): PBT.** No reported result trained with PBT. Every science
  run is single-policy IPPO (ENV-11). `README.md:28` and the `CLAUDE.md`
  project description both describe training as a PBT-style hybrid. The paper
  must describe what ran. Owner's call: say "IPPO, one policy per seed" and
  mention the PBT loop only as benchmarked infrastructure, or drop it.
- **O-2 (builder, $0 CPU; owner go-ahead):** a committed artifact for the
  R_L logistic-centre estimate of β̂_c (CAL-1, CAL-2). The raw
  `calibration_crossing.npz` is committed. Alternatively, restate §4 with the
  estimator that is already committed.
- **O-3 (builder):** measure the actual supplement size, built with
  `git archive` so gitignored archives are excluded (SUP-1).
- **O-4 (owner):** confirm TMLR's supplement limit on the venue's own page
  (SUP-2).
