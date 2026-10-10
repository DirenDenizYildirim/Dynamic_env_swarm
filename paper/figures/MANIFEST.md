# Candidate figures: manifest

Built 2026-10-10 under the decision log's **FIGURES** entry (owner,
2026-10-10). Its later same-day entries (FIGURES ADDENDUM: the restyle,
done by another session in `paper/renders/2026-10-10/`; FIGURES FIRST: the
interactive design, `paper/figures/interactive/`) were read before closing;
two details here were brought into line with FIGURES FIRST (Stage A
Figure 9 verdict string; Stage E survivor tally). These are **candidates, not placements**: nothing here is in
`paper/beyond_pdf/assets/` until the owner rules on it at the section step.
Captions are the owner's; every figure carries factual labels only.

**Conventions used everywhere below.**

- `R/` = `che/bench/results/`; `P6/` = `che/bench/results/phase6/`.
- A number **stated** in a figure (text in a PNG, or text in an HTML
  tooltip, label or table view) is listed with its ledger row, or with its
  committed file and key/line. A stated number with **no ledger row** is
  marked **NEEDS LEDGER ROW**. Plotted marks read from committed files are
  data, not stated numbers.
- Nothing is re-estimated. Where a script re-reads per-seed eval JSONs to
  plot them, it **asserts** that their mean reproduces the committed arm
  mean (to 1e-9) and stops otherwise. Every such assertion passed.
- Static PNGs: matplotlib 3.11.1, DejaVu Sans, 200 dpi, white surface,
  written with `metadata={"Software": None}`. Interactive HTML: one
  self-contained file each (inline CSS, inline JSON data, inline vanilla JS
  building inline SVG; no external URL, script, font or library), light and
  dark themes (it follows the embedding page's `data-theme` when it has one,
  else the OS setting), keyboard-focusable marks, and a table view.
- Palette: the dataviz reference palette's first three categorical slots
  (blue, orange, aqua), validated all-pairs in light and dark with the
  skill's `validate_palette.js` (aqua carries a contrast WARN on light:
  relieved by labels and the table view). Contrast and estimate figures are
  drawn in ink and grey only. Every series is also distinguished by marker
  shape or line style, so each figure reads in greyscale.
- Rebuild: from `paper/figures/src/`, run each `figNN_*.py` with
  `OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 nice -n 15 uv run python figNN_*.py`,
  then `check_metadata.py`.

---

## Stage A: Figures 8 and 9 (the confirmatory result)

### `out/img/fig08_gamma_contrasts.png` and `out/html/fig08_gamma_contrasts.html`

- **Slot:** Figure 8 (`submission.md` §9 Results).
- **What it plots:** two forest panels, completion and survival rate. Rows,
  registered reading first: **Γ = JOINT − ISO, k = 72, 72** (the registered
  confirmatory contrast); Γ at the registered-ladder **k = 60 prefix**
  (seeds 1–60); a rule; then, labelled "outside the confirmatory family",
  **Γ₄ = JOINT − ISO-4** (k = 72, 20), **Γ₄′ = JOINT − sweep_c50_p000**
  (k = 72, 20) and **B̂ = ISO-4 − ISO** (k = 20, 72). Each row: estimate,
  Šidák 95 % CI (m = 2), a grey band ±X (that row's committed 80 %-power
  MDE, `exclusion_mde80`), and, on the k = 72 Γ row only, a hatched floor
  bar ±1 floor-basis sd(Γ). Right-hand text: estimate, CI, and the test
  outcome at the Šidák level (REJECT / null, the committed `reject` field).
  The HTML adds a metric toggle, a **per-seed arm view** (ISO 72, ISO-4 20,
  sweep_c50_p000 20, JOINT 72 seeds, with arm means), tooltips, and a table
  view; its static companions are the PNG above and
  `out/img/fig08b_gamma_arms_per_seed.png`.
- **Sources:**
  - Γ, k = 72: `P6/unblind/unblind.json` → `primary.family.{completion,survival_rate}`
    (`gamma`, `ci_sidak`, `exclusion_mde80`, `sd_gamma`, `z`, `reject`, `k`);
    report lines `P6/unblind/report.md:11-12`.
  - Γ, k = 60: same file → `prefix.family.*`; `report.md:21-22`.
  - floor: same file → `beat_reproducibility.*.sd_gamma_floor_basis`; `report.md:38-39`.
  - Γ₄ and B̂: `P6/post_unblind_analysis/post_gamma4_t2000.json` →
    `gamma4.per_metric.*.{gamma4,b_hat}`; `post_gamma4_t2000.md:12-16`.
  - Γ₄′: `P6/secondary/secondary.json` → `replicate.*.gamma4_prime`;
    `secondary.md:52-53`.
  - per-seed (HTML and fig08b): ISO, JOINT `unblind.json` →
    `primary.per_seed.{iso,joint}.*`; ISO-4 `P6/g1_iso4_5090/eval_iso4_s{1..20}.json`
    → `metrics.*.mean`; sweep_c50_p000 `P6/g1_sec_s1_12_5090/eval_sweep_c50_p000_s{1..12}.json`
    and `P6/g1_grid/eval_sweep_c50_p000_s{13..20}.json` → `metrics.*.mean` (the
    seed split of `che/scripts/p6_secondary.py`). Each eval passes the
    confirmatory reader's guards (step 1000, 512 episodes, eval seed 0, θ*
    config). Arm means asserted equal to `unblind.json` `mean_iso`/`mean_joint`,
    `post_gamma4_t2000.json` `gamma4.*.gamma4.mean_a`, and `secondary.json`
    `metrics.*.sweep_means.sweep_c50_p000`.
