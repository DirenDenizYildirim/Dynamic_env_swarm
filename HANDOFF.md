# HANDOFF — session state for the next model (written 2026-08-02)

You are picking up **mid-Phase-6**, immediately after M6.2. A registered
STOP has fired and a framing ruling is waiting to be transcribed. There is
**no GPU box running** (checked this session: connection refused).

---

## JOB ZERO — transcribe the framing + allocation ruling

`phase6_framing_allocation_ruling.txt` sits **untracked at the repo root**.
It is a ruling relayed and owner-approved 2026-08-02, and per the standing
meta-rule (`CLAUDE.md`, "Rulings bind only once transcribed") **none of it
binds until it is in `docs/decision_log.md`**. Its own closing line says:
*"Confirm transcription with the commit hash, then start (0), then (b)."*

Read the file in full. What it registers, in one line each:

1. **FRAMING: ENVIRONMENT-FIRST.** The paper's contribution is the
   calibrated, theory-certified compound-hostility environment and its
   measurement discipline. Γ is the demonstration that environment uniquely
   enables — **reported whichever way it lands**. The success condition is
   *not* Γ's sign. This is registered **pre-unblind on purpose**, so a null
   Γ cannot be read later as post-hoc reframing.
2. **STATISTICS FREEZE.** The protocol is complete. `T*` is the only open
   instrument question and is resolved **by registered criterion, not by
   discretion**: `T* = 1000` iff *both* confirmatory arms pass the plateau
   guard at the T=1000 re-run; anything else STOPs to a human. No further
   protocol elaboration unless a registered guard fires.
3. **NO-PEEKING.** M6.2 cross-arm outcome comparisons are calibration
   by-catch. **No document may quote a cross-arm M6.2 mean** — one that
   does gets flagged. Per-arm floor computation legitimately uses arm
   labels; comparing arm *outcomes* waits for unblinding.
4. **ALLOCATION CORRECTION.** Reclaimed effort goes to environment-native
   content (behavioral findings family, co-active-visitation mechanism,
   figures) — those are paper **sections**, not garnish.
5. **INTRODUCTION MATERIAL** (owner-approved): the symbiosis argument —
   bitwise nesting, unconditional PRNG consumption and traced-θ are
   scientifically meaningful *because* Γ requires ISO and JOINT to be
   literally the same kernel with parameters zeroed.

**Registrar duties when you transcribe:**

- Cross-reference the entry **both directions** with the existing
  2026-08-02 pilot/fork entry. Both rulings stand and compose: the
  success-condition framing is registered pre-unblind; the
  **one-paper/two-paper fork stays a POST-unblind decision** at the
  results-accepted gate, unchanged.
- ⚠ **One numerical claim in the ruling needs hardening before it enters
  `docs/`.** Rule 2's honesty note says *"ALL THREE arms failed the plateau
  guard"*. That reflects the **pre-fix** instrument. The corrected
  instrument (see below) measures **2 of 3**: ISO and JOINT climbing,
  `sweep_p500` plateaued at 0.36× its own floor. The ruling's operative
  content is unaffected (the STOP fires either way, and the T=1000 re-run
  is ordered either way), but per the standing sub-rule *"numerical claims
  enter documents derived"*, transcribe the measured 2-of-3 and note the
  correction — do not transliterate "all three".

---

## Read before acting

`CLAUDE.md` (invariants + the four standing rules, three of them added
2026-07-30/08-02) → `phase6_framing_allocation_ruling.txt` →
`docs/decision_log.md` from "PHASE-6 REMEDY RULINGS" onward →
`phase6_design_v2.md` (**this is the registration**; v1 is the reviewed
draft only) → `che/bench/results/phase6/m60/m60_report.md`.

---

## What M6.2 measured

24 runs (3 arms × 8 identical reps at seed 0, T=500 updates), each trained
on its protocol config and evaluated at θ\* via `--allow-hash` (cross-config
eval declared, not smuggled). All 24 completed; the shakedown found no
process surprise. Artifacts pulled and verified: `m62_artifacts.tar.zst`
sha256 `eb0ba874fb7eb8d85a982ac77da1cba283edb51d886008c3c6bc8a960726cbfb`,
**79/79 files OK**.

