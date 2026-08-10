# HANDOFF — session state for the next model (written 2026-08-03)

You are picking up **mid-Phase-6, immediately after the M6.2b close-out**. The
STOP that blocked everything is **discharged**: `k` and the variance basis are
ruled, **T\* = 1000 is registered**, and the grid is **authorized at 240
runs**. There is **no GPU box running**.

**Nothing is blocked on a decision any more. Two things gate the grid, and
both are work:**

1. ~~**[OWNER] render inspection of the 24 M5.5 episodes.**~~ **DISCHARGED
   2026-08-10** — `docs/decision_log.md`, *RENDER-GATE FINDINGS*. Ruled **not
   a launch blocker**. The bottom-clustering the inspection asked about is a
   per-training-run residual action bias integrated by the absorbing
   boundary; env geometry is symmetric, no invariant is touched, and the
   completion cost is bounded at ~zero by the replicate pair (same config,
   24-row positional swing, completion 0.781 both). A two-channel diagnostic
   shipped in the same commit so the grid measures it.
2. **The launch batch** — 24 runs (~$4.57) on the rented card, which
   re-measures the floors there and resolves the pre-registered ladder.
   **This is now the only thing gating the grid.**

If you are here to make progress on *content* rather than protocol, the answer
is still `env_native_prompt.md` (work package **E1**, co-active visitation,
zero compute). See *What to do next*.

---

## What was ruled, and what it changed

Full entry: `docs/decision_log.md`, **M6.2b CLOSE-OUT — CERTIFY**
(2026-08-03). Relayed in two rounds, owner-approved, transcribed before
anything was built.

| | ruling |
|---|---|
| **variance basis** | **combined form.** `sd(Γ) = √((σ_iso² + σ_joint²)/k)`. Per-arm `σ√(2/k)` is **superseded for contrasts** and survives as a labelled diagnostic. Guard-fired exception to the freeze. |
| **seeds** | **k = 40** confirmatory (**83.7 %** power@0.03 on the measured floors; the 80 % minimum is k = 37), **k = 20** secondary. |
| **T\*** | **1000**, registered in `locks.yaml` with M6.2b plateau provenance. |
| **grid** | **240 runs ≈ $45.73** at 686 s/run. |
| **budget** | **~$140 remains** for the project, **~$65 GPU** reserve-inclusive (owner, 2026-08-03). |

`CLAUDE.md`'s power standing rule now carries the contrast clause. Two new
registered analysis constants: `K_CONFIRMATORY` 34 → **40**, `K_LADDER_CAP` =
**60**. `T_STAR` moved null → 1000. All three enforced by `test_locks.py`,
which imports the module and asserts equality.

**The M6.2b report was NOT revised.** It records the constants of its era
(k = 34, per-arm basis) correctly; the ruling landed as a dated addendum.

---

## The two things that changed how the grid is graded

Both are easy to lose, and losing either would quietly invalidate a result.

### 1. The floors do not grade the confirmatory test

M6.2b's floors are **8 identical reps at one seed** — run-to-run
nondeterminism. The grid averages over **k distinct seeds**, whose per-run
variance is `σ²_rerun + σ²_seed-variation` ≥ the floor.

- **Confirmatory tests and CIs use the grid's OWN measured per-arm seed
  dispersion.**
- The floors keep two narrower roles: the **beat-reproducibility hurdle**, and
  a **design-stage power basis registered as an UPPER BOUND**. 83.7 % is a
  ceiling, not an estimate.
- **If realized power comes in lower, that is REPORTED, not re-engineered.**
  Registered in advance so it cannot become a post-hoc rescue.

### 2. The floors do not grade the grid's card either

Per-hardware **and** per-artifact both apply, and the M6.2b card is gone. No
transfer assumption was granted. The **launch batch** re-measures on the
rented card (prefer RTX PRO 6000; the two PRO 6000s used so far still differed
~15 % in throughput), then the **ladder** resolves it:

| branch | condition | action |
|---|---|---|
| **A** | k_req ≤ 40 | proceed at k = 40, surplus recorded |
| **B** | 40 < k_req ≤ 60 | raise k to k_req, **no round-trip** (+40 runs max ≈ $7.62) |
| **C** | k_req > 60 | run at k = 60, **degrade honestly** — UNDERPOWERED flag with realized power stated, verdict weight to the survival co-primary |
| **D** | survival power < 80 % too | **STOP** — broken box, not floor drift |

