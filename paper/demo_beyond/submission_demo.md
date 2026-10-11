---
layout: distill
title: A multi-agent fire environment with a hazard-blind reward, and a pre-registered test of training on co-occurring versus isolated stressors
description: In the Compound Hostile Environment (CHE), structural collapse can add ignitions to a cellular-automaton fire, the fire’s smoke attenuates what agents perceive, and inter-agent communication can be denied; the fire itself optimizes against no one and enters no reward, cost or constraint channel.
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
  - name: "4 Severity calibration"
  - name: "5 Coupling A: collapse seeds the fire"
  - name: "6 Coupling B: smoke attenuates perception"
  - name: "7 Communication denial: inert under this encoder at this scale"
  - name: "8 Methodology: bars come with floors"
  - name: "9 The pre-registered compositional test"
  - name: "10 Limitations"
  - name: "11 Reproducibility"
  - name: "Appendices"
_styles: >-
  .print-companion { display: none; } @media print { .print-companion { display: block; } d-article figure iframe { display: none; } }
---

We introduce the Compound Hostile Environment (CHE), a pure-JAX multi-agent reinforcement-learning environment in which a cellular-automaton fire burns in every episode, structural collapse can add ignitions to it, and its smoke attenuates the agents’ perception, alongside an independent communication-denial axis. The fire is an ambient hazard: a fixed stochastic process with nothing in it optimizing against the agents, carried by no cost or constraint channel, and invisible to the reward, which reads only task variables and agent deaths and prices every death the same whatever its cause. Severity levels are placed relative to a measured percolation threshold, and each stressor is a parameter of one transition kernel, so ablations are bitwise-exact nested models; we also describe a measurement protocol in which reproducibility floors are measured per metric, per GPU and per artifact. As predicted before measurement, the supercritical fire consumes the fuel that collapse would ignite: under trained policies, collapse-seeded ignitions per episode fall 4.8-fold<!-- N:CA-4 --> from low to high severity. We then pre-register a test of whether training on co-occurring stressors beats training on each in isolation, at a held-out severity and matched compute, with 72<!-- N:DES-3 --> seeds per arm (above the registered seed ladder’s cap of 60<!-- N:DES-1 -->, a recorded deviation made before unblinding). Joint training raises survival by 0.96<!-- N:RES-2 --> points (Šidák-corrected 95 %<!-- N:DES-13 --> CI [0.47, 1.44]<!-- N:RES-2 -->); task completion shows no detectable change (−1.73<!-- N:RES-1 --> points, CI [−4.12, +0.66]<!-- N:RES-1 -->). Neither joint-versus-isolated difference keeps a stable sign over the final half<!-- N:RES-11 --> of training: the survival gap opens only in the last fifth<!-- N:RES-12 --> of the budget, and completion leans negative from 70 %<!-- N:RES-13 --> of it onward. The survival gain does not survive an inert-share correction registered before unblinding. Because communication denial is inert under our frozen random-projection message encoder at this scale, a third<!-- N:DES-8 --> of the isolated arm’s training episodes contain no active stressor. Removing them, in a 20<!-- N:DES-13 -->-seed sensitivity arm, raises isolated training’s survival by 0.98<!-- N:RES-7 --> points; joint training then differs from it by −0.03<!-- N:RES-6 --> points (CI [−0.68, +0.63]<!-- N:RES-6 -->), although it still sees each coupling twice<!-- N:DES-14 --> as often and always in combination. Studies of compositional generalization should therefore match the share of training that contains an active stressor before attributing a gain to composition.

<!-- BUILDER-WRITTEN DEMONSTRATION (DEMONSTRATION DRAFT ruling, 2026-10-11); not the owner's text -->

<figure class="l-page">
  <iframe src="{{ 'assets/html/submission/explorer_thetastar_random_seed0.html' | relative_url }}" width="100%" height="720" style="border:none" title="Episode explorer: one random-policy episode of CHE at the held-out configuration" loading="lazy"></iframe>
  <figcaption><strong>Figure 1.</strong> One episode of CHE. Twelve<!-- N:ENV-6 --> agents move on a 64 × 64<!-- N:ENV-6 --> grid for 256<!-- N:ENV-6 --> steps at the held-out configuration θ&#42;: fire transmissibility β = 0.49<!-- N:CAL-3 -->, Coupling A κ<sub>A</sub> = 0.06<!-- N:CA-1 -->, Coupling B κ<sub>B</sub> = 1.0<!-- N:CB-1 -->, communication denial δ = 1.0<!-- N:COM-6 -->. The map is environment state: fire, smoke field ρ, weak and collapsed floor, food, agents alive and dead, and collapse-seeded ignitions (Coupling A; here 11<!-- N:DX-33 --> collapse events, 7<!-- N:DX-33 --> seeded ignitions). Perception is only in the selected agent's three panels: its 9 × 9<!-- N:ENV-6 --> observation as produced, the true state of those cells, and P(seen) = τ, the Beer–Lambert transmittance through smoke. Fixed before rendering: θ&#42;, episode key 0, random policy, stochastic actions<!-- N:ENV-13 -->. No outcome is reported. <span class="figure-note">Status: illustrative · random policy · grades nothing · Interact: play (space), scrub or step (← →), jump between events with [ and ], toggle layers, click an agent; opens paused at t = 128<!-- N:DX-33 -->, agent 7<!-- N:DX-33 -->.</span></figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/explorer_thetastar_random_seed0_static.png" class="img-fluid" alt="Three map frames of one random-policy episode, at its start, middle and end, showing fire state, smoke density, weak and collapsed floor, collapse-seeded ignitions, food and agents, with one selected agent's observation, the true state of the same cells, and the probability that each cell was seen." caption="Static companion of Figure 1 for the printed PDF." %}
</div>

<!-- BUILDER-WRITTEN DEMONSTRATION (DEMONSTRATION DRAFT ruling, 2026-10-11); not the owner's text -->

## 1 Introduction

When a training distribution has to cover several stressors, its designer chooses whether the policy meets them together or one at a time, and the choice matters most when they interact. Ecology studies the interactive and cumulative effects of multiple stressors <d-cite key="crain2008stressors"></d-cite><d-cite key="cote2016stressors"></d-cite>, and climate science studies compound events and their risk in their own right <d-cite key="zscheischler2018compound"></d-cite><d-cite key="zscheischler2020typology"></d-cite>. In reinforcement learning the choice is a question of zero-shot generalization <d-cite key="kirk2023zsg"></d-cite>: must a policy see stressors co-occur in training to cope with their co-occurrence at test time? Gao et al. (2024) <d-cite key="gao2024composition"></d-cite> studied it for imitation-learned manipulation; we study it for survival in multi-agent reinforcement learning.

Where the hazard sits in the learning problem decides what such a comparison can teach. In some fire-related work the hazard is the task, as for aerial agents rewarded for moving to burning trees on a fire's boundary <d-cite key="haksar2018"></d-cite>; safe reinforcement learning typically places it in a cost or a constraint <d-cite key="garcia2015safe"></d-cite>. In the Compound Hostile Environment (CHE) it does neither. The fire is an *ambient hazard* (Definition 2, §3): a fixed stochastic process with nothing in it optimizing against the agents, carried by no cost or constraint channel and invisible to the reward, which reads task variables and agent deaths and prices every death at $d_p = 0.5$<!-- N:ENV-1 -->, whatever its cause. Such a hazard is not new in itself; what it gives this study is a comparison in which no reward or cost signal mentions the hazard in either arm. Proposition 1 shows that the fire, which looks like nonstationarity to any one agent, is state: CHE is a well-defined Dec-POMDP, whose states reachable within the horizon form a finite set (§3). With communication denied it does not reduce to a multi-agent POMDP, and finite-horizon Dec-POMDPs are NEXP-complete <d-cite key="bernstein2002"></d-cite>, so we learn policies rather than plan (Remark 1).

Figure 1 shows one episode. CHE is written in pure JAX, and a cellular-automaton fire burns in every episode. For the idealized kernel the burnt region is exactly a bond-percolation cluster (Proposition 2) <d-cite key="grassberger1983"></d-cite><d-cite key="kesten1980"></d-cite>, so the three<!-- N:CAL-3 --> severities are values of the fire's transmissibility β placed below, near and above a *measured* percolation threshold of the implemented kernel (§4). Two stressors are coupled to the fire: collapse can add ignitions (Coupling A, of strength $\kappa_A$; §5), and smoke attenuates each agent's egocentric observation by Beer–Lambert transmittance (Coupling B, $\kappa_B$; §6). A third, link denial at level δ (§7), is independent of it; $\theta = (\beta, \kappa_A, \kappa_B, \delta)$ is the environment configuration. Each stressor is a parameter of one transition or observation kernel whose random numbers are drawn whether or not it is on, so switching it off reproduces the nested model's trajectories bit for bit under the same random keys (§3).

The training question becomes a pre-registered test of two training mixtures (Figure 2).

<figure class="l-page">
  <iframe src="{{ 'assets/html/submission/composer_training_mixtures.html' | relative_url }}" width="100%" height="430" style="border:none" title="Training mixtures of ISO, ISO-4 and JOINT by episode type" loading="lazy"></iframe>
  <figcaption><strong>Figure 2.</strong> What each arm trained on. Each bar splits one arm's training mixture into episode types: Coupling A only, Coupling B only, A and B together, and fire-only. ISO weights its single-stressor components at 1/6<!-- N:DES-16 --> each (A, B or δ alone, each at β 0.43<!-- N:CAL-3 --> and 0.70<!-- N:CAL-3 -->); ISO-4, the correction arm, drops ISO's δ-only components (1/4<!-- N:DES-16 --> each); JOINT's all-on components weigh 1/2<!-- N:DES-16 --> each. Beneath each bar are the per-coupling frequencies (ISO 1/3<!-- N:DES-7 -->, ISO-4 1/2<!-- N:DES-14 -->, JOINT 1<!-- N:DES-7 -->: JOINT sees each coupling 3×<!-- N:DES-7 --> as often as ISO and 2×<!-- N:DES-14 --> as often as ISO-4) and the active share (2/3<!-- N:DES-14 -->, 1<!-- N:DES-14 -->, 1<!-- N:DES-14 -->). It shows configured shares only: no outcome, no trained behaviour, no prediction. <span class="figure-note">Status: configuration facts, read from the committed training configs · grades nothing · Interact: switch ISO's δ-only third between “δ inert under a frozen random-projection encoder at this scale” (default; §7) and “nominal: δ counted” (where it counts as active); split the bars by β; hover a segment for its components and weights; open the table view.</span></figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/composer_training_mixtures.png" class="img-fluid" alt="Stacked bars of the three training mixtures by episode type, with each arm's per-coupling frequencies and the share of episodes that carry an active stressor." caption="Static companion of Figure 2 for the printed PDF." %}
</div>

An isolated arm (ISO) trains one policy on single-stressor configurations and a joint arm (JOINT) one on configurations with every stressor on, both at β = 0.43<!-- N:CAL-3 --> and 0.70<!-- N:CAL-3 -->; both are evaluated at θ\*, every stressor on at the near-critical β = 0.49<!-- N:CAL-3 -->, which neither saw. Architecture, hyperparameters, evaluation draw and compute (1000<!-- N:DES-13 --> updates per run) are matched, with one shared-parameter IPPO policy per training seed<!-- N:ENV-11 --> <d-cite key="dewitt2020ippo"></d-cite>. The estimand is the compositional gap Γ, JOINT's mean minus ISO's at θ\*, on two co-primary outcomes, task completion and survival rate, Šidák-corrected for m = 2<!-- N:DES-13 --> tests. Four<!-- N:DES-12 --> outcome branches, a framing for each and a falsifier for the asymmetric outcome were registered on 2026-08-13<!-- N:DES-12 -->, before the grid began (a fifth<!-- N:DX-102 --> outcome cell was added before unblinding, Appendix E). We ran 72<!-- N:DES-3 --> seeds per arm, above the registered seed ladder's cap of 60<!-- N:DES-1 -->, a recorded deviation made before unblinding (§9.1).

Figure 2 also shows two weaknesses, stated here before the result. First, JOINT sees each coupling three times<!-- N:DES-7 --> as often as ISO, so the endpoints differ in frequency as well as in co-occurrence. A secondary sweep in the spirit of DBCA <d-cite key="keysers2020"></d-cite> holds each coupling's frequency fixed while co-occurrence varies, but on the simplex of episode types it cannot also hold the fire-only share fixed, which rises with co-occurrence<!-- N:DES-9 -->, and it is non-verdict-bearing (§9). Second, communication denial is inert under our frozen random-projection message encoder at this scale (§7), so the third<!-- N:DES-8 --> of ISO's episodes that carry only δ are fire-only. The *active share*, the fraction of training episodes with at least one behaviourally active stressor, is therefore two thirds<!-- N:DES-14 --> for ISO and one<!-- N:DES-14 --> for JOINT. Figure 3 gives the registered readings at θ\*.