**Per-arm floors — sd and range only (rule 2: no outcome means).**

| arm | completion sd | range | survival sd | range |
|---|---|---|---|---|
| ISO | 0.0165 | 0.0510 | 0.0134 | 0.0347 |
| JOINT | 0.0093 | 0.0337 | 0.0156 | 0.0410 |
| sweep p=0.5 | 0.0157 | 0.0453 | 0.0110 | 0.0345 |

(n = 8 each; `episode_return` and `deaths_fire` floors are also in
`floors.json`.) **The per-artifact rule earned its keep**: completion sd
differs **1.8×** between the two arms Γ contrasts. One shared floor would
have made JOINT's bars ~75 % too loose or ISO's ~45 % too tight.

**Power recompute at k = 34, Šidák m = 2 — the < 75 % STOP does NOT fire.**
Completion MDE80: ISO 0.0123, JOINT 0.0069; power@0.03 ≈ 100 % on all four
confirmatory metrics. Completion floors came in **2.4–4.3× smaller** than
the 0.0399 design prior. Surplus recorded; k = 34 stands. **These floors
are T=500 artifacts and die with the re-run** — they do not grade anything
at T*.

**PLATEAU GUARD FIRED → STOP.** Drift over the final 100 updates against
each arm's own floor (drift ratios are explicitly reportable at a STOP):

| arm | drift/100 updates | its floor | ratio | verdict |
|---|---|---|---|---|
| ISO | +0.0174 | 0.0165 | 1.05× | marginal, climbing |
| **JOINT** | **+0.0295** | **0.0093** | **3.2×** | clearly climbing |
| sweep p=0.5 | +0.0056 | 0.0157 | 0.36× | plateaued |

**The sharp part is the asymmetry, not the magnitude.** JOINT is still
improving ~1.7× faster than ISO at end of training (0.000295 vs 0.000174
per update). Γ = J(joint) − J(iso) at θ\*, so an *asymmetric* convergence
rate between exactly the two contrasted arms is a direct confound on the
headline quantity — worse than symmetric non-convergence. Plausible cause:
JOINT trains on 2 all-elements-co-active components (harder) while ISO
trains on 6 single-element ones (easier). This is why the ruling orders a
T=1000 re-run rather than a discretionary extension.

**A bug in our own instrument was found and fixed during this analysis.**
`m62_report.py` sliced the **NaN-filtered** completion series by `--tail`.
Completion is NaN on updates with no finished episode — with horizon 256
and rollout_len 128 that is every other update — so the "final-100-update"
window actually covered **200 updates** and inflated every drift ~2×. The
pre-fix run flagged all three arms; corrected, it flags two. The fix
(window indexed on actual updates, slope rescaled per-update) is **in the
worktree, uncommitted**. See step 0.

**Measured cost, discharging design v2 §6's estimate:** train median 269 s,
eval median 19 s (n = 24 each) → **288 s/run** at T=500. v2 assumed 257 s
train and left eval unmeasured.

---

## The sequence you are to follow (from the ruling, order unchanged)

**0. Clean the instrument before any run.** `che/scripts/m62_report.py`
carries uncommitted changes on top of `7710bba`. Fold in the rule-2 mean
suppression — *the printed report emits per-arm sd, range and drift only,
no per-arm outcome means* — and commit, **or** revert. The blind protocol
freezes the pipeline by commit hash; a dirty script cannot be a frozen
instrument. Note the reading: rule 2's operationalization targets what the
report **prints**; `floors.json` should keep the raw values (they are
needed at unblinding) — but make the suppression mechanical, not
behavioral, and say in the commit message which you did.

**a. [OWNER, not you] render inspection of the 24 M5.5 episodes** — the
third flag; it precedes the grid. Do not do this yourself; it is assigned.

