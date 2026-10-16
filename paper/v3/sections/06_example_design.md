<!-- PAPER V3 DRAFT (PAPER V3 ruling, 2026-10-12): builder-drafted, not owner-approved -->

## 6 Worked example: training on stressors together or apart

<!-- STUB-SPEC
JOB: 6.1: what was registered; the framing-change disclosure (V3-F5); the central limitation in full (V3-F6: the test was sited where composition is weak). 6.2: the design, with the identity, the design error, the δ train/test mismatch and bias (b).
WRITER: W4.
BUDGET: 500 prose words (6.1 about 170, 6.2 about 330); Figure 6 caption at most 50 words.
FROM: P1 §1.2, §4.2 §6.1 and §6.2, §5.2, §5.3 item 1; P3 §1.4 and §5.1; P2 §3 #6; orchestrator note (training δ).
ORDER:
  - 6.1 (a) what was registered, before the main training runs (no date): the test, its outcome branches with a framing for each, and a falsifier ("the claim the paper makes, as a function of the confirmatory outcome", PFB:15-16, may be quoted); (b) the disclosure, about three sentences: after the result was known, the paper's emphasis moved to the environment; the registered branches stay the record of the original framing (Appendix D); every registered reading below is reported as registered (HOME, two homes by ruling); (c) the central limitation in full (HOME): at the test severity Coupling B's own survival effect was not measurable against a three-seed spread (§4.3; one sentence allowed) and communication denial showed no detectable effect (§4.4), so little beyond Coupling A was under test; this was registered in advance as a limitation of every outcome (PFB:245-260, "Required on A, B and C alike", may be quoted); a post hoc check measures it (§6.4). Do not use the professor's phrase "mostly Coupling A" as fact.
  - 6.2 (a) arms: ISO, ISO-4 (sensitivity arm, outside the family, 20 seeds), JOINT; training severities β 0.43 and 0.70, test at the held-out θ* with every stressor on at β 0.49 (CAL-3); matched architecture, hyperparameters, evaluation draw and compute, at matched compute, never convergence (DES-13; HOME); one shared-parameter IPPO policy per seed (ENV-11); Def. 8 (Γ) in words; co-primaries completion and survival, Šidák m = 2 (DES-13); 72 seeds per arm, above the registered cap of 60, a recorded deviation made before unblinding (DES-3, DES-1; HOME, one clause; history Appendix D); every interval conditional on the one registered evaluation draw (DES-13; HOME). Figure 6.
  - 6.2 (b) the shares: per-coupling frequency μ, co-occurrence p, active share, fire-only share (define, BRIEF §5.2); JOINT sees each coupling three times as often as ISO (DES-7; HOME); the identity active share = μ_A + μ_B − p with each arm's values (X4-1; HOME): so no contrast in this design moves co-occurrence alone.
  - 6.2 (c) the design error (HOME; BRIEF §7.1, no dates): δ was already found inert; the design left it out of the secondary sweeps for that reason yet kept two δ-only components of six in ISO, so a third of ISO's episodes are fire-only (DES-8); a review of the registered design identified the bias before the grid; it was registered with its direction and the correcting arm ISO-4 before unblinding, while the grid ran (DES-15).
  - 6.2 (d) the δ train/test mismatch (HOME; use the word "mismatch"): ISO's Coupling-A-only and Coupling-B-only components and all of ISO-4 train with links intact (δ = 0), JOINT with δ = 1, and θ* has δ = 1 (X4-2); harmless only if δ is inert, the premise in question; the interaction check holds δ at 1 and cannot address it.
  - 6.2 (e) bias (b) in one sentence with the registered string "reverses sign on the grid GPU" (DES-10; full readings Appendix D).
