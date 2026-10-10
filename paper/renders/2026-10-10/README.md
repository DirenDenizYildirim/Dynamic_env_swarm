# Renders, 2026-10-10: restyle of the 2026-09-27 episodes (presentation only)

This directory restyles the three committed episode GIFs in
`paper/renders/2026-09-27/`. It shows the same three episodes and the same
trajectories, and only the drawing changes. Mandate: `docs/decision_log.md`,
FIGURES, ADDENDUM item 1 (owner, 2026-10-10). The 2026-09-27 files are not
touched. Rendered on CPU, on the owner's laptop, at a dirty tree based on
`cf3c08f`. The only uncommitted change under `che/` was another session's
docstring wording in `che/env/config.py`; it touches no code. Nothing under
`che/` was modified for this restyle. The renderer imports `che` read-only.

## Selection rule (restated from 2026-09-27, unchanged; nothing chosen from a set)

- **Config:** `che/configs/theta_star_holdout.yaml`, i.e. θ\* (all elements
  on, held-out Medium β = 0.49).
- **Checkpoints:** seed 1, the first seed, of each confirmatory arm in
  `che/bench/results/phase6/g1_conf_5090/`, at T\* = 1000 (the latest step in
  each archive). They are evaluated cross-config with `--allow-hash <training
  hash>`, as the grid's evals were.
- **Episode:** key seed 0, used directly as the episode key. This is **not**
  episode 0 of the 512-episode eval draw. Actions are sampled stochastically,
  as the eval harness does them (no `--greedy`).
- **Baseline:** a random policy on the same config and key.

The constants are written out in `src/episodes.py` (`EPISODES`). No other
episode, seed, key, checkpoint or config was rolled out.

### Checkpoint archives verified before use

Each archive's sha256 was computed and matched against both
`g1_conf_5090/SHA256_CKPT.txt` and the 2026-09-27 README.
`config_hash.txt` in the extracted directory equals the training hash passed
to `--allow-hash`, and the restored step is 1000. `src/episodes.py` asserts
all of this on every run.

| archive | sha256 (computed = SHA256_CKPT.txt = 2026-09-27 README) | training hash | restored step |
|---|---|---|---|
| `ckpt_iso_s1.tar.zst` | `0fc9fd0c6bb84a09a9fdacfd80e24f85339a0d3d3858f072b0852a4466cf3b5a` | `b63fc2d6764c7ffe` | 1000 |
| `ckpt_joint_s1.tar.zst` | `64c49ef8fc8c28b6234b4e3ed03812967f15beb49eadcbb31feff5c38ec19e61` | `da6617b402b08b9b` | 1000 |

## Identity: same episodes, same trajectories

Full results are in `provenance/identity_check.json`, written by
`src/check_identity.py`.

1. **The original renderer is deterministic.** `che.scripts.render_episode`
   was re-run with the 2026-09-27 README's exact commands into a scratch
   directory. All three GIFs came out **byte-identical** to the committed
   ones: equal sha256 (`fbeb9a27…`, `d298ed5b…`, `ef64f923…`), all 129 of 129
   decoded frames pixel-equal, and equal frame durations.
2. **The restyle uses the original code path.** `src/episodes.py` calls
   `render_episode.rollout_frames` itself, unmodified, with the inputs that
   `render_episode.main()` builds for those commands. That function's frame
   dict carries hazard, smoke, food and agent positions/aliveness, but not
   the structural state. To get structure, the call temporarily wraps the
   module's `reset` and `jax.jit`, so that each `EnvState` the original code
   returns is recorded and passed back unchanged. The jitted function is
   still `jax.jit` of the original lambda.
