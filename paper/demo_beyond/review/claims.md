# Claims review — demonstration draft (keeper, 2026-10-11)

Scope: overreach, undersell, conflict (with a ruling, a registered reading,
or the owner's abstract / §1 / §2), missing (a required honesty line or
registered string), cross-section inconsistency, and length where it hurts
the reader. Numbers against their rows, and kit mechanics, belong to the
NUMBERS and MECHANICS auditors and are not repeated here. Every section file
was read in full; line numbers are each file's own (`sections/NN_*.md:line`).
Fix directions are for the builders; nothing here edits a section file.

**Severity:** MUST = a claim the record contradicts, or a registration status
misstated; SHOULD = overreach or scope loss a reviewer would catch, or length
that repeats results; NOTE = precision, or an adjudicated sentence that
stands. Category "adjudicated" = a sentence flagged by its writer or the
coordinator that the record supports (kept, sometimes with a wording note).

Source shorthand: `R/` = `che/bench/results/`; `P6/` = `R/phase6/`; `TF` =
`docs/theory_foundations.md`; `log` = `docs/decision_log.md`.

**Keeper correction made this session.** My brief (§A7) and the supplement's
DX-9 note said the E1.1 prediction was registered before the trained-policy
measurement. That was wrong: E1.1's own CORRECTION (`R/e1/e11_report.md:170-197`)
records that the trained-policy ordering and its fuel-exhaustion cause were
already on record in Phase-4 Result 4 and M3.5. Both files are corrected.
W3 caught it; W1 followed my wrong brief (C-1).

---

## Adjudications asked for

