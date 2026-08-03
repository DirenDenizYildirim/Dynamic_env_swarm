# M6.2b Report — the floor milestone re-run at T = 1000

**Status: the question step (b) was ordered to settle is answered — and a
different registered guard fired.**

- **Plateau: BOTH confirmatory arms PASS.** The asymmetric-convergence
  confound that motivated this re-run is **resolved**.
- **Power: STOP.** JOINT completion power@0.03 is **62.8 %** on the measured
  T = 1000 floor, below the registered **80 %**.

Per the registered sequence (`docs/decision_log.md`, *PHASE-6 FRAMING +
ALLOCATION RULING*, step (b) else-branch): **STOP, report; k is re-ruled by a
human.** This report discharges the "report" half. **k is not re-ruled here**,
and neither is the variance question raised in §6.

> **NO-PEEKING APPLIES** (ruled 2026-08-02). Dispersion, drift and power only.
> **No per-arm or cross-arm outcome mean appears below.** Raw values are in
> `floors.json`, where they are needed at unblinding. Drift ratios are
> explicitly reportable at a STOP (step (d)) and are reported.

**Card: RTX PRO 6000 Blackwell**, 97,887 MiB. **Python 3.12.3, jax/jaxlib
0.11.0.** Source at `1309ef3`. 1000 updates, 512-episode evals at θ\* via
`--allow-hash`.

---

## 1. Headline

| question | answer |
|---|---|
| Do both confirmatory arms converge at T = 1000? | **Yes.** ISO 0.10×, JOINT 0.57× of their own floors. |
| Is the T = 500 asymmetry gone? | **Yes.** JOINT was climbing 1.69× faster than ISO; now both sit inside their floors. |
| Do the floors carry forward from T = 500? | **No — they grew.** ISO 2.1×, JOINT **5.2×**. |
| Does k = 34 survive the measured floors? | **No.** JOINT completion 62.8 % < 80 % → **STOP**. |
| Is survival affected? | **No.** > 99.99 % on both arms. |
| Was the milestone completed? | **No — cut at 17 of 24** (see §7). Both confirmatory arms had finished 8/8. |

---

## 2. Per-arm floors at T = 1000 — dispersion only

8 identical reps at the same seed, so the spread is **run-to-run
nondeterminism**, not seed spread.

| arm | metric | sd (FLOOR) | range |
|---|---|---|---|
| ISO | completion | **0.0339** | 0.1069 |
| | survival_rate | 0.0093 | 0.0269 |
| | episode_return | 1.0757 | 3.4004 |
| | deaths_fire | 0.1077 | 0.3223 |
| JOINT-classic | completion | **0.0483** | 0.1366 |
| | survival_rate | 0.0159 | 0.0545 |
| | episode_return | 1.6058 | 4.5928 |
| | deaths_fire | 0.1970 | 0.6621 |

n = 8 per arm. The **sweep p = 0.5 arm completed only 1 rep and is therefore
reported as no floor at all** — one run has no dispersion, and an assumed
floor would be worse than an absent one.

### These floors carry real uncertainty, and the powers below inherit it

Stated here rather than left for a reviewer. At n = 8 an sd estimate has 7
degrees of freedom:

| arm | completion sd | 95 % CI on that sd |
|---|---|---|
| ISO | 0.0339 | **[0.0224, 0.0690]** |
| JOINT | 0.0483 | **[0.0319, 0.0983]** |

Every power figure in §4 is a **point estimate computed on a 7-dof variance
estimate**. The registered guard grades the point estimate, and this report
follows that rule — but "62.8 %" should not be read as a precise quantity.
Design v2 §4 bought 8 reps over 4 because n = 4 leaves the sd uncertain by
~±40 %; at n = 8 it is roughly −34 %/+104 %. That is better, not tight.

---

## 3. Plateau guard — BOTH ARMS PASS

Drift of completion over the final 100 updates, graded against **each arm's
own** floor (`PLATEAU_PASS` = 1.0).

| arm | slope / update | drift / 100 updates | its floor | ratio | at T = 500 |
|---|---|---|---|---|---|
| ISO | +0.000034 | +0.0034 | 0.0339 | **0.10×** | 1.06× |
| JOINT-classic | +0.000276 | +0.0276 | 0.0483 | **0.57×** | 3.17× |

**This is what the re-run was ordered to settle, and it settled it.** At
T = 500 the problem was not non-convergence as such but **asymmetric**
convergence: JOINT was still improving 1.69× faster than ISO at end of
training, and since Γ = J(joint) − J(iso) is exactly their difference, an
asymmetric rate biases the headline quantity in a direction fixed by which
arm converges more slowly — an artifact of curriculum difficulty, not of
composition. Symmetric non-convergence would partly cancel in a difference;
asymmetric does not.

At T = 1000 both arms sit inside their own floors. **The confound is gone.**

Under the registered item-2 criterion (*T\* = 1000 iff both confirmatory arms
pass the plateau guard at the T = 1000 re-run*), **the plateau branch is
satisfied.** It is the power branch, evaluated at the same step, that STOPs.

---

## 4. Power on the measured floors — the STOP

