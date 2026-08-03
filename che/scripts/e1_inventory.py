"""E1.0 — inventory of the co-active visitation counter, before any analysis.

Work package E1 (`env_native_prompt.md`), authorized by the allocation
correction (framing ruling item 3, docs/decision_log.md 2026-08-02). This is
NOT a protocol milestone and grades nothing. It READS committed artifacts.

WHAT THE COUNTER IS. `coupling_co_active` (invariant #5, che/env/env.py)
counts, per step, collapse-seeded ignitions within Chebyshev radius
`obs_window // 2` of an alive agent, at post-step positions. Logged in the
env info dict since day one on explicit instruction; never analysed.

  Coupling A (Def. 5) makes structural collapse CREATE hazard.
  Coupling B (Def. 6) makes that hazard's smoke BLIND the agent to it.
  The counter measures where those coincide within perception range.

THE PHASE-6 GUARD IS LOAD-BEARING, NOT DECORATION. M6.2/M6.2b eval artifacts
are Phase-6 CONFIRMATORY runs of the ISO and JOINT arms, and
`coupling_co_active` is an OUTCOME channel of those runs. Comparing it across
arms is a cross-arm outcome comparison, forbidden until unblinding (NO-PEEKING,
ruled 2026-08-02). The arm labels sit in the filenames and the data is right
there, so this script refuses phase6 paths structurally rather than by
convention -- see `_assert_not_phase6`.

TWO CHECKS THIS MILESTONE OWES:
  1. co_active <= seeded_ignitions, per episode, BY CONSTRUCTION (the
     co-active set is a subset of the seeded set, intersected with a
     dilated occupancy mask). If it ever fails, the counter or the dilation
     is wrong and every downstream claim is void -> STOP.
  2. The radius caveat: does `obs_window // 2` match the radius over which
     Coupling B actually attenuates? Reported by `radius_finding()`.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np

# Phases this package is allowed to read. Phase 6 is EXCLUDED by ruling.
ALLOWED_PHASES = ("phase3", "phase4", "phase5")
FORBIDDEN_PHASES = ("phase6",)

CHANNELS = (
    "coupling_co_active",
    "seeded_ignitions",
    "collapse_events",
    "blocked_moves",
    "danger_agents",
    "masked_danger_sum",
)


def _assert_not_phase6(path: Path) -> None:
    """Structural refusal, not a convention.

    The NO-PEEKING ruling forbids cross-arm outcome comparison of the
    Phase-6 confirmatory runs until unblinding. This package must never
    touch them, so the refusal is an assertion on every path that enters.
    """
    parts = {p.lower() for p in path.parts}
    for bad in FORBIDDEN_PHASES:
        if bad in parts:
            raise SystemExit(
                f"REFUSED: {path} is a {bad} artifact. M6.2/M6.2b are "
                "Phase-6 CONFIRMATORY runs and coupling_co_active is an "
                "outcome channel of them; comparing it across arms before "
                "unblinding violates the NO-PEEKING ruling (2026-08-02). "
                "If an analysis genuinely needs Phase-6 data, STOP and ask."
            )


def radius_finding(obs_window: int) -> dict:
    """Does the co-active radius match Coupling B's attenuation radius?

    Measured from the code paths, not asserted:

    * The counter uses `dilate(occ, obs_window // 2)`, and `dilate` is
      documented and implemented as CHEBYSHEV (L-inf) dilation with window
      `2*radius + 1` (che/env/structure.py).
    * The observation crop is `k x k` with `k = obs_window`, built by padding
      by `r = k // 2` and slicing at the agent position, so it spans exactly
      Chebyshev -r .. +r (che/env/observation.py).

    So on the OUTER BOUND the two agree exactly. What differs is the shape of
    attenuation INSIDE that bound: Coupling B's optical depth is
    `D = kappa_B * dist * mean_rho` with `dist` EUCLIDEAN, so within one
    Chebyshev shell the optical depth still varies by the ratio of the corner
    distance to the axis distance.
    """
    r = obs_window // 2
    axis, corner = float(r), math.hypot(r, r)
    return {
        "obs_window": obs_window,
        "co_active_radius_chebyshev": r,
        "crop_half_width_chebyshev": r,
        "outer_bound_matches": True,
        "euclidean_dist_at_shell_axis": axis,
        "euclidean_dist_at_shell_corner": corner,
        "optical_depth_ratio_corner_to_axis": corner / axis if axis else float("nan"),
    }


_SEVS = ("low", "medium", "high")


def _sev_from(config: str, fname: str) -> str | None:
    """Severity from the config name, falling back to the filename tag."""
    for s in _SEVS:
        if f"severity_{s}" in config or f"_{s}_" in fname or f"_{s}." in fname:
            return s
    return None


def _train_seed_from(fname: str) -> int | None:
    """Training seed from the `_s<N>` filename tag (NOT the eval seed)."""
    import re

    m = re.search(r"_s(\d+)", fname)
    return int(m.group(1)) if m else None


def _arm_from(fname: str) -> str:
    """The treatment tag a milestone encoded in the filename, e.g. ka0/kaL."""
    stem = fname.rsplit(".", 1)[0]
    drop = {"eval", "train", "npz"} | set(_SEVS)
    import re

    toks = [t for t in stem.split("_")
            if t not in drop and not re.fullmatch(r"s\d+", t)]
    return "_".join(toks) or "-"


def _load_pair(npz: Path) -> dict:
    _assert_not_phase6(npz)
    # Label as `<phase>/<milestone>`. m30b nests its evals one level deeper
    # (m30b/cross/), so walk up to the phase dir rather than assuming depth.
    parts = list(npz.parts)
    ph_i = next(i for i, p in enumerate(parts) if p in ALLOWED_PHASES)
    rec: dict = {
        "milestone": f"{parts[ph_i]}/{parts[ph_i + 1]}",
        "file": npz.name,
    }
    meta = npz.with_suffix(".json")
    if meta.exists():
        j = json.loads(meta.read_text())
        for k in ("config", "config_hash", "seed", "obs_version",
                  "ckpt_step", "n_episodes", "greedy"):
            rec[k] = j.get(k)
        # TWO SCHEMAS. The standard eval harness writes `config` + `seed`
        # (the EVAL seed; the TRAIN seed lives in the filename). m30b's
        # cross-severity matrix instead writes train/eval severity and seed
        # explicitly, and carries no `config` at all. Normalize both, so the
        # table has one meaning per column rather than two.
        rec["sev_train"] = j.get("train_severity") or _sev_from(
            j.get("config") or "", npz.name)
        rec["sev_eval"] = j.get("eval_severity") or rec["sev_train"]
        rec["seed_train"] = j.get("train_seed")
        if rec["seed_train"] is None:
            rec["seed_train"] = _train_seed_from(npz.name)
        rec["seed_eval"] = j.get("eval_seed", j.get("seed"))
        rec["arm"] = _arm_from(npz.name)
    d = np.load(npz, allow_pickle=True)
    present = set(d.files)
    rec["n_ep"] = int(d[next(iter(d.files))].shape[0]) if d.files else 0
    for c in CHANNELS:
        rec[f"has_{c}"] = c in present
    if "coupling_co_active" in present:
        ca = np.asarray(d["coupling_co_active"], dtype=np.float64)
        rec["co_active_mean"] = float(ca.mean())
        rec["co_active_max"] = float(ca.max())
        rec["co_active_nonzero_eps"] = int((ca > 0).sum())
        if "seeded_ignitions" in present:
            si = np.asarray(d["seeded_ignitions"], dtype=np.float64)
            rec["seeded_mean"] = float(si.mean())
            viol = int((ca > si).sum())
            rec["subset_violations"] = viol
            rec["worst_excess"] = float((ca - si).max())
        else:
            rec["subset_violations"] = None
    return rec


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--results", default="che/bench/results")
    ap.add_argument("--out", default="che/bench/results/e1/inventory")
    ap.add_argument("--obs-window", type=int, default=9)
    args = ap.parse_args()

    root = Path(args.results)
    # Select by SCHEMA, not by filename. m30b's cross-severity matrix is
    # named `train_<arm>_s<seed>_eval_<sev>.npz`, so an `eval_*.npz` glob
    # silently drops 27 eval artifacts -- a third of Phase 3's contribution.
    # An episode-level eval npz is identified by carrying the per-episode
    # metric channels; calibration npz (phase2, m33) do not.
    files: list[Path] = []
    for ph in ALLOWED_PHASES:
        for f in sorted((root / ph).rglob("*.npz")):
            try:
                names = set(np.load(f, allow_pickle=True).files)
            except Exception:
                continue
            if {"episode_return", "completion"} <= names:
                files.append(f)
    files = [f for f in files if "phase6" not in {p.lower() for p in f.parts}]

    print("=" * 74)
    print("E1.0 — CO-ACTIVE VISITATION INVENTORY (Phase 3-5 artifacts only)")
    print("=" * 74)
    print("Phase-6 artifacts are EXCLUDED BY RULING and refused structurally.")
    print(f"Scanned: {', '.join(ALLOWED_PHASES)} under {root}")
    print(f"Found {len(files)} eval npz.\n")

    recs = [_load_pair(f) for f in files]

    # ---------------------------------------------------- per-milestone roll-up
    print("-" * 74)
    print(f"{'milestone':<16}{'files':>6}{'has_ca':>8}{'has_si':>8}"
          f"{'ep':>6}{'ca>0 files':>12}{'obs_v':>7}")
    print("-" * 74)
    by_ms: dict[str, list[dict]] = {}
    for r in recs:
        by_ms.setdefault(r["milestone"], []).append(r)
    for ms in sorted(by_ms):
        g = by_ms[ms]
        has_ca = sum(1 for r in g if r.get("has_coupling_co_active"))
        has_si = sum(1 for r in g if r.get("has_seeded_ignitions"))
        nz = sum(1 for r in g if (r.get("co_active_nonzero_eps") or 0) > 0)
        eps = sorted({r.get("n_ep") for r in g})
        ov = sorted({r.get("obs_version") for r in g if r.get("obs_version")})
        print(f"{ms:<16}{len(g):>6}{has_ca:>8}{has_si:>8}"
              f"{str(eps[0] if len(eps) == 1 else '*'):>6}{nz:>12}"
              f"{str(ov[0] if len(ov) == 1 else '*'):>7}")
    print("-" * 74)
    print(f"{'TOTAL':<16}{len(recs):>6}"
          f"{sum(1 for r in recs if r.get('has_coupling_co_active')):>8}"
          f"{sum(1 for r in recs if r.get('has_seeded_ignitions')):>8}")

    # ------------------------------------------------------ the three tiers
    #
    # "Carries the counter" is NOT the same as "can be analysed for
    # co-activity", and neither is the same as "both couplings are live".
    # Coupling B masks the observation ONLY at obs v3 (observation.py gates
    # the whole masking path on `cfg.obs_version == 3`; v3 = v2 planes gated
    # by Coupling-B masking plus the visibility plane, docs/locks.yaml).
    tier1 = [r for r in recs if r.get("has_coupling_co_active")]
    tier2 = [r for r in tier1 if r.get("has_seeded_ignitions")]
    tier3 = [r for r in tier2 if r.get("obs_version") == 3]
    print("\n" + "=" * 74)
    print("THREE TIERS — what is actually analysable, and for what")
    print("=" * 74)
    print(f"  carries coupling_co_active            {len(tier1):>4} files")
    print(f"  + carries seeded_ignitions            {len(tier2):>4} files"
          "   <- co-activity is gradeable here")
    print(f"  + obs v3 (Coupling B actually masks)  {len(tier3):>4} files"
          "   <- BOTH couplings live")
    nz = sum(1 for r in tier2 if (r.get("co_active_nonzero_eps") or 0) > 0)
    print(f"  of the gradeable set, {nz} files have any co-active episode")

    # ------------------------------------------------- the by-construction check
    print("\n" + "=" * 74)
    print("SUBSET CHECK — co_active <= seeded_ignitions, per episode")
    print("=" * 74)
    checked = [r for r in recs if r.get("subset_violations") is not None]
    total_viol = sum(r["subset_violations"] for r in checked)
    print(f"  files checked: {len(checked)}   "
          f"episodes: {sum(r['n_ep'] for r in checked)}")
    print(f"  violations:    {total_viol}")
    if total_viol:
        print("\n  *** STOP — the subset relation FAILED. The counter or the")
        print("      dilation is wrong and every downstream E1 claim is void.")
        for r in checked:
            if r["subset_violations"]:
                print(f"      {r['milestone']}/{r['file']}: "
                      f"{r['subset_violations']} eps, "
                      f"worst excess {r['worst_excess']:+.1f}")
    else:
        print("  PASS — the counter is a subset of the seeded set everywhere.")

    # ------------------------------------------------------------ radius finding
    rf = radius_finding(args.obs_window)
    print("\n" + "=" * 74)
    print("RADIUS FINDING — does the co-active radius match Coupling B's?")
    print("=" * 74)
    print(f"  obs_window {rf['obs_window']}  ->  co-active Chebyshev radius "
          f"{rf['co_active_radius_chebyshev']}, crop half-width "
          f"{rf['crop_half_width_chebyshev']}")
    print("  OUTER BOUND: exact match. A cell outside the crop is not")
    print("    observed at all, so the binary Chebyshev test IS the correct")
    print("    'could this agent perceive it' boundary.")
    print("  INSIDE the bound the two differ: Coupling B's optical depth is")
    print("    D = kappa_B * dist * mean_rho with dist EUCLIDEAN, so at the")
    print(f"    outermost shell D varies by "
          f"{rf['optical_depth_ratio_corner_to_axis']:.3f}x between the axis "
          f"({rf['euclidean_dist_at_shell_axis']:.0f}) and the corner "
          f"({rf['euclidean_dist_at_shell_corner']:.3f})")
    print("    at equal smoke. The counter is therefore an OPPORTUNITY")
    print("    measure (geometric co-location), not a realized-perception")
    print("    one. It BOUNDS every claim in this package.")

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "inventory.json").write_text(json.dumps(
        {"records": recs, "radius_finding": rf,
         "subset_violations_total": total_viol,
         "n_files": len(recs)}, indent=1) + "\n")

    # ------------------------------------------------------ markdown table
    lines = [
        "# E1.0 — co-active visitation inventory (GENERATED)",
        "",
        "`che/scripts/e1_inventory.py`. Phase 3-5 only; Phase 6 refused",
        "structurally (NO-PEEKING, ruled 2026-08-02).",
        "",
        "`sev_eval` is the severity the checkpoint was EVALUATED at;",
        "`sev_train` the one it was trained at. They differ only in m30b,",
        "the cross-severity matrix. `co-active` and `seeded` are per-episode",
        "means over the file's episodes.",
        "",
        "| milestone | arm | sev_train | sev_eval | seed | obs_v | eps | "
        "co-active | seeded | ca<=si |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r in sorted(recs, key=lambda r: (r["milestone"], r["file"])):
        viol = r.get("subset_violations")
        ok = "n/a" if viol is None else ("OK" if viol == 0 else f"FAIL({viol})")
        ca = r.get("co_active_mean")
        si = r.get("seeded_mean")
        lines.append(
            f"| {r['milestone']} | {r.get('arm', '-')} | "
            f"{r.get('sev_train') or '?'} | {r.get('sev_eval') or '?'} | "
            f"{r.get('seed_train') if r.get('seed_train') is not None else '?'} | "
            f"{r.get('obs_version') or '?'} | {r['n_ep']} | "
            f"{'-' if ca is None else f'{ca:.4f}'} | "
            f"{'-' if si is None else f'{si:.4f}'} | {ok} |"
        )
    (out / "inventory.md").write_text("\n".join(lines) + "\n")
    print(f"\nWrote {out / 'inventory.json'} and {out / 'inventory.md'}")


if __name__ == "__main__":
    main()
