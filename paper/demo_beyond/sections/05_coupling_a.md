<!-- BUILDER-WRITTEN DEMONSTRATION (DEMONSTRATION DRAFT ruling, 2026-10-11); not the owner's text -->

## 5 Coupling A: collapse seeds the fire

Coupling A lets structural failure feed the fire: a cell that collapses can ignite the fuel around it. In one illustrative random-policy episode, Figure 1's event track marks the collapse events and the collapse-seeded ignitions they caused (press <kbd>]</kbd> there to jump between them). Figure 6 counts the same events under trained policies, beside the two runs that test the theory.

<figure class="l-page">
  <iframe src="{{ 'assets/html/submission/coupling_a_explorer.html' | relative_url }}" width="100%" height="680" style="border:none" title="Coupling A explorer: collapse-seeded ignitions by severity, their share near agents, and the two Proposition 3 runs" loading="lazy"></iframe>
  <figcaption><strong>Figure 6.</strong> Coupling A under trained policies, and the two runs that test Proposition 3. <em>Top left:</em> collapse-seeded ignitions per episode at Low, Medium and High (β = 0.43 / 0.49 / 0.70<!-- N:CAL-3 -->) in the κ<sub>B</sub> = 1.0<!-- N:CB-1 --> arm of the Coupling-B grid m44 (4.05 / 3.41 / 0.84, a 4.83× fall<!-- N:CA-4 -->) and the κ<sub>A</sub>-on arm of the Coupling-A grid m35 (4.08 / 3.42 / 0.83, 4.92×<!-- N:CA-5 -->). <em>Top right:</em> the share of those ignitions inside an alive agent's 9 × 9<!-- N:ENV-6 --> crop, for all nine measured cells, with their range [0.164, 0.203]<!-- N:CA-6 --> as a band. <em>Bottom left:</em> the first Proposition 3 run, an L = 64 sweep with no agents (κ<sub>A</sub> 0.02, f<sub>weak</sub> 0.4<!-- N:CA-2 -->): burnt cells against realized seeded ignitions, through-origin fit R² 0.998<!-- N:CA-2 -->. <em>Bottom right:</em> the second run, a separate L = 32 test (κ<sub>A</sub> 0.003<!-- N:CA-3 -->) against a protocol-matched reference, given as values because it has no committed data file: ratio 0.992, inside [0.90, 1.02], R² 0.9995<!-- N:CA-3 -->. Neither run uses the locked parameters. The figure cannot show a floor for any trained-policy contrast: the m44 and m35 grids have no identical-run sets, so their whiskers are min–max over training seeds. <span class="figure-note">Status: reference scale (cross-artifact) for any floor; trained policies, 500 updates<!-- N:DX-40 -->; spreads are seed ranges · Proposition 3 panels: handshake runs, no agents · Interact: hover or tab to a point for its value; open “table view” for every number.</span></figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/coupling_a_explorer.png" class="img-fluid" alt="Collapse-seeded ignitions per episode at three severities for two trained grids, the share of them near agents, and the two Proposition 3 handshake runs shown separately." caption="Static companion of Figure 6 for the printed PDF." %}
</div>

### 5.1 Definition and implementation

**Definition 5 (Coupling A, as implemented).** Let $w(g) \in \{0,1\}$ mark weak terrain, a spatially clustered fraction $f_{\mathrm{weak}}$ of the cells drawn once per episode, and let $o_t(g) \in \{0,1\}$ indicate that at least one alive agent stands on cell $g$ before the step. An intact cell collapses at step $t$ with probability

$$
\lambda_t(g) = \big(\lambda_0 + \lambda_{\mathrm{load}}\,o_t(g)\big)\,w(g),
$$

so a cell that is not weak never collapses, and collapsed is absorbing. Coupling A then ignites, with probability $\kappa_A$, each cell that is still Fuel after this step's spread and lies within Chebyshev distance $r_A$ of a cell that collapsed in this step. The fire kernel therefore reads the collapse increment $c' - c$, not the stock of collapsed cells; a seeded cell is Burning in $h'$ and spreads from the next step on. Setting $\kappa_A = 0$ recovers the uncoupled fire kernel $T_H^{\beta,0}$: the ablation "no Coupling A" is a nested model of the full system, not a different environment.

