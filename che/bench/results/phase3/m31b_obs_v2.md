# M3.1b — obs v2 (D5) causal-mechanism confirmation

**Registered check (D5, decision log):** retrain the three seed-0 severity
probes under obs v2 (indicator planes), re-render medium's exact m30b episode
seeds, and answer two pre-registered questions:

1. Does the post-fire burnt-region abandonment disappear?
2. Does the completion-ordering anomaly (medium ≥ high) flatten out?

**Answers: (1) yes, decisively. (2) the inversion disappears — the diagonal is
now strictly monotone in severity.** Details, evidence, and one flagged
deviation (bench cell is *not* neutral) below.

D5 note: everything in this file is the *registered mechanism diagnostic* that
D5 itself commissioned. Per D5, obs-v1 numbers are archived probes and are
never comparable paper results; no v1-vs-v2 number below is a result claim.

## Provenance

- GPU box: vast.ai RTX 5090, jax 0.11.0, code at `1706cb6`
  (M3.1b local half), job `che/scripts/run_m31b_obs_v2.sh`,
  console log `m31b_console.log` (kept out of git with the tarball).
- Training identical to M3.0 seed-0 probes except `obs_version: 2`:
  500 updates, seed 0, death-penalty 0.5, per-severity configs.
  Wall time ~285 s/run (v1: ~266 s, −7% training throughput).
- Checkpoints + evals in `m31b/` (ckpts gitignored as usual):
  config hashes low `1408f1d114df138d`, medium `25767760c9754d76`,
  high `718eb7f871ca098f` (v2 schema).
- Local re-renders: `m31b/renders/medium_v2_s0_ep{0..7}.gif` — same seeds as
  `m30b/renders/medium_s0_ep{0..7}`, byte-deterministic episode reproduction
  confirmed (diagnostic rollouts reproduce every rendered final completion
  exactly). Only ep1/ep3 GIFs committed (m30b precedent); all JSONs committed.

## v2 probe evals (512 stochastic episodes, seed-0 checkpoints)

| severity | completion | survival | deaths_fire/ep | v1 seed-0 diagonal (archived probe) |
|---|---|---|---|---|
| low | 0.714 | 0.993 | 0.09 | 0.748 / 0.991 / 0.11 |
| medium | 0.766 | 0.954 | 0.55 | 0.789 / 0.965 / 0.42 |
| high | **0.802** | **0.935** | **0.78** | 0.786 / 0.864 / 1.63 |

Single training seed per cell (that was the registered scope) — per-severity
deltas carry training-seed noise; the *pattern* is what was registered.

## Q1 — burnt-region abandonment: gone

Visual (matched timesteps, same seeds, same fire footprints):

- **ep3 (the pathological showcase):** v1 completion freezes at 0.59 from
  t=146 to the horizon — remaining food sits stranded inside the burnt region
  while the swarm circles outside it. v2 forages straight through the ash:
  0.75 → 0.84 → 0.91 → **0.97 final** on the identical layout.
- **ep1:** post-fire (t≥110) v1 agents hug the unburnt remainder; v2 agents
  spread through the burnt interior and lead at every matched timestep
  (0.84 vs 0.69 at t=110; final 0.91 vs 0.84).

Quantitative (`che/scripts/burnt_occupancy.py` → `m31b/burnt_occupancy.json`):
post-fire burnt-cell occupancy ratio, (share of alive agents on Burnt) /
(share of grid that is Burnt); 1 = indifference. Over the six seeds with
substantive fires (seeds 0 and 5 fizzle at t≈1, leaving a degenerate
few-cell denominator):

| policy | median | mean | per-seed (1,2,3,4,6,7) |
|---|---|---|---|
| v1 medium | **0.27** | 0.36 | 0.16, 0.92, 0.07, 0.20, 0.46, 0.33 |
| v2 medium | **1.58** | 2.33 | 1.42, 0.65, 1.60, 1.55, 6.87, 1.88 |

v1 under-occupies ash ~4× below indifference (avoidance in 5/6 seeds); v2 is
at-or-above indifference in 5/6 — consistent with rationally sweeping the
late-episode food that mid-fire foraging skipped. The v1 mechanism (Burnt=1.0
reads as *more* dangerous than Burning=0.5 on the ordinal hazard plane) no
longer exists in v2's separate indicator planes.

## Q2 — completion ordering: inversion gone, now strictly monotone

- v1 diagonal: 0.748 < 0.789 ≥ 0.786 (medium/high inverted, near-flat top).
- v2 diagonal: 0.714 < 0.766 < 0.802 (strictly increasing in severity).

The anomaly did not "flatten toward equality" — it resolved: the artifact
suppressing High-trained (fear of its own large ash fields, plus
*underestimating active fire*, which v1 scored as half as dangerous as ash)
is gone. High-trained survival jumps 0.864 → 0.935 with per-episode fire
deaths halved (1.63 → 0.78) — exactly the signature predicted by the
encoding-artifact hypothesis.

Honest caveat: low and medium completion dip slightly (−0.03, −0.02), and the
ep5-style *fire-free* episodes show v2 medium stalling at edges where v1
swept better (ep5: 0.66 vs 0.81; ep2 similar). One training seed each — noise
vs. real coverage regression is unresolved and does not affect the D5
question. Worth an eye at M3.5 acceptance training (3 seeds, longer runs).

## Reference bench cell — flagged deviation from D5 expectation

D5 said "expect ~neutral". Measured (same box, same jax 0.11.0, same
protocol as `obs_v1_ref_cell.json`):

| obs | median env steps/s | Δ vs v1 | peak mem |
|---|---|---|---|
| v1 (5 planes) | 12,652,933 | — | 0.125 GiB |
| v2 (7 planes) | 9,580,456 | **−24.3%** | 0.151 GiB |

Env-only stepping pays for the 5→7-plane crop; end-to-end *training* pays only
−7% (70.9k → 66.0k env-steps/s) because the env share of a train step is
small. Training projection at the Phase-0 env:train ratio (÷81): **~118.3k
train steps/s — still above the 100k contingency line**, margin reduced from
~56k to ~18k. No scope change made; flagged here for the human review. Full
row appended to `gate_report.md`.

## Verdict

- Both registered questions answered in the direction D5 predicted; the
  mechanism (v1 ordinal-hazard encoding artifact) is confirmed as causal.
- Obs v2 locked for M3.2 onward; v1 archived (probes labeled obs-v1; no
  cross-version comparisons ever).
- One open flag for the human: bench cell −24.3% (not neutral); 100k line
  still cleared.
