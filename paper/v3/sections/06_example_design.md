<!-- PAPER V3 DRAFT (PAPER V3 ruling, 2026-10-12): builder-drafted, not owner-approved -->

## 6 Worked example: training on stressors together or apart

### 6.1 What was registered, and what changed

Before the main training runs, we pre-registered the test, its outcomes, a framing for each, and a falsifier.

<!-- SETTLED:wording (2026-10-19, log OWNER QUESTIONS SETTLED: the default stands) of the framing-change disclosure (V3-F5 is ruled; the words are the owner's to approve) -->
After the result was known, the paper's emphasis moved from the test to the environment. The registered framings remain the record of the original plan (Appendix D).

The test was sited where composition is weak. At the test severity, Coupling B's survival effect in calibration was within a three-seed<!-- N:CB-9 --> spread, not a measured floor (§4.3), and communication denial had no detectable effect (§4.4), so the test point may have offered little composition. The registration stated the Coupling-B part of this limitation in advance, for every outcome: that both couplings meet their fixed-value criteria at Medium "is not the same as both producing behavioural effects there".

### 6.2 Design

The isolated arm (ISO) trains on configurations with one stressor on at a time and the joint arm (JOINT) with every stressor on, both at β = 0.43<!-- N:CAL-3 --> and 0.70<!-- N:CAL-3 --> with one shared-parameter IPPO policy per seed<!-- N:ENV-11 --> <d-cite key="dewitt2020ippo"></d-cite>. Both are evaluated at θ\*, the held-out test configuration: every stressor on at β = 0.49<!-- N:CAL-3 -->. Architecture, hyperparameters, evaluation draw and compute (1000<!-- N:DES-13 --> updates) are matched: Γ is read at matched compute, with no claim about convergence: whether training had plateaued by then is not assessed. The gap Γ, JOINT's mean minus ISO's at θ\*, is tested on two co-primaries, completion and survival, Šidák-corrected for m = 2<!-- N:DES-13 -->: the confirmatory family. We ran 72<!-- N:DES-3 --> seeds per arm, above the registered cap of 60<!-- N:DES-1 -->, a recorded deviation made before unblinding. Every interval is conditional on the one registered evaluation draw.

Let $\mu_A$ and $\mu_B$ be the per-coupling frequencies, the shares of episodes with each coupling on, and $p$ the co-occurrence, the share with both. The active share is the share with at least one behaviourally active stressor; the fire-only share $\nu$ is the rest. Fire-only episodes still carry structural collapse, a lethal hazard: <!-- NOT-IN-LEDGER (owner ruling 2026-11-03: the ledger is not updated; the provenance row cites the source; blind review W10): collapse deaths 19.6 % (ISO), 22.4 % (JOINT), 24.5 % (ISO-4) of deaths at θ*, read by the builder from the grid's θ* evals (review/blind_review_checks.md §1) -->at θ\*, collapse causes a fifth to a quarter of all deaths. JOINT sees each coupling three times as often as ISO<!-- N:DES-7 -->, so Γ mixes frequency with co-occurrence. With communication denial inert (§4.4), the active share equals $\mu_A + \mu_B - p$<!-- N:X4-1 -->: 2/3 for ISO and 1 for JOINT<!-- N:X4-1 --><!-- N:DES-14 --> (Figure 5). No contrast in this design moves co-occurrence alone.

<!-- SETTLED:A1(ii) (2026-10-19, log OWNER QUESTIONS SETTLED: the default stands) attribution of the review that found the bias (default "a review of the registered design") -->
One design error is expected to inflate Γ. Communication denial had been found inert and so was left out of the secondary sweeps, yet ISO kept two δ-only components of six<!-- N:DES-16 -->: a third<!-- N:DES-8 --> of ISO's training episodes are fire-only, and the design did not count them. A review of the registered design found the bias before the main runs; it was registered, with its expected direction and a correcting arm, during the main runs and before unblinding<!-- N:DES-15 -->. That arm, ISO-4, is ISO without its δ-only components (active share 1<!-- N:X4-1 --><!-- N:DES-14 -->), a sensitivity arm outside the confirmatory family with 20<!-- N:DES-15 --> seeds. Γ₄ = JOINT − ISO-4 is the corrected gap; B̂ = ISO-4 − ISO.

ISO's single-coupling components and all of ISO-4 train with links intact (δ = 0<!-- N:X4-2 -->), while JOINT trains and θ\* tests at δ = 1<!-- N:X4-2 -->. This train/test mismatch is harmless only if δ is inert; this study does not test what opening the links does to the trained policies at θ\*.

<!-- SETTLED:V3Q21 (2026-10-19, log OWNER QUESTIONS SETTLED: the default stands) bias (b) label kept (default); V3Q22 registered antecedent not mentioned in the main text (default) -->
Another registered caveat, which the registration labels bias (b), concerns differential completion drift in the last 100 updates<!-- N:DES-10 -->; it reverses sign on the grid GPU (the main runs' GPU), so no direction is claimed (Appendix D).

<!-- FIGURE 5: block carried from paper/v2/sections/01_introduction.md:29 (markup, iframe height and alt text as v2 had them); caption replaced; the writer checks the alt text -->

<figure class="l-page">
  <iframe src="{{ 'assets/html/submission/composer_training_mixtures.html' | relative_url }}" width="100%" height="442" style="border:none" title="Training mixtures of ISO, ISO-4 and JOINT by episode type" loading="lazy"></iframe>
  <figcaption><strong>Figure 5.</strong> Each bar splits one arm's training mixture into episode types: Coupling A only, Coupling B only, both together, and fire-only. Beneath each bar are each coupling's frequency (labelled “per-stressor marginal” on the figure) and the active share. <span class="interact">Count δ-only episodes as inert or nominally; split by β.</span></figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/composer_training_mixtures.png" class="img-fluid" alt="Stacked bars of the three training mixtures by episode type, with each arm's per-coupling frequencies and the share of episodes that carry an active stressor." caption="Static companion of Figure 5 for the printed PDF." %}
</div>
