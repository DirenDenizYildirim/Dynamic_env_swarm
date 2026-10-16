# STRUCTURE — the reconciled v3 structure (builder B1, step 3)

Written 2026-10-14 under PAPER V3 (`docs/decision_log.md:6115`) and PAPER V3
PHASE 1 START (log:6218: θ\* only; no commits; no GPU). It reconciles the
three v3 plans — `plans/P1.md` (argument), `plans/P2.md` (reading path),
`plans/P3.md` (referee's view) — and the orchestrator's notes on them
(scratch `planner_findings.md`). For every choice it says which plan it came
from, or "B1 resolution" with the reason. It holds no paper prose. Rules,
facts, glossary and traps are in `BRIEF.md`; the disposition of every
planner finding and the owner questions (V3Q1…) are in `DISPOSITIONS.md`;
each section's specification is in its stub; writer assignments are in
`WRITERS.md`. Check inputs for B2: `checks/terms.txt`, `checks/dates_allow.txt`,
`checks/caveats.yaml`.

---

## 1. How the plans were reconciled

- **Precedence.** Owner rulings and the change list
  (`paper_v3_prompt.md:174-299`) first; then the orchestrator's record
  corrections; then the plans, each in its lens: **P1 decides the order of
  the argument and where each claim sits; P2 decides figures, captions and
  kit mechanics; P3 decides the page/word budget, the term list and what a
  referee needs up front.** Where two plans disagree inside one lens, §11
  records the resolution.
- **Owner-pending choices** take the change list's default where it gives
  one (Prop. 4 an appendix remark in words; Remark 1 cut; figures glossed,
  not rebuilt), else the standing v2 default, and the alternative becomes a
  V3Q in `DISPOSITIONS.md` §4.
- **Nothing that depends on the interaction check is written before its
  results return** (V3-F2). Those places carry `<!-- HOLE:INTERACTION -->`
  (§9).

---

## 2. The section list

Main text = files `00_*` to `12_*`; appendix = `13_*` onward. Files are
assembled in filename order. Files `07_`–`09_` continue §6 and open with an
H3; `14_`–`21_` continue `## Appendices` and open with an H3 (v2's
precedent, v2 STRUCTURE §13 item 1). H2 text uses only ASCII letters,
digits, spaces and ": " (BRIEF §14).

| file | heading (exact) | job | pages | prose words | figures / listings | from |
|---|---|---|---|---|---|---|
| `00_abstract.md` | *(none)* | one question, one result, one lesson (V3-F2); registered strings; disclosure `<d-footnote>` slot (owner writes it) | 0.5 | ≤ 250 | — | P1 §3; P3 §2.2 (≤ 250) |
| `00_hero.md` | *(none)* | the environment before any claim: one random-policy episode; one reading-note sentence on what "illustrative" means | 0.3 | caption ≤ 60, note ≤ 30 | Fig. 1 explorer | P2 §3 #1; P1 front |
| `01_introduction.md` | `## 1 Introduction` | the question an environment must make testable; CHE in a paragraph; the worked example and its result in one paragraph with the strings; **limitations in front** (three short forms, V3-F6); three contributions | 1.3 | 600 | — | P1 §4.2 §1, §5.3; P3 §2.2 |
| `02_related_work.md` | `## 2 Related work` | where the hazard sits (task, cost/constraint, ambient); JAX multi-agent environments; compositional generalization; one sentence on the search (detail App. I) | 0.9 | 400 | Table 1 (compact) | P1 §4.2 §2; P3 §2.2 (1.0) |
| `03_environment.md` | `## 3 The environment` | 3.1 state, step order, fire, smoke (Props. 1–2 in one sentence each); 3.2 the three stressors (Coupling A, Coupling B, comms denial; Prop. 3, Thm. 1 in words); 3.3 the reward (hazard-blind, cause-blind death price, contact-penalty fact); 3.4 exact nesting and theory as tests (**claim → listing → test → figure table**); 3.5 the instance, training, metrics, the counter | 3.0 | 1,050 | Fig. 2 schematic; Listings 1–4; Table 2 (claims) | P1 §4.2 §3; P2 §2 (table); P3 §2.2 |
| `04_calibration.md` | `## 4 What each stressor does` | 4.1 severity by measured phase; 4.2 Coupling A; 4.3 Coupling B (incl. the Medium measurement); 4.4 communication denial (the ruled inert phrase with its bars; the asymmetry) | 2.1 | 700 | Figs. 3–5 | P1 §4.2 §4; P2 §3 #3–#5; P3 §2.2 |
| `05_measurement.md` | `## 5 Measurement protocol` | the floors protocol as rules, not history: per metric, per GPU, per artifact; 80 %-power MDE at the corrected α; the contrast's SE; recorded ≠ graded; a four-run floor's uncertainty | 0.6 | 270 | — (floors explorer in App. C) | P1 §4.2 §5; P3 §2.2; P2 §3 A2 |
| `06_example_design.md` | `## 6 Worked example: training on stressors together or apart` + `### 6.1 What was registered, and what changed` + `### 6.2 Design` | 6.1 what was registered; the framing-change disclosure (V3-F5); the central limitation in full (sited where composition is weak). 6.2 arms, held-out θ\*, matched compute, co-primaries, Šidák, 72 seeds (one clause), one evaluation draw; the identity with each arm's values; the inert third owned as a design error; the δ train/test mismatch; bias (b) in one sentence | 1.3 | 500 | Fig. 6 composer | P1 §4.2 §6.1–6.2, §1.2, §5.2; P2 §3 #6 |
| `07_example_results.md` | `### 6.3 Results` | **the plane decomposition first** (secondary, non-verdict-bearing), then the registered test (table with arm means), the correction, Γ(t) by its string, the size in agents per episode; Γ₄'s detection limit | 1.4 | 480 | Fig. 7 simplex (leads); Fig. 8 readings; Table 3 | P1 §4.2 §6.3, §5.1–5.2; P2 §3 #8–#9; PAPER V3 2(c) |
| `08_interaction_check.md` | `### 6.4 A post hoc interaction check` | what the check is, its label, its result per the PLAN's reading rules, what it is blind to (the one home) — **HOLE until step 0.5** | 0.55 | 200 | Fig. 9 interaction (new; HOLE) | P1 §3.3, §4.2; P2 §4; PLAN.md |
| `09_example_lesson.md` | `### 6.5 What the example teaches` | the lesson (identity: matching the active share cannot isolate co-occurrence); one labelled "we suggest" sentence; future work (ISO-4 at 2000 updates, which gives up matched compute; varying coupling strength) — **lesson HOLE until step 0.5** | 0.35 | 150 | — | P1 §5.2, §3.3; P3 §3.1 (3); V3-F4 |
| `10_limitations.md` | `## 7 Limitations and scope` | only what §1 did not carry: matched compute not convergence (one line), no theorem that joint training wins, cross-GPU blocks by pointer, the d_p ablation's scope, no heuristic baselines, train/test comms by pointer | 0.45 | 200 | — | P1 §4.2 §7; P3 §2.2 |
| `11_using_che.md` | `## 8 Using CHE and reproducing the paper` | API in two lines; configs and locks; how to run (tests, train, evaluate) inside the supplement; compute per run; what can be varied; what the supplement holds and reproduces; the registration statement (V3-V2); evaluation reproducibility | 0.55 | 240 | — | P3 §1.2–§1.3 ("Using CHE"); P1 §4.2 §8; V3-V1–V3 |
| `12_conclusion.md` | `## 9 Conclusion` | three sentences: what CHE is for, what the example showed, what to run next — **one HOLE** | 0.2 | 90 | — | P1 §4.2 §9 |
| `13_appendix_proofs.md` | `## Appendices`, index, `### A Proofs and formal statements` | Props. 1–3, Cor. 1, Thm. 1 (statement per V3Q5), proofs; Prop. 4 as a remark in words with its honesty note; Remark 2′ statement; Listing 5 (the full step) | — | ≈ 1,000 | Listing 5 | P1 §6.1 A; V3-S6 |
| `14_appendix_locks.md` | `### B Locked constants and hyperparameters` | every locked constant (values; dates live in App. D), hyperparameters, budget, the message encoder (Listing 6); Coupling B's lock bands that did not intersect | — | ≈ 350 | Listing 6 | P1 §6.1 B; B1 (Listing 6 moved here) |
| `15_appendix_floors.md` | `### C Floors` | every floor with its GPU, run length, artifact and reps; the exhibits §5 no longer tells, one line each; the floors explorer | — | ≈ 500 | Fig. C1 floors explorer | P1 §6.1 C; P2 §3 A2 |
| `16_appendix_timeline.md` | `### D Registration timeline` | the audit trail (§8 below) | — | ≈ 1,000 + quotations | — | V3-S2; P1 §6.2 |
| `17_appendix_results.md` | `### E Additional results` | Γ(t) tables and figure; the k = 60 analysis (UNDERPOWERED); T = 2000 (descriptive, UNDERPOWERED); the High readout (a-fortiori exclusion, verbatim); fire deaths; seed dispersion over floor; the communication-denial measurements figure | — | ≈ 550 | Fig. E1 Γ(t); Fig. E2 comms | P1 §6.1 E; P2 §3 A1, A3 |
| `18_appendix_secondary.md` | `### F The secondary design` | the sweep, the plane fit, mediation (VOID), arm code names as figure labels | — | ≈ 400 | — | P1 §6.1 F |
| `19_appendix_interaction.md` | `### G The interaction check in full` | plan summary, floors, cross-GPU check, per-arm table, main effects (descriptive) — **HOLE until step 0.5** | — | ≈ 400 | — | P1 §6.1 G; PLAN.md §9 |
| `20_appendix_episodes.md` | `### H Trained-policy episodes` | the ISO and JOINT explorers, separately (default kept; V3Q10) | — | ≈ 80 | Figs. H1, H2 | v2 default (Q12); FIGURE BATCH A3; P2 recommends drop |
| `21_appendix_making.md` | `### I How the literature search ran` + `### J How this paper was made` | the search (DX-101); the division of labour, from the builder's draft quoted in PAPER V3 item 6, for the owner to edit | — | ≈ 400 | — | P1 §6.1 I, J; PAPER V3 item 6 |

**Appendix letters, v2 → v3:** A proofs (kept); B locks (kept, + encoder);
C floors (kept); D–F of v2 (frozen plan, branches, grid provenance) →
**D registration timeline**; v2 G (Γ(t)) → **E**; v2 H (secondary) → **F**;
new **G** (interaction check); v2 I (episodes) → **H**; new **I** (search,
moved from §2) and **J** (how this paper was made).

---

## 3. Page and word budget (V3-S1)

**Measured v2 baseline.** P1 and P2 measured the v2 printed PDF
(`paper/v2/out/submission_v2_print.pdf`, 46 pages) by heading positions
(`pdftotext -bbox`): main text **33.42 pages** from page 1 to the
Appendices heading (P1 §4.1; P2 §1.1). P3 measured 33.71 by the same method
with a slightly different appendix-start reading (P3 §2.1); the 0.3-page
difference is P3's §11 (0.93 against 0.64). B1 uses 33.42 (two plans
agree).

