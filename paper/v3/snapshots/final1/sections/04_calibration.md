<!-- PAPER V3 DRAFT (PAPER V3 ruling, 2026-10-12): builder-drafted, not owner-approved -->

## 4 What each stressor does

<!-- STUB-SPEC
JOB: Say what each stressor does, at which severity, and how finely that was measured (V3-F1). 4.1 severity placed by a measured percolation threshold; 4.2 Coupling A; 4.3 Coupling B, including its Medium measurement (the siting evidence); 4.4 communication denial, the ruled inert phrase with its bars, and the asymmetry of the label.
WRITER: W3.
BUDGET: 700 prose words; Figures 3 to 5 captions at most 60 words each.
FROM: P1 §4.2 §4 and §1.1 (P-S, P-A′, P-B, P-B′, P-K); P3 §1.1 (E1, E2, E4, E10) and §1.4; P2 §3 #3 to #5.
ORDER:
  - 4.1 Def. 4 as a short list (operational definition by locked bands); lead with the committed estimators and their spread and consensus (DX-204), then the locked threshold value with its provenance caveat (CAL-1, no committed estimator; HOME); the three levels (CAL-3) and β_c(64) (CAL-4); Cor. 1 in words at v2's verified level (v2 D2 default; kesten1980, garet2004chemical); Def. 4's Medium-variance prediction refuted for survival (CAL-5, DX-8; HOME); Figure 3 (its renders are illustrative).
  - 4.2 Coupling A under trained 500-update calibration policies (DX-40): collapse-seeded ignitions fall 4.83-fold Low to High, replicated 4.92-fold (CA-4, CA-5): fuel exhaustion, first seen under random policies (DX-9; HOME of the 4.8-fold fall); the near-agent share stays flat (CA-6); the survival effect of A is not located (CA-7: 2 seeds, no floor; say so once); Figure 4.
  - 4.3 Coupling B: masking concentrates at moments of danger (CB-10, DX-11); at High, smoke's survival cost is in the same direction in 3 of 3 contrasts, descriptive and ungraded (CB-5, DX-13, CB-7; HOME); at Medium, the test's severity, its own survival effect was −0.03 points, not measurable against a three-seed spread, not a measured floor (CB-9; HOME of the measurement); Low masks 0.068 % of crop cells (DX-11). Figure 5 (gloss its printed codes; its band is a reference scale (cross-artifact), FIGURE BATCH B9).
  - 4.4 Communication denial: no effect detected at bars of 7.99 completion and 2.60 survival points from 4 seeds, about half power (COM-4, V4-1, V4-2); the content and connectivity checks (COM-2, COM-3, DX-16); hence "inert under a frozen random-projection encoder at this scale" (ruled phrase, HOME, with the bars beside it; V3Q14); then the asymmetry (HOME): the record's working definition of behaviourally active is "not found inert in calibration", which counts Coupling A at High (CA-4) and Coupling B at Low (DX-11) and Medium (CB-9) as active although each is weak there; only δ is counted inert. Invent no threshold. Remark 2′ in one sentence as a refinement of Pynadath & Tambe (READS RULING item 4; pynadath2002; statement in Appendix A; V3Q4).