3. **Per-frame digests are equal for all 257 frames (t = 0 to 256) of every
   episode.** Two kinds of sha256 are taken per frame. The *frame-dict
   digest* covers hazard, smoke, food, agent_pos and agent_alive. The
   *full-state digest* adds structure and weak. The check process (a
   separate process from the render) compares:
   - the frame-dict digests of the original rollout untapped, the original
     rollout tapped, and the restyle render: equal;
   - the full-state digests of the tapped original and the restyle render:
     equal.

   Chain digests (one sha256 over the 257 per-frame digests, in order):

   | episode | frame-dict chain (original = restyle) | full-state chain (original tapped = restyle) |
   |---|---|---|
   | random | `4ad45289cbb0e119db02e6baed667684224e73dd95b4bfdde5b50e6eaf88d380` | `844a3d7179a94656d386d02e0d9f1ea71257551eb61e35087b0f33c885ace18b` |
   | ISO, seed 1 | `b1f8aec76321319d54346bb225d7d12b00cc49b42b9c67e9c5523b41d3a28540` | `a60c62cc48efd89d7365f23f211cf4f2cd0a1f497639cd1fe628c791a62355b5` |
   | JOINT, seed 1 | `298702114579facd034a305235c9939ac0f0045d8b1694962caf158ea7006017` | `be822d0424875b32ceb6f8123f9674c96b8fe9ab38e4d2d0999629ca4435c895` |

   The per-frame lists are in `provenance/*.restyle.json`.
4. **The tapped trajectory reproduces the committed GIFs.** The tapped
   rollout's frames were drawn with the original `draw_frame` and saved with
   `main()`'s settings (every 2nd step, 12 fps, 5.4 × 5.8 in at 110 dpi).
   Each result is byte-identical to the committed 2026-09-27 GIF, with all
   129 frames pixel-equal.
5. **The restyle is itself reproducible.** A second full render gave
   byte-identical GIFs, PNGs and provenance JSONs.

The smoke field never exceeds 1 in any frame of the three episodes (max
ρ = 1.0 exactly), so the smoke ramp does no clipping. This follows from the
model: a cell burns for one step, so ρ′ = 1 on a burning cell and decays by
e^−η afterwards. The render asserts it.

## Render settings, old vs new

| | 2026-09-27 (`render_episode.py`) | 2026-10-10 (`src/render_restyle.py`) |
|---|---|---|
| drawing | matplotlib `imshow` + `scatter`, `FuncAnimation` + `PillowWriter` | numpy raster at an integer **8 px per cell** (nearest-neighbour by construction), PIL for text; exact palette (61 colours), so the GIF is lossless |
| GIF size | 594 × 638 px | 560 × 718 px (arena 512 × 512 px) |
| frames | every 2nd step plus the final one: 129 | **every step**: 257 (t = 0 … 256) |
| timing | 80 ms per frame, 10.3 s loop | 50 ms per frame (20 fps); first frame held 0.8 s, last frame 2.5 s; 16.05 s loop |
| fuel / burning / burnt | `#2d5016` / `#ff4500` / `#4a4a4a` | `#e9ebe0` / `#eb6834` / `#3d3a36` (light / mid / dark), with 1-px light gridlines |
| smoke ρ | white whole-cell overlay, α = 0.7·clip(ρ, 0, 1) | light diagonal **hatching**, opacity 0.9·ρ in 16 equal steps on [0, 1]; legend entry "smoke density ρ (environment field)" with its ramp |
| structure | not drawn | **weak** intact cells (`state.weak`): centre dot; **collapsed** cells (`state.structure`): boxed X, dark on light cells and white on burnt cells, with the cell's hazard fill kept between the strokes |
| food | yellow `#ffd700` square | aqua `#1baf7a` square with a dark ring |
| agents | alive: cyan `#00e5ff` circle; dead: black × | alive: blue `#2a78d6` disc with white and dark rings; dead: hollow dark ring |
| title | `{tag} t=… alive a/12 compl … ret … burning …` | the policy label ("random policy", "ISO, seed 1", "JOINT, seed 1") and "t = k / 256" only |
| legend | none | 8 swatches plus the smoke ramp, drawn by the same raster code as the map |
| static companion | 3 full GIF frames (t = 0, 128, 256) pasted side by side | the same three arena rasters as the GIF frames at t = 0, 128 and 256, side by side under one policy label and one legend; 1648 × 712 px |

