# HANDOFF — session state for the next model (written 2026-07-30)

You are picking up at the **Phase-5 close**. Read, in order, before doing
anything: `CLAUDE.md` (invariants — non-negotiable, and note the two rules
added 2026-07-30), `docs/decision_log.md` from "M5.3 CLOSURE RULING"
onward, and `che/bench/results/phase5/phase5_report.md`.

**Do not start Phase 6.** The PHASE 6 ENTRY GATE is a human decision and it
has grown a queue (below).

## Where things stand

- **Phases 0–5 complete.** Severities β = 0.43/0.49/0.70 (β̂_c = 0.500),
  κ_A = 0.06, κ_B = 1.0, d_p = 0.5, obs v3, **δ = 1.0 and R_comm = 16**
  (`comms_lock.md`).
- **Phase 5's result is a certified negative.** Communication is worth
  nothing measurable to this swarm: five content-ablation arms across two
  severities and two connectivity regimes, plus total denial, all null.
  Theory predicted it (Remark 2″(i) — redundancy substitutes). The
  load-bearing evidence is the **unused connectivity bit**: that signal
  needs no encoder, so its neglect is demand-side, not a limitation of the
  frozen random-projection channel. DIAL was formally declined with
  reasons; the paper carries "gradient-shaped messaging remains untested".
- Suite green, `ruff` clean. Run the suite **chunked and thread-capped** —
  an unbounded `pytest che/tests` once crashed the machine:
  `OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 nice -n 15 uv run pytest <subset>`.

## Added 2026-08-01/02 — the Phase-6 red team, and the M6.0 spike

