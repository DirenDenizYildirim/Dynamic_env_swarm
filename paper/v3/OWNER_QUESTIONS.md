# Owner questions after Paper v3 phase 1 (one page)

Orchestrator, 2026-10-16. Answer by ID ("Q1 T5, Q2 b, …"); "default" accepts
what the text does now. Full options: `DISPOSITIONS.md` §4–§5; evidence:
`REVIEW.md` and `review/`. Every answer is transcribed into the decision log
before it is acted on.

## A. Before the GPU run

- **Q0. The interaction-check plan:** `che/bench/results/phase6/post_v3_interaction/PLAN.md`,
  committed at `415b784` (sha256 `c3ec2dd1…`). **OK as is, or what changes?**
  A change must be committed before the run; the analysis refuses a plan edited later.
- **Q1. What the supplement ships (V3Q16).** Default now: the code, tests, configs,
  registered documents, analysis scripts and committed outputs, **plus the theory
  document and the lock records** (App. A refers to the theory document as shipped).
  Decision-log excerpts: off by default (they quote you). Options: drop the theory
  document (then App. A's four departure sentences lose their referent); add log
  excerpts (then App. D's log quotations become checkable).

## B. The paper

- **Q2. Title (V3Q1).** Default T5, "A multi-agent fire environment with exact stressor
  ablations" (60 characters). Others: T1 (118 characters, 7 printed lines), T1s, T2–T4,
  T6 (`provenance/00_abstract.md`). Also: CHE named in the abstract (B3, default yes).
- **Q3. Page measure (V3Q2).** The final kit build prints the main text at **14.70 pages
  from page 1** and **13.27 from §1** (ceiling 15), with the interaction results still
  to add. That leaves about 0.3 page at the page-1 reading, which may not hold Figure 9.
  Prose is within budget everywhere. (a) Rule the §1 reading; (b) default: keep page 1
  and, if the results overflow, move Figure 5 to App. C.
- **Q4. Theorem 1 (V3Q5, V3Q23).** The paper's closed form does not describe the
  tested toy (`che/env/e2c.py`; App. A). Default: state Thm. 1 for per-step optical
  depths, proof unchanged (matches the code). Alternate: keep the theory document's
  statement and state the mismatch (`sections/alt/…thm1_tf.md`). Either way, amending
  `docs/theory_foundations.md:375-394` is your edit.
- **Q5. Prop. 4 and Remark 2′ (V3Q3, V3Q4).** Default: Prop. 4 is an appendix remark
  in words; Remark 2′ is one sentence in §4.4 plus App. A. Alternates: drop Prop. 4
  (`alt/…no_prop4.md`); Remark 2′ in App. A only, or renamed.
- **Q6. Figures (V3Q8).** The print-legibility check fails on 13 of 13 figures
  (labels print at 2.5–4.3 pt). Default: no rebuild; codes are glossed in captions.
  Options: label-only rebuilds R1–R11 (`plans/P2.md` §7) and print-size companions.
- **Q7. The abstract.** It has 8 words free for the interaction result. Should it also
  carry the central limitation, that the test sits where composition may be weak
  (RC1-22)? Default: no, §1 states it first.
- **Q8. Disclosure (A1).** The `<d-footnote>` slot after the abstract's first sentence
  is yours to write. App. J ("How this paper was made") is drafted in an OWNER-EDITS
  block from PAPER V3 item 6; it names the tool as "Claude (Anthropic), used through
  Claude Code" and records which decisions were delegated. Edit or confirm.
- **Q9. The δ label (V3Q14, V3Q15).** Default: the ruled phrase with its bars beside
  it. Option: authorize one more eval-only condition at θ\* with δ = 0, a direct δ
  check (a new ruling; not part of this run).
- **Q10. `date` and `date_confirmed`** (still v2's 2026-10-11). `--final` is blocked until set.

## C. Record items found (yours to fix or rule; nothing was edited)

- **C1.** `che/tests/test_p6_s7_blocks.py::test_science_tree_identical_to_the_frozen_base`
  **fails at `7a5e009`** now that the checkout has full history: commit `361bec3`
  (2026-10-10) changed two docstrings in `che/env/config.py` ("environment
  configuration"). No behaviour changed. Accept and record, or amend the test's base.
- **C2.** The archive count: App. D keeps "615 of 615", but `phase6_report.md`'s own
  table sums to 636 (F1, carried from v2).
- **C3.** `paper_v3_prompt.md`:208-209 says the plane decomposition separates
  co-occurrence from frequency; it separates it from the *active share* only.
- **C4.** A builder edit to an existing test: `test_locks.py` now grades the
  interaction configs' β (role added to `CALIBRATED_ROLES`). Keep or revert.
- **C5.** Older items: `README.md` is stale; `LICENSE` names you (the supplement
  ships it with the name scrubbed to "Anonymous Authors"); `phase6_framing_branches.md:69, :75, :82` overclaim (not copied).

## D. Defaults (one line accepts all)

V3Q6 (check in §6.4), V3Q9–V3Q13, V3Q17–V3Q22, v2's carried C1 (§2 accuracy fixes),
D2–D5, E2, E4, F2–F6 and G, as listed in `DISPOSITIONS.md` §4–§5.
