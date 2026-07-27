# Coupling-B Lock — M4.3 (**STOP: the three bands do not intersect**)

Date: 2026-07-27. RA calibration of the full environment
(`che/calibration/coupling_b.py`; 64 episodes/severity, L = 64, 12 agents,
horizon 256, obs v3, Coupling A live at its M3.4-locked values — the
severity YAMLs are loaded directly, so the calibration cannot drift from
the training configs). Raw data
`che/bench/results/phase4/m43/coupling_b_calibration.json` (commit
110da6a, wall 21.6 s, CPU); figure `m43/kappa_b_bands.png`.

**This is not a lock proposal.** Per the M4.2 ruling item 5 — "if the
three lock bands fail to intersect, STOP with the three curves side by
side; a non-empty intersection was an assumption, and its failure is a
finding to bring to the lock discussion, not something to route around"
— the milestone stops here. No candidate satisfies even two of the three
bands, and one band is unreachable at **any** κ_B.

## Targets (phase4_prompt.md M4.3)

| observable | band |
|---|---|
| Medium, alive agents, fire-active steps: `masked_frac` | [0.15, 0.45] |
| P(Burning cell at crop distance 3 revealed \| typical Medium smoke) | [0.4, 0.7] |
| E2C cross-reference q(κ_B) | [0.3, 0.7] |

## Measured sweep (random policy)

