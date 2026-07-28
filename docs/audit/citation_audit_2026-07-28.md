# Citation audit — phantom-rule class

**Audit target:** `main` @ `0c612b6e8e19c1372592375f097af9a01197cf62`
("Phase-5 pre-flight: Remark 2'/2", artifact-persistence + transcription rules",
2026-07-28 13:04:43 +0300)
**Run:** 2026-07-28, read-only, one Claude Code session, before M5.0.
**Scope:** every reference to a rule, decision, lock, amendment, precedent,
phase-prompt clause, artifact, commit or measured number appearing in
`docs/decision_log.md`, `CLAUDE.md`, and all phase reports must resolve to
written text inside the repository at the pinned commit.
**Output rule:** proposed corrections are diffs in this document. Nothing in
`che/`, `CLAUDE.md` or `docs/decision_log.md` was edited.

**Working-tree note (not part of the audited state):** at audit time the
working tree also carried an unstaged deletion of `phase2_results.zip` and
`phase3_prompt.md`, and two untracked files `phase4_prompt.md` /
`phase5_prompt.md`. Findings C-1 and C-2 below turn on exactly that.

---

## Verdict summary

### By citation class (method: extract, then resolve each against `git ls-tree -r HEAD`)

| class | extracted | resolved | defects |
|---|---|---|---|
| Backtick-quoted paths / artifacts | 115 tokens | **85** | 2 untracked (C-1, C-2), 1 stale line ref (C-7), 1 layout-only (C-8); 24 tokens were globs, directory prefixes or shell commands — not citations; 3 (`*.tar.zst`, `*.sha256`, `provenance.txt`) are correctly absent and the Q4 ruling says so |
| 7-hex commit hashes | 17 distinct | **17** | none |
| `invariant #N` | 35 call-sites | **35** | none; no `#6`+ cited |
| Bibliography entries (in-text ↔ reference list) | 5 | **5** both ways | 4 *uncited* literature claims — see the claim ledger, not a citation defect |
| `precedent` citations (m30b, m31b/m41, M3.5 drift, M4.3) | 4 | **4** | none |
| Named rules / rulings / locks / amendments | 14 | **11** | C-3, C-4, C-5 |
| Locked numeric values traced to a committed artifact | 9 spot-checks | **8** | C-9 |

### By severity

| | count | ids |
|---|---|---|
| **DANGLING** — cited as binding, no written source anywhere | **3** | C-3, C-4, C-5 |
| **UNTRACKED** — source exists on disk only, not at the pinned commit | **2** | C-1, C-2 |
| **STALE** — source exists but no longer says what the citation claims | **3** | C-6, C-7, C-8 |
| **UNTRACEABLE NUMBERS** — a locked value whose estimator output is not committed | **1** | C-9 |
| **AMBIGUOUS** — resolves, but to two entries sharing a label | **1** | C-10 |

