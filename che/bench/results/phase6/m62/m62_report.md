# M6.2 Report — the Phase-6 floor milestone

**Status: the milestone completed; one of its three registered guards fired.**
The plateau guard reports **STILL CLIMBING on both confirmatory arms**, which
is a registered **STOP**. The floor and power guards passed. The ruled
response — a T = 1000 re-run, not a discretionary extension — is recorded in
`docs/decision_log.md` (*PHASE-6 FRAMING + ALLOCATION RULING*, sequence step
(b)).

> **NO-PEEKING APPLIES TO THIS DOCUMENT** (ruled 2026-08-02). M6.2's
> cross-arm outcome comparisons are calibration by-catch, and the
> confirmatory contrast is read **once**, at T\*, through the blind pipeline.
> **No per-arm or cross-arm outcome mean appears anywhere below** —
> dispersion, drift and power only. The raw values are retained in
> `floors.json`, where they are needed at unblinding. Drift ratios are
> explicitly reportable at a STOP (sequence step (d)), and are reported.

Registered in `phase6_design_v2.md` §4; rulings in `docs/decision_log.md`
(*PHASE-6 REMEDY RULINGS* 4, *PHASE-6 RULINGS, FINAL FIVE* 1a and 3, and the
seed amendment).

**Card: RTX PRO 6000 Blackwell**, jax/jaxlib 0.11.0, source at `64a7397`.
24 runs = 3 arms × 8 identical reps at seed 0, T = 500 updates, each trained
on its protocol config and evaluated on **512 episodes at θ\*** via
`--allow-hash` — cross-config evaluation **declared, not smuggled**.

---

## 1. The headline

| question | answer |
|---|---|
| Did all 24 runs complete? | **Yes** — no process surprise; the shakedown passes. |
| Are the per-arm floors different enough to matter? | **Yes** — completion sd differs **1.77×** between the two arms Γ contrasts. |
| Does k = 34 survive the measured floors? | **Yes** — power@0.03 > 99.99 % on all four confirmatory metrics; the < 75 % STOP does not fire. |
| Is 500 updates enough? | **No.** Both confirmatory arms are still climbing → **STOP**. |
| What does a run actually cost? | **288 s** (269 train + 19 eval), vs v2's 257 s train with eval unmeasured. |

**These floors are T = 500 artifacts and they die with the re-run.** They
graded the seed count and nothing else; the floors that grade the grid are
measured on the T\* artifact at step (b). Recorded explicitly because
carrying them forward is exactly the per-artifact error the rule forbids.

---

## 2. Per-arm floors — dispersion only

8 identical reps at the same seed, so the spread is **run-to-run
nondeterminism**, not seed spread.

| arm | metric | sd (FLOOR) | range |
|---|---|---|---|
| ISO | completion | 0.0165 | 0.0510 |
| | survival_rate | 0.0134 | 0.0347 |
| | episode_return | 0.5002 | 1.5645 |
| | deaths_fire | 0.1405 | 0.3477 |
| JOINT-classic | completion | **0.0093** | 0.0337 |
| | survival_rate | 0.0156 | 0.0410 |
| | episode_return | 0.3135 | 1.1006 |
| | deaths_fire | 0.1865 | 0.4844 |
| sweep p = 0.5 | completion | 0.0157 | 0.0453 |
| | survival_rate | 0.0110 | 0.0345 |
| | episode_return | 0.4784 | 1.3291 |
| | deaths_fire | 0.1498 | 0.4551 |

n = 8 per arm. Full values, including the means, in `floors.json`.

### The per-artifact rule earned its keep here

Completion sd is **0.016475 on ISO and 0.009301 on JOINT** — a ratio of
**1.77**. These are the two arms whose difference *is* Γ, so a single shared
floor would have mis-graded one of them by construction:

- grade JOINT against ISO's floor → its bars are **77 % too loose**
  (0.016475 / 0.009301 = 1.771);
- grade ISO against JOINT's floor → its bars are **44 % too tight**
  (0.009301 / 0.016475 = 0.565).

Neither is a rounding difference, and no argument available *before* the
measurement would have told us which arm was the noisier one. The rule was
adopted on a bitwise-equivalence exhibit at M6.0; this is its first
quantitative payoff on a graded quantity.

