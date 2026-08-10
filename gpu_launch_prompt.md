# Work package G1 — the GPU trip: bench, re-floor, ladder, grid

> Fresh session at repo root, on or about to rent an **RTX PRO 6000 Blackwell**.
> Milestone by milestone. **STOP and report at every STOP marker.** Do not
> collapse two milestones into one run.
>
> Written 2026-08-04 at `d513e2f`. If `git log -1` does not show that commit or
> a descendant, **stop and reconcile before spending money.**
>
> **RECONCILED 2026-08-10 at `9ea5629`** (a descendant — the check passes).
> Three preconditions moved; full entry `docs/decision_log.md`,
> *RENDER-GATE RULINGS, ROUND 2*:
>
> | | was | now |
> |---|---|---|
> | **G1.0(a)** test chunk | owed (SIGTERM-killed) | **DISCHARGED** — green locally; keep as a box smoke test |
> | **G1.0(b)** throughput A/B | owed, 6 channels | **still owed, now 8 channels** |
> | **G1.1** owner render pass | owed, gates the grid | **DISCHARGED** — inspected and ruled |
>
> **The ordering in G1.0(b) is now load-bearing, not hygiene.** Its `> 15 %`
> branch is *drop channels*, which changes the artifact — and floors are
> per-artifact. Running G1.2 first would measure floors on an artifact the
> grid might not use. **A/B before batch. No exceptions.**

---

## 0. Read these first, in this order

1. `CLAUDE.md` — the invariants and the standing rules. Non-negotiable.
2. `HANDOFF.md` — especially **OWED**, which lists what this session must close.
3. `docs/decision_log.md` from **`## M6.2b CLOSE-OUT — CERTIFY`** to the end.
   That entry contains the ladder you will execute in G1.2. Read the
   **TRAINING LOGGER GAINS THE COUPLING COUNTERS** entry immediately after it.
4. `che/bench/results/phase6/m62b/m62b_report.md` **including its ADDENDUM**.
5. `phase6_design_v2.md` §§1–7 — the registered design you are running.

**Do not re-rule anything.** `k = 40`, `T* = 1000`, the combined-variance
basis, the ladder and the budget are all registered. If you believe one is
wrong, **STOP and say so**; do not quietly act on it.

---

## The state you are inheriting

- **Phase 6 is certified and the grid is authorized at 240 runs.** The M6.2b
  power STOP was discharged 2026-08-03.
- **No GPU box is running.** The card that measured the M6.2b floors is gone.
- **Floors are per-hardware AND per-artifact**, so the M6.2b floors do **not**
  grade a run on a newly rented card. That is why G1.2 exists.
- **The training loop changed on 2026-08-04** (six coupling channels added to
  the logger). That change is *additive and bitwise-safe for the env*, but it
  makes the env compute channels XLA previously deleted. **Its throughput cost
  is completely unmeasured.** That is why G1.0 exists and why it runs first.

### Two things are OWED before any spend

1. ~~**`test_ippo test_pbt test_metrics test_locks` has never been run against
   the logger change.**~~ **DISCHARGED 2026-08-10** — green locally, against
   the coupling counters *and* the render-gate channels on top of them. Still
   worth running on the box, as a toolchain smoke test rather than a debt.
2. **The throughput A/B is unmeasured** — the local attempt was killed before
   it flushed. There is no number, not even indicative. **Widened 2026-08-10
   to eight channels**: the render gate added `center_dist_sum`,
   `boundary_agents` and the `alive_agents` denominator to `STEP_METRICS`.
   The `.clear()` mechanism below is unaffected and now measures all eight.
   **This is the only remaining pre-spend debt, and it must run first.**

---

## Before you rent — the box gate (do not skip, it has bitten this project)

- **RTX PRO 6000 Blackwell required.** The gate config needs **~62 GiB at
  compile**. A 31.8 GiB 5090 **cannot** run it. **Never** work around this with
  `--xla_gpu_autotune_level=0`.
- **Gate on network before syncing.** `curl` a PyPI file and measure. **1.4 MB/s
  is too slow** (there is a ~3–4 GB CUDA sync); **46 MB/s is fine**. A slow link
  is a reason to switch boxes, not to wait.
- **Ship ~454 KB, not 49 MB**: `che docs pyproject.toml uv.lock`. Do **not**
  ship `m06/` (47 MB of dead spike leftovers at the repo root).
