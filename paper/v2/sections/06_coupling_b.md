<!-- PAPER V2 DRAFT (PAPER V2 ruling, 2026-10-11): builder-drafted, not owner-approved -->

## 6 Coupling B: smoke attenuates perception

<!-- STUB-SPEC
PURPOSE: Coupling B makes what an agent perceives depend on the hazard's own state. State Def. 6 as implemented and show it in code (Listing 5); state Thm. 1 and what it buys, with the toy gate as a test of the code; give the lock's outcome in one paragraph; report the survival cost at High led by its 3 of 3 replication, and Coupling B's own survival effect at Medium (the home of that measurement); explain where the masking falls; define the co-active counter and what it can see.
SUBSECTIONS (H3, as the demo's): 6.1 Definition and implementation; 6.2 What attenuation does to the value of adaptivity; 6.3 The lock: three bands that did not intersect; 6.4 The cost is paid in survival, at High; 6.5 The co-active counter, and what it can see.
WRITER: W4. BUDGET: 1,050 prose words (the demo's: 1,652); Figures 7 and 8 captions at most 80 words each.
REQUIRED FACTS: DX-33 (Figure 1 opens on agent 7 at t = 128; a pointer, no deep link); ENV-6 (9 × 9 crop); ENV-7 (the eighth plane records the reveal); CB-4 (the toy gate: largest absolute z 2.11; sum of z² 6.55 on 8 degrees of freedom, p = 0.586; mean z −0.44); DX-14 (the memorizing policy flat at ½; J*(0) = 1.0000; J* − ½ = 0.0000 at κ_B = 8 where q = 0.0056); DX-301 (the three bands); CB-3 and DX-12 (the masked-share band unreachable at Medium: ceilings 0.028 / 0.130 / 0.419 against the band's floor 0.150); CB-2 (detection and toy bands disjoint by 1.35× under a random policy, 1.15× under probe policies); CB-1 (κ_B = 1.0 locked on the detection band alone); DX-40 (trained, 500 updates); DX-13 (the three High contrasts −0.0687, −0.1066, −0.0470: −6.87, −10.66, −4.70 points; one run per cell); CB-5 (negative 3 of 3; 1.41× is the first estimate over the High floor, the three's mean about 1.19×, both against a reference scale (cross-artifact)); CB-6 (the first estimate, −8.8 points, quoted only beside CB-5); CB-7 (High floor sd 6.21 points, measured afterwards on four identical runs of a separate artifact); CB-8 (completion flips sign on a same-seed retrain; unresolved); CB-9 (Medium survival −0.03 points, graded against a three-seed spread σ_seed 0.0072, not a floor; this is the home) and METH-1 (the later Medium survival floor 0.0129); CAL-3 (β 0.49 at Medium); DX-11 (masked share at danger moments 0.0809 / 0.0560 / 0.2424 against 0.00068 / 0.00249 / 0.01559 overall); CB-10 (118×, 22×, 16×); CO-4 and DX-37 (the counter: collapse-seeded ignitions inside an alive agent's crop, Chebyshev radius 4); CO-2 (P(zero) 0.563 / 0.578 / 0.883 over 1024 / 1536 / 1024 episodes); CO-1 (0.64 events per episode at Medium); CO-3 (variance over mean 1.31 to 1.40).
FIGURES: Figure 7, static fig04_coupling_b.png (include plus a caption paragraph), carried below; its caption says the band is a reference scale (cross-artifact) although the figure's legend says "floor" (P2-3, FIGURE BATCH B9), and that the figure cannot show intervals, completion or Medium. Figure 8, static fig05_coactive.png, carried below; its caption carries the counter's scope (co-active only in all-on configurations) and that no floor exists for it. Both figures stay where the demo had them (P2-d is Q22). Fonts and widths: P2-4 is Q22; keep the demo's markup.
LISTINGS (carried below, exact lines): Listing 5, che/env/observation.py:300-310 (shortened from the demo's 289-310, KB-2): τ by Beer–Lambert transmittance; the reveal draw is unconditional; the visibility plane is appended. Prose says the draw has its own stream and κ_B is read per episode from the state; it does not echo the code's internal tags.
LATEX: Def. 6's transmittance (one display); Thm. 1's statement with the q display (one display). The proof goes to Appendix A only (LEN); here keep what the theorem buys in two or three sentences, then the gate as a test of the shared transmittance function.
HONESTY LINES AND REGISTERED STRINGS: branch_B section 5 line 5 (Medium siting: this section holds the measurement; lead the High effect with CB-5's 3 of 3, CB-6's −8.8 only beside it) and line 10 (the counter means co-active only in all-on configurations; in a mixture it reads the Coupling-A marginal, which is why mediation is VOID, section 9.2); "reference scale (cross-artifact)"; "not behaviourally suppressed" scoped to trained policies at 500 updates.
FIX-LIST AND FINDINGS ITEMS OWNED: OI-6 (never "a sixth to a quarter"; the ceiling claim scoped to the κ_B = 1.0 arm); P2-3; KB-2 (Listing 5); LEN (Thm. 1's compact proof out; section 6.3 to one paragraph; "physically grounded" to one clause); F5 (the Coupling-B calibration grid named in words; M4.2, M4.4, M5.3b as studies); P3-N11 (class C: keep the demo's Thm. 1(2), which names the signal-blind policy and its value ½); P3-N16 (class C: the demo's scoped strength wording); Q22, Q23, Q24.
DEMO KEEPS (sections/06_coupling_b.md): Def. 6 as implemented; Listing 5's gloss; Thm. 1's statement; the gate numbers; the lock's outcome; the High effect with 3 of 3 first; the Medium −0.03 with its scope; the danger-moment masking; the counter, its scope and Figure 8. CHANGES: the proof to Appendix A; section 6.3 shortened; names plain. DROPS: the duplicated proof; "The direction replicates; the magnitude is modest." if it reads as an aphorism (say the same in a plain sentence).
NOT HERE: "certified"; the 8.8 lead; 1.41× as a pooled or own-artifact floor; "completion intact"; "not behaviourally suppressible" unscoped; "a sixth to a quarter"; the counter as a co-occurrence measure in mixtures; a Medium Coupling-B survival effect; a deep link.
DEPENDENCIES: section 9.2 (mediation uses the scope note; the High readout points to 6.4); section 10 item 1 (Medium siting points here for the measurement).
-->

Coupling B makes what an agent perceives depend on the hazard's own state. Figure 1 opens on agent 7<!-- N:DX-33 --> at t = 128<!-- N:DX-33 --> and shows that agent's observation as produced, the true state of the same 9 × 9<!-- N:ENV-6 --> cells, and the probability that each cell was seen.

### 6.1 Definition and implementation

**Definition 6 (Coupling B: Beer–Lambert observation, as implemented).** Smoke is the per-cell state field $\rho'$ of §3.2, updated after the fire with no spatial smoothing, so it outlives flame. For agent $i$ at $x_i$ and a cell $y$ of its crop, let $\bar\rho_i(y)$ be the mean of $\rho'$ at the four points $x_i + t_s(y - x_i)$, $t_s = (s + \tfrac12)/4$ for $s = 0, \dots, 3$, each read at the nearest cell (smoke outside the grid reads 0). The transmittance is

$$
\tau_i(y) = \exp\!\big(-\kappa_B\,\lVert y - x_i \rVert_2\,\bar\rho_i(y)\big),
$$

a midpoint-rule form of $\exp(-\kappa_B \int_{x_i \to y} \rho\,d\ell)$ along the line of sight. Each crop cell is revealed independently with probability $\tau_i(y)$: a revealed cell passes its seven<!-- N:ENV-7 --> content planes, an unrevealed one passes zeros, and an eighth<!-- N:ENV-7 --> plane records the realized reveal, so the agent can tell "unseen" from "empty". The own cell has distance 0 and is always seen. Setting $\kappa_B = 0$ gives $\tau \equiv 1$ and recovers hazard-independent observation.

Because $\rho'$ is hazard state, perception degrades where and when the fire is active.

**Listing 5.** Coupling B in the observation kernel: transmittance, the reveal draw and the visibility plane.

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

The `reveal` line draws its uniforms whatever $\kappa_B$ is, so at $\kappa_B = 0$ the mask is all ones and the environment is bitwise the one before masking (§3.4, Listing 3). The draw has its own random stream, and $\kappa_B$ is read per episode from the state, which is how a training mixture varies it.

### 6.2 What attenuation does to the value of adaptivity

**Theorem 1 (Memorization gap, and its erosion by Coupling B).** Consider the two-corridor environment $E_{2C}(\kappa_B)$: from a start cell, a path of $d$ steps leads to a branch $b$, from which two disjoint corridors $L$ and $R$ of length $\ell$ lead to the goal; the horizon is $T = d + \ell$ (zero slack: a wrong commitment cannot be undone). At $t = 0$ nature draws $Z \in \{L, R\}$ uniformly; corridor $Z$ burns at depth $\ell_f \ge 1$ beyond $b$, and an agent entering it is disabled. The reward is 1 for reaching the goal by $T$, else 0. At each step $t \le d$ the agent receives the signal $Y_t = Z$ with probability $e^{-\kappa_B (d - t + \ell_f)}$ (Beer–Lambert over the current distance to the fire, unit smoke density), else $Y_t = \varnothing$; signals are independent across time and remembered. Let

$$
q(\kappa_B) = 1 - \prod_{j=\ell_f}^{d+\ell_f} \big(1 - e^{-\kappa_B j}\big)
$$

be the probability of being informed by the commitment point. Then (1) the optimal value is $J^*(\kappa_B) = \tfrac12 + \tfrac12 q(\kappa_B)$; (2) the policies optimal for the fixed-map variant ($Z \equiv z_0$ constant) include the signal-blind policy "always take the corridor other than $z_0$", whose value on $E_{2C}$ is $\tfrac12$ for every $\kappa_B$, so the memorization gap is $J^*(\kappa_B) - J^{\mathrm{static}} = \tfrac12 q(\kappa_B) > 0$ for all finite $\kappa_B$; and (3) $q$ is continuous and strictly decreasing in $\kappa_B$, with $q(0^+) \to 1$ and $q(\kappa_B) \to 0$ as $\kappa_B \to \infty$, so under total perceptual denial the optimal adaptive policy is no better than the memorizing one.

In one toy (proof in Appendix A), a memorizing policy loses exactly half the probability of being informed, and the hazard's own attenuation shrinks that loss continuously to zero; the theorem says nothing about what a learner does in CHE.

The theorem also tests the code. The toy and the observation kernel share one transmittance function, and the toy's information probability agrees at every grid point across Monte Carlo, the closed-form product and the full observation pipeline. The measured optimal value matches $\tfrac12 + \tfrac12 q$ under a three-condition<!-- N:CB-4 --> gate: largest $\lvert z \rvert$ 2.11<!-- N:CB-4 -->, $\sum z^2 = 6.55$<!-- N:CB-4 --> on 8<!-- N:CB-4 --> degrees of freedom ($p = 0.586$<!-- N:CB-4 -->), and mean $z$ −0.44<!-- N:CB-4 -->. The memorizing policy stays flat at ½<!-- N:DX-14 -->, $J^*(0) = 1.0000$<!-- N:DX-14 -->, and $J^* - \tfrac12 = 0.0000$<!-- N:DX-14 --> at $\kappa_B = 8$, where $q = 0.0056$<!-- N:DX-14 -->.

### 6.3 The lock: three bands that did not intersect

The strength $\kappa_B$ was to be locked where three<!-- N:DX-301 --> bands set before calibration intersect. They were a masked share of the crop at Medium in [0.15, 0.45]<!-- N:DX-301 -->, a probability in [0.4, 0.7]<!-- N:DX-301 --> that a Burning cell three<!-- N:DX-301 --> cells away is revealed at Medium, and a toy information probability $q$ in [0.3, 0.7]<!-- N:DX-301 -->. They do not intersect. The masked-share band cannot be reached at Medium: the masked share can only approach the share of crop cells with smoke on their line of sight, 0.130<!-- N:DX-12 --> there under a random policy, below the band's lower edge of 0.150<!-- N:DX-12 -->. The same $\kappa_B$ attenuates the arena's extended smoke more strongly than the toy's single smoke source, which leaves the detection and toy bands disjoint by a factor of 1.35 under a random policy and 1.15 under probe policies<!-- N:CB-2 -->. On 2026-07-27<!-- N:DX-401 -->, $\kappa_B = 1.0$<!-- N:CB-1 --> was locked on the detection band alone; the masked-share band was retired, not widened, and the toy band kept as a consistency check.

### 6.4 Survival cost at High severity

{% include figure.html path="assets/img/submission/fig04_coupling_b.png" class="img-fluid" alt="Left, the masked share of the agent crop at three severities, over all alive agent-steps and at danger moments, on a log scale. Right, three replicate survival contrasts at high severity and then the first estimate, against a hatched band one standard deviation wide on a reference scale measured on another artifact." caption="Figure 7. Coupling B: where the masking falls, and the High survival contrasts." %}

<p class="caption">(a) Masked share of the crop in the coupled arm of the Coupling-B calibration grid (labelled m44 and M4.4), over all alive agent-steps and at danger moments. (b) The High survival contrasts between the arms: three replicates<!-- N:DX-13 -->, then the first estimate. The hatched band, labelled floor, is a reference scale (cross-artifact). The figure cannot show intervals, completion or Medium. <span class="figure-note">Status: trained policies, 500 updates<!-- N:DX-40 --> · static.</span></p>

At High, three<!-- N:DX-13 --> replicate contrasts of survival between $\kappa_B = 1.0$<!-- N:CB-1 --> and $\kappa_B = 0$ are negative three times out of three<!-- N:CB-5 --> (Figure 7(b); trained policies, 500 updates<!-- N:DX-40 -->, $d_p = 0.5$<!-- N:ENV-1 -->, Coupling A on). They are −6.87 and −10.66 points<!-- N:DX-13 --> for the grid's two seeds<!-- N:DX-40 --> and −4.70 points for a same-seed retrain<!-- N:DX-13 -->, each one run per cell<!-- N:DX-13 --> and without an interval. The grid's first estimate, the mean of its two seeds<!-- N:CB-6 -->, was −8.8 points<!-- N:CB-6 -->. The High survival floor, sd 6.21 points<!-- N:CB-7 -->, was measured later on four identical runs<!-- N:DX-40 --> of a separate artifact: a reference scale (cross-artifact). The first estimate is 1.41 times<!-- N:CB-5 --> this floor and the replicates' mean about 1.19 times<!-- N:CB-5 --> it. We report a consistent effect of modest size; the first analysis graded it "strong" against a two-seed<!-- N:DX-38 --> spread, a label retracted under the rule of §8.1. Completion is not resolved, since its contrast flipped sign on the same-seed retrain<!-- N:CB-8 -->.

At Medium, the severity of the held-out test configuration (β = 0.49<!-- N:CAL-3 -->), Coupling B's own survival effect in the same grid was −0.03 points<!-- N:CB-9 -->. It was judged against a three-seed<!-- N:CB-9 --> spread, $\sigma_{\mathrm{seed}} = 0.72$ points<!-- N:CB-9 -->, with no measured floor; the Medium survival floors measured later, on two<!-- N:METH-1 --> GPUs, are 1.29 and 1.30 points<!-- N:METH-1 -->. Coupling B's measured survival cost is therefore at High, while §9's test runs at Medium (§10, item 1).

The masking concentrates on moments of danger, alive agent-steps with a Burning cell inside the agent's crop. In the $\kappa_B = 1.0$<!-- N:CB-1 --> arm the masked share of the crop at danger moments is 0.0809, 0.0560 and 0.2424<!-- N:DX-11 --> at Low, Medium and High, against 0.00068, 0.00249 and 0.01559<!-- N:DX-11 --> over all alive agent-steps: 118, 22 and 16 times<!-- N:CB-10 --> more concentrated (ratios of unrounded shares; Figure 7(a)). Within trained policies at 500 updates<!-- N:DX-40 --> the attenuation was not behaviourally suppressed: the coupled policies' masking ceiling, which does not depend on $\kappa_B$, sat at or above its random-policy value at every severity.

### 6.5 The co-active counter, and what it can see

The environment logs, at every step, the number of collapse-seeded ignitions inside an alive agent's crop, within Chebyshev radius 4<!-- N:DX-37 --> of its post-step position<!-- N:CO-4 -->. It was meant to catch both couplings at once, but only Coupling A produces those ignitions and $\kappa_B$ does not enter the count, so the counter is co-active only in all-on configurations. In a training mixture it reads the Coupling-A marginal alone, which is why the mediation analysis registered on it is void (§9.2).

{% include figure.html path="assets/img/submission/fig05_coactive.png" class="img-fluid" alt="Three bar charts, one per severity, of the share of episodes with zero, one, two, three, and four or more co-active events." caption="Figure 8. The co-active counter per episode, by severity." %}

<p class="caption">Share of episodes with each number of co-active events in the coupled arm of the Coupling-B calibration grid (labelled m44), seeds pooled; both couplings are on in every cell. The figure cannot show a floor, since none exists for this counter, or a training mixture (§6.5). <span class="figure-note">Status: descriptive; trained policies, 500 updates<!-- N:DX-40 -->; no floor · static.</span></p>

In these all-on cells the counter is rare and bursty (Figure 8). The share of episodes with no co-active event is 0.563, 0.578 and 0.883<!-- N:CO-2 --> at Low, Medium and High, the mean at Medium is 0.64<!-- N:CO-1 --> events per episode, and the variance-to-mean ratio, 1.31 to 1.40<!-- N:CO-3 -->, exceeds the Poisson value of 1. Low and Medium are indistinguishable and High is lower, because seeded ignitions fall while the near-agent share stays in its range (§5.3).
