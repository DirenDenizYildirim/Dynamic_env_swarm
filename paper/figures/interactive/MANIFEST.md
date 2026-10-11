# Interactive figures: manifest

Built 2026-10-10 under the decision log's **FIGURES**, its **ADDENDUM** and
**FIGURES FIRST** entries, after `DESIGN.md` (written first). **Candidates,
not placements**: nothing here is in `paper/beyond_pdf/assets/`; the owner
decides at each section step. Captions are the owner's; the alt texts below
are proposals.

**Conventions.** `R/` = `che/bench/results/`; `P6/` = `R/phase6/`. A number
**stated** in a figure (text on the figure, in a tooltip or a table view) is
listed with its ledger row or, where none exists, under **NEEDS LEDGER ROW**
and is **not shown** (the builders route every stated number through
`src/ledger.py`; flipping `SHOW_PENDING` is the only change once rows exist).
Plotted positions read from committed files are data. Every builder asserts
its committed values against the ledger's printed values before drawing.

**Self-containment.** Each HTML file is one document: inline CSS, inline
vanilla JS, inline SVG/canvas, inline data (`<script type="application/json">`).
No external URL, script, font, library or network request. Each file follows
the host page's `data-theme` when same-origin (al-folio), else the OS theme;
never autoplays; honours `prefers-reduced-motion`; hides its controls under
`@media print`; sizes its own iframe when same-origin; every control is a
native button or range with a visible focus ring; every chart has a table
view (`<details>`).

**Visual language.** `DESIGN.md` §3. Episode imagery is identical in palette
and glyphs to the restyled GIFs in `paper/renders/2026-10-10/` (builder's
audit item 5). Colour means stressor identity (Coupling A violet, Coupling B
magenta, both with textures) or map state; statistics are ink and grey.

**Revision 2026-10-10 (evening), after FIGURE BATCH RULINGS and OPENING AND
§1 REOPENED.** Changed: the composer's "as certified" removed (B8); Γ(t)'s
intervals at t ≠ 1000 labelled descriptive (B8); the simplex pairs each
plane prediction with its measured contrast (B10); **new compact opening
ladder (F2b)** for §1; the hero explorer checked for the opening slot (no
change needed). Code: every inline CSS/HTML/JS asset moved verbatim into
`src/templates/` (read at build time, still inlined into each output);
`ruff check paper/figures/interactive/src` is clean (B023, B905, B007, F841,
I001, E501 fixed). **Identity of the rebuild:** after the template move and
the lint fixes, all 34 outputs (10 HTML, 10 PNG, 14 data JSON) were
byte-identical to the previous build except two PNGs, `ladder_registered_readings.png`
and `gamma_t_final_half.png`: the B023 findings there were a real bug
(late-bound `mt` in the tick formatter gave the completion axis three
decimals instead of two); fixed. After the intended changes, the outputs
that differ from the previous build are exactly: composer HTML+PNG (wording;
data payload identical), Γ(t) HTML+PNG (labels; data payload identical),
simplex HTML+PNG (prediction rows regrouped; all other payload fields
identical), the new opening ladder, and `output_checks.json`. Explorer HTML,
PNGs, state digests and codec checks are unchanged; the node decoder check
still passes on all three.

**Rebuild** (from the repo root; CPU only, thread-capped):

    export OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 XLA_FLAGS=--xla_cpu_multi_thread_eigen=false
    nice -n 15 uv run python paper/figures/interactive/src/extract_episodes.py --scratch <scratch dir>   # JAX, ~1 min
    for b in build_explorer build_ladder build_opening_ladder build_composer build_gamma_t build_simplex \
             build_severity build_floors build_coupling_a static_companions check_outputs; do
      nice -n 15 uv run python paper/figures/interactive/src/$b.py; done
    for s in thetastar_random_seed0 thetastar_iso_s1_T1000_ep0 thetastar_joint_s1_T1000_ep0; do
      node paper/figures/interactive/src/test_explorer_decode.js \
        paper/figures/interactive/out/html/explorer_$s.html paper/figures/interactive/out/data/${s}_codec_check.json; done

