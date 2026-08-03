# E1.0 — Co-active visitation: inventory before analysis

**Status: both deliverables are in hand. The subset check PASSES, and the
radius caveat resolves better than the DECISION comment feared — but not
completely, and the residue bounds every claim in this package.**

Work package E1 (`env_native_prompt.md`), authorized by the allocation
correction (framing ruling item 3, `docs/decision_log.md` 2026-08-02). **Not
a protocol milestone.** Zero compute: everything below is measured from
committed artifacts by `che/scripts/e1_inventory.py`.

Generated artifacts: `results/e1/inventory/inventory.md` (the per-file table,
115 rows) and `inventory.json`.

> **NO-PEEKING is enforced structurally, not by convention.** M6.2/M6.2b are
> Phase-6 confirmatory runs and `coupling_co_active` is an outcome channel of
> them, so comparing it across arms before unblinding is forbidden. The
> instrument raises `SystemExit` on any `phase6` path (`_assert_not_phase6`,
> tested). **No Phase-6 artifact was read.**

---

## 1. Headline

| question | answer |
|---|---|
| How many Phase 3–5 eval artifacts carry the counter? | **115 of 115** (58,880 episodes) |
| How many can co-activity actually be graded on? | **76** (38,912 episodes) — the rest predate `seeded_ignitions` |
| How many have **both couplings live**? | **64** (32,768 episodes) — Coupling B masks only at obs v3 |
| Does `co_active ≤ seeded_ignitions` hold? | **Yes. 0 violations in 38,912 episodes.** |
| Does the co-active radius match Coupling B's? | **On the outer bound, exactly. Inside it, no** — see §4. |

---

## 2. The three tiers, and why "115 files" overstates what is analysable

The E1 prompt's file count is right, but "carries the counter" is **not** the
same as "can be analysed for co-activity", and neither is the same as "both
couplings are live". Measured:

| tier | files | episodes | what it supports |
|---|---|---|---|
| carries `coupling_co_active` | **115** | 58,880 | presence only |
| + carries `seeded_ignitions` | **76** | 38,912 | **co-activity is gradeable** |
| + obs v3 (Coupling B actually masks) | **64** | 32,768 | **both couplings live** |

**The 39 excluded files are `m30` (9), `m30b` (27) and `m31b` (3).** They
predate the `seeded_ignitions` channel and their `coupling_co_active` is
identically zero — Phase-3 baselines from before Coupling A was calibrated.
They are inventory, not evidence.

**The 12 further-restricted files are `m35`.** They have Coupling A live
(κ_A on) but run **obs v2**, and `observation.py` gates the entire
Coupling-B masking path on `cfg.obs_version == 3` (v3 = v2 planes gated by
Coupling-B masking, plus the visibility plane — `docs/locks.yaml`). So in
those 12 files the hazard is created by collapse but **nothing attenuates the
agent's view of it**. Co-activity there is pure geometry.

The 64-file tier is `m44` (14), `m53b` (22), `m55` (16), `m53` (6),
`m51e` (4), `pretask` (2). `danger_agents` and `masked_danger_sum` are
present in **exactly** those 64 — the realized-perception channels arrived
with obs v3, which is the same boundary.

### Two inventory facts that would mislead a naive read

1. **`seed` in the eval JSON is the EVAL seed, and it is 0 in all 115 files.**
   The **training** seed is in the filename (`_s0`, `_s1`, …). Reading the
   JSON field alone would conclude the whole corpus is one seed. It is not;
   `inventory.md` carries the training seed in its own column.
2. **`m30b` names its evals `train_<sev>_s<N>_eval_<sev>.npz`, not
   `eval_*.npz`.** A filename glob finds 88 files and silently drops 27 — a
   quarter of the corpus. The instrument selects **by schema** instead. It
   also writes a different JSON schema (`train_severity` / `eval_severity` /
   `train_seed`, no `config`), normalized in the table.

### One caveat that carries into everything downstream

**All 115 artifacts are `ckpt_step = 500` at `n_episodes = 512`.** Phase 3–5
is entirely a T = 500 corpus, while the Phase-6 grid now runs at **T\* =
1000** (registered 2026-08-03). Any co-activity level reported by E1 is a
**T = 500 quantity**, and M6.2b showed that training length changes this
environment's statistics materially. Comparisons to Phase-6 numbers are not
available (blind protocol) and would not be like-for-like anyway.

