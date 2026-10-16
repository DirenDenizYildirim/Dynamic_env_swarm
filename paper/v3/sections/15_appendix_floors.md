<!-- PAPER V3 DRAFT (PAPER V3 ruling, 2026-10-12): builder-drafted, not owner-approved -->

### C Floors

<!-- STUB-SPEC
JOB: Every floor with its GPU, run length, artifact and reps; the exhibits §5 no longer tells, one line each; the floors explorer.
WRITER: W3.
BUDGET: about 500 prose words plus the floor table.
FROM: P1 §6.1 C; P2 §3 A2.
ROWS: METH-1 to METH-5, DX-34, DX-35, DX-38, DX-302, DX-403, DX-412, V5-1, V5-2, V5-3, CB-7, COM-5, HW-1, DES-13.
FIGURES: Figure C1 floors_explorer (gloss once: labelled “M5.1e”, labelled “M6.0”, labelled “per card”, labelled “beat”). Block below.
REGISTERED STRINGS: VOID (comms condition (iii), COM-5).
EVERY OTHER CAVEAT in checks/caveats.yaml: pointer only ("§6.3", "Appendix D"), never restated. C26: any sentence about the interaction check carries "post hoc".
NOT HERE: "floors grow ordered by curriculum difficulty" (an untested hypothesis, METH-5 note); "every bar has a floor".
V2 MATERIAL: paper/v2/sections/13_appendix_locks_floors.md (C); 08_methodology.md (the exhibits).
DEPENDENCIES: §5 points here.
-->

A floor is the standard deviation of a metric over identical reruns at one seed, so it measures nondeterminism alone (§5). The table lists every floor this paper uses, with its GPU, run length, artifact and number of reruns. Paired values are ISO, then JOINT. Each study is named in plain words with its code (key in Appendix D). The confirmatory arms' floors use eight<!-- N:DX-403 --> reruns, because four leave a standard deviation uncertain by about ±40 %<!-- N:DX-303 -->.

