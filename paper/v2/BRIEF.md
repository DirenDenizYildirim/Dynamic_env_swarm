# BRIEF — Paper v2, for the step-4 writers (W1–W6)

Builder B1, step 3 of Paper v2, 2026-10-11, under the decision log's
**PAPER V2** ruling (`docs/decision_log.md:6036`) and its amendment (the v2
process, `:6096`). This brief carries over the demonstration's
`paper/demo_beyond/BRIEF.md` (the "demo brief") with its facts re-verified
(§0), its demonstration-only rules removed, and the v2 additions the
owner's prompt asks for: the roles (§1), the fix list with an owner per item
(§3), the plain-term glossary (§5.2), the disclosure-footnote rule (§12) and
the provenance rule (§13).

**How to use it.** Read this file, then your stubs (`sections/NN_*.md`;
each carries its own `STUB-SPEC` with the facts, figures and listings it
needs), then your section's row in `STRUCTURE.md` and the `FINDINGS.md`
rows your stub names. You should not need to reopen the record; where you
do, the source is named. The per-section fact tables that the demo brief
held in its §D now live in the stubs. Abbreviations: `log` =
`docs/decision_log.md`; `TF` = `docs/theory_foundations.md`; `R/` =
`che/bench/results/`; `P6/` = `R/phase6/`; `RWV` =
`paper/related_work_verification.md`; "demo" = `paper/demo_beyond/`.

---

## 0. How this brief was re-verified (2026-10-11, this session)

| what | how | result |
|---|---|---|
| every ledger ID this brief, `STRUCTURE.md`, `FINDINGS.md` and the stubs cite (ranges expanded) | script (scratch): each ID must resolve in `paper/numbers_ledger.md` or `paper/v2/ledger_supplement.md`; `V6-*` are pre-assigned for W6 (§7) | ran this session: every ID resolves |
| values quoted in this brief and in the stubs | compared by hand with the row text of the ledger or the supplement (the record of numbers) | as written |
| the abstract-level result set (RES-1, RES-2, RES-4, RES-5, RES-6, RES-7, RES-11–RES-14, RES-15, DES-6, HW-1–HW-3, DX-21) | re-read at source: `P6/unblind/report.md:5, :9-25, :31-32, :38-41`; `P6/post_unblind_analysis/post_gamma4_t2000.md:1-36`; `P6/post_unblind_analysis/post_evalfloor_gamma_t_high.md:9, :20-56, :62-66, :76-88` | match |
| the F3 timeline (§7) | re-read: log:1065-1110 (M5.3 CLOSURE), :3551-3556, :3636-3682 (VENUE RULING, proposal 0), :3840-3846 (pre-grid), :3902-4030 (§7 PROPOSALS RULING); `docs/venue_review_2026-08-16.md:1-26, :108-165`; `phase6_design_v2.md:1-40, :60-87, :125-133, :425-436`; `comms_lock.md:1-8`; `che/configs/p6_iso.yaml:1-9, :32, :41-46` | match; it confirms the orchestrator's finding O1 |
| rulings cited by name | every heading line of §4 located by grep this session; bodies read this session: M5.3 CLOSURE (:1065-1110), PHASE-5 CLOSE (:1225-1240), VENUE RULING (:3551-3556, :3636-3682), §7 PROPOSALS RULING (:3902-4030), ENDPOINT CONFOUND (:4549-4575), LADDER BRANCH C (:4616-4626), UNBLIND RESULT (:4978-5004), SECONDARY RESULT (:5070-5110), POST-UNBLIND STAGE RESULT (:5161-5191), SUBMISSION FORMAT (:5192-5260), DEF. 2 WORDING (:5287-5345), WRITING ROLES' OWED item (:5474-5490), TITLE AND TERMINOLOGY (:5583-5622), ABSTRACT, DESCRIPTION, §1 INTRODUCTION, READS RULING (:5655-5780), FIGURE BATCH RULINGS (:5888-5960), OPENING (:5961-5988), DEMONSTRATION DRAFT and PAPER V2 (:5990-6112), PRE-UNBLIND RULINGS (:4913-4932), T\* RULING (:2940-2996, in part), and log:3138-3158 | match. Not re-read beyond the heading this session (carried from the demo brief and the plans): CITATION REPOSITIONING, REPO VISIBILITY, FIGURES, FIGURES FIRST |
| registered strings | log:4987-4994 (UNBLIND RESULT), :4016-4029 (ISO-4 reading rule), :5165-5180 (POST-UNBLIND STAGE RESULT); `paper/branch_B.md:172-192, :223-235` | match |
| code and report facts used in §3, §9.1 and §11 | re-read: `che/env/env.py:159-166, :239-245, :359-362, :394-404, :444-447`; `che/env/hazard.py:8-16, :67-79`; `che/eval/harness.py:42-46`; `che/tests/test_reward_independence.py:6-15`; `che/tests/test_lethality.py:143-148`; `che/tests/test_p6_grid.py:153-172, :205-214`; `R/phase4/phase4_report.md:635-640`; `R/e1/e11_report.md:109-124` | match. `test_p6_grid.py:156-157`'s docstring says "any induced cross-arm covariance"; the registered argument (log:3143-3146) covers positive covariance only (FINDINGS P3-N14) |
| listings | the six ranges of §16 pasted into the stubs by script from the committed files, then compared line by line by a second script | ran this session: 6 of 6 byte-identical after the header line |
| the kit facts in §14 | `paper/beyond_pdf/KIT_NOTES.md` §S1.4–S1.9 (read); `paper/demo_beyond/KIT_BUILD.md` (read); the review's kit-source findings (`paper/v2/review_of_demo.md` M1–M3, N1) | carried; **UNVERIFIED** in a kit build until B2's step-3/4 build runs |
| `RWV` line numbers | B2 is editing `RWV` in parallel (M2). Line numbers below are those of the committed copy (`git show HEAD:paper/related_work_verification.md`) | may shift by B2's edit; the quoted content is what binds |

**Not re-verified this session (marked UNVERIFIED where used):** the
ledger rows' own source lines beyond the set above (the ledger and the
supplement record their verification; the step-2 review sampled 26 tags
and all §1/§9 numbers against source with no mismatch,
`paper/v2/review_of_demo.md` "Checks that came back clean"); the demo
brief's citation "permitted uses" beyond what `RWV` Part 3 and the owner's
§2 (`paper/finale.md:180-370`) say.

---

## 1. Roles (PAPER V2) and how step 4 runs

- **Builders draft; the owner checks every word.** Builder subagents draft
  the paper, title, abstract and `description` included, from the
  demonstration as a scaffold. The owner checks every word, approves
  section by section and is responsible for the result. This supersedes
  *WRITING ROLES* for v2 (PAPER V2 item 1, log:6047-6052).
- **Nothing enters `paper/finale.md` or the submission** until the owner
  has approved it. Nothing is committed unless the owner says so in this
  session. All work is under `paper/v2/`; `paper/demo_beyond/` stays as it
  is.
- **TMLR's LLM policy, as read 2026-10-11** (PAPER V2 item 2, log:6053-6064):
  LLMs may be used as general-purpose assistive tools; authors are fully
  responsible for every word and LLMs cannot be authors; the tool's use is
  mentioned "as a footnote on the first page"; the ideas, claims and
  results are expected to be "human-sourced"; submissions that appear
  largely LLM-generated "will be closely examined". Hence: every claim
  traces to the record, and every sentence has a provenance row (§13).
- **Your files** (`paper/v2/INTERFACE.md`): your `sections/NN_*.md` and any
  `sections/alt/NN_*.<variant>.md` your stub names; `provenance/NN_*.md`
  for each; `ledger_proposals/W<n>.md` for new rows. W1 also owns `title`
  and `description` in `front_matter.yaml`. Edit nothing else: not another
  writer's file, not this brief, not `STRUCTURE.md`, not `FINDINGS.md`
  (review lanes append to it), not the ledger, the supplement, `RWV`, the
  bibliography, `src/`, `CLAUDE.md`, `TF`, configs or code.
- **Step 4 passes:** (1) writers, in parallel; (2) reviewers in three lanes
  (claims, numbers, mechanics) writing to `paper/v2/review/`; (3) writers fix
  their own files, reviewers re-check changed lines, outcomes go to
  `paper/v2/REVIEW.md`; (4) the real-kit build, all checks green. Step 4.5:
  the owner and one blind agent review the built paper.
- **Finding classes (the orchestrator's policy; `FINDINGS.md` gives every
  row):**
  - **A, owner-directed** (on the fix list): apply as the owner directed.
  - **B, standing rule** (not on the list, but the demo or owner text breaks
    a standing written rule): apply, and the provenance row says "class B,
    finding <ID>" with the original wording, so the owner can revert.
  - **C, needs a ruling or an owner choice:** do **not** apply. Keep the
    default `FINDINGS.md` names; where it says so, draft the alternate in
    `sections/alt/`.
  - **A finding you make while writing:** do not apply it unless it is
    class B. Record it in your provenance file's "Findings" section and in
    your hand-back (§18), with location, evidence and proposed direction.

---

## 2. Rules that bind every agent (verbatim from `paper_v2_prompt.md:66-91`)

- **Numbers:** a number comes only from the ledger or the supplement, tagged
  `<!-- N:ID -->`. A number with no row gets a VERIFIED row first, read from
  a committed file at file:line, or it is cut. Never from memory, the spine
  or `branch_B.md` alone, which lag the ledger.
- **Registered strings stay verbatim** where the registration requires them,
  even while §9's jargon is cut: "does not survive the inert-share
  correction"; "sign unstable over the final half" on both co-primaries.
  Completion null is an exclusion with its bound. Matched compute, never
  convergence. B̂ gets no verdict. Bias (b) reverses sign on the grid card.
- **Citations:** keys from `submission.bib` only. A new citation is verified
  through `related_work_verification.md` first; never write a `.bib` entry
  from memory.
- **Double-blind:** no repository URL, no names, no account-resolving hashes,
  no absolute paths. The disclosure footnote names the tool, not the author.
- **No new runs and no GPU spend.** No training, no test-suite runs and no
  project code. The only things you run are the scaffold's build and the
  real kit build (steps 3 and 4).