- **`export UV_HTTP_TIMEOUT=600`** — the 30 s default fails on the 762 MB cudnn
  wheel.
- **Toolchain must be Python ≥ 3.12 and jax/jaxlib 0.11.0.** `uv.lock` pins
  this. Verify on the box before running anything:
  ```
  uv run python -c "import sys, jax, jaxlib; print(sys.version.split()[0], jax.__version__, jaxlib.__version__, jax.devices())"
  ```
  **If it reports jax 0.10.2, STOP.** That means the venv resolved on Python
  3.11 and you are on a different toolchain from every Phase-6 measurement.

---

## G1.0 — Close the owed items, before spending anything

**This is cheap and it protects everything downstream.**

**(a) Run the killed test chunk.**
```
uv run pytest che/tests/test_ippo.py che/tests/test_pbt.py \
               che/tests/test_metrics.py che/tests/test_locks.py -q
```
**If RED → STOP.** `CLAUDE.md` forbids starting a milestone on a red tree, and
the most likely failure is the new `Transition.step_metrics` field.

**(b) Measure the logging cost — the A/B that has never been run.**

The standing throughput rule binds gates to **measured training throughput of
the spending consumer**, which is `pbt.py --bench` at `configs/gate_pop12.yaml`.
Run it twice: once as-is, once with the channels disabled.

To disable without editing tracked code, set the table empty at import:
```
uv run python -c "
import che.train.ippo as ippo; ippo.STEP_METRICS.clear()
import sys; sys.argv=['pbt','--config','che/configs/gate_pop12.yaml','--bench','--windows','5','--window-secs','30']
from che.train.pbt import main; main()"
```
then the same without the `.clear()`. **Record both aggregate steps/s figures
and the percentage delta in the report.**

**Interpreting it — the rule is fixed here, before you see the number:**

| measured delta | action |
|---|---|
| **< 5 %** | absorb it. Note in the report; the 686 s/run basis stands. |
| **5–15 %** | proceed, but **re-derive the run cost** at the new rate and restate the grid cost before G1.3. |
| **> 15 %** | **STOP and report.** The fallback is logging a *subset* — `coupling_co_active` alone answers the question the channels were added for — but dropping channels is a **human call**, not yours. |

**Deliverable:** test chunk green + the A/B numbers. **STOP and report.**

---

## G1.1 — DISCHARGED 2026-08-10 (was: the owner render pass)

~~The 24 M5.5 renders remain un-inspected.~~ **Inspected and ruled.** The
bottom-clustering is a per-training-run residual action bias integrated by
the absorbing boundary; env geometry is symmetric, no invariant is touched,
and the completion cost is bounded ≈ 0 by the replicate control (same config,
24-row positional swing, completion 0.781 both). Ruled **not a launch
blocker**; two diagnostic channels shipped so the grid records it.

Full entries: `docs/decision_log.md`, *RENDER-GATE FINDINGS* and *RENDER-GATE
RULINGS, ROUND 2*.

**This was closed by a ruling, not waived** — which is what the original
instruction here asked for.

---

## G1.2 — The launch batch and the ladder

**24 runs ≈ $4.6.** This re-measures the floors on the card you actually
rented, then resolves a **pre-registered** branch. You execute the branch; you
do not choose it.

```
GIT_COMMIT=$(git rev-parse HEAD) \
OUT=che/bench/results/phase6/g1_floors \
UPDATES=1000 REPS=8 \
bash che/scripts/run_m62b_t1000.sh 2>&1 | tee g1_floors_console.log
```

Notes on that command:
- `OUT` **must be a fresh directory**. The script refuses a non-empty one, and
  refuses to write into the T = 500 milestone dir. Do not defeat either guard:
  floors are per-artifact and mixing run lengths yields a `floors.json` that
  grades nothing.
- The script runs its own pre-flight tests, archives checkpoints, and appends
  toolchain provenance. Let it.
- It runs 3 arms × 8 reps: ISO, JOINT-classic, **and the sweep p = 0.5 arm**
  whose floor M6.2b never obtained (its run was cut at 1 rep by a mains outage).

### Then compute the branch

```
uv run python -m che.scripts.m62_report \
  --out che/bench/results/phase6/g1_floors --reps 8 --updates 1000 \
  --arms "iso:che/configs/p6_iso.yaml joint:che/configs/p6_joint.yaml sweep_p500:che/configs/p6_sweep_c50_p500.yaml"
```

It prints `RE-FLOOR LADDER: BRANCH <X>` and writes `ladder.json`. **Execute
exactly this:**

