# Work package E1 — Co-active visitation: the compound-hostility mechanism

> Fresh session at repo root. **This is not a protocol milestone and must not
> become one.** It is authorized by the allocation correction (framing ruling
> item 3, `docs/decision_log.md` 2026-08-02), which directs reclaimed effort
> to environment-native content. Milestone by milestone; **STOP and report**.
>
> Numbered E1 rather than M6.3 on purpose: M6.3 belongs to the grid, which is
> blocked. E-numbers do not queue behind it.

## Where the project stands (read this before anything else)

Phase 6 is **mid-flight and blocked on a human ruling**, not on work:

- **M6.2b (step b) STOPped on the power guard.** Both confirmatory arms
  converge at T = 1000 (ISO 0.10×, JOINT 0.57× of their own floors), but
  JOINT's completion floor grew 5.2× and its power@0.03 fell to 62.8 %,
  under the registered 80 %. See `che/bench/results/phase6/m62b/m62b_report.md`.
- **`k` is owed a human ruling**, together with the question of whether Γ's
  power is graded on the registered per-arm `σ√(2/k)` or the combined-variance
  form correct for a difference of means (§6 of that report).
- **Do not re-rule either. Do not run the grid. Do not launch GPU jobs.**

**Read, in order:** `CLAUDE.md` → `HANDOFF.md` →
`che/bench/results/phase6/m62b/m62b_report.md` → `docs/decision_log.md` from
"PHASE-6 FRAMING + ALLOCATION RULING" onward → `docs/theory_foundations.md`
§§ on Def. 5 (Coupling A) and Def. 6 (Coupling B).

---

## ⚠ THE ONE TRAP IN THIS TASK — read before touching any artifact

**The NO-PEEKING rule (ruled 2026-08-02) binds this work.** M6.2 and M6.2b
eval artifacts are **Phase-6 confirmatory** runs of the ISO and JOINT arms.
`coupling_co_active` is an **outcome channel** of those runs.

**Comparing co-active visitation between ISO and JOINT is a cross-arm outcome
comparison and is FORBIDDEN until unblinding.** Any document that does it gets
flagged. This is a live trap: the arm labels sit in the filenames, the data is
right there, and the comparison looks scientific rather than procedural.

**Therefore: this work package uses Phase 3–5 artifacts only.**

| use these (115 eval npz) | do NOT touch until unblinding |
|---|---|
| `m30b` (27), `m35` (12), `m30` (9), `m31b` (3) | `m62` (24) |
| `m44` (14) | `m62b` (17) |
| `m53` (6), `m53b` (22), `m55` (16), `m51e` (4), `pretask` (2) | |

If an analysis genuinely requires Phase-6 data, **STOP and ask** — do not
decide it yourself.

---

## Context — what the counter is, and why it is the mechanism