ROWS: CAL-1 to CAL-5, DX-6, DX-7, DX-8, DX-201, DX-202, DX-204, CA-1, CA-4 to CA-7, DX-9, DX-40, CB-1, CB-5, CB-7, CB-9, CB-10, DX-11, DX-13, COM-2 to COM-5, DX-16, V4-1, V4-2, V4-3, ENV-6.
CITATIONS: kesten1980, garet2004chemical (Cor. 1(4) at the verified level only; v2 D2), pynadath2002 (Remark 2′ as READS RULING item 4 permits).
FIGURES: Figure 3 severity_explorer (4.1; gloss: the printed companion subtitle is clipped in print, so state the renders' κ_A 0.06, κ_B 1.0, δ 0 in the caption); Figure 4 coupling_a_explorer (4.2; gloss labelled “m44” and “m35”; its carried alt text says handshake, a banned term: reword the alt text); Figure 5 static fig04_coupling_b.png (4.3; gloss labelled “M4.4”; its legend's "floor" is a reference scale (cross-artifact)). Blocks below.
REGISTERED STRINGS: "inert under a frozen random-projection encoder at this scale" (here, in full); "reference scale (cross-artifact)"; "illustrative" for the severity renders; VOID for comms condition (iii) only if mentioned (home Appendix C).
CAVEATS HOMED HERE (state each in full, once; the detection pattern, from checks/caveats.yaml, must match your home sentence):
  C02 delta_inert_ruled_phrase: Communication denial is "inert under a frozen random-projection encoder at this scale", with the bars it rests on. Pattern: (?i)frozen random-projection
  C03 delta_label_asymmetric: The inert label rests on coarse bars and is applied asymmetrically (Coupling A at High and Coupling B at Low counted active although weak there). Pattern: (?i)\basymmetric
  C31 severity_estimator_provenance: The locked threshold value has no committed estimator; the committed estimators' spread and consensus are stated beside it. Pattern: (?i)\bcommitted estimator
  C32 fuel_limited_fall: Collapse-seeded ignitions fall about 4.8-fold from Low to High under trained (500-update calibration) policies; fuel exhaustion, first seen under random policies. Pattern: 4\.8\d?\s*×
  C33 smoke_high_descriptive: Smoke's survival cost at High - same direction in 3 of 3 contrasts; descriptive, ungraded. Pattern: \b3 of 3\b
  C34 coupling_b_medium_measurement: Coupling B's own survival effect at Medium (the test's severity) was not measurable against a three-seed spread - not a measured floor. Pattern: (?i)\bthree-seed\b
  C35 medium_variance_prediction_refuted: Def. 4's prediction that outcomes vary most at Medium is refuted for survival. Pattern: (?i)\brefuted\b
SHORT FORMS ALLOWED HERE (at most one sentence each; the full statement is at the home):
  C39 hero_illustrative (home 00_hero.md)
EVERY OTHER CAVEAT in checks/caveats.yaml: pointer only ("§6.3", "Appendix D"), never restated. C26: any sentence about the interaction check carries "post hoc".
OWNER-PENDING:
  - Remark 2′ sentence (V3Q4).
  - Cor. 1(4) (v2 D2: default stated at the Garet and Marchand level).
NOT HERE: "certified"; "as predicted before measurement"; "self-limiting" without "fuel exhaustion"; the smoke cost at High as a finding; the Low κ_B contrast (no row); "a sixth to a quarter" (contradicted by its own table); "every acceptance bar"; any m44 or m35 contrast graded against a floor; Γ, the test or its arms (those are §6); "live" (banned: say "active").
V2 MATERIAL: paper/v2/sections/04_severity.md, 05_coupling_a.md (§5.2, §5.3), 06_coupling_b.md (§6.3, §6.4), 07_comms.md (§7.2, §7.3).
DEPENDENCIES: §1 points here for the inert label and its asymmetry; §6.1 points here for the Medium measurement (one sentence allowed there); Appendix C holds the floors behind the bars; Appendix E holds the comms figure.
-->

### 4.1 Severity, placed by a measured threshold

**Definition 4 (Severity regimes).** For an arena of side $L$, let $\xi(\beta)$ be the typical extent of a fire cluster.

- *Low*, subcritical, $\xi(\beta) \ll L$: fires stay local.
- *Medium*, near-critical, $\xi(\beta) \sim L$: one ignition can cascade to the scale of the arena.
- *High*, supercritical: the fire front moves about as fast as the agents.

