<!-- PAPER V2 DRAFT (PAPER V2 ruling, 2026-10-11): builder-drafted, not owner-approved -->

## 4 Severity calibration

<!-- STUB-SPEC
ALTERNATE FOR OWNER CHOICE Q4g (C1): section 4 identical to sections/04_severity.md except that Corollary 1 has no item 4 (the supercritical shape statement) and therefore no garet2004chemical citation. Def. 4's High level still rests on the measured front speed (DX-6), not on item 4 (C1_verification section 2: "Def. 4's survival is a race rests on the measured front speed").
WRITER: W3. BUDGET: section 4's budget.
KEEP IN STEP: every change to sections/04_severity.md is mirrored here, so the two differ only in item 4 and its citation.
-->

Severity in CHE is placed by a measured dynamical phase of the fire: the three levels sit below, near and above the implemented kernel's measured transition (Figure 5).

<figure class="l-page">
  <iframe src="{{ 'assets/html/submission/severity_explorer.html' | relative_url }}" width="100%" height="528" style="border:none" title="Severity explorer: spanning probability against ignition probability, and one fire at each locked level" loading="lazy"></iframe>
  <figcaption><strong>Figure 5.</strong> Severity as a measured phase. Left: the spanning probability, the chance that one centre ignition reaches the arena boundary, against β on an all-fuel grid with no agents, for three arena sides (512 seeds per point<!-- N:DX-7 -->). Vertical rules mark the locked levels; the triangle marks the largest arena's pseudo-critical point. Right: one random-policy episode per level under the severity configurations, with δ 0<!-- N:DX-202 -->; only the fire and its smoke (hatching) are drawn. Neither the R<sub>L</sub> curves nor the locked critical point β̂<sub>c</sub> is shown (§4.3). <span class="figure-note">Status: calibration, no agents (curves) · illustrative, one episode each (renders) · Interact: play or drag the time slider; click a panel.</span></figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/severity_explorer.png" class="img-fluid" alt="Spanning probability of a centre ignition against ignition probability for three grid sizes, with the three locked severities marked, beside one illustrative fire episode at each severity." caption="Static companion of Figure 5 for the printed PDF." %}
</div>

### 4.1 Phase structure of the idealized kernel

**Corollary 1 (Critical point).** On $\mathbb{Z}^2$ with the von Neumann neighbourhood, the fire of Definition 3 with $\iota = 0$ and a single ignition at the origin inherits the critical point of bond percolation (Proposition 2, whose coupling holds on any graph): $\beta_c = 1/2$ exactly, the critical probability of bond percolation on the square lattice (Kesten, 1980)<d-cite key="kesten1980"></d-cite>.

It concerns the idealized kernel (von Neumann neighbourhood, constant burn time, homogeneous fuel, no wind) on the infinite lattice. CHE's fire is that kernel on a finite arena, with ignitions added by Coupling A (§3.2), so the levels are placed against a measured finite-size threshold and, at High, a measured front speed (§4.3).

### 4.2 Severity as phase

**Definition 4 (Severity regimes).** Fix the arena side $L$. Severity levels are defined by the position of the implemented kernel relative to its measured critical point $\hat\beta_c$, through the correlation length $\xi(\beta)$, the typical extent of a fire cluster:

- *Low*, subcritical, $\xi(\beta) \ll L$: fire clusters are local and short-lived, and survival is a local-avoidance problem.
- *Medium*, near-critical, $\xi(\beta) \sim L$: cluster sizes are scale-free up to the arena's size, fluctuations are maximal, and a single ignition can, with non-negligible probability, cascade to arena scale; survival is a global-anticipation problem.
- *High*, supercritical: fire fronts move at a speed comparable to the agents', and survival is a race.

The correlation length motivates the levels; operationally, each level is the observable band it was locked to (§4.3). As qualitatively different phases of one kernel, the levels make training at Low and High and evaluating at Medium (§9.1) a test of transfer to a phase neither arm trained in, though in the scalar $\beta$ it remains an interpolation (§10). Definition 4 also carried an expectation, on record before its test (§4.4), that per-episode outcome variance would peak at Medium.

### 4.3 Measuring the threshold and locking the levels

