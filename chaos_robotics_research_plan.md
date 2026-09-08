# From "Chaos" to a Robotics Paper

A plan for turning the compound-hostile-environment idea into the strongest possible robotics paper, plus a set of independent paper ideas that use only the chaos framing.

---

## 1. The framing, stated once

Most robotics environments make the *task* hard and the *environment* passive. The chaos framing inverts this: the environment is the primary adversary, but it is not an adversary in the game-theoretic sense. It is **ambient**: a fixed stochastic process that stacks hazards, degrades the robot's own capabilities, and runs on a clock.

Three properties define a chaotic environment in this sense:

1. **Hazard stacking.** Multiple hazards are active at once and interact causally (collapse seeds fire, fire produces smoke, smoke blinds sensors). The interactions are non-additive.
2. **Ability degradation.** The robot's sensors, actuators, or energy budget decline as a function of exposure. The robot's capabilities are non-stationary within an episode.
3. **Survival is not rewarded.** Reward references task variables only. The robot learns to survive because death truncates future return, not because survival is shaped in.

The CHE project proved that (1) and (3) can be made formally precise. The robotics paper's job is to add (2) and embodiment.

---

## 2. Design rules that separate research from noise

These apply to every idea in this document. They are the answer to "isn't it just RNG?"

- **Decision variance must dominate luck variance.** Hazards must be partially observable or predictable so that the agent's choices move the outcome. A rockfall you cannot see coming teaches nothing; a rockfall that is more likely under a visibly cracked ceiling is a decision problem. Measure this: run a random policy and a trained policy on the same seeds; if the outcome distributions overlap heavily, the environment is too random.
- **Time or dose pressure is mandatory.** Without it the degenerate solution is to hide. A mission clock, a radiation dose budget, a battery that drains faster under load, or a hazard that eventually reaches everywhere all work.
- **Severity defined by dynamics, not knobs.** CHE calibrated severity by percolation phase (sub/near/super-critical), not by picking arbitrary parameter values. Keep this. It is the single most reviewer-proof design choice in the whole project.
- **Nested ablations.** Every hazard axis must be switchable to zero, producing a strictly simpler environment. This is what lets you attribute effects.
- **Distributional metrics.** Mean return is wrong when survival is bimodal. Report survival rate, task completion conditional on survival, CVaR at a stated α, and time-to-first-loss curves. Report over many seeds.
- **At most two couplings per paper.** CHE had three axes and one (comms) was certified inert. Two well-characterized couplings beat three where one does nothing.

---

## 3. The direct successor paper: "Does the compositional gap survive embodiment?"

This is the paper CHE sets up. It is the highest-value option because only you can write it: you will have the abstract result in hand and can ask whether it predicts embodied behavior.

### Thesis

A policy trained on stacked hazards outperforms a policy trained on each hazard in isolation (Γ > 0), and the gap measured in the abstract gridworld predicts the gap measured in an embodied continuous simulation. The secondary question is which embodiment factor (dynamics, sensor physics, or capability degradation) changes the composition problem most.

### What to build

**Simulator.** Continuous 2D physics, 4 to 8 differential-drive agents. MuJoCo MJX or Brax keeps you in JAX and lets you reuse the CHE training pipeline. Isaac Lab is the alternative if you want later hardware realism, at the cost of leaving JAX. Do not build 3D unless a reviewer forces it; 2D with continuous dynamics is a large enough step from the grid.

**Hazard field.** Reuse the fire cellular automaton as a continuous field on a fine grid underlying the physics world. Smoke as a diffusing scalar field with emission and decay, exactly as in CHE Definition 6. This is deliberate: the hazard kernel stays the same object so that the abstract-to-embodied comparison isolates embodiment, not hazard dynamics.

**Three embodied couplings** (pick two for the main experiment, keep the third as an appendix ablation):

- **Coupling A, structural collapse → hazard.** Collapse events become physical obstacles that also seed fire. Load-triggered failure: floors that fail when too many robots stand on them. Same semantics as CHE.
- **Coupling B, smoke → sensor physics.** Replace the transmittance scalar with a physically motivated range-sensor model: Beer–Lambert attenuation on max range, plus scattering that produces dropout and false near-returns above a density threshold. This is the coupling that most changes with embodiment, because the policy now has to reason about *what kind* of corruption it is seeing, not just a dimmer observation.
- **Coupling C, heat → actuator and energy degradation.** New. Exposure to burning cells accumulates a heat state per robot that reduces maximum wheel torque and increases battery drain. Recovery is slow or zero. This is "ability degradation" from the original framing and is absent from CHE, so it is the paper's clearest novelty.

