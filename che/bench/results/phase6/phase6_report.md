# Phase 6 report — the compositional test (closing index)

**Status: CLOSED 2026-09-27.** Unblinded once (2026-09-26) on the frozen
tree `41b11cd`: **branch B**, with the registered inert-share qualifier: the
survival effect **does not survive** the correction and may not be called a
composition effect. All post-unblind stages have run. **No further GPU spend**
(owner, 2026-09-26: the ISO-4 k = 72 extension was considered and declined).
What remains is writing (`paper/`).

**This file is an index, not a re-analysis.** Each milestone has its own
report or decision-log entry, and each number below is quoted from the
committed artifact named beside it. Nothing here is recomputed. Where this
file and a source disagree, the source wins; where a source and
`docs/decision_log.md` disagree, the log wins.

---

## 1. The result

θ\* = all-on at β = 0.49 (held out of every training mixture), matched budget
T\* = 1000, eval seed 0 × 512 episodes. Family {completion, survival},
Šidák m = 2, z_α = 2.2365, unpaired, graded on the contrast's own seed SE.

| contrast | completion | survival | source |
|---|---|---|---|
| **Γ = JOINT − ISO**, k = 72/72 (primary) | −0.0173, z −1.62, null | **+0.0096, z +4.43, REJECT** | `unblind/report.md` |
| Γ, registered-ladder prefix k = 60 | −0.0217, z −1.80, null | +0.0104, z +4.67, REJECT | `unblind/report.md` |
| falsifier \|z_c\| + z_α < \|z_s\| | 3.855 < 4.433 → **passes** (branch B, not C) | | `unblind/report.md` |
| **Γ₄ = JOINT − ISO-4**, k = 72/20 | −0.0126, null (second exclusion, X₄ = 0.0488) | **−0.0003, z −0.09, null** → DOES NOT SURVIVE | `post_unblind_analysis/post_gamma4_t2000.md` |
| B̂ = ISO-4 − ISO | −0.0046, null | +0.0098, z +3.39 | same |
| Γ₄′ = JOINT − sweep_c50_p000 (same card) | −0.0247, null | +0.0013, z +0.41, null | `secondary/secondary.md` (S5) |
| Γ(t), t = 500…1000, rule (iv) | `+ − + + − − − − − − −` UNSTABLE | `+ − − + + + + + + + +` UNSTABLE | `post_unblind_analysis/post_evalfloor_gamma_t_high.md` |
| Γ_H at β = 0.70 (out of family) | −0.0079, null → exclusion X = 0.0340 | +0.0038, null → exclusion X = 0.0254 | same |
| Γ(2000), 4 seeds, DESCRIPTIVE | +0.0003 | +0.0159, 95 % [−0.0002, +0.0319] | `post_gamma4_t2000.md` |
| fire deaths / episode, JOINT − ISO (secondary) | | −0.1177, z −4.59 | `unblind/report.md` |

**Budget-robustness suffix (registered): "sign unstable over the final
half"** on both co-primaries. The survival gap opens late (Šidák CI excludes
0 at t = 900, 950, 1000 only); completion is negative from t = 700 and its CI
excludes 0 at t = 750 only (−0.0147), which is descriptive, since no
registered test exists at t ≠ T\*.

**Eval reproducibility is exact.** 4 reps × 2 checkpoints bit-identical on
unit 3 and to the grid's unit-1 evals; 280 of 288 paired cross-card
(checkpoint, metric) evals identical, max |Δ| 2.44e−4.

**Secondary (non-verdict-bearing, 95 %, not family-corrected):** the
no-element training share costs survival (γ_n −0.0237 [−0.0419, −0.0057]);
γ_p +0.0326 [+0.0137, +0.0502] does not extrapolate to Γ₄; completion
resolves nothing; both knees UNDERPOWERED; **mediation VOID**, because the
invariant-#5 counter measures only Coupling-A-seeded ignitions, so it is
co-active only in all-on configurations. Source: `secondary/secondary.md`;
decision log *SECONDARY RESULT*.

The paper-facing reading of all of the above is `paper/branch_B.md`.

## 2. Milestones

| step | date | outcome | source |
|---|---|---|---|
| M6.0 traced-θ spike | 2026-08-01/02 | all four acceptances met; 1520 field digests bitwise | `m60/m60_report.md` |
| M6.1 protocol configs | 2026-08-02 | ten generated configs; β-trap becomes a test | `64a7397` |
| M6.2 floors, T = 500 | 2026-08-02 | plateau guard STOP | `m62/m62_report.md` |
| M6.2b floors, T = 1000 | 2026-08-02/03 | plateau pass; power STOP → close-out | `m62b/m62b_report.md`; log *M6.2b CLOSE-OUT* |
| G1.2 launch batch (PRO 6000) | 2026-08-10 | ladder branch A; STOP on run length | `g1/g1_2_report.md` |
| T\* ruling | 2026-08-11 | fixed-budget estimand, Γ(t) window | log *T\* RULING* |
| card-2 partial re-floor | 2026-08-14 | unrecorded rental; **grades nothing**; owner entry owed | `g1_floors_card2/README.md` |
| G1.2 re-floor on the grid card | 2026-09-08/09 | ladder branch B, K_CONF = 46 | log, 2026-09-09 entry |
| §7 proposals ruling | 2026-09-18 | ISO-4, T = 2000, High readout adopted | log *§7 PROPOSALS RULING* |
| G1.3 grid, 252 runs | 2026-09-09 → 09-22 | chunks 1–2 PRO 6000, 3–5 RTX 5090 | `6a026f9`; log *CARD RULING* |
| single-card conversion + 5090 re-floor | 2026-09-22/23 | ladder branch C, cap 60 → 72; `g1_conf_5090` k = 72 | log *SINGLE-CARD*, *LADDER BRANCH C*; `c21cc62` |
| secondary re-card, seeds 1–12 | 2026-09-24/26 | 96 runs, unit 1 | `e88e5fd` |
| ISO-4 (k = 20), T = 2000 (4 × 2) | 2026-09-26 | unit 2 | `968a781`, `83ebf95` |
| pre-unblind rulings (i)–(viii) | 2026-09-26 | A_c registered; k = 72 primary | log *PRE-UNBLIND RULINGS* |
| **UNBLIND** | 2026-09-26 | branch B + inert-share qualifier | `60942fc`; log *UNBLIND RESULT* |
| secondary analysis | 2026-09-26 | S1–S6 ratified before the sweep was read | `a153cae`; log *SECONDARY RESULT* |
| post-unblind evals (unit 3) | 2026-09-26/27 | 1772/1772 evals; suffix UNSTABLE; High null | `c36cf51`, `e76d5a7`; log *POST-UNBLIND STAGE RESULT* |

