# Provenance: sections/00_hero.md

Writer: W1. Checked against the section on 2026-10-11 (no `snapshot.sh` label
taken). The demo's hero is `paper/demo_beyond/sections/00_hero.md:3-10`.

Counts (P3's method, `plans/P3.md` §5, which counts the companion's
include caption with the figure caption): caption 83 words plus figure note
17 = **100** against the cap of 100 (`STRUCTURE.md` §8; the demo's: 152 by
the same method, `plans/P3.md` §5); reading note **43** words against ≤ 50. The figure block's markup is the
demo's, except the iframe `height`, now 1100 (the orchestrator's interim
value; the measured self-sized height is to be re-taken once the abstract
exists).

| # | sentence (verbatim) | support | change from the demo, and why |
|---|---|---|---|
| 1 | Episode explorer: one random-policy episode of CHE at the held-out configuration | ENV-13; paper/figures/interactive/MANIFEST.md:139-141 | kept (iframe `title`) |
| 2 | Figure 1. One episode of CHE. | ENV-13; decision log, OPENING AND §1 REOPENED item 2 (docs/decision_log.md:5969-5971) | kept |
| 3 | The map is environment state: fire, the smoke field ρ, weak and collapsed floor, food, agents alive and dead, and ignitions seeded by collapse. | paper/figures/interactive/MANIFEST.md:88-93; paper/figures/interactive/DESIGN.md:269-271 | edited (demo: "The map is environment state: fire, smoke field ρ, weak and collapsed floor, food, agents alive and dead, and collapse-seeded ignitions (Coupling A; here 11 collapse events, 7 seeded ignitions)."). The two counts (DX-33) are cut to meet the cap (class A, LEN); "(Coupling A)" is cut because the figure prints it (rule R3, P2-b) |
| 4 | Perception is only in the selected agent's three panels: its observation as produced (labelled obs v3, the masking observation), the true state of those cells, and P(seen) = τ, the transmittance through smoke. | paper/figures/interactive/MANIFEST.md:93-98; paper/figures/interactive/DESIGN.md:269-271; che/env/observation.py:300-303; decision log, FIGURE BATCH RULINGS C11 (docs/decision_log.md:5949-5952) | edited (demo: "Perception is only in the selected agent's three panels: its 9 × 9 observation as produced, the true state of those cells, and P(seen) = τ, the Beer–Lambert transmittance through smoke."). Added the gloss of the printed label "obs v3" (class A, F5; BRIEF §5.2); "9 × 9" and "Beer–Lambert" cut because the figure prints both (rule R3) |
| 5 | Configuration, episode key, random policy and stochastic actions were fixed before rendering. | ENV-13; paper/renders/2026-09-27/README.md:22-30 | edited (demo: "Fixed before rendering: θ&#42;, episode key 0, random policy, stochastic actions."). The selection rule stays in one clause; the values of θ\* and of the key are not repeated, because the figure prints them (rule R3) |
| 6 | Status: illustrative · random policy · grades nothing · Interact: play, scrub, jump to events, toggle layers, select an agent. | decision log, SUBMISSION FORMAT RULING constraint 2 (docs/decision_log.md:5245-5247); paper/figures/interactive/MANIFEST.md:100-104 | edited (demo: "Status: illustrative · random policy · grades nothing · Interact: play (space), scrub or step (← →), jump between events with [ and ], toggle layers, click an agent; opens paused at t = 128, agent 7."). The status is kept; the interaction is cut to 10 words (the figure prints its own key list); the default view (DX-33) is dropped, since the figure opens on it (class A, LEN; rule R1) |
| 7 | Three map frames of one random-policy episode, at its start, middle and end, showing fire state, smoke density, weak and collapsed floor, collapse-seeded ignitions, food and agents, with one selected agent's observation, the true state of the same cells, and the probability that each cell was seen. | paper/figures/interactive/MANIFEST.md:131-133 (the companion's frames and panels) | kept (companion `alt` text) |
| 8 | Static companion of Figure 1 for the printed PDF. | decision log, SUBMISSION FORMAT RULING constraint 4 (docs/decision_log.md:5251-5252) | kept (companion caption) |
| 9 | Each caption carries a status: illustrative (grades nothing); registered (read by a rule fixed before unblinding); sensitivity arm (outside the two confirmatory tests); secondary (carries no verdict); descriptive (no test); reference scale (cross-artifact), a spread measured on other runs, shown for scale only. | decision log, SUBMISSION FORMAT RULING constraint 2 (docs/decision_log.md:5245-5247); DES-12; DES-15; decision log, SECONDARY RESULT (docs/decision_log.md:5073); decision log, POST-UNBLIND STAGE RESULT (docs/decision_log.md:5172-5173); decision log, FIGURE BATCH RULINGS B9 (docs/decision_log.md:5922-5923) | new: the reading note (`STRUCTURE.md` §8 rule R4; P3-§6, one note in place of the same disclaimer on every figure). "Secondary" is glossed in plain words; "non-verdict-bearing" is left to its one use in §9.1 (BRIEF §5.3) |

## Demo sentences not carried

| # | demo text (`paper/demo_beyond/sections/00_hero.md:5`) | why |
|---|---|---|
| D1 | "Twelve agents move on a 64 × 64 grid for 256 steps at the held-out configuration θ&#42;: fire transmissibility β = 0.49, Coupling A κ<sub>A</sub> = 0.06, Coupling B κ<sub>B</sub> = 1.0, communication denial δ = 1.0." | the figure prints θ\*'s four values, the grid size, the agent count and t / 256 (its subtitle and scrubber, read this session from `explorer_thetastar_random_seed0.html`), so the caption does not repeat them (rule R3; the stub's "drops θ\*'s four values") |
| D2 | "No outcome is reported." | the status "grades nothing" says it once (LEN) |

## Alternates

- `sections/alt/00_hero.ladder.md` (Q8; P2 option B): the opening ladder as
  the hero, numbered Figure 1, with a hero-position caption and the same
  reading note. Its provenance is `provenance/00_hero.ladder.md`. The
  default is this file (the explorer, OPENING item 2).

## Open items

1. **Iframe height (class C, P2-5, Q22).** Set to 1100 on the
   orchestrator's instruction; P2 measured 1,096 at 1280 px on the demo
   page. The orchestrator re-measures it now that the abstract exists.
2. **Caption at the cap** (100 words). The two DX-33 counts (11 collapse
   events, 7 seeded ignitions) were cut to get there; they can return if
   another clause goes.
3. **Not stated, by rule:** any alive count, completion or return of this
   episode (DX-33 note); the hover readouts of ρ and τ (P2-g; Q11); the
   end-of-episode drift toward the walls (recorded, not graded; §8.5,
   §10).
4. **The figure prints "obs v3"** (glossed here once); a label rebuild is
   Q11.
