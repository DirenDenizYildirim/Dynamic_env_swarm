# VENUE REVIEW II — rolling venues, pre-grid, pre-unblind (2026-08-24)

**Status: an assessment, not a ruling.** Nothing in this document changes a
constant, a config, a lock, an analysis family or a threshold. `SIDAK_M`,
`K_CONFIRMATORY`, `K_SECONDARY`, `T_STAR`, `m62_report.py::METRICS` and every
entry in `docs/locks.yaml` are untouched. The decision it prompted is
transcribed separately in `docs/decision_log.md` (*VENUE RULING II*,
2026-08-24) and binds from that entry, not from this file.

**Written pre-grid and pre-unblind.** `run_p6_grid.sh` has not run, there is no
box, and no Phase-6 outcome mean exists. That timing is the whole reason this
document is worth writing: it preserves the one property the 2026-08-16 ruling
was built to have.

**Provenance.** Every venue fact below was read from the venue's own page on
2026-08-24 and carries its URL. Per the derived-numbers sub-rule (2026-07-28),
nothing is transliterated from memory or from a search summary; §5 records
what could **not** be verified, and one claim from the chat that prompted this
review is retracted there.

**Scope.** This review compares **rolling** venues only. It does not reopen
the RA-L/IROS demotion, whose grounds (`decision_log.md`, *VENUE RULING* §1–2)
are structural and independent of which ML venue is primary.

---

## 1. Why the 2026-08-16 ruling is reopened at all

Not because of an outcome — there is none. Two reasons, both dated after it:

1. **A rolling venue with the same contribution type was never assessed.**
   `venue_review_2026-08-16.md` §1's table considered NeurIPS D&B, TMLR,
   AAMAS, RLC and RA-L/IROS. **DMLR** — the JMLR-family journal whose stated
   scope names reinforcement learning environments — is absent from it. That
   is a gap in the assessment, not a change in the world.
2. **A deadline primary charges a full cycle for a rejection.** With ~7 months
   of runway (`CLAUDE.md`) and one grid's worth of results, the cost of a
   D&B rejection is the calendar, not the review. A rolling primary converts
   that into a sequential retry.

**Neither reason is outcome-conditional, and both were available on
2026-08-16.** This is a correction to an assessment, which is why it can be
made now without weakening the blind.

---

## 2. The three rolling venues, as verified

| | TMLR | DMLR | JAAMAS |
|---|---|---|---|
| submission | rolling (OpenReview) | rolling (OpenReview) | rolling (Springer) |
| blinding | **double-blind**, submissions must be anonymized | **single-blind** | not verified |
| page limit | **no strict limit** — "may be any length, but a paper's length should be justified by its content" | none stated | not verified |
| total time to decision | **not stated** (see §5) | **stated 4–6 months**, up to 10 exceptional | not verified |
| parallel submission | **forbidden** at any archival peer-reviewed venue | not verified | not verified |

### TMLR — acceptance criteria, quoted

Two, and only two:

> (i) "Are the claims made in the submission supported by accurate, convincing
> and clear evidence?"
> (ii) "Would some individuals in TMLR's audience be interested in the findings
> of this paper?"

Criterion (ii) is described as subjective, **with reviewers advised to assume
it satisfied when uncertain.** The criteria page explicitly declines
"significant", "impactful" and "novel" as rejection grounds, and states that
work need not achieve state-of-the-art or introduce a novel method.

Stage deadlines: action editor assigned **within a week**; final recommendation
**once at least two weeks have elapsed after all 3 reviews became public**. No
total is published.

Originality rule, and it is load-bearing for §4: submissions may not reuse text,
figures or results from any paper "published, accepted for publication, or
**submitted in parallel** at another archival, peer-reviewed venue". Overlap
with non-archival venues (workshops, preprint servers) is permitted — but the
anonymization rule forbids linking the submission to a non-anonymous preprint.

### DMLR — scope, quoted

The submissions page lists among its categories **"Data generators and
reinforcement learning environments"** and **"Benchmarking tools and
methods"**. Acceptance additionally requires documentation of collection,
organization, availability and maintenance; reproducibility with code and
evaluation procedures; and a limitations/ethics treatment.

Activity: DBLP lists volumes 1 (2024), 2 (2024/2025) and 3 (2026) — three
volumes in roughly two years. **Low throughput is a fact about the venue's
establishment and is recorded as a risk, not as a defect.**

### JAAMAS — assessed and not pursued

Scope fit is genuine: the journal names multi-agent learning and agent
decision-making architectures, and the JAAMAS track at AAMAS admits extended
abstracts of articles accepted in the 12 months preceding the notification
date, non-anonymous, 2 pages plus references, with an underlying article that
must not extend an archival conference paper (which this would not).

It is declined on **this project's own recorded evidence**, not on fit:

- `venue_review_2026-08-16.md` §6 item 2 — *"No baseline outside the project's
  own two arms... no PLR/ACCEL-style curriculum, no robustness method.
  Acceptable at a benchmark venue where the environment is the contribution;
  **thin at AAMAS/IROS**."* JAAMAS is the AAMAS community's journal, so the one
  recorded reviewer-facing weakness lands hardest exactly there.
- §6 item 4 — the UED / domain-randomization related-work hole is a hole in
  front of the readership most likely to know that literature.
- A journal that scores an agent-theoretic **claim** reads a benchmark as
  supporting infrastructure. The modal branch is **C**, a null (§3 below). A
  claims venue plus a null claim plus a benchmark read as infrastructure is the
  worst of the three combinations.
- Timelines could not be verified at all, against a ~7-month clock.

---

## 3. Fit against what this project actually holds

