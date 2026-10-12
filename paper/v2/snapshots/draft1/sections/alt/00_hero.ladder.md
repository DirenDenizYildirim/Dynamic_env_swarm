<!-- PAPER V2 DRAFT (PAPER V2 ruling, 2026-10-11): builder-drafted, not owner-approved -->

<!-- STUB-SPEC
ALTERNATE FOR OWNER CHOICE Q8 (P2 section 3, option B): the opening ladder as the hero, directly under the abstract, in place of the explorer. The block below is carried from the demo's section 1 Figure 3 (sections/01_introduction.md:26-33). In the full option-B page (STRUCTURE.md section 9) this block is Figure 1, the explorer moves to the head of section 3 as Figure 3, and section 1 no longer carries the ladder; that block move and the 1 and 3 renumbering are a requested B2 build flag, not prose.
CAPTION FOR THE HERO POSITION (P2 section 3, caption obligations under option B): at most 120 words; the first line states that the figure prints rates and the text quotes points (× 100); the registered verdicts first, with "does not survive the inert-share correction" beside the gain; it cannot show Γ(t), so it carries "sign unstable over the final half" with a pointer to Figure 12; ISO-4 is a sensitivity arm outside the confirmatory family, across GPUs (the figure prints this, so the caption need not repeat it); no number the figure prints is repeated; it glosses "unit 1", "cross-unit", "rung" and "full ladder: §9.2". Required facts as for section 1's Figure 3 (RES-1, RES-2, RES-6, DES-1, DES-3, DES-13, DES-15, HW-4).
WRITER: W1. Number it Figure 1 in this file.
-->

<figure class="l-page">
  <iframe src="{{ 'assets/html/submission/opening_ladder.html' | relative_url }}" width="100%" height="427" style="border:none" title="Registered readings: Γ and Γ₄ on survival and completion" loading="lazy"></iframe>
  <figcaption><strong>Figure 1.</strong> The figure prints rates, with intervals conditional on one common evaluation draw<!-- N:DES-13 -->; the text quotes them × 100, as points. Survival: JOINT − ISO (Γ) is REJECT, and the gain does not survive the inert-share correction: JOINT − ISO-4 (Γ₄) is null. Completion: both null; Γ₄ is a second exclusion bound (X₄ is its 80 %<!-- N:METH-7 -->-power minimum detectable effect). JOINT is joint and ISO isolated training; the figure's note defines ISO-4. Unit n is GPU n; cross-unit means different GPUs. Not shown: Γ is sign unstable over the final half on both outcomes (Figure 12). The full ladder is Figure 11 (§9.2). <span class="figure-note">Status: registered for Γ · sensitivity arm for Γ₄ · Interact: none.</span></figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/opening_ladder.png" class="img-fluid" alt="Joint minus isolated training and joint minus ISO-4, for survival and completion, each with its Šidák-corrected interval and registered verdict; the survival gain is shown beside the ISO-4 contrast, labelled does not survive the inert-share correction." caption="Static companion of Figure 1 for the printed PDF." %}
</div>

Each caption carries a status: illustrative (grades nothing); registered (read by a rule fixed before unblinding); sensitivity arm (outside the two confirmatory tests); secondary (carries no verdict); descriptive (no test); reference scale (cross-artifact), a spread measured on other runs, shown for scale only.
