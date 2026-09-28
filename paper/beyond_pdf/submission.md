---
layout: distill
# <!-- PROVISIONAL: owner chooses the title -->
# First candidate under "Title candidates (branch B)" in paper/00_common_spine.md.
# The word "ambient" in it is not yet ratified (owner decision pending since 2026-08-05).
title: "Paid in agents, not in composition: a pre-registered test of joint vs isolated training under ambient hazards"
# <!-- PROVISIONAL: owner rules what description carries -->
# The kit's instructions say "[Your abstract]". The layout needs one line with no double quote,
# and live Beyond PDF submissions use one or two sentences (KIT_NOTES.md S1.4, S1.9 item 1).
# Proposal: the abstract's first sentence, verbatim. The full abstract is the Abstract section.
description: >-
  We introduce the Compound Hostile Environment (CHE), a pure-JAX
  multi-agent RL environment in which a cellular-automaton fire is causally
  coupled to structural collapse (collapse seeds fire) and to perception
  (smoke attenuates observation by Beer–Lambert transmittance), with an
  independent communication-denial axis.
htmlwidgets: true

# Strict double-blind: Anonymous until camera-ready. No name, url or affiliation.
authors:
  - name: Anonymous
    affiliations:
      name: Anonymous

# Kit rule: must be exactly "submission.bib".
bibliography: submission.bib

# Each name must equal its heading's text: the link is slugify(name), the target is the heading's id.
toc:
  - name: Abstract
  - name: 1 Introduction
  - name: 2 Related work
  - name: 3 The environment
  - name: 4 Severity calibration
  - name: "5 Coupling A: hazard begets hazard"
  - name: "6 Coupling B: hazard degrades perception"
  - name: "7 The comms axis: inert under this encoder at this scale, by a joint argument"
  - name: "8 Methodology: bars come with floors"
  - name: "9 The compositional test: design, and the branch-B result"
    subsections:
      - name: Design
      - name: "Results: branch B, with the inert-share qualifier"
  - name: 10 Limitations
  - name: 11 Reproducibility and appendix manifest
  - name: Appendices
---

<!--
SKELETON, milestone S2 (2026-09-27): structure, not prose.
Port source: paper/00_common_spine.md; record behind section 9: paper/branch_B.md.
Numbers: only with a row in paper/numbers_ledger.md, and each carries its row ID in an
N:ID comment right after it. A number with no row is listed for the owner, never derived.
Figures 1 to 10 are the spine's figure list, as labelled slots naming their committed data.
GIFs illustrate and never grade (paper/renders/2026-09-27/README.md).
Double-blind: no repo URL, account name or resolving hash anywhere in this file or in assets/.
Kit mechanics (KIT_NOTES.md): no dollar signs in the body, no Liquid delimiters in comments.
-->

## Abstract

<!-- Verbatim from paper/00_common_spine.md "Abstract — branch B"; blockquote markers dropped and the line break inside "collapse-seeded" joined. The inert-share qualifier is registered (decision log, UNBLIND RESULT) and stays on every revision. TODO(port): none, beyond owner edits. -->

