# M6.0 Spike Report — per-env traced theta, for the Phase-6 entry gate

**Status: all four acceptances met.** Authorized pre-gate by the M6.0 ruling
(human, 2026-08-01; `docs/decision_log.md`), which exists because the
Phase-6 design v1 red team found that **the mixture machinery its §1 depends
on did not exist**, and that theta was a compile-time constant rather than
data. The gate can now register §1 against a demonstrated mechanism and a
measured cost.

Card: **RTX PRO 6000 Blackwell (97,887 MiB)**, jax/jaxlib 0.11.0, CUDA 12.8,
default XLA flags (autotuning ON — never set `--xla_gpu_autotune_level=0` on
this workload). All GPU rows were measured in **one session on one card**.

---

## 1. The headline for the gate

| question | answer |
|---|---|
| Can theta be per-env traced and sampled from a mixture? | **Yes**, end to end. |
| Did it change environment behaviour? | **No** — bitwise, 1520 field digests. |
| What does it cost in throughput? | **≤ 0.62 %**, and below the instrument's own jitter on the spending config. |
| What does it cost in memory? | **+30,720 B** peak (+0.00004 %). |
| Does the mixture actually realize its weights? | **Yes** — 0.7425 vs 0.75 declared over 6,400 episodes (z = −1.39). |

**The precompiled-variant fallback is not needed.** Its granularity cost —
per-*update* rather than per-*episode* mixing, so every env in an update
shares a component and PPO's advantage normalization sees a homogeneous
batch — can be dropped from the design.

---

## 2. Acceptance 2a — bitwise regression (the safety proof)

`che/tests/golden/theta_golden.json`, generated on main **before** any part
of the refactor landed, per the ruling's ordering constraint.

**CPU, both modes: 1520 field digests — 0 changed, 0 missing, 6 added.**
The six are exactly the fields declared in `ALLOWED_NEW_FIELDS`
(`state.theta_live.{beta,kappa_A,kappa_B,delta}`, `state.mixture_component`,
`info.mixture_component`). Re-run and still green after M6.0c added the
mixture, because the categorical draw takes its own `fold_in` stream
(`_MIXTURE_STREAM = 59`).

### Two corrections made mid-flight, both recorded because they matter

**(i) A lumped digest cannot express "a field was added" — and this refactor
adds fields.** The first golden hashed each trajectory into two blobs. Under
that format acceptance 2a would have failed on the very refactor it exists to
certify, for a reason that is not a regression, and the pressure would then
have been to relax the criterion. Fixed on clean main *before* the refactor
landed (the only cheap moment): one digest per field, so pre-existing fields
stay strict while additive growth is acknowledged by name.

**(ii) A pre-existing jit/nojit divergence, found and localized before the
refactor rather than during it.** `info.survival_rate` on severity_high
differs by exactly **one float32 ULP (5.96e-08)** from t = 29, where
`alive.mean()` reassociates once the first agent dies and the mean stops
being exactly 1.0. Trajectory fields agree 20/20 across modes. Had this
surfaced after the refactor it would have been misattributed to traced theta
and spent the ladder's localize-to-an-op branch on a metric artifact.

### GPU arm of the ladder — and the floor rule earning its keep again

Per the ratified ladder the same-code GPU rerun floor was measured **first**.
What followed is the most instructive part of the spike, because the first
answer was wrong in a way only the floor discipline caught.

**Step 1 — floor on the baseline tree: exactly 0.** Two independent baseline
runs, then three more against the same reference: **0 differing field digests
out of 760, in 4 of 4 comparisons.** By the ladder, a zero floor means any
traced-vs-folded difference is *real*, and the localize-to-an-op branch
applies rather than a tolerance.

**Step 2 — traced vs baseline: 2 fields changed.** `info.masked_frac` and
`info.masked_danger_sum`, on severity_high seed 0 only. **No trajectory field
moved** — state, obs, reward, done and actions were identical everywhere.
Read against a zero floor this looked like a genuine traced-vs-folded
difference in two Coupling-B diagnostics.

