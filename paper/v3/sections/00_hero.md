<!-- PAPER V3 DRAFT (PAPER V3 ruling, 2026-10-12): builder-drafted, not owner-approved -->

<!-- FIGURE 1: block carried from paper/v2/sections/00_hero.md:16 (markup, iframe height and alt text as v2 had them); caption replaced; the writer checks the alt text -->

<figure class="l-page">
  <iframe src="{{ 'assets/html/submission/explorer_thetastar_random_seed0.html' | relative_url }}" width="100%" height="700" style="border:none" title="Episode explorer: one random-policy episode of CHE at the test configuration" loading="lazy"></iframe>
  <figcaption><strong>Figure 1.</strong> One random-policy episode at the test configuration of §6. The map shows environment state: fire, smoke, weak and collapsed floor, food, agents and collapse-seeded ignitions. One agent's panels show its observation as masked by smoke (labelled “obs v3” on the figure), those cells' true state and the smoke transmittance. <span class="interact">Play, scrub, jump between events, toggle layers or pick an agent.</span></figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/explorer_thetastar_random_seed0_static.png" class="img-fluid" alt="Three map frames of one random-policy episode, at its start, middle and end, showing fire state, smoke density, weak and collapsed floor, collapse-seeded ignitions, food and agents, with one selected agent's observation, the true state of the same cells, and the probability that each cell was seen." caption="Static companion of Figure 1 for the printed PDF." %}
</div>

Figure 1 is illustrative: it shows one random-policy episode, chosen by a rule fixed before rendering, to explain the environment, and no result in this paper is read from it.