<figure class="l-page">
  <iframe src="{{ 'assets/html/submission/opening_ladder.html' | relative_url }}" width="100%" height="400" style="border:none" title="Registered readings: Γ and Γ₄ on survival and completion" loading="lazy"></iframe>
  <figcaption><strong>Figure 3.</strong> Survival: Γ REJECT; beneath it, Γ₄ null, “does not survive the inert-share correction”. Completion: Γ null; Γ₄ null, “second exclusion bound, X₄ = 0.0488<!-- N:RES-6 -->” (X₄ is Γ₄'s 80 %<!-- N:METH-7 -->-power minimum detectable effect). Γ is JOINT − ISO (k = 72<!-- N:DES-3 --> per arm, one GPU unit<!-- N:HW-4 -->); Γ₄ is JOINT − ISO-4 (k = 72 / 20<!-- N:DES-13 -->, cross-unit<!-- N:HW-4 -->), and ISO-4 is a sensitivity arm outside the confirmatory family. Estimates are rate differences at θ&#42; and matched compute (T&#42; = 1000<!-- N:DES-13 --> updates); the text quotes them × 100, as points. Intervals are Šidák-corrected 95 %<!-- N:DES-13 --> (m = 2<!-- N:DES-13 -->), conditional on one common evaluation draw; Γ₄'s completion interval, [−0.0481, +0.0228]<!-- N:RES-6 -->, is drawn but not printed. k = 72<!-- N:DES-3 --> is a recorded deviation from the registered cap of 60<!-- N:DES-1 -->. The figure cannot show how Γ moved during training (sign unstable over the final half; Figure 12); the full ladder is Figure 11 (§9.2). <span class="figure-note">Status: registered (Šidák-corrected 95 %, k = 72<!-- N:DES-3 -->) for Γ · sensitivity arm, outside the confirmatory family, for Γ₄ · Interact: none; a fixed reading of two rungs, which Figure 11 steps through with the rest.</span></figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/opening_ladder.png" class="img-fluid" alt="Joint minus isolated training and joint minus ISO-4, for survival and completion, each with its Šidák-corrected interval and registered verdict; the survival gain is shown beside the ISO-4 contrast, labelled does not survive the inert-share correction." caption="Static companion of Figure 3 for the printed PDF." %}
</div>

At θ\* the founding hypothesis, that joint training improves both outcomes, did not occur (Figure 3). Joint training raises survival by 0.96<!-- N:RES-2 --> points (Šidák-corrected 95 %<!-- N:DES-13 --> CI [0.47, 1.44]<!-- N:RES-2 -->; points are rate differences × 100), and the survival test rejects. Task completion shows no detectable change, −1.73<!-- N:RES-1 --> points (CI [−4.12, +0.66]<!-- N:RES-1 -->), which excludes a joint-training gain larger than 0.66<!-- N:RES-1 --> points. The falsifier registered for an asymmetric outcome passes (§9.2), so the asymmetry stands. Under Definition 2 it lies between a penalized channel, deaths, and a rewarded one, the task. Read over training, both co-primaries are **sign unstable over the final half**<!-- N:RES-11 -->: the survival gap opens only in the last fifth<!-- N:RES-12 --> of the budget, and completion leans negative from 70 %<!-- N:RES-13 --> of it onward (Figure 12).

The survival gain **does not survive the inert-share correction**. The fire-only third was registered as a bias, with ISO-4 to remove it, on 2026-09-18<!-- N:DES-15 -->, mid-grid and before unblinding; ISO-4 is ISO without its δ-only components, a sensitivity arm outside the confirmatory family with 20<!-- N:DES-13 --> seeds. Its survival is 0.98<!-- N:RES-7 --> points above ISO's, and Γ₄, JOINT minus ISO-4, is −0.03<!-- N:RES-6 --> points (Šidák-corrected 95 %<!-- N:DES-13 --> CI [−0.68, +0.63]<!-- N:RES-6 -->), and a same-card secondary replicate, proposed after Γ₄ was seen, agrees (§9.2). As the registration requires, we do not describe the survival advantage as a composition effect. Two limits apply. Γ₄'s upper bound, +0.63<!-- N:RES-6 -->, lies above Γ's lower bound, +0.47<!-- N:RES-2 -->: the correction excludes a large composition effect, not every one. And ISO-4 raises both the active share (from two thirds<!-- N:DES-14 --> to one<!-- N:DES-14 -->) and each coupling's frequency (from a third<!-- N:DES-7 --> to a half<!-- N:DES-14 -->), so its rise cannot say by itself which matters; §9.2 reports what the non-verdict-bearing secondary design adds, its slope on the fire-only share and where its plane fit fails. Once the active share is matched, JOINT's remaining differences add nothing detectable to survival, although it still sees each coupling twice<!-- N:DES-14 --> as often as ISO-4 and always in combination.

The argument is general, though measured in one environment: a joint-versus-isolated comparison that leaves the active share free can report an active-share effect as a composition effect. In the search described in §2, which read abstracts and did not query IEEE Xplore, we found no reinforcement-learning comparison that matches its arms on that share. We claim no convergence guarantee and no theorem that joint training wins: Proposition 4 bounds what isolated training can be *guaranteed* to transfer, not what it does, and Theorem 1 concerns adaptivity against memorization in a two-corridor toy. Nor do we claim an exact critical value for the implemented kernel, or a survival gap robust to the training budget: every comparison is at matched compute, none at convergence.

Our contributions are:

1. **An environment built as an instrument** (§§3–7): a lethal fire confined to the transition and observation kernels (Definition 2), each step factorized into collapse, fire, smoke, agents and communication (Proposition 1), severity by measured dynamical phase, bitwise-exact nested ablations, and theory that doubles as unit tests (Proposition 3, Theorem 1, Remark 2′).
2. **Calibration findings that stand alone** (§§5–7). Under trained policies, collapse-seeded ignitions fall 4.8-fold<!-- N:CA-4 --> from low to high severity, as the Coupling-A lock had recorded from the random-policy calibration before any trained policy was measured (§5), while their share near agents stays flat<!-- N:CA-6 -->. Smoke costs survival at high severity (the same direction in three of three<!-- N:CB-5 --> replicates; masking concentrated 16–118-fold<!-- N:CB-10 --> on moments of danger), but measured −0.03<!-- N:CB-9 --> points at the test's medium severity, graded only against a three-seed<!-- N:CB-9 --> spread. Communication is inert under a frozen random-projection encoder at this scale.
3. **A measurement protocol in which acceptance bars come with floors** (§8): floors per metric, per GPU and per artifact; contrasts graded on their own standard error; design-stage power as the minimum effect detectable with 80 %<!-- N:METH-7 --> power at the family-corrected α; the bars without a floor named.
4. **A pre-registered test of joint against isolated training** (§9), whose survival advantage does not survive a correction registered before unblinding, and a rule whose argument is general: match the active share before attributing a gain to composition.

<!-- BUILDER-WRITTEN DEMONSTRATION (DEMONSTRATION DRAFT ruling, 2026-10-11); not the owner's text -->

## 2 Related work

For each line of work, this section says where it places the hazard and what its comparisons hold fixed. §1 stated what ours holds fixed (Figure 2); how we searched is described at the end.

**Where the hazard enters learning.** Table 1 sets the nearest fire-related and safety-related work beside CHE.

**Table 1.** Where the hazard enters the learning or planning problem.

| work | agents and method | where the hazard enters |
|---|---|---|
| Haksar & Schwager (2018) <d-cite key="haksar2018"></d-cite> | aerial agents fighting wildfire; multi-agent deep Q-network | **the task**: a reward for moving to burning trees on the fire's boundary (their Algorithm 2); the paper gives the fire no way to harm the agents |
| JaxWildfire (Çakır et al., 2025) <d-cite key="cakir2025jaxwildfire"></d-cite> | one air-tanker agent; JAX cellular-automaton wildfire simulator | **the reward**, hazard-priced: a per-step penalty proportional to the number of burning cells, with a bonus for full extinction; harm to the agent is not described |
| safe reinforcement learning, as García & Fernández (2015) define it <d-cite key="garcia2015safe"></d-cite> | learning policies that maximize return while ensuring reasonable system performance and/or respecting safety constraints | **a constraint or a cost**, typically |
| VULCAN (Liu & Yan, 2026) <d-cite key="liu2026vulcan"></d-cite> | a proposed approach to multi-robot fire search and rescue, planned by a vision-language model rather than learned | **a hazard cost map** that folds in smoke, heat and sensing uncertainty |
| CHE (this paper) | 12<!-- N:ENV-6 --> agents; independent PPO | **ambient**: the transition and observation kernels only; no reward, cost or constraint reads the fire, and the reward prices each death at $d_p = 0.5$<!-- N:ENV-1 -->, whatever its cause |

CHE's reward is hazard-blind rather than hazard-priced (Definition 2): it prices an outcome, each death the same. VULCAN's preliminary evaluation covers baselines, not the approach itself, and its evaluation metric is also abbreviated CHE (cumulative hazard exposure), which is unrelated to our environment's name.

**A hazard that feeds on itself.** Coupling A lets structural collapse add ignitions. The nearest neighbour we found is Raut et al. (2026) <d-cite key="raut2026psps"></d-cite>, who model public-safety power shutoffs as a single-agent decision problem in which the power flows that follow the operator's switching decisions set the failure probability of lines in wildfire areas, which the authors treat as ignition risk; their reward is negative operating cost, and there is no spatial spread model. CHE's agents influence the hazard too, but weakly and indirectly: an occupied weak cell collapses nine times<!-- N:CA-8 --> as often per step as an empty one (Definition 5), yet agent load adds only 0.4–1.4 %<!-- N:CA-9 --> to the collapses per episode under the trained policies of §5, and 7.4–8.3 %<!-- N:CA-9 --> under random policies. Since a collapse may seed fire, we do not claim that CHE's hazard grows without agent influence. The difference from Raut et al. is one of directness and size: there the controlled decision sets the failure probability, while in CHE ignition is not an action available to the agents, and where they stand moves the collapse count only slightly.

**Perception degraded by the hazard.** VULCAN degrades simulated sensing with smoke density and visibility loss, and infers smoke density from image degradation and depth consistency, but has no transmittance model; JaxWildfire's observations are partial and egocentric but not attenuated. In the search described below, we found no reinforcement-learning environment whose observation kernel attenuates by transmittance, as Coupling B does along each line of sight through smoke.

**Simulators and benchmarks in JAX.** CHE follows JaxMARL's environment conventions <d-cite key="rutherford2024jaxmarl"></d-cite> and trains with independent PPO <d-cite key="dewitt2020ippo"></d-cite>. None of the JAX multi-agent benchmarks we surveyed, JaxMARL, Multi-Agent Craftax <d-cite key="alomari2025macraftax"></d-cite> and Assistax <d-cite key="hinckeldey2025assistax"></d-cite>, has an evolving, spreading lethal hazard field or perception attenuated by a hazard. Multi-Agent Craftax comes closest in kind: its agents lose health to hunger and enemies and can die, but its lava is static terrain that agents cannot enter. In Crafter and in Craftax-Classic, the JAX reimplementation described alongside Craftax, lava is lethal, and Crafter and Craftax reward each health point regained and penalize each one lost <d-cite key="hafner2022crafter"></d-cite><d-cite key="matthews2024craftax"></d-cite>, pricing an outcome rather than the hazard, much as our reward prices each death. POBAX <d-cite key="tao2025pobax"></d-cite> is a single-agent suite for partial observability, BenchMARL <d-cite key="bettini2024benchmarl"></d-cite> a multi-agent benchmarking library built on TorchRL rather than JAX, and JaxWildfire has a spreading fire in JAX, with one agent.

**Choosing a training distribution.** Domain randomization trains on a broad, fixed distribution over simulator parameters so that the deployed setting looks like one more sample <d-cite key="tobin2017dr"></d-cite><d-cite key="muratore2022drreview"></d-cite>. Unsupervised environment design adapts the distribution to the learner instead: PAIRED generates environments from a regret objective <d-cite key="dennis2020paired"></d-cite>, Prioritized Level Replay revisits levels by their estimated learning potential <d-cite key="jiang2021plr"></d-cite> and was later recast as environment design <d-cite key="jiang2021robustplr"></d-cite>, and ACCEL evolves levels near the frontier of the agent's ability <d-cite key="parkerholder2022accel"></d-cite>. These methods ask which distribution to train on, usually adaptively; we compare two fixed distributions and evaluate no adaptive curriculum (§10). Our held-out test belongs to the broader problem of zero-shot generalization <d-cite key="kirk2023zsg"></d-cite>.

**Compositional generalization over environmental factors.** The closest earlier study of our question is Gao et al. (2024) <d-cite key="gao2024composition"></d-cite>. In visual imitation learning for robotic manipulation, they ask whether policies compose environmental factors (object type and position, table texture and height, camera position) to succeed on unseen combinations, and use the answer to design data collection. They compare strategies, among them one that varies a single factor at a time from a base setting and one that cycles through factors so that more combinations appear, at a matched number of demonstrations and across levels of a rough effort proxy, the number of factor changes (their §III-C and §IV-A). Policies do compose, more weakly when both factors are physical (their §V-B), and the strategy that covers more combinations does better. Their design is built for data efficiency, not to separate co-occurrence from how often each factor value appears; ours matches compute and, in the ISO-4 correction, the share of training that carries any stressor. The settings differ too: their factors change what the robot sees and must do, and their policies are learned by imitation, while two of our stressors are causally coupled to a lethal hazard and our policies are learned by multi-agent reinforcement learning. CompoSuite <d-cite key="mendez2022composuite"></d-cite> studies compositional multi-task reinforcement learning over robots, objects, objectives and obstacles: composition of tasks, not of co-occurring stressors. The DBCA method <d-cite key="keysers2020"></d-cite> builds splits whose atom distributions are similar and whose compound distributions differ. Our secondary sweep follows that idea, holding each coupling's frequency fixed while co-occurrence varies; our ISO and JOINT endpoints do not, since JOINT sees each coupling three times<!-- N:DES-7 --> as often as ISO (§1, §9).

**Mixed and simultaneous perturbations.** Robust reinforcement learning asks the same question about perturbations. Erdem & Üre (2025) <d-cite key="erdem2025mixed"></d-cite> train single-agent continuous-control policies against a learned adversary that perturbs observations, actions, or both, at every step (their §3.4 and Algorithm 1). They report that agents trained against one modality remain vulnerable to simultaneous attacks on both (their Tables 3–4), and agents trained against their balanced mixed adversary do better under single-type attacks than those trained against a naive mixed adversary (their Table 5). No arm trains on a mixture of single-type attacks: each single-type arm never meets the other modality, and the mixed arms carry the combined budget, which the authors note is more severe. Every adversarially trained arm is perturbed throughout, so nothing in their design corresponds to the fire-only share our correction removes. What it bundles (per-modality exposure, co-occurrence and a larger budget) is nearer to what our corrected contrast leaves in, where JOINT still sees each coupling twice<!-- N:DES-14 --> as often as ISO-4, though their single-type arms see the other modality not at all. Their result is therefore not a test at matched per-modality exposure, and it neither supports nor contradicts our corrected null. Agrawal et al. (2023) <d-cite key="agrawal2023multimodal"></d-cite> train multi-agent policies against random reward, state and action noise, one or two noise types at a time, with a curriculum that raises the noise level and sets training length, so exposure differs between their models. In supervised vision, Tramèr & Boneh (2019) <d-cite key="tramer2019multiple"></d-cite> and Hsiung et al. (2023) <d-cite key="hsiung2023compositional"></d-cite> study robustness to multiple and to composite perturbations.

**Theory.** Chen et al. (2022) <d-cite key="chen2022understandingdr"></d-cite> model domain randomization as returning the optimal history-dependent policy of a latent MDP, a set of fully observed MDPs that differ in their transitions. Every upper bound they prove on its shortfall against the optimal policy of the true MDP assumes each MDP is communicating, with bounded diameter; without that assumption, their Proposition 1 shows the shortfall can grow linearly in the horizon, through an irreversible choice made before anything distinguishes the candidate MDPs. Theorem 1 here (§6) is kin to that construction but not covered by it. Its no-information endpoint has the structure of their Proposition 1's uninformed commitment, with two branches. But its two-corridor toy, with the signals encoded as states, has an absorbing failure, so their diameter assumption fails and their upper bounds do not apply; it has a single terminal reward and can reveal the environment before the branch, which their Proposition 1 does not address; and it measures a different gap, the adaptive optimum against the policy optimal for a fixed map rather than against the optimum for a known environment. Chen et al. therefore do not subsume Theorem 1, and Theorem 1 does not extend their bounds. Pynadath & Tambe (2002) <d-cite key="pynadath2002"></d-cite> relate the complexity of team decision problems with communication to observability: free communication lowers the complexity when the world is collectively observable (their Theorem 4 and Table 2), and makes no difference when it is individually observable or not observable at all (their Theorems 5–6). Remark 2′ (§7) refines this for collective partial observability: communication's marginal value vanishes when interchangeable agents' views are redundant, and returns when roles are irreplaceable or deaths are costly. The survey by Hu et al. (2025, revised 2026) <d-cite key="hu2025adaptablemarl"></d-cite> of adaptability in multi-agent reinforcement learning calls an environment family highly diagnostic if it "systematically varies" factors such as population, observability or communication structure "while holding other factors fixed"; it mentions compositional generalization but does not analyse shifts in several factors at once.

**How we searched.** We searched with LLM-based research assistants between August and October 2026<!-- N:DX-101 -->: first a census of benchmark venues and a search for theorems that could subsume ours, then a search of domain-randomization, environment-design, multi-task and robust-learning neighbours, both through web search and the arXiv API, reading abstracts. The works this section describes in detail were then read in full; the remaining citations rest on their abstracts. We did not query IEEE Xplore. Wherever this paper says that no work does something, it means no work found by this search.

<!-- BUILDER-WRITTEN DEMONSTRATION (DEMONSTRATION DRAFT ruling, 2026-10-11); not the owner's text -->

## 3 The environment

CHE is a grid world in which a team of agents forages while a fire burns. This section states the environment formally, pairs each statement with the code that implements it, and gives the one instance used in every reported experiment. Figure 4 shows one environment step.

{% include figure.html path="assets/img/submission/fig01_schematic.png" class="img-fluid" alt="Five numbered boxes in a row, collapse, hazard, smoke, agents and comms, with a Coupling A arrow from collapse into the hazard box, a Coupling B arrow from smoke down to an observation box drawn from the post-step state, and comms denial entering the comms box with no hazard input." caption="Figure 4. One environment step of CHE." %}

<p class="caption">Five kernels sampled from s to s′ in the order of Proposition 1: collapse, fire, smoke, agents, communication. Coupling A (thick orange arrow) carries the collapse increment c′ − c into the fire kernel; Coupling B (thick blue arrow) carries the smoke field ρ′ into the observation kernel; the denial level δ enters the communication kernel, which has no hazard input. Each agent observes a 9 × 9<!-- N:ENV-6 --> egocentric crop of the post-step state. The agents kernel reads the post-step fields, T<sub>X</sub>(x, a, h′, c′), as the code and Definition 1 do. The arrow colours belong to this figure only; in the interactive figures orange is burning fire and blue marks agents. The reward is not drawn (Definition 2). <span class="figure-note">Status: schematic, no data · Interact: none (static figure).</span></p>

### 3.1 State, kernel and step order

**Definition 1 (Compound Hostile Environment).** A CHE is a Dec-POMDP $\mathcal{M}_\theta = \langle I, \mathcal{S}, \{\mathcal{A}_i\}, T_\theta, R, \{\Omega_i\}, O_\theta, \gamma \rangle$ with a finite set of agents $I$ on a grid $G$, action sets $\mathcal{A}_i$, observation sets $\Omega_i$, reward $R$ (Definition 2), observation kernel $O_\theta$ and discount $\gamma$. It is indexed by the *environment configuration* $\theta = (\beta, \kappa_A, \kappa_B, \delta)$: the fire's per-neighbour ignition probability $\beta$, the strengths $\kappa_A$ and $\kappa_B$ of Couplings A and B, and the communication-denial level $\delta$. Its state space factors as

$$
\mathcal{S} = \mathcal{X} \times \mathcal{H} \times \mathcal{P} \times \mathcal{C} \times \mathcal{K} \times \{0, \dots, T\},
$$

where $x \in \mathcal{X}$ holds the agents' positions $x_i \in G$, their alive flags $\alpha_i \in \{0, 1\}$ and the task state; $h \in \mathcal{H} = \{\mathrm{Fuel}, \mathrm{Burning}, \mathrm{Burnt}\}^G$ is the fire; $\rho \in \mathcal{P} = \mathbb{R}_{\ge 0}^G$ is the smoke field; $c \in \mathcal{C} = \{\mathrm{intact}, \mathrm{collapsed}\}^G$ is the structure; $k \in \mathcal{K}$ is the realized communication graph on $I$; and the last factor is the step index $t$, with horizon $T$. The transition kernel factorizes as

$$
\begin{aligned}
T_\theta(s' \mid s, a) = {} & \underbrace{T_C(c' \mid c, x)}_{\mathrm{collapse}} \; \underbrace{T_H^{\beta,\kappa_A}(h' \mid h, c, c')}_{\mathrm{fire;\ Coupling\ A}} \; \underbrace{T_\rho(\rho' \mid \rho, h')}_{\mathrm{smoke}} \\
& \times \underbrace{T_X(x' \mid x, a, h', c')}_{\mathrm{agents}} \; \underbrace{T_K^{\delta}(k' \mid x')}_{\mathrm{comms}},
\end{aligned}
$$

and agent $i$'s observation is drawn from the post-step state, $o'_i \sim O^i_{\kappa_B}(\cdot \mid x', h', \rho', c', k')$. The dependence of $T_H$ on the collapse increment $c' - c$ is Coupling A (§5); the dependence of $O^i_{\kappa_B}$ on the fire, through the smoke field $\rho'$ it produces, is Coupling B (§6). The weak-cell terrain that $T_C$ reads is drawn at reset and fixed for the episode (§5), and a training mixture (§9.1) draws $\theta$ once per episode, at reset. On notation: an unsubscripted $\gamma$ is always this discount, while the subscripted $\gamma_p$ and $\gamma_n$ of §9 are the secondary design's slopes; Corollary 1 (§4) writes its critical exponents as numbers.

**Proposition 1 (Well-posedness and Markov closure).** For every $\theta$, the process $s_t = (x_t, h_t, \rho_t, c_t, k_t, t)$ under any joint policy is a Markov chain, and $\mathcal{M}_\theta$ is a well-defined Dec-POMDP: finite-horizon optimal joint policies exist, and the standard value definitions apply.

*Proof.* Each factor of $T_\theta$ is a conditional kernel whose conditioning variables are components of $(s, a)$ or components of $s'$ already sampled within the same step: $c' \sim T_C(\cdot \mid c, x)$, then $h' \sim T_H(\cdot \mid h, c, c')$, then $\rho' = T_\rho(\rho, h')$ (deterministic), then $x' \sim T_X(\cdot \mid x, a, h', c')$, then $k' \sim T_K(\cdot \mid x')$. A sequential composition of Markov kernels is a Markov kernel on the product space, so $T_\theta$ is a valid transition kernel on $\mathcal{S}$ and $(s_t)$ is Markov. The action sets are finite. The state space itself is not, since $\mathcal{P} = \mathbb{R}_{\ge 0}^G$ is not a finite set; but every stochastic factor and the reset distribution have finite support, and $\rho$ evolves deterministically from $\rho_0 = 0$, so the states and observations reachable within the horizon form finite sets; restricted to them, $\mathcal{M}_\theta$ is a finite Dec-POMDP, so optimal finite-horizon joint policies exist by the standard argument. $\blacksquare$

From one agent's point of view the fire looks like nonstationarity. Proposition 1 says that formally it is state, evolving under a stationary kernel, so the standard value definitions apply.

**Remark 1 (Hardness).** Bernstein et al. (2002)<d-cite key="bernstein2002"></d-cite> show that finite-horizon Dec-POMDPs are NEXP-complete. With communication denied ($\delta > 0$), a CHE does not reduce to a multi-agent POMDP, so this hardness applies; it is why we learn policies rather than plan.

Listing 1, the body of the environment's `step` function, follows the factorization line by line: $c'$ from the pre-step occupancy; $h'$ as the fire's spread followed by the Coupling-A impulse from $c' - c$; $\rho'$ from $h'$; the agents against $h'$ and $c'$; and the link graph from the new positions and alive flags, on its own stream, with no hazard argument. The reward line reads the task reward and the two death counts and nothing else. (`tl` is the episode's $\theta$; the `frozen` branch is an early control that no configuration in this paper uses.) The observation is then drawn from the new state (`che/env/env.py:394-397`).

**Listing 1.** One environment step in the order of Proposition 1.

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

### 3.2 The fire and its smoke

**Definition 3 (Fire kernel).** Each cell is Fuel, Burning or Burnt. At each step, independently for each ordered pair of a Burning cell $g$ and a Fuel von Neumann neighbour $g' \in N(g)$, the cell $g'$ ignites with probability $\beta$. A Burning cell becomes Burnt after exactly one step, and Burnt is absorbing. Fuel cells may also ignite spontaneously at rate $\iota \ge 0$ per step; CHE uses $\iota = 0$<!-- N:DX-1 -->.

Every episode starts from an all-Fuel grid with one Burning cell at a uniformly random position (`che/env/env.py:241-243`). On every step the kernel draws one uniform per cell and incoming direction; these slots correspond one-to-one to the ordered pairs $g \to g'$, so per-pair independence is exact. Because a Burning cell is Burnt one step later, each unordered edge sees at most one ignition attempt in a trajectory, so these uniforms realize the per-edge Bernoulli variables of Proposition 2's coupling exactly (`che/env/hazard.py:8-16`). Cells outside the arena never burn; there is no wraparound.

**Proposition 2 (Bond percolation).** Under Definition 3 with $\iota = 0$ and a single ignition at the origin, the set of eventually-Burnt cells is equal in distribution to the open cluster of the origin in i.i.d. bond percolation on $(G, E)$ with edge-open probability $\beta$.

Here $E$ is the set of von Neumann edges of the arena. The proof is a short coupling (Appendix A); it is the correspondence between an epidemic with a constant infectious period and bond percolation described by Grassberger (1983)<d-cite key="grassberger1983"></d-cite>, and it is what lets §4 define severity by percolation phase. Its hypotheses hold for CHE's fire on its own. With Coupling A on, collapses can add ignitions during the episode, and the burnt set is then no longer one origin's cluster.

Smoke outlives flame. Per cell,

$$
\rho' = e^{-\eta}\rho + \sigma_s \mathbf{1}[h' = \mathrm{Burning}],
$$

with emission $\sigma_s = 1.0$ and decay $\eta = 0.5$, held fixed by convention and never calibrated<!-- N:DX-1 -->. The update reads the post-step fire $h'$, so a cell emits $\sigma_s$ once, in the step it burns, and its smoke then decays geometrically; there is no spatial smoothing (`che/env/hazard.py:67-79`). The smoke field is state, not what an agent sees: an agent sees only its crop of the state, attenuated by Coupling B through $\rho'$.

Three stressors attach to these kernels, one parameter each: Coupling A ($\kappa_A$, Definition 5, §5) seeds the fire from new collapses, Coupling B ($\kappa_B$, Definition 6, §6) attenuates each agent's crop through $\rho'$, and communication denial ($\delta$, Definition 7, §7) thins the link graph that $T_K$ samples from positions and alive flags only.

### 3.3 Agents, deaths and a hazard-blind reward

