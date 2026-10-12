---
layout: distill
title: 'A pre-registered test of training on co-occurring versus isolated stressors in a multi-agent fire environment'
description: 'A pre-registered test of whether training a single policy on co-occurring stressors beats training it on each in isolation, in the Compound Hostile Environment (CHE), a multi-agent environment where a fire burns in every episode.'
date: 2026-10-11
htmlwidgets: true
authors:
  - name: Anonymous
    affiliations:
      name: Anonymous
bibliography: submission.bib
toc:
  - name: "1 Introduction"
  - name: "2 Related work"
  - name: "3 The environment"
  - name: "4 Severity calibration"
  - name: "5 Coupling A: collapse seeds the fire"
  - name: "6 Coupling B: smoke attenuates perception"
  - name: "7 Communication denial: inert under this encoder at this scale"
  - name: "8 Methodology: bars come with floors"
  - name: "9 The pre-registered compositional test"
  - name: "10 Limitations"
  - name: "11 Reproducibility"
  - name: "Appendices"
_styles: >-
  .print-companion { display: none; } @media print { .print-companion { display: block; } d-article figure iframe { display: none; } .interact { display: none; } } d-article div.highlighter-rouge pre { font-size: 12px; line-height: 1.5; white-space: pre; overflow-x: auto; } d-article div.highlighter-rouge pre code { font-size: inherit; white-space: inherit; } @media (min-width: 1000px) { d-article > div.highlighter-rouge { grid-column: page; } } @media print { d-article div.highlighter-rouge pre { white-space: pre-wrap; overflow-wrap: anywhere; overflow-x: visible; } } d-article mjx-container[display="true"] { overflow-x: auto; overflow-y: hidden; max-width: 100%; } @media print { d-article > table, d-article > span:has(> mjx-container[display="true"]), d-article > div.highlighter-rouge { grid-column: page; } d-article table { display: table; overflow: visible; width: 100%; table-layout: auto; } d-article table th, d-article table td { font-size: 10px; line-height: 1.35; padding: 1px 4px; overflow-wrap: break-word; } d-article table code { white-space: normal; overflow-wrap: anywhere; font-size: 9px; } d-article mjx-container[display="true"] { overflow: visible !important; } d-article div.highlighter-rouge pre { font-size: 9px; } } d-article iframe[src$="/explorer_thetastar_random_seed0.html"], d-article iframe[src$="/explorer_thetastar_iso_s1_T1000_ep0.html"], d-article iframe[src$="/explorer_thetastar_joint_s1_T1000_ep0.html"] { height: 1360px !important; } @media (min-width: 768px) { d-article iframe[src$="/explorer_thetastar_random_seed0.html"], d-article iframe[src$="/explorer_thetastar_iso_s1_T1000_ep0.html"], d-article iframe[src$="/explorer_thetastar_joint_s1_T1000_ep0.html"] { height: 1248px !important; } } @media (min-width: 1000px) { d-article iframe[src$="/explorer_thetastar_random_seed0.html"], d-article iframe[src$="/explorer_thetastar_iso_s1_T1000_ep0.html"], d-article iframe[src$="/explorer_thetastar_joint_s1_T1000_ep0.html"] { height: 764px !important; } } @media (min-width: 1180px) { d-article iframe[src$="/explorer_thetastar_random_seed0.html"], d-article iframe[src$="/explorer_thetastar_iso_s1_T1000_ep0.html"], d-article iframe[src$="/explorer_thetastar_joint_s1_T1000_ep0.html"] { height: 700px !important; } } d-article p.caption { font-size: 13px; line-height: 1.5; color: rgba(0, 0, 0, 0.6); } d-article table { display: block; overflow-x: auto; }
---

<!-- PAPER V2 DRAFT (PAPER V2 ruling, 2026-10-11): builder-drafted, not owner-approved -->

