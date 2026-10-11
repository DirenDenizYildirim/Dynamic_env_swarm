<!-- BUILDER-WRITTEN DEMONSTRATION (DEMONSTRATION DRAFT ruling, 2026-10-11); not the owner's text -->

## 4 Severity calibration

Severity in CHE is a measured dynamical phase of the fire, not a value of $\beta$ chosen by hand. Figure 5 shows the measurement the three levels rest on, beside one fire burning at each level.

<figure class="l-page">
  <iframe src="{{ 'assets/html/submission/severity_explorer.html' | relative_url }}" width="100%" height="520" style="border:none" title="Severity explorer: spanning probability against ignition probability, and one fire at each locked level" loading="lazy"></iframe>
  <figcaption><strong>Figure 5.</strong> Severity as a measured phase. Left: the spanning probability P<sub>span</sub>, the chance that a single centre ignition reaches the arena boundary, against the per-neighbour ignition probability β, on an all-fuel grid with no agents, for L = 32, 48 and 64 (±1 binomial SE; 512 seeds per point<!-- N:DX-7 -->). Vertical rules mark the locked levels, Low 0.43, Medium 0.49 and High 0.70<!-- N:CAL-3 -->, and a triangle marks β<sub>c</sub>(64) ≈ 0.486<!-- N:CAL-4 -->, where P<sub>span</sub> = ½ at L = 64. Right: one random-policy episode at each level on the 64 × 64 arena<!-- N:ENV-6 -->, episode key 0<!-- N:DX-202 -->, under the severity configurations (κ<sub>A</sub> 0.06<!-- N:CA-1 -->, κ<sub>B</sub> 1.0<!-- N:CB-1 -->, δ 0<!-- N:DX-202 -->), each panel captioned with its level's calibration values. Only the fire (fuel, burning, burnt) and the smoke field ρ (light hatching) are drawn, not agents, food or structure. The figure does not show the locked critical point β̂<sub>c</sub> or the crossing curves it was read from (§4.3); each render is one episode, neither a distribution nor trained behaviour. <span class="figure-note">Status: calibration, no agents (curves) · illustrative · random policy · grades nothing (renders) · Interact: press play or drag the time slider (arrow keys step one frame, Shift with an arrow ten); click a panel to highlight its level on the curves; open “table view” for the levels and their values.</span></figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/severity_explorer.png" class="img-fluid" alt="Spanning probability of a centre ignition against ignition probability for three grid sizes, with the three locked severities marked, beside one illustrative fire episode at each severity." caption="Static companion of Figure 5 for the printed PDF." %}
</div>

### 4.1 Phase structure of the idealized kernel

**Corollary 1 (Phase structure).** On $\mathbb{Z}^2$ with the von Neumann neighbourhood, the fire of Definition 3 with $\iota = 0$ and a single ignition inherits the phase structure of bond percolation (Proposition 2, whose coupling holds on any graph, in particular $\mathbb{Z}^2$):

1. *Critical point.* $\beta_c = 1/2$ exactly, a theorem of Kesten (1980)<d-cite key="kesten1980"></d-cite>.
2. *Subcritical,* $\beta < \beta_c$. The burnt cluster is almost surely finite; its expected size $\chi(\beta)$ is finite, the cluster-size distribution has exponential tails, and the correlation length $\xi(\beta)$ is finite.
3. *Critical scaling,* $\beta \uparrow \beta_c$. $\chi(\beta) \sim \lvert\beta - \beta_c\rvert^{-43/18}$ and $\xi(\beta) \sim \lvert\beta - \beta_c\rvert^{-4/3}$, the exponents of two-dimensional percolation.
4. *Supercritical,* $\beta > \beta_c$. With positive probability the fire spreads indefinitely; conditioned on that, the burnt region grows linearly in time, with an asymptotic front speed $v(\beta) > 0$ and a deterministic limiting shape.

The exact value belongs to the idealized kernel (von Neumann neighbourhood, constant burn time, homogeneous fuel, no wind) on the infinite lattice. Other neighbourhoods, heterogeneous fuel, wind or geometric burn times shift $\beta_c$ and break exactness; the existence of the transition and the divergence of $\chi$ and $\xi$ near it are universal, and the design relies on nothing more. CHE's fire kernel on its own is the idealized kernel on a finite arena (Coupling A adds ignitions; §3.2), so the threshold that matters is a finite-size one, and it is measured (§4.3). We do not measure the critical exponents: the lock's decision record notes that their asymptotic regime is out of reach at $L = 64$<!-- N:ENV-6 -->.

### 4.2 Severity as phase

**Definition 4 (Severity regimes).** Fix the arena side $L$. Severity levels are defined by the position of the implemented kernel relative to its measured critical point $\hat\beta_c$, through the correlation length $\xi(\beta)$:

- *Low*, subcritical, $\xi(\beta) \ll L$: fire clusters are local and short-lived, and survival is a local-avoidance problem.
- *Medium*, near-critical, $\xi(\beta) \sim L$: cluster sizes are scale-free up to the arena's size, fluctuations are maximal, and a single ignition can, with non-negligible probability, cascade to arena scale; survival is a global-anticipation problem.
- *High*, supercritical: fire fronts propagate at a speed $v(\beta) > 0$ comparable to the agents' speed, and survival is a race.

The three levels are qualitatively different phases of one kernel, so the question “why these three?” has a principled answer, and training at Low and High while evaluating at Medium (§9.1) asks for transfer to a phase that neither arm trained in. In the scalar $\beta$ it remains an interpolation (§10). When Definition 4 was written it also carried an expectation: that survival at Medium would be least predictable and the most interesting behaviour would appear there, put on record as the prediction that per-episode outcome variance peaks at Medium. That is a prediction, not part of the definition, and §4.4 reports its test.

