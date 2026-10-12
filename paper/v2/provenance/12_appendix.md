# Provenance: sections/12_appendix.md

Writer: W6. Checked against the section on 2026-10-11 (step 4, pass 1) and on 2026-10-12 after the pass-3 fixes and the step-4.3 re-check items.
`TF` = `docs/theory_foundations.md`. "Demo" is
`paper/demo_beyond/sections/12_appendix.md`. The sentence column is the
checker's normalized form (it drops `*`, so "θ^*" reads "θ^").

Word counts (P3's method): the index 49 prose words, Appendix A 916
(target for this file about 800: index about 80, proofs about 720); 965 in
all after the re-check items, 21 % over (the four corrections' signs, RC2-5, added
about 30 words, and the seed-age direction at the re-check 12 more; the plain names for the toy's arms, RC2-24, about 15). The proofs are kept whole; the overrun is the Proposition 3
finite-protocol details moved here from §5.2 (W4) and the Remark 2′
constants moved here from §7 (W4), as their stubs direct.

| # | sentence (verbatim) | support | change from the demo, and why |
|---|---|---|---|
| 1 | Appendices | framing | kept |
| 2 | Appendix A: proofs. | framing | new; class A, P2-h (the appendix index replaces §11's list; STRUCTURE §2 letters) |
| 3 | Appendix B: locks and hyperparameters. | framing | new (index line; App. B is W5's) |
| 4 | Appendix C: reproducibility floors. | framing | new (index line; App. C is W5's) |
| 5 | Appendix D: the frozen analysis plan, quoted. | framing | new (index line) |
| 6 | Appendix E: the registered outcome branches. | framing | new (index line) |
| 7 | Appendix F: grid provenance and blinding. | framing | new (index line) |
| 8 | Appendix G: Γ over the final half of training. | framing | new (index line; demo Appendix H re-lettered G, STRUCTURE §2) |
| 9 | Appendix H: the secondary design. | framing | new (index line; demo Appendix I re-lettered H) |
| 10 | Appendix I: trained-policy episodes. | framing | new (index line; demo Appendix J re-lettered I) |
| 11 | A Proofs | framing | kept |
| 12 | Each statement is in the body, in the section named. | framing | edited (demo 12:7); class A, LEN (claims review C-34: no restated statements) |
| 13 | The proofs follow the formal specification in the notation of Definition 1, and departures from it are noted. | docs/theory_foundations.md:142-154, :195-205, :313-318, :404-419, :627-634 | edited (demo 12:7): the definition of Θ dropped (LEN) |
| 14 | Proposition 1. Statement in §3.1. | framing | edited: the demo's name "(Well-posedness)" dropped, so the label cannot drift from §3.1's |
| 15 | Proof. | framing | kept |
| 16 | Each factor of $T_\theta$ is a conditional kernel, measurable in its conditioning variables, all of which are components of $(s, a)$ or of already-sampled components of $s'$. | docs/theory_foundations.md:142-145 | kept (demo 12:11) |
| 17 | The dependence of $T_H$ on $c'$ and of $T_K$ on $x'$ is a sequential composition within one time step. | docs/theory_foundations.md:145-149; CLAUDE.md:40-46 (invariant 2) | kept, split in two (sentence length); pass 3: the checker now splits it, so it has two rows |
| 18 | Sample $c' \sim T_C(\cdot \mid c, x)$, then $h' \sim T_H(\cdot \mid h, c, c')$, then $\rho' = T_\rho(\rho, h')$ (deterministic), then $x' \sim T_X(\cdot \mid x, a, h', c')$, then $k' \sim T_K(\cdot \mid x')$. | docs/theory_foundations.md:145-149 | kept (second half of the split sentence) |
| 19 | A composition of Markov kernels is a Markov kernel on the product space, so $T_\theta$ is a valid transition kernel on $\mathcal{S}$ and $(s_t)$ is Markov. | docs/theory_foundations.md:149-151 | kept |
| 20 | The action sets are finite, every stochastic factor and the reset distribution have finite support, and $\rho$ evolves deterministically from $\rho_0 = 0$. | docs/theory_foundations.md:151-153; che/env/env.py:239-245 | edited: class A, OI-2 (the reachable-set argument, as the demo's) |
| 21 | The states and observations reachable within the horizon therefore form finite sets; restricted to them, $\mathcal{M}_\theta$ is a finite Dec-POMDP, and optimal finite-horizon joint policies exist by the standard argument. | docs/theory_foundations.md:151-154 | edited; class A, OI-2: "finite Dec-POMDP" only on the reachable states |
| 22 | $\blacksquare$ | framing | kept |
| 23 | The formal specification states that $\mathcal{S}$ and $\Omega_i$ are finite. | docs/theory_foundations.md:151-153 | kept; class A, OI-2 (departure note, demo 12:13) |
| 24 | With the real-valued smoke field $\rho \in \mathbb{R}_{\ge 0}^G$ in the state, that holds only for the states and observations reachable within the horizon, which is all the argument uses. | docs/theory_foundations.md:151-153; che/env/types.py:11 | kept (demo 12:13) |
| 25 | Proposition 2. Statement in §3.2. | framing | edited: name dropped |
| 26 | Proof (coupling). | framing | kept |
| 27 | Attach to each unordered edge $e = \{g, g'\}$ an independent $B_e \sim \mathrm{Bernoulli}(\beta)$, and declare that a transmission attempt across $e$ succeeds if and only if $B_e = 1$. | docs/theory_foundations.md:195-197 | kept (demo 12:17) |
| 28 | Each edge is attempted at most once: when one cell of $e$ first Burns while the other is Fuel, one attempt occurs; afterwards the burning endpoint is Burnt, which is absorbing. | docs/theory_foundations.md:197-200 | kept |
| 29 | If the other endpoint later Burns via a different path, its neighbour across $e$ is already Burnt, so no second attempt occurs. | docs/theory_foundations.md:200-201 | kept |
| 30 | Run with the variables $\{B_e\}$, the fire therefore burns exactly the connected component of the origin in the subgraph of open edges $\{e: B_e = 1\}$, which is the bond-percolation cluster. | docs/theory_foundations.md:201-205 | kept |
| 31 | $\blacksquare$ | framing | kept |
| 32 | This is the coupling behind the correspondence that §3.2 cites, and the implementation realizes it exactly (che/env/hazard.py:8-16). | grassberger1983; paper/related_work_verification.md:283-299 (identity verified; BRIEF §15 permitted use); che/env/hazard.py:8-16 | edited (demo 12:19): §3.2 now carries the citation sentence, so this points to it |
| 33 | It draws one uniform per cell and incoming direction, which maps one-to-one to the ordered pairs of Definition 3. | che/env/hazard.py:8-12 | edited: shortened (LEN) |
| 34 | With a burn time of one step, each unordered edge sees at most one attempt, so these uniforms are the coupling's per-edge variables. | che/env/hazard.py:12-16 | kept, shortened |
| 35 | Proposition 3. Statement in §5.2. | framing | edited: name dropped (W4 drops the divergence clause from it) |
| 36 | Proof. | framing | kept |
| 37 | Each collapse seed grows, by Proposition 2, a burnt cluster equal in distribution to a bond-percolation cluster, of expected size $\chi(\beta)$. | docs/theory_foundations.md:313-315 | kept (demo 12:23) |
| 38 | By linearity of expectation over the Binomial or Poisson number of seeds, the total expected burnt area is $\lambda_A T \chi(\beta)$ when clusters are disjoint; overlaps only remove double counting, which gives the upper bound in general. | docs/theory_foundations.md:315-318 | edited; class A, C1: the demo's "The divergence rate is Corollary 1(3)." removed |
| 39 | $\blacksquare$ | framing | kept |
| 40 | The formal specification adds a divergence rate near the critical point, which rests on critical exponents the paper does not state (§4.1). | docs/theory_foundations.md:309-311, :318, :217-225 | new; class A, C1 and P3-N5: the departure from TF stated (Q4k default: the paper departs and says so in App. A); pass 3: RC2-4, RC1-39 and RM-12: "Corollary 1(3)" removed (the paper's Corollary 1 has no item 3); the rate is described as resting on critical exponents the paper does not state (§4.1) |
| 41 | The equality is approached only when four conditions are matched, each with a known sign. | docs/theory_foundations.md:326-339 | edited; pass 3, RC2-5: each condition now carries its known sign, as TF:328-339 states them, so §5.2's pointer "(Appendix A)" lands on the signs; re-check: RC2-5 (NOT OK): the seed-age condition now states its direction, as §5.2 does: seeds born late have not reached full mass, which lowers the measured slope (TF:333-334, "uniformly-born seeds are age-averaged"; che/bench/results/phase3/phase3_report.md:106-109, the age-averaging "costs" about 7 %); the sentence split after "a known sign" (length, 74 words) |
| 42 | They are an unconditional cluster-mass reference (a spanning-conditioned one underestimates it), seed location (boundary clipping lowers the mass of uniformly placed seeds), seed age (seeds born late have not reached full mass, which lowers the measured slope; at β = 0.43 mass saturates by an age of about 64 steps), and sparsity (sibling seeds and cluster overlap deflate the measured slope). | docs/theory_foundations.md:326-339; che/bench/results/phase3/phase3_report.md:106-109; CAL-3; DX-409 | edited; pass 3, RC2-5: each condition with its sign (TF:328-339); re-check, RC2-5 (NOT OK): seed age now states its direction, as §5.2 does (seeds born late have not reached full mass, which lowers the measured slope; TF:333-334; che/bench/results/phase3/phase3_report.md:106-109); split from the previous sentence (length) |
| 43 | In the Proposition 3 measurements (§5.2) the four factors compose to the observed slope within Monte Carlo error. | docs/theory_foundations.md:335-339 | edited (demo 12:25: "at both of M3.3's grid sizes"); class A, F5 (study code removed) |
| 44 | Theorem 1. Statement in §6.2; items (1)–(3) below refer to it. | framing | edited: name dropped |
| 45 | Proof. | framing | kept |
| 46 | (1) With zero slack, the only decision is the corridor choice at $b$; waiting or probing is impossible within $T$. | docs/theory_foundations.md:405-406 | edited: "and, vacuously, the path to b" cut (LEN) |
| 47 | If informed (probability $q$), taking the corridor other than $Z$ succeeds with probability 1; if not, both corridors are exchangeable given the history, and any choice succeeds with probability $\tfrac12$. | docs/theory_foundations.md:407-409 | kept |
| 48 | Hence $J^ = q + (1-q)\tfrac12 = \tfrac12 + \tfrac{q}{2}$, and no policy exceeds this, since success requires information or a lucky guess. | docs/theory_foundations.md:409-411 | kept |
| 49 | (2) In the fixed-map environment the signal is uninformative, so the signal-blind policy is among the optimal ones there; on $E_{2C}$ it succeeds if and only if $Z = z_0$, with probability $\tfrac12$. | docs/theory_foundations.md:412-414 | kept (the demo's "among the optimal ones"; P3-N11 is class C, Q23) |
| 50 | (3) Each factor $(1 - e^{-\kappa_B j})$ is continuous and strictly increasing in $\kappa_B$ on $(0, \infty)$, so the finite product is too, and $q$ is continuous and strictly decreasing. | docs/theory_foundations.md:415-417 | kept |
| 51 | The product tends to 0 as $\kappa_B \to 0$ and to 1 as $\kappa_B \to \infty$. | docs/theory_foundations.md:417-419 | edited: shortened |
| 52 | $\blacksquare$ | framing | kept |
| 53 | Proposition 4 (A transfer bound for a fixed policy). Statement in §9.1. | framing | edited; class A, C3 (pass 1); pass 3, orchestrator decision 2: the proposition's one name used here too |
| 54 | Proof idea. | framing | edited; class A, C3/P3-N7: "Proof" becomes "Proof idea" (no constant is derived here); no closing square |
| 55 | The difference between the two returns is bounded by telescoping the evaluation operators of the two models along the trajectory distribution; the observation term enters because the policy acts through the observation. | docs/theory_foundations.md:627-630 | edited: demo "The value-difference bound is the standard simulation lemma: telescope the Bellman evaluation operators …" (lemma not cited by name, P3-N7) |
| 56 | Every configuration in $\Theta_{\mathrm{iso}}$ differs from $\theta^$ where both couplings act at once. | docs/theory_foundations.md:619-622, :630-631 | edited (demo 12:33: "ε_min > 0 holds because …"); class A, C3: no ε_min constant |
| 57 | Take a state with a collapse increment next to Fuel and an agent within attenuation range. | docs/theory_foundations.md:631-632 | kept, split (sentence length) |
| 58 | There $T_{\theta^}$ places mass of order $\kappa_A$ on ignition transitions that a configuration with $\kappa_A = 0$ places elsewhere, and the observation kernels differ when $\kappa_B$ differs. | docs/theory_foundations.md:632-634 | kept |
| 59 | The formal specification displays the bound with an explicit constant and concludes more about ISO's slack than an upper bound can show; the paper states the bound in words and draws no such conclusion (§9.1). | docs/theory_foundations.md:610-625; paper_v2_prompt.md:146-150 (C3) | new; class A, C3 with N6 (record item, Q4i, Q4k): the departure from TF stated without the word "irreducible" (NOT HERE list). Replaces the demo's "As §9.1 states, the proposition bounds what ISO can be guaranteed to transfer, not what happens: it does not lower-bound the realized Γ." (pointer only, N16) |
| 60 | Remark 2′. Stated in §7.2, after Pynadath and Tambe. | pynadath2002; paper/related_work_verification.md:953 | kept (demo 12:37) |
| 61 | One step is not spelled out in §7. | framing | edited: split (sentence length) |
| 62 | Let $\tilde q$ be the probability of being informed under the best idling schedule. | docs/theory_foundations.md:497-501 | kept |
| 63 | The commitment draws have different optical depths, so as $\kappa_B \to \infty$ the lowest-depth draw dominates both products and $\tilde q / q \to 1$. | docs/theory_foundations.md:509-514 | kept |
| 64 | The correction peaks at moderate $\kappa_B$, and its relative bite on the value of communication is largest at low $\kappa_B$, where $q$ is near 1. | docs/theory_foundations.md:514-518 | edited: demo "the idling correction is not asymptotic, and its relative bite …" ("peaks at moderate κ_B" is TF's wording) |
| 65 | In the two-agent toy, which is not CHE (4096 episodes and 8192 Monte Carlo draws per point), $\tilde q / q$ is 1.126 at $\kappa_B = 1.0$ and peaks at 1.235 near $\kappa_B = 2$. | DX-15 | new: moved from §7 (W4 stub: the toy's constants go to Appendix A; LEN) |
| 66 | The correction removes 79 %, 54 % and 7 % of $\mathrm{VoC}_{\mathrm{gated}}$ at $\kappa_B$ = 0.5, 1.0 and 3.0. | DX-15 | new: moved from §7 |
| 67 | The check that the denied arm under the no-idle schedule matches $\tfrac12 + \tfrac12 q$ passes (largest absolute z 0.44; χ² 0.51 on 8 degrees of freedom), and the arm with free communication scores 1.0000 at every $\kappa_B$. | DX-15; che/bench/results/phase5/phase5_report.md:540-555 | new (pass 1, moved from §7); pass 3, RC2-24: "handshake gate", "pinned arm" and "free arm" replaced by what they are (the no-idle denied arm against ½ + q/2; the arm with free communication) |

## Findings

- [corr, record] Proposition 4 (TF:610-625): the displayed constant
  γR_max/(1−γ)², the max over agents' observation kernels, the title's
  "irreducible" and the "JOINT trains at ε = 0" contrast are the items N6
  and P3-N7 describe. Appendix A gives a proof idea without a constant,
  cites no lemma by name, and states the departure in one sentence. Class
  C, Q4i and Q4k (TF is not edited).
- [corr, record] Proposition 3 (TF:309-311, :318): the divergence rate rests
  on Corollary 1(3), which v2 drops (C1). Appendix A states the departure.
  Class A for the paper (C1); the TF record item is Q4k.
- [corr, record] Proposition 1 (TF:151-153): "S, Ω_i finite" holds only on
  the reachable states; the departure note is kept (OI-2). Class A; record
  item Q4k.
- [mech] The checker merges the Proposition 1 proof's sentences at
  "… one time step. Sample …" (its `ABBREV` entry `"p."`; see
  `provenance/09_compositional_test.md`, Findings). Class C, B2.

## Alternates

None.

## Open items

- **Proposition names.** Appendix A labels the propositions by number only
  ("Proposition 1. Statement in §3.1."), so the labels cannot drift from
  W3's and W4's chosen names. Proposition 4's name is W6's: "A transfer
  bound for a fixed policy" (§9.1).
- **Citation support (N15, class B).** `grassberger1983` is verified for
  identity only (`RWV:283-299`); its use here is the BRIEF §15 permitted
  use (the SIR–bond-percolation correspondence), now cited by §3.2 and
  pointed to from here. B2's abstract-level support quote for the theory
  keys is not yet in `RWV`.
- **Budget.** This file is 19 % over its 800-word share after pass 3.
- **Pass-3 owner items:** RM-9 (Def. 1 omits the weak-terrain mask and the
  emitted messages, so App. A's Proposition 1 proof inherits the gap), RM-10
  (Proposition 3's derivative stated as an equality, carried from TF),
  RM-11 and RC2-35 (App. A's departure notes cite "the formal
  specification", which no reader can see unless a supplement exists;
  Q4e, Q4k). None is applied.
