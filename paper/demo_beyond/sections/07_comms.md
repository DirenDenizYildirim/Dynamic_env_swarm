<!-- BUILDER-WRITTEN DEMONSTRATION (DEMONSTRATION DRAFT ruling, 2026-10-11); not the owner's text -->

## 7 Communication denial: inert under this encoder at this scale

The third stressor denies inter-agent links. Unlike the couplings it is independent of the fire by construction, and in CHE it had no measurable effect. This section states the kernel (§7.1), the theory of when communication should matter (§7.2), the measurements (§7.3), and how far the null reaches: communication denial is inert under a frozen random-projection message encoder at this scale, and no further. Figure 9 sets the toy, where communication matters by construction, beside the denial contrast in CHE.

{% include figure.html path="assets/img/submission/fig06_comms.png" class="img-fluid" alt="Top left, courier success rate against perception attenuation in the two-agent toy, for free and for denied communication, with the predicted curve. Top right, the denial contrasts at medium severity with their bars. Bottom, the per-run values behind those contrasts." caption="Figure 9. The value of communication in the toy, and the denial contrast in CHE at Medium." %}

<p class="caption">(a) The courier variant of the corridor toy, with scripted policies: the courier's success rate J with free communication, with communication denied under the no-idle schedule (±1 SE), and the prediction ½ + q/2, against κ<sub>B</sub>; the shaded gap is VoC<sub>gated</sub>, which rises from 0 to 0.498<!-- N:COM-1 -->. (b) CHE at Medium: Δ = (δ = 0) − (δ = 1) for completion (+0.0038) and survival (−0.0143)<!-- N:COM-4 -->, each against its bar, ±2 × the floor sd measured on that card (hatched): a post-hoc floor grading. (c, d) The runs behind (b): four seeds at δ = 0, four at δ = 1<!-- N:COM-4 -->, and the identical floor runs, with their means. The figure carries no word “inert”; (a) is the toy and (b–d) are CHE. It cannot show the content ablations, the High-severity runs, the VOID condition, or anything about a trained encoder. <span class="figure-note">Status: descriptive; (a) toy handshake, scripted policies; (b–d) trained policies at Medium, bars are post-hoc floor grading · Interact: none (static figure).</span></p>

### 7.1 The kernel

**Definition 7 (Communication denial, as implemented).** After the agents move, the comms kernel $T_K(k' \mid x')$ samples a directed link graph over the alive agents: for every ordered pair $i \ne j$ of alive agents,

$$
\Pr\big[\, i \to j \text{ open} \,\big] = \mathbf{1}\big[\lVert x'_i - x'_j \rVert_\infty \le R_{\mathrm{comm}}\big]\,(1 - \delta),
$$

with $R_{\mathrm{comm}} = 16$<!-- N:COM-6 --> cells. Each agent emits a message $m_i \in [-1, 1]^{8}$<!-- N:DX-17 --> at step $t$; at $t + 1$ each receiver $j$ gets the mean of the messages delivered over the links then realized, $\bar m_j = \sum_i k'_{ij}\, m_i \,/\, \max(1, \sum_i k'_{ij})$, which is the zero vector when $j$ is isolated. $T_K$ reads positions and aliveness only, with no hazard, smoke or structure input, so denial is mechanistically independent of the fire; hazard-coupled communication is future work. One uniform per ordered pair is drawn at every step whatever $\delta$ is, so $\delta = 0$ gives the deterministic range graph and $\delta = 1$, the locked value<!-- N:COM-6 -->, gives the empty graph, both bitwise. The theory's range-dependent link probability is implemented as this hard Chebyshev range<!-- N:DX-17 -->.

The message head is a tanh-bounded dense layer on the policy's shared trunk. Listing 6 shows the line that makes the channel non-differentiable.

**Listing 6.** Delivered messages carry no gradient.

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

The delivered aggregate is stored in the training batch and the loss recomputes the policy from the stored array; `stop_gradient` states the same thing in code. No gradient crosses the channel, so the message head receives none for the whole run and stays at its initialization<!-- N:ENV-12 -->: what an agent emits is a frozen random projection of trunk features that are themselves trained. The receivers' weights on the message inputs are trained, so whether agents use messages can be tested; what to say was never learned.

### 7.2 When communication should matter

That observability governs the value of communication is not new. Pynadath & Tambe (2002) <d-cite key="pynadath2002"></d-cite> relate the complexity of team decision problems with communication to observability: free communication lowers the complexity when the world is collectively observable (their Theorem 4 and Table 2), and makes no difference when it is individually observable or not observable at all (their Theorems 5–6). Remark 2′ refines this for collective partial observability, in a two-agent extension of the corridor toy of Theorem 1.

**Remark 2′.** Extend $E_{2C}$ with a second agent. (i) Under a team-any reward, communication has zero marginal value when the agents are interchangeable, expendable (no death cost) and at least as numerous as the hypotheses: coverage then achieves $J = 1$ under total denial. When any qualifier fails, value returns; in general it scales with the deficit of agents relative to hypotheses, and a death cost, such as CHE's $d_p = 0.5$<!-- N:ENV-1 -->, prices the redundancy that substitution spends. (ii) In the courier variant, where only agent 1 can complete the task and it observes the other agent only through messages, the denied optimum within the no-idle policy class is $\tfrac12 + \tfrac12 q(\kappa_B)$; with slack $\ell_f$, optimal denied play buys information by idling at the branch and achieves $\tfrac12 + \tfrac12 \tilde q(\kappa_B)$, where $\tilde q$ is the probability of being informed by the commitment point under the best idling schedule, with $\tilde q \ge q$ (equality iff $\ell_f = 0$), so

