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

<!-- FIGURE BLOCK carried from demo (sections/03_environment.md:7-9); writer checks caption against the caption rules in this stub and keeps the block self-contained -->

{% include figure.html path="assets/img/submission/fig01_schematic.png" class="img-fluid" alt="Five numbered boxes in a row, collapse, hazard, smoke, agents and comms, with a Coupling A arrow from collapse into the hazard box, a Coupling B arrow from smoke down to an observation box drawn from the post-step state, and comms denial entering the comms box with no hazard input." caption="Figure 4. One environment step of CHE." %}

<p class="caption">Five kernels sampled from s to s′ in the order of Proposition 1: collapse, fire, smoke, agents, communication. Coupling A (thick orange arrow) carries the collapse increment c′ − c into the fire kernel; Coupling B (thick blue arrow) carries the smoke field ρ′ into the observation kernel; the denial level δ enters the communication kernel, which has no hazard input. Each agent observes a 9 × 9<!-- N:ENV-6 --> egocentric crop of the post-step state. The agents kernel reads the post-step fields, T<sub>X</sub>(x, a, h′, c′), as the code and Definition 1 do. The arrow colours belong to this figure only; in the interactive figures orange is burning fire and blue marks agents. The reward is not drawn (Definition 2). <span class="figure-note">Status: schematic, no data · Interact: none (static figure).</span></p>

<!-- LISTINGS carried verbatim from the committed files: place each where your prose introduces it, keep its LISTING line directly above its fence, never edit the code -->

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