Šidák m = 2 (family α = 0.05 → per-comparison 0.02532, z_crit 2.2365),
k = 34, target effect 0.03.

| arm | metric | σ | MDE at 80 % power | power @ 0.03 | |
|---|---|---|---|---|---|
| ISO | completion | 0.0339 | 0.0253 | **92.2 %** | pass |
| ISO | survival | 0.0093 | 0.0069 | > 99.99 % | pass |
| **JOINT** | **completion** | **0.0483** | **0.0360** | **62.8 %** | **STOP** |
| JOINT | survival | 0.0159 | 0.0118 | > 99.99 % | pass |

**Derived threshold:** the 80 % guard fires once a confirmatory completion
floor exceeds **σ = 0.0402**. ISO is 16 % below that line; JOINT is 20 %
above it.

**Survival is comfortable everywhere**, which matters for the co-primary: the
composition and coupling claims that survival carries are not power-limited.
The primary task-performance metric is.

---

## 5. Floors grew with T — and the growth looks structural

The ruling said explicitly: *"Do not presume its outcome — floors are
per-artifact facts and may grow with T."* They grew, and unevenly.

| arm | completion floor T = 500 | T = 1000 | growth |
|---|---|---|---|
| ISO | 0.0165 | 0.0339 | **2.1×** |
| JOINT-classic | 0.0093 | 0.0483 | **5.2×** |

**Hypothesis, offered as one and not tested here.** At T = 500 both arms were
still climbing steeply, so identical-seed reps were sampled at similar points
on a steep curve and their spread was small. By T = 1000 they have had room to
settle into **different optima**, and the spread reflects that divergence
rather than transient noise.

If that is right, three things follow, and all three are worth carrying:

1. **Floor growth is the price of convergence.** The plateau guard and the
   power guard are in **genuine tension**: buying convergence with run length
   costs run-to-run stability, which costs power.
2. **The arm with the harder curriculum pays most.** JOINT trains on 2
   all-elements-co-active components; ISO on 6 single-element ones. JOINT had
   further to travel at T = 500 (3.17× vs 1.06×) and its floor grew 5.2× vs
   2.1×. The ordering is consistent with the mechanism.
3. **The T = 500 ordering inverted.** At T = 500 JOINT was the *tighter* arm
   (0.0093 vs 0.0165); at T = 1000 it is the *looser* (0.0483 vs 0.0339). **No
   argument available before the measurement would have predicted which arm
   was noisier** — which is the per-artifact rule's whole point, now
   demonstrated twice with opposite signs.

**This is an environment-native finding, not merely a protocol nuisance**, and
it holds regardless of how Γ eventually lands. It is a statement about the
training dynamics this environment induces.

---

## 6. RAISED FOR RULING, NOT ACTED ON — the power formula assumes equal variance

`m62_report.py` computes power **per arm** as `σ√(2/k)`. That is the
**equal-variance** form. Γ = mean(JOINT) − mean(ISO), whose standard error is

    sd(Γ) = √( (σ_iso² + σ_joint²) / k )

With the measured floors the three quantities are:

| basis | power @ 0.03, k = 34 | k for 80 % |
|---|---|---|
| per-arm, ISO (0.0339) | 92.1 % | 25 |
| per-arm, JOINT (0.0483) | **62.8 %** ← what the guard grades | 50 |
| **combined variance** | **76.7 %** | **37** |

The per-arm reads **bracket** the true value; neither is Γ's power. **The
project adopted per-artifact floors precisely because the two arms differ in
stability, then retained a power formula that assumes they do not.**

**The STOP is unaffected** — 76.7 % is also below 80 %, so the guard fires on
either basis and the verdict in §1 stands. **The remedy is affected**: k = 37
versus k = 50.

**Not decided here.** The statistics freeze permits revisiting power machinery
only when a registered guard fires, and one has — but k is a human ruling, and
so is which basis grades it. Both numbers are recorded so the ruling can be
made on the arithmetic rather than on a recollection of it.

---

## 7. What was run, and what was not

**Cut at 17 of 24 runs** for a mains outage at the operator's site. The box was
remote and unaffected; this was a decision about *access* to the instance, not
a loss of running work.

- **ISO 8/8 and JOINT-classic 8/8 completed before the cut.** Both
  confirmatory arms are whole, so **the verdict is unaffected** by the
  truncation.
- **The sweep p = 0.5 arm stopped after rep 1.** It is secondary and
  non-verdict-bearing (design v2 §2). **No sweep floor is reported.** If one is
  wanted later it is 8 runs ≈ $1.50, and it should be re-measured on whatever
  card runs the grid in any case, since floors are per-hardware.
- **`provenance.txt` was captured by hand.** The job script writes it only on
  completion, so a cut run would otherwise have produced none. It records GPU,
  Python 3.12.3, jax/jaxlib 0.11.0 and devices.
- **The plateau/power analysis was run off-box** on the pulled artifacts, for
  the same reason: the analysis step executes after all 24 runs.

