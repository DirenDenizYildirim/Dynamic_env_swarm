# Renders, 2026-09-27: provenance and reading rules

Three episode GIFs and their static companions, rendered on the owner's
laptop (CPU) with `che/scripts/render_episode.py` at tree `f08c97b` (clean).
They are the first renders of Phase-6 checkpoints, and they discharge the
owed check that the renderer works on them (both restored at step 1000).

## Selection rule, fixed before any render was made

- **Config:** `che/configs/theta_star_holdout.yaml`, i.e. θ\* (all-on, held-out
  Medium β = 0.49). Evaluated cross-config with `--allow-hash <training
  hash>`, as the grid's evals were.
- **Checkpoints:** seed 1, the first seed, of each confirmatory arm in
  `che/bench/results/phase6/g1_conf_5090/`, at T\* = 1000. Archive hashes
  were verified against that directory's `SHA256_CKPT.txt`:
  - `ckpt_iso_s1.tar.zst`
    `0fc9fd0c6bb84a09a9fdacfd80e24f85339a0d3d3858f072b0852a4466cf3b5a`,
    training hash `b63fc2d6764c7ffe`
  - `ckpt_joint_s1.tar.zst`
    `64c49ef8fc8c28b6234b4e3ed03812967f15beb49eadcbb31feff5c38ec19e61`,
    training hash `da6617b402b08b9b`
- **Episode:** key seed 0. Actions are sampled stochastically, as the eval
  harness does (no `--greedy`). The render's key is the episode key
  directly, so this is **not** episode 0 of the 512-episode eval draw.
- **Display:** every 2nd step (129 frames, t = 0…256), 12 fps.
- **Baseline:** a random policy on the same config and key.

No other episode, seed or checkpoint was rendered, so nothing was chosen
from a set.

| file | policy | alive at t = 256 | completion | return |
|---|---|---|---|---|
| `thetastar_random_seed0.gif` | random | 12 / 12 | 0.156 | 5 |
| `thetastar_iso_s1_T1000_ep0.gif` | ISO, seed 1, T = 1000 | 10 / 12 | 0.813 | 25 |
| `thetastar_joint_s1_T1000_ep0.gif` | JOINT, seed 1, T = 1000 | 12 / 12 | 0.594 | 19 |

Each `*_static.png` holds the first, middle and final frame (t = 0, 128,
256). It is the static companion the SUBMISSION FORMAT RULING requires for
the browser-printed PDF. Each `*.json` is the renderer's own summary, with
`ckpt_dir` rewritten from the scratch extraction path to the archive it
came from.

## Reading rules (instruments law, clause 2; SUBMISSION FORMAT RULING)

- **These illustrate. They grade nothing.** Each is a single episode. The
  ISO and JOINT episodes happen to differ by 2 of 12 agents (16.7 points)
  and by 0.22 in completion. The measured confirmatory survival difference
  is **+0.96 points** (ledger RES-2), and completion is a null (RES-1). A
  caption must never present these two episodes as showing the result.
  **Whether to show ISO and JOINT side by side at all is the owner's
  decision.** If they are shown, the caption states that each is one
  pre-selected episode and gives the measured effect with its interval.
- **Renderer limits:**
  - There is no structure or collapse layer, so collapse-seeded
    ignitions (Coupling A) are not visually distinguished from other fire.
  - The white overlay is the smoke *field*, not what each agent perceives
    (Coupling B acts on the egocentric crop).
  - The end-of-episode drift of agents to the walls is the known artifact
    (spine §10 item 6): recorded, and ungraded.
- **Double-blind:** the GIFs and PNGs carry only the titles shown. The JSON
  sidecars and this README are provenance and do **not** go into
  `assets/`.

## Commands (thread-capped: `OMP/MKL/OPENBLAS_NUM_THREADS=4`, `XLA_FLAGS=--xla_cpu_multi_thread_eigen=false`, `taskset -c 0-3 nice -n 15`)

    uv run python -m che.scripts.render_episode --config che/configs/theta_star_holdout.yaml \
      --random-policy --seed 0 --every 2 --fps 12 --tag "random policy, theta*" \
      --out thetastar_random_seed0.gif
    uv run python -m che.scripts.render_episode --config che/configs/theta_star_holdout.yaml \
      --ckpt-dir <extracted ckpt_iso_s1> --allow-hash b63fc2d6764c7ffe --seed 0 --every 2 --fps 12 \
      --tag "ISO policy (seed 1, T=1000), theta*" --out thetastar_iso_s1_T1000_ep0.gif
    uv run python -m che.scripts.render_episode --config che/configs/theta_star_holdout.yaml \
      --ckpt-dir <extracted ckpt_joint_s1> --allow-hash da6617b402b08b9b --seed 0 --every 2 --fps 12 \
      --tag "JOINT policy (seed 1, T=1000), theta*" --out thetastar_joint_s1_T1000_ep0.gif

The static strips were made with Pillow (frames 0, n/2 and n−1 pasted side
by side). No repo code was added for them.
