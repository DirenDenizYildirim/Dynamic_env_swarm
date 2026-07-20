"""M3.0b Audit 1: render one episode of a trained policy to a GIF.

Loads a checkpoint through the M3.0 harness restore path (config-hash
guarded, che.eval.harness.load_params), rolls out ONE episode at debug
speed (Python loop over a jitted step — CPU fine), and writes a GIF:

- hazard field:  Fuel / Burning / Burnt colormap
- smoke field:   white alpha overlay (alpha = clip(rho, 0, 1) * 0.7)
- food:          yellow squares
- agents:        alive = cyan circles, dead = black x
- per-frame step counter + running metrics (alive, completion, return)

The rollout reproduces rollout_episode's key discipline exactly
(key -> (key, k_act, k_step) per step, actions from k_act, step from
k_step) so a rendered episode with seed s is the same episode
batch_rollout would produce for that per-episode key — but here the key
is the episode key directly (pass --seed to vary episodes).

--random-policy renders the untrained baseline (also used to smoke-test
this script when checkpoints are unavailable; never a substitute for a
trained-policy audit).
"""

import argparse
import dataclasses
import json
from pathlib import Path

import jax
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation, colors

from che.env.config import load_config
from che.env.env import reset, step
from che.env.types import BURNING
from che.eval.harness import load_params, make_policy_fn
from che.train.rollout import make_random_policy

HAZARD_CMAP = colors.ListedColormap(["#2d5016", "#ff4500", "#4a4a4a"])
HAZARD_NORM = colors.BoundaryNorm([0, 1, 2, 3], HAZARD_CMAP.N)


def rollout_frames(key: jax.Array, ecfg, policy):
    """One episode; returns a list of per-step frame dicts (t=0 included)."""
    jstep = jax.jit(lambda k, s, a: step(k, s, a, ecfg))
    key, k_reset = jax.random.split(key)
    obs, state = reset(k_reset, ecfg)
    n_food0 = int(np.asarray(state.food).sum())

    def snap(state, reward, ep_return):
        return {
            "t": int(state.t),
            "hazard": np.asarray(state.hazard),
            "smoke": np.asarray(state.smoke),
            "food": np.asarray(state.food),
            "pos": np.asarray(state.agent_pos),
            "alive": np.asarray(state.agent_alive),
            "reward": float(reward),
            "return": float(ep_return),
            "completion": 1.0 - float(np.asarray(state.food).sum()) / n_food0,
        }

    frames = [snap(state, 0.0, 0.0)]
    ep_return = 0.0
    for _ in range(ecfg.horizon):
        key, k_act, k_step = jax.random.split(key, 3)
        actions = policy(k_act, obs)
        obs, state, reward, done, _info = jstep(k_step, state, actions)
        ep_return += float(reward)
        frames.append(snap(state, float(reward), ep_return))
        if bool(done):
            break
    return frames


