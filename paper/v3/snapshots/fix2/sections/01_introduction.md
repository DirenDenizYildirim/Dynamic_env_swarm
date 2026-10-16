<!-- PAPER V3 DRAFT (PAPER V3 ruling, 2026-10-12): builder-drafted, not owner-approved -->

## 1 Introduction

<!-- STUB-SPEC
JOB: Pose the question an environment must make testable; introduce CHE in one paragraph (its properties, with pointers to §3 and §4); state the worked example and its result in one paragraph with the registered strings and the size; state the limitations in front (V3-F6); list three contributions.
WRITER: W1.
BUDGET: 600 prose words.
FROM: P1 §4.2 §1 and §5.3; P3 §2.2 and §1.4; V3-F1, V3-F3, V3-F6.
ORDER:
  - the question (stressors meet a policy together or apart; why an environment must make this testable); ecology and compound events as the analogy; zero-shot generalization; Gao et al. as the closest earlier study
  - CHE in a paragraph: pure JAX, multi-agent, fire every episode, Coupling A, Coupling B, communication denial, ambient hazard (Def. 2: the reward reads task variables and deaths, never the fire), severity by a measured threshold, exact nested ablations, theory checked as tests, the floors protocol (pointers §3–§5)
  - the worked example: define "worked example"; the test in one sentence; the result with the strings; the size (about a tenth of an agent per episode, only at updates 900 to 1000, X4-3, RES-12); the inert-share correction; one clause owning the design error (§6.2); one HOLE sentence for the check
  - limitations in front, three short sentences: (1) sited where composition is weak, short form, pointer §6.1; (2) the δ "inert" label is coarse and applied asymmetrically, and ISO and ISO-4 trained with links intact while the test configuration denies them (pointers §4.4, §6.2); (3) one algorithm, one map, 12 agents, no heuristic baselines, one held-out point (THIS is the home)
  - three contributions: (1) CHE and its code; (2) what calibration found (the fuel-limited 4.8-fold fall, short; smoke's High cost, descriptive, short); (3) the worked example and its lesson (no advice here; pointer §6.5)
ROWS: ENV-1, ENV-6, ENV-11, CAL-3, CA-4, CB-5, COM-4, RES-1, RES-2, RES-6, RES-11, RES-12, X4-3, CB-9, DES-8, DES-14, X4-2 (W4).
CITATIONS: crain2008stressors, cote2016stressors, zscheischler2018compound, zscheischler2020typology (analogy); kirk2023zsg; gao2024composition (only what v2 BRIEF §15 permits); haksar2018; garcia2015safe; dewitt2020ippo. Permitted uses: v2 BRIEF §15.
REGISTERED STRINGS: "does not survive the inert-share correction"; "sign unstable over the final half"; "excludes a joint-training gain larger than 0.66 points"; "at matched compute". "Pre-registered" only for the test; no registration date.
CAVEATS HOMED HERE (state each in full, once; the detection pattern, from checks/caveats.yaml, must match your home sentence):
  C05 one_algorithm_one_map_twelve_agents: One algorithm (shared-parameter IPPO), one map (64 × 64), 12 agents, one held-out point, no heuristic baselines. Pattern: (?i)\bone (learning )?algorithm\b
SHORT FORMS ALLOWED HERE (at most one sentence each; the full statement is at the home):
  C01 sited_where_composition_is_weak (home 06_example_design.md)
  C02 delta_inert_ruled_phrase (home 04_calibration.md)
  C03 delta_label_asymmetric (home 04_calibration.md)
  C04 delta_train_test_mismatch (home 06_example_design.md)
  C10 inert_third_design_error (home 06_example_design.md)
  C11 matched_compute_never_convergence (home 06_example_design.md)
  C16 sign_unstable_final_half (home 07_example_results.md)
  C17 completion_exclusion_bound (home 07_example_results.md)
  C18 inert_share_correction (home 07_example_results.md)
  C27 cannot_isolate_co_occurrence (home 09_example_lesson.md)
  C32 fuel_limited_fall (home 04_calibration.md)
  C33 smoke_high_descriptive (home 04_calibration.md)
  C34 coupling_b_medium_measurement (home 04_calibration.md)
EVERY OTHER CAVEAT in checks/caveats.yaml: pointer only ("§6.3", "Appendix D"), never restated. C26: any sentence about the interaction check carries "post hoc".
HOLES:
  - one sentence: the interaction check's pooled result in short form, labelled post hoc (pointer §6.4).
NOT HERE: any date; the framing change (its homes are §6.1 and Appendix D, V3-F5); JOINT's 3× or 2× frequencies (homes §6.2, §6.3); the identity (home §6.2); advice or "therefore"; "first" or "novel" without the search caveat; study codes; Proposition 4; Remark 1.
V2 MATERIAL: paper/v2/sections/01_introduction.md (sentences may be reused where still true; mark them in provenance).
DEPENDENCIES: §6.1 holds the full siting limitation; §4.4 the inert label and its asymmetry; §6.2 the mismatch and the design error; §6.3 the result; §6.5 the lesson.
-->

When a training distribution has to cover several stressors, its designer chooses whether the policy meets them together or one at a time. Ecology studies the interactive and cumulative effects of multiple stressors <d-cite key="crain2008stressors,cote2016stressors"></d-cite>, and climate science the risk from compound events <d-cite key="zscheischler2018compound,zscheischler2020typology"></d-cite>. In reinforcement learning the choice is a question of zero-shot generalization <d-cite key="kirk2023zsg"></d-cite>: must a policy see stressors co-occur in training to cope with their co-occurrence at test time? Gao et al. (2024) <d-cite key="gao2024composition"></d-cite> studied it for imitation-learned manipulation.

The Compound Hostile Environment (CHE), written in pure JAX, makes the question testable in multi-agent reinforcement learning (Figure 1). A cellular-automaton fire burns in every episode, at severities placed below, near and above a measured percolation threshold (§4.1). Two stressors are coupled to the fire: structural collapse can seed ignitions (Coupling A), and smoke attenuates each agent's observation by Beer–Lambert transmittance (Coupling B); a third, communication denial, is independent (§3.2). The fire is an ambient hazard: the reward never reads it and prices every death the same (§3.3). Switching a stressor off reproduces the environment without it bit for bit under the same random keys, and unit tests check the code against closed forms (§3.4). Section 5 describes how we measure the spread of identical reruns.

We use CHE for a worked example, a test registered before the main training runs. It compares a policy trained with every stressor on (the joint arm, JOINT) with one trained on each in isolation (the isolated arm, ISO), at matched compute, at a near-critical configuration neither arm trained on (§6.2). Joint training raises survival by 0.96<!-- N:RES-2 --> percentage points (Šidák-corrected 95 %<!-- N:DES-13 --> CI [+0.47, +1.44]<!-- N:RES-2 -->), about a tenth<!-- N:X4-3 --> of an agent per episode (0.11<!-- N:X4-3 --> of 12<!-- N:ENV-6 --> agents), detectable only in the last fifth<!-- N:RES-12 --> of training (the checkpoints at updates 900 to 1000<!-- N:RES-12 -->). The completion difference shows no detectable change and excludes a joint-training gain larger than 0.66<!-- N:RES-1 --> points. Both differences are sign unstable over the final half of training (§6.3). The survival gain does not survive the inert-share correction. A third<!-- N:DES-8 --> of the isolated arm's training episodes carried only communication denial; against an arm trained without them, joint training shows no detectable survival difference (§6.3). Keeping them was a design error, found before the main training runs; a correcting arm outside the pre-registered test was registered before unblinding, that is, before any outcome contrast was computed (§6.2).

The test was sited where composition is weak: at its severity, Coupling B's own survival effect in calibration was within a three-seed<!-- N:CB-9 --> spread, and communication denial had no detectable effect (§6.1). A post hoc interaction check at the test configuration measures whether the two couplings' effects on trained policies add (§6.4).<!-- HOLE:INTERACTION --><!-- fills (fix round, RC1-9, RM-8): extend the sentence before this marker in place with the check's pooled reading per PLAN §7, labelled post hoc, e.g. "… add: <reading> (§6.4)"; about 13 words of room are left under the 600-word budget --> Communication denial is labelled inert under a frozen random-projection encoder at this scale; the label rests on coarse acceptance thresholds and is applied asymmetrically across stressors (§4.4). The isolated arm and its corrected version trained every episode that contained a coupling with links intact, while the test configuration denies every link, a train/test mismatch (§6.2). Every learned policy comes from one algorithm, shared-parameter independent PPO <d-cite key="dewitt2020ippo"></d-cite>, on one 64 × 64<!-- N:ENV-6 --> map with 12<!-- N:ENV-6 --> agents; the worked example has one held-out test point and no heuristic baseline.

Our contributions are:

1. CHE and its code (§3, §8).
2. What calibration found: under policies trained for 500<!-- N:DX-40 --> updates, collapse-seeded ignitions fall 4.8-fold<!-- N:CA-4 --> from low to high severity, and, descriptively, smoke lowers survival at high severity in 3 of 3<!-- N:CB-5 --> contrasts (§4).
3. The worked example and its lesson: matching the share of training with an active stressor cannot by itself isolate co-occurrence (§6.5).