**Task.** Keep it simple and reward-independent: reach and hold a set of waypoints, or transport items between stations. The task must be achievable by a single robot so that swarm effects are a choice, not a requirement.

### Experiment design

1. **Replicate ISO vs JOINT in the embodied sim** at the same three severity regimes, same held-out-severity protocol, same pre-registered contrast. This gives Γ_embodied.
2. **Transfer question.** Plot Γ_grid against Γ_embodied across severities and across coupling subsets. Correlation is the headline figure. Either sign of result is publishable: positive correlation validates a cheap proxy, no correlation shows embodiment changes the composition problem.
3. **Embodiment decomposition.** Add embodiment factors one at a time to the gridworld (continuous dynamics only; sensor physics only; degradation only) and measure which one moves Γ. This is the mechanism section reviewers will ask for.
4. **Behavioral analysis.** Render trajectories and quantify emergent caution: distance kept from hazard front as a function of heat state, sensor-dropout rate at which agents slow down, retreat events. A short qualitative section with two or three figures.

### Minimal hardware validation

Not learning transfer. Just show the compound-degradation effect is physically real. Two or three cheap ground robots (TurtleBot 3 or similar), a room, a fog machine, and a lidar. Measure single-hazard vs stacked-hazard failure rates on a fixed scripted policy: fog alone, moving obstacles alone, fog plus moving obstacles. The non-additivity of failure rate is the claim. This is two weeks of work and moves the paper from "simulation only" to "validated in principle."

### Novelty verdict (audit, Sept 2026): OPEN

Compositional generalization in robotics is active but concerns task factors, not survival. CompoSuite (Mendez et al. 2022) recombines robot arm, obstacle, object and task descriptor; Gao et al. (Stanford, 2024) showed policies compose environmental factors, reaching 77.5% on unseen combinations vs 2.5% without composition-aware data collection. None compose causally coupled hazards that disable the agent. Vulcan (arXiv 2604.12831, April 2026) is the nearest domain neighbor: hazard-aware multi-agent navigation for indoor fire SAR with a VLM global planner; it places the hazard inside the planner, the boundary CHE already draws. No neighbor found for the abstract-to-embodied transfer question. Must cite: CompoSuite, Gao et al., Vulcan.

### Reviewer objections to preempt

- *"This is a gridworld with physics."* Answer with Coupling C and the sensor-physics model; both are impossible on the grid.
- *"Why fire?"* Because it has an exact phase structure you can calibrate against. Say this in one sentence and cite the percolation result.
- *"Where is the sim-to-real?"* The hardware experiment answers the narrow version. Do not claim more.
- *"Compositional generalization is known."* It is known for language and vision; for embodied multi-agent survival under coupled hazards it is not, and the transfer question is new regardless.

### Venue and timeline

RA-L with ICRA or IROS option. Roughly nine to twelve months after CHE is submitted: three months simulator and couplings, three months training and ablations, two months hardware and writing. Publish the CHE paper first; this paper cites it as the formal model.

---

## 4. Independent paper ideas using only the chaos framing

None of these depend on the CHE codebase. They are ordered roughly by how quickly they could be started.

### 4.1 Chaos as a stress test for foundation-model policies

**Thesis.** Vision-language-action models and other pretrained robot policies fail under stacked sensor degradation in ways that single-hazard benchmarks do not reveal.

**Build.** A test harness that applies physically motivated compound corruptions (fog + low light + rain on camera; scattering + dropout on lidar) to existing manipulation or navigation benchmarks. No training required; you evaluate released policies.

**Why it works.** Timely, cheap, high visibility, and the finding is almost certainly real. Non-additivity of failure across corruptions is the key figure.

**Risk.** Could be seen as "just a robustness benchmark." Mitigate by focusing on interaction effects rather than per-corruption accuracy.

**Venue.** RA-L, CoRL, or an ICRA workshop first for speed.

**Novelty verdict (Sept 2026): CROWDED, window closing.** STRONG-VLA (arXiv 2604.10055, April 2026) benchmarks 28 perturbation channels across text and vision; a second group evaluates 17 uncertainties across 4 modalities (arXiv 2510.00037); LIBERO-Plus and VLATest cover layout, viewpoint, lighting, sensor noise and language; joint-level physical faults are covered (arXiv 2606.10501). No paper found whose central claim is the interaction effect between physically co-occurring corruptions. Viable only as a fast workshop paper with non-additivity as the sole contribution.

