# G1.2 — the launch batch: BRANCH A on power, **STOP on run length**

**Date:** 2026-08-10. **Tree:** `ff92da7`. **Card:** NVIDIA RTX PRO 6000
Blackwell Workstation Edition (97,887 MiB, driver 595.58.03, 500 W cap),
Python 3.12.3 / jax 0.11.0. **24 runs, 3 arms × 8 reps, T = 1000.**
Wall clock 3h27m. Artifact assertion passed: 24 archives, 24 hashes.

**Two results, and they point in opposite directions.** The power ladder
resolves to **BRANCH A** with enormous surplus. The plateau guard **STOPs**.
Both come from the same cause.

## Measured floors (per-arm sd over 8 identical reps — nondeterminism)

| arm | completion | survival_rate | episode_return | deaths_fire |
|---|---|---|---|---|
| iso | 0.0214 | 0.0156 | 0.7421 | 0.1912 |
| joint | 0.0236 | 0.0119 | 0.7525 | 0.1409 |
| **sweep_p500** | **0.0245** | **0.0082** | **0.7771** | **0.1054** |

**The sweep arm has a floor for the first time.** M6.2b's sweep run was cut to
1 rep by a mains outage, which is the arm that exposed the silent-false-pass
defect (`NaN > PLATEAU_PASS` → False → rendered as passing). All three arms
here report `graded: true`; the defect path is not reached.

## Plateau guard — final-100-update slope, floor-graded

| arm | drift over last 100 | floor sd | ratio | verdict |
|---|---|---|---|---|
| iso | +0.01202 | 0.02142 | **0.56×** | plateaued |
| joint | +0.02411 | 0.02363 | **1.02×** | STILL CLIMBING |
| sweep_p500 | +0.02795 | 0.02449 | **1.14×** | STILL CLIMBING |

**VERDICT: STOP — still climbing at 1000 updates: `['joint', 'sweep_p500']`.
Run length must be re-ruled.** This is the registered criterion, binary at
`PLATEAU_PASS = 1.0`. Not self-extended; `T*` escalation is a human ruling.

## Why it STOPped, decomposed — and it is NOT that training got worse

M6.2b recorded its drift directly (`m62b/plateau.json`), so this is measured
against measured, not back-computed from rounded ratios.

| arm | quantity | M6.2b card | this card | change |
|---|---|---|---|---|
| **joint** | drift over window | 0.027587 | 0.024113 | **−12.6 %** |
| | floor sd | 0.048265 | 0.023631 | **−51.0 %** |
| | **ratio** | 0.5716 | 1.0204 | **+78.5 %** |
| **iso** | drift over window | 0.003384 | 0.012021 | **+255 %** |
| | floor sd | 0.033870 | 0.021417 | **−36.8 %** |
| | **ratio** | 0.0999 | 0.5613 | +462 % |

**JOINT's absolute residual drift went DOWN 12.6 %.** It crossed the threshold
because its floor **halved**. The plateau guard is a ratio test with the floor
in the denominator, so a more reproducible card makes it strictly harder to
pass at constant drift.

ISO is a different story — its drift genuinely grew 3.55× — but it still
passes at 0.56×, so it does not contribute to the STOP.

### The reading that matters: this is a NEW TRUE FINDING, not an artifact

The tempting conclusion is "the guard is miscalibrated, a quieter card
shouldn't cause a STOP." **That reading is wrong, and the opposite one is
correct.**

The guard asks: *is the residual drift distinguishable from run-to-run
noise?* Scaling by the arm's own floor is the right way to ask it. On a
quieter card, smaller drift becomes resolvable — so "still climbing" here is
a **true statement that the M6.2b card was not sensitive enough to make**.
JOINT's drift of ~0.0276 was present at M6.2b and sat under a floor of
0.0483; it was there the whole time and could not be seen.

**Therefore M6.2b's plateau PASS should be read as an underpowered null.** It
was a failure to detect drift, not a demonstration of its absence — the exact
distinction `CLAUDE.md`'s newest law was promoted for today
(*instruments state what they are blind to*). The certification that rested on
it (`T* = 1000`) is the thing now owed a re-ruling.

**This is reported, not acted on.** Whether `T*` moves, and to what, is a
human ruling. No run length is self-extended here.

## Power ladder — BRANCH A, with large surplus

Contrast basis, `k = 40`, Šidák `m = 2`:

