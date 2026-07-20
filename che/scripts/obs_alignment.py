"""M3.0b Audit 4: obs-alignment visual check.

One figure, three timesteps of one episode. Each row shows the global
grid annotated with one agent's position (red ring) and its k x k crop
boundary (red rectangle), beside the agent's actual per-plane crop
exactly as the network receives it (obs["grid"][agent, :, :, p] from
observe(), i.e. the post-step observation returned by env.step).

A transposition or off-by-one must be visible by inspection: the crop
panels carry the same hazard colormap / overlays as the global view, the
crop center cell is ringed, and both views share the row-down/col-right
imshow orientation, so the fire/smoke/food pattern inside the red
rectangle must match plane panels cell-for-cell.

Policy: random by default (alignment is a property of observe(), not of
the policy); --ckpt-dir renders a trained policy's episode instead.
"""

import argparse
import dataclasses
from pathlib import Path

import jax
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors, patches

from che.env.config import load_config
from che.env.env import reset, step
from che.env.observation import n_planes
from che.env.types import BURNING
from che.eval.harness import load_params, make_policy_fn
from che.train.rollout import make_random_policy

HAZARD_CMAP = colors.ListedColormap(["#2d5016", "#ff4500", "#4a4a4a"])
HAZARD_NORM = colors.BoundaryNorm([0, 1, 2, 3], HAZARD_CMAP.N)
PLANE_NAMES = {  # per obs_version (D5)
    1: ["hazard (h/2)", "smoke (rho)", "food", "structure", "alive occ"],
    2: ["burning", "burnt", "smoke (rho)", "food", "weak", "collapsed",
        "alive occ"],
}


def rollout_records(key, ecfg, policy):
    """Per-step (state, obs) records; obs[t] is the post-step obs of state[t]."""
    jstep = jax.jit(lambda k, s, a: step(k, s, a, ecfg))
    key, k_reset = jax.random.split(key)
    obs, state = reset(k_reset, ecfg)
    records = [(state, obs)]
    for _ in range(ecfg.horizon):
        key, k_act, k_step = jax.random.split(key, 3)
        actions = policy(k_act, obs)
        obs, state, _r, done, _i = jstep(k_step, state, actions)
        records.append((state, obs))
        if bool(done):
            break
    return records