**Step 3 — direct localization found nothing.** Re-running that exact case
and dumping per-step values gave **identical float32 bit patterns, identical
visibility planes, identical values** — max |Δ| = 0.0 on both channels. A
result that contradicts step 2 unless the difference is intermittent.

**Step 4 — repeat both arms.** Traced vs baseline differed in **2 of 5**
comparisons. Baseline vs baseline: **0 of 4**. Two deterministic trees cannot
produce an intermittent comparison, so one of them had to be unstable.

**Step 5 — the decisive arm: traced against ITSELF.** **1 of 4** comparisons
differed, on **the same two fields, the same case**.

**Resolution: the difference is the traced tree's own run-to-run GPU
nondeterminism, not a traced-vs-folded semantic difference.** And the reason
step 2 misread it is worth stating plainly, because it generalizes:

> **The floor must be measured on the artifact being graded, not on its
> reference.** The floor was measured on the *baseline* tree, which is
> deterministic — so it read zero and made a difference inside the *traced*
> tree's own noise look like a real effect. Floors are per-metric and
> per-hardware (CLAUDE.md); this adds **per-artifact**.

Graded against the correct floor — the traced tree's own rerun floor, which
is **nonzero on exactly those two channels** — the traced-vs-folded GPU
comparison is **within floor**, and the trajectory is bitwise.

| comparison | n | differed | fields |
|---|---|---|---|
| baseline vs baseline (same code) | 4 | **0** | — |
| traced vs traced (same code) | 4 | **1** | `masked_frac`, `masked_danger_sum` |
| traced vs baseline | 5 | **2** | same two |
| **any trajectory field, any comparison** | 13 | **0** | — |

**What is and is not claimed.** The instability is confined to two
Def.-2-compliant diagnostics that no kernel reads, on one severity/seed, and
it did not reproduce under direct measurement, so **its magnitude is not
bounded** — the one time it was measured directly it was exactly zero.
Baseline showed no instability in 4 comparisons and traced showed it in 1 of
4; at those sample sizes **the difference in rates is not established**, so
this is *not* claimed as a regression introduced by the refactor. Mechanism
is consistent with float-reduction order in `masked_fraction`
(`where(alive, per_agent_masked, 0).sum() / max(alive.sum(), 1)`, over a mean
across each 9×9 crop) — the same signature as the pre-existing
`survival_rate` ULP finding. **CPU is unaffected: 0 changed across every run,
both modes.**

**OPEN ITEM for the gate.** Any Phase-6 metric graded near its floor should
either avoid these two channels or carry a measured per-artifact floor for
them. Neither is verdict-bearing in the current design.

---

## 3. Acceptance 2b — nesting suite green, unmodified

`che/tests/test_nesting.py` is byte-identical to its pre-spike state
(`git diff` empty) and passes 7/7. The nesting guarantee is *strengthened* by
tracing: a traced probability cannot be constant-folded away even when it is
exactly zero, which is the mechanism invariant #3 rests on.

---

## 4. Acceptance 2c — the DCE tax, measured paired

A tax is a **difference**, so it was measured paired: same card, same
session, same instrument, same toolchain. Cross-rental comparison would not
do — the Phase-5 report records the same config measuring 24.69 and 27.53
GiB on two rentals from a jax/jaxlib change alone.

**Keep-alive set (standing throughput rule):** population-aggregate
*training* throughput from `pbt.bench_population`; the compiled chunk returns
the training metrics dict, blocks on `total_loss`, and `mean_return` is
consumed host-side for selection. **Env `info` channels are not read by this
consumer**, so diagnostic-channel cost is outside this figure by
construction.

`reference.yaml` is **deliberately not a row** — it is archival, and quoting
it is the row-A error class that has bitten this project three times.

