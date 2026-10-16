---
layout: distill
title: 'A multi-agent fire environment with exact stressor ablations'
description: 'A pure-JAX multi-agent environment in which collapse seeds fire, smoke attenuates perception and every stressor switches off exactly, with a pre-registered test as a worked example.'
date: 2026-10-11
htmlwidgets: true
authors:
  - name: Anonymous
    affiliations:
      name: Anonymous
bibliography: submission.bib
toc:
  - name: "1 Introduction"
  - name: "2 Related work"
  - name: "3 The environment"
  - name: "4 What each stressor does"
  - name: "5 Measurement protocol"
  - name: "6 Worked example: training on stressors together or apart"
  - name: "7 Limitations and scope"
  - name: "8 Using CHE and reproducing the paper"
  - name: "9 Conclusion"
  - name: "Appendices"
_styles: >-
  .print-companion { display: none; } @media print { .print-companion { display: block; } d-article figure iframe { display: none; } .interact { display: none; } } d-article div.highlighter-rouge pre { font-size: 12px; line-height: 1.5; white-space: pre; overflow-x: auto; } d-article div.highlighter-rouge pre code { font-size: inherit; white-space: inherit; } @media (min-width: 1000px) { d-article > div.highlighter-rouge { grid-column: page; } } @media print { d-article div.highlighter-rouge pre { white-space: pre-wrap; overflow-wrap: anywhere; overflow-x: visible; } } d-article mjx-container[display="true"] { overflow-x: auto; overflow-y: hidden; max-width: 100%; } @media print { d-article > table, d-article > span:has(> mjx-container[display="true"]), d-article > div.highlighter-rouge { grid-column: page; } d-article table { display: table; overflow: visible; width: 100%; table-layout: auto; } d-article table th, d-article table td { font-size: 10px; line-height: 1.35; padding: 1px 4px; overflow-wrap: break-word; } d-article table code { white-space: normal; overflow-wrap: anywhere; font-size: 9px; } d-article mjx-container[display="true"] { overflow: visible !important; } d-article div.highlighter-rouge pre { font-size: 9px; } } d-article iframe[src$="/explorer_thetastar_random_seed0.html"], d-article iframe[src$="/explorer_thetastar_iso_s1_T1000_ep0.html"], d-article iframe[src$="/explorer_thetastar_joint_s1_T1000_ep0.html"] { height: 1360px !important; } @media (min-width: 768px) { d-article iframe[src$="/explorer_thetastar_random_seed0.html"], d-article iframe[src$="/explorer_thetastar_iso_s1_T1000_ep0.html"], d-article iframe[src$="/explorer_thetastar_joint_s1_T1000_ep0.html"] { height: 1248px !important; } } @media (min-width: 1000px) { d-article iframe[src$="/explorer_thetastar_random_seed0.html"], d-article iframe[src$="/explorer_thetastar_iso_s1_T1000_ep0.html"], d-article iframe[src$="/explorer_thetastar_joint_s1_T1000_ep0.html"] { height: 764px !important; } } @media (min-width: 1180px) { d-article iframe[src$="/explorer_thetastar_random_seed0.html"], d-article iframe[src$="/explorer_thetastar_iso_s1_T1000_ep0.html"], d-article iframe[src$="/explorer_thetastar_joint_s1_T1000_ep0.html"] { height: 700px !important; } } d-article p.caption { font-size: 13px; line-height: 1.5; color: rgba(0, 0, 0, 0.6); } d-article table { display: block; overflow-x: auto; }
---

<!-- PAPER V3 DRAFT (PAPER V3 ruling, 2026-10-12): builder-drafted, not owner-approved -->

<!-- STUB-SPEC
JOB: One question, one result, one lesson (V3-F2; PROF 4). Body text before the hero, no heading.
WRITER: W1 (also front_matter.yaml title and description; title candidates and description in provenance/00_abstract.md).
BUDGET: at most 250 prose words, comments excluded (P1 §3; P3 §2.2; BLIND §6 item 7).
FROM: P1 §3.1 (moves), §3.2 (description), §3.3 (lesson templates); P3 §2.2; PAPER V3 item 3.
ORDER:
  - (1) The environment, 2 or 3 sentences: CHE, pure JAX, multi-agent; a cellular-automaton fire in every episode; collapse seeds fire (Coupling A); smoke attenuates perception by Beer–Lambert transmittance (Coupling B); communication denial independent; the reward never reads the fire and prices every death the same; severity placed relative to a measured percolation threshold; switching a stressor off reproduces the nested model bit for bit; the code is supplied. Rows: ENV-1, ENV-6, CAL-3 (no calibration number is needed).
  - (2) The question, 1 sentence: as a worked example, a pre-registered test of whether training one policy on co-occurring stressors beats training it on each in isolation, at matched compute, at a held-out near-critical severity. Rows: DES-13, CAL-3.
  - (3) The result, 2 or 3 sentences, registered strings verbatim: survival up 0.96 points with its Šidák-corrected CI (RES-2), about a tenth of an agent per episode (X4-3), only at the end of training (RES-12); it does not survive the inert-share correction (RES-6), which removes the third of isolated training that carried no active stressor, a design error registered with its correction before unblinding (DES-8, DES-15); completion excludes a joint-training gain larger than 0.66 points (RES-1); both differences are sign unstable over the final half (RES-11). The 72-seed deviation is not needed here.
  - (4) The lesson, 1 or 2 sentences, labelled post hoc where it uses the check (HOLE). Any advice is its own labelled sentence, never after therefore, so or thus.
ROWS: ENV-1, ENV-6, CAL-3, DES-8, DES-13, DES-15, RES-1, RES-2, RES-6, RES-11, RES-12, X4-3 (W4 writes it; cite the ID), IC-* (orchestrator, after step 0.5).
REGISTERED STRINGS: "does not survive the inert-share correction"; "sign unstable over the final half"; "excludes a joint-training gain larger than 0.66 points"; "at matched compute". "Null" at most an informal gloss (log:6166), never the result's name.
SHORT FORMS ALLOWED HERE (at most one sentence each; the full statement is at the home):
  C01 sited_where_composition_is_weak (home 06_example_design.md)
  C02 delta_inert_ruled_phrase (home 04_calibration.md)
  C08 active_share_identity (home 06_example_design.md)
  C10 inert_third_design_error (home 06_example_design.md)
  C11 matched_compute_never_convergence (home 06_example_design.md)
  C15 secondary_non_verdict_bearing (home 07_example_results.md)
  C16 sign_unstable_final_half (home 07_example_results.md)
  C17 completion_exclusion_bound (home 07_example_results.md)
  C18 inert_share_correction (home 07_example_results.md)
  C27 cannot_isolate_co_occurrence (home 09_example_lesson.md)
EVERY OTHER CAVEAT in checks/caveats.yaml: pointer only ("§6.3", "Appendix D"), never restated. C26: any sentence about the interaction check carries "post hoc".
HOLES:
  - the lesson sentence(s): pick the row of P1 §3.3 (N, Pn, Pp, M, D) that matches the check's pooled reading under PLAN §7; if the results are not back, use the identity lesson (row M without the check). V3Q7.
  - description in front_matter.yaml: recheck against the final abstract (one line, no double quote, no colon-space, no number).
OWNER-PENDING:
  - the disclosure footnote is the OWNER's (PAPER V3 item 6): leave the comment marker shown below in place, after the first sentence; write no footnote text.
  - title (V3Q1): put P1's T1 in front_matter.yaml; give 3 to 5 candidates in provenance (P1 §2: T1, T1s, T2, T3, T4), with what each leads with.
  - naming CHE in full (v2 B3 default: named).
