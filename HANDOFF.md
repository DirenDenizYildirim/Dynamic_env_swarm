# HANDOFF — session state for the next model (written 2026-08-02, evening)

You are picking up **mid-Phase-6, immediately after M6.2b**. A registered
**STOP has fired on the power guard** and **`k` is owed a human ruling**.
There is **no GPU box running** (destroyed after artifacts were pulled and
sha256-verified).

**Nothing is blocked on work. Everything downstream is blocked on one human
decision.** If you are here to make progress, the answer is
`env_native_prompt.md` — see *What to do next*.

---

## The one open decision

**`k` must be re-ruled by a human**, because M6.2b's power guard fired. It
comes bundled with a second question that must be answered at the same time:

**Which basis grades Γ's power?** The instrument computes power per arm as
`σ√(2/k)` — the **equal-variance** form. Γ = mean(JOINT) − mean(ISO), whose
true standard error is `√((σ_iso² + σ_joint²)/k)`. The project adopted
per-artifact floors *because* the arms differ in stability, then kept a formula
that assumes they do not.

| basis | power @ 0.03, k = 34 | k for 80 % | grid runs | ≈ $ at 686 s/run |
|---|---|---|---|---|
| per-arm JOINT (what the guard grades) | **62.8 %** | 50 | 260 | $49.83 |
| combined variance (correct for a difference) | 76.7 % | **37** | 234 | $44.85 |
| — k = 34 as registered, STOP standing | — | — | 228 | $43.70 |

**The STOP fires on either basis**, so the verdict is not in question. Only
the remedy is.

**Budget note, stated without spin:** the owner has ~$40 for the grid. **Every
option above exceeds it, including the registered k = 34 grid.** The
re-ruling did not create that gap — doubling the run length did, and that was
ordered by the plateau guard. Do not quietly shrink the design to fit; that is
a human call.

---

## What M6.2b measured

24 runs planned at T = 1000; **cut at 17** for a mains outage at the operator's
site. The box was remote and unaffected — this was an access decision, not lost
work. **Both confirmatory arms had completed 8/8**, so the verdict stands.
Full report: `che/bench/results/phase6/m62b/m62b_report.md`.

**Plateau — BOTH ARMS PASS. The re-run did its job.**

| arm | drift / 100 updates | its floor | ratio | at T = 500 |
|---|---|---|---|---|
| ISO | +0.0034 | 0.0339 | **0.10×** | 1.06× |
| JOINT | +0.0276 | 0.0483 | **0.57×** | 3.17× |

The asymmetric-convergence confound that motivated the re-run is **gone**.

**Power — STOP.** JOINT completion 62.8 % < 80 %. ISO 92.2 %. Survival
> 99.99 % on both, so the co-primary is not power-limited.

**Floors grew with T, unevenly, and the ordering inverted.**

| arm | completion floor T=500 | T=1000 | growth |
|---|---|---|---|
| ISO | 0.0165 | 0.0339 | 2.1× |
| JOINT | 0.0093 | **0.0483** | **5.2×** |

