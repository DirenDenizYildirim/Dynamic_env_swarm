<!-- PAPER V3 DRAFT (PAPER V3 ruling, 2026-10-12): builder-drafted, not owner-approved -->

### 6.3 Results

Every secondary analysis, the plane decomposition included, is non-verdict-bearing, as registered: its 95 % intervals are not family-corrected, and its specification was ratified after Γ was seen and before the sweep was read<!-- N:DX-413 -->. A sweep holds each coupling's frequency at 0.5<!-- N:DES-9 --> while $p$ moves from 0 to 0.5<!-- N:DX-28 -->, and three<!-- N:DX-28 --> identification arms at frequency 0.4<!-- N:DES-9 --> make a plane in co-occurrence and fire-only share estimable (Appendix F).

On survival, the plane's co-occurrence slope $\gamma_p$ is +3.26 points per unit $p$ [+1.37, +5.02], and its fire-only-share slope $\gamma_n$ is −2.37 points per unit $\nu$ [−4.19, −0.57]<!-- N:SEC-1 --> (Figure 6, which prints $\mu$ as m and $\nu$ as n). By §6.2's identity, the plane separates co-occurrence from the active share only; per-coupling frequency moves with each slope. The fire-only-share slope predicts ISO-4 − ISO at +0.79 points<!-- N:SEC-3 -->, inside B̂'s interval, though that move also changes frequency. The co-occurrence slope, fitted on $p$ up to 0.5<!-- N:DX-28 -->, predicts JOINT − ISO-4 at +3.26 points<!-- N:SEC-4 -->, far above the measured Γ₄ (Table 3): it does not extrapolate to JOINT.

<!-- FIGURE 6: block carried from paper/v2/sections/09_compositional_test.md:114 (markup, iframe height and alt text as v2 had them); caption replaced; the writer checks the alt text -->

<figure class="l-page">
  <iframe src="{{ 'assets/html/submission/simplex_secondary.html' | relative_url }}" width="100%" height="832" style="border:none" title="Secondary design on the triangle of training mixtures, with plane predictions beside measured contrasts" loading="lazy"></iframe>
  <figcaption><strong>Figure 6.</strong> Left: training mixtures in p and ν, with the arms and the p = 0 sweep arm (labelled “sweep_c50_p000” on the figure). Right: secondary estimates and plane predictions beside B̂, Γ₄, Γ₄′: the change point (labelled “knee” on the figure), the sweep slope (labelled “dose slope” on the figure) and the fire-only share's term (labelled “no-element share” on the figure). <span class="interact">Switch metrics.</span></figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/simplex_secondary.png" class="img-fluid" alt="A triangle of training mixtures by share of both-stressor and fire-only episodes, locating the secondary arms, ISO, ISO-4 and JOINT, beside the secondary estimates and the plane predictions next to the measured contrasts" caption="Static companion of Figure 6 for the printed PDF." %}
</div>

On survival, Γ is +0.96 points, Šidák-corrected 95 % CI [+0.47, +1.44]<!-- N:RES-2 -->: REJECT (Table 3; Figure 7 prints rates). On completion it is −1.73 points [−4.12, +0.66]<!-- N:RES-1 -->, null: no detectable change, and the result excludes a joint-training gain larger than 0.66 points<!-- N:RES-1 -->. The design's completion detection limit, the registration's X, is 3.29 points<!-- N:RES-1 -->; realized power at the 3-point effect that motivated the design was 71.6 %<!-- N:DES-6 -->. The registered falsifier passes<!-- N:RES-5 --> (Appendix D).

The survival gain does not survive the inert-share correction. Γ₄, the corrected gap, is −0.03 points on survival [−0.68, +0.63]<!-- N:RES-6 -->, null, and the gain is not called a composition effect. On completion both gaps are null, so, as registered, Γ₄'s interval is quoted as a second exclusion bound; its detection limit is X₄ = 4.88 points<!-- N:RES-6 -->. Γ₄ excludes only a large composition effect: its survival interval reaches +0.63<!-- N:RES-6 -->, above the lower end of Γ's, +0.47<!-- N:RES-2 -->, and its survival detection limit is 0.90 points<!-- N:X4-4 -->. JOINT still sees each coupling twice as often as ISO-4<!-- N:DES-14 -->, and always combined. Γ₄ compares runs on two GPUs of one model; its same-GPU replicate Γ₄′, JOINT minus the $p = 0$ sweep arm (ISO-4's mixture on JOINT's GPU), agrees on both co-primaries but was proposed after Γ₄ was seen<!-- N:RES-8 --><!-- N:HW-4 --><!-- N:DES-15 -->. Across GPU models, a descriptive diagnostic on 12 paired seeds shifted the survival JOINT − ISO gap by about Γ's size (Appendix D). B̂ is reported without a test, as registered<!-- N:RES-7 -->. Γ = Γ₄ + B̂ holds by construction for arm means, so B̂ adds no separate test; descriptively, its survival estimate, +0.98 points<!-- N:RES-7 -->, is about Γ's size, and it too compares runs on two GPUs. The registered headline for this outcome, "composition is paid in agents, not task return", no longer holds as worded (Appendix D).

