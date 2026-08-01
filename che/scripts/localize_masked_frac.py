"""M6.0 ladder — localize the traced-vs-folded GPU difference.

The GPU rerun floor measured EXACTLY ZERO (two identical baseline runs, 760
field digests, 0 differing), so by the ratified ladder any traced-vs-folded
difference is real and must be localized to a specific op rather than
absorbed by a tolerance.

Two info channels moved on severity_high seed 0 and nothing else did:
`masked_frac` and `masked_danger_sum`. Both are Def.-2-compliant diagnostics
that no kernel reads, and both are float reductions over the SAME obs grid —
whose digest did not change. This script dumps the per-step values so the
magnitude can be stated instead of assumed.

Run in each tree, then diff the two JSON files.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import struct
from pathlib import Path

import jax
import numpy as np

from che.env.config import load_config
from che.env.env import N_ACTIONS, reset, step


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--config", default="che/configs/severity_high.yaml")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--steps", type=int, default=32)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    cfg = load_config(args.config).env
    key = jax.random.PRNGKey(args.seed)
    key, k_reset = jax.random.split(key)
    _, state = reset(k_reset, cfg)

    rows = []
    for t in range(args.steps):
        key, k_act, k_step = jax.random.split(key, 3)
        actions = jax.random.randint(
            k_act, (cfg.n_agents,), 0, N_ACTIONS, dtype=np.int32
        )
        obs, state, _, _, info = step(k_step, state, actions, cfg)
        rows.append(
            {
                "t": t,
                # float64 host-side so the full float32 value is preserved
                "masked_frac": float(np.asarray(info["masked_frac"], np.float32)),
                "masked_danger_sum": float(
                    np.asarray(info["masked_danger_sum"], np.float32)
                ),
                "danger_agents": float(np.asarray(info["danger_agents"])),
                "alive_agents": float(np.asarray(info["alive_agents"])),
                # The input the two channels are reduced FROM. If this is
                # identical while the reductions differ, the difference is in
                # the reduction, not in Coupling B.
                "vis_plane_sum": float(
                    np.asarray(obs["grid"][..., -1], np.float32).sum()
                ),
                # sha256, NOT Python hash(): hash() of bytes is salted per
                # process, so comparing it across two runs is meaningless.
                "vis_plane_sha": hashlib.sha256(
                    np.ascontiguousarray(
                        np.asarray(obs["grid"][..., -1], np.float32)
                    ).tobytes()
                ).hexdigest()[:16],
                # Exact bit patterns. Two float32s can compare EQUAL and still
                # differ in bytes (+0.0 vs -0.0), which moves a digest while
                # moving no value — the distinction the ladder needs.
                "masked_frac_bits": struct.pack(
                    "<f", np.asarray(info["masked_frac"], np.float32)
                ).hex(),
                "masked_danger_sum_bits": struct.pack(
                    "<f", np.asarray(info["masked_danger_sum"], np.float32)
                ).hex(),
            }
        )

    Path(args.out).write_text(json.dumps({"rows": rows}, indent=1) + "\n")
    print(f"wrote {args.out} ({len(rows)} steps)")


if __name__ == "__main__":
    main()