`m62_report.py` computes the branch and writes `ladder.json`. Derived
absorption: **B covers RMS floor growth to ~28.0 %**; k = 40 alone covers only
**4.6 %** before power falls back through 80 %. **D needs a 3.35× survival
floor move** — larger than any card excursion this project has recorded, and
in the worst one (completion 2.75×) survival was the metric that held.

**The ladder trigger is outcome-blind by construction** — `k_req` reads
fixed-seed rerun floors, which carry no cross-arm outcome information. Say
this out loud in the paper; "verdict weight shifts to survival" reads like
outcome-dependent metric selection on its face, and it is not.

**Worst realistic cost (B at cap):** $4.57 + $53.36 = **$57.93**, inside ~$65.

---

## Instrument state

`che/scripts/m62_report.py` — combined-variance power (`_sd_contrast`,
`_power_contrast`, `_mde80_contrast`), the `_k_required` solver, ladder branch
resolution, and `_power_per_arm` retained as a **diagnostic that must never
feed a verdict**. Prior fixes still in place: rule-2 mean suppression, the
`--tail` window bug fixed and hardened against the update number.

**One latent defect was found and fixed while validating the change.** An arm
with **no floor** (M6.2b's 1-rep sweep) printed `-> plateaued`: with no floor
the ratio is NaN, `NaN > PLATEAU_PASS` is False, and the arm rendered as
having passed a guard it was never graded by — *bars come with floors*
reaching the instrument through a NaN. It now prints
`NO FLOOR — UNGRADED (not a pass)` and carries `graded: false` in
`plateau.json`. **No verdict logic changed** and no past verdict moves; but
the launch batch runs a sweep arm, and a failed rep in it would have produced
a silent false pass.

**Verified this session by re-running the instrument on the real M6.2b
artifacts** (branch A, verdict PROCEED): power@k=40 = **83.7 %**, k_req = 37,
80.5 % at k = 37 and 79.3 % at k = 36, +4.6 % RMS → 80.0 %, +28.0 % → k_req
60, survival rail 3.35×. All figures use `floors.json` at full precision —
recomputing from the report's 4-dp display table runs ~0.1 pt low.

---

## What to do next

**Content, available now, zero compute:** `env_native_prompt.md` — work
package **E1, co-active visitation**. 156 eval `.npz` carry
`coupling_co_active` per-episode; it has been logged since day one on explicit
instruction (invariant #5) and **never analysed**. It is the direct observable
of the paper's central compound-hostility claim.

⚠ **The prompt's trap is live:** M6.2/M6.2b eval artifacts are Phase-6
confirmatory runs, so comparing co-active visitation between ISO and JOINT is
a **cross-arm outcome comparison, forbidden until unblinding**. E1 uses
Phase 3–5 artifacts only (115 files). The arm labels sit in the filenames and
the comparison looks scientific rather than procedural.

**Also approved, informational and non-verdict-bearing:** zero-compute
gap-sizing of seed dispersion vs the rerun floor, from Phase 3–5 multi-seed
artifacts. It sharpens what "83.7 % is an upper bound" means before the grid
runs.

**Before the grid, when a box exists:** design v2 §9's M6.1 engineering is
**confirmed shipped** at `64a7397` (a previous HANDOFF wrongly listed it as
owed). What remains is the render pass and the launch batch.

---

## Hardware / cost facts

- **RTX PRO 6000 Blackwell required.** A 31.8 GiB 5090 cannot run the gate
  config (~61.6 GiB at compile). **Never** set `--xla_gpu_autotune_level=0`.
- **686 s/run at T = 1000** on the M6.2b card (~52,000 env-steps/s); M6.2's
  card implied ~60,900 → 557 s/run. **Boxes differ ~15 % within the same
  model**, which is why the launch batch exists.
- **Gate a new box on network before shipping**: `curl` a PyPI file; 1.4 MB/s
  is too slow (~3–4 GB CUDA sync), 46 MB/s is fine. Ship **454 KB**
  (`che docs pyproject.toml uv.lock`) — not the 49 MB that includes `m06/`.
  Set `UV_HTTP_TIMEOUT=600`; the 30 s default fails on the 762 MB cudnn wheel.
- **Toolchain is pinned and the science depends on it:** Python 3.12+, jax /
  jaxlib **0.11.0**. M6.0 certified traced-θ bitwise on it; M6.2 and M6.2b
  measured under it.
- Phase-6 spend to date: ~$5.30 (M6.2 ~$2, M6.2b ~$3.30).

---

## OWED — two things this session left unverified (2026-08-04)

Both are consequences of adding the coupling counters to the training logger
(`docs/decision_log.md`, *TRAINING LOGGER GAINS THE COUPLING COUNTERS*).

1. ~~**The CPU test chunk `test_ippo test_pbt test_metrics test_locks` was
   KILLED, not passed**~~ — **DISCHARGED 2026-08-10.** All four files ran
   green, chunked and thread-capped, against both the coupling counters and
   the render-gate channels on top of them.
2. **The throughput cost of the added channels is UNMEASURED.** A CPU A/B was
   running and was killed before it flushed, so there is no number at all —
   not even an indicative one. See the GPU plan below; this is the main
   reason to want a box. **Widened 2026-08-10:** the A/B now covers **eight**
   channels, not six — the render-gate diagnostic added `center_dist_sum`,
   `boundary_agents` and the `alive_agents` denominator to `STEP_METRICS`.
   Unchanged in kind, and the fallback (log a subset) still applies and is
   still a human call. **ORDERING, ruled 2026-08-10: the A/B must precede the
   launch batch.** Its `> 15 %` branch is *drop channels*, which changes the
   artifact — and floors are per-artifact, so a batch run first would measure
   floors on an artifact the grid might not use.
3. **NEW 2026-08-10 — the bench's `training` keep-alive set had drifted, and
   is fixed.** `throughput.py::_training_info_keys()` enumerated `EP_METRICS`
   only, so from 2026-08-04 — when `STEP_METRICS` was added as a *second*
   table — every `training`-mode env-only row measured an env whose newest
   channels XLA was free to delete. Exactly the M5.1 defect, one table later.
   It now enumerates both tables, and `test_positional_drift.py` asserts the
   superset so a third table fails loudly. **No verdict moves** (gates were
   re-anchored to `pbt.py --bench` long ago), but every training-mode row
   since 2026-08-04 **undercounts** and should not be compared to rows taken
   before it.

## Open threads

- **`m06/` is 47 MB** of pre-M6.0 spike leftovers at the repo root — still
  undecided whether it belongs in the tree.
- **`test_prop3`, `test_calibration`, `test_percolation`** are slow MC files;
  isolate them when running the suite.
- ~~**24 M5.5 renders un-inspected**~~ — inspected and ruled 2026-08-10; no
  longer gates the grid. **Two things it left owed:** the per-artifact floor
  for the two new drift channels, measurable only from the grid's own seeds
  (until then neither channel grades anything — and note the grid **records**
  them without **grading** them: `m62_report.py::METRICS` is deliberately
  untouched, because that tuple is the registered confirmatory family at
  `SIDAK_M = 2` and no diagnostic is worth enlarging it post-registration, so
  the floors need their own post-grid instrument). The **endogeneity family**
  is now **enumerated and canonical** (`decision_log.md`, *RENDER-GATE
  RULINGS, ROUND 2*, ruling 3) — five named members, one of them REFUTED and
  deliberately retained. **The paper cites members by name, never by
  ordinal.**
- **Design v2 §5 and §7 owe a text update** to state the upper-bound framing
  and the seed-dispersion test basis. Ruled, not yet written into v2.

---

## Working agreements

- **Rulings bind only once transcribed** into `decision_log.md` or `CLAUDE.md`
  **in the same session**. This session verified a relayed ruling cited a
  budget document that **does not exist**; it was registered as new rather
  than cited as prior law.
- **Numbers enter documents derived or measured in the same session.** Two
  relayed ladder figures (~22 % absorption, ~$3.5) were corrected on
  derivation to **28.0 %** and **$1.91**, and a relayed cost attribution was
  corrected — against the tree's own baseline the largest component is **card
  throughput**, not plateau-doubled T.
- **Bars come with floors** — per-metric, per-hardware **and** per-artifact.
- **Contrasts are graded on the contrast's SE** (new, 2026-08-03).
- **Design-stage power statements are 80 %-power MDEs** at the family-corrected
  α, never bare 2σ√(2/k).
- Run the CPU suite **chunked and thread-capped**; an unbounded run once
  crashed the machine.
- **Milestones marked STOP end the turn: report and wait for the human.**
