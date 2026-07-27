"""M4.4 report tables: aggregate the 14-cell Coupling-B acceptance grid.

Reads che/bench/results/phase4/m44/eval_*.npz (512 stochastic episodes per
cell) plus the two post-grid calibration runs, and prints the
phase4_report.md M4.4 tables:

  1. per-cell means (14 cells)
  2. seed-pooled arm comparison per severity, with the seed-level spread
  3. coupling-co-active per-episode distribution (Prop.-4 diagnostic —
     the phase prompt asks for the distribution, not just the mean)
  4. danger-moment masking (M4.4 amendment 4a), pooled numerator /
     denominator, never an average of per-step conditional means
  5. cross-arm exposure control (amendment 2) — decides whether the
     provisional perception-exposure finding survives
  6. detection drift at the locked kappa_B (amendment 1; M3.5 precedent)
  7. m31b watch item: Medium coverage conditioned on burnt_fraction
  8. the four-condition inertness falsifier (amendment 3), evaluated

Statistics, with provenance stated precisely. The *falsifier* was logged
pre-data by the human (M4.4 amendment 3); the operationalization below of
its "within seed noise" clause was written by the RA after a first look
at the completion and survival means and before any table was produced.
It is a stated rule, NOT blind pre-registration, and the report says so.
The headline result (High survival) is insensitive to the choice — it
fires both clauses at |delta| = 3.0 sigma_seed with seed ranges 5 points
apart.

  sigma_seed = sqrt(mean over arms of Var(seed means, ddof=1))
  "within seed noise" := the two arms' per-seed value ranges OVERLAP
                         AND |delta| <= 2 * sigma_seed
  "separated"         := both clauses fail

Two seeds per arm (three at Medium) cannot support a formal test: a
seed-level permutation test has minimum two-sided p = 1/3 at 2v2 and
1/10 at 3v3, so no arrangement can reach 0.05. The rule above is
descriptive by necessity and is reported as such — the Phase-3
precedent ("seed ranges overlap on one side") is the same standard.

Episodes are CRN-paired across arms: che.eval.harness.evaluate derives
every episode key from the eval seed alone, and invariant #3 makes PRNG
consumption independent of kappa_B, so episode i starts from a bitwise
identical reset state in both arms (trajectories diverge only through
the actions). The paired per-episode SE is therefore printed as a
secondary figure; it conditions on the two trained policies and so
understates the uncertainty that matters here, which is over seeds.

    uv run python -m che.scripts.m44_report
"""

import argparse
import itertools
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

M44 = Path("che/bench/results/phase4/m44")
KAPPA_LOCKED = 1.0
SEVERITIES = ("low", "medium", "high")
ARMS = ("kb0", "kbL")
ARM_LABEL = {"kb0": "kappa_B=0", "kbL": f"kappa_B={KAPPA_LOCKED}"}
SEEDS = {"low": (0, 1), "medium": (0, 1, 2), "high": (0, 1)}

CELL_KEYS = (
    "completion",
    "survival_rate",
    "deaths_fire",
    "deaths_collapse",
    "burnt_fraction",
    "mean_smoke_exposure",
    "masked_frac",
    "coupling_co_active",
)
# Metrics compared arm-vs-arm. masked_frac / masked_danger_* are excluded:
# they are identically 0 in the kappa_B = 0 arm by construction (the
# nesting invariant), so a cross-arm delta there is a tautology.
COMPARE_KEYS = (
    "episode_return",
    "completion",
    "survival_rate",
    "deaths_fire",
    "deaths_collapse",
    "burnt_fraction",
    "mean_smoke_exposure",
    "coupling_co_active",
    "collapse_events",
    "seeded_ignitions",
)


def load() -> dict:
    per_ep = {}
    for sev in SEVERITIES:
        for arm, s in itertools.product(ARMS, SEEDS[sev]):
            npz = np.load(M44 / f"eval_{sev}_{arm}_dp0.5_s{s}.npz")
            per_ep[(sev, arm, s)] = {k: npz[k] for k in npz.files}
    return per_ep


