<!-- PAPER V3 DRAFT (PAPER V3 ruling, 2026-10-12): builder-drafted, not owner-approved -->

### H Trained-policy episodes

<!-- STUB-SPEC
JOB: Two trained-policy episodes, one ISO and one JOINT, shown separately, illustrative (FIGURE BATCH A3). Kept by default; the owner may drop this appendix (V3Q10; P2 recommends dropping it).
WRITER: W5.
BUDGET: about 80 prose words; captions at most 60 words each.
FROM: v2 Appendix I; FIGURE BATCH A3; P2 §6 (drop recommended).
ROWS: ENV-13, ENV-6, DX-410.
FIGURES: Figures H1 (ISO) and H2 (JOINT): H1, then a sentence, then H2, never side by side; gloss labelled “obs v3” once. Blocks below.
REGISTERED STRINGS: "illustrative".
EVERY OTHER CAVEAT in checks/caveats.yaml: pointer only ("§6.3", "Appendix D"), never restated. C26: any sentence about the interaction check carries "post hoc".
OWNER-PENDING:
  - V3Q10 (drop the appendix).
NOT HERE: any alive count, completion, return or comparison between the two episodes; agent numbers.
V2 MATERIAL: paper/v2/sections/14_appendix_plan_provenance.md (I).
-->

<!-- OWNER-PENDING:V3Q10 -->
<!-- default kept: this appendix stays; the alternative drops it (P2's recommendation) -->

Figures H1 and H2 show one episode of each confirmatory arm, chosen by a rule fixed before any render: θ\*, episode key 0, stochastic actions, training seed 1 at update 1000<!-- N:ENV-13 -->. Each opens at step 128 of 256<!-- N:DX-410 --><!-- N:ENV-6 -->. They are illustrative and support no comparison between the arms.

<!-- FIGURE H1: block carried from paper/v2/sections/14_appendix_plan_provenance.md:188 (markup, iframe height and alt text as v2 had them); caption replaced; the writer checks the alt text -->

<figure class="l-page">
  <iframe src="{{ 'assets/html/submission/explorer_thetastar_iso_s1_T1000_ep0.html' | relative_url }}" width="100%" height="700" style="border:none" title="Episode explorer, ISO policy, training seed 1" loading="lazy"></iframe>
  <figcaption><strong>Figure H1.</strong> One episode of the ISO policy at θ&#42;. The map shows the environment state, including the smoke field ρ. Selecting an agent shows its observation as masked by smoke (labelled “obs v3” on the figure), the true state of the same cells, and the probability τ that each cell was seen. <span class="interact">Play, step, or click an agent.</span></figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/explorer_thetastar_iso_s1_T1000_ep0_static.png" class="img-fluid" alt="Maps of one ISO-policy episode at its start, middle and end, with one agent's observation, the true state of the same cells, and the probability each cell was seen" caption="Static companion of Figure H1 for the printed PDF." %}
</div>

Figure H2 shows the JOINT policy's episode under the same rule; one episode of one seed cannot carry a contrast measured over 72 seeds per arm<!-- N:DES-3 --> and 512 evaluation episodes<!-- N:DES-13 -->.

<!-- FIGURE H2: block carried from paper/v2/sections/14_appendix_plan_provenance.md:199 (markup, iframe height and alt text as v2 had them); caption replaced; the writer checks the alt text -->

<figure class="l-page">
  <iframe src="{{ 'assets/html/submission/explorer_thetastar_joint_s1_T1000_ep0.html' | relative_url }}" width="100%" height="700" style="border:none" title="Episode explorer, JOINT policy, training seed 1" loading="lazy"></iframe>
  <figcaption><strong>Figure H2.</strong> One episode of the JOINT policy at θ&#42;, with the layers and panels of Figure H1. <span class="interact">Play, step, or click an agent.</span></figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/explorer_thetastar_joint_s1_T1000_ep0_static.png" class="img-fluid" alt="Maps of one JOINT-policy episode at its start, middle and end, with one agent's observation, the true state of the same cells, and the probability each cell was seen" caption="Static companion of Figure H2 for the printed PDF." %}
</div>
