"""M6.2 analysis — per-arm floors, the plateau guard, and the k recompute.

Grades nothing against a pre-set bar, because this milestone is what *makes*
the bars. What it does apply are the three STOP rules registered in advance
(`docs/decision_log.md`), so none of them can be chosen after seeing the
numbers:

  PLATEAU   final-100-update slope vs zero, floor-graded. Still climbing at
            500 updates -> STOP and re-rule the run length.
  POWER     recompute confirmatory completion power at k = 34 on the MEASURED
            per-arm floors. Below 75 % -> STOP and re-rule (seeds are $0.07).
            Smaller floors -> record the surplus and proceed.
  SHAKEDOWN any run that failed never reaches here (the job script exits).
"""

from __future__ import annotations

import argparse
import json
import math
import statistics
from pathlib import Path
from statistics import NormalDist

N = NormalDist()
K_CONFIRMATORY = 34
POWER_STOP = 0.75
TARGET_EFFECT = 0.03  # historical completion effect band (red team Part 3)
METRICS = ("completion", "survival_rate", "episode_return", "deaths_fire")


def _sidak_z(m: int = 2, alpha_family: float = 0.05) -> float:
    a1 = 1.0 - (1.0 - alpha_family) ** (1.0 / m)
    return N.inv_cdf(1.0 - a1 / 2.0)


def _power(effect: float, sigma: float, k: int) -> float:
    """Two-sided power at the family-corrected alpha (CLAUDE.md standing
    rule: design-stage statements are 80 %-power MDEs, never bare 2-sigma)."""
    sd = sigma * math.sqrt(2.0 / k)
    return N.cdf(effect / sd - _sidak_z()) if sd > 0 else float("nan")


def _mde80(sigma: float, k: int) -> float:
    return (_sidak_z() + N.inv_cdf(0.80)) * sigma * math.sqrt(2.0 / k)


