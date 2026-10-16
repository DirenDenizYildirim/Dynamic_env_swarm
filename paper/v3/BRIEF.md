# BRIEF — Paper v3, for the step-4 writers (W1–W5)

Builder B1, step 3 of Paper v3, 2026-10-14, under **PAPER V3**
(`docs/decision_log.md:6115`) and **PAPER V3 PHASE 1 START** (log:6218). It
carries v2's brief (`paper/v2/BRIEF.md`, "v2 BRIEF") and re-verifies only
what v3 changes (§0). Where a v2 section binds unchanged, this brief says
so and points to it; read it there. §6 (registered strings) and §7 (the F3
timeline) are copied **verbatim** from v2 BRIEF, followed by v3 landing
tables. New in v3: the change list with an owner per item (§3), the
extended glossary (§5.2), the environment claims table (§8.1), the record
corrections as traps (§9.2) and the style hazards (§9.4).

**How to use it.** Read this file, then your stubs (`sections/NN_*.md`, each
with a `STUB-SPEC`), then your rows in `WRITERS.md` and `STRUCTURE.md` §2,
and the `DISPOSITIONS.md` rows your stub names. Abbreviations: `log` =
`docs/decision_log.md`; `TF` = `docs/theory_foundations.md`; `PR` =
`paper_v3_prompt.md`; `PFB` = `phase6_framing_branches.md`; `BR` =
`paper/v2/review/blind_review.md`; `R/` = `che/bench/results/`; `P6/` =
`R/phase6/`; `RWV` = `paper/related_work_verification.md`; `PLAN` =
`P6/post_v3_interaction/PLAN.md`.

---

## 0. What was re-verified (2026-10-14, this session), and what was not

| what | how | result |
|---|---|---|
| PAPER V3 and PAPER V3 PHASE 1 START | read in full, log:6115-6244 | items cited below by number |
| the change list and the rules | `PR:111-299`, read in full | binding as written; §2–§3 |
| training δ per arm (new caveat) | `che/configs/p6_iso.yaml:41-46` (A-only and B-only components δ 0.0; δ-only components δ 1.0), `p6_iso4.yaml:36-39` (all four components δ 0.0), `p6_joint.yaml:36-37` (δ 1.0), `theta_star_holdout.yaml:76` (δ 1.0) | match the orchestrator's note and P1 §10 item 6, P3 §1.4 |
| the size in agents (V3-F3) | `paper/v2/ledger_supplement.md:100` (DX-406, its scope note: "Used only to set the fire-death contrast … beside the survival gap"); `P6/unblind/unblind.json:61` ("gamma": 0.009553128646479725) | the arithmetic exists; its scope does not cover the size statement → new row X4-3 (§10) |
| Γ₄'s and B̂'s survival detection limits | `P6/post_unblind_analysis/post_gamma4_t2000.md:15-16`, last column 0.0090 and 0.0089 | as P3 quoted; no row yet → X4-4 |
| Thm. 1's measured vs predicted at κ_B = 8 | `R/phase4/phase4_report.md:72` (0.5000 ± 0.0055 measured, 0.5028 predicted, z −0.51) | as P3 said; BR's "J\* − ½ = 0.0000" reading is wrong → X2-1 |
| the registered texts the example quotes | `PFB:102` (branch B headline), `:188-195` (the X sentence), `:245-260` (Medium siting, "Required on A, B and C alike") | match the plans |
| TF lines the plans cite | `TF:636-643` (Prop. 4 honesty note, "must appear in the paper"), `TF:686` ("No theorem that joint training wins") | match |
| ledger rows quoted in this brief | read at `paper/numbers_ledger.md` (ENV-6, CB-9, COM-4, DES-7, DES-12, DES-13, DES-14, RES-12, SUP-1, SUP-2) and `paper/v2/ledger_supplement.md` (DX-11, DX-14, DX-406); the proposal files `paper/v2/ledger_proposals/W3–W6.md` (row IDs listed) | as written |
| the interaction-check plan | `PLAN` read in full (§1–§9) | the reading rules in §8.3 below are PLAN §7's |

