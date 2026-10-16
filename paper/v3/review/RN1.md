# RN1 — numbers review, part 1 (Paper v3, step 4.2)

Reviewer lane RN1, 2026-10-14. Read-only for everything except this file.

## Summary

- **Counts:** MUST 0, SHOULD 7, OWNER 0.
- **MUST items:** none. Every tag in scope resolves, every tagged value matches its row (rounding and units included), and every arithmetic step in the new W2 rows re-computes.
- **The SHOULD items are of three kinds.**
  - Scope or rounding notes that v3 dropped from sentences carried from v2: RN1-1 (ENV-2–5), RN1-2 (CA-4).
  - Wording around carried numbers that drifts past what the row says: RN1-3 (CB-9), RN1-4 (RES-12), RN1-5 (V5-1).
  - Small gaps: a few untagged numbers (RN1-6) and one row note (RN1-7).

**Scope:**
- `snapshots/draft1/sections/` files `00_abstract.md`, `00_hero.md`, `01_introduction.md`, `02_related_work.md`, `03_environment.md`, `04_calibration.md`, `05_measurement.md`, `12_conclusion.md`, `13_appendix_proofs.md` and both alternates (`alt/13_appendix_proofs.thm1_tf.md`, `alt/13_appendix_proofs.no_prop4.md`), `14_appendix_locks.md`, `15_appendix_floors.md`;
- `paper/v3/front_matter.yaml`;
- the new rows in `ledger_proposals/W2.md`. `W1.md` and `W3.md` do not exist: W1 and W3 wrote no rows, and every number in their files resolves to an existing row.

The snapshot is byte-identical to `paper/v3/sections/` and `paper/v3/provenance/` (`diff -rq`, both empty).

**Method:**

