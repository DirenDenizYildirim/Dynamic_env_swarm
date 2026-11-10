<!-- PAPER V3 DRAFT (PAPER V3 ruling, 2026-10-12): builder-drafted, not owner-approved -->

## 4 What each stressor does

### 4.1 Severity, placed by a measured threshold

**Definition 4 (Severity regimes).** For an arena of side $L$, let $\xi(\beta)$ be the typical extent of a fire cluster.

- *Low*, subcritical, $\xi(\beta) \ll L$: fires stay local.
- *Medium*, near-critical, $\xi(\beta) \sim L$: one ignition can cascade to the scale of the arena.
- *High*, supercritical: the fire front moves about as fast as the agents.

Operationally, each level is defined by an observable band, fixed before the main experiment and given in the table below. The calibration ran the fire alone on all-fuel grids (Figure 3), measuring the spanning probability: the chance that one centre ignition reaches the boundary. Three estimators shipped with the calibration data place the critical point between 0.480 and 0.513<!-- N:DX-204 -->, with consensus mean 0.499<!-- N:DX-204 -->; the value fixed for the experiment, 0.500 ± 0.005<!-- N:CAL-1 -->, comes from logistic fits that no committed estimator reproduces. <!-- SETTLED:v2D2 (2026-10-19, log OWNER QUESTIONS SETTLED: the default stands) (carried v2 question D2: Corollary 1(4) stated at the Garet and Marchand level; DISPOSITIONS §5 gives it no V3Q number) -->On the infinite square lattice, the idealized kernel's critical point is exactly ½ (Kesten, 1980)<d-cite key="kesten1980"></d-cite>, and above it a fire that spreads indefinitely burns a region growing linearly towards a deterministic convex shape (Garet & Marchand, 2004<d-cite key="garet2004chemical"></d-cite>; Corollary 1, Appendix A). The agreement checks the implementation and says nothing new about fire.

| severity | $\beta$ | phase | spanning probability ($L = 64$<!-- N:DX-7 -->) | burnt fraction | band it was fixed to |
|---|---|---|---|---|---|
| Low | 0.43<!-- N:CAL-3 --> | subcritical | 0.021<!-- N:CAL-3 --> | 1.9 %<!-- N:CAL-3 --> | spanning below 0.05, burnt 1–5 %<!-- N:DX-201 --> |
| Medium | 0.49<!-- N:CAL-3 --> | near-critical | 0.547<!-- N:CAL-3 --> | 19.8 %<!-- N:CAL-3 --> | spanning 0.3–0.7<!-- N:DX-201 --> |
| High | 0.70<!-- N:CAL-3 --> | supercritical | 0.998<!-- N:CAL-3 --> | 98.3 %<!-- N:CAL-3 --> | front speed 0.5–1.0 cells per step<!-- N:DX-201 -->, measured 0.83<!-- N:DX-6 --> |

Medium, the test severity of §6, lies between the 64<!-- N:DX-7 -->-cell arena's pseudo-critical point, about 0.486<!-- N:CAL-4 -->, and the fixed critical point. Definition 4 also expected outcomes to vary most at Medium. Re-tested with fixed fire-only policies, that expectation is refuted for survival, whose per-episode variance rises with severity (0.00091, 0.00709, 0.00885<!-- N:CAL-5 -->).

<!-- FIGURE 3: block carried from paper/v2/sections/04_severity.md:24 (markup, iframe height and alt text as v2 had them); caption replaced; alt text edited (W3): "illustrative" dropped from the alt so that the caption holds the one allowed short form (C39) -->

<figure class="l-page">
  <iframe src="{{ 'assets/html/submission/severity_explorer.html' | relative_url }}" width="100%" height="528" style="border:none" title="Severity explorer: spanning probability against ignition probability, and one fire at each locked level" loading="lazy"></iframe>
  <figcaption><strong>Figure 3.</strong> Severity as a measured phase. Left: the spanning probability against β for sides 32, 48 and 64<!-- N:DX-7 -->; rules mark the three severities, a triangle the 64-cell arena's pseudo-critical point. Right: one illustrative random-policy episode per severity, with κ<sub>A</sub> 0.06<!-- N:CA-1 -->, κ<sub>B</sub> 1.0<!-- N:CB-1 --> and δ 0<!-- N:DX-202 -->. <span class="interact">Drag the time slider; click a panel.</span></figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/severity_explorer.png" class="img-fluid" alt="Spanning probability of a centre ignition against ignition probability for three grid sizes, with the three locked severities marked, beside one random-policy fire episode at each severity." caption="Static companion of Figure 3 for the printed PDF." %}
</div>

### 4.2 Coupling A

