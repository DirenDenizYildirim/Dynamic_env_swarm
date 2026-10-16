# RC1 — claims review, part 1 (Paper v3, step 4.2)

Reviewer lane RC1, 2026-10-14. Read-only except this file. Snapshot reviewed:
`paper/v3/snapshots/draft1/` (the ten in-scope section files are
byte-identical to the live `paper/v3/sections/` copies, checked with `cmp`).
"S/" = `paper/v3/snapshots/draft1/sections/`, "P/" = `.../provenance/`.

## Summary

**Counts:** 2 MUST, 19 SHOULD, 3 OWNER (24 findings), plus a readability
list for newcomers (V3-S7) with 18 sentences and a rewrite for each.

**MUST, one line each:**

- **RC1-1** App. B, S/14_appendix_locks.md:19: "checks each against the
  configurations and the code defaults" is false. The locked d_p = 0.5 has
  code default 0.0, and `test_locks.py` checks code defaults for only four
  constants. v3 turned v2's accurate "or" into "and".
- **RC1-2** Table 2, S/03_environment.md:228: the claim "communication denial
  reads no hazard" cites Listing 6, which shows the frozen message encoder
  and not what T_K reads. The code that shows it is in Listing 5.

**Scope.** `00_abstract.md`, `00_hero.md`, `01_introduction.md`,
`02_related_work.md`, `03_environment.md`, `04_calibration.md`,
`05_measurement.md`, `13_appendix_proofs.md` and both alternates,
`14_appendix_locks.md`, `15_appendix_floors.md`, their provenance files,
`front_matter.yaml` (title, description), and the title candidates in
P/00_abstract.md.

**Method.** I read the following:

- the rules and the record:
  - `paper_v3_prompt.md` in full;
  - `docs/decision_log.md:6036-6244` (PAPER V2 to the end);
  - `paper/v3/BRIEF.md` and `STRUCTURE.md` in full;
  - the orchestrator notes;
- every in-scope sentence against its provenance row. Where v3 changed a
  sentence, I checked the claim at the record: the ledger rows (canonical
  ledger, v2 supplement, `paper/v3/ledger_proposals/W2.md` and `W4.md`), the
  configs, the tests and the code;
- for V3-E2, read-only: `che/env/e2c.py:1-140`,
  `che/bench/results/phase4/phase4_report.md:1-80`, the nesting tests
  (`che/tests/test_nesting.py:78-100`, `test_comms.py:268-320`),
  `test_lethality.py:125-165`, `che/env/env.py:155-175`, and the defaults
  block of `docs/locks.yaml`;
- every RWV line cited in the in-scope provenance (see "§2 citations"
  below).

**Tools run this session:**

- `provenance_check.py --strict` on the live root for the ten files: OK, 0
  problems. On the snapshot root, the only failures are X-row IDs, because
  the snapshot holds no `ledger_proposals/`.
- `v3_checks.py terms`, `dates` and `caveats` on `paper/v3`: all PASS.
- `wordcount.py` on the snapshot.

**V3-E2 verdict (Theorem 1 against `che/env/e2c.py`).** The default statement
in S/13_appendix_proofs.md:166-176 matches the implemented toy. I checked
each point at the source:

- d = 2, ℓ_f = 2, ℓ = 4, horizon 6: e2c.py:22, :79-85; phase4_report.md:27-29.
- Three remembered signals, at t = 0, 1, 2: one smoke step before the first
  observation, e2c.py:52-56.
- The fire-cell distances are 2.83, 2.24 and 2.00 (e2c.py:28-29), and the
  smoke is 1.000, 1.607 and 1.974 (phase4_report.md:40). So
  D_t = distance × ρ/4 = 0.707, 0.898, 0.987, which is X2-2.
- I recomputed q(1) = 1 − 0.507·0.593·0.627 = 0.8115 (X2-3) and the
  integer-distance form's 0.193 (X2-4).
- X2-1 matches phase4_report.md:72.
- The content-channel sentence matches e2c.py:36-43.
- Proof part (3) needs every D_t > 0, as the text says.
- The alternate `alt/13_appendix_proofs.thm1_tf.md` differs only in the
  Theorem 1 block (by `diff`) and states the mismatch accurately.
- The §3.2 one-sentence form (S/03_environment.md:136) is true under both
  options.
- W2's finding is confirmed. No finding on V3-E2 itself, beyond RC1-20
  (wording) and RC1-23 (OWNER).

**V3-F2 abstract check.** The abstract has one question
(S/00_abstract.md:41, sentence 1) and one lesson (:46), drafted on the
identity because the interaction check has not run. The result takes six
sentences, which is long but holds one result with its required qualifiers.

- Registered strings are verbatim: "does not survive the inert-share
  correction", "sign unstable over the final half", "excludes a
  joint-training gain larger than 0.66 points", and "at matched compute".
- The size is stated plainly (X4-3).
- There is no advice, and no "therefore".
- The abstract does not mention the interaction check, so nothing implies
  that the post hoc check is part of the registered test.
- Findings on the abstract: RC1-3, RC1-4, RC1-5, RC1-6 and RC1-22.

**§2 citations.** Every key used in scope is in `submission.bib` (checked by
script). I spot-read every RWV line cited in the in-scope provenance at the
current file:

- intro: :101, :497-498, :628, :638, :675-686, :884-888;
- §2: :253-273, :621-626, :636-650, :658-665, :906-951, :965-976, :984-987,
  :1061-1069;