**Colour.** The three marks use slots 1 to 3 of the dataviz reference
palette: blue for agents, orange for fire, aqua for food. A validator run
(`--pairs all`, light) gave a worst CVD ΔE of 9.2 (aqua vs orange, deutan;
target ≥ 8) and a worst normal-vision ΔE of 24.0 (floor 15). The original
yellow food failed against orange (normal-vision ΔE 13.7), which is why food
moved to aqua.

**Greyscale.** The hazard states differ in lightness (fuel light, burning
mid, burnt dark). Smoke, weak floor and collapse are patterns, and agents,
food and collapsed floor differ in shape. A greyscale conversion of the
static companion was inspected.

## Sizes

| file | bytes |
|---|---|
| `gif/thetastar_random_seed0.gif` | 2,606,682 |
| `gif/thetastar_iso_s1_T1000_ep0.gif` | 2,705,720 |
| `gif/thetastar_joint_s1_T1000_ep0.gif` | 2,075,240 |
| `img/thetastar_random_seed0_static.png` | 15,986 |
| `img/thetastar_iso_s1_T1000_ep0_static.png` | 16,410 |
| `img/thetastar_joint_s1_T1000_ep0_static.png` | 15,633 |

The GIFs are 2.2 to 3.0 times the 2026-09-27 ones (0.88 to 0.99 MB) because
they have twice the frames.

## Metadata check (double-blind)

`src/check_identity.py` parses every output file:

- **GIFs:** GIF89a. Each holds only 257 images, 257 graphic-control blocks
  (frame timing) and one `NETSCAPE2.0` application block (loop). There are
  no comment or plain-text blocks and no bytes after the trailer.
- **PNGs:** only the `IHDR`, `PLTE`, `IDAT` and `IEND` chunks. There are no
  text, time or EXIF chunks.
- **Raw-byte search** of all six files (case-insensitive): no hits. Two
  kinds of string were searched for.
  - Generic strings: home and scratch paths, repo and host names,
    "software", "author", "comment", "copyright".
  - Identity strings read at run time: the user name, the home directory,
    the host name, the repo path, and git `user.name` / `user.email`, with
    their tokens. They are read when the check runs, so neither the script
    nor its report contains them; the report records only how many were
    searched.

The only text drawn in the images is the policy label, the time step and the
legend.

## Reading rules (carried over from 2026-09-27, updated for this restyle)

- **These illustrate. They grade nothing.** Each GIF is one pre-selected
  episode.
  - In these episodes ISO and JOINT end 2 of 12 agents apart (16.7 points)
    and 0.22 apart in completion.
  - The measured confirmatory survival difference is **+0.96 points**
    (ledger RES-2), and completion is a null (RES-1).
  - A caption must never present these episodes as showing the result.
  - **Whether to show ISO and JOINT side by side at all is the owner's
    decision.** If they are shown, the caption states that each is one
    pre-selected episode and gives the measured effect with its interval.
- **Nothing in the image grades.** The old title's alive counter,
  completion, return and burning count are gone. Dead agents are still
  drawn (they are state), in a neutral hollow ring, and the three files share
  one identical style. A reader can still count the rings, so the rule above
  still binds.
- **The fire differs between episodes only through structure.**
  - Random and JOINT have identical hazard and structure fields in all 257
    frames.
  - ISO's fields first differ from both at t = 16, and hazard and structure
    diverge at that same step. They then differ in 241 frames.
  - The fire's random draws do not depend on actions: `env.step` splits them
    from the step key alone. A policy can therefore change the fire only
    through collapses, whose rate reads agent load (Def. 5), and the
    Coupling A ignitions they seed.
  - A difference in burned area between these GIFs is one episode's
    structural event. It is not an outcome, and a caption must not read it
    as one.
  - Source: `provenance/identity_check.json`, `cross_episode_informational`.
    These are not paper numbers; they need a ledger row before any of them
    is cited.