| row | baseline (folded) | traced | Δ | traced + real mixture | Δ |
|---|---|---|---|---|---|
| gate, elements ON | 60,037 | 59,966 | **−0.12 %** | 59,839 | **−0.33 %** |
| gate, elements OFF | 59,776 | 59,795 | +0.03 % | — | — |
| grid single-policy, ON | 70,580 | 70,674 | +0.13 % | 70,578 | −0.00 % |
| grid single-policy, OFF | 71,228 | 70,787 | **−0.62 %** | — | — |

steps/s, median of 3×15 s windows after a discarded warm-up.

### What the numbers mean, stated at the precision the instrument supports

**The largest paired difference anywhere is 0.62 %.** That is an **upper
bound**, not a point estimate, and the distinction is load-bearing:

- On the **gate config — the spending consumer** — the differences
  (−0.12 %, +0.03 %, −0.33 %) are **smaller than the within-run window IQR**,
  which reaches 0.72 % of median (434/60,037) on the baseline gate row. Not
  resolvable.
- On the single-policy rows the window IQR is tiny (0.003–0.07 %), and there
  the −0.62 % at elements-OFF **is** resolvable. The asymmetry is physical:
  at population 12 the card is saturated enough to hide a small extra op.

**FLOOR NOT MEASURED — flagged, per bars-with-floors.** Window IQR measures
jitter *within one compiled process*. It is **not** a run-to-run
reproducibility floor, which would need N independent re-runs across
recompiles, autotune choices and allocator state. No such floor was measured
for throughput here. The honest claim is therefore **"the tax is bounded
above by ~0.6 %"**, not "the tax is 0.12 %". A point estimate would be a
threshold finer than its instrument.

### The reason the tax is so small — and it is visible in the baseline alone

**Elements-OFF is not faster than elements-ON even in the pre-refactor
tree** (59,776 vs 60,037 on the gate; 71,228 vs 70,580 on grid). So XLA was
never deleting much: the seeding and masking work it *could* fold away is a
tiny share of a training step. The Phase-5 report measured the same structure
from the other side — the comms axis costs 2.9 % of *env-only* throughput but
~0.2 % of *training* throughput, because the env is a small fraction of a
step. The ruling's hypothesis that a mixed batch pays a permanent DCE tax
everywhere is **correct in mechanism and negligible in magnitude**.

### Memory

Peak device bytes: baseline **72,209,814,528** → traced **72,209,845,248**,
i.e. **+30,720 B (+0.00004 %)**, identical across all rows. The mixture adds
four scalars and an int32 per env; nothing changes shape.

### Cross-check on the whole setup

The baseline gate row measures **60,037 steps/s** against the Phase-5 record
of **62,084 steps/s** for the same config — **3.3 % apart on a different
rental with the same jax version**, consistent with the toolchain drift that
report documents. These numbers are comparable to the existing record.

---

## 5. Acceptance 2d — 50-update smoke train on a 2-component mixture