**Measured cost:** train median **668 s**, eval median **18 s** (n = 18 each) →
**686 s/run** at T = 1000. Against the 557 s/run extrapolated from M6.2, i.e.
**23 % higher**, because this card measured ~52,000 env-steps/s against the
~60,900 implied by M6.2's box. **Floors are per-hardware facts and this is the
card they were measured on** — the grid must run on the same card, or its
floors must be re-measured there.

Spend: ~17 runs ≈ 3.3 GPU-h ≈ **$3.30**.

---

## 8. Artifacts

- **16 confirmatory checkpoint archives pulled and sha256-verified against the
  box before release: 16 OK, 0 mismatched.** Gitignored; hashes in
  `SHA256_CKPT.txt`, which is committed.
- Committed: 16 metric `.jsonl` (1000 rows each), 16 `eval_*.json` + `.npz`,
  `floors.json`, `plateau.json`, `power.json`, `verdict.txt`,
  `provenance.txt`, `timings.txt`, `SHA256_CKPT.txt`, `m62b_console.log`, and
  the single completed sweep rep.
- The toolchain was **pinned deliberately** this session: jax 0.11.0 to match
  what M6.0 certified traced-θ bitwise on and M6.2 measured under. `uv.lock`
  had pinned 0.10.2 since 2026-07-18 and bound no run, on any machine; the
  interpreter version was the real determinant and nothing recorded it
  (`docs/decision_log.md`, *TOOLCHAIN PINNING*).

---

## 9. What this hands forward

**Settled:**

1. **T = 1000 converges both confirmatory arms.** The plateau branch of the
   T\* criterion is satisfied.
2. **The T = 500 floors are dead**, as the ruling said they would be. These
   replace them — for this card.
3. **Floor growth with run length is real, uneven, and ordered by curriculum
   difficulty.** Environment-native; belongs in the paper.

**Open, and owed to a human ruling:**

1. **k**, because the power guard fired. 80 % needs **k = 37** (combined
   variance) or **k = 50** (registered per-arm basis).
2. **Which basis grades Γ's power** (§6).
3. **Budget.** At this card's 686 s/run the grid costs ≈ **$43.70** at k = 34,
   **$44.85** at k = 37, **$49.83** at k = 50 — against a stated $40. The
   registered grid already exceeded it before any re-ruling; the re-ruling is
   not what created the gap.

**Not owed, and deliberately not done here:** T\* is **not** registered in
`docs/locks.yaml`. Its slot remains `value: null` with `owed_by` set. The
plateau branch passed, but step (b) STOPped on power, so the criterion's
conditions are not jointly met and writing 1000 into the registry now would
convert a criterion into an assumption.

---

## ADDENDUM 2026-08-03 — the STOP is discharged; this report is not revised

**Everything above stands as measured and is deliberately left unmodified.**
It records the constants of its own era — `K_CONFIRMATORY` = 34, the per-arm
power basis — and a report that correctly states what it was computed with
must not be retro-fitted to a later ruling. What follows is what the human
ruled *on* these numbers, not a correction *to* them.

Ruling: `docs/decision_log.md`, **M6.2b CLOSE-OUT — CERTIFY** (2026-08-03).

**1. The variance question in §6 is answered: the combined form.** Contrasts
are graded on the contrast's SE. The per-arm form is superseded for
contrasts, and `CLAUDE.md`'s power rule carries the amendment.

**2. k = 40** confirmatory (20 secondary). On these floors the combined basis
gives **83.7 %** power@0.03 — above the registered 80 %, whose bare minimum
is k = 37 (unrounded 36.60). The extra 3 seeds are margin against the 7-dof floor CIs §2
flagged.

**3. §6's numbers reproduce exactly under the new instrument**, which is why
they could be ruled on directly. Re-run on `floors.json` at k = 34: per-arm
JOINT **62.8 %**, **contrast 76.7 %**, `_k_required` **37** — all three
identical to §6. (§6's ISO 92.1 % and §4's 92.2 % are one number, 92.15 %,
rounded two ways.) At k = 40 the per-arm diagnostic reads 95.8 % / 70.7 %.

**4. T\* = 1000 is now registered** in `docs/locks.yaml` with this report's
plateau provenance. §9's reasoning for withholding it was right at the time —
the power branch was open. The close-out discharged that branch, so the
criterion's conditions are jointly met and the value enters *measured*.

**5. The floors above do not grade the grid's confirmatory test.** They were
measured as 8 identical reps at **one seed**, i.e. run-to-run nondeterminism,
while the grid averages over k **distinct** seeds. The confirmatory test and
CIs therefore use the grid's own measured seed dispersion; these floors keep
two narrower roles — the beat-reproducibility hurdle, and a design-stage
power basis that is now registered as an **UPPER BOUND**. The 83.7 % above is
a ceiling, not an estimate.

**6. These floors also do not grade the grid's card.** Per-hardware and
per-artifact both apply, and no box is running. A launch batch of 8 × ISO +
8 × JOINT + 8 × sweep (24 runs ≈ $4.57) re-measures them on whatever card the
grid rents, and a pre-registered ladder resolves the outcome without a human
round-trip unless survival power also collapses. The sweep reps also close
§7's missing p = 0.5 floor.