The theory phrases the impulse per collapse event; the implementation draws one uniform per cell, so a cell in range of two new collapses is tried once, and the two rules coincide wherever seeding neighbourhoods do not overlap. The locked values, chosen from a random-policy calibration against target bands for collapses, seeded ignitions and collapse deaths per episode, are $(f_{\mathrm{weak}}, \lambda_0, \lambda_{\mathrm{load}}, \kappa_A, r_A) = (0.15,\ 5\times 10^{-5},\ 4\times 10^{-4},\ 0.06,\ 1)$<!-- N:CA-1 -->, so the seeding neighbourhood is a 3 × 3<!-- N:DX-37 --> block.

Agents influence collapse, weakly and indirectly. An occupied weak cell collapses nine times<!-- N:CA-8 --> as often as an empty one, but most collapses happen with no agent present: without load the locked parameters give about 7.81<!-- N:CA-9 --> collapses per episode, and agents add about 1 % to that under trained policies (0.4–1.4 %, Phase-3 policies at 500 updates<!-- N:CA-9 -->) and 7.4–8.3 %<!-- N:CA-9 --> under random ones. The fire is not independent of the agents, although ignition is not an action available to them.

Listing 4 is the whole of Coupling A in code.

**Listing 4.** Coupling A: the seeding mask, with its uniforms drawn whatever $\kappa_A$ is.

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

Its last three lines carry the claims: `u` is drawn before anything reads $\kappa_A$, so $\kappa_A = 0$ is the nested model bit for bit under the rule of §3.4; the dilation acts on the increment $c' - c$, so an old collapse seeds nothing; and `hazard.seed_ignitions` lights only cells that are still Fuel, which is where §5.3's fuel limitation enters.

### 5.2 The handshake with Proposition 3

**Proposition 3 (Collapse events dominate hazard exposure; divergence near criticality).** Work in the subcritical regime $\beta < \beta_c$ with $\iota = 0$, and suppose collapse events arrive at rate $\lambda_A$ per step, each seeding one ignition at a uniformly located Fuel cell, with seeded clusters pairwise disjoint (the sparse regime, $\lambda_A T \chi(\beta) \ll \lvert G \rvert$, the number of cells). Then the expected burnt area $B_T$ by time $T$ satisfies

$$
\mathbb{E}[B_T] = \lambda_A T\,\chi(\beta)\,\big(1 + o(1)\big), \qquad \text{and in general} \quad \mathbb{E}[B_T] \le \lambda_A T\,\chi(\beta),
$$

where $\chi(\beta)$ is the mean percolation cluster size. Consequently the marginal hazard exposure per unit of structural instability, $\partial\,\mathbb{E}[B_T]/\partial\lambda_A = T\chi(\beta)$, diverges as $\beta \uparrow \beta_c$ like $\lvert \beta - \beta_c \rvert^{-43/18}$.

The proof (Appendix A) grows each seed into a bond-percolation cluster by Proposition 2 and sums expectations; overlaps only remove double counting, and the divergence is Corollary 1. In this regime collapse is the fire's only birth channel, and near criticality one collapse has a divergent expected burnt area.

**Remark (finite-protocol corrections).** The equality branch of Proposition 3 is approached only under (i) an unconditional cluster-mass reference (a spanning-conditioned estimate underestimates it); (ii) a matched distribution of seed locations (boundary clipping lowers the mass of uniformly located seeds below a centre-seeded reference); (iii) matched seed ages (seeds born uniformly in time are age-averaged); and (iv) sparsity in both same-event sibling seeds and cross-cluster overlap, which deflate the measured slope and vanish as $\kappa_A, \lambda \to 0$. Every correction has a known sign.

