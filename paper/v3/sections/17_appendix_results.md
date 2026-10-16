<!-- PAPER V3 DRAFT (PAPER V3 ruling, 2026-10-12): builder-drafted, not owner-approved -->

### E Additional results

<!-- STUB-SPEC
JOB: The results the main text points to: Γ(t) tables and figure; the k = 60 analysis; T = 2000; the High readout (home of the a-fortiori exclusion); fire deaths; seed dispersion over the floor; the communication-denial measurements figure.
WRITER: W5.
BUDGET: about 550 prose words plus the two Γ(t) tables; figure captions at most 60 words each.
FROM: P1 §6.1 E; P2 §3 A1, A3.
ROWS: DX-24, DX-25, RES-1, RES-2, RES-11, RES-12, RES-13, RES-3, DX-20, RES-15, DX-23, DES-11, RES-14, DX-26, RES-10, DX-22, HW-1, DX-21, COM-1, COM-4, DES-13.
FIGURES: Figure E1 gamma_t_final_half (glosses: labelled “grid card”, labelled “single-card curve”); Figure E2 static fig06_comms.png (glosses: labelled “E2C²”, labelled “M5.2”, labelled “M5.5”). Blocks below.
REGISTERED STRINGS: "sign unstable over the final half" first; UNDERPOWERED (k = 60; T = 2000; change points); "a-fortiori exclusion" with its sentence "no gap larger than X at High even where JOINT trained on the evaluated configuration and ISO never saw a composed one" (the X values are MDEs: label them, BRIEF §9.2 trap 5); descriptive for Γ(t) at t below 1000 and T = 2000.
CAVEATS HOMED HERE (state each in full, once; the detection pattern, from checks/caveats.yaml, must match your home sentence):
  C24 high_readout_a_fortiori: The High readout is an a-fortiori exclusion, not a held-out test (full statement in App. E). Pattern: (?i)a-fortiori
EVERY OTHER CAVEAT in checks/caveats.yaml: pointer only ("§6.3", "Appendix D"), never restated. C26: any sentence about the interaction check carries "post hoc".
NOT HERE: the High readout as a held-out test; T = 2000 as anything but descriptive; any Γ(t) value beyond DX-24, DX-25.
V2 MATERIAL: paper/v2/sections/14_appendix_plan_provenance.md (G); 09_compositional_test.md §9.2 (k = 60, T = 2000, High, fire deaths); 07_comms.md (Figure 9 text).
DEPENDENCIES: §6.3 points here; §4.4 points here for the comms figure.
-->

**Sign unstable over the final half**, on both co-primaries<!-- N:RES-11 -->: neither meets the registered rule that all 11<!-- N:DES-13 --> point estimates over updates 500–1000<!-- N:DES-13 --> share one sign (Appendix D). The intervals are Šidák-corrected, registered at update 1000<!-- N:DES-13 --> and descriptive before it. Checkpoints before update 1000 were evaluated after unblinding, on a different GPU of the same model; update 1000 is the main runs' own evaluation, and re-evaluating it on that GPU leaves every sign unchanged (§8).

<!-- FIGURE E1: block carried from paper/v2/sections/09_compositional_test.md:101 (markup, iframe height and alt text as v2 had them); caption replaced; the writer checks the alt text -->

<figure class="l-page">
  <iframe src="{{ 'assets/html/submission/gamma_t_final_half.html' | relative_url }}" width="100%" height="503" style="border:none" title="Gamma over the final half of training, completion and survival" loading="lazy"></iframe>
  <figcaption><strong>Figure E1.</strong> <strong>Sign unstable over the final half</strong>, on both co-primaries<!-- N:RES-11 -->. Γ(t) with Šidák-corrected intervals; only the last checkpoint is the registered Γ. Rings mark signs that differ from the final one, under the sign rule labelled “rule (iv)” on the figure. The main runs’ GPU is labelled “grid card” on the figure; the “single-card curve” re-evaluates the last checkpoint on another GPU. The dotted box is ±1 floor-based standard error of Γ.</figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/gamma_t_final_half.png" class="img-fluid" alt="The retained checkpoints over the final half of training of the joint-minus-isolated difference in completion and in survival, each with its Šidák interval, labelled sign unstable over the final half" caption="Static companion of Figure E1 for the printed PDF." %}
</div>

Completion, k = 72 per arm<!-- N:DES-13 -->, in rates:

