<!-- PAPER V2 DRAFT (PAPER V2 ruling, 2026-10-11): builder-drafted, not owner-approved -->

## Appendices

<!-- STUB-SPEC
PURPOSE: The appendix opening and Appendix A. First an appendix index, one line per appendix A to I (it replaces section 11's list, P2-h). Then the proofs, each stated once: the statements stay in the body ("Statement: §3.1" and so on; claims review C-34), and Appendix A says where it departs from the formal specification.
WRITER: W6. BUDGET (this file): about 800 prose words (index about 80; proofs about 720). The appendix as a whole: 2,000 prose words excluding verbatim quotations and tables (STRUCTURE.md section 6), split 800 here, 350 in W5's B and C, 850 in D to I.
INDEX (appendix headings and letters, STRUCTURE.md section 2): A Proofs; B Locks and hyperparameters; C Floors; D The frozen analysis plan; E The registered outcome branches; F Grid provenance; G Gamma over the final half of training; H The secondary design; I Trained-policy episodes. B and C are W5's file; D to I are W6's next file. Plain text cross-references (INTERFACE).
APPENDIX A CONTENT: Proposition 1's proof, once (the demo's sections/12_appendix.md:11 with the reachable-set argument), with the departure note (the formal specification says S and Ω_i are finite; with the real-valued smoke field that holds only on the reachable states, which is all the argument uses: OI-2). Proposition 2's proof (the coupling) and the implementation-exactness paragraph (home: che/env/hazard.py:8-16; grassberger1983). Proposition 3's proof without "The divergence rate is Corollary 1(3)" (C1), and the finite-protocol details (DX-409: cluster mass at β = 0.43 saturates by an age of about 64 steps; the four measured factors compose to the observed slope within Monte Carlo error at both grid sizes). Theorem 1's proof (home; the demo's 12:29). Proposition 4, by its new name: the proof idea without a constant (the return difference is bounded by telescoping the evaluation operators of the two models along the trajectory distribution; the observation term enters because the policy acts through the observation), and why every ISO configuration differs from θ* on the states where both couplings act at once (a collapse increment next to Fuel with an agent within attenuation range); no display with the constant or with the per-agent maximum, no ISO-against-JOINT contrast, no lemma cited by name (C3, N6, P3-N7; Q4i); a pointer to section 9.1's honesty note. Remark 2′: the extra step (the idling correction is largest at low κ_B and tends to 1 as κ_B grows) and the toy's constants moved from section 7 (DX-15).
REQUIRED FACTS: DX-15, DX-409, CAL-3. No other record number belongs here.
CITATIONS: grassberger1983, pynadath2002 (Remark 2′ pointer).
FIGURES, LISTINGS: none. LATEX: MathJax per BRIEF section 14; proofs end with \blacksquare; no \label; absolute values with \lvert \rvert.
FIX-LIST AND FINDINGS ITEMS OWNED: C1 (Prop. 3's proof), C3 (Prop. 4's name and content), OI-2 (the departure note), P2-9 (Prop. 1's proof once), P2-h (index, slug-safe headings), LEN (no restated statements: C-34), P3-N7, N6, Q4i, Q4k.
DEMO KEEPS (sections/12_appendix.md:5-37): the proofs of Props. 1 to 3 and Thm. 1; the Prop. 1 departure note; the Remark 2′ step. CHANGES: "Statement: §n" in place of restated statements; Prop. 3's rate line out; Prop. 4 renamed, no constant. DROPS: "irreducible"; the divergence-rate line.
NOT HERE: any statement already in the body, restated; any number outside the ledger and the supplement; a reinterpretation of a theorem's hypotheses (Q13, Q23 are the owner's).
-->

- Appendix A: proofs.
- Appendix B: locks and hyperparameters.
- Appendix C: reproducibility floors.
- Appendix D: the frozen analysis plan, quoted.
- Appendix E: the registered outcome branches.
- Appendix F: grid provenance and blinding.
- Appendix G: Γ over the final half of training.
- Appendix H: the secondary design.
- Appendix I: trained-policy episodes.

### A Proofs

Each statement is in the body, in the section named. The proofs follow the formal specification in the notation of Definition 1, and departures from it are noted.

**Proposition 1.** Statement in §3.1.

