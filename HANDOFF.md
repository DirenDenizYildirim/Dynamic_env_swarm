# HANDOFF — session state for the next model (written 2026-08-13)

You are picking up **mid-Phase-6, pre-grid, pre-unblind.** There is **no GPU
box running**. Every gate that blocked the grid on a *decision* is discharged;
what remains is a rental and two owner ratifications.

**The grid is now runnable.** `che/scripts/run_p6_grid.sh` exists as of this
session — it did not before, which was the real pre-rental gap and was found
by the previous session's own T\* commit.

---

## What has happened since the last HANDOFF (which was written 2026-08-03)

That HANDOFF said "the launch batch is the only thing gating the grid." That
is **wrong now, on two counts**: the launch batch ran, and a missing script
gated the grid behind it.

| | state |
|---|---|
| **G1.0(a)** owed test chunk | discharged 2026-08-10 |
| **G1.0(b)** throughput A/B | **discharged** 2026-08-11 — nine added channels cost **< ~0.25 %**. No channel dropped, so the artifact the floors grade is final. `g1/g1_0b_throughput_ab.md` |
| **G1.1** render pass | discharged by ruling 2026-08-10 |
| **G1.2** launch batch | **RAN** 2026-08-10, 24 runs, 3h27m, ~$4.6. **BRANCH A**: k_req = 11 completion / 5 survival against k = 40, realized power 0.9999. `g1/g1_2_report.md`, `g1_floors/ladder.json` |
| **plateau guard** | **STOPped** — and the STOP is **discharged** by the T\* ruling (2026-08-11), which **retired the criterion** |
| **the card** | **RELEASED.** Floors are per-hardware; the next trip **must re-run G1.2 before G1.3** (~$4.08) |

### The T\* ruling, in one paragraph

The plateau criterion was retired as a certification instrument because it is
**detectability-relative**: `drift / floor` with `floor → 0` fails for any
nonzero drift, so it cannot certify on a perfect instrument. It survives
demoted, grading nothing. In its place the **estimand is fixed explicitly** —
primary Γ is the confirmatory contrast at **matched budget T = 1000**, and
*"at convergence" is never claimed anywhere*. **Γ(t) was promoted from
descriptive to REQUIRED robustness evidence** with a pre-registered reading
rule (sign stability over the final half; instability **is** the finding),
mechanised as 11 retained checkpoints on the confirmatory arms only,
**evaluated post-unblind**. T = 2000 was declined. Full entry:
`docs/decision_log.md`, *T\* RULING*.

---

## The grid script — what it is and the three decisions it flags

`che/scripts/run_p6_grid.sh`, asserted by `che/tests/test_p6_grid.py`
(18 tests, including two that drive the whole script end-to-end on
`debug.yaml` in about a minute).

240 runs: confirmatory ISO + JOINT at k = 40, dose sweep c = 0.5 at five p
points and identification c = 0.4 at three, k = 20 each. Resumable via
`lib_run_manifest.sh`, which was written last session and until now was wired
into nothing.

**It computes no cross-arm quantity and there is no analysis call in it.** A
test asserts that. Unblinding is a separate, human-gated step on a frozen tree.

### Three builder decisions, OWED RATIFICATION

The locks fix **how many** seeds; they do not fix which integers, in what
order, or against which eval draw. All three are stated in the script header
with their reasoning, and all three are asserted by tests.

1. **Seeds are 1..k, the same integers in every arm.** Starting at 1 is
   load-bearing: **the floor runs are seed 0**, so a grid run at seed 0 on
   iso/joint/sweep_p500 would be a reproducibility rep wearing a seed's name,
   contributing zero seed variance to the dispersion the confirmatory test
   divides by. Sharing integers across arms is the **conservative** direction:
   the registered `sd(Γ)` is the unpaired combined form, so any positive
   cross-arm covariance makes it an over-estimate.
2. **The eval set is a constant** — seed 0, 512 episodes, every run. Identical
   to the floor protocol, so floors and grid are one instrument, and cross-run
   variance is training-seed variance rather than training-seed plus
   eval-sampling noise.
3. **Run order is seed-major, arm-minor.** Arm-major ordering loses the whole
   rental to a mid-run box failure (a complete ISO arm, a partial JOINT arm,
   no Γ at any k). Seed-major truncation instead yields a smaller **balanced**
   design, so an interruption costs **power, not validity**. This is not a
   licence to stop early and pick k afterwards.

### Guards worth knowing before you run it

- **Parameter-identity stamp** replaces the floor script's refuse-nonempty
  guard, which resume makes unusable. T\*, k, arm set, eval config and eval
  seed are stamped on first run and re-checked on resume; a mismatch is
  refused. Without it the per-artifact protection is simply absent from the
  larger run.
- **`ckpt_step == T*` asserted per run.** The harness defaults to
  `latest_step()`, which is correct and *silently correct-looking* if the
  step-1000 save never landed. It also makes the retention change auditable:
  the confirmatory arms now keep 11 checkpoints while the G1.2 floors were
  measured on 3-checkpoint artifacts, and **the floors transfer only because
  both evaluate the final step**.