**b. M6.2 re-run at T = 1000.** Fresh per-arm floors (length-specific
artifacts — *never* carry the T=500 ones forward), plateau verdict per the
registered criterion, power recompute **on the measured T=1000 floors**.
Do not presume the outcome: floors are per-artifact facts and may grow
with T.
→ **ELSE:** if power@0.03 (Šidák m = 2, k = 34) falls below **80 %** on
either confirmatory arm's floor → **STOP, report; k is re-ruled by human.**
(Note the threshold moved: M6.2's registered STOP was 75 %; this ruling
sets 80 % for step b. `POWER_STOP` in `m62_report.py` is currently 0.75 —
update it as part of step 0 and say so in the commit.)

**c. If both confirmatory arms certify** (plateau guard passes; the sweep
is secondary and **does not gate**) → grid at **T\* = 1000** per the item-1
criterion, no discretion exercised — k = 34 confirmatory / k = 20 secondary
as amended — then freeze → blind → unblind per protocol.
→ **ELSE:** if either confirmatory arm is still climbing at T = 1000 →
**STOP, report drift ratios; T\* escalation is a human ruling — do not
self-extend run length.**

**d. At any STOP:** report drift ratios and floors; **do not report
cross-arm means.**

---

## Cost (estimate, extrapolated from measured T=500 timings)

Train scales linearly in updates, eval is flat: T=1000 → 2×269 + 19 =
**~557 s/run**.

| item | runs | GPU-h | ≈ $ at ~$1/h |
|---|---|---|---|
| M6.2 re-run at T=1000 | 24 | 3.7 | **$4** |
| grid proper (ISO 34 + JOINT 34 + sweep 100 + ident 60) | 228 | 35.3 | **$35** |
| combined | 252 | 39.0 | **$39** |

Against v2's registered ~$27-with-margin. **Money is still not the binding
constraint** — wall-clock and statistical power are, as they have been
since Phase 0.

---

## State of the tree

Tip is `7710bba` ("M6.2 instrument: the floor milestone…").

- **Dirty:** `che/scripts/m62_report.py` — the window-bug fix (18 +/6 −).
  Step 0 resolves it.
- **Untracked:** `che/bench/results/phase6/m62/` (289 MB total; the 24
  `ckpt_*.tar.zst` are **gitignored** by `.gitignore:268`, leaving 81 files
  / **8.8 MB** that should be committed — metrics jsonl, eval json+npz,
  `floors.json`, `plateau.json`, `power.json`, `verdict.txt`,
  `provenance.txt`, `timings.txt`, `SHA256_CKPT.txt`).
- **Untracked, deliberately left alone (ask before reconciling):**
  `phase4_prompt.md`, `phase5_prompt.md`; `phase2_results.zip` and
  `phase3_prompt.md` are deleted-but-tracked.
- **Owed and not yet written:** `che/bench/results/phase6/m62/m62_report.md`
  (the milestone report). Write it **rule-2 compliant** — sd/range/drift
  and power, no cross-arm outcome means.
- **Owed:** design v2 §6 updated with the measured 288 s/run.

⚠ **Transcript hygiene.** Earlier in the previous session, before the
no-peeking rule existed, cross-arm M6.2 outcome means were quoted in chat.
They are in the transcript. **Do not propagate them into any document.**

---

## Hardware

**No box is running.** The M6.2 instance (`ssh -p 53797
root@178.193.102.66`) refused connection when checked this session — assume
it is gone and provision a new one for step (b).

- **A 31.8 GiB 5090 cannot run `configs/gate_pop12.yaml`** — autotuning
  needs ~61.6 GiB *at compile*; autotuning off fits but is 16.4× slower.
  Both fail. **Never set `--xla_gpu_autotune_level=0` on this workload.**
- Phases 5–6 ran on an **RTX PRO 6000 Blackwell (96 GB, ~$1/h)**, gate
  config 62,084 steps/s (Phase 5) / 60,037 re-measured at M6.0.
- Toolchain matters: the same config measured 24.69 GiB on one rental and
  27.53 on the next, from a jax/jaxlib change alone.