Operationally, each level is the observable band fixed for it before the main experiment (table). The calibration ran the fire alone on all-fuel grids (Figure 3), measuring the spanning probability: the chance that one centre ignition reaches the boundary. Three estimators shipped with the calibration data place the critical point between 0.480 and 0.513<!-- N:DX-204 -->, with consensus mean 0.499<!-- N:DX-204 -->; the value fixed for the experiment, 0.500 ± 0.005<!-- N:CAL-1 -->, comes from logistic fits that no committed estimator reproduces. <!-- OWNER-PENDING:v2D2 (carried v2 question D2: Corollary 1(4) stated at the Garet and Marchand level; DISPOSITIONS §5 gives it no V3Q number) -->On the infinite square lattice, the idealized kernel's critical point is exactly ½ (Kesten, 1980)<d-cite key="kesten1980"></d-cite>, and above it a fire that spreads indefinitely burns a region growing linearly towards a deterministic convex shape (Garet & Marchand, 2004<d-cite key="garet2004chemical"></d-cite>; Corollary 1, Appendix A). The agreement checks the implementation and says nothing new about fire.

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

In the Coupling-B grid with masking on, smoke masks 0.068 %, 0.249 % and 1.559 %<!-- N:DX-11 --> of crop cells over all alive agent-steps at Low, Medium and High, and 118, 22 and 16 times<!-- N:CB-10 --> that share at moments of danger, when a burning cell is in the crop (Figure 5(a)). At High, survival is lower with masking on than off in 3 of 3<!-- N:CB-5 --> replicate contrasts: −6.87, −10.66 and −4.70 points<!-- N:DX-13 -->. Each rests on one run per arm, two share a seed, and none has an interval, so this cost is descriptive and ungraded. The band in Figure 5(b), a High survival floor of 6.21 points<!-- N:CB-7 --> from another artifact, is a reference scale (cross-artifact): a spread from other runs, shown for scale only.

At Medium, the test severity, Coupling B's own survival effect was −0.03 points<!-- N:CB-9 -->, judged within noise against a three-seed<!-- N:CB-9 --> spread of 0.72 points<!-- N:CB-9 --> rather than a measured floor.

<!-- FIGURE 5: block carried from paper/v2/sections/06_coupling_b.md:74 (include and alt text as v2 had them); caption replaced -->

{% include figure.html path="assets/img/submission/fig04_coupling_b.png" class="img-fluid" alt="Left, the masked share of the agent crop at three severities, over all alive agent-steps and at danger moments, on a log scale. Right, three replicate survival contrasts at high severity and then the first estimate, against a hatched band one standard deviation wide on a reference scale measured on another artifact." caption="Figure 5. Coupling B: where the masking falls, and the High survival contrasts." %}

<p class="caption">(a) Masked share of the crop by severity, over all alive agent-steps and at moments of danger, in the Coupling-B grid (labelled “M4.4” on the figure). (b) The three High survival contrasts, then the first two<!-- N:DX-40 -->-seed estimate; the hatched band, labelled floor, is a reference scale (cross-artifact).</p>

### 4.4 Communication denial

In a denial study at Medium (four<!-- N:COM-4 --> seeds), opening the links (δ = 0 against δ = 1) changed completion by +0.38 points and survival by −1.43 points<!-- N:COM-4 -->. The acceptance thresholds, 7.99 and 2.60 points<!-- N:COM-4 -->, were twice<!-- N:V4-2 --> the reproducibility floor on that study's GPU (§5), and an effect as large as a threshold would clear it only about half<!-- N:V4-1 --> the time. <!-- OWNER-PENDING:V3Q14 -->We call communication denial "inert under a frozen random-projection encoder at this scale" in this sense only: no effect as large as those thresholds was detected.

The label thus rests on coarse thresholds, and the design applied it asymmetrically across the stressors. Every stressor counted as behaviourally active unless calibration had found it inert, so Coupling A at High (§4.2) and Coupling B at Low and Medium (§4.3) count as active although each is weak there; only δ counts as inert. The composition the worked example tests is therefore, in effect, Coupling A with Coupling B (§6.2). <!-- OWNER-PENDING:V3Q4 -->Remark 2′ (Appendix A) refines Pynadath & Tambe<d-cite key="pynadath2002"></d-cite>, who show that free communication lowers the complexity of team decision problems when the world is collectively observable. In a two-agent toy, it finds that communication has no marginal value when the agents are interchangeable, expendable and at least as numerous as the hypotheses, and regains value when any of these fails.