$$
\mathrm{VoC}_{\mathrm{true}}(\kappa_B) = \tfrac12\big(1 - \tilde q(\kappa_B)\big) \le \tfrac12\big(1 - q(\kappa_B)\big).
$$

Both $q$ and $\tilde q$ decrease in $\kappa_B$, so the value of communication increases with perception decay. The lesson is conditional: communication carries value when perception fails and redundancy is unavailable. Irreplaceable roles, not blindness alone, make it valuable.

We ran the courier variant (M5.2) with scripted policies, delivering messages through the production link kernel and computing $\tau$ with the shared transmittance function, so the toy also tests both kernels. With 4096 episodes and 8192 Monte Carlo draws per point<!-- N:DX-15 -->, the free arm succeeds with probability 1.0000<!-- N:DX-15 --> at every $\kappa_B$, and the no-idle denied arm matches $\tfrac12 + \tfrac12 q$ (largest $\lvert z \rvert$ 0.44, $\chi^2 = 0.51$ on 8 degrees of freedom<!-- N:DX-15 -->; a fit that good was checked against replicate runs, which showed the standard errors sound, before it was accepted). The value of communication against that arm, $\mathrm{VoC}_{\mathrm{gated}} = \tfrac12(1 - q)$, therefore rises monotonically from 0 to 0.498<!-- N:COM-1 --> (Figure 9(a)). The idling correction bites where $q$ is near 1: $\tilde q / q$ is 1.126 at the locked $\kappa_B = 1.0$, peaks at 1.235 near $\kappa_B = 2$ and returns towards 1 at both ends, and the correction removes 79 %, 54 % and 7 % of $\mathrm{VoC}_{\mathrm{gated}}$ at $\kappa_B$ = 0.5, 1.0 and 3.0<!-- N:DX-15 -->. The toy's courier is irreplaceable by construction; CHE's agents are not.

### 7.3 In CHE the channel carries nothing measurable

CHE's agents meet one of Remark 2′(i)'s qualifiers: they are twelve<!-- N:ENV-6 --> interchangeable agents sharing one set of parameters<!-- N:ENV-11 -->. Their deaths are priced, so they are not strictly expendable, and nothing establishes that they are at least as numerous as the hypotheses. Three measurements test whether they use the channel.

First (M5.3: Medium, $\delta = 0$, $R_{\mathrm{comm}} = 8$, two seeds<!-- N:COM-2 -->, 500 updates<!-- N:DX-305 -->), three arms with identical architecture differ only in message content: live; zeroed, where the delivered aggregate is set to zero but the link graph is kept; and shuffled, where sender identities are permuted within a step. No pair differs beyond a bar of twice the earlier Medium floor, about 3 points<!-- N:COM-2 -->: a post-hoc floor grading, which a true effect equal to the bar would clear only about half the time (§8.2). Second (M5.3b: High, three seeds, $R_{\mathrm{comm}}$ = 8 and 16<!-- N:DX-16 -->), the same arms at two ranges: tripling the mean alive out-degree from 1.01 to 2.99<!-- N:COM-3 --> changed nothing, which rules out "nobody was in range" as the explanation, although at High the wider floor sets the bar at about 11 points<!-- N:DX-16 -->.

Third (M5.5: Medium, four seeds, $R_{\mathrm{comm}} = 16$<!-- N:COM-4 -->, message path live in both arms), the denial element itself. With $\delta = 0$ against $\delta = 1$, completion differs by +0.38 points against a bar of 7.99 points, and survival by −1.43 points against a bar of 2.60 points<!-- N:COM-4 -->; both bars are twice the floor sd measured on the same card, a post-hoc floor grading (Figure 9(b–d)). The channel is therefore inert at the resolution these measurements have, bars of about 8 points on completion and 2.6 points on survival<!-- N:COM-4 -->; a true effect of either size would clear its bar only about half the time (§8.2), and this is not a point null. A third condition, no cross-arm difference in danger-moment outcomes, is VOID, not failed: the threshold chosen at implementation to grade it, 20 % on fire deaths per danger agent-step, sat below that quantity's own 27.2 % run-to-run nondeterminism, and the observed 23.2 %<!-- N:COM-5 --> lies between the two (§8.1).

The null rests on two halves, each weaker alone. The first is a mechanism. In the live arm a receiver can tell that it heard from someone without decoding anything; in the zeroed arm it cannot. That signal needs no encoder, and it went unused at both severities, and at High at both ranges, so the channel's neglect is on the demand side (the agents did not need the information) rather than the channel side (they could not read it), and the frozen encoder cannot account for it. The second half is M5.5: removing the channel entirely changes nothing measurable.

Two qualifications bound the claim. Deaths are priced ($d_p = 0.5$<!-- N:ENV-1 -->), so the agents are not strictly expendable and Remark 2′(i)'s clean-zero conditions are not fully met; the measured null therefore also says that the value which returns when a qualifier fails is weak at this scale and this death price. And the message head receives no gradient, so the encoder is a frozen random projection and gradient-shaped messaging is untested: a bound measured on a frozen encoder does not strictly bound a trained one. We claim only that communication denial is inert under a frozen random-projection encoder at this scale.

Three consequences carry into §9. The composition under test there is, in effect, Coupling A × Coupling B. The held-out configuration $\theta^*$ keeps $\delta = 1.0$<!-- N:COM-6 --> for fidelity to the registration, at no cost. And the third of ISO's training episodes that carry only $\delta$<!-- N:DES-8 --> carry, behaviourally, no active stressor: they are fire-only episodes, the source of the inert-share bias that §9 registers and corrects.
