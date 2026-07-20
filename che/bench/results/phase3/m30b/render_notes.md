# M3.0b Audit 1 — render notes

**Status: BLOCKED — no trained-policy episode has been rendered.**

The M3.0 checkpoint archive (`m30.tar.gz` / the nine
`ckpt_{low,medium,high}_dp0.5_s{0,1,2}` orbax dirs) is not present in
this remote container, in git history, or in GitHub releases; it exists
only on the researcher's machine (see `README.md`, deviation 2). Per the
milestone instruction, checkpoints were **not** regenerated.

So, honestly: **no one has still ever watched the trained swarm behave.**
The priority-one question of this milestone — what do the policies
actually do, and is there anything degenerate or absurd — remains open,
and the H1/H2 discrimination (Audit 2) remains open with it.

What was verified here:

- `che/scripts/render_episode.py` (in the pinned 8de4976 worktree and
  copied to the main tree) loads a checkpoint through the real
  `che.eval.harness.load_params` restore path (config-hash guard
  included), reproduces `rollout_episode`'s exact PRNG key discipline,
  and writes a GIF + summary JSON. Smoke-tested end-to-end with a
  2-update debug-scale checkpoint trained into scratch space (grid 16,
  4 agents; discarded, never an audit substitute): restore OK, 256
  frames, hazard/smoke/food/agent/death markers and per-frame metrics
  render correctly.
- The renderer's colormap conventions match `obs_alignment.png`
  (Fuel `#2d5016` dark green / Burning `#ff4500` / Burnt `#4a4a4a`,
  smoke as white alpha overlay, food yellow, alive cyan, dead black x).

Once the archive is extracted, the command loop in `README.md` renders
the ≥8 episodes per (low_s0/Low, high_s2/High, medium_s0/Medium) cell;
the 5–6 representative GIFs and the honest behavioral description belong
in this file, replacing this blocker note.