| branch | condition | what you do |
|---|---|---|
| **A** | `k_req ≤ 40` | Proceed to G1.3 at **k = 40**. Record the surplus. |
| **B** | `40 < k_req ≤ 60` | Proceed to G1.3 at **k = k_req**, **no round-trip**. Log k and the derived cost delta. |
| **C** | `k_req > 60` | Run G1.3 at **k = 60** and **degrade honestly**: completion-Γ carries a pre-registered UNDERPOWERED flag with realized power stated, and verdict weight moves to the **survival co-primary**. **Never chase power beyond 60.** |
| **D** | survival power **also** < 80 % | **STOP.** That is a broken box, not floor drift. Release it, rent a different one, restart at G1.0. |

**Also check the plateau output.** Any arm printing `NO FLOOR — UNGRADED (not
a pass)` means a rep failed and that arm has no floor — investigate before
proceeding; it is not a pass.

**Deliverable:** fresh floors, the branch, and the plateau verdict.
**STOP and report** — even on branch A. The owner wants to see the branch
before $46 is spent.

---

## G1.3 — The grid

**240 runs at k = 40 (or 280 at k = 60 under branch C) ≈ $46–53.**

- **Confirmatory:** ISO and JOINT-classic at θ\*, k per the branch.
- **Secondary:** dose sweep c = 0.5 at p ∈ {0, .125, .25, .375, .5} and the
  identification arm c = 0.4 at p ∈ {0, .2, .4}, **k = 20** each. These do not
  gate anything.
- **θ\* is `che/configs/theta_star_holdout.yaml`** — all elements on at
  β = 0.49, a severity **neither** protocol trains on.

### Traps, each enforced or previously paid for

- **Never train on `joint_medium.yaml`.** It is θ\*'s severity; training on it
  destroys the held-out property Γ depends on. `test_phase6_configs.py` asserts
  no training config carries β = 0.49 — do not disable it.
- **NO-PEEKING is still in force.** Do not compute, print or discuss any
  cross-arm outcome comparison until unblinding. Per-arm floors and drift
  ratios are fine; per-arm **outcome means** are not. The report script
  suppresses them mechanically — do not add them back.
- **The pipeline freezes by commit hash before unblinding.** Record the hash.

**Deliverable:** the grid artifacts, archived. **STOP and report. Do not
unblind.** Unblinding is a separate, human-gated step.

---

## Artifact persistence — asserted, not optional

**Every GPU run persists metrics + provenance + a checkpoint archive
(`tar.zst` + `sha256`) off-instance before the instance is released.** The job
scripts assert this; if an assertion fails, fix it rather than bypassing it. A
rented box is ephemeral and an un-archived checkpoint is a result nobody can
re-render, re-probe or audit.

Before releasing the box, verify hashes match what you pulled, and record
"N OK, 0 mismatched" in the report.

---

## Budget

**~$140 remains for the project; ~$65 is the GPU allocation, reserve-inclusive.**

| item | ≈ cost |
|---|---|
| G1.0 A/B | ~$1 |
| G1.2 launch batch (24 runs) | ~$4.6 |
| G1.3 grid at k = 40 (240 runs) | ~$46 |
| **total** | **~$52** |
| worst realistic (branch B at cap, 280 runs) | ~$58 |

Both fit. **If your running total is heading past $65, STOP and report** — do
not quietly shrink the design to fit, and do not quietly overspend.

---

## Working rules that bind this session

- **Rulings bind only once transcribed** into `docs/decision_log.md` in the
  same session. A relayed instruction is a proposal until you write it down.
  **Relays in this project have twice cited documents that do not exist —
  verify before transcribing.**
- **Numbers enter documents derived or measured in the same session.** Every
  figure in this prompt is a pointer to a source, **not a citable value** —
  re-derive before quoting.
- **Bars come with floors** — per-metric, per-hardware **and** per-artifact.
- **Contrasts are graded on the contrast's SE**, not either arm's.
- After each milestone: `ruff check che/`, the test chunk, and a commit naming
  the milestone.
- **Milestones marked STOP end the turn: report and wait for the human.**

## Non-goals

- Re-ruling `k`, `T*`, the variance basis, the budget or the ladder.
- Unblinding, or any cross-arm outcome comparison before it.
- Touching `che/env/`, `docs/locks.yaml` or any registered constant.
- E1 follow-on work (E1 is complete at `e646758`).