Unchanged from the prior review and restated because it decides the ordering:
the modal branch is **C** (`venue_review_2026-08-16.md` §5), and the tier-1
payload — eight items, `phase6_framing_branches.md` §2 — is largely
**artifact and measurement** contribution rather than claim.

**The two venues fail in opposite directions, and neither failure is fatal:**

- **TMLR grades claims and does not grade the artifact.** Neither criterion
  asks a reviewer to evaluate the environment *as a benchmark* — documentation,
  hosting, licence, maintenance, reusability. The eight tier-1 items would be
  accepted as well-supported claims and the artifact itself would go
  unassessed. If adoption of the CHE environment is a goal, TMLR reviews the
  paper and ignores the thing.
- **DMLR grades the artifact and is young.** Its stated scope contains this
  contribution type verbatim, and its acceptance criteria are close to a
  transcription of the benchmark-track deliverables already owed
  (`decision_log.md`, *VENUE RULING*, owed item 2) — so the fit costs no new
  work. Against that: three volumes in two years, and a stated 4–6 month
  expectation that consumes most of the runway in one attempt.

**Where branch C can die at TMLR, precisely.** Criterion (ii). The criteria
page's own worked example separates a plain reproduction (insufficient
interest) from a systematic robustness study with actionable insights
(sufficient). Branch C is a calibrated instrument plus a well-powered
exclusion, sited at the one severity where both live elements are individually
quiet (§4a, branch-invariant). That reads as the second example, not the
first — but it is the single place an action editor could press, and the
instruction to resolve uncertainty in the author's favour is what makes the
risk small rather than absent.

---

## 4. The ordering argument, and the part of it that did not survive verification

TMLR's originality rule **forbids parallel submission** to another archival
peer-reviewed venue. So the two are strictly **sequential** regardless of
preference, and the only question is which is attempted first.

**The surviving leg.** TMLR's criteria eliminate the dominant rejection risk
for this paper: there is no novelty bar, no significance bar, no SOTA
requirement, and the one subjective criterion carries an explicit
assume-satisfied default. For a paper whose surplus is rigour and whose modal
result is a null, that is the highest-probability first attempt available.

**The leg that failed.** The claim that TMLR turns around fastest, and
therefore that a TMLR rejection still leaves room for DMLR inside the runway,
**is not supported by anything either venue publishes.** TMLR states stage
deadlines and no total; DMLR states a total of 4–6 months. A comparison cannot
be made from those two. The ordering above rests on acceptance probability
alone, and **the sequencing benefit is unquantified** until §5's owed check is
discharged.

This is recorded rather than smoothed over because the ordering is the
operative content of the ruling, and one of its two supports is missing.

---

## 5. What this review is blind to, and one retraction

- **TMLR's total time to decision is unverified and unpublished.** An owner
  task: obtain it from TMLR's published statistics or from the OpenReview
  record, not from an estimate. Until then no runway arithmetic involving TMLR
  may enter any document.
- **RETRACTED, from the chat that prompted this review:** *"TMLR turns around
  fastest"* and a "~2–3 months" figure attached to it. Both were asserted from
  memory before the editorial policies were read, and neither is supported.
  They appear in no document and are recorded here so the retraction is
  auditable.
- **CORRECTED, same chat:** the Journal-to-Conference track was first described
  as materially changing TMLR's standing. Verified, it does not carry that
  weight — see §6.
- **No base rates were consulted** for any venue. Every judgement here is from
  fit and from published policy.
- **JAAMAS was assessed from scope and the AAMAS track CfP only.** Its page
  limit, blinding and timelines are unverified; the decline rests on fit
  arguments that do not depend on them.
- **The reviewer read the repository, not the paper.** No paper exists in this
  tree — unchanged from the prior review, and still the largest blindness in
  both.

---

## 6. The Journal-to-Conference track, verified — do not price it in

Announced 2025-10-21 (TMLR news); the rules were read from the track's own
page on 2026-08-24:

- Eligible journals: **JMLR or TMLR**, including JMLR MLOSS.
- Published no earlier than **2025-01-01**, the window rolling annually to a
  maximum span of two years.
- A TMLR paper requires **"a J2C Certification, Featured Certification or
  Outstanding Certification"** — that is, at least one certification. It is not
  available to an ordinary acceptance.
- The format is typically a **poster**, and the track "shall not be considered
  as being published in the proceedings of the chosen conference."

**Reading.** It is a conditional visibility bonus, not a recovery of
conference standing, and the condition is a selective certification that no
design decision can secure in advance. It is therefore **not a ground** for
the ruling and is recorded so that it is not later mistaken for one.

---

## 7. What follows for the owed list

- **Positioning ruling 6b (anonymity, no repo links) stands and its conflict
  closes.** TMLR is double-blind and requires anonymized submissions,
  including anonymized supplementary code. The 6a/6b tension the 2026-08-16
  ruling left open — a benchmark track possibly *requiring* artifact access —
  does not arise under a TMLR primary. It **returns** if the DMLR fallback is
  exercised, since DMLR is single-blind and requires availability
  documentation.
- **Positioning ruling 6a's page budget is fully discharged** as a constraint:
  TMLR states no strict limit. The appendix-manifest strategy is unconditional
  under the primary.
- **The CfP-mechanics owed item shrinks** to §5's timeline check.
- **The benchmark-track deliverables (owed item 2) become optional under the
  primary and required under the fallback.** They are worth doing regardless:
  they are the artifact's adoption path, which is the one thing a claims venue
  will not supply.
- **Unchanged and still owed:** the IEEE Xplore query, the JaxWildfire and
  arXiv:2604.26150 PDFs, and the four relayed citations. §6 item 6 of the prior
  review — an unverified bibliography — remains the highest-severity
  non-technical risk in the project and is untouched by any venue decision.
