<!-- PAPER V3 DRAFT (PAPER V3 ruling, 2026-10-12): builder-drafted, not owner-approved -->

<!-- STUB-SPEC
JOB: The environment before any claim: one random-policy episode of CHE under the abstract (OPENING item 2), then one reading-note sentence saying what "illustrative" means.
WRITER: W1.
BUDGET: caption at most 60 words; reading note at most 30 words.
FROM: P2 §3 #1 (environment-first strengthens the v2 default); P2 §8 (the hero's limit lives in the reading note); V3-S4.
ROWS: ENV-6, ENV-13 (selection rule), DX-33 (only if a count from this episode is stated: 11 collapse events, 7 collapse-seeded ignitions).
FIGURES: Figure 1, explorer_thetastar_random_seed0.html, companion explorer_thetastar_random_seed0_static.png. Caption says what it shows: the map is environment state (fire, smoke field, weak and collapsed floor, food, agents, collapse-seeded ignitions); one selected agent's three panels are perception (its observation as masked by smoke, the true state of those cells, the transmittance). Gloss once: labelled “obs v3” on the figure. Operating instructions go in a span with class interact (hidden in print).
REGISTERED STRINGS: "illustrative" (SUBMISSION FORMAT constraint 2: animations illustrate, never grade).
CAVEATS HOMED HERE (state each in full, once; the detection pattern, from checks/caveats.yaml, must match your home sentence):
  C39 hero_illustrative: The hero episode is illustrative - one random-policy episode, selected by a fixed rule. Pattern: (?i)\billustrative\b
EVERY OTHER CAVEAT in checks/caveats.yaml: pointer only ("§6.3", "Appendix D"), never restated. C26: any sentence about the interaction check carries "post hoc".
NOT HERE: any alive count, completion or return of this episode; any comparison or effect; calling the map's smoke what agents see; the hover readouts of ρ and τ as numbers; deep links; "grades nothing" (banned).
V2 MATERIAL: paper/v2/sections/00_hero.md.
-->

<!-- FIGURE 1: block carried from paper/v2/sections/00_hero.md:16 (markup, iframe height and alt text as v2 had them); caption replaced; the writer checks the alt text -->

<figure class="l-page">
  <iframe src="{{ 'assets/html/submission/explorer_thetastar_random_seed0.html' | relative_url }}" width="100%" height="700" style="border:none" title="Episode explorer: one random-policy episode of CHE at the held-out configuration" loading="lazy"></iframe>
  <figcaption><strong>Figure 1.</strong> One random-policy episode at the held-out configuration. The map shows environment state: fire, smoke, weak and collapsed floor, food, agents and collapse-seeded ignitions. The selected agent's panels show its observation as masked by smoke (labelled “obs v3” on the figure), those cells' true state and the transmittance through smoke. <span class="interact">Play, scrub, jump between events, toggle layers or pick an agent.</span></figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/explorer_thetastar_random_seed0_static.png" class="img-fluid" alt="Three map frames of one random-policy episode, at its start, middle and end, showing fire state, smoke density, weak and collapsed floor, collapse-seeded ignitions, food and agents, with one selected agent's observation, the true state of the same cells, and the probability that each cell was seen." caption="Static companion of Figure 1 for the printed PDF." %}
</div>

Figure 1 is illustrative: it shows one random-policy episode, chosen by a rule fixed before rendering, to explain the environment, and no result in this paper is read from it.