- §3 and App. A: :291-326, :484-510, :977, :1091-1110;
- §4: :978.

All point at the right entries. W1 and W3 re-pointed the stale v2
references. No stale RWV reference remains in scope. The characterizations
stay inside RWV Part 3, except RC1-12 (VULCAN) and RC1-13 (Gao: "cycling"
is no longer defined).

---

## Findings

### MUST

**RC1-1 (MUST).** S/14_appendix_locks.md:19.

- **What.** "A test in the code supplement (`che/tests/test_locks.py`)
  checks each against the configurations and the code defaults."
- **Evidence.**
  - The code default for the death penalty is 0.0
    (`che/env/config.py:37`: `death_penalty: float = 0.0`), while the locked
    value in the same table is 0.5. `numbers_ledger.md:30` (ENV-1): "che/env/config.py:37
    defaults to 0.0; every live config carries 0.5".
  - `docs/locks.yaml:507-513` lists code-default checks for only `r_comm`,
    `r_seed`, `weak_smooth` and `obs_version`. The test cannot check d_p,
    β̂_c or the analysis constants against a code default.
  - v2 said "against the configurations, the code defaults **or** the
    analysis scripts" (`paper/v2/sections/13_appendix_locks_floors.md:17`).
    P/14_appendix_locks.md row 3 records the change to "and".
- **Fix.** "A test in the code supplement (`che/tests/test_locks.py`) checks
  each against the configurations, the code defaults or the analysis
  scripts that must carry it."

**RC1-2 (MUST).** S/03_environment.md:228 (Table 2).

- **What.** The row "communication denial reads no hazard | 6 (Appendix B)"
  cites Listing 6, which is `che/train/ippo.py:323-329`: the
  `stop_gradient` on delivered messages. That listing shows that the
  message encoder is frozen. It does not show that the communication
  kernel reads no hazard.
- **Evidence.** The code that shows T_K's inputs is in Listing 5
  (S/13_appendix_proofs.md:122-127): `_comms_obs(jax.random.fold_in(key,
  _COMMS_STREAM), pos_new, alive_new, cfg, tl.delta)`, with the comment
  "never h', rho' or c'". STRUCTURE §5 row 6 describes Listing 6 as "the
  message encoder is frozen". Table 2 is described as "the index into the
  code supplement", so a wrong pointer sends the reader to the wrong
  evidence.
- **Fix.** Make the listing cell "5 (Appendix A)". If the frozen encoder
  should be indexed too, add a row: "the message encoder is frozen | 6
  (Appendix B) | `test_comms.py` | —". Check first that a test asserts the
  encoder is frozen; if none does, put "—" in the test cell.

### SHOULD

**RC1-3 (SHOULD).** S/00_abstract.md:41, "visible only in the last fifth of
training".

- **What.** "Visible" reads as "present". But survival Γ(t) is positive at
  every checkpoint from update 650 on (RES-11: signs
  `+ − − + + + + + + + +` over 500–1000). Only its Šidák interval excludes
  zero, and only at t = 900, 950 and 1000 (RES-12). §1 gives the precise
  form, "detectable only at updates 900 to 1000 of 1000"
  (S/01_introduction.md:47), so the abstract and §1 now differ in
  precision.
- **Why SHOULD and not MUST.** The owner's change list says "It appears
  only in the last fifth" (`paper_v3_prompt.md`, V3-F3).
- **Fix.** "…, detectable only in the last fifth of training." Or match §1:
  "…, detectable only from update 900 of 1000."

**RC1-4 (SHOULD).** S/00_abstract.md:41 (the correction sentence) and :46
(the lesson). The lesson does not connect to the result.

- **What.** The lesson says "matching that share alone cannot isolate
  co-occurrence". But the abstract never says that the correction matched
  the share of training with an active stressor (DES-14: ISO-4 and JOINT
  both have active share 1). A reader cannot tell why the lesson follows,
  or what "matching" refers to.
- **Fix.** Rewrite the correction sentence and the lesson. The words are
  about the same in number, which matters with the abstract at its
  250-word cap.
  - Correction: "The correction is an isolated arm trained without the
    third of episodes whose only stressor, communication denial, is inert
    under a frozen random-projection encoder at this scale; it matches the
    joint arm's share of training with an active stressor."
  - Lesson: "Because that share equals the two couplings' frequencies
    summed, less their co-occurrence ($\mu_A + \mu_B - p$), matching it
    alone cannot isolate co-occurrence."

**RC1-5 (SHOULD).** S/00_abstract.md:41, "Keeping that third was our design
error; we registered the correction before any outcome contrast was
computed".