`build_severity.py` runs its own JAX rollouts the first time (no `--scratch`
needed). `out/data/` is provenance (digests, codec checks, pending lists,
frame arrays); **none of it goes into `assets/`**.

**Embedding** (`KIT_NOTES.md` §S1.5): copy the HTML to
`assets/html/submission/` and place it with
`<iframe src="{{ 'assets/html/submission/<file>' | relative_url }}" width="100%" height="<h>" style="border:none" title="<title>"></iframe>`,
with the PNG companion beside it via `figure.html`. Heights below are for a
~900 px column; the file resizes its own iframe when served same-origin.

---

## F1. Episode explorer (hero), one file per episode

| file | size | static companion | size |
|---|---|---|---|
| `out/html/explorer_thetastar_random_seed0.html` | 118 KB | `out/img/explorer_thetastar_random_seed0_static.png` | 134 KB |
| `out/html/explorer_thetastar_iso_s1_T1000_ep0.html` | 171 KB | `out/img/explorer_thetastar_iso_s1_T1000_ep0_static.png` | 136 KB |
| `out/html/explorer_thetastar_joint_s1_T1000_ep0.html` | 116 KB | `out/img/explorer_thetastar_joint_s1_T1000_ep0_static.png` | 129 KB |

- **Anchors:** §3 (random-policy file); deep links for §5 and §6 through the
  URL hash `#t=<0..256>&agent=<1..12|none>&layers=fire,smoke,weak,coll,seed,food,agents`
  (each placed deep link needs its own selection rule first). **ISO and JOINT
  files:** GIF slot 2 is the owner's pending decision; they are separate
  files, never side by side, and carry no tally.
- **Shows:** all 257 states (t = 0…256) of one episode. Layers: fire state,
  smoke density ρ (environment field), weak floor, collapsed floor,
  collapse-seeded ignitions (Coupling A; ring at the step, small ring after),
  food, agents (alive, dead). Event track of collapse events and seeded
  ignitions with prev/next jumps. Selecting an agent (click, 1–9, or buttons)
  shows three 9 × 9 panels at that step: **observation as produced** (obs v3
  content planes; masked cells solid grey with "?"; out-of-arena cells read as
  zero planes, as the env produces them), **state of the same cells** (dead
  agents and the arena edge visible), **P(seen) = τ** (Beer–Lambert
  transmittance, magenta ramp). Hover: cell state, ρ and τ readouts (state
  values, not results). No alive count, completion, return, score or
  comparison anywhere.
- **Controls / keys:** play/pause (space), step (←/→, shift ×10), scrubber,
  speed 0.5/1/2/4×, `[`/`]` events, 1–9 agents. Default view (DESIGN §6 rule
  2, written before rendering): t = 128 with the lowest-index agent alive at
  t = 128 whose observation has an unseen cell, else the lowest-index alive
  agent: **random → agent 7, ISO → agent 5, JOINT → agent 1** (JOINT has no
  agent with an unseen cell at t = 128, so the fallback applied).