<!-- STUB-SPEC
PURPOSE: The abstract, as body text directly after the front matter with no heading (ABSTRACT item 2). It leads with the plain result (F2): what was tested; what happened; why the correction exists, owned as a design error; what the environment and the method contribute; then one labelled recommendation. Spine and order: STRUCTURE.md section 4.
WRITER: W1. Also yours: title and description in front_matter.yaml (B2 owns the file, you own those two fields); the disclosure d-footnote (below); alternates alt/00_abstract.disclosure_line.md and alt/00_abstract.no_recommendation.md; provenance/00_abstract.md with two extra tables, the 3 to 5 title candidates (STRUCTURE.md section 3, each with what it leads with, its length and its support) and the description (new line, support, and the owner's line at paper/finale.md:4 as the revert option).
BUDGET: at most 360 words and at most 2,600 characters, comments excluded (the owner's abstract: 359 words, 2,424 characters; venue limit 5,000, ABSTRACT item 4). No longer than the owner's.
REQUIRED FACTS, move 1 (what was tested): JOINT against ISO, one policy each; trained at β 0.43 and 0.70, evaluated at the held-out near-critical β 0.49 (CAL-3); at matched compute, T* = 1000 updates (DES-13); two co-primaries, task completion and survival, Šidák-corrected for m = 2 (DES-13); a pre-registered test (DES-12, registered 2026-08-13; the date is optional here); 72 seeds per arm (DES-3), above the registered cap of 60 (DES-1), a recorded deviation made before unblinding (DES-3). Plain words: "the registered cap of 60 seeds", never "seed ladder".
REQUIRED FACTS, move 2 (what happened, in this order): survival +0.96 points, Šidák-corrected 95 % CI [0.47, 1.44] (RES-2, DES-13); completion −1.73 points, CI [−4.12, +0.66] (RES-1), stated as an exclusion: "excludes a joint-training gain larger than 0.66 points" (RES-1; never "no effect"; do not confuse the bound with X = 3.29, the MDE in the same row); "sign unstable over the final half" on both co-primaries, verbatim (RES-11), the survival gap opening only in the last fifth (RES-12) and completion leaning negative from 70 % of the budget (RES-13); the survival gain "does not survive the inert-share correction", verbatim with "the" (UNBLIND RESULT, log:4989-4993). No sentence between the first and the last of these characterizes the gain as composition.
REQUIRED FACTS, move 3 (why the correction exists): communication denial is inert under a frozen random-projection message encoder at this scale (COM-4, ENV-12; section 7), so a third of ISO's training episodes carried no active stressor (DES-8): fire-only, not hazard-free; one plain clause owning this as a design error (BRIEF section 7; the design kept a stressor it had already found inert; identified before the grid, V6-1, and registered with its correction before unblinding, DES-15; dates optional here; never "pre-registered" for the correction); ISO-4, a 20-seed sensitivity arm outside the confirmatory family (DES-13, DES-15); ISO-4's survival is 0.98 points above ISO's (RES-7), stated as an estimate with no test, or omitted (never "raises" as a verdict, N11); JOINT minus ISO-4 is −0.03 points, CI [−0.68, +0.63] (RES-6); JOINT still sees each coupling twice as often and always in combination (DES-14). Optional: the correction excludes a large composition effect, not every one (RES-6 upper +0.63 against RES-2 lower +0.47).
REQUIRED FACTS, move 4 (what the environment and the method contribute): pure JAX, multi-agent; a cellular-automaton fire in every episode; structural collapse can add ignitions (Coupling A); smoke attenuates perception by Beer–Lambert transmittance (Coupling B); an independent communication-denial axis; the fire is an ambient hazard: no reward, cost or constraint channel reads it, and the reward reads task variables and agent deaths and prices every death the same (ENV-1, Def. 2); severity placed relative to a measured percolation threshold (CAL-1, CAL-3); each stressor is a parameter of one transition or observation kernel, so ablations are bitwise-exact nested models (N9); "we describe" a measurement protocol with reproducibility floors per metric, per GPU and per artifact (METH-1, METH-2), never "every bar is graded against a floor". Optional, if the budget allows (Q5): collapse-seeded ignitions fall 4.8-fold from low to high severity under trained policies (CA-4), a fall the random-policy calibration had already shown before any trained policy was measured (DX-9), never "as predicted before measurement" (OI-1).
REQUIRED FACTS, move 5 (default): one sentence, after everything else, labelled as a recommendation that this one environment motivates (for example, opening with "We recommend"), with no "therefore", "so" or "thus" (F4). Scope wording is the owner's (Q6). The alternate without it is alt/00_abstract.no_recommendation.md.
DISCLOSURE FOOTNOTE: one d-footnote element at the end of the abstract's first sentence (BRIEF section 12). Plain text, one or two sentences, naming the tool and not the author; no dollar sign, no math, no d-cite, no double quote, no Markdown; it lists the uses the record documents, each with a provenance row (drafting from the owner's rulings with the author checking every word, PAPER V2 item 1, log:6047-6052; the literature search and verification, DX-101 and READS RULING log:5741-5747; others only as the record documents them). It claims nothing more (not "human-sourced"). Scope is Q16; placement Q4f.
FIGURES: none. LISTINGS: none. LATEX: none needed; if any, inline only.
HONESTY LINES AND REGISTERED STRINGS: branch_B section 5 lines 1, 2 and 3 at abstract level, line 4 in substance (BRIEF section 6). Verbatim: "does not survive the inert-share correction"; "sign unstable over the final half"; "at matched compute"; "excludes a joint-training gain larger than 0.66 points" in substance; "fire-only"; "inert under a frozen random-projection encoder at this scale" (full phrase).
FIX-LIST AND FINDINGS ITEMS OWNED: F2; F3 (abstract clause); F4 (labelled sentence); OI-1; N9, N10, N11 (class B: provenance rows carry "class B, finding N" and the owner's original words from paper/finale.md:13); P1-N3; P1-b; O1; RV-R2, RV-R3, RV-R4; Q4b, Q4c, Q4d, Q4f, Q5, Q6, Q16.
MUST NOT APPEAR: "composition effect" without the qualifier; "budget-robust", "converged", "at convergence"; "no effect" for completion; "certified"; "swarm"; PBT; any untagged number; "as predicted before measurement"; "therefore" before the recommendation; "finite Dec-POMDP"; "one transition kernel"; "pre-registered" for the correction; "raises" for ISO-4 against ISO as a verdict; internal jargon (BRIEF section 5.2).
NUMBERS: every number tagged right after it, including "a third" (DES-8), "twice" (DES-14), "20" (DES-13), "72" (DES-3), "60" (DES-1), "4.8-fold" (CA-4), "70 %" (RES-13), "last fifth" (RES-12); points = rate × 100.
STYLE: plain declarative sentences of at most 40 words; no bold; no announced enumerations.
DEMO (the owner's abstract, paper/finale.md:13, carried verbatim into the demo): KEEPS its facts and tags. CHANGES: the order (F2); both registered strings verbatim; the completion exclusion bound added; ISO-4 against ISO as an estimate; the design-error clause; "transition or observation kernel"; "As predicted before measurement" removed; "therefore" removed and the advice labelled. DROPS: nothing else by necessity; the 4.8-fold sentence may move to section 1 (Q5).
NOT HERE: a heading; a figure; the dates of the F3 timeline unless the budget allows; Γ₄′; the High readout; the secondary design.
DEPENDENCIES: section 1 and section 9.2 carry the full statements; section 9.3 carries the recommendation's full form; V6-1 is written by W6 (BRIEF section 7).
-->

We report a pre-registered test of whether training one policy on co-occurring stressors beats training it on each in isolation, in the Compound Hostile Environment (CHE), a pure-JAX multi-agent environment where a cellular-automaton fire burns in every episode.<d-footnote>We used the LLM assistant Claude under our direction; its uses included drafting design documents and reviews, proposing options for our decisions, writing and running the code, analyses and figures, helping with literature search and citations, and drafting this text from our records. The authors are responsible for every word.</d-footnote> Two stressors are coupled to the fire: structural collapse can add ignitions, and smoke attenuates perception by Beer–Lambert transmittance; a third, communication denial, is independent. Joint and isolated training are run at matched compute and evaluated at a held-out near-critical severity, with task completion and survival as Šidák-corrected co-primaries. We ran 72<!-- N:DES-3 --> seeds per arm, above the registered cap of 60<!-- N:DES-1 -->, a recorded deviation made before unblinding.

Joint training raises survival by 0.96<!-- N:RES-2 --> points (Šidák-corrected 95 %<!-- N:DES-13 --> CI [+0.47, +1.44]<!-- N:RES-2 -->); completion shows no detectable change (−1.73<!-- N:RES-1 --> points, CI [−4.12, +0.66]<!-- N:RES-1 -->), which excludes a joint-training gain larger than 0.66<!-- N:RES-1 --> points. Both differences are sign unstable over the final half<!-- N:RES-11 --> of training: the survival gap opens only in the last fifth<!-- N:RES-12 -->, and completion leans negative from 70 %<!-- N:RES-13 --> of the budget. The survival gain does not survive the inert-share correction. Communication denial, inert under a frozen random-projection encoder at this scale, is the only stressor in a third<!-- N:DES-8 --> of the isolated arm's training episodes, which are thus fire-only in effect. This is our design error: we kept a stressor already found inert and did not count the fire-only share it created; found before the main training runs, the bias was registered with its correction while they ran, before unblinding. The correction is a 20<!-- N:DES-13 --><!-- N:DES-15 -->-seed sensitivity arm without those episodes, outside the two confirmatory tests; joint training's survival differs from that arm's by −0.03<!-- N:RES-6 --> points (Šidák-corrected CI [−0.68, +0.63]<!-- N:RES-6 -->), though it still sees each coupling twice<!-- N:DES-14 --> as often, always combined.

The fire is an ambient hazard that no reward, cost or constraint channel reads; the reward reads only task variables and agent deaths, pricing every death the same. Severity is set relative to a measured percolation threshold; each stressor is a parameter of one transition or observation kernel, and switching it off reproduces the nested model's trajectories bit for bit. We describe a measurement protocol with reproducibility floors per metric, per GPU and per artifact. We recommend, from this single environment, that studies of compositional generalization match the share of training with an active stressor before attributing a gain to composition.

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
  <iframe src="{{ 'assets/html/submission/explorer_thetastar_random_seed0.html' | relative_url }}" width="100%" height="1100" style="border:none" title="Episode explorer: one random-policy episode of CHE at the held-out configuration" loading="lazy"></iframe>
  <figcaption><strong>Figure 1.</strong> One episode of CHE. The map is environment state: fire, the smoke field ρ, weak and collapsed floor, food, agents alive and dead, and ignitions seeded by collapse. Only the selected agent's three panels concern perception: its observation as produced (labelled obs v3, the masking observation), those cells' true state, for comparison, and P(seen) = τ, the transmittance through smoke. The held-out configuration θ&#42;, episode key, policy and stochastic actions were fixed before rendering<!-- N:ENV-13 -->. <span class="figure-note">Status: illustrative · random policy · grades nothing · Interact: play, scrub, jump to events, toggle layers, pick agents.</span></figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/explorer_thetastar_random_seed0_static.png" class="img-fluid" alt="Three map frames of one random-policy episode, at its start, middle and end, showing fire state, smoke density, weak and collapsed floor, collapse-seeded ignitions, food and agents, with one selected agent's observation, the true state of the same cells, and the probability that each cell was seen." caption="Static companion of Figure 1 for the printed PDF." %}
</div>

Captions carry a status; the recurring ones are illustrative (grades nothing); registered (read by a rule fixed before unblinding); sensitivity arm (outside the two confirmatory tests); secondary (carries no verdict); descriptive (no test); reference scale (cross-artifact), a spread measured on other runs, shown for scale only.

<!-- PAPER V2 DRAFT (PAPER V2 ruling, 2026-10-11): builder-drafted, not owner-approved -->

## 1 Introduction

<!-- STUB-SPEC
PURPOSE: Pose the question; say why the hazard's placement keeps the comparison clean (Def. 2); introduce CHE in a paragraph; show the test and what it holds fixed (Figure 2); state both weaknesses before the result (JOINT's threefold per-coupling frequency, and the inert third owned as a design error) plus Medium siting in one clause; give the registered result with its correction (Figure 3); say what is not claimed; list three contributions (environment, calibration findings, the test), with the recommendation only as a pointer to section 9.3.
ORDER (P1 section 3; the demo's): question, hazard placement, CHE, the test (Figure 2), the weaknesses, the result and the correction (Figure 3), what is not claimed, contributions.
WRITER: W2. BUDGET: 950 prose words (the demo's: 1,391); Figure 2 caption at most 100 words, Figure 3 caption at most 120.
REQUIRED FACTS: ENV-1 (d_p = 0.5, every death priced the same); ENV-11 (one shared-parameter IPPO policy per training seed); CAL-3 (β 0.43 and 0.70 for training, 0.49 held out); DES-13 (T* = 1000 updates; Šidák m = 2; ISO-4 k = 20); DES-12 (outcome branches, framings and falsifier registered 2026-08-13, before the grid); DX-102 (a fifth outcome cell added before unblinding; Appendix E); DES-3 and DES-1 (72 seeds per arm, above the registered cap of 60, a recorded deviation before unblinding; section 9.1); DES-7 (JOINT sees each coupling three times as often as ISO); DES-9 (the sweep holds frequency at 0.5 while the fire-only share rises with co-occurrence); DES-8 (a third of ISO's episodes are δ-only, so fire-only); DES-14 (active share 2/3 for ISO, 1 for JOINT and ISO-4; JOINT sees each coupling twice as often as ISO-4); V6-1 (2026-08-16, the bias identified before the grid; W6's row) and DES-15 (registered 2026-09-18 with ISO-4, mid-grid and before unblinding); RES-2 (survival +0.96 points, Šidák-corrected 95 % CI [+0.47, +1.44]); RES-1 (completion −1.73 points, CI [−4.12, +0.66], excludes a gain larger than 0.66 points); RES-5 (the falsifier passes; verdict only, numbers in section 9.2); RES-11, RES-12, RES-13 (sign unstable over the final half; the last fifth; negative from 70 %); RES-7 (ISO-4's survival 0.98 points above ISO's, no test); RES-6 (Γ₄ −0.03 points, CI [−0.68, +0.63]); RES-8 (verdict only: a same-GPU replicate, proposed after Γ₄ was seen, agrees); CA-4 and DX-9 (contribution 2: a 4.8-fold fall, which the random-policy calibration had already shown and the Coupling-A lock had recorded before any trained policy was measured); CA-6 (the near-agent share stays flat); CB-5 (3 of 3 at High); CB-10 (masking 16 to 118 times more concentrated at moments of danger); METH-7 (80 % power at the family-corrected α).
CITATIONS: crain2008stressors, cote2016stressors, zscheischler2018compound, zscheischler2020typology (the analogy); kirk2023zsg; gao2024composition (only what the owner-read abstract supports, §1 INTRODUCTION item 2); haksar2018; garcia2015safe (READS RULING item 4 allows it here); bernstein2002 (worst-case class result only); grassberger1983, kesten1980 (Prop. 2); dewitt2020ippo; keysers2020.
FIGURES: Figure 2, composer_training_mixtures.html, companion composer_training_mixtures.png, height 430; Figure 3, opening_ladder.html, companion opening_ladder.png, height 400. Both blocks below are carried from the demo; rewrite the captions. Figure 2's caption carries none of the numbers the figure prints (the demo's had 16 tags; rule R3) and says what it cannot show (outcomes, trained behaviour, predictions). Figure 3's caption leads with the verdicts and the registered string beside the gain, states the conversion to points (the figure prints rates), says it cannot show Γ(t) (sign unstable over the final half; Figure 12), and glosses "unit 1", "cross-unit", "rung" and "full ladder: §9.2" as printed (BRIEF section 5.2). Keep both blocks self-contained and movable (the hero alternate moves Figure 3 to the hero slot).
LISTINGS: none. LATEX: none in full; name Def. 2, Prop. 1, Prop. 2, Prop. 4, Thm. 1 and Remark 2′ by number and point to sections 3 to 9.
HONESTY LINES AND REGISTERED STRINGS: branch_B section 5 lines 1, 2, 3, 7, and 6 in one clause (penalized against rewarded channel), 5 in one clause (Medium siting: Coupling B's own survival effect at the test's severity was not measurable against a three-seed spread; pointer to section 10 item 1; no number here), 4 in a clause (δ inert, so the composition tested is A × B). Verbatim: "does not survive the inert-share correction"; "sign unstable over the final half"; "at matched compute"; "sensitivity arm"; "fire-only". The founding hypothesis "did not occur". "Pre-registered" only for the 2026-08-13 test.
FIX-LIST AND FINDINGS ITEMS OWNED: F3 (two sentences owning the design error, with V6-1 and DES-15, pointing to section 9.1; no "registered as a bias"); F4 (no imperative; the confound's logic may stay with the search caveat, without "behind this result"; contribution 4's "rule" goes; at most "(§9.3)"); C2 (the clause "so we learn policies rather than plan" may stay; no "the hardness applies"; drop "With communication denied it does not reduce to a multi-agent POMDP", P3-N2); C3 (Prop. 4 by its new name in one clause: it bounds what ISO can be guaranteed to transfer, not what happens); OI-1 (contribution 2's timing); OI-2 ("a well-defined Dec-POMDP whose states reachable within the horizon form a finite set"; never "finite Dec-POMDP" alone); P1-a; P1-N3; P1-b; LEN; F5 (Γ₄ named at first use as the corrected gap, JOINT − ISO-4); P3-§2 (Medium siting clause); Q4h, Q5, Q14, Q21, Q24.
STYLE: bold only for the registered strings if at all; no "stated here before the result" or other signposting; sentences of at most 40 words; body dates only 2026-08-13, 2026-08-16, 2026-09-18 (and the grid window if needed).
DEMO KEEPS (sections/01_introduction.md): the order; Figures 2 and 3 (Γ never without Γ₄ near the opening, FIGURE BATCH A1); the corrected Prop. 1 sentence; the corrected fuel-limitation timing; the two limits of the correction in one clause pointing to section 9.2; the search caveat. CHANGES: the result paragraphs lead with the plain result; Remark 1's clause (C2); the δ paragraph becomes an owned design error with the timeline (F3); "The argument is general …" becomes the confound's logic only (F4); CB-9's number leaves contribution 2 and Medium siting becomes a limitation clause; Figure 2's caption loses its numbers. DROPS: "The fire-only third was registered as a bias"; "a rule whose argument is general"; repeated tags (the k = 72 detail, DES-14's shares beyond one sentence); figure-note boilerplate.
NOT HERE: composition effect; "composition does not matter"; budget-robust; "first" or "novel" without the search caveat; "swarm"; PBT; the founding hypothesis as partly supported; ISO-4 against ISO as significant; "exposure" for the active share; "the secondary design attributes"; the recommendation as a contribution or after "therefore".
DEPENDENCIES: section 2 relies on this section stating what the comparison holds fixed and the threefold frequency; section 9.2 delivers γ_n and where the plane fit fails (§1 INTRODUCTION item 3), and this section points there; section 10 item 1 carries Medium siting; section 9.1 carries the full F3 account; section 9.3 the recommendation. V6-1 is W6's row.
-->

When a training distribution has to cover several stressors, its designer chooses whether the policy meets them together or one at a time. Ecology studies the interactive and cumulative effects of multiple stressors <d-cite key="crain2008stressors,cote2016stressors"></d-cite>, and climate science the risk from compound events <d-cite key="zscheischler2018compound,zscheischler2020typology"></d-cite>. In reinforcement learning the choice is a question of zero-shot generalization <d-cite key="kirk2023zsg"></d-cite>: must a policy see stressors co-occur in training to cope with their co-occurrence at test time? Gao et al. (2024) <d-cite key="gao2024composition"></d-cite> studied it for imitation-learned manipulation; we study it in multi-agent reinforcement learning, for survival and task completion under a lethal fire.

Where the hazard sits in the learning problem shapes what such a comparison can teach: in some fire-related work it is the task <d-cite key="haksar2018"></d-cite>, and safe reinforcement learning typically places it in a cost or a constraint <d-cite key="garcia2015safe"></d-cite>. In the Compound Hostile Environment (CHE) the fire is an *ambient hazard* (Definition 2 in §3): a fixed stochastic process that optimizes against no one and enters no reward, cost or constraint channel. The reward reads task variables and agent deaths, and prices every death at $d_p = 0.5$<!-- N:ENV-1 -->, whatever its cause. No reward or cost signal mentions the hazard in either arm; the agents meet the fire only through what they observe and what happens to them. Proposition 1 shows that the fire, which looks like nonstationarity to any one agent, is part of the state: CHE is a well-defined Dec-POMDP whose states reachable within the horizon form a finite set (§3).

CHE is written in pure JAX, and a cellular-automaton fire burns in every episode (Figure 1). For the idealized kernel the burnt region is exactly a bond-percolation cluster (Proposition 2) <d-cite key="grassberger1983,kesten1980"></d-cite>, and the three<!-- N:CAL-3 --> severities place the fire's transmissibility β below, near and above a *measured* percolation threshold of the implemented kernel (§4). Two stressors are coupled to the fire: collapse can add ignitions (Coupling A, of strength $\kappa_A$; §5), and smoke attenuates each agent's egocentric observation by Beer–Lambert transmittance (Coupling B, $\kappa_B$; §6). A third, link denial at level δ, is independent of it (§7); $\theta = (\beta, \kappa_A, \kappa_B, \delta)$ is the environment configuration.

The training question becomes a pre-registered test of two training mixtures (Figure 2).

<figure class="l-page">
  <iframe src="{{ 'assets/html/submission/composer_training_mixtures.html' | relative_url }}" width="100%" height="442" style="border:none" title="Training mixtures of ISO, ISO-4 and JOINT by episode type" loading="lazy"></iframe>
  <figcaption><strong>Figure 2.</strong> What each arm trained on. Each bar splits one arm's training mixture into episode types: Coupling A only, Coupling B only, both together, and fire-only. Beneath each bar are each coupling's frequency (labelled “per-stressor marginal” on the figure) and the active share. ISO-4 is ISO without its δ-only components. The figure shows configured shares, read from the training configs, and cannot show outcomes, trained behaviour or predictions. <span class="figure-note">Status: configuration facts · grades nothing · Interact: count δ-only episodes as inert (default; §7) or nominally; split by β; hover a segment; table view.</span></figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/composer_training_mixtures.png" class="img-fluid" alt="Stacked bars of the three training mixtures by episode type, with each arm's per-coupling frequencies and the share of episodes that carry an active stressor." caption="Static companion of Figure 2 for the printed PDF." %}
</div>

An isolated arm (ISO) trains one policy on single-stressor configurations and a joint arm (JOINT) one on configurations with every stressor on, both at β = 0.43<!-- N:CAL-3 --> and 0.70<!-- N:CAL-3 -->. Both are evaluated at θ\*, every stressor on at the near-critical β = 0.49<!-- N:CAL-3 -->, which neither saw. Architecture, hyperparameters, evaluation draw and compute (1000<!-- N:DES-13 --> updates) are matched, with one shared-parameter IPPO policy per training seed<!-- N:ENV-11 --> <d-cite key="dewitt2020ippo"></d-cite>. The estimand is the compositional gap Γ, JOINT's mean minus ISO's at θ\*, on two co-primary outcomes, task completion and survival, Šidák-corrected for m = 2<!-- N:DES-13 --> tests. Four<!-- N:DES-12 --> outcome branches, a framing for each and a falsifier were registered on 2026-08-13<!-- N:DES-12 -->, before the grid began (a fifth<!-- N:DX-102 --> was added before unblinding, the first computation of any outcome contrast; Appendix E). We ran 72<!-- N:DES-3 --> seeds per arm, above the registered cap of 60<!-- N:DES-1 -->, a recorded deviation made before unblinding (§9.1).

JOINT sees each coupling three times<!-- N:DES-7 --> as often as ISO, so the endpoints differ in frequency as well as in co-occurrence. A secondary sweep in the spirit of DBCA <d-cite key="keysers2020"></d-cite> varies co-occurrence at fixed frequency, but its fire-only share rises with co-occurrence<!-- N:DES-9 -->, and it bears no verdict (§9.1). Communication denial is inert under our frozen message encoder at this scale (§7), so the composition tested is that of the two couplings, and the third<!-- N:DES-8 --> of ISO's training episodes that carry only δ are fire-only. ISO's *active share*, the fraction of training episodes with a behaviourally active stressor, is therefore two thirds<!-- N:DES-14 -->, and JOINT's is one<!-- N:DES-14 -->. This is an error in our design: it left δ out of the secondary sweeps because δ was inert, yet kept it in ISO's mixture, and did not count the fire-only episodes that resulted. A review of the registered design identified the bias on 2026-08-16<!-- N:V6-1 -->, before the grid; we registered it, its direction, and a correcting arm, ISO-4, with its reading rule on 2026-09-18<!-- N:DES-15 -->, mid-grid and before unblinding (§9.1). At the test's severity Coupling B was behaviourally quiet in calibration: its own survival effect was within the spread over three<!-- N:CB-9 --> seeds (§6.4), and by the project's own locks no severity has both couplings strongly live (§10).

<figure class="l-page">
  <iframe src="{{ 'assets/html/submission/opening_ladder.html' | relative_url }}" width="100%" height="427" style="border:none" title="Registered readings: Γ and Γ₄ on survival and completion" loading="lazy"></iframe>
  <figcaption><strong>Figure 3.</strong> Survival: Γ REJECT; the gain “does not survive the inert-share correction” (Γ₄ null). Completion: Γ null; Γ₄ null, a second exclusion bound. Γ is JOINT − ISO, the registered test; Γ₄, the corrected gap, is JOINT − ISO-4, where ISO-4 is a sensitivity arm outside the confirmatory family. X₄, on the completion row, is Γ₄'s minimum detectable effect at 80 %<!-- N:METH-7 --> power. The text quotes the printed rate differences × 100, as points. On the figure “unit 1” is GPU 1, “cross-unit” means across GPUs, and “full ladder: §9.2” points to Figure 11. The figure cannot show how Γ moved during training (sign unstable over the final half; Figure 12). <span class="figure-note">Status: registered for Γ · sensitivity arm for Γ₄ · Interact: none.</span></figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/opening_ladder.png" class="img-fluid" alt="Joint minus isolated training and joint minus ISO-4, for survival and completion, each with its Šidák-corrected interval and registered verdict; the survival gain is shown beside the ISO-4 contrast, labelled does not survive the inert-share correction." caption="Static companion of Figure 3 for the printed PDF." %}
</div>

At θ\*, joint training raises survival by 0.96<!-- N:RES-2 --> points (Šidák-corrected 95 %<!-- N:DES-13 --> CI [+0.47, +1.44]<!-- N:RES-2 -->; points are rate differences × 100), and the survival test rejects (Figure 3). Task completion shows no detectable change, −1.73<!-- N:RES-1 --> points (CI [−4.12, +0.66]<!-- N:RES-1 -->), which excludes a joint-training gain larger than 0.66<!-- N:RES-1 --> points. The founding hypothesis, that joint training improves both outcomes, did not occur. The falsifier registered for an asymmetric outcome passes (§9.2); under Definition 2 the asymmetry lies between a penalized channel, deaths, and a rewarded one, the task. Both co-primaries are sign unstable over the final half<!-- N:RES-11 --> of training: the survival gap opens only in the last fifth<!-- N:RES-12 --> of the budget, and completion leans negative from 70 %<!-- N:RES-13 --> of it onward (Figure 12).

The survival gain does not survive the inert-share correction. ISO-4, ISO without its δ-only components, is a sensitivity arm outside the confirmatory family, trained with 20<!-- N:DES-13 --> seeds on a second GPU<!-- N:HW-4 -->; its survival is 0.98<!-- N:RES-7 --> points above ISO's, an estimate with no registered test. The corrected gap Γ₄, JOINT − ISO-4, is −0.03<!-- N:RES-6 --> points (Šidák-corrected 95 %<!-- N:DES-13 --> CI [−0.68, +0.63]<!-- N:RES-6 -->), although JOINT still sees each coupling twice<!-- N:DES-14 --> as often as ISO-4 and always in combination. A same-GPU replicate, proposed after Γ₄ was seen, agrees. The correction excludes only a large composition effect, and ISO-4 changes the active share and each coupling's frequency together; §9.2 states both limits, what the secondary design adds and where its fit fails.

A joint-versus-isolated comparison that leaves the active share free can report an active-share effect as a composition effect (§9.3). In the search described in §2 we found no reinforcement-learning comparison that trains its isolated arm on a mixture of single stressors and matches that arm to the joint one on this share. We claim no convergence guarantee and no survival gap robust to the training budget: every comparison is at matched compute. Nor do we claim a theorem that joint training wins; Proposition 4 (§9.1), a transfer bound for a fixed policy, bounds only what isolated training can be guaranteed to transfer.

Our contributions are:

1. CHE, an environment built as an instrument, with severity by measured dynamical phase, bitwise-exact nested ablations and theory that doubles as unit tests (§3–§7).
2. Calibration findings that stand without the training comparison. Under the calibration's trained policies, collapse-seeded ignitions fall 4.8-fold<!-- N:CA-4 --> from low to high severity, a fall the random-policy calibration had already shown before any trained policy was measured (§5). Smoke costs survival at high severity, in the same direction in three of three<!-- N:CB-5 --> replicates (§6), and communication denial is inert under the frozen encoder (§7). Under the measurement protocol of §8, acceptance bars come with floors measured per metric, per GPU and per artifact, and the bars that lack one are named.
3. A pre-registered test of joint against isolated training (§9), whose survival advantage does not survive the inert-share correction, which was registered before unblinding.

<!-- PAPER V2 DRAFT (PAPER V2 ruling, 2026-10-11): builder-drafted, not owner-approved -->

## 2 Related work

<!-- STUB-SPEC
PURPOSE: For each line of work, where it places the hazard and what its comparisons hold fixed; priority to Gao et al. (2024) and to DBCA; how the search ran. Characterize a work only as RWV Part 3 and the owner's section 2 (paper/finale.md:180-370) do.
WRITER: W2. BUDGET: 1,150 prose words (the demo's: 1,536), plus Table 1.
PARAGRAPH SET (the owner's and the demo's): where the hazard enters learning (Table 1: Haksar and Schwager; JaxWildfire; safe RL; VULCAN and its unrelated "CHE" metric); a hazard that feeds on itself (Raut et al.; CHE's weak, indirect agent influence by pointer to section 5.1); perception degraded by the hazard (VULCAN, JaxWildfire; "in the search described below, we found no RL environment whose observation kernel attenuates by transmittance"); JAX simulators and benchmarks; choosing a training distribution (DR and UED; "we compare two fixed distributions and evaluate no adaptive curriculum (§10)"; ZSG); compositional generalization (Gao et al. in detail; CompoSuite; DBCA: the sweep follows it, the endpoints do not); mixed and simultaneous perturbations (Erdem and Üre in detail; Agrawal et al.; Tramèr and Boneh; Hsiung et al.); theory (Chen et al.; Pynadath and Tambe; Hu et al.); how we searched.
REQUIRED FACTS: ENV-6 (12 agents, Table 1); ENV-1 (d_p = 0.5, Table 1); DES-7 (JOINT sees each coupling three times as often as ISO, the DBCA sentence); DES-14 (twice as often as ISO-4, the Erdem and Üre sentence); DX-101 (August to October 2026, the search window); CA-8 and CA-9 only if you state the influence here instead of pointing to section 5.1, and then with the accurate range (7.4 to 8.3 % as an increase under random policies; 0.4 to 1.4 % under the trained Phase-3 policies) and its scope.
CITATIONS: haksar2018, cakir2025jaxwildfire, garcia2015safe, liu2026vulcan, raut2026psps, rutherford2024jaxmarl, dewitt2020ippo, alomari2025macraftax, hinckeldey2025assistax, hafner2022crafter, matthews2024craftax, tao2025pobax, bettini2024benchmarl, tobin2017dr, muratore2022drreview, dennis2020paired, jiang2021plr, jiang2021robustplr, parkerholder2022accel, kirk2023zsg, gao2024composition, mendez2022composuite, keysers2020, erdem2025mixed, agrawal2023multimodal, tramer2019multiple, hsiung2023compositional, chen2022understandingdr, pynadath2002, hu2025adaptablemarl. Permitted uses: BRIEF section 15.
FIGURES: none. TABLE 1: keep the demo's (sections/02_related_work.md:9-17), with the same rows; no pipe inside any cell's math.
LISTINGS: none. LATEX: none (d_p in Table 1 as inline math is fine).
HONESTY LINES AND REGISTERED STRINGS: "ambient"; hazard-blind against hazard-priced (one sentence; the home is section 3.3); "we evaluate no adaptive curriculum (§10)" (READS RULING item 4).
FIX-LIST AND FINDINGS ITEMS OWNED: OI-3 (Erdem and Üre: in each adversarially trained arm an attack is computed at every step, their Algorithm 1; six arms, one an unattacked Non-Robust baseline; never "every arm is perturbed throughout"); N15 (their Table 5: ASA-PPO at least as well as N-HYBRID-PPO in all six cells, one tie; never "do better"); OI-4 (no "about seven percent"; pointer to section 5.1 or the accurate range); RV-R1 (each sentence changed against READS RULING item 2 is flagged in provenance as "class A, OI-3 or OI-4, departs from READS RULING item 2, Q4a", with the owner's words); LEN (the Chen et al. paragraph to two or three sentences; Gao et al. and Erdem and Üre to about three each; no repeated numbers); P3-§6 (no "For each line of work, this section says" signpost); Q4a; Q23 (Pynadath and Tambe's Theorem 3 is not added unless the owner approves).
STYLE: paragraphs may open with a short plain topic sentence instead of a bold label; at most one bold run-in per paragraph if kept.
DEMO KEEPS (sections/02_related_work.md): the paragraph set, Table 1 and the search paragraph (verified twice, READS RULING). CHANGES: Erdem and Üre per OI-3 and N15; the agent-influence numbers become a pointer; Chen et al. and Gao et al. shortened. DROPS: the opening signpost; repeated numbers.
NOT HERE: any new characterization of a cited work; "first"; "no work does X" without "found by this search"; Altman or any CMDP citation; SMART; that Erdem and Üre contradict or support us (they do neither); that Chen et al. subsume Thm. 1 or that Thm. 1 extends them.
DEPENDENCIES: points to section 1 (what the comparison holds fixed; the threefold frequency), section 5.1, section 7 (Remark 2′), section 9, section 10.
-->

Table 1 sets the nearest fire-related and safety-related work beside CHE.

**Table 1.** Where the hazard enters the learning or planning problem.

| work | agents and method | where the hazard enters |
|---|---|---|
| Haksar & Schwager (2018) <d-cite key="haksar2018"></d-cite> | aerial agents fighting wildfire; multi-agent deep Q-network | **the task**: a reward for moving to burning trees on the fire's boundary (their Algorithm 2); the paper gives the fire no way to harm the agents |
| JaxWildfire (Çakır et al., 2025) <d-cite key="cakir2025jaxwildfire"></d-cite> | one air-tanker agent; JAX cellular-automaton wildfire simulator | **the reward**, hazard-priced: a per-step penalty proportional to the number of burning cells, with a bonus for full extinction; harm to the agent is not described |
| safe reinforcement learning, as García & Fernández (2015) define it <d-cite key="garcia2015safe"></d-cite> | learning policies that maximize return while ensuring reasonable system performance and/or respecting safety constraints | **a constraint or a cost**, typically |
| VULCAN (Liu & Yan, 2026) <d-cite key="liu2026vulcan"></d-cite> | a proposed approach to multi-robot fire search and rescue, planned by a vision-language model rather than learned | **a hazard cost map** that folds in smoke, heat and sensing uncertainty |
| CHE (this paper) | 12<!-- N:ENV-6 --> agents; independent PPO | **ambient**: the transition and observation kernels only; no reward, cost or constraint reads the fire, and the reward prices each death at $d_p = 0.5$<!-- N:ENV-1 -->, whatever its cause |

CHE's reward is hazard-blind, while JaxWildfire's is hazard-priced: ours prices an outcome, each death the same (Definition 2 in §3.3). VULCAN's preliminary evaluation covers baselines only, and its evaluation metric, cumulative hazard exposure, is also abbreviated CHE, unrelated to our environment's name.

Coupling A lets structural collapse add ignitions. The nearest neighbour we found is Raut et al. (2026) <d-cite key="raut2026psps"></d-cite>, who model public-safety power shutoffs as a single-agent decision problem. In it, the power flows that follow from the operator's switching decisions set the failure probability of lines in wildfire areas, which the authors treat as ignition risk. Their reward is negative operating cost, and there is no spatial spread model. CHE's agents influence the hazard too, but weakly and indirectly: an agent standing on a weak cell raises that cell's collapse rate, yet most collapses happen with no agent present (§5.1). A collapse may then seed fire, so we do not claim that CHE's hazard grows without agent influence. The difference from Raut et al. is one of directness and size: there the controlled decision sets the failure probability, while in CHE ignition is not an action available to the agents.

Coupling B attenuates each agent's observation by Beer–Lambert transmittance along the line of sight through smoke. VULCAN degrades simulated sensing with smoke density and visibility loss, and infers smoke density from image degradation and depth consistency, but it has no transmittance model. JaxWildfire's observations are partial and egocentric but not attenuated. In the search described below, we found no reinforcement-learning environment whose observation kernel attenuates by transmittance.

CHE follows JaxMARL's environment conventions <d-cite key="rutherford2024jaxmarl"></d-cite> and trains with independent PPO <d-cite key="dewitt2020ippo"></d-cite>. Among the JAX multi-agent benchmarks we surveyed, JaxMARL, Multi-Agent Craftax <d-cite key="alomari2025macraftax"></d-cite> and Assistax <d-cite key="hinckeldey2025assistax"></d-cite>, none has an evolving, spreading lethal hazard field or perception attenuated by a hazard. Multi-Agent Craftax comes closest in kind: its agents lose health to hunger and enemies and can die, but its lava is static terrain that agents cannot enter. In Crafter and in Craftax-Classic, the JAX reimplementation described alongside Craftax, lava is lethal, and Crafter and Craftax reward each health point regained and penalize each one lost <d-cite key="hafner2022crafter,matthews2024craftax"></d-cite>, pricing an outcome, as our reward does. POBAX <d-cite key="tao2025pobax"></d-cite> is a single-agent suite for partial observability, and BenchMARL <d-cite key="bettini2024benchmarl"></d-cite> a multi-agent benchmarking library built on TorchRL.

Domain randomization trains on a broad, fixed distribution over simulator parameters so that the deployed setting looks like one more sample <d-cite key="tobin2017dr,muratore2022drreview"></d-cite>. Unsupervised environment design adapts the distribution to the learner instead. PAIRED generates environments from a regret objective <d-cite key="dennis2020paired"></d-cite>; Prioritized Level Replay revisits levels by their estimated learning potential <d-cite key="jiang2021plr"></d-cite> and was later recast as environment design <d-cite key="jiang2021robustplr"></d-cite>; and ACCEL evolves levels near the frontier of the agent's ability <d-cite key="parkerholder2022accel"></d-cite>. These methods ask which distribution to train on, usually adaptively; we compare two fixed distributions and evaluate no adaptive curriculum (§10).

The closest earlier study of our question is Gao et al. (2024) <d-cite key="gao2024composition"></d-cite>. In visual imitation learning for robotic manipulation, they ask whether policies compose environmental factors, such as object type and position, table texture and height, and camera position, to succeed on unseen combinations. They compare data-collection strategies at a matched number of demonstrations, among them varying one factor at a time and cycling through factors so that more combinations appear (their §III-C and §IV-A). Policies do compose, more weakly when both factors are physical (their §V-B), and the strategy that cycles through factors is generally the most effective, which the authors hypothesize is due to the combinations it covers. Their design is built for data efficiency and does not separate co-occurrence from how often each factor value appears. CompoSuite <d-cite key="mendez2022composuite"></d-cite> studies the composition of tasks, over robots, objects, objectives and obstacles, in multi-task reinforcement learning. The DBCA method <d-cite key="keysers2020"></d-cite> builds splits whose atom distributions are similar and whose compound distributions differ. Our secondary sweep follows that idea, holding each coupling's frequency fixed while co-occurrence varies; our ISO and JOINT endpoints do not, since JOINT sees each coupling three times<!-- N:DES-7 --> as often as ISO (§1, §9.1).

Robust reinforcement learning asks the same question about perturbations. Erdem & Üre (2025) <d-cite key="erdem2025mixed"></d-cite> train single-agent continuous-control policies against a learned adversary that perturbs observations, actions, or both, and report that agents trained against one modality remain vulnerable to simultaneous attacks on both (their Tables 3–4). Under single-type attacks, agents trained against their balanced mixed adversary do at least as well as those trained against a naive one in all six cells, one a tie (their Table 5). Of their six training arms, one is an unattacked baseline; in each of the others an attack is computed at every step (their Algorithm 1). No attacked arm schedules clean steps, so none has a counterpart of the fire-only share our correction removes. No arm trains on a mixture of single-type attacks, and the mixed arms carry the combined budget, which the authors note is more severe. Their design thus bundles per-modality frequency, co-occurrence and a larger budget, which is nearer to what our corrected contrast leaves in, where JOINT still sees each coupling twice<!-- N:DES-14 --> as often as ISO-4; it neither supports nor contradicts our corrected null. Agrawal et al. (2023) <d-cite key="agrawal2023multimodal"></d-cite> train multi-agent policies against random reward, state and action noise, one or two types at a time, under a curriculum that raises the noise level and sets training length, so exposure differs between their models. In supervised vision, Tramèr & Boneh (2019) <d-cite key="tramer2019multiple"></d-cite> and Hsiung et al. (2023) <d-cite key="hsiung2023compositional"></d-cite> study robustness to multiple and to composite perturbations.

Chen et al. (2022) <d-cite key="chen2022understandingdr"></d-cite> model domain randomization as returning the optimal history-dependent policy of a latent MDP, a set of fully observed MDPs that differ in their transitions. Every upper bound they prove on its shortfall assumes each MDP is communicating, with bounded diameter. Theorem 1 (§6) is kin to the construction of their Proposition 1, in which an irreversible choice is made before anything distinguishes the candidate MDPs, but it is not covered by it. That construction obtains a shortfall growing linearly in the horizon from per-step rewards in absorbing states, while Theorem 1's two-corridor toy has a single terminal reward and can reveal the corridor before the branch. Read as a latent MDP with the signals encoded as states, the toy has an absorbing failure, so their upper bounds do not apply either. Theorem 1 also measures a different gap: the adaptive optimum against the policy optimal for a fixed map. Chen et al. therefore do not subsume Theorem 1, and Theorem 1 does not extend their bounds. Pynadath & Tambe (2002) <d-cite key="pynadath2002"></d-cite> relate the complexity of team decision problems with communication to observability. Free communication lowers the complexity when the world is collectively observable (their Theorem 4 and Table 2), and makes no difference when it is individually observable or not observable at all (their Theorems 5–6). Remark 2′ (§7) refines this for collective partial observability: communication's marginal value vanishes when interchangeable agents' views are redundant, and returns when roles are irreplaceable or deaths are costly. A survey of adaptability in multi-agent reinforcement learning (Hu et al., 2025, revised 2026) <d-cite key="hu2025adaptablemarl"></d-cite> calls an environment family highly diagnostic if it "systematically varies" factors such as population, observability or communication structure "while holding other factors fixed". It mentions compositional generalization but does not analyse shifts in several factors at once.

We ran the literature search with the help of LLM-based research assistants, between August and October 2026<!-- N:DX-101 -->. A census of benchmark venues and a search for theorems that could subsume ours came first; a search of domain randomization, environment design, multi-task and robust-learning neighbours followed. Both used web search and the arXiv API and read abstracts. The works this section describes in detail were then read in full; the remaining citations rest on their abstracts. We did not query IEEE Xplore. Wherever this paper says that no work does something, it means no work found by this search.

<!-- PAPER V2 DRAFT (PAPER V2 ruling, 2026-10-11): builder-drafted, not owner-approved -->

## 3 The environment

<!-- STUB-SPEC
PURPOSE: State CHE formally and concretely: it is a well-defined Dec-POMDP, finite on its reachable states; its reward is hazard-blind and prices deaths cause-blind; the fire is a bond-percolation process with smoke as state; every ablation is an exact nested model; and the one instance, training and metrics used in every reported experiment.
SUBSECTIONS (H3, as the demo's): 3.1 State, kernel and step order; 3.2 The fire and its smoke; 3.3 Agents, deaths and a hazard-blind reward; 3.4 Nested models: ablations are exact by construction; 3.5 The instance, training and metrics.
WRITER: W3. BUDGET: 1,600 prose words (the demo's: 2,391); Figure 4 caption at most 80 words.
REQUIRED FACTS: ENV-1 (d_p = 0.5 in every configuration reported; the code default is 0.0); ENV-2 to ENV-5 (the d_p ablation, with its scope: the fire alone with no coupling, 500 updates, 3 seeds per cell, an observation encoding that predates the current one, means over the final updates; High survival 0.575 to 0.866, High completion 0.765 to 0.821, Medium survival 0.931 to 0.951 with completion 0.750 at both, Low tied 0.991 against 0.992; never re-run); ENV-6 (64 × 64, 12 agents, horizon 256, 9 × 9 crop, 32 food items); ENV-7 (8 channels: 6 indicators, smoke, visibility; own-state row/L, col/L, alive, t/horizon); ENV-8 (5 actions); ENV-9 (+1 team reward per item); ENV-10 (the network); ENV-11 (one shared-parameter IPPO policy per seed); ENV-12 (message head: no gradient, frozen at initialization); DX-1 (σ_s 1.0, η 0.5, ι 0, held by convention); DX-2 (256 parallel environments, 128 steps per update; the rest in Appendix B); DX-3 (32,768 steps per update; 32,768,000 per run); DES-13 (T* = 1000 updates); CA-8 (an occupied weak cell collapses nine times as often; one clause, pointer to section 5.1, which holds CA-9).
CODE FACTS (read this session; cite as file:line in provenance): single ignition at a uniformly random cell at reset (che/env/env.py:241-243); one uniform per cell and incoming direction realizes Prop. 2's per-edge variables exactly (che/env/hazard.py:8-16); smoke update per cell, no smoothing (che/env/hazard.py:67-79); agent kernel in three stages, collapse-kill before moving (che/env/env.py:159-166); episodes always run to the horizon (che/env/env.py:361); observation drawn from the post-step state on its own stream (che/env/env.py:394-396); completion and survival definitions (che/env/env.py:446-447; che/eval/harness.py:42-46); the reward-independence test pins the alive transition equal (che/tests/test_reward_independence.py:6-15); the cause-blindness test (che/tests/test_lethality.py:143-162).
CITATIONS: bernstein2002 (Remark 1, worst-case class result only), grassberger1983 (Prop. 2's correspondence), cakir2025jaxwildfire (the hazard-priced foil), dewitt2020ippo, lu2022dpo, rutherford2024jaxmarl.
FIGURES: Figure 4, the static schematic fig01_schematic.png (include plus a caption paragraph), carried from the demo below. Caption at most 80 words: the five kernels in the Prop. 1 order; Coupling A from c′ − c; Coupling B from ρ′ to the observation; δ with no hazard input; observation from s′; T_X reads the post-step fields as the code does; arrow colours belong to this figure only; the reward is not drawn. Width (l-page wrapper) is P2-4, class C: keep the demo's markup.
LISTINGS (carried below, exact lines; place each where your prose introduces it; keep the header line inside the fence; the label paragraph says what it proves): Listing 1, che/env/env.py:298-358 (one step in the Prop. 1 order; the reward line reads only the task reward and the death counts); Listing 2, che/env/tasks.py:31-43 (the task reward's signature admits food and occupancy only); Listing 3, che/tests/test_coupling_b.py:131-142 (κ_B = 0 reproduces the pre-masking environment bitwise in hazard, smoke, structure, food, positions, alive flags and reward; the hand-stepped observation check at lines 143 to 156 becomes one sentence citing that range). Your prose must not echo the internal tags inside the code (M4.1, obs v2, obs v3, Q3 ruling).
LATEX: Def. 1 (two displays: the state space; the factorized kernel with T_X(x′ ∣ x, a, h′, c′)); the post-step observation inline; Def. 2's reward formula (one display, with \lvert … \rvert); the smoke update (one display); the nested-model table (math cells without pipes). No \label, \eqref, \tag or \newcommand.
HONESTY LINES AND REGISTERED STRINGS: branch_B section 5 line 6 (home: an asymmetry between survival and completion is between a penalized channel and a rewarded one); "ambient hazard"; "environment configuration"; "stressor" only for the three elements; non-adversarial is not agent-independent.
FIX-LIST AND FINDINGS ITEMS OWNED: C2 (Remark 1 says what Bernstein et al. license: finite-horizon Dec-POMDPs are NEXP-complete in the worst case, so no general exact planner is expected to scale, which is why we learn policies; the "(δ > 0) … does not reduce to a multi-agent POMDP" clause is dropped, P3-N2); OI-2 (Prop. 1 stated with a one-sentence gloss: a well-defined Dec-POMDP, finite on its states reachable within the horizon; the proof moves to Appendix A, P2-9); C1 knock-on (drop the notation note about Corollary 1's exponents at the demo's 03:28; keep one clause that an unsubscripted γ is the discount and γ_p, γ_n are section 9's slopes, if section 9 uses the symbols); KB-2 (Listing 3 shortened); LEN (clause (ii)'s agent-influence numbers become one clause and a pointer to section 5.1); F5 (no milestone codes in prose; "the observation before masking" and "the masking observation", BRIEF section 5.2); P3-§6 (no "This section states" opening); Q4k.
STYLE: definitions and propositions as bold run-in paragraphs; otherwise no bold-led paragraphs; sentences of at most 40 words.
DEMO KEEPS (sections/03_environment.md): Def. 1 with ρ and t; Def. 2 with its formula, the hazard-blind against hazard-priced note, both tests and the d_p ablation with its scope; Def. 3; Prop. 2's statement; the smoke update; the agent-kernel paragraph; the nested-model table; the engineering rule; Listings 1 to 3 (Listing 3 shortened); the instance and the metrics. CHANGES: Prop. 1's proof to Appendix A; Remark 1 (C2); the agent-influence paragraph to a pointer. DROPS: the duplicate proof; the exponent note; signposting.
NOT HERE: "no shaping term", "solely", "hazard-free reward"; that the reward-independence test proves Def. 2 (it shows no direct read, with the alive transition pinned); that the hazard is independent of the agents; PBT; "swarm"; that smoke is spatially smoothed; that the Phase-6 runs used a different observation storage; any statement of Def. 5, 6 or 7 beyond one line each (their sections own them).
DEPENDENCIES: section 4 uses Prop. 2; sections 5 to 7 define their kernels; Appendix A holds the proofs of Props. 1 and 2 and the implementation-exactness paragraph; Appendix B holds the hyperparameters.
-->

CHE is a grid world in which a team of agents forages while a fire burns; Figure 4 shows one step.

{% include figure.html path="assets/img/submission/fig01_schematic.png" class="img-fluid" alt="Five numbered boxes in a row, collapse, hazard, smoke, agents and comms, with a Coupling A arrow from collapse into the hazard box, a Coupling B arrow from smoke down to an observation box drawn from the post-step state, and comms denial entering the comms box with no hazard input." caption="Figure 4. One environment step of CHE." %}

<p class="caption">Collapse, fire, smoke, agents and communication are sampled in the order of Proposition 1. Coupling A (orange) carries c′ − c into the fire; Coupling B (blue) carries ρ′ into the observation, drawn from s′. The comms kernel takes δ and reads no hazard; T<sub>X</sub> reads the post-step h′ and c′, as in the code. Arrow colours are this figure's own. The reward is not drawn (Definition 2). <span class="figure-note">Status: schematic, no data.</span></p>

### 3.1 State, kernel and step order

**Definition 1 (Compound Hostile Environment).** A CHE is a Dec-POMDP $\mathcal{M}_\theta = \langle I, \mathcal{S}, \{\mathcal{A}_i\}, T_\theta, R, \{\Omega_i\}, O_\theta, \gamma \rangle$ with a finite set of agents $I$ on a grid $G$, action sets $\mathcal{A}_i$, observation sets $\Omega_i$, reward $R$ (Definition 2), observation kernel $O_\theta$ and discount $\gamma$. It is indexed by the *environment configuration* $\theta = (\beta, \kappa_A, \kappa_B, \delta)$: the fire's per-neighbour ignition probability $\beta$, the strengths $\kappa_A$ and $\kappa_B$ of Couplings A and B, and the communication-denial level $\delta$. Its state space factors as

$$
\mathcal{S} = \mathcal{X} \times \mathcal{H} \times \mathcal{P} \times \mathcal{C} \times \mathcal{K} \times \{0, \dots, T\},
$$

where $x \in \mathcal{X}$ holds the agents' positions $x_i \in G$, their alive flags $\alpha_i \in \{0, 1\}$ and the task state; $h \in \mathcal{H} = \{\mathrm{Fuel}, \mathrm{Burning}, \mathrm{Burnt}\}^G$ is the fire; $\rho \in \mathcal{P} = \mathbb{R}_{\ge 0}^G$ is the smoke field; $c \in \mathcal{C} = \{\mathrm{intact}, \mathrm{collapsed}\}^G$ is the structure; $k \in \mathcal{K}$ is the realized communication graph on $I$; and the last factor is the step index $t$, with horizon $T$. The transition kernel factorizes as

$$
\begin{aligned}
T_\theta(s' \mid s, a) = {} & \underbrace{T_C(c' \mid c, x)}_{\mathrm{collapse}} \; \underbrace{T_H^{\beta,\kappa_A}(h' \mid h, c, c')}_{\mathrm{fire;\ Coupling\ A}} \; \underbrace{T_\rho(\rho' \mid \rho, h')}_{\mathrm{smoke}} \\
& \times \underbrace{T_X(x' \mid x, a, h', c')}_{\mathrm{agents}} \; \underbrace{T_K^{\delta}(k' \mid x')}_{\mathrm{comms}},
\end{aligned}
$$

and agent $i$'s observation is drawn from the post-step state, $o'_i \sim O^i_{\kappa_B}(\cdot \mid x', h', \rho', c', k')$. The dependence of $T_H$ on the collapse increment $c' - c$ is Coupling A (§5); the dependence of $O^i_{\kappa_B}$ on the fire, through the smoke field $\rho'$ it produces, is Coupling B (§6). A training mixture (§9.1) draws $\theta$ once per episode, at reset. The slopes $\gamma_p$ and $\gamma_n$ (§9.2, Appendix H) are unrelated to this discount.

**Proposition 1 (Well-posedness and Markov closure).** For every $\theta$, the process $s_t = (x_t, h_t, \rho_t, c_t, k_t, t)$ under any joint policy is a Markov chain, and $\mathcal{M}_\theta$ is a well-defined Dec-POMDP: finite-horizon optimal joint policies exist, and the standard value definitions apply.

The proof (Appendix A) composes the five kernels in order. Because $\rho$ is real-valued the state space is not finite, but the states and observations reachable within the horizon form finite sets, and restricted to them $\mathcal{M}_\theta$ is a finite Dec-POMDP.

**Remark 1 (Hardness).** For two or more agents, the finite-horizon Dec-POMDP decision problem is NEXP-hard, and NEXP-complete when the horizon is below the number of states (Bernstein et al., 2002)<d-cite key="bernstein2002"></d-cite>. This bounds the worst case over the class and says nothing about a particular instance; it licenses the expectation that no general exact planner will scale, which is why we learn policies rather than plan.

Listing 1, the body of `step`, follows the factorization; the link graph is drawn on its own stream with no hazard argument, and the reward line reads only the task reward and the two death counts. In the listing, `tl` is the episode's $\theta$, and no configuration here uses the early `frozen` control branch. The observation is then drawn from the new state on its own stream (`che/env/env.py:394-396`).

**Listing 1.** One environment step in the order of Proposition 1.

<!-- LISTING: che/env/env.py:298-358 -->
```python
# che/env/env.py:298-358 (verbatim)
    k_struct, k_seed, k_fire = jax.random.split(key, 3)

    # 1. c' ~ T_C(c, x): reads *pre-step* occupancy.
    occ_pre = occupancy_grid(state.agent_pos, state.agent_alive, cfg.grid_size)
    structure_new = structure_step(
        k_struct,
        state.structure,
        state.weak,
        occ_pre.astype(jnp.float32),
        lambda_0=th.lambda_0,
        lambda_load=th.lambda_load,
    )
    collapse_increment = (structure_new == COLLAPSED) & (state.structure == INTACT)

    # 2. h' ~ T_H(h, c, c'): CA spread, then the Coupling A impulse from the
    # collapse increment (seeded cells are Burning in h', spread next step).
    seed_mask = coupling_a_seed_mask(
        k_seed, collapse_increment, kappa_A=tl.kappa_A, r_seed=th.r_seed
    )
    hazard_ca = hazard_step(k_fire, state.hazard, beta=tl.beta, iota=th.iota)
    if cfg.hazard_mode == "frozen":
        # M1.3: h is frozen — the CA/seed draws above still happen and are
        # discarded, so dynamic<->frozen with the same key share every
        # other stream bitwise (invariant #3). Frozen Burning cells stay
        # Burning: lethal and smoke-emitting, but never spread or burn out.
        hazard_new = state.hazard
        seeded_ignitions = jnp.zeros_like(seed_mask)
    else:
        hazard_new = seed_ignitions(hazard_ca, seed_mask)
        seeded_ignitions = hazard_ca != hazard_new  # Fuel cells Coupling A lit

    # 3. rho' from h' (Def. 6; smoke outlives flame).
    smoke_new = smoke_step(state.smoke, hazard_new, sigma_s=th.sigma_s, eta=th.eta)

    # 4. x' ~ T_X + task dynamics. M1.1: lethality/blocking against h'/c'.
    # DECISION: an agent disabled this step does not collect food this step
    # (it died before/on arrival) — occupancy filters on the post-death
    # alive vector, keeping "dead agents never collect" exact.
    pos_new, alive_new, deaths_fire, deaths_collapse, blocked_moves = agent_step(
        state.agent_pos,
        state.agent_alive,
        actions,
        hazard_new,
        structure_new,
        collapse_increment,
        cfg.grid_size,
    )
    occ_post = occupancy_grid(pos_new, alive_new, cfg.grid_size)
    food_new, task_reward = task_step(state.food, occ_post)
    # Def.-2-compliant death penalty: reads only the alpha transition (an X
    # variable) — never hazard/smoke/structure directly.
    reward = task_reward - th.death_penalty * (deaths_fire + deaths_collapse).astype(
        jnp.float32
    )

    # 5. k' ~ T_K(x'): comms channel (Def. 7, M5.0). Reads post-step
    # positions/aliveness only — never h', rho' or c' — and draws from its
    # own fold_in stream, so delta cannot perturb any kernel above.
    links, links_in_range = _comms_obs(
        jax.random.fold_in(key, _COMMS_STREAM), pos_new, alive_new, cfg, tl.delta
    )
```

### 3.2 The fire and its smoke

**Definition 3 (Fire kernel).** Each cell is Fuel, Burning or Burnt. At each step, independently for each ordered pair of a Burning cell $g$ and a Fuel von Neumann neighbour $g' \in N(g)$, the cell $g'$ ignites with probability $\beta$. A Burning cell becomes Burnt after exactly one step, and Burnt is absorbing. Fuel cells may also ignite spontaneously at rate $\iota \ge 0$ per step; CHE uses $\iota = 0$<!-- N:DX-1 -->.

Every episode starts from an all-Fuel grid with one<!-- N:V3-1 --> Burning cell at a uniformly random position (`che/env/env.py:241-243`). One uniform per cell and incoming direction realizes the per-edge Bernoulli variables of Proposition 2's coupling exactly (`che/env/hazard.py:8-16`; Appendix A), and cells outside the arena never burn.

**Proposition 2 (Bond percolation).** Under Definition 3 with $\iota = 0$ and a single ignition at the origin, the set of eventually-Burnt cells is equal in distribution to the open cluster of the origin in i.i.d. bond percolation on $(G, E)$ with edge-open probability $\beta$.

Here $E$ is the arena's set of von Neumann edges. The proof (Appendix A) is a short coupling, the correspondence between an epidemic with a constant infectious period and bond percolation described by Grassberger (1983)<d-cite key="grassberger1983"></d-cite>. Its hypotheses hold for CHE's fire when Coupling A is off, since collapses otherwise add ignitions.

Smoke outlives flame. Per cell,

$$
\rho' = e^{-\eta}\rho + \sigma_s \mathbf{1}[h' = \mathrm{Burning}],
$$

with emission $\sigma_s = 1.0$ and decay $\eta = 0.5$, held fixed by convention and never calibrated<!-- N:DX-1 -->. A cell emits $\sigma_s$ once, in the step it burns, and its smoke then decays geometrically, with no spatial smoothing (`che/env/hazard.py:67-79`).

### 3.3 Agents, deaths and a hazard-blind reward

The agents kernel $T_X(x' \mid x, a, h', c')$ acts in three deterministic stages that consume no random numbers (`che/env/env.py:159-173`). An alive agent on a cell that collapses in this step is disabled before it moves. Survivors take one of 5<!-- N:ENV-8 --> actions, stay or a von Neumann move clipped to the grid, and a move into a collapsed cell is cancelled. An agent whose new cell is Burning in $h'$ is then disabled, so a cell igniting under a standing agent kills it; Burning cells can be entered, and avoidance must be learned. A disabled agent stays disabled, holds still, collects nothing and disappears from the others' observations.

**Definition 2 (Ambient hazard).** The hazard is *ambient* if and only if (i) and (ii) hold.

(i) *Reward independence:* the reward is a function of task variables and of the agents' alive transition only,

$$
\begin{aligned}
R(s,a,s') = {} & R_{\mathrm{task}}(\mathrm{task}(x), a, \mathrm{task}(x')) \\
& - d_p\,\lvert\{i : \alpha_i = 1,\ \alpha'_i = 0\}\rvert ,
\end{aligned}
$$

where $\mathrm{task}(x)$ denotes the task variables (in CHE, the food grid and the alive agents' positions) and $d_p \ge 0$ is a fixed death penalty. No term of $R$ references $h$, $\rho$ or $c$, and the hazard appears in no auxiliary cost or constraint channel: no CMDP constraint, no Lagrangian penalty, no safety critic.

(ii) *Non-adversarial:* $T_H$ is a fixed stochastic kernel; nothing in the environment optimizes, learns or best-responds.

Under clause (i), survival is learned through two hazard-blind routes: a dead agent collects no further task reward, and each death costs a fixed $d_p = 0.5$<!-- N:ENV-1 -->, whatever its cause, in every configuration reported here except the $d_p$ ablation below (the code's default is 0<!-- N:ENV-1 -->). Fire and collapse reach return only through the transition and observation kernels. A hazard-priced reward signals the hazard's state whether or not anything is harmed: JaxWildfire, for example, penalizes its agent at every step in proportion to the number of burning cells (Çakır et al., 2025)<d-cite key="cakir2025jaxwildfire"></d-cite>. At $d_p = 0$ only the first route would remain.

Listing 2's signature admits only the food and occupancy grids: no fire, smoke or structure argument can reach the task reward.

**Listing 2.** The task reward reads food and occupancy only.

<!-- LISTING: che/env/tasks.py:31-43 -->
```python
# che/env/tasks.py:31-43 (verbatim)
def task_step(food: jax.Array, occupancy: jax.Array) -> tuple[jax.Array, jax.Array]:
    """Collection: an occupied food cell yields +1 team reward and empties.

    Multiple agents on one food cell still collect a single item (+1).
    Returns (food', team_reward). Reads task variables and agent occupancy
    only — no hazard/smoke/structure arguments, by design (Def. 2).
    """
    chex.assert_type(food, jnp.uint8)
    chex.assert_equal_shape([food, occupancy])
    collected = (food == 1) & occupancy
    reward = collected.sum().astype(jnp.float32)
    food_new = jnp.where(collected, jnp.uint8(0), food).astype(jnp.uint8)
    return food_new, reward
```

One test of clause (i) asserts identical rewards, with and without the death penalty, for states that differ only in fire, smoke or structure; fire and structure differ only far from every agent, which pins the alive transition equal (`che/tests/test_reward_independence.py:6-15`). It shows only that the reward reads no hazard state directly, since the fire is meant to change return through deaths. The other kills a standing agent by fire and, separately, by collapse, with identical task state, and asserts a reward of $-d_p$ both times (`che/tests/test_lethality.py:143-162`).

Clause (i) also fixes how §9's two co-primary outcomes enter learning: survival is a penalized channel, each death costing $d_p$, and completion a rewarded one, each collected item earning +1<!-- N:ENV-9 -->. §9.2 reads any asymmetry between them as one between a penalized channel and a rewarded one.

The one ablation of $d_p$ is from the calibration phase, with this scope: the fire alone with no coupling on, 500 updates<!-- N:ENV-2 -->, 3 seeds per cell<!-- N:ENV-2 -->, an observation encoding that predates the one used here, and means over the final training updates. Raising $d_p$ from 0<!-- N:ENV-2 --> to 0.5<!-- N:ENV-1 --> moved High survival from 0.575 to 0.866<!-- N:ENV-2 --> and High completion from 0.765 to 0.821<!-- N:ENV-3 -->, moved Medium survival from 0.931 to 0.951 with completion 0.750 at both<!-- N:ENV-4 -->, and left Low tied, 0.991 against 0.992<!-- N:ENV-5 -->. It was not re-run under the current observation or with the couplings.

Clause (ii) does not make the hazard independent of the agents: a weak cell with an agent on it is nine<!-- N:CA-8 --> times as likely to collapse in a step as an empty one, and a collapse can seed fire (§5.1).

### 3.4 Nested models: ablations are exact by construction

Each stressor is a parameter of one transition or observation kernel, and setting it to zero recovers a nested special case of the same model.

| stressor | parameter | lives in | off ($=0$) recovers | test (`che/tests/`) |
|---|---|---|---|---|
| Coupling A (§5) | $\kappa_A$ | $T_H$, through $c' - c$ | a fire blind to the structure | `test_nesting.py` |
| Coupling B (§6) | $\kappa_B$ | $O^i$ | the pre-masking observation, plus an all-ones visibility plane | Listing 3 |
| communication denial (§7) | $\delta$ | $T_K$ | free, range-limited communication | `test_comms.py` |

The fire's $\beta$ is a parameter of the same kind, positive in every configuration and set by severity (§4).

One engineering rule makes the nesting exact: every stochastic branch draws its uniforms unconditionally and compares them against a probability that may be zero. The draws for Coupling B's reveal, the links and the per-episode mixture use streams derived from the reset or step key by a fixed tag, so adding them left the existing streams untouched. Setting a stressor to zero therefore changes comparisons only, and the same keys reproduce the nested model's trajectory bit for bit.

Listing 3 runs the environment at $\kappa_B = 0$ with and without masking, under the same keys, and asserts bitwise-identical fire, smoke, structure, food, positions, alive flags and rewards. The rest of the test (`che/tests/test_coupling_b.py:143-156`) steps both by hand and asserts identical content planes, an all-ones visibility plane and a zero masked share.

**Listing 3.** With $\kappa_B = 0$, trajectories and rewards are bitwise those of the environment before masking.

<!-- LISTING: che/tests/test_coupling_b.py:131-142 -->
```python
# che/tests/test_coupling_b.py:131-142 (verbatim)
def test_kappa_b_zero_bitwise_recovers_obs_v2():
    """Nesting (M4.1): obs v3 at kappa_B = 0 is the pre-masking env plus a
    constant all-ones visibility plane — state trajectories, rewards, and
    content planes bitwise identical to obs v2 under the same keys."""
    theta = dataclasses.replace(_HOT, kappa_B=0.0)
    cfg3 = EnvConfig(grid_size=L, n_agents=4, horizon=64, theta=theta)
    cfg2 = dataclasses.replace(cfg3, obs_version=2)
    a = _traj(theta, cfg=cfg3)
    b = _traj(theta, cfg=cfg2)
    _assert_bitwise_equal(
        a, b, ("hazard", "smoke", "structure", "food", "pos", "alive", "reward")
    )
```

With $\kappa_A = 0$, collapse activity leaves the fire and smoke bitwise unchanged (`che/tests/test_nesting.py:78-88`); at $\delta = 0$, the environment reproduces, on the CPU, a trajectory digest recorded before the communication channel existed (`che/tests/test_comms.py:272-319`). A structural test also asserts that the traced computation keeps its random-number primitives at parameter value zero, catching a gate such as `if kappa_A > 0:` that behavioural tests miss (`che/tests/test_nesting.py:222-240`).

### 3.5 The instance, training and metrics

Every trained policy and evaluation in this paper uses one instance: a 64 × 64 grid, 12 agents, a horizon of 256 steps, a 9 × 9 egocentric crop and 32 food items<!-- N:ENV-6 -->. Food sits on distinct cells from reset and does not respawn, and an alive agent on a food cell collects it for a team reward of +1<!-- N:ENV-9 -->. The observation's 8 channels<!-- N:ENV-7 --> are six<!-- N:ENV-7 --> indicators (burning, burnt, food, weak, collapsed, alive occupancy), the raw smoke density and Coupling B's visibility plane, which marks the revealed cells. An own-state vector gives the agent's row and column divided by the grid side, its alive flag and $t$ over the horizon<!-- N:ENV-7 -->.

All agents share one actor-critic network over the crop, the own-state vector and the aggregate of delivered messages. It has two convolutions with 16 and 32 channels, a dense layer of 128 units, and separate actor and critic heads with a 64-unit layer each<!-- N:ENV-10 -->. A message head receives no gradient; what it emits is a frozen-at-initialization projection of trained trunk features (§7).

Training is the independent PPO of de Witt et al. (2020)<d-cite key="dewitt2020ippo"></d-cite>, in the PureJaxRL style of Lu et al. (2022)<d-cite key="lu2022dpo"></d-cite>, on the environment conventions of JaxMARL (Rutherford et al., 2024)<d-cite key="rutherford2024jaxmarl"></d-cite>. Each seed trains one shared-parameter policy<!-- N:ENV-11 -->, whose update takes each agent's transitions as separate samples under the team reward. Each update collects 128 steps from 256 parallel environments<!-- N:DX-2 -->, 32,768 environment steps<!-- N:DX-3 -->, each advancing all 12 agents<!-- N:ENV-6 -->. ISO, ISO-4 and JOINT (§9) each train for T\* = 1000 updates<!-- N:DES-13 -->, or 32,768,000 environment steps<!-- N:DX-3 -->, with the hyperparameters of Appendix B.

The co-primary outcomes of §9 are per-episode. *Completion* is $1 - F/32$<!-- N:ENV-6 -->, where $F$ is the number of food items left at the episode's last step; *survival rate* is the fraction of the 12 agents<!-- N:ENV-6 --> alive at the end. Episodes always run to the horizon, even when every agent has died (`che/env/env.py:361`; `che/eval/harness.py:44-45`). Deaths are also recorded by cause, as diagnostics.

<!-- PAPER V2 DRAFT (PAPER V2 ruling, 2026-10-11): builder-drafted, not owner-approved -->

## 4 Severity calibration

<!-- STUB-SPEC
PURPOSE: Severity in CHE is a measured dynamical phase of the fire, placed below, near and above the implemented kernel's measured transition, not a value of β chosen by hand. Corollary 1 at the level verified sources support; Def. 4 with its operational definition by locked observable bands; the measured threshold with its provenance stated honestly; the locked levels; the re-test that refuted Def. 4's Medium prediction for survival.
SUBSECTIONS (H3, as the demo's): 4.1 Phase structure of the idealized kernel; 4.2 Severity as phase; 4.3 Measuring the threshold and locking the levels; 4.4 Re-testing the Medium prediction.
WRITER: W3. Also alt/04_severity.no_item4.md (Corollary 1 without item 4). BUDGET: 700 prose words (the demo's: 998), plus the levels table; Figure 5 caption at most 120 words.
COROLLARY 1 (C1, as the orchestrator directed; C1_verification.md): item 1, β_c = 1/2 exactly for bond percolation on the square lattice (kesten1980, at the level of its title; B2 records the support quote, N15). Item 2 (subcritical) only at the level a verified source supports: by default keep only what B2's support record for kesten1980 covers; the exponential-tails clause goes (N7); if nothing beyond the title is covered, cut item 2 and define χ (mean cluster size) and ξ (correlation length) where Def. 4 and Prop. 3 use them, without claiming their finiteness. Item 3 is dropped, with every 43/18 and 4/3. Item 4 at the verified level with garet2004chemical (Corollary 5.4, p. 188): above β_c the fire spreads indefinitely with positive probability, and, conditioned on that, the region burnt by step n, rescaled by n, converges in Hausdorff distance to a deterministic convex compact set; the speed depends on direction; on ℤ² only; never "an asymptotic front speed v(β)" as one scalar. The alternate file drops item 4 (Q4g). The caveat paragraph: keep that exactness belongs to the idealized kernel on the infinite lattice and that the implemented kernel's threshold is measured (section 4.3); cut the claim that the transition and the divergence of χ and ξ "are universal" (uncited, N7); cut the sentence about the exponents' regime being out of reach (it goes with item 3).
DEF. 4: the theory doc's definition in substance (Low ξ ≪ L, Medium ξ ~ L, High a front at a speed comparable to the agents'), plus one clause that the levels were locked by observable bands (DX-201). Its expectation that Medium outcomes vary most is a prediction, not part of the definition, and section 4.4 reports its test (the demo already separates them). The wording of "three qualitatively different phases" and "fluctuations are maximal" is Q23 (N8, P3-N8, class C): keep the theory doc's terms, but say no more than they do.
REQUIRED FACTS: CAL-1 (the lock record's β̂_c = 0.500 ± 0.005, from R_L logistic centres 0.4985 / 0.5006 / 0.4999; O-2: no committed script produces the centres; say so); the CAL-1 note and DX-204 (committed estimators: pairwise crossing mean 0.504, spread [0.480, 0.513], consensus 0.499; they bracket ½, which validates the port and is not a finding); CAL-2 (self-duality 0.488 / 0.502 / 0.494, same caveat); CAL-3 (levels and their P_span and burnt fractions: Low 0.43, 0.021, 1.9 %; Medium 0.49, 0.547, 19.8 %; High 0.70, 0.998, 98.3 %); CAL-4 (β_c(64) ≈ 0.486); DX-6 (High front speed 0.83 cells per step, 83 % of the agents' speed); DX-7 (512 seeds per point, L in {32, 48, 64}, 35 β values, T_max = 4L, centre ignition; the crossing sweep); DX-201 (the bands); DX-203 (the re-test's provenance: the fire-only probe re-run, 500 updates, three seeds, 512 episodes, equivalent and not bitwise identical); CAL-5 (survival refuted: fixed-policy variance 0.00091 / 0.00709 / 0.00885); DX-8 (completion Medium ≈ Low, 0.01245 against 0.01235; burnt-fraction variance peaks near β ≈ 0.53); ENV-1, ENV-6; for Figure 5's caption CA-1, CB-1, DX-202 (δ 0 in the severity configurations; episode key 0).
CITATIONS: kesten1980; garet2004chemical (only for item 4; it exists once B2 enters it through RWV).
FIGURES: Figure 5, severity_explorer.html, companion severity_explorer.png, height 520, carried below. Caption at most 120 words; it states δ 0 in words, because the printed companion's subtitle is cut before "δ 0" (P2-1); it says the figure shows no R_L centre and no β̂_c band; renders are illustrative, one episode each.
LISTINGS: none. LATEX: Corollary 1 as a numbered list; Def. 4 as a short list; the levels table (no pipes in math). The slow CPU test that checks the sigmoid and a band around ½ may be cited by path (che/tests/test_percolation.py).
HONESTY LINES AND REGISTERED STRINGS: "illustrative" for the renders; the Kesten agreement validates the implementation, it is not a finding about fire; the Medium prediction is refuted for survival, for these fire-only policies at this budget (CAL-5 scope: M3.0, survival only).
FIX-LIST AND FINDINGS ITEMS OWNED: C1; N7; P3-N4; N8 and P3-N8 (class C: keep the terms); P2-1; P3-A3 (class C: keep the demo's order, lock value with provenance first, Q19); LEN (section 4.4's account of the mismatch to one sentence, labelled as the re-test report's account); F5 (M3.0 named as "the re-test at fixed policy"); Q4g, Q19, Q23.
DEMO KEEPS (sections/04_severity.md): Figure 5; section 4.3's measurement and its provenance; the levels table; section 4.4's three-part outcome. CHANGES: Corollary 1 per C1 and N7; the caveat paragraph; Def. 4 gains the bands clause; section 4.4's account paragraph to one sentence. DROPS: 43/18, 4/3 and "∼"; the exponent-regime sentence; the universality claim.
NOT HERE: that CHE reproduces Kesten's value as a finding; that β̂_c comes from a committed script; "maximal unpredictability at Medium" as a property; that Medium is where policies vary most; any critical exponent; any cited claim beyond what kesten1980 and garet2004chemical support at their recorded level.
DEPENDENCIES: section 3 (Prop. 2); section 5.2 (Prop. 3 uses χ); section 9.1 (θ* at Medium); section 10 items 1, 2 and 10.
-->

Severity in CHE is placed by a measured dynamical phase of the fire: the three<!-- N:CAL-3 --> levels sit below, near and above the implemented kernel's measured transition (Figure 5).

<figure class="l-page">
  <iframe src="{{ 'assets/html/submission/severity_explorer.html' | relative_url }}" width="100%" height="528" style="border:none" title="Severity explorer: spanning probability against ignition probability, and one fire at each locked level" loading="lazy"></iframe>
  <figcaption><strong>Figure 5.</strong> Severity as a measured phase. Left: the spanning probability, the chance that one centre ignition reaches the arena boundary, against β on an all-fuel grid with no agents, for three arena sides (512 seeds per point<!-- N:DX-7 -->). Vertical rules mark the locked levels; the triangle marks the largest arena's pseudo-critical point. Right: one random-policy episode per level under the severity configurations, with δ 0<!-- N:DX-202 -->; only the fire and its smoke (hatching) are drawn. Neither the R<sub>L</sub> curves nor the locked critical point β̂<sub>c</sub> is shown (§4.3). <span class="figure-note">Status: calibration, no agents (curves) · illustrative, one episode each (renders) · Interact: play or drag the time slider; click a panel.</span></figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/severity_explorer.png" class="img-fluid" alt="Spanning probability of a centre ignition against ignition probability for three grid sizes, with the three locked severities marked, beside one illustrative fire episode at each severity." caption="Static companion of Figure 5 for the printed PDF." %}
</div>

### 4.1 Phase structure of the idealized kernel

**Corollary 1 (Phase structure).** On $\mathbb{Z}^2$ with the von Neumann neighbourhood, the fire of Definition 3 with $\iota = 0$ and a single ignition at the origin inherits the phase structure of bond percolation (Proposition 2, whose coupling holds on any graph):

1. Its critical point is $\beta_c = 1/2$ exactly, the critical probability of bond percolation on the square lattice (Kesten, 1980)<d-cite key="kesten1980"></d-cite>.
2. For $\beta > \beta_c$ the fire spreads indefinitely with positive probability. On that event the cells ignited by step $n$ are those within $n$ open edges of the origin. Scaled by $1/n$, they converge almost surely in Hausdorff distance to a deterministic convex compact set with non-empty interior, invariant under permutations and reflections of the coordinates (Garet & Marchand, 2004; their Corollary 5.4)<d-cite key="garet2004chemical"></d-cite>. The growth is therefore linear in $n$, at a speed given in each direction by the extent of that set.

Both items concern the idealized kernel (von Neumann neighbourhood, constant burn time, homogeneous fuel, no wind) on the infinite lattice. CHE's fire is that kernel on a finite arena, with ignitions added by Coupling A (§5.1), so the levels are placed against a measured finite-size threshold and, at High, a measured front speed (§4.3).

### 4.2 Severity as phase

**Definition 4 (Severity regimes).** Fix the arena side $L$. Severity levels are defined by the position of the implemented kernel relative to its measured critical point $\hat\beta_c$, through the correlation length $\xi(\beta)$, the typical extent of a fire cluster:

- *Low*, subcritical, $\xi(\beta) \ll L$: fire clusters are local and short-lived, and survival is a local-avoidance problem.
- *Medium*, near-critical, $\xi(\beta) \sim L$: cluster sizes are scale-free up to the arena's size, fluctuations are maximal, and a single ignition can, with non-negligible probability, cascade to arena scale; survival is a global-anticipation problem.
- *High*, supercritical: fire fronts move at a speed comparable to the agents', and survival is a race.

The correlation length motivates the levels; operationally, each level is the observable band it was locked to, that is, fixed on 2026-07-19<!-- N:DX-401 -->, before the main experiment (§4.3). As qualitatively different phases of one kernel, the levels make training at Low and High and evaluating at Medium (§9.1) a test of transfer to a phase neither arm trained in, though in the scalar $\beta$ it remains an interpolation (§10). Definition 4 also carried an expectation, on record before its test (§4.4), that per-episode outcome variance would peak at Medium.

### 4.3 Measuring the threshold and locking the levels

The calibration ran the fire alone on an all-Fuel grid at $L \in \{32, 48, 64\}$<!-- N:DX-7 -->, with 512 seeds per $(L, \beta)$<!-- N:DX-7 -->. A span sweep over 35<!-- N:DX-7 --> values of $\beta$ (0.05 to 0.95 coarsely, 0.40 to 0.60 in steps of 0.01<!-- N:DX-7 -->), each from one centre ignition for $T_{\max} = 4L$ steps<!-- N:DX-7 -->, measured $P_{\mathrm{span}}$, the burnt fraction and the front speed. A crossing sweep ignited the full left column and recorded the left–right crossing probability $R_L(\beta)$.

The severity lock fixed $\hat\beta_c = 0.500 \pm 0.005$<!-- N:CAL-1 -->, from logistic fits to $R_L$ with centres 0.4985, 0.5006 and 0.4999 at $L = 32, 48, 64$<!-- N:CAL-1 -->, and a self-duality check $R_L(0.500) = 0.488, 0.502, 0.494$<!-- N:CAL-2 -->. The lock record states that they were recomputed independently from the committed raw data; no committed script or artifact produces the logistic centres. Among the committed estimators, pairwise crossings of $R_L$ average 0.504<!-- N:CAL-1 -->; the family spans [0.480, 0.513]<!-- N:DX-204 -->, with consensus mean 0.499<!-- N:CAL-1 -->. Their range brackets Kesten's ½. That agreement validates the implementation; it is not a finding about fire, since Proposition 2 and Corollary 1 predict it for this kernel.

Each level was then locked to an observable band, with its measured values ($L = 64$<!-- N:DX-7 -->, 512 seeds<!-- N:DX-7 -->, no agents):

| level | $\beta$ | phase | $P_{\mathrm{span}}$ | burnt fraction | band the level was locked to |
|---|---|---|---|---|---|
| Low | 0.43<!-- N:CAL-3 --> | subcritical | 0.021<!-- N:CAL-3 --> | 1.9 %<!-- N:CAL-3 --> | $P_{\mathrm{span}} < 0.05$ and burnt fraction in [1, 5] %<!-- N:DX-201 --> |
| Medium | 0.49<!-- N:CAL-3 --> | near-critical | 0.547<!-- N:CAL-3 --> | 19.8 %<!-- N:CAL-3 --> | $P_{\mathrm{span}}$ in [0.3, 0.7]<!-- N:DX-201 --> |
| High | 0.70<!-- N:CAL-3 --> | supercritical | 0.998<!-- N:CAL-3 --> | 98.3 %<!-- N:CAL-3 --> | front speed in [0.5, 1.0] cells per step<!-- N:DX-201 -->, measured 0.83<!-- N:DX-6 --> |

At High the front moves at 83 %<!-- N:DX-6 --> of the agents' speed of one cell per step<!-- N:DX-6 -->; escape is possible in principle. Medium sits between the finite-size pseudo-critical point $\beta_c(64) \approx 0.486$<!-- N:CAL-4 -->, where $P_{\mathrm{span}} = 1/2$ at $L = 64$<!-- N:CAL-4 -->, and $\hat\beta_c$. It is the severity of the held-out evaluation configuration of §9, $\theta^* = (\beta, \kappa_A, \kappa_B, \delta)$ = (0.49<!-- N:CAL-3 -->, 0.06<!-- N:CA-1 -->, 1.0<!-- N:CB-1 -->, 1.0<!-- N:COM-6 -->); the compositional test trains at Low and High only.

### 4.4 Re-testing the Medium prediction

The calibration-phase probe at $d_p = 0.5$<!-- N:ENV-1 --> (the fire alone, 500 updates<!-- N:DX-203 -->, three seeds per severity<!-- N:DX-203 -->) had saved no checkpoints. The re-test at fixed policy re-ran it from the same configurations and seeds (equivalent, not bitwise identical) and evaluated each final checkpoint on 512 episodes<!-- N:DX-203 -->. For survival the prediction is refuted: per-episode variance at fixed policy is monotone in severity, 0.00091, 0.00709 and 0.00885 at Low, Medium and High<!-- N:CAL-5 -->. For completion it is not confirmed: Medium and Low tie within bootstrap intervals, 0.01245 against 0.01235<!-- N:DX-8 -->, both above High. The environment-level mechanism is confirmed: with no agents, the burnt fraction's variance peaks near $\beta \approx 0.53$<!-- N:DX-8 -->, just above Medium, and ranks Medium above High above Low at the locked levels.

The re-test report offers an account it did not test: outcome variance is roughly the environment's variance, which peaks near criticality, times the policy's sensitivity to it, which grows with severity. The refutation is scoped to survival, for these fire-only policies at this budget; §10 states what siting the held-out test at Medium costs.

<!-- PAPER V2 DRAFT (PAPER V2 ruling, 2026-10-11): builder-drafted, not owner-approved -->

## 5 Coupling A: collapse seeds the fire

<!-- STUB-SPEC
PURPOSE: Coupling A lets structural collapse seed the fire. State Def. 5 as implemented; give the agents' weak, indirect influence on collapse (the home of those numbers); show the coupling in code (Listing 4); state Prop. 3's linear scaling and report its two handshake runs as two; report that under trained policies the coupling limits itself at High (the home of the 4.83-fold fall), as the random-policy calibration had already shown, with the later prediction's three parts; the near-agent share; Low survival off its ceiling; and that no contrast here has a floor of its own.
SUBSECTIONS (H3, as the demo's): 5.1 Definition and implementation; 5.2 The handshake with Proposition 3; 5.3 Under trained policies the coupling limits itself.
WRITER: W4. BUDGET: 850 prose words (the demo's: 1,307); Figure 6 caption at most 120 words.
REQUIRED FACTS: CA-1 (f_weak 0.15, λ₀ 5e-5, λ_load 4e-4, κ_A 0.06, r_A 1; locked 2026-07-21, DX-401); DX-37 (seeding neighbourhood 3 × 3); CA-8 (an occupied weak cell collapses nine times as often per step; DERIVED, load is boolean); CA-9 (about 7.81 collapses per episode with no load; load adds 0.4 to 1.4 % under the trained Phase-3 policies, 500 updates, and 7.4 to 8.3 % as an increase under random policies, 6.9 to 7.6 % as a share; this is the home, so OWNER ITEM 4 resolves here); DX-304 (both handshake runs: β = 0.43, ι = 0, no primary ignition, no agents); CA-2 (the first run: L = 64 sweep, κ_A 0.02, f_weak 0.4, R² 0.998 over a 14× range of the expected seed count; not the locked parameters); CA-3 (the second: L = 32 CPU test, κ_A 0.003, ratio 0.992 inside [0.90, 1.02], R² 0.9995; a different run, report text only); DX-40 (trained policies, 500 updates); CA-4 (the Coupling-B calibration grid, κ_B = 1.0 arm: 4.05 / 3.41 / 0.84 seeded ignitions per episode, a 4.83-fold fall); CA-5 (the Coupling-A calibration grid replicates: 4.08 / 3.42 / 0.83, 4.92-fold); CAL-3 (High burns 98.3 % of the arena in calibration, no agents); DX-9 (about 5.7-fold already at the random-policy calibration, recorded at the lock as fuel limitation before any trained policy; the later prediction's three parts: fuel-limited at High confirmed, "need not be monotone" not supported, "Medium is the peak" refuted); CA-6 (the near-agent share in [0.164, 0.203] across nine cells); CA-7 (Low survival 0.979 to 0.961, two seeds per arm; weak-cell occupancy higher by 0.054 with the coupling on); DX-10 (Low fire deaths 0.062 to 0.229 per episode, 3.7-fold); CB-1 (κ_B = 1.0 in Figure 6's caption).
FIGURES: Figure 6, coupling_a_explorer.html, companion coupling_a_explorer.png, height 680, carried below. Caption at most 120 words, numbers the figure prints not repeated (rule R3); it glosses "m44" and "m35" as printed (the Coupling-B and Coupling-A calibration grids) and "card" if printed; status "reference scale (cross-artifact)" for any floor; the two Prop. 3 runs shown apart; it cannot show a floor for any trained-policy contrast. A pointer to Figure 1's event track (press ] in Figure 1) replaces any deep link (A6).
LISTINGS (carried below, exact lines): Listing 4, che/env/structure.py:83-102: the uniforms are drawn before anything reads κ_A, so κ_A = 0 is the nested model bit for bit; the dilation acts on the increment c′ − c; seeding lights only cells still Fuel (the fuel limitation of section 5.3). Prose must not echo "Invariant #3" from the code comment.
LATEX: Def. 5's collapse probability (one display); Prop. 3 (one display: the linear form and the inequality). Prop. 3 loses "diverges as β ↑ β_c like the 43/18 power" (C1). It makes no divergence claim on the arena (P3-N5); a divergence on ℤ² would need a verified source, and none is recorded, so by default the divergence clause goes. The finite-protocol remark in one sentence (its four corrections have known signs); details in Appendix A.
HONESTY LINES AND REGISTERED STRINGS: "reference scale (cross-artifact)"; the handshake is two runs, not one, neither at the locked parameters; no m44 or m35 contrast is graded against a floor of its own; seeded-ignition figures are the Coupling-B grid's (CA-4), not the Coupling-A grid's.
FIX-LIST AND FINDINGS ITEMS OWNED: C1 knock-on (Prop. 3's rate); P3-N5 (no divergence on the finite arena); P3-N6 (class B part: scope "collapse is the fire's only birth channel" to the tested regime with no primary ignition, DX-304; the restatement of the proposition is Q13, not applied); OI-1 (the timing paragraph: what the lock recorded before training was the fuel limitation, not the trained fall); OI-4 (the home of the influence numbers); F5 (m44, m35, M3.4, M3.5, M3.3 named as studies); LEN (one sentence per handshake run; the Low paragraph and the floor paragraph to one sentence each); P2-k; Q13, Q4g.
STYLE: no "hazard begets hazard" without the agent-influence sentence; no aphoristic closers (P3-§6); sentences of at most 40 words.
DEMO KEEPS (sections/05_coupling_a.md): Def. 5 as implemented; Listing 4 and its gloss; Prop. 3's statement minus the rate; the remark in one sentence; the two runs reported separately; section 5.3's finding, its replication, the corrected timing and the prediction's three parts; the near-agent share. CHANGES: the rate and the divergence go; names become plain; the influence paragraph becomes the one home of CA-8 and CA-9. DROPS: "near criticality one collapse has a divergent expected burnt area"; repeated statements of the 4.83-fold fall outside this section (they point here).
NOT HERE: one Prop. 3 run; the locked parameters in the handshake; floor-graded seeded-ignition contrasts; that Medium is the co-activity peak; the Coupling-A grid as the source of the 4.83-fold figure; that agents avoid weak cells; "as predicted before measurement".
DEPENDENCIES: section 6.5 (the counter counts these ignitions near agents); section 9.2 (the High readout and mediation point here); section 10 item 1 (A marginal at High).
-->

Coupling A lets structural collapse feed the fire. Figure 1's event track marks one random-policy episode's collapses and the ignitions they seeded (press <kbd>]</kbd> in Figure 1 to step between them); Figure 6 counts them under trained policies.

<figure class="l-page">
  <iframe src="{{ 'assets/html/submission/coupling_a_explorer.html' | relative_url }}" width="100%" height="736" style="border:none" title="Coupling A explorer: collapse-seeded ignitions by severity, their share near agents, and the two Proposition 3 runs" loading="lazy"></iframe>
  <figcaption><strong>Figure 6.</strong> Coupling A under trained policies, and the two Proposition 3 runs. <em>Top:</em> collapse-seeded ignitions per episode by severity, and their share inside an alive agent's crop, in the Coupling-B and Coupling-A calibration grids (labelled m44 and m35; Phases 3 and 4 are calibration stages). Whiskers are min–max over training seeds; neither grid has identical reruns, and nothing shown has a floor. <em>Bottom:</em> the two runs, kept apart, neither at the locked parameters; the second (v2, a revised suite test) has no committed data file and is shown as values. <span class="figure-note">Status: top, trained policies, 500 updates<!-- N:DX-40 -->, seed ranges; bottom, no agents · Interact: hover or tab to a point; table view.</span></figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/coupling_a_explorer.png" class="img-fluid" alt="Collapse-seeded ignitions per episode at three severities for two trained grids, the share of them near agents, and the two Proposition 3 handshake runs shown separately." caption="Static companion of Figure 6 for the printed PDF." %}
</div>

### 5.1 Definition and implementation

**Definition 5 (Coupling A, as implemented).** Let $w(g) \in \{0,1\}$ mark weak terrain, a spatially clustered fraction $f_{\mathrm{weak}}$ of the cells drawn once per episode, and let $o_t(g) \in \{0,1\}$ indicate that at least one alive agent stands on cell $g$ before the step. An intact cell collapses at step $t$ with probability

$$
\lambda_t(g) = \big(\lambda_0 + \lambda_{\mathrm{load}}\,o_t(g)\big)\,w(g),
$$

so a cell that is not weak never collapses, and collapse is absorbing. Coupling A then ignites, with probability $\kappa_A$, each cell that is still Fuel after this step's spread and lies within Chebyshev distance $r_A$ of a cell that collapsed in this step. The fire kernel thus reads only the collapse increment $c' - c$, and a seeded cell is Burning in $h'$. Setting $\kappa_A = 0$ recovers the uncoupled fire kernel $T_H^{\beta,0}$, so the ablation "no Coupling A" is a nested model of the full system.

The theory states the impulse per collapse event; the implementation draws one uniform per cell, and the two rules coincide wherever seeding neighbourhoods do not overlap. The values, locked on 2026-07-21<!-- N:DX-401 -->, are $(f_{\mathrm{weak}}, \lambda_0, \lambda_{\mathrm{load}}, \kappa_A, r_A) = (0.15,\ 5\times 10^{-5},\ 4\times 10^{-4},\ 0.06,\ 1)$<!-- N:CA-1 -->, so the seeding neighbourhood is a 3 × 3<!-- N:DX-37 --> block.

Agents influence collapse, weakly and indirectly. Occupancy enters as a yes-or-no load: a weak cell with any agent on it collapses nine times<!-- N:CA-8 --> as often as an empty one. Without load, the locked parameters give about 7.81<!-- N:CA-9 --> collapses per episode. Load adds 0.4 to 1.4 %<!-- N:CA-9 --> to that count under trained policies (the Coupling-A calibration grid of §5.3) and 7.4 to 8.3 %<!-- N:CA-9 --> under random ones, which is 6.9 to 7.6 %<!-- N:CA-9 --> of all collapses. Agents cannot ignite a cell, but where they stand changes collapse rates, and a collapse can seed fire.

**Listing 4.** Coupling A's seeding mask, with its uniforms drawn whatever $\kappa_A$ is.

<!-- LISTING: che/env/structure.py:83-102 -->
```python
# che/env/structure.py:83-102 (verbatim)
def coupling_a_seed_mask(
    key: jax.Array,
    collapse_increment: jax.Array,
    *,
    kappa_A: float,
    r_seed: int,
) -> jax.Array:
    """Coupling A (Def. 5): each cell in the seeding neighborhood N_A of a
    new collapse (Chebyshev radius r_seed) ignites independently w.p.
    kappa_A. `collapse_increment` is the boolean mask of c' - c, i.e. cells
    that collapsed *this step* — T_H reads the increment, not the stock.
    Returns the candidate ignition mask; `hazard.seed_ignitions` applies it
    to Fuel cells only.
    """
    chex.assert_rank(collapse_increment, 2)
    chex.assert_type(collapse_increment, jnp.bool_)
    # Invariant #3: uniforms drawn even when kappa_A == 0.
    u = jax.random.uniform(key, collapse_increment.shape)
    near_new_collapse = dilate(collapse_increment, r_seed)
    return near_new_collapse & (u < kappa_A)
```

The uniforms `u` are drawn before anything reads $\kappa_A$, so $\kappa_A = 0$ is the nested model bit for bit under the rule of §3.4. The mask then goes to `hazard.seed_ignitions`, which lights only cells still Fuel; this is where the fuel limitation of §5.3 enters.

### 5.2 The handshake with Proposition 3

**Proposition 3 (Collapse events dominate hazard exposure).** Work in the subcritical regime $\beta < \beta_c$ with $\iota = 0$, and suppose collapse events arrive at rate $\lambda_A$ per step, each seeding one ignition at a uniformly located Fuel cell, with seeded clusters pairwise disjoint (the sparse regime, $\lambda_A T \chi(\beta) \ll \lvert G \rvert$, the number of cells). Then the expected burnt area $B_T$ by time $T$ satisfies

$$
\begin{aligned}
\mathbb{E}[B_T] &= \lambda_A T\,\chi(\beta)\,\big(1 + o(1)\big), \\
\text{and in general} \quad \mathbb{E}[B_T] &\le \lambda_A T\,\chi(\beta),
\end{aligned}
$$

where $\chi(\beta)$ is the mean percolation cluster size. Consequently the marginal hazard exposure per unit of structural instability is $\partial\,\mathbb{E}[B_T]/\partial\lambda_A = T\chi(\beta)$.

The proof (Appendix A) grows each seed into a bond-percolation cluster by Proposition 2 and sums expectations; overlaps only remove double counting. With no primary ignition, as in both runs below, collapse is then the fire's only birth channel. In a finite protocol the equality is approached only with an unconditional cluster-mass reference (a spanning-conditioned one understates the mass), matched seed locations and ages, and sparse seeding; boundary clipping, seed age and overlapping seeds each lower the measured slope (Appendix A).

We tested the proposition in two<!-- N:DX-304 --> runs, neither at the locked parameters, both without agents or primary ignition at the subcritical Low level ($\beta = 0.43$, $\iota = 0$<!-- N:DX-304 -->). The first, a dense sweep on a 64 × 64<!-- N:CA-2 --> grid ($\kappa_A = 0.02$, $f_{\mathrm{weak}} = 0.4$<!-- N:CA-2 -->), fits burnt area against realized seeds through the origin: $R^2 = 0.998$<!-- N:CA-2 --> over a 14×<!-- N:CA-2 --> range of the expected seed count. The second, a slower test in the suite on a 32 × 32<!-- N:CA-3 --> grid ($\kappa_A = 0.003$<!-- N:CA-3 -->), divides its slope by a protocol-matched reference computed inside the test: 0.992<!-- N:CA-3 -->, inside the band [0.90, 1.02]<!-- N:CA-3 -->, with $R^2 = 0.9995$<!-- N:CA-3 -->.

### 5.3 Under trained policies the coupling limits itself

In the Coupling-B calibration grid (500 updates<!-- N:DX-40 --> at each severity, $\kappa_B$ off and on, Coupling A on), the $\kappa_B = 1.0$<!-- N:CB-1 --> arm records 4.05, 3.41 and 0.84<!-- N:CA-4 --> collapse-seeded ignitions per episode at Low, Medium and High, a 4.83-fold<!-- N:CA-4 --> fall (from unrounded counts). The Coupling-A calibration grid ($\kappa_A$ off and on, with other policies, trained on the observation before masking) replicates it: 4.08, 3.42 and 0.83<!-- N:CA-5 -->, a 4.92-fold<!-- N:CA-5 --> fall.

Collapse never reads $\beta$; what changes with severity is where the seeds land. At High the fire burns 98.3 %<!-- N:CAL-3 --> of the arena in calibration, and the Fuel-only rule discards most seeding attempts. This concerns ignitions only: the Coupling-A grid's survival contrasts, on two seeds per arm<!-- N:CA-7 --> and with no floor, cannot locate the coupling's largest effect on outcomes.

This fuel limitation was on record before any trained policy was measured. At the Coupling-A lock, the random-policy calibration put seeded ignitions at High about 5.7 times<!-- N:DX-9 --> below Low at every $\kappa_A$ tried, and the lock recorded it as the fuel-exhaustion self-limitation of the ignition channel. A later prediction was written after the trained results existed and before its own analysis. It held that Coupling A is fuel-limited at High, that the co-active count of §6.5 need not be monotone in severity, and that Medium may be its peak. The 4.83-fold<!-- N:CA-4 --> fall confirms the first, which earlier reports already answered. The count is monotone non-increasing and Low and Medium are indistinguishable, so the second is not supported and the third is refuted.

Across all nine<!-- N:CA-6 --> measured cells (two arms of the Coupling-B grid and one of the Coupling-A grid, at three<!-- N:CAL-3 --> severities), the share of seeded ignitions inside an alive agent's crop stays in [0.164, 0.203]<!-- N:CA-6 -->.

At Low the coupling moves survival in the Coupling-A grid off its ceiling, from 0.979 to 0.961<!-- N:CA-7 -->, as fire deaths per episode rise from 0.062 to 0.229<!-- N:DX-10 -->. Weak-cell occupancy is higher by 0.054<!-- N:CA-7 --> with the coupling on, which suggests, on two seeds per arm<!-- N:CA-7 -->, that the policies do not learn to avoid weak cells. No contrast in this section has a floor on its own artifact, since neither grid has identical reruns; any floor beside them is a reference scale (cross-artifact); see §8.6.

<!-- PAPER V2 DRAFT (PAPER V2 ruling, 2026-10-11): builder-drafted, not owner-approved -->

## 6 Coupling B: smoke attenuates perception

<!-- STUB-SPEC
PURPOSE: Coupling B makes what an agent perceives depend on the hazard's own state. State Def. 6 as implemented and show it in code (Listing 5); state Thm. 1 and what it buys, with the toy gate as a test of the code; give the lock's outcome in one paragraph; report the survival cost at High led by its 3 of 3 replication, and Coupling B's own survival effect at Medium (the home of that measurement); explain where the masking falls; define the co-active counter and what it can see.
SUBSECTIONS (H3, as the demo's): 6.1 Definition and implementation; 6.2 What attenuation does to the value of adaptivity; 6.3 The lock: three bands that did not intersect; 6.4 The cost is paid in survival, at High; 6.5 The co-active counter, and what it can see.
WRITER: W4. BUDGET: 1,050 prose words (the demo's: 1,652); Figures 7 and 8 captions at most 80 words each.
REQUIRED FACTS: DX-33 (Figure 1 opens on agent 7 at t = 128; a pointer, no deep link); ENV-6 (9 × 9 crop); ENV-7 (the eighth plane records the reveal); CB-4 (the toy gate: largest absolute z 2.11; sum of z² 6.55 on 8 degrees of freedom, p = 0.586; mean z −0.44); DX-14 (the memorizing policy flat at ½; J*(0) = 1.0000; J* − ½ = 0.0000 at κ_B = 8 where q = 0.0056); DX-301 (the three bands); CB-3 and DX-12 (the masked-share band unreachable at Medium: ceilings 0.028 / 0.130 / 0.419 against the band's floor 0.150); CB-2 (detection and toy bands disjoint by 1.35× under a random policy, 1.15× under probe policies); CB-1 (κ_B = 1.0 locked on the detection band alone); DX-40 (trained, 500 updates); DX-13 (the three High contrasts −0.0687, −0.1066, −0.0470: −6.87, −10.66, −4.70 points; one run per cell); CB-5 (negative 3 of 3; 1.41× is the first estimate over the High floor, the three's mean about 1.19×, both against a reference scale (cross-artifact)); CB-6 (the first estimate, −8.8 points, quoted only beside CB-5); CB-7 (High floor sd 6.21 points, measured afterwards on four identical runs of a separate artifact); CB-8 (completion flips sign on a same-seed retrain; unresolved); CB-9 (Medium survival −0.03 points, graded against a three-seed spread σ_seed 0.0072, not a floor; this is the home) and METH-1 (the later Medium survival floor 0.0129); CAL-3 (β 0.49 at Medium); DX-11 (masked share at danger moments 0.0809 / 0.0560 / 0.2424 against 0.00068 / 0.00249 / 0.01559 overall); CB-10 (118×, 22×, 16×); CO-4 and DX-37 (the counter: collapse-seeded ignitions inside an alive agent's crop, Chebyshev radius 4); CO-2 (P(zero) 0.563 / 0.578 / 0.883 over 1024 / 1536 / 1024 episodes); CO-1 (0.64 events per episode at Medium); CO-3 (variance over mean 1.31 to 1.40).
FIGURES: Figure 7, static fig04_coupling_b.png (include plus a caption paragraph), carried below; its caption says the band is a reference scale (cross-artifact) although the figure's legend says "floor" (P2-3, FIGURE BATCH B9), and that the figure cannot show intervals, completion or Medium. Figure 8, static fig05_coactive.png, carried below; its caption carries the counter's scope (co-active only in all-on configurations) and that no floor exists for it. Both figures stay where the demo had them (P2-d is Q22). Fonts and widths: P2-4 is Q22; keep the demo's markup.
LISTINGS (carried below, exact lines): Listing 5, che/env/observation.py:300-310 (shortened from the demo's 289-310, KB-2): τ by Beer–Lambert transmittance; the reveal draw is unconditional; the visibility plane is appended. Prose says the draw has its own stream and κ_B is read per episode from the state; it does not echo the code's internal tags.
LATEX: Def. 6's transmittance (one display); Thm. 1's statement with the q display (one display). The proof goes to Appendix A only (LEN); here keep what the theorem buys in two or three sentences, then the gate as a test of the shared transmittance function.
HONESTY LINES AND REGISTERED STRINGS: branch_B section 5 line 5 (Medium siting: this section holds the measurement; lead the High effect with CB-5's 3 of 3, CB-6's −8.8 only beside it) and line 10 (the counter means co-active only in all-on configurations; in a mixture it reads the Coupling-A marginal, which is why mediation is VOID, section 9.2); "reference scale (cross-artifact)"; "not behaviourally suppressed" scoped to trained policies at 500 updates.
FIX-LIST AND FINDINGS ITEMS OWNED: OI-6 (never "a sixth to a quarter"; the ceiling claim scoped to the κ_B = 1.0 arm); P2-3; KB-2 (Listing 5); LEN (Thm. 1's compact proof out; section 6.3 to one paragraph; "physically grounded" to one clause); F5 (the Coupling-B calibration grid named in words; M4.2, M4.4, M5.3b as studies); P3-N11 (class C: keep the demo's Thm. 1(2), which names the signal-blind policy and its value ½); P3-N16 (class C: the demo's scoped strength wording); Q22, Q23, Q24.
DEMO KEEPS (sections/06_coupling_b.md): Def. 6 as implemented; Listing 5's gloss; Thm. 1's statement; the gate numbers; the lock's outcome; the High effect with 3 of 3 first; the Medium −0.03 with its scope; the danger-moment masking; the counter, its scope and Figure 8. CHANGES: the proof to Appendix A; section 6.3 shortened; names plain. DROPS: the duplicated proof; "The direction replicates; the magnitude is modest." if it reads as an aphorism (say the same in a plain sentence).
NOT HERE: "certified"; the 8.8 lead; 1.41× as a pooled or own-artifact floor; "completion intact"; "not behaviourally suppressible" unscoped; "a sixth to a quarter"; the counter as a co-occurrence measure in mixtures; a Medium Coupling-B survival effect; a deep link.
DEPENDENCIES: section 9.2 (mediation uses the scope note; the High readout points to 6.4); section 10 item 1 (Medium siting points here for the measurement).
-->

Coupling B makes what an agent perceives depend on the hazard's own state. Figure 1 opens on agent 7<!-- N:DX-33 --> at t = 128<!-- N:DX-33 --> and shows that agent's observation as produced, the true state of the same 9 × 9<!-- N:ENV-6 --> cells, and the probability that each cell was seen.

### 6.1 Definition and implementation

**Definition 6 (Coupling B: Beer–Lambert observation, as implemented).** Smoke is the per-cell state field $\rho'$ of §3.2, updated after the fire with no spatial smoothing, so it outlives flame. For agent $i$ at $x_i$ and a cell $y$ of its crop, let $\bar\rho_i(y)$ be the mean of $\rho'$ at the four points $x_i + t_s(y - x_i)$, $t_s = (s + \tfrac12)/4$ for $s = 0, \dots, 3$, each read at the nearest cell (smoke outside the grid reads 0). The transmittance is

$$
\tau_i(y) = \exp\!\big(-\kappa_B\,\lVert y - x_i \rVert_2\,\bar\rho_i(y)\big),
$$

a midpoint-rule form of $\exp(-\kappa_B \int_{x_i \to y} \rho\,d\ell)$ along the line of sight. Each crop cell is revealed independently with probability $\tau_i(y)$: a revealed cell passes its seven<!-- N:ENV-7 --> content planes, an unrevealed one passes zeros, and an eighth<!-- N:ENV-7 --> plane records the realized reveal, so the agent can tell "unseen" from "empty". The own cell has distance 0 and is always seen. Setting $\kappa_B = 0$ gives $\tau \equiv 1$ and recovers hazard-independent observation.

Because $\rho'$ is hazard state, perception degrades where and when the fire is active.

**Listing 5.** Coupling B in the observation kernel: transmittance, the reveal draw and the visibility plane.

<!-- LISTING: che/env/observation.py:300-310 -->
```python
# che/env/observation.py:300-310 (verbatim)
        tau = transmittance(
            state.smoke, state.agent_pos, kappa_B=state.theta_live.kappa_B, k=k
        )
        reveal = jax.random.uniform(key, tau.shape) < tau  # P(seen) = tau
        grid = jnp.concatenate(
            [
                grid * reveal[..., None].astype(jnp.float32),
                reveal[..., None].astype(jnp.float32),
            ],
            axis=-1,
        )
```

The `reveal` line draws its uniforms whatever $\kappa_B$ is, so at $\kappa_B = 0$ the mask is all ones and the environment is bitwise the one before masking (§3.4, Listing 3). The draw has its own random stream, and $\kappa_B$ is read per episode from the state, which is how a training mixture varies it.

### 6.2 What attenuation does to the value of adaptivity

**Theorem 1 (Memorization gap, and its erosion by Coupling B).** Consider the two-corridor environment $E_{2C}(\kappa_B)$: from a start cell, a path of $d$ steps leads to a branch $b$, from which two disjoint corridors $L$ and $R$ of length $\ell$ lead to the goal; the horizon is $T = d + \ell$ (zero slack: a wrong commitment cannot be undone). At $t = 0$ nature draws $Z \in \{L, R\}$ uniformly; corridor $Z$ burns at depth $\ell_f \ge 1$ beyond $b$, and an agent entering it is disabled. The reward is 1 for reaching the goal by $T$, else 0. At each step $t \le d$ the agent receives the signal $Y_t = Z$ with probability $e^{-\kappa_B (d - t + \ell_f)}$ (Beer–Lambert over the current distance to the fire, unit smoke density), else $Y_t = \varnothing$; signals are independent across time and remembered. Let

$$
q(\kappa_B) = 1 - \prod_{j=\ell_f}^{d+\ell_f} \big(1 - e^{-\kappa_B j}\big)
$$

be the probability of being informed by the commitment point. Then (1) the optimal value is $J^*(\kappa_B) = \tfrac12 + \tfrac12 q(\kappa_B)$; (2) the policies optimal for the fixed-map variant ($Z \equiv z_0$ constant) include the signal-blind policy "always take the corridor other than $z_0$", whose value on $E_{2C}$ is $\tfrac12$ for every $\kappa_B$, so the memorization gap is $J^*(\kappa_B) - J^{\mathrm{static}} = \tfrac12 q(\kappa_B) > 0$ for all finite $\kappa_B$; and (3) $q$ is continuous and strictly decreasing in $\kappa_B$, with $q(0^+) \to 1$ and $q(\kappa_B) \to 0$ as $\kappa_B \to \infty$, so under total perceptual denial the optimal adaptive policy is no better than the memorizing one.

In one toy (proof in Appendix A), a memorizing policy loses exactly half the probability of being informed, and the hazard's own attenuation shrinks that loss continuously to zero; the theorem says nothing about what a learner does in CHE.

The theorem also tests the code. The toy and the observation kernel share one transmittance function, and the toy's information probability agrees at every grid point across Monte Carlo, the closed-form product and the full observation pipeline. The measured optimal value matches $\tfrac12 + \tfrac12 q$ under a three-condition<!-- N:CB-4 --> gate: largest $\lvert z \rvert$ 2.11<!-- N:CB-4 -->, $\sum z^2 = 6.55$<!-- N:CB-4 --> on 8<!-- N:CB-4 --> degrees of freedom ($p = 0.586$<!-- N:CB-4 -->), and mean $z$ −0.44<!-- N:CB-4 -->. The memorizing policy stays flat at ½<!-- N:DX-14 -->, $J^*(0) = 1.0000$<!-- N:DX-14 -->, and $J^* - \tfrac12 = 0.0000$<!-- N:DX-14 --> at $\kappa_B = 8$, where $q = 0.0056$<!-- N:DX-14 -->.

### 6.3 The lock: three bands that did not intersect

The strength $\kappa_B$ was to be locked where three<!-- N:DX-301 --> bands set before calibration intersect. They were a masked share of the crop at Medium in [0.15, 0.45]<!-- N:DX-301 -->, a probability in [0.4, 0.7]<!-- N:DX-301 --> that a Burning cell three<!-- N:DX-301 --> cells away is revealed at Medium, and a toy information probability $q$ in [0.3, 0.7]<!-- N:DX-301 -->. They do not intersect. The masked-share band cannot be reached at Medium: the masked share can only approach the share of crop cells with smoke on their line of sight, 0.130<!-- N:DX-12 --> there under a random policy, below the band's lower edge of 0.150<!-- N:DX-12 -->. The same $\kappa_B$ attenuates the arena's extended smoke more strongly than the toy's single smoke source, which leaves the detection and toy bands disjoint by a factor of 1.35 under a random policy and 1.15 under probe policies<!-- N:CB-2 -->. On 2026-07-27<!-- N:DX-401 -->, $\kappa_B = 1.0$<!-- N:CB-1 --> was locked on the detection band alone; the masked-share band was retired, not widened, and the toy band kept as a consistency check.

### 6.4 Survival cost at High severity

{% include figure.html path="assets/img/submission/fig04_coupling_b.png" class="img-fluid" alt="Left, the masked share of the agent crop at three severities, over all alive agent-steps and at danger moments, on a log scale. Right, three replicate survival contrasts at high severity and then the first estimate, against a hatched band one standard deviation wide on a reference scale measured on another artifact." caption="Figure 7. Coupling B: where the masking falls, and the High survival contrasts." %}

<p class="caption">(a) Masked share of the crop in the coupled arm of the Coupling-B calibration grid (labelled m44 and M4.4), over all alive agent-steps and at danger moments. (b) The High survival contrasts between the arms: three replicates<!-- N:DX-13 -->, then the first estimate. The hatched band, labelled floor, is a reference scale (cross-artifact). The figure cannot show intervals, completion or Medium. <span class="figure-note">Status: trained policies, 500 updates<!-- N:DX-40 --> · static.</span></p>

At High, three<!-- N:DX-13 --> replicate contrasts of survival between $\kappa_B = 1.0$<!-- N:CB-1 --> and $\kappa_B = 0$ are negative three times out of three<!-- N:CB-5 --> (Figure 7(b); trained policies, 500 updates<!-- N:DX-40 -->, $d_p = 0.5$<!-- N:ENV-1 -->, Coupling A on). They are −6.87 and −10.66 points for the grid's two seeds<!-- N:DX-40 --> and −4.70 points for a same-seed retrain<!-- N:DX-13 -->, each one run per cell<!-- N:DX-13 --> and without an interval. The grid's first estimate, the mean of its two seeds<!-- N:CB-6 -->, was −8.8 points<!-- N:CB-6 -->. The High survival floor, sd 6.21 points<!-- N:CB-7 -->, was measured later on four identical runs<!-- N:DX-40 --> of a separate artifact: a reference scale (cross-artifact). The first estimate is 1.41 times<!-- N:CB-5 --> this floor and the replicates' mean about 1.19 times<!-- N:CB-5 --> it. We report a consistent effect of modest size; the first analysis graded it "strong" against a two-seed<!-- N:DX-38 --> spread, a label retracted under the rule of §8.1. Completion is not resolved, since its contrast flipped sign on the same-seed retrain<!-- N:CB-8 -->.

At Medium, the severity of the held-out test configuration (β = 0.49<!-- N:CAL-3 -->), Coupling B's own survival effect in the same grid was −0.03 points<!-- N:CB-9 -->. It was judged against a three-seed<!-- N:CB-9 --> spread, $\sigma_{\mathrm{seed}} = 0.72$ points<!-- N:CB-9 -->, with no measured floor; the Medium survival floors measured later, on two<!-- N:METH-1 --> GPUs, are 1.29 and 1.30 points<!-- N:METH-1 -->. Coupling B's measured survival cost is therefore at High, while §9's test runs at Medium (§10, item 1).

The masking concentrates on moments of danger, alive agent-steps with a Burning cell inside the agent's crop. In the $\kappa_B = 1.0$<!-- N:CB-1 --> arm the masked share of the crop at danger moments is 0.0809, 0.0560 and 0.2424<!-- N:DX-11 --> at Low, Medium and High, against 0.00068, 0.00249 and 0.01559<!-- N:DX-11 --> over all alive agent-steps: 118, 22 and 16 times<!-- N:CB-10 --> more concentrated (ratios of unrounded shares; Figure 7(a)). Within trained policies at 500 updates<!-- N:DX-40 --> the attenuation was not behaviourally suppressed: the coupled policies' masking ceiling, which does not depend on $\kappa_B$, sat at or above its random-policy value at every severity.

### 6.5 The co-active counter, and what it can see

The environment logs, at every step, the number of collapse-seeded ignitions inside an alive agent's crop, within Chebyshev radius 4<!-- N:DX-37 --> of its post-step position<!-- N:CO-4 -->. It was meant to catch both couplings at once, but only Coupling A produces those ignitions and $\kappa_B$ does not enter the count, so the counter is co-active only in all-on configurations. In a training mixture it reads the Coupling-A marginal alone, which is why the mediation analysis registered on it is void (§9.2).

{% include figure.html path="assets/img/submission/fig05_coactive.png" class="img-fluid" alt="Three bar charts, one per severity, of the share of episodes with zero, one, two, three, and four or more co-active events." caption="Figure 8. The co-active counter per episode, by severity." %}

<p class="caption">Share of episodes with each number of co-active events in the coupled arm of the Coupling-B calibration grid (labelled m44), seeds pooled; both couplings are on in every cell. The figure cannot show a floor, since none exists for this counter, or a training mixture (§6.5). <span class="figure-note">Status: descriptive; trained policies, 500 updates<!-- N:DX-40 -->; no floor · static.</span></p>

In these all-on cells the counter is rare and bursty (Figure 8). The share of episodes with no co-active event is 0.563, 0.578 and 0.883<!-- N:CO-2 --> at Low, Medium and High, the mean at Medium is 0.64<!-- N:CO-1 --> events per episode, and the variance-to-mean ratio, 1.31 to 1.40<!-- N:CO-3 -->, exceeds the Poisson value of 1. Low and Medium are indistinguishable and High is lower, because seeded ignitions fall while the near-agent share stays in its range (§5.3).

<!-- PAPER V2 DRAFT (PAPER V2 ruling, 2026-10-11): builder-drafted, not owner-approved -->

## 7 Communication denial: inert under this encoder at this scale

<!-- STUB-SPEC
PURPOSE: The third stressor denies inter-agent links and, unlike the couplings, is independent of the fire. State Def. 7 as implemented and the line that makes the channel non-differentiable (Listing 6); state Remark 2′ after citing Pynadath and Tambe (READS RULING item 4); report the toy handshake and the three measurements in CHE as bars (post-hoc floor grading, about 50 % power); give the two-part argument for inertness with the record's demand-side reading and its two qualifications; end with one neutral sentence that the δ-only third of ISO's training is therefore fire-only, pointing to section 9.1 for the consequence.
SUBSECTIONS (H3, as the demo's): 7.1 The kernel; 7.2 When communication should matter; 7.3 In CHE the channel carries nothing measurable.
WRITER: W4. BUDGET: 800 prose words (the demo's: 1,295); Figure 9 caption at most 80 words.
REQUIRED FACTS: COM-6 (R_comm = 16 cells; δ = 1.0 locked 2026-07-30); DX-17 (messages of dimension 8, one-step latency, masked-mean pooling, Chebyshev range, thinning by 1 − δ with unconditional uniforms); ENV-12 (the message head receives no gradient; receivers' weights are trained); ENV-1 (d_p = 0.5 in Remark 2′(i)'s qualifier); COM-1 (the toy's value of communication rises from 0 to 0.498); DX-15 (the toy's constants: 4096 episodes and 8192 Monte Carlo draws per point; free arm 1.0000; largest absolute z 0.44, χ² 0.51 on 8 degrees of freedom; q̃/q 1.126 at κ_B 1.0, peak 1.235; 79 / 54 / 7 % at κ_B 0.5 / 1.0 / 3.0: these move to Appendix A, LEN); ENV-6 and ENV-11 (twelve interchangeable agents sharing one set of parameters); COM-2 and DX-305 (Medium content ablation, two seeds, R_comm 8, δ = 0, 500 updates; bar about 3 points); COM-3 and DX-16 (High, three seeds, R_comm 8 and 16; out-degree 1.01 to 2.99 changed nothing; bar about 11 points); COM-4 (the denial element at Medium, four seeds, R_comm 16: completion +0.38 points against a bar of 7.99, survival −1.43 against 2.60; both bars twice the floor sd on that GPU); COM-5 (condition (iii) VOID: a 20 % threshold chosen at implementation, below the quantity's own 27.2 % nondeterminism; observed 23.2 %); DES-8 (the δ-only third).
CITATIONS: pynadath2002 (their Theorem 4 and Table 2; Theorems 5 and 6; Theorem 3 only if the owner approves, P3-N12).
FIGURES: Figure 9, static fig06_comms.png (include plus a caption paragraph), carried below. Caption at most 80 words: (a) is the toy with scripted policies, (b to d) are CHE at Medium with post-hoc floor-grading bars; the figure carries no word "inert"; it cannot show the content ablations, the High runs, the VOID condition, or a trained encoder; glosses any study code it prints.
LISTINGS (carried below, exact lines): Listing 6, che/train/ippo.py:323-329: stop_gradient on the delivered messages, so no gradient crosses the channel and the encoder stays at initialization. Prose does not echo "Q3 ruling".
LATEX: Def. 7's link probability (one display); Remark 2′'s statement with the VoC display (one display), stated in full here (READS RULING item 4: cite first, refine second). Remark 2 (superseded) is not stated.
HONESTY LINES AND REGISTERED STRINGS: branch_B section 5 line 4 (δ is inert; the composition tested is A × B; θ* keeps δ = 1.0 for fidelity to the registration). The full phrase "inert under a frozen random-projection encoder at this scale" has its home here. "VOID" for condition (iii). Each measurement is a bar, a post-hoc floor grading at about 50 % power, never a point null and never "excludes effects larger than". The frozen-encoder caveat: a cap measured on a frozen random encoder does not strictly bound a trained one (log:1102-1104); gradient-shaped messaging is untested (log:1106-1107); d_p prices deaths, so Remark 2′(i)'s clean-zero conditions are not fully met (log:1083-1088).
FIX-LIST AND FINDINGS ITEMS OWNED: F3 (the last paragraph is a neutral pointer: the δ-only episodes are fire-only and section 9.1 states the consequence; never "the bias that §9 registers and corrects"); F5 (M5.2, M5.3, M5.3b, M5.5 named as studies: the courier toy, the Medium content ablation, the High content ablation, the denial study); LEN (toy constants to Appendix A; "Three consequences carry into §9" and "The null rests on two halves" become plain sentences without announcing a count); P3-N9 and P3-N10 (class C: keep the theory doc's wording of Remark 2′); P3-N12 (class C: Theorem 3 not added); P3-N17 (class C: the demand-side reading kept, attributed to the record, log:1076-1081); Q23, Q24.
DEMO KEEPS (sections/07_comms.md): Def. 7; Listing 6 and its gloss; Remark 2′ cited first, refined second; the three measurements with their bars; the VOID condition in one sentence (its methods lesson lives in section 8.1); the demand-side argument; the two qualifications. CHANGES: constants to Appendix A; study codes to plain names; the last paragraph to a pointer. DROPS: announced enumerations; the duplicate of section 2's Pynadath and Tambe summary beyond what the citation needs.
NOT HERE: "certified inert"; that trained messages would also be useless; a point null; the 5/3 constant; that communication is load-bearing in CHE; "the swarm does not need the information" (say "the agents"); any statement that the design caught or foresaw the inert share.
DEPENDENCIES: sections 1 and 9.1 rely on "δ inert under this encoder at this scale" to define ISO's fire-only third; section 8.1 carries COM-5's lesson; Appendix A carries the toy's constants.
-->

The third stressor denies links between agents. In CHE, with a frozen message encoder, no measured effect of it cleared its bar (Figure 9).

{% include figure.html path="assets/img/submission/fig06_comms.png" class="img-fluid" alt="Top left, courier success rate against perception attenuation in the two-agent toy, for free and for denied communication, with the predicted curve. Top right, the denial contrasts at medium severity with their bars. Bottom, the per-run values behind those contrasts." caption="Figure 9. Communication in the toy, and denial in CHE at Medium." %}

<p class="caption">(a) The courier variant of the corridor toy (labelled E2C² and M5.2), scripted policies: success with free and with denied communication on the no-idle schedule (pinned); the shaded gap is VoC<sub>gated</sub> (§7.2). (b–d) The denial study (M5.5): contrasts against bars (post-hoc floor grading), and the runs. No panel grades inertness or shows the content ablations, High severity, the VOID condition or a trained encoder. <span class="figure-note">Status: descriptive · static.</span></p>

### 7.1 The kernel

**Definition 7 (Communication denial, as implemented).** After the agents move, the comms kernel $T_K(k' \mid x')$ samples a directed link graph over the alive agents: for every ordered pair $i \ne j$ of alive agents,

$$
\Pr\big[\, i \to j \text{ open} \,\big] = \mathbf{1}\big[\lVert x'_i - x'_j \rVert_\infty \le R_{\mathrm{comm}}\big]\,(1 - \delta),
$$

with $R_{\mathrm{comm}} = 16$<!-- N:COM-6 --> cells. Each agent emits a message $m_i \in [-1, 1]^{8}$<!-- N:DX-17 --> at step $t$; at $t + 1$ each receiver $j$ gets the mean of the messages delivered over the links then realized, $\bar m_j = \sum_i k'_{ij}\, m_i \,/\, \max(1, \sum_i k'_{ij})$, which is the zero vector when $j$ is isolated. $T_K$ reads positions and aliveness only, so denial is mechanistically independent of the fire. One uniform per ordered pair is drawn at every step whatever $\delta$ is, so $\delta = 0$ gives the deterministic range graph and $\delta = 1$, the value locked on 2026-07-30<!-- N:DX-401 -->, gives the empty graph, both bitwise. The theory's range-dependent link probability is implemented as this hard Chebyshev range.

**Listing 6.** Delivered messages carry no gradient.

<!-- LISTING: che/train/ippo.py:323-329 -->
```python
# che/train/ippo.py:323-329 (verbatim)
        # Messages emitted this step are delivered next step. Nothing crosses
        # an episode boundary (autoreset), and stop_gradient states in code
        # what the batch-storage already implies: the channel is not a
        # differentiable path (Q3 ruling; networks.py docstring).
        messages = jax.lax.stop_gradient(
            jnp.where(done[:, None, None], 0.0, emitted)
        )
```

No gradient crosses the channel, so the message head, a tanh-bounded dense layer on the shared trunk, stays at its initialization<!-- N:ENV-12 -->: an agent emits a frozen random projection of trunk features that are themselves trained. The receivers' weights on the message inputs are trained, which makes message use testable; what to say was never learned.

### 7.2 When communication should matter

Remark 2′ refines a result of Pynadath & Tambe <d-cite key="pynadath2002"></d-cite>. Free communication lowers the complexity of the team decision problem when the world is collectively observable (their Theorem 4 and Table 2), and makes no difference when it is individually observable or not observable at all (their Theorems 5–6). Remark 2′ concerns the value of communication under collective partial observability.

**Remark 2′.** Extend $E_{2C}$ with a second agent. (i) Under a team-any reward, communication has zero marginal value when the agents are interchangeable, expendable (no death cost) and at least as numerous as the hypotheses: coverage then achieves $J = 1$ under total denial. When any qualifier fails, value returns; in general it scales with the deficit of agents relative to hypotheses, and a death cost, such as CHE's $d_p = 0.5$<!-- N:ENV-1 -->, prices the redundancy that substitution spends. (ii) In the courier variant, where only agent 1 can complete the task and it observes the other agent only through messages, the denied optimum within the no-idle policy class is $\tfrac12 + \tfrac12 q(\kappa_B)$; with slack $\ell_f$, optimal denied play buys information by idling at the branch and achieves $\tfrac12 + \tfrac12 \tilde q(\kappa_B)$, where $\tilde q$ is the probability of being informed by the commitment point under the best idling schedule, with $\tilde q \ge q$ (equality iff $\ell_f = 0$), so

$$
\mathrm{VoC}_{\mathrm{true}}(\kappa_B) = \tfrac12\big(1 - \tilde q(\kappa_B)\big) \le \tfrac12\big(1 - q(\kappa_B)\big).
$$

Both $q$ and $\tilde q$ decrease in $\kappa_B$, so the value of communication increases with perception decay.

We ran the courier variant with scripted policies, delivering messages through the production link kernel and computing $\tau$ with the shared transmittance function, which tests both kernels. The free arm always succeeds<!-- N:DX-15 -->, the no-idle denied arm matches $\tfrac12 + \tfrac12 q$, and the value of communication against that arm, $\mathrm{VoC}_{\mathrm{gated}} = \tfrac12(1 - q)$, rises monotonically from 0 to 0.498<!-- N:COM-1 --> (Figure 9(a); Appendix A).

### 7.3 In CHE the channel carries nothing measurable

CHE's agents meet one of Remark 2′(i)'s qualifiers: they are twelve<!-- N:ENV-6 --> interchangeable agents sharing one set of parameters<!-- N:ENV-11 -->. Nothing establishes that they are at least as numerous as the hypotheses, and their deaths are priced ($d_p = 0.5$<!-- N:ENV-1 -->), so the clean-zero conditions are not fully met.

In a content ablation at Medium ($\delta = 0$, $R_{\mathrm{comm}} = 8$<!-- N:COM-2 -->, two seeds<!-- N:COM-2 -->, 500 updates<!-- N:DX-305 -->), three arms of identical architecture pass live, zeroed or shuffled messages (the delivered aggregate set to zero with links kept; sender identities permuted within a step). No pair differs beyond a bar of twice<!-- N:COM-2 --> the earlier Medium floor, about 3 points<!-- N:COM-2 -->. The same ablation at High (three seeds<!-- N:DX-16 -->, $R_{\mathrm{comm}}$ = 8 and 16<!-- N:DX-16 -->) found that raising the mean alive out-degree from 1.01 to 2.99<!-- N:COM-3 --> changed nothing, ruling out "nobody was in range". The wider High floors put its bars at 10.44<!-- N:V4-3 --> (completion) and 12.43 points<!-- N:V4-3 --> (survival).

In the denial study (Medium, four seeds<!-- N:COM-4 -->, $R_{\mathrm{comm}} = 16$<!-- N:COM-4 -->, message path live in both arms), completion is 0.38 points higher and survival 1.43 points lower with links open ($\delta = 0$) than with links denied ($\delta = 1$), against bars of 7.99 and 2.60 points<!-- N:COM-4 -->. Both bars are twice<!-- N:V4-2 --> the floor sd measured on the GPU that ran the study (Figure 9(b–d)). Every bar here is a post-hoc floor grading that a true effect of its size would clear only about half the time<!-- N:V4-1 --> (§8.2), so none of these results is a point null. A further condition, on danger-moment outcomes, is VOID: its threshold, chosen at implementation, sat below the quantity's own run-to-run nondeterminism (§8.1).

The content ablations supply a mechanism: in the live arm a receiver can tell that it heard from someone without decoding anything; in the zeroed arm it cannot. That signal needs no encoder and went unused at both severities and, at High, at both ranges. The neglect is therefore on the demand side (the agents did not need the information) rather than the channel side (they could not read it), and the frozen encoder cannot account for it.

Because deaths are priced, Remark 2′(i) leaves communication some value here, which the measurements find weak at this scale and this death price. Gradient-shaped messaging is untested, and a bound measured on a frozen random encoder does not strictly bound a trained one. We claim only that communication denial is inert under a frozen random-projection encoder at this scale.

The composition §9 tests is thus, in effect, Coupling A × Coupling B, with $\delta = 1.0$<!-- N:COM-6 --> kept in $\theta^*$ for fidelity to the registration. The δ-only third<!-- N:DES-8 --> of ISO's training is fire-only, and §9.1 gives the consequence.

<!-- PAPER V2 DRAFT (PAPER V2 ruling, 2026-10-11): builder-drafted, not owner-approved -->

## 8 Methodology: bars come with floors

<!-- STUB-SPEC
PURPOSE: The measurement rules section 9 uses, each stated with the one exhibit from the project's own record that produced it, and where this paper falls short of them (section 8.6, kept whole). Define once what a reproducibility floor is.
SUBSECTIONS (H3, as the demo's): 8.1 A bar without a floor is void; 8.2 Contrasts and power; 8.3 Floors move with the run, and gates must not divide by them; 8.4 The floor is a check, not the test variance (the demo's "hurdle" becomes "check", BRIEF section 5.2); 8.5 Instruments state what they are blind to; 8.6 Where this paper falls short of its own rules.
WRITER: W5. BUDGET: 850 prose words (the demo's: 1,447); Figure 10 caption at most 120 words.
REQUIRED FACTS: METH-1 (the Medium completion floor moved 2.75-fold, 0.0145 to 0.0399, survival 0.0129 to 0.0130; GPU, code version and configuration all differ, so the exhibit shows a floor can move for one metric and not another, not which factor moved it); DX-403 (RTX 5090 against RTX PRO 6000; reps); METH-2 (the reference code version read 0 of 760 field hashes differing in 4 of 4 comparisons; the refactored version differed from itself 1 time in 4 on two diagnostic channels; no trajectory field differed); DX-38 (σ_seed 0.0295 against the later High floor 0.0621, CB-7: the first floor-less bar, its "strong" retracted); DX-302 (roughly 46 seeds per arm to match Medium's resolution at High); COM-5 (the VOID condition: 20 % against 27.2 %, observed 23.2 %; the threshold was chosen at implementation, not registered); METH-3 (per-arm forms 92.1 % and 62.8 % against the contrast's 76.7 %, k = 34); METH-4 (k = 20 on a bare 2σ figure gave 55.6 % power, caught at registration); METH-7 and DES-13 (the 80 %-power MDE at the family-corrected α; z_α = 2.2365); DX-34 and METH-5 (floor growth 500 to 1000 updates: ISO 0.0165 to 0.0339, JOINT 0.0093 to 0.0483, 2.1-fold and 5.2-fold; length confounded with machine; the curriculum-difficulty ordering is an untested hypothesis); METH-6 (the T* ruling of 2026-08-11 retired a registered convergence check that divided by the floor, and fixed the estimand at matched compute); DX-21 (floor-based standard errors 0.00970 and 0.00177; the numbers' home is section 9.2, so here state the rule and point); DX-32 (24 of 24 rendered episodes of the Coupling-B grid drift towards a wall; rendered-pixel centroids, a diagnostic); CB-9 and DX-306 and DX-303 (for section 8.6: CB-9 graded against a three-seed spread; floors exist only for the sweep's p = 0.5 arm and the identification arm is ungraded; a four-run floor is uncertain by about ±40 %); DX-28 (p = 0.5).
FIGURES: Figure 10, floors_explorer.html, companion floors_explorer.png, height 460, carried below. Caption at most 120 words; it glosses "card", "floor basis", "beat", "M5.1e" and "M6.0" as printed (BRIEF section 5.2); each tab prints its confound, so the caption need not repeat the numbers (rule R3).
LISTINGS: none (Listing 3 may be referred to as the bitwise discipline that makes same-version comparisons meaningful).
LATEX: two displays: the contrast standard error in the unequal-k form section 9 uses, sd(Γ) = √(s_ISO²/k_ISO + s_JOINT²/k_JOINT), noting that equal k gives √((σ_ISO² + σ_JOINT²)/k); and MDE₈₀ = (z_α + z_0.8) sd(Γ). Section 9.1 points back here instead of re-deriving.
HONESTY LINES AND REGISTERED STRINGS: "recorded, not graded" (the position-drift diagnostics have no floors and were kept out of the registered family); a differenced test sees asymmetry and nothing else; "reference scale (cross-artifact)"; bias (b)'s readings are in section 9.1 (state here only the rule that every reading of a registered bias is reported, with a pointer); "Bias (b) reverses sign on the grid card" belongs to section 9.1.
FIX-LIST AND FINDINGS ITEMS OWNED: F5 (card to GPU; M4.4, M5.1e, M5.3, M5.3b, M5.5, M6.0, M6.2, M6.2b to study descriptions, codes only in Appendix C's key; floor-basis to "the floor-based standard error of Γ"; beat-reproducibility to "the check that an effect exceeds rerun noise"; re-floor to "re-measured reproducibility floor"; tree, digest and traced to "two versions of the code" and "per-field trajectory hashes"; plateau guard to "a registered convergence check, retired before the grid"; drift channels to "position-drift diagnostics (recorded, not graded)"; box to "machine"; launch batch to "the first floor study"); OI-5 (never "different hardware" for M5.3's floor); LEN (each rule with a one-sentence exhibit; the exhibits' detail to Appendix C; HW-1's numbers to section 9.2; bias (b) to section 9.1); P3-§6 (no "This section states" opening; rule statements may be bold once each, nothing else bold).
DEMO KEEPS (sections/08_methodology.md): each rule with its exhibit and its confound; Figure 10; section 8.6 whole. CHANGES: the jargon; the exhibits' detail to Appendix C; section 8.4's numbers become a pointer; section 8.5's bias (b) paragraph becomes a rule plus a pointer. DROPS: repeated numbers.
NOT HERE: "every bar in the paper is floor-graded"; "the RTX 5090 is less reproducible" (the intervals overlap, DX-35); the curriculum-difficulty ordering as a finding; "card" alone for METH-1's exhibit (GPU, code version and configuration); a registered status for M5.5's 20 % threshold.
DEPENDENCIES: section 9.1 uses rules 8.2 and 8.4 for design-stage power and the test; section 9.2 uses 8.4's check; section 10 item 6 uses 8.5; Appendix C (W5) holds every floor.
-->

GPU training is not reproducible run to run: the compiler chooses kernels by timing them and some reductions use atomics. A reproducibility floor is the standard deviation of a metric over identical reruns, with the same seed, configuration and code. Each rule below came from a defect in the project's record; Appendix C lists every floor.

<figure class="l-page">
  <iframe src="{{ 'assets/html/submission/floors_explorer.html' | relative_url }}" width="100%" height="472" style="border:none" title="Floors explorer: reproducibility floors per GPU, per artifact and per run length, and the confirmatory grid against its floor" loading="lazy"></iframe>
  <figcaption><strong>Figure 10.</strong> Reproducibility floors per GPU, per artifact and per run length, and the confirmatory grid against its floor, one tab each, with its confound. On the figure, "card" is the GPU, "box" the machine, "tree" a code version and "reps" identical reruns; M5.1e, M5.5 and M6.0 are keyed in Appendix C. "Traced" and "baseline" are the refactored and reference versions, compared by per-field trajectory hashes ("field digests"); "floor-basis sd(Γ)" is the floor-based standard error of Γ (§8.4). It cannot show contrasts without a floor (§8.6). <span class="figure-note">Status: point estimates over identical reruns, about ±40 % uncertain at four reruns<!-- N:DX-303 --> · Interact: click a tab or press ← / →; hover or tab to a mark.</span></figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/floors_explorer.png" class="img-fluid" alt="Reproducibility floors on two GPUs, rerun comparisons of two versions of the code, floor growth from the shorter to the longer run length, and the confirmatory grid's seed dispersion against its floor, each with its confound stated." caption="Static companion of Figure 10 for the printed PDF." %}
</div>

### 8.1 A bar without a floor is void

No acceptance threshold enters an analysis script without a measured floor for the quantity it grades, or an explicit UNDERPOWERED flag. A threshold below its instrument's noise cannot pass under the null, so its output is void, and a void test voids a PASS as it voids a FAIL. The rule followed four<!-- N:V5-1 --> bars with invented constants (Appendix C). In one, the denial study of §7 graded a condition with a 20 %<!-- N:COM-5 --> threshold, chosen at implementation, against a quantity whose rerun nondeterminism is 27.2 %<!-- N:COM-5 -->. Since the threshold sits below the noise, the condition is VOID; the observed 23.2 %<!-- N:COM-5 --> exceeded the threshold but not the noise.

Floors are facts per metric and per GPU. Re-measuring the Medium floor moved completion's 2.75-fold<!-- N:METH-1 --> and left survival's unchanged, 0.0129<!-- N:METH-1 --> against 0.0130<!-- N:METH-1 -->. The two studies differ in GPU, code version and configuration, so the exhibit cannot say which of them moved the completion floor. The floor is measured on the GPU that runs the grid.

Floors are facts per artifact. In a refactor of the environment code, the rerun floor measured on the reference version read zero, so two<!-- N:METH-2 --> diagnostic channels that differed between the versions looked like a semantic change. The refactored version then differed from itself 1 time in 4<!-- N:METH-2 --> on the same channels. An equivalence claim between A and B needs A against A and B against B as well as A against B.

### 8.2 Contrasts and power

A contrast is graded on its own standard error. For Γ, the difference between the JOINT and ISO arm means over $k_{\mathrm{JOINT}}$ and $k_{\mathrm{ISO}}$ seeds with seed standard deviations $s_{\mathrm{JOINT}}$ and $s_{\mathrm{ISO}}$,

$$
\operatorname{sd}(\Gamma) = \sqrt{\frac{s_{\mathrm{ISO}}^2}{k_{\mathrm{ISO}}} + \frac{s_{\mathrm{JOINT}}^2}{k_{\mathrm{JOINT}}}},
$$

which for equal $k$ is $\sqrt{(s_{\mathrm{ISO}}^2 + s_{\mathrm{JOINT}}^2)/k}$. The per-arm forms, each arm's own $s\sqrt{2/k}$, bracket that value without equalling it: at $k = 34$<!-- N:METH-3 -->, on the 1000<!-- N:DX-34 -->-update completion floors and a 0.03<!-- N:DES-4 --> effect, ISO's gave 92.1 %<!-- N:METH-3 --> power and JOINT's 62.8 %<!-- N:METH-3 -->, where the contrast's power was 76.7 %<!-- N:METH-3 -->.

A design-stage power statement is the minimum detectable effect at 80 %<!-- N:METH-7 --> power and the family-corrected level,

$$
\mathrm{MDE}_{80} = \big(z_\alpha + z_{0.8}\big)\,\operatorname{sd}(\Gamma),
$$

with $z_\alpha = 2.2365$<!-- N:DES-13 --> the Šidák-corrected critical value for the two co-primaries. The exclusion bound $X$ that §9 attaches to a null is this quantity on the grid's realized seed dispersion. A bare $2\sigma\sqrt{2/k}$ is the effect at which an uncorrected test would just reject, which it detects about half<!-- N:V4-1 --> the time; it survives only for grading an observed effect against a floor after the fact, labelled as such. The confirmatory seed count was first ruled at $k = 20$<!-- N:METH-4 --> on such a figure, without the Šidák correction; corrected, completion had 55.6 %<!-- N:METH-4 --> power against its motivating effect band, a slip caught before any run.

### 8.3 Floors move with the run, and gates must not divide by them

Floors grow with run length. From 500<!-- N:DX-34 --> to 1000<!-- N:DX-34 --> updates the completion floor grew 2.1-fold for ISO and 5.2-fold for JOINT<!-- N:METH-5 -->, with length confounded with machine.

A gate that divides by a floor diverges on more reproducible hardware. A registered convergence check, retired before the grid, divided each arm's late-training drift by its floor, so any nonzero drift fails as the floor goes to zero; it fired when JOINT's floor fell faster than its drift. The $T^*$ ruling of 2026-08-11<!-- N:METH-6 --> retired it as a gate, fixed the estimand as Γ at matched compute, and made Γ(t) required robustness evidence (§9.2).

### 8.4 The floor is a check, not the test variance

The floor and the test statistic are different variances. A floor comes from identical reruns at one seed, while a $k$-seed arm mean varies by seed as well. The confirmatory contrast is graded on the grid's own seed dispersion. The floor serves the check that an effect exceeds rerun noise, which uses the floor-based standard error of Γ: the display in §8.2 with floors in place of seed standard deviations (§9.2). For design-stage power, the floor gives an upper bound, labelled as one.

### 8.5 Instruments state what they are blind to

A differenced test sees asymmetry and nothing else. A condition of the form "no cross-arm difference in X" cancels any X present in both arms. In 24 of 24<!-- N:DX-32 --> rendered episodes of the Coupling-B calibration grid, the alive agents' centroid drifted towards a wall (rendered-pixel centroids, a diagnostic). That grid's inertness falsifier, logged before its data, included the condition "no cross-arm exposure/positioning difference", which could not see a drift present in both arms; the verdict it fed rests on its other conditions.

Measuring is not grading. A recorded channel becomes evidence only inside a registered analysis family, with a floor measured on its artifact. Position-drift diagnostics added before the grid are recorded for every grid run. They are recorded, not graded: adding them to the registered family after registration would have enlarged it and inflated its correction.

The differential drift between the arms, bias (b) of §9.1, changed sign between the four<!-- N:DES-10 --><!-- N:V6-4 --> floor studies that read it before unblinding, so §9.1 reports every reading.

### 8.6 Where this paper falls short of its own rules

Coupling B's Medium survival effect was judged only against a three-seed<!-- N:CB-9 --> spread (§6.4). The trained-policy contrasts of §5 and §6 come from two calibration grids without identical reruns: their spreads are seed ranges, and any floor shown beside them is a reference scale (cross-artifact). In the secondary design, floors exist only for the sweep arm at $p = 0.5$<!-- N:DX-28 -->; the intermediate sweep arms assume that floor, and the identification arm is ungraded<!-- N:DX-306 -->. ISO-4 has no identical reruns, so the contrasts that involve it are graded on seed dispersion alone, and the High-severity readout flags ISO-4 UNDERPOWERED for the check against rerun noise. The position-drift diagnostics have no floor. Every floor is itself a point estimate: measured on four<!-- N:DX-303 --> identical runs, a standard deviation is uncertain by roughly ±40 %<!-- N:DX-303 -->.

<!-- PAPER V2 DRAFT (PAPER V2 ruling, 2026-10-11): builder-drafted, not owner-approved -->

## 9 The pre-registered compositional test

<!-- STUB-SPEC
PURPOSE: The pre-registered test: its design (9.1), its results read in the registered order (9.2), and the one labelled recommendation the result motivates (9.3). Section 9.1 is the home of the δ design error (F3); section 9.2 is the home of every contrast; section 9.3 is the home of the recommendation (F4).
SUBSECTIONS (H3): 9.1 Design; 9.2 Results; 9.3 A recommendation and its scope (new: STRUCTURE.md section 5).
WRITER: W6. Also ledger_proposals/W6.md with V6-1, V6-2, V6-3 exactly as BRIEF section 7 gives them, each re-verified at its source; W1, W2 and W5 cite them. BUDGET: 2,100 prose words (9.1 about 900, 9.2 about 1,050, 9.3 about 150; the demo's: 3,103); captions at most 130 (Figure 11), 120 (Figure 12), 130 (Figure 13).
9.1, IN ORDER: Def. 8 (ISO, JOINT, Γ(θ*); the co-primaries; survival made co-primary on 2026-08-02 before the grid, DES-12). Prop. 4, renamed as an upper bound (for example "a transfer bound for a fixed policy"), stated in words, with no display, no constant and no ISO-against-JOINT slack contrast (C3, N6, P3-N7; Q4i): for a fixed policy, the difference in return between two configurations is bounded above in terms of how far their transition and observation kernels differ; every ISO training configuration differs from θ* on the states where both couplings act at once, the region the counter was built to measure; then the honesty note (TF:636-643, must appear): it bounds what ISO can be guaranteed to transfer, not what happens; it does not lower-bound Γ; compositional generalization can emerge from isolated training; it motivates the experiment and the experiment decides; the theory's prediction about ISO's exposure to that region was not tested, because the counter is co-active only in all-on configurations. The arms (the table is the numeric home of DES-7, DES-8, DES-14, DES-16; refer to Figure 2): what is matched (network, hyperparameters, DX-2; budget DX-3, DES-13; one evaluation draw, DES-13). Estimand and test in three sentences, pointing to section 8.2 for the formula (no estimator display): Γ at matched compute; Šidák m = 2, z_α = 2.2365, normal z, unpaired; positive covariance, the expected sign, makes the unpaired test conservative (P3-N14: never "any induced covariance"; log:3143-3146); graded on the grid's own seed dispersion; the floor serves only the check against rerun noise and as an upper-bound power basis; intervals conditional on the one evaluation draw. Seeds in two sentences (DES-1 to DES-3: registered k = 40 and a cap of 60 under the registered seed rule; k = 46 on the RTX PRO 6000's re-measured floor; on the RTX 5090s the rule required 72, and on 2026-09-22 the cap was raised to 72, a deviation from a registered rule, recorded as one, made before unblinding and conservative; seeds 1 to 60 are a prefix, so the registered k = 60 analysis is reported beside it); realized completion power 71.6 % at k = 72 and 60.2 % at k = 60 (DES-6), reported, not re-engineered; design-stage power detail to Appendix D. The endpoint confound and the secondary design (DES-7: threefold; the sweep holds each coupling at 0.5 while co-occurrence p moves, in the spirit of DBCA, keysers2020; on the triangle of training mixtures a fixed frequency forces the fire-only share to equal p, DES-9; identification arms at frequency 0.4 on a parallel line; secondary arms k = 20 with δ off, so the p = 0 sweep arm trains on ISO-4's mixture; JOINT differs from every secondary arm in carrying δ = 1.0; all of it non-verdict-bearing). THE DESIGN ERROR (F3 home; BRIEF section 7, rows 1 to 11; V6-1 to V6-3, DES-12, DES-15): one paragraph owning it plainly, with the dates; the direction (inflates Γ; JOINT's active share 1.5 times ISO's, DX-31); ISO's configured no-element share of 0 true nominally and false behaviourally (DES-16); the composition under test is A × B; the registration before unblinding and on the owner's attestation; the lead-in is not "Registered biases, stated before the result". Bias (b) with all its readings (DES-10: +0.01209 on the first floor study and +0.0179 on the 2026-09-08 re-measured floor, both RTX PRO 6000, against −0.0083 on the GPU that ran the grid; DES-11's training-log slopes): its sign reverses on the grid GPU; no direction is claimed. The registered readings as one-line rules, verbatim in Appendix D; quote only the ISO-4 rule (log:4016-4029). Blinding in three sentences (DES-12; DX-416; DES-15's attestation; DX-405; DX-411), details in Appendix F. Define once: unblinding, the confirmatory family, a registered outcome, GPU 1 to 3 (BRIEF section 5.2).
9.2, IN THE REGISTERED ORDER (each verdict before its numbers): Γ (Figure 11; the contrast table is the home of RES-1 to RES-3, RES-6 to RES-9, RES-14, RES-15 with DX-19, DX-20, DX-23, DX-26: verdicts in prose, intervals by reference to the table); the falsifier (RES-5, reported as registered; branch B stands, not C; under Def. 2 the asymmetry is between a penalized channel and a rewarded one); the inert-share correction (Γ₄ named at first use as the corrected gap, JOINT − ISO-4; the registered string; "the branch label stays B"; completion's second exclusion bound, X₄ = 0.0488; branch B's headline "no longer holds as worded"; Γ₄ is across GPUs, HW-4; Γ₄′ named at first use as the same-GPU replicate of the correction, JOINT minus the p = 0 sweep arm, which trains on ISO-4's mixture on JOINT's GPU, proposed on 2026-09-26 after Γ₄ was seen and unable to change its qualifier, DES-15; it agrees; the replicate difference RES-9; B̂ = ISO-4 − ISO reported without a test and with no verdict, RES-7; Γ = Γ₄ + B̂ holds by construction and is not a second finding); the correction's two limits (home: Γ₄'s upper bound +0.63 above Γ's lower +0.47; ISO to ISO-4 changes active share 2/3 to 1 and per-coupling frequency 1/3 to 1/2 together, DES-14, DES-7); Γ(t), "sign unstable over the final half" on both (Figure 12; RES-11 first, then RES-12's shape, DX-25's range through t = 850 as −0.37 to +0.36 points, RES-13's lean; completion is unresolved and leaning negative, not unaffected; the single-GPU curve has the same signs); T = 2000 in one sentence (RES-15, DX-23, DES-11: the drift has not visibly reversed, which is all it may be cited for); what the secondary design adds and where its fit fails (Figure 13; §1 INTRODUCTION item 3 obligation: the fire-only-share slope γ_n predicts ISO-4 − ISO at +0.79 points, SEC-3, inside B̂'s interval, without attributing B̂ to the fire-only share as such; the co-occurrence slope γ_p, SEC-1, raises survival across the sampled region but also raises per-coupling frequency, and its plane, fitted on p up to 0.5, predicts +3.26 points for JOINT − ISO-4 at p = 1, SEC-4, against −0.03 and +0.13 measured: it does not extrapolate to JOINT, N12; secondary, non-verdict-bearing, many 95 % intervals, none family-corrected; the rest in Appendix H); where the survival gap lives in one sentence (RES-10, DX-22, DX-406: about 0.11 agents per episode, descriptive); the High readout (RES-14, DX-26: the a-fortiori exclusion with its sentence verbatim; within rerun noise; not a held-out test; at High Coupling B is live, CB-5, and Coupling A marginal, CA-4: the mirror of Medium, pointing to sections 5.3 and 6.4); mediation VOID (SEC-7, DX-29; diagnosed after the run without changing the rule; the counter counts what only Coupling A produces, CO-4); hardware and reproducibility in one sentence each (HW-1 and DX-21: seed dispersion over the floor and survival Γ 5.40 times its floor-based standard error, clearing the check against rerun noise; HW-4 and DX-5: the GPU blocks, pointing to Appendix F; evaluation reproducibility, pointing to section 11, with no absolute-value bars anywhere, M1).
9.3: the confound's logic as a claim (a joint-against-isolated comparison that leaves the active share free mixes it with composition; true by construction, as the threefold frequency is, ENDPOINT CONFOUND log:4549-4570); the recommendation, labelled as one that this single environment motivates (for example, opening with "We recommend"); the exclusion caveat by pointer to section 9.2; the one-environment scope (section 10 points here). No "therefore", "so" or "thus" before it. It is not a contribution.
REQUIRED FACTS (all tagged; values in BRIEF section 8): DES-1 to DES-16; RES-1 to RES-15; SEC-1 to SEC-7; HW-1 to HW-4; DX-2, DX-3, DX-5, DX-18 to DX-31, DX-39, DX-402, DX-404 (only if the t value is mentioned: printed, not applied), DX-405, DX-406, DX-411, DX-413, DX-416; V6-1 to V6-3; METH-6, METH-7; CAL-3, CA-1, CB-1, COM-6 (θ*); CB-5, CA-4 (High readout pointers); ENV-1, ENV-6, ENV-11; CO-4.
CITATIONS: keysers2020; dewitt2020ippo.
FIGURES (carried below; captions rewritten to the caps; numbers the figure prints are not repeated, rule R3): Figure 11, ladder_registered_readings.html, companion ladder_registered_readings.png, height 1000 (glosses "rung", "unit", "floor basis", "sweep_c50_p000" and "Γ₄′" as printed; status per row: registered for Γ, sensitivity arm for Γ₄, secondary for Γ₄′, B̂ a registered estimand with no test; cannot show arm-symmetric effects, evaluation-set sampling, other budgets, or which of the two quantities carries ISO-4's rise). Figure 12, gamma_t_final_half.html, companion gamma_t_final_half.png, height 480 (the registered string first; only t = 1000 is registered, earlier intervals descriptive; no trend; glosses "card" and "single-card curve"). Figure 13, simplex_secondary.html, companion simplex_secondary.png, height 820 (status chips verbatim; glosses "no-element share" as the fire-only share, "m" and "n" as μ and ν, the sweep and identification arm codes, γ_p and γ_n as the co-occurrence and fire-only-share slopes; the γ_n pair that fits and the γ_p pair that misses, B10; cannot separate per-coupling frequency, co-occurrence and active share). Refer to Figures 2 and 3; do not re-embed them. Keep the simplex in section 9.2 (Q9).
LISTINGS: none. LATEX: Def. 8's display only. No estimator display (section 8.2 holds it). No Prop. 4 display.
HONESTY LINES AND REGISTERED STRINGS: branch_B section 5 lines 1, 2, 3, 4, 6, 7, 8, 9, 10 (all but 5, which points to section 10). Verbatim: "does not survive the inert-share correction"; "sign unstable over the final half"; "second exclusion bound"; REJECT and null; UNDERPOWERED (the k = 60 analysis, both change points, T = 2000, ISO-4 for the check at High); VOID; "non-verdict-bearing" once in 9.1, then "secondary"; the a-fortiori sentence; "sensitivity arm"; "fire-only"; "at matched compute"; branch A "did not occur"; "the branch label stays B". Bias (b) reverses sign on the grid GPU. B̂ carries no verdict word.
FIX-LIST AND FINDINGS ITEMS OWNED: C3, N6, P3-N7 (Prop. 4); F3 (home), O1, P1-N1, P3-N19, N5 (the design's own premise may be cited); F4 (home, 9.3); F5 (every term of BRIEF section 5.2 that section 9 uses; codes only in Appendix H's table; S1 to S6 only inside Appendix D's quotation); M1 (no pipe; the evaluation figure lives in section 11); N12 ("does not extrapolate"); N16 and LEN (each number once, table or prose; the demo's three-row readings table becomes one-line rules with a pointer to Appendix D; the k history in two sentences; design-stage power to Appendix D; blinding in three sentences); N17 (the demo's discussion paragraph goes: no "cost 20 runs", no "one level down" echo, no "a registered design caught it"; "(§5–§6)" where the evidence spans both); P3-N14; P1-N7 (no branch_B lags); P1-b; P1-c (no day count); P3-U3 (class C: not added); P3-N20 and P3-U1 (class C: Γ₄'s survival X not stated); Q4h, Q4i, Q9, Q17, Q18, Q25.
STYLE: verdict before numbers; plain topic sentences in place of the demo's seven bold-led paragraphs in a row (bold only for registered strings and the proposition's run-in label); no "Each rung's verdict sits before its numbers", "The shape, after the verdict" or "Two limits bound the correction" announcements; sentences of at most 40 words outside quotations; body dates only those a claim needs (2026-08-02, 2026-08-13, 2026-08-16, 2026-09-09 to 09-22, 2026-09-18, 2026-09-22, 2026-09-26).
DEMO KEEPS (sections/09_compositional_test.md): the registered reading order; Figures 11 to 13; one contrast table; the falsifier with its margin; the High readout's registered wording; mediation VOID with its diagnosis; the γ_n-fits and γ_p-fails pair. CHANGES: F5 throughout; Prop. 4 renamed and stated in words; the design-error paragraph replaces "Registered biases, stated before the result"; the recommendation moves to 9.3, labelled; "does not extrapolate" replaces "saturates"; each number once; the readings table to one-line rules. DROPS: "A registered design caught it"; "The arm … cost 20 runs"; the second statement of every tabled number; the estimator display; Prop. 4's display and its ISO-against-JOINT contrast.
NOT HERE: every item of branch_B section 8 (BRIEF section 6.3); "significant" for B̂; Γ = Γ₄ + B̂ as a finding; "the dose design attributes"; Γ(t) as a trend; T = 2000 as "Γ holds"; the High readout as held-out; that the cross-GPU caveat "finds support"; that the RTX 5090 is less reproducible; mediation as a result; any number from the log alone (BRIEF section 17); "irreducible"; "pre-registered" for the correction.
DEPENDENCIES: section 1's promises (γ_n and where the plane fails; the threefold confound); section 6.5's scope note; section 7's δ-inert; section 8's rules 8.2 and 8.4; Appendices D to H (W6), Appendix C (W5, floors), Appendix F (GPU blocks).
-->

### 9.1 Design

**Definition 8 (Training protocols and the compositional gap).** Let $J_\theta(\pi)$ be the expected episodic return of joint policy $\pi$ in $\mathcal{M}_\theta$, and let $\theta^*$ be the test configuration, every stressor on at a severity held out of training. Let $\Theta_{\mathrm{iso}}$ be the configurations in which at most one of $\kappa_A$, $\kappa_B$, $\delta$ is nonzero; the fire ($\beta > 0$) burns in all of them. The ISO protocol trains one policy $\pi_{\mathrm{iso}}$ on a uniform mixture of configurations in $\Theta_{\mathrm{iso}}$. The JOINT protocol trains one policy $\pi_{\mathrm{joint}}$ on a mixture whose support includes configurations with every stressor on, at training severities only. The compositional gap is

$$
\Gamma(\theta^*) = J_{\theta^*}(\pi_{\mathrm{joint}}) - J_{\theta^*}(\pi_{\mathrm{iso}}).
$$

The registered test replaces $J$ by an outcome metric's mean over evaluation episodes, on two co-primaries: task completion, the founding primary, and survival rate (§3.5). Survival became a co-primary on 2026-08-02<!-- N:DES-12 -->, before the grid, because, as that ruling records, both couplings' calibration grids had moved survival while their completion effects sat at or below the floors then measured (§5–§6).

**Proposition 4 (A transfer bound for a fixed policy).** For a fixed policy and two configurations that share the reward, the difference between its discounted returns is bounded above by a term that grows with how far their transition and observation kernels differ. Every configuration in $\Theta_{\mathrm{iso}}$ differs from $\theta^*$ on the states where both couplings act at once, a collapse-seeded fire within perception-attenuation range of an agent (proof idea in Appendix A).

Proposition 4 bounds what ISO can be *guaranteed* to transfer, not what happens. It does not lower-bound Γ, and compositional generalization can emerge from isolated training; it motivates the experiment, and the experiment decides. Its prediction about ISO's exposure to that region was not tested, because the counter built to measure visits there (§6.5) is co-active only in all-on configurations (§9.2).

The test configuration θ\* has every stressor on at the held-out severity, β 0.49, $\kappa_A$ 0.06, $\kappa_B$ 1.0, δ 1.0<!-- N:CAL-3 --><!-- N:CA-1 --><!-- N:CB-1 --><!-- N:COM-6 -->, and no arm trains at β 0.49<!-- N:CAL-3 --> (Figure 2 in §1). In the table, μ is the per-coupling frequency, the share of training episodes carrying a given coupling, and p the co-occurrence, the share carrying both. The active share is the share with at least one behaviourally active stressor, and the fire-only share ν, counted behaviourally, is the rest.

| arm | components, each at β 0.43 and 0.70<!-- N:CAL-3 --> | μ | p | active share | fire-only ν |
|---|---|---|---|---|---|
| ISO | A-only, B-only, δ-only; 6 × 1/6<!-- N:DES-16 --> | 1/3<!-- N:DES-7 --> | 0<!-- N:DES-7 --> | 2/3<!-- N:DES-14 --> | 1/3<!-- N:DES-8 --> |
| ISO-4 | A-only, B-only; 4 × 1/4<!-- N:DES-16 --> | 1/2<!-- N:DES-14 --> | 0<!-- N:DES-14 --> | 1<!-- N:DES-14 --> | 0<!-- N:DES-14 --> |
| JOINT | all-on; 2 × 1/2<!-- N:DES-16 --> | 1<!-- N:DES-7 --> | 1<!-- N:DES-7 --> | 1<!-- N:DES-14 --> | 0<!-- N:DES-14 --> |

ISO-4, a sensitivity arm outside the confirmatory family, is ISO without its two δ-only components, and the corrected gap Γ₄ is JOINT − ISO-4. All arms share the network and the IPPO hyperparameters (Appendix B<!-- N:DX-2 -->), one shared-parameter policy per training seed<!-- N:ENV-11 --><d-cite key="dewitt2020ippo"></d-cite>, a budget of T\* = 1000<!-- N:DES-13 --> updates of 32,768 environment steps each<!-- N:DX-3 -->, and one evaluation draw, seed 0 × 512 episodes at θ\*<!-- N:DES-13 -->.

Γ is read at matched compute, at the fixed budget T\*<!-- N:METH-6 -->, and convergence is claimed nowhere. The confirmatory family is the two co-primary tests, Šidák-corrected (m = 2<!-- N:DES-13 -->): unpaired normal z tests against $z_\alpha = 2.2365$<!-- N:DES-13 --> on the contrast's standard error from each arm's seed dispersion (§8.2). A null carries its exclusion bound X, the 80 %-power MDE at that α<!-- N:METH-7 -->. Positive cross-arm covariance, the expected sign given the shared seed integers, makes the unpaired test conservative. Floors serve only the check that an effect exceeds rerun noise (§8.4) and, as an upper bound, design-stage power (Appendix D); every interval is conditional on the one evaluation draw.

The design registered k = 40<!-- N:DES-1 --> seeds per arm and a seed rule, capped at 60<!-- N:DES-1 -->, that recomputes k from floors re-measured on the grid's GPU. It gave 46<!-- N:DES-2 --> on an RTX PRO 6000 and 72<!-- N:DES-3 --> on GPU 1, the RTX 5090 that ran the rest of the grid and every confirmatory run (GPU 2 and GPU 3 are two more of that model<!-- N:DX-5 -->; Appendix F). Raising the cap to 72 on 2026-09-22<!-- N:DES-3 --> was a deviation from a registered rule, recorded as one, made before unblinding, and conservative, since added seeds favour neither sign of Γ. The registered k = 60 analysis, on seeds 1–60<!-- N:DES-1 --><!-- N:RES-3 -->, is reported beside it; realized completion power at a 0.03<!-- N:DES-4 --> effect is 60.2 % and 71.6 % at k = 60 and 72<!-- N:DES-6 -->.

JOINT sees each coupling three times as often as ISO<!-- N:DES-7 -->, so Γ mixes per-coupling frequency with composition. A secondary sweep holds μ = 0.5 while p moves from 0 to 0.5<!-- N:DX-28 -->, in the spirit of DBCA<d-cite key="keysers2020"></d-cite>, which the ISO and JOINT endpoints do not follow. On the triangle of training mixtures $\mu = (1 + p - \nu)/2$, so a fixed μ forces ν = p<!-- N:DES-9 -->. Identification arms on the parallel line μ = 0.4, ν = 0.2 + p<!-- N:DES-9 --> identify a plane in p and ν (Appendix H). Secondary arms run k = 20<!-- N:DES-13 --> seeds, with δ off, on GPU 1<!-- N:DX-5 -->. The p = 0<!-- N:DX-28 --> sweep arm therefore trains on ISO-4's mixture on JOINT's GPU, and JOINT, unlike every secondary arm, carries δ = 1.0<!-- N:COM-6 -->, inert (§7). The secondary design is **non-verdict-bearing**.

The registered design contains an error, and the bias it creates inflates Γ. Communication denial had been found inert on 2026-07-30<!-- N:V6-2 --> (§7). The design registered on 2026-08-02<!-- N:V6-3 --> kept δ in θ\* for fidelity to the registration and excluded it from the secondary sweeps because it was inert. It still gave ISO two δ-only components of six<!-- N:V6-3 -->. A question it set for reviewers judged the arms symmetric on δ, on the premise that neither trains on δ = 1.0<!-- N:COM-6 -->, which is false for both, and asked for a second opinion. So a third of ISO's training episodes<!-- N:DES-8 --> are fire-only, which the design never counted: ISO's configured no-stressor share of 0<!-- N:DES-16 --> is true nominally and false behaviourally, and JOINT's active share is 1.5 times ISO's<!-- N:DX-31 -->. A review of the registered design identified this on 2026-08-16<!-- N:V6-1 -->, before the grid, noting that the confirmatory arm applied a different rule to the same fact as the sweeps. The grid began on 2026-09-09<!-- N:DES-12 --> without the correction. The bias, its direction and ISO-4 with its reading rule were registered on 2026-09-18<!-- N:DES-15 -->, mid-grid (120 of 252 runs<!-- N:DES-15 -->) and before unblinding, on our attestation, recorded with the ruling, that no outcome mean had been computed or viewed. The composition actually tested is A × B.

Bias (b) is the registered caveat on differential drift: JOINT − ISO completion drift over the last 100 updates<!-- N:DES-10 -->, a local sensitivity estimate and never a bound. It read +0.0242<!-- N:V6-4 --> per 100 updates on the confirmatory arms' floor study at 1000 updates and +0.01209<!-- N:DES-10 --> on the grid's launch floor study (2026-08-10<!-- N:DES-5 -->). It read +0.0179<!-- N:DES-10 --> on the 2026-09-08 re-measured floor, all three on an RTX PRO 6000, but −0.0083 on GPU 1<!-- N:DES-10 -->. In the 2000-update subsample (§9.2), the differential training-log slopes over updates 500–1000 are +0.00247 (completion) and +0.00718 (survival) per 100 updates<!-- N:DES-11 -->. The sign reverses on the grid GPU, and no direction is claimed.

The registered outcomes, branches A–D of 2026-08-13<!-- N:DES-12 --> and a fifth<!-- N:DX-405 --> cell, $A_c$, added before unblinding, are in Appendix E. Branch B (survival only) also needs a registered falsifier to pass. The ISO-4 rule states that if Γ rejects on a co-primary and "**Γ₄'s CI on that co-primary includes 0 or its sign is opposite**, the paper states that the effect **does not survive the inert-share correction**". If Γ and Γ₄ are both null, "Γ₄ is quoted as a second exclusion bound". Appendix D quotes every rule with its date.

The grid ended on 2026-09-22<!-- N:DES-12 -->; its runner computes no cross-arm quantity. On 2026-09-26<!-- N:DX-405 --> the pre-unblind rulings fixed the statistic, the sign rule, k = 72<!-- N:DES-3 --> as primary and $A_c$. Unblinding, the first computation of any outcome contrast, followed the same day<!-- N:DES-12 --> (Appendix F).

### 9.2 Results

<figure class="l-page">
  <iframe src="{{ 'assets/html/submission/ladder_registered_readings.html' | relative_url }}" width="100%" height="1012" style="border:none" title="Registered readings in order: Gamma, Gamma4, Gamma4 prime and B-hat on both co-primaries" loading="lazy"></iframe>
  <figcaption><strong>Figure 11.</strong> The registered readings in order, one row (a “rung”) per contrast: Γ, with the registered k = 60<!-- N:DES-1 --><!-- N:RES-3 --> analysis (labelled “prefix”); Γ₄; Γ₄′, JOINT minus the p = 0<!-- N:DX-28 --> sweep arm (labelled sweep_c50_p000); and B̂, which carries no verdict. “Unit n” is GPU n, “cross-unit” means across GPUs, and the “seed ladder” is the registered seed rule (§9.1). The grey band is the 80 %-power MDE<!-- N:METH-7 -->; the stipple, on Γ only, is ±1 floor-based standard error of Γ (labelled “floor basis”). The figure cannot show effects present in both arms, evaluation-set sampling, other budgets, or which of active share and per-coupling frequency carries the ISO-4 − ISO difference. <span class="figure-note">Status: registered (Γ); sensitivity arm (Γ₄); secondary (Γ₄′) · Interact: step rows with ◀ ▶ or the arrow keys; toggle the bands; “table view”.</span></figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/ladder_registered_readings.png" class="img-fluid" alt="Two forest plots, completion and survival, of the registered contrasts in order with their Šidák-corrected intervals and verdicts" caption="Static companion of Figure 11 for the printed PDF." %}
</div>

At k = 72<!-- N:DES-3 -->, Γ rejects on survival and is null on completion (Figure 11 and the contrast table). The completion null excludes a joint-training gain larger than 0.66 points<!-- N:RES-1 -->, the upper end of its interval. Its exclusion bound X, the gap of either sign the design would detect with 80 %<!-- N:METH-7 --> power, is 3.29 points<!-- N:RES-1 -->, and the negative point estimate does not reject. The registered k = 60<!-- N:DES-1 --><!-- N:RES-3 --> analysis reads the same and is flagged UNDERPOWERED.

All contrasts at θ\* and T\* = 1000<!-- N:DES-13 --> unless the row says otherwise, in points (rate × 100), with Šidák-corrected 95 %<!-- N:DES-13 --> intervals unless marked; k is given in the order of the contrast's two arms.

| contrast | k | completion | survival | status |
|---|---|---|---|---|
| Γ = JOINT − ISO | 72 / 72<!-- N:DES-3 --> | null: −1.73 [−4.12, +0.66], z −1.62<!-- N:RES-1 --> | REJECT: +0.96 [+0.47, +1.44], z +4.43<!-- N:RES-2 --> | confirmatory |
| Γ, registered k = 60 analysis | 60 / 60<!-- N:DES-1 --> | null: −2.17<!-- N:RES-3 --> [−4.86, +0.52]<!-- N:DX-20 -->, z −1.80<!-- N:RES-3 --> | REJECT: +1.04<!-- N:RES-3 --> [+0.54, +1.55]<!-- N:DX-20 -->, z +4.67<!-- N:RES-3 --> | seeds 1–60<!-- N:RES-3 -->, UNDERPOWERED |
| Γ₄ = JOINT − ISO-4 | 72 / 20<!-- N:DES-3 --><!-- N:DES-13 --> | null: −1.26 [−4.81, +2.28], z −0.80<!-- N:RES-6 -->; second exclusion bound | null: −0.03 [−0.68, +0.63], z −0.09<!-- N:RES-6 --> | sensitivity arm, across GPUs |
| Γ₄′ = JOINT − the p = 0<!-- N:DX-28 --> sweep arm | 72 / 20<!-- N:DES-3 --><!-- N:DES-13 --> | null: −2.47<!-- N:RES-8 --> [−6.16, +1.22], z −1.50<!-- N:DX-19 --> | null: +0.13 [−0.56, +0.81], z +0.41<!-- N:RES-8 --> | secondary, same GPU, read at $z_\alpha$ |
| B̂ = ISO-4 − ISO | 20 / 72<!-- N:DES-13 --><!-- N:DES-3 --> | −0.46<!-- N:RES-7 --> [−4.05, +3.12]<!-- N:DX-19 --> | +0.98 [+0.33, +1.63]<!-- N:RES-7 --> | no registered test, no verdict; across GPUs |
| replicate difference: p = 0<!-- N:DX-28 --> sweep arm − ISO-4 | 20 / 20<!-- N:DES-13 --> | +1.21 [−2.79, +5.20], 95 %<!-- N:DX-19 --> | −0.15 [−0.86, +0.56], 95 %<!-- N:RES-9 --> | secondary, across GPUs |
| $\Gamma_H$, all-on at β = 0.70<!-- N:CAL-3 --> | 72 / 72<!-- N:DES-3 --> | null: −0.79<!-- N:RES-14 --> [−3.26, +1.68]<!-- N:DX-26 --> | null: +0.38<!-- N:RES-14 --> [−1.46, +2.23]<!-- N:DX-26 --> | evaluation only, out of family, not held out |
| $\Gamma_{H,4}$ = JOINT − ISO-4 at β = 0.70<!-- N:CAL-3 --> | 72 / 20<!-- N:DES-3 --><!-- N:DES-13 --> | null: −0.75 [−3.87, +2.36]<!-- N:DX-26 --> | null: −1.28 [−3.50, +0.95]<!-- N:DX-26 --> | no reading rule of its own |
| Γ(2000) | 4 / 4<!-- N:RES-15 --> | +0.03<!-- N:RES-15 --> [−3.63, +3.69]<!-- N:DX-23 -->, 95 % | +1.59 [−0.02, +3.19]<!-- N:RES-15 -->, 95 % | descriptive, UNDERPOWERED |

The registered falsifier passes. It requires the completion contrast to exclude, in standardized units, an effect as large as the observed survival effect. With $z_c$ and $z_s$ the two statistics Γ / sd(Γ), $\lvert z_c\rvert + z_\alpha = 3.855 < 4.433 = \lvert z_s\rvert$<!-- N:RES-5 --> (4.040 < 4.673 at k = 60<!-- N:RES-5 -->). Branch B stands, completion null and survival positive, and branch C does not apply. Under Definition 2 the asymmetry is between a penalized channel and a rewarded one: the reward prices every death at $d_p = 0.5$<!-- N:ENV-1 --> whatever its cause and never reads the hazard. Branch A, the founding hypothesis, did not occur, and neither did $A_c$.

Γ₄ is null on survival. By the registered rule, Γ rejects and Γ₄'s interval contains 0, so the survival effect **does not survive the inert-share correction**, and this paper does not call it a composition effect. The branch label stays B, because the rule fixes it by Γ. Branch B's registered headline, "composition is paid in agents, not task return", no longer holds as worded. On completion both contrasts are null, so Γ₄ is a **second exclusion bound**, X₄ = 0.0488 (4.88 points)<!-- N:RES-6 -->.

Γ₄ is a contrast across GPUs: ISO-4 trained on GPU 2, JOINT on GPU 1<!-- N:HW-4 -->. Γ₄′, the same-GPU replicate of the correction, is JOINT minus the p = 0<!-- N:DX-28 --> sweep arm (§9.1). It was proposed on 2026-09-26<!-- N:DES-15 -->, after Γ₄ was seen and before that arm was read, and by rule it cannot change Γ₄'s qualifier. It agrees: null on both co-primaries.

B̂, ISO-4 − ISO, has no registered test and no verdict, and no magnitude threshold on it was registered. Because Γ = Γ₄ + B̂ holds identically for arm means, a B̂ close to Γ restates a Γ₄ close to 0 and is not a second finding.

Γ₄'s upper bound, +0.63 points<!-- N:RES-6 -->, lies above Γ's lower bound, +0.47<!-- N:RES-2 -->, so the correction excludes a large composition effect but leaves a smaller one possible. Removing the δ-only episodes also raises both the active share, from two thirds to one<!-- N:DES-14 -->, and each coupling's frequency, from a third to a half<!-- N:DES-7 --><!-- N:DES-14 -->, and B̂ alone cannot say which matters. What Γ₄ does say is that, once the active share is matched, JOINT's remaining differences add nothing detectable to survival, although JOINT still sees each coupling twice as often as ISO-4<!-- N:DES-14 --> and always in combination.

Γ(t) is **sign unstable over the final half** on both co-primaries<!-- N:RES-11 --> (Figure 12; Appendix G gives every value): the registered rule calls the result budget-robust only if all 11 point estimates over updates 500–1000<!-- N:DES-13 --> share one sign. As registered, the instability is the finding, and every reading here holds at matched compute only. Survival Γ(t) stays between −0.37 and +0.36 points through update 850<!-- N:DX-25 -->, every interval containing zero. It reads +0.56, +0.83 and +0.96 points at updates 900, 950 and 1000<!-- N:RES-12 -->, the only checkpoints whose Šidák interval excludes zero: the survival gap opens only in the last fifth of the budget<!-- N:RES-12 -->. Completion is negative at every checkpoint from update 700, 70 % of the budget<!-- N:RES-13 -->, and its interval excludes zero only at update 750, −1.47 points [−2.83, −0.10]<!-- N:RES-13 -->, descriptively. Completion is unresolved and leans negative.

<figure class="l-page">
  <iframe src="{{ 'assets/html/submission/gamma_t_final_half.html' | relative_url }}" width="100%" height="503" style="border:none" title="Gamma over the final half of training, completion and survival" loading="lazy"></iframe>
  <figcaption><strong>Figure 12.</strong> <strong>Sign unstable over the final half</strong>, on both co-primaries<!-- N:RES-11 -->. Γ(t) is JOINT − ISO over the final half of training, with Šidák whiskers. A ringed sign differs from the sign at T&#42;; rule (iv) is the pre-unblind sign ruling quoted in Appendix D. Only the checkpoint at T&#42; is the registered Γ; earlier intervals are descriptive. “Grid card” is GPU 1 and “post-unblind card” GPU 3; the “single-card curve” re-evaluates the T&#42; checkpoints on GPU 3. The dotted box is ±1 floor-based standard error of Γ (labelled “floor basis”). The figure cannot show where either difference goes after T&#42;. <span class="figure-note">Status: registered at T&#42;, descriptive before · Interact: hover a checkpoint; toggle the single-card curve and the box.</span></figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/gamma_t_final_half.png" class="img-fluid" alt="The retained checkpoints over the final half of training of the joint-minus-isolated difference in completion and in survival, each with its Šidák interval, labelled sign unstable over the final half" caption="Static companion of Figure 12 for the printed PDF." %}
</div>

The 2000-update subsample (4 seeds per arm<!-- N:RES-15 -->, UNDERPOWERED) keeps a positive differential training-log slope over updates 1000–2000, +0.00204 (survival) and +0.00384 (completion) per 100 updates<!-- N:DX-23 -->, as over 500–1000 (§9.1). The drift it measures has not visibly reversed, which is all it may be cited for.

The secondary design (Figure 13; Appendix H) reports 95 %<!-- N:DX-413 --> intervals that are not family-corrected. At ISO's fire-only share of 1/3<!-- N:DES-8 -->, the survival plane's fire-only-share slope γ<sub>n</sub> predicts ISO-4 − ISO = +0.79 points<!-- N:SEC-3 -->, inside B̂'s interval. This does not attribute B̂ to the fire-only share as such, because at fixed p a move in ν also moves μ. The co-occurrence slope γ<sub>p</sub> is positive across the sampled region, but moving single-stressor into both-stressor episodes also raises each coupling's frequency, and the triangle does not separate the two. Fitted on p up to 0.5<!-- N:DX-28 -->, the plane predicts JOINT − ISO-4 = +3.26 points at p = 1<!-- N:SEC-4 -->, far above the measured Γ₄ and Γ₄′: γ<sub>p</sub> does not extrapolate to JOINT.

<figure class="l-page">
  <iframe src="{{ 'assets/html/submission/simplex_secondary.html' | relative_url }}" width="100%" height="832" style="border:none" title="Secondary design on the triangle of training mixtures, with plane predictions beside measured contrasts" loading="lazy"></iframe>
  <figcaption><strong>Figure 13.</strong> The secondary design; the change point is labelled “knee”. Left: the triangle of training mixtures in co-occurrence p and fire-only share ν (labelled n), lines of fixed per-coupling frequency μ (labelled m), and the arms. Right: the secondary estimates, where γ<sub>p</sub> and γ<sub>n</sub> are the co-occurrence and fire-only-share slopes, the “dose slope” is the sweep's slope in p, and the “no-element share” is the fire-only share's part of the sweep's endpoint change. Below, the plane's γ<sub>n</sub> prediction sits beside B̂, which it fits, and its γ<sub>p</sub> prediction beside Γ₄ and Γ₄′, which it misses; the p = 0<!-- N:DX-28 --> sweep arm is labelled sweep_c50_p000. The figure cannot separate per-coupling frequency, co-occurrence and active share. <span class="figure-note">Status: secondary · Interact: switch the metric; toggle the predictions; hover.</span></figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/simplex_secondary.png" class="img-fluid" alt="A triangle of training mixtures by share of both-stressor and fire-only episodes, locating the secondary arms, ISO, ISO-4 and JOINT, beside the secondary estimates and the plane predictions next to the measured contrasts" caption="Static companion of Figure 13 for the printed PDF." %}
</div>

On a secondary metric outside the family, descriptive and without a floor, JOINT has 0.1177 fewer fire deaths per episode than ISO (z = −4.59)<!-- N:RES-10 -->; expressed in agents, the survival gap is about 0.11<!-- N:DX-406 --> of the 12<!-- N:ENV-6 --> agents per episode.

The High-severity readout re-evaluated every T\* checkpoint of ISO, JOINT and ISO-4 with every stressor on at β = 0.70<!-- N:CAL-3 -->, out of family. Both co-primaries are null, so the reading is an **a-fortiori exclusion**: no gap larger than 3.40 completion points or 2.54 survival points<!-- N:RES-14 --> at High even where JOINT trained on the evaluated configuration and ISO never saw a composed one. $\Gamma_H$ lies within rerun noise, at 0.73 and 0.75 times its floor-based standard error (completion, survival)<!-- N:RES-14 -->; ISO-4 has no identical reruns, so that check is UNDERPOWERED for it. The readout is not a held-out test: JOINT trained on this configuration at weight 1/2<!-- N:DES-16 -->. At High, Coupling B's survival effect replicated in direction in 3 of 3 contrasts<!-- N:CB-5 --> (§6.4) while Coupling A is marginal (§5.3), the mirror image of θ\*'s Medium siting (§10).

Mediation is **VOID**<!-- N:SEC-7 -->. The registered mediator, the counter's realized count during training, had a first-stage slope on p of −1.03 × 10⁻⁵, 95 % [−2.91 × 10⁻⁵, +0.93 × 10⁻⁵]<!-- N:DX-29 -->. A rule fixed before the sweep was read voids it when that interval contains zero. Diagnosed after the run, with the rule unchanged: the counter counts collapse-seeded ignitions inside an alive agent's crop<!-- N:CO-4 -->, which only Coupling A produces. In mixtures it measures the Coupling-A frequency that the sweep holds fixed and is blind to co-occurrence.

Seed dispersion exceeds the rerun floor in both arms, 1.12 and 1.09 times on completion and 1.25 and 1.19 times on survival (ISO, JOINT)<!-- N:HW-1 -->. Survival Γ, at 5.40 times its floor-based standard error<!-- N:HW-1 --> (completion 1.78 times<!-- N:DX-21 -->), clears the check that an effect exceeds rerun noise. Γ and Γ₄′ ran on GPU 1 and the post-unblind evaluations on GPU 3<!-- N:HW-4 --><!-- N:DX-5 --> (Appendix F); §11 reports how closely evaluation reproduces on one GPU and across GPUs.

### 9.3 A recommendation and its scope

A comparison of joint and isolated training that leaves the active share free can report an active-share effect as a composition effect. This follows from the comparison's design alone, as JOINT's threefold per-coupling frequency over ISO<!-- N:DES-7 --> does. We make one recommendation, motivated by this result alone: that studies of compositional generalization match the share of training that contains an active stressor before attributing a gain to composition. It was motivated in one environment at one scale, and whether it holds elsewhere is untested. Matching the active share here left JOINT's other differences in place, and the corrected contrast excludes only a large composition effect (§9.2).

<!-- PAPER V2 DRAFT (PAPER V2 ruling, 2026-10-11): builder-drafted, not owner-approved -->

## 10 Limitations

<!-- STUB-SPEC
PURPOSE: Every branch-invariant limitation of the design, in the registered order with Medium siting first, stated whatever the result; then what the record adds, split into what was registered or recorded before the outcome and what was found after it. Pointers, not restated numbers.
WRITER: W5. BUDGET: 700 prose words (the demo's: 1,051). Numbered list for items 1 to 10, then two short bullet lists.
OPENING: one sentence scoped to items 1 to 10 (N13, P3-L0): those are properties of the design, registered before the outcome was known; never claim that for the later lists.
ITEMS 1 TO 10 (the demo's order, sections/10_limitations.md:7-16): 1 Medium siting (registered as branch-invariant, phase6_framing_branches.md:245-261; branch_B section 5 line 5): θ* sits where Coupling B's own survival effect was −0.03 points against a three-seed spread, not a floor (CB-9); its survival effect is at High, 3 of 3, −4.7 to −10.7 points (CB-5), the registered text quoting the first estimate, 8.8 points (CB-6), only beside it; Medium was chosen because both couplings clear their lock criteria there and its floors are smallest, which trades effect existence for measurability; no severity has both couplings strongly live (at Medium B quiet and A live; at High A marginal by construction, its seeded ignitions falling 4.83-fold, CA-4, pointer to section 5.3, and B live); the High readout adds breadth, not a test where both bite; the pre-unblind line reading a Medium survival effect as one "the single coupling did not show" is struck. This item keeps its numbers: they are the registered limitation's content. 2 One held-out severity, interpolated in one scalar (CAL-3). 3 No coordination is required (ENV-6, ENV-9, ENV-11); "swarm" is not a claim. 4 The death penalty (ENV-1; branch_B line 6; the ablation's scope ENV-2, pointer to section 3.3). 5 A frozen message encoder (ENV-12; the full phrase "inert under a frozen random-projection encoder at this scale"; gradient-shaped messaging untested; the composition probed is A × B). 6 Position and time are observed (ENV-7); the wall-drift artifact (DX-32, a diagnostic); no differenced test can see it; the position-drift diagnostics are recorded, not graded. 7 Conditional intervals (DES-13). 8 GPU block structure (HW-4, DX-5, DX-30; branch_B line 8): one sentence, pointing to Appendix F, with GPU 1 to 3 as BRIEF section 5.2 names them. 9 No external baseline and no adaptive curriculum evaluated (READS RULING item 4; DX-2: one hyperparameter set for every arm). 10 A simple hazard (DX-1; Def. 3; Corollary 1's exact value holds only for the idealized kernel).
WHAT THE RECORD ADDS, REGISTERED OR RECORDED BEFORE THE OUTCOME: the design error (F3, one bullet: the confirmatory Γ carries a design error whose direction inflates it; the correction rests on a 20-seed sensitivity arm outside the family, trained on another GPU; the branch label stays B; pointer to section 9.1); bars without a floor of their own (CB-9; the calibration grids; the intermediate sweep arms and the identification arm; ISO-4 with no identical reruns; pointer to section 8.6); a recorded deviation (k = 72 against the registered cap of 60, pointer to section 9.1, no numbers: Q7); what Proposition 4, by its new name, does not say (one line, pointer to section 9.1: Q7).
WHAT THE RECORD ADDS, FOUND AFTER UNBLINDING: the correction's own limits (the registered string; pointer to section 9.2; which of active share and per-coupling frequency carries the effect is open); matched compute only, with "sign unstable over the final half" on both co-primaries and the T = 2000 subsample UNDERPOWERED (pointer to section 9.2); completion unresolved, an exclusion with its bound, leaning negative (pointer to section 9.2; its realized power is in section 9.1); the registered mediator was blind to co-occurrence in mixed training, so mediation is VOID (pointer to section 9.2); the secondary family's many 95 % intervals, none family-corrected, non-verdict-bearing; one environment, one scale, one learner, which is the scope of the recommendation in section 9.3 (F4).
REQUIRED FACTS: CB-9, CB-5, CB-6, CA-4, CAL-3 (item 1, 2); ENV-1, ENV-2, ENV-6, ENV-7, ENV-9, ENV-11, ENV-12; DX-1, DX-2, DX-5, DX-30, DX-32; DES-13; HW-4; DES-1, DES-3 only if numbers are kept in the deviation line (default: none).
FIGURES, LISTINGS, LATEX: none.
HONESTY LINES AND REGISTERED STRINGS: branch_B section 5 lines 1, 2, 3, 4, 5 (home of the registered limitation), 6, 8; "does not survive the inert-share correction"; "sign unstable over the final half"; "recorded, not graded"; "no severity has both couplings strongly live"; "no adaptive curriculum evaluated".
FIX-LIST AND FINDINGS ITEMS OWNED: N13, P3-L0, P3-N15 (the opening scoped; the split); F3 (the bullet); F4 (the scope pointer, no "the argument … is general"); C3 (the new name); F5 (card and unit to GPU; Phase-N named); LEN (pointers); P3-Ladd; Q7, Q15.
DEMO KEEPS (sections/10_limitations.md): items 1 to 10 in order with their content; the record's additions. CHANGES: the opening sentence scoped; the additions split by timing, pointers in place of numbers; the F3 bullet; the advice bullet becomes a scope pointer. DROPS: restated numbers outside item 1.
NOT HERE: a new limitation that contradicts a result; "the design could not have found a composition effect"; any outcome-dependent omission of a registered item; a limitation phrased as a finding; "The argument for matching the active share is general".
DEPENDENCIES: section 1 points to item 1; section 2 cites item 9; section 6.4 holds the Medium measurement; sections 7, 8, 9 hold the material the pointers name.
-->

Items 1 to 10 are properties of the design, stated whatever the outcome. Each was listed, in this order, before unblinding, and item 1 was registered as applying to every outcome.

1. θ\* sits at Medium, where Coupling B's own measured survival effect was −0.03 points<!-- N:CB-9 -->, graded only against a three-seed<!-- N:CB-9 --> spread. Coupling B's survival effect is at High, where the Coupling-B contrast replicated in direction three times out of three<!-- N:CB-5 -->, between −4.7 and −10.7 points<!-- N:CB-5 -->; the registered text quotes the first two-seed estimate, 8.8 points<!-- N:CB-6 -->. Medium was chosen because both couplings clear their lock criteria there and its floors are the smallest, which trades the existence of a behavioural effect for measurability. By the project's own locks, no severity has both couplings strongly live: at Medium B is quiet and A live, and at High A is marginal by construction (§5.3) and B live. The High readout adds breadth in severity and does not test composition where both couplings bite. The pre-unblind line that read a Medium survival effect as one "the single coupling did not show" is struck: Γ₄ and Γ₄′ contradict it.
2. θ\* is one held-out point, interpolated in one scalar between the training severities β = 0.43 and 0.70<!-- N:CAL-3 -->, and no training data lies near criticality.
3. The task requires no coordination: twelve agents<!-- N:ENV-6 --> share one policy's parameters and a team reward of +1<!-- N:ENV-9 --> per collected item; "swarm" is not a claim.
4. The reward sees deaths, at $d_p = 0.5$<!-- N:ENV-1 --> each, and not the hazard, so the asymmetry between survival and completion is between a penalized channel and a rewarded one. The only $d_p$ ablation is narrow and was not re-run under the protocol of §9 (§3.3).
5. Communication denial is inert under a frozen random-projection encoder at this scale: the message head receives no gradient, and gradient-shaped messaging remains untested. The composition the test probes is A × B; δ is carried in θ\* for registration fidelity.
6. The observation includes the agent's own position and the time step, so a policy can condition on where and when it is, independently of the hazard. The wall-drift artifact (§8.5) is the visible form, and no differenced test can see it; the position-drift diagnostics are recorded, not graded.
7. Every interval in §9 is conditional on one common evaluation draw, seed 0 × 512 episodes<!-- N:DES-13 -->, which cancels in Γ; the intervals carry training-seed variance only.
8. The confirmatory runs and every analysed secondary run, the same-GPU replicate's included, trained on GPU 1<!-- N:DX-5 -->; ISO-4 trained on GPU 2, so Γ₄ and B̂ are across GPUs; and the post-unblind evaluations ran on GPU 3<!-- N:HW-4 --> (Appendix F).
9. No external baseline, domain-randomization schedule or adaptive curriculum is evaluated; every arm uses one learner, single-policy IPPO, with one hyperparameter set (Appendix B).
10. The hazard is simple: a one-step burn time, a single ignition at reset, no spontaneous ignition ($\iota = 0$<!-- N:DX-1 -->), and no wind or fuel heterogeneity. Corollary 1's exact critical value is specific to this idealized kernel on the infinite lattice.

Registered or recorded before unblinding:

- The confirmatory comparison carries a design error, which inflates Γ: a third<!-- N:DES-8 --> of ISO's training episodes are fire-only (§9.1). Its correction, registered before unblinding, rests on a 20-seed<!-- N:DES-13 --> sensitivity arm outside the confirmatory family, trained on another GPU.
- Several bars have no floor on their own artifact, because the design ran no identical reruns for them (§8.6).
- The confirmatory seed count exceeds the registered seed rule's cap, a deviation recorded before unblinding (§9.1).
- Proposition 4 (A transfer bound for a fixed policy) bounds what isolated training can be guaranteed to transfer and does not lower-bound the realized gap; the experiment decides (§9.1).

Found after unblinding:

- The survival effect does not survive the inert-share correction; the branch label stays B (§9.2). The correction excludes only a large composition effect and leaves open whether the active share or the per-coupling frequency carries the ISO-4 − ISO difference, which is reported without a test. The same-GPU replicate, proposed after Γ₄ was seen, agrees.
- On both co-primaries Γ(t) is sign unstable over the final half, so Γ is a claim at matched compute only; the T = 2000<!-- N:RES-15 --> subsample, UNDERPOWERED by registration, cannot settle another budget (§9.2).
- Completion is unresolved: its null is an exclusion with its bound, and it leans negative late in training (§9.2).
- The registered mediator was blind to co-occurrence in mixed training, so mediation is VOID (§9.2).
- The secondary analyses report many intervals, none family-corrected (Appendix H).

All of it was measured in one environment, at one scale, with one learner: the scope of the recommendation in §9.3.

<!-- PAPER V2 DRAFT (PAPER V2 ruling, 2026-10-11): builder-drafted, not owner-approved -->

## 11 Reproducibility

<!-- STUB-SPEC
PURPOSE: What a reader can re-run and check without a link: what the code and records contain (stated as what exists, promising no release, N14); what is exact (ablations by construction; evaluation, the home of HW-2 and HW-3) and what is not (GPU training, which is why floors are measured); the cost of a run, and the throughput statement folded in from the demo's Appendix G; the checkpoint archives and their hashes; one look per stage (pointer to section 9.1).
WRITER: W5. Also the alternate alt/11_reproducibility.supplement.md (the demo's supplement framing, for Q4e). BUDGET: 300 prose words (the demo's: 473).
REQUIRED FACTS: HW-2 (four repeated evaluations of each of two checkpoints bit-identical on one GPU and identical to the grid's evaluations); HW-3 (across GPUs, 280 of 288 paired evaluations identical, largest absolute difference 2.44 × 10⁻⁴: write it in words or with \lvert\Delta\rvert, never with bare pipes, M1); DX-4 (518 to 521 s per 1000-update training run, 9 to 10 s per 512-episode evaluation, on one RTX 5090); DX-407 (Python 3.12.3, jax 0.11.0); DX-3 (32,768,000 environment steps per run); DX-2 (hyperparameters in Appendix B); DX-5 (GPU models); DX-408 (a re-verification matched every recorded archive hash; one floor set mostly unhashed, Appendix F). The throughput statement (demo Appendix G, sections/12_appendix.md:197): the paper states no environment-only throughput figure; any such figure would have to state which outputs its consumer reads; the only cost figures are training measurements (DX-4).
CODE FACTS: every locked constant is reachable from a configuration and asserted by a test against the configurations and code defaults (che/tests/test_locks.py; CLAUDE.md locks rule); GPU training is not run-to-run reproducible because the compiler autotunes kernels by timing and some reductions use atomics (che/bench/results/phase4/phase4_report.md:637-639, read this session).
FIGURES, LISTINGS, LATEX: none (Listing 3 may be referred to).
HONESTY LINES AND REGISTERED STRINGS: none specific; never a size or venue limit (O-3, O-4 OPEN; SUP-1, SUP-2 are not to be stated); no URL; no commit hash; sha256 values allowed but none needed.
FIX-LIST AND FINDINGS ITEMS OWNED: M1 (the home of the evaluation figure, without a pipe); N14 (class C: state what exists; the alternate describes a supplement); P3-U4 (evaluation reproducibility stated once, here); LEN (one look per stage in one sentence; the appendix list removed, since the appendix index replaces it, P2-h); Q4e, Q15.
DEMO KEEPS (sections/11_reproducibility.md): what is exact and what is not; the cost of a re-run; the checkpoints paragraph; one look per stage. CHANGES: "What the anonymized code supplement contains" becomes a description of what exists; the M1 line rewritten; the throughput note added. DROPS: the appendix list; "the anonymized code supplement" as a promise.
NOT HERE: any URL; "available on GitHub"; a size or a limit; "all code is released"; commit hashes; GPU addresses or UUIDs; dollar figures.
DEPENDENCIES: section 3.4 (bitwise nesting); section 8 (why floors are measured); section 9.1 (one look); Appendix B (W5), Appendix F (W6).
-->

The code behind this paper is one repository. It holds the environment, training, evaluation and calibration code, and every configuration, θ\* and the generated protocol configurations included. It also holds the analysis scripts that produced the results of §9, a registry of the locked constants, and a CPU test suite that runs the theory checks as unit tests. A test asserts that the configurations and code defaults agree with the registry and that each registered analysis constant equals the literal in the script that uses it. Each listing is a verbatim excerpt of the repository, labelled with file and lines.

Ablations are exact by construction: every stochastic branch consumes its random numbers whether or not its stressor is on, so switching a stressor off reproduces the nested model's trajectories bit for bit under the same keys (§3.4, Listing 3). Four repeated evaluations of each of two checkpoints are bit-identical on one GPU and identical to the grid's own evaluations<!-- N:HW-2 -->. Re-evaluated on another GPU, the final checkpoints of all confirmatory runs gave identical completion and survival values in 280 of 288<!-- N:HW-3 --> checkpoint–metric pairs, and the largest absolute difference is 2.44 × 10⁻⁴<!-- N:HW-3 -->. GPU training is not run-to-run reproducible (§8), which is why floors are measured (Appendix C).

On GPU 1, an RTX 5090<!-- N:DX-5 -->, a 1000-update training run took 518–521 s and a 512-episode evaluation 9–10 s<!-- N:DX-4 --> (Python 3.12.3, jax 0.11.0<!-- N:DX-407 -->). A run is 32,768,000<!-- N:DX-3 --> environment steps, each advancing all 12<!-- N:ENV-6 --> agents; Appendix B gives the hyperparameters. These are training measurements. The paper states no environment-only throughput figure, because under the compiler's dead-code elimination such a figure depends on which outputs its consumer reads.

The §9 checkpoints were archived off the rented machines with recorded sha256 hashes, except a partial floor set that grades nothing, in which one of 12<!-- N:DX-408 --> archives has a hash (Appendix F). A re-verification matched every recorded hash<!-- N:DX-408 -->. The analysis scripts refuse to run out of order, and each stage's log records a single run (Appendix F).

<!-- PAPER V2 DRAFT (PAPER V2 ruling, 2026-10-11): builder-drafted, not owner-approved -->

## Appendices

<!-- STUB-SPEC
PURPOSE: The appendix opening and Appendix A. First an appendix index, one line per appendix A to I (it replaces section 11's list, P2-h). Then the proofs, each stated once: the statements stay in the body ("Statement: §3.1" and so on; claims review C-34), and Appendix A says where it departs from the formal specification.
WRITER: W6. BUDGET (this file): about 800 prose words (index about 80; proofs about 720). The appendix as a whole: 2,000 prose words excluding verbatim quotations and tables (STRUCTURE.md section 6), split 800 here, 350 in W5's B and C, 850 in D to I.
INDEX (appendix headings and letters, STRUCTURE.md section 2): A Proofs; B Locks and hyperparameters; C Floors; D The frozen analysis plan; E The registered outcome branches; F Grid provenance; G Gamma over the final half of training; H The secondary design; I Trained-policy episodes. B and C are W5's file; D to I are W6's next file. Plain text cross-references (INTERFACE).
APPENDIX A CONTENT: Proposition 1's proof, once (the demo's sections/12_appendix.md:11 with the reachable-set argument), with the departure note (the formal specification says S and Ω_i are finite; with the real-valued smoke field that holds only on the reachable states, which is all the argument uses: OI-2). Proposition 2's proof (the coupling) and the implementation-exactness paragraph (home: che/env/hazard.py:8-16; grassberger1983). Proposition 3's proof without "The divergence rate is Corollary 1(3)" (C1), and the finite-protocol details (DX-409: cluster mass at β = 0.43 saturates by an age of about 64 steps; the four measured factors compose to the observed slope within Monte Carlo error at both grid sizes). Theorem 1's proof (home; the demo's 12:29). Proposition 4, by its new name: the proof idea without a constant (the return difference is bounded by telescoping the evaluation operators of the two models along the trajectory distribution; the observation term enters because the policy acts through the observation), and why every ISO configuration differs from θ* on the states where both couplings act at once (a collapse increment next to Fuel with an agent within attenuation range); no display with the constant or with the per-agent maximum, no ISO-against-JOINT contrast, no lemma cited by name (C3, N6, P3-N7; Q4i); a pointer to section 9.1's honesty note. Remark 2′: the extra step (the idling correction is largest at low κ_B and tends to 1 as κ_B grows) and the toy's constants moved from section 7 (DX-15).
REQUIRED FACTS: DX-15, DX-409, CAL-3. No other record number belongs here.
CITATIONS: grassberger1983, pynadath2002 (Remark 2′ pointer).
FIGURES, LISTINGS: none. LATEX: MathJax per BRIEF section 14; proofs end with \blacksquare; no \label; absolute values with \lvert \rvert.
FIX-LIST AND FINDINGS ITEMS OWNED: C1 (Prop. 3's proof), C3 (Prop. 4's name and content), OI-2 (the departure note), P2-9 (Prop. 1's proof once), P2-h (index, slug-safe headings), LEN (no restated statements: C-34), P3-N7, N6, Q4i, Q4k.
DEMO KEEPS (sections/12_appendix.md:5-37): the proofs of Props. 1 to 3 and Thm. 1; the Prop. 1 departure note; the Remark 2′ step. CHANGES: "Statement: §n" in place of restated statements; Prop. 3's rate line out; Prop. 4 renamed, no constant. DROPS: "irreducible"; the divergence-rate line.
NOT HERE: any statement already in the body, restated; any number outside the ledger and the supplement; a reinterpretation of a theorem's hypotheses (Q13, Q23 are the owner's).
-->

- Appendix A: proofs.
- Appendix B: locks and hyperparameters.
- Appendix C: reproducibility floors.
- Appendix D: the frozen analysis plan, quoted.
- Appendix E: the registered outcome branches.
- Appendix F: grid provenance and blinding.
- Appendix G: Γ over the final half of training.
- Appendix H: the secondary design.
- Appendix I: trained-policy episodes.

### A Proofs

Each statement is in the body, in the section named. The proofs follow the formal specification in the notation of Definition 1, and departures from it are noted.

**Proposition 1.** Statement in §3.1.

**Proof.** Each factor of $T_\theta$ is a conditional kernel, measurable in its conditioning variables, all of which are components of $(s, a)$ or of already-sampled components of $s'$. The dependence of $T_H$ on $c'$ and of $T_K$ on $x'$ is a sequential composition within one time step. Sample $c' \sim T_C(\cdot \mid c, x)$, then $h' \sim T_H(\cdot \mid h, c, c')$, then $\rho' = T_\rho(\rho, h')$ (deterministic), then $x' \sim T_X(\cdot \mid x, a, h', c')$, then $k' \sim T_K(\cdot \mid x')$. A composition of Markov kernels is a Markov kernel on the product space, so $T_\theta$ is a valid transition kernel on $\mathcal{S}$ and $(s_t)$ is Markov. The action sets are finite, every stochastic factor and the reset distribution have finite support, and $\rho$ evolves deterministically from $\rho_0 = 0$. The states and observations reachable within the horizon therefore form finite sets; restricted to them, $\mathcal{M}_\theta$ is a finite Dec-POMDP, and optimal finite-horizon joint policies exist by the standard argument. $\blacksquare$

The formal specification states that $\mathcal{S}$ and $\Omega_i$ are finite. With the real-valued smoke field $\rho \in \mathbb{R}_{\ge 0}^G$ in the state, that holds only for the states and observations reachable within the horizon, which is all the argument uses.

**Proposition 2.** Statement in §3.2.

**Proof (coupling).** Attach to each unordered edge $e = \{g, g'\}$ an independent $B_e \sim \mathrm{Bernoulli}(\beta)$, and declare that a transmission attempt across $e$ succeeds if and only if $B_e = 1$. Each edge is attempted at most once: when one cell of $e$ first Burns while the other is Fuel, one attempt occurs; afterwards the burning endpoint is Burnt, which is absorbing. If the other endpoint later Burns via a different path, its neighbour across $e$ is already Burnt, so no second attempt occurs. Run with the variables $\{B_e\}$, the fire therefore burns exactly the connected component of the origin in the subgraph of open edges $\{e : B_e = 1\}$, which is the bond-percolation cluster. $\blacksquare$

This is the coupling behind the correspondence that §3.2 cites<d-cite key="grassberger1983"></d-cite>, and the implementation realizes it exactly (`che/env/hazard.py:8-16`). It draws one uniform per cell and incoming direction, which maps one-to-one to the ordered pairs of Definition 3. With a burn time of one step, each unordered edge sees at most one attempt, so these uniforms are the coupling's per-edge variables.

**Proposition 3.** Statement in §5.2.

**Proof.** Each collapse seed grows, by Proposition 2, a burnt cluster equal in distribution to a bond-percolation cluster, of expected size $\chi(\beta)$. By linearity of expectation over the Binomial or Poisson number of seeds, the total expected burnt area is $\lambda_A T \chi(\beta)$ when clusters are disjoint; overlaps only remove double counting, which gives the upper bound in general. $\blacksquare$

The formal specification adds a divergence rate near the critical point, which rests on critical exponents the paper does not state (§4.1). The equality is approached only when four conditions are matched, each with a known sign: an unconditional cluster-mass reference (a spanning-conditioned one underestimates it), seed location (boundary clipping lowers the mass of uniformly placed seeds), seed age (cluster mass at β = 0.43<!-- N:CAL-3 --> saturates by an age of about 64 steps<!-- N:DX-409 -->), and sparsity (sibling seeds and cluster overlap deflate the measured slope). In the Proposition 3 measurements (§5.2) the four factors compose to the observed slope within Monte Carlo error.

**Theorem 1.** Statement in §6.2; items (1)–(3) below refer to it.

**Proof.** *(1)* With zero slack, the only decision is the corridor choice at $b$; waiting or probing is impossible within $T$. If informed (probability $q$), taking the corridor other than $Z$ succeeds with probability 1; if not, both corridors are exchangeable given the history, and any choice succeeds with probability $\tfrac12$. Hence $J^* = q + (1-q)\tfrac12 = \tfrac12 + \tfrac{q}{2}$, and no policy exceeds this, since success requires information or a lucky guess. *(2)* In the fixed-map environment the signal is uninformative, so the signal-blind policy is among the optimal ones there; on $E_{2C}$ it succeeds if and only if $Z = z_0$, with probability $\tfrac12$. *(3)* Each factor $(1 - e^{-\kappa_B j})$ is continuous and strictly increasing in $\kappa_B$ on $(0, \infty)$, so the finite product is too, and $q$ is continuous and strictly decreasing. The product tends to 0 as $\kappa_B \to 0$ and to 1 as $\kappa_B \to \infty$. $\blacksquare$

**Proposition 4 (A transfer bound for a fixed policy).** Statement in §9.1.

**Proof idea.** The difference between the two returns is bounded by telescoping the evaluation operators of the two models along the trajectory distribution; the observation term enters because the policy acts through the observation. Every configuration in $\Theta_{\mathrm{iso}}$ differs from $\theta^*$ where both couplings act at once. Take a state with a collapse increment next to Fuel and an agent within attenuation range. There $T_{\theta^*}$ places mass of order $\kappa_A$ on ignition transitions that a configuration with $\kappa_A = 0$ places elsewhere, and the observation kernels differ when $\kappa_B$ differs.

The formal specification displays the bound with an explicit constant and concludes more about ISO's slack than an upper bound can show; the paper states the bound in words and draws no such conclusion (§9.1).

**Remark 2′.** Stated in §7.2, after Pynadath and Tambe<d-cite key="pynadath2002"></d-cite>. One step is not spelled out in §7. Let $\tilde q$ be the probability of being informed under the best idling schedule. The commitment draws have different optical depths, so as $\kappa_B \to \infty$ the lowest-depth draw dominates both products and $\tilde q / q \to 1$. The correction peaks at moderate $\kappa_B$, and its relative bite on the value of communication is largest at low $\kappa_B$, where $q$ is near 1. In the two-agent toy, which is not CHE (4096 episodes and 8192 Monte Carlo draws per point<!-- N:DX-15 -->), $\tilde q / q$ is 1.126 at $\kappa_B = 1.0$ and peaks at 1.235 near $\kappa_B = 2$<!-- N:DX-15 -->. The correction removes 79 %, 54 % and 7 % of $\mathrm{VoC}_{\mathrm{gated}}$ at $\kappa_B$ = 0.5, 1.0 and 3.0<!-- N:DX-15 -->. The check that the denied arm under the no-idle schedule matches $\tfrac12 + \tfrac12 q$ passes (largest absolute z 0.44; χ² 0.51 on 8 degrees of freedom<!-- N:DX-15 -->), and the arm with free communication scores 1.0000 at every $\kappa_B$<!-- N:DX-15 -->.

<!-- PAPER V2 DRAFT (PAPER V2 ruling, 2026-10-11): builder-drafted, not owner-approved -->

### B Locks and hyperparameters

<!-- STUB-SPEC
PURPOSE: Appendix B: every locked constant with its value, ruling date and record, then the training hyperparameters and the budget. Appendix C: every reproducibility floor the paper uses, with its GPU, run length, artifact and number of identical reruns, and the key to the study codes (the one place the codes appear, F5). These files continue the appendix after W6's Appendix A; they open with an H3 by design (STRUCTURE.md section 13).
WRITER: W5 (moved from W6 for load and because Appendix C holds the exhibits of section 8: STRUCTURE.md section 10). BUDGET: about 350 prose words across both, plus the tables.
APPENDIX B REQUIRED FACTS: the environment locks (CAL-1 with its O-2 caveat: the lock record's value, the committed estimators beside it; CAL-3; CA-1; CB-1; COM-6; ENV-1; DX-401 for every ruling date and for the weak-floor smoothing passes and the observation version; DX-1 for σ_s, η, ι, not locked, held by convention); the analysis constants (DES-1, DES-3, DES-13, DES-4 for the 0.03 band, DX-402 for every date, METH-6 for the retired convergence check's constants, which grade nothing); the hyperparameters (DX-2: learning rate 3e-4 constant; γ 0.99; GAE λ 0.95; clip 0.2; entropy 0.01; value 0.5; gradient-norm clip 0.5; Adam ε 1e-5; 256 environments; 128 steps; 4 minibatches; 4 epochs; checkpoint every 50 updates) and the budget (DX-3). The demo's tables (sections/12_appendix.md:39-81) are the template; keep code identifiers such as K_CONFIRMATORY only as table labels, with a plain description beside each.
APPENDIX C REQUIRED FACTS: each floor row of the demo's table (sections/12_appendix.md:83-102) with its IDs: METH-1, DX-403, DX-412, COM-5, CB-7, DX-40, METH-2, DX-5, DX-34, METH-5, DES-1, DES-5, DES-2, DES-10, DX-35, DES-3, HW-2, HW-4, DX-36; the ±40 % uncertainty of a four-run floor (DX-403 or DX-303); the overlap of the RTX 5090 and RTX PRO 6000 intervals and that no claim is made that either GPU is less reproducible (DX-35). Add a key mapping each study code to its plain name as sections 5 to 9 use it (for example, the four-run Medium floor study on an RTX 5090, the Coupling-B calibration grid); add, in one or two sentences each, the exhibit details section 8 moved here (the refactor exhibit's two code versions; the run-length exhibit's two machines).
FIGURES, LISTINGS, LATEX: none; tables only (no pipes inside math in a cell).
HONESTY LINES AND REGISTERED STRINGS: "reference scale (cross-artifact)" for the High floor's use beside the Coupling-B grid; floors are per metric, per GPU and per artifact; the partial re-measurement of 2026-08-14 is provenance only and grades nothing.
FIX-LIST AND FINDINGS ITEMS OWNED: F5 (the key; "card" to GPU; "unit" to GPU n; "rep" to identical rerun; launch batch to "the first floor study"; G1.2 named in plain words); LEN (the demo's App. C ratios paragraph already moved; keep it to the table and the key); OI-5 (never "different hardware" for M5.3's floor); Q20.
DEMO KEEPS (sections/12_appendix.md:39-102): both lock tables, the hyperparameter table, the floors table and the overlap sentence. CHANGES: jargon to plain names with the key; GPU naming. DROPS: nothing.
NOT HERE: GPU addresses or UUIDs; commit hashes; any number not in the ledger or the supplement.
-->

Each locked constant below was fixed by a ruling on the date given, and the test described in §11 checks each against the configurations, the code defaults or the analysis scripts.

| constant | value | ruled | record |
|---|---|---|---|
| critical point $\hat\beta_c$ | 0.500 ± 0.005<!-- N:CAL-1 --> | 2026-07-19<!-- N:DX-401 --> | severity lock record; no committed script reproduces its estimator, and the committed estimators give a crossing mean of 0.504 and a consensus of 0.499<!-- N:CAL-1 --> |
| β Low / Medium / High | 0.43 / 0.49 / 0.70<!-- N:CAL-3 --> | 2026-07-19<!-- N:DX-401 --> | severity lock record |
| β held out (θ\*) | 0.49<!-- N:CAL-3 --> | 2026-08-02<!-- N:DX-401 --> | the ruling that sited θ\*: train at the two extremes and hold out the middle |
| $f_{\mathrm{weak}}$, $\lambda_0$, $\lambda_{\mathrm{load}}$, $\kappa_A$, $r_A$ | 0.15, 5e-5, 4e-4, 0.06, 1<!-- N:CA-1 --> | 2026-07-21<!-- N:DX-401 --> | Coupling-A lock record |
| weak-floor smoothing passes | 2<!-- N:DX-401 --> | 2026-07-21<!-- N:DX-401 --> | Coupling-A lock record, locked as the code default |
| $\kappa_B$ | 1.0<!-- N:CB-1 --> | 2026-07-27<!-- N:DX-401 --> | Coupling-B lock record, on the detection band alone |
| δ off / on; $R_{\mathrm{comm}}$ | 0.0 / 1.0<!-- N:DX-401 -->; 16<!-- N:COM-6 --> | 2026-07-30<!-- N:DX-401 --> | communication lock record |
| death penalty $d_p$ | 0.5<!-- N:ENV-1 --> | 2026-07-19<!-- N:DX-401 --> | the death-penalty design decision |
| observation encoding | 3<!-- N:DX-401 -->, the masking observation (§3) | 2026-07-24<!-- N:DX-401 --> | the observation design decision |
| $\sigma_s$, η, ι | 1.0, 0.5, 0.0<!-- N:DX-1 --> | not locked | held fixed by convention, never calibrated |

| analysis constant | value | ruled | role |
|---|---|---|---|
| `K_CONFIRMATORY` | 40<!-- N:DES-1 --> | 2026-08-03<!-- N:DX-402 --> | design seeds per confirmatory arm, the seed rule's base |
| `K_LADDER_CAP` | 60<!-- N:DES-1 --> | 2026-08-03<!-- N:DX-402 --> | the seed rule's cap |
| `K_CONFIRMATORY_REALIZED` | 72<!-- N:DES-3 --> | 2026-09-22<!-- N:DX-402 --> | the seed count at which Γ is read, a recorded deviation (§9.1) |
| `K_SECONDARY` | 20<!-- N:DES-13 --> | 2026-08-02<!-- N:DX-402 --> | seeds per secondary arm; ISO-4 uses the same count |
| `SIDAK_M`; $z_\alpha$ | 2; 2.2365<!-- N:DES-13 --> | 2026-08-02<!-- N:DX-402 --> | the two co-primary tests, Šidák-corrected |
| `POWER_STOP` | 0.80<!-- N:DX-402 --> | 2026-08-02<!-- N:DX-402 --> | the minimum design-stage power at the 0.03<!-- N:DES-4 --> band |
| `T_STAR` | 1000<!-- N:DES-13 --> | 2026-08-11<!-- N:DX-402 --> | the training budget in updates, unchanged since 2026-08-03<!-- N:DX-402 --> |
| `GAMMA_T_RETENTION` | 11<!-- N:DES-13 --> | 2026-08-11<!-- N:DX-402 --> | checkpoints kept for Γ(t): updates 500–1000 every 50<!-- N:DES-13 --> |
| evaluation draw | seed 0 × 512 episodes<!-- N:DES-13 --> | registered with the grid layout | common to every run; not in the lock registry |
| `PLATEAU_PASS`; `PLATEAU_REVIEW` | 1.0; 1.5<!-- N:DX-402 --> | 2026-08-02<!-- N:DX-402 --> | the convergence check's thresholds, retired 2026-08-11<!-- N:METH-6 -->; grade nothing |

The training hyperparameters are identical for every run of §9; the grid passes none on the command line, so the configured defaults apply.

| hyperparameter | value |
|---|---|
| learning rate | 3e-4, constant, no schedule<!-- N:DX-2 --> |
| discount γ; GAE λ | 0.99; 0.95<!-- N:DX-2 --> |
| PPO clip ε | 0.2<!-- N:DX-2 --> |
| entropy coefficient; value coefficient | 0.01; 0.5<!-- N:DX-2 --> |
| global gradient-norm clip; Adam ε | 0.5; 1e-5<!-- N:DX-2 --> |
| parallel environments; steps per update | 256; 128<!-- N:DX-2 --> |
| minibatches; epochs | 4; 4<!-- N:DX-2 --> |
| checkpoint interval | 50 updates<!-- N:DX-2 --> |
| budget | 32,768 environment steps per update, 32,768,000 per run<!-- N:DX-3 --> |

### C Floors

A floor is the standard deviation of a metric over identical reruns at one seed, so it measures nondeterminism alone. Floors are per metric, per GPU, per artifact and per run length; the table lists each one this paper uses, under its study code (key below), with paired floors given as ISO, then JOINT. With four reruns a standard deviation has three degrees of freedom and is uncertain by about ±40 %<!-- N:DX-403 -->, and the confirmatory training floors use eight<!-- N:DX-403 -->.

| study | GPU, updates | arms or artifact | reruns | floor | use |
|---|---|---|---|---|---|
| M5.1e | RTX 5090, 500<!-- N:DX-403 --> | Medium | 4<!-- N:DX-403 --> | completion 0.0145, survival 0.0129<!-- N:METH-1 --> | the communication studies' Medium bars |
| M5.5 | RTX PRO 6000, 500<!-- N:DX-412 --> | Medium, $R_{\mathrm{comm}}$ 16<!-- N:METH-1 --> | 4<!-- N:DX-412 --> | completion 0.0399, survival 0.0130<!-- N:METH-1 --> | with M5.1e, the per-GPU exhibit (§8.1) |
| M5.5, danger moments | RTX PRO 6000, 500<!-- N:DX-412 --> | Medium | 4<!-- N:DX-412 --> | 27.2 % (sd 0.00182)<!-- N:COM-5 --> | voids a 20 %<!-- N:COM-5 --> threshold (§8.1) |
| M5.3b | RTX PRO 6000<!-- N:DX-403 -->, 500<!-- N:DX-40 --> | High | 4<!-- N:DX-40 --> | survival 0.0621<!-- N:CB-7 --> | reference scale (cross-artifact) |
| M6.0 | RTX PRO 6000<!-- N:DX-5 --> | two code versions | 4 comparisons<!-- N:METH-2 --> | 0 of 760 hashes differ in each of 4 comparisons (reference); 1 of 4 comparisons differs (refactored)<!-- N:METH-2 --> | the per-artifact exhibit (§8.1) |
| M6.2 | RTX PRO 6000, 500<!-- N:DX-34 --> | ISO, JOINT | 8<!-- N:DX-403 --> | completion 0.0165, 0.0093<!-- N:DX-34 --> | the convergence check |
| M6.2b | RTX PRO 6000, 1000<!-- N:DX-34 --> | ISO, JOINT | 8<!-- N:DX-403 --> | completion 0.0339, 0.0483<!-- N:DX-34 --> | set the design k = 40<!-- N:DES-1 --> |
| G1.2 | RTX PRO 6000<!-- N:DES-5 -->, 1000<!-- N:DX-403 --> | ISO, JOINT, sweep at p = 0.5<!-- N:DX-28 --> | 8<!-- N:DX-403 --> | sd(Γ) at k = 40: completion 0.00504, survival 0.00310<!-- N:DES-5 --> | design-stage power |
| re-measured, 2026-09-08<!-- N:DES-2 --> | RTX PRO 6000<!-- N:DES-2 -->, 1000<!-- N:DX-412 --> | ISO, JOINT, sweep at p = 0.5<!-- N:DX-28 --> | 8<!-- N:DX-403 --> | the seed rule gave k = 46<!-- N:DES-2 --> | the registered seed rule (§9.1) |
| re-measured on GPU 1 | RTX 5090<!-- N:DX-35 -->, 1000<!-- N:DX-412 --> | ISO, JOINT, sweep at p = 0.5<!-- N:DX-28 --> | 8<!-- N:DX-35 --> | completion 0.0587, 0.0577; survival 0.0100, 0.0112<!-- N:DX-35 --> | the seed rule (k = 72<!-- N:DES-3 -->); the check against rerun noise |
| High readout | the 2026-09-08 runs, evaluated on GPU 3<!-- N:V5-2 --> | ISO, JOINT at High | 8<!-- N:V5-2 --> | completion 0.0681, 0.0613; survival 0.0180, 0.0395<!-- N:V5-2 --> | the check against rerun noise at High (§9.2) |
| evaluation | GPU 3<!-- N:HW-4 --> | two checkpoints<!-- N:HW-2 --> | 4<!-- N:HW-2 --> | bit-identical<!-- N:HW-2 --> | evaluation reproducibility (§11) |
| partial, 2026-08-14<!-- N:DX-36 --> | not recorded<!-- N:DX-36 -->, 1000<!-- N:V5-3 --> | ISO, JOINT | 8 + 4<!-- N:DX-36 --> | none reported | provenance only |

The floors of GPU 1 cannot be distinguished from those of the 2026-09-08 re-measurement on an RTX PRO 6000: the 95 %<!-- N:DX-35 --> intervals for the standard deviation overlap (ISO completion: [0.0186, 0.0571] on the RTX PRO 6000, [0.0388, 0.1194] on GPU 1<!-- N:DX-35 -->). No claim is made that either GPU is less reproducible.

The rule of §8.1 followed four<!-- N:V5-1 --> bars whose constants the ruling calls invented. The Coupling-B calibration grid graded its High survival effect against a two-seed spread of 0.0295<!-- N:DX-38 -->, below the High floor in the table, and its "strong" grade was retracted (§6.4). The content ablation at Medium applied a floor hard-coded from the four-run<!-- N:DX-403 --> Medium floor study on an RTX 5090, not one measured on its own runs. Re-sited at High, the ablation measured its floor first, but a bar set on that floor was out of reach: matching Medium's resolution would take roughly 46<!-- N:DX-302 --> seeds per arm. The denial study set its third condition's threshold below the rerun nondeterminism of its quantity. Those floor data predate the comparison, and the ruling records that a difference above the floor would have left the verdict NOT INERT standing. In the per-artifact exhibit, both versions of the code ran on one GPU, and the two<!-- N:METH-2 --> channels that differed were masking diagnostics at High severity.

| code | plain name |
|---|---|
| M3.5 (printed m35) | the Coupling-A calibration grid |
| M4.4 (printed m44) | the Coupling-B calibration grid |
| M5.1e | the four-run<!-- N:DX-403 --> Medium floor study on an RTX 5090 |
| M5.3, M5.3b | the content ablation at Medium, and the same ablation at High |
| M5.5 | the denial study |
| M6.0 | the refactor of the environment code |
| M6.2, M6.2b | the confirmatory arms' floor studies at 500 and 1000<!-- N:DX-34 --> updates |
| G1.2 | the grid's launch floor study (2026-08-10<!-- N:DES-5 -->) |

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

The registered constants are in Appendix B. The reading rules follow, quoted from the registration record with their dates: emphasis is the record's own, one indented code line is set inline, and omissions are marked […]. A "§" inside a quotation refers to the record's own sections, and S1–S6 are its labels for the secondary analyses.

**1. The estimand** (T\* ruling, item 2, 2026-08-11<!-- N:METH-6 -->):

> **Primary Γ = the confirmatory contrast at MATCHED BUDGET T = 1000<!-- N:DES-13 -->, all arms — registered as a fixed-budget claim.**
>
> **"At convergence" is explicitly NOT claimed anywhere.** The paper says **"at matched compute"** throughout, which is also the practitioner-relevant question. […]

**2. Budget robustness** (item 3 of the same ruling; restated for every branch on 2026-08-13<!-- N:DES-12 -->):

> The fixed-budget conclusion is reported as **budget-robust iff the sign of Γ is stable over the final half of training**. If the sign is still moving at T, **that instability IS the finding** and is reported as such.

> Mechanism: 11 retained checkpoints, updates 500–1000 at interval 50<!-- N:DES-13 -->, confirmatory arms only, **evaluated post-unblind**. Every branch above gains "— budget-robust" or "— sign unstable over the final half" as a suffix, and the suffix is not optional.

**3. The branch-B falsifier** (2026-08-13<!-- N:DES-12 -->):

> Branch B is claimable **only if** the completion contrast excludes an effect as large, in standardized units, as the observed survival effect:
>
> `|z_c| + z_α  <  |z_s|,     z = Γ / sd(Γ) per metric`
>
> with `sd(Γ)` the grid's own measured per-arm seed dispersion in the combined form and `z_α = 2.2365`<!-- N:DES-13 --> the two-sided Šidák critical value at m = 2. **If it fails, the result is branch C with an asymmetry the design could not resolve — not branch B.**

**4. Test variance and floor** (the frozen analysis plan, amended 2026-08-13<!-- N:V6-5 -->):

> **The confirmatory tests and CIs are computed on the GRID'S OWN measured per-arm seed dispersion, not on the floors.** The floors are 8<!-- N:DX-403 --> identical reps at one seed; the grid averages over k distinct seeds, and those are different variances. The floors keep exactly two narrower roles: the **beat-reproducibility hurdle**, and a **design-stage power basis registered as an UPPER BOUND** (§5, superseded note, item 2). […]

Design-stage power is therefore a ceiling. On the grid's launch floor study (an RTX PRO 6000, 2026-08-10<!-- N:DES-5 -->), the design-stage MDE₈₀ at k = 40 was 1.55 completion and 0.95 survival points<!-- N:DES-5 -->. On the floors of GPU 1, design-stage completion power at a 0.03 effect was 72.2 % at k = 60 and 80.4 % at k = 72<!-- N:DES-4 -->; §9.1 gives the realized power.

**5. The inert-share rule** (2026-09-18<!-- N:DES-15 -->):

> - Γ and Γ₄ are reported **side by side on every branch**, with B̂ and its CI.
> - If Γ rejects on a co-primary and **Γ₄'s CI on that co-primary includes 0 or its sign is opposite**, the paper states that the effect **does not survive the inert-share correction**, in the abstract-level summary and not only in an appendix. **The branch label does not change** — it is fixed by Γ — but branch A/B text may not describe the effect as a composition effect without that qualifier.
> - If Γ is null and Γ₄ is null, Γ₄ is quoted as a second exclusion bound.
> - If Γ is null and Γ₄ rejects **negative**, it is reported under branch D's framing (matched-budget asymmetry) as a secondary observation, never as a confirmatory finding.
> - **No magnitude threshold on B̂ is introduced**, now or later.

**6. The High readout**, its reading for a null (same ruling):

> - **Γ_H null → an *a fortiori* exclusion**, and the only outcome this readout can establish: *"no gap larger than X at High even where JOINT trained on the evaluated configuration and ISO never saw a composed one."* Quoted as an exclusion with X from the grid's own seed dispersion, never as an absence. […]

The same entry states that the readout "is NOT a held-out test", that a positive $\Gamma_H$ is "NOT separable from in-distribution advantage", and that a negative one is "exploratory".

**7. The T = 2000 subsample** (same ruling):

> **What it may be cited for:** whether the differential drift measured at T = 1000 (review §6 item 1: 0.01209 per 100 updates<!-- N:DES-10 -->) visibly persists, closes or reverses. **What it may not be cited for:** any claim that Γ "holds" or "vanishes" at T = 2000.

**8. The mediation void rule** (the frozen analysis plan, 2026-08-02<!-- N:DX-414 -->):

> **If realized dose does not vary with assigned p, the dose figure has no x-axis and is declared VOID** — registered now, not decided after seeing the first stage.

**9. The pre-unblind rulings** (2026-09-26<!-- N:DX-405 -->):

| # | question | RULED |
|---|---|---|
| (i) | what "−" means in the branch table | **Rejection with negative sign** (\|z\| > z_α, Γ < 0). A negative estimate that does not reject is a null. Ratified as built. |
| (ii) | the cell (completion +, survival null), absent from the registered table | **REGISTERED NOW as branch A_c — the founding claim on the founding primary.** […] |
| (iii) | test statistic | **Normal z, z_α = 2.2365<!-- N:DES-13 -->**, as the frozen plan wrote; the t critical value is printed, not applied. Ratified as built. |
| (iv) | Γ(t) "sign stable" | **All 11 point estimates, t = 500 … 1000, share one nonzero sign**, per co-primary; t = 1000 is the grid's own eval. Consequence accepted in advance: on a null Γ, chance flips read UNSTABLE. Ratified as built. |
| (v) | Γ₄ sample and threshold | **JOINT k = 72 vs ISO-4 k = 20<!-- N:DES-3 --><!-- N:DES-13 -->**, SE `sqrt(s_J²/72 + s_4²/20)`, "rejects" and "CI includes 0" at z_α = 2.2365. (Γ null, Γ₄ rejects positive) stays UNREGISTERED. Ratified as built. |
| (vi) | Γ_H reading | **As (i), at z_α = 2.2365.** Ratified as built. |
| (vii) | primary k | **k = 72 stays primary**; the registered-ladder k = 60<!-- N:DES-1 --> prefix is reported beside it, UNDERPOWERED-flagged. |
| (viii) | re-evaluate the 144 T\* = 1000 checkpoints on the post-unblind card | **YES.** […] |

In (viii), "the post-unblind card" is GPU 3.

**10. The secondary specification** (2026-09-26, after unblinding and before the sweep was read<!-- N:DX-413 -->):

> (S1) PAVA + OLS slope CI; (S2) single-hinge breakpoint, UNDERPOWERED iff the CI spans {0.125 … 0.375}<!-- N:DX-28 -->; (S3) plane fit, bound = 95 % CI of 0.5·γ_n; (S4) training co-activity over updates 1…1000, VOID iff the first-stage CI contains 0; (S5) the same-card replicate is ADDED, beside Γ₄, unable to change its qualifier; (S6) 95 % intervals, Γ₄′ at z_α. […]

The omitted words name the code version, which identifies the repository.

### E The registered outcome branches

"Positive" and "null" mean rejection or non-rejection at θ\* in the confirmatory family, and "−" means rejection with negative sign (Appendix D, item 9). Branches A–D were registered on 2026-08-13<!-- N:DES-12 -->, each with a framing; the registered table's venue-lean column is omitted. $A_c$ was added on 2026-09-26<!-- N:DX-405 -->, before unblinding, for a cell the table lacked.

| branch | completion | survival | headline claim, as registered ($A_c$: its registered claims, summarized) |
|---|---|---|---|
| A | + | + | founding registration, verbatim (Γ(θ\*) > 0) |
| B | null | + | composition is paid in **agents**, not task return |
| C | null | null | the instrument, and what it excludes |
| D | − on either co-primary | − on either co-primary | not separable from the matched-budget asymmetry |
| $A_c$ | + | null | the founding claim on the founding primary; the survival null quoted as an exclusion; no asymmetry claim |

The result is branch B, with the inert-share qualifier attached (§9.2).

### F Grid provenance and blinding

The grid was 252 runs<!-- N:DX-30 --> from 2026-09-09 to 2026-09-22<!-- N:DES-12 -->. Seeds 1–12 of all ten arms (ISO, JOINT and eight secondary arms) ran on an RTX PRO 6000, then seeds 13–20 of all ten arms and 21–46 of ISO and JOINT on GPU 1<!-- N:DX-30 -->. The confirmatory artifact holds all 72 seeds of ISO and JOINT on GPU 1<!-- N:HW-4 -->: 76 runs executed there and seeds 13–46 copied from the grid<!-- N:DX-30 -->. The superseded RTX PRO 6000 seeds enter only a descriptive diagnostic of the GPU effect. Seeds 1–12 of the secondary arms were re-run on GPU 1 (96 runs<!-- N:DX-30 -->), so every analysed secondary run is on GPU 1 and Γ₄′ is a same-GPU contrast. ISO-4 and the T = 2000 subsample trained on GPU 2, so Γ₄ and B̂ are across GPUs, and the post-unblind evaluations ran on GPU 3<!-- N:HW-4 -->.

All arms share seed integers, and seed 0, the floor seed, never enters the grid<!-- N:DX-416 -->. Runs are ordered seed-major and chunks end on seed boundaries, so an interruption leaves a smaller balanced design and both arms of a seed share one GPU. Every checkpoint archive's recorded sha256 matched on re-verification on 2026-09-27, 615 of 615<!-- N:DX-408 -->. A partial re-measurement of floors on another rented GPU on 2026-08-14<!-- N:DX-36 --> is provenance only.

The grid runner computes no cross-arm quantity, which a unit test asserts along with the seed properties above, and the floor reports print dispersions only. The unblinding script refuses an unflagged artifact or a modified code version, later analysis scripts refuse to run before its log exists, and each log records one run of its stage<!-- N:DX-411 -->.

### G Gamma over the final half of training

**Sign unstable over the final half**, on both co-primaries<!-- N:RES-11 -->: neither meets the registered rule that all 11<!-- N:DES-13 --> point estimates share one sign (Appendix D, items 2 and 9). Values are rates, and the Šidák-corrected intervals are registered at update 1000<!-- N:DES-13 --> and descriptive before it. Checkpoints before update 1000 were evaluated on GPU 3; update 1000 is the grid's own evaluation, and re-evaluating it on GPU 3 leaves every sign unchanged (cross-GPU agreement: §11).

Completion, k = 72 per arm<!-- N:DES-13 -->:

| update | Γ(t) | sd(Γ) | Šidák CI | sign |
|---|---|---|---|---|
| 500 | +0.0017<!-- N:DX-24 --> | 0.00321<!-- N:DX-24 --> | [−0.0055, +0.0089]<!-- N:DX-24 --> | + |
| 550 | −0.0017<!-- N:DX-24 --> | 0.00353<!-- N:DX-24 --> | [−0.0096, +0.0062]<!-- N:DX-24 --> | − |
| 600 | +0.0018<!-- N:DX-24 --> | 0.00362<!-- N:DX-24 --> | [−0.0063, +0.0099]<!-- N:DX-24 --> | + |
| 650 | +0.0015<!-- N:DX-24 --> | 0.00481<!-- N:DX-24 --> | [−0.0093, +0.0122]<!-- N:DX-24 --> | + |
| 700 | −0.0037<!-- N:DX-24 --> | 0.00470<!-- N:DX-24 --> | [−0.0142, +0.0068]<!-- N:DX-24 --> | − |
| 750 | −0.0147<!-- N:RES-13 --> | 0.00610<!-- N:DX-24 --> | [−0.0283, −0.0010]<!-- N:RES-13 --> | − |
| 800 | −0.0035<!-- N:DX-24 --> | 0.00677<!-- N:DX-24 --> | [−0.0187, +0.0116]<!-- N:DX-24 --> | − |
| 850 | −0.0053<!-- N:DX-24 --> | 0.00729<!-- N:DX-24 --> | [−0.0216, +0.0110]<!-- N:DX-24 --> | − |
| 900 | −0.0039<!-- N:DX-24 --> | 0.00843<!-- N:DX-24 --> | [−0.0228, +0.0149]<!-- N:DX-24 --> | − |
| 950 | −0.0016<!-- N:DX-24 --> | 0.01021<!-- N:DX-24 --> | [−0.0245, +0.0212]<!-- N:DX-24 --> | − |
| 1000 | −0.0173<!-- N:RES-1 --> | 0.01068<!-- N:DX-24 --> | [−0.0412, +0.0066]<!-- N:RES-1 --> | − |

Survival rate, k = 72 per arm<!-- N:DES-13 -->:

| update | Γ(t) | sd(Γ) | Šidák CI | sign |
|---|---|---|---|---|
| 500 | +0.0022<!-- N:DX-25 --> | 0.00228<!-- N:DX-25 --> | [−0.0029, +0.0073]<!-- N:DX-25 --> | + |
| 550 | −0.0037<!-- N:DX-25 --> | 0.00220<!-- N:DX-25 --> | [−0.0086, +0.0013]<!-- N:DX-25 --> | − |
| 600 | −0.0027<!-- N:DX-25 --> | 0.00232<!-- N:DX-25 --> | [−0.0078, +0.0025]<!-- N:DX-25 --> | − |
| 650 | +0.0011<!-- N:DX-25 --> | 0.00242<!-- N:DX-25 --> | [−0.0043, +0.0065]<!-- N:DX-25 --> | + |
| 700 | +0.0031<!-- N:DX-25 --> | 0.00235<!-- N:DX-25 --> | [−0.0021, +0.0084]<!-- N:DX-25 --> | + |
| 750 | +0.0036<!-- N:DX-25 --> | 0.00255<!-- N:DX-25 --> | [−0.0021, +0.0093]<!-- N:DX-25 --> | + |
| 800 | +0.0020<!-- N:DX-25 --> | 0.00232<!-- N:DX-25 --> | [−0.0032, +0.0072]<!-- N:DX-25 --> | + |
| 850 | +0.0018<!-- N:DX-25 --> | 0.00234<!-- N:DX-25 --> | [−0.0034, +0.0071]<!-- N:DX-25 --> | + |
| 900 | +0.0056<!-- N:RES-12 --> | 0.00231<!-- N:DX-25 --> | [+0.0004, +0.0108]<!-- N:DX-25 --> | + |
| 950 | +0.0083<!-- N:RES-12 --> | 0.00219<!-- N:DX-25 --> | [+0.0034, +0.0132]<!-- N:DX-25 --> | + |
| 1000 | +0.0096<!-- N:RES-2 --> | 0.00216<!-- N:DX-25 --> | [+0.0047, +0.0144]<!-- N:RES-2 --> | + |

### H The secondary design

Everything here is secondary, with 95 % intervals bootstrapped over seeds within arm (B = 2000<!-- N:DX-28 -->), conditional on the common evaluation draw and not family-corrected. Each arm has k = 20 seeds<!-- N:DES-13 --> on GPU 1 with δ off. With μ, p and ν as in §9.1, the triangle gives $\nu = 1 - 2\mu + p$, and the arm names are the labels of Figure 13's table view.

| arm | μ | p | ν | survival | completion |
|---|---|---|---|---|---|
| `sweep_c50_p000` | 0.5<!-- N:DES-9 --> | 0<!-- N:DX-28 --> | 0<!-- N:DES-9 --> | 0.9241<!-- N:DX-28 --> | 0.7847<!-- N:DX-28 --> |
| `sweep_c50_p125` | 0.5<!-- N:DES-9 --> | 0.125<!-- N:DX-28 --> | 0.125<!-- N:DES-9 --> | 0.9249<!-- N:DX-28 --> | 0.7775<!-- N:DX-28 --> |
| `sweep_c50_p250` | 0.5<!-- N:DES-9 --> | 0.25<!-- N:DX-28 --> | 0.25<!-- N:DES-9 --> | 0.9261<!-- N:DX-28 --> | 0.7797<!-- N:DX-28 --> |
| `sweep_c50_p375` | 0.5<!-- N:DES-9 --> | 0.375<!-- N:DX-28 --> | 0.375<!-- N:DES-9 --> | 0.9264<!-- N:DX-28 --> | 0.7656<!-- N:DX-28 --> |
| `sweep_c50_p500` | 0.5<!-- N:DES-9 --> | 0.5<!-- N:DX-28 --> | 0.5<!-- N:DES-9 --> | 0.9289<!-- N:DX-28 --> | 0.7749<!-- N:DX-28 --> |
| `ident_c40_p000` | 0.4<!-- N:DES-9 --> | 0<!-- N:DX-28 --> | 0.2<!-- N:DES-9 --> | — | — |
| `ident_c40_p200` | 0.4<!-- N:DES-9 --> | 0.2<!-- N:DX-28 --> | 0.4<!-- N:DES-9 --> | — | — |
| `ident_c40_p400` | 0.4<!-- N:DES-9 --> | 0.4<!-- N:DX-28 --> | 0.6<!-- N:DES-9 --> | — | — |
| ISO-4 (GPU 2) | 0.5<!-- N:DES-14 --> | 0<!-- N:DES-14 --> | 0<!-- N:DES-14 --> | 0.9256<!-- N:DX-18 --> | 0.7726<!-- N:DX-18 --> |

The p = 0<!-- N:DX-28 --> sweep arm carries exactly ISO-4's training mixture.

| estimate (points) | survival | completion |
|---|---|---|
| sweep slope per unit p (labelled “dose slope”; separate fit) | +0.89 [−0.33, +2.11]<!-- N:SEC-5 --> | −2.51 [−9.43, +4.12]<!-- N:DX-27 --> |
| sweep endpoint, p = 0.5 minus p = 0 | +0.48 [−0.21, +1.17]<!-- N:SEC-5 --> | −0.97 [−4.82, +2.87]<!-- N:DX-27 --> |
| γ<sub>p</sub>, the co-occurrence slope, per unit p | +3.26 [+1.37, +5.02]<!-- N:SEC-1 --> | +2.69 [−6.75, +12.45]<!-- N:DX-27 --> |
| γ<sub>n</sub>, the fire-only-share slope, per unit ν | −2.37 [−4.19, −0.57]<!-- N:SEC-1 --> | −6.52 [−15.34, +2.42]<!-- N:DX-27 --> |
| bound, 0.5 γ<sub>n</sub> | −1.19 [−2.10, −0.28]<!-- N:SEC-2 --> | −3.26 [−7.67, +1.21]<!-- N:DX-27 --> |
| change point in p (labelled “knee”) | 0.375 [0.125, 0.375]<!-- N:DX-28 -->, UNDERPOWERED<!-- N:SEC-6 --> | 0.375 [0.125, 0.375]<!-- N:DX-28 -->, UNDERPOWERED<!-- N:SEC-6 --> |
| plane prediction of JOINT − ISO-4 (γ<sub>p</sub> × 1) | §9.2 | +2.69<!-- N:DX-417 -->; γ<sub>p</sub>'s interval contains both measured values |

The plane $y = \gamma_0 + \gamma_p p + \gamma_n \nu$ is a seed-level ordinary least squares (OLS) fit over all eight arms, and the bound, the fire-only share's part of the sweep's endpoint change, excludes zero on survival. The sweep slope is a separate seed-level OLS fit over the five sweep arms, with an isotonic fit (PAVA) giving its monotone shape. The plane's slope along the sweep is $\gamma_p + \gamma_n$, so the two need not agree, and on completion they do not. The change point is the breakpoint of the best single-hinge fit. Linearity is assumed and checked only coarsely: arm-mean residuals lie within ±0.4 SE on survival and ±1.1 SE on completion, 8 points for 3 parameters<!-- N:DX-39 -->.

Per-coupling frequency, co-occurrence and active share cannot all be held fixed on the triangle. Floors exist only for the sweep's p = 0.5 arm: the other sweep arms assume that floor, and the identification arms are ungraded<!-- N:DX-306 -->. The counter's realized count is endogenous, so nothing here is its causal effect, and mediation is VOID (§9.2).

### I Trained-policy episodes

Figures I1 and I2 show one episode of each confirmatory arm, separately, chosen by a rule fixed before any render: θ\*, episode key 0, stochastic actions, training seed 1 at update 1000<!-- N:ENV-13 -->. Each opens at step 128 of 256<!-- N:DX-410 --><!-- N:ENV-6 -->. They illustrate the environment under a trained policy and grade nothing.

<figure class="l-page">
  <iframe src="{{ 'assets/html/submission/explorer_thetastar_iso_s1_T1000_ep0.html' | relative_url }}" width="100%" height="868" style="border:none" title="Episode explorer, ISO policy, training seed 1" loading="lazy"></iframe>
  <figcaption><strong>Figure I1.</strong> One episode of the ISO policy at θ&#42;. The map is environment state, the smoke field ρ included. Selecting an agent shows its observation as produced (labelled obs v3: the masking observation, §6.1), the true cells, and the probability τ that each was seen. It cannot compare training protocols. <span class="figure-note">Status: illustrative · grades nothing · Interact: play, step, click an agent.</span></figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/explorer_thetastar_iso_s1_T1000_ep0_static.png" class="img-fluid" alt="Maps of one ISO-policy episode at its start, middle and end, with one agent's observation, the true state of the same cells, and the probability each cell was seen" caption="Static companion of Figure I1 for the printed PDF." %}
</div>

Figure I2 shows the JOINT policy's episode under the same rule. One episode of one seed cannot carry a contrast that §9.2 measures over 72 seeds per arm and 512 evaluation episodes<!-- N:DES-3 --><!-- N:DES-13 -->.

<figure class="l-page">
  <iframe src="{{ 'assets/html/submission/explorer_thetastar_joint_s1_T1000_ep0.html' | relative_url }}" width="100%" height="872" style="border:none" title="Episode explorer, JOINT policy, training seed 1" loading="lazy"></iframe>
  <figcaption><strong>Figure I2.</strong> One episode of the JOINT policy at θ&#42;, with the layers and panels of Figure I1; only the observation panel shows what the selected agent perceives. It cannot compare training protocols. <span class="figure-note">Status: illustrative · grades nothing · Interact: as Figure I1.</span></figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/explorer_thetastar_joint_s1_T1000_ep0_static.png" class="img-fluid" alt="Maps of one JOINT-policy episode at its start, middle and end, with one agent's observation, the true state of the same cells, and the probability each cell was seen" caption="Static companion of Figure I2 for the printed PDF." %}
</div>
