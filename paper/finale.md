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
---

We introduce the Compound Hostile Environment (CHE), a pure-JAX multi-agent reinforcement-learning environment in which a cellular-automaton fire burns in every episode, structural collapse can add ignitions to it, and its smoke attenuates the agents’ perception, alongside an independent communication-denial axis. The fire is an ambient hazard: a fixed stochastic process with nothing in it optimizing against the agents, carried by no cost or constraint channel, and invisible to the reward, which reads only task variables and agent deaths and prices every death the same whatever its cause. Severity levels are placed relative to a measured percolation threshold, and each stressor is a parameter of one transition kernel, so ablations are bitwise-exact nested models; we also describe a measurement protocol in which reproducibility floors are measured per metric, per GPU and per artifact. As predicted before measurement, the supercritical fire consumes the fuel that collapse would ignite: under trained policies, collapse-seeded ignitions per episode fall 4.8-fold<!-- N:CA-4 --> from low to high severity. We then pre-register a test of whether training on co-occurring stressors beats training on each in isolation, at a held-out severity and matched compute, with 72<!-- N:DES-3 --> seeds per arm (above the registered seed ladder’s cap of 60<!-- N:DES-1 -->, a recorded deviation made before unblinding). Joint training raises survival by 0.96<!-- N:RES-2 --> points (Šidák-corrected 95 %<!-- N:DES-13 --> CI [0.47, 1.44]<!-- N:RES-2 -->); task completion shows no detectable change (−1.73<!-- N:RES-1 --> points, CI [−4.12, +0.66]<!-- N:RES-1 -->). Neither joint-versus-isolated difference keeps a stable sign over the final half<!-- N:RES-11 --> of training: the survival gap opens only in the last fifth<!-- N:RES-12 --> of the budget, and completion leans negative from 70 %<!-- N:RES-13 --> of it onward. The survival gain does not survive an inert-share correction registered before unblinding. Because communication denial is inert under our frozen random-projection message encoder at this scale, a third<!-- N:DES-8 --> of the isolated arm’s training episodes contain no active stressor. Removing them, in a 20<!-- N:DES-13 -->-seed sensitivity arm, raises isolated training’s survival by 0.98<!-- N:RES-7 --> points; joint training then differs from it by −0.03<!-- N:RES-6 --> points (CI [−0.68, +0.63]<!-- N:RES-6 -->), although it still sees each coupling twice<!-- N:DES-14 --> as often and always in combination. Studies of compositional generalization should therefore match the share of training that contains an active stressor before attributing a gain to composition.

## 1 Introduction

When a training distribution has to cover several stressors, its designer
chooses whether the policy meets them together or one at a time, and the choice
matters most when the stressors interact. Ecology and climate science study the
interactive and cumulative effects of multiple stressors (Crain et al., 2008)
<!-- cite:crain2008stressors --> and the risk from compound events (Zscheischler
et al., 2018) <!-- cite:zscheischler2018compound --> as objects in their own
right. In reinforcement learning the same choice is a question of
generalization: must a policy see stressors co-occur during training to cope
with their co-occurrence at test time? It has been studied for imitation-learned
manipulation (Gao et al., 2024) <!-- cite:gao2024composition -->, and it belongs
to the wider problem of zero-shot generalization (Kirk et al., 2023)
<!-- cite:kirk2023zsg -->. We study it for survival in multi-agent
reinforcement learning, in an environment where agents are killed by fire and by
structural collapse, two of the stressors are coupled to the fire, and a third
acts independently.

