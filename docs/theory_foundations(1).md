# Formal Foundations — Compound Hostile Environment Swarm Project

**Status:** working draft v0.1 — theory backbone for the RA-L/IROS 2027 submission.
**Scope:** formalizes the environment (augmented Dec-POMDP), the hazard kernel and
its phase structure, Couplings A and B, the comms axis, and the compositional
generalization hypothesis. Every claim is tagged **[PROVEN]**, **[CITED]** (standard
result we invoke), or **[EMPIRICAL]** (motivated by theory, decided by experiment).

---

## 0. Notation

- Grid $G \subset \mathbb{Z}^2$, $|G| = m$ cells; neighborhood $N(g)$ (von Neumann
  unless stated otherwise; Moore variants noted where thresholds change).
- $n$ agents, index set $I = \{1,\dots,n\}$.
- Time $t = 0, 1, 2, \dots$; horizon $T$ (episodic) or discount $\gamma \in (0,1)$
  (used for theory statements; the implementation is episodic).
- $\Delta(\mathcal{Y})$ = probability distributions over $\mathcal{Y}$.
- Stressor configuration $\theta = (\beta, \kappa_A, \kappa_B, \delta) \in \Theta$:
  hazard transmissibility $\beta$, Coupling A strength $\kappa_A$, Coupling B
  strength $\kappa_B$, comms-denial level $\delta$.

---

## 1. The environment as a factored, augmented Dec-POMDP

### Definition 1 (Compound Hostile Environment, CHE)

A CHE is a Dec-POMDP
$\mathcal{M}_\theta = \langle I, \mathcal{S}, \{\mathcal{A}_i\}, T_\theta, R, \{\Omega_i\}, O_\theta, \gamma \rangle$
whose state space factors as

$$\mathcal{S} = \mathcal{X} \times \mathcal{H} \times \mathcal{C} \times \mathcal{K}$$

- $\mathcal{X}$: joint agent state (positions $x_i \in G$, alive/disabled flags
  $\alpha_i \in \{0,1\}$, task-carried state).
- $\mathcal{H} = \Sigma_H^{G}$: hazard field; per-cell hazard state
  $\Sigma_H = \{\mathrm{Fuel}, \mathrm{Burning}, \mathrm{Burnt}\}$ for the discrete
  kernel (a continuous intensity variant $\mathcal{H} = [0,1]^G$ is an
  implementation option; the theory below uses the discrete kernel).
- $\mathcal{C} = \{\mathrm{intact}, \mathrm{collapsed}\}^{G}$: structural state.
- $\mathcal{K}$: comms-channel state (realized link graph $G^{\mathrm{comm}}_t$ on $I$).

and whose **transition kernel factorizes** as