- **Floors are per-hardware facts.** If step (b) runs on a different card
  than M6.2 did, that is *fine* — the T=1000 floors are measured fresh on
  that card and grade the grid that runs on it — but the grid must then run
  on the same card. Record the card in `provenance.txt` (the script does).

---

## After the grid — the allocation correction (ruling item 3)

Reclaimed protocol effort goes to **environment-native content**, which is
paper sections, not garnish:

- **Behavioral findings family** — endogenous exposure; the ash-encoding
  arc (`docs/decision_log.md:54`; `phase4_report.md:521` on ash foraging);
  perception self-regulation; information-buying / branch-loitering
  (`decision_log.md:1134`, `phase5_report.md:1045`).
- **Co-active-visitation mechanism material** (invariant #5's counter has
  been logged since day one — use it).
- **Figure production.**
- **Introduction skeleton** from ruling item 4 (the symbiosis argument).

Grounds recorded in the ruling: an allocation audit found two weeks of
near-total protocol work protecting a ~3-point effect while
environment-native content sat untouched. The −8.8 pt Coupling-B survival
result needed no power analysis; the machinery exists because *this*
effect is small, and it is now sufficient.

---

## Phase 0–5 facts you will need

- Severities **β = 0.43 / 0.49 / 0.70** (β̂_c = 0.500); **κ_A = 0.06**,
  **κ_B = 1.0**, **d_p = 0.5**, obs v3, **δ = 1.0**, **R_comm = 16**.
- **θ\* = held-out β 0.49** (`theta_star_holdout.yaml`) — training uses the
  extremes {0.43, 0.70}. **Never train on `joint_medium.yaml`** in Phase 6;
  it would destroy the held-out property Γ depends on (flagged in
  `locks.yaml`).
- **Phase 5 is a certified negative:** communication is worth nothing
  measurable to this swarm; the load-bearing evidence is the unused
  connectivity bit (demand-side, not an encoder limitation).
- **Phase 4:** Coupling B is not inert — −8.8 pt survival at High,
  completion intact.
- **M6.0:** θ is per-env traced in `EnvState.theta_live`, sampled at
  reset/autoreset. 2a bitwise: **1520 field digests, 0 changed**. DCE tax
  ≤ 0.62 %. **θ binds at RESET, not at step** (both directions pinned in
  `test_traced_theta.py`).
- **Locks are enforced by test:** `docs/locks.yaml` + `che/tests/
  test_locks.py`. Every lock lands in `locks.yaml` in the same commit its
  ruling is transcribed.

---

## Working agreements

- **Rulings bind only once transcribed** into `decision_log.md` or
  `CLAUDE.md` **in the same session**. Transcribe first, then act.
- **Numbers enter documents derived or measured in the same session** —
  never transliterated from a chat heuristic.
- **Bars come with floors**, and floors are per-metric, per-hardware **and
  per-artifact**.
- **Design-stage power statements are 80 %-power MDEs** at the
  family-corrected α, never bare 2σ√(2/k).
- GPU jobs: no local CUDA. Hand the user scripts in `che/scripts/`, or
  drive a box over SSH if given access. Launch detached with `nohup`, poll
  in separate calls, `scp` back, **verify sha256 before releasing any
  instance**. Watch out: `pkill -f <pattern>` matches your own SSH command
  line.
- Run the CPU suite **chunked and thread-capped** — an unbounded
  `pytest che/tests` once crashed the machine:
  `OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 nice -n 15 uv run pytest <subset>`.
- After each milestone: `uv run ruff check che/`, the chunked suite, commit
  naming the milestone. Never start the next milestone red.
- **Milestones marked STOP end the turn: report and wait for the human.**

## Open threads (small)

- **24 M5.5 renders un-inspected** (`che/bench/results/phase5/m55/renders/`)
  — this is sequence step (a), owner-assigned.
- **M5.1k lever sweep truncated at 3/6 rows.** The two informative rows
  already answered it: no free throughput win; more concurrent envs are
  marginally worse.
- **Ablation certification table** — cut from the confirmatory plan
  (final-five ruling 5) with the registration honesty that requires.