**Not re-verified (carried from v2 BRIEF, which records its own
verification, v2 BRIEF §0):** every other ledger row's source line; v2's
rulings table (v2 BRIEF §4); the kit facts (v2 BRIEF §14, now exercised by
v2's real-kit build); citation permitted uses (v2 BRIEF §15). TMLR's pages
were read by P3 only through a summarizing fetch tool (P3 §0): **no TMLR
quotation enters the paper until someone re-reads the page directly and the
reading is transcribed** (V3Q24).

---

## 1. Roles (PAPER V3) and how step 4 runs

- **Builders draft; the owner checks every word and is responsible**
  (PR:43-65; PAPER V2 item 1 carries). Nothing enters `paper/finale.md` or
  the submission until the owner approves it.
- **No commits or pushes until the owner names the branch** (log:6236-6243).
  No GPU (log:6241). No training. Only the eval-only interaction check is
  authorized, at θ\* only (log:6226-6235), and the owner runs it.
- **Your files:** the section files and alternates your `WRITERS.md` row
  names; `paper/v3/provenance/<same file name>` for each; your
  `paper/v3/ledger_proposals/W<n>.md` for new rows. Edit nothing else: not
  another writer's file, this brief, `STRUCTURE.md`, `DISPOSITIONS.md`,
  `checks/`, the ledgers, `RWV`, the bibliography, `src/`, `paper/v2/`,
  `CLAUDE.md`, `docs/`, registered documents, configs or code.
- **Step 4:** writers in parallel → reviewers in lanes (claims ×2, numbers
  ×2, mechanics) writing to `paper/v3/review/` → writers fix their own
  files, reviewers re-check changed lines against a snapshot → outcomes in
  `paper/v3/REVIEW.md` → the real-kit build with all checks green. Step 4.5:
  the owner and one blind reviewer in a separate session.
- **A finding you make while writing:** record it in your provenance file's
  "Findings" list and your hand-back; apply it only if it is a standing-rule
  fix (v2 BRIEF §1, class B), with the original wording kept so the owner
  can revert.

---

## 2. Rules that bind every agent

Read them verbatim at `PR:111-172` ("Rules that bind every agent"). The
deltas from v2 BRIEF §2:

- registered strings: the v3 list (`PR:118-124`) says bias (b) "reverses sign
  on the grid **GPU**" (v2: "card");
- **post hoc is labelled wherever it appears, abstract included**, and never
  joins the registered family (PR:63-65, :134-135);
- **every new analysis has a measured floor** (PR:135; PLAN §6 provides the
  interaction check's);
- **code supplement exists** (V3-V1): double-blind now binds the supplement
  too (PR:128-133);
- commits: suspended by the owner (log:6236-6243), overriding PR:167-169;
- hooks: if a hook refuses an action, rename or report; never route around it
  (PR:170-172).

---

## 3. The change list (V3-*), with an owner for each item

Read the items verbatim at `PR:174-299`. "Applied by" names who carries the
item in step 4 (writers W1–W5 per `WRITERS.md`; B2 = build and checks;
orchestrator = rows from step 0.5, transcriptions, the supplement).

| item | what | applied by | notes |
|---|---|---|---|
| **V3-F1** | environment first; each property with its rows | **W2** (§3: properties, Table 2), **W3** (§4: what each does), **W1** (§1 contributions; abstract) | §8.1 below lists each property, its rows and its narrowing |
| **V3-F2** | abstract: one question, one result, one lesson; written after the check; `description` rechecked | **W1** | lesson is a HOLE until step 0.5; templates in `00_abstract.md`'s stub (P1 §3.3) |
| **V3-F3** | the size plainly: about a tenth of an agent per episode; last fifth only; the paper no longer rests on it | **W4** (§6.3 home; writes row X4-3); **W1** (abstract, §1 short form) | "only at updates 900–1000" is the precise form (RES-12) |
| **V3-F4** | identity; matching the active share cannot isolate co-occurrence; the plane leads the results, non-verdict-bearing; Γ stays the test; future work; advice never a "therefore" | **W4** (§6.2 identity, row X4-1; §6.3 plane first), **W5** (§6.5 lesson, advice, future work), **W1** (abstract lesson) | the plane separates co-occurrence from the **active share**, not from frequency (§9.2 trap 2) |
| **V3-F5** | disclose the framing change | **W4** (§6.1, about three sentences; App. D, with row X4-5) | not in §1 or the abstract (STRUCTURE §11 row 13) |
| **V3-F6** | limitations in front: sited where composition is weak; δ "inert" coarse and asymmetric (+ the train/test mismatch); one algorithm, one map, 12 agents | **W1** (§1 short forms), **W4** (§6.1 home of the siting; §6.2 home of the mismatch), **W3** (§4.3 the CB-9 measurement; §4.4 the asymmetry) | homes in `checks/caveats.yaml` C01–C05, C34 |
| **V3-S1** | 12–15 printed pages of main text | **every writer** (budgets, STRUCTURE §3); **B2** (≤ 15 check) | page measure V3Q2 |
| **V3-S2** | registration-timeline appendix; main text at most the unblinding date and the fact of registration | **W4** (App. D); **every writer** (no other date; `checks/dates_allow.txt`); **B2** (date check) | the appendix stub lists every moved item |
| **V3-S3** | no internal codes or private vocabulary in the main text; glossary extended; unrebuilt figure labels glossed once | **every writer** (§5.2; `checks/terms.txt`); **B2** (term check) | gloss form: `labelled “TERM” on the figure` |
| **V3-S4** | captions say what the figure shows; limits once, in the text | **every writer with a figure** (STRUCTURE §4) | |
| **V3-S5** | each caveat once (one-home map) | **every writer** (`checks/caveats.yaml`, your stub's CAVEATS); **B2** (one-home check) | |
| **V3-S6** | Remark 1 cut; Prop. 4 an appendix remark in words with its honesty note; keep Props. 1–3, Thm. 1, Cor. 1 at v2's verified level | **W2** (§3, App. A) | Thm. 1 per V3Q5; Remark 2′ per V3Q4 |
| **V3-S7** | write for a newcomer; avoid v2 P3 §6's patterns and BR's 101 sentences | **every writer** (§9.4) | |
| **V3-E1** | the interaction check | **orchestrator** (run, analysis, rows IC-*); **W5** (§6.4, App. G); **W1** (abstract, §1, §9 holes) | text waits for step 0.5 |
| **V3-E2** | Thm. 1's statement against the implemented toy | **W2** (App. A statement per V3Q5; rows X2-1, X2-2) | mismatch found (P3 §3.3; §9.2 trap 1) |
| **V3-E3** | new numbers need VERIFIED rows first | **every writer**; rows owed listed in `WRITERS.md` | |
| **V3-V1** | the anonymized code supplement | **step-2 builder** (built); **W5** (§8 describes it) | size and TMLR limit need rows (SUP-1, SUP-2 OPEN; V3Q24) |
| **V3-V2** | a registration statement, honest about its limits | **W5** (§8, two sentences), **W4** (App. D, full) | full-history check is the owner's (V3Q16) |
| **V3-V3** | §11 (v3 §8) describes the supplement | **W5** | v2 Q4e settled for the supplement option |
| **Checks M1–M4, kit checks** | carried | **B2** | v2 BRIEF §3 |
| **Disclosure** | the owner writes the `<d-footnote>`; App. J starts from the builder's draft in PAPER V3 item 6 | **owner** (footnote); **W5** (App. J draft) | agents never write the footnote; W1 leaves its slot |
| **Open questions** | one-page `OWNER_QUESTIONS.md` at step 4.5; title reopened | **orchestrator**, from `DISPOSITIONS.md` §4–§5 | |

---

## 4. Binding rulings, by entry name

v2 BRIEF §4 binds unchanged; read it there. Added for v3:

| entry | what it forces in your text |
|---|---|
| PAPER V3 (:6115) | item 1: the professor's review is **not a ruling** (:6121-6122): never cite it as fact (e.g. "mostly Coupling A" is the review's phrase); item 2(c): the plane leads the example's results, labelled non-verdict-bearing, Γ stays the registered test; item 3: environment-first, registered strings verbatim, "null" at most an informal gloss, the framing change disclosed; item 4: ISO-4 at 2000 updates is future work, no run; item 6: the owner writes the footnote |
| PAPER V3 PHASE 1 START (:6218) | the interaction check is at θ\* only; Low and High are **not run** and their check is not authorized: never imply they were |
| UNBLIND RESULT, POST-UNBLIND STAGE RESULT, SECONDARY RESULT, §7 PROPOSALS, PRE-UNBLIND, T\* | as v2 BRIEF §4 (all registered strings and readings stand) |
| READS RULING item 4 (:5732) | the communication-denial discussion presents Remark 2′ as a refinement of Pynadath & Tambe (in v3: one sentence in §4.4, statement in App. A; V3Q4) |
| FIGURE BATCH RULINGS (:5888) | A1 (Γ never without Γ₄ near the opening) now applies to §6.3's first mention of Γ, since no opening ladder remains; A3 (ISO/JOINT episodes only in the appendix, separately); B7 (B̂ no verdict); B9 (spreads from other runs are "reference scale (cross-artifact)"); B10 (the simplex shows the γ_n pair that fits and the γ_p pair that misses) |
| TITLE AND TERMINOLOGY (:5583) | "stressor", "ambient hazard", "environment configuration" stand; the title is reopened again (PR:298-299) |

---

## 5. Terminology, the glossary, and the strings that stay

### 5.1 Ruled terms

v2 BRIEF §5.1 binds, with two v3 changes: (a) "pre-registered" attaches to
the test only, and the main text gives **no registration date** (V3-S2:
"the test was registered before the main training runs"); (b) the inert
phrase's full form appears at its home (§4.4) and at most in §1 and the
abstract; elsewhere "inert (§4.4)".

### 5.2 Plain-term glossary (v2 BRIEF §5.2, extended for v3)

"Defined in" is the v3 file where the term is defined once. Rows marked
**new** are v3 additions. A term marked *banned* is in `checks/terms.txt`
and may appear in the main text only inside a figure-label gloss.

| internal term | plain replacement (defined once) | defined in | note |
|---|---|---|---|
| **worked example** (new) | the pre-registered test, presented as an example of what CHE makes testable | `01_introduction.md` | never "the main result" |
| CHE | **the Compound Hostile Environment (CHE)** | `00_abstract.md`, again `01_` | naming is the owner's call (v2 Q4c default: named) |
| stressor | one of Coupling A, Coupling B, communication denial | `01_` | the fire is not a stressor (D1) |
| θ, θ\* | **environment configuration θ = (β, κ_A, κ_B, δ)**; θ\* **the held-out test configuration** (β 0.49, every stressor on) | `03_` (θ), `06_` (θ\*) | |
| Low, Medium, High | **the three severities**, placed below, near and above the measured percolation threshold | `04_` | |
| the grid | **the main training runs** of the test | `06_` | "the grid GPU" stays inside the registered bias-(b) string |
| unblind, unblinding | **unblinding: the first computation of any outcome contrast** | `06_` | "pre-unblind"/"post-unblind" *banned* |
| lock, locked | **fixed before the main experiment** (values in App. B; dates in App. D) | `03_` | "lock record", "lock ruling" *banned* |
| floor | **reproducibility floor: the spread of identical reruns of one artifact on one GPU** | `05_` | "floor basis", "re-floor" *banned* |
| bar | **acceptance threshold** (with its floor) | `05_` | |
| **detection limit** (new) | **the effect a test detects with 80 % power at its family-corrected level** (the 80 %-power MDE; the registration's X) | `05_` | never called a bound (BR W4) |
| **exclusion bound** (new) | **the larger absolute end of a confidence interval that contains zero** ("excludes a gain larger than …") | `05_` | the registered completion sentence stays verbatim |
| confirmatory family | **the two registered co-primary tests, Šidák-corrected** | `06_` | |
| branch A–D, A_c | **registered outcome**; letters in App. D only | `06_` (6.1) | *banned* letters |
| ISO, ISO-4, JOINT | **the isolated arm**, **the isolated arm without its communication-only components**, **the joint arm** | `06_` | |
| Γ, Γ₄, Γ₄′, B̂, Γ_H, Γ(t) | Γ **the gap JOINT − ISO**; Γ₄ **the corrected gap JOINT − ISO-4**; Γ₄′ **the same-GPU replicate of the correction**; B̂ **ISO-4 − ISO, reported without a test**; Γ_H **the High-severity readout**; Γ(t) **Γ at earlier checkpoints** | `06_`/`07_` | v2 BRIEF §5.2 rows carry |
| **per-coupling frequency μ** (new as a symbol in the main text) | **the share of training episodes in which a given coupling is on** (μ_A, μ_B) | `06_` | v2 "marginal", "dose" (*banned*) |
| **co-occurrence p** (new) | **the share of training episodes in which both couplings are on together** | `06_` | |
| **active share** | **the share of training episodes with at least one behaviourally active stressor**; with δ inert, **= μ_A + μ_B − p** | `06_` | the identity's home (C08) |
| **fire-only share ν** | **the share of training episodes with no active stressor** (ν = 1 − active share) | `06_` | never "hazard-free", "no-element" (*banned*) |
| simplex | **the triangle of training mixtures** | `07_` | |
| γ_p, γ_n | **the co-occurrence slope**, **the fire-only-share slope** | `07_` | what the plane separates: co-occurrence from the active share only (§9.2 trap 2) |
| knee | **change point** | App. F | *banned* in the main text |
| `sweep_c50_p000` etc. | **the p = 0 sweep arm, which trains on ISO-4's mixture on JOINT's GPU**; **the sweep arm at co-occurrence p** | `07_` (if needed) / App. F | *banned* codes |
| **interaction check** (new) | **a post hoc, evaluation-only check, at θ\* only, of whether the two couplings' effects on trained policies add** | `08_` | always labelled post hoc (C26) |
| **condition** (new) | one of **neither coupling, Coupling A only, Coupling B only, both**, each θ\* with κ_A and/or κ_B set to 0 | `08_` | δ = 1.0 in all four |
| **interaction contrast I** (new) | **I = J(both) − J(A only) − J(B only) + J(neither)**; I = 0 means the effects add; I < 0 that both together cost more than the sum | `08_` | sign convention stated once |
| **main effect** (new) | **J(A only) − J(neither)**, likewise for B; descriptive context, not tests | `08_` / App. G | PLAN §4 |
| **evaluation self-floor** (new) | **the spread of repeated evaluations of the same checkpoint in the same condition on the run's GPU** | `08_` | PLAN §6 |
| **registration timeline** (new) | **Appendix D**: dates, rulings, GPU blocks, seeds, archives | `06_` (pointer) | |
| **code supplement** (new) | **the anonymized archive of the code, configs, tests, analysis scripts and registration documents submitted with the paper** | `11_` | |
| card, unit n, GPU 1/2/3 | **"on one GPU", "on a second GPU of the same model"**; the numbered GPUs appear only in App. D | `07_` (one sentence) | *banned* in the main text |
| study codes (M3.0 … G1.3), m44, m35 | **name the study** ("the Coupling-B calibration grid", "a four-run floor study at Medium") | first use | *banned*; key in App. D |
| obs v2/v3 | **the observation before masking / as masked by smoke** | `03_` | *banned* |
| E2C, E2C² | **the corridor toy**, **the two-agent courier toy** | `03_` / App. A | *banned* |
| handshake | **a check against the closed form** | `03_` | *banned* |
| co-active | only for the counter: **collapse-seeded ignitions near an agent** | `03_` (3.5) | |
| reference scale (cross-artifact) | **a spread measured on other runs, shown for scale only** (FIGURE BATCH B9) | `04_` | ruled wording; kept |
| sensitivity arm | **an arm outside the confirmatory family** (ISO-4) | `06_` | registered wording |
| VOID, REJECT, null, UNDERPOWERED | registered verdict words, used only where registered | `06_`/`07_` | "null" never as the result's name (log:6166) |
| illustrative | **shown to explain, never to grade** | `00_hero.md` | replaces "grades nothing" (*banned*) |
| rung, ladder, floor basis, grades nothing, live, dose, instrument, box, digest, traced, chip | *banned* or plain words (v2 BRIEF §5.2; `checks/terms.txt`) | — | "box" (the machine) is not in the term list because the schematic's boxes are legitimate; do not use it for a machine |

### 5.3 Strings that stay verbatim

v2 BRIEF §5.3 binds unchanged, except that "the branch label stays B" now
lives in App. D (P1 §1.2) and "a-fortiori exclusion" with its sentence lives
in App. E (one sentence may point to it in §6.3).

---

## 6. Registered strings and honesty lines (v2 BRIEF §6, VERBATIM), then their v3 landing

*The following block is copied verbatim from `paper/v2/BRIEF.md:279-330`. Its "lands in" columns name v2 sections; the v3 landing is the table after it (§6.4).*

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

### 6.4 v3 landing (B1)

v3 file names; the full form at the home, elsewhere only where
`checks/caveats.yaml` allows a short form.

| string / honesty line | v3 home | also (short form) |
|---|---|---|
| "does not survive the inert-share correction" | `07_` (§6.3) | abstract, §1 |
| "sign unstable over the final half" (both co-primaries, with the shapes) | `07_` | abstract, §1; App. E tables |
| "second exclusion bound" (X₄) | `07_` | — |
| REJECT / null | `07_` (table and text) | — |
| UNDERPOWERED | App. E (k = 60, T = 2000, change points) | `07_` one clause if needed |
| VOID (mediation; comms condition (iii)) | App. F; App. C | — |
| non-verdict-bearing | `07_`, once (the plane's first sentence) | abstract if it names the plane |
| a-fortiori exclusion + its sentence | App. E | `07_` one sentence |
| reference scale (cross-artifact) | `04_` (Figs. 4, 5 captions) | App. C |
| illustrative | `00_hero.md` | `04_` (severity renders) |
| recorded, not graded | `05_` (the rule) | — |
| completion as an exclusion ("excludes a joint-training gain larger than 0.66 points") | `07_` | abstract, §1 |
| bias (b) "reverses sign on the grid GPU" | `06_` (§6.2, one sentence) | App. D (all readings) |
| "the branch label stays B"; branch B's headline "no longer holds as worded" | App. D | `07_`: one clause, no branch letter |
| the founding hypothesis "did not occur" | App. D | `07_` may say it in plain words without the letter |
| honesty line 1 (inert-share qualifier) | `07_` | abstract, §1 |
| line 2 (matched compute + Γ(t) suffix) | `06_` (matched compute), `07_` (suffix) | abstract, §1, §7 one line |
| line 3 (completion exclusion) | `07_` | abstract, §1 |
| line 4 (δ inert; the composition tested is A × B) | `04_` (§4.4) | §1, `06_` "inert (§4.4)" |
| line 5 (Medium siting; the struck line stays struck) | `04_` (the measurement) and `06_` (§6.1, the limitation, as registered, PFB:245-260) | §1 (short form) |
| line 6 (death penalty; penalized vs rewarded channel) | `03_` (§3.3) | App. D (the falsifier's reading) |
| line 7 (endpoint confound, 3×) | `06_` (§6.2) | — |
| line 8 (hardware blocks) | App. D (home) | `07_` one sentence |
| line 9 (secondary intervals not family-corrected) | `07_` | — |
| line 10 (the counter co-active only in all-on configurations) | `03_` (§3.5) | App. F (mediation) |
| §6.3's "what NOT to claim" | binds every file | — |

---

## 7. The δ design error (F3): the record (v2 BRIEF §7, VERBATIM), then its v3 placement

*Copied verbatim from `paper/v2/BRIEF.md:335-385`. In v3, every date in it moves to App. D (V3-S2); the main text keeps the facts without dates (§7.1).*

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

### 7.1 v3 placement (B1)

- **Home: `06_` §6.2**, one paragraph, **no dates**: the design kept a
  stressor it had already found inert; it left δ out of the secondary
  sweeps for that reason but kept two δ-only components of six in ISO; it
  did not count the resulting fire-only third; a review of the registered
  design identified the bias **before the grid**; it was registered with its
  direction and a correcting arm, ISO-4, **before unblinding**, while the
  grid was running. This is the "design error" caveat (C10).
- **§1:** one clause (owned as a design error; pointer). **Abstract:** one
  clause (P1 §3.1 item 3). **App. D:** the full dated table above, with
  V6-1, V6-2, V6-3, DES-12, DES-15, and the attestation.
- **The v2 wording constraints above bind unchanged** (owning it plainly; no
  foresight framing; "registered before unblinding" for the correction;
  "a review of the registered design" — attribution is carried v2 question
  A1(ii)).

---

## 8. Claims: the environment (V3-F1), the result set, and the check

### 8.1 The environment's properties, each with its rows (P1 §1.1 with P3 §1.1's verdicts)

| property | rows / code | narrowing the text must keep (P3 verdict) | home |
|---|---|---|---|
| collapse seeds the fire (Coupling A) | CA-1; CA-2, CA-3, DX-304 (Prop. 3 in two runs, at non-locked κ_A, no agents); DX-37; `che/env/structure.py:83-102` | OK as a mechanism. The fall under trained policies is fuel exhaustion, already seen with random policies (DX-9); the "trained" policies are 500-update calibration policies (DX-40); the hazard is not agent-independent (CA-8, CA-9) | `03_` (§3.2), `04_` (§4.2) |
| it limits itself Low → High | CA-4 (4.83×), CA-5 (4.92×), DX-9 (5.7×, random) | never "as predicted before measurement"; NARROW "self-limiting" to fuel exhaustion | `04_` |
| smoke attenuates perception (Coupling B) | CB-1; DX-1; CB-10, DX-11; `che/env/observation.py:300-310` | Coupling B sits in the observation kernel; "not suppressible" only for trained policies at 500 updates | `03_`, `04_` (§4.3) |
| smoke's survival cost at High | CB-5, DX-13, CB-7 | **descriptive**, "same direction in 3 of 3", single runs, two sharing a seed (WEAK BAR); the Low contrast has no row — do not use it | `04_` |
| hazard-blind reward, cause-blind death price (Def. 2) | ENV-1, ENV-9; ENV-2–ENV-5 (d_p ablation, scope); `che/env/tasks.py:31-43`; `che/tests/test_reward_independence.py`; `che/tests/test_lethality.py:143-162` | OK as a code property; NARROW: an agent dies only on a burning or collapsing cell, so the death price is in effect a contact price, and ENV-2 shows it drives survival learning (BR W7) | `03_` (§3.3) |
| severity by a measured percolation threshold | CAL-1 (O-2: no committed estimator), DX-204 (committed estimators), CAL-2–CAL-5, DX-201, DX-6, DX-7, DX-8 | lead with the committed estimators and the bands; two phases and a finite-size window; Def. 4's Medium-variance prediction refuted for survival (CAL-5) | `04_` (§4.1) |
| ablations are bitwise-exact nested models | `che/tests/test_nesting.py:78-88, :222-240`; `test_coupling_b.py:131-156`; `test_comms.py:272-319`; golden digests | "under the same random keys, on one backend"; the κ_A test compares fire and smoke only; the δ test compares against a pre-channel digest on CPU; checkable with the supplement | `03_` (§3.4) |
| theory checked as unit tests | Prop. 2/Cor. 1 (`test_percolation.py`), Prop. 3 (CA-2, CA-3; `test_prop3.py`), Thm. 1 (CB-4, DX-14, X2-1; `test_e2c.py`) | closed forms the code is checked against, in toys and at non-locked parameters — not a theory contribution; Thm. 1 per V3Q5 | `03_` (§3.4 table) |
| the floors protocol | METH-1–METH-4, METH-7, HW-1, DX-21, DX-303 | "the protocol this paper follows"; name which bars have floors, never "every bar"; a four-run floor is ±40 % (DX-303); no RL-evaluation citation unless verified (V3Q17) | `05_` |
| communication denial, independent axis | COM-6, ENV-12, DX-17; COM-2–COM-5, DX-16, V4-1–V4-3 | the ruled inert phrase with its bars beside it (7.99 completion, 2.60 survival points, 4 seeds, about half power); the asymmetry; never "certified" | `04_` (§4.4) |
| the co-active counter | CO-4, DX-37; CO-1–CO-3 | co-active only in all-on configurations | `03_` (§3.5) |
| one instance, one learner, matched budget | ENV-6, ENV-7, ENV-8, ENV-10, ENV-11, DX-2, DX-3, DX-4, DX-407 | IPPO, one shared-parameter policy per seed; no PBT in any reported run; one 64 × 64 map, 12 agents | `03_` (§3.5), `11_` |
| the code ships | supplement rows owed (SUP-1, SUP-2 OPEN) | no size or limit stated until rows exist | `11_` |
| API and usability | `che/env/env.py:200, :283-290`; `che/train/ippo.py:668-679`; `che/eval/harness.py:240-244` | do **not** claim JaxMARL compatibility (no wrapper; the reward is a team scalar) | `11_` |

### 8.2 The result set

v2 BRIEF §8 binds unchanged (values, IDs, units); read it there. The v3
homes: Γ, Γ₄, Γ₄′, B̂, Γ(t), secondary (SEC-1, SEC-3, SEC-4), arms →
`07_`/`06_`; k = 60, T = 2000, High readout, fire deaths, Γ(t) tables →
App. E; mediation → App. F; GPU blocks and the seed history → App. D;
evaluation reproducibility → `11_`. New v3 numbers (rows owed, `WRITERS.md`):
X4-1 (identity per arm), X4-2 (training δ per arm), X4-3 (agents per
episode), X4-4 (Γ₄'s and B̂'s detection limits), X4-5 (framing-change
date, App. D only), X2-1 and X2-2 (Thm. 1's toy), IC-* (the check).

### 8.3 The interaction check: what may be said (PLAN §1–§8)

- **What it is:** eval-only, post hoc, at θ\* only; four conditions
  (neither, A only, B only, both), δ = 1.0 throughout; the final checkpoints
  of ISO (72), JOINT (72) and ISO-4 (20); the registered draw (seed 0, 512
  episodes) with common random numbers; I per policy and co-primary.
- **Test:** per arm and pooled (stratified by seed count), normal intervals
  on seed dispersion, **Šidák over 8** (4 estimates × 2 co-primaries);
  observed-SE MDE80 as the detection limit; evaluation self-floor and a
  reproducibility check on the run GPU (PLAN §6).
- **Reading rules (PLAN §7):** "detectable" = the Šidák interval excludes 0
  **and** the floor check is met; report sign and size (survival also in
  agents per episode). Otherwise an **exclusion with its bound**: "|I| < B at
  the family-corrected level", B = the larger absolute interval end, MDE80
  beside it; never "no interaction" or "additive". **The headline is the
  pooled pair**; per-arm rows say whether the answer depends on training.
  Cross-arm differences in I are descriptive only.
- **Blind to (PLAN §8; one home `08_`):** θ\* only; fixed policies (not
  whether training on co-occurrence helps — that is Γ); the additive scale
  of bounded rates; one draw; δ held at 1.0; not a cross-arm test; post hoc;
  the arms met the four conditions differently in training (ISO trained on
  A-only and B-only at δ = 0, ISO-4 never saw δ = 1, JOINT trained only with
  every stressor on; all training at β 0.43 / 0.70, never 0.49).
- **Label wherever it appears:** "post hoc" (shortest form: "a post hoc
  check at the test configuration"). It never joins the confirmatory family
  and changes no registered reading (PLAN §1).

---

## 9. Traps, record corrections, claims ceiling, style

### 9.1 Known traps (carried)

v2 BRIEF §9.1 binds unchanged (every bullet); read it there. Changes: the
"recommendation in §9.3" bullet is replaced by V3-F4 (§9.3 below); the F3
dates leave the main text (§7.1).

### 9.2 Record corrections (orchestrator notes, re-checked where cited in §0) — new traps

1. **Thm. 1's stated signal model does not match the implemented toy.**
   `TF:375-394` (and v2 §6.2) state unit smoke density over the integer
   distance d − t + ℓ_f; `che/env/e2c.py` uses the production kernel
   (Euclidean distance, a growing single-cell smoke field). The toy's
   optical depths are ≈ 0.71 / 0.90 / 0.99, not 4 / 3 / 2; at κ_B = 1 the toy's
   q ≈ 0.81 against the formula's 0.19 (P3 §3.3; builder derivation, not a
   paper number). The code agrees with its own test (q built from measured
   transmittances). **Do not write v2's statement.** App. A states Thm. 1
   per V3Q5. BR's "J\* − ½ = 0.0000 contradicts the theorem" is **wrong**:
   0.5000 ± 0.0055 measured against 0.5028 predicted, z −0.51
   (`phase4_report.md:72`; row X2-1). Thm. 1's J\* is the value of the
   content channel only (P3 §3.3 item 5).
2. **The plane separates co-occurrence from the active share, not from
   frequency.** ν = 1 − 2μ + p in every arm, so each slope moves frequency
   with it. Never write "separates co-occurrence from frequency" (it is in
   `checks/terms.txt`). No design in the record isolates co-occurrence. The
   prompt's own phrase "separates the two" (`PR:208-209`) is right only in
   this reading (record correction reported).
3. **Training δ.** ISO's A-only and B-only components and all of ISO-4
   train at δ = 0; JOINT trains at δ = 1; θ\* has δ = 1 (§0). This is a
   train/test mismatch for ISO and ISO-4 in communication denial; it is
   harmless only if δ is inert, the premise in question. It belongs with
   the limitations (home §6.2, short form §1). The interaction check holds
   δ = 1 and **cannot address it**.
4. **DX-406 is scoped** to the fire-death comparison. The size statement
   uses row X4-3, not DX-406, and never the professor's "0.11" from the
   review text.
5. **The registration defines X as the 80 %-power MDE** (`PFB:190-195`), so
   the registered completion sentence stays verbatim; any further exclusion
   statement uses the CI bound and says so; X is named "the effect the
   design detects with 80 % power (the registration's X)". The High-readout
   "no gap larger than 3.40 … 2.54" numbers are MDEs (RES-14): label them.
   Drop "conservative" for the k increase unless the positive-covariance
   argument is given (v2 BRIEF §9.1).
6. **CB-9 rests on a three-seed spread, not a measured floor** (ledger :80).
   It is the main evidence for the siting limitation, so §4.3 says so.
7. **TMLR facts** came through a summarizing fetch tool (P3 §0): "up to
   100MB", PDF or ZIP, anonymized; "up to 12 pages (of main content)" for a
   two-week review. **Not quotable** until re-read directly and transcribed
   (V3Q24).
8. **Figures:** v2's main text was 33.42 printed pages; figures cost 3.46 in
   all and iframes nothing in print, so the cut is a text cut. Print
   companions print about 231 pt wide with 2.5–4.3 pt labels (illegible,
   BR W9). Every rebuild (R1–R11, print-size) is a **proposal** needing the
   owner's agreement; none is approved; any rebuild writes to a new output
   directory, because v2's build reads `paper/figures/*/out/`.
9. **Record items not to repeat:** `README.md:13-17, :28-35` (stale: "grid
   not yet run", PBT, β̂_c as Kesten reproduction); `LICENSE:3` names the
   author (step 2's scrub); `PFB:69, :75, :82` overclaim (β̂_c = 0.500 with
   no committed estimator; "Comms certified inert at swarm scale"; "ordered
   by curriculum difficulty") — never echo them; this checkout is a shallow
   clone, so the registration commit dates cannot be verified here.
10. **The interaction-check results do not exist yet.** Every sentence that
    depends on them is a `<!-- HOLE:INTERACTION -->`. Never guess an
    outcome, a sign or a bound.
11. **"Behaviourally active" has no operational definition in the record**
    beyond "not found inert in calibration" (log:3977-3980). State the
    asymmetry; do not invent a threshold or compute alternative active
    shares (that would be a new analysis).
12. **ISO-4 at 2000 updates matches exposure counts by doubling compute**,
    so it gives up matched compute; the future-work sentence says so (P3
    §3.1 point 3).

### 9.3 Claims floor and ceiling (v3)

**Must be said (floor):** v2 BRIEF §9.2's floor, minus the recommendation,
plus: CHE is the contribution and the test its worked example; the
emphasis moved to the environment after the result was known (§6.1); the
test was sited where composition is weak, stated as central and up front;
the size: about a tenth of an agent per episode (X4-3), only at updates
900–1000; the identity active share = μ_A + μ_B − p and its consequence;
the plane leads the results, labelled; the interaction check's result with
its label and bound (once back); the δ train/test mismatch; one algorithm,
one map, 12 agents; the code supplement and an honest registration
statement.

**Must not be exceeded (ceiling):** v2 BRIEF §9.2's ceiling, plus: no
claim from the interaction check about training (it holds policies fixed),
about Low or High, or about δ; no "the plane separates co-occurrence from
frequency"; no advice after "therefore", "so" or "thus", and none as a
contribution — it is one labelled "we suggest, from this one environment"
sentence; no theory contribution claimed (the theorems are checks); no
JaxMARL compatibility; no supplement size or venue limit without rows; no
statement that Low/High checks were run.

### 9.4 Style hazards (P3 §4; V3-S7)

Avoid: undefined private vocabulary; pointing at records the reader cannot
see ("the ruling", "the lock record", "the formal specification"); internal
codes glossed after the fact; terms used before they are defined (define,
don't cut, registered strings); stacked qualifiers and clause chains;
unclear referents and dangling participles; wrong verbs and category errors
("the theorem tests the code"); misused statistical terms (§9.2 item 5);
arithmetic the reader must reconstruct; project history inside the argument
(it goes to App. D); telegraphic captions; repetition (the one-home map);
machine-register tells (bold-label paragraph openers, ", not …" antitheses,
aphoristic closers, announced enumerations, "This section states", status
disclaimers on captions, sentences over 40 words); print-only defects
("Interact:" text and "press ]" outside the `interact` span). Do not
reproduce any of BR §8's 101 sentences (BR:338-480).

---

## 10. Numbers and units

v2 BRIEF §10 binds (tags, points, interval labels, scope in the sentence).
v3 changes:

- New rows go in `paper/v3/ledger_proposals/W<n>.md` with IDs **`X<n>-<k>`**
  (STRUCTURE §12 item 3), in the supplement's row format
  (ID | value | what | source | status), VERIFIED from a committed file at
  file:line, or DERIVED with the arithmetic on verified rows.
- Interaction-check numbers come only from rows **`IC-<k>`** in
  `paper/v3/ledger_proposals/IC.md`, written by the orchestrator from the
  committed step-0.5 report. Until they exist, write a HOLE, not a number.
- **Commit constraint:** rows must be read from committed files; outputs of
  this session (the supplement build in `paper/v3/out/`, the interaction
  results) are not committed while the owner's commit ban holds. Such rows
  are marked `PENDING-COMMIT` and may not be cited in text until they are
  VERIFIED (V3Q25).
- The size in agents: **"about a tenth of an agent per episode (0.11 of
  12)"**, tagged X4-3, with RES-2 beside it.

## 11. Double-blind

v2 BRIEF §11 binds, with v3 changes: the anonymized code supplement exists
(V3-V1), so §8 may say "the code supplement" and in-repository paths may be
cited as paths inside it; never a repository URL, an account, a commit hash
or an absolute path; the registration documents' content sha256 values may
be printed only if the owner agrees (V3Q16; they resolve to nothing but are
a new kind of identifier in the text).

## 12. Disclosure

- **The owner writes the `<d-footnote>`** on the abstract (PAPER V3 item 6;
  log:6193-6202). W1 leaves its slot as a comment
  (`<!-- OWNER: disclosure d-footnote here -->`) at the end of the
  abstract's first sentence. No agent drafts the footnote text.
- **App. J "How this paper was made"** starts from the builder's
  recommendation quoted in PAPER V3 item 6: a statement of the division of
  labour, and that some proposals came from the assistant — in particular,
  that the inert-share bias and ISO-4 were first raised in an
  assistant-drafted review and adopted by the owner. W5 drafts it for the
  owner to edit (log:6197-6202). Carried v2 question A1 (scope;
  attribution) stays open.

## 13. Provenance

v2 BRIEF §13 binds, with: files are `paper/v3/provenance/<section file
name>`; the change column is "change from v2, and why" (reused / edited /
new, with the v2 file:line when reused); W1's provenance for
`00_abstract.md` also carries the title candidates (STRUCTURE §10, V3Q1)
and the `description`. Run `provenance_check.py --strict` (B2's copy).

## 14. Kit syntax

v2 BRIEF §14 binds unchanged, except **line 1**:
`<!-- PAPER V3 DRAFT (PAPER V3 ruling, 2026-10-12): builder-drafted, not owner-approved -->`,
and the H3-opening files listed in STRUCTURE §12 item 2. Interaction
pointers go inside `<span class="interact">…</span>` (hidden in print).

## 15. Citations

v2 BRIEF §15 binds unchanged (keys from v3's `submission.bib`, B2's copy;
characterize works only as `RWV` Part 3 records). **No new citation by
default**: Safety Gym, Safety-Gymnasium, Melting Pot, and RL
evaluation-methodology works (Henderson et al., Agarwal et al., …) are not
in `RWV` and need verification first (V3Q17).

## 16. Figures and listings

Numbering, placement, glosses and listings: STRUCTURE §4–§5. The stubs
carry each figure block and listing block as v2 carried them (a comment
names the v2 source). Rewrite captions to V3-S4; keep blocks
self-contained.

## 17. NO SOURCE: do not state

v2 BRIEF §17 binds, with v3 changes: Γ₄'s and B̂'s detection limits may be
stated once row X4-4 exists; the agents-per-episode size once X4-3 exists;
anything about the interaction check only from IC-* rows; still no supplement
size or venue limit (SUP-1, SUP-2 OPEN), no total GPU-hours, no CPU-suite
time and no training throughput unless a row is written (V3Q18); no Low or
High interaction result (not run).

## 18. Hand-back (each writer)

v2 BRIEF §18 binds (files and word counts; tags used; new rows; numbers you
could not tag; departures from your stub; listings; alternates; findings
and owner questions numbered against `DISPOSITIONS.md` §4), plus: every
HOLE you left, every OWNER-PENDING marker, and the output of the term,
date and one-home checks on your files if B2's checks are available.