**Read `phase6_redteam_v1.md`, then `phase6_redteam_remedies.md`.** The
design v1 was reviewed and **must not be registered as written**. All four
open findings were RULED on 2026-08-02 (`decision_log.md`, "PHASE-6 REMEDY
RULINGS"); the remedies doc records the options and which were selected.

**The four rulings, in one line each:**
1. **θ\* siting** — train on the EXTREMES {0.43, 0.70}, hold out the MIDDLE
   (θ\* = 0.49). Def. 8 satisfied literally, both couplings live, smallest
   floors. **`beta_holdout` is now resolved to a MEASURED value** and
   `theta_star_holdout.yaml` loads.
2. **Estimand** — endpoints (ISO vs JOINT-classic) confirmatory; matched
   sweep secondary with its no-element gradient reported; **c = 0.4
   identification arm** so the confound is bounded, not just noted.
3. **Seeds — k = 20** uniformly (~$15). At k = 4 completion was unresolvable
   before a single run.
4. **Floors — 8 reps** per evaluation config, before any bar, on the grid's
   card, **per-arm** (per-artifact rule).

Still unruled: the ablation certification table (15 runs for a property
`test_nesting.py` already proves).

**Do NOT train on `joint_medium.yaml` in Phase 6** — Medium is θ\*'s
severity now, and training on it would destroy the held-out property Γ
depends on. Flagged in `locks.yaml`.

The findings that produced those rulings, for context — the three fatal
ones:

1. **§6 costs Phase 6 from row A (142,421 steps/s)** — `m06_probe.yaml`,
   `obs_window` 5, elements off. `phase5_report.md:119` calls that "a drift
   reference, **not the gate**", and the report's own table has the gate at
   62,084. It is the ÷81 pattern a fourth time. §3 also registers all evals
   onto a 5090 the same report measured as non-viable.
2. **Every bar in §5 is void**: floors come from Medium, the evaluation is at
   β = 0.46/0.60 where **no floor has ever been measured**, and survival
   floors move **4.8×** across severity (0.0130 → 0.0621).
3. **k = 4 seeds is ~5× too small** — completion MDE 0.0564 against
   historical effects ≤ 0.03. And seeds are nearly free: `m55/timings.txt`
   measures a 500-update run at **257 s ≈ $0.07**. The whole redesign at
   k = 20 is ~$15.

Plus: §1's fixed-margin mixture cannot be clean (a 2×2 table with fixed
margins has one degree of freedom, so no-element time moves 1:1 with
co-occurrence — and the draft's own sign check is backwards), and **both
held-out severities are where composition is weakest** (Coupling A is
fuel-limited at high β, Coupling B near-dead at low β — neither point has
both elements live). The proposed v2 fix is to separate the two
generalization axes; it costs nothing.

**M6.0 spike: COMPLETE, all four acceptances met.** See
`che/bench/results/phase6/m60/m60_report.md`.

- Theta is now **per-env traced** ({β, κ_A, κ_B, δ} in `EnvState.theta_live`)
  and sampled at reset/autoreset from a `MixtureConfig`. **2a: bitwise, 1520
  field digests, 0 changed.** 2b: nesting suite green, unmodified.
  **2c: DCE tax ≤ 0.62 %** — and below the instrument's own jitter on the
  gate config; memory +30,720 B. **2d: realized mixture 0.7425 vs 0.75
  declared over 6,400 episodes.**
- **The precompiled-variant fallback is not needed** and can be dropped from
  the design along with its granularity cost.
- **Theta binds at RESET, not at step time.** A mid-episode
  `replace(cfg, theta=…)` is now silently inert. Production is unaffected
  (all CLI overrides are applied in `main()` before reset) and both
  directions are asserted in `che/tests/test_traced_theta.py`.
- `zeros_state` now **requires** `theta_live`. That caught a Coupling-B test
  that had been **passing for the wrong reason** with masking silently off.
- Owed before any ≥3-component design: **per-component count logging** (a
  mean over component indices only reads as a ratio for two components).
- **Per-artifact floors are now REPO LAW** (CLAUDE.md, adopted 2026-08-02):
  measure the floor on the artifact being graded, never on its reference.
- **GPU ladder finding that produced that rule.** On GPU, two
  Def.-2 diagnostics (`masked_frac`, `masked_danger_sum`, High seed 0)
  differ run-to-run. It first read as a real traced-vs-folded difference
  because the floor had been measured on the BASELINE tree — which is
  deterministic (0/4) — while the instability lives in the traced tree
  (1/4 against itself). No trajectory field differed in any of 13
  comparisons; CPU is unaffected. **Floors are per-metric, per-hardware and
  — this is the new part — PER-ARTIFACT: measure the floor on the thing
  being graded, not on its reference.** Operational form: an equivalence
  claim between A and B needs A-vs-A and B-vs-B, not just A-vs-B — two
  deterministic artifacts cannot compare intermittently.

## Added 2026-07-31 — locks are now enforced by test

A read-only structural review found a locked constant that **no config
could reach**: R_comm was locked at 16 on 07-30 and `ThetaConfig.r_comm`
still defaulted to 8.0, with the locked geometry supplied only by
`--r-comm 16` inside two shell scripts. Consequence check came back clean —
**M5.5 ran at R = 16** (its own `provenance.txt`; measured out-degree 3.213,
the R=16 geometry) — so the inertness certificate covers the locked
geometry and nothing needed re-running.

What changed, all in `docs/decision_log.md` under "REPO-EXPLORER RULINGS":

- **`docs/locks.yaml`** is now the single machine-readable registry of every
  locked constant, and **`che/tests/test_locks.py` (35 tests)** asserts
  configs and dataclass defaults agree with it. The load-bearing assertion
  is anti-inheritance: a locked value must be *written* in the configs that
  carry it. **New standing rule in CLAUDE.md: every lock lands in
  `locks.yaml` in the same commit it is ruled.**
- `r_comm: 16.0` and `death_penalty: 0.5` are now written into the severity
  configs. **No past run changes** — every Phase-3/4/5 script passed both
  as flags already. A bare `--config severity_*.yaml` run no longer
  silently violates D4.
- **`joint_{low,medium,high}.yaml`** — all elements ON (δ = 1.0) at the
  three calibrated severities. This is the JOINT protocol's multi-element
  training support (Def. 8), not θ*.
- **`theta_star_holdout.yaml`** — the Def.-8 held-out composition point.
  **It does not load, on purpose**: β is the sentinel
  `PENDING_PHASE6_CALIBRATION` and `load_config` raises on it. Every other
  locked value is written out. Fill it in only after the entry gate fixes
  *and calibrates* the held-out β; `beta_holdout.value` in `locks.yaml` is
  null until then, and the test tripwire refuses any unregistered β.
- CLAUDE.md's **layout block** was refreshed (it had omitted
  `che/calibration/` and `che/eval/` entirely) and a **phase-close
  checklist** added, whose first item is keeping it refreshed.

