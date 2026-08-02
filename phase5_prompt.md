# Phase 5 — Communication axis: architecture, Remark-2 VoC validation, δ lock

> Fresh session at repo root. Prerequisites: Phase 4 complete + accepted
> (GO 2026-07-28), κ_B = 1.0 locked, all prior locks in force, standing
> throughput rule active. Pre-task from the Phase-4 close rulings: render
> the matched High κ_B=0 control set (6 episodes, same seeds as the
> locked-arm High renders) before starting M5.0. Milestone by milestone;
> STOP and report.

## Context

The comms axis (Def. 7) is the third stressor element: messages over a
realized link graph, per-link alive probability p_link(d)·(1−δ). Design
commitments from theory, restated: T_K reads positions only — never h,
ρ, or c (mechanistic independence is what "independent load-bearing
axis" means); δ = 0 recovers free range-limited comms as the nested
model; Remark 2 predicts VoC(κ_B) = ½(1−q(κ_B)) in E2C — communication
is worth most exactly when smoke has blinded individual perception —
which is this phase's theory hook and companion figure to M4.2.

This is the first *network* change since Phase 0 (message head +
aggregation). Expect the bench to land below the 100k line; the uint8
contingency then activates mechanically per the standing rule — planned
non-event, not a discussion.

## Milestone 5.0 — Architecture + link kernel

- **Link kernel (`che/env/comms.py`):** links alive between alive-agent
  pairs with p = 1[d ≤ R_comm] · (1−δ) (hard range, Bernoulli denial;
  d = Chebyshev). Draws from a dedicated fold_in stream (M3.1/M4.1
  pattern), one uniform per ordered pair per step, **unconditional** —
  δ = 0 and δ = 1 are bitwise-nested parameterizations of one kernel.
  Link state k_t enters `info` (per-episode delivery rate, mean degree).
- **Message path (`che/train/networks.py`):** each agent emits m ∈ R^8
  (tanh) from its trunk at step t; delivery at **t+1** over the realized
  links (one-step latency — no intra-step fixed point, and it makes
  message content strictly pre-decision information); aggregation =
  masked mean over delivering neighbors (permutation-invariant; zero
  vector when isolated) concatenated to the own-state vec. Sender's own
  message is not self-delivered. Message tensors live in the carry —
  document the shapes in the codebase tour style.
- **Nesting tests:** δ cannot perturb any env kernel stream (state
  trajectories bitwise-identical across δ under matched keys — actions
  aside, so test at fixed action sequences); δ = 1 ⇒ delivered aggregate
  ≡ 0 vector bitwise; message-zeroed network ≡ δ = 1 outcomes given
  matched keys; permutation invariance of aggregation; dead agents
  neither send nor deliver.
- **Accept:** suite green (budget ≤ 4 min holds or is flagged). STOP.

## Milestone 5.1 — Bench row (standing rule applies)

Reference cell env-only + one 500-update Medium training run with the
full message path. If the training projection < 100k steps/s: activate
uint8 obs storage + in-network normalization, re-bench, record both
rows. Do not ask; do not renormalize the line. **Accept:** gate-report
rows + verdict. STOP only if something *other* than the pre-registered
contingency fires.

## Milestone 5.2 — ★ Remark-2 VoC validation ★ (theory §5 Remark 2)

Two-agent E2C extension at the locked Option-A geometry, slack T =
d + ℓ + 1, reward 1 if *any* agent reaches the goal:

- **Scripted policies (validation, not training):** scout protocol per
  Remark 2 — agent 2 enters corridor L at the branch; surviving one step
  it messages "L safe"; its silence (or observed death, which Coupling B
  may occlude — route knowledge of the death *only* through the message
  channel) identifies Z. Agent 1 acts on the delivered bit. Under δ = 0:
  success ≈ 1 at every κ_B. Under δ = 1: agent 1 reverts to the
  single-agent optimal of M4.2 → J = ½ + q(κ_B)/2.
- **Predicted curves:** free-comms line at 1; denied-comms curve = the
  M4.2 prediction (same shared-constant machinery); VoC(κ_B) = J_free −
  J_denied — must be increasing in κ_B, → ½·(1−q) shape.
- **Acceptance (@slow):** the M4.2 three-condition gate (Šidák 2.69 /
  joint χ² p ≥ 0.05 / |mean z| ≤ 2/√n) applied to the δ = 1 curve vs
  prediction; δ = 0 curve ≥ 0.99 at every κ_B; measured VoC
  monotonically increasing across the grid (isotonic within noise).
- **Figure:** J vs κ_B, both arms + VoC shaded — the companion panel to
  the Theorem-1 figure, and Remark 2's "comms is load-bearing exactly
  when perception fails" as a picture.
- **Accept:** slow test green, figure in phase5_report.md. STOP — human
  reviews (fourth theory↔implementation handshake).

## Milestone 5.3 — Utility gate: does the swarm USE messages?

The denial axis is vacuous if messages carry nothing. Paired probes at
Medium (both couplings on, δ = 0, 500 updates, 2 seeds): message path
live vs message aggregate hard-zeroed (same architecture, same param
count — zeroing at the aggregation point, not a different network).
CRN-paired evals.

- Live > zeroed on completion or survival (strong grade under the M4.4
  rule) → comms is load-bearing; proceed.
- Indistinguishable → **STOP with the numbers**: the message design
  (dim, aggregation, latency) goes to a human discussion before any
  lock — do not iterate architecture silently. (Expectation from
  Remark 2 + M4.4: masked perception at Medium leaves information on
  the table that neighbors can supply; but expectation is not evidence.)
- **Accept:** verdict table. STOP only on the null branch.

## Milestone 5.4 — (R_comm, δ) calibration → human lock

Propose the locked values against measured observables (random policy +
the M5.3 live-arm checkpoints):

- **R_comm band:** at reference density (12 agents, 64²), mean alive
  degree ∈ [2, 5] and P(swarm connected) ∈ [0.3, 0.7] at δ = 0 —
  connected enough to matter, sparse enough that positioning matters.
  Sweep R_comm ∈ {6, 8, 10, 12, 16}.
- **δ band (the Phase-7 element value):** sweep δ ∈ {0.25, 0.5, 0.75,
  0.9, 1.0} evaluating the M5.3 live policies; propose the smallest δ
  whose performance cost vs δ = 0 carries a strong grade, with the full
  degradation curve reported. If only δ = 1.0 qualifies, propose it —
  total denial is a legitimate element value, but the curve must show
  we didn't skip a cheaper sufficient point.
- Bands are proposals; misses or non-intersections come to the STOP
  with curves, per the M4.3 precedent (retire/demote with reasons, no
  band-shopping).
- **Accept:** `comms_lock.md` proposal table. STOP — human locks.

## Milestone 5.5 — Acceptance grid (Phase-5 close)

- 3 severities × δ ∈ {0, locked} × 2 seeds (+ third seed at Medium),
  dp = 0.5, 500 updates, Couplings A and B ON at locked params —
  message path live in both arms; the ablation is denial, not
  architecture.
- **Pre-registered inertness falsifier (symmetric, M4.4 pattern):** the
  denial element is inert at swarm scale iff (i) Δcompletion and
  Δsurvival within seed noise (M4.4 stated rule, now pre-registered for
  this grid), (ii) delivery-rate difference confirms the knob moved,
  (iii) no cross-arm difference in danger-moment outcomes (deaths_fire
  conditioned on burning-in-crop). All hold → reportable negative.
- Report: the M4.4 table battery + delivery rate, mean degree, message-
  usage diagnostic (live-vs-zeroed eval of the trained δ=0 policies —
  free re-check of M5.3 at 500 updates), co-active distributions,
  render audit (6/severity at locked δ + matched δ=0 Medium pairs; look
  for comms-mediated coordination: converging responses to unseen
  hazards).
- **Accept:** phase5_report.md complete. STOP — Phase 5 complete.
  **PHASE 6 ENTRY GATE fires next: re-read the D6-proposal with the RA
  before any Phase-6 work** (decision_log.md gate line).

## Non-goals

Hazard-coupled comms (future work per Def. 7), message-content
analysis/interpretability beyond the usage diagnostic, attention
aggregation or multi-round messaging (design iteration only via the
M5.3 null branch), ISO/JOINT/dose-response (Phase 6), theory-doc edits.
