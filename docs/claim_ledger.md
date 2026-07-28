# Claim ledger — validation status of every formal claim

**Pinned to:** `main` @ `0c612b6e8e19c1372592375f097af9a01197cf62` (2026-07-28).
**Source of claims:** `docs/theory_foundations.md` v0.1.
**Purpose:** two jobs at once. (1) An engineering register: nothing in the
theory doc gets asserted in the paper without a named test, a scheduled phase,
a literature reference, or an explicit hedge. (2) **A paper appendix asset** —
"validation status of every formal claim" — which is a stronger honesty signal
to RA-L/IROS reviewers than a methods paragraph, and cheap because the column
already exists in the repo.

## Classification

| code | meaning |
|---|---|
| **(a)** | **Validated by an executable test.** The test is named. It runs in CI-equivalent form (`pytest che/tests`). |
| **(b)** | **Scheduled for validation.** The phase and milestone are named. Not yet evidence. |
| **(c)** | **Cited literature.** A standard result we invoke. The reference is named — or flagged as *missing from the bibliography*. |
| **(d)** | **Motivational / untested.** True-by-construction, argued in prose, or simply not yet touched. **Every (d) the paper would state needs a hook or an explicit hedge** — the "action" column says which. |

**Test-suite state at the pinned commit:** 123 fast tests **PASS** (`pytest -m
"not slow"`, exit 0, ~2.5 min CPU). 12 `@slow` theory tests — outcomes in the
(a) rows below.

**Why every theory-doc correction here is a diff and not an edit:**
`docs/theory_foundations.md` is **human-owned** — `phase1_2_prompt.md:212`
lists "any edit to `docs/theory_foundations.md` (human-owned)" as a standing
non-goal, and Phases 3 and 4 repeat it. The one amendment made under that rule
(the post-M3.3 finite-protocol remark, and later Remark 2′/2″) was
human-authored. This ledger proposes; it does not amend.

**Reading the doc's own tags:** `theory_foundations.md` self-tags claims
`[PROVEN]` / `[CITED]` / `[EMPIRICAL]`. Those tags describe *mathematical*
status. This ledger describes *implementation-validation* status. A `[PROVEN]`
claim can be ledger-(d) — proved on paper, never checked against the code —
and several are.

---

## §1 — Environment as a factored augmented Dec-POMDP

| # | Claim | Doc tag | Ledger | Evidence / action |
|---|---|---|---|---|
| 1.1 | **Def. 1** — state factorizes as `S = X × H × C × K`; kernel factorizes as `T_C · T_H · T_K · T_X` | — | **(d) — DEFECT** | See **L-1** below. The factorization omits ρ (smoke), which D3 locked as a state component. Must be corrected before the paper states Def. 1. |
| 1.2 | **Def. 2(1)** — reward-independence: `R(s,a) = R(task(x), a)`, no term reads h, ρ or c | — | **(a)** | `test_reward_independence.py::test_reward_identical_across_hazard_smoke_structure` and `::test_reward_identical_with_death_penalty`. Far-field construction (Chebyshev margin ≥ 6) makes the α-transition provably identical across variants. CLAUDE.md invariant #1. |
| 1.3 | **Def. 2(2)** — non-adversarial: `T_H` is a fixed kernel with no optimizing component | — | **(d) by construction** | Not falsifiable by a test (it is the absence of a thing). Verified by inspection: `che/env/hazard.py` takes no policy, no value, no learned parameter. **No hedge needed**; state as a design property, not a result. |
| 1.4 | **Def. 2(2) subtlety** — the env is non-adversarial but *not agent-independent* (agents trigger collapse via `T_C`, hence fire via Coupling A) | — | **(a)** | `test_structure_weak.py::test_load_term_fires_only_under_occupancy`; realized at scale in M3.5 (`blocked_moves`, `weak_occupancy` channels). The doc already prescribes "one honest sentence in the paper" — **keep that sentence**. |
| 1.5 | **Prop. 1** — the process is Markov; `M_θ` is a well-posed finite Dec-POMDP | [PROVEN] | **(a) indirect** | No single test asserts the whole ordering. Four tests pin it edge-by-edge: ρ' reads h' (`test_hazard::test_smoke_reads_post_update_burning`); h' reads the collapse increment (`test_coupling_a::test_env_step_seeds_iff_new_collapse`); x' reads c' (`test_lethality::test_collapse_under_agent_kills_no_escape`); x' reads h' (`test_lethality::test_step_ignition_under_stationary_agent_kills_and_penalizes`). **Action: cheap win — add one order test** that mutates each stage and asserts the downstream stage sees it. |
| 1.6 | **Remark 1** — finite-horizon Dec-POMDPs are NEXP-complete | [CITED] | **(c)** | Bernstein, Givan, Immerman, Zilberstein (2002) — present in the bibliography. |
| 1.7 | With δ > 0 the CHE does not collapse to an MPOMDP | [CITED] | **(d)** | Asserted, not argued and not tested. It is true for δ = 1 (no messages ⇒ no shared observation) but is stated for all δ > 0. **Action: hedge** to "for δ > 0 the CHE is not an MPOMDP, since joint observability fails whenever a link drops", or drop the clause — the hardness framing survives on δ = 1 alone. |

**L-1 — Def. 1 omits the smoke field ρ from the state space.** The doc's
`S = X × H × C × K` has no ρ factor, and the displayed transition kernel has no
ρ term, yet:

- **D3 is locked** (`decision_log.md:18`): "Smoke field ρ with emission σ_s and
  decay η is a state component (Def. 6); smoke persists after flame passes."
- **CLAUDE.md invariant #2** gives the step order as
  `c' → h' → ρ' = e^{−η}ρ + σ_s·1[burning] → x' → k'`, with observations drawn
  from `O_{κ_B}(·|x', h', ρ', c', k')`.