### 4.2 Degradation-aware planning under a dose budget

**Thesis.** A single robot exploring a hazardous site with a depleting health budget (radiation dose, thermal exposure) should plan differently from a robot with a time budget alone; risk-sensitive planners that model degradation outperform time-only planners.

**Build.** Stochastic orienteering with a health state that affects future capability. Model-based planning (MCTS or MPC over a learned or known degradation model). Compare against time-budget-only baselines.

**Why it works.** Clean formal problem, direct application to nuclear decommissioning and disaster response, and a method contribution rather than an environment contribution.

**Risk.** The planning literature is crowded. The novelty is degradation coupling to capability, so make that the whole paper.

**Venue.** ICRA, RA-L.

**Novelty verdict (Sept 2026): MEDIUM; coupling must be the whole paper.** Minimum-dose planning is mature: DC-A* for decommissioning robots (Nucl. Sci. Eng. 2025), layered radiation costmaps (Robotics 2021), Rao-combined ABC for minimum-dose inspection paths (Nucl. Sci. Tech. 2023), and a 2021 review in Nucl. Eng. Technol. All treat dose as a cost to minimize. Total-ionising-dose degradation of electronics and cameras is documented but not modeled by any planner found. The open contribution is dose as capability degradation, not dose minimization.

### 4.3 Online self-model drift and recovery under continuous degradation

**Thesis.** A robot can estimate its own declining capabilities online (torque loss, sensor bias) and adapt its policy, extending damage-recovery work from discrete injuries to continuous decline.

**Build.** A quadruped or manipulator in simulation with progressive actuator degradation; a self-model that tracks capability drift; a policy that conditions on the estimated self-model. Cully et al. 2015 is the anchor citation; the extension is continuous, time-varying degradation rather than a single break.

**Why it works.** Strong story, single-robot so cheaper than swarm work, and directly addresses "ability degradation."

**Risk.** Needs a convincing degradation model. Use published motor thermal models rather than inventing one.

**Venue.** RA-L, Science Robotics if the hardware result is strong.

**Novelty verdict (Sept 2026): CROWDED. Drop as written.** Two 2026 quadruped papers already model motor thermal degradation: thermal-aware locomotion with a full-body thermal model in Isaac Gym, deployed on hardware (arXiv 2603.01631, March 2026), and a residual policy correcting for thermal state (arXiv 2605.27046, May 2026). Mixture-of-experts RL for fault-tolerant locomotion (arXiv 2606.25965, June 2026) and RMA (wear and tear as an adaptation target) close the rest. Surviving variant: *unobserved* drift, where the robot has no degradation sensor and must infer decline from behavior. That is a different paper.

### 4.4 Expendability economics in multi-robot systems

**Thesis.** When robots have heterogeneous survival probabilities, optimal task allocation deliberately sacrifices some robots (scouts, relays), and this can be learned or planned explicitly.

**Build.** A risk-sensitive task allocation problem where robots have known or estimated hazard exposure and the team objective is mission completion. Compare explicit sacrifice strategies to risk-neutral allocation.

**Why it works.** Novel framing, strong swarm-intelligence fit, ethically interesting in a way that gives the paper a discussion section.

**Risk.** Can drift into pure operations research. Keep robots embodied and hazards dynamic.

**Venue.** Swarm Intelligence journal, ANTS, or RA-L.

**Novelty verdict (Sept 2026): OPEN, one neighbor to position against.** Tihanyi et al. (arXiv 2103.01840) split multi-robot safe planning into single-agent stochastic reachability plus high-level task allocation, with the objective of maximizing the safety of *all* robots. That is the opposite objective, which makes it the ideal contrast baseline. Failure-aware coordination (arXiv 2508.02529, 2025) treats degradation and faults as disruptions to recover from, not resources to spend. No work found that explicitly optimizes sacrificing robots. Best independent second paper.

### 4.5 Caution as a transferable skill

**Thesis.** A policy trained across a curriculum of hazard intensities and types acquires a general "caution" behavior that transfers zero-shot to unseen hazard types.

**Build.** A family of hazards with different dynamics (fire, flood, gas, structural) sharing an observation interface. Train on a subset, test on held-out hazard types. Measure whether transfer is explained by shared low-level behaviors (slow down when observations degrade, keep distance from fronts).

