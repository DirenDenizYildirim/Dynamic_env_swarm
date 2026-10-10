# Interactive figures: design (2026-10-10)

Written before any figure in this directory was built, under the decision
log's **FIGURES**, its **ADDENDUM** and **FIGURES FIRST** entries (owner,
2026-10-10). Candidates and proposals only: nothing here is placed in the
paper, and the paper's structure is the owner's decision. Captions are the
owner's; every figure carries factual labels and registered verdict strings
only.

---

## 1. What the published Beyond PDF examples do

Read on 2026-10-10 as data (page HTML and every iframe's HTML/JS, saved to a
scratch directory, never executed, nothing copied). Listing pages:
https://tmlr-beyond-pdf.org/about, https://tmlr-beyond-pdf.org/under_review/
(five submissions, plus the kit's example on page 2), and
https://tmlr-beyond-pdf.org/accepted/ (one paper).

| entry | interactive figures | what they are |
|---|---|---|
| [D5gNaP6QHN](https://tmlr-beyond-pdf.org/under_review/D5gNaP6QHN/) (world-model friction diagnosis) | 14 iframes + 3 MP4 | the richest: a synchronized 5-panel checkpoint player, 12 Plotly line/band charts, a "Central Claim" box above the abstract, a revision note |
| [HGmCGa0Q3O](https://tmlr-beyond-pdf.org/under_review/HGmCGa0Q3O/) (chain-of-thought compression) | 7 iframes | small vanilla-SVG explorers: sliders and selects that recompute a formula, one-line data-provenance subtitle |
| [JNhGH8NVUL](https://tmlr-beyond-pdf.org/under_review/JNhGH8NVUL/) (CoT answer flips) | 8 iframes | d3 charts, pill toggles across models, a prev/next stepper through examples ("1 / 8"), a Sankey |
| [fDT1sioSnn](https://tmlr-beyond-pdf.org/under_review/fDT1sioSnn/), [6AGOgvdze1](https://tmlr-beyond-pdf.org/under_review/6AGOgvdze1/) | none | static PNGs (one forest plot; recovery/robustness plots) |
| [z4PfNDNAcN](https://tmlr-beyond-pdf.org/accepted/z4PfNDNAcN/) (accepted; HMC root-finding) | none | static PNGs, one GIF, a diagram |
| [kit example](https://tmlr-beyond-pdf.org/under_review/submission/) | 3 iframes | a physics toy (matter.js + Tailwind from CDNs), tangent-line and graph demos |

### Patterns that work (adopted)

1. **The claim before the evidence.** D5gNaP6QHN opens with a boxed
   "Central Claim" in which every hedge is written out, then the abstract.
   Its figures arrive in the order of its hypotheses (H1, H2), and its
   captions carry their status in words: "post-hoc descriptive audit",
   "added in revision", "interactive". For this paper the equivalent is the
   **registered reading first**: the verdict string leads every figure that
   carries one.
2. **One synchronized player, many panels.** The D5 checkpoint player is a
   single canvas loop driving five panels from one scrubber (pause, scrub,
   0.5×/1×/2×, a "frame k / N" readout). It is the strongest figure on the
   site because the reader controls time. The episode explorer adopts the
   control set and adds keyboard access and layer toggles.
3. **Floors drawn as series.** D5's Figure 5b draws the noise floors as
   their own banded channels next to the estimates, so the reader sees what
   a slope has to beat. This project's floor bars are the same idea.
4. **A marked regime boundary.** D5 draws its critical friction as a
   labelled vertical rule on every sweep chart. The severity explorer marks
   the three locked levels the same way.
5. **Steppers for ordered material.** JNhGH8NVUL's "prev / next, 1 / 8"
   explorer suits material whose order matters. The registered readings have
   an order (Γ → Γ₄ → Γ₄′ → B̂), so the ladder is a stepper.
6. **Provenance as a subtitle.** HGmCGa0Q3O's explorers state the data's
   source in one muted line above the controls. Ours state the artifact
   class and interval level the same way ("secondary · 95 %, not
   family-corrected").
7. **Small, dependency-free widgets.** HGmCGa0Q3O's files are 4–7 KB of
   inline SVG and vanilla JS and work offline. That is the bar here.

### Patterns to avoid (each seen at least once)

- **Network at view time.** Every D5 chart loads Plotly from a CDN, every
  file loads Google Fonts, JNhGH8NVUL loads d3 from its own domain, the kit
  example loads Tailwind and matter.js. Offline or in an archive, the figure
  is blank. Ours: inline everything (hard rule).
- **No printed fallback.** No iframe on the site has a static companion; in
  the browser-printed PDF, an iframe prints as whatever its first paint was,
  or as nothing. Ours: a PNG companion beside every iframe, and
  `@media print` hides the controls inside the iframe.
- **Fixed iframe heights that clip.** All examples set `height` on the
  iframe and `overflow:hidden` inside it; at phone width the legend or axis
  is cut off. Ours: layouts reflow to one column, and each file sets its own
  iframe height when the embedding page is same-origin (it is: assets are
  served from the paper's own site), inside a try/catch.
- **Autoplay and unconditional animation.** The D5 player starts playing on
  load; JNhGH8NVUL types text with a blinking caret. None of the 32 files
  checks `prefers-reduced-motion`, `prefers-color-scheme`, or `@media print`,
  and none sets an ARIA attribute. Ours: never autoplay; respect reduced
  motion; follow the host theme; every control is a native button or range
  with a label and a visible focus ring.
- **Colour as the only identity channel** (pill colours, Sankey bands).
  Ours: shape, texture and direct labels carry identity; colour supports.
- **Decorative interpretation in the figure** (JNhGH8NVUL's "THE FEYNMAN
  TRAP" header, ✓/✗ icons). Ours: factual labels and registered strings only.

---

## 2. Audit of the candidates in `paper/figures/out/` (read-only)

State at 2026-10-10 ~20:00 (another agent is still building there).

| file | passes | findings |
|---|---|---|
| `fig08_gamma_contrasts.{png,html}` | registered family first; Šidák CIs; MDE80 bands; floor on the Γ row only; no external URL | (1) The **k = 60 prefix row is not flagged UNDERPOWERED**; the committed report flags it (`unblind/report.md:17`) and spine §9.2 item 1 requires it. (2) **k = 72 is not labelled as the recorded deviation** (DES-3). (3) No row carries the registered consequence string **"does not survive the inert-share correction"** (UNBLIND RESULT; `post_gamma4_t2000.md:19`), so the figure shows Γ₄ null without its registered reading. (4) B̂ shows "REJECT". The committed decision column prints it (`post_gamma4_t2000.md:16`), but no verdict word is recorded for B̂ (UNBLIND RESULT gives only the estimate, z and interval), so per the builder's audit it should carry estimate and interval only. (5) No `prefers-reduced-motion` handling (no motion to speak of, so minor). |
| `fig09_gamma_t.{png,html}` | registered verdict first, signs printed, floor at T\* only, card footer | (1) The verdict reads **"sign rule (iv): UNSTABLE"**, not the registered string **"sign unstable over the final half"** (POST-UNBLIND STAGE RESULT). (2) A connecting polyline joins the 11 checkpoints; not a fit, but it reads as a trajectory between unmeasured points (the manifest says so; the figure does not). |
| `fig10_secondary.{png,html}` | "SECONDARY · non-verdict-bearing · 95 % … not family-corrected" header; knees UNDERPOWERED; mediation VOID; JOINT drawn outside the sampled range | (1) Uses **"element(s)"** in axis labels ("both elements", "no-element share"); the TITLE AND TERMINOLOGY RULINGS make **"stressor"** the paper's word for the composable elements. (2) Dense: six panels in one PNG; the prediction-vs-measured panel, which §1 points to ("where its fit fails"), is one of six. (3) Many stated completion numbers are marked NEEDS LEDGER ROW in its manifest. |
| `fig02_calibration.{png,html}` | no R_L logistic centres drawn (O-2 respected); locked levels marked | Draws **β̂_c = 0.500 ± 0.005 (locked)** as a band; its provenance is the lock record only (CAL-1, O-2 open). Not a violation of "no R_L logistic centres", but the one number in the panel whose estimator has no committed artifact. |
| `fig03_coupling_a.png` | CA-2 drawn as its own run; m44 and m35 separate | Only the L = 64 sweep (CA-2) is shown; CA-3 is a separate run with no JSON and is absent, which is correct. |
| `fig04_coupling_b.png` | floor band; first estimate beside the replicates | Prints per-seed values (−0.0687, −0.1066, −0.0470, −0.0876); CB-5 carries only the range and CB-6 the −0.0876, so the other two need ledger rows. |

None of these files is modified by this work.

---

## 3. One visual language

**Principle.** Colour means one of two things and nothing else: **which
stressor** (Coupling A, Coupling B) or **which hazard state** (fuel,
burning, burnt). Everything statistical (estimates, intervals, bands,
verdicts) is ink and grey, so no colour can carry a valence ("good" green,
"bad" red) that the registration does not. Shape, texture and direct labels
carry identity in greyscale.

### Tokens (CSS custom properties, light / dark)

**Revised 2026-10-10 (same day), after the builder's audit:** the episode
imagery must match the restyled GIFs in `paper/renders/2026-10-10/`
(identity-checked), so the paper has one visual language. Those GIFs use
blue agents, aqua food and orange fire, so the stressor identity colours
moved off blue, aqua and orange.

| role | light | dark | notes |
|---|---|---|---|
| surface | `#fcfcfb` | `#1a1a19` | dataviz reference surfaces |
| ink (primary text, estimates) | `#0b0b0b` | `#f5f5f2` | |
| secondary text | `#52514e` | `#c3c2b7` | |
| muted (axes, ticks) | `#898781` | `#898781` | |
| hairline grid | `#e1e0d9` | `#2c2c2a` | solid, never dashed |
| band (MDE80 wash) | `#ecebe5` | `#2a2a27` | |
| **Coupling A** | `#4a3aa7` violet | `#9085e9` | texture: 45° lines; explorer: violet ring |
| **Coupling B** | `#e87ba4` magenta | `#d55181` | texture: 135° lines; explorer: the τ ramp ends in `#9c2f5c` |
| A + B together | both fills | both | texture: both directions (crosshatch) |
| fire-only (no active stressor) | `#c3c2b7` grey | `#4a4945` | no texture |

**Map imagery (explorer, severity renders): one palette in both themes,
identical to the restyled GIFs** (`render_restyle.py`): fuel `#e9ebe0`,
burning `#eb6834`, burnt `#3d3a36`, faint cell gridline (`#8c8a83` at 16 %),
smoke density ρ as light diagonal hatching `#f4f1eb` with opacity ∝ ρ in 16
steps ("smoke density ρ (environment field)"), weak intact floor as a centre
dot, collapsed floor as a boxed ×, food as an aqua `#1baf7a` square with a
dark ring, agents as blue `#2a78d6` discs in white and dark rings, dead
agents as hollow rings. Explorer-only marks: collapse-seeded ignitions as a
violet (Coupling A) ring with a white halo; **unseen (masked) cells in the
observation panel as solid grey `#a9a59a` with a "?"**, never hatching,
because hatching is the smoke field's mark and the two must not be confused.
The map keeps its palette in dark mode (it is a picture of the state); only
the page chrome around it themes.

**Validation** (dataviz `validate_palette.js`, run 2026-10-10): the stressor
pair violet/magenta passes every gate in both modes (light: CVD ΔE 24.9,
normal-vision 33.9; dark: CVD 16.0, normal-vision 19.7). The light magenta
sits at 2.62:1 on the surface (WARN): the relief is that every B mark also
carries its texture and a direct label. Rejected: A = blue with B = violet
(dark-mode CVD ΔE 1.9, FAIL); A = aqua with B = violet (passes, but aqua is
the GIFs' food colour); A = blue with B = orange (blue are the GIFs' agents,
orange their fire); magenta for A next to orange fire (normal-vision ΔE 12.9
against burning, FAIL all-pairs). Hazard states read by lightness in
greyscale (fuel light, burning mid, burnt dark).

### Statistical marks (all figures)

| mark | drawing |
|---|---|
| estimate, registered (Šidák 95 %) interval | filled ink marker, 2px ink whisker with caps |
| estimate, uncorrected 95 % interval (secondary) | hollow ink marker, 1px whisker, open ends |
| plane prediction (secondary) | hollow diamond, 1px whisker |
| 80 %-power MDE (±X around 0) | grey wash band, toggleable |
| reproducibility floor (±1 floor-basis sd) | **stipple** band (dots = noise), only where a floor exists |
| zero | 1px muted rule |
| marker shapes by arm/contrast | Γ ● · Γ₄ ▲ · Γ₄′ ◆ · B̂ ■ · k = 60 prefix ○ |

### Verdict chips (registered strings, verbatim)

`REJECT` and **"does not survive the inert-share correction"**: ink-filled
chip. `null`, **"sign unstable over the final half"**, "second exclusion
bound": outlined chip. `UNDERPOWERED`, `VOID`: outlined chip on a stipple
background (the instrument, not the world). No green, no red, no icons.
A chip always sits **left of** (before) the numbers it governs.

### Type and spacing

System sans (`system-ui, -apple-system, "Segoe UI", Roboto, sans-serif`),
no web font. 12 px labels, 13 px body, 15 px panel heads (semibold);
`tabular-nums` in tables, ticks and readouts only. 8 px spacing grid; 12–16 px
card padding; one control row above the plot it scopes.

### Controls, keyboard, motion, print, theme

- Native `<button aria-pressed>` toggles and `<input type="range">`; ≥ 28 px
  targets; a 2 px focus ring in ink. Every interactive mark is focusable and
  shows on focus what it shows on hover. Tooltips enhance; every value is
  also in the table view (`<details>` under each chart).
- Keyboard: Space play/pause, ←/→ one step (Shift: ten), Home/End, digits
  select (explorer agent / ladder rung), `[` and `]` jump between marked
  events.
- **No autoplay.** With `prefers-reduced-motion: reduce`, transitions are
  off, the ladder reveals without fades, and playback still runs only when
  the reader presses play.
- **Theme:** the file reads the host page's `data-theme` when same-origin
  (al-folio sets it), else `prefers-color-scheme`. Dark values are their own
  validated steps, not an inversion.
- **Print:** `@media print` hides the controls and shows the full state
  (all ladder rungs, the poster frame). The paper carries a PNG companion
  beside each iframe regardless.
- **Size:** reflows to one column under 640 px with a 16 px gutter; each
  file posts its height to the iframe element when same-origin.
- **Double-blind:** no URL, path, name, hash or hostname in any output;
  PNGs written with `metadata={"Software": None}` and checked for text
  chunks; HTML checked for `http`, `/home`, user names and 40-hex strings.

---

## 4. The figure set

Priority order is the brief's. "Ledger" lists the rows a figure's **stated**
numbers come from; plotted positions read from committed files are data.
Any stated number without a row is listed in `MANIFEST.md` as NEEDS LEDGER
ROW and is **not shown** until a row exists (the build scripts carry a
switch per number).

### F1. Episode explorer (hero) — one file per episode

- **Anchors:** §3 (the environment), with deep links reused in §5
  (collapse-seeded ignitions) and §6 (an agent's attenuated view). One file
  can be embedded several times with different initial states through its
  URL hash (`#t=…&agent=…&layers=…`); each embed's initial state needs its
  own written selection rule before it is placed.
- **Reader question:** *What does an episode of CHE look like, and what does
  an agent actually see of it?*
- **Controls:** play/pause, scrubber, step, speed 0.5/1/2/4×; layer toggles
  (fire state, smoke density field, weak floor, collapsed floor,
  collapse-seeded ignitions, food, agents); an event track under the
  scrubber marking the steps with collapse events and collapse-seeded
  ignitions (environment events only; no death marks); `[`/`]` jump between
  them; click or press 1–12 to select an agent → three 9 × 9 panels:
  **observation as produced** (obs v3 content planes; masked cells drawn as
  "unseen"), **state, same cells**, and **P(seen) = τ** (Beer–Lambert
  transmittance through the smoke field). The selected agent's crop is
  outlined on the map.
- **What it never shows:** no alive count, no completion or return readout,
  no comparison, no second episode. Agents are drawn alive or dead (the GIF
  legend's "agent, dead") because that is the state. Labels: the policy
  (owner may strip it: `build_explorer.py --no-label`), "t = k / 256", layer
  names, "illustrative". The observation panel shows alive occupancy only
  (obs plane 6); the state panel shows dead agents too, so the difference is
  visible.
- **Data:** rendered locally from the pre-selected episodes of
  `paper/renders/2026-09-27/README.md` (θ\* = `che/configs/theta_star_holdout.yaml`,
  episode key 0, stochastic actions; random policy; ISO and JOINT seed 1 at
  step 1000 from `che/bench/results/phase6/g1_conf_5090/`, sha256 checked
  against `SHA256_CKPT.txt`, restored cross-config with the README's
  `--allow-hash` values). The trajectory is checked frame by frame against
  `che.scripts.render_episode.rollout_frames` (called unmodified): sha256 of
  hazard, smoke, food, positions and alive flags at every one of the 257
  states must match, and the final alive/completion/return must equal the
  committed render JSONs. Collapse-seeded ignition cells are recovered by
  re-running the step's own kernels (`structure_step`,
  `coupling_a_seed_mask`, `hazard_step`, `seed_ignitions`) with the step's
  key split, and asserted to reproduce `h'` bitwise and `info["seeded_ignitions"]`
  exactly. Each observation is asserted equal to (true crop × reveal,
  reveal) for every frame and agent, so the file stores only the reveal
  bits and τ.
- **Ledger:** ENV-6 (64 × 64, 12 agents, horizon 256, 9 × 9 crop), ENV-7
  (planes), CB-1 (κ_B = 1.0), CAL-3 (β = 0.49 at θ\*). No outcome number.
- **Static companion:** frames t = 0, 128, 256 plus the three 9 × 9 panels
  for one agent, chosen by the rule in §6 below.
- **Risks:** (1) a reader counts disabled agents and compares files; they
  are never side by side and carry no tally, and GIF slot 2's decision
  covers whether the ISO/JOINT files appear at all. (2) The end-of-episode
  drift to the walls is visible (spine §10 item 6); recorded, ungraded. (3)
  "Smoke field" vs "perception" must not blur: the map's smoke layer is the
  state ρ; only the observation panel shows perception.

### F2. Registered-readings ladder

- **Anchors:** §9.2 (the result); a collapsed first rung could preview it
  under the abstract (owner's call).
- **Reader question:** *Read in the registered order, what does each
  contrast say, and what does the correction change?*
- **Controls:** a stepper (1 Γ · 2 Γ₄ · 3 Γ₄′ · 4 B̂, prev/next, ←/→);
  earlier rungs stay visible and dim; "show all"; MDE80 band toggle; floor
  toggle; "k = 60 prefix" row toggle (flagged UNDERPOWERED); a metric
  emphasis (completion | survival) that never hides the other.
- **Each rung shows, in this order:** the verdict chip(s), then the estimate
  with its Šidák 95 % interval, k per arm (72/72 with "recorded deviation:
  registered cap 60"; 72/20; 20/72), the card/unit mark (Γ: one unit; Γ₄
  and B̂: cross-unit; Γ₄′: same card), and the date tag where the record
  gives one (ISO-4 rule registered 2026-09-18; Γ₄′ proposed 2026-09-26
  after Γ₄ was seen). Rung 2 adds the registered consequence on survival,
  "does not survive the inert-share correction", and on completion, "second
  exclusion bound". **Verdict chips only where a verdict word is recorded**
  (builder's audit, 2026-10-10): Γ at k = 72 and the k = 60 prefix (null /
  REJECT; the prefix also UNDERPOWERED), Γ₄ (null), Γ₄′ (null). **B̂ has no
  registered test: estimate and interval only, no chip, no z**, although the
  committed report's decision column prints "REJECT" for it. MDE80 bands only
  on the confirmatory family and on Γ₄ completion (X₄ is recorded).
- **Data:** `P6/unblind/unblind.json` (`primary`, `prefix`,
  `beat_reproducibility`), `P6/post_unblind_analysis/post_gamma4_t2000.json`
  (`gamma4.per_metric.*`), `P6/secondary/secondary.json` (`replicate.*`).
- **Ledger:** RES-1, RES-2, RES-3, RES-6, RES-7, RES-8, DES-1, DES-3,
  DES-13, DES-15, HW-1, HW-4.
- **Static companion:** all rungs, both metrics, bands on.
- **Risks:** Γ = Γ₄ + B̂ holds by construction; the figure states no such
  sum. B̂'s interval excluding 0 can still be read as a verdict; the figure
  gives it no chip and the text must not either.

### F3. Training-mixture composer

- **Anchors:** §9.1 (design), and the paragraph of §1 on the active share.
- **Reader question:** *What did each arm's training distribution contain?*
- **Controls:** arm rows ISO / ISO-4 / JOINT as 100 % stacked bars of
  episode types (A only, B only, A + B, fire-only); a "nominal / as
  behaviourally certified" switch for ISO's δ-only third; a severity split
  (Low β 0.43 / High β 0.70) toggle; hover a segment for its config
  components and weights. Beneath each bar: per-stressor marginals (A, B)
  and the active share. Display only: **no slider, no prediction**.
- **Data:** the three configs' `mixture.components` (weights, κ_A, κ_B, δ,
  β); the δ-only reading from DES-8.
- **Ledger:** DES-7, DES-8, DES-14, CAL-3. The shares 1/3, 1/2, 1 and the
  ratios 3× (DES-7) and 2× (DES-14) are ledgered; per-component weights are
  read from the committed configs (file + key, listed in MANIFEST).
- **Static companion:** the same three bars, behavioural view, severity split on.
- **Risks:** the eye reads "ISO-4 and JOINT differ in composition" as "they
  differ in active share". The figure aligns the active-share marks of ISO-4
  and JOINT on one vertical, and their per-stressor marginals (0.5 vs 1.0)
  beside it.

### F4. Γ(t) over the final half

- **Anchors:** §9.2 item 6; appendix H.
- **Reader question:** *Did the sign of Γ hold over the final half of
  training?*
- **Controls:** completion | survival panels side by side (stacked on
  phones); hover/focus a checkpoint; single-card toggle (t = 1000
  re-evaluated on the post-unblind card; t < 1000 unchanged); floor toggle.
- **Shows first, always:** "sign unstable over the final half" for both
  co-primaries, then the 11-sign string with the disagreeing checkpoints
  outlined. Points with Šidák whiskers, **no connecting line, no trend
  line**. Tooltips print the sign at every t and the value only where a
  ledger row exists (RES-1/2 at 1000, RES-12 at 900/950, RES-13 at 750).
- **Data:** `P6/post_unblind_analysis/post_evalfloor_gamma_t_high.json`
  (`gamma_t.points`, `gamma_t.verdict`, `gamma_t.cross_card_T_star`);
  floor `unblind.json` `beat_reproducibility`.
- **Ledger:** RES-11, RES-12, RES-13, RES-1, RES-2, DES-13, HW-2, HW-3.
- **Static companion:** both panels, grid-card curve.
- **Risks:** the late survival rise invites a trend reading; there is none
  drawn and the verdict sits above it.

### F5. Secondary simplex

- **Anchors:** §9.2 item 4 (what §1 promises: "where its fit fails").
- **Reader question:** *Where do the secondary arms sit relative to ISO,
  ISO-4 and JOINT, and does the plane fitted there reach JOINT?*
- **Controls:** metric switch (survival | completion); hover an arm or
  estimate; "show prediction" step (the plane's γ_p × 1 at JOINT, then the
  measured Γ₄ and Γ₄′ beside it).
- **Shows:** the training simplex in (p, n) coordinates (both-stressor share
  p, fire-only share n; single-stressor share 1 − p − n), the feasible
  triangle, the sweep (m = 0.5) and identification (m = 0.4) lines, the
  sampled region shaded, ISO, ISO-4/sweep_c50_p000 and JOINT outside it;
  a panel of γ_p, γ_n, the bound and the two predictions against their
  measured contrasts. Labels: "secondary · non-verdict-bearing · 95 %, not
  family-corrected", "knee: UNDERPOWERED", "mediation: VOID".
- **Data:** `P6/secondary/secondary.json`; Γ₄ from `post_gamma4_t2000.json`.
- **Ledger:** DES-9, DES-8, DES-14, SEC-1…SEC-7, RES-6, RES-7, RES-8.
- **Static companion:** survival view, prediction shown.
- **Risks:** γ_p read as a composition effect; its panel carries "moves
  per-stressor exposure with p" as the plane's axis definition, not as a
  sentence (factual axis label), and the measured Γ₄/Γ₄′ sit beside it.

### F6. If time remains

- **Severity explorer (§4):** P_span against β at L = 32/48/64 from
  `R/phase2/calibration.npz` with ±1 SE, the three locked levels as rules
  (CAL-3), and an **illustrative** synchronized three-panel fire render at
  β = 0.43 / 0.49 / 0.70 (rule in §6). No R_L logistic centres (O-2).
- **Coupling A explorer (§5):** CA-4/CA-5 per-severity seeded ignitions
  and CA-6's near-agent share; the Prop. 3 handshakes CA-2 and CA-3 in
  **separate** panels (CA-3 has no committed data file, so it can only be a
  labelled value, not a plot).
- **Floors explorer (§8):** METH-1 (card, code tree **and config**
  confounded: M5.5 records R_comm 16, M5.1e predates the R_comm lock), METH-2,
  METH-5 (length and box confounded), HW-1, with both confounds on the
  figure.
- **Not to be drawn anywhere** (builder's audit, 2026-10-10): CB-5's "1.41×
  the floor" as a pool of the 3/3 replication (it is the first 2-seed
  estimate, CB-6, over the High floor); any step-order schematic must follow
  the code, where T_X reads the post-step fields h′ and c′.

---

## 5. Proposed figure-led reading path (a proposal; the structure is the owner's)

The paper's argument is a sequence of registered readings, and each section
can be led by one figure the reader operates before the text explains it.

| where | figure | role |
|---|---|---|
| after the abstract | F2, first rung only, collapsed ("Γ: survival REJECT; completion null"), with "read the ladder in §9.2" as its link | the result at a glance, the registered string first (D5's "Central Claim" pattern, done with the registered words) |
| §3 | **F1, random policy** (hero) | the environment before any training question: fire, smoke, collapse, and one agent's attenuated view |
| §4 | F6 severity explorer | severity as a measured phase, with the illustrative renders |
| §5 | F1 deep link at the first collapse-seeded ignition (rule needed) + Coupling A explorer | hazard begets hazard, seen then counted |
| §6 | F1 deep link with an agent selected in smoke (rule needed) | the field is not the view: Coupling B made tangible |
| §8 | floors explorer | bars come with floors |
| §9.1 | **F3** mixture composer | what each arm trained on; the active share made visible before the result |
| §9.2 | **F2** ladder → **F4** Γ(t) → **F5** simplex | the registered order: verdict, correction, robustness, what the secondary design adds and where its fit fails |
| GIF slot 2 | F1 ISO / F1 JOINT, separately, if the owner places them | illustration only |

What could move: F3 could open §9 rather than sit in §9.1; F1's §6 deep
link could replace Figure 4's masking panel as the section's lead; the
ladder preview after the abstract is optional and duplicates §9.2 by design.

---

## 6. Selection rules, written before rendering

1. **Explorer files:** exactly the three 2026-09-27 episodes (§4 F1). No
   other episode, key, seed or checkpoint is rendered.
2. **Explorer default view and static observation panel:** frame t = 128;
   agent = the lowest-index agent alive at t = 128 whose observation at
   t = 128 has at least one unseen cell; if there is none, the lowest-index
   agent alive at t = 128. The static companion uses t = 0, 128, 256 for
   the map (the frames of the 2026-09-27 strips) and this agent's three
   panels at t = 128.
3. **Illustrative severity renders (F6, if built):**
   `che.scripts.render_episode.rollout_frames` on
   `che/configs/severity_{low,medium,high}.yaml`, random policy
   (`che.train.rollout.make_random_policy`), episode key
   `jax.random.PRNGKey(0)`, one episode each, all 257 states; only the
   hazard and smoke layers are drawn; labelled "illustrative · random policy
   · episode key 0". Nothing is chosen from a set.