- **What.** A reader can take "registered the correction" to mean that the
  pre-registered test was amended. In fact the correcting arm is a
  sensitivity arm **outside the confirmatory family**, and Γ stays the
  registered test (DES-15; BRIEF §7, "the confirmatory family did not
  change"). §1 has the same gap: "corrected by an arm registered before
  unblinding" (S/01_introduction.md:47). There, "corrected" also implies
  that the design error was repaired, when it was only measured.
- **Fix.**
  - Abstract: "…; we registered the correction, outside the pre-registered
    test, before any outcome contrast was computed."
  - §1: "…, identified before the main training runs; a correcting arm,
    outside the registered test, was registered before unblinding, …"

**RC1-6 (SHOULD).** `front_matter.yaml` `description`.

- **What.** "A pure-JAX multi-agent environment in which collapse seeds
  fire and smoke attenuates perception, every stressor switches off
  exactly, and a pre-registered test serves as a worked example." The last
  clause falls under "in which": the test is not something that happens
  inside the environment.
- **Fix** (one line; no `"`, no `: `, no digit): "A pure-JAX multi-agent
  environment in which collapse seeds fire, smoke attenuates perception
  and every stressor switches off exactly, with a pre-registered test as a
  worked example."

**RC1-7 (SHOULD).** S/00_abstract.md:39 and S/01_introduction.md:45,
"switching a stressor off reproduces the environment without it bit for
bit".

- **What.** In a stochastic environment, "bit for bit" means something only
  under the same random keys. BRIEF §8.1 gives the narrowing the text must
  keep: "under the same random keys, on one backend". The κ_A test also
  compares fire and smoke only (`test_nesting.py:78-88`). §3.4 states all
  of this (S/03_environment.md:193, :216), but the two summary claims drop
  even the keys.
- **Fix.** Add "under the same random keys" to both: "switching a stressor
  off reproduces the environment without it bit for bit under the same
  random keys". That is 5 words each. In the abstract, they can come from
  the gloss in sentence 11; see RC1-22.

**RC1-8 (SHOULD).** S/01_introduction.md:52, "Coupling B's own survival
effect in calibration was not measurable against a three-seed spread".

- **What.** It was measured: −0.03 points (CB-9). It was not
  *distinguishable* from a three-seed spread of 0.72 points, which is not a
  measured floor. "Not measurable" misdescribes the evidence that the
  central limitation rests on.
- **Fix.** "at its severity, Coupling B's own survival effect in
  calibration, −0.03 points, was too small to tell apart from a three-seed
  spread, …". Or, without the number: "…was within a three-seed spread".

**RC1-9 (SHOULD).** S/01_introduction.md:49-52, the hole and the
limitations paragraph.

- **What.** The hole after the worked-example paragraph will hold "one
  sentence: the check's pooled reading … labelled post hoc". Row 21 (:52)
  already says "A post hoc interaction check measures whether the two
  couplings' effects on trained policies add at the test configuration
  (§6.4)." Once the hole is filled, §1 will describe the check twice, in
  two paragraphs. The result will also sit next to the registered result,
  before the reader learns why the check exists (the siting).
- **Fix.** Fill the hole by extending row 21 in place, and delete the
  separate hole slot. For example: "A post hoc interaction check at the
  test configuration measures whether the two couplings' effects on trained
  policies add: <pooled reading per PLAN §7> (§6.4)." This keeps the check
  inside the limitation it answers and out of the registered-result
  paragraph. I checked row 21's design wording against `PLAN.md` §1–§3; it
  matches.

**RC1-10 (SHOULD).** S/03_environment.md:236, "Every trained policy and
evaluation here uses one instance".

- **What.** "Evaluation" overreaches. The corridor toy runs on a 13 × 13
  grid (X2-5). The Prop. 3 check runs on 32 × 32 (CA-3). The percolation
  calibration uses L = 32, 48 and 64 (DX-7). §1 scopes this correctly:
  "Every learned policy" (S/01_introduction.md:52; P/01 row 24).
- **Fix.** "Every trained policy, and every evaluation of one, uses one
  instance: …"

**RC1-11 (SHOULD).** S/04_calibration.md:98, the Remark 2′ sentence.

- **What.** "Remark 2′ (Appendix A) refines a result of Pynadath & Tambe on
  when free communication lowers the complexity of team decision problems:
  under collective partial observability, communication's marginal value
  vanishes when …".
  - Read in one sentence, the clause after the colon looks like Pynadath
    and Tambe's result. Their result is a complexity result: Thm 4,
    collective observability (RWV:978). It is not a value result.
  - "views are redundant" does not match Remark 2′(i)'s conditions. Those
    are: interchangeable, expendable, at least as numerous as the
    hypotheses, team-any reward (S/13_appendix_proofs.md:184).
  - v2 kept the two sentences apart (`paper/v2/sections/07_comms.md:55`).
  - The phrase is the owner's (P/04 row 59), and V3Q4 is pending.
- **Fix** (two sentences): "Remark 2′ (Appendix A) refines Pynadath &
  Tambe, who show that free communication lowers the complexity of the
  team decision problem when the world is collectively observable. For
  collective partial observability, Remark 2′ finds in a two-agent toy
  that communication's marginal value vanishes when the agents are
  interchangeable, expendable and at least as numerous as the hypotheses,
  and returns when roles are irreplaceable or deaths are costly."

**RC1-12 (SHOULD).** S/02_related_work.md:28 (Table 1, VULCAN row).

- **What.** "fire search and rescue, planned by a vision-language model".
  v2's "a proposed approach" was cut. RWV:967: "**VULCAN itself is not
  evaluated** (baselines only; deployment 'ongoing')". The table now
  presents an unevaluated proposal like the evaluated systems around it.
- **Fix.** "proposed fire search and rescue, planned by a vision-language
  model" (one word).

**RC1-13 (SHOULD).** S/02_related_work.md:35, "Policies do compose, and
cycling through factors is generally the most effective strategy".

- **What.** v3 cut v2's sentence that introduced the strategies ("varying
  one factor at a time and cycling through factors so that more
  combinations appear", `paper/v2/sections/02_related_work.md:43`). Now
  "cycling through factors" arrives undefined, as if the reader knew the
  strategy set. RWV:973 supports "Stair 'generally the most effective'"
  only for the named strategy.
- **Fix.** "Comparing data-collection strategies, they find that policies
  do compose and that a strategy cycling through factors, so that more
  combinations appear, is generally the most effective; but their design,
  built for data efficiency, does not separate co-occurrence from how
  often each factor value appears."

**RC1-14 (SHOULD).** S/05_measurement.md:34, the definition of "exclusion
bound".

- **What.** The definition is "When a confidence interval contains zero,
  its larger absolute end is an exclusion bound". Two of the paper's uses
  do not fit it:
  - The registered completion sentence "excludes a joint-training gain
    larger than 0.66 points" uses the interval's **upper** end. RES-1's
    interval is [−4.12, +0.66], so its larger absolute end is 4.12.
  - The registered string "second exclusion bound" refers to X₄ = 0.0488
    (BRIEF §6.1), which is an 80 %-power MDE, a detection limit under §5's
    own terms (BRIEF §9.2 trap 5).
  - The definition comes from BRIEF §5.2, so the scaffold carries the
    conflict.
- **Fix.**
  - §5: "When a confidence interval contains zero, each end bounds the
    effect in its direction: the data exclude a gain larger than the upper
    end and a loss larger than the lower end, at the interval's level; the
    larger absolute end bounds the effect's size in either direction."
  - §6.3 (W4; RC2's lane): say once that the registration's own wording
    calls X₄ an "exclusion bound", and that X₄ is a detection limit.

**RC1-15 (SHOULD).** S/03_environment.md:185, "a death by fire and one by
collapse each cost $-d_p$".

- **What.** "Cost −d_p" is a double negative. Read literally, it says each
  death adds d_p to the reward. The test asserts a reward of −0.5
  (`test_lethality.py:162`).
- **Fix.** "… and a death by fire and one by collapse each change the
  reward by $-d_p$."

**RC1-16 (SHOULD).** S/00_hero.md:22, :29 and S/01_introduction.md:47,
"held-out".

- **What.** The hero's caption and reading note both say "at the held-out
  configuration" before any configuration or training set has been
  introduced. θ\* is defined only in §6.2. A newcomer cannot tell held out
  from what.
- **Fix** (hero caption): "One random-policy episode at the configuration
  the worked example tests (§6), with every stressor on."

**RC1-17 (SHOULD).** S/01_introduction.md:52, "Both isolated arms trained
every coupling episode with links intact".

- **What.** The second isolated arm (ISO-4) has not been introduced. The
  previous paragraph calls it only "an arm trained without them".
  "Coupling episode" is also undefined.
- **Fix.** "The isolated arm and its corrected version trained every
  episode that contained a coupling with communication links intact,
  while the test configuration denies every link: a train/test mismatch
  (§6.2)."

**RC1-18 (SHOULD).** Budgets (V3-S1).

- **What.** `wordcount.py` on the snapshot gives these prose counts against
  STRUCTURE §3:
  - §2: 420 (400), and Table 1 has 122 words in cells (cap 120);
  - §3: 1,129 (1,050);
  - §4: 770 (700), with captions at 213 against 3 × 60;
  - §5: 302 (270).
  - That is about 200 words over in this lane's main text. The writers
    report this, but no file in scope proposes the cuts.
- **Fix.** Take the cuts the writers name: §3's d_p numbers to App. B (60
  words, P/03), §5 row 12 (36 words, P/05), and §4's captions down to 60
  each. Also accept RC1-7, RC1-11 and RC1-13 only together with
  equal-length cuts.

**RC1-19 (SHOULD).** S/13_appendix_proofs.md:184-194, Remark 2′ beside
Theorem 1.

- **What.** In v3 the two now sit 10 lines apart in one appendix. Theorem 1
  defines ℓ_f as the fire's depth beyond the branch. Remark 2′(ii) uses
  "with slack ℓ_f" for a different quantity. P/13 rows 88-89 and V3Q4 keep
  this open.
- **Why it matters now.** In v2 the two statements were in different
  sections. In v3 the reader meets the second meaning a paragraph after the
  first.
- **Fix.** Use another symbol for the slack in Remark 2′ (for example,
  $s$), if V3Q4 keeps the remark.

**RC1-20 (SHOULD).** S/13_appendix_proofs.md:182, "The measured optimal
value matches ½ + ½q".

- **What.** What was measured is the value of the hand-coded policy: walk
  to b; if informed, take the corridor ≠ Z, else L
  (`phase4_report.md:54-55`). The theorem shows that policy is optimal.
  "Measured optimal value" claims that an optimum was measured, which
  sounds like a search over policies.
- **Fix.** "The measured value of the policy the proof shows optimal (if
  informed, take the corridor other than Z; else a fixed one) matches
  $\tfrac12 + \tfrac12 q$, …"