def draw_frame(ax, frame, n_agents: int, grid_size: int, tag: str):
    ax.clear()
    ax.imshow(
        frame["hazard"],
        cmap=HAZARD_CMAP,
        norm=HAZARD_NORM,
        origin="upper",
        interpolation="nearest",
    )
    # Smoke: white overlay, alpha from density (rho is bounded ~ sigma_s/(1-e^-eta)).
    alpha = np.clip(frame["smoke"], 0.0, 1.0) * 0.7
    ax.imshow(
        np.ones((*frame["smoke"].shape, 3)),
        origin="upper",
        interpolation="nearest",
        alpha=alpha,
    )
    fr, fc = np.nonzero(frame["food"])
    ax.scatter(fc, fr, marker="s", s=14, c="#ffd700", edgecolors="none", zorder=3)
    alive, pos = frame["alive"], frame["pos"]
    ax.scatter(
        pos[alive, 1], pos[alive, 0], marker="o", s=26, c="#00e5ff",
        edgecolors="white", linewidths=0.5, zorder=4,
    )
    ax.scatter(
        pos[~alive, 1], pos[~alive, 0], marker="x", s=26, c="black",
        linewidths=1.5, zorder=4,
    )
    burning = int((frame["hazard"] == BURNING).sum())
    ax.set_title(
        f"{tag}  t={frame['t']:3d}  alive {int(alive.sum())}/{n_agents}  "
        f"compl {frame['completion']:.2f}  ret {frame['return']:+.1f}  "
        f"burning {burning}",
        fontsize=8,
    )
    ax.set_xlim(-0.5, grid_size - 0.5)
    ax.set_ylim(grid_size - 0.5, -0.5)
    ax.set_xticks([])
    ax.set_yticks([])


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--config", required=True)
    p.add_argument("--ckpt-dir", help="orbax checkpoint dir (harness restore path)")
    p.add_argument("--random-policy", action="store_true",
                   help="render the untrained random baseline instead")
    p.add_argument("--death-penalty", type=float, default=None,
                   help="theta override — must match training (hash guard)")
    p.add_argument("--obs-version", type=int, default=None, choices=(1, 2),
                   help="override cfg obs_version — archival renders of "
                        "obs-v1 checkpoints only (D5)")
    p.add_argument("--allow-hash", action="append", default=[],
                   metavar="HASH",
                   help="accept this named legacy checkpoint hash (see "
                        "che.eval.harness); recorded in the summary JSON")
    p.add_argument("--seed", type=int, default=0, help="episode key seed")
    p.add_argument("--greedy", action="store_true")
    p.add_argument("--every", type=int, default=1, help="render every Nth step")
    p.add_argument("--fps", type=int, default=10)
    p.add_argument("--out", required=True, help="output .gif path")
    p.add_argument("--tag", default="", help="short label shown in the title")
    args = p.parse_args(argv)
    if bool(args.ckpt_dir) == bool(args.random_policy):
        p.error("exactly one of --ckpt-dir / --random-policy")

    cfg = load_config(args.config)
    if args.death_penalty is not None:
        cfg = dataclasses.replace(
            cfg,
            env=dataclasses.replace(
                cfg.env,
                theta=dataclasses.replace(
                    cfg.env.theta, death_penalty=args.death_penalty
                ),
            ),
        )
    if args.obs_version is not None:
        cfg = dataclasses.replace(
            cfg, env=dataclasses.replace(cfg.env, obs_version=args.obs_version)
        )
    ecfg = cfg.env
    if args.random_policy:
        policy = make_random_policy(ecfg.n_agents)
    else:
        params, ckpt_step = load_params(
            args.ckpt_dir, cfg, allow_hashes=tuple(args.allow_hash)
        )
        policy = make_policy_fn(cfg, params, greedy=args.greedy)
        print(f"restored {args.ckpt_dir} @ step {ckpt_step}")

    frames = rollout_frames(jax.random.PRNGKey(args.seed), ecfg, policy)
    shown = frames[:: args.every]
    if shown[-1] is not frames[-1]:
        shown.append(frames[-1])  # always end on the final state

    fig, ax = plt.subplots(figsize=(5.4, 5.8), dpi=110)
    anim = animation.FuncAnimation(
        fig,
        lambda f: draw_frame(ax, f, ecfg.n_agents, ecfg.grid_size, args.tag),
        frames=shown,
        interval=1000 // args.fps,
    )
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    anim.save(out, writer=animation.PillowWriter(fps=args.fps))
    plt.close(fig)

    last = frames[-1]
    summary = {
        "config": args.config,
        "ckpt_dir": args.ckpt_dir,
        "seed": args.seed,
        "greedy": args.greedy,
        "obs_version": cfg.env.obs_version,
        "allow_hash": args.allow_hash or None,
        "steps": last["t"],
        "final_completion": last["completion"],
        "final_alive": int(last["alive"].sum()),
        "n_agents": ecfg.n_agents,
        "episode_return": last["return"],
    }
    out.with_suffix(".json").write_text(json.dumps(summary, indent=1) + "\n")
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