def seed_means(per_ep: dict, sev: str, arm: str, key: str) -> np.ndarray:
    return np.array(
        [per_ep[(sev, arm, s)][key].mean() for s in SEEDS[sev]], dtype=np.float64
    )


def sigma_seed(a: np.ndarray, b: np.ndarray) -> float:
    """Pooled between-seed SD of the seed means (see module docstring)."""
    return float(np.sqrt(np.mean([a.var(ddof=1), b.var(ddof=1)])))


def classify(a: np.ndarray, b: np.ndarray) -> tuple[float, float, bool, str]:
    """(delta, sigma_seed, overlap, verdict) for arm b vs arm a.

    The binary verdict is the pre-committed rule. It is GRADED because
    the two clauses are not equally strong at this seed count:

      SEPARATED(strong) — ranges disjoint AND |delta| > 2 sigma_seed
      SEPARATED(weak)   — exactly one clause fires

    Range-disjointness alone is weak evidence: under the null, two
    2-seed arms have disjoint ranges in 2 of the 6 equally likely
    arrangements (p = 1/3), and 2 of 20 at 3v3 (p = 0.1). The
    |delta| > 2 sigma_seed clause alone is also weak, because
    Var(2 points, ddof=1) can collapse toward zero by chance and make
    2 sigma_seed absurdly small. Only findings that fire BOTH clauses
    are reported as robust.

    At 2 seeds per arm the second clause can never fire ALONE: writing r
    for an arm's range, sigma_seed = sqrt(r_a^2 + r_b^2) / 2, while
    overlapping intervals force |delta| <= (r_a + r_b) / 2, and
    (r_a + r_b)^2 <= 2 (r_a^2 + r_b^2). So overlap implies
    |delta| <= 2 sigma_seed, and at 2v2 "weak" always means "disjoint
    ranges, delta inside 2 sigma_seed". Pinned in test_m44_stats.py.
    """
    delta = float(b.mean() - a.mean())
    sig = sigma_seed(a, b)
    overlap = bool(a.min() <= b.max() and b.min() <= a.max())
    disjoint = not overlap
    exceeds = abs(delta) > 2.0 * sig
    if not disjoint and not exceeds:
        return delta, sig, overlap, "within-noise"
    if disjoint and exceeds:
        return delta, sig, overlap, "SEPARATED(strong)"
    return delta, sig, overlap, "SEPARATED(weak)"


def is_separated(verdict: str) -> bool:
    return verdict.startswith("SEPARATED")


def paired_se(per_ep: dict, sev: str, key: str) -> float:
    """SE of the CRN-paired per-episode difference, seeds concatenated.

    Secondary only: conditions on the sampled policies (see docstring).
    """
    n = min(len(SEEDS[sev]), len(SEEDS[sev]))
    diffs = []
    for s in SEEDS[sev][:n]:
        diffs.append(per_ep[(sev, "kbL", s)][key] - per_ep[(sev, "kb0", s)][key])
    d = np.concatenate(diffs).astype(np.float64)
    return float(d.std(ddof=1) / np.sqrt(d.size))


def pooled(per_ep: dict, sev: str, arm: str, key: str) -> np.ndarray:
    return np.concatenate([per_ep[(sev, arm, s)][key] for s in SEEDS[sev]])


def table_cells(per_ep: dict) -> None:
    print("### Per-cell means (512 episodes each)\n")
    print("| cell | " + " | ".join(CELL_KEYS) + " |")
    print("|" + "---|" * (len(CELL_KEYS) + 1))
    for sev in SEVERITIES:
        for arm, s in itertools.product(ARMS, SEEDS[sev]):
            d = per_ep[(sev, arm, s)]
            vals = " | ".join(f"{d[k].mean():.4f}" for k in CELL_KEYS)
            print(f"| {sev}_{arm}_s{s} | {vals} |")
    print()


