<!-- PAPER V3 DRAFT (PAPER V3 ruling, 2026-10-12): builder-drafted, not owner-approved -->

### 6.3 Results

<!-- STUB-SPEC
JOB: Report the worked example's results: the plane decomposition first (PAPER V3 item 2(c)), labelled non-verdict-bearing; then the registered test, the correction, Γ(t) by its registered string, and the size stated plainly (V3-F3). Γ stays the registered test.
WRITER: W4.
BUDGET: 480 prose words; Figures 7 and 8 captions at most 60 words each; Table 3 (arm means and the registered readings).
FROM: P1 §4.2 §6.3, §5.1, §5.2; P2 §3 #8 to #9 and §5; P3 §3.2 (W4 items); PAPER V3 item 2(c); V3-F3, V3-F4.
ORDER:
  - (a) the plane, first (Figure 7): one sentence labels every secondary analysis non-verdict-bearing, with 95 % intervals not family-corrected, ratified after Γ was seen and before the sweep was read (DX-413; HOME of the label); the co-occurrence slope γ_p and the fire-only-share slope γ_n with intervals (SEC-1); γ_n predicts ISO-4 − ISO (SEC-3), inside B̂'s interval; γ_p predicts JOINT − ISO-4 (SEC-4) against Γ₄ and Γ₄′ measured (RES-6, RES-8): it does not extrapolate to JOINT; residuals check only coarse linearity (DX-39). Say exactly: the plane separates co-occurrence from the active share; per-coupling frequency moves with each slope.
  - (b) the registered test (Table 3 with absolute arm means, RES-4; Figure 8): survival Γ +0.96 points with its Šidák-corrected CI, REJECT (RES-2), always beside Γ₄ (FIGURE BATCH A1); completion: no detectable change, "excludes a joint-training gain larger than 0.66 points" (RES-1; HOME), with realized completion power 71.6 % at the motivating effect (DES-6; HOME) and X named as the effect the design detects with 80 % power (BRIEF §9.2 trap 5); the falsifier passes (RES-5, verdict only).
  - (c) the correction: Γ₄, the corrected gap JOINT − ISO-4 (RES-6): survival "does not survive the inert-share correction" (HOME); completion a "second exclusion bound"; JOINT still sees each coupling twice as often as ISO-4, always combined (DES-14; HOME); Γ₄ excludes only a large composition effect (its upper bound +0.63 above Γ's lower bound +0.47; HOME); Γ₄'s survival detection limit (X4-4; one clause); B̂ = ISO-4 − ISO reported without a test (RES-7; HOME); Γ = Γ₄ + B̂ holds by construction and is not a finding (HOME); Γ₄ compares runs on two GPUs; the same-GPU replicate Γ₄′ agrees and was proposed after Γ₄ was seen (RES-8, RES-9, HW-4, DES-15; HOME, one sentence); branch B's registered headline no longer holds as worded (one clause, no branch letter; Appendix D).
  - (d) Γ(t): "sign unstable over the final half" on both co-primaries (RES-11; HOME); the survival gap appears only at updates 900 to 1000 (RES-12); completion leans negative from 70 % of the budget (RES-13); tables and figure in Appendix E.
  - (e) the size, plainly (V3-F3 HOME): the survival gain is about a tenth of an agent per episode (0.11 of 12; X4-3), visible only at the end of training; the paper does not rest on it. One sentence may point to the High readout's a-fortiori exclusion (Appendix E).
ROWS: SEC-1, SEC-3, SEC-4, DX-39, DX-413, RES-1, RES-2, RES-4, RES-5, RES-6, RES-7, RES-8, RES-9, RES-11, RES-12, RES-13, DES-6, DES-13, DES-14, DES-15, HW-4, X4-3, X4-4.
FIGURES: Figure 7 simplex_secondary (first; glosses: labelled “knee”, labelled “no-element share”, labelled “sweep_c50_p000”; caption names γ_p's and γ_n's rows first, P2 R6 fallback); Figure 8 ladder_registered_readings (glosses: labelled “rung”, labelled “unit 1”, labelled “cross-unit”, labelled “floor basis”; the figure prints rates, the text points: say so once). Blocks below.
REGISTERED STRINGS: "does not survive the inert-share correction"; "sign unstable over the final half" (both co-primaries); "excludes a joint-training gain larger than 0.66 points"; "second exclusion bound"; REJECT and null; "non-verdict-bearing" once, then "secondary"; B̂ gets no verdict.
CAVEATS HOMED HERE (state each in full, once; the detection pattern, from checks/caveats.yaml, must match your home sentence):
  C06 joint_twice_iso4: JOINT sees each coupling twice as often as ISO-4, and always combined. Pattern: (?i)\btwice as often\b
  C15 secondary_non_verdict_bearing: The plane decomposition and every secondary analysis are non-verdict-bearing; their 95 % intervals are not family-corrected. Pattern: (?i)\bnon-verdict-bearing\b
  C16 sign_unstable_final_half: Registered string "sign unstable over the final half", on both co-primaries, with the shapes. Pattern: (?i)sign unstable over the final half
  C17 completion_exclusion_bound: Completion shows no detectable change and "excludes a joint-training gain larger than 0.66 points". Pattern: (?i)joint-training gain larger than
  C18 inert_share_correction: Registered string - the survival gain "does not survive the inert-share correction". Pattern: (?i)does not survive the inert-share correction
  C19 gamma4_excludes_only_large: Γ₄ excludes only a large composition effect (its upper bound lies above Γ's lower bound). Pattern: (?i)\bonly a large\b
  C20 bhat_without_test: B̂ = ISO-4 − ISO is reported without a test and gets no verdict. Pattern: B̂[^.]{0,120}\b(without a test|no test)\b
  C21 gamma_sum_by_construction: Γ = Γ₄ + B̂ holds by construction for arm means and is never a finding. Pattern: Γ\s*=\s*Γ₄\s*\+
  C22 cross_gpu_and_same_gpu_replicate: Γ₄ compares runs on two GPUs; the same-GPU replicate agrees and was proposed after Γ₄ was seen (GPU blocks in App. D). Pattern: (?i)\bsame-GPU replicate\b
  C23 realized_completion_power: Realized completion power at the motivating effect is 71.6 %, stated once beside the exclusion. Pattern: 71\.6
SHORT FORMS ALLOWED HERE (at most one sentence each; the full statement is at the home):
  C24 high_readout_a_fortiori (home 17_appendix_results.md)
EVERY OTHER CAVEAT in checks/caveats.yaml: pointer only ("§6.3", "Appendix D"), never restated. C26: any sentence about the interaction check carries "post hoc".
NEW ROWS OWED:
  - X4-3 (W4): about 0.11 agents per episode, DERIVED: 0.0095531 (P6/unblind/unblind.json:61) × 12 (ENV-6) = 0.1146; identity as DX-406 (deaths per episode = 12 × (1 − survival rate); che/env/env.py:446; che/tests/test_lethality.py:201-202); scope: the size statement.
  - X4-4 (W4): Γ₄ and B̂ survival detection limits 0.0090 and 0.0089, VERIFIED at P6/post_unblind_analysis/post_gamma4_t2000.md:15-16 (last column); confirm the column is the 80 %-power detection limit at the stated family level before use (V3Q18).
NOT HERE: "composition effect" without the correction; "composition does not matter"; "the plane separates co-occurrence from frequency"; Γ = Γ₄ + B̂ as a finding; a verdict for B̂; "budget-robust", "converged"; GPU 1/2/3, "card", "unit", "rung", "knee" outside glosses; the k = 60, T = 2000 and High details (Appendix E); mediation (Appendix F); "conservative" for the k increase; advice (that is §6.5).
V2 MATERIAL: paper/v2/sections/09_compositional_test.md §9.2.
DEPENDENCIES: §6.2 defines the shares and the identity; §6.5 (W5) points here for Γ₄'s limits; Appendix E (W5) and F (W4) hold the details.
-->

The secondary analysis comes first, because it shows what this design can separate. Every secondary analysis, the plane decomposition included, is non-verdict-bearing, as registered: its 95 % intervals are not family-corrected, and its specification was ratified after Γ was seen and before the sweep was read<!-- N:DX-413 -->. A sweep holds each coupling's frequency at 0.5<!-- N:DES-9 --> while p moves from 0 to 0.5<!-- N:DX-28 -->, and three identification arms at frequency 0.4<!-- N:DES-9 --> make a plane in co-occurrence and fire-only share estimable (Appendix F).

On survival, the plane's co-occurrence slope $\gamma_p$ is +3.26 points per unit p [+1.37, +5.02], and its fire-only-share slope $\gamma_n$ is −2.37 points per unit ν [−4.19, −0.57]<!-- N:SEC-1 --> (Figure 7). By the identity of §6.2, the plane separates co-occurrence from the active share only; per-coupling frequency moves with each slope. The fire-only-share slope predicts ISO-4 − ISO at +0.79 points<!-- N:SEC-3 -->, inside B̂'s interval, without attributing B̂ to the fire-only share as such, since that move also changes frequency. The co-occurrence slope, fitted on p up to 0.5<!-- N:DX-28 -->, predicts JOINT − ISO-4 at +3.26 points<!-- N:SEC-4 -->, far above the measured Γ₄ (Table 3): it does not extrapolate to JOINT. The plane's linearity is checked only coarsely (Appendix F).

<!-- FIGURE 7: block carried from paper/v2/sections/09_compositional_test.md:114 (markup, iframe height and alt text as v2 had them); caption replaced; the writer checks the alt text -->

<figure class="l-page">
  <iframe src="{{ 'assets/html/submission/simplex_secondary.html' | relative_url }}" width="100%" height="832" style="border:none" title="Secondary design on the triangle of training mixtures, with plane predictions beside measured contrasts" loading="lazy"></iframe>
  <figcaption><strong>Figure 7.</strong> Read first: the plane's prediction from the fire-only-share slope γ<sub>n</sub> beside the measured B̂, and from the co-occurrence slope γ<sub>p</sub> beside the measured Γ₄ and Γ₄′. Left, the triangle of training mixtures in p and ν; right, the secondary estimates: the change point (labelled “knee” on the figure), the sweep slope (labelled “dose slope” on the figure), the fire-only share's part of the endpoint change (labelled “no-element share” on the figure), the p = 0 sweep arm (labelled “sweep_c50_p000” on the figure). <span class="interact">Switch the metric; toggle the predictions.</span></figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/simplex_secondary.png" class="img-fluid" alt="A triangle of training mixtures by share of both-stressor and fire-only episodes, locating the secondary arms, ISO, ISO-4 and JOINT, beside the secondary estimates and the plane predictions next to the measured contrasts" caption="Static companion of Figure 7 for the printed PDF." %}
</div>

The registered test reads as follows (Table 3, Figure 8). On survival, Γ is +0.96 points, Šidák-corrected 95 % CI [+0.47, +1.44]<!-- N:RES-2 -->: REJECT. On completion it is −1.73 points [−4.12, +0.66]<!-- N:RES-1 -->, null: no detectable change, and the result excludes a joint-training gain larger than 0.66 points<!-- N:RES-1 -->. The effect the design detects with 80 % power at the family-corrected level, the registration's X, is 3.29 points on completion<!-- N:RES-1 -->, and realized power against the 3-point effect that motivated the design was 71.6 %<!-- N:DES-6 -->. The registered falsifier for this outcome passes<!-- N:RES-5 --> (Appendix D).

The survival gain does not survive the inert-share correction. On survival, Γ₄, the corrected gap, is −0.03 points [−0.68, +0.63]<!-- N:RES-6 -->, null, and the gain is not called a composition effect; on completion, where both gaps are null, Γ₄ is a second exclusion bound. Γ₄ excludes only a large composition effect: its upper bound, +0.63<!-- N:RES-6 -->, lies above Γ's lower bound, +0.47<!-- N:RES-2 -->, and its survival detection limit is 0.90 points<!-- N:X4-4 -->. JOINT still sees each coupling twice as often as ISO-4<!-- N:DES-14 -->, and always combined. Γ₄ compares runs on two GPUs; its same-GPU replicate Γ₄′, JOINT minus the p = 0 sweep arm (ISO-4's mixture trained on JOINT's GPU), agrees, null on both co-primaries, but was proposed after Γ₄ was seen<!-- N:RES-8 --><!-- N:HW-4 --><!-- N:DES-15 -->. B̂ is reported without a test, as registered; it is +0.98 points on survival<!-- N:RES-7 -->. Because Γ = Γ₄ + B̂ holds by construction for arm means, B̂ is not a second finding. The registered headline for this outcome, "composition is paid in agents, not task return", no longer holds as worded (Appendix D).

Γ(t), the gap at the earlier retained checkpoints, is sign unstable over the final half on both co-primaries<!-- N:RES-11 -->. On survival, its Šidák interval excludes zero only at updates 900, 950 and 1000<!-- N:RES-12 -->. Completion is negative at every checkpoint from update 700, 70 % of the budget<!-- N:RES-13 -->, and leans negative without resolving (Appendix E).

Restated in agents, the survival gain is about a tenth of an agent per episode (0.11 of 12<!-- N:X4-3 --><!-- N:ENV-6 -->), and it appears only in the last fifth of training<!-- N:RES-12 -->. The paper does not rest on it.

**Table 3.** Arm means (rates) and the registered contrasts (points, rate × 100) at θ\* after 1000<!-- N:DES-13 --> updates, with Šidák-corrected 95 % intervals; k is given in the order of each contrast's two arms.

| quantity | k | completion | survival | status |
|---|---|---|---|---|
| ISO mean | 72<!-- N:DES-3 --> | 0.7772<!-- N:RES-4 --> | 0.9158<!-- N:RES-4 --> | confirmatory arm |
| JOINT mean | 72<!-- N:DES-3 --> | 0.7600<!-- N:RES-4 --> | 0.9254<!-- N:RES-4 --> | confirmatory arm |
| ISO-4 mean | 20<!-- N:DES-13 --> | 0.7726<!-- N:DX-18 --> | 0.9256<!-- N:DX-18 --> | sensitivity arm |
| Γ = JOINT − ISO | 72 / 72<!-- N:DES-3 --> | null: −1.73 [−4.12, +0.66]<!-- N:RES-1 --> | REJECT: +0.96 [+0.47, +1.44]<!-- N:RES-2 --> | confirmatory |
| Γ₄ = JOINT − ISO-4 | 72 / 20<!-- N:DES-3 --><!-- N:DES-13 --> | null: −1.26 [−4.81, +2.28]<!-- N:RES-6 --> | null: −0.03 [−0.68, +0.63]<!-- N:RES-6 --> | sensitivity arm, two GPUs |
| Γ₄′ = JOINT − the p = 0 sweep arm | 72 / 20<!-- N:DES-3 --><!-- N:DES-13 --> | null: −2.47 [−6.16, +1.22]<!-- N:RES-8 --><!-- N:DX-19 --> | null: +0.13 [−0.56, +0.81]<!-- N:RES-8 --> | secondary, one GPU |
| B̂ = ISO-4 − ISO | 20 / 72<!-- N:DES-13 --><!-- N:DES-3 --> | −0.46 [−4.05, +3.12]<!-- N:RES-7 --><!-- N:DX-19 --> | +0.98 [+0.33, +1.63]<!-- N:RES-7 --> | no registered test |

<!-- FIGURE 8: block carried from paper/v2/sections/09_compositional_test.md:64 (markup, iframe height and alt text as v2 had them); caption replaced; the writer checks the alt text -->

<figure class="l-page">
  <iframe src="{{ 'assets/html/submission/ladder_registered_readings.html' | relative_url }}" width="100%" height="1012" style="border:none" title="Registered readings in order: Gamma, Gamma4, Gamma4 prime and B-hat on both co-primaries" loading="lazy"></iframe>
  <figcaption><strong>Figure 8.</strong> The registered contrasts in order on completion and survival, one step per row (labelled “rung” on the figure): Γ, with the registered 60-seed analysis; Γ₄; Γ₄′; and B̂, which has no registered test. Rows name one GPU (labelled “unit 1” on the figure) or two (labelled “cross-unit” on the figure). Values are rates. The stipple on Γ is ±1 floor-based standard error (labelled “floor basis” on the figure). <span class="interact">Step through the rows; toggle the bands.</span></figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/ladder_registered_readings.png" class="img-fluid" alt="Two forest plots, completion and survival, of the registered contrasts in order with their Šidák-corrected intervals and verdicts" caption="Static companion of Figure 8 for the printed PDF." %}
</div>
