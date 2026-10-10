# Writing drafts (working record; never ships)

Kept under the *DRAFTS FILE* ruling (`docs/decision_log.md`, 2026-10-06).
The owner drafts in the chat; each draft is appended here **verbatim** in
the same turn, with the date, the step, and the builder's open check
findings beside it, labelled as the builder's. Entries are appended, never
edited. A section the owner calls done is copied from here into
`paper/finale.md`.

---

## 2026-10-10 · Title · draft 1

Owner's draft, verbatim:

```text
A Multi-Agent Environment with Causally Coupled Hazards and a Pre-Registered Test of Joint versus Isolated Training
```

**Builder's check findings (the builder's, not the owner's text; open):**

1. **Conflict, misreading risk: "Joint versus Isolated Training" has no
   object.** After "Multi-Agent", the default MARL reading is joint vs
   independent *learners*. The study holds that fixed: every arm is the same
   shared-parameter IPPO (ENV-11). What varies is which elements share a
   training episode (D2; DES-7). The second reading, from "Hazards", is
   joint vs isolated *hazards*, but the fire burns in every episode (D1); the
   composed elements are Coupling A, Coupling B and comms denial.
2. **Conflict with the record's terms, minor: "Causally Coupled Hazards".**
   Def. 2's "the hazard" is the fire (h) alone. Collapse is lethal
   (`deaths_collapse`, `che/env/env.py:183`) but is the structure state c.
   Coupling A links collapse to fire; Coupling B links the fire's smoke to
   perception, not to another hazard; comms denial is independent. The plural
   holds only if the paper defines "hazards" as fire and collapse, and then
   "coupled" names Coupling A only.
3. **Undersell (suggestion): Def. 2 is absent.** The record names the
   hazard-outside-reward-and-cost property as what separates the setting
   from CMDP/safe RL and JaxWildfire (`docs/theory_foundations.md`, Def. 2).
   Without it, "hazards" takes the field's default reading. Acceptable if
   `description` or the abstract carries it.
4. **"Pre-Registered": supported at this level.** The JOINT-vs-ISO test is
   the confirmatory Γ, registered 2026-08-13, pre-grid (DES-12). Binds
   elsewhere: the body states the registration's form (committed documents;
   no external registry found in the repository) and its deviations,
   k 40 → 46 → 72 (DES-1 to DES-3) and ISO-4 added mid-grid outside the
   family (DES-15).
5. **Passes.** Missing: none (no result claimed, so the inert-share
   qualifier and the Γ(t) suffix do not bind the title). Numbers: none.
   Mechanics: one line, no `"`, `$`, `{{` or `{%`; names no environment,
   so repository visibility does not bite the title. No "swarm", PBT or
   "adversary". Typos and grammar: none; title case consistent.

Open items: "swarm" is settled for the title if this wording stands;
"ambient" is still unratified (not used here; it bites at the abstract);
repository visibility still unanswered (it bites wherever the name appears).

## 2026-10-10 · Title · owner's answer (not a draft)

Repository visibility, asked under draft 1: "the repo will go private"
(decision log, REPO VISIBILITY). Draft 1's open item on visibility is
**resolved**; naming the environment stays the owner's choice wherever the
name could appear.

## 2026-10-10 · Title · draft 2

Owner's draft, verbatim:

```text
A Multi-Agent Fire Environment with a Hazard-Blind Reward, and a Pre-Registered Test of Training on Co-occurring versus Isolated Stressors
```

**Draft 1's findings:** 1 (no object for joint/isolated) **resolved**:
"co-occurring versus isolated" is the D2 design (co-occurrence 1.0 in JOINT,
0.0 in ISO; config headers, DES-7). 2 ("hazards" plural) **resolved**.
3 (Def. 2 absent) **resolved**. 4 ("Pre-Registered") unchanged: supported
(DES-12), and binds the body.

**Builder's check findings (the builder's, not the owner's text; open):**

1. **Conflict with the record's terms: "Stressors" has three senses in the
   record.** Def. 2 names the fire itself "an ambient survival stressor"
   (`docs/theory_foundations.md:56, :68`). The theory doc calls
   θ = (β, κ_A, κ_B, δ), the fire's β included, the "stressor
   configuration" (:23). D1 calls the composable set {Coupling A,
   Coupling B, comms denial} "elements". "Isolated stressors" is true only
   in D1's sense: in every ISO episode the fire co-occurs with the one
   element (D1). The paper needs one sense, and if "stressors" means the
   elements, Def. 2's name for the fire moves with it. That name is the
   open "ambient" item, so the two decisions are linked.
2. **Undersell (suggestion): the couplings are gone.** "Fire Environment"
   names the substrate. The causal couplings (collapse seeds fire; smoke
   attenuates perception), which are both the environment's mechanism and
   what the test composes, appear nowhere, and "Stressors" does not say what
   they are. The task (foraging, ENV-9) is also unnamed; "Hazard-Blind
   Reward" keeps "Fire Environment" from reading as a monitoring or
   suppression task. Acceptable if `description` or the abstract carries
   the couplings.
3. **"Hazard-Blind Reward": supported.** It is the ruled term (DEF. 2
   WORDING RULING, 2026-09-27). Binds elsewhere: the body states the
   cause-blind death penalty, d_p = 0.5 (ENV-1; `branch_B.md` §5 item 6),
   and Def. 2's other half (no cost or constraint channel), which "Reward"
   does not cover.
4. **Typos and grammar: hyphenated compounds capitalized inconsistently.**
   "Multi-Agent", "Hazard-Blind" and "Pre-Registered" capitalize the second
   part; "Co-occurring" does not. The comma before "and" is not an error: it
   keeps the test from reading as a second thing the environment is "with".
5. **Passes.** Missing: none (no result claimed). Numbers: none. Mechanics:
   one line, no `"`, `$`, `{{` or `{%`; 19 words, 138 characters (no TMLR
   or OpenReview title limit has been checked). Double-blind: names nothing.
   No "swarm", PBT or "adversary".

Open items: "ambient" is still unratified and now tied to finding 1;
"swarm" is settled for the title if "Multi-Agent" stands.

## 2026-10-10 · Title · draft 3

Owner's draft, verbatim:

```text
A multi-agent fire environment with a hazard-blind reward, and a pre-registered test of training on co-occurring versus isolated stressors
```

Same words as draft 2, in sentence case.

**Draft 2's findings:** 4 (capitalization) **resolved**: sentence case is
consistent. 1 ("stressors" has three senses) **pending the owner's ruling**
on the proposal sent with this draft: "stressor" means the elements you
combine; Def. 2 is renamed (proposed "ambient hazard"); θ is renamed
(proposed "environment configuration"). Not transcribed yet, so not binding.
2 (couplings absent, suggestion) **open**. 3 ("hazard-blind reward") binds
the body, unchanged. 5 (passes) unchanged.

**Builder's verification of that proposal (the builder's notes):**
- Correct: POSITIONING RULINGS §3 kept "stressor" for the ecology
  multiple-stressors analogy (log:2527-2529); its two verified works,
  Crain et al. 2008 and Côté et al. 2016, are in `submission.bib`.
- Correct: the spine abstract says "co-occurring stressors" (spine:66).
- Not mentioned, and supporting: the registered documents already use the
  elements sense (`phase6_framing_branches.md:108`; `phase6_design_v2.md:26,
  :106`), and so does the code (`che/env/types.py:38`, `che/env/config.py:163`).
- Count corrected: "about 19 places" is every occurrence in the theory doc,
  spine, `branch_B.md` and `submission.md`, but most are already in the
  elements sense. What changes is Def. 2's name (theory doc :56, :63, :68;
  spine :52, :215; `submission.md:68`) and θ's name (theory doc :23). The
  proposal misses the θ docstrings in `che/env/config.py:3, :22` and three
  fire-sense uses in `paper/related_work_verification.md` (:154, :864, :871).
- Correct: under it, "isolated stressors" is literally true; each ISO
  component carries exactly one element (`che/configs/p6_iso.yaml:41-46`).
- A cost it does not state: "survival" leaves Def. 2's name.

## 2026-10-10 · Title · called done

Owner's final text, verbatim:

```text
A multi-agent fire environment with a hazard-blind reward, and a pre-registered test of training on co-occurring versus isolated stressors
```

Identical to draft 3. Copied into `paper/finale.md` (YAML `title`).

**Draft 3's findings, closed:** 1 ("stressors" has three senses)
**resolved by ruling** (TITLE AND TERMINOLOGY RULINGS: "stressor" names the
composable elements; Def. 2 is the "ambient hazard"; θ is the "environment
configuration"). 2 (couplings absent, suggestion) **closed by the owner's
choice**: the title is final without them; the abstract or `description` can
carry them. 3 ("hazard-blind reward") still binds the body: the cause-blind
d_p = 0.5 and Def. 2's no-cost-or-constraint-channel half.
"Pre-registered" also binds the body: the registration's form and its
deviations (DES-1 to DES-3, DES-15).

The owner asked for the builder's view on "fire"; given in the session
(keep it).

## 2026-10-10 · Abstract · draft 1

Owner's draft, verbatim:

```text
We introduce CHE, a pure-JAX multi-agent reinforcement-learning environment in which a cellular-automaton fire is causally coupled to structural collapse (collapse seeds fire) and to perception (smoke attenuates observations by Beer–Lambert transmittance), alongside an independent communication-denial axis. The fire is an ambient hazard: no cost or constraint channel carries it, and the reward is blind to it, reading only task variables and agent deaths, which it penalizes equally whatever their cause. Severity levels are placed relative to a measured percolation threshold, each stressor is a parameter of one transition kernel so that ablations are bitwise-exact nested models, and results are graded against reproducibility floors measured per metric, per GPU and per artifact. Calibration also shows that collapse-seeded fire limits itself: seeded ignitions per episode fall 4.8-fold from low to high severity. We then pre-register a test of whether training on co-occurring stressors beats training on each in isolation, at a held-out severity and matched compute, with 72 seeds per arm (raised before unblinding from the registered 40). Joint training raises survival by 0.96 points (Šidák-corrected 95 % CI [0.47, 1.44]); task completion shows no detectable change (−1.73 points, CI [−4.12, +0.66]). This gain does not survive an inert-share correction registered before unblinding. Because communication denial is inert under our frozen random-projection message encoder, a third of the isolated arm’s training episodes contain no active stressor. Removing them, in a 20-seed sensitivity arm, raises isolated training’s survival by 0.98 points, and joint training then differs from it by only −0.03 points (CI [−0.68, +0.63]), although it still sees each coupling twice as often and always in combination. Neither outcome’s difference keeps a stable sign over the final half of training: the survival gap opens only in the last fifth of the budget, and completion leans negative from 70 % of it onward. Studies of compositional generalization should match the share of training that contains an active stressor before attributing a gain to composition. Code, configurations and the frozen analysis plan are provided as anonymized supplementary material.
```

334 words, 2,267 characters.

**Builder's check findings (the builder's, not the owner's text; open):**

1. **Conflict: "results are graded against reproducibility floors measured
   per metric, per GPU and per artifact".** (a) The confirmatory Γ is graded
   on its own seed-dispersion SE; floors are the beat-reproducibility hurdle
   (HW-1) and a design-stage bound (`CLAUDE.md`, 2026-08-03 amendment and
   corollary). (b) The next sentence's own finding cannot be floor-graded:
   m44 has no identical-rep set, so the 4.83× is labelled REFERENCE SCALE
   (`che/bench/results/e1/e11_report.md:113-121`). (c) CB-9 was graded
   against a 3-seed σ_seed, not a measured floor.
2. **Conflict, attachment: "Neither outcome's difference keeps a stable
   sign …".** The registered suffix belongs to Γ (JOINT − ISO). The sentence
   follows the Γ₄ sentence, so "difference" and "the survival gap" read as
   JOINT − ISO-4, which is ≈ 0. "Difference" names no arms.
3. **Conflict with Def. 2: "The fire is an ambient hazard: …"** defines
   "ambient" by clause 1 only. Clause 2, non-adversarial (a fixed kernel,
   nothing optimizing), is the half that separates the setting from
   robust/minimax MARL and from the adversarial neighbour (Erdem & Üre).
4. **Overreach, mild: "only −0.03 points".** The CI is stated, but "only"
   leans on the point estimate. Γ₄'s upper end (+0.63) is above Γ's lower
   end (0.47), so the correction does not exclude a composition share of
   that size; Γ₄ is an exclusion, not an absence (`branch_B.md` §8).
5. **Overreach, mechanism: "collapse-seeded fire limits itself".** The
   confirmed mechanism, registered before the measurement, is that the
   supercritical fire consumes the fuel collapse would ignite
   (`e11_report.md:18-24`): the fire limits Coupling A's seeding. The counts
   come from trained policies (m44, coupling-enabled arm, 500 updates),
   replicated in m35 (CA-5).
6. **Missing scope: comms "inert under our frozen random-projection message
   encoder"** drops "at this scale" (checklist :31).
7. **Missing, owner's call here, required in §9: "raised before unblinding
   from the registered 40".** True, but it merges the registered ladder
   (40 → 46, DES-2) with the recorded deviation past the ladder's cap
   (60 → 72, DES-3).
8. **Not abstract-required, owed in §9:** B̂ and Γ₄ are cross-card
   contrasts (UNBLIND RESULT); the same-card replicate Γ₄′ (+0.13, RES-8)
   backs them (`branch_B.md` §5 item 8).
9. **Obligations created by the last sentence:** O-3 (supplement size,
   `git archive`), O-4 (TMLR's limit, and whether the Beyond PDF route
   takes a supplement: not verified), and an anonymization pass over the
   analysis-plan documents (they carry commit hashes).
10. **Numbers: all match.** CA-4 (4.8-fold, OK≈ 4.83); DES-13 and DES-3
    (72); DES-1 (40); RES-2 (0.96, [0.47, 1.44], Šidák 95 %); RES-1 (−1.73,
    [−4.12, +0.66]); DES-8 (a third); DES-13 (20 seeds); RES-7 (0.98);
    RES-6 (−0.03, [−0.68, +0.63]); DES-14 (twice as often, always in
    combination); RES-11 (final half); RES-12 (last fifth, DERIVED); RES-13
    (70 %, DERIVED and added to the row this session).
11. **Mechanics.** No `$`, `{{`, `{%` or `"`. "CHE" is never expanded, and
    the acronym is in the repository's README (REPO VISIBILITY: your call).
    No TMLR or OpenReview abstract limit has been checked. Placement
    (`description` and/or a body section) is still open.
12. **Passes.** The inert-share qualifier is at abstract level and its
    registration status is right; the suffix is on both co-primaries
    (attachment aside, finding 2); the completion lean and its CI are
    stated; matched compute, no convergence claim; "stressor" and "ambient
    hazard" follow the 2026-10-10 ruling; DES-14 is used correctly; no PBT,
    "swarm", mediation or dose-design attribution.

## 2026-10-10 · Abstract · draft 2

Owner's draft, verbatim:

```text
We introduce CHE, a pure-JAX multi-agent reinforcement-learning environment in which structural collapse seeds a cellular-automaton fire and the fire’s smoke attenuates the agents’ perception, alongside an independent communication-denial axis. The fire is an ambient hazard: a fixed stochastic process with nothing in it optimizing against the agents, carried by no cost or constraint channel, and invisible to the reward, which reads only task variables and agent deaths and prices every death the same whatever its cause. Severity levels are placed relative to a measured percolation threshold, and each stressor is a parameter of one transition kernel, so ablations are bitwise-exact nested models. As predicted before measurement, supercritical fire consumes the fuel that collapse would ignite: under trained policies, collapse-seeded ignitions per episode fall 4.8-fold from low to high severity. We then pre-register a test of whether training on co-occurring stressors beats training on each in isolation, at a held-out severity and matched compute, with 72 seeds per arm (above the registered seed ladder’s cap of 60, a recorded deviation made before unblinding). Joint training raises survival by 0.96 points (Šidák-corrected 95 % CI [0.47, 1.44]); task completion shows no detectable change (−1.73 points, CI [−4.12, +0.66]). Neither joint-versus-isolated difference keeps a stable sign over the final half of training: the survival gap opens only in the last fifth of the budget, and completion leans negative from 70 % of it onward. The survival gain does not survive an inert-share correction registered before unblinding. Because communication denial is inert under our frozen random-projection message encoder at this scale, a third of the isolated arm’s training episodes contain no active stressor. Removing them, in a 20-seed sensitivity arm, raises isolated training’s survival by 0.98 points; joint training then differs from it by −0.03 points (CI [−0.68, +0.63]), although it still sees each coupling twice as often and always in combination. Studies of compositional generalization should therefore match the share of training that contains an active stressor before attributing a gain to composition
```

330 words, 2,225 characters.

**Draft 1's findings:** 1 (floors) **resolved by removal**; 2 (suffix
attachment) **resolved**: the suffix now follows Γ and names its arms;
3 (Def. 2 clause 2) **resolved**; 4 ("only") **resolved**; 5 (mechanism)
**resolved**, and checked: in m35 collapse events stay flat across severity
(7.92 / 7.91 / 7.85 per episode) while seeded ignitions fall
(`che/bench/results/phase3/phase3_report.md:187-204`), so fewer collapses do
not explain the fall; 6 ("at this scale") **resolved**; 7 (k deviation)
**resolved**; 8 (cross-card, §9) unchanged, owed in §9; 9 (supplement)
**lapsed** with the sentence; the code question moves to `description` or
§11; 10 to 12 carry over.