**RC1-21 (SHOULD).** S/03_environment.md:218, "Propositions 2 and 3 and
Theorem 1 are closed forms that the code is tested against".

- **What.** Proposition 2 is an equality in distribution with bond
  percolation, not a closed form. What the test checks is Corollary 1's
  β_c = ½ and the finite-size behaviour (`test_percolation.py`). Table 2's
  row says this correctly.
- **Fix.** "Propositions 2 and 3, Corollary 1 and Theorem 1 are exact
  results that the code is tested against, in toys and at parameters other
  than the locked ones; the paper claims no theory beyond them."

### OWNER

**RC1-22 (OWNER).** The abstract lacks the central limitation (V3-F6).

- **What.** "The test was sited where composition is weak" is to be
  "central, not a caveat" (`paper_v3_prompt.md` V3-F6; PROF 1). STRUCTURE
  §7 allows a short form in the abstract, and W1 left it out for the
  250-word cap (P/00_abstract.md, "Holes"). As it stands, the abstract
  reports "Joint training raises survival" with no hint that, at the test
  severity, Coupling B's own effect was too small to detect (CB-9).
- **Proposal** (17 words): "The test sits where composition is weak: at
  its severity, smoke's own survival effect was too small to detect in
  calibration." Place it after the question sentence.
- **Cuts to pay for it** (about 17 words):
  - the gloss ": each changes sign between checkpoints" (5);
  - "of training" after "final half" (2);
  - "(0.11 of 12 agents)" (4; the "about a tenth" form stays);
  - "As a worked example, we report" → "As a worked example," (3);
  - "Structural" (1);
  - "by Beer–Lambert transmittance" (3).
