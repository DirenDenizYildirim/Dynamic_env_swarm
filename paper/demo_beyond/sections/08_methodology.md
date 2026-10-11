<!-- BUILDER-WRITTEN DEMONSTRATION (DEMONSTRATION DRAFT ruling, 2026-10-11); not the owner's text -->

## 8 Methodology: bars come with floors

GPU training is not reproducible run to run: XLA chooses kernels by timing them and some reductions use atomics, so two runs with the same seed, configuration and code can differ. A reproducibility floor is the standard deviation of a metric over such identical runs, the noise any acceptance bar on that metric must clear. This section states the measurement rules the project adopted, each with the defect in its own record that produced it, and ends with where this paper falls short of them (§8.6). Figure 10 steps through the floor exhibits; each tab prints its confound.

<figure class="l-page">
  <iframe src="{{ 'assets/html/submission/floors_explorer.html' | relative_url }}" width="100%" height="460" style="border:none" title="Floors explorer: reproducibility floors per card, per artifact, per run length, and the grid against its floor" loading="lazy"></iframe>
  <figcaption><strong>Figure 10.</strong> Reproducibility floors, one exhibit per tab. <em>Per card (and tree, and config):</em> the Medium floor on two runs, completion 0.0145 against 0.0399 (2.75×) while survival stays at 0.0129 against 0.0130<!-- N:METH-1 -->; card, code tree and configuration all differ between the two runs. <em>Per artifact:</em> GPU rerun comparisons during a refactor, one square per comparison: the reference tree against itself, 0 of 760 field digests differing in 4 of 4 comparisons; the refactored tree against itself, 1 of 4 differing, on two diagnostic channels<!-- N:METH-2 -->; and the cross-tree comparisons. <em>Per run length:</em> completion of identical runs at 500 and 1000 updates, floor growth 2.1× for ISO and 5.2× for JOINT<!-- N:METH-5 -->; run length and box both differ. <em>The grid against its floor:</em> each confirmatory arm's seed standard deviation over its floor (k = 72 per arm<!-- N:DES-13 -->), and survival Γ at 5.40× its floor-basis sd(Γ)<!-- N:HW-1 -->. The figure cannot show each floor's own uncertainty, the contrasts in this paper that have no floor (§8.6), or the drift channels, which have none. <span class="figure-note">Status: floors are point standard deviations over identical runs, roughly ±40 % uncertain when measured on four identical runs<!-- N:DX-303 --> · Interact: click a tab or press ← / →; hover or tab to a mark for its value.</span></figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/floors_explorer.png" class="img-fluid" alt="Reproducibility floors on two cards, rerun comparisons of two code trees, floor growth from the shorter to the longer run length, and the confirmatory grid's seed dispersion against its floor, each with its confound stated." caption="Static companion of Figure 10 for the printed PDF." %}
</div>

### 8.1 A bar without a floor is void

**No acceptance bar without a measured floor for the quantity it grades, or an explicit UNDERPOWERED flag.** A bar below its instrument's noise cannot pass under the null, so it is not a test: its output is void, not failed, and a void test voids a PASS exactly as it voids a FAIL. Four bars in the record produced the rule. M4.4 graded its High survival effect against $\sigma_{\mathrm{seed}} = 0.0295$<!-- N:DX-38 -->, the spread of two seed means, where the High floor measured later is 0.0621<!-- N:CB-7 -->; its "strong" grade was retracted (§6.4). M5.3 graded its content ablation against a Medium floor hard-coded from an earlier run. M5.3b measured its High floor first, on its own card, and found that matching Medium's resolution at High would take roughly 46 seeds per arm<!-- N:DX-302 -->. M5.5's third condition, specified as no cross-arm difference in danger-moment outcomes, was graded with a 20 % threshold chosen at implementation, not registered, on a quantity whose run-to-run nondeterminism measures 27.2 %; the observed 23.2 %<!-- N:COM-5 --> exceeds the threshold and falls short of the noise, so the condition is VOID. The floor data predate the comparison, and had the difference exceeded the floor, the verdict as produced, NOT INERT, would have stood.

