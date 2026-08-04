"""E1.1 — severity response of co-active visitation, floor-graded.

Work package E1, milestone 1 (`env_native_prompt.md`). Zero compute; reads
committed Phase 3-5 artifacts only. Phase 6 is refused structurally by
`e1_inventory._assert_not_phase6`, which every load here goes through.

THE PRE-REGISTERED PREDICTION (fixed in writing at `ce7ec3d`, before any
number below was computed):

    Coupling A is "marginal by construction" at High -- supercritical fire
    consumes the fuel collapse would ignite (coupling_a_lock.md) -- while
    Coupling B's masking ceiling RISES with severity (kappa_b_lock.md). So
    co-activity need not be monotone in severity, and MEDIUM MAY BE ITS PEAK.
    Medium is also theta*.

THE DECOMPOSITION THIS MILESTONE USES. `coupling_co_active` is summed over
steps per episode (che/eval/harness.py), and by E1.0's subset result it is a
subset of `seeded_ignitions`. So

    co_active = seeded x share,     share = P(seeded ignition near an agent)

which splits the severity response into Coupling A's PRODUCTIVITY (how much
hazard collapse creates, fuel-limited at High) and the NEAR-AGENT SHARE
(geometry and behaviour). Those are different mechanisms and the prediction
is really about the first, so reporting only their product would hide it.

FLOORS -- READ THIS BEFORE READING ANY GRADE.

Bars come with floors (CLAUDE.md), and floors are per-metric, per-hardware
AND per-artifact. The only identical-config replicate sets in Phase 3-5 are
`eval_floor_rep*` in m55 (Medium) and m53b (High), n = 4 each. Therefore:

  * There is NO reproducibility floor at Low, for any artifact.
  * There is NO reproducibility floor for m44 or m35 -- nobody ran identical
    reps of them -- so a severity contrast computed on those artifacts CANNOT
    be floor-graded on its own artifact, which is what the per-artifact
    amendment (2026-08-02) requires.

This module therefore does NOT pretend to floor-grade those contrasts. It
reports the m55/m53b floors as the only measured co-activity reproducibility
scale that exists in the project, labels every cross-artifact use of them as
a REFERENCE SCALE rather than a floor grade, and flags the rest UNDERPOWERED.
Inventing a threshold here is precisely the failure the standing rule names.
"""

from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path

import numpy as np

from che.scripts.e1_inventory import _assert_not_phase6

# n = 4 leaves an sd uncertain by roughly +-40 % (3 dof) -- M5.5 recorded
# this when it bought 8 reps over 4 for the Phase-6 floors.
FLOOR_N_WARN = 8

FLOOR_SETS = {
    "medium": ("che/bench/results/phase5/m55", "m55"),
    "high": ("che/bench/results/phase5/m53b", "m53b"),
}

# Severity-response grids. `arm_on` is the arm with the coupling ENABLED.
GRIDS = {
    "m44": {
        "dir": "che/bench/results/phase4/m44",
        "obs": 3,
        "arm_on": "kbL",
        "arm_off": "kb0",
        "note": "Coupling-B ablation; BOTH couplings live (obs v3)",
    },
    "m35": {
        "dir": "che/bench/results/phase3/m35",
        "obs": 2,
        "arm_on": "kaL",
        "arm_off": "ka0",
        "note": "Coupling-A ablation; obs v2, so Coupling B does NOT mask",
    },
}
SEVS = ("low", "medium", "high")


def _episode_means(npz: Path) -> dict[str, float]:
    """Per-file episode means of the channels E1 needs."""
    _assert_not_phase6(npz)
    d = np.load(npz, allow_pickle=True)
    out: dict[str, float] = {}
    for c in ("coupling_co_active", "seeded_ignitions", "collapse_events"):
        if c in d.files:
            out[c] = float(np.asarray(d[c], dtype=np.float64).mean())
    ca, si = out.get("coupling_co_active"), out.get("seeded_ignitions")
    # The share is undefined when Coupling A produced nothing; leave it None
    # rather than imputing 0, which would read as "never near an agent".
    out["share"] = (ca / si) if (ca is not None and si) else float("nan")
    return out


