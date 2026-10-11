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
