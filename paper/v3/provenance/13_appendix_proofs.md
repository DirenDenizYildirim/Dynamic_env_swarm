# Provenance: sections/13_appendix_proofs.md

Writer: W2 (Paper v3, step 4, 2026-10-14). Checked with
`paper/v3/src/provenance_check.py --strict 13_appendix_proofs`. "v2 NN:n" is
`paper/v2/sections/NN_*.md` line n (03 environment, 04 severity, 05 Coupling
A, 06 Coupling B, 07 comms, 09 compositional test, 12 appendix). `TF` is
`docs/theory_foundations.md` (not edited). The two alternates
(`alt/13_appendix_proofs.thm1_tf.md`, `alt/13_appendix_proofs.no_prop4.md`)
have their own provenance files and differ only in the blocks named there.

Counts after the fix round (step 4.3): prose **2,345** words (draft1: 2,087;
the fix round added the departures paragraph, RM-2/RM-3/RM-4, about 110
words, the Cor. 1 note, and the lead for Listings 4 and 5 moved here from §3,
RM-1). Draft1's account follows. Draft1 counts: prose 2,087 words against the stub's "about 1,000"
(the index 46; Appendix A 2,041). The overrun is structural: v3 moves into
Appendix A every statement that v2 printed in the body (Props. 1–3, Cor. 1,
Thm. 1, Remark 2′ and the transfer remark: about 780 words), adds the
Thm. 1 departure and the toy's facts V3-E2 asks for (about 330 words), and
keeps v2's Appendix A proofs (965 words in v2) and the Prop. 3 runs that
have no other home now (110 words). Proofs are kept whole at v2's verified
level. Three listings after the fix round (Listings 3–5), byte-identical (`build_v3.py`: 6/6).

Checks run this session: `build_v3.py --out <scratch>` (listings 6/6, 0
unresolved cross-references, no M1 flag here), and with `--alt thm1_tf` and
`--alt no_prop4`. The appendix is outside the terms, dates and caveats scans
by design (`checks/caveats.yaml` appendix_files).