The transcription meta-rule added at this very commit ("a chat ruling binds
only once transcribed") is the right rule and it is now in `CLAUDE.md`. The
findings below are the **remaining stock** of pre-rule citations that were
never transcribed — the same class as "tooling rule 3c/3d", found by applying
the new rule backwards over the whole repo.

---

## A. Dangling citations (cited as binding; no written source)

### C-1 — `phase4_prompt.md` is not in the repository

| field | value |
|---|---|
| **Class** | untracked source for binding acceptance bands |
| **Cited at** | `HANDOFF.md:5`, `HANDOFF.md:38`, `kappa_b_lock.md:113` ("Targets (phase4_prompt.md M4.3)"), and by implication every "phase prompt" reference in `phase4_report.md` (lines 4, 8, 139, 237, 433, 538) |
| **Resolves to** | nothing at `0c612b6` — `git ls-files` does not track it; it exists only in the working tree |
| **Severity** | **HIGH** |

`kappa_b_lock.md` states the three κ_B lock bands — masked_frac ∈ [0.15, 0.45],
detection ∈ [0.4, 0.7], E2C q ∈ [0.3, 0.7] — under the heading "Targets
(phase4_prompt.md M4.3)". Those bands are the entire substance of the M4.3
STOP, the band-non-intersection finding, the retirement of `masked_frac`, and
the demotion of E2C. Their stated source is a file that is not under version
control. The bands *are* additionally recorded as data in
`che/bench/results/phase4/m43/coupling_b_calibration.json` → `bands` (verified:
`masked_frac_medium [0.15, 0.45]`, `detection_medium [0.4, 0.7]`,
`e2c_q [0.3, 0.7]`), which is the only committed provenance they have.

This is structurally identical to the tooling-rule-3c incident: a specification
cited for months as repo law, living only outside the repo.

**Proposed correction — commit the prompt.** (Not applied; `phase4_prompt.md`
is outside the audit's write scope only in the sense that it is a
human-authored spec — recommend the human runs it.)

```
git add phase4_prompt.md phase5_prompt.md
git commit -m "Transcribe phase-4/5 prompts into the repo (citation audit C-1/C-2)"
```

**Proposed correction — make the lock self-contained** (diff for human review):

```diff
--- a/kappa_b_lock.md
+++ b/kappa_b_lock.md
@@
-## Targets (phase4_prompt.md M4.3)
+## Targets (phase4_prompt.md M4.3; machine-readable copy in
+## `che/bench/results/phase4/m43/coupling_b_calibration.json` → `bands`)
```

### C-2 — `phase5_prompt.md` is not in the repository

| field | value |
|---|---|
| **Class** | untracked source for the Phase-5 rulings |
| **Cited at** | `docs/decision_log.md:369` — "six questions raised on reading `phase5_prompt.md`" |
| **Resolves to** | nothing at `0c612b6` |
| **Severity** | **MEDIUM** (rising to HIGH the moment M5.0 runs) |

The entire "Phase-5 pre-flight rulings" block (Q1–Q6) and its round-2 sequel
are responses to a document that is not committed. Q5's accountability entry in
particular — "the [2, 5] / [0.3, 0.7] bands were written without the geometry
arithmetic" — is a criticism of text that a future reader cannot read.

Same fix as C-1.

*(Audit-verified in passing: Q5's arithmetic is correct. 12 agents uniform on
64², Chebyshev radius R, boundary-corrected mean alive out-degree
= 11·((2R+1) − R(R+1)/64)²/4096 gives 0.409 at R = 6 and 2.22 at R = 16,
matching the "~0.41" / "~2.22" in the ruling. The band [2, 5] is indeed
unreachable below R ≈ 15.)*

### C-3 — "D6-proposal" does not exist

| field | value |
|---|---|
| **Class** | **phantom** — a gate condition naming a document that was never written |
| **Cited at** | `docs/decision_log.md:314`, `docs/decision_log.md:361` (both PHASE 6 ENTRY GATE blocks), `phase5_prompt.md:140` |
| **Resolves to** | nothing. `docs/decision_log.md` contains D1–D5 and no D6 of any kind; no file in the repo (excluding `.venv`) contains the string other than these three call-sites |
| **Severity** | **HIGH** |

The text is a hard gate: *"PHASE 6 ENTRY GATE (do not start Phase 6 without
executing this line): Re-read D6-proposal with the RA."* A gate that cannot be
executed because its object does not exist is precisely the failure mode the
2026-07-28 meta-rule was written to stop. It is currently duplicated verbatim
at two places in the decision log, which makes it read more binding, not less.

**Proposed correction (diff for human review).** Two branches — the human
chooses:

*(a) if the D6 proposal exists in a chat transcript* → transcribe it as a D6
entry and repoint the gate:

```diff
--- a/docs/decision_log.md
+++ b/docs/decision_log.md
@@
+## D6 (PROPOSAL — not locked) — dose-response mixture design (Phase 6)
+
+<transcribed verbatim from the chat record of <date>>
+
@@
 PHASE 6 ENTRY GATE (do not start Phase 6 without executing this line):
-Re-read D6-proposal with the RA. Decisions owed before any Phase-6 run:
+Re-read the D6 proposal above with the RA. Decisions owed before any
+Phase-6 run:
```

*(b) if it does not* → strike the reference and keep the three owed decisions,
which are self-contained and do not need D6:

```diff
 PHASE 6 ENTRY GATE (do not start Phase 6 without executing this line):
-Re-read D6-proposal with the RA. Decisions owed before any Phase-6 run:
+Decisions owed before any Phase-6 run (no D6 proposal was ever written
+down; struck by the 2026-07-28 citation audit under the transcription
+meta-rule):
 (1) dose-response design formalized into the phase prompt;
 (2) pilot scoped (2 mixture points);
 (3) one-paper vs two-paper fork scheduled for after the pilot.
```