1. **"Predicted before measurement" (CA-4).** What the record supports: the
   fuel limitation was **first measured at the random-policy calibration**
   (High seeded ignitions ≈ 5.7× below Low at every κ_A, `coupling_a_lock.md:45-55`)
   and **recorded as "fuel-exhaustion self-limitation of the ignition
   channel" at the human lock of 2026-07-21** (`coupling_a_lock.md:75-90`),
   before any trained policy was measured (M3.5 ran on the locked parameters,
   `R/phase3/phase3_report.md:153-157`; M4.4 later). The E1.1 three-part
   prediction was registered before *E1.1's* analysis (`e11_report.md:15-21`)
   but **after** the trained results existed (`e11_report.md:170-197`: "the
   prediction was already answerable from Result 4 before E1 began").
   **Ruling for the demo:** §1 and §5 say "recorded at the Coupling-A lock,
   from the random-policy calibration, before any trained policy was
   measured"; neither says "registered before that measurement". §5:78 is
   right in substance (C-14); §1:44 must change (C-1). The owner's abstract
   overreaches mildly: OWNER ITEM O-1.
2. **Prop. 1's finiteness.** Since the 2026-10-10 C11 amendment (log:5939-5955),
   Def. 1 puts ρ ∈ ℝ≥0^G in the state (`TF:38-44, :53-54`), but the proof
   still says "$\mathcal{S}$, $\mathcal{A}$ and $\Omega_i$ are finite"
   (`TF:151-153`). That is false of $\mathcal{S}$ as defined, and of $\Omega_i$,
   whose smoke plane is real-valued. It is true of the **reachable** states
   and observations within the horizon: every stochastic factor and the reset
   have finite support (Bernoulli, categorical and integer draws), and ρ
   evolves deterministically from ρ₀ = 0. **Ruling for the demo:** W2's §3
   argument (`03_environment.md:32`) is the correct one. App. A
   (`12_appendix.md:11`) adopts it, with a one-line note that the theory
   document's finiteness sentence predates the ρ amendment (C-8, C-32).
   `HANDOFF.md:213` still lists "the theory-doc ρ amendment" as open, though
   C11 applied it. OWNER ITEM O-2.
3. **§2's two departures from owner wording.** Both demo versions are accurate
   and are kept (C-6, C-7). Recorded: the owner left both as written
   (READS RULING item 2, log:5760-5765; finding at `paper/writing_drafts.md:2042-2050`).
   OWNER ITEMS O-3 and O-4.
4. **W4's three items.**
   - The "0.11 agents" sentence is an exact identity: deaths = 12 × (1 −
     survival rate), since no agent revives (`che/env/env.py:446`;
     `test_lethality.py:203`). It is kept, labelled descriptive (C-24).
   - "nothing detectable is left on survival for composition to explain"
     overreaches (C-23).
   - Γ₄′ is a **secondary (S5)** analysis, not part of the sensitivity arm
     (C-22).
5. **M5.3's floor.** W3's "hard-coded from an earlier run" is what the record
   shows. CLAUDE.md's "different hardware" is not (C-19). OWNER ITEM O-5.
6. **The least-sure sentences.** Each is addressed by the row named:

   | sentence | row | outcome |
   |---|---|---|
   | §1:44 | C-1 | fix |
   | §1:37 | C-5 | keep |
   | §2:31 | C-7 | keep |
   | §4:25 | C-13 | keep, with a qualifier |
   | §3:143 | C-9 | keep, with wording |
   | §3:222 | C-11 | keep |
   | §5:76 | C-15 | fix |
   | §7:60 | C-17 | keep |
   | §6:79 | C-16 | fix scope |
   | §9:116 | C-27 | keep |

7. **Length.** C-3, C-12, C-28, C-29, C-31 and C-34 name the passages to cut.
   About 2,500 words could go with no claim lost.

---

## `sections/00_hero.md`

No claims findings. The caption says "No outcome is reported" and keeps
perception (the panels) apart from the state (the map), as DESIGN.md §4 F1
requires.

## `sections/01_introduction.md`

| id | file:line | category | severity | the phrase, quoted | why, with the rule or source | fix direction |
|---|---|---|---|---|---|---|
| C-1 | 01:44 | overreach; cross-section (§5:78) | MUST | "fall 4.8-fold … from low to high severity, as registered before that measurement" | The E1.1 registration came after the trained results (`R/e1/e11_report.md:170-197`). What predates the trained measurement is the calibration record and the lock (`coupling_a_lock.md:45-55, :75-90`). It also contradicts §5:78. Adjudication 1 | "…fall 4.8-fold, as the Coupling-A lock had recorded from the random-policy calibration before any trained policy was measured (§5), while their share near agents stays flat" |
| C-2 | 01:37 | undersell | NOTE | (absent) the same-card replicate | Γ₄′ = +0.13 [−0.56, +0.81] (RES-8) shows the correction does not rest on a cross-card contrast (`paper/branch_B.md:41-42`). The owner's abstract also omits it | optional clause after the Γ₄ sentence: "a same-card replicate, proposed after Γ₄ was seen, agrees (§9.2)" |
| C-3 | 01:35-37 | length | SHOULD | the two result paragraphs | §1 is ≈ 2,080 words against the 900–1,200 target. OPENING AND §1 REOPENED item 3 asks for "shorter", carried by Figures 2–3. Fig. 3 and §9.2 already carry the falsifier arithmetic (3.855 / 4.433), the "11 registered checkpoints from update 500 to 1000" detail and the completion Γ₄ clause | keep every verdict string and the two limits; cut the falsifier numbers ("the registered falsifier passes", §9.2), the checkpoint detail and the completion-Γ₄ clause (Fig. 3 shows it); trim the four dates at 01:22 to the 2026-08-13 registration |
| C-4 | 01:7 | overreach (scope) | NOTE | "Proposition 1 shows … CHE is a finite Dec-POMDP" | true on the reachable states only (adjudication 2). The owner's §1 says the same (`paper/finale.md:51-52`) | leave as the owner's claim, or add "on its reachable states"; must match §3:32 |
| C-5 | 01:37 | adjudicated | NOTE | "Once the active share is matched, JOINT's remaining differences add nothing detectable to survival, although it still sees each coupling twice as often…" | the owner's own sentence (`paper/finale.md:129-132`), placed after both limits (+0.63 > +0.47; two quantities change). It does not overreach in that position | keep |

## `sections/02_related_work.md`

| id | file:line | category | severity | the phrase, quoted | why, with the rule or source | fix direction |
|---|---|---|---|---|---|---|
| C-6 | 02:21 | adjudicated (departs from owner) | NOTE | "agent load adds only 0.4–1.4 % … and 7.4–8.3 % under random policies" | exact, in the increase reading the sentence uses (CA-9). The owner's "about seven percent" fits only the share reading (log:5760-5765) | keep the demo version; OWNER ITEM O-4 |
| C-7 | 02:31 | adjudicated (departs from owner) | NOTE | "Every adversarially trained arm is perturbed throughout" | the Non-Robust baseline is unattacked; the adversarial arms are attacked at every step (`paper/writing_drafts.md:2042-2045`; log:5760-5762). The demo is accurate and keeps the owner's point (no fire-only counterpart) | keep; OWNER ITEM O-3 |

## `sections/03_environment.md`

| id | file:line | category | severity | the phrase, quoted | why, with the rule or source | fix direction |
|---|---|---|---|---|---|---|
| C-8 | 03:32 | cross-section (vs 12:11) | MUST | "the states and observations reachable within the horizon form finite sets" | correct, and it departs knowingly from `TF:151-153` (adjudication 2). App. A typesets the false version, so the paper proves Prop. 1 twice with different finiteness claims | keep §3. Fix App. A (C-32). Add to §3 one clause naming why ("ρ ∈ ℝ≥0^G is not a finite set") |
| C-9 | 03:143 | adjudicated | NOTE | "Fire and collapse affect return only through the dynamics: the transition kernel … and the observation kernel…" | supported: `TF:97-101`; `che/env/env.py:159-196`; the fire never touches food (`che/env/tasks.py:31-43`). "Dynamics" for the observation kernel is loose | "…only through the transition and observation kernels, never through the reward" |
| C-10 | 03:186 | overreach (factual slip) | NOTE | "the per-episode mixture draw each use a stream derived from the step key by a fixed tag" | the mixture draw folds the **reset** key (`che/env/env.py:221`) | "derived from the reset or step key" |
| C-11 | 03:222 | adjudicated | NOTE | "These tests run in the CPU suite; the digest is checked on the CPU only…" | `che/tests/test_comms.py:280-288` (skip off CPU; "smoke exponential is not bit-identical across backends") | keep: it scopes "bitwise" correctly |
| C-12 | 03:125; 05:56; 06:9; 06:47 | length (repetition) | SHOULD | the three-stressor preview with locked values (03:125); the unconditional-draw rule explained again (05:56, 06:47); the smoke update restated (06:9) | §3.4 (03:186) already gives the rule, §§5–7 give the definitions, and §3.2 gives the smoke update | 03:125 to one sentence with pointers; 05:56 and 06:47 to one sentence each citing §3.4; 06:9 refer to §3.2 for ρ′ |

## `sections/04_severity.md`

| id | file:line | category | severity | the phrase, quoted | why, with the rule or source | fix direction |
|---|---|---|---|---|---|---|
| C-13 | 04:25 | adjudicated | NOTE | "CHE's fire is the idealized kernel on a finite arena" | supported by the code: von Neumann neighbours, burn time one step, homogeneous fuel, no wind, ι = 0 (DX-1), non-wrapping boundary (`che/env/hazard.py:29-64`). None of Cor. 1's listed departures applies (`TF:227-233`). The theory doc had expected a non-idealized port (`TF:266`), which is why it reads oddly | keep; qualify "the fire kernel on its own (Coupling A adds ignitions; §3.2)" |

## `sections/05_coupling_a.md`

| id | file:line | category | severity | the phrase, quoted | why, with the rule or source | fix direction |
|---|---|---|---|---|---|---|
| C-14 | 05:78 | adjudicated | NOTE | "The fall was predicted before trained policies were measured. It was first recorded at the random-policy calibration … A later prediction … (its answer was already on record…)" | matches the record (adjudication 1). "Predicted" is a little strong for a calibration-stage measurement | keep; optionally "anticipated", and cite the lock's ruling date 2026-07-21 (`coupling_a_lock.md:75-90`). §1 must match this paragraph |
| C-15 | 05:76 | overreach | SHOULD | "With Proposition 3 this places Coupling A's leverage below and near criticality: it matters most where the fire is otherwise rare" | true of the **ignition channel** (`coupling_a_lock.md:82-90`). Not shown for outcomes: M3.5's κ_A survival contrasts are −0.018 / −0.017 / −0.034 at Low / Medium / High, largest at High (`R/phase3/phase3_report.md:184, :192, :200`; 2 seeds, unfloored) | "places the ignition channel's leverage …"; add that the M3.5 survival contrasts (2 seeds) do not locate it |

## `sections/06_coupling_b.md`

| id | file:line | category | severity | the phrase, quoted | why, with the rule or source | fix direction |
|---|---|---|---|---|---|---|
| C-16 | 06:79 | overreach (scope) | SHOULD | "the masking ceiling of the states the policies visited … sat at or above its random-policy value at every severity" | true of the κ_B = 1.0 arm only. The κ_B = 0 arm sits below at Low and Medium (0.0258 < 0.0279; 0.1016 < 0.1278; `R/phase4/phase4_report.md:388-392`). The report's own sentence (:394-395) is ambiguous. The 500-update scope is right | "the coupled (κ_B = 1.0) policies' masking ceiling … sat at or above…" |

## `sections/07_comms.md`

| id | file:line | category | severity | the phrase, quoted | why, with the rule or source | fix direction |
|---|---|---|---|---|---|---|
| C-17 | 07:60 | adjudicated | NOTE | "That signal needs no encoder, and it went unused…" | log:1076-1081 (M5.3 CLOSURE RULING); `R/phase5/phase5_report.md:1030-1034`; `comms_lock.md:42-50` | keep |
| C-18 | 07:54 | overreach (scope) | NOTE | "CHE's agents resemble the case of Remark 2′(i)… except that their deaths are priced" | Remark 2′(i) also needs agents "at least as numerous as the hypotheses" (`TF:493-496`), which nothing establishes for CHE | add "and nothing establishes the remark's numerosity qualifier for CHE", or drop "resemble" |

## `sections/08_methodology.md`

| id | file:line | category | severity | the phrase, quoted | why, with the rule or source | fix direction |
|---|---|---|---|---|---|---|
| C-19 | 08:18 | adjudicated | NOTE | "M5.3 graded its content ablation against a Medium floor hard-coded from an earlier run" | supported (`R/phase5/phase5_report.md:831`; log:950). M5.1e and M5.3 both ran on an RTX 5090 (`R/phase5/m51e/provenance.txt:6`; `R/phase5/m53/provenance.txt:7`; `phase5_report.md:361`) | keep; OWNER ITEM O-5 |
| C-20 | 08:44 | overreach (unsourced) | NOTE | "nothing known before the measurement said which arm would be noisier" | the record has only the ruling's "Do not presume its outcome" (`P6/m62b/m62b_report.md:128-129`) | "the ruling that ordered the measurement said not to presume its outcome" |
| C-21 | 08:5 | overreach (overgeneralization) | NOTE | "so two runs with the same seed, configuration and code differ" | they **can** differ (`R/phase4/phase4_report.md:637-639`). The reference tree's reruns were identical 4 of 4 (METH-2) | "can differ" |

## `sections/09_compositional_test.md`

| id | file:line | category | severity | the phrase, quoted | why, with the rule or source | fix direction |
|---|---|---|---|---|---|---|
| C-22 | 09:72 (also 09:86) | conflict (registration status) | MUST | "sensitivity arm, outside the confirmatory family, for Γ₄, Γ₄′ and B̂" | Γ₄′ is the secondary instrument's S5, proposed 2026-09-26 **after Γ₄ was seen** (log:5043-5051, :5058-5065; `P6/secondary/secondary.md:5, :55`; DES-15). It is not part of the sensitivity arm registered 2026-09-18. B̂ has no registered test (FIGURE BATCH B7). The §9.1 table (09:58) already says "secondary, at z_α" | Fig. 11 note: "sensitivity arm, outside the confirmatory family, for Γ₄; secondary (S5), non-verdict-bearing, read at z_α, for Γ₄′; no registered test for B̂". Table 09:86 status: add "secondary (S5)" |
| C-23 | 09:139 | overreach | SHOULD | "nothing detectable is left on survival for composition to explain" | Γ₄ is an exclusion, not an absence: its upper bound +0.63 lies above Γ's lower bound +0.47 (RES-6, RES-2; `paper/branch_B.md:227-228`; 09:101 itself). JOINT − ISO-4 bundles 2× per-coupling frequency with co-occurrence, so "composition" is not the only remainder | "…JOINT's remaining differences, twice the per-coupling frequency and full co-occurrence, add nothing detectable to survival (an exclusion; a composition effect up to +0.63 points is not ruled out)" |
| C-24 | 09:131 | adjudicated | NOTE | "the survival gap, expressed in agents, is of the same size, about 0.11 agents per episode" | exact identity: deaths = 12 × (1 − survival rate) (`che/env/env.py:446`; no revival, `che/tests/test_lethality.py:203`), so 12 × 0.0096 ≈ 0.115 against 0.1177 fewer fire deaths. Both channels are out of family and unfloored | keep, labelled "by that identity; descriptive, grades nothing"; avoid causal verbs |
| C-25 | 09:15 | cross-section | NOTE | "both couplings moved survival while their completion effects sat at or below the reproducibility floor (§5, §6)" | this is the registration's rationale (`phase6_framing_branches.md:149-155`). §5 reports no completion effect at all, and M3.5 predates every floor | attribute it ("as the registration records"); drop "§5" or add the M3.5 completion line to §5 |
| C-26 | 09:47; 09:129 | missing (scope) | NOTE | sweep ↔ JOINT extrapolation | the sweep's both-coupling components carry δ = 0 (`che/configs/p6_sweep_c50_p250.yaml:38, :42`); JOINT's carry δ = 1.0 (`p6_joint.yaml:36-37`). Harmless only under the δ-inert reading | one clause: "(JOINT also differs in δ, inert under this encoder at this scale, §7)" |
| C-27 | 09:116 | adjudicated | NOTE | "This says only that the drift has not visibly reversed…" | the registered permitted use (App. D item 6; §7 PROPOSALS RULING, proposal 2). Both later slopes are positive (DX-23) | keep |
| C-28 | 09:72; 09:81-101; 09:53-62; 09:129; 09:64 | length | SHOULD | Fig. 11 caption (≈ 260 words); the results table and then the same estimates and CIs again in 09:91-99; the §9.1 readings table; 09:129's survival estimates; the blinding paragraph | the Fig. 11 caption repeats every verdict the table under it gives. The prose repeats every CI in the table. The readings table duplicates App. D. 09:129 duplicates App. I's table. Blinding is repeated in §11:13 and App. F | Fig. 11 caption: identity of rows and marks, plus what it cannot show. Prose: verdict sentences only, CIs by reference to the table. §9.1 table: cut, or keep three rows. 09:129: keep only the two predictions against measured contrasts and the tension sentence. Keep blinding here and cut §11:13 (C-31) |

## `sections/10_limitations.md`

| id | file:line | category | severity | the phrase, quoted | why, with the rule or source | fix direction |
|---|---|---|---|---|---|---|
| C-29 | 10:20-22 | length | NOTE | "The correction's own limits"; "Matched compute only"; "Completion is unresolved" | each restates numbers stated in §1 and §9.2. Required in substance (spine §10), not with every number | keep the bullets; replace the numbers with pointers to §9.2 |

All ten spine items (`paper/00_common_spine.md:563-605`) are present, in
order, with the Medium-siting limitation and the struck line (honesty line 5).

## `sections/11_reproducibility.md`

| id | file:line | category | severity | the phrase, quoted | why, with the rule or source | fix direction |
|---|---|---|---|---|---|---|
| C-30 | 11:7 | overreach (stated reason) | NOTE | "That is why the tests of §9 are graded on each arm's own seed dispersion" | the record's reason is that the floor and the test statistic are different variances (`CLAUDE.md`, contrasts amendment, corollary). Nondeterminism is why floors are measured | "That is why floors are measured; the tests of §9 use each arm's seed dispersion because a k-seed mean varies by seed as well (§8.4)" |
| C-31 | 11:13 | length | NOTE | "One look per stage…" | duplicates 09:64 | one sentence with a pointer to §9.1 |

## `sections/12_appendix.md`

| id | file:line | category | severity | the phrase, quoted | why, with the rule or source | fix direction |
|---|---|---|---|---|---|---|
| C-32 | 12:11 | cross-section (vs 03:32) | MUST | "$\mathcal{S}$, $\mathcal{A} = \prod_i \mathcal{A}_i$ and $\Omega_i$ are finite, so $\mathcal{M}_\theta$ is a finite Dec-POMDP" | faithful to `TF:151-153`, but false since the C11 amendment (`TF:38-44, :53-54`; log:5939-5955), and it contradicts §3:32 | use §3's reachable-set argument, plus a dated note: "the formal specification's proof states $\mathcal{S}$ finite; with ρ ∈ ℝ≥0^G this holds for the reachable states" |
| C-33 | 12:29 | conflict (registered trap: two runs) | SHOULD | "Empirically (M3.3, at L = 32<!-- N:CA-3 --> and L = 64…)" | M3.3's L = 32 run is the first slow test (v1, ratio 1.025; `R/phase3/phase3_report.md:95-101`), not CA-3's v2 purified handshake (κ_A 0.003, ratio 0.992; :131-147). The tag merges two runs | drop the CA-3 tag, and say "M3.3's L = 32 and L = 64 analyses"; no new number is needed |
| C-34 | 12:19-25; 12:31-41; 12:51-61; 12:126; 12:207 | length | SHOULD | the full restatements of Prop. 3, Thm. 1 and Remark 2′; the App. C ratios paragraph; the App. E branch reading | §5, §6 and §7 already state these. 12:126 repeats §8.4 and §9.2. 12:207 repeats §9.2. The appendix is ≈ 6,300 words | statements → "Statement: §5 (Proposition 3)" and so on, keeping the proofs; keep only Remark 2′'s lowest-depth asymptotic sentence (12:61), which §7 lacks; cut 12:126 to its first sentence; 12:207 to one line |

---

## OWNER ITEMS (the demo edits none of these)

- **O-1 (abstract, `paper/finale.md:13`; §1 contribution 2, `:159-160`).**
  "As predicted before measurement" overreaches mildly. The self-limitation
  was first *measured* under a random policy at calibration (≈ 5.7×,
  `coupling_a_lock.md:45-55`) and recorded at the 2026-07-21 lock
  (`:75-90`) before any trained policy ran. It was not predicted before any
  measurement, and the formal E1.1 prediction came after the trained results
  (`R/e1/e11_report.md:170-197`). What the record supports: "as recorded at
  calibration, before any trained policy was measured".
- **O-2 (theory doc and §1).** `docs/theory_foundations.md:151-153` (Prop. 1
  proof) says S and Ω_i are finite. The 2026-10-10 amendment made
  ρ ∈ ℝ≥0^G a state component (`:38-44, :53-54`). A dated amendment is owed:
  "finite on the states reachable within the horizon".
  - The same doc's observation-kernel line (`:62-63`) is still unprimed and
    omits ρ.
  - The owner's §1 "finite Dec-POMDP" (`paper/finale.md:51-52`) inherits the
    finiteness issue.
  - `HANDOFF.md:213` still lists the ρ amendment as open; C11 applied it
    (log:5939-5955).
- **O-3 (§2, `paper/finale.md:310-311`).** "every arm is perturbed throughout"
  is inaccurate: Erdem & Üre's Non-Robust baseline is unattacked
  (`paper/writing_drafts.md:2042-2045`). The owner left it knowingly (READS
  RULING item 2, log:5760-5762). The demo's "every adversarially trained arm"
  is accurate.
- **O-4 (§2, `paper/finale.md:217-218`).** "agents add … about seven percent
  under random policies". As an increase, which is what "add" says, CA-9 gives
  7.4–8.3 %; "about seven" fits only the share reading (6.9–7.6 %).
  Recorded at log:5762-5764. Minor.
- **O-5 (`CLAUDE.md:344`; log:1194).** "M5.3's hardcoded Medium floor applied
  to a run on different hardware / a different card" is not what the
  provenance shows:
  - M5.1e and M5.3 both ran on an RTX 5090 (`R/phase5/m51e/provenance.txt:6`;
    `R/phase5/m53/provenance.txt:7`); `phase5_report.md:361` says "M5.3 stays
    closed on the 5090". Whether it was the same physical unit is not
    recorded.
  - The recorded defect is that the floor was a hard-coded constant, Medium-
    and card-specific (`phase5_report.md:831`; log:950). Its danger was reuse
    at High on another card (M5.3b).
  - Nobody edits CLAUDE.md; the owner decides.
- **O-6 (reports, for awareness; nothing is edited).**
  - `R/phase4/phase4_report.md:366`'s "a sixth to a quarter" of the crop
    contradicts its own table (0.081 / 0.056 at Low / Medium).
  - `:394-395`'s "at or above the random-policy ceiling at every severity"
    holds for the κ_B = 1.0 arm only. That bears on the scope of the
    "not behaviourally suppressible" headline (`:647-648`).

---

## Fix-round re-check

Keeper, 2026-10-11. Scope: the `+` lines of `review/fix_round.diff` only, read
against `DECISIONS.md` and `resolutions_W1–W4.md`. Line numbers are the
post-fix files'.

**Tally.** C-items: 34 of 34 pass. 25 were fixed in the adjudicated direction,
and the 9 adjudicated keeps were kept. Every MUST is closed:
- C-1: §1:44 now matches §5:80.
- C-8 and C-32: §3:32 and App. A 12:11-13 now use one reachable-set argument,
  and App. A notes the departure from the theory document.
- C-22: the Fig. 11 status (09:69), the table row (09:83), 09:59 and 09:94 now
  call Γ₄′ "secondary (S5)".

The three agreement checks (CA-4 timing, Prop. 1, Fig. 11 status labels) pass.
`+` lines checked: 223. Non-OK: 5, of which 0 MUST, 1 SHOULD and 4 NOTE; they
are listed below.

**Checked and OK (not findings):**
- "Smoke costs survival at high severity" (01:44) is the owner's wording
  (`paper/finale.md:163-165`).
- "was still rising at T\*" (09:111) is recorded as a description at
  log:5174-5176.
- "saturates before JOINT" (09:136) comes from `paper/branch_B.md:79` and
  spine :554.
- "Γ₄ and Γ₄′ contradict it" (10:7) comes from `branch_B.md:181`.
- "at High A is marginal by construction" (09:130, 10:7) is the §7 PROPOSALS
  RULING's wording (spine :570-572), and each sentence scopes it to seeded
  ignitions.
- "rules out 'nobody was in range'" (07:56) matches `R/phase5/phase5_report.md:902-906`.

| id | file:line | category | severity | the phrase, quoted | why, with the rule or source | fix direction |
|---|---|---|---|---|---|---|
| C-R1 | 07:56; 07:58 | overreach; conflict (§8.2:40, CLAUDE.md power rule) | SHOULD | "the null excludes effects larger than about 3 points"; "limits that null to effects larger than about 11 points"; "removing the channel changes completion by no more than about 8 points, survival by no more than about 2.6 points, and danger-moment outcomes by no more than about 27 % relative" | Each bound is a 2σ bar (2 × the floor sd). §8.2:40 says such a bar is "the effect at which a test would just reject, 50 % power". The 2σ form is allowed only for post-hoc floor grading of an observed effect (CLAUDE.md, 2026-08-02), so it cannot be restated as an exclusion. The 27 % bound is taken from the condition that the next sentence calls VOID, and a void instrument's output is not evidence (bars-with-floors rule). The wording is the record's (`comms_lock.md:37-39`; `R/phase5/phase5_report.md:912-914, :1024-1027`), and it predates the power rule. I missed it in round 1; it sits on a `+` line now | Keep the record's own scope: "inert at the resolution these measurements have … not a point null" (`phase5_report.md:1024-1027`). State each bound as a bar: "no difference reached its bar (about 3 points at M5.3, about 11 at M5.3b; 7.99 and 2.60 points at M5.5), a post-hoc floor grading that a true effect equal to the bar would clear only about half the time (§8.2)". Drop the 27 % bound, or say the VOID condition bounds nothing |
| C-R2 | 05:80 (also 01:44) | overreach (wording) | NOTE | "The fall was recorded before any trained policy was measured" | The trained 4.83-fold fall could not be recorded before trained policies existed. The lock recorded the fuel-exhaustion self-limitation, seen as a ≈ 5.7× fall under random policies (`coupling_a_lock.md:47-50, :82-85`). §1:44's "as the Coupling-A lock had recorded" reads acceptably. Separately, W3's reason for skipping C-14's optional date ("no ledger row") is mistaken: DX-401 carries the 2026-07-21 Coupling-A ruling date (`ledger_supplement.md:84`), and 12:48 already uses it | "The fuel limitation was recorded before any trained policy was measured: …". Optionally add "(2026-07-21<!-- N:DX-401 -->)" |
| C-R3 | 03:32; 12:11 | overreach (logic gap) | NOTE | "Optimal finite-horizon joint policies of a finite Dec-POMDP exist by the standard argument" (03:32); "follows by the standard argument for finite Dec-POMDPs" (12:11) | Each proof has just said that $\mathcal{S}$ is not finite, then applies the finite-model argument without naming the restriction it applies to. The two files agree with each other (check 3 passes); the gap is shared | Use the same words in both files: "…form finite sets; restricted to them, $\mathcal{M}_\theta$ is a finite Dec-POMDP, so optimal finite-horizon joint policies exist by the standard argument" |
| C-R4 | 09:69 (status for B̂) | undersell; keeper self-correction (C-22) | NOTE | "no registered test for B̂" | The B̂ part of C-22 was too strict. The 2026-09-18 ruling registers B̂ = ISO-4 − ISO as the sensitivity arm's bias estimate (log:4011-4012), to be "reported side by side on every branch, with B̂ and its CI" (log:4018), with "No magnitude threshold on B̂" (log:4029). The label is still true, and 09:56 (B̂ in the 2026-09-18 row) and 09:96 are right; the label just reads as if B̂ were unregistered | Optional: "B̂: registered estimand (2026-09-18), reported with its CI, no test" |
| C-R5 | `review/DECISIONS.md:45-46` (item 9) | conflict (process) | NOTE | "a number that has no row is cut rather than given one now" | It conflicts with the ledger rule that a new number "gets its row first" (`paper/numbers_ledger.md:12`; CLAUDE.md:134). It was also not followed: W3 and W4 added seven rows this round (DX-305, DX-306, DX-412 to DX-416), while W3 cut a date under the same item (C-R2) | Reword: "a number with no row gets a VERIFIED row first, or is cut". The rows the writers added stand if they are verified; that check belongs to the NUMBERS lane |

I disagree with no other DECISIONS item. Items 3 and 4 follow adjudications
1 and 2, and item 5 follows C-7.