Where the hazard sits in the learning problem shapes what such a comparison can
teach. In some fire-related work the hazard is the task itself, as for a team of
aerial robots fighting forest fires (Haksar & Schwager, 2018)
<!-- cite:haksar2018 -->. In safe and constrained reinforcement learning it
enters a cost or a constraint. <!-- no verified bib entry for CMDP / safe RL
yet; add one via related_work_verification.md --> In the Compound Hostile
Environment (CHE) it does neither. The fire is an *ambient hazard*
(Definition 2): a fixed stochastic process with nothing in it optimizing against
the agents, carried by no cost or constraint channel, and invisible to the
reward. The reward reads task variables and agent deaths, and prices every death
at the same fixed penalty, 0.5 <!-- N:ENV-1 -->, whatever its cause. Agents
therefore learn to survive only from outcomes: a dead agent collects no further
task reward, and each death costs the penalty. A hazard that acts only through
the dynamics is not new in itself. What it gives this study is a comparison in
which no reward or cost signal mentions the hazard in either arm. Agents meet
the fire only through what they observe and what happens to them, so the arms
differ only in what their training distributions show the agents. From one
agent's point of view the fire looks like nonstationarity. Proposition 1 shows
that it is state: the full process is a Markov chain and the environment is a
finite Dec-POMDP, so the standard value definitions apply. With communication
denied, the problem does not reduce to a multi-agent POMDP, and finite-horizon
Dec-POMDPs are NEXP-complete (Bernstein et al., 2002)
<!-- cite:bernstein2002 -->, which is why we learn policies rather than plan.

CHE is built to answer the training question as a measurement. A
cellular-automaton fire burns in every episode. For the idealized kernel, the
burnt region is exactly a bond-percolation cluster (Proposition 2; Grassberger,
1983; Kesten, 1980) <!-- cite:grassberger1983 --> <!-- cite:kesten1980 -->, so
severity has a natural definition: three levels <!-- N:CAL-3 --> placed below,
near and above a *measured* percolation threshold of the implemented kernel,
rather than at arbitrary parameter values. Two stressors are coupled to the
fire. Structural collapse can add ignitions (Coupling A), and smoke attenuates
each agent's egocentric observation by Beer–Lambert transmittance (Coupling B).
A third, the denial of inter-agent links (δ), is independent of it. Each
stressor is a parameter of one transition or observation kernel, and every
stochastic branch consumes its random numbers whether or not its stressor is
on. Switching a stressor off therefore reproduces the nested model's
trajectories bit for bit: ablations are exact by construction. Calibrating the
environment produced findings that stand without any training comparison
(§§4–7).

The training question is then posed as a pre-registered test. An isolated arm
(ISO) trains one policy on a mixture of single-stressor configurations, and a
joint arm (JOINT) trains one on configurations with every stressor on. Both
train at a low and a high severity (β = 0.43 and 0.70) <!-- N:CAL-3 --> and are
evaluated at the near-critical severity, β = 0.49 <!-- N:CAL-3 -->, which
neither saw. Architecture and compute are matched: single-policy IPPO (de Witt
et al., 2020) <!-- cite:dewitt2020ippo -->, one policy per training seed <!-- N:ENV-11 -->. The
co-primary outcomes are task completion and survival, Šidák-corrected for two
tests <!-- N:DES-13 -->. The four possible outcomes <!-- N:DES-12 -->, a
framing for each, and a falsifier for the asymmetric outcome were registered on
2026-08-13 <!-- N:DES-12 -->, before the grid began on 2026-09-09
<!-- N:DES-12 -->; survival had been made a co-primary on 2026-08-02
<!-- N:DES-12 -->. We ran 72 seeds per arm <!-- N:DES-3 -->, above the
registered seed ladder's cap of 60 <!-- N:DES-1 -->, a recorded deviation made
before unblinding (§9.1). The comparison has a known weakness, which we state
before the result: JOINT sees each coupling three times as often as ISO
<!-- N:DES-7 -->, so the endpoints differ in dose as well as in co-occurrence. A
secondary design holds each coupling's frequency fixed while co-occurrence
varies, a split in the spirit of DBCA (Keysers et al., 2020)
<!-- cite:keysers2020 -->. It cannot also hold the share of fire-only episodes
fixed, which rises with co-occurrence <!-- N:DES-9 -->, and it is not
verdict-bearing (§9). The founding hypothesis, that joint training improves both
outcomes, did not occur.