### 4.3 Measuring the threshold and locking the levels

The calibration ran the fire with no agents on an all-Fuel grid, at $L \in \{32, 48, 64\}$ with 512 seeds per $(L, \beta)$<!-- N:DX-7 -->. A span sweep over 35 values of $\beta$ (0.05 to 0.95 coarsely, 0.40 to 0.60 in steps of 0.01), each from a single centre ignition for $T_{\max} = 4L$ steps<!-- N:DX-7 -->, measured $P_{\mathrm{span}}$, the mean burnt fraction and the front speed. A crossing sweep ignited the full left column and recorded the left–right crossing probability $R_L(\beta)$, whose curves for different $L$ cross near the threshold.

The severity lock fixed $\hat\beta_c = 0.500 \pm 0.005$<!-- N:CAL-1 -->, from logistic fits to $R_L$ with centres 0.4985, 0.5006 and 0.4999 at $L = 32, 48, 64$<!-- N:CAL-1 -->, and a self-duality check $R_L(0.500) = 0.488, 0.502, 0.494$<!-- N:CAL-2 -->. These values come from the lock's decision record, which states that they were recomputed independently from the raw calibration data; the raw data is committed, but no committed script or artifact produces the logistic centres. The committed estimators give a slightly wider picture: pairwise crossings of $R_L$ average 0.504<!-- N:CAL-1 -->, and the calibration report's estimators span [0.480, 0.513]<!-- N:DX-204 -->, with consensus mean 0.499<!-- N:CAL-1 -->. Together they bracket Kesten's ½. That agreement validates the implementation; it is not a finding about fire, since Proposition 2 and Corollary 1 predict it for this kernel. A slow CPU test re-checks the sigmoid and a fixed threshold band around ½ (`che/tests/test_percolation.py`).

The levels were then fixed by observables, each required to fall in a band, and locked with their measured values (calibration at $L = 64$<!-- N:DX-7 -->, 512 seeds<!-- N:DX-7 -->, no agents):

| level | $\beta$ | phase | $P_{\mathrm{span}}$ | burnt fraction | band the level was locked to |
|---|---|---|---|---|---|
| Low | 0.43<!-- N:CAL-3 --> | subcritical | 0.021<!-- N:CAL-3 --> | 1.9 %<!-- N:CAL-3 --> | $P_{\mathrm{span}} < 0.05$ and burnt fraction in [1, 5] %<!-- N:DX-201 --> |
| Medium | 0.49<!-- N:CAL-3 --> | near-critical | 0.547<!-- N:CAL-3 --> | 19.8 %<!-- N:CAL-3 --> | $P_{\mathrm{span}}$ in [0.3, 0.7]<!-- N:DX-201 --> |
| High | 0.70<!-- N:CAL-3 --> | supercritical | 0.998<!-- N:CAL-3 --> | 98.3 %<!-- N:CAL-3 --> | front speed in [0.5, 1.0] cells/step<!-- N:DX-201 -->, measured 0.83<!-- N:DX-6 --> |

At High the front moves at 0.83 cells per step, 83 % of the agents' speed of one cell per step<!-- N:DX-6 -->: it can be outrun, barely, and nearly the whole arena eventually burns. Medium sits between the finite-size pseudo-critical point $\beta_c(64) \approx 0.486$<!-- N:CAL-4 -->, where $P_{\mathrm{span}} = 1/2$ at $L = 64$, and $\hat\beta_c$, in the arena's near-critical regime. It is the severity of the held-out evaluation configuration of §9, $\theta^* = (\beta, \kappa_A, \kappa_B, \delta)$ = (0.49<!-- N:CAL-3 -->, 0.06<!-- N:CA-1 -->, 1.0<!-- N:CB-1 -->, 1.0<!-- N:COM-6 -->). The compositional test trains at Low and High only.

### 4.4 Re-testing the Medium prediction

The prediction was on record before its re-test at fixed policy (M3.0). The re-test used the calibration-phase probe at $d_p = 0.5$<!-- N:ENV-1 --> (the fire alone, 500 updates<!-- N:DX-203 -->, three seeds per severity<!-- N:DX-203 -->). That probe had saved no checkpoints, so it was re-run with the same configurations and seeds (equivalent, not bitwise identical), and the re-test evaluated its final checkpoints on 512 episodes each<!-- N:DX-203 -->. Its outcome has three parts:

- *Survival: refuted.* The per-episode variance at fixed policy is monotone in severity, 0.00091, 0.00709 and 0.00885 at Low, Medium and High<!-- N:CAL-5 -->, highest at High.
- *Completion: not confirmed.* Medium and Low tie within their bootstrap intervals, 0.01245 against 0.01235<!-- N:DX-8 -->, both above High.
- *Environment-level mechanism: confirmed.* With no agents, the variance of the burnt fraction peaks near $\beta \approx 0.53$<!-- N:DX-8 -->, inside the near-critical window just above the Medium level, and at the three locked levels it ranks Medium above High above Low.

The re-test report offers an account of the mismatch, not a separate test of it: outcome variance is roughly the environment's variance times the policy's sensitivity to it, and while the first factor peaks near criticality, the second grows with severity: at Low a trained policy absorbs the fire's fluctuations at the survival ceiling, and at High every realization couples into deaths and lost food. What the re-test establishes is narrower. Among the three levels the fire's own outcome varies most at Medium, a property of the environment; trained policies' survival does not, which refutes the prediction for survival, for these fire-only policies at this budget. What siting the held-out test at Medium costs is stated in §10.
