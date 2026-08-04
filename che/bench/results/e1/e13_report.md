# E1.3 — Figures and a drafted mechanism section

**Status: delivered. Three figures and a paper-section draft, from committed
artifacts only. E1 is complete.**

Work package E1, milestone 3 (`env_native_prompt.md`). Zero compute.
Instrument `che/scripts/plot_e1_mechanism.py` — pure replot from the E1 JSONs
and Phase 3–5 eval `.npz`, matplotlib only, no new dependencies, following the
`plot_m43_bands.py` house style (`Agg`, `constrained_layout`, `tab:` colours,
`dpi=150`).

---

## 1. Deliverables

| artifact | claim it carries |
|---|---|
| `figures/fig1_mechanism.png` | `co_active = seeded × share`. The severity response lives entirely in Coupling A's productivity (4.83× drop, fuel exhaustion); the near-agent share is flat (span 0.025). |
| `figures/fig2_distribution.png` | The counter is zero-inflated and over-dispersed — P(0) = 0.563 / 0.578 / 0.883, var/mean 1.31–1.40. Compound hostility is rare and bursty. |
| `figures/fig3_endogeneity.png` | The endogeneity null: seed dispersion ÷ reproducibility floor = 1.25× / 0.57×; no training treatment exceeds 1.4× its own pooled dispersion. |
| `e13_mechanism_section.md` | **The drafted paper section**, written to be lifted into the manuscript. |

Every number in the figures is drawn from `severity.json`, `endogeneity.json`
or the Phase 3–5 eval `.npz`; nothing is hard-coded.

---

## 2. Two design decisions worth recording

**Fig. 2 exists because of E1.2's correction.** `phase4_report.md` Result 4
warned that "the mean alone would have been actively misleading" for this
counter, and E1.1 used means throughout without saying so. Rather than only
noting the caveat in prose, the distribution now has its own figure — the
zero-inflation is the phenomenon, not a nuisance.

**Fig. 3's left panel is deliberately single-coloured.** The first render
coloured bars above 1× differently, which made the 1.25× and 1.29× Medium
ratios read as detections. At n = 3–4 they are not, and a colour scheme that
implied otherwise would have undercut the null the panel exists to show. The
axis annotation now says so explicitly.

**Fig. 1 marks Low as "no floor measured"** rather than plotting a bare point
that would read as if it had been graded. No reproducibility floor exists at
Low for any artifact in the corpus.

---

## 3. The limits, carried into the draft

The work package required E1.3 to state the limits. All six are in the
draft's own **Limits** section rather than buried in a report:

1. The **radius caveat** from E1.0 — the counter bounds rather than resolves;
   optical depth varies 1.414× across the outermost shell alone.
2. The **endogeneity result is a failure to detect**, at n = 3–4 with 2–3 dof,
   not a proof of absence.
3. **No Low-severity floor exists**; cross-milestone floors are labelled
   *reference scale*, never *floor*.
4. The **within-training trajectory is unmeasurable** — 0 of 92 training logs
   carry the counter.
5. All artifacts are **500-update checkpoints**; the confirmatory experiment
   runs at twice that.
6. **Phase-6 data is excluded** by the blind protocol, and the code refuses
   those paths structurally.

---

## 4. E1 is complete

| milestone | outcome |
|---|---|
| **E1.0** | Subset check passed (0 violations / 38,912 episodes); radius caveat resolved — exact on the outer bound, 1.414× residue inside; inventory is 115 files but only 76 gradeable and 64 with both couplings live. |
| **E1.1** | Pre-registered prediction **refuted** (plateau-and-cliff, not a Medium peak); `seeded × share` decomposition; share flat; relative-floor variance result. |
| **E1.2** | Motivating premise found **retracted**; three tests find **no detectable endogeneity**; a registered Phase-6 guard flagged as likely to fire; invariant #5 found half-satisfied. |
| **E1.3** | Three figures and a drafted paper section, limits stated. |

**Provenance correction carried from E1.2, restated so it is not lost:** the
work package's claim that the counter had "never been analysed" is false —
`phase4_report.md` Result 4 analysed it on the same m44 artifacts and already
reported the cell means, the κ_B null with its explanation, and the inverted
severity ordering. E1 re-derived those independently and identically. What E1
adds is the decomposition, the variance result, the m35 replication, the
endogeneity tests, the floor discipline, and the figures.

---

## 5. Open items handed forward

Neither is E1's to decide.

1. **The training logger drops the counter** (`coupling_co_active`,
   `seeded_ignitions`, `collapse_events`, `danger_agents`,
   `masked_danger_sum` — 0 of 92 files). Adding them is **cheap before the
   grid and impossible after**, and would answer the within-training question
   E1.2 could not. Engineering decision for a human.
2. **The Phase-6 dose figure's void rule is at risk** (E1.2 §5). The
   suggested sequencing — run the first-stage check at unblinding before
   building the downstream isotonic/bootstrap machinery — is a note, not a
   re-ruling.

Nothing in `che/env/`, the protocol, `docs/locks.yaml` or any registered
constant was touched by any E1 milestone. This package read.