- **Raw checkpoint dirs are reclaimed** after the archive lists successfully
  (`tar -tf`, not merely a hash of a file nobody read back). 240 of them do
  not fit beside their archives.
- **3 consecutive failures aborts**; isolated failures are tolerated and
  retried by re-running the identical command. The final assertion checks
  every tag **by name** and re-hashes its archive — counts are not trusted.

---

## What to do next

### 1. Two ratifications, both $0, both pre-rental

- **`phase6_framing_branches.md`** — outcome-conditional framing, drafted
  2026-08-11, **still untracked and unratified**. It registers what the paper
  claims as a function of the confirmatory outcome, decided before the outcome
  exists. It also asks two questions it cannot answer itself (§6 items 1–2:
  whether branch B has a refuting completion effect size, and whether branch
  D's threshold should be a number). **Both must be settled pre-unblind or
  not at all.**
- **The three grid-script decisions above.**

### 2. The rental, one trip

`G1.2 re-floor (~$4.08) → ladder → G1.3 grid (~$40.9) → post-unblind Γ(t)
eval (~$3.60)`. Registrar's projected trip total **~$48.6** against a **~$65**
GPU reserve. The $45.73 grid authorization stands as-registered; the Γ(t)
block is a **reserve draw**, not an authorization amendment.

Read `gpu_launch_prompt.md` before renting. Its G1.0/G1.1 sections are
discharged history; **its G1.3 section still carries no command block** — use
`run_p6_grid.sh`.

### 3. Free work if there is no box

- **Release hygiene** (framing §7): `README.md` is 24 bytes, `m06/` is 47 MB
  of undecided pre-M6.0 spike leftovers, the repo root carries console logs
  and phase prompts. This has a deadline attached: **deferring it selects
  RA-L by default**, because the D&B branch needs a releasable artifact and
  the window after the grid is thin.
- **Design v2 §5 and §7** owe a text update stating the upper-bound framing
  and the seed-dispersion test basis. Ruled, still unwritten.
- **The three no-scoop checks** (positioning rulings §1, owner tasks, open).

---

## Still owed, carried forward

- **Per-artifact floors for the two render-gate drift channels**, measurable
  only from the grid's own seeds. Until they exist **neither channel grades
  anything** — and note the grid **records** them without **grading** them:
  `m62_report.py::METRICS` is deliberately untouched, because that tuple is
  the registered confirmatory family at `SIDAK_M = 2` and no diagnostic is
  worth enlarging it post-registration. The floors need their own post-grid
  instrument.
- **The endogeneity family is enumerated and canonical** (`decision_log.md`,
  *RENDER-GATE RULINGS, ROUND 2*, ruling 3) — five named members, one REFUTED
  and deliberately retained. **The paper cites members by name, never by
  ordinal.**
- **Training-mode env-only bench rows taken between 2026-08-04 and
  2026-08-10 undercount** (the keep-alive set had drifted to enumerate
  `EP_METRICS` only). Fixed; no verdict moves; do not compare across that
  boundary.
- **`test_prop3`, `test_calibration`, `test_percolation`** are slow MC files —
  isolate them when running the suite.

---

## Hardware / cost facts

- **RTX PRO 6000 Blackwell required.** A 31.8 GiB 5090 cannot compile the gate
  config (~61.6 GiB at autotune). **Never** set `--xla_gpu_autotune_level=0`.
- **Measured rate $1.2358/h** (`vastai show instances`, id 47454262) — not the
  ~$1.00/h the earlier projections assumed, which understated everything 24 %.
- **497 s/run at T = 1000** on the G1.2 card (686 s on M6.2b's). **Boxes differ
  ~15 % within the same model**, which is why the re-floor is not optional.
- **Gate a new box on network before shipping**: `curl` a PyPI file; 1.4 MB/s
  is too slow, 46 MB/s is fine. Ship **454 KB** (`che docs pyproject.toml
  uv.lock`), not the 49 MB that includes `m06/`. Set `UV_HTTP_TIMEOUT=600`.
- **Toolchain is pinned and the science depends on it:** Python 3.12+, jax /
  jaxlib **0.11.0**.
- Phase-6 spend to date: **~$9.9** (M6.2 ~$2, M6.2b ~$3.30, G1.0b+G1.2 ~$4.6).

---

## Working agreements

- **Rulings bind only once transcribed** into `decision_log.md` or `CLAUDE.md`
  **in the same session**. Relays in this project have twice cited documents
  that **do not exist** — verify before transcribing.
- **Numbers enter documents derived or measured in the same session.**
- **Bars come with floors** — per-metric, per-hardware **and** per-artifact.
- **Contrasts are graded on the contrast's SE**, not either arm's.
- **Design-stage power statements are 80 %-power MDEs** at the family-corrected
  α, never bare 2σ√(2/k).
- **Instruments state what they are blind to**, and **recording a channel is
  not grading it**.
- Run the CPU suite **chunked and thread-capped**; an unbounded run once
  crashed the machine.
- **Milestones marked STOP end the turn: report and wait for the human.**