---

## 3. Subset check — PASS, and it is a real check

`co_active ≤ seeded_ignitions` holds **by construction**: the co-active set is
the seeded set intersected with a dilated occupancy mask. Measured over the
76 files that carry both channels:

- **38,912 episodes, 0 violations.**
- **Largest observed `co_active − seeded` is exactly 0.0**, i.e. the bound is
  attained — there are episodes where every seeded ignition was within
  perception range of some alive agent. A strict inequality everywhere would
  have been mildly suspicious; saturation is what a genuine subset looks like.

**Independent consistency check, unplanned and stronger than the required
one.** `m35` is the κ_A ablation, and it splits cleanly:

| m35 arm | κ_A | seeded (mean/ep) | co-active (mean/ep) |
|---|---|---|---|
| `ka0`, all three severities (6 files) | off | **0.0000** | **0.0000** |
| `kaL`, all three severities (6 files) | on | > 0 | > 0 |

Coupling A off ⇒ no seeded ignitions ⇒ no co-activity, exactly as Def. 5
requires, at every severity, with no exceptions. The counter is measuring
what it claims to measure.

---

## 4. The radius finding — better than feared, and the residue is real

The DECISION comment at `che/env/env.py` reads: *Chebyshev radius
`obs_window // 2`, matching the crop; revisit when Coupling B fixes
attenuation range.* E1.0 owes an answer. Measured from the two code paths:

- The counter dilates occupancy by `obs_window // 2`, and `dilate` is
  **Chebyshev** (L∞) with window `2r + 1` (`che/env/structure.py`).
- The crop is `k × k` with `k = obs_window`, padded by `r = k // 2` and
  sliced at the agent position, so it spans exactly Chebyshev −r…+r
  (`che/env/observation.py`). `obs_window = 9` is enforced odd, so **r = 4**.

**On the outer bound the two agree exactly, and this is the important half.**
A cell outside the crop is not observed *at all* — perception is hard-bounded
by the crop, not merely attenuated near its edge. So the binary Chebyshev
test **is** the correct "could this agent perceive it" boundary, and the
DECISION comment's worry does not bite there.

**Inside the bound they differ, and this is the part to state plainly.**
Coupling B's optical depth is `D = κ_B · dist · mean_rho` with `dist`
**Euclidean**. Within the outermost Chebyshev shell, Euclidean distance runs
from **4.000** (axis) to **5.657** (corner), so at equal smoke the optical
depth varies by a factor of **1.414** across cells the counter treats
identically.

### What that means for every claim in this package

**`coupling_co_active` is an OPPORTUNITY measure, not a realized-perception
measure.** It counts collapse-seeded ignitions that are *geometrically
positioned to be perceived*, and is silent on whether smoke actually hid
them. Two consequences, both of which belong in the paper rather than in a
reviewer's report:

1. It is an **upper bound** on genuinely-co-active-and-perceived events.
2. The realized side is carried by different channels — `masked_danger_sum`
   and `danger_agents` — which exist in exactly the 64-file obs-v3 tier. The
   mechanism story needs both halves, and the artifacts support that only on
   those 64 files.

This is a **scope caveat, not a defect**: the counter is correct for what it
measures, and its radius is the right one. It simply measures co-location,
and the name "co-active" should be read that way.

---

## 5. What E1.1 inherits

- The gradeable set is **76 files**; the both-couplings-live set is **64**.
- Severity is available for every file, and `m30b` additionally separates
  **train** from **eval** severity (the cross-severity matrix) — which E1.2's
  endogeneity question can use directly.
- **The E1.1 prediction is already pre-registered in `env_native_prompt.md`**
  (committed `ce7ec3d`, before this work began): co-activity need not be
  monotone in severity, and Medium may be its peak. Recording that the
  prediction predates the measurement, because the mandatory subset check
  required loading the data and some per-severity numbers were therefore
  visible during E1.0. The prediction was fixed in writing first.
- **Every E1.1 number needs a floor grade or an UNDERPOWERED flag.** No
  threshold has been invented here, and none should be.

---

## 6. STOP

Per the work package: **deliverable is the inventory table plus the radius
finding, then STOP and report.** Both are delivered. The subset check passed,
so E1.1 is unblocked, but it is a separate milestone and is not started.

Nothing in `che/env/`, the protocol, `docs/locks.yaml` or any registered
constant was touched. This package reads.