1. **Read first.** I read the preamble's binding inputs: `paper_v3_prompt.md` in full; `docs/decision_log.md` from PAPER V2 to the end; `BRIEF.md` in full; `STRUCTURE.md` §1–§3; `WRITERS.md`; the planner notes.
2. **Resolved every tag.** I indexed every row ID in `paper/numbers_ledger.md`, `paper/v2/ledger_supplement.md`, `paper/v2/ledger_proposals/*.md` and `paper/v3/ledger_proposals/*.md`. That is 198 IDs, with no ID defined twice. I then extracted all 322 `<!-- N:ID -->` tag instances in scope, and all 322 resolve.
3. **Read each tagged number beside its row**, in sentence context, checking value, rounding, points against fractions, and agents per episode against rates. Where a sentence was new or edited in v3 (per `provenance/*.md` and by grepping v2's sentence), I compared it with v2's wording to see whether the claim around the number moved.
4. **Scanned for untagged numbers**, both digits and number words, after stripping comments, code and math.
5. **Re-read every W2 row's source at HEAD** (`git show HEAD:<path>`), and re-ran all W2 arithmetic in Python: X2-2 at all seven κ_B > 0; X2-3; X2-4; the Def. 6 cross-check.
6. **Re-read X4-3's sources at HEAD** (W4's row, cited in W1's files): `unblind.json:55, :61`; `p6_joint.yaml:12`; `env.py:443-446`; `test_lethality.py:202-203`. 0.009553128646479725 × 12 = 0.11464.

**Commit status:**
- Every W2 source is committed and clean against HEAD (`git status` is empty on `che/bench/results/phase4/`, `che/env/`, `che/tests/test_coupling_b.py` and `docs/theory_foundations.md`).
- The working tree's uncommitted `docs/locks.yaml` edit is purely additive, at line 527 onward (`git diff --stat`: 61 insertions). Every ledger row in scope cites `locks.yaml` lines ≤ 462, so no cited line moved.
- No tag in scope cites a PENDING row (IC-*, X5-*).

**Not re-opened (carried from v2 and verified there):**
- "Šidák-corrected 95 %" tagged DES-13: the row gives m = 2 and z_α, not "95"; it is v2's tag at v2 `00_abstract.md:26`.
- The 0.03 effect in §C's contrast-SE bullet, tagged DES-4: the value is at `m62b_report.md:173`, and the tag is v2's at v2 `08_methodology.md:47`.
- Proposition 3's "neither at the locked parameters": v2 `05_coupling_a.md:90`.

---

## Findings

### RN1-1 — SHOULD — the d_p ablation lost its "training-log means" scope

- **Location:** `sections/03_environment.md:187`.
- **What is wrong:** The ablation numbers (0.575 → 0.866, 0.765 → 0.821, 0.931 → 0.951, 0.991 against 0.992) are training-log means over the last 50 logged updates, not evaluations. v2 said so ("means over the final training updates", v2 `03_environment.md:189`; v2 03 REQUIRED FACTS: "means over the final updates"). v3's parenthesis keeps the fire alone, 500 updates, 3 seeds and the older encoding, but drops this qualifier. Every other survival number in the paper is an evaluation mean, so the reader cannot tell these apart.
- **Evidence:** `che/bench/results/phase2/phase2_report.md:35` (HEAD): "Final metrics: NaN-safe mean over the last 50 logged updates; across-seed mean ± half min–max range". ENV-2's row also records "± = half the min–max range".
- **Fix:** `(the fire alone, 500<!-- N:ENV-2 --> updates, 3<!-- N:ENV-2 --> seeds per cell, an older observation encoding, training-log means over the final updates, not re-run)`.

### RN1-2 — SHOULD — "4.83-fold" beside rounded counts that give 4.82

- **Location:** `sections/04_calibration.md:69`.
- **What is wrong:** The sentence prints 4.05 and 0.84 and then "This 4.83-fold fall". A reader dividing the printed counts gets 4.82. v2 carried the reason: "a 4.83-fold fall (from unrounded counts)" (v2 `05_coupling_a.md:94`). v3 dropped the parenthesis.
- **Evidence:** CA-4's note: "4.0527 / 0.8398 = 4.83 (from the rounded inputs, 4.82)".
- **Fix:** `This 4.83-fold<!-- N:CA-4 --> fall (from unrounded counts) is fuel exhaustion …`. Alternatively write "about 4.8-fold", as §1 does.

### RN1-3 — SHOULD — CB-9 is "within noise", not "not measurable"

- **Location:** `sections/01_introduction.md:52`.
- **What is wrong:** "Coupling B's own survival effect in calibration was not measurable against a three-seed spread". The effect was measured (−0.03 points). The record says it was judged within noise against a three-seed σ_seed, not that it could not be measured. §4.3 of the same draft says it correctly (`04_calibration.md:86`: "was −0.03 points, judged within noise against a three-seed spread of 0.72 points rather than a measured floor"). The short form should not say less, or something different, than its home.
- **Evidence:** CB-9: "Medium survival −0.0003, 'within noise' … 3 seeds per arm, graded against a 3-seed σ_seed of 0.0072, **not** a measured floor".
- **Fix:** `at its severity, Coupling B's own survival effect in calibration was within the spread of three<!-- N:CB-9 --> seeds, with no measured floor, and communication denial had no detectable effect (§4.3, §4.4, §6.1).`

### RN1-4 — SHOULD — "visible only in the last fifth" and "only at updates 900 to 1000": the scope of RES-12

- **Location:** `sections/00_abstract.md:41` and `sections/01_introduction.md:47`.
- **What is wrong:** RES-12 is scoped to the eleven Γ(t) checkpoints, updates 500–1000 every 50: 900, 950 and 1000 are "the only points whose Šidák CI excludes 0".
  - **The abstract's "visible"** can be read as "present". But survival's point estimate is already positive from update 650 on (RES-11, survival signs `+ − − + + + + + + + +`), and lies between −0.37 and +0.36 points through 850 (DX-25). What appears only in the last fifth is a detectable gain, not a visible one.
  - **The introduction's "detectable only at updates 900 to 1000 of 1000"** reads as if every earlier update had been tested. Updates before 500 were never evaluated (DES-13: Γ(t) at 11 checkpoints, 500–1000).
- **Evidence:** RES-12 (row value and its "last fifth" derivation); RES-11; DES-13; DX-25.
- **Fix:**
  - Abstract: `detectable only in the last fifth<!-- N:RES-12 --> of training`. This is V3-F3's "appears only in the last fifth", with the operative word.
  - §1: `a gain detectable only at the last three checkpoints, updates 900 to 1000<!-- N:RES-12 --> of 1000<!-- N:DES-13 -->`. Alternatively, "of the checkpoints from update 500<!-- N:DES-13 --> on, detectable only at 900 to 1000<!-- N:RES-12 -->".

### RN1-5 — SHOULD — "four thresholds broke its first rule" goes past V5-1 as corrected

- **Location:** `sections/15_appendix_floors.md:39`.
- **What is wrong:** v2's sentence was "four bars whose constants the ruling calls invented" (v2 `13_appendix_locks_floors.md:81`). v3 changes it to "four thresholds broke its first rule". §5 states that first rule as: a bar is used only with a floor measured on the artifact it grades, or the analysis is declared underpowered (`05_measurement.md:28`).
  - The high-severity content ablation (M5.3b) met that rule: it measured its floor on its own runs first, as the same bullet says two sentences later. Its defect was a bar no affordable seed count could reach.
  - V5-1's fix-round note records exactly this correction: "the earlier 'what' said all four lacked a floor, which is wrong for M5.3 and M5.3b".
  - So the new verb reintroduces, for M5.3b, the reading V5-1 was corrected to exclude. CLAUDE.md's own origin line, "four bars set without floors", is the record's looser wording; V5-1 narrowed it.
- **Evidence:** V5-1 (`paper/v2/ledger_proposals/W5.md:14`, note); DX-302; `15_appendix_floors.md:39`, the M5.3b sentence.
- **Fix:** `Before the protocol existed, four<!-- N:V5-1 --> thresholds were set on constants the record later called invented.` The four examples that follow stay as they are.

### RN1-6 — SHOULD — a few numbers have no tag

Each of these has a row. v2 tagged the first two.

| location | number | row | proposed |
|---|---|---|---|
| `04_calibration.md:48` (table header) | $L = 64$ | DX-7 (v2 tagged it, v2 `04_severity.md:58`) | `($L = 64$<!-- N:DX-7 -->)` |
| `04_calibration.md:54` | "the 64-cell arena's" | DX-7 / ENV-6 | `64<!-- N:DX-7 -->-cell` |
| `03_environment.md:104` | "checked in two runs" | DX-304 (v2 tagged it, v2 `05_coupling_a.md:90`) | `two<!-- N:DX-304 --> runs` |
| `04_calibration.md:92` (Fig. 5 caption) | "first two-seed estimate" | CB-6 / DX-40 (m44: "2 seeds (3 at Medium)") | `two<!-- N:DX-40 -->-seed` |
| `15_appendix_floors.md:53` (Fig. C1 caption) | "at 500 and 1000 updates" | DX-34 | `500 and 1000<!-- N:DX-34 --> updates` |

`03_environment.md:236` puts one ENV-6 tag after the whole list "64 × 64 … 32 food items". That is one row covering one group of numbers, so it is acceptable as it stands.

### RN1-7 — SHOULD — X2-2's cross-check cites line values it does not use

- **Location:** `ledger_proposals/W2.md:15` (X2-2, source column).
- **What is wrong:** The Def. 6 cross-check multiplies by smoke values 1.6065 and 1.9744 and cites `P4:40`. That line prints 1.607 and 1.974 (HEAD `phase4_report.md:40`: "ρ at the fire cell therefore runs 1.000, 1.607, 1.974"). The four-decimal values are Def. 6 arithmetic: 1 + e^−0.5 = 1.60653, and 1 + 1.60653·e^−0.5 = 1.97441. With the printed values the products are 0.89832 and 0.98700, so the row's three-decimal values (0.707, 0.898, 0.987) are unaffected. The primary derivation from `tau_profile` is exact.
- **Fix:** In the note, write "the fire cell's smoke 1.000, 1.607, 1.974 (`P4:40`; 1.60653 and 1.97441 by Def. 6 with σ_s 1, η 0.5)".

---

## What was checked and found right (no finding)

### Abstract, hero, §1, §9 and `front_matter.yaml`

- RES-2: 0.96 points, CI [+0.47, +1.44].
- X4-3: "about a tenth", 0.11 of 12. Re-derived at HEAD: 0.11464. The row's scope is the size statement, so DX-406 is correctly not used.
- ENV-6: 12 agents; 64 × 64.
- DES-8: "a third".
- RES-1: 0.66 points.
- DES-13: 1000.
- CB-9: three seeds.
- DX-40: 500 updates.
- CA-4: 4.8-fold.
- CB-5: 3 of 3.
- The hero states no number.
- §9 and `front_matter.yaml` (title, description) state no number.

### §2

ENV-6 (12) and ENV-1 (d_p 0.5). "Their Tables 3–4" is a citation locator verified in v2 (v2 provenance `02_related_work.md:59`).

### §3

- DX-1: ι 0, σ_s 1.0, η 0.5.
- V3-1: one ignition.
- CA-8: nine times.
- CA-9: 0.4–1.4 %, m35, 500 updates.
- X2-7: four quadrature points, `observation.py:78`.
- COM-6: R_comm 16.
- DX-17: [−1, 1]^8, carried from v2 `07_comms.md:35`.
- ENV-1 and ENV-2 to ENV-5: values exact, against HEAD `phase2_report.md:41-48`.
- ENV-9: +1.
- ENV-6.
- ENV-11.
- DX-3: 32,768.
- DX-37: radius 4.

### §4

- DX-204: [0.480, 0.513] and consensus 0.499.
- CAL-1: 0.500 ± 0.005, with its O-2 caveat stated.
- CAL-3: the table, exact.
- DX-201: the bands.
- DX-6: 0.83.
- CAL-4: 0.486.
- CAL-5: 0.00091 / 0.00709 / 0.00885. "Fixed fire-only policies" checked at `R/phase3/def4_variance.md:3`: M2.5 pillar-only checkpoints.
- DX-7: sides 32, 48, 64; 512 seeds.
- CA-1, CB-1, DX-202 (κ_A 0.06, κ_B 1.0, δ 0).
- CA-5: 4.92.
- DX-9: about 5.7.
- CA-6: nine cells, 0.164–0.203.
- CA-7: two seeds.
- DX-11: 0.068 %, 0.249 %, 1.559 %.
- CB-10: 118 / 22 / 16, in severity order.
- DX-13: −6.87, −10.66, −4.70.
- CB-7: 6.21 points.
- CB-8.
- CB-9: −0.03 and 0.72 points.
- COM-4: +0.38 and −1.43 with links open. The sign was checked at HEAD `phase5_report.md:974-980`: δ 0 minus δ 1 = 0.7396 − 0.7358 and 0.9188 − 0.9331. Bars 7.99 and 2.60; four seeds; range 16.
- V4-2: twice.
- V4-1: about half.
- COM-2: two seeds, about 3 points.
- COM-3: 1.01 → 2.99.

### §5

METH-7 (80 %), V4-1 (about half; for a 2σ bar compared directly with the observed contrast, as V4-1 derives) and DX-303 (±40 %).

### App. A, both alternates

- DX-409: about 64 steps at β 0.43.
- DX-304, CA-2 and CA-3: two runs, kept separate, with their parameters.
- CB-4: max |z| 2.11, Σz² 6.55 on 8 dof, p 0.586, mean z −0.44.
- DX-14: 0.0084; J\*(0) = 1.0000.
- ENV-1.
- DX-15: 1.0000; 0.44; 0.51 on 8 dof; 4096 / 8192; 1.126; 1.235; 79 / 54 / 7 %.
- COM-1: 0.498.
- The alternates differ from the main file only in Theorem 1's block (thm1_tf) or the Prop. 4 remark (no_prop4). Their numbers match.

### App. B

- CAL-1, CAL-3, CA-1.
- DX-401: weak_smooth 2; δ 0.0 / 1.0; obs version.
- CB-1, COM-6, ENV-1, DX-1.
- DES-1: 40, 60.
- DES-13: 72, 20, m 2, z 2.2365, 1000, 11, 500–1000 every 50, seed 0 × 512.
- DX-402: 0.80; 1.0, 1.5.
- DX-2: every hyperparameter.
- DX-3; ENV-10; DX-17.
- DX-301: the three bands; "three cells".
- DX-12: 0.130, 0.150.
- CB-2: 1.35, 1.15.
- ENV-12.

### App. C

Every table cell against DX-403, DX-412, METH-1, COM-5, V4-3, CB-7, DX-40, DX-5, METH-2, DX-34, DES-1, DES-5, DX-28, DES-2, DX-35, DES-3, V5-2, HW-4, HW-2, DX-36 and V5-3. Also the overlap intervals (DX-35), the exhibit bullets (V5-1, DX-38, DX-302, COM-5, METH-1, METH-2, METH-3, METH-4, METH-5, DES-13, DX-32, DX-28, DX-306) and eight reruns (DX-403).

### W2's new rows, sources re-read at HEAD

| row | result |
|---|---|
| X2-1 | `phase4_report.md:72` reads `0.5000 ± 0.0055 \| 0.5028 \| −0.0028 \| −0.51`. J\*_pred = ½ + ½·q_MC: 0.5 + 0.5 × 0.0056 = 0.5028, and the same identity holds at κ_B = 1 (0.9052), matching "q from the toy's own transmittances on an independent random stream". 8192 episodes at `:54-55`. |
| X2-2 | −ln τ / κ_B over `e2c_sweep.json`'s seven κ_B > 0 profiles (lines 64, 89, 114, 139, 164, 189, 214) gives 0.7071, 0.8981, 0.9872 at every κ_B. The Def. 6 check √8/4, √5·1.60653/4, 2·1.97441/4 gives 0.70711, 0.89808, 0.98721. The quadrature claim is right at `observation.py:129-137`: one rounded sample lands on the fire cell. See RN1-7 for the note. |
| X2-3 | `e2c_sweep.json:80` gives 0.8115140460771753, and 1 − ∏(1 − τ) recomputes to 0.81151. |
| X2-4 | 1 − (1 − e^−2)(1 − e^−3)(1 − e^−4) = 0.19343. The exponents 4, 3, 2 = d − t + ℓ_f at t = 0, 1, 2. The formula is at `docs/theory_foundations.md:388-390`, unmodified in the working tree. |
| X2-5 | `phase4_report.md:27-29`; `e2c_sweep.json:4-9`; `e2c.py:80-85` (D_PATH 2, L_F 2, CORRIDOR_LEN 4, K_OBS 9, HORIZON 6). |
| X2-6 | `phase4_report.md:141-145` (d = 6, k = 17, τ = 1.0000 at the first two steps, q ≡ 1); `e2c.py:22-34`; `test_coupling_b.py:79`. |
| X2-7 | `observation.py:78` (`N_QUAD = 4`), `:92`, `:129`. |

All seven sources are committed and unmodified.

---

## Re-check (fix2)

Re-check round, step 4.3, 2026-10-16.

**What I compared:** snapshot `fix2` against `draft1` (word-level `git diff --no-index`), in the same scope as above. I read the writers' outcomes in `resolutions_W1.md` to `resolutions_W5.md`.

**State of the tree:**
- `fix2/sections/` is identical to the live `paper/v3/sections/`, alternates included.
- `paper/numbers_ledger.md` and `paper/v2/` are unchanged against HEAD.
- There are still no `W1.md` or `W3.md` proposal files.
- W2 added no row; its only edit is X2-2's note.

**Tags:**
- I re-extracted every tag in scope: 327 instances, all resolving against the 200 IDs now indexed.
- The two IDs added since draft1, IC-4's re-citation and X4-6, are outside my scope.
- The values of the rows my files cite are unchanged. X4-3 still carries 0.009553128646479725.
- CA-9 and CB-8 no longer appear in scope; their sentences were cut (see RN1-8).

| finding | verdict | note |
|---|---|---|
| RN1-1 | OK | The ablation's settings moved to App. B (`14_appendix_locks.md:67`), which now says it "reports training-log means over the final updates and was not re-run" (`phase2_report.md:35`). The values were re-checked: ENV-2 to ENV-5, ENV-1 0.5, 500 updates, 3 seeds. §3 keeps only the High survival pair with "(Appendix B)", so the scope is one click away. |
| RN1-2 | OK | "(from unrounded counts)" is restored at `04_calibration.md:69`. |
| RN1-3 | OK | `01_introduction.md:49`: "was within a three-seed<!-- N:CB-9 --> spread". This matches CB-9 and the home in §4.3. |
| RN1-4 | OK | The abstract (`00_abstract.md:42`) says "detectable only in the last fifth". §1 (`:47`) says "detectable only in the last fifth of training (the checkpoints at updates 900 to 1000)". Both fit RES-12's scope, and the misleading "of 1000" is gone. |
| RN1-5 | OK | `15_appendix_floors.md:39`: "four thresholds were set on constants the record later called invented". This is consistent with V5-1's corrected note. |
| RN1-6 | OK | All five places are now tagged: `03:104` "two" DX-304; `04:48` $L = 64$ DX-7; `04:54` "64-cell" DX-7; the Fig. 5 caption "two-seed" DX-40 (M4.4's first High estimate is 2 seeds, per DX-40); the Fig. C1 caption "500 and 1000" DX-34. |
| RN1-7 | OK | X2-2's note now says that 1.60653 and 1.97441 come from Def. 6 arithmetic, and that the printed values give 0.89832 and 0.98700. I re-computed both. |

### New findings in the changed lines

**RN1-8 — SHOULD — a broken sentence, and Coupling A's agent-influence number has lost its scale**

- **Location:** `sections/03_environment.md:104`.
- **What is wrong:**
  - The fix round cut CA-9's clause (W2, RM-1, the page ceiling; `provenance/03_environment.md:15, :52`) and left the text reading "… collapses nine<!-- N:CA-8 --> times as often as an empty one,. Below the percolation threshold …". The stray ",." prints.
  - CA-8's 9× now stands alone. BRIEF §8.1 lists CA-8 and CA-9 together as the narrowing for "the hazard is not agent-independent". Without CA-9, a reader cannot tell that occupancy adds only 0.4–1.4 % of the collapses per episode under the calibration policies, so the 9× overstates how far agents drive collapse.
- **Fix, preferred:** `… as often as an empty one, though load adds only 0.4 to 1.4 %<!-- N:CA-9 --> to the collapses per episode under 500-update<!-- N:DX-40 --> calibration policies.` This is draft1's clause, about 15 words.
- **Fix, if the page budget forbids that:** at least `… as often as an empty one.`, with CA-9's range stated wherever Coupling A's agent influence is next discussed.

### Other changed lines in scope with numbers, checked with no finding

- **Abstract:** 0.96 "percentage points"; DES-8 "the third"; RES-1 0.66, with the registered string kept verbatim.
- **§1:** "neither arm trained on" (CAL-3: training at β 0.43 and 0.70, test at 0.49).
- **§4.1:** Medium "between" 0.486 (CAL-4) and the fixed 0.500 (CAL-1).
- **§4.2:** CA-4 now scoped to "runs … with Coupling B on", the κ_B = 1.0 arm.
- **§4.3:** "with masking on" (DX-11, the κ_B = 1.0 arm).
- **§4.4:** COM-4 with four seeds.
- **App. C:**
  - The new content-check bullet: COM-2, two seeds, about 3 points; COM-3, 1.01 → 2.99.
  - "the table's first and fourth rows" is right: rows 1 and 4 are the four-run Medium study and the High content ablation.
  - "(G1.2 protocol)".
- **App. A:**
  - The new departures paragraph: ι = 0 is DX-1.
  - "the policy the proof shows optimal (if informed, take the corridor other than Z; else a fixed one)" matches the hand-coded policy at `phase4_report.md:53-55` (tie-break to L).
  - Listings 4 and 5 are moved, not edited.
  - The alternates mirror the main file except Theorem 1's block (thm1_tf) and the Prop. 4 remark (no_prop4).
- **§5:** the reworded exclusion-bound definition (each end bounds its own direction; the larger absolute end bounds the size) introduces no number. The 80 % (METH-7), "about half" (V4-1) and ±40 % (DX-303) tags are unchanged.

**Re-check counts:** OK 7, OK-DECLINED 0, REOPEN 0, OWNER 0. New findings: MUST 0, SHOULD 1 (RN1-8), OWNER 0.
