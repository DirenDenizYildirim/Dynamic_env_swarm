# Owner questions after Paper v2 phase 1

Orchestrator, 2026-10-12. This file gathers every open decision. Sources:

- `FINDINGS.md` §3 (Q1–Q25);
- the OWNER-level review findings (`REVIEW.md`);
- B2's owner items;
- the blind review (`review/blind_review.md`).

Questions are grouped and ordered by priority. Each one says:

- what v2 does now (the **default**);
- the options;
- where to look.

You can answer by number, for example "A1 b, B1 T1, …". "Default" means you
accept what the text already does. Group G can be accepted in one line.

---

## A. Integrity and framing (decide these first)

**A1. LLM authorship and the disclosure footnote.** Sources: RC1-3, Q16,
Q4h.

The record indicates that builder (LLM) sessions wrote the registered
Phase-6 design and the 2026-08-16 review that found the inert-share bias,
and that you ruled on both:

- `phase6_design_v2.md:13-15`: "drafted by the same agent that produced the
  red team and proposed the remedies";
- log:3557-3559: "an assessment written this session from the repository".

TMLR expects ideas, claims and results to be "human-sourced". The question
has three parts.

- **(i) The footnote's scope.**
  - Default: "its uses included …" drafting, literature search and
    verification, writing and running code and analyses, making figures,
    and drafting design documents, reviews and proposed options. It closes
    with "The authors are responsible for every word."
  - Option: narrow or widen that list. The footnote names the tool, not
    you.
- **(ii) How §9.1 attributes the 2026-08-16 finding.**
  - Default: "a review of the registered design".
  - Options: say it was LLM-assisted, or name it as builder-written.
- **(iii) Rewriting parts yourself.** Will you write or rewrite the
  abstract, §1's opening and §10 yourself before submission?

**A2. Where the disclosure appears (Q4f).**

A `<d-footnote>` puts its marker on page 1, but its text prints on page 43
of 46, in Distill's footnote list (final build).

- **a. Default:** the footnote only.
- **b.** A visible first-page line (`sections/alt/00_abstract.disclosure_line.md`).
- **c.** Both.

**A3. The blind review's new points.** They are not yet in the paper and
not in `FINDINGS.md`. For each, choose: add to §10 (limitations), address
in the text, check the record first, or leave it.

- **W1.** The "inert" label on communication denial rests on bars of about
  2.6 survival points and 8 completion points from 4 seeds. That is coarser
  than the roughly 1-point effects it explains, and the label is applied
  asymmetrically: Coupling A at High and Coupling B at Low/Medium are as
  weak, yet count as active.
- **W2.** Active share = μ_A + μ_B − p. So "match the active share"
  un-matches frequency, and the paper does not say so.
- **W3.** The test had little capacity, because Coupling B shows no
  measurable effect at θ\*, and the survival gain is about 0.11 agents per
  episode.
- **W6.** Theorem 1's test value, q = 0.0056 at κ_B = 8, is inconsistent
  with the signal model §6 states.
  - The number matches its source (`phase4_report.md:94`, row DX-14). I
    checked that.
  - Whether §6 describes the toy that was tested is unchecked. It is a
    read-only check, with no runs.

**A4. The δ design-error wording (Q4h, with A1).**

Do you approve the corrected timeline as the basis of the text? Default: all
three of these are stated (rows V6-1 to V6-3):

- δ was certified inert on 2026-07-30, before the design;
- the design excluded δ from the sweeps but not from ISO;
- the bias was found pre-grid on 2026-08-16, and registered with ISO-4
  mid-grid on 2026-09-18.

---

## B. Title, abstract and `description`

**B1. Title (Q3).** All five candidates and their notes are in
`provenance/00_abstract.md`.

- **T1 (default, recommended):** "A pre-registered test of training on
  co-occurring versus isolated stressors in a multi-agent fire environment"
- **T1s:** "A pre-registered test of training on co-occurring versus
  isolated stressors"
- **T2:** "Training on co-occurring versus isolated stressors in a
  multi-agent fire environment, a pre-registered test in which joint
  training's survival gain does not survive the inert-share correction"
- **T3:** "A multi-agent fire environment in which collapse seeds fire and
  smoke attenuates perception, and a pre-registered test of training on
  co-occurring versus isolated stressors"
