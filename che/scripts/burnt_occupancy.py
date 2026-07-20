"""M3.1b diagnostic: post-fire burnt-region occupancy, obs v1 vs v2 (D5).

For each m30b medium episode seed, roll out the exact rendered episode
(render_episode's key discipline — same seed, same trajectory) under
(a) the obs-v1 M3.0 medium checkpoint and (b) the obs-v2 M3.1b medium
checkpoint, and measure over the post-fire window (burning == 0, burnt
area > 0, any agent alive):

    occupancy_ratio = mean_t [ (alive agents on Burnt / alive agents)
                               / (Burnt cells / all cells) ]

ratio ~ 1 -> agents treat ash as ordinary terrain; << 1 -> ash avoidance
(the m30b "burnt-region abandonment" finding). Seeds whose fire fizzles
at t~1 leave a degenerate few-cell denominator — filter on postfire burnt
fraction when summarizing (see m31b_obs_v2.md).

Usage (CPU fine, ~8 min):
    uv run python che/scripts/burnt_occupancy.py <out.json>
"""

import dataclasses
import json
import sys

import jax
import numpy as np

from che.env.config import load_config
from che.env.types import BURNING, BURNT
from che.eval.harness import load_params, make_policy_fn
from che.scripts.render_episode import rollout_frames

CFG_PATH = "che/configs/severity_medium.yaml"
SEEDS = range(8)
RUNS = {
    "v1": dict(
        ckpt="che/bench/results/phase3/m30/ckpt_medium_dp0.5_s0",
        obs_version=1,
        # M3.0 checkpoint predates the M3.1/D5 config schema; recorded
        # escape hatch per the M3.0b sequencing decision.
        allow=("39ddff0c16947c43",),
    ),
    "v2": dict(
        ckpt="che/bench/results/phase3/m31b/ckpt_medium_v2_dp0.5_s0",
        obs_version=2,
        allow=(),
    ),
}


def main(out_path: str):
    out = {}
    for tag, spec in RUNS.items():
        cfg = load_config(CFG_PATH)
        cfg = dataclasses.replace(
            cfg,
            env=dataclasses.replace(
                cfg.env,
                obs_version=spec["obs_version"],
                theta=dataclasses.replace(cfg.env.theta, death_penalty=0.5),
            ),
        )
        params, _ = load_params(spec["ckpt"], cfg, allow_hashes=spec["allow"])
        policy = make_policy_fn(cfg, params)
        rows = []
        for seed in SEEDS:
            frames = rollout_frames(jax.random.PRNGKey(seed), cfg.env, policy)
            ratios, burnt_fracs = [], []
            for f in frames:
                burnt = f["hazard"] == BURNT
                n_alive = int(f["alive"].sum())
                if (f["hazard"] == BURNING).any() or not burnt.any() or n_alive == 0:
                    continue
                pos = f["pos"][f["alive"]]
                on_burnt = int(burnt[pos[:, 0], pos[:, 1]].sum())
                ratios.append((on_burnt / n_alive) / float(burnt.mean()))
                burnt_fracs.append(float(burnt.mean()))
            rows.append(
                dict(
                    seed=int(seed),
                    postfire_steps=len(ratios),
                    final_burnt_frac=burnt_fracs[-1] if burnt_fracs else 0.0,
                    occupancy_ratio=float(np.mean(ratios)) if ratios else None,
                    completion=frames[-1]["completion"],
                    alive=int(frames[-1]["alive"].sum()),
                )
            )
            print(tag, rows[-1])
        out[tag] = rows
    with open(out_path, "w") as fh:
        json.dump(out, fh, indent=1)
    print("wrote", out_path)


if __name__ == "__main__":
    main(sys.argv[1])