At T = 500 JOINT was the *tighter* arm; at T = 1000 it is the *looser*. **This
is an environment-native finding, not a protocol nuisance** — convergence and
run-to-run stability trade against each other, and the arm with the harder
curriculum (2 all-elements-co-active components vs ISO's 6 single-element ones)
pays more. It belongs in the paper regardless of how Γ lands.

Honest limit: at n = 8 these floors carry 95 % CIs of **[0.0224, 0.0690]**
(ISO) and **[0.0319, 0.0983]** (JOINT). The single-number powers are point
estimates on 7-dof variance estimates.

**The sweep p = 0.5 arm completed 1 of 8 reps and NO sweep floor is reported.**
It is secondary and non-verdict-bearing. If wanted later: 8 runs ≈ $1.50, and
it should be measured on whatever card runs the grid anyway.

**T\* is NOT registered.** `locks.yaml` keeps its slot at `value: null` with
`owed_by`. The plateau branch passed, but step (b) STOPped on power, so the
criterion's conditions are not jointly met. Writing 1000 in now would convert a
criterion into an assumption. A test asserts the slot stays empty on both
sides.

---

## What to do next — the ruling already answered this

Framing ruling item 3 (binding, `659ca82`) directs reclaimed effort to
**environment-native content**, on grounds of an allocation audit that found
two weeks of near-total protocol work protecting a ~3-point effect while
environment-native content sat untouched. **We are in that state again:**
protocol is blocked, those sections are still unwritten.

**`env_native_prompt.md` is written and ready** — work package **E1,
co-active visitation**, chosen by the owner. Zero new compute: 156 eval `.npz`
across 12 milestones already carry `coupling_co_active` per-episode, and it has
**never been analysed** despite being logged since day one on explicit
instruction (invariant #5).

⚠ **That prompt contains a live trap and states it up front:** M6.2/M6.2b eval
artifacts are Phase-6 confirmatory runs, so **comparing co-active visitation
between ISO and JOINT is a cross-arm outcome comparison, forbidden until
unblinding**. E1 uses Phase 3–5 artifacts only (115 files).

---

## What this session did

Six commits, tree clean, `ruff` green.

| hash | |
|---|---|
| `659ca82` | **Job zero** — framing ruling transcribed, cross-referenced both directions with the pilot/fork entry, honesty note corrected to the measured **2 of 3** |
| `da66ef9` | **Analysis-constant registry** ruled + enforced; **step 0 discharged** |
| `b7e09d8` | M6.2 artifacts (81 files) + report + design v2 §6 measured cost |
| `f428e40` | Prompts tracked, deletions recorded, HANDOFF committed |
| `1309ef3` `ff493d5` | **Toolchain pinned** — jax 0.11.0, Python 3.12+, lock made true |
| `402d422` | M6.2b verdict + verified artifacts |

**Two defects of the same class were closed:**

1. **Analysis constants lived only in prose and script literals.**
   `docs/locks.yaml` now has an `analysis:` section (`K_CONFIRMATORY`,
   `K_SECONDARY`, `SIDAK_M`, `POWER_STOP`, `PLATEAU_PASS`, `PLATEAU_REVIEW`)
   and `test_locks.py` **imports the module and asserts equality**. Env
   constants are enforced by config reachability; analysis thresholds have no
   config, so import is the substitute — and the section says so, rather than
   pretending the config rule was weakened.
2. **`uv.lock` had never bound a single run.** It pinned jax 0.10.2 from
   2026-07-18 while M6.0, M6.2 and the local venv all ran 0.11.0. The
   **interpreter** was the real determinant (0.11.0 needs Python ≥ 3.12;
   `requires-python` said ≥ 3.11) and **no artifact recorded it**. Now pinned,
   and `provenance.txt` records python/jax/jaxlib/devices.

That is the R_comm pattern for the third and fourth time: **a declared value
with no mechanism.** Both are now enforced by test.

---

## Instrument state

`che/scripts/m62_report.py` is clean and frozen-able:

- **Rule-2 mean suppression** — stdout gets sd, range and drift only;
  `floors.json` keeps raw values for unblinding. Mechanical, not behavioral.
- **Window bug fixed and hardened.** It sliced the NaN-filtered completion
  series by `--tail`; completion is NaN every other update, so the
  "final-100-update" window spanned 200 and every drift read ~2× high. Both
  window and regression now run on the logged `update` number.
- **`POWER_STOP` 0.80**, `PLATEAU_REVIEW` reporting-only (never a verdict).
- `run_m62b_t1000.sh` wraps `run_m62_floors.sh` **unmodified** — fresh-output-dir
  guard, owed-tests pre-flight, archive assertion, toolchain provenance append.

---

## Hardware / cost facts

- **RTX PRO 6000 Blackwell required.** A 31.8 GiB 5090 cannot run the gate
  config (~61.6 GiB at compile). **Never** set `--xla_gpu_autotune_level=0`.
- **Boxes differ ~15 %**: M6.2's card implied ~60,900 env-steps/s; M6.2b's
  measured ~52,000 → **686 s/run at T = 1000**. **Floors are per-hardware, so
  the grid must run on the M6.2b card or re-measure floors on its own.**
- **Gate a new box on network before shipping**: `curl` a PyPI file; 1.4 MB/s
  is too slow (a ~3–4 GB CUDA sync), 46 MB/s is fine. Ship **454 KB**
  (`che docs pyproject.toml uv.lock`) — not the 49 MB that includes `m06/`.
  Set `UV_HTTP_TIMEOUT=600`; the 30 s default fails on the 762 MB cudnn wheel.
- Spend to date this phase: M6.2 ~$2, M6.2b ~$3.30.

---

## Open threads

- **`m06/` is 47 MB** of pre-M6.0 spike leftovers at the repo root — undecided
  whether it belongs in the tree.
- **`test_prop3`, `test_calibration`, `test_percolation` have never run under
  local CPU jax** since 2026-08-02. They passed on GPU (CUDA jax) as the
  step-(b) pre-flight — good evidence, different execution path.
- **24 M5.5 renders un-inspected** — owner-assigned, precedes the grid.
- Design v2 §9's M6.1 engineering (per-component count logging, protocol config
  tests) is still owed before the grid.

## Working agreements

- **Rulings bind only once transcribed** into `decision_log.md` or `CLAUDE.md`
  **in the same session**.
- **Numbers enter documents derived or measured in the same session.**
- **Bars come with floors** — per-metric, per-hardware **and per-artifact**.
- **Design-stage power statements are 80 %-power MDEs** at the family-corrected
  α, never bare 2σ√(2/k).
- Run the CPU suite **chunked and thread-capped**; an unbounded run once
  crashed the machine.
- **Milestones marked STOP end the turn: report and wait for the human.**