The calibration ran the fire alone on an all-Fuel grid at $L \in \{32, 48, 64\}$<!-- N:DX-7 -->, with 512 seeds per $(L, \beta)$<!-- N:DX-7 -->. A span sweep over 35<!-- N:DX-7 --> values of $\beta$ (0.05 to 0.95 coarsely, 0.40 to 0.60 in steps of 0.01<!-- N:DX-7 -->), each from one centre ignition for $T_{\max} = 4L$ steps<!-- N:DX-7 -->, measured $P_{\mathrm{span}}$, the burnt fraction and the front speed. A crossing sweep ignited the full left column and recorded the left–right crossing probability $R_L(\beta)$.

The severity lock fixed $\hat\beta_c = 0.500 \pm 0.005$<!-- N:CAL-1 -->, from logistic fits to $R_L$ with centres 0.4985, 0.5006 and 0.4999 at $L = 32, 48, 64$<!-- N:CAL-1 -->, and a self-duality check $R_L(0.500) = 0.488, 0.502, 0.494$<!-- N:CAL-2 -->. The lock record states that they were recomputed independently from the committed raw data; no committed script or artifact produces the logistic centres. Among the committed estimators, pairwise crossings of $R_L$ average 0.504<!-- N:CAL-1 -->; the family spans [0.480, 0.513]<!-- N:DX-204 -->, with consensus mean 0.499<!-- N:CAL-1 -->. All of them bracket Kesten's ½. That agreement validates the implementation; it is not a finding about fire, since Proposition 2 and Corollary 1 predict it for this kernel.

Each level was then locked to an observable band, with its measured values ($L = 64$<!-- N:DX-7 -->, 512 seeds<!-- N:DX-7 -->, no agents):

| level | $\beta$ | phase | $P_{\mathrm{span}}$ | burnt fraction | band the level was locked to |
|---|---|---|---|---|---|
| Low | 0.43<!-- N:CAL-3 --> | subcritical | 0.021<!-- N:CAL-3 --> | 1.9 %<!-- N:CAL-3 --> | $P_{\mathrm{span}} < 0.05$ and burnt fraction in [1, 5] %<!-- N:DX-201 --> |
| Medium | 0.49<!-- N:CAL-3 --> | near-critical | 0.547<!-- N:CAL-3 --> | 19.8 %<!-- N:CAL-3 --> | $P_{\mathrm{span}}$ in [0.3, 0.7]<!-- N:DX-201 --> |
| High | 0.70<!-- N:CAL-3 --> | supercritical | 0.998<!-- N:CAL-3 --> | 98.3 %<!-- N:CAL-3 --> | front speed in [0.5, 1.0] cells per step<!-- N:DX-201 -->, measured 0.83<!-- N:DX-6 --> |

At High the front moves at 83 %<!-- N:DX-6 --> of the agents' speed of one cell per step<!-- N:DX-6 -->, so it can be outrun, barely. Medium sits between the finite-size pseudo-critical point $\beta_c(64) \approx 0.486$<!-- N:CAL-4 -->, where $P_{\mathrm{span}} = 1/2$ at $L = 64$<!-- N:CAL-4 -->, and $\hat\beta_c$. It is the severity of the held-out evaluation configuration of §9, $\theta^* = (\beta, \kappa_A, \kappa_B, \delta)$ = (0.49<!-- N:CAL-3 -->, 0.06<!-- N:CA-1 -->, 1.0<!-- N:CB-1 -->, 1.0<!-- N:COM-6 -->); the compositional test trains at Low and High only.

### 4.4 Re-testing the Medium prediction

The calibration-phase probe at $d_p = 0.5$<!-- N:ENV-1 --> (the fire alone, 500 updates<!-- N:DX-203 -->, three seeds per severity<!-- N:DX-203 -->) had saved no checkpoints. The re-test at fixed policy re-ran it from the same configurations and seeds (equivalent, not bitwise identical) and evaluated each final checkpoint on 512 episodes<!-- N:DX-203 -->. For survival the prediction is refuted: per-episode variance at fixed policy is monotone in severity, 0.00091, 0.00709 and 0.00885 at Low, Medium and High<!-- N:CAL-5 -->. For completion it is not confirmed: Medium and Low tie within bootstrap intervals, 0.01245 against 0.01235<!-- N:DX-8 -->, both above High. The environment-level mechanism is confirmed: with no agents, the burnt fraction's variance peaks near $\beta \approx 0.53$<!-- N:DX-8 -->, just above Medium, and ranks Medium above High above Low at the locked levels.

The re-test report offers an account it did not test: outcome variance is roughly the environment's variance, which peaks near criticality, times the policy's sensitivity to it, which grows with severity. The refutation is scoped to survival, for these fire-only policies at this budget; §10 states what siting the held-out test at Medium costs.