| study (code) | GPU, updates | arms or artifact | reruns | floor | use |
|---|---|---|---|---|---|
| four-run Medium floor study (M5.1e) | RTX 5090, 500<!-- N:DX-403 --> | Medium | 4<!-- N:DX-403 --> | completion 0.0145, survival 0.0129<!-- N:METH-1 --> | the content ablation's Medium threshold |
| denial study (M5.5) | RTX PRO 6000, 500<!-- N:DX-412 --> | Medium, communication range 16<!-- N:METH-1 --> | 4<!-- N:DX-412 --> | completion 0.0399, survival 0.0130<!-- N:METH-1 --> | the denial thresholds (§4.4); the per-GPU exhibit |
| denial study, danger moments (M5.5) | RTX PRO 6000, 500<!-- N:DX-412 --> | Medium | 4<!-- N:DX-412 --> | 27.2 % (sd 0.00182)<!-- N:COM-5 --> | voids a 20 %<!-- N:COM-5 --> threshold |
| content ablation at High (M5.3b) | RTX PRO 6000<!-- N:DX-403 -->, 500<!-- N:DX-40 --> | High | 4<!-- N:DX-40 --> | completion 0.0522<!-- N:V4-3 -->, survival 0.0621<!-- N:CB-7 --> | the High content ablation's thresholds; a reference scale (cross-artifact) in §4.3 |
| refactor of the environment code (M6.0) | RTX PRO 6000<!-- N:DX-5 --> | two code versions | 4 comparisons<!-- N:METH-2 --> | reference version: 0 of 760 per-field trajectory hashes differ, in 4 of 4 comparisons; refactored version: differs in 1 of 4<!-- N:METH-2 --> | the per-artifact exhibit |
| confirmatory arms' floor study, 500 updates (M6.2) | RTX PRO 6000, 500<!-- N:DX-34 --> | ISO, JOINT | 8<!-- N:DX-403 --> | completion 0.0165, 0.0093<!-- N:DX-34 --> | the retired convergence check |
| confirmatory arms' floor study, 1000 updates (M6.2b) | RTX PRO 6000, 1000<!-- N:DX-34 --> | ISO, JOINT | 8<!-- N:DX-403 --> | completion 0.0339, 0.0483<!-- N:DX-34 --> | set the design seed count, k = 40<!-- N:DES-1 --> |
| the grid's launch floor study (G1.2 protocol) | RTX PRO 6000<!-- N:DES-5 -->, 1000<!-- N:DX-403 --> | ISO, JOINT, sweep arm at p = 0.5<!-- N:DX-28 --> | 8<!-- N:DX-403 --> | sd(Γ) at k = 40: completion 0.00504, survival 0.00310<!-- N:DES-5 --> | design-stage power |
| re-measurement before the grid | RTX PRO 6000<!-- N:DES-2 -->, 1000<!-- N:DX-412 --> | ISO, JOINT, sweep arm at p = 0.5<!-- N:DX-28 --> | 8<!-- N:DX-403 --> | the seed rule gave k = 46<!-- N:DES-2 --> | the registered seed rule (Appendix D) |
| re-measurement on the grid's GPU | RTX 5090<!-- N:DX-35 -->, 1000<!-- N:DX-412 --> | ISO, JOINT, sweep arm at p = 0.5<!-- N:DX-28 --> | 8<!-- N:DX-35 --> | completion 0.0587, 0.0577; survival 0.0100, 0.0112<!-- N:DX-35 --> | the seed rule (k = 72<!-- N:DES-3 -->); the check that an effect exceeds rerun noise |
| High readout | the grid GPU's floor runs (1000<!-- N:DX-412 --> updates), evaluated at High on a third GPU of the same model<!-- N:V5-2 --> | ISO, JOINT at High | 8<!-- N:V5-2 --> | completion 0.0681, 0.0613; survival 0.0180, 0.0395<!-- N:V5-2 --> | the rerun-noise check at High (Appendix E) |
| evaluation | the same third GPU<!-- N:HW-4 --> | two checkpoints<!-- N:HW-2 --> | 4<!-- N:HW-2 --> | bit-identical<!-- N:HW-2 --> | evaluation reproducibility (§8) |
| partial re-measurement on a second rented GPU | not recorded<!-- N:DX-36 -->, 1000<!-- N:V5-3 --> | ISO, JOINT | 8 + 4<!-- N:DX-36 --> | none reported | provenance only |

The grid GPU's floors cannot be told apart from those of the re-measurement before the grid: the 95 %<!-- N:DX-35 --> intervals for the standard deviation overlap (ISO completion: [0.0186, 0.0571] on the RTX PRO 6000, [0.0388, 0.1194] on the RTX 5090<!-- N:DX-35 -->). No claim is made that either GPU is less reproducible.