In the runs of the Coupling-B calibration grid with Coupling B on (500-update<!-- N:DX-40 --> policies at each severity), collapse-seeded ignitions per episode fall from 4.05 at Low and 3.41 at Medium to 0.84 at High<!-- N:CA-4 -->. This 4.83-fold<!-- N:CA-4 --> fall (from unrounded counts) is fuel exhaustion (a seed lights only unburnt fuel), first seen under random policies at about 5.7-fold<!-- N:DX-9 -->. The Coupling-A calibration grid (other policies, Coupling A off and on) replicates it at 4.92-fold<!-- N:CA-5 -->. In all nine<!-- N:CA-6 --> measured cells, the share of seeded ignitions inside an alive agent's crop stays between 0.164 and 0.203<!-- N:CA-6 --> (Figure 4). Where Coupling A costs survival most is not located: its grid's survival contrasts rest on two seeds per arm<!-- N:CA-7 -->, with no reproducibility floor (§5).

<!-- FIGURE 4: block carried from paper/v2/sections/05_coupling_a.md:23 (markup, iframe height and alt text as v2 had them); caption replaced; alt text edited (W3): "handshake" (banned term) removed -->

<figure class="l-page">
  <iframe src="{{ 'assets/html/submission/coupling_a_explorer.html' | relative_url }}" width="100%" height="736" style="border:none" title="Coupling A explorer: collapse-seeded ignitions by severity, their share near agents, and the two Proposition 3 runs" loading="lazy"></iframe>
  <figcaption><strong>Figure 4.</strong> Coupling A. Top: collapse-seeded ignitions and their share near agents, by severity, in the Coupling-B grid (labelled “m44” on the figure) and the Coupling-A grid (labelled “m35” on the figure). Bottom: the two checks of Proposition 3, the second labelled “handshake” on the figure. <span class="interact">Hover a point; table view.</span></figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/coupling_a_explorer.png" class="img-fluid" alt="Collapse-seeded ignitions per episode at three severities for two trained grids, the share of them near agents, and the two Proposition 3 runs shown separately." caption="Static companion of Figure 4 for the printed PDF." %}
</div>

### 4.3 Coupling B

In the Coupling-B grid with masking on, smoke masks 0.068 %, 0.249 % and 1.559 %<!-- N:DX-11 --> of crop cells over all alive agent-steps at Low, Medium and High, and 118, 22 and 16 times<!-- N:CB-10 --> that share at moments of danger, when a burning cell is in the crop (Figure C2(a), Appendix C). At High, survival is lower with masking on than off in 3 of 3<!-- N:CB-5 --> replicate contrasts: −6.87, −10.66 and −4.70 points<!-- N:DX-13 -->. Each rests on one run per arm, two share a seed, and none has an interval, so this cost is descriptive and ungraded. The band in Figure C2(b), a High survival floor of 6.21 points<!-- N:CB-7 --> from another artifact, is a reference scale (cross-artifact): a spread from other runs, shown for scale only.

At Medium, the test severity, Coupling B's own survival effect was −0.03 points<!-- N:CB-9 -->, judged within noise against a three-seed<!-- N:CB-9 --> spread of 0.72 points<!-- N:CB-9 --> rather than a measured floor.

### 4.4 Communication denial

In a denial study at Medium (four<!-- N:COM-4 --> seeds), opening the links (δ = 0 against δ = 1) changed completion by +0.38 points and survival by −1.43 points<!-- N:COM-4 -->. The acceptance thresholds, 7.99 and 2.60 points<!-- N:COM-4 -->, were twice<!-- N:V4-2 --> the reproducibility floor on that study's GPU (§5), and an effect as large as a threshold would clear it only about half<!-- N:V4-1 --> the time. The survival threshold is 2.7<!-- NOT-IN-LEDGER (owner ruling 2026-11-03: the ledger is not updated; the provenance row cites the source; blind review W4a): 2.60 / 0.96 = 2.71, from COM-4 and RES-2 --> times the survival gap of §6.3, so the study would only rarely have detected a denial effect of that gap's size. Its falsifier first returned "NOT INERT" on a condition about fire deaths at moments of danger, later voided because its threshold lay below that quantity's rerun noise (Appendix C). <!-- SETTLED:V3Q14 (2026-10-19, log OWNER QUESTIONS SETTLED: the default stands) -->We call communication denial "inert under a frozen random-projection encoder at this scale" in this sense only: no effect as large as those thresholds was detected. Inertness is a property of this agent, whose message head is never trained (Appendix B), not of the environment; with learned communication <d-cite key="foerster2016dial,sukhbaatar2016commnet"></d-cite>, denial may matter.

The label thus rests on coarse thresholds, and the design applied it asymmetrically across the stressors. Every stressor counted as behaviourally active unless calibration had found it inert, so Coupling A at High (§4.2) and Coupling B at Low and Medium (§4.3) count as active although each is weak there; only δ counts as inert. The composition the worked example tests is therefore, in effect, Coupling A with Coupling B (§6.2). <!-- SETTLED:V3Q4 (2026-10-19, log OWNER QUESTIONS SETTLED: the default stands) -->Remark 2′ (Appendix A) relates to Pynadath & Tambe<d-cite key="pynadath2002"></d-cite>, who show that free communication lowers the complexity of team decision problems when the world is collectively observable. In a two-agent toy, Remark 2′ shows that communication has no marginal value when the agents are interchangeable, expendable and at least as numerous as the hypotheses, and regains value when any of these fails.