At the held-out severity, joint training raises survival by 0.96 points
(Šidák-corrected 95 % CI [0.47, 1.44]) <!-- N:RES-2 --> <!-- N:DES-13 -->.
Task completion shows no detectable change: −1.73 points, CI [−4.12, +0.66]
<!-- N:RES-1 -->, which excludes a joint-training gain larger than 0.66 points
<!-- N:RES-1 -->. The registered falsifier for an asymmetric result passes
<!-- N:RES-5 -->, so the asymmetry stands. Under Definition 2 it is an asymmetry
between a penalized channel, deaths, and a rewarded one, the task. Neither
joint-versus-isolated difference keeps a stable sign over the final half of
training <!-- N:RES-11 -->: the survival gap opens only in the last fifth of the
budget <!-- N:RES-12 -->, and the completion difference leans negative from 70 %
of it onward <!-- N:RES-13 -->.

The survival gain does not survive the inert-share correction. Communication
denial is inert under our frozen random-projection message encoder at this
scale (§7), so the third of ISO's training episodes that carry only δ
<!-- N:DES-8 --> carry no active stressor. We registered this bias, and an arm
to remove it, on 2026-09-18 <!-- N:DES-15 -->, before unblinding. That arm,
ISO-4, is ISO without its δ-only episodes: a sensitivity arm outside the
confirmatory family, trained with 20 seeds <!-- N:DES-13 --> <!-- N:DES-15 -->.
Its survival is 0.98 points above ISO's <!-- N:RES-7 -->, and JOINT's survival
differs from ISO-4's by −0.03 points (CI [−0.68, +0.63]) <!-- N:RES-6 -->. As
the registration requires, we do not describe the survival advantage as a
composition effect. Two limits apply. First, the corrected contrast's upper
bound, +0.63 <!-- N:RES-6 -->, lies above the uncorrected contrast's lower
bound, +0.47 <!-- N:RES-2 -->, so the correction excludes a large composition
effect, not every composition effect. Second, removing the δ-only episodes
changes two things at once: the share of training with an active stressor rises
from two thirds to all of it <!-- N:DES-8 --> <!-- N:DES-14 -->, and each
coupling's frequency rises from a third to a half of episodes <!-- N:DES-7 -->
<!-- N:DES-14 -->. The 0.98-point rise cannot say by itself which of the two
matters; §9.2 reports what the secondary design adds on this question, including
where its fit fails. What the corrected contrast does say is that, once the
active share is matched, JOINT's remaining differences add nothing detectable to
survival: it sees each coupling twice as often as ISO-4 <!-- N:DES-14 --> and
always in combination.

The argument behind this result is general, although we measured it in one
environment: a comparison of joint and isolated training that leaves the active
share free can report an active-share effect as a composition effect. What
separates this work from earlier joint-versus-isolated comparisons is what the
comparison holds fixed. In the literature search described in §2, which read
abstracts and did not query IEEE Xplore, we found no reinforcement-learning
comparison that matches its arms on how much of training carries any stressor.

We do not claim convergence guarantees for the training procedure, or a theorem
that joint training wins: Proposition 4 bounds what isolated training can be
*guaranteed* to transfer, not what it does, and Theorem 1 concerns adaptivity
against memorization in a two-corridor toy. We do not claim an exact critical
value for the implemented kernel, whose threshold is measured. Nor do we claim
that the survival gap is robust to the training budget, since its sign is not
stable over the final half of training.

Our contributions are:

1. **An environment built as an instrument.** CHE places a lethal fire in the
   transition and observation kernels only (Definition 2), factorizes each step
   into collapse, fire, smoke, agents and communication (Proposition 1), defines
   severity by measured dynamical phase, and makes every ablation a
   bitwise-exact nested model. Its theory doubles as unit tests: the
   implementation reproduces Proposition 3's linear scaling, Theorem 1's value
   curve and Remark 2′'s value of communication (§§3–7).
2. **Calibration findings that stand without the training comparison.** As
   predicted before measurement, the supercritical fire consumes the fuel that
   collapse would ignite: under trained policies, collapse-seeded ignitions
   fall 4.8-fold from low to high severity <!-- N:CA-4 -->, while the share of
   them near agents stays flat <!-- N:CA-6 --> (§5). Smoke attenuation costs
   survival at high severity, replicated in direction three times out of three
   <!-- N:CB-5 -->, and the masking concentrates 16–118-fold on moments of
   danger <!-- N:CB-10 --> (§6). At the medium severity used for the test, its
   own measured effect on survival was −0.03 points, graded only against a
   three-seed spread <!-- N:CB-9 --> (§10). Communication is inert under our
   frozen random-projection encoder at this scale (§7).
