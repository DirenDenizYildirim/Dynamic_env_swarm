# G1.0(b) — the throughput A/B, measured at last

**Date:** 2026-08-10. **Tree:** `ff92da7`. **Status:** the OWED item from the
2026-08-04 *TRAINING LOGGER GAINS THE COUPLING COUNTERS* entry is
**DISCHARGED**. Two prior attempts were killed before they flushed, so until
today there was no number at all — not even indicative.

## The box

| | |
|---|---|
| provider / device | vast.ai — **NVIDIA RTX PRO 6000 Blackwell Workstation Edition** |
| device memory | 97,887 MiB |
| driver | 595.58.03 |
| **power cap** | **500.00 W** — recorded because it is a per-hardware fact and the WS card's nominal is higher |
| host | 128 cores, 498 GB RAM, 32 GB container overlay |
| toolchain | **Python 3.12.3, jax 0.11.0, jaxlib 0.11.0**, `CudaDevice(id=0)` |
| `workspace_is_volume` | **false** — nothing on this instance survives recycle/destroy |

Box gate passed on every clause of `gpu_launch_prompt.md`: the card is the
required PRO 6000 (a 31.8 GiB 5090 cannot host this — the run below peaks at
**67.25 GiB**), the network measured **118 MB/s** against a 46 MB/s "fine"
bar, and the toolchain is the certified 0.11.0 rather than the 0.10.2 that a
Python-3.11 venv silently resolves.

## Method

`bench_population(windows=5, window_secs=30.0, seed=0)` on
`che/configs/gate_pop12.yaml` — the spending configuration the standing
throughput rule binds gates to. Run as **two separate processes** so neither
arm inherits the other's compilation cache. The OFF arm clears
`ippo.STEP_METRICS` before tracing; `STEP_METRICS.items()` is iterated inside
the traced rollout body (`ippo.py:317`), so clearing genuinely removes the
reads and lets XLA dead-code-eliminate the channels.

## Result

| arm | channels | median steps/s | window rates | IQR | peak device bytes | compile |
|---|---|---|---|---|---|---|
| **ON** (as-is) | 9 | **60,861** | 60895, 60751, 60785, 60861, 60979 | 169 | 72,209,845,248 | 95.51 s |
| **OFF** (cleared) | 0 | **60,874** | 60874, 60801, 60840, 60915, 60988 | 131 | 72,209,845,248 | 95.47 s |

**Delta: 13 steps/s, 0.021 %** — the ON arm nominally slower.

**STATED AS A RESOLUTION LIMIT, NOT AS AN EFFECT.** 13 steps/s is an order of
magnitude inside either arm's own IQR (169 and 131, i.e. ~0.25 %). This
instrument cannot distinguish the two arms. The defensible claim is
**"the logging cost is below ~0.25 %"**, not "the logging cost is 0.021 %" —
quoting the point estimate would be a bar finer than its instrument, which
this project treats as void by construction.

Two corroborating signals that the channels are near-free:

- **Peak device memory is identical to the byte** across arms
  (72,209,845,248 = 67.25 GiB). The channels are scalar reductions; XLA's
  memory plan does not move.
- **Compile time is identical** to 0.04 s (95.51 vs 95.47).

### Registered branch: **< 5 % → ABSORB**

Per the G1.0(b) table, fixed before the number was seen: *"absorb it. Note in
the report; the 686 s/run basis stands."* No re-derivation of the run cost is
required, and the `> 15 %` drop-channels branch — the one that would have
changed the artifact the floors are measured on — is not reached.

### One honest limit on what this A/B attributes

`alive_agents` is read **twice** in the collector: once via `STEP_METRICS`
(added 2026-08-10) and once as a standalone `Transition` field at
`ippo.py:315`, which feeds `mean_out_degree` and predates this change.
Clearing `STEP_METRICS` does not remove the second read, so the OFF arm still
computes that channel. **The A/B therefore measures the full cost of eight
channels and the marginal cost of the ninth.** Since the ninth was already
being computed, its true marginal cost is near zero by construction — which
is a reason the total is small, and a reason not to read the total as
"9 channels cost 0.02 %".

## The cost basis, and a favourable surprise

The 686 s/run basis behind the $45.73 grid authorization was derived on the
**M6.2b card**, whose throughput the cost table records as **~52,000
steps/s**; the faster **M6.2 card** in the same table is **~60,900 steps/s**
(`decision_log.md`, M6.2b CLOSE-OUT item 3).

**This box measures 60,861 steps/s — the M6.2-card figure, not the M6.2b
one.** If the s/run scales with it, the grid would land nearer the 557 s/run
row than the 686 s/run row.

**That extrapolation is deliberately NOT taken here.** The log's own
attribution (228 × (686 − 557) s for a 60,900 → 52,000 change) is not exactly
proportional, so the mapping from bench steps/s to grid s/run is not a clean
ratio, and re-deriving a cost from it would be exactly the kind of
transliterated arithmetic the derived-numbers rule exists to stop. **The
launch batch prints the measured s/run directly, and that figure supersedes
every extrapolation including this paragraph.**

## Provenance note on the committed record

The two committed `Aggregate training throughput` rows in the tree are a
different configuration and a different card — 159,011 steps/s (Phase-0
config, `results/gate_report.md`) and 142,421 steps/s (RTX 5090 at
`n_envs` 256, `results/phase5/m51d/gate_rows_A.md`, where the Phase-5 report
also records that **`gate_pop12.yaml` did not compile on the 5090, twice**).
The ~60,900 / ~52,000 figures live only inside the decision log's cost
derivation, with no committed bench row behind them. **This is therefore the
first committed bench row for `gate_pop12.yaml`.**

## Raw

`g1_0b_ab.json` — both arms' full `bench_population` dicts as emitted.
