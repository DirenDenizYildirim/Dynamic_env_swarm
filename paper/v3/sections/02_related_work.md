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

For Coupling A, the nearest neighbour we found is Raut et al. (2026) <d-cite key="raut2026psps"></d-cite>, a single-agent model of public-safety power shutoffs in which power flows resulting from the operator's switching set the failure probability of lines in wildfire areas, treated as ignition risk. <!-- OWNER-PENDING:v2C1 (carried v2 question C1 / Q4a: READS RULING item 2 recorded the owner's section 2 as final; this sentence keeps v2's accuracy fix OI-4 of the "about seven percent" sentence; DISPOSITIONS §5 gives C1 no V3Q number) -->In CHE, ignition is not an action available to the agents, though where they stand changes collapse rates (§3.2). For Coupling B, VULCAN degrades simulated sensing with smoke but has no transmittance model, and JaxWildfire's observations are partial but not attenuated. In our search (Appendix I), we found no reinforcement-learning environment whose observation kernel attenuates by transmittance. Among the JAX multi-agent benchmarks we surveyed, JaxMARL <d-cite key="rutherford2024jaxmarl"></d-cite>, Multi-Agent Craftax <d-cite key="alomari2025macraftax"></d-cite> and Assistax <d-cite key="hinckeldey2025assistax"></d-cite>, none has an evolving, spreading lethal hazard field or perception attenuated by a hazard.

Domain randomization and unsupervised environment design ask which distribution to train on, the latter adaptively <d-cite key="tobin2017dr,muratore2022drreview,dennis2020paired,jiang2021plr,jiang2021robustplr,parkerholder2022accel"></d-cite>; our worked example compares fixed distributions on a held-out configuration, a zero-shot generalization test <d-cite key="kirk2023zsg"></d-cite>, and evaluates no adaptive curriculum.

The closest earlier study of our question is Gao et al. (2024) <d-cite key="gao2024composition"></d-cite>, who ask, in visual imitation learning for robotic manipulation, whether policies compose environmental factors to succeed on unseen combinations. <!-- OWNER-PENDING:v2C1 (as above: v2's accuracy fix RC1-24 of the owner's "the strategy that covers more combinations does better"; RWV Part 3) -->Comparing data-collection strategies, they find that policies do compose and that a strategy cycling through factors, so that more combinations appear, is generally the most effective; their design, built for data efficiency, does not separate co-occurrence from how often each factor value appears. The DBCA method <d-cite key="keysers2020"></d-cite> builds train and test splits with similar distributions of single elements and different distributions of their combinations; our secondary sweep follows that idea, holding each coupling's frequency fixed while co-occurrence varies (Appendix F). <!-- OWNER-PENDING:v2C1 (as above: v2's accuracy fixes OI-3 of the owner's Erdem and Üre sentences) -->In robust reinforcement learning, Erdem & Üre (2025) <d-cite key="erdem2025mixed"></d-cite> report that single-agent policies trained against an adversary on one modality, observations or actions, remain vulnerable to simultaneous attacks on both (their Tables 3–4). Their attacked runs schedule no unattacked steps, and runs attacked on both modalities carry both budgets, so per-modality frequency, co-occurrence and total budget change together.

A survey of adaptability in multi-agent reinforcement learning (Hu et al., 2025, revised 2026) <d-cite key="hu2025adaptablemarl"></d-cite> calls an environment family highly diagnostic if it "systematically varies" factors such as observability or communication structure "while holding other factors fixed". It mentions compositional generalization but analyses no shift in several factors at once. Wherever we say that no work does something, we mean none found by that search.
