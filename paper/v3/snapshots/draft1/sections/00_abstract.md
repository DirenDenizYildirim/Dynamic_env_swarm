<!-- PAPER V3 DRAFT (PAPER V3 ruling, 2026-10-12): builder-drafted, not owner-approved -->

<!-- STUB-SPEC
JOB: One question, one result, one lesson (V3-F2; PROF 4). Body text before the hero, no heading.
WRITER: W1 (also front_matter.yaml title and description; title candidates and description in provenance/00_abstract.md).
BUDGET: at most 250 prose words, comments excluded (P1 §3; P3 §2.2; BLIND §6 item 7).
FROM: P1 §3.1 (moves), §3.2 (description), §3.3 (lesson templates); P3 §2.2; PAPER V3 item 3.
ORDER:
  - (1) The environment, 2 or 3 sentences: CHE, pure JAX, multi-agent; a cellular-automaton fire in every episode; collapse seeds fire (Coupling A); smoke attenuates perception by Beer–Lambert transmittance (Coupling B); communication denial independent; the reward never reads the fire and prices every death the same; severity placed relative to a measured percolation threshold; switching a stressor off reproduces the nested model bit for bit; the code is supplied. Rows: ENV-1, ENV-6, CAL-3 (no calibration number is needed).
  - (2) The question, 1 sentence: as a worked example, a pre-registered test of whether training one policy on co-occurring stressors beats training it on each in isolation, at matched compute, at a held-out near-critical severity. Rows: DES-13, CAL-3.
  - (3) The result, 2 or 3 sentences, registered strings verbatim: survival up 0.96 points with its Šidák-corrected CI (RES-2), about a tenth of an agent per episode (X4-3), only at the end of training (RES-12); it does not survive the inert-share correction (RES-6), which removes the third of isolated training that carried no active stressor, a design error registered with its correction before unblinding (DES-8, DES-15); completion excludes a joint-training gain larger than 0.66 points (RES-1); both differences are sign unstable over the final half (RES-11). The 72-seed deviation is not needed here.
  - (4) The lesson, 1 or 2 sentences, labelled post hoc where it uses the check (HOLE). Any advice is its own labelled sentence, never after therefore, so or thus.
ROWS: ENV-1, ENV-6, CAL-3, DES-8, DES-13, DES-15, RES-1, RES-2, RES-6, RES-11, RES-12, X4-3 (W4 writes it; cite the ID), IC-* (orchestrator, after step 0.5).
REGISTERED STRINGS: "does not survive the inert-share correction"; "sign unstable over the final half"; "excludes a joint-training gain larger than 0.66 points"; "at matched compute". "Null" at most an informal gloss (log:6166), never the result's name.
SHORT FORMS ALLOWED HERE (at most one sentence each; the full statement is at the home):
  C01 sited_where_composition_is_weak (home 06_example_design.md)
  C02 delta_inert_ruled_phrase (home 04_calibration.md)
  C08 active_share_identity (home 06_example_design.md)
  C10 inert_third_design_error (home 06_example_design.md)
  C11 matched_compute_never_convergence (home 06_example_design.md)
  C15 secondary_non_verdict_bearing (home 07_example_results.md)
  C16 sign_unstable_final_half (home 07_example_results.md)
  C17 completion_exclusion_bound (home 07_example_results.md)
  C18 inert_share_correction (home 07_example_results.md)
  C27 cannot_isolate_co_occurrence (home 09_example_lesson.md)
EVERY OTHER CAVEAT in checks/caveats.yaml: pointer only ("§6.3", "Appendix D"), never restated. C26: any sentence about the interaction check carries "post hoc".
HOLES:
  - the lesson sentence(s): pick the row of P1 §3.3 (N, Pn, Pp, M, D) that matches the check's pooled reading under PLAN §7; if the results are not back, use the identity lesson (row M without the check). V3Q7.
  - description in front_matter.yaml: recheck against the final abstract (one line, no double quote, no colon-space, no number).
OWNER-PENDING:
  - the disclosure footnote is the OWNER's (PAPER V3 item 6): leave the comment marker shown below in place, after the first sentence; write no footnote text.
  - title (V3Q1): put P1's T1 in front_matter.yaml; give 3 to 5 candidates in provenance (P1 §2: T1, T1s, T2, T3, T4), with what each leads with.
  - naming CHE in full (v2 B3 default: named).
NOT HERE: "composition effect" without the correction string; "null" as the result's name; converged, budget-robust, certified, swarm, PBT, finite Dec-POMDP, one transition kernel; "pre-registered" for the correction; study codes; any date (V3-S2); the hazard-blind reward as the lead; the professor's "mostly Coupling A" (a review, not a ruling); any interaction-check number before IC rows exist.
V2 MATERIAL: paper/v2/sections/00_abstract.md and provenance/00_abstract.md (v2's title candidates and description).
DEPENDENCIES: X4-3 (W4); IC rows (orchestrator); the lesson of 09_example_lesson.md (W5) must agree with this abstract's lesson.
-->

We present the Compound Hostile Environment (CHE), a pure-JAX multi-agent environment in which a cellular-automaton fire burns in every episode.<!-- OWNER: disclosure d-footnote here (after the first sentence; the owner writes it, PAPER V3 item 6) --><!-- OWNER-PENDING:V3Q1 title in front_matter.yaml is P1's T1; candidates in provenance/00_abstract.md --><!-- OWNER-PENDING:B3 CHE named in full in the abstract (carried v2 default) --> Structural collapse seeds ignitions (Coupling A), smoke attenuates perception by Beer–Lambert transmittance (Coupling B), and communication denial is an independent third stressor. The reward never reads the fire and prices every death the same. Severity is placed relative to a measured percolation threshold, switching a stressor off reproduces the environment without it bit for bit, and the code is supplied.

As a worked example, we report a pre-registered test of whether training one policy on co-occurring stressors beats training it on each in isolation, at matched compute, at a held-out near-critical severity. Joint training raises survival by 0.96<!-- N:RES-2 --> points (Šidák-corrected 95 %<!-- N:DES-13 --> CI [+0.47, +1.44]<!-- N:RES-2 -->), about a tenth<!-- N:X4-3 --> of an agent per episode (0.11<!-- N:X4-3 --> of 12<!-- N:ENV-6 --> agents), visible only in the last fifth<!-- N:RES-12 --> of training. The survival gain does not survive the inert-share correction. The correction removes from isolated training the third<!-- N:DES-8 --> of episodes whose only stressor, communication denial, is inert under a frozen random-projection encoder at this scale. Keeping that third was our design error; we registered the correction before any outcome contrast was computed. Completion shows no detectable change and excludes a joint-training gain larger than 0.66<!-- N:RES-1 --> points. Both differences are sign unstable over the final half of training: each changes sign between checkpoints.

<!-- HOLE:INTERACTION -->
<!-- OWNER-PENDING:V3Q7 -->
<!-- fills: the lesson sentence(s), labelled post hoc; P1 §3.3 templates; PLAN §7 reading rules. DRAFTED NOW with the identity lesson (P1 §3.3 row "Not back in time" = row M without the check; WRITERS §4 item 4; V3Q7). Revisit when IC rows exist: keep, extend with the check's pooled reading (labelled post hoc), or replace by the matching P1 §3.3 row; §6.5 (W5) must state the same lesson. -->
Because the share of training with an active stressor equals the two couplings' frequencies summed, less their co-occurrence ($\mu_A + \mu_B - p$), matching that share alone cannot isolate co-occurrence.
