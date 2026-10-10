"""Stage E mechanism GIFs, under the selection rule written in MANIFEST.md
before any render: θ* config, episode key 0, the random policy or the JOINT
seed-1 checkpoint at step 1000, every 2nd step at 12 fps, agent index 0.

Imports che read-only. The rollout reproduces che/scripts/render_episode.py's
`rollout_frames` key discipline exactly, so each render is the same episode
as the committed GIF for that policy (asserted against the committed
sidecar). Two layers env.step does not return are recomputed and asserted:

- Coupling A's per-cell seed mask: the step's own kernels and keys
  (structure_step, coupling_a_seed_mask, hazard_step, seed_ignitions), with
  structure' and hazard' asserted bitwise equal to env.step's, and the count
  equal to info["seeded_ignitions"].
- agent 0's crop without attenuation: observe() on the same post-step state
  with theta_live.kappa_B = 0 (τ = 1). Asserted: wherever the received crop's
  visibility plane is 1, its content equals the unattenuated crop's.

Usage (thread-capped, CPU):
  gif_mechanisms.py --policy random
  gif_mechanisms.py --policy joint --ckpt-dir <extracted ckpt_joint_s1>
"""

from __future__ import annotations

import argparse
import json

import jax
import jax.numpy as jnp
import matplotlib

matplotlib.use("Agg")
import common as C  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib import animation, colors  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Patch, Rectangle  # noqa: E402

from che.env.comms import aggregate  # noqa: E402
from che.env.config import load_config  # noqa: E402
from che.env.env import _OBS_STREAM, reset, step  # noqa: E402
from che.env.hazard import hazard_step, seed_ignitions  # noqa: E402
from che.env.observation import observe  # noqa: E402
from che.env.structure import coupling_a_seed_mask, structure_step  # noqa: E402
from che.env.tasks import occupancy_grid  # noqa: E402
from che.env.types import BURNING, COLLAPSED, INTACT  # noqa: E402
from che.eval.harness import load_params, make_policy_fn  # noqa: E402
from che.train.rollout import make_random_policy, zero_messages  # noqa: E402

CONFIG = "che/configs/theta_star_holdout.yaml"
RENDERS = C.ROOT / "paper" / "renders" / "2026-09-27"
SIDECAR = {
    "random": RENDERS / "thetastar_random_seed0.json",
    "joint": RENDERS / "thetastar_joint_s1_T1000_ep0.json",
}
POLICY_LABEL = {"random": "random policy", "joint": "JOINT policy (seed 1, T = 1000)"}
EVERY, FPS, AGENT = 2, 12, 0
# the committed renderer's palette (render_episode.py), kept for continuity
HAZ = colors.ListedColormap(["#2d5016", "#ff4500", "#4a4a4a"])
HAZ_NORM = colors.BoundaryNorm([0, 1, 2, 3], HAZ.N)
WEAK, SEED, FOOD, AGENT_C, UNSEEN = (
    "#e8d9a8",
    "#ff4fd8",
    "#ffd700",
    "#00e5ff",
    "#8c8c8c",
)