**Flagged, per design v2 §4:** floors for the four intermediate sweep points
are **assumed common** with the p = 0.5 point. The sweep is secondary and
non-verdict-bearing, so the assumption is stated rather than measured — but
the ISO/JOINT gap above is direct evidence that such assumptions can be
wrong by ~1.8× between arms, and any sweep claim must carry that caveat.

### Against the pre-M6.2 priors

Design v2 §5 registered the seed count against Medium-cell priors of
**completion σ 0.0399, survival σ 0.0130**.

| metric | ISO | JOINT |
|---|---|---|
| completion vs prior 0.0399 | 2.42× **smaller** | 4.29× **smaller** |
| survival vs prior 0.0130 | 1.03× larger | 1.20× larger |

Completion came in far tighter than the prior; **survival came in at or
slightly above it**. Recorded in both directions, because a report that only
notes the favourable half of a floor measurement is not a floor measurement.

---

## 3. Plateau guard — FIRED, on both confirmatory arms

Drift of completion over the final 100 updates, graded against **each arm's
own** floor (`PLATEAU_PASS` = 1.0).

| arm | slope / update | drift / 100 updates | its floor | ratio | verdict |
|---|---|---|---|---|---|
| ISO | +0.000174 | +0.0174 | 0.0165 | **1.06×** | climbing (REVIEW band) |
| **JOINT-classic** | **+0.000295** | **+0.0295** | **0.0093** | **3.17×** | **clearly climbing** |
| sweep p = 0.5 | +0.000056 | +0.0056 | 0.0157 | 0.36× | plateaued |

**Two of three, and the two are the two that matter.** The sweep is secondary
and does not gate; both **confirmatory** arms fail.

### The sharp part is the asymmetry, not the magnitude

JOINT is still improving **1.69× faster than ISO** at the end of training
(0.000295 vs 0.000174 per update). Γ = J(joint) − J(iso) at θ\*, so an
*asymmetric* convergence rate between exactly the two contrasted arms is a
**direct confound on the headline quantity**. Symmetric non-convergence would
at least partially cancel in a difference; this does not — it biases Γ in a
direction fixed by which arm happens to be slower to converge, which is an
artifact of training-set difficulty rather than of composition.

Plausible mechanism, stated as a hypothesis and not tested here: **JOINT
trains on 2 all-elements-co-active components while ISO trains on 6
single-element ones.** The harder curriculum has further to go at any fixed
update count.

This is why the ruled response is a **T = 1000 re-run under the registered
criterion** rather than a discretionary extension: the question "is the run
long enough" becomes a measurement with its answer fixed in advance.

---

## 4. Power recompute on the measured floors — k = 34 stands

Šidák m = 2 (family α = 0.05 → per-comparison 0.02532, z_crit 2.2365),
k = `K_CONFIRMATORY` = 34, target effect 0.03.

| arm | metric | σ | MDE at 80 % power | power @ 0.03 |
|---|---|---|---|---|
| ISO | completion | 0.0165 | **0.0123** | > 99.99 % |
| ISO | survival | 0.0134 | 0.0100 | > 99.99 % |
| JOINT | completion | 0.0093 | **0.0069** | > 99.99 % |
| JOINT | survival | 0.0156 | 0.0117 | > 99.99 % |

The registered STOP (*PROVISIONAL ON M6.2*: confirmatory completion power
below 75 % → re-rule k) **does not fire**. Per that same ruling's other
branch, **the surplus is recorded and k = 34 stands** — it is not spent down.

Two honest caveats. **First**, the MDEs above are 80 %-power MDEs at the
family-corrected α, per the standing rule; they are *not* 2σ√(2/k) detection
thresholds, which would be smaller and would mean something different.
**Second**, 0.03 is an upper bound on *observed* completion effects in
earlier phases, not a prior on the true effect at θ\* — it is the best anchor
available and the seed count is calibrated against it, nothing more.

**And these numbers do not carry forward.** They are computed on T = 500
floors. Step (b) recomputes power on the measured T = 1000 floors against a
threshold that has since moved to **80 %**.

---

## 5. Measured cost — discharges design v2 §6

| quantity | measured | n |
|---|---|---|
| train (500 updates) | **269 s** median | 24 |
| eval (512 episodes at θ\*) | **19 s** median | 24 |
| **per run** | **288 s** | |

v2 §6 assumed **257 s** train and left evaluation **estimated, not measured**.
The measured total is 12 % above the registered basis. At ~$1/h that is
**$0.08/run**; money remains not the binding constraint.

