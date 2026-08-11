"""M6.1 — emit the Phase-6 protocol configs from the registered design.

The mixture weights are design parameters with real arithmetic behind them
(c − p, 1 − 2c + p), and hand-typing 10 files of that is how a sweep ends up
silently unbalanced. So the arithmetic lives here, the emitted YAML is
committed and reviewable, and `test_phase6_configs.py` re-derives it and
compares — the files are explicit AND machine-checked.

Design registered in `phase6_design_v2.md`; rulings in `docs/decision_log.md`
("PHASE-6 REMEDY RULINGS", "PHASE-6 RULINGS, FINAL FIVE", and the seed
amendment).

  training severities  {0.43, 0.70}, uniform      held out: 0.49 (= theta*)
  ISO                  {A-only, B-only, d-only} x {sev}, 6 components
  JOINT-classic        {all-on} x {sev}, 2 components
  sweep  c = 0.5       p in {0, .125, .25, .375, .5}, 8 components each
  ident  c = 0.4       p in {0, .2, .4},              8 components each

ZERO-WEIGHT COMPONENTS ARE KEPT, deliberately. At p = 0 the joint cell has
weight 0 and at c = 0.5, p = 0 so does the pillar cell. Dropping them would
renumber the components between sweep points, and the per-component logging
channels (`mixture_w0..w7`) are indexed — `mixture_w2` must mean the same
component at every p or the realized-weight audit is unreadable.

Usage:
    uv run python -m che.scripts.make_phase6_configs            # write
    uv run python -m che.scripts.make_phase6_configs --locks    # registry block
"""

from __future__ import annotations

import argparse
from pathlib import Path

# Locked constants (docs/locks.yaml). Restated here ONLY as the generator's
# input; test_locks.py is what enforces agreement.
BETA_LOW, BETA_HIGH = 0.43, 0.70
KAPPA_A, KAPPA_B, DELTA_ON = 0.06, 1.0, 1.0
TRAIN_SEVERITIES = (("low", BETA_LOW), ("high", BETA_HIGH))

# (name, kappa_A, kappa_B, delta)
A_ONLY = ("a", KAPPA_A, 0.0, 0.0)
B_ONLY = ("b", 0.0, KAPPA_B, 0.0)
D_ONLY = ("d", 0.0, 0.0, DELTA_ON)
AB = ("ab", KAPPA_A, KAPPA_B, 0.0)
ALL_ON = ("joint", KAPPA_A, KAPPA_B, DELTA_ON)
PILLAR = ("pillar", 0.0, 0.0, 0.0)

OUT = Path("che/configs")


def _components(cells) -> list[dict]:
    """cells: [(elem_tuple, weight_within_severity)] -> flat component list."""
    out = []
    for sev_name, beta in TRAIN_SEVERITIES:
        for (elem, kA, kB, d), w in cells:
            out.append(
                {
                    "name": f"{elem}_{sev_name}",
                    "weight": round(w / len(TRAIN_SEVERITIES), 6),
                    "beta": beta,
                    "kappa_A": kA,
                    "kappa_B": kB,
                    "delta": d,
                }
            )
    return out


def iso() -> list[dict]:
    third = 1.0 / 3.0
    return _components([(A_ONLY, third), (B_ONLY, third), (D_ONLY, third)])


def joint() -> list[dict]:
    return _components([(ALL_ON, 1.0)])


def sweep(c: float, p: float) -> list[dict]:
    """Marginal-matched family: per-element marginal fixed at c, only
    co-occurrence varies. The no-element share is 1 - 2c + p and therefore
    moves 1:1 with p — structural, and reported, not hidden (v2 §2)."""
    a = b = c - p
    pillar = 1.0 - 2.0 * c + p
    assert min(a, b, p, pillar) >= -1e-12, (c, p, a, pillar)
    assert abs(a + b + p + pillar - 1.0) < 1e-9
    return _components([(A_ONLY, a), (B_ONLY, b), (AB, p), (PILLAR, pillar)])


# The two arms Gamma is defined on. Only these carry the Gamma(t) retention
# window (T* ruling, 2026-08-11); every secondary arm keeps the default 3.
CONFIRMATORY: frozenset[str] = frozenset({"p6_iso", "p6_joint"})

# T* and the checkpoint cadence, as the generator sees them. Kept beside the
# retention derivation so the two cannot drift apart silently.
T_STAR_UPDATES = 1000
CKPT_INTERVAL = 50


def gamma_t_retention(
    t_star: int = T_STAR_UPDATES, interval: int = CKPT_INTERVAL
) -> int:
    """Checkpoints that must be retained to cover the FINAL HALF of training.

    The registered Gamma(t) reading rule grades sign stability over the final
    half, so updates [T/2, T] must survive on disk. Orbax keeps the last
    `max_to_keep` saves at `interval` spacing, so that window needs
    T/(2*interval) + 1 of them -- 11 at T = 1000, interval 50.

    THIS IS A FUNCTION, NOT A CONSTANT, ON PURPOSE. Writing 11 would couple
    the registered window to T* by coincidence: if T* ever moved, 11 would
    silently stop meaning "the final half" and every test would stay green.
    That is the same provenance rot the T* ruling's item 7 was issued
    against, one layer down.
    """
    if t_star % (2 * interval):
        raise ValueError(
            f"T*={t_star} is not a whole number of half-intervals at "
            f"interval={interval}; the Gamma(t) window would be ragged."
        )
    return t_star // (2 * interval) + 1