def rollout(policy, ecfg):
    jstep = jax.jit(lambda k, s, a: step(k, s, a, ecfg))
    th = ecfg.theta
    assert ecfg.hazard_mode == "dynamic"

    @jax.jit
    def kernels(k_step, state):
        # env.step's first two kernels, verbatim order and keys (env.py:298-327)
        tl = state.theta_live
        k_struct, k_seed, k_fire = jax.random.split(k_step, 3)
        occ_pre = occupancy_grid(state.agent_pos, state.agent_alive, ecfg.grid_size)
        s_new = structure_step(
            k_struct,
            state.structure,
            state.weak,
            occ_pre.astype(jnp.float32),
            lambda_0=th.lambda_0,
            lambda_load=th.lambda_load,
        )
        inc = (s_new == COLLAPSED) & (state.structure == INTACT)
        mask = coupling_a_seed_mask(k_seed, inc, kappa_A=tl.kappa_A, r_seed=th.r_seed)
        h_ca = hazard_step(k_fire, state.hazard, beta=tl.beta, iota=th.iota)
        h_new = seed_ignitions(h_ca, mask)
        return s_new, h_new, h_ca != h_new

    @jax.jit
    def crop_clear(state, key_obs):
        s0 = state.replace(
            theta_live=state.theta_live.replace(
                kappa_B=jnp.zeros_like(state.theta_live.kappa_B)
            )
        )
        return observe(s0, ecfg, key_obs)["grid"][AGENT]

    key = jax.random.PRNGKey(0)
    key, k_reset = jax.random.split(key)
    obs, state = reset(k_reset, ecfg)
    n_food0 = int(np.asarray(state.food).sum())
    seeded_ever = np.zeros((ecfg.grid_size,) * 2, bool)

    def snap(state, obs, clear, seeded, ret):
        return dict(
            t=int(state.t),
            hazard=np.asarray(state.hazard),
            smoke=np.asarray(state.smoke),
            structure=np.asarray(state.structure),
            weak=np.asarray(state.weak),
            food=np.asarray(state.food),
            pos=np.asarray(state.agent_pos),
            alive=np.asarray(state.agent_alive),
            seeded=seeded,
            seeded_ever=seeded_ever.copy(),
            seen=np.asarray(obs["grid"][AGENT]),
            clear=np.asarray(clear),
            ret=ret,
            completion=1.0 - float(np.asarray(state.food).sum()) / n_food0,
        )

    clear0 = crop_clear(state, jax.random.fold_in(k_reset, _OBS_STREAM))
    frames = [snap(state, obs, clear0, np.zeros_like(seeded_ever), 0.0)]
    messages = zero_messages(ecfg.n_agents)
    ret, n_seeds, n_steps_checked = 0.0, 0, 0
    for _ in range(ecfg.horizon):
        key, k_act, k_step = jax.random.split(key, 3)
        actions, messages = policy(k_act, obs, aggregate(messages, obs["links"]))
        s_mine, h_mine, seeded = kernels(k_step, state)
        obs, state, reward, done, info = jstep(k_step, state, actions)
        assert np.array_equal(np.asarray(s_mine), np.asarray(state.structure))
        assert np.array_equal(np.asarray(h_mine), np.asarray(state.hazard))
        seeded = np.asarray(seeded)
        assert int(seeded.sum()) == int(info["seeded_ignitions"])
        n_seeds += int(seeded.sum())
        seeded_ever |= seeded
        clear = crop_clear(state, jax.random.fold_in(k_step, _OBS_STREAM))
        ret += float(reward)
        frames.append(snap(state, obs, clear, seeded, ret))
        n_steps_checked += 1
        if bool(done):
            break
    # visible content of the received crop equals the unattenuated crop
    for f in frames:
        vis = f["seen"][..., 7] > 0.5
        assert np.array_equal(f["seen"][..., :7][vis], f["clear"][..., :7][vis])
        assert np.all(f["clear"][..., 7] == 1.0)
    return frames, dict(steps=n_steps_checked, seeds=n_seeds)


# ------------------------------------------------------------------ drawing
def draw_arena_A(ax, f, label):
    ax.clear()
    ax.imshow(f["hazard"], cmap=HAZ, norm=HAZ_NORM, interpolation="nearest")
    wr, wc = np.nonzero(f["weak"] & (f["structure"] == INTACT))
    ax.scatter(wc, wr, marker="s", s=2.2, c=WEAK, linewidths=0, zorder=2)
    cr, cc = np.nonzero(f["structure"] == COLLAPSED)
    ax.scatter(
        cc, cr, marker="s", s=13, c="#000000", edgecolors=WEAK, linewidths=0.5, zorder=3
    )
    er, ec = np.nonzero(f["seeded_ever"] & ~f["seeded_since"])
    ax.scatter(
        ec,
        er,
        marker="o",
        s=10,
        facecolors="none",
        edgecolors=SEED,
        linewidths=0.8,
        zorder=4,
    )
    nr, nc = np.nonzero(f["seeded_since"])
    ax.scatter(
        nc,
        nr,
        marker="o",
        s=95,
        facecolors="none",
        edgecolors=SEED,
        linewidths=2.0,
        zorder=5,
    )
    fr, fc = np.nonzero(f["food"])
    ax.scatter(fc, fr, marker="s", s=10, c=FOOD, linewidths=0, zorder=3)
    p, a = f["pos"], f["alive"]
    ax.scatter(
        p[a, 1],
        p[a, 0],
        marker="o",
        s=22,
        c=AGENT_C,
        edgecolors="white",
        linewidths=0.5,
        zorder=6,
    )
    ax.scatter(
        p[~a, 1], p[~a, 0], marker="x", s=22, c="black", linewidths=1.4, zorder=6
    )
    n = f["hazard"].shape[0]
    ax.set_xlim(-0.5, n - 0.5)
    ax.set_ylim(n - 0.5, -0.5)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(
        f"Coupling A, structure layer\n{label} · θ* · t = {f['t']:3d}", fontsize=8
    )
    ax.text(
        0.0,
        -0.035,
        f"collapsed cells {int((f['structure'] == COLLAPSED).sum())}   "
        f"Coupling-A ignitions so far {int(f['seeded_ever'].sum())}   "
        f"burning {int((f['hazard'] == BURNING).sum())}",  # no survivor tally
        transform=ax.transAxes,
        fontsize=7,
        va="top",
        ha="left",
    )


