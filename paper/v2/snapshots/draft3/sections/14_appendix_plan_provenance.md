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

**7. The 2000-update subsample** (same ruling):

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

The grid was 252 runs<!-- N:DX-30 --> from 2026-09-09 to 2026-09-22<!-- N:DES-12 -->. Seeds 1–12 of all ten arms (ISO, JOINT and eight secondary arms) ran on an RTX PRO 6000, then seeds 13–20 of all ten arms and 21–46 of ISO and JOINT on GPU 1<!-- N:DX-30 -->. The confirmatory artifact holds all 72 seeds of ISO and JOINT on GPU 1<!-- N:HW-4 -->: 76 runs executed there and seeds 13–46 copied from the grid<!-- N:DX-30 -->. The superseded RTX PRO 6000 seeds enter only a descriptive diagnostic of the GPU effect. Seeds 1–12 of the secondary arms were re-run on GPU 1 (96 runs<!-- N:DX-30 -->), so every analysed secondary run is on GPU 1 and Γ₄′ is a same-GPU contrast. ISO-4 and the 2000-update subsample trained on GPU 2, so Γ₄ and B̂ are across GPUs, and the post-unblind evaluations ran on GPU 3<!-- N:HW-4 -->.

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
  <iframe src="{{ 'assets/html/submission/explorer_thetastar_iso_s1_T1000_ep0.html' | relative_url }}" width="100%" height="700" style="border:none" title="Episode explorer, ISO policy, training seed 1" loading="lazy"></iframe>
  <figcaption><strong>Figure I1.</strong> One episode of the ISO policy at θ&#42;. The map is environment state, the smoke field ρ included. Selecting an agent shows its observation as produced (labelled obs v3: the masking observation, §6.1), the true cells, and the probability τ that each was seen. It cannot compare training protocols. <span class="figure-note">Status: illustrative · grades nothing · Interact: play, step, click an agent.</span></figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/explorer_thetastar_iso_s1_T1000_ep0_static.png" class="img-fluid" alt="Maps of one ISO-policy episode at its start, middle and end, with one agent's observation, the true state of the same cells, and the probability each cell was seen" caption="Static companion of Figure I1 for the printed PDF." %}
</div>

Figure I2 shows the JOINT policy's episode under the same rule. One episode of one seed cannot carry a contrast that §9.2 measures over 72 seeds per arm and 512 evaluation episodes<!-- N:DES-3 --><!-- N:DES-13 -->.

<figure class="l-page">
  <iframe src="{{ 'assets/html/submission/explorer_thetastar_joint_s1_T1000_ep0.html' | relative_url }}" width="100%" height="700" style="border:none" title="Episode explorer, JOINT policy, training seed 1" loading="lazy"></iframe>
  <figcaption><strong>Figure I2.</strong> One episode of the JOINT policy at θ&#42;, with the layers and panels of Figure I1; only the observation panel shows what the selected agent perceives. It cannot compare training protocols. <span class="figure-note">Status: illustrative · grades nothing · Interact: as Figure I1.</span></figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/explorer_thetastar_joint_s1_T1000_ep0_static.png" class="img-fluid" alt="Maps of one JOINT-policy episode at its start, middle and end, with one agent's observation, the true state of the same cells, and the probability each cell was seen" caption="Static companion of Figure I2 for the printed PDF." %}
</div>
