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

The hazard is not agent-independent: a weak cell with an agent on it collapses nine<!-- N:CA-8 --> times as often as an empty one,. Below the percolation threshold, with collapses as the fire's only source and their clusters apart, the expected burnt area grows linearly in the collapse rate (Proposition 3, checked in two<!-- N:DX-304 --> runs at parameters other than the locked ones; Appendix A).

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

with $R_{\mathrm{comm}} = 16$<!-- N:COM-6 --> cells. Messages $m_i \in [-1, 1]^{8}$<!-- N:DX-17 --> arrive one step later as the mean over a receiver's open links.

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

**Table 2.** Each property of CHE with the listing, test (in the code supplement's `che/tests/`) and figure that carry it.

| property | listing | test | figure |
|---|---|---|---|
| fire, smoke and agents in Definition 1's order (Proposition 1) | 3 (Appendix A) | `test_hazard.py`, `test_lethality.py` | 2 |
| the fire is bond percolation; severity by a measured threshold (Proposition 2, Corollary 1) | — | `test_percolation.py` | 3 |
| collapse seeds the fire (Coupling A; Proposition 3) | 1 | `test_coupling_a.py`, `test_prop3.py` | 1, 4 |
| smoke attenuates perception (Coupling B; Theorem 1) | 4 (Appendix A) | `test_coupling_b.py`, `test_e2c.py` | 1, 5 |
| communication denial reads no hazard | 3 (Appendix A) | `test_comms.py` | — |
| hazard-blind reward, cause-blind death price (Definition 2) | 2 | `test_reward_independence.py`, `test_lethality.py` | — |
| ablations are bitwise-nested models | 5 (Appendix A) | `test_nesting.py`, `test_coupling_b.py`, `test_comms.py` | — |
| locked constants are reachable from the configurations | — | `test_locks.py` | — |
| reproducibility floors per metric, GPU and artifact (§5) | — | — | C1 |

### 3.5 Instance, training and metrics

Every trained policy, and every evaluation of one, uses one instance: a 64 × 64 grid, 12 agents, a horizon of 256 steps, a 9 × 9 egocentric crop and 32 food items<!-- N:ENV-6 -->.

Each seed trains one shared-parameter actor-critic policy<!-- N:ENV-11 --> (Appendix B) with the independent PPO of de Witt et al. (2020)<d-cite key="dewitt2020ippo"></d-cite>, in the style of Lu et al. (2022)<d-cite key="lu2022dpo"></d-cite>, at 32,768<!-- N:DX-3 --> environment steps per update.

Both outcomes are per episode: *completion* is $1 - F/32$<!-- N:ENV-6 -->, with $F$ the food left at the end, and *survival* is the fraction of the 12<!-- N:ENV-6 --> agents alive at the end. Episodes always run to the horizon.

A coupling-co-active counter logs the collapse-seeded ignitions within Chebyshev radius 4<!-- N:DX-37 --> of an alive agent. Only Coupling A produces them and $\kappa_B$ does not enter the count, so it is co-active only in all-on configurations.