**Builder's check findings (the builder's, not the owner's text; open):**

1. **Typo: the last sentence has no full stop.**
2. **Ambiguity, minor: "structural collapse seeds a cellular-automaton
   fire".** It can read as collapse being the fire's source. The fire starts
   from one random ignition at reset (`che/env/env.py:202`) and burns in
   every episode (D1); collapse adds ignitions only where κ_A > 0.
3. **Undersell (suggestion): the floors methodology is now absent.** Draft
   1's defect was the scope ("results are graded"), not the topic; the
   record lists floors per metric, hardware and artifact as a contribution
   (§8). Your call.
4. **Owed elsewhere, not here:** Def. 2's note that the hazard is not
   agent-independent (load-triggered collapse feeds Coupling A) is "worth
   one honest sentence in the paper" (`docs/theory_foundations.md`, Def. 2
   clause 2): §3.
5. **Numbers: all match.** New: 60 (DES-1, K_LADDER_CAP); the rest as in
   draft 1, with 72 now tied to DES-3's deviation.
6. **Mechanics** as draft 1: no `$`, `{{`, `{%` or `"`; "CHE" never
   expanded (your call); no abstract limit checked; placement open.

## 2026-10-10 · Abstract · draft 3

Owner's draft, verbatim:

```text
We introduce CHE, a pure-JAX multi-agent reinforcement-learning environment in which a cellular-automaton fire burns in every episode, structural collapse can add ignitions to it, and its smoke attenuates the agents’ perception, alongside an independent communication-denial axis. The fire is an ambient hazard: a fixed stochastic process with nothing in it optimizing against the agents, carried by no cost or constraint channel, and invisible to the reward, which reads only task variables and agent deaths and prices every death the same whatever its cause. Severity levels are placed relative to a measured percolation threshold; each stressor is a parameter of one transition kernel, so ablations are bitwise-exact nested models; and reproducibility floors are measured per metric, per GPU and per artifact: between two GPUs, the task-completion floor moved 2.75-fold while the survival floor did not. We then pre-register a test of whether training on co-occurring stressors beats training on each in isolation, at a held-out severity and matched compute, with 72 seeds per arm (above the registered seed ladder’s cap of 60, a recorded deviation made before unblinding). Joint training raises survival by 0.96 points (Šidák-corrected 95 % CI [0.47, 1.44]); task completion shows no detectable change (−1.73 points, CI [−4.12, +0.66]). Neither joint-versus-isolated difference keeps a stable sign over the final half of training: the survival gap opens only in the last fifth of the budget, and completion leans negative from 70 % of it onward. The survival gain does not survive an inert-share correction registered before unblinding. Because communication denial is inert under our frozen random-projection message encoder at this scale, a third of the isolated arm’s training episodes contain no active stressor. Removing them, in a 20-seed sensitivity arm, raises isolated training’s survival by 0.98 points; joint training then differs from it by −0.03 points (CI [−0.68, +0.63]), although it still sees each coupling twice as often and always in combination. Studies of compositional generalization should therefore match the share of training that contains an active stressor before attributing a gain to composition.
```

335 words, 2,229 characters.

**Draft 2's findings:** 1 (full stop) **resolved**; 2 (collapse as the
fire's source) **resolved**: "burns in every episode" is D1's own wording;
3 (floors absent) **addressed**, see finding 1 below; 4 (agent-dependence
sentence) owed in §3, unchanged; 5 and 6 carry over.

**Builder's check findings (the builder's, not the owner's text; open):**

1. **Overreach: "between two GPUs, the task-completion floor moved
   2.75-fold while the survival floor did not".** The two floors (M5.1e on
   the RTX 5090, M5.5 on the RTX PRO 6000, both Medium) were also measured on
   different code trees, `fa32113` and `1c1ce76`, and the science code
   differs between them: `che/env/config.py`, `observation.py`, `e2c2.py`,
   `che/train/ippo.py`, `che/eval/harness.py` (checked this session with
   `git diff --stat`). Ledger METH-1: card is confounded with tree. As
   written, the sentence attributes the move to the GPU. The per-metric half
   stands: in the same pair, completion moved and survival did not.
   (`CLAUDE.md`'s rule text states it as a card effect; the ledger, built
   later from the source, wins.)
2. **Undersell (suggestion): the self-limiting finding is gone,** so the
   abstract now carries no calibration finding. Your call.
3. **Numbers: all match.** New: 2.75-fold (METH-1, 0.0399 / 0.0145 =
   2.747); survival 0.0129 → 0.0130 (METH-1).
4. **Mechanics** as before: no `$`, `{{`, `{%` or `"`; "CHE" never
   expanded (your call); no abstract limit checked; placement open.

## 2026-10-10 · Abstract · draft 4

Owner's draft, verbatim:

```text
We introduce CHE, a pure-JAX multi-agent reinforcement-learning environment in which a cellular-automaton fire burns in every episode, structural collapse can add ignitions to it, and its smoke attenuates the agents’ perception, alongside an independent communication-denial axis. The fire is an ambient hazard: a fixed stochastic process with nothing in it optimizing against the agents, carried by no cost or constraint channel, and invisible to the reward, which reads only task variables and agent deaths and prices every death the same whatever its cause. Severity levels are placed relative to a measured percolation threshold, and each stressor is a parameter of one transition kernel, so ablations are bitwise-exact nested models; we also describe a measurement protocol in which reproducibility floors are measured per metric, per GPU and per artifact. As predicted before measurement, the supercritical fire consumes the fuel that collapse would ignite: under trained policies, collapse-seeded ignitions per episode fall 4.8-fold from low to high severity. We then pre-register a test of whether training on co-occurring stressors beats training on each in isolation, at a held-out severity and matched compute, with 72 seeds per arm (above the registered seed ladder’s cap of 60, a recorded deviation made before unblinding). Joint training raises survival by 0.96 points (Šidák-corrected 95 % CI [0.47, 1.44]); task completion shows no detectable change (−1.73 points, CI [−4.12, +0.66]). Neither joint-versus-isolated difference keeps a stable sign over the final half of training: the survival gap opens only in the last fifth of the budget, and completion leans negative from 70 % of it onward. The survival gain does not survive an inert-share correction registered before unblinding. Because communication denial is inert under our frozen random-projection message encoder at this scale, a third of the isolated arm’s training episodes contain no active stressor. Removing them, in a 20-seed sensitivity arm, raises isolated training’s survival by 0.98 points; joint training then differs from it by −0.03 points (CI [−0.68, +0.63]), although it still sees each coupling twice as often and always in combination. Studies of compositional generalization should therefore match the share of training that contains an active stressor before attributing a gain to composition.
```

357 words, 2,389 characters.

**Draft 3's findings:** 1 (floor move attributed to the GPU) **resolved**:
the example is gone and the protocol is described as a protocol. 2 (no
calibration finding) **resolved**: the self-limiting sentence is back,
unchanged from draft 2, where it was checked.

**Builder's check findings (the builder's, not the owner's text):** none
new. Overreach, undersell, conflict, missing, numbers and typos: clean
against the record. Open, and the owner's to decide: "CHE" is never
expanded (REPO VISIBILITY); placement (`description` and/or a body section);
no TMLR or OpenReview abstract limit has been checked.

## 2026-10-10 · Abstract · draft 5 ("probably final")

Owner's draft, verbatim:

```text
We introduce the Compound Hostile Environment (CHE), a pure-JAX multi-agent reinforcement-learning environment in which a cellular-automaton fire burns in every episode, structural collapse can add ignitions to it, and its smoke attenuates the agents’ perception, alongside an independent communication-denial axis. The fire is an ambient hazard: a fixed stochastic process with nothing in it optimizing against the agents, carried by no cost or constraint channel, and invisible to the reward, which reads only task variables and agent deaths and prices every death the same whatever its cause. Severity levels are placed relative to a measured percolation threshold, and each stressor is a parameter of one transition kernel, so ablations are bitwise-exact nested models; we also describe a measurement protocol in which reproducibility floors are measured per metric, per GPU and per artifact. As predicted before measurement, the supercritical fire consumes the fuel that collapse would ignite: under trained policies, collapse-seeded ignitions per episode fall 4.8-fold from low to high severity. We then pre-register a test of whether training on co-occurring stressors beats training on each in isolation, at a held-out severity and matched compute, with 72 seeds per arm (above the registered seed ladder’s cap of 60, a recorded deviation made before unblinding). Joint training raises survival by 0.96 points (Šidák-corrected 95 % CI [0.47, 1.44]); task completion shows no detectable change (−1.73 points, CI [−4.12, +0.66]). Neither joint-versus-isolated difference keeps a stable sign over the final half of training: the survival gap opens only in the last fifth of the budget, and completion leans negative from 70 % of it onward. The survival gain does not survive an inert-share correction registered before unblinding. Because communication denial is inert under our frozen random-projection message encoder at this scale, a third of the isolated arm’s training episodes contain no active stressor. Removing them, in a 20-seed sensitivity arm, raises isolated training’s survival by 0.98 points; joint training then differs from it by −0.03 points (CI [−0.68, +0.63]), although it still sees each coupling twice as often and always in combination. Studies of compositional generalization should therefore match the share of training that contains an active stressor before attributing a gain to composition.
```

361 words, 2,424 characters; the owner checked the abstract limit: 5,000
characters (2026-10-10). The only change from draft 4 is the full name,
"the Compound Hostile Environment (CHE)".

**Builder's check findings (the builder's, not the owner's text):** none
new. The name is the owner's double-blind call (REPO VISIBILITY): the repo
goes private before upload, and copies made while it was public are
unchecked. "Hostile" beside Def. 2's non-adversarial clause: the second
sentence answers the adversarial reading the builder raised at the title
step. Open, the owner's: placement (`description` and/or a body section).

## 2026-10-10 · Abstract · called done

The owner's final text is draft 5, verbatim. Copied into `paper/finale.md`
as a body section directly after the front matter, with no heading (the
owner's placement, "for now"), and 17 `<!-- N:ID -->` comments; stripping
them reproduces draft 5 exactly (checked). Decision log: ABSTRACT.

## 2026-10-10 · description · draft 1

Owner's draft, verbatim:

```text
In the Compound Hostile Environment (CHE), structural collapse can add ignitions to a cellular-automaton fire, the fire’s smoke attenuates what agents perceive, and inter-agent communication can be denied; the fire itself enters no reward, cost or constraint channel.
```

38 words, 267 characters. Parses as a plain YAML scalar unchanged (checked);
no `"`, line break, backslash, `$`, `{{`, `{%`, `: ` or ` #`.

**Builder's check findings (the builder's, not the owner's text; open):**

1. **No defect against the record.** Coupling A ("can add ignitions"),
   Coupling B and the δ axis are stated as built; "the fire itself enters no
   reward, cost or constraint channel" is Def. 2 clause 1 (no term of R
   references h, ρ or c; no cost or constraint channel).
2. **Note, not a defect: "itself" carries the death penalty.** The reward
   prices deaths (d_p = 0.5, ENV-1), fire deaths included; the sentence is
   true because it says the fire *itself*. A reader of the meta description
   sees no abstract; the title's "hazard-blind" and the abstract carry the
   pricing.
3. **Suggestion (builder's observation, not a record rule): "Hostile" stands
   alone here.** In the abstract the second sentence answers the adversarial
   reading; this line, read standalone as the meta description, has no
   non-adversarial clause (Def. 2 clause 2).
4. **Observation: it restates the abstract's opening** (sentence 1 and the
   channel half of sentence 2), directly above it. The owner's choice;
   the 2026-09-28 note said to look again in a preview.
5. **Resolves a title-step suggestion:** the couplings the title lacks are
   here. Result, test and code are absent by choice; the code question moves
   to §11. Numbers: none. Typos and grammar: none.

## 2026-10-10 · description · draft 2

Owner's draft, verbatim:

```text
In the Compound Hostile Environment (CHE), structural collapse can add ignitions to a cellular-automaton fire, the fire’s smoke attenuates what agents perceive, and inter-agent communication can be denied; the fire itself optimizes against no one and enters no reward, cost or constraint channel.
```

43 words, 296 characters. Parses as a plain YAML scalar unchanged (checked);
no `"`, line break, backslash, `$`, `{{`, `{%`, `: ` or ` #`.

**Draft 1's findings:** 3 ("Hostile" standalone) **resolved**: "optimizes
against no one" is Def. 2 clause 2 (a fixed kernel, nothing optimizing),
scoped to the fire, and true of it. 2 ("itself" carries the death penalty)
and 4 (restates the abstract's opening) stand as notes, not defects.

**Builder's check findings (the builder's):** none new.

## 2026-10-10 · description · called done

The owner's final text is draft 2, verbatim, now `paper/finale.md`'s
`description` (a plain YAML scalar; parsed back equal, checked). Decision
log: DESCRIPTION.

## 2026-10-10 · §1 Introduction · draft 1

Owner's draft, verbatim:

````markdown
## 1 Introduction

Teams of agents that operate in hazardous settings rarely face one danger at a
time, and the dangers interact. A structural collapse can start a fire, the
fire's smoke degrades what agents can perceive, and communication can fail for
reasons of its own. Anyone who chooses a training distribution for such a team
faces a practical question: must the policy see these stressors together during
training to cope with them together at test time, or is it enough to see each
one alone? This is a question of compositional generalization over environmental
factors. It has been studied for imitation-learned manipulation (Gao et al.,
2024) <!-- cite:gao2024composition | OWNER READS before submission --> and is the
combinatorial-interpolation case of Kirk et al.'s (2023) taxonomy of zero-shot
generalization <!-- cite:kirk2023zsg -->. We study it for survival in
multi-agent reinforcement learning, where the stressors are coupled and lethal.

In the work closest to ours, a hazard enters the learning problem in one of two
places. In monitoring and suppression tasks it is the objective, and the reward
scores the fire's coverage or its suppression (e.g., Haksar & Schwager, 2018)
<!-- cite:haksar2018 -->. In safe and constrained reinforcement learning it is a
cost or a constraint. <!-- no verified bib entry for CMDP / safe RL yet; add one
via related_work_verification.md --> We study a third placement. In the Compound
Hostile Environment (CHE), the fire is an *ambient hazard* (Definition 2): a
fixed stochastic process with nothing in it optimizing against the agents,
carried by no cost or constraint channel, and invisible to the reward. The
reward reads task variables and agent deaths, and it prices every death the
same, d_p = 0.5 <!-- N:ENV-1 -->, whatever its cause. Survival is therefore
learned through two hazard-blind routes: a dead agent collects no further task
reward, and each death costs a fixed amount. From one agent's point of view the
fire looks like nonstationarity. Proposition 1 shows that it is state: the full
process is a Markov chain and the environment is a finite Dec-POMDP, so the
standard value definitions apply. With communication denied, the problem does
not reduce to a multi-agent POMDP, and finite-horizon Dec-POMDPs are
NEXP-complete (Bernstein et al., 2002) <!-- cite:bernstein2002 -->, which is
why we learn policies rather than plan.