- The owner chooses.

**RC1-23 (OWNER).** The naming "Remark 2′" (S/04_calibration.md:98;
S/13_appendix_proofs.md:184).

- **What.** Remark 1 is cut, and no Remark 2 exists in the paper. A reader
  meets "Remark 2′" with no 1 and no 2, and the prime signals a variant of
  something the paper never shows. This is part of V3Q4.
- **Proposal.** If the remark stays, call it "Remark 1" or "Remark
  (communication value)". Note the departure from the theory record's
  numbering once in App. A, as the appendix already does for other
  departures.

**RC1-24 (OWNER).** Title candidates (`front_matter.yaml` T1;
P/00_abstract.md:67-71).

- **What.** T1, T1s and T4 say "coupled stressors", and T3 says "coupled
  fire stressors". Only two of the three stressors are coupled to the fire;
  communication denial is independent (Def. 7; S/01_introduction.md:45).
  This is not false, but a reader may take all three as coupled.
- T1 is also 118 characters, which W1 notes is about five printed lines.
- **Proposals:**
  - T1': "A multi-agent fire environment whose collapse and smoke feed the
    hazard, with a pre-registered worked example";
  - or keep T1s and let the `description` carry the example.

---

## Readability for a newcomer (V3-S7)

These sentences in scope cannot be parsed without project context, or bury
the point. Each comes with a rewrite. Rewrites that change a claim are
already findings above, and are marked here by their ID.

1. S/00_abstract.md:41.
   - Now: "Joint training raises survival by 0.96 points …"
   - Problem: "points" of what?
   - Rewrite: "Joint training raises the share of agents alive at the end of
     an episode by 0.96 percentage points …"
2. S/00_abstract.md:41.
   - Now: "The correction removes from isolated training the third of
     episodes whose only stressor, communication denial, is inert …"
   - Rewrite: see RC1-4 (it names the corrected arm and what it matches).
3. S/00_abstract.md:41.
   - Now: "Both differences are sign unstable over the final half of
     training: each changes sign between checkpoints."
   - Problem: which two differences?
   - Rewrite: "Both the survival and the completion differences are sign
     unstable over the final half of training: each changes sign between
     the checkpoints saved there."
4. S/00_abstract.md:46.
   - Now: "Because the share of training with an active stressor equals …
     ($\mu_A + \mu_B - p$), matching that share alone cannot isolate
     co-occurrence."
   - Problem: μ and p are undefined.
   - Rewrite: see RC1-4, or say "(the two frequencies summed, less the
     share with both)" without symbols.
5. S/01_introduction.md:47.
   - Now: "Keeping them was a design error, identified before the main
     training runs and corrected by an arm registered before unblinding,
     the first computation of any outcome contrast (§6.2)."
   - Problem: the appositive dangles.
   - Rewrite: "Keeping them was a design error. It was found before the
     main training runs, and a correcting arm, outside the registered test,
     was registered before unblinding, that is, before any difference
     between arms was computed (§6.2)."
6. S/01_introduction.md:47.
   - Now: "The survival gain does not survive the inert-share correction:
     a third of the isolated arm's training episodes carried only
     communication denial, and against an arm trained without them joint
     training shows no detectable survival difference (§6.3)."
   - Problem: 37 words with two clauses.
   - Rewrite: "The survival gain does not survive the inert-share correction.
     A third of the isolated arm's training episodes carried only
     communication denial; against an arm trained without them, joint
     training shows no detectable survival difference (§6.3)."
7. S/01_introduction.md:52.
   - Now: "The test was sited where composition is weak: …"
   - Problem: "composition" is undefined for a newcomer.
   - Rewrite: "The test was placed where the stressors had little to
     combine: …" (with RC1-8's correction).
8. S/01_introduction.md:52, "Both isolated arms trained every coupling
   episode with links intact …" — see RC1-17.
9. S/02_related_work.md:35.
   - Now: "The DBCA method builds splits whose atom distributions are
     similar and whose compound distributions differ; …"
   - Rewrite: "The DBCA method builds train and test splits with similar
     distributions of single elements and different distributions of their
     combinations; …"