- **Data and identity** (`src/extract_episodes.py`): θ\* =
  `che/configs/theta_star_holdout.yaml`, episode key `PRNGKey(0)`,
  stochastic actions; checkpoints `P6/g1_conf_5090/ckpt_{iso,joint}_s1.tar.zst`,
  sha256 verified against `SHA256_CKPT.txt` (0fc9fd0c…, 64c49ef8…), restored at
  step 1000 with `--allow-hash` b63fc2d6764c7ffe / da6617b402b08b9b. Checks
  run, all passed:
  1. sha256 of (hazard, smoke, food, agent_pos, agent_alive) at **every one
     of 257 states equals** `che.scripts.render_episode.rollout_frames`
     (called unmodified), for all three episodes (`out/data/*_digests.json`);
  2. final alive count, completion and return equal the committed
     2026-09-27 render JSONs;
  3. collapse-seeded ignition cells recovered with the env's own kernels
     reproduce h′ and c′ bitwise and `info["seeded_ignitions"]` /
     `info["collapse_events"]` exactly at every step (random 11 collapse
     events / 7 seeded ignitions; ISO 12 / 7; JOINT 11 / 7);
  4. every observation equals (true crop × reveal, reveal), and re-drawing
     the reveal from the step's obs stream with the env's `transmittance`
     reproduces the visibility plane, so the stored τ is the τ the draw used;
  5. encoding (zero-run RLE, cell lists, packed bits, base64) round-trips in
     Python, and **the page's own JS decoder, run under node on the page's
     own data, reproduces every array's sha256** (`src/test_explorer_decode.js`).
  Smoke is stored as round(ρ·255) (ρ ≤ 1 asserted), τ as round(τ·255).
- **Stated numbers:** β 0.49 (CAL-3), κ_A 0.06 (CA-1), κ_B 1.0 (CB-1),
  δ 1.0 (COM-6), 64 × 64, 12 agents, 9 × 9, horizon 256 (ENV-6); t values;
  hover readouts of ρ and τ are per-cell state of the shown episode.
- **Static companion:** maps at t = 0, 128, 256 (the 2026-09-27 strip
  frames) + the three panels for the default agent at t = 128, with legend.
- **Iframe height:** 720 (desktop); stacks to one column under 700 px.
- **Alt text (proposal):** "Interactive player of one episode on a 64 by 64
  grid: fire state, smoke density, weak and collapsed floor, collapse-seeded
  ignitions, food and twelve agents over 256 steps, with one selected agent's
  9 by 9 observation, the true state of the same cells, and the probability
  each cell was seen."
- **Opening slot (OPENING AND §1 REOPENED, item 2), checked 2026-10-10:**
  at rest the random-policy file shows t = 128 with agent 7 and its three
  panels selected, paused (no autoplay; playback starts only on the reader's
  press, also under `prefers-reduced-motion`). At 360 px width the layout
  stacks to one column with no clipping (map ~330 px; layer and agent pills
  wrap). Iframe height at phone width ≈ 1100 (self-sizing when same-origin).
  **Visible labels and their sources:** "random policy" (selection rule,
  `paper/renders/2026-09-27/README.md`); θ\* (β 0.49 CAL-3, κ_A 0.06 CA-1,
  κ_B 1.0 CB-1, δ 1.0 COM-6); 64 × 64 cells, 12 agents, 9 × 9 cells,
  t = k / 256 (ENV-6); "episode key 0" (README selection rule, file + key;
  NEEDS LEDGER ROW if a row is wanted for identifiers); speeds and agent
  numbers are interface labels; the hover readouts of ρ and τ are per-cell
  state of the shown episode (not results; NEEDS LEDGER ROW if the owner
  wants them treated as stated numbers, else they can be removed).
- **Policy label:** plain ("random policy", "ISO policy · training seed 1 ·
  update 1000", …); `build_explorer.py --no-label` strips it.

## F2. Registered-readings ladder

`out/html/ladder_registered_readings.html` (24 KB) ·
`out/img/ladder_registered_readings.png` (258 KB) · iframe height 1000.

- **Anchors:** §9.2; optional collapsed first rung under the abstract.
- **Shows:** both co-primaries, rows in registered order Γ (k = 72) → [Γ,
  k = 60 prefix, toggle] → Γ₄ → Γ₄′ → B̂. Stepper (1–4, ←/→, show all;
  previous rungs dimmed, later rungs "not yet read"). Each row: identity, k,
  card/unit, registration date; **verdict chip first**, then estimate and
  Šidák 95 % CI; whisker; MDE80 band (toggle) on the confirmatory family and
  on Γ₄ completion only; floor (stipple, ±1 floor-basis sd(Γ)) on Γ only.
  Rung 2 carries the registered consequences: survival **"does not survive
  the inert-share correction"**, completion **"second exclusion bound,
  X₄ = 0.0488"**. **B̂ carries no chip and no z** (no registered test; builder's
  audit item 1). The k = 60 row carries **UNDERPOWERED** before its verdict.
  Footnote: k = 72 is the recorded deviation (cap 60 raised 2026-09-22).
