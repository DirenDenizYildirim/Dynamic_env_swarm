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
| 3 | Before the main training runs, we pre-registered a test of whether a policy must meet stressors together in training to cope with them together at test time, with its possible outcomes, a framing of the paper for each and a falsifier: in the registration's words, "the claim the paper makes, as a function of the confirmatory outcome". | DES-12; phase6_framing_branches.md:15-16 (the quotation); phase6_framing_branches.md:101-104, :160-167 | new: §6.1 (a) per the stub; the fact of registration without its date (V3-S2; checks/dates_allow.txt); quotation from PFB:15-16 as the stub allows |
| 4 | After the result was known, the paper's emphasis moved from that claim to the environment. | X4-5; decision log, PAPER V3 (docs/decision_log.md:6158-6169), item 3 | new: the framing-change disclosure, V3-F5 home (C14); OWNER-PENDING wording |
| 5 | The registered framings remain the record of the original plan (Appendix D), and §6.3 reports every registered reading as registered. | decision log, PAPER V3 (docs/decision_log.md:6166-6169); phase6_framing_branches.md:101-104 | new: V3-F5 (registered branches stay the record of the original framing; every reading reported as registered) |
| 6 | The test was sited where composition is weak. | CB-9; COM-4; phase6_framing_branches.md:245-260 | new: C01 home, the central limitation (V3-F6); stated as a fact of the siting, not the professor's phrase (BRIEF §4, PAPER V3 item 1 not a ruling) |
| 7 | At the test severity, Coupling B's own survival effect was within a three-seed spread, not a measured floor (§4.3), and communication denial had no detectable effect (§4.4), so little beyond Coupling A was under test. | CB-9 (note: graded against a 3-seed σ_seed, not a measured floor); COM-4; paper/v3/BRIEF.md:483-484 | new: C34 short form (one sentence allowed in 06) with BRIEF §9.2 trap 6; COM-4 by pointer to §4.4; 'little beyond Coupling A was under test' is W4's wording of PFB:248-252 ('which is not the same as both producing behavioural effects there') |
| 8 | The registration stated this in advance as a limitation of every outcome; a post hoc interaction check measures it (§6.4). | phase6_framing_branches.md:245-260 ('Required on A, B and C alike'); paper/v3/sections/08_interaction_check.md (the check, §6.4) | new: C01 (registered in advance as a limitation of every outcome; the post hoc check measures it); C26 post hoc label in the sentence; the branch letters of the registered phrase not quoted (terms.txt) |
| 9 | 6.2 Design | framing | new (stub heading) |
| 10 | The isolated arm (ISO) trains on configurations with one stressor on at a time and the joint arm (JOINT) with every stressor on, both at β = 0.43 and 0.70, one shared-parameter IPPO policy per training seed. | CAL-3; ENV-11; dewitt2020ippo; paper/related_work_verification.md (dewitt2020ippo entry, as v2 used it at paper/v2/sections/09_compositional_test.md:46) | edited from paper/v2/sections/01_introduction.md:38 ('An isolated arm (ISO) trains one policy on single-stressor configurations ...'): merged with the IPPO clause of paper/v2/sections/09_compositional_test.md:46 |
| 11 | Both are evaluated at θ\, the held-out test configuration: every stressor on at β = 0.49, which neither arm saw. | CAL-3; CA-1; CB-1; COM-6 | edited from paper/v2/sections/01_introduction.md:38 and paper/v2/sections/09_compositional_test.md:38: θ* named 'the held-out test configuration' (BRIEF §5.2); 'near-critical' dropped (defined in §4) |
| 12 | Architecture, hyperparameters, evaluation draw and compute (1000 updates) are matched, so Γ is read at matched compute and nothing is claimed about convergence. | DES-13; DX-2; decision log, T* RULING (docs/decision_log.md:2977-2984) | edited from paper/v2/sections/01_introduction.md:38 ('Architecture, hyperparameters, evaluation draw and compute (1000 updates) are matched') and paper/v2/sections/09_compositional_test.md:48 ('Γ is read at matched compute ... convergence is claimed nowhere'): C11 home; worded 'nothing is claimed about convergence' because terms.txt bans 'at convergence' |
| 13 | The gap Γ, JOINT's mean minus ISO's at θ\, is tested on two co-primary outcomes, completion and survival, Šidák-corrected for m = 2; these two tests are the confirmatory family. | DES-13; decision log, FINAL FIVE entry (docs/decision_log.md:1655), co-primaries (DES-12) | edited from paper/v2/sections/01_introduction.md:38 and paper/v2/sections/09_compositional_test.md:48: Def. 8 in words (stub); the confirmatory family defined (BRIEF §5.2) |
| 14 | We ran 72 seeds per arm, above the registered cap of 60, a recorded deviation made before unblinding, the first computation of any outcome contrast (Appendix D). | DES-3; DES-1; decision log, LADDER BRANCH C, AND THE CAP RAISED 60 → 72 (docs/decision_log.md:4616-4623) | kept from paper/v2/sections/01_introduction.md:38 ('We ran 72 seeds per arm, above the registered cap of 60, a recorded deviation made before unblinding'), with v2's unblinding definition (paper/v2/sections/01_introduction.md:38) attached; C09 home |
| 15 | Every interval is conditional on the one registered evaluation draw (512 episodes, evaluation seed 0). | DES-13; phase6_framing_branches.md:262-265 (§4b) | edited from paper/v2/sections/09_compositional_test.md:48 ('every interval is conditional on the one evaluation draw') and :46 ('seed 0 × 512 episodes'): C12 home |
| 16 | Let $\mu_A$ and $\mu_B$ be the per-coupling frequencies, the shares of training episodes in which each coupling is on, and p the co-occurrence, the share with both on. | DES-7; DES-14; paper/v3/BRIEF.md:176-177 (glossary: μ, p) | edited from paper/v2/sections/09_compositional_test.md:38 ('μ is the per-coupling frequency ... and p the co-occurrence'): μ_A, μ_B as the identity needs (V3-F4) |
| 17 | The active share is the share with at least one behaviourally active stressor, and the fire-only share ν is the rest. | DES-14 (scope note: active share); DES-8; paper/v3/BRIEF.md:178-179 | edited from paper/v2/sections/09_compositional_test.md:38: ν named here (glossary) |
| 18 | JOINT sees each coupling three times as often as ISO, so Γ mixes frequency with co-occurrence. | DES-7 | edited from paper/v2/sections/09_compositional_test.md:52 ('JOINT sees each coupling three times as often as ISO, so Γ mixes per-coupling frequency with composition'): 'composition' made 'co-occurrence' (V3-F4 vocabulary); C07 home |
| 19 | Counting communication denial as inert (§4.4), the active share equals $\mu_A + \mu_B - p$: 1/3 + 1/3 − 0 = 2/3 for ISO and 1 + 1 − 1 = 1 for JOINT (Figure 6). | X4-1; DES-7; DES-14; decision log, §7 PROPOSALS RULING (docs/decision_log.md:3977-3980), δ counted inert | new: the identity with each arm's values (V3-F4; C08 home; row X4-1) |
| 20 | No contrast in this design moves co-occurrence alone. | X4-1; DES-9; paper/v3/BRIEF.md:461-466 (§9.2 trap 2) | new: the identity's consequence (stub 6.2 (b); C08) |
| 21 | One design error inflates Γ. | DES-8; DES-15; decision log, §7 PROPOSALS RULING (docs/decision_log.md:3977-3982), proposal 0 item 2 ('the bias inflates Γ') | edited from paper/v2/sections/09_compositional_test.md:54 ('The registered design contains an error, and the bias it creates inflates Γ'): C10 home, owned plainly (BRIEF §7) |
| 22 | Communication denial had already been found inert and was left out of the secondary sweeps for that reason, yet ISO kept two δ-only components of six, so a third of its training episodes are fire-only, and the design did not count them. | V6-2; V6-3; DES-16; DES-8; phase6_design_v2.md:129-131 | edited from paper/v2/sections/09_compositional_test.md:54: dates removed (V3-S2; BRIEF §7.1); 'did not count' kept (BRIEF §7.1) |
| 23 | A review of the registered design identified the bias before the main training runs. | V6-1; docs/venue_review_2026-08-16.md:11-14, :112-163 | edited from paper/v2/sections/09_compositional_test.md:54 ('A review of the registered design identified this on 2026-08-16, before the grid'): date removed (V3-S2); 'the grid' made 'the main training runs' (glossary); OWNER-PENDING A1(ii) attribution |
| 24 | We registered it, its direction and a correcting arm with its reading rule before unblinding, while those runs were under way. | DES-15; decision log, §7 PROPOSALS RULING (docs/decision_log.md:3902-3913) | edited from paper/v2/sections/09_compositional_test.md:54: dates and '120 of 252' moved to Appendix D (V3-S2); 'registered before unblinding' wording (BRIEF §7) |
| 25 | That arm, ISO-4, is ISO without its δ-only components (active share 1/2 + 1/2 − 0 = 1), a sensitivity arm outside the confirmatory family with 20 seeds. | DES-15; X4-1; DES-14; DES-13 (K_SECONDARY 20) | edited from paper/v2/sections/09_compositional_test.md:46 ('ISO-4, a sensitivity arm outside the confirmatory family, is ISO without its two δ-only components'): ISO-4's identity value added (X4-1) |
| 26 | The corrected gap is Γ₄ = JOINT − ISO-4, and B̂ = ISO-4 − ISO. | DES-15; RES-6; RES-7 | edited from paper/v2/sections/09_compositional_test.md:46 (Γ₄) and BRIEF §5.2 (B̂ defined here per WRITERS §3); 'reported without a test' left to §6.3 (C20 home) |
| 27 | ISO's Coupling-A-only and Coupling-B-only components and all of ISO-4 train with links intact (δ = 0), while JOINT trains and θ\ tests at δ = 1. | X4-2 | new: the δ train/test facts (BRIEF §9.2 trap 3; row X4-2) |
| 28 | This train/test mismatch is harmless only if δ is inert, the premise in question; the post hoc interaction check (§6.4) holds δ at 1 and cannot address it. | X4-2; COM-4; che/bench/results/phase6/post_v3_interaction/PLAN.md (conditions hold δ = 1.0; BRIEF §8.3) | new: C04 home ('mismatch'); C26 post hoc label in the sentence |
| 29 | Bias (b), the registered caveat on how completion drifts differently in the two arms over the last 100 training updates, reverses sign on the grid GPU, the GPU that ran the main training runs; no direction is claimed (Appendix D). | DES-10; decision log, T* RULING (docs/decision_log.md:3018-3021), the drift as a local sensitivity estimate; V6-4 | edited from paper/v2/sections/09_compositional_test.md:56 ('Bias (b) is the registered caveat on differential drift ... The sign reverses on the grid GPU, and no direction is claimed'): one sentence (stub 6.2 (e)); the registered string 'reverses sign on the grid GPU' (PR:124; C13 home); readings moved to Appendix D; OWNER-PENDING V3Q21 |
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