Extrapolation for step (b), labelled an estimate: train scales linearly in
updates and eval is flat, so T = 1000 → 2 × 269 + 19 ≈ **557 s/run**, and 24
runs ≈ **3.7 GPU-h ≈ $4**.

---

## 6. A bug in our own instrument, found during this analysis

`m62_report.py` sliced the **NaN-filtered** completion series by `--tail`.
Completion is NaN on any update that finished no episode — at horizon 256 and
`rollout_len` 128 that is **every other update**, uniformly (measured on these
logs: 250 non-NaN rows of 500; inter-point gap exactly 2, no exceptions). The
"final-100-update" window therefore spanned **200 updates**, and every drift
came out ≈ 2× high.

**Effect on the verdict:** the pre-fix run flagged **all three** arms;
corrected, it flags **two**. The STOP fires either way, so no decision was
made on the wrong number — but the on-box report's drift *magnitudes* were
wrong, and the "all three" figure had already been relayed into a ruling,
where it was corrected on transcription rather than transliterated.

**The fix, and a second pass over it.** The window and the regression now both
run on the **logged update number**, so neither depends on how densely
completion happens to be logged. An intermediate form of the fix rescaled a
position-based slope by `len(win)/tail`, which is exact only under uniform
spacing; it agreed to every digit on these logs, but the assumption is not one
a frozen instrument should carry. Both forms produce **bit-identical** slopes
here — verified — so no number in this report depends on which was used.

**Also folded in at the same time**, since a dirty script cannot be a frozen
instrument (sequence step 0):

- **Rule-2 mean suppression**, mechanical rather than behavioral: the printed
  report emits sd, range and drift only. `floors.json` keeps the raw values.
- **`POWER_STOP` 0.75 → 0.80** for step (b), and every threshold in the module
  is now a **named constant mirrored in `docs/locks.yaml`** under `analysis:`,
  asserted against the module literal by `test_locks.py`
  (*ANALYSIS-CONSTANT REGISTRY*, 2026-08-02).
- **`PLATEAU_REVIEW` = 1.5**, reporting-only: it labels ISO's 1.06× as
  marginal without touching the binary verdict at `PLATEAU_PASS` = 1.0.

---

## 7. Shakedown — the dropped pilot's surviving job

**24 of 24 runs completed.** No failure, no resume, no config-hash refusal, no
missing artifact. The job script's fail-fast checks (`--allow-hash` present,
`tar --zstd` available, all four summary files non-empty before release) all
held, and the per-run `|| exit 1` never triggered.

The pilot was dropped on the grounds that it could not protect a spend smaller
than itself; its shakedown role moved here. That role is discharged.

---

## 8. Provenance and artifacts

- **Checkpoint archive:** `m62_artifacts.tar.zst`, sha256
  `eb0ba874fb7eb8d85a982ac77da1cba283edb51d886008c3c6bc8a960726cbfb`,
  **79/79 files verified** after transfer. The 24 `ckpt_*.tar.zst` are
  gitignored (`.gitignore:268`); their individual hashes are in
  `SHA256_CKPT.txt`, which is committed.
- **Committed here:** the 24 metric `.jsonl`, 24 `eval_*.json` + `.npz`,
  `floors.json`, `plateau.json`, `power.json`, `verdict.txt`,
  `provenance.txt`, `timings.txt`, `SHA256_CKPT.txt`, `SHA256SUMS.txt` and
  `m62_console.log`.
- **`verdict.txt`, `floors.json`, `plateau.json` and `power.json` were
  regenerated off-box** by re-running the corrected instrument on the pulled
  artifacts — no run was repeated. The regeneration is recorded in
  `provenance.txt` itself.
- **`m62_console.log` is the raw on-box run log** and contains the *pre-fix*
  printed report, including its outcome means. It is retained deliberately as
  the unedited record of what the box did. Rule 2 binds **documents** that
  cite cross-arm means; this is an artifact, and nothing in this report or any
  other document reads a mean from it.

---

## 9. What this milestone hands to step (b)

1. A **STOP**, with drift ratios reported and no cross-arm means.
2. A **validated per-arm floor instrument** — the method, not the numbers.
3. A **measured cost basis** of 288 s/run at T = 500, from which the T = 1000
   estimate is extrapolated.
4. A **clean shakedown**, so a failure at step (b) is a signal rather than
   noise.

What it explicitly does **not** hand forward: any floor, any bar, any power
figure. Those are length-specific and are re-measured on the T\* artifact.