$$T_\theta(s' \mid s, a) \;=\; \underbrace{T_C(c' \mid c, x)}_{\text{structure}} \;\cdot\; \underbrace{T_H^{\beta,\kappa_A}(h' \mid h, c, c')}_{\text{hazard (Coupling A enters here)}} \;\cdot\; \underbrace{T_K^{\delta}(k' \mid x')}_{\text{comms}} \;\cdot\; \underbrace{T_X(x' \mid x, a, h, c)}_{\text{agents}}$$

Each agent's observation is drawn from
$O_\theta^i(o_i \mid s) = O^i_{\kappa_B}(o_i \mid x, h, c, k)$, where the
**dependence of the observation kernel on $h$ is Coupling B** (Section 5).

### Definition 2 (Passive survival stressor) — the paper's core reframe, stated formally

The hazard is a **passive survival stressor** iff:

1. **Reward-independence:** $R(s, a)$ is measurable with respect to task variables
   only — formally, $R(s,a) = R(\mathrm{task}(x), a)$; no term of $R$ references
   $h$ or $c$. The hazard influences return *only* through the transition kernel
   (disabling agents: $\alpha_i \to 0$ when agent $i$ occupies a Burning cell) and
   the observation kernel (Coupling B). Contrast: the monitoring/suppression
   literature places the hazard *inside* $R$ (coverage of the fire front, mapping
   error, suppression progress). This one-line definition is what cleanly separates
   the project from Haksar & Schwager–style work and the entire
   monitoring/estimation lineage.
2. **Non-adversarial:** $T_H$ is a *fixed* stochastic kernel — there is no
   optimizing, learning, or best-responding component in the environment. This
   distinguishes the setting from robust/minimax MARL and pursuit-evasion.
   Note the subtlety: through $T_C(c' \mid c, x)$, agent behavior *can* influence
   collapse (load-triggered failure) and hence, via Coupling A, the hazard. The
   environment is still non-adversarial in the formal sense above (fixed kernel,
   no objective), but it is not agent-independent — worth one honest sentence in
   the paper, because it is also realistic (robots walking on weak floors).

### Proposition 1 (Well-posedness / Markov closure) [PROVEN]

For every $\theta \in \Theta$, the process $s_t = (x_t, h_t, c_t, k_t)$ under any
joint policy is a Markov chain, and $\mathcal{M}_\theta$ is a well-defined
Dec-POMDP: finite-horizon optimal joint policies exist, and all standard value
definitions apply.

**Proof.** $T_\theta$ as defined is a product of conditional kernels, each
measurable in its conditioning variables, all of which are components of
$(s, a)$ or of already-sampled components of $s'$ (the dependence of $T_H$ on
$c'$ and of $T_K$ on $x'$ is a sequential composition within one time step:
sample $c' \sim T_C$, then $h' \sim T_H(\cdot \mid h, c, c')$, then
$x' \sim T_X$, then $k' \sim T_K(\cdot \mid x')$). A composition of Markov
kernels is a Markov kernel on the product space, so $T_\theta$ is a valid
transition kernel on $\mathcal{S}$ and $(s_t)$ is Markov. $\mathcal{S}$,
$\mathcal{A} = \prod_i \mathcal{A}_i$, and $\Omega_i$ are finite, so
$\mathcal{M}_\theta$ is a finite Dec-POMDP; existence of optimal finite-horizon
joint policies is standard. $\blacksquare$

**Why this matters (one paragraph for the paper):** from any single agent's
perspective the hazard looks like *nonstationarity*; Proposition 1 says that,
formally, it is not — the hazard is *state*, evolving under a stationary kernel.
This is precisely the reframe from "hazard as target / hazard as noise" to
"hazard as environment dynamics one must survive," and it licenses every
standard MARL training tool without modification.

### Remark 1 (Hardness, one line for the paper) [CITED]

Finite-horizon Dec-POMDPs are NEXP-complete (Bernstein, Givan, Immerman,
Zilberstein, 2002). With comms denial ($\delta > 0$) the CHE does not collapse
to an MPOMDP, so the hardness framing applies and justifies the
learning-based (rather than planning-based) approach.

---
## 2. The hazard kernel and its exact phase structure

### Definition 3 (Fire-CA kernel)

Per-cell states $\{\mathrm{Fuel}, \mathrm{Burning}, \mathrm{Burnt}\}$. At each
step, independently for each ordered pair (Burning cell $g$, Fuel neighbor
$g' \in N(g)$): $g'$ ignites with probability $\beta$. A Burning cell becomes
Burnt after exactly one step (the constant-burn-time model; a geometric burn
time is an implementation variant, noted below). Burnt is absorbing. Spontaneous
ignition rate $\iota \ge 0$ per Fuel cell per step (we take $\iota = 0$ in the
propositions and reintroduce it as a knob).

This kernel has finite interaction radius 1, is translation-invariant up to
terrain heterogeneity, and is implementable as a depthwise convolution — the
theory and the GPU implementation are the same object.

### Proposition 2 (Exact equivalence to bond percolation) [PROVEN / CITED]

Under Definition 3 with $\iota = 0$ and a single ignition at the origin, the
set of eventually-Burnt cells is equal in distribution to the open cluster of
the origin in i.i.d. **bond percolation** on $(G, E)$ with edge-open probability
$\beta$.

**Proof (coupling).** Attach to each *unordered* edge $e = \{g, g'\}$ an
independent $B_e \sim \mathrm{Bernoulli}(\beta)$, and declare that a
transmission attempt across $e$ succeeds iff $B_e = 1$. Claim: each edge is
attempted at most once. When some cell of $e$ first Burns while the other is
Fuel, one attempt occurs; afterwards the burning endpoint is Burnt (absorbing),
and if the other endpoint later Burns via a different path, its neighbor across
$e$ is already Burnt, so no second attempt occurs. Hence the fire dynamics,
run with the variables $\{B_e\}$, burn exactly the connected component of the
origin in the subgraph of open edges $\{e : B_e = 1\}$, which is the bond
percolation cluster. $\blacksquare$

This is the SIR-with-constant-infectious-period $\leftrightarrow$ bond
percolation mapping (Grassberger, 1983); we get it here with a self-contained
proof, which is worth including in the paper's appendix because it is short and
it imports fifty years of percolation theory for free.

### Corollary 1 (Phase structure) [CITED]

On $\mathbb{Z}^2$ with von Neumann neighborhood:

1. **Critical point.** $\beta_c = 1/2$ exactly (Kesten, 1980).
2. **Subcritical** ($\beta < \beta_c$): the burnt cluster is a.s. finite; its
   expected size $\chi(\beta) < \infty$; cluster-size distribution has
   exponential tails; correlation length $\xi(\beta) < \infty$.
3. **Critical scaling.** As $\beta \uparrow \beta_c$:
   $\chi(\beta) \sim |\beta - \beta_c|^{-\gamma_p}$ with $\gamma_p = 43/18$,
   and $\xi(\beta) \sim |\beta - \beta_c|^{-\nu_p}$ with $\nu_p = 4/3$
   (2D percolation universality).
4. **Supercritical** ($\beta > \beta_c$): with positive probability the fire
   spreads indefinitely; conditioned on survival, the burnt region grows
   linearly in time with an asymptotic front speed $v(\beta) > 0$ and a
   deterministic limiting shape (shape-theorem behavior for spatial epidemics).

Caveats tracked honestly: exact $\beta_c = 1/2$ is specific to the idealized
kernel (von Neumann, constant burn time, homogeneous fuel, no wind). Moore
neighborhoods, heterogeneous fuel, wind advection, and geometric burn times
shift $\beta_c$ and break exactness, but **the existence of the phase
transition and the divergence of $\chi$, $\xi$ near it are universal** — which
is all the design below relies on. The implemented kernel's critical point is
*measured*, not assumed (Section 3).

---

## 3. Severity, defined by dynamical phase rather than by knob position

### Definition 4 (Severity regimes)

Fix arena side length $L$ (so $m \approx L^2$). Severity levels are defined by
the position of the implemented kernel relative to its measured critical point
$\hat\beta_c$ via the correlation length $\xi(\beta)$:

- **Low** — subcritical: $\xi(\beta) \ll L$. Hazard clusters are local and
  short-lived; survival is a *local avoidance* problem.
- **Medium** — near-critical: $\xi(\beta) \sim L$. Cluster sizes are
  (finite-size) scale-free; fluctuations are maximal; a single ignition can, with
  non-negligible probability, cascade to arena scale. Survival is a *global
  anticipation* problem with maximal unpredictability. This is the regime where
  memorization is most punished, and we should expect the paper's most
  interesting behavior here.
- **High** — supercritical: fire fronts propagate at speed $v(\beta) > 0$
  comparable to agent speed. Survival is a *race* problem.

**Why this beats "low/medium/high knob settings":** the three severities are
three *qualitatively different dynamical phases* of the same kernel, which (i)
gives reviewers a principled answer to "why these three levels?", (ii) predicts
*a priori* which regime stresses which capability, and (iii) makes severity
transfer ("held-out severity levels" in the locked hypothesis) a statement
about generalization *across dynamical phases*, which is a much stronger framing
than interpolation between knob values.

### Calibration protocol (Phase 2 deliverable) [EMPIRICAL]

Because the implemented kernel will not be the idealized one:

1. Sweep $\beta$ on the target grid size; from single-seed ignitions measure
   $P_{\mathrm{span}}(\beta)$ (probability the burnt cluster reaches the arena
   boundary), mean burnt fraction, and front speed.
2. Estimate $\hat\beta_c$ as the steepest point of $P_{\mathrm{span}}(\beta)$
   (finite-size crossing).
3. Fix severity levels by *observables*, not by $\beta$: e.g. Low: burnt
   fraction $\in [1, 5]\%$ per episode; Medium: $P_{\mathrm{span}} \in
   [0.3, 0.7]$; High: front speed $\in [0.5, 1] \times$ agent speed. Bands are
   provisional and locked after Phase 2 measurement.

This doubles as the **correctness test of the CA port**: if the ported
PyTorchFire/JaxWildfire kernel does not exhibit a clean sigmoid in
$P_{\mathrm{span}}$, the port is wrong. Theory as unit test.

---

## 4. Coupling A — structural failure seeds the hazard

### Definition 5 (Coupling A)

Collapse dynamics: cell $g$ collapses at time $t$ with probability
$\lambda(g, x_t, c_t)$ (spontaneous load-driven term plus an agent-load term;
collapsed is absorbing). Coupling A: each collapse event at $g$ ignites each
Fuel cell in a seeding neighborhood $N_A(g)$ independently with probability
$\kappa_A$ (equivalently, adds an impulse to the ignition field). Setting
$\kappa_A = 0$ recovers the uncoupled system $T_H^{\beta,0}(h' \mid h)$ — i.e.
**the ablation "no Coupling A" is a nested model of the full system**, not a
different environment. Same for $\kappa_B = 0$ and $\delta = 0$ below. This
nesting is the formal backbone of Phase 7 (Section 8).

### Proposition 3 (Collapse events dominate hazard exposure; divergence near criticality) [PROVEN, with a stated approximation]

Work in the subcritical regime $\beta < \beta_c$ with $\iota = 0$, and suppose
collapse events arrive at rate $\lambda_A$ per step, each seeding one ignition
at (say) a uniformly located Fuel cell, with seeded clusters pairwise disjoint
(sparse regime: $\lambda_A T\, \chi(\beta) \ll m$). Then the expected total
burnt area by time $T$ satisfies

$$\mathbb{E}[B_T] = \lambda_A \, T \, \chi(\beta)\,(1 + o(1)), \qquad \text{and in general } \mathbb{E}[B_T] \le \lambda_A T \chi(\beta),$$

where $\chi(\beta)$ is the mean percolation cluster size. Consequently the
marginal hazard exposure per unit of structural instability,
$\partial \mathbb{E}[B_T] / \partial \lambda_A = T \chi(\beta)$, **diverges** as
$\beta \uparrow \beta_c$ like $|\beta - \beta_c|^{-43/18}$.

**Proof.** Each collapse seed grows, by Proposition 2, a burnt cluster equal in
distribution to a bond-percolation cluster, of expected size $\chi(\beta)$.
By linearity of expectation over the $\mathrm{Binomial}$/Poisson number of
seeds, the total expected burnt area is $\lambda_A T \chi(\beta)$ when clusters
are disjoint; overlaps only remove double counting, giving the upper bound in
general. The divergence rate is Corollary 1(3). $\blacksquare$

**Interpretation for the paper:** in calm (subcritical) conditions with no
spontaneous ignition, *structural failure is the hazard's only birth channel*,
and near criticality a *single* collapse has divergent expected consequences —
this is the formal signature of a *compound cascading disaster*, and it is the
quantitative reason Coupling A changes the problem character rather than adding
noise: the policy's incentive to model and avoid *structural* risk is
proportional to $\chi(\beta)$, i.e. it is severity-dependent by a power law.

---
## 5. Coupling B — the hazard degrades perception, and a theorem on why that matters

### Definition 6 (Coupling B, Beer–Lambert observation model)

Agent $i$'s ability to observe a feature at position $y$ from position $x_i$
is gated by the transmittance along the line of sight:

$$\tau_i(y) \;=\; \exp\!\Big(-\kappa_B \int_{x_i \to y} \rho_H \, d\ell\Big),$$

where $\rho_H$ is the local hazard/smoke density (in the discrete kernel, a
kernel-smoothed indicator of Burning/recently-Burnt cells — smoke outlives
flame, which is the physically honest choice and an implementation knob). The
feature is observed with probability $\tau_i(y)$ (or observed with noise scale
$\propto 1/\tau$; both are faithful instantiations). $\kappa_B = 0$ recovers
hazard-independent observation. Beer–Lambert attenuation is the standard
optics model for smoke/turbidity, so Coupling B is *physically grounded*, not
an ad-hoc noise schedule — worth a sentence in the paper.

Key structural property: $O^i_{\kappa_B}$ depends on $h_t$ — perception quality
is **a function of the hazard's own evolving state**, so degradation
concentrates exactly where and when the hazard is active. This is the formal
difference from an always-on independent sensory-noise axis, and it is what
makes the following theorem possible.

### Theorem 1 (Memorization gap, and its erosion by Coupling B) [PROVEN]

Consider the two-corridor environment $E_{2C}(\kappa_B)$: start cell $s_0$, a
path of $d$ steps to a branch $b$, from which two disjoint corridors $L, R$ of
length $\ell$ lead to the goal. Horizon $T = d + \ell$ (zero slack: a wrong
commitment cannot be undone). At $t = 0$ nature draws $Z \in \{L, R\}$
uniformly; corridor $Z$ burns at depth $\ell_f \ge 1$ beyond $b$, and any agent
entering corridor $Z$ is disabled. Reward $1$ for reaching the goal by $T$,
else $0$. At each step $t \le d$, the agent receives an informative signal
$Y_t = Z$ with probability $e^{-\kappa_B (d - t + \ell_f)}$ (Beer–Lambert over
the current distance to the fire, unit smoke density), else $Y_t = \varnothing$;
signals are independent across time and remembered. Let

$$q(\kappa_B) \;=\; 1 - \prod_{j=\ell_f}^{\,d+\ell_f} \big(1 - e^{-\kappa_B j}\big)$$

be the probability of being informed by the commitment point. Then:

1. **Optimal dynamic value.** $J^*(\kappa_B) = \tfrac12 + \tfrac12\, q(\kappa_B)$.
2. **The memorizing policy.** Any policy optimal for the *fixed-map* variant
   ($Z \equiv z_0$ constant) includes the signal-blind policy "always take the
   corridor $\ne z_0$"; its value on $E_{2C}$ is $\tfrac12$, for every
   $\kappa_B$. Hence the **memorization gap** is
   $$J^*(\kappa_B) - J^{\mathrm{static}} \;=\; \tfrac12\, q(\kappa_B) \;>\; 0 \quad \text{for all finite } \kappa_B .$$
3. **Coupling B erodes the value of adaptivity.** $q$ is continuous and
   strictly decreasing in $\kappa_B$, with $q(0^+) \to 1$ (gap $\to \tfrac12$,
   maximal) and $q(\kappa_B) \to 0$ as $\kappa_B \to \infty$ (gap $\to 0$: under
   total perceptual denial, the optimal adaptive policy is *no better than the
   memorizing one*).

**Proof.**
*(1)* With zero slack, the only decisions are the corridor choice at $b$ and
(vacuously) the path to $b$; waiting or probing is impossible within $T$.
If informed (probability $q$), taking the corridor $\ne Z$ succeeds with
probability 1; if uninformed, both corridors are exchangeable given the
history, so any choice succeeds with probability $\tfrac12$; hence
$J^* = q + (1-q)\tfrac12 = \tfrac12 + \tfrac{q}2$, and no policy can exceed
this since success requires either information (prob. $q$) or a lucky guess.
*(2)* In the fixed-map environment the signal is uninformative (constant $Z$),
so the signal-blind policy is optimal there; on $E_{2C}$ it succeeds iff
$Z = z_0$, probability $\tfrac12$.
*(3)* Each factor $(1 - e^{-\kappa_B j})$ is continuous and strictly increasing
in $\kappa_B$ on $(0,\infty)$, so the finite product is, so $q$ is continuous
and strictly decreasing; the limits are immediate ($e^{-\kappa_B j} \to 1$
pointwise as $\kappa_B \to 0$, so the product $\to 0$; $\to 1$ as
$\kappa_B \to \infty$). $\blacksquare$

**What Theorem 1 buys the paper.** In one toy: (i) a *proof* of the document's
founding intuition ("a static hazard can be memorized; an evolving one forces
generalization"), with the gap exactly quantified as half the information
probability; (ii) a proof that Coupling B is not merely additive difficulty —
it *interacts* with the pillar by continuously destroying the very information
channel that makes adaptivity valuable. This is the formal argument that the
couplings compose into something qualitatively new, which is the paper's
load-bearing claim (Claim 4 of the validation pass) expressed in miniature.

### Remark 2 (All three axes interact: comms is load-bearing exactly when perception fails) [PROVEN, remark-level]

Extend $E_{2C}$ with a second agent and slack $T = d + \ell + 1$, reward 1 if
*any* agent reaches the goal. With free comms: agent 2 enters corridor $L$ at
the branch; if it survives one step it messages "L safe" (agent 1 takes $L$),
and if it is disabled its silence identifies $Z = L$ (agent 1 takes $R$).
Success probability $1$, for every $\kappa_B$. Under full comms denial
($\delta = 1$), no message passes and — since Coupling B also occludes direct
observation of agent 2's fate — agent 1 reverts to the single-agent value
$\tfrac12 + \tfrac{q(\kappa_B)}2$. The marginal value of communication is
therefore

$$\mathrm{VoC}(\kappa_B) \;=\; \tfrac12\big(1 - q(\kappa_B)\big),$$

which is **increasing in $\kappa_B$**: communication matters most precisely
when the hazard has blinded individual perception. This single formula
justifies, in advance, why comms denial must be trained *jointly* with the
couplings rather than staged — the stressors are value-coupled even though
comms is mechanistically independent. (Also a ready-made intuition figure:
plot $J^*$ vs. $\kappa_B$ with and without comms.)

---

## 6. The comms axis

### Definition 7 (Comms denial)

Messages $m_{ij,t}$ pass over the realized link graph $G^{\mathrm{comm}}_t$;
link $(i,j)$ is alive at time $t$ with probability
$p_{\mathrm{link}}(\|x_i - x_j\|)\cdot(1-\delta)$ (range-dependent baseline
scaled by the denial level; dropout, delay, and bandwidth-cap variants are
implementation options under the same $\delta$ parameterization). Design
choice, stated explicitly: $T_K$ does **not** depend on $h$ — comms denial is
mechanistically independent of the hazard (that is what "independent
load-bearing axis" means formally), even though Remark 2 shows their *values*
interact. Hazard-coupled comms (smoke attenuating radio, collapse severing
relays) is deliberately future work.

---
## 7. The compositional generalization hypothesis, formalized

### Definition 8 (Training protocols and the compositional gap)

Let $J_\theta(\pi)$ be the expected episodic return of joint policy $\pi$ in
$\mathcal{M}_\theta$. Fix the test configuration $\theta^* = $ (all elements
active, at held-out severity levels). Define:

- $\Theta_{\mathrm{iso}} = \{\theta : \text{at most one of } \kappa_A, \kappa_B, \delta \text{ is nonzero}\}$
  (dynamic hazard $\beta > 0$ may be active throughout, since the pillar is the
  substrate the elements attach to — **decision point D1 below**).
- **ISO protocol:** a single policy $\pi_{\mathrm{iso}}$ trained on a uniform
  mixture over a finite set of single-element configurations
  $\subset \Theta_{\mathrm{iso}}$.
- **JOINT protocol:** a single policy $\pi_{\mathrm{joint}}$ trained on a
  mixture whose support includes multi-element configurations (all elements
  co-active) at training severity levels (still excluding $\theta^*$'s held-out
  severities).
- **Compositional gap:** $\Gamma(\theta^*) = J_{\theta^*}(\pi_{\mathrm{joint}}) - J_{\theta^*}(\pi_{\mathrm{iso}})$.

**The locked hypothesis, restated:** $\Gamma(\theta^*) > 0$, with primary
metric task completion rate. **[EMPIRICAL — this is Phase 7's job.]**

### Proposition 4 (Why the hypothesis is plausible: an irreducible shift term for ISO) [PROVEN, bound-shaped]

(Simulation lemma, stated for our factored kernels; constants not optimized.)
For any policy $\pi$ and configurations $\theta, \theta'$ sharing reward $R$
with $|R| \le R_{\max}$,

$$\big|J_{\theta}(\pi) - J_{\theta'}(\pi)\big| \;\le\; \frac{\gamma R_{\max}}{(1-\gamma)^2}\, \varepsilon(\theta, \theta') , \qquad \varepsilon(\theta,\theta') = \sup_{s,a}\Big[ \|T_\theta(\cdot\mid s,a) - T_{\theta'}(\cdot\mid s,a)\|_1 + \max_i \|O^i_\theta(\cdot \mid s) - O^i_{\theta'}(\cdot\mid s)\|_1 \Big].$$

For every $\theta \in \Theta_{\mathrm{iso}}$, the kernels differ from
$\theta^*$'s on all states where coupling-co-active events occur (e.g. a
collapse-seeded fire adjacent to an agent whose observation is
simultaneously attenuated), so $\varepsilon(\theta, \theta^*) \ge
\varepsilon_{\min} > 0$ uniformly over $\Theta_{\mathrm{iso}}$ — the transfer
guarantee available to ISO carries an **irreducible slack**
$\propto \varepsilon_{\min}$, whereas JOINT trains at $\varepsilon = 0$ on the
element combination (slack only in the held-out severity direction).

**Proof.** The value-difference bound is the standard simulation lemma
(telescoping the Bellman evaluation operators of the two models along the
trajectory distribution; the observation term enters because $\pi$ acts through
$O$). $\varepsilon_{\min} > 0$ holds because on states $s$ with a collapse
increment adjacent to Fuel and an agent within attenuation range,
$T_{\theta^*}$ places $\kappa_A$-order mass on ignition transitions that
$T_\theta$ ($\kappa_A = 0$) places elsewhere, and similarly for the
observation term when $\kappa_B$ differs. $\blacksquare$

**Honesty note (must appear in the paper):** Proposition 4 bounds what can be
*guaranteed*, not what happens: upper bounds on ISO's transfer do not lower-bound
the realized gap $\Gamma$. Compositional generalization can and sometimes does
emerge from isolated training. The theory's role is to (i) locate exactly
*where* ISO's guarantee breaks (the coupling-co-active state region — which also
tells us what to *measure*: visitation frequency of that region), and (ii)
motivate the experiment. The experiment decides. Framing it this way is
strictly stronger with reviewers than pretending the hypothesis is a theorem.

### Measurement corollary (free, and worth a figure)

Log the visitation frequency of coupling-co-active states (collapse-seeded
fire within perception-attenuation range of an agent) under both protocols.
Prediction from Proposition 4's mechanism: ISO policies have near-zero training
exposure to this region and elevated failure rates *inside* it at test time;
JOINT failures should be more uniformly distributed. This turns the abstract
shift term into a plottable, reviewer-friendly diagnostic — and it is nearly
free to log in a vectorized simulator.

---

## 8. Nested-model ablation semantics — the formal backbone of Phase 7

Every stressor element is a *parameter of one kernel*, and switching it off
recovers a nested special case of the same model — never a different
environment:

| Element | Parameter | Lives in | Off ($=0$) recovers |
|---|---|---|---|
| Dynamic hazard (pillar) | $\beta$ | $T_H$ | static/no hazard field (Phase 1 control) |
| Coupling A | $\kappa_A$ | $T_H$ (dependence on $\Delta c$) | hazard blind to structure |
| Coupling B | $\kappa_B$ | $O^i$ | hazard-independent perception |
| Comms denial | $\delta$ | $T_K$ | free (range-limited) comms |
| Severity | $\beta$ vs. $\hat\beta_c$ | $T_H$ | — (defined by phase, Def. 4) |

Consequences worth stating in the methods section: (i) ablations are exact
nested models — no confound from re-implementation or re-tuning of a separate
environment; (ii) the five locked Phase 7 configs are five points in $\Theta$;
(iii) the severity sweep and the ablations share one codebase and one set of
calibration measurements.

---

## 9. What we deliberately do not claim

1. **No convergence guarantees for the evolutionary+MARL hybrid.** PBT-style
   population training on a nonstationary, nonconvex multi-agent objective has
   no useful known guarantees; we treat the training loop as an empirical tool
   (cite Jaderberg et al., 2017) and report seeds/variance per the locked
   budget.
2. **No theorem that joint training wins.** Proposition 4 is a plausibility
   bound; Theorem 1 is a toy-environment proof about *adaptivity vs.
   memorization*, not about ISO vs. JOINT protocols. The hypothesis is
   empirical by design (Reading 1, locked).
3. **No exact critical values for the implemented kernel.** Exactness holds for
   the idealized kernel (Prop. 2, Cor. 1); the implemented kernel's phase
   structure is measured (Section 3 protocol). Claims in the paper reference
   measured order parameters, not $\beta_c = 1/2$.

## 10. Theory → practice hooks (feeds the Claude Code prompts)

- **Phase 2 unit test:** ported CA kernel must reproduce a sigmoidal
  $P_{\mathrm{span}}(\beta)$ with finite-size sharpening; severity bands
  calibrated per Section 3. A kernel that fails this is mis-ported.
- **Phase 3 unit test:** with $\iota = 0$, $\beta < \hat\beta_c$, measured
  $\mathbb{E}[B_T]$ must scale linearly in collapse rate with slope
  $\approx T\hat\chi(\beta)$ (Prop. 3), with $\hat\chi$ measured from
  single-seed runs. Direct quantitative validation of Coupling A's
  implementation.
- **Phase 4 unit test:** implement $E_{2C}$ as a micro-environment; a trained
  (or even hand-coded optimal) policy must trace the $J^*(\kappa_B) = \tfrac12 +
  \tfrac12 q(\kappa_B)$ curve (Thm. 1). Validates the observation-attenuation
  code path against a closed form.
- **Phase 6/7 logging:** coupling-co-active state visitation counter (Section 7
  measurement corollary) — implement from day one; retrofitting logging into
  JIT-compiled rollouts is painful.

## 11. Decision points flagged (need your call before Phase 7 is fully specified)

- **D1 — Is the dynamic hazard itself part of $\Theta_{\mathrm{iso}}$'s
  baseline?** Recommended: yes — the pillar ($\beta > 0$) is active in *all*
  ISO configs, and "elements" = {Coupling A, Coupling B, comms}. This matches
  the locked ablation list (which ablates couplings/comms, and has
  static-hazard-trained as a *separate* config), keeps the hypothesis about
  *coupling composition*, and avoids an underpowered 4-way element grid.
- **D2 — ISO instantiation.** The locked hypothesis says "trained on each
  element in isolation and only combined at evaluation." Two readings: (a)
  one policy on a mixture of single-element configs (recommended: well-defined,
  same architecture/compute as JOINT, clean comparison); (b) separate
  specialist policies somehow merged at test (ill-defined for weight-space
  merging; only defensible as a policy-mixture baseline). Recommend locking (a)
  as the hypothesis test and, if budget allows, reporting (b) as a secondary
  baseline.
- **D3 — Smoke persistence.** Does $\rho_H$ (Coupling B's density) track
  Burning only, or Burning + decaying-Burnt (smoke outlives flame)?
  Recommended: the latter (physically honest; one extra decay parameter);
  decide before Phase 4 so $E_{2C}$'s closed form is matched by the real
  code path.

## References (to be formalized in the bibliography)

- Bernstein, Givan, Immerman, Zilberstein (2002), *The Complexity of
  Decentralized Control of Markov Decision Processes*, Math. Oper. Res.
- Grassberger (1983), *On the critical behavior of the general epidemic
  process and dynamical percolation*, Math. Biosci.
- Kesten (1980), *The critical probability of bond percolation on the square
  lattice equals 1/2*, Comm. Math. Phys.
- Jaderberg et al. (2017), *Population Based Training of Neural Networks*.
- Haksar & Schwager (2018), IROS — distributed MADQN under fire spread with
  restrictive comms (positioned as: hazard in the reward = monitoring/
  suppression framing; our Def. 2 separates the settings).