- **Numbers stated (PNG text, and HTML labels/tooltips/table):**

  | shown | ledger / source |
  |---|---|
  | Γ completion −0.0173 [−0.0412, +0.0066], null | RES-1 |
  | Γ survival +0.0096 [+0.0047, +0.0144], REJECT | RES-2 |
  | Γ k = 60: completion −0.0217, survival +0.0104 | RES-3 |
  | Γ k = 60 Šidák CIs [−0.0486, +0.0052] and [+0.0054, +0.0155] | **NEEDS LEDGER ROW**: `unblind/report.md:21-22` |
  | Γ₄ survival −0.0003 [−0.0068, +0.0063]; completion −0.0126 | RES-6 |
  | Γ₄ completion CI [−0.0481, +0.0228] | **NEEDS LEDGER ROW**: `post_gamma4_t2000.md:12` |
  | B̂ survival +0.0098 [+0.0033, +0.0163]; completion −0.0046 | RES-7 |
  | B̂ completion CI [−0.0405, +0.0312] | **NEEDS LEDGER ROW**: `post_gamma4_t2000.md:13` |
  | Γ₄′ survival +0.0013 [−0.0056, +0.0081]; completion −0.0247 | RES-8 |
  | Γ₄′ completion CI [−0.0616, +0.0122] | **NEEDS LEDGER ROW**: `secondary.md:52` |
  | k = 72, 60, 20; Šidák m = 2 | DES-13 (72, 20, m = 2); RES-3 (60); DES-15 (ISO-4 k = 20) |
  | REJECT / null labels | the `reject` fields above (RES-1, -2, -3, -6, -7, -8 state the same decisions) |
  | *HTML only:* X completion 0.0329 (RES-1); X₄ completion 0.0488 (RES-6) | ledger |
  | *HTML only:* X survival 0.0066; X k = 60 0.0370 / 0.0069; X Γ₄ survival 0.0090; X B̂ 0.0493 / 0.0089 | **NEEDS LEDGER ROW**: `unblind/report.md:12, :21-22`; `post_gamma4_t2000.md:13, :15-16` |
  | *HTML only:* X Γ₄′ 0.0508 / 0.0094 | **NEEDS LEDGER ROW**: `secondary.json` `replicate.*.gamma4_prime.exclusion_mde80` (not printed in `secondary.md`) |
  | *HTML only:* sd(Γ) per row (0.01068, 0.00216, 0.01203, 0.00224, 0.01587, 0.00294, 0.01652, 0.00307, 0.01602, 0.00289) | **NEEDS LEDGER ROW**: the `sd_gamma` keys above; `report.md:11-12, :21-22`; `post_gamma4_t2000.md:12-16` (Γ₄′ JSON only) |
  | *HTML only:* z per row: Γ −1.62 / +4.43 (RES-1, -2); k = 60 −1.80 / +4.67 (RES-3); Γ₄ −0.09 (RES-6), B̂ +3.39 (RES-7), Γ₄′ +0.41 (RES-8) | ledger |
  | *HTML only:* z Γ₄ completion −0.80, B̂ completion −0.29, Γ₄′ completion −1.50 | **NEEDS LEDGER ROW**: `post_gamma4_t2000.md:12-13`; `secondary.md:52` |
  | *HTML only:* floor-basis sd(Γ) 0.00970 / 0.00177 | **NEEDS LEDGER ROW**: `unblind/report.md:38-39` (HW-1 carries only the 5.40× ratio) |
  | *HTML only:* arm means ISO 0.7772 / 0.9158, JOINT 0.7600 / 0.9254 | RES-4 |
  | *HTML only:* arm means ISO-4 0.7726 / 0.9256, sweep_c50_p000 0.7847 / 0.9241 | **NEEDS LEDGER ROW**: `post_gamma4_t2000.md:12, :15`; `secondary.md:22, :35` |
  | *HTML table, fig08b:* per-seed values (4 decimals) | data read from the committed eval files listed above, not ledger numbers |

- **Interval levels and floors:** every interval is the committed Šidák
  95 % CI at m = 2, z_α = 2.2365 (DES-13), conditional on the common eval
  draw. Γ₄, Γ₄′ and B̂ are reported at the family's z_α as their reports
  do, but are outside the confirmatory family (DES-15). Floor: only the
  k = 72 Γ row has one (the beat-reproducibility floor of `unblind.json`);
  ISO-4 has no rep set (`post_evalfloor_gamma_t_high.md:84, :86` says so for
  High; no ISO-4 or sweep_c50_p000 floor exists at θ*), so the other rows
  carry no floor bar. The floor bar is ±1 floor-basis sd(Γ), not a 2σ bar.
- **Known limits:** the MDE band is drawn around 0 as ±X; X is the 80 %-power
  MDE at Šidák α (METH-7), the "exclusion" quantity of the registered plan.
  Γ = Γ₄ + B̂ holds by construction (arm means); the figure states no such
  sentence. The k = 60 prefix row is optional; drop it if §9 does not cite RES-3.
- **Metadata check:** passed (see the last section).

### `out/img/fig08b_gamma_arms_per_seed.png`

Static companion of the HTML's per-seed view (sources and assertions as
above). States only k (72, 20: DES-13) and the axis. Optional; Figure 8
does not need it.

### `out/img/fig09_gamma_t.png`, `out/img/fig09b_gamma_t_single_card.png`, `out/html/fig09_gamma_t.html`

- **Slot:** Figure 9 (§9 Results; appendix H).
- **What it plots:** Γ(t) = JOINT − ISO at the 11 retained checkpoints
  t = 500, 550, …, 1000, both co-primaries, k = 72 per arm, with the Šidák
  95 % band. **The registered verdict is stated first**, in each panel's
  title, verbatim: "rule (iv): sign unstable over the final half" (both
  co-primaries; verdict strings verbatim are allowed by the FIGURES FIRST
  ruling, item 3), with the 11 signs printed above the panel. A hatched bar at t = 1000 is the T\* floor
  (±1 floor-basis sd(Γ), the same floor as Figure 8). A footer states which
  card evaluated which point. **Companion** `fig09b`: the single-card curve
  (ruling viii): identical at t < 1000, with t = 1000 re-evaluated on the
  post-unblind card; its title reads "single-card signs: not stable
  (descriptive)", because the registered rule reads the grid's own t = 1000
  eval. The HTML toggles
  between the two and adds a crosshair tooltip (arrow keys step through
  checkpoints) and a table view.
- **Sources:** `P6/post_unblind_analysis/post_evalfloor_gamma_t_high.json`
  → `gamma_t.points.*` (`t`, `gamma`, `ci_sidak`, `sd_gamma`, `z`, `mean_a`
  = ISO, `mean_b` = JOINT), `gamma_t.verdict.*.{signs,stable}`,
  `gamma_t.cross_card_T_star.*.{gamma_post_card_T_star,single_card_signs,single_card_stable}`;
  report `post_evalfloor_gamma_t_high.md:20-72`. Floor:
  `P6/unblind/unblind.json` `beat_reproducibility.*.sd_gamma_floor_basis`.
  The script asserts that the t = 1000 point equals the primary Γ and that
  the committed signs match the committed estimates.
