# Which card produced what — Phase 6

**Navigation aid, not the artifacts.** `pro6000/` and `rtx5090/` hold
**symlinks**. Nothing was moved or copied. This file is the authoritative
map; the symlinks are for convenience.

## Why nothing was physically split

**`g1_grid/` contains BOTH cards and cannot be split.** Its 252 archives sit
beside a single `.manifest/`, a single `grid_params.txt` stamp and a single
`SHA256_CKPT.txt`. `lib_run_manifest.sh::manifest_complete` requires an
archive and its manifest entry in the **same directory**, and re-hashes the
archive; `manifest_assert_all` checks every tag by name. Moving archives out
would break resume, break the pull script's guard, and break the audit trail
that makes the grid citable. It stays whole.

## The map

### RTX 5090 — `rtx5090/`

| directory | what | status |
|---|---|---|
| `g1_floors_5090` | G1.2-protocol floors on the 5090, 24 runs. Produced ladder **BRANCH C** (`k_req` completion 72) | on the box, not yet pulled |
| `g1_conf_5090` | **Confirmatory at k = 72**, one stamp, all 72 seeds on the 5090. Seeded with conf seeds 13–46 copied from `g1_grid`, then runs seeds 1–12 and 47–72 | running |
| *(secondary re-card)* | seeds 1–12, the 8 secondary arms | pending |

### RTX PRO 6000 — `pro6000/`

| directory | what |
|---|---|
| `g1_floors` | G1.2 launch batch, 2026-08-10 (archives rebuilt — see its README) |
| `g1_floors_2026-09-08` | G1.2 re-floor that set **K_CONF = 46** (branch B) |
| `m60` | M6.0 traced-θ spike |
| `m62` | M6.2 floors at T = 500 |
| `m62b` | M6.2b floors at T = 1000 |

### MIXED — `../g1_grid/` — **deliberately not filed under either card**

252 runs, both cards. `cards.txt` in that directory is the per-run record.

| seeds | arms | card |
|---|---|---|
| 1–12 | all 10 | **RTX PRO 6000** |
| 13–20 | all 10 | **RTX 5090** |
| 21–46 | iso, joint only | **RTX 5090** |

**One card per seed throughout — no seed is split across cards.** That is the
property the analysis depends on.

After the single-card conversion completes, `g1_grid`'s **confirmatory** seeds
1–12 are **superseded** by `g1_conf_5090` and must not be used in Γ. Its
secondary seeds 13–20 remain live.

### UNKNOWN CARD — `../g1_floors_card2/` — **cannot be filed**

A partial re-floor from 2026-08-14 whose card **was never recorded**. It
grades nothing and an owner decision-log entry is owed on it. It is not
filed under either card because nobody knows which one it was — filing it by
guess is exactly the error these folders exist to prevent.

## Rulings behind this layout

- **CARD RULING** (`a7eb245`) — the grid remainder moved to the 5090
- **Amendment** (`7b0c30e`) — realized timings; a cross-card eval floor is owed
- **SINGLE-CARD CONFIRMATORY** (`96e1569`) and its extension (`87ec7f5`)
- **LADDER BRANCH C** (`30151d7`) — cap raised 60 → 72