**Page measure for B2's ≤ 15 check (proposed; owner V3Q2):** from the top of
printed page 1 to the first appendix heading, front matter included (P1
§4.1, P3 §2.2), on the kit's printed PDF.

**Word method (one method everywhere, PR:485):** v2 `plans/P3.md` §5 steps
1–5, as re-implemented by v3 P3 (`scratchpad/P3/wordcount.py`): comments and
fenced code dropped; captions (figcaption, `<p class="caption">`, include
`caption=`) and figure-note spans counted separately; math dropped;
markdown-it paragraphs and list items = **prose**; tables and headings
counted separately. Budgets below are **prose**; captions have caps;
tables are reported. B2 is asked to commit a copy of that script under
`paper/v3/src/` so writers and reviewers count the same way (B2's lane).

| part | pages | prose words | caption cap | from |
|---|---|---|---|---|
| front matter (title, description, byline, contents) | 0.75 | — | — | fixed by the kit (P3 §2.2) |
| abstract | 0.5 | ≤ 250 | — | P1 §3; P3 §2.2 |
| hero | 0.3 | note ≤ 30 | 60 | P2 §3 (0.31 at v2 size) |
| §1 | 1.3 | 600 | — | P1 1.25 / P3 1.5 |
| §2 | 0.9 | 400 | table ≤ 120 | P1 0.9 / P3 1.0 |
| §3 | 3.0 | 1,050 | Fig. 2 ≤ 50; Table 2 ≤ 160 | P1 3.0 / P3 3.25 |
| §4 | 2.1 | 700 | Figs. 3–5 ≤ 60 each | P1 2.0 / P3 2.25 |
| §5 | 0.6 | 270 | — | P1 0.6 / P3 0.75 |
| §6.1–6.2 | 1.3 | 500 | Fig. 6 ≤ 50 | P1 1.4 |
| §6.3 | 1.4 | 480 | Figs. 7, 8 ≤ 60 each; Table 3 | P1 1.5 |
| §6.4 | 0.55 | 200 | Fig. 9 ≤ 60 | P1 0.5 (+ P2's figure) |
| §6.5 | 0.35 | 150 | — | P1 0.35 |
| §7 | 0.45 | 200 | — | P1 0.6 / P3 0.5 |
| §8 | 0.55 | 240 | — | P1 0.5 / P3 0.5 |
| §9 | 0.2 | 90 | — | P1 0.25 |
| **total** | **14.25** | **≈ 5,130** | ≈ 600 | P1 14.35 / P3 13.75 |

Margin 0.75 page against the ceiling of 15. If the owner wants TMLR's
2-week review tier ("up to 12 pages (of main content)", P3 §0, a
fetch-tool summary not yet re-read directly), P3's first cuts apply: §2 to
0.75, §4 to 1.75, §3 to 2.75, and Fig. 5 moves to the appendix (P2 §3).
Figures at v2 print sizes cost ≈ 2.4 pages of the 14.25 (P2 §3).

---

## 4. Figures (P2 §3, with B1's changes)

Captions say what the figure shows (V3-S4): panels, axes, marks, arms; the
registered verdict string first where the figure carries one; no "cannot
show" clause, no status line, no number the figure prints, no interaction
instructions in print (they go in `<span class="interact">`, hidden in
print). Each figure's limit is stated once, at its text home (§7).
**Figures are glossed, not rebuilt** (default; V3Q8): each printed internal
label is glossed once, in its caption, in the exact form
`labelled “TERM” on the figure` (the form `checks/terms.txt` exempts).

| fig | file (basename) | where | gloss owed (printed label → plain) | from |
|---|---|---|---|---|
| 1 | `explorer_thetastar_random_seed0.html` (+ `_static.png`) | `00_hero.md` | "obs v3" → the observation as masked by smoke | P2 #1; R1 |
| 2 | static `fig01_schematic.png` | `03_environment.md` §3.1 | — | P2 #2 |
| 3 | `severity_explorer.html` (+ `.png`) | `04_calibration.md` §4.1 | companion subtitle clipped in print ("δ 0" lost, v2 P2-1): state κ_A 0.06, κ_B 1.0, δ 0 for the renders in the caption | P2 #3; R8 |
| 4 | `coupling_a_explorer.html` (+ `.png`) | §4.2 | "m44", "m35" → the Coupling-B / Coupling-A calibration grids | P2 #4; R2 |
| 5 | static `fig04_coupling_b.png` | §4.3 | "M4.4", "seed 0/1 (M4.4)"; legend "floor" → reference scale (cross-artifact) | P2 #5; R4; FIGURE BATCH B9 |
| 6 | `composer_training_mixtures.html` (+ `.png`) | `06_example_design.md` §6.2 | toggle "δ inert under a frozen random-projection encoder at this scale" (state it is the figure's toggle; the text home is §4.4) | P2 #6; R3 |
| 9 | **new** interaction-check figure | `08_interaction_check.md` | — (built after step 0.5; a "post hoc" mark; no verdict mark) | P2 #7, §4 |
| 7 | `simplex_secondary.html` (+ `.png`) | `07_example_results.md` §6.3, first | "knee" → change point; "no-element share" → fire-only share; `sweep_c50_p000` → the p = 0 sweep arm; caption names γ_p and γ_n's rows first (R6 fallback) | P2 #8, §5; R5–R6 |
| 8 | `ladder_registered_readings.html` (+ `.png`) | §6.3 | "rung" → step; "unit 1", "cross-unit" → GPU blocks (App. D); "floor basis" → floor-based standard error | P2 #9; R7 |
| C1 | `floors_explorer.html` | App. C | "M5.1e", "M5.5", "M6.0", "per card", "beat" (appendix: glossed in its caption) | P2 A2; R10 |
| E1 | `gamma_t_final_half.html` | App. E | "grid card", "post-unblind card", "single-card curve" | P2 A1; R9 |
| E2 | static `fig06_comms.png` | App. E | "E2C² handshake (M5.2)", "denial contrast (M5.5)", "the M5.5 bar" | P2 A3; R11 |
| H1, H2 | ISO / JOINT explorers | App. H | "obs v3" | v2 default kept (V3Q10) |

**Dropped:** the opening ladder (P2 §6); `fig05_coactive` (P2 §6 default:
the counter is one sentence in §3.5); slot versions and GIFs (by ruling,
FIGURE BATCH A2, A4, A5). **Numbering:** main-text figures 1–9 in reading
order (P2 numbered the interaction figure 7 because it placed it right after the design; with the check at §6.4 it is Figure 9), appendix figures by letter (C1, E1, E2, H1, H2). Iframe heights: the
v2 measured heights carry (P2 §9); Fig. 9's is measured when built.

**The new interaction figure (P2 §4)** is a new rendering of committed
artifacts (PR:146 item 4). It waits for the step-0.5 results **and their
commit** (rows must be read from committed files; the owner's commit ban is
in force, log:6236-6243). Until then `08_interaction_check.md` carries the
figure slot as a HOLE.

## 5. Listings

Main text: four short listings in §3 (B1 resolution: v2's 61-line step
listing costs about 0.8 printed page; the schematic and the claims table
carry the step order in the main text, and the full step moves to App. A).

| L | file:lines | proves | where |
|---|---|---|---|
| 1 | `che/env/structure.py:83-102` | Coupling A's uniforms are drawn before κ_A is read; seeding acts on c′ − c | §3.2 |
| 2 | `che/env/observation.py:300-310` | τ by Beer–Lambert; the reveal draw is unconditional | §3.2 |
| 3 | `che/env/tasks.py:31-43` | the task reward's signature admits food and occupancy only (hazard-blind) | §3.3 |
| 4 | `che/tests/test_coupling_b.py:131-142` | κ_B = 0 reproduces the pre-masking environment bitwise | §3.4 |
| 5 | `che/env/env.py:298-358` | one step in the Prop. 1 order | App. A |
| 6 | `che/train/ippo.py:323-329` | `stop_gradient`: the message encoder is frozen | App. B |

The stubs carry each block exactly as v2 carried it (LISTING line, header
line, byte-identical body; v2 BRIEF §0: 6 of 6 byte-identical).

## 6. Theory (V3-S6)

| statement | main text | appendix | from |
|---|---|---|---|
| Def. 1, Prop. 1 | §3.1, one sentence ("well-defined Dec-POMDP whose reachable states form a finite set") | App. A proof | P1 §5.4 |
| Def. 2 | §3.3 display (as v2) | — | v2 |
| Defs. 3 (fire, with its smoke update), 5, 6, 7 | §3.1–§3.2, one display each at most; Def. 4 in §4.1, Def. 8 in §6.2 | — | v2; P3 §2.2 (definitions move from v2 §5–§7 into §3) |
| Prop. 2, Cor. 1 | §3.1 (Prop. 2 one sentence), §4.1 (Cor. 1 in words) | App. A | P1 §5.4; Cor. 1(4) still v2 D2 |
| Prop. 3 | §3.2 in words; checked in two runs | App. A | P1 §5.4; v2 D3 still open |
| Thm. 1 | §3.2 in words only | App. A, statement per **V3Q5** (default: per-step optical depths D_t > 0, matching the implemented toy; content-channel sentence) | P3 §3.3; orchestrator note; B1 resolution §11 row 9 |
| Remark 1 | **cut** | — | V3-S6 |
| Prop. 4 | none (no "Proposition 4" in the main text) | **a remark in words, with its honesty note** (TF:636-643) | V3-S6 default; drop = V3Q3 |
| Remark 2′ | §4.4, one sentence presenting it as a refinement of Pynadath & Tambe (READS RULING item 4) | statement in App. A | B1 resolution §11 row 8; V3Q4 |

## 7. One home per caveat (V3-S5)

The machine-readable map, with detection patterns, is
`checks/caveats.yaml` (39 entries; B2's check counts them). Summary
(file → caveats homed there; "also" = short forms allowed):

| home | caveats (also allowed in) |
|---|---|
| `00_hero.md` | the hero is illustrative (also §4 renders) |
| `01_introduction.md` | one algorithm, one map, 12 agents, no baselines |
| `03_environment.md` | the counter is co-active only in all-on configurations; the death price is in effect a contact price; the hazard is not agent-independent |
| `04_calibration.md` | the ruled inert phrase with its bars (also abstract, §1); the inert label's asymmetry (also §1); the threshold's estimator provenance; the 4.8-fold fuel-limited fall (also §1); the High smoke cost descriptive, 3 of 3 (also §1); Coupling B at Medium against a three-seed spread (also §1, §6.1); Def. 4's prediction refuted for survival |
| `05_measurement.md` | a four-run floor's ±40 % |
| `06_example_design.md` | **sited where composition is weak** (also abstract, §1); the δ train/test mismatch (also §1); JOINT 3× ISO; the identity (also abstract, §6.5); 72 seeds a recorded deviation; the inert third a design error (also abstract, §1); matched compute (also abstract, §1, §6.5, §7); one evaluation draw (also §6.4's own list); bias (b) reverses sign on the grid GPU; the framing change (second home App. D) |
| `07_example_results.md` | secondary, non-verdict-bearing, not family-corrected (also abstract); "sign unstable over the final half" (also abstract, §1); the completion exclusion (also abstract, §1); "does not survive the inert-share correction" (also abstract, §1); JOINT 2× ISO-4; Γ₄ excludes only a large effect; B̂ without a test; Γ = Γ₄ + B̂ by construction; cross-GPU and the same-GPU replicate; realized completion power 71.6 % |
| `08_interaction_check.md` | what the check is blind to (the full list once); post hoc label required wherever the check appears (label rule, all files) |
| `09_example_lesson.md` | matching the active share cannot isolate co-occurrence (also abstract, §1) |
| `10_limitations.md` | no theorem that joint training wins |
| `11_using_che.md` | evaluation reproducibility (280 of 288) |
| `17_appendix_results.md` | the High readout's a-fortiori exclusion (also one sentence in §6.3) |

Where the plans differed on a home, §11 records the resolution.

## 8. The registration-timeline appendix (V3-S2)

`16_appendix_timeline.md` holds every date, ruling, provenance item, GPU
block, study code, seed and archive that leaves the main text. Its stub
lists each item with its source (P1 §6.2; v2 BRIEF §7; v2 App. D–F). In
short:

1. **Registration statement (V3-V2):** internal, version-controlled record;
   dates self-reported; the supplement carries the registration documents
   with a hash manifest; a public registry (OSF) next time. The full-history
   check of the 2026-08-13 commits is the owner's (this checkout is shallow;
   V3Q16).
2. **Dated events:** environment locks (DX-401, DX-402, V6-2); design
   registered with δ retained (V6-3); co-primaries (DES-12); outcome
   branches and falsifier (DES-12); plan amended (V6-5); bias identified
   pre-grid (V6-1); grid window (DES-12); bias and ISO-4 registered mid-grid,
   120 of 252 (DES-15); pre-unblind rulings and the fifth cell (DX-405,
   DX-102); unblinding (DES-12); secondary specification ratified (DX-413);
   same-GPU replicate proposed after Γ₄ (DES-15); the framing change
   (2026-10-12, row X4-5).
3. **Quotations, verbatim:** the frozen plan's reading rules; the outcome
   branches with the falsifier and its reading (RES-5); branch B's headline
   "no longer holds as worded"; "the branch label stays B".
4. **The seed rule's history** (DES-1–DES-6); **bias (b) in full** (DES-10,
   DES-11, V6-4).
5. **GPU blocks** (HW-4, DX-5, DX-30, DX-36): "GPU 1/2/3" appear here only.
6. **Study codes** with plain names (key table).
7. **Seeds and archives:** the floor seed never in the grid (DX-416); 615 of
   615 archive hashes (DX-408; v2 F1's 636 question open).
8. **Blinding:** one look per stage (DX-411); the inventory of
   outcome-derived quantities visible before unblinding — owner-attested
   only (V3Q19).
9. **The framing change** (V3-F5's second home).

## 9. Interaction-check holes

Marker: `<!-- HOLE:INTERACTION -->` on its own line, with a one-line
comment saying what fills it. Rows for the check come from step 0.5 as
`IC-<k>` in `paper/v3/ledger_proposals/IC.md` (orchestrator).

| file | what waits |
|---|---|
| `00_abstract.md` | the lesson sentence(s) (P1 §3.3 templates) |
| `01_introduction.md` | one sentence: the check's result in short form |
| `08_interaction_check.md` | the result paragraph; Figure 9 |
| `09_example_lesson.md` | the outcome-dependent half of the lesson (the identity half is written now) |
| `12_conclusion.md` | one clause |
| `19_appendix_interaction.md` | the per-arm table, floors, cross-GPU count, main effects |
| `front_matter.yaml` | `description` is rechecked against the final abstract |

If the results are not back in time, the abstract and §6.5 fall back to the
identity lesson (P1 §3.3, row "Not back in time"), and §6.4 states the check
as planned (V3Q7).

## 10. Owner-pending defaults (index; full list `DISPOSITIONS.md` §4)

Title (V3Q1, default P1's T1); page measure (V3Q2); Prop. 4 (V3Q3, default
appendix remark); Remark 2′ (V3Q4); Thm. 1 (V3Q5); check placement (V3Q6,
default §6.4); abstract lesson (V3Q7); figure rebuilds (V3Q8, default
glossed); Γ(t)/floors placement (V3Q9, default appendix); ISO/JOINT explorers
(V3Q10, default kept in App. H); print column (V3Q11, default kit);
points vs fractions (V3Q12, default text in points, glossed once per
figure); post hoc words in Fig. 9's caption (V3Q13, default yes); δ label
(V3Q14, default the ruled phrase with its bars beside it).

## 11. Conflicts between the plans, and the resolutions

| # | topic | P1 | P2 | P3 | resolution (and why) |
|---|---|---|---|---|---|
| 1 | page budget | 14.35 | ≤ 3.5 pages of figures | 13.75 | **14.25** (§3): between them; keeps 0.75 margin; P2's figure ceiling respected (≈ 2.4 at v2 sizes) |
| 2 | "Using CHE" section | §8 code, registration, reproducibility (0.5) | — | a separate usability section (0.5) | **merged** into one §8 (0.55): one home for API, run commands, supplement, registration statement, reproducibility |
| 3 | home of "sited where composition is weak" | §6.1, short form §1 | — | introduction | **§6.1 home, §1 short form** (P1): the full statement needs CB-9's grading, the registered text and the check's result, which sit with the example; §1 still states it first and as central (V3-F6) |
| 4 | home of the δ asymmetry and train/test mismatch | asymmetry §4.4 | — | both in §1 | **asymmetry §4.4** (its numbers live there), **mismatch §6.2** (the arms are described there); §1 carries one clause for both |
| 5 | home of the identity | §6.2 | — | the lesson | **§6.2** (P1): the plane, which leads §6.3, needs the identity first; §6.5 states the lesson ("cannot isolate co-occurrence") as its own home |
| 6 | V3-F3 size row | NEW N1 | — | DX-406 suffices | **new row X4-3** (P1 + orchestrator): DX-406's scope note limits it to the fire-death comparison (`ledger_supplement.md:100`) |
| 7 | dates in the main text | unblinding date only | — | registration + unblinding | **unblinding date only** (change list V3-S2: "the fact of registration") |
| 8 | Remark 2′ | out of the main text (App. A or drop) | — | owner question; V3-S6 silent | **§4.4 one sentence + App. A statement** (B1): READS RULING item 4 says the comms section presents it as a refinement of Pynadath & Tambe; moving it wholly out changes a ruling, so it is V3Q4 |
| 9 | Thm. 1 | keep only if V3-E2 confirms | appendix panel | mismatch found; state for general D_t | **main text in words only; App. A default = the general-D_t statement** (V3-E2 says "make the paper's statement match the code"), marked owner-pending because it departs from TF:375-394 (orchestrator: owner item); alternative = TF's statement with the mismatch stated, or cut (V3Q5) |
| 10 | Prop. 4 | lean drop | — | (appendix) | **appendix remark in words** (change-list default); drop = V3Q3 |
| 11 | interaction check placement | §6.4 after plane and Γ | right after the design | — | **§6.4** (P1; PAPER V3 2(c) puts the plane first in the results); P2's "after the design" = P1's alternative (end of §6.1), V3Q6 |
| 12 | Γ₄'s detection limit | optional (N3) | — | use it (BLIND W4) | **used, one clause in §6.3, row X4-4** (P3; V3-E3 anticipates it); not stated = V3Q18 |
| 13 | framing change in §1 | no | — | one sentence in §1 | **not in §1**: V3-F5 names its two homes (§6.1 and App. D) |
| 14 | step listing (v2 L1, 61 lines) | §3.1 "step order (Listing)" | listing + schematic | — | **moved to App. A** (B1, page budget); Fig. 2 and Table 2 carry the step order |
| 15 | `fig05_coactive` | — | goes unless the counter paragraph stays | — | **dropped**: the counter is one sentence in §3.5 |
| 16 | ISO/JOINT explorers | App. H (P2's call) | drop (recommended) | — | **kept in App. H** (v2 default; FIGURE BATCH A3 placed them); drop = V3Q10 |
| 17 | post hoc words in Fig. 9's caption | label everywhere | chip only? (owner) | — | **chip and the words "post hoc" in the caption** (PR:63-65 read literally; two words); V3Q13 |
| 18 | one-home of "secondary intervals not family-corrected" | §6.3 home but also listed in §7's contents | — | results | **§6.3 only**; §7 does not restate |
| 19 | conclusion | 0.25 page | — | none | **kept, 0.2 page** (a TMLR reader expects one; three sentences) |
| 20 | appendix I (search) | own appendix | — | — | **with J in one file** (`21_appendix_making.md`): both describe how the paper was made |
| 21 | page measure | from page 1 (front matter in) | — | owner question | **from page 1** (conservative) for B2's check; V3Q2 |

## 12. Interface extensions (recorded here; no v3 INTERFACE.md exists)

These follow v2's `INTERFACE.md` unless stated. B2 is asked to adopt them.

1. **Line 1 of every section file:**
   `<!-- PAPER V3 DRAFT (PAPER V3 ruling, 2026-10-12): builder-drafted, not owner-approved -->`
   (B2's `build_v3.py` still carries v2's line at the time of writing.)
2. **File list** as §2: `00_abstract.md`, `00_hero.md` first; `07_`–`09_`
   open with an H3 (continuing §6); `14_`–`21_` open with an H3 (continuing
   `## Appendices`). Main text = `00_*`–`12_*`.
3. **New-row IDs:** writers' rows are `X<n>-<k>` in
   `paper/v3/ledger_proposals/W<n>.md` (v2's `V<n>-<k>` would collide with
   v2 W3's `V3-1` and with the change-list codes V3-F1 …); interaction-check
   rows are `IC-<k>` in `paper/v3/ledger_proposals/IC.md`. Both match the
   build's ID pattern. The build must resolve IDs against the canonical
   ledger, `paper/v2/ledger_supplement.md`, `paper/v2/ledger_proposals/*.md`
   and `paper/v3/ledger_proposals/*.md`.
4. **Markers:** `<!-- HOLE:INTERACTION -->` (waits for step 0.5);
   `<!-- OWNER-PENDING:V3Qn -->` (text drafted on a default the owner has
   not ruled). The build should count both and report them, like STUB-SPEC
   blocks.
5. **Figure-label glosses** use the exact form `labelled “TERM” on the
   figure` inside the caption (the exemption in `checks/terms.txt`).
6. **Provenance** files are `paper/v3/provenance/<section file name>`, one
   row per sentence, with v2's columns and the change column reading
   "change from v2, and why" (v2 sentence reused / edited / new).
7. **Alternates** in `sections/alt/NN_slug.<variant>.md`, only where §10's
   owner choice has distinct text: `alt/13_appendix_proofs.thm1_tf.md`
   (V3Q5), `alt/13_appendix_proofs.no_prop4.md` (V3Q3).