We introduce the Compound Hostile Environment (CHE), a pure-JAX
multi-agent RL environment in which a cellular-automaton fire is causally
coupled to structural collapse (collapse seeds fire) and to perception
(smoke attenuates observation by Beer–Lambert transmittance), with an
independent communication-denial axis. The hazard is an *ambient survival
stressor*: it enters neither the reward nor any cost or constraint channel;
the reward sees only task variables and agent deaths, which it prices the
same whatever their cause. Three properties make CHE an
instrument rather than a demo: severity is defined by a *measured*
percolation critical point (β̂_c = 0.500 ± 0.005<!-- N:CAL-1 -->, reproducing Kesten's
exact value), every stressor is a parameter of one kernel so that
ablations are *bitwise exact* nested models, and every acceptance bar in
the paper is graded against a measured reproducibility floor. Calibration
yields four findings independent of any training comparison: collapse-seeded
fire self-limits where the hazard is worst; compound hostility is
rare and bursty; perception decay cannot be behaviourally suppressed; and
inter-agent communication is inert under a frozen random-projection
message encoder at this scale. We then run a pre-registered, mechanically
blinded test of compositional generalization: whether training on
co-occurring stressors beats training on the same stressors in isolation,
at a held-out severity and matched compute (k = 72<!-- N:DES-13 --> seeds per arm; the
registered k = 60<!-- N:RES-3 --> prefix reads the same). At matched compute, joint
training improves survival at the held-out severity by 0.96 points<!-- N:RES-2 -->
(family-wise 95 % CI [0.47, 1.44]<!-- N:RES-2 -->, Šidák-corrected for the two<!-- N:DES-13 -->
co-primaries), while task completion shows no gain larger than 0.66 points<!-- N:RES-1 -->
at the same level: the asymmetry the registered falsifier requires. **The
survival advantage does not survive the pre-registered inert-share
correction.** An isolated-training arm without its fire-only episodes
matches joint training (difference −0.03 points<!-- N:RES-6 -->, replicated on the same
hardware), and a secondary dose design attributes the gap to fire-only
training episodes rather than to composition. The contrast's sign is not
stable over the final half of training: the survival gap opens only in the
last fifth<!-- N:RES-12 --> of the budget and is still growing at the matched budget. All
code, configs, locks and the frozen analysis plan are released.

## 1 Introduction

Port from `paper/00_common_spine.md` §1, in the order of the spine's contribution list. <!-- TODO(port) -->

## 2 Related work

Port from `paper/00_common_spine.md` §2; citations as `d-cite` keys from `assets/bibliography/submission.bib`. <!-- TODO(port): the UED / domain-randomization paragraph starts from the DRAFT in paper/related_work_verification.md Part 2, after the owner's reads. -->

## 3 The environment

Port from `paper/00_common_spine.md` §3. <!-- TODO(port): carry Def. 2 as reworded (DEF. 2 WORDING RULING), the hazard-blind vs hazard-priced note, and the Phase-2 death-penalty ablation with its scope (ledger ENV-2 to ENV-5). Describe training as it ran (ledger ENV-11; O-1 owner wording). Use "multi-agent", not "swarm", as a claim. -->

> **Figure 1 (slot).** Env schematic: the five kernels and the step order, with the two couplings drawn as arrows.
> *Status:* draft now (no data). *Source:* Prop. 1 step order, `docs/theory_foundations.md`.
<!-- FIGURE 1 TODO(figure) -->

<!-- GIF SLOT 1: committed render, paper/renders/2026-09-27/ (selection rule and reading rules in its README). One episode, stochastic actions. It illustrates and grades nothing. Before submission the caption must state the renderer's limits: no structure or collapse layer, so collapse-seeded ignitions are not distinguished from other fire; the white overlay is the smoke field, not what an agent perceives; the end-of-episode drift to the walls is the known artifact (spine section 10, item 6). The static companion below carries the GIF into the browser-printed PDF. TODO(port): caption. -->

{% include figure.html path="assets/gif/submission/thetastar_random_seed0.gif" alt="Random-policy episode at theta-star" class="img-fluid rounded" caption="GIF slot 1 (placeholder caption). One episode of a random policy at θ*. Illustrates the hazard; grades nothing." %}

{% include figure.html path="assets/img/submission/thetastar_random_seed0_static.png" alt="First, middle and final frame of the random-policy episode" class="img-fluid rounded" caption="Static companion for the printed PDF: the first, middle and final frame of the episode above." %}

## 4 Severity calibration

Port from `paper/00_common_spine.md` §4. <!-- TODO(port): ledger O-2 is open (no committed artifact for the R_L logistic centres behind the critical-point estimate). -->