10. S/02_related_work.md:35.
    - Now: "Their attacked arms schedule no clean steps, and their mixed
      arms carry the combined budget, so the design bundles per-modality
      frequency, co-occurrence and a larger budget."
    - Rewrite, staying inside RWV:974 and :1069 (it does not say "perturbed
      at every step"): "None of their attacked training runs schedules
      unattacked steps, and the runs attacked on both modalities carry the
      sum of the single-modality budgets, so per-modality frequency,
      co-occurrence and total budget change together."
11. S/03_environment.md:136.
    - Now: "In a corridor toy built on the same observation code, ignoring
      the attenuated signal costs exactly half the probability of being
      informed before committing, and this cost falls continuously to zero
      as $\kappa_B$ grows (Theorem 1, Appendix A)."
    - Rewrite: "In a two-corridor toy built on the same observation code, a
      policy that remembers the smoke-attenuated signal beats one that
      ignores it by exactly half the probability of seeing the signal
      before it must choose a corridor; that advantage shrinks continuously
      to zero as $\kappa_B$ grows (Theorem 1, Appendix A)."
12. S/03_environment.md:187.
    - Now: "In the one ablation of $d_p$ (the fire alone, 500 updates, 3
      seeds per cell, an older observation encoding, not re-run), raising
      it from 0 to 0.5 moved survival …"
    - Problem: "cell" here means an experimental setting, in a grid-world
      paper; the parenthesis holds five qualifiers.
    - Rewrite: "One ablation varied $d_p$, with the fire alone, 500
      updates, 3 seeds per setting and an older observation encoding; it
      was not re-run. Raising $d_p$ from 0 to 0.5 moved survival …"
13. S/03_environment.md:185, "… each cost $-d_p$" — see RC1-15.
14. S/04_calibration.md:69 (also :84).
    - Now: "In the coupled arm of the Coupling-B calibration grid …"
    - Problem: "coupled arm" is undefined.
    - Rewrite: "In the runs of the Coupling-B calibration grid with
      Coupling B on (500-update policies at each severity, Coupling A on
      throughout), …"
15. S/04_calibration.md:46.
    - Now: "Three estimators committed with the calibration data place the
      critical point between 0.480 and 0.513 …"
    - Problem: "committed" is version-control vocabulary.
    - Rewrite: "Three estimators whose code and data ship with the
      calibration place the critical point …". C31's detection pattern is
      "committed estimator", so keep that phrase in its home sentence:
      "…that no committed estimator reproduces" can stay as it is.
16. S/05_measurement.md:26.
    - Now: "… an acceptance threshold, or bar, is used only with a floor
      measured on the artifact it grades …"
    - Problem: "artifact" is undefined.
    - Rewrite: "… only with a floor measured on the same code and
      configuration it grades …"
17. S/05_measurement.md:36.
    - Now: "A recorded channel becomes evidence only inside a registered
      analysis family …"
    - Problem: "channel" is undefined.
    - Rewrite: "A logged diagnostic becomes evidence only inside a
      registered family of tests …"
18. S/02_related_work.md:35, "cycling through factors" — see RC1-13.

## Checked and found sound (no finding)

- The abstract's and §1's numbers and tags match their rows:
  - RES-1 [−0.0412, +0.0066];
  - RES-2;
  - RES-6 [−0.0068, +0.0063];
  - RES-11 and RES-12;
  - DES-8 (1/3);
  - X4-3 (0.0095531 × 12 = 0.1146);
  - CB-9 (−0.0003, three-seed σ 0.0072);
  - COM-4 (bars twice the M5.5 floors: 2 × 0.0399, 2 × 0.0130);
  - CA-4 (4.05/0.84 = 4.82).
- "Matched compute" appears without any convergence claim.
- "Pre-registered" is attached only to the test.
- No date appears in scope outside the allow-list (the dates check passes).
- Def. 7 with δ = 1 gives the empty link graph, as §1's mismatch sentence
  needs (S/03_environment.md:141). The training δ per arm matches X4-2's
  configs.
- §3.4's narrowing of the nesting claim (keys, one backend, κ_A test on fire
  and smoke, δ against a CPU hash) matches `test_nesting.py:78-88` and
  `test_comms.py:268-320`.
- Death only on a burning or collapsing cell, the basis of the contact-price
  caveat: `env.py:159-173`.