`coupling_co_active` (invariant #5, `che/env/env.py:399–404`) counts, per step,
**collapse-seeded ignitions within Chebyshev radius `obs_window // 2` of an
alive agent**, evaluated at post-step positions. It has been logged in the env
`info` dict **since day one**, on the explicit instruction that retrofitting it
into jitted rollouts later would be painful. It has **never been analysed.**

It is the mechanism variable for the paper's central claim. Compound hostility
is not "two stressors present"; it is the two **acting on the same agent at the
same time**:

- **Coupling A** (Def. 5) makes structural collapse *create* hazard.
- **Coupling B** (Def. 6) makes that hazard's smoke *blind the agent to it*.
- The counter measures where those coincide **within perception range**.

The paper's environment-first framing rests on the claim that this environment
produces compound hostility rather than additive stress. **This counter is the
direct observable of that claim, and it is currently unexamined.**

Related channels already logged alongside it, per-episode, in every eval npz:
`seeded_ignitions`, `danger_agents`, `masked_danger_sum`, `collapse_events`,
`blocked_moves`.

---

## Milestone E1.0 — Inventory before analysis

Establish what exists before computing anything on it.

- Which Phase 3–5 eval artifacts carry the counter, at which θ, severity,
  seed and protocol. Build a table.
- **Confirm the DECISION comment's scope caveat** (`env.py:400`): the radius is
  `obs_window // 2`, "revisit when Coupling B fixes attenuation range". Does
  the co-active radius match the radius over which Coupling B actually
  attenuates? **If it does not, say so plainly** — it bounds every claim in
  this package, and it is better stated by us than found by a reviewer.
- Sanity-check the counter against `seeded_ignitions`: co-active ≤ seeded, by
  construction. **If that inequality ever fails, STOP** — it means the counter
  or the dilation is wrong, and every downstream claim would be void.

**Deliverable:** inventory table + the radius finding. **STOP and report.**

## Milestone E1.1 — Does co-activity vary with severity, and with κ_A/κ_B?

The first real question. Using Phase 2/3 locked severities (β = 0.43 / 0.49 /
0.70) and the Phase 3–4 grids:

- How does co-active visitation scale with severity? A prediction exists and
  should be stated **before** looking: Coupling A is "marginal by construction"
  at High (`coupling_a_lock.md`) because supercritical fire consumes the fuel
  collapse would ignite, while Coupling B's masking ceiling *rises* with
  severity (0.028 / 0.130 / 0.419 across Low / Medium / High, `kappa_b_lock.md`).
  **So co-activity need not be monotone in severity** — and Medium may be its
  peak. Medium is also θ\*. If that holds, it is a strong independent
  justification for the θ\*-siting ruling, arrived at from mechanism rather
  than from lock criteria.
- Every number carries a floor grade. **Bars come with floors** — use the
  measured per-milestone floors, or flag UNDERPOWERED. Do not invent a
  threshold.

**Deliverable:** severity-response of co-activity, floor-graded. **STOP.**

## Milestone E1.2 — Is co-activity endogenous?

M4.3 established that **policies regulate their own exposure** (the M4.3
exposure finding was later retracted in its strong form — read
`phase4_report.md` and the retraction before citing it). Co-active visitation
is therefore **endogenous**: it is partly a policy choice, not only an
environment property.

- Does realized co-activity differ between policies trained under different
  protocols at the *same* evaluation θ? (Phase 3–5 arms only.)
- Does it change over training within a run? The training `.jsonl` logs carry
  per-update channels — check what is actually there before assuming.
- **This is presented as mediation, never as causal regression** — the
  pre-registered void rule in design v2 §7 applies in spirit: an endogenous
  dose has no clean x-axis.

**Deliverable:** endogeneity evidence, with the mediation framing explicit.
**STOP.**

## Milestone E1.3 — Figures + a drafted paper section

- Figures from existing artifacts only (`che/scripts/` has the plotting
  precedents — follow their style; matplotlib, no new dependencies).
- A drafted mechanism section: what compound hostility *is* in this
  environment, measured rather than asserted.
- **State the limits.** The radius caveat from E1.0, the endogeneity from
  E1.2, and the fact that Phase-6 data is excluded by the blind protocol.

**Deliverable:** figures + section draft. **STOP.**

---

## Hard constraints

- **No new GPU runs.** Everything here is analysis of committed artifacts. If
  you think you need compute, **STOP and ask** — a box costs money and the
  budget is $40 for the grid, which is already over.
- **Do not touch** `che/env/`, the protocol, `docs/locks.yaml`, or any
  registered constant. This package **reads**.
- **Numbers enter documents derived or measured in the same session** — never
  transliterated from this prompt. Every figure above (5.2×, 0.028/0.130/0.419,
  62.8 %) is a pointer to a source, not a citable value.
- **Rulings bind only once transcribed.** If the human rules something in
  chat, transcribe it to `docs/decision_log.md` before acting on it.
- Run the CPU suite **chunked and thread-capped** —
  `OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 nice -n 15 uv run pytest <subset>`.
  An unbounded run once crashed the machine. Note `test_prop3`,
  `test_calibration` and `test_percolation` are slow MC files — isolate them,
  and they have **not** run on local CPU since 2026-08-02 (they passed on GPU).
- After each milestone: `ruff`, the chunked suite, commit naming the milestone.

## Non-goals

- Re-ruling `k`, T\*, or anything else the M6.2b STOP left open.
- Running or designing the Phase-6 grid.
- Any cross-arm comparison of M6.2/M6.2b outcomes (see the trap above).
- Re-opening Phase 0–5 results.

## Open items inherited, for awareness only

- `m06/` is 47 MB of pre-M6.0 spike leftovers sitting at the repo root; nobody
  has decided whether it belongs in the tree.
- Design v2 §9 lists engineering owed before the grid (M6.1) — per-component
  count logging, protocol config tests. Not this package's job.
