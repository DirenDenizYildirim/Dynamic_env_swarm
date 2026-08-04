"""E1.2 — is co-active visitation endogenous? Mediation framing, never causal.

Work package E1, milestone 2 (`env_native_prompt.md`). Zero compute; Phase
3-5 artifacts only, Phase 6 refused structurally.

THE PROMPT'S PREMISE IS RETRACTED, AND THAT IS LOAD-BEARING. The work package
motivates this milestone with "M4.3 established that policies regulate their
own exposure". `phase4_report.md` Result 3 **retracts that finding**: the 3x
suppression at Medium was a 200-update transient, by 500 updates trained
policies sit at or ABOVE the random-policy ceiling at every severity, and the
kappa_B = 0 control fails the test in the wrong direction. The ruling restated
it as a fire-avoidance byproduct, concluding: *perception attenuation is not
behaviourally suppressible -- the swarm cannot position its way out of it.*

So this milestone may NOT lean on M4.3. It has to establish endogeneity, or
fail to, on its own evidence. The prompt told us to read the retraction first;
this is what reading it changes.

THE TEST THAT ACTUALLY IDENTIFIES ENDOGENEITY. Two dispersions on the SAME
artifact and the same config hash:

  * `eval_floor_rep*`  -- identical config, identical seed, N reps.
    Spread = run-to-run NONDETERMINISM.
  * `eval_<arm>_s<N>`  -- same config, DIFFERENT training seeds.
    Spread = nondeterminism + WHICH POLICY YOU GOT.

If seed dispersion materially exceeds the reproducibility floor, policy
identity moves co-activity and it is endogenous. If they coincide, the
variation is nondeterminism and there is nothing for a policy to steer. This
is a same-artifact comparison, so it is a genuine floor grade -- unlike E1.1's
cross-artifact reference scales.

m55 pairs d0.0 (Medium) with its floor reps at hash 1602ca6bf2a8f357; m53b
pairs A_live (High) with its floor reps at hash fdeeea9aa9d1f4d2.

THE PURE BEHAVIOURAL PROBE. m55's `muted_s<N>` evaluates the SAME CHECKPOINTS
as `d0.0_s<N>` with the message channel cut at eval time -- identical weights,
identical config hash, one input changed. Any co-activity difference is
behaviour and nothing else. It pairs by seed, so it is analysed paired.

MEDIATION, NEVER CAUSAL REGRESSION. Realized co-activity is an outcome of the
policy, so regressing anything on it identifies nothing. Everything below is
descriptive. The pre-registered void rule (design v2 section 7) applies in
spirit: if realized dose does not vary with the assigned treatment, a dose
figure has no x-axis and is VOID.
"""

from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path

import numpy as np

from che.scripts.e1_inventory import _assert_not_phase6

# (label, dir, arm glob, floor glob, severity) -- arm and floor share a
# config hash in each pair; the script asserts it rather than trusting it.
PAIRS = (
    ("m55 / d0.0", "che/bench/results/phase5/m55",
     "eval_d0.0_s*.npz", "eval_floor_rep*.npz", "medium"),
    ("m53b / A_live", "che/bench/results/phase5/m53b",
     "eval_A_live_s*.npz", "eval_floor_rep*.npz", "high"),
)

# Same checkpoints, one eval-time input changed. Pure behaviour.
PAIRED_PROBE = ("che/bench/results/phase5/m55",
                "eval_d0.0_s{n}.npz", "eval_muted_s{n}.npz", (0, 1, 2, 3))

# Different TRAINING treatments, compared within milestone.
TREATMENTS = (
    ("m55 medium: delta 0.0 -> 1.0", "che/bench/results/phase5/m55",
     "eval_d0.0_s*.npz", "eval_d1.0_s*.npz"),
    ("m53b high: arm A_live -> B_live", "che/bench/results/phase5/m53b",
     "eval_A_live_s*.npz", "eval_B_live_s*.npz"),
    ("m44 low: kappa_B 0 -> locked", "che/bench/results/phase4/m44",
     "eval_low_kb0_*.npz", "eval_low_kbL_*.npz"),
    ("m44 medium: kappa_B 0 -> locked", "che/bench/results/phase4/m44",
     "eval_medium_kb0_*.npz", "eval_medium_kbL_*.npz"),
    ("m44 high: kappa_B 0 -> locked", "che/bench/results/phase4/m44",
     "eval_high_kb0_*.npz", "eval_high_kbL_*.npz"),
)

KEYS = ("coupling_co_active", "seeded_ignitions", "share")


def _means(npz: Path) -> dict[str, float]:
    _assert_not_phase6(npz)
    d = np.load(npz, allow_pickle=True)
    ca = float(np.asarray(d["coupling_co_active"], np.float64).mean())
    out = {"coupling_co_active": ca}
    if "seeded_ignitions" in d.files:
        si = float(np.asarray(d["seeded_ignitions"], np.float64).mean())
        out["seeded_ignitions"] = si
        out["share"] = ca / si if si else float("nan")
    return out


def _hash_of(npz: Path) -> str | None:
    j = npz.with_suffix(".json")
    return json.loads(j.read_text()).get("config_hash") if j.exists() else None


