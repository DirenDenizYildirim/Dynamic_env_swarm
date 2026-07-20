# M3.0b — Red-team audit: status and environment caveats

Session: remote fresh-clone container, 2026-07-20. This file records what
this milestone's audits could and could not execute in this environment,
and every deviation from the milestone prompt. Nothing here is merged;
the milestone ends at a human STOP.

## Environment reality (deviations from the prompt's assumed setup)

1. **No local M3.1 work exists here.** The remote has exactly one branch
   (`main` @ 8de4976, M3.0-complete). A branch `m31-structure` could not
   be "confirmed committed" — it does not exist in this container or on
   the remote. Everything that the prompt routes to `m31-structure`
   (mutation-audit test additions, `--allow-hash`) is instead committed
   on the session branch `claude/m30-red-team-audit-vi33gk` (branched
   from 8de4976) in a **separate commit**, so it can be cherry-picked
   onto the real `m31-structure` once that branch is pushed. The
   prompt's "verify the M3.1 nesting test exists and is green" could
   not be performed — no M3.1 code to verify.
2. **The M3.0 checkpoint archive is not in this environment.** Searched:
   working tree, full git history of all branches, GitHub releases/tags,
   container filesystem. `.gitignore` (`/m30.tar.gz`,
   `che/bench/results/phase3/m30/ckpt_*/`) confirms the checkpoints were
   deliberately kept out of git and live only on the researcher's
   machine / GPU box. Per the milestone instruction ("if the archive
   cannot be found, STOP and ask the human — do not regenerate
   checkpoints silently"), **no checkpoints were regenerated** and the
   checkpoint-dependent audits are prepared but not executed.
3. The `../che-m30` worktree was created at 8de4976 as specified; the
   only files added to it are `che/scripts/render_episode.py` and
   `che/scripts/obs_alignment.py` (identical copies committed here).

## Audit status (CLOSED — local completion 2026-07-20, main workstation)

The cloud session's blockers were environmental only; everything below was
completed locally, where the m30 checkpoints live. This table supersedes
the cloud statuses (kept in the git history of this file).

| Audit | Status | Artifact |
|---|---|---|
| 1 — episode renders | **DONE** — 24 trained-policy episodes rendered and watched; no degenerate behavior; Medium burnt-region-abandonment finding flagged | `render_notes.md`, `renders/` (6 GIFs committed, 24 JSONs) |
| 2 — cross-severity 3×3 | **DONE** — 27 cells × 512 eps at pinned `8de4976`; diagonal reproduces the M3.0 GPU means to 3 decimals | `cross/cross_matrix.md` (+ per-cell npz/json) |
| 3 — mutation audit | **DONE, 7/7 caught** — re-run in full on `m31-structure` (the code going forward); mutation-g gap closed by a structural invariant-#3 test committed there (`fe95f43`) | `mutation_audit.md` (closing section) |
| 4 — obs alignment | **DONE** — visual + numeric crosscheck (cloud) | `obs_alignment.png`, notes in `mutation_audit.md`'s sibling section below |

Sequencing notes (local closure): M3.1 was moved off local main onto
`m31-structure` (`0081854`, not merged); main was reset to `72d0609` —
env/eval code identical to `8de4976`, so audits 1/2 ran on exactly the
checkpoint-training code (renders from a pinned `8de4976` worktree, matrix
via the driver's pinned-worktree import). The nine checkpoint
`config_hash.txt` files were restored to their true old-schema hashes
(verified by recomputation); post-merge access to these checkpoints goes
through the harness `--allow-hash` flag (cherry-picked onto
`m31-structure` as `156d780`), which records the old→current mapping in
the eval summary JSON — explicit and recorded, never silent.

## Audit 4 result (obs alignment)

`obs_alignment.png`: severity High (β=0.70), seed 1, random policy
(alignment is a property of `observe()`, policy-independent — trained
checkpoints unavailable, see above), agent 9, t ∈ {20, 50, 90}, one row
per timestep: global grid + 9×9 crop rectangle beside the five per-plane
crops exactly as the network receives them. The burning front, smoke
gradient, and food cells inside the red rectangle match the crop panels
cell-for-cell by inspection; the center ring sits on the agent's own
cell (alive-occupancy plane shows the observer at the center).

Numeric crosscheck (same episode, t ∈ {20, 50, 90}): for **every** agent,
a hand-built crop of `[hazard/2, ρ, food, collapsed, occ]` from the
global post-step state (numpy pad + slice) was compared with
`obs["grid"][agent]` — **0 mismatches** across all agents × 3 timesteps
× 5 planes, including edge padding. No transposition, no off-by-one.

## To run the blocked audits once the archive is available

```bash
# from the main repo root; archive extracted so that
# ../che-m30/che/bench/results/phase3/m30/ckpt_{sev}_dp0.5_s{seed}/ exist
cd ../che-m30
for sev in low medium high; do for s in 0 1 2; do for ep in 0 1 2 3 4 5 6 7; do
  uv run python -m che.scripts.render_episode \
    --config che/configs/severity_${sev}.yaml --death-penalty 0.5 \
    --ckpt-dir che/bench/results/phase3/m30/ckpt_${sev}_dp0.5_s${s} \
    --seed ${ep} --every 2 --tag ${sev}_s${s} \
    --out /abs/path/main-repo/che/bench/results/phase3/m30b/renders/${sev}_s${s}_ep${ep}.gif
done; done; done   # prompt asks for low_s0/Low, high_s2/High, medium_s0/Medium ≥8 each

cd ../Dynamic_env_swarm
uv run python che/scripts/m30b_cross_matrix.py \
  --worktree ../che-m30 \
  --ckpt-root ../che-m30/che/bench/results/phase3/m30 \
  --out-dir che/bench/results/phase3/m30b/cross
```