def _slope(ys: list[float]) -> float:
    """OLS slope per update over the tail window."""
    n = len(ys)
    xs = list(range(n))
    mx, my = sum(xs) / n, sum(ys) / n
    den = sum((x - mx) ** 2 for x in xs)
    if not den:
        return 0.0
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys, strict=True))
    return num / den


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", required=True)
    ap.add_argument("--reps", type=int, default=8)
    ap.add_argument("--arms", required=True, help="'name:cfg name:cfg ...'")
    ap.add_argument("--updates", type=int, default=500)
    ap.add_argument("--tail", type=int, default=100)
    args = ap.parse_args()
    out = Path(args.out)
    arms = [p.split(":")[0] for p in args.arms.split()]

    floors: dict = {}
    print("=" * 72)
    print("M6.2 — PER-ARM FLOORS (identical runs, same seed: nondeterminism)")
    print("=" * 72)
    for arm in arms:
        vals: dict[str, list[float]] = {m: [] for m in METRICS}
        for rep in range(1, args.reps + 1):
            f = out / f"eval_{arm}_rep{rep}.json"
            if not f.exists():
                print(f"  MISSING {f.name}")
                continue
            m = json.loads(f.read_text())["metrics"]
            for key in METRICS:
                if key in m:
                    vals[key].append(m[key]["mean"])
        floors[arm] = {}
        print(f"\n  {arm}  (n = {len(vals['completion'])})")
        print(f"    {'metric':<18}{'mean':>10}{'sd (FLOOR)':>12}{'range':>10}")
        for key in METRICS:
            v = vals[key]
            if len(v) < 2:
                continue
            sd = statistics.stdev(v)
            floors[arm][key] = {
                "mean": statistics.mean(v), "sd": sd,
                "range": max(v) - min(v), "n": len(v), "values": v,
            }
            print(f"    {key:<18}{statistics.mean(v):>10.4f}{sd:>12.4f}"
                  f"{max(v) - min(v):>10.4f}")
    (out / "floors.json").write_text(json.dumps(floors, indent=1) + "\n")

    # ---------------------------------------------------------- plateau
    print("\n" + "=" * 72)
    print(f"PLATEAU GUARD — final-{args.tail}-update slope vs zero, floor-graded")
    print("=" * 72)
    plateau: dict = {}
    stop_plateau = []
    for arm in arms:
        slopes = []
        for rep in range(1, args.reps + 1):
            f = out / f"{arm}_rep{rep}.jsonl"
            if not f.exists():
                continue
            rows = [json.loads(ln) for ln in f.read_text().splitlines() if ln.strip()]
            ys = [r["completion"] for r in rows
                  if r.get("completion") is not None
                  and not (isinstance(r["completion"], float)
                           and math.isnan(r["completion"]))]
            if len(ys) >= args.tail:
                slopes.append(_slope(ys[-args.tail:]))
        if not slopes:
            continue
        # Total drift over the window vs the arm's own measured floor.
        drift = statistics.mean(slopes) * args.tail
        sd_floor = floors.get(arm, {}).get("completion", {}).get("sd", float("nan"))
        climbing = abs(drift) > sd_floor if sd_floor == sd_floor else False
        plateau[arm] = {"mean_slope_per_update": statistics.mean(slopes),
                        "drift_over_window": drift, "floor_sd": sd_floor,
                        "still_climbing": bool(climbing)}
        verdict = "STILL CLIMBING" if climbing else "plateaued"
        print(f"  {arm:<12} drift over last {args.tail}: {drift:+.4f}   "
              f"floor sd {sd_floor:.4f}   -> {verdict}")
        if climbing:
            stop_plateau.append(arm)
    (out / "plateau.json").write_text(json.dumps(plateau, indent=1) + "\n")

    # ------------------------------------------------------------ power
    print("\n" + "=" * 72)
    print(f"POWER RECOMPUTE on measured floors (k = {K_CONFIRMATORY}, Sidak m = 2)")
    print("=" * 72)
    conf = [a for a in ("iso", "joint") if a in floors]
    power: dict = {}
    stop_power = []
    for arm in conf:
        for key in ("completion", "survival_rate"):
            s = floors[arm].get(key, {}).get("sd")
            if s is None:
                continue
            pw = _power(TARGET_EFFECT, s, K_CONFIRMATORY)
            power[f"{arm}.{key}"] = {
                "sigma": s, "mde80": _mde80(s, K_CONFIRMATORY),
                "power_at_target": pw,
            }
            flag = ""
            if key == "completion" and pw < POWER_STOP:
                flag = "  <-- BELOW 75% STOP THRESHOLD"
                stop_power.append(f"{arm}.{key}")
            print(f"  {arm:<8}{key:<16} sigma {s:.4f}  MDE80 "
                  f"{_mde80(s, K_CONFIRMATORY):.4f}  power@{TARGET_EFFECT} "
                  f"{pw:.1%}{flag}")
    (out / "power.json").write_text(json.dumps(power, indent=1) + "\n")

    # ------------------------------------------------------- eval cost
    t = out / "timings.txt"
    if t.exists():
        tr = [int(x.split()[1].rstrip("s")) for x in t.read_text().splitlines()
              if x.startswith("train_")]
        ev = [int(x.split()[1].rstrip("s")) for x in t.read_text().splitlines()
              if x.startswith("eval_")]
        if tr and ev:
            print("\n" + "=" * 72)
            print("MEASURED COST (discharges the v2 section-6 estimate)")
            print("=" * 72)
            print(f"  train  median {statistics.median(tr):.0f} s  (n={len(tr)})")
            print(f"  eval   median {statistics.median(ev):.0f} s  (n={len(ev)})")
            tot = statistics.median(tr) + statistics.median(ev)
            print(f"  per run total {tot:.0f} s")

    print("\n" + "=" * 72)
    if stop_plateau:
        print(f"VERDICT: STOP — still climbing at {args.updates} updates: "
              f"{stop_plateau}. Run length must be re-ruled.")
    elif stop_power:
        print(f"VERDICT: STOP — confirmatory completion power below "
              f"{POWER_STOP:.0%} on measured floors: {stop_power}. "
              "Re-rule the seed count (seeds are $0.07 each).")
    else:
        print("VERDICT: PROCEED — plateaued, and confirmatory power holds on "
              "the measured floors. Bars for the grid come from floors.json.")
    print("=" * 72)


if __name__ == "__main__":
    main()