def measure_floors() -> dict:
    """Reproducibility floors from identical-config replicates."""
    floors: dict = {}
    for sev, (d, tag) in FLOOR_SETS.items():
        reps = sorted(Path(d).glob("eval_floor_rep*.npz"))
        if not reps:
            continue
        vals = [_episode_means(p) for p in reps]
        f: dict = {"milestone": tag, "n_reps": len(reps), "severity": sev}
        for key in ("coupling_co_active", "seeded_ignitions", "share"):
            xs = [v[key] for v in vals if v.get(key) == v.get(key)]
            if len(xs) >= 2:
                f[key] = {
                    "mean": statistics.mean(xs),
                    "sd": statistics.stdev(xs),
                    "range": max(xs) - min(xs),
                }
        floors[sev] = f
    return floors


def measure_grid(spec: dict) -> dict:
    """Per-severity, per-arm cells of a severity grid."""
    cells: dict = {}
    for npz in sorted(Path(spec["dir"]).glob("eval_*.npz")):
        if "floor_rep" in npz.name:
            continue
        name = npz.name
        sev = next((s for s in SEVS if f"_{s}_" in name), None)
        arm = spec["arm_on"] if f"_{spec['arm_on']}_" in name else (
            spec["arm_off"] if f"_{spec['arm_off']}_" in name else None)
        if sev is None or arm is None:
            continue
        cells.setdefault((sev, arm), []).append(_episode_means(npz))
    out: dict = {}
    for (sev, arm), vals in cells.items():
        rec: dict = {"n_seeds": len(vals)}
        for key in ("coupling_co_active", "seeded_ignitions", "share"):
            xs = [v[key] for v in vals if v.get(key) == v.get(key)]
            if xs:
                rec[key] = {
                    "mean": statistics.mean(xs),
                    "sd": statistics.stdev(xs) if len(xs) > 1 else None,
                    "min": min(xs), "max": max(xs), "n": len(xs),
                }
        out[f"{sev}|{arm}"] = rec
    return out


