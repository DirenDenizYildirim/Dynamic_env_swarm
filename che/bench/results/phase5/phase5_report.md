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
| envs128 | 24.69 | half the envs (fallback-ladder rung 2) |

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

**Status: the gate is UNRESOLVED and the remedy is a human scope
decision.** Every option that fits alters `n_minibatches`, `pop_size` or
`n_envs`. Recommendation deferred to the Phase-6 entry gate, where D6 is
already owed — Phase 5's own milestones do not use the population path.
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

### Owed to the human at this STOP

Theory-doc edits are a Phase-5 non-goal, so **no amendment was made**.
Remark 2‴ says constants "are deferred to M5.2"; they are now measured
and the proposed amendment is: replace "no numeric ratio belongs in this
document before then" with the peak ratio 1.235 at κ_B ≈ 2, the locked
value 1.126, and the → 1 asymptote. That is a human call at the fourth
theory↔implementation handshake, not a builder's edit.