Γ(t), the gap at earlier checkpoints, is sign unstable over the final half on both co-primaries, the registration's term for a sign that changes across checkpoints in that half<!-- N:RES-11 -->. On survival, its Šidák interval excludes zero only at updates 900, 950 and 1000<!-- N:RES-12 -->. Completion is negative at every checkpoint from update 700<!-- N:RES-13 --> and leans negative, unresolved (Appendix E).

In agents, the survival gain is about a tenth of an agent per episode (0.11 of 12<!-- N:X4-3 --><!-- N:ENV-6 -->), detectable only in the last fifth of training<!-- N:RES-12 -->. The paper does not rest on it.

**Table 3.** Arm means (rates) and registered contrasts (points, rate × 100) at θ\*, with Šidák-corrected 95 % intervals; k in the order of each contrast's arms. As registered, intervals use normal quantiles; for contrasts with a 20-seed arm, t-based intervals would be slightly wider.

| quantity | k | completion | survival | status |
|---|---|---|---|---|
| ISO mean | 72<!-- N:DES-3 --> | 0.7772<!-- N:RES-4 --> | 0.9158<!-- N:RES-4 --> | confirmatory arm |
| JOINT mean | 72<!-- N:DES-3 --> | 0.7600<!-- N:RES-4 --> | 0.9254<!-- N:RES-4 --> | confirmatory arm |
| ISO-4 mean | 20<!-- N:DES-13 --> | 0.7726<!-- N:DX-18 --> | 0.9256<!-- N:DX-18 --> | sensitivity arm |
| Γ = JOINT − ISO | 72 / 72<!-- N:DES-3 --> | null: −1.73 [−4.12, +0.66]<!-- N:RES-1 --> | REJECT: +0.96 [+0.47, +1.44]<!-- N:RES-2 --> | confirmatory |
| Γ₄ = JOINT − ISO-4 | 72 / 20<!-- N:DES-3 --><!-- N:DES-13 --> | null: −1.26 [−4.81, +2.28]<!-- N:RES-6 --> | null: −0.03 [−0.68, +0.63]<!-- N:RES-6 --> | sensitivity arm, two GPUs |
| Γ₄′ = JOINT − the p = 0 sweep arm | 72 / 20<!-- N:DES-3 --><!-- N:DES-13 --> | null: −2.47 [−6.16, +1.22]<!-- N:RES-8 --><!-- N:DX-19 --> | null: +0.13 [−0.56, +0.81]<!-- N:RES-8 --> | secondary, one GPU |
| B̂ = ISO-4 − ISO | 20 / 72<!-- N:DES-13 --><!-- N:DES-3 --> | −0.46 [−4.05, +3.12]<!-- N:RES-7 --><!-- N:DX-19 --> | +0.98 [+0.33, +1.63]<!-- N:RES-7 --> | no registered test |

<!-- FIGURE 7: block carried from paper/v2/sections/09_compositional_test.md:64 (markup, iframe height and alt text as v2 had them); caption replaced; the writer checks the alt text -->

<figure class="l-page">
  <iframe src="{{ 'assets/html/submission/ladder_registered_readings.html' | relative_url }}" width="100%" height="1012" style="border:none" title="Registered readings in order: Gamma, Gamma4, Gamma4 prime and B-hat on both co-primaries" loading="lazy"></iframe>
  <figcaption><strong>Figure 7.</strong> The registered contrasts in order, one step per row (labelled “rung” on the figure): Γ, with the registered 60-seed<!-- N:DES-1 --> analysis; Γ₄; Γ₄′; and B̂, with no registered test. Rows name one GPU (labelled “unit 1” on the figure) or two (labelled “cross-unit” on the figure). Γ's stipple is ±1 floor-based standard error (labelled “floor basis” on the figure). <span class="interact">Step the rows.</span></figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/ladder_registered_readings.png" class="img-fluid" alt="Two forest plots, completion and survival, of the registered contrasts in order with their Šidák-corrected intervals and verdicts" caption="Static companion of Figure 7 for the printed PDF." %}
</div>