def table_arms(per_ep: dict) -> dict:
    print("### Seed-pooled arm comparison\n")
    print(
        "| severity | metric | kappa_B=0 (per-seed) | "
        f"kappa_B={KAPPA_LOCKED} (per-seed) | delta | sigma_seed | "
        "paired SE | verdict |"
    )
    print("|---|---|---|---|---|---|---|---|")
    out = {}
    for sev in SEVERITIES:
        for k in COMPARE_KEYS:
            a = seed_means(per_ep, sev, "kb0", k)
            b = seed_means(per_ep, sev, "kbL", k)
            delta, sig, overlap, verdict = classify(a, b)
            pse = paired_se(per_ep, sev, k)
            fmt = "%.5f" if abs(a.mean()) < 0.01 else "%.4f"
            astr = ", ".join(fmt % v for v in a)
            bstr = ", ".join(fmt % v for v in b)
            mark = f"**{verdict}**" if is_separated(verdict) else verdict
            print(
                f"| {sev} | {k} | {a.mean():.4f} ({astr}) | "
                f"{b.mean():.4f} ({bstr}) | {delta:+.4f} | {sig:.4f} | "
                f"{pse:.5f} | {mark} |"
            )
            out[f"{sev}/{k}"] = {
                "kb0_seed_means": a.tolist(),
                "kbL_seed_means": b.tolist(),
                "delta": delta,
                "sigma_seed": sig,
                "ranges_overlap": overlap,
                "paired_se": pse,
                "verdict": verdict,
            }
    print()
    return out


def table_coactive(per_ep: dict) -> dict:
    print("### Coupling-co-active visitation — per-episode distribution\n")
    print(
        "| severity | arm | mean | share=0 | q50 | q75 | q90 | q99 | max |"
        " counts 0/1/2/3/4+ |"
    )
    print("|---|---|---|---|---|---|---|---|---|---|")
    out = {}
    for sev in SEVERITIES:
        for arm in ARMS:
            v = pooled(per_ep, sev, arm, "coupling_co_active").astype(np.float64)
            hist = [float((v == i).mean()) for i in range(4)] + [float((v >= 4).mean())]
            print(
                f"| {sev} | {ARM_LABEL[arm]} | {v.mean():.3f} | "
                f"{(v == 0).mean():.3f} | {np.quantile(v, 0.50):.0f} | "
                f"{np.quantile(v, 0.75):.0f} | {np.quantile(v, 0.90):.0f} | "
                f"{np.quantile(v, 0.99):.0f} | {v.max():.0f} | "
                + "/".join(f"{h:.3f}" for h in hist)
                + " |"
            )
            out[f"{sev}/{arm}"] = {
                "mean": float(v.mean()),
                "share_zero": float((v == 0).mean()),
                "q90": float(np.quantile(v, 0.90)),
                "max": float(v.max()),
                "hist_0_1_2_3_4plus": hist,
                "n_episodes": int(v.size),
            }
    print()
    return out