**Proof.** Each factor of $T_\theta$ is a conditional kernel, measurable in its conditioning variables, all of which are components of $(s, a)$ or of already-sampled components of $s'$. The dependence of $T_H$ on $c'$ and of $T_K$ on $x'$ is a sequential composition within one time step. Sample $c' \sim T_C(\cdot \mid c, x)$, then $h' \sim T_H(\cdot \mid h, c, c')$, then $\rho' = T_\rho(\rho, h')$ (deterministic), then $x' \sim T_X(\cdot \mid x, a, h', c')$, then $k' \sim T_K(\cdot \mid x')$. A composition of Markov kernels is a Markov kernel on the product space, so $T_\theta$ is a valid transition kernel on $\mathcal{S}$ and $(s_t)$ is Markov. The action sets are finite, every stochastic factor and the reset distribution have finite support, and $\rho$ evolves deterministically from $\rho_0 = 0$. The states and observations reachable within the horizon therefore form finite sets; restricted to them, $\mathcal{M}_\theta$ is a finite Dec-POMDP, and optimal finite-horizon joint policies exist by the standard argument. $\blacksquare$

The formal specification states that $\mathcal{S}$ and $\Omega_i$ are finite. With the real-valued smoke field $\rho \in \mathbb{R}_{\ge 0}^G$ in the state, that holds only for the states and observations reachable within the horizon, which is all the argument uses.

**Proposition 2.** Statement in §3.2.

**Proof (coupling).** Attach to each unordered edge $e = \{g, g'\}$ an independent $B_e \sim \mathrm{Bernoulli}(\beta)$, and declare that a transmission attempt across $e$ succeeds if and only if $B_e = 1$. Each edge is attempted at most once: when one cell of $e$ first Burns while the other is Fuel, one attempt occurs; afterwards the burning endpoint is Burnt, which is absorbing. If the other endpoint later Burns via a different path, its neighbour across $e$ is already Burnt, so no second attempt occurs. Run with the variables $\{B_e\}$, the fire therefore burns exactly the connected component of the origin in the subgraph of open edges $\{e : B_e = 1\}$, which is the bond-percolation cluster. $\blacksquare$

This is the coupling behind the correspondence that §3.2 cites<d-cite key="grassberger1983"></d-cite>, and the implementation realizes it exactly (`che/env/hazard.py:8-16`). It draws one uniform per cell and incoming direction, which maps one-to-one to the ordered pairs of Definition 3. With a burn time of one step, each unordered edge sees at most one attempt, so these uniforms are the coupling's per-edge variables.

**Proposition 3.** Statement in §5.2.

**Proof.** Each collapse seed grows, by Proposition 2, a burnt cluster equal in distribution to a bond-percolation cluster, of expected size $\chi(\beta)$. By linearity of expectation over the Binomial or Poisson number of seeds, the total expected burnt area is $\lambda_A T \chi(\beta)$ when clusters are disjoint; overlaps only remove double counting, which gives the upper bound in general. $\blacksquare$

The formal specification adds a divergence rate near the critical point, which rests on critical exponents the paper does not state (§4.1). The equality is approached only when four conditions are matched, each with a known sign: an unconditional cluster-mass reference (a spanning-conditioned one underestimates it), seed location (boundary clipping lowers the mass of uniformly placed seeds), seed age (cluster mass at β = 0.43<!-- N:CAL-3 --> saturates by an age of about 64 steps<!-- N:DX-409 -->), and sparsity (sibling seeds and cluster overlap deflate the measured slope). In the Proposition 3 measurements (§5.2) the four factors compose to the observed slope within Monte Carlo error.

**Theorem 1.** Statement in §6.2; items (1)–(3) below refer to it.

**Proof.** *(1)* With zero slack, the only decision is the corridor choice at $b$; waiting or probing is impossible within $T$. If informed (probability $q$), taking the corridor other than $Z$ succeeds with probability 1; if not, both corridors are exchangeable given the history, and any choice succeeds with probability $\tfrac12$. Hence $J^* = q + (1-q)\tfrac12 = \tfrac12 + \tfrac{q}{2}$, and no policy exceeds this, since success requires information or a lucky guess. *(2)* In the fixed-map environment the signal is uninformative, so the signal-blind policy is among the optimal ones there; on $E_{2C}$ it succeeds if and only if $Z = z_0$, with probability $\tfrac12$. *(3)* Each factor $(1 - e^{-\kappa_B j})$ is continuous and strictly increasing in $\kappa_B$ on $(0, \infty)$, so the finite product is too, and $q$ is continuous and strictly decreasing. The product tends to 0 as $\kappa_B \to 0$ and to 1 as $\kappa_B \to \infty$. $\blacksquare$

**Proposition 4 (A transfer bound for a fixed policy).** Statement in §9.1.

**Proof idea.** The difference between the two returns is bounded by telescoping the evaluation operators of the two models along the trajectory distribution; the observation term enters because the policy acts through the observation. Every configuration in $\Theta_{\mathrm{iso}}$ differs from $\theta^*$ where both couplings act at once. Take a state with a collapse increment next to Fuel and an agent within attenuation range. There $T_{\theta^*}$ places mass of order $\kappa_A$ on ignition transitions that a configuration with $\kappa_A = 0$ places elsewhere, and the observation kernels differ when $\kappa_B$ differs.

The formal specification displays the bound with an explicit constant and concludes more about ISO's slack than an upper bound can show; the paper states the bound in words and draws no such conclusion (§9.1).

**Remark 2′.** Stated in §7.2, after Pynadath and Tambe<d-cite key="pynadath2002"></d-cite>. One step is not spelled out in §7. Let $\tilde q$ be the probability of being informed under the best idling schedule. The commitment draws have different optical depths, so as $\kappa_B \to \infty$ the lowest-depth draw dominates both products and $\tilde q / q \to 1$. The correction peaks at moderate $\kappa_B$, and its relative bite on the value of communication is largest at low $\kappa_B$, where $q$ is near 1. In the two-agent toy, which is not CHE (4096 episodes and 8192 Monte Carlo draws per point<!-- N:DX-15 -->), $\tilde q / q$ is 1.126 at $\kappa_B = 1.0$ and peaks at 1.235 near $\kappa_B = 2$<!-- N:DX-15 -->. The correction removes 79 %, 54 % and 7 % of $\mathrm{VoC}_{\mathrm{gated}}$ at $\kappa_B$ = 0.5, 1.0 and 3.0<!-- N:DX-15 -->. The check that the denied arm under the no-idle schedule matches $\tfrac12 + \tfrac12 q$ passes (largest absolute z 0.44; χ² 0.51 on 8 degrees of freedom<!-- N:DX-15 -->), and the arm with free communication scores 1.0000 at every $\kappa_B$<!-- N:DX-15 -->.