- **Sources:** `P6/unblind/unblind.json` (`primary`, `prefix`,
  `beat_reproducibility`), `P6/post_unblind_analysis/post_gamma4_t2000.json`
  (`gamma4.per_metric.*`, labels `DOES_NOT_SURVIVE`, `SECOND_EXCLUSION`),
  `P6/secondary/secondary.json` (`replicate.*.gamma4_prime`).
- **Stated numbers → ledger:** Γ RES-1, RES-2 (z, CI, X completion 0.0329);
  k = 60 RES-3 (estimates, z); Γ₄ RES-6 (survival estimate, CI, z;
  completion estimate; X₄ 0.0488); Γ₄′ RES-8; B̂ RES-7 (estimates; survival
  CI); k 72 / 20 / 60 DES-3, DES-13, DES-1; m = 2, T\* = 1000 DES-13; dates
  DES-15, DES-3; units HW-4. Floor values: plotted only.
- **Alt text (proposal):** "Two forest plots, completion and survival, of
  the registered contrasts in order: joint minus isolated training, its
  60-seed prefix, joint minus ISO-4, joint minus a same-card replicate arm,
  and ISO-4 minus isolated, each with its Šidák-corrected interval and its
  registered verdict."

## F2b. Compact opening ladder (new, for §1)

`out/html/opening_ladder.html` (15 KB) · `out/img/opening_ladder.png` (136 KB) ·
iframe height ≈ 400 in a ~700 px text column (≈ 760 at phone width).

