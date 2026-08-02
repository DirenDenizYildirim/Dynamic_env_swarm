"""M6.2 analysis — per-arm floors, the plateau guard, and the k recompute.

Grades nothing against a pre-set bar, because this milestone is what *makes*
the bars. What it does apply are the three STOP rules registered in advance
(`docs/decision_log.md`), so none of them can be chosen after seeing the
numbers:

  PLATEAU   final-tail-update slope vs zero, graded against the arm's OWN
            floor. Ratio above PLATEAU_PASS -> STILL CLIMBING -> STOP and
            re-rule the run length. PLATEAU_REVIEW labels a marginal band
            and is REPORTING ONLY -- it never changes a verdict.
  POWER     recompute confirmatory completion power at k = K_CONFIRMATORY on
            the MEASURED per-arm floors. Below POWER_STOP -> STOP and re-rule
            (seeds are $0.07). Smaller floors -> record the surplus and
            proceed.
  SHAKEDOWN any run that failed never reaches here (the job script exits).

Every threshold above is a registered constant mirrored in docs/locks.yaml
under `analysis:` and asserted by che/tests/test_locks.py.
"""

from __future__ import annotations

import argparse
import json
import math
import statistics
from pathlib import Path
from statistics import NormalDist

N = NormalDist()

# --------------------------------------------------------------------------
# REGISTERED ANALYSIS CONSTANTS. Every literal below is mirrored in
# `docs/locks.yaml` under `analysis:`, and `che/tests/test_locks.py` imports
# this module and asserts they agree. Change one without the other and the
# suite goes red — which is the whole point (analysis thresholds have no
# config to be reachable from, so this import IS their enforcement route).
K_CONFIRMATORY = 34  # seeds on ISO and JOINT-classic, the Gamma-graded arms
K_SECONDARY = 20  # seeds on the sweeps + identification arm
SIDAK_M = 2  # confirmatory family {Gamma_completion, Gamma_survival}
POWER_STOP = 0.80  # framing ruling, step (b); was 0.75 for M6.2 itself
PLATEAU_PASS = 1.0  # VERDICT-BEARING: drift/own-floor above this -> STOP
PLATEAU_REVIEW = 1.5  # REPORTING ONLY: marginal band, never a verdict
# --------------------------------------------------------------------------

TARGET_EFFECT = 0.03  # historical completion effect band (red team Part 3)
METRICS = ("completion", "survival_rate", "episode_return", "deaths_fire")


def _sidak_z(m: int = SIDAK_M, alpha_family: float = 0.05) -> float:
    a1 = 1.0 - (1.0 - alpha_family) ** (1.0 / m)
    return N.inv_cdf(1.0 - a1 / 2.0)


def _power(effect: float, sigma: float, k: int) -> float:
    """Two-sided power at the family-corrected alpha (CLAUDE.md standing
    rule: design-stage statements are 80 %-power MDEs, never bare 2-sigma)."""
    sd = sigma * math.sqrt(2.0 / k)
    return N.cdf(effect / sd - _sidak_z()) if sd > 0 else float("nan")


def _mde80(sigma: float, k: int) -> float:
    return (_sidak_z() + N.inv_cdf(0.80)) * sigma * math.sqrt(2.0 / k)


def _slope(pts: list[tuple[int, float]]) -> float:
    """OLS slope of y on the UPDATE NUMBER, i.e. per update by construction.

    Takes (update, y) pairs rather than a bare series on purpose. Completion
    is logged only on updates that finished an episode, so the series is
    gappy; regressing on position would silently return a per-logged-point
    slope. See the window comment in main() for the bug that cost.
    """
    n = len(pts)
    mx = sum(x for x, _ in pts) / n
    my = sum(y for _, y in pts) / n
    den = sum((x - mx) ** 2 for x, _ in pts)
    if not den:
        return 0.0
    return sum((x - mx) * (y - my) for x, y in pts) / den


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
    print("NO-PEEKING (ruled 2026-08-02): outcome MEANS are suppressed from")
    print("this report until unblinding — dispersion only. floors.json keeps")
    print("the raw values; they are needed then, not now.")
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
        print(f"    {'metric':<18}{'sd (FLOOR)':>12}{'range':>10}")
        for key in METRICS:
            v = vals[key]
            if len(v) < 2:
                continue
            sd = statistics.stdev(v)
            # The mean and the raw values go to floors.json, never to stdout:
            # the suppression is mechanical, not behavioral (ruling item 3).
            floors[arm][key] = {
                "mean": statistics.mean(v), "sd": sd,
                "range": max(v) - min(v), "n": len(v), "values": v,
            }
            print(f"    {key:<18}{sd:>12.4f}{max(v) - min(v):>10.4f}")
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
            # BUG FIXED (found in the M6.2 analysis): completion is NaN on
            # updates with no finished episode — with horizon 256 and
            # rollout_len 128 that is every other update. Slicing the
            # FILTERED series by --tail therefore covered 2x the updates it
            # claimed, inflating every reported drift ~2x.
            #
            # The window and the regression both run on the LOGGED UPDATE
            # NUMBER, so neither depends on how densely completion happens
            # to be logged. An earlier form of this fix rescaled a
            # position-based slope by len(win)/tail, which is exact only
            # under uniform spacing; it agreed to the digit on the M6.2 logs
            # (gap exactly 2 throughout) but the assumption is not one the
            # instrument should carry.
            pts = [(int(r["update"]), r["completion"]) for r in rows
                   if r.get("completion") is not None
                   and not (isinstance(r["completion"], float)
                            and math.isnan(r["completion"]))]
            if not pts:
                continue
            last = pts[-1][0]
            win = [(u, y) for u, y in pts if u > last - args.tail]
            if len(win) >= 3:
                slopes.append(_slope(win))
        if not slopes:
            continue
        # Total drift over the window vs the arm's OWN measured floor
        # (per-artifact rule). The verdict is binary at PLATEAU_PASS;
        # PLATEAU_REVIEW only labels, and must never gate.
        drift = statistics.mean(slopes) * args.tail
        sd_floor = floors.get(arm, {}).get("completion", {}).get("sd", float("nan"))
        have_floor = sd_floor == sd_floor and sd_floor > 0
        ratio = abs(drift) / sd_floor if have_floor else float("nan")
        climbing = ratio > PLATEAU_PASS if have_floor else False
        marginal = climbing and ratio <= PLATEAU_REVIEW
        plateau[arm] = {"mean_slope_per_update": statistics.mean(slopes),
                        "drift_over_window": drift, "floor_sd": sd_floor,
                        "ratio_to_floor": ratio,
                        "still_climbing": bool(climbing),
                        "review_band": bool(marginal)}
        if not climbing:
            verdict = "plateaued"
        elif marginal:
            verdict = "STILL CLIMBING (marginal — REVIEW band, not a verdict)"
        else:
            verdict = "STILL CLIMBING"
        print(f"  {arm:<12} drift over last {args.tail}: {drift:+.4f}   "
              f"floor sd {sd_floor:.4f}   ratio {ratio:.2f}x   -> {verdict}")
        if climbing:
            stop_plateau.append(arm)
    (out / "plateau.json").write_text(json.dumps(plateau, indent=1) + "\n")

    # ------------------------------------------------------------ power
    print("\n" + "=" * 72)
    print(f"POWER RECOMPUTE on measured floors (k = {K_CONFIRMATORY}, "
          f"Sidak m = {SIDAK_M})")
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
                flag = f"  <-- BELOW {POWER_STOP:.0%} STOP THRESHOLD"
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