## 3. Artifacts: archives, hashes, and where they live

Every `ckpt_*.tar.zst` is gitignored; its `sha256` is committed beside it in
`SHA256_CKPT.txt`. **Re-verified locally 2026-09-27** by basename against the
committed hash file (the confirmatory file still carries `g1_grid/` paths for
seeds 13–46, so `sha256sum -c` would report false failures elsewhere).

| directory | archives | verified | note |
|---|---|---|---|
| `g1_conf_5090` | 144 | 144 | **the confirmatory artifact** |
| `g1_grid` | 252 | 252 | conf seeds 1–12 superseded; secondary 13–20 live |
| `g1_sec_s1_12_5090` | 96 | 96 | secondary re-card |
| `g1_iso4_5090` | 20 | 20 | |
| `g1_t2000_5090` | 8 | 8 | |
| `g1_floors_5090` | 24 | 24 | the `--floors` input to the unblind |
| `g1_floors_2026-09-08` | 24 | 24 | set K_CONF = 46 |
| `g1_floors` | 24 | 24 | against its 2026-09-09 rebuilt hash file |
| `m62`, `m62b` | 24, 16 | 24, 16 | |
| `m60` | 3 | 3 | incl. `m06_spike_ckpt.tar.zst` (hash in `m06_ARCHIVE.md`) |
| `g1_floors_card2` | 12 | **1** | **only rep1 was ever hashed**; 11 have no recorded hash; rep2 is truncated. Grades nothing. |
| `post_*`, `unblind/`, `secondary/` | 0 | — | eval JSON/NPZ and reports only, committed in git |

**615 of 615 recorded hashes match; 0 mismatches.**

The card for each directory is in `by_card/README.md` (three RTX 5090
units; `g1_grid` mixes PRO 6000 seeds 1–12 with 5090 seeds 13–46, one card
per seed).

**Single copy.** Every archive above exists on the owner's laptop only. The
off-instance rule is met (the GPU boxes are gone), but no second copy is
recorded anywhere in the tree. With GPU spend closed, these checkpoints
cannot be regenerated, so a second copy is the one remaining protection.

## 4. What is graded, and what is only recorded (instruments law)

- **Graded, confirmatory:** Γ on {completion, survival} at θ\*, k = 72.
- **Graded, registered reading rules, out of family:** Γ₄ / B̂ (qualifier),
  Γ(t) sign rule (suffix), Γ_H (exclusions only).
- **Descriptive only:** T = 2000; the cross-card check; the single-card Γ(t)
  curve; every secondary interval.
- **Recorded, grades nothing:** the render-gate drift channels (no
  per-artifact floor yet); `g1_floors_card2/`; `g1_grid` confirmatory seeds
  1–12 (superseded by the re-card; card diagnostic only).
- **Blind spots, stated where reported:** Γ cannot see arm-symmetric
  effects; every interval is conditional on the single 512-episode eval draw;
  no severity has both couplings strongly live (A marginal at High, B quiet at
  Medium); the co-active counter is A-only in mixed training.

## 5. Phase-close checklist (CLAUDE.md)

- [x] **Layout refreshed** against the tree (2026-09-27; it had omitted `paper/`).
- [x] **Locks:** no constant was ruled after the grid (the entries from
      *PRE-UNBLIND RULINGS* on rule interpretations, record results and
      reposition citations; none rules a constant); the Phase-6 analysis locks
      (`K_CONFIRMATORY_REALIZED`, `GAMMA_T_RETENTION`, `K_SECONDARY`,
      `K_LADDER_CAP`, `SIDAK_M`, `T_STAR`, …) are in `docs/locks.yaml`, and
      `test_locks.py` passed at this close.
- [x] **Phase report:** this file. Archives re-verified (§3).
- [x] **`HANDOFF.md` rewritten** for the writing phase.
- [x] §7 OWED item 5: the ISO configs' header now states the behavioural
      no-element share (generator change; the other 11 generated configs
      are byte-identical).

**Still owed by the owner:** the card-2 decision-log entry; a second copy of
the archives. (Unit 3: destroyed, owner-confirmed 2026-09-27.)