- **Anchors:** §1 (OPENING AND §1 REOPENED, item 3). Built from the full
  ladder's own data (`build_ladder.build_data()`): same values, assertions
  and ledger routing. **Only Γ (k = 72) and Γ₄, both co-primaries, no
  toggles**, so it can never show Γ without Γ₄ (A1). Survival block first
  (the abstract's order), then completion; per block, Γ and Γ₄ rows on one
  shared axis. Verdict chips first: Γ survival REJECT; Γ completion null;
  Γ₄ survival null with **"does not survive the inert-share correction"**
  on the line directly under it, next to the Γ survival gain; Γ₄ completion
  null with **"second exclusion bound, X₄ = 0.0488"**. ISO-4 marked "sensitivity
  arm, outside the confirmatory family · cross-unit", k 72 / 20. A
  link-style label "full ladder: §9.2". Footnote: ISO-4's definition and
  registration date; k = 72 as the recorded deviation.
- **Every number shown → ledger:** Γ survival +0.0096 [+0.0047, +0.0144]
  RES-2; Γ completion −0.0173 [−0.0412, +0.0066] RES-1; Γ₄ survival −0.0003
  [−0.0068, +0.0063] RES-6; Γ₄ completion −0.0126 RES-6 (its CI
  [−0.0481, +0.0228]: **NEEDS LEDGER ROW**, hidden, whisker drawn); X₄ 0.0488
  RES-6; k 72 / 72 DES-3, DES-13; k 72 / 20 DES-13, DES-15; m = 2, T\* = 1000
  DES-13; "unit 1", "cross-unit" HW-4; 2026-09-18 DES-15; cap 60 and
  2026-09-22 DES-1, DES-3; axis ticks are graduations.
- **Alt text (proposal):** "Joint minus isolated training and joint minus
  ISO-4, for survival and completion, each with its Šidák-corrected interval
  and registered verdict; the survival gain is shown beside the ISO-4
  contrast, labelled does not survive the inert-share correction."

## F3. Training-mixture composer

`out/html/composer_training_mixtures.html` (19 KB) ·
`out/img/composer_training_mixtures.png` (125 KB) · iframe height 430.

- **Anchors:** §9.1; the §1 paragraph on the active share.
- **Shows:** ISO, ISO-4, JOINT as 100 % bars of episode types (A only, B
  only, A + B together, fire-only = δ-only), textures 45°/135°/crosshatch;
  per-stressor marginals A, B and the active share beneath, aligned across
  arms (ISO-4 and JOINT share active share 1; marginals 0.5 vs 1.0).
  Switches: "δ inert under a frozen random-projection encoder at this scale"
  (default; "as certified" removed everywhere, B8) vs "nominal: δ counted";
  split by β 0.43 / 0.70. Hover: config components and weights. **No slider,
  no prediction.**
- **Sources:** `che/configs/p6_iso.yaml`, `p6_iso4.yaml`, `p6_joint.yaml`
  (`mixture.components`, via `load_config`).
- **Every number shown → ledger:** segment shares ISO 1/3 · 1/3 · 1/3 (A,
  B: DES-7; fire-only: DES-8), ISO-4 1/2 · 1/2 (DES-14), JOINT 1 (DES-7);
  marginals ISO A 1/3, B 1/3 and JOINT A 1, B 1 (DES-7), ISO-4 A 1/2, B 1/2
  (DES-14); active share 2/3 / 1 / 1 (DES-14); "3× ISO" (DES-7), "2× ISO-4"
  (DES-14); β 0.43 / 0.70 (CAL-3); tooltip κ_A 0.06 (CA-1), κ_B 1.0
  (CB-1), δ 1.0 (COM-6), 0 values (configs). **NEEDS LEDGER ROW:** the
  per-component weights 1/6, 1/4, 1/2 shown with the severity split and in
  tooltips/table (source `che/configs/p6_{iso,iso4,joint}.yaml`
  `mixture.components[*].weight`, normalised); the nominal-view ISO active
  share 1 (source `p6_iso.yaml:7`, "no-element 0.0000"). Axis ticks 0,
  1/3, 1/2, 2/3, 1 are graduations.
- **Alt text (proposal):** "Stacked bars of the three training mixtures by
  episode type, with each arm's per-stressor frequencies and the share of
  episodes that carry an active stressor."

## F4. Γ(t) over the final half

`out/html/gamma_t_final_half.html` (19 KB) · `out/img/gamma_t_final_half.png`
(125 KB) · iframe height 480.

- **Shows, first:** "sign unstable over the final half" (both co-primaries),
  then the 11-sign string with disagreeing checkpoints ringed; points with
  Šidák whiskers, **no connecting line, no trend line**; a bracket over
  t = 500–950 labelled "descriptive intervals (no registered test at
  t ≠ T\*)" and "T\* registered" at 1000, thin whiskers for the descriptive
  intervals and a thick one for the registered Γ (B8); floor at T\* only;
  toggle for the single-card curve (t = 1000 re-evaluated on the
  post-unblind card, hollow marker). Card note under the plot.
- **Sources:** `P6/post_unblind_analysis/post_evalfloor_gamma_t_high.json`
  (`gamma_t.points`, `gamma_t.verdict`, `gamma_t.cross_card_T_star`); floor
  `P6/unblind/unblind.json`. Asserted: the committed signs, stability flags
  and disagreeing checkpoints match the points.
- **Stated numbers → ledger:** signs RES-11; t = 1000 RES-1/RES-2;
  survival t = 900/950 estimates RES-12; completion t = 750 RES-13; 11
  checkpoints, k = 72, m = 2 DES-13.
- **Alt text (proposal):** "Eleven checkpoints from update 500 to 1000 of
  the joint-minus-isolated difference in completion and in survival, each
  with its Šidák interval and its sign, labelled sign unstable over the final
  half."

