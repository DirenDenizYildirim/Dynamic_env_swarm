<!-- PAPER V3 DRAFT (PAPER V3 ruling, 2026-10-12): builder-drafted, not owner-approved -->

### B Locked constants and hyperparameters

<!-- STUB-SPEC
JOB: Every locked constant with its value (dates live in Appendix D), the hyperparameters and budget, the message encoder (Listing 6), and Coupling B's lock bands that did not intersect.
WRITER: W2.
BUDGET: about 350 prose words plus tables.
FROM: P1 §6.1 B; B1 (Listing 6 moved here from v2 §7, page budget).
ROWS: CAL-1, CAL-3, CA-1, CB-1, COM-6, ENV-1, ENV-12, DX-1, DX-2, DX-3, DX-17, DX-401, DX-402 (values only; dates to Appendix D), CB-2, CB-3, DX-12, DX-301, DES-13.
LISTINGS: Listing 6, che/train/ippo.py:323-329 (stop_gradient: the message encoder is frozen; ENV-12). Block below.
REGISTERED STRINGS: none.
EVERY OTHER CAVEAT in checks/caveats.yaml: pointer only ("§6.3", "Appendix D"), never restated. C26: any sentence about the interaction check carries "post hoc".
NOT HERE: ruling dates (Appendix D); study codes without the key; "lock record" phrasing aimed at a reader who cannot see it.
V2 MATERIAL: paper/v2/sections/13_appendix_locks_floors.md (B); 06_coupling_b.md §6.3; 07_comms.md (Listing 6).
DEPENDENCIES: §3 points here for hyperparameters and the encoder.
-->

Each constant below was fixed before the main experiment; Appendix D gives when. A test in the code supplement (`che/tests/test_locks.py`) checks each against the configurations, the code defaults or the analysis scripts that must carry it.

| constant | value | described in |
|---|---|---|
| critical point $\hat\beta_c$ | 0.500 ± 0.005<!-- N:CAL-1 --> | §4.1, with its estimator's provenance |
| β at Low / Medium / High | 0.43 / 0.49 / 0.70<!-- N:CAL-3 --> | §4.1 |
| β held out ($\theta^*$) | 0.49<!-- N:CAL-3 --> | §6.2 |
| $f_{\mathrm{weak}}$, $\lambda_0$, $\lambda_{\mathrm{load}}$, $\kappa_A$, $r_A$ | 0.15, 5e-5, 4e-4, 0.06, 1<!-- N:CA-1 --> | Definition 5 |
| smoothing passes of the weak-terrain field | 2<!-- N:DX-401 --> | Definition 5 |
| $\kappa_B$ | 1.0<!-- N:CB-1 --> | Definition 6; the bands below |
| δ off / on; $R_{\mathrm{comm}}$ | 0.0 / 1.0<!-- N:DX-401 -->; 16<!-- N:COM-6 --> | Definition 7 |
| death penalty $d_p$ | 0.5<!-- N:ENV-1 --> | Definition 2 |
| observation encoding | the observation as masked by smoke<!-- N:DX-401 --> | Definition 6 |
| $\sigma_s$, η, ι | 1.0, 0.5, 0.0<!-- N:DX-1 --> | Definition 3; not locked, fixed by convention and never calibrated |

The analysis constants of the worked example (§6) are fixed the same way.

| constant | value | role |
|---|---|---|
| `K_CONFIRMATORY` | 40<!-- N:DES-1 --> | design seeds per confirmatory arm, the base of the registered seed rule |
| `K_LADDER_CAP` | 60<!-- N:DES-1 --> | the seed rule's cap |
| `K_CONFIRMATORY_REALIZED` | 72<!-- N:DES-13 --> | the seed count at which Γ is read (§6.2; history in Appendix D) |
| `K_SECONDARY` | 20<!-- N:DES-13 --> | seeds per secondary arm; ISO-4 uses the same count |
| `SIDAK_M`; $z_\alpha$ | 2; 2.2365<!-- N:DES-13 --> | the two co-primary tests, Šidák-corrected |
| `POWER_STOP` | 0.80<!-- N:DX-402 --> | the minimum design-stage power |
| `T_STAR` | 1000<!-- N:DES-13 --> | the training budget in updates |
| `GAMMA_T_RETENTION` | 11<!-- N:DES-13 --> | checkpoints kept for Γ(t): updates 500–1000 every 50<!-- N:DES-13 --> |
| evaluation draw | seed 0 × 512 episodes<!-- N:DES-13 --> | common to every run; not in the constant registry |
| `PLATEAU_PASS`; `PLATEAU_REVIEW` | 1.0; 1.5<!-- N:DX-402 --> | thresholds of a convergence check, retired when the estimand was fixed at a matched budget, before the main training runs |