- **Numbers stated:**

  | shown | ledger / source |
  |---|---|
  | signs `+ − + + − − − − − − −` (completion), `+ − − + + + + + + + +` (survival); UNSTABLE on both | RES-11 |
  | single-card signs (identical) | `post_evalfloor_gamma_t_high.md:69-70` (spine §9.2 item 6: "the single-card curve has the same signs"); **NEEDS LEDGER ROW** if quoted |
  | k = 72, m = 2, T\* = 1000, 11 checkpoints 500–1000 every 50 | DES-13 |
  | *HTML only:* Γ(t), Šidák CI at survival t = 900, 950, 1000 | RES-12 (estimates); the CIs are `post_evalfloor_gamma_t_high.md:52-54`, **NEEDS LEDGER ROW** for the interval endpoints |
  | *HTML only:* completion Γ(750) −0.0147 [−0.0283, −0.0010] | RES-13 |
  | *HTML only:* t = 1000 values | RES-1, RES-2 |
  | *HTML only:* every other Γ(t), CI, sd(Γ), z, and the per-arm means at each t | **NEEDS LEDGER ROW** (as a group): `post_evalfloor_gamma_t_high.md:26-36, :44-54`; arm means only in the JSON (`mean_a`, `mean_b`) |
  | *HTML only, single-card t = 1000:* −0.0173 [−0.0412, +0.0066] and +0.0096 [+0.0047, +0.0144] | **NEEDS LEDGER ROW**: `post_evalfloor_gamma_t_high.json` `cross_card_T_star.*.gamma_post_card_T_star` (equal to RES-1/RES-2 at 4 decimals; `post_evalfloor_gamma_t_high.md:69-70` prints the estimates) |

- **Interval levels and floors:** Šidák 95 % (m = 2) at every checkpoint, as
  committed; descriptive at t ≠ T\* (no registered test exists there,
  RES-13). Floor only at T\* = 1000 (none was measured at t < 1000).
- **Known limits:** t < 1000 was evaluated on the post-unblind card and
  t = 1000 on the grid card (HW-2, HW-3: eval-reproducible, 280 of 288
  paired evals identical). The connecting line joins discrete checkpoints;
  no value between them was measured. The T = 2000 subsample (RES-15) is not
  in this slot.
- **Metadata check:** passed.

---

## Stage B: Figure 10 (secondary)

### `out/img/fig10_secondary.png` and `out/html/fig10_secondary.html`

- **Slot:** Figure 10 (§9.2 item 4; appendix I).
- **What it plots:** a header label "SECONDARY · non-verdict-bearing · 95 %
  bootstrap-over-seeds intervals, not family-corrected · k = 20 per arm".
  (1) Survival rate and completion against p for the five sweep arms
  (m = 0.5, n = p) and the three identification arms (m = 0.4, n = 0.2 + p):
  every seed (20 per arm), the arm means, and the committed confound-plane
  fit per arm (dotted). Above each panel, the knee's committed 95 % CI as a
  bracket with κ̂ marked, labelled "UNDERPOWERED". A hatched floor bar at
  sweep p = 0.5, the only floored arm (±1 rerun sd). (2) The design space
  (p, n) with all eight secondary arms, the sampled p range shaded, and
  ISO (0, 1/3), ISO-4 and sweep_c50_p000 (0, 0) and **JOINT (1, 0), outside
  the sampled range**. (3) The **non-extrapolation**: the plane's committed
  prediction for JOINT − ISO-4 (γ_p × 1, with γ_p's 95 % CI) beside the
  measured Γ₄ and Γ₄′ (Šidák 95 % CIs). (4) The committed secondary
  estimates per metric: dose slope, endpoint (with its ±1 floor-basis SE
  hatched), γ_p, γ_n, the no-element bound. A footer label: "mediation:
  VOID". The HTML adds a metric toggle (survival rate / completion; the
  prediction panel follows it), tooltips per arm and estimate, and table
  views.
- **Sources:** `P6/secondary/secondary.json` → `design`;
  `metrics.*.confound.arm_means_vs_plane` (per-arm `mean`, `fit`,
  `resid_over_se`); `metrics.*.dose_trend` (`ols_slope_per_unit_p`,
  `ols_slope_ci95`); `metrics.*.knee` (`kappa`, `ci95`, `flag`,
  `underpowered`); `metrics.*.confound` (`gamma_p`, `gamma_p_ci95`,
  `gamma_n`, `gamma_n_ci95`, `bound_confound_share_of_sweep_change`,
  `bound_ci95`); `metrics.*.endpoint_grade` (`endpoint_diff`, `ci95`,
  `se_floor_basis`, `floor_sd_sweep_p500`, `floor_note`); `mediation.verdict`;
  `replicate.*.gamma4_prime`. Γ₄: `post_gamma4_t2000.json`
  `gamma4.per_metric.*.gamma4`. Per-seed: `P6/g1_sec_s1_12_5090/eval_<arm>_s{1..12}.json`
  and `P6/g1_grid/eval_<arm>_s{13..20}.json` → `metrics.*.mean` (the
  instrument's seed split; g1_grid's superseded seeds 1–12 are never
  opened), each mean asserted equal to the committed arm mean. Reference
  arm coordinates: ISO (p = 0, n = 1/3) DES-7/DES-8; ISO-4 (0, 0) and JOINT
  (1, 0) DES-14; sweep_c50_p000 (0, 0) `secondary.md:9`. ISO-4 and
  sweep_c50_p000 have the same realized marginals (both config headers,
  `che/configs/p6_iso4.yaml:7`, `che/configs/p6_sweep_c50_p000.yaml:7`; the
  sweep config carries extra zero-weight components).