def table_danger(per_ep: dict) -> dict:
    """Amendment 4a: danger-moment masking, pooled num/den (never a mean
    of per-step conditional means). The danger *rate* is kappa_B-free by
    construction and so is comparable across arms; the masked share is
    identically 0 at kappa_B = 0 and is reported for the locked arm only.
    """
    print("### Danger-moment masking (amendment 4a) — diagnostic, not a band\n")
    print(
        "| severity | arm | danger rate (danger/alive) | masked_frac "
        "(unconditional) | masked_frac at danger moments | amplification |"
    )
    print("|---|---|---|---|---|---|")
    out = {}
    for sev in SEVERITIES:
        for arm in ARMS:
            num = pooled(per_ep, sev, arm, "masked_danger_sum").sum()
            den = pooled(per_ep, sev, arm, "danger_agents").sum()
            alive = pooled(per_ep, sev, arm, "alive_agents").sum()
            uncond = pooled(per_ep, sev, arm, "masked_frac").mean()
            rate = float(den / alive)
            cond = float(num / den) if den > 0 else float("nan")
            amp = cond / uncond if uncond > 0 else float("nan")
            cond_s = "0 (inert)" if arm == "kb0" else f"{cond:.4f}"
            amp_s = "n/a" if arm == "kb0" else f"{amp:.2f}x"
            print(
                f"| {sev} | {ARM_LABEL[arm]} | {rate:.4f} | {uncond:.5f} | "
                f"{cond_s} | {amp_s} |"
            )
            out[f"{sev}/{arm}"] = {
                "danger_rate": rate,
                "masked_frac_uncond": float(uncond),
                "masked_frac_danger": cond,
                "amplification": float(amp) if uncond > 0 else None,
            }
    print()
    return out


def table_exposure(per_ep: dict, calib: dict, m43: dict) -> dict:
    """Amendment 2: the kappa_B = 0 arm as the free control for the
    provisional perception-exposure finding. Identical lethality
    incentives, masking bitwise-inert; any positioning difference must
    then be perception-driven rather than a fire-avoidance byproduct.
    """
    print("### Cross-arm exposure control (amendment 2)\n")
    print(
        f"| severity | measure | kappa_B=0 | kappa_B={KAPPA_LOCKED} | delta | verdict |"
    )
    print("|---|---|---|---|---|---|")
    out = {}
    # (1) eval-side, seed-replicated.
    for sev in SEVERITIES:
        for key, label in (
            ("mean_smoke_exposure", "smoke exposure (alive agents)"),
            ("danger_rate", "danger rate (danger/alive)"),
        ):
            if key == "danger_rate":
                a = np.array(
                    [
                        per_ep[(sev, "kb0", s)]["danger_agents"].sum()
                        / per_ep[(sev, "kb0", s)]["alive_agents"].sum()
                        for s in SEEDS[sev]
                    ]
                )
                b = np.array(
                    [
                        per_ep[(sev, "kbL", s)]["danger_agents"].sum()
                        / per_ep[(sev, "kbL", s)]["alive_agents"].sum()
                        for s in SEEDS[sev]
                    ]
                )
            else:
                a = seed_means(per_ep, sev, "kb0", key)
                b = seed_means(per_ep, sev, "kbL", key)
            delta, sig, overlap, verdict = classify(a, b)
            print(
                f"| {sev} | {label} | {a.mean():.5f} | {b.mean():.5f} | "
                f"{delta:+.5f} | {verdict} |"
            )
            out[f"{sev}/{key}"] = {
                "kb0": float(a.mean()),
                "kbL": float(b.mean()),
                "kb0_seed_means": a.tolist(),
                "kbL_seed_means": b.tolist(),
                "delta": delta,
                "sigma_seed": sig,
                "verdict": verdict,
            }
    # (2) calibration-side positioning measures, evaluated at kappa = 1e6
    # on the states each policy actually visited, so they are kappa_B-free
    # observables of *where the swarm stood*. Seed-0 checkpoints, 64
    # episodes, no seed replication -> descriptive only.
    print(
        "\n| severity | measure (calib, seed-0 ckpt, 64 eps) | kappa_B=0 | "
        f"kappa_B={KAPPA_LOCKED} | delta |"
    )
    print("|---|---|---|---|---|")
    for sev in SEVERITIES:
        for key in ("masked_frac_ceiling", "exposed_agent_share"):
            a = calib["kb0"]["probe_policy"][sev][key]
            b = calib["kbL"]["probe_policy"][sev][key]
            print(f"| {sev} | {key} | {a:.4f} | {b:.4f} | {b - a:+.4f} |")
            out[f"{sev}/{key}"] = {"kb0": a, "kbL": b, "delta": b - a}

    # (3) The decisive table for the M4.3 provisional finding. The
    # random-policy reference is bitwise identical across the M4.3 and
    # M4.4 calibration runs (same engine, same seed, same protocol), so
    # the columns are directly comparable and differ only in the policy
    # being probed.
    print(
        "\n**masked_frac ceiling (kappa_B -> inf) by policy** — the M4.3 "
        "suppression finding re-measured against its two controls: "
        "training length (200 vs 500 updates) and the kappa_B = 0 arm.\n"
    )
    m43_cols = sorted(m43)
    cols = ["random"] + [f"M4.3 200u kB={k}" for k in m43_cols]
    cols += ["M4.4 500u kB=0", f"M4.4 500u kB={KAPPA_LOCKED}"]
    print("| severity | " + " | ".join(cols) + " |")
    print("|" + "---|" * (len(cols) + 1))
    for sev in SEVERITIES:
        row = [calib["kbL"]["random_policy"][sev]["masked_frac_ceiling"]]
        row += [m43[k]["probe_policy"][sev]["masked_frac_ceiling"] for k in m43_cols]
        row += [calib[a]["probe_policy"][sev]["masked_frac_ceiling"] for a in ARMS]
        print(f"| {sev} | " + " | ".join(f"{v:.4f}" for v in row) + " |")
        out[f"{sev}/ceiling_by_policy"] = dict(zip(cols, row, strict=True))

    # (4) Survivorship caveat, stated with the numbers that make it
    # unavoidable: mean_smoke_exposure averages over ALIVE agents, so an
    # arm that loses more agents mechanically reports lower exposure.
    # Conditioning on zero-death episodes does NOT fix this — it is a
    # collider, and the retained populations differ by arm.
    print("\n**Survivorship caveat for the exposure column**\n")
    print(
        "| severity | arm | zero-death episode share | exposure | ditto, zero-death |"
    )
    print("|---|---|---|---|---|")
    for sev in SEVERITIES:
        for arm in ARMS:
            surv = pooled(per_ep, sev, arm, "survival_rate")
            expo = pooled(per_ep, sev, arm, "mean_smoke_exposure")
            full = surv >= 1.0
            share = float(full.mean())
            print(
                f"| {sev} | {ARM_LABEL[arm]} | {share:.3f} | "
                f"{expo.mean():.5f} | {expo[full].mean():.5f} |"
            )
            out[f"{sev}/{arm}/zero_death"] = {
                "share": share,
                "exposure_all": float(expo.mean()),
                "exposure_zero_death": float(expo[full].mean()),
            }
    print()
    return out