Every run of the worked example uses the hyperparameters below. The main training runs pass none on the command line, so the configured defaults apply.

| hyperparameter | value |
|---|---|
| learning rate | 3e-4, constant, no schedule<!-- N:DX-2 --> |
| discount γ; GAE λ | 0.99; 0.95<!-- N:DX-2 --> |
| PPO clip ε | 0.2<!-- N:DX-2 --> |
| entropy coefficient; value coefficient | 0.01; 0.5<!-- N:DX-2 --> |
| global gradient-norm clip; Adam ε | 0.5; 1e-5<!-- N:DX-2 --> |
| parallel environments; steps per update | 256; 128<!-- N:DX-2 --> |
| minibatches; epochs | 4; 4<!-- N:DX-2 --> |
| checkpoint interval | 50 updates<!-- N:DX-2 --> |
| budget | 32,768 environment steps per update, 32,768,000 per run<!-- N:DX-3 --> |
| network | two convolutions with 16 and 32 channels, a dense layer of 128 units, actor and critic heads with a 64-unit layer each<!-- N:ENV-10 --> |
| messages | dimension 8, delivered one step later as a masked mean over open links<!-- N:DX-17 --> |

The strength $\kappa_B$ was to be locked where three<!-- N:DX-301 --> bands set before calibration intersect. They were a masked share of the crop at Medium in [0.15, 0.45]<!-- N:DX-301 -->, a probability in [0.4, 0.7]<!-- N:DX-301 --> that a Burning cell three<!-- N:DX-301 --> cells away is revealed at Medium, and the corridor toy's $q$ (Theorem 1) in [0.3, 0.7]<!-- N:DX-301 -->. They do not intersect. The masked-share band cannot be reached at Medium: the masked share can only approach the share of crop cells with smoke on their line of sight, 0.130<!-- N:DX-12 --> there under a random policy, below the band's lower edge of 0.150<!-- N:DX-12 -->. The same $\kappa_B$ attenuates the arena's extended smoke more strongly than the toy's single smoke source, which leaves the detection and toy bands disjoint by a factor of 1.35 under a random policy and 1.15 under probe policies<!-- N:CB-2 -->. $\kappa_B = 1.0$<!-- N:CB-1 --> was therefore locked on the detection band alone; the masked-share band was retired, not widened, and the toy band was kept as a consistency check.

The one ablation of the death penalty $d_p$ ran the fire alone with no coupling, for 500<!-- N:ENV-2 --> updates with 3<!-- N:ENV-2 --> seeds per setting, on an older observation encoding; it reports training-log means over the final updates and was not re-run. Raising $d_p$ from 0<!-- N:ENV-2 --> to 0.5<!-- N:ENV-1 --> moved survival at High severity from 0.575 to 0.866<!-- N:ENV-2 --> and completion there from 0.765 to 0.821<!-- N:ENV-3 -->. Survival at Medium moved from 0.931 to 0.951<!-- N:ENV-4 -->, and Low stayed tied, 0.991 against 0.992<!-- N:ENV-5 -->.

No gradient crosses the communication channel, so the message head, a tanh-bounded dense layer on the shared trunk, stays at its initialization<!-- N:ENV-12 -->: an agent emits a fixed random projection of trunk features that are themselves trained. The receivers' weights on the message inputs are trained, which makes message use testable; what to say was never learned.

<!-- LISTING 6: block carried byte-for-byte from paper/v2/sections/07_comms.md:39; move it, never edit it -->

**Listing 6.** Delivered messages carry no gradient, so the message encoder stays at its initialization.

<!-- LISTING: che/train/ippo.py:323-329 -->
```python
# che/train/ippo.py:323-329 (verbatim)
        # Messages emitted this step are delivered next step. Nothing crosses
        # an episode boundary (autoreset), and stop_gradient states in code
        # what the batch-storage already implies: the channel is not a
        # differentiable path (Q3 ruling; networks.py docstring).
        messages = jax.lax.stop_gradient(
            jnp.where(done[:, None, None], 0.0, emitted)
        )
```
