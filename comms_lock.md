# comms_lock.md — the comms axis, locked as a certified negative

**Status: LOCKED 2026-07-30** (human + RA, "M5.3 CLOSURE RULING",
`docs/decision_log.md`). This lock is unusual and says so up front: it
records that **the knob does nothing at swarm scale**, and certifies why.
A lock that says "this parameter is inert, here is the evidence" is a
legitimate lock — the alternative is leaving a registered element
unspecified because its calibration bands were falsified rather than met.

| parameter | locked value | basis |
|---|---|---|
| **δ** (comms denial, Def. 7) | **1.0** | by convention: maximal denial, cleanest element semantics for θ*. Performance bands **void-by-null** (below). |
| **R_comm** | **16** | geometric observable alone: mean alive out-degree **2.99–3.37** (M5.3b Cell B, 12 agents on 64², trained High policies), inside the [2, 5] prior band. R = 8 measures 0.93–1.06 and misses it. |

---

## Why the δ bands are void, not missed

M5.4 was specified to "propose the smallest δ whose performance cost vs
δ = 0 carries a strong grade, with the full degradation curve reported".
That procedure has no output when the cost is ≈ 0 at every δ — and it is,
because **the channel's content is not used at all**. The band's premise
was falsified before the sweep could be run, so the sweep was folded into
the closure ruling rather than executed.

This is explicitly **not** band-shopping (the M4.3 precedent it would
otherwise resemble): no band was widened, replaced, or re-chosen after
seeing data. A premise was falsified and the dependent procedure was
retired with its reasons recorded.

## The certification

Five content-ablation arms across two severities and two connectivity
regimes, all null against measured reproducibility floors:

| milestone | severity | R_comm | out-degree | arms | result |
|---|---|---|---|---|---|
| M5.3 | Medium | 8 | 1.11–1.42 | live / zeroed / shuffled × 2 seeds | null; bound **< 3 points** |
| M5.3b Cell A | High | 8 | 0.93–1.06 | live / zeroed / shuffled × 3 seeds | null; bound < 11 points |
| M5.3b Cell B | High | 16 | 2.99–3.37 | live / zeroed / shuffled × 3 seeds | null; bound < 11 points |

Two properties make this a certification rather than an absence of
evidence:

1. **The connectivity bit is the load-bearing evidence.** A receiver knows
   it heard from *someone* without decoding anything — that signal needs no
   encoder. Its worthlessness is therefore **demand-side** (the swarm does
   not need the information) and not **channel-side** (the swarm cannot
   read the message). The frozen-encoder objection does not rescue the
   channel, because the encoder-free signal is unused too.
2. **The sign flips with connectivity.** live − zeroed on completion is
   −0.0338 at R = 8 and +0.0354 at R = 16. An effect that reverses when
   agents are given three times as many neighbours is noise with a sign.

Theory anticipated this: **Remark 2″(i)** — redundancy substitutes for
communication when agents are interchangeable, expendable, and at least as
numerous as the hypotheses. M5.2's coverage arm measured it in miniature
(J = 1 at every κ_B under total denial). M5.3/M5.3b are that result at
swarm scale.

## Hedges, stated because the clean-zero conditions were not met

- **`dp = 0.5` prices deaths**, so agents are not strictly *expendable* and
  the theory's clean-zero conditions do not fully hold. The measured null
  is therefore the stronger statement: the deficit formulation's "value
  returns" term is **weak at this scale and this death price**, not merely
  absent in the idealized case.
- **Gradient-shaped messaging remains untested.** The channel was a fixed
  random projection of trained trunk features (Q3 stop-gradient ruling), so
  a < 3-point cap measured on a frozen encoder does not *strictly* bound a
  trained one. DIAL was formally declined with reasons (decision log); this
  sentence is the paper's limitation, carried explicitly.
- **R_comm is locked on geometry alone.** The second prior observable,
  P(swarm connected) ∈ [0.3, 0.7], was never measured — with performance
  insensitive to R_comm, it carries no weight it could have carried, and
  the full {6, 8, 10, 12, 16, 20, 24, 28} sweep was not run. Only R = 8 and
  R = 16 are measured points. Recorded as a limitation of the lock, not
  hidden by it.
- **Performance-insensitivity is the reason the geometric lock is
  admissible at all**: with no measurable performance dependence on R_comm,
  the choice cannot be tuned toward a favourable result.

## What is retained downstream

δ = 1.0 stays in θ* for **registration fidelity at zero cost** — the
element remains in the recorded design, and the Phase-7 composition is
effectively over {Coupling A, Coupling B}. The dose-response x-axis
(A×B co-active visitation) is unaffected (D6 append, decision log).

M5.5 runs as **certification, not exploration**: Medium × δ ∈ {0, 1.0} × 4
seeds, expected verdict INERT, graded against a measured reproducibility
floor with its regime named.

## Provenance

- `che/bench/results/phase5/m53/` — Medium, 3 arms × 2 seeds (2026-07-29)
- `che/bench/results/phase5/m53b/` — High, 2 cells × 3 arms × 3 seeds plus
  the measured High floor (2026-07-30)
- `che/bench/results/phase5/phase5_report.md` — M5.3, M5.3b
- `docs/decision_log.md` — "M5.3 null branch settled", "M5.3b outcome",
  "M5.3 CLOSURE RULING"
