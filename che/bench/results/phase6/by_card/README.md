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

### RTX 5090 — `rtx5090/` — three rented UNITS of the same model

Updated 2026-09-27 at the Phase-6 close; every row is pulled and
hash-verified locally. Unit identities: unit 1 `180.189.55.43:13768` (UUID
never recorded; gone — vast.ai re-rented it); unit 2
`GPU-cc0a5b55-…` (decision log, *BOX CHANGE* entry §2; destroyed by the owner
2026-09-26); unit 3 `GPU-c4a5b128-…` (`post_gamma_t/UNIT.txt`; SSH refused
2026-09-27, owner to confirm it is destroyed rather than stopped).

| directory | unit | what |
|---|---|---|
| `g1_floors_5090` | 1 | G1.2-protocol floors, 24 runs. Ladder **BRANCH C** (`k_req` completion 72) |
| `g1_conf_5090` | 1 | **Confirmatory at k = 72**, one stamp, all 72 seeds on unit 1 (seeds 13–46 copied from `g1_grid`) |
| `g1_sec_s1_12_5090` | 1 | secondary re-card, seeds 1–12, the 8 secondary arms (96 runs) |
| `g1_iso4_5090` | 2 | ISO-4 sensitivity arm, k = 20 (§7 proposal 1) |
| `g1_t2000_5090` | 2 | T = 2000 subsample, 4 seeds × ISO/JOINT (descriptive) |
| `post_gamma_t`, `post_high`, `post_evalfloor` | 3 | post-unblind evals only (no training): Γ(t), High readout, eval floor |

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

The single-card conversion is complete: `g1_grid`'s **confirmatory** seeds
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
