# Provenance: sections/07_example_results.md

Writer: W4 (Paper v3, step 4, 2026-10-14). Checked against the section on 2026-10-14.
v2 source: `paper/v2/sections/09_compositional_test.md` (§9.2). Interval values in
the sentences are points (rate × 100) of the cited rows.

Word counts (`paper/v3/src/wordcount.py`): see the hand-back; budget 480 prose,
captions 60 each.

| # | sentence (verbatim) | support | change from v2, and why |
|---|---|---|---|
| 1 | 6.3 Results | framing | edited: v2 '9.2 Results' renumbered (STRUCTURE §2) |
| 2 | Every secondary analysis, the plane decomposition included, is non-verdict-bearing, as registered: its 95 % intervals are not family-corrected, and its specification was ratified after Γ was seen and before the sweep was read. | SEC-1; DX-413; DX-28 (95 %, bootstrap); che/bench/results/phase6/secondary/secondary.md:5 | edited from paper/v2/sections/09_compositional_test.md:112: C15 home; fix round, RM-1: the lead sentence before it ('The secondary analysis comes first …') cut |
| 3 | A sweep holds each coupling's frequency at 0.5 while $p$ moves from 0 to 0.5, and three identification arms at frequency 0.4 make a plane in co-occurrence and fire-only share estimable (Appendix F). | DES-9; DX-28 | edited from paper/v2/sections/09_compositional_test.md:52; fix round, RM-11: $p$ as math; RN2-3: 'three' tagged DX-28 |
| 4 | On survival, the plane's co-occurrence slope $\gamma_p$ is +3.26 points per unit $p$ [+1.37, +5.02], and its fire-only-share slope $\gamma_n$ is −2.37 points per unit $\nu$ [−4.19, −0.57] (Figure 7). | SEC-1 | edited from paper/v2/sections/09_compositional_test.md:112 and v2 App. H; fix round, RM-11: $p$, $\nu$ as math |
| 5 | By the identity of §6.2, the plane separates co-occurrence from the active share only; per-coupling frequency moves with each slope. | X4-1; DES-9; che/bench/results/phase6/secondary/secondary.md:60 ('γ_p moves single-element mass into both-element episodes, which also raises per-element exposure'); paper/v3/BRIEF.md:461-466 | new: V3-F4 and BRIEF §9.2 trap 2 (the plane separates co-occurrence from the active share only) |
| 6 | The fire-only-share slope predicts ISO-4 − ISO at +0.79 points, inside B̂'s interval, though that move also changes frequency. | SEC-3; RES-7; DES-9 | kept from paper/v2/sections/09_compositional_test.md:112; fix round, RM-1: 'without attributing B̂ to the fire-only share as such' shortened to 'though that move also changes frequency' |
| 7 | The co-occurrence slope, fitted on $p$ up to 0.5, predicts JOINT − ISO-4 at +3.26 points, far above the measured Γ₄ (Table 3): it does not extrapolate to JOINT. | SEC-4; DX-28; RES-6 | kept from paper/v2/sections/09_compositional_test.md:112; fix round, RM-11: $p$ as math; the following sentence on linearity cut for RM-1 (Appendix F states it, DX-39) |
| 8 | Secondary design on the triangle of training mixtures, with plane predictions beside measured contrasts | framing | kept (v2 iframe title, paper/v2/sections/09_compositional_test.md:115) |
| 9 | Figure 7. Read first: the plane's prediction from the fire-only-share slope γ n beside the measured B̂, and from the co-occurrence slope γ p beside the measured Γ₄ and Γ₄′. | SEC-3; SEC-4; RES-6; RES-7; RES-8; paper/figures/interactive/MANIFEST.md:278-290 | edited from v2 Figure 13's caption (paper/v2/sections/09_compositional_test.md:116): γ_p's and γ_n's rows named first (P2 R6 fallback; stub) |
| 10 | Left, the triangle of training mixtures in co-occurrence p and fire-only share ν (labelled “n” on the figure), with lines of fixed per-coupling frequency μ (labelled “m” on the figure); right, the secondary estimates: the change point (labelled “knee” on the figure), the sweep slope (labelled “dose slope” on the figure), the fire-only share's part of the endpoint change (labelled “no-element share” on the figure), the p = 0 sweep arm (labelled “sweep_c50_p000” on the figure). | DES-9; SEC-5; SEC-6; DX-28; paper/figures/interactive/MANIFEST.md:278-283 | edited from v2 Figure 13's caption; fix round, RM-10: the printed m and n glossed in the exact form |
| 11 | Switch the metric; toggle the predictions. | paper/figures/interactive/MANIFEST.md:291 | edited: v2's 'Interact:' list cut to the interact span |
| 12 | A triangle of training mixtures by share of both-stressor and fire-only episodes, locating the secondary arms, ISO, ISO-4 and JOINT, beside the secondary estimates and the plane predictions next to the measured contrasts | framing | kept (v2 alt text, paper/v2/sections/09_compositional_test.md:120) |
| 13 | Static companion of Figure 7 for the printed PDF. | framing | edited: Figure 13 → Figure 7 |
| 14 | On survival, Γ is +0.96 points, Šidák-corrected 95 % CI [+0.47, +1.44]: REJECT (Table 3, Figure 8). | RES-2; DES-13 | edited from paper/v2/sections/09_compositional_test.md:73; fix round, RM-1: the lead sentence 'The registered test reads as follows' cut and its pointers moved here |
| 15 | On completion it is −1.73 points [−4.12, +0.66], null: no detectable change, and the result excludes a joint-training gain larger than 0.66 points. | RES-1 | edited from paper/v2/sections/09_compositional_test.md:73 ('The completion null excludes a joint-training gain larger than 0.66 points, the upper end of its interval'): C17 home, the registered string verbatim; 'no detectable change' (stub) |
| 16 | The design's completion detection limit, the registration's X, is 3.29 points; realized power at the 3-point effect that motivated the design was 71.6 %. | RES-1; METH-7; DES-6; phase6_framing_branches.md:188-195; che/scripts/p6_unblind.py:116-117 | edited from paper/v2/sections/09_compositional_test.md:73 and :50: C23 home; X named a detection limit, never a bound (BRIEF §9.2 trap 5); fix round, RM-1: shortened |
| 17 | The registered falsifier for this outcome passes (Appendix D). | RES-5 | edited from paper/v2/sections/09_compositional_test.md:89: the verdict only (stub (b)); the rule and the margin are in Appendix D |
| 18 | The survival gain does not survive the inert-share correction. | RES-6; decision log, UNBLIND RESULT (docs/decision_log.md:4987-4994) | edited from paper/v2/sections/09_compositional_test.md:91 ('the survival effect does not survive the inert-share correction'): the registered string first (C18 home) |
| 19 | Γ₄, the corrected gap, is −0.03 points on survival [−0.68, +0.63], null, and the gain is not called a composition effect. | RES-6; docs/decision_log.md:4018-4025 | edited from paper/v2/sections/09_compositional_test.md:91; fix round, RN2-2, RC2-9, RC1-14: split from the completion clause |
| 20 | On completion both gaps are null, so Γ₄ is a second exclusion bound, the registration's term for its detection limit, X₄ = 4.88 points. | RES-6 (X₄ 0.0488); che/bench/results/phase6/post_unblind_analysis/post_gamma4_t2000.md:18 | fix round, RN2-2, RC2-9, RC1-14 (SHOULD): 'second exclusion bound' kept verbatim, and the registered X₄ stated as the detection limit it is (BRIEF §9.2 trap 5) |
| 21 | Γ₄ excludes only a large composition effect: its upper bound, +0.63, lies above Γ's lower bound, +0.47, and its survival detection limit is 0.90 points. | RES-6; RES-2; X4-4 | edited from paper/v2/sections/09_compositional_test.md:97 ('Γ₄'s upper bound, +0.63 points, lies above Γ's lower bound, +0.47, so the correction excludes a large composition effect but leaves a smaller one possible'): C19 home; Γ₄'s detection limit added (X4-4; STRUCTURE §11 row 12) |
| 22 | JOINT still sees each coupling twice as often as ISO-4, and always combined. | DES-14 | kept from paper/v2/sections/09_compositional_test.md:97 ('JOINT still sees each coupling twice as often as ISO-4 and always in combination'): C06 home |
| 23 | Γ₄ compares runs on two GPUs; its same-GPU replicate Γ₄′, JOINT minus the $p = 0$ sweep arm (ISO-4's mixture on JOINT's GPU), agrees on both co-primaries but was proposed after Γ₄ was seen. | RES-8; HW-4; DES-15; DX-28 | edited from paper/v2/sections/09_compositional_test.md:93: C22 home; fix round, RM-1 and RM-11: shortened, $p = 0$ as math |
| 24 | B̂ is reported without a test, as registered. | RES-7; docs/decision_log.md:4029 | edited from paper/v2/sections/09_compositional_test.md:95: C20 home; fix round, RM-1: '+0.98 points on survival' left to Table 3 |
| 25 | Because Γ = Γ₄ + B̂ holds by construction for arm means, B̂ is not a second finding. | RES-2; RES-6; RES-7 | kept from paper/v2/sections/09_compositional_test.md:95 ('Because Γ = Γ₄ + B̂ holds identically for arm means, a B̂ close to Γ restates a Γ₄ close to 0 and is not a second finding'), shortened; C21 home |
| 26 | The registered headline for this outcome no longer holds as worded (Appendix D). | phase6_framing_branches.md:102; decision log, UNBLIND RESULT (docs/decision_log.md:4987-4994) | edited from paper/v2/sections/09_compositional_test.md:91: one clause, no branch letter; fix round, RM-1: the quotation left to Appendix D.3 |
| 27 | Γ(t), the gap at earlier checkpoints, is sign unstable over the final half on both co-primaries. | RES-11; DES-13 | edited from paper/v2/sections/09_compositional_test.md:99: C16 home; fix round, RM-1: 'retained' cut |
| 28 | On survival, its Šidák interval excludes zero only at updates 900, 950 and 1000. | RES-12 | edited from paper/v2/sections/09_compositional_test.md:99 ('It reads +0.56, +0.83 and +0.96 points at updates 900, 950 and 1000, the only checkpoints whose Šidák interval excludes zero'): values to Appendix E (budget) |
| 29 | Completion is negative at every checkpoint from update 700 and leans negative without resolving (Appendix E). | RES-13 | edited from paper/v2/sections/09_compositional_test.md:99; fix round, RM-1: '70 % of the budget' cut (update 700 of 1000 stays) |
| 30 | Restated in agents, the survival gain is about a tenth of an agent per episode (0.11 of 12), detectable only in the last fifth of training. | X4-3; ENV-6; RES-12 (note: 'last fifth' DERIVED, every exclusion at t ≥ 900 > 800) | new: V3-F3 home (row X4-3); fix round, RC2-14 and RN1-4: 'appears' made 'detectable' (only detectability is confined to the last fifth); the precise checkpoints stand in the preceding paragraph |
| 31 | The paper does not rest on it. | framing; paper_v3_prompt.md:201-204 (V3-F3: 'The paper no longer rests on it') | new: V3-F3 |
| 32 | Table 3. Arm means (rates) and registered contrasts (points, rate × 100) at θ\, with Šidák-corrected 95 % intervals; k in the order of each contrast's arms. | DES-13 | edited from paper/v2/sections/09_compositional_test.md:75; fix round, RM-1: shortened ('after 1000 updates' is in §6.2) |
| 33 | quantity / k / completion / survival / status | framing | edited from paper/v2/sections/09_compositional_test.md:77: 'contrast' column made 'quantity' (arm means added) |
| 34 | ISO mean / 72 / 0.7772 / 0.9158 / confirmatory arm | DES-3; RES-4 | new row (RES-4 arm means; stub Table 3) |
| 35 | JOINT mean / 72 / 0.7600 / 0.9254 / confirmatory arm | DES-3; RES-4 | new row |
| 36 | ISO-4 mean / 20 / 0.7726 / 0.9256 / sensitivity arm | DES-13; DX-18 | new row |
| 37 | Γ = JOINT − ISO / 72 / 72 / null: −1.73 [−4.12, +0.66] / REJECT: +0.96 [+0.47, +1.44] / confirmatory | DES-3; RES-1; RES-2 | kept from paper/v2/sections/09_compositional_test.md:79 (z values dropped) |
| 38 | Γ₄ = JOINT − ISO-4 / 72 / 20 / null: −1.26 [−4.81, +2.28] / null: −0.03 [−0.68, +0.63] / sensitivity arm, two GPUs | DES-3; DES-13; RES-6; HW-4 | kept from paper/v2/sections/09_compositional_test.md:81 (z values dropped; 'across GPUs' made 'two GPUs') |
| 39 | Γ₄′ = JOINT − the p = 0 sweep arm / 72 / 20 / null: −2.47 [−6.16, +1.22] / null: +0.13 [−0.56, +0.81] / secondary, one GPU | DES-3; DES-13; RES-8; DX-19; HW-4 | kept from paper/v2/sections/09_compositional_test.md:82 ('same GPU' made 'one GPU' so the C22 pattern stays in its one sentence) |
| 40 | B̂ = ISO-4 − ISO / 20 / 72 / −0.46 [−4.05, +3.12] / +0.98 [+0.33, +1.63] / no registered test | DES-13; DES-3; RES-7; DX-19 | kept from paper/v2/sections/09_compositional_test.md:83 (status shortened to 'no registered test') |
| 41 | Registered readings in order: Gamma, Gamma4, Gamma4 prime and B-hat on both co-primaries | framing | kept (v2 iframe title, paper/v2/sections/09_compositional_test.md:65) |
| 42 | Figure 8. The registered contrasts in order on completion and survival, one step per row (labelled “rung” on the figure): Γ, with the registered 60-seed analysis; Γ₄; Γ₄′; and B̂, which has no registered test. | RES-1; RES-2; RES-3; RES-6; RES-7; RES-8; paper/figures/interactive/MANIFEST.md:162-173 | edited from v2 Figure 11's caption (paper/v2/sections/09_compositional_test.md:66): the 'rung' label glossed in the exact form (V3-S3) |
| 43 | Rows name one GPU (labelled “unit 1” on the figure) or two (labelled “cross-unit” on the figure). | HW-4; paper/figures/interactive/MANIFEST.md:165 | edited from v2 Figure 11's caption ('“Unit n” is GPU n, “cross-unit” means across GPUs'): glossed without GPU numbers in the main text (V3-S3) |
| 44 | Values are rates. | paper/figures/interactive/MANIFEST.md:173-176 (the figure plots the rates of its JSON sources) | new: the figure prints rates, the text points (stub; V3Q12 default) |
| 45 | The stipple on Γ is ±1 floor-based standard error (labelled “floor basis” on the figure). | DX-21; paper/figures/interactive/MANIFEST.md:166-168 | edited from v2 Figure 11's caption ('the stipple, on Γ only, is ±1 floor-based standard error of Γ (labelled “floor basis”)') |
| 46 | Step through the rows; toggle the bands. | paper/figures/interactive/MANIFEST.md:163-164 | edited: v2's 'Interact:' list cut to the interact span |
| 47 | Two forest plots, completion and survival, of the registered contrasts in order with their Šidák-corrected intervals and verdicts | framing | kept (v2 alt text, paper/v2/sections/09_compositional_test.md:70) |
| 48 | Static companion of Figure 8 for the printed PDF. | framing | edited: Figure 11 → Figure 8 |

## Findings

- [record] DX-406 and the v3 WRITERS.md spec for X4-3 cite
  `che/tests/test_lethality.py:201-202` for "no agent revives"; in the
  committed file the comment and its assert are at :202-203 (:201 is the
  "hazard actually killed someone" assert). X4-3 cites :202-203. Direction:
  correct DX-406's line reference.
- [caption] Figure 7's caption carries four glosses (knee, dose slope,
  no-element share, sweep_c50_p000) and Figure 8's four (rung, unit 1,
  cross-unit, floor basis); both exceed the 60-word cap because of them
  (counts in the hand-back). "dose slope" is printed on Figure 7 and is a
  banned term, so it is glossed although the stub's list omits it.
- [figure] Figure 8 prints a registration date on each row
  (`paper/figures/interactive/MANIFEST.md:165`, "registration date"), a date
  in the main text that the date check cannot see (it scans no figure). A
  label-only rebuild (V3Q8) would remove it.
- [style] Prose is over the 480-word budget (hand-back); the overage is the
  plane paragraph, which PAPER V3 item 2(c) moves into the results.

## Alternates

None.