- **`che/env/types.py:51`** carries `smoke: jax.Array` in `EnvState`.
- **Def. 6** then uses `ρ_H` as if it had been introduced.

So the implementation, the locked design decision and the project's own
invariant all treat ρ as state; only Definition 1 does not. This matters
because Def. 1 is a paper asset and because Prop. 1's Markov-closure argument
is *about* the completeness of the state factorization — an argument that is
incomplete if a genuine state component is missing from it.

Two further Def. 1 defects, smaller:

- The displayed product writes `T_K^δ(k'|x')` **before** `T_X(x'|x,a,h,c)`,
  which reads as sampling `k'` from an `x'` that does not exist yet. The proof
  text immediately below gives the correct order; the formula does not.
- The observation kernel is written `O^i_{κ_B}(o_i | x, h, c, k)` — no ρ —
  while Coupling B attenuates on ρ, not h. Def. 6 uses `ρ_H`. The two
  definitions disagree about what the observation kernel reads.

**Proposed correction (for human review; not applied):**

```diff
--- a/docs/theory_foundations.md
+++ b/docs/theory_foundations.md
@@ Definition 1
-$$\mathcal{S} = \mathcal{X} \times \mathcal{H} \times \mathcal{C} \times \mathcal{K}$$
+$$\mathcal{S} = \mathcal{X} \times \mathcal{H} \times \mathcal{P} \times \mathcal{C} \times \mathcal{K}$$
@@
-- $\mathcal{H} = \Sigma_H^{G}$: hazard field; per-cell hazard state
+- $\mathcal{H} = \Sigma_H^{G}$: hazard field; per-cell hazard state
   $\Sigma_H = \{\mathrm{Fuel}, \mathrm{Burning}, \mathrm{Burnt}\}$ ...
+- $\mathcal{P} = \mathbb{R}_{\ge 0}^{G}$: smoke density field $\rho$ (Def. 6).
+  Smoke outlives flame (**D3**), so $\rho$ is a state component and not a
+  function of $h$ — this is what makes Coupling B depend on history rather
+  than on the instantaneous fire.
@@
-$$T_\theta(s' \mid s, a) \;=\; \underbrace{T_C(c' \mid c, x)}_{\text{structure}} \;\cdot\; \underbrace{T_H^{\beta,\kappa_A}(h' \mid h, c, c')}_{\text{hazard (Coupling A enters here)}} \;\cdot\; \underbrace{T_K^{\delta}(k' \mid x')}_{\text{comms}} \;\cdot\; \underbrace{T_X(x' \mid x, a, h, c)}_{\text{agents}}$$
+$$T_\theta(s' \mid s, a) \;=\; \underbrace{T_C(c' \mid c, x)}_{\text{structure}} \cdot \underbrace{T_H^{\beta,\kappa_A}(h' \mid h, c, c')}_{\text{hazard (Coupling A)}} \cdot \underbrace{T_P(\rho' \mid \rho, h')}_{\text{smoke}} \cdot \underbrace{T_X(x' \mid x, a, h', c')}_{\text{agents}} \cdot \underbrace{T_K^{\delta}(k' \mid x')}_{\text{comms}}$$
+
+written left to right in sampling order (this *is* the implemented order —
+CLAUDE.md invariant #2, `che/env/env.py`).
@@
-$O_\theta^i(o_i \mid s) = O^i_{\kappa_B}(o_i \mid x, h, c, k)$, where the
+$O_\theta^i(o_i \mid s) = O^i_{\kappa_B}(o_i \mid x', h', \rho', c', k')$, where the
 **dependence of the observation kernel on $h$ is Coupling B** (Section 5).
```

---

## §2 — Hazard kernel and phase structure

| # | Claim | Doc tag | Ledger | Evidence / action |
|---|---|---|---|---|
| 2.1 | **Def. 3** — constant-burn-time fire CA; Burnt absorbing; spontaneous rate ι | — | **(a)** | `test_hazard.py`: `test_absorbing_burnt_and_one_step_burn`, `test_beta_zero_never_spreads_beta_one_is_plus_shape`, `test_spontaneous_ignition_iota_one`, `test_seed_ignitions_only_fuel`, `test_same_key_bitwise_identical`, `test_shapes_and_dtypes_preserved`. |
| 2.2 | **Prop. 2** — eventually-Burnt set ≡ open cluster of bond percolation at β | [PROVEN/CITED] | **(a) indirect + (c)** | Grassberger (1983) in the bibliography. The proof's load-bearing step ("each edge is attempted at most once") is realized by the per-cell-per-direction sampling scheme, argued in prose at `che/env/hazard.py:8–16`, **not** by a test. Empirical consequence *is* tested: β̂_c = 0.500 (2.4). **Action: consider a direct test** — instrument the kernel to count per-edge attempts on a small grid and assert ≤ 1. Cheap; closes the only gap in the doc's proudest self-contained proof. |
| 2.3 | **Cor. 1(1)** — β_c = 1/2 exactly on Z² von Neumann | [CITED] | **(c)** | Kesten (1980) — in the bibliography. |
| 2.4 | The **implemented** kernel reproduces β_c = 1/2 | — | **(a)** | `test_percolation.py::test_beta_c_in_band` (band [0.42, 0.58], `@slow`); measured β̂_c = 0.500 ± 0.005 (`severity_lock.md`). **Caveat: see citation audit C-9** — the pivot estimator behind "0.500" is not committed; the committed consensus is 0.4991 and the committed crossings mean is 0.5045. The *test* is unaffected (any of these passes the band). |
| 2.5 | **Cor. 1(2)** — subcritical: finite cluster, finite χ, exponential tails, finite ξ | [CITED] | **(c) + (a) partial** | Finiteness at β = 0.43 measured: P_span = 0.021, burnt fraction 1.9% (`severity_lock.md`); χ̂(β) curve in `estimates.npz`. Exponential tails and ξ are **not measured**. |
| 2.6 | **Cor. 1(3)** — γ_p = 43/18, ν_p = 4/3 (2D percolation universality) | [CITED] | **(c) — REFERENCE MISSING** + **(d) for our kernel** | **No bibliography entry** for the exponents (the standard refs are den Nijs 1979 / Nienhuis 1982). And explicitly *not* reproduced here: `severity_lock.md:22` — "χ̂(β) rises ~17× … effective exponent ≈ 1.6 in the accessible window; **asymptotic γ = 43/18 not reachable at L = 64 — reported honestly, not claimed**." **Action: (i) add the reference; (ii) the paper must carry the L = 64 hedge wherever 43/18 appears.** See also 4.4. |
| 2.7 | **Cor. 1(4)** — supercritical: linear growth, front speed v(β) > 0, limiting shape | [CITED] | **(a) for v; (d) for the shape theorem** | v̂ measured monotone increasing 0.36 → 0.99 cells/step (`calibration_report.md`); `test_percolation.py::test_front_speed_increasing_top_betas`; v̂ = 0.83 at the locked High β = 0.70. The **shape theorem** is invoked with **no reference and no measurement**. **Action: drop the shape clause or cite it** — nothing downstream depends on it. |
| 2.8 | Caveat: exact β_c is specific to the idealized kernel; only the *existence* of the transition is universal, and that is all the design relies on | — | **(a)** | Honest and correct as written; the measured-not-assumed protocol is implemented (§3). Keep verbatim. |

