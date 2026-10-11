"""Per-frame state of the three pre-selected episodes, for the episode explorer.

Selection rule (fixed 2026-09-27, `paper/renders/2026-09-27/README.md`;
restated, not changed): theta* = che/configs/theta_star_holdout.yaml, episode
key jax.random.PRNGKey(0), stochastic actions (no --greedy); the random
policy; ISO and JOINT training seed 1 at update 1000 from
che/bench/results/phase6/g1_conf_5090/, restored cross-config with the
README's --allow-hash values. Nothing is chosen from a set.

Identity, asserted for every episode:

1. The REFERENCE trajectory is `che.scripts.render_episode.rollout_frames`,
   called unmodified with the inputs `render_episode.main()` builds. The
   instrumented rollout below mirrors its key discipline line by line, and
   the sha256 of (hazard, smoke, food, agent_pos, agent_alive) must match
   the reference at every one of the 257 states.
2. Final alive count, completion and return equal the committed render
   JSONs of 2026-09-27.
3. Collapse-seeded ignition cells are recovered by re-running the step's
   own kernels (structure_step, coupling_a_seed_mask, hazard_step,
   seed_ignitions) on the step's key split; asserted to reproduce h' and c'
   bitwise and info["seeded_ignitions"] / info["collapse_events"] exactly.
4. Each observation is asserted equal to (true 9x9 crop x reveal, reveal),
   so the explorer stores the reveal bits only. tau comes from the env's
   own `transmittance`; the reveal draw is re-run from the step's obs stream
   and asserted to equal the visibility plane, so the stored tau is the tau
   the draw used.

Reads che/ read-only. Writes only under paper/figures/interactive/out/data/.
Run (CPU, thread-capped), from the repo root:

    OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 \
    XLA_FLAGS=--xla_cpu_multi_thread_eigen=false nice -n 15 \
    uv run python paper/figures/interactive/src/extract_episodes.py --scratch <dir>
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "out" / "data"
REPO = HERE.parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402

import che.scripts.render_episode as RE  # noqa: E402
from che.env.comms import aggregate  # noqa: E402
from che.env.config import load_config  # noqa: E402
from che.env.env import _OBS_STREAM, reset, step  # noqa: E402
from che.env.hazard import hazard_step, seed_ignitions  # noqa: E402
from che.env.observation import transmittance  # noqa: E402
from che.env.structure import coupling_a_seed_mask, structure_step  # noqa: E402
from che.env.tasks import occupancy_grid  # noqa: E402
from che.env.types import BURNING, BURNT, COLLAPSED, INTACT  # noqa: E402
from che.eval.harness import load_params, make_policy_fn  # noqa: E402
from che.train.rollout import make_random_policy, zero_messages  # noqa: E402

CONFIG = "che/configs/theta_star_holdout.yaml"
EPISODE_SEED = 0
CKPT_DIR = REPO / "che/bench/results/phase6/g1_conf_5090"
RENDERS = REPO / "paper/renders/2026-09-27"

EPISODES = (
    dict(stem="thetastar_random_seed0", archive=None),
    dict(
        stem="thetastar_iso_s1_T1000_ep0",
        archive="ckpt_iso_s1.tar.zst",
        sha256="0fc9fd0c6bb84a09a9fdacfd80e24f85339a0d3d3858f072b0852a4466cf3b5a",
        allow_hash="b63fc2d6764c7ffe",
    ),
    dict(
        stem="thetastar_joint_s1_T1000_ep0",
        archive="ckpt_joint_s1.tar.zst",
        sha256="64c49ef8fc8c28b6234b4e3ed03812967f15beb49eadcbb31feff5c38ec19e61",
        allow_hash="da6617b402b08b9b",
    ),
)


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def frame_digest(hazard, smoke, food, pos, alive) -> str:
    h = hashlib.sha256()
    for a, dt in (
        (hazard, np.uint8),
        (smoke, np.float32),
        (food, np.uint8),
        (pos, np.int32),
        (alive, np.bool_),
    ):
        a = np.ascontiguousarray(np.asarray(a))
        assert a.dtype == dt, (a.dtype, dt)
        h.update(a.tobytes())
    return h.hexdigest()


def make_policy(ep, cfg, scratch: Path):
    if ep["archive"] is None:
        return make_random_policy(cfg.env.n_agents), None
    arch = CKPT_DIR / ep["archive"]
    got = sha256_file(arch)
    listed = (CKPT_DIR / "SHA256_CKPT.txt").read_text()
    assert got == ep["sha256"], f"sha256 mismatch for {arch.name}"
    assert any(
        line.split()[0] == got and line.split()[1].endswith(ep["archive"])
        for line in listed.splitlines()
        if line.strip()
    ), "not in SHA256_CKPT.txt"
    dest = scratch / ep["archive"].replace(".tar.zst", "")
    if not dest.exists():
        subprocess.run(
            ["tar", "--zstd", "-xf", str(arch), "-C", str(scratch)], check=True
        )
    params, ckpt_step = load_params(dest, cfg, allow_hashes=(ep["allow_hash"],))
    assert int(ckpt_step) == 1000, ckpt_step
    return make_policy_fn(cfg, params, greedy=False), int(ckpt_step)


def true_crops(state, k: int) -> np.ndarray:
    """The obs-v3 content planes (observation.py plane order), unmasked,
    cropped around each agent with zero padding: [n, k, k, 7]."""
    hz = np.asarray(state.hazard)
    L = hz.shape[0]
    occ = np.zeros((L, L), np.float32)
    pos = np.asarray(state.agent_pos)
    alive = np.asarray(state.agent_alive)
    for (r, c), a in zip(pos, alive, strict=True):
        if a:
            occ[r, c] = 1.0
    planes = np.stack(
        [
            (hz == BURNING).astype(np.float32),
            (hz == BURNT).astype(np.float32),
            np.asarray(state.smoke, np.float32),
            np.asarray(state.food).astype(np.float32),
            np.asarray(state.weak).astype(np.float32),
            (np.asarray(state.structure) == COLLAPSED).astype(np.float32),
            occ,
        ],
        axis=-1,
    )
    r = k // 2
    padded = np.pad(planes, ((r, r), (r, r), (0, 0)))
    return np.stack([padded[p0 : p0 + k, p1 : p1 + k] for p0, p1 in pos])


def instrumented_rollout(key, ecfg, policy):
    """Mirrors RE.rollout_frames exactly; also records obs, info and the
    step-internal Coupling-A masks recovered from the env's own kernels."""
    th = ecfg.theta
    jstep = jax.jit(lambda k, s, a: step(k, s, a, ecfg))

    @jax.jit
    def internals(k_step, state):
        tl = state.theta_live
        k_struct, k_seed, k_fire = jax.random.split(k_step, 3)
        occ_pre = occupancy_grid(state.agent_pos, state.agent_alive, ecfg.grid_size)
        structure_new = structure_step(
            k_struct,
            state.structure,
            state.weak,
            occ_pre.astype(jnp.float32),
            lambda_0=th.lambda_0,
            lambda_load=th.lambda_load,
        )
        inc = (structure_new == COLLAPSED) & (state.structure == INTACT)
        seed_mask = coupling_a_seed_mask(
            k_seed, inc, kappa_A=tl.kappa_A, r_seed=th.r_seed
        )
        hazard_ca = hazard_step(k_fire, state.hazard, beta=tl.beta, iota=th.iota)
        hazard_new = seed_ignitions(hazard_ca, seed_mask)
        return structure_new, inc, hazard_new, hazard_ca != hazard_new

    @jax.jit
    def tau_and_reveal(obs_key, state):
        tau = transmittance(
            state.smoke,
            state.agent_pos,
            kappa_B=state.theta_live.kappa_B,
            k=ecfg.obs_window,
        )
        reveal = jax.random.uniform(obs_key, tau.shape) < tau
        return tau, reveal

    k = ecfg.obs_window
    key, k_reset = jax.random.split(key)
    obs, state = reset(k_reset, ecfg)
    n_food0 = int(np.asarray(state.food).sum())
    rec = dict(
        hazard=[],
        smoke=[],
        food=[],
        pos=[],
        alive=[],
        structure=[],
        reveal=[],
        tau=[],
        seeded=[],
        collapse_inc=[],
        completion=[],
        ret=[],
        digest=[],
    )
    weak = np.asarray(state.weak)

    def record(state, obs, obs_key, ep_return, seeded, inc):
        grid = np.asarray(obs["grid"])
        crops = true_crops(state, k)
        vis = grid[..., 7]
        assert np.array_equal(grid[..., :7], crops * vis[..., None]), (
            "obs != crop x reveal"
        )
        assert set(np.unique(vis)).issubset({0.0, 1.0})
        tau, reveal = tau_and_reveal(obs_key, state)
        tau, reveal = np.asarray(tau), np.asarray(reveal)
        assert np.array_equal(reveal.astype(np.float32), vis), (
            "reveal re-draw != obs plane"
        )
        assert np.array_equal(np.asarray(state.weak), weak)
        rec["hazard"].append(np.asarray(state.hazard))
        rec["smoke"].append(np.asarray(state.smoke))
        rec["food"].append(np.asarray(state.food))
        rec["pos"].append(np.asarray(state.agent_pos))
        rec["alive"].append(np.asarray(state.agent_alive))
        rec["structure"].append(np.asarray(state.structure))
        rec["reveal"].append(reveal)
        rec["tau"].append(tau.astype(np.float32))
        rec["seeded"].append(seeded)
        rec["collapse_inc"].append(inc)
        rec["completion"].append(1.0 - float(np.asarray(state.food).sum()) / n_food0)
        rec["ret"].append(ep_return)
        rec["digest"].append(
            frame_digest(
                state.hazard,
                state.smoke,
                state.food,
                state.agent_pos,
                state.agent_alive,
            )
        )

    L = ecfg.grid_size
    zeros = np.zeros((L, L), bool)
    record(state, obs, jax.random.fold_in(k_reset, _OBS_STREAM), 0.0, zeros, zeros)
    ep_return = 0.0
    messages = zero_messages(ecfg.n_agents)
    n_seeded = n_collapse = 0
    for _ in range(ecfg.horizon):
        key, k_act, k_step = jax.random.split(key, 3)
        actions, messages = policy(k_act, obs, aggregate(messages, obs["links"]))
        s_new, inc, h_new, seeded = internals(k_step, state)
        obs, state_next, reward, done, info = jstep(k_step, state, actions)
        assert np.array_equal(np.asarray(h_new), np.asarray(state_next.hazard)), (
            "h' recompute"
        )
        assert np.array_equal(np.asarray(s_new), np.asarray(state_next.structure)), (
            "c' recompute"
        )
        seeded, inc = np.asarray(seeded), np.asarray(inc)
        assert int(seeded.sum()) == int(info["seeded_ignitions"])
        assert int(inc.sum()) == int(info["collapse_events"])
        n_seeded += int(seeded.sum())
        n_collapse += int(inc.sum())
        state = state_next
        ep_return += float(reward)
        record(
            state, obs, jax.random.fold_in(k_step, _OBS_STREAM), ep_return, seeded, inc
        )
        if bool(done):
            break
    return rec, weak, n_seeded, n_collapse


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--scratch", required=True, help="checkpoint extraction dir")
    ap.add_argument("--only", default=None, help="one stem")
    args = ap.parse_args(argv)
    scratch = Path(args.scratch)
    scratch.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    cfg = load_config(str(REPO / CONFIG))
    ecfg = cfg.env
    for ep in EPISODES:
        if args.only and ep["stem"] != args.only:
            continue
        policy, ckpt_step = make_policy(ep, cfg, scratch)
        ref = RE.rollout_frames(jax.random.PRNGKey(EPISODE_SEED), ecfg, policy)
        ref_digest = [
            frame_digest(f["hazard"], f["smoke"], f["food"], f["pos"], f["alive"])
            for f in ref
        ]
        rec, weak, n_seeded, n_collapse = instrumented_rollout(
            jax.random.PRNGKey(EPISODE_SEED), ecfg, policy
        )
        assert len(ref_digest) == len(rec["digest"]) == ecfg.horizon + 1
        assert ref_digest == rec["digest"], (
            "trajectory differs from the original renderer"
        )
        committed = json.loads((RENDERS / f"{ep['stem']}.json").read_text())
        last = ref[-1]
        assert int(last["alive"].sum()) == committed["final_alive"]
        assert abs(last["completion"] - committed["final_completion"]) < 1e-12
        assert abs(last["return"] - committed["episode_return"]) < 1e-9
        assert int(last["t"]) == committed["steps"]
        smoke = np.stack(rec["smoke"])
        assert float(smoke.max()) <= 1.0 + 1e-7, smoke.max()
        np.savez_compressed(
            OUT / f"{ep['stem']}_frames.npz",
            hazard=np.stack(rec["hazard"]),
            smoke=smoke,
            food=np.stack(rec["food"]),
            pos=np.stack(rec["pos"]),
            alive=np.stack(rec["alive"]),
            structure=np.stack(rec["structure"]),
            weak=weak,
            reveal=np.stack(rec["reveal"]),
            tau=np.stack(rec["tau"]),
            seeded=np.stack(rec["seeded"]),
            collapse_inc=np.stack(rec["collapse_inc"]),
        )
        (OUT / f"{ep['stem']}_digests.json").write_text(
            json.dumps(
                {
                    "episode": ep["stem"],
                    "config": CONFIG,
                    "episode_key_seed": EPISODE_SEED,
                    "checkpoint_archive": ep["archive"],
                    "checkpoint_archive_sha256": ep.get("sha256"),
                    "allow_hash": ep.get("allow_hash"),
                    "checkpoint_step": ckpt_step,
                    "n_frames": len(ref_digest),
                    "frame_digest": (
                        "sha256 over hazard|smoke|food|agent_pos|agent_alive bytes"
                    ),
                    "reference": (
                        "che.scripts.render_episode.rollout_frames (unmodified)"
                    ),
                    "all_frames_equal_reference": True,
                    "final_matches_committed_render_json": True,
                    "seeded_ignitions_total": n_seeded,
                    "collapse_events_total": n_collapse,
                    "digests": rec["digest"],
                },
                indent=1,
            )
            + "\n"
        )
        print(
            f"{ep['stem']}: 257/257 frames equal the reference; "
            f"collapse events {n_collapse}, seeded ignitions {n_seeded}; "
            f"smoke max {smoke.max():.4f}"
        )


if __name__ == "__main__":
    main()
