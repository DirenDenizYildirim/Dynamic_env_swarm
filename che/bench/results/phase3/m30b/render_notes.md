# M3.0b Audit 1 — render notes

**Status: DONE (local run, 2026-07-20).** 24 episodes rendered — 8 each of
(low_s0 / Low), (medium_s0 / Medium), (high_s2 / High) — from the pinned
`8de4976` worktree through the real `che.eval.harness.load_params` restore
path (config-hash guard, old-schema hashes restored to the checkpoint dirs;
see the M3.0b closure section of `README.md`). All 24 GIFs + per-episode
summary JSONs are in `renders/`; the six representative GIFs cited below are
committed, the rest live untracked on the researcher's machine (regenerable
by seed — the renderer reproduces `rollout_episode`'s key discipline, so
`--seed N` is episode N deterministically).

## Outcome summary (per-episode finals)

| cell | completion (8 eps) | final alive / 12 |
|---|---|---|
| low_s0 / Low | 0.66–0.94 (median ≈ 0.77) | 12 in 7 eps, 11 in 1 |
| medium_s0 / Medium | 0.59–0.94 (median ≈ 0.82) | 10–12 |
| high_s2 / High | 0.78–0.97 (median ≈ 0.89) | 11–12 |

Consistent with the M3.0 eval means — no cherry-picking surprises.

## Honest behavioral description (what the swarm actually does)

**Nothing degenerate or absurd.** Agents move purposefully toward food,
collection is continuous while fire is live, deaths are near-misses at the
burning front, not suicidal walks into it. The policies are recognizably
doing the task. Three severity-specific behaviors, one of them a real
finding:

1. **High (β = 0.70, supercritical) — sweep, dodge, mop up.** One fire
   front crosses the whole arena by t ≈ 70–90 (`high_s2_ep0.gif`: 33 cells
   burning at t = 64, burnt-out by t ≈ 130). Agents dodge the front
   (typically 0–1 death), then collect on the burnt field arena-wide, where
   nothing can ignite again. Food is not consumed by fire (design: task
   state is hazard-independent, Def. 2), so completion keeps climbing after
   the burn — final completions 0.78–0.97, the best of the three cells.
   The post-sweep arena is objectively safe and the High policy exploits
   it fully.
2. **Medium (β = 0.49, near-critical) — post-fire abandonment of the burnt
   region. This is the audit's main behavioral finding.** The burn is
   dendritic and partial (~40% of the arena), dead by t ≈ 130. In
   `medium_s0_ep3.gif`, from t = 128 to t = 256 the 11 surviving agents
   hover on the green margin at the edge of the burnt cluster while ~13
   food items sit inside it — **zero food collected in the entire second
   half of the episode**, though burnt cells are passable and harmless
   (tested: `test_burnt_is_passable_and_harmless`). Completion stalls at
   0.59. Plausible mechanism, flagged for human judgment: the hazard obs
   plane encodes cell state / 2, so Burnt = 1.0 reads *higher* than
   Burning = 0.5 — to the network, ash literally looks more dangerous than
   fire. A Medium-trained policy always has a green half to retreat to and
   never has to learn that ash is safe; a High-trained policy has no green
   refuge after the sweep and does learn it. This would also explain the
   pooled completion ordering high > low > medium (M3.0 report). **Not a
   spec violation** — the encoding is as designed — but it is a
   representation choice with visible behavioral cost; any change is a
   design decision for the human (obs encoding is frozen under the
   ablation-nesting invariant).
3. **Low (β = 0.43, subcritical) — coverage-limited, not hazard-limited.**
   The fire fizzles to nothing (`low_s0_ep0.gif`: a few grey specks, zero
   burning from mid-episode). With no threat at all, completions still
   stall at 0.66–0.69 in 3 of 8 episodes: the swarm confines itself to a
   subregion (ep0: all 12 agents patrol the right half for the last 64
   steps while all remaining food sits in the left half). The Low policy's
   ceiling is exploration/coverage, not survival. Explains Low's low
   pooled completion variance (M3.0): outcomes are policy-limited, not
   environment-limited.

## Representative GIFs (committed)

- `high_s2_ep0.gif` — the sweep + arena-wide mop-up (completion 0.97).
- `high_s2_ep1.gif` — typical High episode (0.78, one death at the front).
- `medium_s0_ep3.gif` — **the abandonment finding** (0.59, food visibly
  stranded in the burnt cluster for 128 steps).
- `medium_s0_ep1.gif` — Medium with 2 deaths (worst survival rendered).
- `low_s0_ep0.gif`, `low_s0_ep5.gif` — subcritical stalls (0.66 both,
  12/12 alive, food left uncollected on open green field).