---

## §3 — Severity by dynamical phase

| # | Claim | Doc tag | Ledger | Evidence / action |
|---|---|---|---|---|
| 3.1 | **Def. 4** — three severities are three dynamical phases (sub / near / super-critical) | — | **(a)** | `severity_lock.md` (human-locked 2026-07-19): Low β = 0.43 (P_span 0.021, bf 1.9%), Medium β = 0.49 (P_span 0.547, bf 19.8%), High β = 0.70 (v̂ 0.83, bf 98.3%). Written into `che/configs/severity_{low,medium,high}.yaml` with npz hashes. |
| 3.2 | Def. 4 rationale — three phases beat three knob settings (principled level choice; a-priori capability prediction; severity transfer = generalization across phases) | — | **(d)** | Rhetorical, and a *good* argument. No hedge needed for (i) and (iii). **(ii) "predicts a priori which regime stresses which capability" is the part that got tested — and partly failed: see 3.3.** |
| 3.3 | **Def. 4's Medium prediction** — "fluctuations are maximal… this is the regime where memorization is most punished, and we should expect the paper's most interesting behavior here" | — | **(a) — PARTLY REFUTED** | **The single most important row in this ledger.** `def4_variance.md` (M3.0, registered in advance, 512 eval episodes × 3 severities × 3 seeds at fixed policy): **survival_rate REFUTED** — per-episode variance is *monotone* in severity (high 0.00885 > medium 0.00709 > low 0.00091), High highest, not Medium. **completion NOT CONFIRMED** — Medium 0.01245 vs Low 0.01235, inside bootstrap CIs. **Environment-level mechanism CONFIRMED** — burnt-fraction variance peaks near criticality (max at β = 0.53; medium 0.0354 ≫ high 0.0019 > low 0.0008). Decomposition on record: outcome variance ≈ env variance × policy sensitivity, and the two factors peak in different regimes. **Action — MANDATORY: the theory doc still states the prediction with no amendment banner**, unlike Remark 2 which got one. See **L-2**. |
| 3.4 | Calibration protocol (sweep β, estimate β̂_c from steepest P_span, fix severities by observables) | [EMPIRICAL] | **(a)** | Executed M2.1–M2.4. One documented spec correction: pairwise crossings of centre-seed P_span do not exist (one-sided finite-size bias), replaced by the left–right crossing probability R_L — `calibration_report.md:42–57`, human-approved 2026-07-19. The provisional bands in the doc (Low bf ∈ [1,5]%, Medium P_span ∈ [0.3,0.7], High v̂ ∈ [0.5,1]) were all **satisfied**. |
| 3.5 | "Theory as unit test" — a kernel that fails the sigmoid is mis-ported | — | **(a)** | `test_percolation.py` (3 `@slow` tests). **But see L-3: "mis-ported" is a false provenance claim.** |

**L-2 — Def. 4's Medium-fluctuation prediction was tested and did not survive
at the task level; the theory doc does not say so.** The doc reads: *"This is
the regime where memorization is most punished, and we should expect the
paper's most interesting behavior here."* The repo's own registered re-test
returned REFUTED (survival) / NOT CONFIRMED (completion).

The prediction is not *worthless* — the environment-level mechanism confirmed
cleanly, and the decomposition explaining the gap is a genuine result. But
a reader of the theory doc alone would carry an expectation the data has
already denied, and Phase 6/7 seed budgets are being set partly on it
(`def4_variance.md:110` already routes the opposite conclusion into Phase 6:
*High*-severity cells need more seeds).

Precedent for the fix exists in the same document: Remark 2 got a dated
"superseded in part" banner the moment its denied baseline was found wrong.
Def. 4 deserves the same treatment.

**Proposed correction (for human review; not applied):**

