<!-- PAPER V3 DRAFT (PAPER V3 ruling, 2026-10-12): builder-drafted, not owner-approved -->

## Appendices

<!-- STUB-SPEC
ALTERNATE FOR OWNER CHOICE V3Q3 (V3-S6): identical to sections/13_appendix_proofs.md except that the transfer-bound remark (formerly Proposition 4) and its honesty note are dropped; then section 7 keeps "no theorem that joint training wins" alone.
WRITER: W2. BUDGET: Appendix A's.
KEEP IN STEP: every change to sections/13_appendix_proofs.md is mirrored here.
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