def table_drift(calib: dict, m43: dict | None) -> dict:
    """Amendment 1: detection at the locked kappa_B under the 500-update
    M4.4 checkpoints, vs the 200-update M4.3 probes (M3.5 precedent).
    """
    print("### Detection drift at the locked kappa_B (amendment 1)\n")
    kappas = calib["kbL"]["kappa_candidates"]
    idx = kappas.index(KAPPA_LOCKED)
    band = calib["kbL"]["bands"]["detection_medium"]
    print(
        f"Detection band (Medium, the binding one): [{band[0]}, {band[1]}]. "
        f"Values are P(detect) at kappa_B = {KAPPA_LOCKED}, ring distance "
        f"{calib['kbL']['detection_ring']['distance']}.\n"
    )
    cols = ["random"] + [f"M4.3 probe kB={k}" for k in sorted(m43 or {})]
    cols += ["M4.4 kb0 (500u)", "M4.4 kbL (500u)"]
    print("| severity | " + " | ".join(cols) + " | in band (M4.4 kbL) |")
    print("|" + "---|" * (len(cols) + 2))
    out = {}
    for sev in SEVERITIES:
        row = [calib["kbL"]["random_policy"][sev]["detection"][idx]]
        for k in sorted(m43 or {}):
            row.append(m43[k]["probe_policy"][sev]["detection"][idx])
        row.append(calib["kb0"]["probe_policy"][sev]["detection"][idx])
        row.append(calib["kbL"]["probe_policy"][sev]["detection"][idx])
        ok = band[0] <= row[-1] <= band[1]
        print(
            f"| {sev} | "
            + " | ".join(f"{v:.4f}" for v in row)
            + f" | {'yes' if ok else 'NO'} |"
        )
        out[sev] = {"values": row, "columns": cols, "m44_kbL_in_band": bool(ok)}
    print()
    return out


