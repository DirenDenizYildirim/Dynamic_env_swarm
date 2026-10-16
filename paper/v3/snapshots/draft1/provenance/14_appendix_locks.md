# Provenance: sections/14_appendix_locks.md

Writer: W2 (Paper v3, step 4, 2026-10-14). Checked with
`paper/v3/src/provenance_check.py --strict 14_appendix_locks`. "v2 NN:n" is
`paper/v2/sections/NN_*.md` line n (03 environment, 06 Coupling B, 07 comms,
13 appendix B/C).

Counts (P3's method): prose **294** words against about 350; tables 281
words; one listing (Listing 6), byte-identical (`build_v3.py`: 6/6). Every
value is one v2 printed (v2 13:8-46), with its ruling date removed (dates
live in Appendix D, W4) and every lock-record pointer replaced by the
section that describes the constant.

| # | sentence (verbatim) | support | change from v2, and why |
|---|---|---|---|
| 1 | B Locked constants and hyperparameters | framing | edited (v2 13:3 "B Locks and hyperparameters"; the stub's heading) |
| 2 | Each constant below was fixed before the main experiment; Appendix D gives when. | DX-401; DX-402; paper/v3/BRIEF.md:167 | edited (v2 13:6): "fixed by a ruling on the date given" → "fixed before the main experiment; Appendix D gives when" (dates move to Appendix D, V3-S2; stub NOT HERE: ruling dates) |
| 3 | A test in the code supplement (che/tests/test_locks.py) checks each against the configurations and the code defaults. | che/tests/test_locks.py:131-176; che/tests/test_locks.py:350-363 | edited (v2 13:6): "the test described in §11" → the test's path in the code supplement; "or the analysis scripts" folded into "the code defaults" (test_locks.py:350 checks the analysis modules' literals) |
| 4 | constant / value / described in | framing | edited (v2 13:8): the "ruled" and "record" columns dropped (dates to Appendix D; no lock-record pointers, stub NOT HERE); a "described in" column added |
| 5 | critical point $\hat\beta_c$ / 0.500 ± 0.005 / §4.1, with its estimator's provenance | CAL-1 | edited (v2 13:10): the estimator caveat replaced by a pointer to its home §4.1 (checks/caveats.yaml C31) |
| 6 | β at Low / Medium / High / 0.43 / 0.49 / 0.70 / §4.1 | CAL-3 | kept (v2 13:11), date dropped |
| 7 | β held out ($\theta^$) / 0.49 / §6.2 | CAL-3; DX-401 | kept (v2 13:12), date and ruling gloss dropped |
| 8 | $f_{\mathrm{weak}}$, $\lambda_0$, $\lambda_{\mathrm{load}}$, $\kappa_A$, $r_A$ / 0.15, 5e-5, 4e-4, 0.06, 1 / Definition 5 | CA-1 | kept (v2 13:13), date dropped |
| 9 | smoothing passes of the weak-terrain field / 2 / Definition 5 | DX-401; che/env/structure.py:38-55 | edited (v2 13:14 "weak-floor smoothing passes"): "weak-floor" → "weak-terrain field" (Definition 5's term) |
| 10 | $\kappa_B$ / 1.0 / Definition 6; the bands below | CB-1 | edited (v2 13:15): "Coupling-B lock record, on the detection band alone" → "Definition 6; the bands below" |
| 11 | δ off / on; $R_{\mathrm{comm}}$ / 0.0 / 1.0; 16 / Definition 7 | DX-401; COM-6 | kept (v2 13:16), date dropped |
| 12 | death penalty $d_p$ / 0.5 / Definition 2 | ENV-1 | kept (v2 13:17), date dropped |
| 13 | observation encoding / the observation as masked by smoke / Definition 6 | DX-401; che/env/observation.py:1-36 | edited (v2 13:18 "3, the masking observation (§3)"): the internal version number dropped (terms list: obs v3); "as masked by smoke" (BRIEF §5.2) |
| 14 | $\sigma_s$, η, ι / 1.0, 0.5, 0.0 / Definition 3; not locked, fixed by convention and never calibrated | DX-1 | kept (v2 13:19) |
| 15 | The analysis constants of the worked example (§6) are fixed the same way. | DX-402; DES-13 | new (one framing sentence for the second table) |
| 16 | constant / value / role | framing | edited (v2 13:21): the "ruled" column dropped (Appendix D) |
| 17 | K_CONFIRMATORY / 40 / design seeds per confirmatory arm, the base of the registered seed rule | DES-1 | kept (v2 13:23); "the seed rule's base" → "the base of the registered seed rule" |
| 18 | K_LADDER_CAP / 60 / the seed rule's cap | DES-1 | kept (v2 13:24) |
| 19 | K_CONFIRMATORY_REALIZED / 72 / the seed count at which Γ is read (§6.2; history in Appendix D) | DES-13; DES-3 | edited (v2 13:25): "a recorded deviation (§9.1)" → "(§6.2; history in Appendix D)": the deviation's home is §6.2 (checks/caveats.yaml C09), so it is pointed to, not restated |
| 20 | K_SECONDARY / 20 / seeds per secondary arm; ISO-4 uses the same count | DES-13 | kept (v2 13:26) |
| 21 | SIDAK_M; $z_\alpha$ / 2; 2.2365 / the two co-primary tests, Šidák-corrected | DES-13 | kept (v2 13:27) |
| 22 | POWER_STOP / 0.80 / the minimum design-stage power | DX-402 | edited (v2 13:28): "at the 0.03 band" cut (DES-4's band belongs to the seed-rule history, Appendix D) |
| 23 | T_STAR / 1000 / the training budget in updates | DES-13; DX-402 | edited (v2 13:29): "unchanged since 2026-08-03" cut (date, Appendix D) |
| 24 | GAMMA_T_RETENTION / 11 / checkpoints kept for Γ(t): updates 500–1000 every 50 | DES-13 | kept (v2 13:30) |
| 25 | evaluation draw / seed 0 × 512 episodes / common to every run; not in the constant registry | DES-13 | edited (v2 13:31): "registered with the grid layout" cut; "not in the lock registry" → "not in the constant registry" |
| 26 | PLATEAU_PASS; PLATEAU_REVIEW / 1.0; 1.5 / thresholds of a convergence check retired before the main training runs (Appendix D) | DX-402; METH-6; DES-12 | edited (v2 13:32 "the convergence check's thresholds, retired 2026-08-11; grade nothing"): date → "before the main training runs" (METH-6 2026-08-11 precedes the grid's start, DES-12 2026-09-09); "grade nothing" cut (terms list) |
| 27 | Every run of the worked example uses the hyperparameters below. | DX-2 | edited (v2 13:34 "The training hyperparameters are identical for every run of §9") |
| 28 | The main training runs pass none on the command line, so the configured defaults apply. | DX-2; che/scripts/run_p6_grid.sh:299-301 | edited (v2 13:34): "the grid" → "the main training runs" (BRIEF §5.2) |
| 29 | hyperparameter / value | framing | kept (v2 13:36) |
| 30 | learning rate / 3e-4, constant, no schedule | DX-2 | kept (v2 13:38) |
| 31 | discount γ; GAE λ / 0.99; 0.95 | DX-2 | kept (v2 13:39) |
| 32 | PPO clip ε / 0.2 | DX-2 | kept (v2 13:40) |
| 33 | entropy coefficient; value coefficient / 0.01; 0.5 | DX-2 | kept (v2 13:41) |
| 34 | global gradient-norm clip; Adam ε / 0.5; 1e-5 | DX-2 | kept (v2 13:42) |
| 35 | parallel environments; steps per update / 256; 128 | DX-2 | kept (v2 13:43) |
| 36 | minibatches; epochs / 4; 4 | DX-2 | kept (v2 13:44) |
| 37 | checkpoint interval / 50 updates | DX-2 | kept (v2 13:45) |
| 38 | budget / 32,768 environment steps per update, 32,768,000 per run | DX-3; DES-13 | kept (v2 13:46) |
| 39 | network / two convolutions with 16 and 32 channels, a dense layer of 128 units, actor and critic heads with a 64-unit layer each | ENV-10; che/train/networks.py:87-110 | new row: v2 03:234's network sentence moved here (§3.5 points to Appendix B) |
| 40 | messages / dimension 8, delivered one step later as a masked mean over open links | DX-17; che/env/comms.py:99-110 | new row: v2 07:11's message dimension and delivery moved here |
| 41 | The strength $\kappa_B$ was to be locked where three bands set before calibration intersect. | DX-301; kappa_b_lock.md:113-119 | kept (v2 06:37); moved here (stub JOB: "Coupling B's lock bands that did not intersect") |
| 42 | They were a masked share of the crop at Medium in [0.15, 0.45], a probability in [0.4, 0.7] that a Burning cell three cells away is revealed at Medium, and the corridor toy's $q$ (Theorem 1) in [0.3, 0.7]. | DX-301; kappa_b_lock.md:113-119 | edited (v2 06:37): "a toy information probability q" → "the corridor toy's q (Theorem 1)" (stub: toy codes as plain names) |
| 43 | They do not intersect. | DX-301; kappa_b_lock.md:105-111 | kept (v2 06:37) |
| 44 | The masked-share band cannot be reached at Medium: the masked share can only approach the share of crop cells with smoke on their line of sight, 0.130 there under a random policy, below the band's lower edge of 0.150. | CB-3; DX-12; kappa_b_lock.md:155-169 | kept (v2 06:37) |
| 45 | The same $\kappa_B$ attenuates the arena's extended smoke more strongly than the toy's single smoke source, which leaves the detection and toy bands disjoint by a factor of 1.35 under a random policy and 1.15 under probe policies. | CB-2; kappa_b_lock.md:187-196 | kept (v2 06:37) |
| 46 | $\kappa_B = 1.0$ was therefore locked on the detection band alone; the masked-share band was retired, not widened, and the toy band was kept as a consistency check. | CB-1; kappa_b_lock.md:1-23; kappa_b_lock.md:412-418 | edited (v2 06:37 "On 2026-07-27, κ_B = 1.0 was locked …"): the date moves to Appendix D (V3-S2); "therefore" added; "kept" → "was kept" |
| 47 | No gradient crosses the communication channel, so the message head, a tanh-bounded dense layer on the shared trunk, stays at its initialization: an agent emits a fixed random projection of trunk features that are themselves trained. | ENV-12; che/train/networks.py:26-38; che/train/networks.py:108-112; che/train/ippo.py:323-329 | edited (v2 07:24): "frozen random projection" → "fixed random projection" (the ruled phrase's home is §4.4); "the trunk" → "the shared trunk"; moved here with Listing 6 (STRUCTURE §5 row 6) |
| 48 | The receivers' weights on the message inputs are trained, which makes message use testable; what to say was never learned. | ENV-12; che/train/networks.py:108-112 | kept (v2 07:24) |
| 49 | Listing 6. Delivered messages carry no gradient, so the message encoder stays at its initialization. | che/train/ippo.py:323-329 | edited (v2 07:12 "Delivered messages carry no gradient."): the label says what follows from it (stub); listing byte-identical (build: 6/6) |

## Findings

- [record] `docs/locks.yaml` is modified in the working tree this session
  (`git status`: ` M docs/locks.yaml`, presumably the interaction-check
  configs). This file cites no `locks.yaml` line, only ledger rows read at
  their committed sources; the ledger rows DX-401 and DX-402 cite
  `locks.yaml` line numbers, which a reviewer should re-check against the
  committed file if the edit shifted them.
- [scope] The analysis-constant table keeps v2's set. `K_CONFIRMATORY_REALIZED`
  points to §6.2 for the deviation (caveat C09's home) rather than restating
  it; the seed rule's history is Appendix D's (W4).

## Alternates

None.
