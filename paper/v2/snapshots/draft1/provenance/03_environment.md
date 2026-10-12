# Provenance: sections/03_environment.md

Writer: W3. Checked against the section on 2026-10-11 with
`paper/v2/src/provenance_check.py 03_environment` (no snapshot label taken).

Counts (P3's method, `plans/P3.md` §5, as `STRUCTURE.md` §6 states it): prose
1,763 words against a budget of 1,600 (the demo's 2,391); Figure 4's caption,
with its include caption and status note, 79 words against a cap of 80.
Listings 1–3 are pasted from the stub's exact blocks (`che/env/env.py:298-358`,
`che/env/tasks.py:31-43`, `che/tests/test_coupling_b.py:131-142`); the build
reports them byte-identical.

"demo 03:n" is `paper/demo_beyond/sections/03_environment.md` line n. "TF" is
`docs/theory_foundations.md`, which is not edited (its errors are reported in
Open items).

| # | sentence (verbatim) | support | change from the demo, and why |
|---|---|---|---|
| 1 | 3 The environment | framing | kept (demo 03:3) |
| 2 | CHE is a grid world in which a team of agents forages while a fire burns; Figure 4 shows one step. | ENV-6; che/env/tasks.py:31-43; che/env/env.py:241-243 | edited: demo 03:5's first sentence kept and joined to the figure pointer; the demo's "This section states the environment formally, pairs each statement with the code that implements it, and gives the one instance used in every reported experiment." cut (LEN; P3-§6, meta-signposting) |
| 3 | Five numbered boxes in a row, collapse, hazard, smoke, agents and comms, with a Coupling A arrow from collapse into the hazard box, a Coupling B arrow from smoke down to an observation box drawn from the post-step state, and comms denial entering the comms box with no hazard input. | framing; paper/figures/MANIFEST.md:457-472 | kept (demo 03:7) |
| 4 | Figure 4. One environment step of CHE. | framing | kept (demo 03:7) |
| 5 | Collapse, fire, smoke, agents and communication are sampled in the order of Proposition 1. | docs/theory_foundations.md:55-58; CLAUDE.md:40-45; paper/figures/MANIFEST.md:459-464 | edited: demo 03:9 "Five kernels sampled from s to s′ in the order of Proposition 1: collapse, fire, smoke, agents, communication." reworded to fit the 80-word cap (STRUCTURE.md §8; LEN) |
| 6 | Coupling A (orange) carries c′ − c into the fire; Coupling B (blue) carries ρ′ into the observation, drawn from s′. | paper/figures/MANIFEST.md:464-468; docs/theory_foundations.md:38-44; che/env/env.py:298-358 | edited: demo 03:9's sentences on Coupling A and Coupling B shortened (cap); demo's "Each agent observes a 9 × 9 egocentric crop of the post-step state." cut (the figure prints it; ENV-6 is stated in §3.5) |
| 7 | The comms kernel takes δ and reads no hazard; T X reads the post-step h′ and c′, as in the code. | paper/figures/MANIFEST.md:468-470; docs/theory_foundations.md:42-44; che/env/env.py:159-173; che/env/env.py:352-358 | edited: demo 03:9's "the denial level δ enters the communication kernel, which has no hazard input" and "The agents kernel reads the post-step fields, T_X(x, a, h′, c′), as the code and Definition 1 do." shortened (cap) |
| 8 | Arrow colours are this figure's own. | framing; paper/figures/MANIFEST.md:464-468 | edited: demo "The arrow colours belong to this figure only; in the interactive figures orange is burning fire and blue marks agents." shortened (cap) |
| 9 | The reward is not drawn (Definition 2). | paper/figures/MANIFEST.md:459-472 | kept |
| 10 | Status: schematic, no data. | framing | edited: "· Interact: none (static figure)" cut; the status vocabulary is explained once under the hero (STRUCTURE.md §8, R4) |
| 11 | 3.1 State, kernel and step order | framing | kept |
| 12 | Definition 1 (Compound Hostile Environment). A CHE is a Dec-POMDP $\mathcal{M}_\theta = \langle I, \mathcal{S}, \{\mathcal{A}_i\}, T_\theta, R, \{\Omega_i\}, O_\theta, \gamma \rangle$ with a finite set of agents $I$ on a grid $G$, action sets $\mathcal{A}_i$, observation sets $\Omega_i$, reward $R$ (Definition 2), observation kernel $O_\theta$ and discount $\gamma$. | docs/theory_foundations.md:33-34; docs/theory_foundations.md:15-20 | kept (demo 03:13) |
| 13 | It is indexed by the environment configuration $\theta = (\beta, \kappa_A, \kappa_B, \delta)$: the fire's per-neighbour ignition probability $\beta$, the strengths $\kappa_A$ and $\kappa_B$ of Couplings A and B, and the communication-denial level $\delta$. | docs/theory_foundations.md:23-25; decision log, TITLE AND TERMINOLOGY RULINGS (docs/decision_log.md:5583) | kept (demo 03:13) |
| 14 | Its state space factors as | docs/theory_foundations.md:35-37 | kept (demo 03:13) |
| 15 | where $x \in \mathcal{X}$ holds the agents' positions $x_i \in G$, their alive flags $\alpha_i \in \{0, 1\}$ and the task state; $h \in \mathcal{H} = \{\mathrm{Fuel}, \mathrm{Burning}, \mathrm{Burnt}\}^G$ is the fire; $\rho \in \mathcal{P} = \mathbb{R}_{\ge 0}^G$ is the smoke field; $c \in \mathcal{C} = \{\mathrm{intact}, \mathrm{collapsed}\}^G$ is the structure; $k \in \mathcal{K}$ is the realized communication graph on $I$; and the last factor is the step index $t$, with horizon $T$. | docs/theory_foundations.md:38-53 | kept (demo 03:19) |
| 16 | The transition kernel factorizes as | docs/theory_foundations.md:55-58 | kept (demo 03:19) |
| 17 | and agent $i$'s observation is drawn from the post-step state, $o'_i \sim O^i_{\kappa_B}(\cdot \mid x', h', \rho', c', k')$. | CLAUDE.md:40-45; che/env/env.py:394-396 | kept (demo 03:28). Departs from TF:62-63, whose observation line is unprimed and omits ρ (OI-2 record item, reported in Open items; TF not edited) |
| 18 | The dependence of $T_H$ on the collapse increment $c' - c$ is Coupling A (§5); the dependence of $O^i_{\kappa_B}$ on the fire, through the smoke field $\rho'$ it produces, is Coupling B (§6). | docs/theory_foundations.md:286-296; docs/theory_foundations.md:344-374; che/env/env.py:298-358 | kept (demo 03:28) |
| 19 | A training mixture (§9.1) draws $\theta$ once per episode, at reset. | che/env/env.py:217-222; che/env/env.py:390 | edited: demo 03:28's "The weak-cell terrain that T_C reads is drawn at reset and fixed for the episode (§5), and" cut (§5's; LEN) |
| 20 | The slopes $\gamma_p$ and $\gamma_n$ (§9.2, Appendix H) are unrelated to this discount. | SEC-1; SEC-3; framing | edited; class A, C1 (knock-on): demo 03:28 "On notation: an unsubscripted γ is always this discount, while the subscripted γ_p and γ_n of §9 are the secondary design's slopes; Corollary 1 (§4) writes its critical exponents as numbers." becomes one clause; the exponent note goes with Corollary 1(3) |
| 21 | Proposition 1 (Well-posedness and Markov closure). For every $\theta$, the process $s_t = (x_t, h_t, \rho_t, c_t, k_t, t)$ under any joint policy is a Markov chain, and $\mathcal{M}_\theta$ is a well-defined Dec-POMDP: finite-horizon optimal joint policies exist, and the standard value definitions apply. | docs/theory_foundations.md:137-140 | kept (demo 03:30) |
| 22 | The proof (Appendix A) composes the five kernels in order. | docs/theory_foundations.md:142-151; paper/demo_beyond/sections/03_environment.md:32 | edited; class A, P2-9: the demo's proof (03:32) moves to Appendix A; this sentence names the one step it rests on |
| 23 | Because $\rho$ is real-valued the state space is not finite, but the states and observations reachable within the horizon form finite sets, and restricted to them $\mathcal{M}_\theta$ is a finite Dec-POMDP. | paper/demo_beyond/sections/03_environment.md:32; docs/theory_foundations.md:40-44; che/env/env.py:257; paper/v2/FINDINGS.md:50 | edited; class A, OI-2 and P2-9: this sentence keeps the reachable-state argument of the demo's proof (states and observations reachable within the horizon are finite; ρ starts at 0 and evolves deterministically). TF:151-153 says S and Ω_i are finite, false with ρ real-valued (record item, reported). Also cut: demo 03:34 "From one agent's point of view the fire looks like nonstationarity. Proposition 1 says that formally it is state, evolving under a stationary kernel, so the standard value definitions apply." (§1 carries it; LEN) |
| 24 | Remark 1 (Hardness). For two or more agents, the finite-horizon Dec-POMDP decision problem is NEXP-hard, and NEXP-complete when the horizon is below the number of states (Bernstein et al., 2002). | bernstein2002; paper/related_work_verification.md:249; paper/v2/citations/theory_cites.md:53-74 | edited; class A, C2: demo 03:36 "Bernstein et al. (2002) show that finite-horizon Dec-POMDPs are NEXP-complete." now carries the scope the support record verifies (two or more agents; NEXP-hard, NEXP-complete when the horizon is below the number of states) |
| 25 | This bounds the worst case over the class and says nothing about a particular instance; it licenses the expectation that no general exact planner will scale, which is why we learn policies rather than plan. | paper/v2/citations/theory_cites.md:76-81; paper_v2_prompt.md:144-148; from owner text (paper/finale.md:54-55) for the closing clause | edited; class A, C2 and P3-N2: demo 03:36 "With communication denied (δ > 0), a CHE does not reduce to a multi-agent POMDP, so this hardness applies; it is why we learn policies rather than plan." The δ clause is dropped (P3-N2) and "this hardness applies" becomes what the result licenses. TF:163-168 carries both defects (record item, reported) |
| 26 | Listing 1, the body of step, follows the factorization; the link graph is drawn on its own stream with no hazard argument, and the reward line reads only the task reward and the two death counts. | che/env/env.py:298-358 | edited: demo 03:38's line-by-line gloss cut, since the listing's numbered comments carry it (LEN) |
| 27 | In the listing, tl is the episode's $\theta$, and no configuration here uses the early frozen control branch. | che/env/env.py:318-322; che/env/env.py:297; che/env/config.py:165 (default "dynamic"; no file in che/configs sets hazard_mode, grep this session) | edited: demo 03:38's parenthetical "(`tl` is the episode's θ; the `frozen` branch is an early control that no configuration in this paper uses.)" made a sentence |
| 28 | The observation is then drawn from the new state on its own stream (che/env/env.py:394-396). | che/env/env.py:394-396 | edited: "on its own stream" added (code comment at :394-395); the demo cited :394-397 |
| 29 | Listing 1. One environment step in the order of Proposition 1. | che/env/env.py:298-358 | kept (demo 03:40) |
| 30 | 3.2 The fire and its smoke | framing | kept |
| 31 | Definition 3 (Fire kernel). Each cell is Fuel, Burning or Burnt. | docs/theory_foundations.md:175 | kept (demo 03:109) |
| 32 | At each step, independently for each ordered pair of a Burning cell $g$ and a Fuel von Neumann neighbour $g' \in N(g)$, the cell $g'$ ignites with probability $\beta$. | docs/theory_foundations.md:175-177 | kept (demo 03:109) |
| 33 | A Burning cell becomes Burnt after exactly one step, and Burnt is absorbing. | docs/theory_foundations.md:177-179 | kept (demo 03:109) |
| 34 | Fuel cells may also ignite spontaneously at rate $\iota \ge 0$ per step; CHE uses $\iota = 0$. | docs/theory_foundations.md:179-181; DX-1 | kept (demo 03:109) |
| 35 | Every episode starts from an all-Fuel grid with one Burning cell at a uniformly random position (che/env/env.py:241-243). | che/env/env.py:241-243 | kept (demo 03:111) |
| 36 | One uniform per cell and incoming direction realizes the per-edge Bernoulli variables of Proposition 2's coupling exactly (che/env/hazard.py:8-16; Appendix A), and cells outside the arena never burn. | che/env/hazard.py:8-16; che/env/hazard.py:29-36 | edited (STRUCTURE.md §7: the implementation-exactness argument's home is Appendix A; LEN): demo 03:111's "On every step the kernel draws one uniform per cell and incoming direction; these slots correspond one-to-one to the ordered pairs g → g′, so per-pair independence is exact. Because a Burning cell is Burnt one step later, each unordered edge sees at most one ignition attempt in a trajectory, so these uniforms realize the per-edge Bernoulli variables of Proposition 2's coupling exactly" becomes one sentence; "there is no wraparound" folded into "never burn" |
| 37 | Proposition 2 (Bond percolation). Under Definition 3 with $\iota = 0$ and a single ignition at the origin, the set of eventually-Burnt cells is equal in distribution to the open cluster of the origin in i.i.d. bond percolation on $(G, E)$ with edge-open probability $\beta$. | docs/theory_foundations.md:189-192 | kept (demo 03:113) |
| 38 | Here $E$ is the arena's set of von Neumann edges. | che/env/hazard.py:23-24; framing | kept (demo 03:115, reworded) |
| 39 | The proof (Appendix A) is a short coupling, the correspondence between an epidemic with a constant infectious period and bond percolation described by Grassberger (1983). | grassberger1983; paper/related_work_verification.md:283; paper/v2/citations/theory_cites.md:137-165; docs/theory_foundations.md:194-208 | edited: demo 03:115's "and it is what lets §4 define severity by percolation phase" cut (§4.1 says it; LEN) |
| 40 | Its hypotheses hold for CHE's fire when Coupling A is off, since collapses otherwise add ignitions. | che/env/env.py:241-243; DX-1; che/env/env.py:298-358 | edited: demo 03:115 "Its hypotheses hold for CHE's fire on its own. With Coupling A on, collapses can add ignitions during the episode, and the burnt set is then no longer one origin's cluster." merged into one sentence (LEN) |
| 41 | Smoke outlives flame. | CLAUDE.md:66-67 (D3) | kept (demo 03:117) |
| 42 | Per cell, | framing | kept (demo 03:117) |
| 43 | with emission $\sigma_s = 1.0$ and decay $\eta = 0.5$, held fixed by convention and never calibrated. | DX-1 | kept (demo 03:123) |
| 44 | A cell emits $\sigma_s$ once, in the step it burns, and its smoke then decays geometrically, with no spatial smoothing (che/env/hazard.py:67-79). | che/env/hazard.py:67-79; docs/theory_foundations.md:177-179 | edited: "The update reads the post-step fire h′, so" cut (the display shows h′); demo 03:123's "The smoke field is state, not what an agent sees: an agent sees only its crop of the state, attenuated by Coupling B through ρ′." cut (§3.5 gives the observation; LEN). Demo 03:125's stressor paragraph is folded into §3.4's table (LEN) |
| 45 | 3.3 Agents, deaths and a hazard-blind reward | framing | kept |
| 46 | The agents kernel $T_X(x' \mid x, a, h', c')$ acts in three deterministic stages that consume no random numbers (che/env/env.py:159-173). | che/env/env.py:159-173 | edited: demo cited :159-196; demo 03:129's last sentence "Death consumes no random numbers, so it cannot shift another kernel's stream." folded in (LEN) |
| 47 | An alive agent on a cell that collapses in this step is disabled before it moves. | che/env/env.py:161-164 | kept ("falls and" cut) |
| 48 | Survivors take one of 5 actions, stay or a von Neumann move clipped to the grid, and a move into a collapsed cell is cancelled. | ENV-8; che/env/env.py:68; che/env/env.py:165-167 | edited: "and Burnt cells are passable" cut (LEN) |
| 49 | An agent whose new cell is Burning in $h'$ is then disabled, so a cell igniting under a standing agent kills it; Burning cells can be entered, and avoidance must be learned. | che/env/env.py:168-171 | kept (demo 03:129) |
| 50 | A disabled agent stays disabled, holds still, collects nothing and disappears from the others' observations. | che/env/env.py:167; che/env/env.py:69-71; che/env/observation.py:35-36 | kept (demo 03:129; "vanishes from" → "disappears from") |
| 51 | Definition 2 (Ambient hazard). The hazard is ambient if and only if (i) and (ii) hold. | docs/theory_foundations.md:66-85; decision log, TITLE AND TERMINOLOGY RULINGS (docs/decision_log.md:5583) | kept (demo 03:131) |
| 52 | (i) Reward independence: the reward is a function of task variables and of the agents' alive transition only, | docs/theory_foundations.md:87-91; decision log, DEF. 2 WORDING RULING (docs/decision_log.md:5287) | kept (demo 03:133; the run-in label now ends in a colon, so it is one sentence) |
| 53 | where $\mathrm{task}(x)$ denotes the task variables (in CHE, the food grid and the alive agents' positions) and $d_p \ge 0$ is a fixed death penalty. | docs/theory_foundations.md:91-92; che/env/tasks.py:1-7 | kept (demo 03:139, first half) |
| 54 | No term of $R$ references $h$, $\rho$ or $c$, and the hazard appears in no auxiliary cost or constraint channel: no CMDP constraint, no Lagrangian penalty, no safety critic. | docs/theory_foundations.md:91-94; decision log, DEF. 2 WORDING RULING (docs/decision_log.md:5287) | kept (demo 03:139, second half; split at the semicolon for sentence length, P3-§6) |
| 55 | (ii) Non-adversarial: $T_H$ is a fixed stochastic kernel; nothing in the environment optimizes, learns or best-responds. | docs/theory_foundations.md:126-128 | kept (demo 03:141) |
| 56 | Under clause (i), survival is learned through two hazard-blind routes: a dead agent collects no further task reward, and each death costs a fixed $d_p = 0.5$, whatever its cause, in every configuration reported here (the code's default is 0). | ENV-1; decision log, DEF. 2 WORDING RULING (docs/decision_log.md:5287); docs/theory_foundations.md:94-96 | edited: "(the code's default is 0)" added (stub REQUIRED FACTS; ENV-1 note: `che/env/config.py:37` defaults to 0.0) |
| 57 | Fire and collapse reach return only through the transition and observation kernels. | docs/theory_foundations.md:98-101 | edited: demo 03:143's "never through the reward: the transition kernel disables agents and, for collapse, blocks moves; the observation kernel shows them to the agents, and through it Coupling B attenuates perception" cut (LEN; P3-§6, antithesis) |
| 58 | The penalty prices an outcome, not the hazard. | decision log, DEF. 2 WORDING RULING (docs/decision_log.md:5287); docs/theory_foundations.md:112-115 | kept (demo 03:143; the ruling's own words, log:5328-5329; this section's one contrast) |
| 59 | A hazard-priced reward signals the hazard's state whether or not anything is harmed: JaxWildfire, for example, penalizes its agent at every step in proportion to the number of burning cells (Çakır et al., 2025). | cakir2025jaxwildfire; paper/related_work_verification.md:941; docs/theory_foundations.md:116-117 | edited (reworded). Demo 03:143's next sentence "CHE's reward carries information about the fire only through outcomes the task also suffers." cut (it restates the routes; LEN) |
| 60 | At $d_p = 0$ only the first route would remain. | docs/theory_foundations.md:119-120; decision log, DEF. 2 WORDING RULING (docs/decision_log.md:5287) | kept (demo 03:143) |
| 61 | Listing 2's signature admits only the food and occupancy grids, so no fire, smoke or structure argument can reach the task reward. | che/env/tasks.py:31-43 | edited: demo 03:145's "Listing 1's reward line subtracts d_p times the sum of fire and collapse deaths, adding the two causes before pricing them." cut (the cause-blindness test carries it; LEN) |
| 62 | Listing 2. The task reward reads food and occupancy only. | che/env/tasks.py:31-43 | kept (demo 03:147) |
| 63 | Two tests check clause (i). | che/tests/test_reward_independence.py:1-15; che/tests/test_lethality.py:143-162 | kept (demo 03:166) |
| 64 | One asserts identical rewards, with and without the death penalty, for states that differ only in fire, smoke or structure, every difference far from all agents so that the alive transition is pinned equal (che/tests/test_reward_independence.py:6-15). | che/tests/test_reward_independence.py:6-15 | edited (shortened; LEN) |
| 65 | It shows only that the reward reads no hazard state directly, since the fire is meant to change return through deaths. | che/tests/test_reward_independence.py:6-12 | edited: demo's "which is all such a test can show" folded into "only" |
| 66 | The other kills a standing agent by fire and, separately, by collapse, with identical task state, and asserts a reward of $-d_p$ both times (che/tests/test_lethality.py:143-162). | che/tests/test_lethality.py:143-162 | edited (shortened; LEN) |
| 67 | Clause (i) also fixes how §9's two co-primary outcomes enter learning: survival is a penalized channel, each death costing $d_p$, and completion a rewarded one, each collected item earning +1. | ENV-1; ENV-9; paper/branch_B.md:182-183 | kept (demo 03:168, merged); "neither mentions the fire" cut (LEN) |
| 68 | §9.2 reads any asymmetry between them as one between a penalized channel and a rewarded one. | paper/branch_B.md:182-183; decision log, DEF. 2 WORDING RULING (docs/decision_log.md:5287) | edited (reworded): honesty line 6, whose home this is (BRIEF.md §6.2) |
| 69 | The one ablation of $d_p$ is from the calibration phase, with this scope: the fire alone with no coupling on, 500 updates, 3 seeds per cell, an observation encoding that predates the one used here, and means over the final training updates. | ENV-2; che/bench/results/phase2/phase2_report.md:27-37; decision log, DEF. 2 WORDING RULING (docs/decision_log.md:5287) | edited (reworded, scope unchanged; branch_B §5 line 6) |
| 70 | Raising $d_p$ from 0 to 0.5 moved High survival from 0.575 to 0.866 and High completion from 0.765 to 0.821, moved Medium survival from 0.931 to 0.951 with completion 0.750 at both, and left Low tied, 0.991 against 0.992. | ENV-1; ENV-2; ENV-3; ENV-4; ENV-5 | kept (demo 03:170; the 0 now carries ENV-2's tag) |
| 71 | It was not re-run under the current observation or with the couplings. | decision log, DEF. 2 WORDING RULING (docs/decision_log.md:5287) | kept (demo 03:170) |
| 72 | Clause (ii) does not make the hazard independent of the agents: a weak cell with an agent on it is nine times as likely to collapse in a step as an empty one, and a collapse can seed fire (§5.1). | CA-8; docs/theory_foundations.md:129-133 | edited; class A, LEN and N16 (the influence numbers' home is §5.1, where OI-4 resolves): demo 03:172 "An agent standing on a weak cell raises that cell's per-step collapse probability ninefold, and a collapse can seed fire. Most collapses happen with no agent present: agent load adds 0.4–1.4 % to the number of collapses per episode under trained policies (Phase-3 policies, 500 updates) and 7.4–8.3 % under random ones. The environment is non-adversarial in the formal sense, a fixed kernel with no objective, but it is not agent-independent (§2)." becomes one sentence and a pointer; "ninefold" is scoped as CA-8's note requires (load is boolean: occupied against empty) |
| 73 | 3.4 Nested models: ablations are exact by construction | framing | kept |
| 74 | Each stressor is a parameter of one transition or observation kernel, and setting it to zero recovers a nested special case of the same model. | docs/theory_foundations.md:659-661; CLAUDE.md:46-51 | edited: demo 03:176 "Each stressor is a parameter of one kernel, and setting it to zero recovers a nested special case of the same model, never a different environment." now says "one transition or observation kernel" (κ_B is in the observation kernel; the wording of finding N9) and drops the antithesis (P3-§6) |
| 75 | stressor / parameter / lives in / off ($=0$) recovers / asserted by | framing | kept (demo 03:178) |
| 76 | Coupling A (Definition 5, §5) / $\kappa_A$ / $T_H$, through $c' - c$ / a fire blind to the structure / che/tests/test_nesting.py | docs/theory_foundations.md:665; che/tests/test_nesting.py:78-98 | edited: "(Definition 5, §5)" added; demo 03:125's stressor paragraph folded into the table (LEN) |
| 77 | Coupling B (Definition 6, §6) / $\kappa_B$ / $O^i$ / the observation before masking, plus an all-ones visibility plane / Listing 3 | che/tests/test_coupling_b.py:118-121; che/env/observation.py:24; docs/theory_foundations.md:666 | edited; class B, new finding (Open items, W3-F2): demo cell "perception independent of the hazard" (from TF:666, "hazard-independent perception") becomes what the test asserts, the pre-masking observation plus an all-ones visibility plane; the burning plane still shows the fire at κ_B = 0. "(Definition 6, §6)" added |
| 78 | communication denial (Definition 7, §7) / $\delta$ / $T_K$ / free, range-limited communication / che/tests/test_comms.py | docs/theory_foundations.md:667; che/tests/test_comms.py:72-79 | edited: "(Definition 7, §7)" added |
| 79 | The fire's $\beta$ is a parameter of the same kind, positive in every configuration and set by severity (§4). | CLAUDE.md:62-63 (D1); docs/theory_foundations.md:664 | edited (shortened; LEN) |
| 80 | One engineering rule makes the nesting exact: every stochastic branch draws its uniforms unconditionally and compares them against a probability that may be zero. | CLAUDE.md:46-51; che/env/hazard.py:3-6 | edited: "no draw is gated on a parameter's value" cut (it restates; LEN) |
| 81 | The draws for Coupling B's reveal, the links and the per-episode mixture use streams derived from the reset or step key by a fixed tag, so adding them left the existing streams untouched. | che/env/env.py:50-67 | kept (demo 03:186, reworded) |
| 82 | Setting a stressor to zero therefore changes comparisons only, and the same keys reproduce the nested model's trajectory bit for bit. | CLAUDE.md:46-51; docs/theory_foundations.md:670-672 | edited: demo's "changes comparisons, never which random numbers are drawn" and "with no re-implementation or re-tuning of a separate environment" cut (P3-§6, antithesis; LEN) |
| 83 | Listing 3 runs the environment at $\kappa_B = 0$ with and without masking, under the same keys, and asserts bitwise-identical fire, smoke, structure, food, positions, alive flags and rewards. | che/tests/test_coupling_b.py:131-142 | edited: "the test for Coupling B" cut; "with the masking observation and with the observation that predates masking" → "with and without masking" (LEN) |
| 84 | The rest of the test (che/tests/test_coupling_b.py:143-156) steps both by hand and asserts identical content planes, an all-ones visibility plane and a zero masked share. | che/tests/test_coupling_b.py:143-156 | edited; class A, KB-2: Listing 3 is shortened to :131-142, so the hand-stepped check (:143-156) is one sentence citing its range (demo 03:188's second sentence, reworded) |
| 85 | Listing 3. With $\kappa_B = 0$, trajectories and rewards are bitwise those of the environment before masking. | che/tests/test_coupling_b.py:131-142 | edited: demo label "With κ_B = 0, the environment is bitwise the one without Coupling B." now says what the shortened listing asserts (state trajectories and rewards; the observation gains a constant plane) |
| 86 | With $\kappa_A = 0$, collapse activity leaves the fire and smoke bitwise unchanged (che/tests/test_nesting.py:78-88); at $\delta = 0$, the environment reproduces, on the CPU, a trajectory digest recorded before the communication channel existed (che/tests/test_comms.py:272-319). | che/tests/test_nesting.py:78-88; che/tests/test_comms.py:272-319; che/tests/test_comms.py:279-287 | edited: "The other two nestings have tests of the same kind." cut; "on the CPU" folded in from the demo's last sentence (LEN) |
| 87 | A structural test also asserts that the traced computation keeps its random-number primitives at parameter value zero, catching a gate such as if kappa_A > 0: that behavioural tests miss (che/tests/test_nesting.py:222-240). | che/tests/test_nesting.py:222-240 | edited (reworded); demo 03:222's "These tests run in the CPU suite; the digest is checked on the CPU only, since the smoke exponential is not bit-identical across backends." cut, its fact kept as "on the CPU" (LEN) |
| 88 | 3.5 The instance, training and metrics | framing | kept |
| 89 | Every trained policy and evaluation in this paper uses one instance: a 64 × 64 grid, 12 agents, a horizon of 256 steps, a 9 × 9 egocentric crop and 32 food items. | ENV-6; che/configs/p6_joint.yaml:11-16 (all live configs in che/configs carry the same five values, checked this session) | edited; class B, new finding (Open items, W3-F3): demo 03:226 "Every reported experiment uses one instance" is contradicted by the calibration (L = 32, 48, 64, no agents; DX-7) and one Proposition 3 test (L = 32; CA-3); scoped to trained policies and evaluations |
| 90 | Food sits on distinct cells from reset and does not respawn, and an alive agent on a food cell collects it for a team reward of +1. | che/env/tasks.py:24-28; che/env/tasks.py:31-43; ENV-9 | edited: "agents start on uniformly random cells" cut (LEN) |
| 91 | The observation's 8 channels are six indicators (burning, burnt, food, weak, collapsed, alive occupancy), the raw smoke density and Coupling B's visibility plane, which marks the revealed cells. | ENV-7; che/env/observation.py:3-10; che/env/observation.py:22-36 | edited: "so that unseen can be told from absent; an agent's own cell is always revealed" cut (Coupling B's observation is §6's; LEN) |
| 92 | An own-state vector gives the agent's row and column over $L$, its alive flag and $t$ over the horizon. | ENV-7; che/env/observation.py:56 | kept (demo 03:226; split at the semicolon; "divided by" → "over") |
| 93 | All agents share one actor-critic network over the crop, the own-state vector and the aggregate of delivered messages. | ENV-10; che/train/networks.py:75-93 | kept (demo 03:228; lead shortened) |
| 94 | It has two convolutions with 16 and 32 channels, a dense layer of 128 units, and separate actor and critic heads with a 64-unit layer each. | ENV-10; che/train/networks.py:87-110 | kept (demo 03:228, split) |
| 95 | A message head receives no gradient, so what it emits is a frozen-at-initialization projection of trained trunk features (§7). | ENV-12; che/train/networks.py:27-36 | edited: "that neighbours receive one step later" cut (§7's) |
| 96 | Training is the independent PPO of de Witt et al. (2020), in the PureJaxRL style of Lu et al. (2022), on the environment conventions of JaxMARL (Rutherford et al., 2024). | dewitt2020ippo; paper/related_work_verification.md:472; lu2022dpo; paper/related_work_verification.md:453; rutherford2024jaxmarl; paper/related_work_verification.md:372 | kept (demo 03:230, reworded) |
| 97 | Each seed trains one shared-parameter policy, and each agent's transitions are independent samples under the team reward. | ENV-11; che/train/ippo.py:4 | kept (demo 03:230, split and reworded) |
| 98 | Each update collects 128 steps from 256 parallel environments, 32,768 environment steps, each advancing all 12 agents. | DX-2; DX-3; ENV-6 | kept (demo 03:230) |
| 99 | ISO, ISO-4 and JOINT (§9) each train for T\* = 1000 updates, or 32,768,000 environment steps, with the hyperparameters of Appendix B. | DES-13; DX-3; DX-2 | edited; class B, new finding (Open items, W3-F4): demo "A run lasts T* = 1000 updates (a training budget, not the episode horizon T), 32,768,000 environment steps, identical for every arm of §9. The other hyperparameters, the same for every run, are in Appendix B." The four-seed T = 2000 runs of §9 and the calibration-phase runs are not 1000 updates, and DX-2 covers Phase-6 runs; scoped to ISO, ISO-4 and JOINT as DX-3 states; the antithesis cut (P3-§6) |
| 100 | The co-primary outcomes of §9 are per-episode. | DES-12 | edited: demo 03:232 "Two per-episode metrics are the co-primary outcomes of §9." shortened (LEN) |
| 101 | Completion is $1 - F/32$, where $F$ is the number of food items left at the episode's last step; survival rate is the fraction of the 12 agents alive at the end. | ENV-6; che/env/env.py:446-447 | edited (merged; LEN) |
| 102 | Episodes always run to the horizon, even when every agent has died (che/env/env.py:361; che/eval/harness.py:44-45). | che/env/env.py:361; che/eval/harness.py:44-45 | edited (shortened; LEN) |
| 103 | Deaths are also recorded by cause, as diagnostics. | che/eval/harness.py:46-47 | edited: "fire or collapse" and "the reward does not distinguish them" cut (Definition 2 says it; LEN) |

## Open items

New findings made while writing, and what could not be sourced. Classes as in
`paper/v2/BRIEF.md` §1; class B items are applied in the section with the
demo's wording quoted in the row, class C items are not applied.

- **W3-F1, record (OWNER ITEM 2; class C, Q4k).** `docs/theory_foundations.md:151-153`
  says "$\mathcal{S}$, $\mathcal{A}$, and $\Omega_i$ are finite, so
  $\mathcal{M}_\theta$ is a finite Dec-POMDP"; with
  $\mathcal{P} = \mathbb{R}_{\ge 0}^G$ in the state (TF:40-44, :49-50) and the
  raw smoke density in the observation (ENV-7), neither set is finite. The
  argument holds on the states and observations reachable within the horizon,
  which is what v2 says (row 23; the proof is Appendix A's). Also
  TF:62-63: the observation line $O^i_{\kappa_B}(o_i \mid x, h, c, k)$ is
  unprimed and omits ρ, while `CLAUDE.md:40-45` and `che/env/env.py:394-396`
  draw it from the post-step state with ρ′ (v2 row 17 follows the code).
  Direction: a dated note in TF, or the paper's departure note in Appendix A
  (W6). TF not edited.
- **W3-F1b, record (C2; class C, Q4k).** TF:163-168, Remark 1: "so the
  hardness framing applies" and "With comms denial ($\delta > 0$) the CHE does
  not collapse to an MPOMDP". Both are gone from v2 (rows 24–25); TF not
  edited.
- **W3-F2, accuracy (class B, applied; also a TF record item, class C).**
  The nested-model table's Coupling B cell said κ_B = 0 recovers "perception
  independent of the hazard" (demo 03:181, from TF:666 "hazard-independent
  perception"). At κ_B = 0 the crop still carries the burning, burnt and smoke
  planes (`che/env/observation.py:24-26`); what the test asserts is the
  pre-masking observation plus an all-ones visibility plane
  (`che/tests/test_coupling_b.py:118-121`). v2's cell says that (row 77).
  TF:62-64 ("the dependence of the observation kernel on $h$ is Coupling B")
  has the same looseness; v2's Definition 1 keeps the demo's "through the
  smoke field ρ′ it produces". Direction: owner confirms the cell; TF note
  optional.
- **W3-F3, accuracy (class B, applied).** Demo 03:226 "Every reported
  experiment uses one instance": the severity calibration ran at L = 32, 48
  and 64 with no agents (DX-7) and one Proposition 3 test runs at L = 32
  (CA-3). v2 scopes it to trained policies and evaluations (row 89); every
  live config in `che/configs/` carries the instance (checked by grep this
  session; `debug.yaml` and the archival `m06_probe.yaml` differ).
- **W3-F4, accuracy (class B, applied).** Demo 03:230 "identical for every
  arm of §9" and "The other hyperparameters, the same for every run": the
  four-seed T = 2000 runs of §9.2 train 2000 updates (RES-15), the
  calibration-phase runs 500 (ENV-2), and DX-2 records the hyperparameters of
  the Phase-6 runs. v2 scopes the budget to ISO, ISO-4 and JOINT, as DX-3
  does (row 99).
- **W3-F5, owner choice (class C).** Row 56 adds "(the code's default is 0)",
  which the stub lists as a required fact (ENV-1 note). It tells a re-runner
  that the configs, not the defaults, carry d_p = 0.5. Direction: keep, or
  move it to Appendix B or §11.
- **Cross-references not yet resolvable.** "§5.1" (row 72) and Definitions 5,
  6 and 7 (rows 76–78) point into W4's sections, which were stubs when this
  file was checked; the build lists them as unresolved until W4's headings and
  definitions exist.
- **Budget.** Prose is 1,763 words, 10 % over the 1,600 target (the
  tolerance edge). The cuts came from restatement and code glosses; no
  required fact, honesty line or listing was cut.
- **Not stated, no source needed a row.** The message delay ("received one
  step later", demo 03:228) and the reward test's six-cell distance
  (`che/tests/test_reward_independence.py:10`) were cut rather than given new
  rows. Every number in the section carries a canonical-ledger or supplement
  tag; no new ledger row was needed (no `ledger_proposals/W3.md`).