We tested the proposition twice and report the two runs separately; they differ in grid size, regime and reference, and neither uses the locked parameters. Both run the fire and structure kernels with no agents and no primary ignition at the Low level, $\beta = 0.43$ with $\iota = 0$<!-- N:DX-304 -->, inside the proposition's subcritical regime. The first, a dense GPU sweep at L = 64 with $\kappa_A = 0.02$ and $f_{\mathrm{weak}} = 0.4$<!-- N:CA-2 -->, sweeps $\lambda_0$ and fits burnt area against the realized number of seeds through the origin: the relation is linear, $R^2 = 0.998$ over a 14× range of the expected seed count<!-- N:CA-2 -->. Its slope lies below the naive cluster-size reference, on the side the inequality permits, and the remark's four corrections compose to it within Monte Carlo error. The second, a slow CPU test in the suite at L = 32 in a purified regime ($\kappa_A = 0.003$<!-- N:CA-3 -->), computes its reference inside the test under the sweep's own protocol: slope over matched reference 0.992, inside the band [0.90, 1.02], $R^2 = 0.9995$<!-- N:CA-3 -->.

### 5.3 Under trained policies the coupling limits itself

Proposition 3 concerns the regime below criticality; above it, the fire removes what the coupling needs. Under trained policies (the Coupling-B grid m44, $\kappa_B = 1.0$ arm, 500 updates<!-- N:DX-40 -->), collapse-seeded ignitions per episode are 4.05, 3.41 and 0.84 at Low, Medium and High, a 4.83-fold fall<!-- N:CA-4 -->. The Coupling-A grid m35, with different policies and an earlier observation version, replicates it: 4.08, 3.42 and 0.83, a 4.92-fold fall<!-- N:CA-5 -->. Collapse never reads $\beta$; what changes with severity is where the seeds land. At High the supercritical fire burns 98.3 %<!-- N:CAL-3 --> of the arena in calibration (no agents), so most seeding attempts fall on burnt cells and the Fuel-only rule filters them out. With Proposition 3 this places the ignition channel's leverage below and near criticality: collapse seeds the most fire where the fire is otherwise rare, and at High the channel is marginal by construction (§10). That holds for the ignition channel; the Coupling-A grid's survival contrasts, on two seeds per arm<!-- N:CA-7 --> and with no floor, do not show where its effect on outcomes is largest.

The fuel limitation behind this fall was recorded before any trained policy was measured. At the Coupling-A lock (2026-07-21<!-- N:DX-401 -->), the random-policy calibration put seeded ignitions at High about 5.7 times<!-- N:DX-9 --> below Low at every $\kappa_A$ tried, and the lock recorded this as the fuel-exhaustion self-limitation of the ignition channel. A later prediction, registered before the analysis that produced the numbers above but after the trained results existed, had three parts: Coupling A is fuel-limited at High; the co-active count of §6 need not be monotone in severity; Medium may be its peak. The first is confirmed by the 4.83-fold fall<!-- N:CA-4 --> (its answer was already on record in the Phase-3 and Phase-4 reports, as that analysis notes). The second is not supported: the count is monotone non-increasing. The third is refuted: Low and Medium are indistinguishable<!-- N:DX-9 -->.

The fall happens upstream of the agents. The co-active count is the number of seeded ignitions times the share of them inside an alive agent's crop, and that share is flat: across all nine measured cells (both $\kappa_B$ arms of m44 and the $\kappa_A$-on arm of m35, at three severities) it lies in [0.164, 0.203]<!-- N:CA-6 -->. Severity changes how much seeded fire there is, not how much of it reaches an agent's view.

At Low the coupling moves survival off its ceiling. In the Coupling-A grid (M3.5: $\kappa_A$ from 0 to 0.06<!-- N:CA-1 -->, two seeds per arm<!-- N:CA-7 -->, 500 updates<!-- N:DX-40 -->), Low survival falls from 0.979 to 0.961<!-- N:CA-7 --> and fire deaths per episode rise from 0.062 to 0.229, 3.7-fold<!-- N:DX-10 -->. The policies do not respond by avoiding weak cells: weak-cell occupancy at Low is higher with the coupling on, by 0.054<!-- N:CA-7 -->, with no overlap between the arms' seed ranges; on two seeds per arm this is suggestive, not conclusive.

No contrast in this section is graded against a floor on its own artifact. The m44 and m35 grids have no identical-run sets, so their spreads are seed ranges and any floor beside them would be a reference scale (cross-artifact) (§8.6). The 4.83-fold fall<!-- N:CA-4 --> lies far outside those ranges and replicates on a second grid; the Low survival drop and the occupancy shift rest on two seeds per arm. §6 returns to the near-agent share: the co-active counter counts exactly these ignitions.
