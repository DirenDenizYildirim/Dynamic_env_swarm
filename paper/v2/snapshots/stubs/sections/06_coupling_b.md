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

<!-- FIGURE BLOCK carried from demo (sections/06_coupling_b.md:75-77); writer checks caption against the caption rules in this stub and keeps the block self-contained -->

{% include figure.html path="assets/img/submission/fig04_coupling_b.png" class="img-fluid" alt="Left, the masked share of the agent crop at three severities, over all alive agent-steps and at danger moments, on a log scale. Right, three replicate survival contrasts at high severity and then the first estimate, against a hatched band of one floor standard deviation." caption="Figure 7. Coupling B: where the masking falls, and the High survival contrasts." %}

<p class="caption">(a) For each severity, the masked share of an agent's crop in the κ<sub>B</sub> = 1.0 arm of the Coupling-B grid, over all alive agent-steps (open) and at danger moments, when a Burning cell is in the crop (filled), on a log scale, with the concentration ratios 118×, 22× and 16×<!-- N:CB-10 -->. (b) High survival, κ<sub>B</sub> 1.0 − 0: the three replicate contrasts first (the grid's seeds 0 and 1, then the same-seed retrain: −0.0687, −0.1066, −0.0470<!-- N:DX-13 -->), then, below the rule, the first estimate, the mean of seeds 0 and 1 (−0.0876<!-- N:CB-6 -->). The hatched band is ±1 sd of the High survival floor, 0.0621<!-- N:CB-7 -->, measured on four identical runs<!-- N:DX-40 --> of a separate artifact: a reference for this grid, not its own floor, and a two-run contrast's own floor would be wider. The figure cannot show intervals (each contrast is one run per cell), completion (unresolved), or Medium. <span class="figure-note">Status: reference scale (cross-artifact) for the band; trained policies, 500 updates<!-- N:DX-40 --> · Interact: none (static figure).</span></p>

<!-- FIGURE BLOCK carried from demo (sections/06_coupling_b.md:91-93); writer checks caption against the caption rules in this stub and keeps the block self-contained -->

{% include figure.html path="assets/img/submission/fig05_coactive.png" class="img-fluid" alt="Three bar charts, one per severity, of the share of episodes with zero, one, two, three, and four or more co-active events." caption="Figure 8. The co-active counter is rare and bursty: its distribution, not its mean." %}

<p class="caption">Share of episodes with 0, 1, 2, 3 and ≥ 4 co-active events, one panel per severity (β = 0.43 / 0.49 / 0.70<!-- N:CAL-3 -->), in the κ<sub>B</sub> = 1.0 arm of the Coupling-B grid, seeds pooled: P(0) = 0.563 / 0.578 / 0.883 over n = 1024 / 1536 / 1024 episodes<!-- N:CO-2 -->. The counter counts collapse-seeded ignitions inside an alive agent's crop; κ<sub>B</sub> does not enter it, so it is co-active only where Coupling B is also on, as in these all-on cells. The figure cannot show a floor (none exists for this artifact's counter), the over-dispersion, or training mixtures, in which the counter reads Coupling A alone. <span class="figure-note">Status: descriptive; trained policies, 500 updates<!-- N:DX-40 -->, single-configuration runs; no floor · Interact: none (static figure).</span></p>

<!-- LISTINGS carried verbatim from the committed files: place each where your prose introduces it, keep its LISTING line directly above its fence, never edit the code -->

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