- **Thresholds set before the protocol.** Before the protocol existed, four<!-- N:V5-1 --> thresholds were set on constants the record later called invented. The Coupling-B calibration grid graded its High survival effect against a two-seed spread of 0.0295<!-- N:DX-38 -->, below the High floor later measured at 0.0621<!-- N:CB-7 -->, and its "strong" grade was retracted. The content ablation at Medium applied a floor hard-coded from the four-run Medium floor study instead of one measured on its own runs. Re-sited at High, it measured its floor first, but matching Medium's resolution would have taken roughly 46<!-- N:DX-302 --> seeds per arm. The denial study set a 20 %<!-- N:COM-5 --> threshold on danger-moment outcomes below that quantity's rerun nondeterminism of 27.2 %<!-- N:COM-5 -->, so that condition is VOID: the observed 23.2 %<!-- N:COM-5 --> exceeded the threshold but not the noise.
- **The content checks of communication.** These used the thresholds in the table's first and fourth rows. At Medium (two<!-- N:COM-2 --> seeds), no pair of actual, zeroed and shuffled messages differed beyond about 3 points<!-- N:COM-2 -->; at High, raising the mean number of in-range partners from 1.01 to 2.99<!-- N:COM-3 --> changed nothing.
- **Per GPU.** The Medium completion floor moved from 0.0145 to 0.0399, 2.75-fold<!-- N:METH-1 -->, while survival's stayed at 0.0129 against 0.0130<!-- N:METH-1 -->. The GPU, the code version and the configuration all differed between the two studies, so the exhibit cannot say which of them moved the completion floor.
- **Per artifact.** In the refactor of the environment code, the reference version's rerun floor read zero, so two<!-- N:METH-2 --> masking diagnostics at High that differed between the versions looked like a semantic change. The refactored version then differed from itself 1 time in 4<!-- N:METH-2 --> on the same channels. An equivalence claim between A and B needs A against A and B against B, as well as A against B.
- **The contrast's standard error.** At k = 34<!-- N:METH-3 -->, on the 1000<!-- N:DX-34 -->-update completion floors and a 0.03<!-- N:DES-4 --> effect, each arm's own $s\sqrt{2/k}$ gave 92.1 % and 62.8 %<!-- N:METH-3 --> power, where the contrast's power was 76.7 %<!-- N:METH-3 -->.
- **The 80 %-power rule.** The confirmatory seed count was first set at k = 20<!-- N:METH-4 --> on a bare 2σ figure, without the Šidák correction for the two co-primaries ($z_\alpha = 2.2365$<!-- N:DES-13 -->). Corrected, completion had 55.6 %<!-- N:METH-4 --> power against its motivating effect band, a slip caught before any run.
- **Run length.** From 500 to 1000<!-- N:DX-34 --> updates, the completion floor grew 2.1-fold for ISO and 5.2-fold for JOINT<!-- N:METH-5 -->, with run length confounded with machine.
- **Dividing by a floor.** A registered convergence check divided each arm's late-training drift by its floor, so it fired when JOINT's floor fell faster than its drift. It was retired before the grid, and the estimand was fixed as the gap at a matched budget of 1000<!-- N:DES-13 --> updates.
- **Differenced tests.** In 24 of 24<!-- N:DX-32 --> rendered episodes of the Coupling-B calibration grid, the alive agents' centroid drifted towards a wall (rendered-pixel centroids, a diagnostic). That grid's condition "no cross-arm exposure/positioning difference" could not see a drift present in both arms.
- **Coverage.** In the secondary design, floors exist only for the sweep arm at p = 0.5<!-- N:DX-28 -->; the other sweep arms assume that floor, and the identification arm has none<!-- N:DX-306 -->. ISO-4 has no identical reruns, so the contrasts that involve it are graded on seed dispersion alone.

<!-- FIGURE C1: block carried from paper/v2/sections/08_methodology.md:22 (markup, iframe height and alt text as v2 had them); caption replaced; alt text checked by W3 against the figure (kept) -->

<figure class="l-page">
  <iframe src="{{ 'assets/html/submission/floors_explorer.html' | relative_url }}" width="100%" height="472" style="border:none" title="Floors explorer: reproducibility floors per GPU, per artifact and per run length, and the confirmatory grid against its floor" loading="lazy"></iframe>
  <figcaption><strong>Figure C1.</strong> Reproducibility floors, one tab each. The first tab shows the Medium floors of the four-run floor study on an RTX 5090 (labelled “M5.1e” on the figure) and of the denial study (M5.5) on an RTX PRO 6000, labelled “per card” on the figure; “card” is the GPU, “box” the machine and “code tree” the code version. The second shows rerun comparisons within and between two versions of the environment code (labelled “M6.0” on the figure), where “traced” is the refactored version, “baseline” the reference and “field digests” per-field trajectory hashes. The third shows completion floors at 500 and 1000<!-- N:DX-34 --> updates, and the fourth the confirmatory grid's seed dispersion against its floor, with survival's gap against its floor-based standard error, labelled “floor-basis sd(Γ)” on the figure. <span class="interact">Click a tab or press ← / →; hover or tab to a mark.</span></figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/floors_explorer.png" class="img-fluid" alt="Reproducibility floors on two GPUs, rerun comparisons of two versions of the code, floor growth from the shorter to the longer run length, and the confirmatory grid's seed dispersion against its floor, each with its confound stated." caption="Static companion of Figure C1 for the printed PDF." %}
</div>