**Floors are facts per metric and per hardware.** Re-measuring the Medium floor moved the completion floor 2.75-fold, from 0.0145 to 0.0399, and left survival at 0.0129 against 0.0130<!-- N:METH-1 -->. The two runs differ in card (RTX 5090 against RTX PRO 6000<!-- N:DX-403 -->), code tree and configuration, so the exhibit shows that a floor can move for one metric and not another, not which factor moved it. Neither "it will be the same" nor "it will differ" is safe; the floor is measured on the card that runs the grid.

**Floors are facts per artifact.** In the refactor that made the environment configuration a per-episode traced input (M6.0), the GPU rerun floor was measured first on the reference tree and read zero: 0 of 760 field digests differed, in 4 of 4 comparisons<!-- N:METH-2 -->. Against it, two diagnostic channels that differed between the refactored and the reference tree looked like a semantic change, but the refactored tree differed from itself 1 time in 4, on the same two channels<!-- N:METH-2 -->, and no trajectory field differed in any comparison. The floor had been measured on the more deterministic artifact. An equivalence claim between A and B needs A against A and B against B, not only A against B: two deterministic artifacts cannot compare intermittently.

### 8.2 Contrasts and power

**A contrast is graded on the contrast's standard error.** For $\Gamma = \overline{\mathrm{JOINT}} - \overline{\mathrm{ISO}}$ over $k$ seeds per arm,

$$
\operatorname{sd}(\Gamma) = \sqrt{\frac{\sigma_{\mathrm{ISO}}^2 + \sigma_{\mathrm{JOINT}}^2}{k}},
$$

never either arm's own $\sigma\sqrt{2/k}$. The per-arm forms bracket the truth without equalling it: at $k = 34$<!-- N:METH-3 --> on the M6.2b floors, ISO's form gave 92.1 % power and JOINT's 62.8 %, where the contrast's power was 76.7 %<!-- N:METH-3 -->. The project had adopted per-artifact floors because the arms differ in stability, then kept a power formula that assumed they do not.

**A design-stage power statement is the 80 %-power minimum detectable effect at the family-corrected level**<!-- N:METH-7 -->,

$$
\mathrm{MDE}_{80} = \big(z_\alpha + z_{0.8}\big)\,\operatorname{sd}(\Gamma),
$$

with $z_\alpha$ the family-corrected critical value (Šidák over the two co-primaries, $z_\alpha = 2.2365$<!-- N:DES-13 -->); with equal variances, $\operatorname{sd}(\Gamma) = \sigma\sqrt{2/k}$. The exclusion bound $X$ that §9 attaches to a null has the same form, on the grid's realized seed dispersion. A bare $2\sigma\sqrt{2/k}$ is the effect at which a test would just reject, 50 % power. Phase-6 seeds were first ruled at $k = 20$<!-- N:METH-4 --> on such a figure, which also omitted the Šidák correction; corrected, completion had 55.6 % power against its own motivating effect band<!-- N:METH-4 -->, caught while the registration was drafted, before any run. The 2σ form survives only for post-hoc floor grading of an observed effect, labelled as such, as in Figure 9(b).

### 8.3 Floors move with the run, and gates must not divide by them

**Floors grow with run length.** From 500 to 1000 updates the completion floor grew from 0.0165 to 0.0339 for ISO and from 0.0093 to 0.0483 for JOINT<!-- N:DX-34 -->, 2.1-fold and 5.2-fold<!-- N:METH-5 -->; the two lengths ran on different RTX PRO 6000 boxes, so length is confounded with box. The ordering inverted, JOINT being the tighter arm at 500 updates and the looser at 1000, and the ruling that ordered the measurement had said not to presume its outcome. A floor measured at one budget does not grade runs at another. That the growth follows each arm's curriculum difficulty is a hypothesis we did not test (two arms).