- **Caption limits: which this restyle removes.**
  - **Removed:** "there is no structure or collapse layer". Weak and
    collapsed cells are now drawn exactly from `state.weak` and
    `state.structure`.
  - **Remains:** collapse-seeded ignitions (Coupling A) are still not
    distinguished from other fire. The step's `info` exposes only their
    per-step count (`seeded_ignitions`); the per-cell mask is internal to
    `che.env.env.step`. Recovering it would mean re-executing step internals
    outside `step`, so it was not done. Episode totals from `info` are in
    `provenance/*.restyle.json`.
  - **Changed, not removed:** the smoke is no longer a white overlay. It is
    hatching that the legend itself labels "smoke density ρ (environment
    field)". It is still the field and not what any agent perceives:
    Coupling B acts on each agent's egocentric crop, and no agent's view is
    drawn. A caption no longer has to explain a white overlay, but it must
    not call the hatching perception.
  - **Remains:** the end-of-episode drift of agents to the walls is the
    known artifact (spine §10 item 6). It is visible at t = 256 and is
    recorded, not graded.
- **Placement.** Only `gif/*.gif` and `img/*_static.png` may go into
  `paper/beyond_pdf/assets/`. This README, `provenance/` and `src/` are
  provenance and stay out. Each GIF needs its static companion beside it
  (SUBMISSION FORMAT RULING).

## Commands

All commands run from the repo root, CPU only, with thread caps:
`OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4
XLA_FLAGS=--xla_cpu_multi_thread_eigen=false PYTHONDONTWRITEBYTECODE=1`,
prefixed by `taskset -c 0-3 nice -n 15`.

    # 1. determinism of the original renderer: the 2026-09-27 README commands, into scratch
    uv run python -m che.scripts.render_episode --config che/configs/theta_star_holdout.yaml \
      --random-policy --seed 0 --every 2 --fps 12 --tag "random policy, theta*" \
      --out <rerun>/thetastar_random_seed0.gif
    uv run python -m che.scripts.render_episode --config che/configs/theta_star_holdout.yaml \
      --ckpt-dir <extracted ckpt_iso_s1> --allow-hash b63fc2d6764c7ffe --seed 0 --every 2 --fps 12 \
      --tag "ISO policy (seed 1, T=1000), theta*" --out <rerun>/thetastar_iso_s1_T1000_ep0.gif
    uv run python -m che.scripts.render_episode --config che/configs/theta_star_holdout.yaml \
      --ckpt-dir <extracted ckpt_joint_s1> --allow-hash da6617b402b08b9b --seed 0 --every 2 --fps 12 \
      --tag "JOINT policy (seed 1, T=1000), theta*" --out <rerun>/thetastar_joint_s1_T1000_ep0.gif

    # 2. the restyle (verifies and extracts the archives itself into <scratch>)
    uv run python paper/renders/2026-10-10/src/render_restyle.py --scratch <scratch>

    # 3. the checks (identity, digests, redraw, cross-episode, metadata)
    uv run python paper/renders/2026-10-10/src/check_identity.py \
      --scratch <scratch2> --rerun-dir <rerun>

## Files

- `gif/<stem>.gif`, `img/<stem>_static.png`: the outputs. The stems are the
  2026-09-27 ones.
- `src/episodes.py`: the selection constants, archive verification, the call
  into the original rollout, and the digests.
- `src/render_restyle.py`: the drawing.
- `src/check_identity.py`: the checks above.
- `provenance/<stem>.restyle.json`: the render's own record (inputs, per-frame
  digests, palette size, ρ max, `info` totals).
- `provenance/identity_check.json`: the check results.
- `SHA256SUMS`: hashes of everything above and of this README.