CHE is built to answer the training question as a measurement. A
cellular-automaton fire burns in every episode. For the idealized kernel, the
burnt region is exactly a bond-percolation cluster (Proposition 2; Grassberger,
1983; Kesten, 1980) <!-- cite:grassberger1983 --> <!-- cite:kesten1980 -->, so
severity has a natural definition: three levels placed below, near and above a
*measured* percolation threshold of the implemented kernel, rather than at
arbitrary parameter values. Three stressors attach to the fire. Structural
collapse can add ignitions (Coupling A), smoke attenuates each agent's
egocentric observation by Beer–Lambert transmittance (Coupling B), and
inter-agent links can be denied (δ). Each stressor is a parameter of one
transition or observation kernel, and every stochastic branch consumes its
random numbers whether or not its stressor is on. Switching a stressor off
therefore reproduces the nested model's trajectories bit for bit: ablations
are exact by construction. Calibrating the environment produced findings that
stand without any training comparison (§§4–7).

The training question is then posed as a pre-registered test. An isolated arm
(ISO) trains one policy on a mixture of single-stressor configurations, and a
joint arm (JOINT) trains one on configurations with every stressor on. Both
train at a low and a high severity (β = 0.43 and 0.70) <!-- N:CAL-3 --> and are
evaluated at the near-critical severity, β = 0.49 <!-- N:CAL-3 -->, which
neither saw. Architecture and compute are matched: single-policy IPPO (de Witt
et al., 2020) <!-- cite:dewitt2020ippo -->, one policy per training seed. The
co-primary outcomes are task completion and survival, Šidák-corrected for two
tests. The four possible outcomes, a framing for each, and a falsifier for the
asymmetric outcome were registered on 2026-08-13 <!-- N:DES-12 -->, before the
grid began on 2026-09-09 <!-- N:DES-12 -->; survival had been made a
co-primary on 2026-08-02 <!-- N:DES-12 -->. We ran 72 seeds per arm
<!-- N:DES-3 -->, above the registered seed ladder's cap of 60
<!-- N:DES-1 -->, a recorded deviation made before unblinding (§9.1). The
comparison has a known weakness, which we state before the result: JOINT sees
each coupling three times as often as ISO <!-- N:DES-7 -->, so the endpoints
differ in dose as well as in co-occurrence. A secondary design holds each
stressor's frequency fixed while co-occurrence varies, a split in the spirit of
DBCA (Keysers et al., 2020) <!-- cite:keysers2020 -->, but it is not
verdict-bearing and resolves neither its trend nor its knees (§9.2). The
founding hypothesis, that joint training improves both outcomes, did not occur.

At the held-out severity, joint training raises survival by 0.96 points
(Šidák-corrected 95 % CI [0.47, 1.44]) <!-- N:RES-2 -->. Task completion shows
no detectable change: −1.73 points, CI [−4.12, +0.66] <!-- N:RES-1 -->, which
excludes a joint-training gain larger than 0.66 points <!-- N:RES-1 -->. The
registered falsifier for an asymmetric result passes <!-- N:RES-5 -->, so the
asymmetry stands. Under Definition 2 it is an asymmetry between a penalized
channel, deaths, and a rewarded one, the task. Neither joint-versus-isolated
difference keeps a stable sign over the final half of training
<!-- N:RES-11 -->: the survival gap opens only in the last fifth of the budget
<!-- N:RES-12 -->, and the completion difference leans negative from 70 % of it
onward <!-- N:RES-13 -->.

The survival gain does not survive the inert-share correction. Communication
denial is inert under our frozen random-projection message encoder at this
scale (§7), so the third of ISO's training episodes that carry only δ
<!-- N:DES-8 --> carry no active stressor. We registered this bias, and an arm
to remove it, on 2026-09-18 <!-- log: §7 PROPOSALS RULING; DES-15 in the
owner's local ledger -->, before unblinding. That arm, ISO-4, is ISO without
its δ-only episodes, trained with 20 seeds <!-- N:DES-13 -->. Its survival is
0.98 points above ISO's <!-- N:RES-7 -->, and JOINT's survival differs from
ISO-4's by −0.03 points (CI [−0.68, +0.63]) <!-- N:RES-6 -->. As the
registration requires, we do not describe the survival advantage as a
composition effect. Two limits apply. First, the corrected contrast's upper
bound, +0.63 <!-- N:RES-6 -->, lies above the uncorrected contrast's lower
bound, +0.47 <!-- N:RES-2 -->, so the correction excludes a large composition
effect, not every composition effect. Second, removing the δ-only episodes
changes two things at once: the share of training with an active stressor
rises from two thirds to all of it <!-- N:DES-8 -->, and each coupling's
frequency rises from a third to a half of episodes <!-- N:DES-7; p6_iso4.yaml:7
-->. The 0.98-point rise therefore cannot say which of the two matters. What
the corrected contrast does say is that, once the active share is matched,
JOINT's remaining differences add nothing detectable to survival: it sees each
coupling twice as often as ISO-4 <!-- N:DES-14, owner's local ledger;
p6_iso4.yaml:7 --> and always in combination.

The methods lesson reaches beyond this environment. A comparison of joint and
isolated training that leaves the active share free can report an exposure
effect as a composition effect. Our separation from earlier joint-versus-isolated
comparisons is what the comparison holds fixed. In the literature search
described in §2, which was abstract-level, we found no reinforcement-learning
comparison that matches its arms on how much of training carries any stressor.

We do not claim convergence guarantees for the training procedure, or a theorem
that joint training wins: Proposition 4 bounds what isolated training can be
*guaranteed* to transfer, not what it does, and Theorem 1 concerns adaptivity
against memorization in a two-corridor toy. We do not claim an exact critical
value for the implemented kernel, whose threshold is measured. Nor do we claim
that the survival gap is robust to the training budget, since its sign is not
stable over the final half of training.

Our contributions are:

1. **An environment built as an instrument.** CHE places a lethal fire in the
   transition and observation kernels only (Definition 2), factorizes each
   step into collapse, fire, smoke, agents and communication (Proposition 1),
   defines severity by measured dynamical phase, and makes every ablation a
   bitwise-exact nested model. Its theory doubles as unit tests: the
   implementation reproduces Proposition 3's linear scaling, Theorem 1's value
   curve and Remark 2′'s value of communication (§§3–7).
2. **Calibration findings that stand without the training comparison.** As
   predicted before measurement, the supercritical fire consumes the fuel that
   collapse would ignite: under trained policies, collapse-seeded ignitions
   fall 4.8-fold from low to high severity <!-- N:CA-4 -->, while the share of
   them near agents stays flat <!-- N:CA-6 --> (§5). Smoke attenuation costs
   survival at high severity, replicated in direction three times out of three
   <!-- N:CB-5 -->, and the masking concentrates 16–118-fold on moments of
   danger <!-- N:CB-10 --> (§6). Communication is inert under our frozen
   random-projection encoder at this scale (§7).
3. **A measurement protocol in which acceptance bars come with floors.**
   Reproducibility floors are measured per metric, per GPU and per artifact;
   contrasts are graded on their own standard error; and design-stage power is
   stated as the minimum effect detectable with 80 % power at the
   family-corrected α (§8).
4. **A pre-registered test of joint against isolated training.** Its survival
   advantage does not survive a correction registered before unblinding, and it
   teaches a transferable lesson: match the active share before attributing a
   gain to composition (§9).
````

About 1,470 words, comments excluded. No `$`, `{{` or `{%`.

**Builder's check findings (the builder's, not the owner's text; open):**

*Conflict*
1. **"Three stressors attach to the fire."** δ does not: it is independent
   of the fire (D1; theory §6, "comms is mechanistically independent";
   your own abstract and `description` say "independent").
2. **"where the stressors are coupled and lethal."** Under the 2026-10-10
   ruling the stressors are A, B and δ. A and B are coupled; δ is
   independent and inert; B is not itself lethal. What kills is the fire and
   collapse (`deaths_fire`, `deaths_collapse`), and the fire is not a
   stressor.
3. **"an exposure effect" (methods-lesson paragraph).** P6 of the draft
   itself shows "exposure" is two things: the active share, which ISO-4
   matches, and per-coupling frequency, which it does not (DES-14). The word
   leaves the reader to guess which.

*Overreach*
4. **"We study a third placement."** Builder's observation, not in the
   record or the search: a hazard that acts only through the dynamics (death
   ends the return; the reward never sees the hazard) is common in RL
   environments outside the two lineages named, e.g. lava cells in
   gridworlds. Read alone, the sentence makes the placement sound new. The
   record's separation is what the comparison holds fixed (ENDPOINT
   CONFOUND; the search).
5. **"Teams of agents … rarely face one danger at a time, and the dangers
   interact."** A claim about the world with no source. The record's support
   for interacting co-occurring stressors is the ecology/climate analogy
   (`crain2008stressors`, `cote2016stressors`, `zscheischler2018compound`,
   `zscheischler2020typology`), not agent teams.
6. **Haksar & Schwager's reward** ("scores the fire's coverage or its
   suppression"): the record verifies the entry, not the reward;
   `related_work_verification.md` §10 says to quote the reward from the PDF.
7. **Kirk et al.'s "combinatorial-interpolation case":** this comes from the
   unratified Part-2 draft (builder text). The record verifies Kirk only
   bibliographically; no full-text read confirms the term.
8. **Suggestion, low: "reaches beyond this environment", "transferable
   lesson".** The evidence is one environment; the generality rests on the
   confounding argument, not a second measurement.

