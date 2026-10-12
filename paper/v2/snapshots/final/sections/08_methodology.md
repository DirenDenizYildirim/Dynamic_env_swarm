<!-- PAPER V2 DRAFT (PAPER V2 ruling, 2026-10-11): builder-drafted, not owner-approved -->

## 8 Methodology: bars come with floors

<!-- STUB-SPEC
PURPOSE: The measurement rules section 9 uses, each stated with the one exhibit from the project's own record that produced it, and where this paper falls short of them (section 8.6, kept whole). Define once what a reproducibility floor is.
SUBSECTIONS (H3, as the demo's): 8.1 A bar without a floor is void; 8.2 Contrasts and power; 8.3 Floors move with the run, and gates must not divide by them; 8.4 The floor is a check, not the test variance (the demo's "hurdle" becomes "check", BRIEF section 5.2); 8.5 Instruments state what they are blind to; 8.6 Where this paper falls short of its own rules.
WRITER: W5. BUDGET: 850 prose words (the demo's: 1,447); Figure 10 caption at most 120 words.
REQUIRED FACTS: METH-1 (the Medium completion floor moved 2.75-fold, 0.0145 to 0.0399, survival 0.0129 to 0.0130; GPU, code version and configuration all differ, so the exhibit shows a floor can move for one metric and not another, not which factor moved it); DX-403 (RTX 5090 against RTX PRO 6000; reps); METH-2 (the reference code version read 0 of 760 field hashes differing in 4 of 4 comparisons; the refactored version differed from itself 1 time in 4 on two diagnostic channels; no trajectory field differed); DX-38 (σ_seed 0.0295 against the later High floor 0.0621, CB-7: the first floor-less bar, its "strong" retracted); DX-302 (roughly 46 seeds per arm to match Medium's resolution at High); COM-5 (the VOID condition: 20 % against 27.2 %, observed 23.2 %; the threshold was chosen at implementation, not registered); METH-3 (per-arm forms 92.1 % and 62.8 % against the contrast's 76.7 %, k = 34); METH-4 (k = 20 on a bare 2σ figure gave 55.6 % power, caught at registration); METH-7 and DES-13 (the 80 %-power MDE at the family-corrected α; z_α = 2.2365); DX-34 and METH-5 (floor growth 500 to 1000 updates: ISO 0.0165 to 0.0339, JOINT 0.0093 to 0.0483, 2.1-fold and 5.2-fold; length confounded with machine; the curriculum-difficulty ordering is an untested hypothesis); METH-6 (the T* ruling of 2026-08-11 retired a registered convergence check that divided by the floor, and fixed the estimand at matched compute); DX-21 (floor-based standard errors 0.00970 and 0.00177; the numbers' home is section 9.2, so here state the rule and point); DX-32 (24 of 24 rendered episodes of the Coupling-B grid drift towards a wall; rendered-pixel centroids, a diagnostic); CB-9 and DX-306 and DX-303 (for section 8.6: CB-9 graded against a three-seed spread; floors exist only for the sweep's p = 0.5 arm and the identification arm is ungraded; a four-run floor is uncertain by about ±40 %); DX-28 (p = 0.5).
FIGURES: Figure 10, floors_explorer.html, companion floors_explorer.png, height 460, carried below. Caption at most 120 words; it glosses "card", "floor basis", "beat", "M5.1e" and "M6.0" as printed (BRIEF section 5.2); each tab prints its confound, so the caption need not repeat the numbers (rule R3).
LISTINGS: none (Listing 3 may be referred to as the bitwise discipline that makes same-version comparisons meaningful).
LATEX: two displays: the contrast standard error in the unequal-k form section 9 uses, sd(Γ) = √(s_ISO²/k_ISO + s_JOINT²/k_JOINT), noting that equal k gives √((σ_ISO² + σ_JOINT²)/k); and MDE₈₀ = (z_α + z_0.8) sd(Γ). Section 9.1 points back here instead of re-deriving.
HONESTY LINES AND REGISTERED STRINGS: "recorded, not graded" (the position-drift diagnostics have no floors and were kept out of the registered family); a differenced test sees asymmetry and nothing else; "reference scale (cross-artifact)"; bias (b)'s readings are in section 9.1 (state here only the rule that every reading of a registered bias is reported, with a pointer); "Bias (b) reverses sign on the grid card" belongs to section 9.1.
FIX-LIST AND FINDINGS ITEMS OWNED: F5 (card to GPU; M4.4, M5.1e, M5.3, M5.3b, M5.5, M6.0, M6.2, M6.2b to study descriptions, codes only in Appendix C's key; floor-basis to "the floor-based standard error of Γ"; beat-reproducibility to "the check that an effect exceeds rerun noise"; re-floor to "re-measured reproducibility floor"; tree, digest and traced to "two versions of the code" and "per-field trajectory hashes"; plateau guard to "a registered convergence check, retired before the grid"; drift channels to "position-drift diagnostics (recorded, not graded)"; box to "machine"; launch batch to "the first floor study"); OI-5 (never "different hardware" for M5.3's floor); LEN (each rule with a one-sentence exhibit; the exhibits' detail to Appendix C; HW-1's numbers to section 9.2; bias (b) to section 9.1); P3-§6 (no "This section states" opening; rule statements may be bold once each, nothing else bold).
DEMO KEEPS (sections/08_methodology.md): each rule with its exhibit and its confound; Figure 10; section 8.6 whole. CHANGES: the jargon; the exhibits' detail to Appendix C; section 8.4's numbers become a pointer; section 8.5's bias (b) paragraph becomes a rule plus a pointer. DROPS: repeated numbers.
NOT HERE: "every bar in the paper is floor-graded"; "the RTX 5090 is less reproducible" (the intervals overlap, DX-35); the curriculum-difficulty ordering as a finding; "card" alone for METH-1's exhibit (GPU, code version and configuration); a registered status for M5.5's 20 % threshold.
DEPENDENCIES: section 9.1 uses rules 8.2 and 8.4 for design-stage power and the test; section 9.2 uses 8.4's check; section 10 item 6 uses 8.5; Appendix C (W5) holds every floor.
-->

GPU training is not reproducible run to run: the compiler chooses kernels by timing them and some reductions use atomics. A reproducibility floor is the standard deviation of a metric over identical reruns, with the same seed, configuration and code. Each rule below came from a defect in the project's record; Appendix C lists every floor.

<figure class="l-page">
  <iframe src="{{ 'assets/html/submission/floors_explorer.html' | relative_url }}" width="100%" height="472" style="border:none" title="Floors explorer: reproducibility floors per GPU, per artifact and per run length, and the confirmatory grid against its floor" loading="lazy"></iframe>
  <figcaption><strong>Figure 10.</strong> Reproducibility floors per GPU, per artifact and per run length, and the confirmatory grid against its floor, one tab each, with its confound. On the figure, "card" is the GPU, "box" the machine, "tree" a code version and "reps" identical reruns; M5.1e, M5.5 and M6.0 are keyed in Appendix C. "Traced" and "baseline" are the refactored and reference versions, compared by per-field trajectory hashes ("field digests"); "floor-basis sd(Γ)" is the floor-based standard error of Γ (§8.4). It cannot show contrasts without a floor (§8.6). <span class="figure-note">Status: point estimates over identical reruns, about ±40 % uncertain at four reruns<!-- N:DX-303 --> · Interact: click a tab or press ← / →; hover or tab to a mark.</span></figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/floors_explorer.png" class="img-fluid" alt="Reproducibility floors on two GPUs, rerun comparisons of two versions of the code, floor growth from the shorter to the longer run length, and the confirmatory grid's seed dispersion against its floor, each with its confound stated." caption="Static companion of Figure 10 for the printed PDF." %}
</div>

### 8.1 A bar without a floor is void

No acceptance threshold enters an analysis script without a measured floor for the quantity it grades, or an explicit UNDERPOWERED flag. A threshold below its instrument's noise cannot pass under the null, so its output is void, and a void test voids a PASS as it voids a FAIL. The rule followed four<!-- N:V5-1 --> bars with invented constants (Appendix C). In one, the denial study of §7 graded a condition with a 20 %<!-- N:COM-5 --> threshold, chosen at implementation, against a quantity whose rerun nondeterminism is 27.2 %<!-- N:COM-5 -->. Since the threshold sits below the noise, the condition is VOID; the observed 23.2 %<!-- N:COM-5 --> exceeded the threshold but not the noise.

Floors are facts per metric and per GPU. Re-measuring the Medium floor moved completion's 2.75-fold<!-- N:METH-1 --> and left survival's unchanged, 0.0129<!-- N:METH-1 --> against 0.0130<!-- N:METH-1 -->. The two studies differ in GPU, code version and configuration, so the exhibit cannot say which of the three moved the completion floor. The floor is measured on the GPU that runs the grid.

Floors are facts per artifact. In a refactor of the environment code, the rerun floor measured on the reference version read zero, so two<!-- N:METH-2 --> diagnostic channels that differed between the versions looked like a semantic change. The refactored version then differed from itself 1 time in 4<!-- N:METH-2 --> on the same channels. An equivalence claim between A and B needs A against A and B against B as well as A against B.

### 8.2 Contrasts and power

A contrast is graded on its own standard error. For Γ, the difference between the JOINT and ISO arm means over $k_{\mathrm{JOINT}}$ and $k_{\mathrm{ISO}}$ seeds with seed standard deviations $s_{\mathrm{JOINT}}$ and $s_{\mathrm{ISO}}$,

$$
\operatorname{sd}(\Gamma) = \sqrt{\frac{s_{\mathrm{ISO}}^2}{k_{\mathrm{ISO}}} + \frac{s_{\mathrm{JOINT}}^2}{k_{\mathrm{JOINT}}}},
$$

which for equal $k$ is $\sqrt{(s_{\mathrm{ISO}}^2 + s_{\mathrm{JOINT}}^2)/k}$. The per-arm forms, each arm's own $s\sqrt{2/k}$, bracket that value without equalling it: at $k = 34$<!-- N:METH-3 -->, on the 1000<!-- N:DX-34 -->-update completion floors and a 0.03<!-- N:DES-4 --> effect, ISO's gave 92.1 %<!-- N:METH-3 --> power and JOINT's 62.8 %<!-- N:METH-3 -->, where the contrast's power was 76.7 %<!-- N:METH-3 -->.

A design-stage power statement is the minimum detectable effect at 80 %<!-- N:METH-7 --> power and the family-corrected level,

$$
\mathrm{MDE}_{80} = \big(z_\alpha + z_{0.8}\big)\,\operatorname{sd}(\Gamma),
$$

with $z_\alpha = 2.2365$<!-- N:DES-13 --> the Šidák-corrected critical value for the two co-primaries. The exclusion bound $X$ that §9 attaches to a null is this quantity on the grid's realized seed dispersion. A bare $2\sigma\sqrt{2/k}$ is the effect at which an uncorrected test would just reject, which it detects about half<!-- N:V4-1 --> the time; it survives only for grading an observed effect against a floor after the fact, labelled as such. The confirmatory seed count was first ruled at $k = 20$<!-- N:METH-4 --> on such a figure, without the Šidák correction; corrected, completion had 55.6 %<!-- N:METH-4 --> power against its motivating effect band, a slip caught before any run.

### 8.3 Floors move with the run, and gates must not divide by them

Floors grow with run length. From 500<!-- N:DX-34 --> to 1000<!-- N:DX-34 --> updates the completion floor grew 2.1-fold for ISO and 5.2-fold for JOINT<!-- N:METH-5 -->, with length confounded with machine.

A gate that divides by a floor diverges on more reproducible hardware. A registered convergence check, retired before the grid, divided each arm's late-training drift by its floor, so any nonzero drift fails as the floor goes to zero; it fired when JOINT's floor fell faster than its drift. The $T^*$ ruling of 2026-08-11<!-- N:METH-6 --> retired it as a gate, fixed the estimand as Γ at matched compute, and made Γ(t) required robustness evidence (§9.2).

### 8.4 The floor is a check, not the test variance

The floor and the test statistic are different variances. A floor comes from identical reruns at one seed, while a $k$-seed arm mean varies by seed as well. The confirmatory contrast is graded on the grid's own seed dispersion. The floor serves the check that an effect exceeds rerun noise, which uses the floor-based standard error of Γ: the display in §8.2 with floors in place of seed standard deviations (§9.2). For design-stage power, the floor gives an upper bound, labelled as one.

### 8.5 Instruments state what they are blind to

A differenced test sees asymmetry and nothing else. A condition of the form "no cross-arm difference in X" cancels any X present in both arms. In 24 of 24<!-- N:DX-32 --> rendered episodes of the Coupling-B calibration grid, the alive agents' centroid drifted towards a wall (rendered-pixel centroids, a diagnostic). That grid's inertness falsifier, logged before its data, included the condition "no cross-arm exposure/positioning difference", which could not see a drift present in both arms; the verdict it fed rests on its other conditions.

Measuring is not grading. A recorded channel becomes evidence only inside a registered analysis family, with a floor measured on its artifact. Position-drift diagnostics added before the grid are recorded for every grid run. They are recorded, not graded: adding them to the registered family after registration would have enlarged it and inflated its correction.

The differential drift between the arms, bias (b) of §9.1, changed sign between the four<!-- N:DES-10 --><!-- N:V6-4 --> floor studies that read it at 1000<!-- N:DES-13 --> updates before unblinding, so §9.1 reports every reading.

### 8.6 Where this paper falls short of its own rules

Coupling B's Medium survival effect was judged only against a three-seed<!-- N:CB-9 --> spread (§6.4). The trained-policy contrasts of §5 and §6 come from two calibration grids without identical reruns: their spreads are seed ranges, and any floor shown beside them is a reference scale (cross-artifact). In the secondary design, floors exist only for the sweep arm at $p = 0.5$<!-- N:DX-28 -->; the intermediate sweep arms assume that floor, and the identification arm is ungraded<!-- N:DX-306 -->. ISO-4 has no identical reruns, so the contrasts that involve it are graded on seed dispersion alone, and the High-severity readout flags ISO-4 UNDERPOWERED for the check against rerun noise. The position-drift diagnostics have no floor. Every floor is itself a point estimate: measured on four<!-- N:DX-303 --> identical runs, a standard deviation is uncertain by roughly ±40 %<!-- N:DX-303 -->.
