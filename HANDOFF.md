# HANDOFF — session state for the next model (written 2026-08-13,
venue amended 2026-08-24 — see §2a)

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

### 1. Everything before the rental is DONE (2026-08-13)

The owner **delegated the pre-rental decisions to the builder**, stating bias
avoidance as the reason. Recorded in `decision_log.md` with its limits —
delegation *relocates* bias rather than removing it; what protects these
rulings is that they were made **with no outcome visible**, and each carries
**the argument against it** as well as for it.

| item | state |
|---|---|
| the three grid-layout decisions | **RATIFIED**, plus two constraints the proposal did not carry: the confirmatory analysis is **UNPAIRED** (shared seed integers create no pairs), and **Γ's CI is conditional on the common eval draw** |
| `phase6_framing_branches.md` | **RATIFIED**, now tracked. §6 items 1–4 all ruled |
| design v2 §5 / §7 | **written** — the upper-bound framing and the seed-dispersion test basis, owed since the M6.2b close-out |
| release hygiene | **done** — README written, `m06/` archived + untracked, `*_console.log` generalized |
| the three no-scoop checks | **run. No scoop.** One spine item narrowed; one check only partially discharged (below) |

**Two rulings worth knowing before you touch the analysis:**

- **Branch B now has a registered falsifier:** `|z_c| + z_α < |z_s|` in
  standardized units. It uses the frozen Šidák `z_α = 2.2365` and **invents no
  constant**. Derived check: a survival effect of 0.010 admits |completion| <
  0.0050; 0.020 admits < 0.0212. A barely-rejecting survival result therefore
  **cannot** support the asymmetry claim, which is correct.
- **Branch D deliberately has NO magnitude threshold, and none may be
  introduced post-unblind.** Γ(t) measures directly what a threshold would
  only proxy for.

### 1a. The grid can run in four chunks of 60 — ruled 2026-08-14

`MAX_RUNS=60`, four invocations. The chunks land exactly on seed boundaries
(seeds 1–6, 7–12, 13–18, then 19–20 plus the confirmatory tail 21–40), and
**that alignment is the safety argument**: seed-major order puts both arms of
every seed on the **same card**, so a card effect is common-mode and **cancels
in Γ**. Chunks may therefore run on different rented cards. When `MAX_RUNS` is
hit mid-seed the loop **finishes the seed** before stopping.

- **Cost is power, not validity.** `sd(Γ)` may inflate **1.93×** (completion) /
  **3.14×** (survival) before power falls to 80 %. Realized power is
  **reported, not re-engineered**.
- **No extra re-flooring.** The grid's own seed dispersion already contains the
  card variance, so it is a superset of any single card's floor and the
  beat-reproducibility hurdle is **subsumed**. One re-floor, first card.
- **Money ≈ unchanged:** same GPU-hours (~36.4 h ≈ $45.0), plus ~$1.5 for four
  setups instead of one.
- **Obligation:** `cards.txt` records the block structure and **the paper
  reports it** whenever more than one card ran the grid.

A planned chunk pause exits **green** and prints `CHUNK COMPLETE`; only real
failures exit red.

### 2. The rental — one trip, or four

`G1.2 re-floor (~$4.08) → ladder → G1.3 grid (~$40.9) → post-unblind Γ(t)
eval (~$3.60)`. Registrar's projected trip total **~$48.6** against a **~$65**
GPU reserve. The $45.73 grid authorization stands as-registered; the Γ(t)
block is a **reserve draw**, not an authorization amendment.

Read `gpu_launch_prompt.md` before renting. Its G1.0/G1.1 sections are
discharged history; **its G1.3 section still carries no command block** — use
`run_p6_grid.sh`.

### 2a. VENUE IS RULED — TMLR primary, DMLR fallback (2026-08-24)

**The primary venue is TMLR; DMLR is the registered fallback; both are
rolling and they are attempted SEQUENTIALLY** — TMLR's originality policy
forbids parallel submission at another archival peer-reviewed venue. RA-L /
IROS remains demoted to a branch-A-conditional stretch. Ruled pre-grid and
pre-unblind, which is what makes it provably not outcome-selected. Full entry:
`docs/decision_log.md`, *VENUE RULING II*; the assessment behind it is
`docs/venue_review_2026-08-24.md` (an assessment — it rules nothing).

It **supersedes** the 2026-08-16 *VENUE RULING* on the primary/fallback pair
only: **NeurIPS D&B is no longer registered anywhere in the ladder**, and its
CfP-reading task is **struck**. The 2026-08-16 grounds for demoting RA-L/IROS
stand untouched, as do `phase6_framing_branches.md` §7's supersession and
ruling 6c. It **does not** edit the branch table, change any constant, or
authorize spend.

**Two positioning rulings move, both by verification rather than by waiver:**

- **6b (anonymity, no repo links) STANDS and its conflict is CLOSED under the
  primary** — TMLR is double-blind, requires anonymized submissions and
  anonymized supplementary code (≤100 MB), and forbids linkage to a
  non-anonymous preprint. **The conflict RETURNS if the DMLR fallback is
  exercised** (single-blind, requires availability/maintenance docs) and is
  re-ruled then, not pre-emptively.
- **6a's page budget is DISCHARGED** — TMLR states no strict page limit, so
  the appendix-manifest strategy is unconditional under the primary.

**One venue mechanic is UNVERIFIED and it is the only one left: TMLR publishes
NO total time to decision** (stage deadlines only). A "~2–3 months" figure was
asserted in chat, is **retracted**, and enters no document. **No runway
arithmetic involving TMLR may be written until that check is discharged.**
The Journal-to-Conference track is **not** a ground for the ruling: it needs a
J2C/Featured/Outstanding certification, is a poster, and is explicitly not
published in the conference proceedings.

**Four proposals are OWED RULING and may be adopted only pre-unblind**
(review §7; ranked, not bundled — $12.91 total against a ~$16.4 free reserve):
**(0) $0** — register in writing that ISO spends 1/3 of its training budget on
the **certified-inert** δ element, a bias that **inflates Γ**;
**(1) $3.41** — an `ISO-4` control arm; **(2) $2.68** — a T = 2000 subsample on
the confirmatory arms; **(3) $6.82** — an UNDERPOWERED-flagged High point.
Proposal 0's finding is the substantive one and is transcribed in full in the
log entry.

### 3. Free work if there is no box

The pre-rental queue is empty. What remains is **owed before submission, not
before the rental**:

- **The IEEE Xplore query** — the one no-scoop check that is only *partially*
  discharged. Xplore needs authenticated access and was **not queried**; what
  ran was a general-web sweep of the RA-L/IROS swarm literature, which found
  only single-stressor, task-coupled work. **An owner task.**
- **Read the JaxWildfire PDF** (arXiv:2512.06102) and arXiv:2604.26150
  directly. The positioning ruling leans on two rows — single-agent, and a
  reward that is a penalty proportional to burning cells — obtained from an
  automated summary, which is strong enough to rule on positioning and **not**
  strong enough to write related work from.
- **Phase prompts still sit at the repo root**, and a clone is still 47 MB
  heavier than it looks: untracking `m06/` does not remove its blobs from
  history. A rewrite is destructive and is an owner decision.

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
