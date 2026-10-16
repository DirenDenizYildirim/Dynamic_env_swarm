<!-- PAPER V3 DRAFT (PAPER V3 ruling, 2026-10-12): builder-drafted, not owner-approved -->

## 5 Measurement protocol

<!-- STUB-SPEC
JOB: The floors protocol as the rules this paper follows, not as a history of mistakes (BLIND W9): which bars have floors and how they are measured. Exhibits go to Appendix C.
WRITER: W3.
BUDGET: 270 prose words; at most two displays.
FROM: P1 §4.2 §5 and P-F; P3 §1.1 E7 (NARROW and unpositioned) and §2.2; P2 §3 A2.
ORDER:
  - a bar comes with a floor measured on the artifact being graded, per metric and per GPU (METH-1, METH-2, HW-1; one sentence of exhibit at most, details Appendix C)
  - design power is the 80 %-power detection limit at the family-corrected α (METH-7; one display); define "detection limit" and "exclusion bound" here (BRIEF §5.2)
  - a contrast is graded on the contrast's standard error (one display, the unequal-k form §6 uses)
  - the floor is a check that an effect exceeds rerun noise, not the test variance (DX-21)
  - recorded is not graded: a channel becomes evidence only with a registered family and a floor; differenced tests cannot see effects present in both arms (say "cannot see", not "blind to")
  - a floor from four runs is itself uncertain by about ±40 % (DX-303; HOME)
ROWS: METH-1, METH-2, METH-3, METH-4, METH-7, HW-1, DX-21, DX-303.
CITATIONS: none by default (no RL evaluation-methodology work is verified in RWV; V3Q17).
REGISTERED STRINGS: "recorded, not graded" (substance).
CAVEATS HOMED HERE (state each in full, once; the detection pattern, from checks/caveats.yaml, must match your home sentence):
  C36 four_run_floor_uncertainty: A floor from four runs is itself uncertain by about ±40 %. Pattern: ±\s*40\s*%
EVERY OTHER CAVEAT in checks/caveats.yaml: pointer only ("§6.3", "Appendix D"), never restated. C26: any sentence about the interaction check carries "post hoc".
NOT HERE: the four bars that broke the rule, the 46-seed story, the refactor story (Appendix C, one line each); "every acceptance bar is graded against a floor" (name which have one); study codes; "instrument", "hurdle", "beat", "floor basis", "re-floor", "card" (banned); "blind to" (the check's list owns that phrase, C25).
V2 MATERIAL: paper/v2/sections/08_methodology.md (§8.1 to §8.5; §8.6's shortfalls go to §7 or Appendix C).
DEPENDENCIES: §6 uses these rules; Appendix C (W3) holds every floor.
-->

GPU training is not bitwise reproducible. A reproducibility floor is the standard deviation of a metric over identical reruns of one artifact (the same code, configuration and seed) on one GPU. Under this protocol, an acceptance threshold, or bar, needs a floor measured on the artifact it grades, for that metric and GPU, or the analysis is declared underpowered.

A design-stage power statement is a detection limit: the effect a test detects with 80 %<!-- N:METH-7 --> power at its family-corrected level $\alpha$, computed on the contrast's own standard error,

$$
\mathrm{MDE}_{80} = \big(z_\alpha + z_{0.8}\big)\,\mathrm{SE}, \qquad \mathrm{SE} = \sqrt{\frac{s_A^2}{k_A} + \frac{s_B^2}{k_B}},
$$

where $z$ are standard normal quantiles and $s_A$ and $s_B$ are the two arms' seed standard deviations over $k_A$ and $k_B$ seeds. A bare $2\sigma\sqrt{2/k}$ threshold detects an effect of its own size only about half<!-- N:V4-1 --> the time, so it serves only as a labelled, after-the-fact grading of an observed effect against a floor. When a confidence interval contains zero, each end is an exclusion bound in its direction: at the interval's level, the data exclude a gain larger than the upper end and a loss larger than the lower end, and the larger absolute end bounds the effect's size.

The floor is not the test's variance: an arm mean over $k$ seeds also varies by seed, so contrasts are graded on seed dispersion, and the floor checks only that an effect exceeds rerun noise. A logged diagnostic becomes evidence only inside a registered family of tests, with a floor measured on its artifact; until then it is recorded, not graded. A difference between arms cannot show an effect present in both. A floor is itself an estimate: from four identical runs, a standard deviation is uncertain by about ±40 %<!-- N:DX-303 -->.