3. **A measurement protocol in which acceptance bars come with floors.**
   Reproducibility floors are measured per metric, per GPU and per artifact;
   contrasts are graded on their own standard error; and design-stage power is
   stated as the minimum effect detectable with 80 % power
   <!-- N:METH-7 --> at the family-corrected α (§8).
4. **A pre-registered test of joint against isolated training.** Its survival
   advantage does not survive a correction registered before unblinding, and it
   points to a rule whose argument is general: match the active share before
   attributing a gain to composition (§9).

## 2 Related work

This section says, for each line of work, where it places the hazard and what
its comparisons hold fixed. §1 stated what our comparison holds fixed; how we
searched is described at the end.

**Where the hazard enters learning.** In multi-agent wildfire fighting the
hazard is the objective. Haksar & Schwager (2018) <!-- cite:haksar2018 -->
train aerial agents with a multi-agent deep Q-network and reward them for moving
to burning trees on the fire's boundary (their Algorithm 2); the paper gives the
fire no way to harm them. JaxWildfire (Çakır et al., 2025)
<!-- cite:cakir2025jaxwildfire | read in full 2026-10-10 by an assistant -->, a
JAX cellular-automaton wildfire simulator, trains a single air-tanker agent
whose reward is a per-step penalty proportional to the number of burning cells,
with a bonus for full extinction; the paper does not describe harm to the agent.
Safe reinforcement learning, which García & Fernández (2015)
<!-- cite:garcia2015safe --> define as learning policies that maximize return
while ensuring reasonable system performance and/or respecting safety
constraints, typically places a hazard in a constraint or a cost. VULCAN (Liu &
Yan, 2026) <!-- cite:liu2026vulcan -->, a proposed multi-robot fire
search-and-rescue approach planned by a vision-language model rather than
learned, folds smoke, heat and sensing uncertainty into a hazard cost map; its
preliminary evaluation covers baselines, not the approach itself. Its evaluation
metric is also abbreviated CHE (cumulative hazard exposure), which is unrelated
to our environment's name. In CHE no reward, cost or constraint reads the fire
(Definition 2); the reward prices deaths, whatever their cause.

**A hazard that feeds on itself.** Coupling A lets structural collapse add
ignitions. The nearest neighbour we found is Raut et al. (2026)
<!-- cite:raut2026psps | read in full 2026-10-10 by an assistant -->, who model
public-safety power shutoffs as a single-agent decision problem: the power
flows that follow from the operator's switching decisions set the failure
probability of lines in wildfire areas, which the authors treat as ignition
risk. Their reward is negative operating cost, and there is no spatial spread
model. CHE's agents influence the hazard too, but weakly and indirectly. An
agent standing on a weak cell raises that cell's collapse rate nine-fold
<!-- N:CA-8 --> (Definition 5), but most collapses happen with no agent present:
under trained policies, agents add about one percent to the number of collapses
per episode, and about seven percent under random policies <!-- N:CA-9 -->. A
collapse may then seed fire. So we do not claim that CHE's hazard grows without
agent influence. The difference from Raut et al. is one of directness and size:
there the controlled decision sets the failure probability, while here ignition
is not an action available to the agents, and where they stand moves the
collapse count only slightly.

**Perception degraded by the hazard.** Coupling B attenuates each agent's
observation by Beer–Lambert transmittance along the line of sight through smoke.
VULCAN degrades simulated sensing with smoke density and visibility loss and
infers smoke density from image degradation and depth consistency, but it has
no transmittance model. JaxWildfire's observations are partial and egocentric
but not attenuated. In the search described below, we found no
reinforcement-learning environment whose observation kernel attenuates by
transmittance.

