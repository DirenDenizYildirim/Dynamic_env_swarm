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