The block appears twice — `decision_log.md:313–317` (indented, inside the M4.4
amendments entry) and `decision_log.md:360–364` (flush, after the M4.4 outcome
entry). One should be deleted in either branch; the flush copy at 360 is the
live one.

### C-4 — "the locked hypothesis" / "the locked ablation list" / "the five locked Phase 7 configs"

| field | value |
|---|---|
| **Class** | **phantom** — the paper's headline hypothesis is cited as locked, with no locked text anywhere |
| **Cited at** | `docs/theory_foundations.md:197`, `:466`, `:532`, `:548` ("Reading 1, locked"), `:577`, `:580` |
| **Resolves to** | nothing. No repo file states the hypothesis, the ablation list, the five Phase-7 configs, or "Reading 1". `docs/decision_log.md` records D1–D5 only; `phase0_substrate_prompt.md` and `phase1_2_prompt.md` do not contain them |
| **Severity** | **HIGH** — this is the load-bearing claim of the submission |

`theory_foundations.md:466` reads: *"**The locked hypothesis, restated:**
Γ(θ*) > 0, with primary metric task completion rate."* "Restated" implies a
prior statement. There is none in the repo. §11's D1 further cites "the locked
ablation list (which ablates couplings/comms, and has static-hazard-trained as
a *separate* config)" — also unwritten. §9(2) cites "(Reading 1, locked)".

Practically: Phase 7 is specified by reference to a document nobody can open,
and the compositional gap Γ's *primary metric* (completion rate) is fixed by
the same unwritten source. Note that the primary metric matters concretely —
M4.4 found the Coupling-B effect lands on **survival**, not completion
(−8.8 pt survival at High, completion within noise). If the locked primary
metric really is completion alone, that decision deserves to be visible.

**Proposed correction (diff for human review)** — transcribe as D0 in the
decision log, since it predates D1:

```diff
--- a/docs/decision_log.md
+++ b/docs/decision_log.md
@@
+## D0 — The locked hypothesis, ablation list, and Phase-7 configs (pre-Phase-0)
+
+Transcribed 2026-07-28 by the citation audit; cited as "locked" by
+`docs/theory_foundations.md` §3, §7, §9 and §11 since v0.1 but never
+written down in the repo. Text below is <verbatim from the chat record /
+RECONSTRUCTED — human to confirm which>.
+
+**Hypothesis (Reading 1):** Γ(θ*) = J_θ*(π_joint) − J_θ*(π_iso) > 0 at
+θ* = all elements active at held-out severity levels. **Primary metric:
+task completion rate.**
+
+**Ablation list (five Phase-7 configs):** <...>
+
+**Held-out severities:** <...>
```

Until that lands, every "locked" in §3/§7/§9/§11 of the theory doc should read
"working" — see the diff bundle at the end of this document.

### C-5 — "Render audit (standing rule)" — no such standing rule

| field | value |
|---|---|
| **Class** | **phantom** — a "standing rule" that exists only as the phrase citing it |
| **Cited at** | `che/bench/results/phase4/phase4_report.md:508` ("### Render audit (standing rule + amendment 4c)"), `che/scripts/run_m44_grid.sh:98`, `phase4_prompt.md:127` ("**Render audit (standing rule):**") |
| **Resolves to** | nothing. `docs/decision_log.md` contains exactly one entry headed "Standing rule" — the 2026-07-21 **100k-line / uint8-contingency** rule (`decision_log.md:69`). `CLAUDE.md` has no render rule. Grepping `-i render` across `decision_log.md` + `CLAUDE.md` returns only incidental prose |
| **Severity** | **MEDIUM** |

Render audits *were* performed at M3.0b, M3.1b and M4.4 and are genuinely
valuable — the M4.4 audit is what confirmed CRN pairing visually and produced
the "High is a single front passage" reading. The defect is only that a real,
repeatedly-honoured practice is cited as a written rule that was never written.
It is a rule worth having: it would have caught the missing matched-High
control before the box was released.

**Proposed correction (diff for human review)** — transcribe it, at the same
place the artifact-persistence rule went:

```diff
--- a/CLAUDE.md
+++ b/CLAUDE.md
@@ (after "Artifact persistence for GPU runs")
+## Render audit standing rule (practice since M3.0b; transcribed 2026-07-28)
+
+**Every acceptance grid renders ≥ 6 episodes per severity at the locked
+parameter value, plus a matched control pair (same episode seeds) on the
+ablation arm at the severity carrying the headline result.** The audit is
+watched, not just produced, and its findings go in the phase report.
+Origin: cited as a "standing rule" by `phase4_prompt.md`,
+`run_m44_grid.sh` and `phase4_report.md` since Phase 3 while existing
+nowhere in writing; the M4.4 gap (matched κ_B = 0 renders at Medium only,
+headline at High) is what it would have prevented.
```

Note the rule as practised was *weaker* than what M4.4 needed. The proposed
wording fixes the gap `phase4_report.md:530` flagged rather than freezing the
version that let it through.

---

## B. Stale citations (source exists, no longer says this)

### C-6 — theory §10's Phase-3 hook still describes the superseded v1 protocol

| field | value |
|---|---|
| **Cited at** | `docs/theory_foundations.md:559–563` |
| **Superseded by** | M3.3 ruling, `docs/decision_log.md:81–130`, human-locked 2026-07-21 |
| **Severity** | MEDIUM (a paper-facing hook) |

§10 still reads: *"measured E[B_T] must scale linearly in collapse rate with
slope ≈ Tχ̂(β), **with χ̂ measured from single-seed runs**."* The M3.3 ruling
logged exactly that comparison as an **RA spec error** (protocol-mismatched
quantities) and replaced it with `matched_reference` computed inside the test.
`che/tests/test_prop3.py::test_prop3_slope_matches_matched_reference` accepts
against `matched_ref` with the human-locked band [0.90, 1.02], not against χ̂.

```diff
--- a/docs/theory_foundations.md
+++ b/docs/theory_foundations.md
@@
 - **Phase 3 unit test:** with $\iota = 0$, $\beta < \hat\beta_c$, measured
   $\mathbb{E}[B_T]$ must scale linearly in collapse rate with slope
-  $\approx T\hat\chi(\beta)$ (Prop. 3), with $\hat\chi$ measured from
-  single-seed runs. Direct quantitative validation of Coupling A's
-  implementation.
+  $\approx T\hat\chi(\beta)$ (Prop. 3). **Protocol (M3.3 ruling,
+  human-locked 2026-07-21):** the reference must be computed *matched to
+  the sweep's protocol* — uniform seed locations, uniform birth times
+  (age-averaged), unconditional cluster mass — not against the Phase-2
+  centre-seeded, spanning-conditioned $\hat\chi$. Comparing the two was
+  logged as a spec error; the L = 32 pass under the naive comparison was
+  a cancellation of opposite biases. Direct quantitative validation of
+  Coupling A's implementation.
```

### C-7 — `run_m44_grid.sh:128` now points at the retro-flag, not the violation

| field | value |
|---|---|
| **Cited at** | `docs/decision_log.md:402` — *"`run_m44_grid.sh:128` states 'ckpt_* dirs stay on the box'"* |
| **Actual** | at `0c612b6`, line **128** is the first line of the `# RETRO-FLAG (human, 2026-07-28)` comment block (128–134); the `echo` the citation describes is line **135**, the last line of the file |
| **Severity** | LOW — cosmetic, but it is a line-number citation inside a ruling about citation discipline, and the fix ordered by that same ruling is what moved it |

A neat self-referential drift: ruling item 4(2) ordered the line retro-flagged
in place; doing so inserted seven comment lines *above* it, so the citation
recorded in item 4 now resolves to the flag rather than to the flagged line.

The ruling's three-part fix was audited and **all three parts are executed at
this commit**: (1) the artifact-persistence rule is `CLAUDE.md:148–155`;
(2) `run_m44_grid.sh:128–135` carries the RETRO-FLAG block and the superseded
echo; (3) the transcription meta-rule is `CLAUDE.md:139–146`.

```diff
--- a/docs/decision_log.md
+++ b/docs/decision_log.md
@@
-or `*.sha256` exists in the repo tree, and `run_m44_grid.sh:128` states
+or `*.sha256` exists in the repo tree, and `run_m44_grid.sh` (line 128 at
+ruling time; line 135 once fix (2) below inserted the retro-flag above it)
+states
 "ckpt_* dirs stay on the box" — so M4.4 did **not** produce a local
```

### C-8 — `CLAUDE.md`'s repository layout lists `che/env/comms.py`, which does not exist