def pick_agent(records, timesteps):
    """An agent alive at every chosen t, closest to fire at the middle t."""
    n_agents = np.asarray(records[0][0].agent_alive).shape[0]
    alive_all = np.ones(n_agents, dtype=bool)
    for t in timesteps:
        alive_all &= np.asarray(records[t][0].agent_alive)
    if not alive_all.any():
        raise SystemExit("no agent alive at all chosen timesteps — retune -t")
    t_mid = timesteps[len(timesteps) // 2]
    state = records[t_mid][0]
    burn_r, burn_c = np.nonzero(np.asarray(state.hazard) == BURNING)
    pos = np.asarray(state.agent_pos)
    if burn_r.size == 0:
        return int(np.nonzero(alive_all)[0][0])
    d = np.abs(pos[:, 0:1] - burn_r) + np.abs(pos[:, 1:2] - burn_c)
    dmin = np.where(alive_all, d.min(axis=1), np.inf)
    return int(dmin.argmin())


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--config", required=True)
    p.add_argument("--ckpt-dir")
    p.add_argument("--death-penalty", type=float, default=None)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("-t", "--timesteps", default="30,80,150",
                   help="comma-separated env steps to show")
    p.add_argument("--agent", type=int, default=None,
                   help="agent index (default: alive-and-nearest-fire)")
    p.add_argument("--out", required=True, help="output .png path")
    args = p.parse_args(argv)

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
    ecfg = cfg.env
    if args.ckpt_dir:
        params, _ = load_params(args.ckpt_dir, cfg)
        policy = make_policy_fn(cfg, params)
    else:
        policy = make_random_policy(ecfg.n_agents)

    records = rollout_records(jax.random.PRNGKey(args.seed), ecfg, policy)
    timesteps = [int(t) for t in args.timesteps.split(",")]
    for t in timesteps:
        if t >= len(records):
            raise SystemExit(f"t={t} beyond episode length {len(records) - 1}")
    a = args.agent if args.agent is not None else pick_agent(records, timesteps)
    k = ecfg.obs_window
    r = k // 2

    n_ch = n_planes(ecfg)
    plane_names = PLANE_NAMES[ecfg.obs_version]
    fig, axes = plt.subplots(
        len(timesteps), 1 + n_ch,
        figsize=(2.3 * (1 + n_ch), 2.6 * len(timesteps)), dpi=130,
    )
    for row, t in enumerate(timesteps):
        state, obs = records[t]
        hazard = np.asarray(state.hazard)
        smoke = np.asarray(state.smoke)
        food = np.asarray(state.food)
        pos = np.asarray(state.agent_pos)
        alive = np.asarray(state.agent_alive)
        crop = np.asarray(obs["grid"][a])  # [k, k, N_PLANES] as the net sees it

        ax = axes[row, 0]
        ax.imshow(hazard, cmap=HAZARD_CMAP, norm=HAZARD_NORM,
                  origin="upper", interpolation="nearest")
        ax.imshow(np.ones((*smoke.shape, 3)), origin="upper",
                  interpolation="nearest", alpha=np.clip(smoke, 0, 1) * 0.7)
        fr, fc = np.nonzero(food)
        ax.scatter(fc, fr, marker="s", s=8, c="#ffd700", zorder=3)
        ax.scatter(pos[alive, 1], pos[alive, 0], s=12, c="#00e5ff",
                   edgecolors="white", linewidths=0.4, zorder=4)
        ar, ac = pos[a]
        ax.scatter([ac], [ar], s=60, facecolors="none", edgecolors="red",
                   linewidths=1.4, zorder=5)
        ax.add_patch(patches.Rectangle(
            (ac - r - 0.5, ar - r - 0.5), k, k,
            fill=False, edgecolor="red", linewidth=1.2, zorder=5))
        ax.set_title(f"t={t}  agent {a} @ (r={ar}, c={ac})", fontsize=8)
        ax.set_xlim(-0.5, ecfg.grid_size - 0.5)
        ax.set_ylim(ecfg.grid_size - 0.5, -0.5)
        ax.set_xticks([])
        ax.set_yticks([])
        if row == 0:
            ax.set_ylabel("row (down) ->", fontsize=7)

        for pl in range(n_ch):
            ax = axes[row, 1 + pl]
            if ecfg.obs_version == 1 and pl == 0:
                # v1 hazard plane is h/2 in {0, .5, 1} — same colormap
                ax.imshow(crop[:, :, 0] * 2.0, cmap=HAZARD_CMAP,
                          norm=HAZARD_NORM, origin="upper",
                          interpolation="nearest")
            else:
                ax.imshow(crop[:, :, pl], cmap="viridis", vmin=0.0,
                          vmax=max(1.0, float(crop[:, :, pl].max())),
                          origin="upper", interpolation="nearest")
            ax.scatter([r], [r], s=40, facecolors="none", edgecolors="red",
                       linewidths=1.0, zorder=5)
            ax.set_xticks(range(0, k, 2))
            ax.set_yticks(range(0, k, 2))
            ax.tick_params(labelsize=5, length=2)
            if row == 0:
                ax.set_title(f"plane {pl}: {plane_names[pl]}", fontsize=7)

    fig.suptitle(
        f"obs v{ecfg.obs_version} alignment — red rect on the global grid "
        "vs the agent's actual "
        f"{k}x{k} crop (rows down, cols right; center cell ringed)",
        fontsize=9,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out)
    print(f"wrote {out} (agent {a}, timesteps {timesteps})")


if __name__ == "__main__":
    main()
