<!-- PAPER V3 DRAFT (PAPER V3 ruling, 2026-10-12): builder-drafted, not owner-approved -->

### D Registration timeline

<!-- STUB-SPEC
JOB: The audit trail that leaves the main text (V3-S2): every date, ruling, provenance item, GPU block, study code, seed and archive, plus the registration statement (V3-V2) and the framing change (V3-F5's second home). Plain, dated, sourced.
WRITER: W4.
BUDGET: about 1,000 prose words plus tables and verbatim quotations.
FROM: V3-S2; P1 §6.2; v2 BRIEF §7 (the F3 table); v2 Appendices D to F; P3 §3.1 point (5).
ORDER:
  - D.1 Registration statement (V3-V2): the record is internal and version-controlled; its dates are self-reported; the supplement carries the registration documents (phase6_design_v2.md, phase6_framing_branches.md) with a hash manifest; a public registry (OSF) next time. What a reader can check, and what rests on the authors' history (this checkout is shallow; the full-history check is the owner's, V3Q16).
  - D.2 Dated events (table: date | event | row/source): environment locks (DX-401, DX-402); the comms axis closed as inert 2026-07-30 (V6-2); design registered 2026-08-02 with δ retained, two δ-only components of six in ISO, δ excluded from the sweeps (V6-3); co-primaries ruled 2026-08-02 (DES-12); outcome branches and falsifier 2026-08-13 (DES-12); the frozen plan amended 2026-08-13 (V6-5); the bias identified 2026-08-16 by a review of the registered design, pre-grid (V6-1); grid 2026-09-09 to 09-22 (DES-12); the bias and ISO-4 with its reading rule registered 2026-09-18, mid-grid, 120 of 252 runs, on the owner's attestation (DES-15; log:3907-3909); pre-unblind rulings and the fifth outcome cell 2026-09-26 (DX-405, DX-102); unblinding 2026-09-26 (DES-12); the secondary specification ratified after Γ and before the sweep was read (DX-413); the same-GPU replicate proposed after Γ₄ was seen (DES-15); the framing change 2026-10-12 (X4-5). Use the v2 BRIEF §7 table (copied verbatim in this BRIEF) for the F3 rows; state no day count.
  - D.3 Quotations, verbatim, with their dates: the frozen plan's estimand and reading rules (v2 Appendix D items, trimmed to the rules the paper uses; never paraphrase inside a quotation; a "§" inside a quotation is the record's own); the registered outcome branches table (PFB:101-104, venue-lean column omitted and said so), the fifth cell A_c (DX-405, DX-102); the falsifier and its margin (RES-5); branch B's registered headline "composition is paid in agents, not task return" no longer holds as worded; "the branch label stays B"; branch A, the founding hypothesis, did not occur. If the owner agrees (V3Q22), note that the registration listed the environment items as standing on every outcome (PFB:53-76), with its overclaims flagged (PFB:69, :75, :82).
  - D.4 The seed rule's history: k = 40 registered, 46 on the re-measured floor, cap 60, 72 realized as a recorded deviation before unblinding (DES-1 to DES-5); realized power (DES-4, DES-6).
  - D.5 Bias (b) in full: its readings (DES-10, DES-11, V6-4), "reverses sign on the grid GPU".
  - D.6 GPU blocks: Γ on GPU 1 (all 72 seeds of ISO and JOINT), ISO-4 and the 2000-update subsample on GPU 2, post-unblind evaluations on GPU 3, the superseded RTX PRO 6000 seeds descriptive only (HW-4, DX-5, DX-30, DX-36). "GPU 1/2/3" appear only here.
  - D.7 Study codes, a key table: code | plain name | where used (M3.0 … M6.2b, G1.2, G1.3, m35, m44, E1.1, E2C, E2C²).
  - D.8 Seeds and archives: shared seed integers, seed 0 reserved for floors, never in the grid (DX-416); seed-major order and chunking; 615 of 615 archive hashes matched on re-verification (DX-408; no hash quoted; v2 F1's 636-vs-615 question open).
  - D.9 Blinding: one look per stage; analysis scripts refuse to run out of order (DX-411); the inventory of outcome-derived quantities visible before unblinding is owner-attested only (V3Q19): leave a marker, state nothing.
  - D.10 The framing change: the owner's ruling of 2026-10-12 moved the paper's emphasis to the environment after the result was known; the registered branches stay the record of the original framing (X4-5; PAPER V3 item 3).
ROWS: DX-401, DX-402, V6-1, V6-2, V6-3, V6-4, V6-5, DES-1 to DES-6, DES-10, DES-11, DES-12, DES-15, DX-405, DX-102, DX-413, RES-5, HW-4, DX-5, DX-30, DX-36, DX-408, DX-411, DX-416, X4-5.
REGISTERED STRINGS: every quotation verbatim; "no longer holds as worded"; "the branch label stays B"; bias (b) "reverses sign on the grid GPU"; "registered before unblinding" for the correction.
EVERY OTHER CAVEAT in checks/caveats.yaml: pointer only ("§6.3", "Appendix D"), never restated. C26: any sentence about the interaction check carries "post hoc".
NEW ROWS OWED:
  - X4-5 (W4): 2026-10-12, the framing change (the owner's environment-first ruling), VERIFIED at docs/decision_log.md:6115 and :6158-6169.
OWNER-PENDING:
  - D.1 full-history check and content hashes (V3Q16).
  - D.9 blinding inventory (V3Q19).
  - D.3 registered antecedent (V3Q22).
  - attribution of the 2026-08-16 review (carried v2 A1(ii)).
NOT HERE: commit hashes, hosts, GPU UUIDs, account names; any reinterpretation of a registered rule; a day count between identification and registration; "certified" outside a verbatim quotation (and flag it there).
V2 MATERIAL: paper/v2/sections/14_appendix_plan_provenance.md (D, E, F); paper/v2/BRIEF.md §7; paper/v2/ledger_proposals/W6.md.
DEPENDENCIES: every main-text file points here instead of giving a date.
-->

This appendix holds the record that the main text leaves out: when each part of the worked example was fixed, what the registration said, which GPU ran what, and how the seeds and archives were kept. Dates are as recorded in the project's own dated log and documents.

**D.1 Registration statement.** The registration is an internal, version-controlled record kept in the project's repository: the frozen design, the outcome framings, and a dated log of the decisions taken during the study. Its dates are self-reported. The code supplement carries the two registration documents, the frozen design and the outcome framings, with a hash manifest of every file it ships, so a reader can compare the quoted registration text with the shipped documents, check with the manifest that the archive arrived unaltered, and rerun the analysis scripts on the committed results. The dated log and the design review are not part of the supplement by default, so the quotations from the log (the estimand, the inert-share rule, the High readout, the 2000-update<!-- N:RES-15 --> subsample, the rulings before unblinding and the secondary specification) cannot be checked against the supplement unless log excerpts ship with it. What a reader cannot check is when the documents were written: that rests on the repository's history, which is not public. We checked that history. The frozen design was first committed on 2026-08-02 and last changed on 2026-08-13; the outcome framings were committed on 2026-08-13 and not changed afterwards; the first provenance file of the main training runs was committed on 2026-09-09, the confirmatory artifact's hash file on 2026-09-23, and the unblinding log on 2026-09-26<!-- N:X4-6 --> (dates in the committer's local time, UTC+3). These are commit dates in a private version-controlled repository, set by the committer's own clock, so they are self-reported, not externally timestamped. On a future project we would register in a public registry such as OSF.
<!-- OWNER-PENDING:V3Q16 full-history check DONE (fix round, RC2-12; dates stated above, no commit hash in the text); still open: content hashes of the registration documents in this appendix, and decision-log excerpts in the supplement (V3-V1); review RC2-12: after V3Q16, the shallow-clone sentence becomes either "The authors checked that the registration documents' commits predate the main training runs; the history itself is not public" or "The repository's history is not part of the supplement" -->

**D.2 Dated events.** Each row names the record that dates it.

| date | event | record |
|---|---|---|
| 2026-07-19 to 2026-07-30<!-- N:DX-401 --> | the environment constants are fixed (values in Appendix B): the severities and the death price, then Coupling A, the masking observation, Coupling B, and communication denial with its range | dated log; Appendix B |
| 2026-07-30<!-- N:V6-2 --> | communication denial is closed as inert at this scale (the log's words are "a certified negative") | dated log |
| 2026-08-02<!-- N:V6-3 --> | the design is registered; it keeps δ in θ\* "for registration fidelity at zero cost", gives ISO two δ-only components of six<!-- N:V6-3 -->, and leaves δ out of the secondary sweeps because it is inert | frozen design |
| 2026-08-02<!-- N:DES-12 --> | survival becomes a co-primary; the secondary sample size, Šidák m = 2 and the mediation void rule are fixed<!-- N:DX-402 --><!-- N:DX-414 --> | dated log; frozen design |
| 2026-08-03<!-- N:DX-402 --> | the registered seed count, 40, and the seed rule's cap, 60<!-- N:DES-1 -->, are fixed | dated log |
| 2026-08-10<!-- N:DES-5 --> | the main runs' launch floor study, on an RTX PRO 6000 | dated log |
| 2026-08-11<!-- N:METH-6 --> | the convergence check is retired, and the estimand is fixed at a matched budget of 1000<!-- N:DES-13 --> updates, with the rule for Γ(t) | dated log |
| 2026-08-13<!-- N:DES-12 --> | the outcome branches, a framing for each and the falsifier are registered | outcome framings |
| 2026-08-13<!-- N:V6-5 --> | the frozen plan is amended: the tests use the main runs' own seed dispersion | frozen design |
| 2026-08-14<!-- N:DX-36 --> | a partial re-measurement of floors on another rented GPU (provenance only) | the floor study's own record (results directory) |
| 2026-08-16<!-- N:V6-1 --> | a review of the registered design identifies the inert-share bias in ISO and its direction, before the main runs | design review; dated log |
| 2026-09-08<!-- N:DES-2 --> | floors re-measured on an RTX PRO 6000; the seed rule gives 46<!-- N:DES-2 --> | dated log |
| 2026-09-09 to 2026-09-22<!-- N:DES-12 --> | the main training runs, 252<!-- N:DX-30 --> runs | dated log; results report |
| 2026-09-18<!-- N:DES-15 --> | the bias, its direction, ISO-4 with its reading rule, the High readout and the 2000-update<!-- N:RES-15 --> subsample are registered, with 120 of 252<!-- N:DES-15 --> runs done | dated log |
| 2026-09-22<!-- N:DES-3 --> | the seed cap is raised to 72<!-- N:DES-3 -->, a recorded deviation | dated log |
| 2026-09-26<!-- N:DX-405 --> | the rulings before unblinding, (i)–(viii), and a fifth outcome cell, $A_c$<!-- N:DX-102 --> | dated log |
| 2026-09-26<!-- N:DES-12 --> | unblinding, later the same day | dated log; unblinding log |
| 2026-09-26<!-- N:DX-413 --> | the secondary specification is ratified, after unblinding for Γ and before the sweep is read; the same-GPU replicate Γ₄′ is proposed after Γ₄ is seen<!-- N:DES-15 --> | dated log |
| 2026-09-27<!-- N:DX-408 --> | every checkpoint archive's recorded hash is re-verified | results report |
| 2026-10-12<!-- N:X4-5 --> | the framing change (D.10) | dated log |

The design error of §6.2 runs through these rows. The design registered on 2026-08-02<!-- N:V6-3 --> kept a stressor it had already found inert, left it out of the sweeps for that reason, and kept it in ISO. One of its own questions for reviewers rested on the premise that "Neither protocol trains on δ = 1.0", which is false for both arms: ISO's δ-only components and both of JOINT's train at δ = 1<!-- N:X4-2 -->. The outcome branches registered on 2026-08-13<!-- N:DES-12 --> did no inert-share accounting. A review of the registered design found the bias on 2026-08-16<!-- N:V6-1 -->, noting that the confirmatory arm "applies a different rule to the same fact" as the sweeps. The main runs began without the correction. The correction was registered on 2026-09-18<!-- N:DES-15 -->, mid-run and before unblinding, on our attestation, recorded with the decision, that no outcome mean, per arm or across arms, had been computed or viewed. The confirmatory family did not change.
<!-- OWNER-PENDING:A1(ii) attribution of the 2026-08-16 review (default "a review of the registered design") -->

**D.3 The registered rules, quoted.** Emphasis is the record's own, one indented code line is set inline, and omissions are marked […]. A "§" inside a quotation refers to the record's own sections, "card" and "unit" are the record's words for a GPU, and S1–S6 are its labels for the secondary analyses.

*The estimand* (2026-08-11<!-- N:METH-6 -->):

> **Primary Γ = the confirmatory contrast at MATCHED BUDGET T = 1000<!-- N:DES-13 -->, all arms — registered as a fixed-budget claim.**
>
> **"At convergence" is explicitly NOT claimed anywhere.** The paper says **"at matched compute"** throughout, which is also the practitioner-relevant question. […]

*Budget robustness* (same ruling; restated for every branch on 2026-08-13<!-- N:DES-12 -->):

> The fixed-budget conclusion is reported as **budget-robust iff the sign of Γ is stable over the final half of training**. If the sign is still moving at T, **that instability IS the finding** and is reported as such.

> Mechanism: 11 retained checkpoints, updates 500–1000 at interval 50<!-- N:DES-13 -->, confirmatory arms only, **evaluated post-unblind**. Every branch above gains "— budget-robust" or "— sign unstable over the final half" as a suffix, and the suffix is not optional.

*The test's variance* (the frozen plan, amended 2026-08-13<!-- N:V6-5 -->):

> **The confirmatory tests and CIs are computed on the GRID'S OWN measured per-arm seed dispersion, not on the floors.** The floors are 8<!-- N:DX-403 --> identical reps at one seed; the grid averages over k distinct seeds, and those are different variances. The floors keep exactly two narrower roles: the **beat-reproducibility hurdle**, and a **design-stage power basis registered as an UPPER BOUND** (§5, superseded note, item 2). […]

*The outcome branches* (2026-08-13<!-- N:DES-12 -->). "Positive" and "null" mean rejection or non-rejection at θ\* in the confirmatory family, and "−" means rejection with negative sign (ruling (i) below). The registered table's venue column is omitted. $A_c$ was added on 2026-09-26<!-- N:DX-405 -->, before unblinding, for a cell the table lacked.

| branch | completion | survival | headline claim, as registered ($A_c$: its registered claims, summarized) |
|---|---|---|---|
| A | + | + | founding registration, verbatim [Γ(θ\*) > 0] |
| B | null | + | composition is paid in **agents**, not task return |
| C | null | null | the instrument, and what it excludes |
| D | − (either) | [− (either)] | not separable from the matched-budget asymmetry |
| $A_c$ | + | null | the founding claim on the founding primary; the survival null quoted as an exclusion; no asymmetry claim |

In row D, "− (either)" means rejection with negative sign on either co-primary; the registered table writes it once, under completion, and square brackets mark our additions.

<!-- OWNER-PENDING:V3Q22 registered antecedent (default: this note in Appendix D only, not in the main text) -->
The same document lists the environment and measurement items as standing on every outcome, "the larger part of the paper", which "does not depend on Γ at all". Three of its entries overclaim and are not repeated in this paper: a threshold value with no committed estimator behind it (§4.1 gives the committed estimators), communication denial "certified inert at swarm scale" (§4.4 gives the scoped phrase and its bars), and floors "ordered by curriculum difficulty", an untested hypothesis.

*The falsifier for branch B* (2026-08-13<!-- N:DES-12 -->):

> Branch B is claimable **only if** the completion contrast excludes an effect as large, in standardized units, as the observed survival effect:
>
> `|z_c| + z_α  <  |z_s|,     z = Γ / sd(Γ) per metric`
>
> with `sd(Γ)` the grid's own measured per-arm seed dispersion in the combined form and `z_α = 2.2365`<!-- N:DES-13 --> the two-sided Šidák critical value at m = 2. **If it fails, the result is branch C with an asymmetry the design could not resolve — not branch B.**

It passes: with $z_c$ and $z_s$ the two statistics, $\lvert z_c\rvert + z_\alpha = 3.855 < 4.433 = \lvert z_s\rvert$, and 4.040 < 4.673 in the registered 60-seed analysis<!-- N:RES-5 -->. Under Definition 2 the asymmetry is between a penalized channel and a rewarded one: the reward prices every death at $d_p = 0.5$<!-- N:ENV-1 --> whatever its cause and never reads the hazard. The result is branch B, completion null and survival positive. Branch A, the founding hypothesis, did not occur, and neither did $A_c$. Branch B's registered headline, "composition is paid in **agents**, not task return", no longer holds as worded, because the survival effect does not survive the inert-share correction (§6.3); the branch label stays B, because the rule below fixes it by Γ.

*The inert-share rule* (2026-09-18<!-- N:DES-15 -->):

> - Γ and Γ₄ are reported **side by side on every branch**, with B̂ and its CI.
> - If Γ rejects on a co-primary and **Γ₄'s CI on that co-primary includes 0 or its sign is opposite**, the paper states that the effect **does not survive the inert-share correction**, in the abstract-level summary and not only in an appendix. **The branch label does not change** — it is fixed by Γ — but branch A/B text may not describe the effect as a composition effect without that qualifier.
> - If Γ is null and Γ₄ is null, Γ₄ is quoted as a second exclusion bound.
> - If Γ is null and Γ₄ rejects **negative**, it is reported under branch D's framing (matched-budget asymmetry) as a secondary observation, never as a confirmatory finding.
> - **No magnitude threshold on B̂ is introduced**, now or later.

*The High readout* (same ruling):

> - **Γ_H null → an *a fortiori* exclusion**, and the only outcome this readout can establish: *"no gap larger than X at High even where JOINT trained on the evaluated configuration and ISO never saw a composed one."* Quoted as an exclusion with X from the grid's own seed dispersion, never as an absence. […]

The same entry states that the readout "is NOT a held-out test", that a positive $\Gamma_H$ is "NOT separable from in-distribution advantage", and that a negative one is "exploratory".

*The 2000-update<!-- N:RES-15 --> subsample* (same ruling):

> **What it may be cited for:** whether the differential drift measured at T = 1000 (review §6 item 1: 0.01209 per 100 updates<!-- N:DES-10 -->) visibly persists, closes or reverses. **What it may not be cited for:** any claim that Γ "holds" or "vanishes" at T = 2000.

*The mediation void rule* (the frozen plan, 2026-08-02<!-- N:DX-414 -->):

> **If realized dose does not vary with assigned p, the dose figure has no x-axis and is declared VOID** — registered now, not decided after seeing the first stage.

*The rulings before unblinding* (2026-09-26<!-- N:DX-405 -->):

| # | question | RULED |
|---|---|---|
| (i) | what "−" means in the branch table | **Rejection with negative sign** (\|z\| > z_α, Γ < 0). A negative estimate that does not reject is a null. Ratified as built. |
| (ii) | the cell (completion +, survival null), absent from the registered table | **REGISTERED NOW as branch A_c — the founding claim on the founding primary.** […] |
| (iii) | test statistic | **Normal z, z_α = 2.2365<!-- N:DES-13 -->**, as the frozen plan wrote; the t critical value is printed, not applied. Ratified as built. |
| (iv) | Γ(t) "sign stable" | **All 11<!-- N:DES-13 --> point estimates, t = 500 … 1000, share one nonzero sign**, per co-primary; t = 1000 is the grid's own eval. Consequence accepted in advance: on a null Γ, chance flips read UNSTABLE. Ratified as built. |
| (v) | Γ₄ sample and threshold | **JOINT k = 72 vs ISO-4 k = 20<!-- N:DES-3 --><!-- N:DES-13 -->**, SE `sqrt(s_J²/72 + s_4²/20)`, "rejects" and "CI includes 0" at z_α = 2.2365. (Γ null, Γ₄ rejects positive) stays UNREGISTERED. Ratified as built. |
| (vi) | Γ_H reading | **As (i), at z_α = 2.2365.** Ratified as built. |
| (vii) | primary k | **k = 72 stays primary**; the registered-ladder k = 60<!-- N:DES-1 --> prefix is reported beside it, UNDERPOWERED-flagged. |
| (viii) | re-evaluate the 144<!-- N:DES-3 --> T\* = 1000 checkpoints on the post-unblind card | **YES.** […] |

In (viii), "the post-unblind card" is GPU 3 (D.6).

*The secondary specification* (2026-09-26, after unblinding and before the sweep was read<!-- N:DX-413 -->):

> (S1) PAVA + OLS slope CI; (S2) single-hinge breakpoint, UNDERPOWERED iff the CI spans {0.125 … 0.375}<!-- N:DX-28 -->; (S3) plane fit, bound = 95 % CI of 0.5·γ_n; (S4) training co-activity over updates 1…1000, VOID iff the first-stage CI contains 0; (S5) the same-card replicate is ADDED, beside Γ₄, unable to change its qualifier; (S6) 95 % intervals, Γ₄′ at z_α. […]

The omitted words name the code version, which would identify the repository.

**D.4 The seed rule.** The design registered k = 40<!-- N:DES-1 --> seeds per confirmatory arm and a rule, capped at 60<!-- N:DES-1 -->, that recomputes k from floors re-measured on the GPU that would run the main training runs. On the launch floor study of 2026-08-10<!-- N:DES-5 --> the design-stage detection limit at k = 40 was 1.55 completion and 0.95 survival points<!-- N:DES-5 -->. The rule gave 46<!-- N:DES-2 --> on the RTX PRO 6000 floors of 2026-09-08<!-- N:DES-2 -->, and 72<!-- N:DES-3 --> on the RTX 5090 that ran the confirmatory runs. The rule's registered action at the cap was "PROCEED at k = 60 and DEGRADE HONESTLY, never chase". On 2026-09-22<!-- N:DES-3 --> the cap was raised to 72 instead, before unblinding and with no outcome seen; this is a deviation from a registered rule, recorded as one. Seeds 1–60 are a prefix of the 72, so the registered 60-seed analysis is reported beside the primary one (Appendix E). On the RTX 5090's floors, design-stage completion power at a 3-point effect was 72.2 % at k = 60 and 80.4 % at k = 72<!-- N:DES-4 -->, an upper bound because floors measure rerun noise alone; realized power was 60.2 % and 71.6 %<!-- N:DES-6 -->.

**D.5 Bias (b).** The registered caveat on differential drift is the difference between JOINT's and ISO's completion drift over the last 100 of 1000<!-- N:DES-13 --> training updates<!-- N:DES-10 -->, quoted as a local sensitivity estimate and never as a bound. Four floor studies read it at 1000 updates<!-- N:DES-10 --><!-- N:V6-4 -->: +0.0242<!-- N:V6-4 --> per 100 updates on the confirmatory arms' earlier floor study, +0.01209<!-- N:DES-10 --> on the launch floor study and +0.0179<!-- N:DES-10 --> on the 2026-09-08<!-- N:DES-2 --> re-measurement, all three on an RTX PRO 6000, but −0.0083<!-- N:DES-10 --> on GPU 1. Bias (b) therefore reverses sign on the grid GPU, and no direction is claimed. In the 2000-update<!-- N:RES-15 --> subsample, the differential training-log slopes over updates 500–1000 are +0.00247 for completion and +0.00718 for survival per 100 updates<!-- N:DES-11 -->, a different estimator from the floor studies'.

**D.6 GPU blocks.** The runs analysed here used one GPU model, the RTX 5090, on three rented units<!-- N:DX-5 -->. GPU 1 ran Γ: all 72 seeds of ISO and JOINT<!-- N:HW-4 -->, of which 76 runs were executed there and seeds 13–46 were copied from the main runs<!-- N:DX-30 -->. GPU 1 also ran every analysed secondary run, so Γ₄′ is a same-GPU contrast. GPU 2 trained ISO-4 and the 2000-update<!-- N:RES-15 --> subsample, so Γ₄ and B̂ compare runs on two GPUs, and GPU 3 ran the evaluations after unblinding<!-- N:HW-4 -->. Seeds 1–12 of all ten arms first ran on an RTX PRO 6000<!-- N:DX-30 -->; those runs were superseded, enter only a descriptive diagnostic of the GPU effect, and the secondary arms' seeds 1–12 were re-run on GPU 1 (96 runs<!-- N:DX-30 -->).

**D.7 Study codes.** The project's internal codes appear on some figures and in the supplement. Their plain names:

| code | plain name |
|---|---|
| M3.0 | the re-test of Definition 4's prediction that outcomes vary most at Medium |
| M3.3 | the check of Proposition 3 against its closed form |
| M3.4 | the Coupling-A calibration under random policies |
| M3.5 (printed m35) | the Coupling-A calibration grid |
| M4.2 | the check of Theorem 1 in the corridor toy (printed E2C) |
| M4.4 (printed m44) | the Coupling-B calibration grid |
| E1.1 | the severity response of collapse-seeded ignitions near agents |
| M5.1e | the four-run<!-- N:DX-403 --> Medium floor study on an RTX 5090 |
| M5.2 | the check of Remark 2′ in the two-agent courier toy (printed E2C²) |
| M5.3, M5.3b | the content ablation at Medium, and the same ablation at High |
| M5.5 | the denial study |
| M6.0 | the refactor of the environment code |
| M6.2, M6.2b | the confirmatory arms' floor studies at 500 and 1000<!-- N:DX-34 --> updates |
| G1.2 | the floor-study protocol of the main runs: the launch floor study (2026-08-10<!-- N:DES-5 -->) and its re-measurements of 2026-09-08<!-- N:DES-2 --> and on the RTX 5090 |
| G1.3 | the main training runs |

**D.8 Seeds and archives.** All arms share seed integers, and seed 0, the floor seed, never enters the main runs<!-- N:DX-416 -->. Runs are ordered seed-major and chunks end on seed boundaries, so an interruption leaves a smaller balanced design and both arms of a seed share one GPU. Every checkpoint archive's recorded sha256 matched on re-verification on 2026-09-27<!-- N:DX-408 -->, 615 of 615<!-- N:DX-408 -->; the hashes ship with the supplement's result directories, not here.
<!-- OWNER-PENDING:F1 archive count "615 of 615" against the 636 that the same report's archive table sums to (DISPOSITIONS §5 F1 carries; review RN2-1); the count is kept until the owner reconciles the record -->

**D.9 Blinding.** The runner of the main training runs computes no cross-arm quantity, and a unit test asserts it. Each analysis stage ran once: the unblinding script refuses an unflagged artifact or a modified code version, later analysis scripts refuse to run before its log exists, and each log records one run of its stage<!-- N:DX-411 -->.
<!-- OWNER-PENDING:V3Q19 the inventory of outcome-derived quantities visible when k = 72 and ISO-4 were decided is owner-attested only; nothing is stated beyond one look per stage -->

**D.10 The framing change.** On 2026-10-12<!-- N:X4-5 -->, after the result was known, we moved the paper's emphasis to the environment, and the pre-registered test became its worked example (§6.1). No constant, registration or registered reading changed. The registered outcome branches and their framings, quoted in D.3, remain the record of the original plan.