| field | value |
|---|---|
| **Cited at** | `CLAUDE.md` repository-layout block |
| **Actual** | `che/env/comms.py` is absent; it is M5.0's deliverable (`phase5_prompt.md:26`) |
| **Severity** | LOW |

Every other path in the layout block resolves (14/15 checked individually).
The layout is aspirational for this one row. Harmless today; worth a marker so
it is not read as "already built". Fix belongs in `CLAUDE.md` (out of write
scope):

```diff
-    comms.py       # link graph sampling + message masking (Def. 7)
+    comms.py       # link graph sampling + message masking (Def. 7) — M5.0, not yet built
```

---

## C. Untraceable numbers

### C-9 — the locked β̂_c = 0.500's lead estimator is not reproducible from the repo

| field | value |
|---|---|
| **Class** | numeric provenance gap |
| **Cited at** | `severity_lock.md:11` — *"R_L logistic centers (32/48/64) \| 0.4985 / 0.5006 / 0.4999 \| L-independent; **the pivot**"*; `severity_lock.md:16` — *"Self-duality check R_L(0.500) \| 0.488 / 0.502 / 0.494"*; quoted onward by `calibration_report.md:99–103` and `phase2_report.md:92` |
| **Resolves to** | **no committed artifact and no committed code path** |
| **Severity** | **HIGH** — β̂_c = 0.500 ± 0.005 is the anchor for all three severity locks and for the "CA port is quantitatively validated" claim |

Verified against the committed data:

- `che/bench/results/phase2/estimates.json` contains
  `beta_c_R_crossings` = {L32×L48: [0.4986, 0.5025, 0.5157], L48×L64: [0.5010]},
  mean **0.5045**; `beta_c_logistic_fit_L64` = **0.4893** (that is a logistic
  fit of **P_span**, not of R_L); `R_at_beta_c_consensus` =
  {L32: 0.4795, L48: 0.4838, L64: 0.4741} at β = 0.4991.
- `che/calibration/estimates.py:213` applies `logistic_fit` to
  `out["p_span_L64"]` **only**. There is no per-L logistic fit of R_L anywhere
  in `che/`.
- The strings `0.4985`, `0.5006`, `0.4999`, `0.488 / 0.502 / 0.494` occur in
  the repo **only** in `severity_lock.md` and in `calibration_report.md`'s
  quotation of it.

So the pivot estimator — the one row `severity_lock.md` labels as decisive, and
the one that lands on 0.500 rather than the committed 0.5045 — was computed by
an RA script that was never committed, and its output was never written to
`estimates.json`. `severity_lock.md:3–5` says the data was "independently recomputed by the
RA", which is honest about the recomputation but does not flag that the
recomputation left no trace.

Second, smaller discrepancy in the same table: row 2 reports "Fit-based R_L
pairwise crossings | 0.498–0.507". The committed crossings span
0.4986–0.5157 (`calibration_report.md:31` reports the L32×L48 triple as
0.499–0.516 and says "all are reported, none discarded"). If "fit-based" means
crossings of the *fitted* curves rather than the raw ones, that is a third
uncommitted computation; if not, the stated range silently drops the 0.5157
crossing.

**This does not mean the lock is wrong.** β̂_c = 0.500 sits inside the
committed spread [0.480, 0.513], the committed consensus mean is 0.4991, and
the theory test's band [0.42, 0.58] passes with room. It means the *pivot*
cannot currently be audited, and a reviewer asking "how did you get 0.500 and
not 0.5045?" cannot be answered from the repository.