```diff
--- a/docs/theory_foundations.md
+++ b/docs/theory_foundations.md
@@ Definition 4, Medium bullet
 - **Medium** — near-critical: $\xi(\beta) \sim L$. Cluster sizes are
   (finite-size) scale-free; fluctuations are maximal; a single ignition can, with
   non-negligible probability, cascade to arena scale. Survival is a *global
-  anticipation* problem with maximal unpredictability. This is the regime where
-  memorization is most punished, and we should expect the paper's most
-  interesting behavior here.
+  anticipation* problem with maximal unpredictability.
+
+> **Measured 2026-07-20 (M3.0), and the task-level half did not survive.**
+> The original text predicted maximal *outcome* variance at Medium. At fixed
+> policy (512 eval episodes × 3 seeds per severity,
+> `che/bench/results/phase3/def4_variance.md`): per-episode **survival**
+> variance is **monotone in severity** (High highest) — REFUTED; **completion**
+> variance shows no resolvable Medium peak (Medium 0.01245 vs Low 0.01235,
+> CIs overlap) — NOT CONFIRMED. The **environment-level** mechanism is
+> CONFIRMED: burnt-fraction variance peaks near criticality (β ≈ 0.53).
+> Decomposition: outcome variance ≈ (environment variance) × (policy
+> sensitivity); the environment factor peaks at Medium but policy sensitivity
+> grows with severity, so the product need not peak at Medium. The phase
+> characterization of Medium stands; the claim about where the *interesting
+> behavior* lands does not, and the paper must not make it.
```

**L-3 — "the ported PyTorchFire/JaxWildfire kernel" is a false provenance
claim.** `theory_foundations.md:215–216` and `:556–558` describe the CA as a
*port* of PyTorchFire / JaxWildfire, and §10 says "A kernel that fails this is
mis-ported."

The kernel was not ported. `phase0_substrate_prompt.md:41` instructs:
*"Implement `che/env/hazard.py` per Def. 3 and Def. 6 of the theory doc"*, and
`che/env/hazard.py` contains no attribution to either project. Neither name
appears anywhere else in the repo, in the bibliography, or in
`pyproject.toml`'s dependencies.

The phrasing has already propagated: `che/tests/test_percolation.py:7` and
`:58` say "mis-ported", as does `phase1_2_prompt.md:170`. In a submission, an
uncorrected provenance claim of this kind is a serious problem — it credits
code that was not used and implies a validation lineage that does not exist.

**Proposed correction (for human review; not applied):**

```diff
-This doubles as the **correctness test of the CA port**: if the ported
-PyTorchFire/JaxWildfire kernel does not exhibit a clean sigmoid in
-$P_{\mathrm{span}}$, the port is wrong. Theory as unit test.
+This doubles as the **correctness test of the CA implementation**: if the
+kernel (implemented directly from Def. 3, not ported from an existing
+wildfire simulator) does not exhibit a clean sigmoid in
+$P_{\mathrm{span}}$, the implementation is wrong. Theory as unit test.
@@ §10
-- **Phase 2 unit test:** ported CA kernel must reproduce a sigmoidal
+- **Phase 2 unit test:** the CA kernel must reproduce a sigmoidal
   $P_{\mathrm{span}}(\beta)$ with finite-size sharpening; severity bands
-  calibrated per Section 3. A kernel that fails this is mis-ported.
+  calibrated per Section 3. A kernel that fails this is mis-implemented.
```