NOT HERE: "composition effect" without the correction string; "null" as the result's name; converged, budget-robust, certified, swarm, PBT, finite Dec-POMDP, one transition kernel; "pre-registered" for the correction; study codes; any date (V3-S2); the hazard-blind reward as the lead; the professor's "mostly Coupling A" (a review, not a ruling); any interaction-check number before IC rows exist.
V2 MATERIAL: paper/v2/sections/00_abstract.md and provenance/00_abstract.md (v2's title candidates and description).
DEPENDENCIES: X4-3 (W4); IC rows (orchestrator); the lesson of 09_example_lesson.md (W5) must agree with this abstract's lesson.
-->

We present the Compound Hostile Environment (CHE), a pure-JAX multi-agent environment in which a cellular-automaton fire burns in every episode.<!-- OWNER: disclosure d-footnote here (after the first sentence; the owner writes it, PAPER V3 item 6) --><!-- OWNER-PENDING:V3Q1 title in front_matter.yaml is T5 since the final pass (shortest accurate candidate; P1's T1 and the others in provenance/00_abstract.md) --><!-- OWNER-PENDING:B3 CHE named in full in the abstract (carried v2 default) --> Collapse seeds ignitions (Coupling A), smoke attenuates perception (Coupling B) and communication denial is an independent third stressor; the reward never reads the fire. Severity is placed relative to a measured percolation threshold, switching a stressor off reproduces the environment without it bit for bit under the same random keys, and the code is supplied.

<!-- OWNER-PENDING:V3Q7 also RC1-22 / RC2-18: whether a short form of the siting limitation (C01) enters the abstract, here or in the post-check lesson -->
As a worked example, a pre-registered test asks whether one policy trained on co-occurring stressors beats one trained on each in isolation, at matched compute and a held-out near-critical severity. Joint training raises survival by 0.96<!-- N:RES-2 --> percentage points (Šidák-corrected 95 %<!-- N:DES-13 --> CI [+0.47, +1.44]<!-- N:RES-2 -->), about a tenth<!-- N:X4-3 --> of an agent per episode, detectable only in the last fifth<!-- N:RES-12 --> of training. The survival gain does not survive the inert-share correction. The correction trains an isolated arm without the third<!-- N:DES-8 --> of episodes whose only stressor, communication denial, had no detectable effect in calibration, matching the joint arm's share of training with an active stressor. Keeping that third was our design error; we registered the correction, outside the pre-registered test, before any outcome contrast was computed. The completion difference excludes a joint-training gain larger than 0.66<!-- N:RES-1 --> points. Both differences are sign unstable over the final half of training.

<!-- HOLE:INTERACTION -->
<!-- OWNER-PENDING:V3Q7 -->
<!-- fills: the check's pooled reading, one sentence labelled post hoc (P1 §3.3; PLAN §7), placed before the lesson below; room is left for it (fix round, RM-1: the abstract is held at 242 words after the final pass, so a sentence of up to 8 words fits under 250; a longer one needs the lesson shortened). Keep, extend or replace the identity lesson below per V3Q7; §6.5 (W5) must state the same lesson. -->
Because the share of training with an active stressor equals the couplings' frequencies summed, less their co-occurrence ($\mu_A + \mu_B - p$), matching it alone cannot isolate co-occurrence.

<!-- PAPER V3 DRAFT (PAPER V3 ruling, 2026-10-12): builder-drafted, not owner-approved -->

<!-- STUB-SPEC
JOB: The environment before any claim: one random-policy episode of CHE under the abstract (OPENING item 2), then one reading-note sentence saying what "illustrative" means.
WRITER: W1.
BUDGET: caption at most 60 words; reading note at most 30 words.
FROM: P2 §3 #1 (environment-first strengthens the v2 default); P2 §8 (the hero's limit lives in the reading note); V3-S4.
ROWS: ENV-6, ENV-13 (selection rule), DX-33 (only if a count from this episode is stated: 11 collapse events, 7 collapse-seeded ignitions).
FIGURES: Figure 1, explorer_thetastar_random_seed0.html, companion explorer_thetastar_random_seed0_static.png. Caption says what it shows: the map is environment state (fire, smoke field, weak and collapsed floor, food, agents, collapse-seeded ignitions); one selected agent's three panels are perception (its observation as masked by smoke, the true state of those cells, the transmittance). Gloss once: labelled “obs v3” on the figure. Operating instructions go in a span with class interact (hidden in print).
REGISTERED STRINGS: "illustrative" (SUBMISSION FORMAT constraint 2: animations illustrate, never grade).
CAVEATS HOMED HERE (state each in full, once; the detection pattern, from checks/caveats.yaml, must match your home sentence):
  C39 hero_illustrative: The hero episode is illustrative - one random-policy episode, selected by a fixed rule. Pattern: (?i)\billustrative\b
EVERY OTHER CAVEAT in checks/caveats.yaml: pointer only ("§6.3", "Appendix D"), never restated. C26: any sentence about the interaction check carries "post hoc".
NOT HERE: any alive count, completion or return of this episode; any comparison or effect; calling the map's smoke what agents see; the hover readouts of ρ and τ as numbers; deep links; "grades nothing" (banned).
V2 MATERIAL: paper/v2/sections/00_hero.md.
-->

<!-- FIGURE 1: block carried from paper/v2/sections/00_hero.md:16 (markup, iframe height and alt text as v2 had them); caption replaced; the writer checks the alt text -->

<figure class="l-page">
  <iframe src="{{ 'assets/html/submission/explorer_thetastar_random_seed0.html' | relative_url }}" width="100%" height="700" style="border:none" title="Episode explorer: one random-policy episode of CHE at the test configuration" loading="lazy"></iframe>
  <figcaption><strong>Figure 1.</strong> One random-policy episode at the test configuration of §6. The map shows environment state: fire, smoke, weak and collapsed floor, food, agents and collapse-seeded ignitions. One agent's panels show its observation as masked by smoke (labelled “obs v3” on the figure), those cells' true state and the smoke transmittance. <span class="interact">Play, scrub, jump between events, toggle layers or pick an agent.</span></figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/explorer_thetastar_random_seed0_static.png" class="img-fluid" alt="Three map frames of one random-policy episode, at its start, middle and end, showing fire state, smoke density, weak and collapsed floor, collapse-seeded ignitions, food and agents, with one selected agent's observation, the true state of the same cells, and the probability that each cell was seen." caption="Static companion of Figure 1 for the printed PDF." %}
</div>

Figure 1 is illustrative: it shows one random-policy episode, chosen by a rule fixed before rendering, to explain the environment, and no result in this paper is read from it.

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

We use CHE for a worked example, a test registered before the main training runs. It compares a policy trained with every stressor on (the joint arm, JOINT) with one trained on each in isolation (the isolated arm, ISO), at matched compute, at a near-critical configuration neither arm trained on (§6.2). Joint training raises survival by 0.96<!-- N:RES-2 --> percentage points (Šidák-corrected 95 %<!-- N:DES-13 --> CI [+0.47, +1.44]<!-- N:RES-2 -->), about a tenth<!-- N:X4-3 --> of an agent per episode (0.11<!-- N:X4-3 --> of 12<!-- N:ENV-6 --> agents), detectable only in the last fifth<!-- N:RES-12 --> of training (the checkpoints at updates 900 to 1000<!-- N:RES-12 -->). Completion shows no detectable change, and the difference excludes a joint-training gain larger than 0.66<!-- N:RES-1 --> points. Both differences are sign unstable over the final half of training (§6.3). The survival gain does not survive the inert-share correction. A third<!-- N:DES-8 --> of the isolated arm's training episodes carried only communication denial; against an arm trained without them, joint training shows no detectable survival difference (§6.3). Keeping them was a design error, found before the main training runs; a correcting arm outside the pre-registered test was registered before unblinding, that is, before any outcome contrast was computed (§6.2).

The test was sited where composition is weak: at its severity, Coupling B's own survival effect in calibration was within a three-seed<!-- N:CB-9 --> spread, and communication denial had no detectable effect (§6.1). A post hoc interaction check at the test configuration measures whether the two couplings' effects on trained policies add (§6.4).<!-- HOLE:INTERACTION --><!-- fills (fix round, RC1-9, RM-8): extend the sentence before this marker in place with the check's pooled reading per PLAN §7, labelled post hoc, e.g. "… add: <reading> (§6.4)"; about 13 words of room are left under the 600-word budget --> Communication denial is labelled inert under a frozen random-projection encoder at this scale; the label rests on coarse acceptance thresholds and is applied asymmetrically across stressors (§4.4). The isolated arm and its corrected version trained every episode that contained a coupling with links intact, while the test configuration denies every link, a train/test mismatch (§6.2). Every learned policy comes from one algorithm, shared-parameter independent PPO <d-cite key="dewitt2020ippo"></d-cite>, on one 64 × 64<!-- N:ENV-6 --> map with 12<!-- N:ENV-6 --> agents; the worked example has one held-out test point and no heuristic baseline.

Our contributions are:

1. CHE and its code (§3, §8).
2. What calibration found: under policies trained for 500<!-- N:DX-40 --> updates, collapse-seeded ignitions fall 4.8-fold<!-- N:CA-4 --> from low to high severity, and, descriptively, smoke lowers survival at high severity in 3 of 3<!-- N:CB-5 --> contrasts (§4).
3. The worked example and its lesson: matching the share of training with an active stressor cannot by itself isolate co-occurrence (§6.5).

<!-- PAPER V3 DRAFT (PAPER V3 ruling, 2026-10-12): builder-drafted, not owner-approved -->

## 2 Related work

<!-- STUB-SPEC
JOB: Place CHE: where the hazard sits in comparable environments (the task, a cost or constraint, or ambient); JAX and multi-agent environments; compositional generalization and co-occurring perturbations. One sentence on how the search ran (detail in Appendix I).
WRITER: W3.
BUDGET: 400 prose words plus a compact Table 1 (at most 120 words in cells).
FROM: P1 §4.2 §2; P3 §2.2 (v2 §2 cut by about two thirds).
ROWS: DX-101 (the search; Appendix I).
CITATIONS: only keys in v3's submission.bib, characterized only as RWV Part 3 records (v2 BRIEF §15): haksar2018, garcia2015safe, rutherford2024jaxmarl, alomari2025macraftax, hinckeldey2025assistax, tao2025pobax, bettini2024benchmarl, hafner2022crafter, matthews2024craftax, cakir2025jaxwildfire, liu2026vulcan, raut2026psps, tobin2017dr, muratore2022drreview, dennis2020paired, jiang2021plr, jiang2021robustplr, parkerholder2022accel, mendez2022composuite, keysers2020, erdem2025mixed, agrawal2023multimodal, tramer2019multiple, hsiung2023compositional, chen2022understandingdr, gao2024composition, kirk2023zsg, hu2025adaptablemarl. No new citation (V3Q17).
REGISTERED STRINGS: none required here.
EVERY OTHER CAVEAT in checks/caveats.yaml: pointer only ("§6.3", "Appendix D"), never restated. C26: any sentence about the interaction check carries "post hoc".
OWNER-PENDING:
  - v2 C1 (READS RULING item 2): six of the owner's §2 sentences were changed for accuracy in v2; reuse v2's accurate text and keep the provenance flag.
NOT HERE: Safety Gym, Safety-Gymnasium, Melting Pot or RL evaluation-methodology works (unverified, V3Q17); "every arm is perturbed throughout"; Erdem & Üre "do better"; JaxMARL compatibility; DBCA describing the ISO/JOINT endpoints (it describes the sweep only).
V2 MATERIAL: paper/v2/sections/02_related_work.md and provenance/02_related_work.md (its Open items).
DEPENDENCIES: §1 states the question; §6.2 states what the comparison holds fixed.
-->

**Table 1.** Where the hazard enters the learning or planning problem.

| work | agents and method | where the hazard enters |
|---|---|---|
| Haksar & Schwager (2018) <d-cite key="haksar2018"></d-cite> | aerial agents; multi-agent deep Q-network | **the task**: a reward for moving to burning boundary trees; agents have no damage state |
| JaxWildfire (Çakır et al., 2025) <d-cite key="cakir2025jaxwildfire"></d-cite> | one air-tanker agent; JAX simulator | **the reward**: a penalty proportional to the number of burning cells; agent harm not described |
| safe reinforcement learning (García & Fernández, 2015) <d-cite key="garcia2015safe"></d-cite> | maximizing return under safety constraints | **a constraint or a cost**, typically |
| VULCAN (Liu & Yan, 2026) <d-cite key="liu2026vulcan"></d-cite> | proposed fire search and rescue, planned by a vision-language model | **a hazard cost map** of smoke, heat and sensing uncertainty |
| CHE (this paper) | 12<!-- N:ENV-6 --> agents; independent PPO | **ambient**: transition and observation kernels only; the reward prices each death at $d_p = 0.5$<!-- N:ENV-1 -->, whatever its cause |

For Coupling A, the nearest neighbour we found is Raut et al. (2026) <d-cite key="raut2026psps"></d-cite>, a single-agent model of public-safety power shutoffs in which power flows resulting from the operator's switching set the failure probability of lines in wildfire areas, treated as ignition risk. <!-- OWNER-PENDING:v2C1 (carried v2 question C1 / Q4a: READS RULING item 2 recorded the owner's section 2 as final; this sentence keeps v2's accuracy fix OI-4 of the "about seven percent" sentence; DISPOSITIONS §5 gives C1 no V3Q number) -->In CHE, ignition is not an action available to the agents, though where they stand changes collapse rates (§3.2). For Coupling B, VULCAN degrades simulated sensing with smoke but has no transmittance model, and JaxWildfire's observations are partial but not attenuated. Our search found no reinforcement-learning environment whose observation kernel attenuates by transmittance. Among the JAX multi-agent benchmarks we surveyed, JaxMARL <d-cite key="rutherford2024jaxmarl"></d-cite>, Multi-Agent Craftax <d-cite key="alomari2025macraftax"></d-cite> and Assistax <d-cite key="hinckeldey2025assistax"></d-cite>, none has an evolving, spreading lethal hazard field or perception attenuated by a hazard.

Domain randomization and unsupervised environment design ask which distribution to train on, the latter adaptively <d-cite key="tobin2017dr,muratore2022drreview,dennis2020paired,jiang2021plr,jiang2021robustplr,parkerholder2022accel"></d-cite>; our worked example compares fixed distributions on a held-out configuration, a zero-shot generalization test <d-cite key="kirk2023zsg"></d-cite>, and evaluates no adaptive curriculum.

The closest earlier study of our question is Gao et al. (2024) <d-cite key="gao2024composition"></d-cite>, who ask, in visual imitation learning for robotic manipulation, whether policies compose environmental factors to succeed on unseen combinations. <!-- OWNER-PENDING:v2C1 (as above: v2's accuracy fix RC1-24 of the owner's "the strategy that covers more combinations does better"; RWV Part 3) -->Comparing data-collection strategies, they find that policies do compose and that a strategy cycling through factors, so that more combinations appear, is generally the most effective; their design, built for data efficiency, does not separate co-occurrence from how often each factor value appears. The DBCA method <d-cite key="keysers2020"></d-cite> builds train and test splits with similar distributions of single elements and different distributions of their combinations; our secondary sweep follows that idea, holding each coupling's frequency fixed while co-occurrence varies (Appendix F). <!-- OWNER-PENDING:v2C1 (as above: v2's accuracy fixes OI-3 of the owner's Erdem and Üre sentences) -->In robust reinforcement learning, Erdem & Üre (2025) <d-cite key="erdem2025mixed"></d-cite> report that single-agent policies trained against an adversary on one modality, observations or actions, remain vulnerable to simultaneous attacks on both (their Tables 3–4). Their attacked runs schedule no unattacked steps, and runs attacked on both modalities carry both budgets, so per-modality frequency, co-occurrence and total budget change together.

A survey of adaptability in multi-agent reinforcement learning (Hu et al., 2025, revised 2026) <d-cite key="hu2025adaptablemarl"></d-cite> calls an environment family highly diagnostic if it "systematically varies" factors such as observability or communication structure "while holding other factors fixed". It mentions compositional generalization but analyses no shift in several factors at once. Wherever we say that no work does something, we mean none found by the search of Appendix I.

<!-- PAPER V3 DRAFT (PAPER V3 ruling, 2026-10-12): builder-drafted, not owner-approved -->

## 3 The environment

<!-- STUB-SPEC
JOB: CHE is the contribution: state its parts and properties, each with the rows or code that carry them (V3-F1). 3.1 state, step order, fire and smoke; 3.2 the three stressors; 3.3 the reward; 3.4 exact nesting and theory checked as tests, with the claim table; 3.5 the instance, training, metrics and the counter.
WRITER: W2.
BUDGET: 1,050 prose words; Figure 2 caption at most 50 words; Table 2 at most 160 words in cells; four listings (56 code lines).
FROM: P1 §1.1 and §4.2 §3; P2 §2 (the claim table; listings instead of figures for the reward and the nesting); P3 §1.1 (verdicts) and §2.2 (definitions from v2 §5 to §7 move here).
ORDER:
  - 3.1 State, step order, fire and smoke: Def. 1 (state; factorized kernel; post-step observation) in at most two displays; Prop. 1 in one sentence (a well-defined Dec-POMDP whose reachable states form a finite set; proof Appendix A); the CA fire (Def. 3) and Prop. 2 in one sentence (bond percolation for the idealized kernel; grassberger1983, kesten1980); smoke outlives flame (the smoke update of Def. 3, one display); one Burning cell at reset (V3-1); Figure 2.
  - 3.2 The stressors: Coupling A (Def. 5, Listing 1; Prop. 3's linear scaling in words, checked in two runs, CA-2, CA-3); the hazard is not agent-independent (CA-8, CA-9; HOME); Coupling B (Def. 6: Beer–Lambert transmittance in the observation kernel, Listing 2); Thm. 1 in words only, as a statement true under both V3Q5 options (in a two-agent corridor toy, the value of remembering an attenuated signal is computed exactly; Appendix A); communication denial δ (Def. 7), independent, with a frozen random-projection message encoder (ENV-12, DX-17; Listing 6 is in Appendix B); θ = (β, κ_A, κ_B, δ).
  - 3.3 The reward: Def. 2 display; hazard-blind, deaths priced cause-blind at d_p = 0.5 (ENV-1); Listing 3; the two tests (test_reward_independence.py; test_lethality.py:143-162); then plainly: an agent dies only on a burning or collapsing cell, so the death price is in effect a contact price, and the d_p ablation shows it drives survival learning (ENV-2 to ENV-5, with its scope) (HOME, BLIND W7).
  - 3.4 Exact nesting and theory as tests: every stochastic branch consumes its random numbers unconditionally, so κ_A = 0, κ_B = 0 or δ = 0 reproduces the nested model bitwise under the same keys on one backend; Listing 4; the limits (the κ_A test compares fire and smoke; the δ test compares with a recorded pre-channel trajectory hash on CPU); then Table 2 (claim, listing, test, figure; about 8 rows; it is the index into the code supplement).
  - 3.5 Instance, training, metrics, counter: 64 × 64 map, 12 agents, horizon 256, 9 × 9 crop, 32 food (ENV-6); one shared-parameter IPPO policy per seed (ENV-11; dewitt2020ippo, lu2022dpo); hyperparameters in Appendix B (DX-2); budget DX-3; co-primaries completion and survival; the coupling-co-active counter counts collapse-seeded ignitions near an agent, so it is co-active only in all-on configurations (CO-4; HOME).
ROWS: ENV-1 to ENV-12, V3-1, DX-1, DX-2, DX-3, DX-17, DX-37, CA-1, CA-2, CA-3, CA-8, CA-9, CB-1, CB-4, COM-6, CO-4, DX-14 (only through Thm. 1 in words; no number needed).
CITATIONS: grassberger1983, kesten1980 (Prop. 2, identity only); dewitt2020ippo, lu2022dpo; bernstein2002 only if a worst-case class result is needed (Remark 1 is cut, so probably not).
FIGURES: Figure 2, static fig01_schematic.png (block below).
LISTINGS: Listing 1 structure.py:83-102 (3.2); Listing 2 observation.py:300-310 (3.2); Listing 3 tasks.py:31-43 (3.3); Listing 4 test_coupling_b.py:131-142 (3.4). Blocks below, byte-identical. Code comments keep their internal tags; your prose never echoes them. The 61-line step listing moved to Appendix A (STRUCTURE §11 row 14).
LATEX: Def. 1 (at most 2 displays), Def. 2, Def. 3 (fire kernel with its smoke update), Def. 5, Def. 6, Def. 7 (one display each at most; Def. 4 is in §4, Def. 8 in §6.2). No \label, \eqref, \tag, \newcommand.
REGISTERED STRINGS: "ambient hazard" (ruled term); "stressor"; "environment configuration"; "fire-only" if used.
CAVEATS HOMED HERE (state each in full, once; the detection pattern, from checks/caveats.yaml, must match your home sentence):
  C28 counter_all_on_only: The coupling-co-active counter counts collapse-seeded ignitions near an agent, so it is co-active only in all-on configurations. Pattern: (?i)\ball-on\b
  C29 death_price_contact_penalty: An agent dies only on a burning or collapsing cell, so the cause-blind death price is in effect a hazard-contact price, and it drives survival learning. Pattern: (?i)\bcontact (penalty|price)\b
  C30 hazard_not_agent_independent: The hazard is not agent-independent - an occupied weak cell collapses about nine times as often. Pattern: (?i)\bagent-independent\b
EVERY OTHER CAVEAT in checks/caveats.yaml: pointer only ("§6.3", "Appendix D"), never restated. C26: any sentence about the interaction check carries "post hoc".
NOT HERE: "finite Dec-POMDP" without "on its reachable states"; "one transition kernel" (it is "one transition or observation kernel"); Remark 1 (cut); "the formal specification"; JaxMARL compatibility; Thm. 1's v2 closed form (it does not describe the toy, BRIEF §9.2 trap 1); obs v2/v3, E2C, handshake, digest, traced (banned); PBT.
V2 MATERIAL: paper/v2/sections/03_environment.md (most of 3.1 to 3.5), 05_coupling_a.md §5.1, 06_coupling_b.md §6.1, 07_comms.md §7.1 (definitions).
DEPENDENCIES: Appendix A (W2) holds the proofs and Thm. 1's statement; §4 (W3) holds what each stressor does; §8 (W5) the API.
-->

CHE is a grid world in which a team of agents forages while a fire burns (Figure 2).

### 3.1 State, step order, fire and smoke

**Definition 1 (Compound Hostile Environment).** A CHE is a Dec-POMDP $\mathcal{M}_\theta = \langle I, \mathcal{S}, \{\mathcal{A}_i\}, T_\theta, R, \{\Omega_i\}, O_\theta, \gamma \rangle$ on a grid $G$, indexed by the *environment configuration* $\theta = (\beta, \kappa_A, \kappa_B, \delta)$ of Definitions 3, 5, 6 and 7. Its state $s = (x, h, \rho, c, k, t)$ holds the agents $x$ (positions, alive flags $\alpha_i$, task state), the fire $h \in \{\mathrm{Fuel}, \mathrm{Burning}, \mathrm{Burnt}\}^G$, the smoke $\rho \in \mathbb{R}_{\ge 0}^G$, the structure $c \in \{\mathrm{intact}, \mathrm{collapsed}\}^G$, the link graph $k$ and the step $t \le T$. The transition kernel factorizes in this order:

$$
\begin{aligned}
T_\theta(s' \mid s, a) = {} & T_C(c' \mid c, x)\; T_H^{\beta,\kappa_A}(h' \mid h, c, c')\; T_\rho(\rho' \mid \rho, h') \\
& \times T_X(x' \mid x, a, h', c')\; T_K^{\delta}(k' \mid x'),
\end{aligned}
$$

and agent $i$ observes the post-step state, $o'_i \sim O^i_{\kappa_B}(\cdot \mid x', h', \rho', c', k')$.

By Proposition 1 (Appendix A), $\mathcal{M}_\theta$ is a well-defined Dec-POMDP whose states and observations reachable within the horizon form finite sets. A constant is *locked* if it was fixed before the main experiment (values in Appendix B, dates in Appendix D).

**Definition 3 (Fire and smoke).** Each cell is Fuel, Burning or Burnt. At each step, independently for each ordered pair of a Burning cell $g$ and a Fuel von Neumann neighbour $g'$, the cell $g'$ ignites with probability $\beta$; a Burning cell is Burnt one step later, and Burnt is absorbing. Spontaneous ignition is off ($\iota = 0$<!-- N:DX-1 -->). Smoke is state, and it outlives flame: per cell,

$$
\rho' = e^{-\eta}\rho + \sigma_s \mathbf{1}[h' = \mathrm{Burning}],
$$

with $\sigma_s = 1.0$ and $\eta = 0.5$<!-- N:DX-1 --> fixed by convention, never calibrated, and no spatial smoothing.

Every episode starts from an all-Fuel grid with one<!-- N:V3-1 --> Burning cell at a uniformly random position. With Coupling A off, the cells that ever burn then form a bond-percolation cluster with edge probability $\beta$ (Proposition 2, Appendix A)<d-cite key="grassberger1983,kesten1980"></d-cite>, which §4.1 uses to place severity.

<!-- FIGURE 2: block carried from paper/v2/sections/03_environment.md:25 (include and alt text as v2 had them); caption replaced -->

{% include figure.html path="assets/img/submission/fig01_schematic.png" class="img-fluid" alt="Five numbered boxes in a row, collapse, hazard, smoke, agents and comms, with a Coupling A arrow from collapse into the hazard box, a Coupling B arrow from smoke down to an observation box drawn from the post-step state, and comms denial entering the comms box with no hazard input." caption="Figure 2. One environment step of CHE." %}

<p class="caption">Collapse, fire, smoke, agents and communication are sampled in this order. Coupling A (orange) carries c′ − c into the fire; Coupling B (blue) carries the smoke ρ′ into the observation, drawn from the post-step state. Denial δ enters the communication kernel, which reads no hazard.</p>

### 3.2 The stressors

**Definition 5 (Coupling A, as implemented).** Weak terrain $w(g) \in \{0, 1\}$ marks a clustered fraction $f_{\mathrm{weak}}$ of the cells, drawn per episode, and $o_t(g) \in \{0, 1\}$ marks at least one alive agent on cell $g$ before the step. An intact cell collapses with probability

$$
\lambda_t(g) = \big(\lambda_0 + \lambda_{\mathrm{load}}\, o_t(g)\big)\, w(g),
$$

and collapse is absorbing. Coupling A then ignites, with probability $\kappa_A$, each cell still Fuel after this step's spread within Chebyshev distance $r_A$ of a cell that collapsed in this step: the fire reads the increment $c' - c$.

<!-- LISTING 1: block carried byte-for-byte from paper/v2/sections/05_coupling_a.md:48; move it, never edit it -->

**Listing 1.** Coupling A's seeding mask: its uniforms are drawn before $\kappa_A$ is read, and it acts on $c' - c$ only.

<!-- LISTING: che/env/structure.py:83-102 -->
```python
# che/env/structure.py:83-102 (verbatim)
def coupling_a_seed_mask(
    key: jax.Array,
    collapse_increment: jax.Array,
    *,
    kappa_A: float,
    r_seed: int,
) -> jax.Array:
    """Coupling A (Def. 5): each cell in the seeding neighborhood N_A of a
    new collapse (Chebyshev radius r_seed) ignites independently w.p.
    kappa_A. `collapse_increment` is the boolean mask of c' - c, i.e. cells
    that collapsed *this step* — T_H reads the increment, not the stock.
    Returns the candidate ignition mask; `hazard.seed_ignitions` applies it
    to Fuel cells only.
    """
    chex.assert_rank(collapse_increment, 2)
    chex.assert_type(collapse_increment, jnp.bool_)
    # Invariant #3: uniforms drawn even when kappa_A == 0.
    u = jax.random.uniform(key, collapse_increment.shape)
    near_new_collapse = dilate(collapse_increment, r_seed)
    return near_new_collapse & (u < kappa_A)
```

The hazard is not agent-independent: a weak cell with an agent on it collapses nine<!-- N:CA-8 --> times as often as an empty one. Below the percolation threshold, with collapses as the fire's only source and their clusters apart, the expected burnt area grows linearly in the collapse rate (Proposition 3, checked in two<!-- N:DX-304 --> runs at parameters other than the locked ones; Appendix A).

**Definition 6 (Coupling B, as implemented).** For agent $i$ at $x_i$ and a cell $y$ of its crop,

$$
\tau_i(y) = \exp\!\big(-\kappa_B\, \lVert y - x_i \rVert_2\, \bar\rho_i(y)\big),
$$

a midpoint-rule Beer–Lambert transmittance, where $\bar\rho_i(y)$ averages $\rho'$ at four<!-- N:X2-7 --> evenly spaced points on the line of sight. Each crop cell is revealed independently with probability $\tau_i(y)$; an unrevealed cell passes zeros, and a visibility plane records the reveal. Setting $\kappa_B = 0$ gives $\tau \equiv 1$ (Listing 4, Appendix A).

Because $\rho'$ is hazard state, perception degrades where and when the fire is active.

In a corridor toy built on the same observation code, ignoring the attenuated signal costs exactly half the probability of being informed before committing, and this cost falls continuously to zero as $\kappa_B$ grows (Theorem 1, Appendix A); this concerns optimal values in the toy, not learners in CHE.

**Definition 7 (Communication denial, as implemented).** After the agents move, each directed link between alive agents $i \ne j$ opens with probability

$$
\Pr\big[\, i \to j \text{ open} \,\big] = \mathbf{1}\big[\lVert x'_i - x'_j \rVert_\infty \le R_{\mathrm{comm}}\big]\,(1 - \delta),
$$

with $R_{\mathrm{comm}} = 16$<!-- N:COM-6 --> cells. Messages $m_i \in [-1, 1]^{8}$<!-- N:DX-17 --> from a frozen, randomly initialized message head (Appendix B) arrive one step later as the mean over a receiver's open links.

$T_K$ reads positions and aliveness only, so denial is independent of the fire.

### 3.3 A hazard-blind reward

**Definition 2 (Ambient hazard).** The hazard is *ambient* if (i) the reward reads task variables and the agents' alive transition only,

$$
\begin{aligned}
R(s,a,s') = {} & R_{\mathrm{task}}(\mathrm{task}(x), a, \mathrm{task}(x')) \\
& - d_p\,\lvert\{i : \alpha_i = 1,\ \alpha'_i = 0\}\rvert ,
\end{aligned}
$$

with no term in $h$, $\rho$ or $c$ and no auxiliary cost or constraint; and (ii) $T_H$ is a fixed stochastic kernel that nothing in the environment optimizes.

In CHE the task variables are the food grid and the alive agents' positions, and each death costs $d_p = 0.5$<!-- N:ENV-1 -->, whatever its cause.

<!-- LISTING 2: block carried byte-for-byte from paper/v2/sections/03_environment.md:167 (Listing 3 in draft1; renumbered in the fix round); move it, never edit it -->

**Listing 2.** The task reward's signature admits the food and occupancy grids only.

<!-- LISTING: che/env/tasks.py:31-43 -->
```python
# che/env/tasks.py:31-43 (verbatim)
def task_step(food: jax.Array, occupancy: jax.Array) -> tuple[jax.Array, jax.Array]:
    """Collection: an occupied food cell yields +1 team reward and empties.

    Multiple agents on one food cell still collect a single item (+1).
    Returns (food', team_reward). Reads task variables and agent occupancy
    only — no hazard/smoke/structure arguments, by design (Def. 2).
    """
    chex.assert_type(food, jnp.uint8)
    chex.assert_equal_shape([food, occupancy])
    collected = (food == 1) & occupancy
    reward = collected.sum().astype(jnp.float32)
    food_new = jnp.where(collected, jnp.uint8(0), food).astype(jnp.uint8)
    return food_new, reward
```

Two tests check that the reward reads no hazard directly: states that differ only in fire, smoke or structure, with the alive transition held equal, get equal rewards, and a death by fire or by collapse changes the reward by $-d_p$.

An agent dies only on a cell that is burning or collapsing, so the cause-blind death price is in effect a hazard-contact price, and it drives survival learning. In the one ablation of $d_p$, raising it from 0<!-- N:ENV-2 --> to 0.5<!-- N:ENV-1 --> raised survival at High severity (§4.1) from 0.575 to 0.866<!-- N:ENV-2 --> (Appendix B). Survival thus enters learning as a penalized channel and completion, at +1<!-- N:ENV-9 --> per item, as a rewarded one; any asymmetry between them is read that way.

### 3.4 Exact nesting, and theory checked as tests

Each stressor is a parameter of one transition or observation kernel: setting $\kappa_A = 0$ gives a fire that ignores the structure, $\kappa_B = 0$ the observation before masking plus an all-ones visibility plane, and $\delta = 0$ free, range-limited communication.

These are nested models because every stochastic branch draws its uniforms unconditionally and compares them with a probability that may be zero. A zero therefore changes comparisons only, and the same keys reproduce the nested model's trajectory bit for bit on one backend; Listing 5 (Appendix A) is the test for $\kappa_B = 0$.

The test for $\kappa_A = 0$ compares fire and smoke only, since agents respond to collapses; the test for $\delta = 0$ matches, on the CPU, a trajectory hash recorded before the communication channel existed.

Propositions 2 and 3, Corollary 1 and Theorem 1 are exact results that the code is tested against, in toys and at parameters other than the locked ones; the paper claims no theory beyond them.

**Table 2.** Properties of CHE with the listing (3–5 in Appendix A), test (`che/tests/test_*.py`, code supplement) and figure carrying each.

| property | listing | test | fig. |
|---|---|---|---|
| step order of Definition 1 (Prop. 1) | 3 | `hazard`, `lethality` | 2 |
| fire is bond percolation; severity by measured threshold (Prop. 2, Cor. 1) | — | `percolation` | 3 |
| collapse seeds fire (Coupling A, Prop. 3) | 1 | `coupling_a`, `prop3` | 1, 4 |
| smoke attenuates perception (Coupling B, Thm. 1) | 4 | `coupling_b`, `e2c` | 1, 5 |
| communication denial reads no hazard | 3 | `comms` | — |
| hazard-blind reward, cause-blind death price (Def. 2) | 2 | `reward_independence`, `lethality` | — |
| ablations nest bitwise | 5 | `nesting`, `coupling_b`, `comms` | — |
| locked constants reachable from configurations | — | `locks` | — |
| floors per metric, GPU and artifact (§5) | — | — | C1 |

### 3.5 Instance, training and metrics

Every trained policy, and every evaluation of one, uses one instance: a 64 × 64 grid, 12 agents, a horizon of 256 steps, a 9 × 9 egocentric crop and 32 food items<!-- N:ENV-6 -->.

Each seed trains one shared-parameter actor-critic policy<!-- N:ENV-11 --> (Appendix B) with the independent PPO of de Witt et al. (2020)<d-cite key="dewitt2020ippo"></d-cite>, in the style of Lu et al. (2022)<d-cite key="lu2022dpo"></d-cite>, at 32,768<!-- N:DX-3 --> environment steps per update.

Both outcomes are per episode: *completion* is $1 - F/32$<!-- N:ENV-6 -->, with $F$ the food left at the end, and *survival* is the fraction of the 12<!-- N:ENV-6 --> agents alive at the end. Episodes always run to the horizon.

A coupling-co-active counter logs the collapse-seeded ignitions within Chebyshev radius 4<!-- N:DX-37 --> of an alive agent. Only Coupling A produces them and $\kappa_B$ does not enter the count, so it is co-active only in all-on configurations.

<!-- PAPER V3 DRAFT (PAPER V3 ruling, 2026-10-12): builder-drafted, not owner-approved -->

## 4 What each stressor does

<!-- STUB-SPEC
JOB: Say what each stressor does, at which severity, and how finely that was measured (V3-F1). 4.1 severity placed by a measured percolation threshold; 4.2 Coupling A; 4.3 Coupling B, including its Medium measurement (the siting evidence); 4.4 communication denial, the ruled inert phrase with its bars, and the asymmetry of the label.
WRITER: W3.
BUDGET: 700 prose words; Figures 3 to 5 captions at most 60 words each.
FROM: P1 §4.2 §4 and §1.1 (P-S, P-A′, P-B, P-B′, P-K); P3 §1.1 (E1, E2, E4, E10) and §1.4; P2 §3 #3 to #5.
ORDER:
  - 4.1 Def. 4 as a short list (operational definition by locked bands); lead with the committed estimators and their spread and consensus (DX-204), then the locked threshold value with its provenance caveat (CAL-1, no committed estimator; HOME); the three levels (CAL-3) and β_c(64) (CAL-4); Cor. 1 in words at v2's verified level (v2 D2 default; kesten1980, garet2004chemical); Def. 4's Medium-variance prediction refuted for survival (CAL-5, DX-8; HOME); Figure 3 (its renders are illustrative).
  - 4.2 Coupling A under trained 500-update calibration policies (DX-40): collapse-seeded ignitions fall 4.83-fold Low to High, replicated 4.92-fold (CA-4, CA-5): fuel exhaustion, first seen under random policies (DX-9; HOME of the 4.8-fold fall); the near-agent share stays flat (CA-6); the survival effect of A is not located (CA-7: 2 seeds, no floor; say so once); Figure 4.
  - 4.3 Coupling B: masking concentrates at moments of danger (CB-10, DX-11); at High, smoke's survival cost is in the same direction in 3 of 3 contrasts, descriptive and ungraded (CB-5, DX-13, CB-7; HOME); at Medium, the test's severity, its own survival effect was −0.03 points, not measurable against a three-seed spread, not a measured floor (CB-9; HOME of the measurement); Low masks 0.068 % of crop cells (DX-11). Figure 5 (gloss its printed codes; its band is a reference scale (cross-artifact), FIGURE BATCH B9).
  - 4.4 Communication denial: no effect detected at bars of 7.99 completion and 2.60 survival points from 4 seeds, about half power (COM-4, V4-1, V4-2); the content and connectivity checks (COM-2, COM-3, DX-16); hence "inert under a frozen random-projection encoder at this scale" (ruled phrase, HOME, with the bars beside it; V3Q14); then the asymmetry (HOME): the record's working definition of behaviourally active is "not found inert in calibration", which counts Coupling A at High (CA-4) and Coupling B at Low (DX-11) and Medium (CB-9) as active although each is weak there; only δ is counted inert. Invent no threshold. Remark 2′ in one sentence as a refinement of Pynadath & Tambe (READS RULING item 4; pynadath2002; statement in Appendix A; V3Q4).
ROWS: CAL-1 to CAL-5, DX-6, DX-7, DX-8, DX-201, DX-202, DX-204, CA-1, CA-4 to CA-7, DX-9, DX-40, CB-1, CB-5, CB-7, CB-9, CB-10, DX-11, DX-13, COM-2 to COM-5, DX-16, V4-1, V4-2, V4-3, ENV-6.
CITATIONS: kesten1980, garet2004chemical (Cor. 1(4) at the verified level only; v2 D2), pynadath2002 (Remark 2′ as READS RULING item 4 permits).
FIGURES: Figure 3 severity_explorer (4.1; gloss: the printed companion subtitle is clipped in print, so state the renders' κ_A 0.06, κ_B 1.0, δ 0 in the caption); Figure 4 coupling_a_explorer (4.2; gloss labelled “m44” and “m35”; its carried alt text says handshake, a banned term: reword the alt text); Figure 5 static fig04_coupling_b.png (4.3; gloss labelled “M4.4”; its legend's "floor" is a reference scale (cross-artifact)). Blocks below.
REGISTERED STRINGS: "inert under a frozen random-projection encoder at this scale" (here, in full); "reference scale (cross-artifact)"; "illustrative" for the severity renders; VOID for comms condition (iii) only if mentioned (home Appendix C).
CAVEATS HOMED HERE (state each in full, once; the detection pattern, from checks/caveats.yaml, must match your home sentence):
  C02 delta_inert_ruled_phrase: Communication denial is "inert under a frozen random-projection encoder at this scale", with the bars it rests on. Pattern: (?i)frozen random-projection
  C03 delta_label_asymmetric: The inert label rests on coarse bars and is applied asymmetrically (Coupling A at High and Coupling B at Low counted active although weak there). Pattern: (?i)\basymmetric
  C31 severity_estimator_provenance: The locked threshold value has no committed estimator; the committed estimators' spread and consensus are stated beside it. Pattern: (?i)\bcommitted estimator
  C32 fuel_limited_fall: Collapse-seeded ignitions fall about 4.8-fold from Low to High under trained (500-update calibration) policies; fuel exhaustion, first seen under random policies. Pattern: 4\.8\d?\s*×
  C33 smoke_high_descriptive: Smoke's survival cost at High - same direction in 3 of 3 contrasts; descriptive, ungraded. Pattern: \b3 of 3\b
  C34 coupling_b_medium_measurement: Coupling B's own survival effect at Medium (the test's severity) was not measurable against a three-seed spread - not a measured floor. Pattern: (?i)\bthree-seed\b
  C35 medium_variance_prediction_refuted: Def. 4's prediction that outcomes vary most at Medium is refuted for survival. Pattern: (?i)\brefuted\b
SHORT FORMS ALLOWED HERE (at most one sentence each; the full statement is at the home):
  C39 hero_illustrative (home 00_hero.md)
EVERY OTHER CAVEAT in checks/caveats.yaml: pointer only ("§6.3", "Appendix D"), never restated. C26: any sentence about the interaction check carries "post hoc".
OWNER-PENDING:
  - Remark 2′ sentence (V3Q4).
  - Cor. 1(4) (v2 D2: default stated at the Garet and Marchand level).
NOT HERE: "certified"; "as predicted before measurement"; "self-limiting" without "fuel exhaustion"; the smoke cost at High as a finding; the Low κ_B contrast (no row); "a sixth to a quarter" (contradicted by its own table); "every acceptance bar"; any m44 or m35 contrast graded against a floor; Γ, the test or its arms (those are §6); "live" (banned: say "active").
V2 MATERIAL: paper/v2/sections/04_severity.md, 05_coupling_a.md (§5.2, §5.3), 06_coupling_b.md (§6.3, §6.4), 07_comms.md (§7.2, §7.3).
DEPENDENCIES: §1 points here for the inert label and its asymmetry; §6.1 points here for the Medium measurement (one sentence allowed there); Appendix C holds the floors behind the bars; Appendix E holds the comms figure.
-->

### 4.1 Severity, placed by a measured threshold

**Definition 4 (Severity regimes).** For an arena of side $L$, let $\xi(\beta)$ be the typical extent of a fire cluster.

- *Low*, subcritical, $\xi(\beta) \ll L$: fires stay local.
- *Medium*, near-critical, $\xi(\beta) \sim L$: one ignition can cascade to the scale of the arena.
- *High*, supercritical: the fire front moves about as fast as the agents.

Operationally, each level is the observable band fixed for it before the main experiment (table). The calibration ran the fire alone on all-fuel grids (Figure 3), measuring the spanning probability: the chance that one centre ignition reaches the boundary. Three estimators shipped with the calibration data place the critical point between 0.480 and 0.513<!-- N:DX-204 -->, with consensus mean 0.499<!-- N:DX-204 -->; the value fixed for the experiment, 0.500 ± 0.005<!-- N:CAL-1 -->, comes from logistic fits that no committed estimator reproduces. <!-- OWNER-PENDING:v2D2 (carried v2 question D2: Corollary 1(4) stated at the Garet and Marchand level; DISPOSITIONS §5 gives it no V3Q number) -->On the infinite square lattice, the idealized kernel's critical point is exactly ½ (Kesten, 1980)<d-cite key="kesten1980"></d-cite>, and above it a fire that spreads indefinitely burns a region growing linearly towards a deterministic convex shape (Garet & Marchand, 2004<d-cite key="garet2004chemical"></d-cite>; Corollary 1, Appendix A). The agreement checks the implementation and says nothing new about fire.

| severity | $\beta$ | phase | spanning probability ($L = 64$<!-- N:DX-7 -->) | burnt fraction | band it was fixed to |
|---|---|---|---|---|---|
| Low | 0.43<!-- N:CAL-3 --> | subcritical | 0.021<!-- N:CAL-3 --> | 1.9 %<!-- N:CAL-3 --> | spanning below 0.05, burnt 1–5 %<!-- N:DX-201 --> |
| Medium | 0.49<!-- N:CAL-3 --> | near-critical | 0.547<!-- N:CAL-3 --> | 19.8 %<!-- N:CAL-3 --> | spanning 0.3–0.7<!-- N:DX-201 --> |
| High | 0.70<!-- N:CAL-3 --> | supercritical | 0.998<!-- N:CAL-3 --> | 98.3 %<!-- N:CAL-3 --> | front speed 0.5–1.0 cells per step<!-- N:DX-201 -->, measured 0.83<!-- N:DX-6 --> |

Medium, the test severity of §6, lies between the 64<!-- N:DX-7 -->-cell arena's pseudo-critical point, about 0.486<!-- N:CAL-4 -->, and the fixed critical point. Definition 4 also expected outcomes to vary most at Medium. Re-tested with fixed fire-only policies, that expectation is refuted for survival, whose per-episode variance rises with severity (0.00091, 0.00709, 0.00885<!-- N:CAL-5 -->).

<!-- FIGURE 3: block carried from paper/v2/sections/04_severity.md:24 (markup, iframe height and alt text as v2 had them); caption replaced; alt text edited (W3): "illustrative" dropped from the alt so that the caption holds the one allowed short form (C39) -->

<figure class="l-page">
  <iframe src="{{ 'assets/html/submission/severity_explorer.html' | relative_url }}" width="100%" height="528" style="border:none" title="Severity explorer: spanning probability against ignition probability, and one fire at each locked level" loading="lazy"></iframe>
  <figcaption><strong>Figure 3.</strong> Severity as a measured phase. Left: the spanning probability against β for sides 32, 48 and 64<!-- N:DX-7 -->; rules mark the three severities, a triangle the 64-cell arena's pseudo-critical point. Right: one illustrative random-policy episode per severity, with κ<sub>A</sub> 0.06<!-- N:CA-1 -->, κ<sub>B</sub> 1.0<!-- N:CB-1 --> and δ 0<!-- N:DX-202 -->. <span class="interact">Drag the time slider; click a panel.</span></figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/severity_explorer.png" class="img-fluid" alt="Spanning probability of a centre ignition against ignition probability for three grid sizes, with the three locked severities marked, beside one random-policy fire episode at each severity." caption="Static companion of Figure 3 for the printed PDF." %}
</div>

### 4.2 Coupling A

In the runs of the Coupling-B calibration grid with Coupling B on (500-update<!-- N:DX-40 --> policies at each severity), collapse-seeded ignitions per episode fall from 4.05 at Low and 3.41 at Medium to 0.84 at High<!-- N:CA-4 -->. This 4.83-fold<!-- N:CA-4 --> fall (from unrounded counts) is fuel exhaustion (a seed lights only unburnt fuel), first seen under random policies at about 5.7-fold<!-- N:DX-9 -->. The Coupling-A calibration grid (other policies, Coupling A off and on) replicates it at 4.92-fold<!-- N:CA-5 -->. In all nine<!-- N:CA-6 --> measured cells, the share of seeded ignitions inside an alive agent's crop stays between 0.164 and 0.203<!-- N:CA-6 --> (Figure 4). Where Coupling A costs survival most is not located: its grid's survival contrasts rest on two seeds per arm<!-- N:CA-7 -->, with no reproducibility floor (§5).

<!-- FIGURE 4: block carried from paper/v2/sections/05_coupling_a.md:23 (markup, iframe height and alt text as v2 had them); caption replaced; alt text edited (W3): "handshake" (banned term) removed -->

<figure class="l-page">
  <iframe src="{{ 'assets/html/submission/coupling_a_explorer.html' | relative_url }}" width="100%" height="736" style="border:none" title="Coupling A explorer: collapse-seeded ignitions by severity, their share near agents, and the two Proposition 3 runs" loading="lazy"></iframe>
  <figcaption><strong>Figure 4.</strong> Coupling A. Top: collapse-seeded ignitions and their share near agents, by severity, in the Coupling-B grid (labelled “m44” on the figure) and the Coupling-A grid (labelled “m35” on the figure). Bottom: the two checks of Proposition 3, the second labelled “handshake” on the figure. <span class="interact">Hover a point; table view.</span></figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/coupling_a_explorer.png" class="img-fluid" alt="Collapse-seeded ignitions per episode at three severities for two trained grids, the share of them near agents, and the two Proposition 3 runs shown separately." caption="Static companion of Figure 4 for the printed PDF." %}
</div>

### 4.3 Coupling B

In the Coupling-B grid with masking on, smoke masks 0.068 %, 0.249 % and 1.559 %<!-- N:DX-11 --> of crop cells over all alive agent-steps at Low, Medium and High, and 118, 22 and 16 times<!-- N:CB-10 --> that share at moments of danger, when a burning cell is in the crop (Figure 5(a)). At High, survival is lower with masking on than off in 3 of 3<!-- N:CB-5 --> replicate contrasts: −6.87, −10.66 and −4.70 points<!-- N:DX-13 -->. Each rests on one run per arm, two share a seed, and none has an interval, so this cost is descriptive and ungraded. The band in Figure 5(b), a High survival floor of 6.21 points<!-- N:CB-7 --> from another artifact, is a reference scale (cross-artifact): a spread from other runs, shown for scale only.

At Medium, the test severity, Coupling B's own survival effect was −0.03 points<!-- N:CB-9 -->, judged within noise against a three-seed<!-- N:CB-9 --> spread of 0.72 points<!-- N:CB-9 --> rather than a measured floor.

<!-- FIGURE 5: block carried from paper/v2/sections/06_coupling_b.md:74 (include and alt text as v2 had them); caption replaced -->

{% include figure.html path="assets/img/submission/fig04_coupling_b.png" class="img-fluid" alt="Left, the masked share of the agent crop at three severities, over all alive agent-steps and at danger moments, on a log scale. Right, three replicate survival contrasts at high severity and then the first estimate, against a hatched band one standard deviation wide on a reference scale measured on another artifact." caption="Figure 5. Coupling B: where the masking falls, and the High survival contrasts." %}

<p class="caption">(a) Masked share of the crop by severity, over all alive agent-steps and at moments of danger, in the Coupling-B grid (labelled “M4.4” on the figure). (b) The three High survival contrasts, then the first two<!-- N:DX-40 -->-seed estimate; the hatched band, labelled floor, is a reference scale (cross-artifact).</p>

### 4.4 Communication denial

In a denial study at Medium (four<!-- N:COM-4 --> seeds), opening the links (δ = 0 against δ = 1) changed completion by +0.38 points and survival by −1.43 points<!-- N:COM-4 -->. The acceptance thresholds, 7.99 and 2.60 points<!-- N:COM-4 -->, were twice<!-- N:V4-2 --> the reproducibility floor on that study's GPU (§5), and an effect as large as a threshold would clear it only about half<!-- N:V4-1 --> the time. <!-- OWNER-PENDING:V3Q14 -->We call communication denial "inert under a frozen random-projection encoder at this scale" in this sense only: no effect as large as those thresholds was detected.

The label thus rests on coarse thresholds, and the design applied it asymmetrically across the stressors. Every stressor counted as behaviourally active unless calibration had found it inert, so Coupling A at High (§4.2) and Coupling B at Low and Medium (§4.3) count as active although each is weak there; only δ counts as inert. The composition the worked example tests is therefore, in effect, Coupling A with Coupling B (§6.2). <!-- OWNER-PENDING:V3Q4 -->Remark 2′ (Appendix A) refines Pynadath & Tambe<d-cite key="pynadath2002"></d-cite>, who show that free communication lowers the complexity of team decision problems when the world is collectively observable. In a two-agent toy, it finds that communication has no marginal value when the agents are interchangeable, expendable and at least as numerous as the hypotheses, and regains value when any of these fails.

<!-- PAPER V3 DRAFT (PAPER V3 ruling, 2026-10-12): builder-drafted, not owner-approved -->

## 5 Measurement protocol

<!-- STUB-SPEC
JOB: The floors protocol as the rules this paper follows, not as a history of mistakes (BLIND W9): which bars have floors and how they are measured. Exhibits go to Appendix C.
WRITER: W3.
BUDGET: 270 prose words; at most two displays.
FROM: P1 §4.2 §5 and P-F; P3 §1.1 E7 (NARROW and unpositioned) and §2.2; P2 §3 A2.
ORDER:
  - a bar comes with a floor measured on the artifact being graded, per metric and per GPU (METH-1, METH-2, HW-1; one sentence of exhibit at most, details Appendix C)
  - design power is the 80 %-power detection limit at the family-corrected α (METH-7; one display); define "detection limit" and "exclusion bound" here (BRIEF §5.2)
  - a contrast is graded on the contrast's standard error (one display, the unequal-k form §6 uses)
  - the floor is a check that an effect exceeds rerun noise, not the test variance (DX-21)
  - recorded is not graded: a channel becomes evidence only with a registered family and a floor; differenced tests cannot see effects present in both arms (say "cannot see", not "blind to")
  - a floor from four runs is itself uncertain by about ±40 % (DX-303; HOME)
ROWS: METH-1, METH-2, METH-3, METH-4, METH-7, HW-1, DX-21, DX-303.
CITATIONS: none by default (no RL evaluation-methodology work is verified in RWV; V3Q17).
REGISTERED STRINGS: "recorded, not graded" (substance).
CAVEATS HOMED HERE (state each in full, once; the detection pattern, from checks/caveats.yaml, must match your home sentence):
  C36 four_run_floor_uncertainty: A floor from four runs is itself uncertain by about ±40 %. Pattern: ±\s*40\s*%
EVERY OTHER CAVEAT in checks/caveats.yaml: pointer only ("§6.3", "Appendix D"), never restated. C26: any sentence about the interaction check carries "post hoc".
NOT HERE: the four bars that broke the rule, the 46-seed story, the refactor story (Appendix C, one line each); "every acceptance bar is graded against a floor" (name which have one); study codes; "instrument", "hurdle", "beat", "floor basis", "re-floor", "card" (banned); "blind to" (the check's list owns that phrase, C25).
V2 MATERIAL: paper/v2/sections/08_methodology.md (§8.1 to §8.5; §8.6's shortfalls go to §7 or Appendix C).
DEPENDENCIES: §6 uses these rules; Appendix C (W3) holds every floor.
-->

GPU training is not bitwise reproducible. A reproducibility floor is the standard deviation of a metric over identical reruns of one artifact (the same code, configuration and seed) on one GPU. Under this protocol, an acceptance threshold, or bar, needs a floor measured on the artifact it grades, for that metric and GPU, or the analysis is declared underpowered. Not every comparison has a floor (Appendix C).

A design-stage power statement is a detection limit: the effect a test detects with 80 %<!-- N:METH-7 --> power at its family-corrected level $\alpha$, computed on the contrast's standard error,

$$
\mathrm{MDE}_{80} = \big(z_\alpha + z_{0.8}\big)\,\mathrm{SE}, \qquad \mathrm{SE} = \sqrt{\frac{s_A^2}{k_A} + \frac{s_B^2}{k_B}},
$$

where $z$ are standard normal quantiles and $s_A$ and $s_B$ are the arms' seed standard deviations over $k_A$ and $k_B$ seeds. A bare $2\sigma\sqrt{2/k}$ threshold detects an effect of its own size only about half<!-- N:V4-1 --> the time, so it only grades an observed effect against a floor, after the fact and labelled. When a confidence interval contains zero, each end is an exclusion bound: at the interval's level, the data exclude a gain above the upper end and a loss below the lower end, and the larger absolute end bounds the effect's size. The registration also calls its detection limit X an exclusion bound (§6.3).

The floor is not the test's variance: arm means also vary by seed, so contrasts are graded on seed dispersion, and the floor only checks that an effect exceeds rerun noise. A logged diagnostic becomes evidence only inside a registered test family, with a floor on its artifact; until then it is recorded, not graded. A difference between arms cannot show an effect present in both. From four identical runs, a floor is itself uncertain by about ±40 %<!-- N:DX-303 -->.

<!-- PAPER V3 DRAFT (PAPER V3 ruling, 2026-10-12): builder-drafted, not owner-approved -->

## 6 Worked example: training on stressors together or apart

<!-- STUB-SPEC
JOB: 6.1: what was registered; the framing-change disclosure (V3-F5); the central limitation in full (V3-F6: the test was sited where composition is weak). 6.2: the design, with the identity, the design error, the δ train/test mismatch and bias (b).
WRITER: W4.
BUDGET: 500 prose words (6.1 about 170, 6.2 about 330); Figure 6 caption at most 50 words.
FROM: P1 §1.2, §4.2 §6.1 and §6.2, §5.2, §5.3 item 1; P3 §1.4 and §5.1; P2 §3 #6; orchestrator note (training δ).
ORDER:
  - 6.1 (a) what was registered, before the main training runs (no date): the test, its outcome branches with a framing for each, and a falsifier ("the claim the paper makes, as a function of the confirmatory outcome", PFB:15-16, may be quoted); (b) the disclosure, about three sentences: after the result was known, the paper's emphasis moved to the environment; the registered branches stay the record of the original framing (Appendix D); every registered reading below is reported as registered (HOME, two homes by ruling); (c) the central limitation in full (HOME): at the test severity Coupling B's own survival effect was not measurable against a three-seed spread (§4.3; one sentence allowed) and communication denial showed no detectable effect (§4.4), so little beyond Coupling A was under test; this was registered in advance as a limitation of every outcome (PFB:245-260, "Required on A, B and C alike", may be quoted); a post hoc check measures it (§6.4). Do not use the professor's phrase "mostly Coupling A" as fact.
  - 6.2 (a) arms: ISO, ISO-4 (sensitivity arm, outside the family, 20 seeds), JOINT; training severities β 0.43 and 0.70, test at the held-out θ* with every stressor on at β 0.49 (CAL-3); matched architecture, hyperparameters, evaluation draw and compute, at matched compute, never convergence (DES-13; HOME); one shared-parameter IPPO policy per seed (ENV-11); Def. 8 (Γ) in words; co-primaries completion and survival, Šidák m = 2 (DES-13); 72 seeds per arm, above the registered cap of 60, a recorded deviation made before unblinding (DES-3, DES-1; HOME, one clause; history Appendix D); every interval conditional on the one registered evaluation draw (DES-13; HOME). Figure 6.
  - 6.2 (b) the shares: per-coupling frequency μ, co-occurrence p, active share, fire-only share (define, BRIEF §5.2); JOINT sees each coupling three times as often as ISO (DES-7; HOME); the identity active share = μ_A + μ_B − p with each arm's values (X4-1; HOME): so no contrast in this design moves co-occurrence alone.
  - 6.2 (c) the design error (HOME; BRIEF §7.1, no dates): δ was already found inert; the design left it out of the secondary sweeps for that reason yet kept two δ-only components of six in ISO, so a third of ISO's episodes are fire-only (DES-8); a review of the registered design identified the bias before the grid; it was registered with its direction and the correcting arm ISO-4 before unblinding, while the grid ran (DES-15).
  - 6.2 (d) the δ train/test mismatch (HOME; use the word "mismatch"): ISO's Coupling-A-only and Coupling-B-only components and all of ISO-4 train with links intact (δ = 0), JOINT with δ = 1, and θ* has δ = 1 (X4-2); harmless only if δ is inert, the premise in question; the interaction check holds δ at 1 and cannot address it.
  - 6.2 (e) bias (b) in one sentence with the registered string "reverses sign on the grid GPU" (DES-10; full readings Appendix D).
ROWS: DES-1, DES-3, DES-7, DES-8, DES-9, DES-10, DES-13, DES-14, DES-15, DES-16, CAL-3, ENV-11, CB-9 (pointer or one sentence), COM-4 (pointer), X4-1, X4-2.
CITATIONS: dewitt2020ippo; keysers2020 only to say the sweep follows DBCA (ENDPOINT CONFOUND: never the ISO/JOINT endpoints).
FIGURES: Figure 6 composer_training_mixtures (6.2). Its caption says what it shows (each arm's training mixture by episode type; each coupling's frequency and the active share); gloss once that the toggle printed on it reads labelled “δ inert under a frozen random-projection encoder at this scale” is the figure's control (the label's home is §4.4). Block below.
LATEX: at most one display (the identity or Γ's definition).
REGISTERED STRINGS: "at matched compute"; "sensitivity arm"; "fire-only"; bias (b) "reverses sign on the grid GPU"; "registered before unblinding" for the correction; "pre-registered" only for the test.
CAVEATS HOMED HERE (state each in full, once; the detection pattern, from checks/caveats.yaml, must match your home sentence):
  C01 sited_where_composition_is_weak: The test was sited where composition is weak (Coupling B quiet at the test severity, communication denial without detectable effect); registered in advance as a limitation of every outcome; the post hoc interaction check measures it. Pattern: (?i)\bsited where\b
  C04 delta_train_test_mismatch: ISO's Coupling-A-only and Coupling-B-only components and all of ISO-4 train with links intact (δ = 0), while θ* has δ = 1; a train/test mismatch in communication denial. Detection phrase - "mismatch". Pattern: (?i)\bmismatch
  C07 joint_thrice_iso: JOINT sees each coupling three times as often as ISO (the endpoint confound). Pattern: (?i)\bthree times as often\b
  C08 active_share_identity: Active share = μ_A + μ_B − p, with each arm's values; so no contrast in this design moves co-occurrence alone. Pattern: μ_A\s*\+\s*μ_B
  C09 seeds_72_recorded_deviation: 72 seeds per arm, above the registered cap of 60, a recorded deviation made before unblinding (history in App. D). Pattern: (?i)\brecorded deviation\b
  C10 inert_third_design_error: A third of ISO's training episodes carried no active stressor; owned as a design error, identified before the grid and registered with its correction before unblinding (no dates in the main text). Pattern: (?i)\bdesign error\b
  C11 matched_compute_never_convergence: The comparison is at matched compute, never at convergence. Pattern: (?i)\bmatched compute\b
  C12 one_evaluation_draw: Every interval is conditional on the one registered evaluation draw. Pattern: (?i)\b(one|single|the one) (registered |common )?evaluation draw\b
  C13 bias_b_reverses_sign: Bias (b) "reverses sign on the grid GPU" (registered string); full readings in App. D. Pattern: (?i)reverses sign on the grid GPU
  C14 framing_change: The paper's emphasis moved to the environment after the result was known; the registered outcome branches stay the record of the original framing. Two homes by ruling (V3-F5) - here and App. D. Pattern: (?i)\bafter the (result|outcome) was known\b
SHORT FORMS ALLOWED HERE (at most one sentence each; the full statement is at the home):
  C34 coupling_b_medium_measurement (home 04_calibration.md)
EVERY OTHER CAVEAT in checks/caveats.yaml: pointer only ("§6.3", "Appendix D"), never restated. C26: any sentence about the interaction check carries "post hoc".
NEW ROWS OWED:
  - X4-1 (W4): the identity at each arm, DERIVED from DES-7, DES-14, DES-16, DES-9: ISO 1/3 + 1/3 − 0 = 2/3; ISO-4 1/2 + 1/2 − 0 = 1; JOINT 1 + 1 − 1 = 1; sweep arms (μ = 0.5) 1 − p; identification arms (μ = 0.4) 0.8 − p (P1 §5.2; check each input at its row source).
  - X4-2 (W4): training δ per arm, VERIFIED at che/configs/p6_iso.yaml:41-46, p6_iso4.yaml:36-39, p6_joint.yaml:36-37, theta_star_holdout.yaml:76 (BRIEF §0).
OWNER-PENDING:
  - the framing-change wording (V3-F5 is ruled; the words are the owner's to approve).
  - attribution of the review that found the bias (carried v2 A1(ii); default "a review of the registered design").
  - bias (b) label kept (V3Q21).
  - the registered antecedent not mentioned (V3Q22).
NOT HERE: any date (the registration date included; V3-S2); branch letters (Appendix D); "registered as a bias", "a registered design caught it", "stated before the result"; "certified"; "pre-registered correction"; GPU 1/2/3; study codes; the plane's result (§6.3); the interaction result (§6.4); "twice as often" (home §6.3).
V2 MATERIAL: paper/v2/sections/09_compositional_test.md §9.1; 01_introduction.md (the arms paragraph).
DEPENDENCIES: §6.3 (W4) relies on the identity and the shares being defined here; §1 (W1) cites X4-2; §6.4 (W5) repeats only its own evaluation-draw caveat.
-->

### 6.1 What was registered, and what changed

Before the main training runs, we pre-registered the test, its outcomes, a framing for each, and a falsifier.

<!-- OWNER-PENDING:wording of the framing-change disclosure (V3-F5 is ruled; the words are the owner's to approve) -->
After the result was known, the paper's emphasis moved from the test to the environment. The registered framings remain the record of the original plan (Appendix D).

The test was sited where composition is weak. At the test severity, Coupling B's survival effect in calibration was within a three-seed<!-- N:CB-9 --> spread, not a measured floor (§4.3), and communication denial had no detectable effect (§4.4), so the test point may have offered little composition. The registration stated the Coupling-B half in advance, for every outcome: that both couplings meet their fixed-value criteria at Medium "is not the same as both producing behavioural effects there". A post hoc interaction check measures this (§6.4).

### 6.2 Design

The isolated arm (ISO) trains on configurations with one stressor on at a time and the joint arm (JOINT) with every stressor on, both at β = 0.43<!-- N:CAL-3 --> and 0.70<!-- N:CAL-3 --> with one shared-parameter IPPO policy per seed<!-- N:ENV-11 --> <d-cite key="dewitt2020ippo"></d-cite>. Both are evaluated at θ\*, the held-out test configuration: every stressor on at β = 0.49<!-- N:CAL-3 -->. Architecture, hyperparameters, evaluation draw and compute (1000<!-- N:DES-13 --> updates) are matched: Γ is read at matched compute, with no claim about convergence. The gap Γ, JOINT's mean minus ISO's at θ\*, is tested on two co-primaries, completion and survival, Šidák-corrected for m = 2<!-- N:DES-13 -->: the confirmatory family. We ran 72<!-- N:DES-3 --> seeds per arm, above the registered cap of 60<!-- N:DES-1 -->, a recorded deviation made before unblinding. Every interval is conditional on the one registered evaluation draw.

Let $\mu_A$ and $\mu_B$ be the per-coupling frequencies, the shares of episodes with each coupling on, and $p$ the co-occurrence, the share with both. The active share is the share with at least one behaviourally active stressor; the fire-only share $\nu$ is the rest. JOINT sees each coupling three times as often as ISO<!-- N:DES-7 -->, so Γ mixes frequency with co-occurrence. With communication denial inert (§4.4), the active share equals $\mu_A + \mu_B - p$<!-- N:X4-1 -->: 2/3 for ISO and 1 for JOINT<!-- N:X4-1 --><!-- N:DES-14 --> (Figure 6). No contrast in this design moves co-occurrence alone.

<!-- OWNER-PENDING:A1(ii) attribution of the review that found the bias (default "a review of the registered design") -->
One design error inflates Γ. Communication denial had been found inert and so was left out of the secondary sweeps, yet ISO kept two δ-only components of six<!-- N:DES-16 -->: a third<!-- N:DES-8 --> of ISO's training episodes are fire-only, and the design did not count them. A review of the registered design found the bias before the main runs; it was registered with its direction and a correcting arm during them, before unblinding<!-- N:DES-15 -->. That arm, ISO-4, is ISO without its δ-only components (active share 1<!-- N:X4-1 --><!-- N:DES-14 -->), a sensitivity arm outside the confirmatory family with 20<!-- N:DES-15 --> seeds. Γ₄ = JOINT − ISO-4 is the corrected gap; B̂ = ISO-4 − ISO.

ISO's single-coupling components and all of ISO-4 train with links intact (δ = 0<!-- N:X4-2 -->), while JOINT trains and θ\* tests at δ = 1<!-- N:X4-2 -->. This train/test mismatch is harmless only if δ is inert; the post hoc interaction check (§6.4) holds δ at 1 and cannot address it.

<!-- OWNER-PENDING:V3Q21 bias (b) label kept (default); V3Q22 registered antecedent not mentioned in the main text (default) -->
Bias (b), the registered caveat on differential completion drift in the last 100 updates<!-- N:DES-10 -->, reverses sign on the grid GPU (the main runs' GPU), so no direction is claimed (Appendix D).

<!-- FIGURE 6: block carried from paper/v2/sections/01_introduction.md:29 (markup, iframe height and alt text as v2 had them); caption replaced; the writer checks the alt text -->

<figure class="l-page">
  <iframe src="{{ 'assets/html/submission/composer_training_mixtures.html' | relative_url }}" width="100%" height="442" style="border:none" title="Training mixtures of ISO, ISO-4 and JOINT by episode type" loading="lazy"></iframe>
  <figcaption><strong>Figure 6.</strong> Each bar splits one arm's training mixture into episode types: Coupling A only, Coupling B only, both together, and fire-only. Beneath each bar are each coupling's frequency (labelled “per-stressor marginal” on the figure) and the active share. <span class="interact">Count δ-only episodes as inert or nominally; split by β.</span></figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/composer_training_mixtures.png" class="img-fluid" alt="Stacked bars of the three training mixtures by episode type, with each arm's per-coupling frequencies and the share of episodes that carry an active stressor." caption="Static companion of Figure 6 for the printed PDF." %}
</div>

<!-- PAPER V3 DRAFT (PAPER V3 ruling, 2026-10-12): builder-drafted, not owner-approved -->

### 6.3 Results

<!-- STUB-SPEC
JOB: Report the worked example's results: the plane decomposition first (PAPER V3 item 2(c)), labelled non-verdict-bearing; then the registered test, the correction, Γ(t) by its registered string, and the size stated plainly (V3-F3). Γ stays the registered test.
WRITER: W4.
BUDGET: 480 prose words; Figures 7 and 8 captions at most 60 words each; Table 3 (arm means and the registered readings).
FROM: P1 §4.2 §6.3, §5.1, §5.2; P2 §3 #8 to #9 and §5; P3 §3.2 (W4 items); PAPER V3 item 2(c); V3-F3, V3-F4.
ORDER:
  - (a) the plane, first (Figure 7): one sentence labels every secondary analysis non-verdict-bearing, with 95 % intervals not family-corrected, ratified after Γ was seen and before the sweep was read (DX-413; HOME of the label); the co-occurrence slope γ_p and the fire-only-share slope γ_n with intervals (SEC-1); γ_n predicts ISO-4 − ISO (SEC-3), inside B̂'s interval; γ_p predicts JOINT − ISO-4 (SEC-4) against Γ₄ and Γ₄′ measured (RES-6, RES-8): it does not extrapolate to JOINT; residuals check only coarse linearity (DX-39). Say exactly: the plane separates co-occurrence from the active share; per-coupling frequency moves with each slope.
  - (b) the registered test (Table 3 with absolute arm means, RES-4; Figure 8): survival Γ +0.96 points with its Šidák-corrected CI, REJECT (RES-2), always beside Γ₄ (FIGURE BATCH A1); completion: no detectable change, "excludes a joint-training gain larger than 0.66 points" (RES-1; HOME), with realized completion power 71.6 % at the motivating effect (DES-6; HOME) and X named as the effect the design detects with 80 % power (BRIEF §9.2 trap 5); the falsifier passes (RES-5, verdict only).
  - (c) the correction: Γ₄, the corrected gap JOINT − ISO-4 (RES-6): survival "does not survive the inert-share correction" (HOME); completion a "second exclusion bound"; JOINT still sees each coupling twice as often as ISO-4, always combined (DES-14; HOME); Γ₄ excludes only a large composition effect (its upper bound +0.63 above Γ's lower bound +0.47; HOME); Γ₄'s survival detection limit (X4-4; one clause); B̂ = ISO-4 − ISO reported without a test (RES-7; HOME); Γ = Γ₄ + B̂ holds by construction and is not a finding (HOME); Γ₄ compares runs on two GPUs; the same-GPU replicate Γ₄′ agrees and was proposed after Γ₄ was seen (RES-8, RES-9, HW-4, DES-15; HOME, one sentence); branch B's registered headline no longer holds as worded (one clause, no branch letter; Appendix D).
  - (d) Γ(t): "sign unstable over the final half" on both co-primaries (RES-11; HOME); the survival gap appears only at updates 900 to 1000 (RES-12); completion leans negative from 70 % of the budget (RES-13); tables and figure in Appendix E.
  - (e) the size, plainly (V3-F3 HOME): the survival gain is about a tenth of an agent per episode (0.11 of 12; X4-3), visible only at the end of training; the paper does not rest on it. One sentence may point to the High readout's a-fortiori exclusion (Appendix E).
ROWS: SEC-1, SEC-3, SEC-4, DX-39, DX-413, RES-1, RES-2, RES-4, RES-5, RES-6, RES-7, RES-8, RES-9, RES-11, RES-12, RES-13, DES-6, DES-13, DES-14, DES-15, HW-4, X4-3, X4-4.
FIGURES: Figure 7 simplex_secondary (first; glosses: labelled “knee”, labelled “no-element share”, labelled “sweep_c50_p000”; caption names γ_p's and γ_n's rows first, P2 R6 fallback); Figure 8 ladder_registered_readings (glosses: labelled “rung”, labelled “unit 1”, labelled “cross-unit”, labelled “floor basis”; the figure prints rates, the text points: say so once). Blocks below.
REGISTERED STRINGS: "does not survive the inert-share correction"; "sign unstable over the final half" (both co-primaries); "excludes a joint-training gain larger than 0.66 points"; "second exclusion bound"; REJECT and null; "non-verdict-bearing" once, then "secondary"; B̂ gets no verdict.
CAVEATS HOMED HERE (state each in full, once; the detection pattern, from checks/caveats.yaml, must match your home sentence):
  C06 joint_twice_iso4: JOINT sees each coupling twice as often as ISO-4, and always combined. Pattern: (?i)\btwice as often\b
  C15 secondary_non_verdict_bearing: The plane decomposition and every secondary analysis are non-verdict-bearing; their 95 % intervals are not family-corrected. Pattern: (?i)\bnon-verdict-bearing\b
  C16 sign_unstable_final_half: Registered string "sign unstable over the final half", on both co-primaries, with the shapes. Pattern: (?i)sign unstable over the final half
  C17 completion_exclusion_bound: Completion shows no detectable change and "excludes a joint-training gain larger than 0.66 points". Pattern: (?i)joint-training gain larger than
  C18 inert_share_correction: Registered string - the survival gain "does not survive the inert-share correction". Pattern: (?i)does not survive the inert-share correction
  C19 gamma4_excludes_only_large: Γ₄ excludes only a large composition effect (its upper bound lies above Γ's lower bound). Pattern: (?i)\bonly a large\b
  C20 bhat_without_test: B̂ = ISO-4 − ISO is reported without a test and gets no verdict. Pattern: B̂[^.]{0,120}\b(without a test|no test)\b
  C21 gamma_sum_by_construction: Γ = Γ₄ + B̂ holds by construction for arm means and is never a finding. Pattern: Γ\s*=\s*Γ₄\s*\+
  C22 cross_gpu_and_same_gpu_replicate: Γ₄ compares runs on two GPUs; the same-GPU replicate agrees and was proposed after Γ₄ was seen (GPU blocks in App. D). Pattern: (?i)\bsame-GPU replicate\b
  C23 realized_completion_power: Realized completion power at the motivating effect is 71.6 %, stated once beside the exclusion. Pattern: 71\.6
SHORT FORMS ALLOWED HERE (at most one sentence each; the full statement is at the home):
  C24 high_readout_a_fortiori (home 17_appendix_results.md)
EVERY OTHER CAVEAT in checks/caveats.yaml: pointer only ("§6.3", "Appendix D"), never restated. C26: any sentence about the interaction check carries "post hoc".
NEW ROWS OWED:
  - X4-3 (W4): about 0.11 agents per episode, DERIVED: 0.0095531 (P6/unblind/unblind.json:61) × 12 (ENV-6) = 0.1146; identity as DX-406 (deaths per episode = 12 × (1 − survival rate); che/env/env.py:446; che/tests/test_lethality.py:201-202); scope: the size statement.
  - X4-4 (W4): Γ₄ and B̂ survival detection limits 0.0090 and 0.0089, VERIFIED at P6/post_unblind_analysis/post_gamma4_t2000.md:15-16 (last column); confirm the column is the 80 %-power detection limit at the stated family level before use (V3Q18).
NOT HERE: "composition effect" without the correction; "composition does not matter"; "the plane separates co-occurrence from frequency"; Γ = Γ₄ + B̂ as a finding; a verdict for B̂; "budget-robust", "converged"; GPU 1/2/3, "card", "unit", "rung", "knee" outside glosses; the k = 60, T = 2000 and High details (Appendix E); mediation (Appendix F); "conservative" for the k increase; advice (that is §6.5).
V2 MATERIAL: paper/v2/sections/09_compositional_test.md §9.2.
DEPENDENCIES: §6.2 defines the shares and the identity; §6.5 (W5) points here for Γ₄'s limits; Appendix E (W5) and F (W4) hold the details.
-->

Every secondary analysis, the plane decomposition included, is non-verdict-bearing, as registered: its 95 % intervals are not family-corrected, and its specification was ratified after Γ was seen and before the sweep was read<!-- N:DX-413 -->. A sweep holds each coupling's frequency at 0.5<!-- N:DES-9 --> while $p$ moves from 0 to 0.5<!-- N:DX-28 -->, and three<!-- N:DX-28 --> identification arms at frequency 0.4<!-- N:DES-9 --> make a plane in co-occurrence and fire-only share estimable (Appendix F).

On survival, the plane's co-occurrence slope $\gamma_p$ is +3.26 points per unit $p$ [+1.37, +5.02], and its fire-only-share slope $\gamma_n$ is −2.37 points per unit $\nu$ [−4.19, −0.57]<!-- N:SEC-1 --> (Figure 7, which prints $\mu$ as m and $\nu$ as n). By §6.2's identity, the plane separates co-occurrence from the active share only; per-coupling frequency moves with each slope. The fire-only-share slope predicts ISO-4 − ISO at +0.79 points<!-- N:SEC-3 -->, inside B̂'s interval, though that move also changes frequency. The co-occurrence slope, fitted on $p$ up to 0.5<!-- N:DX-28 -->, predicts JOINT − ISO-4 at +3.26 points<!-- N:SEC-4 -->, far above the measured Γ₄ (Table 3): it does not extrapolate to JOINT.

<!-- FIGURE 7: block carried from paper/v2/sections/09_compositional_test.md:114 (markup, iframe height and alt text as v2 had them); caption replaced; the writer checks the alt text -->

<figure class="l-page">
  <iframe src="{{ 'assets/html/submission/simplex_secondary.html' | relative_url }}" width="100%" height="832" style="border:none" title="Secondary design on the triangle of training mixtures, with plane predictions beside measured contrasts" loading="lazy"></iframe>
  <figcaption><strong>Figure 7.</strong> Left: training mixtures in p and ν, with the arms and the p = 0 sweep arm (labelled “sweep_c50_p000” on the figure). Right: secondary estimates and plane predictions beside B̂, Γ₄, Γ₄′: the change point (labelled “knee” on the figure), the sweep slope (labelled “dose slope” on the figure) and the fire-only share's term (labelled “no-element share” on the figure). <span class="interact">Switch metrics.</span></figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/simplex_secondary.png" class="img-fluid" alt="A triangle of training mixtures by share of both-stressor and fire-only episodes, locating the secondary arms, ISO, ISO-4 and JOINT, beside the secondary estimates and the plane predictions next to the measured contrasts" caption="Static companion of Figure 7 for the printed PDF." %}
</div>

On survival, Γ is +0.96 points, Šidák-corrected 95 % CI [+0.47, +1.44]<!-- N:RES-2 -->: REJECT (Table 3; Figure 8 prints rates). On completion it is −1.73 points [−4.12, +0.66]<!-- N:RES-1 -->, null: no detectable change, and the result excludes a joint-training gain larger than 0.66 points<!-- N:RES-1 -->. The design's completion detection limit, the registration's X, is 3.29 points<!-- N:RES-1 -->; realized power at the 3-point effect that motivated the design was 71.6 %<!-- N:DES-6 -->. The registered falsifier passes<!-- N:RES-5 --> (Appendix D).

The survival gain does not survive the inert-share correction. Γ₄, the corrected gap, is −0.03 points on survival [−0.68, +0.63]<!-- N:RES-6 -->, null, and the gain is not called a composition effect. On completion both gaps are null, so Γ₄ is a second exclusion bound, the registration's term for its detection limit, X₄ = 4.88 points<!-- N:RES-6 -->. Γ₄ excludes only a large composition effect: its upper bound, +0.63<!-- N:RES-6 -->, lies above Γ's lower bound, +0.47<!-- N:RES-2 -->, and its survival detection limit is 0.90 points<!-- N:X4-4 -->. JOINT still sees each coupling twice as often as ISO-4<!-- N:DES-14 -->, and always combined. Γ₄ compares runs on two GPUs; its same-GPU replicate Γ₄′, JOINT minus the $p = 0$ sweep arm (ISO-4's mixture on JOINT's GPU), agrees on both co-primaries but was proposed after Γ₄ was seen<!-- N:RES-8 --><!-- N:HW-4 --><!-- N:DES-15 -->. B̂ is reported without a test, as registered<!-- N:RES-7 -->. Γ = Γ₄ + B̂ holds by construction for arm means, so B̂ is not a second finding. The registered headline for this outcome no longer holds as worded (Appendix D).

Γ(t), the gap at earlier checkpoints, is sign unstable over the final half on both co-primaries<!-- N:RES-11 -->. On survival, its Šidák interval excludes zero only at updates 900, 950 and 1000<!-- N:RES-12 -->. Completion is negative at every checkpoint from update 700<!-- N:RES-13 --> and leans negative, unresolved (Appendix E).

In agents, the survival gain is about a tenth of an agent per episode (0.11 of 12<!-- N:X4-3 --><!-- N:ENV-6 -->), detectable only in the last fifth of training<!-- N:RES-12 -->. The paper does not rest on it.

**Table 3.** Arm means (rates) and registered contrasts (points, rate × 100) at θ\*, with Šidák-corrected 95 % intervals; k in the order of each contrast's arms.

| quantity | k | completion | survival | status |
|---|---|---|---|---|
| ISO mean | 72<!-- N:DES-3 --> | 0.7772<!-- N:RES-4 --> | 0.9158<!-- N:RES-4 --> | confirmatory arm |
| JOINT mean | 72<!-- N:DES-3 --> | 0.7600<!-- N:RES-4 --> | 0.9254<!-- N:RES-4 --> | confirmatory arm |
| ISO-4 mean | 20<!-- N:DES-13 --> | 0.7726<!-- N:DX-18 --> | 0.9256<!-- N:DX-18 --> | sensitivity arm |
| Γ = JOINT − ISO | 72 / 72<!-- N:DES-3 --> | null: −1.73 [−4.12, +0.66]<!-- N:RES-1 --> | REJECT: +0.96 [+0.47, +1.44]<!-- N:RES-2 --> | confirmatory |
| Γ₄ = JOINT − ISO-4 | 72 / 20<!-- N:DES-3 --><!-- N:DES-13 --> | null: −1.26 [−4.81, +2.28]<!-- N:RES-6 --> | null: −0.03 [−0.68, +0.63]<!-- N:RES-6 --> | sensitivity arm, two GPUs |
| Γ₄′ = JOINT − the p = 0 sweep arm | 72 / 20<!-- N:DES-3 --><!-- N:DES-13 --> | null: −2.47 [−6.16, +1.22]<!-- N:RES-8 --><!-- N:DX-19 --> | null: +0.13 [−0.56, +0.81]<!-- N:RES-8 --> | secondary, one GPU |
| B̂ = ISO-4 − ISO | 20 / 72<!-- N:DES-13 --><!-- N:DES-3 --> | −0.46 [−4.05, +3.12]<!-- N:RES-7 --><!-- N:DX-19 --> | +0.98 [+0.33, +1.63]<!-- N:RES-7 --> | no registered test |

<!-- FIGURE 8: block carried from paper/v2/sections/09_compositional_test.md:64 (markup, iframe height and alt text as v2 had them); caption replaced; the writer checks the alt text -->

<figure class="l-page">
  <iframe src="{{ 'assets/html/submission/ladder_registered_readings.html' | relative_url }}" width="100%" height="1012" style="border:none" title="Registered readings in order: Gamma, Gamma4, Gamma4 prime and B-hat on both co-primaries" loading="lazy"></iframe>
  <figcaption><strong>Figure 8.</strong> The registered contrasts in order, one step per row (labelled “rung” on the figure): Γ, with the registered 60-seed<!-- N:DES-1 --> analysis; Γ₄; Γ₄′; and B̂, with no registered test. Rows name one GPU (labelled “unit 1” on the figure) or two (labelled “cross-unit” on the figure). Γ's stipple is ±1 floor-based standard error (labelled “floor basis” on the figure). <span class="interact">Step the rows.</span></figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/ladder_registered_readings.png" class="img-fluid" alt="Two forest plots, completion and survival, of the registered contrasts in order with their Šidák-corrected intervals and verdicts" caption="Static companion of Figure 8 for the printed PDF." %}
</div>

<!-- PAPER V3 DRAFT (PAPER V3 ruling, 2026-10-12): builder-drafted, not owner-approved -->

### 6.4 A post hoc interaction check

<!-- STUB-SPEC
JOB: Report the post hoc, evaluation-only interaction check at θ* (V3-E1): what it is, its label, its result under PLAN §7's reading rules, and what it is blind to (the one home of that list). It measures the central limitation of §6.1; it changes no registered reading.
WRITER: W5.
BUDGET: 200 prose words; Figure 9 caption at most 60 words.
FROM: P1 §3.3; P2 §4; PLAN.md §1 to §8; V3-E1.
ORDER:
  - (a) what it is (writable now, with HOLEs for numbers that need IC rows): post hoc and evaluation-only, proposed after the result was known, planned and fixed before its run, outside the registered family; at θ* only; four conditions (neither coupling, Coupling A only, Coupling B only, both), each θ* with κ_A and/or κ_B set to 0 and δ = 1 throughout; the final checkpoints of ISO, JOINT and ISO-4 (DES-3, DES-13); the registered evaluation draw with common random numbers; I = J(both) − J(A only) − J(B only) + J(neither) per policy, sign convention once (I < 0: together they cost more than the sum); per arm and pooled, Šidák-corrected over the family of estimates (count from an IC row); an evaluation self-floor on the run GPU.
  - (b) the result (HOLE): the pooled pair first, per PLAN §7: either a detectable interaction with its sign and size (survival also in agents per episode), or an exclusion "|I| below B points at the family-corrected level" with the detection limit beside it; per-arm rows say whether the answer depends on how the policy was trained; cross-arm differences descriptive only. Figure 9.
  - (c) what it is blind to (HOME, the full list once; use the phrase "blind to"): θ* only (Low and High were not run); fixed policies, so it says nothing about whether training on co-occurrence helps (that is Γ); additivity on the scale of bounded rates; one evaluation draw; δ held at 1; not a cross-arm test; post hoc; the arms met the four conditions differently in training (ISO trained on A-only and B-only at δ = 0, ISO-4 never at δ = 1, JOINT only with every stressor on; all at β 0.43 and 0.70, never 0.49).
ROWS: DES-3, DES-13, CAL-3; IC-* (orchestrator, from the committed step-0.5 report: the number of evaluations, Šidák m and z, per-arm and pooled I with interval ends, MDE80s, self-floor results, the cross-GPU identical count, realized GPU-hours).
FIGURES: Figure 9, the new interaction-check figure (P2 §4: per arm a 2 × 2 condition panel; a forest plot of I by arm and pooled with per-seed points, intervals and the self-floor band; a "post hoc" mark, no verdict mark). It does not exist yet: a figure builder makes it from the committed outputs after step 0.5 (STRUCTURE §4). Caption: what it shows, and the words "post hoc" (V3Q13).
REGISTERED STRINGS: none (the check is not registered). Its label: "post hoc" wherever it appears.
CAVEATS HOMED HERE (state each in full, once; the detection pattern, from checks/caveats.yaml, must match your home sentence):
  C25 interaction_blind_to: What the interaction check is blind to (θ* only; fixed policies; additive scale; one draw; δ held at 1; no cross-arm test; post hoc; arms' training conditions differ). The full list once. Pattern: (?i)\bblind to\b
SHORT FORMS ALLOWED HERE (at most one sentence each; the full statement is at the home):
  C12 one_evaluation_draw (home 06_example_design.md)
EVERY OTHER CAVEAT in checks/caveats.yaml: pointer only ("§6.3", "Appendix D"), never restated. C26: any sentence about the interaction check carries "post hoc".
HOLES:
  - every number in (a) that has no row yet (IC rows)
  - the result paragraph (b)
  - Figure 9 block (with its measured iframe height)
NOT HERE: "pre-check" as if registered; "no interaction" or "additive" (it is an exclusion with its bound); any verdict word (REJECT, null) for I; any cross-arm test; Low or High; any statement about training effects or about δ; the professor's review as authority.
V2 MATERIAL: none (new).
DEPENDENCIES: IC rows (orchestrator, step 0.5); §6.1 points here; §6.5 (W5) and the abstract (W1) use its reading; Appendix G (W5) holds the full tables.
-->

To measure what composition θ\* offered (§6.1), we added a post hoc, evaluation-only check, planned before it ran and outside the confirmatory family (Appendix G). The final checkpoint of every ISO, JOINT and ISO-4 run is evaluated at θ\* in four conditions, neither coupling, Coupling A only, Coupling B only and both, on the registered evaluation draw with common random numbers (§3.4). Per policy and co-primary, the post hoc interaction contrast is

$$
I = J(\text{both}) - J(\text{A only}) - J(\text{B only}) + J(\text{neither}).
$$

Higher $J$ is better, so $I = 0$ means that the couplings' effects add, and $I < 0$ that together they cost more than their separate costs summed. $I$ is estimated per arm and pooled, with Šidák-corrected intervals over eight<!-- N:IC-4 --> tests and a measured evaluation self-floor (Appendix G).

<!-- HOLE:INTERACTION -->
<!-- fills: (b) the result paragraph, pooled pair first, per PLAN §7 -->

<!-- HOLE:INTERACTION -->
<!-- fills: Figure 9 block: the interaction figure (iframe and print companion), built after step 0.5 -->

Besides being post hoc, the check is blind to several things. Holding policies fixed, it cannot say whether training on co-occurrence helps, which Γ tests. It covers θ\* only, tests additivity only on the scale of rates, where a ceiling can create or hide an interaction, holds δ at 1<!-- N:COM-6 -->, tests no difference between arms, and is conditional on the one evaluation draw. The arms also met the four conditions differently in training (Appendix G), so each arm's $I$ also reflects its policies' familiarity with each condition, which pooling averages but does not remove.

<!-- PAPER V3 DRAFT (PAPER V3 ruling, 2026-10-12): builder-drafted, not owner-approved -->

### 6.5 What the example teaches

<!-- STUB-SPEC
JOB: The lesson (V3-F4; PROF 3; BLIND W2): by the identity, matching the active share alone cannot isolate co-occurrence, and no design in this study isolates it; the check-dependent half of the lesson; one labelled advice sentence; future work.
WRITER: W5.
BUDGET: 150 prose words.
FROM: P1 §5.2 and §3.3; P3 §3.1 point (3); V3-F4; PAPER V3 item 4.
ORDER:
  - (a) the identity half (write now; HOME of "cannot isolate co-occurrence"): by the identity of §6.2 (point, do not restate it), matching the active share moves per-coupling frequency, so it cannot isolate co-occurrence; the three designs side by side: the sweep fixes frequency and moves the fire-only share (DES-9, SEC-5); the correction fixes the active share and moves frequency (point to §6.3, do not say "twice as often"); the plane fixes the fire-only share and moves frequency with p. None isolates co-occurrence.
  - (b) the check-dependent half (HOLE): one or two sentences from the matching row of P1 §3.3, labelled post hoc.
  - (c) advice, if any: one sentence of its own, labelled "We suggest, from this one environment, …"; never after therefore, so or thus; not a contribution.
  - (d) future work: ISO-4 trained for 2000 updates, which would match each coupling's exposure count to JOINT's but gives up matched compute (PAPER V3 item 4; no run authorized); varying coupling strength instead of frequency. A third item (a test point where both couplings are active) only if the owner adds it (V3Q20).
ROWS: DES-9, DES-14 (pointer), SEC-5, X4-1 (pointer), IC-* (for the HOLE).
REGISTERED STRINGS: none required; "non-verdict-bearing" is not repeated here.
CAVEATS HOMED HERE (state each in full, once; the detection pattern, from checks/caveats.yaml, must match your home sentence):
  C27 cannot_isolate_co_occurrence: Matching the active share alone cannot isolate co-occurrence; no design here isolates it (the lesson, never after "therefore"). Pattern: (?i)\bisolat\w* co-occurrence\b
SHORT FORMS ALLOWED HERE (at most one sentence each; the full statement is at the home):
  C08 active_share_identity (home 06_example_design.md)
  C11 matched_compute_never_convergence (home 06_example_design.md)
EVERY OTHER CAVEAT in checks/caveats.yaml: pointer only ("§6.3", "Appendix D"), never restated. C26: any sentence about the interaction check carries "post hoc".
HOLES:
  - (b) the check-dependent lesson
  - (c) the advice sentence's content, which depends on (b)
NOT HERE: "match the active share" as advice (by the identity it un-matches frequency); "the plane separates co-occurrence from frequency"; "therefore"; "twice as often" (home §6.3); the identity restated in full (home §6.2); any claim about Low, High or training effects from the check.
V2 MATERIAL: paper/v2/sections/09_compositional_test.md §9.3 (replaced, not reused).
DEPENDENCIES: §6.2 (identity), §6.3 (Γ₄'s limits), §6.4 (the check); the abstract's lesson (W1) must match (b) and (c).
-->

By the identity of §6.2, holding the active share fixed while co-occurrence changes forces per-coupling frequency to change with it, so matching the active share alone cannot isolate co-occurrence. None of the study's designs isolates it. The sweep holds each coupling's frequency fixed and moves the fire-only share with co-occurrence. The inert-share correction holds the active share fixed and moves frequency along with co-occurrence (§6.3). The plane's co-occurrence slope holds the fire-only share fixed and moves frequency with co-occurrence.

<!-- HOLE:INTERACTION -->
<!-- fills: (b) the check-dependent half of the lesson, labelled post hoc; (c) the labelled advice sentence -->

Two experiments would go further. ISO-4 trained for 2000<!-- N:X5-3 --> updates would meet each coupling as often as JOINT does in the registered budget, at the cost of matched compute, leaving co-occurrence as the main remaining difference. Varying the couplings' strength, with frequency, co-occurrence and the active share fixed, would test whether composition appears where both couplings are strong (§6.1).

<!-- PAPER V3 DRAFT (PAPER V3 ruling, 2026-10-12): builder-drafted, not owner-approved -->

## 7 Limitations and scope

<!-- STUB-SPEC
JOB: Only what §1's three up-front limitations did not carry, as pointers or one line each.
WRITER: W5.
BUDGET: 200 prose words.
FROM: P1 §4.2 §7; P3 §2.2 and §1.4; READS RULING item 4.
ORDER:
  - matched compute, never convergence (one line; DES-13)
  - no theorem says joint training wins (TF:686; HOME)
  - one budget; one held-out point between the training severities (pointer §6.2)
  - the d_p ablation's scope (ENV-2 to ENV-5: 500 updates, 3 seeds, fire only)
  - no heuristic baselines; the task needs no coordination and the agents share parameters (pointer §1)
  - no adaptive curriculum is evaluated (READS RULING item 4)
  - cross-GPU blocks and the δ train/test difference by pointer only (§6.3, §6.2)
ROWS: DES-13, ENV-2, ENV-3, ENV-4, ENV-5, ENV-11.
REGISTERED STRINGS: "at matched compute" (one line).
CAVEATS HOMED HERE (state each in full, once; the detection pattern, from checks/caveats.yaml, must match your home sentence):
  C38 no_theorem_joint_wins: No theorem says joint training wins. Pattern: (?i)\bno theorem\b
SHORT FORMS ALLOWED HERE (at most one sentence each; the full statement is at the home):
  C11 matched_compute_never_convergence (home 06_example_design.md)
EVERY OTHER CAVEAT in checks/caveats.yaml: pointer only ("§6.3", "Appendix D"), never restated. C26: any sentence about the interaction check carries "post hoc".
NOT HERE: anything §1 already states (sited where composition is weak; the inert label; one algorithm, one map, 12 agents) beyond a pointer; the word "mismatch" (home §6.2); secondary intervals not family-corrected (home §6.3); dates; Proposition 4.
V2 MATERIAL: paper/v2/sections/10_limitations.md.
DEPENDENCIES: §1 (W1) carries the three up-front limitations.
-->

§1 lists the largest limitations first, and each sits where it arises: how much composition the test configuration offered, and what the post hoc interaction check measured there (§6.1, §6.4); the coarse and unevenly applied inert label for communication denial (§4.4); the communication setting that differs between training and test for two arms (§6.2); and one learner, one map and one team size (§1).

Every comparison in the worked example is at matched compute, 1000<!-- N:DES-13 --> updates per run, and says nothing about other budgets (§6.2). No theorem in this paper says that joint training should win; the hypothesis the worked example tests is empirical. The test configuration is one held-out severity between the two training severities (§6.2). The hazard is simple, with one ignition at reset, a one-step burn and no wind or uneven fuel (§3.1). The only ablation of the death price is narrow, with three seeds<!-- N:ENV-2 -->, 500<!-- N:ENV-2 --> updates and the fire as the only hazard (§3.3). The task needs no coordination, the agents share one set of parameters, and no heuristic or scripted baseline is reported (§1). We compare fixed training distributions and evaluate no adaptive curriculum. Comparisons across GPUs are marked where they occur (§6.3).

<!-- PAPER V3 DRAFT (PAPER V3 ruling, 2026-10-12): builder-drafted, not owner-approved -->

## 8 Using CHE and reproducing the paper

<!-- STUB-SPEC
JOB: What a user needs (P3 §1.2) and what the code supplement holds and reproduces (V3-V1, V3-V3), the registration statement (V3-V2), and what is exact (evaluation) and what is not (GPU training).
WRITER: W5.
BUDGET: 240 prose words; one short code block at most (the API, not a LISTING unless copied from a committed file with a LISTING line).
FROM: P3 §1.2 and §1.3; P1 §4.2 §8; V3-V1, V3-V2, V3-V3.
ORDER:
  - the API in two lines: reset(key, cfg) returns (obs, state); step(key, state, actions, cfg) returns (obs, state, team reward, done, info) (che/env/env.py:200, :283-290); functional, jit- and vmap-ready
  - configuration: YAML configs carry θ and the locked sub-parameters and per-episode training mixtures (che/env/config.py); every locked constant is asserted by a test (che/tests/test_locks.py)
  - how to run, as the commands run inside the unpacked supplement: the CPU test suite; training (python -m che.train.ippo with config, updates and seed); evaluation (python -m che.eval.harness with config and checkpoint directory) (ippo.py:668-674; harness.py:240-244; paper/v3/supplement/SHIPPED_README.md)
  - compute: one 1000-update run and one evaluation on one RTX 5090 (DX-4), environment steps per run (DX-3), toolchain (DX-407)
  - what can be varied (the trainer accepts grid-size and n-envs flags, ippo.py:676-677) and that every reported result uses one instance (ENV-6); exact nesting gives common-random-number contrasts (the interaction check uses this)
  - the supplement: what it holds (package, configs, tests, analysis scripts, registration documents, hash manifest) and that it reproduces every analysis from committed evaluation outputs; retraining needs a GPU; checkpoints are not shipped; its size only with a row (PENDING)
  - the registration statement, two sentences: the registration record is internal and version-controlled, its dates are self-reported, the supplement carries the registration documents with a hash manifest; a public registry next time (full account Appendix D)
  - evaluation is bit-identical on one GPU; 280 of 288 paired evaluations agree across GPUs, largest difference stated (HW-2, HW-3; HOME); GPU training is not bitwise reproducible across GPUs
ROWS: DX-3, DX-4, DX-407, ENV-6, HW-2, HW-3; supplement rows X5-1 (size) and X5-2 (TMLR limit) only once VERIFIED (V3Q24, V3Q25).
REGISTERED STRINGS: none.
CAVEATS HOMED HERE (state each in full, once; the detection pattern, from checks/caveats.yaml, must match your home sentence):
  C37 evaluation_reproducibility: Evaluation is bit-identical on one GPU; 280 of 288 paired evaluations agree across GPUs. Pattern: \b280 of 288\b
EVERY OTHER CAVEAT in checks/caveats.yaml: pointer only ("§6.3", "Appendix D"), never restated. C26: any sentence about the interaction check carries "post hoc".
NEW ROWS OWED:
  - X5-1 (W5): the supplement zip's size, from step 2's committed output (paper/v3/out/build_summary.json once committed); PENDING-COMMIT until then.
  - X5-2 (W5): TMLR's supplementary-material limit, only after the page is re-read directly and the reading transcribed (V3Q24); else cut.
  - optional, V3Q18: training throughput DERIVED from DX-3 and DX-4; CPU-suite time from a committed supplement check.
OWNER-PENDING:
  - decision-log excerpts in the supplement (V3-V1 owner decision); content hashes of the registration files in the text (V3Q16).
NOT HERE: JaxMARL compatibility; a repository URL, account, commit hash or absolute path; "the formal specification" (TF does not ship by default, V3Q16); any supplement size or venue limit without a row; total GPU-hours; PBT; dates.
V2 MATERIAL: paper/v2/sections/11_reproducibility.md; paper/v2/sections/alt/ (the supplement alternate, if present); step 2's paper/v3/supplement/SHIPPED_README.md and its report.
DEPENDENCIES: step 2 (supplement contents and commands); Appendix D (W4) carries the full registration account.
-->

CHE is a functional JAX environment: `reset(key, cfg)` returns observations and state, and `step(key, state, actions, cfg)` also returns the team reward, a done flag and an info dictionary. YAML configurations set θ, the fixed sub-parameters and any training mixture, and a test checks them against a registry of the fixed constants (Appendix B).

In the anonymized code supplement, `uv run pytest -q che/tests` runs the CPU tests, and `uv run python -m che.train.ippo` and `uv run python -m che.eval.harness` train and evaluate. On one RTX 5090<!-- N:DX-5 -->, a 1000-update run took 518–521 s and a 512-episode evaluation 9–10 s<!-- N:DX-4 -->.

The supplement holds the package, configurations, tests, registration documents, analysis scripts with the committed outputs they read, and a sha256 manifest; its README recomputes the registered analyses on a CPU. The post hoc interaction check's analysis needs version history, so it does not run there. Checkpoints ship only as hashes.

<!-- OWNER-PENDING:V3Q16 -->
<!-- what else ships is the owner's call (RM-OWNER-1): the supplement builder ships docs/theory_foundations.md and the four lock records by default (paper/v3/supplement/README.md, rules D3, D4), while DISPOSITIONS V3Q16's default ships the hash manifest only; if they ship, add "the theory document and the records of how each fixed constant was measured" to the list above. Decision-log excerpts are off by default (V3-V1 owner decision). The supplement's size and TMLR's limit wait for rows X5-1 and X5-2 (PENDING; V3Q24, V3Q25) and are not stated. -->

<!-- OWNER-PENDING:V3_V2 the registration statement's wording, in particular the commitment to a public registry next time, is the owner's to confirm -->

Our registration record is internal and version-controlled, so its dates are self-reported; the hash manifest shows only that the archive arrived unaltered (Appendix D). A public registry such as OSF would remove this limit; we intend to use one next time.

Evaluation reproduces closely: repeated evaluations of two checkpoints on one GPU were bit-identical and matched the main runs' own<!-- N:HW-2 -->, and across GPUs 280 of 288<!-- N:HW-3 --> paired checkpoint and metric values agreed exactly, differing by at most 2.44 × 10⁻⁴<!-- N:HW-3 -->. GPU training is not, which is why reproducibility floors are measured (§5).

<!-- PAPER V3 DRAFT (PAPER V3 ruling, 2026-10-12): builder-drafted, not owner-approved -->

## 9 Conclusion

<!-- STUB-SPEC
JOB: Three sentences: what CHE is for; what the worked example showed (with its strings, short); what to run next.
WRITER: W1.
BUDGET: 90 prose words.
FROM: P1 §4.2 §9.
ROWS: none required (no new numbers; point to §6).
REGISTERED STRINGS: if the result is restated, only by pointer; no caveat restated (every caveat in this file is pointer-only).
EVERY OTHER CAVEAT in checks/caveats.yaml: pointer only ("§6.3", "Appendix D"), never restated. C26: any sentence about the interaction check carries "post hoc".
HOLES:
  - one clause on the check's reading, labelled post hoc
NOT HERE: new claims; advice; numbers; dates.
DEPENDENCIES: §6.5 and the abstract must agree with it.
-->

CHE is for studying how stressors coupled to an evolving fire shape what multi-agent policies learn, with each stressor able to be switched off exactly. Its worked example, a pre-registered test of training on stressors together or apart, is read in §6.3 exactly as registered, and §6.5 draws its lesson for how such tests are designed.
<!-- HOLE:INTERACTION -->
<!-- fills: one clause: the check's reading, labelled post hoc (pointer §6.4); it may join the sentence before or stand as a short sentence; about 7 words of room are left under the 90-word budget (fix round, RM-1) -->
Next, the corrected isolated arm could be trained until each coupling's exposure count matches the joint arm's, and coupling strength could be varied instead of frequency (§6.5).

<!-- PAPER V3 DRAFT (PAPER V3 ruling, 2026-10-12): builder-drafted, not owner-approved -->

## Appendices

<!-- STUB-SPEC
JOB: The appendix index (one line per appendix A to J), then Appendix A: the formal statements and proofs the main text uses (V3-S6), at the level v2 verified, with Thm. 1 stated to match the implemented toy (V3-E2, V3Q5), Prop. 4 as a remark in words with its honesty note, and the full step listing.
WRITER: W2.
BUDGET: about 1,000 prose words, excluding displays and the listing.
FROM: P1 §5.4 and §6.1 A; P3 §3.3 (Thm. 1); V3-S6; v2 STRUCTURE §8 (LaTeX levels).
ORDER:
  - index: A Proofs and formal statements; B Locked constants and hyperparameters; C Floors; D Registration timeline; E Additional results; F The secondary design; G The interaction check in full; H Trained-policy episodes; I How the literature search ran; J How this paper was made.
  - A: Prop. 1 statement and proof once (finite on its reachable states; v2 OWNER ITEM 2); Listing 5, the full step in the Prop. 1 order (env.py:298-358, carried below).
  - A: Prop. 2 statement and proof; the implementation-exactness paragraph (v2); Cor. 1 at v2's verified level ((1) with kesten1980; (2) only at a verified level; (3) dropped; (4) with garet2004chemical, v2 D2 default).
  - A: Prop. 3 statement (linear scaling, no 43/18 rate, no divergence claim on the finite map) and proof (v2 D3 open: equality vs inequality).
  - A: Thm. 1 (OWNER-PENDING V3Q5). Default: state it for per-step reveal probabilities τ_t(κ_B) = exp(−κ_B D_t) with optical depths D_t > 0 and q = 1 − ∏_t (1 − τ_t); the proof is unchanged (it uses only independent, remembered per-step signals and q); the unit-density, integer-distance form is the special case D_t = d − t + ℓ_f; the toy's D_t are the production kernel's optical depths (row X2-2); part (3) needs every D_t > 0 (the code documents the failure when not: d = 6 gives τ ≡ 1, phase4_report.md:140-148); J* is the value of the content channel only, which is what the scored policies read (P3 §3.3 item 5; phase4_report.md:170-195); measured 0.5000 ± 0.0055 against predicted 0.5028 at κ_B = 8, z −0.51 (X2-1); say that this statement departs from the theory record's unit-density form (v2 C2 default: the paper departs and says so).
  - A: Remark 2′ statement as v2 had it, with the toy constants (DX-15) (OWNER-PENDING V3Q4: the ℓ_f clash with Thm. 1, part (i) unproven, and the refinement wording are open).
  - A: a remark in words, no display, no constant: a transfer bound for a fixed policy (formerly Proposition 4): it bounds what isolated training can be guaranteed to transfer, not what happens, and it is an upper bound; with its honesty note in substance (TF:636-643: upper bounds on ISO's transfer do not lower-bound the realized gap; compositional generalization can emerge from isolated training; the experiment decides). OWNER-PENDING V3Q3 (drop is the alternative).
ROWS: CAL-3, DX-15, DX-409, CB-4, DX-14, X2-1, X2-2.
CITATIONS: grassberger1983, kesten1980, garet2004chemical, chen2022understandingdr (Thm. 1 kin to their Prop. 1 construction, as RWV records), pynadath2002 (Remark 2′).
LISTINGS: Listing 5, che/env/env.py:298-358 (block below, byte-identical).
LATEX: as v2 STRUCTURE §8's appendix column, minus Remark 1; Thm. 1's display per the default above. No \label, \eqref, \tag, \newcommand.
REGISTERED STRINGS: none.
EVERY OTHER CAVEAT in checks/caveats.yaml: pointer only ("§6.3", "Appendix D"), never restated. C26: any sentence about the interaction check carries "post hoc".
NEW ROWS OWED:
  - X2-1 (W2): 0.5000 ± 0.0055 measured, 0.5028 predicted, z −0.51 at κ_B = 8, VERIFIED at che/bench/results/phase4/phase4_report.md:72.
  - X2-2 (W2): the toy's optical depths dist_t · ρ̄_t (P3 reports 0.707, 0.898, 0.987), DERIVED from the committed tau_profile in che/bench/results/phase4/m42/e2c_sweep.json (τ_t = exp(−κ_B D_t), so D_t = −ln τ_t / κ_B; show the arithmetic at one κ_B); only if V3Q5's default stands.
OWNER-PENDING:
  - V3Q5 Thm. 1 statement (alternate file alt/13_appendix_proofs.thm1_tf.md: TF's statement with the mismatch stated plainly).
  - V3Q3 Prop. 4 remark (alternate alt/13_appendix_proofs.no_prop4.md: without it; then §7 keeps "no theorem that joint training wins" alone).
  - V3Q4 Remark 2′.
  - v2 D2, D3, D4, D5 (Cor. 1(4); Prop. 3 as an inequality; Def. 1's state; smaller wording).
NOT HERE: Remark 1 (cut); "irreducible"; an ISO-vs-JOINT slack contrast; Prop. 4's constant; "the formal specification" (the theory record is not shipped by default, V3Q16: say "the theory record" only if it ships, else make each statement self-contained); E2C codes outside the listing (say "the corridor toy").
V2 MATERIAL: paper/v2/sections/12_appendix.md (index and A); 06_coupling_b.md §6.2 and 07_comms.md §7.2 for the statements.
DEPENDENCIES: §3 (W2) names these by number; §4.4 (W3) has Remark 2′'s one sentence.
-->

- Appendix A: proofs and formal statements.
- Appendix B: locked constants and hyperparameters.
- Appendix C: reproducibility floors.
- Appendix D: the registration timeline.
- Appendix E: additional results of the worked example.
- Appendix F: the secondary design.
- Appendix G: the post hoc interaction check in full.
- Appendix H: trained-policy episodes.
- Appendix I: how the literature search ran.
- Appendix J: how this paper was made.

### A Proofs and formal statements

This appendix states and proves the results that §3 uses. Where a statement departs from the project's theory document (`docs/theory_foundations.md` in the code supplement), the departure is noted. <!-- OWNER-PENDING:V3Q16 --><!-- OWNER-PENDING:V3Q23 -->

Definitions and results keep that document's numbers, which the code's docstrings cite; this is why Definition 2 follows Definition 7 in §3 and the only numbered remark is 2′. The definitions of §3 are stated as implemented, and four depart from the document. Definition 1 draws the observation from the post-step state, smoke included, as the code does. Definition 3 carries the smoke update and fixes $\iota = 0$<!-- N:DX-1 -->, which the document keeps as a parameter $\iota \ge 0$. For Definition 5, the document states the impulse per collapse event; the implementation draws one uniform per cell, and the two rules coincide wherever seeding neighbourhoods do not overlap. For Definition 7, the document's range-dependent link probability is implemented as a hard Chebyshev range.

**Proposition 1 (Well-posedness and Markov closure).** For every $\theta$, the process $s_t = (x_t, h_t, \rho_t, c_t, k_t, t)$ under any joint policy is a Markov chain, and $\mathcal{M}_\theta$ is a well-defined Dec-POMDP: finite-horizon optimal joint policies exist, and the standard value definitions apply.

**Proof.** Each factor of $T_\theta$ is a conditional kernel, measurable in its conditioning variables, all of which are components of $(s, a)$ or of already-sampled components of $s'$. The dependence of $T_H$ on $c'$ and of $T_K$ on $x'$ is a sequential composition within one time step: sample $c' \sim T_C(\cdot \mid c, x)$, then $h' \sim T_H(\cdot \mid h, c, c')$, then $\rho' = T_\rho(\rho, h')$ (deterministic), then $x' \sim T_X(\cdot \mid x, a, h', c')$, then $k' \sim T_K(\cdot \mid x')$. A composition of Markov kernels is a Markov kernel on the product space, so $T_\theta$ is a valid transition kernel on $\mathcal{S}$ and $(s_t)$ is Markov. The action sets are finite, every stochastic factor and the reset distribution have finite support, and $\rho$ evolves deterministically from $\rho_0 = 0$. The states and observations reachable within the horizon therefore form finite sets; restricted to them, $\mathcal{M}_\theta$ is a finite Dec-POMDP, and optimal finite-horizon joint policies exist by the standard argument. $\blacksquare$

The theory document states that $\mathcal{S}$ and $\Omega_i$ are finite. With the real-valued smoke field in the state, that holds only for the states and observations reachable within the horizon, which is all the argument uses.

Listing 3, the body of `step`, follows the factorization; `tl` is the episode's $\theta$, and no configuration in this paper uses the early `frozen` control branch.

<!-- LISTING 3: block carried byte-for-byte from paper/v2/sections/03_environment.md:58 (Listing 5 in draft1; renumbered in the fix round); move it, never edit it -->

**Listing 3.** One environment step in the order of Proposition 1.

<!-- LISTING: che/env/env.py:298-358 -->
```python
# che/env/env.py:298-358 (verbatim)
    k_struct, k_seed, k_fire = jax.random.split(key, 3)

    # 1. c' ~ T_C(c, x): reads *pre-step* occupancy.
    occ_pre = occupancy_grid(state.agent_pos, state.agent_alive, cfg.grid_size)
    structure_new = structure_step(
        k_struct,
        state.structure,
        state.weak,
        occ_pre.astype(jnp.float32),
        lambda_0=th.lambda_0,
        lambda_load=th.lambda_load,
    )
    collapse_increment = (structure_new == COLLAPSED) & (state.structure == INTACT)

    # 2. h' ~ T_H(h, c, c'): CA spread, then the Coupling A impulse from the
    # collapse increment (seeded cells are Burning in h', spread next step).
    seed_mask = coupling_a_seed_mask(
        k_seed, collapse_increment, kappa_A=tl.kappa_A, r_seed=th.r_seed
    )
    hazard_ca = hazard_step(k_fire, state.hazard, beta=tl.beta, iota=th.iota)
    if cfg.hazard_mode == "frozen":
        # M1.3: h is frozen — the CA/seed draws above still happen and are
        # discarded, so dynamic<->frozen with the same key share every
        # other stream bitwise (invariant #3). Frozen Burning cells stay
        # Burning: lethal and smoke-emitting, but never spread or burn out.
        hazard_new = state.hazard
        seeded_ignitions = jnp.zeros_like(seed_mask)
    else:
        hazard_new = seed_ignitions(hazard_ca, seed_mask)
        seeded_ignitions = hazard_ca != hazard_new  # Fuel cells Coupling A lit

    # 3. rho' from h' (Def. 6; smoke outlives flame).
    smoke_new = smoke_step(state.smoke, hazard_new, sigma_s=th.sigma_s, eta=th.eta)

    # 4. x' ~ T_X + task dynamics. M1.1: lethality/blocking against h'/c'.
    # DECISION: an agent disabled this step does not collect food this step
    # (it died before/on arrival) — occupancy filters on the post-death
    # alive vector, keeping "dead agents never collect" exact.
    pos_new, alive_new, deaths_fire, deaths_collapse, blocked_moves = agent_step(
        state.agent_pos,
        state.agent_alive,
        actions,
        hazard_new,
        structure_new,
        collapse_increment,
        cfg.grid_size,
    )
    occ_post = occupancy_grid(pos_new, alive_new, cfg.grid_size)
    food_new, task_reward = task_step(state.food, occ_post)
    # Def.-2-compliant death penalty: reads only the alpha transition (an X
    # variable) — never hazard/smoke/structure directly.
    reward = task_reward - th.death_penalty * (deaths_fire + deaths_collapse).astype(
        jnp.float32
    )

    # 5. k' ~ T_K(x'): comms channel (Def. 7, M5.0). Reads post-step
    # positions/aliveness only — never h', rho' or c' — and draws from its
    # own fold_in stream, so delta cannot perturb any kernel above.
    links, links_in_range = _comms_obs(
        jax.random.fold_in(key, _COMMS_STREAM), pos_new, alive_new, cfg, tl.delta
    )
```

Listings 4 and 5 carry two claims of §3. In Listing 4 the reveal draw of Definition 6 is made whatever $\kappa_B$ is, with $\kappa_B$ read per episode from the state. Listing 5 runs the environment at $\kappa_B = 0$ with and without masking, under the same keys, and asserts bitwise-identical fire, smoke, structure, food, positions, alive flags and rewards.

<!-- LISTING 4: block carried byte-for-byte from paper/v2/sections/06_coupling_b.md:36 (Listing 2 of §3 in draft1; moved to Appendix A in the fix round, RM-1); move it, never edit it -->

**Listing 4.** Coupling B in the observation kernel: the reveal draw is made whatever $\kappa_B$ is.

<!-- LISTING: che/env/observation.py:300-310 -->
```python
# che/env/observation.py:300-310 (verbatim)
        tau = transmittance(
            state.smoke, state.agent_pos, kappa_B=state.theta_live.kappa_B, k=k
        )
        reveal = jax.random.uniform(key, tau.shape) < tau  # P(seen) = tau
        grid = jnp.concatenate(
            [
                grid * reveal[..., None].astype(jnp.float32),
                reveal[..., None].astype(jnp.float32),
            ],
            axis=-1,
        )
```

<!-- LISTING 5: block carried byte-for-byte from paper/v2/sections/03_environment.md:211 (Listing 4 of §3 in draft1; moved to Appendix A in the fix round, RM-1); move it, never edit it -->

**Listing 5.** With $\kappa_B = 0$, trajectories and rewards are bitwise those of the environment before masking.

<!-- LISTING: che/tests/test_coupling_b.py:131-142 -->
```python
# che/tests/test_coupling_b.py:131-142 (verbatim)
def test_kappa_b_zero_bitwise_recovers_obs_v2():
    """Nesting (M4.1): obs v3 at kappa_B = 0 is the pre-masking env plus a
    constant all-ones visibility plane — state trajectories, rewards, and
    content planes bitwise identical to obs v2 under the same keys."""
    theta = dataclasses.replace(_HOT, kappa_B=0.0)
    cfg3 = EnvConfig(grid_size=L, n_agents=4, horizon=64, theta=theta)
    cfg2 = dataclasses.replace(cfg3, obs_version=2)
    a = _traj(theta, cfg=cfg3)
    b = _traj(theta, cfg=cfg2)
    _assert_bitwise_equal(
        a, b, ("hazard", "smoke", "structure", "food", "pos", "alive", "reward")
    )
```

**Proposition 2 (Bond percolation).** Under Definition 3 with $\iota = 0$ and a single ignition at the origin, the set of eventually-Burnt cells is equal in distribution to the open cluster of the origin in i.i.d. bond percolation on $(G, E)$ with edge-open probability $\beta$, where $E$ is the arena's set of von Neumann edges.

**Proof (coupling).** Attach to each unordered edge $e = \{g, g'\}$ an independent $B_e \sim \mathrm{Bernoulli}(\beta)$, and declare that a transmission attempt across $e$ succeeds if and only if $B_e = 1$. Each edge is attempted at most once: when one cell of $e$ first Burns while the other is Fuel, one attempt occurs; afterwards the burning endpoint is Burnt, which is absorbing. If the other endpoint later Burns via a different path, its neighbour across $e$ is already Burnt, so no second attempt occurs. Run with the variables $\{B_e\}$, the fire therefore burns exactly the connected component of the origin in the subgraph of open edges $\{e : B_e = 1\}$, which is the bond-percolation cluster. $\blacksquare$

This is the correspondence between an epidemic with a constant infectious period and bond percolation described by Grassberger (1983)<d-cite key="grassberger1983"></d-cite>. The implementation realizes it exactly: it draws one uniform per cell and incoming direction (`che/env/hazard.py:8-16`), and with a one-step burn time each unordered edge sees at most one attempt, so these uniforms are the coupling's per-edge variables. Coupling A, when on, adds ignitions and breaks the hypotheses.

**Corollary 1 (Phase structure).** On $\mathbb{Z}^2$ with the von Neumann neighbourhood, the fire of Definition 3 with $\iota = 0$ and a single ignition at the origin inherits the phase structure of bond percolation (Proposition 2, whose coupling holds on any graph):

1. Its critical point is $\beta_c = 1/2$ exactly, the critical probability of bond percolation on the square lattice (Kesten, 1980)<d-cite key="kesten1980"></d-cite>.
2. For $\beta > \beta_c$ the fire spreads indefinitely with positive probability. On that event the cells ignited by step $n$ are those within $n$ open edges of the origin. Scaled by $1/n$, they converge almost surely in Hausdorff distance to a deterministic convex compact set with non-empty interior, invariant under permutations and reflections of the coordinates (Garet & Marchand, 2004; their Corollary 5.4)<d-cite key="garet2004chemical"></d-cite>. The growth is therefore linear in $n$, at a speed given in each direction by the extent of that set.

<!-- v2 D2 (Corollary 1, item 2 at the Garet and Marchand level) is still open; kept at v2's verified level. -->

Both items concern the idealized kernel (von Neumann neighbourhood, constant burn time, homogeneous fuel, no wind) on the infinite lattice; CHE's arena is finite, so §4.1 places the levels against a measured threshold. The theory document's corollary also lists the subcritical regime and the critical exponents near $\beta_c$; the paper uses neither, so they are omitted, and its fourth item is numbered 2 here.

**Proposition 3 (Collapse events dominate hazard exposure).** Work in the subcritical regime $\beta < \beta_c$ with $\iota = 0$, and suppose collapse events arrive at rate $\lambda_A$ per step, each seeding one ignition at a uniformly located Fuel cell, with seeded clusters pairwise disjoint (the sparse regime, $\lambda_A T \chi(\beta) \ll \lvert G \rvert$, the number of cells). Then the expected burnt area $B_T$ by time $T$ satisfies

$$
\begin{aligned}
\mathbb{E}[B_T] &= \lambda_A T\,\chi(\beta)\,\big(1 + o(1)\big), \\
\text{and in general} \quad \mathbb{E}[B_T] &\le \lambda_A T\,\chi(\beta),
\end{aligned}
$$

where $\chi(\beta)$ is the mean percolation cluster size. Consequently the marginal hazard exposure per unit of structural instability is $\partial\,\mathbb{E}[B_T]/\partial\lambda_A = T\chi(\beta)$.

<!-- v2 D3 (Proposition 3 as an inequality; the derivative stated as an equality) is still open; kept at v2's verified level. -->

**Proof.** Each collapse seed grows, by Proposition 2, a burnt cluster equal in distribution to a bond-percolation cluster, of expected size $\chi(\beta)$. By linearity of expectation over the Binomial or Poisson number of seeds, the total expected burnt area is $\lambda_A T \chi(\beta)$ when clusters are disjoint; overlaps only remove double counting, which gives the upper bound in general. $\blacksquare$

The theory document adds a divergence rate near the critical point, which rests on critical exponents the paper does not state. In a finite protocol the equality is approached only when four conditions are matched, each with a known sign. They are an unconditional cluster-mass reference (a spanning-conditioned one underestimates it), seed location (boundary clipping lowers the mass of uniformly placed seeds), seed age (seeds born late have not reached full mass, which lowers the measured slope; at β = 0.43<!-- N:CAL-3 --> mass saturates by an age of about 64 steps<!-- N:DX-409 -->), and sparsity (sibling seeds and cluster overlap deflate the measured slope).

Two<!-- N:DX-304 --> runs check the proposition, neither at the locked parameters, both without agents or primary ignition at the subcritical Low level ($\beta = 0.43$, $\iota = 0$<!-- N:DX-304 -->), so collapse is the fire's only birth channel. The first, a dense sweep on a 64 × 64<!-- N:CA-2 --> grid ($\kappa_A = 0.02$, $f_{\mathrm{weak}} = 0.4$<!-- N:CA-2 -->), fits burnt area against realized seeds through the origin: $R^2 = 0.998$<!-- N:CA-2 --> over a 14×<!-- N:CA-2 --> range of the expected seed count. The second, a slower test in the suite on a 32 × 32<!-- N:CA-3 --> grid ($\kappa_A = 0.003$<!-- N:CA-3 -->), divides its slope by a protocol-matched reference computed inside the test: 0.992<!-- N:CA-3 -->, inside the band [0.90, 1.02]<!-- N:CA-3 -->, with $R^2 = 0.9995$<!-- N:CA-3 -->. In both, the four factors compose to the observed slope within Monte Carlo error.

<!-- OWNER-PENDING:V3Q5 -->

**Theorem 1 (Memorization gap, and its erosion by Coupling B).** Consider the corridor toy at attenuation strength $\kappa_B$: from a start cell, a path of $d$ steps leads to a branch $b$, from which two disjoint corridors $L$ and $R$ of length $\ell$ lead to the goal; the horizon is $T = d + \ell$ (zero slack: a wrong commitment cannot be undone). At $t = 0$ nature draws $Z \in \{L, R\}$ uniformly; corridor $Z$ burns at depth $\ell_f \ge 1$ beyond $b$, and an agent entering it is disabled. The reward is 1 for reaching the goal by $T$, else 0. At each step $t = 0, \dots, d$ the agent receives the signal $Y_t = Z$ with probability $\tau_t(\kappa_B) = e^{-\kappa_B D_t}$, else $Y_t = \varnothing$, where the optical depth $D_t > 0$ of its line of sight to the fire, per unit $\kappa_B$, does not depend on $\kappa_B$. Signals are independent across time and remembered. Let

$$
q(\kappa_B) = 1 - \prod_{t=0}^{d} \big(1 - e^{-\kappa_B D_t}\big)
$$

be the probability of being informed by the commitment point. Then (1) the optimal value is $J^*(\kappa_B) = \tfrac12 + \tfrac12 q(\kappa_B)$; (2) the policies optimal for the fixed-map variant ($Z \equiv z_0$ constant) include the signal-blind policy "always take the corridor other than $z_0$", whose value on the toy is $\tfrac12$ for every $\kappa_B$, so the memorization gap is $J^*(\kappa_B) - J^{\mathrm{static}} = \tfrac12 q(\kappa_B) > 0$ for all finite $\kappa_B$; and (3) $q$ is continuous and strictly decreasing in $\kappa_B$, with $q(0^+) \to 1$ and $q(\kappa_B) \to 0$ as $\kappa_B \to \infty$, so under total perceptual denial the optimal adaptive policy is no better than the memorizing one.

**Proof.** (1) With zero slack, the only decision is the corridor choice at $b$; waiting or probing is impossible within $T$. If informed (probability $q$), taking the corridor other than $Z$ succeeds with probability 1; if not, both corridors are exchangeable given the history, and any choice succeeds with probability $\tfrac12$. Hence $J^* = q + (1-q)\tfrac12 = \tfrac12 + \tfrac{q}{2}$, and no policy exceeds this, since success requires information or a lucky guess. (2) In the fixed-map environment the signal is uninformative, so the signal-blind policy is among the optimal ones there; on the toy it succeeds if and only if $Z = z_0$, with probability $\tfrac12$. (3) Because every $D_t > 0$, each factor $(1 - e^{-\kappa_B D_t})$ is continuous and strictly increasing in $\kappa_B$ on $(0, \infty)$, so the finite product is too, and $q$ is continuous and strictly decreasing. The product tends to 0 as $\kappa_B \to 0$ and to 1 as $\kappa_B \to \infty$. $\blacksquare$

The proof uses only that the signals are independent and remembered, that $q$ is the probability of being informed, and, in part (3), that $D_t > 0$. The theory document states the theorem for unit smoke density over the integer distance to the fire, the special case $D_t = d - t + \ell_f$; this statement departs from it because the implemented toy (`che/env/e2c.py`) is not that case. The toy runs the production smoke update and observation kernel (Definitions 3 and 6) on a fire cell held Burning, at $d = 2$ and $\ell_f = 2$<!-- N:X2-5 -->. Its $D_t$ is therefore the Euclidean distance to the fire times the quadrature mean of a single smoke cell that grows each step. Its depths are $D_0, D_1, D_2$ = 0.707, 0.898, 0.987<!-- N:X2-2 -->, where the integer-distance form has 4, 3 and 2<!-- N:X2-4 -->; at $\kappa_B = 1$ its $q$ is 0.8115<!-- N:X2-3 -->, where that form gives 0.193<!-- N:X2-4 -->.

Part (3) fails when some $D_t = 0$. A larger geometry tried first ($d = 6$, a 17 × 17 crop<!-- N:X2-6 -->) had $\tau = 1$ exactly at the first two<!-- N:X2-6 --> steps, because the four-point<!-- N:X2-7 --> quadrature never sampled the single smoke cell at that range, so $q \equiv 1$ for every $\kappa_B$.

The toy also leaks $Z$ through the visibility plane: smoke sits only on the fire's side, so the mirror corridor's cell is always revealed, and the pattern of reveals alone identifies $Z$. $J^*$ is therefore the value of the content channel (the burning and smoke planes), the only input the scored policies read, which a test enforces. The construction is kin to the irreversible commitment in Proposition 1 of Chen et al. (2022)<d-cite key="chen2022understandingdr"></d-cite>.

The measured value of the policy the proof shows optimal (if informed, take the corridor other than $Z$; else a fixed one) matches $\tfrac12 + \tfrac12 q$, with $q$ computed from the toy's own transmittances on an independent random stream, under a three-condition check over the sweep of $\kappa_B$: largest $\lvert z \rvert$ 2.11, $\sum z^2 = 6.55$ on 8 degrees of freedom ($p = 0.586$), and mean $z$ −0.44<!-- N:CB-4 -->. At $\kappa_B = 8$ it is 0.5000 ± 0.0055 against 0.5028 predicted ($z$ −0.51)<!-- N:X2-1 -->. The memorizing policy stays at ½ (largest deviation 0.0084), and $J^*(0) = 1.0000$<!-- N:DX-14 -->.

**Remark 2′ (Value of communication).** Extend the corridor toy of Theorem 1 with a second agent; §4.4 refers to this remark. (i) Under a team-any reward, communication has zero marginal value when the agents are interchangeable, expendable (no death cost) and at least as numerous as the hypotheses: coverage then achieves $J = 1$ under total denial. When any qualifier fails, value returns; in general it scales with the deficit of agents relative to hypotheses, and a death cost, such as CHE's $d_p = 0.5$<!-- N:ENV-1 -->, prices the redundancy that substitution spends. (ii) In the courier variant, where only agent 1 can complete the task and it observes the other agent only through messages, the denied optimum within the no-idle policy class is $\tfrac12 + \tfrac12 q(\kappa_B)$; with slack $\ell_f$, optimal denied play buys information by idling at the branch and achieves $\tfrac12 + \tfrac12 \tilde q(\kappa_B)$, where $\tilde q$ is the probability of being informed by the commitment point under the best idling schedule, with $\tilde q \ge q$ (equality iff $\ell_f = 0$), so

$$
\mathrm{VoC}_{\mathrm{true}}(\kappa_B) = \tfrac12\big(1 - \tilde q(\kappa_B)\big) \le \tfrac12\big(1 - q(\kappa_B)\big).
$$

Both $q$ and $\tilde q$ decrease in $\kappa_B$, so the value of communication increases with perception decay. <!-- OWNER-PENDING:V3Q4 -->

The commitment draws have different optical depths, so as $\kappa_B \to \infty$ the lowest-depth draw dominates both products and $\tilde q / q \to 1$. The correction peaks at moderate $\kappa_B$, and its relative bite on the value of communication is largest at low $\kappa_B$, where $q$ is near 1.

In the courier variant with scripted policies, run through the production link kernel and the shared transmittance function, free communication scores 1.0000 at every $\kappa_B$<!-- N:DX-15 -->. The no-idle denied arm matches $\tfrac12 + \tfrac12 q$ (largest absolute z 0.44; χ² 0.51 on 8 degrees of freedom<!-- N:DX-15 -->), so $\mathrm{VoC}_{\mathrm{gated}} = \tfrac12(1 - q)$ rises monotonically from 0 to 0.498<!-- N:COM-1 -->. In this two-agent toy, which is not CHE (4096 episodes and 8192 Monte Carlo draws per point<!-- N:DX-15 -->), $\tilde q / q$ is 1.126 at $\kappa_B = 1.0$ and peaks at 1.235 near $\kappa_B = 2$<!-- N:DX-15 -->. The correction removes 79 %, 54 % and 7 % of $\mathrm{VoC}_{\mathrm{gated}}$ at $\kappa_B$ = 0.5, 1.0 and 3.0<!-- N:DX-15 -->.

<!-- OWNER-PENDING:V3Q3 -->

**A transfer bound for a fixed policy (remark).** For a fixed policy and two configurations that share the reward, the difference between the policy's discounted returns is bounded above by a term that grows with how far their transition and observation kernels differ. It follows by telescoping the two models' evaluation operators along the trajectory distribution. Every configuration the isolated arm trains on (§6.2) differs from the test configuration $\theta^*$ on the states where both couplings act at once, such as a collapse increment next to Fuel with an agent within attenuation range. There $\theta^*$ places mass of order $\kappa_A$ on ignition transitions that a configuration with $\kappa_A = 0$ places elsewhere, and the observation kernels differ wherever $\kappa_B$ differs.

The remark bounds what isolated training can be guaranteed to transfer, not what happens. An upper bound on the isolated arm's transfer does not lower-bound the realized gap; compositional generalization can emerge from isolated training, and the experiment decides. The theory document displays the bound with a constant and concludes more about the isolated arm's slack than an upper bound can show; this remark draws no such conclusion. Its prediction about exposure to that region was not tested, since the counter of §3.5 cannot measure it.

<!-- PAPER V3 DRAFT (PAPER V3 ruling, 2026-10-12): builder-drafted, not owner-approved -->

### B Locked constants and hyperparameters

<!-- STUB-SPEC
JOB: Every locked constant with its value (dates live in Appendix D), the hyperparameters and budget, the message encoder (Listing 6), and Coupling B's lock bands that did not intersect.
WRITER: W2.
BUDGET: about 350 prose words plus tables.
FROM: P1 §6.1 B; B1 (Listing 6 moved here from v2 §7, page budget).
ROWS: CAL-1, CAL-3, CA-1, CB-1, COM-6, ENV-1, ENV-12, DX-1, DX-2, DX-3, DX-17, DX-401, DX-402 (values only; dates to Appendix D), CB-2, CB-3, DX-12, DX-301, DES-13.
LISTINGS: Listing 6, che/train/ippo.py:323-329 (stop_gradient: the message encoder is frozen; ENV-12). Block below.
REGISTERED STRINGS: none.
EVERY OTHER CAVEAT in checks/caveats.yaml: pointer only ("§6.3", "Appendix D"), never restated. C26: any sentence about the interaction check carries "post hoc".
NOT HERE: ruling dates (Appendix D); study codes without the key; "lock record" phrasing aimed at a reader who cannot see it.
V2 MATERIAL: paper/v2/sections/13_appendix_locks_floors.md (B); 06_coupling_b.md §6.3; 07_comms.md (Listing 6).
DEPENDENCIES: §3 points here for hyperparameters and the encoder.
-->

Each constant below was fixed before the main experiment; Appendix D gives when. A test in the code supplement (`che/tests/test_locks.py`) checks each against the configurations, the code defaults or the analysis scripts that must carry it.

| constant | value | described in |
|---|---|---|
| critical point $\hat\beta_c$ | 0.500 ± 0.005<!-- N:CAL-1 --> | §4.1, with its estimator's provenance |
| β at Low / Medium / High | 0.43 / 0.49 / 0.70<!-- N:CAL-3 --> | §4.1 |
| β held out ($\theta^*$) | 0.49<!-- N:CAL-3 --> | §6.2 |
| $f_{\mathrm{weak}}$, $\lambda_0$, $\lambda_{\mathrm{load}}$, $\kappa_A$, $r_A$ | 0.15, 5e-5, 4e-4, 0.06, 1<!-- N:CA-1 --> | Definition 5 |
| smoothing passes of the weak-terrain field | 2<!-- N:DX-401 --> | Definition 5 |
| $\kappa_B$ | 1.0<!-- N:CB-1 --> | Definition 6; the bands below |
| δ off / on; $R_{\mathrm{comm}}$ | 0.0 / 1.0<!-- N:DX-401 -->; 16<!-- N:COM-6 --> | Definition 7 |
| death penalty $d_p$ | 0.5<!-- N:ENV-1 --> | Definition 2 |
| observation encoding | the observation as masked by smoke<!-- N:DX-401 --> | Definition 6 |
| $\sigma_s$, η, ι | 1.0, 0.5, 0.0<!-- N:DX-1 --> | Definition 3; not locked, fixed by convention and never calibrated |

The analysis constants of the worked example (§6) are fixed the same way.

| constant | value | role |
|---|---|---|
| `K_CONFIRMATORY` | 40<!-- N:DES-1 --> | design seeds per confirmatory arm, the base of the registered seed rule |
| `K_LADDER_CAP` | 60<!-- N:DES-1 --> | the seed rule's cap |
| `K_CONFIRMATORY_REALIZED` | 72<!-- N:DES-13 --> | the seed count at which Γ is read (§6.2; history in Appendix D) |
| `K_SECONDARY` | 20<!-- N:DES-13 --> | seeds per secondary arm; ISO-4 uses the same count |
| `SIDAK_M`; $z_\alpha$ | 2; 2.2365<!-- N:DES-13 --> | the two co-primary tests, Šidák-corrected |
| `POWER_STOP` | 0.80<!-- N:DX-402 --> | the minimum design-stage power |
| `T_STAR` | 1000<!-- N:DES-13 --> | the training budget in updates |
| `GAMMA_T_RETENTION` | 11<!-- N:DES-13 --> | checkpoints kept for Γ(t): updates 500–1000 every 50<!-- N:DES-13 --> |
| evaluation draw | seed 0 × 512 episodes<!-- N:DES-13 --> | common to every run; not in the constant registry |
| `PLATEAU_PASS`; `PLATEAU_REVIEW` | 1.0; 1.5<!-- N:DX-402 --> | thresholds of a convergence check, retired when the estimand was fixed at a matched budget, before the main training runs |

Every run of the worked example uses the hyperparameters below. The main training runs pass none on the command line, so the configured defaults apply.

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
| network | two convolutions with 16 and 32 channels, a dense layer of 128 units, actor and critic heads with a 64-unit layer each<!-- N:ENV-10 --> |
| messages | dimension 8, delivered one step later as a masked mean over open links<!-- N:DX-17 --> |

The strength $\kappa_B$ was to be locked where three<!-- N:DX-301 --> bands set before calibration intersect. They were a masked share of the crop at Medium in [0.15, 0.45]<!-- N:DX-301 -->, a probability in [0.4, 0.7]<!-- N:DX-301 --> that a Burning cell three<!-- N:DX-301 --> cells away is revealed at Medium, and the corridor toy's $q$ (Theorem 1) in [0.3, 0.7]<!-- N:DX-301 -->. They do not intersect. The masked-share band cannot be reached at Medium: the masked share can only approach the share of crop cells with smoke on their line of sight, 0.130<!-- N:DX-12 --> there under a random policy, below the band's lower edge of 0.150<!-- N:DX-12 -->. The same $\kappa_B$ attenuates the arena's extended smoke more strongly than the toy's single smoke source, which leaves the detection and toy bands disjoint by a factor of 1.35 under a random policy and 1.15 under probe policies<!-- N:CB-2 -->. $\kappa_B = 1.0$<!-- N:CB-1 --> was therefore locked on the detection band alone; the masked-share band was retired, not widened, and the toy band was kept as a consistency check.

The one ablation of the death penalty $d_p$ ran the fire alone with no coupling, for 500<!-- N:ENV-2 --> updates with 3<!-- N:ENV-2 --> seeds per setting, on an older observation encoding; it reports training-log means over the final updates and was not re-run. Raising $d_p$ from 0<!-- N:ENV-2 --> to 0.5<!-- N:ENV-1 --> moved survival at High severity from 0.575 to 0.866<!-- N:ENV-2 --> and completion there from 0.765 to 0.821<!-- N:ENV-3 -->. Survival at Medium moved from 0.931 to 0.951<!-- N:ENV-4 -->, and Low stayed tied, 0.991 against 0.992<!-- N:ENV-5 -->.

No gradient crosses the communication channel, so the message head, a tanh-bounded dense layer on the shared trunk, stays at its initialization<!-- N:ENV-12 -->: an agent emits a fixed random projection of trunk features that are themselves trained. The receivers' weights on the message inputs are trained, which makes message use testable; what to say was never learned.

<!-- LISTING 6: block carried byte-for-byte from paper/v2/sections/07_comms.md:39; move it, never edit it -->

**Listing 6.** Delivered messages carry no gradient, so the message encoder stays at its initialization.

<!-- LISTING: che/train/ippo.py:323-329 -->
```python
# che/train/ippo.py:323-329 (verbatim)
        # Messages emitted this step are delivered next step. Nothing crosses
        # an episode boundary (autoreset), and stop_gradient states in code
        # what the batch-storage already implies: the channel is not a
        # differentiable path (Q3 ruling; networks.py docstring).
        messages = jax.lax.stop_gradient(
            jnp.where(done[:, None, None], 0.0, emitted)
        )
```

<!-- PAPER V3 DRAFT (PAPER V3 ruling, 2026-10-12): builder-drafted, not owner-approved -->

### C Floors

<!-- STUB-SPEC
JOB: Every floor with its GPU, run length, artifact and reps; the exhibits §5 no longer tells, one line each; the floors explorer.
WRITER: W3.
BUDGET: about 500 prose words plus the floor table.
FROM: P1 §6.1 C; P2 §3 A2.
ROWS: METH-1 to METH-5, DX-34, DX-35, DX-38, DX-302, DX-403, DX-412, V5-1, V5-2, V5-3, CB-7, COM-5, HW-1, DES-13.
FIGURES: Figure C1 floors_explorer (gloss once: labelled “M5.1e”, labelled “M6.0”, labelled “per card”, labelled “beat”). Block below.
REGISTERED STRINGS: VOID (comms condition (iii), COM-5).
EVERY OTHER CAVEAT in checks/caveats.yaml: pointer only ("§6.3", "Appendix D"), never restated. C26: any sentence about the interaction check carries "post hoc".
NOT HERE: "floors grow ordered by curriculum difficulty" (an untested hypothesis, METH-5 note); "every bar has a floor".
V2 MATERIAL: paper/v2/sections/13_appendix_locks_floors.md (C); 08_methodology.md (the exhibits).
DEPENDENCIES: §5 points here.
-->

A floor is the standard deviation of a metric over identical reruns at one seed, so it measures nondeterminism alone (§5). The table lists every floor this paper uses, with its GPU, run length, artifact and number of reruns. Paired values are ISO, then JOINT. Each study is named in plain words with its code (key in Appendix D). The confirmatory arms' floors use eight<!-- N:DX-403 --> reruns, because four leave a standard deviation uncertain by about ±40 %<!-- N:DX-303 -->.

| study (code) | GPU, updates | arms or artifact | reruns | floor | use |
|---|---|---|---|---|---|
| four-run Medium floor study (M5.1e) | RTX 5090, 500<!-- N:DX-403 --> | Medium | 4<!-- N:DX-403 --> | completion 0.0145, survival 0.0129<!-- N:METH-1 --> | the content ablation's Medium threshold |
| denial study (M5.5) | RTX PRO 6000, 500<!-- N:DX-412 --> | Medium, communication range 16<!-- N:METH-1 --> | 4<!-- N:DX-412 --> | completion 0.0399, survival 0.0130<!-- N:METH-1 --> | the denial thresholds (§4.4); the per-GPU exhibit |
| denial study, danger moments (M5.5) | RTX PRO 6000, 500<!-- N:DX-412 --> | Medium | 4<!-- N:DX-412 --> | 27.2 % (sd 0.00182)<!-- N:COM-5 --> | voids a 20 %<!-- N:COM-5 --> threshold |
| content ablation at High (M5.3b) | RTX PRO 6000<!-- N:DX-403 -->, 500<!-- N:DX-40 --> | High | 4<!-- N:DX-40 --> | completion 0.0522<!-- N:V4-3 -->, survival 0.0621<!-- N:CB-7 --> | the High content ablation's thresholds; a reference scale (cross-artifact) in §4.3 |
| refactor of the environment code (M6.0) | RTX PRO 6000<!-- N:DX-5 --> | two code versions | 4 comparisons<!-- N:METH-2 --> | reference version: 0 of 760 per-field trajectory hashes differ, in 4 of 4 comparisons; refactored version: differs in 1 of 4<!-- N:METH-2 --> | the per-artifact exhibit |
| confirmatory arms' floor study, 500 updates (M6.2) | RTX PRO 6000, 500<!-- N:DX-34 --> | ISO, JOINT | 8<!-- N:DX-403 --> | completion 0.0165, 0.0093<!-- N:DX-34 --> | the retired convergence check |
| confirmatory arms' floor study, 1000 updates (M6.2b) | RTX PRO 6000, 1000<!-- N:DX-34 --> | ISO, JOINT | 8<!-- N:DX-403 --> | completion 0.0339, 0.0483<!-- N:DX-34 --> | set the design seed count, k = 40<!-- N:DES-1 --> |
| the grid's launch floor study (G1.2 protocol) | RTX PRO 6000<!-- N:DES-5 -->, 1000<!-- N:DX-403 --> | ISO, JOINT, sweep arm at p = 0.5<!-- N:DX-28 --> | 8<!-- N:DX-403 --> | sd(Γ) at k = 40: completion 0.00504, survival 0.00310<!-- N:DES-5 --> | design-stage power |
| re-measurement before the grid | RTX PRO 6000<!-- N:DES-2 -->, 1000<!-- N:DX-412 --> | ISO, JOINT, sweep arm at p = 0.5<!-- N:DX-28 --> | 8<!-- N:DX-403 --> | the seed rule gave k = 46<!-- N:DES-2 --> | the registered seed rule (Appendix D) |
| re-measurement on the grid's GPU | RTX 5090<!-- N:DX-35 -->, 1000<!-- N:DX-412 --> | ISO, JOINT, sweep arm at p = 0.5<!-- N:DX-28 --> | 8<!-- N:DX-35 --> | completion 0.0587, 0.0577; survival 0.0100, 0.0112<!-- N:DX-35 --> | the seed rule (k = 72<!-- N:DES-3 -->); the check that an effect exceeds rerun noise |
| High readout | the grid GPU's floor runs (1000<!-- N:DX-412 --> updates), evaluated at High on a third GPU of the same model<!-- N:V5-2 --> | ISO, JOINT at High | 8<!-- N:V5-2 --> | completion 0.0681, 0.0613; survival 0.0180, 0.0395<!-- N:V5-2 --> | the rerun-noise check at High (Appendix E) |
| evaluation | the same third GPU<!-- N:HW-4 --> | two checkpoints<!-- N:HW-2 --> | 4<!-- N:HW-2 --> | bit-identical<!-- N:HW-2 --> | evaluation reproducibility (§8) |
| partial re-measurement on a second rented GPU | not recorded<!-- N:DX-36 -->, 1000<!-- N:V5-3 --> | ISO, JOINT | 8 + 4<!-- N:DX-36 --> | none reported | provenance only |

The grid GPU's floors cannot be told apart from those of the re-measurement before the grid: the 95 %<!-- N:DX-35 --> intervals for the standard deviation overlap (ISO completion: [0.0186, 0.0571] on the RTX PRO 6000, [0.0388, 0.1194] on the RTX 5090<!-- N:DX-35 -->). No claim is made that either GPU is less reproducible.

- **Thresholds set before the protocol.** Before the protocol existed, four<!-- N:V5-1 --> thresholds were set on constants the record later called invented. The Coupling-B calibration grid graded its High survival effect against a two-seed spread of 0.0295<!-- N:DX-38 -->, below the High floor later measured at 0.0621<!-- N:CB-7 -->, and its "strong" grade was retracted. The content ablation at Medium applied a floor hard-coded from the four-run Medium floor study instead of one measured on its own runs. Re-sited at High, it measured its floor first, but matching Medium's resolution would have taken roughly 46<!-- N:DX-302 --> seeds per arm. The denial study set a 20 %<!-- N:COM-5 --> threshold on danger-moment outcomes below that quantity's rerun nondeterminism of 27.2 %<!-- N:COM-5 -->, so that condition is VOID: the observed 23.2 %<!-- N:COM-5 --> exceeded the threshold but not the noise.
- **The content checks of communication.** These used the thresholds in the table's first and fourth rows. At Medium (two<!-- N:COM-2 --> seeds), no pair of actual, zeroed and shuffled messages differed beyond about 3 points<!-- N:COM-2 -->; at High, raising the mean number of in-range partners from 1.01 to 2.99<!-- N:COM-3 --> changed nothing.
- **Per GPU.** The Medium completion floor moved from 0.0145 to 0.0399, 2.75-fold<!-- N:METH-1 -->, while survival's stayed at 0.0129 against 0.0130<!-- N:METH-1 -->. The GPU, the code version and the configuration all differed between the two studies, so the exhibit cannot say which of them moved the completion floor.
- **Per artifact.** In the refactor of the environment code, the reference version's rerun floor read zero, so two<!-- N:METH-2 --> masking diagnostics at High that differed between the versions looked like a semantic change. The refactored version then differed from itself 1 time in 4<!-- N:METH-2 --> on the same channels. An equivalence claim between A and B needs A against A and B against B, as well as A against B.
- **The contrast's standard error.** At k = 34<!-- N:METH-3 -->, on the 1000<!-- N:DX-34 -->-update completion floors and a 0.03<!-- N:DES-4 --> effect, each arm's own $s\sqrt{2/k}$ gave 92.1 % and 62.8 %<!-- N:METH-3 --> power, where the contrast's power was 76.7 %<!-- N:METH-3 -->.
- **The 80 %-power rule.** The confirmatory seed count was first set at k = 20<!-- N:METH-4 --> on a bare 2σ figure, without the Šidák correction for the two co-primaries ($z_\alpha = 2.2365$<!-- N:DES-13 -->). Corrected, completion had 55.6 %<!-- N:METH-4 --> power against its motivating effect band, a slip caught before any run.
- **Run length.** From 500 to 1000<!-- N:DX-34 --> updates, the completion floor grew 2.1-fold for ISO and 5.2-fold for JOINT<!-- N:METH-5 -->, with run length confounded with machine.
- **Dividing by a floor.** A registered convergence check divided each arm's late-training drift by its floor, so it fired when JOINT's floor fell faster than its drift. It was retired before the grid, and the estimand was fixed as the gap at a matched budget of 1000<!-- N:DES-13 --> updates.
- **Differenced tests.** In 24 of 24<!-- N:DX-32 --> rendered episodes of the Coupling-B calibration grid, the alive agents' centroid drifted towards a wall (rendered-pixel centroids, a diagnostic). That grid's condition "no cross-arm exposure/positioning difference" could not see a drift present in both arms.
- **Coverage.** In the secondary design, floors exist only for the sweep arm at p = 0.5<!-- N:DX-28 -->; the other sweep arms assume that floor, and the identification arm has none<!-- N:DX-306 -->. ISO-4 has no identical reruns, so the contrasts that involve it are graded on seed dispersion alone.

<!-- FIGURE C1: block carried from paper/v2/sections/08_methodology.md:22 (markup, iframe height and alt text as v2 had them); caption replaced; alt text checked by W3 against the figure (kept) -->

<figure class="l-page">
  <iframe src="{{ 'assets/html/submission/floors_explorer.html' | relative_url }}" width="100%" height="472" style="border:none" title="Floors explorer: reproducibility floors per GPU, per artifact and per run length, and the confirmatory grid against its floor" loading="lazy"></iframe>
  <figcaption><strong>Figure C1.</strong> Reproducibility floors, one tab each. The first tab shows the Medium floors of the four-run floor study on an RTX 5090 (labelled “M5.1e” on the figure) and of the denial study (M5.5) on an RTX PRO 6000, labelled “per card” on the figure; “card” is the GPU, “box” the machine and “code tree” the code version. The second shows rerun comparisons within and between two versions of the environment code (labelled “M6.0” on the figure), where “traced” is the refactored version, “baseline” the reference and “field digests” per-field trajectory hashes. The third shows completion floors at 500 and 1000<!-- N:DX-34 --> updates, and the fourth the confirmatory grid's seed dispersion against its floor, with survival's gap against its floor-based standard error, labelled “floor-basis sd(Γ)” on the figure. <span class="interact">Click a tab or press ← / →; hover or tab to a mark.</span></figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/floors_explorer.png" class="img-fluid" alt="Reproducibility floors on two GPUs, rerun comparisons of two versions of the code, floor growth from the shorter to the longer run length, and the confirmatory grid's seed dispersion against its floor, each with its confound stated." caption="Static companion of Figure C1 for the printed PDF." %}
</div>

<!-- PAPER V3 DRAFT (PAPER V3 ruling, 2026-10-12): builder-drafted, not owner-approved -->

### D Registration timeline

<!-- STUB-SPEC
JOB: The audit trail that leaves the main text (V3-S2): every date, ruling, provenance item, GPU block, study code, seed and archive, plus the registration statement (V3-V2) and the framing change (V3-F5's second home). Plain, dated, sourced.
WRITER: W4.
BUDGET: about 1,000 prose words plus tables and verbatim quotations.
FROM: V3-S2; P1 §6.2; v2 BRIEF §7 (the F3 table); v2 Appendices D to F; P3 §3.1 point (5).
ORDER:
  - D.1 Registration statement (V3-V2): the record is internal and version-controlled; its dates are self-reported; the supplement carries the registration documents (phase6_design_v2.md, phase6_framing_branches.md) with a hash manifest; a public registry (OSF) next time. What a reader can check, and what rests on the authors' history (this checkout is shallow; the full-history check is the owner's, V3Q16).
  - D.2 Dated events (table: date | event | row/source): environment locks (DX-401, DX-402); the comms axis closed as inert 2026-07-30 (V6-2); design registered 2026-08-02 with δ retained, two δ-only components of six in ISO, δ excluded from the sweeps (V6-3); co-primaries ruled 2026-08-02 (DES-12); outcome branches and falsifier 2026-08-13 (DES-12); the frozen plan amended 2026-08-13 (V6-5); the bias identified 2026-08-16 by a review of the registered design, pre-grid (V6-1); grid 2026-09-09 to 09-22 (DES-12); the bias and ISO-4 with its reading rule registered 2026-09-18, mid-grid, 120 of 252 runs, on the owner's attestation (DES-15; log:3907-3909); pre-unblind rulings and the fifth outcome cell 2026-09-26 (DX-405, DX-102); unblinding 2026-09-26 (DES-12); the secondary specification ratified after Γ and before the sweep was read (DX-413); the same-GPU replicate proposed after Γ₄ was seen (DES-15); the framing change 2026-10-12 (X4-5). Use the v2 BRIEF §7 table (copied verbatim in this BRIEF) for the F3 rows; state no day count.
  - D.3 Quotations, verbatim, with their dates: the frozen plan's estimand and reading rules (v2 Appendix D items, trimmed to the rules the paper uses; never paraphrase inside a quotation; a "§" inside a quotation is the record's own); the registered outcome branches table (PFB:101-104, venue-lean column omitted and said so), the fifth cell A_c (DX-405, DX-102); the falsifier and its margin (RES-5); branch B's registered headline "composition is paid in agents, not task return" no longer holds as worded; "the branch label stays B"; branch A, the founding hypothesis, did not occur. If the owner agrees (V3Q22), note that the registration listed the environment items as standing on every outcome (PFB:53-76), with its overclaims flagged (PFB:69, :75, :82).
  - D.4 The seed rule's history: k = 40 registered, 46 on the re-measured floor, cap 60, 72 realized as a recorded deviation before unblinding (DES-1 to DES-5); realized power (DES-4, DES-6).
  - D.5 Bias (b) in full: its readings (DES-10, DES-11, V6-4), "reverses sign on the grid GPU".
  - D.6 GPU blocks: Γ on GPU 1 (all 72 seeds of ISO and JOINT), ISO-4 and the 2000-update subsample on GPU 2, post-unblind evaluations on GPU 3, the superseded RTX PRO 6000 seeds descriptive only (HW-4, DX-5, DX-30, DX-36). "GPU 1/2/3" appear only here.
  - D.7 Study codes, a key table: code | plain name | where used (M3.0 … M6.2b, G1.2, G1.3, m35, m44, E1.1, E2C, E2C²).
  - D.8 Seeds and archives: shared seed integers, seed 0 reserved for floors, never in the grid (DX-416); seed-major order and chunking; 615 of 615 archive hashes matched on re-verification (DX-408; no hash quoted; v2 F1's 636-vs-615 question open).
  - D.9 Blinding: one look per stage; analysis scripts refuse to run out of order (DX-411); the inventory of outcome-derived quantities visible before unblinding is owner-attested only (V3Q19): leave a marker, state nothing.
  - D.10 The framing change: the owner's ruling of 2026-10-12 moved the paper's emphasis to the environment after the result was known; the registered branches stay the record of the original framing (X4-5; PAPER V3 item 3).
ROWS: DX-401, DX-402, V6-1, V6-2, V6-3, V6-4, V6-5, DES-1 to DES-6, DES-10, DES-11, DES-12, DES-15, DX-405, DX-102, DX-413, RES-5, HW-4, DX-5, DX-30, DX-36, DX-408, DX-411, DX-416, X4-5.
REGISTERED STRINGS: every quotation verbatim; "no longer holds as worded"; "the branch label stays B"; bias (b) "reverses sign on the grid GPU"; "registered before unblinding" for the correction.
EVERY OTHER CAVEAT in checks/caveats.yaml: pointer only ("§6.3", "Appendix D"), never restated. C26: any sentence about the interaction check carries "post hoc".
NEW ROWS OWED:
  - X4-5 (W4): 2026-10-12, the framing change (the owner's environment-first ruling), VERIFIED at docs/decision_log.md:6115 and :6158-6169.
OWNER-PENDING:
  - D.1 full-history check and content hashes (V3Q16).
  - D.9 blinding inventory (V3Q19).
  - D.3 registered antecedent (V3Q22).
  - attribution of the 2026-08-16 review (carried v2 A1(ii)).
NOT HERE: commit hashes, hosts, GPU UUIDs, account names; any reinterpretation of a registered rule; a day count between identification and registration; "certified" outside a verbatim quotation (and flag it there).
V2 MATERIAL: paper/v2/sections/14_appendix_plan_provenance.md (D, E, F); paper/v2/BRIEF.md §7; paper/v2/ledger_proposals/W6.md.
DEPENDENCIES: every main-text file points here instead of giving a date.
-->

This appendix holds the record that the main text leaves out: when each part of the worked example was fixed, what the registration said, which GPU ran what, and how the seeds and archives were kept. Dates are as recorded in the project's own dated log and documents.

**D.1 Registration statement.** The registration is an internal, version-controlled record kept in the project's repository: the frozen design, the outcome framings, and a dated log of the decisions taken during the study. Its dates are self-reported. The code supplement carries the two registration documents, the frozen design and the outcome framings, with a hash manifest of every file it ships, so a reader can compare the quoted registration text with the shipped documents, check with the manifest that the archive arrived unaltered, and rerun the analysis scripts on the committed results. The dated log and the design review are not part of the supplement by default, so the quotations from the log (the estimand, the inert-share rule, the High readout, the 2000-update<!-- N:RES-15 --> subsample, the rulings before unblinding and the secondary specification) cannot be checked against the supplement unless log excerpts ship with it. What a reader cannot check is when the documents were written: that rests on the repository's history, which is not public. We checked that history. The frozen design was first committed on 2026-08-02 and last changed on 2026-08-13; the outcome framings were committed on 2026-08-13 and not changed afterwards; the first provenance file of the main training runs was committed on 2026-09-09, the confirmatory artifact's hash file on 2026-09-23, and the unblinding log on 2026-09-26<!-- N:X4-6 --> (calendar dates as the commits record them). These are commit dates in a private version-controlled repository, set by the committer's own clock, so they are self-reported, not externally timestamped. On a future project we would register in a public registry such as OSF.
<!-- OWNER-PENDING:V3Q16 full-history check DONE (fix round, RC2-12; dates stated above, no commit hash in the text); still open: content hashes of the registration documents in this appendix, and decision-log excerpts in the supplement (V3-V1); review RC2-12: after V3Q16, the shallow-clone sentence becomes either "The authors checked that the registration documents' commits predate the main training runs; the history itself is not public" or "The repository's history is not part of the supplement" -->

**D.2 Dated events.** Each row names the record that dates it.

| date | event | record |
|---|---|---|
| 2026-07-19 to 2026-07-30<!-- N:DX-401 --> | the environment constants are fixed (values in Appendix B): the severities and the death price, then Coupling A, the masking observation, Coupling B, and communication denial with its range | dated log; Appendix B |
| 2026-07-30<!-- N:V6-2 --> | communication denial is closed as inert at this scale (the log's words are "a certified negative") | dated log |
| 2026-08-02<!-- N:V6-3 --> | the design is registered; it keeps δ in θ\* "for registration fidelity at zero cost", gives ISO two δ-only components of six<!-- N:V6-3 -->, and leaves δ out of the secondary sweeps because it is inert | frozen design |
| 2026-08-02<!-- N:DES-12 --> | survival becomes a co-primary; the secondary sample size, Šidák m = 2 and the mediation void rule are fixed<!-- N:DX-402 --><!-- N:DX-414 --> | dated log; frozen design |
| 2026-08-03<!-- N:DX-402 --> | the registered seed count, 40, and the seed rule's cap, 60<!-- N:DES-1 -->, are fixed | dated log |
| 2026-08-10<!-- N:DES-5 --> | the main runs' launch floor study, on an RTX PRO 6000 | dated log |
| 2026-08-11<!-- N:METH-6 --> | the convergence check is retired, and the estimand is fixed at a matched budget of 1000<!-- N:DES-13 --> updates, with the rule for Γ(t) | dated log |
| 2026-08-13<!-- N:DES-12 --> | the outcome branches, a framing for each and the falsifier are registered | outcome framings |
| 2026-08-13<!-- N:V6-5 --> | the frozen plan is amended: the tests use the main runs' own seed dispersion | frozen design |
| 2026-08-14<!-- N:DX-36 --> | a partial re-measurement of floors on another rented GPU (provenance only) | the floor study's own record (results directory) |
| 2026-08-16<!-- N:V6-1 --> | a review of the registered design identifies the inert-share bias in ISO and its direction, before the main runs | design review; dated log |
| 2026-09-08<!-- N:DES-2 --> | floors re-measured on an RTX PRO 6000; the seed rule gives 46<!-- N:DES-2 --> | dated log |
| 2026-09-09 to 2026-09-22<!-- N:DES-12 --> | the main training runs, 252<!-- N:DX-30 --> runs | dated log; results report |
| 2026-09-18<!-- N:DES-15 --> | the bias, its direction, ISO-4 with its reading rule, the High readout and the 2000-update<!-- N:RES-15 --> subsample are registered, with 120 of 252<!-- N:DES-15 --> runs done | dated log |
| 2026-09-22<!-- N:DES-3 --> | the seed cap is raised to 72<!-- N:DES-3 -->, a recorded deviation | dated log |
| 2026-09-26<!-- N:DX-405 --> | the rulings before unblinding, (i)–(viii), and a fifth outcome cell, $A_c$<!-- N:DX-102 --> | dated log |
| 2026-09-26<!-- N:DES-12 --> | unblinding, later the same day | dated log; unblinding log |
| 2026-09-26<!-- N:DX-413 --> | the secondary specification is ratified, after unblinding for Γ and before the sweep is read; the same-GPU replicate Γ₄′ is proposed after Γ₄ is seen<!-- N:DES-15 --> | dated log |
| 2026-09-27<!-- N:DX-408 --> | every checkpoint archive's recorded hash is re-verified | results report |
| 2026-10-12<!-- N:X4-5 --> | the framing change (D.10) | dated log |

The design error of §6.2 runs through these rows. The design registered on 2026-08-02<!-- N:V6-3 --> kept a stressor it had already found inert, left it out of the sweeps for that reason, and kept it in ISO. One of its own questions for reviewers rested on the premise that "Neither protocol trains on δ = 1.0", which is false for both arms: ISO's δ-only components and both of JOINT's train at δ = 1<!-- N:X4-2 -->. The outcome branches registered on 2026-08-13<!-- N:DES-12 --> did no inert-share accounting. A review of the registered design found the bias on 2026-08-16<!-- N:V6-1 -->, noting that the confirmatory arm "applies a different rule to the same fact" as the sweeps. The main runs began without the correction. The correction was registered on 2026-09-18<!-- N:DES-15 -->, mid-run and before unblinding, on our attestation, recorded with the decision, that no outcome mean, per arm or across arms, had been computed or viewed. The confirmatory family did not change.
<!-- OWNER-PENDING:A1(ii) attribution of the 2026-08-16 review (default "a review of the registered design") -->

**D.3 The registered rules, quoted.** Emphasis is the record's own, one indented code line is set inline, and omissions are marked […]. A "§" inside a quotation refers to the record's own sections, "card" and "unit" are the record's words for a GPU, and S1–S6 are its labels for the secondary analyses.

*The estimand* (2026-08-11<!-- N:METH-6 -->):

> **Primary Γ = the confirmatory contrast at MATCHED BUDGET T = 1000<!-- N:DES-13 -->, all arms — registered as a fixed-budget claim.**
>
> **"At convergence" is explicitly NOT claimed anywhere.** The paper says **"at matched compute"** throughout, which is also the practitioner-relevant question. […]

*Budget robustness* (same ruling; restated for every branch on 2026-08-13<!-- N:DES-12 -->):

> The fixed-budget conclusion is reported as **budget-robust iff the sign of Γ is stable over the final half of training**. If the sign is still moving at T, **that instability IS the finding** and is reported as such.

> Mechanism: 11 retained checkpoints, updates 500–1000 at interval 50<!-- N:DES-13 -->, confirmatory arms only, **evaluated post-unblind**. Every branch above gains "— budget-robust" or "— sign unstable over the final half" as a suffix, and the suffix is not optional.

*The test's variance* (the frozen plan, amended 2026-08-13<!-- N:V6-5 -->):

> **The confirmatory tests and CIs are computed on the GRID'S OWN measured per-arm seed dispersion, not on the floors.** The floors are 8<!-- N:DX-403 --> identical reps at one seed; the grid averages over k distinct seeds, and those are different variances. The floors keep exactly two narrower roles: the **beat-reproducibility hurdle**, and a **design-stage power basis registered as an UPPER BOUND** (§5, superseded note, item 2). […]

*The outcome branches* (2026-08-13<!-- N:DES-12 -->). "Positive" and "null" mean rejection or non-rejection at θ\* in the confirmatory family, and "−" means rejection with negative sign (ruling (i) below). The registered table's venue column is omitted. $A_c$ was added on 2026-09-26<!-- N:DX-405 -->, before unblinding, for a cell the table lacked.

| branch | completion | survival | headline claim, as registered ($A_c$: its registered claims, summarized) |
|---|---|---|---|
| A | + | + | founding registration, verbatim [Γ(θ\*) > 0] |
| B | null | + | composition is paid in **agents**, not task return |
| C | null | null | the instrument, and what it excludes |
| D | − (either) | [− (either)] | not separable from the matched-budget asymmetry |
| $A_c$ | + | null | the founding claim on the founding primary; the survival null quoted as an exclusion; no asymmetry claim |

In row D, "− (either)" means rejection with negative sign on either co-primary; the registered table writes it once, under completion, and square brackets mark our additions.

<!-- OWNER-PENDING:V3Q22 registered antecedent (default: this note in Appendix D only, not in the main text) -->
The same document lists the environment and measurement items as standing on every outcome, "the larger part of the paper", which "does not depend on Γ at all". Three of its entries overclaim and are not repeated in this paper: a threshold value with no committed estimator behind it (§4.1 gives the committed estimators), communication denial "certified inert at swarm scale" (§4.4 gives the scoped phrase and its bars), and floors "ordered by curriculum difficulty", an untested hypothesis.

*The falsifier for branch B* (2026-08-13<!-- N:DES-12 -->):

> Branch B is claimable **only if** the completion contrast excludes an effect as large, in standardized units, as the observed survival effect:
>
> `|z_c| + z_α  <  |z_s|,     z = Γ / sd(Γ) per metric`
>
> with `sd(Γ)` the grid's own measured per-arm seed dispersion in the combined form and `z_α = 2.2365`<!-- N:DES-13 --> the two-sided Šidák critical value at m = 2. **If it fails, the result is branch C with an asymmetry the design could not resolve — not branch B.**

It passes: with $z_c$ and $z_s$ the two statistics, $\lvert z_c\rvert + z_\alpha = 3.855 < 4.433 = \lvert z_s\rvert$, and 4.040 < 4.673 in the registered 60-seed analysis<!-- N:RES-5 -->. Under Definition 2 the asymmetry is between a penalized channel and a rewarded one: the reward prices every death at $d_p = 0.5$<!-- N:ENV-1 --> whatever its cause and never reads the hazard. The result is branch B, completion null and survival positive. Branch A, the founding hypothesis, did not occur, and neither did $A_c$. Branch B's registered headline, "composition is paid in **agents**, not task return", no longer holds as worded, because the survival effect does not survive the inert-share correction (§6.3); the branch label stays B, because the rule below fixes it by Γ.

*The inert-share rule* (2026-09-18<!-- N:DES-15 -->):

> - Γ and Γ₄ are reported **side by side on every branch**, with B̂ and its CI.
> - If Γ rejects on a co-primary and **Γ₄'s CI on that co-primary includes 0 or its sign is opposite**, the paper states that the effect **does not survive the inert-share correction**, in the abstract-level summary and not only in an appendix. **The branch label does not change** — it is fixed by Γ — but branch A/B text may not describe the effect as a composition effect without that qualifier.
> - If Γ is null and Γ₄ is null, Γ₄ is quoted as a second exclusion bound.
> - If Γ is null and Γ₄ rejects **negative**, it is reported under branch D's framing (matched-budget asymmetry) as a secondary observation, never as a confirmatory finding.
> - **No magnitude threshold on B̂ is introduced**, now or later.

*The High readout* (same ruling):

> - **Γ_H null → an *a fortiori* exclusion**, and the only outcome this readout can establish: *"no gap larger than X at High even where JOINT trained on the evaluated configuration and ISO never saw a composed one."* Quoted as an exclusion with X from the grid's own seed dispersion, never as an absence. […]

The same entry states that the readout "is NOT a held-out test", that a positive $\Gamma_H$ is "NOT separable from in-distribution advantage", and that a negative one is "exploratory".

*The 2000-update<!-- N:RES-15 --> subsample* (same ruling):

> **What it may be cited for:** whether the differential drift measured at T = 1000 (review §6 item 1: 0.01209 per 100 updates<!-- N:DES-10 -->) visibly persists, closes or reverses. **What it may not be cited for:** any claim that Γ "holds" or "vanishes" at T = 2000.

*The mediation void rule* (the frozen plan, 2026-08-02<!-- N:DX-414 -->):

> **If realized dose does not vary with assigned p, the dose figure has no x-axis and is declared VOID** — registered now, not decided after seeing the first stage.

*The rulings before unblinding* (2026-09-26<!-- N:DX-405 -->):

| # | question | RULED |
|---|---|---|
| (i) | what "−" means in the branch table | **Rejection with negative sign** (\|z\| > z_α, Γ < 0). A negative estimate that does not reject is a null. Ratified as built. |
| (ii) | the cell (completion +, survival null), absent from the registered table | **REGISTERED NOW as branch A_c — the founding claim on the founding primary.** […] |
| (iii) | test statistic | **Normal z, z_α = 2.2365<!-- N:DES-13 -->**, as the frozen plan wrote; the t critical value is printed, not applied. Ratified as built. |
| (iv) | Γ(t) "sign stable" | **All 11<!-- N:DES-13 --> point estimates, t = 500 … 1000, share one nonzero sign**, per co-primary; t = 1000 is the grid's own eval. Consequence accepted in advance: on a null Γ, chance flips read UNSTABLE. Ratified as built. |
| (v) | Γ₄ sample and threshold | **JOINT k = 72 vs ISO-4 k = 20<!-- N:DES-3 --><!-- N:DES-13 -->**, SE `sqrt(s_J²/72 + s_4²/20)`, "rejects" and "CI includes 0" at z_α = 2.2365. (Γ null, Γ₄ rejects positive) stays UNREGISTERED. Ratified as built. |
| (vi) | Γ_H reading | **As (i), at z_α = 2.2365.** Ratified as built. |
| (vii) | primary k | **k = 72 stays primary**; the registered-ladder k = 60<!-- N:DES-1 --> prefix is reported beside it, UNDERPOWERED-flagged. |
| (viii) | re-evaluate the 144<!-- N:DES-3 --> T\* = 1000 checkpoints on the post-unblind card | **YES.** […] |

In (viii), "the post-unblind card" is GPU 3 (D.6).

*The secondary specification* (2026-09-26, after unblinding and before the sweep was read<!-- N:DX-413 -->):

> (S1) PAVA + OLS slope CI; (S2) single-hinge breakpoint, UNDERPOWERED iff the CI spans {0.125 … 0.375}<!-- N:DX-28 -->; (S3) plane fit, bound = 95 % CI of 0.5·γ_n; (S4) training co-activity over updates 1…1000, VOID iff the first-stage CI contains 0; (S5) the same-card replicate is ADDED, beside Γ₄, unable to change its qualifier; (S6) 95 % intervals, Γ₄′ at z_α. […]

The omitted words name the code version, which would identify the repository.

**D.4 The seed rule.** The design registered k = 40<!-- N:DES-1 --> seeds per confirmatory arm and a rule, capped at 60<!-- N:DES-1 -->, that recomputes k from floors re-measured on the GPU that would run the main training runs. On the launch floor study of 2026-08-10<!-- N:DES-5 --> the design-stage detection limit at k = 40 was 1.55 completion and 0.95 survival points<!-- N:DES-5 -->. The rule gave 46<!-- N:DES-2 --> on the RTX PRO 6000 floors of 2026-09-08<!-- N:DES-2 -->, and 72<!-- N:DES-3 --> on the RTX 5090 that ran the confirmatory runs. The rule's registered action at the cap was "PROCEED at k = 60 and DEGRADE HONESTLY, never chase". On 2026-09-22<!-- N:DES-3 --> the cap was raised to 72 instead, before unblinding and with no outcome seen; this is a deviation from a registered rule, recorded as one. Seeds 1–60 are a prefix of the 72, so the registered 60-seed analysis is reported beside the primary one (Appendix E). On the RTX 5090's floors, design-stage completion power at a 3-point effect was 72.2 % at k = 60 and 80.4 % at k = 72<!-- N:DES-4 -->, an upper bound because floors measure rerun noise alone; realized power was 60.2 % and 71.6 %<!-- N:DES-6 -->.

**D.5 Bias (b).** The registered caveat on differential drift is the difference between JOINT's and ISO's completion drift over the last 100 of 1000<!-- N:DES-13 --> training updates<!-- N:DES-10 -->, quoted as a local sensitivity estimate and never as a bound. Four floor studies read it at 1000 updates<!-- N:DES-10 --><!-- N:V6-4 -->: +0.0242<!-- N:V6-4 --> per 100 updates on the confirmatory arms' earlier floor study, +0.01209<!-- N:DES-10 --> on the launch floor study and +0.0179<!-- N:DES-10 --> on the 2026-09-08<!-- N:DES-2 --> re-measurement, all three on an RTX PRO 6000, but −0.0083<!-- N:DES-10 --> on GPU 1. Bias (b) therefore reverses sign on the grid GPU, and no direction is claimed. In the 2000-update<!-- N:RES-15 --> subsample, the differential training-log slopes over updates 500–1000 are +0.00247 for completion and +0.00718 for survival per 100 updates<!-- N:DES-11 -->, a different estimator from the floor studies'.

**D.6 GPU blocks.** The runs analysed here used one GPU model, the RTX 5090, on three rented units<!-- N:DX-5 -->. GPU 1 ran Γ: all 72 seeds of ISO and JOINT<!-- N:HW-4 -->, of which 76 runs were executed there and seeds 13–46 were copied from the main runs<!-- N:DX-30 -->. GPU 1 also ran every analysed secondary run, so Γ₄′ is a same-GPU contrast. GPU 2 trained ISO-4 and the 2000-update<!-- N:RES-15 --> subsample, so Γ₄ and B̂ compare runs on two GPUs, and GPU 3 ran the evaluations after unblinding<!-- N:HW-4 -->. Seeds 1–12 of all ten arms first ran on an RTX PRO 6000<!-- N:DX-30 -->; those runs were superseded, enter only a descriptive diagnostic of the GPU effect, and the secondary arms' seeds 1–12 were re-run on GPU 1 (96 runs<!-- N:DX-30 -->).

**D.7 Study codes.** The project's internal codes appear on some figures and in the supplement. Their plain names:

| code | plain name |
|---|---|
| M3.0 | the re-test of Definition 4's prediction that outcomes vary most at Medium |
| M3.3 | the check of Proposition 3 against its closed form |
| M3.4 | the Coupling-A calibration under random policies |
| M3.5 (printed m35) | the Coupling-A calibration grid |
| M4.2 | the check of Theorem 1 in the corridor toy (printed E2C) |
| M4.4 (printed m44) | the Coupling-B calibration grid |
| E1.1 | the severity response of collapse-seeded ignitions near agents |
| M5.1e | the four-run<!-- N:DX-403 --> Medium floor study on an RTX 5090 |
| M5.2 | the check of Remark 2′ in the two-agent courier toy (printed E2C²) |
| M5.3, M5.3b | the content ablation at Medium, and the same ablation at High |
| M5.5 | the denial study |
| M6.0 | the refactor of the environment code |
| M6.2, M6.2b | the confirmatory arms' floor studies at 500 and 1000<!-- N:DX-34 --> updates |
| G1.2 | the floor-study protocol of the main runs: the launch floor study (2026-08-10<!-- N:DES-5 -->) and its re-measurements of 2026-09-08<!-- N:DES-2 --> and on the RTX 5090 |
| G1.3 | the main training runs |

**D.8 Seeds and archives.** All arms share seed integers, and seed 0, the floor seed, never enters the main runs<!-- N:DX-416 -->. Runs are ordered seed-major and chunks end on seed boundaries, so an interruption leaves a smaller balanced design and both arms of a seed share one GPU. Every checkpoint archive's recorded sha256 matched on re-verification on 2026-09-27<!-- N:DX-408 -->, 615 of 615<!-- N:DX-408 -->; the hashes ship with the supplement's result directories, not here.
<!-- OWNER-PENDING:F1 archive count "615 of 615" against the 636 that the same report's archive table sums to (DISPOSITIONS §5 F1 carries; review RN2-1); the count is kept until the owner reconciles the record -->

**D.9 Blinding.** The runner of the main training runs computes no cross-arm quantity, and a unit test asserts it. Each analysis stage ran once: the unblinding script refuses an unflagged artifact or a modified code version, later analysis scripts refuse to run before its log exists, and each log records one run of its stage<!-- N:DX-411 -->.
<!-- OWNER-PENDING:V3Q19 the inventory of outcome-derived quantities visible when k = 72 and ISO-4 were decided is owner-attested only; nothing is stated beyond one look per stage -->

**D.10 The framing change.** On 2026-10-12<!-- N:X4-5 -->, after the result was known, we moved the paper's emphasis to the environment, and the pre-registered test became its worked example (§6.1). No constant, registration or registered reading changed. The registered outcome branches and their framings, quoted in D.3, remain the record of the original plan.

<!-- PAPER V3 DRAFT (PAPER V3 ruling, 2026-10-12): builder-drafted, not owner-approved -->

### E Additional results

<!-- STUB-SPEC
JOB: The results the main text points to: Γ(t) tables and figure; the k = 60 analysis; T = 2000; the High readout (home of the a-fortiori exclusion); fire deaths; seed dispersion over the floor; the communication-denial measurements figure.
WRITER: W5.
BUDGET: about 550 prose words plus the two Γ(t) tables; figure captions at most 60 words each.
FROM: P1 §6.1 E; P2 §3 A1, A3.
ROWS: DX-24, DX-25, RES-1, RES-2, RES-11, RES-12, RES-13, RES-3, DX-20, RES-15, DX-23, DES-11, RES-14, DX-26, RES-10, DX-22, HW-1, DX-21, COM-1, COM-4, DES-13.
FIGURES: Figure E1 gamma_t_final_half (glosses: labelled “grid card”, labelled “single-card curve”); Figure E2 static fig06_comms.png (glosses: labelled “E2C²”, labelled “M5.2”, labelled “M5.5”). Blocks below.
REGISTERED STRINGS: "sign unstable over the final half" first; UNDERPOWERED (k = 60; T = 2000; change points); "a-fortiori exclusion" with its sentence "no gap larger than X at High even where JOINT trained on the evaluated configuration and ISO never saw a composed one" (the X values are MDEs: label them, BRIEF §9.2 trap 5); descriptive for Γ(t) at t below 1000 and T = 2000.
CAVEATS HOMED HERE (state each in full, once; the detection pattern, from checks/caveats.yaml, must match your home sentence):
  C24 high_readout_a_fortiori: The High readout is an a-fortiori exclusion, not a held-out test (full statement in App. E). Pattern: (?i)a-fortiori
EVERY OTHER CAVEAT in checks/caveats.yaml: pointer only ("§6.3", "Appendix D"), never restated. C26: any sentence about the interaction check carries "post hoc".
NOT HERE: the High readout as a held-out test; T = 2000 as anything but descriptive; any Γ(t) value beyond DX-24, DX-25.
V2 MATERIAL: paper/v2/sections/14_appendix_plan_provenance.md (G); 09_compositional_test.md §9.2 (k = 60, T = 2000, High, fire deaths); 07_comms.md (Figure 9 text).
DEPENDENCIES: §6.3 points here; §4.4 points here for the comms figure.
-->

**Sign unstable over the final half**, on both co-primaries<!-- N:RES-11 -->: neither meets the registered rule that all 11<!-- N:DES-13 --> point estimates over updates 500–1000<!-- N:DES-13 --> share one sign (Appendix D). The intervals are Šidák-corrected, registered at update 1000<!-- N:DES-13 --> and descriptive before it. Checkpoints before update 1000 were evaluated after unblinding, on a different GPU of the same model; update 1000 is the main runs' own evaluation, and re-evaluating it on that GPU leaves every sign unchanged (§8). On Figure E1 the registered sign rule is labelled “rule (iv)” and the main runs' GPU “grid card”, and the “single-card curve” re-evaluates the last checkpoint on another GPU.

<!-- FIGURE E1: block carried from paper/v2/sections/09_compositional_test.md:101 (markup, iframe height and alt text as v2 had them); caption replaced; the writer checks the alt text -->

<figure class="l-page">
  <iframe src="{{ 'assets/html/submission/gamma_t_final_half.html' | relative_url }}" width="100%" height="503" style="border:none" title="Gamma over the final half of training, completion and survival" loading="lazy"></iframe>
  <figcaption><strong>Figure E1.</strong> <strong>Sign unstable over the final half</strong>, on both co-primaries<!-- N:RES-11 -->. Γ(t) with Šidák-corrected intervals; only the last checkpoint is the registered Γ. Rings mark signs that differ from the final one. The dotted box is ±1 floor-based standard error of Γ.</figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/gamma_t_final_half.png" class="img-fluid" alt="The retained checkpoints over the final half of training of the joint-minus-isolated difference in completion and in survival, each with its Šidák interval, labelled sign unstable over the final half" caption="Static companion of Figure E1 for the printed PDF." %}
</div>

Completion, k = 72 per arm<!-- N:DES-13 -->, in rates:

| update | Γ(t) | sd(Γ) | Šidák CI | sign |
|---|---|---|---|---|
| 500 | +0.0017<!-- N:DX-24 --> | 0.00321<!-- N:DX-24 --> | [−0.0055, +0.0089]<!-- N:DX-24 --> | + |
| 550 | −0.0017<!-- N:DX-24 --> | 0.00353<!-- N:DX-24 --> | [−0.0096, +0.0062]<!-- N:DX-24 --> | − |
| 600 | +0.0018<!-- N:DX-24 --> | 0.00362<!-- N:DX-24 --> | [−0.0063, +0.0099]<!-- N:DX-24 --> | + |
| 650 | +0.0015<!-- N:DX-24 --> | 0.00481<!-- N:DX-24 --> | [−0.0093, +0.0122]<!-- N:DX-24 --> | + |
| 700 | −0.0037<!-- N:DX-24 --> | 0.00470<!-- N:DX-24 --> | [−0.0142, +0.0068]<!-- N:DX-24 --> | − |
| 750 | −0.0147<!-- N:RES-13 --> | 0.00610<!-- N:DX-24 --> | [−0.0283, −0.0010]<!-- N:RES-13 --> | − |
| 800 | −0.0035<!-- N:DX-24 --> | 0.00677<!-- N:DX-24 --> | [−0.0187, +0.0116]<!-- N:DX-24 --> | − |
| 850 | −0.0053<!-- N:DX-24 --> | 0.00729<!-- N:DX-24 --> | [−0.0216, +0.0110]<!-- N:DX-24 --> | − |
| 900 | −0.0039<!-- N:DX-24 --> | 0.00843<!-- N:DX-24 --> | [−0.0228, +0.0149]<!-- N:DX-24 --> | − |
| 950 | −0.0016<!-- N:DX-24 --> | 0.01021<!-- N:DX-24 --> | [−0.0245, +0.0212]<!-- N:DX-24 --> | − |
| 1000 | −0.0173<!-- N:RES-1 --> | 0.01068<!-- N:DX-24 --> | [−0.0412, +0.0066]<!-- N:RES-1 --> | − |

Survival rate, k = 72 per arm<!-- N:DES-13 -->, in rates:

| update | Γ(t) | sd(Γ) | Šidák CI | sign |
|---|---|---|---|---|
| 500 | +0.0022<!-- N:DX-25 --> | 0.00228<!-- N:DX-25 --> | [−0.0029, +0.0073]<!-- N:DX-25 --> | + |
| 550 | −0.0037<!-- N:DX-25 --> | 0.00220<!-- N:DX-25 --> | [−0.0086, +0.0013]<!-- N:DX-25 --> | − |
| 600 | −0.0027<!-- N:DX-25 --> | 0.00232<!-- N:DX-25 --> | [−0.0078, +0.0025]<!-- N:DX-25 --> | − |
| 650 | +0.0011<!-- N:DX-25 --> | 0.00242<!-- N:DX-25 --> | [−0.0043, +0.0065]<!-- N:DX-25 --> | + |
| 700 | +0.0031<!-- N:DX-25 --> | 0.00235<!-- N:DX-25 --> | [−0.0021, +0.0084]<!-- N:DX-25 --> | + |
| 750 | +0.0036<!-- N:DX-25 --> | 0.00255<!-- N:DX-25 --> | [−0.0021, +0.0093]<!-- N:DX-25 --> | + |
| 800 | +0.0020<!-- N:DX-25 --> | 0.00232<!-- N:DX-25 --> | [−0.0032, +0.0072]<!-- N:DX-25 --> | + |
| 850 | +0.0018<!-- N:DX-25 --> | 0.00234<!-- N:DX-25 --> | [−0.0034, +0.0071]<!-- N:DX-25 --> | + |
| 900 | +0.0056<!-- N:RES-12 --> | 0.00231<!-- N:DX-25 --> | [+0.0004, +0.0108]<!-- N:DX-25 --> | + |
| 950 | +0.0083<!-- N:RES-12 --> | 0.00219<!-- N:DX-25 --> | [+0.0034, +0.0132]<!-- N:DX-25 --> | + |
| 1000 | +0.0096<!-- N:RES-2 --> | 0.00216<!-- N:DX-25 --> | [+0.0047, +0.0144]<!-- N:RES-2 --> | + |

The registered k = 60<!-- N:DES-1 --> analysis, on seeds 1–60<!-- N:RES-3 -->, reads as the k = 72<!-- N:DES-3 --> analysis does and is flagged UNDERPOWERED; the registered seed rule had required 72<!-- N:DES-3 --> seeds for completion. Completion is null at −2.17 points<!-- N:RES-3 --> [−4.86, +0.52]<!-- N:DX-20 -->, z −1.80<!-- N:RES-3 -->, and survival rejects at +1.04 points<!-- N:RES-3 --> [+0.54, +1.55]<!-- N:DX-20 -->, z +4.67<!-- N:RES-3 -->, with Šidák-corrected intervals. Realized completion power against a 3-point effect is 60.2 % at k = 60 and 71.6 % at k = 72<!-- N:DES-6 -->.

The 2000-update subsample (4 seeds per arm<!-- N:RES-15 -->, trained on a second GPU of the same model<!-- N:HW-4 -->) is descriptive and UNDERPOWERED by registration. Its Γ(2000) is +0.03 points<!-- N:RES-15 --> [−3.63, +3.69]<!-- N:DX-23 --> on completion and +1.59 points [−0.02, +3.19]<!-- N:RES-15 --> on survival, with 95 % intervals that are not family-corrected. The difference between JOINT's and ISO's training-curve slopes stays positive over updates 1000–2000, at +0.00384 (completion) and +0.00204 (survival) per 100 updates<!-- N:DX-23 -->, as it was over updates 500–1000<!-- N:DES-11 -->. The drift it measures has not visibly reversed, which is all it may be cited for.

The High-severity readout re-evaluated every final checkpoint of ISO, JOINT and ISO-4 with every stressor on at β = 0.70<!-- N:CAL-3 -->, outside the confirmatory family. Both co-primaries are null, so the reading is an **a-fortiori exclusion**: no gap larger than 3.40 completion points or 2.54 survival points<!-- N:RES-14 --> at High even where JOINT trained on the evaluated configuration and ISO never saw a composed one. Those two values are the readout's 80 %-power detection limits (the registered sentence's X), and its Šidák-corrected intervals are [−3.26, +1.68] (completion) and [−1.46, +2.23] (survival) points<!-- N:DX-26 -->. JOINT − ISO-4 at High is null too, at −0.75 [−3.87, +2.36] and −1.28 [−3.50, +0.95] points<!-- N:DX-26 -->, with no reading rule of its own. The JOINT − ISO gap lies within rerun noise, at 0.73 and 0.75 times its floor-based standard error (completion, survival)<!-- N:RES-14 -->; ISO-4 has no identical reruns, so that check is UNDERPOWERED for it. The readout is not a held-out test: JOINT trained on this configuration at weight 1/2<!-- N:DES-16 -->, and ISO never trained with more than one stressor on.

On secondary metrics outside the family, descriptive and without a floor, JOINT has 0.1177 fewer fire deaths per episode than ISO (z = −4.59)<!-- N:RES-10 -->, at 0.6949 against 0.8126<!-- N:DX-22 -->, and its episode return differs by −0.4958 (z = −1.44)<!-- N:DX-22 -->.

Seed dispersion exceeds the rerun floor in both arms, 1.12 and 1.09 times on completion and 1.25 and 1.19 times on survival (ISO, JOINT)<!-- N:HW-1 -->. Survival Γ, at 5.40 times its floor-based standard error<!-- N:HW-1 --> (completion 1.78 times<!-- N:DX-21 -->), clears the check that an effect exceeds rerun noise.

Figure E2 shows the measurements behind the inert label of §4.4; on it the two-agent courier toy is labelled “E2C²” and “M5.2”, and the denial study “M5.5”. In the two-agent courier toy, the value of communication rises from 0 to 0.498<!-- N:COM-1 --> as perception decays (Figure E2(a)).

<!-- FIGURE E2: block carried from paper/v2/sections/07_comms.md:23 (include and alt text as v2 had them); caption replaced -->

{% include figure.html path="assets/img/submission/fig06_comms.png" class="img-fluid" alt="Top left, courier success rate against perception attenuation in the two-agent toy, for free and for denied communication, with the predicted curve. Top right, the denial contrasts at medium severity with their bars. Bottom, the per-run values behind those contrasts." caption="Figure E2. Communication in the toy, and denial in CHE at Medium." %}

<p class="caption">(a) The two-agent courier toy with scripted policies: success with free and with denied communication; the shaded gap is the value of communication. (b–d) The denial study at Medium: contrasts between open and denied links against bars of twice<!-- N:V4-2 --> the floor sd, and the per-run values.</p>

<!-- PAPER V3 DRAFT (PAPER V3 ruling, 2026-10-12): builder-drafted, not owner-approved -->

### F The secondary design

<!-- STUB-SPEC
JOB: The secondary design in full: arms (with code names as labels matching Figure 7), the sweep, the plane fit and its coarse linearity check, the same-GPU replicate table, mediation (VOID), and what that analysis could not see.
WRITER: W4.
BUDGET: about 400 prose words plus tables.
FROM: P1 §6.1 F; v2 Appendix H.
ROWS: DES-9, DX-28, SEC-1 to SEC-7, DX-27, DX-29, DX-306, DX-417, DX-39, RES-6, RES-7, RES-8, RES-9, DX-18, DX-19.
REGISTERED STRINGS: "non-verdict-bearing"; VOID (mediation); UNDERPOWERED (change points); "95 %, not family-corrected".
EVERY OTHER CAVEAT in checks/caveats.yaml: pointer only ("§6.3", "Appendix D"), never restated. C26: any sentence about the interaction check carries "post hoc".
NOT HERE: "the plane separates co-occurrence from frequency"; mediation as a finding.
V2 MATERIAL: paper/v2/sections/14_appendix_plan_provenance.md (H).
DEPENDENCIES: §6.3 points here.
-->

Everything here is secondary and non-verdict-bearing, with 95 % intervals bootstrapped over seeds within arm (B = 2000<!-- N:DX-28 -->), conditional on the common evaluation draw and not family-corrected. Each secondary arm has k = 20<!-- N:DES-13 --> seeds, trained on the GPU that ran Γ (Appendix D) with communication denial off in every component<!-- N:X4-2 -->. Write μ for the per-coupling frequency (equal for the two couplings in every arm here), p for the co-occurrence and ν for the fire-only share, as in §6.2. On the triangle of training mixtures $\nu = 1 - 2\mu + p$<!-- N:DES-9 -->, so the active share is $1 - \nu = 2\mu - p$<!-- N:X4-1 -->. Figure 7 prints μ as m and ν as n; the arm names below are the labels of its table view.

| arm | μ | p | ν | active share | survival | completion |
|---|---|---|---|---|---|---|
| `sweep_c50_p000` | 0.5<!-- N:DES-9 --> | 0<!-- N:DX-28 --> | 0<!-- N:DES-9 --> | 1<!-- N:X4-1 --> | 0.9241<!-- N:DX-28 --> | 0.7847<!-- N:DX-28 --> |
| `sweep_c50_p125` | 0.5<!-- N:DES-9 --> | 0.125<!-- N:DX-28 --> | 0.125<!-- N:DES-9 --> | 0.875<!-- N:X4-1 --> | 0.9249<!-- N:DX-28 --> | 0.7775<!-- N:DX-28 --> |
| `sweep_c50_p250` | 0.5<!-- N:DES-9 --> | 0.25<!-- N:DX-28 --> | 0.25<!-- N:DES-9 --> | 0.75<!-- N:X4-1 --> | 0.9261<!-- N:DX-28 --> | 0.7797<!-- N:DX-28 --> |
| `sweep_c50_p375` | 0.5<!-- N:DES-9 --> | 0.375<!-- N:DX-28 --> | 0.375<!-- N:DES-9 --> | 0.625<!-- N:X4-1 --> | 0.9264<!-- N:DX-28 --> | 0.7656<!-- N:DX-28 --> |
| `sweep_c50_p500` | 0.5<!-- N:DES-9 --> | 0.5<!-- N:DX-28 --> | 0.5<!-- N:DES-9 --> | 0.5<!-- N:X4-1 --> | 0.9289<!-- N:DX-28 --> | 0.7749<!-- N:DX-28 --> |
| `ident_c40_p000` | 0.4<!-- N:DES-9 --> | 0<!-- N:DX-28 --> | 0.2<!-- N:DES-9 --> | 0.8<!-- N:X4-1 --> | — | — |
| `ident_c40_p200` | 0.4<!-- N:DES-9 --> | 0.2<!-- N:DX-28 --> | 0.4<!-- N:DES-9 --> | 0.6<!-- N:X4-1 --> | — | — |
| `ident_c40_p400` | 0.4<!-- N:DES-9 --> | 0.4<!-- N:DX-28 --> | 0.6<!-- N:DES-9 --> | 0.4<!-- N:X4-1 --> | — | — |
| ISO-4 (second GPU) | 0.5<!-- N:DES-14 --> | 0<!-- N:DES-14 --> | 0<!-- N:DES-14 --> | 1<!-- N:DES-14 --> | 0.9256<!-- N:DX-18 --> | 0.7726<!-- N:DX-18 --> |

The p = 0 sweep arm carries exactly ISO-4's training mixture. Along the sweep, μ stays fixed while p and ν rise together, so the active share falls as co-occurrence rises; along the identification line the same holds 0.2<!-- N:DES-9 --> lower in active share.

| estimate (points) | survival | completion |
|---|---|---|
| sweep slope per unit p (labelled “dose slope”; separate fit) | +0.89 [−0.33, +2.11]<!-- N:SEC-5 --> | −2.51 [−9.43, +4.12]<!-- N:DX-27 --> |
| sweep endpoint, p = 0.5 minus p = 0 | +0.48 [−0.21, +1.17]<!-- N:SEC-5 --> | −0.97 [−4.82, +2.87]<!-- N:DX-27 --> |
| γ<sub>p</sub>, the co-occurrence slope, per unit p | +3.26 [+1.37, +5.02]<!-- N:SEC-1 --> | +2.69 [−6.75, +12.45]<!-- N:DX-27 --> |
| γ<sub>n</sub>, the fire-only-share slope, per unit ν | −2.37 [−4.19, −0.57]<!-- N:SEC-1 --> | −6.52 [−15.34, +2.42]<!-- N:DX-27 --> |
| bound, 0.5 γ<sub>n</sub> | −1.19 [−2.10, −0.28]<!-- N:SEC-2 --> | −3.26 [−7.67, +1.21]<!-- N:DX-27 --> |
| change point in p (labelled “knee”) | 0.375 [0.125, 0.375]<!-- N:DX-28 -->, UNDERPOWERED<!-- N:SEC-6 --> | 0.375 [0.125, 0.375]<!-- N:DX-28 -->, UNDERPOWERED<!-- N:SEC-6 --> |
| plane prediction of JOINT − ISO-4 (γ<sub>p</sub> × 1) | §6.3 | +2.69<!-- N:DX-417 -->; γ<sub>p</sub>'s interval contains both measured values |

The plane $y = \gamma_0 + \gamma_p p + \gamma_n \nu$ is a seed-level ordinary least squares (OLS) fit over all eight<!-- N:DX-28 --> arms; $\gamma_p$ is the co-occurrence slope and $\gamma_n$ the fire-only-share slope. The bound, the fire-only share's part of the sweep's endpoint change, excludes zero on survival. The sweep slope is a separate seed-level OLS fit over the five sweep arms, with an isotonic fit by the pool-adjacent-violators algorithm (PAVA) giving its monotone shape. The plane's slope along the sweep is $\gamma_p + \gamma_n$, so the two need not agree, and on completion they do not. The change point is the breakpoint of the best single-hinge fit. Linearity is assumed and checked only coarsely: arm-mean residuals lie within ±0.4 SE on survival and ±1.1 SE on completion, 8 points for 3 parameters<!-- N:DX-39 -->.

Because $1 - \nu = 2\mu - p$, a step in $\gamma_p$'s direction at fixed ν moves μ by half as much as p<!-- N:DES-9 -->, and a step in $\gamma_n$'s direction at fixed p moves μ too. Per-coupling frequency, co-occurrence and active share cannot all be held fixed on the triangle, so the plane separates co-occurrence from the active share only.

The same-GPU replicate of the correction subtracts the p = 0 sweep arm from JOINT, both trained on the GPU that ran Γ (§6.3):

| contrast | k | completion | survival | level |
|---|---|---|---|---|
| Γ₄′ = JOINT − the p = 0 sweep arm | 72 / 20<!-- N:DES-3 --><!-- N:DES-13 --> | −2.47 [−6.16, +1.22], z −1.50<!-- N:RES-8 --><!-- N:DX-19 --> | +0.13 [−0.56, +0.81], z +0.41<!-- N:RES-8 --> | Šidák-corrected 95 % |
| replicate difference: the p = 0 sweep arm − ISO-4 | 20 / 20<!-- N:DES-13 --> | +1.21 [−2.79, +5.20]<!-- N:DX-19 --> | −0.15 [−0.86, +0.56]<!-- N:RES-9 --> | 95 %, across GPUs |

The replicate is reported beside the registered Γ₄ and cannot change its reading.

Mediation is VOID<!-- N:SEC-7 -->. The registered mediator, the counter's realized count during training, had a first-stage slope on p of −1.03 × 10⁻⁵, 95 % [−2.91 × 10⁻⁵, +0.93 × 10⁻⁵]<!-- N:DX-29 -->, and a rule fixed before the sweep was read voids the analysis when that interval contains zero (Appendix D). Diagnosed after the run, with the rule unchanged: the counter counts collapse-seeded ignitions inside an alive agent's crop<!-- N:CO-4 -->, which only Coupling A produces. In these mixtures it measures the Coupling-A frequency that the sweep holds fixed, and it cannot register co-occurrence.

Floors exist only for the sweep's p = 0.5 arm: the other sweep arms assume that floor, and the identification arms are ungraded<!-- N:DX-306 -->. The counter's realized count is endogenous, so nothing here is its causal effect.

<!-- PAPER V3 DRAFT (PAPER V3 ruling, 2026-10-12): builder-drafted, not owner-approved -->

### G The interaction check in full

<!-- STUB-SPEC
JOB: The interaction check's full record: what was planned and fixed before the run (PLAN.md, by section, not reproduced), the floors and the cross-GPU check, the per-arm and pooled table, the main effects (descriptive), and realized cost.
WRITER: W5.
BUDGET: about 400 prose words plus tables.
FROM: P1 §6.1 G; PLAN.md §2 to §9.
ROWS: IC-* only (orchestrator, from the committed step-0.5 report).
REGISTERED STRINGS: none; label "post hoc"; the PLAN's "observed-SE MDE80" is a detection limit, not a bound.
EVERY OTHER CAVEAT in checks/caveats.yaml: pointer only ("§6.3", "Appendix D"), never restated. C26: any sentence about the interaction check carries "post hoc".
HOLES:
  - everything numeric; the tables; the realized GPU-hours (from the run's timings.txt, never the estimate).
NOT HERE: a cross-arm test; Low or High; the estimate of 1.7 to 2.7 GPU-hours as if realized.
V2 MATERIAL: none.
DEPENDENCIES: step 0.5 results and their commit; §6.4 points here.
-->

The interaction check of §6.4 is post hoc. It was proposed after the registered result was known and was fixed in a written analysis plan before any of its evaluations ran. The analysis script refuses to run unless that plan is committed and unchanged and its hash matches the one the evaluation run recorded, so a later edit to the plan shows as a refusal. The supplement carries no version history, so the analysis does not run from it (§8). The check never joins the confirmatory family and changes no registered reading.

Each condition is θ\* with only $\kappa_A$ and $\kappa_B$ changed: neither coupling (both 0), Coupling A only ($\kappa_A = 0.06$<!-- N:CA-1 -->, $\kappa_B = 0$), Coupling B only ($\kappa_A = 0$, $\kappa_B = 1.0$<!-- N:CB-1 -->), and both, which is θ\* itself. β = 0.49<!-- N:CAL-3 -->, δ = 1.0<!-- N:COM-6 --> and every other fixed value stay at θ\*'s. The three new configurations are generated from θ\*'s file, and a test asserts that each loads to θ\* with exactly its κ values replaced.

The policies are the final checkpoints, at update 1000<!-- N:DES-13 -->, of every ISO and JOINT run (72 seeds each<!-- N:DES-3 -->) and every ISO-4 run (20 seeds<!-- N:DES-13 -->), each archive verified against its recorded sha256 before use. Each policy is evaluated in each condition on the registered draw, 512 episodes from evaluation seed 0<!-- N:DES-13 -->, with actions sampled as trained. Because every condition uses the same seed, each policy meets the same initial states and random streams in all four, and the conditions differ only through the couplings. That gives 656<!-- N:IC-1 --> main evaluations and 36<!-- N:IC-2 --> more for the self-floor. The arms met the four conditions differently in training: ISO trained on each coupling alone with links intact and on neither coupling with links denied, ISO-4 only on each coupling alone with links intact, and JOINT only with every stressor on, all at β = 0.43 and 0.70<!-- N:CAL-3 -->, never at 0.49<!-- N:CAL-3 -->. This is why the arm rows are reported beside the pooled one.

For policy $i$, $J_i(c)$ is its mean completion or survival over the episodes in condition $c$, and $I_i$ is the contrast displayed in §6.4. An arm's estimate is the mean of $I_i$ over its seeds, with the standard error from their spread, which carries both seed and episode-sampling variation. The pooled estimate weights each arm by its number of seeds and does not assume that the arms share one $I$. The family is three arms and the pool on two co-primaries, eight<!-- N:IC-4 --> intervals, Šidák-corrected (z ≈ 2.73<!-- N:IC-5 -->); the intervals are normal, as for the registered contrasts and Γ₄. Each estimate's detection limit is its 80 %-power MDE from the observed standard error<!-- N:METH-7 -->. Differences in $I$ between arms are reported without a test. Outside the family and with no reading rule, the report also gives each arm's four condition means and the main effects $J(\text{A only}) - J(\text{neither})$ and $J(\text{B only}) - J(\text{neither})$, which show whether each coupling alone moves the trained policies at θ\*.

For the first-seed checkpoint of each arm, every condition is evaluated three<!-- N:IC-3 --> more times on the run's GPU, so each checkpoint and condition has four<!-- N:IC-3 --> copies. The analysis reports whether the copies are bit-identical, their spread per metric and the spread of $I$ across copies. Each condition is floored separately: the earlier finding that evaluations at θ\* reproduce exactly on one GPU (§8) is not assumed for the other conditions. If any copy differs, a detectable reading also needs the estimate to exceed, in absolute value, twice the largest floor spread of $I$, the post hoc two-sigma floor-grading convention. The "both" evaluation of every policy is also compared, descriptively, with the original evaluation of the same checkpoint at θ\*, and the report states how many agree on both co-primaries.

An estimate shows a detectable interaction if its Šidák interval excludes zero and the floor check is met; its sign and size are then reported, for survival also in agents per episode (× 12<!-- N:ENV-6 -->). Otherwise it is an exclusion with its bound: $\lvert I\rvert < B$ at the family-corrected level, where $B$ is the larger absolute end of the interval, with the detection limit beside it. The pooled pair is the headline; the arm rows say whether the answer depends on how the policies were trained. If the floor or the comparison with the original evaluations cannot be computed, the analysis refuses rather than report part of the family. What the check is blind to is listed in §6.4; the arms' training conditions are given above.

<!-- HOLE:INTERACTION -->
<!-- fills: per-arm and pooled table; floors; cross-GPU identical count; main effects; realized GPU-hours (IC rows) -->

<!-- PAPER V3 DRAFT (PAPER V3 ruling, 2026-10-12): builder-drafted, not owner-approved -->

### H Trained-policy episodes

<!-- STUB-SPEC
JOB: Two trained-policy episodes, one ISO and one JOINT, shown separately, illustrative (FIGURE BATCH A3). Kept by default; the owner may drop this appendix (V3Q10; P2 recommends dropping it).
WRITER: W5.
BUDGET: about 80 prose words; captions at most 60 words each.
FROM: v2 Appendix I; FIGURE BATCH A3; P2 §6 (drop recommended).
ROWS: ENV-13, ENV-6, DX-410.
FIGURES: Figures H1 (ISO) and H2 (JOINT): H1, then a sentence, then H2, never side by side; gloss labelled “obs v3” once. Blocks below.
REGISTERED STRINGS: "illustrative".
EVERY OTHER CAVEAT in checks/caveats.yaml: pointer only ("§6.3", "Appendix D"), never restated. C26: any sentence about the interaction check carries "post hoc".
OWNER-PENDING:
  - V3Q10 (drop the appendix).
NOT HERE: any alive count, completion, return or comparison between the two episodes; agent numbers.
V2 MATERIAL: paper/v2/sections/14_appendix_plan_provenance.md (I).
-->

<!-- OWNER-PENDING:V3Q10 -->
<!-- default kept: this appendix stays; the alternative drops it (P2's recommendation) -->

Figures H1 and H2 show one episode of each confirmatory arm, chosen by a rule fixed before any render: θ\*, episode key 0, stochastic actions, training seed 1 at update 1000<!-- N:ENV-13 -->. Each opens at step 128 of 256<!-- N:DX-410 --><!-- N:ENV-6 -->. They are illustrative and support no comparison between the arms.

<!-- FIGURE H1: block carried from paper/v2/sections/14_appendix_plan_provenance.md:188 (markup, iframe height and alt text as v2 had them); caption replaced; the writer checks the alt text -->

<figure class="l-page">
  <iframe src="{{ 'assets/html/submission/explorer_thetastar_iso_s1_T1000_ep0.html' | relative_url }}" width="100%" height="700" style="border:none" title="Episode explorer, ISO policy, training seed 1" loading="lazy"></iframe>
  <figcaption><strong>Figure H1.</strong> One episode of the ISO policy at θ&#42;. The map shows the environment state, including the smoke field ρ. Selecting an agent shows its observation as masked by smoke (labelled “obs v3” on the figure), the true state of the same cells, and the probability τ that each cell was seen. <span class="interact">Play, step, or click an agent.</span></figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/explorer_thetastar_iso_s1_T1000_ep0_static.png" class="img-fluid" alt="Maps of one ISO-policy episode at its start, middle and end, with one agent's observation, the true state of the same cells, and the probability each cell was seen" caption="Static companion of Figure H1 for the printed PDF." %}
</div>

Figure H2 shows the JOINT policy's episode under the same rule; one episode of one seed cannot carry a contrast measured over 72 seeds per arm<!-- N:DES-3 --> and 512 evaluation episodes<!-- N:DES-13 -->.

<!-- FIGURE H2: block carried from paper/v2/sections/14_appendix_plan_provenance.md:199 (markup, iframe height and alt text as v2 had them); caption replaced; the writer checks the alt text -->

<figure class="l-page">
  <iframe src="{{ 'assets/html/submission/explorer_thetastar_joint_s1_T1000_ep0.html' | relative_url }}" width="100%" height="700" style="border:none" title="Episode explorer, JOINT policy, training seed 1" loading="lazy"></iframe>
  <figcaption><strong>Figure H2.</strong> One episode of the JOINT policy at θ&#42;, with the layers and panels of Figure H1. <span class="interact">Play, step, or click an agent.</span></figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/explorer_thetastar_joint_s1_T1000_ep0_static.png" class="img-fluid" alt="Maps of one JOINT-policy episode at its start, middle and end, with one agent's observation, the true state of the same cells, and the probability each cell was seen" caption="Static companion of Figure H2 for the printed PDF." %}
</div>

<!-- PAPER V3 DRAFT (PAPER V3 ruling, 2026-10-12): builder-drafted, not owner-approved -->

### I How the literature search ran

<!-- STUB-SPEC
JOB: I: how the literature search ran (moved from §2). J: how this paper was made, starting from the builder's recommendation quoted in PAPER V3 item 6, for the owner to edit.
WRITER: W5.
BUDGET: I about 150 prose words; J about 250 prose words.
FROM: P1 §6.1 I and J; PAPER V3 item 6 (log:6193-6202); v2 §2 "How we searched".
ORDER:
  - I: the search procedure and its verification (DX-101), as v2 §2 described it; the novelty caveat ("in the search described here we found no …").
  - J (heading "### J How this paper was made", below): the division of labour (the authors made the rulings, checked every word and are responsible for it; an LLM assistant drafted text, code, analyses, figures, reviews and proposed options, as the record documents); that some proposals came from the assistant, in particular that the inert-share bias and ISO-4 were first raised in an assistant-drafted review and adopted by the authors; that every sentence has a provenance record. Name the tool, never the author. The owner edits this; carried v2 A1 (scope and attribution) stays open.
ROWS: DX-101.
REGISTERED STRINGS: none.
EVERY OTHER CAVEAT in checks/caveats.yaml: pointer only ("§6.3", "Appendix D"), never restated. C26: any sentence about the interaction check carries "post hoc".
OWNER-PENDING:
  - the whole of J is the owner's to edit (PAPER V3 item 6); the footnote is the owner's alone.
  - carried v2 A1(i)–(iii).
NOT HERE: names, accounts, URLs, hashes; claims the record does not show (do not assert that the ideas are human-sourced; that is the owner's statement); the footnote text.
V2 MATERIAL: paper/v2/sections/02_related_work.md ("How we searched"); paper/v2/OWNER_QUESTIONS.md A1.
-->

We ran the literature search with the help of LLM-based research assistants, between August and October 2026<!-- N:DX-101 -->. A census of benchmark venues and a search for theorems that could subsume ours came first; a search of domain randomization, environment design, multi-task and robust-learning neighbours followed. Both used web search and the arXiv API and read abstracts. The works §2 describes in detail were then read in full; the remaining citations rest on their abstracts. We did not query IEEE Xplore. Wherever this paper says that no work does something, it means no work found by this search.

### J How this paper was made

<!-- OWNER-EDITS: the whole of Appendix J, from this heading to the end of the file, is a builder draft for the owner to edit (PAPER V3 item 6, docs/decision_log.md:6193-6202). The disclosure footnote on the abstract is the owner's alone and is not drafted here. -->
<!-- OWNER-PENDING:A1 -->
<!-- carried v2 A1: (i) the footnote's scope; (ii) attributing the review that first raised the inert-share bias and ISO-4 to the assistant (the draft below follows PAPER V3 item 6); (iii) whether the owner rewrites parts of the text -->

This study was carried out by its authors with an LLM assistant, Claude (Anthropic), used through Claude Code. The authors made or ratified the study's decisions, among them the environment's design, the constants fixed before the main experiment, the registered design, the scope of the post hoc interaction check, the reading of the results and the framing of this paper. Some decisions are recorded as delegated to the assistant: on the authors' instruction, the assistant made the remaining design decisions before the GPU rental, among them the seed layout, the run order, the branch rules and the ratification of the registered outcome framings, and the authors gave avoiding their own bias as the reason. A few later rulings were the assistant's call at the authors' request. From early in the project, a decision bound only once it was written into the project's dated decision record; before that rule, some directives existed only in conversation.

<!-- OWNER-PENDING:PLAN_OK no owner approval of PLAN.md is transcribed (log ends at the PAPER V3 PHASE 1 START entry); once the owner's OK is transcribed, replace the next sentence with "The authors approved that plan before the run" or similar -->

The analysis plan of the post hoc interaction check was written by the assistant, and no approval of it by the authors is yet recorded. The assistant implemented the code and tests to these decisions, ran analyses on the authors' instruction, drafted reports, figures and reviews of the design, proposed options for the authors to accept or reject, and drafted this paper's text section by section.

Some proposals came from the assistant. In particular, the inert-share bias in the isolated arm and the correcting arm ISO-4 were first raised in an assistant-drafted review of the registered design, and the authors adopted both and registered them before unblinding (Appendix D).

Every sentence of this paper has a provenance record that ties it to a decision, a row of the numbers ledger or a committed file, and every number in the text comes from that ledger, whose rows cite the file and line they were read from or show their derivation. Separate assistant instances reviewed the drafts. The authors checked every word and are responsible for the whole.

<!-- END OWNER-EDITS (Appendix J) -->