`masked_frac` and `detection` are computed as **expectations** — the
mean of (1 − τ) over crop cells and the mean of τ over Burning ring
cells — which are exactly the expectations of the realized channels with
the Bernoulli noise integrated out (pinned against the env's own
`masked_frac` info channel in `test_coupling_b_calib.py`). All
candidates are evaluated on **one rollout per severity** (CRN); for an
obs-blind policy this is exact, since κ_B cannot perturb the trajectory
(invariant #3).

| κ_B | Med masked_frac | masked\|exposed | Med detection | E2C q | detection Low / High | masked Low / High |
|---|---|---|---|---|---|---|
| 0.05 | 0.001 ✗ | 0.003 | 0.950 ✗ | 1.000 ✗ | 0.951 / 0.946 | 0.000 / 0.003 |
| 0.10 | 0.001 ✗ | 0.006 | 0.903 ✗ | 0.999 ✗ | 0.906 / 0.895 | 0.001 / 0.006 |
| 0.20 | 0.003 ✗ | 0.012 | 0.817 ✗ | 0.996 ✗ | 0.821 / 0.803 | 0.001 / 0.012 |
| 0.35 | 0.004 ✗ | 0.020 | 0.704 ✗ | 0.983 ✗ | 0.711 / 0.686 | 0.002 / 0.019 |
| **0.50** | 0.006 ✗ | 0.027 | **0.609 ✓** | 0.958 ✗ | 0.618 / 0.588 | 0.002 / 0.025 |
| 0.75 | 0.008 ✗ | 0.036 | **0.482 ✓** | 0.894 ✗ | 0.491 / 0.459 | 0.003 / 0.033 |
| 1.00 | 0.010 ✗ | 0.043 | 0.384 ✗ | 0.812 ✗ | 0.393 / 0.362 | 0.004 / 0.039 |
| 1.50 | 0.012 ✗ | 0.055 | 0.247 ✗ | **0.626 ✓** | 0.255 / 0.230 | 0.005 / 0.049 |
| 2.00 | 0.014 ✗ | 0.064 | 0.162 ✗ | **0.456 ✓** | 0.168 / 0.149 | 0.005 / 0.055 |
| 3.00 | 0.017 ✗ | 0.076 | 0.072 ✗ | 0.222 ✗ | 0.075 / 0.066 | 0.007 / 0.064 |

Admissible κ_B per band, by log-linear interpolation:

| band | admissible κ_B |
|---|---|
| masked_frac ∈ [0.15, 0.45] | **none — unreachable at any κ_B** |
| detection ∈ [0.4, 0.7] | [0.36, 0.95] |
| E2C q ∈ [0.3, 0.7] | [1.28, 2.62] |

![three bands](che/bench/results/phase4/m43/kappa_b_bands.png)

## Finding 1 — the Medium `masked_frac` band is occupancy-limited, not attenuation-limited

A crop cell can only ever be masked if its line of sight carries optical
depth (D = dist · mean_ρ > 0); cells with no smoke on the ray are
transparent at *every* κ_B. The share of such carrier cells is therefore
the **ceiling** `masked_frac` approaches as κ_B → ∞, and it is set by
geometry and by where the swarm stands — not by the coupling:

| severity | masked_frac ceiling (κ_B → ∞) | exposed-agent share | fire-active steps/ep |
|---|---|---|---|
| Low | 0.028 | 0.093 | 56 |
| **Medium** | **0.130** | 0.266 | 131 |
| High | 0.419 | 0.529 | 89 |

**Medium's ceiling, 0.130, is below the band's floor of 0.150.** Measured
directly (`--kappas 3 10 100 1000`): masked_frac rises 0.017 → 0.025 →
0.037 → 0.048, still climbing toward 0.130 at κ_B = 1000. Seed-stable
(0.1304 at seed 0, 0.1317 at seed 1).

The mechanism: on fire-active steps only 26.6 % of alive agents have any
smoke on any crop ray at all, because smoke decays at η = 0.5 (half-life
1.4 steps) and so tracks the *fire front*, not the burn scar — a thin,
moving structure on a 64² arena with 12 agents. Averaged over the swarm,
87 % of crop cells are transparent by construction. At the κ_B values
the other two bands admit (0.36–2.62) the observable reads 0.004–0.014,
i.e. **10–35× below the band floor**.

Note the ladder: at High the ceiling is 0.419 and the band *is* within
reach (though only at κ_B ≳ 3, where detection has collapsed to 0.07).
The band as written is satisfiable in principle — just not at the
severity it was written for.

## Finding 2 — detection and E2C q are disjoint by ~1.35×

The two reachable bands admit [0.36, 0.95] and [1.28, 2.62]. The gap is
the geometry dependence flagged and acknowledged at the M4.2 STOP: E2C's
single-cell smoke source is sampled only at the ray's endpoint, so its
optical depth is ≈ dist · ρ/4, while the swarm env's extended smoke is
sampled along the whole ray. The same κ_B therefore bites ~2–3× harder
in the arena than in E2C, exactly as predicted when Option-A geometry
was approved. **These q values are Option-A E2C and must be quoted as
such.**

## Obligation discharged — detection ring is in the well-sampled regime

M4.2 ruling item 2 required this to be explicit, not implicit:
`endpoint_sampled_fraction` = **1.0** for the distance-3 ring at k = 9
and k = 17 — every ring cell is occludable by a single-cell source at
that cell, so Finding 1 of M4.2 does not touch the detection band. (The
same function returns < 1 at distance ≥ 5.) Pinned by
`test_detection_ring_is_in_the_quadrature_sampled_regime`.

Incidental but useful: detection is nearly **severity-portable** —
0.618 / 0.609 / 0.588 across Low / Medium / High at κ_B = 0.5 — because
it already conditions on a Burning cell being 3 away, so it measures the
local smoke structure at a fire front, which is similar in all three
regimes. Neither of the other two observables has this property.

## Options for the lock discussion

**A. Lock from the detection band; demote the other two to reported
diagnostics.** κ_B ∈ [0.36, 0.95]. Detection is the only band that is
reachable, measured in the production env, at a distance the quadrature
resolves, and severity-portable. `masked_frac` and E2C q get recorded
with their measured values and the reasons they could not bind.

**B. Re-scope the masked_frac band to the geometry.** Either condition
it on exposed agents (`masked|exposed`, 0.020–0.041 over the detection
interval) or lower the absolute band toward the ceiling. Both are honest
re-readings of the intent — "perception meaningfully degraded, not
blind" is about agents *near* smoke, and the arena average is diluted by
the 73 % of agents nowhere near fire. Note that even conditioned, the
numbers are small: the intent may need restating in terms of detection.

**C. Re-scope or drop the E2C cross-reference band.** Its κ_B scale is a
property of the Option-A micro-env geometry, not of the environment the
paper trains in. Keeping it as a *lock band* imports a toy's geometry
into the env's parameter; keeping it as a *reported* number preserves
the Thm.-1 link without that.

**D. Change the environment** (σ_s, η, agent count, arena size) so
Medium's smoke coverage is higher. **Explicitly out of scope** — the
phase-4 non-goals forbid smoke-parameter changes, and this would
invalidate the Phase-2 severity calibration.

### RA recommendation: A + C, propose **κ_B = 0.5**

Detection 0.609 (mid-band), masked_frac 0.006 (Medium) / 0.025 (High),
E2C q 0.958. Rationale: the detection band's intent clause ("meaningfully
degraded, not blind") is the one the measurement can honour — at
κ_B = 0.5 a Burning cell three cells away is seen ~61 % of the time,
degraded but far from blind, and the value transfers across all three
severities. Taking the E2C band instead (κ_B ∈ [1.28, 2.62]) would put
detection at 0.25–0.16 — a Burning cell three cells away seen one time
in five, which reads as *blind*, contradicting the stated intent of the
first band.

If instead you weight the Thm.-1 cross-reference highest, κ_B = 1.5 is
the natural pick (q = 0.626, detection 0.247) — but then the M4.4 grid
should expect a large completion/survival cost at Medium and High, and
the report should say the coupling was set to the theory's
partial-information point rather than the env's detection band.

## Probe policies — not run

The prompt calls for one fresh 200-update probe policy per severity
alongside the random policy. **Not run:** the STOP triggered on the
random-policy sweep, and the probes cost GPU time that the lock
discussion may redirect. `che/scripts/run_m43_probes.sh` is ready — it
trains the three probes (~6 GPU-minutes total at 200 updates) and
re-runs this calibration under them, writing
`m43/coupling_b_calibration_probe.json`.

Worth knowing before deciding: the ceiling is **policy-dependent**. A
fire-avoiding trained policy would lower exposure and push Medium's
ceiling further below the band; a food-chasing one could raise it.
`--probe-kappa-B` defaults to 0.5 (the recommendation above); the
resulting mild circularity — the probe's state distribution is induced
at one candidate — is why the sweep holds that distribution fixed and
evaluates all candidates on it (CRN), rather than re-rolling per
candidate.