- App. C's attribution "eight reruns, because four leave … ±40 %" is
  supported (DX-303's scope note: "the reason M5.5 bought 8 reps").
- The interaction-check design sentence in §1 (row 21) matches `PLAN.md`
  §1–§3. App. A's index labels App. G "post hoc".
- V3-S6 is met:
  - Remark 1 does not appear in scope.
  - Prop. 4 appears only as an unnumbered remark in words, with its honesty
    note (S/13_appendix_proofs.md:198-200); the no_prop4 alternate differs
    only by that block.
  - Props. 1–3, Cor. 1 and Thm. 1 are kept.
- Double-blind: no URL, name or absolute path in scope. App. A's
  `docs/theory_foundations.md` reference is OWNER-PENDING V3Q16, as marked.

---

## Re-check (fix2)

RC1, step 4.3, 2026-10-16. I compared snapshot `paper/v3/snapshots/fix2/` with draft1, using the saved diff (`scratchpad/diff_draft1_fix2.txt`), and read the writers' outcomes in `paper/v3/review/resolutions_W1.md`–`W5.md`. The ten in-scope section files in fix2 are byte-identical to the live `paper/v3/sections/` files (checked with `cmp`). I re-reviewed only lines that changed. Citations below are fix2 `file:line`.

Checks run on the live tree in this round:
- `provenance_check.py --strict` on the ten in-scope files: OK, 0 problems.
- `v3_checks.py` terms, dates and caveats: all PASS.
- `wordcount.py` (prose words against budget):

| section | prose words | budget |
|---|---|---|
| abstract | 234 | 250 |
| §1 | 587 | 600 |
| §2 | 400 | 400 (Table 1: 119) |
| §3 | 1,040 | 1,050 |
| §4 | 700 | 700 |
| §5 | 269 | 270 |

### Verdicts on the original findings

| finding | verdict | note |
|---|---|---|
| RC1-1 (MUST) | OK | `14_appendix_locks.md:19` now reads "the configurations, the code defaults or the analysis scripts that must carry it". |
| RC1-2 (MUST) | OK | Table 2 (`03_environment.md:187`) now points to Listing 3, the step listing in App. A, whose `_comms_obs(..., pos_new, alive_new, cfg, tl.delta)` reads no hazard. W2's reason for adding no encoder row holds: no test asserts the `stop_gradient`. See new finding RC1-26 for what that cut leaves behind. |
| RC1-3 | OK | `00_abstract.md:42` now says "detectable only in the last fifth". §1 adds "the checkpoints at updates 900 to 1000". |
| RC1-4 | OK | The correction sentence now names the arm and the matched share, and the lesson refers back to it. A new referent problem follows: see RC1-29. |
| RC1-5 | OK | Abstract: "registered the correction, outside the pre-registered test, before …". §1: "a correcting arm outside the pre-registered test was registered before unblinding". "Corrected by an arm" is gone. |
| RC1-6 | OK | `front_matter.yaml:18` now reads "…in which collapse seeds fire, smoke attenuates perception and every stressor switches off exactly, with a pre-registered test as a worked example." |
| RC1-7 | OK | "under the same random keys" added in both places. §3.4 (`03_environment.md:173, :175`) keeps the one-backend limit, the κ_A fire-and-smoke limit and the δ CPU-hash limit. |
| RC1-8 | OK | Now "within a three-seed spread" (CB-9). |
| RC1-9 | OK | The separate hole slot is gone. The HOLE now follows the check sentence, with a note to extend that sentence in place (`01_introduction.md:49`). |
| RC1-10 | OK | `03_environment.md:195`. |
| RC1-11 | OK | `04_calibration.md:98` now has two sentences. Pynadath & Tambe's result is stated as a complexity result (RWV:978). Remark 2′'s conditions match App. A (interchangeable, expendable, at least as numerous as the hypotheses). The V3Q4 marker is in place. |
| RC1-12 | OK | "proposed" restored (`02_related_work.md:28`). |
| RC1-13 | OK | "Comparing data-collection strategies, they find … a strategy cycling through factors, so that more combinations appear, is generally the most effective" (RWV:973). The v2C1 marker is kept. |
| RC1-14 | OK | W3's part: the §5 definition now gives a bound for each end and the size bound, which fits the registered "gain larger than 0.66". W4's part: `07_example_results.md:58` names X₄ "the registration's term for its detection limit". |
| RC1-15 | OK | "a death by fire or by collapse changes the reward by $-d_p$". |
| RC1-16 | OK | Hero: "the test configuration of §6". §1: "a near-critical configuration neither arm trained on". The abstract keeps "held-out near-critical severity", which is acceptable because the abstract states what is held out. |
| RC1-17 | OK | `01_introduction.md:49`, in my wording. |
| RC1-18 | OK | Every in-scope main-text file is now within its prose budget (counts above). Caption totals are RM's to grade. |
| RC1-19 | OWNER | W2's reason holds. The theory document itself writes "with slack ℓ_f" (`docs/theory_foundations.md:497-501`), so renaming the slack would decide part of V3Q4. The V3Q4 marker is in place. |
| RC1-20 | OK | Fixed in the main file and in both alternates (one hit each). |
| RC1-21 | OK | `03_environment.md:177`. |
| RC1-22 (OWNER) | OWNER | Marker `OWNER-PENDING:V3Q7 also RC1-22 / RC2-18` at `00_abstract.md:41`. The options are recorded in the provenance "Holes" section. |
| RC1-23 (OWNER) | OWNER | The V3Q4 marker is kept. App. A now explains the numbering (`13_appendix_proofs.md:52`), but see RC1-27. |
| RC1-24 (OWNER) | OWNER | T5 and T6 are added, and neither says "coupled stressors"; V3Q1 is in place. W1 is right that my proposed T1′ was wrong: smoke does not feed the hazard, it attenuates perception (Def. 6). I withdraw T1′. |
| Readability 1, 2, 4, 5, 6, 8 | OK | The abstract now says "percentage points". The §1 sentence is split. Items 2, 4 and 8 are covered by RC1-4 and RC1-17. |
| Readability 3 | OK-DECLINED | "Both differences" now comes right after the completion sentence, and the survival result opens the paragraph. That reads acceptably. |
| Readability 7 | OK-DECLINED | C01's detection phrase "sited where composition is weak" is required in its short form, and §1's first paragraph sets up co-occurrence. |
| Readability 9, 10, 12, 14–18 | OK | Each was checked at its changed line. Item 10 stays inside RWV:974 and :1061-1069. |
| Readability 11 | OK-DECLINED | §3 is at its budget, and the sentence is correct. |
| Readability 13 | OK | Same fix as RC1-15. |

### New findings in the changed lines

**RC1-25 (MUST).** `03_environment.md:104` reads: "…collapses nine times as often as an empty one,. Below the percolation threshold…".

- **What is wrong.** There is a stray ",." left over from cutting the CA-9 clause. The same text is in the live file. This is garbled print text.
- **Fix:** "…collapses nine<!-- N:CA-8 --> times as often as an empty one. Below the percolation threshold…"

**RC1-26 (SHOULD).** §3.2 no longer describes the frozen message encoder.

- **What changed.** The fix round cut "The message head receives no gradient, so agents send a fixed random projection of their trained features (Appendix B)." (draft1 `03_environment.md:146`).
- **Why it matters.** §1 (`01_introduction.md:49`) and §4.4 (`04_calibration.md:96`) use the ruled phrase "inert under a frozen random-projection encoder at this scale". A newcomer now meets "frozen random-projection encoder" with no definition and no pointer anywhere in the main text. The definition sits only in App. B (`14_appendix_locks.md:69`).
- **Fix (cheapest):** add a pointer at the ruled phrase's home in §4.4: "…'inert under a frozen random-projection encoder at this scale' (the encoder: Appendix B) in this sense only: …". That costs 4 words.
- **Alternative:** restore a 16-word sentence after `03_environment.md` "$T_K$ reads positions and aliveness only…": "No gradient reaches the message head, so messages are a fixed random projection of trained features (Appendix B)."

**RC1-27 (SHOULD).** `13_appendix_proofs.md:52` reads: "…this is why Definition 2 follows Definition 7 in §3 and the one remark is numbered 2′."

- **What is wrong.** The default appendix, and the thm1_tf alternate, also hold the unnumbered remark "A transfer bound for a fixed policy (remark)" (`13_appendix_proofs.md:243`; `alt/13_appendix_proofs.thm1_tf.md:217`). So there are two remarks, and "the one remark" is false in two of the three versions. It is true only in no_prop4.
- **Fix:** "…and the one numbered remark is numbered 2′." The same edit goes in both alternates, which carry the sentence at `:26`.

**RC1-28 (SHOULD).** `05_measurement.md:28` and §5 as a whole.

- **What is wrong.** The cut floor-coverage sentence was the only main-text statement of which acceptance thresholds lack a floor. §5 now states the rule universally: "an acceptance threshold, or bar, needs a floor measured on the artifact it grades, for that metric and GPU, or the analysis is declared underpowered".
- **Why it matters.** Some thresholds have neither a floor nor an underpowered flag: the ISO-4 contrasts and the drift diagnostics (App. C, coverage bullet). The calibration contrasts of §4.2 and §4.3 are called "ungraded" or "no reproducibility floor" in their own sections. BRIEF §8.1 asks the text to "name which bars have floors, never 'every bar'".
- **Fix (10 words, against the 1 word of room):** append "Not every threshold in this paper has one; Appendix C lists which." This needs a 9-word cut elsewhere in §5, or the owner accepts 278 against 270. One candidate cut: "computed on the contrast's own standard error," could become "on the contrast's standard error,".

**RC1-29 (SHOULD).** `00_abstract.md:47` reads: "Because that share equals the couplings' frequencies summed, less their co-occurrence ($\mu_A + \mu_B - p$), matching it alone cannot isolate co-occurrence."

- **What is wrong.** "That share" points back to "the joint arm's share of training with an active stressor" in the correction sentence. Three sentences already sit between them, and the HOLE's post hoc sentence will be inserted before the lesson (the HOLE note at :45 says so). The referent will then be four or five sentences back.
- **Fix:** "Because the share of training with an active stressor equals the couplings' frequencies summed, less their co-occurrence ($\mu_A + \mu_B - p$), matching it alone cannot isolate co-occurrence." That is 5 more words; the abstract is at 234 against 250.

**RC1-30 (SHOULD).** `00_abstract.md:42` reads: "…whose only stressor, communication denial, had no detectable effect, …".

- **What changed.** The ruled phrase was replaced, which is allowed (resolutions_W1). But the plain form drops the phrase's scope, and states as a flat fact what rests on coarse four-seed thresholds at about half power, measured in calibration (COM-4, V4-1).
- **Fix (2 words):** "…had no detectable effect in calibration, …".

**RC1-31 (SHOULD, minor).** Two wording problems in §1 and §2:

- `01_introduction.md:47`: "The completion difference shows no detectable change and excludes…". A difference does not "show a change". Fix: "Completion shows no detectable change, and the difference excludes a joint-training gain larger than 0.66 points." The registered string is unchanged.
- `02_related_work.md:37`: "…we mean none found by that search." The sentence that named "the search described in Appendix I" in this paragraph was cut, so "that search" now points two paragraphs back. Fix: "…none found by the search of Appendix I."

### Counts (re-check)

- Original findings (24):
  - OK: 20 (RC1-1 to RC1-18, RC1-20 and RC1-21; RC1-14 counted once for its two parts).
  - OWNER: 4 (RC1-19, RC1-22, RC1-23, RC1-24).
  - REOPEN: 0.
- Readability items: 15 OK, 3 OK-DECLINED (items 3, 7 and 11).
- New findings: 7. One MUST (RC1-25) and six SHOULD (RC1-26 to RC1-31).