| # | sentence (verbatim) | support | change from v2, and why |
|---|---|---|---|
| 1 | Appendices | framing | kept (v2 12:3) |
| 2 | Appendix A: proofs and formal statements. | framing | edited (v2 12:6): index line for the v3 letters (STRUCTURE §2) |
| 3 | Appendix B: locked constants and hyperparameters. | framing | edited (v2 12:7) |
| 4 | Appendix C: reproducibility floors. | framing | kept (v2 12:8) |
| 5 | Appendix D: the registration timeline. | framing | new: v2 D–F become D (STRUCTURE §2; V3-S2) |
| 6 | Appendix E: additional results of the worked example. | framing | new (v2 G re-lettered; STRUCTURE §2) |
| 7 | Appendix F: the secondary design. | framing | kept (v2 H re-lettered F) |
| 8 | Appendix G: the post hoc interaction check in full. | framing | new (STRUCTURE §2); "post hoc" per the label rule (PR:63-65; caveats C26) |
| 9 | Appendix H: trained-policy episodes. | framing | kept (v2 I re-lettered H) |
| 10 | Appendix I: how the literature search ran. | framing | new (STRUCTURE §2) |
| 11 | Appendix J: how this paper was made. | framing | new (STRUCTURE §2; PAPER V3 item 6) |
| 12 | A Proofs and formal statements | framing | edited (v2 12:16 "A Proofs"; the stub's heading) |
| 13 | This appendix states and proves the results that §3 uses. | framing | edited (v2 12:18 "Each statement is in the body, in the section named."): the statements now live here (stub JOB) |
| 14 | Where a statement departs from the project's theory document (docs/theory_foundations.md in the code supplement), the departure is noted. | docs/theory_foundations.md:142-154; docs/theory_foundations.md:309-318; docs/theory_foundations.md:375-402; docs/theory_foundations.md:610-643; paper/v3/supplement/README.md:54 | edited (v2 12:18 "The proofs follow the formal specification … departures from it are noted"): "the formal specification" → "the project's theory document (docs/theory_foundations.md in the code supplement)", since the supplement ships it by default (supplement README rule D3) while DISPOSITIONS V3Q16's default removes such references; OWNER-PENDING V3Q16 and V3Q23 marked |
| 15 | Definitions and results keep that document's numbers, which the code's docstrings cite; this is why Definition 2 follows Definition 7 in §3 and the only numbered remark is 2′. | che/env/structure.py:83-92; che/env/tasks.py:31-36; CLAUDE.md:1-20 | new, fix round RM-4: the numbering explained once (Definition 2 after Definition 7; the remark numbered 2′); final pass: RC1-27, RM-17: "the one remark is numbered 2′" → "the only numbered remark is 2′" (the transfer remark is unnumbered; true in all three versions) |
| 16 | The definitions of §3 are stated as implemented, and four depart from the document. | framing | new, fix round RM-2 (MUST) and RM-3: the lead of the departures paragraph |
| 17 | Definition 1 draws the observation from the post-step state, smoke included, as the code does. | docs/theory_foundations.md:62-64; CLAUDE.md:40-45; che/env/env.py:394-396 | new, fix round RM-3: TF draws O(o_i ∣ x, h, c, k); the paper follows the code and CLAUDE.md invariant 2 |
| 18 | Definition 3 carries the smoke update and fixes $\iota = 0$, which the document keeps as a parameter $\iota \ge 0$. | DX-1; docs/theory_foundations.md:173-181 | new, fix round RM-3: TF keeps ι ≥ 0 as a knob (TF:180-181); the smoke update lives in TF's Def. 1 and Def. 6 |
| 19 | For Definition 5, the document states the impulse per collapse event; the implementation draws one uniform per cell, and the two rules coincide wherever seeding neighbourhoods do not overlap. | docs/theory_foundations.md:288-292; che/env/structure.py:83-102; paper/v2/sections/05_coupling_a.md:42 | restored from v2 05:42 ("The theory states the impulse per collapse event; …"), fix round RM-2 (MUST); placed here rather than after Definition 5 in §3 because of the page ceiling (RM-1; RM-2's own fallback) |
| 20 | For Definition 7, the document's range-dependent link probability is implemented as a hard Chebyshev range. | docs/theory_foundations.md:563-565; che/env/comms.py:66-96; paper/v2/sections/07_comms.md:35 | restored from v2 07:35 ("The theory's range-dependent link probability is implemented as this hard Chebyshev range."), fix round RM-2 (MUST); placed here for the page ceiling (RM-1) |
| 21 | Proposition 1 (Well-posedness and Markov closure). For every $\theta$, the process $s_t = (x_t, h_t, \rho_t, c_t, k_t, t)$ under any joint policy is a Markov chain, and $\mathcal{M}_\theta$ is a well-defined Dec-POMDP: finite-horizon optimal joint policies exist, and the standard value definitions apply. | docs/theory_foundations.md:137-140 | edited: v2 03:48's statement moved here (stub ORDER: statement and proof once); v2 12:20 "Statement in §3.1" replaced |
| 22 | Proof. | framing | kept (v2 12:22) |
| 23 | Each factor of $T_\theta$ is a conditional kernel, measurable in its conditioning variables, all of which are components of $(s, a)$ or of already-sampled components of $s'$. | docs/theory_foundations.md:142-145 | kept (v2 12:22) |
| 24 | The dependence of $T_H$ on $c'$ and of $T_K$ on $x'$ is a sequential composition within one time step: sample $c' \sim T_C(\cdot \mid c, x)$, then $h' \sim T_H(\cdot \mid h, c, c')$, then $\rho' = T_\rho(\rho, h')$ (deterministic), then $x' \sim T_X(\cdot \mid x, a, h', c')$, then $k' \sim T_K(\cdot \mid x')$. | docs/theory_foundations.md:145-149; CLAUDE.md:40-46 | kept (v2 12:22); v2's two sentences rejoined with a colon (the checker split them at "step. Sample") |
| 25 | A composition of Markov kernels is a Markov kernel on the product space, so $T_\theta$ is a valid transition kernel on $\mathcal{S}$ and $(s_t)$ is Markov. | docs/theory_foundations.md:149-151 | kept (v2 12:22) |
| 26 | The action sets are finite, every stochastic factor and the reset distribution have finite support, and $\rho$ evolves deterministically from $\rho_0 = 0$. | docs/theory_foundations.md:151-153; che/env/env.py:239-245 | kept (v2 12:22) |
| 27 | The states and observations reachable within the horizon therefore form finite sets; restricted to them, $\mathcal{M}_\theta$ is a finite Dec-POMDP, and optimal finite-horizon joint policies exist by the standard argument. | docs/theory_foundations.md:151-154 | kept (v2 12:22; "finite Dec-POMDP" only on the reachable states, v2 OI-2) |
| 28 | $\blacksquare$ | framing | kept |
| 29 | The theory document states that $\mathcal{S}$ and $\Omega_i$ are finite. | docs/theory_foundations.md:151-153 | edited (v2 12:24): "The formal specification" → "The theory document" (V3Q16) |
| 30 | With the real-valued smoke field in the state, that holds only for the states and observations reachable within the horizon, which is all the argument uses. | docs/theory_foundations.md:151-153; che/env/types.py:11 | edited (v2 12:24): "$\rho \in \mathbb{R}_{\ge 0}^G$" dropped (Def. 1 in §3 gives it) |
| 31 | Listing 3, the body of step, follows the factorization; tl is the episode's $\theta$, and no configuration in this paper uses the early frozen control branch. | che/env/env.py:298-358; che/env/env.py:318-322; che/env/config.py:165 | edited (v2 03:54): moved with the listing (STRUCTURE §11 row 14); v2's link-graph, reward-line and observation-stream sentences cut (Appendix A's budget; §3.4 and Table 2 carry them); fix round RM-1: renumbered Listing 3 |
| 32 | Listing 3. One environment step in the order of Proposition 1. | che/env/env.py:298-358 | kept (v2 03:56); listing byte-identical (build: 6/6); fix round RM-1: renumbered Listing 3 (listing order follows the reading order) |
| 33 | Listings 4 and 5 carry two claims of §3. | framing | new, fix round RM-1: Listings 2 and 4 of draft1's §3 moved here as Listings 4 and 5 (RM's proposal) |
| 34 | In Listing 4 the reveal draw of Definition 6 is made whatever $\kappa_B$ is, with $\kappa_B$ read per episode from the state. | che/env/observation.py:300-310; che/env/observation.py:290-294 | edited (v2 06:27; draft1's Listing 2 label), fix round RM-1: moved with the listing |
| 35 | Listing 5 runs the environment at $\kappa_B = 0$ with and without masking, under the same keys, and asserts bitwise-identical fire, smoke, structure, food, positions, alive flags and rewards. | che/tests/test_coupling_b.py:131-142 | kept (v2 03:207), fix round RM-1: moved with the listing |
| 36 | Listing 4. Coupling B in the observation kernel: the reveal draw is made whatever $\kappa_B$ is. | che/env/observation.py:300-310 | fix round RM-1: draft1's Listing 2, renumbered; label and body unchanged (build: 6/6 byte-identical) |
| 37 | Listing 5. With $\kappa_B = 0$, trajectories and rewards are bitwise those of the environment before masking. | che/tests/test_coupling_b.py:131-142 | fix round RM-1: draft1's Listing 4, renumbered; label and body unchanged (build: 6/6 byte-identical) |
| 38 | Proposition 2 (Bond percolation). Under Definition 3 with $\iota = 0$ and a single ignition at the origin, the set of eventually-Burnt cells is equal in distribution to the open cluster of the origin in i.i.d. bond percolation on $(G, E)$ with edge-open probability $\beta$, where $E$ is the arena's set of von Neumann edges. | docs/theory_foundations.md:189-192; che/env/hazard.py:23-24 | edited: v2 03:130's statement moved here with v2 03:132's "Here E is the arena's set of von Neumann edges" folded in (stub ORDER) |
| 39 | Proof (coupling). | framing | kept (v2 12:28) |
| 40 | Attach to each unordered edge $e = \{g, g'\}$ an independent $B_e \sim \mathrm{Bernoulli}(\beta)$, and declare that a transmission attempt across $e$ succeeds if and only if $B_e = 1$. | docs/theory_foundations.md:195-197 | kept (v2 12:28) |
| 41 | Each edge is attempted at most once: when one cell of $e$ first Burns while the other is Fuel, one attempt occurs; afterwards the burning endpoint is Burnt, which is absorbing. | docs/theory_foundations.md:197-200 | kept (v2 12:28) |
| 42 | If the other endpoint later Burns via a different path, its neighbour across $e$ is already Burnt, so no second attempt occurs. | docs/theory_foundations.md:200-201 | kept (v2 12:28) |
| 43 | Run with the variables $\{B_e\}$, the fire therefore burns exactly the connected component of the origin in the subgraph of open edges $\{e: B_e = 1\}$, which is the bond-percolation cluster. | docs/theory_foundations.md:201-205 | kept (v2 12:28) |
| 44 | $\blacksquare$ | framing | kept |
| 45 | This is the correspondence between an epidemic with a constant infectious period and bond percolation described by Grassberger (1983). | grassberger1983; paper/related_work_verification.md:308-326; docs/theory_foundations.md:194-208 | edited (v2 03:132 and 12:30): v2's citation sentence moves here (§3 now cites in one clause); "the coupling behind the correspondence that §3.2 cites" reworded |
| 46 | The implementation realizes it exactly: it draws one uniform per cell and incoming direction (che/env/hazard.py:8-16), and with a one-step burn time each unordered edge sees at most one attempt, so these uniforms are the coupling's per-edge variables. | che/env/hazard.py:8-16 | edited (v2 12:30): v2's three sentences in one (Appendix A's budget) |
| 47 | Coupling A, when on, adds ignitions and breaks the hypotheses. | che/env/env.py:298-358; DX-1 | edited (v2 03:132 "Its hypotheses hold for CHE's fire when Coupling A is off, since collapses otherwise add ignitions"): moved here and reworded |
| 48 | Corollary 1 (Phase structure). On $\mathbb{Z}^2$ with the von Neumann neighbourhood, the fire of Definition 3 with $\iota = 0$ and a single ignition at the origin inherits the phase structure of bond percolation (Proposition 2, whose coupling holds on any graph): | docs/theory_foundations.md:210-212; docs/theory_foundations.md:194-203 | kept (v2 04:35); moved here from §4.1 (stub ORDER; §4.1 states it in words, W3) |
| 49 | Its critical point is $\beta_c = 1/2$ exactly, the critical probability of bond percolation on the square lattice (Kesten, 1980). | kesten1980; paper/related_work_verification.md:291-307 | kept (v2 04:37), at v2's verified level (identity: the title) |
| 50 | For $\beta > \beta_c$ the fire spreads indefinitely with positive probability. | garet2004chemical; paper/related_work_verification.md:1091-1110 | kept (v2 04:38); v2 D2 open (default: the Garet and Marchand level) |
| 51 | On that event the cells ignited by step $n$ are those within $n$ open edges of the origin. | garet2004chemical; paper/related_work_verification.md:1091-1110 | kept (v2 04:38) |
| 52 | Scaled by $1/n$, they converge almost surely in Hausdorff distance to a deterministic convex compact set with non-empty interior, invariant under permutations and reflections of the coordinates (Garet & Marchand, 2004; their Corollary 5.4). | garet2004chemical; paper/related_work_verification.md:1091-1110 | kept (v2 04:38) |
| 53 | The growth is therefore linear in $n$, at a speed given in each direction by the extent of that set. | garet2004chemical; paper/related_work_verification.md:1091-1110 | kept (v2 04:38) |
| 54 | Both items concern the idealized kernel (von Neumann neighbourhood, constant burn time, homogeneous fuel, no wind) on the infinite lattice; CHE's arena is finite, so §4.1 places the levels against a measured threshold. | docs/theory_foundations.md:227-228 | edited (v2 04:40): second sentence shortened ("CHE's fire is that kernel on a finite arena, with ignitions added by Coupling A, so the levels are placed against a measured finite-size threshold and, at High, a measured front speed (§4.3)" → "CHE's arena is finite, so §4.1 places the levels against a measured threshold") |
| 55 | The theory document's corollary also lists the subcritical regime and the critical exponents near $\beta_c$; the paper uses neither, so they are omitted, and its fourth item is numbered 2 here. | docs/theory_foundations.md:212-226 | new, fix round RM-3: TF's Cor. 1 items 2 (subcritical) and 3 (critical exponents) are omitted and item 4 is numbered 2; said once |
| 56 | Proposition 3 (Collapse events dominate hazard exposure). Work in the subcritical regime $\beta < \beta_c$ with $\iota = 0$, and suppose collapse events arrive at rate $\lambda_A$ per step, each seeding one ignition at a uniformly located Fuel cell, with seeded clusters pairwise disjoint (the sparse regime, $\lambda_A T \chi(\beta) \ll \lvert G \rvert$, the number of cells). | docs/theory_foundations.md:298-305 | kept (v2 05:46); moved here from §5.2 (stub ORDER); no 43/18 rate, no divergence claim |
| 57 | Then the expected burnt area $B_T$ by time $T$ satisfies | docs/theory_foundations.md:305-308 | kept (v2 05:46) |
| 58 | where $\chi(\beta)$ is the mean percolation cluster size. | docs/theory_foundations.md:308-309 | kept (v2 05:53) |
| 59 | Consequently the marginal hazard exposure per unit of structural instability is $\partial\,\mathbb{E}[B_T]/\partial\lambda_A = T\chi(\beta)$. | docs/theory_foundations.md:309-311 | kept (v2 05:53); v2 D3 and RM-10 (the derivative stated as an equality) still open, marked in a comment |
| 60 | Proof. | framing | kept (v2 12:36) |
| 61 | Each collapse seed grows, by Proposition 2, a burnt cluster equal in distribution to a bond-percolation cluster, of expected size $\chi(\beta)$. | docs/theory_foundations.md:313-315 | kept (v2 12:37) |
| 62 | By linearity of expectation over the Binomial or Poisson number of seeds, the total expected burnt area is $\lambda_A T \chi(\beta)$ when clusters are disjoint; overlaps only remove double counting, which gives the upper bound in general. | docs/theory_foundations.md:315-318 | kept (v2 12:38) |
| 63 | $\blacksquare$ | framing | kept |
| 64 | The theory document adds a divergence rate near the critical point, which rests on critical exponents the paper does not state. | docs/theory_foundations.md:309-311; docs/theory_foundations.md:318; docs/theory_foundations.md:217-225 | edited (v2 12:40): "The formal specification" → "The theory document" (V3Q16); "(§4.1)" cut (§4.1 states no exponent either) |
| 65 | In a finite protocol the equality is approached only when four conditions are matched, each with a known sign. | docs/theory_foundations.md:326-339 | edited (v2 12:41 "The equality is approached only when four conditions are matched, each with a known sign."): "In a finite protocol" added from v2 05:55 |
| 66 | They are an unconditional cluster-mass reference (a spanning-conditioned one underestimates it), seed location (boundary clipping lowers the mass of uniformly placed seeds), seed age (seeds born late have not reached full mass, which lowers the measured slope; at β = 0.43 mass saturates by an age of about 64 steps), and sparsity (sibling seeds and cluster overlap deflate the measured slope). | docs/theory_foundations.md:326-339; che/bench/results/phase3/phase3_report.md:106-109; CAL-3; DX-409 | kept (v2 12:42) |
| 67 | Two runs check the proposition, neither at the locked parameters, both without agents or primary ignition at the subcritical Low level ($\beta = 0.43$, $\iota = 0$), so collapse is the fire's only birth channel. | DX-304; CA-2; CA-3; che/bench/results/phase3/phase3_report.md:20-22 | edited (v2 05:55 "We tested the proposition in two runs, …"): moved here (§3.2 gives one clause); "so collapse is the fire's only birth channel" from v2 05:54, scoped to these runs (v2 P3-N6) |
| 68 | The first, a dense sweep on a 64 × 64 grid ($\kappa_A = 0.02$, $f_{\mathrm{weak}} = 0.4$), fits burnt area against realized seeds through the origin: $R^2 = 0.998$ over a 14× range of the expected seed count. | CA-2; che/bench/results/phase3/phase3_report.md:110-118 | kept (v2 05:55) |
| 69 | The second, a slower test in the suite on a 32 × 32 grid ($\kappa_A = 0.003$), divides its slope by a protocol-matched reference computed inside the test: 0.992, inside the band [0.90, 1.02], with $R^2 = 0.9995$. | CA-3; che/bench/results/phase3/phase3_report.md:126-150 | kept (v2 05:55) |
| 70 | In both, the four factors compose to the observed slope within Monte Carlo error. | docs/theory_foundations.md:335-339 | edited (v2 12:43 "In the Proposition 3 measurements (§5.2) the four factors compose to the observed slope within Monte Carlo error.") |
| 71 | Theorem 1 (Memorization gap, and its erosion by Coupling B). Consider the corridor toy at attenuation strength $\kappa_B$: from a start cell, a path of $d$ steps leads to a branch $b$, from which two disjoint corridors $L$ and $R$ of length $\ell$ lead to the goal; the horizon is $T = d + \ell$ (zero slack: a wrong commitment cannot be undone). | docs/theory_foundations.md:377-381; che/env/e2c.py:1-10 | edited (v2 06:29; OWNER-PENDING V3Q5): $E_{2C}(\kappa_B)$ → "the corridor toy at attenuation strength κ_B" (stub NOT HERE: toy codes) |
| 72 | At $t = 0$ nature draws $Z \in \{L, R\}$ uniformly; corridor $Z$ burns at depth $\ell_f \ge 1$ beyond $b$, and an agent entering it is disabled. | docs/theory_foundations.md:381-383; che/env/e2c.py:45-51 | kept (v2 06:29) |
| 73 | The reward is 1 for reaching the goal by $T$, else 0. | docs/theory_foundations.md:383-384 | kept (v2 06:29) |
| 74 | At each step $t = 0, \dots, d$ the agent receives the signal $Y_t = Z$ with probability $\tau_t(\kappa_B) = e^{-\kappa_B D_t}$, else $Y_t = \varnothing$, where the optical depth $D_t > 0$ of its line of sight to the fire, per unit $\kappa_B$, does not depend on $\kappa_B$. | che/env/e2c.py:161-213; che/env/e2c.py:273-294; che/env/observation.py:86-142; X2-2 | edited (V3-E2; V3Q5 default): v2 06:29 / TF:384-387 "with probability e^{−κ_B (d − t + ℓ_f)} (Beer–Lambert over the current distance to the fire, unit smoke density)" → "with probability τ_t(κ_B) = e^{−κ_B D_t} … where the optical depth D_t > 0 … does not depend on κ_B". The implemented toy reveals the fire with τ_t = exp(−κ_B · dist_t · ρ̄_t) from the shared transmittance (e2c.py:273-294; observation.py:86-142), and its D_t are κ_B-independent (X2-2: identical at all seven κ_B > 0). W2 confirmed P3 §3.3 this session (Findings) |
| 75 | Signals are independent across time and remembered. | docs/theory_foundations.md:387-388; che/env/e2c.py:203-206 | edited (v2 06:29): split; the toy draws each step's reveal from its own key (e2c.py:203-206) |
| 76 | Let | framing | kept (v2 06:29) |
| 77 | be the probability of being informed by the commitment point. | docs/theory_foundations.md:390-391; che/env/e2c.py:354 | edited: the display now reads $q = 1 - \prod_{t=0}^{d}(1 - e^{-\kappa_B D_t})$, which is the toy's own "q_analytic" (e2c.py:354, `1 - prod(1 - taus)`); v2's closed form over j = ℓ_f … d + ℓ_f is the special case D_t = d − t + ℓ_f (V3Q5 default) |
| 78 | Then (1) the optimal value is $J^(\kappa_B) = \tfrac12 + \tfrac12 q(\kappa_B)$; (2) the policies optimal for the fixed-map variant ($Z \equiv z_0$ constant) include the signal-blind policy "always take the corridor other than $z_0$", whose value on the toy is $\tfrac12$ for every $\kappa_B$, so the memorization gap is $J^(\kappa_B) - J^{\mathrm{static}} = \tfrac12 q(\kappa_B) > 0$ for all finite $\kappa_B$; and (3) $q$ is continuous and strictly decreasing in $\kappa_B$, with $q(0^+) \to 1$ and $q(\kappa_B) \to 0$ as $\kappa_B \to \infty$, so under total perceptual denial the optimal adaptive policy is no better than the memorizing one. | docs/theory_foundations.md:392-402 | kept (v2 06:33); "on $E_{2C}$" → "on the toy" |
| 79 | Proof. | framing | kept (v2 12:45) |
| 80 | (1) With zero slack, the only decision is the corridor choice at $b$; waiting or probing is impossible within $T$. | docs/theory_foundations.md:405-406 | kept (v2 12:46) |
| 81 | If informed (probability $q$), taking the corridor other than $Z$ succeeds with probability 1; if not, both corridors are exchangeable given the history, and any choice succeeds with probability $\tfrac12$. | docs/theory_foundations.md:407-409 | kept (v2 12:47) |
| 82 | Hence $J^ = q + (1-q)\tfrac12 = \tfrac12 + \tfrac{q}{2}$, and no policy exceeds this, since success requires information or a lucky guess. | docs/theory_foundations.md:409-411 | kept (v2 12:48) |
| 83 | (2) In the fixed-map environment the signal is uninformative, so the signal-blind policy is among the optimal ones there; on the toy it succeeds if and only if $Z = z_0$, with probability $\tfrac12$. | docs/theory_foundations.md:412-414 | kept (v2 12:49; "on $E_{2C}$" → "on the toy") |
| 84 | (3) Because every $D_t > 0$, each factor $(1 - e^{-\kappa_B D_t})$ is continuous and strictly increasing in $\kappa_B$ on $(0, \infty)$, so the finite product is too, and $q$ is continuous and strictly decreasing. | docs/theory_foundations.md:415-417 | edited (v2 12:50; V3Q5 default): the factor is $(1 - e^{-\kappa_B D_t})$, and "Because every D_t > 0" states the one hypothesis part (3) needs |
| 85 | The product tends to 0 as $\kappa_B \to 0$ and to 1 as $\kappa_B \to \infty$. | docs/theory_foundations.md:417-419 | kept (v2 12:51) |
| 86 | $\blacksquare$ | framing | kept |
| 87 | The proof uses only that the signals are independent and remembered, that $q$ is the probability of being informed, and, in part (3), that $D_t > 0$. | docs/theory_foundations.md:404-419; paper/v3/plans/P3.md:418-420 | new (V3-E2; P3 §3.3 "the proof needs no change; it uses only independent, remembered per-step signals and q"; confirmed by W2 against the proof's text) |
| 88 | The theory document states the theorem for unit smoke density over the integer distance to the fire, the special case $D_t = d - t + \ell_f$; this statement departs from it because the implemented toy (che/env/e2c.py) is not that case. | docs/theory_foundations.md:384-391; che/env/e2c.py:1-63 | new (V3-E2; stub ORDER: "say that this statement departs from the theory record's unit-density form", v2 C2 default; V3Q23) |
| 89 | The toy runs the production smoke update and observation kernel (Definitions 3 and 6) on a fire cell held Burning, at $d = 2$ and $\ell_f = 2$. | X2-5; che/env/e2c.py:12-19; che/env/e2c.py:45-58; che/env/e2c.py:79-100; che/bench/results/phase4/phase4_report.md:27-40 | new (V3-E2) |
| 90 | Its $D_t$ is therefore the Euclidean distance to the fire times the quadrature mean of a single smoke cell that grows each step. | che/env/observation.py:94-142; che/env/e2c.py:115-123; che/bench/results/phase4/phase4_report.md:37-40; X2-2 | new (V3-E2): one of the four nearest-cell quadrature points lands on the single smoky cell at each step (X2-2's cross-check) |
| 91 | Its depths are $D_0, D_1, D_2$ = 0.707, 0.898, 0.987, where the integer-distance form has 4, 3 and 2; at $\kappa_B = 1$ its $q$ is 0.8115, where that form gives 0.193. | X2-2; X2-4; X2-3 | new (V3-E2): rows X2-2 (DERIVED from e2c_sweep.json), X2-4 (DERIVED: the integer-distance form at the toy's geometry), X2-3 (VERIFIED, e2c_sweep.json:80) |
| 92 | Part (3) fails when some $D_t = 0$. | che/bench/results/phase4/phase4_report.md:140-145 | new (stub ORDER: "part (3) needs every D_t > 0 (the code documents the failure when not …)") |
| 93 | A larger geometry tried first ($d = 6$, a 17 × 17 crop) had $\tau = 1$ exactly at the first two steps, because the four-point quadrature never sampled the single smoke cell at that range, so $q \equiv 1$ for every $\kappa_B$. | X2-6; X2-7; che/env/e2c.py:22-34; che/tests/test_coupling_b.py:79-100 | new (stub ORDER; row X2-6) |
| 94 | The toy also leaks $Z$ through the visibility plane: smoke sits only on the fire's side, so the mirror corridor's cell is always revealed, and the pattern of reveals alone identifies $Z$. | che/bench/results/phase4/phase4_report.md:170-179; che/env/e2c.py:36-43 | new (P3 §3.3 item 5; stub ORDER: the content-channel sentence) |
| 95 | $J^$ is therefore the value of the content channel (the burning and smoke planes), the only input the scored policies read, which a test enforces. | che/bench/results/phase4/phase4_report.md:181-186; che/tests/test_e2c.py:201-221; che/env/e2c.py:146-152 | new (P3 §3.3 item 5; phase4_report.md:181-184: "Thm. 1's J* is the value of the content channel only") |
| 96 | The construction is kin to the irreversible commitment in Proposition 1 of Chen et al. (2022). | chen2022understandingdr; paper/related_work_verification.md:977 | new (stub CITATIONS: "Thm. 1 kin to their Prop. 1 construction, as RWV records"; v2 02:47 carries the fuller comparison) |
| 97 | The measured value of the policy the proof shows optimal (if informed, take the corridor other than $Z$; else a fixed one) matches $\tfrac12 + \tfrac12 q$, with $q$ computed from the toy's own transmittances on an independent random stream, under a three-condition check over the sweep of $\kappa_B$: largest $\lvert z \rvert$ 2.11, $\sum z^2 = 6.55$ on 8 degrees of freedom ($p = 0.586$), and mean $z$ −0.44. | CB-4; che/bench/results/phase4/phase4_report.md:46-55; che/env/e2c.py:237-264; che/env/e2c.py:297-315 | edited (v2 06:35): moved here from §6.2; v2's "The theorem also tests the code" cut (BLIND #51, category error); "q computed from the toy's own transmittances on an independent random stream" states what the check compares with (V3-E2); fix round RC1-20: what was measured is the value of the hand-coded policy the proof shows optimal (phase4_report.md:52-55; e2c.py:240-241), not an optimum found by search |
| 98 | At $\kappa_B = 8$ it is 0.5000 ± 0.0055 against 0.5028 predicted ($z$ −0.51). | X2-1 | new: replaces v2 06:35's "J* − ½ = 0.0000 at κ_B = 8, where q = 0.0056" (DX-14), which the blind review read as a contradiction (BRIEF §9.2 trap 1); measured ± SE against predicted, row X2-1 (phase4_report.md:72) |
| 99 | The memorizing policy stays at ½ (largest deviation 0.0084), and $J^(0) = 1.0000$. | DX-14 | edited (v2 06:35): "(largest deviation 0.0084)" added from DX-14's row |
| 100 | Remark 2′ (Value of communication). Extend the corridor toy of Theorem 1 with a second agent; §4.4 refers to this remark. (i) Under a team-any reward, communication has zero marginal value when the agents are interchangeable, expendable (no death cost) and at least as numerous as the hypotheses: coverage then achieves $J = 1$ under total denial. | docs/theory_foundations.md:486-494; ENV-1 | kept (v2 07:27; OWNER-PENDING V3Q4): moved here (stub ORDER: "Remark 2′ statement as v2 had it"); "Extend $E_{2C}$" → "Extend the corridor toy"; the Pynadath and Tambe framing sentence is §4.4's (W3); fix round RM-5: the parenthesis holds the remark's name, and "§4.4 refers to this remark" moves into the first sentence; "of Theorem 1" added (RC1-19's ℓ_f clash stays V3Q4's) |
| 101 | When any qualifier fails, value returns; in general it scales with the deficit of agents relative to hypotheses, and a death cost, such as CHE's $d_p = 0.5$, prices the redundancy that substitution spends. (ii) In the courier variant, where only agent 1 can complete the task and it observes the other agent only through messages, the denied optimum within the no-idle policy class is $\tfrac12 + \tfrac12 q(\kappa_B)$; with slack $\ell_f$, optimal denied play buys information by idling at the branch and achieves $\tfrac12 + \tfrac12 \tilde q(\kappa_B)$, where $\tilde q$ is the probability of being informed by the commitment point under the best idling schedule, with $\tilde q \ge q$ (equality iff $\ell_f = 0$), so | docs/theory_foundations.md:494-506; ENV-1 | kept (v2 07:27); the ℓ_f clash with Thm. 1 (P3-20) is V3Q4's, not changed |
| 102 | Both $q$ and $\tilde q$ decrease in $\kappa_B$, so the value of communication increases with perception decay. | docs/theory_foundations.md:506-507 | kept (v2 07:31) |
| 103 | The commitment draws have different optical depths, so as $\kappa_B \to \infty$ the lowest-depth draw dominates both products and $\tilde q / q \to 1$. | docs/theory_foundations.md:509-514 | kept (v2 12:63); v2's "One step is not spelled out in §7. Let q̃ be …" cut (q̃ is now defined in the statement just above) |
| 104 | The correction peaks at moderate $\kappa_B$, and its relative bite on the value of communication is largest at low $\kappa_B$, where $q$ is near 1. | docs/theory_foundations.md:514-518 | kept (v2 12:64) |
| 105 | In the courier variant with scripted policies, run through the production link kernel and the shared transmittance function, free communication scores 1.0000 at every $\kappa_B$. | DX-15; che/bench/results/phase5/phase5_report.md:509-536 | edited (v2 07:32 and 12:67): "We ran the courier variant …, which tests both kernels" and "the arm with free communication scores 1.0000" merged ("which tests both kernels" cut) |
| 106 | The no-idle denied arm matches $\tfrac12 + \tfrac12 q$ (largest absolute z 0.44; χ² 0.51 on 8 degrees of freedom), so $\mathrm{VoC}_{\mathrm{gated}} = \tfrac12(1 - q)$ rises monotonically from 0 to 0.498. | DX-15; COM-1; che/bench/results/phase5/phase5_report.md:540-558 | edited (v2 07:32 and 12:67): merged |
| 107 | In this two-agent toy, which is not CHE (4096 episodes and 8192 Monte Carlo draws per point), $\tilde q / q$ is 1.126 at $\kappa_B = 1.0$ and peaks at 1.235 near $\kappa_B = 2$. | DX-15 | kept (v2 12:65) |
| 108 | The correction removes 79 %, 54 % and 7 % of $\mathrm{VoC}_{\mathrm{gated}}$ at $\kappa_B$ = 0.5, 1.0 and 3.0. | DX-15 | kept (v2 12:66) |
| 109 | A transfer bound for a fixed policy (remark). | framing | new name (V3-S6: "Prop. 4 becomes a remark in the appendix, in words"; OWNER-PENDING V3Q3); unnumbered, so that no "Proposition 4" or new remark number appears |
| 110 | For a fixed policy and two configurations that share the reward, the difference between the policy's discounted returns is bounded above by a term that grows with how far their transition and observation kernels differ. | docs/theory_foundations.md:610-617 | edited (v2 09:34, statement in words): moved here; "bounded above by a term that grows with how far their transition and observation kernels differ" kept |
| 111 | It follows by telescoping the two models' evaluation operators along the trajectory distribution. | docs/theory_foundations.md:627-630 | edited (v2 12:55): shortened; "the observation term enters because the policy acts through the observation" cut (budget) |
| 112 | Every configuration the isolated arm trains on (§6.2) differs from the test configuration $\theta^$ on the states where both couplings act at once, such as a collapse increment next to Fuel with an agent within attenuation range. | docs/theory_foundations.md:619-622; docs/theory_foundations.md:630-632 | edited (v2 09:34, 12:56-57): "$\Theta_{\mathrm{iso}}$" → "every configuration the isolated arm trains on (§6.2)"; the state given as v2 12:57's example |
| 113 | There $\theta^$ places mass of order $\kappa_A$ on ignition transitions that a configuration with $\kappa_A = 0$ places elsewhere, and the observation kernels differ wherever $\kappa_B$ differs. | docs/theory_foundations.md:632-634 | kept (v2 12:58) |
| 114 | The remark bounds what isolated training can be guaranteed to transfer, not what happens. | docs/theory_foundations.md:636-638 | edited (v2 09:36): the honesty note, which "must appear in the paper" (TF:636), stated in substance |
| 115 | An upper bound on the isolated arm's transfer does not lower-bound the realized gap; compositional generalization can emerge from isolated training, and the experiment decides. | docs/theory_foundations.md:637-643 | edited (v2 09:36): "It does not lower-bound Γ" → "does not lower-bound the realized gap" (Γ is defined in §6.2; the appendix reads standalone) |
| 116 | The theory document displays the bound with a constant and concludes more about the isolated arm's slack than an upper bound can show; this remark draws no such conclusion. | docs/theory_foundations.md:610-625; paper_v2_prompt.md:146-150 | edited (v2 12:59): "The formal specification" → "The theory document" (V3Q16); "and draws no such conclusion (§9.1)" → "this remark draws no such conclusion"; no "irreducible" (terms list) |
| 117 | Its prediction about exposure to that region was not tested, since the counter of §3.5 cannot measure it. | docs/theory_foundations.md:645-654; CO-4 | edited (v2 09:36): the counter's limit by pointer to its home §3.5 (caveat C28), not restated |

## Findings

- **[V3-E2, record] Theorem 1's stated signal model does not match the
  implemented toy. Confirmed by W2 this session, read-only, at the sources.**
  - `TF:384-391` (= v2 §6.2): the signal arrives with probability
    e^{−κ_B (d − t + ℓ_f)}, "unit smoke density" over the integer distance,
    and q = 1 − ∏_{j=ℓ_f}^{d+ℓ_f}(1 − e^{−κ_B j}).
  - `che/env/e2c.py:12-19, :45-58, :161-213, :273-294`: the toy's only
    information channel is the production observation path; the fire cell is
    revealed with τ_t = exp(−κ_B · ‖y − x_t‖₂ · ρ̄_t) from the shared
    `transmittance` (`che/env/observation.py:86-142`), with ρ̄_t the mean of a
    single, growing smoke cell (1.000, 1.607, 1.974; `phase4_report.md:40`) at
    four nearest-cell quadrature points, one of which lands on the smoky cell.
  - Optical depths: D_t = −ln τ_t / κ_B = 0.7071, 0.8981, 0.9872 from the
    committed `tau_profile` (`e2c_sweep.json:89-93`), identical at all seven
    κ_B > 0 (row X2-2), and equal to √8·1.000/4, √5·1.6065/4, 2·1.9744/4. The
    stated form has 4, 3, 2.
  - At κ_B = 1 the toy's q is 0.8115 (`e2c_sweep.json:80`, X2-3); the stated
    closed form gives 0.1934 (X2-4). At κ_B = 8: 0.0046 against about 1e-7
    (builder arithmetic, not used in the text).
  - The code agrees with its own test: `predict_q` and `q_analytic` build q
    from the measured τ (`e2c.py:297-315, :354`), never from the closed form.
  - The proof needs no change: (1) and (2) use only independent, remembered
    signals and q; (3) uses only that every exponent is positive.
  - P3's finding (P3 §3.3, items 1–5) is **confirmed** in every particular,
    including item 4: the blind review's "J* − ½ = 0.0000 contradicts the
    theorem" is wrong (`phase4_report.md:72`: 0.5000 ± 0.0055 measured,
    0.5028 predicted, z −0.51; row X2-1), and item 5: J* is the content
    channel's value only (`phase4_report.md:170-186`;
    `che/tests/test_e2c.py:201`).
  - Direction: the default text states Thm. 1 for per-step optical depths
    D_t > 0 (OWNER-PENDING V3Q5) and says it departs from TF; the alternate
    keeps TF's statement and states the mismatch. TF is not edited (record
    item R-1, DISPOSITIONS §6).
- **[record, V3Q16] Two records disagree on whether the theory document
  ships.** The stub (and DISPOSITIONS V3Q16's default) assume it is not
  shipped and ask for self-contained statements; the step-2 supplement ships
  `docs/theory_foundations.md` by default (`paper/v3/supplement/README.md:54`,
  rule D3, "on by default"). The text names it as a file in the code
  supplement and is marked OWNER-PENDING V3Q16; if the owner removes it from
  the supplement, the four departure sentences (Prop. 1, Prop. 3, Thm. 1, the
  transfer remark) need a different referent or must go.
- **[style] "Remark 2′" keeps its name** although Remark 1 is cut and no
  Remark 2 exists (V3Q4 covers Remark 2′'s fate; the name is §4.4's too).
  The transfer remark is unnumbered on purpose.
- **[record, v2 D3 / RM-10] Proposition 3's derivative** is stated as an
  equality, and "(1 + o(1))" names no limit; kept at v2's verified level,
  flagged in a comment.
- **[record, v2 RM-9] Definition 1's state** omits the weak-terrain mask and
  the emitted messages, which Prop. 1's proof inherits (v2 D4, carried).

## Alternates

- `sections/alt/13_appendix_proofs.thm1_tf.md` (V3Q5): Theorem 1 as the
  theory document states it (unit density, integer distance), followed by
  the mismatch stated plainly with the same rows; everything else identical.
- `sections/alt/13_appendix_proofs.no_prop4.md` (V3Q3): without the transfer
  remark and its honesty note; everything else identical. With it, §7's "no
  theorem that joint training wins" stands alone (W5), and TF:636's "must
  appear in the paper" becomes moot (record item R-6).
- Recommendation: the default (general D_t), because it is the statement
  the code satisfies; for V3Q3 no recommendation (both are faithful).
