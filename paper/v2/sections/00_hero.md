<!-- PAPER V2 DRAFT (PAPER V2 ruling, 2026-10-11): builder-drafted, not owner-approved -->

<!-- STUB-SPEC
PURPOSE: The random-policy episode explorer directly under the abstract (OPENING AND §1 REOPENED item 2): the environment before any claim, illustrative, grading nothing. Then a short reading note (STRUCTURE.md section 8, rule R4) that says once what the status labels used in every caption mean: illustrative, registered, sensitivity arm, secondary (non-verdict-bearing), descriptive, reference scale (cross-artifact).
WRITER: W1. BUDGET: caption at most 100 words including the figure note (the demo's: 147); reading note at most 50 words, one paragraph after the figure block.
FIGURE: Figure 1, explorer_thetastar_random_seed0.html, print companion explorer_thetastar_random_seed0_static.png, iframe height 720 (the demo's; P2 measured 1,096 self-sized at 1280 px: P2-5, class C, not changed). The block below is carried from the demo; rewrite its caption to the cap.
CAPTION MUST CARRY: the status "illustrative · random policy · grades nothing"; the selection rule in one clause (θ* configuration, episode key 0, random policy, stochastic actions, fixed before rendering: ENV-13); that the map is environment state, including the smoke field ρ, and only the selected agent's three panels are perception (DESIGN F1 risk 3); how to operate it in at most about 15 words. It drops θ*'s four values, which the figure prints (rule R3). It glosses "obs v3", printed on the figure, as the masking observation (BRIEF section 5.2). Any other number it keeps carries its tag (ENV-6, DX-33).
REQUIRED FACTS: ENV-6 (64 × 64 grid, 12 agents, horizon 256, 9 × 9 crop); ENV-13 (selection rule); DX-33 (11 collapse events and 7 collapse-seeded ignitions in this episode; default view t = 128, agent 7); CAL-3, CA-1, CB-1, COM-6 (θ*'s values, only if the figure does not print them).
HONESTY LINES AND REGISTERED STRINGS: "illustrative"; animations illustrate and never grade (SUBMISSION FORMAT constraint 2).
FIX-LIST AND FINDINGS ITEMS OWNED: LEN (caption); F5 (the "obs v3" gloss); P2-b (rules R1 to R3); P3-§6 (one reading note in place of the same disclaimer on every figure); Q8 (hero alternate: alt/00_hero.ladder.md); P2-g (state none of the hover readouts of ρ and τ).
DEMO KEEPS: the figure block, its alt text, the status, the selection rule, the state-versus-perception sentence. CHANGES: the caption trimmed to 100 words; θ*'s values out; the interaction list shortened. DROPS: nothing else.
NOT HERE: any alive count, completion or return of this episode (DX-33 note); any comparison; any claim that the episode shows an effect; calling the map's smoke "what agents see"; the end-of-episode drift toward walls is a known artifact, not interpreted; a deep link; the ρ and τ hover values as stated numbers.
KEEP THE BLOCK MOVABLE: no prose elsewhere may say "above" or "below" about it (the hero alternate moves it to the head of section 3).
-->

<figure class="l-page">
  <iframe src="{{ 'assets/html/submission/explorer_thetastar_random_seed0.html' | relative_url }}" width="100%" height="700" style="border:none" title="Episode explorer: one random-policy episode of CHE at the held-out configuration" loading="lazy"></iframe>
  <figcaption><strong>Figure 1.</strong> One episode of CHE. The map is environment state: fire, the smoke field ρ, weak and collapsed floor, food, agents alive and dead, and ignitions seeded by collapse. Only the selected agent's three panels concern perception: its observation as produced (labelled obs v3, the masking observation), those cells' true state, for comparison, and P(seen) = τ, the transmittance through smoke. The held-out configuration θ&#42;, episode key, policy and stochastic actions were fixed before rendering<!-- N:ENV-13 -->. <span class="figure-note">Status: illustrative · random policy · grades nothing · Interact: play, scrub, jump to events, toggle layers, pick agents.</span></figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/explorer_thetastar_random_seed0_static.png" class="img-fluid" alt="Three map frames of one random-policy episode, at its start, middle and end, showing fire state, smoke density, weak and collapsed floor, collapse-seeded ignitions, food and agents, with one selected agent's observation, the true state of the same cells, and the probability that each cell was seen." caption="Static companion of Figure 1 for the printed PDF." %}
</div>

Captions carry a status. Recurring statuses: illustrative (grades nothing); registered (read by a rule fixed before unblinding); sensitivity arm (outside the two confirmatory tests); secondary (carries no verdict); descriptive (no test); reference scale (cross-artifact), a spread measured on other runs, shown for scale only.