**Simulators and benchmarks in JAX.** CHE follows JaxMARL's environment
conventions (Rutherford et al., 2024) <!-- cite:rutherford2024jaxmarl --> and
trains with independent PPO (de Witt et al., 2020) <!-- cite:dewitt2020ippo -->.
Among the JAX multi-agent benchmarks we surveyed, JaxMARL, Multi-Agent Craftax
(Al Omari et al., 2025) <!-- cite:alomari2025macraftax --> and Assistax
(Hinckeldey et al., 2025) <!-- cite:hinckeldey2025assistax -->, none has an
evolving, spreading lethal hazard field or perception attenuated by a hazard.
Multi-Agent Craftax comes closest in kind: its agents lose health to hunger and
enemies and can die, but its lava is static terrain that agents cannot enter.
In Crafter and in Craftax-Classic, the JAX reimplementation described alongside
Craftax, lava is lethal; and Crafter and Craftax reward each health point
regained and penalize each one lost (Hafner, 2022; Matthews et al., 2024)
<!-- cite:hafner2022crafter --> <!-- cite:matthews2024craftax -->, pricing an
outcome rather than the hazard, much as our reward prices each death. POBAX
(Tao et al., 2025) <!-- cite:tao2025pobax --> is a single-agent suite for
partial observability, and BenchMARL (Bettini et al., 2024)
<!-- cite:bettini2024benchmarl --> is a multi-agent benchmarking library built
on TorchRL rather than JAX. JaxWildfire has a spreading fire in JAX, with one
agent.

**Choosing a training distribution.** Domain randomization trains on a broad,
fixed distribution over simulator parameters so that the deployed setting looks
like one more sample (Tobin et al., 2017) <!-- cite:tobin2017dr -->; Muratore
et al. (2022) <!-- cite:muratore2022drreview --> review the approach.
Unsupervised environment design adapts the distribution to the learner instead.
PAIRED generates environments from a regret objective (Dennis et al., 2020)
<!-- cite:dennis2020paired -->; Prioritized Level Replay revisits levels by
their estimated learning potential (Jiang et al., 2021a)
<!-- cite:jiang2021plr --> and was later recast as environment design (Jiang et
al., 2021b) <!-- cite:jiang2021robustplr -->; and ACCEL evolves levels near
the frontier of the agent's ability (Parker-Holder et al., 2022)
<!-- cite:parkerholder2022accel -->. These methods ask which distribution to
train on, usually adaptively. We compare two fixed distributions and evaluate
no adaptive curriculum (§10). Kirk et al. (2023) <!-- cite:kirk2023zsg -->
survey zero-shot generalization in reinforcement learning, the broader problem
our held-out test belongs to.

**Compositional generalization over environmental factors.** The closest
earlier study of our question is Gao et al. (2024)
<!-- cite:gao2024composition | read in full 2026-10-10 by Claude and by the
owner -->. In visual imitation learning for robotic manipulation, they ask
whether policies compose environmental factors, such as object type and
position, table texture and height, and camera position, to succeed on unseen
combinations, and they use the answer to design data collection. One of their
strategies varies a single factor at a time from a base setting; another cycles
through factors so that more combinations appear. They compare strategies at a
matched number of demonstrations, across levels of a rough effort proxy, the
number of factor changes (their §III-C and §IV-A). Policies do compose, more
weakly when both factors are physical (their §V-B), and the strategy that covers
more combinations does better. Their design is built for data efficiency, not
to separate co-occurrence from how often each factor value appears. Ours matches
compute and, in the ISO-4 correction, the share of training that carries any
stressor. The settings differ too: their factors change what the robot sees and
must do, while two of our stressors are causally coupled to a lethal hazard and
the third is independent of it; their policies are learned by imitation, ours
by multi-agent reinforcement learning. CompoSuite (Mendez et al., 2022)
<!-- cite:mendez2022composuite --> studies compositional multi-task
reinforcement learning over robots, objects, objectives and obstacles, which is
composition of tasks, not of co-occurring stressors. The DBCA method of Keysers
et al. (2020) <!-- cite:keysers2020 --> builds splits whose atom distributions
are similar and whose compound distributions differ. Our secondary sweep follows
that idea, holding each coupling's frequency fixed while co-occurrence varies;
our ISO and JOINT endpoints do not (§1, §9).

