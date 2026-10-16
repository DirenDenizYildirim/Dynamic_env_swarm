# Provenance: sections/00_hero.md

Writer: W1 (Paper v3, step 4.1, 2026-10-14). Checked against the section
with `paper/v3/src/provenance_check.py --root paper/v3 --strict 00_hero`
(no snapshot label taken). "v2" is `paper/v2/sections/00_hero.md` and its
provenance `paper/v2/provenance/00_hero.md` ("v2 row n").

Counts (P3's method, which counts the companion's include caption with the
figure caption): figcaption 52 words + companion caption 8 = **60** against
the cap of 60 (STRUCTURE §3); the `interact` span, hidden in print
(`paper/v3/src/kit_styles.css:13`), adds 11 words, so 71 if it is counted.
Reading note: **30** words against ≤ 30. The figure block's markup, iframe
`height` (700), iframe `title` and companion `alt` are v2's, unchanged; the
alt text was checked against `paper/figures/interactive/MANIFEST.md:131-133`
(the companion shows the maps at t = 0, 128, 256 and the three panels).

| # | sentence (verbatim) | support | change from v2, and why |
|---|---|---|---|
| 1 | Episode explorer: one random-policy episode of CHE at the held-out configuration | ENV-13; paper/figures/interactive/MANIFEST.md:139-141 | kept (iframe `title`, v2 row 1) |
| 2 | Figure 1. One random-policy episode at the held-out configuration. | ENV-13; paper/renders/2026-09-27/README.md:22-30 (θ\* config, episode key 0, random policy, stochastic actions) | edited from v2 row 2 ("Figure 1. One episode of CHE."): says what the figure shows (V3-S4), including that the policy is random and the configuration is the held-out one, which v2 put in its selection-rule sentence |
| 3 | The map shows environment state: fire, smoke, weak and collapsed floor, food, agents and collapse-seeded ignitions. | paper/figures/interactive/MANIFEST.md:88-91 (layers); paper/figures/interactive/DESIGN.md:269-271 (state versus perception) | edited from v2 row 3 ("The map is environment state: fire, the smoke field ρ, weak and collapsed floor, food, agents alive and dead, and ignitions seeded by collapse."): shortened for the 60-word cap; the symbol ρ dropped (not defined before §3) |
| 4 | The selected agent's panels show its observation as masked by smoke (labelled “obs v3” on the figure), those cells' true state and the transmittance through smoke. | paper/figures/interactive/MANIFEST.md:92-97 (the three panels: observation as produced, state of the same cells, P(seen) = τ); che/env/observation.py:300-310; paper/v3/BRIEF.md §5.2 (obs v3 → the observation as masked by smoke) | edited from v2 row 4, which BR §8 #9 lists ("obs v3" and "masking observation" are internal names; "as produced" unclear). The printed label is now glossed once in the exempt form `labelled “TERM” on the figure` (V3-S3; `checks/terms.txt`). "Show" in place of v2's "concern perception": the true-state panel is a comparison, not perception (v2 fix RC1-9; DESIGN.md:269-271); "P(seen) = τ" dropped (τ not yet defined) |
| 5 | Play, scrub, jump between events, toggle layers or pick an agent. | paper/figures/interactive/MANIFEST.md:100-101 (controls); paper/v3/BRIEF.md §14 (interaction pointers in `<span class="interact">`, hidden in print) | edited from v2 row 6's interaction half; now in the `interact` span (BR §9: "Interact:" text in print); v2's status half ("illustrative · random policy · grades nothing") dropped: "grades nothing" is banned (`checks/terms.txt`), and the illustrative status is stated once, in the reading note (row 8; caveat C39's home) |
| 6 | Three map frames of one random-policy episode, at its start, middle and end, showing fire state, smoke density, weak and collapsed floor, collapse-seeded ignitions, food and agents, with one selected agent's observation, the true state of the same cells, and the probability that each cell was seen. | paper/figures/interactive/MANIFEST.md:131-133 | kept (companion `alt`, v2 row 7) |
| 7 | Static companion of Figure 1 for the printed PDF. | decision log, SUBMISSION FORMAT RULING constraint 4 (docs/decision_log.md:5251-5252) | kept (companion caption, v2 row 8) |
| 8 | Figure 1 is illustrative: it shows one random-policy episode, chosen by a rule fixed before rendering, to explain the environment, and no result in this paper is read from it. | ENV-13 (selection rule fixed before any render; "nothing chosen from a set"); paper/renders/2026-09-27/README.md:22-32; decision log, SUBMISSION FORMAT RULING constraint 2 (docs/decision_log.md:5245-5247: animations illustrate, never grade); DX-33 (never state this episode's alive count, completion or return) | new: the reading note (stub: one sentence on what "illustrative" means; P2 §8). Replaces v2 rows 9a–9b, the list of recurring statuses, which BR §8 #10 lists ("grades nothing", "carries no verdict", "cross-artifact" idiosyncratic). C39's home sentence (pattern "illustrative") |

## v2 sentences not carried

| # | v2 text | why |
|---|---|---|
| D1 | "The held-out configuration θ&#42;, episode key, policy and stochastic actions were fixed before rendering." (v2 row 5) | folded into the reading note (row 8: "chosen by a rule fixed before rendering") and row 2 (random policy, held-out configuration) |
| D2 | "Captions carry a status. Recurring statuses: …" (v2 rows 9a, 9b) | BR §8 #10; V3-S4 (captions say what the figure shows; no status disclaimer on every caption) |

## Findings

- **figure label, class C (V3Q8).** The figure still prints "obs v3"; it is
  glossed once here. A label-only rebuild (P2 R1) would remove the gloss.
- **caption cap, class C.** If the `interact` span counts toward the
  60-word cap, the caption is 71; the span is hidden in print, so W1
  counted it apart, like v2's figure-note span. STRUCTURE §3 does not say.
- Not stated, by rule (DX-33; stub NOT HERE): this episode's alive count,
  completion or return; its 11 collapse events and 7 seeded ignitions
  (allowed, but cut for the cap); the ρ and τ hover readouts.