**This adds a ninth entry-gate item, implicitly: the held-out β is now a
loud missing value in the tree.** It is entry-gate item 1's output.

## Two rules added 2026-07-30 — read them before writing any script

1. **Bars come with floors** (`CLAUDE.md`). No acceptance threshold enters
   a script without a measured floor for the quantity it grades, or an
   explicit UNDERPOWERED flag. **Thresholds finer than their instruments
   are void by construction** — void, not failed, because they would void
   a PASS identically. Four bars in one phase were set without floors and
   each was wrong. Floors are **per-metric AND per-hardware** facts.
2. **Throughput figures state their XLA flags** (proposed by the RA, in
   the decision log; the standing keep-alive-set rule is its sibling). The
   same config measures 3,795 and 62,084 steps/s on one flag.

## Hardware — the plan changed on measurement

**A 31.8 GiB 5090 cannot run `configs/gate_pop12.yaml`.** Autotuning on
needs ~61.6 GiB *at compile*; autotuning off fits but is 16.4× slower
(→ 6,295 GPU-hours). Both fail. Phase 5 finished on an **RTX PRO 6000
Blackwell (96 GB, ~$1/h) at 62,084 steps/s** — one 1000-update population
run costs **$0.88** and takes 53 min. **No box is running**; that instance
was destroyed after all artifacts were pulled and sha256-verified.

Never set `--xla_gpu_autotune_level=0` on this workload. Toolchain matters:
the same config measured 24.69 GiB on one rental and 27.53 on the next,
from a jax/jaxlib change alone.

## The PHASE 6 ENTRY GATE queue (all human-owed)

Original four: (1) dose-response design formalized into the phase prompt;
(2) pilot scoped to 2 mixture points; (3) one-paper vs two-paper fork
scheduled after the pilot; (4) power analysis from the **measured**
reproducibility floors, checking the registered 4 seeds/point against them.

Added this session:

5. **Budget decomposition** — 86e9 planned steps has **no bottom-up
   derivation anywhere in the repo**. It is the same computation as the
   power analysis (runs = design × seeds-from-floors, costed at $0.88/run).
   A realistic Phase 6/7 is ~$81, so **money is not the constraint —
   wall-clock and statistical power are**.
6. **Hardware**, given the 5090 is out.
7. **Composition is effectively {Coupling A, Coupling B}**; δ = 1.0 is
   retained in θ* for registration fidelity at zero cost. The
   dose-response x-axis (A×B co-active visitation) is unaffected.
8. **Power reality:** High resolves only ~11-point effects (floor
   completion 0.0522 / survival 0.0621) where Medium resolves ~3
   (0.0399 / 0.0130). Any High claim needs a huge effect or many seeds —
   ~46 seeds/arm to reach Medium's bar. Design Phase 6 knowing this.

## Open threads (small)

- **24 M5.5 renders are un-inspected** — the branch-loitering /
  information-buying watch item is genuinely open
  (`che/bench/results/phase5/m55/renders/`).
- **M5.1k lever sweep truncated at 3/6 rows** (instance stopped
  mid-sweep). The two informative rows already answered it: there is **no
  free throughput win**; more concurrent envs are marginally *worse*.
- **Untracked/deleted in the worktree, deliberately left alone:**
  `phase4_prompt.md`, `phase5_prompt.md` untracked; `phase2_results.zip`,
  `phase3_prompt.md` deleted. Ask before reconciling.

## Working agreements

- GPU jobs: no local CUDA. Either hand the user scripts in `che/scripts/`,
  or — as on 2026-07-30 — drive a box directly over SSH if given access.
  Launch detached with `nohup`, poll in separate calls, `scp` artifacts
  back, **verify sha256 before releasing any instance**. Watch out:
  `pkill -f <pattern>` matches your own SSH command line.
- After each milestone: `uv run ruff check che/`, the chunked CPU suite,
  commit naming the milestone. Never start the next milestone red.
- Milestones marked STOP end the turn: report and wait for the human.
- **Rulings bind only once transcribed** into `decision_log.md` or
  `CLAUDE.md` in the same session. Transcribe first, then act.
- Numbers enter documents **derived or measured in the same session** —
  never transliterated from a chat heuristic.
