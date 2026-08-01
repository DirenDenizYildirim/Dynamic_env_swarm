"""M6.0 acceptance 2d — 50-update smoke train on a 2-component mixture.

What this has to show, per the ruling: the mixture actually drives TRAINING
(not just `reset` in a unit test), per-episode component labels are logged,
and the realized mixture ratio matches the declared weights.

The realized ratio comes from the `mixture_component` episode metric, which
is done-masked and averaged over finished episodes exactly like every other
M1.4 episode metric. With two components labelled 0/1 that mean IS the
realized weight of component 1. (A mean over indices only reads as a ratio
for two components — Phase 6's four-component design will need per-component
counts. Out of the spike's scope fence, and noted in `ippo.EP_METRICS`.)

The mixture used is the smallest one that exercises the machinery
end-to-end: an elements-OFF component (pillar only) against the config's own
all-elements theta, so the two components differ in kappa_A, kappa_B AND
delta simultaneously and a bug that dropped any one of them would show.

Usage (GPU box, repo root):
    uv run python -m che.scripts.smoke_mixture_train --out smoke_2d.json
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import math
import subprocess
import time
from pathlib import Path

import jax
import numpy as np

from che.env.config import MixtureComponent, MixtureConfig, load_config
from che.train.ippo import train

W_JOINT = 0.75  # declared weight of the all-elements component


def _provenance() -> dict:
    def _git(*a: str) -> str:
        try:
            return subprocess.check_output(
                ["git", *a], text=True, stderr=subprocess.DEVNULL
            ).strip()
        except Exception:  # noqa: BLE001
            return "unknown"

    return {
        "git_commit": _git("rev-parse", "HEAD"),
        "jax_version": jax.__version__,
        "device": jax.local_devices()[0].device_kind,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--config", default="che/configs/severity_medium.yaml")
    ap.add_argument("--updates", type=int, default=50)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", required=True)
    ap.add_argument("--metrics", default=None)
    args = ap.parse_args()

    cfg = load_config(args.config)
    mixture = MixtureConfig(
        components=(
            # index 0 — pillar only: every composable element off.
            MixtureComponent(
                name="pillar", weight=1.0 - W_JOINT, kappa_A=0.0, kappa_B=0.0,
                delta=0.0,
            ),
            # index 1 — the config's own theta (all elements as locked).
            MixtureComponent(name="joint", weight=W_JOINT),
        )
    )
    cfg = dataclasses.replace(
        cfg, env=dataclasses.replace(cfg.env, mixture=mixture)
    )
    th = cfg.env.theta
    print(
        f"base theta: beta={th.beta} kappa_A={th.kappa_A} kappa_B={th.kappa_B} "
        f"delta={th.delta}  n_envs={cfg.train.n_envs} horizon={cfg.env.horizon}",
        flush=True,
    )
    print(f"mixture: pillar {1 - W_JOINT:.2f} / joint {W_JOINT:.2f}", flush=True)

    t0 = time.perf_counter()
    _, history = train(
        cfg, n_updates=args.updates, seed=args.seed, metrics_path=args.metrics
    )
    wall = time.perf_counter() - t0

    def _series(name: str) -> np.ndarray:
        return np.asarray([h[name] for h in history], dtype=np.float64).ravel()

    # POOLED AS NUMERATOR / DENOMINATOR, not as a mean of per-update means.
    # Each update logs mixture_component = (sum of component labels at done) /
    # n_episodes for THAT update, and updates finish different numbers of
    # episodes. Averaging those ratios would weight a 1-episode update equally
    # with a 40-episode one — the exact error the M4.4 danger-moment and M5.0
    # comms channels are structured to avoid. Recovering the numerator and
    # pooling is exact given what is logged.
    comp = _series("mixture_component")
    n_eps = _series("n_episodes")
    ok = np.isfinite(comp) & np.isfinite(n_eps) & (n_eps > 0)
    numerator = float((comp[ok] * n_eps[ok]).sum())
    total_eps = float(n_eps[ok].sum())
    if total_eps == 0:
        raise SystemExit("no finished episodes — increase --updates")
    realized = numerator / total_eps
    # Binomial sd of the realized proportion over all finished episodes.
    sd = math.sqrt(W_JOINT * (1.0 - W_JOINT) / max(total_eps, 1.0))
    z = (realized - W_JOINT) / sd if sd > 0 else float("nan")

    result = {
        "provenance": _provenance(),
        "config": args.config,
        "updates": args.updates,
        "declared_weight_joint": W_JOINT,
        "realized_weight_joint": realized,
        "total_finished_episodes": total_eps,
        "binomial_sd": sd,
        "z": z,
        "wall_s": round(wall, 1),
        "updates_per_s": round(args.updates / wall, 3),
        "pooled_numerator": numerator,
        "final_completion": float(_series("completion")[ok][-1]),
        "final_survival": float(_series("survival_rate")[ok][-1]),
        "verdict": "MATCH" if abs(z) < 3.0 else "MISMATCH",
    }
    Path(args.out).write_text(json.dumps(result, indent=1) + "\n")

    print("\n=== acceptance 2d ===", flush=True)
    print(f"  declared weight (joint) : {W_JOINT}")
    print(f"  realized weight (joint) : {realized:.4f}")
    print(f"  finished episodes       : {total_eps:.0f}")
    print(f"  binomial sd / z         : {sd:.4f} / {z:+.2f}")
    print(f"  wall                    : {wall:.1f}s for {args.updates} updates")
    print(f"  VERDICT: {result['verdict']} (|z| < 3)")
    print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