> **Figure 2 (slot).** Percolation calibration: `P_span` and `R_L` vs β at three L<!-- N:CAL-1 -->; `β̂_c` marked; the three severity levels<!-- N:CAL-3 -->.
> *Status:* data committed. *Source:* `che/bench/results/phase2/` (`calibration_crossing.npz`, `calibration.npz`, `estimates.json`, `calibration_report.md`); levels locked in `severity_lock.md`.
<!-- FIGURE 2 TODO(figure): the R_L logistic-centre estimate has no committed artifact yet (ledger O-2). -->

## 5 Coupling A: hazard begets hazard

Port from `paper/00_common_spine.md` §5. <!-- TODO(port) -->

> **Figure 3 (slot).** Coupling A: Prop. 3 linear handshake; seeded ignitions vs severity (the 4.83×<!-- N:CA-4 --> fall).
> *Status:* data committed. *Source:* handshake `che/bench/results/phase3/m33/prop3_L64.json` and `.npz`; seeded ignitions `che/bench/results/e1/severity/severity.json` (m44), replication in `che/bench/results/phase3/phase3_report.md` (m35).
<!-- FIGURE 3 TODO(figure): the two Prop. 3 runs are two runs, not one (ledger CA-2, CA-3). -->

## 6 Coupling B: hazard degrades perception

Port from `paper/00_common_spine.md` §6. <!-- TODO(port): the scope note on "co-active" goes wherever the counter is used (spine section 6). -->

> **Figure 4 (slot).** Coupling B: masking concentration on danger moments; High survival effect with floor bars.
> *Status:* data committed. *Source:* `che/bench/results/phase4/m44/m44_analysis.json`, `che/bench/results/phase4/phase4_report.md`; replicate deltas `che/bench/results/phase5/pretask/replicate_deltas.txt`; High floor `che/bench/results/phase5/m53b/reproducibility_floor_high.txt`.
<!-- FIGURE 4 TODO(figure): floor bars required; lead with the replicated effect, the first estimate only beside it (ledger CB-5, CB-6). -->

> **Figure 5 (slot).** Co-active event distribution per episode at three severities<!-- N:CO-2 -->.
> *Status:* data committed. *Source:* `che/bench/results/phase4/phase4_report.md` (Result 4, the Coupling-B-on rows) and `che/bench/results/e1/e11_report.md`.
<!-- FIGURE 5 TODO(figure): show the distribution, never the mean alone; the caption carries the counter's scope (co-active only where Coupling B is also on). -->

## 7 The comms axis: inert under this encoder at this scale, by a joint argument

Port from `paper/00_common_spine.md` §7. <!-- TODO(port): write "inert under a frozen random-projection encoder at this scale", never "certified inert" (pre-submission checklist). -->

> **Figure 6 (slot).** Comms: VoC handshake; δ = 0 vs 1<!-- N:COM-4 --> with floor bars.
> *Status:* data committed. *Source:* VoC `che/bench/results/phase5/m52/e2c2_sweep.json`; denial arms and floor `che/bench/results/phase5/m55/`; `che/bench/results/phase5/phase5_report.md`.
<!-- FIGURE 6 TODO(figure): floor bars required. -->

## 8 Methodology: bars come with floors

Port from `paper/00_common_spine.md` §8. <!-- TODO(port) -->

> **Figure 7 (slot).** Floors: per-card, per-run-length, per-artifact bar chart.
> *Status:* data committed. *Source:* per-card `che/bench/results/phase5/m51e/reproducibility_floor.txt` and `che/bench/results/phase5/m55/reproducibility_floor_medium.txt`; per-artifact `che/bench/results/phase6/m60/m60_report.md`; per-run-length `che/bench/results/phase6/m62/floors.json` and `che/bench/results/phase6/m62b/m62b_report.md`.
<!-- FIGURE 7 TODO(figure): card is confounded with code tree in the per-card pair, and run length with box in the per-run-length pair (ledger METH-1, METH-5); the caption says so. -->

## 9 The compositional test: design, and the branch-B result

Port the section lead-in from `paper/00_common_spine.md` §9. <!-- TODO(port) -->

### Design