- **Do not edit** `CLAUDE.md`, `docs/theory_foundations.md`, the canonical
  ledger, the configs or any code. Do not edit `paper/finale.md` until the
  owner approves a section. Where the record itself is wrong (OWNER ITEMS),
  report it.
- **Commit nothing unless the owner says so** in this session. Work goes in
  a new folder, `paper/v2/`, with the scaffold's layout. `paper/demo_beyond/`
  stays as it is, for comparison.

For v2, "`submission.bib`" is `paper/v2/assets/bibliography/submission.bib`
(B2's verbatim copy of the corrected `RWV` entries, INTERFACE layout).

---

## 3. The owner's fix list, with an owner for each item

The fix list is `paper_v2_prompt.md:93-221`; read it there verbatim.
`FINDINGS.md` gives each item's class, v2 default, alternate and owner
question. "Owner" below is who applies it in v2.

| item | what | applied by | notes |
|---|---|---|---|
| **M1** | prose pipes become one-row tables | **B2** (source scan for one pipe; kit table count = source count); **W5** (§11 states the evaluation figure once, without a pipe); **W6** (§9.2 points to §11; no pipe anywhere) | the trigger is one unescaped pipe, not two (review M1; kramdown 2.4.0) |
| **M2** | raw LaTeX in the reference list; resolve every `d-cite` and cross-reference | **B2** (Unicode at source in `RWV`, re-copy the `.bib`, check every rendered entry and hover card); writers keep cross-references plain text (§14) | |
| **M3** | empty BibTeX year | **B2** (`date` placeholder); **owner decision** (the date, `submitted_date`: Q2) | the year field holds a full date in the kit's format (review M3) |
| **M4** | HTML comments in the built page | **B2** (stripped staging copy with 0 `<!--` and 0 `%` lines); **owner decision** (OpenReview upload: Q1) | keep tags in the repository copy |
| **C1** | Corollary 1(3) and (4) | **W3** (§4.1; alternate without (4)); **W4** (Prop. 3 loses the 43/18 rate); **W6** (App. A's Prop. 3 proof); **B2** (enters `garet2004chemical` through `RWV`) | drop (3); (4) at the verified level by default (Q4g) |
| **C2** | soften Remark 1 | **W3** (§3.1); **W2** (§1's clause) | also drop the "(δ > 0)" reduction clause (P3-N2) |
| **C3** | Proposition 4 is an upper bound | **W6** (§9.1, App. A); **W2** (§1 clause); **W5** (§10 line) | no display with the unverified constant; no ISO-vs-JOINT slack contrast (N6, P3-N7; Q4i) |
| **F1** | retitle; 3–5 candidates | **W1** (`front_matter.yaml` title; candidates in `provenance/00_abstract.md`); **owner decision** (Q3) | `STRUCTURE.md` §3 lists the reconciled candidates |
| **F2** | abstract leads with the plain result | **W1**; `description` re-checked against the new opening (**W1**, Q4d) | spine in `STRUCTURE.md` §4 |
| **F3** | own the δ confound as a design error | **W6** (§9.1, full account); **W2** (§1, two sentences); **W1** (abstract clause); **W5** (§10 bullet); **W4** (§7 last paragraph, neutral pointer) | record facts in §7 below; the fix list's "found … mid-grid" is corrected (O1) |
| **F4** | advice separated from "therefore" | **W6** (§9.3, the one labelled recommendation); **W1** (abstract: one labelled sentence by default, alternate without); **W2** (§1: no imperative, pointer); **W5** (§10: scope pointer) | a recommendation is not a contribution |
| **F5** | cut internal jargon | **W6** (§9, App.); **W5** (§8, §10, §11); every writer (§5.2 glossary); figure labels glossed in captions | "no-coupling sweep arm" misdescribes the arm: use §5.2's term (P3-N18) |
| **OWNER ITEM 1** | "as predicted before measurement" | **W1** (abstract), **W2** (§1 contribution 2), **W4** (§5.3) | DX-9 note gives the corrected timing |
| **OWNER ITEM 2** | Prop. 1's finiteness, "finite Dec-POMDP" | **W3** (§3.1), **W2** (§1), **W6** (App. A, proof once) | record items TF:151-153, :62-63 reported |
| **OWNER ITEM 3** | "every arm is perturbed throughout" | **W2** (§2) | accurate wording departs from READS RULING item 2: flagged, Q4a |
| **OWNER ITEM 4** | "about seven percent" | **W2** (§2), **W4** (§5.1 home of the number) | same flag, Q4a |
| **OWNER ITEMS 5–6** | record fixes (CLAUDE.md:344 and log:1194; `phase4_report.md:366, :394-395`) | **owner decision** (Q4l); writers never repeat either | report only |
| **KIT_BUILD 1** | reference-list LaTeX | = M2, **B2** | |
| **KIT_BUILD 2** | long code lines cut on screen | **B2** (listing CSS); **W3**, **W4** (the shortened ranges of §16) | Listing 1 cannot be shortened (P2 §4) |
| **KIT_BUILD 3** | 869 comments | = M4, **B2** | |
| **KIT_BUILD 4** | kit navbar, footer, sidebar | **B2** (screenshots at 1280 and 1440 px); no text change | |
| **Length** | tighter; no result restated | **every writer**: budgets and the one-home map in `STRUCTURE.md` §6–§7 | |
| **"Stuff like this"** | new findings | reported in `FINDINGS.md`; applied only when class B | |

---

## 4. Binding rulings, by entry name (heading line in `docs/decision_log.md`)

| entry | what it forces in your text |
|---|---|
| UNBLIND RESULT (:4978) | branch B; survival Γ "does not survive the inert-share correction", stated in the abstract-level summary; the branch label stays B; never "composition effect" without the qualifier; completion: Γ₄ is a second exclusion bound, X₄ = 0.0488 (RES-6); Γ₄ and B̂ are cross-unit (:4995-4997) |
| SECONDARY RESULT (:5070) | non-verdict-bearing; 95 % intervals, many, none family-corrected; γ_p "does **not** extrapolate … Reported, not resolved"; mediation VOID; the counter is co-active only in all-on configurations |
| POST-UNBLIND STAGE RESULT (:5161) | "sign unstable over the final half" on both co-primaries; the survival gap opens late; the completion lean must be stated; High readout = a-fortiori exclusions; evaluations reproduce bit-for-bit |
| T\* RULING (:2940) | "at matched compute" throughout; "at convergence" nowhere; Γ(t) is required robustness evidence |
| §7 PROPOSALS RULING (:3902) | the inert-share bias registered with its direction (inflates Γ); ISO-4 a sensitivity arm outside the family, k = 20; the reading rule (:4016-4029, verbatim in App. D); T = 2000 descriptive; High readout eval-only; mid-grid, 120 of 252 runs, owner attestation (:3907-3909) |
| PRE-UNBLIND RULINGS (:4913) | normal z at z_α = 2.2365 (t printed, not applied); the sign rule (all 11 estimates share one sign); k = 72 primary, k = 60 beside it UNDERPOWERED; branch A_c registered |
| LADDER BRANCH C (:4616) | k = 72 is a recorded deviation from a registered rule, pre-unblind, no outcome seen |
| ENDPOINT CONFOUND (:4549) | JOINT sees each coupling 3× as often as ISO; DBCA describes the sweep, never the ISO/JOINT endpoints |
| M5.3 CLOSURE RULING (:1065); PHASE-5 CLOSE RULINGS (:1211) | the comms axis closed 2026-07-30 (the record says "certified": never echo it); demand-side reading (:1074-1081); clean-zero conditions not fully met because d_p prices deaths (:1083-1088); a < 3-point cap on a frozen encoder does not strictly bound a trained one (:1102-1104); "gradient-shaped messaging remains untested" (:1106-1107) |
| DEF. 2 WORDING RULING (:5287) | hazard-blind reward that prices deaths cause-blind (d_p = 0.5); "no shaping term" and "solely" struck; the d_p ablation reported with its scope, never re-run |
| SUBMISSION FORMAT RULING (:5192) | constraints 1–4 (:5242-5252): double-blind, self-contained figures; animations illustrate and never grade; interactive quantities obey static rules; the printed PDF stands alone |
| WRITING ROLES (:5429) | superseded for v2 by PAPER V2 item 1; its OWED comment-stripping item (:5474-5486) is B2's M4 |
| REPO VISIBILITY (:5552) | the repository goes private before upload |
| TITLE AND TERMINOLOGY RULINGS (:5583) | the terms of §5.1 stand; the title is reopened (PAPER V2 item 3) |
| ABSTRACT (:5655) | reopened (PAPER V2 item 3). Item 2: a body section with no heading. Item 3: the environment named in full is the owner's double-blind call (Q4c). Item 4: venue limit 5,000 characters; the owner's text was 2,424 |
| DESCRIPTION (:5680) | one line; no `"`, no backslash, no `: `, no number (so no tag); it restates the abstract's opening (item 3), so it changes with a new opening (F2; Q4d) |
| §1 INTRODUCTION (:5700) | item 3: §9.2 reports γ_n and where the fit fails, and §1 points there; §1's safe-RL sentence may cite `garcia2015safe` |
| READS RULING (:5732) | characterize cited works only as `RWV` Part 3 records; item 2: two §2 phrases "left as written" (the v2 change is flagged, Q4a); item 4: §10 says no adaptive curriculum is evaluated; §7 presents Remark 2′ as a refinement of Pynadath & Tambe (their Theorem 4, Theorems 5–6, Table 2) |
| CITATION REPOSITIONING RULING (:5111) | who is cited for what (§15) |
| FIGURES (:5781); FIGURES FIRST (:5841); FIGURE BATCH RULINGS (:5888) | figures from committed sources only; A1: Γ never shown without Γ₄ near the opening; A3: ISO/JOINT episodes only in the appendix, separately; A6: no explorer deep links; B7: B̂ no verdict; B9: spreads from other runs are "reference scale (cross-artifact)", never "floor"; B10: the simplex shows the γ_n pair that fits and the γ_p pair that misses |
| OPENING AND §1 REOPENED (:5961) | the random-policy explorer directly under the abstract (item 2; hero alternate is Q8); §1 carried by the composer and the compact ladder (item 3); §2's position decided at the final pass (item 4; Q10) |
| DEMONSTRATION DRAFT (:5990) | governed the demo only; its line-1 "builder-written" label does **not** carry into v2 |
| PAPER V2 (:6036) and amendment (:6096) | §1 above |
| `CLAUDE.md` standing rules | bars come with floors (per metric, per hardware, per artifact); contrasts graded on the contrast's SE; power = the 80 %-power MDE at the family-corrected α; instruments state what they are blind to; measuring is not grading |

---

## 5. Terminology, the plain-term glossary (F5), and the strings that stay

### 5.1 Ruled terms (TITLE AND TERMINOLOGY RULINGS; D1)

| use | never | note |
|---|---|---|
| **stressor** = one of {Coupling A, Coupling B, comms denial} | "the fire is a stressor" | the fire burns in every episode (D1) |
| **ambient hazard** (Def. 2) for the fire | "passive", "ambient survival stressor" | non-adversarial, not instrumented, no energy claim |
| **environment configuration** θ = (β, κ_A, κ_B, δ) | "stressor configuration" | θ includes β |
| **fire-only** episode | "hazard-free", "empty of hazard" | δ-only episodes are fire-only (β 0.43 / 0.70) |
| **co-occurring** stressors | "co-active" outside the counter | "co-active" names the counter only |
| **multi-agent**, "team", "agents" | "swarm" as a claim | the task needs no coordination |
| **at matched compute** | "at convergence", "converged gap", "budget-robust" | T\* ruling |
| **inert under a frozen random-projection encoder at this scale** | "certified inert" (the record and `p6_iso.yaml:8` say it: never echo) | full phrase in §7, the abstract and §10 item 5; elsewhere "inert (§7)" |
| **active share** (share of training episodes with at least one behaviourally active stressor) | "exposure" unqualified | DES-14 scope note |
| ISO, ISO-4, JOINT; Γ, Γ₄, Γ₄′, B̂, Γ_H, Γ(t) | new arm or contrast names | plain names at first use (§5.2) |
| single-policy IPPO, one policy per training seed | "PBT", "population-based" for any reported run | ENV-11; O-1 (Q4j) |
| **pre-registered** for the JOINT-vs-ISO test registered 2026-08-13 only | "pre-registered correction" | the correction was "registered before unblinding" (DES-15) |

### 5.2 Plain-term glossary (F5)

One plain replacement per term, **defined once** (where the "defined in"
column says), then used throughout. Built from P3 §4's table and the
review's counts (`review_of_demo.md` F5). "Figures that print it" are
frozen this phase (no rebuild, P2 §0): their captions carry the gloss
once, in the form "(labelled X on the figure)".

| internal term | plain replacement (defined once) | defined in | figures that print it | note |
|---|---|---|---|---|
| card, grid card, same-card, single-card | **GPU**: "the GPU that ran the grid", "on the same GPU", "on one GPU" | §9.1 | Figs 6, 10, 12 ("card", "single-card curve") | §8 and App. C too |
| unit 1 / 2 / 3, cross-unit | **GPU 1, GPU 2, GPU 3**: three rented RTX 5090s (DX-5, HW-4); "across GPUs" | §9.1 | Figs 3, 11 ("unit 1", "cross-unit") | caption gloss: "unit n is GPU n" |
| ladder (the seed rule) | **the registered seed rule** (DES-1–DES-3) | §9.1 | — | the k = 60 "prefix" is "the registered k = 60 analysis (seeds 1–60)" |
| ladder (the figure), rung | **Figure 11, the registered readings in order**; a rung is **a step** of that order | §9.2 | Figs 3, 11 ("rung" buttons; "full ladder: §9.2") | |
| `sweep_c50_p000` | **the p = 0 sweep arm, which trains on ISO-4's mixture on JOINT's GPU** (not "the no-coupling sweep arm", which misdescribes it: P3-N18; DES-9; log:5043-5047) | §9.1 | Figs 11, 13 | code names only in App. H's table, as labels matching Figure 13 |
| `sweep_c50_p125` … `p500`; `ident_c40_*` | **the sweep arm at co-occurrence p**; **the identification arm at p** | §9.1 | Fig 13 | |
| re-floor | **re-measured reproducibility floor** | §8.1 | — | |
| S1–S6 | name the analysis: the sweep slope, the change-point test, **the plane fit**, the mediation test, **the same-GPU replicate**, the interval convention | §9.2 | — | verbatim only inside App. D's quotation |
| floor-basis sd(Γ) | **the floor-based standard error of Γ** (DX-21) | §8.4 | Figs 10, 11 ("floor basis", "floor-basis sd(Γ)") | |
| beat-reproducibility (hurdle) | **the check that an effect exceeds rerun noise** (HW-1) | §8.4 | Fig 10 ("beat") | |
| Γ₄ | at first use: **the corrected gap, JOINT − ISO-4**; then Γ₄ | §1 and §9.2 | Figs 3, 11 | |
| Γ₄′ | at first use: **the same-GPU replicate of the correction: JOINT minus the p = 0 sweep arm, which trains on ISO-4's mixture on JOINT's GPU** (RES-8); then Γ₄′ | §9.2 | Figs 11, 13 | |
| B̂ | **ISO-4 − ISO, reported without a test** | §9.2 | Figs 11, 13 | never a verdict word |
| Γ_H | **the High-severity readout** | §9.2 | — | |
| M3.0, M3.3, M3.4, M3.5, M4.2, M4.4, M5.1e, M5.2, M5.3, M5.3b, M5.5, M6.0, M6.2, M6.2b, G1.2 | **name the study** ("the Coupling-B calibration grid", "a four-run floor study at Medium on an RTX 5090") | first use in each section | Fig 10 ("M5.1e", "M6.0") | codes only in App. C's study column, with a key |
| m44, m35 | **the Coupling-B calibration grid**, **the Coupling-A calibration grid** | §5.3 | Fig 6 ("m44", "m35") | caption gloss |
| rep set, reps, identical-run set | **identical reruns** | §8.1 | — | |
| k_req | **the seed count the rule required** | §9.1 | — | |
| launch batch | **the grid's launch floor study (2026-08-10)** (CORRECTED by the orchestrator, 2026-10-12: "the first floor study" was false, App. C lists the earlier M6.2 and M6.2b floor studies of the same arms; review RC2-1, RN2-3, W5-F4) | §8 or §9.1 | — | DES-5 |
| plateau guard | **a registered convergence check, retired before the grid** (METH-6) | §8.3 | — | |
| drift channels | **position-drift diagnostics (recorded, not graded)** | §8.5 | — | |
| hurdle | **check** | — | — | |
| verdict chip | **verdict label** | — | Figs 11, 13 | |
| family | **the confirmatory family: the two co-primary tests, Šidák-corrected**; then "the two registered tests" | §9.1 | — | |
| branch A–D, A_c | **registered outcome**, defined once; letters in App. E | §9.1 | — | "branch B" stays where a registered reading uses it (the falsifier; "the branch label stays B") |
| unblind, unblinding | **unblinding: the first computation of any outcome contrast** | §9.1 | — | |
| instrument | **analysis script** | — | — | "instruments state what they are blind to" is a rule's name and may stay in §8.5 |
| box | **machine** | — | — | |
| tree, digest, traced (§8's refactor exhibit) | **two versions of the code**; **per-field trajectory hashes** | §8.1 | — | |
| dose | **per-coupling frequency** or **realized count** | §9.1 | — | "dose figure … VOID" stays inside App. D's quotation |
| knee | **change point** | §9.2 or App. H | Fig 13 ("knee") | |
| PAVA, OLS | App. H only | — | — | |
| simplex | **the triangle of training mixtures** | §9.1 | Fig 13 | |
| γ_p, γ_n | **the co-occurrence slope**, **the fire-only-share slope** (symbols kept in App. H) | §9.2 | Fig 13 (literal `γ_p`, `γ_n`) | §3's note on γ (discount vs these slopes) stays one clause |
| m, n (simplex axes) | μ (per-coupling frequency), ν (fire-only share), or the words | §9.1 | Fig 13 | |
| "no-element share …" | **fire-only share** (terminology ruling) | Fig 13 caption | Fig 13 | label defect, P2-2 |
| "floor: ±1 sd = 0.0621" | **a reference scale (cross-artifact)** for this grid (B9) | Fig 7 caption | Fig 7 (`fig04_coupling_b.png`) | label defect, P2-3 |
| obs v2, obs v3 | **the observation before masking**, **the masking observation** | §3.4 | explorers ("observation, as produced (obs v3)") | listings' docstrings keep the tags (byte-identity); prose never echoes them |
| co-active | only for the counter: **collapse-seeded ignitions near an agent** | §6.5 | — | |
| eval | **evaluation** | — | — | |
| lock, locked | **fixed (locked) before the main experiment, with its date** | §3 or §4 | — | |
| Phase-N | name the stage ("the calibration phase") | — | — | |

### 5.3 Strings that stay verbatim (registration or ruling)

"does not survive the inert-share correction"; "sign unstable over the
final half" (both co-primaries); "second exclusion bound"; "a-fortiori
exclusion" with its sentence "no gap larger than X at High even where JOINT
trained on the evaluated configuration and ISO never saw a composed one";
REJECT and null; UNDERPOWERED; VOID; "non-verdict-bearing" (once in §9.1,
then "secondary"); "reference scale (cross-artifact)"; "sensitivity arm";
"fire-only"; "inert under a frozen random-projection encoder at this scale";
"at matched compute"; "stressor", "ambient hazard", "environment
configuration"; the App. D quotations, untouched.

---

## 6. Registered strings and honesty lines: where each lands in v2

### 6.1 Registered strings

| string (verbatim) | governs | lands in |
|---|---|---|
| **does not survive the inert-share correction** | survival Γ given Γ₄ | abstract (required at abstract level), §1, §9.2 (home), §10 |
| **sign unstable over the final half** | Γ(t), **both** co-primaries | abstract, §1, §9.2 (home; verdict first, then the shape), App. G |
| **second exclusion bound** (X₄ = 0.0488) | completion Γ₄ | §9.2 |
| **REJECT** / **null** | Γ (k = 72 and the k = 60 analysis), Γ₄, Γ₄′, Γ_H, Γ_H,4 only | §9.2 |
| **UNDERPOWERED** | the k = 60 analysis; both change points; T = 2000; ISO-4 for the check against rerun noise at High | §9.1, §9.2, App. H |
| **VOID** | mediation (SEC-7); comms condition (iii) (COM-5) | §9.2, App. H; §7, §8.1 |
| **non-verdict-bearing** | every secondary analysis | §9.1 once, then "secondary"; App. H |
| **a-fortiori exclusion** + its sentence | High readout | §9.2 |
| **reference scale (cross-artifact)** | any spread from other runs | §5 (Fig. 6), §6 (Fig. 7) |
| **illustrative** | explorers and renders | hero, Fig. 5's renders, App. I |
| **recorded, not graded** (substance) | the position-drift diagnostics | §8.5, §10 item 6 |
| completion null as an exclusion: "excludes a joint-training gain larger than 0.66 points" (RES-1) | completion Γ | abstract, §1, §9.2; the point estimate −1.73 is never "a loss" |
| bias (b) "reverses sign on the grid card" (DES-10) | differential drift | §9.1 (home, all readings), §1 (one clause), §8.5 (rule, pointer) |
| "the branch label stays B"; branch B's registered headline ("composition is paid in **agents**, not task return", `phase6_framing_branches.md:102`) "no longer holds as worded" | branch | §9.2, App. E |
| the founding hypothesis "did not occur" (branch A) | branch A | §1, §9.2 |

### 6.2 `paper/branch_B.md` §5 honesty lines (`:174-192`) → v2 landing

State each in substance where it lands; the bold label is not prose to paste.

| # | line | lands in |
|---|---|---|
| 1 | **The inert-share qualifier**, abstract-level (registered). | abstract, §1, §9.2, §10 |
| 2 | **Matched compute, never convergence** (T\* ruling) + the Γ(t) suffix. | abstract, §1, §9.1, §9.2, §10 |
| 3 | **Completion null = exclusion with its bound**, never "no effect". | abstract, §1, §9.2 |
| 4 | **δ is inert**; the composition tested is A × B. | §7 (end), §9.1, §10 item 5 |
| 5 | **Medium siting (§4a)**: Coupling B's own survival effect at Medium was −0.0003; its 8.8-point effect is at High. *The pre-unblind line calling a Medium survival effect "a composition effect the single coupling did not show" is STRUCK.* | §6.4 (the measurement's home), §10 item 1 (the registered limitation, with the struck line), §1 (one clause pointing to §10). Lead the High effect with CB-5's 3/3; quote 8.8 (CB-6) only beside it |
| 6 | **The death penalty**: the reward sees deaths (0.5 each), not the hazard; the asymmetry is between a penalized channel and a rewarded one. | §3.3 (home), §9.2 (the falsifier's reading), §10 item 4, §1 (one clause) |
| 7 | **The endpoint confound**: JOINT sees each coupling 3× as often as ISO; the sweep holds marginals fixed and cannot hold the fire-only share fixed at the same time. | §1, §9.1 (home) |
| 8 | **Hardware block structure**: Γ on one GPU; ISO-4 on a second of the same model; Γ₄′ on the confirmatory GPU; post-unblind evaluations on a third. | §9.2 (one sentence), §10 item 8, App. F (home) |
| 9 | **Many secondary intervals, none family-corrected.** | §9.2, App. H |
| 10 | **The co-active counter** means co-active only in all-on configurations. | §6.5 (home), §9.2 (mediation) |

### 6.3 `paper/branch_B.md` §8: what NOT to claim (verbatim, `:225-235`)

- Not "compound stress is paid in agents" — the registered wording no longer holds; it is *exposure*.
- Not "composition does not matter" — Γ₄ and Γ₄′ are exclusions (Šidák CIs [−0.68, +0.63] and [−0.56, +0.81] points on survival, RES-6, RES-8), not absences, and γ_p is a local positive slope.
- Not "composition does not affect the task" — the completion bounds are the claim.
- Not the founding hypothesis. Say flatly that branch A did not occur.
- Not mediation — the mediator was blind.
- Not "budget-robust" and not a converged gap — the registered suffix is "sign unstable over the final half".
- Not "completion is unaffected" — it is unresolved and leans negative.

Gloss: where the record says the survival effect is "exposure, not
composition", the matched quantity is the **active share** (DES-14). At
matched active share JOINT still has 2× ISO-4's per-coupling frequency plus
full co-occurrence, and Γ₄ is null. Say "active share" when you mean it.

---

## 7. The δ design error (F3): the record, and the rows to cite

The owner's F3 asks v2 to own the δ confound as a design error. The record
corrects one premise of the fix list's wording: the bias was **found before
the grid** and **registered mid-grid** (orchestrator finding O1, confirmed
this session). Every writer who touches F3 uses these facts and no others.

| # | step | date | record (read this session) |
|---|---|---|---|
| 1 | The comms axis is closed as inert at this scale (the record says "certified negative"; never echo "certified"), with the frozen-encoder caveat | **2026-07-30** | M5.3 CLOSURE RULING, log:1065; `comms_lock.md:1-3` ("LOCKED 2026-07-30") |
| 2 | The registered Phase-6 design records δ as inert and retains it in θ\* "for registration fidelity at zero cost" | **2026-08-02** (rulings incorporated) | `phase6_design_v2.md:9, :30-33` |
| 3 | The same design gives ISO two δ-only components of six | 2026-08-02 | `phase6_design_v2.md:63, :69-71`; `che/configs/p6_iso.yaml:41-46` |
| 4 | The same design **excludes δ from the secondary sweeps because it is inert** ("Comms is certified inert, so including it would multiply components without adding information") | 2026-08-02 | `phase6_design_v2.md:129-131` |
| 5 | Its review question rests on "Neither protocol trains on δ = 1.0", which is false for both arms | 2026-08-02 | `phase6_design_v2.md:431-433`; `p6_iso.yaml:43, :46` (δ 1.0) — record item, never edited (N5) |
| 6 | Outcome branches registered, with no inert-share accounting | 2026-08-13 | DES-12 |
| 7 | **Identified, pre-grid**, by a review of the registered design: 2 of 6 of ISO's training episodes carry no behaviourally active element; direction: inflates Γ; "The confirmatory arm applies a different rule to the same fact" | **2026-08-16** | `docs/venue_review_2026-08-16.md:1, :11-14, :112-163`; recorded "AWAITING RULING" in VENUE RULING, log:3551, :3643-3655 |
| 8 | The grid begins without the correction | **2026-09-09** | DES-12 (grid 2026-09-09 → 09-22); log:3845 ("no grid run has started", 2026-09-09) |
| 9 | **Registered mid-grid, pre-unblind**: the bias and its direction (proposal 0) and ISO-4 with its reading rule (proposal 1), with 120 of 252 runs done, on the owner's attestation that no outcome mean had been computed or viewed | **2026-09-18** | §7 PROPOSALS RULING, log:3902-3913, :3970-3989, :3996-4029; DES-15 |
| 10 | ISO-4 trains on a second GPU; the same-GPU replicate Γ₄′ is proposed after Γ₄ was seen | 2026-09-26 | DES-15; UNBLIND RESULT log:4995-4997; HW-4 |
| 11 | Unblinding: the survival effect does not survive the inert-share correction | 2026-09-26 | UNBLIND RESULT, log:4987-4994; DES-12 |

**Pre-assigned ledger-proposal rows (W6 writes them in
`ledger_proposals/W6.md`, re-verifying each at its source; W1, W2 and W5
cite the IDs).** Dates are record numbers and take a tag.

| ID | value | what | source | status |
|---|---|---|---|---|
| V6-1 | 2026-08-16 | the inert-share bias in ISO identified, pre-grid and pre-unblind, by a review of the registered design | `docs/venue_review_2026-08-16.md:1, :11-14, :112-163`; log:3551, :3643-3655 | VERIFIED by B1 at these lines (2026-10-11); W6 re-verifies |
| V6-2 | 2026-07-30 | the comms axis closed as inert at this scale (comms lock) | log:1065; `comms_lock.md:1-3` | VERIFIED by B1 (2026-10-11); W6 re-verifies |
| V6-3 | 2026-08-02 | the registered design retained δ, gave ISO two δ-only components of six, and excluded δ from the secondary sweeps because it was inert | `phase6_design_v2.md:9, :30-33, :63, :69-71, :129-131` | VERIFIED by B1 (2026-10-11); W6 re-verifies |

Already rowed: 2026-08-13 and the grid window (DES-12); 2026-09-18 and
120 of 252 (DES-15); 2026-09-26 (DES-12, DES-15). **Do not state a day
count** between identification and registration (it would need its own
DERIVED row and adds nothing).

**Wording constraints (all writers).**
- Own it plainly: the design kept a stressor it had already found inert,
  applied a different rule to it in the confirmatory arms than in the
  sweeps, and did not count the resulting fire-only share. Do not present
  the registration as foresight ("registered as a bias", "a registered
  design caught it", "stated before the result" are out).
- Keep the true facts that remain: the bias and its direction were
  registered **before unblinding**, ISO-4 and its rule were fixed before the
  look, and the confirmatory family did not change.
- "Registered before unblinding" for the correction; "pre-registered" only
  for the 2026-08-13 test.
- The identification: "a review of the registered design" (the record names
  no author; double-blind). The attribution is owner question Q4h.
- Never "certified inert"; never imply δ's inertness was discovered after
  the design.
- The exact wording is the owner's to approve (Q4h). Draft it at the
  homes `STRUCTURE.md` §5 gives: §9.1 (full), §1 (two sentences), abstract
  (one clause), §10 (one bullet), §7 (neutral pointer).

---

## 8. The result set (values, IDs, homes)

Prose states contrasts in **points** (rate × 100, two decimals); tables may
use rates with four decimals. Every interval names its level. Every
Phase-6 interval is conditional on the one evaluation draw (seed 0 × 512
episodes, DES-13). The **home** is where the full statement lives
(`STRUCTURE.md` §7); elsewhere state at most the abstract-level set, or
point.

| quantity | value | ID | home |
|---|---|---|---|
| Γ survival (k = 72) | +0.96 points, z +4.43, Šidák-corrected 95 % CI [+0.47, +1.44]; REJECT | RES-2, DES-13 | §9.2 table |
| Γ completion (k = 72) | −1.73 points, z −1.62, CI [−4.12, +0.66]; null; excludes a gain larger than 0.66 points; X 3.29 points | RES-1 | §9.2 table |
| realized completion power at 0.03 | 71.6 % (k = 72), 60.2 % (k = 60) | DES-6 | §9.1 |
| k = 60 analysis | completion −2.17, survival +1.04 points; CIs [−4.86, +0.52], [+0.54, +1.55]; UNDERPOWERED | RES-3, DX-20 | §9.2 table |
| falsifier | 3.855 < 4.433 (k = 60: 4.040 < 4.673) | RES-5 | §9.2 |
| Γ₄ survival | −0.03 points, z −0.09, CI [−0.68, +0.63]; null | RES-6 | §9.2 table |
| Γ₄ completion | −1.26 points, CI [−4.81, +2.28]; second exclusion bound, X₄ = 0.0488 | RES-6 | §9.2 table |
| Γ₄′ | survival +0.13, z +0.41, CI [−0.56, +0.81]; completion −2.47 [−6.16, +1.22]; null | RES-8, DX-19 | §9.2 table |
| replicate difference (p = 0 sweep arm − ISO-4) | survival −0.15 points, 95 % [−0.86, +0.56] | RES-9 | §9.2 |
| B̂ = ISO-4 − ISO | survival +0.98, CI [+0.33, +1.63]; completion −0.46 [−4.05, +3.12]; **no test, no verdict** | RES-7, DX-19 | §9.2 table |
| Γ(t) | "sign unstable over the final half", both; signs completion `+ − + + − − − − − − −`, survival `+ − − + + + + + + + +` | RES-11 | §9.2, App. G |
| survival shape | +0.56 / +0.83 / +0.96 at t = 900 / 950 / 1000, the only Šidák exclusions; "opens in the last fifth" | RES-12 | §9.2 |
| completion lean | negative from t = 700 (70 % of the budget); Γ(750) −1.47 [−2.83, −0.10], descriptive | RES-13 | §9.2 |
| T = 2000 (4 seeds, descriptive, UNDERPOWERED) | survival +1.59, 95 % [−0.02, +3.19]; completion +0.03 | RES-15, DX-23 | §9.2 (one sentence) |
| High readout | a-fortiori exclusions: no gap larger than 3.40 completion / 2.54 survival points; 0.73× / 0.75× the floor-based SE | RES-14, DX-26 | §9.2 |
| fire deaths JOINT − ISO | −0.1177 per episode, z −4.59 (secondary, out of family) | RES-10, DX-22 | §9.2 (one sentence) |
| secondary | γ_n −2.37 [−4.19, −0.57], γ_p +3.26 [+1.37, +5.02] points (95 %); γ_n predicts B̂ +0.79 (inside B̂'s interval); γ_p predicts +3.26 for JOINT − ISO-4 against −0.03 / +0.13 measured (does not extrapolate) | SEC-1, SEC-3, SEC-4, RES-6, RES-8 | §9.2, App. H |
| mediation | VOID; first-stage slope −1.03 × 10⁻⁵ [−2.91 × 10⁻⁵, +0.93 × 10⁻⁵] | SEC-7, DX-29 | §9.2, App. H |
| arms | ISO 6 × 1/6 (A, B, δ alone × β 0.43, 0.70); ISO-4 4 × 1/4; JOINT 2 × 1/2; per-coupling frequency ISO 1/3, ISO-4 1/2, JOINT 1 (JOINT 3× ISO, 2× ISO-4); active share 2/3, 1, 1; fire-only share of ISO 1/3 | DES-7, DES-8, DES-14, DES-16 | §9.1 arms table |
| seeds | 72 per confirmatory arm (DES-3), registered k = 40 and cap 60 (DES-1), k = 46 on the 2026-09-08 re-measured floor (DES-2); ISO-4 and secondary arms k = 20 (DES-13) | DES-1–DES-3, DES-13 | §9.1 |
| GPUs | Γ: all 72 seeds on GPU 1; ISO-4 and T = 2000 on GPU 2; post-unblind evaluations on GPU 3 | HW-4, DX-5 | App. F |
| reproducibility | seed sd / floor 1.12× / 1.09× (completion), 1.25× / 1.19× (survival); survival Γ 5.40× its floor-based SE; evaluations bit-identical on one GPU; 280 of 288 paired cross-GPU evaluations identical, largest absolute difference 2.44 × 10⁻⁴ | HW-1, HW-2, HW-3, DX-21 | §9.2 (HW-1), §11 (HW-2, HW-3) |

Never present Γ = Γ₄ + B̂ (0.96 ≈ −0.03 + 0.98) as a finding: it holds by
construction for arm means.

---

## 9. Known traps, the claims ceiling and floor, and known lags

### 9.1 Known traps

From `writing_session_prompt.md:138-180` (each has caught a draft): the
inert-share qualifier is never dropped · the Γ(t) suffix on both
co-primaries; the survival gap opens late; the completion lean is stated ·
completion null = an exclusion with its bound · matched compute, never
convergence · bias (b) reverses sign on the grid card · Coupling B's High
effect leads with CB-5's 3/3, not −8.8; its Medium survival effect is
−0.0003 (CB-9) · seeded-ignition figures are m44 (CA-4), not m35; the Def.-4
refutation is M3.0 and survival only (CAL-5); the Prop.-3 handshake is two
runs (CA-2, CA-3) · no reported run used PBT (ENV-11) · comms is "inert
under a frozen random-projection encoder at this scale", never "certified
inert" · the counter is co-active only in all-on configurations ·
fire-only, not hazard-free · Def. 2: hazard-blind, deaths priced
cause-blind; the d_p ablation with its scope · an untested hypothesis is
never a finding ("curriculum difficulty", METH-5) · recorded is not graded
· GIFs and explorers illustrate, never grade · no acceptance-rate or odds
figure · "swarm" is not a claim · "stressor" names only the composable
elements.

Carried from the demo brief, re-verified:
- **B̂ has no verdict.** `post_gamma4_t2000.md:16` prints "REJECT" for it
  (read this session); the log and RES-7 record no verdict (FIGURE BATCH B7).
- **CB-5's "1.41×"** is the first 2-seed estimate (−0.0876, CB-6) over the
  High floor 0.0621, not a pool; the mean of the three contrasts is ≈ 1.19×
  (CB-5 note). That floor is a cross-artifact reference for the Coupling-B
  grid.
- **"A sixth to a quarter"** (`phase4_report.md:366`) contradicts its own
  table; the ceiling claim at :394-395 holds for the κ_B = 1.0 arm only
  (OWNER ITEM 6; DX-11 note). Do not repeat either.
- **"Not behaviourally suppressible"** is scoped to trained policies at
  500 updates.
- **"As predicted before measurement"** is out (OWNER ITEM 1): the fuel
  limitation was first seen at the random-policy calibration (≈ 5.7×, DX-9)
  and recorded at the Coupling-A lock (2026-07-21, DX-401) before any
  trained policy was measured; the later E1.1 prediction came after the
  trained results were on record, and two of its three parts failed (DX-9
  note).
- **No m44 / m35 contrast is graded against a floor on its own artifact**
  (`R/e1/e11_report.md:111-121`, read this session); their spreads are
  reference scales.
- **Never "every acceptance bar is graded against a measured floor".** Say
  which bars have floors (§8.6).
- **Def. 4's "maximal unpredictability … most interesting behaviour"** at
  Medium is a design-time expectation, refuted for survival (CAL-5).
- **ISO-4 and Γ₄ are across GPUs**; Γ₄′ is same-GPU and was proposed after
  Γ₄ was seen, before its arm was read (DES-15).
- **The High readout is not a held-out test** (JOINT trained on that
  configuration at weight 1/2; `post_evalfloor_gamma_t_high.md:88`, read).
- **T = 2000 is descriptive, 4 seeds, UNDERPOWERED**, cited only for whether
  the drift visibly persists, closes or reverses (`post_gamma4_t2000.md:35`,
  read).
- **The hazard is not agent-independent** (CA-8, CA-9; home §5.1).
- **The reward-independence test pins the alive transition equal** and
  changes h, ρ, c only far from every agent (`test_reward_independence.py:6-15`,
  read); the cause-blindness test kills an agent by fire and by collapse and
  asserts −d_p both times (`test_lethality.py:143-148`, read).
- **Five registered outcome cells**: A–D on 2026-08-13 and A_c on 2026-09-26,
  pre-unblind (DX-102, DX-405).
- **ISO-4's rule was registered mid-grid** (120 of 252) and pre-unblind, on
  the owner's attestation (log:3907-3909; DES-15).
- **Prop. 4 bounds what ISO can be guaranteed, not what happens** (honesty
  note, TF:636-643, "must appear in the paper").
- **No dollar figures** (costs are not ledgered).

New in v2 (each is a `FINDINGS.md` row):
- the F3 timeline of §7 (O1); "pre-registered" only for the 2026-08-13 test
  (P1-N3);
- "each stressor is a parameter of one transition **or observation**
  kernel" (N9);
- "positive covariance, the expected sign, makes the unpaired test
  conservative", never "any induced covariance" (P3-N14; log:3143-3146);
- "γ_p does not extrapolate to JOINT", never "saturates" (N12);
- no 43/18 or 4/3 anywhere, and no divergence claim on the finite arena
  (C1, P3-N5);
- never "irreducible" for Prop. 4, and no ISO-vs-JOINT slack contrast
  (C3, N6);
- never "finite Dec-POMDP" without "on its reachable states" (OWNER ITEM 2);
- Remark 1 is a worst-case result for the class; no "(δ > 0) … does not
  reduce to a multi-agent POMDP" (C2, P3-N2);
- the recommendation is labelled, lives in §9.3, is not a contribution, and
  never follows "therefore", "so" or "thus" (F4);
- no internal jargon in body prose (§5.2); one home per result
  (`STRUCTURE.md` §7); a caption does not repeat a number the figure prints;
- "Every adversarially trained arm is perturbed throughout" and "do better"
  (Erdem & Üre) are out (OWNER ITEM 3, N15);
- "the agents did not need the information" is the record's demand-side
  reading (log:1074-1081); keep it as the record's reading (P3-N17 is an
  owner choice).

### 9.2 Claims ceiling and floor

**Must be said (floor):** CHE is pure JAX and multi-agent; a CA fire burns
in every episode; collapse can add ignitions (Coupling A); smoke attenuates
perception by Beer–Lambert transmittance (Coupling B); an independent
comms-denial axis; the fire is an ambient hazard in no reward, cost or
constraint channel; the reward reads task variables and deaths and prices
every death the same; severity placed relative to a **measured**
percolation threshold; bitwise-exact nested ablations; floors per metric,
per GPU, per artifact; collapse-seeded ignitions fall 4.8-fold Low → High
under trained policies (CA-4; home §5.3); the pre-registered test (held-out
severity, matched compute, 72 seeds, cap 60, a recorded deviation before
unblinding); survival +0.96 points [0.47, 1.44]; completion −1.73 [−4.12,
+0.66], an exclusion of a gain above 0.66; sign unstable over the final
half on both; the survival gap opens in the last fifth; completion leans
negative from 70 %; the survival gain does not survive the inert-share
correction; δ inert under the frozen encoder at this scale; a third of
ISO's episodes fire-only, **owned as a design error**; ISO-4 (20 seeds) is
0.98 points above ISO, with no test; Γ₄ −0.03 [−0.68, +0.63]; JOINT still
sees each coupling twice as often and always combined; **the
recommendation (labelled; §9.3)**.

**Must not be exceeded (ceiling):** no composition effect; no "composition
does not matter" (bounds only: Γ₄'s upper bound +0.63 lies above Γ's lower
bound +0.47); no budget robustness or convergence; no claim that ISO-4's
rise is due to the active share rather than the per-coupling frequency
(both change; §9.2 reports γ_n and where the plane fails); no novelty claim
beyond "in the search described in §2 we found no …"; the recommendation
was motivated in one environment and is not a general result.

### 9.3 Known lags: the ledger and the rulings win over these

| where | lag | correct |
|---|---|---|
| spine abstract | omits the completion lean; suffix on one contrast; "every acceptance bar … graded against a measured floor"; β̂_c as a reproduction (O-2); "a secondary dose design attributes the gap"; k = 72 not called a deviation; "All code … released" | the rulings and RES-11–RES-13, CB-9, CAL-1 note, SEC rows, DES-3 |
| `branch_B.md` §1, §3, §6, §7 | "keeps more of the swarm alive"; "attributes the gap to fire-only training episodes"; "accounts for the whole effect"; "A registered design caught it"; "Predicted by Def. 2"; "grid 2026-09-08 → 09-23"; "the dose design attributes it" | multi-agent; non-verdict-bearing; γ_n fits ISO-4 − ISO, γ_p fails at JOINT; the F3 facts of §7; grid 2026-09-09 → 09-22 (DES-12) |
| `branch_B.md:225` | quotes branch B's headline as "compound stress is paid in agents" | the registration reads "composition is paid in **agents**, not task return" (`phase6_framing_branches.md:102`; N4) |
| `branch_B.md` §0 | B̂ "95 % [+0.0041, +0.0155]" | RES-7's Šidák CI [+0.0033, +0.0163] |
| `branch_B.md` §4 item 8 | T = 2000 slopes rounded | DES-11, DX-23 |
| `TF` Def. 1 (:62-63) | observation kernel unprimed, without ρ | post-step O(· ∣ x′, h′, ρ′, c′, k′) (`CLAUDE.md` inv. #2; `env.py:394-396`) |
| `TF` Prop. 1 (:151-153) | "S … Ω finite" | finite only on the reachable states (OWNER ITEM 2) |
| `TF` Remark 1 (:163-168), Cor. 1 (:210-233), Prop. 3 (:309-318), Prop. 4 (:610-625) | "the hardness framing applies"; uncited (3) and (4); the 43/18 rate; "irreducible" and the JOINT ε = 0 contrast | §9.1 above; record items for the owner (Q4k) |
| `TF` Def. 8 (:600-608); §9 item 1 | "primary metric task completion"; DBCA "for the first time"; "PBT-style population training" | co-primaries since 2026-08-02; DBCA describes the sweep; IPPO (ENV-11) |
| `TF` Prop. 4 measurement corollary (:645-653) | predicts ISO's exposure to co-active states | the counter is blind in mixtures: never present it as tested |
| `phase6_design_v2.md:431` | "Neither protocol trains on δ = 1.0" | both do (`p6_iso.yaml:43, :46`); registered, never edited (N5) |
| `che/tests/test_p6_grid.py:156-157` docstring | "any induced cross-arm covariance on the safe side" | positive covariance (log:3143-3146) |
| instrument printouts | "UNSTABLE: the sign of Γ is still moving…"; "REJECT" for B̂ | "sign unstable over the final half"; no verdict for B̂ |
| figure labels (frozen) | "no-element share" (Fig 13); "floor" (Fig 7); "obs v3"; "card", "rung", "unit"; "full ladder: §9.2" | glossed in captions (§5.2); a label rebuild is Q11 |
| `KIT_NOTES.md` §S1.5 | `normalizeTag` handles only `{\"a}` and `{\i}` | it strips any `{\X c}` accent macro and drops the accent (review M2, N4) |

---

## 10. Numbers and units

- **Every record number carries a tag** right after it, no space:
  `0.96 points<!-- N:RES-2 -->`; several sources: `<!-- N:RES-2 --><!-- N:DES-13 -->`.
  Record number = measured, ruled, configured, derived or dated value
  (constants, k, β, dates, CIs, ratios, shares such as "a third" or
  "twice"). **Untagged:** section, figure and definition numbers;
  definitional counts ("two arms", "one policy"); theory constants inside a
  cited theorem (β_c = 1/2).
- **Units:** points = rate × 100, two decimals; CIs likewise; exact
  conversion, no re-rounding; `−` (U+2212) in prose; `+` on positive
  interval ends.
- **Interval labels:** "Šidák-corrected 95 % CI" (family, Γ₄, Γ₄′, B̂, Γ_H);
  "95 %, not family-corrected" (secondary, T = 2000); "descriptive" (Γ(t) at
  t ≠ 1000). Every Phase-6 interval is conditional on the one evaluation
  draw.
- **Scope in the sentence:** arm, severity, k, GPU where it matters,
  registered or secondary or descriptive.
- **A number in neither file** gets a VERIFIED row in your
  `ledger_proposals/W<n>.md` first, in the supplement's row format
  (ID | value | what | source | status / note), with ID `V<n>-<k>`, value,
  committed source at file:line and `VERIFIED` (read this session at that
  file:line), or **DERIVED** with the arithmetic on verified rows. Otherwise
  it is cut. §17 lists the numbers with no source; do not state them.

---

## 11. Double-blind (strict)

- No name, account, e-mail, repository URL, GitHub or OSF link, rental host
  string, host address, GPU UUID, local or absolute path, or commit hash,
  **not even a 7-character prefix** (the Phase-6 reports carry a git hash on
  line 3; never quote it).
- Registration is described **by date**. Archive sha256 values are allowed
  (they resolve to nothing). GPU model names are allowed.
- In-repository file paths are allowed in listings and their labels (they
  name the code). Whether an anonymized code supplement exists is undecided
  (N14, Q4e): do not promise one.
- The environment is named CHE in the abstract and body (ABSTRACT item 3,
  the owner's call; Q4c).
- **HTML comments ship in the page source** unless stripped at staging
  (M4): never put a name, a path outside the code, a hash or a note about
  people in one. Ledger tags, `LISTING` lines and STUB-SPEC blocks are fine
  (B2 strips them in the staged copy).
- **No "builder-written" label** anywhere in v2: the line-1 status comment
  (§14) replaces it, and the disclosure footnote (§12) is the paper's
  statement of tool use.
- The disclosure footnote names the tool, not the author.

---

## 12. The disclosure-footnote rule (PAPER V2 item 2; review N1)

- **Requirement.** TMLR's FAQ asks that the tool's use be mentioned "as a
  footnote on the first page" (PAPER V2 item 2, log:6057-6058).
- **Form (default).** W1 writes one `<d-footnote>…</d-footnote>` at the end
  of the abstract's first sentence in `sections/00_abstract.md`. The
  abstract is the only body text that can land on printed page 1 (P2 §3).
- **Content rules.** Plain text, one or two sentences. Names the tool, not
  the author. No name, account, URL, path or hash. No `$`, no math, no
  `<d-cite>`, no `"`, no Markdown (raw HTML only: `<em>` if needed).
- **What it says.** That an LLM tool was used, and for what, as the record
  documents each use; every use gets a provenance row: drafting of this
  text from the owner's rulings and records, with the author checking every
  word and responsible for it (PAPER V2 item 1, log:6047-6052); the
  literature search and its verification (§2's "How we searched", DX-101;
  READS RULING, log:5741-5747); other uses only as the record documents
  them. It claims nothing the record does not show (for example, it does
  not assert that the ideas are "human-sourced"; that is the owner's
  statement to make). Which uses it names is owner question Q16.
- **Where the kit puts it.** The kit layout places `<d-footnote-list>` after
  the article (`distill.html:161-164`, per the review's reading of the kit
  source): the marker is on page 1, but the text prints at the end of the
  page and of the printed PDF. UNVERIFIED in a build: B2's checks report the
  marker's page and where the text prints.
- **Alternate (owner choice, Q4f).** W1 also writes
  `sections/alt/00_abstract.disclosure_line.md`: the same abstract with a
  visible first-page disclosure line (a short paragraph directly after the
  abstract, before the hero), with or without the `<d-footnote>`.

---

## 13. The provenance rule (INTERFACE "Provenance rows")

- **One file per section**: `provenance/NN_slug.md`, in B2's
  `provenance/TEMPLATE.md` format (if it differs from the line below, the
  template wins). One table row **per sentence**, in order:

  `| # | sentence (verbatim) | support | change from the demo, and why |`

- **What counts as a sentence:** every prose sentence; captions; figure-note
  status tags; table cells that carry a claim; `alt` text; the disclosure
  footnote; listing labels.
- **Support** is one of: ledger ID(s); a decision-log entry heading with its
  line number; file:line; a citation key plus the `RWV` line that supports
  the use; `framing` for a sentence that makes no claim.
- **Change column:** "kept" / "edited" / "new" / "from owner text
  (`paper/finale.md:<line>`)"; the class and finding ID for any fix ("class
  A, F3"; "class B, finding N12"), and for class B the demo's (or owner's)
  original wording, so the owner can revert.
- **A pipe inside a cell** is written `\|`; a sentence containing math is
  copied as written.
- **At the end of the file:** a "Findings" list for anything new you found
  (kind, location, evidence, proposed direction; not applied unless class
  B), and the alternates you wrote.
- **W1 only:** `provenance/00_abstract.md` also carries the title candidates
  (3–5, each with what it leads with and its support) and the `description`
  (new line, support, and the owner's line from `paper/finale.md:4` as the
  revert option).

---

## 14. Kit syntax and traps

Facts from `paper/beyond_pdf/KIT_NOTES.md` §S1.4–S1.9, the demo's one real
kit build (`paper/demo_beyond/KIT_BUILD.md`) and the review's reading of
the kit source. B2's build and checks are the ground truth.

**File shape.**
- Line 1, exactly: `<!-- PAPER V2 DRAFT (PAPER V2 ruling, 2026-10-11): builder-drafted, not owner-approved -->`
- Then the `## N Title` heading exactly as your stub has it (none in
  `00_abstract.md` and `00_hero.md`; `13_` and `14_` open with an H3, since
  they continue `## Appendices`), then the STUB-SPEC block, which you keep
  until the owner's review, then your text. No YAML in section files.
- Subsections are H3. **H2 text:** ASCII letters, digits, spaces and ": "
  only beyond the leading number (the `toc` link is `slugify(name)` and
  must equal kramdown's id). **No heading anywhere** carries Γ, β, math,
  an em dash, quotes, `*` or parentheses. H3s may carry "9.1"-style numbers
  (not in the `toc`); appendix H3s are a letter plus ASCII words
  ("G Gamma over the final half of training").
- Definitions and propositions are bold run-in paragraphs
  (`**Definition 2 (Ambient hazard).** …`); a proof ends with `$\blacksquare$`.

**Pipes (M1).** kramdown 2.4.0 starts a table on **one** unescaped `|`
outside a code span, on a prose line, a list item or a blockquote line;
math does not protect it (table detection runs first). Write absolute
values `$\lvert x\rvert$`, norms `$\lVert x\rVert$`, conditioning `\mid`,
or words. Never `|` inside math in a table row. Raw HTML blocks are safe.
B2 checks the source (one pipe) and the kit (table count = source count).

**Math (MathJax 3.2.0).** The compile step rewrites every lone `$` to `$$`
everywhere, code and comments included (`KIT_NOTES.md` §S1.6 item 2).
- Inline: `$…$` (becomes inline `$$…$$`). Display: its own paragraph, `$$`
  on its own lines, blank lines around. Never a single inline expression
  alone as a paragraph (it would become display).
- **No `$` in raw HTML** (figcaption, `<p class="caption">`, `<d-footnote>`,
  HTML labels): Unicode there (κ<sub>B</sub>, θ&#42;, Γ₄, ≤, ×).
- No `{{` or `{%` in math (`x^{{2}}` runs Liquid); no `\newcommand`,
  `\label`, `\eqref`, `\tag`; refer to "the display in Definition 2".
- Rendered without error in the demo's kit build (578 expressions):
  `\mathcal`, `\mathbb`, `\mathbf{1}`, `\mathrm`, `\operatorname`,
  `\underbrace`, `\tfrac`, `aligned`, `\blacksquare`, `\lvert`, `\Big(`.
  Anything else, flag it for B2.

**Liquid.** Only `{% include figure.html … %}` and
`{{ '…' | relative_url }}`. `{{` and `{%` execute anywhere, comments
included.

**Front matter (`front_matter.yaml`; W1's `title` and `description`).**
One line each; no `"`, no backslash, no `<` or `&` (the title is
interpolated raw into the `<h1>` and into a JavaScript string,
`distill.html:24`, `:130`); a plain YAML scalar cannot contain `: `, so
avoid it, or B2 single-quotes the value and checks it; `description` has no
number (DESCRIPTION item 1), so no tag. Length matters: a title over about
75 characters takes more than three lines at 1280 px and pushes the
abstract, and the footnote marker, down (P2 §3, P2-7; preview estimate).

**HTML.** `&lt;` `&gt;` `&amp;` in raw HTML; Markdown is not parsed inside
HTML blocks (`<em>`, `<strong>`, `<code>`); no `--` inside a comment, no
nested comments; no `{:` at a line start; blank line before and after every
table, list, fence and display. No `<details>`, `<aside>`, `<d-appendix>`,
`markdown="1"` or kramdown footnotes for content that must print.

**Prose traps (P2 §5.3).** Bare `_` or `*` opens emphasis (write θ\*,
Γ₄, `$\Gamma_H$`); a line starting `: `, `*[`, `[^`, four spaces, or `1. `,
`- `, `+ ` (unless a list is intended); `--`, `---`, `...`, `<<`, `>>` in
prose (typographic conversion); `<` followed by a letter in prose.

**Figures.** The iframe form and the print companion as in your stub's
carried blocks; `include` `caption="…"` and `alt="…"` hold no `"`, no `{`
and no record numbers (a figure number is fine). A static figure with
numbers or math in its caption: a short include caption, then a
`<p class="caption">` paragraph carrying the full caption and its tags.
**Keep each figure block self-contained and movable** (no "above",
"below", "the next figure" in prose; refer by number): the hero alternate
moves blocks (`STRUCTURE.md` §9).

**Captions.** Say what the figure shows and what it cannot show; never what
to conclude beyond a registered string. Registered verdict strings go
first. A number the figure prints is not repeated in its caption (P2 R3).
Status tags at most about 12 words, interaction at most about 15; the
status vocabulary is explained once in the reading note under the hero
(W1). Each caption glosses, once, any jargon the figure prints (§5.2).
Caption caps are in `STRUCTURE.md` §8.

**Listings.** `<!-- LISTING: <repo-relative path>:<start>-<end> -->` on its
own line, then the fence. The fence's first line is the header
`# <path>:<start>-<end> (verbatim)`, matching the LISTING line exactly (the
demo's form, P2 §4); B2's build accepts that one header line and checks
that the rest of the fence body is byte-identical to those lines of the
committed file (`src/build_v2.py`, listing check; INTERFACE "Listings").
Introduce each listing in a label paragraph ("**Listing 1.** …") and say
what it proves. The code's own comments carry internal tags (`M4.1`,
`obs v3`, `Q3 ruling`, `invariant #3`): byte-identity keeps them; your prose
must not echo them. Your stub carries the exact block; move it, never edit
it.

**Cross-references** are plain text: "§9.2", "Figure 4", "Table 2",
"Listing 3", "Appendix C" (INTERFACE). B2's build lists each with its
target.

**Citations.** `<d-cite key="k1,k2"></d-cite>` (INTERFACE); every key in
`paper/v2/assets/bibliography/submission.bib`, or the build fails.

---

## 15. Citations: keys and permitted uses

Keys only from `paper/v2/assets/bibliography/submission.bib`: the 40 keys
of `paper/beyond_pdf/assets/bibliography/submission.bib` (listed below),
corrected at source by B2 (M2), plus `garet2004chemical` once B2 has
entered it through `RWV`. **Characterize a work only as `RWV` Part 3 and
the owner's §2 (`paper/finale.md:180-370`) do; say nothing new about any
cited work.**

| key | permitted use |
|---|---|
| `crain2008stressors`, `cote2016stressors` | ecology studies interactive and cumulative effects of multiple stressors (origin of "stressor") |
| `zscheischler2018compound`, `zscheischler2020typology` | compound events and their risk studied in their own right (analogy) |
| `gao2024composition` | closest earlier study of the question: visual imitation learning for manipulation; factors; matched number of demonstrations; policies compose, more weakly when both factors are physical; built for data efficiency, not to separate co-occurrence from frequency (owner-read, §1 INTRODUCTION item 2) |
| `kirk2023zsg` | zero-shot generalization; our held-out test belongs to it |
| `haksar2018` | the hazard is the task: multi-agent deep Q-network rewarded for moving to burning trees on the boundary (their Algorithm 2); the fire cannot harm them |
| `garcia2015safe` | definition of safe RL; safe RL typically puts a hazard in a constraint or cost (may now be cited in §1, READS RULING item 4) |
| `bernstein2002` | finite-horizon Dec-POMDPs are NEXP-complete (a worst-case result for the class; Remark 1). VERIFIED for identity only (N15) |
| `grassberger1983` | SIR with a constant infectious period ↔ bond percolation (Prop. 2). Identity only (N15) |
| `kesten1980` | β_c = 1/2 for bond percolation on the square lattice (Cor. 1(1); its title states it). Identity only (N15) |
| `garet2004chemical` (new, B2) | **only** for Cor. 1(4) at the level `paper/v2/citations/C1_verification.md` §2 verified: supercritical bond percolation on ℤ², conditioned on the origin's cluster being infinite, the chemical ball of radius n rescaled by n converges in Hausdorff distance to a deterministic convex compact set (their Corollary 5.4, p. 188); the speed depends on direction |
| `dewitt2020ippo` | independent PPO |
| `lu2022dpo` | the PureJaxRL implementation basis |
| `rutherford2024jaxmarl` | JaxMARL environment conventions; a JAX MARL benchmark with no spreading lethal hazard |
| `alomari2025macraftax` | Multi-Agent Craftax: health lost to hunger and enemies, agents can die; lava is static terrain agents cannot enter |
| `hinckeldey2025assistax` | Assistax, a JAX MARL benchmark with no hazard field |
| `tao2025pobax` | POBAX, a single-agent partial-observability suite |
| `bettini2024benchmarl` | BenchMARL, built on TorchRL, not JAX |
| `hafner2022crafter`, `matthews2024craftax` | lava lethal in Crafter and Craftax-Classic; reward ± per health point (prices an outcome) |
| `cakir2025jaxwildfire` | JAX CA wildfire, one air-tanker agent; per-step penalty proportional to burning cells plus an extinction bonus (hazard-priced); no agent harm described; observations partial, egocentric, not attenuated |
| `liu2026vulcan` | VLM-planned multi-robot fire search and rescue; a hazard cost map; preliminary evaluation covers baselines; degrades sensing with smoke without a transmittance model; its metric "CHE" (cumulative hazard exposure) is unrelated to our name |
| `raut2026psps` | single-agent public-safety power shutoffs; power flows set line failure probability (ignition risk); reward negative operating cost; no spatial spread |
| `tobin2017dr`, `muratore2022drreview` | domain randomization |
| `dennis2020paired`, `jiang2021plr`, `jiang2021robustplr`, `parkerholder2022accel` | PAIRED; Prioritized Level Replay; PLR as environment design; ACCEL |
| `mendez2022composuite` | CompoSuite: composition of tasks, not of co-occurring stressors |
| `keysers2020` | DBCA: our **sweep** follows it; the ISO/JOINT endpoints do not |
| `erdem2025mixed` | single-agent continuous control against a learned adversary on observations, actions or both; single-type arms vulnerable to simultaneous attacks (their Tables 3–4); Table 5 tests single-type attacks on the two hybrid arms only (ASA-PPO at least as well as N-HYBRID-PPO in 6 of 6 cells, one tie); six arms including an unattacked Non-Robust baseline; in each adversarially trained arm an attack is computed at every step (their Algorithm 1), a capped magnitude that may be near zero (unreported); none mixes single-type attacks; neither supports nor contradicts our corrected null (`RWV` HEAD :918, :1004-1014) |
| `agrawal2023multimodal` | MARL against random reward, state and action noise, one or two types at a time, with a curriculum; exposure differs between models |
| `tramer2019multiple`, `hsiung2023compositional` | robustness to multiple and composite perturbations (supervised vision) |
| `chen2022understandingdr` | DR as a latent MDP; upper bounds assume communicating MDPs; Thm. 1 is kin to their Prop. 1 construction but not covered; neither subsumes the other |
| `pynadath2002` | COM-MTDP: free communication lowers complexity under collective observability (their Theorem 4, Table 2) and makes no difference when individually or not observable (Theorems 5–6); Remark 2′ refines this (READS RULING item 4). `RWV` HEAD :922 also records Theorem 3 (NEXP → PSPACE under collective partial observability); citing it is owner question (P3-N12) |
| `hu2025adaptablemarl` | an environment family is highly diagnostic if it "systematically varies" factors "while holding other factors fixed" |
| `jaderberg2017pbt` | not cited by default (O-1, Q4j) |
| `zhao2020simtoreal` | sim-to-real survey (neighbour only; uncited in the demo) |

Not citable (no entry): Altman or any CMDP text; SMART; JaxWildfire's
ancestry; DIAL; any source for Cor. 1(2)'s tails, the "universal" caveat,
the simulation lemma, or χ's divergence on ℤ², unless B2 enters one first.

---

## 16. Figures and listings

Default numbering (hero option A, the ruled one). Numbers come from this
table; refer to figures by these numbers only. Heights are the demo's
iframe attributes (P2 measured larger self-sized heights; changing them is
P2-5, class C).

| fig | file (basename) | print companion | iframe H | section, writer | stated numbers come from |
|---|---|---|---|---|---|
| 1 | `explorer_thetastar_random_seed0.html` | `explorer_thetastar_random_seed0_static.png` | 720 | hero, W1 | ENV-6, ENV-13, CAL-3, CA-1, CB-1, COM-6; DX-33 |
| 2 | `composer_training_mixtures.html` | `composer_training_mixtures.png` | 430 | §1, W2 (§9.1 refers back) | DES-7, DES-8, DES-14, DES-16, CAL-3 |
| 3 | `opening_ladder.html` | `opening_ladder.png` | 400 | §1, W2 | RES-1, RES-2, RES-6, DES-1, DES-3, DES-13, DES-15, HW-4 |
| 4 | static `fig01_schematic.png` (from `paper/figures/out/img/`) | — | — | §3, W3 | ENV-6 |
| 5 | `severity_explorer.html` | `severity_explorer.png` | 520 | §4, W3 | CAL-3, CAL-4, CA-1, CB-1, DX-7, DX-202 |
| 6 | `coupling_a_explorer.html` | `coupling_a_explorer.png` | 680 | §5, W4 | CA-2–CA-6, CAL-3, DX-40 |
| 7 | static `fig04_coupling_b.png` | — | — | §6, W4 | CB-10, CB-6, CB-7, DX-13 |
| 8 | static `fig05_coactive.png` | — | — | §6, W4 | CO-2, CAL-3 |
| 9 | static `fig06_comms.png` | — | — | §7, W4 | COM-4, COM-1 |
| 10 | `floors_explorer.html` | `floors_explorer.png` | 460 | §8, W5 | METH-1, METH-2, METH-5, HW-1, DES-13, DX-303 |
| 11 | `ladder_registered_readings.html` | `ladder_registered_readings.png` | 1000 | §9.2, W6 | RES-1–RES-3, RES-6–RES-8, DES-1, DES-3, DES-13, DES-15, HW-1, HW-4 |
| 12 | `gamma_t_final_half.html` | `gamma_t_final_half.png` | 480 | §9.2, W6 | RES-1, RES-2, RES-11–RES-13, DES-13 |
| 13 | `simplex_secondary.html` | `simplex_secondary.png` | 820 | §9.2, W6 | DES-7–DES-9, DES-14, SEC-1–SEC-7, RES-6–RES-8 |
| I1 | `explorer_thetastar_iso_s1_T1000_ep0.html` | `…_static.png` | 720 | App. I, W6 | ENV-13 |
| I2 | `explorer_thetastar_joint_s1_T1000_ep0.html` | `…_static.png` | 720 | App. I, W6 | ENV-13 |

Not used, by ruling: the slot versions of the interactive figures (A2);
every GIF (A4, A5); explorer deep links (A6). Under hero option B (Q8) the
opening ladder becomes Figure 1 and the explorer Figure 3, at the head of
§3 (`STRUCTURE.md` §9).

**Listings (six; 124 code lines against the demo's 152; P2 §4).** No `$`,
`{{` or `{%` in any range (P2, checked).

| L | file:lines | proves | section, writer |
|---|---|---|---|
| 1 | `che/env/env.py:298-358` | one step in the Prop. 1 order; the reward line reads only the task reward and the death counts | §3, W3 |
| 2 | `che/env/tasks.py:31-43` | the task reward's signature admits food and occupancy only | §3, W3 |
| 3 | `che/tests/test_coupling_b.py:131-142` (shortened from :131-156) | κ_B = 0 reproduces the pre-masking environment bitwise (hazard, smoke, structure, food, positions, alive flags, reward); the hand-stepped observation check (:143-156) becomes one sentence citing the range | §3, W3 |
| 4 | `che/env/structure.py:83-102` | Coupling A's uniforms are drawn before κ_A is read; seeding acts on c′ − c | §5, W4 |
| 5 | `che/env/observation.py:300-310` (shortened from :289-310) | τ by Beer–Lambert; the reveal draw is unconditional; the visibility plane is appended | §6, W4 |
| 6 | `che/train/ippo.py:323-329` | `stop_gradient`: no gradient crosses the channel, so the encoder is frozen (ENV-12) | §7, W4 |

Listings 1 and 2 keep lines over 79 characters (`env.py:310, :330, :336,
:349, :357`; `tasks.py:31`); B2's listing CSS handles them (KIT_BUILD 2).

---

## 17. NO SOURCE: do not state

- R_L logistic centres as produced by a committed artifact (O-2): CAL-1 is
  the lock record's value.
- Per-arm realized training dose (0.000809–0.000817) and the identification
  arms' "0.80×" (log:5099-5106 only; no committed table).
- Supplement size (SUP-1, O-3) and any venue supplement limit (SUP-2, O-4).
- Any acceptance rate, odds or time-to-decision; any dollar cost or total
  GPU-hours.
- Floors for the position-drift diagnostics (none exist).
- "4096 runs per Prop.-3 point" (no row).
- Any alive count, completion or return of a rendered episode (random, ISO,
  JOINT), any difference between two episodes, and the renders README's
  alive tallies (`paper/renders/2026-09-27/README.md:33-35`).
- The hero explorer's hover readouts of ρ and τ as stated numbers
  (`paper/figures/interactive/MANIFEST.md:149-152`).
- Any Γ(t) value beyond DX-24 and DX-25; any T = 2000 value beyond RES-15
  and DX-23.
- "About one in five" for the near-agent share (state CA-6's range).
- Mean alive out-degree beyond COM-3 (1.01 → 2.99).
- Γ₄'s and B̂'s survival X (0.0090 and 0.0089, `post_gamma4_t2000.md:15-16`):
  no row; whether to add one is Q18 (P3-U1).
- A training throughput derived from DX-3 and DX-4 (P3-U5, Q18).
- A day count between 2026-08-16 and 2026-09-18.
- Any planner's or reviewer's derivation offered for the owner's check
  (N6's vacuity, P3-N7's constants, P3-N16's "1 in 4"): these are remarks,
  not paper numbers.

---

## 18. Hand-back (each writer, to the orchestrator)

1. The files written (paths), with prose and caption word counts against
   your budgets.
2. Every `N:` tag used (ID → where), and every new row in your
   `ledger_proposals/W<n>.md`.
3. Every number you wanted and could not tag (not stated in the text).
4. Every class-A and class-B change you applied, by `FINDINGS.md` ID.
5. Every departure from your stub or this brief, with the reason.
6. The listings used (L-number and range).
7. The alternates you wrote (`sections/alt/…`).
8. New findings (not applied unless class B), and open questions for the
   owner, numbered against `FINDINGS.md`'s Q-list where one fits.
