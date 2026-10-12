# STRUCTURE — the reconciled v2 structure (builder B1, step 3)

Written 2026-10-11 under PAPER V2 (`docs/decision_log.md:6036`) and its
amendment (`:6096`). It reconciles the three plans
(`plans/P1.md`, the argument; `plans/P2.md`, the Beyond PDF reading path;
`plans/P3.md`, the referee's view) and the step-2 review
(`review_of_demo.md`) into one structure, and says for each choice which
plan it came from and why. It contains no paper prose: fragments quoted
from the plans are theirs and are marked as such. Rules, facts and the
glossary are in `BRIEF.md`; the disposition of every finding is in
`FINDINGS.md`; each section's specification is in its stub.

---

## 1. How the plans were reconciled

- **Precedence.** The owner's rulings and the fix list first; then
  `INTERFACE.md` (the build contract); then the plans, each in its own lens:
  **P1 decides the order of the argument and where claims sit**, **P2 decides
  figure placement, kit mechanics and listings**, **P3 decides the word
  budget, the jargon cut and what a referee needs up front**. The review's
  Part 2 decisions are adopted where no plan contradicts them; where one
  does, §11 records the conflict and its resolution.
- **Default that needs no ruling.** Where a plan's proposal would change a
  ruling or needs an owner choice (class C, `FINDINGS.md`), the structure
  keeps the ruled or demo default and the proposal becomes an owner
  question; where the choice has distinct text, an alternate file is
  drafted (§9).
- **The orchestrator's policy on findings** (classes A, B, C) is applied
  row by row in `FINDINGS.md`.

---

## 2. The section list

The numbering is the demo's, unchanged: the opening ladder prints "full
ladder: §9.2" (`paper/figures/interactive/out/html/opening_ladder.html`,
read this session) and figures are not rebuilt this phase (P2 §0), so the
results stay at §9.2 and §2 stays after §1 (P1 §3 note; review R6). Moving
§2 after the results would renumber §9.2 and needs the owner (Q10). The only
structural changes: a new **§9.3** (the labelled recommendation, F4's
home, §5 below), App. G (throughput) folded into §11 so the later appendices
move up one letter, and the appendix split into three files for the writer
split (§10).