- **T4:** "A pre-registered test of training on co-occurring versus isolated
  stressors, in a multi-agent environment with an ambient fire hazard"

**B2. Registered strings in the abstract (Q4b).** The abstract carries "does
not survive the inert-share correction" and "sign unstable over the final
half" verbatim, where the ABSTRACT ruling accepted paraphrases.

- **Default:** verbatim.
- **Option:** your paraphrases.

**B3. Naming CHE in the abstract (Q4c).**

- **Default:** named in full, as under your ABSTRACT item 3.

**B4. `description` (Q4d).**

- **Default:** a new line, "A pre-registered test of whether training a
  single policy on co-occurring stressors beats training it on each in
  isolation, in the Compound Hostile Environment (CHE), a multi-agent
  environment where a fire burns in every episode."
- **Option:** keep your ruled line, which is quoted in
  `provenance/00_abstract.md`.

**B5. The recommendation (Q6).**

- **Default:** one labelled sentence closing the abstract, scoped "studies
  of compositional generalization" (your wording), plus §9.3.
- **Options:**
  - §9.3 only (`alt/00_abstract.no_recommendation.md`);
  - the narrower scope "joint-versus-isolated comparisons";
  - A3-W2 may change its wording either way.

**B6. The 4.8-fold calibration finding in the abstract (Q5).**

- **Default:** left out of the abstract; it is in §1 and §5.

---

## C. Rulings needed for text that already changed

**C1. Supersede READS RULING item 2 for v2 (Q4a).**

Six sentences of your final §2 changed for accuracy. They are listed
exactly, with your text and the v2 text side by side, in
`provenance/02_related_work.md` → Open items. They include "every arm is
perturbed throughout", "about seven percent" and Erdem & Üre's "do better".

Under the meta-rule, this needs a transcribed ruling. Options: yes, or keep
your sentences.

**C2. The theory doc (Q4k).**

The paper departs from `docs/theory_foundations.md` on six items:

- Cor. 1(3)/(4) and its "universal" caveat;
- Prop. 3's rate;
- Prop. 1's "S, Ω finite";
- Def. 1's observation line;
- Remark 1;
- Prop. 4's "irreducible", and its JOINT ε = 0 contrast.

Options:

- **a. Default:** the paper departs and says so in App. A.
- **b.** Amend the theory doc with dated notes. This is your edit; I may
  not make it.

**C3. Record fixes (Q4l): who makes them, and when.** The files concerned:

- `severity_lock.md:22-23` and `coupling_a_lock.md:84-89` (the dropped
  rate);
- `CLAUDE.md:344` and log:1194 (OWNER ITEM 5);
- `phase4_report.md:366, :394-395` (OWNER ITEM 6);
- `HANDOFF.md:227`;
- `KIT_NOTES.md` §S1.5/§S4;
- `branch_B.md:225`, a misquote of the registered headline;
- `phase6_design_v2.md:431`, which is registered and never edited, so it is
  a note only.

For transcription, if you adopt them:

- the corrected F3 timeline;
- the glossary correction ("the grid's launch floor study").

---

## D. Theory content

**D1. Proposition 4 (Q4i).** Two independent derivations say the bound
certifies nothing at CHE's scale: the step-2 review's N6 and P3. They also
flag a max-for-sum term and a missing 1/γ. The blind review says it "is not
a proposition" as stated in words.

- **a. Default:** keep it in words, renamed "A transfer bound for a fixed
  policy".
- **b.** Move it to App. A.
- **c.** Drop it.
- **d.** Restore a precise statement, after you check the derivations.

**D2. Corollary 1(4) (Q4g).**

- **Default:** stated at the level Garet & Marchand (2004, Cor. 5.4)
  supports. That is one new citation, read in full and recorded in
  `related_work_verification.md` Part 4.
- **Option:** drop it (`alt/04_severity.no_item4.md`).

**D3. Proposition 3 (Q13, RM-10).**

- **Default:** the theory doc's statement, minus the rate.
- **Option:** restate it as an inequality, with the equality as an
  approximation, and add "no primary ignition" to its hypotheses. The proof
  does not establish the exact derivative equality.

**D4. Definition 1 (RM-9).** Its state omits the weak-terrain mask and the
occupancy-mode argument, so Prop. 1's Markov claim holds only given them.

- **Default:** unchanged.
- **Option:** add both to the state.