ROWS: DES-1, DES-3, DES-7, DES-8, DES-9, DES-10, DES-13, DES-14, DES-15, DES-16, CAL-3, ENV-11, CB-9 (pointer or one sentence), COM-4 (pointer), X4-1, X4-2.
CITATIONS: dewitt2020ippo; keysers2020 only to say the sweep follows DBCA (ENDPOINT CONFOUND: never the ISO/JOINT endpoints).
FIGURES: Figure 6 composer_training_mixtures (6.2). Its caption says what it shows (each arm's training mixture by episode type; each coupling's frequency and the active share); gloss once that the toggle printed on it reads labelled “δ inert under a frozen random-projection encoder at this scale” is the figure's control (the label's home is §4.4). Block below.
LATEX: at most one display (the identity or Γ's definition).
REGISTERED STRINGS: "at matched compute"; "sensitivity arm"; "fire-only"; bias (b) "reverses sign on the grid GPU"; "registered before unblinding" for the correction; "pre-registered" only for the test.
CAVEATS HOMED HERE (state each in full, once; the detection pattern, from checks/caveats.yaml, must match your home sentence):
  C01 sited_where_composition_is_weak: The test was sited where composition is weak (Coupling B quiet at the test severity, communication denial without detectable effect); registered in advance as a limitation of every outcome; the post hoc interaction check measures it. Pattern: (?i)\bsited where\b
  C04 delta_train_test_mismatch: ISO's Coupling-A-only and Coupling-B-only components and all of ISO-4 train with links intact (δ = 0), while θ* has δ = 1; a train/test mismatch in communication denial. Detection phrase - "mismatch". Pattern: (?i)\bmismatch
  C07 joint_thrice_iso: JOINT sees each coupling three times as often as ISO (the endpoint confound). Pattern: (?i)\bthree times as often\b
  C08 active_share_identity: Active share = μ_A + μ_B − p, with each arm's values; so no contrast in this design moves co-occurrence alone. Pattern: μ_A\s*\+\s*μ_B
  C09 seeds_72_recorded_deviation: 72 seeds per arm, above the registered cap of 60, a recorded deviation made before unblinding (history in App. D). Pattern: (?i)\brecorded deviation\b
  C10 inert_third_design_error: A third of ISO's training episodes carried no active stressor; owned as a design error, identified before the grid and registered with its correction before unblinding (no dates in the main text). Pattern: (?i)\bdesign error\b
  C11 matched_compute_never_convergence: The comparison is at matched compute, never at convergence. Pattern: (?i)\bmatched compute\b
  C12 one_evaluation_draw: Every interval is conditional on the one registered evaluation draw. Pattern: (?i)\b(one|single|the one) (registered |common )?evaluation draw\b
  C13 bias_b_reverses_sign: Bias (b) "reverses sign on the grid GPU" (registered string); full readings in App. D. Pattern: (?i)reverses sign on the grid GPU
  C14 framing_change: The paper's emphasis moved to the environment after the result was known; the registered outcome branches stay the record of the original framing. Two homes by ruling (V3-F5) - here and App. D. Pattern: (?i)\bafter the (result|outcome) was known\b
SHORT FORMS ALLOWED HERE (at most one sentence each; the full statement is at the home):
  C34 coupling_b_medium_measurement (home 04_calibration.md)
EVERY OTHER CAVEAT in checks/caveats.yaml: pointer only ("§6.3", "Appendix D"), never restated. C26: any sentence about the interaction check carries "post hoc".
NEW ROWS OWED:
  - X4-1 (W4): the identity at each arm, DERIVED from DES-7, DES-14, DES-16, DES-9: ISO 1/3 + 1/3 − 0 = 2/3; ISO-4 1/2 + 1/2 − 0 = 1; JOINT 1 + 1 − 1 = 1; sweep arms (μ = 0.5) 1 − p; identification arms (μ = 0.4) 0.8 − p (P1 §5.2; check each input at its row source).
  - X4-2 (W4): training δ per arm, VERIFIED at che/configs/p6_iso.yaml:41-46, p6_iso4.yaml:36-39, p6_joint.yaml:36-37, theta_star_holdout.yaml:76 (BRIEF §0).
OWNER-PENDING:
  - the framing-change wording (V3-F5 is ruled; the words are the owner's to approve).
  - attribution of the review that found the bias (carried v2 A1(ii); default "a review of the registered design").
  - bias (b) label kept (V3Q21).
  - the registered antecedent not mentioned (V3Q22).
NOT HERE: any date (the registration date included; V3-S2); branch letters (Appendix D); "registered as a bias", "a registered design caught it", "stated before the result"; "certified"; "pre-registered correction"; GPU 1/2/3; study codes; the plane's result (§6.3); the interaction result (§6.4); "twice as often" (home §6.3).
V2 MATERIAL: paper/v2/sections/09_compositional_test.md §9.1; 01_introduction.md (the arms paragraph).
DEPENDENCIES: §6.3 (W4) relies on the identity and the shares being defined here; §1 (W1) cites X4-2; §6.4 (W5) repeats only its own evaluation-draw caveat.
-->

### 6.1 What was registered, and what changed

Before the main training runs, we pre-registered the test, its outcomes, a framing for each, and a falsifier.

<!-- OWNER-PENDING:wording of the framing-change disclosure (V3-F5 is ruled; the words are the owner's to approve) -->
After the result was known, the paper's emphasis moved from the test to the environment. The registered framings remain the record of the original plan (Appendix D).

The test was sited where composition is weak. At the test severity, Coupling B's calibrated survival effect was within a three-seed<!-- N:CB-9 --> spread, not a measured floor (§4.3), and communication denial had no detectable effect (§4.4), so the test point may have offered little composition. The registration stated the Coupling-B half in advance, for every outcome: that both couplings meet their fixed-value criteria here "is not the same as both producing behavioural effects there". A post hoc interaction check measures this (§6.4).

### 6.2 Design

The isolated arm (ISO) trains on configurations with one stressor on at a time and the joint arm (JOINT) with every stressor on, both at β = 0.43<!-- N:CAL-3 --> and 0.70<!-- N:CAL-3 --> with one shared-parameter IPPO policy per seed<!-- N:ENV-11 --> <d-cite key="dewitt2020ippo"></d-cite>. Both are evaluated at θ\*, the held-out test configuration: every stressor on at β = 0.49<!-- N:CAL-3 -->. Architecture, hyperparameters, evaluation draw and compute (1000<!-- N:DES-13 --> updates) are matched: Γ is read at matched compute, with no claim about convergence. The gap Γ, JOINT's mean minus ISO's at θ\*, is tested on two co-primaries, completion and survival, Šidák-corrected for m = 2<!-- N:DES-13 -->: the confirmatory family. We ran 72<!-- N:DES-3 --> seeds per arm, above the registered cap of 60<!-- N:DES-1 -->, a recorded deviation made before unblinding. Every interval is conditional on the one registered evaluation draw.

Let $\mu_A$ and $\mu_B$ be the per-coupling frequencies, the shares of episodes with each coupling on, and $p$ the co-occurrence, the share with both. The active share is the share with at least one behaviourally active stressor; the fire-only share $\nu$ is the rest. JOINT sees each coupling three times as often as ISO<!-- N:DES-7 -->, so Γ mixes frequency with co-occurrence. With communication denial inert (§4.4), the active share equals $\mu_A + \mu_B - p$<!-- N:X4-1 -->: 2/3 for ISO and 1 for JOINT<!-- N:X4-1 --><!-- N:DES-14 --> (Figure 6). No contrast in this design moves co-occurrence alone.

<!-- OWNER-PENDING:A1(ii) attribution of the review that found the bias (default "a review of the registered design") -->
One design error inflates Γ. Communication denial had been found inert and so was left out of the secondary sweeps, yet ISO kept two δ-only components of six<!-- N:DES-16 -->: a third<!-- N:DES-8 --> of ISO's training episodes are fire-only, and the design did not count them. A review of the registered design found the bias before the main runs; it was registered with its direction and a correcting arm before unblinding, during the main runs<!-- N:DES-15 -->. That arm, ISO-4, is ISO without its δ-only components (active share 1<!-- N:X4-1 --><!-- N:DES-14 -->), a sensitivity arm outside the confirmatory family with 20<!-- N:DES-15 --> seeds. The corrected gap is Γ₄ = JOINT − ISO-4, and B̂ = ISO-4 − ISO.

ISO's single-coupling components and all of ISO-4 train with links intact (δ = 0<!-- N:X4-2 -->), while JOINT trains and θ\* tests at δ = 1<!-- N:X4-2 -->. This train/test mismatch is harmless only if δ is inert; the post hoc interaction check (§6.4) holds δ at 1 and cannot address it.

<!-- OWNER-PENDING:V3Q21 bias (b) label kept (default); V3Q22 registered antecedent not mentioned in the main text (default) -->
Bias (b), the registered caveat on differential completion drift in the last 100 updates<!-- N:DES-10 -->, reverses sign on the grid GPU (the main runs' GPU), so no direction is claimed (Appendix D).

<!-- FIGURE 6: block carried from paper/v2/sections/01_introduction.md:29 (markup, iframe height and alt text as v2 had them); caption replaced; the writer checks the alt text -->

<figure class="l-page">
  <iframe src="{{ 'assets/html/submission/composer_training_mixtures.html' | relative_url }}" width="100%" height="442" style="border:none" title="Training mixtures of ISO, ISO-4 and JOINT by episode type" loading="lazy"></iframe>
  <figcaption><strong>Figure 6.</strong> Each bar splits one arm's training mixture into episode types: Coupling A only, Coupling B only, both together, and fire-only. Beneath each bar are each coupling's frequency (labelled “per-stressor marginal” on the figure) and the active share. <span class="interact">Count δ-only episodes as inert or nominally; split by β.</span></figcaption>
</figure>

<div class="print-companion">
{% include figure.html path="assets/img/submission/composer_training_mixtures.png" class="img-fluid" alt="Stacked bars of the three training mixtures by episode type, with each arm's per-coupling frequencies and the share of episodes that carry an active stressor." caption="Static companion of Figure 6 for the printed PDF." %}
</div>