Port from `paper/00_common_spine.md` §9.1. <!-- TODO(port): the seed-count history is stated as a deviation (ledger DES-1 to DES-3); blinding is described in-text by date, never by hash or link. -->

### Results: branch B, with the inert-share qualifier

Port from `paper/00_common_spine.md` §9.2 (record: `paper/branch_B.md`). <!-- TODO(port): the registered reading comes first in every item; the survival effect is never called a composition effect without the inert-share qualifier. -->

> **Figure 8 (slot).** The confirmatory contrast with CI and MDE band, with Γ₄, Γ₄′ and B̂ beside it (the inert-share correction is the centre of this section).
> *Status:* data committed. *Source:* `che/bench/results/phase6/unblind/`, `che/bench/results/phase6/post_unblind_analysis/`, `che/bench/results/phase6/secondary/`.
<!-- FIGURE 8 TODO(figure): intervals at their registered level; the registered reading first. -->

> **Figure 9 (slot).** Γ(t) over the final half, both co-primaries, Šidák bands; the single-card curve as a companion.
> *Status:* data committed. *Source:* `che/bench/results/phase6/post_unblind_analysis/`.
<!-- FIGURE 9 TODO(figure): the registered verdict is "sign unstable over the final half" on both co-primaries; report it first, the shape second. -->

> **Figure 10 (slot).** Dose sweep and identification arm, labelled secondary; the `γ_p` plane with its non-extrapolation to JOINT marked.
> *Status:* data committed. *Source:* `che/bench/results/phase6/secondary/`.
<!-- FIGURE 10 TODO(figure): non-verdict-bearing; many intervals, none family-corrected; knees UNDERPOWERED. -->

<!-- GIF SLOT 2, OWNER DECISION PENDING (paper/renders/2026-09-27/README.md): whether to show the ISO and JOINT seed-1 episodes at all, and side by side. The files are in assets/gif/submission/ (thetastar_iso_s1_T1000_ep0.gif, thetastar_joint_s1_T1000_ep0.gif) with static companions in assets/img/submission/. They are not placed. If they are shown, the caption states that each is one pre-selected episode and gives the measured effect with its interval (ledger RES-2); they are never captioned as showing the result. -->
> **GIF slot 2 (owner decision pending).** Trained-policy episodes, ISO and JOINT. Not placed.

## 10 Limitations

Port from `paper/00_common_spine.md` §10, every item, in its order. <!-- TODO(port): omitting an item where the outcome makes it awkward is outcome-dependent disclosure. -->

## 11 Reproducibility and appendix manifest

Port from `paper/00_common_spine.md` §11. <!-- TODO(port): ledger O-3 (supplement size) and O-4 (venue limit) are open; the supplement is described without links. -->

## Appendices

Manifest from `paper/00_common_spine.md` §11. <!-- TODO(port) -->

### A. Full proofs

Port per spine §11, appendix A (Props. 1–4, Thm. 1, Remark 2′). <!-- TODO(port) -->

### B. Calibration protocol and every lock with its record

Port per spine §11, appendix B. <!-- TODO(port) -->

### C. Floors: every measured floor with card, run length, and artifact

Port per spine §11, appendix C. <!-- TODO(port) -->

### D. The frozen analysis plan, verbatim, with its registration date

Port per spine §11, appendix D. <!-- TODO(port) -->

### E. The four registered outcome branches, verbatim, with the falsifiers

Port per spine §11, appendix E. <!-- TODO(port) -->

### F. Grid provenance: cards, block structure, chunk boundaries, archive hashes

Port per spine §11, appendix F. <!-- TODO(port): archive sha256 values only; no hash that resolves to an account. -->

### G. Throughput and the keep-alive-set statement for every env-only figure

Port per spine §11, appendix G. <!-- TODO(port) -->

### H. Γ(t) curves and the sign-stability reading

Port per spine §11, appendix H. <!-- TODO(port) -->

### I. Secondary sweeps with UNDERPOWERED flags where applicable

Port per spine §11, appendix I. <!-- TODO(port) -->