| contrast | sd(Γ) | MDE80 | power@0.03 | k_req |
|---|---|---|---|---|
| Γ completion | 0.00504 | 0.0155 | 100.0 % | **11** |
| Γ survival_rate | 0.00310 | 0.0095 | 100.0 % | **5** |

**`RE-FLOOR LADDER: BRANCH A` — proceed at k = 40, surplus recorded
(k_req = 11).** Against `K_LADDER_CAP = 60` this is not close.

### The same cause, two opposite-signed consequences

The floor shrinkage that **tightened** the plateau guard **loosened** the
power requirement — the floor is the *denominator* of the plateau ratio and
the *numerator* of sd(Γ). One card property, two effects in opposite
directions. Worth stating plainly because reading either result in isolation
gives a misleading picture of what this card did.

## Measured cost — discharges the design-v2 §6 estimate

| | |
|---|---|
| train | median **485 s** (n = 24) |
| eval | median **12 s** (n = 24) |
| **per run** | **497 s** |

Against the **686 s/run** the $45.73 grid authorization was derived on. This
measurement supersedes the 686 s basis and the earlier extrapolation in
`g1_0b_throughput_ab.md`.

**THE RATE, MEASURED RATHER THAN ASSUMED.** This instance billed at
**$1.2358/h** (`vastai show instances`, id 47454262), not the **~$1.00/h**
the decision log carries for a PRO 6000 (2026-07-30 hardware-split entry).
Using the assumed rate understates every projection by 24 %, so the rented
rate is what is recorded here:

| | at assumed $1.00/h | **at measured $1.2358/h** |
|---|---|---|
| 240-run grid (33.1 h) | $33.1 | **$40.9** |
| re-run of this batch (3.3 h) | $3.30 | **$4.08** |

**The grid still comes in under the $45.73 authorization — by ~$4.8, not by
the ~$12.6 that the $1.00/h assumption would suggest.** The saving is real
but roughly a third the size, and it comes entirely from the faster card
(497 vs 686 s/run), which the run-length ruling may erase: **any increase in
`T*` scales the train component (485 s of the 497) linearly.** At T = 2000
the grid would be ~$80 and outside the authorization entirely.

**Caveat that must travel with the 497 s/run:** it is on **this card**, and
the card was released the same day. See below.

## Consequence of releasing the box

Floors are per-hardware. **These floors do not grade a grid run on a
different card**, and the grid was not run today (owner's call, 2026-08-10).
The next trip therefore needs G1.2 re-run before G1.3 — at the measured rate
that is 24 × 497 s ≈ **3.3 h ≈ $4.08**, against **$1.2358/h** to hold this
box idle. Releasing is correct for any resumption gap beyond ~3.3 hours, and
the instance was destroyed (id 47454262) once every artifact was retrieved
and hash-verified.

**What survives the release, card-independent:**

- The **throughput A/B** is permanently discharged — "logging cost below
  ~0.25 %" is a property of the code, not the card.
- The **plateau finding above**, which is about the *relationship* between
  drift and floor and is the reason a `T*` ruling is owed. It does not expire
  with the card, though its exact ratios do.
- The **sweep arm's floor exists at all** for the first time.
- A realistic **cost basis** and a rehearsed procedure.

## Artifacts

`che/bench/results/phase6/g1_floors/` — 81 files committed (metrics, evals,
`floors.json`, `plateau.json`, `power.json`, `verdict.txt`, `provenance.txt`,
`SHA256_CKPT.txt`, `timings.txt`, console log). The 24 `ckpt_*.tar.zst`
(590 MB total) are gitignored per `.gitignore:268-269` and held off-instance
on the researcher's machine, as with M6.2b.

**Transfer verified:** `g1_floors.tar` sha256
`184f8fab85092edefa7bbc66e711355122d57d206c5f8ad078c8d154e3abe4dc`, identical
on box and locally; all **24 of 24** per-checkpoint hashes re-verified locally
against `SHA256_CKPT.txt` after extraction (`OK: 24  FAILED: 0`).

## Owed

1. **A `T*` ruling.** Two arms still climbing at T = 1000, one of them
   confirmatory. `DO NOT self-extend run length` — this is human.
2. **Re-read the M6.2b certification** in light of the underpowered-null
   reading above. `T* = 1000` is registered in `locks.yaml` with M6.2b
   plateau provenance; that provenance is now contested by a more sensitive
   instrument.
3. **Fresh floors on whatever card runs the grid**, per the per-hardware rule.
