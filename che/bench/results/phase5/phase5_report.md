# Phase 5 report

The communication axis: architecture, the Remark-2 VoC handshake, and the
δ lock. Phase-5 pre-flight produced four corrections to Remark 2 and three
new repo rules before a line of Phase-5 code was written; those are
recorded in `docs/decision_log.md` and `CLAUDE.md` and are not repeated
here except where a milestone measured what they deferred.

---

## Pre-task — Phase-4 replication (retrain-then-render)

Run from `0c612b6` on the GPU box, pre-authorized under the Q4 ruling.

The M4.4 checkpoints could not be re-rendered — the archive half of
"tooling rule 3c/3d" was never implemented, so the run that produced the
Phase-4 headline left no restorable artifact. The pre-authorized fallback
was to retrain the two High cells and render from the fresh checkpoints.

**What it found is not what it was run to find.** The replicate used the
*same seed* as the M4.4 original, so the two rows should have matched to
the bit. They did not:

| arm | metric | replicate | M4.4 | Δ |
|---|---|---|---|---|
| κ_B = 0 | completion | 0.8412 | 0.7905 | **+0.0507** |
| κ_B = 0 | survival | 0.9160 | 0.9408 | −0.0247 |
| κ_B = L | completion | 0.7773 | 0.8017 | −0.0244 |
| κ_B = L | survival | 0.8690 | 0.8721 | −0.0031 |

GPU training is not reproducible run-to-run at fixed seed: XLA autotunes
by timing and reductions land in nondeterministic order. The cross-arm
*effect* survives — survival −0.047 (replicate) vs −0.069 (M4.4), same
sign and rough size — but completion **flips sign**, +0.011 in M4.4
against −0.064 in the replicate.

Consequence, ruled at the M5.1 STOP: the Phase-4 survival claim stands;
the "completion intact" clause is **restated**, not retracted, as
unresolved at one run per cell. The correction note is in
`phase4/phase4_report.md`.

---

## M5.0 — Architecture + link kernel

`che/env/comms.py` implements T_K (Def. 7) at Prop.-1 position 5.

- **Hard range cutoff** (Q6 ruling): p = 1[d_Cheb ≤ R_comm]·(1 − δ). The
  former `p_link_max` multiplier is retired — it had no meaning under a
  hard cutoff and no config ever set it.
- **Directed links** with out-degree reporting. 0 < δ < 1 therefore
  permits asymmetric delivery, which is physically legitimate (fading is
  directional) and is documented rather than symmetrized away.
