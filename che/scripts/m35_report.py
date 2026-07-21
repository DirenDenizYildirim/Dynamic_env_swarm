"""M3.5 report tables: aggregate the 12-cell acceptance-grid evals.

Reads che/bench/results/phase3/m35/eval_*.json (512 stochastic episodes
per cell) and prints the phase3_report.md M3.5 tables: per-cell metrics,
seed-pooled arm comparison per severity, and the M3.4-lock addendum
drift table (trained-policy realized structural observables vs the
random-policy calibration values from coupling_a_calibration.json).

    uv run python -m che.scripts.m35_report
"""

import itertools
import json
from pathlib import Path

import numpy as np

M35 = Path("che/bench/results/phase3/m35")
M34 = Path("che/bench/results/phase3/m34/coupling_a_calibration.json")

SEVERITIES = ("low", "medium", "high")
ARMS = ("ka0", "kaL")
SEEDS = (0, 1)
KEYS = (
    "completion",
    "survival_rate",
    "deaths_fire",
    "deaths_collapse",
    "collapse_events",
    "seeded_ignitions",
    "blocked_moves",
    "weak_occupancy",
)


def load() -> dict:
    per_ep = {}
    for sev, arm, s in itertools.product(SEVERITIES, ARMS, SEEDS):
        npz = np.load(M35 / f"eval_{sev}_{arm}_dp0.5_s{s}.npz")
        per_ep[(sev, arm, s)] = {k: npz[k] for k in KEYS}
    return per_ep


def main() -> None:
    per_ep = load()

    print("### per-cell means (512 episodes each)\n")
    hdr = "| cell | " + " | ".join(KEYS) + " |"
    print(hdr)
    print("|" + "---|" * (len(KEYS) + 1))
    for (sev, arm, s), d in per_ep.items():
        cells = " | ".join(f"{d[k].mean():.3f}" for k in KEYS)
        print(f"| {sev}_{arm}_s{s} | {cells} |")

    print("\n### seed-pooled arm comparison (1024 episodes per arm)\n")
    print("| severity | metric | ka=0 | ka=0.06 | delta |")
    print("|---|---|---|---|---|")
    for sev in SEVERITIES:
        for k in KEYS:
            a = np.concatenate([per_ep[(sev, "ka0", s)][k] for s in SEEDS])
            b = np.concatenate([per_ep[(sev, "kaL", s)][k] for s in SEEDS])
            print(
                f"| {sev} | {k} | {a.mean():.3f} | {b.mean():.3f} | "
                f"{b.mean() - a.mean():+.3f} |"
            )

    print("\n### M3.4-lock addendum: trained-policy drift vs calibration\n")
    calib = json.loads(M34.read_text())
    # Locked candidate = candidate 2 (index 1) of the factored design.
    locked = calib["candidates"][1]
    print(
        "| severity | metric | random-policy calib | trained (kaL, pooled)"
        " | band | flag |"
    )
    print("|---|---|---|---|---|---|")
    bands = {
        "collapse_events": (3.0, 10.0),
        "seeded_ignitions": (1.0, 5.0),
        "deaths_collapse": (0.05, 0.5),
    }
    calib_key = {
        "collapse_events": "n_collapses",
        "seeded_ignitions": "n_seeded",
        "deaths_collapse": "deaths_collapse",
    }
    for sev in SEVERITIES:
        for k, (lo, hi) in bands.items():
            trained = np.concatenate([per_ep[(sev, "kaL", s)][k] for s in SEEDS]).mean()
            ref = locked[sev][calib_key[k]]
            # Bands bind at Low (and Medium for the first two) per the
            # lock; flags are raised for Low only, per the addendum.
            flag = (
                "**FLAG**"
                if sev == "low" and not (lo <= trained <= hi)
                else "ok"
                if lo <= trained <= hi
                else "n/a (not binding)"
            )
            print(
                f"| {sev} | {k} | {ref:.3f} | {trained:.3f} | [{lo}, {hi}] | {flag} |"
            )


if __name__ == "__main__":
    main()