def table_m31b(per_ep: dict) -> dict:
    """m31b watch item: coverage on fire-free episodes, conditioned on the
    per-episode burnt_fraction that the harness now carries (M4.0).
    """
    print("### m31b watch item — coverage conditioned on burnt_fraction\n")
    edges = [0.0, 0.05, 0.20, 0.40, 0.60, 1.01]
    labels = ["<0.05 (fire-free)", "0.05-0.20", "0.20-0.40", "0.40-0.60", ">0.60"]
    print("| severity | arm | " + " | ".join(labels) + " |")
    print("|" + "---|" * (len(labels) + 2))
    out = {}
    for sev in SEVERITIES:
        for arm in ARMS:
            bf = pooled(per_ep, sev, arm, "burnt_fraction")
            cm = pooled(per_ep, sev, arm, "completion")
            cells, rec = [], {}
            for i, lab in enumerate(labels):
                m = (bf >= edges[i]) & (bf < edges[i + 1])
                n = int(m.sum())
                cells.append(f"{cm[m].mean():.3f} (n={n})" if n else "- (n=0)")
                rec[lab] = {"completion": float(cm[m].mean()) if n else None, "n": n}
            print(f"| {sev} | {ARM_LABEL[arm]} | " + " | ".join(cells) + " |")
            out[f"{sev}/{arm}"] = rec
    print()
    return out


def falsifier(arms: dict, danger: dict, expo: dict) -> dict:
    """Amendment 3, verbatim: the coupling is inert at swarm scale iff
    (i) delta completion and survival are within seed noise, AND (ii)
    there is no cross-arm exposure/positioning difference, AND (iii)
    danger-moment masking is negligible, AND (iv) there is no co-active
    visitation difference. All four -> reportable negative result.
    """
    print("### Inertness falsifier (amendment 3, logged pre-data)\n")
    c1_hits = [
        f"{sev}/{k} ({arms[f'{sev}/{k}']['delta']:+.4f}, "
        f"{arms[f'{sev}/{k}']['verdict'].split('(')[1][:-1]})"
        for sev in SEVERITIES
        for k in ("completion", "survival_rate")
        if is_separated(arms[f"{sev}/{k}"]["verdict"])
    ]
    c1 = not c1_hits
    c2_hits = [
        f"{name} ({rec['delta']:+.5f}, {rec['verdict'].split('(')[1][:-1]})"
        for name, rec in expo.items()
        if is_separated(rec.get("verdict", ""))
    ]
    c2 = not c2_hits
    # (iii) "negligible" is read against the unconditional masked_frac it
    # is meant to correct: the diagnostic is non-negligible if danger
    # moments carry materially more masking than the swarm average.
    c3_hits = [
        f"{sev} ({danger[f'{sev}/kbL']['amplification']:.0f}x)"
        for sev in SEVERITIES
        if danger[f"{sev}/kbL"]["amplification"] is not None
        and danger[f"{sev}/kbL"]["amplification"] >= 2.0
    ]
    c3 = not c3_hits
    c4_hits = [
        f"{sev} ({arms[f'{sev}/coupling_co_active']['delta']:+.4f})"
        for sev in SEVERITIES
        if is_separated(arms[f"{sev}/coupling_co_active"]["verdict"])
    ]
    c4 = not c4_hits
    rows = [
        ("(i) completion/survival within seed noise", c1, c1_hits),
        ("(ii) no cross-arm exposure/positioning difference", c2, c2_hits),
        ("(iii) danger-moment masking negligible (<2x uncond.)", c3, c3_hits),
        ("(iv) no co-active visitation difference", c4, c4_hits),
    ]
    print("| condition | holds? | evidence against |")
    print("|---|---|---|")
    for label, ok, hits in rows:
        print(
            f"| {label} | {'yes' if ok else '**NO**'} | "
            f"{'-' if ok else '; '.join(hits)} |"
        )
    inert = c1 and c2 and c3 and c4
    print(
        f"\n**Verdict: {'INERT' if inert else 'NOT INERT'}** — all four "
        "conditions must hold for the reportable-negative-result branch.\n"
    )
    return {
        "conditions": {
            "i_completion_survival": c1,
            "ii_exposure_positioning": c2,
            "iii_danger_masking": c3,
            "iv_co_active": c4,
        },
        "counterexamples": {"i": c1_hits, "ii": c2_hits, "iii": c3_hits, "iv": c4_hits},
        "inert": bool(inert),
    }