A_LEGEND = [
    Patch(facecolor="#2d5016", label="fuel"),
    Patch(facecolor="#ff4500", label="burning"),
    Patch(facecolor="#4a4a4a", label="burnt"),
    Line2D(
        [0],
        [0],
        marker="s",
        ls="none",
        mfc=WEAK,
        mec=WEAK,
        ms=3,
        label="weak cell (intact)",
    ),
    Line2D(
        [0],
        [0],
        marker="s",
        ls="none",
        mfc="#000000",
        mec=WEAK,
        ms=5,
        label="collapsed cell",
    ),
    Line2D(
        [0],
        [0],
        marker="o",
        ls="none",
        mfc="none",
        mec=SEED,
        mew=2,
        ms=8,
        label="Coupling-A ignition, since last frame",
    ),
    Line2D(
        [0],
        [0],
        marker="o",
        ls="none",
        mfc="none",
        mec=SEED,
        mew=0.8,
        ms=4,
        label="Coupling-A ignition, earlier",
    ),
    Line2D([0], [0], marker="s", ls="none", mfc=FOOD, mec=FOOD, ms=4, label="food"),
    Line2D(
        [0], [0], marker="o", ls="none", mfc=AGENT_C, mec="white", ms=5, label="agent"
    ),
    Line2D(
        [0], [0], marker="x", ls="none", color="black", ms=5, label="disabled agent"
    ),
]


OUTSIDE = "#e6e6e6"


def crop_rgb(g, received, oob):
    """9 x 9 crop from the obs planes: 0 burning, 1 burnt, 2 smoke, 3 food,
    4 weak, 5 collapsed, 6 alive occupancy, 7 visibility (v3)."""
    k = g.shape[0]
    rgb = np.empty((k, k, 3))
    rgb[:] = colors.to_rgb("#2d5016")
    rgb[g[..., 1] > 0.5] = colors.to_rgb("#4a4a4a")
    rgb[g[..., 0] > 0.5] = colors.to_rgb("#ff4500")
    rgb[g[..., 5] > 0.5] = (0, 0, 0)
    a = np.clip(g[..., 2], 0, 1)[..., None] * 0.7
    rgb = rgb * (1 - a) + a  # smoke: white overlay, as the committed renderer
    if received:
        rgb[g[..., 7] < 0.5] = colors.to_rgb(UNSEEN)
    rgb[oob] = colors.to_rgb(OUTSIDE)  # padded cells beyond the arena edge (obs pads 0)
    return rgb


def outside(pos, k, n):
    r = k // 2
    rows = pos[0] + np.arange(-r, r + 1)
    cols = pos[1] + np.arange(-r, r + 1)
    return ((rows < 0) | (rows >= n))[:, None] | ((cols < 0) | (cols >= n))[None, :]


