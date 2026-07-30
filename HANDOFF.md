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