**D5. Smaller theory wording (Q23).**

- **Default:** the theory doc's statements as given.
- Items:
  - Remark 2′(i)–(ii);
  - Thm. 1(2)'s J^static;
  - Def. 4's "phases" and "fluctuations are maximal";
  - citing Pynadath & Tambe's Theorem 3.

---

## E. Upload and format

**E1. Code availability (Q4e).**

- **a. Default:** §11 states what exists and promises nothing.
- **b.** An anonymized supplement (`alt/11_reproducibility.supplement.md`).
- **c.** "On acceptance".

This also decides App. A's four references to "the formal specification",
which a reader cannot see (RM-11, RC2-35).

**E2. Comment stripping (Q1).** Strip HTML comments (ledger tags) and the
bib's `%` lines for the OpenReview upload too, not only for a rendered-site
link?

- **Default:** the staged copy is stripped; the repository copy keeps its
  tags.

**E3. `date` and `submitted_date` (Q2).**

- `date` prints in the cite box as a full date, and should be no later than
  the upload day.
- With `submitted_date` unset, the byline reads "Not submitted yet".
- `build_v2.py --final` refuses to run until you set `date_confirmed: true`.

**E4. The hero (Q8).**

- **Default:** the episode explorer, as OPENING item 2 ruled.
- **Option:** the opening ladder under the abstract, with the explorer
  leading §3. This needs a build step not yet built (RM-6).

**E5. Layout defaults.**

- §2's position (Q10): default after §1. Moving it renumbers §9.2, which a
  figure prints.
- The simplex (Q9): default in §9.2.
- App. I's explorers (Q12): default kept.
- A label-only figure rebuild in a later phase (Q11): default glossed in
  captions, no rebuild.
- Placement fixes (Q22).

---

## F. Numbers and the record

**F1. Archive count (RN2-7).** App. F's "615 of 615" archives matches its
row and `phase6_report.md:101`. But that report's own archive table sums to
636. Which is right? A record fix may be owed.

**F2. The "bias (b)" label (RC2-34).** With F3 applied, no "bias (a)"
appears, so the label is orphaned.

- **Default:** keep the record's label.
- **Option:** rename it, for example "the differential-drift caveat".

**F3. A ledger rule for numbers that describe cited works (RN1-16).** These
are counts or values from other papers, which BRIEF §10 does not cover.

- **Default:** untagged, with support through
  `related_work_verification.md`.

**F4. New rows (Q18).** Γ₄'s and B̂'s survival detection limits, 0.0090 and
0.0089 (`post_gamma4_t2000.md:15-16`). The blind review's W1/W3 may make
them useful.

- **Default:** not stated.

**F5. Small record choices.**

- O-1, PBT (Q4j): default unmentioned.
- O-2, leading §4 with the β̂_c estimators (Q19): default the demo's order.

**F6. A citation name form.** `lu2022dpo` renders its author as "Schroeder
de Witt, C.", while `dewitt2020ippo` renders "de Witt, C.S.".

- **Default:** both as their records give them.

---

## G. Length and wording defaults (one line accepts all)

- **Q7:** §10 keeps the k = 72 and Prop. 4 lines as pointers.
- **Q14:** contribution 3 (floors) stays as your §1 listed it, with no new
  citation.
- **Q15:** the pre-registration is described by date only; there is no
  public registry.
- **Q17:** "the p = 0 sweep arm, which trains on ISO-4's mixture on JOINT's
  GPU" replaces the fix list's "no-coupling sweep arm".
- **Q20:** the length targets. v2's body is about 29 % shorter than the
  demo's, with §1, §2 and §9 still over budget.
- **Q21:** up-front limitations in §1 cover the Medium siting only.
- **Q24:** your and the demo's wording on the High smoke cost and the
  contributions.
- **Q25:** P3's γ_n reading is not added.

---

## H. What happens next

Once you answer, phase 2 runs as follows:

1. Your rulings are transcribed into `docs/decision_log.md` first, per the
   meta-rule.
2. They are applied to `paper/v2/`.
3. The claims and numbers reviewers re-check the changed lines.
4. The real-kit build and the artifact are refreshed.
5. Section by section, only text you approve moves into `paper/finale.md`.

Tell me if you want a different order, for example to approve sections as
they stand before the rulings.