(Docstring wording in `che/tests/test_percolation.py` and
`phase1_2_prompt.md` should follow; both are outside this audit's write scope.)

---

## §4 — Coupling A

| # | Claim | Doc tag | Ledger | Evidence / action |
|---|---|---|---|---|
| 4.1 | **Def. 5** — collapse seeds each Fuel cell in `N_A(g)` w.p. κ_A; collapsed absorbing | — | **(a)** | `test_coupling_a.py`: `test_seed_mask_iff_new_collapse_within_radius`, `test_env_step_seeds_iff_new_collapse`, `test_seeded_fire_smokes_and_kills_like_primary`, `test_seeded_fire_spreads_like_primary`. Locked params `(f_weak, λ₀, λ_load, κ_A, r_A) = (0.15, 5e-5, 4e-4, 0.06, 1)` — `coupling_a_lock.md`, human 2026-07-21. |
| 4.2 | κ_A = 0 recovers the uncoupled system as a **nested model** (and likewise κ_B = 0, δ = 0) | — | **(a) for κ_A, κ_B; (b) for δ** | `test_nesting.py::test_kappa_a_immaterial_without_collapses`, `::test_zeroed_branches_still_consume_prng_structurally`; `test_structure_weak::test_lambda_zero_bitwise_recovers_structure_off_trajectories`; `test_coupling_b::test_kappa_b_zero_bitwise_recovers_obs_v2`, `::test_reveal_draw_present_at_kappa_b_zero`. **δ is not implemented** — `che/env/comms.py` does not exist; nesting tests are specified at M5.0. |
| 4.3 | **Prop. 3** — `E[B_T] = λ_A·T·χ(β)(1+o(1))` in the sparse regime; `≤` in general | [PROVEN, approx.] | **(a)** | `test_prop3.py::test_prop3_slope_matches_matched_reference` (`@slow`), **GREEN**: slope 41.18 vs matched_ref 41.49 → ratio **0.992 ∈ [0.90, 1.02]** (human-locked band), R² **0.9995 ≥ 0.99**. Regime purity asserted separately (`::test_purified_regime`, overlap proxy 0.016–0.023 ≤ 0.03). GPU-scale L = 64 sweep: slope 45.56, R² 0.9979. Supporting: `::test_collapse_is_the_only_birth_channel`, `::test_seeding_scales_with_lambda`. |
| 4.4 | **Prop. 3 corollary** — marginal exposure `∂E[B_T]/∂λ_A = Tχ(β)` **diverges** as β ↑ β_c like `|β−β_c|^{−43/18}` | [PROVEN] | **(d) — NOT MEASURED** | The Prop.-3 sweep runs at a **single** β (0.43, locked Low). The repo contains **no measurement of the slope's β-dependence**, and per 2.6 the 43/18 exponent is explicitly unreachable at L = 64 (measured effective exponent ≈ 1.6 over the accessible window). The *χ̂(β) curve itself* is measured and does rise ~17× — that is the honest supporting evidence. **Action — MANDATORY HEDGE:** the paper may say "expected burnt area per collapse scales with the mean cluster size χ(β), which we measure rising ~17× from β = 0.30 toward criticality"; it may **not** quote 43/18 as a property of this kernel. **Optional hook (cheap):** re-run the Prop.-3 sweep at 3–4 β values below β_c and report the measured slope-vs-χ̂(β) relation — turns (d) into (a) for a few CPU-hours. |
| 4.5 | Interpretation — "structural failure is the hazard's only birth channel in calm conditions"; incentive to avoid structural risk ∝ χ(β) | — | **(a) for the first half; (d) for the second** | Birth-channel claim: `test_prop3::test_collapse_is_the_only_birth_channel` (ι = 0, no primary ignition ⇒ zero seeds ⇒ zero burnt). The *behavioural* claim ("the policy's incentive … is proportional to χ") was tested at M3.5 and **found absent**: weak-cell occupancy under κ_A = 0.06 is **equal or higher** than the control at Low (+0.054) and Medium (+0.031) — no avoidance shift. `phase3_report.md`, Question (a). **Action: hedge** — the incentive exists in the model; the trained swarm at dp = 0.5 does not act on it. Say so; it is an interesting negative. |
| 4.6 | **Remark (finite-protocol corrections, post-M3.3, human-authored)** — four named factors, all downward, composing to the observed slope with an L-independent residual; linear structure exact (R² = 0.998) | — | **(a)** | Each factor measured: `m33/deficit_decomposition.json`; waterfall 62.85 ×1.121 ×0.834 ×0.928 ×0.836 = 45.56 (`phase3_report.md`). L-independence of the residual: 0.843 (L = 32) vs 0.836 (L = 64). R² = 0.9979 ≈ 0.998 ✓. Exemplary — this is what a (d)→(a) conversion looks like. |
| 4.7 | Low-severity fuel-exhaustion self-limitation of the ignition channel (High seeding ~5.7× below Low at every κ_A) | — | **(a)** | `coupling_a_lock.md` (random policy, κ-independent ratio) and confirmed under **trained** policies at M3.5 (realized seeding 0.83/ep at High vs 4.08 at Low). Recurs at M4.4 Result 4. Paper sentence already drafted in `coupling_a_lock.md:87–91`. Not in the theory doc — **worth adding** as the empirical mirror of 4.4. |

---

## §5 — Coupling B and Theorem 1

| # | Claim | Doc tag | Ledger | Evidence / action |
|---|---|---|---|---|
| 5.1 | **Def. 6** — Beer–Lambert transmittance `τ = exp(−κ_B ∫ρ dℓ)`; feature observed w.p. τ | — | **(a)** | `test_coupling_b.py`: `test_transmittance_exact_on_uniform_smoke` (closed form), `test_transmittance_monotone_in_distance_smoke_and_kappa`, `test_masking_respects_visibility_plane_exactly`, `test_masked_frac_info_channel`, `test_kappa_b_cannot_perturb_state_trajectories`. Locked κ_B = 1.0 (`kappa_b_lock.md`, human 2026-07-27). |
| 5.2 | "Beer–Lambert is the standard optics model for smoke/turbidity, so Coupling B is *physically grounded*" | — | **(c) — REFERENCE MISSING** | No bibliography entry. The claim is uncontroversial but the doc explicitly proposes to make it "worth a sentence in the paper" — a physical-grounding sentence needs a citation. **Action: add one.** |
| 5.3 | **Implementation caveat** — 4-point midpoint quadrature under-resolves isolated single-cell sources beyond axis distance ≈ 4 | — | **(a)** | `test_coupling_b::test_isolated_smoke_cell_is_unoccluded_beyond_quadrature_range`; ruled a documented kernel property (M4.2 ruling item 2). Detection band confirmed in the well-sampled regime: `endpoint_sampled_fraction = 1.0` at distance 3, pinned by `test_coupling_b_calib::test_detection_ring_is_in_the_quadrature_sampled_regime`. **Not in the theory doc.** Limitations sentence already drafted (`phase4_report.md:163–168`). **Action: the paper must carry it** — it bounds occlusion from below. |
| 5.4 | **Thm. 1(1)** — `J*(κ_B) = ½ + q(κ_B)/2` | [PROVEN] | **(a)** | `test_e2c.py::test_empirical_matches_numeric_prediction` (`@slow`), **GREEN** under the human's final three-condition gate (2026-07-27): max\|z\| = **2.11** ≤ 2.69 (Šidák); Σz² = **6.55** on 8 dof, p = **0.586** ≥ 0.05; mean z = **−0.44**, within 0.71. Three independent routes to q agree (`::test_q_estimators_agree`), including through the full `observe` pipeline. |
| 5.5 | **Thm. 1(2)** — the memorizing policy is worth ½ for every κ_B; gap = q/2 | [PROVEN] | **(a)** | `test_e2c.py::test_memorizing_policy_flat_at_half`. Max deviation 0.0084 at κ_B = 5 against 2·SE = 0.0110; no trend in κ_B. |
| 5.6 | **Thm. 1(3)** — q continuous, strictly decreasing; gap → ½ as κ_B → 0, → 0 as κ_B → ∞ | [PROVEN] | **(a)** | `test_e2c.py::test_j_star_at_zero_and_large_kappa`: J*(0) = **1.0000** ≥ 0.99; J*(8) − ½ = **0.0000** ≤ 0.02. |
| 5.7 | Thm. 1's closed form `q = 1 − ∏(1−e^{−κ_B j})` | [PROVEN] | **(a) as an idealization** | The validated object is the **numeric** q computed through the shared `transmittance` against the real smoke trajectory; the closed form is the unit-density approximation. They agree to ≤ 0.008 across the grid (`phase4_report.md` result table, "q (MC)" vs "q (analytic)"). **Action: state in the paper which one the figure plots** — the numeric one. |
| 5.8 | **Thm. 1's idealization** that occlusion is pure information loss | — | **(a) — FALSIFIED as an implementation statement** | M4.2 Finding 2: smoke co-locates with fire, so the mirror corridor's ray is always clear and "exactly one candidate masked" identifies Z from the **visibility plane alone**. Measured plane-7-only oracle accuracy: 0.508 (κ_B = 0) → 0.857, 0.966, 0.989, 0.998, **≥ 0.9999 from κ_B = 3**. Handled correctly: scored policies are content-only, enforced end-to-end by `::test_scored_policies_never_read_the_visibility_plane` and `::test_corridors_are_exchangeable`; prediction and rollout use independent PRNG streams. **Action — MANDATORY FOOTNOTE**, already drafted (`phase4_report.md:190–196`). The theory doc carries no note of this at all. |
| 5.9 | Key structural property — perception quality is a function of the hazard's own state, so degradation concentrates where/when the hazard is active | — | **(a)** | Quantified at swarm scale, M4.4 Result 2: masking at danger moments vs unconditional — Low **118×**, Medium **22×**, High **16×**. This is the doc's qualitative claim turned into a number, and it is one of the paper's better ones. |
| 5.10 | **Remark 2** — VoC(κ_B) = ½(1−q), increasing in κ_B | [PROVEN, remark] | **(b) — SUPERSEDED IN PART** | Banner present and dated (2026-07-28). Denied-arm baseline was an **RA theory error**: with two interchangeable agents and a team-any reward, role splitting achieves 1 without any message. Scheduled: **M5.2**. |
| 5.11 | **Remark 2′(i)** — under team-any reward, comms has zero marginal value when agents are interchangeable, expendable and ≥ the hypothesis count | [PROVEN, remark] | **(b)** | Scheduled M5.2 as the "any-agent coverage" third curve (flat at ~1 under total denial), per Q1 ruling. |
| 5.12 | **Remark 2′(i) generalization** — "VoC under team-any reward **scales with the hypothesis-count-minus-agent-count deficit**, and death costs price the redundancy that substitution spends" | [PROVEN, remark] | **(d)** | Stated as a general law with **no proof and no test**. The 3-corridors/2-agents intuition behind it is sound; the scaling claim is not established. `dp = 0.5` pricing redundancy is plausible but unmeasured. **Action: hedge to a conjecture**, or restrict the sentence to the concrete case that *is* argued (deficit > 0 ⇒ VoC > 0). |
| 5.13 | **Remark 2′(ii)** — courier variant: denied optimum within the no-idle class is ½ + q/2; with slack, `VoC_true = ½(1−q̃)` with `q̃ ≥ q`, equality iff ℓ_f = 0 | [PROVEN, remark] | **(b)** | Scheduled M5.2: the fourth scripted "denied + dawdle" curve with its own MC prediction over the d + ℓ_f window (round-2 ruling item 1, ~1 CPU-hour authorized). The acceptance gate stays on the pinned-schedule curve; VoC reported both ways. Good design — the residual is being *measured*, not reasoned around. |
| 5.14 | "Numerically at Option-A geometry, `q̃/q → 5/3` as κ_B → ∞" | — | **(d)** | A bare numeric assertion with **no artifact behind it**. Its derivation lives in `decision_log.md:437–441` and is a **draw-counting** argument (3 pre-commitment draws vs 5 with two idle draws at branch distance 2.00), i.e. the small-τ limit where q ≈ Στ. That approximation treats all draws as equal-τ, which the actual optical depths (distances 2.83 / 2.24 / 2.00 against ρ = 1.000 / 1.607 / 1.974) do not satisfy. **Action: hedge to "≈ 5/3 by draw counting" until M5.2 measures it**, then replace with the measured ratio. |
| 5.15 | Corrected lesson — "communication is load-bearing exactly when perception fails **and redundancy is unavailable**" | [PROVEN, remark] | **(b)** | The sharpened claim. M5.2 measures all four curves; M5.3's utility gate and M5.5's falsifier test it at swarm scale. |

---

## §6 — Comms axis

| # | Claim | Doc tag | Ledger | Evidence / action |
|---|---|---|---|---|
| 6.1 | **Def. 7** — link alive w.p. `p_link(‖x_i−x_j‖)·(1−δ)` | — | **(b)** | **Not implemented.** `che/env/comms.py` does not exist at the pinned commit (it *is* listed in `CLAUDE.md`'s layout block — citation audit C-8). M5.0. Note the M5.0 spec has already changed the kernel to a **hard range** `1[d ≤ R_comm]·(1−δ)` with `p_link_max` retired (Q6 ruling) — **the theory doc's `p_link(d)` form is now more general than what will be built.** |
| 6.2 | `T_K` does **not** depend on h — comms denial is mechanistically independent of the hazard | — | **(b)** | M5.0 nesting tests: "δ cannot perturb any env kernel stream". Design commitment restated in `phase5_prompt.md:14–17`. |
| 6.3 | δ = 0 recovers free (range-limited) comms as a nested model | — | **(b)** | M5.0, per invariant #3 (unconditional draw of one uniform per ordered pair per step). |
| 6.4 | Hazard-coupled comms (smoke attenuating radio, collapse severing relays) is deliberately future work | — | **(d) by design** | Correct as a scoping statement. Keep. |

---

## §7 — Compositional generalization

| # | Claim | Doc tag | Ledger | Evidence / action |
|---|---|---|---|---|
| 7.1 | **Def. 8** — Θ_iso, ISO and JOINT protocols, compositional gap Γ | — | **(b)** | Phase 6–7. D1 and D2 are locked (`decision_log.md`), so the protocols are pinned. |
| 7.2 | **The hypothesis Γ(θ*) > 0, primary metric task completion rate** | [EMPIRICAL] | **(b)** + **citation defect** | Phase 7 is its job — correctly self-tagged. **But "the locked hypothesis" has no written source in the repo** (citation audit C-4): not in `decision_log.md` (D1–D5 only), not in either phase prompt. The *primary metric* is the sharp end: M4.4 found Coupling B costs **survival** (−8.8 pt at High) while leaving **completion** intact. If completion alone is the locked primary metric, Phase 7 could report Γ ≈ 0 on a metric the couplings demonstrably do not move. **Action: transcribe D0 and re-examine the metric choice before Phase 6 designs the grid.** |
| 7.3 | **Prop. 4** — simulation-lemma value bound; ε(θ,θ*) ≥ ε_min > 0 uniformly over Θ_iso, so ISO's guarantee carries irreducible slack | [PROVEN, bound] | **(d)** + **(c) reference missing** | The simulation lemma is standard but **has no bibliography entry** (usual ref: Kearns & Singh 2002). ε_min > 0 is argued in prose, never quantified. Not directly testable — it bounds a *guarantee*, not a behaviour. **Action: add the reference. No further hedge needed** — 7.4 already does the work. |
| 7.4 | **Honesty note** — Prop. 4 bounds what can be guaranteed, not what happens; upper bounds on ISO transfer do not lower-bound Γ; compositional generalization can emerge from isolated training; the experiment decides | — | **(d) by design** | This is the model for how every other (d) in this ledger should read. **Keep verbatim in the paper.** |
| 7.5 | **Measurement corollary** — log coupling-co-active visitation | — | **(a)** | Live from day one (CLAUDE.md invariant #5): `test_env::test_coupling_co_active_counter_plumbing`, `test_coupling_a::test_coactive_counter_hand_built_scenario`. **First real data at M4.4** (Result 4): distribution is **zero-inflated and over-dispersed** — 56–88% of episodes contain no co-active event, tail reaches 9 — so the mean alone would have misled. Severity ordering **inverted** (Low 0.69 > Medium 0.56 ≫ High 0.16), which is 4.7's fuel exhaustion recurring. |
| 7.6 | **Prediction from Prop. 4's mechanism** — ISO policies have near-zero training exposure to the co-active region and elevated failure rates *inside* it; JOINT failures more uniform | — | **(b)** | Phase 7. The counter and its per-episode distribution are ready; the *conditional failure rate inside the region* is the piece still to build. **Action: confirm the eval harness can emit failures conditioned on co-active count before Phase 7 starts** — this is exactly the M4.0 lesson (retrofit metrics before the phase that needs them). |

---

## §8 — Nested-model ablation semantics

| # | Claim | Doc tag | Ledger | Evidence / action |
|---|---|---|---|---|
| 8.1 | β off recovers static/no-hazard (Phase 1 control) | — | **(a)** | `test_frozen.py` (5 tests); `test_nesting::test_dynamic_frozen_diverge_only_through_freeze`. |
| 8.2 | κ_A off recovers hazard blind to structure | — | **(a)** | See 4.2. |
| 8.3 | κ_B off recovers hazard-independent perception | — | **(a)** | `test_coupling_b::test_kappa_b_zero_bitwise_recovers_obs_v2` — obs v3 at κ_B = 0 is bitwise obs v2 content plus an all-ones visibility plane. Confirmed at trajectory level by the M4.4 render audit (matched Medium pairs: identical burn scars, burning counts 0/10/16/0 at t = 64/128/192/254). |
| 8.4 | δ off recovers free comms | — | **(b)** | M5.0. |
| 8.5 | "Ablations are exact nested models — no confound from re-implementation" | — | **(a)** | The whole `test_nesting.py` suite (9 tests) plus the structural-form tests. The strongest engineering claim in the document and the best-evidenced. |

---

## §9 — What we deliberately do not claim

All three are honest disclaimers, correctly stated, and all three should
survive into the paper verbatim.

| # | Claim | Ledger | Note |
|---|---|---|---|
| 9.1 | No convergence guarantees for the evolutionary+MARL hybrid | **(c)/(d) by design** | Jaderberg et al. (2017) in the bibliography ✓. |
| 9.2 | No theorem that joint training wins | **(d) by design** | Cites "(Reading 1, locked)" — the phantom of C-4. Strike the parenthetical or transcribe D0. |
| 9.3 | No exact critical values for the implemented kernel; claims reference measured order parameters, not β_c = 1/2 | **(a)** | Honoured in practice: `severity_lock.md` leads with the measured β̂_c. **Mild tension**: the same file then says "the idealized kernel's exact β_c = 1/2 (Kesten) is reproduced to three decimal places… the CA port is quantitatively validated" — which is a claim *about* β_c = 1/2, and rests on the untraceable estimator of C-9. Reproducing 1/2 is a fine result; just make sure the number quoted is one the repo can regenerate. |

---

## §10 — Theory → practice hooks

| # | Hook | Ledger | Note |
|---|---|---|---|
| 10.1 | Phase 2: sigmoidal P_span + calibrated bands | **(a)** | `test_percolation.py`. Wording defect L-3 ("ported"/"mis-ported"). |
| 10.2 | Phase 3: measured E[B_T] linear in collapse rate, slope ≈ Tχ̂ | **(a) — but the hook text is STALE** | Citation audit C-6: the hook still specifies the χ̂ comparison that the M3.3 ruling logged as a **spec error**. The live protocol is `matched_reference`. |
| 10.3 | Phase 4: E2C traces J* = ½ + q/2 | **(a)** | `test_e2c.py`, 5 `@slow` + 5 fast tests. |
| 10.4 | Phase 6/7: co-active counter from day one | **(a)** | Honoured — see 7.5. The doc's warning ("retrofitting logging into JIT-compiled rollouts is painful") was correct and was re-learned anyway at M4.0 (`burnt_fraction` retrofit). |

---

## §11 — Decision points

| # | Point | Ledger | Note |
|---|---|---|---|
| 11.1 | **D1** — dynamic hazard in Θ_iso's baseline | **resolved** | `decision_log.md:8`, restated in `CLAUDE.md`. |
| 11.2 | **D2** — ISO instantiation (a) mixture policy | **resolved** | `decision_log.md:13`. Secondary baseline (b) "if budget allows" is unscheduled — **(d)**, fine as an option. |
| 11.3 | **D3** — smoke outlives flame | **resolved** | `decision_log.md:18`; σ_s = 1.0, η = 0.5 in the configs. **But Def. 1 was never updated to match — L-1.** |

---

## Action register — what must change before the paper states these

Ordered by what a reviewer would catch first.

| # | Action | Claim | Severity |
|---|---|---|---|
| A-1 | **Amend Def. 4's Medium prediction** with the M3.0 refutation banner | 3.3 | **HIGH — a stated prediction the repo has already refuted** |
| A-2 | **Correct the "ported PyTorchFire/JaxWildfire" provenance** (2 sites in the theory doc, 2 in `test_percolation.py`, 1 in `phase1_2_prompt.md`) | 3.5 / L-3 | **HIGH — false attribution** |
| A-3 | **Add ρ to Def. 1's state space and kernel product**; fix the T_K/T_X order and the observation kernel's arguments | 1.1 / L-1 | **HIGH — Prop. 1's hypothesis is incomplete as written** |
| A-4 | **Hedge the 43/18 divergence rate** wherever it appears (Cor. 1(3), Prop. 3's corollary); never quote it as a property of this kernel | 2.6 / 4.4 | **HIGH** |
| A-5 | **Transcribe the locked hypothesis (D0)** and re-examine "primary metric = completion" against M4.4's survival finding | 7.2 | **HIGH** |
| A-6 | **Carry the two M4.2 paper sentences** — quadrature lower-bound limitation, and the masking-is-informative footnote — into the theory doc / paper | 5.3 / 5.8 | **MEDIUM — both already drafted** |
| A-7 | **Add four missing references**: 2D percolation exponents; shape theorem (or drop); Beer–Lambert; simulation lemma | 2.6 / 2.7 / 5.2 / 7.3 | MEDIUM |
| A-8 | **Repoint theory §10's Phase-3 hook** to the v2 matched-reference protocol | 10.2 | MEDIUM |
| A-9 | **Hedge Remark 2′(i)'s deficit-scaling law** to a conjecture; **hedge `q̃/q → 5/3`** as draw-counting until M5.2 measures it | 5.12 / 5.14 | MEDIUM |
| A-10 | **Hedge Prop. 3's behavioural corollary** — the χ-proportional incentive exists in the model; M3.5 found the swarm does not act on it | 4.5 | MEDIUM |
| A-11 | Add a **Prop.-1 step-order test** (one test, mutate each stage, assert the downstream stage sees it) | 1.5 | LOW — cheap |
| A-12 | Add a **per-edge-attempt-count test** for Prop. 2's coupling | 2.2 | LOW — cheap, closes the doc's best proof |
| A-13 | Optional: **sweep Prop. 3's slope across β** to convert 4.4 from (d) to (a) | 4.4 | LOW — a few CPU-hours |
| A-14 | Reconcile Def. 7's `p_link(d)` with M5.0's hard-range kernel | 6.1 | LOW — before M5.0 lands |
| A-15 | Confirm the eval harness can emit **failure conditioned on co-active count** before Phase 7 | 7.6 | LOW — but do it early (M4.0 lesson) |

---

## Ledger totals

| | count |
|---|---|
| Claims inventoried (§1–§8) | 57 |
| plus §9 disclaimers (3), §10 hooks (4), §11 decision points (3) | 10 |
| **(a)** validated by a named executable test | **32** |
| **(b)** scheduled (Phase 5: 8, Phase 6–7: 4) | **12** |
| **(c)** cited literature — reference present in the bibliography | **5** |
| **(c)** cited literature — **reference missing** | **4** — 2.6, 2.7, 5.2, 7.3 |
| **(d)** motivational / untested | **13** |
| of which **(d) needing a mandatory hedge or correction before the paper** | **8** — 1.1, 1.7, 2.6, 2.7, 4.4, 4.5, 5.12, 5.14 |
| Claims **tested and not supported** (carried honestly) | **3** — Def. 4's Medium prediction (3.3), Thm. 1's pure-information-loss idealization (5.8), Prop. 3's behavioural corollary (4.5) |

*(Codes sum above 57: several claims carry two, e.g. (c) for the literature
result and (a) for its reproduction in the implemented kernel.)*

The 3 "tested and not supported" rows are the ledger's most valuable output.
Two of them (5.8, 4.5) are already documented in phase reports with drafted
paper language. **The third (3.3) is not documented in the theory doc at all**
— which is exactly the gap this ledger exists to close.
