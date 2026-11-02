<!-- PAPER V3 DRAFT (PAPER V3 ruling, 2026-10-12): builder-drafted, not owner-approved -->

### G Trained-policy episodes

<!-- SETTLED:V3Q10 (2026-10-19, log OWNER QUESTIONS SETTLED: the default stands) -->
<!-- default kept: this appendix stays; the alternative drops it (P2's recommendation) -->

Figures G1 and G2 show one episode of each confirmatory arm, chosen by a rule fixed before any render: θ\*, episode key 0, stochastic actions, training seed 1 at update 1000<!-- N:ENV-13 -->. Each opens at step 128 of 256<!-- N:DX-410 --><!-- N:ENV-6 -->. They are illustrative and support no comparison between the arms.

<!-- FIGURE G1: block carried from paper/v2/sections/14_appendix_plan_provenance.md:188 (markup, iframe height and alt text as v2 had them); caption replaced; the writer checks the alt text -->

<figure class="l-page">
  <iframe src="{{ 'assets/html/submission/explorer_thetastar_iso_s1_T1000_ep0.html' | relative_url }}" width="100%" height="700" style="border:none" title="Episode explorer, ISO policy, training seed 1" loading="lazy"></iframe>
  <figcaption><strong>Figure G1.</strong> One episode of the ISO policy at θ&#42;. The map shows the environment state, including the smoke field ρ. Selecting an agent shows its observation as masked by smoke (labelled “obs v3” on the figure), the true state of the same cells, and the probability τ that each cell was seen. <span class="interact">Play, step, or click an agent.</span></figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/explorer_thetastar_iso_s1_T1000_ep0_static.png" class="img-fluid" alt="Maps of one ISO-policy episode at its start, middle and end, with one agent's observation, the true state of the same cells, and the probability each cell was seen" caption="Static companion of Figure G1 for the printed PDF." %}
</div>

Figure G2 shows the JOINT policy's episode under the same rule; one episode of one seed cannot carry a contrast measured over 72 seeds per arm<!-- N:DES-3 --> and 512 evaluation episodes<!-- N:DES-13 -->.

<!-- FIGURE G2: block carried from paper/v2/sections/14_appendix_plan_provenance.md:199 (markup, iframe height and alt text as v2 had them); caption replaced; the writer checks the alt text -->

<figure class="l-page">
  <iframe src="{{ 'assets/html/submission/explorer_thetastar_joint_s1_T1000_ep0.html' | relative_url }}" width="100%" height="700" style="border:none" title="Episode explorer, JOINT policy, training seed 1" loading="lazy"></iframe>
  <figcaption><strong>Figure G2.</strong> One episode of the JOINT policy at θ&#42;, with the layers and panels of Figure G1. <span class="interact">Play, step, or click an agent.</span></figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/explorer_thetastar_joint_s1_T1000_ep0_static.png" class="img-fluid" alt="Maps of one JOINT-policy episode at its start, middle and end, with one agent's observation, the true state of the same cells, and the probability each cell was seen" caption="Static companion of Figure G2 for the printed PDF." %}
</div>