def _spread(files: list[Path]) -> dict:
    vals = [_means(f) for f in files]
    out: dict = {"n": len(vals)}
    for k in KEYS:
        xs = [v[k] for v in vals if v.get(k) == v.get(k)]
        if len(xs) >= 2:
            out[k] = {"mean": statistics.mean(xs), "sd": statistics.stdev(xs),
                      "min": min(xs), "max": max(xs)}
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default="che/bench/results/e1/endogeneity")
    args = ap.parse_args()
    results: dict = {}

    # ---------------------------------------------------------- test 1
    print("=" * 78)
    print("E1.2 TEST 1 — SEED DISPERSION vs REPRODUCIBILITY, same artifact")
    print("=" * 78)
    print("Same config hash, so this IS a floor grade, not a reference scale.")
    print("ratio > 1 => which policy you got moves co-activity => endogenous.\n")
    results["test1"] = {}
    for label, d, arm_g, fl_g, sev in PAIRS:
        arm = sorted(Path(d).glob(arm_g))
        flo = sorted(Path(d).glob(fl_g))
        ha, hf = {_hash_of(p) for p in arm}, {_hash_of(p) for p in flo}
        same_hash = ha == hf and len(ha) == 1
        sa, sf = _spread(arm), _spread(flo)
        print(f"  {label}  ({sev})   hash match: "
              f"{'YES' if same_hash else 'NO — grade is void'}  "
              f"[{ha.pop() if len(ha) == 1 else '*'}]")
        rec = {"severity": sev, "same_hash": same_hash,
               "seed": sa, "repro": sf, "ratio": {}}
        for k in KEYS:
            if k not in sa or k not in sf:
                continue
            r = sa[k]["sd"] / sf[k]["sd"] if sf[k]["sd"] else float("inf")
            rec["ratio"][k] = r
            print(f"      {k:<20} seed sd {sa[k]['sd']:.5f} (n={sa['n']})   "
                  f"repro sd {sf[k]['sd']:.5f} (n={sf['n']})   "
                  f"ratio {r:.2f}x")
        results["test1"][label] = rec
        print()

    # ---------------------------------------------------------- test 2
    print("=" * 78)
    print("E1.2 TEST 2 — SAME CHECKPOINTS, message channel cut at eval")
    print("=" * 78)
    print("Identical weights and config hash; only an input changed. Paired.\n")
    d, a_t, b_t, seeds = PAIRED_PROBE
    rows, deltas = [], []
    for n in seeds:
        pa, pb = Path(d) / a_t.format(n=n), Path(d) / b_t.format(n=n)
        if not (pa.exists() and pb.exists()):
            continue
        va, vb = _means(pa), _means(pb)
        rows.append((n, va, vb))
        deltas.append(vb["coupling_co_active"] - va["coupling_co_active"])
        print(f"  seed {n}: co_active {va['coupling_co_active']:.4f} -> "
              f"{vb['coupling_co_active']:.4f}   "
              f"delta {deltas[-1]:+.4f}")
    if deltas:
        md = statistics.mean(deltas)
        sd = statistics.stdev(deltas) if len(deltas) > 1 else float("nan")
        fl = results["test1"].get("m55 / d0.0", {}).get(
            "repro", {}).get("coupling_co_active", {}).get("sd")
        print(f"\n  paired mean delta {md:+.5f}  (sd of deltas {sd:.5f}, "
              f"n={len(deltas)})")
        if fl:
            print(f"  vs its OWN reproducibility floor {fl:.5f}  ->  "
                  f"{abs(md) / fl:.2f}x floor")
        results["test2"] = {"deltas": deltas, "mean": md, "sd": sd,
                            "floor": fl}

    # ---------------------------------------------------------- test 3
    print("\n" + "=" * 78)
    print("E1.2 TEST 3 — do TRAINING treatments move realized co-activity?")
    print("=" * 78)
    print("The Phase-6 dose figure needs YES. Graded on each pair's own")
    print("seed dispersion, pooled — the dispersion a contrast actually has.\n")
    results["test3"] = {}
    for label, d, ga, gb in TREATMENTS:
        fa, fb = sorted(Path(d).glob(ga)), sorted(Path(d).glob(gb))
        if not (fa and fb):
            continue
        sa, sb = _spread(fa), _spread(fb)
        rec: dict = {"n_a": sa["n"], "n_b": sb["n"]}
        line = f"  {label:<34}"
        for k in ("coupling_co_active", "share"):
            if k not in sa or k not in sb:
                continue
            delta = sb[k]["mean"] - sa[k]["mean"]
            # Pooled seed sd of the two arms -- the dispersion of the
            # quantity being contrasted, not of either arm alone.
            pooled = ((sa[k]["sd"] ** 2 + sb[k]["sd"] ** 2) / 2) ** 0.5
            rec[k] = {"delta": delta, "pooled_seed_sd": pooled,
                      "ratio": abs(delta) / pooled if pooled else float("inf")}
            line += (f"  {k.split('_')[0]}: {delta:+.4f} "
                     f"({rec[k]['ratio']:.1f}x pooled sd)")
        print(line)
        results["test3"][label] = rec

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "endogeneity.json").write_text(json.dumps(results, indent=1) + "\n")
    print(f"\nWrote {out / 'endogeneity.json'}")


if __name__ == "__main__":
    main()