**Proposed correction** — add the estimator to `che/calibration/estimates.py`
so `estimates.json` carries it, then re-quote (code change is out of this
audit's write scope; specified here for M5.x or a standalone fix):

```python
# che/calibration/estimates.py, inside compute_all(), crossing branch
r_logistic = {
    f"L{L}": logistic_fit(betas, out[f"r_cross_L{L}"])[0] for L in sizes
}
out["beta_c_R_logistic_centers"] = r_logistic          # the severity_lock pivot
out["R_at_half"] = {f"L{L}": float(np.interp(0.500, betas, out[f"r_cross_L{L}"]))
                    for L in sizes}                     # the self-duality row
```

and then:

```diff
--- a/severity_lock.md
+++ b/severity_lock.md
@@
-| R_L logistic centers (32/48/64) | 0.4985 / 0.5006 / 0.4999 | L-independent; the pivot |
-| Fit-based R_L pairwise crossings | 0.498–0.507 | ill-conditioned (curves coincident) — consistent |
+| R_L logistic centers (32/48/64) | 0.4985 / 0.5006 / 0.4999 | L-independent; the pivot. Recomputed by the RA from `calibration_crossing.npz`; **not** in `estimates.json` at the time of the lock — see `estimates.json:beta_c_R_logistic_centers` once the estimator lands |
+| Fit-based R_L pairwise crossings | 0.498–0.507 (crossings of the *fitted* curves; the raw-curve crossings in `estimates.json` span 0.4986–0.5157) | ill-conditioned (curves coincident) — consistent |
```

---

## D. Ambiguous citations

### C-10 — "amendment 4" and "amendment 4a/4b/4c" are two different entries

| field | value |
|---|---|
| **Cited at** | `phase4_report.md:232` ("human amendment 4" = third seed at Medium); `phase4_report.md:353` ("amendment 4a"), `:508`, `:531` ("amendment 4c"); `run_m44_grid.sh:7, 25`; `run_p5_pretask_high_kb0.sh:5`; `m44_report.py:11` |
| **Resolve to** | **different documents.** "amendment 4" → `decision_log.md:308` *M4.4 amendments* item 4 (third seed). "amendment 4a/4c" → `decision_log.md:255` *M4.3 lock* item 4, "M4.4 addenda (a)/(b)/(c)" |
| **Severity** | LOW — both resolve; the collision is a readability trap for the paper's methods section |

Recommend calling the second family "M4.4 addendum (a)/(c)" everywhere, matching
its actual heading, and reserving "amendment N" for the *M4.4 amendments* block.

---

## E. Everything that resolved cleanly (spot-checks worth recording)

Recorded so the human can see the audit was not one-sided.

| Citation | Verified against | Result |
|---|---|---|
| 17 distinct 7-hex commit hashes across all `.md` | `git cat-file -e` | **17/17 resolve** |
| D4 evidence: "High survival 0.575 → 0.866, deaths_fire 5.10 → 1.61 (−68%), completion 0.765 → 0.821" | `phase2_report.md:47–48` | exact |
| M4.4 outcome item 3: "Medium detection 0.4465 at 500 updates" | `phase4_report.md:455`, `m44_analysis.json` | exact |
| κ_B lock revision table, κ_B = 1.0 row: det 0.3836 / 0.4383 / 0.4266 | raw `m43/coupling_b_calibration{,_probe_kB0.5,_probe_kB1.5}.json`, index of κ = 1.0 | **exact to 4 dp** |
| κ_B lock, E2C q = 0.812 at κ_B = 1.0 | `m43/*.json` → `e2c_q[6]` = 0.81151 | exact |
| Q5 geometry arithmetic (mean degree 0.41 @ R=6, 2.22 @ R=16) | recomputed with boundary correction | **confirmed** |
| M3.3 waterfall: 62.85 ×1.121 ×0.834 ×0.928 ×0.836 = 45.56 | `m33/deficit_decomposition.json`, arithmetic | closes |
| Prop.-3 residual is L-independent (0.843 @ L32 vs 0.836 @ L64) | `phase3_report.md:99` | consistent with the claim |
| M4.2 gate constants (2.69 Šidák, χ²(n) p ≥ 0.05, 2/√n) | `che/tests/test_e2c.py:48–70` comment block | present verbatim, with rationale |
| Artifact-persistence rule + transcription meta-rule "all executed this session" | `CLAUDE.md:138–156`, `run_m44_grid.sh:130–137`, `run_p5_pretask_high_kb0.sh` | **3/3 executed** |
| "no `*.tar.zst` or `*.sha256` exists in the repo tree" (Q4 finding) | `git ls-tree -r HEAD` | **still true** — correct as written |
| Theory bibliography (Bernstein 2002, Grassberger 1983, Kesten 1980, Jaderberg 2017, Haksar & Schwager 2018) | in-text ↔ reference list | **5/5 both ways** |
| `phase0_report.md`: "$110–215 acceptable band", "fallback ladder rung 2" | `phase0_substrate_prompt.md:100–111` | exact |
| "M3.5 drift precedent", "M3.4 → M3.5 precedent", "m30b precedent", "M4.3 precedent" | `coupling_a_lock.md:95–104`, `phase3_report.md:208`, `.gitignore`, `kappa_b_lock.md` | all four resolve |
| `invariant #1…#5` (35 call-sites) | `CLAUDE.md` invariants 1–5 | all resolve; no #6+ cited |
| 14 of 15 paths in `CLAUDE.md`'s layout block | filesystem | 14 OK, 1 = C-8 |

---

## F. Repository hygiene, noticed in passing (not citation defects)

1. **`phase3_prompt.md` is deleted in the working tree but tracked at HEAD.**
   `coupling_a_lock.md:13` and `decision_log.md:83` cite it. It resolves at the
   audited commit; committing that deletion would convert both into C-1-class
   dangling citations. Recommend `git restore phase3_prompt.md`.
2. **`phase2_results/` duplicates `che/bench/results/phase2/`** (35 tracked
   files, byte-identical reports), and `phase2_results.zip` is *also* tracked
   and *also* deleted in the working tree. Three copies of one phase's
   artifacts, two of them in a half-deleted state, is a provenance hazard: a
   citation to `calibration_report.md` by basename now has two committed
   targets.
3. **`.gitignore` for Phase 5 already implements the artifact-persistence
   rule correctly** — `*.tar.zst` ignored, `.sha256` and `provenance.txt`
   committed. Confirmed against `CLAUDE.md:147–156`. No action.

---

## G. Consolidated diff bundle for human review

Everything below is proposed, **not applied**. Ordered by severity.

```
HIGH    C-3   strike or transcribe "D6-proposal"          docs/decision_log.md
HIGH    C-4   transcribe the locked hypothesis as D0      docs/decision_log.md
HIGH    C-9   commit the R_L logistic-centre estimator    che/calibration/estimates.py + severity_lock.md
HIGH    C-1   git add phase4_prompt.md                    (repo root)
MED     C-2   git add phase5_prompt.md                    (repo root)
MED     C-5   transcribe the render-audit standing rule   CLAUDE.md
MED     C-6   repoint theory §10's Phase-3 hook to v2     docs/theory_foundations.md
LOW     C-7   line-number note                            docs/decision_log.md
LOW     C-8   mark comms.py as not-yet-built              CLAUDE.md
LOW     C-10  rename "amendment 4a/4c" → "M4.4 addendum"  phase4_report.md + scripts
LOW     F-1   git restore phase3_prompt.md                (working tree)
LOW     F-2   de-duplicate phase2_results/                (repo root)
```

Additional wording change implied by C-4, applied nowhere until D0 lands — in
`docs/theory_foundations.md`, six occurrences of "locked" that currently point
at nothing:

```diff
-transfer ("held-out severity levels" in the locked hypothesis) a statement
+transfer ("held-out severity levels" in the working hypothesis) a statement
@@
-**The locked hypothesis, restated:** $\Gamma(\theta^*) > 0$, with primary
+**The working hypothesis:** $\Gamma(\theta^*) > 0$, with primary
@@
-environment; (ii) the five locked Phase 7 configs are five points in $\Theta$;
+environment; (ii) the Phase 7 configs are five points in $\Theta$;
@@
-   empirical by design (Reading 1, locked).
+   empirical by design.
@@
-  the locked ablation list (which ablates couplings/comms, and has
+  the working ablation list (which ablates couplings/comms, and has
@@
-- **D2 — ISO instantiation.** The locked hypothesis says "trained on each
+- **D2 — ISO instantiation.** The working hypothesis says "trained on each
```

---

## H. What this audit could not check

Stated so the coverage is not overread.

- **Chat-transcript claims.** Where a citation points at a human ruling issued
  in conversation, this audit can only report that the repo does not contain
  it. C-3, C-4 and C-5 may each have a real chat origin; that is the human's
  call to transcribe or strike, exactly as the meta-rule prescribes.
- **Numbers inside `.npz`/`.png` artifacts** were checked only where a JSON
  sibling existed. The M4.4 tables were spot-checked against
  `m44_analysis.json`, not re-derived from the per-episode `.npz` files.
- **GPU-run reproducibility.** No run was re-executed. Provenance blocks
  (commit, device, wall time) were checked for presence and internal
  consistency, not re-measured.
- **`phase1_2_prompt.md` and `phase0_substrate_prompt.md`** were read for
  citation *targets* (they resolve) but their own outbound citations were not
  audited to the same depth as the decision log and phase reports.
