<!-- PAPER V2 DRAFT (PAPER V2 ruling, 2026-10-11): builder-drafted, not owner-approved -->

## 5 Coupling A: collapse seeds the fire

<!-- STUB-SPEC
PURPOSE: Coupling A lets structural collapse seed the fire. State Def. 5 as implemented; give the agents' weak, indirect influence on collapse (the home of those numbers); show the coupling in code (Listing 4); state Prop. 3's linear scaling and report its two handshake runs as two; report that under trained policies the coupling limits itself at High (the home of the 4.83-fold fall), as the random-policy calibration had already shown, with the later prediction's three parts; the near-agent share; Low survival off its ceiling; and that no contrast here has a floor of its own.
SUBSECTIONS (H3, as the demo's): 5.1 Definition and implementation; 5.2 The handshake with Proposition 3; 5.3 Under trained policies the coupling limits itself.
WRITER: W4. BUDGET: 850 prose words (the demo's: 1,307); Figure 6 caption at most 120 words.
REQUIRED FACTS: CA-1 (f_weak 0.15, λ₀ 5e-5, λ_load 4e-4, κ_A 0.06, r_A 1; locked 2026-07-21, DX-401); DX-37 (seeding neighbourhood 3 × 3); CA-8 (an occupied weak cell collapses nine times as often per step; DERIVED, load is boolean); CA-9 (about 7.81 collapses per episode with no load; load adds 0.4 to 1.4 % under the trained Phase-3 policies, 500 updates, and 7.4 to 8.3 % as an increase under random policies, 6.9 to 7.6 % as a share; this is the home, so OWNER ITEM 4 resolves here); DX-304 (both handshake runs: β = 0.43, ι = 0, no primary ignition, no agents); CA-2 (the first run: L = 64 sweep, κ_A 0.02, f_weak 0.4, R² 0.998 over a 14× range of the expected seed count; not the locked parameters); CA-3 (the second: L = 32 CPU test, κ_A 0.003, ratio 0.992 inside [0.90, 1.02], R² 0.9995; a different run, report text only); DX-40 (trained policies, 500 updates); CA-4 (the Coupling-B calibration grid, κ_B = 1.0 arm: 4.05 / 3.41 / 0.84 seeded ignitions per episode, a 4.83-fold fall); CA-5 (the Coupling-A calibration grid replicates: 4.08 / 3.42 / 0.83, 4.92-fold); CAL-3 (High burns 98.3 % of the arena in calibration, no agents); DX-9 (about 5.7-fold already at the random-policy calibration, recorded at the lock as fuel limitation before any trained policy; the later prediction's three parts: fuel-limited at High confirmed, "need not be monotone" not supported, "Medium is the peak" refuted); CA-6 (the near-agent share in [0.164, 0.203] across nine cells); CA-7 (Low survival 0.979 to 0.961, two seeds per arm; weak-cell occupancy higher by 0.054 with the coupling on); DX-10 (Low fire deaths 0.062 to 0.229 per episode, 3.7-fold); CB-1 (κ_B = 1.0 in Figure 6's caption).
FIGURES: Figure 6, coupling_a_explorer.html, companion coupling_a_explorer.png, height 680, carried below. Caption at most 120 words, numbers the figure prints not repeated (rule R3); it glosses "m44" and "m35" as printed (the Coupling-B and Coupling-A calibration grids) and "card" if printed; status "reference scale (cross-artifact)" for any floor; the two Prop. 3 runs shown apart; it cannot show a floor for any trained-policy contrast. A pointer to Figure 1's event track (press ] in Figure 1) replaces any deep link (A6).
LISTINGS (carried below, exact lines): Listing 4, che/env/structure.py:83-102: the uniforms are drawn before anything reads κ_A, so κ_A = 0 is the nested model bit for bit; the dilation acts on the increment c′ − c; seeding lights only cells still Fuel (the fuel limitation of section 5.3). Prose must not echo "Invariant #3" from the code comment.
LATEX: Def. 5's collapse probability (one display); Prop. 3 (one display: the linear form and the inequality). Prop. 3 loses "diverges as β ↑ β_c like the 43/18 power" (C1). It makes no divergence claim on the arena (P3-N5); a divergence on ℤ² would need a verified source, and none is recorded, so by default the divergence clause goes. The finite-protocol remark in one sentence (its four corrections have known signs); details in Appendix A.
HONESTY LINES AND REGISTERED STRINGS: "reference scale (cross-artifact)"; the handshake is two runs, not one, neither at the locked parameters; no m44 or m35 contrast is graded against a floor of its own; seeded-ignition figures are the Coupling-B grid's (CA-4), not the Coupling-A grid's.
FIX-LIST AND FINDINGS ITEMS OWNED: C1 knock-on (Prop. 3's rate); P3-N5 (no divergence on the finite arena); P3-N6 (class B part: scope "collapse is the fire's only birth channel" to the tested regime with no primary ignition, DX-304; the restatement of the proposition is Q13, not applied); OI-1 (the timing paragraph: what the lock recorded before training was the fuel limitation, not the trained fall); OI-4 (the home of the influence numbers); F5 (m44, m35, M3.4, M3.5, M3.3 named as studies); LEN (one sentence per handshake run; the Low paragraph and the floor paragraph to one sentence each); P2-k; Q13, Q4g.
STYLE: no "hazard begets hazard" without the agent-influence sentence; no aphoristic closers (P3-§6); sentences of at most 40 words.
DEMO KEEPS (sections/05_coupling_a.md): Def. 5 as implemented; Listing 4 and its gloss; Prop. 3's statement minus the rate; the remark in one sentence; the two runs reported separately; section 5.3's finding, its replication, the corrected timing and the prediction's three parts; the near-agent share. CHANGES: the rate and the divergence go; names become plain; the influence paragraph becomes the one home of CA-8 and CA-9. DROPS: "near criticality one collapse has a divergent expected burnt area"; repeated statements of the 4.83-fold fall outside this section (they point here).
NOT HERE: one Prop. 3 run; the locked parameters in the handshake; floor-graded seeded-ignition contrasts; that Medium is the co-activity peak; the Coupling-A grid as the source of the 4.83-fold figure; that agents avoid weak cells; "as predicted before measurement".
DEPENDENCIES: section 6.5 (the counter counts these ignitions near agents); section 9.2 (the High readout and mediation point here); section 10 item 1 (A marginal at High).
-->

Coupling A lets structural collapse feed the fire. Figure 1's event track marks one random-policy episode's collapses and the ignitions they seeded (press <kbd>]</kbd> in Figure 1 to step between them); Figure 6 counts them under trained policies.

<figure class="l-page">
  <iframe src="{{ 'assets/html/submission/coupling_a_explorer.html' | relative_url }}" width="100%" height="736" style="border:none" title="Coupling A explorer: collapse-seeded ignitions by severity, their share near agents, and the two Proposition 3 runs" loading="lazy"></iframe>
  <figcaption><strong>Figure 6.</strong> Coupling A under trained policies, and the two Proposition 3 runs. <em>Top:</em> collapse-seeded ignitions per episode by severity, and their share inside an alive agent's crop, in the Coupling-B and Coupling-A calibration grids (labelled m44 and m35; Phases 3 and 4 are calibration stages). Whiskers are min–max over training seeds; neither grid has identical reruns, and nothing shown has a floor. <em>Bottom:</em> the two runs, kept apart, neither at the locked parameters; the second (v2, a revised suite test) has no committed data file and is shown as values. <span class="figure-note">Status: top, trained policies, 500 updates<!-- N:DX-40 -->, seed ranges; bottom, no agents · Interact: hover or tab to a point; table view.</span></figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/coupling_a_explorer.png" class="img-fluid" alt="Collapse-seeded ignitions per episode at three severities for two trained grids, the share of them near agents, and the two Proposition 3 handshake runs shown separately." caption="Static companion of Figure 6 for the printed PDF." %}
</div>

### 5.1 Definition and implementation

**Definition 5 (Coupling A, as implemented).** Let $w(g) \in \{0,1\}$ mark weak terrain, a spatially clustered fraction $f_{\mathrm{weak}}$ of the cells drawn once per episode, and let $o_t(g) \in \{0,1\}$ indicate that at least one alive agent stands on cell $g$ before the step. An intact cell collapses at step $t$ with probability

$$
\lambda_t(g) = \big(\lambda_0 + \lambda_{\mathrm{load}}\,o_t(g)\big)\,w(g),
$$

so a cell that is not weak never collapses, and collapse is absorbing. Coupling A then ignites, with probability $\kappa_A$, each cell that is still Fuel after this step's spread and lies within Chebyshev distance $r_A$ of a cell that collapsed in this step. The fire kernel thus reads only the collapse increment $c' - c$, and a seeded cell is Burning in $h'$. Setting $\kappa_A = 0$ recovers the uncoupled fire kernel $T_H^{\beta,0}$, so the ablation "no Coupling A" is a nested model of the full system.

The theory states the impulse per collapse event; the implementation draws one uniform per cell, and the two rules coincide wherever seeding neighbourhoods do not overlap. The values, locked on 2026-07-21<!-- N:DX-401 -->, are $(f_{\mathrm{weak}}, \lambda_0, \lambda_{\mathrm{load}}, \kappa_A, r_A) = (0.15,\ 5\times 10^{-5},\ 4\times 10^{-4},\ 0.06,\ 1)$<!-- N:CA-1 -->, so the seeding neighbourhood is a 3 × 3<!-- N:DX-37 --> block.

Agents influence collapse, weakly and indirectly. Occupancy enters as a yes-or-no load: a weak cell with any agent on it collapses nine times<!-- N:CA-8 --> as often as an empty one. Without load, the locked parameters give about 7.81<!-- N:CA-9 --> collapses per episode. Load adds 0.4 to 1.4 %<!-- N:CA-9 --> to that count under trained policies (the Coupling-A calibration grid of §5.3) and 7.4 to 8.3 %<!-- N:CA-9 --> under random ones, which is 6.9 to 7.6 %<!-- N:CA-9 --> of all collapses. Agents cannot ignite a cell, but where they stand changes collapse rates, and a collapse can seed fire.

**Listing 4.** Coupling A's seeding mask, with its uniforms drawn whatever $\kappa_A$ is.

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

The uniforms `u` are drawn before anything reads $\kappa_A$, so $\kappa_A = 0$ is the nested model bit for bit under the rule of §3.4. The mask then goes to `hazard.seed_ignitions`, which lights only cells still Fuel; this is where the fuel limitation of §5.3 enters.

### 5.2 The handshake with Proposition 3

**Proposition 3 (Collapse events dominate hazard exposure).** Work in the subcritical regime $\beta < \beta_c$ with $\iota = 0$, and suppose collapse events arrive at rate $\lambda_A$ per step, each seeding one ignition at a uniformly located Fuel cell, with seeded clusters pairwise disjoint (the sparse regime, $\lambda_A T \chi(\beta) \ll \lvert G \rvert$, the number of cells). Then the expected burnt area $B_T$ by time $T$ satisfies

$$
\begin{aligned}
\mathbb{E}[B_T] &= \lambda_A T\,\chi(\beta)\,\big(1 + o(1)\big), \\
\text{and in general} \quad \mathbb{E}[B_T] &\le \lambda_A T\,\chi(\beta),
\end{aligned}
$$

where $\chi(\beta)$ is the mean percolation cluster size. Consequently the marginal hazard exposure per unit of structural instability is $\partial\,\mathbb{E}[B_T]/\partial\lambda_A = T\chi(\beta)$.

The proof (Appendix A) grows each seed into a bond-percolation cluster by Proposition 2 and sums expectations; overlaps only remove double counting. With no primary ignition, as in both runs below, collapse is then the fire's only birth channel. In a finite protocol the equality is approached only with an unconditional cluster-mass reference (a spanning-conditioned one understates the mass), matched seed locations and ages, and sparse seeding; boundary clipping, seed age and overlapping seeds each lower the measured slope (Appendix A).

We tested the proposition in two<!-- N:DX-304 --> runs, neither at the locked parameters, both without agents or primary ignition at the subcritical Low level ($\beta = 0.43$, $\iota = 0$<!-- N:DX-304 -->). The first, a dense sweep on a 64 × 64<!-- N:CA-2 --> grid ($\kappa_A = 0.02$, $f_{\mathrm{weak}} = 0.4$<!-- N:CA-2 -->), fits burnt area against realized seeds through the origin: $R^2 = 0.998$<!-- N:CA-2 --> over a 14×<!-- N:CA-2 --> range of the expected seed count. The second, a slower test in the suite on a 32 × 32<!-- N:CA-3 --> grid ($\kappa_A = 0.003$<!-- N:CA-3 -->), divides its slope by a protocol-matched reference computed inside the test: 0.992<!-- N:CA-3 -->, inside the band [0.90, 1.02]<!-- N:CA-3 -->, with $R^2 = 0.9995$<!-- N:CA-3 -->.

### 5.3 Under trained policies the coupling limits itself

In the Coupling-B calibration grid (500 updates<!-- N:DX-40 --> at each severity, $\kappa_B$ off and on, Coupling A on), the $\kappa_B = 1.0$<!-- N:CB-1 --> arm records 4.05, 3.41 and 0.84<!-- N:CA-4 --> collapse-seeded ignitions per episode at Low, Medium and High, a 4.83-fold<!-- N:CA-4 --> fall (from unrounded counts). The Coupling-A calibration grid ($\kappa_A$ off and on, with other policies, trained on the observation before masking) replicates it: 4.08, 3.42 and 0.83<!-- N:CA-5 -->, a 4.92-fold<!-- N:CA-5 --> fall.

Collapse never reads $\beta$; what changes with severity is where the seeds land. At High the fire burns 98.3 %<!-- N:CAL-3 --> of the arena in calibration, and the Fuel-only rule discards most seeding attempts. This concerns ignitions only: the Coupling-A grid's survival contrasts, on two seeds per arm<!-- N:CA-7 --> and with no floor, cannot locate the coupling's largest effect on outcomes.

This fuel limitation was on record before any trained policy was measured. At the Coupling-A lock, the random-policy calibration put seeded ignitions at High about 5.7 times<!-- N:DX-9 --> below Low at every $\kappa_A$ tried, and the lock recorded it as the fuel-exhaustion self-limitation of the ignition channel. A later prediction was written after the trained results existed and before its own analysis. It held that Coupling A is fuel-limited at High, that the co-active count of §6.5 need not be monotone in severity, and that Medium may be its peak. The 4.83-fold<!-- N:CA-4 --> fall confirms the first, which earlier reports already answered. The count is monotone non-increasing and Low and Medium are indistinguishable, so the second is not supported and the third is refuted.

Across all nine<!-- N:CA-6 --> measured cells (two arms of the Coupling-B grid and one of the Coupling-A grid, at three<!-- N:CAL-3 --> severities), the share of seeded ignitions inside an alive agent's crop stays in [0.164, 0.203]<!-- N:CA-6 -->.

At Low the coupling moves survival in the Coupling-A grid off its ceiling, from 0.979 to 0.961<!-- N:CA-7 -->, as fire deaths per episode rise from 0.062 to 0.229<!-- N:DX-10 -->. Weak-cell occupancy is higher by 0.054<!-- N:CA-7 --> with the coupling on, which suggests, on two seeds per arm<!-- N:CA-7 -->, that the policies do not learn to avoid weak cells. No contrast in this section has a floor on its own artifact, since neither grid has identical reruns; any floor beside them is a reference scale (cross-artifact); see §8.6.
