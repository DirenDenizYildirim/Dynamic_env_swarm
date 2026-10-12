# Provenance: sections/04_severity.md

Writer: W3. Checked against the section on 2026-10-11 with
`paper/v2/src/provenance_check.py 04_severity` (no snapshot label taken).

Counts (P3's method, `plans/P3.md` §5, as `STRUCTURE.md` §6 states it): prose
786 words against a budget of 700 (the demo's 998); the alternate without
Corollary 1's supercritical item is 706. Figure 5's caption and note, with
the companion's include caption, 118 words against a cap of 120. The levels
table is not counted. The iframe height is 528 px, the measured self-sized
height at 1280 px from the orchestrator's table.

"demo 04:n" is `paper/demo_beyond/sections/04_severity.md` line n. "TF" is
`docs/theory_foundations.md` (not edited). Corollary 1's items are numbered 1
and 2 here; demo items 2 and 3 are cut and demo item 4 is this file's item 2.

| # | sentence (verbatim) | support | change from the demo, and why |
|---|---|---|---|
| 1 | 4 Severity calibration | framing | kept (demo 04:3) |
| 2 | Severity in CHE is placed by a measured dynamical phase of the fire: the three levels sit below, near and above the implemented kernel's measured transition (Figure 5). | CLAUDE.md:70-71; CAL-1; CAL-3; severity_lock.md:25-31 | edited: demo 04:5 "Severity in CHE is a measured dynamical phase of the fire, not a value of β chosen by hand. Figure 5 shows the measurement the three levels rest on, beside one fire burning at each level." The antithesis goes (P3-§6) and the figure pointer is folded in (LEN). Pass 3, RN1-15 (class B, consistency): "three" now carries CAL-3, as §1 tags the same count |
| 3 | Severity explorer: spanning probability against ignition probability, and one fire at each locked level | framing; paper/figures/interactive/MANIFEST.md:309-313 | kept (demo 04:8); the iframe height is now the measured 528 px (the orchestrator's height table, from paper/v2/out/kit_checks.md) |
| 4 | Figure 5. Severity as a measured phase. | framing | kept (demo 04:9) |
| 5 | Left: the spanning probability, the chance that one centre ignition reaches the arena boundary, against β on an all-fuel grid with no agents, for three arena sides (512 seeds per point). | DX-7; che/bench/results/phase2/calibration_report.md:4-10; paper/figures/interactive/MANIFEST.md:309-311 | edited: the P_span symbol, "for L = 32, 48 and 64" and "±1 binomial SE" are not repeated, since the figure prints them (STRUCTURE.md §8, R3); the seed count, which it does not print, stays |
| 6 | Vertical rules mark the locked levels; the triangle marks the largest arena's pseudo-critical point. | CAL-3; CAL-4; paper/figures/interactive/MANIFEST.md:309-311 | edited: the printed values "Low 0.43, Medium 0.49 and High 0.70" and "β_c(64) ≈ 0.486, where P_span = ½ at L = 64" are not repeated (R3) |
| 7 | Right: one random-policy episode per level under the severity configurations, with δ 0; only the fire and its smoke (hatching) are drawn. | DX-202; paper/figures/interactive/MANIFEST.md:312-317 | edited; class B, P2-1: "δ 0" stays in the caption because the printed companion's subtitle is cut before it; "64 × 64", "episode key 0" and the κ values, which the figure prints, are not repeated (R3); "each panel captioned with its level's calibration values" and "not agents, food or structure" cut (cap) |
| 8 | Neither the R L curves nor the locked critical point β̂ c is shown (§4.3). | paper/figures/interactive/MANIFEST.md:309-311; CAL-1 | edited: demo "The figure does not show the locked critical point β̂c or the crossing curves it was read from (§4.3); each render is one episode, neither a distribution nor trained behaviour." The second clause moves to the status note ("illustrative, one episode each") |
| 9 | Status: calibration, no agents (curves) · illustrative, one episode each (renders) · Interact: play or drag the time slider; click a panel. | framing; paper/figures/interactive/MANIFEST.md:312-313 | edited: the status tag and the interaction shortened to the caps of STRUCTURE.md §8 (R4); the arrow-key and table-view instructions cut |
| 10 | Spanning probability of a centre ignition against ignition probability for three grid sizes, with the three locked severities marked, beside one illustrative fire episode at each severity. | paper/figures/interactive/MANIFEST.md:322-324 | kept (demo 04:13) |
| 11 | Static companion of Figure 5 for the printed PDF. | framing | kept (demo 04:13) |
| 12 | 4.1 Phase structure of the idealized kernel | framing | kept (demo 04:16) |
| 13 | Corollary 1 (Phase structure). On $\mathbb{Z}^2$ with the von Neumann neighbourhood, the fire of Definition 3 with $\iota = 0$ and a single ignition at the origin inherits the phase structure of bond percolation (Proposition 2, whose coupling holds on any graph): | docs/theory_foundations.md:210-212; docs/theory_foundations.md:194-203 | kept (demo 04:18; ", in particular ℤ²" cut) |
| 14 | Its critical point is $\beta_c = 1/2$ exactly, the critical probability of bond percolation on the square lattice (Kesten, 1980). | kesten1980; paper/related_work_verification.md:266; paper/v2/citations/theory_cites.md:83-107 | edited; class A, C1, and class B, N15: demo item 1 "*Critical point.* β_c = 1/2 exactly, a theorem of Kesten (1980)." now states the value at the level of the cited title. Demo items 2 and 3 are cut: (2) "*Subcritical,* β < β_c. The burnt cluster is almost surely finite; its expected size χ(β) is finite, the cluster-size distribution has exponential tails, and the correlation length ξ(β) is finite." (class B, N7 and P1-N4: no verified source beyond kesten1980's title, theory_cites.md:103-107); (3) "*Critical scaling,* β ↑ β_c. χ(β) ∼ \|β − β_c\|^{−43/18} and ξ(β) ∼ \|β − β_c\|^{−4/3}, the exponents of two-dimensional percolation." (class A, C1; P3-N4) |
| 15 | For $\beta > \beta_c$ the fire spreads indefinitely with positive probability. | garet2004chemical; paper/related_work_verification.md:1072-1076; paper/v2/citations/C1_verification.md:296-298 | edited; class A, C1 (rows 15–18 replace demo item 4, "*Supercritical,* β > β_c. With positive probability the fire spreads indefinitely; conditioned on that, the burnt region grows linearly in time, with an asymptotic front speed v(β) > 0 and a deterministic limiting shape."). Positive probability above β_c is presupposed by the theorem's conditional measure (setup, p. 170). The alternate drops rows 15–18 (Q4g) |
| 16 | On that event the cells ignited by step $n$ are those within $n$ open edges of the origin. | paper/v2/citations/C1_verification.md:187-198; paper/related_work_verification.md:1093-1097 | new; class A, C1: the identification of the cells ignited by step n with the chemical ball of radius n is the step-2 reviewer's derivation from Definition 3 and Proposition 2's coupling (Open items W3-F8) |
| 17 | Scaled by $1/n$, they converge almost surely in Hausdorff distance to a deterministic convex compact set with non-empty interior, invariant under permutations and reflections of the coordinates (Garet & Marchand, 2004; their Corollary 5.4). | garet2004chemical; paper/related_work_verification.md:1082-1089 | new; class A, C1: Corollary 5.4 (p. 188) as recorded, with "their" marking the cited work's numbering for the cross-reference check |
| 18 | The growth is therefore linear in $n$, at a speed given in each direction by the extent of that set. | garet2004chemical; paper/related_work_verification.md:1079-1081; paper/related_work_verification.md:1100-1102; paper/v2/citations/C1_verification.md:278-283 | new; class A, C1: replaces the single scalar "front speed v(β)" (C1_verification.md:305). It says only what Corollaries 4.2 and 5.4 give: the speed in each direction is the set's extent in that direction (1/µ(u)); it claims neither that the set is a disc nor that it is not |
| 19 | Both items concern the idealized kernel (von Neumann neighbourhood, constant burn time, homogeneous fuel, no wind) on the infinite lattice. | docs/theory_foundations.md:227-228; paper/v2/citations/C1_verification.md:287-289 | edited; class B, N7: demo 04:25 "The exact value belongs to the idealized kernel (von Neumann neighbourhood, constant burn time, homogeneous fuel, no wind) on the infinite lattice. Other neighbourhoods, heterogeneous fuel, wind or geometric burn times shift β_c and break exactness; the existence of the transition and the divergence of χ and ξ near it are universal, and the design relies on nothing more." The uncited claims about other kernels and universality are cut (review_of_demo.md:675-689); the scope is kept |
| 20 | CHE's fire is that kernel on a finite arena, with ignitions added by Coupling A (§5.1), so the levels are placed against a measured finite-size threshold and, at High, a measured front speed (§4.3). | docs/theory_foundations.md:232-233; DX-201; DX-6; paper/v2/citations/C1_verification.md:303-304; che/env/structure.py:83-102 | edited: demo 04:25 "CHE's fire kernel on its own is the idealized kernel on a finite arena (Coupling A adds ignitions; §3.2), so the threshold that matters is a finite-size one, and it is measured (§4.3). We do not measure the critical exponents: the lock's decision record notes that their asymptotic regime is out of reach at L = 64." The exponent sentence goes with item 3 (class A, C1); the front-speed clause says what the High level rests on (C1_verification.md:303-304). Pass 3, RM-13: the pointer for Coupling A is §5.1, where Definition 5 is, not §3.2 |
| 21 | 4.2 Severity as phase | framing | kept (demo 04:27) |
| 22 | Definition 4 (Severity regimes). Fix the arena side $L$. | docs/theory_foundations.md:239-241 | kept (demo 04:29) |
| 23 | Severity levels are defined by the position of the implemented kernel relative to its measured critical point $\hat\beta_c$, through the correlation length $\xi(\beta)$, the typical extent of a fire cluster: | docs/theory_foundations.md:241-243; docs/theory_foundations.md:245-250 | edited: "the typical extent of a fire cluster" glosses ξ where it is used, without claiming finiteness, since Corollary 1 no longer defines it (stub; N7); the gloss follows TF's own use (local clusters at Low, arena-scale cascades at Medium); Open items W3-F10 |
| 24 | Low, subcritical, $\xi(\beta) \ll L$: fire clusters are local and short-lived, and survival is a local-avoidance problem. | docs/theory_foundations.md:245-246 | kept (demo 04:31) |
| 25 | Medium, near-critical, $\xi(\beta) \sim L$: cluster sizes are scale-free up to the arena's size, fluctuations are maximal, and a single ignition can, with non-negligible probability, cascade to arena scale; survival is a global-anticipation problem. | docs/theory_foundations.md:247-250 | kept (demo 04:32); class C, N8 and P3-N8: "fluctuations are maximal" kept as the theory doc's term (Q23); "maximal unpredictability" and "most interesting behavior" stay out of the definition, as in the demo |
| 26 | High, supercritical: fire fronts move at a speed comparable to the agents', and survival is a race. | docs/theory_foundations.md:253-254; DX-6 | edited; class A, C1: demo "fire fronts propagate at a speed v(β) > 0 comparable to the agents' speed". The scalar v(β) goes (C1_verification.md:305); the speed meant is the one measured on the arena (§4.3) |
| 27 | The correlation length motivates the levels; operationally, each level is the observable band it was locked to, that is, fixed on 2026-07-19, before the main experiment (§4.3). | DX-201; severity_lock.md:25-31; paper/v2/FINDINGS.md:76; DX-401; DES-12 | new; class C, N8: the one clause FINDINGS.md's default adds (the levels were locked by observable bands; ξ is motivation). The wording of "phases" and "fluctuations" is Q23. Pass 3, RC1-28 (class A, F5; BRIEF.md §5.2 "lock, locked"): "locked" is defined at its first prose use as fixed on 2026-07-19 (DX-401), before the main experiment (the grid began 2026-09-09, DES-12) |
| 28 | As qualitatively different phases of one kernel, the levels make training at Low and High and evaluating at Medium (§9.1) a test of transfer to a phase neither arm trained in, though in the scalar $\beta$ it remains an interpolation (§10). | docs/theory_foundations.md:256-262; che/configs/p6_iso.yaml:13; che/configs/p6_joint.yaml:36-37 | edited: demo 04:35 "The three levels are qualitatively different phases of one kernel, so the question 'why these three?' has a principled answer, and training at Low and High while evaluating at Medium (§9.1) asks for transfer to a phase that neither arm trained in. In the scalar β it remains an interpolation (§10)." "Principled answer" cut (P3-§6); "qualitatively different phases" kept (class C, N8, Q23) |
| 29 | Definition 4 also carried an expectation, on record before its test (§4.4), that per-episode outcome variance would peak at Medium. | docs/theory_foundations.md:247-252; che/bench/results/phase3/def4_variance.md:7 | edited: demo 04:35 "When Definition 4 was written it also carried an expectation: that survival at Medium would be least predictable and the most interesting behaviour would appear there, put on record as the prediction that per-episode outcome variance peaks at Medium. That is a prediction, not part of the definition, and §4.4 reports its test." Shortened (LEN; P3-§6, antithesis); demo 04:55's "The prediction was on record before its re-test" is folded in here |
| 30 | 4.3 Measuring the threshold and locking the levels | framing | kept (demo 04:37) |
| 31 | The calibration ran the fire alone on an all-Fuel grid at $L \in \{32, 48, 64\}$, with 512 seeds per $(L, \beta)$. | DX-7 | kept (demo 04:39, reworded) |
| 32 | A span sweep over 35 values of $\beta$ (0.05 to 0.95 coarsely, 0.40 to 0.60 in steps of 0.01), each from one centre ignition for $T_{\max} = 4L$ steps, measured $P_{\mathrm{span}}$, the burnt fraction and the front speed. | DX-7; che/bench/results/phase2/calibration_report.md:4-8 | edited: "the mean burnt fraction" → "the burnt fraction"; "from a single centre ignition" → "from one centre ignition" |
| 33 | A crossing sweep ignited the full left column and recorded the left–right crossing probability $R_L(\beta)$. | DX-7; che/bench/results/phase2/calibration_report.md:8-10 | edited: "whose curves for different L cross near the threshold" cut (LEN) |
| 34 | The severity lock fixed $\hat\beta_c = 0.500 \pm 0.005$, from logistic fits to $R_L$ with centres 0.4985, 0.5006 and 0.4999 at $L = 32, 48, 64$, and a self-duality check $R_L(0.500) = 0.488, 0.502, 0.494$. | CAL-1; CAL-2; severity_lock.md:7-16 | kept (demo 04:41) |
| 35 | The lock record states that they were recomputed independently from the committed raw data; no committed script or artifact produces the logistic centres. | severity_lock.md:3-5; CAL-1 | edited (shortened); the O-2 caveat (CAL-1 note) is kept. Class C, P3-A3: the demo's order is kept, the lock record's value first (Q19) |
| 36 | Among the committed estimators, pairwise crossings of $R_L$ average 0.504; the family spans [0.480, 0.513], with consensus mean 0.499. | CAL-1; DX-204; che/bench/results/phase2/calibration_report.md:18-26 | edited: demo 04:41 "The committed estimators give a slightly wider picture: pairwise crossings of R_L average 0.504, and the calibration report's estimators span [0.480, 0.513], with consensus mean 0.499." shortened (LEN) |
| 37 | Their range brackets Kesten's ½. | DX-204; che/bench/results/phase2/calibration_report.md:26-28 | edited: demo 04:41 "Together they bracket Kesten's ½." Pass 3, RC1-30: one estimate cannot bracket a value; "Their range brackets Kesten's ½." (the range [0.480, 0.513], DX-204) |
| 38 | That agreement validates the implementation; it is not a finding about fire, since Proposition 2 and Corollary 1 predict it for this kernel. | severity_lock.md:18-20; framing | kept (demo 04:41): the stub's honesty line, and this section's one contrast. The next demo sentence, "A slow CPU test re-checks the sigmoid and a fixed threshold band around ½ (che/tests/test_percolation.py).", is cut (LEN; the stub made it optional) |
| 39 | Each level was then locked to an observable band, with its measured values ($L = 64$, 512 seeds, no agents): | DX-201; DX-7; severity_lock.md:25 | edited: demo 04:43 "The levels were then fixed by observables, each required to fall in a band, and locked with their measured values (calibration at L = 64, 512 seeds, no agents):" shortened (LEN) |
| 40 | level / $\beta$ / phase / $P_{\mathrm{span}}$ / burnt fraction / band the level was locked to | framing | kept (demo 04:45) |
| 41 | Low / 0.43 / subcritical / 0.021 / 1.9 % / $P_{\mathrm{span}} < 0.05$ and burnt fraction in [1, 5] % | CAL-3; DX-201 | kept (demo 04:47) |
| 42 | Medium / 0.49 / near-critical / 0.547 / 19.8 % / $P_{\mathrm{span}}$ in [0.3, 0.7] | CAL-3; DX-201 | kept (demo 04:48) |
| 43 | High / 0.70 / supercritical / 0.998 / 98.3 % / front speed in [0.5, 1.0] cells per step, measured 0.83 | CAL-3; DX-201; DX-6 | kept (demo 04:49; "cells/step" → "cells per step") |
| 44 | At High the front moves at 83 % of the agents' speed of one cell per step; escape is possible in principle. | DX-6; severity_lock.md:31; severity_lock.md:36-37 | edited: demo 04:51 "At High the front moves at 0.83 cells per step, 83 % of the agents' speed of one cell per step: it can be outrun, barely, and nearly the whole arena eventually burns." The 0.83 (in the table) and the burnt share (98.3 %, in the table) are not repeated (LEN). Pass 3, RC1-30 and RC1-38: "so it can be outrun, barely" (an aphoristic flourish) → "escape is possible in principle", the lock record's own words (severity_lock.md:36-37) |
| 45 | Medium sits between the finite-size pseudo-critical point $\beta_c(64) \approx 0.486$, where $P_{\mathrm{span}} = 1/2$ at $L = 64$, and $\hat\beta_c$. | CAL-4; severity_lock.md:30 | edited: "in the arena's near-critical regime" cut (LEN) |
| 46 | It is the severity of the held-out evaluation configuration of §9, $\theta^* = (\beta, \kappa_A, \kappa_B, \delta)$ = (0.49, 0.06, 1.0, 1.0); the compositional test trains at Low and High only. | CAL-3; CA-1; CB-1; COM-6; che/configs/theta_star_holdout.yaml:57; che/configs/p6_iso.yaml:13 | kept (demo 04:51, two sentences joined) |
| 47 | 4.4 Re-testing the Medium prediction | framing | kept (demo 04:53) |
| 48 | The calibration-phase probe at $d_p = 0.5$ (the fire alone, 500 updates, three seeds per severity) had saved no checkpoints. | ENV-1; DX-203; che/bench/results/phase3/def4_variance.md:5; che/bench/results/phase2/phase2_report.md:27-30 | edited: demo 04:55's "That probe had saved no checkpoints" leads, so the sentence order follows what happened; "The prediction was on record before its re-test" moved to §4.2 (row 29); "Its outcome has three parts:" cut (P3-§6, announced enumeration) |
| 49 | The re-test at fixed policy re-ran it from the same configurations and seeds (equivalent, not bitwise identical) and evaluated each final checkpoint on 512 episodes. | DX-203; che/bench/results/phase3/def4_variance.md:3-5 | edited; F5: "(M3.0)" dropped, the study named "the re-test at fixed policy"; demo 04:55 reworded |
| 50 | For survival the prediction is refuted: per-episode variance at fixed policy is monotone in severity, 0.00091, 0.00709 and 0.00885 at Low, Medium and High. | CAL-5; che/bench/results/phase3/def4_variance.md:106 | edited: demo list item "*Survival: refuted.* The per-episode variance at fixed policy is monotone in severity, 0.00091, 0.00709 and 0.00885 at Low, Medium and High, highest at High." made a sentence (P3-§6, list-ification); "highest at High" cut (monotone says it) |
| 51 | For completion it is not confirmed: Medium and Low tie within bootstrap intervals, 0.01245 against 0.01235, both above High. | DX-8; che/bench/results/phase3/def4_variance.md:107 | edited: demo list item "*Completion: not confirmed.* Medium and Low tie within their bootstrap intervals, 0.01245 against 0.01235, both above High." made a sentence |
| 52 | The environment-level mechanism is confirmed: with no agents, the burnt fraction's variance peaks near $\beta \approx 0.53$, just above Medium, and ranks Medium above High above Low at the locked levels. | DX-8; che/bench/results/phase3/def4_variance.md:108 | edited: demo list item "*Environment-level mechanism: confirmed.* With no agents, the variance of the burnt fraction peaks near β ≈ 0.53, inside the near-critical window just above the Medium level, and at the three locked levels it ranks Medium above High above Low." made a sentence; "inside the near-critical window" cut |
| 53 | The re-test report offers an account it did not test: outcome variance is roughly the environment's variance, which peaks near criticality, times the policy's sensitivity to it, which grows with severity. | che/bench/results/phase3/def4_variance.md:102 | edited; LEN (the stub: one sentence, labelled as the re-test report's account): demo 04:61 "The re-test report offers an account of the mismatch, not a separate test of it: outcome variance is roughly the environment's variance times the policy's sensitivity to it, and while the first factor peaks near criticality, the second grows with severity: at Low a trained policy absorbs the fire's fluctuations at the survival ceiling, and at High every realization couples into deaths and lost food." |
| 54 | The refutation is scoped to survival, for these fire-only policies at this budget; §10 states what siting the held-out test at Medium costs. | CAL-5; DX-203; framing | edited: demo 04:61 "What the re-test establishes is narrower. Among the three levels the fire's own outcome varies most at Medium, a property of the environment; trained policies' survival does not, which refutes the prediction for survival, for these fire-only policies at this budget. What siting the held-out test at Medium costs is stated in §10." The restatement is cut (LEN); the scope and the pointer are kept |

## Alternates

- `sections/alt/04_severity.no_item4.md` (owner question Q4g): identical to
  this section except Corollary 1, which keeps only the critical point (no
  supercritical item, no `garet2004chemical`), is retitled "(Critical
  point)", and whose scope sentence reads "It concerns" for "Both items
  concern". It is built from the same body file, so the two stay in step.
  This section (with the item) is the default that `FINDINGS.md` C1 and Q4g
  name; nothing in the design depends on the item.

## Open items

New findings made while writing, and what could not be sourced. Class B items
are applied with the demo's wording quoted in the row; class C items are not
applied.

- **W3-F6, record (C1, N7; class C, Q4k and Q4l).** TF:217-225 tags
  Corollary 1 [CITED] while items 3 and 4 cite nothing; TF:227-232 calls the
  transition and the divergence of χ and ξ "universal" without a source;
  TF:253 gives the High level "speed $v(\beta) > 0$" as one scalar; and
  `severity_lock.md:22-23` still says "asymptotic γ = 43/18 not reachable at
  L = 64" (REC-2). v2 departs on all four (rows 14–20, 26). Not edited.
- **W3-F7, citation level (N7, N15; class B, applied).** kesten1980 is
  verified at the level of its title only (`citations/theory_cites.md:98-107`),
  so demo item 2 (almost-sure finiteness below β_c, finite χ, exponential
  tails, finite ξ) has no verified source and is cut entirely. If the owner
  wants any of it back, a source must be verified through
  `related_work_verification.md` first. The one claim v2 makes below the
  title's level, positive probability of indefinite spread above β_c, rests
  on Garet & Marchand's setup, whose conditional measure divides by that
  probability (RWV:1072-1076); the alternate drops it with the item.
- **W3-F8, derivation in a cited statement (class C).** Row 16's "the cells
  ignited by step n are those within n open edges of the origin" is the
  step-2 reviewer's induction from Definition 3 and Proposition 2's coupling
  (`citations/C1_verification.md:187-198`; Cox & Durrett 1988, p. 174, state
  the same identification, not in the bibliography). Nothing in the paper
  proves it. Direction: one sentence after Proposition 2's proof in
  Appendix A (W6), or the owner accepts it as a one-line consequence.
- **W3-F9, wording (N8, P3-N8; class C, Q23).** Definition 4 keeps the theory
  doc's "fluctuations are maximal" at Medium and "qualitatively different
  phases", although the burnt-fraction variance peaks near β ≈ 0.53 (DX-8)
  and percolation has two phases and a critical point. v2 adds the clause
  that the levels are operationally the locked bands (row 27) and says no
  more; the terms are the owner's to change.
- **W3-F10, definition (class C).** ξ is glossed as "the typical extent of a
  fire cluster" (row 23), a gloss of how TF:245-250 uses it, because
  Corollary 1 no longer defines it. Owner to confirm the wording; no source
  defines it for the paper.
- **W3-F11, figure (P2-1; class B, applied; Q11).** The printed companion's
  subtitle is cut before "δ 0"; the caption states δ 0 (row 7). A label fix
  needs a rebuild (Q11).
- **Budget.** Prose is 786 words after the pass-3 fixes, 12 % over the 700
  target; the alternate is 706. The excess is the supercritical item at its verified wording (about
  80 words), which the default keeps.
- **No new ledger rows for §4.** Every number carries a canonical-ledger or
  supplement tag (the pass-3 date tag reuses DX-401).

### Pass 3 (review of draft1): owner items

The full disposition is in `paper/v2/review/resolutions_W3.md`.

- **RN1-16, OWNER (class C).** Numerals that describe cited works carry no
  tag: "(Kesten, 1980)", "(Garet & Marchand, 2004; their Corollary 5.4)". Each
  is verified in the citation records the rows name. Direction: an owner rule
  exempting them.
- **RC1-39, RC2-4 and RM-12 (W6's App. A line "Corollary 1(3)").** No change
  is needed here: §4.1 states only items 1 and 2 and does not mention the
  dropped exponent item, so App. A's fix stands on its own.