**Mixed and simultaneous perturbations.** Robust reinforcement learning asks the
same question about perturbations. Erdem & Üre (2025)
<!-- cite:erdem2025mixed | read in full 2026-10-10 by Claude (publisher's
version of record) --> train single-agent continuous-control policies against a
learned adversary that perturbs observations, actions, or both; in their
formulation the adversary acts at every step (their §3.4 and Algorithm 1). From
their Tables 3–4 they report that agents trained against one modality remain
vulnerable to simultaneous attacks on both. Agents trained against their
balanced mixed adversary also do better under single-type attacks than agents
trained against a naive mixed adversary (their Table 5). No arm in their
comparison trains on a mixture of single-type attacks: each single-type arm
never meets the other modality, and the mixed arms carry the combined budget,
which the authors note is more severe. Because every arm is perturbed
throughout, their design has no counterpart of the fire-only share our
correction removes. What it bundles is how much each arm sees of each modality,
whether it sees them together, and a larger budget. That is nearer to what our
corrected contrast leaves in, where JOINT still sees each coupling twice as
often as ISO-4 <!-- N:DES-14 -->, though unlike ISO-4 their single-type arms
see the other modality not at all. Their result is therefore not a test at
matched per-modality exposure, and it neither supports nor contradicts our
corrected null. Agrawal et al. (2023) <!-- cite:agrawal2023multimodal --> train
multi-agent policies against random reward, state and action noise with a
curriculum that raises the noise level, one or two noise types at a time; the
curriculum sets training length, so exposure differs between their models. In
supervised vision, Tramèr & Boneh (2019) <!-- cite:tramer2019multiple --> and
Hsiung et al. (2023) <!-- cite:hsiung2023compositional --> study robustness to
multiple and to composite perturbations.

**Theory.** Chen et al. (2022) <!-- cite:chen2022understandingdr | read in full
2026-10-10 by Claude, main text and Appendix G --> model domain randomization as
returning the optimal history-dependent policy of a latent MDP, a set of fully
observed MDPs that differ in their transitions, and bound its shortfall against
the optimal policy of the true MDP. Every upper bound they prove assumes that
each MDP in the set is communicating, with bounded diameter. Without that
assumption, their Proposition 1 shows the shortfall can grow linearly in the
horizon: in their construction, per-step rewards follow an irreversible choice
among several branches made before anything distinguishes the candidate MDPs.
Theorem 1 here is kin to that construction but not covered by it. Its
two-corridor toy, with the signals encoded as states, has an absorbing failure,
so their diameter assumption fails and their upper bounds do not apply.
Proposition 1, for its part, says nothing about a toy with a single terminal
reward that can reveal the environment before the branch. Theorem 1 gives that
toy's exact optimal value as a continuous function of how much is revealed
before commitment, which perception attenuation controls. It also measures a
different gap: the adaptive optimum against the policy that is optimal when the
map is fixed, not against the optimum for a known environment. Its
no-information endpoint has the structure of Proposition 1's uninformed
commitment, with two branches. Chen et al. therefore do not subsume Theorem 1,
and Theorem 1 does not extend their bounds. For communication, Pynadath & Tambe
(2002) <!-- cite:pynadath2002 --> relate the complexity of team decision
problems with communication to observability. Free communication lowers the
complexity when the world is collectively observable (their Theorem 4 and
Table 2), and communication makes no difference when it is individually
observable or not observable at all (Theorems 5–6). Remark 2′ refines this for
collective partial observability: communication's marginal value vanishes when
interchangeable agents' views are redundant, and returns when roles are
irreplaceable or deaths are costly (§7). The survey of adaptability in
multi-agent reinforcement learning by Hu et al. (2025, revised 2026)
<!-- cite:hu2025adaptablemarl | the recommendation quoted is in v2 only -->
calls an environment family highly diagnostic if it "systematically varies"
factors such as population, observability or communication structure "while
holding other factors fixed". It mentions compositional generalization but does
not analyse shifts in several factors at once.

**How we searched.** We ran the literature search with the help of LLM-based
research assistants, between August and October 2026. A census of benchmark
venues and a search for theorems that could subsume ours came first; a search of
domain randomization, environment design, multi-task and robust-learning
neighbours followed. Both used web search and the arXiv API and read abstracts.
The works this section describes in detail were then read in full; the
remaining citations rest on their abstracts. We did not query IEEE Xplore.
Wherever this paper says that no work does something, it means no work found by
this search.
