# Provenance: sections/20_appendix_episodes.md

Writer: W5 (Paper v3, step 4.1, 2026-10-14). Checked with
`paper/v3/src/provenance_check.py --strict`. v2 material: App. I
(`paper/v2/sections/14_appendix_plan_provenance.md:184-205`). Kept by default; the owner may drop the appendix
(V3Q10; P2 recommends dropping it). `<!-- OWNER-PENDING:V3Q10 -->` marks it.

| # | sentence (verbatim) | support | change from v2, and why |
|---|---|---|---|
| 1 | H Trained-policy episodes | framing | edited (v2 "I Trained-policy episodes"; letter H per STRUCTURE §2) |
| 2 | Figures H1 and H2 show one episode of each confirmatory arm, chosen by a rule fixed before any render: θ\, episode key 0, stochastic actions, training seed 1 at update 1000. | ENV-13 | edited from v2 paper/v2/sections/14_appendix_plan_provenance.md:186 (Figures I1, I2 → H1, H2; "separately" dropped, since the layout keeps them apart, FIGURE BATCH A3) |
| 3 | Each opens at step 128 of 256. | DX-410; ENV-6 | kept (v2 paper/v2/sections/14_appendix_plan_provenance.md:186) |
| 4 | They are illustrative and support no comparison between the arms. | ENV-13; decision log, FIGURE BATCH RULINGS (docs/decision_log.md:5888) A3 | edited from v2 paper/v2/sections/14_appendix_plan_provenance.md:186 ("They illustrate the environment under a trained policy and grade nothing"): "grade nothing" is banned vocabulary (`checks/terms.txt`); the registered word "illustrative" kept; "cannot compare training protocols" moved here from v2's captions (V3-S4) |
| 5 | Episode explorer, ISO policy, training seed 1 | framing (iframe title) | kept (carried by the stub) |
| 6 | Figure H1. One episode of the ISO policy at θ. | ENV-13 | edited from v2 Figure I1 caption (paper/v2/sections/14_appendix_plan_provenance.md:190); renumbered |
| 7 | The map shows the environment state, including the smoke field ρ. | che/env/types.py:11, :91; paper/figures/interactive/DESIGN.md:424-427 | edited from v2 Figure I1 caption ("The map is environment state, the smoke field ρ included") |
| 8 | Selecting an agent shows its observation as masked by smoke (labelled “obs v3” on the figure), the true state of the same cells, and the probability τ that each cell was seen. | ENV-7; paper/figures/interactive/DESIGN.md:424-427 | edited from v2 Figure I1 caption: the "obs v3" gloss in the v3 form (BRIEF §5.2: "the observation as masked by smoke"); "It cannot compare training protocols" moved to the text (V3-S4) |
| 9 | Play, step, or click an agent. | framing | edited from v2's "Interact: play, step, click an agent" figure note; now inside `<span class="interact">`, hidden in print (BRIEF §14); the "Status" note dropped (V3-S4) |
| 10 | Maps of one ISO-policy episode at its start, middle and end, with one agent's observation, the true state of the same cells, and the probability each cell was seen | ENV-13 | kept (alt text carried by the stub) |
| 11 | Static companion of Figure H1 for the printed PDF. | framing | kept (renumbered by the stub) |
| 12 | Figure H2 shows the JOINT policy's episode under the same rule; one episode of one seed cannot carry a contrast measured over 72 seeds per arm and 512 evaluation episodes. | ENV-13; DES-3; DES-13 | edited from v2 paper/v2/sections/14_appendix_plan_provenance.md:197 (two sentences joined into the one sentence the stub allows between the figures; "§9.2 measures" → "measured") |
| 13 | Episode explorer, JOINT policy, training seed 1 | framing (iframe title) | kept (carried by the stub) |
| 14 | Figure H2. One episode of the JOINT policy at θ, with the layers and panels of Figure H1. | ENV-13 | edited from v2 Figure I2 caption (paper/v2/sections/14_appendix_plan_provenance.md:201): renumbered; "only the observation panel shows what the selected agent perceives" and "It cannot compare training protocols" cut (cap; V3-S4) |
| 15 | Play, step, or click an agent. | framing | edited from v2's "Interact: play, step, click an agent" figure note; now inside `<span class="interact">`, hidden in print (BRIEF §14); the "Status" note dropped (V3-S4) |
| 16 | Maps of one JOINT-policy episode at its start, middle and end, with one agent's observation, the true state of the same cells, and the probability each cell was seen | ENV-13 | kept (alt text) |
| 17 | Static companion of Figure H2 for the printed PDF. | framing | kept |

## Findings

- Word count: 77 prose words against about 80; captions 54 and 21 words.
