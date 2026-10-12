<!-- PAPER V2 DRAFT (PAPER V2 ruling, 2026-10-11): builder-drafted, not owner-approved -->

## 3 The environment

<!-- STUB-SPEC
PURPOSE: State CHE formally and concretely: it is a well-defined Dec-POMDP, finite on its reachable states; its reward is hazard-blind and prices deaths cause-blind; the fire is a bond-percolation process with smoke as state; every ablation is an exact nested model; and the one instance, training and metrics used in every reported experiment.
SUBSECTIONS (H3, as the demo's): 3.1 State, kernel and step order; 3.2 The fire and its smoke; 3.3 Agents, deaths and a hazard-blind reward; 3.4 Nested models: ablations are exact by construction; 3.5 The instance, training and metrics.
WRITER: W3. BUDGET: 1,600 prose words (the demo's: 2,391); Figure 4 caption at most 80 words.
REQUIRED FACTS: ENV-1 (d_p = 0.5 in every configuration reported; the code default is 0.0); ENV-2 to ENV-5 (the d_p ablation, with its scope: the fire alone with no coupling, 500 updates, 3 seeds per cell, an observation encoding that predates the current one, means over the final updates; High survival 0.575 to 0.866, High completion 0.765 to 0.821, Medium survival 0.931 to 0.951 with completion 0.750 at both, Low tied 0.991 against 0.992; never re-run); ENV-6 (64 × 64, 12 agents, horizon 256, 9 × 9 crop, 32 food items); ENV-7 (8 channels: 6 indicators, smoke, visibility; own-state row/L, col/L, alive, t/horizon); ENV-8 (5 actions); ENV-9 (+1 team reward per item); ENV-10 (the network); ENV-11 (one shared-parameter IPPO policy per seed); ENV-12 (message head: no gradient, frozen at initialization); DX-1 (σ_s 1.0, η 0.5, ι 0, held by convention); DX-2 (256 parallel environments, 128 steps per update; the rest in Appendix B); DX-3 (32,768 steps per update; 32,768,000 per run); DES-13 (T* = 1000 updates); CA-8 (an occupied weak cell collapses nine times as often; one clause, pointer to section 5.1, which holds CA-9).
CODE FACTS (read this session; cite as file:line in provenance): single ignition at a uniformly random cell at reset (che/env/env.py:241-243); one uniform per cell and incoming direction realizes Prop. 2's per-edge variables exactly (che/env/hazard.py:8-16); smoke update per cell, no smoothing (che/env/hazard.py:67-79); agent kernel in three stages, collapse-kill before moving (che/env/env.py:159-166); episodes always run to the horizon (che/env/env.py:361); observation drawn from the post-step state on its own stream (che/env/env.py:394-396); completion and survival definitions (che/env/env.py:446-447; che/eval/harness.py:42-46); the reward-independence test pins the alive transition equal (che/tests/test_reward_independence.py:6-15); the cause-blindness test (che/tests/test_lethality.py:143-162).
CITATIONS: bernstein2002 (Remark 1, worst-case class result only), grassberger1983 (Prop. 2's correspondence), cakir2025jaxwildfire (the hazard-priced foil), dewitt2020ippo, lu2022dpo, rutherford2024jaxmarl.
FIGURES: Figure 4, the static schematic fig01_schematic.png (include plus a caption paragraph), carried from the demo below. Caption at most 80 words: the five kernels in the Prop. 1 order; Coupling A from c′ − c; Coupling B from ρ′ to the observation; δ with no hazard input; observation from s′; T_X reads the post-step fields as the code does; arrow colours belong to this figure only; the reward is not drawn. Width (l-page wrapper) is P2-4, class C: keep the demo's markup.
LISTINGS (carried below, exact lines; place each where your prose introduces it; keep the header line inside the fence; the label paragraph says what it proves): Listing 1, che/env/env.py:298-358 (one step in the Prop. 1 order; the reward line reads only the task reward and the death counts); Listing 2, che/env/tasks.py:31-43 (the task reward's signature admits food and occupancy only); Listing 3, che/tests/test_coupling_b.py:131-142 (κ_B = 0 reproduces the pre-masking environment bitwise in hazard, smoke, structure, food, positions, alive flags and reward; the hand-stepped observation check at lines 143 to 156 becomes one sentence citing that range). Your prose must not echo the internal tags inside the code (M4.1, obs v2, obs v3, Q3 ruling).
LATEX: Def. 1 (two displays: the state space; the factorized kernel with T_X(x′ ∣ x, a, h′, c′)); the post-step observation inline; Def. 2's reward formula (one display, with \lvert … \rvert); the smoke update (one display); the nested-model table (math cells without pipes). No \label, \eqref, \tag or \newcommand.
HONESTY LINES AND REGISTERED STRINGS: branch_B section 5 line 6 (home: an asymmetry between survival and completion is between a penalized channel and a rewarded one); "ambient hazard"; "environment configuration"; "stressor" only for the three elements; non-adversarial is not agent-independent.
FIX-LIST AND FINDINGS ITEMS OWNED: C2 (Remark 1 says what Bernstein et al. license: finite-horizon Dec-POMDPs are NEXP-complete in the worst case, so no general exact planner is expected to scale, which is why we learn policies; the "(δ > 0) … does not reduce to a multi-agent POMDP" clause is dropped, P3-N2); OI-2 (Prop. 1 stated with a one-sentence gloss: a well-defined Dec-POMDP, finite on its states reachable within the horizon; the proof moves to Appendix A, P2-9); C1 knock-on (drop the notation note about Corollary 1's exponents at the demo's 03:28; keep one clause that an unsubscripted γ is the discount and γ_p, γ_n are section 9's slopes, if section 9 uses the symbols); KB-2 (Listing 3 shortened); LEN (clause (ii)'s agent-influence numbers become one clause and a pointer to section 5.1); F5 (no milestone codes in prose; "the observation before masking" and "the masking observation", BRIEF section 5.2); P3-§6 (no "This section states" opening); Q4k.
STYLE: definitions and propositions as bold run-in paragraphs; otherwise no bold-led paragraphs; sentences of at most 40 words.
DEMO KEEPS (sections/03_environment.md): Def. 1 with ρ and t; Def. 2 with its formula, the hazard-blind against hazard-priced note, both tests and the d_p ablation with its scope; Def. 3; Prop. 2's statement; the smoke update; the agent-kernel paragraph; the nested-model table; the engineering rule; Listings 1 to 3 (Listing 3 shortened); the instance and the metrics. CHANGES: Prop. 1's proof to Appendix A; Remark 1 (C2); the agent-influence paragraph to a pointer. DROPS: the duplicate proof; the exponent note; signposting.
NOT HERE: "no shaping term", "solely", "hazard-free reward"; that the reward-independence test proves Def. 2 (it shows no direct read, with the alive transition pinned); that the hazard is independent of the agents; PBT; "swarm"; that smoke is spatially smoothed; that the Phase-6 runs used a different observation storage; any statement of Def. 5, 6 or 7 beyond one line each (their sections own them).
DEPENDENCIES: section 4 uses Prop. 2; sections 5 to 7 define their kernels; Appendix A holds the proofs of Props. 1 and 2 and the implementation-exactness paragraph; Appendix B holds the hyperparameters.
-->

CHE is a grid world in which a team of agents forages while a fire burns; Figure 4 shows one step.

{% include figure.html path="assets/img/submission/fig01_schematic.png" class="img-fluid" alt="Five numbered boxes in a row, collapse, hazard, smoke, agents and comms, with a Coupling A arrow from collapse into the hazard box, a Coupling B arrow from smoke down to an observation box drawn from the post-step state, and comms denial entering the comms box with no hazard input." caption="Figure 4. One environment step of CHE." %}

<p class="caption">Collapse, fire, smoke, agents and communication are sampled in the order of Proposition 1. Coupling A (orange) carries c′ − c into the fire; Coupling B (blue) carries ρ′ into the observation, drawn from s′. The comms kernel takes δ and reads no hazard; T<sub>X</sub> reads the post-step h′ and c′, as in the code. Arrow colours are this figure's own. The reward is not drawn (Definition 2). <span class="figure-note">Status: schematic, no data.</span></p>

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

and agent $i$'s observation is drawn from the post-step state, $o'_i \sim O^i_{\kappa_B}(\cdot \mid x', h', \rho', c', k')$. The dependence of $T_H$ on the collapse increment $c' - c$ is Coupling A (§5); the dependence of $O^i_{\kappa_B}$ on the fire, through the smoke field $\rho'$ it produces, is Coupling B (§6). A training mixture (§9.1) draws $\theta$ once per episode, at reset. The slopes $\gamma_p$ and $\gamma_n$ (§9.2, Appendix H) are unrelated to this discount.

**Proposition 1 (Well-posedness and Markov closure).** For every $\theta$, the process $s_t = (x_t, h_t, \rho_t, c_t, k_t, t)$ under any joint policy is a Markov chain, and $\mathcal{M}_\theta$ is a well-defined Dec-POMDP: finite-horizon optimal joint policies exist, and the standard value definitions apply.

The proof (Appendix A) composes the five kernels in order. Because $\rho$ is real-valued the state space is not finite, but the states and observations reachable within the horizon form finite sets, and restricted to them $\mathcal{M}_\theta$ is a finite Dec-POMDP.

**Remark 1 (Hardness).** For two or more agents, the finite-horizon Dec-POMDP decision problem is NEXP-hard, and NEXP-complete when the horizon is below the number of states (Bernstein et al., 2002)<d-cite key="bernstein2002"></d-cite>. This bounds the worst case over the class and says nothing about a particular instance; it licenses the expectation that no general exact planner will scale, which is why we learn policies rather than plan.

Listing 1, the body of `step`, follows the factorization; the link graph is drawn on its own stream with no hazard argument, and the reward line reads only the task reward and the two death counts. In the listing, `tl` is the episode's $\theta$, and no configuration here uses the early `frozen` control branch. The observation is then drawn from the new state on its own stream (`che/env/env.py:394-396`).

**Listing 1.** One environment step in the order of Proposition 1.

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

### 3.2 The fire and its smoke

**Definition 3 (Fire kernel).** Each cell is Fuel, Burning or Burnt. At each step, independently for each ordered pair of a Burning cell $g$ and a Fuel von Neumann neighbour $g' \in N(g)$, the cell $g'$ ignites with probability $\beta$. A Burning cell becomes Burnt after exactly one step, and Burnt is absorbing. Fuel cells may also ignite spontaneously at rate $\iota \ge 0$ per step; CHE uses $\iota = 0$<!-- N:DX-1 -->.

Every episode starts from an all-Fuel grid with one<!-- N:V3-1 --> Burning cell at a uniformly random position (`che/env/env.py:241-243`). One uniform per cell and incoming direction realizes the per-edge Bernoulli variables of Proposition 2's coupling exactly (`che/env/hazard.py:8-16`; Appendix A), and cells outside the arena never burn.

**Proposition 2 (Bond percolation).** Under Definition 3 with $\iota = 0$ and a single ignition at the origin, the set of eventually-Burnt cells is equal in distribution to the open cluster of the origin in i.i.d. bond percolation on $(G, E)$ with edge-open probability $\beta$.

Here $E$ is the arena's set of von Neumann edges. The proof (Appendix A) is a short coupling, the correspondence between an epidemic with a constant infectious period and bond percolation described by Grassberger (1983)<d-cite key="grassberger1983"></d-cite>. Its hypotheses hold for CHE's fire when Coupling A is off, since collapses otherwise add ignitions.

Smoke outlives flame. Per cell,

$$
\rho' = e^{-\eta}\rho + \sigma_s \mathbf{1}[h' = \mathrm{Burning}],
$$

with emission $\sigma_s = 1.0$ and decay $\eta = 0.5$, held fixed by convention and never calibrated<!-- N:DX-1 -->. A cell emits $\sigma_s$ once, in the step it burns, and its smoke then decays geometrically, with no spatial smoothing (`che/env/hazard.py:67-79`).

### 3.3 Agents, deaths and a hazard-blind reward

The agents kernel $T_X(x' \mid x, a, h', c')$ acts in three deterministic stages that consume no random numbers (`che/env/env.py:159-173`). An alive agent on a cell that collapses in this step is disabled before it moves. Survivors take one of 5<!-- N:ENV-8 --> actions, stay or a von Neumann move clipped to the grid, and a move into a collapsed cell is cancelled. An agent whose new cell is Burning in $h'$ is then disabled, so a cell igniting under a standing agent kills it; Burning cells can be entered, and avoidance must be learned. A disabled agent stays disabled, holds still, collects nothing and disappears from the others' observations.

**Definition 2 (Ambient hazard).** The hazard is *ambient* if and only if (i) and (ii) hold.

(i) *Reward independence:* the reward is a function of task variables and of the agents' alive transition only,

$$
\begin{aligned}
R(s,a,s') = {} & R_{\mathrm{task}}(\mathrm{task}(x), a, \mathrm{task}(x')) \\
& - d_p\,\lvert\{i : \alpha_i = 1,\ \alpha'_i = 0\}\rvert ,
\end{aligned}
$$

where $\mathrm{task}(x)$ denotes the task variables (in CHE, the food grid and the alive agents' positions) and $d_p \ge 0$ is a fixed death penalty. No term of $R$ references $h$, $\rho$ or $c$, and the hazard appears in no auxiliary cost or constraint channel: no CMDP constraint, no Lagrangian penalty, no safety critic.

(ii) *Non-adversarial:* $T_H$ is a fixed stochastic kernel; nothing in the environment optimizes, learns or best-responds.

Under clause (i), survival is learned through two hazard-blind routes: a dead agent collects no further task reward, and each death costs a fixed $d_p = 0.5$<!-- N:ENV-1 -->, whatever its cause, in every configuration reported here except the $d_p$ ablation below (the code's default is 0<!-- N:ENV-1 -->). Fire and collapse reach return only through the transition and observation kernels. A hazard-priced reward signals the hazard's state whether or not anything is harmed: JaxWildfire, for example, penalizes its agent at every step in proportion to the number of burning cells (Çakır et al., 2025)<d-cite key="cakir2025jaxwildfire"></d-cite>. At $d_p = 0$ only the first route would remain.

Listing 2's signature admits only the food and occupancy grids: no fire, smoke or structure argument can reach the task reward.

**Listing 2.** The task reward reads food and occupancy only.

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

One test of clause (i) asserts identical rewards, with and without the death penalty, for states that differ only in fire, smoke or structure; fire and structure differ only far from every agent, which pins the alive transition equal (`che/tests/test_reward_independence.py:6-15`). It shows only that the reward reads no hazard state directly, since the fire is meant to change return through deaths. The other kills a standing agent by fire and, separately, by collapse, with identical task state, and asserts a reward of $-d_p$ both times (`che/tests/test_lethality.py:143-162`).

Clause (i) also fixes how §9's two co-primary outcomes enter learning: survival is a penalized channel, each death costing $d_p$, and completion a rewarded one, each collected item earning +1<!-- N:ENV-9 -->. §9.2 reads any asymmetry between them as one between a penalized channel and a rewarded one.

The one ablation of $d_p$ is from the calibration phase, with this scope: the fire alone with no coupling on, 500 updates<!-- N:ENV-2 -->, 3 seeds per cell<!-- N:ENV-2 -->, an observation encoding that predates the one used here, and means over the final training updates. Raising $d_p$ from 0<!-- N:ENV-2 --> to 0.5<!-- N:ENV-1 --> moved High survival from 0.575 to 0.866<!-- N:ENV-2 --> and High completion from 0.765 to 0.821<!-- N:ENV-3 -->, moved Medium survival from 0.931 to 0.951 with completion 0.750 at both<!-- N:ENV-4 -->, and left Low tied, 0.991 against 0.992<!-- N:ENV-5 -->. It was not re-run under the current observation or with the couplings.

Clause (ii) does not make the hazard independent of the agents: a weak cell with an agent on it is nine<!-- N:CA-8 --> times as likely to collapse in a step as an empty one, and a collapse can seed fire (§5.1).

### 3.4 Nested models: ablations are exact by construction

Each stressor is a parameter of one transition or observation kernel, and setting it to zero recovers a nested special case of the same model.

| stressor | parameter | lives in | off ($=0$) recovers | test (`che/tests/`) |
|---|---|---|---|---|
| Coupling A (§5) | $\kappa_A$ | $T_H$, through $c' - c$ | a fire blind to the structure | `test_nesting.py` |
| Coupling B (§6) | $\kappa_B$ | $O^i$ | the pre-masking observation, plus an all-ones visibility plane | Listing 3 |
| communication denial (§7) | $\delta$ | $T_K$ | free, range-limited communication | `test_comms.py` |

The fire's $\beta$ is a parameter of the same kind, positive in every configuration and set by severity (§4).

One engineering rule makes the nesting exact: every stochastic branch draws its uniforms unconditionally and compares them against a probability that may be zero. The draws for Coupling B's reveal, the links and the per-episode mixture use streams derived from the reset or step key by a fixed tag, so adding them left the existing streams untouched. Setting a stressor to zero therefore changes comparisons only, and the same keys reproduce the nested model's trajectory bit for bit.

Listing 3 runs the environment at $\kappa_B = 0$ with and without masking, under the same keys, and asserts bitwise-identical fire, smoke, structure, food, positions, alive flags and rewards. The rest of the test (`che/tests/test_coupling_b.py:143-156`) steps both by hand and asserts identical content planes, an all-ones visibility plane and a zero masked share.

**Listing 3.** With $\kappa_B = 0$, trajectories and rewards are bitwise those of the environment before masking.

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

With $\kappa_A = 0$, collapse activity leaves the fire and smoke bitwise unchanged (`che/tests/test_nesting.py:78-88`); at $\delta = 0$, the environment reproduces, on the CPU, a trajectory digest recorded before the communication channel existed (`che/tests/test_comms.py:272-319`). A structural test also asserts that the traced computation keeps its random-number primitives at parameter value zero, catching a gate such as `if kappa_A > 0:` that behavioural tests miss (`che/tests/test_nesting.py:222-240`).

### 3.5 The instance, training and metrics

Every trained policy and evaluation in this paper uses one instance: a 64 × 64 grid, 12 agents, a horizon of 256 steps, a 9 × 9 egocentric crop and 32 food items<!-- N:ENV-6 -->. Food sits on distinct cells from reset and does not respawn, and an alive agent on a food cell collects it for a team reward of +1<!-- N:ENV-9 -->. The observation's 8 channels<!-- N:ENV-7 --> are six<!-- N:ENV-7 --> indicators (burning, burnt, food, weak, collapsed, alive occupancy), the raw smoke density and Coupling B's visibility plane, which marks the revealed cells. An own-state vector gives the agent's row and column divided by the grid side, its alive flag and $t$ over the horizon<!-- N:ENV-7 -->.

All agents share one actor-critic network over the crop, the own-state vector and the aggregate of delivered messages. It has two convolutions with 16 and 32 channels, a dense layer of 128 units, and separate actor and critic heads with a 64-unit layer each<!-- N:ENV-10 -->. A message head receives no gradient; what it emits is a frozen-at-initialization projection of trained trunk features (§7).

Training is the independent PPO of de Witt et al. (2020)<d-cite key="dewitt2020ippo"></d-cite>, in the PureJaxRL style of Lu et al. (2022)<d-cite key="lu2022dpo"></d-cite>, on the environment conventions of JaxMARL (Rutherford et al., 2024)<d-cite key="rutherford2024jaxmarl"></d-cite>. Each seed trains one shared-parameter policy<!-- N:ENV-11 -->, whose update takes each agent's transitions as separate samples under the team reward. Each update collects 128 steps from 256 parallel environments<!-- N:DX-2 -->, 32,768 environment steps<!-- N:DX-3 -->, each advancing all 12 agents<!-- N:ENV-6 -->. ISO, ISO-4 and JOINT (§9) each train for T\* = 1000 updates<!-- N:DES-13 -->, or 32,768,000 environment steps<!-- N:DX-3 -->, with the hyperparameters of Appendix B.

The co-primary outcomes of §9 are per-episode. *Completion* is $1 - F/32$<!-- N:ENV-6 -->, where $F$ is the number of food items left at the episode's last step; *survival rate* is the fraction of the 12 agents<!-- N:ENV-6 --> alive at the end. Episodes always run to the horizon, even when every agent has died (`che/env/env.py:361`; `che/eval/harness.py:44-45`). Deaths are also recorded by cause, as diagnostics.