def draw_crop(ax, g, title, received, oob):
    ax.clear()
    ax.imshow(crop_rgb(g, received, oob), interpolation="nearest")
    k = g.shape[0]
    vis = (g[..., 7] > 0.5 if received else np.ones((k, k), bool)) & ~oob
    weak_seen = (g[..., 4] > 0.5) & (g[..., 5] < 0.5) & vis
    for r, c in zip(*np.nonzero(weak_seen), strict=True):
        ax.add_patch(
            Rectangle((c - 0.5, r - 0.5), 1, 1, fill=False, ec=WEAK, lw=0.8, zorder=2)
        )
    fr, fc = np.nonzero((g[..., 3] > 0.5) & vis)
    ax.scatter(fc, fr, marker="s", s=60, c=FOOD, linewidths=0, zorder=3)
    orr, oc = np.nonzero((g[..., 6] > 0.5) & vis)
    ax.scatter(
        oc,
        orr,
        marker="o",
        s=90,
        c=AGENT_C,
        edgecolors="white",
        linewidths=0.7,
        zorder=4,
    )
    if received:
        ur, uc = np.nonzero((g[..., 7] < 0.5) & ~oob)
        ax.scatter(uc, ur, marker="x", s=40, c="#ffffff", linewidths=1.0, zorder=4)
    ax.add_patch(
        Rectangle(
            (k // 2 - 0.5, k // 2 - 0.5), 1, 1, fill=False, ec="white", lw=1.6, zorder=5
        )
    )
    ax.set_xticks(np.arange(-0.5, k, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, k, 1), minor=True)
    ax.grid(which="minor", color="#000000", lw=0.3, alpha=0.35)
    ax.tick_params(which="both", length=0, labelbottom=False, labelleft=False)
    ax.set_title(title, fontsize=7.6)


def draw_B(axes, f, label, n):
    a0, a1, a2 = axes
    a0.clear()
    a0.imshow(f["hazard"], cmap=HAZ, norm=HAZ_NORM, interpolation="nearest")
    alpha = np.clip(f["smoke"], 0, 1) * 0.7
    a0.imshow(np.ones((*f["smoke"].shape, 3)), interpolation="nearest", alpha=alpha)
    fr, fc = np.nonzero(f["food"])
    a0.scatter(fc, fr, marker="s", s=6, c=FOOD, linewidths=0, zorder=3)
    p, al = f["pos"], f["alive"]
    a0.scatter(
        p[al, 1],
        p[al, 0],
        marker="o",
        s=14,
        c=AGENT_C,
        edgecolors="white",
        linewidths=0.4,
        zorder=4,
    )
    a0.scatter(
        p[~al, 1], p[~al, 0], marker="x", s=14, c="black", linewidths=1.2, zorder=4
    )
    r, c = p[AGENT]
    a0.add_patch(
        Rectangle((c - 4.5, r - 4.5), 9, 9, fill=False, ec="white", lw=1.4, zorder=5)
    )
    a0.set_xlim(-0.5, n - 0.5)
    a0.set_ylim(n - 0.5, -0.5)
    a0.set_xticks([])
    a0.set_yticks([])
    a0.set_title(f"{label} · θ* · t = {f['t']:3d}", fontsize=7.6)
    seen = f["seen"]
    n_unseen = int((seen[..., 7] < 0.5).sum())
    fire_in = bool((f["clear"][..., 0] > 0.5).any())
    state = "alive" if f["alive"][AGENT] else "disabled"
    oob = outside(p[AGENT], seen.shape[0], n)
    draw_crop(a1, f["clear"], "agent 0, without attenuation (κ_B = 0)", False, oob)
    draw_crop(a2, seen, "agent 0, as received (κ_B = 1.0)", True, oob)
    a1.text(
        0.0,
        -0.04,
        f"agent 0 {state} · fire in crop: {'yes' if fire_in else 'no'}",
        transform=a1.transAxes,
        fontsize=7,
        va="top",
    )
    a2.text(
        0.0,
        -0.04,
        f"unseen cells: {n_unseen} of 81",
        transform=a2.transAxes,
        fontsize=7,
        va="top",
    )


B_LEGEND = [
    Patch(facecolor="#2d5016", label="fuel"),
    Patch(facecolor="#ff4500", label="burning"),
    Patch(facecolor="#4a4a4a", label="burnt"),
    Patch(facecolor="#000000", label="collapsed"),
    Patch(facecolor="#ffffff", edgecolor="#999999", label="smoke (white overlay)"),
    Patch(facecolor="none", edgecolor=WEAK, label="weak cell"),
    Line2D([0], [0], marker="s", ls="none", mfc=FOOD, mec=FOOD, ms=5, label="food"),
    Line2D(
        [0], [0], marker="o", ls="none", mfc=AGENT_C, mec="white", ms=6, label="agent"
    ),
    Patch(facecolor=UNSEEN, label="unseen (masked by Beer–Lambert)"),
    Patch(facecolor=OUTSIDE, edgecolor="#999999", label="outside the arena"),
]


def mark_since(frames):
    """Coupling-A ignitions since the previous SHOWN frame (none lost to skipping)."""
    shown = frames[::EVERY]
    if shown[-1] is not frames[-1]:
        shown.append(frames[-1])
    idx = [f["t"] for f in shown]
    by_t = {f["t"]: f for f in frames}
    prev = -1
    for f, t in zip(shown, idx, strict=False):
        acc = np.zeros_like(f["seeded"])
        for u in range(prev + 1, t + 1):
            acc |= by_t[u]["seeded"]
        f["seeded_since"] = acc
        prev = t
    return shown


def save_gif(fig, update, shown, name):
    anim = animation.FuncAnimation(fig, update, frames=shown, interval=1000 // FPS)
    p = C.GIF / name
    anim.save(p, writer=animation.PillowWriter(fps=FPS))
    plt.close(fig)
    return p


def static_strip(draw, ncols_per, shown, name, figsize, legend):
    picks = [f for f in shown if f["t"] in (0, 128, 256)]
    assert [f["t"] for f in picks] == [0, 128, 256]
    fig = plt.figure(figsize=figsize, dpi=110)
    if ncols_per == 1:
        axs = fig.subplots(1, 3)
        for ax, f in zip(axs, picks, strict=False):
            draw(ax, f)
    else:
        axs = fig.subplots(3, 3, gridspec_kw={"width_ratios": [1.25, 1, 1]})
        for row, f in zip(axs, picks, strict=False):
            draw(row, f)
    fig.legend(
        handles=legend,
        loc="lower center",
        ncol=5,
        fontsize=6.6,
        frameon=False,
        bbox_to_anchor=(0.5, -0.01),
    )
    fig.subplots_adjust(
        bottom=0.12 if ncols_per == 1 else 0.07, wspace=0.08, hspace=0.32
    )
    p = C.IMG / name
    fig.savefig(
        p, dpi=110, metadata={"Software": None}, bbox_inches="tight", pad_inches=0.05
    )
    plt.close(fig)
    return p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--policy", choices=("random", "joint"), required=True)
    ap.add_argument("--ckpt-dir")
    args = ap.parse_args()
    cfg = load_config(CONFIG)  # run from the repo root, as the committed renders were
    ecfg = cfg.env
    side = C.load_json(SIDECAR[args.policy])
    if args.policy == "random":
        policy = make_random_policy(ecfg.n_agents)
    else:
        params, ckpt_step = load_params(
            args.ckpt_dir, cfg, allow_hashes=tuple(side["allow_hash"])
        )
        assert ckpt_step == 1000, ckpt_step
        policy = make_policy_fn(cfg, params, greedy=False)
    frames, stats = rollout(policy, ecfg)
    last = frames[-1]
    got = dict(
        steps=last["t"],
        final_completion=last["completion"],
        final_alive=int(last["alive"].sum()),
        episode_return=last["ret"],
    )
    want = {k: side[k] for k in got}
    assert got == want, (got, want)  # the same episode as the committed render
    print("same episode as the committed render:", got, "| seeds", stats)

    label = POLICY_LABEL[args.policy]
    tag = "random" if args.policy == "random" else "joint_s1_T1000"
    shown = mark_since(frames)
    n = ecfg.grid_size

    # ---- mechanism A
    figA = plt.figure(figsize=(5.4, 6.3), dpi=110)
    axA = figA.add_axes([0.04, 0.2, 0.92, 0.71])
    figA.legend(
        handles=A_LEGEND,
        loc="lower center",
        ncol=3,
        fontsize=6.4,
        frameon=False,
        bbox_to_anchor=(0.5, 0.0),
    )
    pA = save_gif(
        figA,
        lambda f: draw_arena_A(axA, f, label),
        shown,
        f"mechA_structure_{tag}_ep0.gif",
    )
    sA = static_strip(
        lambda ax, f: draw_arena_A(ax, f, label),
        1,
        shown,
        f"mechA_structure_{tag}_ep0_static.png",
        (14.5, 5.6),
        A_LEGEND,
    )

    # ---- mechanism B
    figB = plt.figure(figsize=(10.24, 4.0), dpi=100)  # integral pixels: 1024 x 400
    axB = figB.subplots(1, 3, gridspec_kw={"width_ratios": [1.25, 1, 1]})
    figB.legend(
        handles=B_LEGEND,
        loc="lower center",
        ncol=5,
        fontsize=6.4,
        frameon=False,
        bbox_to_anchor=(0.5, 0.0),
    )
    figB.subplots_adjust(left=0.02, right=0.98, top=0.9, bottom=0.17, wspace=0.12)
    pB = save_gif(
        figB,
        lambda f: draw_B(axB, f, label, n),
        shown,
        f"mechB_agent0_view_{tag}_ep0.gif",
    )
    sB = static_strip(
        lambda row, f: draw_B(row, f, label, n),
        3,
        shown,
        f"mechB_agent0_view_{tag}_ep0_static.png",
        (10.2, 11.5),
        B_LEGEND,
    )

    danger = sum(
        1 for f in frames if (f["clear"][..., 0] > 0.5).any() and f["alive"][AGENT]
    )
    masked_steps = sum(1 for f in frames if (f["seen"][..., 7] < 0.5).any())
    summ = dict(
        policy=args.policy,
        **got,
        coupling_a_ignitions=stats["seeds"],
        collapsed_final=int((last["structure"] == COLLAPSED).sum()),
        agent0_steps_fire_in_crop=danger,
        agent0_steps_any_cell_masked=masked_steps,
        frames_shown=len(shown),
    )
    print(json.dumps(summ))
    for p in (pA, sA, pB, sB):
        print(p.name, p.stat().st_size)


if __name__ == "__main__":
    main()