*Missing (placement yours; §9 must carry each)*
9. **The sweep's two facts not stated.** (a) It cannot hold the empty share
   fixed: the no-element share rises with co-occurrence, 0 → 0.5
   (`p6_sweep_c50_p*.yaml:7`; ENDPOINT CONFOUND, "state this rather than let
   a reviewer find it"; `branch_B.md` §5 item 7). (b) The secondary family
   did resolve two slopes: γ_n < 0 and γ_p > 0 (SEC-1). "Resolves neither its
   trend nor its knees" is accurate, but read alone it says the design found
   nothing; γ_p is the one composition-direction result, positive, local,
   and it does not extrapolate (SEC-4; `branch_B.md` §1, §8).
10. **ISO-4's status:** the date is given, not that it is a sensitivity arm
    outside the confirmatory family (DES-15). The abstract says "sensitivity
    arm".
11. **Suggestion: Coupling B at the test severity.** §1 states Coupling B's
    High effect next to a Medium test; at Medium its own effect was −0.0003
    (CB-9, 3 seeds, not floor-graded). The registered §4a limitation is
    required in the paper (§10).
12. **Owed before the text stands:** the Gao read (your comment); a verified
    CMDP / safe-RL entry (your comment); the IEEE Xplore query behind the
    search claim (checklist :66).
13. **Undersell, optional:** γ_n bears on "cannot say which of the two
    matters": it predicts +0.79 from the empty share alone against +0.98
    observed (SEC-3, RES-7; non-verdict-bearing). The sentence is right about
    B̂ alone.

*Numbers*
14. **All values match.** IDs missing or incomplete: "95 %" and "two tests"
    (DES-13); "three levels" (CAL-3); "four possible outcomes" (DES-12, four
    branches added to its note today); "80 %" (METH-7, new today); "all of
    it" and "a half" (DES-14). DES-14 and DES-15 are in the repository ledger,
    uncommitted, not a local copy.

*Mechanics*
15. `<!-- cite:key -->` placeholders must become `<d-cite key="…"></d-cite>`;
    Distill prints its own marker, so the parenthetical author-year text
    would sit beside it (your call). Process comments ("OWNER READS…", "no
    verified bib entry…", "owner's local ledger", "log: …") ship in the page
    source unless stripped (comment stripping, OWED). "d_p" renders as
    literal text; math is `$$…$$` in the kit.

*Passes*
16. Qualifier adjacent and scoped; suffix on both co-primaries; completion
    bound; the asymmetry as a penalized against a rewarded channel; falsifier;
    branch A stated flatly; the co-primary dated before the grid (a
    registered obligation); the k deviation; the endpoint confound; IPPO, no
    PBT; Prop. 1, Prop. 2 and Thm. 1 within their statements; Prop. 4's
    required honesty note; theory §9's non-claims; no Kesten claim for the
    implemented kernel; comms scoped; Coupling B led by its replication; the
    search's level stated.

## 2026-10-10 · §1 Introduction · draft 2

Owner's draft, verbatim:

````markdown
## 1 Introduction

When a training distribution has to cover several stressors, its designer
chooses whether the policy meets them together or one at a time, and the choice
matters most when the stressors interact. Ecology and climate science study the
interactive and cumulative effects of multiple stressors (Crain et al., 2008)
<!-- cite:crain2008stressors --> and the risk from compound events (Zscheischler
et al., 2018) <!-- cite:zscheischler2018compound --> as objects in their own
right. In reinforcement learning the same choice is a question of
generalization: must a policy see stressors co-occur during training to cope
with their co-occurrence at test time? It has been studied for imitation-learned
manipulation (Gao et al., 2024) <!-- cite:gao2024composition | OWNER READS
before submission -->, and it belongs to the wider problem of zero-shot
generalization (Kirk et al., 2023) <!-- cite:kirk2023zsg -->. We study it for
survival in multi-agent reinforcement learning, in an environment where agents
are killed by fire and by structural collapse, two of the stressors are coupled
to the fire, and a third acts independently.

Where the hazard sits in the learning problem shapes what such a comparison can
teach. In some fire-related work the hazard is the task itself, as for a team of
aerial robots fighting forest fires (Haksar & Schwager, 2018)
<!-- cite:haksar2018 -->. In safe and constrained reinforcement learning it
enters a cost or a constraint. <!-- no verified bib entry for CMDP / safe RL
yet; add one via related_work_verification.md --> In the Compound Hostile
Environment (CHE) it does neither. The fire is an *ambient hazard*
(Definition 2): a fixed stochastic process with nothing in it optimizing against
the agents, carried by no cost or constraint channel, and invisible to the
reward. The reward reads task variables and agent deaths, and prices every death
at the same fixed penalty, 0.5 <!-- N:ENV-1 -->, whatever its cause. Agents
therefore learn to survive only from outcomes: a dead agent collects no further
task reward, and each death costs the penalty. A hazard that acts only through
the dynamics is not new in itself. What it gives this study is a comparison in
which neither arm is ever told about the hazard, so the arms differ only in what
their training distributions show the agents. From one agent's point of view the
fire looks like nonstationarity. Proposition 1 shows that it is state: the full
process is a Markov chain and the environment is a finite Dec-POMDP, so the
standard value definitions apply. With communication denied, the problem does
not reduce to a multi-agent POMDP, and finite-horizon Dec-POMDPs are
NEXP-complete (Bernstein et al., 2002) <!-- cite:bernstein2002 -->, which is
why we learn policies rather than plan.

CHE is built to answer the training question as a measurement. A
cellular-automaton fire burns in every episode. For the idealized kernel, the
burnt region is exactly a bond-percolation cluster (Proposition 2; Grassberger,
1983; Kesten, 1980) <!-- cite:grassberger1983 --> <!-- cite:kesten1980 -->, so
severity has a natural definition: three levels <!-- N:CAL-3 --> placed below,
near and above a *measured* percolation threshold of the implemented kernel,
rather than at arbitrary parameter values. Two stressors are coupled to the
fire. Structural collapse can add ignitions (Coupling A), and smoke attenuates
each agent's egocentric observation by Beer–Lambert transmittance (Coupling B).
A third, the denial of inter-agent links (δ), is independent of it. Each
stressor is a parameter of one transition or observation kernel, and every
stochastic branch consumes its random numbers whether or not its stressor is
on. Switching a stressor off therefore reproduces the nested model's
trajectories bit for bit: ablations are exact by construction. Calibrating the
environment produced findings that stand without any training comparison
(§§4–7).

The training question is then posed as a pre-registered test. An isolated arm
(ISO) trains one policy on a mixture of single-stressor configurations, and a
joint arm (JOINT) trains one on configurations with every stressor on. Both
train at a low and a high severity (β = 0.43 and 0.70) <!-- N:CAL-3 --> and are
evaluated at the near-critical severity, β = 0.49 <!-- N:CAL-3 -->, which
neither saw. Architecture and compute are matched: single-policy IPPO (de Witt
et al., 2020) <!-- cite:dewitt2020ippo -->, one policy per training seed. The
co-primary outcomes are task completion and survival, Šidák-corrected for two
tests <!-- N:DES-13 -->. The four possible outcomes <!-- N:DES-12 -->, a
framing for each, and a falsifier for the asymmetric outcome were registered on
2026-08-13 <!-- N:DES-12 -->, before the grid began on 2026-09-09
<!-- N:DES-12 -->; survival had been made a co-primary on 2026-08-02
<!-- N:DES-12 -->. We ran 72 seeds per arm <!-- N:DES-3 -->, above the
registered seed ladder's cap of 60 <!-- N:DES-1 -->, a recorded deviation made
before unblinding (§9.1). The comparison has a known weakness, which we state
before the result: JOINT sees each coupling three times as often as ISO
<!-- N:DES-7 -->, so the endpoints differ in dose as well as in co-occurrence. A
secondary design holds each coupling's frequency fixed while co-occurrence
varies, a split in the spirit of DBCA (Keysers et al., 2020)
<!-- cite:keysers2020 -->. It cannot also hold the share of fire-only episodes
fixed, which rises with co-occurrence <!-- N:DES-9 -->, and it is not
verdict-bearing (§9). The founding hypothesis, that joint training improves both
outcomes, did not occur.

At the held-out severity, joint training raises survival by 0.96 points
(Šidák-corrected 95 % CI [0.47, 1.44]) <!-- N:RES-2 --> <!-- N:DES-13 -->.
Task completion shows no detectable change: −1.73 points, CI [−4.12, +0.66]
<!-- N:RES-1 -->, which excludes a joint-training gain larger than 0.66 points
<!-- N:RES-1 -->. The registered falsifier for an asymmetric result passes
<!-- N:RES-5 -->, so the asymmetry stands. Under Definition 2 it is an asymmetry
between a penalized channel, deaths, and a rewarded one, the task. Neither
joint-versus-isolated difference keeps a stable sign over the final half of
training <!-- N:RES-11 -->: the survival gap opens only in the last fifth of the
budget <!-- N:RES-12 -->, and the completion difference leans negative from 70 %
of it onward <!-- N:RES-13 -->.

The survival gain does not survive the inert-share correction. Communication
denial is inert under our frozen random-projection message encoder at this
scale (§7), so the third of ISO's training episodes that carry only δ
<!-- N:DES-8 --> carry no active stressor. We registered this bias, and an arm
to remove it, on 2026-09-18 <!-- N:DES-15 -->, before unblinding. That arm,
ISO-4, is ISO without its δ-only episodes: a sensitivity arm outside the
confirmatory family, trained with 20 seeds <!-- N:DES-13 --> <!-- N:DES-15 -->.
Its survival is 0.98 points above ISO's <!-- N:RES-7 -->, and JOINT's survival
differs from ISO-4's by −0.03 points (CI [−0.68, +0.63]) <!-- N:RES-6 -->. As
the registration requires, we do not describe the survival advantage as a
composition effect. Two limits apply. First, the corrected contrast's upper
bound, +0.63 <!-- N:RES-6 -->, lies above the uncorrected contrast's lower
bound, +0.47 <!-- N:RES-2 -->, so the correction excludes a large composition
effect, not every composition effect. Second, removing the δ-only episodes
changes two things at once: the share of training with an active stressor rises
from two thirds to all of it <!-- N:DES-8 --> <!-- N:DES-14 -->, and each
coupling's frequency rises from a third to a half of episodes <!-- N:DES-7 -->
<!-- N:DES-14 -->. The 0.98-point rise cannot say by itself which of the two
matters. The secondary design's estimated cost of fire-only training predicts
+0.79 points of it <!-- N:SEC-3 -->, which points to the active share, but that
design is not verdict-bearing. What the corrected contrast does say is that,
once the active share is matched, JOINT's remaining differences add nothing
detectable to survival: it sees each coupling twice as often as ISO-4
<!-- N:DES-14 --> and always in combination.

The argument behind this result is general, although we measured it in one
environment: a comparison of joint and isolated training that leaves the active
share free can report an active-share effect as a composition effect. What
separates this work from earlier joint-versus-isolated comparisons is what the
comparison holds fixed. In the literature search described in §2, which read
abstracts and did not query IEEE Xplore, we found no reinforcement-learning
comparison that matches its arms on how much of training carries any stressor.

We do not claim convergence guarantees for the training procedure, or a theorem
that joint training wins: Proposition 4 bounds what isolated training can be
*guaranteed* to transfer, not what it does, and Theorem 1 concerns adaptivity
against memorization in a two-corridor toy. We do not claim an exact critical
value for the implemented kernel, whose threshold is measured. Nor do we claim
that the survival gap is robust to the training budget, since its sign is not
stable over the final half of training.

Our contributions are:

1. **An environment built as an instrument.** CHE places a lethal fire in the
   transition and observation kernels only (Definition 2), factorizes each step
   into collapse, fire, smoke, agents and communication (Proposition 1), defines
   severity by measured dynamical phase, and makes every ablation a
   bitwise-exact nested model. Its theory doubles as unit tests: the
   implementation reproduces Proposition 3's linear scaling, Theorem 1's value
   curve and Remark 2′'s value of communication (§§3–7).
2. **Calibration findings that stand without the training comparison.** As
   predicted before measurement, the supercritical fire consumes the fuel that
   collapse would ignite: under trained policies, collapse-seeded ignitions
   fall 4.8-fold from low to high severity <!-- N:CA-4 -->, while the share of
   them near agents stays flat <!-- N:CA-6 --> (§5). Smoke attenuation costs
   survival at high severity, replicated in direction three times out of three
   <!-- N:CB-5 -->, and the masking concentrates 16–118-fold on moments of
   danger <!-- N:CB-10 --> (§6). At the medium severity used for the test, its
   own measured effect on survival was −0.03 points, graded only against a
   three-seed spread <!-- N:CB-9 --> (§10). Communication is inert under our
   frozen random-projection encoder at this scale (§7).
3. **A measurement protocol in which acceptance bars come with floors.**
   Reproducibility floors are measured per metric, per GPU and per artifact;
   contrasts are graded on their own standard error; and design-stage power is
   stated as the minimum effect detectable with 80 % power
   <!-- N:METH-7 --> at the family-corrected α (§8).
4. **A pre-registered test of joint against isolated training.** Its survival
   advantage does not survive a correction registered before unblinding, and it
   points to a rule whose argument is general: match the active share before
   attributing a gain to composition (§9).
````

About 1,620 words, comments excluded. No `$`, `{{` or `{%`.

**Draft 1's findings:** 1, 2 (δ independent; stressors coupled and lethal)
**resolved**. 3 ("exposure") **resolved**: "active-share effect". 4 ("third
placement") **resolved**: "not new in itself". 5 (world claim) **resolved**:
the ecology/climate analogy, in one sentence, from verified entries. 6
(Haksar's reward) **resolved**: now only what the abstract supports, the task
is fighting forest fires. 7 (Kirk's term) **resolved**: bibliographic-level
claim. 8 (generality) **resolved**: "general, although we measured it in one
environment". 9(a) (sweep's empty share) **resolved** (DES-9). 9(b) see
finding 1 below. 10 (ISO-4 status) **resolved**. 11 (Coupling B at Medium)
**resolved** in contribution 2 (CB-9, scoped). 12 still owed (Gao read;
CMDP/safe-RL entry; IEEE Xplore, now disclosed in the text). 13 taken up, see
finding 1. 14 **resolved**: every number carries an ID. 15 (mechanics)
partly: "d_p" gone; placeholders and process comments remain.

**Builder's check findings (the builder's, not the owner's text; open):**

1. **Selective use of the secondary plane fit.** The draft cites γ_n's
   prediction (+0.79 of the 0.98, SEC-3) as pointing to the active share.
   The same fit's γ_p predicts JOINT − ISO-4 ≈ +3.3 points (SEC-4) where Γ₄
   measures −0.03 (RES-6): the plane mispredicts there by about 3 points.
   Citing the half that fits without the half that does not is selective;
   `branch_B.md` §1 states γ_p as a tension that does not extrapolate (§8:
   "γ_p is a local positive slope").
2. **Ambiguity: "neither arm is ever told about the hazard".** Agents see
   the fire: burning, burnt and smoke are observation planes
   (`che/env/observation.py:24-26`; ENV-7), attenuated by Coupling B. The
   sentence can read as the agents being unaware of the hazard; what is true
   is that no reward, cost or constraint signal carries it.
3. **Owed, unchanged:** the Gao read; a verified CMDP / safe-RL entry.
4. **Mechanics, unchanged:** `<!-- cite:key -->` placeholders become
   `<d-cite key="…"></d-cite>`; process comments ("OWNER READS…", "no
   verified bib entry…") are stripped before upload.
5. **Numbers: all match, every number has an ID.** New: +0.79 (SEC-3,
   DERIVED −0.0237 × (0 − 1/3)); −0.03 at Medium (CB-9, −0.0003); 0.5
   (ENV-1); "rises with co-occurrence" (DES-9).
6. **Passes.** Everything that passed in draft 1, plus the fixes above. The
   Zscheischler title ("Future climate risk from compound events") supports
   "the risk from compound events"; Haksar's verified abstract supports "a
   team of aerial robots fighting forest fires".

## 2026-10-10 · §1 Introduction · draft 3

Owner's draft, verbatim:

````markdown
## 1 Introduction

When a training distribution has to cover several stressors, its designer
chooses whether the policy meets them together or one at a time, and the choice
matters most when the stressors interact. Ecology and climate science study the
interactive and cumulative effects of multiple stressors (Crain et al., 2008)
<!-- cite:crain2008stressors --> and the risk from compound events (Zscheischler
et al., 2018) <!-- cite:zscheischler2018compound --> as objects in their own
right. In reinforcement learning the same choice is a question of
generalization: must a policy see stressors co-occur during training to cope
with their co-occurrence at test time? It has been studied for imitation-learned
manipulation (Gao et al., 2024) <!-- cite:gao2024composition -->, and it belongs
to the wider problem of zero-shot generalization (Kirk et al., 2023)
<!-- cite:kirk2023zsg -->. We study it for survival in multi-agent
reinforcement learning, in an environment where agents are killed by fire and by
structural collapse, two of the stressors are coupled to the fire, and a third
acts independently.

Where the hazard sits in the learning problem shapes what such a comparison can
teach. In some fire-related work the hazard is the task itself, as for a team of
aerial robots fighting forest fires (Haksar & Schwager, 2018)
<!-- cite:haksar2018 -->. In safe and constrained reinforcement learning it
enters a cost or a constraint. <!-- no verified bib entry for CMDP / safe RL
yet; add one via related_work_verification.md --> In the Compound Hostile
Environment (CHE) it does neither. The fire is an *ambient hazard*
(Definition 2): a fixed stochastic process with nothing in it optimizing against
the agents, carried by no cost or constraint channel, and invisible to the
reward. The reward reads task variables and agent deaths, and prices every death
at the same fixed penalty, 0.5 <!-- N:ENV-1 -->, whatever its cause. Agents
therefore learn to survive only from outcomes: a dead agent collects no further
task reward, and each death costs the penalty. A hazard that acts only through
the dynamics is not new in itself. What it gives this study is a comparison in
which no reward or cost signal mentions the hazard in either arm. Agents meet
the fire only through what they observe and what happens to them, so the arms
differ only in what their training distributions show the agents. From one
agent's point of view the fire looks like nonstationarity. Proposition 1 shows
that it is state: the full process is a Markov chain and the environment is a
finite Dec-POMDP, so the standard value definitions apply. With communication
denied, the problem does not reduce to a multi-agent POMDP, and finite-horizon
Dec-POMDPs are NEXP-complete (Bernstein et al., 2002)
<!-- cite:bernstein2002 -->, which is why we learn policies rather than plan.

CHE is built to answer the training question as a measurement. A
cellular-automaton fire burns in every episode. For the idealized kernel, the
burnt region is exactly a bond-percolation cluster (Proposition 2; Grassberger,
1983; Kesten, 1980) <!-- cite:grassberger1983 --> <!-- cite:kesten1980 -->, so
severity has a natural definition: three levels <!-- N:CAL-3 --> placed below,
near and above a *measured* percolation threshold of the implemented kernel,
rather than at arbitrary parameter values. Two stressors are coupled to the
fire. Structural collapse can add ignitions (Coupling A), and smoke attenuates
each agent's egocentric observation by Beer–Lambert transmittance (Coupling B).
A third, the denial of inter-agent links (δ), is independent of it. Each
stressor is a parameter of one transition or observation kernel, and every
stochastic branch consumes its random numbers whether or not its stressor is
on. Switching a stressor off therefore reproduces the nested model's
trajectories bit for bit: ablations are exact by construction. Calibrating the
environment produced findings that stand without any training comparison
(§§4–7).

The training question is then posed as a pre-registered test. An isolated arm
(ISO) trains one policy on a mixture of single-stressor configurations, and a
joint arm (JOINT) trains one on configurations with every stressor on. Both
train at a low and a high severity (β = 0.43 and 0.70) <!-- N:CAL-3 --> and are
evaluated at the near-critical severity, β = 0.49 <!-- N:CAL-3 -->, which
neither saw. Architecture and compute are matched: single-policy IPPO (de Witt
et al., 2020) <!-- cite:dewitt2020ippo -->, one policy per training seed. The
co-primary outcomes are task completion and survival, Šidák-corrected for two
tests <!-- N:DES-13 -->. The four possible outcomes <!-- N:DES-12 -->, a
framing for each, and a falsifier for the asymmetric outcome were registered on
2026-08-13 <!-- N:DES-12 -->, before the grid began on 2026-09-09
<!-- N:DES-12 -->; survival had been made a co-primary on 2026-08-02
<!-- N:DES-12 -->. We ran 72 seeds per arm <!-- N:DES-3 -->, above the
registered seed ladder's cap of 60 <!-- N:DES-1 -->, a recorded deviation made
before unblinding (§9.1). The comparison has a known weakness, which we state
before the result: JOINT sees each coupling three times as often as ISO
<!-- N:DES-7 -->, so the endpoints differ in dose as well as in co-occurrence. A
secondary design holds each coupling's frequency fixed while co-occurrence
varies, a split in the spirit of DBCA (Keysers et al., 2020)
<!-- cite:keysers2020 -->. It cannot also hold the share of fire-only episodes
fixed, which rises with co-occurrence <!-- N:DES-9 -->, and it is not
verdict-bearing (§9). The founding hypothesis, that joint training improves both
outcomes, did not occur.

At the held-out severity, joint training raises survival by 0.96 points
(Šidák-corrected 95 % CI [0.47, 1.44]) <!-- N:RES-2 --> <!-- N:DES-13 -->.
Task completion shows no detectable change: −1.73 points, CI [−4.12, +0.66]
<!-- N:RES-1 -->, which excludes a joint-training gain larger than 0.66 points
<!-- N:RES-1 -->. The registered falsifier for an asymmetric result passes
<!-- N:RES-5 -->, so the asymmetry stands. Under Definition 2 it is an asymmetry
between a penalized channel, deaths, and a rewarded one, the task. Neither
joint-versus-isolated difference keeps a stable sign over the final half of
training <!-- N:RES-11 -->: the survival gap opens only in the last fifth of the
budget <!-- N:RES-12 -->, and the completion difference leans negative from 70 %
of it onward <!-- N:RES-13 -->.

The survival gain does not survive the inert-share correction. Communication
denial is inert under our frozen random-projection message encoder at this
scale (§7), so the third of ISO's training episodes that carry only δ
<!-- N:DES-8 --> carry no active stressor. We registered this bias, and an arm
to remove it, on 2026-09-18 <!-- N:DES-15 -->, before unblinding. That arm,
ISO-4, is ISO without its δ-only episodes: a sensitivity arm outside the
confirmatory family, trained with 20 seeds <!-- N:DES-13 --> <!-- N:DES-15 -->.
Its survival is 0.98 points above ISO's <!-- N:RES-7 -->, and JOINT's survival
differs from ISO-4's by −0.03 points (CI [−0.68, +0.63]) <!-- N:RES-6 -->. As
the registration requires, we do not describe the survival advantage as a
composition effect. Two limits apply. First, the corrected contrast's upper
bound, +0.63 <!-- N:RES-6 -->, lies above the uncorrected contrast's lower
bound, +0.47 <!-- N:RES-2 -->, so the correction excludes a large composition
effect, not every composition effect. Second, removing the δ-only episodes
changes two things at once: the share of training with an active stressor rises
from two thirds to all of it <!-- N:DES-8 --> <!-- N:DES-14 -->, and each
coupling's frequency rises from a third to a half of episodes <!-- N:DES-7 -->
<!-- N:DES-14 -->. The 0.98-point rise cannot say by itself which of the two
matters; §9.2 reports what the secondary design adds on this question, including
where its fit fails. What the corrected contrast does say is that, once the
active share is matched, JOINT's remaining differences add nothing detectable to
survival: it sees each coupling twice as often as ISO-4 <!-- N:DES-14 --> and
always in combination.

The argument behind this result is general, although we measured it in one
environment: a comparison of joint and isolated training that leaves the active
share free can report an active-share effect as a composition effect. What
separates this work from earlier joint-versus-isolated comparisons is what the
comparison holds fixed. In the literature search described in §2, which read
abstracts and did not query IEEE Xplore, we found no reinforcement-learning
comparison that matches its arms on how much of training carries any stressor.

We do not claim convergence guarantees for the training procedure, or a theorem
that joint training wins: Proposition 4 bounds what isolated training can be
*guaranteed* to transfer, not what it does, and Theorem 1 concerns adaptivity
against memorization in a two-corridor toy. We do not claim an exact critical
value for the implemented kernel, whose threshold is measured. Nor do we claim
that the survival gap is robust to the training budget, since its sign is not
stable over the final half of training.

Our contributions are:

1. **An environment built as an instrument.** CHE places a lethal fire in the
   transition and observation kernels only (Definition 2), factorizes each step
   into collapse, fire, smoke, agents and communication (Proposition 1), defines
   severity by measured dynamical phase, and makes every ablation a
   bitwise-exact nested model. Its theory doubles as unit tests: the
   implementation reproduces Proposition 3's linear scaling, Theorem 1's value
   curve and Remark 2′'s value of communication (§§3–7).
2. **Calibration findings that stand without the training comparison.** As
   predicted before measurement, the supercritical fire consumes the fuel that
   collapse would ignite: under trained policies, collapse-seeded ignitions
   fall 4.8-fold from low to high severity <!-- N:CA-4 -->, while the share of
   them near agents stays flat <!-- N:CA-6 --> (§5). Smoke attenuation costs
   survival at high severity, replicated in direction three times out of three
   <!-- N:CB-5 -->, and the masking concentrates 16–118-fold on moments of
   danger <!-- N:CB-10 --> (§6). At the medium severity used for the test, its
   own measured effect on survival was −0.03 points, graded only against a
   three-seed spread <!-- N:CB-9 --> (§10). Communication is inert under our
   frozen random-projection encoder at this scale (§7).
3. **A measurement protocol in which acceptance bars come with floors.**
   Reproducibility floors are measured per metric, per GPU and per artifact;
   contrasts are graded on their own standard error; and design-stage power is
   stated as the minimum effect detectable with 80 % power
   <!-- N:METH-7 --> at the family-corrected α (§8).
4. **A pre-registered test of joint against isolated training.** Its survival
   advantage does not survive a correction registered before unblinding, and it
   points to a rule whose argument is general: match the active share before
   attributing a gain to composition (§9).
````

Three changes from draft 2, checked by a sentence-level diff: the Gao
comment, the "told about the hazard" sentence, and the γ_n sentence.

**Draft 2's findings:** 1 (selective plane fit) **resolved**: replaced by a
pointer to §9.2. 2 ("told about the hazard") **resolved**: "no reward or cost
signal mentions the hazard", and agents meet the fire "through what they
observe and what happens to them" (observation planes, ENV-7; transitions).
4 (mechanics) unchanged, staging work.

**Builder's check findings (the builder's, not the owner's text; open):**

1. **The Gao comment lost its "OWNER READS before submission" note.** The
   record still lists the read as owed (checklist :54-58; `submission.bib`
   `%` flag above `gao2024composition`; `HANDOFF.md` item 6). Removing the
   note from the comment does not discharge it. If the read is done, the
   owner says so and it is recorded; if not, the citation stays owed.
2. **New obligation for §9.2, created by the pointer:** report what the
   secondary design adds on the active-share-versus-frequency question
   (γ_n, SEC-1, SEC-3), **and where its fit fails** (γ_p's prediction for
   JOINT − ISO-4, ≈ +3.3 points, SEC-4, against Γ₄ −0.03, RES-6).
3. **Still owed:** a verified CMDP / safe-RL entry (the comment remains).
4. No other change; everything else as checked in draft 2.

## 2026-10-10 · §1 Introduction · called done

The owner's final text is draft 3, verbatim, now in `paper/finale.md` after
the abstract. The builder added one comment, `<!-- N:ENV-11 -->` after "one
policy per training seed"; stripping it reproduces draft 3 exactly
(checked). Gao et al. read by the owner (with LLM summaries alongside), so
finding 1 is **resolved**. Finding 2 (§9.2 obligation) and 3 (CMDP / safe-RL
entry) carry forward. Decision log: §1 INTRODUCTION.

## 2026-10-10 · §2 Related work · draft 1

Owner's draft, verbatim:

````markdown
## 2 Related work

This section says, for each line of work, where it places the hazard and what
its comparisons hold fixed. §1 stated what our comparison holds fixed; how we
searched is described at the end.

**Where the hazard enters learning.** In multi-agent wildfire fighting the
hazard is the objective. Haksar & Schwager (2018) <!-- cite:haksar2018 -->
train aerial agents with a multi-agent deep Q-network and reward them for moving
to burning trees on the fire's boundary (their Algorithm 2); the fire cannot
harm them. JaxWildfire (Çakır et al., 2025) <!-- cite:cakir2025jaxwildfire |
read in full 2026-10-10 by an assistant; OWNER skims before submission -->, a
JAX cellular-automaton wildfire simulator, trains a single air-tanker agent
whose reward is a per-step penalty proportional to the number of burning cells,
with a bonus for full extinction. In constrained Markov decision processes a
hazard can instead be priced as a cost held below a bound (Altman, 1999)
<!-- cite:altman1999cmdp | verified 2026-10-10; add to
related_work_verification.md before it enters the .bib -->, and safe
reinforcement learning more broadly treats safety as constraints to respect
during learning or deployment (García & Fernández, 2015)
<!-- cite:garcia2015safe | same status as altman1999cmdp -->. VULCAN (Liu &
Yan, 2026) <!-- cite:liu2026vulcan -->, a multi-robot fire search-and-rescue
system planned by a vision-language model rather than learned, folds smoke and
heat into a hazard cost map. Its evaluation metric is also abbreviated CHE
(cumulative hazard exposure), which is unrelated to our environment's name. In
CHE no reward, cost or constraint reads the fire (Definition 2); the reward
prices deaths, whatever their cause.

**A hazard that feeds on itself.** Coupling A lets structural collapse add
ignitions. The nearest neighbour we found is Raut et al. (2026)
<!-- cite:raut2026psps | read in full 2026-10-10 by an assistant -->, who model
public-safety power shutoffs as a single-agent decision problem: the power
flows that follow from the operator's switching decisions set the failure
probability of lines in wildfire areas, which the authors treat as ignition
risk. Their reward is negative operating cost, and there is no spatial spread
model. In their model the hazard's growth runs through the controlled decision.
In CHE it runs through the environment: a collapse seeds fire with no action in
the path. Collapse itself is not independent of the agents, however. An agent
standing on a weak cell raises that cell's collapse rate nine-fold
<!-- N:CA-1, DERIVED (5e-5 + 4e-4) / 5e-5 = 9; needs its own ledger row -->
(Definition 5). So we do not claim that CHE's hazard grows without agent
influence. We claim only that ignition is a side effect of where agents stand,
not a variable they control.

**Perception degraded by the hazard.** Coupling B attenuates each agent's
observation by Beer–Lambert transmittance along the line of sight through smoke.
VULCAN degrades simulated sensing with smoke density and visibility loss, but
it has no transmittance model and estimates smoke density from image
degradation. JaxWildfire's observations are partial and egocentric but not
attenuated. In the search described below, we found no reinforcement-learning
environment whose observation kernel attenuates by transmittance.

**Simulators and benchmarks in JAX.** CHE follows JaxMARL's environment
conventions (Rutherford et al., 2024) <!-- cite:rutherford2024jaxmarl --> and
trains with independent PPO (de Witt et al., 2020) <!-- cite:dewitt2020ippo -->.
Among the JAX multi-agent benchmarks we surveyed, JaxMARL, Multi-Agent Craftax
(Al Omari et al., 2025) <!-- cite:alomari2025macraftax --> and Assistax
(Hinckeldey et al., 2025) <!-- cite:hinckeldey2025assistax -->, none has an
evolving, spreading lethal hazard field or perception attenuated by the hazard.
Multi-Agent Craftax comes closest in kind: its agents lose health to hunger and
enemies and can die, and its lava is lethal, but the lava is static terrain.
<!-- MA-Craftax's released code (craftax_ma/game_logic.py) also prices health
changes at +/-0.1 per point, close to our cause-blind death penalty; Crafter
(Hafner 2022) and Craftax (Matthews et al. 2024) state this in their papers but
have no verified bib entries yet --> POBAX (Tao et al., 2025)
<!-- cite:tao2025pobax --> is a single-agent suite for partial observability,
and BenchMARL (Bettini et al., 2024) <!-- cite:bettini2024benchmarl --> is a
multi-agent benchmarking library built on TorchRL rather than JAX. JaxWildfire
has a spreading fire in JAX, but one agent, which the fire cannot harm.

**Choosing a training distribution.** Domain randomization trains on a broad,
fixed distribution over simulator parameters so that the deployed setting looks
like one more sample (Tobin et al., 2017) <!-- cite:tobin2017dr -->; Muratore
et al. (2022) <!-- cite:muratore2022drreview --> review the approach.
Unsupervised environment design adapts the distribution to the learner instead.
PAIRED generates environments from a regret objective (Dennis et al., 2020)
<!-- cite:dennis2020paired -->; Prioritized Level Replay revisits levels by
their estimated learning potential (Jiang et al., 2021a)
<!-- cite:jiang2021plr --> and was later recast as environment design (Jiang et
al., 2021b) <!-- cite:jiang2021robustplr -->; and ACCEL evolves levels near
the frontier of the agent's ability (Parker-Holder et al., 2022)
<!-- cite:parkerholder2022accel -->. These methods ask which distribution to
train on, usually adaptively. We compare two fixed distributions and evaluate
no adaptive curriculum (§10). Kirk et al. (2023) <!-- cite:kirk2023zsg -->
survey zero-shot generalization in reinforcement learning, the broader problem
our held-out test belongs to.

**Compositional generalization over environmental factors.** The closest
earlier study of our question is Gao et al. (2024)
<!-- cite:gao2024composition -->. In goal-conditioned visual imitation learning
for robotic manipulation, they ask whether policies compose environmental
factors, such as object type and position, table texture and height, and camera
position, to succeed on unseen combinations, and they use the answer to design
data collection. One of their strategies varies a single factor at a time from a
base setting; another cycles through factors so that more combinations appear.
They compare strategies at a matched number of demonstrations and a matched
count of factor changes, which they use as a rough proxy for collection effort
(their §III-C and §IV-A). Policies do compose, more weakly when both factors
are physical (their §V-B), and the strategy that covers more combinations does
better. Their design matches data quantity and effort. It does not match how
often each factor value appears, or the share of data that departs from the base
setting. Ours matches compute and, in the ISO-4 correction, the share of
training that carries any stressor. The settings differ too: their factors
change what the robot sees and must do, while ours are causally coupled to a
lethal hazard; their policies are learned by imitation, ours by multi-agent
reinforcement learning. CompoSuite (Mendez et al., 2022)
<!-- cite:mendez2022composuite --> studies compositional multi-task
reinforcement learning over robots, objects, objectives and obstacles, which is
composition of tasks, not of co-occurring stressors. The DBCA method of Keysers
et al. (2020) <!-- cite:keysers2020 --> builds splits whose atom distributions
are similar and whose compound distributions differ. Our secondary sweep follows
that idea, holding each coupling's frequency fixed while co-occurrence varies;
our ISO and JOINT endpoints do not (§1, §9).

**Mixed and simultaneous perturbations.** Robust reinforcement learning asks the
same question about perturbations. Erdem & Üre (2025)
<!-- cite:erdem2025mixed | read in full 2026-10-10 by an assistant; OWNER skims
before submission --> find, in single-agent continuous control against a
learned adversary, that agents trained against observation-only or action-only
attacks remain vulnerable to simultaneous attacks on both, and they propose an
adversary that balances its budget across the two. In their comparison every
adversarial arm is perturbed at every step, and the mixed arms train under the
combined budget, which the authors note is more severe. It is therefore not a
comparison at matched exposure, and its direction neither supports nor
contradicts our corrected null. Agrawal et al. (2023)
<!-- cite:agrawal2023multimodal --> train multi-agent policies against random
reward, state and action noise with a curriculum that raises the noise level,
one or two noise types at a time; the curriculum sets training length, so
exposure differs between their models. Neither reinforcement-learning comparison
matches the share of training that carries any perturbation. In supervised
vision, Tramèr & Boneh (2019) <!-- cite:tramer2019multiple --> and Hsiung et
al. (2023) <!-- cite:hsiung2023compositional --> study robustness to multiple
and to composite perturbations.

**Theory.** Chen et al. (2022) <!-- cite:chen2022understandingdr | read in full
2026-10-10 by an assistant; OWNER skims before submission --> analyse domain
randomization as finding the optimal policy of a latent MDP and bound its
sim-to-real gap. They argue that history-dependent policies are needed to
identify the latent environment, and their Proposition 1 constructs a case in
which it cannot be identified before the agent must commit. Theorem 1 here is
related in spirit: it gives an exact value for a partially observed two-corridor
toy in which how identifiable the environment is before commitment is set
continuously by perception attenuation, and its no-information endpoint is the
coin-flip commitment of their construction. Chen et al. have no observation
channel, since their states are fully observed, and they give rates rather than
exact values, so they do not subsume it. For communication, Pynadath & Tambe
(2002) <!-- cite:pynadath2002 --> show that the complexity of team decision
problems with communication depends on observability: communication makes no
difference when the world is individually observable or not observable at all,
and free communication lowers the complexity when it is collectively observable
(their §3, Theorems 5–6 and Table 2). Remark 2′ refines this for collective
partial observability: communication's marginal value vanishes when
interchangeable agents' views are redundant, and returns when roles are
irreplaceable or deaths are costly (§7). The survey of adaptability in
multi-agent reinforcement learning by Hu et al. (2025)
<!-- cite:hu2025adaptablemarl --> recommends environment families that vary one
factor at a time while holding the others fixed. It does not treat combined
factors.

**How we searched.** We ran the literature search with the help of LLM-based
research assistants, between August and October 2026. A census of benchmark
venues and a search for theorems that could subsume ours came first; a search of
domain randomization, environment design, multi-task and robust-learning
neighbours followed. Both used web search and the arXiv API and read abstracts.
The works this section describes in detail were then read in full; the
remaining citations rest on their abstracts. We did not query IEEE Xplore.
Wherever this paper says that no work does something, it means no work found by
this search.
````

(Builder check in progress: external claims sent to web-verification agents at the owner's invitation; findings appended when they return.)

**Builder's check findings, part 1: internal (the builder's; open):**

1. **Conflict with a ruling: the owed reads.** CITATION REPOSITIONING RULING
   (owner, 2026-09-26) item 2: Erdem & Üre "is owed a full read by the owner
   before the paper characterizes it"; item 3: Chen et al. "is owed a read
   before the paper claims Theorem 1 is unsubsumed"; NO-SCOOP CHECKS
   (2026-08-13): read the JaxWildfire and arXiv:2604.26150 PDFs "directly".
   The draft characterizes all four from an assistant's full read, with "OWNER
   skims before submission". Either the owner reads them, or a new ruling
   replaces the requirement, transcribed first.
2. **Conflict, terminology: "ours are causally coupled to a lethal hazard"**
   (Gao paragraph). δ is independent of the fire (D1; the abstract,
   `description` and §1 all say so).
3. **Overreach: "ignition is … not a variable they control".** Agents'
   positions set the collapse rate 9× (CA-8, added today; `structure.py:78`;
   load is boolean, so any occupancy), and position is set by their movement
   actions; CA-7: no weak-cell avoidance was learned, weak occupancy rose under
   κ_A. Both models are agent-mediated and indirect. What does differ in the
   record: ignition is in Raut et al.'s decision problem and in no CHE reward
   (Def. 2), and λ₀ > 0 collapses cells with no agent present.
4. **"How we searched": "the works this section describes in detail were
   then read in full".** `related_work_verification.md` still records every
   work at abstract level; the 2026-10-10 full reads happened outside this
   session's record. The draft's comments mark four (JaxWildfire, Raut,
   Erdem & Üre, Chen) and Gao (owner); the detailed claims about Haksar
   (Algorithm 2), VULCAN, Pynadath & Tambe (theorem numbers), Agrawal, Hu
   and the MA-Craftax code go beyond abstracts too. Which were read in full,
   and by whom, needs recording for the sentence to be backed.
5. **Obligation forwarded to §10:** "evaluate no adaptive curriculum (§10)".
   Spine §10 item 9 carries it ("no DR schedule, no PLR/ACCEL curriculum").
6. **Checked and supported:** Beer–Lambert "along the line of sight"
   (`observation.py:13-14`, ray quadrature); 9× (CA-8); Theorem 1's exact
   value ½ + q/2 and its no-information endpoint ½ as κ_B → ∞ (theory doc);
   Remark 2′ (zero marginal value when agents are interchangeable,
   expendable and numerous enough; returns when roles are irreplaceable or
   deaths are costly); JaxMARL conventions and IPPO (CLAUDE.md, ENV-11); the
   sweep and ISO-4 descriptions (DES-9, DES-14).
7. **Mechanics:** new keys `altman1999cmdp`, `garcia2015safe` need verified
   entries first (agents checking); `cakir2025jaxwildfire`'s author field
   renders raw LaTeX in Distill (one of the 8 fields). The 9× comment is not
   in `N:ID` form; its row is now CA-8.

Part 2 (external claims, web-checked) follows when the agents return.

**Builder's check findings, part 2: external claims, web-checked (the
builder's; open).** Four agents read the full texts (and the MA-Craftax
code). Record: `paper/related_work_verification.md` Part 3.

*Overreach*
8. **JaxWildfire "which the fire cannot harm" (said twice).** The paper never
   mentions agent harm and its code is unreleased: inference from silence.
9. **MA-Craftax "its lava is lethal".** Not in MA-Craftax: players cannot
   enter lava (collision map) and its game logic has no lava damage. Lava is
   lethal in Crafter and Craftax-Classic. "Static terrain" is right.
10. **Chen et al. "the coin-flip commitment of their construction".** Their
    Prop. 1 instance is an M-way irreversible commitment (wrong w.p.
    1 − 1/M), stated for dropping Assumption 1; a coin flip only at M = 2,
    which they never take. Non-identifiability appears in the proof
    (App. G.1). The rest of the paragraph (latent MDP, rates, fully observed
    states; history-dependence argued, not proven) is supported.
11. **Gao et al., two places.** (a) "It does not match … the share of data
    that departs from the base setting": in their real L-vs-Stair pair that
    share is equal (15/16) by construction, though never discussed; value
    frequencies do differ. (b) "a matched count of factor changes":
    demonstrations are matched within a subplot; factor changes measure
    effort and are not matched across strategies (Complete 100, Single
    Factor ≤ 10). Minor: "goal-conditioned" holds for the formal setup and
    real-robot runs, not the simulation runs.
12. **Hu et al.** The held-fixed recommendation is in v2 only (2026; the
    citation says 2025) and reads "systematically varies … while holding
    other factors fixed", not "one factor at a time". "It does not treat
    combined factors" overreaches: it mentions compositional generalization
    and compositional policies; what it lacks is an analysis of simultaneous
    multi-factor shifts.
13. **VULCAN "system".** Key components with preliminary evaluation; VULCAN
    itself is not evaluated (baselines only), deployment "ongoing". Minor:
    the hazard map also includes sensing uncertainty; smoke density is
    inferred from RGB degradation *and* depth consistency.
14. **Pynadath & Tambe "(their §3, Theorems 5–6 and Table 2)".** Theorems
    5–6 give the no-difference cases; "free communication lowers the
    complexity when collectively observable" is Theorem 4 (NEXP → P).
15. **Minor:** García & Fernández define safe RL as ensuring "reasonable
    system performance and/or" respecting constraints; the draft gives the
    constraint half. Erdem & Üre's "every arm perturbed at every step" is an
    inference (no sentence states it); "combined budget" is the draft's
    phrase (separate per-modality caps).

*Bibliography*
16. **García & Fernández: verified and entered** (`garcia2015safe`, JMLR;
    `submission.bib` now 38 entries). **Altman: owner's choice.** The DOI
    resolves to the 2021 Routledge reissue; the 1999 Chapman & Hall/CRC
    original (ISBN 9780849303821) has no single verbatim record. The draft
    says "Altman, 1999".
17. **Caveat a reviewer may raise:** MA-Craftax perception is attenuated by
    darkness (not a hazard); the draft's "by the hazard" is precise.

*Supported* (with the scope above): Haksar & Schwager (MADQN; boundary-tree
reward, one of five terms; no damage state); JaxWildfire (JAX CA, one
air-tanker agent, burning-cell penalty + terminal bonus, unattenuated partial
egocentric observations); VULCAN (VLM planner, hazard cost map, CHE =
cumulative hazard exposure); Raut et al. (authors confirmed; one PPO agent;
flow-set line failure ≈ ignition risk; negative operating cost; no spread);
MA-Craftax health and death, no spreading hazard; JaxMARL, Assistax, POBAX,
BenchMARL; Gao's strategies and section numbers; Erdem & Üre's setting,
finding and "more severe" note; Agrawal et al. throughout; Chen et al.
except finding 10; Pynadath & Tambe's results.

## 2026-10-10 · §2 Related work · draft 2

Owner's draft, verbatim:

````markdown
## 2 Related work

This section says, for each line of work, where it places the hazard and what
its comparisons hold fixed. §1 stated what our comparison holds fixed; how we
searched is described at the end.

**Where the hazard enters learning.** In multi-agent wildfire fighting the
hazard is the objective. Haksar & Schwager (2018) <!-- cite:haksar2018 -->
train aerial agents with a multi-agent deep Q-network and reward them for moving
to burning trees on the fire's boundary (their Algorithm 2); the paper gives the
fire no way to harm them. JaxWildfire (Çakır et al., 2025)
<!-- cite:cakir2025jaxwildfire | read in full 2026-10-10 by an assistant; OWNER
skims before submission -->, a JAX cellular-automaton wildfire simulator,
trains a single air-tanker agent whose reward is a per-step penalty proportional
to the number of burning cells, with a bonus for full extinction; the paper does
not describe harm to the agent. Safe reinforcement learning, which García &
Fernández (2015) <!-- cite:garcia2015safe --> define as learning policies that
maximize return while ensuring reasonable system performance and/or respecting
safety constraints, typically places a hazard in a constraint or a cost. VULCAN
(Liu & Yan, 2026) <!-- cite:liu2026vulcan -->, which reports the key components
and a preliminary evaluation of a multi-robot fire search-and-rescue approach
planned by a vision-language model rather than learned, folds smoke, heat and
sensing uncertainty into a hazard cost map. Its evaluation metric is also
abbreviated CHE (cumulative hazard exposure), which is unrelated to our
environment's name. In CHE no reward, cost or constraint reads the fire
(Definition 2); the reward prices deaths, whatever their cause.

**A hazard that feeds on itself.** Coupling A lets structural collapse add
ignitions. The nearest neighbour we found is Raut et al. (2026)
<!-- cite:raut2026psps | read in full 2026-10-10 by an assistant -->, who model
public-safety power shutoffs as a single-agent decision problem: the power
flows that follow from the operator's switching decisions set the failure
probability of lines in wildfire areas, which the authors treat as ignition
risk. Their reward is negative operating cost, and there is no spatial spread
model. In their model the hazard's growth runs through the controlled decision.
In CHE it runs through the environment: a collapse seeds fire with no action in
the path. Collapse itself is not independent of the agents, however. An agent
standing on a weak cell raises that cell's collapse rate nine-fold
<!-- N:CA-1, DERIVED (5e-5 + 4e-4) / 5e-5 = 9; needs its own ledger row -->
(Definition 5). So we do not claim that CHE's hazard grows without agent
influence. We claim only that ignition is a side effect of where agents stand,
not a variable they control.

**Perception degraded by the hazard.** Coupling B attenuates each agent's
observation by Beer–Lambert transmittance along the line of sight through smoke.
VULCAN degrades simulated sensing with smoke density and visibility loss and
infers smoke density from image degradation and depth consistency, but it has
no transmittance model. JaxWildfire's observations are partial and egocentric
but not attenuated. In the search described below, we found no
reinforcement-learning environment whose observation kernel attenuates by
transmittance.

**Simulators and benchmarks in JAX.** CHE follows JaxMARL's environment
conventions (Rutherford et al., 2024) <!-- cite:rutherford2024jaxmarl --> and
trains with independent PPO (de Witt et al., 2020) <!-- cite:dewitt2020ippo -->.
Among the JAX multi-agent benchmarks we surveyed, JaxMARL, Multi-Agent Craftax
(Al Omari et al., 2025) <!-- cite:alomari2025macraftax --> and Assistax
(Hinckeldey et al., 2025) <!-- cite:hinckeldey2025assistax -->, none has an
evolving, spreading lethal hazard field or perception attenuated by a hazard.
Multi-Agent Craftax comes closest in kind: its agents lose health to hunger and
enemies and can die, but its lava is static terrain that agents cannot enter.
Its single-agent predecessors make lava lethal and, like CHE, price an outcome
rather than the hazard: Crafter and Craftax reward each health point regained
and penalize each one lost (Hafner, 2022; Matthews et al., 2024)
<!-- cite:hafner2022crafter --> <!-- cite:matthews2024craftax | both BibTeX
retrieved and parked; enter via related_work_verification.md if kept -->, much as
our reward prices each death. POBAX (Tao et al., 2025)
<!-- cite:tao2025pobax --> is a single-agent suite for partial observability,
and BenchMARL (Bettini et al., 2024) <!-- cite:bettini2024benchmarl --> is a
multi-agent benchmarking library built on TorchRL rather than JAX. JaxWildfire
has a spreading fire in JAX, with one agent.

**Choosing a training distribution.** Domain randomization trains on a broad,
fixed distribution over simulator parameters so that the deployed setting looks
like one more sample (Tobin et al., 2017) <!-- cite:tobin2017dr -->; Muratore
et al. (2022) <!-- cite:muratore2022drreview --> review the approach.
Unsupervised environment design adapts the distribution to the learner instead.
PAIRED generates environments from a regret objective (Dennis et al., 2020)
<!-- cite:dennis2020paired -->; Prioritized Level Replay revisits levels by
their estimated learning potential (Jiang et al., 2021a)
<!-- cite:jiang2021plr --> and was later recast as environment design (Jiang et
al., 2021b) <!-- cite:jiang2021robustplr -->; and ACCEL evolves levels near
the frontier of the agent's ability (Parker-Holder et al., 2022)
<!-- cite:parkerholder2022accel -->. These methods ask which distribution to
train on, usually adaptively. We compare two fixed distributions and evaluate
no adaptive curriculum (§10). Kirk et al. (2023) <!-- cite:kirk2023zsg -->
survey zero-shot generalization in reinforcement learning, the broader problem
our held-out test belongs to.

**Compositional generalization over environmental factors.** The closest
earlier study of our question is Gao et al. (2024)
<!-- cite:gao2024composition -->. In visual imitation learning for robotic
manipulation, they ask whether policies compose environmental factors, such as
object type and position, table texture and height, and camera position, to
succeed on unseen combinations, and they use the answer to design data
collection. One of their strategies varies a single factor at a time from a base
setting; another cycles through factors so that more combinations appear. They
compare strategies at a matched number of demonstrations, across levels of a
rough effort proxy, the number of factor changes (their §III-C and §IV-A).
Policies do compose, more weakly when both factors are physical (their §V-B),
and the strategy that covers more combinations does better. Their design is
built for data efficiency, not to separate co-occurrence from how often each
factor value appears. Ours matches compute and, in the ISO-4 correction, the
share of training that carries any stressor. The settings differ too: their
factors change what the robot sees and must do, while ours are causally coupled
to a lethal hazard; their policies are learned by imitation, ours by multi-agent
reinforcement learning. CompoSuite (Mendez et al., 2022)
<!-- cite:mendez2022composuite --> studies compositional multi-task
reinforcement learning over robots, objects, objectives and obstacles, which is
composition of tasks, not of co-occurring stressors. The DBCA method of Keysers
et al. (2020) <!-- cite:keysers2020 --> builds splits whose atom distributions
are similar and whose compound distributions differ. Our secondary sweep follows
that idea, holding each coupling's frequency fixed while co-occurrence varies;
our ISO and JOINT endpoints do not (§1, §9).

**Mixed and simultaneous perturbations.** Robust reinforcement learning asks the
same question about perturbations. Erdem & Üre (2025)
<!-- cite:erdem2025mixed | read in full 2026-10-10 by an assistant; OWNER skims
before submission --> find, in single-agent continuous control against a
learned adversary, that agents trained against observation-only or action-only
attacks remain vulnerable to simultaneous attacks on both, and they propose an
adversary that balances its budget across the two. Their mixed arms train under
the combined budget of both attack types, which the authors note is more
severe, so the comparison is not made at matched exposure, and its direction
neither supports nor contradicts our corrected null. Agrawal et al. (2023)
<!-- cite:agrawal2023multimodal --> train multi-agent policies against random
reward, state and action noise with a curriculum that raises the noise level,
one or two noise types at a time; the curriculum sets training length, so
exposure differs between their models. Neither reinforcement-learning comparison
matches the share of training that carries any perturbation. In supervised
vision, Tramèr & Boneh (2019) <!-- cite:tramer2019multiple --> and Hsiung et
al. (2023) <!-- cite:hsiung2023compositional --> study robustness to multiple
and to composite perturbations.

**Theory.** Chen et al. (2022) <!-- cite:chen2022understandingdr | read in full
2026-10-10 by an assistant; OWNER skims before submission --> analyse domain
randomization as finding the optimal policy of a latent MDP and bound its
sim-to-real gap. They argue that history-dependent policies are needed to
identify the latent environment, and their Proposition 1 constructs a case in
which the agent must make an irreversible choice among several environments
before it can identify the true one. Theorem 1 here is related in spirit: it
gives an exact value for a partially observed two-corridor toy in which how
identifiable the environment is before commitment is set continuously by
perception attenuation, and its no-information endpoint is an uninformed
commitment of the same kind, two-way here and many-way there. Chen et al. have
no observation channel, since their states are fully observed, and they give
rates rather than exact values, so they do not subsume it. For communication,
Pynadath & Tambe (2002) <!-- cite:pynadath2002 --> relate the complexity of
team decision problems with communication to observability. Free communication
lowers the complexity when the world is collectively observable (their
Theorem 4 and Table 2), and communication makes no difference when it is
individually observable or not observable at all (Theorems 5–6). Remark 2′
refines this for collective partial observability: communication's marginal
value vanishes when interchangeable agents' views are redundant, and returns
when roles are irreplaceable or deaths are costly (§7). The survey of
adaptability in multi-agent reinforcement learning by Hu et al. (2025, revised
2026) <!-- cite:hu2025adaptablemarl | the recommendation quoted is in v2 only
--> calls an environment family highly diagnostic if it "systematically varies"
factors such as population, observability or communication structure "while
holding other factors fixed". It mentions compositional generalization but does
not analyse shifts in several factors at once.

**How we searched.** We ran the literature search with the help of LLM-based
research assistants, between August and October 2026. A census of benchmark
venues and a search for theorems that could subsume ours came first; a search of
domain randomization, environment design, multi-task and robust-learning
neighbours followed. Both used web search and the arXiv API and read abstracts.
The works this section describes in detail were then read in full; the
remaining citations rest on their abstracts. We did not query IEEE Xplore.
Wherever this paper says that no work does something, it means no work found by
this search.
````

**Draft 1's findings:** part 2's 8 (JaxWildfire harm) **resolved**; 9
(MA-Craftax lava) **resolved**; 10 (Chen's coin flip) **resolved**: "several
environments", "two-way here and many-way there"; 11 (Gao) **resolved**: "at
a matched number of demonstrations, across levels of a rough effort proxy";
"built for data efficiency, not to separate co-occurrence from how often each
factor value appears"; "goal-conditioned" dropped; 12 (Hu) **resolved**:
v2 dated, quoted, scope narrowed; 13 (VULCAN) **mostly resolved**, see 3
below; 14 (Pynadath theorem numbers) **resolved**; 15 **resolved** (García's
definition in full; Erdem & Üre's "every step" dropped); 16: Altman dropped,
García cited; Crafter and Craftax now cited and **entered**
(`hafner2022crafter`, `matthews2024craftax`; `submission.bib` 40 entries;
every key the draft cites exists). Part 1's 4 ("read in full") **resolved**
by the Part 3 record together with "with the help of LLM-based research
assistants".

**Builder's check findings (the builder's; open):**

1. **Unresolved, part 1's 1: the owed reads.** The comments still read "read
   in full … by an assistant; OWNER skims", against the 2026-09-26 ruling
   (Erdem & Üre: a full read by the owner before characterizing; Chen et al.:
   a read before "do not subsume it", which the draft now claims). The owner
   reads them, or a new ruling is transcribed first.
2. **Unresolved, part 1's 2: "ours are causally coupled to a lethal hazard"**
   (Gao paragraph). δ is not.
3. **Unresolved, part 1's 3: "not a variable they control"** (CA-8).
4. **Minor, VULCAN: "reports … a preliminary evaluation of a … approach".**
   Its preliminary evaluation (Tables I–II) covers the baselines only;
   VULCAN itself is not evaluated (Sec. III-C).
5. **Minor, "Its single-agent predecessors make lava lethal".** True of
   Crafter and Craftax-Classic; in full Craftax lava is blocked, not lethal
   (Part 3), and the cited Matthews et al. covers both.
6. **Mechanics:** the 9× comment still reads "N:CA-1, DERIVED …; needs its
   own ledger row"; the row exists now (CA-8).
7. **Available, the owner's call:** `garcia2015safe` can now carry §1's
   uncited safe-RL sentence (a §1 edit).

## 2026-10-10 · §2 Related work · draft 3

Owner's draft, verbatim:

````markdown
## 2 Related work

This section says, for each line of work, where it places the hazard and what
its comparisons hold fixed. §1 stated what our comparison holds fixed; how we
searched is described at the end.

**Where the hazard enters learning.** In multi-agent wildfire fighting the
hazard is the objective. Haksar & Schwager (2018) <!-- cite:haksar2018 -->
train aerial agents with a multi-agent deep Q-network and reward them for moving
to burning trees on the fire's boundary (their Algorithm 2); the paper gives the
fire no way to harm them. JaxWildfire (Çakır et al., 2025)
<!-- cite:cakir2025jaxwildfire | read in full 2026-10-10 by an assistant -->, a
JAX cellular-automaton wildfire simulator, trains a single air-tanker agent
whose reward is a per-step penalty proportional to the number of burning cells,
with a bonus for full extinction; the paper does not describe harm to the agent.
Safe reinforcement learning, which García & Fernández (2015)
<!-- cite:garcia2015safe --> define as learning policies that maximize return
while ensuring reasonable system performance and/or respecting safety
constraints, typically places a hazard in a constraint or a cost. VULCAN (Liu &
Yan, 2026) <!-- cite:liu2026vulcan -->, a proposed multi-robot fire
search-and-rescue approach planned by a vision-language model rather than
learned, folds smoke, heat and sensing uncertainty into a hazard cost map; its
preliminary evaluation covers baselines, not the approach itself. Its evaluation
metric is also abbreviated CHE (cumulative hazard exposure), which is unrelated
to our environment's name. In CHE no reward, cost or constraint reads the fire
(Definition 2); the reward prices deaths, whatever their cause.

**A hazard that feeds on itself.** Coupling A lets structural collapse add
ignitions. The nearest neighbour we found is Raut et al. (2026)
<!-- cite:raut2026psps | read in full 2026-10-10 by an assistant -->, who model
public-safety power shutoffs as a single-agent decision problem: the power
flows that follow from the operator's switching decisions set the failure
probability of lines in wildfire areas, which the authors treat as ignition
risk. Their reward is negative operating cost, and there is no spatial spread
model. CHE's agents influence the hazard too, but less directly. An agent
standing on a weak cell raises that cell's collapse rate nine-fold
<!-- N:CA-8 --> (Definition 5), agents choose where to stand, and a collapse
may then seed fire. So we do not claim that CHE's hazard grows without agent
influence. The difference from Raut et al. is one of directness: there the
controlled decision sets the failure probability, while here ignition is not an
action available to the agents and follows only from where they choose to
stand.

**Perception degraded by the hazard.** Coupling B attenuates each agent's
observation by Beer–Lambert transmittance along the line of sight through smoke.
VULCAN degrades simulated sensing with smoke density and visibility loss and
infers smoke density from image degradation and depth consistency, but it has
no transmittance model. JaxWildfire's observations are partial and egocentric
but not attenuated. In the search described below, we found no
reinforcement-learning environment whose observation kernel attenuates by
transmittance.

**Simulators and benchmarks in JAX.** CHE follows JaxMARL's environment
conventions (Rutherford et al., 2024) <!-- cite:rutherford2024jaxmarl --> and
trains with independent PPO (de Witt et al., 2020) <!-- cite:dewitt2020ippo -->.
Among the JAX multi-agent benchmarks we surveyed, JaxMARL, Multi-Agent Craftax
(Al Omari et al., 2025) <!-- cite:alomari2025macraftax --> and Assistax
(Hinckeldey et al., 2025) <!-- cite:hinckeldey2025assistax -->, none has an
evolving, spreading lethal hazard field or perception attenuated by a hazard.
Multi-Agent Craftax comes closest in kind: its agents lose health to hunger and
enemies and can die, but its lava is static terrain that agents cannot enter.
In Crafter and in Craftax-Classic, the JAX reimplementation described alongside
Craftax, lava is lethal; and Crafter and Craftax reward each health point
regained and penalize each one lost (Hafner, 2022; Matthews et al., 2024)
<!-- cite:hafner2022crafter --> <!-- cite:matthews2024craftax | both BibTeX
retrieved and parked; enter via related_work_verification.md if kept -->,
pricing an outcome rather than the hazard, much as our reward prices each death.
POBAX (Tao et al., 2025) <!-- cite:tao2025pobax --> is a single-agent suite
for partial observability, and BenchMARL (Bettini et al., 2024)
<!-- cite:bettini2024benchmarl --> is a multi-agent benchmarking library built
on TorchRL rather than JAX. JaxWildfire has a spreading fire in JAX, with one
agent.

**Choosing a training distribution.** Domain randomization trains on a broad,
fixed distribution over simulator parameters so that the deployed setting looks
like one more sample (Tobin et al., 2017) <!-- cite:tobin2017dr -->; Muratore
et al. (2022) <!-- cite:muratore2022drreview --> review the approach.
Unsupervised environment design adapts the distribution to the learner instead.
PAIRED generates environments from a regret objective (Dennis et al., 2020)
<!-- cite:dennis2020paired -->; Prioritized Level Replay revisits levels by
their estimated learning potential (Jiang et al., 2021a)
<!-- cite:jiang2021plr --> and was later recast as environment design (Jiang et
al., 2021b) <!-- cite:jiang2021robustplr -->; and ACCEL evolves levels near
the frontier of the agent's ability (Parker-Holder et al., 2022)
<!-- cite:parkerholder2022accel -->. These methods ask which distribution to
train on, usually adaptively. We compare two fixed distributions and evaluate
no adaptive curriculum (§10). Kirk et al. (2023) <!-- cite:kirk2023zsg -->
survey zero-shot generalization in reinforcement learning, the broader problem
our held-out test belongs to.

**Compositional generalization over environmental factors.** The closest
earlier study of our question is Gao et al. (2024)
<!-- cite:gao2024composition | read in full 2026-10-10 by Claude and by the
owner -->. In visual imitation learning for robotic manipulation, they ask
whether policies compose environmental factors, such as object type and
position, table texture and height, and camera position, to succeed on unseen
combinations, and they use the answer to design data collection. One of their
strategies varies a single factor at a time from a base setting; another cycles
through factors so that more combinations appear. They compare strategies at a
matched number of demonstrations, across levels of a rough effort proxy, the
number of factor changes (their §III-C and §IV-A). Policies do compose, more
weakly when both factors are physical (their §V-B), and the strategy that covers
more combinations does better. Their design is built for data efficiency, not
to separate co-occurrence from how often each factor value appears. Ours matches
compute and, in the ISO-4 correction, the share of training that carries any
stressor. The settings differ too: their factors change what the robot sees and
must do, while two of our stressors are causally coupled to a lethal hazard and
the third is independent of it; their policies are learned by imitation, ours
by multi-agent reinforcement learning. CompoSuite (Mendez et al., 2022)
<!-- cite:mendez2022composuite --> studies compositional multi-task
reinforcement learning over robots, objects, objectives and obstacles, which is
composition of tasks, not of co-occurring stressors. The DBCA method of Keysers
et al. (2020) <!-- cite:keysers2020 --> builds splits whose atom distributions
are similar and whose compound distributions differ. Our secondary sweep follows
that idea, holding each coupling's frequency fixed while co-occurrence varies;
our ISO and JOINT endpoints do not (§1, §9).

**Mixed and simultaneous perturbations.** Robust reinforcement learning asks the
same question about perturbations. Erdem & Üre (2025)
<!-- cite:erdem2025mixed | read in full 2026-10-10 by Claude (publisher's
version of record) --> train single-agent continuous-control policies against a
learned adversary that perturbs observations, actions, or both. In their
formulation the adversary acts at every step (their §3.4 and Algorithm 1). Agents
trained against one modality remain vulnerable to simultaneous attacks on both
(their Tables 3–4), and an adversary that learns to balance its budget across
the two produces agents that also hold up better against single-type attacks.
No arm in their comparison trains on a mixture of single-type attacks. Each
single-type arm never meets the other modality, and the mixed arms carry the
combined budget, which the authors note is more severe. Their comparison
therefore bundles seeing both modalities at all, seeing them together, and a
larger budget. Its direction matches our uncorrected contrast, and it carries
the confound our correction removes, so it neither supports nor contradicts our
corrected null. Agrawal et al. (2023) <!-- cite:agrawal2023multimodal --> train
multi-agent policies against random reward, state and action noise with a
curriculum that raises the noise level, one or two noise types at a time; the
curriculum sets training length, so exposure differs between their models.
Neither reinforcement-learning comparison matches the share of training that
carries any perturbation together with which perturbations each arm sees. In
supervised vision, Tramèr & Boneh (2019) <!-- cite:tramer2019multiple --> and
Hsiung et al. (2023) <!-- cite:hsiung2023compositional --> study robustness to
multiple and to composite perturbations.

**Theory.** Chen et al. (2022) <!-- cite:chen2022understandingdr | read in full
2026-10-10 by Claude, main text and Appendix G --> model domain randomization as
returning the optimal history-dependent policy of a latent MDP, a set of fully
observed MDPs that differ in their transitions, and bound its shortfall against
the optimal policy of the true MDP. Their upper bounds assume that every MDP in
the set is communicating, with bounded diameter. Without that assumption, their
Proposition 1 shows the shortfall can grow linearly in the horizon: the agent
must make an irreversible choice among several branches before anything
distinguishes the candidate MDPs. Theorem 1 here is kin to that construction.
Its two-corridor toy can be read as a two-member latent MDP with an absorbing
failure, so it violates their diameter assumption and lies in the regime of
their Proposition 1. In that regime, Theorem 1 gives the exact optimal value as
a continuous function of how much the environment reveals before commitment,
which perception attenuation controls. It also measures a different gap: the
adaptive optimum against the policy that is optimal when the map is fixed, not
against the optimum for a known environment. Its no-information endpoint is
Proposition 1's uninformed commitment with two branches. Chen et al. therefore
do not subsume Theorem 1, and Theorem 1 does not extend their bounds. For
communication, Pynadath & Tambe (2002) <!-- cite:pynadath2002 --> relate the
complexity of team decision problems with communication to observability. Free
communication lowers the complexity when the world is collectively observable
(their Theorem 4 and Table 2), and communication makes no difference when it is
individually observable or not observable at all (Theorems 5–6). Remark 2′
refines this for collective partial observability: communication's marginal
value vanishes when interchangeable agents' views are redundant, and returns
when roles are irreplaceable or deaths are costly (§7). The survey of
adaptability in multi-agent reinforcement learning by Hu et al. (2025, revised
2026) <!-- cite:hu2025adaptablemarl | the recommendation quoted is in v2 only
--> calls an environment family highly diagnostic if it "systematically varies"
factors such as population, observability or communication structure "while
holding other factors fixed". It mentions compositional generalization but does
not analyse shifts in several factors at once.

**How we searched.** We ran the literature search with the help of LLM-based
research assistants, between August and October 2026. A census of benchmark
venues and a search for theorems that could subsume ours came first; a search of
domain randomization, environment design, multi-task and robust-learning
neighbours followed. Both used web search and the arXiv API and read abstracts.
The works this section describes in detail were then read in full; the
remaining citations rest on their abstracts. We did not query IEEE Xplore.
Wherever this paper says that no work does something, it means no work found by
this search.
````

(Builder check in progress: new Erdem & Üre and Chen et al. claims sent back to the agents that read those papers.)

**Draft 2's findings:** 2 (δ coupling) **resolved**; 3 ("not a variable they
control") **resolved**: "ignition is not an action available to the agents";
4 (VULCAN) **resolved**; 5 (Craftax-Classic) **resolved**; 6 (9× ID)
**resolved** (`N:CA-8`). New claims checked by the agents that read the
papers (`related_work_verification.md` Part 3, follow-up).

**Builder's check findings (the builder's; open):**

1. **The owed reads (your decision).** The comments now credit Claude's
   reads. The 2026-09-26 ruling asks for the owner's full read of Erdem &
   Üre before characterizing it and a read of Chen et al. before "do not
   subsume". A comment cannot change a ruling: either the owner reads them,
   or a new ruling (e.g. "a full read by Claude, recorded in
   `related_work_verification.md` Part 3, discharges the owner-read
   requirement") is transcribed first.
2. **Overreach, Raut paragraph: "ignition … follows only from where they
   choose to stand".** Most collapses happen with no agent present: about
   7.81 per episode from the base rate λ₀ alone, against 7.85–7.92 measured
   under trained policies, so load adds about 1 % (≈ 7 % under random
   policies). CA-9, added today. The fact makes "less directly" stronger, not
   weaker.
3. **Conflict, Erdem & Üre: "it carries the confound our correction
   removes".** The correction removes the empty share, training with no
   active stressor (DES-8, DES-14). Their adversarial arms are attacked at
   every step (the draft's own sentence; Alg. 1), so they have no empty
   share. What they bundle, by the draft's previous sentence, is exposure to
   each modality and budget, which is closer to what ISO-4 leaves in (JOINT
   still sees each coupling 2× as often, DES-14).
4. **Overreach, Erdem & Üre: "an adversary that learns to balance its budget
   … produces agents that also hold up better against single-type attacks".**
   Supported only against the naive hybrid (Table 5, 6 of 6, one tie). No
   table compares it with the single-type-trained arms under single-type
   attacks; only the abstract claims that. "Better" names no comparator.
5. **Minor, Erdem & Üre: "(their Tables 3–4)".** That is the authors'
   reading; each table has an exception.
6. **Overreach, Chen et al.: "lies in the regime of their Proposition 1".**
   Violating Assumption 1 means their upper bounds do not apply. Prop. 1 is
   an existence claim whose Ω(H) comes from per-step reward in absorbing
   states; the toy pays a terminal reward and reveals the corridor with
   positive probability, so Prop. 1 says nothing about its gap. "Can be read
   as" also needs the signals encoded as states (their model has no
   observation channel). "No-information endpoint … with two branches" is
   structurally right (uniform prior), with a different reward structure.
7. **Mechanics:** the Crafter/Craftax comment still says "parked; enter …
   if kept"; both are entered.

*Supported, new in draft 3:* Erdem & Üre's attack at every step (§3.4, Alg.
1), no arm mixing single-type attacks, the mixed arms "more severe"; Chen et
al.'s members differing in transitions, Assumption 1 under every upper bound,
Prop. 1's Ω(H) against the true MDP's optimum, and Theorem 1's different gap
(memorization gap, not the known-environment optimum).

## 2026-10-10 · §2 Related work · draft 4

Owner's draft, verbatim:

````markdown
## 2 Related work

This section says, for each line of work, where it places the hazard and what
its comparisons hold fixed. §1 stated what our comparison holds fixed; how we
searched is described at the end.

**Where the hazard enters learning.** In multi-agent wildfire fighting the
hazard is the objective. Haksar & Schwager (2018) <!-- cite:haksar2018 -->
train aerial agents with a multi-agent deep Q-network and reward them for moving
to burning trees on the fire's boundary (their Algorithm 2); the paper gives the
fire no way to harm them. JaxWildfire (Çakır et al., 2025)
<!-- cite:cakir2025jaxwildfire | read in full 2026-10-10 by an assistant -->, a
JAX cellular-automaton wildfire simulator, trains a single air-tanker agent
whose reward is a per-step penalty proportional to the number of burning cells,
with a bonus for full extinction; the paper does not describe harm to the agent.
Safe reinforcement learning, which García & Fernández (2015)
<!-- cite:garcia2015safe --> define as learning policies that maximize return
while ensuring reasonable system performance and/or respecting safety
constraints, typically places a hazard in a constraint or a cost. VULCAN (Liu &
Yan, 2026) <!-- cite:liu2026vulcan -->, a proposed multi-robot fire
search-and-rescue approach planned by a vision-language model rather than
learned, folds smoke, heat and sensing uncertainty into a hazard cost map; its
preliminary evaluation covers baselines, not the approach itself. Its evaluation
metric is also abbreviated CHE (cumulative hazard exposure), which is unrelated
to our environment's name. In CHE no reward, cost or constraint reads the fire
(Definition 2); the reward prices deaths, whatever their cause.

**A hazard that feeds on itself.** Coupling A lets structural collapse add
ignitions. The nearest neighbour we found is Raut et al. (2026)
<!-- cite:raut2026psps | read in full 2026-10-10 by an assistant -->, who model
public-safety power shutoffs as a single-agent decision problem: the power
flows that follow from the operator's switching decisions set the failure
probability of lines in wildfire areas, which the authors treat as ignition
risk. Their reward is negative operating cost, and there is no spatial spread
model. CHE's agents influence the hazard too, but weakly and indirectly. An
agent standing on a weak cell raises that cell's collapse rate nine-fold
<!-- N:CA-8 --> (Definition 5), but most collapses happen with no agent present:
under trained policies, agents add about one percent to the number of collapses
per episode, and about seven percent under random policies <!-- N:CA-9 -->. A
collapse may then seed fire. So we do not claim that CHE's hazard grows without
agent influence. The difference from Raut et al. is one of directness and size:
there the controlled decision sets the failure probability, while here ignition
is not an action available to the agents, and where they stand moves the
collapse count only slightly.

**Perception degraded by the hazard.** Coupling B attenuates each agent's
observation by Beer–Lambert transmittance along the line of sight through smoke.
VULCAN degrades simulated sensing with smoke density and visibility loss and
infers smoke density from image degradation and depth consistency, but it has
no transmittance model. JaxWildfire's observations are partial and egocentric
but not attenuated. In the search described below, we found no
reinforcement-learning environment whose observation kernel attenuates by
transmittance.

**Simulators and benchmarks in JAX.** CHE follows JaxMARL's environment
conventions (Rutherford et al., 2024) <!-- cite:rutherford2024jaxmarl --> and
trains with independent PPO (de Witt et al., 2020) <!-- cite:dewitt2020ippo -->.
Among the JAX multi-agent benchmarks we surveyed, JaxMARL, Multi-Agent Craftax
(Al Omari et al., 2025) <!-- cite:alomari2025macraftax --> and Assistax
(Hinckeldey et al., 2025) <!-- cite:hinckeldey2025assistax -->, none has an
evolving, spreading lethal hazard field or perception attenuated by a hazard.
Multi-Agent Craftax comes closest in kind: its agents lose health to hunger and
enemies and can die, but its lava is static terrain that agents cannot enter.
In Crafter and in Craftax-Classic, the JAX reimplementation described alongside
Craftax, lava is lethal; and Crafter and Craftax reward each health point
regained and penalize each one lost (Hafner, 2022; Matthews et al., 2024)
<!-- cite:hafner2022crafter --> <!-- cite:matthews2024craftax -->, pricing an
outcome rather than the hazard, much as our reward prices each death. POBAX
(Tao et al., 2025) <!-- cite:tao2025pobax --> is a single-agent suite for
partial observability, and BenchMARL (Bettini et al., 2024)
<!-- cite:bettini2024benchmarl --> is a multi-agent benchmarking library built
on TorchRL rather than JAX. JaxWildfire has a spreading fire in JAX, with one
agent.

**Choosing a training distribution.** Domain randomization trains on a broad,
fixed distribution over simulator parameters so that the deployed setting looks
like one more sample (Tobin et al., 2017) <!-- cite:tobin2017dr -->; Muratore
et al. (2022) <!-- cite:muratore2022drreview --> review the approach.
Unsupervised environment design adapts the distribution to the learner instead.
PAIRED generates environments from a regret objective (Dennis et al., 2020)
<!-- cite:dennis2020paired -->; Prioritized Level Replay revisits levels by
their estimated learning potential (Jiang et al., 2021a)
<!-- cite:jiang2021plr --> and was later recast as environment design (Jiang et
al., 2021b) <!-- cite:jiang2021robustplr -->; and ACCEL evolves levels near
the frontier of the agent's ability (Parker-Holder et al., 2022)
<!-- cite:parkerholder2022accel -->. These methods ask which distribution to
train on, usually adaptively. We compare two fixed distributions and evaluate
no adaptive curriculum (§10). Kirk et al. (2023) <!-- cite:kirk2023zsg -->
survey zero-shot generalization in reinforcement learning, the broader problem
our held-out test belongs to.

**Compositional generalization over environmental factors.** The closest
earlier study of our question is Gao et al. (2024)
<!-- cite:gao2024composition | read in full 2026-10-10 by Claude and by the
owner -->. In visual imitation learning for robotic manipulation, they ask
whether policies compose environmental factors, such as object type and
position, table texture and height, and camera position, to succeed on unseen
combinations, and they use the answer to design data collection. One of their
strategies varies a single factor at a time from a base setting; another cycles
through factors so that more combinations appear. They compare strategies at a
matched number of demonstrations, across levels of a rough effort proxy, the
number of factor changes (their §III-C and §IV-A). Policies do compose, more
weakly when both factors are physical (their §V-B), and the strategy that covers
more combinations does better. Their design is built for data efficiency, not
to separate co-occurrence from how often each factor value appears. Ours matches
compute and, in the ISO-4 correction, the share of training that carries any
stressor. The settings differ too: their factors change what the robot sees and
must do, while two of our stressors are causally coupled to a lethal hazard and
the third is independent of it; their policies are learned by imitation, ours
by multi-agent reinforcement learning. CompoSuite (Mendez et al., 2022)
<!-- cite:mendez2022composuite --> studies compositional multi-task
reinforcement learning over robots, objects, objectives and obstacles, which is
composition of tasks, not of co-occurring stressors. The DBCA method of Keysers
et al. (2020) <!-- cite:keysers2020 --> builds splits whose atom distributions
are similar and whose compound distributions differ. Our secondary sweep follows
that idea, holding each coupling's frequency fixed while co-occurrence varies;
our ISO and JOINT endpoints do not (§1, §9).

**Mixed and simultaneous perturbations.** Robust reinforcement learning asks the
same question about perturbations. Erdem & Üre (2025)
<!-- cite:erdem2025mixed | read in full 2026-10-10 by Claude (publisher's
version of record) --> train single-agent continuous-control policies against a
learned adversary that perturbs observations, actions, or both; in their
formulation the adversary acts at every step (their §3.4 and Algorithm 1). From
their Tables 3–4 they report that agents trained against one modality remain
vulnerable to simultaneous attacks on both. Agents trained against their
balanced mixed adversary also do better under single-type attacks than agents
trained against a naive mixed adversary (their Table 5). No arm in their
comparison trains on a mixture of single-type attacks: each single-type arm
never meets the other modality, and the mixed arms carry the combined budget,
which the authors note is more severe. Because every arm is perturbed
throughout, their design has no counterpart of the fire-only share our
correction removes. What it bundles is how much each arm sees of each modality,
whether it sees them together, and a larger budget. That is nearer to what our
corrected contrast leaves in, where JOINT still sees each coupling twice as
often as ISO-4 <!-- N:DES-14 -->, though unlike ISO-4 their single-type arms
see the other modality not at all. Their result is therefore not a test at
matched per-modality exposure, and it neither supports nor contradicts our
corrected null. Agrawal et al. (2023) <!-- cite:agrawal2023multimodal --> train
multi-agent policies against random reward, state and action noise with a
curriculum that raises the noise level, one or two noise types at a time; the
curriculum sets training length, so exposure differs between their models. In
supervised vision, Tramèr & Boneh (2019) <!-- cite:tramer2019multiple --> and
Hsiung et al. (2023) <!-- cite:hsiung2023compositional --> study robustness to
multiple and to composite perturbations.

**Theory.** Chen et al. (2022) <!-- cite:chen2022understandingdr | read in full
2026-10-10 by Claude, main text and Appendix G --> model domain randomization as
returning the optimal history-dependent policy of a latent MDP, a set of fully
observed MDPs that differ in their transitions, and bound its shortfall against
the optimal policy of the true MDP. Every upper bound they prove assumes that
each MDP in the set is communicating, with bounded diameter. Without that
assumption, their Proposition 1 shows the shortfall can grow linearly in the
horizon: in their construction, per-step rewards follow an irreversible choice
among several branches made before anything distinguishes the candidate MDPs.
Theorem 1 here is kin to that construction but not covered by it. Its
two-corridor toy, with the signals encoded as states, has an absorbing failure,
so their diameter assumption fails and their upper bounds do not apply.
Proposition 1, for its part, says nothing about a toy with a single terminal
reward that can reveal the environment before the branch. Theorem 1 gives that
toy's exact optimal value as a continuous function of how much is revealed
before commitment, which perception attenuation controls. It also measures a
different gap: the adaptive optimum against the policy that is optimal when the
map is fixed, not against the optimum for a known environment. Its
no-information endpoint has the structure of Proposition 1's uninformed
commitment, with two branches. Chen et al. therefore do not subsume Theorem 1,
and Theorem 1 does not extend their bounds. For communication, Pynadath & Tambe
(2002) <!-- cite:pynadath2002 --> relate the complexity of team decision
problems with communication to observability. Free communication lowers the
complexity when the world is collectively observable (their Theorem 4 and
Table 2), and communication makes no difference when it is individually
observable or not observable at all (Theorems 5–6). Remark 2′ refines this for
collective partial observability: communication's marginal value vanishes when
interchangeable agents' views are redundant, and returns when roles are
irreplaceable or deaths are costly (§7). The survey of adaptability in
multi-agent reinforcement learning by Hu et al. (2025, revised 2026)
<!-- cite:hu2025adaptablemarl | the recommendation quoted is in v2 only -->
calls an environment family highly diagnostic if it "systematically varies"
factors such as population, observability or communication structure "while
holding other factors fixed". It mentions compositional generalization but does
not analyse shifts in several factors at once.

**How we searched.** We ran the literature search with the help of LLM-based
research assistants, between August and October 2026. A census of benchmark
venues and a search for theorems that could subsume ours came first; a search of
domain randomization, environment design, multi-task and robust-learning
neighbours followed. Both used web search and the arXiv API and read abstracts.
The works this section describes in detail were then read in full; the
remaining citations rest on their abstracts. We did not query IEEE Xplore.
Wherever this paper says that no work does something, it means no work found by
this search.
````

**Draft 3's findings:** 2 (collapse "only from where they stand")
**resolved** (CA-8, CA-9); 3 (Erdem & Üre's confound) **resolved**: "no
counterpart of the fire-only share our correction removes", "nearer to what
our corrected contrast leaves in"; 4 ("hold up better") **resolved**: "than
agents trained against a naive mixed adversary (their Table 5)"; 5 (Tables
3–4) **resolved**: "they report"; 6 (Chen's regime) **resolved**: upper bounds
do not apply; Prop. 1 "says nothing about" the toy; signals encoded as
states; 7 (stale comment) **resolved**.

**Builder's check findings (the builder's; open):**

1. **The owed reads (your decision, unchanged).** The comments credit
   Claude's reads; the 2026-09-26 ruling asks for yours (Erdem & Üre before
   characterizing; Chen et al. before "do not subsume"). Read them, or rule
   that the recorded full reads discharge it, transcribed first.
2. **Minor, Erdem & Üre: "Because every arm is perturbed throughout".** Their
   Non-Robust baseline is plain PPO with no attack, and NA-PPO's noise
   schedule is unspecified; it is the adversarial arms that are attacked at
   every step.
3. **Minor, numbers: "about seven percent under random policies"** (CA-9).
   Read as what agents *add to* the no-agent count it is 7.4–8.3 %; as a
   share of all collapses it is 6.9–7.6 %. The trained figure is 0.4–1.4 %
   either way. Scope: "trained" is the m35 Phase-3 policies (500 updates,
   single configurations), not the Phase-6 policies. CA-9's note now gives
   both forms.

Everything else in draft 4 is clean against the record and the full-text
checks.

## 2026-10-10 · §2 Related work · called done

The owner's final text is draft 4, verbatim, now in `paper/finale.md` after
§1, with the owner's comments and IDs; nothing added. Finding 1 **resolved by
ruling** (READS RULING: the recorded full reads discharge the owner reads;
the owner will still read and review personally). Findings 2 ("every arm")
and 3 ("about seven percent") **left as written**, the owner's call.
