<!-- PAPER V3 DRAFT (PAPER V3 ruling, 2026-10-12): builder-drafted, not owner-approved -->

## 5 Measurement protocol

GPU training is not bitwise reproducible. A reproducibility floor is the standard deviation of a metric over identical reruns of one artifact (the same code, configuration and seed) on one GPU. Under this protocol, an acceptance threshold, or bar, needs a floor measured on the artifact it grades, for that metric and GPU, or the analysis is declared underpowered. Not every comparison has a floor (Appendix C).

A design-stage power statement is a detection limit: the effect a test detects with 80 %<!-- N:METH-7 --> power at its family-corrected level $\alpha$, computed on the contrast's standard error,

$$
\mathrm{MDE}_{80} = \big(z_\alpha + z_{0.8}\big)\,\mathrm{SE}, \qquad \mathrm{SE} = \sqrt{\frac{s_A^2}{k_A} + \frac{s_B^2}{k_B}},
$$

where $z$ are standard normal quantiles and $s_A$ and $s_B$ are the arms' seed standard deviations over $k_A$ and $k_B$ seeds. A bare $2\sigma\sqrt{2/k}$ threshold detects an effect of its own size only about half<!-- N:V4-1 --> the time, so it only grades an observed effect against a floor, after the fact and labelled. When a confidence interval contains zero, each end is an exclusion bound: at the interval's level, the data exclude a gain above the upper end and a loss below the lower end, and the larger absolute end bounds the effect's size. The registration also calls its detection limit X an exclusion bound (§6.3).

The floor is not the test's variance: arm means also vary by seed, so contrasts are graded on seed dispersion, and the floor only checks that an effect exceeds rerun noise. A logged diagnostic becomes evidence only inside a registered test family, with a floor on its artifact; until then it is recorded, not graded. A difference between arms cannot show an effect present in both. From four identical runs, a floor is itself uncertain by about ±40 %<!-- N:DX-303 -->.
