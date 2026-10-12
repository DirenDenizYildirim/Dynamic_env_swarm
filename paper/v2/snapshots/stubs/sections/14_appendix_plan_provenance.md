<!-- PAPER V2 DRAFT (PAPER V2 ruling, 2026-10-11): builder-drafted, not owner-approved -->

### D The frozen analysis plan

<!-- STUB-SPEC
PURPOSE: Appendices D to I. D: the frozen analysis plan, its constants and reading rules quoted verbatim with their dates (the home of the quotations; S1 to S6 stay verbatim only inside the quotation). E: the registered outcome branches. F: grid provenance (the home of the GPU blocks, the seed layout, the archives, and the blinding details section 9.1 points to). G: Γ over the final half of training (the two tables). H: the secondary design in full (arm table with the code names as labels matching Figure 13; families; mediation; what the instrument is blind to). I: two trained-policy episodes, one per confirmatory arm, shown separately (Figures I1, I2; demo Appendix J).
HEADINGS (H3, exact; ASCII, no parentheses, P2-h): D The frozen analysis plan; E The registered outcome branches; F Grid provenance; G Gamma over the final half of training; H The secondary design; I Trained-policy episodes.
WRITER: W6. BUDGET: about 850 prose words across D to I, excluding verbatim quotations and tables (STRUCTURE.md section 6); Figures I1 and I2 captions at most 60 words each.
D REQUIRED: DES-13 (the constants); the quotations of the demo's sections/12_appendix.md:104-169 (the T* ruling items 2 and 3, log:2940 entry; the falsifier, phase6_framing_branches.md:160-167; the inert-share reading rule, log:4016-4029; the High readout, same ruling; the T = 2000 rule; the mediation void rule, DX-414; the pre-unblind rulings table, DX-405, log:4913 entry; the secondary specification S1 to S6, DX-413). Trim to the rules the paper uses; never paraphrase inside a quotation; say that a "§" inside a quotation is the record's own section; keep the omission of the code version from the S-list quotation (it identifies the repository). The pre-unblind table's pipes are inside a Markdown table and in code spans: keep the demo's escaping. Design-stage power detail moved from section 9.1 (DES-4, DES-5; upper bounds; DX-404 if the t value is mentioned).
E REQUIRED: the branch table (phase6_framing_branches.md:101-104; omit the venue-lean column and say so); A_c registered 2026-09-26 before the look (DX-405, DX-102); the falsifier with its margin (RES-5); branch B's registered headline ("composition is paid in agents, not task return") "no longer holds as worded".
F REQUIRED: DX-30 (252 runs; the PRO 6000 and RTX 5090 blocks; the confirmatory directory; the secondary re-run); DES-12 (the grid window); HW-4 and DX-5 (GPU 1 to 3: Γ and every analysed secondary run on GPU 1, so Γ₄′ is same-GPU; ISO-4 and T = 2000 on GPU 2, so Γ₄ and B̂ are across GPUs; the post-unblind evaluations on GPU 3; the superseded PRO 6000 seeds enter only a descriptive diagnostic); DX-416 (shared seed integers; seed 0 reserved for floors); seed-major ordering and chunking (test_p6_grid.py, as the demo's 12:191); DX-408 (615 of 615 archive hashes matched; no hash quoted); DX-36 (the partial re-measurement of 2026-08-14, provenance only); the blinding details (DES-15's attestation, DX-411's one invocation per stage, the grid runner computing no cross-arm quantity).
G REQUIRED: the two tables of the demo's sections/12_appendix.md:199-235, unchanged in value (DX-24, DX-25, RES-1, RES-2, RES-11, RES-12, RES-13, DES-13), "sign unstable over the final half" first, descriptive at t below 1000, t below 1000 evaluated on GPU 3, the single-GPU curve with the same signs, HW-3 by pointer to section 11.
H REQUIRED: the arm table (DES-9, DX-28) with the code names as labels; the sweep means (DX-28); the estimates table (SEC-1 to SEC-6, DX-27, DX-28, SEC-3, SEC-4, RES-6, RES-7, RES-8, DX-417); the plane and the coarse linearity check (DX-39); the same-GPU replicate table (RES-8, RES-9, DX-19); arm means (DX-18); mediation VOID (SEC-7, DX-29); what the instrument is blind to (DX-306). Define μ and ν (the figure labels them m and n), the co-occurrence slope γ_p and the fire-only-share slope γ_n, the change point (knee), PAVA and OLS, here and only here. The "no-element confound" in the demo's sentence becomes the fire-only-share confound; secondary, non-verdict-bearing, 95 %, not family-corrected.
I REQUIRED: ENV-13 (the selection rule: θ*, episode key 0, stochastic actions, training seed 1 at update 1000, fixed before rendering); ENV-6; CAL-3, CA-1, CB-1, COM-6 only if the figure does not print them; DX-410 (opens at t = 128; do not state the agent numbers). Figures I1 and I2 shown separately, I1, then a sentence, then I2, never side by side (FIGURE BATCH A3), plain policy labels, "illustrative · grades nothing", no alive count, tally, completion, return or comparison; the measured contrasts are in section 9.2. Keeping this appendix is Q12.
FIGURES: Figure I1, explorer_thetastar_iso_s1_T1000_ep0.html, companion explorer_thetastar_iso_s1_T1000_ep0_static.png, height 720; Figure I2, explorer_thetastar_joint_s1_T1000_ep0.html, companion explorer_thetastar_joint_s1_T1000_ep0_static.png, height 720. Both carried below from the demo, where they were Figures J1 and J2: renumber them I1 and I2 and rewrite the captions to 60 words; gloss "obs v3".
LISTINGS: none. LATEX: none beyond inline symbols.
HONESTY LINES AND REGISTERED STRINGS: branch_B section 5 lines 8 and 9; every App. D quotation verbatim; UNDERPOWERED for both change points; VOID; "illustrative".
FIX-LIST AND FINDINGS ITEMS OWNED: F5 (the appendix pass: card, unit, codes, S-labels outside quotations, rep set, k_req); P2-h; P2-j and Q12; LEN (App. H prose halved; captions I1, I2 to 60 words; no restatement of section 9.2's readings); M1 (no prose pipe; the App. D table's pipes stay inside the table as the demo had them, and B2's table count must match).
DEMO KEEPS (sections/12_appendix.md:104-302): D's quotations, E's table, F's provenance list, the Γ(t) tables (as G), the secondary tables (as H), the two trained-policy explorers (as I). CHANGES: letters G, H, I (demo H, I, J); headings without parentheses; jargon to plain names; GPU naming; figure numbers I1, I2. DROPS: the demo's Appendix G (folded into section 11); repeated readings.
NOT HERE: unit addresses, UUIDs, hosts, commit hashes; the venue-lean column; any reinterpretation of a registered rule; any number outside the ledger and the supplement; a side-by-side ISO and JOINT view.
-->

### E The registered outcome branches

### F Grid provenance

### G Gamma over the final half of training

### H The secondary design

### I Trained-policy episodes

<!-- FIGURE BLOCK carried from demo (sections/12_appendix.md:284-291); writer checks caption against the caption rules in this stub and keeps the block self-contained -->

<figure class="l-page">
  <iframe src="{{ 'assets/html/submission/explorer_thetastar_iso_s1_T1000_ep0.html' | relative_url }}" width="100%" height="720" style="border:none" title="Episode explorer, ISO policy, training seed 1" loading="lazy"></iframe>
  <figcaption><strong>Figure J1.</strong> One pre-selected episode of the ISO policy (training seed 1, update 1000) at θ&#42; (β 0.49, κ<sub>A</sub> 0.06, κ<sub>B</sub> 1.0, δ 1.0<!-- N:CAL-3 --><!-- N:CA-1 --><!-- N:CB-1 --><!-- N:COM-6 -->), episode key 0<!-- N:ENV-13 -->, on the 64 × 64 grid with 12 agents over 256 steps<!-- N:ENV-6 -->. The map layers are the fire state, the smoke density ρ (the environment's field, not what any agent sees), weak and collapsed floor, collapse-seeded ignitions, food, and agents alive or dead. Selecting an agent shows three 9 × 9<!-- N:ENV-6 --> panels for that step: its observation as produced, the true state of the same cells, and the probability that each cell was seen, τ, the Beer–Lambert transmittance. The figure shows one episode of one training seed; it carries no alive count, completion or return, and it cannot show any difference between training protocols. Any drift towards a wall late in an episode is the known artifact of §10, not a behaviour of interest. <span class="figure-note">Status: illustrative · ISO policy, training seed 1 · grades nothing · Interact: play or pause (space), step (← →, shift for 10), scrub, change speed; jump between collapse events and seeded ignitions with [ and ]; select an agent by clicking its marker or pressing 1–9; toggle layers. Opens at t = 128<!-- N:DX-410 -->.</span></figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/explorer_thetastar_iso_s1_T1000_ep0_static.png" class="img-fluid" alt="Maps of one ISO-policy episode at its start, middle and end, with one agent's observation, the true state of the same cells, and the probability each cell was seen" caption="Static companion of Figure J1 for the printed PDF." %}
</div>

<!-- FIGURE BLOCK carried from demo (sections/12_appendix.md:295-302); writer checks caption against the caption rules in this stub and keeps the block self-contained -->

<figure class="l-page">
  <iframe src="{{ 'assets/html/submission/explorer_thetastar_joint_s1_T1000_ep0.html' | relative_url }}" width="100%" height="720" style="border:none" title="Episode explorer, JOINT policy, training seed 1" loading="lazy"></iframe>
  <figcaption><strong>Figure J2.</strong> One pre-selected episode of the JOINT policy (training seed 1, update 1000) at θ&#42; (β 0.49, κ<sub>A</sub> 0.06, κ<sub>B</sub> 1.0, δ 1.0<!-- N:CAL-3 --><!-- N:CA-1 --><!-- N:CB-1 --><!-- N:COM-6 -->), episode key 0<!-- N:ENV-13 -->, on the 64 × 64 grid with 12 agents over 256 steps<!-- N:ENV-6 -->. The layers and panels are those of Figure J1: the map's smoke layer is the environment's field ρ, and only the observation panel shows what the selected agent perceives. The figure shows one episode of one training seed; it carries no alive count, completion or return, and it cannot show any difference between training protocols. <span class="figure-note">Status: illustrative · JOINT policy, training seed 1 · grades nothing · Interact: as Figure J1 (play, step, scrub, speed; [ and ] for events; click or 1–9 for an agent; layer toggles). Opens at t = 128<!-- N:DX-410 -->.</span></figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/explorer_thetastar_joint_s1_T1000_ep0_static.png" class="img-fluid" alt="Maps of one JOINT-policy episode at its start, middle and end, with one agent's observation, the true state of the same cells, and the probability each cell was seen" caption="Static companion of Figure J2 for the printed PDF." %}
</div>