- **Numbers stated:**

  | shown | ledger / source |
  |---|---|
  | m = 0.5, n = p; m = 0.4, n = 0.2 + p | DES-9 |
  | k = 20 per arm | DES-13 (K_SECONDARY) |
  | ISO (p = 0, n = 1/3); ISO-4 (0, 0); JOINT (1, 0); sweep_c50_p000 (0, 0) | DES-8, DES-14; `secondary.md:9` |
  | UNDERPOWERED (both knees) | SEC-6 |
  | mediation: VOID | SEC-7 |
  | "γ_p × 1 (p: 0 → 1, n: 0 → 0)" | SEC-4's arithmetic |
  | *HTML only, survival:* γ_p +0.0326 [+0.0137, +0.0502], γ_n −0.0237 [−0.0419, −0.0057] | SEC-1 |
  | *HTML only, survival:* bound −0.0119 [−0.0210, −0.0028] | SEC-2 |
  | *HTML only, survival:* prediction JOINT − ISO-4 +0.0326 | SEC-4 (its CI is γ_p's, SEC-1) |
  | *HTML only, survival:* slope +0.0089 [−0.0033, +0.0211]; endpoint +0.0048 [−0.0021, +0.0117] | SEC-5 |
  | *HTML only, survival:* Γ₄, Γ₄′ | RES-6, RES-8 |
  | *HTML only, completion:* slope −0.0251 [−0.0943, +0.0412]; endpoint −0.0097 [−0.0482, +0.0287]; γ_p +0.0269 [−0.0675, +0.1245]; γ_n −0.0652 [−0.1534, +0.0242]; bound −0.0326 [−0.0767, +0.0121] | **NEEDS LEDGER ROW**: `secondary.md:25-26, :28` |
  | *HTML only, completion:* prediction JOINT − ISO-4 = γ_p × 1 = +0.0269 [−0.0675, +0.1245] | **NEEDS LEDGER ROW**, DERIVED as SEC-4: +0.0269 × (1 − 0) + γ_n × (0 − 0) |
  | *HTML only, completion:* Γ₄ −0.0126 [−0.0481, +0.0228]; Γ₄′ −0.0247 [−0.0616, +0.0122] | RES-6 / RES-8 (estimates); CIs **NEEDS LEDGER ROW** as for Figure 8 |
  | *HTML only:* knee κ̂ 0.375, 95 % CI [0.125, 0.375] (both metrics) | **NEEDS LEDGER ROW**: `secondary.md:27, :40` |
  | *HTML only:* floor at sweep p = 0.5: rerun sd 0.0130 (survival), 0.0196 (completion); floor-basis SE of the endpoint 0.0041 / 0.0062 | **NEEDS LEDGER ROW**: `secondary.json` `metrics.*.endpoint_grade.{floor_sd_sweep_p500,se_floor_basis}` |
  | *HTML only:* per-arm means, plane fits and (mean − fit)/SE | **NEEDS LEDGER ROW** (as a group): `secondary.md:22, :29, :35, :42` (means and residuals); fits only in the JSON |

- **Interval levels and floors:** secondary intervals are the committed 95 %
  bootstrap-over-seeds (B = 2000), **not family-corrected**; Γ₄ and Γ₄′
  carry their committed Šidák 95 % CIs, and the legend separates the two
  kinds. Floors: the sweep p = 0.5 rerun floor (8 reps) at that arm only,
  and the endpoint's floor-basis SE, which the instrument computes with the
  p = 0.5 floor **assumed common at p = 0** (flagged in the source; stated in
  the tooltip). Intermediate sweep points and the identification arm have no
  floor (`secondary.md:61`).
- **Known limits:** the plane is linear in (p, n) by assumption
  (`secondary.md:59`). The figure plots no plane value at JOINT's (1, 0):
  γ₀ is not committed, so only the committed contrast γ_p × 1 is shown.
  The predicted ISO-4 − ISO (SEC-3, +0.0079) is **not** drawn: it has no
  committed interval (owner decision below). The mediation panel is absent
  by the instrument's own verdict ("the dose figure has no x-axis").
- **Metadata check:** passed.

---

## Stage C: Figures 2–7 (calibration, couplings, co-active, comms, floors)

### `out/img/fig02_calibration.png` and `out/html/fig02_calibration.html`

- **Slot:** Figure 2 (§4).
- **What it plots:** (left) P_span(β) at L = 32, 48, 64 over the 35-point
  grid; (right) R_L(β) over 0.40–0.60; each point with its committed
  binomial ±1 SE (512 seeds). The locked β̂_c = 0.500 ± 0.005 as a band
  and line; the three locked levels as dotted lines, with the L = 64
  P_span value at each (0.021, 0.547, 0.998); R = 1/2 as a reference line.
  The HTML toggles P_span / R_L and each L, with a crosshair tooltip and a
  table view.
- **Sources:** `R/phase2/estimates.npz` → `betas`, `p_span_L{32,48,64}`,
  `p_span_se_L*`, `r_betas`, `r_L*`, `r_se_L*` (identical to
  `phase2_results/`, checked byte-for-byte). β̂_c: `docs/locks.yaml:46-57`,
  `severity_lock.md:7`. Levels and P_span values: `severity_lock.md:29-31`,
  `R/phase2/calibration_report.md:107-109`; the script asserts that the
  committed L = 64 curve rounds to them.
- **Numbers stated:** β̂_c = 0.500 ± 0.005 (CAL-1); 0.43 / 0.49 / 0.70 and
  P_span 0.021 / 0.547 / 0.998 (CAL-3); L = 32, 48, 64 and 512 seeds
  (CAL-1, `calibration_report.md:5-7`; **NEEDS LEDGER ROW** for "512 seeds"
  if a caption quotes it); R = 1/2 (theory value, Kesten; not a measured
  number). HTML table/tooltips: every curve value ± SE, data from the npz.
- **Interval levels:** ±1 SE, binomial, as committed. No CI is computed.
- **Known limits, and what is missing (ledger O-2):** the R_L
  **logistic-centre** estimates (0.4985 / 0.5006 / 0.4999) that the lock
  rests on have **no committed script or artifact**, so no logistic fit,
  centre or crossing is computed or drawn; the band is the lock's value,
  not something this figure's data derive. The committed alternatives
  (`R/phase2/estimates.json`: R_L pairwise crossings 0.4986, 0.5025, 0.5157,
  0.5010, mean 0.504; consensus 0.499) are not drawn either (owner decision
  below). The self-duality values R_L(0.500) (CAL-2) are visible as data at
  β = 0.50 but not labelled.
- **Metadata check:** passed.

### `out/img/fig03_coupling_a.png`

- **Slot:** Figure 3 (§5).
- **What it plots:** (a) the Prop.-3 dense sweep at L = 64: E[B_T] (burnt
  cells at the horizon) against realized E[N_seeds] at the five λ₀ values,
  ±1 SE, with the committed through-origin fit line; the run's parameters
  printed in the panel (β 0.43, κ_A 0.02, f_weak 0.4, 4096 runs per point,
  no agents). (b) collapse-seeded ignitions per episode at Low / Medium /
  High under trained policies: m44 (κ_B = 1.0 arm) and m35 (κ_A on arm),
  per-seed values (2–3 seeds) and pooled means.
- **Trap respected:** the two Prop.-3 runs are two runs. Only CA-2's run
  (dense sweep, L = 64, κ_A 0.02, f_weak 0.4: not the locked parameters) has
  committed data and is drawn, labelled with its own parameters. CA-3's
  handshake (purified L = 32 CPU test, κ_A 0.003, ratio 0.992) is report text
  only and is **not** drawn or quoted.
- **Sources:** (a) `R/phase3/m33/prop3_L64.json` → `e_n_seeds`, `e_b_t`,
  `se_b_t`, `slope_through_origin` (:44), `r2_through_origin` (:45),
  `grid_size`, `beta`, `kappa_A`, `f_weak`, `n_seeds_mc`. (b) m44:
  `R/e1/severity/severity.json` → `grids.m44.cells.{low,medium,high}|kbL.seeded_ignitions.mean`;
  per-seed `R/phase4/m44/m44_analysis.json` →
  `arm_comparison.*/seeded_ignitions.kbL_seed_means`. m35: `severity.json`
  → `grids.m35.cells.*|kaL`; per-seed `R/phase3/m35/eval_{lv}_kaL_dp0.5_s{0,1}.json`
  → `metrics.seeded_ignitions.mean`. Seed means asserted to reproduce the
  pooled means; pooled means asserted to round to CA-4 / CA-5.
- **Numbers stated:** R² = 0.998 (CA-2); L = 64, β = 0.43, κ_A = 0.02,
  f_weak = 0.4 (CA-2's note); "4096 runs per point" (**NEEDS LEDGER ROW**:
  `prop3_L64.json` `n_seeds_mc`); m44 Low / High = 4.83× (CA-4);
  m35 4.92× (CA-5); β per level (CAL-3); "500 updates" (`R/phase3/phase3_report.md:154`, M3.5 grid;
  `R/phase4/phase4_report.md:581`, M4.4; **NEEDS LEDGER ROW** if quoted).
- **Interval levels and floors:** (a) ±1 SE as committed. (b) no interval:
  the per-seed points are the spread (2 or 3 seeds). **No floor is drawn
  in (b)**: the only seeded-ignition floors (`severity.json` `floors`:
  Medium from m55, High from m53b, 4 reps each) were measured on other
  artifacts, and the per-artifact amendment forbids grading m44 or m35
  against them. They are also below a marker's size (sd 0.0075 and 0.0029
  per episode). Owner decision below.