def _grade(delta: float, floor: float | None, same_artifact: bool) -> str:
    """Never invents a threshold; says what it cannot do."""
    if floor is None:
        return "NO FLOOR — UNDERPOWERED"
    ratio = abs(delta) / floor if floor else float("inf")
    scale = "floor" if same_artifact else "REFERENCE SCALE (cross-artifact)"
    return f"{ratio:.1f}x {scale}"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default="che/bench/results/e1/severity")
    args = ap.parse_args()

    print("=" * 78)
    print("E1.1 — SEVERITY RESPONSE OF CO-ACTIVE VISITATION")
    print("=" * 78)
    print("PRE-REGISTERED PREDICTION (ce7ec3d, before measurement):")
    print("  Coupling A is fuel-limited at High and Coupling B's masking")
    print("  ceiling rises with severity, so co-activity need NOT be monotone")
    print("  in severity — and MEDIUM MAY BE ITS PEAK. Medium is theta*.\n")

    floors = measure_floors()
    print("=" * 78)
    print("FLOORS — identical-config replicates, the only ones that exist")
    print("=" * 78)
    for sev in SEVS:
        f = floors.get(sev)
        if not f:
            print(f"  {sev:<7} NO REPRODUCIBILITY FLOOR EXISTS "
                  "(no identical-rep set at this severity)")
            continue
        ca, sh = f.get("coupling_co_active"), f.get("share")
        warn = "" if f["n_reps"] >= FLOOR_N_WARN else \
            f"   [n={f['n_reps']}: sd uncertain ~±40% (3 dof)]"
        print(f"  {sev:<7} {f['milestone']:<6} co_active sd {ca['sd']:.4f} "
              f"(range {ca['range']:.4f})   share sd "
              f"{sh['sd']:.4f}{warn}" if ca and sh else f"  {sev}: partial")

    # ------------------------------------------------ variance decomposition
    #
    # co_active = seeded x share. If the reproducibility floor of `seeded` is
    # far tighter than that of `share`, then run-to-run variation in
    # co-activity is inherited almost entirely from WHERE THE AGENTS ARE, not
    # from how much hazard collapse creates. That is a statement about which
    # half of the mechanism the policy actually controls, and it is measured
    # here rather than asserted.
    print("\n" + "=" * 78)
    print("RELATIVE FLOORS — which half of co_active = seeded x share moves?")
    print("=" * 78)
    for sev in SEVS:
        f = floors.get(sev)
        if not f:
            continue
        row = []
        for key in ("seeded_ignitions", "share", "coupling_co_active"):
            v = f.get(key)
            if v and v["mean"]:
                row.append(f"{key.split('_')[0]:<7}{v['sd'] / v['mean']:>7.2%}")
        print(f"  {sev:<7}{f['milestone']:<6} " + "   ".join(row))
    print("  If rel(co_active) ~ rel(share) >> rel(seeded), then ALL run-to-run")
    print("  variation in co-activity comes from agent positioning.")

    results: dict = {"floors": floors, "grids": {}}
    for tag, spec in GRIDS.items():
        grid = measure_grid(spec)
        results["grids"][tag] = {"spec": spec, "cells": grid}
        print("\n" + "=" * 78)
        print(f"{tag.upper()} — {spec['note']}")
        print("=" * 78)
        print(f"  {'cell':<16}{'n':>3}{'co_active':>12}{'seeded':>10}"
              f"{'share':>9}   {'spread(co_active)':>18}")
        for sev in SEVS:
            for arm in (spec["arm_on"], spec["arm_off"]):
                c = grid.get(f"{sev}|{arm}")
                if not c:
                    continue
                ca = c.get("coupling_co_active", {})
                si = c.get("seeded_ignitions", {})
                sh = c.get("share", {})
                spread = (f"[{ca.get('min', float('nan')):.3f}, "
                          f"{ca.get('max', float('nan')):.3f}]")
                shm = sh.get("mean")
                print(f"  {sev + '|' + arm:<16}{c['n_seeds']:>3}"
                      f"{ca.get('mean', float('nan')):>12.4f}"
                      f"{si.get('mean', float('nan')):>10.4f}"
                      f"{(float('nan') if shm is None else shm):>9.3f}"
                      f"   {spread:>18}")

        # ---- the severity contrast, on the coupling-ENABLED arm only
        on = spec["arm_on"]

        def floor_for(key: str, *sevs: str) -> float | None:
            # A floor is only a FLOOR on its own artifact. m44/m35 have no
            # identical-rep set, so m55/m53b floors are a REFERENCE SCALE.
            for s in sevs:
                if s in floors and key in floors[s]:
                    return floors[s][key]["sd"]
            return None

        for key, label in (("coupling_co_active", "co_active"),
                           ("share", "share = P(near agent | seeded)")):
            print(f"\n  SEVERITY CONTRASTS on {on} (coupling enabled), {label}:")
            for a, b in (("low", "medium"), ("medium", "high"),
                         ("low", "high")):
                va = grid.get(f"{a}|{on}", {}).get(key)
                vb = grid.get(f"{b}|{on}", {}).get(key)
                if not (va and vb):
                    continue
                delta = vb["mean"] - va["mean"]
                print(f"    {a:>6} -> {b:<7} delta {delta:+.4f}   "
                      f"{_grade(delta, floor_for(key, b, a), False)}")

        # ---- the coupling contrast WITHIN severity: does the ablated
        # element move co-activity at all? The counter is purely geometric,
        # so any effect here can only be ENDOGENOUS (via behaviour).
        off = spec["arm_off"]
        print(f"\n  {on} vs {off} WITHIN severity, co_active "
              "(any effect is endogenous — the counter is geometric):")
        for sev in SEVS:
            vo = grid.get(f"{sev}|{on}", {}).get("coupling_co_active")
            vf = grid.get(f"{sev}|{off}", {}).get("coupling_co_active")
            if not (vo and vf):
                continue
            delta = vo["mean"] - vf["mean"]
            print(f"    {sev:<7} {on} - {off} = {delta:+.4f}   "
                  f"{_grade(delta, floor_for('coupling_co_active', sev), False)}")

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "severity.json").write_text(json.dumps(results, indent=1) + "\n")
    print(f"\nWrote {out / 'severity.json'}")


if __name__ == "__main__":
    main()
