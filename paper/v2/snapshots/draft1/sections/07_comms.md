<!-- PAPER V2 DRAFT (PAPER V2 ruling, 2026-10-11): builder-drafted, not owner-approved -->

## 7 Communication denial: inert under this encoder at this scale

<!-- STUB-SPEC
PURPOSE: The third stressor denies inter-agent links and, unlike the couplings, is independent of the fire. State Def. 7 as implemented and the line that makes the channel non-differentiable (Listing 6); state Remark 2′ after citing Pynadath and Tambe (READS RULING item 4); report the toy handshake and the three measurements in CHE as bars (post-hoc floor grading, about 50 % power); give the two-part argument for inertness with the record's demand-side reading and its two qualifications; end with one neutral sentence that the δ-only third of ISO's training is therefore fire-only, pointing to section 9.1 for the consequence.
SUBSECTIONS (H3, as the demo's): 7.1 The kernel; 7.2 When communication should matter; 7.3 In CHE the channel carries nothing measurable.
WRITER: W4. BUDGET: 800 prose words (the demo's: 1,295); Figure 9 caption at most 80 words.
REQUIRED FACTS: COM-6 (R_comm = 16 cells; δ = 1.0 locked 2026-07-30); DX-17 (messages of dimension 8, one-step latency, masked-mean pooling, Chebyshev range, thinning by 1 − δ with unconditional uniforms); ENV-12 (the message head receives no gradient; receivers' weights are trained); ENV-1 (d_p = 0.5 in Remark 2′(i)'s qualifier); COM-1 (the toy's value of communication rises from 0 to 0.498); DX-15 (the toy's constants: 4096 episodes and 8192 Monte Carlo draws per point; free arm 1.0000; largest absolute z 0.44, χ² 0.51 on 8 degrees of freedom; q̃/q 1.126 at κ_B 1.0, peak 1.235; 79 / 54 / 7 % at κ_B 0.5 / 1.0 / 3.0: these move to Appendix A, LEN); ENV-6 and ENV-11 (twelve interchangeable agents sharing one set of parameters); COM-2 and DX-305 (Medium content ablation, two seeds, R_comm 8, δ = 0, 500 updates; bar about 3 points); COM-3 and DX-16 (High, three seeds, R_comm 8 and 16; out-degree 1.01 to 2.99 changed nothing; bar about 11 points); COM-4 (the denial element at Medium, four seeds, R_comm 16: completion +0.38 points against a bar of 7.99, survival −1.43 against 2.60; both bars twice the floor sd on that GPU); COM-5 (condition (iii) VOID: a 20 % threshold chosen at implementation, below the quantity's own 27.2 % nondeterminism; observed 23.2 %); DES-8 (the δ-only third).
CITATIONS: pynadath2002 (their Theorem 4 and Table 2; Theorems 5 and 6; Theorem 3 only if the owner approves, P3-N12).
FIGURES: Figure 9, static fig06_comms.png (include plus a caption paragraph), carried below. Caption at most 80 words: (a) is the toy with scripted policies, (b to d) are CHE at Medium with post-hoc floor-grading bars; the figure carries no word "inert"; it cannot show the content ablations, the High runs, the VOID condition, or a trained encoder; glosses any study code it prints.
LISTINGS (carried below, exact lines): Listing 6, che/train/ippo.py:323-329: stop_gradient on the delivered messages, so no gradient crosses the channel and the encoder stays at initialization. Prose does not echo "Q3 ruling".
LATEX: Def. 7's link probability (one display); Remark 2′'s statement with the VoC display (one display), stated in full here (READS RULING item 4: cite first, refine second). Remark 2 (superseded) is not stated.
HONESTY LINES AND REGISTERED STRINGS: branch_B section 5 line 4 (δ is inert; the composition tested is A × B; θ* keeps δ = 1.0 for fidelity to the registration). The full phrase "inert under a frozen random-projection encoder at this scale" has its home here. "VOID" for condition (iii). Each measurement is a bar, a post-hoc floor grading at about 50 % power, never a point null and never "excludes effects larger than". The frozen-encoder caveat: a cap measured on a frozen random encoder does not strictly bound a trained one (log:1102-1104); gradient-shaped messaging is untested (log:1106-1107); d_p prices deaths, so Remark 2′(i)'s clean-zero conditions are not fully met (log:1083-1088).
FIX-LIST AND FINDINGS ITEMS OWNED: F3 (the last paragraph is a neutral pointer: the δ-only episodes are fire-only and section 9.1 states the consequence; never "the bias that §9 registers and corrects"); F5 (M5.2, M5.3, M5.3b, M5.5 named as studies: the courier toy, the Medium content ablation, the High content ablation, the denial study); LEN (toy constants to Appendix A; "Three consequences carry into §9" and "The null rests on two halves" become plain sentences without announcing a count); P3-N9 and P3-N10 (class C: keep the theory doc's wording of Remark 2′); P3-N12 (class C: Theorem 3 not added); P3-N17 (class C: the demand-side reading kept, attributed to the record, log:1076-1081); Q23, Q24.
DEMO KEEPS (sections/07_comms.md): Def. 7; Listing 6 and its gloss; Remark 2′ cited first, refined second; the three measurements with their bars; the VOID condition in one sentence (its methods lesson lives in section 8.1); the demand-side argument; the two qualifications. CHANGES: constants to Appendix A; study codes to plain names; the last paragraph to a pointer. DROPS: announced enumerations; the duplicate of section 2's Pynadath and Tambe summary beyond what the citation needs.
NOT HERE: "certified inert"; that trained messages would also be useless; a point null; the 5/3 constant; that communication is load-bearing in CHE; "the swarm does not need the information" (say "the agents"); any statement that the design caught or foresaw the inert share.
DEPENDENCIES: sections 1 and 9.1 rely on "δ inert under this encoder at this scale" to define ISO's fire-only third; section 8.1 carries COM-5's lesson; Appendix A carries the toy's constants.
-->

The third stressor denies links between agents; in CHE it had no measurable effect (Figure 9).

{% include figure.html path="assets/img/submission/fig06_comms.png" class="img-fluid" alt="Top left, courier success rate against perception attenuation in the two-agent toy, for free and for denied communication, with the predicted curve. Top right, the denial contrasts at medium severity with their bars. Bottom, the per-run values behind those contrasts." caption="Figure 9. Communication in the toy, and denial in CHE at Medium." %}

<p class="caption">(a) The courier variant of the corridor toy (labelled E2C² and M5.2), scripted policies: success with free and with denied communication on the no-idle schedule (pinned); the shaded gap is VoC<sub>gated</sub> (§7.2). (b–d) The denial study (M5.5): contrasts against bars (post-hoc floor grading), and the runs. No panel grades inertness or shows the content ablations, High severity, the VOID condition or a trained encoder. <span class="figure-note">Status: descriptive · static.</span></p>

### 7.1 The kernel

**Definition 7 (Communication denial, as implemented).** After the agents move, the comms kernel $T_K(k' \mid x')$ samples a directed link graph over the alive agents: for every ordered pair $i \ne j$ of alive agents,

$$
\Pr\big[\, i \to j \text{ open} \,\big] = \mathbf{1}\big[\lVert x'_i - x'_j \rVert_\infty \le R_{\mathrm{comm}}\big]\,(1 - \delta),
$$

with $R_{\mathrm{comm}} = 16$<!-- N:COM-6 --> cells. Each agent emits a message $m_i \in [-1, 1]^{8}$<!-- N:DX-17 --> at step $t$; at $t + 1$ each receiver $j$ gets the mean of the messages delivered over the links then realized, $\bar m_j = \sum_i k'_{ij}\, m_i \,/\, \max(1, \sum_i k'_{ij})$, which is the zero vector when $j$ is isolated. $T_K$ reads positions and aliveness only, so denial is mechanistically independent of the fire. One uniform per ordered pair is drawn at every step whatever $\delta$ is, so $\delta = 0$ gives the deterministic range graph and $\delta = 1$, the value locked on 2026-07-30<!-- N:DX-401 -->, gives the empty graph, both bitwise. The theory's range-dependent link probability is implemented as this hard Chebyshev range.

**Listing 6.** Delivered messages carry no gradient.

<!-- LISTING: che/train/ippo.py:323-329 -->
```python
# che/train/ippo.py:323-329 (verbatim)
        # Messages emitted this step are delivered next step. Nothing crosses
        # an episode boundary (autoreset), and stop_gradient states in code
        # what the batch-storage already implies: the channel is not a
        # differentiable path (Q3 ruling; networks.py docstring).
        messages = jax.lax.stop_gradient(
            jnp.where(done[:, None, None], 0.0, emitted)
        )
```

No gradient crosses the channel, so the message head, a tanh-bounded dense layer on the shared trunk, stays at its initialization for the whole run<!-- N:ENV-12 -->: an agent emits a frozen random projection of trunk features that are themselves trained. The receivers' weights on the message inputs are trained, so whether agents use messages can be tested; what to say was never learned.

### 7.2 When communication should matter

Remark 2′ refines a result of Pynadath & Tambe <d-cite key="pynadath2002"></d-cite>. Free communication lowers the complexity of the team decision problem when the world is collectively observable (their Theorem 4 and Table 2), and makes no difference when it is individually observable or not observable at all (their Theorems 5–6). Remark 2′ concerns the value of communication under collective partial observability.

**Remark 2′.** Extend $E_{2C}$ with a second agent. (i) Under a team-any reward, communication has zero marginal value when the agents are interchangeable, expendable (no death cost) and at least as numerous as the hypotheses: coverage then achieves $J = 1$ under total denial. When any qualifier fails, value returns; in general it scales with the deficit of agents relative to hypotheses, and a death cost, such as CHE's $d_p = 0.5$<!-- N:ENV-1 -->, prices the redundancy that substitution spends. (ii) In the courier variant, where only agent 1 can complete the task and it observes the other agent only through messages, the denied optimum within the no-idle policy class is $\tfrac12 + \tfrac12 q(\kappa_B)$; with slack $\ell_f$, optimal denied play buys information by idling at the branch and achieves $\tfrac12 + \tfrac12 \tilde q(\kappa_B)$, where $\tilde q$ is the probability of being informed by the commitment point under the best idling schedule, with $\tilde q \ge q$ (equality iff $\ell_f = 0$), so

$$
\mathrm{VoC}_{\mathrm{true}}(\kappa_B) = \tfrac12\big(1 - \tilde q(\kappa_B)\big) \le \tfrac12\big(1 - q(\kappa_B)\big).
$$

Both $q$ and $\tilde q$ decrease in $\kappa_B$, so the value of communication increases with perception decay.

We ran the courier variant with scripted policies, delivering messages through the production link kernel and computing $\tau$ with the shared transmittance function, so the toy also tests both kernels. The free arm always succeeds<!-- N:DX-15 -->, the no-idle denied arm matches $\tfrac12 + \tfrac12 q$, and the value of communication against that arm, $\mathrm{VoC}_{\mathrm{gated}} = \tfrac12(1 - q)$, rises monotonically from 0 to 0.498<!-- N:COM-1 --> (Figure 9(a); Appendix A).

### 7.3 In CHE the channel carries nothing measurable

CHE's agents meet one of Remark 2′(i)'s qualifiers: they are twelve<!-- N:ENV-6 --> interchangeable agents sharing one set of parameters<!-- N:ENV-11 -->. Nothing establishes that they are at least as numerous as the hypotheses, and their deaths are priced ($d_p = 0.5$<!-- N:ENV-1 -->), so the clean-zero conditions are not fully met.

In a content ablation at Medium ($\delta = 0$, $R_{\mathrm{comm}} = 8$<!-- N:COM-2 -->, two seeds<!-- N:COM-2 -->, 500 updates<!-- N:DX-305 -->), three arms of identical architecture pass live, zeroed or shuffled messages (the delivered aggregate set to zero with links kept; sender identities permuted within a step). No pair differs beyond a bar of twice the earlier Medium floor, about 3 points<!-- N:COM-2 -->. The same ablation at High (three seeds, $R_{\mathrm{comm}}$ = 8 and 16<!-- N:DX-16 -->) found that tripling the mean alive out-degree, from 1.01 to 2.99<!-- N:COM-3 -->, changed nothing, ruling out "nobody was in range". The wider High floor puts that bar at about 11 points<!-- N:DX-16 -->.

In the denial study (Medium, four seeds, $R_{\mathrm{comm}} = 16$<!-- N:COM-4 -->, message path live in both arms), $\delta = 0$ against $\delta = 1$ moves completion by +0.38 points against a bar of 7.99 points, and survival by −1.43 points against a bar of 2.60 points<!-- N:COM-4 -->. Both bars are twice<!-- N:V4-2 --> the floor sd measured on that GPU (Figure 9(b–d)). Every bar here is a post-hoc floor grading that a true effect of its size would clear only about half the time<!-- N:V4-1 --> (§8.2), so none of these results is a point null. A further condition, on danger-moment outcomes, is VOID: its threshold, chosen at implementation, sat below the quantity's own run-to-run nondeterminism (§8.1).

The content ablations supply a mechanism: in the live arm a receiver can tell that it heard from someone without decoding anything; in the zeroed arm it cannot. That signal needs no encoder and went unused at both severities and, at High, at both ranges. The neglect is therefore on the demand side (the agents did not need the information) rather than the channel side (they could not read it), and the frozen encoder cannot account for it.

With deaths priced, the null also says that the value returning when a qualifier fails is weak at this scale and this death price. Gradient-shaped messaging is untested, and a bound measured on a frozen random encoder does not strictly bound a trained one. We claim only that communication denial is inert under a frozen random-projection encoder at this scale.

The composition §9 tests is thus, in effect, Coupling A × Coupling B, with $\delta = 1.0$<!-- N:COM-6 --> kept in $\theta^*$ for fidelity to the registration. The δ-only third<!-- N:DES-8 --> of ISO's training is fire-only, and §9.1 gives the consequence.