- **Unconditional PRNG consumption** (invariant #3): the [n, n] uniforms
  are always drawn, including the discarded diagonal, and compared
  against 1 − δ. δ = 0 recovers the deterministic range graph and δ = 1
  the empty graph, both bitwise, no branch.
- **Comms state is not carried in `EnvState`.** The deferred Phase-5
  design question resolved to: k′ is a function of x′ alone, so it is
  recomputed per step and returned in `obs["links"]` rather than stored.
- **Message head** (Q3 ruling, option (a)): `tanh(Dense(msg_dim))` off
  the trunk, stop-gradient on the message input. Messages are therefore a
  frozen-at-init random projection of *trained* trunk features. DIAL is
  pre-registered as M5.3 null-branch item #1 if the utility gate fails.

**Nesting verified bitwise.** `test_comms.py` pins a golden pre-M5.0
trajectory digest (`7f971393…a849c3230`); adding the comms axis left it
unchanged.

---

## M5.1 — Bench row, and the re-anchored gate

This milestone spent more session time than its scientific weight
deserves, and produced three findings anyway. All three were measurement
defects, not environment defects.

### M5.1a–b — the benchmark was measuring nothing

The first comms bench row came back **+3.1 % faster after adding work**.
That is not a plausible speedup, and the tell was believed rather than
explained away: XLA had dead-code-eliminated the entire comms kernel
because the probe never read `obs["links"]` or the new info counters. HLO
evidence: 1 tensor survived where 189 should have.

Re-measured with a probe that reads every channel: **8,630,698 →
3,390,689 steps/s (−60.7 %)**.

`test_bench.py` gained a regression test asserting that
`[n_agents, n_agents]` tensors survive compilation.

### M5.1c — "the env cost" is not a single number

The −59.5 % was initially reported as *the comms cost*. That was wrong
and is retracted here: it is the cost of the **keep-alive set**, and the
comms kernel is a small part of it. Decomposed by probe mode on the
64² / 1024-env / 12-agent reference cell:

| probe | median steps/s | vs legacy |
|---|---|---|
| legacy (M4.1's keep-alive set) | 8,608,593 | +0.0 % |
| + comms channels | 8,356,360 | **−2.9 %** |
| + everything training reads | 7,921,594 | −8.0 % |
| + everything eval reads | 3,386,909 | −60.7 % |

**The comms axis costs 2.9 % of env-only throughput on this cell** — and
~0.2 % of actual training throughput, since the env is a small fraction
of a training step (see the M5.1d table). The 60 % is what the
*evaluation* diagnostics cost, and evaluation is not what spends the
training budget.
This is what motivated the human's throughput rule (CLAUDE.md): under
DCE, an env-only figure is meaningless without its keep-alive set.

### M5.1d–h — the gate, re-anchored, and where it stopped

Per ruling 1b/1c/1d the ÷81 projection is retired; the guarded quantity
is directly measured population-aggregate training throughput.

- **Row A** (Phase-0 M0.6 config, today's code): **142,421 steps/s**,
  −10.4 % against the Phase-0 159.0 k. Peak device memory 22.78 GiB.
  This is a drift reference, not the gate — that config carries
  `obs_window` 5, superseded at M1.2.
- **Row B** (`gate_pop12.yaml`, the Phase-6/7 spending configuration):
  **did not compile.** Twice.

The first failure was obs storage: the float32 population obs trajectory
is 11.39 GiB and minibatching copies it. The pre-registered uint8
contingency activated (ruling 1c, mechanical) and cut that tensor 4×.

It failed again at **49.08 GiB**, with autotuning off and at a 95 %
memory fraction — a capacity number, not an allocator artifact. The
compile-only memory probe (`che/bench/memprobe.py`) priced every remedy
at once rather than discovering one layer at a time:

| candidate | peak GiB | changes |
|---|---|---|
| baseline | 49.31 | as committed |
| remat | 47.22 | recompute activations; same run |
| remat+nmb8 | 26.88 | + smaller minibatch (**changes optimization**) |
| nmb8 | 27.93 | smaller minibatch (**changes optimization**) |
| nmb16 | 18.66 | smaller minibatch (**changes optimization**) |
| pop6 | 24.66 | half the population (**changes the design**) |
| envs128 | 24.69 ⚠ | half the envs (fallback-ladder rung 2) |

⚠ **Corrected 2026-07-30 (M5.1j).** This 24.69 GiB is stale by 2.85 GiB.
The identical configuration measured **27.5349 GiB** when it was re-priced
as the committed baseline a day later, on the same card with the same
flags. See M5.1j below; the ladder choice does not change, the headroom
claim does.

**Nothing experiment-preserving fits a 31.8 GiB card.** My arithmetic had
predicted remat would roughly halve the requirement; it delivered 4 %.
The reason is in XLA's own log, which I had not read closely enough
before proposing it:

```
Can't reduce memory use below 28.31GiB by rematerialization;
only reduced to 37.92GiB, down from 55.00GiB originally
```

XLA was **already rematerializing aggressively**, so `jax.checkpoint` was
largely redundant with the compiler's own pass. That line also settles
the question independently of the probe: even under perfect
rematerialization the configuration needs 28.31 GiB, which is 89 % of the
card — and a config that needs 89 % of the card to compile is not a safe
operating point for a multi-run grid.

**Remedy: fallback-ladder rung 2, applied a second time** (delegated
ruling 2026-07-29, `decision_log.md`). This was initially parked as a
"scope decision"; it is not one. The pre-agreed ladder lives in
`phase0_substrate_prompt.md` — not in the Phase-5 prompt, which is why it
was missed on the first pass — and Phase 0 already applied rung 2 once,
moving 1024 → 256 envs/member for this identical reason. Rung
availability has since changed:

| rung | status |
|---|---|
| 1. grid 64²→48² | **unavailable** — β_c = 0.500 and the severities were calibrated at 64²; percolation thresholds are finite-size dependent |
| 2. n_envs tuning | **applied**: 256 → 128 (24.69 GiB, 78 % of card — ⚠ corrected 2026-07-30 to 27.53 GiB, **87 %**; M5.1j) |
| 3. n_agents 12→8 | **unavailable** — M5.4's R_comm band is defined at "12 agents, 64²" |
| 4. grid 48²→32² | same objection as rung 1 |
| 5. pop 12→10 | marked "M0.6 only" |

Rung 2 is the only live rung and the only one that moves no calibrated
quantity: the environment, the task and every locked θ are untouched.
`n_minibatches` 4→16 fits better (18.66 GiB) and was **rejected** — it is
not on the ladder and changes the optimization with no pre-agreement
about what that does to PBT selection, which is the band-shopping the
M4.3 precedent forbids.

Two consequences, recorded because the ladder requires it: Phase-6/7 runs
at this config need **1000 updates rather than 500** to preserve planned
experiment steps, and we are now **8× below the Phase-0 reference
n_envs** (1024 → 128) — a fact for the Phase-6 entry gate to weigh.
Row B is re-benched by `run_m51i_gate_rung2.sh`; **the 100 k line is not
renormalized**, and if the re-bench lands under it that is reported to
the entry gate, not fixed by another config edit.

Phase 5's own milestones do not use the population path.
M5.3–M5.5 are single-learner runs at the severity operating point, and
that path is healthy. Two figures, because they measure different things
and conflating them is easy:

| | M4.1 | M5.1 (comms live) | Δ |
|---|---|---|---|
| steady-state training rate (ippo's counter) | 68,598 | 68,475 | **−0.18 %** |
| wall clock, 500 updates | 276 s | 284 s | +2.9 % |
| implied one-time compile | 37.2 s | 44.7 s | +7.5 s |

The comms axis costs essentially **nothing** in steady state; the extra
wall clock is almost entirely one-time compilation of the new kernel.
Note that this is *not* the same as the reference cell's −2.9 %: that is
an env-only number, and the env is a small enough fraction of a training
step that a 2.9 % env cost dilutes to ~0.2 % of training. Which is
precisely the M5.1c lesson — the figure depends on the consumer, so the
consumer has to be named every time.

### M5.1e — the reproducibility floor

Four identical runs (Medium, dp 0.5, seed 0, 500 updates): this is
nondeterminism alone, not seed spread.

| metric | mean | sd | range |
|---|---|---|---|
| completion | 0.7381 | 0.0145 | 0.0319 |
| survival_rate | 0.9191 | 0.0129 | 0.0316 |
| episode_return | 23.1328 | 0.5026 | 1.1182 |

Falsifier condition (i) now reads "within the measured reproducibility
floor" and cites this study. **Caveat that bounds every use of it:** n = 4
gives an sd with 3 dof, itself uncertain by ~±40 %. It is an order of
magnitude, not a threshold to three decimals, and it describes the
*nondeterministic* regime only.

### M5.1h — fp32 division is not correctly rounded on GPU

The uint8 work shipped with two tests that passed on CPU and failed on
the box. Root cause was in the code, not the tests: `dequantize_grid`
computed `u8 × (scale/255)` with the division on device, and XLA's GPU
backend lowers fp32 divide to an approximate reciprocal, so a full-scale
code reconstructed as 0.99999994 instead of 1.0. The plane table's claim
that indicator planes round-trip exactly was false on the only backend
that matters.

Fixed by folding the reciprocal on the host in numpy and leaving a single
multiply on device — exact by construction rather than by luck of
rounding. The round-trip test now runs under jit as well as eagerly (the
failure was compile-only), and `test_dequantize_does_no_device_division`
inspects the lowered HLO so the property is guarded on any backend.

### M5.1i–j — the re-bench produced no rate, and the requirement had moved

**M5.1i (2026-07-29): row B was killed at the 1800 s backstop, `rc=137`,
no rate.** Three attempts have now produced three artifacts and no gate
number: an OOM naming 49.08 GiB, a bounded OOM after 1112 s retrying a
fixed 5.72 GiB allocation, and a bare SIGKILL. The last one carries no
diagnostic at all — `pbt.py --bench` is atomic from outside, so init,
compile, warm-up and the timing windows all fail identically.

**M5.1j (2026-07-30) found that the requirement itself had drifted.** Two
committed artifacts price a byte-identical configuration on the same card
with the same `--xla_gpu_autotune_level=0` flag:

| envs 128 / pop 12 / nmb 4 / uint8 / remat off | temp GiB | total GiB |
|---|---|---|
| `m51g/memprobe.json`, candidate `envs128` (fa32113) | 24.5467 | **24.6872** |
| `m51i/memprobe_rung2.json`, `baseline` (dbdb15c) | 27.3944 | **27.5349** |

**+2.8477 GiB, +11.53 %.** In the same pair, `jax.checkpoint` went from
saving 2.09 GiB to saving 5 KB (27.394371 → 27.394376 GiB), so what moved
is *activation retention*, not merely a level.

Three consequences, which is why this is a correction and not a footnote:

- The rung-2 ruling was taken on "24.69 GiB, 78 % of the card". At
  27.53 GiB it is **87 %** of a 31.8 GiB card. The ladder choice stands —
  rung 2 is still the only rung that moves no calibrated quantity — but
  the headroom claim attached to it was wrong.
- `run_m51i_gate_rung2.sh` sized `MEM_FRACTION=0.95` as "30.2 GiB for a
  24.69 GiB requirement", i.e. 5.5 GiB of slack. The real slack is
  2.7 GiB, 8.8 % of the arena, which BFC fragmentation can consume.
- `m51i/verdict.txt` concluded "rung 2 already cut the requirement 49.31 →
  ~24.7 GiB, so a failure here is about how the row is measured, not about
  whether the rung worked". Against 27.53 GiB that is **not established**;
  the failure may be capacity after all. The artifact is left unedited —
  run artifacts are immutable — and this section is the correction of
  record.

This is the ÷81 pattern one level down: a number measured once, written
into a config header and a ladder decision, then cited across two
milestones while the thing it measured moved underneath it.

**What the local CPU bisect settled, and what it could not.** Compile-only
probes on this CPU box, at reduced scale, cleared four candidate causes
outright:

| candidate | effect on compiled temp |
|---|---|
| M5.1h dequantize hunk reverted (divide on device) | **0.00 MiB** |
| `msg_mode` live / zeroed / shuffled (M5.3) | 0.14 MiB at probe scale, ~54 MiB scaled to gate |
| probe **order** within one process (`lru_cache` eviction) | **0.00 MiB** |
| candidate path vs baseline path, identical config | **0.00 MiB** |

The last two matter because m51g priced `envs128` as its 7th candidate and
m51i priced it as its 1st: the instrument is a deterministic function of
the config, so that is not the difference. CPU fusion is not GPU fusion,
so a null here does not clear a suspect on the box — M5.1h in particular
touches the differentiated forward path, where a multiply-by-literal and a
divide can fuse differently on GPU only.

Exactly two candidates survive: **GPU-specific fusion** from one of the
five commits between the runs, or a **toolchain change between two
rentals**, which no provenance file recorded. `memprobe.py` now writes
jax/jaxlib/backend/device into its JSON; comparing a memory requirement
across rentals without them is the env-only-throughput mistake in a
different unit.

**The instrument, not a fourth attempt.** `che/bench/rowb_probe.py` runs
the ladder `init → compile → one chunk → windows` in stages that print as
they go and **rewrite their JSON after every stage**, with device
`memory_stats()` at each one and on failure, so a kill leaves a trail
instead of a return code. `run_m51j_rowb_diagnostic.sh` wraps it with the
code-vs-toolchain 2×2 (HEAD and a fa32113 worktree, same box, same
session, module path asserted so it cannot silently resolve to today's
code), a 5 s sampler recording GPU memory / utilisation / host RSS — which
is what separates an allocator-retry loop from host swap from
slow-but-progressing — a `preallocate=false` contrast that names the
failing allocation, and a check that no leftover process from the three
killed attempts is holding the card.

**Scope, stated so it cannot drift.** Row B guards Phase-6/7 spending
only; no Phase-5 milestone uses the population path, and that path is
healthy at 68.5 k steps/s. The gate number is owed to the **Phase-6 entry
gate**. If M5.1j lands without a rate, the trail goes to that gate and row
B is not attempted again inside Phase 5. The 100 k line is not
renormalized and no experiment quantity is touched.

**Hardware split (human, 2026-07-30).** Phase 5 finishes on an RTX PRO
6000 Blackwell (96 GB, ~$1.00/h); Phase 6/7 spends on a 5090 (~$0.40/h),
because the required rate to keep 86e9 steps inside $150 scales linearly
with price — 71.7 k steps/s at $0.45/h against 239 k at $1.50/h — and two
same-generation cards will not differ by 3×.

That split changes what M5.1j is *for*. On a 96 GB card the gate config
simply runs, which answers nothing; so section 3 of the job caps XLA's
arena in GiB and walks it upward, and the first rung that runs is the
**minimum viable arena**. That is the number deciding whether Phase 6/7 on
a 5090 is feasible at all, and it is measured with a control arm on
identical silicon — something a 5090 alone cannot provide, because it can
only supply the failing half. It is an emulation of arena *size*, not a
5090 measurement, and it is labelled as such in the verdict.

The gate row itself still has to come from the 5090: CLAUDE.md binds
throughput gates to the spending consumer, and the verdict script detects
the device and refuses to compare a non-5090 rate to the 100 k line.

Three obligations follow, recorded in `decision_log.md`: the **M5.1e
reproducibility floor is card-specific and is re-measured** before M5.4/M5.5
run on the new card (M5.5's falsifier condition (i) cites it by name, and
grading against a floor from other hardware is the defect M5.1j just caught
one level up); **no comparison straddles cards**; and M5.3 stays closed on
the 5090, where its three arms were CRN-paired.

**Recorded unpriced, not implemented:** the remaining ladder rungs all move
calibrated quantities, and the off-ladder knobs change the optimization or
the design — but there is one option in the same class as `remat`
(mathematically neutral: same hyperparameters, same updates, same PBT
selection, trading wall clock for memory) that nobody has priced —
**evaluating the population vmap in G sequential groups**. From the
measured `pop6` candidate (13.77 GiB), two groups of six should peak near
13.9 GiB at roughly 2× the update-phase wall clock. That is arithmetic
from measured numbers and is **labelled an estimate**, not a measurement;
adopting it is a Phase-6-entry-gate decision.

### M5.1j results (2026-07-30, RTX PRO 6000 Blackwell, jax/jaxlib 0.11.0)

**Q1 — the requirement drift is the TOOLCHAIN; the five commits are
cleared.** Same box, same session, same flags:

| code | measured | card / date |
|---|---|---|
| fa32113 (m51g's tree) | 27.534881 GiB | PRO 6000, 07-30 |
| HEAD `cc53a4e` | 27.534886 GiB | PRO 6000, 07-30 |
| dbdb15c (m51i), for reference | 27.534882 GiB | **5090**, 07-29 |
| fa32113 (m51g), for reference | **24.6872 GiB** | **5090**, 07-28 |

Old and new code agree to five decimals today, and today's figure matches
m51i's *on a different GPU* to seven. Two cards agree; two dates do not. The
+11.53 % moved with the rental's toolchain between 07-28 and 07-29 — not
with our code, not with the device. `remat` tells the same story in a second
quantity: 2.09 GiB saved at m51g, +5×10⁻⁶ GiB today.

**Q2 — row B was never broken. The cause was our own instrument flag.**

| | compile | one chunk | rate | peak |
|---|---|---|---|---|
| `--xla_gpu_autotune_level=0` | 10.0 s | 1036.2 s | 3,795 steps/s | 27.53 GiB |
| autotuning **on** (default) | 101.8 s | 63.2 s | **62,186 steps/s** | **61.56 GiB** |

**16.4× apart**, reproduced three times at 1036.6 / 1036.2 / 1036.2 s and
twice at 63.2 s. The peak column is the whole history: the autotuner's
scratch is a **compile-time** requirement of ~61.6 GiB, so on a 31.8 GiB
5090 it cannot fit — *that* was m51d's "49.08 GiB" and m51i's 5.72 GiB
retry loop. We disabled autotuning to make it fit, which made it 16×
slower, then spent three attempts diagnosing the slowness we had
introduced, behind guards sized for the OOM we had removed. Every "hang"
was arithmetic proceeding correctly at an untuned convolution's pace.

Memory was never the constraint on *execution*: the 31.8 GiB arena and the
90.22 GiB full card both executed in 1036 s, with stage-one peak 27.53 GiB
in both — exactly memprobe's prediction.

**Q3 — the gate row: 62,084 steps/s (IQR 25)**, rates [62102, 62077,
62084]. Warm equals cold (62,186), so there is no amortization; that is the
steady-state rate. It is **below the 100 k line**, and it is **not on the
spending consumer** — CLAUDE.md binds the gate to the card that spends, and
the 5090 is now out (below).

### The budget was computed from the wrong configuration

| config | rate | GPU-h for 86e9 steps | @$0.45/h | @$1.00/h |
|---|---|---|---|---|
| row A — `m06_probe.yaml`, **obs_window 5** | 142,421 | 167.7 | $75 | $168 |
| **gate config — obs_window 9, autotune on** | **62,084** | **384.8** | **$173** | **$385** |
| gate config, autotune off | 3,795 | 6,294.8 | $2,833 | $6,295 |

The "86e9 steps → 167.7 GPU-hours, ~$151 with ×2 buffer" line came from row
A, which runs `m06_probe.yaml` at **obs_window 5** — superseded at M1.2. The
configuration Phase 6/7 actually runs carries obs_window 9, 3.24× the
observation volume, and measures **2.29× slower**. Phase 6/7 therefore needs
**384.8 GPU-hours, not 167.7**, against a $150–215 total budget.

**This was true before any hardware question and is not fixed by choosing a
card.** It is the ÷81 pattern a third time: a headline number attached to a
configuration that is not the one that spends.

### The 5090 is not viable at this configuration

Autotuning on needs ~61.6 GiB at compile against a 5090's 31.8 GiB → OOM.
Autotuning off fits, at 3,795 steps/s → 6,295 GPU-hours → $2,833. Both
fail, so the hardware split ruled earlier on 2026-07-30 (Phase 6/7 on a
~$0.40/h 5090) does not survive its own measurement. Even a 96 GB card
shows BFC pressure warnings during autotuned compiles, and the autotuner's
temp varied run to run (27.39 vs 28.26 GiB), so the requirement is not a
fixed number.

### Owed to the Phase-6 entry gate

Reported, not resolved here; the 100 k line is not renormalized:

1. The budget must be **recomputed at the real configuration**; the $151
   figure is retired.
2. Phase 6/7 needs either a card with ~62 GiB of compile headroom (~$1/h →
   $385) or a configuration that lets the autotuner fit a cheaper card —
   `n_minibatches` 16 prices at 9.36 GiB and sequential population groups at
   ~13.9 GiB, both untested against autotuner scratch.
3. Any future throughput figure **states its XLA flags**, exactly as the
   standing rule already requires a keep-alive set. A rate without its flags
   is not a measurement: 3,795 and 62,084 are the same code, same card, same
   day.

### M5.1k — the throughput levers do not exist

Run 2026-07-30, autotuning on, same card. Priced before cutting any
science, on the argument that a 1.5× throughput win is worth more than a
seed.

| lever | pop/envs/nmb | steps/s | vs baseline | $/run |
|---|---|---|---|---|
| baseline | 12/128/4 | **62,084** (IQR 46) | 1.00× | $0.88 |
| envs256_nmb8 | 12/256/8 | 60,492 (IQR 112) | **0.97×** | $0.90 |
| envs512_nmb16 | 12/512/16 | 60,044 (cold call only) | ~0.97× | — |

The baseline canary reproduces M5.1j **to the digit** (62,084 vs 62,084),
across an instance restart, so the table is trustworthy.

**The hypothesis is falsified.** It was argued from per-env efficiency —
40.4 steps/s/env here against 51.8 at Phase 0 (159,000 / 3072) — that part
of the gap was launch overhead and more concurrent envs would recover it.
Doubling and quadrupling them recovers nothing, and is marginally *worse*
both times. The whole gap is the 3.24× observation volume of obs_window 9;
this workload is compute-bound, and there is no free throughput win.

Two consequences: the fallback-ladder rung-2 application costs nothing in
throughput (n_envs 128 and 256 measure the same), and **the budget cannot
be fixed by engineering** — it is a scope question or nothing.

The remaining rows (`envs256_nmb4`, `nmb16`, `pop8`) were not run: the
instance stopped mid-sweep, and the two cleanest tests had already settled
the question. `pop8` is a scope cut rather than a throughput lever in any
case. Partial artifacts are in `m51k/`; the truncation is recorded here
rather than left as a silent gap.

**Where the budget actually stands.** At $1/h a 1000-update population run
costs **$0.88** and takes 53 min, so $200 buys 227 runs (113 with the ×2
buffer). The 86e9 envelope has **no bottom-up derivation anywhere in the
repo** — it appears in `phase0_substrate_prompt.md`, in `throughput.py` as
a constant, and in every report that cites it. A generous sketch of the
actual Phase 6/7 (5 configs × 4 seeds × 3 severities, plus 8 dose-response
points × 4 seeds) is 92 runs ≈ 81 GPU-h ≈ **$81**, or $162 with the buffer —
9 % of the envelope. **Decomposing the number is the entry gate's job and
should precede any cut**, because pricing a placeholder is how the $151
line survived three phases.

---

## M5.2 — ★ Remark-2 VoC validation ★ (theory §5 Remark 2′/2″/2‴)

**Claim under test.** Communication is load-bearing exactly when
perception fails *and redundancy is unavailable*. In the courier variant
of E_2C the free-comms arm sits at J = 1 for every κ_B, the denied arm
decays to the ½ memorization floor, and the gap — VoC — increases with
perception decay.

### Protocol

`che/env/e2c2.py`, engine shared with the `@slow` test and the figure
script (`che/scripts/plot_e2c2.py`). Geometry, (σ_s, η), the smoke-step
protocol, k and the shared `transmittance` are **imported from
`che/env/e2c.py`**, not restated — a divergence between the Theorem-1 and
Remark-2 figures has to be about comms, not about the arena
(`test_shares_the_theorem1_geometry`).

- **Courier variant** (Q1 ruling): only agent 0 can score; agent 1 scouts
  and cannot. Reward 1 iff the courier reaches the goal by T.
- **Horizon derived, not asserted** (Q2 ruling): the scout's report is
  worthless until it has walked *past* the fire depth, so the verdict
  lands at d + ℓ_f and **T = d + ℓ_f + ℓ = 8**. Remark 2's original
  T = d + ℓ + 1 is the ℓ_f = 1 case. The step the derivation rests on is
  pinned by `test_e2c.py::test_scout_dies_at_the_fire_anchored_step`.
- **Blinding** (Q6 ruling): the courier reads content planes only, never
  plane 6 (alive occupancy) and never plane 7 (the M4.2 side channel), so
  the scout's fate reaches it *only* as a message. Both are enforced by
  poisoning the plane and asserting bit-identical outcomes.
- **Delivery through the production Def.-7 kernel** — `in_range_mask` +
  `sample_links`, not a bespoke coin. M5.2 therefore doubles as a
  handshake for the comms kernel: if its range test or δ convention were
  wrong, the free arm would stop hitting 1.

### Results (4096 episodes / 8192 MC per point)

| κ_B | J_free | J_denied | predicted ½+q/2 | z | q | q̃ | VoC_gated | VoC_true |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 1.0000 | 1.0000 | 1.0000 | +0.00 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| 0.5 | 1.0000 | 0.9795 | 0.9800 | −0.22 | 0.9601 | 0.9917 | 0.0200 | 0.0042 |
| 1.0 | 1.0000 | 0.9053 | 0.9049 | +0.07 | 0.8098 | 0.9116 | 0.0951 | 0.0442 |
| 1.5 | 1.0000 | 0.8096 | 0.8102 | −0.10 | 0.6205 | 0.7495 | 0.1898 | 0.1252 |
| 2.0 | 1.0000 | 0.7339 | 0.7306 | +0.44 | 0.4612 | 0.5599 | 0.2694 | 0.2200 |
| 3.0 | 1.0000 | 0.6135 | 0.6118 | +0.22 | 0.2235 | 0.2776 | 0.3882 | 0.3612 |
| 5.0 | 1.0000 | 0.5281 | 0.5249 | +0.40 | 0.0498 | 0.0503 | 0.4751 | 0.4749 |
| 8.0 | 1.0000 | 0.5034 | 0.5018 | +0.21 | 0.0035 | 0.0057 | 0.4982 | 0.4971 |

**Acceptance: all three conditions green.**

1. Gate on the pinned (protocol-matched) arm: max |z| = 0.44 ≤ 2.69;
   joint χ² = 0.51 on 8 dof, p = 1.000 ≥ 0.05; |mean z| = 0.13 ≤ 0.71.
2. Free arm ≥ 0.99 at every κ_B — in fact exactly 1.0000 everywhere.
3. VoC monotonically increasing, 0.0000 → 0.4982, no decrease anywhere.

**A note on that χ².** Σz² = 0.51 where 8 is expected is a *suspiciously
good* fit (p ≈ 7×10⁻⁴ in the lower tail), which is the classic signature
of overstated standard errors — a gate that would not catch a real
defect. Rather than accept a pass on trust, the z distribution was
measured directly (16 seeds × 5 κ_B points, `e2c2_replicates.json`):
**pooled mean z = −0.205, sd = 1.133, 8.7 % beyond 2σ.** The SEs are
sound and if anything mildly conservative, so the gate is calibrated and
the headline sweep was a lucky draw. Recorded because a pass obtained by
not looking is not a pass.

### Remark 2‴'s deferred constants, now measured

Remark 2‴ struck the chat-heuristic claim q̃/q → 5/3 and deferred every
constant to this milestone. The analytic ratio (exact, no MC noise):

| κ_B | 0 | 0.25 | 0.5 | 1.0 | 1.5 | 2.0 | 3.0 | 5.0 | 8.0 | 16 |
|---|---|---|---|---|---|---|---|---|---|---|
| q̃/q | 1.000 | 1.007 | 1.036 | 1.126 | 1.199 | **1.235** | 1.232 | 1.143 | 1.052 | 1.002 |

Every clause of Remark 2‴ is confirmed:

- **the ratio → 1 at both ends**, not to 5/3. The struck claim would have
  put the asymptote at 1.667; the measured maximum anywhere is 1.235.
- **it peaks at moderate κ_B** — 1.235 at κ_B = 2, against the decision
  log's pre-registered estimate of "~1.25–1.3 near κ_B 2–3".
- **at the locked κ_B = 1.0 the ratio is 1.126**, against the
  pre-registered estimate of ~1.13.
- **the relative VoC correction is largest at LOW κ_B**: it removes
  **79 %** of VoC_gated at κ_B = 0.5, 54 % at κ_B = 1.0, and 7 % at
  κ_B = 3. VoC lives in 1 − q, so the thin margin is at the low end.

(The MC ratio at κ_B = 8 reads 1.62, which is noise: q = 0.0035 ± 0.0007
there and the ratio of two near-zero rates has no precision. The
asymptotic statement rests on the analytic column, which has none.)

### Finding: idling is not free, and that is why the family matters

Remark 2″ says q̃ ≥ q because slack lets denied play buy information. The
measurement adds a wrinkle the remark does not: **an individual idle
placement can be worse than committing on schedule.** Smoke accumulates
every step, so spending a slack step early pushes every later observation
to a smokier time — schedule (2,2,1,0,0) is measurably worse than pinned
at κ_B = 5.

What rescues q̃ ≥ q is that the open-loop family *contains*
(2,1,0,0,0) — move immediately, then idle at the branch — whose draws are
a strict superset of the pinned schedule's. That schedule is the argmax at
**every** κ_B on the grid: proximity beats smoke-thinness throughout.

This is why the ruling's insistence on enumerating the full family rather
than exhibiting one dawdling policy was the right call. The two-line
optimality argument (module docstring, restated): while uninformed the
courier's information state is exactly t, since "no evidence so far" is a
deterministic function of t; once informed it commits immediately. So the
optimal denied policy is a choice of idle placement — open-loop — and the
maximum over the enumerated family is the optimum. `½ + q̃/2` is therefore
an **equality**, not a lower bound.

### Coverage arm — Remark 2′(i) as a picture

With the reward changed to team-any and the two agents splitting
corridors, **J = 1 at every κ_B under total denial**. Zero VoC. This is
the qualifier clause (i) needed: interchangeable, expendable agents at
least as numerous as the hypotheses make communication worthless, and it
is the courier's irreplaceable role — not blindness — that creates value.
The swarm env's d_p = 0.5 prices exactly that redundancy.

### Figure

`m52/e2c2_remark2.png` — J vs κ_B, both arms, VoC_true shaded green and
the dawdle correction shaded orange as its own band, with the VoC curves
and the relative correction below. The companion panel to the Theorem-1
figure.

### Theory-doc amendment — deferral discharged

Remark 2‴ created its own deferral: constants "are deferred to M5.2,
where q and q̃ are measured on the same grid by the shared MC machinery".
M5.2 measured them by that machinery in the same session, satisfying the
sub-rule on numbers entering documents *derived*, so under the delegated
ruling of 2026-07-29 the amendment was **made**: the ratio table, the
1.235 peak at κ_B ≈ 2, the 1.126 locked value, the → 1 asymptote, and the
"idling is not free" property the remark did not anticipate. The edit is
confined to discharging that deferral; no other theory text was touched,
and it remains reversible by the human at this handshake.

---

## M5.3 — Utility gate: does the swarm USE messages?

**VERDICT: NULL BRANCH.** All three arms are indistinguishable at the
measured reproducibility floor. Per the phase prompt and round-2 ruling
item 3 this is a STOP: the message design goes to a human discussion
before any lock, DIAL-style differentiable comms is pre-registered as
item #1, and **the architecture was not iterated here.**

### Protocol

Three arms at Medium, both couplings on, δ = 0, d_p = 0.5, 500 updates,
2 seeds, 512 CRN-paired eval episodes per cell (`run_m53_utility_gate.sh`,
run from `5030992`). Identical architecture and parameter count
throughout — the ablation is message *content*, never capacity:

| arm | what it cuts |
|---|---|
| live | nothing; messages as emitted |
| zeroed | the aggregate, hard-zeroed at the aggregation point — content dies, the link graph survives (so it is **not** the δ = 1 denial arm) |
| shuffled | sender identities permuted within the step — delivery pattern and the multiset of emitted messages preserved exactly, only who-said-what destroyed |

`test_msg_modes.py` pins the properties the verdict depends on: the three
arms init to bitwise-identical parameters, the shuffle leaves every
receiver's in-degree and the emitted multiset untouched, the arm choice
shifts no other PRNG stream (the shuffle key is a `fold_in`, never a
split), and eval honours the trained arm with `mute` kept separate for
M5.5's diagnostic.

### Results (seed-averaged eval means ± sd over 2 seeds)

| arm | completion | survival | episode return |
|---|---|---|---|
| live | 0.7403 ± 0.0211 | 0.9340 ± 0.0206 | 23.2944 ± 0.5517 |
| zeroed | 0.7242 ± 0.0336 | 0.9136 ± 0.0030 | 22.6553 ± 1.0924 |
| shuffled | 0.7271 ± 0.0104 | 0.9194 ± 0.0234 | 22.7817 ± 0.4716 |

Pairwise, graded against the M5.1e floor (bar = 2 × floor: completion
0.0290, survival 0.0258):

| pair | Δcompletion | Δsurvival | Δreturn | fraction of bar |
|---|---|---|---|---|
| live − zeroed | +0.0161 | +0.0204 | +0.639 | 0.56 / 0.79 |
| live − shuffled | +0.0133 | +0.0146 | +0.513 | 0.46 / 0.57 |
| zeroed − shuffled | −0.0029 | −0.0058 | −0.127 | 0.10 / 0.22 |

Nothing clears the bar, so the mechanically applied label is the null
branch. The pre-registered alternatives — "live > shuffled → sender-
specific content used" and "live ~ shuffled > zeroed → connectivity /
global content only" — both require a strong grade that no pair achieves.

### The nominal ordering, and why it is not the verdict

Live is nominally first on all three metrics against both other arms,
with zeroed − shuffled ≈ 0. That is the pattern a real effect would
make, and it is worth stating plainly rather than burying — but it is
not evidence at this n, for three reasons:

1. **It does not survive per-seed.** On completion, zeroed seed 0
   (0.7479) beats live seed 0 (0.7254); on survival, shuffled seed 1
   (0.9359) beats live seed 1 (0.9194). The ordering exists only in the
   seed-averaged means, and every arm's own ± spread is comparable to or
   larger than the deltas.
2. **The paired SE is the wrong bar, and a large one.** Pooled over the
   shared eval episode set, live − zeroed reads +0.0161 with a paired SE
   of 0.0047 — nominally 3.4 σ. That SE measures *eval-episode* noise
   only. The arms are different trained policies, so the operative
   uncertainty is training nondeterminism (M5.1e), against which the same
   delta is 0.56 of the bar. Quoting "+0.0161 ± 0.0047" would manufacture
   a significance the design cannot support; the script grades against
   the floor for exactly this reason, and the number is recorded here so
   nobody re-derives the wrong one later.
3. **Δsurvival and Δdeaths_fire are one fact, not two.** deaths_fire
   pools to 0.608 (live) / 0.848 (zeroed) / 0.763 (shuffled); the
   live − zeroed gap of 0.240 deaths over 12 agents is 0.0200, i.e. the
   +0.0204 survival delta re-expressed. It corroborates nothing.

### Channel diagnostics (pooled over both seeds, 1024 episodes/arm)

Ratios of sums, never means of ratios (the M4.4 numerator/denominator
discipline):

| arm | delivery rate | mean alive out-degree | masked_frac | danger rate | masked at danger |
|---|---|---|---|---|---|
| live | 1.0000 | 1.1094 | 0.00224 | 0.0364 | 0.0546 |
| zeroed | 1.0000 | 1.4216 | 0.00239 | 0.0338 | 0.0609 |
| shuffled | 1.0000 | 1.2768 | 0.00224 | 0.0321 | 0.0608 |

Two of these are handshakes rather than findings. Delivery rate is
**exactly** 1.0000 in every arm and every training run — δ = 0 recovers
the deterministic range graph, as `comms.py` claims and `test_comms.py`
pins. And the masking channels reproduce M4.4's Medium row
(danger rate 0.0396, masked_frac 0.00249, masked-at-danger 0.0560) to
within seed noise, so the environment these arms trained in is the
calibrated one.

The out-degree column is a *measurement for M5.4*, recorded not ruled:
at the plumbing default R_comm = 8.0 the mean alive out-degree is
1.11–1.42 under trained policies, against M5.4's prior band of [2, 5].
The Q5 ruling already logged that the band was written without the
geometry arithmetic (uniform 12 agents on 64² gives ~0.41 at R = 6 rising
to only ~2.22 at R = 16), and converted M5.4's R_comm step to
curves-first for that reason. This row is consistent with that
accounting and is not a band failure, because R_comm is not yet locked.

### Three candidate mechanisms — for the discussion, none actioned

Listed because the null is a design question and the discussion should
start from measurements rather than from scratch. Each is a hypothesis;
none is a proposal, and no code was changed on the strength of any.

1. **Nothing optimizes what to say.** Under the Q3 ruling the message
   head receives zero gradient for the whole run, so content is a
   frozen-at-init random projection of trained trunk features. Receivers
   *can* learn to decode it, which is what keeps M5.3 falsifiable, but
   "the swarm learned what to say" was out of scope by construction. This
   is the mechanism DIAL (item #1) addresses.
2. **There may be little to say at this operating point.** Averaged over
   the swarm, 0.22 % of a crop is masked; even at danger moments it is
   5.5 %, and danger moments are 3.4 % of alive agent-steps. Remark 2's
   premise is that comms is load-bearing exactly where perception fails —
   at Medium, perception mostly does not fail. M4.4 measured
   masked-at-danger at High as 0.2424, 4.4× the Medium value.
3. **There may be nobody to say it to.** With mean out-degree ~1.1–1.4,
   the typical receiver aggregates one neighbour or none, and the masked
   mean over a single sender is that sender's message. R_comm is
   unlocked, so this is a knob the gate ran at an arbitrary setting.

Candidates 2 and 3 are questions about *where the gate was run*, not
about the architecture, and both are answerable with the existing code
path. Candidate 1 is not. Which of the three the discussion pursues
first is a human call, and the M5.3 STOP is where it is owed.

### What the null does and does not license

It does **not** retract anything. M5.2's VoC handshake stands on its own
evidence — scripted policies in a micro-environment where the courier's
role is irreplaceable by construction — and M5.3 asks a different
question about a trained swarm with 12 interchangeable agents. Remark 2′(i)
predicted exactly that redundancy substitutes for communication when
agents are interchangeable and at least as numerous as the hypotheses;
M5.2's coverage arm measured J = 1 at every κ_B under total denial. A
null utility gate at swarm scale is the same statement, one level up, and
it was on the record before the numbers existed.

What it does block is the downstream reading. M5.4 proposes to lock δ as
the Phase-7 element value, and M5.5's inertness falsifier grades a denial
ablation — both interpret δ as removing something the swarm was using. On
this evidence that premise is unestablished at Medium, and the falsifier
would be measuring the removal of a channel not yet shown to carry usable
content. That is a discussion input, not a decision taken here.

### Settled at the STOP: the gate is re-sited at High (M5.3b, pre-registered)

The human discussion the prompt required was held on 2026-07-30. It found
that **the gate was run at the severity where its own mechanism measures
zero.** M4.4 Result 1, which predates the Phase-5 prompt:

| severity | Δsurvival (κ_B 0 → 1.0) | verdict | masked at danger | danger rate |
|---|---|---|---|---|
| low | +0.0059 | strong (1.16× threshold) | 0.0809 | 0.0068 |
| **medium** | **−0.0003** | **within noise** | 0.0560 | 0.0396 |
| high | **−0.0876** | **strong**, deaths_fire ×2.6 | **0.2424** | 0.0621 |

M5.3 asked whether neighbours can supply information the hazard withholds,
at the severity where our own prior measurement says it withholds nothing.
The prompt's stated expectation — "masked perception at Medium leaves
information on the table that neighbours can supply" — is contradicted by
M4.4's own Medium row.

**This is covering the range, not band-shopping** (M4.3 precedent, as
institutionalized for R_comm by the Q5 ruling): no threshold, label or
grading rule moves, **Medium's null stands as reported and is not
superseded**, and both cells are reported together whatever High returns.

**DIAL (item #1) is deferred on a dependency, not rejected.** It fixes what
gets said; whether the encoding binds cannot be measured in a cell with
nothing to encode, so a differentiable channel at Medium would return this
same null for this same reason. Even if built, it must be evaluated at High
to be interpretable — so High precedes it on either path.

Design, fixed before any number exists (`run_m53b_high_utility_gate.sh`):

- **The floor is measured first, on the same card, and the verdict reads
  it.** M5.3's script hardcoded the M5.1e floor, which is Medium- *and*
  card-specific; M4.4's σ_seed at High (0.0227/0.0295) is 2–4× Medium's
  (0.0107/0.0072). Section 1 runs four identical High runs and section 4
  grades against that file, refusing to produce a verdict if it is absent.
- **3 seeds**, per the M4.4 precedent for large-variance cells.
- **Cell A (verdict):** High, δ = 0, R_comm = 8 — one change from M5.3.
- **Cell B (sensitivity):** High, δ = 0, R_comm = 16. At High the swarm
  loses agents, so the graph is sparser exactly where the need is greatest:
  High raises demand and cuts supply at once. Cell B separates "no content
  is useful" from "no one was in range to hear it".

Pre-registered labels, all three fixed in advance:

| outcome | reading |
|---|---|
| A separates | comms load-bearing where perception fails; Remark 2 confirmed at swarm scale; proceed to M5.4 |
| A null, B separates | the constraint is **connectivity**; R_comm is load-bearing, not a plumbing default, and M5.4 must lock it where the channel is usable |
| both null | regime- and connectivity-independent; the reading returns to Remark 2′(i) — redundancy substitutes for communication, as M5.2's coverage arm measured — and the human chooses between a reportable negative and DIAL, with two cells and two severities of evidence |

### Artifacts

`che/bench/results/phase5/m53/`: six checkpoint archives
(`ckpt_{arm}_s{seed}.tar.zst` + `.sha256`, asserted by the job script per
the artifact-persistence rule), per-arm JSONL training metrics, per-episode
eval `.npz` + summary `.json`, `verdict.txt`, `timings.txt` (283–286 s per
training run), `provenance.txt`. The three arms carry distinct config
hashes (`660418c6…` live, `7328b27b…` zeroed, `96498520…` shuffled) so a
resume can never mistake one arm's checkpoint for another's. These
checkpoints cannot be regenerated: GPU training is not reproducible
run-to-run (M5.1e).

**Caveat carried from M5.1e and binding on every grade above:** the floor
has 3 dof and is itself uncertain by ~±40 %. Differences near the bar are
near the bar, not resolved. The largest here is 0.79 of it.

---

## M5.3b — the gate re-sited at High: null at both ranges

Run 2026-07-30 on an RTX PRO 6000 Blackwell, jax/jaxlib 0.11.0. Both cells
complete: 4 floor runs + 2 cells × 3 arms × 3 seeds, CRN-paired evals,
22 checkpoint archives. **Verdict: NULL AT HIGH TOO, AT BOTH RANGES** —
the third pre-registered branch.

### The measured High floor, and what it costs the gate

| metric | Medium (M5.1e) | **High (M5.3b)** | ratio | bar = 2× |
|---|---|---|---|---|
| completion | 0.0145 | **0.0522** | 3.6× | 0.1044 |
| survival_rate | 0.0129 | **0.0621** | 4.8× | 0.1243 |

Four identical runs, same seed: at High a single run's survival moves by
±0.06 from nondeterminism alone. **This is the milestone's most consequential
number**, and it was measured before the arms were compared, exactly so it
could not be chosen afterwards.

### Results

| cell | arm | completion (SE of mean) | survival (SE) | out-degree |
|---|---|---|---|---|
| **A**, R=8 | live | 0.7574 (0.0280) | 0.8436 (0.0458) | 1.012 |
| | zeroed | 0.7911 (0.0059) | 0.8289 (0.0419) | 0.930 |
| | shuffled | 0.8103 (0.0061) | 0.8464 (0.0450) | 1.055 |
| **B**, R=16 | live | 0.7774 (0.0298) | 0.8299 (0.0452) | 2.985 |
| | zeroed | 0.7420 (0.0118) | 0.8273 (0.0185) | 3.256 |
| | shuffled | 0.7094 (0.0118) | 0.8397 (0.0599) | 3.369 |

No pairwise difference exceeds **0.65× the bar** anywhere in either cell.

### Three things make this null more informative than M5.3's

1. **Connectivity is eliminated as the explanation.** Cell B tripled mean
   alive out-degree (1.01 → 2.99) at delivery rate 1.0000, and changed
   nothing. The "there was nobody in range to hear it" hypothesis —
   candidate 3 of the M5.3 discussion — is dead, and that is precisely what
   the pre-registered sensitivity cell existed to decide.
2. **The completion difference flips sign between cells**: live − zeroed is
   **−0.0338** at R=8 and **+0.0354** at R=16. An effect that reverses when
   agents are given three times as many neighbours is noise with a sign, not
   a mechanism.
3. **The bar is honest about what was not tested.** With arm-mean SEs of
   0.028–0.046 and a bar of 0.104/0.124, Cell A can only resolve effects of
   roughly ten points. **This null means "no effect larger than ~11 points",
   where M5.3's Medium null meant "no effect larger than ~3 points".**

### The re-siting traded measurability for mechanism — stated plainly

M5.3b was recommended because Coupling B's mechanism is 4.3× stronger at
High (masked-at-danger 0.2424 vs 0.0560). It is. But the floor is 3.6–4.8×
larger there too, so the bar rose in step and the High cell is **not better
powered than Medium** — it is worse. Reaching Medium's bar at High would
take roughly 46 seeds per arm, which is a wall rather than a budget line.

The consequence for reading the two milestones together: **Medium is the
cell that bounds the effect (< 3 points); High is the cell that eliminates
connectivity.** Neither alone would have settled it.

### Carried forward

- **M5.4 datum:** R_comm = 16 yields mean alive out-degree 2.99–3.37 under
  trained High policies — inside the [2, 5] prior band that R = 8 (1.0)
  misses. Recorded whatever M5.4's fate.
- **A general power finding, beyond comms:** any claim at High needs a
  measured floor beside it. M4.4's High survival result (−0.0876, graded
  "strong" against σ_seed = 0.0295 from two seeds) is **1.41× this measured
  floor**, not 3σ. M4.4's own report warned that "Var of two points can
  collapse toward zero by chance"; it did. The direction survives (M5.1
  replication, 3/3), the confidence language does not. Flagged for the
  human — M5.5's High cells at 2 seeds inherit the same limit.

### Branch taken

Per the pre-registration, both cells null returns the reading to Remark
2′(i): **redundancy substitutes for communication** when agents are
interchangeable, expendable and at least as numerous as the hypotheses —
which is what M5.2's coverage arm measured in miniature (J = 1 under total
denial). The choice between accepting this as a reportable negative and
building DIAL is the human's, now with two severities, two connectivity
regimes and three content ablations behind it.

---

## M5.5 — Phase-5 acceptance: the denial element, certified

Run 2026-07-30 on an RTX PRO 6000 Blackwell. Rescoped per the M5.3 closure
ruling: Medium × δ ∈ {0, 1.0} × 4 seeds, **message path live in both arms**
(the ablation is denial, never architecture), R_comm = 16 at the locked
value. 4 floor runs + 8 grid runs + mute diagnostic + 24 matched renders.

### FINAL VERDICT

> **INERT WITHIN MEASUREMENT RESOLUTION** — conditions (i), (ii) pass
> against measured bars; condition (iii) as-registered is retracted as
> structurally defective (threshold 20 % < instrument floor 27.2 %) and
> re-graded against the pre-dated floor: 23.2 % < 27.2 %, not resolvable.
> The inertness claim rests jointly on this certification and on M5.3's
> demand-side mechanism evidence (the unused connectivity bit).

The verdict **as produced** (`m55/verdict.txt`, "NOT INERT") stands
unedited in the artifact, with this adjudication beside it.

### Results

| δ | completion | survival | delivery | out-degree | fire/danger |
|---|---|---|---|---|---|
| 0.0 | 0.7396 ± 0.0195 | 0.9188 ± 0.0114 | 1.0000 | 3.213 | 0.00744 |
| 1.0 | 0.7358 ± 0.0131 | 0.9331 ± 0.0065 | 0.0000 | 0.000 | 0.00571 |

- **(i)** Δcompletion +0.0038 vs bar 0.0799; Δsurvival −0.0143 vs bar
  0.0260. Both within the floor measured on this card.
- **(ii)** The knob provably moved: delivery 1.0000 → 0.0000, out-degree
  3.213 → 0.000 — the empty graph `comms.py` specifies, not a weakened one.
- **(iii)** Void (below).

### Why condition (iii) is VOID rather than FAILED

The distinction is load-bearing. A threshold set below its instrument's
measured floor **cannot pass under the null**; a test that cannot pass
regardless of the truth is not a test, and its output is not evidence.

The quantity is fire deaths per danger agent-step. Four identical runs
(same seed, same config) measure it at 0.00810 / 0.00408 / 0.00776 /
0.00688 — **sd 0.00182, 27.2 % relative**. The registered threshold was
20 %. The observed cross-arm difference, 23.2 %, sits between the two: it
exceeds the threshold and falls short of the noise.

Three clauses license the re-grade against the charge of special pleading,
and they are stated here rather than assumed:

1. **The floor data pre-date the comparison.** Section 1 ran before Section
   2 by construction. This is instrument calibration, not post-hoc rescue.
2. **The defect is structural** — it would void a PASS identically. A bar
   finer than its instrument is broken in both directions.
3. **The counterfactual is on the record:** had the 23.2 % exceeded the
   27.2 % floor, **NOT INERT would stand**, and this ruling says so.

For scale, the δ = 0 arm's own per-seed spread (0.00517–0.01041) is wider
than the entire cross-arm difference it was being graded against.

### The floor, and why re-measuring it was not optional

| metric | M5.1e (5090) | M5.5 (PRO 6000) | ratio |
|---|---|---|---|
| completion | 0.0145 | **0.0399** | **2.75×** |
| survival_rate | 0.0129 | **0.0130** | 1.01× |

The card reconciliation flagged in the M5.5 script discharged itself:
re-measurement mattered for one metric and not the other. Neither "it will
be the same" nor "it will differ" was safe to assume — which is now the
motivating exhibit for the **bars-come-with-floors** rule (`CLAUDE.md`,
2026-07-30). Floors are per-metric *and* per-hardware facts.

### What the certification does and does not claim

It claims the denial element is inert **at the resolution these
measurements have**: no effect on completion above ~8 points, on survival
above ~2.6 points, or on danger-moment outcomes above ~27 % relative, at
Medium with 4 seeds. It does not claim a point null.

The strength of the Phase-5 comms result comes from the *joint* argument,
not this grid alone: M5.3/M5.3b established the mechanism (the unused
connectivity bit is demand-side — that signal needs no encoder, so its
neglect cannot be blamed on the frozen random projection), and M5.5
certifies that removing the channel entirely changes nothing measurable.
Either half alone would be weaker.

Carried limitation, unchanged: **gradient-shaped messaging remains
untested; the channel was a fixed random projection.**

### Artifacts

`che/bench/results/phase5/m55/` — 12 checkpoint archives (all 12 verified
against their sha256 before the instance was released), per-episode evals,
the muted-eval diagnostic, both floors, 24 matched renders (δ = 0 vs
δ = 1 at identical episode seeds; the branch-loitering watch item is
un-inspected and left for the human), provenance, and the unedited
verdict.