PLAN: tuple[tuple[str, list[dict], str], ...] = (
    ("p6_iso", iso(), "ISO (D2): every element seen ONLY in isolation."),
    ("p6_joint", joint(), "JOINT-classic: all elements co-active."),
    *(
        (
            f"p6_sweep_c50_p{int(p * 1000):03d}",
            sweep(0.5, p),
            f"Dose sweep c=0.5, p={p}. No-element share {1 - 2 * 0.5 + p:.3f}.",
        )
        for p in (0.0, 0.125, 0.25, 0.375, 0.5)
    ),
    *(
        (
            f"p6_ident_c40_p{int(p * 1000):03d}",
            sweep(0.4, p),
            f"Identification arm c=0.4, p={p}. "
            f"No-element share {1 - 2 * 0.4 + p:.3f}.",
        )
        for p in (0.0, 0.2, 0.4)
    ),
)


def render(name: str, comps: list[dict], purpose: str) -> str:
    marg_a = sum(c["weight"] for c in comps if c["kappa_A"] > 0)
    marg_b = sum(c["weight"] for c in comps if c["kappa_B"] > 0)
    co = sum(c["weight"] for c in comps if c["kappa_A"] > 0 and c["kappa_B"] > 0)
    none = sum(
        c["weight"]
        for c in comps
        if c["kappa_A"] == 0 and c["kappa_B"] == 0 and c["delta"] == 0
    )
    lines = [
        f"# {name}.yaml — GENERATED by che/scripts/make_phase6_configs.py.",
        "# Do not hand-edit: test_phase6_configs.py re-derives every weight",
        "# and fails on drift. Registered design: phase6_design_v2.md.",
        "#",
        f"# {purpose}",
        "#",
        f"# Realized marginals: A {marg_a:.4f}  B {marg_b:.4f}  "
        f"co-occurrence {co:.4f}  no-element {none:.4f}",
        "# Training severities {0.43, 0.70}, uniform. beta = 0.49 is HELD OUT",
        "# (theta*) and must never appear here — enforced by test_locks.",
        "env:",
        "  grid_size: 64",
        "  n_agents: 12",
        "  horizon: 256",
        "  obs_window: 9",
        "  obs_version: 3",
        "  n_food: 32",
        "",
        "# Base theta: the locked constants. Every component states all four",
        "# traced fields explicitly, so nothing here is inherited by accident.",
        "theta:",
        f"  beta: {BETA_LOW}",
        f"  kappa_A: {KAPPA_A}",
        "  lambda_0: 5.0e-5",
        "  lambda_load: 4.0e-4",
        "  f_weak: 0.15",
        f"  kappa_B: {KAPPA_B}",
        "  delta: 0.0",
        "  r_comm: 16.0",
        "  death_penalty: 0.5",
        "  iota: 0.0",
        "  sigma_s: 1.0",
        "  eta: 0.5",
        "",
        "mixture:",
        "  components:",
    ]
    for c in comps:
        lines.append(
            f"    - {{name: {c['name']}, weight: {c['weight']}, "
            f"beta: {c['beta']}, kappa_A: {c['kappa_A']}, "
            f"kappa_B: {c['kappa_B']}, delta: {c['delta']}}}"
        )
    lines += [
        "",
        "train:",
        "  n_envs: 256",
        "  rollout_len: 128",
        "  n_minibatches: 4",
        "  n_epochs: 4",
        "  ckpt_interval: 50",
    ]
    # Gamma(t) robustness evidence (T* ruling, 2026-08-11). CONFIRMATORY arms
    # only: Gamma is the ISO-vs-JOINT contrast, so no secondary arm needs the
    # window and none gets the storage. Retention must cover the final HALF of
    # training -- see GAMMA_T_RETENTION for the relationship this number is a
    # solution of, and test_locks.py for its assertion.
    if name in CONFIRMATORY:
        lines += [
            f"  ckpt_max_to_keep: {gamma_t_retention()}"
            "  # Gamma(t) window: final half of training",
        ]
    lines += [""]
    return "\n".join(lines)


def locks_block() -> str:
    out = ["  # -- Phase-6 protocol configs (M6.1, GENERATED). Base theta carries",
           "  # the locked constants; the mixture components carry the treatment.",
           "  # test_phase6_configs.py checks every component against the locks and",
           "  # asserts none carries the held-out beta."]
    for name, _, purpose in PLAN:
        out += [
            f"  che/configs/{name}.yaml:",
            "    role: protocol",
            "    theta:",
            "      kappa_A: kappa_A",
            "      lambda_0: lambda_0",
            "      lambda_load: lambda_load",
            "      f_weak: f_weak",
            "      kappa_B: kappa_B",
            "      delta: delta_element_off",
            "      r_comm: r_comm",
            "      death_penalty: death_penalty",
            "    env:",
            "      obs_version: obs_version",
            "    explicit: [beta, kappa_A, kappa_B, delta, r_comm, death_penalty]",
            f"    note: {purpose!r}",  # quoted: notes contain ': '
        ]
    return "\n".join(out) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--locks", action="store_true", help="print registry block")
    args = ap.parse_args()
    if args.locks:
        print(locks_block())
        return
    for name, comps, purpose in PLAN:
        (OUT / f"{name}.yaml").write_text(render(name, comps, purpose))
        print(f"wrote {name}.yaml  ({len(comps)} components)")


if __name__ == "__main__":
    main()