- **Known limits:** the χ̂ reference line and the deficit waterfall of
  `phase3_report.md` are not drawn (the slot asks for the linearity; the
  reference needs the report's protocol-correction discussion to be read).
- **Metadata check:** passed.

### `out/img/fig04_coupling_b.png`

- **Slot:** Figure 4 (§6).
- **What it plots:** (a) for each severity, the masked share of the crop
  over all alive agent-steps (open) and at danger moments (filled), log
  scale, with the amplification ratio. (b) High survival, κ_B 1.0 − 0:
  **the three replicate contrasts first** (seed 0 and seed 1 of M4.4, and
  the same-seed seed-0 retrain), then, below a rule, the **first estimate**
  (the 2-seed M4.4 mean) beside them; a hatched band ±1 sd of the High
  reproducibility floor.
- **Sources:** (a) `R/phase4/m44/m44_analysis.json` →
  `danger_moment_masking.{low,medium,high}/kbL.{masked_frac_uncond,masked_frac_danger,amplification}`;
  report table `R/phase4/phase4_report.md:362-364`. (b) seed contrasts:
  `m44_analysis.json` `arm_comparison.high/survival_rate.{kb0_seed_means,kbL_seed_means}`
  (seed 0 equals `R/phase5/pretask/replicate_deltas.txt` "M4.4 originals
  survival_rate −0.0687"; seed 1 equals `phase4_report.md:641` "−0.1066",
  both asserted); retrain `replicate_deltas.txt` "replicate pair
  survival_rate −0.0470"; first estimate `m44_analysis.json`
  `arm_comparison.high/survival_rate.delta` (:378); floor
  `R/phase5/m53b/reproducibility_floor_high.txt:7`.
- **Numbers stated:** 118× / 22× / 16× (CB-10); −0.0687, −0.1066, −0.0470
  (CB-5: "range −0.047 to −0.107"; the three values individually are
  `replicate_deltas.txt` and `phase4_report.md:641`, **NEEDS LEDGER ROW** for
  −0.0687 and −0.1066 as stated values); −0.0876 (CB-6); floor 0.0621
  (CB-7, OK≈); "4 identical High runs" (CB-7's source, :1-3).
- **Interval levels and floors:** no CI exists for these contrasts (one run
  per cell); the floor is the measured High survival floor (4 identical
  runs, M5.3b), the one CB-5 grades against ("pooled 1.41× the floor" =
  0.0876 / 0.0621). The band is ±1 per-run floor sd; a two-run contrast's
  own floor would be wider by √2 (not drawn, not computed into the figure).
- **Known limits:** completion (CB-8, the sign flip) and Medium survival
  (CB-9) are not in this slot. In (a) the danger-moment share is pooled
  over episodes (`masked_danger_sum / danger_agents`), as the report defines it.
- **Metadata check:** passed.

### `out/img/fig05_coactive.png`

- **Slot:** Figure 5 (§6).
- **What it plots:** small multiples, one per severity: the share of
  episodes with 0, 1, 2, 3 and ≥ 4 co-active events (m44, κ_B = 1.0 arm,
  seeds pooled), P(0) labelled, n episodes labelled. **The distribution, not
  the mean.**
- **Sources:** `R/phase4/m44/m44_analysis.json` →
  `co_active.{low,medium,high}/kbL.{hist_0_1_2_3_4plus,share_zero,n_episodes}`;
  report `phase4_report.md:423-427`. The script asserts each histogram sums
  to 1 and P(0) rounds to CO-2.
- **Numbers stated:** P(0) 0.563 / 0.578 / 0.883 and n 1024 / 1536 / 1024
  (CO-2); β per level (CAL-3).
- **Interval levels and floors:** none. No floor exists for the m44 artifact's
  counter; the co-active floors in `severity.json` (m55 Medium, m53b High)
  are other artifacts' (as for Figure 3; owner decision below).
- **Known limits:** pooled over 2 / 3 / 2 seeds; the counter's scope (co-active
  only where Coupling B is also on) belongs in the caption (`submission.md`
  slot comment). The histogram bins are the committed ones (no finer
  binning exists in the JSON). Over-dispersion (CO-3) is not shown.
- **Metadata check:** passed.

### `out/img/fig06_comms.png`

- **Slot:** Figure 6 (§7).
- **What it plots:** (a) E2C² (M5.2): J for the free arm, J for the denied
  (pinned) arm with ±1 SE, and the predicted ½ + q/2, against κ_B; the shaded
  gap is labelled VoC_gated. (b) the M5.5 denial contrasts Δ = (δ = 0) −
  (δ = 1) at Medium, completion and survival, each with its registered bar
  (±2 × the floor sd on that card), hatched. (c, d) the runs behind (b):
  4 seeds at δ = 0, 4 at δ = 1, and the 4 identical-seed floor runs, with
  their means.
- **Sources:** (a) `R/phase5/m52/e2c2_sweep.json` → `sweep[*].{kappa_B,j_free,j_pinned,se_j_pinned,j_predicted}`
  (the report's "J_denied" column is `j_pinned`: `phase5_report.md:542-551`).
  (b) `R/phase5/m55/verdict.txt` (bars and contrasts, parsed);
  (c, d) `R/phase5/m55/eval_d{0.0,1.0}_s{0..3}.json` and
  `eval_floor_rep{1..4}.json` → `metrics.*.mean`. The script asserts the
  per-seed means reproduce the verdict's contrasts and the floor runs'
  sd reproduces `reproducibility_floor_medium.txt:7-8`.
- **Numbers stated:** Δ +0.0038 and −0.0143 (COM-4); "VoC_gated" label only
  (its 0 → 0.498 range is COM-1; the figure prints no VoC value); 4 seeds,
  4 floor runs (COM-4 "4 seeds"; METH-1's source for the floor runs).
  The bar values 0.0799 / 0.0260 are drawn, not printed (COM-4).
- **Interval levels and floors:** (a) ±1 SE as committed (the gate's own
  z-test is not redrawn). (b) the registered M5.5 bar is 2 × floor sd: the
  2σ form CLAUDE.md permits only for post-hoc floor grading, labelled so in
  the legend.
- **Known limits:** condition (iii) (COM-5, VOID) and the M5.3/M5.3b
  connectivity results (COM-2, COM-3) are not drawn. The figure carries no
  word "inert".
- **Metadata check:** passed.

### `out/img/fig07_floors.png`

- **Slot:** Figure 7 (§8; appendix C).
- **What it plots:** (a) Medium floor sd for completion and survival on two
  cards (M5.1e RTX 5090; M5.5 RTX PRO 6000), legend-labelled with their
  **code tree and config hash as A / B**, so the confound is in the figure;
  the completion ratio. (b) completion floor sd for ISO and JOINT at T = 500
  (M6.2) and T = 1000 (M6.2b), legend-labelled **box 1 / box 2**; the ratios.
  (c) M6.0: same-code GPU rerun comparisons that differed, per tree pairing.
- **Sources:** (a) `R/phase5/m51e/reproducibility_floor.txt:6-7` and
  `R/phase5/m55/reproducibility_floor_medium.txt:7-8`; the 4 + 4 rep evals
  (`m51e/eval_medium_rep{1..4}.json`, `m55/eval_floor_rep{1..4}.json`) are
  read only to assert the sds. Config hashes: each eval JSON's `config_hash`
  (they differ). (b) `P6/m62/floors.json` and `P6/m62b/floors.json` →
  `{iso,joint}.completion.{sd,values}`; `m62b_report.md:134-135`. (c)
  `P6/m60/m60_report.md:109-111` (table rows parsed and asserted).
- **Numbers stated:** 0.0145, 0.0399, 0.0129, 0.0130, 2.75× (METH-1);
  2.1×, 5.2× (METH-5); 0.0165, 0.0339, 0.0093, 0.0483 (**NEEDS LEDGER ROW**:
  `m62b_report.md:134-135`; T = 500 values also `m62/floors.json`
  `*.completion.sd`); 0 of 4, 1 of 4 (METH-2); 2 of 5 (**NEEDS LEDGER ROW**:
  `m60_report.md:111`); "4 identical runs", "8 identical runs"
  (`reproducibility_floor*.txt:1`; `floors.json` `n`; **NEEDS LEDGER ROW**
  for 8).
- **Interval levels:** none; floors are point sds (3 and 7 dof: the source
  files' own caveat, ±40 % at n = 4).
- **Known limits:** (a) card is confounded with code tree (METH-1's caveat)
  **and with config hash** (see "inconsistencies" in the hand-back). (b) run
  length is confounded with box (METH-5); "ordered by curriculum difficulty"
  is a hypothesis and is not in the figure. (c) the reference tree's
  "0 of 760 digests" (METH-2) is not drawn as a count; the trajectory-field
  row (0 of 13) is mentioned in the legend wording "no trajectory field".
- **Metadata check:** passed.

---

## Stage D: Figure 1 (environment schematic)

### `out/img/fig01_schematic.svg` and `out/img/fig01_schematic.png`

- **Slot:** Figure 1 (§3).
- **What it shows:** one environment step. Five numbered kernels in the
  Prop.-1 sampling order: (1) collapse c′ ~ T_C(c, x), agent load raises
  collapse probability; (2) hazard h′ ~ T_H(h, c, c′), fire CA with β;
  (3) smoke ρ′ = e^{−η}ρ + σ_s·1[h′ burning]; (4) agents x′ ~ T_X(x, a, h′, c′),
  fire and collapse kill, collapse blocks; (5) comms k′ ~ T_K(x′), link
  denial δ. **Coupling A** is drawn as the (orange, thick) arrow from
  collapse to hazard, labelled "c′ − c seeds ignitions, κ_A". **Coupling B**
  is the (blue, thick) arrow from smoke to the observation kernel, labelled
  "Beer–Lambert on ρ′, κ_B". **δ** enters the comms kernel from above,
  labelled "independent: no hazard input". Actions a enter the agents
  kernel. The observation box: o′_i ~ O^i_{κ_B}(· | x′, h′, ρ′, c′, k′),
  9 × 9 egocentric crop, drawn from the post-step state s′. The two
  couplings are also distinguished by position and label, so the figure
  reads in greyscale.
- **Sources:** `docs/theory_foundations.md` Def. 1 (factorization), Prop. 1
  (sequential composition, :125-142), Def. 5 (Coupling A, :274), Def. 6
  (Beer–Lambert, :332), Def. 7 (comms, T_K independent of h, :540);
  `CLAUDE.md` invariant #2; the implemented order `che/env/env.py:1-9` and
  `step()` (:296-357); the agent kernel's kill/block semantics
  `che/env/env.py:159-196`.
- **Numbers stated:** 9 × 9 crop (ENV-6). No other number.
- **Notation choice to confirm:** the agents kernel is written
  **T_X(x, a, h′, c′)**, as implemented (`env.py:4, :13`: "lethality/blocking
  are evaluated against the post-update fields"), and as Prop. 1's proof
  composes it (h′, c′ are already sampled when T_X runs). Def. 1's display
  and CLAUDE.md invariant #2 write T_X(x, a, h, c). The figure follows the
  code; the owner may prefer the theory doc's notation (owner decision below).
- **Known limits:** the reward (Def. 2: task variables and the cause-blind
  alive transition only) is not drawn; the slot does not ask for it. No
  structure/collapse rendering, no data.
- **Format:** matplotlib, text converted to paths in the SVG (no font
  dependency); the SVG's `<metadata>` block and generator comment are
  stripped. **Metadata check:** passed.

---

## Stage E: mechanism GIFs

### Selection rule (written 2026-10-10, BEFORE any render was made)

Fixed to choices already used by `paper/renders/2026-09-27/` (rule 9 of the
FIGURES brief). Nothing else is rendered, so nothing is chosen from a set.

- **Config:** `che/configs/theta_star_holdout.yaml` (θ\*: all elements on,
  held-out Medium β = 0.49). The JOINT checkpoint is evaluated cross-config
  through the harness's `--allow-hash` path, with the training hash read
  from the committed sidecar `paper/renders/2026-09-27/thetastar_joint_s1_T1000_ep0.json`
  (`allow_hash`), never typed by hand.
- **Episode:** key seed 0, with `che/scripts/render_episode.py`'s
  `rollout_frames` key discipline reproduced exactly (`split(key)` → reset
  key; per step `split(key, 3)` → action key, step key), so each mechanism
  render **is the same episode** as the committed GIF for the same policy.
  Asserted after the rollout: final alive, completion and return equal the
  committed sidecars (random: 12 / 12, 0.15625, 5.0; JOINT: 12 / 12,
  0.59375, 19.0). If they differ, nothing is written.
- **Policies, both, for both mechanisms (4 GIFs):** (i) the random policy;
  (ii) JOINT seed 1 at step 1000, archive
  `che/bench/results/phase6/g1_conf_5090/ckpt_joint_s1.tar.zst`, its sha256
  verified against `SHA256_CKPT.txt:73` before extraction into an empty
  scratch directory. All four are reported and none is withheld. **Which
  policy's version is placed is decided by a content-independent criterion
  only:** whether trained-policy episodes are shown at all (GIF slot 2, an
  owner decision). Actions are sampled stochastically (no `--greedy`), as the
  harness and the committed renders do.
- **Display:** every 2nd step (t = 0, 2, …, 256: 129 frames), 12 fps, as the
  committed renders. Static companion of each GIF: the frames at t = 0, 128
  and 256.
- **Mechanism A ("structure layer"), whole arena:** the hazard field
  (Fuel / Burning / Burnt), weak cells, collapsed cells, agents, and the
  **collapse-seeded ignitions**: cells lit by Coupling A since the previous
  shown frame are ringed, and every cell Coupling A has lit so far keeps a
  small persistent mark, so no seed is lost to frame skipping. Smoke is not
  overlaid (it would hide the structure layer). The per-cell seed mask is
  not exposed by `env.step`, so it is **recomputed with the step's own
  kernels and keys** (`structure_step`, `coupling_a_seed_mask`,
  `hazard_step`, `seed_ignitions`, the step key split three ways as in
  `env.py:298`) and **asserted bitwise** against `env.step`'s returned
  structure and hazard at every step, and its count against
  `info["seeded_ignitions"]`. If any assertion fails, the GIF is not built
  and that is reported instead.
- **Mechanism B ("agent's-eye view"):** **agent index 0**, fixed by index
  before rendering, not by anything it encounters. Three panels: the arena
  with agent 0's 9 × 9 crop outlined; agent 0's crop **without** attenuation
  (the same post-step state through the same observation kernel with
  κ_B = 0 in `theta_live` only, which makes τ = 1, so every cell is
  revealed); agent 0's crop **as received** (the obs `env.step` returned at
  κ_B = 1.0), unseen cells drawn as unseen. Asserted: wherever the received
  crop's visibility plane is 1, its content equals the unattenuated crop's.
  If agent 0 sees little fire in this episode, the GIF shows that; no other
  agent is rendered without an owner ruling.
- **Reading rules (as the 2026-09-27 README):** these illustrate, they grade
  nothing; each is one episode; captions must not present them as evidence.

### Results under the rule (rendered after the rule above was written)

Renderer: `paper/figures/src/gif_mechanisms.py` (imports `che` read-only;
`che/scripts/render_episode.py` untouched). Run from the repo root as the
committed renders were: `OMP/MKL/OPENBLAS_NUM_THREADS=4`,
`XLA_FLAGS=--xla_cpu_multi_thread_eigen=false`, `taskset -c 0-3 nice -n 15`.
Archive check: `sha256(ckpt_joint_s1.tar.zst)` =
`64c49ef8fc8c28b6234b4e3ed03812967f15beb49eadcbb31feff5c38ec19e61`, equal to
`SHA256_CKPT.txt:73`; members listed first (no absolute or `..` paths),
extracted to a new empty scratch directory outside the repo; restored at
step 1000 (asserted).

**Every assertion of the rule held, for both policies:** each rollout is the
committed episode (random: 12 / 12 alive, completion 0.15625, return 5.0;
JOINT: 12 / 12, 0.59375, 19.0, equal to the committed sidecars); at all 256
steps the recomputed structure and hazard equal `env.step`'s bitwise and the
recomputed seed count equals `info["seeded_ignitions"]`; at all 257 frames
agent 0's received crop equals the unattenuated crop wherever it is visible.
A clean rebuild reproduced every GIF and PNG byte-for-byte.

| file | what | episode facts (from the rollout) |
|---|---|---|
| `out/gif/mechA_structure_random_ep0.gif` + `out/img/..._static.png` | Coupling A structure layer, random policy | 11 collapsed cells at t = 256; 7 Coupling-A ignitions |
| `out/gif/mechA_structure_joint_s1_T1000_ep0.gif` + `_static.png` | same, JOINT seed 1, T = 1000 | 11 collapsed; 7 Coupling-A ignitions |
| `out/gif/mechB_agent0_view_random_ep0.gif` + `_static.png` | agent 0's crop without / with attenuation, random policy | agent 0: **0** steps with fire in its crop, **0** steps with any masked cell |
| `out/gif/mechB_agent0_view_joint_s1_T1000_ep0.gif` + `_static.png` | same, JOINT seed 1 | agent 0: **0** and **0** |

Sizes: 441–452 KB (A), 840–912 KB (B); 129 frames at 12 fps; A 594 × 693 px,
B 1024 × 400 px. The episode facts above are rollout output, not ledger
numbers; the GIFs state only t, the policy, and running counts of collapsed
cells, Coupling-A ignitions, burning cells and unseen crop cells. **No
survivor tally:** a first render carried "alive N / 12" in the structure
GIF; it was removed and both A GIFs re-rendered (same rule, same episodes,
presentation only) after reading the FIGURES FIRST ruling ("never side by
side and with no survivor tally"). Agent 0's own state (alive / disabled) is
still printed under its crop, since it explains a frozen crop.

**Mechanism A is built faithfully.** Collapse-seeded ignitions are exactly
the cells Coupling A lit (bitwise-checked), not inferred from the picture.

**Mechanism B is built, but under the declared rule it does not show
Coupling B acting.** In both pre-declared episodes agent 0 never has a
burning cell in its 9 × 9 crop and never has a masked cell, so the
"without" and "as received" panels are identical in every frame. That is
what the rule produces, and it is reported, not worked around: no other
agent or episode was rendered. (Crop cells beyond the arena edge, which the
observation pads with 0, are drawn as "outside the arena" from agent 0's
position so they are not misread as fuel.) Owner decision below.

Known limits: the structure GIF does not overlay smoke; the agent's-eye GIF
draws the observation planes, not what a network "sees" in its weights; the
end-of-episode wall drift (spine §10 item 6) is visible in both; weak cells
are the per-episode terrain mask, so they are identical across policies.
The committed 2026-09-27 GIFs were not touched.

**Metadata check:** passed (GIF blocks: NETSCAPE2.0 loop, graphic control,
image, trailer; no comment or other application block).

---

## Index of outputs

| file | slot | static companion |
|---|---|---|
| `out/img/fig01_schematic.svg`, `.png` | Figure 1 | itself |
| `out/img/fig02_calibration.png`, `out/html/fig02_calibration.html` | Figure 2 | the PNG |
| `out/img/fig03_coupling_a.png` | Figure 3 | — |
| `out/img/fig04_coupling_b.png` | Figure 4 | — |
| `out/img/fig05_coactive.png` | Figure 5 | — |
| `out/img/fig06_comms.png` | Figure 6 | — |
| `out/img/fig07_floors.png` | Figure 7 | — |
| `out/img/fig08_gamma_contrasts.png`, `out/html/fig08_gamma_contrasts.html` | Figure 8 | the PNG (contrast view) and `fig08b_gamma_arms_per_seed.png` (per-seed view) |
| `out/img/fig09_gamma_t.png`, `out/html/fig09_gamma_t.html` | Figure 9 | the PNG; `fig09b_gamma_t_single_card.png` is the single-card companion |
| `out/img/fig10_secondary.png`, `out/html/fig10_secondary.html` | Figure 10 | the PNG (survival prediction panel; the HTML's completion view has no static) |
| `out/gif/mechA_*`, `out/gif/mechB_*` | GIF candidates (§5, §6) | `out/img/mech*_static.png` |

Interactive pages' natural height at 800 px width, table view collapsed:
Fig 2 ≈ 470 px, Fig 8 ≈ 420 px, Fig 9 ≈ 400 px, Fig 10 ≈ 720 px (the
iframe scrolls when a table view is opened). In a same-origin iframe they
follow the embedding page's `data-theme`; opened alone, the OS setting.

## Metadata check (double-blind, rule 7)

`paper/figures/src/check_metadata.py`, run after the final build over all
25 files in `out/`: **0 failures.** PNG: every file carries only IHDR,
pHYs, IDAT, IEND (no tEXt / zTXt / iTXt / eXIf / tIME). GIF: no comment or
non-loop application block. All files, text and binary: no account, owner
or host name, no home or scratch path, no repo host, no e-mail, no IPv4, no
GPU UUID, no rental host, and no 7–40-character prefix of any of the
repository's 212 commit hashes (the forbidden list is built at run time
from the environment and `git rev-list --all`, so it is written nowhere).
The SVG's generator comment, `<metadata>` block and DOCTYPE are stripped;
its only URIs are the SVG/XLink namespace identifiers. The HTML files
reference no URL at all except the SVG namespace identifier in
`createElementNS`. The scripts in `src/` are not outputs: `gif_mechanisms.py`
reads the training hash from the committed sidecar rather than containing it.

---

## Owner decisions needed

1. **Every slot:** whether each candidate appears, where (main text or
   appendix), and its caption. In particular: Figure 8's k = 60 prefix row
   (keep only if §9 cites RES-3); whether the "confirmatory family / outside
   the confirmatory family" labels and the REJECT / null column stay;
   Figure 10 in §9.2 or appendix I.
2. **Verdict labels in figures.** Figure 9's panels carry the registered
   string verbatim ("rule (iv): sign unstable over the final half"),
   Figure 8 carries "REJECT" / "null", Figure 10 "UNDERPOWERED" and "VOID",
   as FIGURES FIRST item 3 allows. If the owner wants verdicts in captions
   only, drop them.
3. **Figure 2 and O-2.** The β̂_c band is the lock's value; its estimator
   has no committed artifact. Options: keep the band (with the caption
   naming the lock), mark the committed crossing estimates instead
   (`estimates.json`), or discharge O-2 first.
4. **Cross-artifact floors (Figures 3 and 5).** The only seeded-ignition and
   co-active floors were measured on m55 / m53b, not on m44 or m35. Not
   drawn, by the per-artifact amendment. The owner may rule otherwise.
5. **Figure 10, SEC-3.** The plane's predicted ISO-4 − ISO (+0.0079) is not
   drawn because no interval is committed for it. Adding it needs a ledger
   row for a derived interval (γ_n's CI × (−1/3)) first.
6. **Figure 1 notation:** T_X(x, a, h′, c′) as implemented, or
   T_X(x, a, h, c) as in Def. 1 and CLAUDE.md invariant #2.
7. **Mechanism GIFs.** (a) Which policy's version of each to place: by the
   rule, only by the content-independent GIF-slot-2 decision (are trained
   episodes shown at all?). (b) **Mechanism B shows no attenuation** under
   the declared rule. Options: drop it; or rule a new selection *before*
   anything else is rendered. The builder's labelled recommendation: render
   **all 12 agents' crops** of the same episode in one panel grid (choosing
   nothing), rather than a rule that picks the agent by what it encountered.
8. **NEEDS LEDGER ROW items** (listed per figure above, collected in the
   hand-back) need rows before any of them is quoted in a caption or text.
9. **Captions must carry** what figures deliberately do not say: Figure 4's
   floor is per run (a two-run contrast's floor is wider); Figure 7's
   confounds (card with code tree and config hash; run length with box);
   Figure 5's counter scope; the GIF reading rules (one episode,
   illustrates, grades nothing).

## Not built, and why

- **R_L logistic centres and any β̂_c estimate (Figure 2):** ledger O-2, no
  committed artifact; computing one is a new estimator.
- **The CA-3 Prop.-3 handshake (Figure 3):** report text only, no committed
  data file.
- **The mediation (dose) figure:** VOID by the instrument's own verdict
  ("the dose figure has no x-axis", SEC-7).
- **Interactive versions of Figures 3–7:** judged to add nothing a static
  panel does not (each has 3–12 marks); Figure 2 got one (curves by L).
- **A Coupling-B GIF that shows masking:** the rule-bound render shows none
  (above); nothing else was rendered.
- **Not in any slot, so not built:** the T = 2000 curves (RES-15), the High
  readout (RES-14), Figure 4's completion sign flip (CB-8).
- **The 2026-09-27 GIFs:** left untouched, per rule 9.
- **Nothing was skipped for a missing dependency:** everything used numpy,
  matplotlib, Pillow, jax and `che`.