## F5. Secondary simplex

`out/html/simplex_secondary.html` (28 KB) · `out/img/simplex_secondary.png`
(220 KB) · iframe height 820.

- **Shows:** chips "secondary", "non-verdict-bearing", "95 %, not
  family-corrected", "knee: UNDERPOWERED", "mediation: VOID". Left: the
  training simplex in (p, n) with iso-marginal lines (m = 1/3, 0.4, 0.5),
  the sweep and identification arms, the sampled region, ISO, ISO-4 (=
  sweep_c50_p000's mixture) and JOINT at m = 1 outside it; arm means against
  p with the committed plane fit as grey ticks (no numbers). Right:
  secondary estimates (95 %), then the plane's predictions against the
  measured contrasts, as two labelled pairs (B10): "ISO-4 − ISO: plane
  prediction from γ_n, measured B̂" (SEC-3 +0.0079 beside RES-7 +0.0098
  [+0.0033, +0.0163]) and "JOINT − ISO-4: plane prediction from γ_p,
  measured Γ₄ and Γ₄′" (SEC-4 ≈ +0.033 with γ_p's interval [+0.0137,
  +0.0502] from SEC-1, beside RES-6 and RES-8). Completion shows the γ_p pair
  only (no ledgered γ_n prediction for completion).
  Metric switch survival | completion; prediction toggle.
- **Sources:** `P6/secondary/secondary.json` (`design`, `metrics.*`,
  `mediation`, `replicate`); `P6/post_unblind_analysis/post_gamma4_t2000.json`.
  Asserted: m = (1 + p − n)/2 for every arm.
- **Stated numbers → ledger:** survival rows SEC-1, SEC-2, SEC-3, SEC-4,
  SEC-5; UNDERPOWERED SEC-6; VOID SEC-7; Γ₄, Γ₄′, B̂ RES-6, RES-8, RES-7
  (completion: estimates only); geometry DES-9, DES-8, DES-14, DES-7; k = 20
  DES-13; arm (p, n) values `R/phase6/secondary/secondary.md:9-16`.
- **Alt text (proposal):** "A triangle of training mixtures by share of
  both-stressor and fire-only episodes, locating the secondary arms, ISO,
  ISO-4 and JOINT, beside the secondary estimates and the plane's predicted
  contrasts next to the measured ones."

## F6a. Severity explorer

`out/html/severity_explorer.html` (175 KB) · `out/img/severity_explorer.png`
(140 KB) · iframe height 520.

- **Anchors:** §4. **Shows:** P_span against β at L = 32/48/64 with ±1 SE
  (committed estimator output), the three locked levels as rules, β_c(64)
  marked; **no R_L logistic centre and no β̂_c band** (O-2). A synchronized
  three-panel **illustrative** render at β 0.43/0.49/0.70 (hazard + smoke
  layers only), one scrubber; click a panel to highlight its level.
- **Selection rule** (DESIGN §6 rule 3, written before rendering):
  `rollout_frames` on `che/configs/severity_{low,medium,high}.yaml`, random
  policy, `PRNGKey(0)`; these configs have κ_A 0.06, κ_B 1.0, δ 0, as the
  subtitle says. Hashes of the rendered arrays: `out/data/severity_*_check.json`.
- **Sources:** `R/phase2/estimates.npz` (`betas`, `p_span_L*`,
  `p_span_se_L*`, `beta_half`). **Stated numbers:** CAL-3 (levels, P_span,
  burnt fraction, labelled "calibration … no agents"), CAL-4 (0.486); κ
  values CA-1, CB-1; δ 0 from the configs.
- **Alt text (proposal):** "Spanning probability of a centre ignition
  against ignition probability for three grid sizes, with the three locked
  severities marked, beside one illustrative fire episode at each severity."

## F6b. Coupling A explorer

`out/html/coupling_a_explorer.html` (19 KB) ·
`out/img/coupling_a_explorer.png` (182 KB) · iframe height 680.