The agents kernel $T_X(x' \mid x, a, h', c')$ acts in three deterministic stages (`che/env/env.py:159-196`). An alive agent on a cell that collapses in this step falls and is disabled before it moves. Survivors take one of 5<!-- N:ENV-8 --> actions, stay or a von Neumann move clipped to the grid; a move into a collapsed cell is cancelled, and Burnt cells are passable. Then an agent whose new cell is Burning in $h'$ is disabled, so a cell igniting under a standing agent kills it; Burning cells can be entered, and avoidance must be learned. A disabled agent stays disabled, holds still, collects nothing and vanishes from the others' observations. Death consumes no random numbers, so it cannot shift another kernel's stream.

**Definition 2 (Ambient hazard).** The hazard is *ambient* if and only if (i) and (ii) hold.

(i) *Reward independence.* The reward is a function of task variables and of the agents' alive transition only,

$$
R(s,a,s') = R_{\mathrm{task}}(\mathrm{task}(x), a, \mathrm{task}(x')) - d_p\,\lvert\{i : \alpha_i = 1,\ \alpha'_i = 0\}\rvert ,
$$

where $\mathrm{task}(x)$ denotes the task variables (in CHE, the food grid and the alive agents' positions) and $d_p \ge 0$ is a fixed death penalty; no term of $R$ references $h$, $\rho$ or $c$, and the hazard appears in no auxiliary cost or constraint channel: no CMDP constraint, no Lagrangian penalty, no safety critic.

(ii) *Non-adversarial.* $T_H$ is a fixed stochastic kernel: nothing in the environment optimizes, learns or best-responds.

Under clause (i), survival is learned through two hazard-blind routes: a dead agent collects no further task reward, and each death costs a fixed $d_p = 0.5$<!-- N:ENV-1 -->, whatever its cause, in every configuration this paper reports. Fire and collapse affect return only through the transition and observation kernels, never through the reward: the transition kernel disables agents and, for collapse, blocks moves; the observation kernel shows them to the agents, and through it Coupling B attenuates perception. The penalty prices an outcome, not the hazard. A hazard-priced reward signals the hazard's state whether or not anything is harmed: in JaxWildfire, for example, Çakır et al. (2025)<d-cite key="cakir2025jaxwildfire"></d-cite> penalize the agent at every step in proportion to the number of burning cells. CHE's reward carries information about the fire only through outcomes the task also suffers. At $d_p = 0$ only the first route would remain.

Listing 2 is the task reward: its signature admits the food and occupancy grids and nothing else, so no fire, smoke or structure argument can reach it. Listing 1's reward line subtracts $d_p$ times the sum of fire and collapse deaths, adding the two causes before pricing them.

**Listing 2.** The task reward reads food and occupancy only.

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

Two tests check clause (i). The reward-independence test steps states that differ only in fire, smoke or structure, with every fire and structure difference far from all agents so that the alive transition is pinned equal, and asserts identical rewards, with and without the death penalty (`che/tests/test_reward_independence.py`). It shows that the reward reads no hazard state directly, which is all such a test can show, since the fire is meant to change return through deaths. The cause-blindness test kills a standing agent by fire in one configuration and by collapse in another, with identical task state, and asserts that both steps return $-d_p$ (`che/tests/test_lethality.py:143-162`).

Clause (i) also fixes how the two co-primary outcomes of §9 enter learning. Survival is a penalized channel, each death costing $d_p$; completion is a rewarded channel, each collected item earning +1<!-- N:ENV-9 -->; neither mentions the fire. An asymmetric result between them is an asymmetry between a penalized channel and a rewarded one, and §9.2 reads it in those terms.

The record holds one ablation of $d_p$, from the calibration phase, and we report it with its scope: the fire alone with no coupling on, 500 updates<!-- N:ENV-2 -->, 3 seeds per cell<!-- N:ENV-2 -->, an observation encoding that predates the one used here, and means over the final training updates. Raising $d_p$ from 0 to 0.5<!-- N:ENV-1 --> moved High survival from 0.575 to 0.866<!-- N:ENV-2 --> and High completion from 0.765 to 0.821<!-- N:ENV-3 -->, moved Medium survival from 0.931 to 0.951 with completion 0.750 at both<!-- N:ENV-4 -->, and left Low tied, 0.991 against 0.992<!-- N:ENV-5 -->. It was not re-run under the current observation or with the couplings.

Clause (ii) does not make the hazard independent of the agents. An agent standing on a weak cell raises that cell's per-step collapse probability ninefold<!-- N:CA-8 -->, and a collapse can seed fire. Most collapses happen with no agent present: agent load adds 0.4–1.4 %<!-- N:CA-9 --> to the number of collapses per episode under trained policies (Phase-3 policies, 500 updates<!-- N:CA-9 -->) and 7.4–8.3 %<!-- N:CA-9 --> under random ones. The environment is non-adversarial in the formal sense, a fixed kernel with no objective, but it is not agent-independent (§2).

### 3.4 Nested models: ablations are exact by construction

Each stressor is a parameter of one kernel, and setting it to zero recovers a nested special case of the same model, never a different environment.

| stressor | parameter | lives in | off ($=0$) recovers | asserted by |
|---|---|---|---|---|
| Coupling A | $\kappa_A$ | $T_H$, through $c' - c$ | a fire blind to the structure | `che/tests/test_nesting.py` |
| Coupling B | $\kappa_B$ | $O^i$ | perception independent of the hazard | Listing 3 |
| communication denial | $\delta$ | $T_K$ | free, range-limited communication | `che/tests/test_comms.py` |

The fire's own $\beta$ is a parameter of the same kind, but it is positive in every configuration, and its value is set by severity relative to the measured threshold (§4).

One engineering rule makes the nesting exact: every stochastic branch consumes its random stream unconditionally, drawing its uniforms and comparing them against a probability that may be zero; no draw is gated on a parameter's value. Coupling B's reveal draw, the link draw and the per-episode mixture draw each use a stream derived from the reset or step key by a fixed tag, so adding them left the existing streams untouched. Setting a stressor to zero changes comparisons, never which random numbers are drawn, so the same keys reproduce the nested model's trajectory bit for bit, with no re-implementation or re-tuning of a separate environment.

Listing 3, the test for Coupling B, runs the environment at $\kappa_B = 0$ with the masking observation and with the observation that predates masking, under the same keys, and asserts bitwise-identical fire, smoke, structure, food, positions, alive flags and rewards. Stepping both by hand, it then asserts identical content planes, an all-ones visibility plane and a zero masked share.

**Listing 3.** With $\kappa_B = 0$, the environment is bitwise the one without Coupling B.

```python
# che/tests/test_coupling_b.py:131-156 (verbatim)
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
    # Obs-level recovery over a hand-stepped rollout with shared keys.
    key = jax.random.PRNGKey(3)
    key, k_reset = jax.random.split(key)
    obs3, s3 = reset(k_reset, cfg3)
    obs2, s2 = reset(k_reset, cfg2)
    for _ in range(20):
        assert (obs3["grid"][..., :7] == obs2["grid"]).all()
        assert (obs3["grid"][..., 7] == 1.0).all()
        key, k_act, k_step = jax.random.split(key, 3)
        actions = jax.random.randint(k_act, (4,), 0, 5, jnp.int32)
        obs3, s3, _, _, info3 = step(k_step, s3, actions, cfg3)
        obs2, s2, _, _, _ = step(k_step, s2, actions, cfg2)
        assert float(info3["masked_frac"]) == 0.0
    assert (s3.smoke > 0).any()  # the fire actually made smoke
```

The other two nestings have tests of the same kind. With $\kappa_A = 0$, collapse activity leaves the fire and smoke trajectories bitwise unchanged (`che/tests/test_nesting.py`); at $\delta = 0$, the environment reproduces a trajectory digest recorded before the communication channel existed (`che/tests/test_comms.py`). Because a gate such as `if kappa_A > 0:` around a draw on a dedicated stream would be invisible to behavioural tests, structural tests assert that the traced computation still contains its random-number primitives at parameter value zero. These tests run in the CPU suite; the digest is checked on the CPU only, since the smoke exponential is not bit-identical across backends.

### 3.5 The instance, training and metrics

Every reported experiment uses one instance: a 64 × 64 grid, 12 agents, a horizon of 256 steps, a 9 × 9 egocentric crop and 32 food items<!-- N:ENV-6 -->. Food is scattered on distinct cells at reset and does not respawn; agents start on uniformly random cells. An alive agent on a food cell collects it, for a team reward of +1 per item<!-- N:ENV-9 -->. The observation has 8 channels<!-- N:ENV-7 -->: six indicators (burning, burnt, food, weak, collapsed, alive occupancy), the raw smoke density, and Coupling B's visibility plane, which records which cells were revealed so that unseen can be told from absent; an agent's own cell is always revealed. An own-state vector gives the agent's row and column divided by the side $L$, its alive flag, and $t$ divided by the horizon<!-- N:ENV-7 -->.

All agents share one actor-critic network, which reads the agent's crop, its own-state vector and the aggregate of messages delivered to it: two convolutions with 16 and 32 channels, a dense layer of 128 units, and separate actor and critic heads with a 64-unit layer each<!-- N:ENV-10 -->. A message head emits a vector that neighbours receive one step later; it receives no gradient, so it emits a frozen-at-initialization projection of trained trunk features (§7).

Training is the independent PPO of de Witt et al. (2020)<d-cite key="dewitt2020ippo"></d-cite>, implemented in the PureJaxRL style of Lu et al. (2022)<d-cite key="lu2022dpo"></d-cite> on the environment conventions of JaxMARL, Rutherford et al. (2024)<d-cite key="rutherford2024jaxmarl"></d-cite>: one shared-parameter policy per training seed<!-- N:ENV-11 -->, with each agent's transitions treated as independent samples that all receive the team reward. Each update collects 128 steps from 256 parallel environments<!-- N:DX-2 -->, 32,768 environment steps<!-- N:DX-3 -->, each advancing all 12 agents<!-- N:ENV-6 -->. A run lasts T\* = 1000 updates<!-- N:DES-13 --> (a training budget, not the episode horizon $T$), 32,768,000 environment steps<!-- N:DX-3 -->, identical for every arm of §9. The other hyperparameters, the same for every run, are in Appendix B.

Two per-episode metrics are the co-primary outcomes of §9. *Completion* is $1 - F/32$<!-- N:ENV-6 -->, where $F$ is the number of food items remaining at the episode's last step. *Survival rate* is the fraction of the 12 agents<!-- N:ENV-6 --> alive at the last step. An episode ends only at the horizon, so an episode in which every agent has died still runs to it (`che/env/env.py:361`; `che/eval/harness.py:44-45`). Deaths are also recorded by cause, fire or collapse, as diagnostics; the reward does not distinguish them.

<!-- BUILDER-WRITTEN DEMONSTRATION (DEMONSTRATION DRAFT ruling, 2026-10-11); not the owner's text -->

## 4 Severity calibration

Severity in CHE is a measured dynamical phase of the fire, not a value of $\beta$ chosen by hand. Figure 5 shows the measurement the three levels rest on, beside one fire burning at each level.

<figure class="l-page">
  <iframe src="{{ 'assets/html/submission/severity_explorer.html' | relative_url }}" width="100%" height="520" style="border:none" title="Severity explorer: spanning probability against ignition probability, and one fire at each locked level" loading="lazy"></iframe>
  <figcaption><strong>Figure 5.</strong> Severity as a measured phase. Left: the spanning probability P<sub>span</sub>, the chance that a single centre ignition reaches the arena boundary, against the per-neighbour ignition probability β, on an all-fuel grid with no agents, for L = 32, 48 and 64 (±1 binomial SE; 512 seeds per point<!-- N:DX-7 -->). Vertical rules mark the locked levels, Low 0.43, Medium 0.49 and High 0.70<!-- N:CAL-3 -->, and a triangle marks β<sub>c</sub>(64) ≈ 0.486<!-- N:CAL-4 -->, where P<sub>span</sub> = ½ at L = 64. Right: one random-policy episode at each level on the 64 × 64 arena<!-- N:ENV-6 -->, episode key 0<!-- N:DX-202 -->, under the severity configurations (κ<sub>A</sub> 0.06<!-- N:CA-1 -->, κ<sub>B</sub> 1.0<!-- N:CB-1 -->, δ 0<!-- N:DX-202 -->), each panel captioned with its level's calibration values. Only the fire (fuel, burning, burnt) and the smoke field ρ (light hatching) are drawn, not agents, food or structure. The figure does not show the locked critical point β̂<sub>c</sub> or the crossing curves it was read from (§4.3); each render is one episode, neither a distribution nor trained behaviour. <span class="figure-note">Status: calibration, no agents (curves) · illustrative · random policy · grades nothing (renders) · Interact: press play or drag the time slider (arrow keys step one frame, Shift with an arrow ten); click a panel to highlight its level on the curves; open “table view” for the levels and their values.</span></figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/severity_explorer.png" class="img-fluid" alt="Spanning probability of a centre ignition against ignition probability for three grid sizes, with the three locked severities marked, beside one illustrative fire episode at each severity." caption="Static companion of Figure 5 for the printed PDF." %}
</div>

### 4.1 Phase structure of the idealized kernel

**Corollary 1 (Phase structure).** On $\mathbb{Z}^2$ with the von Neumann neighbourhood, the fire of Definition 3 with $\iota = 0$ and a single ignition inherits the phase structure of bond percolation (Proposition 2, whose coupling holds on any graph, in particular $\mathbb{Z}^2$):

1. *Critical point.* $\beta_c = 1/2$ exactly, a theorem of Kesten (1980)<d-cite key="kesten1980"></d-cite>.
2. *Subcritical,* $\beta < \beta_c$. The burnt cluster is almost surely finite; its expected size $\chi(\beta)$ is finite, the cluster-size distribution has exponential tails, and the correlation length $\xi(\beta)$ is finite.
3. *Critical scaling,* $\beta \uparrow \beta_c$. $\chi(\beta) \sim \lvert\beta - \beta_c\rvert^{-43/18}$ and $\xi(\beta) \sim \lvert\beta - \beta_c\rvert^{-4/3}$, the exponents of two-dimensional percolation.
4. *Supercritical,* $\beta > \beta_c$. With positive probability the fire spreads indefinitely; conditioned on that, the burnt region grows linearly in time, with an asymptotic front speed $v(\beta) > 0$ and a deterministic limiting shape.

The exact value belongs to the idealized kernel (von Neumann neighbourhood, constant burn time, homogeneous fuel, no wind) on the infinite lattice. Other neighbourhoods, heterogeneous fuel, wind or geometric burn times shift $\beta_c$ and break exactness; the existence of the transition and the divergence of $\chi$ and $\xi$ near it are universal, and the design relies on nothing more. CHE's fire kernel on its own is the idealized kernel on a finite arena (Coupling A adds ignitions; §3.2), so the threshold that matters is a finite-size one, and it is measured (§4.3). We do not measure the critical exponents: the lock's decision record notes that their asymptotic regime is out of reach at $L = 64$<!-- N:ENV-6 -->.

### 4.2 Severity as phase

**Definition 4 (Severity regimes).** Fix the arena side $L$. Severity levels are defined by the position of the implemented kernel relative to its measured critical point $\hat\beta_c$, through the correlation length $\xi(\beta)$:

- *Low*, subcritical, $\xi(\beta) \ll L$: fire clusters are local and short-lived, and survival is a local-avoidance problem.
- *Medium*, near-critical, $\xi(\beta) \sim L$: cluster sizes are scale-free up to the arena's size, fluctuations are maximal, and a single ignition can, with non-negligible probability, cascade to arena scale; survival is a global-anticipation problem.
- *High*, supercritical: fire fronts propagate at a speed $v(\beta) > 0$ comparable to the agents' speed, and survival is a race.

The three levels are qualitatively different phases of one kernel, so the question “why these three?” has a principled answer, and training at Low and High while evaluating at Medium (§9.1) asks for transfer to a phase that neither arm trained in. In the scalar $\beta$ it remains an interpolation (§10). When Definition 4 was written it also carried an expectation: that survival at Medium would be least predictable and the most interesting behaviour would appear there, put on record as the prediction that per-episode outcome variance peaks at Medium. That is a prediction, not part of the definition, and §4.4 reports its test.

### 4.3 Measuring the threshold and locking the levels

The calibration ran the fire with no agents on an all-Fuel grid, at $L \in \{32, 48, 64\}$ with 512 seeds per $(L, \beta)$<!-- N:DX-7 -->. A span sweep over 35 values of $\beta$ (0.05 to 0.95 coarsely, 0.40 to 0.60 in steps of 0.01), each from a single centre ignition for $T_{\max} = 4L$ steps<!-- N:DX-7 -->, measured $P_{\mathrm{span}}$, the mean burnt fraction and the front speed. A crossing sweep ignited the full left column and recorded the left–right crossing probability $R_L(\beta)$, whose curves for different $L$ cross near the threshold.

The severity lock fixed $\hat\beta_c = 0.500 \pm 0.005$<!-- N:CAL-1 -->, from logistic fits to $R_L$ with centres 0.4985, 0.5006 and 0.4999 at $L = 32, 48, 64$<!-- N:CAL-1 -->, and a self-duality check $R_L(0.500) = 0.488, 0.502, 0.494$<!-- N:CAL-2 -->. These values come from the lock's decision record, which states that they were recomputed independently from the raw calibration data; the raw data is committed, but no committed script or artifact produces the logistic centres. The committed estimators give a slightly wider picture: pairwise crossings of $R_L$ average 0.504<!-- N:CAL-1 -->, and the calibration report's estimators span [0.480, 0.513]<!-- N:DX-204 -->, with consensus mean 0.499<!-- N:CAL-1 -->. Together they bracket Kesten's ½. That agreement validates the implementation; it is not a finding about fire, since Proposition 2 and Corollary 1 predict it for this kernel. A slow CPU test re-checks the sigmoid and a fixed threshold band around ½ (`che/tests/test_percolation.py`).

The levels were then fixed by observables, each required to fall in a band, and locked with their measured values (calibration at $L = 64$<!-- N:DX-7 -->, 512 seeds<!-- N:DX-7 -->, no agents):

| level | $\beta$ | phase | $P_{\mathrm{span}}$ | burnt fraction | band the level was locked to |
|---|---|---|---|---|---|
| Low | 0.43<!-- N:CAL-3 --> | subcritical | 0.021<!-- N:CAL-3 --> | 1.9 %<!-- N:CAL-3 --> | $P_{\mathrm{span}} < 0.05$ and burnt fraction in [1, 5] %<!-- N:DX-201 --> |
| Medium | 0.49<!-- N:CAL-3 --> | near-critical | 0.547<!-- N:CAL-3 --> | 19.8 %<!-- N:CAL-3 --> | $P_{\mathrm{span}}$ in [0.3, 0.7]<!-- N:DX-201 --> |
| High | 0.70<!-- N:CAL-3 --> | supercritical | 0.998<!-- N:CAL-3 --> | 98.3 %<!-- N:CAL-3 --> | front speed in [0.5, 1.0] cells/step<!-- N:DX-201 -->, measured 0.83<!-- N:DX-6 --> |

At High the front moves at 0.83 cells per step, 83 % of the agents' speed of one cell per step<!-- N:DX-6 -->: it can be outrun, barely, and nearly the whole arena eventually burns. Medium sits between the finite-size pseudo-critical point $\beta_c(64) \approx 0.486$<!-- N:CAL-4 -->, where $P_{\mathrm{span}} = 1/2$ at $L = 64$, and $\hat\beta_c$, in the arena's near-critical regime. It is the severity of the held-out evaluation configuration of §9, $\theta^* = (\beta, \kappa_A, \kappa_B, \delta)$ = (0.49<!-- N:CAL-3 -->, 0.06<!-- N:CA-1 -->, 1.0<!-- N:CB-1 -->, 1.0<!-- N:COM-6 -->). The compositional test trains at Low and High only.

### 4.4 Re-testing the Medium prediction

The prediction was on record before its re-test at fixed policy (M3.0). The re-test used the calibration-phase probe at $d_p = 0.5$<!-- N:ENV-1 --> (the fire alone, 500 updates<!-- N:DX-203 -->, three seeds per severity<!-- N:DX-203 -->). That probe had saved no checkpoints, so it was re-run with the same configurations and seeds (equivalent, not bitwise identical), and the re-test evaluated its final checkpoints on 512 episodes each<!-- N:DX-203 -->. Its outcome has three parts:

- *Survival: refuted.* The per-episode variance at fixed policy is monotone in severity, 0.00091, 0.00709 and 0.00885 at Low, Medium and High<!-- N:CAL-5 -->, highest at High.
- *Completion: not confirmed.* Medium and Low tie within their bootstrap intervals, 0.01245 against 0.01235<!-- N:DX-8 -->, both above High.
- *Environment-level mechanism: confirmed.* With no agents, the variance of the burnt fraction peaks near $\beta \approx 0.53$<!-- N:DX-8 -->, inside the near-critical window just above the Medium level, and at the three locked levels it ranks Medium above High above Low.

The re-test report offers an account of the mismatch, not a separate test of it: outcome variance is roughly the environment's variance times the policy's sensitivity to it, and while the first factor peaks near criticality, the second grows with severity: at Low a trained policy absorbs the fire's fluctuations at the survival ceiling, and at High every realization couples into deaths and lost food. What the re-test establishes is narrower. Among the three levels the fire's own outcome varies most at Medium, a property of the environment; trained policies' survival does not, which refutes the prediction for survival, for these fire-only policies at this budget. What siting the held-out test at Medium costs is stated in §10.

<!-- BUILDER-WRITTEN DEMONSTRATION (DEMONSTRATION DRAFT ruling, 2026-10-11); not the owner's text -->

## 5 Coupling A: collapse seeds the fire

Coupling A lets structural failure feed the fire: a cell that collapses can ignite the fuel around it. In one illustrative random-policy episode, Figure 1's event track marks the collapse events and the collapse-seeded ignitions they caused (press <kbd>]</kbd> there to jump between them). Figure 6 counts the same events under trained policies, beside the two runs that test the theory.

<figure class="l-page">
  <iframe src="{{ 'assets/html/submission/coupling_a_explorer.html' | relative_url }}" width="100%" height="680" style="border:none" title="Coupling A explorer: collapse-seeded ignitions by severity, their share near agents, and the two Proposition 3 runs" loading="lazy"></iframe>
  <figcaption><strong>Figure 6.</strong> Coupling A under trained policies, and the two runs that test Proposition 3. <em>Top left:</em> collapse-seeded ignitions per episode at Low, Medium and High (β = 0.43 / 0.49 / 0.70<!-- N:CAL-3 -->) in the κ<sub>B</sub> = 1.0<!-- N:CB-1 --> arm of the Coupling-B grid m44 (4.05 / 3.41 / 0.84, a 4.83× fall<!-- N:CA-4 -->) and the κ<sub>A</sub>-on arm of the Coupling-A grid m35 (4.08 / 3.42 / 0.83, 4.92×<!-- N:CA-5 -->). <em>Top right:</em> the share of those ignitions inside an alive agent's 9 × 9<!-- N:ENV-6 --> crop, for all nine measured cells, with their range [0.164, 0.203]<!-- N:CA-6 --> as a band. <em>Bottom left:</em> the first Proposition 3 run, an L = 64 sweep with no agents (κ<sub>A</sub> 0.02, f<sub>weak</sub> 0.4<!-- N:CA-2 -->): burnt cells against realized seeded ignitions, through-origin fit R² 0.998<!-- N:CA-2 -->. <em>Bottom right:</em> the second run, a separate L = 32 test (κ<sub>A</sub> 0.003<!-- N:CA-3 -->) against a protocol-matched reference, given as values because it has no committed data file: ratio 0.992, inside [0.90, 1.02], R² 0.9995<!-- N:CA-3 -->. Neither run uses the locked parameters. The figure cannot show a floor for any trained-policy contrast: the m44 and m35 grids have no identical-run sets, so their whiskers are min–max over training seeds. <span class="figure-note">Status: reference scale (cross-artifact) for any floor; trained policies, 500 updates<!-- N:DX-40 -->; spreads are seed ranges · Proposition 3 panels: handshake runs, no agents · Interact: hover or tab to a point for its value; open “table view” for every number.</span></figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/coupling_a_explorer.png" class="img-fluid" alt="Collapse-seeded ignitions per episode at three severities for two trained grids, the share of them near agents, and the two Proposition 3 handshake runs shown separately." caption="Static companion of Figure 6 for the printed PDF." %}
</div>

### 5.1 Definition and implementation

**Definition 5 (Coupling A, as implemented).** Let $w(g) \in \{0,1\}$ mark weak terrain, a spatially clustered fraction $f_{\mathrm{weak}}$ of the cells drawn once per episode, and let $o_t(g) \in \{0,1\}$ indicate that at least one alive agent stands on cell $g$ before the step. An intact cell collapses at step $t$ with probability

$$
\lambda_t(g) = \big(\lambda_0 + \lambda_{\mathrm{load}}\,o_t(g)\big)\,w(g),
$$

so a cell that is not weak never collapses, and collapsed is absorbing. Coupling A then ignites, with probability $\kappa_A$, each cell that is still Fuel after this step's spread and lies within Chebyshev distance $r_A$ of a cell that collapsed in this step. The fire kernel therefore reads the collapse increment $c' - c$, not the stock of collapsed cells; a seeded cell is Burning in $h'$ and spreads from the next step on. Setting $\kappa_A = 0$ recovers the uncoupled fire kernel $T_H^{\beta,0}$: the ablation "no Coupling A" is a nested model of the full system, not a different environment.

The theory phrases the impulse per collapse event; the implementation draws one uniform per cell, so a cell in range of two new collapses is tried once, and the two rules coincide wherever seeding neighbourhoods do not overlap. The locked values, chosen from a random-policy calibration against target bands for collapses, seeded ignitions and collapse deaths per episode, are $(f_{\mathrm{weak}}, \lambda_0, \lambda_{\mathrm{load}}, \kappa_A, r_A) = (0.15,\ 5\times 10^{-5},\ 4\times 10^{-4},\ 0.06,\ 1)$<!-- N:CA-1 -->, so the seeding neighbourhood is a 3 × 3<!-- N:DX-37 --> block.

Agents influence collapse, weakly and indirectly. An occupied weak cell collapses nine times<!-- N:CA-8 --> as often as an empty one, but most collapses happen with no agent present: without load the locked parameters give about 7.81<!-- N:CA-9 --> collapses per episode, and agents add about 1 % to that under trained policies (0.4–1.4 %, Phase-3 policies at 500 updates<!-- N:CA-9 -->) and 7.4–8.3 %<!-- N:CA-9 --> under random ones. The fire is not independent of the agents, although ignition is not an action available to them.

Listing 4 is the whole of Coupling A in code.

**Listing 4.** Coupling A: the seeding mask, with its uniforms drawn whatever $\kappa_A$ is.

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

Its last three lines carry the claims: `u` is drawn before anything reads $\kappa_A$, so $\kappa_A = 0$ is the nested model bit for bit under the rule of §3.4; the dilation acts on the increment $c' - c$, so an old collapse seeds nothing; and `hazard.seed_ignitions` lights only cells that are still Fuel, which is where §5.3's fuel limitation enters.

### 5.2 The handshake with Proposition 3

**Proposition 3 (Collapse events dominate hazard exposure; divergence near criticality).** Work in the subcritical regime $\beta < \beta_c$ with $\iota = 0$, and suppose collapse events arrive at rate $\lambda_A$ per step, each seeding one ignition at a uniformly located Fuel cell, with seeded clusters pairwise disjoint (the sparse regime, $\lambda_A T \chi(\beta) \ll \lvert G \rvert$, the number of cells). Then the expected burnt area $B_T$ by time $T$ satisfies

$$
\mathbb{E}[B_T] = \lambda_A T\,\chi(\beta)\,\big(1 + o(1)\big), \qquad \text{and in general} \quad \mathbb{E}[B_T] \le \lambda_A T\,\chi(\beta),
$$

where $\chi(\beta)$ is the mean percolation cluster size. Consequently the marginal hazard exposure per unit of structural instability, $\partial\,\mathbb{E}[B_T]/\partial\lambda_A = T\chi(\beta)$, diverges as $\beta \uparrow \beta_c$ like $\lvert \beta - \beta_c \rvert^{-43/18}$.

The proof (Appendix A) grows each seed into a bond-percolation cluster by Proposition 2 and sums expectations; overlaps only remove double counting, and the divergence is Corollary 1. In this regime collapse is the fire's only birth channel, and near criticality one collapse has a divergent expected burnt area.

**Remark (finite-protocol corrections).** The equality branch of Proposition 3 is approached only under (i) an unconditional cluster-mass reference (a spanning-conditioned estimate underestimates it); (ii) a matched distribution of seed locations (boundary clipping lowers the mass of uniformly located seeds below a centre-seeded reference); (iii) matched seed ages (seeds born uniformly in time are age-averaged); and (iv) sparsity in both same-event sibling seeds and cross-cluster overlap, which deflate the measured slope and vanish as $\kappa_A, \lambda \to 0$. Every correction has a known sign.

We tested the proposition twice and report the two runs separately; they differ in grid size, regime and reference, and neither uses the locked parameters. Both run the fire and structure kernels with no agents and no primary ignition at the Low level, $\beta = 0.43$ with $\iota = 0$<!-- N:DX-304 -->, inside the proposition's subcritical regime. The first, a dense GPU sweep at L = 64 with $\kappa_A = 0.02$ and $f_{\mathrm{weak}} = 0.4$<!-- N:CA-2 -->, sweeps $\lambda_0$ and fits burnt area against the realized number of seeds through the origin: the relation is linear, $R^2 = 0.998$ over a 14× range of the expected seed count<!-- N:CA-2 -->. Its slope lies below the naive cluster-size reference, on the side the inequality permits, and the remark's four corrections compose to it within Monte Carlo error. The second, a slow CPU test in the suite at L = 32 in a purified regime ($\kappa_A = 0.003$<!-- N:CA-3 -->), computes its reference inside the test under the sweep's own protocol: slope over matched reference 0.992, inside the band [0.90, 1.02], $R^2 = 0.9995$<!-- N:CA-3 -->.

### 5.3 Under trained policies the coupling limits itself

Proposition 3 concerns the regime below criticality; above it, the fire removes what the coupling needs. Under trained policies (the Coupling-B grid m44, $\kappa_B = 1.0$ arm, 500 updates<!-- N:DX-40 -->), collapse-seeded ignitions per episode are 4.05, 3.41 and 0.84 at Low, Medium and High, a 4.83-fold fall<!-- N:CA-4 -->. The Coupling-A grid m35, with different policies and an earlier observation version, replicates it: 4.08, 3.42 and 0.83, a 4.92-fold fall<!-- N:CA-5 -->. Collapse never reads $\beta$; what changes with severity is where the seeds land. At High the supercritical fire burns 98.3 %<!-- N:CAL-3 --> of the arena in calibration (no agents), so most seeding attempts fall on burnt cells and the Fuel-only rule filters them out. With Proposition 3 this places the ignition channel's leverage below and near criticality: collapse seeds the most fire where the fire is otherwise rare, and at High the channel is marginal by construction (§10). That holds for the ignition channel; the Coupling-A grid's survival contrasts, on two seeds per arm<!-- N:CA-7 --> and with no floor, do not show where its effect on outcomes is largest.

The fuel limitation behind this fall was recorded before any trained policy was measured. At the Coupling-A lock (2026-07-21<!-- N:DX-401 -->), the random-policy calibration put seeded ignitions at High about 5.7 times<!-- N:DX-9 --> below Low at every $\kappa_A$ tried, and the lock recorded this as the fuel-exhaustion self-limitation of the ignition channel. A later prediction, registered before the analysis that produced the numbers above but after the trained results existed, had three parts: Coupling A is fuel-limited at High; the co-active count of §6 need not be monotone in severity; Medium may be its peak. The first is confirmed by the 4.83-fold fall<!-- N:CA-4 --> (its answer was already on record in the Phase-3 and Phase-4 reports, as that analysis notes). The second is not supported: the count is monotone non-increasing. The third is refuted: Low and Medium are indistinguishable<!-- N:DX-9 -->.

The fall happens upstream of the agents. The co-active count is the number of seeded ignitions times the share of them inside an alive agent's crop, and that share is flat: across all nine measured cells (both $\kappa_B$ arms of m44 and the $\kappa_A$-on arm of m35, at three severities) it lies in [0.164, 0.203]<!-- N:CA-6 -->. Severity changes how much seeded fire there is, not how much of it reaches an agent's view.

At Low the coupling moves survival off its ceiling. In the Coupling-A grid (M3.5: $\kappa_A$ from 0 to 0.06<!-- N:CA-1 -->, two seeds per arm<!-- N:CA-7 -->, 500 updates<!-- N:DX-40 -->), Low survival falls from 0.979 to 0.961<!-- N:CA-7 --> and fire deaths per episode rise from 0.062 to 0.229, 3.7-fold<!-- N:DX-10 -->. The policies do not respond by avoiding weak cells: weak-cell occupancy at Low is higher with the coupling on, by 0.054<!-- N:CA-7 -->, with no overlap between the arms' seed ranges; on two seeds per arm this is suggestive, not conclusive.

No contrast in this section is graded against a floor on its own artifact. The m44 and m35 grids have no identical-run sets, so their spreads are seed ranges and any floor beside them would be a reference scale (cross-artifact) (§8.6). The 4.83-fold fall<!-- N:CA-4 --> lies far outside those ranges and replicates on a second grid; the Low survival drop and the occupancy shift rest on two seeds per arm. §6 returns to the near-agent share: the co-active counter counts exactly these ignitions.

<!-- BUILDER-WRITTEN DEMONSTRATION (DEMONSTRATION DRAFT ruling, 2026-10-11); not the owner's text -->

## 6 Coupling B: smoke attenuates perception

Coupling B makes what an agent perceives depend on the hazard's own state. Figure 1 opens on agent 7 at t = 128<!-- N:DX-33 -->: beside the map, three panels show that agent's observation as produced, the true state of the same 9 × 9<!-- N:ENV-6 --> cells, and the probability that each cell was seen. The map's smoke layer is the state $\rho$; only the observation panel is perception, and its unseen cells tell the agent that it did not see them, not what they hold.

### 6.1 Definition and implementation

**Definition 6 (Coupling B: Beer–Lambert observation, as implemented).** Smoke is the per-cell state field $\rho'$ of §3.2, updated after the fire with no spatial smoothing, so it outlives flame. For agent $i$ at $x_i$ and a cell $y$ of its crop, let $\bar\rho_i(y)$ be the mean of $\rho'$ at the four points $x_i + t_s(y - x_i)$, $t_s = (s + \tfrac12)/4$ for $s = 0, \dots, 3$, each read at the nearest cell (smoke outside the grid reads 0). The transmittance is

$$
\tau_i(y) = \exp\!\big(-\kappa_B\,\lVert y - x_i \rVert_2\,\bar\rho_i(y)\big),
$$

a midpoint-rule form of $\exp(-\kappa_B \int_{x_i \to y} \rho\,d\ell)$ along the line of sight. Each crop cell is revealed independently with probability $\tau_i(y)$: a revealed cell passes its seven content planes, an unrevealed one passes zeros, and an eighth plane records the realized reveal<!-- N:ENV-7 -->, so the agent can tell "unseen" from "empty". The own cell has distance 0 and is always seen. $\kappa_B = 0$ gives $\tau \equiv 1$ and recovers hazard-independent observation.

Beer–Lambert attenuation is the standard optical model for light through smoke, so the coupling is physically grounded rather than an ad hoc noise schedule. What matters for learning is structural: perception quality is a function of the hazard's evolving state, so degradation concentrates where and when the fire is active, which an independent sensory-noise axis would not do. One property of the quadrature is documented and pinned by a test: its sample points never fall on a ray's endpoint, so a single isolated smoke cell near the edge of the crop does not occlude its own line of sight. The property was ruled acceptable because the fire's smoke is spatially extended.

Listing 5 shows the observation kernel's Coupling-B branch.

**Listing 5.** Coupling B in the observation kernel: transmittance, the reveal draw, and the visibility plane.

```python
# che/env/observation.py:289-310 (verbatim)
    if cfg.obs_version == 3:
        # Coupling B (Def. 6, M4.1): per-cell stochastic masking of the
        # content planes + the realized reveal mask as the final plane.
        # The uniforms are drawn unconditionally (invariant #3): at
        # kappa_B = 0, tau == 1 and u < 1 always, so the mask is all-ones
        # and the content planes are bitwise those of the pre-masking env.
        if key is None:
            raise ValueError("obs v3 requires a PRNG key for the reveal draw")
        # M6.0: kappa_B is traced, per episode, from the state — the mixture
        # varies it. Everything else observe() reads off cfg is static
        # (obs_version, window, grid size) and cannot be varied by a mixture.
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

In Listing 5 the `reveal` line draws its uniforms whatever $\kappa_B$ is, so at $\kappa_B = 0$ the mask is all ones and the environment is bitwise the one before masking (§3.4, Listing 3); the draw has its own stream, and $\kappa_B$ is read per episode from the state, which is how a training mixture varies it.

### 6.2 What attenuation does to the value of adaptivity

Theorem 1 states, in a toy, why attenuation by the hazard's own smoke matters to a learner.

**Theorem 1 (Memorization gap, and its erosion by Coupling B).** Consider the two-corridor environment $E_{2C}(\kappa_B)$: from a start cell, a path of $d$ steps leads to a branch $b$, from which two disjoint corridors $L$ and $R$ of length $\ell$ lead to the goal; the horizon is $T = d + \ell$ (zero slack: a wrong commitment cannot be undone). At $t = 0$ nature draws $Z \in \{L, R\}$ uniformly; corridor $Z$ burns at depth $\ell_f \ge 1$ beyond $b$, and an agent entering it is disabled. The reward is 1 for reaching the goal by $T$, else 0. At each step $t \le d$ the agent receives the signal $Y_t = Z$ with probability $e^{-\kappa_B (d - t + \ell_f)}$ (Beer–Lambert over the current distance to the fire, unit smoke density), else $Y_t = \varnothing$; signals are independent across time and remembered. Let

$$
q(\kappa_B) = 1 - \prod_{j=\ell_f}^{d+\ell_f} \big(1 - e^{-\kappa_B j}\big)
$$

be the probability of being informed by the commitment point. Then (1) the optimal value is $J^*(\kappa_B) = \tfrac12 + \tfrac12 q(\kappa_B)$; (2) the policies optimal for the fixed-map variant ($Z \equiv z_0$ constant) include the signal-blind policy "always take the corridor other than $z_0$", whose value on $E_{2C}$ is $\tfrac12$ for every $\kappa_B$, so the memorization gap is $J^*(\kappa_B) - J^{\mathrm{static}} = \tfrac12 q(\kappa_B) > 0$ for all finite $\kappa_B$; and (3) $q$ is continuous and strictly decreasing in $\kappa_B$, with $q(0^+) \to 1$ and $q(\kappa_B) \to 0$ as $\kappa_B \to \infty$, so under total perceptual denial the optimal adaptive policy is no better than the memorizing one.

*Proof (compact; in full in Appendix A).* With zero slack the only decision is the corridor at $b$. An informed agent (probability $q$) takes the corridor other than $Z$ and succeeds; an uninformed one faces exchangeable corridors and succeeds with probability $\tfrac12$. Hence $J^* = q + \tfrac12(1 - q)$, and no policy does better, since success needs information or a lucky guess. The signal-blind policy succeeds iff $Z = z_0$. Each factor $1 - e^{-\kappa_B j}$ is continuous and strictly increasing in $\kappa_B$ on $(0, \infty)$, which gives (3); the limits are immediate. $\blacksquare$

The theorem is narrow and exact: in one toy, a memorizing policy loses exactly half the probability of being informed, and the hazard's own attenuation shrinks that loss continuously to zero. It concerns optimal values in the toy, not what a learner does in CHE. It is also a test of the code. The toy and the observation kernel call one transmittance function, so on the toy (M4.2) the information probability agrees at every grid point whether it is computed by Monte Carlo on that function, by the closed-form product or through the full observation pipeline, and the measured optimal value matches $\tfrac12 + \tfrac12 q$ under a three-condition gate: largest $\lvert z \rvert$ 2.11, $\sum z^2 = 6.55$ on 8 degrees of freedom ($p = 0.586$), mean $z$ −0.44<!-- N:CB-4 -->. The memorizing policy stays flat at ½ (largest deviation 0.0084 at $\kappa_B = 5$, against 2 SE = 0.0110), $J^*(0) = 1.0000$, and $J^* - \tfrac12 = 0.0000$ at $\kappa_B = 8$, where $q = 0.0056$<!-- N:DX-14 -->.

### 6.3 The lock: three bands that did not intersect

The coupling strength $\kappa_B$ was to be locked where three bands, set before calibration, intersect: a masked share of the crop at Medium on fire-active steps in [0.15, 0.45]; a probability in [0.4, 0.7] that a Burning cell three cells away is revealed under typical Medium smoke; and a toy information probability $q$ in [0.3, 0.7]<!-- N:DX-301 -->. They do not intersect. The masked-share band is unreachable at Medium at any $\kappa_B$<!-- N:CB-3 -->: as $\kappa_B$ grows the masked share approaches the share of crop cells with any smoke on their line of sight, and under a random policy that ceiling is 0.028, 0.130 and 0.419 at Low, Medium and High, so at Medium it sits below the band's floor of 0.150<!-- N:DX-12 -->. Smoke decays fast and tracks the moving front, which leaves most crop cells transparent at any $\kappa_B$. The detection and toy bands are disjoint by a factor of 1.35 under a random policy and 1.15 under probe policies<!-- N:CB-2 -->: the same $\kappa_B$ attenuates the arena's extended smoke more strongly than the toy's single smoke source. $\kappa_B = 1.0$ was locked on the detection band alone<!-- N:CB-1 -->, inside it under the probe policies the lock governs; the masked-share band was retired, not widened, and the toy band was demoted to a consistency check. The detection band held again under the 500-update<!-- N:DX-40 --> policies of the grid below.

### 6.4 The cost is paid in survival, at High

Figure 7 shows where the masking falls (a) and the High survival contrasts in the order the record supports them (b).

{% include figure.html path="assets/img/submission/fig04_coupling_b.png" class="img-fluid" alt="Left, the masked share of the agent crop at three severities, over all alive agent-steps and at danger moments, on a log scale. Right, three replicate survival contrasts at high severity and then the first estimate, against a hatched band of one floor standard deviation." caption="Figure 7. Coupling B: where the masking falls, and the High survival contrasts." %}

<p class="caption">(a) For each severity, the masked share of an agent's crop in the κ<sub>B</sub> = 1.0 arm of the Coupling-B grid, over all alive agent-steps (open) and at danger moments, when a Burning cell is in the crop (filled), on a log scale, with the concentration ratios 118×, 22× and 16×<!-- N:CB-10 -->. (b) High survival, κ<sub>B</sub> 1.0 − 0: the three replicate contrasts first (the grid's seeds 0 and 1, then the same-seed retrain: −0.0687, −0.1066, −0.0470<!-- N:DX-13 -->), then, below the rule, the first estimate, the mean of seeds 0 and 1 (−0.0876<!-- N:CB-6 -->). The hatched band is ±1 sd of the High survival floor, 0.0621<!-- N:CB-7 -->, measured on four identical runs<!-- N:DX-40 --> of a separate artifact: a reference for this grid, not its own floor, and a two-run contrast's own floor would be wider. The figure cannot show intervals (each contrast is one run per cell), completion (unresolved), or Medium. <span class="figure-note">Status: reference scale (cross-artifact) for the band; trained policies, 500 updates<!-- N:DX-40 --> · Interact: none (static figure).</span></p>

At High (Figure 7(b)), three replicate contrasts of survival between $\kappa_B = 1.0$ and $\kappa_B = 0$ (trained policies, 500 updates, $d_p = 0.5$, Coupling A on<!-- N:DX-40 -->) share their sign: −6.87 and −10.66 points for the grid's two seeds and −4.70 points for a same-seed retrain<!-- N:DX-13 -->, a range of −4.7 to −10.7 points, negative 3 times out of 3<!-- N:CB-5 -->. Each is one run per cell, so none has an interval. The grid's first estimate, the mean of its two seeds, was −8.8 points<!-- N:CB-6 -->. The High survival floor, sd 6.21 points<!-- N:CB-7 -->, was measured afterwards on four identical runs<!-- N:DX-40 --> of a separate artifact; the first estimate is 1.41 times<!-- N:CB-5 --> that floor and the mean of the three replicates about 1.19 times<!-- N:CB-5 -->, both ratios against a reference scale (cross-artifact), not the grid's own floor. The direction replicates; the magnitude is modest. The first report had graded the effect "strong" against a two-seed spread, and that label was retracted when the floor was measured (§8.1). Completion is not resolved: its contrast flipped sign on the same-seed retrain<!-- N:CB-8 -->, and no completion effect is resolvable above the reproducibility floor.

At Medium, the severity of the held-out test configuration (β = 0.49<!-- N:CAL-3 -->), Coupling B's own survival effect was −0.03 points<!-- N:CB-9 -->. That figure was judged against a three-seed spread, $\sigma_{\mathrm{seed}} = 0.0072$<!-- N:CB-9 -->, not a measured floor; the Medium survival floor measured later is 0.0129<!-- N:METH-1 -->. Coupling B is live at High and quiet at Medium, where §9's test is run; §10 states what follows.

Where the masking falls explains why the cost appears in survival. Call an alive agent at a step when a Burning cell is inside its crop a danger moment. In the $\kappa_B = 1.0$ arm, the masked share of the crop at danger moments is 0.0809, 0.0560 and 0.2424 at Low, Medium and High, against 0.00068, 0.00249 and 0.01559 over all alive agent-steps<!-- N:DX-11 -->: masking is 118, 22 and 16 times more concentrated when a threat is in view<!-- N:CB-10 --> (Figure 7(a)). The unconditional share averages over agents that are mostly nowhere near fire, which is why it made a poor calibration band. Within the scope of trained policies at 500 updates<!-- N:DX-40 -->, the attenuation was not behaviourally suppressed: the masking ceiling of the states the coupled ($\kappa_B = 1.0$) policies visited, a quantity that does not depend on $\kappa_B$, sat at or above its random-policy value at every severity, and an apparent regulation of smoke exposure seen in shorter-trained probe policies survived neither longer training nor the $\kappa_B = 0$ control.

### 6.5 The co-active counter, and what it can see

From its first version the environment logs, at every step, the number of collapse-seeded ignitions inside an alive agent's crop, within Chebyshev radius 4<!-- N:DX-37 --> of its post-step position<!-- N:CO-4 -->. The counter is meant to catch both couplings at once, a collapse-seeded fire inside a view that smoke can attenuate. Only Coupling A produces those ignitions, however, and $\kappa_B$ does not enter the count, so the counter measures that coincidence only in configurations where Coupling B is also on: it is co-active only in all-on configurations. In a training mixture it reads the Coupling-A marginal alone, which is why the mediation analysis registered on it is void (§9.2).

Figure 8 shows the counter's distribution in the all-on cells.

{% include figure.html path="assets/img/submission/fig05_coactive.png" class="img-fluid" alt="Three bar charts, one per severity, of the share of episodes with zero, one, two, three, and four or more co-active events." caption="Figure 8. The co-active counter is rare and bursty: its distribution, not its mean." %}

<p class="caption">Share of episodes with 0, 1, 2, 3 and ≥ 4 co-active events, one panel per severity (β = 0.43 / 0.49 / 0.70<!-- N:CAL-3 -->), in the κ<sub>B</sub> = 1.0 arm of the Coupling-B grid, seeds pooled: P(0) = 0.563 / 0.578 / 0.883 over n = 1024 / 1536 / 1024 episodes<!-- N:CO-2 -->. The counter counts collapse-seeded ignitions inside an alive agent's crop; κ<sub>B</sub> does not enter it, so it is co-active only where Coupling B is also on, as in these all-on cells. The figure cannot show a floor (none exists for this artifact's counter), the over-dispersion, or training mixtures, in which the counter reads Coupling A alone. <span class="figure-note">Status: descriptive; trained policies, 500 updates<!-- N:DX-40 -->, single-configuration runs; no floor · Interact: none (static figure).</span></p>

In these all-on cells (single configurations, not mixtures) the counter is rare and bursty, which is why Figure 8 shows its distribution rather than its mean. The share of episodes with no co-active event is 0.563, 0.578 and 0.883 at Low, Medium and High<!-- N:CO-2 -->; the mean at Medium is 0.64 events per episode<!-- N:CO-1 -->, and the variance-to-mean ratio, 1.31–1.40<!-- N:CO-3 -->, exceeds the Poisson value of 1. The $\kappa_B = 0$ arm differs from it only by small amounts of inconsistent sign, none graded against a floor, as expected of a count that reads no smoke. The severity profile is the one §5's factors give: Low and Medium are indistinguishable and High is lower, because seeded ignitions fall while the near-agent share stays flat.

<!-- BUILDER-WRITTEN DEMONSTRATION (DEMONSTRATION DRAFT ruling, 2026-10-11); not the owner's text -->

## 7 Communication denial: inert under this encoder at this scale

The third stressor denies inter-agent links. Unlike the couplings it is independent of the fire by construction, and in CHE it had no measurable effect. This section states the kernel (§7.1), the theory of when communication should matter (§7.2), the measurements (§7.3), and how far the null reaches: communication denial is inert under a frozen random-projection message encoder at this scale, and no further. Figure 9 sets the toy, where communication matters by construction, beside the denial contrast in CHE.

{% include figure.html path="assets/img/submission/fig06_comms.png" class="img-fluid" alt="Top left, courier success rate against perception attenuation in the two-agent toy, for free and for denied communication, with the predicted curve. Top right, the denial contrasts at medium severity with their bars. Bottom, the per-run values behind those contrasts." caption="Figure 9. The value of communication in the toy, and the denial contrast in CHE at Medium." %}

<p class="caption">(a) The courier variant of the corridor toy, with scripted policies: the courier's success rate J with free communication, with communication denied under the no-idle schedule (±1 SE), and the prediction ½ + q/2, against κ<sub>B</sub>; the shaded gap is VoC<sub>gated</sub>, which rises from 0 to 0.498<!-- N:COM-1 -->. (b) CHE at Medium: Δ = (δ = 0) − (δ = 1) for completion (+0.0038) and survival (−0.0143)<!-- N:COM-4 -->, each against its bar, ±2 × the floor sd measured on that card (hatched): a post-hoc floor grading. (c, d) The runs behind (b): four seeds at δ = 0, four at δ = 1<!-- N:COM-4 -->, and the identical floor runs, with their means. The figure carries no word “inert”; (a) is the toy and (b–d) are CHE. It cannot show the content ablations, the High-severity runs, the VOID condition, or anything about a trained encoder. <span class="figure-note">Status: descriptive; (a) toy handshake, scripted policies; (b–d) trained policies at Medium, bars are post-hoc floor grading · Interact: none (static figure).</span></p>

### 7.1 The kernel

**Definition 7 (Communication denial, as implemented).** After the agents move, the comms kernel $T_K(k' \mid x')$ samples a directed link graph over the alive agents: for every ordered pair $i \ne j$ of alive agents,

$$
\Pr\big[\, i \to j \text{ open} \,\big] = \mathbf{1}\big[\lVert x'_i - x'_j \rVert_\infty \le R_{\mathrm{comm}}\big]\,(1 - \delta),
$$

with $R_{\mathrm{comm}} = 16$<!-- N:COM-6 --> cells. Each agent emits a message $m_i \in [-1, 1]^{8}$<!-- N:DX-17 --> at step $t$; at $t + 1$ each receiver $j$ gets the mean of the messages delivered over the links then realized, $\bar m_j = \sum_i k'_{ij}\, m_i \,/\, \max(1, \sum_i k'_{ij})$, which is the zero vector when $j$ is isolated. $T_K$ reads positions and aliveness only, with no hazard, smoke or structure input, so denial is mechanistically independent of the fire; hazard-coupled communication is future work. One uniform per ordered pair is drawn at every step whatever $\delta$ is, so $\delta = 0$ gives the deterministic range graph and $\delta = 1$, the locked value<!-- N:COM-6 -->, gives the empty graph, both bitwise. The theory's range-dependent link probability is implemented as this hard Chebyshev range<!-- N:DX-17 -->.

The message head is a tanh-bounded dense layer on the policy's shared trunk. Listing 6 shows the line that makes the channel non-differentiable.

**Listing 6.** Delivered messages carry no gradient.

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

The delivered aggregate is stored in the training batch and the loss recomputes the policy from the stored array; `stop_gradient` states the same thing in code. No gradient crosses the channel, so the message head receives none for the whole run and stays at its initialization<!-- N:ENV-12 -->: what an agent emits is a frozen random projection of trunk features that are themselves trained. The receivers' weights on the message inputs are trained, so whether agents use messages can be tested; what to say was never learned.

### 7.2 When communication should matter

That observability governs the value of communication is not new. Pynadath & Tambe (2002) <d-cite key="pynadath2002"></d-cite> relate the complexity of team decision problems with communication to observability: free communication lowers the complexity when the world is collectively observable (their Theorem 4 and Table 2), and makes no difference when it is individually observable or not observable at all (their Theorems 5–6). Remark 2′ refines this for collective partial observability, in a two-agent extension of the corridor toy of Theorem 1.

**Remark 2′.** Extend $E_{2C}$ with a second agent. (i) Under a team-any reward, communication has zero marginal value when the agents are interchangeable, expendable (no death cost) and at least as numerous as the hypotheses: coverage then achieves $J = 1$ under total denial. When any qualifier fails, value returns; in general it scales with the deficit of agents relative to hypotheses, and a death cost, such as CHE's $d_p = 0.5$<!-- N:ENV-1 -->, prices the redundancy that substitution spends. (ii) In the courier variant, where only agent 1 can complete the task and it observes the other agent only through messages, the denied optimum within the no-idle policy class is $\tfrac12 + \tfrac12 q(\kappa_B)$; with slack $\ell_f$, optimal denied play buys information by idling at the branch and achieves $\tfrac12 + \tfrac12 \tilde q(\kappa_B)$, where $\tilde q$ is the probability of being informed by the commitment point under the best idling schedule, with $\tilde q \ge q$ (equality iff $\ell_f = 0$), so

$$
\mathrm{VoC}_{\mathrm{true}}(\kappa_B) = \tfrac12\big(1 - \tilde q(\kappa_B)\big) \le \tfrac12\big(1 - q(\kappa_B)\big).
$$

Both $q$ and $\tilde q$ decrease in $\kappa_B$, so the value of communication increases with perception decay. The lesson is conditional: communication carries value when perception fails and redundancy is unavailable. Irreplaceable roles, not blindness alone, make it valuable.

We ran the courier variant (M5.2) with scripted policies, delivering messages through the production link kernel and computing $\tau$ with the shared transmittance function, so the toy also tests both kernels. With 4096 episodes and 8192 Monte Carlo draws per point<!-- N:DX-15 -->, the free arm succeeds with probability 1.0000<!-- N:DX-15 --> at every $\kappa_B$, and the no-idle denied arm matches $\tfrac12 + \tfrac12 q$ (largest $\lvert z \rvert$ 0.44, $\chi^2 = 0.51$ on 8 degrees of freedom<!-- N:DX-15 -->; a fit that good was checked against replicate runs, which showed the standard errors sound, before it was accepted). The value of communication against that arm, $\mathrm{VoC}_{\mathrm{gated}} = \tfrac12(1 - q)$, therefore rises monotonically from 0 to 0.498<!-- N:COM-1 --> (Figure 9(a)). The idling correction bites where $q$ is near 1: $\tilde q / q$ is 1.126 at the locked $\kappa_B = 1.0$, peaks at 1.235 near $\kappa_B = 2$ and returns towards 1 at both ends, and the correction removes 79 %, 54 % and 7 % of $\mathrm{VoC}_{\mathrm{gated}}$ at $\kappa_B$ = 0.5, 1.0 and 3.0<!-- N:DX-15 -->. The toy's courier is irreplaceable by construction; CHE's agents are not.

### 7.3 In CHE the channel carries nothing measurable

CHE's agents meet one of Remark 2′(i)'s qualifiers: they are twelve<!-- N:ENV-6 --> interchangeable agents sharing one set of parameters<!-- N:ENV-11 -->. Their deaths are priced, so they are not strictly expendable, and nothing establishes that they are at least as numerous as the hypotheses. Three measurements test whether they use the channel.

First (M5.3: Medium, $\delta = 0$, $R_{\mathrm{comm}} = 8$, two seeds<!-- N:COM-2 -->, 500 updates<!-- N:DX-305 -->), three arms with identical architecture differ only in message content: live; zeroed, where the delivered aggregate is set to zero but the link graph is kept; and shuffled, where sender identities are permuted within a step. No pair differs beyond a bar of twice the earlier Medium floor, about 3 points<!-- N:COM-2 -->: a post-hoc floor grading, which a true effect equal to the bar would clear only about half the time (§8.2). Second (M5.3b: High, three seeds, $R_{\mathrm{comm}}$ = 8 and 16<!-- N:DX-16 -->), the same arms at two ranges: tripling the mean alive out-degree from 1.01 to 2.99<!-- N:COM-3 --> changed nothing, which rules out "nobody was in range" as the explanation, although at High the wider floor sets the bar at about 11 points<!-- N:DX-16 -->.

Third (M5.5: Medium, four seeds, $R_{\mathrm{comm}} = 16$<!-- N:COM-4 -->, message path live in both arms), the denial element itself. With $\delta = 0$ against $\delta = 1$, completion differs by +0.38 points against a bar of 7.99 points, and survival by −1.43 points against a bar of 2.60 points<!-- N:COM-4 -->; both bars are twice the floor sd measured on the same card, a post-hoc floor grading (Figure 9(b–d)). The channel is therefore inert at the resolution these measurements have, bars of about 8 points on completion and 2.6 points on survival<!-- N:COM-4 -->; a true effect of either size would clear its bar only about half the time (§8.2), and this is not a point null. A third condition, no cross-arm difference in danger-moment outcomes, is VOID, not failed: the threshold chosen at implementation to grade it, 20 % on fire deaths per danger agent-step, sat below that quantity's own 27.2 % run-to-run nondeterminism, and the observed 23.2 %<!-- N:COM-5 --> lies between the two (§8.1).

The null rests on two halves, each weaker alone. The first is a mechanism. In the live arm a receiver can tell that it heard from someone without decoding anything; in the zeroed arm it cannot. That signal needs no encoder, and it went unused at both severities, and at High at both ranges, so the channel's neglect is on the demand side (the agents did not need the information) rather than the channel side (they could not read it), and the frozen encoder cannot account for it. The second half is M5.5: removing the channel entirely changes nothing measurable.

Two qualifications bound the claim. Deaths are priced ($d_p = 0.5$<!-- N:ENV-1 -->), so the agents are not strictly expendable and Remark 2′(i)'s clean-zero conditions are not fully met; the measured null therefore also says that the value which returns when a qualifier fails is weak at this scale and this death price. And the message head receives no gradient, so the encoder is a frozen random projection and gradient-shaped messaging is untested: a bound measured on a frozen encoder does not strictly bound a trained one. We claim only that communication denial is inert under a frozen random-projection encoder at this scale.

Three consequences carry into §9. The composition under test there is, in effect, Coupling A × Coupling B. The held-out configuration $\theta^*$ keeps $\delta = 1.0$<!-- N:COM-6 --> for fidelity to the registration, at no cost. And the third of ISO's training episodes that carry only $\delta$<!-- N:DES-8 --> carry, behaviourally, no active stressor: they are fire-only episodes, the source of the inert-share bias that §9 registers and corrects.

<!-- BUILDER-WRITTEN DEMONSTRATION (DEMONSTRATION DRAFT ruling, 2026-10-11); not the owner's text -->

## 8 Methodology: bars come with floors

GPU training is not reproducible run to run: XLA chooses kernels by timing them and some reductions use atomics, so two runs with the same seed, configuration and code can differ. A reproducibility floor is the standard deviation of a metric over such identical runs, the noise any acceptance bar on that metric must clear. This section states the measurement rules the project adopted, each with the defect in its own record that produced it, and ends with where this paper falls short of them (§8.6). Figure 10 steps through the floor exhibits; each tab prints its confound.

<figure class="l-page">
  <iframe src="{{ 'assets/html/submission/floors_explorer.html' | relative_url }}" width="100%" height="460" style="border:none" title="Floors explorer: reproducibility floors per card, per artifact, per run length, and the grid against its floor" loading="lazy"></iframe>
  <figcaption><strong>Figure 10.</strong> Reproducibility floors, one exhibit per tab. <em>Per card (and tree, and config):</em> the Medium floor on two runs, completion 0.0145 against 0.0399 (2.75×) while survival stays at 0.0129 against 0.0130<!-- N:METH-1 -->; card, code tree and configuration all differ between the two runs. <em>Per artifact:</em> GPU rerun comparisons during a refactor, one square per comparison: the reference tree against itself, 0 of 760 field digests differing in 4 of 4 comparisons; the refactored tree against itself, 1 of 4 differing, on two diagnostic channels<!-- N:METH-2 -->; and the cross-tree comparisons. <em>Per run length:</em> completion of identical runs at 500 and 1000 updates, floor growth 2.1× for ISO and 5.2× for JOINT<!-- N:METH-5 -->; run length and box both differ. <em>The grid against its floor:</em> each confirmatory arm's seed standard deviation over its floor (k = 72 per arm<!-- N:DES-13 -->), and survival Γ at 5.40× its floor-basis sd(Γ)<!-- N:HW-1 -->. The figure cannot show each floor's own uncertainty, the contrasts in this paper that have no floor (§8.6), or the drift channels, which have none. <span class="figure-note">Status: floors are point standard deviations over identical runs, roughly ±40 % uncertain when measured on four identical runs<!-- N:DX-303 --> · Interact: click a tab or press ← / →; hover or tab to a mark for its value.</span></figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/floors_explorer.png" class="img-fluid" alt="Reproducibility floors on two cards, rerun comparisons of two code trees, floor growth from the shorter to the longer run length, and the confirmatory grid's seed dispersion against its floor, each with its confound stated." caption="Static companion of Figure 10 for the printed PDF." %}
</div>

### 8.1 A bar without a floor is void

**No acceptance bar without a measured floor for the quantity it grades, or an explicit UNDERPOWERED flag.** A bar below its instrument's noise cannot pass under the null, so it is not a test: its output is void, not failed, and a void test voids a PASS exactly as it voids a FAIL. Four bars in the record produced the rule. M4.4 graded its High survival effect against $\sigma_{\mathrm{seed}} = 0.0295$<!-- N:DX-38 -->, the spread of two seed means, where the High floor measured later is 0.0621<!-- N:CB-7 -->; its "strong" grade was retracted (§6.4). M5.3 graded its content ablation against a Medium floor hard-coded from an earlier run. M5.3b measured its High floor first, on its own card, and found that matching Medium's resolution at High would take roughly 46 seeds per arm<!-- N:DX-302 -->. M5.5's third condition, specified as no cross-arm difference in danger-moment outcomes, was graded with a 20 % threshold chosen at implementation, not registered, on a quantity whose run-to-run nondeterminism measures 27.2 %; the observed 23.2 %<!-- N:COM-5 --> exceeds the threshold and falls short of the noise, so the condition is VOID. The floor data predate the comparison, and had the difference exceeded the floor, the verdict as produced, NOT INERT, would have stood.

**Floors are facts per metric and per hardware.** Re-measuring the Medium floor moved the completion floor 2.75-fold, from 0.0145 to 0.0399, and left survival at 0.0129 against 0.0130<!-- N:METH-1 -->. The two runs differ in card (RTX 5090 against RTX PRO 6000<!-- N:DX-403 -->), code tree and configuration, so the exhibit shows that a floor can move for one metric and not another, not which factor moved it. Neither "it will be the same" nor "it will differ" is safe; the floor is measured on the card that runs the grid.

**Floors are facts per artifact.** In the refactor that made the environment configuration a per-episode traced input (M6.0), the GPU rerun floor was measured first on the reference tree and read zero: 0 of 760 field digests differed, in 4 of 4 comparisons<!-- N:METH-2 -->. Against it, two diagnostic channels that differed between the refactored and the reference tree looked like a semantic change, but the refactored tree differed from itself 1 time in 4, on the same two channels<!-- N:METH-2 -->, and no trajectory field differed in any comparison. The floor had been measured on the more deterministic artifact. An equivalence claim between A and B needs A against A and B against B, not only A against B: two deterministic artifacts cannot compare intermittently.

### 8.2 Contrasts and power

**A contrast is graded on the contrast's standard error.** For $\Gamma = \overline{\mathrm{JOINT}} - \overline{\mathrm{ISO}}$ over $k$ seeds per arm,

$$
\operatorname{sd}(\Gamma) = \sqrt{\frac{\sigma_{\mathrm{ISO}}^2 + \sigma_{\mathrm{JOINT}}^2}{k}},
$$

never either arm's own $\sigma\sqrt{2/k}$. The per-arm forms bracket the truth without equalling it: at $k = 34$<!-- N:METH-3 --> on the M6.2b floors, ISO's form gave 92.1 % power and JOINT's 62.8 %, where the contrast's power was 76.7 %<!-- N:METH-3 -->. The project had adopted per-artifact floors because the arms differ in stability, then kept a power formula that assumed they do not.

**A design-stage power statement is the 80 %-power minimum detectable effect at the family-corrected level**<!-- N:METH-7 -->,

$$
\mathrm{MDE}_{80} = \big(z_\alpha + z_{0.8}\big)\,\operatorname{sd}(\Gamma),
$$

with $z_\alpha$ the family-corrected critical value (Šidák over the two co-primaries, $z_\alpha = 2.2365$<!-- N:DES-13 -->); with equal variances, $\operatorname{sd}(\Gamma) = \sigma\sqrt{2/k}$. The exclusion bound $X$ that §9 attaches to a null has the same form, on the grid's realized seed dispersion. A bare $2\sigma\sqrt{2/k}$ is the effect at which a test would just reject, 50 % power. Phase-6 seeds were first ruled at $k = 20$<!-- N:METH-4 --> on such a figure, which also omitted the Šidák correction; corrected, completion had 55.6 % power against its own motivating effect band<!-- N:METH-4 -->, caught while the registration was drafted, before any run. The 2σ form survives only for post-hoc floor grading of an observed effect, labelled as such, as in Figure 9(b).

### 8.3 Floors move with the run, and gates must not divide by them

**Floors grow with run length.** From 500 to 1000 updates the completion floor grew from 0.0165 to 0.0339 for ISO and from 0.0093 to 0.0483 for JOINT<!-- N:DX-34 -->, 2.1-fold and 5.2-fold<!-- N:METH-5 -->; the two lengths ran on different RTX PRO 6000 boxes, so length is confounded with box. The ordering inverted, JOINT being the tighter arm at 500 updates and the looser at 1000, and the ruling that ordered the measurement had said not to presume its outcome. A floor measured at one budget does not grade runs at another. That the growth follows each arm's curriculum difficulty is a hypothesis we did not test (two arms).

**A gate that divides by a floor diverges on better hardware.** The registered plateau guard divided the drift over the last 100 updates<!-- N:DES-10 --> by the floor sd. On a second card JOINT's residual drift fell while its floor shrank by more, and the guard fired; as the floor goes to zero any nonzero drift fails, so on a perfect instrument nothing passes. The $T^*$ ruling of 2026-08-11<!-- N:METH-6 --> retired the guard as a pass/fail gate, kept it as a reported statistic, fixed the estimand as Γ at matched compute, and made Γ(t) required robustness evidence (§9): it narrowed the claim and added a test the result could fail.

### 8.4 The floor is a hurdle, not the test variance

**The floor and the test statistic are different variances.** A floor comes from identical runs at one seed; a $k$-seed arm mean varies by seed and by nondeterminism. The confirmatory contrast is therefore graded on the grid's own seed dispersion, and the floor serves a separate hurdle: does the effect beat reproducibility? On the confirmatory grid each arm's seed standard deviation is 1.12 and 1.09 times its floor for completion and 1.25 and 1.19 times for survival (ISO, JOINT)<!-- N:HW-1 -->; survival Γ is 5.40 times<!-- N:HW-1 --> its floor-basis sd(Γ) of 0.00177<!-- N:DX-21 -->, and completion Γ is 1.78 times its 0.00970 in magnitude<!-- N:DX-21 -->. Used for design-stage power, the floor gives an upper bound on the power the grid will have, labelled as one.

### 8.5 Instruments state what they are blind to

**A differenced test sees asymmetry and nothing else.** A condition of the form "no cross-arm difference in X" cancels any X present in both arms. In 24 of 24 rendered episodes of the Coupling-B grid the alive agents drifted towards a wall, their centroid moving down from row 32.3 to 49.2 against an arena centre of 31.5, in a direction set by the training run<!-- N:DX-32 -->; these are rendered-pixel centroids, a diagnostic and not a state measurement. The inertness falsifier for Coupling B, logged before its data, included the condition "no cross-arm exposure/positioning difference", which passed with the drift present in both arms. It could never have seen the drift, and nothing said so for several phases. The verdict it fed does not move, but its silence was evidence about asymmetry only.

**Measuring is not grading.** A channel in the environment's info, the evaluation archive or the training log is recorded; it becomes evidence only inside a registered analysis family, with a floor measured on its artifact. The Phase-6 grid records drift channels for every run at no cost. They are recorded, not graded: no floor exists for them, and they were kept out of the registered family, because a diagnostic added after registration enlarges the family and inflates its correction.

**Every reading of a registered bias is reported.** Bias (b), differential drift, was estimated before unblinding, in three floor studies, as the JOINT − ISO completion drift over the last 100 updates: +0.01209 on the launch batch and +0.0179 on a later re-floor, both on RTX PRO 6000 cards, and −0.0083 on the RTX 5090 that ran the grid<!-- N:DES-10 -->. Its sign reversed on the grid card; we report every reading and claim no direction (§9.1).

### 8.6 Where this paper falls short of its own rules

Not every number in this paper is graded against a floor on its own artifact. Coupling B's Medium survival effect, −0.03 points<!-- N:CB-9 -->, was judged against a three-seed spread, $\sigma_{\mathrm{seed}} = 0.0072$<!-- N:CB-9 -->, not a floor. The trained-policy contrasts of §5 and §6 come from the m44 and m35 grids, which have no identical-run sets; their spreads are seed ranges, and every floor beside them is a reference scale (cross-artifact). In §9.2's secondary design, floors exist only for the sweep's $p = 0.5$<!-- N:DX-28 --> arm; the intermediate points assume that floor and the identification arm is ungraded<!-- N:DX-306 -->. ISO-4 has no identical-run set, so Γ₄ and $\hat B$ (§9.1) are graded on seed dispersion with no beat-reproducibility hurdle, and ISO-4's High-readout numbers carry an UNDERPOWERED flag for that hurdle. The drift channels have no floor at all. And every floor is itself a point estimate: measured on four identical runs, an sd is uncertain by roughly ±40 %<!-- N:DX-303 -->.

<!-- BUILDER-WRITTEN DEMONSTRATION (DEMONSTRATION DRAFT ruling, 2026-10-11); not the owner's text -->

## 9 The pre-registered compositional test

This section states the test as registered and reports it in the registered order: the confirmatory verdict, the correction, the budget-robustness reading, then the analyses that carry no verdict. Every reading rule was fixed before unblinding; Appendix D quotes each verbatim with its date, and Appendix E gives the outcome branches.

### 9.1 Design

**Definition 8 (Training protocols and the compositional gap).** Let $J_\theta(\pi)$ be the expected episodic return of joint policy $\pi$ in $\mathcal{M}_\theta$, and let $\theta^*$ be the test configuration, every stressor on at a severity held out of training. Let $\Theta_{\mathrm{iso}}$ be the configurations in which at most one of $\kappa_A$, $\kappa_B$, $\delta$ is nonzero; the fire ($\beta > 0$) burns in all of them. The ISO protocol trains one policy $\pi_{\mathrm{iso}}$ on a uniform mixture of configurations in $\Theta_{\mathrm{iso}}$; the JOINT protocol trains one policy $\pi_{\mathrm{joint}}$ on a mixture whose support includes configurations with every stressor on, at training severities only. The compositional gap is

$$
\Gamma(\theta^*) = J_{\theta^*}(\pi_{\mathrm{joint}}) - J_{\theta^*}(\pi_{\mathrm{iso}}).
$$

The registered test reads the same contrast with $J$ replaced by the mean of an outcome metric over evaluation episodes, on two co-primaries: task completion, the founding primary, on which the founding hypothesis was $\Gamma(\theta^*) > 0$, and survival rate (§3). Survival was made a co-primary on 2026-08-02<!-- N:DES-12 -->, before the grid, because, as the registration records, the earlier coupling grids had shown the couplings moving survival while their completion effects sat at or below the reproducibility floor (§6).

**Proposition 4 (An irreducible shift term for ISO).** For any policy $\pi$ and configurations $\theta, \theta'$ sharing reward $R$ with $\lvert R\rvert \le R_{\max}$, and with $J$ read as the $\gamma$-discounted return (the form the theory uses for its statements; the implementation is episodic),

$$
\big\lvert J_{\theta}(\pi) - J_{\theta'}(\pi)\big\rvert \le \frac{\gamma R_{\max}}{(1-\gamma)^2}\,\varepsilon(\theta,\theta'), \qquad \varepsilon(\theta,\theta') = \sup_{s,a}\Big[\big\lVert T_\theta(\cdot\mid s,a) - T_{\theta'}(\cdot\mid s,a)\big\rVert_1 + \max_i \big\lVert O^i_\theta(\cdot\mid s) - O^i_{\theta'}(\cdot\mid s)\big\rVert_1\Big].
$$

For every $\theta \in \Theta_{\mathrm{iso}}$ the kernels differ from those of $\theta^*$ on every state where both couplings act at once (a collapse-seeded fire within perception-attenuation range of an agent), so $\varepsilon(\theta,\theta^*) \ge \varepsilon_{\min} > 0$ uniformly over $\Theta_{\mathrm{iso}}$: ISO's transfer guarantee carries an irreducible slack proportional to $\varepsilon_{\min}$, whereas JOINT trains at $\varepsilon = 0$ on the stressor combination, with slack only in the held-out severity direction (proof in Appendix A). Proposition 4 bounds what ISO can be *guaranteed* to transfer, not what happens: it does not lower-bound the realized $\Gamma$, it concerns return rather than the co-primaries, and compositional generalization can emerge from isolated training. It motivates the experiment; the experiment decides. The counter built to measure visits to that region (§6) is co-active only in all-on configurations, so the theory's prediction about ISO's exposure to the region was not tested (mediation, §9.2).

**The arms.** Figure 2 (§1) shows what each arm trained on. Every arm trains uniformly at β = 0.43 (subcritical) and β = 0.70 (supercritical)<!-- N:CAL-3 -->; none trains at β = 0.49<!-- N:CAL-3 -->, the held-out severity of θ\*, and a test fails if any training configuration carries it. θ\* is every stressor on at β 0.49, $\kappa_A$ 0.06, $\kappa_B$ 1.0, δ 1.0<!-- N:CAL-3 --><!-- N:CA-1 --><!-- N:CB-1 --><!-- N:COM-6 -->.

| arm | training components | weight each | per-coupling marginal | co-occurrence | active share (behavioural) |
|---|---|---|---|---|---|
| ISO | {A-only, B-only, δ-only} × {0.43, 0.70}<!-- N:CAL-3 --> | 1/6<!-- N:DES-16 --> | 1/3<!-- N:DES-7 --> | 0<!-- N:DES-7 --> | 2/3<!-- N:DES-14 --> |
| ISO-4 | {A-only, B-only} × {0.43, 0.70}<!-- N:CAL-3 --> | 1/4<!-- N:DES-16 --> | 1/2<!-- N:DES-14 --> | 0<!-- N:DES-14 --> | 1<!-- N:DES-14 --> |
| JOINT | {all-on} × {0.43, 0.70}<!-- N:CAL-3 --> | 1/2<!-- N:DES-16 --> | 1<!-- N:DES-7 --> | 1<!-- N:DES-7 --> | 1<!-- N:DES-14 --> |

ISO-4, adopted on 2026-09-18<!-- N:DES-15 --> as a sensitivity arm outside the confirmatory family, is ISO with its two δ-only components removed and nothing else changed. All arms share the network, the IPPO hyperparameters (Appendix B<!-- N:DX-2 -->), one shared-parameter policy per training seed<!-- N:ENV-11 --><d-cite key="dewitt2020ippo"></d-cite>, the budget of T\* = 1000<!-- N:DES-13 --> updates of 32,768 environment steps, 32,768,000 per run<!-- N:DX-3 -->, and one evaluation draw, eval seed 0 × 512 episodes at θ\*<!-- N:DES-13 -->.

**Estimand and test.** Γ is read at matched compute, at the fixed budget T\*, never at convergence (T\* ruling, 2026-08-11<!-- N:METH-6 -->). For each co-primary, with $\bar y$ the arm mean and $s$ the arm's own seed standard deviation,

$$
\hat\Gamma = \bar y_{\mathrm{joint}} - \bar y_{\mathrm{iso}}, \qquad \widehat{\mathrm{sd}}(\hat\Gamma) = \sqrt{\frac{s_{\mathrm{iso}}^2}{k_{\mathrm{iso}}} + \frac{s_{\mathrm{joint}}^2}{k_{\mathrm{joint}}}}, \qquad z = \frac{\hat\Gamma}{\widehat{\mathrm{sd}}(\hat\Gamma)} .
$$

The family is the two co-primaries, Šidák-corrected (m = 2<!-- N:DES-13 -->): a contrast rejects when $\lvert z\rvert > z_\alpha = 2.2365$<!-- N:DES-13 -->, the two-sided normal critical value at per-comparison level $1-(1-0.05)^{1/2}$, with Šidák-corrected 95 %<!-- N:DES-13 --> CI $\hat\Gamma \pm z_\alpha\,\widehat{\mathrm{sd}}(\hat\Gamma)$. A null carries the exclusion bound $X = (z_\alpha + z_{0.8})\,\widehat{\mathrm{sd}}(\hat\Gamma)$, the 80 %-power MDE at the family-corrected α (the $\mathrm{MDE}_{80}$ of §8)<!-- N:METH-7 -->. The test is unpaired (arms share seed integers, which puts any induced covariance on the safe side) and graded on the grid's own seed dispersion in the contrast form (§8); floors serve only as the beat-reproducibility hurdle and as an upper-bound power basis. The t critical value at 142 degrees of freedom, 2.2604<!-- N:DX-404 -->, is printed and not applied. Every interval is conditional on the common evaluation draw and carries training-seed variance only.

**Seeds, and how k reached 72.** The design registered k = 40<!-- N:DES-1 --> seeds per confirmatory arm and a re-floor ladder capped at 60<!-- N:DES-1 -->: floors re-measured on the grid's card set the smallest k with 80 %<!-- N:DX-402 --> power at the 0.03<!-- N:DES-4 --> target effect, up to the cap, beyond which the grid would run at the cap with completion flagged UNDERPOWERED. The re-floor run on 2026-09-08 (logged 2026-09-09) on an RTX PRO 6000 set k = 46<!-- N:DES-2 -->; the grid then moved to RTX 5090 units<!-- N:DX-5 -->, whose re-floor returned $k_{\mathrm{req}}$ = 72 for completion and 3 for survival, and on 2026-09-22 the cap was raised to 72<!-- N:DES-3 -->. This is a deviation from a registered rule, recorded as one, made before unblinding with no outcome seen, and conservative: the cap was a cost cap, $k_{\mathrm{req}}$ comes from floors at seed 0, which the grid never uses, and added seeds raise power without favouring either sign of Γ. Seeds 1–60<!-- N:DES-1 --> are a prefix of 1–72<!-- N:DES-3 -->, so the registered k = 60 analysis is reported beside the primary k = 72, designated before the look.

**Design-stage power, as an upper bound.** Floors come from identical runs at one seed and seed dispersion only adds to them, so floor-based power is a ceiling, registered as one. The launch-batch floors (RTX PRO 6000, 2026-08-10) gave, at k = 40, MDE80 1.55 / 0.95 points on completion / survival<!-- N:DES-5 -->; the grid card's floors gave completion power at 0.03 of 72.2 % at k = 60 and 80.4 % at k = 72<!-- N:DES-4 -->. Realized completion power on the grid's own dispersion is 71.6 % at k = 72 and 60.2 % at k = 60<!-- N:DES-6 -->: reported, not re-engineered.

**The endpoint confound, and the matched instrument.** JOINT sees each coupling three times as often as ISO<!-- N:DES-7 -->, so Γ mixes dose with composition. A secondary design holds dose fixed: its sweep keeps each coupling's marginal at $\mu = 0.5$ while the co-occurrence share $p$ moves over {0, 0.125, 0.25, 0.375, 0.5}<!-- N:DX-28 -->, a split in the spirit of the DBCA method of Keysers et al. (2020)<d-cite key="keysers2020"></d-cite>; the ISO and JOINT endpoints, whose atom frequencies differ threefold, do not follow DBCA. Nor is the sweep clean: on the training simplex $\mu = (1 + p - \nu)/2$, with $\nu$ the fire-only share, so a fixed $\mu$ forces $\nu = p$<!-- N:DES-9 -->, and marginal, co-occurrence and active share cannot all be held at once. Identification arms ($\mu = 0.4$, $\nu = 0.2 + p$<!-- N:DES-9 -->) lie on a parallel line offset by 0.2 in fire-only share, which identifies the plane $y = \gamma_0 + \gamma_p p + \gamma_n \nu$ (the registration had called the lines non-parallel; the specification ratified before the sweep was read corrects that). Secondary arms run k = 20<!-- N:DES-13 --> seeds with δ off, so `sweep_c50_p000` trains on exactly ISO-4's mixture; JOINT also differs from every secondary arm in carrying δ = 1.0<!-- N:COM-6 -->, inert under this encoder at this scale (§7). All of it is **non-verdict-bearing**.

**Registered biases, stated before the result.** (a) *Inert share.* Two of ISO's six components are δ-only<!-- N:DES-8 -->, and δ is inert under a frozen random-projection message encoder at this scale (§7), so those episodes are fire-only: no behaviourally active stressor, the fire burning at β 0.43 or 0.70<!-- N:CAL-3 --> as in every episode. ISO's configured no-element share of 0 is true nominally and false behaviourally<!-- N:DES-16 -->; its active share is 2/3 against JOINT's 1<!-- N:DES-14 -->, a 1.5-fold<!-- N:DX-31 --> difference. Registered on 2026-09-18<!-- N:DES-15 --> with its direction, the bias inflates Γ; ISO-4 removes it, and its reading rule was registered and ISO-4 trained before the look. The composition under test is therefore A × B; δ is carried in θ\* for registration fidelity. (b) *Differential drift.* JOINT − ISO completion drift over the last 100 updates, a local sensitivity estimate and never a bound, read +0.01209 per 100 updates on the launch batch and +0.0179 on the 2026-09-08 re-floor (both RTX PRO 6000) but −0.0083 on the grid card<!-- N:DES-10 -->; the T = 2000 subsample's differential training-log slope over updates 500–1000 is +0.00247 (completion) and +0.00718 (survival) per 100 updates<!-- N:DES-11 -->. The sign reverses on the grid card; no direction is claimed.

**The registered readings.** Three rules decide what the confirmatory results may say (verbatim in Appendix D):

| reading | status | rule |
|---|---|---|
| branch, with the falsifier | confirmatory family; registered 2026-08-13<!-- N:DES-12 --> | rejection at $z_\alpha$ on each co-primary fixes the branch ($A_c$ added 2026-09-26<!-- N:DX-405 -->); branch B is claimable only if $\lvert z_c\rvert + z_\alpha < \lvert z_s\rvert$ |
| inert-share correction, Γ₄ = JOINT − ISO-4 and B̂ = ISO-4 − ISO | sensitivity arm, outside the family, k = 20<!-- N:DES-13 -->; registered 2026-09-18<!-- N:DES-15 --> | "If Γ rejects on a co-primary and Γ₄'s CI on that co-primary includes 0 or its sign is opposite, the paper states that the effect does not survive the inert-share correction"; "If Γ is null and Γ₄ is null, Γ₄ is quoted as a second exclusion bound"; no magnitude threshold on B̂ |
| budget robustness, Γ(t) at 11 checkpoints, updates 500–1000 every 50<!-- N:DES-13 --> | required robustness evidence | budget-robust iff all 11 point estimates share one sign; otherwise "sign unstable over the final half" |

The rest carry no verdict on Γ: the same-card replicate Γ₄′ (a secondary analysis, S5, proposed after Γ₄ was seen and read at $z_\alpha$ beside it); the eval-only High readout, whose null is an a-fortiori exclusion; the T = 2000 subsample, 4 seeds per arm<!-- N:RES-15 -->, descriptive and UNDERPOWERED; and the non-verdict-bearing secondary design.

**Blinding, as a property of the tooling.** The branches, their framings and the falsifier were registered on 2026-08-13<!-- N:DES-12 -->, before the grid ran (2026-09-09 to 2026-09-22<!-- N:DES-12 -->). The grid runner computes no cross-arm quantity, and tests in `che/tests/test_p6_grid.py` assert it, along with the exclusion of seed 0, the floor seed<!-- N:DX-416 -->, and shared seed integers across arms; floor reports print dispersions only. ISO-4 and its rule were adopted mid-grid, with 120 of 252<!-- N:DES-15 --> runs done, on a recorded attestation that no Phase-6 outcome mean had been computed or viewed. The pre-unblind rulings of 2026-09-26<!-- N:DX-405 --> fixed the statistic, the Γ(t) sign rule, k = 72<!-- N:DES-3 --> as primary and the $A_c$ cell. The unblinding instrument refuses an unflagged artifact or a modified tree, later instruments refuse to run before its log exists, and each log records a single run of its stage<!-- N:DX-411 -->.

### 9.2 Results

Figure 11 is the full ladder of registered readings (Figure 3 in §1 showed its first two rungs). Each rung's verdict sits before its numbers.

<figure class="l-page">
  <iframe src="{{ 'assets/html/submission/ladder_registered_readings.html' | relative_url }}" width="100%" height="1000" style="border:none" title="Registered readings ladder: Gamma, Gamma4, Gamma4 prime and B-hat on both co-primaries" loading="lazy"></iframe>
  <figcaption><strong>Figure 11.</strong> The registered readings at θ&#42;, both co-primaries, one rung per contrast in registered order: Γ = JOINT − ISO (with its k = 60<!-- N:DES-1 --> prefix as an optional row); Γ₄ = JOINT − ISO-4, whose survival rung carries the registered consequence <strong>does not survive the inert-share correction</strong> and whose completion rung carries <strong>second exclusion bound</strong>; Γ₄′ = JOINT − <code>sweep_c50_p000</code>, the same-card replicate; and B̂ = ISO-4 − ISO, with no verdict chip. Each row gives its verdict chip, then the estimate and Šidák-corrected 95 % interval, k per arm, the RTX 5090 unit(s)<!-- N:DX-5 --> and the registration date where the record gives one; k = 72<!-- N:DES-3 --> is a recorded deviation from the registered cap of 60<!-- N:DES-1 -->. The grey band is the 80 %-power MDE (confirmatory family and Γ₄ completion only); the stipple is ±1 floor-basis sd(Γ), on Γ only, because only Γ's two arms have a rep set. The figure cannot show effects present in both arms, which cancel in every contrast; eval-set sampling (every interval is conditional on one 512-episode<!-- N:DES-13 --> draw); any budget other than T&#42; = 1000<!-- N:DES-13 -->; or whether ISO-4's rise comes from its active share or its per-coupling frequency. It states no sum: Γ = Γ₄ + B̂ holds for arm means by construction. <span class="figure-note">Status: registered (Šidák-corrected 95 %, k = 72<!-- N:DES-3 -->) for Γ; sensitivity arm, outside the confirmatory family, for Γ₄; secondary (S5), non-verdict-bearing, read at z<sub>α</sub>, for Γ₄′; B̂ is a registered estimand (2026-09-18<!-- N:DES-15 -->), reported with its CI and no test · Interact: step the rungs with ◀ ▶ or the arrow keys, or press “show all”; toggle the MDE band, the floor stipple and the k = 60 prefix row (UNDERPOWERED); “table view” lists every value.</span></figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/ladder_registered_readings.png" class="img-fluid" alt="Two forest plots, completion and survival, of the registered contrasts in order with their Šidák-corrected intervals and verdicts" caption="Static companion of Figure 11 for the printed PDF." %}
</div>

All contrasts at θ\*, T\* = 1000<!-- N:DES-13 -->, in points (rate × 100), with Šidák-corrected 95 % intervals unless marked; k in the order of the contrast's two arms.

| contrast | k | completion | survival | status |
|---|---|---|---|---|
| Γ = JOINT − ISO | 72 / 72<!-- N:DES-3 --> | null: −1.73 [−4.12, +0.66]<!-- N:RES-1 --> | REJECT: +0.96 [+0.47, +1.44]<!-- N:RES-2 --> | confirmatory |
| Γ, k = 60 prefix | 60 / 60<!-- N:DES-1 --> | null: −2.17<!-- N:RES-3 --> [−4.86, +0.52]<!-- N:DX-20 --> | REJECT: +1.04<!-- N:RES-3 --> [+0.54, +1.55]<!-- N:DX-20 --> | registered-ladder prefix, UNDERPOWERED |
| Γ₄ = JOINT − ISO-4 | 72 / 20<!-- N:DES-3 --><!-- N:DES-13 --> | null: −1.26 [−4.81, +2.28]<!-- N:RES-6 -->, second exclusion bound | null: −0.03 [−0.68, +0.63]<!-- N:RES-6 --> | sensitivity arm, cross-unit |
| Γ₄′ = JOINT − `sweep_c50_p000` | 72 / 20<!-- N:DES-3 --><!-- N:DES-13 --> | null: −2.47<!-- N:RES-8 --> [−6.16, +1.22]<!-- N:DX-19 --> | null: +0.13 [−0.56, +0.81]<!-- N:RES-8 --> | secondary (S5), same card, read at $z_\alpha$ |
| B̂ = ISO-4 − ISO | 20 / 72<!-- N:DES-13 --><!-- N:DES-3 --> | −0.46<!-- N:RES-7 --> [−4.05, +3.12]<!-- N:DX-19 --> | +0.98 [+0.33, +1.63]<!-- N:RES-7 --> | no registered test, no verdict |
| $\Gamma_H$, all-on at β = 0.70<!-- N:CAL-3 --> | 72 / 72<!-- N:DES-3 --> | null: −0.79<!-- N:RES-14 --> [−3.26, +1.68]<!-- N:DX-26 --> | null: +0.38<!-- N:RES-14 --> [−1.46, +2.23]<!-- N:DX-26 --> | eval-only, out of family, not held out |
| Γ(2000) | 4 / 4<!-- N:RES-15 --> | +0.03<!-- N:RES-15 --> [−3.63, +3.69]<!-- N:DX-23 -->, 95 % | +1.59 [−0.02, +3.19]<!-- N:RES-15 -->, 95 % | descriptive, UNDERPOWERED |

**The confirmatory contrast.** At k = 72<!-- N:DES-3 -->, Γ rejects on survival and is null on completion. JOINT's survival exceeds ISO's by +0.96 points, z = +4.43, Šidák-corrected 95 % CI [+0.47, +1.44]<!-- N:RES-2 -->. Completion Γ is −1.73 points (z = −1.62)<!-- N:RES-1 -->: the null excludes a joint-training gain larger than 0.66 points<!-- N:RES-1 -->, and its bound X, the gap of either sign the design would detect with 80 % power, is 3.29 points<!-- N:RES-1 -->. The negative point estimate does not reject and is not a loss. Arm means are 0.7772 (ISO) and 0.7600 (JOINT) on completion, 0.9158 and 0.9254 on survival<!-- N:RES-4 -->. The k = 60 prefix reads the same (z = +4.67 and −1.80<!-- N:RES-3 -->), UNDERPOWERED-flagged as the ladder requires, with realized completion power 60.2 % against 71.6 % at k = 72<!-- N:DES-6 -->.

**The falsifier.** Branch B is claimable only if the completion contrast excludes, in standardized units, an effect as large as the observed survival effect: $\lvert z_c\rvert + z_\alpha = 3.855 < 4.433 = \lvert z_s\rvert$<!-- N:RES-5 --> (4.040 < 4.673 at k = 60<!-- N:RES-5 -->). Branch B stands; the result is not branch C. Under Definition 2 the asymmetry is between a penalized channel and a rewarded one: the reward prices every death at $d_p = 0.5$<!-- N:ENV-1 --> whatever its cause and never reads the hazard, while completion is the rewarded task. Branch A, the founding hypothesis, did not occur, and neither did $A_c$.

**The inert-share correction.** By the rule registered on 2026-09-18<!-- N:DES-15 -->, Γ₄ = JOINT − ISO-4 is null on survival: −0.03 points, z = −0.09, Šidák-corrected 95 % CI [−0.68, +0.63]<!-- N:RES-6 -->. Γ rejects and Γ₄'s interval contains 0, so the survival effect **does not survive the inert-share correction**, and this paper does not call it a composition effect; the branch label stays B, because the rule fixes it by Γ. On completion both are null, so Γ₄ is a **second exclusion bound**, X₄ = 0.0488<!-- N:RES-6 --> (4.88 points). Branch B's registered headline, "composition is paid in agents, not task return", no longer holds as worded.

Γ₄ is cross-unit: ISO-4 ran on a second RTX 5090 unit, JOINT on the first<!-- N:HW-4 -->. Γ₄′ = JOINT − `sweep_c50_p000` repeats it on one card, against ISO-4's exact mixture trained on the confirmatory unit. It is a secondary analysis (S5), proposed on 2026-09-26<!-- N:DES-15 --> after Γ₄ was seen and before `sweep_c50_p000` was read, and by rule it could not change Γ₄'s qualifier. It agrees, null on both metrics (survival +0.13 points, z = +0.41<!-- N:RES-8 -->; table). `sweep_c50_p000` − ISO-4, the two copies of the ISO-4 mixture on different cards, is −0.15 survival points, 95 % [−0.86, +0.56]<!-- N:RES-9 --> (completion in Appendix I).

Removing ISO's fire-only episodes moves its survival by B̂ = ISO-4 − ISO = +0.98 points<!-- N:RES-7 --> (interval in the table, at the family's Šidák level). B̂ has no registered test and no verdict, and no magnitude threshold on it was ever registered. Because Γ = Γ₄ + B̂ holds identically for arm means, B̂ ≈ Γ restates Γ₄ ≈ 0; it is not a second finding.

Two limits bound the correction. First, it excludes a large composition effect, not every one: Γ₄'s upper bound, +0.63 points<!-- N:RES-6 -->, lies above Γ's lower bound, +0.47<!-- N:RES-2 -->. Second, ISO → ISO-4 changes two quantities at once, the active share from 2/3 to 1<!-- N:DES-14 --> and each coupling's frequency from 1/3 to 1/2<!-- N:DES-7 --><!-- N:DES-14 -->, and B̂ cannot say which carries the rise. What Γ₄ does say is that once the active share is matched, JOINT's remaining differences, each coupling twice as often as in ISO-4<!-- N:DES-14 --> and always in combination, add nothing detectable to survival.

**Budget robustness: sign unstable over the final half.** By the registered sign rule, Γ(t) is **sign unstable over the final half** on both co-primaries<!-- N:RES-11 -->. Every reading above is a statement at matched compute, T\* = 1000<!-- N:DES-13 -->, and about no other budget; as registered, the instability is the finding. Figure 12 shows the 11<!-- N:DES-13 --> checkpoints.

<figure class="l-page">
  <iframe src="{{ 'assets/html/submission/gamma_t_final_half.html' | relative_url }}" width="100%" height="480" style="border:none" title="Gamma over the final half of training, completion and survival" loading="lazy"></iframe>
  <figcaption><strong>Figure 12.</strong> <strong>Sign unstable over the final half</strong>, on both co-primaries<!-- N:RES-11 -->. Γ(t) = JOINT − ISO at the 11 retained checkpoints, updates 500 to 1000 in steps of 50, k = 72 per arm<!-- N:DES-13 --><!-- N:DES-3 -->, with Šidák whiskers. The rule asks that all 11 point estimates share one sign; ringed points are the checkpoints whose sign differs from the sign at T&#42; (completion 500, 600, 650; survival 550, 600<!-- N:RES-11 -->). Only t = 1000 is the registered Γ (thick whisker); earlier intervals are descriptive, as no test is registered at t ≠ T&#42;. No line joins the points and no trend is fitted. The figure cannot show where either difference goes after T&#42; = 1000 and carries no convergence claim: the estimand is fixed-budget. <span class="figure-note">Status: registered at t = 1000; descriptive at t &lt; 1000 · Interact: hover or focus a checkpoint for its sign (values are printed at the checkpoints quoted in the text); toggle the single-card curve (t = 1000 re-evaluated on the post-unblind unit, hollow marker) and the floor band at T&#42;; “table view” lists every point.</span></figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/gamma_t_final_half.png" class="img-fluid" alt="The retained checkpoints over the final half of training of the joint-minus-isolated difference in completion and in survival, each with its Šidák interval, labelled sign unstable over the final half" caption="Static companion of Figure 12 for the printed PDF." %}
</div>

The shape, after the verdict. Survival Γ(t) stays between −0.37 and +0.36 points through t = 850, negative at 550 and 600, every interval containing zero<!-- N:DX-25 -->; it then reads +0.56, +0.83 and +0.96 points at t = 900, 950 and 1000<!-- N:RES-12 -->, the only checkpoints whose Šidák interval excludes zero. The survival gap opens only in the last fifth of the budget<!-- N:RES-12 --> and was still rising at T\*. Completion leans negative in the second half: negative at every checkpoint from t = 700, 70 % of the budget<!-- N:RES-13 -->, with an interval excluding zero at t = 750 only, −1.47 points, Šidák-corrected [−2.83, −0.10]<!-- N:RES-13 --> (descriptive). Completion is unresolved and leaning negative, not unaffected. Γ(t) mixes units, t < 1000 evaluated on the post-unblind unit and t = 1000 the grid's own evaluation; re-evaluating t = 1000 on the post-unblind unit gives a single-card curve with the same signs.

The T = 2000 subsample, 4 seeds per arm<!-- N:RES-15 -->, is descriptive, UNDERPOWERED and graded by no test (Γ(2000) in the table). Its differential training-log slope stays positive over updates 1000–2000, +0.00204 (survival) and +0.00384 (completion) per 100 updates<!-- N:DX-23 -->, against +0.00718 and +0.00247 over 500–1000<!-- N:DES-11 -->. This says only that the drift has not visibly reversed, not that Γ holds, grows or vanishes, and Γ(2000) is no convergence argument.

**What the secondary design adds, and where its fit fails.** This paragraph is secondary and **non-verdict-bearing**: 95 % intervals, many of them, none family-corrected. Figure 13 places the arms on the training simplex.

<figure class="l-page">
  <iframe src="{{ 'assets/html/submission/simplex_secondary.html' | relative_url }}" width="100%" height="820" style="border:none" title="Secondary design on the training simplex, with plane predictions beside measured contrasts" loading="lazy"></iframe>
  <figcaption><strong>Figure 13.</strong> The secondary design: <strong>secondary, non-verdict-bearing, 95 %, not family-corrected</strong>; knee UNDERPOWERED; mediation VOID. Left: the training simplex in co-occurrence p (share of episodes with both couplings) and fire-only share ν, which the figure labels n, the single-stressor share being 1 − p − ν; lines of fixed per-coupling marginal μ (which the figure labels m) at 1/3<!-- N:DES-7 -->, 0.4 and 0.5<!-- N:DES-9 -->; the sweep (μ = 0.5) and identification (μ = 0.4) arms and the region they sample; ISO, ISO-4 (whose mixture <code>sweep_c50_p000</code> repeats) and JOINT, outside the sampled region at p = 1<!-- N:DES-7 -->. Below, the arm means at θ&#42;, k = 20 per arm<!-- N:DES-13 -->, against p, the fitted plane as grey ticks. Right: the secondary estimates with 95 % intervals, then two labelled pairs: the plane's prediction of ISO-4 − ISO from γ<sub>n</sub> beside the measured B̂, and its prediction of JOINT − ISO-4 from γ<sub>p</sub> beside the measured Γ₄ and Γ₄′. The γ<sub>n</sub> prediction lies inside B̂'s interval; the γ<sub>p</sub> prediction lies far above Γ₄ and Γ₄′. The figure cannot separate per-coupling exposure from co-occurrence or from active share (moving p at fixed ν, or ν at fixed p, also moves μ), cannot show a causal effect of any realized dose, grades no intermediate arm against a floor of its own, and assumes the plane is linear. <span class="figure-note">Status: secondary, non-verdict-bearing, 95 %, not family-corrected · Interact: switch the metric (survival | completion; completion shows the γ<sub>p</sub> pair only); toggle “plane predictions and measured contrasts”; hover an arm or an estimate; “table view” lists every value.</span></figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/simplex_secondary.png" class="img-fluid" alt="A triangle of training mixtures by share of both-stressor and fire-only episodes, locating the secondary arms, ISO, ISO-4 and JOINT, beside the secondary estimates and the plane predictions next to the measured contrasts" caption="Static companion of Figure 13 for the printed PDF." %}
</div>

At ISO's behavioural fire-only share of 1/3, the survival plane's $\gamma_n$ predicts ISO-4 − ISO = +0.79 points<!-- N:SEC-3 -->, inside the measured B̂, +0.98 [+0.33, +1.63]<!-- N:RES-7 -->. This does not attribute B̂ to the fire-only share as such: at fixed $p$ a move in $\nu$ is also a move in $\mu$, so $\gamma_n$ is the slope along which active share and per-coupling frequency change together. $\gamma_p$ is a tension, not a finding: at fixed fire-only share, moving single-stressor episodes into both-stressor episodes raises survival across the sampled region ($\gamma_p$ = +3.26 points per unit co-occurrence, 95 % [+1.37, +5.02]<!-- N:SEC-1 -->), but it also raises each coupling's frequency, which the simplex does not let the design separate. And the plane fails where it would matter: fitted on $p \le 0.5$<!-- N:DX-28 -->, it predicts JOINT − ISO-4 = +3.26 points at $p = 1$<!-- N:SEC-4 -->, while Γ₄ and Γ₄′ measure −0.03 and +0.13<!-- N:RES-6 --><!-- N:RES-8 -->; a local slope that does not extrapolate claims nothing. Appendix I gives the rest: $\gamma_n$ and the bound on the fire-only confound (bounded away from zero), the sweep's own slope (its interval contains zero), the completion family (nothing resolves), both knees (UNDERPOWERED) and the coarse linearity check.

**Where the survival gap lives.** On secondary metrics outside the family, descriptive and graded against no floor of their own, JOINT episodes have 0.1177 fewer fire deaths than ISO episodes (z = −4.59)<!-- N:RES-10 -->, 0.6949 against 0.8126 per episode<!-- N:DX-22 -->. Because no agent revives, deaths per episode equal 12<!-- N:ENV-6 --> × (1 − survival rate), so by that identity the survival gap corresponds to about 0.11 agents per episode<!-- N:DX-406 -->, of the same size; this is descriptive and grades nothing. Episode return differs by −0.4958 (z = −1.44)<!-- N:DX-22 -->.

**The High readout: a-fortiori exclusions.** Every T\* checkpoint of ISO, JOINT and ISO-4 was re-evaluated, unconditionally, with every stressor on at β = 0.70<!-- N:CAL-3 --> (eval-only, out of family). Both co-primaries are null (table), so the reading is an **a-fortiori exclusion**: no gap larger than 3.40 completion points or 2.54 survival points<!-- N:RES-14 --> at High even where JOINT trained on the evaluated configuration and ISO never saw a composed one. $\Gamma_{H,4}$ is null on both, −0.75 and −1.28 points, Šidák-corrected 95 % CIs [−3.87, +2.36] and [−3.50, +0.95]<!-- N:DX-26 -->. $\Gamma_H$ is 0.73× and 0.75× its floor-basis sd(Γ) on the evaluation unit<!-- N:RES-14 -->, within rerun noise. It is not a held-out test: JOINT trained on this configuration at weight 1/2<!-- N:DES-16 -->, ISO only on single-stressor High components. At High, Coupling B is live (its survival effect replicated in direction 3/3<!-- N:CB-5 -->) and Coupling A marginal by construction, its seeded ignitions falling 4.83-fold from Low<!-- N:CA-4 -->: the mirror of Medium.

**Mediation: VOID.** The registered mediator, the co-active counter's realized training dose, carried a void rule fixed before the sweep was read: VOID if its first-stage slope on $p$ has a 95 % interval containing zero. The slope is −1.03 × 10⁻⁵ per unit $p$, 95 % [−2.91 × 10⁻⁵, +0.93 × 10⁻⁵]<!-- N:DX-29 -->, so mediation is **VOID**<!-- N:SEC-7 -->. Diagnosed after the run, without changing the rule: the counter counts collapse-seeded ignitions inside an alive agent's crop<!-- N:CO-4 -->, which only Coupling A produces, with or without Coupling B, so in mixtures it measures the A marginal the sweep holds fixed. The registered mediator was blind to co-occurrence in mixed training; "co-active" describes the counter only in all-on configurations.

**Reproducibility and hardware.** Seed dispersion exceeds the rerun floor in both arms, 1.12× / 1.09× on completion and 1.25× / 1.19× on survival (ISO / JOINT), and survival Γ is 5.40× its floor-basis sd(Γ)<!-- N:HW-1 --> (completion 1.78×<!-- N:DX-21 -->), clearing the beat-reproducibility hurdle. Evaluation is exact on one card: four repeats of two checkpoints are bit-identical on the post-unblind unit and to the grid's own evaluations<!-- N:HW-2 -->; across cards, 280 of 288 paired (checkpoint, metric) evaluations are identical, max |Δ| = 2.44 × 10⁻⁴<!-- N:HW-3 -->. Blocks: Γ on one RTX 5090 unit, ISO-4 and the T = 2000 subsample on a second, Γ₄′ on the first, the post-unblind evaluations on a third<!-- N:HW-4 --><!-- N:DX-5 -->.

**Discussion.** Match the active share before claiming composition. Once ISO's fire-only episodes are removed, which raises its active share and each coupling's frequency together, JOINT's remaining differences, twice<!-- N:DES-14 --> the per-coupling frequency and full co-occurrence, add nothing detectable to survival. That is an exclusion: a composition effect up to +0.63 points<!-- N:RES-6 --> is not ruled out. The arm that showed it cost 20 runs<!-- N:DES-13 -->. A registered design caught it: the bias and its reading rule were fixed before the look, and read alone the confirmatory contrast invites a composition reading the correction does not support. Survival moving while completion stays unresolved also appeared one level down, for Coupling B at High (§6). The co-occurrence slope $\gamma_p$, which saturates before JOINT, earns a figure, not a claim. All of it holds at matched compute, sign unstable over the final half, in one environment.

<!-- BUILDER-WRITTEN DEMONSTRATION (DEMONSTRATION DRAFT ruling, 2026-10-11); not the owner's text -->

## 10 Limitations

These limitations are properties of the design, registered or recorded before the outcome was known, and they are stated here whatever the result. The first ten follow the order fixed for every outcome branch; the rest are what the record adds.

1. **Medium siting.** θ\* sits at Medium, where Coupling B's own measured survival effect was −0.03 points, graded only against a three-seed spread and not a measured floor<!-- N:CB-9 -->. Its survival effect lives at High, where the $\kappa_B$ 1.0 − 0 contrast replicated in direction three times out of three, between −4.7 and −10.7 points<!-- N:CB-5 --> (the registered text quotes the first two-seed estimate, 8.8 points<!-- N:CB-6 -->). Medium was chosen because both couplings clear their lock criteria there and its floors are the smallest, which trades the existence of a behavioural effect for measurability. By the project's own locks no severity has both couplings strongly live: at Medium B is quiet and A live; at High A is marginal by construction, its seeded ignitions falling 4.83-fold from Low<!-- N:CA-4 -->, and B live. The High readout adds breadth in severity; it does not test composition where both couplings bite. The pre-unblind line that read a Medium survival effect as one "the single coupling did not show" is struck: Γ₄ and Γ₄′ contradict it.
2. **One held-out severity.** θ\* is one point, interpolated in one scalar between training at β = 0.43 and 0.70<!-- N:CAL-3 -->. No training data lies near criticality, so the test point is dynamically unlike either training severity; whether that makes it the hardest regime or a confound, the design cannot say.
3. **No coordination is required.** Twelve agents<!-- N:ENV-6 --> share one policy's parameters<!-- N:ENV-11 --> and a team reward of +1 per collected item<!-- N:ENV-9 -->; the task can be solved without coordination. "Swarm" is not a claim of this paper.
4. **The death penalty.** The reward sees deaths, at $d_p = 0.5$ each<!-- N:ENV-1 -->, not the hazard, so the survival/completion asymmetry is between a penalized channel and a rewarded one. The only $d_p$ ablation is old and narrow: the fire alone with no couplings, 500 updates, 3 seeds, and an earlier observation encoding<!-- N:ENV-2 -->. At $d_p = 0$ survival would be learned only because death truncates task return; the ablation was not re-run under the Phase-6 protocol.
5. **A frozen message encoder.** "Inert" is scoped to a frozen random-projection message encoder at this scale: the message head receives no gradient<!-- N:ENV-12 -->, and gradient-shaped messaging is untested. The composition the test probes is A × B, with δ carried for registration fidelity.
6. **Position and time are observed.** The own-state vector carries row/L, col/L and t/horizon<!-- N:ENV-7 -->, so a policy can condition on where and when it is independently of the hazard. Its visible form is the wall-drift artifact: in renders of the Phase-4 (Coupling-B) policies, 24 of 24 episodes drift towards a wall<!-- N:DX-32 --> (rendered-pixel centroids, a diagnostic). No differenced test can see it, since a drift present in both arms cancels in Γ. The drift channels the grid records are recorded, not graded: they have no floors.
7. **Conditional intervals.** Every Phase-6 interval is conditional on one common evaluation draw, eval seed 0 × 512 episodes<!-- N:DES-13 -->. The draw cancels in a difference of arm means; the intervals carry training-seed variance only and say nothing about eval-set sampling.
8. **Hardware block structure.** Three rented units of one card model, the RTX 5090<!-- N:DX-5 -->. Γ uses all 72<!-- N:DES-3 --> seeds of both arms on unit 1, as does every analysed secondary run (seeds 1–12 re-run there, 13–20 from the grid<!-- N:DX-30 -->), so Γ₄′ is same-card. ISO-4 and the T = 2000 subsample trained on unit 2, so Γ₄ and B̂ are cross-unit. The post-unblind evaluations (Γ(t) at t < 1000, the High readout, the eval floor) ran on unit 3<!-- N:HW-4 -->. The grid's first 12 seeds ran on an RTX PRO 6000; they were superseded by the single-card re-run and enter only a descriptive card diagnostic<!-- N:DX-30 -->.
9. **No external baseline and no adaptive curriculum.** The paper compares two fixed training distributions on one environment, with one learner (single-policy IPPO, the same hyperparameter set for every arm<!-- N:DX-2 -->). No domain-randomization schedule or adaptive curriculum is evaluated.
10. **A simple hazard.** Burn time is exactly one step, there is a single ignition at reset, spontaneous ignition is off (ι = 0<!-- N:DX-1 -->), and there is no wind or fuel heterogeneity. The burnt region is a percolation cluster by construction (Proposition 2), and Corollary 1's exact critical value holds only for that idealized kernel.

What the record adds:

- **The correction's own limits.** The survival effect **does not survive the inert-share correction**, but the correction excludes a large composition effect, not every one: Γ₄'s upper bound lies above Γ's lower bound (§9.2). Removing ISO's δ-only episodes changes the active share and each coupling's frequency together, and nothing in this design separates them; the secondary plane's $\gamma_n$ moves both. Which of the two carries the effect is open.
- **Matched compute only.** Γ is a fixed-budget contrast; Γ(t) is sign unstable over the final half on both co-primaries, the survival gap opened only late (§9.2), and no claim about convergence or another budget is made. The T = 2000 subsample is UNDERPOWERED.
- **Completion is unresolved.** The completion null is an exclusion with its bound, and the completion difference leaned negative over the second half (§9.2); the paper does not claim that completion is unaffected.
- **What Proposition 4 does not say.** It bounds what ISO can be guaranteed to transfer, not the realized gap; no theorem here predicts which arm wins.
- **Bars without their own floor.** Coupling B's Medium effect was graded against a three-seed spread<!-- N:CB-9 -->; the Coupling-A and Coupling-B grids have no identical-rep set, so their spreads are reference scales (cross-artifact); the intermediate sweep arms assume the sweep endpoint's floor, and the identification arms are ungraded; ISO-4 has no rep set and is graded on seed dispersion only; fire deaths and every other out-of-family channel grade nothing.
- **Instruments blind to what they did not measure.** Every differenced test sees only asymmetry between arms. The registered mediator was blind to co-occurrence in mixed training, so mediation is VOID rather than null. The secondary family reports many 95 % intervals, none family-corrected, and is non-verdict-bearing.
- **A recorded deviation.** The confirmatory arms ran k = 72<!-- N:DES-3 --> seeds against a registered cap of 60<!-- N:DES-1 -->; the change was made before unblinding with no outcome seen, and the registered k = 60 analysis is reported beside it.
- **One environment.** The argument for matching the active share is general, but it was measured in one environment, at one scale, with one learner.

<!-- BUILDER-WRITTEN DEMONSTRATION (DEMONSTRATION DRAFT ruling, 2026-10-11); not the owner's text -->

## 11 Reproducibility

**What the anonymized code supplement contains.** The environment (`che/env/`), training (`che/train/`), evaluation (`che/eval/`) and calibration (`che/calibration/`) code; every configuration (`che/configs/`), including the generated Phase-6 protocol configurations and θ\*; the analysis instruments that produced every Phase-6 number (`che/scripts/p6_unblind.py`, `che/scripts/p6_post_analysis.py`, `che/scripts/p6_secondary.py`); the registry of locked constants (`docs/locks.yaml`) with the test that asserts the configurations and code defaults agree with it (`che/tests/test_locks.py`); and the CPU test suite (`che/tests/`), which runs the theory checks as unit tests. Every locked environment constant is reachable from a configuration and checked by that test, and every locked analysis constant is checked against the literal in the instrument that uses it, so a lock cannot live only in prose or on a command line.

**What is exact, and what is not.** Ablations are exact by construction: every stochastic branch consumes its random numbers whether or not its stressor is on, so switching a stressor off reproduces the nested model's trajectories bit for bit under the same keys (Listing 3, §3). Evaluation is reproducible: four repeated evaluations of each of two checkpoints are bit-identical on one card and identical to the grid's own evaluations<!-- N:HW-2 -->, and across cards 280 of 288 paired evaluations are identical, max |Δ| = 2.44 × 10⁻⁴<!-- N:HW-3 -->. GPU training is not run-to-run reproducible, because the compiler autotunes kernels by timing and some reductions use atomics. That is why reproducibility floors are measured, as identical reruns on the card that ran each study (Appendix C); the tests of §9 use each arm's own seed dispersion instead, because a mean over k seeds varies by seed as well as by nondeterminism (§8).

**Cost of a re-run.** A 1000-update training run took 518–521 s and a 512-episode evaluation 9–10 s on one RTX 5090<!-- N:DX-4 --> (Python 3.12.3, jax 0.11.0<!-- N:DX-407 -->), for 32,768,000 environment steps per run<!-- N:DX-3 -->. The IPPO hyperparameters are in Appendix B<!-- N:DX-2 -->, the seed layout and card blocks in Appendix F.

**Checkpoints.** The trained checkpoints are not in the supplement. Each archive has a recorded sha256, and a re-verification matched every recorded hash<!-- N:DX-408 -->; Appendix F states the one floor set whose archives were mostly never hashed, which grades nothing.

**One look per stage.** The analysis instruments refuse to run out of order, and each stage's log records a single run (§9.1, blinding).

**Appendices.**

- A. Proofs: Propositions 1–4, Theorem 1 and Remark 2′.
- B. Every locked constant with its ruling date; the IPPO hyperparameters and the budget.
- C. Every measured floor, with card, run length, artifact and sample size.
- D. The frozen analysis plan: registered constants and reading rules, verbatim, with dates.
- E. The registered outcome branches and the falsifier.
- F. Grid provenance: runs, seed layout, card blocks, archives.
- G. Throughput: what the paper does and does not state.
- H. Γ(t): both full tables and the sign reading.
- I. The secondary design: every arm and interval.
- J. Trained-policy episodes: one illustrative episode per arm, shown separately.

<!-- BUILDER-WRITTEN DEMONSTRATION (DEMONSTRATION DRAFT ruling, 2026-10-11); not the owner's text -->

## Appendices

### A Proofs

Each statement is in the body, where the section named below gives it; this appendix gives the proofs, typeset from the formal specification, with one departure noted under Proposition 1. The notation is that of Definition 1, with $\Theta$ the set of environment configurations $\theta = (\beta, \kappa_A, \kappa_B, \delta)$.

**Proposition 1 (Well-posedness).** Statement in §3.1.

**Proof.** Each factor of $T_\theta$ is a conditional kernel, measurable in its conditioning variables, all of which are components of $(s, a)$ or of already-sampled components of $s'$. The dependence of $T_H$ on $c'$ and of $T_K$ on $x'$ is a sequential composition within one time step: sample $c' \sim T_C(\cdot \mid c, x)$, then $h' \sim T_H(\cdot \mid h, c, c')$, then $\rho' = T_\rho(\rho, h')$ (deterministic), then $x' \sim T_X(\cdot \mid x, a, h', c')$, then $k' \sim T_K(\cdot \mid x')$. A composition of Markov kernels is a Markov kernel on the product space, so $T_\theta$ is a valid transition kernel on $\mathcal{S}$ and $(s_t)$ is Markov. The action sets are finite, every stochastic factor and the reset distribution have finite support, and $\rho$ evolves deterministically from $\rho_0 = 0$, so the states and observations reachable within the horizon form finite sets; restricted to them, $\mathcal{M}_\theta$ is a finite Dec-POMDP, so optimal finite-horizon joint policies exist by the standard argument. $\blacksquare$

This departs from the formal specification's wording, which states that $\mathcal{S}$ and $\Omega_i$ are finite: with the real-valued smoke field $\rho \in \mathbb{R}_{\ge 0}^G$ in the state, that holds only for the states and observations reachable within the horizon, which is all the argument uses.

**Proposition 2 (Bond percolation).** Statement in §3.2.

**Proof (coupling).** Attach to each unordered edge $e = \{g, g'\}$ an independent $B_e \sim \mathrm{Bernoulli}(\beta)$, and declare that a transmission attempt across $e$ succeeds iff $B_e = 1$. Each edge is attempted at most once: when one cell of $e$ first Burns while the other is Fuel, one attempt occurs; afterwards the burning endpoint is Burnt, which is absorbing, and if the other endpoint later Burns via a different path, its neighbour across $e$ is already Burnt, so no second attempt occurs. Hence the fire, run with the variables $\{B_e\}$, burns exactly the connected component of the origin in the subgraph of open edges $\{e : B_e = 1\}$, which is the bond-percolation cluster. $\blacksquare$

This is the mapping between SIR with a constant infectious period and bond percolation that Grassberger (1983)<d-cite key="grassberger1983"></d-cite> gives, here with a self-contained proof. The implementation realizes the coupling exactly (`che/env/hazard.py`, module docstring): Definition 3 asks for independent ignition attempts per ordered pair (Burning cell $g$, Fuel neighbour $g'$); the kernel samples one uniform per cell per incoming direction, and the ordered pair $(g \to g')$ maps bijectively to the slot ($g'$, direction of $g$ from $g'$), so per-ordered-pair independence is exact. With a burn time of exactly one step, each unordered edge sees at most one attempt over the whole trajectory, so these uniforms are also the per-edge Bernoulli variables of the coupling.

**Proposition 3 (Collapse events dominate hazard exposure; divergence near criticality).** Statement in §5.2.

**Proof.** Each collapse seed grows, by Proposition 2, a burnt cluster equal in distribution to a bond-percolation cluster, of expected size $\chi(\beta)$. By linearity of expectation over the Binomial or Poisson number of seeds, the total expected burnt area is $\lambda_A T \chi(\beta)$ when clusters are disjoint; overlaps only remove double counting, which gives the upper bound in general. The divergence rate is Corollary 1(3). $\blacksquare$

Two details of the finite-protocol remark (§5.2) that §5 does not repeat: under correction (iii), cluster mass at $\beta = 0.43$<!-- N:CAL-3 --> saturates by an age of $t_{\mathrm{sat}} \approx 64$ steps<!-- N:DX-409 -->; and at both of M3.3's grid sizes the four measured factors compose to the observed slope within Monte Carlo error, with a residual that does not depend on grid size.

**Theorem 1 (Memorization gap, and its erosion by Coupling B).** Statement in §6.2; items (1)–(3) below refer to it.

**Proof.** *(1)* With zero slack, the only decisions are the corridor choice at $b$ and, vacuously, the path to $b$; waiting or probing is impossible within $T$. If informed (probability $q$), taking the corridor other than $Z$ succeeds with probability 1; if uninformed, both corridors are exchangeable given the history, so any choice succeeds with probability $\tfrac12$. Hence $J^* = q + (1-q)\tfrac12 = \tfrac12 + \tfrac{q}{2}$, and no policy can exceed this, since success requires either information (probability $q$) or a lucky guess. *(2)* In the fixed-map environment the signal is uninformative (constant $Z$), so the signal-blind policy is among the optimal ones there; on $E_{2C}$ it succeeds iff $Z = z_0$, with probability $\tfrac12$. *(3)* Each factor $(1 - e^{-\kappa_B j})$ is continuous and strictly increasing in $\kappa_B$ on $(0, \infty)$, so the finite product is too, and $q$ is continuous and strictly decreasing. The limits are immediate: $e^{-\kappa_B j} \to 1$ pointwise as $\kappa_B \to 0$, so the product tends to 0, and it tends to 1 as $\kappa_B \to \infty$. $\blacksquare$

**Proposition 4 (An irreducible shift term for ISO).** Statement in §9.1, for the $\gamma$-discounted return; the simulation lemma is stated for the factored kernels, with constants not optimized.

**Proof.** The value-difference bound is the standard simulation lemma: telescope the Bellman evaluation operators of the two models along the trajectory distribution; the observation term enters because $\pi$ acts through $O$. $\varepsilon_{\min} > 0$ holds because on states $s$ with a collapse increment adjacent to Fuel and an agent within attenuation range, $T_{\theta^*}$ places mass of order $\kappa_A$ on ignition transitions that $T_\theta$ with $\kappa_A = 0$ places elsewhere, and similarly for the observation term when $\kappa_B$ differs. $\blacksquare$

As §9.1 states, the proposition bounds what ISO can be *guaranteed* to transfer, not what happens: it does not lower-bound the realized $\Gamma$.

**Remark 2′.** Stated in §7.2, after Pynadath & Tambe (2002)<d-cite key="pynadath2002"></d-cite>. One step §7 does not spell out: write $\tilde q$ for the probability of being informed under the best idling schedule. The draws of the commitment schedule have different optical depths, so as $\kappa_B \to \infty$ the lowest-depth draw dominates both products and $\tilde q / q \to 1$: the idling correction is not asymptotic, and its relative bite on the value of communication is largest at low $\kappa_B$, where $q$ is near 1.

### B Locks and hyperparameters

Every locked environment constant is reachable from a configuration and asserted against the configurations and code defaults by `che/tests/test_locks.py`; every analysis constant is asserted against the literal in the instrument that uses it.

| constant | value | ruled | record |
|---|---|---|---|
| critical point $\hat\beta_c$ | 0.500 ± 0.005<!-- N:CAL-1 --> | 2026-07-19<!-- N:DX-401 --> | severity lock record; its estimator ($R_L$ logistic centres) has no committed script, and the committed estimators give a crossing mean of 0.504 and a consensus of 0.499<!-- N:CAL-1 --> |
| β Low / Medium / High | 0.43 / 0.49 / 0.70<!-- N:CAL-3 --> | 2026-07-19<!-- N:DX-401 --> | severity lock record |
| β held out (θ\*) | 0.49<!-- N:CAL-3 --> | 2026-08-02<!-- N:DX-401 --> | Phase-6 design ruling; equal to β Medium, kept separate because the role differs |
| $f_{\mathrm{weak}}$, $\lambda_0$, $\lambda_{\mathrm{load}}$, $\kappa_A$, $r_A$ | 0.15, 5e-5, 4e-4, 0.06, 1<!-- N:CA-1 --> | 2026-07-21<!-- N:DX-401 --> | Coupling-A lock record |
| weak-floor smoothing passes | 2<!-- N:DX-401 --> | 2026-07-21<!-- N:DX-401 --> | Coupling-A lock record |
| $\kappa_B$ | 1.0<!-- N:CB-1 --> | 2026-07-27<!-- N:DX-401 --> | $\kappa_B$ lock record, on the detection band alone |
| δ off / on; $R_{\mathrm{comm}}$ | 0.0<!-- N:DX-401 --> / 1.0; 16<!-- N:COM-6 --> | 2026-07-30<!-- N:DX-401 --> | communication lock record |
| death penalty $d_p$ | 0.5<!-- N:ENV-1 --> | 2026-07-19<!-- N:DX-401 --> | the death-penalty design decision |
| observation version | v3<!-- N:DX-401 --> | 2026-07-24<!-- N:DX-401 --> | the observation design decision, frozen after the Coupling-B observation milestone |
| $\sigma_s$, η, ι | 1.0, 0.5, 0.0<!-- N:DX-1 --> | not locked | held fixed by convention, never calibrated |

| analysis constant | value | ruled | role |
|---|---|---|---|
| `K_CONFIRMATORY` | 40<!-- N:DES-1 --> | 2026-08-03<!-- N:DX-402 --> | design seed count per confirmatory arm; the re-floor ladder computes against it |
| `K_LADDER_CAP` | 60<!-- N:DES-1 --> | 2026-08-03<!-- N:DX-402 --> | the ladder's cap |
| `K_CONFIRMATORY_REALIZED` | 72<!-- N:DES-3 --> | 2026-09-22<!-- N:DX-402 --> | the k at which Γ is read; a recorded deviation |
| `K_SECONDARY` | 20<!-- N:DES-13 --> | 2026-08-02<!-- N:DX-402 --> | seeds per secondary arm; ISO-4 uses the same k |
| `SIDAK_M`; $z_\alpha$ | 2; 2.2365<!-- N:DES-13 --> | 2026-08-02<!-- N:DX-402 --> | the confirmatory family of two co-primaries |
| `POWER_STOP` | 0.80<!-- N:DX-402 --> | 2026-08-02<!-- N:DX-402 --> | minimum design-stage power at the 0.03<!-- N:DES-4 --> band |
| `T_STAR` | 1000<!-- N:DES-13 --> | 2026-08-11<!-- N:DX-402 --> | the fixed budget (provenance re-pointed; value unchanged since 2026-08-03<!-- N:DX-402 -->) |
| `GAMMA_T_RETENTION` | 11<!-- N:DES-13 --> | 2026-08-11<!-- N:DX-402 --> | checkpoints kept for Γ(t), updates 500–1000 every 50<!-- N:DES-13 --> |
| evaluation draw | seed 0 × 512 episodes<!-- N:DES-13 --> | with the grid layout | common to every run |
| `PLATEAU_PASS`; `PLATEAU_REVIEW` | 1.0; 1.5<!-- N:DX-402 --> | 2026-08-02<!-- N:DX-402 --> | the plateau criterion, retired as a certification instrument on 2026-08-11<!-- N:METH-6 -->; grades nothing |

Training hyperparameters, identical for every Phase-6 arm (the grid passes none on the command line, so the configured defaults apply):

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

A floor is the standard deviation of a metric over identical reruns at one seed: nondeterminism alone, not seed spread. Floors are per metric, per card, per artifact and per run length; this appendix lists each one the paper uses, with its card, run length, artifact and number of reps. With four reps an sd has 3 degrees of freedom and is uncertain by about ±40 %<!-- N:DX-403 -->; the Phase-6 training floors use eight<!-- N:DX-403 -->.

| study | card | updates | artifact | reps | floor | use |
|---|---|---|---|---|---|---|
| M5.1e | RTX 5090<!-- N:DX-403 --> | 500<!-- N:DX-403 --> | Medium, couplings locked, communication live at δ = 0<!-- N:METH-1 --> | 4<!-- N:DX-403 --> | completion 0.0145, survival 0.0129<!-- N:METH-1 --> | Phase-5 bars |
| M5.5 | RTX PRO 6000<!-- N:DX-412 --> | 500<!-- N:DX-412 --> | Medium, $R_{\mathrm{comm}}$ 16<!-- N:METH-1 --> | 4<!-- N:DX-412 --> | completion 0.0399, survival 0.0130<!-- N:METH-1 --> | with M5.1e, the per-hardware exhibit; card, code tree and configuration all differ |
| M5.5 danger-moment | RTX PRO 6000<!-- N:DX-412 --> | 500<!-- N:DX-412 --> | Medium | 4<!-- N:DX-412 --> | 27.2 % relative nondeterminism (sd 0.00182)<!-- N:COM-5 --> | voids the 20 %<!-- N:COM-5 --> condition (iii) |
| M5.3b | RTX PRO 6000<!-- N:DX-403 --> | 500<!-- N:DX-40 --> | High | 4<!-- N:DX-40 --> | survival 0.0621<!-- N:CB-7 --> | reference scale (cross-artifact) for the Phase-4 High effect |
| M6.0 | RTX PRO 6000<!-- N:DX-5 --> | n/a | field digests, traced vs reference tree | 4 comparisons<!-- N:METH-2 --> | reference tree 0 of 760 differing in 4 of 4; traced tree differs from itself 1 time in 4, on two diagnostic channels<!-- N:METH-2 --> | the per-artifact exhibit |
| M6.2 | RTX PRO 6000<!-- N:DX-34 --> | 500<!-- N:DX-34 --> | ISO, JOINT | 8<!-- N:DX-403 --> | completion ISO 0.0165, JOINT 0.0093<!-- N:DX-34 --> | plateau guard |
| M6.2b | RTX PRO 6000, another box<!-- N:DX-34 --> | 1000<!-- N:DX-34 --> | ISO, JOINT | 8<!-- N:DX-403 --> | completion ISO 0.0339, JOINT 0.0483<!-- N:DX-34 --> | set the design k = 40<!-- N:DES-1 --><!-- N:DX-402 -->; floors grow with run length, 2.1× and 5.2×<!-- N:METH-5 -->, length confounded with box |
| G1.2 launch batch, 2026-08-10<!-- N:DES-5 --> | RTX PRO 6000 | 1000<!-- N:DX-403 --> | ISO, JOINT, sweep endpoint | 8<!-- N:DX-403 --> | design-stage sd(Γ) at k = 40: 0.00504 / 0.00310<!-- N:DES-5 --> | design-stage power; drift ISO 0.56×, JOINT 1.02× its floor<!-- N:DES-10 --> |
| re-floor, 2026-09-08<!-- N:DES-2 --> | RTX PRO 6000<!-- N:DES-2 --> | 1000<!-- N:DX-412 --> | ISO, JOINT, sweep endpoint | 8<!-- N:DX-403 --> | $k_{\mathrm{req}}$ 46<!-- N:DES-2 --> | the ladder; drift ISO 0.80×, JOINT 0.68×<!-- N:DES-10 --> |
| grid-card re-floor | RTX 5090, unit 1<!-- N:DX-35 --> | 1000<!-- N:DX-412 --> | ISO, JOINT, sweep endpoint | 8<!-- N:DX-35 --> | completion ISO 0.0587, JOINT 0.0577; survival 0.0100, 0.0112<!-- N:DX-35 --> | the ladder ($k_{\mathrm{req}}$ 72 / 3<!-- N:DES-3 -->); the beat-reproducibility hurdle; drift ISO 0.33×, JOINT 0.19×<!-- N:DES-10 --> |
| evaluation floor | RTX 5090, unit 3<!-- N:HW-4 --> | evaluation only | two checkpoints | 4<!-- N:HW-2 --> | bit-identical, and identical to the grid's evaluations<!-- N:HW-2 --> | evaluation reproducibility |
| partial re-floor, 2026-08-14<!-- N:DX-36 --> | not recorded<!-- N:DX-36 --> | n/a | ISO, JOINT | 8 ISO + 4 JOINT evaluated<!-- N:DX-36 --> | none reported | provenance only; grades nothing |

The grid card's floors cannot be distinguished from the RTX PRO 6000's: the 95 % intervals for the sd overlap (ISO completion [0.0186, 0.0571] on the RTX PRO 6000 against [0.0388, 0.1194] on the RTX 5090<!-- N:DX-35 -->), and no claim is made that either card is less reproducible.

### D The frozen analysis plan

The registered constants are those of Appendix B: Šidák m = 2 with $z_\alpha$ = 2.2365, T\* = 1000, Γ(t) at 11 checkpoints over updates 500–1000 every 50, k = 20 per secondary arm, k = 72 realized per confirmatory arm, and one evaluation draw, eval seed 0 × 512 episodes<!-- N:DES-13 --><!-- N:DES-3 -->. The reading rules follow, quoted verbatim from the registration record with their dates; emphasis is the record's own, one indented code line is set inline, omissions are marked […], and nothing inside a quotation is paraphrased. A "§" inside a quotation refers to the record's own sections, not to this paper's.

**1. The fixed-budget estimand** (T\* ruling, item 2, 2026-08-11<!-- N:METH-6 -->):

> **Primary Γ = the confirmatory contrast at MATCHED BUDGET T = 1000<!-- N:DES-13 -->, all arms — registered as a fixed-budget claim.**
>
> **"At convergence" is explicitly NOT claimed anywhere.** The paper says **"at matched compute"** throughout, which is also the practitioner-relevant question.

**2. Budget robustness** (T\* ruling, item 3, 2026-08-11<!-- N:METH-6 -->; restated for every branch on 2026-08-13<!-- N:DES-12 -->):

> The fixed-budget conclusion is reported as **budget-robust iff the sign of Γ is stable over the final half of training**. If the sign is still moving at T, **that instability IS the finding** and is reported as such.

> Mechanism: 11 retained checkpoints, updates 500–1000 at interval 50<!-- N:DES-13 -->, confirmatory arms only, **evaluated post-unblind**. Every branch above gains "— budget-robust" or "— sign unstable over the final half" as a suffix, and the suffix is not optional.

**3. The branch-B falsifier** (2026-08-13<!-- N:DES-12 -->):

> Branch B is claimable **only if** the completion contrast excludes an effect as large, in standardized units, as the observed survival effect:
>
> `|z_c| + z_α  <  |z_s|,     z = Γ / sd(Γ) per metric`
>
> with `sd(Γ)` the grid's own measured per-arm seed dispersion in the combined form and `z_α = 2.2365`<!-- N:DES-13 --> the two-sided Šidák critical value at m = 2. **If it fails, the result is branch C with an asymmetry the design could not resolve — not branch B.**

**4. The inert-share reading rule** (the proposals ruling of 2026-09-18<!-- N:DES-15 -->):

> - Γ and Γ₄ are reported **side by side on every branch**, with B̂ and its CI.
> - If Γ rejects on a co-primary and **Γ₄'s CI on that co-primary includes 0 or its sign is opposite**, the paper states that the effect **does not survive the inert-share correction**, in the abstract-level summary and not only in an appendix. **The branch label does not change** — it is fixed by Γ — but branch A/B text may not describe the effect as a composition effect without that qualifier.
> - If Γ is null and Γ₄ is null, Γ₄ is quoted as a second exclusion bound.
> - If Γ is null and Γ₄ rejects **negative**, it is reported under branch D's framing (matched-budget asymmetry) as a secondary observation, never as a confirmatory finding.
> - **No magnitude threshold on B̂ is introduced**, now or later.

**5. The High readout** (the same ruling, 2026-09-18<!-- N:DES-15 -->), its reading for a null:

> - **Γ_H null → an *a fortiori* exclusion**, and the only outcome this readout can establish: *"no gap larger than X at High even where JOINT trained on the evaluated configuration and ISO never saw a composed one."* Quoted as an exclusion with X from the grid's own seed dispersion, never as an absence.

The same entry states that the readout "is NOT a held-out test", that a positive $\Gamma_H$ is "NOT separable from in-distribution advantage", and that a negative one is "exploratory".

**6. The T = 2000 subsample** (the same ruling, 2026-09-18<!-- N:DES-15 -->):

> **What it may be cited for:** whether the differential drift measured at T = 1000 (review §6 item 1: 0.01209 per 100 updates<!-- N:DES-10 -->) visibly persists, closes or reverses. **What it may not be cited for:** any claim that Γ "holds" or "vanishes" at T = 2000.

**7. The mediation void rule** (the design's frozen analysis plan, ruled 2026-08-02<!-- N:DX-414 -->):

> **If realized dose does not vary with assigned p, the dose figure has no x-axis and is declared VOID** — registered now, not decided after seeing the first stage.

**8. The pre-unblind rulings** (2026-09-26<!-- N:DX-405 -->, before the look):

| # | question | RULED |
|---|---|---|
| (i) | what "−" means in the branch table | **Rejection with negative sign** (\|z\| > z_α, Γ < 0). A negative estimate that does not reject is a null. Ratified as built. |
| (ii) | the cell (completion +, survival null), absent from the registered table | **REGISTERED NOW as branch A_c — the founding claim on the founding primary.** […] |
| (iii) | test statistic | **Normal z, z_α = 2.2365<!-- N:DES-13 -->**, as the frozen plan wrote; the t critical value is printed, not applied. Ratified as built. |
| (iv) | Γ(t) "sign stable" | **All 11 point estimates, t = 500 … 1000, share one nonzero sign**, per co-primary; t = 1000 is the grid's own eval. Consequence accepted in advance: on a null Γ, chance flips read UNSTABLE. Ratified as built. |
| (v) | Γ₄ sample and threshold | **JOINT k = 72 vs ISO-4 k = 20<!-- N:DES-3 --><!-- N:DES-13 -->**, SE `sqrt(s_J²/72 + s_4²/20)`, "rejects" and "CI includes 0" at z_α = 2.2365. (Γ null, Γ₄ rejects positive) stays UNREGISTERED. Ratified as built. |
| (vi) | Γ_H reading | **As (i), at z_α = 2.2365.** Ratified as built. |
| (vii) | primary k | **k = 72 stays primary**; the registered-ladder k = 60<!-- N:DES-1 --> prefix is reported beside it, UNDERPOWERED-flagged. |
| (viii) | re-evaluate the 144 T\* = 1000 checkpoints on the post-unblind card | **YES.** […] |

The 144 checkpoints of (viii) are the 72 seeds of each confirmatory arm<!-- N:DES-3 -->. Branch $A_c$ of (ii) is in Appendix E; (viii) produced the single-card curve of Appendix H.

**9. The secondary specification** (ratified 2026-09-26, after unblinding and before the sweep was read<!-- N:DX-413 -->):

> (S1) PAVA + OLS slope CI; (S2) single-hinge breakpoint, UNDERPOWERED iff the CI spans {0.125 … 0.375}<!-- N:DX-28 -->; (S3) plane fit, bound = 95 % CI of 0.5·γ_n; (S4) training co-activity over updates 1…1000, VOID iff the first-stage CI contains 0; (S5) the same-card replicate is ADDED, beside Γ₄, unable to change its qualifier; (S6) 95 % intervals, Γ₄′ at z_α. […]

The omitted words name the code version, which identifies the repository.

### E The registered outcome branches

"Positive" and "null" mean rejection or non-rejection in the confirmatory family (Γ on completion and on survival) at θ\*, Šidák m = 2, graded on the grid's own per-arm seed dispersion; "−" means rejection with negative sign (Appendix D, item 8 (i)). Branches A–D were registered on 2026-08-13<!-- N:DES-12 --> with a framing each; the registered table's fifth column, a venue lean, is omitted here. $A_c$ was registered on 2026-09-26<!-- N:DX-405 -->, before the look, for a cell the table did not contain.

| branch | completion | survival | headline claim, as registered ($A_c$: its registered claims, summarized) |
|---|---|---|---|
| A | + | + | founding registration, verbatim |
| B | null | + | composition is paid in **agents**, not task return |
| C | null | null | the instrument, and what it excludes |
| D | − on either co-primary | − on either co-primary | not separable from the matched-budget asymmetry |
| $A_c$ | + | null | the founding claim on the founding primary; the survival null quoted as an exclusion; no asymmetry claim |

The result is branch B, with the falsifier passing and the inert-share qualifier attached (§9.2).

### F Grid provenance

- **The grid.** 252 runs<!-- N:DX-30 -->, run from 2026-09-09 to 2026-09-22<!-- N:DES-12 -->: seeds 1–12 of all 10 arms on an RTX PRO 6000, then seeds 13–20 of all 10 arms and 21–46 of ISO and JOINT on an RTX 5090<!-- N:DX-30 -->. The 10 arms are ISO, JOINT and the 8 secondary arms.
- **The confirmatory artifact.** All 72 seeds of ISO and JOINT on one RTX 5090 unit: 76 runs executed there (seeds 1–12 and 47–72 of both arms<!-- N:DX-4 -->) plus seeds 13–46 copied from the grid<!-- N:DX-30 -->. The grid's RTX PRO 6000 seeds 1–12 were superseded and enter only a descriptive card diagnostic.
- **Secondary arms.** Seeds 1–12 of the 8 secondary arms were re-run on the same unit, 96 runs<!-- N:DX-30 -->; seeds 13–20 come from the grid. Every analysed secondary run is on unit 1.
- **Other blocks.** ISO-4 (20 seeds<!-- N:DES-13 -->) and the T = 2000 subsample (4 seeds per arm<!-- N:RES-15 -->) trained on a second RTX 5090 unit; the post-unblind evaluations ran on a third<!-- N:HW-4 -->.
- **Seeds.** Every arm uses the same seed integers; seed 0 is reserved for floors and never enters the grid<!-- N:DX-416 -->; runs are ordered seed-major, so that an interruption leaves a smaller balanced design rather than a complete arm beside an empty one; and the grid ran in chunks that end on seed boundaries, so both arms of a seed share a card. Tests in `che/tests/test_p6_grid.py` assert each property.
- **Archives.** Every checkpoint was archived off the rented machine as a compressed archive with a sha256 recorded beside it, and the job scripts fail a run whose archive or hash is missing. A re-verification on 2026-09-27 matched every recorded hash, 615 of 615<!-- N:DX-408 -->. No hash is quoted here.
- **What grades nothing.** A partial re-floor on a second rented card on 2026-08-14 (8 ISO and 4 JOINT evaluated reps, card not recorded<!-- N:DX-36 -->) is provenance only; of its 12 archives, one has a recorded hash<!-- N:DX-408 -->.

### G Throughput

The paper states no environment-only throughput figure. Under the compiler's dead-code elimination, an environment-only figure depends on which outputs its consumer reads, so any such figure would have to state its keep-alive set; none is needed here. The only cost figures are training measurements: 518–521 s per 1000-update training run and 9–10 s per 512-episode evaluation on one RTX 5090<!-- N:DX-4 -->, at 32,768,000 environment steps per run<!-- N:DX-3 -->, each step advancing all 12 agents<!-- N:ENV-6 -->.

### H Gamma(t) over the final half

**Sign unstable over the final half**, on both co-primaries<!-- N:RES-11 -->: the registered rule (Appendix D, item 2; ruling (iv) in item 8) requires all 11 point estimates to share one sign, and neither co-primary meets it. The tables are in rates (four decimals); intervals are Šidák-corrected at the family level, registered at t = 1000 and descriptive at every t < 1000, where no test is registered. Checkpoints t < 1000 were evaluated on the post-unblind unit; t = 1000 is the grid's own evaluation. Across cards at T\*, 280 of 288 paired evaluations are identical<!-- N:HW-3 -->, and the curve with t = 1000 re-evaluated on the post-unblind unit has the same signs on both metrics.

Completion, k = 72 per arm<!-- N:DES-13 -->:

| t | Γ(t) | sd(Γ) | Šidák CI | sign |
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

Survival rate, k = 72 per arm<!-- N:DES-13 -->:

| t | Γ(t) | sd(Γ) | Šidák CI | sign |
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

The signs read `+ − + + − − − − − − −` on completion and `+ − − + + + + + + + +` on survival<!-- N:RES-11 -->. On survival, only t = 900, 950 and 1000 have intervals excluding zero<!-- N:RES-12 -->; on completion, only t = 750<!-- N:RES-13 -->. These describe the trajectory of the arm-mean difference; they are not tests, and no trend is fitted to them.

### I The secondary design

Everything here is secondary and **non-verdict-bearing**. Intervals are 95 %, bootstrap over seeds within arm (B = 2000<!-- N:DX-28 -->), conditional on the common evaluation draw, and there are many of them, none family-corrected. Each arm has k = 20 seeds<!-- N:DES-13 --> on the confirmatory unit, with δ off. The per-coupling marginal is written $\mu$ and the fire-only share $\nu$ (Figure 13 labels them m and n); on the simplex $\nu = 1 - 2\mu + p$.

| arm | per-coupling marginal $\mu$ | co-occurrence $p$ | fire-only share $\nu$ |
|---|---|---|---|
| `sweep_c50_p000` | 0.5<!-- N:DES-9 --> | 0<!-- N:DX-28 --> | 0<!-- N:DES-9 --> |
| `sweep_c50_p125` | 0.5<!-- N:DES-9 --> | 0.125<!-- N:DX-28 --> | 0.125<!-- N:DES-9 --> |
| `sweep_c50_p250` | 0.5<!-- N:DES-9 --> | 0.25<!-- N:DX-28 --> | 0.25<!-- N:DES-9 --> |
| `sweep_c50_p375` | 0.5<!-- N:DES-9 --> | 0.375<!-- N:DX-28 --> | 0.375<!-- N:DES-9 --> |
| `sweep_c50_p500` | 0.5<!-- N:DES-9 --> | 0.5<!-- N:DX-28 --> | 0.5<!-- N:DES-9 --> |
| `ident_c40_p000` | 0.4<!-- N:DES-9 --> | 0<!-- N:DX-28 --> | 0.2<!-- N:DES-9 --> |
| `ident_c40_p200` | 0.4<!-- N:DES-9 --> | 0.2<!-- N:DX-28 --> | 0.4<!-- N:DES-9 --> |
| `ident_c40_p400` | 0.4<!-- N:DES-9 --> | 0.4<!-- N:DX-28 --> | 0.6<!-- N:DES-9 --> |

`sweep_c50_p000` carries exactly ISO-4's training mixture. Sweep means at θ\*, by $p$ = 0, 0.125, 0.25, 0.375, 0.5: survival 0.9241 / 0.9249 / 0.9261 / 0.9264 / 0.9289; completion 0.7847 / 0.7775 / 0.7797 / 0.7656 / 0.7749<!-- N:DX-28 -->.

| estimate (points) | survival | completion |
|---|---|---|
| dose slope, sweep, per unit $p$ (separate OLS fit) | +0.89 [−0.33, +2.11]<!-- N:SEC-5 --> | −2.51 [−9.43, +4.12]<!-- N:DX-27 --> |
| endpoint, $p$ = 0.5 minus $p$ = 0 | +0.48 [−0.21, +1.17]<!-- N:SEC-5 --> | −0.97 [−4.82, +2.87]<!-- N:DX-27 --> |
| $\gamma_p$, per unit co-occurrence | +3.26 [+1.37, +5.02]<!-- N:SEC-1 --> | +2.69 [−6.75, +12.45]<!-- N:DX-27 --> |
| $\gamma_n$, per unit fire-only share | −2.37 [−4.19, −0.57]<!-- N:SEC-1 --> | −6.52 [−15.34, +2.42]<!-- N:DX-27 --> |
| bound, $0.5\,\gamma_n$ | −1.19 [−2.10, −0.28]<!-- N:SEC-2 --> | −3.26 [−7.67, +1.21]<!-- N:DX-27 --> |
| knee | 0.375 [0.125, 0.375]<!-- N:DX-28 -->, UNDERPOWERED<!-- N:SEC-6 --> | 0.375 [0.125, 0.375]<!-- N:DX-28 -->, UNDERPOWERED<!-- N:SEC-6 --> |
| plane prediction, ISO-4 − ISO (from $\gamma_n$) | +0.79<!-- N:SEC-3 -->; measured B̂ +0.98 [+0.33, +1.63]<!-- N:RES-7 --> | not drawn in Figure 13, and no value stated |
| plane prediction, JOINT − ISO-4 (from $\gamma_p$, at $p$ = 1<!-- N:DES-7 -->) | +3.26<!-- N:SEC-4 -->; measured Γ₄ −0.03<!-- N:RES-6 -->, Γ₄′ +0.13<!-- N:RES-8 --> | +2.69 ($\gamma_p$ × 1)<!-- N:DX-27 --><!-- N:DX-417 -->; measured Γ₄ −1.26<!-- N:RES-6 -->, Γ₄′ −2.47<!-- N:RES-8 --> |

The plane is $y = \gamma_0 + \gamma_p p + \gamma_n \nu$, fitted by seed-level least squares over all eight arms; the bound is the no-element confound's share of the sweep's endpoint change. In the plane the slope along the sweep is $\gamma_p + \gamma_n$; the sweep's own slope in the first row is a separate least-squares fit, so the two need not agree (on completion they do not). Linearity is assumed and checked only coarsely: arm-mean residuals from the plane lie within ±0.4 SE on survival and ±1.1 SE on completion, 8 points for 3 parameters<!-- N:DX-39 -->.

**The same-card replicate** (S5), at $z_\alpha$ for Γ₄′ and 95 % for the replicate difference:

| metric | Γ₄′ = JOINT − `sweep_c50_p000` | `sweep_c50_p000` − ISO-4 (cross-card) |
|---|---|---|
| completion | −2.47<!-- N:RES-8 -->, z −1.50, Šidák [−6.16, +1.22]<!-- N:DX-19 --> | +1.21 [−2.79, +5.20]<!-- N:DX-19 --> |
| survival | +0.13, z +0.41, Šidák [−0.56, +0.81]<!-- N:RES-8 --> | −0.15 [−0.86, +0.56]<!-- N:RES-9 --> |

Arm means: ISO-4 0.7726 (completion) and 0.9256 (survival); `sweep_c50_p000` 0.7847 and 0.9241<!-- N:DX-18 -->.

**Mediation: VOID.** The first-stage slope of realized training dose on $p$ is −1.03 × 10⁻⁵ per unit $p$, 95 % [−2.91 × 10⁻⁵, +0.93 × 10⁻⁵]<!-- N:DX-29 -->; its interval contains zero, so by the registered rule mediation is VOID<!-- N:SEC-7 -->. The counter behind the dose counts collapse-seeded ignitions near alive agents, which Coupling A produces with or without Coupling B, so in mixtures it tracks the A marginal that the sweep holds fixed.

**What this instrument is blind to.** Linearity in $(p, \nu)$ is an assumption, tested only by the coarse residuals above. Per-coupling marginal, co-occurrence and active share cannot all be held fixed on the simplex, and $\gamma_p$ moves single-stressor mass into both-stressor episodes, which also raises per-coupling exposure. Floors exist only for the sweep endpoint, $p$ = 0.5: the intermediate arms assume it, and the identification arms are ungraded<!-- N:DX-306 -->. Realized dose is endogenous; nothing here is a causal effect of it.

### J Trained-policy episodes

Figures J1 and J2 show one pre-selected episode of each confirmatory arm, separately. The selection rule was fixed before any render and chooses nothing from a set: θ\*, episode key 0, stochastic actions, training seed 1 at update 1000 of each arm<!-- N:ENV-13 -->. The explorers illustrate the environment under a trained policy; they grade nothing. The measured contrasts are in §9.2. Figure J1 shows the ISO policy's episode.

<figure class="l-page">
  <iframe src="{{ 'assets/html/submission/explorer_thetastar_iso_s1_T1000_ep0.html' | relative_url }}" width="100%" height="720" style="border:none" title="Episode explorer, ISO policy, training seed 1" loading="lazy"></iframe>
  <figcaption><strong>Figure J1.</strong> One pre-selected episode of the ISO policy (training seed 1, update 1000) at θ&#42; (β 0.49, κ<sub>A</sub> 0.06, κ<sub>B</sub> 1.0, δ 1.0<!-- N:CAL-3 --><!-- N:CA-1 --><!-- N:CB-1 --><!-- N:COM-6 -->), episode key 0<!-- N:ENV-13 -->, on the 64 × 64 grid with 12 agents over 256 steps<!-- N:ENV-6 -->. The map layers are the fire state, the smoke density ρ (the environment's field, not what any agent sees), weak and collapsed floor, collapse-seeded ignitions, food, and agents alive or dead. Selecting an agent shows three 9 × 9<!-- N:ENV-6 --> panels for that step: its observation as produced, the true state of the same cells, and the probability that each cell was seen, τ, the Beer–Lambert transmittance. The figure shows one episode of one training seed; it carries no alive count, completion or return, and it cannot show any difference between training protocols. Any drift towards a wall late in an episode is the known artifact of §10, not a behaviour of interest. <span class="figure-note">Status: illustrative · ISO policy, training seed 1 · grades nothing · Interact: play or pause (space), step (← →, shift for 10), scrub, change speed; jump between collapse events and seeded ignitions with [ and ]; select an agent by clicking its marker or pressing 1–9; toggle layers. Opens at t = 128<!-- N:DX-410 -->.</span></figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/explorer_thetastar_iso_s1_T1000_ep0_static.png" class="img-fluid" alt="Maps of one ISO-policy episode at its start, middle and end, with one agent's observation, the true state of the same cells, and the probability each cell was seen" caption="Static companion of Figure J1 for the printed PDF." %}
</div>

Figure J2 shows the JOINT policy's episode under the same rule. The two figures are deliberately not placed side by side: a single episode of a single seed cannot carry a contrast that §9.2 measures over 72 seeds per arm and a common set of 512 evaluation episodes<!-- N:DES-3 --><!-- N:DES-13 -->, and nothing in either episode is offered as evidence for or against it.

<figure class="l-page">
  <iframe src="{{ 'assets/html/submission/explorer_thetastar_joint_s1_T1000_ep0.html' | relative_url }}" width="100%" height="720" style="border:none" title="Episode explorer, JOINT policy, training seed 1" loading="lazy"></iframe>
  <figcaption><strong>Figure J2.</strong> One pre-selected episode of the JOINT policy (training seed 1, update 1000) at θ&#42; (β 0.49, κ<sub>A</sub> 0.06, κ<sub>B</sub> 1.0, δ 1.0<!-- N:CAL-3 --><!-- N:CA-1 --><!-- N:CB-1 --><!-- N:COM-6 -->), episode key 0<!-- N:ENV-13 -->, on the 64 × 64 grid with 12 agents over 256 steps<!-- N:ENV-6 -->. The layers and panels are those of Figure J1: the map's smoke layer is the environment's field ρ, and only the observation panel shows what the selected agent perceives. The figure shows one episode of one training seed; it carries no alive count, completion or return, and it cannot show any difference between training protocols. <span class="figure-note">Status: illustrative · JOINT policy, training seed 1 · grades nothing · Interact: as Figure J1 (play, step, scrub, speed; [ and ] for events; click or 1–9 for an agent; layer toggles). Opens at t = 128<!-- N:DX-410 -->.</span></figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/explorer_thetastar_joint_s1_T1000_ep0_static.png" class="img-fluid" alt="Maps of one JOINT-policy episode at its start, middle and end, with one agent's observation, the true state of the same cells, and the probability each cell was seen" caption="Static companion of Figure J2 for the printed PDF." %}
</div>
