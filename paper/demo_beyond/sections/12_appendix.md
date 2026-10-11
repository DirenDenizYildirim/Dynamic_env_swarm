<!-- BUILDER-WRITTEN DEMONSTRATION (DEMONSTRATION DRAFT ruling, 2026-10-11); not the owner's text -->

## Appendices

### A Proofs

Each statement is in the body, where the section named below gives it; this appendix gives the proofs, typeset from the formal specification, with one departure noted under Proposition 1. The notation is that of Definition 1, with $\Theta$ the set of environment configurations $\theta = (\beta, \kappa_A, \kappa_B, \delta)$.

**Proposition 1 (Well-posedness).** Statement in §3.1.

**Proof.** Each factor of $T_\theta$ is a conditional kernel, measurable in its conditioning variables, all of which are components of $(s, a)$ or of already-sampled components of $s'$. The dependence of $T_H$ on $c'$ and of $T_K$ on $x'$ is a sequential composition within one time step: sample $c' \sim T_C(\cdot \mid c, x)$, then $h' \sim T_H(\cdot \mid h, c, c')$, then $\rho' = T_\rho(\rho, h')$ (deterministic), then $x' \sim T_X(\cdot \mid x, a, h', c')$, then $k' \sim T_K(\cdot \mid x')$. A composition of Markov kernels is a Markov kernel on the product space, so $T_\theta$ is a valid transition kernel on $\mathcal{S}$ and $(s_t)$ is Markov. The action sets are finite, every stochastic factor and the reset distribution have finite support, and $\rho$ evolves deterministically from $\rho_0 = 0$, so the states and observations reachable within the horizon form finite sets; restricted to them, $\mathcal{M}_\theta$ is a finite Dec-POMDP, so optimal finite-horizon joint policies exist by the standard argument. $\blacksquare$

This departs from the formal specification's wording, which states that $\mathcal{S}$ and $\Omega_i$ are finite: with the real-valued smoke field $\rho \in \mathbb{R}_{\ge 0}^G$ in the state, that holds only for the states and observations reachable within the horizon, which is all the argument uses.

**Proposition 2 (Bond percolation).** Statement in §3.2.

**Proof (coupling).** Attach to each unordered edge $e = \{g, g'\}$ an independent $B_e \sim \mathrm{Bernoulli}(\beta)$, and declare that a transmission attempt across $e$ succeeds iff $B_e = 1$. Each edge is attempted at most once: when one cell of $e$ first Burns while the other is Fuel, one attempt occurs; afterwards the burning endpoint is Burnt, which is absorbing, and if the other endpoint later Burns via a different path, its neighbour across $e$ is already Burnt, so no second attempt occurs. Hence the fire, run with the variables $\{B_e\}$, burns exactly the connected component of the origin in the subgraph of open edges $\{e : B_e = 1\}$, which is the bond-percolation cluster. $\blacksquare$

This is the mapping between SIR with a constant infectious period and bond percolation that Grassberger (1983)<d-cite key="grassberger1983"></d-cite> gives, here with a self-contained proof. The implementation realizes the coupling exactly (`che/env/hazard.py`, module docstring): Definition 3 asks for independent ignition attempts per ordered pair (Burning cell $g$, Fuel neighbour $g'$); the kernel samples one uniform per cell per incoming direction, and the ordered pair $(g \to g')$ maps bijectively to the slot ($g'$, direction of $g$ from $g'$), so per-ordered-pair independence is exact. With a burn time of exactly one step, each unordered edge sees at most one attempt over the whole trajectory, so these uniforms are also the per-edge Bernoulli variables of the coupling.

**Proposition 3 (Collapse events dominate hazard exposure; divergence near criticality).** Statement in §5.2.

**Proof.** Each collapse seed grows, by Proposition 2, a burnt cluster equal in distribution to a bond-percolation cluster, of expected size $\chi(\beta)$. By linearity of expectation over the Binomial or Poisson number of seeds, the total expected burnt area is $\lambda_A T \chi(\beta)$ when clusters are disjoint; overlaps only remove double counting, which gives the upper bound in general. The divergence rate is Corollary 1(3). $\blacksquare$

Two details of the finite-protocol remark (§5.2) that §5 does not repeat: under correction (iii), cluster mass at $\beta = 0.43$<!-- N:CAL-3 --> saturates by an age of $t_{\mathrm{sat}} \approx 64$ steps<!-- N:DX-409 -->; and at both of M3.3's grid sizes the four measured factors compose to the observed slope within Monte Carlo error, with a residual that does not depend on grid size.

**Theorem 1 (Memorization gap, and its erosion by Coupling B).** Statement in §6.2; items (1)–(3) below refer to it.

**Proof.** *(1)* With zero slack, the only decisions are the corridor choice at $b$ and, vacuously, the path to $b$; waiting or probing is impossible within $T$. If informed (probability $q$), taking the corridor other than $Z$ succeeds with probability 1; if uninformed, both corridors are exchangeable given the history, so any choice succeeds with probability $\tfrac12$. Hence $J^* = q + (1-q)\tfrac12 = \tfrac12 + \tfrac{q}{2}$, and no policy can exceed this, since success requires either information (probability $q$) or a lucky guess. *(2)* In the fixed-map environment the signal is uninformative (constant $Z$), so the signal-blind policy is among the optimal ones there; on $E_{2C}$ it succeeds iff $Z = z_0$, with probability $\tfrac12$. *(3)* Each factor $(1 - e^{-\kappa_B j})$ is continuous and strictly increasing in $\kappa_B$ on $(0, \infty)$, so the finite product is too, and $q$ is continuous and strictly decreasing. The limits are immediate: $e^{-\kappa_B j} \to 1$ pointwise as $\kappa_B \to 0$, so the product tends to 0, and it tends to 1 as $\kappa_B \to \infty$. $\blacksquare$

**Proposition 4 (An irreducible shift term for ISO).** Statement in §9.1, for the $\gamma$-discounted return; the simulation lemma is stated for the factored kernels, with constants not optimized.

**Proof.** The value-difference bound is the standard simulation lemma: telescope the Bellman evaluation operators of the two models along the trajectory distribution; the observation term enters because $\pi$ acts through $O$. $\varepsilon_{\min} > 0$ holds because on states $s$ with a collapse increment adjacent to Fuel and an agent within attenuation range, $T_{\theta^*}$ places mass of order $\kappa_A$ on ignition transitions that $T_\theta$ with $\kappa_A = 0$ places elsewhere, and similarly for the observation term when $\kappa_B$ differs. $\blacksquare$

As §9.1 states, the proposition bounds what ISO can be *guaranteed* to transfer, not what happens: it does not lower-bound the realized $\Gamma$.

**Remark 2′.** Stated in §7.2, after Pynadath & Tambe (2002)<d-cite key="pynadath2002"></d-cite>. One step §7 does not spell out: write $\tilde q$ for the probability of being informed under the best idling schedule. The draws of the commitment schedule have different optical depths, so as $\kappa_B \to \infty$ the lowest-depth draw dominates both products and $\tilde q / q \to 1$: the idling correction is not asymptotic, and its relative bite on the value of communication is largest at low $\kappa_B$, where $q$ is near 1.

### B Locks and hyperparameters

Every locked environment constant is reachable from a configuration and asserted against the configurations and code defaults by `che/tests/test_locks.py`; every analysis constant is asserted against the literal in the instrument that uses it.

| constant | value | ruled | record |
|---|---|---|---|
| critical point $\hat\beta_c$ | 0.500 ± 0.005<!-- N:CAL-1 --> | 2026-07-19<!-- N:DX-401 --> | severity lock record; its estimator ($R_L$ logistic centres) has no committed script, and the committed estimators give a crossing mean of 0.504 and a consensus of 0.499<!-- N:CAL-1 --> |
| β Low / Medium / High | 0.43 / 0.49 / 0.70<!-- N:CAL-3 --> | 2026-07-19<!-- N:DX-401 --> | severity lock record |
| β held out (θ\*) | 0.49<!-- N:CAL-3 --> | 2026-08-02<!-- N:DX-401 --> | Phase-6 design ruling; equal to β Medium, kept separate because the role differs |
| $f_{\mathrm{weak}}$, $\lambda_0$, $\lambda_{\mathrm{load}}$, $\kappa_A$, $r_A$ | 0.15, 5e-5, 4e-4, 0.06, 1<!-- N:CA-1 --> | 2026-07-21<!-- N:DX-401 --> | Coupling-A lock record |
| weak-floor smoothing passes | 2<!-- N:DX-401 --> | 2026-07-21<!-- N:DX-401 --> | Coupling-A lock record |
| $\kappa_B$ | 1.0<!-- N:CB-1 --> | 2026-07-27<!-- N:DX-401 --> | $\kappa_B$ lock record, on the detection band alone |
| δ off / on; $R_{\mathrm{comm}}$ | 0.0<!-- N:DX-401 --> / 1.0; 16<!-- N:COM-6 --> | 2026-07-30<!-- N:DX-401 --> | communication lock record |
| death penalty $d_p$ | 0.5<!-- N:ENV-1 --> | 2026-07-19<!-- N:DX-401 --> | the death-penalty design decision |
| observation version | v3<!-- N:DX-401 --> | 2026-07-24<!-- N:DX-401 --> | the observation design decision, frozen after the Coupling-B observation milestone |
| $\sigma_s$, η, ι | 1.0, 0.5, 0.0<!-- N:DX-1 --> | not locked | held fixed by convention, never calibrated |

| analysis constant | value | ruled | role |
|---|---|---|---|
| `K_CONFIRMATORY` | 40<!-- N:DES-1 --> | 2026-08-03<!-- N:DX-402 --> | design seed count per confirmatory arm; the re-floor ladder computes against it |
| `K_LADDER_CAP` | 60<!-- N:DES-1 --> | 2026-08-03<!-- N:DX-402 --> | the ladder's cap |
| `K_CONFIRMATORY_REALIZED` | 72<!-- N:DES-3 --> | 2026-09-22<!-- N:DX-402 --> | the k at which Γ is read; a recorded deviation |
| `K_SECONDARY` | 20<!-- N:DES-13 --> | 2026-08-02<!-- N:DX-402 --> | seeds per secondary arm; ISO-4 uses the same k |
| `SIDAK_M`; $z_\alpha$ | 2; 2.2365<!-- N:DES-13 --> | 2026-08-02<!-- N:DX-402 --> | the confirmatory family of two co-primaries |
| `POWER_STOP` | 0.80<!-- N:DX-402 --> | 2026-08-02<!-- N:DX-402 --> | minimum design-stage power at the 0.03<!-- N:DES-4 --> band |
| `T_STAR` | 1000<!-- N:DES-13 --> | 2026-08-11<!-- N:DX-402 --> | the fixed budget (provenance re-pointed; value unchanged since 2026-08-03<!-- N:DX-402 -->) |
| `GAMMA_T_RETENTION` | 11<!-- N:DES-13 --> | 2026-08-11<!-- N:DX-402 --> | checkpoints kept for Γ(t), updates 500–1000 every 50<!-- N:DES-13 --> |
| evaluation draw | seed 0 × 512 episodes<!-- N:DES-13 --> | with the grid layout | common to every run |
| `PLATEAU_PASS`; `PLATEAU_REVIEW` | 1.0; 1.5<!-- N:DX-402 --> | 2026-08-02<!-- N:DX-402 --> | the plateau criterion, retired as a certification instrument on 2026-08-11<!-- N:METH-6 -->; grades nothing |

Training hyperparameters, identical for every Phase-6 arm (the grid passes none on the command line, so the configured defaults apply):

| hyperparameter | value |
|---|---|
| learning rate | 3e-4, constant, no schedule<!-- N:DX-2 --> |
| discount γ; GAE λ | 0.99; 0.95<!-- N:DX-2 --> |
| PPO clip ε | 0.2<!-- N:DX-2 --> |
| entropy coefficient; value coefficient | 0.01; 0.5<!-- N:DX-2 --> |
| global gradient-norm clip; Adam ε | 0.5; 1e-5<!-- N:DX-2 --> |
| parallel environments; steps per update | 256; 128<!-- N:DX-2 --> |
| minibatches; epochs | 4; 4<!-- N:DX-2 --> |
| checkpoint interval | 50 updates<!-- N:DX-2 --> |
| budget | 32,768 environment steps per update, 32,768,000 per run<!-- N:DX-3 --> |

### C Floors

A floor is the standard deviation of a metric over identical reruns at one seed: nondeterminism alone, not seed spread. Floors are per metric, per card, per artifact and per run length; this appendix lists each one the paper uses, with its card, run length, artifact and number of reps. With four reps an sd has 3 degrees of freedom and is uncertain by about ±40 %<!-- N:DX-403 -->; the Phase-6 training floors use eight<!-- N:DX-403 -->.

| study | card | updates | artifact | reps | floor | use |
|---|---|---|---|---|---|---|
| M5.1e | RTX 5090<!-- N:DX-403 --> | 500<!-- N:DX-403 --> | Medium, couplings locked, communication live at δ = 0<!-- N:METH-1 --> | 4<!-- N:DX-403 --> | completion 0.0145, survival 0.0129<!-- N:METH-1 --> | Phase-5 bars |
| M5.5 | RTX PRO 6000<!-- N:DX-412 --> | 500<!-- N:DX-412 --> | Medium, $R_{\mathrm{comm}}$ 16<!-- N:METH-1 --> | 4<!-- N:DX-412 --> | completion 0.0399, survival 0.0130<!-- N:METH-1 --> | with M5.1e, the per-hardware exhibit; card, code tree and configuration all differ |
| M5.5 danger-moment | RTX PRO 6000<!-- N:DX-412 --> | 500<!-- N:DX-412 --> | Medium | 4<!-- N:DX-412 --> | 27.2 % relative nondeterminism (sd 0.00182)<!-- N:COM-5 --> | voids the 20 %<!-- N:COM-5 --> condition (iii) |
| M5.3b | RTX PRO 6000<!-- N:DX-403 --> | 500<!-- N:DX-40 --> | High | 4<!-- N:DX-40 --> | survival 0.0621<!-- N:CB-7 --> | reference scale (cross-artifact) for the Phase-4 High effect |
| M6.0 | RTX PRO 6000<!-- N:DX-5 --> | n/a | field digests, traced vs reference tree | 4 comparisons<!-- N:METH-2 --> | reference tree 0 of 760 differing in 4 of 4; traced tree differs from itself 1 time in 4, on two diagnostic channels<!-- N:METH-2 --> | the per-artifact exhibit |
| M6.2 | RTX PRO 6000<!-- N:DX-34 --> | 500<!-- N:DX-34 --> | ISO, JOINT | 8<!-- N:DX-403 --> | completion ISO 0.0165, JOINT 0.0093<!-- N:DX-34 --> | plateau guard |
| M6.2b | RTX PRO 6000, another box<!-- N:DX-34 --> | 1000<!-- N:DX-34 --> | ISO, JOINT | 8<!-- N:DX-403 --> | completion ISO 0.0339, JOINT 0.0483<!-- N:DX-34 --> | set the design k = 40<!-- N:DES-1 --><!-- N:DX-402 -->; floors grow with run length, 2.1× and 5.2×<!-- N:METH-5 -->, length confounded with box |
| G1.2 launch batch, 2026-08-10<!-- N:DES-5 --> | RTX PRO 6000 | 1000<!-- N:DX-403 --> | ISO, JOINT, sweep endpoint | 8<!-- N:DX-403 --> | design-stage sd(Γ) at k = 40: 0.00504 / 0.00310<!-- N:DES-5 --> | design-stage power; drift ISO 0.56×, JOINT 1.02× its floor<!-- N:DES-10 --> |
| re-floor, 2026-09-08<!-- N:DES-2 --> | RTX PRO 6000<!-- N:DES-2 --> | 1000<!-- N:DX-412 --> | ISO, JOINT, sweep endpoint | 8<!-- N:DX-403 --> | $k_{\mathrm{req}}$ 46<!-- N:DES-2 --> | the ladder; drift ISO 0.80×, JOINT 0.68×<!-- N:DES-10 --> |
| grid-card re-floor | RTX 5090, unit 1<!-- N:DX-35 --> | 1000<!-- N:DX-412 --> | ISO, JOINT, sweep endpoint | 8<!-- N:DX-35 --> | completion ISO 0.0587, JOINT 0.0577; survival 0.0100, 0.0112<!-- N:DX-35 --> | the ladder ($k_{\mathrm{req}}$ 72 / 3<!-- N:DES-3 -->); the beat-reproducibility hurdle; drift ISO 0.33×, JOINT 0.19×<!-- N:DES-10 --> |
| evaluation floor | RTX 5090, unit 3<!-- N:HW-4 --> | evaluation only | two checkpoints | 4<!-- N:HW-2 --> | bit-identical, and identical to the grid's evaluations<!-- N:HW-2 --> | evaluation reproducibility |
| partial re-floor, 2026-08-14<!-- N:DX-36 --> | not recorded<!-- N:DX-36 --> | n/a | ISO, JOINT | 8 ISO + 4 JOINT evaluated<!-- N:DX-36 --> | none reported | provenance only; grades nothing |

The grid card's floors cannot be distinguished from the RTX PRO 6000's: the 95 % intervals for the sd overlap (ISO completion [0.0186, 0.0571] on the RTX PRO 6000 against [0.0388, 0.1194] on the RTX 5090<!-- N:DX-35 -->), and no claim is made that either card is less reproducible.

### D The frozen analysis plan

The registered constants are those of Appendix B: Šidák m = 2 with $z_\alpha$ = 2.2365, T\* = 1000, Γ(t) at 11 checkpoints over updates 500–1000 every 50, k = 20 per secondary arm, k = 72 realized per confirmatory arm, and one evaluation draw, eval seed 0 × 512 episodes<!-- N:DES-13 --><!-- N:DES-3 -->. The reading rules follow, quoted verbatim from the registration record with their dates; emphasis is the record's own, one indented code line is set inline, omissions are marked […], and nothing inside a quotation is paraphrased. A "§" inside a quotation refers to the record's own sections, not to this paper's.

**1. The fixed-budget estimand** (T\* ruling, item 2, 2026-08-11<!-- N:METH-6 -->):

> **Primary Γ = the confirmatory contrast at MATCHED BUDGET T = 1000<!-- N:DES-13 -->, all arms — registered as a fixed-budget claim.**
>
> **"At convergence" is explicitly NOT claimed anywhere.** The paper says **"at matched compute"** throughout, which is also the practitioner-relevant question.

**2. Budget robustness** (T\* ruling, item 3, 2026-08-11<!-- N:METH-6 -->; restated for every branch on 2026-08-13<!-- N:DES-12 -->):

> The fixed-budget conclusion is reported as **budget-robust iff the sign of Γ is stable over the final half of training**. If the sign is still moving at T, **that instability IS the finding** and is reported as such.

> Mechanism: 11 retained checkpoints, updates 500–1000 at interval 50<!-- N:DES-13 -->, confirmatory arms only, **evaluated post-unblind**. Every branch above gains "— budget-robust" or "— sign unstable over the final half" as a suffix, and the suffix is not optional.

**3. The branch-B falsifier** (2026-08-13<!-- N:DES-12 -->):

> Branch B is claimable **only if** the completion contrast excludes an effect as large, in standardized units, as the observed survival effect:
>
> `|z_c| + z_α  <  |z_s|,     z = Γ / sd(Γ) per metric`
>
> with `sd(Γ)` the grid's own measured per-arm seed dispersion in the combined form and `z_α = 2.2365`<!-- N:DES-13 --> the two-sided Šidák critical value at m = 2. **If it fails, the result is branch C with an asymmetry the design could not resolve — not branch B.**

**4. The inert-share reading rule** (the proposals ruling of 2026-09-18<!-- N:DES-15 -->):

> - Γ and Γ₄ are reported **side by side on every branch**, with B̂ and its CI.
> - If Γ rejects on a co-primary and **Γ₄'s CI on that co-primary includes 0 or its sign is opposite**, the paper states that the effect **does not survive the inert-share correction**, in the abstract-level summary and not only in an appendix. **The branch label does not change** — it is fixed by Γ — but branch A/B text may not describe the effect as a composition effect without that qualifier.
> - If Γ is null and Γ₄ is null, Γ₄ is quoted as a second exclusion bound.
> - If Γ is null and Γ₄ rejects **negative**, it is reported under branch D's framing (matched-budget asymmetry) as a secondary observation, never as a confirmatory finding.
> - **No magnitude threshold on B̂ is introduced**, now or later.

**5. The High readout** (the same ruling, 2026-09-18<!-- N:DES-15 -->), its reading for a null:

> - **Γ_H null → an *a fortiori* exclusion**, and the only outcome this readout can establish: *"no gap larger than X at High even where JOINT trained on the evaluated configuration and ISO never saw a composed one."* Quoted as an exclusion with X from the grid's own seed dispersion, never as an absence.

The same entry states that the readout "is NOT a held-out test", that a positive $\Gamma_H$ is "NOT separable from in-distribution advantage", and that a negative one is "exploratory".

**6. The T = 2000 subsample** (the same ruling, 2026-09-18<!-- N:DES-15 -->):

> **What it may be cited for:** whether the differential drift measured at T = 1000 (review §6 item 1: 0.01209 per 100 updates<!-- N:DES-10 -->) visibly persists, closes or reverses. **What it may not be cited for:** any claim that Γ "holds" or "vanishes" at T = 2000.

**7. The mediation void rule** (the design's frozen analysis plan, ruled 2026-08-02<!-- N:DX-414 -->):

> **If realized dose does not vary with assigned p, the dose figure has no x-axis and is declared VOID** — registered now, not decided after seeing the first stage.

**8. The pre-unblind rulings** (2026-09-26<!-- N:DX-405 -->, before the look):

| # | question | RULED |
|---|---|---|
| (i) | what "−" means in the branch table | **Rejection with negative sign** (\|z\| > z_α, Γ < 0). A negative estimate that does not reject is a null. Ratified as built. |
| (ii) | the cell (completion +, survival null), absent from the registered table | **REGISTERED NOW as branch A_c — the founding claim on the founding primary.** […] |
| (iii) | test statistic | **Normal z, z_α = 2.2365<!-- N:DES-13 -->**, as the frozen plan wrote; the t critical value is printed, not applied. Ratified as built. |
| (iv) | Γ(t) "sign stable" | **All 11 point estimates, t = 500 … 1000, share one nonzero sign**, per co-primary; t = 1000 is the grid's own eval. Consequence accepted in advance: on a null Γ, chance flips read UNSTABLE. Ratified as built. |
| (v) | Γ₄ sample and threshold | **JOINT k = 72 vs ISO-4 k = 20<!-- N:DES-3 --><!-- N:DES-13 -->**, SE `sqrt(s_J²/72 + s_4²/20)`, "rejects" and "CI includes 0" at z_α = 2.2365. (Γ null, Γ₄ rejects positive) stays UNREGISTERED. Ratified as built. |
| (vi) | Γ_H reading | **As (i), at z_α = 2.2365.** Ratified as built. |
| (vii) | primary k | **k = 72 stays primary**; the registered-ladder k = 60<!-- N:DES-1 --> prefix is reported beside it, UNDERPOWERED-flagged. |
| (viii) | re-evaluate the 144 T\* = 1000 checkpoints on the post-unblind card | **YES.** […] |

The 144 checkpoints of (viii) are the 72 seeds of each confirmatory arm<!-- N:DES-3 -->. Branch $A_c$ of (ii) is in Appendix E; (viii) produced the single-card curve of Appendix H.

**9. The secondary specification** (ratified 2026-09-26, after unblinding and before the sweep was read<!-- N:DX-413 -->):

> (S1) PAVA + OLS slope CI; (S2) single-hinge breakpoint, UNDERPOWERED iff the CI spans {0.125 … 0.375}<!-- N:DX-28 -->; (S3) plane fit, bound = 95 % CI of 0.5·γ_n; (S4) training co-activity over updates 1…1000, VOID iff the first-stage CI contains 0; (S5) the same-card replicate is ADDED, beside Γ₄, unable to change its qualifier; (S6) 95 % intervals, Γ₄′ at z_α. […]

The omitted words name the code version, which identifies the repository.

### E The registered outcome branches

"Positive" and "null" mean rejection or non-rejection in the confirmatory family (Γ on completion and on survival) at θ\*, Šidák m = 2, graded on the grid's own per-arm seed dispersion; "−" means rejection with negative sign (Appendix D, item 8 (i)). Branches A–D were registered on 2026-08-13<!-- N:DES-12 --> with a framing each; the registered table's fifth column, a venue lean, is omitted here. $A_c$ was registered on 2026-09-26<!-- N:DX-405 -->, before the look, for a cell the table did not contain.

| branch | completion | survival | headline claim, as registered ($A_c$: its registered claims, summarized) |
|---|---|---|---|
| A | + | + | founding registration, verbatim |
| B | null | + | composition is paid in **agents**, not task return |
| C | null | null | the instrument, and what it excludes |
| D | − on either co-primary | − on either co-primary | not separable from the matched-budget asymmetry |
| $A_c$ | + | null | the founding claim on the founding primary; the survival null quoted as an exclusion; no asymmetry claim |

The result is branch B, with the falsifier passing and the inert-share qualifier attached (§9.2).

### F Grid provenance

- **The grid.** 252 runs<!-- N:DX-30 -->, run from 2026-09-09 to 2026-09-22<!-- N:DES-12 -->: seeds 1–12 of all 10 arms on an RTX PRO 6000, then seeds 13–20 of all 10 arms and 21–46 of ISO and JOINT on an RTX 5090<!-- N:DX-30 -->. The 10 arms are ISO, JOINT and the 8 secondary arms.
- **The confirmatory artifact.** All 72 seeds of ISO and JOINT on one RTX 5090 unit: 76 runs executed there (seeds 1–12 and 47–72 of both arms<!-- N:DX-4 -->) plus seeds 13–46 copied from the grid<!-- N:DX-30 -->. The grid's RTX PRO 6000 seeds 1–12 were superseded and enter only a descriptive card diagnostic.
- **Secondary arms.** Seeds 1–12 of the 8 secondary arms were re-run on the same unit, 96 runs<!-- N:DX-30 -->; seeds 13–20 come from the grid. Every analysed secondary run is on unit 1.
- **Other blocks.** ISO-4 (20 seeds<!-- N:DES-13 -->) and the T = 2000 subsample (4 seeds per arm<!-- N:RES-15 -->) trained on a second RTX 5090 unit; the post-unblind evaluations ran on a third<!-- N:HW-4 -->.
- **Seeds.** Every arm uses the same seed integers; seed 0 is reserved for floors and never enters the grid<!-- N:DX-416 -->; runs are ordered seed-major, so that an interruption leaves a smaller balanced design rather than a complete arm beside an empty one; and the grid ran in chunks that end on seed boundaries, so both arms of a seed share a card. Tests in `che/tests/test_p6_grid.py` assert each property.
- **Archives.** Every checkpoint was archived off the rented machine as a compressed archive with a sha256 recorded beside it, and the job scripts fail a run whose archive or hash is missing. A re-verification on 2026-09-27 matched every recorded hash, 615 of 615<!-- N:DX-408 -->. No hash is quoted here.
- **What grades nothing.** A partial re-floor on a second rented card on 2026-08-14 (8 ISO and 4 JOINT evaluated reps, card not recorded<!-- N:DX-36 -->) is provenance only; of its 12 archives, one has a recorded hash<!-- N:DX-408 -->.

### G Throughput

The paper states no environment-only throughput figure. Under the compiler's dead-code elimination, an environment-only figure depends on which outputs its consumer reads, so any such figure would have to state its keep-alive set; none is needed here. The only cost figures are training measurements: 518–521 s per 1000-update training run and 9–10 s per 512-episode evaluation on one RTX 5090<!-- N:DX-4 -->, at 32,768,000 environment steps per run<!-- N:DX-3 -->, each step advancing all 12 agents<!-- N:ENV-6 -->.

### H Gamma(t) over the final half

**Sign unstable over the final half**, on both co-primaries<!-- N:RES-11 -->: the registered rule (Appendix D, item 2; ruling (iv) in item 8) requires all 11 point estimates to share one sign, and neither co-primary meets it. The tables are in rates (four decimals); intervals are Šidák-corrected at the family level, registered at t = 1000 and descriptive at every t < 1000, where no test is registered. Checkpoints t < 1000 were evaluated on the post-unblind unit; t = 1000 is the grid's own evaluation. Across cards at T\*, 280 of 288 paired evaluations are identical<!-- N:HW-3 -->, and the curve with t = 1000 re-evaluated on the post-unblind unit has the same signs on both metrics.

Completion, k = 72 per arm<!-- N:DES-13 -->:

| t | Γ(t) | sd(Γ) | Šidák CI | sign |
|---|---|---|---|---|
| 500 | +0.0017<!-- N:DX-24 --> | 0.00321<!-- N:DX-24 --> | [−0.0055, +0.0089]<!-- N:DX-24 --> | + |
| 550 | −0.0017<!-- N:DX-24 --> | 0.00353<!-- N:DX-24 --> | [−0.0096, +0.0062]<!-- N:DX-24 --> | − |
| 600 | +0.0018<!-- N:DX-24 --> | 0.00362<!-- N:DX-24 --> | [−0.0063, +0.0099]<!-- N:DX-24 --> | + |
| 650 | +0.0015<!-- N:DX-24 --> | 0.00481<!-- N:DX-24 --> | [−0.0093, +0.0122]<!-- N:DX-24 --> | + |
| 700 | −0.0037<!-- N:DX-24 --> | 0.00470<!-- N:DX-24 --> | [−0.0142, +0.0068]<!-- N:DX-24 --> | − |
| 750 | −0.0147<!-- N:RES-13 --> | 0.00610<!-- N:DX-24 --> | [−0.0283, −0.0010]<!-- N:RES-13 --> | − |
| 800 | −0.0035<!-- N:DX-24 --> | 0.00677<!-- N:DX-24 --> | [−0.0187, +0.0116]<!-- N:DX-24 --> | − |
| 850 | −0.0053<!-- N:DX-24 --> | 0.00729<!-- N:DX-24 --> | [−0.0216, +0.0110]<!-- N:DX-24 --> | − |
| 900 | −0.0039<!-- N:DX-24 --> | 0.00843<!-- N:DX-24 --> | [−0.0228, +0.0149]<!-- N:DX-24 --> | − |
| 950 | −0.0016<!-- N:DX-24 --> | 0.01021<!-- N:DX-24 --> | [−0.0245, +0.0212]<!-- N:DX-24 --> | − |
| 1000 | −0.0173<!-- N:RES-1 --> | 0.01068<!-- N:DX-24 --> | [−0.0412, +0.0066]<!-- N:RES-1 --> | − |

Survival rate, k = 72 per arm<!-- N:DES-13 -->:

| t | Γ(t) | sd(Γ) | Šidák CI | sign |
|---|---|---|---|---|
| 500 | +0.0022<!-- N:DX-25 --> | 0.00228<!-- N:DX-25 --> | [−0.0029, +0.0073]<!-- N:DX-25 --> | + |
| 550 | −0.0037<!-- N:DX-25 --> | 0.00220<!-- N:DX-25 --> | [−0.0086, +0.0013]<!-- N:DX-25 --> | − |
| 600 | −0.0027<!-- N:DX-25 --> | 0.00232<!-- N:DX-25 --> | [−0.0078, +0.0025]<!-- N:DX-25 --> | − |
| 650 | +0.0011<!-- N:DX-25 --> | 0.00242<!-- N:DX-25 --> | [−0.0043, +0.0065]<!-- N:DX-25 --> | + |
| 700 | +0.0031<!-- N:DX-25 --> | 0.00235<!-- N:DX-25 --> | [−0.0021, +0.0084]<!-- N:DX-25 --> | + |
| 750 | +0.0036<!-- N:DX-25 --> | 0.00255<!-- N:DX-25 --> | [−0.0021, +0.0093]<!-- N:DX-25 --> | + |
| 800 | +0.0020<!-- N:DX-25 --> | 0.00232<!-- N:DX-25 --> | [−0.0032, +0.0072]<!-- N:DX-25 --> | + |
| 850 | +0.0018<!-- N:DX-25 --> | 0.00234<!-- N:DX-25 --> | [−0.0034, +0.0071]<!-- N:DX-25 --> | + |
| 900 | +0.0056<!-- N:RES-12 --> | 0.00231<!-- N:DX-25 --> | [+0.0004, +0.0108]<!-- N:DX-25 --> | + |
| 950 | +0.0083<!-- N:RES-12 --> | 0.00219<!-- N:DX-25 --> | [+0.0034, +0.0132]<!-- N:DX-25 --> | + |
| 1000 | +0.0096<!-- N:RES-2 --> | 0.00216<!-- N:DX-25 --> | [+0.0047, +0.0144]<!-- N:RES-2 --> | + |

The signs read `+ − + + − − − − − − −` on completion and `+ − − + + + + + + + +` on survival<!-- N:RES-11 -->. On survival, only t = 900, 950 and 1000 have intervals excluding zero<!-- N:RES-12 -->; on completion, only t = 750<!-- N:RES-13 -->. These describe the trajectory of the arm-mean difference; they are not tests, and no trend is fitted to them.

### I The secondary design

Everything here is secondary and **non-verdict-bearing**. Intervals are 95 %, bootstrap over seeds within arm (B = 2000<!-- N:DX-28 -->), conditional on the common evaluation draw, and there are many of them, none family-corrected. Each arm has k = 20 seeds<!-- N:DES-13 --> on the confirmatory unit, with δ off. The per-coupling marginal is written $\mu$ and the fire-only share $\nu$ (Figure 13 labels them m and n); on the simplex $\nu = 1 - 2\mu + p$.

| arm | per-coupling marginal $\mu$ | co-occurrence $p$ | fire-only share $\nu$ |
|---|---|---|---|
| `sweep_c50_p000` | 0.5<!-- N:DES-9 --> | 0<!-- N:DX-28 --> | 0<!-- N:DES-9 --> |
| `sweep_c50_p125` | 0.5<!-- N:DES-9 --> | 0.125<!-- N:DX-28 --> | 0.125<!-- N:DES-9 --> |
| `sweep_c50_p250` | 0.5<!-- N:DES-9 --> | 0.25<!-- N:DX-28 --> | 0.25<!-- N:DES-9 --> |
| `sweep_c50_p375` | 0.5<!-- N:DES-9 --> | 0.375<!-- N:DX-28 --> | 0.375<!-- N:DES-9 --> |
| `sweep_c50_p500` | 0.5<!-- N:DES-9 --> | 0.5<!-- N:DX-28 --> | 0.5<!-- N:DES-9 --> |
| `ident_c40_p000` | 0.4<!-- N:DES-9 --> | 0<!-- N:DX-28 --> | 0.2<!-- N:DES-9 --> |
| `ident_c40_p200` | 0.4<!-- N:DES-9 --> | 0.2<!-- N:DX-28 --> | 0.4<!-- N:DES-9 --> |
| `ident_c40_p400` | 0.4<!-- N:DES-9 --> | 0.4<!-- N:DX-28 --> | 0.6<!-- N:DES-9 --> |

`sweep_c50_p000` carries exactly ISO-4's training mixture. Sweep means at θ\*, by $p$ = 0, 0.125, 0.25, 0.375, 0.5: survival 0.9241 / 0.9249 / 0.9261 / 0.9264 / 0.9289; completion 0.7847 / 0.7775 / 0.7797 / 0.7656 / 0.7749<!-- N:DX-28 -->.

| estimate (points) | survival | completion |
|---|---|---|
| dose slope, sweep, per unit $p$ (separate OLS fit) | +0.89 [−0.33, +2.11]<!-- N:SEC-5 --> | −2.51 [−9.43, +4.12]<!-- N:DX-27 --> |
| endpoint, $p$ = 0.5 minus $p$ = 0 | +0.48 [−0.21, +1.17]<!-- N:SEC-5 --> | −0.97 [−4.82, +2.87]<!-- N:DX-27 --> |
| $\gamma_p$, per unit co-occurrence | +3.26 [+1.37, +5.02]<!-- N:SEC-1 --> | +2.69 [−6.75, +12.45]<!-- N:DX-27 --> |
| $\gamma_n$, per unit fire-only share | −2.37 [−4.19, −0.57]<!-- N:SEC-1 --> | −6.52 [−15.34, +2.42]<!-- N:DX-27 --> |
| bound, $0.5\,\gamma_n$ | −1.19 [−2.10, −0.28]<!-- N:SEC-2 --> | −3.26 [−7.67, +1.21]<!-- N:DX-27 --> |
| knee | 0.375 [0.125, 0.375]<!-- N:DX-28 -->, UNDERPOWERED<!-- N:SEC-6 --> | 0.375 [0.125, 0.375]<!-- N:DX-28 -->, UNDERPOWERED<!-- N:SEC-6 --> |
| plane prediction, ISO-4 − ISO (from $\gamma_n$) | +0.79<!-- N:SEC-3 -->; measured B̂ +0.98 [+0.33, +1.63]<!-- N:RES-7 --> | not drawn in Figure 13, and no value stated |
| plane prediction, JOINT − ISO-4 (from $\gamma_p$, at $p$ = 1<!-- N:DES-7 -->) | +3.26<!-- N:SEC-4 -->; measured Γ₄ −0.03<!-- N:RES-6 -->, Γ₄′ +0.13<!-- N:RES-8 --> | +2.69 ($\gamma_p$ × 1)<!-- N:DX-27 --><!-- N:DX-417 -->; measured Γ₄ −1.26<!-- N:RES-6 -->, Γ₄′ −2.47<!-- N:RES-8 --> |

The plane is $y = \gamma_0 + \gamma_p p + \gamma_n \nu$, fitted by seed-level least squares over all eight arms; the bound is the no-element confound's share of the sweep's endpoint change. In the plane the slope along the sweep is $\gamma_p + \gamma_n$; the sweep's own slope in the first row is a separate least-squares fit, so the two need not agree (on completion they do not). Linearity is assumed and checked only coarsely: arm-mean residuals from the plane lie within ±0.4 SE on survival and ±1.1 SE on completion, 8 points for 3 parameters<!-- N:DX-39 -->.

**The same-card replicate** (S5), at $z_\alpha$ for Γ₄′ and 95 % for the replicate difference:

| metric | Γ₄′ = JOINT − `sweep_c50_p000` | `sweep_c50_p000` − ISO-4 (cross-card) |
|---|---|---|
| completion | −2.47<!-- N:RES-8 -->, z −1.50, Šidák [−6.16, +1.22]<!-- N:DX-19 --> | +1.21 [−2.79, +5.20]<!-- N:DX-19 --> |
| survival | +0.13, z +0.41, Šidák [−0.56, +0.81]<!-- N:RES-8 --> | −0.15 [−0.86, +0.56]<!-- N:RES-9 --> |

Arm means: ISO-4 0.7726 (completion) and 0.9256 (survival); `sweep_c50_p000` 0.7847 and 0.9241<!-- N:DX-18 -->.

**Mediation: VOID.** The first-stage slope of realized training dose on $p$ is −1.03 × 10⁻⁵ per unit $p$, 95 % [−2.91 × 10⁻⁵, +0.93 × 10⁻⁵]<!-- N:DX-29 -->; its interval contains zero, so by the registered rule mediation is VOID<!-- N:SEC-7 -->. The counter behind the dose counts collapse-seeded ignitions near alive agents, which Coupling A produces with or without Coupling B, so in mixtures it tracks the A marginal that the sweep holds fixed.

**What this instrument is blind to.** Linearity in $(p, \nu)$ is an assumption, tested only by the coarse residuals above. Per-coupling marginal, co-occurrence and active share cannot all be held fixed on the simplex, and $\gamma_p$ moves single-stressor mass into both-stressor episodes, which also raises per-coupling exposure. Floors exist only for the sweep endpoint, $p$ = 0.5: the intermediate arms assume it, and the identification arms are ungraded<!-- N:DX-306 -->. Realized dose is endogenous; nothing here is a causal effect of it.

### J Trained-policy episodes

Figures J1 and J2 show one pre-selected episode of each confirmatory arm, separately. The selection rule was fixed before any render and chooses nothing from a set: θ\*, episode key 0, stochastic actions, training seed 1 at update 1000 of each arm<!-- N:ENV-13 -->. The explorers illustrate the environment under a trained policy; they grade nothing. The measured contrasts are in §9.2. Figure J1 shows the ISO policy's episode.

<figure class="l-page">
  <iframe src="{{ 'assets/html/submission/explorer_thetastar_iso_s1_T1000_ep0.html' | relative_url }}" width="100%" height="720" style="border:none" title="Episode explorer, ISO policy, training seed 1" loading="lazy"></iframe>
  <figcaption><strong>Figure J1.</strong> One pre-selected episode of the ISO policy (training seed 1, update 1000) at θ&#42; (β 0.49, κ<sub>A</sub> 0.06, κ<sub>B</sub> 1.0, δ 1.0<!-- N:CAL-3 --><!-- N:CA-1 --><!-- N:CB-1 --><!-- N:COM-6 -->), episode key 0<!-- N:ENV-13 -->, on the 64 × 64 grid with 12 agents over 256 steps<!-- N:ENV-6 -->. The map layers are the fire state, the smoke density ρ (the environment's field, not what any agent sees), weak and collapsed floor, collapse-seeded ignitions, food, and agents alive or dead. Selecting an agent shows three 9 × 9<!-- N:ENV-6 --> panels for that step: its observation as produced, the true state of the same cells, and the probability that each cell was seen, τ, the Beer–Lambert transmittance. The figure shows one episode of one training seed; it carries no alive count, completion or return, and it cannot show any difference between training protocols. Any drift towards a wall late in an episode is the known artifact of §10, not a behaviour of interest. <span class="figure-note">Status: illustrative · ISO policy, training seed 1 · grades nothing · Interact: play or pause (space), step (← →, shift for 10), scrub, change speed; jump between collapse events and seeded ignitions with [ and ]; select an agent by clicking its marker or pressing 1–9; toggle layers. Opens at t = 128<!-- N:DX-410 -->.</span></figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/explorer_thetastar_iso_s1_T1000_ep0_static.png" class="img-fluid" alt="Maps of one ISO-policy episode at its start, middle and end, with one agent's observation, the true state of the same cells, and the probability each cell was seen" caption="Static companion of Figure J1 for the printed PDF." %}
</div>

Figure J2 shows the JOINT policy's episode under the same rule. The two figures are deliberately not placed side by side: a single episode of a single seed cannot carry a contrast that §9.2 measures over 72 seeds per arm and a common set of 512 evaluation episodes<!-- N:DES-3 --><!-- N:DES-13 -->, and nothing in either episode is offered as evidence for or against it.

<figure class="l-page">
  <iframe src="{{ 'assets/html/submission/explorer_thetastar_joint_s1_T1000_ep0.html' | relative_url }}" width="100%" height="720" style="border:none" title="Episode explorer, JOINT policy, training seed 1" loading="lazy"></iframe>
  <figcaption><strong>Figure J2.</strong> One pre-selected episode of the JOINT policy (training seed 1, update 1000) at θ&#42; (β 0.49, κ<sub>A</sub> 0.06, κ<sub>B</sub> 1.0, δ 1.0<!-- N:CAL-3 --><!-- N:CA-1 --><!-- N:CB-1 --><!-- N:COM-6 -->), episode key 0<!-- N:ENV-13 -->, on the 64 × 64 grid with 12 agents over 256 steps<!-- N:ENV-6 -->. The layers and panels are those of Figure J1: the map's smoke layer is the environment's field ρ, and only the observation panel shows what the selected agent perceives. The figure shows one episode of one training seed; it carries no alive count, completion or return, and it cannot show any difference between training protocols. <span class="figure-note">Status: illustrative · JOINT policy, training seed 1 · grades nothing · Interact: as Figure J1 (play, step, scrub, speed; [ and ] for events; click or 1–9 for an agent; layer toggles). Opens at t = 128<!-- N:DX-410 -->.</span></figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/explorer_thetastar_joint_s1_T1000_ep0_static.png" class="img-fluid" alt="Maps of one JOINT-policy episode at its start, middle and end, with one agent's observation, the true state of the same cells, and the probability each cell was seen" caption="Static companion of Figure J2 for the printed PDF." %}
</div>
