# Provenance: sections/06_example_design.md

Writer: W4 (Paper v3, step 4, 2026-10-14). Checked against the section on 2026-10-14.
`log` = `docs/decision_log.md`; `PFB` = `phase6_framing_branches.md`. v2 sources
are `paper/v2/sections/09_compositional_test.md` (§9.1) and
`paper/v2/sections/01_introduction.md` (the arms paragraph).

Word counts (`paper/v3/src/wordcount.py`): see the hand-back; budget 500 prose,
caption 50.

| # | sentence (verbatim) | support | change from v2, and why |
|---|---|---|---|
| 1 | 6 Worked example: training on stressors together or apart | framing | kept (stub heading, STRUCTURE §2) |
| 2 | 6.1 What was registered, and what changed | framing | new (stub heading) |
| 3 | Before the main training runs, we pre-registered the test, its outcomes, a framing for each, and a falsifier. | DES-12; phase6_framing_branches.md:15-16, :101-104, :160-167 | edited (fix round, RM-1): the quotation of PFB:15-16 cut for the page ceiling; the fact of registration without its date (V3-S2) |
| 4 | After the result was known, the paper's emphasis moved from the test to the environment. | X4-5; decision log, PAPER V3 (docs/decision_log.md:6158-6169), item 3 | new: V3-F5 home (C14); fix round, RM-1: 'from that claim' made 'from the test' (antecedent cut); OWNER-PENDING wording |
| 5 | The registered framings remain the record of the original plan (Appendix D). | decision log, PAPER V3 (docs/decision_log.md:6166-6169); phase6_framing_branches.md:101-104 | new: V3-F5; fix round, RM-1: the clause on §6.3 cut |
| 6 | The test was sited where composition is weak. | CB-9; COM-4; phase6_framing_branches.md:245-260 | new: C01 home, the central limitation (V3-F6); stated as a fact of the siting, not the professor's phrase (BRIEF §4, PAPER V3 item 1 not a ruling) |
| 7 | At the test severity, Coupling B's survival effect in calibration was within a three-seed spread, not a measured floor (§4.3), and communication denial had no detectable effect (§4.4), so the test point may have offered little composition. | CB-9 (note: graded against a 3-seed σ_seed, not a measured floor); COM-4; paper/v3/BRIEF.md:483-484 | fix round, RC2-1 (MUST): 'so little beyond Coupling A was under test' replaced; RN2-3: three-seed tagged; final pass: RC2-22(a), 'calibrated survival effect' made 'survival effect in calibration' |
| 8 | The registration stated the Coupling-B half in advance, for every outcome: that both couplings meet their fixed-value criteria at Medium "is not the same as both producing behavioural effects there". | phase6_framing_branches.md:248-256 (§4a: 'Medium was chosen because both couplings clear their lock criteria there … which is not the same as both producing behavioural effects there') | fix round, RC2-1 (MUST): only the Coupling-B half credited, PFB quoted verbatim; final pass: RC2-22(b), 'here' made 'at Medium' (the quotation unchanged) |
| 9 | A post hoc interaction check measures this (§6.4). | paper/v3/sections/08_interaction_check.md (§6.4); che/bench/results/phase6/post_v3_interaction/PLAN.md:91-97 (I), :105-111 (main effects) | fix round, RC2-1: 'measures this' replaces the pre-judging clause; C26 post hoc label in the sentence. Support re-pointed to the amended plan (2026-10-17) |
| 10 | 6.2 Design | framing | new (stub heading) |
| 11 | The isolated arm (ISO) trains on configurations with one stressor on at a time and the joint arm (JOINT) with every stressor on, both at β = 0.43 and 0.70 with one shared-parameter IPPO policy per seed. | CAL-3; ENV-11; dewitt2020ippo; paper/related_work_verification.md (dewitt2020ippo entry, as v2 used it at paper/v2/sections/09_compositional_test.md:46) | edited from paper/v2/sections/01_introduction.md:38, merged with the IPPO clause of paper/v2/sections/09_compositional_test.md:46; fix round, RM-1: shortened |
| 12 | Both are evaluated at θ\, the held-out test configuration: every stressor on at β = 0.49. | CAL-3; CA-1; CB-1; COM-6 | edited from paper/v2/sections/01_introduction.md:38 and paper/v2/sections/09_compositional_test.md:38; fix round, RM-1: 'which neither arm saw' cut (the held-out status is in 'held-out') |
| 13 | Architecture, hyperparameters, evaluation draw and compute (1000 updates) are matched: Γ is read at matched compute, with no claim about convergence. | DES-13; DX-2; decision log, T* RULING (docs/decision_log.md:2977-2984) | edited from paper/v2/sections/01_introduction.md:38 and paper/v2/sections/09_compositional_test.md:48: C11 home; terms.txt bans 'at convergence'; fix round, RM-1: shortened |
| 14 | The gap Γ, JOINT's mean minus ISO's at θ\, is tested on two co-primaries, completion and survival, Šidák-corrected for m = 2: the confirmatory family. | DES-13; decision log, FINAL FIVE entry (docs/decision_log.md:1655); DES-12 (co-primaries) | edited from paper/v2/sections/01_introduction.md:38 and paper/v2/sections/09_compositional_test.md:48: Def. 8 in words; the confirmatory family defined; fix round, RM-1: shortened |
| 15 | We ran 72 seeds per arm, above the registered cap of 60, a recorded deviation made before unblinding. | DES-3; DES-1; decision log, LADDER BRANCH C, AND THE CAP RAISED 60 → 72 (docs/decision_log.md:4616-4625) | kept from paper/v2/sections/01_introduction.md:38; C09 home; fix round, RC2-16: unblinding's definition removed (it is defined at its first use in §1); RM-1: '(Appendix D)' cut |
| 16 | Every interval is conditional on the one registered evaluation draw. | DES-13; phase6_framing_branches.md:262-265 (§4b) | edited from paper/v2/sections/09_compositional_test.md:48: C12 home; fix round, RM-1: '512 episodes, evaluation seed 0' cut (stated in §6.4 and Appendix G) |
| 17 | Let $\mu_A$ and $\mu_B$ be the per-coupling frequencies, the shares of episodes with each coupling on, and $p$ the co-occurrence, the share with both. | DES-7; DES-14; paper/v3/BRIEF.md:176-177 | edited from paper/v2/sections/09_compositional_test.md:38; fix round, RM-11: $p$ typeset as math; RM-1: shortened |
| 18 | The active share is the share with at least one behaviourally active stressor; the fire-only share $\nu$ is the rest. | DES-14 (scope note: active share); DES-8; paper/v3/BRIEF.md:178-179 | edited from paper/v2/sections/09_compositional_test.md:38; fix round, RM-11: $\nu$ typeset as math |
| 19 | JOINT sees each coupling three times as often as ISO, so Γ mixes frequency with co-occurrence. | DES-7 | edited from paper/v2/sections/09_compositional_test.md:52 ('JOINT sees each coupling three times as often as ISO, so Γ mixes per-coupling frequency with composition'): 'composition' made 'co-occurrence' (V3-F4 vocabulary); C07 home |
| 20 | With communication denial inert (§4.4), the active share equals $\mu_A + \mu_B - p$: 2/3 for ISO and 1 for JOINT (Figure 6). | X4-1; DES-14; decision log, §7 PROPOSALS RULING (docs/decision_log.md:3977-3980) | new: the identity with each arm's values (C08 home; X4-1); fix round, RM-1: the arithmetic left to row X4-1, the values kept |
| 21 | No contrast in this design moves co-occurrence alone. | X4-1; DES-9; paper/v3/BRIEF.md:461-466 (§9.2 trap 2) | new: the identity's consequence (stub 6.2 (b); C08) |
| 22 | One design error inflates Γ. | DES-8; DES-15; decision log, §7 PROPOSALS RULING (docs/decision_log.md:3977-3982), proposal 0 item 2 ('the bias inflates Γ') | edited from paper/v2/sections/09_compositional_test.md:54 ('The registered design contains an error, and the bias it creates inflates Γ'): C10 home, owned plainly (BRIEF §7) |
| 23 | Communication denial had been found inert and so was left out of the secondary sweeps, yet ISO kept two δ-only components of six: a third of ISO's training episodes are fire-only, and the design did not count them. | V6-2; V6-3; DES-16; DES-8; phase6_design_v2.md:129-131 | edited from paper/v2/sections/09_compositional_test.md:54; fix round, RM-1: merged and shortened; agent of 'kept' corrected to ISO |
| 24 | A review of the registered design found the bias before the main runs; it was registered with its direction and a correcting arm during them, before unblinding. | V6-1; DES-15; docs/venue_review_2026-08-16.md:11-14, :112-163; docs/decision_log.md:3902-3913 | edited from paper/v2/sections/09_compositional_test.md:54; fix round, RM-1; final pass: 'during them, before unblinding' (budget); OWNER-PENDING A1(ii) |
| 25 | That arm, ISO-4, is ISO without its δ-only components (active share 1), a sensitivity arm outside the confirmatory family with 20 seeds. | DES-15; X4-1; DES-14; DES-13 (K_SECONDARY 20) | edited from paper/v2/sections/09_compositional_test.md:46; fix round, RM-1: ISO-4's arithmetic left to X4-1 |
| 26 | Γ₄ = JOINT − ISO-4 is the corrected gap; B̂ = ISO-4 − ISO. | DES-15; RES-6; RES-7 | edited from paper/v2/sections/09_compositional_test.md:46; final pass: RM-1 (page ceiling), word order tightened to keep the file at budget after RC2-22 |
| 27 | ISO's single-coupling components and all of ISO-4 train with links intact (δ = 0), while JOINT trains and θ\ tests at δ = 1. | X4-2 | new (BRIEF §9.2 trap 3); fix round, RM-1: 'Coupling-A-only and Coupling-B-only' made 'single-coupling' |
| 28 | This train/test mismatch is harmless only if δ is inert; a fifth condition of the post hoc interaction check measures what opening the links does to every trained policy at θ\ (§6.4). | X4-2; COM-4; che/bench/results/phase6/post_v3_interaction/PLAN.md:31-34, :49, :98-104 (the links-open condition and D, for all 164 policies); decision log, PLAN AMENDMENT (docs/decision_log.md:6436), item 4 | new: C04 home; C26 label; fix round, RM-1: 'the premise in question' cut. Amended 2026-10-17 (PLAN AMENDMENT item 4): 'holds δ at 1 and cannot address it' → 'a fifth condition … measures what opening the links does' |
| 29 | Bias (b), the registered caveat on differential completion drift in the last 100 updates, reverses sign on the grid GPU (the main runs' GPU), so no direction is claimed (Appendix D). | DES-10; decision log, T* RULING (docs/decision_log.md:3018-3021); V6-4 | edited from paper/v2/sections/09_compositional_test.md:56; registered string kept (C13 home); fix round, RM-1: shortened; OWNER-PENDING V3Q21 |
| 30 | Training mixtures of ISO, ISO-4 and JOINT by episode type | framing | kept (v2 iframe title, paper/v2/sections/01_introduction.md:30) |
| 31 | Figure 6. Each bar splits one arm's training mixture into episode types: Coupling A only, Coupling B only, both together, and fire-only. | DES-7; DES-8; DES-14; paper/figures/interactive/MANIFEST.md:223-231 | edited from v2 Figure 2's caption (paper/v2/sections/01_introduction.md:31): 'What each arm trained on' dropped; numbers left to the figure (V3-S4) |
| 32 | Beneath each bar are each coupling's frequency (labelled “per-stressor marginal” on the figure) and the active share. | DES-7; DES-14; paper/figures/interactive/MANIFEST.md:223-231 | kept from v2 Figure 2's caption; the printed label glossed once (V3-S3) |
| 33 | Count δ-only episodes as inert or nominally; split by β. | paper/figures/interactive/MANIFEST.md:226-228 | edited: v2's status line and 'Interact:' list cut to the interact span (V3-S4; BRIEF §9.4); the toggle's printed wording is not quoted, because its phrase is C02's detection pattern, homed in §4.4 |
| 34 | Stacked bars of the three training mixtures by episode type, with each arm's per-coupling frequencies and the share of episodes that carry an active stressor. | framing | kept (v2 alt text, paper/v2/sections/01_introduction.md:35) |
| 35 | Static companion of Figure 6 for the printed PDF. | framing | edited: Figure 2 → Figure 6 |

## Findings

- [record] STRUCTURE §4 row 6 asks Figure 6's caption to gloss the toggle's
  printed label "δ inert under a frozen random-projection encoder at this
  scale". That phrase is C02's detection pattern (`checks/caveats.yaml`, home
  `04_calibration.md`), and the caveat check does not exempt glosses, so the
  gloss would fail the one-home check in 06. The caption describes the toggle
  instead ("count δ-only episodes as inert or nominally"), as v2 did. Direction:
  B1/B2 decide whether the gloss exemption should extend to caveats.
- [record] The label "bias (b)" has no definition in the registration
  documents or the decision log that W4 could find (grep of
  `phase6_design_v2.md`, `phase6_framing_branches.md`, `docs/`); it lives in
  the ledger (DES-10's "what" column), `writing_session_prompt.md:150` and the
  v2/v3 briefs. The caveat itself is registered (T* RULING, log:3018-3021). The
  sentence keeps the label (V3Q21 default) and says what it is.
- [style] Budget: prose is over the stub's 500 words (see hand-back); every
  required item of the STUB-SPEC is present, and the overage is the design
  error, the mismatch and the identity, which the stub makes homes here.

## Alternates

None.
