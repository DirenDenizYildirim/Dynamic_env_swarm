"""M6.2 analysis — per-arm floors, the plateau guard, and the k recompute.

Grades nothing against a pre-set bar, because this milestone is what *makes*
the bars. What it does apply are the three STOP rules registered in advance
(`docs/decision_log.md`), so none of them can be chosen after seeing the
numbers:

  PLATEAU   final-tail-update slope vs zero, graded against the arm's OWN
            floor. Ratio above PLATEAU_PASS -> STILL CLIMBING -> STOP and
            re-rule the run length. PLATEAU_REVIEW labels a marginal band
            and is REPORTING ONLY -- it never changes a verdict.
  POWER     recompute confirmatory power at k = K_CONFIRMATORY on the
            MEASURED floors, graded on the CONTRAST's SE — sd(Gamma) =
            sqrt((s_iso^2 + s_joint^2)/k), ruled 2026-08-03. The per-arm
            form assumes an equality of variance that per-artifact floors
            exist to deny; it survives here as a labelled diagnostic only.
  LADDER    resolve the pre-registered re-floor branch from k_req, the
            smallest k reaching POWER_STOP. A: proceed. B: raise k to k_req,
            no round-trip. C: run at K_LADDER_CAP and degrade honestly with
            an UNDERPOWERED flag. D: survival gone too -> broken box, STOP.
            The trigger is OUTCOME-BLIND: k_req reads fixed-seed rerun
            floors, never a cross-arm outcome.
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
K_CONFIRMATORY = 40  # seeds on ISO and JOINT-classic, the Gamma-graded arms
K_SECONDARY = 20  # seeds on the sweeps + identification arm
K_LADDER_CAP = 60  # branch B ceiling / branch C k, re-floor ladder
SIDAK_M = 2  # confirmatory family {Gamma_completion, Gamma_survival}
POWER_STOP = 0.80  # framing ruling, step (b); was 0.75 for M6.2 itself
PLATEAU_PASS = 1.0  # VERDICT-BEARING: drift/own-floor above this -> STOP
PLATEAU_REVIEW = 1.5  # REPORTING ONLY: marginal band, never a verdict
T_STAR = 1000  # REGISTERED fixed-budget estimand (T* ruling 2026-08-11)
# Gamma(t) robustness window (T* ruling, item 3). Checkpoints retained on the
# CONFIRMATORY arms so the final HALF of training survives for the post-unblind
# Gamma(t) stage. A SOLUTION of T_STAR / (2 * ckpt_interval) + 1, not an
# independent constant -- test_gamma_t_retention.py asserts the relationship
# against the live T_STAR so a future T* change fails loudly.
GAMMA_T_RETENTION = 11
# --------------------------------------------------------------------------

TARGET_EFFECT = 0.03  # historical completion effect band (red team Part 3)
METRICS = ("completion", "survival_rate", "episode_return", "deaths_fire")


def _sidak_z(m: int = SIDAK_M, alpha_family: float = 0.05) -> float:
    a1 = 1.0 - (1.0 - alpha_family) ** (1.0 / m)
    return N.inv_cdf(1.0 - a1 / 2.0)


def _sd_contrast(sigma_a: float, sigma_b: float, k: int) -> float:
    """SE of Gamma = mean(B) - mean(A), k seeds per arm.

    The COMBINED-variance form, ruled 2026-08-03 (decision_log, M6.2b
    CLOSE-OUT item 1). The per-arm `sigma*sqrt(2/k)` assumes the two arms
    share a variance, which per-artifact floors exist precisely to deny.
    """
    return math.sqrt((sigma_a**2 + sigma_b**2) / k)


def _power_contrast(effect: float, sigma_a: float, sigma_b: float,
                    k: int) -> float:
    """Two-sided power of the CONTRAST at the family-corrected alpha."""
    sd = _sd_contrast(sigma_a, sigma_b, k)
    return N.cdf(effect / sd - _sidak_z()) if sd > 0 else float("nan")


def _mde80_contrast(sigma_a: float, sigma_b: float, k: int) -> float:
    return (_sidak_z() + N.inv_cdf(0.80)) * _sd_contrast(sigma_a, sigma_b, k)


def _k_required(effect: float, sigma_a: float, sigma_b: float,
                target: float = POWER_STOP) -> int:
    """Smallest k whose CONTRAST power reaches `target` — the ladder's input.

    Closed form: sd_needed = effect / (z_sidak + z_target), and
    k = (sigma_a^2 + sigma_b^2) / sd_needed^2, rounded up.
    """
    sd_needed = effect / (_sidak_z() + N.inv_cdf(target))
    return math.ceil((sigma_a**2 + sigma_b**2) / sd_needed**2)


def _power_per_arm(effect: float, sigma: float, k: int) -> float:
    """DIAGNOSTIC ONLY — one arm's own dispersion, never a grade on Gamma.

    Superseded for contrasts 2026-08-03. Retained because the two per-arm
    reads BRACKET the contrast's power, which is a useful sanity display,
    and because the M6.2b report's figures were computed this way and must
    stay reproducible. Never feed this to a verdict.
    """
    sd = sigma * math.sqrt(2.0 / k)
    return N.cdf(effect / sd - _sidak_z()) if sd > 0 else float("nan")


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
                        "graded": bool(have_floor),
                        "still_climbing": bool(climbing),
                        "review_band": bool(marginal)}
        # An arm with NO floor is UNGRADED, never "plateaued". Without this
        # branch a missing floor (n = 1 rep, or a failed rep) makes `ratio`
        # NaN, and `NaN > PLATEAU_PASS` is False -> the arm printed as
        # PASSED. That is the void-reads-as-a-pass defect CLAUDE.md's "bars
        # come with floors" rule exists to prevent: a test finer than its
        # instrument is VOID, and a void test voids a PASS identically.
        # Verdict logic is unchanged and still binary at PLATEAU_PASS -- an
        # ungraded arm simply never enters `stop_plateau`, which is correct
        # for the secondary sweep (it does not gate) and is caught for the
        # confirmatory arms by the power section, which resolves no branch
        # unless BOTH are present.
        if not have_floor:
            verdict = "NO FLOOR — UNGRADED (not a pass)"
        elif not climbing:
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
    #
    # Graded on the CONTRAST's SE (ruled 2026-08-03). The per-arm reads are
    # printed first, labelled [diag], because they BRACKET the contrast and
    # seeing the bracket is informative -- but they never grade anything.
    print("\n" + "=" * 72)
    print(f"POWER on measured floors — CONTRAST basis (k = {K_CONFIRMATORY}, "
          f"Sidak m = {SIDAK_M})")
    print("=" * 72)
    conf = [a for a in ("iso", "joint") if a in floors]
    power: dict = {}
    for arm in conf:
        for key in ("completion", "survival_rate"):
            s = floors[arm].get(key, {}).get("sd")
            if s is None:
                continue
            pa = _power_per_arm(TARGET_EFFECT, s, K_CONFIRMATORY)
            power[f"diagnostic.{arm}.{key}"] = {
                "sigma": s, "power_at_target_per_arm": pa,
            }
            print(f"  [diag] {arm:<7}{key:<16} sigma {s:.4f}  per-arm "
                  f"power@{TARGET_EFFECT} {pa:.1%}")

    k_req: dict = {}
    if len(conf) == 2:
        print("  " + "-" * 68)
        for key in ("completion", "survival_rate"):
            si = floors["iso"].get(key, {}).get("sd")
            sj = floors["joint"].get(key, {}).get("sd")
            if si is None or sj is None:
                continue
            pw = _power_contrast(TARGET_EFFECT, si, sj, K_CONFIRMATORY)
            kr = _k_required(TARGET_EFFECT, si, sj)
            k_req[key] = kr
            power[f"contrast.{key}"] = {
                "sigma_iso": si, "sigma_joint": sj,
                "sd_gamma": _sd_contrast(si, sj, K_CONFIRMATORY),
                "mde80": _mde80_contrast(si, sj, K_CONFIRMATORY),
                "power_at_target": pw, "k_required": kr,
            }
            print(f"  GAMMA  {key:<16} sd(G) "
                  f"{_sd_contrast(si, sj, K_CONFIRMATORY):.5f}  MDE80 "
                  f"{_mde80_contrast(si, sj, K_CONFIRMATORY):.4f}  "
                  f"power@{TARGET_EFFECT} {pw:.1%}  k_req {kr}")
    else:
        print("  [contrast power needs BOTH confirmatory arms — not computed]")
    (out / "power.json").write_text(json.dumps(power, indent=1) + "\n")

    # --------------------------------------------------- the re-floor ladder
    #
    # Pre-registered 2026-08-03 (decision_log, M6.2b CLOSE-OUT item 6). It
    # replaces the human round-trip the bare POWER_STOP clause forced. The
    # trigger is OUTCOME-BLIND by construction: k_req is a function of
    # fixed-seed rerun floors only, and carries no cross-arm outcome
    # information.
    branch = action = None
    if "completion" in k_req:
        kr = k_req["completion"]
        surv = power.get("contrast.survival_rate", {}).get("power_at_target")
        if surv is not None and surv < POWER_STOP:
            branch, action = "D", (
                "STOP — survival power has also collapsed. That is not floor "
                "drift, it is a broken box. Different card; this is the only "
                "genuine round-trip left."
            )
        elif kr <= K_CONFIRMATORY:
            branch, action = "A", (
                f"PROCEED at k = {K_CONFIRMATORY}. Surplus recorded "
                f"(k_req = {kr})."
            )
        elif kr <= K_LADDER_CAP:
            branch, action = "B", (
                f"PROCEED at k = {kr}, no human round-trip. Registrar logs "
                f"k and the derived cost delta (+{2 * (kr - K_CONFIRMATORY)} "
                "runs)."
            )
        else:
            branch, action = "C", (
                f"PROCEED at k = {K_LADDER_CAP} and DEGRADE HONESTLY, never "
                f"chase (k_req = {kr}). completion-Gamma carries the "
                "pre-registered UNDERPOWERED flag with realized power "
                "stated; verdict weight shifts to the survival co-primary."
            )
        realized = _power_contrast(
            TARGET_EFFECT, floors["iso"]["completion"]["sd"],
            floors["joint"]["completion"]["sd"],
            min(max(kr, K_CONFIRMATORY), K_LADDER_CAP),
        )
        print("\n" + "=" * 72)
        print(f"RE-FLOOR LADDER: BRANCH {branch}")
        print("=" * 72)
        print(f"  k_req(completion) = {kr}   cap = {K_LADDER_CAP}   "
              f"realized power@{TARGET_EFFECT} = {realized:.1%}")
        print(f"  {action}")
        (out / "ladder.json").write_text(json.dumps({
            "branch": branch, "k_req": k_req, "k_cap": K_LADDER_CAP,
            "k_confirmatory": K_CONFIRMATORY, "realized_power": realized,
            "action": action,
        }, indent=1) + "\n")

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
    elif branch is None:
        print("VERDICT: INCOMPLETE — contrast power needs both confirmatory "
              "arms. No branch resolved; nothing is certified.")
    elif branch == "D":
        print("VERDICT: STOP — branch D. " + action)
    else:
        print(f"VERDICT: PROCEED — plateaued, ladder branch {branch}. "
              + action + " Bars for the grid come from floors.json; the "
              "confirmatory TEST uses the grid's own seed dispersion.")
    print("=" * 72)


if __name__ == "__main__":
    main()