`severity_medium.yaml` wrapped in {pillar 0.25 (κ_A = κ_B = δ = 0),
joint 0.75 (the config's locked theta)} — chosen so the two components differ
in **all three elements at once**, and a bug dropping any one of them would
show.

| quantity | value |
|---|---|
| declared weight (joint) | 0.75 |
| **realized weight (joint)** | **0.7425** |
| finished episodes | 6,400 |
| binomial sd / z | 0.0054 / **−1.39** |
| **verdict** | **MATCH** (\|z\| < 3) |

The mixture drives **training**, not merely `reset`: per-episode component
labels ride the `EP_METRICS` path, done-masked exactly like every other M1.4
episode metric.

**Instrument bug caught before it reached the GPU.** The first version
computed the realized ratio as a mean of per-update means, over updates that
finish different numbers of episodes — weighting a 1-episode update equally
with a 40-episode one. That is precisely the error the M4.4 danger-moment and
M5.0 comms channels are structured to avoid, and the CPU dry-run exposed it.
It now pools numerator over denominator, exact given what is logged, with the
NaN mask applied jointly so the two series cannot misalign.

**Limitation, stated rather than discovered later:** a mean over component
*indices* only reads as a mixture ratio for **two** components. Phase 6's
four-component design needs per-component counts — a logging change (one
channel per component, or a one-hot sum), not a mechanism change.
Deliberately outside the spike's 2-component scope fence.

---

## 6. What the refactor changed, and what it caught

**Behavioural change, pinned rather than left latent:** theta now binds at
**reset**, not at step time. A mid-episode `dataclasses.replace(cfg, theta=…)`
is silently inert — unavoidable, because a mixture must give different envs
different theta inside one batched step, which a per-call config cannot
express. `che/tests/test_traced_theta.py` asserts it in both directions.
**Production is unaffected and that is asserted too:** every CLI theta
override (`--kappa-a`, `--kappa-b`, `--delta`, `--r-comm`) is applied in
`main()` before any reset, verified across `ippo.py`, `harness.py`,
`render_episode.py`.

**`zeros_state` now requires `theta_live`, and that deliberate choice paid
immediately.** It turned four `test_coupling_b` sites into loud failures
where a default-theta state was being stepped against a `kappa_B = 1.0`
config. Three were failing tests; the fourth
(`test_danger_channels_are_zero_without_fire_and_at_kappa_b_zero`) was
**passing for the wrong reason** — asserting `masked_danger_sum == 0` while
Coupling B was silently disabled. A convenience default would have kept it
green and meaningless.

**Scope fence held.** `sigma_s`/`eta` stayed static: they feed
`observation.plane_scales` → the uint8 quantization scales, whose reciprocal
is folded **on the host** precisely because fp32 division is not correctly
rounded on the GPU backend (M5.1h). Verified during the spike that
`plane_scales` does **not** depend on `kappa_B`, so the uint8 path is
untouched by the mixture as scoped.

---

## 7. Artifacts and provenance

Archived off-instance before release, sha256 verified end-to-end:

| archive | sha256 |
|---|---|
| `m60_artifacts.tar.zst` (2c + 2d) | `153bb9c3bb22715b8a0a0640f728110e2a6634811e19cd58d542d47d466959bd` |
| `m60_gpu_artifacts.tar.zst` (GPU ladder) | `35f93aafddb5aa3330b779f6cbbaf3e0573f779324e9169df6ddad513bd03ad4` |

Per-file sums in each archive's `SHA256SUMS.txt`, all `OK` on re-verification
locally after transfer.

**No checkpoint archive, stated explicitly rather than silently skipped:**
the spike produced no result-bearing checkpoint. The 2d run is a 50-update
smoke train whose purpose is the realized-ratio audit, not a policy, and it
was run with `ckpt_dir=None`. The artifact-persistence rule's checkpoint
clause has nothing to bite on here; metrics and provenance are archived as
required.

---

## 8. What this changes for the gate docket

**Removed (now answered by measurement):**
- *Is the §1 treatment implementable?* Yes, per-episode, no fallback needed.
- *What does it cost?* ≤ 0.6 % throughput, +30 KB memory — below the noise
  on the spending config.
- *Precompiled-variant fallback and its granularity cost.* Moot.

**Newly owed, surfaced by the spike:**
- **Per-component count logging** before any ≥3-component design is
  registered (§5 limitation).
- **A run-to-run throughput floor**, if the gate ever wants a *point*
  estimate of the tax rather than the upper bound recorded here.
- **A per-artifact floor for `masked_frac` / `masked_danger_sum` on GPU**, if
  either is ever graded near its floor (§2, GPU arm). Neither is
  verdict-bearing in the current design.
- **A candidate amendment to the bars-with-floors rule**: floors are
  per-metric, per-hardware **and per-artifact** — measuring the floor on a
  reference rather than on the thing being graded is what made a
  within-noise difference read as a real effect here. Human ruling owed on
  whether that goes into CLAUDE.md.

**Unchanged and still owed** — the red team's findings stand and are not
touched by this spike: the floors at the evaluation severities, the seed
count, the estimand and its fixed-margin confound, and the siting of θ\*
where both couplings are live.