**A gate that divides by a floor diverges on better hardware.** The registered plateau guard divided the drift over the last 100 updates<!-- N:DES-10 --> by the floor sd. On a second card JOINT's residual drift fell while its floor shrank by more, and the guard fired; as the floor goes to zero any nonzero drift fails, so on a perfect instrument nothing passes. The $T^*$ ruling of 2026-08-11<!-- N:METH-6 --> retired the guard as a pass/fail gate, kept it as a reported statistic, fixed the estimand as Γ at matched compute, and made Γ(t) required robustness evidence (§9): it narrowed the claim and added a test the result could fail.

### 8.4 The floor is a hurdle, not the test variance

**The floor and the test statistic are different variances.** A floor comes from identical runs at one seed; a $k$-seed arm mean varies by seed and by nondeterminism. The confirmatory contrast is therefore graded on the grid's own seed dispersion, and the floor serves a separate hurdle: does the effect beat reproducibility? On the confirmatory grid each arm's seed standard deviation is 1.12 and 1.09 times its floor for completion and 1.25 and 1.19 times for survival (ISO, JOINT)<!-- N:HW-1 -->; survival Γ is 5.40 times<!-- N:HW-1 --> its floor-basis sd(Γ) of 0.00177<!-- N:DX-21 -->, and completion Γ is 1.78 times its 0.00970 in magnitude<!-- N:DX-21 -->. Used for design-stage power, the floor gives an upper bound on the power the grid will have, labelled as one.

### 8.5 Instruments state what they are blind to

**A differenced test sees asymmetry and nothing else.** A condition of the form "no cross-arm difference in X" cancels any X present in both arms. In 24 of 24 rendered episodes of the Coupling-B grid the alive agents drifted towards a wall, their centroid moving down from row 32.3 to 49.2 against an arena centre of 31.5, in a direction set by the training run<!-- N:DX-32 -->; these are rendered-pixel centroids, a diagnostic and not a state measurement. The inertness falsifier for Coupling B, logged before its data, included the condition "no cross-arm exposure/positioning difference", which passed with the drift present in both arms. It could never have seen the drift, and nothing said so for several phases. The verdict it fed does not move, but its silence was evidence about asymmetry only.

**Measuring is not grading.** A channel in the environment's info, the evaluation archive or the training log is recorded; it becomes evidence only inside a registered analysis family, with a floor measured on its artifact. The Phase-6 grid records drift channels for every run at no cost. They are recorded, not graded: no floor exists for them, and they were kept out of the registered family, because a diagnostic added after registration enlarges the family and inflates its correction.

**Every reading of a registered bias is reported.** Bias (b), differential drift, was estimated before unblinding, in three floor studies, as the JOINT − ISO completion drift over the last 100 updates: +0.01209 on the launch batch and +0.0179 on a later re-floor, both on RTX PRO 6000 cards, and −0.0083 on the RTX 5090 that ran the grid<!-- N:DES-10 -->. Its sign reversed on the grid card; we report every reading and claim no direction (§9.1).

### 8.6 Where this paper falls short of its own rules

Not every number in this paper is graded against a floor on its own artifact. Coupling B's Medium survival effect, −0.03 points<!-- N:CB-9 -->, was judged against a three-seed spread, $\sigma_{\mathrm{seed}} = 0.0072$<!-- N:CB-9 -->, not a floor. The trained-policy contrasts of §5 and §6 come from the m44 and m35 grids, which have no identical-run sets; their spreads are seed ranges, and every floor beside them is a reference scale (cross-artifact). In §9.2's secondary design, floors exist only for the sweep's $p = 0.5$<!-- N:DX-28 --> arm; the intermediate points assume that floor and the identification arm is ungraded<!-- N:DX-306 -->. ISO-4 has no identical-run set, so Γ₄ and $\hat B$ (§9.1) are graded on seed dispersion with no beat-reproducibility hurdle, and ISO-4's High-readout numbers carry an UNDERPOWERED flag for that hurdle. The drift channels have no floor at all. And every floor is itself a point estimate: measured on four identical runs, an sd is uncertain by roughly ±40 %<!-- N:DX-303 -->.