| update | Γ(t) | sd(Γ) | Šidák CI | sign |
|---|---|---|---|---|
| 500 | +0.0017<!-- N:DX-24 --> | 0.00321<!-- N:DX-24 --> | [−0.0055, +0.0089]<!-- N:DX-24 --> | + |
| 550 | −0.0017<!-- N:DX-24 --> | 0.00353<!-- N:DX-24 --> | [−0.0096, +0.0062]<!-- N:DX-24 --> | − |
| 600 | +0.0018<!-- N:DX-24 --> | 0.00362<!-- N:DX-24 --> | [−0.0063, +0.0099]<!-- N:DX-24 --> | + |
| 650 | +0.0015<!-- N:DX-24 --> | 0.00481<!-- N:DX-24 --> | [−0.0093, +0.0122]<!-- N:DX-24 --> | + |
| 700 | −0.0037<!-- N:DX-24 --> | 0.00470<!-- N:DX-24 --> | [−0.0142, +0.0068]<!-- N:DX-24 --> | − |
| 750 | −0.0147<!-- N:RES-13 --> | 0.00610<!-- N:DX-24 --> | [−0.0283, −0.0010]<!-- N:RES-13 --> | − |
| 800 | −0.0035<!-- N:DX-24 --> | 0.00677<!-- N:DX-24 --> | [−0.0187, +0.0116]<!-- N:DX-24 --> | − |
| 850 | −0.0053<!-- N:DX-24 --> | 0.00729<!-- N:DX-24 --> | [−0.0216, +0.0110]<!-- N:DX-24 --> | − |
| 900 | −0.0039<!-- N:DX-24 --> | 0.00843<!-- N:DX-24 --> | [−0.0228, +0.0149]<!-- N:DX-24 --> | − |
| 950 | −0.0016<!-- N:DX-24 --> | 0.01021<!-- N:DX-24 --> | [−0.0245, +0.0212]<!-- N:DX-24 --> | − |
| 1000 | −0.0173<!-- N:RES-1 --> | 0.01068<!-- N:DX-24 --> | [−0.0412, +0.0066]<!-- N:RES-1 --> | − |

Survival rate, k = 72 per arm<!-- N:DES-13 -->, in rates:

| update | Γ(t) | sd(Γ) | Šidák CI | sign |
|---|---|---|---|---|
| 500 | +0.0022<!-- N:DX-25 --> | 0.00228<!-- N:DX-25 --> | [−0.0029, +0.0073]<!-- N:DX-25 --> | + |
| 550 | −0.0037<!-- N:DX-25 --> | 0.00220<!-- N:DX-25 --> | [−0.0086, +0.0013]<!-- N:DX-25 --> | − |
| 600 | −0.0027<!-- N:DX-25 --> | 0.00232<!-- N:DX-25 --> | [−0.0078, +0.0025]<!-- N:DX-25 --> | − |
| 650 | +0.0011<!-- N:DX-25 --> | 0.00242<!-- N:DX-25 --> | [−0.0043, +0.0065]<!-- N:DX-25 --> | + |
| 700 | +0.0031<!-- N:DX-25 --> | 0.00235<!-- N:DX-25 --> | [−0.0021, +0.0084]<!-- N:DX-25 --> | + |
| 750 | +0.0036<!-- N:DX-25 --> | 0.00255<!-- N:DX-25 --> | [−0.0021, +0.0093]<!-- N:DX-25 --> | + |
| 800 | +0.0020<!-- N:DX-25 --> | 0.00232<!-- N:DX-25 --> | [−0.0032, +0.0072]<!-- N:DX-25 --> | + |
| 850 | +0.0018<!-- N:DX-25 --> | 0.00234<!-- N:DX-25 --> | [−0.0034, +0.0071]<!-- N:DX-25 --> | + |
| 900 | +0.0056<!-- N:RES-12 --> | 0.00231<!-- N:DX-25 --> | [+0.0004, +0.0108]<!-- N:DX-25 --> | + |
| 950 | +0.0083<!-- N:RES-12 --> | 0.00219<!-- N:DX-25 --> | [+0.0034, +0.0132]<!-- N:DX-25 --> | + |
| 1000 | +0.0096<!-- N:RES-2 --> | 0.00216<!-- N:DX-25 --> | [+0.0047, +0.0144]<!-- N:RES-2 --> | + |