- **Anchors:** §5. **Shows:** seeded ignitions per episode by severity
  (m44 κ_B 1.0 arm and m35 κ_A on arm, min–max over seeds, Low/High ratios);
  near-agent share for all nine cells with the [0.164, 0.203] range; **the
  two Prop. 3 runs in separate panels**: the L = 64 sweep (plot, committed
  through-origin fit) and the L = 32 matched-reference handshake (values
  only: it has no committed data file).
- **Sources:** `R/e1/severity/severity.json` (`grids.m44.cells`,
  `grids.m35.cells`); `R/phase3/m33/prop3_L64.json`. **Stated numbers:**
  CA-4, CA-5, CA-6, CA-2, CA-3; β levels CAL-3.
- **Alt text (proposal):** "Collapse-seeded ignitions per episode at three
  severities for two trained grids, the share of them near agents, and the
  two Proposition 3 handshake runs shown separately."

## F6c. Floors explorer

`out/html/floors_explorer.html` (18 KB) · `out/img/floors_explorer.png`
(192 KB) · iframe height 460.

- **Anchors:** §8. Tabs: per card (and tree, and config); per artifact; per
  run length; the grid against its floor. **Each panel states its confound
  on the figure:** METH-1 "card, code tree and config all differ between the
  two runs (M5.5 records R_comm 16; M5.1e predates the R_comm lock)"
  (builder's audit item 3); METH-5 "run length and box both differ".
- **Sources:** `R/phase5/m51e/reproducibility_floor.txt`,
  `R/phase5/m55/reproducibility_floor_medium.txt`, cards
  `R/phase5/phase5_report.md:1011-1014`; `P6/m60/m60_report.md` (comparison
  table); `P6/m62/floors.json`, `P6/m62b/floors.json` (per-run values);
  `P6/unblind/unblind.json` `beat_reproducibility`.
- **Stated numbers:** METH-1, METH-2, METH-5, HW-1, k = 72 (DES-13).
- **Alt text (proposal):** "Reproducibility floors on two cards, rerun
  comparisons of two code trees, floor growth from 500 to 1000 updates, and
  the confirmatory grid's seed dispersion against its floor, each with its
  confound stated."

---

## NEEDS LEDGER ROW (computed in the builders; hidden until a row exists)

Machine-readable lists: `out/data/{ladder,gamma_t,simplex}_pending.json`
(figure, what, value, committed source). In summary:

| figure | numbers | committed source |
|---|---|---|
| F2 | Γ survival X 0.0066; k = 60 Šidák CIs [−0.0486, +0.0052], [+0.0054, +0.0155] and X 0.0370 / 0.0069; Γ₄ completion CI [−0.0481, +0.0228] and z −0.80; Γ₄′ completion CI [−0.0616, +0.0122] and z −1.50; B̂ completion CI [−0.0405, +0.0312] | `unblind/report.md:12, :21-22`; `post_gamma4_t2000.md:12-13`; `secondary.md:52` |
| F4 | every Γ(t) estimate and Šidák CI at t ≠ 1000 not covered by RES-12/RES-13 (36 values), the survival CIs at t = 900, 950, and the single-card t = 1000 estimates and CIs | `post_evalfloor_gamma_t_high.md:26-36, :44-54, :69-70`; JSON `gamma_t.cross_card_T_star.*.gamma_post_card_T_star` |
| F5 | completion: dose slope −0.0251 [−0.0943, +0.0412]; endpoint −0.0097 [−0.0482, +0.0287]; γ_p +0.0269 [−0.0675, +0.1245]; γ_n −0.0652 [−0.1534, +0.0242]; bound −0.0326 [−0.0767, +0.0121]; prediction γ_p × 1 = +0.0269 (DERIVED as SEC-4); Γ₄ and Γ₄′ completion CIs | `secondary.md:25-28, :52`; `post_gamma4_t2000.md:12` |
| F6a, F6b, F6c | sample sizes (512 seeds per calibration point; 4096 runs per Prop. 3 point; 4 and 8 identical runs per floor; 500 training updates) were **removed** from the figure text pending rows | `R/phase2/calibration_provenance.json` `n_seeds`; `prop3_L64.json` `n_seeds_mc`; floor files; `phase3_report.md` |

Shown from a committed file + key without a ledger row (owner may want
rows): component weights 1/6, 1/4, 1/2 (configs); the arm (p, n) values
(`secondary.md:9-16`); card names RTX 5090 / RTX PRO 6000
(`phase5_report.md:1011`); "seeds 1–60" (`unblind/report.md:17`).

## Not built, and why

- **Co-active distribution (Figure 5)** and **Coupling B danger
  concentration (Figure 4):** not in the brief's priority list; the
  candidates in `paper/figures/out/` cover them. Builder's audit item 2
  applies to any Figure 4: CB-5's "1.41×" is the first 2-seed estimate over
  the High floor, not a pool of the 3/3 replication.
- **A step-order schematic (Figure 1):** not built; per audit item 4 it must
  follow the code (T_X reads h′ and c′).
- **Comms (Figure 6):** not built; must not suggest comms is non-inert.

## Inconsistencies found (reported, not resolved)

1. `paper/branch_B.md` §1 ("bounded at ±0.7 points") and §8 ("≈ ±0.7
   points") vs ledger RES-6's note: the spine was fixed to give Γ₄ and Γ₄′
   their own bounds (Γ₄′ reaches +0.81, RES-8); branch_B.md was not.
2. `P6/post_unblind_analysis/post_gamma4_t2000.md:16` prints a decision
   "REJECT" for B̂ (and `post_gamma4_t2000.json` carries `reject: true`),
   while the UNBLIND RESULT entry and ledger RES-7 record no verdict word for
   B̂. The ladder follows the log (no chip).
3. `paper/figures/out/fig09_gamma_t.*` shows "sign rule (iv): UNSTABLE"
   rather than the registered string "sign unstable over the final half";
   `fig08_*` lacks the UNDERPOWERED flag on the k = 60 row and labels B̂
   "REJECT" (see item 2). Read-only here; listed for the other agent.
4. `paper/beyond_pdf/submission.md`'s GIF-slot-1 comment says the renderer
   has "no structure or collapse layer"; that holds for the 2026-09-27 GIFs,
   not for the 2026-10-10 restyle or this explorer.

## Double-blind and self-containment check (recorded 2026-10-10)

`src/check_outputs.py` over all 11 HTML and 11 PNG outputs (re-run after the
evening revision): **0 findings**
(`out/data/output_checks.json`). HTML: no `http(s)://` (the SVG namespace
identifier excepted), no `<script src`, `<link`, `@import`, `<iframe`,
`fetch(`, no `/home/`, `/tmp/`, user or account name, `github`, tool name,
or 40-hex commit hash; repository paths and source comments were also
removed from the pages. PNG: written with `metadata={"Software": None}`; no
tEXt/zTXt/iTXt/eXIf/tIME chunk. Rendered and inspected in a headless
browser (light, dark, 390 px width) before recording.

## Builder's audit (coordinator, 2026-10-10) — applied

1. Verdict words only where recorded: B̂ shows estimate and interval only
   (F2, F5); Γ₄ and Γ₄′ "null"; the k = 60 prefix UNDERPOWERED.
2. CB-5 "1.41×": not drawn anywhere (no Coupling B figure built here).
3. METH-1 confound is card, code tree **and** config: stated on F6c.
4. T_X reads post-step fields: noted for any schematic (none built).
5. One visual language with the restyled GIFs: F1 and F6a use their
   palette and glyphs; stressor colours moved to violet/magenta; unseen
   cells use solid grey with "?" so they cannot be read as smoke hatching.