def figure(per_ep: dict, out_path: Path) -> None:
    keys = [
        ("completion", "completion"),
        ("survival_rate", "survival rate"),
        ("mean_smoke_exposure", "smoke exposure"),
        ("coupling_co_active", "co-active visits / ep"),
    ]
    fig, axgrid = plt.subplots(2, 4, figsize=(15.5, 7.2))
    axes = axgrid[0]
    x = np.arange(len(SEVERITIES))
    w = 0.36
    for ax, (key, label) in zip(axes, keys, strict=True):
        for j, arm in enumerate(ARMS):
            mu = [seed_means(per_ep, s, arm, key).mean() for s in SEVERITIES]
            ax.bar(
                x + (j - 0.5) * w,
                mu,
                w,
                label=ARM_LABEL[arm],
                color=("#8c8c8c" if arm == "kb0" else "#c1440e"),
                alpha=0.85,
            )
            for i, sev in enumerate(SEVERITIES):
                pts = seed_means(per_ep, sev, arm, key)
                ax.scatter(
                    np.full(pts.size, x[i] + (j - 0.5) * w),
                    pts,
                    s=16,
                    c="k",
                    zorder=3,
                )
        ax.set_xticks(x)
        ax.set_xticklabels(SEVERITIES)
        ax.set_title(label, fontsize=10)
        ax.grid(axis="y", alpha=0.3)
    axes[0].set_ylabel("512 eps x seeds; dots = per-seed means")
    axes[0].legend(fontsize=8, loc="lower right")

    # Bottom row: the same four metrics as a cross-arm delta against the
    # decision rule. The absolute bars above start at zero (as they must),
    # which visually mutes an 8.8-point survival change; this row is where
    # the rule can actually be read off. Band = +/- 2 sigma_seed.
    for ax, (key, label) in zip(axgrid[1], keys, strict=True):
        for i, sev in enumerate(SEVERITIES):
            a = seed_means(per_ep, sev, "kb0", key)
            b = seed_means(per_ep, sev, "kbL", key)
            delta, sig, _, verdict = classify(a, b)
            ax.bar(
                x[i],
                delta,
                0.5,
                color=("#c1440e" if is_separated(verdict) else "#c8c8c8"),
                alpha=0.9,
            )
            ax.errorbar(x[i], 0.0, yerr=2 * sig, color="k", capsize=6, lw=1.2, zorder=3)
            if is_separated(verdict):
                ax.annotate(
                    "strong" if "strong" in verdict else "weak",
                    (x[i], delta),
                    textcoords="offset points",
                    xytext=(0, 7 if delta > 0 else -14),
                    ha="center",
                    fontsize=7,
                )
        ax.axhline(0.0, color="k", lw=0.8)
        ax.margins(y=0.20)  # headroom so the strong/weak labels clear the axis
        ax.set_xticks(x)
        ax.set_xticklabels(SEVERITIES)
        ax.set_title(f"delta {label}", fontsize=10)
        ax.grid(axis="y", alpha=0.3)
    axgrid[1][0].set_ylabel(
        "kappa_B=1.0 minus kappa_B=0\nbars = delta, whiskers = 2 sigma_seed"
    )

    fig.suptitle(
        "M4.4 acceptance grid — Coupling B ablation "
        f"(kappa_B = 0 vs {KAPPA_LOCKED}), dp=0.5, 500 updates",
        fontsize=11,
    )
    fig.tight_layout()
    fig.savefig(out_path, dpi=140)
    plt.close(fig)
    print(f"[figure] {out_path}")