**Why it works.** Connects to meta-learning and generalization literature with a robotics-specific claim.

**Risk.** "Caution" must be operationalized precisely or reviewers will call it vague. Define it as measurable behaviors before training anything.

**Venue.** CoRL, RA-L.

**Novelty verdict (Sept 2026): OPEN but underspecified.** Closest work is contextual RL for OOD generalization, e.g. SPARC (arXiv 2511.09737) on wind-perturbed MuJoCo and Gran Turismo 7. Nothing on cross-hazard-type transfer. Without an operational definition of caution, reviewers will read it as domain randomization under a new name.

### 4.6 Marine chaos: storm-coupled dynamics for surface vessels

**Thesis.** Wave fields that simultaneously perturb dynamics, degrade sensors (spray, motion blur), and constrain time (battery in high sea state) form a compound stressor for USVs analogous to fire for ground robots.

**Build.** Spectral wave model coupled to a vessel dynamics model; sensor degradation as a function of sea state; a navigation task with a time budget.

**Why it works.** Real application domain with few learning-based results, and the framing transfers cleanly.

**Risk.** Marine simulation fidelity is a rabbit hole. Use existing open models and do not build your own hydrodynamics.

**Venue.** RA-L, OCEANS, IROS.

**Novelty verdict (Sept 2026): CROWDED on control, open on compound coupling, low fit.** USV disturbance rejection and risk-aware RL are dense: distributional RL local planners under unknown currents (Lin, McConnell, Englot 2023), DRIQN for heteroscedastic sensor noise varying with sea state (arXiv 2512.00030), and a 2026 review (Sensors 26:2852). No work stacks dynamics, sensor and energy degradation under one sea-state variable, but fidelity cost is high and it reuses none of your assets.

---

## 5. Choosing between them

| Idea | Depends on CHE | Compute cost | Novelty (audited Sept 2026) | Fit to your skills | Time to first result |
|---|---|---|---|---|---|
| 3. Embodied compositional gap | Yes | Medium | Open | Very high | 6 months |
| 4.1 Foundation-model stress test | No | Low | Crowded, closing | Medium | 2 months |
| 4.2 Dose-budget planning | No | Low | Medium (coupling only) | Medium | 3 months |
| 4.3 Self-model drift | No | Medium | Crowded, drop | High | 5 months |
| 4.4 Expendability | No | Low | Open | High | 4 months |
| 4.5 Caution transfer | No | High | Open, vague | High | 6 months |
| 4.6 Marine | No | Medium | Crowded on control | Low | 8 months |

**Ranking after the audit.** Section 3 first, unchanged. 4.4 is the best independent second paper: cheap, no direct competitor, and a clean contrast target in Tihanyi et al. 4.2 is viable only if dose-to-capability degradation is the entire contribution. 4.1 is a fast workshop paper or nothing. Drop 4.3 as written. 4.5 and 4.6 only if the others fall through.

**Shelf life of this audit.** The STRONG-VLA and thermal-quadruped papers date from April through July 2026; six months earlier both ideas would have read as open. Re-run the novelty check immediately before committing to any second paper.

---

## 6. Pitfalls specific to how you work

From reading the CHE repository, three things to watch:

- **Protocol growth.** Pre-registration and locks are good. Locks on locks and red teams of red teams are how a project stalls one experiment short of its result. Set a rule: no new methodological document after the design is registered. New worries go in the limitations section.
- **Simulator fidelity.** The embodied paper will tempt you toward realistic fire, realistic smoke, realistic lidar. Every one of those is a month. Use the simplest physically motivated model that a reviewer would accept, and cite the model instead of deriving it.
- **Axis count.** Two couplings, characterized deeply, beat three with one inert. Decide which two before writing any code and state the third as future work.

---

## 7. Suggested sequence

1. **Now to +2 months.** Finish CHE. Run the grid, write, submit to Swarm Intelligence.
2. **+2 to +4 months.** While CHE is in review, build the embodied simulator and the sensor-physics model. Optionally draft 4.4 as a workshop paper (4.1 only if started immediately).
3. **+4 to +8 months.** Train ISO and JOINT in the embodied sim. Run the transfer analysis.
4. **+8 to +10 months.** Hardware validation, writing.
5. **+10 to +12 months.** Submit to RA-L.

By the end you would have a formal model paper, a robotics paper that validates it, and the chaos framing established as your research identity rather than a single project.