The registered k = 60<!-- N:DES-1 --> analysis, on seeds 1–60<!-- N:RES-3 -->, reads as the k = 72<!-- N:DES-3 --> analysis does and is flagged UNDERPOWERED; the registered seed rule had required 72<!-- N:DES-3 --> seeds for completion. Completion is null at −2.17 points<!-- N:RES-3 --> [−4.86, +0.52]<!-- N:DX-20 -->, z −1.80<!-- N:RES-3 -->, and survival rejects at +1.04 points<!-- N:RES-3 --> [+0.54, +1.55]<!-- N:DX-20 -->, z +4.67<!-- N:RES-3 -->, with Šidák-corrected intervals. Realized completion power against a 3-point effect is 60.2 % at k = 60 and 71.6 % at k = 72<!-- N:DES-6 -->.

The 2000-update subsample (4 seeds per arm<!-- N:RES-15 -->, trained on a second GPU of the same model<!-- N:HW-4 -->) is descriptive and UNDERPOWERED by registration. Its Γ(2000) is +0.03 points<!-- N:RES-15 --> [−3.63, +3.69]<!-- N:DX-23 --> on completion and +1.59 points [−0.02, +3.19]<!-- N:RES-15 --> on survival, with 95 % intervals that are not family-corrected. The difference between JOINT's and ISO's training-curve slopes stays positive over updates 1000–2000, at +0.00384 (completion) and +0.00204 (survival) per 100 updates<!-- N:DX-23 -->, as it was over updates 500–1000<!-- N:DES-11 -->. The drift it measures has not visibly reversed, which is all it may be cited for.

The High-severity readout re-evaluated every final checkpoint of ISO, JOINT and ISO-4 with every stressor on at β = 0.70<!-- N:CAL-3 -->, outside the confirmatory family. Both co-primaries are null, so the reading is an **a-fortiori exclusion**: no gap larger than 3.40 completion points or 2.54 survival points<!-- N:RES-14 --> at High even where JOINT trained on the evaluated configuration and ISO never saw a composed one. Those two values are the readout's 80 %-power detection limits (the registered sentence's X), and its Šidák-corrected intervals are [−3.26, +1.68] (completion) and [−1.46, +2.23] (survival) points<!-- N:DX-26 -->. JOINT − ISO-4 at High is null too, at −0.75 [−3.87, +2.36] and −1.28 [−3.50, +0.95] points<!-- N:DX-26 -->, with no reading rule of its own. The JOINT − ISO gap lies within rerun noise, at 0.73 and 0.75 times its floor-based standard error (completion, survival)<!-- N:RES-14 -->; ISO-4 has no identical reruns, so that check is UNDERPOWERED for it. The readout is not a held-out test: JOINT trained on this configuration at weight 1/2<!-- N:DES-16 -->, and ISO never trained with more than one stressor on.

On secondary metrics outside the family, descriptive and without a floor, JOINT has 0.1177 fewer fire deaths per episode than ISO (z = −4.59)<!-- N:RES-10 -->, at 0.6949 against 0.8126<!-- N:DX-22 -->, and its episode return differs by −0.4958 (z = −1.44)<!-- N:DX-22 -->.

Seed dispersion exceeds the rerun floor in both arms, 1.12 and 1.09 times on completion and 1.25 and 1.19 times on survival (ISO, JOINT)<!-- N:HW-1 -->. Survival Γ, at 5.40 times its floor-based standard error<!-- N:HW-1 --> (completion 1.78 times<!-- N:DX-21 -->), clears the check that an effect exceeds rerun noise.

Figure E2 shows the measurements behind the inert label of §4.4. In the two-agent courier toy, the value of communication rises from 0 to 0.498<!-- N:COM-1 --> as perception decays (Figure E2(a)).

<!-- FIGURE E2: block carried from paper/v2/sections/07_comms.md:23 (include and alt text as v2 had them); caption replaced -->

{% include figure.html path="assets/img/submission/fig06_comms.png" class="img-fluid" alt="Top left, courier success rate against perception attenuation in the two-agent toy, for free and for denied communication, with the predicted curve. Top right, the denial contrasts at medium severity with their bars. Bottom, the per-run values behind those contrasts." caption="Figure E2. Communication in the toy, and denial in CHE at Medium." %}

<p class="caption">(a) The two-agent courier toy (labelled “E2C²” and “M5.2” on the figure), with scripted policies: success with free and with denied communication; the shaded gap is the value of communication. (b–d) The denial study at Medium (labelled “M5.5” on the figure): contrasts between open and denied links against bars of twice<!-- N:V4-2 --> the floor sd, and the per-run values.</p>