def figure_coactive(per_ep: dict, out_path: Path) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(12.5, 3.6), sharey=True)
    bins = np.arange(-0.5, 9.5, 1.0)
    for ax, sev in zip(axes, SEVERITIES, strict=True):
        for arm, color in zip(ARMS, ("#8c8c8c", "#c1440e"), strict=True):
            v = pooled(per_ep, sev, arm, "coupling_co_active")
            ax.hist(
                np.clip(v, 0, 9),
                bins=bins,
                density=True,
                histtype="step",
                lw=1.8,
                color=color,
                label=ARM_LABEL[arm],
            )
        ax.set_title(f"{sev}", fontsize=10)
        ax.set_xlabel("co-active visits per episode (clipped at 9)")
        ax.grid(alpha=0.3)
    axes[0].set_ylabel("density")
    axes[0].legend(fontsize=8)
    fig.suptitle(
        "M4.4 — coupling-co-active per-episode distribution (Prop.-4 diagnostic)",
        fontsize=11,
    )
    fig.tight_layout()
    fig.savefig(out_path, dpi=140)
    plt.close(fig)
    print(f"[figure] {out_path}")


def main(argv=None) -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out-json", default=str(M44 / "m44_analysis.json"))
    p.add_argument("--fig", default=str(M44 / "m44_grid.png"))
    p.add_argument("--fig-coactive", default=str(M44 / "m44_coactive.png"))
    p.add_argument(
        "--m43-dir",
        default="che/bench/results/phase4/m43",
        help="M4.3 probe calibrations, for the drift column",
    )
    args = p.parse_args(argv)

    per_ep = load()
    calib = {
        arm: json.loads((M44 / f"m44_calibration_{arm}.json").read_text())
        for arm in ARMS
    }
    m43 = {}
    for f in sorted(Path(args.m43_dir).glob("coupling_b_calibration_probe_kB*.json")):
        kb = f.stem.split("kB")[-1]
        m43[kb] = json.loads(f.read_text())

    table_cells(per_ep)
    arms = table_arms(per_ep)
    coact = table_coactive(per_ep)
    danger = table_danger(per_ep)
    expo = table_exposure(per_ep, calib, m43)
    drift = table_drift(calib, m43)
    m31b = table_m31b(per_ep)
    verdict = falsifier(arms, danger, expo)

    figure(per_ep, Path(args.fig))
    figure_coactive(per_ep, Path(args.fig_coactive))

    Path(args.out_json).write_text(
        json.dumps(
            {
                "kappa_B_locked": KAPPA_LOCKED,
                "seeds": {k: list(v) for k, v in SEEDS.items()},
                "arm_comparison": arms,
                "co_active": coact,
                "danger_moment_masking": danger,
                "exposure_control": expo,
                "detection_drift": drift,
                "m31b_burnt_fraction_buckets": m31b,
                "inertness_falsifier": verdict,
            },
            indent=1,
        )
        + "\n"
    )
    print(f"[json] {args.out_json}")


if __name__ == "__main__":
    main()