| file | heading (exact) | purpose (one sentence) | leading figure | ledger IDs that carry it | writer |
|---|---|---|---|---|---|
| `00_abstract.md` | *(none; body text before the hero)* | The test, its plain result with the registered strings, why the correction exists (owned as a design error), what the environment and protocol contribute, and one labelled recommendation. | — | RES-1, RES-2, RES-6, RES-7, RES-11–RES-13, DES-1, DES-3, DES-8, DES-13, DES-14, DES-15, CAL-3, ENV-1, CA-4 (optional) | W1 |
| `00_hero.md` | *(none)* | One random-policy episode of the environment before any claim, illustrative, grading nothing; plus a short reading note on the status labels. | Fig. 1 explorer | ENV-6, ENV-13, CAL-3, CA-1, CB-1, COM-6, DX-33 | W1 |
| `01_introduction.md` | `## 1 Introduction` | The question; why the hazard's placement keeps the comparison clean; the test and what it holds fixed; both weaknesses before the result (the 3× frequency and the inert third, owned); the result with its correction; what is not claimed; three contributions. | Fig. 2 composer, Fig. 3 opening ladder | ENV-1, ENV-11, CAL-3, DES-1, DES-3, DES-7, DES-8, DES-12–DES-15, V6-1, RES-1, RES-2, RES-5, RES-6, RES-7, RES-11–RES-13, CA-4, CA-6, CB-5, CB-10, METH-7, DX-9, DX-102 | W2 |
| `02_related_work.md` | `## 2 Related work` | For each line of work, where the hazard sits and what its comparisons hold fixed; priority to Gao et al. and DBCA; how the search ran. | Table 1 | ENV-1, ENV-6, DES-7, DES-14, CA-8, CA-9 (or a pointer to §5.1), DX-101 | W2 |
| `03_environment.md` | `## 3 The environment` | CHE is a well-defined Dec-POMDP, finite on its reachable states; its reward is hazard-blind and prices deaths cause-blind; the fire is a bond-percolation process; every ablation is an exact nested model; the one instance, training and metrics. | Fig. 4 schematic | ENV-1–ENV-12, DX-1–DX-3, DES-13, CA-8 | W3 |
| `04_severity.md` | `## 4 Severity calibration` | Severity is a measured dynamical phase; Cor. 1 at the level verified sources support; the measured threshold with its provenance; the locked levels; Def. 4's Medium prediction refuted for survival. | Fig. 5 severity explorer | CAL-1–CAL-5, DX-6–DX-8, DX-201–DX-204, CA-1, CB-1, COM-6, ENV-1, ENV-6 | W3 |
| `05_coupling_a.md` | `## 5 Coupling A: collapse seeds the fire` | Collapse seeds fire; agents influence it weakly (home of the numbers); Prop. 3's linear scaling holds in two separate runs; under trained policies the coupling limits itself at High, as the random-policy calibration had already shown. | Fig. 6 Coupling A explorer | CA-1–CA-9, DX-9, DX-10, DX-37, DX-40, DX-304, DX-401, CAL-3, CB-1 | W4 |
| `06_coupling_b.md` | `## 6 Coupling B: smoke attenuates perception` | Smoke attenuates perception by Beer–Lambert transmittance; Thm. 1 says why that matters in a toy; the cost is paid in survival at High (3/3) and was −0.03 points at Medium (home); the counter and what it can see. | pointer to Fig. 1's panels; Fig. 7 | CB-1–CB-10, CO-1–CO-4, DX-11–DX-14, DX-37, DX-40, DX-301, METH-1, DX-33 | W4 |
| `07_comms.md` | `## 7 Communication denial: inert under this encoder at this scale` | Denial is inert under a frozen random-projection encoder at this scale, by a two-part argument with stated limits; this is the premise of the correction, whose consequence §9.1 owns. | Fig. 9 | COM-1–COM-6, ENV-1, ENV-6, ENV-11, ENV-12, DX-16, DX-17, DX-305, DES-8 | W4 |
| `08_methodology.md` | `## 8 Methodology: bars come with floors` | The measurement rules §9 uses, each with the exhibit that produced it, and where this paper falls short of them. | Fig. 10 floors explorer | METH-1–METH-7, DX-21, DX-32, DX-34, DX-38, DX-302, DX-303, COM-5, CB-7, CB-9, DES-13 | W5 |
| `09_compositional_test.md` | `## 9 The pre-registered compositional test` with `### 9.1 Design`, `### 9.2 Results`, `### 9.3 A recommendation and its scope` | 9.1: the estimand, the arms, the statistics, how k reached 72, the endpoint confound and the secondary design, **the design error (F3 home)**, bias (b), the registered readings, blinding. 9.2: the registered readings in order. 9.3: the one labelled recommendation (F4 home). | Fig. 11 ladder; Fig. 12 Γ(t); Fig. 13 simplex | DES-1–DES-16, RES-1–RES-15, SEC-1–SEC-7, HW-1–HW-4, DX-2, DX-3, DX-5, DX-18–DX-31, DX-39, DX-405, DX-406, DX-411, DX-416, V6-1–V6-3, METH-6, METH-7 | W6 |
| `10_limitations.md` | `## 10 Limitations` | Every branch-invariant limitation in the registered order (Medium siting first), then what the record adds, split into what was registered before the outcome and what was found after; pointers, not restated numbers. | — | CB-9, CB-5, CB-6, CA-4, CAL-3, ENV-1, ENV-2, ENV-6, ENV-7, ENV-9, ENV-11, ENV-12, DX-1, DX-2, DX-5, DX-30, DX-32, DES-13, HW-4 | W5 |
| `11_reproducibility.md` | `## 11 Reproducibility` | What a reader can re-run and check without a link; what is exact (ablations, evaluation: home of HW-2 and HW-3) and what is not (GPU training); the cost of a run and the throughput statement (old App. G). | — | HW-2, HW-3, DX-2–DX-5, DX-407, DX-408 | W5 |
| `12_appendix.md` | `## Appendices`, then `### A Proofs` | The appendix index (one line per appendix, replacing §11's list) and the proofs, each stated once (statements stay in the body). | — | DX-15, DX-409, CAL-3 | W6 |
| `13_appendix_locks_floors.md` | `### B Locks and hyperparameters`, `### C Floors` | Every locked constant with its ruling date, the hyperparameters and budget; every floor with its GPU, run length, artifact and reps, and the key to study codes. | — | CAL-1, CAL-3, CA-1, CB-1, COM-6, ENV-1, DX-1, DX-2, DX-3, DX-401–DX-403, DX-412, DES-1–DES-5, DES-10, DES-13, METH-1, METH-2, DX-34, DX-35, DX-36, CB-7, COM-5, HW-2 | W5 |
| `14_appendix_plan_provenance.md` | `### D The frozen analysis plan`, `### E The registered outcome branches`, `### F Grid provenance`, `### G Gamma over the final half of training`, `### H The secondary design`, `### I Trained-policy episodes` | The registered rules verbatim with dates; the branches; runs, seeds, GPU blocks and archives; the Γ(t) tables; the secondary design in full; two trained-policy episodes, shown separately. | Figs. I1, I2 | DES-9–DES-13, DES-15, DX-24–DX-30, DX-36, DX-39, DX-405, DX-408, DX-410, DX-413, DX-414, DX-416, RES-1, RES-2, RES-6–RES-9, RES-11–RES-13, RES-15, SEC-1–SEC-7, HW-3, HW-4, ENV-13 | W6 |

**Appendix letters, demo → v2:** A, B, C, D, E, F unchanged; demo G
(throughput) → folded into §11; demo H (Γ(t)) → **G**; demo I (secondary)
→ **H**; demo J (trained-policy episodes) → **I**, with Figures J1, J2 →
**I1, I2**. Source: P1 §8b, P2 §6.1 and the review's App. G decision all
fold G into §11; the re-lettering keeps the appendix contiguous. The
explorers print no figure or appendix letter (checked by grep, this
session).

---

## 3. Title candidates (F1)

Constraints (P1 §1; review F1; P2 §3): the hazard-blind reward does not
lead (PAPER V2 item 3); "multi-agent", not "swarm"; "stressor" for the
elements; "pre-registered" attaches to the 2026-08-13 test only (DES-12),
never to the correction (DES-15); nothing implies a composition effect; one
line, no `"`, no backslash, no `<` or `&`; a `: ` needs YAML single quotes
(B2 checks); the environment is named only if the owner chooses. Length:
P2-7 measured that the current title (138 characters) fills the first
1280 × 800 screen; about 75 characters or fewer keeps three lines (preview
estimate). Every candidate below is longer than that, so W1 also proposes
shortened forms of the owner's preferred lead. Lengths below were counted
this session.

The candidates are the planners' and the reviewer's, reconciled; W1 refines
them into the 3–5 the owner sees (in `provenance/00_abstract.md`), each with
its note and support, and puts the recommended one in `front_matter.yaml`.

| # | candidate (from) | leads with | note |
|---|---|---|---|
| T1 | *A pre-registered test of training on co-occurring versus isolated stressors in a multi-agent fire environment* (P1 T1) | the test | no result; the smallest amendment to the ratified title (log:5620-5621); 109 characters |
| T2 | *Training on co-occurring versus isolated stressors in a multi-agent fire environment, a pre-registered test whose survival gain does not survive the inert-share correction* (P1 T2, P1's recommendation; review candidate 2 is the same lead) | the question, then the plain result with the registered string | matches F2; never shows the gain without its qualifier (the analogue of FIGURE BATCH A1); omits completion and the Γ(t) suffix (Q3); 171 characters |
| T3 | *A multi-agent fire environment in which collapse seeds fire and smoke attenuates perception, and a pre-registered test of training on co-occurring versus isolated stressors* (P1 T3) | the environment's two couplings | no result; no comms; 172 characters |
| T4 | *A pre-registered test of joint versus isolated training on co-occurring stressors, in a multi-agent environment with an ambient fire hazard* (review candidate 1) | the test, with the ruled term "ambient" | no result; 139 characters |
| T5 | *A third of isolated training without an active stressor, and a pre-registered test of training on co-occurring versus isolated stressors in a multi-agent fire environment* (P1 T4) | the design error (F3) as the lesson | honest, but may read as if the error were the main finding, and loses the encoder scope (Q3); 170 characters |

Rejected, with the plans' reasons: a lead on "matching the active share"
(reads as a conclusion, F4; P1, review candidate 3); "exposure, not
composition" (unqualified "exposure", `branch_B.md:225-226`); "… accounts
for the survival gain" (B̂ has no verdict; two quantities move, DES-14); a
lead on the matched-marginal sweep (non-verdict-bearing; resolved nothing);
a question title (P1); "a pre-registered null" (undersells completion's
exclusion; review candidate 4).

---

## 4. The abstract's spine (F2)

From P1 §2 (the moves), checked against P3 §1.2 and §2 (what a referee needs
at abstract level) and the review's F2 must-keep list. Order is the
owner's F2 order (`paper_v2_prompt.md:160-167`). **Budget: ≤ 360 words and
≤ 2,600 characters, comments excluded** (the owner's text: 359 words and
2,424 characters; venue limit 5,000, ABSTRACT item 4). P3 proposed ≤ 300
words; the v2 abstract must carry more mandatory content than the owner's
(both registered strings verbatim, the exclusion bound, the design-error
clause), so the budget stays at the owner's length.

1. **What was tested** (one or two sentences): in a multi-agent fire
   environment (CHE, named: Q4c), whether training one policy on
   co-occurring stressors (JOINT) beats training it on each in isolation
   (ISO), read at a held-out near-critical severity, **at matched
   compute**, on two co-primaries, Šidák-corrected; a pre-registered test;
   72 seeds per arm, above the registered cap of 60, a recorded deviation
   made before unblinding (plain words, not "seed ladder").
2. **What happened**, in this order (P1's ordering choice; the alternative
   puts the qualifier before the suffix and was rejected because "sign
   unstable" would then read as if it were about Γ₄):
   1. survival up, +0.96 points with its Šidák-corrected CI;
   2. completion: no detectable change, stated as an exclusion with its
      bound ("excludes a joint-training gain larger than 0.66 points");
   3. "sign unstable over the final half" on both co-primaries, verbatim,
      with the two shapes (survival gap opens only in the last fifth;
      completion leans negative from 70 %);
   4. the survival gain "does not survive the inert-share correction",
      verbatim, with "the", and "registered before unblinding" (never
      "pre-registered") if the registration is mentioned.

   No sentence between 1 and 4 characterizes the gain as composition.
3. **Why the correction exists** (not why the gain exists): δ inert under a
   frozen random-projection message encoder at this scale, so a third of
   ISO's training episodes carried no active stressor (fire-only); **one
   plain clause owning it as a design error** (§5); the 20-seed
   sensitivity arm ISO-4, outside the confirmatory family; ISO-4's survival
   0.98 points above ISO's stated as an estimate with no test (never
   "raises"), or omitted; Γ₄ −0.03 points with its CI; JOINT still sees each
   coupling twice as often and always in combination. Optional: the
   correction excludes a large composition effect, not every one (required
   in §1 and §9.2, optional here).
4. **What the environment and the method contribute:** pure JAX,
   multi-agent; CA fire every episode; Coupling A; Coupling B by
   Beer–Lambert transmittance; independent comms denial; the ambient hazard
   (no reward, cost or constraint channel reads it; deaths priced the same);
   severity relative to a measured percolation threshold; each stressor a
   parameter of one transition **or observation** kernel (N9), so ablations
   are bitwise-exact nested models; "we describe" a measurement protocol
   with floors per metric, per GPU and per artifact. The 4.8-fold
   calibration finding may stay, corrected (no "as predicted before
   measurement"), if the budget allows; otherwise it lives in §1 and §5
   (Q5).
5. **The labelled recommendation** (default): one sentence, after
   everything else, marked as a recommendation that this one environment
   motivates, with no "therefore"; the alternate omits it (Q6).

**Disclosure footnote:** a `<d-footnote>` at the end of the first sentence
(P2 §3; BRIEF §12).

**Must not appear:** "composition effect" without the qualifier;
"budget-robust", "converged", "at convergence"; "no effect" for
completion; "certified"; "swarm"; PBT; any untagged number; "as predicted
before measurement"; "therefore" before the recommendation; "finite
Dec-POMDP"; "one transition kernel"; "pre-registered" for the correction.

**`description`:** it restates the abstract's opening (DESCRIPTION item 3),
so with a new opening it changes (F2: "re-check `description` against the
new abstract"). One line, no `"`, no backslash, no `: `, no number. P1
option A (the test, no result) is the default direction; option B adds the
qualifier. The owner's line (`paper/finale.md:4`) is kept in W1's
provenance as the revert option (Q4d).

---

## 5. Where F3 (the design error) and F4 (the recommendation) sit

**F3** (P1 §4; P3 §2 item 1; review F3; O1). The record's timeline is in
`BRIEF.md` §7, with three pre-assigned rows (V6-1–V6-3).

| location | role | content |
|---|---|---|
| §9.1 | **home**: the full account, one paragraph | δ already found inert (2026-07-30) when the design was registered (2026-08-02); the design excluded δ from the sweeps for that reason yet gave ISO two δ-only components of six; identified by a review of the registered design on 2026-08-16, before the grid; the grid began on 2026-09-09 without the correction; registered with ISO-4 and its rule on 2026-09-18, mid-grid (120 of 252 runs) and before unblinding, on the owner's attestation; the direction (inflates Γ); the cross-GPU consequence and the same-GPU replicate. Retitled paragraph lead without "stated before the result" |
| §1 | two sentences | owned as a flaw in the design; identified before the grid (2026-08-16) and registered with its correction mid-grid, before unblinding (2026-09-18); pointer to §9.1 |
| abstract | one clause | owned plainly; dates optional |
| §7, last paragraph | neutral pointer | the δ-only third is fire-only; §9.1 states the consequence (no "registers and corrects") |
| §10 | one bullet under "what the record adds" | the confirmatory Γ carries a design error whose direction inflates it; the correction rests on a 20-seed sensitivity arm outside the family, on another GPU; the same-GPU replicate agrees; the branch label stays B; pointer to §9.1 |
| §9.2 | — | the demo's "A registered design caught it" is cut |

**F4** (P1 §5; P3 §2 "F4 placement"; review F4). **Home: §9.3, a short
subsection** headed `### 9.3 A recommendation and its scope`. Reason: P1
wanted one plainly headed final paragraph of §9.2; P3 wanted §10 or the end
of §9.2; a separate H3 satisfies both (labelled, apart from any sentence
that reads as a conclusion) without touching §9.2's number (printed on the
opening ladder). It holds: the confound's logic as a claim (a comparison
that leaves the active share free mixes it with composition; true by
construction, like the 3× marginal, ENDPOINT CONFOUND log:4549-4570); the
recommendation, labelled as one this single environment motivates; the
exclusion caveat by pointer (+0.63 > +0.47, §9.2). Elsewhere:

| location | v2 |
|---|---|
| abstract | one labelled sentence, no "therefore" (default); alternate without (Q6); scope wording is the owner's (P1 prefers "joint-versus-isolated comparisons" to "studies of compositional generalization") |
| §1 | the confound's logic may stay, with the search caveat; no imperative; "behind this result" goes; the contributions list C-env, C-cal and C-test only; at most a pointer "(§9.3)" |
| §2 | none |
| §10 | the one-environment scope limit, pointing to §9.3 |
| §9.2 | the demo's "Discussion. Match the active share …" paragraph is cut |

---

## 6. Word budget

Prose words, counted as P3 counted them (`plans/P3.md` §5: comments, code,
math, captions and tables excluded; markdown-it paragraphs and list items).
Tolerance ±10 % per section; the body total is a ceiling.

| part | demo (P3 count) | v2 target | change |
|---|---|---|---|
| abstract | 359 | ≤ 360 (≤ 2,600 characters) | restructured, not shorter (§4) |
| hero caption + notes | 152 | ≤ 100, plus a reading note ≤ 50 | −34 % |
| §1 | 1,391 | 950 | −32 % |
| §2 | 1,536 | 1,150 | −25 % |
| §3 | 2,391 | 1,600 | −33 % |
| §4 | 998 | 700 | −30 % |
| §5 | 1,307 | 850 | −35 % |
| §6 | 1,652 | 1,050 | −36 % |
| §7 | 1,295 | 800 | −38 % |
| §8 | 1,447 | 850 | −41 % |
| §9 | 3,103 | 2,100 (9.1 ≈ 900, 9.2 ≈ 1,050, 9.3 ≈ 150) | −32 % |
| §10 | 1,051 | 700 | −33 % |
| §11 | 473 | 300 | −37 % |
| **body, §1–§11** | **16,644** | **11,050** | **−34 %** |
| appendix (excluding verbatim quotations and tables) | 2,404 (2,902 with 498 of quotation) | 2,000, plus the quotations (about 500) kept | −17 % |
| captions and figure notes | 2,828 (2,299 + 529) | ≤ 1,500 (caps in §8) | −47 % |
| **all of it** (abstract + body + appendix with quotations + captions, hero included, + the reading note) | **≈ 22,700** (359 + 16,644 + 2,902 + 2,828) | **≈ 15,500** (360 + 11,050 + 2,500 + 1,500 + 50) | **≈ −32 %** |

Sources of the budget: P3 §5 targeted −41 % on the body (9,850); the
review's targets were the demo brief's upper bounds (≈ 14,500); P2 §8 gave
the caption caps. The v2 target sits between them because the v2 text
carries more required content than the demo in §1 (the owned design error,
Medium siting) and §9 (the full F3 account), and because §2's verified
characterizations cut less safely than repetition does. The cuts come from
repetition, process history and captions (P3 §5), never from an honesty
line or a registered string.

---

## 7. One home per result

Each result is stated in full once, at its **home**; elsewhere it appears
only as the abstract-level short form or as a pointer. Reconciled from P1
§8a, P2 §8, P3 §5 and the review's N16.

| result | home | short form kept in | pointer only (or cut) |
|---|---|---|---|
| Γ: survival REJECT, completion exclusion (RES-1, RES-2) | §9.2 table | abstract; §1; Fig. 3 caption (verdicts only) | §9.2 prose gives verdicts and the exclusion sentence, CIs by reference to the table; Fig. 11 caption repeats no verdict the table gives; §10 points |
| the correction: Γ₄, Γ₄′, B̂ (RES-6–RES-9) | §9.2 table | abstract (Γ₄; B̂ as an estimate or omitted); §1 | Fig. 11 caption; §10 points |
| the correction's two limits (+0.63 > +0.47; two quantities move, DES-14) | §9.2 | §1, one clause | §10 points; §9.3 points |
| Γ(t): "sign unstable over the final half" and the shapes (RES-11–RES-13) | §9.2, Fig. 12 | abstract, §1 | App. G holds the tables only; §10 points |
| k = 72 as a recorded deviation (DES-1–DES-3) | §9.1 (two sentences) | abstract, §1 (one clause each) | figure captions "k = 72 (§9.1)"; App. B and D hold the constants; §10 keeps one pointer line without numbers (Q7) |
| the arms' shares: per-coupling frequency, active share, fire-only share (DES-7, DES-8, DES-14, DES-16) | §9.1 arms table, and Fig. 2 | abstract, §1 (one sentence each) | Fig. 2 caption carries none of the numbers the figure prints; §2 keeps "three times" and "twice" as pointers |
| the δ design error (F3) | §9.1 | §1 (two sentences), abstract (one clause) | §7 and §10 point (§5 above) |
| the recommendation (F4) | §9.3 | abstract (one labelled sentence, default) | §1, §10 point |
| δ inert under the frozen encoder | §7 | abstract, §1, §9.1, §10 item 5 (the full phrase in §7, the abstract and §10 item 5; elsewhere "inert (§7)") | — |
| the 4.83× fuel-limited fall (CA-4, CA-5, DX-9) | §5.3 | abstract (Q5), §1 contribution 2 | §9.2's High readout and §10 item 1 say "(§5.3)" |
| agents' influence on collapse (CA-8, CA-9) | §5.1 | — | §2 and §3.3: one clause and a pointer (OWNER ITEM 4 resolves at the home) |
| Coupling B at Medium, −0.03 points (CB-9) | §6.4 | §10 item 1 (the registered limitation keeps its numbers) | §1: a limitation clause, no number; §8.6: pointer |
| Coupling B at High, 3/3 (CB-5) | §6.4 | §1 contribution 2; §10 item 1 | §9.2's High readout points |
| the d_p ablation and the penalized-vs-rewarded channel (ENV-1–ENV-5) | §3.3 | §1, §9.2, §10 item 4 (one clause each) | §7 one clause (Remark 2′'s qualifier) |
| seed dispersion over the floor; 5.40× (HW-1, DX-21) | §9.2 | — | §8.4 states the rule and points |
| evaluation reproducibility (HW-2, HW-3) | §11 | — | §9.2 one clause, pointer; App. G one clause |
| GPU blocks (HW-4, DX-5, DX-30) | App. F | §9.2 and §10 item 8 (one sentence each; honesty line 8 requires both) | figures print "cross-unit" |
| blinding and one look per stage (DX-411, DX-416) | §9.1 (three sentences) | — | §11 and App. F point |
| registered reading rules, quoted | App. D (verbatim) | §9.1: the ISO-4 rule only, quoted | §9.1's demo three-row table becomes one-line rules with a pointer |
| Prop. 1's proof | App. A | §3.1 one-sentence gloss | — |
| Thm. 1's proof | App. A | — | §6.2 keeps the statement only |
| Prop. 2's implementation exactness | App. A | §3.2 one sentence | — |
| Props. 3, 4, Thm. 1, Remark 2′ statements | body (§5, §9.1, §6, §7) | — | App. A gives proofs only ("Statement: §n") |
| Prop. 4's honesty note | §9.1 | §1, one clause | App. A and §10 point |
| floors, every one | App. C | §8 states each rule with one exhibit | — |
| the hazard-blind vs hazard-priced contrast | §3.3 | — | §2's Table 1 and one sentence |
| the endpoint confound and DBCA (DES-7, `keysers2020`) | §9.1 | §1 (one sentence) | §2 points |
| appendix list | App. index (top of `12_appendix.md`) | — | §11's list is cut |

---

## 8. Figures, captions, listings and LaTeX

**Figures** (P2 §2): the demo's fifteen, in the demo's places, numbered as
in `BRIEF.md` §16. Not used, by ruling: the slot versions, every GIF, deep
links (A2, A4–A6). The hero stays the explorer by default (§9). The simplex
stays in §9.2 (A1's adopted path; moving it to App. H is Q9). Fig. 8 stays
in §6 (FIGURE BATCH A2's slot; P2 proposed moving it to the appendix: Q22).

**Caption caps** (P2 R2, tightened to P3's total; figure notes included):
hero ≤ 100; Fig. 2 ≤ 100; Fig. 3 ≤ 120; Fig. 4 ≤ 80; Fig. 5 ≤ 120;
Fig. 6 ≤ 120; Figs. 7, 8, 9 ≤ 80 each; Fig. 10 ≤ 120; Fig. 11 ≤ 130;
Fig. 12 ≤ 120; Fig. 13 ≤ 130; Figs. I1, I2 ≤ 60 each. Total ≤ 1,500.

**Caption rules** (P2 R1–R3 with P3 §6): (R1) the status, the interaction,
the registered string where one applies, and one specific "cannot show"
clause; (R2) the caps above; (R3) a number the figure prints is not
repeated in its caption; (R4, P3) the status vocabulary ("illustrative",
"registered", "sensitivity arm", "secondary", "descriptive", "reference
scale (cross-artifact)") is explained once in a reading note under the
hero, so each caption carries a status tag of about 12 words or fewer; (R5)
each caption glosses once any jargon its figure prints (`BRIEF.md` §5.2).

**Listings** (P2 §4): six, two shortened (`BRIEF.md` §16); the stubs carry
the exact blocks, each with the header line `# <path>:<start>-<end>
(verbatim)` as the fence's first line (P2's form, which B2's build accepts
and strips before its byte-identity check).

**LaTeX** (P2 §5.1, with C1–C3 applied): about twelve body displays.

| statement | v2 body | v2 appendix |
|---|---|---|
| Def. 1 (state; factorized kernel; post-step observation) | keep (2 displays) | — |
| Prop. 1 | statement and a one-sentence gloss (finite on reachable states) | the proof, once |
| Remark 1 | softened (C2), no LaTeX | — |
| Def. 2 | keep (1 display) | — |
| Def. 3, smoke update | keep (1 display) | — |
| Prop. 2 | statement | proof; the implementation-exactness paragraph |
| Cor. 1 | (1) with `kesten1980`; (2) only at a verified level; (3) dropped; (4) at the verified level with `garet2004chemical` (alternate: dropped) | — |
| Def. 4 | short list, with the operational definition by locked bands | — |
| Def. 5 | keep (1 display) | — |
| Prop. 3 | the linear-scaling statement (1 display), no 43/18 rate, no divergence claim on the arena | proof; the finite-protocol details |
| Def. 6 | keep (1 display) | — |
| Thm. 1 | statement with the q display, what it buys, the gate | the proof |
| Def. 7 | keep (1 display) | — |
| Remark 2′ | full statement with the VoC display (READS RULING item 4: §7 presents it) | the extra step; the toy's constants (DX-15) |
| §8 contrast SE and MDE₈₀ | keep (2 displays), the contrast SE in the unequal-k form §9 uses | — |
| Def. 8 | keep (1 display) | — |
| §9.1 estimator display | cut; point to §8.2 | — |
| Prop. 4 | renamed; stated in words with the honesty note; **no display** (the constant and the per-agent max are unverified: N6, P3-N7) | the proof idea without a constant; the ε_min > 0 argument |

No `\label`, `\eqref`, `\tag` or `\newcommand` (no cross-reference route in
the kit).

---

## 9. Alternates, and the hero option

Owner choices with distinct text get an alternate in `sections/alt/`,
drafted by the section's writer (INTERFACE layout):

| file | writer | choice | default it replaces | owner question |
|---|---|---|---|---|
| `alt/00_abstract.disclosure_line.md` | W1 | a visible first-page disclosure line (with or without the `<d-footnote>`) | the `<d-footnote>` alone | Q4f |
| `alt/00_abstract.no_recommendation.md` | W1 | the abstract without the labelled recommendation | one labelled sentence | Q6 |
| `alt/00_hero.ladder.md` | W1 | the opening ladder as the hero (P2 option B) | the explorer (OPENING item 2) | Q8 |
| `alt/04_severity.no_item4.md` | W3 | Cor. 1 without item (4) | (4) with `garet2004chemical` | Q4g |
| `alt/11_reproducibility.supplement.md` | W5 | §11 describing an anonymized code supplement | §11 describing what exists, promising nothing | Q4e |

**The hero option B, as a full page** needs more than one file swap: the
opening-ladder block moves from §1 to the hero slot, the explorer block
moves to the head of §3, and Figures 1 and 3 swap numbers throughout (every
other number is unchanged: the order becomes ladder 1, composer 2,
explorer 3, schematic 4). **Request to B2 (recorded here, B2's to accept):**
a build flag that performs this block move and the 1 ↔ 3 renumbering
mechanically. To make it possible, every writer keeps figure blocks
self-contained and movable and refers to figures by number only
(`BRIEF.md` §14). W1's alternate supplies the hero-position caption.

---

## 10. Writer assignments

The default split, adapted in one place, with the reason:

| writer | files | budget (prose) | notes |
|---|---|---|---|
| **W1** | `00_abstract.md`, `00_hero.md`; `front_matter.yaml` (`title`, `description`); the disclosure `<d-footnote>`; `alt/00_abstract.disclosure_line.md`, `alt/00_abstract.no_recommendation.md`, `alt/00_hero.ladder.md`; `provenance/00_abstract.md` (with the title candidates and `description`), `provenance/00_hero.md` | ≈ 510 + captions | title candidates per §3 |
| **W2** | `01_introduction.md`, `02_related_work.md` | 2,100 | §1 depends on W6's F3 rows (V6-1) |
| **W3** | `03_environment.md`, `04_severity.md`; `alt/04_severity.no_item4.md` | 2,300 | Listings 1–3 |
| **W4** | `05_coupling_a.md`, `06_coupling_b.md`, `07_comms.md` | 2,700 | Listings 4–6 |
| **W5** | `08_methodology.md`, `10_limitations.md`, `11_reproducibility.md`, **`13_appendix_locks_floors.md` (App. B, C)**; `alt/11_reproducibility.supplement.md` | ≈ 2,200 | |
| **W6** | `09_compositional_test.md`, `12_appendix.md` (index, App. A), `14_appendix_plan_provenance.md` (App. D–I); `ledger_proposals/W6.md` with V6-1–V6-3 | ≈ 3,750 | the heaviest file set |

**The adaptation:** App. B (locks) and App. C (floors) move from W6 to W5,
in their own file. Reasons: W6's default load (§9 at 2,100 words with every
registered string, plus ≈ 2,000 appendix words, two Γ(t) tables and five
captions) was about twice any other writer's; and App. C is the home of the
floor exhibits whose rules W5 writes in §8, so the rules and their data stay
with one writer. Keeping the appendix contiguous (A–I in order) needs three
files (`12_`, `13_`, `14_`); `13_` and `14_` open with an H3, not an H2, by
design (they continue `## Appendices`).

**Dependencies and order.** The writers work in parallel; these
cross-section facts are fixed in `BRIEF.md` so nobody waits:
- the F3 facts and the IDs V6-1–V6-3 (`BRIEF.md` §7): W6 writes the rows;
  W1, W2 and W5 cite them;
- the figure and listing numbers (`BRIEF.md` §16) and the appendix letters
  (§2 above);
- the plain names (`BRIEF.md` §5.2): Γ₄′'s plain name is defined in §9.2
  by W6, Γ₄'s at first use in §1 by W2 and again in §9.2;
- §1 promises that §9.2 reports γ_n and where the plane fit fails (§1
  INTRODUCTION item 3): W6 delivers it;
- §2 relies on §1 stating what the comparison holds fixed and the 3×
  frequency (W2 owns both);
- §10 item 1 (W5) carries the Medium siting that §1 (W2) points to, and
  §6.4 (W4) holds the measurement.

---

## 11. Conflicts between the plans, and the resolutions

| # | topic | P1 | P2 | P3 | review | resolution (and why) |
|---|---|---|---|---|---|---|
| 1 | hero | — | opening ladder under the abstract, explorer leads §3 (as an owner question) | — | keep the explorer | **explorer** (ruled, OPENING item 2); option B drafted as an alternate with a build-flag request (§9); Q8 |
| 2 | abstract length | 2,400–2,800 characters | — | ≤ 300 words | — | **≤ 360 words, ≤ 2,600 characters** (§4: more required content than the owner's) |
| 3 | 4.8-fold finding in the abstract | keep corrected, or move to §1 (Q) | — | move to §1 | — | keep corrected if within budget; W1's call, recorded in provenance; Q5 |
| 4 | recommendation's home | final paragraph of §9.2 | — | §10 or end of §9.2 | §9.2 or a discussion | **§9.3**, a short labelled subsection (§5) |
| 5 | recommendation in the abstract | optional, labelled | — | "one environment" beside it | — | **one labelled sentence** (closest to the owner's abstract and F4's direction); alternate without; Q6 |
| 6 | Prop. 4 | rename; keep in §9.1 with the honesty note | name and honesty note in the body; display and proof in App. A | rename, then demote or drop (Q) | keep renamed in §9.1 or move to App. A; drop the ISO-vs-JOINT contrast | **§9.1 in words, renamed, with the honesty note; no display anywhere** (the orchestrator's C3 rule: nothing N6 or P3 show wrong); App. A gives the proof idea; Q4i |
| 7 | Cor. 1 | (1) plus the universal divergence; drop (3), (4) | (1), (2) in the body; (3), (4) in the appendix only if verified | drop exponents; drop (4) unless verified | drop (3); state (4) with `garet2004chemical` | **as directed by the orchestrator**: drop (3) and Prop. 3's rate; (4) at the verified level (alternate: drop); (2) and the "universal" caveat only at a verified level (N7), so by default the caveat is cut and the measured-threshold sentence kept; Q4g |
| 8 | word budget | — | caption caps | −41 % body | the demo brief's upper bounds | **−34 % body**, captions −47 % (§6) |
| 9 | "no-coupling sweep arm" (the prompt's F5 example) | — | (used it in the label glossary) | misdescribes the arm (N18) | used it | **"the p = 0 sweep arm, which trains on ISO-4's mixture on JOINT's GPU"** (accuracy; class B); Q17 |
| 10 | cross-reference tokens | — | `[[fig:…]]` tokens numbered by the build | — | — | **plain text** (INTERFACE "Cross-references"); B2's build lists targets; the hero alternate uses a build flag instead (§9) |
| 11 | listing header line inside the fence | — | keep `# path:range (verbatim)` as line 1 | — | — | **keep the header line** (P2): INTERFACE asks for a byte-identical fence body, and B2's build extends that check to accept one matching header line (`src/build_v2.py`, listing check), so the printed listing names its source |
| 12 | Fig. 8 (co-active) | — | move to a new appendix | — | keep in §6 | **keep in §6** (stable numbering for parallel writers; FIGURE BATCH A2's slot); Q22 |
| 13 | §2's position | after §1 | constrained by "full ladder: §9.2" | — | keep after §1 (R6) | **after §1**; Q10 |
| 14 | Medium siting in §1 | via a pointer in §1's weaknesses paragraph | — | required in §1 | in §10 | **one clause in §1** pointing to §10 item 1 (registered as branch-invariant, `phase6_framing_branches.md:245-261`); the measurement's home is §6.4; Q21 confirms |
| 15 | CB-9 in §1's contributions | drop the number (it is a limitation) | — | Medium siting up front | — | contribution 2 drops CB-9's number; the limitation clause carries Medium siting without a number |
| 16 | bias (b) | keep in §8 and §9.1 | — | §9.1 once, a §1 clause, cut the §8 copy | keep three readings in §8 | **§9.1 home** with all readings; §8.5 states the rule and points; not in §1 by default (Q21) |
| 17 | §8's exhibits | each rule with its exhibit; numbers to App. C | — | exhibits to App. C, one sentence left | keep each rule with its exhibit | each rule with a **one-sentence** exhibit; the exhibits' details in App. C; §8.6 whole |
| 18 | k = 72 bullet in §10 | cut as a restatement (Q) | — | — | keep the "recorded deviation" item | **keep one pointer line, no numbers**; Q7 |
| 19 | App. G (throughput) | one line in §11 | one line in §11 | folded in | fold into §11 or F | **folded into §11**; appendices re-lettered (§2) |
| 20 | Thm. 1 in the body | — | two or three plain sentences and the display | Chen et al. detail beside Thm. 1 in App. A | keep the statement, proof to App. A | **keep the formal statement** in §6.2 (trimming a theorem's statement risks error), proof only in App. A |
| 21 | Remark 2′ | keep in §7 (READS RULING) | conditional lesson in words in the body, full statement in App. A | — | keep as a refinement of Pynadath & Tambe | **full statement in §7** (READS RULING item 4); toy constants to App. A |
| 22 | caption convention | — | R1–R3 | one reading note at the first figure; status ≤ 12 words | trim captions | **both** (§8): the reading note goes under the hero (W1) |
| 23 | presentation fixes (iframe heights, figure widths, print order, "Interact" hidden in print) | — | apply (builder decisions) | — | — | **not applied** by default (new mechanical findings: PAPER V2 item 4 says report before fixing); Q22 proposes applying them |
| 24 | δ timeline | found pre-grid, registered mid-grid | — | the same | the same | **the record's timeline** (class B under O1); wording Q4h |
| 25 | the appendix's writer | — | — | — | — | default split adapted: App. B, C to W5 (§10) |

---

## 12. Owner questions (index)

The full list, with the facts behind each, is in `FINDINGS.md` §3. The
review's numbering is kept (Q1–Q4l); the plans' questions are consolidated
as Q5–Q25. Structural ones: Q3 (title), Q4d (`description`), Q5 (4.8-fold
in the abstract), Q6 (recommendation in the abstract), Q7 (§10 pointer
lines), Q8 (hero), Q9 (simplex), Q10 (§2's position), Q12 (App. I), Q20
(length), Q21 (up-front limitations in §1), Q22 (presentation fixes).

---

## 13. Extensions to `INTERFACE.md` (recorded here, per its rule)

1. **Three appendix files** (`12_appendix.md`, `13_appendix_locks_floors.md`,
   `14_appendix_plan_provenance.md`), assembled in filename order; `13_` and
   `14_` open with an H3 (they continue `## Appendices`) and carry their
   STUB-SPEC after the first H3.
2. **A new H3, `### 9.3 A recommendation and its scope`**, inside §9 (not in
   the `toc`).
3. **Pre-assigned ledger-proposal IDs V6-1–V6-3** (W6's file), cited by
   W1, W2 and W5 before W6 writes them (`BRIEF.md` §7).
4. **Figure-block markup carried from the demo** inside the stubs, each
   preceded by a comment "carried from demo …, writer checks caption".
5. **Listings pasted into the stubs** with their `LISTING` lines, the
   header line B2's build accepts, and the exact lines of the committed
   files.
6. **The hero option B** needs a B2 build flag (block move and figure
   1 ↔ 3 renumbering), requested in §9; until B2 accepts it, only W1's
   `alt/00_hero.ladder.md` exists.
7. **W1's provenance file** also carries the title candidates and the
   `description` (`BRIEF.md` §13).
